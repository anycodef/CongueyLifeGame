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

    def reconfig(self, valor):
        self.rect.x += valor / 2
        self.rect.y += valor / 2
        self.rect.width -= valor
        self.rect.height -= valor

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
        self.screen = screen
        self.rect_screen = screen.get_rect()

        self.padding = -50
        self.color_background = 'orange'

        # This rect not is modified
        self.rect = Rect(self.padding, self.padding,
                         self.rect_screen.width - 2 * self.padding, self.rect_screen.height - 2 * self.padding)

        self.rect_dynamic = self.rect

        # initial pos for the first cell
        self.rect_general_cell = Rect(self.padding, self.padding, 50, 50)

        print(f"x: {self.rect_general_cell.x}")
        print(f"y: {self.rect_general_cell.y}")
        print(f"width: {self.rect_general_cell.width}")
        print(f"height: {self.rect_general_cell.height}")

        # algorithms for find the columns and the rows
        # for columns
        cont = 1
        while cont * self.rect_general_cell.width < self.rect_screen.width - 2 * self.padding:
            cont += 1
        self.colum = cont

        # for columns
        cont = 1
        while cont * self.rect_general_cell.height < self.rect_screen.height - 2 * self.padding:
            cont += 1
        self.row = cont

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
                print(f"c: {self.list_cells[i_row].__len__()} -> {self.colum}, r: {self.list_cells.__len__()} -> {self.row}")

                self.list_cells[i_row][i_column].no_automatic()

    def reconfig(self, value):
        for i_row in range(self.row):
            for i_column in range(self.colum):
                self.list_cells[i_row][i_column].reconfig(value)

        self.rect_dynamic.x += value / 2
        self.rect_dynamic.y += value / 2
        self.rect_dynamic.width += value
        self.rect_dynamic.height += value

        self.rect_general_cell.width += value
        self.rect_general_cell.height += value

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

        print(self.list_cells.__len__())
        self.list_cells = [row1] + self.list_cells + [row2]
        print(self.list_cells.__len__())

        self.colum += 2
        self.row += 2

    def run(self):
        dd_row = False
        dd_column = False
        print(self.row)
        for i_row in range(self.row):
            for i_column in range(self.colum):
                self.list_cells[i_row][i_column].show()

        # check if it must add two columns or two rows
        if not dd_column and self.list_cells[0][0].rect.x > self.rect_screen.x:
            dd_column = True
        if not dd_row and self.list_cells[0][0].rect.y > self.rect_screen.y:
            dd_row = True

        if dd_row or dd_column:
            self.add_cells()















