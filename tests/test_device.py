# *****************************************************************************
#       Copyright (C) 2024 - Dragomir J. - Test all DEVICE.py scripts
# *****************************************************************************
import unittest
import device1, device2

class TestDevice(unittest.TestCase):
    ######################################################################
    #   DEVICE 1
    ######################################################################
    def test_get_sensor_data_from_device1_mq2_connected(self):
        # Real-world test case where the MQ-2 sensor is connected to Arduino, which is then connected to Raspberry Pi via USB
        device1.DEBUG = False
        self.assertIsNotNone(device1.getSensorData(), "Error with serial read!") # Expecting value that is not None
        
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
    def test_get_sensor_data_from_device2_mq2_connected(self):
        # Real-world test case where the MQ-2 sensor is connected to Arduino, which is then connected to Raspberry Pi via USB
        device2.DEBUG = False
        self.assertIsNotNone(device2.getSensorData(), "Error with serial read!") # Expecting value that is not None
        
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