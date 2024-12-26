# *****************************************************************************
#  Dragomir J. - MQTT CLIENT W/ KAFKA PRODUCER
# *****************************************************************************
import os
import json
import datetime
import paho.mqtt.client as mqtt
from pykafka import KafkaClient
from dotenv import load_dotenv

# DJ - CONFIG FILE WITH PREDEFINED VARIABLES
load_dotenv() # Load dotenv vars
BROKER      = 'mqtt.eclipseprojects.io'
MQTT_TOPIC  = os.getenv('MQTT_DEVICE_TOPIC')
KAFKA_TOPIC = os.getenv('APACHE_KAFKA_INPUT_TOPIC')

#############################################################################
#   MQTT BROKER - Read data from `mqtt.eclipseprojects.io` BROKER
#############################################################################
mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt.connect(BROKER, 1883, 60)
mqtt.subscribe(f'{MQTT_TOPIC}/#') # Every device sends data to `MQTT_TOPIC/device[N]`


#############################################################################
#   KAFKA PRODUCER - Connecting to KAFKA and preparing PRODUCER 
#############################################################################
kafka = None
try:
    kafka    = KafkaClient(hosts=f'{os.getenv("APACHE_KAFKA_IP_ADDRESS")}:{os.getenv("APACHE_KAFKA_PORT")}', socket_timeout_ms=7000, offsets_channel_socket_timeout_ms=3000)
    topic    = kafka.topics[KAFKA_TOPIC]
    producer = topic.get_sync_producer()
except:
    print('KAFKA CONNECTION ERROR!!!')
    exit(0)

# MQTT FUNCTION THAT GETS DATA AND SENDS IT TO KAFKA
def on_message(client, userdata, msg):
    data = msg.payload.decode('utf-8')
    try:
        timestamp = datetime.datetime.now() # Necessary because of the `window` function in Apache Spark
        kafkaMessage = {
            'timestamp': str(timestamp), 
            'device_name': str(msg.topic[len(MQTT_TOPIC) + 1:]), 
            'data': float(data)
        }
        
        producer.produce(json.dumps(kafkaMessage).encode('utf-8'), 
            partition_key = bytes(msg.topic, 'ascii')
        )

        print(f'{timestamp}\t MQTT MSG: {str(data).rjust(7)} FROM `{msg.topic}`, KAFKA published MQTT MSG to `{KAFKA_TOPIC}`')
    except:
        print('\nCANNOT SEND DATA TO KAFKA!')
        exit(1)

if __name__ == '__main__':
    if kafka is None:
        print('EXITING...')
        exit(2)

    while True:
        mqtt.loop(.753)
        mqtt.on_message = on_message