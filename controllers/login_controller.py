from flask import Blueprint, flash, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask_user import roles_accepted, login_required
from models.user.users import User

login = Blueprint("login", __name__, template_folder="templates")


@login.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.validate_user(email, password)
        if (user == None):
            flash('Usuário e/ou senha incorreta!')
            return render_template('login.html')
        else:
            login_user(user)
            return redirect(url_for('home'))
    else:
        return render_template('login.html')

@login.route("/login")
def index():
    return render_template("login.html")

@login.route('/logout')
@roles_accepted("Admin", "Estatistico", "Operador")
@login_required
def logout():
    logout_user()
    return render_template("login.html")
