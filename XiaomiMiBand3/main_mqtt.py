import sys
from auth import MiBand3
from cursesmenu import *
from cursesmenu.items import *
from constants import ALERT_TYPES
import time
import paho.mqtt.client as mqtt
from bluepy.btle import Peripheral, DefaultDelegate, ADDR_TYPE_RANDOM, BTLEException, BTLEDisconnectError
import 

###############################################
# Aurora Polo Rodríguez & Javier Medina Quero #
###############################################

def call_immediate():
    print 'Sending Call Alert'
    time.sleep(1)
    band.send_alert(ALERT_TYPES.PHONE)
def msg_immediate():
    print 'Sending Message Alert'
    time.sleep(1)
    band.send_alert(ALERT_TYPES.MESSAGE)
def detail_info():
    print 'MiBand'
    print 'Soft revision:',band.get_revision()
    print 'Hardware revision:',band.get_hrdw_revision()
    print 'Steps:', band.get_steps()
    print 'Battery:', band.get_battery_info()
    raw_input('Press Enter to continue')
def custom_message():
    band.send_custom_alert(5)
def custom_call():
    band.send_custom_alert(3)
def custom_missed_call():
    band.send_custom_alert(4)
def l(x):
    print 'Realtime heart BPM:', x
def heart_beat():
    band.start_raw_data_realtime(heart_measure_callback=l)
    raw_input('Press Enter to continue')
def sensor():
    band.start_raw_data_realtime(accel_raw_callback=l)
    raw_input('Press Enter to continue')
def change_date():
    band.change_date()

connected = False
MAC_ADDR = "E6:FD:82:DB:AC:EB"
atHome = 0
client = mqtt.Client()
client.connect("192.168.1.2",1883)
    
while connected == False:
    try:
        print ('Attempting to connect to ', MAC_ADDR)
        band = MiBand3(MAC_ADDR, debug=True)
        band.setSecurityLevel(level = "medium")
        band.authenticate()
        connected = True
    except (IOError,BTLEException) as e:
        print ('Impossible to connect')
        
    time.sleep(5)
        
client.publish("sensor_data/atHome", str("{'atHome': 1}"))
                
while True:
    if connected == True:
        try:
            print band.get_steps()
            client.publish("sensor_data/steps", str(band.get_steps()))
            print band.get_heart_rate()
            client.connect("192.168.1.2",1883)
            client.publish("sensor_data/hr", str(band.get_heart_rate()))
            time.sleep(5)
        except (IOError,BTLEException) as e:
            connected = False
            client.connect("192.168.1.2",1883)
    if connected == False:
        time.sleep(5)
        print 'Not at home'
        client.publish("sensor_data/atHome", str("{'atHome': 0}"))
        
        try:
            band = MiBand3(MAC_ADDR, debug=True)
            band.setSecurityLevel(level = "medium")
            band.authenticate()
            connected = True
            atHome = 1
            client.connect("192.168.1.2",1883,5)
            client.publish("sensor_data/atHome", str("{'atHome': 1}"))
        except (IOError,BTLEException) as e:
            print 'Not home yet'
       