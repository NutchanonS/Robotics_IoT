from mqtt import MQTTClient
# from paho.mqtt import client as MQTTClient
import halo, time, event
import json

MQTTHOST = "43.255.104.62"
MQTTPORT = 1883

# Fill in as you like
client_id = ""

# Example Path
TopicSub = "scamper3/command"
TopicPub = "scamper3/signalfromrobot"
TopicPub2 = "scamper3/action"
userName = 'root'#'superAIEngineer2'
passWord = 'Tunder@99'#'superAIEngineer2'
command = 'gyro'
action = 'blue'
show = ''
my_id = '4'
level = '1'
status = '1'

# Connect to the MQTT server
def on_mqtt_connect():
   mqttClient.connect(clean_session = True)
   time.sleep(3)

# publish a message
def on_publish(topic, payload, retain=False, qos = 1):
   mqttClient.publish(topic, payload, retain, qos)

# message processing function
def on_message_come(topic, msg):
   print(topic + " " + ":" + str(msg))
   global command,action,id_
   print(str(topic))
   if ( str(topic).find(TopicSub) > 0 ):
      id_ = str(msg)[2:-1].split("/")[0]
      if id_ == my_id :
         command = str(msg)[2:-1].split("/")[1]
         action = str(msg)[2:-1].split("/")[2]
         #on_publish(TopicPub2, id_  + str(msg)[2:-1] , retain = False, qos = 1)
         print('Received',id_ )

# subscribe message
def on_subscribe():
   mqttClient.set_callback(on_message_come)
   mqttClient.subscribe(TopicSub, qos = 1)

# Order
def order(command,action):
   global status,level,my_id   
   # if command.find('gyro') > 0  :
   if command == 'gyro' :
      status = '1'
      print("Gyro Action")
      gyro(action)

   if command == 'led' :
      status ='1'
      led()

   if command == 'off' :
      status ='1'
      halo.led.off_all()
   
   if command == 'treat' and status == '1' :
      for i in range(int(level)) :
         halo.led.show_animation('meteor_green')
         time.sleep(1)
      halo.led.off_all()
      on_publish(TopicPub2, my_id + ' treatment completed', retain = False, qos = 1)
      status = '0'
        
# led 
def led() :
   halo.led.show_ring(action)

# Gyro 
def gyro(action):
   global level
   if halo.motion_sensor.get_pitch() < 10:
      level = '3'
      x = action+' '+action+' '+action+' '+action+' '+action+' '+action+' '+action+' '+action+' '+action+' '+action+' '+action+' '+action
      halo.led.show_ring(x)

   if halo.motion_sensor.get_pitch()  > 10  and halo.motion_sensor.get_pitch() < 30:
      level = '2'
      x = action+' '+action+' '+action+' '+action+' '+action+' '+action+' '+action+' '+action+' black'+' black'+' black'+' black'+' black'
      halo.led.show_ring(x)

   if halo.motion_sensor.get_pitch() > 20 and halo.motion_sensor.get_pitch() < 90:
      level = '1'
      x = action+' '+action+' '+action+' '+action+' black'+' black'+' black'+' black'+' black'+' black'+' black'+' black'
      halo.led.show_ring(x)

mqttClient = MQTTClient(client_id, MQTTHOST, port=MQTTPORT, user=userName, password=passWord, keepalive=500, ssl=False)

@event.start
def on_start():
   global command,status
   count = 0
   isConnectedMQTT = 0
   while True:
         if halo.wifi.is_connected():
            
            if ( isConnectedMQTT == 0 ):
                on_mqtt_connect()
                isConnectedMQTT = 1
                on_subscribe()
                halo.led.show_all(0, 20, 0)
                time.sleep(1)
                on_publish(TopicPub,"WIFI AND MQTT IS CONNECTED", retain = False, qos = 1) 
            else:
               count = count + 1
               on_publish(TopicPub, 'count ' + str(count), retain = False, qos = 1)
               time.sleep(1)
 
         else:
           halo.led.show_all(20, 0, 0)
           halo.wifi.start(ssid = 'SuperAI', password = 'Thailand', mode = halo.wifi.WLAN_MODE_STA)

           time.sleep(2)
         order(command,action)
         print("my command :", command, status)