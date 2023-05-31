# Screen File

import pygame



class Screen:

    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.fpsClock = pygame.time.Clock()
        self.pyScreen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("Neon Climbing")
        pass

    def resetScreen(self, width, height):
        self.width = width
        self.height = height
        self.pyScreen = pygame.display.set_mode((self.width, self.height))
        pass
