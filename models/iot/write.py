from models.db import db
from models.iot.actuators import Actuator
from models.iot.devices import Device
from datetime import datetime

class Write(db.Model):
    __tablename__ = "write"
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    write_datetime = db.Column(db.DateTime(), nullable=False)
    actuators_id = db.Column(db.Integer, db.ForeignKey(Actuator.id), nullable=False)
    value = db.Column(db.Float, nullable=True)

    def save_write(topic, value):
        actuator = Actuator.query.filter(Actuator.topic == topic).first()
        device = Device.query.filter(Device.id == actuator.devices_id).first()
        if (Actuator is not None) and (device.is_active == True):
            write = Write(write_datetime=datetime.now(), actuators_id=actuator.id, value=float(value))
            db.session.add(write)
            db.session.commit()

    def get_write(actuator_id, start, end):
        actuator_id = Actuator.get_actuator_id(actuator_id)
        write = Write.query.filter(Write.actuators_id == actuator_id, Write.write_datetime > start,
                            Write.write_datetime < end).all()
        return write