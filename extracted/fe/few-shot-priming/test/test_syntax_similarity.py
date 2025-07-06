import unittest
from experiments import *
from argument_sampling.syntax_similarity import *

class SyntaxSimilarityUnitTest(unittest.TestCase):
    def test_similarity_calculation(self):
        ibmsc_experiments = load_splits("ibmsc", oversample=False)
        ibmsc_experiments["training"] = ibmsc_experiments["training"].sample(10)
        ibmsc_experiments["validation"] = ibmsc_experiments["validation"].sample(12)
        sim = calc_syntactic_similarity(ibmsc_experiments["validation"], ibmsc_experiments["training"])
        self.assertEqual(len(sim),12)

