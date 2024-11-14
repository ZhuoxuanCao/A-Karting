from trackblock import TrackBlock
class Boost(TrackBlock):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 255, 0))
    def draw(self, screen):
        super().draw(screen)