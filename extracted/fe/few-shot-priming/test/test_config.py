import unittest
from config import *
class TestConfig(unittest.TestCase):
    def test_config(self):
        best_params = get_prompt_fine_tuning_best_params()
        self.assertEqual(best_params["batch-size"], 16)

        params = get_prompt_fine_tuning_params()
        self.assertEqual(params["batch-size"], [1])

        path_source, path_trianing, path_valiation, path_test = get_experiment_paths("vast")
        self.assertEqual(path_source, None)


    def test_parameters(self):
        params = load_topic_similarity_params()
        self.assertEqual(params["contextual_size"], 768)
        self.assertEqual(params["n_components"], 15)
        self.assertEqual(params["num_epochs"], 20)

    def test_get_similarities_path(self):
        experiment = "ibmsc"
        experiment_type = "validation"
        path = get_similarities_path(experiment, experiment_type)
        self.assertEqual(path, "/bigwork/nhwpajjy/pre-trained-models/topic-models/similarities-ibmsc-validation-ctm.bin")

    def test_dump_bow_size(self):
        dump_bow_size("ibmsc", "validation", 10)
        bow_size = load_bow_size("ibmsc", "validation")
        self.assertEqual(bow_size, 10)