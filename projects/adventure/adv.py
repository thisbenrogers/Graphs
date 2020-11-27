from room import Room
from player import Player
from world import World
from utils import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
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

# ! --------------------Start Ben Rogers Code----------

class Traversal_Graph():
    def __init__(self):
        self.rooms = {}
        self.visited = set()

    def add_room(self, room_id):
        self.rooms[room_id] = {}
        return None

    def get_opposite(self, cardinal_direction):
        opposite = {
            'n': 's',
            's': 'n',
            'e': 'w',
            'w': 'e'
        }
        return oppostie[cardinal_direction]

    def add_unexplored_exits(self):
        # player mus be currently in the room 
        # ! assumes that room is being visited for the 1st time
        # this function adds ALL exits, 
        room_id = player.current_room.id
        anon_exits = player.current_room.get_exits()
        for ex in anon_exits:
            self.rooms[room_id][ex] = '?'
        return None

    def update_exit(self, rm1_id, direction, rm2_id):
        # call this function AFTER player has traveled to new unexplored exit
        self.rooms[rm1_id][direction] = rm2_id
        self.add_room(rm2_id)
        opposite_dir = self.get_opposite(direction)
        self.rooms[rm2_id][opposite_dir] = rm1_id
        return None

    def show_exits(self, room_id):
        return self.rooms[room_id]

    def move_player(self, direction):
        player.travel(direction)
        traversal_path.append(direction)
        return None

    def get_rand_unexplored_dir(self, dir_arr):
        # *     returns a string with one cardinal direction chosen from the passed-in array
        # *     returns None if dead-end
        rand_arr = []
        room_id = player.current_room.id
        for direction, value in self.rooms[room_id].items():
            if value == '?':
                rand_arr.append(direction)
        if len(rand_arr) == 0:
            return None
        return random.choice(rand_arr)

    def find_nearest_unexplored(self):
        # * returns {room_id: {'direction': '?'}} once unexplored direction is found, or
        # * returns None if there are no unexplored directions left
        return None

    def dft(self):
        # * returns None when a dead-end is reached
        return None

    def traverse(self):
        # * runs dft() until None is returned
        # *     runs find_nearest_unexplored() once dft() returns None, then re-runs dft()
        # *     if find_nearest_unexplored returns None, 
        # *         return None from this method
        return None



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
