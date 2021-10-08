import random
import time
from pyngrok import ngrok
import paho.mqtt.client as mqtt

client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
client = mqtt.Client(client_id)
client.username_pw_set('luis', password='siemens')
client.connect('2.tcp.ngrok.io:16967', 1883, 60)
# ngrok.set_auth_token("1maRk4vOQk2K5rgbOjxgV7wMSsi_6H7x5h9fdKWWm6MFLnvft")
# public_url = ngrok.connect("http://127.0.0.1:5001")                       # tunnel to host:port instead of localhost
#
# print(public_url)



while True:
    speed = random.randint(1, 100)
    pressure = random.randint(1, 1000)
    ts = time.time() * 1000
    print("push")
    client.publish('/0532/01/device01',payload='{"ts": %d, "pressure": %f, "speed": %f}'%(ts, pressure, speed),qos=0)
    time.sleep(2)