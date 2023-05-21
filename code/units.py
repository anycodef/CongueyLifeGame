from pygame import Rect
from pygame.draw import line, rect
from pygame.mouse import get_pos, get_pressed

class Cell:
    def __init__(self):
        self.side = 50
        self.color = 'green'

class DynamicGrid:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # cell
        self.cell_attr = Cell()

        # color
        self.color_line = 'black'
        self.width_line = 1

        # dynamic grid
        self.rect = Rect(-self.cell_attr.side, -self.cell_attr.side, self.screen_rect.width + 2 * self.cell_attr.side,
                         self.screen_rect.height + 2 * self.cell_attr.side)

        self.row = int(self.rect.height / self.cell_attr.side)
        self.column = int(self.rect.width / self.cell_attr.side)
        self.list_intersection_points = []
        self.list_extreme_points = []

        # cell
        self.list_live_cell_points = []

        # procedure: find interception points and extremes points list
        y = self.rect.y
        h1, h2 = [], []

        for row in range(self.row + 1):
            row_points = []
            x = self.rect.x
            for column in range(self.column + 1):
                if column != self.column and row != self.row:
                    row_points.append([x, y])

                if column == 0:
                    h1.append([x, y])
                if column == self.column:
                    h2.append([x, y])

                x += self.cell_attr.side
            if row != self.row:
                self.list_intersection_points.append(row_points)
            y += self.cell_attr.side

        v1, v2 = self.list_intersection_points[0], self.list_intersection_points.copy().pop()

        self.list_extreme_points.append(list(zip(h1, h2)))
        self.list_extreme_points.append(list(zip(v1, v2)))

    def draw_grip_and_live_cells(self):
        for orientation in self.list_extreme_points:
            for point1, point2 in orientation:
                line(self.screen, self.color_line, point1, point2, self.width_line)

    def listen_points_live_cell(self):
        for point_inter in self.list_intersection_points:
            if 























