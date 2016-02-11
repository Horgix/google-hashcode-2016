#! /usr/bin/env python3

from enum import Enum

class Cell(Enum):
    painted = '#'
    clear = '.'

class Warehouse:
    def __init__(self, nb, x, y):
        self.x = x
        self.y = y
        self.nb = nb
        self.products = {}

#class Order:

class Map:
    def import_from_file(self, filename):
        with open(filename, 'r') as f:
            # Parse basic informations
            (self.rows,
                self.columns,
                self.dronesNb,
                self.deadline,
                self.maximumLoad
                ) = tuple([int(x) for x in f.readline().split()])
            # Parse products section
            self.productsNb = int(f.readline())
            self.productsWeight = {}
            weights = [int(x) for x in f.readline().split()]
            if len(weights) != self.productsNb:
                raise Exception("Products weight list != products number: " +
                        str(weights) + " vs " + str(self.productsNb))
            for pnb, w in enumerate(weights):
                self.productsWeight[pnb] = w
            # Parse warehouse sections
            self.warehousesNb = int(f.readline())
            self.warehouses = {}
            for i in range(self.warehousesNb):
                wr, wc = tuple([int(x) for x in f.readline().split()])
                products = [int(x) for x in f.readline().split()]
                self.warehouses[i] = Warehouse(i, wr, wc)
                if len(products) != self.productsNb:
                    raise Exception("Warehouse products list != products number: " +
                            str(products) + " vs " + str(self.productsNb))
                for pnb, availables in enumerate(products):
                    self.warehouses[i].products[pnb] = availables


            #self.rows = int(self.rows)
            #self.columns = int(self.columns)
            #for lineNb, line in enumerate(f.readlines()):
            #    if lineNb >= self.rows:
            #        raise Exception("Line number out of bounds")
            #    line = line.rstrip('\n')
            #    self.matrix[lineNb] = {}
            #    for columnNb, cell in enumerate(line):
            #        if columnNb >= self.columns:
            #            raise Exception("Column number out of bounds")
            #        self.matrix[lineNb][columnNb] = Cell(cell)
    def __str__(self):
        out = ""
        out += "Rows: " + str(self.rows) + "\n"
        out += "Columns: " + str(self.columns) + "\n"
        out += "Drones number: " + str(self.dronesNb) + "\n"
        out += "Deadline: " + str(self.deadline) + "\n"
        out += "Maximum load per drone: " + str(self.maximumLoad) + "\n"
        out += "Products number: " + str(self.productsNb) + "\n"
        #for pnb, w in self.productsWeight.items():
        #    out += "Product " + str(pnb) + " weight = " + str(w) + "\n"
        #for i in range(self.rows):
        #    for j in range(self.columns):
        #        out += self.matrix[i][j].value
        #    out += '\n'
        return out

s = Map()
s.import_from_file('mother_of_all_warehouses.in')
print(s)
