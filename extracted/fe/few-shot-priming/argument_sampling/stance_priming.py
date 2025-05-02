import pandas as pd
import json
from collections import Counter

from few_shot_priming.argument_sampling.topic_similarity import load_similar_examples, get_similar_examples
from sklearn.metrics import f1_score, accuracy_score
from tqdm import tqdm
from few_shot_priming.config import *
from few_shot_priming.experiments import load_splits
from sentence_transformers import SentenceTransformer, losses, SentencesDataset, datasets, util
from sentence_transformers.evaluation import BinaryClassificationEvaluator
from sentence_transformers.readers import InputExample
from collections import *
from scipy.spatial.distance import cosine

def preprocess_dataset(dataset):
    for split in dataset:
        dataset[split]["topic-text"] = dataset[split].apply(lambda record: record["topic"] + "[SEP]" + record["text"], axis=1)

def generate_test_dataset(df, three_classes=False):
    list1 = []
    list2 = []
    labels = []
    for topic, df_topic in df.groupby("topic"):
        df_stances = list(df_topic.groupby("stance"))
        if len(df_stances)<2 or (three_classes and len(df_stances)<3)   :
            continue
        df_stance_1 = df_stances[0][1]
        df_stance_2 = df_stances[1][1]
        if not len(df_stance_1) or not len(df_stance_2):
            continue

        if three_classes:
            df_stance_3 = df_stances[2][1]
            if not len(df_stance_3) and not len(df_stance_2):
                continue

        for i, argument in df_topic.iterrows():
            for j, argument_2 in df_topic.iterrows():
                if j>i:
                    list1.append(argument["topic-text"])
                    list2.append(argument_2["topic-text"])
                    if argument["stance"] == argument_2["stance"]:
                        label = 1
                    else:
                        label = 0
                    labels.append(label)

    return list1, list2, labels

def train(model, params, train_dataloader, evaluator=None, output_model_path=None):


    learning_rate = params["lr"]
    epochs = params["epochs"]
    train_loss = losses.ContrastiveLoss(model=model)
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        optimizer_params = {'lr' : learning_rate},
        output_path=output_model_path,
        epochs=epochs,
        evaluator=evaluator,
        save_best_model=True,
        evaluation_steps=1000
    )
    return model

def create_evaluator(df_test, three_examples=False):
    list1, list2, labels = generate_test_dataset(df_test, three_examples)
    evaluator = BinaryClassificationEvaluator(list1, list2, labels,show_progress_bar=True)
    return evaluator


def generate_training_examples(df_training, three_classes=False):
    contrastive_examples = []
    guid = 0
    for topic, df_topic in df_training.groupby("topic"):
        df_stances = list(df_topic.groupby("stance"))
        if len(df_stances)<2 or (three_classes and len(df_stances)<3):
            continue
        df_stance_1 = df_stances[0][1]
        df_stance_2 = df_stances[1][1]

        if not len(df_stance_1) or not len(df_stance_2):
            continue
        if three_classes:
            df_stance_3 = df_stances[2][1]
            if not len(df_stance_3) or not len(df_stance_2):
                continue
        for i, argument in df_topic.iterrows():
            for j, argument_2 in df_topic.iterrows():
                if j>i:
                    pair = [argument["topic-text"], argument_2["topic-text"]]
                    if argument["stance"] == argument_2["stance"]:
                        label = 1
                    else:
                        label = 0
                    guid = guid + 1
            contrastive_examples.append(InputExample(texts=pair, label=label, guid=guid))

    return contrastive_examples

def load_similarities(path_similarities):

    with open(path_similarities, "r") as file:
        similarities= json.load(file)
    similarities_with_int_idices = {}
    for key in similarities:
        similarities_with_int_idices[int(key)]= {}
    for key in similarities:
        for train_key in similarities[key]:
            similarities_with_int_idices[int(key)][int(train_key)] = similarities[key][train_key]
    return similarities_with_int_idices

def generate_similarity_matrix(experiment, path_model, path_similarities, debug=False):

    model = SentenceTransformer(path_model)
    dataset =  load_splits(experiment, oversample=False, validate=False )
    preprocess_dataset(dataset)
    test_text = dataset["test"]["topic-text"]
    training_text = dataset["training"]["topic-text"]
    test_embeddings = model.encode(test_text.values.tolist())
    training_embeddings = model.encode(training_text.values.tolist())
    cosine_scores = util.cos_sim(test_embeddings, training_embeddings)
    similarities = defaultdict(dict)
    i,j = 0, 0
    for _,test_record in tqdm(dataset["test"].iterrows()):
        for _,train_record in dataset["training"].iterrows():
            similarities[test_record["id"]][train_record["id"]] = float(cosine_scores[i,j])
            j = j + 1
        i = i + 1
        j = 0
    with open(path_similarities, "w") as file:
        json.dump(similarities, file )


def generate_most_similar_stance_arguments(experiment, path_similarities, path_samples, different_topics, debug, max_threshold=None, drop_duplicate_perspectives=False):

    similarities = load_similarities(path_similarities)
    dataset =  load_splits(experiment, oversample=False, validate=False, drop_duplicate_perspectives=drop_duplicate_perspectives, debug=debug)
    df_training = dataset["training"]

    all_samples = []
    if experiment == "vast":
        ks = [3, 6, 12, 24, 48, 96]
    else:
        ks = [2, 4, 8, 16, 32, 64]

    if different_topics:
        for _, test_record in tqdm(dataset["test"].iterrows()):
            instances_scores_map = similarities[test_record["id"]]
            elements_to_drop = []
            if  max_threshold:
                for key in instances_scores_map:
                    if instances_scores_map[key] >max_threshold:
                        elements_to_drop.append(key)
                for key in elements_to_drop:
                    del instances_scores_map[key]

            df_training_subset = df_training[df_training["id"].isin(instances_scores_map.keys())]
            df_training_subset["score"] = df_training_subset["id"].apply(lambda id: instances_scores_map[id])
            training_instances = list(df_training_subset.itertuples(index=False))
            training_instances.sort(key=lambda x: x.score, reverse=True)

            for k in ks:
                topic_set = set()
                id_set = set()
                samples = []
                exists_enough_topics = True
                if len(training_instances) < k:
                    k = len(training_instances)
                #if len(training_instances) == 0:
                    #raise ValueError
                while len(id_set) < k:


                    for training_record in training_instances:
                        if exists_enough_topics and training_record.topic not in topic_set and training_record.id not in id_set:
                            id_set.add(training_record.id)
                            topic_set.add(training_record.topic)
                        elif not exists_enough_topics and training_record.id not in id_set:
                            id_set.add(training_record.id)
                            topic_set.add(training_record.topic)
                        if len(id_set) == k:
                            samples = []
                            for instance in training_instances:
                                if instance.id in id_set:
                                    samples.append(instance)
#                                    exists = False
#                                    for sample in samples:
#                                        if instance.id == sample.id:
#                                            exists=True
#                                            break
#                                    if not exists:

                            break
                    if len(id_set) < k:
                        exists_enough_topics = False

                df_samples = pd.DataFrame(samples)
                df_samples["k"] = k
                df_samples["test-id"] = test_record["id"]
                all_samples.append(df_samples)

    else:
        for _, test_record in dataset["test"].iterrows():
            instances_scores_map = similarities[test_record["id"]]
            if  max_threshold:
                elements_to_drop = []
                for key in instances_scores_map:
                    if instances_scores_map[key] >=max_threshold:
                        elements_to_drop.append(key)
                for key in elements_to_drop:
                        del instances_scores_map[key]
            instances_scores = list(zip(instances_scores_map.keys(), instances_scores_map.values()))
            instances_scores.sort(key = lambda x: x[1], reverse=True)
            for k in ks:
                top_indices, top_scores = zip(*instances_scores[:k])
                samples = df_training[df_training["id"].isin(top_indices)]
                samples.drop_duplicates(["id"], inplace=True) # in perspectrum dataset some entries are duplicate
                #print(test_record["id"])
                samples["test-id"] = test_record["id"]
                samples["score"]=top_scores
                samples["k"]=k
                all_samples.append(samples)
    df_samples = pd.concat(all_samples)
    if max_threshold:
        path_samples = path_samples.replace(".tsv", f"-{max_threshold:.2}.tsv")
    df_samples.to_csv(path_samples, sep="\t", encoding="utf-8", columns=["topic", "stance", "text", "id", "score", "test-id", "k"])

def get_thresholds_for_percentiles(path_similarities, percentile_num):
    similarities = load_similarities(path_similarities)
    similarity_list = []
    for test_index in similarities:
        similarity_list.extend(similarities[test_index].values())
    percentile_size = len(similarity_list) // percentile_num
    indices = range(0,len(similarity_list),percentile_size)
    print(indices)
    similarity_list = sorted(similarity_list)
    thrsholds = [similarity_list[i] for i in list(indices)]

    return thrsholds

def get_pathes_for_thresholds(path_sample_root, path_similarities, percentile_num):
    thresholds = get_thresholds_for_percentiles(path_similarities, percentile_num)
    threshold_pathes_list = []
    for threshold in thresholds:
        path_samples = path_sample_root.replace(".tsv", f"-{threshold:.2}.tsv")
        threshold_pathes_list.append((threshold, path_samples))
    return threshold_pathes_list


def evaluate_samples(experiment, path_samples, debug):
    dataset =  load_splits(experiment, oversample=False, validate=False, drop_duplicate_perspectives=False, debug=debug)
    df = dataset["test"]

    all_metrics = []
    for k in get_ks(experiment):
        predictions = []
        df_all_similar_examples = load_similar_examples(experiment, "test", path_similar_examples=path_samples, topic_count=None, few_shot_size=k)
        for _, record in df.iterrows():
            training_dataset = get_similar_examples(record["id"], df_examples=df_all_similar_examples)
            if not len(training_dataset):
                pass
            labels = training_dataset["stance"].values
            counter = Counter(labels)


            label = counter.most_common(1)[0][0]
            predictions.append(label)
        labels = df["stance"]
        metrics = {}
        if experiment == "vast":
            f1s = f1_score(labels, predictions, average=None, labels=[0, 1, 2])
            neutral_f1 = f1s[2]
            metrics[f"test/neutral-f1"] = neutral_f1
        else:
            f1s = f1_score(labels, predictions, average=None, labels=[0, 1])
        con_f1 = f1s[0]
        pro_f1 = f1s[1]

        macro_f1 = f1_score(labels, predictions, average="macro")
        accuracy = accuracy_score(labels, predictions)
        metrics[f"test/pro-f1"] = pro_f1
        metrics[f"test/con-f1"] = con_f1
        metrics[f"test/macro-f1"] = macro_f1
        metrics[f"test/accuracy"] = accuracy
        metrics["k"] = k
        all_metrics.append(metrics)
    return all_metrics
