import datetime

from flask_user import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from models.db import db
from models.user.roles import Role
from models.user.user_roles import UserRoles


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(256), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    def save_user(username, email, password, role):
        user = User(
            username=username, 
            email=email,
            email_confirmed_at=datetime.datetime.now(),
            password=generate_password_hash(password)
            )
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()

    def get_users():
        users = User.query.all()
        return users

    def get_single_user(id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            return user

    def update_user(id, role_type, username, email, password):
        user = User.query.filter(User.id == id).first()
        role = Role.get_single_role(role_type)
        user.roles.remove(user.get_this_user_role())
        user.roles.append(role)
        user.username = username
        user.email = email
        user.password = generate_password_hash(password)
        db.session.commit()
        return User.get_users()

    def delete_user(id):
        user = User.query.filter(User.id == id).first()
        if user.get_this_user_role().name != "Admin":
            db.session.delete(user)
            db.session.commit()
        return User.get_users()

    def get_user_id(user_id):
        id = User.query.filter_by(id=user_id).first()
        if id is not None:
            return id

    def validate_user(email, password):
        user = User.query.filter(User.email == email).first()
        if (user == None or not check_password_hash(user.password, password)):
            return None
        else:
            return user
        
    def get_this_user_role(self):
        role_id = UserRoles.query.filter(UserRoles.user_id == self.id).first().role_id
        role = Role.query.filter(Role.id == role_id).first()
        
        return role


    def get_user_role(user):
        user = User.query.filter(User.email == user.email).first()
        role = UserRoles.query.filter(UserRoles.user_id==user.id).first()
        return role
