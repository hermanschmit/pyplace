import math

import matplotlib.pyplot as plt
import numpy as np

size = 1000000
x1 = np.random.exponential(scale=1.0, size=size)
x1_2 = x1 ** 2
x1_2 = x1_2 / 2
x1_3 = (x1 ** 3) / math.factorial(3)
x1_4 = (x1 ** 4) / math.factorial(4)
x100 = np.random.exponential(scale=100, size=size)
x100 /= 100
print x1.mean()
print x1_2.mean()
print x1_3.mean()
print x1_4.mean()
print x100.mean()

bins = np.arange(0, 20.0, 0.1)
# the histogram of the data
plt.hist(x1, bins, normed=1, facecolor='green')
plt.hist(x100, bins, normed=1, facecolor='red')
plt.hist(x1_2, bins, normed=1, facecolor='yellow')
plt.hist(x1_3, bins, normed=1, facecolor='white')
plt.hist(x1_4, bins, normed=1, facecolor='blue')

# add a 'best fit' line
# y = mlab.normpdf( bins, mu, sigma)
# l = plt.plot(bins, 'r--', linewidth=1)

plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.grid(True)

plt.show()
