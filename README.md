Alma-Miniproject
===

## Dependencias
* Python 3.9
* Mysql 5.7
* Docker (opcional)
* Docker-compose (opcional)
* Traefik (opcional)

## Despliegue basico:
Creamos la carpeta del entorno virtual y ejecutamos el script de activacion
```
$ cd alma
$ pip install virtualenv \
    && venv .venv \
    && source .venv/bin/activate
$ pip install requirements.txt
```

### Variables para la base de datos
```
$ export DATABASE_HOST=
$ export DATABASE_USER=
$ export DATABASE_PASSWORD=
$ export DATABASE=
```
### Flask Variables
```
$ export FLASK_ENV=development
$ export FLASK_APP=alma.py
```
### Run

```
$ flask run
```
## Despliegue con docker

```

```

