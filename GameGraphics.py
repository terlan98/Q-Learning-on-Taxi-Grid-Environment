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

from Agent import Agent, env

LOCS = [(0, 0), (0, 4), (4, 0), (4, 3)]


class MapElement(pygame.sprite.Sprite):
    def __init__(self, imagePath):
        super(MapElement, self).__init__()
        self.surf = pygame.image.load(imagePath).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

    def setPosition(self, corX, corY):
        self.rect = self.surf.get_rect(
            center=(corX+(self.surf.get_width()/2), corY + (self.surf.get_height()/2)))

    def scale(self, a, b):
        self.surf = pygame.transform.scale(self.surf, (a, b))


# Define constants for the screen width and height
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

SPRITE_WIDTH = 70
SPRITE_HEIGHT = 70

val = randint(1, 3)


class GameGraphics:

    screen = None
    all_sprites = pygame.sprite.Group()  # used for rendering
    clock = None
    # player = None

    # Variable to keep the main loop running
    running = True

    # To prevent refreshing screen while sprites are being created
    # freezeScreen = False

    count = 0
    xPosition = 0
    yPosition = 0

    def __init__(self):
        # Initialize pygame
        self.agent = Agent.train(num_epochs=100000)
        pygame.init()

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()

        self.addBackgroundSprite()

    def addBackgroundSprite(self):
        element = MapElement("taxi_assets/emptyGrid.png")
        element.scale(SCREEN_WIDTH, SCREEN_HEIGHT)
        element.setPosition(-15, -15)

        self.all_sprites.add(element)

    def drawGrid(self, state):
        # self.freezeScreen = True
        self.xPosition = 85
        self.yPosition = 90
        self.all_sprites.empty()
        self.addBackgroundSprite()

        taxiRow, taxiCol, passIndex, destIndex = map(int, state)

        for i in range(5):
            for j in range(5):
                # print(mapArray[i][j], self.xPosition, self.yPosition, end=" ")

                if i == taxiRow and j == taxiCol:
                    element = MapElement("taxi_assets/taxiCar.png")
                    element.scale(SPRITE_WIDTH, SPRITE_HEIGHT)
                    element.setPosition(self.xPosition - 10,
                                        self.yPosition - 15)
                    self.all_sprites.add(element)
                elif passIndex != 4 and i == LOCS[passIndex][0] and j == LOCS[passIndex][1]:
                    element = MapElement("taxi_assets/samirMlm.png")
                    element.scale(SPRITE_WIDTH, SPRITE_HEIGHT)
                    element.setPosition(self.xPosition, self.yPosition)
                    self.all_sprites.add(element)
                elif i == LOCS[destIndex][0] and j == LOCS[destIndex][1]:
                    element = MapElement("taxi_assets/destination.png")
                    element.scale(SPRITE_WIDTH, SPRITE_HEIGHT)
                    element.setPosition(self.xPosition + 10, self.yPosition)
                    self.all_sprites.add(element)

                self.xPosition = self.xPosition + 90
            self.xPosition = 100
            self.yPosition = self.yPosition + 100
        # self.freezeScreen = False
        # print()

    def activateScreen(self, num_rounds):
        while num_rounds:
            while not self.agent.done and self.running:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.running = False
                    elif event.type == QUIT:
                        self.running = False

                state = self.agent.make_move()
                self.drawGrid(state)

                # Fill the screen with black
                self.screen.fill((133, 131, 131))

                # Draw entities on the screen
                for entity in self.all_sprites:
                    self.screen.blit(entity.surf, entity.rect)

                # Update the display
                pygame.display.flip()
                self.clock.tick(3)

            self.agent.cur_state = env.reset()
            self.agent.done = False
            num_rounds -= 1
            # time.sleep(1)


if __name__ == "__main__":
    graphics = GameGraphics()
    # graphics.drawGrid("2201")  # taxi i, taxi j, pass indx, dest index
    graphics.activateScreen(num_rounds=10)
    print("it works")
