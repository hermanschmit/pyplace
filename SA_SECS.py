'''
SA_SECS
'''

import numpy as np

import SA_base


class SA_SECS(SA_base.SA_base):
    INIT_TEMP_MULTIPLIER = 2.0
    TAKEN_SAMPLE_SIZE = 100
    TINY_COOL = 0.999
    FROZEN = 10

    def __init__(self, problemInst, movesPerTemp=500, cool=0.9, c=1.025, alpha=12):
        SA_base.SA_base.__init__(self, problemInst, 0, movesPerTemp, cool)
        self.c = c
        self.alpha = alpha
        self.prevAvgE = self.cost
        self.resetStats()

    def initTemp(self):
        moveDelta = []
        for j in xrange(0, 1000):
            delta = self.inst.genMove()
            moveDelta.append(delta)
        return self.INIT_TEMP_MULTIPLIER * np.std(moveDelta)

    def equilibrium(self, delta):
        if self.upCount + self.dnCount < self.TAKEN_SAMPLE_SIZE:
            if delta < 0.0:
                self.dnCount += 1
                self.dnSum += delta
            elif delta > 0.0:
                self.upCount += 1
                self.upSum += delta
            return False
        else:
            dnAvg = -1.0 * self.dnSum / self.dnCount
            upAvg = self.upSum / self.upCount
            self.upCount = 0
            self.dnCount = 0
            self.upSum = 0.0
            self.dnSum = 0.0
            if dnAvg < upAvg and upAvg / dnAvg < self.c or \
                                    dnAvg > upAvg and dnAvg / upAvg < self.c:
                return True
            else:
                return False

    def newTemp(self, temp, var):
        self.resetStats()
        if var == 0.0:
            return temp * self.cool
        dif = self.alpha * temp * temp / var
        if temp - dif < temp * self.cool:
            return temp * self.cool
        return temp - dif

    def optimize(self):
        moves = 0
        costList = []
        temp = self.initTemp()
        frozenCount = 0
        lastCost = 0
        while frozenCount < self.FROZEN and moves < self.MAXMOVES:
            equil = False
            self.upCount = 0
            self.upSum = 0.0
            self.dnCount = 0
            self.dnSum = 0.0
            tempCount = 0
            while not equil and tempCount < self.movesPerTemp:
                moves += 1
                tempCount += 1
                delta = self.inst.genMove()
                if self.metropolis(delta, temp):
                    self.commitMove(delta)
                    equil = self.equilibrium(delta)
            var = self.costVar()
            cost = self.inst.cost()
            if lastCost == cost:
                frozenCount += 1
            else:
                frozenCount = 0
            temp = self.newTemp(temp, var)
            tempCount = 0
            costList.append(moves)
            costList.append(cost)
            lastCost = cost
        return costList


if __name__ == '__main__':
    import TravSales

    inst = TravSales.TravSales()
    base = SA_SECS(inst, 500, 0.9, 1.025, 14)
    print base.optimize()
