from pygame import Rect
from pygame.mouse import get_pos
from code.widgets.Bar.speedController import SpeedController


class HorizontalBar:
    def __init__(self, screen, rect_father, fps_grid_current, list_fps_grid):
        self.rect_father = rect_father

        self.rect = Rect(self.rect_father.x, self.rect_father.y + self.rect_father.height - 60, rect_father.width, 60)

        self.speed_controller = SpeedController(screen, self.rect, fps_grid_current, list_fps_grid)

        self.speed_hiding_y = -1

    def run(self):
        if self.rect.y < self.rect_father.y + self.rect_father.height:
            self.show()
        self.listen_position_mouse()
        self.updating_position()

    def show(self):
        self.speed_controller.show()

    def updating_position(self):
        self.speed_controller.updating_position()

    def listen_position_mouse(self):
        if self.rect_father.x <= get_pos()[0] <= self.rect_father.x + self.rect_father.width and \
                self.rect_father.y + self.rect_father.height - self.rect.height <= get_pos()[1] <= \
                self.rect_father.y + self.rect_father.height:
            if self.rect.y <= self.rect_father.y + self.rect_father.height - self.rect.height:
                self.rect.y = self.rect_father.y + self.rect_father.height - self.rect.height
            else:
                self.rect.y += self.speed_hiding_y

            self.speed_controller.listen_grade_mouse()

        else:
            if self.rect.y >= self.rect_father.y + self.rect_father.height:
                self.rect.y = self.rect_father.y + self.rect_father.height
            else:
                self.rect.y -= self.speed_hiding_y

    def return_fps(self):
        return self.speed_controller.fps_current
