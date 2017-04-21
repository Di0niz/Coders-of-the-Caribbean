# -*- coding: utf-8 -*-
import unittest
from subprocess import Popen, PIPE, STDOUT

from app import ShipEntity, BarrelEntity
import app


class TestStringMethods(unittest.TestCase):

    def tes2t_search_path(self):
        """Проверка упирания в границу"""
        raw = """3
        16
        0 SHIP 15 16 5 0 73 1
        2 SHIP 22 15 5 0 91 1
        4 SHIP 22 8 0 0 83 1
        1 SHIP 3 4 0 1 80 0
        3 SHIP 18 16 0 1 76 0
        9 MINE 20 6 0 0 0 0
        53 CANNONBALL 14 14 0 1 0 0
        54 CANNONBALL 14 16 3 1 0 0
        15 BARREL 7 5 12 0 0 0
        19 BARREL 16 7 18 0 0 0
        24 BARREL 10 4 14 0 0 0
        26 BARREL 18 8 18 0 0 0
        29 BARREL 14 6 14 0 0 0
        33 BARREL 18 10 11 0 0 0
        34 BARREL 13 4 17 0 0 0
        55 BARREL 14 14 30 0 0 0
        """

        # Передаем тестовую выборку данных
        out, err = self.runapp(raw)
        print out
        print "---"
        print err


    def tes2t_circle(self):
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

        a = app.offset_to_cube((21, 18))
        b = app.cube_neighbor(a, 3, 10)

        print app.cube_to_offset(b)
        new_ship = ShipEntity(1, 21, 18, 0, 1, 100, 1)
        target = BarrelEntity(2, 3, 10, 20)

        print new_ship, self.find_shortest(new_ship, [target])



    def runapp(self, raw):
        p = Popen(['python', "app.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=False)

        # Передаем тестовую выборку данных
        out, err = p.communicate(input=raw)
        return out, err #[len(raw)+1: err.find("Traceback")-1]


    def uniform_cost_search(self, start, goals):
        """ За основу взят алгоритм с wiki
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

        node = (start.x, start.y)
        frontier = [node]
        explored = []

        # определение оптимальных вершин
        vertex = {node:(0, start, None)}

        # пока есть что обходить
        while not (node is None or len(frontier) == 0):

            node = frontier.pop()

            explored.append(node)

            distance = vertex[node][0]
            ship = vertex[node][1]

            for future in ship.futures():
                n = (future.x, future.y)
                #for n in future.collitions:
                if n not in explored:

                    # определяем вес связи
                    next_distance = distance + 1

                    # помечаем текущую вершину
                    if n not in vertex or next_distance < vertex[n][0]:
                        vertex[n] = (next_distance, future, node)

                    if not (n in frontier or n in goals):
                        frontier.append(n)

        return vertex



    def find_shortest(self, start, unit_goals):
        """Описание алгоритма поиска кратчайшего пути"""
        goals = []

        mapping_goals = {}

        for unit in unit_goals:
            goals.append((unit.x, unit.y))
            mapping_goals[(unit.x, unit.y)] = unit

        #print goals

        vertex = self.uniform_cost_search(start, goals)
        # востанавливаем цепочку

        target = None
        min_len = 100
        min_node = None
        min_ship = None
        #min_solution, min_target = [], None
        for goal in goals:

            if goal in vertex:
                distance, future, node =  vertex[goal]
                if distance < min_len:
                    min_distance = distance
                    min_node = goal

        future = None
        if min_node is not None:
            target = mapping_goals[min_node]
            distance, prev_future, node = vertex[min_node]
            future = prev_future
            while node is not None:
                future = prev_future
                dist, prev_future, node = vertex[node]
                print prev_future,prev_future.rotation, prev_future.speed, prev_future.command


            # ищем цель

        #print vertex, target

        return target, future


if __name__ == '__main__':
    unittest.main()

