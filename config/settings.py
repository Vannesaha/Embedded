# Configuration settings for MQTT Broker
BROKER = "192.168.1.110"  # broker address
PORT = 1883
DEVICE_ID = "embedded"

STATUS_TOPIC = f"status/{DEVICE_ID}"  # status topic for this device
RESPONSE_TOPIC = f"response/device/{DEVICE_ID}"  # response topic for this device
DIRECT_TOPIC = f"device/{DEVICE_ID}"  # direct messages to this device

LWT_MESSAGE = f"offline due to error"  # last will and testament message
OFFLINE_MESSAGE = f"offline"  # message to send when device goes offline
ONLINE_MESSAGE = f"online"  # message to send when device comes online
# COMMAND_TOPIC = f"device/{DEVICE_ID}/command"  # command topic for this device
