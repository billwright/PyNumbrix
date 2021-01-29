__author__ = 'bwright'

import math
import PossibleValues

class Cell:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.neighbors = []
        self.possible_values = PossibleValues.PossibleValues()
        self.given = True
        if value is None:
            self.given = False

    def __str__(self):
        return "Cell(" + str(self.row) + "," + str(self.col) + ")=" + str(self.value)

    def __repr__(self):
        return "Cell(" + str(self.row) + "," + str(self.col) + ")=" + str(self.value)

    def set_value(self, value):
        if (self.value is not None and (value > 81 or value < 1 or type(value) != int)):
            print("ERROR: trying to set cell", str(self), "to", value)
        else:
            print("Setting cell", str(self), "to", value)
            self.value = value

    def reset_value(self, value):
        # This method doesn't check for overwriting of cell value
        self.value = value

    def get_value(self):
        return self.value

    def set_neighbors(self, neighbors, used_values):
        self.neighbors = neighbors
        self.set_possible_values(used_values)

    def known_neighbors(self):
        return [n for n in self.neighbors if n.value is not None]

    def known_neighbor_values(self):
        return [n.get_value() for n in self.known_neighbors()]

    def unknown_neighbors(self):
        return [n for n in self.neighbors if n.value is None]

    def unknown_neighbor(self):
        if len(self.unknown_neighbors()) == 0:
            return None
        return self.unknown_neighbors()[0]

    def has_one_unknown_neighbor(self):
        return len(self.unknown_neighbors()) == 1

    def one_away_neighbors(self):
        if self.value is None:
            return []
        one_neighbors = [n for n in self.neighbors if n.value is not None]
        return [n for n in one_neighbors if math.fabs(n.value - self.value) == 1]

    def one_away_unknown_neighbor_value(self):
        difference = self.one_away_neighbors()[0].get_value() - self.value
        return self.value - difference

    def set_value_to_next_neighbor(self):
        possible_values = self.get_possible_values()
        if possible_values.size() > 0:
            self.value = possible_values[0]

    def get_possible_values(self):
        return self.possible_values

    def has_neighbor_with_value(self, desired_value):
        for cell in self.neighbors:
            if cell.get_value() == desired_value:
                return True
        return False

    def set_possible_values(self, used_values):
        num_rows = 9
        self.possible_values.clear(used_values)
        for cell in self.neighbors:
            if cell.value is None:
                self.possible_values.add_unknown()
            else:
                if cell.value == 1:
                    self.possible_values.add_value(num_rows * num_rows)
                else:
                    self.possible_values.add_value(cell.get_value() - 1)
                if cell.value == num_rows * num_rows:
                    self.possible_values.add_value(1)
                else:
                    self.possible_values.add_value(cell.get_value() + 1)


    def draw(self, canvas, position, cell_dimension):
        font_size = cell_dimension // 3
        neighbor_font_size = font_size // 2

        display_value = str(self.value)
        if self.value is None:
            display_value = ''
        font_color = "Blue"
        if self.has_one_unknown_neighbor() and len(self.one_away_neighbors()) == 1:
            font_color = "White"
        if self.value is None and len(self.one_away_neighbors()) == 2:
            font_color = "White"
        canvas.draw_text(display_value, position, font_size, font_color)
        if self.value is None:
            neighbor_text = str(self.possible_values)
            text_length = len(neighbor_text)
            neighbor_pos = (position[0] - (neighbor_font_size * text_length // 4), position[1] + font_size)
            canvas.draw_text(neighbor_text, neighbor_pos, neighbor_font_size, "Blue")

