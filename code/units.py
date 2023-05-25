from pygame.draw import rect
from pygame.mouse import get_pos, get_pressed
from pygame.event import get as get_event

from pygame import KEYDOWN, KEYUP, K_SPACE
from pygame import K_LEFT, K_RIGHT, K_DOWN, K_UP


class Cell:
    def __init__(self):
        self.side = 50
        self.color = 'green'
        self.point_on_top_of = None
        self.width_border_on_top_of = 2

        # on click
        self.one_time_clicked = True


class DynamicGrid:
    def __init__(self, screen, rect_surface_pather):
        self.screen = screen
        self.screen_rect = rect_surface_pather

        # fps
        self.FPS_list = [4, 10, 15, 20, 30, 60, 120]
        self.fps = 20
        self.time_count = 0

        # vector move
        self.vect_move = [0, 0]

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

        # state
        self.play = False

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
            if -self.cell_attr.side <= points[0] <= self.screen_rect.width + self.cell_attr.side and \
                    -self.cell_attr.side <= points[1] <= self.screen_rect.height + self.cell_attr.side:
                rect(self.screen, 'black', (*points, self.cell_attr.side, self.cell_attr.side), width=1)

        if self.list_live_cell_points:
            for point_cell in self.list_live_cell_points:
                if -self.cell_attr.side <= point_cell[0] <= self.screen_rect.width + self.cell_attr.side and \
                        -self.cell_attr.side <= point_cell[1] <= self.screen_rect.height + self.cell_attr.side:
                    rect(self.screen, self.cell_attr.color, (*point_cell, self.cell_attr.side, self.cell_attr.side))
                    rect(self.screen, 'black', (*point_cell, self.cell_attr.side, self.cell_attr.side), width=1)

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

    def move(self):
        if self.vect_move[0] or self.vect_move[1]:
            self.x_center += self.vect_move[0]
            self.y_center += self.vect_move[1]

            self.calculate_disposition_of_grid()

            if self.list_live_cell_points:
                list_live_cell_points = []
                for point in self.list_live_cell_points:
                    list_live_cell_points.append([self.vect_move[0] + point[0], self.vect_move[1] + point[1]])
                self.list_live_cell_points = list_live_cell_points

        for event in get_event():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.play = not self.play
                if event.unicode == '+':
                    self.reconfigure_position_and_side_measure(5)
                if event.unicode == '-':
                    self.reconfigure_position_and_side_measure(-5)
                if event.key == K_UP and self.vect_move[1] <= 0:
                    self.vect_move[1] = 5
                elif event.key == K_DOWN and self.vect_move[1] >= 0:
                    self.vect_move[1] = -5
                elif event.key == K_LEFT and self.vect_move[0] >= 0:
                    self.vect_move[0] = 5
                elif event.key == K_RIGHT and self.vect_move[0] <= 0:
                    self.vect_move[0] = -5
            elif event.type == KEYUP:
                if (event.key == K_UP and self.vect_move[1] > 0) or \
                        (event.key == K_DOWN and self.vect_move[1] < 0):
                    self.vect_move[1] = 0
                elif (event.key == K_LEFT and self.vect_move[0] > 0) or \
                        (event.key == K_RIGHT and self.vect_move[0] < 0):
                    self.vect_move[0] = 0

    def automatic_run(self):

        # step 1
        list_point_cell_influenced = []
        for point_live_cell in self.list_live_cell_points:
            for x in [-self.cell_attr.side, 0, self.cell_attr.side]:
                for y in [-self.cell_attr.side, 0, self.cell_attr.side]:
                    if x or y:
                        list_point_cell_influenced.append([point_live_cell[0] + x, point_live_cell[1] + y])

        # step 2
        list_point_unique = []
        for point in list_point_cell_influenced:
            if point not in list_point_unique:
                list_point_unique.append(point)

        list_list_point_num_repeat = []
        for unique_point in list_point_unique:
            list_list_point_num_repeat.append([unique_point, list_point_cell_influenced.count(unique_point)])

        # step 3
        new_list_live_cell_points = []
        for point, num_weight in list_list_point_num_repeat:
            if (point in self.list_live_cell_points and (num_weight in [2, 3])) or \
                    (point not in self.list_live_cell_points and num_weight == 3):
                new_list_live_cell_points.append(point)

        # step 4
        self.list_live_cell_points = new_list_live_cell_points

    def run(self, fps_system, list_rect_no_listen_pos_mouse):
        # controller of the grid situation
        if self.play:
            if self.time_count >= fps_system / self.fps:
                self.automatic_run()
                self.time_count = 0
            else:
                self.time_count += 1
        else:
            # listen the position of mouse if not is the bar.
            for rect_exclusion in list_rect_no_listen_pos_mouse:
                if rect_exclusion.x + rect_exclusion.height <= get_pos()[0] <= rect_exclusion.x and \
                        rect_exclusion.y + rect_exclusion.height <= get_pos()[1] <= rect_exclusion.y:
                    self.listen_points_on_top_of_and_select_live_cells()

        self.draw_grip_and_live_cells()

