from flask import Blueprint, request, render_template, redirect
from flask_user import roles_accepted, login_required, current_user
from models.iot.sensors import Sensor

sensor_ = Blueprint("sensors", __name__, template_folder="views")

@sensor_.route("/register_sensor")
@roles_accepted("Admin")
@login_required
def register_sensor():
    role_id = current_user.get_this_user_role().id
    return render_template("register_sensor.html", roles=role_id)

@sensor_.route("/add_sensor", methods=["POST"])
@roles_accepted("Admin")
@login_required
def add_sensor():
    sensor = request.form.get('sensor')
    topic = request.form.get('topic')
    is_active = True if request.form.get("is_active") == "on" else False
    Sensor.save_sensor(sensor, topic, is_active)
    role_id = current_user.get_this_user_role().id
    return render_template("sensors.html", sensors=Sensor.get_sensors(), roles=role_id)

@sensor_.route("/edit_sensor")
@roles_accepted("Admin")
@login_required
def edit_sensor():
    id = request.args.get("sensor_id", None)
    role_id = current_user.get_this_user_role().id
    if id == None: render_template("sensors.html", sensors=Sensor.get_sensors(), roles=role_id)
    sensor = Sensor.get_single_sensor(id)
    return render_template("update_sensor.html", sensor=sensor, roles=role_id)

@sensor_.route("/update_sensor", methods=['POST'])
@roles_accepted("Admin")
@login_required
def update_sensor():
    id = request.form.get("id")
    name = request.form.get("name")
    topic = request.form.get("topic")
    is_active = True if request.form.get("is_active") == "on" else False
    Sensor.update_sensor(id, name, topic, is_active)
    role_id = current_user.get_this_user_role().id
    return render_template("sensors.html", sensors=Sensor.get_sensors(), roles=role_id)

@sensor_.route("/sensors")
@login_required
def list_sensors():   
    role_id = current_user.get_this_user_role().id
    return render_template("sensors.html", sensors=Sensor.get_sensors(), roles=role_id)

@sensor_.route("/del_sensor", methods=["GET"])
@roles_accepted("Admin")
@login_required
def del_sensor():
    id = request.args.get("id", None)
    sensors = Sensor.delete_sensor(id) 
    role_id = current_user.get_this_user_role().id
    return render_template("sensors.html", sensors=sensors, roles=role_id)