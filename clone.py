import pygame

# Ghost Clone System implemented with the help of ChatGPT, for logic planning and Pygame integration.
# Clone system inspired by the tutorial:
# "How to create a Replay System like in Super Meat Boy using Unity"
# Available at: https://www.youtube.com/watch?v=ilOQstDnX2I
class Clone:
    def __init__(self, history, runAnimation, idleAnimation, jumpAnimation, delay_frames=300):
        self.history = history  # List of previous player states
        self.delay_frames = delay_frames  # Number of frames the clone lags behind
        self.runAnimation = runAnimation  # List of images for running animation
        self.idleAnimation = idleAnimation  # List of images for idle animation
        self.jumpAnimation = jumpAnimation  # List of images for jumping animation
        self.data = None  # Placeholder for the clone's current frame data

    def update(self):
        # Only update if we have enough history to account for the delay
        if len(self.history) > self.delay_frames:
            self.data = self.history[-self.delay_frames]  # Get the delayed frame from history

    def draw(self, surface):
        if not self.data:
            return  # Exit if there's no data to draw

        move = self.data  # Extract movement data from the delayed frame

        # Choose the correct animation based on the movement state
        frame = self.jumpAnimation[move["frame"]] if move["isJumping"] else (
            self.runAnimation[move["frame"]] if move["isRunning"] else self.idleAnimation[move["frame"]]
        )

        if not move["facing"]:
            frame = pygame.transform.flip(frame, True, False)  # Flip the frame if facing left

        ghost = frame.copy()  # Create a copy of the frame
        ghost.set_alpha(100)  # Make the clone semi-transparent
        surface.blit(ghost, (move["x"], move["y"]))  # Draw the clone at the recorded position