# *****************************************************************************
#  Dragomir J. - IoT DEVICE_2 W/ MQTT! (DEVICE:2)
# *****************************************************************************
import os
import time
import serial
import paho.mqtt.publish as mqtt
from random import uniform
from dotenv import load_dotenv

# DJ - CONFIG FILE WITH PREDEFINED VARIABLES
load_dotenv() # Load dotenv vars
BROKER = 'mqtt.eclipseprojects.io' # MQTT Broker on the internet for easier demonstration
TOPIC  = f'{os.getenv("MQTT_DEVICE_TOPIC")}/{os.path.basename(__file__).split(".")[0]}' # Add the name of the file to TOPIC because of Spark grouping
DEBUG  = True

#############################################################################
#   getSerialInput - Get serial input from Arduino connected via USB
#############################################################################
def getSerialInput():
    input = None
    if not DEBUG:
        try:
            input = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # Check if the port is correct!
            input.reset_input_buffer()
        except:
            input = None
    return input


#############################################################################
#   getSensorData - Get data from the MQ-2 sensor
#############################################################################
def getSensorData(input):
    """ (RASPBERRY PI) Get the CO value from the MQ-2 sensor """
    if not DEBUG and input is not None:
        if input.in_waiting > 0:
            return float(input.readline().decode('utf-8').rstrip())
    elif DEBUG:
        return round(uniform(0, 999), 2) # Simulate read
    return None

# Execution is possible only from the terminal!!!
if __name__ == '__main__':
    if DEBUG:
        print('DEBUG MODE IS ON!!!\n')

    # CHECK IF .ENV FILE EXISTS AND IF THE TOPIC IS NOT EMPTY
    if TOPIC.split('/')[0] == 'None' or len(TOPIC.split('/')[0]) == 0:
        print('NO .ENV FILE OR TOPIC IS EMPTY!!!')
        exit(0)
        
    # Get Serial input (ONLY ONCE!)
    input = getSerialInput() 

    # INFINITE LOOP
    while True:
        try:
            data = f'{getSensorData(input):.3f}'
            mqtt.single(TOPIC, data, hostname = BROKER)
            print(f'MQTT: {str(data).rjust(7)} to topic {TOPIC}')
            if DEBUG: 
                time.sleep(0.33) # SECONDS!
        except:
            print('ERROR WHILE TRYING TO GET SENSOR DATA!')
            exit(1)