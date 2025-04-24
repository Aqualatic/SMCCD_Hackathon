# Credited to CDcodes for class
# Video : https://www.youtube.com/watch?v=ePiMYe7JpJo
# Github : https://github.com/ChristianD37/YoutubeTutorials/blob/master/spritesheet/test_game.py
import pygame
import json

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename

        # Load the sprite sheet image
        self.sprite_sheet = pygame.image.load(filename).convert()

        # Load the corresponding JSON metadata
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)

    def get_sprite(self, x, y, w, h):
        # Create a surface for the sprite
        sprite = pygame.Surface((w, h)).convert()

        # Set black as the transparent color
        sprite.set_colorkey((0, 0, 0))

        # Copy the sprite portion from the sprite sheet
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))

        return sprite

    def parse_sprite(self, name):
        # Get the frame data for the sprite by name
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]

        # Extract the sprite image from the sprite sheet
        image = self.get_sprite(x, y, w, h)

        return image






