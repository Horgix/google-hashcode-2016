#! /usr/bin/env python3

from enum import Enum

class Cell(Enum):
    painted = 1
    clear = 2

class Surface:
    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.matrix = {}
    def import_from_file(self, filename):
        with open('simple.in', 'r') as f:
            self.rows, self.columns = tuple(f.readline().split())
            self.rows = int(self.rows)
            self.columns = int(self.columns)
            for lineNb, line in enumerate(f.readlines()):
                if lineNb >= self.rows:
                    raise Exception
                line = line.rstrip('\n')
                for columnNb, cell in enumerate(line):
                    if columnNb >= self.columns:
                        raise Exception
                    self.matrix[lineNb] = {}
                    if cell == '#':
                        self.matrix[lineNb][columnNb] = Cell.painted
                    elif cell == '.':
                        self.matrix[lineNb][columnNb] = Cell.clear
                    else:
                        print(cell)
                        raise Exception

s = Surface()
s.import_from_file('simple.in')
