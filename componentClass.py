from mqttClient import MqttClient
from abc import ABCMeta, abstractmethod
import sys,signal


class Component:

    __metaclass__ = ABCMeta

    def __init__(self):
        self.mqttHandler = MqttClient()
        self.mqttHandler.setup_client()

        self.pollingRate = 1
        self.loopCycles = 1
        
    # Component specific setup 
    # Needs to contain all the code to be executed once 
    # before the loop starts
    # Needs to be implemented in order for the main to run correctly
    @abstractmethod
    def setup(self):
        pass

    # Component specific data handling and MQTT publishing 
    # It should receive the main timestamp to stamp the package
    # in order to ensure coherence between components.
    #
    # Needs to be implemented in order for the main to run correctly
    @abstractmethod
    def handleData(self,timestamp):
        pass
    
    # Component specific setup JSON payload generation
    # (Good practice to implement it, so it's well organized)
    def gen_payload_message(self, data,timestamp):
        pass

    # Calculate the number of loop cycles before sampling the 
    # sensor based on the rate the loop is run
    def calculate_loop_cycles(self,loop_rate):
        self.loopCycles = int(self.pollingRate / loopRate)