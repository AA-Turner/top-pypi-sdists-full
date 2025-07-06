from unittest import TestCase
from few_shot_priming.baseline import *

class TestBaseline(TestCase):
    def test_random_baseline(self):
        config = get_baseline_config()
        accu, pro_f1, con_f1, mac_f1 = baseline(config, offline=True, validate=True)
        print(accu)
        self.assertTrue(True)