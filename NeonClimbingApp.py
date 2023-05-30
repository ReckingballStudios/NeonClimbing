# Application File


import pygame



class App:
    """
    Configurable Variables
    """
    headerCoords = (10, 10)
    infoCoords = (10, 125)
    tempCoords = (190, 125)
    imageCoords = (600, 150)





    # Initialize
    def __init__(self):


        self.fontTemperature = pygame.font.SysFont('timesnewroman', int(100))
        self.fontHeader = pygame.font.SysFont('timesnewroman', int(80))
        self.fontInfo = pygame.font.SysFont('timesnewroman', int(25))
        self.colorText = (200, 200, 200)
        self.colorTempText = (255, 255, 255)
        
        pass


    # Handle Mouse / Touch Inputs from user
    def handleMouse(self, event):
        
        pass

    def handleKeyboard(self, event):
        return event.type != pygame.KEYDOWN


    def update(self):

        pass



    def paint(self, screen):

        self.paintWillowRiver(screen)

        pass


    def paintWillowRiver(self, screen):
        text = self.fontHeader.render("WILLOW RIVER", True, self.colorText)
        screen.blit(text, App.headerCoords)

        screen.blit(Willow.img_1, App.imageCoords)

        text = self.fontTemperature.render("76°F", True, self.colorTempText)
        screen.blit(text, App.tempCoords)
        pass


class Willow:

    img_1 = pygame.transform.scale(pygame.image.load('Data/WillowRiver_1.JPG'), (400, 400))

    def __init__(self):

        pass

    def getTemperature(self):

        pass
