__author__ = 'bwright'

import Path


# Helper function. Tried to make this a static method (see below), but couldn't call it outside of this file for
# some unknown reason
def create_link_tuples_from_chains(chains):
    # Returns a list of tuples with the cell value start and end points - cells need to be retrieved from board
    # at higher level

    links = []
    first_link_of_first_chain = chains[0][0]
    if first_link_of_first_chain != 1:
        # If first chain doesn't start with one, then we need a link from one (None, since we don't know location)
        links.append((None, first_link_of_first_chain))
    for chain_index in range(len(chains) - 1):
        links.append((chains[chain_index][-1], chains[chain_index+1][0]))
    last_link_of_last_chain = chains[-1][-1]
    if last_link_of_last_chain != 81:
        # If the last chain doesn't end at 81, then we need a link to 81 (None, since we don't know location)
        links.append((last_link_of_last_chain, None))
    return links


class Link:
    def __init__(self, low_cell, high_cell):
        self.lower_cell = low_cell
        self.higher_cell = high_cell

    def __repr__(self):
        return "Link(" + str(self.get_lower_value()) + "->" + str(self.get_higher_value()) + ") - size: " + str(self.size())

    @staticmethod
    def create_link_tuples_from_chains(chains):
        # Returns a list of tuples with the cell value start and end points - cells need to be retrieved from board
        # at higher level

        links = []
        first_link_of_first_chain = chains[0][0]
        if first_link_of_first_chain != 1:
            # If first chain doesn't start with one, then we need a link from one (None, since we don't know location)
            links.append((None, first_link_of_first_chain))
        for chain_index in range(len(chains) - 1):
            links.append((chains[chain_index][-1], chains[chain_index+1][0]))
        last_link_of_last_chain = chains[-1][-1]
        if last_link_of_last_chain != 81:
            # If the last chain doesn't end at 81, then we need a link to 81 (None, since we don't know location)
            links.append((last_link_of_last_chain, None))
        return links

    def size(self):
        value = self.get_higher_value() - self.get_lower_value()
        if self.higher_cell is not None and self.lower_cell is not None:
            value -= 1
        return value

    def find_paths(self):
        path = [self.lower_cell]
        search_value = None
        increment = 1
        if self.lower_cell is None:
            path = [self.higher_cell]
            increment = -1
        elif self.higher_cell is not None:
            search_value = self.get_higher_value()

        return self.extend_path(Path.Path(path, increment), search_value, self.size())

    def extend_path(self, current_path, end_value, depth):
        successful_paths = []
        start = current_path.last_node()
        if depth == 0:
            print("Testing if this path works: " + str(current_path))
            if start.has_neighbor_with_value(end_value):
                # Found the end point!
                print("     Found successful path!")
                return [Path.Path(current_path)]    # In a list, since we always return a list of paths

            # We failed to find the desired endpoint in the required depth - stop searching
            print("     This was a dead end...")
            return None

        for neighbor in start.unknown_neighbors():
            # Make sure we aren't visiting a node already on our path
            if neighbor in current_path:
                continue

            new_path = Path.Path(current_path)
            new_path.add_node(neighbor)
            success_subpaths = self.extend_path(new_path, end_value, depth - 1)
            if success_subpaths is not None:
                successful_paths.extend(success_subpaths)

        print("Done with this path. I found " + str(len(successful_paths)) + " successful paths")

        return successful_paths

    def get_lower_value(self):
        if self.lower_cell:
            return self.lower_cell.get_value()
        else:
            return 1

    def get_higher_value(self):
        if self.higher_cell:
            return self.higher_cell.get_value()
        else:
            return 81
