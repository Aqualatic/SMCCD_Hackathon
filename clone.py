class Clone:
    def __init__(self, history, runAnimation, idleAnimation, jumpAnimation, delay_frames=300):
        self.history = history
        self.frame = 0
        self.delay_frames = delay_frames
        self.runAnimation = runAnimation
        self.idleAnimation = idleAnimation
        self.jumpAnimation = jumpAnimation
        self.playing = False
        self.data = None

    def restart(self):
        self.frame = 0
        self.playing = True

    def update(self):
        if self.playing and self.frame + self.delay_frames < len(self.history):
            self.data = self.history[self.frame + self.delay_frames]
            self.frame += 1
        else:
            self.playing = False

    def draw(self, surface):
        if not self.playing or self.frame_index >= len(self.movements):
            return
        move = self.movements[self.frame_index]
        frame = self.jumpAnimation[move["frame"]] if move["isJumping"] else (
            self.runAnimation[move["frame"]] if move["isRunning"] else self.idleAnimation[move["frame"]]
        )
        if not move["facing"]:
            frame = pygame.transform.flip(frame, True, False)
        surface.blit(frame, (move["x"], move["y"]))

