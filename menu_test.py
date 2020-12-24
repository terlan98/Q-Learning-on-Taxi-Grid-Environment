import pygame
import pygame_menu
from pygame_menu import sound


pygame.init()

win_size = (700, 600)
screen = pygame.display.set_mode(win_size)

PATH = 'taxi_assets\icon.png'

pygame.display.set_caption('Taxi Game AI')
icon = pygame.image.load(PATH)
pygame.display.set_icon(icon)

def start_the_game():
    # write code
    print("Start")

def start_AI_the_game():
    # write code
    print("Start (AI)")

def start_new_agent_the_game():
    # write code
    print("Train New Agent")

menu = pygame_menu.Menu(win_size[1], win_size[0], 'Main Menu', theme=pygame_menu.themes.THEME_SOLARIZED)

menu.add_label('Artifial Intelligence',
               max_char=-1, 
               font_size=70, 
               font_name="Times", 
               font_color=(125, 125, 135))
menu.add_vertical_margin(10)

menu.add_image(PATH,
               angle=15,
               #margin=(-100,-25)
               scale=(0.2, 0.2), 
               scale_smooth=True)
menu.add_vertical_margin(20)



menu.add_button('Start', 
                start_the_game,
                font_name="Times", 
                font_color=(125, 125, 125), 
                font_size=35)
menu.add_vertical_margin(20)

menu.add_button('Start AI', 
                start_AI_the_game, 
                font_name="Times", 
                font_color=(125, 125, 125), 
                font_size=35)
menu.add_vertical_margin(20)

menu.add_button('Train New Agent', 
                start_new_agent_the_game, 
                font_name="Times", 
                font_color=(125, 125, 125), 
                font_size=35)
menu.add_vertical_margin(20)


menu.add_button('Quit', pygame_menu.events.EXIT)
menu.add_vertical_margin(20)


menu.mainloop(screen)
