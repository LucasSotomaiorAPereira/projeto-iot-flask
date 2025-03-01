import network
import time

import ujson
import _thread
from machine import Pin, ADC, PWM
from umqtt.simple import MQTTClient
from servo import Servo

MQTT_CLIENT_ID = "sensores"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND_GAS = "purificador/sensors/gas"
MQTT_TOPIC_SEND_PARTICLES = "purificador/sensors/particles"
MQTT_TOPIC_SEND = "purificador/sensors"
MQTT_TOPIC_RELE = "purificador/rele"
MQTT_TOPIC_SERVO = "purificador/servo"
MQTT_TOPIC_ATUADORES = "purificador/atuadores"
MQTT_TOPIC_VALUES = "purificador/values"

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

gas = ADC(Pin(34, Pin.IN))
gas.atten(ADC.ATTN_11DB)

particula = ADC(Pin(35, Pin.IN))
particula.atten(ADC.ATTN_11DB)

rele = Pin(12, Pin.OUT)
servo = Servo(pin=13)

print("Connecting to WiFi", end="")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while not wifi.isconnected():
  pass

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)

publish_value_rele = 0
publish_value_servo = 0

def callback(topic, msg):
  msg = ujson.loads(msg.decode())
  if topic.decode() == MQTT_TOPIC_RELE:
    global publish_value_rele
    publish_value_rele = int(msg["valor"])
  elif topic.decode() == MQTT_TOPIC_SERVO:
    global publish_value_servo
    publish_value_servo = int(msg["valor"])
  else:
    global gas_value, particula_value
    gas_value = int(msg["gas"])
    particula_value = int(msg["particula"])

client.set_callback(callback)
client.connect()

print("\nConnected!")

client.subscribe(MQTT_TOPIC_RELE)
client.subscribe(MQTT_TOPIC_SERVO)
client.subscribe(MQTT_TOPIC_VALUES)

def check_msg():
  while True:
    time.sleep(1)
    client.check_msg()

def verify_values():
  global gas_value, particula_value
  if (gas_value > 30000 or particula_value > 30000): return True
  else: return False

verification_antes = False
verification = False

def change_rele():
  global verification_antes
  global verification
  global publish_value_rele
  global publish_value_servo

  while True:
    if publish_value_rele == 1 or publish_value_servo == 1: 
        if publish_value_rele == 1: rele.on()
        else: rele.off()
        if publish_value_servo == 1: servo.move(180)
        else: servo.move(0)
    else:
        verification = verify_values()
        if verification != verification_antes:
            verification_antes = verification
            if (verification):
                servo.move(180)
                rele.on()
                message_atuadores = ujson.dumps({
                    "rele": "1",
                    "servo": "1"
                })
                client.publish(MQTT_TOPIC_ATUADORES, message_atuadores)
            else: 
                servo.move(0)
                rele.off()
                message_atuadores = ujson.dumps({
                    "rele": "0",
                    "servo": "0"
                })
                client.publish(MQTT_TOPIC_ATUADORES, message_atuadores)

        elif not verification :
            servo.move(0)
            rele.off()
    time.sleep(1)

_thread.start_new_thread(check_msg, ())
_thread.start_new_thread(change_rele, ())

print("Medindo...")
while True:
  gas_value = gas.read_u16()
  particula_value = particula.read_u16()
  message = ujson.dumps({
    "gas": gas_value,
    "particula": particula_value
  })
  message_gas = ujson.dumps({
    "gas": gas_value
  })
  message_particle = ujson.dumps({
    "particula": particula_value
  })
  client.publish(MQTT_TOPIC_SEND, message)
  client.publish(MQTT_TOPIC_SEND_GAS, message_gas)
  client.publish(MQTT_TOPIC_SEND_PARTICLES, message_particle)
  time.sleep(1)
