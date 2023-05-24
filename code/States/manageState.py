# system
from sys import exit

from pygame.display import set_mode
from pygame import init as init_all_pygame, quit

# state
from code.States.gameLifeConguey import GameLifeCongueyState

# constants
from code.Globals.constants import exit_code


class Screen:
    def __init__(self):
        self.width = 900
        self.height = 600
        self.obj = set_mode()


class ManagerState:
    def __init__(self):

        init_all_pygame()
        self.screen = Screen()

        self.exitProgram = False

        self.stateClass = GameLifeCongueyState
        self.stateOBJ = None

    def run(self):
        while self.stateClass != exit_code:

            if self.stateClass:
                self.stateOBJ = self.stateClass(self.screen.obj)
                self.stateClass = None

            self.stateClass = self.stateOBJ.run()

        quit()
        exit()









