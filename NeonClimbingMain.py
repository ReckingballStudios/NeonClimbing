
import pygame

import NeonClimbingScreen
import NeonClimbingApp
from Watchdog import WatchdogTimer

print("Hello! :)")

pygame.init()
screen = NeonClimbingScreen.Screen(1920, 1080, 60)
app = NeonClimbingApp.App()



# Making an invisible cursor
custom_cursor_data = [
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                "
]
# Create a cursor with the custom cursor data.
custom_cursor, custom_cursor_mask = pygame.cursors.compile(custom_cursor_data, black='X', white='.', xor='o')
# Set the custom cursor.
pygame.mouse.set_cursor((32, 32), (0, 0), custom_cursor, custom_cursor_mask)

# NOTE! v- mouse.set_visible(False) produces a bug in the RaspberryPi version
# pygame.mouse.set_visible(False)

# Utility Variables
running = True
counter = 0

# watchdog timer
watchdogTimeout = 120
watchdog = WatchdogTimer(watchdogTimeout)
iteration = 0
watchdogFrameReset = 600


while running:
    # Start watchdog at beginning of frame
    if iteration == 0:
        watchdog.start()



    # Handle User Input    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle Mouse Input
        app.handleMouse(event)

        # Handle Keyboard Input
        running = app.handleKeyboard(event)
    # end for    

    # Update Frame
    app.update()

    # Paint Frame to Screen
    app.paint(screen.pyScreen)

    # Update Display
    pygame.display.update()
    screen.fpsClock.tick(60)


    iteration += 1
    # Reset Watchdog at end of frame
    if iteration == watchdogFrameReset:
        watchdog.stop()
        iteration = 0



# end while


