# blade_guard.py


class BladeGuard:
    def __init__(self, mqtt_handler):
        self.mqtt_handler = mqtt_handler  # Initialize the MQTT handler
        self.blade_status = "off"  # Initialize the blade status to off

    def handle_mqtt_message(self, client, payload):
        if payload == "ON":
            self.start_blade_guard()
        elif payload == "OFF":
            self.stop_blade_guard()
        elif payload == "LEFT":
            self.move_left()
        elif payload == "RIGHT":
            self.move_right()
        else:
            print("Invalid command")

    def start_blade_guard(self):
        if self.blade_status == "off":  # Check if the blade is off
            self.blade_status = "on"

            # Publish a message to the MQTT broker for the blade status
            self.mqtt_handler.client.publish(
                "home/status/emb/blade_guard", "ON", qos=1, retain=True
            )
            print("Blade_guard has started spinning.")
        else:
            self.mqtt_handler.client.publish(
                "home/status/emb/blade_guard", "ALREADY ON", qos=1, retain=True
            )
            print("Blade_guard is already spinning.")

    def stop_blade_guard(self):
        if self.blade_status == "on":  # Check if the blade is on
            self.blade_status = "off"

            # Publish a message to the MQTT broker for the blade status
            self.mqtt_handler.client.publish(
                "home/status/emb/blade_guard", "OFF", qos=1, retain=True
            )
            print("Blade_guard has stopped spinning.")
        else:
            self.mqtt_handler.client.publish(
                "home/status/emb/blade_guard", "ALREADY OFF", qos=1, retain=True
            )
            print("Blade_guard is already stopped.")

    def move_left(self):
        self.mqtt_handler.client.publish(
            "home/status/emb/blade_guard", "LEFT", qos=1, retain=True
        )
        print("Blade_guard is moving left.")

    def move_right(self):
        self.mqtt_handler.client.publish(
            "home/status/emb/blade_guard", "RIGHT", qos=1, retain=True
        )
        print("Blade_guard is moving right.")
