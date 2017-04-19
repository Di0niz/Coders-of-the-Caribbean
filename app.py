# -*- coding: utf-8 -*-
import sys
import math


# convert cube to odd-r offset
def cube_to_offset(cube):
    x, y, z = cube

    col = x + (z - (z&1)) / 2
    row = z
    return (col, row)

# convert odd-r offset to cube
def offset_to_cube(offset):
    row, col = offset

    x = col - (row - (row&1)) / 2
    z = row
    y = -x-z
    return (x,y,z)

def cube_distance(a, b):
    ax, ay, az = a
    bx, by, bz = b

    return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) / 2

def cube_direction(rotation):
    directions = [
        ( 1,-1, 0), ( 1, 0,-1), (0, 1,-1),
        (-1, 1, 0), (-1, 0, 1), (0,-1, 1)
    ]
    return directions[rotation]

def cube_add(a, b):
    ax, ay, az = a
    bx, by, bz = b

    return (ax + bx, ay + by, az + bz)

def cube_scale(hex, radius):
    x, y, z = hex
    return (x * radius, y * radius, z * radius)

def cube_neighbor(hex, rotation, radius = 1):
        return cube_add(hex, cube_scale(cube_direction(rotation), radius))

def cube_rotation(a, b):
    ax, ay, az = a
    bx, by, bz = cube_near(a, b)
    hex = (bx - ax, by - ay, bz - az)
    x, y, z = hex
    rotation = 0
    for i in xrange(6):
        
        dx, dy, dz = cube_direction(i) 

        if dx == x and dy == y and dz == z:
            rotation = i
            break

    return rotation

def cube_round(hex):
    hx, hy, hz = hex
    rx, ry, rz = int(hx), int(hy), int(hz)
    diff_x, diff_y, diff_z = abs(rx-hx),abs(ry-hy), abs(rz-hz)

    if diff_x > diff_y and diff_x > diff_z:
        rx = -ry-rz
    elif diff_y > diff_z:
        ry = -rx-rz
    else:
        rz = -rx-ry

    return (rx,ry,rz)

def lerp(a, b, t): 
    return a + (b - a) * t

def cube_lerp(a, b, t): 
    ax, ay, az = a
    bx, by, bz = b
    return (lerp(ax, bx, t), 
            lerp(ay, by, t),
            lerp(az, bz, t))


def cube_near(a, b):
    N = cube_distance(a, b)
    return cube_round(cube_lerp(a, b, 1.0/N ))



class EntityType(object):
    """Описание внутриигровых объектов"""
    SHIP, BARREL, MINE, CANNONBALL = "SHIP", "BARREL", "MINE", "CANNONBALL"


class Entity(object):
    """Определение базового класса внутриигровых объектов"""
    def __init__(self, entity_id, x, y):
        self.entity_id = entity_id
        self.x, self.y = x, y

    def update(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return "%d" % self.entity_id

    def dist_to(self, to_unit):
        self_cube = offset_to_cube((self.x, self.y))
        unit_cube = offset_to_cube((to_unit.x, to_unit.y))
        return cube_distance(self_cube, unit_cube)

class ShipEntity(Entity):
    def __init__(self, entity_id, x, y, rotation, speed, rum, player):
        Entity.__init__(self, entity_id, x, y)
        self.speed = speed
        self.rum = rum
        self.rotation = rotation
        self.player = player
        self.fire_wait = 0

    def update(self, x, y, rotation, speed, rum, player):
        Entity.update(self, x, y)
        self.speed = speed
        self.rum = rum
        self.rotation = rotation
        self.player = player
        self.fire_wait = max(0, self.fire_wait -1)

    def find_near_entity(self, entities):
        near_entity = None
        min_dist = 10000

        for entity in entities:
            cur_dist = self.dist_to(entity)

            if cur_dist < min_dist:
                near_entity = entity
                min_dist = cur_dist

        return near_entity

    def make_command(self, command):
        if command[0] == Commands.MOVE:
            res = "MOVE %d %d" % (command[1].x, command[1].y)
        elif command[0] == Commands.FIRE:
            res = "FIRE %d %d" % (command[1].x, command[1].y)
            self.fire_wait = 2
        elif command[0] == Commands.WAIT:
            res = "WAIT"
        return res

    def __repr__(self):
        return "S%d" % self.entity_id

class BarrelEntity(Entity):
    def __init__(self, entity_id, x, y, rum):
        Entity.__init__(self, entity_id, x, y)
        self.rum = rum

    def __repr__(self):
        return "B%d" % self.entity_id

class World(object):
    """Описание игрового мира"""

    WIDTH = 23
    HEIGHT = 21

    def __init__(self):
        """ Определяем список объектов доступных для класса """
        self.allships = {}

    def update(self):

        self.ships = []
        self.barrels = []
        self.enemyships = []
        self.cannonballs = []

        # инициализируем поле
        self.field = [0] * World.WIDTH * World.HEIGHT

        my_ship_count = int(raw_input())  # the number of remaining ships
        entity_count = int(raw_input())  # the number of entities (e.g. ships, mines or cannonballs)
        for i in xrange(entity_count):

            entity_id, entity_type, x, y, arg_1, arg_2, arg_3, arg_4 = raw_input().split()
            if entity_type == EntityType.BARREL:
                self.barrels.append(BarrelEntity(int(entity_id), int(x), int(y), int(arg_1)))
                self.field[int(x)+ int(y) * World.HEIGHT] = 1
            elif entity_type == EntityType.SHIP:

                if not int(entity_id) in self.allships:
                    ship = ShipEntity(int(entity_id), int(x), int(y), int(arg_1), int(arg_2), int(arg_3), int(arg_4))
                    # сохраняем информацию о корабле
                    self.allships[int(entity_id)] = ship
                else:
                    ship = self.allships[int(entity_id)]
                    ship.update(int(x), int(y), int(arg_1), int(arg_2), int(arg_3), int(arg_4))

                if arg_4 == "1":
                    self.ships.append(ship)
                else:
                    self.enemyships.append(ship)

                self.field[int(x)+ int(y) * World.HEIGHT] = 1


class Commands(object):
    MOVE = 1
    FIRE = 2
    MINE = 3
    SLOWER = 4
    WAIT = 5

class Actions(object):
    MOVE = 1
    FIRE = 2
    NEAR_ENEMY = 3
    NEED_RUM = 4
    MOVE_ENEMY = 5
    MOVE_RUM = 6

class Problems(object):
    MOVE = 1

def SUB(l, exclude = None):
    if not exclude is None:
        return [x for x in l if x!=exclude]
    return l
    
class Strategy(object):

    def __init__(self, world):
        self.world = world

    def get_actions(self, ship, exclude = None):

        command = None
        action = None

        near_enemy = ship.find_near_entity(SUB(self.world.enemyships, exclude))
        near_barrel = ship.find_near_entity(SUB(self.world.barrels, exclude))

        while command is None:
            if action is None:
                action = Actions.MOVE

            elif action == Actions.MOVE:
                print >> sys.stderr, "ENEMY" ,ship.dist_to(near_enemy) < 5, ship.dist_to(near_enemy)
                
        
                if ship.rum > 60 and near_enemy is not None:
                    action = Actions.MOVE_ENEMY
                elif near_enemy is not None and near_enemy.speed == 0 and ship.dist_to(near_enemy) < 5:
                    print >> sys.stderr, "ENEMY" ,ship.dist_to(near_enemy) < 5, ship.dist_to(near_enemy)
                    action = Actions.FIRE
                else:
                    action = Actions.NEED_RUM

            elif action == Actions.MOVE_ENEMY:

                if near_enemy.speed > 0 and ship.dist_to(near_enemy) > 4:
                    command = (Commands.MOVE, near_enemy)
                elif near_enemy.speed == 0:
                    action = Actions.FIRE
                else:
                    command = (Commands.WAIT, )

            elif action == Actions.NEED_RUM:
                if near_barrel is None:
                    action = Actions.MOVE_ENEMY
                else:
                    command = (Commands.MOVE, near_barrel)

            elif action == Actions.FIRE:
                command = (Commands.FIRE, near_enemy)

            print >> sys.stderr, action, command


        return command

WORLD = World()

while True:

    WORLD.update()

    STRATEGY = Strategy(WORLD)

    commands = {}

    for my_ship in WORLD.ships:
        commands[my_ship] = STRATEGY.get_actions(my_ship)

    # проверяем есть ли дубли, если есть тогда исключаем общую цель
    for i in WORLD.ships:
        for j in WORLD.ships:
            if i != j:
                if commands[i][0] == Commands.MOVE and isinstance(commands[i][1],BarrelEntity):
                    if commands[i][1] == commands[j][1]:
                        commands[j] = STRATEGY.get_actions(j, commands[j][1])
    
    # выводим список доступных комманд
    for ship in commands:
        command = ship.make_command(commands[ship])
        print command

