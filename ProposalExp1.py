import networkx
from pylab import *

import PlaceSite
import SA_SECS
import SA_SimpleEquil
import SA_base

if __name__ == '__main__':

    SIZE = 1024
    g = networkx.barabasi_albert_graph(SIZE, 3)

    moves = 1000
    cool = 0.99
    t0 = 10000.0
    results = list()

    for exp in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]:
        for stride in [32, 16, 8, 4, 0]:
            inst = PlaceSite.PlaceSite(graph=g, stride=stride, exp=exp)
            print "stride: ", stride
            print "Initial cost: ", inst.cost()
            base = SA_base.SA_base(inst, t0, moves, cool)
            costList = base.optimize()
            print "Final cost (1.0): ", inst.cost(weighted=False)
            print "Final cost (wtd): ", inst.cost(weighted=True)
            print "CostList: ", costList
            results.append(
                ("SA_base", exp, stride, cool, t0, moves, inst.cost(weighted=True), inst.cost(weighted=False)))
            inst.G.draw()
            fname = "placeSAbase_size%d_stride%03d_flat.svg" % (SIZE, stride)
            savefig(fname)

    for exp in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]:
        for stride in [32, 16, 8, 4, 0]:
            inst = PlaceSite.PlaceSite(graph=g, stride=stride, exp=exp)
            print "stride: ", stride
            print "Initial cost: ", inst.cost()
            base = SA_SimpleEquil.SA_SimpleEquil(inst, movesPerTemp=moves, cool=cool)
            costList = base.optimize()
            print "Final cost (1.0): ", inst.cost(weighted=False)
            print "Final cost (wtd): ", inst.cost(weighted=True)
            print "CostList: ", costList
            results.append(("SA_SE", exp, stride, cool, t0, moves, inst.cost(weighted=True), inst.cost(weighted=False)))
            inst.G.draw()
            fname = "placeSASE_size%d_stride%03d_flat.svg" % (SIZE, stride)
            savefig(fname)

    for exp in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]:
        for stride in [32, 16, 8, 4, 0]:
            inst = PlaceSite.PlaceSite(graph=g, stride=stride, exp=exp)
            print "stride: ", stride
            print "Initial cost: ", inst.cost()
            base = SA_SECS.SA_SECS(inst, movesPerTemp=moves, cool=cool)
            costList = base.optimize()
            print "Final cost (1.0): ", inst.cost(weighted=False)
            print "Final cost (wtd): ", inst.cost(weighted=True)
            print "CostList: ", costList
            results.append(("SECS", exp, stride, cool, t0, moves, inst.cost(weighted=True), inst.cost(weighted=False)))
            inst.G.draw()
            fname = "placeSASECS_size%d_stride%03d_flat.svg" % (SIZE, stride)
            savefig(fname)

    import csv

    with open('results.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Alg', 'Exp', 'Stride', 'Cool', 't0', 'Moves', 'costWeighted', 'costFlat'])
        for r in results:
            writer.writerow(r)
    csvfile.close()
    print results
