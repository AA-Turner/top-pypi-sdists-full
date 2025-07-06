import unittest
from experiments import *
from argument_sampling.diversify import *
class testCluster(unittest.TestCase):
    def test_get_vectors(self):
        dataset = load_splits("ibmsc", "validation")
        df_training = dataset["training"].sample(10)
        embeddings, ids, topics = get_embeddings(df_training)
        self.assertTrue(len(embeddings), 10)
        self.assertTrue(type(embeddings),np.ndarray)
        self.assertTrue(embeddings.shape, (10,768))
        return embeddings, ids, topics

    def test_save(self):
        embeddings, ids, topics = self.test_get_vectors()
        save_embeddings(embeddings, ids, topics, "/home/yamen/tmp")
        self.assertTrue(os.path.exists("/home/yamen/tmp/embeddings.txt"))
        self.assertTrue(os.path.exists("/home/yamen/tmp/topics.txt"))


    def test_load(self):
        embeddings, ids, topics = self.test_get_vectors()
        save_embeddings(embeddings, ids, topics, "/home/yamen/tmp")
        loaded_embeddings, loaded_ids, loaded_topics = load_embeddings("/home/yamen/tmp")
        self.assertTrue((loaded_embeddings==embeddings).any())
        self.assertTrue((ids == loaded_ids).any())
        self.assertEqual(topics, loaded_topics)

    def test_cluster(self):
        dataset = load_splits(experiment="ibmsc")
        embeddings, ids, topics = get_embeddings(dataset["training"])
        labels, centriods = cluster(embeddings, ids,10, n_clusters=16)
        self.assertEqual(len(centriods), 160)

    def test_sample_diversify(self):

        save_diverse_examples("ibmsc", "test")
        df_shots = sample_diverse_examples("ibmsc", "test", 16)
        self.assertGreater(df_shots["topic"].nunique(),14)