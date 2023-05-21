from pygame.draw import rect
from pygame import Rect
from pygame.mouse import get_pos, get_pressed

from code.Globals.funcionts import is_on_top_of


class Cell:
    def __init__(self, screen, rect_cell):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.rect = rect_cell
        self.radius = 2

        self.color_dead = 'gray'
        self.color_mouse_here = 'dark gray'
        self.color_live = 'green'
        self.color_cell = self.color_dead

        self.is_live = False
        self.is_active = False

        # algorithms for selected cell
        self.pos_mouse_pressed = None
        # algorithms for selected cell

    def reconfig(self, vect_list_move, value):
        self.rect.x += vect_list_move[0]
        self.rect.y += vect_list_move[1]
        self.rect.width -= value
        self.rect.height -= value

    def automatic(self):
        if self.is_live:
            self.color_cell = self.color_live
        else:
            self.color_cell = self.color_dead

    def no_automatic(self):
        if is_on_top_of(self.rect, get_pos()):
            if not self.is_live:
                self.color_cell = self.color_mouse_here

            # algorithms for selected cell
            if get_pressed()[0]:
                if self.pos_mouse_pressed != get_pos():
                    self.is_live = not self.is_live
                if not self.pos_mouse_pressed:
                    self.pos_mouse_pressed = get_pos()
            else:
                self.pos_mouse_pressed = None
            # algorithms for selected cell

        elif self.is_live:
            self.color_cell = self.color_live
        else:
            self.color_cell = self.color_dead

    def show(self):
        rect(self.screen, self.color_cell, self.rect, border_radius=self.radius)


class PackageCell:
    def __init__(self, screen):

        # main surface
        self.screen = screen
        self.rect_screen = screen.get_rect()

        # imaginary rect
        self.padding = -50
        self.color_background = 'orange'

        # settings cell
        width_cell = 50
        height_cell = 50

        # algorithms for find the columns and the rows
        # for columns
        cont = 1
        while cont * width_cell < self.rect_screen.width - 2 * self.padding or not cont % 2:
            cont += 1
        self.colum = cont

        # for columns
        cont = 1
        while cont * height_cell < self.rect_screen.height - 2 * self.padding or not cont % 2:
            cont += 1
        self.row = cont

        # This rect not is modified
        x_first_cell = (self.rect_screen.width - self.colum * width_cell) / 2
        y_first_cell = (self.rect_screen.height - self.row * height_cell) / 2

        # initial pos for the first cell
        self.rect_general_cell = Rect(x_first_cell, y_first_cell, 50, 50)

        self.rect = Rect(x_first_cell, y_first_cell, self.colum * width_cell, self.row * height_cell)

        self.rect_dynamic = self.rect

        self.list_cells = []       # list bidimensional

    def find_pos_and_instance_cells(self):
        for i_row in range(self.row):
            row_cells = []
            for i_column in range(self.colum):
                row_cells.append(Cell(self.screen, self.rect_general_cell.copy()))
                self.rect_general_cell.x += self.rect_general_cell.width

            self.rect_general_cell.x = self.padding
            self.rect_general_cell.y += self.rect_general_cell.height

            self.list_cells.append(row_cells)

    def automatic(self):
        for i_row in range(self.row):
            for i_column in range(self.colum):
                self.list_cells[i_row][i_column].automatic()

    def no_automatic(self):
        for i_row in range(self.row):
            for i_column in range(self.colum):
                self.list_cells[i_row][i_column].no_automatic()

    def reconfig(self, value):
        row_center = (self.row - 1) / 2 + 1
        column_center = (self.colum - 1) / 2 + 1

        for i_row in range(self.row):
            for i_column in range(self.colum):
                displacement_vector = [(row_center - i_row) * value, (column_center - i_column) * value]
                self.list_cells[i_row][i_column].reconfig(displacement_vector, value)

        self.rect_general_cell.width += value
        self.rect_general_cell.height += value

        self.rect_dynamic.width = self.colum * self.rect.width
        self.rect_dynamic.height = self.row * self.rect.height
        self.rect_dynamic.x = self.list_cells[0][0].rect.x
        self.rect_dynamic.y = self.list_cells[0][0].rect.y

    def add_cells(self):
        height = self.rect_general_cell.height
        width = self.rect_general_cell.width
        x, y = self.rect_dynamic.x - width, self.rect_dynamic.y

        for index, row in enumerate(self.list_cells):
            self.list_cells[index] = [Cell(self.screen, Rect(x, y, width, height))] + row
            self.list_cells[index] += [Cell(self.screen, Rect(self.rect_dynamic.x + self.rect_dynamic.width, y, width, height))]
            y += height

        y = self.rect_dynamic.y - height
        row1 = [Cell(self.screen, Rect(x + i * width, y, width, height)) for i in range(self.list_cells[0].__len__())]

        y += (self.list_cells.__len__() + 1) * height
        row2 = [Cell(self.screen, Rect(x + i * width, y, width, height)) for i in range(self.list_cells[0].__len__())]

        self.list_cells = [row1] + self.list_cells + [row2]

        self.colum += 2
        self.row += 2

    def listen_for_resize(self):
        # check if it must add two columns or two rows
        if self.list_cells[0][0].rect.x >= 0 or \
                self.list_cells[0][0].rect.y >= 0:
            self.add_cells()

    def run(self):
        for i_row in range(self.row):
            for i_column in range(self.colum):
                self.list_cells[i_row][i_column].show()

















