import unittest
from experiments import *
class TestLoad(unittest.TestCase):
    def test_load(self):
        dataset = load_splits("vast")

        training_df = dataset["training"]



        #self.assertEqual(13477, dataset["training"].shape[0])


    def test_load_topic_count(self):
        topic_count_5_dataset = load_splits("vast", topic_count=5, validate=False)
        self.assertEqual(topic_count_5_dataset["training"]["topic"].nunique(), 5)
        topic_count_1000_dataset = load_splits("vast", topic_count=1000, validate=False)
        self.assertEqual(topic_count_1000_dataset["training"]["topic"].nunique(), 1000)
