import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions


def get_db(): #funcion para obtener la base de datos y el cursor
    if 'db' not in g: #si es que no se encuentra el atributo db en g
        g.db=mysql.connector.connect( #entonces crea en g.db un conector para la base de datos
            host=current_app.config["DATABASE_HOST"],
            user=current_app.config["DATABASE_USER"],
            password=current_app.config["DATABASE_PASSWORD"],
            database=current_app.config["DATABASE"]
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c
                
def close_db(e=None): #funcion para cerrar la conexion a la base de datos
    db=g.pop('db', None) #con pop quitamos el atributo db

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)
    db.commit()

@click.command('init-db')
@with_appcontext

def init_db_command():
    init_db()
    click.echo("Base de datos inicializada")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)