import paho.mqtt.client as mqtt

from config.settings import (
    BROKER,  # MQTT broker address
    PORT,  # MQTT broker port
    STATUS_TOPIC,  # MQTT topic for status messages
    DIRECT_TOPIC,  # MQTT topic for direct messages
    LWT_MESSAGE,  # Last Will and Testament message
    OFFLINE_MESSAGE,  # Offline message
    ONLINE_MESSAGE,  # Online message
    DEVICE_ID,  # Unique device identifier
)


class MQTTSubscriber:
    def __init__(self):
        self.client = mqtt.Client(client_id=DEVICE_ID)
        self.client.will_set(STATUS_TOPIC, payload=LWT_MESSAGE, qos=1, retain=True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.messages = {}  # Initialize the messages dictionary

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
            client.publish(STATUS_TOPIC, f"{ONLINE_MESSAGE}", qos=1, retain=True)
            client.subscribe([(DIRECT_TOPIC, 0)])
        else:
            print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received on {msg.topic}: {msg.payload.decode()}")
        payload = msg.payload.decode()
        self.messages[msg.topic] = (
            payload  # Update the messages dictionary with the new message
        )

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    def run(self):
        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()
            input("Press Enter to disconnect...\n")
        finally:
            self.client.publish(STATUS_TOPIC, OFFLINE_MESSAGE, qos=1, retain=True)
            self.client.disconnect()
            self.client.loop_stop()
