#!/usr/bin/env python

# Root topic
rootTopic = "truck1"

# Broker configuration
mqttBroker = "192.168.1.126"
mqttPort = "1883"

mqttUser = " "
mqttPasswd = " "

# Components configuration
componentDic = {
    "imuClass": "Imu",
    "proximityClass": "ProximitySensor",
    "motorClass": "Motor",
    "cameraClass": "Camera"}

componentsSamplingIntevalInSeconds = {
    "imuClass": 0.1,
    "proximityClass": 0.4,
    "motorClass": 10.0,
    "cameraClass": 100.0}
