from flask import Flask, redirect, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from Config.Config import Config
'''from modulo_Depositos.Controller_Diposit import diposit_controller'''
from modulo_Depositos.Controller_Diposit.diposit_controller import diposit_controller
from modulo_Impulsores.Controller_Driving.driving_controller import driving_controller
from modulo_Valvulas.Controller_Valve.valve_controller import valve_controller

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db = SQLAlchemy(app)

def init_db(app):
    with app.app_context():
        db.create_all()

init_db(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mi API Flask"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(diposit_controller)
app.register_blueprint(driving_controller)
app.register_blueprint(valve_controller)

@app.route('/')
def index():
    return redirect(url_for('swagger_ui.show'))

if __name__ == '__main__':
    app.run(debug=True)