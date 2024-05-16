import grid
from grid import Point
import utils
from node import Node
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import Polygon
import math


class Searcher:
    """
    This class is a container for several search algorithms.

    Attributes:
        initial (Point): The initial point.
        destination (Point): The destination point
        enclosures (list): A list of Polygon objects representing enclosures.
        turfs (list): A list of Polygon objects representing turfs.
    """

    def __init__(self, initial, destination, enclosures, turfs):
        """
        Initializes a new Searcher object.

        :param initial: The initial point.
        :param destination: The destination point
        :param enclosures: A list of Polygon objects representing enclosures.
        :param turfs: A list of Polygon objects representing turfs.
        """
        self.initial = initial
        self.destination = destination
        self.enclosures = enclosures
        self.turfs = turfs

    def path_cost(self):
        """
        Calculates the default path cost for dfs bfs.

        :return: An integer representing path cost.
        """
        return 1

    def action_cost(self, state, action, result):
        """
        Calculates the action cost from state s taking an action to state s'.

        :param state: The state s.
        :param action: The action taken from state s to state s'.
        :param result: State s'.
        :return: An integer representing action cost from state s to state s'.
        """
        if not self.turf_collision(result):
            return 1
        return 1.5

    def heuristic(self, node):
        """
        Calculates the straight line distance heuristic from node to destination.

        :param node: The node to calculate the heuristic for.
        :return: A floating point number representing the straight line distance from node to destination.
        """
        x1 = node.state.x
        y1 = node.state.y
        x2 = self.destination.x
        y2 = self.destination.y
        pt1 = [x1, y1]
        pt2 = [x2, y2]
        distance = math.dist(pt1, pt2)
        return distance


    def is_cycle(self, child, reached):
        """
        Determines if a new child node has already been reached.

        :param child: The child node.
        :param reached: a set of points that have already been reached.
        :return: True if child has been reached, False otherwise.
        """
        s = child.state
        if s.to_tuple() in reached:
            return True
        return False

    def actions(self, state):
        """
        Returns the actions available to state s.

        :param state: State s.
        :return: A list of actions available to state s.
        """
        actions = ["UP", "RIGHT", "DOWN", "LEFT"]
        return actions

    def result(self, state, action):
        """
        Calculates and returns the new state s' from state s doing an action.

        :param state: State s.
        :param action: A string representation of an action.
        :return: A new state s'.
        """
        x = state.x
        y = state.y
        if action == "UP":
            if y < grid.MAX - 1:
                point = Point(x, y + 1)
                return point
        if action == "RIGHT":
            if x < grid.MAX - 1:
                point = Point(x + 1, y)
                return point
        if action == "DOWN":
            if y > 0:
                point = Point(x, y - 1)
                return point
        if action == "LEFT":
            if x > 0:
                point = Point(x - 1, y)
                return point
        return None

    def enclosure_collision(self, point):
        """
        Checks in the current point collides with an enclosure.

        :param point: A new state that has just been generated.
        :return: True if collision, False otherwise.
        """
        x = point.x
        y = point.y
        test_point = ShapelyPoint(x, y)
        for polygon in self.enclosures:
            is_inside = polygon.contains(test_point)
            touches = polygon.touches(test_point)
            if is_inside or touches:
                return True
        return False

    def turf_collision(self, point):
        """
        Checks in the new state collides with a turf.

        :param point: A new state that has just been generated.
        :return: True if collision, False otherwise.
        """
        x = point.x
        y = point.y
        test_point = ShapelyPoint(x, y)
        for polygon in self.turfs:
            is_inside = polygon.contains(test_point)
            touches = polygon.touches(test_point)
            if is_inside or touches:
                return True
        return False

    def expand(self, node):  # expand method for gbfs and a*
        """
        Expand current node to its children nodes.

        :param node: The node to be expanded.
        :return: Child node objects.
        """
        s = node.state
        for action in self.actions(s):
            s_prime = self.result(s, action)
            if s_prime is not None:  # if point is in bounds
                if not self.enclosure_collision(s_prime): # if point is not touching or inside of an enclosure
                    cost = node.path_cost + self.action_cost(s, action, s_prime)
                    child = Node(s_prime, node, action, cost)
                    yield child

    def expand1(self, node):  # expand method for bfs and dfs
        """
        Expand current node to its children nodes.

        :param node: The node to be expanded.
        :return: Child node objects.
        """
        s = node.state
        for action in self.actions(s):
            s_prime = self.result(s, action)
            if s_prime is not None:
                if not self.enclosure_collision(s_prime):
                    cost = node.path_cost + self.path_cost()
                    child = Node(s_prime, node, action, cost)
                    yield child

    def is_goal(self, state):
        """
        Checks if state of current node is goal state.

        :param state: The state of the current node.
        :return: True if state is goal, False otherwise.
        """
        if state.__eq__(self.destination):
            return True
        return False

    def breadth_first_search(self):
        """
        The Breadth-First Search algorithm.

        :return: Returns the solution path as a list, or nothing if there is no solution.
        """
        print("Breadth-First Search:")
        node = Node(self.initial, None, None, 0)
        if self.is_goal(node.get_state()):
            return node.find_path(node, 1)
        frontier = utils.Queue()
        frontier.push(node)
        reached = set()
        reached.add(self.initial.to_tuple())

        while not frontier.isEmpty():
            node = frontier.pop()

            for child in self.expand1(node):
                s = child.state
                if self.is_goal(s):
                    return child.find_path(child, len(reached) + 1)
                if s.to_tuple() not in reached:
                    reached.add(s.to_tuple())
                    frontier.push(child)
        return None

    def depth_first_search(self):
        """
        The Depth-First Search algorithm.

        :return: Returns the solution path as a list, or nothing if there is no solution.
        """
        print("Depth-First Search:")
        node = Node(self.initial, None, None, 0)
        frontier = utils.Stack()
        frontier.push(node)
        reached = set()
        reached.add(self.initial.to_tuple())

        while not frontier.isEmpty():
            node = frontier.pop()
            if self.is_goal(node.get_state()):
                return node.find_path(node, len(reached))

            for child in self.expand1(node):
                if not self.is_cycle(child, reached):
                    reached.add(child.state.to_tuple())
                    frontier.push(child)
        return None

    def greedy_best_first_search(self):
        """
        The Greedy Best-First Search algorithm.

        :return: Returns the solution path as a list, or nothing if there is no solution.
        """
        print("Greedy Best-First Search:")
        node = Node(self.initial, None, None, 0)
        frontier = utils.PriorityQueue()
        frontier.push(node, self.heuristic(node))
        reached = dict()
        reached[self.initial.to_tuple()] = node

        while not frontier.isEmpty():
            node = frontier.pop()
            if self.is_goal(node.get_state()):
                return node.find_path(node, len(reached))
            for child in self.expand(node):
                s = child.state
                if s.to_tuple() not in reached or child.path_cost < reached[s.to_tuple()].path_cost:
                    reached[s.to_tuple()] = child
                    frontier.update(child, self.heuristic(child))
        return None

    def a_star_search(self):
        """
        The A* Search algorithm.

        :return: Returns the solution path as a list, or nothing if there is no solution.
        """
        print("A* Search:")
        node = Node(self.initial, None, None, 0)
        frontier = utils.PriorityQueue()
        frontier.push(node, node.path_cost + self.heuristic(node))
        reached = dict()
        reached[self.initial.to_tuple()] = node

        while not frontier.isEmpty():
            node = frontier.pop()
            if self.is_goal(node.get_state()):
                return node.find_path(node, len(reached))
            for child in self.expand(node):
                s = child.state
                if s.to_tuple() not in reached or child.path_cost < reached[s.to_tuple()].path_cost:
                    reached[s.to_tuple()] = child
                    frontier.update(child, child.path_cost + self.heuristic(child))
        return None

    def uniform_cost_search(self):
        """
        The Uniform-Cost Search algorithm

        :return: Returns the solution path as a list, or nothing if there is no solution.
        """
        print("Uniform-Cost Search:")
        node = Node(self.initial, None, None, 0)
        frontier = utils.PriorityQueue()
        frontier.push(node, node.path_cost)
        reached = dict()
        reached[self.initial.to_tuple()] = node

        while not frontier.isEmpty():
            node = frontier.pop()
            if self.is_goal(node.get_state()):
                return node.find_path(node, len(reached))
            for child in self.expand(node):
                s = child.state
                if s.to_tuple() not in reached or child.path_cost < reached[s.to_tuple()].path_cost:
                    reached[s.to_tuple()] = child
                    frontier.update(child, child.path_cost)
        return None

