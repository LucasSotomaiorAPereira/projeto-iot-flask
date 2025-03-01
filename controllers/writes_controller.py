from flask import Blueprint, request, render_template
from flask_user import login_required, roles_accepted, current_user
from models.iot.write import Write
from models.iot.actuators import Actuator

write = Blueprint("write",__name__, template_folder="views")

@write.route("/history_write")
@roles_accepted("Admin", "Operador")
@login_required
def history_write():
    actuators = Actuator.get_actuators()
    write = {}
    role_id = current_user.get_this_user_role().id
    return render_template("history_write.html", actuators = actuators, write = write, roles=role_id)

@write.route("/get_write", methods=['POST'])
@login_required
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        write = Write.get_write(id, start, end)
        actuators = Actuator.get_actuators()
        role_id = current_user.get_this_user_role().id
        return render_template("history_write.html", actuators = actuators, write = write, roles=role_id)