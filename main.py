import paho.mqtt.client as mqtt
import pygame
import json
import threading
import time
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("tele/main_battery/SENSOR")
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print(data['voltage'])
    display_temperature(data['voltage'])


def display_temperature(voltage):
    # Initialize pygame
    pygame.init()

    # Create a window
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption('Temperature Display')

    # Set up fonts
    font = pygame.font.Font(None, 36)
    text = font.render(f'Temperature: {voltage}', True, (255, 255, 255))

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the text on the screen
        screen.fill((0, 0, 0))
        screen.blit(text, (50, 50))
        pygame.display.flip()

    # Quit pygame
    pygame.quit()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
username = "owntracks"
password = "zhopa"
client.username_pw_set(username, password)
client.connect("192.168.0.106", 8883, 60)
client.loop_forever()





