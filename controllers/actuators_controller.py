from flask import Blueprint, redirect, render_template, request
from flask_user import current_user, login_required, roles_accepted

from models.iot.actuators import Actuator

actuator_ = Blueprint("actuators", __name__, template_folder="templates")

@actuator_.route("/register_actuator")
@roles_accepted("Admin")
@login_required
def register_actuator():
    role_id = current_user.get_this_user_role().id
    return render_template("register_actuator.html", roles=role_id)

@actuator_.route("/add_actuator", methods=["POST"])
@roles_accepted("Admin")
@login_required
def add_actuator():
    actuator = request.form.get('actuator')
    topic = request.form.get('topic')
    is_active = True if request.form.get("is_active") == "on" else False
    print(actuator, topic, is_active)
    Actuator.save_actuator(actuator, topic, is_active)
    role_id = current_user.get_this_user_role().id
    return render_template("actuators.html", actuators=Actuator.get_actuators(), roles=role_id)

@actuator_.route("/edit_actuator")
@roles_accepted("Admin")
@login_required
def edit_actuator():
    role_id = current_user.get_this_user_role().id
    id = request.args.get("id", None)
    if id == None: render_template("actuators.html", actuators=Actuator.get_actuators(), roles=role_id)
    actuator = Actuator.get_single_actuator(id)
    return render_template("update_actuator.html", actuator=actuator, roles=role_id)

@actuator_.route("/update_actuator", methods=['POST'])
@login_required
def update_actuator():
    id = request.form.get("id")
    name = request.form.get("name")
    topic = request.form.get("topic")
    is_active = True if request.form.get("is_active") == "on" else False
    Actuator.update_actuator(id, name, topic, is_active)
    role_id = current_user.get_this_user_role().id
    return render_template("actuators.html", actuators=Actuator.get_actuators(), roles=role_id)

@actuator_.route("/actuators")
@login_required
def list_actuators():
    role_id = current_user.get_this_user_role().id
    return render_template("actuators.html", actuators=Actuator.get_actuators(), roles=role_id)

@actuator_.route("/del_actuator", methods=["GET"])
@roles_accepted("Admin")
@login_required
def del_actuator():
    id = request.args.get("id", None)
    actuators = Actuator.delete_actuator(id)
    role_id = current_user.get_this_user_role().id
    return render_template("actuators.html", actuators=actuators, roles=role_id)