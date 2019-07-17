import paho.mqtt.client as mqtt
from config import configuration as config
from config import azureconfiguration as iothub
import ssl

class MqttClient(mqtt.Client):
    """
    Extends the normal mqttClient class to implement some connection parameters
    that should be generic to all the components in the system
    """

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    # The callback for disconnection, which stops the loop()
    def on_disconnect(self, client, userdata, rc=0):
        print("Disconnected result code "+str(rc))
        self.loop_stop()

    # Sets up the connection with the broker on the server specified in mqttconfig.py
    def setup_client(self):
        self.username_pw_set(config.mqttUser, password=config.mqttPasswd)
        self.connect(config.mqttBroker, config.mqttPort, 60)
        self.loop_start()
    
    def setup_client_azure(self):
        self.username_pw_set(username=iothub.iot_hub_name+".azure-devices.net/" + iothub.device_id + "/?api-version=2018-06-30", password=iothub.sas_token)
        self.tls_set(ca_certs=iothub.path_to_root_cert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
        self.tls_insecure_set(False)
        self.connect(iothub.iot_hub_name+".azure-devices.net", port=8883)
        self.loop_start()