from room import Room
from player import Player
from world import World
from utils import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# ! -------------Start-Ben-Rogers-Code------------------------------

# ?
# ?     Helpful commands:
# ?
# ?         player.current_room.id
# ?         player.current_room.get_exits()
# ?         player.travel(direction)
# ?

# TODO Construct a Graph with:
# TODO      - Depth-first traversal that picks a random unexplored direction 
# TODO          from the player's current room, 
# TODO          travels and logs that direction, then loops
# TODO      - When we reach a dead-end (i.e. a room with no unexplored paths), 
# TODO          walk back to the nearest room that does contain an unexplored path
# TODO      - Use Breadth-First search to find the nearest room with a '?' for an exit

class Graph():
    def __init__(self):
        self.rooms = {}
        self.visited_rooms = set()
        self.path = []

    def add_room(self, room_id):
        self.rooms[room_id] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
        return None

    def add_exit(self, rm1, direction, rm2):
        self.rooms[rm1][direction] = rm2
        return None

    def show_exits(self, room):
        return self.rooms[room]

    def find_nearest_unexplored(self, room):
        # * bfs
        # *     returns shortest path to next unexplored exit
        # *     return a list with n,s,w,e cardinal directions
        # *     INCLUDES the unexplored direction as the last step in path
        self.visited_rooms.clear()
        path = []
        q = Queue()
        q.enqueue(room)
        while q.size() > 0:
            room = q.dequeue()
            if room not in self.visited_rooms:
                exits = self.show_exits(room)
                for exit_direction, exit_room in exits.items():
                    path.append(exit_direction)
                    q.enqueue(exit_room)
                    if exit_direction == '?':
                        return path
                self.visited.add(room)
        return None

curr_room = player.current_room.id
print(f"player.current_room.id {curr_room}")
print(f"player.current_room.get_exits() {player.current_room.get_exits()}")
print(f"player.travel('n') {player.travel('n')}")
curr_room = player.current_room.id
print(f"player.current_room.id {curr_room}")
print(f"player.current_room.get_exits() {player.current_room.get_exits()}")
print(f"player.travel('n') {player.travel('n')}")
curr_room = player.current_room.id
print(f"player.current_room.id {curr_room}")
print(f"player.current_room.get_exits() {player.current_room.get_exits()}")

# ! -------------End-Ben-Rogers-Code--------------------------------
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
