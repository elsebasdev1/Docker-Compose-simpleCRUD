Proyecto: CRUD de Tareas con Microservicios (Flask + Redis) y Docker Compose

Este proyecto es una aplicación web simple para gestionar una lista de tareas (CRUD: Crear, Leer, Actualizar, Borrar). Está construida siguiendo una arquitectura de microservicios y es orquestada usando Docker Compose.

Arquitectura

La aplicación se compone de dos servicios principales:

Un servidor web escrito en Python usando el micro-framework Flask.

Maneja toda la lógica de negocio (CRUD).

Sirve una interfaz de usuario (UI) renderizando una plantilla HTML.

Se comunica con el servicio redis para persistir los datos.

redis (Microservicio de Base de Datos):

Una base de datos en memoria Redis (usando la imagen oficial redis:alpine).

Almacena la lista de tareas.

No expone ningún puerto al exterior (a la máquina "host"); solo es accesible por el servicio web a través de la red interna de Docker.

Estructura de Archivos

/
├── docker-compose.yml   # El plano que define y conecta los servicios
├── Dockerfile           # Las instrucciones para construir la imagen de la app 'web'
├── app.py               # El código fuente de la aplicación Flask (rutas, lógica CRUD)
├── requirements.txt     # Las dependencias de Python (flask, redis)
├── templates/
│   └── index.html       # La plantilla HTML para la interfaz de usuario
│
└── start_app(change_route).bat  # Script para iniciar la app en Windows


docker-compose.yml: Orquesta el inicio de web y redis. Mapea el puerto 8000 de la máquina host al puerto 5000 del contenedor web.

Dockerfile: Construye la imagen del servicio web. Usa python:3.9-slim, instala las dependencias de requirements.txt y ejecuta app.py.

app.py: El cerebro de la aplicación. Define las rutas (/, /add, /delete, /update) y se conecta a Redis usando host='redis'.

requirements.txt: Lista las librerías de Python necesarias.

templates/index.html: La vista (frontend) que el usuario ve en el navegador.

Cómo Desplegar en una Nueva Máquina

Este es el proceso para ejecutar la aplicación completa en cualquier PC que tenga Docker Desktop instalado.

Prerrequisitos

Asegurarse de que Docker Desktop esté instalado.

Iniciar la aplicación Docker Desktop.

Opción 1: Despliegue con el Script

Haz clic derecho en el archivo start_app(change_route).bat y selecciona Editar.

Cambia la ruta C:\ruta\completa\a\tu\proyecto-docker por la ruta real donde copiaste la carpeta.

Guarda los cambios y haz doble clic en start_app(change_route).bat.

La terminal se abrirá, construirá la app y mostrará los logs.

Opción 2: Despliegue Manual

Abre una terminal,

Ejecuta el siguiente comando:

docker-compose up --build

Una vez que los contenedores estén corriendo, abre tu navegador web y ve a:

http://localhost:8000

Para limpiar y eliminar los contenedores y la red, ejecuta:

docker-compose down
