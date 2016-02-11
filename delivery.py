#! /usr/bin/env python3

class Warehouse:
    def __init__(self, nb, r, c):
        self.row = r            # Warehouse position row
        self.column = c         # Warehouse position column
        self.nb = nb            # Warehouse number (ID)
        self.products = {}      # Number of each product in stock

class Order:
    def __init__(self, i, n, r, c):
        self.row = r            # Order destination row
        self.colum = c          # Order destination column
        self.nb = i             # Order number (ID)
        self.productsNb = n     # Number of products in order
        self.products = {}      # Number of each product in order
    def getDelivered(self, productID, quantity):
        self.products[productID] -= quantiy
        if self.products[productID] == 0:
            del(self.products[productID])
        elif self.products[productID] < 0:
            raise Exception("Delivered too much of a product !")
    def satisfied(self):
        return self.products == {}

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
            # Parse orders section
            self.ordersNb = int(f.readline())
            self.orders = {}
            for i in range(self.ordersNb):
                dr, dc = tuple([int(x) for x in f.readline().split()])
                items = int(f.readline())
                self.orders[i] = Order(i, items, dr, dc)
                ps = [int(x) for x in f.readline().split()]
                if len(ps) != items:
                    raise Exception("Orders nb wrong somewhere")
                for p in ps:
                    if not p in self.orders[i].products:
                        self.orders[i].products[p] = 1
                    else:
                        self.orders[i].products[p] += 1
            # End of parsing
            remainingLines = f.readlines()
            if remainingLines != []:
                raise Exception("Didn't parse every line")

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
        out += "Warehouses number: " + str(self.warehousesNb) + "\n"
        out += "Orders number: " + str(self.ordersNb) + "\n"
        #for i in range(self.rows):
        #    for j in range(self.columns):
        #        out += self.matrix[i][j].value
        #    out += '\n'
        return out

filename = "mother_of_all_warehouses.in"
#filename = "busy_day.in"
s = Map()
s.import_from_file(filename)
print(s)
