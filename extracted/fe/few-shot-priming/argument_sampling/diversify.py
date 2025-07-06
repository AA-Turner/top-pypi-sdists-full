import json
import logging
import math
import sys
import numpy as np

import pandas as pd
from sentence_transformers import *
from sklearn.neighbors import NearestCentroid
from sklearn.cluster import AgglomerativeClustering
from few_shot_priming.config import *
from few_shot_priming.experiments import *
from few_shot_priming.mylogging import *

from few_shot_priming.utils import *


def get_embeddings(df_training):
    model = SentenceTransformer('all-mpnet-base-v2')
    df_training["topic-text"] = df_training.apply(lambda record: record["topic"] + "[SEP]" + record["text"], axis=1)

    training_text = df_training["topic-text"]
    topics = df_training["topic"].values.tolist()
    training_embeddings = model.encode(training_text.values.tolist())
    ids = df_training["id"].values.tolist()
    return training_embeddings, ids, topics

def save_embeddings(embeddings, ids, topics, path):
    ids = np.reshape(ids, (len(ids),1))
    vectors_with_ids = np.hstack((ids, embeddings))
    np.savetxt(path+"/embeddings.txt",vectors_with_ids, delimiter=",")
    with open(path+"/topics.json", "w") as file:
        json.dump(topics, file)



def load_embeddings(path):
    vectors = np.genfromtxt(path+"/embeddings.txt", delimiter=",")
    with open(path+"/topics.json", "r") as file:
        topics = json.load(file)
    return vectors[:,1:], np.uint32(vectors[:,0]), topics

def cluster(vectors, ids, count_of_samples_per_cluster, **args):
    clustering = AgglomerativeClustering(**args).fit(vectors)
    labels = clustering.labels_

    clf = NearestCentroid()
    clf.fit(vectors, labels)
    samples = []
    for centriod in clf.centroids_:
        distances = []
        label = clf.predict([centriod])
        cluster_instances = [l==label[0] for l in labels]

        for i, vector in enumerate(vectors):
            if cluster_instances[i]:
                distances.append((i, np.linalg.norm(centriod-vector)))
        distances = sorted(distances, key= lambda element_id: element_id[1])
        if count_of_samples_per_cluster > len(distances):
            count_of_samples_per_cluster = len(distances)
        sampled_indices = [element_id[0] for element_id in distances[:count_of_samples_per_cluster]]
        samples.extend([(ids[sampled_index], labels[sampled_index]) for sampled_index in sampled_indices])

    return labels, samples


def find_diverse_examples(experiment, experiment_type, k, count_of_samples_per_cluster, drop_duplicate_perspectives, topic_count=None, logger=None):
    if experiment_type=="validation":
        validate=True
    else:
        validate=False

    log_message(logger, f"clustering on {experiment} {experiment_type} {k} few shots", logging.INFO)
    dataset = load_splits(experiment, oversample=False, validate=validate, drop_duplicate_perspectives=drop_duplicate_perspectives, topic_count=topic_count)
    df_training = dataset["training"]
    embeddings, ids, topics = get_embeddings(df_training)
    if k > len(df_training):
        k = len(df_training)

    labels, centroid_samples = cluster(embeddings, ids, count_of_samples_per_cluster, n_clusters=k)
    log_message(logger, f"found {len(set(labels))} clusters", logging.INFO)
    centroid_ids = [centroid_sample[0] for centroid_sample in centroid_samples]
    df_diverse= df_training[df_training["id"].isin(centroid_ids)]
    mapping =dict(centroid_samples)
    df_diverse["cluster"] = df_diverse["id"].apply(lambda x: mapping[x])
    return df_diverse


def save_diverse_examples(experiment, experiment_type, ks, count_of_samples_per_cluster,  drop_duplicate_perspectives=False, topic_counts = None, logger=None):
    if topic_counts:
        path = get_diverse_example_path(experiment, experiment_type, topic_counts)

    else:
        path = get_diverse_example_path(experiment, experiment_type, )

    if drop_duplicate_perspectives:
        path = path.replace(".tsv", "no-duplicate.tsv")
    log_message(logger, f"saving to path {path}")
    all_diverse_samples = []
    if topic_counts:
        log_message(logger, f"performing clustering on {list(topic_counts)}")
        assert (len(ks)==1)
        k = ks[0]

        for topic_count in topic_counts:
            log_message(logger, f"performing clustering on  {topic_count}", logging.INFO)
            df_diverse = find_diverse_examples(experiment, experiment_type, k,count_of_samples_per_cluster,drop_duplicate_perspectives, topic_count, logger=logger)
            df_diverse["k"] = k
            df_diverse["topic-count"] = topic_count
            all_diverse_samples.append(df_diverse)
    else:
        for k in ks:
            df_diverse = find_diverse_examples(experiment, experiment_type, k, count_of_samples_per_cluster, drop_duplicate_perspectives, topic_count=None, logger=logger)
            df_diverse["k"]=k
            all_diverse_samples.append(df_diverse)

    df_all_diverse_examples = pd.concat(all_diverse_samples)

    df_all_diverse_examples.to_csv(path, sep="\t")

def sample_diverse_examples(experiment, experiment_type, k, logger, topic_count=None, drop_duplicate_perspectives=False):
    path = get_diverse_example_path(experiment, experiment_type, topic_count, drop_duplicate_perspectives)
    df_diverse_examples = pd.read_csv(path, sep="\t")

    if topic_count:
        df_diverse_examples = df_diverse_examples[df_diverse_examples["topic-count"] == topic_count]

    if experiment == "ibmsc" or experiment =="perspectrum":
        label_ratio = {"validation": 0.5, "test": 0.5}


    log_message(logger,f"sampling pro, con, neutral arguments for {k} few shots", level= logging.INFO)
    if experiment == "ibmsc" or experiment =="perspectrum":
        pro_count = math.floor(k * label_ratio[experiment_type])
        con_count = k - pro_count
    else:

        #con_count, pro_count, neutral_count = decide_vast_shot_size(k)
        con_count, pro_count, neutral_count = k/3, k/3, k/3

    df_diverse_examples = df_diverse_examples[df_diverse_examples["k"] == k]
    instances = []
    for cluster, df_cluster in df_diverse_examples.groupby("cluster"):
        con_arguments = df_cluster[df_cluster["stance"] == 0]
        pro_arguments = df_cluster[df_cluster["stance"] == 1]
        if experiment == "vast":
            neutral_arguments = df_cluster[df_cluster["stance"] == 2]
        if experiment == "vast" and len(neutral_arguments) and neutral_count:
            instance = neutral_arguments.sample(1)
            neutral_count = neutral_count - 1
        elif len(con_arguments) and con_count:
            instance = con_arguments.sample(1)
            con_count = con_count - 1
        elif len(pro_arguments):
            instance = pro_arguments.sample(1)
            pro_count = pro_count - 1
        elif len(con_arguments):
            instance = con_arguments.sample(1)
            con_count = con_count - 1
        elif experiment == "vast" and len(neutral_arguments):
            instance = neutral_arguments.sample(1)
            neutral_count = neutral_count - 1
        else:
            break

        instance["cluster"] = cluster
        instances.append(instance)
    df_examples = pd.concat(instances)
    log_message(logger,f"found that count of pro arguments {len(df_examples[df_examples['stance'] == 1])}", level= logging.INFO)
    log_message(logger,f"found that count of con arguments {len(df_examples[df_examples['stance'] == 0])}", level= logging.INFO)
    log_message(logger,f"found that count of neutral arguments {len(df_examples[df_examples['stance'] == 2])}", level= logging.INFO)
    #df_examples = df_diverse_examples.groupby("cluster").sample(1)
    df_examples.sort_values("topic", inplace=True)
    return df_examples
