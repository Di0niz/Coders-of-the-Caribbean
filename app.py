# -*- coding: utf-8 -*-
import sys
import math


class EntityType(object):
    """Описание внутриигровых объектов"""
    SHIP, BARREL, MINE, CANNONBALL = "SHIP", "BARREL", "MINE", "CANNONBALL"


class Entity(object):
    """Определение базового класса внутриигровых объектов"""
    def __init__(self, entity_id, x, y):
        self.entity_id = entity_id
        self.x, self.y = x, y

    def __repr__(self):
        return "%d" % self.entity_id

    def dist_to(self, to_unit):
        return abs(self.x - to_unit.x) + abs(self.y - to_unit.y)

class ShipEntity(Entity):
    def __init__(self, entity_id, x, y, rotation, speed, rum, player):
        Entity.__init__(self, entity_id, x, y)
        self.speed = 0
        self.rum = 0
        self.rotation = 0
        self.player = 0

    def find_near_entity(self, entities):
        near_entity = None
        min_dist = 10000

        for entity in entities:
            cur_dist = self.dist_to(entity)

            if cur_dist < min_dist:
                near_entity = entity
                min_dist = cur_dist

        return near_entity

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
        self.ships = []
        self.barrels = []
        self.enemyships = []

        self.field = []

    def update(self):

        self.ships = []
        self.barrels = []
        self.enemyships = []
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
                ship = ShipEntity(int(entity_id), int(x), int(y), int(arg_1), int(arg_2), int(arg_3), int(arg_4))
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
                
                
                if near_enemy is not None and ship.dist_to(near_enemy) < 4:
                    print >> sys.stderr, "ENEMY" ,ship.dist_to(near_enemy) < 4, ship.dist_to(near_enemy)
                    action = Actions.FIRE
                    
                elif ship.rum > 60 and near_enemy is not near_enemy:
                    action = Actions.MOVE_ENEMY
                else:
                    action = Actions.NEED_RUM
            elif action == Actions.MOVE_ENEMY:
                if ship.dist_to(near_enemy) > 3:
                    command = (Commands.MOVE, near_enemy)
                else:
                    action = Actions.FIRE

            elif action == Actions.NEED_RUM:
                if near_barrel is None:
                    action = Actions.MOVE_ENEMY
                else:
                    command = (Commands.MOVE, near_barrel)

            elif action == Actions.FIRE:
                command = (Commands.FIRE, near_enemy)
            print >> sys.stderr, action, command


        return command

    def parse_command(self, command):
        if command[0] == Commands.MOVE:
            res = "MOVE %d %d" % (command[1].x, command[1].y)
        elif command[0] == Commands.FIRE:
            res = "FIRE %d %d" % (command[1].x, command[1].y)
        return res



WORLD = World()

while True:

    WORLD.update()

    STRATEGY = Strategy(WORLD)

    commands = []

    for my_ship in WORLD.ships:
        commands.append(STRATEGY.get_actions(my_ship))

    # проверяем есть ли дубли, если есть тогда исключаем общую цель
    com_len = len(commands)
    for i in xrange(com_len - 1):
        for j in xrange(i, com_len):
            if commands[i][0] == Commands.MOVE and isinstance(commands[i][1],BarrelEntity):
                if commands[i][1] == commands[j][1]:
                    commands[j] = STRATEGY.get_actions(my_ship, commands[j][1])
    
    # выводим список доступных комманд
    for comm in commands:
        print STRATEGY.parse_command(comm)
                    
