from models.db import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column("id", db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(512))

    def save_role(name, description):
        role = Role(name=name, description=description)
        db.session.add(role)
        db.session.commit()
        return role

    def get_single_role(name):
        role = Role.query.filter(Role.name == name).first()
        return role

    def get_role():
        role = Role.query.all()
        return role
