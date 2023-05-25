from pygame.draw import rect
from pygame import Rect

from pygame.mouse import get_pos, get_pressed


class SpeedController:
    def __init__(self, screen, rect_father, fps_current, fps_list):

        self.screen = screen

        self.fps_current = fps_current
        self.fps_list = fps_list

        self.color_bar = 'white'
        self.color_bar_fill = 'dark green'

        self.rect_father = rect_father
        self.rect_bar = Rect(self.rect_father.x + 30, self.rect_father.y + (self.rect_father.height - 10) / 2, 240, 10)
        self.side_grade = self.rect_bar.width / self.fps_list.__len__()

        self.points_grade = [[self.rect_bar.x, self.rect_bar.y]]

        for i in range(self.fps_list.__len__()):
            self.points_grade.append(
                [self.points_grade[i][0] + self.side_grade, self.rect_bar.y])
        self.points_grade = self.points_grade[1:]

        self.rect_bar_fill = Rect(self.rect_bar.x, self.rect_bar.y, self.points_grade[self.fps_list.index(self.fps_current)][0] - self.rect_bar.x, 10)

    def show(self):
        rect(self.screen, self.color_bar, self.rect_bar)
        rect(self.screen, self.color_bar_fill, self.rect_bar_fill)

    def updating_position(self):
        self.rect_bar.y = self.rect_father.y + (self.rect_father.height - self.rect_bar_fill.height) / 2
        self.rect_bar_fill.y = self.rect_bar.y

    def listen_grade_mouse(self):
        for i, points in list(enumerate(self.points_grade)):
            # modify a level var
            if points[0] - self.side_grade <= get_pos()[0] <= points[0] and \
                    points[1] <= get_pos()[1] <= points[1] + self.rect_bar_fill.height:

                # draw preview of the selected part
                rect(self.screen, 'black', (self.rect_bar_fill.x, self.rect_bar_fill.y, points[0] - self.rect_bar_fill.x, self.rect_bar_fill.height), width=1)

                if get_pressed()[0]:
                    self.rect_bar_fill.width = points[0] - self.rect_bar_fill.x
                    self.fps_current = self.fps_list[i]

