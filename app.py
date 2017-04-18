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

    def __init__(self):
        """ Определяем список объектов доступных для класса """
        self.ships = []
        self.barrels = []
        self.enemyships = []

    def update(self):

        self.ships = []
        self.barrels = []
        self.enemyships = []

        my_ship_count = int(raw_input())  # the number of remaining ships
        entity_count = int(raw_input())  # the number of entities (e.g. ships, mines or cannonballs)
        for i in xrange(entity_count):

            entity_id, entity_type, x, y, arg_1, arg_2, arg_3, arg_4 = raw_input().split()
            if entity_type == EntityType.BARREL:
                self.barrels.append(BarrelEntity(int(entity_id), int(x), int(y), int(arg_1)))
            elif entity_type == EntityType.SHIP:
                ship = ShipEntity(int(entity_id), int(x), int(y), int(arg_1), int(arg_2), int(arg_3), int(arg_4))
                if arg_4 == "1":
                    self.ships.append(ship)
                else:
                    self.enemyships.append(ship)

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
    MOVE_RUM = 5

class Problems(object):
    MOVE = 1

class Strategy(object):

    def __init__(self, world):
        self.world = world

    def get_actions(self, ship):

        command = None
        action = None

        near_enemy = ship.find_near_entity(self.world.enemyships)
        near_barrel = ship.find_near_entity(self.world.barrels)

        while command is None:
            if action is None:
                action = Actions.MOVE

            elif action == Actions.MOVE:
                
                print >> sys.stderr, "ENEMY" ,ship.dist_to(near_enemy) < 4, ship.dist_to(near_enemy)
                
                if near_enemy is not None and ship.dist_to(near_enemy) < 4:
                    action = Actions.FIRE
                    
                elif ship.rum > 60:
                    action = Actions.MOVE_ENEMY
                else:
                    action = Actions.NEED_RUM
            elif action == Actions.MOVE_ENEMY:

                target = near_enemy
                if ship.dist_to(target) > 3:
                    command = (Commands.MOVE, target)
                else:
                    action = Actions.FIRE

            elif action == Actions.NEED_RUM:
                target = near_barrel
                if target is None:
                    action = Actions.MOVE_ENEMY
                else:
                    command = (Commands.MOVE, target)

            elif action == Actions.FIRE:
                command = (Commands.FIRE, near_enemy)
            print >> sys.stderr, action, command


        return self.parse_command(command)

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

    for my_ship in WORLD.ships:
        result = STRATEGY.get_actions(my_ship)
        print result

