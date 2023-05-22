from pygame import Rect
from pygame.draw import line, rect
from pygame.mouse import get_pos, get_pressed


class Cell:
    def __init__(self):
        self.side = 50
        self.color = 'green'
        self.point_on_top_of = None
        self.width_border_on_top_of = 2

        # on click
        self.one_time_clicked = True


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

        self.row = None
        self.column = None
        self.list_intersection_points = None
        self.list_extreme_points = None

        # cell
        self.list_live_cell_points = []

    def calculate_disposition_of_grid(self):

        # initialize the variables
        self.list_live_cell_points = []
        self.list_extreme_points = []
        self.list_intersection_points = []

        self.row = 0
        while self.row * self.cell_attr.side < self.rect.height:
            self.row += 1

        self.column = 0
        while self.column * self.cell_attr.side < self.rect.width:
            self.column += 1

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

        if self.list_live_cell_points:
            for point_cell in self.list_live_cell_points:
                rect(self.screen, self.cell_attr.color, (*point_cell, self.cell_attr.side, self.cell_attr.side))

        if self.cell_attr.point_on_top_of:
            rect(self.screen, 'black', (*self.cell_attr.point_on_top_of, self.cell_attr.side, self.cell_attr.side), self.cell_attr.width_border_on_top_of)

    def listen_points_on_top_of_and_select_live_cells(self):
        for row in self.list_intersection_points:
            for point_inter in row:
                if point_inter[0] < get_pos()[0] < point_inter[0] + self.cell_attr.side and point_inter[1] < get_pos()[1] < point_inter[1] + self.cell_attr.side:
                    self.cell_attr.point_on_top_of = point_inter
                    if get_pressed()[0]:
                        if self.cell_attr.one_time_clicked:
                            self.cell_attr.one_time_clicked = False
                            if point_inter in self.list_live_cell_points:
                                self.list_live_cell_points.remove(point_inter)
                            else:
                                self.list_live_cell_points.append(point_inter)
                    else:
                        self.cell_attr.one_time_clicked = True

    def reconfigure_position_and_side_measure(self, value):
        if 10 < self.cell_attr.side and value < 0 or self.cell_attr.side < 60 and value > 0:
            self.cell_attr.side += value
        self.calculate_disposition_of_grid()

