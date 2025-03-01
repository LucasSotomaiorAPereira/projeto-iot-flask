from models.db import db
from models.iot.devices import Device

class Actuator(db.Model):
    __tablename__ = "actuators"
    id = db.Column('id', db.Integer, primary_key=True)
    devices_id = db.Column(db.Integer, db.ForeignKey(Device.id))
    topic = db.Column(db.String(50))

    def save_actuator(name, topic, is_active):
        device = Device(name=name, is_active=is_active)
        actuator = Actuator(devices_id=device.id, topic=topic)

        device.actuators.append(actuator)
        db.session.add(device)
        db.session.commit()

    def get_actuators():
        actuators = Actuator.query.join(Device, Device.id == Actuator.devices_id)\
            .add_columns(Device.id, Device.name,
                        Device.is_active, Actuator.topic).all()
        return actuators
    
    def get_single_actuator(id):
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        if actuator is not None:
            actuator = Actuator.query.filter(Actuator.devices_id == id)\
                            .join(Device).add_columns(Device.id, Device.name, 
                                    Device.is_active, Actuator.topic).first()
            return actuator
        
    def update_actuator(id, name, topic, is_active):
        device = Device.query.filter(Device.id == id).first()
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        if device is not None:
            device.name = name
            actuator.topic = topic
            device.is_active = is_active
            db.session.commit()
            return Actuator.get_actuators()
        
    def delete_actuator(id):
        device = Device.query.filter(Device.id == id).first()
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()

        db.session.delete(actuator)
        db.session.delete(device)
        db.session.commit()

        return Actuator.get_actuators()
    
    def get_actuator_id(device_id):
        actuator = Actuator.query.filter(Actuator.devices_id == device_id).first()
        if actuator is not None:
            return actuator.id