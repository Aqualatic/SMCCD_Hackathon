import pygame
import random
import time
from spritesheet import Spritesheet
from clone import GhostClone
from animationsAndMusic import loadAnimations, loadSounds

pygame.init()

# Screen setup
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('SMCCD_Hackathon')

# Load animations and sounds from assets.py
runAnimation, idleAnimation, jumpAnimation = loadAnimations()
walkSounds, jumpSounds, postJumpSounds, songs = loadSounds()

# Tiles
tileWidth = 66
tileHeight = 69
myTilesSpritesheet = Spritesheet('tiles.png')
tilesSpriteSheet = [myTilesSpritesheet.parse_sprite('tiles-0.png'),
                    myTilesSpritesheet.parse_sprite('tiles-1.png')]

# Ground tile rects
ground_tiles = []
x_position = 0
while x_position < WIDTH:
    tile_rect = pygame.Rect(x_position, HEIGHT - tileHeight, tileWidth, tileHeight)
    ground_tiles.append(tile_rect)
    x_position += tileWidth

# Global variables
timer = pygame.time.Clock()
FPS = 60
player_x = 300
player_y = 300
PLAYERSPEED = 3
x_direction = 0
facingRight = True
currentAnimation = idleAnimation
index = 0
ANIMATIONCOOLDOWN = 100
last_update = pygame.time.get_ticks()
isJumping = False
jumpIndex = 0
jumpAnimationStarted = False
verticalVelocity = 0
GRAVITY = 0.5
JUMPSTRENGTH = -12
lastWalkSound = 0
WALKSOUNDCOOLDOWN = 300  # milliseconds
wasOnGround = False
lastPostJumpSound = 0
POSTJUMPSOUNDCOOLDOWN = 500  # milliseconds
postJumpPlayed = False
nextSong = None

# Main gimmick
# Clone system
playerMovements = []
clones = []

#TODO
# Sound volume changer
# Levels
# Read me

# Music handling
def playSong(song_path):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    return pygame.mixer.Sound(song_path).get_length()

currentSong = random.choice(songs)
songLength = playSong(currentSong)
songStartTime = time.time()
songEndTime = songStartTime + songLength

def getNextSong():
    return random.choice([s for s in songs if s != currentSong])

# Image variables
bg = pygame.image.load('back.png').convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
middle = pygame.image.load('middle.png').convert_alpha()
middle = pygame.transform.scale(middle, (WIDTH, HEIGHT))
middle.set_colorkey((0, 0, 0))

# Main game loop
run = True
while run:
    # Inital setup
    now = time.time()
    timeLeft = songEndTime - now
    timer.tick(FPS)
    screen.blit(bg, (0, 0))
    screen.blit(middle, (0, 0))

    # Queue the next song 3 seconds before the current one ends
    if timeLeft <= 3 and not pygame.mixer.music.get_busy():
        currentSong = getNextSong()
        songLength = playSong(currentSong)
        songStartTime = time.time()
        songEndTime = songStartTime + songLength

    # Draw and update tile graphics
    ground_tiles.clear()
    x_position = 0
    while x_position < WIDTH:
        tile = tilesSpriteSheet[0] if (x_position // tileWidth) % 2 == 0 else tilesSpriteSheet[1]
        screen.blit(tile, (x_position, HEIGHT - tileHeight))
        ground_tiles.append(pygame.Rect(x_position, HEIGHT - tileHeight, tileWidth, tileHeight))
        x_position += tileWidth

    keys = pygame.key.get_pressed()
    x_direction = 0

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x_direction = 1
        facingRight = True
        if not isJumping:
            currentAnimation = runAnimation
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x_direction = -1
        facingRight = False
        if not isJumping:
            currentAnimation = runAnimation
    elif not isJumping:
        currentAnimation = idleAnimation

    now = pygame.time.get_ticks()

    # Handle jump animation
    if isJumping:
        if not jumpAnimationStarted:
            jumpIndex = 0
            jumpAnimationStarted = True
            last_update = now
        if (now - last_update) >= ANIMATIONCOOLDOWN:
            last_update = now
            if jumpIndex < len(jumpAnimation) - 1:
                jumpIndex += 1
    else:
        if (now - last_update) >= ANIMATIONCOOLDOWN:
            last_update = now
            index = (index + 1) % len(currentAnimation)

    # Apply horizontal movement
    player_x += PLAYERSPEED * x_direction

    # Apply gravity
    verticalVelocity += GRAVITY
    player_y += verticalVelocity

    # Build player rect
    currentFrame = jumpAnimation[jumpIndex] if isJumping else currentAnimation[index]
    playerRect = pygame.Rect(player_x, player_y, currentFrame.get_width(), currentFrame.get_height())

    # Collision detection
    onGround = False
    for tileRect in ground_tiles:
        if playerRect.colliderect(tileRect):
            if verticalVelocity > 0 and playerRect.bottom > tileRect.top:
                playerRect.bottom = tileRect.top
                player_y = playerRect.y
                verticalVelocity = 0
                isJumping = False
                jumpIndex = 0
                jumpAnimationStarted = False
                onGround = True

    # Post-jump sound
    if onGround and not wasOnGround and not postJumpPlayed:
        now = pygame.time.get_ticks()
        if now - lastPostJumpSound >= POSTJUMPSOUNDCOOLDOWN:
            random.choice(postJumpSounds).play()
            lastPostJumpSound = now
            postJumpPlayed = True

    # Reset post-jump sound flag
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and onGround:
        isJumping = True
        jumpAnimationStarted = False
        verticalVelocity = JUMPSTRENGTH
        wasOnGround = False
        postJumpPlayed = False

    # Walk sound effect
    if x_direction != 0 and onGround:
        now = pygame.time.get_ticks()
        if now - lastWalkSound >= WALKSOUNDCOOLDOWN:
            random.choice(walkSounds).play()
            lastWalkSound = now

    # Record movement
    playerMovements.append({
        "x": player_x,
        "y": player_y,
        "frame": jumpIndex if isJumping else index,
        "isJumping": isJumping,
        "facing": facingRight,
        "isRunning": currentAnimation == runAnimation  # Add isRunning flag
    })

    # Update and draw clones
    for clone in clones:
        if clone.playing:
            clone.update()
        clone.draw(screen)

    # Draw player
    frame = jumpAnimation[jumpIndex] if isJumping else currentAnimation[index]
    if not facingRight:
        frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, (playerRect.x, playerRect.y))
    player_x, player_y = playerRect.x, playerRect.y

    wasOnGround = onGround

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # First, create a clone from the current movement history
                clones.append(GhostClone(playerMovements.copy(), runAnimation, idleAnimation, jumpAnimation))

                # Then tell all clones to start playing
                for clone in clones:
                    clone.restart()

                # Now reset the player state and clear the recording
                player_x, player_y = 300, 300
                verticalVelocity = 0
                isJumping = False
                jumpIndex = 0
                jumpAnimationStarted = False
                postJumpPlayed = False
                playerMovements.clear()

    pygame.display.flip()

pygame.quit()
