README.md
Este documento proporciona información sobre cómo usar y administrar una aplicación de Python en un entorno de Kubernetes, junto con los comandos y configuraciones necesarios. La aplicación se encarga de manejar eventos de eliminación de máquinas virtuales (VM) y se integra con RabbitMQ. A continuación, se explican los pasos clave y los comandos necesarios.

Docker Build con Parámetros
Para construir una imagen de Docker con parámetros, utiliza el siguiente comando:

bash
Copy code
docker build --build-arg SECRET_FILE=config.json -t usoppone99/rabbitmq_vmremovedevent:1.0.X .
Este comando construye una imagen Docker llamada "usoppone99/rabbitmq_vmremovedevent" con la versión "1.0.X" y utiliza el archivo "config.json" como argumento durante la construcción.

Crear, Correr y Actualizar el Repositorio en Docker Hub
Para crear, correr y actualizar el repositorio en Docker Hub, sigue estos pasos:

bash
Copy code
# Construir la imagen Docker
docker build -t usoppone99/rabbitmq_vmremovedevent:1.0.X .

# Ejecutar el contenedor
docker run usoppone99/rabbitmq_vmremovedevent:1.0.X

# Subir la imagen al repositorio en Docker Hub
docker push usoppone99/rabbitmq_vmremovedevent:1.0.X
Estos comandos te permiten construir la imagen, ejecutar la aplicación en un contenedor y subirla a Docker Hub.

Aplicar el function.yaml en Kubernetes
Para aplicar la configuración definida en el archivo function.yaml, utiliza el siguiente comando:

bash
Copy code
kubectl -n vmware-functions apply -f function.yaml
Este comando aplica la configuración de Kubernetes especificada en el archivo function.yaml en el namespace "vmware-functions".

Revisar el function.yaml
Para revisar los detalles de la configuración definida en el archivo function.yaml, utiliza el siguiente comando:

bash
Copy code
kubectl describe -f function.yaml
Este comando muestra información detallada sobre la configuración de Kubernetes definida en el archivo function.yaml.

Listar el Contexto de Cluster de Kubernetes, Namespaces y PODs
Para listar los contextos de cluster de Kubernetes, los namespaces y los PODs en el clúster actual, utiliza el siguiente comando:

bash
Copy code
kubectl get pods -A
Este comando muestra una lista de todos los PODs en todos los namespaces del clúster actual.

Ejemplo de Resultado:
sql
Copy code
NAMESPACE            NAME                                                         READY   STATUS    RESTARTS   AGE
vmware-functions     kn-py-rabbitmq-handler-00001-deployment-66f4f78c6b-4djxp          2/2     Running   0          23m
vmware-functions     kn-py-rabbitmq-handler-dispatcher-6f5648c5cd-q8b8p                1/1     Running   0          23m
vmware-functions     kn-py-rabbitmq-handler-trigger-k27z7-dispatcher-67b69456ffz62vw   1/1     Running   0          23m
Este ejemplo muestra el estado de los PODs en el namespace "vmware-functions".

Visualizar los Logs de un POD
Para visualizar los logs de un POD específico en un namespace determinado, utiliza el siguiente comando:

bash
Copy code
kubectl logs -n vmware-functions <nombre-pod>
Reemplaza <nombre-pod> con el nombre del POD del cual deseas ver los logs.

Crear y Destruir PODs desde function.yaml
Puedes crear y destruir los PODs definidos en el archivo function.yaml utilizando los siguientes comandos:

Para crear los PODs:

bash
Copy code
kubectl -n vmware-functions apply -f function.yaml
Para destruir los PODs:

bash
Copy code
kubectl -n vmware-functions delete -f function.yaml
Asegúrate de que la configuración en function.yaml sea la deseada antes de aplicarla o eliminarla.

Pruebas Locales
Para ejecutar pruebas locales, sigue estos pasos:

Construye la imagen Docker en la carpeta donde se encuentra el Dockerfile:
bash
Copy code
docker build -t usoppone99/rabbitmq_vmremovedevent:1.0.4 .
Ejecuta el contenedor:
bash
Copy code
docker run -p 5000:5000 usoppone99/rabbitmq_vmremovedevent:1.0.4
En una ventana de comandos en la carpeta donde se encuentra el archivo .json, utiliza curl para enviar una solicitud POST a la aplicación:
bash
Copy code
curl -X POST http://localhost:5000 -H "Content-Type: application/json" -d @testevent.json
Configuración de la Cola de RabbitMQ
La configuración de la cola de RabbitMQ incluye las siguientes propiedades:

x-max-length: 5000
x-queue-type: classic
durable: true
Asegúrate de que RabbitMQ esté configurado de acuerdo con estas propiedades para que la aplicación funcione correctamente.

Crear un Secret en VEBA
Para crear un secret en VEBA, utiliza los siguientes comandos:

Desde la carpeta donde se encuentra el archivo json:

bash
Copy code
kubectl get secrets -n vmware-functions
kubectl -n vmware-functions create secret generic removevm-secret --from-file=config.json
O alternativamente, utilizando un nombre de archivo diferente:

bash
Copy code
kubectl -n vmware-functions create secret generic removevm-secret --from-file=VMREMOVE_SECRET=vmremove-secret.json
kubectl -n vmware-functions label secret removevm-secret app=veba-ui
Estos comandos crean un secret en el namespace "vmware-functions" a partir del archivo JSON proporcionado.

Visualizar el Archivo en Base64
Para visualizar el contenido del secret en formato base64, utiliza uno de los siguientes comandos:

bash
Copy code
kubectl get secret vmremove-secret -n vmware-functions -o json
kubectl get secret vmremove-secret -n vmware-functions -o=jsonpath='{.data}' > secret_base64.txt
O utilizando una ruta específica:

bash
Copy code
kubectl get secret vmremove-secret -n vmware-functions -o=jsonpath='{.data.VMREMOVE_SECRET}' > secret_base64.txt
Esto te permitirá ver el contenido del secret en formato base64.

Eliminar un Secret
Si necesitas eliminar un secret, puedes utilizar el siguiente comando:

bash
Copy code
kubectl delete secret removevm-secret -n vmware-functions
Este comando eliminará el secret llamado "removevm-secret" en el namespace "vmware-functions". Asegúrate de estar seguro antes de ejecutar este comando, ya que la información del secret no se podrá recuperar.
