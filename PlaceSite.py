'''
PlaceSimple

Create random graph.
Place in grid

'''

import random

import networkx
from pylab import *

import MemFuncGraph


def hyp(ax, ay, bx, by):
    xdiff = ax - bx
    ydiff = ay - by
    return math.hypot(xdiff, ydiff)


class PlaceSite(object):
    def site1D(self, x):
        z = (x + self.stride / 4) % (self.stride + self.stride / 2)
        if z < self.stride / 2:
            return 'm'
        else:
            return 'f'

    def site(self, x, y):
        if self.stride == 0:
            if x % 2 ^ y % 2 == 1:
                return 'm'
            else:
                return 'f'

        xt = self.site1D(x)
        yt = self.site1D(y)
        if xt == 'f' and yt == 'f':
            return 'f'
        if xt != yt and xt == 'm' or yt == 'm':
            return 'm'
        return 'x'

    def __init__(self, graphsize=64, stride=4, seed=40, graph=None, exp=0.0):
        random.seed(seed)
        self.stride = stride
        self.exp = exp
        if (stride < 4 and stride > 0) or stride < 0:
            self.stride = 4
        self.OrderedList = list()
        self.candidateMove = [0, 0]
        if graph is None:
            self.G = MemFuncGraph.MemFuncGraph(graphsize=graphsize, exp=exp)
        else:
            self.G = MemFuncGraph.MemFuncGraph(graph=graph, exp=exp)

        self.num = len(self.G.node)
        if self.stride == 0:
            self.dimension = int(ceil(sqrt(self.num)))
        else:
            d = ceil(sqrt(self.num / 2))
            d2 = ceil(d / self.stride) * self.stride * 1.5
            self.dimension = int(d2)

        self.numT = {}

        self.siteList = dict()
        for t in ['m', 'f']:
            self.numT[t] = len([sNode for sNode in filter(lambda x: x[1]['type'] == t,
                                                          self.G.nodes(data=True))])
            self.siteList[t] = list()

        for x in xrange(self.dimension):
            for y in xrange(self.dimension):
                self.siteList[self.site(x, y)].append((x, y))

        self.initMap = [[None for y in xrange(self.dimension)] for x in xrange(self.dimension)]

        i = 0
        for n in self.G.nodes():
            t = self.G.node[n]['type']
            (x, y) = random.choice(self.siteList[t])

            self.G.node[n]['loc'] = (x, y)
            self.siteList[t].remove((x, y))
            self.initMap[x][y] = n
            i += 1

        for t in ['m', 'f']:
            while len(self.siteList[t]) > 0:
                (x, y) = self.siteList[t].pop()
                assert (self.initMap[x][y] is None)
                self.G.add_node(i, type=t, loc=(x, y))
                self.initMap[x][y] = self.G.node[i]
                i += 1

        self.currentCost = self.cost()
        self.currentDelta = 0

    def genMove(self):
        delta = 0.
        self.candidateMove = [0, 0]

        def validMove():
            if self.candidateMove[0] == self.candidateMove[1]:
                return False
            if self.G.node[self.candidateMove[0]]['type'] != self.G.node[self.candidateMove[1]]['type']:
                return False
            return True

        while not validMove():
            self.candidateMove = [random.choice(list(self.G.node)),
                                  random.choice(list(self.G.node))]

        pos0 = self.G.node[self.candidateMove[0]]['loc']
        pos1 = self.G.node[self.candidateMove[1]]['loc']

        for nbr in networkx.all_neighbors(self.G, self.candidateMove[0]):
            if nbr == self.candidateMove[1]:
                continue
            nbrpos = self.G.node[nbr]['loc']
            if self.exp:
                w = self.G.adj[self.candidateMove[0]][nbr]['weight']
            else:
                w = 1.0
            delta += w * hyp(*(nbrpos + pos1))
            delta -= w * hyp(*(nbrpos + pos0))

        for nbr in networkx.all_neighbors(self.G, self.candidateMove[1]):
            if nbr == self.candidateMove[0]:
                continue
            nbrpos = self.G.node[nbr]['loc']
            if self.exp:
                w = self.G.adj[self.candidateMove[1]][nbr]['weight']
            else:
                w = 1.0
            delta += w * hyp(*(nbrpos + pos0))
            delta -= w * hyp(*(nbrpos + pos1))

        return delta

    def cost(self, weighted=True):
        accumCost = 0.

        for (u, v, d) in self.G.edges(data=True):
            if weighted:
                wt = d['weight']
            else:
                wt = 1.0

            pos1 = self.G.node[u]['loc']
            pos2 = self.G.node[v]['loc']
            dist = hyp(*(pos1 + pos2))
            accumCost += dist * wt
        return accumCost

    def commitMove(self):
        loc0 = self.G.node[self.candidateMove[0]]['loc']
        loc1 = self.G.node[self.candidateMove[1]]['loc']
        self.G.node[self.candidateMove[0]]['loc'] = loc1
        self.G.node[self.candidateMove[1]]['loc'] = loc0
        self.candidateMove = [0, 0]
        self.currentCost += self.currentDelta


def test1(inst):
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


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    inst = PlaceSite()
    test1(inst)
    inst.G.draw()
    plt.show()

    for i in xrange(1, 100):
        d = inst.genMove()
        if d <= 0.:
            inst.commitMove()

    inst.G.draw()
    plt.show()

    inst = PlaceSite(exp=10.)
    test1(inst)
    inst.G.draw()
    plt.show()

    for i in xrange(1, 1000):
        d = inst.genMove()
        if d <= 0.:
            inst.commitMove()

    inst.G.draw()
    plt.show()
