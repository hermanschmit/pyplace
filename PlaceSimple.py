'''
PlaceSimple

Create random graph.
Place in grid

'''
import math
import random

import networkx
from pylab import *


def hyp(ax, ay, bx, by):
    xdiff = ax - bx
    ydiff = ay - by
    return math.hypot(xdiff, ydiff)


class PlaceSimple(object):
    def __init__(self, seed=40):
        self.dimension = 9
        self.OrderedList = list()
        self.num = self.dimension * self.dimension

        self.candidateMove = [0, 0]
        # self.G = networkx.barabasi_albert_graph(self.num,3)
        self.G = networkx.grid_graph(dim=[self.dimension, self.dimension])
        x = 0
        y = 0
        for n in self.G.nodes():
            self.G.node[n] = (x, y)
            y += 1
            if y == self.dimension:
                x += 1
                y = 0
        for n, nbrs in self.G.adj.items():
            for nbr, eattr in nbrs.items():
                self.G.edge[n][nbr]['weight'] = 1.0

        self.currentCost = self.cost()
        self.currentDelta = 0

    def genMove(self):
        delta = 0.
        self.candidateMove = [0, 0]

        def validMove():
            if self.candidateMove[0] == self.candidateMove[1]:
                return False
            return True

        while not validMove():
            self.candidateMove = [random.choice(list(self.G.node)),
                                  random.choice(list(self.G.node))]

        pos0 = self.G.node[self.candidateMove[0]]
        pos1 = self.G.node[self.candidateMove[1]]

        for nbr in networkx.all_neighbors(self.G, self.candidateMove[0]):
            if nbr == self.candidateMove[1]:
                continue
            nbrpos = self.G.node[nbr]
            delta += hyp(*(nbrpos + pos1))
            delta -= hyp(*(nbrpos + pos0))

        for nbr in networkx.all_neighbors(self.G, self.candidateMove[1]):
            if nbr == self.candidateMove[0]:
                continue
            nbrpos = self.G.node[nbr]
            delta += hyp(*(nbrpos + pos0))
            delta -= hyp(*(nbrpos + pos1))

        return delta

    def cost(self):
        accumCost = 0.
        for (u, v, d) in self.G.edges(data=True):
            wt = d['weight']
            pos1 = self.G.node[u]
            pos2 = self.G.node[v]
            dist = hyp(*(pos1 + pos2))
            accumCost += dist * wt
        return accumCost

    def commitMove(self):
        (self.G.node[self.candidateMove[1]], self.G.node[self.candidateMove[0]]) = \
            (self.G.node[self.candidateMove[0]], self.G.node[self.candidateMove[1]])
        self.candidateMove = [0, 0]
        self.currentCost += self.currentDelta


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    inst = PlaceSimple()
    icost = inst.cost()
    print "Initial: ", icost
    cost = icost
    for i in xrange(1, 10):
        d = inst.genMove()
        print "Delta:", d
        print "Move:", inst.candidateMove
        inst.commitMove()
        cost += d
        actualcost = inst.cost()
        print "New Cost", cost
        print "Actual Cost", actualcost
        if abs(cost - actualcost) > 0.000001:
            print '********'
            sys.exit()
        else:
            print '--------'
        cost = actualcost

    networkx.draw(inst.G, pos=inst.G.node)
    plt.show()

    for i in xrange(1, 100000):
        d = inst.genMove()
        if d <= 0.:
            inst.commitMove()

    networkx.draw(inst.G, pos=inst.G.node)
    plt.show()
