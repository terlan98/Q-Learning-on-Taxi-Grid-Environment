# # Import libraries
# import sys

# sys.path.insert(0, '../../')

import os
import pygame
import copy
import pygame_menu
from GameController import GameController
from GameGraphics import SCREEN_WIDTH, SCREEN_HEIGHT

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ["Aritifical Integigent About Page",
         "sahdbhasdba skjdbksjabdjas kdbaskas",
         "dashdbkjasbd dajsdbkjaskdbjas",
         "sjadnas asdnaskj"]

PATH = 'taxi_assets/'
pic1 = 'icon.png'
pic2 = "ai.png"

FPS = 60.0
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

sound = None  # type: pygame_menu.sound.Sound
surface = None  # type: pygame.Surface
main_menu = None  # type: pygame_menu.Menu
clock = None


def start_the_game(test = False):    
    # main_menu.disable()
    # main_menu.reset(1)
    GameController().run()
    exit()
   
def start_AI_the_game():
    print("Start (AI)")
    print("Menu Exit")
    #main_menu.disable()
    #main_menu.reset(1)
    GameController().run()
    exit()
    

def start_new_agent_the_game():
    # write code
    print("Train New Agent")
    GameController().run()
    exit()
    #exit

COLORS = [(0,0,0),
          (100, 131, 147),
          (100, 171, 181),
          (115, 131, 147),
          (46, 131, 147),
          (46, 131, 98),
          (46, 70, 98),
          (10, 117, 75),
          (79, 102, 175),
          (31, 92, 175),
          (255, 255, 255)]


def main(test=False):
    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    # os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Taxi AI Game')

    icon = pygame.image.load(PATH + pic1)
    pygame.display.set_icon(icon)
    
    clock = pygame.time.Clock()
    
    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    play_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
    
    play_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1],
        onclose=pygame_menu.events.DISABLE_CLOSE,
        # onclose=pygame_menu.events.EXIT,
        theme = play_theme,
        title='Play Menu',
        width=WINDOW_SIZE[0],
    )
    
    play_menu.add_label('Group 5',
                        max_char=-1, 
                        font_size=70, 
                        font_name="Times", 
                        font_color=COLORS[1])
    play_menu.add_vertical_margin(10)

    play_menu.add_image(PATH + pic2, 
                        angle=5, 
                        scale=(0.3, 0.3), 
                        scale_smooth=True)
    play_menu.add_vertical_margin(30)
    
    play_menu.add_button('Start', 
                         start_the_game, 
                         font_name="Times", 
                         font_size=35)
    play_menu.add_vertical_margin(20)
        
    play_menu.add_button('Start AI', 
                         start_AI_the_game, 
                         font_name="Times", 
                         font_size=35)
    play_menu.add_vertical_margin(20) 
    
    play_menu.add_button('Train New Agent', 
                         start_new_agent_the_game, 
                         font_name="Times", 
                         font_size=35)
    play_menu.add_vertical_margin(20) 
    
    play_menu.add_button('Return', 
                         pygame_menu.events.BACK, 
                         font_name="Times", 
                         font_size=35)
    play_menu.add_vertical_margin(20) 
    # play_menu.add_button('Exit', pygame_menu.events.EXIT, font_name="Times", font_size=35)

    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
##    about_theme.widget_margin = (0, 0)
##    about_theme.widget_offset = (0, 0)

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1],
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=about_theme,
        title='About',
        width=WINDOW_SIZE[0],
    )
    for m in ABOUT:
        about_menu.add_label(m, 
                             align=pygame_menu.locals.ALIGN_CENTER, 
                             font_name="Times", 
                             font_size=30)
    about_menu.add_label('')
    
    about_menu.add_button('Return', 
                          pygame_menu.events.BACK, 
                          font_name="Times", 
                          font_size=35)

  

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
    main_theme.menubar_close_button = False  # Disable close button
    
    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1],
        width=WINDOW_SIZE[0],
        onclose=pygame_menu.events.EXIT,
        title='Main Menu',
        theme=main_theme,
    )

    main_menu.add_label('Artifial Intelligence',
               max_char=-1, 
               font_size=70, 
               font_name="Times", 
               font_color=COLORS[1])
    main_menu.add_vertical_margin(10)

    main_menu.add_image(PATH + pic1,
               angle=15,
               scale=(0.2, 0.2), 
               scale_smooth=True)
    main_menu.add_vertical_margin(40)

    main_menu.add_button('Play', 
                         play_menu,
                         font_name="Times", 
                         font_size=35)
    main_menu.add_vertical_margin(20)
    
    main_menu.add_button('About', 
                         about_menu, 
                         font_name="Times", 
                         font_size=35)
    main_menu.add_vertical_margin(20)
    
    main_menu.add_button('Quit', 
                         pygame_menu.events.EXIT, 
                         font_name="Times", 
                         font_size=35)
    main_menu.add_vertical_margin(20)
    #main_menu.mainloop(surface,  fps_limit=FPS)
    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
##        main_background()
        
        # # Application events
        # events = pygame.event.get()
        # for event in events:
        #     if event.type == pygame.QUIT:
        #         exit()

                
        # Main menu
        main_menu.mainloop(surface, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
