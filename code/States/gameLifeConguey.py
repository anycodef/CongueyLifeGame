from pygame import QUIT
from pygame.display import flip
from pygame.time import Clock
from pygame.event import get as get_event

from pygame import KEYDOWN, KEYUP
from pygame import K_LEFT, K_RIGHT, K_DOWN, K_UP, K_ESCAPE, K_SPACE

from code.Globals.constants import exit_code

from code.units import DynamicGrid


class BasicState:
    def __init__(self, screen, color_background):
        self.screen = screen
        self.rect = self.screen.get_rect()

        self.FPS = 10
        self.tick_ = Clock().tick

        self.color_background = color_background

        self.class_state_return = None

    def show(self):
        self.screen.fill(self.color_background)


class GameLifeCongueyState(BasicState):
    def __init__(self, screen):
        BasicState.__init__(self, screen, 'white')

        self.dynamic_grid = DynamicGrid(self.screen)
        self.dynamic_grid.calculate_disposition_of_grid()

        self.vect_move = [0, 0]

        self.play = False

    def run(self):
        while not self.class_state_return:
            self.show()  # code flip basic state

            if self.play:
                self.dynamic_grid.automatic_run()
            else:
                self.dynamic_grid.listen_points_on_top_of_and_select_live_cells()

            self.dynamic_grid.draw_grip_and_live_cells()

            if self.vect_move[0] or self.vect_move[1]:
                self.dynamic_grid.move(self.vect_move)

            for event in get_event():
                if event.type == QUIT:
                    self.class_state_return = exit_code
                # meanwhile
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.play = not self.play
                    if event.key == K_ESCAPE:
                        self.class_state_return = exit_code
                    if event.unicode == '+':
                        self.dynamic_grid.reconfigure_position_and_side_measure(5)
                    if event.unicode == '-':
                        self.dynamic_grid.reconfigure_position_and_side_measure(-5)
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

            flip()
            self.tick_(self.FPS)

        return self.class_state_return

