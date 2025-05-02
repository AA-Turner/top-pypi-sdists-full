import unittest
import os.path
from config import *
from experiments import *
from argument_sampling.topic_similarity import *
from argument_sampling.topic_similarity_sentence_transformer import *
class TestTopicSimilarity(unittest.TestCase):
    def test_model_creation(self):

        splits = load_splits("ibmsc")
        df_training = splits["training"].sample(100)
        df_sample = df_training.sample(100)
        print(df_sample.columns)
        params = load_topic_similarity_params()
        topic_model, bow = create_topic_model(df_sample, params)
        self.assertTrue(params)
        return topic_model, bow
    def test_save_model(self):
        topic_model, bow = self.test_model_creation()
        self.assertTrue(bow)
        topic_model_path = get_topic_model_path("ibmsc", "validation")
        dump_model(topic_model, topic_model_path)
        self.assertTrue(os.path.exists(topic_model_path))

    def test_load_model(self):
        bow_size = load_bow_size("ibmsc", "validation")
        topic_model_path = get_topic_model_path("ibmsc", "validation")
        params = load_topic_similarity_params()
        model = load_topic_model(topic_model_params=params, bow_size=bow_size, topic_model_path=topic_model_path)
        self.assertTrue(model)

    def test_evaluate_model(self):
        evaluate_model("ibmsc", 3, True)

    def test_similarities(self):
        #set_seed(45)
        splits = load_splits("ibmsc")
        df_training = splits["training"]
        df_test = splits["test"]
        params = load_topic_similarity_params()
        model, bow = create_topic_model(df_test, params)
        similarities = calc_all_similarity(df_test=df_test, df_train=df_training, model=model)
        #self.assertTrue(similarities.shape[0], 100)
        #self.assertTrue(similarities.shape[1], 100)
        for i in range(similarities.shape[0]):
            _i = np.argmin(similarities[i ,:])
            print(i)
            print(_i)
            print(df_test["text"].iloc[i])
            print(df_training["text"].iloc[_i])
            #self.assertEqual(np.argmin(similarities[i, :]), i)


    def test_similarities_save(self):
        splits = load_splits("ibmsc")
        df_training = splits["training"]
        params = load_topic_similarity_params()
        model, bow = create_topic_model(df_training, params)
        similarities = calc_all_similarity(df_test=splits["validation"], df_train=df_training, model=model)
        save_similarities(experiment="ibmsc", experiment_type="validation", similarities=similarities, model="ctm")
        loaded_similarities = load_similarities(experiment="ibmsc", experiment_type="validation",)
        self.assertEqual(len(similarities), len(loaded_similarities))

        for test_index in similarities:
            for train_index in similarities[test_index]:
                self.assertEqual(similarities[test_index][train_index], loaded_similarities[test_index][train_index])

    def test_sample_similar(self):
        splits = load_splits("ibmsc")
        df_training = splits["training"]
        df_test = splits["validation"]
        params = load_topic_similarity_params()
        # model, bow = create_topic_model(df_training, params)
        # similarities = calc_all_similarity(df_test=df_training, df_train=df_training, model=model)
        similarities = load_similarities("ibmsc", "validation")
        for i in df_test["id"].values.tolist():
            examples, scores = sample_similar_examples(i, similarities, df_training, 10)
            print(df_test[df_test["id"]==i])
            print(examples["text"])


    def test_lda_similarities(self):
        splits = load_splits("ibmsc")
        similarities = calc_similarity_lda(splits["validation"], splits["training"])
        self.assertEqual(similarities.shape[0], len(splits["validation"]))
        self.assertEqual(similarities.shape[1], len(splits["training"]))