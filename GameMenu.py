import pygame
import pygame_menu
from pygame_menu import sound


pygame.init()

win_size = (700, 600)
screen = pygame.display.set_mode(win_size)

pygame.display.set_caption('Taxi Game AI')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

def start_the_game():
    # write code
    print("Start")
    #import GameGraphics as gg
    #x = gg()
    pass

def start_AI_the_game():
    # write code
    print("Start (AI)")
    pass

def start_new_agent_the_game():
    # write code
    print("Train New Agent")
    pass

menu = pygame_menu.Menu(win_size[1], win_size[0], 'Main Menu', theme=pygame_menu.themes.THEME_SOLARIZED)

menu.add_text_input('', default='Artifial Intelligence')
menu.add_vertical_margin(20)

menu.add_button('Start', start_the_game)
menu.add_vertical_margin(20)

menu.add_button('Start AI', start_AI_the_game)
menu.add_vertical_margin(20)

menu.add_button('Train New Agent', start_new_agent_the_game)
menu.add_vertical_margin(20)

# menu.add_button('About', start_new_agent_the_game)
# menu.add_vertical_margin(20)

menu.add_button('Quit', pygame_menu.events.EXIT)



menu.mainloop(screen)
