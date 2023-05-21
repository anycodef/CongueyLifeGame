from pygame import Rect


class DynamicGrid:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # cell
        self.side_cell = 50

        # dynamic grid
        self.rect = Rect(-self.side_cell, -self.side_cell, self.screen_rect.width + 2 * self.side_cell,
                         self.screen_rect.height + 2 * self.side_cell)

        self.row = int(self.rect.height / self.side_cell)
        self.column = int(self.rect.width / self.side_cell)
        self.list_intersection_points = [[self.rect.x, self.rect.y]]
        self.list_extreme_points = []

        # cell
        self.list_live_cell_points = []

        # procedure

