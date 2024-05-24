# status.py


class Status:
    def __init__(
        self,
        mqtt_handler,
    ):
        self.mqtt_handler = mqtt_handler  # Initialize the MQTT handler

    def handle_mqtt_message(self, client, payload):
        if payload == "":
            self.send_current_status()
        else:
            print("Invalid command")

    def send_current_status(self):
        # Get the current status of the device
        current_status = self.mqtt_handler.is_online

        # Publish a message to the MQTT broker for the blade status
        self.mqtt_handler.client.publish(
            "home/status/emb", current_status, qos=1, retain=True
        )
        print(f"embedded status is.  {current_status}.")
