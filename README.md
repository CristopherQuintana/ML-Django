# Predictor de Demanda

A través de un modelo de Machine Learning, este proyecto nos da el top 10 de mejores productos a comprar en cuatro categorías, Notebooks, PCs, Tablets e Impresoras

# Software Stack
Debian 11.6
Python 3.9.2
Base de Datos SQLite

### Docker, Máquina Virtual, Sistema Operativa

Con una terminal situarse dentro del directorio raiz donde fue clonado este repositorio, por ej: ~/git/predictor/.
Una vez situado en la raiz del proyecto, dirigirse al directorio docker y ejecutar lo siguiente para construir la imagen docker:

`docker build -t predictor:version1.0 .`

Una vez construida la imagen, lanzar un contenedor montando un volumen que contenga el código del repositorio

`docker run -p 1438:1438 predictor`

# Construido con

Django
con ayuda de
Jupyter Notebook