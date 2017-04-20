# -*- coding: utf-8 -*-
import unittest
from subprocess import Popen, PIPE, STDOUT


class TestStringMethods(unittest.TestCase):

    def test_search_path(self):
        """Тестируем функионал разворота у второго корабля"""
        raw = """2
        18
        0 SHIP 7 10 3 1 90 1
        2 SHIP 17 12 4 0 86 1
        1 SHIP 3 10 0 1 97 0
        3 SHIP 18 14 4 0 47 0
        4 MINE 6 5 0 0 0 0
        6 MINE 6 6 0 0 0 0
        32 CANNONBALL 18 14 2 0 0 0
        33 CANNONBALL 17 12 3 2 0 0
        11 BARREL 20 15 19 0 0 0
        10 BARREL 20 5 19 0 0 0
        12 BARREL 18 7 13 0 0 0
        16 BARREL 5 10 16 0 0 0
        17 BARREL 16 8 13 0 0 0
        19 BARREL 3 8 15 0 0 0
        22 BARREL 15 7 11 0 0 0
        25 BARREL 14 12 11 0 0 0
        24 BARREL 14 8 11 0 0 0
        26 BARREL 18 6 19 0 0 0
        2
        19
        0 SHIP 7 10 3 0 89 1
        2 SHIP 17 12 4 0 85 1
        1 SHIP 3 10 0 0 96 0
        3 SHIP 18 14 4 0 46 0
        4 MINE 6 5 0 0 0 0
        6 MINE 6 6 0 0 0 0
        33 CANNONBALL 17 12 3 1 0 0
        34 CANNONBALL 18 14 2 2 0 0
        35 CANNONBALL 6 6 1 2 0 0
        11 BARREL 20 15 19 0 0 0
        10 BARREL 20 5 19 0 0 0
        12 BARREL 18 7 13 0 0 0
        16 BARREL 5 10 16 0 0 0
        17 BARREL 16 8 13 0 0 0
        19 BARREL 3 8 15 0 0 0
        22 BARREL 15 7 11 0 0 0
        25 BARREL 14 12 11 0 0 0
        24 BARREL 14 8 11 0 0 0
        26 BARREL 18 6 19 0 0 0"""

        #stdin = sys.stdin.write(raw)
        #stdout = sys.stdout
        p = Popen(['python', "app.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=False)

        # Передаем тестовую выборку данных
        out, err = p.communicate(input=raw)
        # вырезаем         
        print err[len(raw)+1: err.find("Traceback")-1]
        print '---'
        print out




if __name__ == '__main__':
    unittest.main()

