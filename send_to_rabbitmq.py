from flask import Flask, request, jsonify
from cloudevents.http import from_http
import logging
import pika
import json

# Existing Flask application setup
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)

# Define RabbitMQ configuration
rabbitmq_config = {
    "RABBITMQ_HOST": "192.168.68.97",
    "RABBITMQ_USERNAME": "cs_creaevento",
    "RABBITMQ_PASSWORD": "Nuevo123*",
    "QUEUE_NAME": "vmware_VmRemovedEvent"
}

# Context manager for RabbitMQ connection
class RabbitMQConnection:
    def __init__(self, config):
        self.config = config

    def __enter__(self):
        self.credentials = pika.PlainCredentials(username=self.config["RABBITMQ_USERNAME"], password=self.config["RABBITMQ_PASSWORD"])
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.config["RABBITMQ_HOST"], credentials=self.credentials))
        self.channel = self.connection.channel()
        return self.channel

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

# CloudEvent route
@app.route('/', methods=['POST'])
def handle_cloud_event():
    try:
        event = from_http(request.headers, request.get_data(), None)

        data = event.data
        attrs = event._attributes

        app.logger.info(f"Received CloudEvent data: {data}")
        app.logger.info(f"CloudEvent attributes: {attrs}")

        # Convert the CloudEvent data to a JSON message
        json_message = json.dumps(data)

        # Publish the JSON message to RabbitMQ using the context manager
        try:
            with RabbitMQConnection(rabbitmq_config) as channel:
                channel.basic_publish(
                    exchange="",
                    routing_key=rabbitmq_config["QUEUE_NAME"],
                    body=json_message.encode('utf-8')  # Encode the message as bytes
                )
            app.logger.info(f"Sent message to {rabbitmq_config['QUEUE_NAME']}: {json_message}")
        except Exception as e:
            app.logger.error(f"Failed to publish message to RabbitMQ: {e}")

        return jsonify({"status": "success"}), 200

    except KeyError as e:
        sc = 400
        msg = f'could not decode cloud event: {e}'
        app.logger.error(msg)
        message = {
            'status': sc,
            'error': msg,
        }
        resp = jsonify(message)
        resp.status_code = sc
        return resp

    except Exception as e:
        sc = 500
        msg = f'could not process CloudEvent: {e}'
        app.logger.error(msg)
        message = {
            'status': sc,
            'error': msg,
        }
        resp = jsonify(message)
        resp.status_code = sc
        return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)