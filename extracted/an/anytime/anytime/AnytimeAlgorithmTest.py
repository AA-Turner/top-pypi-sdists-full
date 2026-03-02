#!python3

"""
A test for the generic AnytimeAlgorithm module.
Finds the maximum of a vector; stops at timeout and returns the best so far.
"""

import random, numpy as np
from AnytimeAlgorithm2 import AnytimeAlgorithm

class MaximumFinder(AnytimeAlgorithm):
    def __init__(self, vector):
        self.vector = vector
        self.currentMaximum = 0

    def update(self):
        i = random.randint(0,len(self.vector)-1)
        if self.vector[i]>self.currentMaximum:
            self.currentMaximum = self.vector[i]
            print("self",self,"result",self.currentMaximum)

    def result(self):
        return self.currentMaximum

v = np.random.rand(10000000)
finder = MaximumFinder(v)
print(finder.result_after(0.0001))  # seconds
print(finder.result_after(0.001))  # seconds
print(finder.result_after(0.01))  # seconds
