import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_mapping( #definicion de variable de entorno
        SECRET_KEY="mikey",
        DATABASE_HOST=os.environ.get("FLASK_DATABASE_HOST"),
        DATABASE_PASSWORD=os.environ.get("FLASK_DATABASE_PASSWORD"),
        DATABASE_USER=os.environ.get("FLASK_DATABASE_USER"),
        DATABASE=os.environ.get("FLASK_DATABASE"),
    )

    from . import db

    db.init_app(app) 
    
    from . import auth
    from . import alma

    app.register_blueprint(auth.bp)
    app.register_blueprint(alma.bp)

    @app.route("/hola")
    def hola():
        return "hola mundo"

    return app


# $env:FLASK_APP="alma.py"
# $env:FLASK_ENV="development"
# $env:FLASK_DATABASE_HOST="localhost"
# $env:FLASK_DATABASE_PASSWORD="24204121"
# $env:FLASK_DATABASE_USER="beats7"
# $env:FLASK_DATABASE="db"