from pygame.image import load
from code.Globals.constants import path_root

from pygame.draw import rect
from pygame import Rect

from pygame.mouse import get_pos, get_pressed


class ManageLessAndPlusButton:
    def __init__(self, screen):

        self.screen = screen

        self.space_between_buttons = 10

        self.side_button_normal = 30
        self.side_button_selected = 35
        self.side_button_pressed = 40

        self.buttons_dict = {
            'less': {'rect': Rect(0, 0, self.side_button_normal, self.side_button_normal),
                     'color': 'blue'},

            'plus': {'rect': Rect(0, 0, self.side_button_normal, self.side_button_normal),
                     'color': 'red'}
        }

        self.calculate_position()

        self.name_buttons_pressed = None

    def show(self):
        for _Rect in self.buttons_dict.values():
            rect(self.screen, _Rect['color'], _Rect['rect'], border_radius=3)

    def calculate_position(self):

        y = self.screen.get_rect().height - self.buttons_dict['less']['rect'].height - self.space_between_buttons

        if self.buttons_dict['plus']['rect'].width == self.side_button_normal and self.buttons_dict['less']['rect'].width == self.side_button_normal:
            self.buttons_dict['plus']['rect'].x = self.screen.get_rect().width - 2 * (self.buttons_dict['plus']['rect'].width + self.space_between_buttons)
            self.buttons_dict['plus']['rect'].y = y

            self.buttons_dict['less']['rect'].x = self.screen.get_rect().width - self.buttons_dict['less']['rect'].width - self.space_between_buttons
            self.buttons_dict['less']['rect'].y = y

    def listen_pos_mouse_and_press(self):

        for name, img in self.buttons_dict.items():
            side_button = self.side_button_normal
            if img['rect'].x <= get_pos()[0] <= img['rect'].x + img['rect'].width and \
                    img['rect'].y <= get_pos()[1] <= img['rect'].y + img['rect'].height:
                side_button = self.side_button_selected

                if get_pressed()[0] and not self.name_buttons_pressed:
                    side_button = self.side_button_pressed
                    self.name_buttons_pressed = name
                    print(name)
                else:
                    self.name_buttons_pressed = None

            self.buttons_dict[name]['rect'].x += (self.buttons_dict[name]['rect'].width - side_button) / 2
            self.buttons_dict[name]['rect'].y += (self.buttons_dict[name]['rect'].height - side_button) / 2

            self.buttons_dict[name]['rect'].width = side_button
            self.buttons_dict[name]['rect'].height = side_button













