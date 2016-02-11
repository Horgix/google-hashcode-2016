#! /usr/bin/env python3

from enum import Enum
from cmath import sqrt
from math import ceil

class Warehouse:
    def __init__(self, nb, r, c):
        self.row = r            # Warehouse position row
        self.column = c         # Warehouse position column
        self.nb = nb            # Warehouse number (ID)
        self.products = {}      # Number of each product in stock
    def retrieveProduct(self, productID, quantity):
        self.products[productID] -= quantity
        if self.products[productID] < 0:
            raise Exception("Retrieved too much of a product !")

class Order:
    def __init__(self, i, n, r, c):
        self.row = r            # Order destination row
        self.colum = c          # Order destination column
        self.nb = i             # Order number (ID)
        self.productsNb = n     # Number of products in order
        self.products = {}      # Number of each product in order
    def getDelivered(self, productID, quantity):
        self.products[productID] = self.products[productID] - quantity
        if self.products[productID] == 0:
            del(self.products[productID])
        elif self.products[productID] < 0:
            raise Exception("Delivered too much of a product !")
    def isSatisfied(self):
        return self.products == {}
    def __str__(self):
        return "Order " + str(self.nb)# + " = " + str(self.products)

class DroneStatus(Enum):
    Flying = 1
    AtWarehouse = 2
    AtDestination = 2

class Drone:
    def __init__(self, n, r, c, m):
        self.row = r            # Drone current row
        self.colum = c          # Drone current column
        self.nb = n             # Drone number (ID)
        self.status = DroneStatus.AtWarehouse
        self.products = {}      # Quantity of each product that the drone carries
        self.maximumLoad = m
        self.weight = 0
    def pickProductToDeliver(self, fieldmap):
        order = [o for onb, o in fieldmap.orders.items() if not o.isSatisfied()][0]
        # Pick a product
        ## Pick first product to be delivered
        (prod, quantity) = [(pnb, quantity) for pnb, quantity in order.products.items() if quantity > 0][0]
        pweight = fieldmap.productsWeight[prod]
        maxCarry = self.maximumLoad / pweight
        if maxCarry >= quantity:
            toPick = quantity
        else:
            toPick = floor(maxCarry)
        fieldmap.orders[order.nb].getDelivered(prod, toPick)
        print("Drone " + str(self.nb) + " is going to pick " + str(toPick)
                + " items of product " + str(prod) + " for order "
                + str(order))
        return (prod, toPick)

    def load(self, productID, quantity, weight):
        if self.status != DroneStatus.AtWarehouse:
            raise Exception("Drone must be at a warehouse to load stuff")
        if not productID in self.products:
            self.products[productID] = 0
        self.products[productID] += quantity
        self.weight += quantity * weight
        if self.weight > maximumLoad:
            raise Exception("Drone overloaded")
    def deliver(self):
        if self.status != DroneStatus.AtDestination:
            raise Exception("Drone must be at a destination to deliver stuff")

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
                        self.orders[i].products[p] = 0
                    self.orders[i].products[p] += 1
                print(self.orders[i])
            # End of parsing
            remainingLines = f.readlines()
            if remainingLines != []:
                raise Exception("Didn't parse every line")
            # Setup drones
            self.drones = {}
            startr = self.warehouses[0].row
            startc = self.warehouses[0].column
            for i in range(self.dronesNb):
                self.drones[i] = Drone(i, startr, startc, self.maximumLoad)


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
    def getNumberOfSatisfiedOrders(self):
        return len([o for onb, o in self.orders.items() if o.isSatisfied()])
    #def processTurn(self):
    def findWarehouseWithEnoughProducts(self, productID, quantity):
        for wnb, w in self.warehouses.items():
            if w.products[productID] >= quantity:
                return wnb
        # If we get there, the product is available nowhere
        raise Exception("Product not available in warehouses")
    def loadProduct(self, droneID, warehouseID, productID, quantity):
        self.warehouses[warehouseID].retrieveProduct(productID, quantity)
        self.drones[droneID].loadWith(productID, quantity)
    def processTurn(self):
        for drone in [d for dnb, d in self.drones.items() if d.status == DroneStatus.AtWarehouse]:
            drone.pickProductToDeliver(self)

def flightLength(startr, startc, endr, endc):
    v1 = (startr - endr)
    if v1 < 0:
        v1 *= -1
    v2 = (startc - endc)
    if v2 < 0:
        v2 *= -1
    return ceil(sqrt((v1 * v1) + (v2 * v2)))

filename = "mother_of_all_warehouses.in"
#filename = "busy_day.in"
s = Map()
s.import_from_file(filename)
print(s)
print(s.getNumberOfSatisfiedOrders())
s.processTurn()
