import pygame
from spritesheet import Spritesheet
pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('SMCCD_Hackathon')

# Load sprite sheet
mySpritesheet = Spritesheet('animations.png')

# This function scales a sprite surface by the given factor.
# For example, factor=4 makes the sprite 4 times bigger in both width and height.
def scale_sprite(sprite, factor=2.5):
    # Get the original width and height of the sprite
    width = sprite.get_width() * factor
    height = sprite.get_height() * factor

    # Scale the sprite to the new dimensions (width x height)
    return pygame.transform.scale(sprite, (width, height))


# Load animations (Changed to look better and take up less space)
runAnimation = [scale_sprite(mySpritesheet.parse_sprite(f'cyber prisoner run cycle-Sheet-{i}.png')) for i in range(8)]
idleAnimation = [scale_sprite(mySpritesheet.parse_sprite(f'cyber prisoner idle-Sheet-{i}.png')) for i in range(8)]
jumpAnimation = [scale_sprite(mySpritesheet.parse_sprite(f'cyber prisoner jump cycle -Sheet-{i}.png')) for i in range(11)]


# Tiles
tile_width = 66
tile_height = 69
myTilesSpritesheet = Spritesheet('tiles.png')
tilesSpriteSheet = [myTilesSpritesheet.parse_sprite('tiles-0.png'),
                    myTilesSpritesheet.parse_sprite('tiles-1.png')]

# Ground tile rects
ground_tiles = []
x_position = 0
while x_position < WIDTH:
    tile_rect = pygame.Rect(x_position, HEIGHT - tile_height, tile_width, tile_height)
    ground_tiles.append(tile_rect)
    x_position += tile_width

# Global variables
timer = pygame.time.Clock()
FPS = 60
player_x = 300
player_y = 300
PLAYERSPEED = 5
x_direction = 0
facing_right = True
current_animation = idleAnimation
index = 0
ANIMATIONCOOLDOWN = 100
last_update = pygame.time.get_ticks()
is_jumping = False
jump_index = 0
jump_animation_started = False
vertical_velocity = 0
GRAVITY = 0.5
JUMPSTRENGTH = -12

# Image variables
bg = pygame.image.load('back.png').convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
middle = pygame.image.load('middle.png').convert_alpha()
middle = pygame.transform.scale(middle, (WIDTH, HEIGHT))
middle.set_colorkey((0, 0, 0))

# Main game loop
run = True
while run:
    timer.tick(FPS)
    screen.blit(bg, (0, 0))
    screen.blit(middle, (0, 0))

    # Draw and update tile graphics
    ground_tiles.clear()
    x_position = 0
    while x_position < WIDTH:
        tile = tilesSpriteSheet[0] if (x_position // tile_width) % 2 == 0 else tilesSpriteSheet[1]
        screen.blit(tile, (x_position, HEIGHT - tile_height))
        ground_tiles.append(pygame.Rect(x_position, HEIGHT - tile_height, tile_width, tile_height))
        x_position += tile_width

    keys = pygame.key.get_pressed()
    x_direction = 0

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x_direction = 1
        facing_right = True
        if not is_jumping:
            current_animation = runAnimation
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x_direction = -1
        facing_right = False
        if not is_jumping:
            current_animation = runAnimation
    elif not is_jumping:
        current_animation = idleAnimation

    now = pygame.time.get_ticks()

    # Handle jump animation
    if is_jumping:
        if not jump_animation_started:
            jump_index = 0
            jump_animation_started = True
            last_update = now

        if (now - last_update) >= ANIMATIONCOOLDOWN:
            last_update = now
            if jump_index < len(jumpAnimation) - 1:
                jump_index += 1
    else:
        if (now - last_update) >= ANIMATIONCOOLDOWN:
            last_update = now
            index = (index + 1) % len(current_animation)

    # Apply horizontal movement
    player_x += PLAYERSPEED * x_direction

    # Apply GRAVITY
    vertical_velocity += GRAVITY
    player_y += vertical_velocity

    # Build player rect
    current_frame = jumpAnimation[jump_index] if is_jumping else current_animation[index]
    player_rect = pygame.Rect(player_x, player_y, current_frame.get_width(), current_frame.get_height())

    # Collision detection
    on_ground = False
    for tile_rect in ground_tiles:
        if player_rect.colliderect(tile_rect):
            # Check from above (landing)
            if vertical_velocity > 0 and player_rect.bottom > tile_rect.top:
                player_rect.bottom = tile_rect.top
                player_y = player_rect.y
                vertical_velocity = 0
                is_jumping = False
                jump_index = 0
                jump_animation_started = False
                on_ground = True

    # Jump
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and on_ground:
        is_jumping = True
        jump_animation_started = False
        vertical_velocity = JUMPSTRENGTH

    # Draw player
    if is_jumping:
        frame = jumpAnimation[jump_index]
    else:
        frame = current_animation[index]
    if not facing_right:
        frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, (player_rect.x, player_rect.y))
    player_x, player_y = player_rect.x, player_rect.y

    # Ending game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
