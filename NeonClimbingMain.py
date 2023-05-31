import pygame
import NeonClimbingScreen
import NeonClimbingApp

print("Hello! :)")

pygame.init()
screen = NeonClimbingScreen.Screen(1920, 1080, 60)
app = NeonClimbingApp.App()

# Utility Variables
running = True
counter = 0

while running:

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

# end while
