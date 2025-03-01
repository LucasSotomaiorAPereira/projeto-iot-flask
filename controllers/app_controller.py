from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from controllers.sensors_controller import sensor_
from controllers.login_controller import login
from controllers.actuators_controller import actuator_
from controllers.reads_controller import read
from controllers.writes_controller import write
from controllers.users_controller import user
from flask_mqtt import Mqtt
from models.db import db, instance
from flask_login import LoginManager
from flask_user import current_user, login_required, UserManager, roles_accepted
import time
import json
import _thread

from models.iot.read import Read
from models.iot.write import Write
from models.user.users import User

gas = 0
particula = 0
rele = 0
servo = 0
rele_antes = 0
servo_antes = 0


class CustomUserManager(UserManager):
    def unauthenticated_view(self):
        flash("Você deve fazer login para acessar essa pagina")
        return redirect("/")

    def unauthorized_view(self):
        flash("Você não tem permissão para acessar essa página")
        return redirect("/")


def create_app():
    app = Flask(__name__, template_folder="./views/",
                static_folder="./static/", root_path="./")

    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(actuator_, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'purificador-secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance

    db.init_app(app)

    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 5000
    app.config['MQTT_TLS_ENABLED'] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = 'leosaito632@gmail.com'
    app.config['MAIL_PASSWORD'] = 'password'
    app.config['MAIL_DEFAULT_SENDER'] = '"MyApp" <noreply@example.com>'

    mqtt_client = Mqtt()
    mqtt_client.init_app(app)

    topic_subscribe = "purificador/sensors"
    topic_subscribe_atuadores = "purificador/atuadores"

    app.secret_key = 'd54gdh543trg@!54gdh'
    login_manager = LoginManager()
    login_manager.init_app(app)

    user_manager = CustomUserManager(app, db, User)

    @app.route('/')
    def index():
        return render_template("login.html")

    @app.route('/sobre')
    @login_required
    def sobre():
        user = current_user
        role = user.get_this_user_role()
        return render_template("sobre.html", roles=role.id)

    @app.route('/home')
    @login_required
    def home():
        global gas, particula, servo, rele, servo_antes, rele_antes
        user = current_user
        role = user.get_this_user_role()
        values = {"gas": gas, "particula": particula}

        if servo == servo_antes and rele == rele_antes:
            if servo == "1" and rele == "1":
                return render_template('home.html', roles=role.id, values=values, user_role=role.name, valor="on")
            else:
                return render_template('home.html', roles=role.id, values=values, user_role=role.name, valor="livre")

        else:
            rele_antes = rele
            servo_antes = servo
            if servo == "1" and rele == "1":
                return render_template('home.html', roles=role.id, values=values, user_role=role.name, valor="on")
            else:
                return render_template('home.html', roles=role.id, values=values, user_role=role.name, valor="off")

    @app.route('/publish_message', methods=['GET', 'POST'])
    @login_required
    def publish_message():
        request_data = request.get_json()
        message = json.dumps({
            "valor": request_data['message']
        })
        Write.save_write(request_data['topic'], request_data['message'])
        publish_result = mqtt_client.publish(request_data["topic"], message)
        return jsonify(publish_result)

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe(topic_subscribe)
            mqtt_client.subscribe(topic_subscribe_atuadores)
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        global gas, particula, servo, rele
        js = json.loads(message.payload.decode())
        try:
            with app.app_context():
                gas = (js["gas"])
                particula = (js["particula"])
                Read.save_read("purificador/sensors/gas", gas)
                Read.save_read("purificador/sensors/particles",
                               particula)
        except:
            pass
        try:
            with app.app_context():
                servo = js['servo']
                rele = js['rele']
                Write.save_write("purificador/servo", servo)
                Write.save_write("purificador/rele", rele)
        except:
            pass

    @mqtt_client.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print("Disconnected from broker")

    return app
