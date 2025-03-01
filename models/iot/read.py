from models.db import db
from models.iot.sensors import Sensor
from models.iot.devices import Device
from datetime import datetime

class Read(db.Model):
    __tablename__ = "read"
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable=False)
    sensors_id = db.Column(db.Integer, db.ForeignKey(Sensor.id), nullable=False)
    value = db.Column(db.Float, nullable=True)

    def save_read(topic, value):
        sensor = Sensor.query.filter(Sensor.topic == topic).first()
        device = Device.query.filter(Device.id == sensor.devices_id).first()
        if (Sensor is not None) and (device.is_active == True):
            read = Read(read_datetime=datetime.now(), sensors_id=sensor.id, value=float(value))
            db.session.add(read)
            db.session.commit()

    def get_read(sensor_id, start, end):
        sensor_id = Sensor.get_sensor_id(sensor_id)
        read = Read.query.filter(Read.sensors_id == sensor_id, Read.read_datetime > start,
                            Read.read_datetime < end).all()
        return read
