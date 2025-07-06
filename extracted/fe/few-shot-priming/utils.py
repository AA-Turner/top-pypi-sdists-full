
import os
import os
import random

import pandas as pd


from few_shot_priming.config import *
from transformers import set_seed


def init_reproducible(seed):
    set_seed(seed)

def get_model_instruction_fine_tuninig_from(args):
    if args.alpaca_7b:
        return "alpaca-7b"
    elif args.mistral_7b_instruct:
        return "mistral-7b-instruct"
    elif args.vicuna_7b:
        return "vicuna-7b"

def get_model_prompting_from(args):
    if args.llama2_7b:
        return "llama2-7b"
    elif args.opt_30b:
        return "opt-30b"
    elif args.gpt2:
        return "gpt2"
    elif args.alpaca_7b:
        return "alpaca-7b"
    elif args.mistral_7b_instruct:
        return "mistral-7b-instruct"
    elif args.vicuna_7b:
        return "vicuna-7b"
    elif args.gemma_7b_instruct:
        return "gemma-7b-instruct"

def get_experiment_from(args):

    if args.vast:
        experiment = "vast"
    elif args.perspectrum:
        experiment = "perspectrum"
    elif args.ibmsc:
        experiment = "ibmsc"

    return experiment

def get_sampling_strategy_from(args):
    if args.similar_examples:
        sampling_strategy = "similar"
    elif args.diverse_examples:
        sampling_strategy = "diverse-examples"
    else:
        sampling_strategy = None
    return sampling_strategy

def get_similarity_from(args):
    if args.parse_tree_kernel:
        similarity = "parse-tree-kernel"
    elif args.ctm:
        similarity = "ctm"
    elif args.sentence_transformer:
        similarity = "sentence-transformer"
    else:
        similarity = None
    return similarity

def get_experiment_type_from(args):
    if args.validate:
        experiment_type = "validation"
    else:
        experiment_type= "test"
    return experiment_type

def get_sampling_strateg_property_from(args):
    if args.path_similar_examples:
        return args.path_similar_examples.split("/")[-1].replace(".csv","").replace(".tsv","")

def get_model_name(config):
    model_name = config["model-name"]
    return model_name

def get_run_name(args, config, prompting_type):

    experiment = get_experiment_from(args)
    experiment_type = get_experiment_type_from(args)
    sampling_strategy = get_sampling_strategy_from(args)
    sampling_strategy_property = get_sampling_strateg_property_from(args)
    model_name = get_model_name(config)
    if "/" in model_name:
        model_name = model_name.split("/")[-1]
    if prompting_type =="prompt-fine-tuning" and args.no_fine_tuning:
            model_name = model_name + "no-fine-tuning"
    if prompting_type == "prompt" and args.openai:
        model_name = "openai"
    few_shot_size = get_few_shot_size(experiment)
    if prompting_type =="prompt-fine-tuning" and args.optimize:
        run = f"optimize-hyperparameters-few-shot-k-{few_shot_size}"
    elif args.analyze_k:
        run = "analyze-k"
    elif args.analyze_prime_similarity:
        run =f"analyze-prime-similarity-{few_shot_size}"
    elif args.analyze_topic_similarity:
        run =f"analyze-topic-similarity-{few_shot_size}"
    elif args.analyze_topic_count:
        run =f"analyze-topic-count-k-{few_shot_size}"
    elif prompting_type =="prompt-fine-tuning" and args.all_training_data:
        run = f"all-training-data"
    else:
        run = f"k-{few_shot_size}"

    if sampling_strategy:
        if sampling_strategy_property:
            if run:
                results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}-{run}-{sampling_strategy_property}"
            else:
                results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}-{sampling_strategy_property}"
        elif run:
            results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}-{run}-{sampling_strategy}"
        else:
            results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}-{sampling_strategy}"


    else:
        if run:
            results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}-{run}-random-examples"
        else:
            results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}-random-examples"
    return results_name




def average_seeds(df_results):
    #metric_columns = [column for column in df_results.columns if column.startswith("validation") or column.startswith("test")]
    if "seed" in df_results.columns:
        if "k" in df_results.columns:
            df_average = df_results.groupby("k").mean().reset_index()
            df_average["seed"]= "average"
            df_results = pd.concat([df_results, df_average])
        elif "topic-count" in df_results.columns:
            df_average = df_results.groupby("topic-count").mean().reset_index()
            df_average["seed"]= "average"
            df_results = pd.concat([df_results, df_average])
        elif "max-similarity" in df_results.columns:
            df_average = df_results.groupby("max-similarity").mean().reset_index()
            df_average["seed"]= "average"
            df_results = pd.concat([df_results, df_average])
        else:
            df_average = df_results.mean()
            df_average["seed"]="average"
            df_results.loc["average"]=df_average



    return df_results

def get_max_topic_count(experiment, is_validate):
    """
    get the maximum count of unique topics in a dataset
    :param experiment:
    :param is_validate:
    :return:
    """
    path_source, path_training, path_validation, path_test = get_experiment_paths(experiment)
    df_training = pd.read_csv(path_training, sep=",")
    df_validation = pd.read_csv(path_validation, sep=",")
    if not is_validate:
        df_training = pd.concat([df_training, df_validation])
    if experiment == "ibmsc":
        topic_label = "topicText"
    else:
        topic_label = "topic_str"
    return df_training[topic_label].nunique()

def get_topic_count_range(experiment, is_validate):
    max_topic_count = get_max_topic_count(experiment, is_validate)
    if experiment == "ibmsc":
        topic_counts = list(range(1, max_topic_count+1, 5))
        topic_counts.append(max_topic_count)
    else:
        if is_validate:
            topic_counts = [5, 50, 100, 200, 300,  max_topic_count]
        else:
            topic_counts = [5, 1000, 2000, 3000, 4000, max_topic_count]
    return topic_counts

def decide_vast_shot_size(few_shot_size):
    if few_shot_size == 2:
        class_few_shot_size = 0
    else:
        class_few_shot_size = few_shot_size // 3
    random_value = random.randint(0,2)
    neutral_shot_size = class_few_shot_size
    pro_shot_size = class_few_shot_size
    con_shot_size = class_few_shot_size


    if few_shot_size % 3 == 2:
        if random_value == 0:
            pro_shot_size = pro_shot_size + 1
            neutral_shot_size = neutral_shot_size+ 1

        elif random_value == 1:
            con_shot_size = con_shot_size + 1
            neutral_shot_size = neutral_shot_size+ 1
        else:
            pro_shot_size = pro_shot_size+ 1
            con_shot_size = con_shot_size+ 1

    else:

        if random_value == 0:
            con_shot_size = con_shot_size + 1
        elif random_value == 1:
            pro_shot_size = pro_shot_size + 1
        else:
            neutral_shot_size = neutral_shot_size + 1

    assert (con_shot_size+pro_shot_size + neutral_shot_size == few_shot_size)

    return con_shot_size, pro_shot_size, neutral_shot_size