# Usar la imagen base de Python 3.9.17 en Debian Bullseye
FROM python:3.9.17-bullseye

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el contenido de los directorios del proyecto a /app en el contenedor
COPY . /app

# Instalar las dependencias del proyecto desde requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Instalar el cliente de PostgreSQL
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Exponer el puerto en el que Django está configurado para escuchar (si es necesario)
EXPOSE 1438

# Comando para ejecutar la aplicación Django (ajústalo según tus necesidades)
CMD ["python", "manage.py", "runserver", "0.0.0.0:1438"]