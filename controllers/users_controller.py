
from flask import Blueprint, render_template, request
from flask_user import current_user, login_required, roles_accepted

from models.user.roles import Role
from models.user.user_roles import UserRoles
from models.user.users import User

user = Blueprint("user", __name__, template_folder="views")


@user.route('/register_user')
@roles_accepted("Admin")
@login_required
def register_user():
    role_id = current_user.get_this_user_role().id
    all_roles = Role.get_role()
    return render_template("register_user.html", roles=role_id, all_roles=all_roles)


@user.route('/add_user', methods=['POST'])
@roles_accepted("Admin")
@login_required
def add_user():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    role_name = request.form.get("role_name")
    role = Role.get_single_role(role_name)
    User.save_user(username, email, password, role)
    role_id = current_user.get_this_user_role().id
    return render_template("users.html", users=User.get_users(),roles=role_id)

@user.route("/edit_user")
@roles_accepted("Admin")
@login_required
def edit_user():
    role_id = current_user.get_this_user_role().id
    id = request.args.get("user", None)
    if id == None: render_template("users.html", users=User.get_users())
    user = User.get_single_user(id)
    all_roles=Role.get_role()
    return render_template("update_user.html", user=user, roles=role_id, all_roles=all_roles)

@user.route("/update_user", methods=['POST'])
@roles_accepted("Admin")
@login_required
def update_user():
    id = request.form.get("id")
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    role_type = request.form.get("role_type")
    role_id = current_user.get_this_user_role().id
    users = User.update_user(id, role_type, username, email, password)
    return render_template("users.html", users=users, roles=role_id)

@user.route("/del_user")
@roles_accepted("Admin")
@login_required
def del_user():
    id = request.args.get("user")
    User.delete_user(id)
    role_id = current_user.get_this_user_role().id
    return render_template("users.html", users=User.get_users(), roles=role_id)

@user.route("/list_users")
@login_required
def list_users():
    role_id = current_user.get_this_user_role().id
    return render_template("users.html", users=User.get_users(),roles=role_id)