# MQTT handler class to handle the MQTT connection and messages

import paho.mqtt.client as mqtt
import socket
import logging

from src.embedded.blade import EmbeddedDevice
from src.embedded.blade_guard import BladeGuard
from src.utils.status import Status

from config.settings import (
    BROKER,  # MQTT broker address
    PORT,  # MQTT broker port
    # STATUS_TOPIC,  # MQTT topic for status messages
    # DIRECT_TOPIC,  # MQTT topic for direct messages
    LWT_MESSAGE,  # Last Will and Testament message
    # OFFLINE_MESSAGE,  # Offline message
    # ONLINE_MESSAGE,  # Online message
    DEVICE_ID,  # Unique device identifier
)

# List of topics to subscribe to
# topics = [
#     "home/control/emb/status",
#     "home/control/emb/blade",
#     "home/control/emb/blade_guard/move",
# ]


class MQTTHandler:
    def __init__(self):
        self.client = mqtt.Client(client_id=DEVICE_ID)

        self.client.will_set(
            "home/status/emb", payload=LWT_MESSAGE, qos=1, retain=True
        )  # Set the last will and testament message
        self.client.on_connect = self.on_connect  # Set the on_connect callback function
        self.client.on_message = self.on_message  # Set the on_message callback function
        self.client.on_disconnect = (
            self.on_disconnect
        )  # Set the on_disconnect callback function

        # keep track of the online status of the device
        self.is_online = "offline"

        self.embedded = EmbeddedDevice(self)  # Initialize the embedded device
        self.blade_guard = BladeGuard(self)  # Initialize the embedded device
        self.status = Status(self)  # Initialize the status

        self.messages = {}  # Initialize the messages dictionary
        # self.subscribe(topics)  # Subscribe to the topics

        self.topic_handlers = {
            "home/control/emb/status": self.status.handle_mqtt_message,
            "home/control/emb/blade": self.embedded.handle_mqtt_message,
            "home/control/emb/blade_guard/move": self.blade_guard.handle_mqtt_message,
            # Add more topics here...
        }

    def subscribe(self, topics):
        for topic in topics:
            self.client.subscribe(topic)
            logging.info(f"Subscribed to {topic}")

    # function to handle the on_connect event
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected successfully to broker: {BROKER}.")
            # print(f"Connected with result code {rc}")

            self.is_online = "online"  # set the online status to True

            # Publish an online message when connected
            client.publish("home/status/emb", "online", qos=1, retain=True)
            self.subscribe(
                self.topic_handlers.keys()
            )  # Subscribe to the topics in the topic_handlers list

    # function to handle the on_message event
    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()  # Decode the message payload
        self.messages[msg.topic] = (
            payload  # Update the messages dictionary with the new message
        )

        handler = self.topic_handlers.get(msg.topic)
        if handler:
            handler(client, payload)
        else:
            print(f"No handler for topic {msg.topic}")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.is_online = False
            print("Unexpected disconnection.")

    def run(self):
        socket.setdefaulttimeout(10)  # Set a timeout for all socket connections
        try:
            self.client.connect(BROKER, PORT, 60)  # Connect to the broker
            self.client.loop_start()  # Start the loop
            input("Press Enter to disconnect...\n")
        except socket.timeout:  # Handle the timeout exception after 60s
            print("Connection attempt timed out.")
        finally:
            # Publish an offline message
            self.client.publish(
                "home/status/emb", "offline", qos=1, retain=True
            )  # Publish an offline message
            self.client.disconnect()  # Disconnect from the broker
            self.client.loop_stop()  # Stop the loop
