import networkx
from pylab import *

import PlaceSite
import SA_base

if __name__ == '__main__':

    SIZE = 1024
    g = networkx.barabasi_albert_graph(SIZE, 3)

    moves = 2000
    cool = 0.97
    t0 = 2000.0
    results = list()

    exp = 0.0
    for stride in [32, 16, 8, 4, 0]:
        inst = PlaceSite.PlaceSite(graph=g, stride=stride)
        print "stride: ", stride
        print "Initial cost: ", inst.cost()
        base = SA_base.SA_base(inst, t0, moves, cool)
        costList = base.optimize()
        print "Final cost (1.0): ", inst.cost(weighted=False)
        print "Final cost (wtd): ", inst.cost(weighted=True)
        print "CostList: ", costList
        results.append((exp, stride, cool, t0, moves, inst.cost(weighted=True), inst.cost(weighted=False)))
        inst.G.draw()
        fname = "place_size%d_stride%03d_flat.svg" % (SIZE, stride)
        savefig(fname)

    exp = 1.0
    for stride in [32, 16, 8, 4, 0]:
        inst = PlaceSite.PlaceSite(graph=g, stride=stride, exp=exp)
        print "stride: ", stride
        print "Initial cost: ", inst.cost()
        base = SA_base.SA_base(inst, t0, moves, cool)
        costList = base.optimize()
        print "Final cost (1.0): ", inst.cost(weighted=False)
        print "Final cost (wtd): ", inst.cost(weighted=True)
        print "CostList: ", costList
        results.append((exp, stride, cool, t0, moves, inst.cost(weighted=True), inst.cost(weighted=False)))

        inst.G.draw()
        fname = "place_size%d_stride%03d_exp%.1f.svg" % (SIZE, stride, exp)
        savefig(fname)

    exp = 2.
    for stride in [32, 16, 8, 4, 0]:
        inst = PlaceSite.PlaceSite(graph=g, stride=stride, exp=exp)
        print "stride: ", stride
        print "Initial cost: ", inst.cost()
        base = SA_base.SA_base(inst, t0, moves, cool)
        costList = base.optimize()
        print "Final cost (1.0): ", inst.cost(weighted=False)
        print "Final cost (wtd): ", inst.cost(weighted=True)
        print "CostList: ", costList
        results.append((exp, stride, cool, t0, moves, inst.cost(weighted=True), inst.cost(weighted=False)))

        inst.G.draw()
        fname = "place_size%d_stride%03d_exp%.1f.svg" % (SIZE, stride, exp)
        savefig(fname)

    exp = 3.
    for stride in [32, 16, 8, 4, 0]:
        inst = PlaceSite.PlaceSite(graph=g, stride=stride, exp=exp)
        print "stride: ", stride
        print "Initial cost: ", inst.cost()
        base = SA_base.SA_base(inst, t0, moves, cool)
        costList = base.optimize()
        print "Final cost (1.0): ", inst.cost(weighted=False)
        print "Final cost (wtd): ", inst.cost(weighted=True)
        print "CostList: ", costList
        results.append((exp, stride, cool, t0, moves, inst.cost(weighted=True), inst.cost(weighted=False)))

        inst.G.draw()
        fname = "place_size%d_stride%03d_exp%.1f.svg" % (SIZE, stride, exp)
        savefig(fname)

    exp = 4.
    for stride in [32, 16, 8, 4, 0]:
        inst = PlaceSite.PlaceSite(graph=g, stride=stride, exp=exp)
        print "stride: ", stride
        print "Initial cost: ", inst.cost()
        base = SA_base.SA_base(inst, t0, moves, cool)
        costList = base.optimize()
        print "Final cost (1.0): ", inst.cost(weighted=False)
        print "Final cost (wtd): ", inst.cost(weighted=True)
        print "CostList: ", costList
        results.append((exp, stride, cool, t0, moves, inst.cost(weighted=True), inst.cost(weighted=False)))

        inst.G.draw()
        fname = "place_size%d_stride%03d_exp%.1f.svg" % (SIZE, stride, exp)
        savefig(fname)

    exp = 5.
    for stride in [32, 16, 8, 4, 0]:
        inst = PlaceSite.PlaceSite(graph=g, stride=stride, exp=exp)
        print "stride: ", stride
        print "Initial cost: ", inst.cost()
        base = SA_base.SA_base(inst, t0, moves, cool)
        costList = base.optimize()
        print "Final cost (1.0): ", inst.cost(weighted=False)
        print "Final cost (wtd): ", inst.cost(weighted=True)
        print "CostList: ", costList
        results.append((exp, stride, cool, t0, moves, inst.cost(weighted=True), inst.cost(weighted=False)))

        inst.G.draw()
        fname = "place_size%d_stride%03d_exp%.1f.svg" % (SIZE, stride, exp)
        savefig(fname)

    import csv

    with open('results.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Exp', 'Stride', 'Cool', 't0', 'Moves', 'costWeighted', 'costFlat'])
        for r in results:
            writer.writerow(r)
    csvfile.close()
    print results
