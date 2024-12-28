# *****************************************************************************
#  Dragomir J. - Test EMITTER.py script
# *****************************************************************************
import unittest
import emitter

class TestEmitter(unittest.TestCase):
    def test_get_kafka_consumer(self):
        self.assertIsNotNone(emitter.getKafkaConsumer(), "Error with Kafka consumer!")

    def test_get_socketio_client(self):
        sio = emitter.getSocketioClient(False)
        self.assertIsNotNone(sio, "Error with SocketIO client!")
        if sio is not None:
            sio.disconnect()

if __name__ == '__main__':
    unittest.main()