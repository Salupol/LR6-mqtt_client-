import paho.mqtt.client as mqtt
import pygame
import json
from datetime import datetime


class MQTTClient:
    def __init__(self, broker_address, broker_port, username, password):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username, password)

        try:
            self.client.connect(broker_address, broker_port, 60)
        except:
            self.error_message = "Failed to connect to MQTT server"
            self.write_to_log(self.error_message)
            self.display_info(self.error_message, success=False)

    def write_to_log(self, message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open('data.log', 'a') as log_file:
            log_entry = f"[{current_time}] {message}\n"
            log_file.write(log_entry)

    def display_info(self, message, success=True):
        font = pygame.font.Font(None, 36)
        screen.fill((0, 0, 0))
        text_color = (0, 255, 0) if success else (255, 0, 0)
        text = font.render(message, True, text_color)
        text2 = font.render('Press q to quit', True, (255, 255, 255))
        screen.blit(text, (50, 50))
        screen.blit(text2, (500, 700))
        pygame.display.flip()

    def display_clock(self, screen):
        font = pygame.font.Font(None, 48)
        current_time = datetime.now().strftime("%H:%M:%S")
        clock_text = font.render(current_time, True, (255, 255, 255), (0, 0, 0, 0))
        screen_width, screen_height = screen.get_size()
        center_x = screen_width // 2 - clock_text.get_width() // 2
        center_y = screen_height // 2 - clock_text.get_height() // 2
        transparent_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        transparent_surface.blit(clock_text, (center_x, center_y))
        screen.blit(transparent_surface, (0, 0))
        pygame.display.flip()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.write_to_log("Connected successfully, waiting for messages")
            self.display_info("Connected successfully, waiting for messages")
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
        font = pygame.font.Font(None, 36)
        screen.fill((0, 0, 0))

        text = font.render(f'Voltage: {voltage}', True, (255, 255, 255))
        text2 = font.render('Press q to quit', True, (255, 255, 255))
        screen.blit(text, (50, 100))
        screen.blit(text2, (500, 700))
        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Info from MQTT')
mqtt_client = MQTTClient("192.168.0.106", 8883, "owntracks", "zhopa")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
            exit()
    pygame.display.flip()
    mqtt_client.display_clock(screen)
    mqtt_client.client.loop(1)
pygame.quit()
