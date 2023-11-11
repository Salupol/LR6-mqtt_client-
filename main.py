import paho.mqtt.client as mqtt
import pygame
import json


class MQTTClient:
    def __init__(self, broker_address, broker_port, username, password):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username, password)

        try:
            self.client.connect(broker_address, broker_port, 60)
        except Exception:
            self.error_message = "Failed to connect to MQTT server"
            self.write_to_log(self.error_message)
            self.display_info(self.error_message, success=False)


    def write_to_log(self, message):
        with open('data.log', 'a') as log_file:
            log_file.write(message + '\n')

    def display_info(self, message, success=True):
        # Set up fonts
        font = pygame.font.Font(None, 36)

        # Draw the text on the screen
        screen.fill((0, 0, 0))
        text_color = (0, 255, 0) if success else (255, 0, 0)
        text = font.render(message, True, text_color)
        text2 = font.render('Press q to quit', True, (255, 255, 255))
        screen.blit(text, (50, 50))
        screen.blit(text2, (500, 700))
        pygame.display.flip()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.write_to_log("Connected successfully")
            self.display_info("Connected successfully")
            self.client.subscribe("tele/main_battery/SENSOR")
        else:
            error_message = f"Connection failed with result code {rc}"
            self.write_to_log(error_message)
            self.display_info(error_message, success=False)

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        voltage = data.get('voltage')

        if voltage is not None:
            self.write_to_log(f"Received voltage: {voltage}")
            self.display_temperature(voltage)

    def display_temperature(self, voltage):
        # Set up fonts
        font = pygame.font.Font(None, 36)

        # Draw the text on the screen
        text = font.render(f'Voltage: {voltage}', True, (255, 255, 255))
        text2 = font.render('Press q to quit', True, (255, 255, 255))
        screen.blit(text, (50, 100))
        screen.blit(text2, (500, 700))
        pygame.display.flip()

# Initialize pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Info from MQTT')

# Create an instance of the MQTTClient class
mqtt_client = MQTTClient("192.168.0.106", 8883, "owntracks", "zhopa")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
            exit()

    # Continue the Pygame display update
    pygame.display.flip()

    # Continue the MQTT loop
    mqtt_client.client.loop(1)  # Add a short delay to avoid high CPU usage

# Quit pygame
pygame.quit()
