# *****************************************************************************
#  Dragomir J. - Test DEVICE.py scripts
# *****************************************************************************
import unittest
import device1, device2

class TestDevice(unittest.TestCase):
    ######################################################################
    #   DEVICE 1
    ######################################################################
    if not device1.DEBUG: # Only test if the debug variable is set to off!
        def test_get_sensor_data_from_device1_mq2_connected(self):
            # Real-world test case where the MQ-2 sensor is connected to Arduino, which is then connected to Raspberry Pi via USB
            self.assertIsNotNone(device1.getSensorData(), "Error with serial read!") # Expecting value that is not None
    else:
        def test_get_sensor_data_from_device1_no_mq2_debug_on(self):
            # Development test case to simulate data reading without Arduino
            device1.DEBUG = True
            self.assertIsNotNone(device1.getSensorData(), "Error with serial read!") # Expecting value that is not None
            
        def test_get_sensor_data_from_device1_no_mq2_debug_off(self):
            # Development test case to simulate data reading without Arduino
            device1.DEBUG = False
            self.assertIsNone(device1.getSensorData(), "Error with serial read!") # Expecting None
    
    ######################################################################
    #   DEVICE 2
    ######################################################################
    if not device2.DEBUG: # Only test if the debug variable is set to off!
        def test_get_sensor_data_from_device2_mq2_connected(self):
            # Real-world test case where the MQ-2 sensor is connected to Arduino, which is then connected to Raspberry Pi via USB
            self.assertIsNotNone(device2.getSensorData(), "Error with serial read!") # Expecting value that is not None
    else:
        def test_get_sensor_data_from_device2_no_mq2_debug_on(self):
            # Development test case to simulate data reading without Arduino
            device2.DEBUG = True
            self.assertIsNotNone(device2.getSensorData(), "Error with serial read!") # Expecting value that is not None
            
        def test_get_sensor_data_from_device2_no_mq2_debug_off(self):
            # Development test case to simulate data reading without Arduino
            device2.DEBUG = False
            self.assertIsNone(device2.getSensorData(), "Error with serial read!") # Expecting None

if __name__ == '__main__':
    unittest.main()