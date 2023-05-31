# Application File


import pygame
import python_weather
import asyncio
import os
import time




class App:
    """
    Configurable Variables
    """
    coordsHeader    = (110,     10)
    coordsInfo      = (10,      200)
    coordsTime      = (1470,    5)
    coordsTemp      = (310,     200)
    coordsHumidity  = (coordsTemp[0] + 440,     coordsTemp[1] + 30)
    coordsWind      = (coordsTemp[0] + 440,     coordsTemp[1] + 100)
    coordsImage     = (1280,    150)

    weatherUpdateFrequencySeconds = 900

    # Initialize
    def __init__(self):


        self.fontTemperature = pygame.font.SysFont('timesnewroman', int(175))
        self.fontHeader = pygame.font.SysFont('timesnewroman', int(140))
        self.fontInfo = pygame.font.SysFont('timesnewroman', int(65))
        self.fontTime = pygame.font.SysFont('timesnewroman', int(40))
        self.colorText = (225, 225, 225)
        self.colorTempText = (255, 255, 255)
        self.colorBackground = (50, 50, 50)

        self.timer = time.time()
        asyncio.run(updateWeatherWillow())
        pass


    # Handle Mouse / Touch Inputs from user
    def handleMouse(self, event):
        
        pass

    def handleKeyboard(self, event):
        return event.type != pygame.KEYDOWN


    def update(self):
        deltaTime = time.time() - self.timer
        if deltaTime > self.weatherUpdateFrequencySeconds:
            print(deltaTime)
            self.timer = time.time()
        pass



    def paint(self, screen):
        screen.fill(self.colorBackground)
        self.paintTime(screen)
        self.paintWillowRiver(screen)

        pass

    def paintTime(self, screen):
        text = self.fontTime.render("{}".format(time.ctime()), True, self.colorText)
        screen.blit(text, App.coordsTime)
        pass

    def paintWillowRiver(self, screen):

        # Write Title
        textTitle = self.fontHeader.render("WILLOW RIVER", True, self.colorText)
        screen.blit(textTitle, App.coordsHeader)

        # Write Temperature, Humidity, Wind
        textTemperature = self.fontTemperature.render("{}°F".format(Willow.temperature), True, self.colorTempText)
        screen.blit(textTemperature, App.coordsTemp)

        # Write Humidity
        textHumidity = self.fontInfo.render("{}% Humidity".format(Willow.humidity), True, self.colorText)
        screen.blit(textHumidity, App.coordsHumidity)

        # Write Wind
        textWind = self.fontInfo.render("{} MPH".format(Willow.wind), True, self.colorText)
        screen.blit(textWind, App.coordsWind)

        # Draw Image
        screen.blit(Willow.img_1, App.coordsImage)

        pass


class Willow:

    img_1 = pygame.transform.scale(pygame.image.load('Data/WillowRiver_1.JPG'), (600, 900))

    temperature = 999
    humidity = 999
    wind = 999



async def updateWeatherWillow():
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get("Hudson, WI")
        print(weather.current.temperature)
        Willow.temperature = weather.current.temperature
        Willow.humidity = weather.current.humidity
        Willow.wind = weather.current.wind_speed

