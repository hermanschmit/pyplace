'''
sa_test1
'''

import copy

from pylab import *

import SA_ConstSpeed
import SA_SECS
import SA_SimpleEquil
import SA_WFF
import SA_base
import TravSales


def integral(costList):
    if len(costList) < 4:
        return 0.0

    def muldiff(x, y1, y0): return x * (y1 - y0)

    def add(x, y): return x + y

    return reduce(add, map(muldiff,
                           costList[3::2],
                           costList[2::2],
                           costList[0:-3:2]))


if __name__ == '__main__':
    inst = TravSales.TravSales()
    '''
    moves[1000,15000]
    cool[0.7, 0.96]
    speed[5, 15]
    c[0.25, 1.5]
    '''

    print "SA base sweeps:"
    bestFinal = -1.0
    bestIntegral = -1.0
    for moves in [1000, 5000, 10000, 15000]:
        for cool in [0.95, 0.9, 0.85, 0.8, 0.70]:
            instSA = copy.deepcopy(inst)
            base = SA_base.SA_base(instSA, 500.0, moves, cool)
            costList = base.optimize()
            if bestFinal == -1.0 or costList[-1] < bestFinal:
                bestFinal = costList[-1]
                bestFinalCostList = costList
                bestFinalParam = [moves, cool]
            intgrl = integral(costList)
            if bestIntegral == -1.0 or intgrl < bestIntegral:
                bestIntegral = intgrl
                bestIntegralCostList = costList
                bestIntegralParam = [moves, cool]

    print "Base: Best Final: ", bestFinalParam, \
        " Cost: ", bestFinalCostList[-2:]
    print "Base: Best Integral: ", bestIntegralParam, \
        " Cost: ", bestIntegralCostList[-2:]

    plot(bestFinalCostList[0::2], bestFinalCostList[1::2], 'go-',
         label='finalBase')
    plot(bestIntegralCostList[0::2], bestIntegralCostList[1::2], 'g*-',
         label='intBase')

    bestFinal = -1.0
    bestIntegral = -1.0

    for moves in [500, 1000, 2500]:
        for speed in [12, 13, 14]:
            for cool in [0.9, 0.93, 0.94]:
                instCS = copy.deepcopy(inst)
                constSp = SA_ConstSpeed.SA_ConstSpeed(instCS, moves, cool, speed)
                costList = constSp.optimize()
                if bestFinal == -1.0 or costList[-1] < bestFinal:
                    bestFinal = costList[-1]
                    bestFinalCostList = costList
                    bestFinalParam = [moves, speed]
                intgrl = integral(costList)
                if bestIntegral == -1.0 or intgrl < bestIntegral:
                    bestIntegral = intgrl
                    bestIntegralCostList = costList
                    bestIntegralParam = [moves, speed]

    print "CS: Best Final: ", bestFinalParam, \
        " Cost: ", bestFinalCostList[-2:]
    print "CS: Best Integral: ", bestIntegralParam, \
        " Cost: ", bestIntegralCostList[-2:]

    plot(bestFinalCostList[0::2], bestFinalCostList[1::2], 'bo-',
         label='finalCS')
    plot(bestIntegralCostList[0::2], bestIntegralCostList[1::2], 'b*-',
         label='intCS')

    bestFinal = -1.0
    bestIntegral = -1.0

    for moves in [1000, 5000, 8000]:
        for cool in [0.9, 0.93, 0.94]:
            for c in [0.25, 0.5, 0.75, 1.0, 1.25]:
                instWFF = copy.deepcopy(inst)
                wff = SA_WFF.SA_WFF(instWFF, moves, cool, c)
                costList = wff.optimize()
                if bestFinal == -1.0 or costList[-1] < bestFinal:
                    bestFinal = costList[-1]
                    bestFinalCostList = costList
                    bestFinalParam = [cool, c]
                intgrl = integral(costList)
                if bestIntegral == -1.0 or intgrl < bestIntegral:
                    bestIntegral = intgrl
                    bestIntegralCostList = costList
                    bestIntegralParam = [cool, c]

    print "WFF: Best Final: ", bestFinalParam, \
        " Cost: ", bestFinalCostList[-2:]
    print "WFF: Best Integral: ", bestIntegralParam, \
        " Cost: ", bestIntegralCostList[-2:]

    plot(bestFinalCostList[0::2], bestFinalCostList[1::2], 'ro-',
         label='finalCS')
    plot(bestIntegralCostList[0::2], bestIntegralCostList[1::2], 'r*-',
         label='intCS')

    bestFinal = -1.0
    bestIntegral = -1.0

    for cool in [0.87, 0.9, 0.93, 0.94, 0.95]:
        for c in [1.01, 1.02, 1.05, 1.1]:
            for moves in [1000, 5000, 8000]:
                instSE = copy.deepcopy(inst)
                se = SA_SimpleEquil.SA_SimpleEquil(instSE, moves, cool, c)
                costList = se.optimize()
                if bestFinal == -1.0 or costList[-1] < bestFinal:
                    bestFinal = costList[-1]
                    bestFinalCostList = costList
                    bestFinalParam = [cool, c]
                intgrl = integral(costList)
                if bestIntegral == -1.0 or intgrl < bestIntegral:
                    bestIntegral = intgrl
                    bestIntegralCostList = costList
                    bestIntegralParam = [cool, c]

    print "SE: Best Final: ", bestFinalParam, \
        " Cost: ", bestFinalCostList[-2:]
    print "SE: Best Integral: ", bestIntegralParam, \
        " Cost: ", bestIntegralCostList[-2:]

    plot(bestFinalCostList[0::2], bestFinalCostList[1::2], 'mo-',
         label='finalCS')
    plot(bestIntegralCostList[0::2], bestIntegralCostList[1::2], 'm*-',
         label='intCS')

    bestFinal = -1.0
    bestIntegral = -1.0

    for cool in [0.87, 0.9, 0.93, 0.94, 0.95]:
        for c in [1.01, 1.02, 1.05, 1.1]:
            for moves in [500, 1000, 2500]:
                instSECS = copy.deepcopy(inst)
                se = SA_SECS.SA_SECS(instSE, moves, cool, c, 14)
                costList = se.optimize()
                if bestFinal == -1.0 or costList[-1] < bestFinal:
                    bestFinal = costList[-1]
                    bestFinalCostList = costList
                    bestFinalParam = [cool, c]
                intgrl = integral(costList)
                if bestIntegral == -1.0 or intgrl < bestIntegral:
                    bestIntegral = intgrl
                    bestIntegralCostList = costList
                    bestIntegralParam = [cool, c]

    print "SE: Best Final: ", bestFinalParam, \
        " Cost: ", bestFinalCostList[-2:]
    print "SE: Best Integral: ", bestIntegralParam, \
        " Cost: ", bestIntegralCostList[-2:]

    plot(bestFinalCostList[0::2], bestFinalCostList[1::2], 'yo-',
         label='finalCS')
    plot(bestIntegralCostList[0::2], bestIntegralCostList[1::2], 'y*-',
         label='intCS')

    show()

    print bestFinalCostList
