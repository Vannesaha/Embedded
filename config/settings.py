# Configuration settings for MQTT Broker
BROKER = "localhost"  # broker address
PORT = 1883
DEVICE_ID = "hydraulic"

STATUS_TOPIC = f"status/device/{DEVICE_ID}"  # status topic for this device
RESPONSE_TOPIC = f"response/device/{DEVICE_ID}"  # response topic for this device
DIRECT_TOPIC = f"device/{DEVICE_ID}"  # direct messages to this device

LWT_MESSAGE = f"{DEVICE_ID}: offline due to error"  # last will and testament message
OFFLINE_MESSAGE = f"{DEVICE_ID}: offline"  # message to send when device goes offline
# COMMAND_TOPIC = f"device/{DEVICE_ID}/command"  # command topic for this device
