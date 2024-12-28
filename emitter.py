# *****************************************************************************
#  Dragomir J. - SOCKETIO EMITTER W/ KAFKA CONSUMER
# *****************************************************************************
import os
import json
import socketio
from pykafka import KafkaClient
from pykafka.common import OffsetType
from dotenv import load_dotenv
from datetime import datetime

# DJ - CONFIG FILE WITH CONST VARIABLES
load_dotenv() # Load dotenv vars

#############################################################################
#   KAFKA CONSUMER - Connects to KAFKA and prepares CONSUMER for reading
#############################################################################
def getKafkaConsumer():
    try:
        kafka    = KafkaClient(hosts=f'{os.getenv("APACHE_KAFKA_IP_ADDRESS")}:{os.getenv("APACHE_KAFKA_PORT")}', socket_timeout_ms=7000, offsets_channel_socket_timeout_ms=3000)
        topic    = kafka.topics[os.getenv('APACHE_KAFKA_OUTPUT_TOPIC')]
        consumer = topic.get_simple_consumer(
            auto_offset_reset     = OffsetType.LATEST, # Get only the latest data from the topic
            reset_offset_on_start = True
        )

        return consumer
    except:
        return None

#############################################################################
#   SOCKETIO - Enables live updates without the need for page refresh
#############################################################################
def getSocketioClient(retry = True):
    try:
        sio = socketio.Client()
        sio.reconnection_attempts = 1 # Because of this the script will exit if limit is exceeded
        print(f'http://{os.getenv("FLASK_IP_ADDRESS")}:{os.getenv("FLASK_PORT")}')
        sio.connect(f'http://{os.getenv("FLASK_IP_ADDRESS")}:{os.getenv("FLASK_PORT")}', retry=retry)
        
        return sio
    except:
        return None
    
# Extract the time value from the date string
def getTime(date_string):
    return str(datetime.fromisoformat(date_string).time())

if __name__ == '__main__':
    kafka = getKafkaConsumer()
    if kafka is None:
        print('KAFKA CONNECTION ERROR!!!\nEXITING...')
        exit(0)

    sio = getSocketioClient()
    if sio is None:
        print('SOCKETIO CONNECTION ERROR!!!\nEXITING...')
        exit(1)

    print(f'CONNECTION BETWEEN THE SOCKETIO AND FLASK SERVER HAS BEEN ESTABLISHED! (SID = {sio.sid})')
    try:
        for msg in kafka:
            if msg is not None and sio is not None:
                message = json.loads(msg.value.decode('utf-8'))
                
                # Refactor the message before sending it to clients
                message['window_start'] = getTime(message['window']['start'])
                message['window_end']   = getTime(message['window']['end'])
                message['data'] = message.pop('average') # Rename the "average" key to "data"
                del message['window'] # Remove the "window" key from the message

                try:
                    print(json.dumps(message))
                    sio.emit('broadcast_event', message)
                except:
                    print('SIO EMIT ERROR WITH THE MESSAGE ABOVE!\n')
    except:
        sio.disconnect()
        print('KAFKA ERROR WHILE READING MESSAGES!\nEXITING...')
        exit(2)