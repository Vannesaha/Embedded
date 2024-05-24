# embedded.py


# EmbeddedDevice class
class EmbeddedDevice:
    def __init__(self, mqtt_handler):

        self.mqtt_handler = mqtt_handler  # Initialize the MQTT handler
        self.blade_status = "off"  # Initialize the blade status to off

    # Handle the MQTT message for the blade
    def handle_mqtt_message(self, client, payload):
        if payload == "ON":
            self.start_blade()
        elif payload == "OFF":
            self.stop_blade()
        else:
            print("Invalid command")

    def start_blade(self):
        if self.blade_status == "off":  # Check if the blade is off
            self.blade_status = "on"

            # Publish a message to the MQTT broker for the blade status
            self.mqtt_handler.client.publish(
                "home/status/emb/blade", "ON", qos=1, retain=True
            )
            print("Blade has started spinning.")
        else:
            self.mqtt_handler.client.publish(
                "home/status/emb/blade", "ALREADY ON", qos=1, retain=True
            )
            print("Blade is already spinning.")

    def stop_blade(self):
        if self.blade_status == "on":  # Check if the blade is on
            self.blade_status = "off"

            # Publish a message to the MQTT broker for the blade status
            self.mqtt_handler.client.publish(
                "home/status/emb/blade", "OFF", qos=1, retain=True
            )
            print("Blade has stopped spinning.")
        else:
            self.mqtt_handler.client.publish(
                "home/status/emb/blade", "ALREADY OFF", qos=1, retain=True
            )
            print("Blade is already stopped.")
