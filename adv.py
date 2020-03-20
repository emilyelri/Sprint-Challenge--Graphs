from room import Room
from player import Player
from world import World
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
# world.print_rooms()

player = Player(world.starting_room)

# brainstorm:
#     no recursive this time
#     store reverse path -- will need to map opposite directions
#     cycle around each room's exits randomly until none are left
#     to make sure all rooms are visited, have conditional for while visited is less than the number of rooms?? don't hard code 500
#     make a graph --- SCRAPPED. graph already exists room_graph. can len(room_graph) -- yep
#     Stack?? -- SCRAPPED
#     grab each room and print to see what the data looks like
#     if the room hasn't already been visited:
#         add it to a dictionary -- store the id as key and the exit directions as value
#         ADD IN: import random is here for a reason, maybe randomize the order -- make it different each time, try to find best number <997 i think it was
#         also store the reverse of the direction used to enter so that we can move the player back out -- SCRAPPED, will store reverse later, want to grab it here
#         take the reverse out of the value array so we don't accidentally return before we've explored the other rooms
#     then i want to back track until the player returns to the last room that still has routes to explore
#         visited won't work here
#         if we remove the exits from rooms when that exit has been fully explored, we can check by seeing if the visited array is empty
#         while visited array is empty:
#             move backwards basically
#             using the reversed path, pop the last value
#             add it to the traversal path
#             and move the player over player.travel(old room) or previous or something

#         once we've returned to a still 'active' room
#         grab the next available direction -- use visited
#         move in that direction -- add to traversal, add the opposite direction to reversal, and move the player in that direction

#         should run until every room has been visited because it will keep popping back once it reaches a deadend and then continue exploring an unexplored

#         draw up game plan

# game plan
#     store the traversal_path as well as a reverse_path.
#     traversal is the total path of the player, reverse_path is more fluid and will be used to help player return to an active room after a dead end.
#     map opposite directions for easy reuse.
#     create a visited dictionary to track which rooms have been hit already.
#     initialize visited with world.starting_room

#     while the length of the visited dictionary is less than the length of the provided room_graph:
#         if the player's current room hasn't been visited,
#             add it to the dictionary by id with a value of an array of all exits - not a set because we are going to modify this.
#             grab the latest entry in reverse_path
#             remove it from the visited[id] array so we know not to go back to the last room.
#             randomize the order of the array of directions - this will make the program run differently every time
#         a conditional statement next for once we've reached a deadend:
#         while the direction array of the current room is 0
#             pop off the latest direction from the reversed path
#             add that to traversal_path becauase this is part of the player's total path as they move backwards
#             ERROR - don't forget to move the player

#         for each new room in the "stack", then:
#         move the player in the first direction of the array
#         add that to traversal_path
#         add the opposite direction to reverse_path
#         ERROR - don't forget to move the player

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = []                                                             # final result path
reverse_path = []                                                               # for back-tracking
visited = {}                                                                    # the usual - will have key of room id and value of exits array
opposite = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
    }

visited[player.current_room.id] = player.current_room.get_exits()               # init visited dict with format {room.id: [exits dictions]}
                                                                                # ex {1: ['n', 's'], 2: ['e', 'w']}

while len(visited) < len(room_graph) - 1:                                       # while we haven't visited ALL the rooms: ERROR -- need len(room_graph) - 1 ?
    # print(player.current_room.get_exits())
    
    # room = player.current_room                                                # didnt work?
    # room_id = player.current_room.id
    
    if player.current_room.id not in visited:                                       # if the current room hasn't yet been added to visited:
        visited[player.current_room.id] = player.current_room.get_exits()               # add the id as a key! and add the exits as an array for the value.
        prev = reverse_path[-1]                                                         # grab the opposite of the last traveled direction - the path back
        visited[player.current_room.id].remove(prev)                                    # and remove the path back from the exits to the current room so we don't revisit it
        random.shuffle(visited[player.current_room.id])                                 # shuff the exits for current room

    
    while len(visited[player.current_room.id]) == 0:                                 # while there are no exits remaining to explore for a room
        prev = reverse_path.pop()                                                       # pop the path back from path and set to prev
        traversal_path.append(prev)                                                     # add that direction to the final traversal path
        player.travel(prev)                                                             # and then move the player in the direction - back to the last room that still has exits left to explore

    move_direction = visited[player.current_room.id].pop(0)                         # grab that first random direction from the current room in visited
    traversal_path.append(move_direction)                                           # add it to traversal path
    reverse_path.append(opposite[move_direction])                                           # add the OPPOSITE of it to the path
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
    print()
    print(len(traversal_path))
    print()
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