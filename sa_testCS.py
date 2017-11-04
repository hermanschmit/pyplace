'''
sa_test1
'''

import math
import random

import numpy as np
from pylab import *

import TravSales


def accept(delta, temp):
    if delta < 0.0:
        return True
    rand = random.random()
    e = math.exp(-1.0 * (delta / temp))
    if rand < e:
        return True
    return False


def newTemp(temp, var, c):
    if var == 0:
        return temp / 2.0

    dif = c * temp * temp / var
    if temp < dif:
        return temp / 2.0
    return temp - c * temp * temp / var


if __name__ == '__main__':
    costList = []
    moves = 0
    inst = TravSales.TravSales()
    print "Initial: ", inst.cost()
    moveDelta = []
    for j in xrange(1, 1000):
        delta = inst.genMove()
        moveDelta.append(delta)
        inst.commitMove()
    temp = 2 * np.std(moveDelta)
    print "Start Temp:", temp

    for i in xrange(1, 150):
        moveDelta = []
        acceptDelta = []
        for j in xrange(1, 10000):
            moves += 1
            delta = inst.genMove()
            moveDelta.append(delta)
            if accept(delta, temp):
                inst.commitMove()
                acceptDelta.append(delta)
        if len(acceptDelta) > 0:
            std = np.std(acceptDelta)
        else:
            std = 0

        temp = newTemp(temp, std * std, 5)
        print "Temp: ", temp
        costList.append(moves)
        costList.append(inst.cost())

        #        inst.plotPath()
        #        show()
        print "moveDelta   (avg): ", np.mean(moveDelta)
        print "moveDelta   (std): ", np.std(moveDelta)
        if len(acceptDelta) > 0:
            print "acceptDelta (avg): ", np.mean(acceptDelta)
            print "acceptDelta (std): ", np.std(acceptDelta)

        print "Cost: ", inst.cost()
    print "Final: ", inst.cost()
    plot(costList[0::2], costList[1::2], 'go-')
    show()
