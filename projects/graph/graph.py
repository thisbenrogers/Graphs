"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()
        return None

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1].add(v2)
        return None


    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # Make a queue
        q = Queue()

        # make a set for visited nodes
        visited = set()

        # enqueue the starting node
        q.enqueue(starting_vertex)

        # loop while the queue isn't empty
        while q.size() > 0:
            # dequeue current node
            current_node = q.dequeue()
            # check if current node has been visited
            if current_node not in visited:
                # perform our operation, printing in this instance
                print(current_node)
                # mark as visited
                visited.add(current_node)
                # get neighbors
                neighbors = self.get_neighbors(current_node)
                # enqueue each neighbor
                for neighbor in neighbors:
                    q.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Make a stack
        s = Stack()

        # make a set for visited nodes
        visited = set()

        # enqueue the starting node
        s.push(starting_vertex)

        # loop while the queue isn't empty
        while s.size() > 0:
            # dequeue current node
            current_node = s.pop()
            # check if current node has been visited
            if current_node not in visited:
                # perform our operation, printing in this instance
                print(f"dft: {current_node}")
                # mark as visited
                visited.add(current_node)
                # get neighbors
                neighbors = self.get_neighbors(current_node)
                # push each neighbor
                for neighbor in neighbors:
                    s.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if visited is None:
            visited = set()
        visited.add(starting_vertex)
        print(f"dft_r: {starting_vertex}")
        for next in self.vertices[starting_vertex] - visited:
            self.dft_recursive(next, visited)
        return visited

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breadth-first order.
        """
        # initializes set for tracking visited nodes and a list for simplified queue
        visited = set()
        q = [[starting_vertex]]

        # base case
        if starting_vertex == destination_vertex:
            print("Same node")
            return None
        
        # traverses the graph
        while q:
            path = q.pop(0)
            node = path[-1]
            
            # if we haven't been here yet,
            if node not in visited:
                neighbors = self.get_neighbors(node)

                # check out all the neighbors
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    q.append(new_path)

                    # check to see if the neighbor is the destination vertex
                    if neighbor == destination_vertex:
                        print("Shortest path = ", *new_path) 
                        return
                
                # track that we've visited this node
                visited.add(node)

        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        pass  # TODO

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
