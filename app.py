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

    def __str__(self):
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

    def __str__(self):
        return "S%s" % super(Entity, self)

class BarrelEntity(Entity):
    def __init__(self, entity_id, x, y, rum):
        Entity.__init__(self, entity_id, x, y)
        self.rum = rum

    def __str__(self):
        return "B%s" % super(Entity, self)

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

    def get_actions(self):

        command = None
        action = None

        find_solution = True
        while find_solution:
            if action == None:
                action = Actions.MOVE

            elif action == Actions.MOVE:

                command = (Commands.MOVE, target)

                find_solution = True
            elif action == Actions.NEAR_ENEMY:
                pass
            elif action == Actions.NEED_RUM:
                pass
            elif action == Actions.NEED_RUM:
                pass
            elif action == Actions.FIRE:
                pass


        actions = []

        for ship in self.world.ships:
            near_entity = ship.find_near_entity(self.world.barrels)
            if not near_entity is None:
                actions.append("MOVE %d %d" % (near_entity.x, near_entity.y))

        if len(actions) == 0:
            actions.append("WAIT")
        return "\n".join(actions)

    def next_move(self):
        """Определеяем следующий ход"""
        pass


WORLD = World()

while True:

    WORLD.update()

    STRATEGY = Strategy(WORLD)

    print STRATEGY.get_actions()
