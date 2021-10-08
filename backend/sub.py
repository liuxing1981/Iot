import json
import time

import paho.mqtt.client as mqtt
import taos

mqtt_broken_server = '127.0.0.1'
mqtt_broken_port = 1883
db_server = '127.0.0.1'
topics = ['/0532/01/device01', '/0532/01/device02', '/0532/01/device03']

conn = taos.connect(host=db_server, user='root', password='siemens!123', database='db_0532_01')

def init_db():
    for topic in topics:
        _, area, factory_id, device_id = topic.split('/')
        dbname = 'db_%s_%s'%(area, factory_id)
        conn.execute("create database if not exists %s" % dbname)
        conn.select_db(dbname)
        conn.execute("create table if not exists %s(ts timestamp, speed float, pressure float)"%device_id)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    _, area, factory_id, device_id = msg.topic.split('/')
    payload = str(msg.payload.decode('utf-8')).replace("'", '"')
    payload_json = json.loads(payload)
    conn.execute("insert into %s values(%d,%f,%f)"%(device_id, payload_json['ts'], payload_json['pressure'], payload_json['speed']))
    print(msg.topic)
    print(payload_json)


init_db()
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('luis','siemens')
client.connect('127.0.0.1', 1883, 600)
for topic in topics:
    client.subscribe(topics[0], qos=0)
client.loop_forever()
