# Import the pygame module
from threading import Thread

import pygame
import time
import random
from random import randint

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

# mapArray = [  # original
# 	["#", "#", "#", "#", "#", "#", "#"],
# 	["#", "=", "=", "#", "=", "=", "#"],
# 	["#", "=", "=", "#", "F", "=", "#"],
# 	["#", "=", "=", "=", "=", "=", "#"],
# 	["#", "=", "=", "T", "=", "=", "#"],
# 	["#", "S", "=", "=", "=", "=", "#"],
# 	["#", "#", "#", "#", "#", "#", "#"]
# ]







class MapElement(pygame.sprite.Sprite):
    def __init__(self, imagePath):
        super(MapElement, self).__init__()
        self.surf = pygame.image.load(imagePath).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    
    def setPosition(self,corX,corY):
        self.rect = self.surf.get_rect(center=(corX+(self.surf.get_width()/2), corY + (self.surf.get_height()/2)))

    def scale(self,a,b):
        self.surf = pygame.transform.scale(self.surf, (a, b))
        
    

        
    


# Define constants for the screen width and height
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("taxi_assets/taxiCar.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100, 100))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        
         # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class GameGraphics:
    
    screen = None
    all_sprites = pygame.sprite.Group()  # used for rendering
    clock = None
    # player = None
    
    # Variable to keep the main loop running
    running = True
    
    count = 0
    xPosition = 0
    yPosition = 0
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        
        self.addBackgroundSprite()
    
    def addBackgroundSprite(self):
        element = MapElement("taxi_assets/emptyGrid-2.png")
        element.scale(500, 500)
        element.setPosition(100, 100)
        
        self.all_sprites.add(element)
    
    def drawGrid(self, mapArray):
        print("Draw is called", self, mapArray)
        self.xPosition = 0
        self.yPosition = 0
        self.all_sprites.empty()
        self.addBackgroundSprite()
        
        for i in range(len(mapArray)):
            for j in range(len(mapArray[i])):
                
                # print(mapArray[i][j], self.xPosition, self.yPosition, end=" ")
                
                if mapArray[i][j] == "#" :
                    if i == 0 or i == 6 or j == 0 or j == 6:
                        element = MapElement("taxi_assets/brick_wall.png")
                        element.scale(100,100)
                        element.setPosition(self.xPosition, self.yPosition)
                    else:
                        val = randint(1,3)
                        if val == 1:
                            element = MapElement("taxi_assets/house1.png")
                        elif val == 2:
                            element = MapElement("taxi_assets/house2.png")
                        else:
                            element = MapElement("taxi_assets/house3.png")
                        element.scale(80,80)
                        element.setPosition(self.xPosition + 12, self.yPosition + 7)
                    
                    self.all_sprites.add(element)
                    
        
                if mapArray[i][j] == "T" :
                    element = MapElement("taxi_assets/taxiCar.png")
                    element.setPosition(self.xPosition + 10, self.yPosition)
                    element.scale(90,90)
                    self.all_sprites.add(element)
        
                if mapArray[i][j] == "S" :
                    element = MapElement("taxi_assets/samirMlm.png")
                    element.setPosition(self.xPosition + 13, self.yPosition + 13)
                    element.scale(70,70)
                    self.all_sprites.add(element)
                
                if mapArray[i][j] == "F" :
                    element = MapElement("taxi_assets/destination.png")
                    element.setPosition(self.xPosition + 23, self.yPosition +12)
                    element.scale(70,70)
                    self.all_sprites.add(element)
                
                self.xPosition = self.xPosition + 100
            self.xPosition = 0
            self.yPosition = self.yPosition + 100
            # print()
    
            
    def activateScreen(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                elif event.type == QUIT:
                    self.running = False

            # Fill the screen with black
            self.screen.fill((128, 128, 128))
            
            if len(self.all_sprites) not in [33, 32]:
                continue
            
            # Draw entities on the screen
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)
        
            # Update the display
            pygame.display.flip()
            # self.clock.tick(1)
            time.sleep(0.5)

if __name__ == "__main__":
    graphics = GameGraphics()
    graphics.drawGrid(mapArray)
    thread = Thread(target = graphics.activateScreen())
    thread.start()
    print("it works")
