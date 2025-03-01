from flask import Flask
from models import *
from werkzeug.security import generate_password_hash

def create_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
        role_adm = Role.save_role( "Admin", "Usuário full" )
        role_est = Role.save_role( "Estatistico", "Usuário com acesso aos dados dos sensores")
        role_op = Role.save_role( "Operador", "Usuário com acesso aos dados dos atuadores")
        User.save_user("Admin", "admin@example.com","admin", role_adm)
        User.save_user("Estatistico", "estatistico@example.com","estatistico", role_est)
        User.save_user("Operador", "operador@example.com","operador", role_op)
        Actuator.save_actuator("Rele", "purificador/rele", 1)
        Actuator.save_actuator("Servo", "purificador/servo", 1)
        Sensor.save_sensor("Gas", "purificador/sensors/gas", 1)
        Sensor.save_sensor("Particula", "purificador/sensors/particles", 1)


