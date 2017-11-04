'''
SA_base
'''
import SA_base


class SA_vpr(SA_base.SA_base):
    FROZEN = 3
    MAXMOVES = 1000000

    def __init__(self, problemInst, t0=500.0, movesPerTemp=500, cool=1.0):
        SA_base.SA_base.__init__(self, problemInst, t0, movesPerTemp, cool)

    def newTemp(self, temp, accept):
        self.resetStats()
        if accept > 0.96: return temp * 0.45 * self.cool
        if accept > 0.8:  return temp * 0.8 * self.cool
        if accept > 0.15: return temp * 0.86 * self.cool
        return temp * 0.73 * self.cool

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
            temp = self.newTemp(temp, (1.0 * self.tcount) / self.movesPerTemp)
            costList.append(moves)
            costList.append(cost)
            lastCost = cost
        return costList


if __name__ == '__main__':
    import TravSales

    inst = TravSales.TravSales()
    base = SA_vpr(inst, 500, 10000)
    print base.optimize()
