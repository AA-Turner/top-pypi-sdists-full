import unittest
from few_shot_priming.argument_sampling.stance_priming import *
class StancePrimingUnitTest(unittest.TestCase):
    def testPercentilesCalc(self):
        path_similarity = "/home/yamen/tmp/perspectrum-stance-similarties.json"
        thresholds = get_thresholds_for_percentiles(path_similarity, 10)
        print(thresholds)
