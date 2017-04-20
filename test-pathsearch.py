# -*- coding: utf-8 -*-
import unittest
from subprocess import Popen, PIPE, STDOUT


class TestStringMethods(unittest.TestCase):

    def test_search_path(self):
        """Тестируем алгоритм поиска"""
        raw = """3
        23
        0 SHIP 5 9 4 1 66 1
        2 SHIP 7 8 4 1 91 1
        4 SHIP 16 10 4 1 91 1
        1 SHIP 3 10 2 1 96 0
        3 SHIP 7 18 1 1 95 0
        5 SHIP 20 16 2 1 97 0
        7 MINE 17 11 0 0 0 0
        6 MINE 17 9 0 0 0 0
        12 MINE 11 11 0 0 0 0
        11 MINE 11 9 0 0 0 0
        28 CANNONBALL 20 17 4 1 0 0
        29 CANNONBALL 6 8 1 0 0 0
        30 CANNONBALL 20 17 4 3 0 0
        31 CANNONBALL 6 9 1 1 0 0
        14 BARREL 10 11 12 0 0 0
        13 BARREL 10 9 12 0 0 0
        15 BARREL 8 1 20 0 0 0
        17 BARREL 21 3 11 0 0 0
        19 BARREL 17 10 15 0 0 0
        20 BARREL 4 7 12 0 0 0
        22 BARREL 19 2 11 0 0 0
        26 BARREL 11 12 16 0 0 0
        25 BARREL 11 8 16 0 0 0"""

        #stdin = sys.stdin.write(raw)
        #stdout = sys.stdout
        p = Popen(['python', "app.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=False)

        # Передаем тестовую выборку данных
        out, err = p.communicate(input=raw)

        self.assertTrue("MOVE 20 16" in out)
        
        print 1,out


if __name__ == '__main__':
    unittest.main()

