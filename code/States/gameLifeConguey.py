from pygame import QUIT
from pygame.display import flip
from pygame.time import Clock
from pygame.event import get as get_event
from pygame.mouse import get_pos

from pygame import KEYDOWN
from pygame import K_ESCAPE, K_SPACE

from code.Globals.constants import exit_code

from code.units import DynamicGrid
from code.widgets.Bar.bar import HorizontalBar


class BasicState:
    def __init__(self, screen, color_background):
        self.screen = screen
        self.rect = self.screen.get_rect()

        self.FPS = 120
        self.tick_ = Clock().tick

        self.color_background = color_background

        self.class_state_return = None

    def show(self):
        self.screen.fill(self.color_background)


class GameLifeCongueyState(BasicState):
    def __init__(self, screen):
        BasicState.__init__(self, screen, 'white')

        self.dynamic_grid = DynamicGrid(self.screen, self.screen.get_rect())
        self.dynamic_grid.calculate_disposition_of_grid()

        self.bar = HorizontalBar(screen, screen.get_rect(), self.dynamic_grid.fps, self.dynamic_grid.FPS_list)

        self.list_exclusion_no_listen_get_pos = [self.bar.rect]

    def run(self):
        while not self.class_state_return:
            self.show()  # code flip basic state

            self.dynamic_grid.run(self.FPS, self.list_exclusion_no_listen_get_pos)
            self.bar.run()
            self.dynamic_grid.fps = self.bar.return_fps()

            for event in get_event():
                if event.type == QUIT:
                    self.class_state_return = exit_code
                # meanwhile
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.class_state_return = exit_code

            flip()
            self.tick_(self.FPS)

        return self.class_state_return

