# Application File
import json.decoder

import pygame
import python_weather
from datetime import datetime
from python_weather import enums
import asyncio
from aiohttp import client_exceptions
import time
import math



class App:

    # Coordinates               X-Coordinate                    Y-Coordinate
    coordsHeader            = (110,                             20)
    coordsTime              = (1460,                            5)
    coordsUpdating          = (coordsTime[0] - 80,              coordsTime[1] + 60)
    coordsImage             = (1280,                            150)
    coordsClimbIndex        = (coordsImage[0] - 80,             coordsImage[1])

    coordsCurrently         = (coordsHeader[0] + 185,           195)
    coordsIcon              = (25,                              coordsCurrently[1])
    coordsTemp              = (coordsIcon[0] + 255,             coordsIcon[1])
    coordsHiLo              = (coordsTemp[0] + 480,             coordsTemp[1] + 35)
    coordsDewPoint          = (coordsHiLo[0],                   coordsHiLo[1] + 65)
    coordsWind              = (coordsHiLo[0],                   coordsDewPoint[1] + 65)
    coordsPrecip            = (coordsIcon[0] + 200,             coordsTemp[1] + 250)
    coordsPrecipText        = (coordsPrecip[0] + 100,           coordsPrecip[1] + 18)
    coordsSunrise           = (coordsPrecip[0] + 280,           coordsPrecip[1])
    coordsSunriseText       = (coordsSunrise[0] + 110,          coordsSunrise[1] + 18)
    coordsSunset            = (coordsSunrise[0] + 340,          coordsPrecip[1])
    coordsSunsetText        = (coordsSunset[0] + 110,           coordsSunset[1] + 18)

    # Future Forecast Coords
    coordsTomorrow          = (coordsIcon[0] + 225,             coordsIcon[1] + 400)
    coordsUbermorgen        = (coordsTomorrow[0] + 525,         coordsTomorrow[1])
    coordsTomorrowIcon      = (coordsTomorrow[0] - 100,         coordsTomorrow[1] + 50)
    coordsUbermorgenIcon    = (coordsUbermorgen[0] - 100,       coordsUbermorgen[1] + 50)
    coordsTomorrowTemp      = (coordsTomorrow[0] - 135,         coordsTomorrow[1] + 270)
    coordsUbermorgenTemp    = (coordsUbermorgen[0] - 135,       coordsUbermorgen[1] + 270)
    coordsTomorrowPrecip    = (coordsTomorrowIcon[0] + 260,     coordsTomorrowIcon[1] + 20)
    coordsUbermorgenPrecip  = (coordsUbermorgenIcon[0] + 260,   coordsUbermorgenIcon[1] + 30)


    sizeClimbIndex = (72, 900)

    weatherUpdateFrequency = 3600   # 3600 = 1 hour
    iterateScreenFrequency = 60     # 60 = 1 minute

    # Initialize
    def __init__(self):

        # Font and Text initialization
        self.fontTemperature = pygame.font.SysFont  ('timesnewroman', int(230))
        self.fontTempSmall = pygame.font.SysFont    ('timesnewroman', int(90))
        self.fontHeader = pygame.font.SysFont       ('timesnewroman', int(140))
        self.fontCurrently = pygame.font.SysFont    ('timesnewroman', int(80))
        self.fontInfo = pygame.font.SysFont         ('timesnewroman', int(55))
        self.fontTime = pygame.font.SysFont         ('timesnewroman', int(40))
        #
        # self.fontTemperature = pygame.font.SysFont  ('arial', int(230))
        # self.fontTempSmall = pygame.font.SysFont    ('arial', int(90))
        # self.fontHeader = pygame.font.SysFont       ('arial', int(140))
        # self.fontCurrently = pygame.font.SysFont    ('arial', int(80))
        # self.fontInfo = pygame.font.SysFont         ('arial', int(55))
        # self.fontTime = pygame.font.SysFont         ('arial', int(40))

        # self.fontTemperature = pygame.font.SysFont  ('gotham', int(290  ))
        # self.fontTempSmall = pygame.font.SysFont    ('gotham', int(115   ))
        # self.fontHeader = pygame.font.SysFont       ('gotham', int(175  ))
        # self.fontCurrently = pygame.font.SysFont    ('gotham', int(100   ))
        # self.fontInfo = pygame.font.SysFont         ('gotham', int(75   ))
        # self.fontTime = pygame.font.SysFont         ('gotham', int(50   ))

        self.colorText = (235, 235, 235)
        self.colorTempText = (255, 255, 255)
        self.colorBackground = (25, 25, 25)
        self.colorBackground2 = (12, 12, 12)

        # App Conditions
        self.updatingWeather = False

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
        self.locations.append(Location("Taylors Falls", "Taylors Falls, MN", Location.imgTaylorsFalls_1))
        self.locations.append(Location("Rainy Lake", "International Falls, MN", Location.imgRainyLake_1))
        self.locations.append(Location("Devil's Lake", "Baraboo, WI", Location.imgDevilsLake_1))
        self.locations.append(Location("Red Rocks Canyon", "Las Vegas, NV", Location.imgRedRocks_1))
        self.locations.append(Location("El Potrero Chico", "Hidalgo, NL, MX", Location.imgElPotreroChico_1))
        self.locations.append(Location("Frankenjura", "Regensburg, DE", Location.imgFrankenjura_1))
        pass


    # Handle Mouse / Touch Inputs from user
    def handleMouse(self, event):
        touchX = pygame.mouse.get_pos()[0]

        if event.type == pygame.MOUSEBUTTONUP and touchX < 960:
            self.decrementLocation()
        elif event.type == pygame.MOUSEBUTTONUP and touchX >= 960:
            self.iterateLocation()
        pass

    def decrementLocation(self):
        # Go to the previous location
        self.currentLocation -= 1
        if self.currentLocation < 0:
            self.currentLocation = Location.NUM_LOCATIONS - 1

        # self.locations[self.currentLocation].updateWeather()
        self.iterateTimer = time.time()
        pass

    def iterateLocation(self):
        # Go to the next location
        self.currentLocation += 1
        if self.currentLocation >= Location.NUM_LOCATIONS:
            self.currentLocation = 0

        # self.locations[self.currentLocation].updateWeather()
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

        # Timer has expired, therefore update weather
        if self.updatingWeather:
            self.weatherTimer = time.time()
            for i in range(Location.NUM_LOCATIONS):
                 self.locations[i].updateWeather()
            self.updatingWeather = False


        # We want one frame to paint that it is updating weather
        if deltaTime > self.weatherUpdateFrequency:
            self.updatingWeather = True
        pass


    def paint(self, screen):
        screen.fill(self.colorBackground)
        self.paintTime(screen)
        self.paintLocation(screen, location=self.locations[self.currentLocation])

        if self.updatingWeather:
            self.paintUpdatingWeather(screen)
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
        textCurrently = self.fontCurrently.render("Currently {}".format(location.weatherKind), True, self.colorText)
        # screen.blit(textCurrently, App.coordsCurrently)

        # Draw Icon
        self.paintWeatherIcon(screen, self.locations[self.currentLocation].weatherKind, App.coordsIcon)

        # Write Temperature
        textTemperature = self.fontTemperature.render("{}°F".format(location.temperature), True, self.colorTempText)
        if location.temperature >= 100 or location.temperature <= -10:
            textTemperature = self.fontTemperature.render("{}°".format(location.temperature), True, self.colorTempText)

        screen.blit(textTemperature, App.coordsTemp)

        # Write Humidity
        textHighLow = self.fontInfo.render("{}°F | {}°F".format(location.high, location.low), True, self.colorText)
        screen.blit(textHighLow, App.coordsHiLo)

        # Write Dew Point
        textDewPoint = self.fontInfo.render("{}°F Dew Point".format(location.dewPoint), True, self.colorText)
        screen.blit(textDewPoint, App.coordsDewPoint)

        # Write Wind
        textWind = self.fontInfo.render("{} MPH {}".format(location.windSpeed, location.windDir), True, self.colorText)
        screen.blit(textWind, App.coordsWind)

        # Draw Precipitation
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.RAIN_SMALL], App.coordsPrecip)
        textPrecipitation = self.fontInfo.render("{:d}%".format(int(location.chanceOfRain)), True, self.colorText)
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

        self.paintFutureForecast(screen, location)
        pass

    def paintFutureForecast(self, screen, location):
        # Draw Background
        tomLoc = App.coordsTomorrow
        rectBorder = (tomLoc[0]-165, tomLoc[1]-5, 1050, 415)
        pygame.draw.rect(screen, self.colorBackground2, rectBorder)

        # Draw Tomorrow
        tomorrowDayOfWeek = App.weekdayFromDate(location.tomorrow["date"])
        text = self.fontInfo.render("{dow:}".format(dow=tomorrowDayOfWeek), True, self.colorText)
        screen.blit(text, App.coordsTomorrow)

        # Draw Tomorrows Weather Icon
        self.paintWeatherIcon(screen, int(location.tomorrow["hourly"][5]["weatherCode"]), App.coordsTomorrowIcon)

        # Draw Tomorrows High
        string = "{hi:}°F | {low:}°F".format(hi=location.tomorrow["maxtempF"], low=location.tomorrow["mintempF"])
        text = self.fontTempSmall.render(string, True, self.colorText)
        screen.blit(text, App.coordsTomorrowTemp)

        # Draw Tomorrows Precipitation Chance
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.RAIN_SMALL], App.coordsTomorrowPrecip)
        precipitationChance = location.tomorrowChanceOfRain
        text = self.fontInfo.render("{chance:d}%".format(chance=int(precipitationChance)), True, self.colorText)
        screen.blit(text, (App.coordsTomorrowPrecip[0]+15, App.coordsTomorrowPrecip[1]+90))

        # Draw Ubermorgen
        ubermorgenDayOfWeek = App.weekdayFromDate(location.ubermorgen["date"])
        text = self.fontInfo.render("{}".format(ubermorgenDayOfWeek), True, self.colorText)
        screen.blit(text, App.coordsUbermorgen)

        # Draw Ubermorgens Weather Icon
        self.paintWeatherIcon(screen, int(location.ubermorgen["hourly"][5]["weatherCode"]), App.coordsUbermorgenIcon)

        # Draw Ubermorgens High
        string = "{hi:}°F | {low:}°F".format(hi=location.ubermorgen["maxtempF"], low=location.ubermorgen["mintempF"])
        text = self.fontTempSmall.render(string, True, self.colorText)
        screen.blit(text, App.coordsUbermorgenTemp)

        # Draw Tomorrows Precipitation Chance
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.RAIN_SMALL], App.coordsUbermorgenPrecip)
        precipitationChance = location.ubermorgenChanceOfRain
        text = self.fontInfo.render("{chance:}%".format(chance=int(precipitationChance)), True, self.colorText)
        screen.blit(text, (App.coordsUbermorgenPrecip[0] + 15, App.coordsUbermorgenPrecip[1] + 90))
        pass

    def paintWeatherIcon(self, screen, weather, coords):
        icon = WeatherIcon.imgWeatherIcon[WeatherIcon.UNKNOWN]

        if weather == enums.Kind.SUNNY.value:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.SUNNY]
        elif weather == enums.Kind.PARTLY_CLOUDY.value:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.PARTLY_CLOUDY]
        elif weather == enums.Kind.CLOUDY.value or weather == enums.Kind.FOG.value or weather in [248, 260]:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.CLOUDY]
        elif weather == enums.Kind.VERY_CLOUDY.value:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.VERY_CLOUDY]
        elif weather == enums.Kind.LIGHT_SHOWERS.value or weather in [353]:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.LIGHT_SHOWERS]
        elif weather == enums.Kind.LIGHT_SLEET.value or weather == enums.Kind.LIGHT_SLEET_SHOWERS.value:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.SNOWY]
        elif weather == enums.Kind.THUNDERY_SHOWERS.value or weather in [200, 386, 389, 392, 395]:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.THUNDERY_SHOWERS]
        elif weather == enums.Kind.LIGHT_SNOW.value or weather == enums.Kind.HEAVY_SNOW.value or weather in [227, 230, 323, 326, 329, 332, 335, 338]:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.SNOWY]
        elif weather == enums.Kind.LIGHT_RAIN.value or weather in [263, 266, 293, 296]:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.LIGHT_RAIN]
        elif weather == enums.Kind.HEAVY_SHOWERS.value or weather == enums.Kind.HEAVY_RAIN.value or weather in [299, 302, 305, 308]:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.HEAVY_RAIN]
        elif weather == enums.Kind.LIGHT_SNOW_SHOWERS.value or weather == enums.Kind.HEAVY_SNOW_SHOWERS.value:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.MIX]
        elif weather == enums.Kind.THUNDERY_HEAVY_RAIN.value or weather == enums.Kind.THUNDERY_SNOW_SHOWERS.value:
            icon = WeatherIcon.imgWeatherIcon[WeatherIcon.THUNDERSTORMS]
        else:
            print(f"Weather Icon Code Invalid: {weather}")

        screen.blit(icon, coords)
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
        pygame.draw.rect(screen, self.colorBackground2, rectBorder)
        pygame.draw.rect(screen, colorClimbIndex, rect)

        # Draw Climber Icon
        screen.blit(WeatherIcon.imgClimberIcon, (App.coordsClimbIndex[0], y))

        # text = self.fontTime.render("   Climbing Index: {CI:d}".format(CI=int(location.climbingIndex)), True, self.colorText)
        # screen.blit(text, App.coordsClimbIndex)
        pass

    def paintUpdatingWeather(self, screen):
        text = self.fontTime.render("Updating Weather : Please Wait", True, self.colorText)
        screen.blit(text, App.coordsUpdating)

        screen.blit(WeatherIcon.imgUpdatingIcon, (App.coordsUpdating[0] - 100, App.coordsUpdating[1] - 20))
        pass

    @staticmethod
    def weekdayFromDate(date):

        dateObject = datetime.strptime(date, "%Y-%m-%d")

        dayName = dateObject.strftime("%a")

        return dayName

    @staticmethod
    def calculateDewPoint(temperature, humidity):

        # Assure the natural log is not undefined
        if humidity < 1:
            humidity = 1

        temperatureCelsius = (temperature - 32) * 5 / 9

        # Magnus-Tetens formula
        MAGNUS_A = 17.27
        MAGNUS_B = 237.7

        # Derive the intermediate variable
        alpha = ((MAGNUS_A * temperatureCelsius) / (MAGNUS_B + temperatureCelsius) + math.log(humidity / 100.0))

        # Calculate the Dew Point
        dewPointCelsius = (MAGNUS_B * alpha) / (MAGNUS_A - alpha)


        dewPointFahrenheit = (dewPointCelsius * 9 / 5) + 32
        return int(dewPointFahrenheit)

    @staticmethod
    def calculateChanceOfRain(weatherFromThatDay):
        highestChance = 0

        # starting at index 3 (6am) ending at index 7 (9pm)
        for i in range(3, 7):
            chance = int(weatherFromThatDay["hourly"][i]["chanceofrain"])
            if chance > highestChance:
                highestChance = chance

        return highestChance

class Location:
    i = 0
    WILLOW_RIVER = i
    i += 1
    SANDSTONE = i
    i += 1
    RED_WING = i
    i += 1
    TAYLORS_FALLS = i
    i += 1
    RAINY_LAKE = i
    i += 1
    DEVILS_LAKE = i
    i += 1
    RED_ROCK_CANYON = i
    i += 1
    EL_POTRERO_CHICO = i
    i += 1
    FRANKENJURA = i
    i += 1
    NUM_LOCATIONS = i


    imgSize = (600, 900)
    imgWillow_1 = pygame.transform.scale(pygame.image.load('Data/WillowRiver_1.JPG'), imgSize)
    imgSandstone_1 = pygame.transform.scale(pygame.image.load('Data/Sandstone.JPG'), imgSize)
    imgRedWing_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Data/RedWing_1.JPG'), 90), imgSize)
    imgRainyLake_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Data/RainyLake_1.jpg'), -90), imgSize)
    imgDevilsLake_1 = pygame.transform.scale(pygame.image.load('Data/DevilsLake.jpg'), imgSize)
    imgRedRocks_1 = pygame.transform.scale(pygame.image.load('Data/RedRocks_1.jpg'), imgSize)
    imgElPotreroChico_1 = pygame.transform.scale(pygame.image.load('Data/ElPotreroChico.jpg'), imgSize)
    imgFrankenjura_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Data/Frankenjura_1.jpg'), -90), imgSize)
    imgTaylorsFalls_1 = pygame.transform.scale(pygame.image.load('Data/TaylorsFalls.png'), imgSize)


    def __init__(self, name, weatherLocation, image):

        # Initialized from parameters
        self.name = name
        self.weatherLocation = weatherLocation
        self.image = image

        # Initialized from the update weather function
        self.temperature = 999
        self.high = 999
        self.low = 999
        self.humidity = 999
        self.dewPoint = 999
        self.windSpeed = 999
        self.windDir = "NA"
        self.precipitation = 999
        self.chanceOfRain = 999
        self.sunrise = "NA"
        self.sunset = "NA"
        self.weatherKind = 999
        self.forecast = 0
        self.today = 0
        self.tomorrow = 0
        self.ubermorgen = 0
        self.tomorrowChanceOfRain = 0
        self.ubermorgenChanceOfRain = 0

        # Derived from the Climbing Index Algorithm
        self.climbingIndex = 0

        self.updateWeather()


        pass

    def calculateClimbingIndex(self):

        temperatureScore = self.calculateTemperatureScore()

        humidityScore = self.calculateHumidityScore()

        dewPointScore = self.calculateDewPointScore()

        windScore = self.calculateWindScore()

        self.climbingIndex = (.45 * temperatureScore) + (.20 * humidityScore) + (.20 * dewPointScore) + (.15 * windScore)

        if self.weatherKind == enums.Kind.SUNNY.value:
            self.climbingIndex += 5
        elif self.weatherKind == enums.Kind.PARTLY_CLOUDY.value:
            self.climbingIndex += 7
        elif self.weatherKind == enums.Kind.CLOUDY.value:
            self.climbingIndex += 6
        elif self.weatherKind == enums.Kind.VERY_CLOUDY.value:
            self.climbingIndex += 5

        # General boost to the Climbing Index score
        self.climbingIndex += 5

        # If you found this then you got me. I'm biased, what can I say
        if self.name == "Willow River":
            self.climbingIndex += 2

        # We don't like rain
        self.climbingIndex = self.climbingIndex - self.chanceOfRain

        # Validation, 8 is lowest so picture still displays, and bar is visible
        if self.climbingIndex < 8:
            self.climbingIndex = 8
        if self.climbingIndex > 100:
            self.climbingIndex = 100

        pass

    def calculateTemperatureScore(self):
        if self.temperature < 0 or self.temperature > 100:
            return -100

        x = self.temperature

        # Formula derived from interpolation
        # temperatureScore  =   1.5873 * math.pow(10, -9) * math.pow(x, 7)
        # temperatureScore +=  -7.8968 * math.pow(10, -7) * math.pow(x, 6)
        # temperatureScore +=   1.6052 * math.pow(10, -4) * math.pow(x, 5)
        # temperatureScore +=  -1.7224 * math.pow(10, -2) * math.pow(x, 4)
        # temperatureScore +=   1.0485 * math.pow(10,  0) * math.pow(x, 3)
        # temperatureScore +=  -3.6070 * math.pow(10,  1) * math.pow(x, 2)
        # temperatureScore +=   6.5155 * math.pow(10,  2) * math.pow(x, 1)
        # temperatureScore +=  -4.8000 * math.pow(10,  3)

        # Horner's Method for the interpolated polynomial function
        temperatureScore = int(
                ((((((1.587301587301587301587301587301587301587301587301587301508619546e-9 * x
                      - 7.89682539682539682539682539682539682539682539682539682507312352e-7) * x
                     + 1.605158730158730158730158730158730158730158730158730158675234314e-4) * x
                    - 1.722420634920634920634920634920634920634920634920634920585300265e-2) * x
                   + 1.048456349206349206349206349206349206349206349206349206323544646) * x
                  - 36.06968253968253968253968253968253968253968253968253968178346568) * x
                 + 651.5476190476190476190476190476190476190476190476190476073392221) * x
                - 4800.0
        )

        # print("temp: {}, score: {}".format(x, temperatureScore))

        # Remain within -100 | +100 bounds
        if temperatureScore < -100:
            temperatureScore = -100
        if temperatureScore > 100:
            temperatureScore = 100

        return temperatureScore

    def calculateHumidityScore(self):
        x = self.humidity

        # Derive our polynomial from interpolation
        # humidityScore =     -0.000018353 * math.pow(x, 4)
        # humidityScore +=     0.0040823 * math.pow(x, 3)
        # humidityScore +=    -0.31230 * math.pow(x, 2)
        # humidityScore +=     8.5099 * x
        # humidityScore +=     25

        # Horner's Method for our Polynomial Interpolation
        humidityScore = int(
                (((-0.000018353 * x
                   + 0.0040823) * x
                  - 0.31230) * x
                 + 8.5099) * x
                + 25
        )

        if humidityScore < 0:
            humidityScore = 0
        if humidityScore > 100:
            humidityScore = 100

        # print("Humidity {}: {}".format(x, humidityScore))

        return humidityScore

    def calculateDewPointScore(self):
        dewPoint = self.dewPoint
        x = dewPoint

        # Our Polynomial Function derived from interpolation
        dewPointScore = int(
                (-0.08236208236208236 * x
                 + 6.674436674436674) * x
                - 33.566433566433566
        )

        if dewPointScore < 0:
            dewPointScore = 0
        if dewPointScore > 100:
            dewPointScore = 100

        # print("Dew Point {}: {}".format(x, dewPointScore))

        return dewPointScore

    def calculateWindScore(self):
        x = self.windSpeed
        windScore = int(((-0.006393298059964714 * x - 0.31172839506172894) * x + 6.781084656084661) * x + 69)

        if windScore < 0:
            windScore = 0
        if windScore > 100:
            windScore = 100

        # print("Wind Speed {}: {}".format(x, windScore))

        return windScore

    def updateWeather(self):
        try:
            asyncio.run(self.updateWeatherAsync())
        except client_exceptions.ClientConnectorError:
            print("Updating Weather Connection Error")
        except client_exceptions.ClientOSError:
            print("Updating Weather OS Error")
        except client_exceptions.ClientError as e:
            print(f"Updating Weather Client Error: {e}")
        except json.decoder.JSONDecodeError:
            print("Updating Weather JSON Error")
        except RuntimeError:
            print("Updating Weather Runtime Error")
        except TimeoutError:
            print("Updating Weather Timeout Error")


        try:
            self.calculateClimbingIndex()
        except AttributeError:
            print("Attribute Error")

        pass

    async def updateWeatherAsync(self):

        from urllib.parse import quote
        import aiohttp

        location = quote(self.weatherLocation)
        url = f"https://wttr.in/{location}?format=j1"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                weather = await response.json(content_type=None)

                self.forecast       = weather["weather"]

                self.today          = weather["weather"][0]
                self.tomorrow       = weather["weather"][1]
                self.ubermorgen     = weather["weather"][2]

                self.temperature    = int(weather["current_condition"][0]["temp_F"])
                self.high           = int(self.today["maxtempF"])
                self.low            = int(self.today["mintempF"])
                self.humidity       = int(weather["current_condition"][0]["humidity"])
                self.dewPoint       = App.calculateDewPoint(self.temperature, self.humidity)
                self.windSpeed      = int(weather["current_condition"][0]["windspeedMiles"])
                self.windDir        = weather["current_condition"][0]["winddir16Point"]
                self.precipitation  = float(weather["current_condition"][0]["precipInches"])
                self.chanceOfRain   = App.calculateChanceOfRain(self.today)
                self.weatherKind    = int(weather["current_condition"][0]["weatherCode"])
                self.sunrise        = self.today["astronomy"][0]["sunrise"]
                self.sunset         = self.today["astronomy"][0]["sunset"]

                self.tomorrowChanceOfRain   = App.calculateChanceOfRain(self.tomorrow)
                self.ubermorgenChanceOfRain = App.calculateChanceOfRain(self.ubermorgen)

        pass


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
    imgUpdatingIcon = pygame.transform.scale(pygame.image.load('Data/refresh.png'), (80, 80))

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
