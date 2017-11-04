'''
SA_WFF
'''

import numpy as np
from pylab import *

import SA_base


class SA_WFF(SA_base.SA_base):
    INIT_TEMP_MULTIPLIER = 2.0

    def __init__(self, problemInst, movesPerTemp=500, cool=0.9, c=0.25):
        SA_base.SA_base.__init__(self, problemInst, 0, movesPerTemp, cool)
        self.c = c
        self.prevAvgE = self.cost
        self.resetStats()

    def initTemp(self):
        moveDelta = []
        for j in xrange(0, self.movesPerTemp):
            delta = self.inst.genMove()
            moveDelta.append(delta)
        return self.INIT_TEMP_MULTIPLIER * np.std(moveDelta)

    def equilibrium(self):
        if self.acount >= self.movesPerTemp:
            self.prevAvgE = self.costMean()
            self.acount = 0
            return True
        if self.tcount <= 50:
            self.acount += 1
            return False
        if self.acount <= 500:
            self.acount += 1
            return False

        if (self.prevAvgE - self.costMean()) > \
                (self.c * self.costStdDev() / math.sqrt(self.tcount)):
            self.prevAvgE = self.costMean()
            self.acount = 0
            return True
        self.acount += 1
        return False

    def optimize(self):
        moves = 0
        costList = []
        temp = self.initTemp()
        frozenCount = 0
        lastCost = 0
        while frozenCount < self.FROZEN and moves < self.MAXMOVES:
            equil = False
            self.acount = 0
            while not equil:
                moves += 1
                delta = self.inst.genMove()
                if self.metropolis(delta, temp):
                    self.commitMove(delta)
                equil = self.equilibrium()
            std = self.costStdDev()
            cost = self.inst.cost()
            if lastCost == cost:
                frozenCount += 1
            else:
                frozenCount = 0
            temp = self.newTemp(temp)
            costList.append(moves)
            costList.append(cost)
            lastCost = cost
        return costList


if __name__ == '__main__':
    import TravSales

    inst = TravSales.TravSales()
    base = SA_WFF(inst, 10000, 0.9, 0.1)
    print base.optimize()
