from pygame import Rect
from pygame.draw import rect
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
        self.rect = self.screen_rect.copy()
        self.x_center = self.rect.width / 2
        self.y_center = self.rect.height / 2

        self.row = None
        self.column = None
        self.list_intersection_points = None

        # cell
        self.list_live_cell_points = []

    def calculate_disposition_of_grid(self):

        # initialize the variables
        self.list_intersection_points = []

        # find a xs and ys for form interception points
        xs = [self.x_center]
        for i in [1, -1]:
            x_variable = self.x_center
            side_cell = self.cell_attr.side * i
            while (x_variable < self.screen_rect.width and i == 1) or (x_variable > 0 and i == -1):
                x_variable += side_cell
                xs.append(x_variable)

        ys = [self.y_center]
        for i in [1, -1]:
            y_variable = self.y_center
            side_cell = self.cell_attr.side * i
            while (y_variable < self.screen_rect.height and i == 1) or (y_variable > 0 and i == -1):
                y_variable += side_cell
                ys.append(y_variable)

        for x in xs:
            for y in ys:
                self.list_intersection_points.append([x, y])

    def draw_grip_and_live_cells(self):
        for points in self.list_intersection_points:
            rect(self.screen, 'black', (*points, self.cell_attr.side, self.cell_attr.side), width=1)

        if self.list_live_cell_points:
            for point_cell in self.list_live_cell_points:
                rect(self.screen, self.cell_attr.color, (*point_cell, self.cell_attr.side, self.cell_attr.side))

        if self.cell_attr.point_on_top_of:
            rect(self.screen, 'black', (*self.cell_attr.point_on_top_of, self.cell_attr.side, self.cell_attr.side),
                 self.cell_attr.width_border_on_top_of)

    def listen_points_on_top_of_and_select_live_cells(self):
        for point_inter in self.list_intersection_points:
            if point_inter[0] < get_pos()[0] < point_inter[0] + self.cell_attr.side and \
                    point_inter[1] < get_pos()[1] < point_inter[1] + self.cell_attr.side:
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
            self.update_points_live_cells(self.cell_attr.side - value, self.cell_attr.side)

    def update_points_live_cells(self, old_side=1, new_side=1):
        list_points_updated_live_cell = []

        for point in self.list_live_cell_points:
            vector = [self.x_center - point[0], self.y_center - point[1]]
            list_points_updated_live_cell.append([-vector[0] * new_side / old_side + self.x_center,
                                                  -vector[1] * new_side / old_side + self.y_center])

        self.list_live_cell_points = list_points_updated_live_cell

    def move(self, vector):
        self.x_center += vector[0]
        self.y_center += vector[1]

        self.calculate_disposition_of_grid()

        if self.list_live_cell_points:
            list_live_cell_points = []
            for point in self.list_live_cell_points:
                list_live_cell_points.append([vector[0] + point[0], vector[1] + point[1]])
            self.list_live_cell_points = list_live_cell_points












