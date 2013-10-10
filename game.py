import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import time
from random import randint

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER1 = None
PLAYER2 = None
CURRENT_PLAYER = None
######################

GAME_WIDTH = 18
GAME_HEIGHT = 10

#### Put class definitions here ####

class Wall(GameElement):
    IMAGE = "StoneBlock"
    SOLID = True

class Fake_Wall(Wall):
    SOLID = True

####

class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False

####

class Character(GameElement):
    SOLID = True
    count = 0

    def __init__(self, player):
        GameElement.__init__(self)
        self.inventory = []
        self.IMAGE = player

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

####

class Gem(GameElement):
    IMAGE = "OrangeGem"
    SOLID = False
    def __init__(self, pos):
        self.fakewall = pos

    def interact(self, player):
        player.inventory.append(self)
        new_wall = Fake_Wall()
        GAME_BOARD.register(new_wall)
        GAME_BOARD.del_el(self.fakewall[0],self.fakewall[1])
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" %(len(player.inventory)))


####   End class definitions    ####
def keyboard_handler():
    pick_player()

    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"
  
    if direction:
        next_location = CURRENT_PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]
    
        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el:
            existing_el.interact(CURRENT_PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(CURRENT_PLAYER.x, CURRENT_PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, CURRENT_PLAYER)


# if a the 1 or 2 key is hit then it will switch which player 
# is allowed to move as the current player
def pick_player():
    global CURRENT_PLAYER
    if KEYBOARD[key._1]:
        CURRENT_PLAYER = PLAYER1

    if KEYBOARD[key._2]:
        CURRENT_PLAYER = PLAYER2

######################################################################
def initialize():
    """Put game initialization code here"""

    # getting map tokens out of txt file
    map_file = open("map.txt")
    map_txt = map_file.read()
    map_file.close()

    # create a list of map tokens
    map_tokens = map_txt.split('\n')
    for i in range(len(map_tokens)):
        map_tokens[i] = map_tokens[i].split()

    # empty lists of gem and wall tokens to be placed on map
    wall_positions = []
    fake_wall_positions = []
    gem_positions = []
    walls = []
    fake_walls = []
    gems = []

    # single items on map
    heart = Heart()

    # sorts map tokens into appropriate lists
    for y in range(len(map_tokens)):
        for x in range(len(map_tokens[y])):
            if map_tokens[y][x] == '#':
                wall_positions.append((x,y))
            if map_tokens[y][x] == '*':
                fake_wall_positions.append((x,y))
            if map_tokens[y][x] == '?':
                gem_positions.append((x,y))
            if map_tokens[y][x] == 'x':
                GAME_BOARD.register(heart)
                GAME_BOARD.set_el(x,y,heart)


    # places the wall tokens down on map
    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0],pos[1], wall)
        walls.append(wall)

    # places the FAKE wall tokens down on map
    for pos in fake_wall_positions:
        fake_wall = Fake_Wall()
        GAME_BOARD.register(fake_wall)
        GAME_BOARD.set_el(pos[0],pos[1], fake_wall)
        fake_walls.append(fake_wall)

    fake_walls_positions = [
        (14,3),
        (11,6),
        (10,2),
        (7,3),
        (1,5),
        (13,1),
        (12,7),
        (7,8),
        (3,1)
    ]
    
    count = 0
    # places the gems tokens down on map
    for pos in gem_positions:
        gem = Gem(fake_walls_positions[count])
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0],pos[1], gem)
        gems.append(gem)
        count +=1


    global PLAYER1
    PLAYER1 = Character("Girl")
    GAME_BOARD.register(PLAYER1)
    GAME_BOARD.set_el(1, 1, PLAYER1)
    print PLAYER1

    global PLAYER2
    PLAYER2 = Character("Boy")
    GAME_BOARD.register(PLAYER2)
    GAME_BOARD.set_el(16, 8, PLAYER2)
    print PLAYER2

    global CURRENT_PLAYER
    CURRENT_PLAYER = PLAYER1

