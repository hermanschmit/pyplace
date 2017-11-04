'''
TravSales Inst
Use as a proto for a base class of SA problem definitions
'''
import math
import random

from pylab import *


def hyp(ax, ay, bx, by):
    xdiff = ax - bx
    ydiff = ay - by
    return math.hypot(xdiff, ydiff)


class TravSales(object):
    def __init__(self, seed=40):
        self.dimension = 500
        self.OrderedList = dict()
        self.num = 100
        self.candidateMove = [0, 0]
        random.seed(seed)
        for i in xrange(0, self.num):
            self.OrderedList[i] = ((random.random() * self.dimension),
                                   (random.random() * self.dimension))
        self.currentCost = self.cost()
        self.currentDelta = 0

    def genMove(self):
        self.candidateMove = [0, 0]

        def validMove():
            if self.candidateMove[0] == self.candidateMove[1]:
                return False
            if self.candidateMove[0] - self.candidateMove[1] == 1:
                return False
            if self.candidateMove[1] - self.candidateMove[0] == 1:
                return False
            if self.candidateMove[0] == 0:
                return False
            if self.candidateMove[0] == self.num - 1:
                return False
            if self.candidateMove[1] == 0:
                return False
            if self.candidateMove[1] == self.num - 1:
                return False
            return True

        while not validMove():
            self.candidateMove = [int(random.random() * self.num),
                                  int(random.random() * self.num)]
        a = self.candidateMove[0]
        b = self.candidateMove[1]
        delta = (hyp(*(self.OrderedList[a - 1] + self.OrderedList[b]))
                 + hyp(*(self.OrderedList[b] + self.OrderedList[a + 1]))
                 + hyp(*(self.OrderedList[b - 1] + self.OrderedList[a]))
                 + hyp(*(self.OrderedList[a] + self.OrderedList[b + 1]))
                 - hyp(*(self.OrderedList[a - 1] + self.OrderedList[a]))
                 - hyp(*(self.OrderedList[a + 1] + self.OrderedList[a]))
                 - hyp(*(self.OrderedList[b - 1] + self.OrderedList[b]))
                 - hyp(*(self.OrderedList[b + 1] + self.OrderedList[b])))

        self.currentDelta = delta

        return delta

    def cost(self):
        accumCost = 0.
        for i in xrange(0, self.num - 1):
            accumCost += hyp(*(self.OrderedList[i] + self.OrderedList[i + 1]))
        return accumCost

    def commitMove(self):
        (self.OrderedList[self.candidateMove[0]],
         self.OrderedList[self.candidateMove[1]]) = \
            (self.OrderedList[self.candidateMove[1]],
             self.OrderedList[self.candidateMove[0]])
        self.candidateMove = [0, 0]
        self.currentCost += self.currentDelta

    def plotPath(self):
        xList = []
        yList = []
        for (i, v) in self.OrderedList.items():
            xList.append(v[0])
            yList.append(v[1])
        plot(xList, yList, 'go-')


if __name__ == '__main__':
    inst = TravSales()
    icost = inst.cost()
    print "Initial: ", icost
    cost = icost

    for i in xrange(1, 5):
        d = inst.genMove()
        print "Delta:", d
        inst.commitMove()
        inst.plotPath()
        show()
        cost += d

    print "Cost: ", cost
    print "Full Cost: ", inst.cost()
