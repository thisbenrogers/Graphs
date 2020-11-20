from collections import deque

class Queue():
    def __init__(self):
        self.queue = deque()
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.popleft()
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph():
    def __init__(self):
        self.rooms = {}
        self.visited_rooms = set()
        self.last_visited = None
        self.path = []

    def add_room(self, room_id):
        self.rooms[room_id] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
        return None

    def add_exit(self, rm1, direction, rm2):
        self.rooms[rm1][direction] = rm2
        return None

    def dft(self, room, visited=None):
        if visited is None:
            visited = set()
        visited.add(room)
        # ! do our operations here
        for next in self.rooms[room] - visited:
            self.dft(next, visited)
        return visited
