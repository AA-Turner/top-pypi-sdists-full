import unittest
from argument_sampling.topic_similarity import *
from collections import Counter

class testSampleFiles(unittest.TestCase):
    def test_sample_files_mostl_similar_different_topics_perspectrum(self):
        df_similar_examples_different_topics = load_similar_examples("perspectrum", "test", "/bigwork/nhwpajjy/contrastive_learning/sampling_strategies_optimized/perspectrum-most-similar-different-topics-unbalanced-contrastive.tsv")
        for test_id, df in df_similar_examples_different_topics.groupby("test-id"):
            print(df)
            self.assertEqual(df["k"].sort_values().unique().tolist(), [2, 4, 8, 16, 32, 64])
        #stance_counts = df_similar_examples_different_topics.groupby("test-id").agg({"stance":Counter})
        #expected_stance_counts = {1: 8 , 0:8}
        #for stance in stance_counts.stance:
        #    self.assertEqual(stance, expected_stance_counts)
        topic_counts = df_similar_examples_different_topics.groupby("test-id").agg({"topic":lambda l: len(set(l))})

        for topic_count in topic_counts.topic:
            self.assertGreater(topic_count, 7)


        retrieved_counts = df_similar_examples_different_topics.groupby("test-id").agg({"id":lambda l: len(set(l))})
        for retrieved_count in retrieved_counts.id:

            self.assertEqual(retrieved_count, 16)
        self.assertEqual(len(df_similar_examples_different_topics["test-id"].unique()), 2773)


    def test_sample_files_most_similar_different_topics_vast(self):
        df_similar_examples_different_topics = load_similar_examples("vast", "test", "/bigwork/nhwpajjy/few-shot-priming/sampling-strategies/vast-most-similar-different-topics.tsv", few_shot_size=24)
        #k = [2, 4, 8, 16, 32, 64]
        #self.assertEqual(df_similar_examples_different_topics["k"].unique().tolist(), k)
        stance_counts = df_similar_examples_different_topics.groupby("test-id").agg({"stance":Counter})
        expected_stance_counts = {1: 8 , 0:8, 2:8}
        for stance in stance_counts.stance:
            self.assertEqual(stance, expected_stance_counts)
        topic_counts = df_similar_examples_different_topics.groupby("test-id").agg({"topic":lambda l: len(set(l))})

        for topic_count in topic_counts.topic:
            self.assertGreater(topic_count, 7)



        retrieved_counts = df_similar_examples_different_topics.groupby("test-id").agg({"id":lambda l: len(set(l))})
        for retrieved_count in retrieved_counts.id:

            self.assertEqual(retrieved_count, 24)

        self.assertEqual(len(df_similar_examples_different_topics["test-id"].unique()), 1460)

    def test_sample_files_most_similar_different_topics(self):
        df_similar_examples_different_topics = load_similar_examples("ibmsc", "test", "/bigwork/nhwpajjy/few-shot-priming/sampling-strategies/ibmsc-most-similar-different-topics.tsv")
    #k = [2, 4, 8, 16, 32, 64]
    #self.assertEqual(df_similar_examples_different_topics["k"].unique().tolist(), k)
        stance_counts = df_similar_examples_different_topics.groupby("test-id").agg({"stance":Counter})
        expected_stance_counts = {1: 8 , 0:8}
        for stance in stance_counts.stance:
            self.assertEqual(stance, expected_stance_counts)
        topic_counts = df_similar_examples_different_topics.groupby("test-id").agg({"topic":lambda l: len(set(l))})

        for topic_count in topic_counts.topic:
            self.assertGreater(topic_count, 7)



        retrieved_counts = df_similar_examples_different_topics.groupby("test-id").agg({"id":lambda l: len(set(l))})
        for retrieved_count in retrieved_counts.id:

            self.assertEqual(retrieved_count, 16)

        self.assertEqual(len(df_similar_examples_different_topics["test-id"].unique()), 1355)



    def test_sample_files_most_similar_different_topics__majority_stance_perspectrum(self):
        df_similar_examples_different_topics_majority_stance = load_similar_examples("perspectrum", "test", "/bigwork/nhwpajjy/few-shot-priming/sampling-strategies/perspectrum-most-similar-majority-stance-different-topic.tsv")
    #k = [2, 4, 8, 16, 32, 64]
    #self.assertEqual(df_similar_examples_different_topics["k"].unique().tolist(), k)
        df_similar_examples_different_topics_majority_stance["topic-stance"] = df_similar_examples_different_topics_majority_stance.apply(lambda x: str(hash(x["topic"])) + str(x["stance"]), axis=1)
        retrieved_counts = df_similar_examples_different_topics_majority_stance.groupby("test-id").agg({"id":lambda l: len(set(l))})
        for retrieved_count in retrieved_counts.id:
    
            self.assertEqual(retrieved_count, 16)
        #self.assertEqual(len(df_similar_examples_different_topics_majority_stance["test-id"].unique()), 2773)

        stance_counts = df_similar_examples_different_topics_majority_stance.groupby("test-id").agg({"stance":Counter})
        expected_stance_counts = {1: 8 , 0:8}
        for stance in stance_counts.stance:
            if stance != expected_stance_counts:
                print(stance)
            #self.assertEqual(stance, expected_stance_counts)
        topic_counts = df_similar_examples_different_topics_majority_stance.groupby("test-id").agg({"topic":lambda l: len(set(l))})

        for topic_count in topic_counts.topic:
            self.assertGreater(topic_count, 7)
        topic_stance_counts = df_similar_examples_different_topics_majority_stance.groupby("test-id").agg({"topic-stance": lambda l: len(set(l))})
        print(topic_stance_counts)
        for topic_count in topic_stance_counts:
            self.assertEqual(topic_count, 1)
