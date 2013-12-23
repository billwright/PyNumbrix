__author__ = 'bwright'

class Checkpoint:

    def __init__(self, board_state, alternate_paths):
        self.board_state = board_state
        self.alternate_paths = alternate_paths

    def __str__(self):
        return "Checkpoint(" + str(len(self.alternate_paths)) + " alt. paths)"

    def __repr__(self):
        return self.__str__()

    def get_board_state(self):
        return self.board_state

    def pop_next_path(self):
        return self.alternate_paths.pop()

    def out_of_paths(self):
        return len(self.alternate_paths) == 0