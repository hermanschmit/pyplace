import copy

from pylab import *

import PlaceSite
import SA_base

if __name__ == '__main__':
    inst = PlaceSite.PlaceSite(graphsize=256, stride=16)
    '''
    moves[1000,15000]
    cool[0.7, 0.96]
    speed[5, 15]
    c[0.25, 1.5]
    '''

    print "Initial cost: ", inst.cost()

    print "SA base sweeps:"
    bestFinal = -1.0
    bestIntegral = -1.0
    # for moves in [1000, 5000, 10000, 15000, 20000, 25000]:
    for moves in [25000]:
        # for cool in [0.95, 0.9, 0.85, 0.8, 0.70]:
        for cool in [0.70]:
            instSA = copy.deepcopy(inst)
            base = SA_base.SA_base(instSA, 500.0, moves, cool)
            costList = base.optimize()
            if bestFinal == -1.0 or costList[-1] < bestFinal or \
                    (costList[-1] == bestFinal and len(costList) < len(bestFinalCostList)):
                bestFinal = costList[-1]
                bestFinalCostList = costList
                bestFinalParam = [moves, cool]
                print bestFinal

    print "Base: Best Final: ", bestFinalParam, \
        " Cost: ", bestFinalCostList[-2:]

    plot(bestFinalCostList[0::2], bestFinalCostList[1::2], 'go-',
         label='finalBase')

    bestFinal = -1.0

    show()

    inst.G.draw()
    show()
