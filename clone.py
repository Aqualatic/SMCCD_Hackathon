import pygame


# Ghost Clone System implemented with the help of ChatGPT, for logic planning and Pygame integration.
# Clone system inspired by the tutorial:
# "How to create a Replay System like in Super Meat Boy using Unity"
# Available at: https://www.youtube.com/watch?v=ilOQstDnX2I

class GhostClone:
    def __init__(self, history, runAnimation, idleAnimation, jumpAnimation):
        self.history = history
        self.frame = 0
        self.active = True
        self.runAnimation = runAnimation
        self.idleAnimation = idleAnimation
        self.jumpAnimation = jumpAnimation
        self.playing = False
        self.data = None

    def restart(self):
        self.frame = 0
        self.playing = True

    def update(self):
        if self.playing and self.frame < len(self.history):
            self.data = self.history[self.frame]
            self.frame += 1
        else:
            self.playing = False  # Stop playback after one loop

    def draw(self, surface):
        if self.playing and self.data:
            if self.data["isJumping"]:
                animate = self.jumpAnimation
            elif self.data["isRunning"]:
                animate = self.runAnimation
            else:
                animate = self.idleAnimation

            frame = animate[self.data["frame"]]
            if not self.data["facing"]:
                frame = pygame.transform.flip(frame, True, False)
            ghost = frame.copy()
            ghost.set_alpha(100)  # Transparent
            surface.blit(ghost, (self.data["x"], self.data["y"]))
