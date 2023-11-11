import paho.mqtt.client as mqtt
import pygame
import json
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
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Info from MQTT')

    # Set up fonts
    font = pygame.font.Font(None, 36)
    text = font.render(f'Voltage: {voltage}', True, (255, 255, 255))
    #printing "press q to quit"
    text2 = font.render(f'Press q to quit', True, (255, 255, 255))


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
        # Draw the text on the screen
        screen.fill((0, 0, 0))
        screen.blit(text, (50, 50))
        screen.blit(text2, (500, 700 ))
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





