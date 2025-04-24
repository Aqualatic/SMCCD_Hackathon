import pygame
import os
from spritesheet import Spritesheet

# Load and scale sprite helper
def scaleSprite(sprite, factor=2.5):
    width = sprite.get_width() * factor
    height = sprite.get_height() * factor
    return pygame.transform.scale(sprite, (width, height))

# Load all animations
def loadAnimations():
    mySpritesheet = Spritesheet('animations.png')

    runAnimation = [scaleSprite(mySpritesheet.parse_sprite(f'cyber prisoner run cycle-Sheet-{i}.png')) for i in range(8)]
    idleAnimation = [scaleSprite(mySpritesheet.parse_sprite(f'cyber prisoner idle-Sheet-{i}.png')) for i in range(8)]
    jumpAnimation = [scaleSprite(mySpritesheet.parse_sprite(f'cyber prisoner jump cycle -Sheet-{i}.png')) for i in range(11)]

    return runAnimation, idleAnimation, jumpAnimation

# Load all sounds
def loadSounds():
    walkSounds = [pygame.mixer.Sound(os.path.join('Footstep_Sound_Effects/Walk/Dirt', f'DIRT - Walk Short {i}.wav')) for i in range(1, 9)]
    jumpSounds = [pygame.mixer.Sound(os.path.join('Footstep_Sound_Effects/Jump/Dirt', f'Post Jump {i}.wav')) for i in range(1, 9)]
    postJumpSounds = [pygame.mixer.Sound(os.path.join('Footstep_Sound_Effects/Jump/Dirt', f'Post Jump {i}.wav')) for i in range(1, 9)]

    songs = [os.path.join('Ost', file) for file in os.listdir('Ost') if file.endswith('.mp3')]

    return walkSounds, jumpSounds, postJumpSounds, songs
