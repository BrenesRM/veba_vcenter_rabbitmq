# docker build con parametros.
# to run: docker build --build-arg SECRET_FILE=config.json -t usoppone99/rabbitmq_vmremovedevent:1.0.X .

# Crea, corre y actualiza el repo en internet, hub docker.
# docker build -t usoppone99/rabbitmq_vmremovedevent:1.0.X .
# docker run usoppone99/rabbitmq_vmremovedevent:1.0.X
# docker push usoppone99/rabbitmq_vmremovedevent:1.0.X

# Aplicar el function.yaml
kubectl -n vmware-functions apply -f function.yaml

# Revisar el function.yaml
kubectl describe -f function.yaml

# Lista el contexto de cluster de kubernetes donde se encuentra, se muestran los namespaces y los PODS.
kubectl get pods -A

# Pod (Docker que contiene la aplicación):
vmware-functions     kn-py-rabbitmq-handler-00001-deployment-66f4f78c6b-4djxp          2/2     Running   0          23m  
# Pod que maneja el post de la aplicación:
vmware-functions     kn-py-rabbitmq-handler-dispatcher-6f5648c5cd-q8b8p                1/1     Running   0          23m  
# Pod que maneja el evento: vmremovedevent
vmware-functions     kn-py-rabbitmq-handler-trigger-k27z7-dispatcher-67b69456ffz62vw   1/1     Running   0          23m  

# Comando donde se visualiza los logs de POD, kubectl logs -n namespaces + nombre pod: kn-py-rabbitmq-handler-00001-deployment-66f4f78c6b-4djxp 
kubectl logs -n vmware-functions kn-py-rabbitmq-handler-00001-deployment-66f4f78c6b-4djxp  

# Comando para crear el pod del app y el handler, el pod de triguer se genera a la hora de asociarlo en el VEBA, en la parte de eventos.
kubectl -n vmware-functions apply -f function.yaml  

# Destruye los PODs creados en el function.yaml anteriormente, podría ser necesario eliminar primero el evento desde el VEBA y dspues el:
kubectl -n vmware-functions delete -f function.yaml  

Test local:

# Correr en la carpeta donde esta el dockerfile
docker build -t usoppone99/rabbitmq_vmremovedevent:1.0.4 .
docker run -p 5000:5000 usoppone99/rabbitmq_vmremovedevent:1.0.4

# En un cmd en la carpeta donde esta el .json.
curl -X POST http://localhost:5000 -H "Content-Type: application/json" -d @testevent.json


# En investigación.
curl -X POST http://kn-py-rabbitmq-handler.vmware-functions.bc-ifebv-102.central.bccr.fi.cr -H "Content-Type: application/json" -d @testevent.json

# Configuración de la cola:
Details
Features	
x-max-length:	5000
arguments:	
x-queue-type:	classic
durable:	true

# Crear un secret en VEBA, desde la carpeta donde se encuentra el json
kubectl get secrets -n vmware-functions 
kubectl -n vmware-functions create secret generic removevm --from-file=CONFIG_REMOVEVM=config_removevm.json  

# Remove a secret, kubectl delete secret <secret-name> -n <namespace>
kubectl delete secret removevm -n vmware-functions  

