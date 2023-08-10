# Predictor de Demanda

A través de un modelo de Machine Learning, este proyecto nos da el top 10 de mejores productos a comprar en cuatro categorías, Notebooks, PCs, Tablets e Impresoras

## Software Stack
Debian 11.6
Python 3.9.2
Base de Datos SQLite

### Docker, Máquina Virtual, Sistema Operativa

Con una terminal situarse dentro del directorio raiz donde fue clonado este repositorio, por ej: ~/git/predictor/.
Una vez situado en la raiz del proyecto, dirigirse al directorio docker y ejecutar lo siguiente para construir la imagen docker:

`docker build -t predictor:version1.0 .`

Una vez construida la imagen, lanzar un contenedor montando un volumen que contenga el código del repositorio

`docker run -p 1438:1438 predictor:version1.0`

## Como instalar en servidor

#### Clonar el código de GitHub usando el siguiente comando

`git clone https://CristopherQuintana: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@github.com/CristopherQuintana/ML-Django.git`

##### Entrar a carpeta de proyecto

`cd ML-Django`

##### Instalar entorno virtual

`virutalenv venv`

##### Ingresar a entorno virtual

`source venv/bin/activate`

##### Instalar librerías

`pip install -r requirements.txt`

##### Ingresar a carpeta predictor, crear archivo .env

`cd predictor`
`nano .env`

##### Editar archivo .env con la siguiente línea de texto

`SECRET_KEY=to9qy&jvn3&x55i(&q0!iyttpghq-7n@yd%#xw$$=zii-p@1ls`

##### Volver a carpeta original

`cd ..`

##### Ejecutar código

`python manage.py runserver 146.83.198.35:1438`
## Construido con

Django
con ayuda de
Jupyter Notebook