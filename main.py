import sys, pygame
from pygame.locals import *
import time
import subprocess
import os
import toml
import requests
from subprocess import *
from time import gmtime, strftime

#Configuration for ToucheScreen
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

#Loading config file.
config = toml.load('config.toml')

# Initialize pygame and hide mouse
pygame.init()
#pygame.display.init()

pygame.mouse.set_visible(1)

# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, colour):
    font=pygame.font.Font(None,42)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))
    pygame.draw.rect(screen, white, (xpo-10,ypo-10,width,height),3)

# define function for printing text in a specific place with a specific colour
def make_label(text, xpo, ypo, fontsize, colour):
    font=pygame.font.Font(None,fontsize)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))

# define function for back button
def back_button():
    font=pygame.font.Font(None,25)
    label=font.render(str('Back >'), 1, (red))
    screen.blit(label,(250,200))
    pygame.draw.rect(screen, blue, (245,195,65,30),3)

# define function that checks for touch location
def on_click():
    update_time()
    # get the position that was touched
    touch_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    #  x_min                 x_max   y_min                y_max
    # button 1 event
    if 20 <= touch_pos[0] <= 130 and 53 <= touch_pos[1] <=103:
            button(1)
    # button 2 event
    if 170 <= touch_pos[0] <= 290 and 30 <= touch_pos[1] <=85:
            button(2)

    # button 6 the exit button
    if 277 <= touch_pos[0] <= 320 and 196 <= touch_pos[1] <=240:
            button(2)

# define function for getting and printing the cloak
def update_time():
    le_time = time.strftime("%H:%M:%S", gmtime())
    #Printing white rectangle before the cloak to avoid superposition
    pygame.draw.rect(screen, white,(125,11,90,30))
    make_label(le_time,125,11,30,black)

# define function for getting unique data from url
def get_jeedom_data(id):
    lurl = (config['jeedom']['server_url'] + "/core/api/jeeApi.php?apikey=" + config['jeedom']['apikey'] + "&type=cmd&id=" + id)
    r = requests.get(lurl)
    data = r.content.decode("utf-8")
    return data

# Define each button press action
def button(number):
    print ("You pressed button ",number)

    if number == 1:
        carImg = pygame.image.load("img_src/main_test.png").convert_alpha()
        screen.blit(carImg, (0, 0))
        make_label(get_jeedom_data(config['jeedom']['id_temp_intern']), 200, 120, 55, blue)
        make_label(get_jeedom_data(config['jeedom']['id_meteo_condition']), 200, 100, 20, blue)
        back_button()
        pygame.display.flip()

    if number == 2:
        sys.exit()

    if number == 3:
        time.sleep(5) #do something interesting here
        sys.exit()

    if number == 4:
        time.sleep(5) #do something interesting here
        sys.exit()

    if number == 5:
        time.sleep(5) #do something interesting here
        sys.exit()

    if number == 6:
        sys.exit()


#colors     R    G    B
white   = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)
black   = (  0,   0,   0)
cyan    = ( 50, 255, 255)
magenta = (255,   0, 255)
yellow  = (255, 255,   0)
orange  = (255, 127,   0)

# Set up the base menu you can customize your menu with the colors above

#set size of the screen
size = width, height = 320, 240
screen = pygame.display.set_mode(size,pygame.NOFRAME)

# Background Color
#screen.fill(black)
background = pygame.image.load("img_src/main_v1.png").convert_alpha()
screen.blit(background, (0, 0))

# Buttons and labels
# First Row
make_button("Chauffage", 20, 60, 55, 120, white)
make_button("Menu 2", 170, 60, 55, 120, white)
update_time()

# While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print ("screen pressed") #for debugging purposes
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            print (pos) #for checking
            pygame.draw.circle(screen, white, pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
            on_click()

#ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()