from trackblock import TrackBlock
class Checkpoint(TrackBlock):
    def __init__(self, x, y, checkpoint_id):
        super().__init__(x, y, (128, 128, 128))  # checkpoint color
        self.checkpoint_id = checkpoint_id
    def draw(self, screen):
        super().draw(screen)