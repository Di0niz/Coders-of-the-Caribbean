# -*- coding: utf-8 -*-
import unittest
from subprocess import Popen, PIPE, STDOUT

from app import *


class TestStringMethods(unittest.TestCase):

    def test_search_path(self):
        """Проверка упирания в границу"""
        raw = """2
        21
        0 SHIP 7 17 3 0 17 1
        2 SHIP 2 19 3 2 45 1
        1 SHIP 4 17 3 1 93 0
        3 SHIP 20 20 1 1 100 0
        10 MINE 6 12 0 0 0 0
        46 CANNONBALL 7 19 3 1 0 0
        47 CANNONBALL 6 17 2 1 0 0
        48 CANNONBALL 6 19 1 1 0 0
        49 CANNONBALL 5 17 0 2 0 0
        11 BARREL 10 3 13 0 0 0
        13 BARREL 8 2 19 0 0 0
        16 BARREL 8 1 19 0 0 0
        18 BARREL 11 3 11 0 0 0
        20 BARREL 16 2 13 0 0 0
        22 BARREL 2 1 13 0 0 0
        25 BARREL 1 17 19 0 0 0
        24 BARREL 1 3 19 0 0 0
        26 BARREL 11 1 12 0 0 0
        28 BARREL 4 7 10 0 0 0
        31 BARREL 20 1 19 0 0 0
        33 BARREL 19 4 20 0 0 0
        """

        # Передаем тестовую выборку данных
        out, err = self.runapp(raw)
        print out
        print "---"
        print err


    def test_circle(self):
        """Проверка зацикливания варианта решения"""

        raw = """2
        5
        0 SHIP 22 20 0 0 56 1
        4 SHIP 22 8 0 0 66 1
        1 SHIP 13 4 5 1 96 0
        3 SHIP 15 7 2 1 56 0
        29 BARREL 14 6 14 0 0 0"""

        out, err = self.runapp(raw)
        print out
        print "---"
        print err


    def te2st_find_shortest_path(self):
        
        raw = """1
        27
        0 SHIP 8 5 4 0 100 1
        1 SHIP 8 15 2 0 100 0
        4 MINE 5 5 0 0 0 0
        11 BARREL 18 14 17 0 0 0
        10 BARREL 18 6 17 0 0 0
        13 BARREL 15 15 13 0 0 0
        12 BARREL 15 5 13 0 0 0
        15 BARREL 2 19 13 0 0 0
        14 BARREL 2 1 13 0 0 0
        17 BARREL 16 12 19 0 0 0
        16 BARREL 16 8 19 0 0 0
        19 BARREL 5 18 15 0 0 0
        18 BARREL 5 2 15 0 0 0
        21 BARREL 11 15 17 0 0 0
        20 BARREL 11 5 17 0 0 0
        23 BARREL 16 18 15 0 0 0
        22 BARREL 16 2 15 0 0 0
        24 BARREL 1 10 16 0 0 0
        26 BARREL 4 15 15 0 0 0
        25 BARREL 4 5 15 0 0 0
        27 BARREL 14 10 10 0 0 0
        29 BARREL 15 13 15 0 0 0
        28 BARREL 15 7 15 0 0 0
        31 BARREL 3 13 17 0 0 0
        30 BARREL 3 7 17 0 0 0
        33 BARREL 9 12 20 0 0 0
        32 BARREL 9 8 20 0 0 0
        1
        29
        0 SHIP 8 5 4 0 99 1
        1 SHIP 8 15 2 0 99 0
        4 MINE 5 5 0 0 0 0
        34 CANNONBALL 8 15 0 4 0 0
        35 CANNONBALL 5 15 1 2 0 0
        11 BARREL 18 14 17 0 0 0
        10 BARREL 18 6 17 0 0 0
        13 BARREL 15 15 13 0 0 0
        12 BARREL 15 5 13 0 0 0
        15 BARREL 2 19 13 0 0 0
        14 BARREL 2 1 13 0 0 0
        17 BARREL 16 12 19 0 0 0
        16 BARREL 16 8 19 0 0 0
        19 BARREL 5 18 15 0 0 0
        18 BARREL 5 2 15 0 0 0
        21 BARREL 11 15 17 0 0 0
        20 BARREL 11 5 17 0 0 0
        23 BARREL 16 18 15 0 0 0
        22 BARREL 16 2 15 0 0 0
        24 BARREL 1 10 16 0 0 0
        26 BARREL 4 15 15 0 0 0
        25 BARREL 4 5 15 0 0 0
        27 BARREL 14 10 10 0 0 0
        29 BARREL 15 13 15 0 0 0
        28 BARREL 15 7 15 0 0 0
        31 BARREL 3 13 17 0 0 0
        30 BARREL 3 7 17 0 0 0
        33 BARREL 9 12 20 0 0 0
        32 BARREL 9 8 20 0 0 0"""

        out, err = self.runapp(raw)

        print out
        print "---"
        print err

    def test_collition(self):
        """Проверяем реализацию коллизий"""

        #print self.find_shortest(new_ship, [target])

        a = offset_to_cube((1, 1))
        b = cube_neighbor(a, 5, 5)
        b = cube_neighbor(b, 3, 2)

        ax, ay = cube_to_offset(a)
        bx, by = cube_to_offset(b)

        new_ship = ShipEntity(1, ax, ay, 0, 1, 100, 1)
        target = BarrelEntity(2, bx, by, 10)

        print new_ship
        move_barrell, target = self.find_shortest(new_ship, [target])
        print "NEXT: ", move_barrell,move_barrell.rotation,move_barrell.speed
        move_barrell, target  = self.find_shortest(move_barrell, [target])
        print "NEXT: ", move_barrell,move_barrell.rotation,move_barrell.speed
        move_barrell, target  = self.find_shortest(move_barrell, [target])
        print "NEXT: ", move_barrell,move_barrell.rotation,move_barrell.speed
        move_barrell, target  = self.find_shortest(move_barrell, [target])
        print "NEXT: ", move_barrell,move_barrell.rotation,move_barrell.collisions,move_barrell.speed    

        print (ax, ay), '=>', (bx, by)



    def runapp(self, raw):
        p = Popen(['python', "app.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=False)

        # Передаем тестовую выборку данных
        out, err = p.communicate(input=raw)
        return out, err #[len(raw)+1: err.find("Traceback")-1]


    def uniform_cost_search(self, start, goals):
        """ За основу взят алгоритм с wiki
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        
        """

        node = (start.x, start.y, start.rotation)

        # обходим не в глубину, а с учетом уровня дерева

        frontier = [node]
        next_frontier = []
        explored = []

        # определение оптимальных вершин
        vertex = {node: (0, start, None)}

        # ищем последнюю часть
        find_target = None
        find_goal   = None

        # изменяем алгоритм поиска
        # распостраняем волны до 50

        # пока есть что обходить

        current_distance = 0

        while not (node is None or len(frontier) == 0 or find_target is not None):

            node = frontier.pop()

            explored.append(node)

            distance, ship, prev_node = vertex[node]

            for future in ship.futures():
                n = (future.x, future.y, future.rotation)
                #for n in future.collisions:
                if n not in explored:

                    # определяем вес связи
                    next_distance = distance + 1


                    for collision in future.collisions:
                        if collision in goals:
                            find_target = n
                            find_goal = collision



                    # помечаем текущую вершину
                    if n not in vertex or next_distance < vertex[n][0]:
                        vertex[n] = (next_distance, future, node)

                        for collision in future.collisions:
                            if collision in goals:
                                find_target = n
                                find_goal = collision

                    if not (n in frontier):
                        next_frontier.append(n)

            # проверяем что 
            if len(frontier) == 0 and distance < 3:
                frontier = next_frontier
                next_frontier = []

        if find_target == None:
            min_dist = 100
            min_drot = 6

            for goal in goals:
                ghex = offset_to_cube(goal)

                # ищем ближайшего к нашей цели
                for potential in next_frontier:
                    px,py,protation = potential
                    phex = offset_to_cube((px,py))

                    dist = cube_distance(phex, ghex)

                    if min_dist > dist:
                        min_dist = dist
                        find_target = potential
                        find_goal = goal

                    elif min_dist == dist:
                        rotation = cube_rotation(phex, ghex)
                        d_rot = (rotation - protation + 6) % 6
                        if min_drot > d_rot:
                            min_drot = d_rot
                            find_target = potential
                            find_goal = goal

        return vertex, find_target, find_goal



    def find_shortest(self, start, unit_goals):
        """Описание алгоритма поиска кратчайшего пути"""
        goals = []

        mapping_goals = {}

        for unit in unit_goals:
            goals.append((unit.x, unit.y))
            mapping_goals[(unit.x, unit.y)] = unit

        #print goals

        vertex, node, goal = self.uniform_cost_search(start, goals)
        # востанавливаем цепочку
        future = None
        prev_future = None
        while node is not None:
            future = prev_future
            dist, prev_future, node = vertex[node]

        return future, mapping_goals[goal]


if __name__ == '__main__':
    unittest.main()

