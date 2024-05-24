# Status-luokka hallinnoimaan laitteen tilaa ja viestien käsittelyä


class Status:
    def __init__(self, mqtt_handler, broker):
        self.mqtt_handler = mqtt_handler  # Alustetaan MQTT-handler
        self.broker = broker  # MQTT brokerin osoite
        self.is_online = "offline"  # Alustetaan laitteen tila offline-tilaan

    def handle_mqtt_message(self, client, payload):
        # Käsitellään saapuvat MQTT-viestit
        if payload == "":
            self.send_current_status()  # Lähetetään nykyinen tila, jos viesti on tyhjä
        else:
            print(
                "Invalid command"
            )  # Tulostetaan virheviesti, jos komento on virheellinen

    def send_current_status(self):
        # Lähetetään laitteen nykyinen tila
        current_status = self.is_online  # Haetaan nykyinen tila
        self.mqtt_handler.client.publish(
            "home/status/emb", current_status, qos=1, retain=True
        )  # Julkaistaan tila MQTT:lle
        print(f"Embedded status is {current_status}.")  # Tulostetaan tila

    def on_connect(self, client, userdata, flags, rc):
        # Käsitellään yhteyden muodostaminen
        if rc == 0:
            print(
                f"Connected successfully to broker: {self.broker}."
            )  # Tulostetaan onnistunut yhteysviesti
            self.is_online = "online"  # Päivitetään tila online-tilaan
            client.publish(
                "home/status/emb", "online", qos=1, retain=True
            )  # Julkaistaan online-viesti

    def on_disconnect(self, client, userdata, rc):
        # Käsitellään yhteyden katkeaminen
        if rc != 0:
            self.is_online = "offline"  # Päivitetään tila offline-tilaan
            print(
                "Unexpected disconnection."
            )  # Tulostetaan virheviesti odottamattomasta katkeamisesta
