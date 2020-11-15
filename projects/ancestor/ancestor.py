from util import Queue

class Graph:
    def __init__(self):
        
        self.vertices = {}
        self.visited = set()

    def add_vertex(self, vertex_id):

        self.vertices[vertex_id] = set()
        return None

    def add_parent(self, v1, v2):

        self.vertices[v1].add(v2)
        return None

    def get_parents(self, vertex_id):

        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        return None

    def find_earliest_ancestor(self, start):

        p = self.get_parents(start)
        queue = Queue()
        res = []    # ? possibly make this into a list of lists that are a path from start node
                    # ?      pop() the last item off the longest list, or
                    # ?      pop the end off each list of the longest size and return the min

        if len(p) == 0:
            return -1

        queue.enqueue(start)

        while queue.size() > 0:
            curr_node = queue.dequeue()
            print(f"res in while: {res}") # ! for testing, remove
            if curr_node not in self.visited:
                self.visited.add(curr_node)
                parents = self.get_parents(curr_node)

                if parents is not set():
                    for p in parents:
                        queue.enqueue(p)
                if len(parents) == 0:
                    res.append(curr_node)

        print(f"res: {res}") # ! for testing, remove

        if len(res) == 2:
            a = res.pop()
            b = res.pop()
            return min(a, b)
        else:
            return res.pop()
                
        


def earliest_ancestor(ancestors, starting_node):
    g = Graph()
    for entry in ancestors:
        if entry[1] not in g.vertices:
            g.add_vertex(entry[1])
        if entry[0] not in g.vertices:
            g.add_vertex(entry[0])
        g.add_parent(entry[1], entry[0])
    
    return g.find_earliest_ancestor(starting_node)

# ! Remove testing funciotns below

ind = 3
test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
r = earliest_ancestor(test_ancestors, ind)
print(f"test {ind} res: {r}")