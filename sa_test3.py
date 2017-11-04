'''
sa_test3
'''

import copy
import math
from multiprocessing import Pool

from pylab import *

import SA_ConstSpeed
import SA_SECS
import SA_SimpleEquil
import SA_WFF
import SA_base
import SA_vpr
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


def paraOpt(instP, optimCls, args):
    instSA = optimCls(copy.deepcopy(instP), **args)
    return [args, instSA.optimize()]


def createFrontier(dim, center, reach=1):
    returnList = [center]
    for k in center:
        argRange = dim[k]
        idx = argRange.index(center[k])
        # always do neighbors
        if idx > 0:
            newArg = copy.deepcopy(center)
            newArg[k] = argRange[idx - 1]
            returnList.append(newArg)
        if idx + 1 < len(argRange):
            newArg = copy.deepcopy(center)
            newArg[k] = argRange[idx + 1]
            returnList.append(newArg)

        if idx >= reach and reach > 1:
            newArg = copy.deepcopy(center)
            newArg[k] = argRange[idx - reach]
            returnList.append(newArg)
        if idx < len(argRange) - reach and reach > 1:
            newArg = copy.deepcopy(center)
            newArg[k] = argRange[idx + reach]
            returnList.append(newArg)
    return returnList


def getBestResults(rlist):
    best = None
    for r in rlist:
        if best == None or r[1][-1] < best[1][-1]:
            best = r
    return best[0], best[1]


def paramSearch(current, dimen, optObj):
    best = None
    reach = 4
    count = 0
    while current != best or count <= 4:
        best = current
        front = createFrontier(dimen, current, reach)
        execute = [(inst, optObj, x) for x in front]
        rx = [pool.apply_async(paraOpt, a) for a in execute]
        results = [r.get() for r in rx]
        (current, bestResult) = getBestResults(results)
        count += 1
        if count % 3 == 0 and reach > 1:
            reach -= 1
    return (current, bestResult)


if __name__ == '__main__':
    print 'starting'
    inst = TravSales.TravSales()
    '''
    moves[1000,15000]
    cool[0.7, 0.96]
    speed[5, 15]
    c[0.25, 1.5]
    '''

    pool = Pool(processes=7)

    dimen = {'cool': [1.0 - x * 0.01 for x in range(1, 20)],
             'movesPerTemp': [int(math.pow(2.0, y)) for y in range(6, 16)]}
    current = {'cool': 0.90, 'movesPerTemp': 1024}
    (current, bestResult) = paramSearch(current, dimen, SA_base.SA_base)

    print "Base: Best Final: ", current, \
        " Cost: ", bestResult[-2:]
    plot(bestResult[0::2], bestResult[1::2], 'go-', label='base')

    legend()

    show()

    dimen = {'cool': [1.0 - x * 0.01 for x in range(1, 20)],
             'movesPerTemp': [int(math.pow(2.0, y)) for y in range(6, 16)],
             'alpha': range(9, 17, 1)}
    current = {'cool': 0.90, 'movesPerTemp': 1024, 'alpha': 12}
    (current, bestResult) = paramSearch(current, dimen, SA_ConstSpeed.SA_ConstSpeed)

    print "CS: Best Final: ", current, \
        " Cost: ", bestResult[-2:]
    plot(bestResult[0::2], bestResult[1::2], 'bo-', label='CS')

    dimen = {'cool': [1.0 - x * 0.01 for x in range(1, 20)],
             'movesPerTemp': [int(math.pow(2.0, y)) for y in range(6, 16)],
             'c': [x * 0.25 for x in range(1, 10)]}
    current = {'cool': 0.90, 'movesPerTemp': 1024, 'c': 0.75}
    (current, bestResult) = paramSearch(current, dimen, SA_WFF.SA_WFF)

    print "WFF: Best Final: ", current, \
        " Cost: ", bestResult[-2:]
    plot(bestResult[0::2], bestResult[1::2], 'ro-', label='WFF')

    dimen = {'cool': [1.0 - x * 0.01 for x in range(1, 20)],
             'movesPerTemp': [int(math.pow(2.0, y)) for y in range(6, 16)],
             'c': [1.0 + x * 0.025 for x in range(1, 20)]}
    current = {'cool': 0.90, 'movesPerTemp': 1024, 'c': 1.05}
    (current, bestResult) = paramSearch(current, dimen, SA_SimpleEquil.SA_SimpleEquil)

    print "SE: Best Final: ", current, \
        " Cost: ", bestResult[-2:]
    plot(bestResult[0::2], bestResult[1::2], 'mo-', label='SE')

    dimen = {'cool': [1.0 - x * 0.01 for x in range(1, 20)],
             'movesPerTemp': [int(math.pow(2.0, y)) for y in range(6, 16)],
             'c': [1.0 + x * 0.025 for x in range(1, 20)],
             'alpha': range(9, 17, 1)}
    current = {'cool': 0.90, 'movesPerTemp': 1024, 'c': 1.05, 'alpha': 12}
    (current, bestResult) = paramSearch(current, dimen, SA_SECS.SA_SECS)

    print "SECS: Best Final: ", current, \
        " Cost: ", bestResult[-2:]
    plot(bestResult[0::2], bestResult[1::2], 'yo-', label='SECS')

    dimen = {'cool': [1.1 - x * 0.01 for x in range(0, 20)],
             'movesPerTemp': [int(math.pow(2.0, y)) for y in range(6, 16)]}
    current = {'cool': 1.0, 'movesPerTemp': 1024}
    (current, bestResult) = paramSearch(current, dimen, SA_vpr.SA_vpr)

    print "VPR: Best Final: ", current, \
        " Cost: ", bestResult[-2:]
    plot(bestResult[0::2], bestResult[1::2], 'co-', label='VPR')

    legend()

    show()
