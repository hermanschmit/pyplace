'''
SA_ConstSpeed
'''

import numpy as np

import SA_base


class SA_ConstSpeed(SA_base.SA_base):
    INIT_TEMP_MULTIPLIER = 2.0
    TINY_COOL = 0.999
    FROZEN = 10

    def __init__(self, problemInst, movesPerTemp=500, cool=0.9, alpha=10):
        SA_base.SA_base.__init__(self, problemInst, 0.0, movesPerTemp, cool)
        self.alpha = alpha

    def initTemp(self):
        moveDelta = []
        for j in xrange(0, self.movesPerTemp):
            delta = self.inst.genMove()
            moveDelta.append(delta)
        return self.INIT_TEMP_MULTIPLIER * np.std(moveDelta)

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
            for j in xrange(0, self.movesPerTemp):
                moves += 1
                delta = self.inst.genMove()
                if self.metropolis(delta, temp):
                    self.commitMove(delta)
            var = self.costVar()
            if lastCost == self.cost:
                frozenCount += 1
            else:
                frozenCount = 0
            temp = self.newTemp(temp, var)
            costList.append(moves)
            costList.append(self.cost)
            lastCost = self.cost
        return costList


if __name__ == '__main__':
    import TravSales

    inst = TravSales.TravSales()
    base = SA_ConstSpeed(inst, 1000, 0.9, 10)
    print base.optimize()
