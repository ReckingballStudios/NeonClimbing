# Screen File

import pygame

usingRaspberryPi = False

class Screen:

    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.fpsClock = pygame.time.Clock()
        if usingRaspberryPi:
            self.pyScreen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.width = 1024
            self.height = 600
            self.pyScreen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Neon Climbing")
        pass

    def resetScreen(self, width, height):
        self.width = width
        self.height = height
        self.pyScreen = pygame.display.set_mode((self.width, self.height))
        pass
