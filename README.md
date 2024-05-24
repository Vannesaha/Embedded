## Testing

This application uses MQTT for communication. You can use the `mosquitto_sub` and `mosquitto_pub` commands to subscribe to topics and publish messages for testing.

1. **Status Messages:** The application publishes status messages (such as connection and offline messages) to the `home/status/emb` topic. To see these messages, subscribe to this topic using the following command:

   ```bash
   mosquitto_sub -h localhost -t home/status/emb
   ```

   When the application starts, you should automatically see connection and offline messages.

2. **Status Control Messages:** The application listens for control messages on the `home/control/emb/status` topic. To send a control message, you can use the `mosquitto_pub` command. For example, to send an empty control message, use the following command:

   ```bash
   mosquitto_pub -h localhost -p 1883 -t home/control/emb/status -m ""
   ```

   The application will respond to control messages by publishing a status message. To see these responses, you can subscribe to the `home/status/emb/` topic:

   ```bash
   mosquitto_sub -h localhost -t home/control/emb/status
   ```

3. **Blade Status Messages:** The application publishes blade status messages to the `home/status/emb/blade` topic. To see these messages, subscribe to this topic using the following command:

   ```bash
   mosquitto_sub -h localhost -t home/status/emb/blade
   ```

4. **Blade Control Messages:** The application listens for blade control messages on the `home/control/emb/blade` topic. To send a blade control message, you can use the `mosquitto_pub` command. For example, to turn the blade on or off, use the following command:

   ```bash
   mosquitto_pub -h localhost -p 1883 -t home/control/emb/blade -m "ON"
   ```

Remember to replace `localhost` with the address of your MQTT broker if it's not running on your local machine.
