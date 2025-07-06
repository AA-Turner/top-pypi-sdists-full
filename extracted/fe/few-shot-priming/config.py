from datetime import datetime
import os
import yaml

from pathlib import Path


root_path = Path(__file__).parent

def get_absolute_path(path):
    return Path(root_path, path)

def adjust_config(config):
    for key in config:
        if isinstance(config[key],str):
            config[key] = config[key].replace("/bigwork/nhwpajjy","/mnt/home/yajjour")
        elif isinstance(config[key],dict):
            adjust_config(config[key])
        else:
            pass
def adjust_config_to_kisski():
    config = load_config()
    adjust_config(config)
    save_config(config)

def load_config():
    """
    Load the configuration of the experiment and the model
    :return: a dictionary containing the configuration of the experiments
    """

    conf_path = Path(root_path, "conf.yaml")
    with open(conf_path) as file:
        config = yaml.safe_load(file)
        return config

def save_config(config):
    conf_path = Path(root_path, "conf.yaml")
    with open(conf_path, "w") as file:
        yaml.dump(config, file)

def get_prompting_config():
    config = load_config()
    return config["prompt"]


def get_prompt_fine_tuning():
    """
    Load the prompting approach main configuration
    :return:
    """
    config = load_config()
    return config["prompt-fine-tuning"]

def get_prompt_fine_tuning_params(model):
    """
    Load the prompt params to optimize  the model
    :return: a dictionary containing the params for the few shot model
    """
    prompt_fine_tuning_config = get_prompt_fine_tuning()
    return prompt_fine_tuning_config[f"{model}-params"]

def get_prompt_fine_tuning_best_params(experiment, model):
    """
    Load the prompting approach best params
    :return:
    """
    prompting_config = get_prompt_fine_tuning()
    return prompting_config[f"{model}-best-params"][experiment]

def get_contrastive_embeddings_params(experiment):
    config = load_config()
    return config["stance-priming"]["best-params"][experiment]

def get_experiment_paths(experiment):
    conf = load_config()
    if experiment == "ibmsc":
        path_source = Path(root_path, conf["dataset"]["path-ibmsc-root"])
    elif experiment == "perspectrum":
        path_source = None
    else:
        path_source = None
    path_training = Path(root_path, conf["experiment"][experiment]["path-training"])
    path_test = Path(root_path, conf["experiment"][experiment]["path-test"])
    if experiment in ["ibmsc", "perspectrum", "vast", "snopes"]:
        path_validation = Path(root_path, conf["experiment"][experiment]["path-validation"])
    else:
        path_validation = None
    return path_source, path_training, path_validation, path_test


def get_baseline_params():
    config = load_config()
    return config["baseline"]["params"]

def get_baseline_config():
    config = load_config()
    config = config["baseline"]
    return config

def get_baseline_best_params(experiment):
    config = load_config()
    return config["baseline"]["best-params"][experiment]

def get_logs(experiment, run):
    config = load_config()
    home_directory = os.path.expanduser( '~' )
    now = datetime.now()
    time_now = now.strftime("%m-%d-%H:%M")
    path = config["experiment"][experiment]["path-logs"].replace("time", time_now).replace("run", run)
    return Path(home_directory, path)

def get_run_results_path(experiment=None, run=""):
    config = load_config()
    home_directory = os.path.expanduser( '~' )
    now = datetime.now()
    time_now = now.strftime("%m-%d-%H:%M")
    path = config["experiment"][experiment]["path-run-results"].replace("time", time_now)
    path = path.replace("run", run)
    return Path(home_directory, path)

def get_results_path(experiment=None, run=""):
    config = load_config()
    home_directory = os.path.expanduser( '~' )
    now = datetime.now()
    time_now = now.strftime("%m-%d-%H:%M")
    path_results = config["experiment"][experiment]["path-results"].replace("time", time_now)
    return Path(home_directory, path_results)

def get_openai_key():
    config = load_config()
    return config["openai"]["key"]

def load_topic_similarity_params():
    config = load_config()
    return config["topic-similarity"]["params"]

def get_topic_model_path(experiment, experiment_type):
    config = load_config()
    token = f"{experiment}-{experiment_type}"
    return config["topic-similarity"]["model-path"][token]

def get_similarities_path(experiment, experiment_type, model):

    config = load_config()
    token = f"{experiment}-{experiment_type}"
    return config["topic-similarity"][f"{model}-similarity-path"][token]

def dump_bow_size(experiment, experiment_type, bow_size):
    config = load_config()
    token = f"{experiment}-{experiment_type}"
    config["topic-similarity"]["bow"][token] = bow_size
    save_config(config)

def load_bow_size(experiment, experiment_type):
    config = load_config()
    token = f"{experiment}-{experiment_type}"
    return config["topic-similarity"]["bow"][token]

def get_template_path():
    conf = load_config()
    return Path(root_path, conf["prompt-fine-tuning"]["path-template"])

def get_diverse_example_path(experiment, experiment_type, topic_count=None, drop_duplicates=False):
    config = load_config()
    token = f"{experiment}-{experiment_type}"
    if drop_duplicates and experiment != "perspectrum":
        raise ValueError("duplicates are only considered for the perspectrum dataset")

    if topic_count:
        return config["topic-similarity"]["diverse-examples-topics"][token]
    elif drop_duplicates:
        return config["topic-similarity"]["diverse-examples"][f"{token}-no-duplicates"]
    else:
        return config["topic-similarity"]["diverse-examples"][token]

def get_similar_examples_path(experiment, experiment_type, topic_count=None):
    config = load_config()
    token = f"{experiment}-{experiment_type}"
    if topic_count:
         return  config["topic-similarity"]["similar-examples-topics"][token]
    else:
        return  config["topic-similarity"]["similar-examples-ks"][token]

def get_gpt2_params():
    return {
    "model-input-limit": 1024,
    "model-name": "gpt2",
    "model-path": "gpt2",
    "model-type": "gpt2"
    }

def get_seeds():
    conf = load_config()
    return conf["seeds"]

def get_ks(experiment):
    conf = load_config()
    return conf["experiment"][experiment]["ks"]

def get_few_shot_size(experiment):
    conf = load_config()
    return conf["experiment"][experiment]["few-shot-size"]

def get_analyze_k_results_pathes():
    conf = load_config()
    return conf["analyze-k"]

def get_analyze_topic_count_results_pathes():
    conf = load_config()
    return conf["analyze-topic-count"]

def get_analyze_topic_count_k():
    conf = load_config()
    return conf["analyze-topic-count"]["k"]

def get_topic_similarity_logs_path():
    conf = load_config()
    return conf["topic-similarity"] ["path-logs"]

def get_count_of_samples_per_cluster():
    conf = load_config()
    return conf["topic-similarity"]["count-of-samples-per-cluster"]


