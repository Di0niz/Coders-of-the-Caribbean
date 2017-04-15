# -*- coding: utf-8 -*-
import sys
import math


class EntityType(object):
    """Описание внутриигровых объектов"""
    SHIP, BARREL, MINE, CANNONBALL = "SHIP", "BARREL", "MINE", "CANNONBALL"


class Entity(object):
    """Определение базового класса внутриигровых объектов"""
    def __init__(self, entity_id):
        self.entity_id = entity_id

    def __str__(self):
        return "%d" % self.entity_id

class ShipEntity(Entity):
    def __init__(self, entity_id, x, y, rotation, speed, rum, player):
        Entity.__init__(self, entity_id)
        self.x, self.y = x, y
        self.speed = 0
        self.rum = 0
        self.rotation = 0
        self.player = 0

    def find_near_entity(self, entities):
        near_entity = None
        min_dist = 10000

        for entity in entities:
            cur_dist = (self.x - entity.x)**2 + (self.y - entity.y)**2

            if cur_dist < min_dist:
                near_entity = entity
                min_dist = cur_dist

        return near_entity

    def __str__(self):
        return "S%s" % super(Entity, self)

class BarrelEntity(Entity):
    def __init__(self, entity_id, x, y, rum):
        Entity.__init__(self, entity_id)
        self.x, self.y = x, y
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


class Strategy(object):

    def __init__(self, world):
        self.world = world

    def get_actions(self):

        actions = []

        for ship in self.world.ships:
            near_entity = ship.find_near_entity(self.world.barrels)
            actions.append("MOVE %d %d" % (near_entity.x, near_entity.y))
        return "\n".join(actions)


WORLD = World()

while True:

    WORLD.update()

    STRATEGY = Strategy(WORLD)

    print STRATEGY.get_actions()
