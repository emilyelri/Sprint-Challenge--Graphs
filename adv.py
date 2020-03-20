from room import Room
from player import Player
from world import World
import random
from ast import literal_eval
from util import Stack

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
# world.print_rooms()

player = Player(world.starting_room)














# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = []                                                             # final result path
path = []                                                                       # less permanent path
visited = {}                                                                    # the usual
opposite = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}                             # for back-tracking

visited[player.current_room.id] = player.current_room.get_exits()               # init visited dict with format {room.id: [exits dictions]}
                                                                                # ex {1: ['n', 's'], 2: ['e', 'w']}

while len(visited) < len(room_graph) - 1:                                       # while we haven't visited ALL the rooms:
    # print(player.current_room.get_exits())
    
    if player.current_room.id not in visited:                                       # if the current room hasn't yet been added to visited:
        visited[player.current_room.id] = player.current_room.get_exits()               # add the id as a key! and add the exits as an array for the value.
        random.shuffle(visited[player.current_room.id])                                 # shuff the exits for current room

        prev = path[-1]                                                                 # grab the opposite of the last traveled direction - the path back
        visited[player.current_room.id].remove(prev)                                    # and remove the path back from the exits to the current room so we don't revisit it
    
    while len(visited[player.current_room.id]) < 1:                                 # when there are no exits remaining to explore for a room
        prev = path.pop()                                                               # pop the path back from path and set to prev
        traversal_path.append(prev)                                                     # add that direction to the final traversal path
        player.travel(prev)                                                             # and then move the player in the direction - back to the last room

    move_direction = visited[player.current_room.id].pop(0)                         # grab that first random direction from the current room in visited
    traversal_path.append(move_direction)                                           # add it to traversal path
    path.append(opposite[move_direction])                                           # add the OPPOSITE of it to the path
    player.travel(move_direction)                                                   # then move in that direction

                                                                                    # rinse and repeat until all rooms have been added to visited!

    
    
















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