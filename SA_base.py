'''
SA_base
'''
import math
import random


class SA_base(object):
    FROZEN = 3
    MAXMOVES = 1000000

    def __init__(self, problemInst, t0=500.0, movesPerTemp=500, cool=0.9):
        self.inst = problemInst
        self.t0 = t0
        self.cool = cool
        self.movesPerTemp = movesPerTemp
        self.cost = self.inst.cost()
        self.resetStats()
        print "SA_base: t0, %f, movesPerTemp, %d, cool, %f" % (t0, movesPerTemp, cool)
        random.seed(25)

    def metropolis(self, delta, temp):
        if delta <= 0.0:
            return True
        rand = random.random()
        e = math.exp(-1.0 * (delta / temp))
        if rand < e:
            return True
        return False

    def updateStats(self):
        self.q += self.tcount * (self.cost - self.m) * (self.cost - self.m) / (self.tcount + 1)
        self.m += (self.cost - self.m) / (self.tcount + 1)
        self.sum += self.cost
        self.tcount += 1

    def resetStats(self):
        self.tcount = 0
        self.m = 0
        self.q = 0
        self.sum = 0

    def costMean(self):
        if self.tcount == 0: return self.cost
        return self.sum / self.tcount

    def costStdDev(self):
        if self.tcount == 0: return 0.0
        return math.sqrt(self.q / self.tcount)

    def costVar(self):
        if self.tcount == 0: return 0.0
        return self.q / self.tcount

    def commitMove(self, delta):
        self.inst.commitMove()
        self.cost += delta
        self.updateStats()

    def newTemp(self, temp):
        self.resetStats()
        return temp * self.cool

    def optimize(self):
        moves = 0
        costList = []
        temp = self.t0
        frozenCount = 0
        lastCost = 0
        while frozenCount < self.FROZEN and moves < self.MAXMOVES:
            for j in xrange(0, self.movesPerTemp):
                moves += 1
                delta = self.inst.genMove()
                if self.metropolis(delta, temp):
                    self.commitMove(delta)
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
    base = SA_base(inst, 500, 10000, 0.9)
    print base.optimize()
