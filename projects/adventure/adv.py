from room import Room
from player import Player
from world import World
from utils import Queue, Stack

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


# * Things we are tracking in the self. scope of the Graph():
# *     rooms we have visited
# *     EACH and EVERY cardinal direction for EACH and EVERY travel-move

class Traversal_Graph():
    def __init__(self):
        self.rooms = {}
        self.visited = set()
        self.path = []

    def add_room(self, room_id):
        self.rooms[room_id] = {}
        return None

    def add_anonymous_exit(self, room_id, exit_dir):
        existing = self.rooms[room_id]
        if exit_dir not in existing.keys():
            self.rooms[room_id][exit_dir] = '?'
        return None

    def get_opposite(self, cardinal_direction):
        opposite = {
            'n': 's',
            's': 'n',
            'e': 'w',
            'w': 'e'
        }
        print(f"opposite: {opposite[cardinal_direction]}")
        return opposite[cardinal_direction]

    def add_exit(self, rm1, direction, rm2):
        self.rooms[rm1][direction] = rm2
        self.add_room(rm2)
        opposite_dir = self.get_opposite(direction)
        self.rooms[rm2][opposite_dir] = rm1
        return None

    def show_exits(self, room):
        return self.rooms[room]

    def find_nearest_unexplored(self, room):
        # * bfs
        # *     returns shortest path to next unexplored exit
        # *     return a list with n,s,w,e cardinal directions
        # *     INCLUDES the unexplored direction as the last step in path
        nearest_visited = []
        path = []
        q = Queue()
        q.enqueue(room)
        while q.size() > 0:
            room = q.dequeue()
            if room not in nearest_visited:
                exits = self.show_exits(room)
                for exit_direction, exit_room in exits.items():
                    path.append(exit_direction)
                    q.enqueue(exit_room)
                    if exit_direction == '?':
                        return path
                nearest_visited.append(room)
        return None

    def get_rand_unexplored_dir(self, dir_arr, room_id):

        # *     returns a string with one cardinal direction chosen from the passed-in array
        # *     returns None if dead-end
        
        rand_arr = []

        for card, value in self.rooms[room_id].items():
            if value == '?':
                rand_arr.append(card)

        if len(rand_arr) == 0:
            return None

        return random.choice(rand_arr)

    def df_traverse(self):
        room_stack = Stack()

        initial_room = player.current_room.id
        room_stack.push(initial_room)

        while room_stack.size() > 0:
            curr_room = room_stack.pop()
            if curr_room not in self.visited:
                # * perform operations here

                # Adds to self.visited
                self.visited.add(curr_room)

                # adds curr_room to MY graph
                if curr_room not in self.rooms:
                    self.add_room(curr_room)

                # gets all exits
                exits = player.current_room.get_exits()

                # adds cardinal exit directions to MY graph (with a '?' value)
                for ex in exits:
                    self.add_anonymous_exit(curr_room, ex)

               
                # checks for dead-end,
                # retraces steps to nearest unexplored exit in case of dead-end
               
                # retrace = Queue()
                # if len(exits) == 1:
                #     retraced_steps = self.find_nearest_unexplored(curr_room)
                #     while len(retraced_steps) > 0:
                #         step = retrace.dequeue()
                #         traversal_path.append(step)
                #         player.travel(step)
                #         # self.visited
                #         # self.add_room
                #         # curr_room = player

                # ! Need to log current room after above dead-end check
                
                # chooses a random dir
                rand_dir = self.get_rand_unexplored_dir(exits, curr_room)
                print(f"rand_dir: {rand_dir}")

                # travel in that direction
                player.travel(rand_dir)

                # log that direction
                traversal_path.append(rand_dir)

                # get new room id
                new_room = player.current_room.id

                # add the exit we just traveled to MY graph
                self.add_exit(curr_room, rand_dir, new_room)

                # add to the df-stack
                room_stack.push(new_room)

                print(f"self.rooms: {self.rooms}")

        # check for length of MY graph (ensure it's at 500)
        # if len(self.rooms) == 500:


attempt = Traversal_Graph()
attempt.df_traverse()

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
