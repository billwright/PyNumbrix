__author__ = 'bwright'


class PossibleValues:
    def __init__(self, used_values=[]):
        self.values = []
        self.used_values = used_values
        self.clear(used_values)

    def __str__(self):
        return str(self.values)

    def add_value(self, new_value):
        self.values.append(new_value)

    def has_only_one(self):
        return len(self.values) == 1

    def get_value(self):
        return self.values[0]

    def add_unknown(self):
        self.values.append('?')

    def clear(self, used_values):
        self.values = []
        self.used_values = used_values

    def size(self):
        return len(self.values)