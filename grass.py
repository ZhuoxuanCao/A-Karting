from trackblock import TrackBlock
class Grass(TrackBlock):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 255, 0))
    def draw(self, screen):
        super().draw(screen)