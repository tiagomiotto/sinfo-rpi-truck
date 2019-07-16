from mqttClient import MqttClient
from abc import ABCMeta, abstractmethod
import transformations
import time
import json


class Component:

    __metaclass__ = ABCMeta

    def __init__(self, publishTopic):
        self.mqttHandler = MqttClient()
        self.mqttHandler.setup_client()

        # Rate in which data is send to the cloud in ms
        self.samplingRate = 1

        # Rate in which you acquire data from the sensor in ms
        self.pollingRate = 1

        # Number of samples to be transformed before being sent to the cloud
        self.numberOfSamples = 1

        # Mqtt topic for the component to publish
        self.pubTopic = publishTopic

        # Mqtt topic to recieve commands, such as changing the sampling rate
        # and selecting the transformation
        self.subTopic = self.pubTopic + "/commands"

        # Transformation to be done on the samples acquired
        self.transformation = getattr(transformations, 'default')


    # Used to change the number of samples during runtime
    def change_sample_size(self, newSampRate):
        self.samplingRate = newSampRate
        self.numberOfSamples = int(self.samplingRate / self.pollingRate)
        print("Number of samples", self.numberOfSamples )
        

    # Set the transformation for the collected samples
    # from the ones available in the transformations class
    def set_transformation(self, transform):
        self.transformation = getattr(transformations, transform)


    # Component specific run code
    # It should contain all the extra actions aside from
    # setup and data acquisition to be perfomed once per cycle
    # Refrain from including heavy operations, otherwise it can
    # mess with the sampling rate
    def run(self):
        pass

    # Main loop for all the components
    # It will be called run by main.py
    # Be concious about its structure when writing your
    # setup and data acquisition methods
    def loop(self):
        loopcount = 0
        self.setup()
        samples = []
        while True:
            begin = time.time()
            # Acquire and store the sample if it is not None
            acquired = self.acquireData()
            # if acquired is None:
            #     continue
            samples.append(acquired)

            # Run the extra actions
            self.run()

            # Increment the sample counter
            loopcount += 1

            # When the required samples have been acquired transform and send
            if loopcount == self.numberOfSamples:
                dataToSend = self.transformation(samples)
                self.mqttHandler.publish(
                    self.pubTopic, json.dumps(self.gen_payload_message(dataToSend)))
                loopcount = 0
                samples = [] # clear the samples

            end = time.time()
            # Sleep the polling rate - elapsed time on calculations
            if (end-begin)<self.pollingRate:
                time.sleep(self.pollingRate-(end-begin))

    # Component specific setup
    # Is run before the loop starts
    @abstractmethod
    def setup(self):
        pass

    # Component specific data handling and MQTT publishing
    # Should return the sample acquired from the component
    # In the form of a dictionary with the field as the key
    # and the data as the values.
    @abstractmethod
    def acquireData(self):
        pass

    # Generate the payload message specific for that device
    # In JSON
    @abstractmethod
    def gen_payload_message(self, data):
        pass