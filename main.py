import pygame
from spritesheet import Spritesheet
pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('SMCCD_Hackathon')

timer = pygame.time.Clock()

mySpritesheet = Spritesheet('animations.png')
runAnimation = [mySpritesheet.parse_sprite('cyber prisoner run cycle-Sheet-0.png'), mySpritesheet.parse_sprite('cyber prisoner run cycle-Sheet-1.png'),mySpritesheet.parse_sprite('cyber prisoner run cycle-Sheet-2.png'),
           mySpritesheet.parse_sprite('cyber prisoner run cycle-Sheet-3.png'),mySpritesheet.parse_sprite('cyber prisoner run cycle-Sheet-4.png'),mySpritesheet.parse_sprite('cyber prisoner run cycle-Sheet-5.png'),
           mySpritesheet.parse_sprite('cyber prisoner run cycle-Sheet-5.png'),mySpritesheet.parse_sprite('cyber prisoner run cycle-Sheet-6.png'),mySpritesheet.parse_sprite('cyber prisoner run cycle-Sheet-7.png')]
index = 0

#TODO
# Change fps to be device dependent
fps = 60
player_x = 300
player_y = 300
player_speed = 5
x_direction = 0
y_direction = 0

bg = pygame.image.load('back.png').convert() # replace with background image
bg = pygame.transform.scale(bg,
                       (WIDTH,
                        HEIGHT))
middle = pygame.image.load('middle.png').convert_alpha() # replace with background image
middle = pygame.transform.scale(middle,
                       (WIDTH,
                        HEIGHT))
middle.set_colorkey((0, 0, 0))

run = True
while run:
    timer.tick(fps)
    screen.blit(bg,(0,0))
    screen.blit(middle,(0,0))

    #TODO
    # update images
    # add animation
    # have a way to record multiple previous inputs ( rewind time )
    screen.blit(runAnimation[index], (player_x, player_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #TODO
        # ADD Gravity
        # Remove Down key-press ( Not needed if gravity pulls down )
        # If down kep is kep crouch?
        # set a different vertical speed from horizontal

        # Credited to LeMaster Tech for movement
        # Video : https://www.youtube.com/watch?v=sfniTyS9yHo&t=180s
        # Github : https://github.com/plemaster01/PygameMovement/blob/main/main.py
        if event.type == pygame.KEYDOWN: #not the most responsive when pressing multiple keys
            if event.key == pygame.K_RIGHT:
                x_direction = 1
            elif event.key == pygame.K_LEFT:
                pygame.transform.flip(runAnimation[index], True, False) # flip run animation # does not work
                x_direction = -1
            elif event.key == pygame.K_UP:
                y_direction = -1
            elif event.key == pygame.K_DOWN:
                y_direction = 1
            elif event.key == pygame.K_r: #TODO On a kep press reset level
                print("Do something")
            if index < 8:
                index += 1
            else:
                index = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                x_direction = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_direction = 0
    player_x += player_speed * x_direction
    player_y += player_speed * y_direction
    pygame.display.flip()
pygame.quit()