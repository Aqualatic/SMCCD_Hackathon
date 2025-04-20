import pygame
pygame.init()

#TODO
# decide to keep this or improve upon it
"""
# Set size of window
screen = pygame.display.set_mode((640,640))
screen_rect = screen.get_rect()

# Load and resize image
image = pygame.image.load('image1.png').convert()
image = pygame.transform.scale(image,
                               (image.get_width() / 20,
                                image.get_height() / 20))
image_rect = image.get_rect(center=screen_rect.center)

# Game loop
running = True
x = y = 300
clock = pygame.time.Clock()


while running:

    #manage window
    for event in pygame.event.get(): # Keep Window open
        if event.type == pygame.QUIT:
            running = False

    #display image
    #screen.blit(image,(300,300)) # BLIT: Basically, blit means to copy graphics from one image to another. A more formal definition is to copy an array of data to a bitmapped array destination. You can think of blit as just "assigning" pixels. Much like setting values in our screen-list above, blitting assigns the color of pixels in our image.
    pygame.display.flip()

    keys = pygame.key.get_pressed() # slow inputs
    #while (#!not colliding w/ something ):
    if keys[pygame.K_UP]:
        y -= 1 # Down is +y
    if keys[pygame.K_DOWN]:
        y += 1 # Up is -y
    if keys[pygame.K_LEFT]:
        x -= 1 # left is -x
    if keys[pygame.K_RIGHT]:
        x += 1 # right is +x
    #screen.blit(image, (x, y))

    #Handles Collision w edge of screen, change to collision with other objects
    screen.blit(image, image_rect)
    image_rect.move_ip(x, y)
    image_rect.clamp_ip(screen_rect)

    clock.tick(60) # Limits framerate to 60, change for higher refresh rate monitors (or keep at 60 who c)

pygame.quit() # Close window
"""

# Credited to LeMaster Tech
# Video : https://www.youtube.com/watch?v=sfniTyS9yHo&t=180s
# Github : https://github.com/plemaster01/PygameMovement/blob/main/main.py
WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Movement!')

timer = pygame.time.Clock()
#TODO
# Change fps to be device dependent
fps = 60
player_x = 300
player_y = 300
player_speed = 5
x_direction = 0
y_direction = 0

run = True
while run:
    timer.tick(fps)
    pygame.draw.rect(screen, 'brown', [0, HEIGHT - 100, WIDTH, 100])
    #TODO
    # update images
    # add animation
    # have a way to record multiple previous inputs ( rewind time )
    image = pygame.image.load('image1.png').convert()
    image = pygame.transform.scale(image,
                                   (image.get_width() / 20,
                                    image.get_height() / 20))
    screen.blit(image, (player_x, player_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #TODO
        # ADD Gravity
        # Remove Down key-press ( Not needed if gravity pulls down )
        # If down kep is kep crouch?
        # set a different vertical speed from horizontal
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_direction = 1
            elif event.key == pygame.K_LEFT:
                x_direction = -1
            elif event.key == pygame.K_UP:
                y_direction = -1
            elif event.key == pygame.K_DOWN:
                y_direction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                x_direction = 0
            elif event.key == pygame.K_LEFT:
                x_direction = 0
            elif event.key == pygame.K_UP:
                y_direction = 0
            elif event.key == pygame.K_DOWN:
                y_direction = 0
    player_x += player_speed * x_direction
    player_y += player_speed * y_direction
    #TODO
    # Have the background update to hide previous drawn images
    pygame.display.flip()
pygame.quit()