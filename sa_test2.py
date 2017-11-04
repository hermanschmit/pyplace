'''
sa_test2
'''

import copy
from multiprocessing import Pool

from pylab import *

import SA_base
import TravSales


def paraOptimize(instP, optCls, args):
    instSA = optCls(copy.deepcopy(instP), **args)
    return [args, instSA.optimize()]


if __name__ == '__main__':
    inst = TravSales.TravSales()
    pool = Pool(processes=8)

    results = [pool.apply_async(paraOptimize, a) for a in [(inst, SA_base.SA_base, {'cool': 0.9,
                                                                                    'movesPerTemp': 10000}),
                                                           (inst, SA_base.SA_base,
                                                            {'cool': 0.89, 'movesPerTemp': 10000}),
                                                           (inst, SA_base.SA_base,
                                                            {'cool': 0.88, 'movesPerTemp': 10000}),
                                                           (inst, SA_base.SA_base,
                                                            {'cool': 0.87, 'movesPerTemp': 10000}),
                                                           (inst, SA_base.SA_base,
                                                            {'cool': 0.86, 'movesPerTemp': 10000}),
                                                           (inst, SA_base.SA_base,
                                                            {'cool': 0.85, 'movesPerTemp': 10000}),
                                                           (
                                                           inst, SA_base.SA_base, {'cool': 0.84, 'movesPerTemp': 10000})
                                                           ]]
    print [r.get() for r in results]

##    result1 = pool.apply_async(paraOptimize,(inst,10000))
##    result2 = pool.apply_async(paraOptimize,(inst,15000))
##    result3 = pool.apply_async(paraOptimize,(inst,20000))
##    result4 = pool.apply_async(paraOptimize,(inst,30000))
##    result5 = pool.apply_async(paraOptimize,(inst,40000))
##
##    print result1.get(timeout=60)
##    print result2.get(timeout=60)
##    print result3.get(timeout=60)
##    print result4.get(timeout=60)
##
##    print result5.get(timeout=60)
