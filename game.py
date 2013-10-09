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

# class Rect(object):
    
#     def __init__(self, x, y, width, height):
#         self._x, self._y = x, y
#         self._width, self._height = width, height

#     def set_x(self, value): self._x = value
#     x = property(lambda self: self._x, set_x)
#     def set_y(self, value): self._y = value
#     y = property(lambda self: self._y, set_y)
#     def set_width(self, value): self._width = value
#     width = property(lambda self: self._width, set_width)
#     def set_height(self, value): self._height = value
#     height = property(lambda self: self._height, set_height)
#     def set_pos(self, value): self._x, self._y = value
#     pos = property(lambda self: (self._x, self._y), set_pos)
#     def set_size(self, value): self._width, self._height = value
#     size = property(lambda self: (self._width, self._height), set_size)

#     def contains(self, x, y):
#         if x < self._x or x > self._x + self._width: return False
#         if y < self._y or y > self._y + self._height: return False
#         return True

#     def intersects(self, other):
#         if self._x + self._width < other.x: return False
#         if other.x + other.width < self._x: return False
#         if self._y + self._height < other.y: return False
#         if other.y + other.height < self._y: return False
#         return True





############
# class Enemy(GameElement):
#     SOLID = True
#     IMAGE = "EnemyBug"

#     def __init__(self):
#         GameElement.__init__(self)
#         self.dist=1

#         self.xMove=1
#         self.yMove=0

#         self.direction=1
#         self.nextdir=3
#         self.xdir=[0,-self.dist,self.dist,0,0]
#         self.ydir=[0,0,0,-self.dist,self.dist]
#         # 

#         # self.direction = random.randint(1,4)
#         # self.dist = 3
#         # self.moves = random.randint(2,5)
#         # self.moveCount = 0;

#     def update(self, block_group):
#         self.xMove=self.xdir[self.nextdir]
#         self.yMove=self.ydir[self.nextdir]

#         self.rect.move_ip(self.xMove,self.yMove)

#         if pyglet.sprite.spritecollide(self, block_group, False):
#             self.rect.move_ip(-self.xMove,-self.yMove)

#             self.xMove=self.xdir[self.direction]
#             self.yMove=self.ydir[self.direction]
#             self.rect.move_ip(self.xMove,self.yMove)

#             if pyglet.sprite.spritecollide(self, block_group, False):
#                 self.rect.move_ip(-self.xMove,-self.yMove)
#                 if self.nextdir<3:
#                     self.nextdir=randint(3,4)
#                 else:
#                     self.nextdir=randint(1,2)
#         else:
#             self.direction=self.nextdir
#             if self.nextdir<3:
#                 self.nextdir=randint(3,4)
#             else:
#                 self.nextdir=randint(1,2)



       
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
        # if CURRENT_PLAYER.inventory) >= 5:
        #     print "Congratulations, %s! You just won because you retrieved 5 items!" %CURRENT_PLAYER
        #     # time.sleep function creates a pause in the game before it "ends/exits" the
        #     # game and the window of the game
        #     ###### HOWEVER ######
        #     # the game does not show that the last gem gets picked up before it ends the game
        #     time.sleep(5)
        #     sys.exit(0)

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

    # global ENEMY
    # ENEMY = Enemy()
    # GAME_BOARD.register(ENEMY)
    # GAME_BOARD.set_el(16, 8, ENEMY)
    # print ENEMY

    global CURRENT_PLAYER
    CURRENT_PLAYER = PLAYER1

