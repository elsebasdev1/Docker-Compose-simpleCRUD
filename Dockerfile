# 1. Usamos una imagen base oficial de Python.
# 'slim' es una versión ligera, buena para desarrollo/producción.
FROM python:3.9-slim

# 2. Establecemos el directorio de trabajo DENTRO del contenedor
WORKDIR /code

# 3. Copiamos PRIMERO el archivo de requisitos.
#    Esto aprovecha la caché de Docker: si no cambiamos los requisitos,
#    no se volverán a instalar en cada 'build'.
COPY requirements.txt requirements.txt

# 4. Instalamos las dependencias de Python
RUN pip install -r requirements.txt

# 5. Copiamos el resto del código de nuestra aplicación (el 'app.py')
COPY . .

# 6. El comando por defecto para ejecutar cuando se inicie el contenedor
CMD ["python", "app.py"]