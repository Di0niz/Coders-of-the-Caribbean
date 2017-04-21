# -*- coding: utf-8 -*-
import unittest
from subprocess import Popen, PIPE, STDOUT

from app import ShipEntity, BarrelEntity


class TestStringMethods(unittest.TestCase):


    def test_collition(self):
        """Проверяем реализацию коллизий"""

        new_ship = ShipEntity(1, 22, 20, 4, 2, 100, 1)


        target = BarrelEntity(2, 13, 4, 20)
        
        v = {}
        i = 1
        for ship in new_ship.futures():
            print ship, ship.collitions, (ship.x, ship.y), ship.rotation
            v[ship] = i
            i = i + 1
            print "---"
            for ship1 in ship.futures():
                print ship1, ship1.collitions, (ship1.x, ship1.y), ship1.rotation


        fut= new_ship.futures()[1].futures()[0].futures()[3].futures()[0].futures()[0]
        print (fut.x, fut.y)


        print self.find_shortest(new_ship, [target])



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
                for n in future.collitions:
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

        for unit in unit_goals:
            goals.append((unit.x, unit.y))

        vertex = self.uniform_cost_search(start, goals)
        # востанавливаем цепочку

        min_len = 10
        min_solution = []
        for goal in goals:
            solution = [goal]
            node = vertex[goal][2]
 
            while node is not None:
                solution.insert(0, node)
                node = vertex[node][2]

            if min_len > len(solution):
                min_solution = solution

        return solution


if __name__ == '__main__':
    unittest.main()

