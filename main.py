import paho.mqtt.client as mqtt
import pygame
import json


# Function to write logs to a file
def write_to_log(message):
    with open('data.log', 'a') as log_file:
        log_file.write(message + '\n')


# Function to update the temperature display in Pygame
def display_temperature(voltage):
    # Set up fonts
    font = pygame.font.Font(None, 36)

    # Draw the text on the screen
    screen.fill((0, 0, 0))
    text = font.render(f'Voltage: {voltage}', True, (255, 255, 255))
    text2 = font.render(f'Press q to quit', True, (255, 255, 255))
    screen.blit(text, (50, 50))
    screen.blit(text2, (500, 700))
    pygame.display.flip()


def on_connect(client, userdata, flags, rc):
    write_to_log("Connected with result code " + str(rc))
    print("Connected with result code " + str(rc))
    client.subscribe("tele/main_battery/SENSOR")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    voltage = data.get('voltage')

    if voltage is not None:
        write_to_log(f"Received voltage: {voltage}")
        print(f"Received voltage: {voltage}")
        display_temperature(voltage)


# Initialize pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Info from MQTT')

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
username = "owntracks"
password = "zhopa"
client.username_pw_set(username, password)
client.connect("192.168.0.106", 8883, 60)

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
    client.loop(0.1)  # Add a short delay to avoid high CPU usage

# Quit pygame
pygame.quit()
