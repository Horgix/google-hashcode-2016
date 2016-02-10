#! /usr/bin/env python3

from enum import Enum

class Cell(Enum):
    painted = '#'
    clear = '.'

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
                    raise Exception("Line number out of bounds")
                line = line.rstrip('\n')
                self.matrix[lineNb] = {}
                for columnNb, cell in enumerate(line):
                    if columnNb >= self.columns:
                        raise Exception("Column number out of bounds")
                    self.matrix[lineNb][columnNb] = Cell(cell)
    def __str__(self):
        out = ""
        for i in range(self.rows):
            for j in range(self.columns):
                out += self.matrix[i][j].value
            out += '\n'
        return out

s = Surface()
s.import_from_file('simple.in')
print(s)
