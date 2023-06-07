# Application File


import pygame
import python_weather
from python_weather import enums
import asyncio
from aiohttp import client_exceptions
import os
import time
import math




class App:

    # Coordinates
    coordsHeader    = (110,     10)
    coordsTime      = (1460,    5)
    coordsImage     = (1280,    150)
    coordsClimbIndex = (coordsImage[0] - 80, coordsImage[1])

    coordsCurrently = (coordsHeader[0] + 185,     185)
    coordsIcon      = (15,      220)
    coordsTemp      = (coordsIcon[0] + 250,           coordsIcon[1]+25)
    coordsHumidity  = (coordsTemp[0] + 440,     coordsTemp[1] + 30)
    coordsWind      = (coordsTemp[0] + 440,     coordsTemp[1] + 100)
    coordsPrecip    = (coordsIcon[0] + 200,   coordsTemp[1] + 200)
    coordsPrecipText = (coordsPrecip[0] + 100,   coordsPrecip[1] + 15)
    coordsSunrise   = (coordsPrecip[0] + 280, coordsPrecip[1])
    coordsSunriseText = (coordsSunrise[0] + 110, coordsSunrise[1] + 15)
    coordsSunset    = (coordsSunrise[0] + 340, coordsPrecip[1])
    coordsSunsetText = (coordsSunset[0] + 110, coordsSunset[1] + 15)


    sizeClimbIndex = (72, 900)

    weatherUpdateFrequency = 900
    iterateScreenFrequency = 60

    # Initialize
    def __init__(self):

        # Font and Text initialization
        self.fontTemperature = pygame.font.SysFont('timesnewroman', int(175))
        self.fontHeader = pygame.font.SysFont('timesnewroman', int(140))
        self.fontInfo = pygame.font.SysFont('timesnewroman', int(65))
        self.fontTime = pygame.font.SysFont('timesnewroman', int(40))

        self.colorText = (235, 235, 235)
        self.colorTempText = (255, 255, 255)
        self.colorBackground = (25, 25, 25)

        # Locations Array
        self.currentLocation = Location.WILLOW_RIVER
        self.locations = []
        self.initializeLocations()
        self.locations[self.currentLocation].updateWeather()

        self.iterateTimer = time.time()
        self.weatherTimer = time.time()

        pass


    def initializeLocations(self):
        self.locations.append(Location("Willow River", "Hudson, WI", Location.imgWillow_1))
        self.locations.append(Location("Sandstone", "Sandstone, MN", Location.imgSandstone_1))
        self.locations.append(Location("Red Wing", "Red Wing, MN", Location.imgRedWing_1))
        self.locations.append(Location("Rainy Lake", "International Falls, MN", Location.imgRainyLake_1))
        self.locations.append(Location("Devil's Lake", "Baraboo, WI", Location.imgDevilsLake_1))
        self.locations.append(Location("Red Rocks Canyon", "Las Vegas, NV", Location.imgRedRocks_1))
        self.locations.append(Location("El Potrero Chico", "Hidalgo, NL, MX", Location.imgElPotreroChico_1))
        self.locations.append(Location("Frankenjura", "Regensburg, DE", Location.imgFrankenjura_1))
        pass


    # Handle Mouse / Touch Inputs from user
    def handleMouse(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.iterateLocation()
        pass

    def iterateLocation(self):
        # Go to the next location
        self.currentLocation += 1
        if self.currentLocation >= Location.NUM_LOCATIONS:
            self.currentLocation = 0

        self.locations[self.currentLocation].updateWeather()
        self.iterateTimer = time.time()
        pass


    def handleKeyboard(self, event):
        return event.type != pygame.KEYDOWN


    def update(self):
        # Iterate timer
        deltaTime = time.time() - self.iterateTimer
        if deltaTime > self.iterateScreenFrequency:
            self.iterateLocation()

        # Weather Update Timer
        deltaTime = time.time() - self.weatherTimer
        if deltaTime > self.weatherUpdateFrequency:
            self.weatherTimer = time.time()
            # for i in range(Location.NUM_LOCATIONS):
            #     self.locations[i].updateWeather()
        pass



    def paint(self, screen):
        screen.fill(self.colorBackground)
        self.paintTime(screen)
        self.paintLocation(screen, location=self.locations[self.currentLocation])
        pass

    def paintTime(self, screen):
        text = self.fontTime.render("{}".format(time.ctime()), True, self.colorText)
        screen.blit(text, App.coordsTime)
        pass

    def paintLocation(self, screen, location):
        layout = self.currentLocation % 2

        # Write Title
        textTitle = self.fontHeader.render("{}".format(location.name), True, self.colorText)
        screen.blit(textTitle, App.coordsHeader)

        # Write Currently
        textCurrently = self.fontInfo.render("Currently {}".format(location.weatherKind), True, self.colorText)
        screen.blit(textCurrently, App.coordsCurrently)

        # Draw Icon
        self.paintWeatherIcon(screen)

        # Write Temperature
        textTemperature = self.fontTemperature.render("{}°F".format(location.temperature), True, self.colorTempText)
        screen.blit(textTemperature, App.coordsTemp)

        # Write Humidity
        textHumidity = self.fontInfo.render("{}% Humidity".format(location.humidity), True, self.colorText)
        screen.blit(textHumidity, App.coordsHumidity)

        # Write Wind
        textWind = self.fontInfo.render("{} MPH".format(location.windSpeed, location.windDir), True, self.colorText)
        screen.blit(textWind, App.coordsWind)

        # Draw Precipitation
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.RAIN_SMALL], App.coordsPrecip)
        textPrecipitation = self.fontInfo.render("{:d}\"".format(int(location.precipitation/100)), True, self.colorText)
        screen.blit(textPrecipitation, App.coordsPrecipText)

        # Draw Sunrise
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.SUNRISE], App.coordsSunrise)
        text = "{rise:}".format(rise=location.sunrise)
        textSunrise = self.fontInfo.render(text[:5], True, self.colorText)
        screen.blit(textSunrise, App.coordsSunriseText)

        # Draw Sunset
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.SUNSET], App.coordsSunset)
        text = "{set:}".format(set=location.sunset)
        textSunset = self.fontInfo.render(text[:5], True, self.colorText)
        screen.blit(textSunset, App.coordsSunsetText)

        # Draw Climbing Index
        self.paintTodaysClimbingIndex(screen, location)

        # Draw Image
        screen.blit(location.image, App.coordsImage)
        pass

    def paintWeatherIcon(self, screen):
        weather = self.locations[self.currentLocation].weatherKind
        icon = WeatherIcon.imgWeatherIcon[WeatherIcon.UNKNOWN]

        if weather == enums.Kind.SUNNY:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.SUNNY]
        elif weather == enums.Kind.PARTLY_CLOUDY:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.PARTLY_CLOUDY]
        elif weather == enums.Kind.CLOUDY or weather == enums.Kind.FOG:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.CLOUDY]
        elif weather == enums.Kind.VERY_CLOUDY:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.VERY_CLOUDY]
        elif weather == enums.Kind.LIGHT_SHOWERS:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.LIGHT_SHOWERS]
        elif weather == enums.Kind.LIGHT_SLEET or weather == enums.Kind.LIGHT_SLEET_SHOWERS:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.SNOWY]
        elif weather == enums.Kind.THUNDERY_SHOWERS:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.THUNDERY_SHOWERS]
        elif weather == enums.Kind.LIGHT_SNOW or weather == enums.Kind.HEAVY_SNOW:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.SNOWY]
        elif weather == enums.Kind.LIGHT_RAIN:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.LIGHT_RAIN]
        elif weather == enums.Kind.HEAVY_SHOWERS or weather == enums.Kind.HEAVY_RAIN:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.HEAVY_RAIN]
        elif weather == enums.Kind.LIGHT_SNOW_SHOWERS or weather == enums.Kind.HEAVY_SNOW_SHOWERS:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.MIX]
        elif weather == enums.Kind.THUNDERY_HEAVY_RAIN or weather == enums.Kind.THUNDERY_SNOW_SHOWERS:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.THUNDERSTORMS]

        screen.blit(icon, App.coordsIcon)
        pass

    def paintTodaysClimbingIndex(self, screen, location):
        climbIndex = .01 * location.climbingIndex
        climbIndex255 = climbIndex * 255

        red = 255 - climbIndex255
        green = climbIndex255

        colorClimbIndex = (red, green, 0)
        black = (0, 0, 0)
        height = (1 - climbIndex) * App.sizeClimbIndex[1]
        y = App.coordsClimbIndex[1] + height
        rect = (App.coordsClimbIndex[0], y, App.sizeClimbIndex[0], App.sizeClimbIndex[1] - height)
        thickness = 10
        rectBorder = (rect[0]-thickness, App.coordsClimbIndex[1]-thickness, App.sizeClimbIndex[0]+615+2*thickness, App.sizeClimbIndex[1]+2*thickness)
        pygame.draw.rect(screen, color=black, rect=rectBorder)
        pygame.draw.rect(screen, color=colorClimbIndex, rect=rect)

        # Draw Climber Icon
        screen.blit(WeatherIcon.imgClimberIcon, (App.coordsClimbIndex[0], y))

        # text = self.fontTime.render("   Climbing Index: {CI:d}".format(CI=int(location.climbingIndex)), True, self.colorText)
        # screen.blit(text, App.coordsClimbIndex)
        pass




class Location:
    WILLOW_RIVER = 0
    SANDSTONE = 1
    RED_WING = 2
    RAINY_LAKE = 3
    DEVILS_LAKE = 4
    RED_ROCK_CANYON = 5
    EL_POTRERO_CHICO = 6
    FRANKENJURA = 7
    NUM_LOCATIONS = 8

    imgSize = (600, 900)
    imgWillow_1 = pygame.transform.scale(pygame.image.load('Data/WillowRiver_1.JPG'), imgSize)
    imgSandstone_1 = pygame.transform.scale(pygame.image.load('Data/Sandstone.JPG'), imgSize)
    imgRedWing_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Data/RedWing_1.JPG'), 90), imgSize)
    imgRainyLake_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Data/RainyLake_1.jpg'), -90), imgSize)
    imgDevilsLake_1 = pygame.transform.scale(pygame.image.load('Data/DevilsLake.jpg'), imgSize)
    imgRedRocks_1 = pygame.transform.scale(pygame.image.load('Data/RedRocks_1.jpg'), imgSize)
    imgElPotreroChico_1 = pygame.transform.scale(pygame.image.load('Data/ElPotreroChico.jpg'), imgSize)
    imgFrankenjura_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Data/Frankenjura_1.jpg'), -90), imgSize)


    def __init__(self, name, weatherLocation, image):
        self.name = name
        self.weatherLocation = weatherLocation
        self.image = image
        self.temperature = 999
        self.humidity = 999
        self.windSpeed = 999
        self.windDir = "NA"
        self.precipitation = 999
        self.sunrise = "NA"
        self.sunset = "NA"
        self.weatherKind = "NA"
        self.forecast = 0
        self.today = 0
        self.tomorrow = 0
        self.ubermorgen = 0

        self.climbingIndex = 0

        # self.updateWeather()
        pass

    def calculateClimbingIndex(self):

        temperatureScore = self.calculateTemperatureScore()

        humidityScore = self.calculateHumidityScore()

        windScore = self.calculateWindScore()

        self.climbingIndex = (.50 * temperatureScore) + (.35 * humidityScore) + (.15 * windScore)

        if self.weatherKind == enums.Kind.SUNNY:
            self.climbingIndex += 2
        elif self.weatherKind == enums.Kind.PARTLY_CLOUDY:
            self.climbingIndex += 4
        elif self.weatherKind == enums.Kind.CLOUDY:
            self.climbingIndex += 3
        elif self.weatherKind == enums.Kind.VERY_CLOUDY:
            self.climbingIndex += 3

        self.climbingIndex = self.climbingIndex - self.precipitation

        # Validation
        if self.climbingIndex < 0:
            self.climbingIndex = 0
        if self.climbingIndex > 100:
            self.climbingIndex = 100

        pass

    def calculateTemperatureScore(self):
        x = self.temperature
        temperatureScore = 0

        # Formulas derived from interpolation
        if self.temperature < 45:
            temperatureScore = 2.8333 * x - 42.5
        elif self.temperature < 55:
            temperatureScore = -0.133333*math.pow(x, 2) + 14.833*x - 312.5
        else:
            temperatureScore = -0.0326*math.pow(x, 2) + 3.7527*x - 7.7819

        # Remain within 0 - 100 bounds
        if temperatureScore < 0:
            temperatureScore = 0
        if temperatureScore > 100:
            temperatureScore = 100

        return temperatureScore

    def calculateHumidityScore(self):
        x = self.humidity

        # Derive our polynomial from interpolation
        humidityScore =     -0.000018353 * math.pow(x, 4)
        humidityScore +=     0.0040823 * math.pow(x, 3)
        humidityScore +=    -0.31230 * math.pow(x, 2)
        humidityScore +=     8.5099 * x
        humidityScore +=     25

        if humidityScore < 0:
            humidityScore = 0
        if humidityScore > 100:
            humidityScore = 100

        return humidityScore

    def calculateWindScore(self):
        windScore = 100 - (5 * math.fabs(20 - self.windSpeed))
        if windScore < 0:
            windScore = 0
        if windScore > 100:
            windScore = 100

        return windScore

    def updateWeather(self):
        try:
            asyncio.run(self.updateWeatherAsync())
        except client_exceptions.ClientConnectorError:
            print("Connection Error")
        self.calculateClimbingIndex()
        pass

    async def updateWeatherAsync(self):
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get(self.weatherLocation)
            self.temperature = weather.current.temperature
            self.humidity = weather.current.humidity
            self.windSpeed = weather.current.wind_speed
            self.windDir = weather.current.wind_direction
            self.precipitation = 100 * weather.current.precipitation
            self.weatherKind = weather.current.kind
            self.forecast = iter(weather.forecasts)
            self.today = next(self.forecast)
            self.tomorrow = next(self.forecast)
            self.ubermorgen = next(self.forecast)
            self.sunrise = self.today.astronomy.sun_rise
            self.sunset  = self.today.astronomy.sun_set

            # print(self.today)
            # print(self.tomorrow)
            # print(self.ubermorgen)



class WeatherIcon:
    iconSize = 250
    imgWeatherIcon = \
        [
            pygame.transform.scale(pygame.image.load('Data/Weather/Sunny.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/Cloudy.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/LightRain.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/HeavyRain.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/PartlyCloudy.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/Snowy.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/Thunderstorms.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/ThunderyShowers.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/VeryCloudy.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/Unknown.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/LightShowers.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/Mix.png'), (iconSize, iconSize)),
            pygame.transform.scale(pygame.image.load('Data/Weather/Sunrise.png'), (100, 100)),
            pygame.transform.scale(pygame.image.load('Data/Weather/Sunset.png'), (100, 100)),
            pygame.transform.scale(pygame.image.load('Data/Weather/LightRain.png'), (100, 100))
        ]
    imgClimberIcon = pygame.transform.scale(pygame.image.load('Data/climberIcon.png'), (72, 72))

    SUNNY = 0
    CLOUDY = 1
    LIGHT_RAIN = 2
    HEAVY_RAIN = 3
    PARTLY_CLOUDY = 4
    SNOWY = 5
    THUNDERSTORMS = 6
    THUNDERY_SHOWERS = 7
    VERY_CLOUDY = 8
    UNKNOWN = 9
    LIGHT_SHOWERS = 10
    MIX = 11
    SUNRISE = 12
    SUNSET = 13
    RAIN_SMALL = 14
    NUM_WEATHER_ICONS = 15

