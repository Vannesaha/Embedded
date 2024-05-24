# MQTT handler class to handle the MQTT connection and messages

import paho.mqtt.client as mqtt
import socket
import logging

from src.embedded.blade import EmbeddedDevice
from src.embedded.blade_guard import BladeGuard
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
topics = [
    "home/control/emb/status",
    "home/control/emb/blade",
    "home/control/emb/blade_guard/move",
]


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

        self.embedded = EmbeddedDevice(self)  # Initialize the embedded device
        self.blade_guard = BladeGuard(self)  # Initialize the embedded device

        self.messages = {}  # Initialize the messages dictionary
        self.subscribe(topics)  # Subscribe to the topics

        # keep track of the online status of the device
        self.is_online = False

    def subscribe(self, topics):
        for topic in topics:
            self.client.subscribe(topic)
            logging.info(f"Subscribed to {topic}")

    # function to handle the on_connect event
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected successfully to broker: {BROKER}.")
            # print(f"Connected with result code {rc}")

            self.is_online = True  # set the online status to True

            # Publish an online message when connected
            client.publish("home/status/emb", "online", qos=1, retain=True)
            self.subscribe(topics)  # Subscribe to the topics in the topics list

            # client.subscribe([(DIRECT_TOPIC, 0)])  # Subscribe to the direct topic

            # # example for subscribing to conrol topic for emb status
            # client.subscribe("home/control/emb/status")

            # # example for subscribing to conrol topic for emb blade
            # client.subscribe("home/control/emb/blade")

    # function to handle the on_message event
    def on_message(self, client, userdata, msg):
        # print(f"Received on {msg.topic}: {msg.payload.decode()}")
        payload = msg.payload.decode()  # Decode the message payload
        self.messages[msg.topic] = (
            payload  # Update the messages dictionary with the new message
        )
        # check if the message is a control message for emb status (can be empty message)
        if msg.topic == "home/control/emb/status":
            status_message = "online" if self.is_online else "offline"
            # publish the status message if the device is online
            client.publish("home/status/emb", status_message)
            print(f"Status message published: {status_message}")

        # check if the message is a control message for emb blade
        if msg.topic == "home/control/emb/blade":
            if payload == "ON":
                self.embedded.start_blade()
            elif payload == "OFF":
                self.embedded.stop_blade()
            else:
                print("Invalid command")

        # check if the message is a control message for bleade guard
        if msg.topic == "home/control/emb/blade_guard/move":
            if payload == "ON":
                self.blade_guard.start_blade_guard()
            elif payload == "OFF":
                self.blade_guard.stop_blade_guard()
            else:
                print("Invalid command")

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
