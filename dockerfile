# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install flask
RUN pip install pika
RUN pip install Werkzeug
RUN pip install cloudevents

# Copy your Python script into the container
COPY send_to_rabbitmq.py /app/send_to_rabbitmq.py

# Expose port 5000
EXPOSE 5000

# Run your Python script when the container launches
CMD ["python", "send_to_rabbitmq.py"]
