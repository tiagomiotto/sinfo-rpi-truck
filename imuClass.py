from componentClass import Component
import time
import os.path
import operator
import RTIMU
import os
import sys
import getopt
import json
sys.path.append('.')


class Imu(Component):
    """
    An implementation of the component class to acquire and publish the 
    data from the Inertial Measurement unit, namely the data from the
    accelerometer and the gyroscope.
    """

    # Setup method for this specific device
    def setup(self):
        # This is mostly the legacy code used in the SINFO Workshop
        # Load configuration file: sensor settigs + calibration
        SETTINGS_FILE = "RTIMULib"
        self.s = RTIMU.Settings(SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(self.s)

        print("IMU Name: " + self.imu.IMUName())

        t_shutdown = 0
        if (not self.imu.IMUInit()):
            print ("IMU Init Failed, try #: ".format(str(t_shutdown)))
            t_shutdown += 1
            if t_shutdown > 9:
                sys.exit(1)

        else:
            print "IMU Init Succeeded"

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)
        self.imu.setSampleRate(400)

        # Used to set up the polling interval of the sensor
        # Converted from mS to seconds
        self.pollingRate = 1.0/(400/self.imu.IMUGetPollInterval())

        self.change_sample_size(1)
        

    # Data Handling for this specific device, from collection to publishing to the correct MQTT Topics.
    def acquireData(self):
        if self.imu.IMURead():
            data = self.imu.getIMUData()
            return data
        # Else return None
        return None

    def gen_payload_message(self, data):
        try:
            payload = {
                'accel': {
                    'x': data.get('accel')[0],
                    'y': data.get('accel')[1],
                    'z': data.get('accel')[2]
                },
                'gyro': {
                    'x': data.get('gyro')[0],
                    'y': data.get('gyro')[1],
                    'z': data.get('gyro')[2]
                },
                # Note: This is a UNIX timestamp in microseconds
                'timestamp': data.get('timestamp')
            }
        except: 
            print("Received wrong data structure")
        return payload

