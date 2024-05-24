# MQTT handler class to handle the MQTT connection and messages

import paho.mqtt.client as mqtt
import socket

# Import embedded device modules
from src.embedded.blade import EmbeddedDevice
from src.embedded.blade_guard import BladeGuard
from src.utils.status import Status

# Import configuration settings
from config.settings import (
    BROKER,  # MQTT broker address
    PORT,  # MQTT broker port
    LWT_MESSAGE,  # Last Will and Testament message
    DEVICE_ID,  # Unique device identifier
)


class MQTTHandler:
    def __init__(self):
        # Initialize MQTT client
        self.client = mqtt.Client(client_id=DEVICE_ID)

        # Initialize embedded device and blade guard handlers
        self.embedded = EmbeddedDevice(self)
        self.blade_guard = BladeGuard(self)
        self.status = Status(self, BROKER)

        # Set the last will and testament message
        self.client.will_set("home/status/emb", payload=LWT_MESSAGE, qos=1, retain=True)

        # Set callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.status.on_disconnect

        # Initialize messages dictionary
        self.messages = {}

        # Define topic handlers and their corresponding functions
        self.topic_handlers = {
            "home/control/emb/status": self.status.handle_mqtt_message,
            "home/control/emb/blade": self.embedded.handle_mqtt_message,
            "home/control/emb/blade_guard/move": self.blade_guard.handle_mqtt_message,
        }

    def subscribe(self, topics):
        # Subscribe to given topics
        for topic in topics:
            self.client.subscribe(topic)
            print(f"Subscribed to {topic}")

    def on_connect(self, client, userdata, flags, rc):
        # Handle connection event
        self.status.on_connect(client, userdata, flags, rc)
        if rc == 0:
            # Subscribe to the topics in the topic_handlers list
            for topic in self.topic_handlers.keys():
                client.subscribe(topic)
                print(f"Subscribed to {topic} after connecting")

    def on_message(self, client, userdata, msg):
        # Handle received message
        payload = msg.payload.decode()  # Decode the message payload
        self.messages[msg.topic] = (
            payload  # Update the messages dictionary with the new message
        )

        # Handler for the received message topic for easier message handling
        handler = self.topic_handlers.get(msg.topic)
        if handler:
            handler(client, payload)
            print(f"Handled message on {msg.topic}: {payload}")
        else:
            print(f"No handler for topic {msg.topic}")

    def run(self):
        # Set a timeout for all socket connections
        socket.setdefaulttimeout(10)
        try:
            # Connect to the broker
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()  # Start the loop
            print(f"Connecting to broker at {BROKER}:{PORT}")
            input("Press Enter to disconnect...\n")
        except socket.timeout:
            # Handle the timeout exception after 60 seconds
            print("Connection attempt timed out.")
        finally:
            # Publish an offline message
            self.client.publish("home/status/emb", "offline", qos=1, retain=True)
            self.client.disconnect()  # Disconnect from the broker
            self.client.loop_stop()  # Stop the loop
            print("Disconnected from broker and stopped loop")
