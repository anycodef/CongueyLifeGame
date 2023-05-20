from pygame import QUIT
from pygame.display import flip
from pygame.time import Clock
from pygame.event import get as get_event

from pygame import KEYDOWN, KEYUP, K_PLUS, K_LESS

from code.Globals.constants import exit_code

from code.units import PackageCell


class BasicState:
    def __init__(self, screen, color_background):
        self.screen = screen
        self.rect = self.screen.get_rect()

        self.FPS = 60
        self.tick_ = Clock().tick

        self.color_background = color_background

        self.class_state_return = None

    def show(self):
        self.screen.fill(self.color_background)


class GameLifeCongueyState(BasicState):
    def __init__(self, screen):
        BasicState.__init__(self, screen, 'white')

        self.pack_cells = PackageCell(screen)
        self.pack_cells.find_pos_and_instance_cells()

        self.play = False

    def run(self):
        while not self.class_state_return:
            self.show()  # code flip basic state

            if self.play:
                self.pack_cells.automatic()
            else:
                self.pack_cells.no_automatic()

            # show package cells
            self.pack_cells.run()

            for event in get_event():
                if event.type == QUIT:
                    self.class_state_return = exit_code
                # meanwhile
                if event.type == KEYDOWN:
                    if event.key == K_PLUS:
                        print("PLUSS")
                        self.pack_cells.reconfig(5)
                    if event.key == K_LESS:
                        print("LESS")
                        self.pack_cells.reconfig(-5)

            flip()
            self.tick_(self.FPS)

        return self.class_state_return

