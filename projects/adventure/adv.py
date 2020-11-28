from room import Room
from player import Player
from world import World
from utils import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# ! --------------------Start Ben Rogers Code----------

class Traversal_Graph():
    def __init__(self):
        self.rooms = {}
        self.visited = set()

    def add_empty_room(self, room_id):
        self.rooms[room_id] = {}
        return None

    def show_exits(self, room_id):
        # *     returns dictionary
        return self.rooms[room_id]

    def move_player(self, cardinal_direction):
        # *     keeps player.current_room.id and traversal_path in lockstep with each other
        player.travel(cardinal_direction)
        traversal_path.append(cardinal_direction)
        return None

    def get_opposite(self, cardinal_direction):
        # *     for use in self.update_exit()
        opposite = {
            'n': 's',
            's': 'n',
            'e': 'w',
            'w': 'e'
        }
        return opposite[cardinal_direction]

    def add_unexplored_exits(self):
        # *     player must be currently in the room 
        # *     this function adds ALL available exits (will overwrite any existing entries)
        # !     assumes that room is being visited for the 1st time
        room_id = player.current_room.id
        anon_exits = player.current_room.get_exits()
        for ex in anon_exits:
            if ex not in self.rooms[room_id].keys():
                self.rooms[room_id][ex] = '?'
        return None

    def update_exit(self, rm1_id, direction, rm2_id):
        # !     call this function AFTER player has traveled to new unexplored exit
        self.rooms[rm1_id][direction] = rm2_id
        if rm2_id not in self.visited:
            self.add_empty_room(rm2_id)
        opposite_dir = self.get_opposite(direction)
        self.rooms[rm2_id][opposite_dir] = rm1_id
        return None

    def get_rand_unexplored_dir(self):
        # *     returns a string with one cardinal direction from players CURRENT ROOM
        # *     returns None if dead-end
        rand_list = []
        room_id = player.current_room.id
        for direction, value in self.show_exits(room_id).items():
            if value == '?':
                rand_list.append(direction)
        if len(rand_list) == 0:
            return None
        return random.choice(rand_list)

    def retrace(self, path_list):
        # *     moves player along path to nearest unexplored exit
        for entry in path_list:
            direction, _ = entry
            self.move_player(direction)
        return None

    def find_nearest_unexplored(self):
        # *     uses bfs to find path to nearest unexplored exit
        # *     once path is found, calls self.retrace() to move player there.
        # *         returns True once unexplored direction is found, or
        # *         returns None if there are no unexplored directions left
        # *
        # *     we need the room we're traveling to so we can self.show_exits(curr_room),
        # *     so each entry in the Queue holds lists of tuples: 
        # *         (direction_to_travel, room_traveling_to)
        # *         the room_traveling_to is ignored by self.retrace(curr_path)

        q = Queue()
        visited = set()

        # *     this starting value is a throwaway tuple that kickstarts the while loop
        # *     it is removed in the target-case check
        q.enqueue([(random.choice(player.current_room.get_exits()), player.current_room.id)])

        while q.size() > 0:
            curr_path = q.dequeue()
            curr_node = curr_path[-1]
            curr_dir, curr_room = curr_node 

            if curr_room == '?':
                # *     removes the last direction 
                # *     (so self.dft() can manage selecting a new unexplored direction)
                curr_path.pop()
                # *     removes the first direction
                # *     (our path TO the starting Node, enqueue'd above)
                curr_path.pop(0)
                # *     sends a proper list of tuples for self.retrace() to unpack
                self.retrace(curr_path)
                return True
            
            if curr_node not in visited:
                visited.add(curr_node)

                # *     get the exits
                exits = self.show_exits(curr_room)

                # *     iterate over exits, enqueue the PATH and ROOM to them
                for key, value in exits.items():
                    path_copy = curr_path + [(key, value)]
                    q.enqueue(path_copy)
        return None


    def dft(self):
        # *     moves player in depth-first traversal of maze
        # *     returns None when a dead-end is reached
        s = Stack()
        s.push(player.current_room.id)
        while s.size() > 0:
            curr_room = s.pop()
            if curr_room not in self.visited:
                self.visited.add(curr_room)
                if curr_room not in self.rooms:
                    self.add_empty_room(curr_room)
                self.add_unexplored_exits()
            rand_dir = self.get_rand_unexplored_dir()
            if rand_dir is None:
                return None
            self.move_player(rand_dir)
            new_room = player.current_room.id
            self.update_exit(curr_room, rand_dir, new_room)
            s.push(new_room)
        return None

    def traverse(self):
        # *     runs dft() until None is returned, then
        # *         runs find_nearest_unexplored(), then re-runs traverse()
        # *         if find_nearest_unexplored returns None, 
        # *             return None from this method, we are finished
        exploring = self.dft()
        if exploring is None:
            unexplored = self.find_nearest_unexplored()
            if unexplored is None:
                return None
            self.traverse()

# *     This attempt currently traverses the entire graph in 990-1028 moves
attempt = Traversal_Graph()
attempt.traverse()

# ! ---------------------End Ben Rogers Code-----------

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
