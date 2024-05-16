from grid import Point


class Node:
    """
    This class represents a node in the grid.

    Attributes:
        state (Point): The current state of the node.
        parent (Node): The parent node of this node.
        action (Action): The action taken by the parent node to get to this node.
        path_cost (int): The cost of the path between this node and the initial node.
    """

    def __init__(self, state, parent, action, path_cost=0):
        """
        Initializes a new Node object.
        :param state: The current state of the node.
        :param parent: The parent node of this node.
        :param action: The action taken by the parent node to get to this node.
        :param path_cost: The cost of the path between this node and the initial node.
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def get_state(self):
        """
        Returns the state of the current node.

        :return: the state of the node as a Point object.
        """
        return self.state

    def find_path(self, node, expanded):
        """
        Finds the solution path from the initial node to the goal node.

        :param node: The solution node.
        :param expanded: the total number of nodes that were expanded during the search.
        :return: A list of points representing the solution path.
        """
        current_node = node
        res_path = []
        cost = node.path_cost
        print("Path cost: " + str(cost))
        print("Nodes expanded: " + str(expanded))
        print("\n")
        while current_node.parent is not None:
            res_path.append(current_node.state)
            cost += current_node.path_cost
            current_node = current_node.parent
        res_path.append(current_node.state)

        return list(reversed(res_path))








