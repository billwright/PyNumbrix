__author__ = 'bwright'
import math
import Cell
import Link
import Checkpoint

class Numbrix:
    def __init__(self, size, cell_dimension, state=[]):
        self.size = size
        self.cell_dimension = cell_dimension
        self.board = []
        self.check_points = []
        self.backtrack_count = 0
        self.create_board(state)

    def create_board(self, state):
        self.board = []
        pos = 0
        for row in range(self.size):
            new_row = []
            for col in range(self.size):
                new_cell = Cell.Cell(row, col, None)
                new_row.append(new_cell)
            self.board.append(new_row)

        self.load_state(state)

    def load_full_state(self, state):
        state_index = 0
        for row in self.board:
            for cell in row:
                cell.reset_value(state[state_index])
                state_index += 1

    def load_short_state(self, state):
        self.board[0][0].set_value(state[0])
        self.board[0][2].set_value(state[1])
        self.board[0][4].set_value(state[2])
        self.board[0][6].set_value(state[3])
        self.board[0][8].set_value(state[4])

        self.board[2][0].set_value(state[5])
        self.board[2][8].set_value(state[6])

        self.board[4][0].set_value(state[7])
        self.board[4][8].set_value(state[8])

        self.board[6][0].set_value(state[9])
        self.board[6][8].set_value(state[10])

        self.board[8][0].set_value(state[11])
        self.board[8][2].set_value(state[12])
        self.board[8][4].set_value(state[13])
        self.board[8][6].set_value(state[14])
        self.board[8][8].set_value(state[15])

    def load_state(self, state):
        if len(state) == 16:
            self.load_short_state(state)
        else:
            self.load_full_state(state)
        self.set_neighbors()

    def unsolvable_state(self):
        # Returns true of the board is in an unsolvable state. This looks for the situations shown here:
        #
        #               0         1         2         3         4         5         6         7         8
        # ------------------------------------------------------------------------------------------------
        # Row 0:        13        14        15        16        17        20        21        24        25
        # Row 1:        12        11      None      None        18        19        22        23        26
        # Row 2:         9        10        33        32        31        30        29        28        27
        # Row 3:         8         7        34        45        46        47        48        49        50
        # Row 4:        37        36        35        44        43      None      None        52        51
        # ...
        # Row 7:        52        49        44        43        42      None      None        35        36
        # Row 8:        51        50        45      None        41        40        39        38        37

        #
        # Note that cell (3,1) has 7 in it and all neighbors are filled in, but none are a 6.
        # Note that cell (8,3) is None but has no possible value that can satisfy the puzzle.
        for row in self.board:
            for cell in row:
                if cell.get_value() is not None and cell.get_value() != 1 and cell.get_value() != 81:
                    if len(cell.unknown_neighbors()) == 0:
                        neighbor_values = cell.known_neighbor_values()
                        if ((cell.get_value() + 1) not in neighbor_values) or ((cell.get_value() - 1) not in neighbor_values):
                            return True     # The state is unsolvable
        return False    # The state can be solved

    def __repr__(self):
        return "Numbrix({0}, {1}, {2} cells filled)".format(str(self.size), str(self.dimension),
                                                            str(len(self.used_values())))

    def __str__(self):
        board_str = '     '
        for n in range(self.size):
            board_str += str(n).rjust(10)
        board_str += '\n'
        board_str += '------'
        for n in range(self.size):
            board_str += '-'.rjust(10, '-')
        board_str += '\n'
        rowNum = 0
        for row in self.board:
            board_str += "Row " + str(rowNum) + ":"
            for cell in row:
                board_str += str(cell.get_value()).rjust(10)
            board_str += '\n'
            rowNum += 1
        board_str += "Total cells filled: " + str(len(self.used_values())) + "\n"
        board_str += "Chains are: " + str(self.get_chains()) + "\n"
        board_str += "End points are: " + str(self.get_chain_end_points()) + "\n"
        board_str += "Missing links are: " + str(self.get_missing_links()) + "\n"
        board_str += "Smallest link is: " + str(self.get_smallest_link()) + "\n"
        board_str += "Number of current checkpoints are: " + str(len(self.check_points)) + "\n"
        board_str += "Number of backtracks so far: " + str(self.backtrack_count) + "\n"
        return board_str

    def get_board_state(self):
        state = []
        for row in self.board:
            for cell in row:
                state.append(cell.get_value())
        return state

    def set_value(self, position, value):
        cell = self.board[position[0]][position[1]]
        cell.set_value(value)

    def test_fill(self):
        num = 1
        for row in range(self.size):
            for col in range(self.size):
                self.board[row][col] = num
                num += 1

    def get_cell(self, row, col):
        return self.board[row][col]

    def set_neighbors_for_cell(self, cell, row, col, used_values):
        neighbors = []
        if row != 0:
            neighbors.append(self.board[row-1][col])
        if row < self.size-1:
            neighbors.append(self.board[row+1][col])
        if col != 0:
            neighbors.append(self.board[row][col-1])
        if col < self.size-1:
            neighbors.append(self.board[row][col+1])
        cell.set_neighbors(neighbors, used_values)

    def fill_forced(self):
        # Check for neighbors that are two away from each other
        for row in self.board:
            for cell in row:
                if cell.get_value() is None and cell.get_possible_values().has_only_one():
                    cell.set_value(cell.get_possible_values().get_value())

        # Check for one unknown neighbor with one neighbor one away
        for row in self.board:
            for cell in row:
                unknown_neighbors = cell.unknown_neighbors()
                one_neighbors = cell.one_away_neighbors()
                if cell.get_value() is None and len(one_neighbors) == 2:
                    # Check for unknown cells with two one-away neighbors
                    difference = math.fabs(one_neighbors[1].get_value() - one_neighbors[0].get_value())
                    min_neighbor_value = min(one_neighbors[1].get_value(), one_neighbors[0].get_value())
                    new_value = int(min_neighbor_value + difference // 2)
                    print("Cell", cell, "has 2 1-away neighbors and its value should therefore be", new_value)
                    cell.set_value(new_value)

                if len(unknown_neighbors) == 1:
                    print("cell", cell, "has one unknown neighbor")
                    if len(one_neighbors) == 1 and cell.get_value() != 1 and cell.get_value() != 81:
                        print("    - and it has just one neighbor one away")
                        neighbor_value = cell.one_away_unknown_neighbor_value()
                        print("        - and the value of the unknown cell is", neighbor_value)
                        cell.unknown_neighbor().set_value(neighbor_value)

    def fill_forced_until_done(self):
        previous_used_value_count = 0
        while len(self.used_values()) > previous_used_value_count:
            previous_used_value_count = len(self.used_values())
            self.update_possible_values()
            self.fill_forced()

            print("After forced filling:")
            print(self)

    def used_values(self):
        used_vals = []
        for row in self.board:
            for cell in row:
                if cell.get_value() is not None:
                    used_vals.append(cell.get_value())
        used_vals.sort()
        return used_vals

    def get_chains(self):
        chains = []
        start = None
        end = None
        for val in self.used_values():
            if start is None:
                start = val
            elif end is None:
                if val == start + 1:
                    end = val
                else:
                    chains.append(range(start, start+1))
                    start = val
            elif val == end + 1:
                # Extend current chain
                end = val
            else:
                # Previous chain has ended and a new chain is starting. We indicate a started chain by
                # setting end to None
                #if val == (self.size * self.size):
                #    chains.append(range(start, end+2))
                #else:
                    chains.append(range(start, end+1))
                    start = val
                    end = None

        # Close last open chain
        chains.append(range(start, val+1))

        return chains

    def get_chain_end_points(self):
        end_points = set()
        first_chain = True
        found_1 = False
        found_81 = False
        for chain in self.get_chains():
            if chain[0] == 1 or chain[-1] == 1:
                found_1 = True
            if chain[0] == 81 or chain[-1] == 81:
                found_81 = True
            #if first_chain and chain[0] != 1:
            #        # Then we need to add zero as an end-point to indicate we don't have 1 yet.
            #        end_points.add(0)
            if chain[0] != 1:
                    end_points.add(chain[0])

            #if chain[-1] != 81:
            end_points.add(chain[-1])
            #first_chain = False

        if not found_1:
            end_points.add(0)
        if not found_81:
            end_points.add(82)

        sorted_end_points = list(end_points)
        sorted_end_points.sort()
        return sorted_end_points

    def get_cell_with_value(self, desired_value):
        if desired_value is None:
            return None

        for row in self.board:
            for cell in row:
                if cell.get_value() == desired_value:
                    return cell
        return None

    def get_missing_links(self):
        chains = self.get_chains()
        list_tuples = Link.create_link_tuples_from_chains(chains)

        missing_links = []
        for list_tuple in list_tuples:
            missing_links.append(Link.Link(self.get_cell_with_value(list_tuple[0]), self.get_cell_with_value(list_tuple[-1])))

        return missing_links

    def get_missing_links_old(self):
        missing_links = []
        end_points = self.get_chain_end_points()
        for index in range(len(end_points) - 1):
            if end_points[index] == 0:
                    missing_links.append(Link.Link(None, self.get_cell_with_value(end_points[index+1])))
            #elif end_points[index+1] != 81:
            else:
                    missing_links.append(Link.Link(self.get_cell_with_value(end_points[index]), self.get_cell_with_value(end_points[index+1])))

        if len(end_points) > 0 and end_points[-1] != 81:
            missing_links.append(Link.Link(self.get_cell_with_value(end_points[-1]), None))

        return missing_links

    def get_smallest_link(self):
        smallest_link = None
        for link in self.get_missing_links():
            #if (smallest_link is None or link.size() < smallest_link.size()) and link.get_lower_value() != 1 and link.get_higher_value() != 81:
            if smallest_link is None or link.size() < smallest_link.size():
                smallest_link = link
        return smallest_link

    def fill_in_link(self, link):
        next_value = None

        for cell in link:
            if cell.get_value() is not None:
                next_value = cell.get_value() + link.get_increment()
            else:
                cell.set_value(next_value)
                next_value += link.get_increment()

    def is_done(self):
        return len(self.used_values()) == 81

    def update_possible_values(self):
        for row in self.board:
            for cell in row:
                cell.set_possible_values(self.used_values())

    def set_neighbors(self):
        used_values = self.used_values()
        for row in range(self.size):
            for col in range(self.size):
                self.set_neighbors_for_cell(self.board[row][col], row, col, used_values)

    def fill_in_one_unknown_neighbors(self):
        print("In fill_in_one_unknown_neighbors")
        for row in range(self.size):
            for col in range(self.size):
                self.get_cell(row, col).check_for_one_unknown_neighbor_for_cell(row, col)

    def all_values(self):
        values = []
        for row in self.board:
            values.extend([n.value for n in row])
        values.sort()
        return values

    def solve(self):
        while not self.is_done():
            self.fill_forced_until_done()

            smallest_link = self.get_smallest_link()
            if smallest_link is None:
                continue
            smallest_link_paths = smallest_link.find_paths()
            if len(smallest_link_paths) > 0:
                if len(smallest_link_paths) > 1:
                    print("I have multiple successful paths - " + str(len(smallest_link_paths)) + " of them")
                    print("Creating a possible checkpoint and searching for a solvable state from successful paths")
                    new_checkpoint = Checkpoint.Checkpoint(self.get_board_state(), smallest_link_paths)

                    self.find_solvable_state_from_checkpoint(new_checkpoint)

                    if not new_checkpoint.out_of_paths():
                        print("SETTING A CHECKPOINT!")
                        self.check_points.append(new_checkpoint)
                else:
                    print("I found only one successful path, so I'm taking it")
                    self.fill_in_link(smallest_link_paths[0])
            else:
                print("MUST BACK-UP! Found no paths from current board state")
                self.backtrack_count += 1
                last_checkpoint = self.check_points[-1]

                self.find_solvable_state_from_checkpoint(last_checkpoint)

                # If that was the last viable path, then we are done with this checkpoint and can remove it
                if last_checkpoint.out_of_paths():
                    self.check_points.pop()

    def find_solvable_state_from_checkpoint(self, check_point):
        # Modifies the board state to the first path from the checkpoint that has a solvable state

        unsolvable_state = True
        while unsolvable_state and not check_point.out_of_paths():
            # Restore board state to decision point
            self.load_state(check_point.get_board_state())
            print("Rolled back state:")
            print(self)

            # Get the next viable path and check that it is solvable
            chosen_link = check_point.pop_next_path()
            self.fill_in_link(chosen_link)

            # Fill is forced moves also, as this can make checking for an unsolvable state easier - we find it quicker
            self.fill_forced_until_done()

            print("Trying this link to see if it is solvable:")
            print(self)
            unsolvable_state = self.unsolvable_state()
            if unsolvable_state:
                print("Dang, that wasn't solvable, trying the next one")
                self.backtrack_count += 1
            else:
                print("Found solvable state:")
                print(self)

        return unsolvable_state

    def draw(self, canvas, pos):
        board_dimension = self.cell_dimension * self.size

        # Draw outline
        canvas.draw_polygon([pos,
                             (pos[0] + board_dimension, pos[1]),
                             (pos[0] + board_dimension, pos[1] + board_dimension),
                             (pos[0], pos[1] + board_dimension)], 2, 'Black', 'Green')

        y_value = pos[1]
        for row in self.board:
            y_value += self.cell_dimension
            canvas.draw_line((pos[0], y_value), (board_dimension + pos[0], y_value), 2, 'Black')

        x_value = pos[0]
        for row in self.board:
            x_value += self.cell_dimension
            canvas.draw_line((x_value, pos[1]), (x_value, board_dimension + pos[1]), 2, 'Black')

        pos_y = pos[1] + self.cell_dimension // 2
        for row in self.board:
            pos_x = pos[0] + self.cell_dimension // 2
            for cell in row:
                #cell_str = str(cell)
                #if cell == None:
                #    cell_str = ''
                #canvas.draw_text(cell_str, (pos_x, pos_y), FONT_DIMENSION, "Blue")
                cell.draw(canvas, (pos_x, pos_y), self.cell_dimension)
                pos_x += self.cell_dimension
            pos_y += self.cell_dimension