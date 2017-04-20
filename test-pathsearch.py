# -*- coding: utf-8 -*-
import unittest
from subprocess import Popen, PIPE, STDOUT


class TestStringMethods(unittest.TestCase):

    def test_search_path(self):
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
        # вырезаем
        print err
        print '---'
        print out


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

        print err
        print '---'
        print out


    def runapp(self, raw):
        p = Popen(['python', "app.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=False)

        # Передаем тестовую выборку данных
        out, err = p.communicate(input=raw)
        return out, err[len(raw)+1: err.find("Traceback")-1]
        

if __name__ == '__main__':
    unittest.main()

