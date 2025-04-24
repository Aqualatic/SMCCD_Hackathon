import pygame
import random
import time
from spritesheet import Spritesheet
from clone import Clone
from animationsAndMusic import loadanimations, loadsounds

pygame.init()

# Screen setup
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('SMCCD_Hackathon')

# Load animations and sounds
runAnimation, idleAnimation, jumpAnimation = loadanimations()
walkSounds, jumpSounds, postJumpSounds, songs = loadsounds()

# Tile setup
tileWidth = 66
tileHeight = 69
myTilesSpritesheet = Spritesheet('tiles.png')
tilesSpriteSheet = [myTilesSpritesheet.parse_sprite('tiles-0.png'),
                    myTilesSpritesheet.parse_sprite('tiles-1.png')]
ground_tiles = []

# Music
def playsong(song_path):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    return pygame.mixer.Sound(song_path).get_length()

currentSong = random.choice(songs)
songLength = playsong(currentSong)
songStartTime = time.time()
songEndTime = songStartTime + songLength

def getnextsong():
    return random.choice([s for s in songs if s != currentSong])

# Background
bg = pygame.image.load('back.png').convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
middle = pygame.image.load('middle.png').convert_alpha()
middle = pygame.transform.scale(middle, (WIDTH, HEIGHT))
middle.set_colorkey((0, 0, 0))

# Timing
timer = pygame.time.Clock()
FPS = 60

# Player
player_x = 300
player_y = 300
playerSpeed = 3
x_direction = 0
facingRight = True
currentAnimation = idleAnimation
index = 0
animationCooldown = 100
last_update = pygame.time.get_ticks()
isJumping = False
jumpIndex = 0
jumpAnimationStarted = False
verticalVelocity = 0
GRAVITY = 0.5
jumpStrength = -12
lastWalkSound = 0
walkSoundCooldown = 300
wasOnGround = False
lastPostJumpSound = 0
postJumpSoundCooldown = 500
postJumpPlayed = False

trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Clone logic
cloneDelayFrames = 3 * FPS  #  seconds
movementHistory = []
clone = Clone([], runAnimation, idleAnimation, jumpAnimation)

# Main game loop flag
run = True
# Main game loop
while run:
    # Get the current time to calculate time left in the song
    now = time.time()
    timeLeft = songEndTime - now

    # Cap the frame rate
    timer.tick(FPS)

    # Draw background and middle layer images
    screen.blit(bg, (0, 0))
    screen.blit(middle, (0, 0))

    # If the song has ended (within 3 seconds buffer), play the next song
    if timeLeft <= 3 and not pygame.mixer.music.get_busy():
        currentSong = getnextsong()                  # Fetch the next song
        songLength = playsong(currentSong)           # Start the new song
        songStartTime = time.time()                  # Record start time
        songEndTime = songStartTime + songLength     # Calculate end time

    # Draw ground tiles
    ground_tiles.clear()
    x_position = 0
    while x_position < WIDTH:
        # Alternate between two ground tile sprites for visual variation
        tile = tilesSpriteSheet[0] if (x_position // tileWidth) % 2 == 0 else tilesSpriteSheet[1]
        screen.blit(tile, (x_position, HEIGHT - tileHeight))
        # Save tile rect for collision detection
        ground_tiles.append(pygame.Rect(x_position, HEIGHT - tileHeight, tileWidth, tileHeight))
        x_position += tileWidth

    # Read keyboard input for movement
    keys = pygame.key.get_pressed()
    x_direction = 0

    # Move right
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x_direction = 1
        facingRight = True
        if not isJumping:
            currentAnimation = runAnimation

    # Move left
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x_direction = -1
        facingRight = False
        if not isJumping:
            currentAnimation = runAnimation

    # Idle animation when not jumping or moving
    elif not isJumping:
        currentAnimation = idleAnimation

    # Handle animation timing
    now = pygame.time.get_ticks()

    # Jump animation logic
    if isJumping:
        if not jumpAnimationStarted:
            jumpIndex = 0
            jumpAnimationStarted = True
            last_update = now
        if (now - last_update) >= animationCooldown:
            last_update = now
            if jumpIndex < len(jumpAnimation) - 1:
                jumpIndex += 1

    # Idle or run animation logic
    else:
        if (now - last_update) >= animationCooldown:
            last_update = now
            index = (index + 1) % len(currentAnimation)

    # Update player position
    player_x += playerSpeed * x_direction
    verticalVelocity += GRAVITY  # Apply gravity
    player_y += verticalVelocity

    # Choose the correct frame to draw
    currentFrame = jumpAnimation[jumpIndex] if isJumping else currentAnimation[index]

    # Update player rectangle for collisions and drawing
    playerRect = pygame.Rect(player_x, player_y, currentFrame.get_width(), currentFrame.get_height())

    # Collision detection with the ground
    onGround = False
    for tileRect in ground_tiles:
        if playerRect.colliderect(tileRect):
            if verticalVelocity > 0 and playerRect.bottom > tileRect.top:
                playerRect.bottom = tileRect.top  # Adjust position to sit on tile
                player_y = playerRect.y
                verticalVelocity = 0  # Stop falling
                isJumping = False
                jumpIndex = 0
                jumpAnimationStarted = False
                onGround = True

    # Play sound when landing after a jump
    if onGround and not wasOnGround and not postJumpPlayed:
        now = pygame.time.get_ticks()
        if now - lastPostJumpSound >= postJumpSoundCooldown:
            random.choice(postJumpSounds).play()
            lastPostJumpSound = now
            postJumpPlayed = True

    # Start jump if UP or W is pressed and player is on ground
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and onGround:
        isJumping = True
        jumpAnimationStarted = False
        verticalVelocity = jumpStrength  # Apply jump force
        wasOnGround = False
        postJumpPlayed = False

    # Play walking sound while moving on ground
    if x_direction != 0 and onGround:
        now = pygame.time.get_ticks()
        if now - lastWalkSound >= walkSoundCooldown:
            random.choice(walkSounds).play()
            lastWalkSound = now


    # Record movement for clone
    movementHistory.append({
        "x": player_x,
        "y": player_y,
        "frame": jumpIndex if isJumping else index,
        "isJumping": isJumping,
        "facing": facingRight,
        "isRunning": currentAnimation == runAnimation
    })

    if len(movementHistory) > cloneDelayFrames:
        delayedFrame = movementHistory[-cloneDelayFrames]
        clone.data = delayedFrame

    # Idea from this YouTube tutorial on creating dust trail effects in Pygame.
    # Video: https://www.youtube.com/watch?v=nfJGJ98RW60
    # Clear previous trail
    trail_surface.fill((0, 0, 0, 0))

    # Draw trail (past positions up to the clone's current position)
    if len(movementHistory) > cloneDelayFrames:
        trail_color = (0, 255, 255, 100)  # Cyan with alpha transparency
        trail_points = [(frame["x"] + 16, frame["y"] + 32) for frame in movementHistory[-cloneDelayFrames:]]

        if len(trail_points) > 1:
            pygame.draw.lines(trail_surface, trail_color, False, trail_points, 4)

    # Blit trail to main screen
    screen.blit(trail_surface, (0, 0))

    # Draw clone
    if clone.data:
        # Determine which animation frame to use for the clone based on its state (jumping, running, idle)
        frame = jumpAnimation[clone.data["frame"]] if clone.data["isJumping"] else (
            runAnimation[clone.data["frame"]] if clone.data["isRunning"] else idleAnimation[clone.data["frame"]]
        )

        # If the clone is not facing right, flip the frame horizontally
        if not clone.data["facing"]:
            frame = pygame.transform.flip(frame, True, False)

        # Create a copy of the selected frame and apply transparency (alpha)
        ghost = frame.copy()
        ghost.set_alpha(100)

        # Blit (draw) the clone onto the screen at its position
        screen.blit(ghost, (clone.data["x"], clone.data["y"]))

    # Draw player
    # Choose the correct animation frame for the player based on whether they are jumping or not
    frame = jumpAnimation[jumpIndex] if isJumping else currentAnimation[index]

    # If the player is not facing right, flip the frame horizontally
    if not facingRight:
        frame = pygame.transform.flip(frame, True, False)

    # Blit (draw) the player onto the screen at their position
    screen.blit(frame, (playerRect.x, playerRect.y))

    # Save the player's current position for later use (e.g., swapping with clone)
    player_x, player_y = playerRect.x, playerRect.y

    # Update the ground state to track whether the player was on the ground last frame
    wasOnGround = onGround

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game if the player closes the window
            run = False
        elif event.type == pygame.KEYDOWN:
            # Check if the 'R' key is pressed to swap positions with the clone
            if event.key == pygame.K_r and clone.data:
                # Swap the player’s and clone’s positions
                temp_x, temp_y = player_x, player_y
                player_x = clone.data["x"]
                player_y = clone.data["y"]
                clone.data["x"] = temp_x
                clone.data["y"] = temp_y

    pygame.display.flip()

pygame.quit()
