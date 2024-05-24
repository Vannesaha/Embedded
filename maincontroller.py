# maincontroller.py

from src.utils.mqtt_handler import MQTTHandler


class MainController:
    def __init__(self):
        self.mqtt_handler = MQTTHandler()

    def start(self):
        self.mqtt_handler.run()
