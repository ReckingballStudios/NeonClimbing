# Application File


import pygame
import python_weather
from python_weather import enums
import asyncio
from aiohttp import client_exceptions
import time
import math




class App:

    # Coordinates
    coordsHeader    = (110,     20)
    coordsTime      = (1460,    5)
    coordsUpdating  = (coordsTime[0] - 80, coordsTime[1] + 60)
    coordsImage     = (1280,    150)
    coordsClimbIndex = (coordsImage[0] - 80, coordsImage[1])

    coordsCurrently = (coordsHeader[0] + 185,     195)
    coordsIcon      = (25,      coordsCurrently[1] + 5)
    coordsTemp      = (coordsIcon[0] + 255,           coordsIcon[1])
    coordsHumidity  = (coordsTemp[0] + 475,     coordsTemp[1] + 25)
    coordsDewPoint  = (coordsHumidity[0],     coordsHumidity[1] + 65)
    coordsWind      = (coordsHumidity[0],     coordsDewPoint[1] + 65)
    coordsPrecip    = (coordsIcon[0] + 200,   coordsTemp[1] + 250)
    coordsPrecipText = (coordsPrecip[0] + 100,   coordsPrecip[1] + 18)
    coordsSunrise   = (coordsPrecip[0] + 280, coordsPrecip[1])
    coordsSunriseText = (coordsSunrise[0] + 110, coordsSunrise[1] + 18)
    coordsSunset    = (coordsSunrise[0] + 340, coordsPrecip[1])
    coordsSunsetText = (coordsSunset[0] + 110, coordsSunset[1] + 18)

    # Future Forecast Coords
    coordsTomorrow = (coordsIcon[0] + 225, coordsIcon[1] + 400)
    coordsUbermorgen = (coordsTomorrow[0] + 525, coordsTomorrow[1])
    coordsTomorrowIcon = (coordsTomorrow[0] - 100, coordsTomorrow[1] + 50)
    coordsUbermorgenIcon = (coordsUbermorgen[0] - 100, coordsUbermorgen[1] + 50)
    coordsTomorrowTemp = (coordsTomorrow[0] - 135, coordsTomorrow[1] + 270)
    coordsUbermorgenTemp = (coordsUbermorgen[0] - 135, coordsUbermorgen[1] + 270)
    coordsTomorrowPrecip = (coordsTomorrowIcon[0] + 260, coordsTomorrowIcon[1] + 20)
    coordsUbermorgenPrecip = (coordsUbermorgenIcon[0] + 260, coordsUbermorgenIcon[1] + 30)


    sizeClimbIndex = (72, 900)

    weatherUpdateFrequency = 900
    iterateScreenFrequency = 60

    # Initialize
    def __init__(self):

        # Font and Text initialization
        self.fontTemperature = pygame.font.SysFont('timesnewroman', int(230))
        self.fontTempSmall = pygame.font.SysFont('timesnewroman', int(90))
        self.fontHeader = pygame.font.SysFont('timesnewroman', int(140))
        self.fontCurrently = pygame.font.SysFont('timesnewroman', int(80))
        self.fontInfo = pygame.font.SysFont('timesnewroman', int(55))
        self.fontTime = pygame.font.SysFont('timesnewroman', int(40))

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
        if event.type == pygame.MOUSEBUTTONUP:
            self.iterateLocation()
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
        if location.temperature >= 100:
            textTemperature = self.fontTemperature.render("{}°".format(location.temperature), True, self.colorTempText)

        screen.blit(textTemperature, App.coordsTemp)

        # Write Humidity
        textHumidity = self.fontInfo.render("{}% Humidity".format(location.humidity), True, self.colorText)
        screen.blit(textHumidity, App.coordsHumidity)

        # Write Dew Point
        textDewPoint = self.fontInfo.render("{}°F Dew Point".format(location.dewPoint), True, self.colorText)
        screen.blit(textDewPoint, App.coordsDewPoint)

        # Write Wind
        textWind = self.fontInfo.render("{} MPH {}".format(location.windSpeed, location.windDir.value), True, self.colorText)
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
        tomorrowDayOfWeek = self.weekdayFromIndex(location.tomorrow.date.weekday())
        text = self.fontInfo.render("{dow:}".format(dow=tomorrowDayOfWeek), True, self.colorText)
        screen.blit(text, App.coordsTomorrow)

        # Draw Tomorrows Weather Icon
        self.paintWeatherIcon(screen, self.deriveWeatherKind(location.tomorrow), App.coordsTomorrowIcon)

        # Draw Tomorrows High
        string = "{hi:}°F | {low:}°F".format(hi=location.tomorrow.highest_temperature, low=location.tomorrow.lowest_temperature)
        text = self.fontTempSmall.render(string, True, self.colorText)
        screen.blit(text, App.coordsTomorrowTemp)

        # Draw Tomorrows Precipitation Chance
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.RAIN_SMALL], App.coordsTomorrowPrecip)
        precipitationChance = location.tomorrowChanceOfRain
        text = self.fontInfo.render("{chance:d}%".format(chance=int(precipitationChance)), True, self.colorText)
        screen.blit(text, (App.coordsTomorrowPrecip[0]+15, App.coordsTomorrowPrecip[1]+90))

        # Draw Ubermorgen
        ubermorgenDayOfWeek = self.weekdayFromIndex(location.ubermorgen.date.weekday())
        text = self.fontInfo.render("{}".format(ubermorgenDayOfWeek), True, self.colorText)
        screen.blit(text, App.coordsUbermorgen)

        # Draw Ubermorgens Weather Icon
        self.paintWeatherIcon(screen, self.deriveWeatherKind(location.ubermorgen), App.coordsUbermorgenIcon)

        # Draw Ubermorgens High
        string = "{hi:}°F | {low:}°F".format(hi=location.ubermorgen.highest_temperature, low=location.ubermorgen.lowest_temperature)
        text = self.fontTempSmall.render(string, True, self.colorText)
        screen.blit(text, App.coordsUbermorgenTemp)

        # Draw Tomorrows Precipitation Chance
        screen.blit(WeatherIcon.imgWeatherIcon[WeatherIcon.RAIN_SMALL], App.coordsUbermorgenPrecip)
        precipitationChance = location.ubermorgenChanceOfRain
        text = self.fontInfo.render("{chance:}%".format(chance=int(precipitationChance)), True, self.colorText)
        screen.blit(text, (App.coordsUbermorgenPrecip[0]+ 15, App.coordsUbermorgenPrecip[1] + 90))
        pass

    def paintWeatherIcon(self, screen, weather, coords):
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

    def weekdayFromIndex(self, index):
        weekdays = \
            [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ]
        return weekdays[index]

    @staticmethod
    def deriveChanceOfRain(dailyForecast):
        chance = 0
        hourlyForecast = iter(dailyForecast.hourly)

        # Note: hourlyForecast is actually every 3 hours
        for i in range(8):
            hourly = next(hourlyForecast)
            if i >= 4:
                chance += hourly.chances_of_rain

        chance /= 4
        return chance

    @staticmethod
    def deriveWeatherKind(dailyForecast):
        hourlyForecast = iter(dailyForecast.hourly)
        for i in range(5):
            next(hourlyForecast)

        time3pm = next(hourlyForecast)
        return time3pm.kind

    @staticmethod
    def deriveDewPoint(dailyForecast):
        hourlyForecast = iter(dailyForecast.hourly)
        for i in range(5):
            next(hourlyForecast)

        time3pm = next(hourlyForecast)
        return time3pm.dew_point

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
        self.name = name
        self.weatherLocation = weatherLocation
        self.image = image
        self.temperature = 999
        self.humidity = 999
        self.dewPoint = 999
        self.windSpeed = 999
        self.windDir = "NA"
        self.precipitation = 999
        self.chanceOfRain = 999
        self.sunrise = "NA"
        self.sunset = "NA"
        self.weatherKind = "NA"
        self.forecast = 0
        self.today = 0
        self.tomorrow = 0
        self.ubermorgen = 0
        self.tomorrowChanceOfRain = 0
        self.ubermorgenChanceOfRain = 0


        self.climbingIndex = 0

        self.updateWeather()


        pass

    def calculateClimbingIndex(self):

        temperatureScore = self.calculateTemperatureScore()

        humidityScore = self.calculateHumidityScore()

        dewPointScore = self.calculateDewPointScore()

        windScore = self.calculateWindScore()

        self.climbingIndex = (.40 * temperatureScore) + (.15 * humidityScore) + (.30 * dewPointScore) + (.15 * windScore)

        if self.weatherKind == enums.Kind.SUNNY:
            self.climbingIndex += 2
        elif self.weatherKind == enums.Kind.PARTLY_CLOUDY:
            self.climbingIndex += 4
        elif self.weatherKind == enums.Kind.CLOUDY:
            self.climbingIndex += 3
        elif self.weatherKind == enums.Kind.VERY_CLOUDY:
            self.climbingIndex += 3

        self.climbingIndex = self.climbingIndex - self.chanceOfRain

        # Validation, 8 is lowest so picture still displays, and bar is visible
        if self.climbingIndex < 8:
            self.climbingIndex = 8
        if self.climbingIndex > 100:
            self.climbingIndex = 100

        pass

    def calculateTemperatureScore(self):
        if self.temperature < 0 or self.temperature > 103:
            return -100


        x = self.temperature
        # Formula derived from interpolation
        temperatureScore =      0.00000016765 * math.pow(x, 5)
        temperatureScore +=    -0.000031609 * math.pow(x, 4)
        temperatureScore +=     0.0012482 * math.pow(x, 3)
        temperatureScore +=     0.015440 * math.pow(x, 2)
        temperatureScore +=     0.91796 * x

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

    def calculateDewPointScore(self):
        dewPoint = App.deriveDewPoint(self.today)
        if dewPoint > 75 or dewPoint < -8:
            return 0

        x = dewPoint
        # Our Polynomial Function derived from interpolation
        dewPointScore =     0.00000026936 * math.pow(x, 5)
        dewPointScore +=   -0.000034728 * math.pow(x, 4)
        dewPointScore +=    0.0016441 * math.pow(x, 3)
        dewPointScore +=   -0.10873 * math.pow(x, 2)
        dewPointScore +=    4.5017 * x
        dewPointScore +=    40

        if dewPointScore < 0:
            dewPointScore = 0
        if dewPointScore > 100:
            dewPointScore = 100

        # print("{}: {}".format(x, dewPointScore))

        return dewPointScore

    def calculateWindScore(self):
        windScore = 100 - (10 * math.fabs(10 - self.windSpeed))

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
        except client_exceptions.ClientOSError:
            print("OS Error")
        except client_exceptions.ClientError:
            print("Client Error")

        try:
            self.calculateClimbingIndex()
        except AttributeError:
            print("Attribute Error")

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

            self.chanceOfRain = App.deriveChanceOfRain(self.today)
            self.tomorrowChanceOfRain = App.deriveChanceOfRain(self.tomorrow)
            self.ubermorgenChanceOfRain = App.deriveChanceOfRain(self.ubermorgen)
            self.dewPoint = App.deriveDewPoint(self.today)

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

