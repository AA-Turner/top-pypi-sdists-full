import math
import random

import os
import json
import numpy as np
import pandas as pd

from scipy.spatial.distance import cosine
from collections import defaultdict

from tqdm import tqdm

# from prompting_stance import *
# from experiment import *
from few_shot_priming.argument_sampling.topic_similarity_sentence_transformer import *
from few_shot_priming.config import *
from few_shot_priming.utils import *
from few_shot_priming.experiments import *


os.environ["TOKENIZERS_PARALLELISM"] = "false"

def load_similarities(experiment, experiment_type, model="ctm"):
    path_similarities = get_similarities_path(experiment, experiment_type, model)
    with open(path_similarities, "r") as file:
        similarities= json.load(file)
    similarities_with_int_idices = {}
    for key in similarities:
        similarities_with_int_idices[int(key)]= {}
    for key in similarities:
        for train_key in similarities[key]:
            similarities_with_int_idices[int(key)][int(train_key)] = similarities[key][train_key]
    return similarities_with_int_idices


def save_similarities(experiment, experiment_type, similarities, model="ctm"):
    path_similarities = get_similarities_path(experiment, experiment_type, model)
    os.makedirs(os.path.dirname(path_similarities), exist_ok=True)

    with open(path_similarities, "w") as file:
        json.dump(similarities, file )
    print("succeed")

def evaluate_model(experiment, experiment_type, arguments_to_check, baseline=False):
    """
    :param model: contextual topic model to be evaluated

    """
    #similarities = load_similarities(experiment, experiment_type)
    if experiment_type =="validation":
        validate=True
    else:
        validate=False
    splits = load_splits(experiment, validate=validate, oversample=False)
    df_validation = splits[experiment_type]
    df_training = splits["training"]
    if baseline:
        sentence_transformer_similarities = load_similarities(experiment, experiment_type, model="sentence-transformer")
        #lda_similarities = calc_similarity_lda(df_validation, df_training)
    all_similar_examples = []
    arguments_to_check = df_validation.sample(arguments_to_check)
    for i, argument_record in arguments_to_check.iterrows():
        i = np.random.randint(0,len(df_validation))

        sentence_transformer_examples, sentence_transformer_score = sample_similar_examples(argument_record["id"], sentence_transformer_similarities, df_training, df_training.shape[0])
        sentence_transformer_examples.rename(columns={"text":"sentence-transformer-text", "topic":"sentence-transformer-topic"}, inplace=True)
        sentence_transformer_examples["sentence-transformer-score"] = sentence_transformer_score
        queries = [argument_record["text"] for _ in range(0,len(df_training))]
        queries_topic = [argument_record["topic"] for _ in range(0,len(df_training))]
        sentence_transformer_examples["query-text"] = queries
        sentence_transformer_examples["query-topic"] = queries_topic
        all_similar_examples.append(pd.concat([sentence_transformer_examples.reset_index()], axis=1))

    df_sorted_examples = pd.concat(all_similar_examples)
    df_sorted_examples.to_csv(f"~/contexutal_topic_model_{experiment}_{experiment_type}_evaluation.csv", sep="\t", columns=["query-text", "query-topic",
                                                                    #"ctm-text", "ctm-topic", "ctm-score",
                                                                    "sentence-transformer-text", "sentence-transformer-topic", "sentence-transformer-score"])




#memory = Memory("/tmp/similar-examples")
#@memory.cache
def sort_and_filter_hashmap(test_hashmap, df_training_indices):

    claims_with_similarity = sorted(test_hashmap.items(),key=lambda x: -x[1])
    items_indices = [claim_with_sim[0] for claim_with_sim in claims_with_similarity if claim_with_sim[0] in df_training_indices]
    return items_indices

def check_exists(instance, instances):
    for record in instances:
        if instance["arc_id"].values[0] == record["arc_id"].values[0]:
            return True
    return False


def sample_similar_examples(test_index, similarities, df_training, few_shot_size, experiment="ibmsc"):

    test_hashmap = similarities[test_index]
        #print(claims_with_similarity)
    df_training_indices = set(df_training["id"].values.tolist())

    items_indices = sort_and_filter_hashmap(test_hashmap, df_training_indices)

    df_pro_instances =  df_training[df_training["stance"]==1]
    df_con_instances =  df_training[df_training["stance"]==0]
    if experiment == "vast":
        df_neutral_instances = df_training[df_training["stance"]==2]
    if experiment == "ibmsc" or experiment == "perspectrum":
        class_few_shot_size = few_shot_size // 2
        pro_shot_size = class_few_shot_size
        con_shot_size = few_shot_size - pro_shot_size
    else:
        #con_shot_size, pro_shot_size, neutral_shot_size = decide_vast_shot_size(few_shot_size)
        con_shot_size, pro_shot_size, neutral_shot_size = few_shot_size/3, few_shot_size/3, few_shot_size/3
    if len(df_pro_instances)< pro_shot_size:
        df_pro_instances = df_pro_instances.sample(pro_shot_size, replace=True)
    if len(df_con_instances) < con_shot_size:
        df_con_instances = df_con_instances.sample(con_shot_size, replace=True)
    if experiment == "vast" and len(df_neutral_instances) < neutral_shot_size:
        df_neutral_instances = df_neutral_instances.sample(neutral_shot_size, replace=True)
    instances = []

    pro_instances_count = 0
    con_instances_count = 0
    neutral_instances_count = 0
    for index in items_indices:
        pro_instance = df_pro_instances[df_pro_instances["id"]==index]
        con_instance = df_con_instances[df_con_instances["id"]==index]
        if experiment == "vast":
            neutral_instances = df_neutral_instances[df_neutral_instances["id"]==index]
        if experiment == "vast" and len(neutral_instances) and neutral_instances_count < neutral_shot_size:
            if not check_exists(neutral_instances, instances):
                instances.append(neutral_instances)
                neutral_instances_count = neutral_instances_count + 1
        elif len(con_instance) and con_instances_count < con_shot_size:
            if (experiment =="ibmsc" or experiment == "perspectrum") or not check_exists(con_instance, instances):
                instances.append(con_instance)
                con_instances_count = con_instances_count +1
        elif len(pro_instance) and pro_instances_count<pro_shot_size:
            if (experiment =="ibmsc" or experiment == "perspectrum") or not check_exists(pro_instance, instances):
                instances.append(pro_instance)
                pro_instances_count = pro_instances_count + 1
        if (experiment =="ibmsc" or experiment == "perspectrum") and pro_instances_count + con_instances_count == few_shot_size:
            break
        if experiment == "vast" and pro_instances_count + con_instances_count + neutral_instances_count == few_shot_size:
            break
    df_few_shots = pd.concat(instances)
    df_few_shots["score"] = df_few_shots["id"].apply(lambda x: test_hashmap[x])
    df_few_shots.sort_values("topic", inplace=True)
    return df_few_shots, df_few_shots["score"]

def save_similar_examples_topic_counts(few_shot_size, experiment, save_text=False, debug=False):
    topic_counts = get_topic_count_range(experiment, False)

    similarities = load_similarities(experiment, "test", model="sentence-transformer")

    all_topic_count_instances = []
    for topic_count in tqdm(topic_counts):
        dataset = load_splits(experiment, validate= False, oversample=False,  topic_count= topic_count, debug=debug)
        for _, argument in tqdm(dataset["test"].iterrows()):
            test_id = argument["id"]
            similar_examples, scores = sample_similar_examples(test_id, similarities, dataset["training"], few_shot_size=few_shot_size, experiment=experiment)
            similar_examples["test-id"] = test_id
            similar_examples["topic-count"] = topic_count
            if save_text:
                similar_examples["test-text"] = argument["text"]
            all_topic_count_instances.append(similar_examples)
    path_examples_topic_counts = get_similar_examples_path(experiment, "test", topic_count=True)
    df_examples_topic_count = pd.concat(all_topic_count_instances)
    df_examples_topic_count.to_csv(path_examples_topic_counts, sep="\t", encoding="utf-8")

def save_similar_examples_ks( experiment, experiment_type, path_similar_examples, save_text=False, debug=False, drop_duplicate_perspectives=False):
    is_validate = experiment_type == "validation"
    similarities = load_similarities(experiment, experiment_type, model="sentence-transformer")
    print("loaded matrix")
    dataset = load_splits(experiment, oversample=False, validate=is_validate, debug=debug, drop_duplicate_perspectives=drop_duplicate_perspectives)
    print(f"loaded dataset with size {len(dataset)}")
    all_k_similar_instances = []
    for k in tqdm(get_ks(experiment)):
        for _, argument in tqdm(dataset[experiment_type].iterrows()):
            test_id = argument["id"]
            similar_examples, scores = sample_similar_examples(test_id, similarities, dataset["training"], few_shot_size=k, experiment=experiment)
            similar_examples["test-id"] = test_id
            similar_examples["k"] = k
            if save_text:
                similar_examples["test-text"] = argument["text"]
            all_k_similar_instances.append(similar_examples)

    df_examples_ks = pd.concat(all_k_similar_instances)
    df_examples_ks.to_csv(path_similar_examples, sep="\t", encoding="utf-8")


def load_similar_examples(experiment, experiment_type, path_similar_examples=None, topic_count=None, few_shot_size=16):
    if not path_similar_examples:
        path_similar_examples = get_similar_examples_path(experiment, experiment_type, topic_count=topic_count)
    df_examples = pd.read_csv(path_similar_examples, sep="\t")


    if topic_count:
        df_examples = df_examples[df_examples["topic-count"]==topic_count]
    elif few_shot_size:
        df_examples = df_examples[df_examples["k"]==few_shot_size]
    return df_examples



def get_similar_examples(test_index, df_examples):
    return df_examples[df_examples["test-id"]==test_index]