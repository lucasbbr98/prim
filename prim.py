from operator import attrgetter


# Sorry, I was too lazy to actually make this any better. It should be in a 'helper file' in larger projects
def are_values_unique(x):
    """ Asserts values are unique in a list """
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)


class Vertex:
    """ Represents a vertex, for instance: A, B, C ... """

    def __init__(self, label: str):
        self.label = label

        # Needed for Prim's algorithm. Updated at the startup automatically
        self.ties = []
        self.has_visited = False
        self.neighbours = []

    @property
    def unvisited_neighbours(self) -> list:
        return [n for n in self.neighbours if not n.has_visited]

    def __repr__(self):
        return "Vertex {0}".format(self.label)


class Connection:
    """ Represents a Connection between two Vertex objects, with an associated weight """

    def __init__(self, vertex_one: Vertex, vertex_two: Vertex, weight: float):
        self.vertex_one = vertex_one
        self.vertex_two = vertex_two
        self.weight = weight
        self.has_chosen = False

    def __repr__(self):
        return "Connection {0} - {1} - {2}".format(self.vertex_one.label, self.weight, self.vertex_two.label)


class Graph:
    """ Represents a whole Graph. It also facilitates developers to create them with helper functions """

    def __init__(self, vertexes=None, connections=None):
        if connections is None:
            connections = []
        if vertexes is None:
            vertexes = []
        self.vertexes = vertexes
        self.connections = connections
        self.__origin_index__ = None
        self.__destination_index__ = None

    def get_vertex_by_label(self, label: str) -> Vertex:
        if not label or not isinstance(label, str):
            raise ValueError("Label must be a string")

        vertex = None
        for v in self.vertexes:
            if v.label == label:
                vertex = v
                break
        return vertex

    def get_cost_from_to(self, v1: Vertex, v2: Vertex) -> float:
        distance = 0
        for c in self.connections:
            if (c.vertex_one == v1 and c.vertex_two == v2) or (c.vertex_one == v2 and c.vertex_two == v1):
                distance = c.weight
                break
        return distance

    def add_vertex(self, label: str):
        if label in [x.label for x in self.vertexes]:
            raise IndexError("Labels must be unique. We have found a duplicate in Vertex labeled: {0}".format(label))
        self.vertexes.append(Vertex(label=label.upper()))

    def add_vertexes(self, list_of_labels: list):
        if not all(isinstance(e, str) for e in list_of_labels):
            raise ValueError("List of vertexes labels must contain only strings")

        list_of_labels_upper = [x.upper() for x in list_of_labels]
        if not are_values_unique(list_of_labels_upper):
            raise IndexError("All values of vertexes labels must be unique. Please check again.")

        for label in list_of_labels_upper:
            self.add_vertex(label)

    def add_connection(self, label_one: str, weight: float, label_two: str):
        if not label_one or not label_two or not isinstance(label_one, str) or not isinstance(label_two, str):
            raise ValueError("Connection labels must be of type string.")
        label_one = label_one.upper()
        label_two = label_two.upper()
        if label_one == label_two:
            raise ValueError("Connection labels cannot be identical."
                             "\nGot: {0} - {1} - {2}".format(label_one, weight, label_two))

        vertex_one = self.get_vertex_by_label(label=label_one)
        if not vertex_one:
            raise ValueError("A Vertex with label {0} was not found".format(label_one))
        vertex_two = self.get_vertex_by_label(label=label_two)
        if not vertex_two:
            raise ValueError("A Vertex with label {0} was not found".format(vertex_two))

        try:
            weight = float(weight)
        except ValueError:
            raise ValueError("Weight must be a number")

        if weight <= 0:
            raise ValueError("Weights must be positive and greater than 0")

        for c in self.connections:
            if (c.vertex_one == vertex_one and c.vertex_two == vertex_two) or (
                    c.vertex_one == vertex_two and c.vertex_two == vertex_one):
                raise ValueError("You have assigned two weights for the same vertexes."
                                 "\nAssigned: {0} - {1} - {2}"
                                 "\nAttempted: {3} - {4} - {5}".format(c.vertex_one.label, c.weight, c.vertex_two.label,
                                                                       c.vertex_one.label, weight, c.vertex_two.label))

        self.connections.append(Connection(vertex_one=vertex_one, weight=weight, vertex_two=vertex_two))
        vertex_one.neighbours.append(vertex_two)
        vertex_two.neighbours.append(vertex_one)

    def add_connections(self, tuple_of_connections: list):
        for c in tuple_of_connections:
            self.add_connection(c[0], c[1], c[2])


class SpanningTree:
    """ Represents a SpanningTree """

    def __init__(self, connections=None):
        if connections is None:
            self.connections = []
        else:
            self.connections = connections


class Prim:
    def __init__(self, graph=None):
        if isinstance(graph, Graph):
            self.graph = graph
        else:
            self.graph = Graph()

        self.spanning_tree = SpanningTree()

    def solve(self) -> SpanningTree:
        if not self.graph.vertexes or len(self.graph.vertexes) <= 0:
            raise ValueError("No graph found. Use Prim.graph.add_vertex() and Prim.graph.add_edge() to get started")

        current_vertex = self.graph.vertexes[0]
        current_vertex.has_visited = True
        has_finished = False

        while not has_finished:
            minimum_connection = None
            for c in self.search_connections:
                if c.has_chosen:
                    continue
                if not minimum_connection or c.weight < minimum_connection.weight:
                    minimum_connection = c

            if not minimum_connection:
                has_finished = True
            else:
                minimum_connection.has_chosen = True
                minimum_connection.vertex_one.has_visited = True
                minimum_connection.vertex_two.has_visited = True
                self.spanning_tree.connections.append(minimum_connection)

        return self.spanning_tree

    @property
    def search_connections(self):
        avaiable_connections = []
        for c in self.graph.connections:
            if c.has_chosen:
                continue
            if (c.vertex_one.has_visited and not c.vertex_two.has_visited) or (c.vertex_two.has_visited and not c.vertex_one.has_visited):
                avaiable_connections.append(c)

        return avaiable_connections


if __name__ == '__main__':
    """ Example on how to setup and run the Prim's algorithm """
    # Initiates an instance of Prim's class
    p = Prim()
    # Add vertexes with any custom Label
    p.graph.add_vertexes(['A', 'B', 'C', 'E', 'F', 'G', 'H'])
    # Adds connections between the vertexes. Labels must match with already added vertexes
    p.graph.add_connections([
        ('A', 8, 'B'),
        ('A', 5, 'E'),
        ('A', 1, 'F'),
        ('A', 6, 'H'),
        ('B', 6, 'F'),
        ('B', 4, 'C'),
        ('C', 2, 'F'),
        ('C', 7, 'G'),
        ('E', 3, 'H'),
        ('F', 5, 'H'),
        ('F', 9, 'G')
    ])

    # Solves and returns a SpanningTree object, with all the information stored inside it
    minimum_spanning_tree = p.solve()

