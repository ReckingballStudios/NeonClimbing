# Application File


import pygame
import python_weather
from python_weather import enums
import asyncio
import os
import time




class App:

    # Coordinates
    coordsHeader    = (110,     10)
    coordsTime      = (1460,    5)
    coordsImage     = (1280,    150)
    coordsCurrently = (coordsHeader[0] + 185,     185)
    coordsIcon      = (75,      220)
    coordsTemp      = (coordsIcon[0] + 250,           coordsIcon[1]+25)
    coordsHumidity  = (coordsTemp[0] + 440,     coordsTemp[1] + 30)
    coordsWind      = (coordsTemp[0] + 440,     coordsTemp[1] + 100)
    coordsPrecip    = (coordsIcon[0] + 35,   coordsTemp[1] + 200)
    coordsPrecipText = (coordsPrecip[0] + 100,   coordsPrecip[1] + 15)
    coordsSunrise   = (coordsPrecip[0] + 360, coordsPrecip[1])
    coordsSunriseText = (coordsSunrise[0] + 110, coordsSunrise[1] + 15)
    coordsSunset    = (coordsSunrise[0] + 400, coordsPrecip[1])
    coordsSunsetText = (coordsSunset[0] + 110, coordsSunset[1] + 15)

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
        self.locations.append(Location(Location.WILLOW_RIVER,    "Willow River", "Hudson, WI", Location.imgWillow_1))
        self.locations.append(Location(Location.SANDSTONE,       "Sandstone", "Sandstone, MN", Location.imgSandstone_1))
        self.locations.append(Location(Location.RED_WING,        "Red Wing", "Red Wing, MN", Location.imgRedWing_1))
        self.locations.append(Location(Location.RAINY_LAKE,      "Rainy Lake", "International Falls, MN", Location.imgRainyLake_1))
        self.locations.append(Location(Location.DEVILS_LAKE,     "Devil's Lake", "Baraboo, WI", Location.imgDevilsLake_1))
        self.locations.append(Location(Location.EL_POTRERO_CHICO, "El Potrero Chico", "Hidalgo, NL, MX", Location.imgElPotreroChico_1))
        self.locations.append(Location(Location.FRANKENJURA,     "Frankenjura", "Regensburg, DE", Location.imgFrankenjura_1))
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
            for i in range(Location.NUM_LOCATIONS):
                self.locations[i].updateWeather()
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
        textCurrently = self.fontInfo.render("Currently {}".format(location.description), True, self.colorText)
        screen.blit(textCurrently, App.coordsCurrently)

        # Draw Icon
        self.drawWeatherIcon(screen)

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
        textPrecipitation = self.fontInfo.render("{}%".format(location.precipitation), True, self.colorText)
        screen.blit(textPrecipitation, App.coordsPrecipText)

        # Draw Sunrise
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.SUNRISE], App.coordsSunrise)
        textSunrise = self.fontInfo.render("{}".format(location.sunrise), True, self.colorText)
        screen.blit(textSunrise, App.coordsSunriseText)

        # Draw Sunset
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.SUNSET], App.coordsSunset)
        textSunset = self.fontInfo.render("{}".format(location.sunset), True, self.colorText)
        screen.blit(textSunset, App.coordsSunsetText)

        # Draw Image
        screen.blit(location.image, App.coordsImage)
        pass

    def drawWeatherIcon(self, screen):
        weather = self.locations[self.currentLocation].description
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



class Location:
    WILLOW_RIVER = 0
    SANDSTONE = 1
    RED_WING = 2
    RAINY_LAKE = 3
    DEVILS_LAKE = 4
    EL_POTRERO_CHICO = 5
    FRANKENJURA = 6
    NUM_LOCATIONS = 7

    imgWillow_1 = pygame.transform.scale(pygame.image.load('Data/WillowRiver_1.JPG'), (600, 900))
    imgSandstone_1 = pygame.transform.scale(pygame.image.load('Data/Sandstone.JPG'), (600, 900))
    imgRedWing_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Data/RedWing_1.JPG'), 90), (600, 900))
    imgRainyLake_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Data/RainyLake_1.jpg'), -90), (600, 900))
    imgDevilsLake_1 = pygame.transform.scale(pygame.image.load('Data/DevilsLake.jpg'), (600, 900))
    imgElPotreroChico_1 = pygame.transform.scale(pygame.image.load('Data/ElPotreroChico.jpg'), (600, 900))
    imgFrankenjura_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Data/Frankenjura_1.jpg'), -90), (600, 900))


    def __init__(self, index, name, weatherLocation, image):
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
        self.description = "NA"
        self.forecast = 0
        self.today = 0
        # self.updateWeather()
        pass

    def updateWeather(self):
        asyncio.run(self.updateWeatherAsync())
        pass

    async def updateWeatherAsync(self):
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get(self.weatherLocation)
            self.temperature = weather.current.temperature
            self.humidity = weather.current.humidity
            self.windSpeed = weather.current.wind_speed
            self.windDir = weather.current.wind_direction
            self.precipitation = weather.current.precipitation
            self.description = weather.current.kind
            self.forecast = iter(weather.forecasts)
            self.today = next(self.forecast)
            self.sunrise = self.today.astronomy.sun_rise
            self.sunset  = self.today.astronomy.sun_set



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

