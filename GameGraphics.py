# Import the pygame module
import pygame
import random
import time

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
    QUIT,
)

mapArray = [  # original
	["#", "#", "#", "#", "#", "#", "#"],
	["#", "=", "=", "#", "=", "=", "#"],
	["#", "=", "=", "#", "F", "=", "#"],
	["#", "=", "=", "=", "=", "=", "#"],
	["#", "=", "=", "T", "=", "=", "#"],
	["#", "S", "=", "=", "=", "=", "#"],
	["#", "#", "#", "#", "#", "#", "#"]
]







class MapElement(pygame.sprite.Sprite):
    def __init__(self, imagePath):
        super(MapElement, self).__init__()
        self.surf = pygame.image.load(imagePath).convert_alpha()
        #self.surf = pygame.transform.scale(self.surf, (100, 100))
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
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -100)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 100)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-100, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(100, 0)
        
         # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT



# Initialize pygame
pygame.init()




# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
all_sprites = pygame.sprite.Group()

element = MapElement("taxi_assets/emptyGrid-2.png")
element.scale(500,500)
element.setPosition(100,100)
all_sprites.add(element)

# Instantiate player and map
player = Player()


# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering

all_sprites.add(player)


clock = pygame.time.Clock()

# Variable to keep the main loop running
running = True



count = 0
xPosition = 0
yPosition = 0


    
for i in range(len(mapArray)):
    for j in range(len(mapArray[i])):
        print(mapArray[i][j], xPosition, yPosition ,end=" ")
        if mapArray[i][j] == "#" :
            if i == 0 or i == 6 or j == 0 or j == 6:
                element = MapElement("taxi_assets/brick_wall.png")
            else:
                element = MapElement("taxi_assets/house1.png")
            
            element.setPosition(xPosition,yPosition)
            all_sprites.add(element)
                    

        if mapArray[i][j] == "T" :
            element = MapElement("taxi_assets/taxiCar.png")
            element.setPosition(xPosition,yPosition)
            all_sprites.add(element)

        if mapArray[i][j] == "S" :
            element = MapElement("taxi_assets/samirMlm.png")
            element.setPosition(xPosition + 25,yPosition + 25)
            all_sprites.add(element)

        
        if mapArray[i][j] == "F" :
            element = MapElement("taxi_assets/destination.png")
            element.setPosition(xPosition + 35,yPosition + 25)
            all_sprites.add(element)
        
        

        
        xPosition = xPosition + 100
    xPosition = 0
    yPosition = yPosition + 100
    print()




# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False

        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False



    

    
    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player and enemies sprite based on user keypresses
    player.update(pressed_keys)

    # Fill the screen with black
    screen.fill((128, 128, 128))

    # Draw the player and enemies on the screen
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # Update the display
    pygame.display.flip()
    clock.tick(30)
    # time.sleep(100)


