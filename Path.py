__author__ = 'bwright'

class Path:

    def __init__(self, path, increment=1):
        if isinstance(path, Path):
            self.path = list(path.get_path())   # Make copy of path list
            self.increment = path.get_increment()
        else:
            self.path = path
            self.increment = increment

    def get_path(self):
        return self.path

    def get_increment(self):
        return self.increment

    def size(self):
        return len(self.path) - 1

    def last_node(self):
        return self.path[-1]

    def add_node(self, node):
        self.path.append(node)

    def __iter__(self):
        return self.path.__iter__()