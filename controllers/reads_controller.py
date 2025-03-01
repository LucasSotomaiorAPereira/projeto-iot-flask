from flask import Blueprint, request, render_template
from flask_user import roles_accepted, login_required, current_user
from models.iot.read import Read
from models.iot.sensors import Sensor

read = Blueprint("read",__name__, template_folder="views")

@read.route("/history_read")
@roles_accepted("Admin", "Estatistico")
@login_required
def history_read():
    sensors = Sensor.get_sensors()
    read = {}
    role_id = current_user.get_this_user_role().id
    return render_template("history_read.html", sensors = sensors, read = read, roles=role_id)

@read.route("/get_read", methods=['POST'])
@login_required
def get_read():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        read = Read.get_read(id, start, end)
        sensors = Sensor.get_sensors()
        role_id = current_user.get_this_user_role().id
        return render_template("history_read.html", sensors = sensors, read = read,  roles=role_id)