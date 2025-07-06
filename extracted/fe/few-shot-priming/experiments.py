import pandas as pd
import os
import math
from few_shot_priming.config import *
from few_shot_priming.argument_sampling.topic_similarity import *


def save_splits():
    """
    Save the splits of the experiments by sampling a validation set from the training set with exclusive topic sets
    :return:
    """
    path_source, path_training, path_validation, path_test = get_experiment_paths()
    df_arguments = pd.read_csv(path_source, sep=",", encoding="utf-8")
    df_training = df_arguments[df_arguments["split"] == "train"]
    df_test = df_arguments[df_arguments["split"] == "test"]
    training_topics = df_training["topicTarget"].sample(12).unique()
    training_topics = training_topics[:10]
    df_sampled_training = df_training[df_training["topicTarget"].isin(training_topics)]
    df_validation = df_training[~df_training["topicTarget"].isin(training_topics)]
    df_sampled_training.to_csv(path_training, sep=",", encoding="utf-8", index=False)
    df_validation.to_csv(path_validation, sep=",", encoding="utf-8", index=False)
    df_test.to_csv(path_test, sep=",", encoding="utf-8", index=False)
    #save_splits_topic_counts()
def save_splits_topic_counts():

    for experiment in ["ibmsc", "vast"]:
        path_source, path_training, path_validation, path_test = get_experiment_paths(experiment)
        df_training = pd.read_csv(path_training, sep=",", encoding="utf-8")
        df_validation = pd.read_csv(path_validation, sep=",", encoding="utf-8")
        df_training["split"] = "training"
        df_validation["split"] = "validation"
        df_all_training = pd.concat([df_training, df_validation])

        if experiment == "ibmsc":
            topic_label = "topicText"
        else:
            topic_label = "topic_str"
        is_validate = False
        topic_count_range = get_topic_count_range(experiment, is_validate)

        for topic_count in topic_count_range:
            df_all_training[f"topic-count-{topic_count}"]=False
            topics = df_all_training[topic_label].unique()
            chosen_topics = np.random.choice(topics, topic_count, replace=False)
            df_all_training[f"topic-count-{topic_count}"] = df_all_training[topic_label].apply(lambda x: x in chosen_topics)

        df_training = df_all_training[df_all_training["split"] == "training"]
        df_validation = df_all_training[df_all_training["split"] == "validation"]
        del df_training["split"]
        del df_validation["split"]
        df_training.to_csv(f"/home/yamen/projects/few-shot-priming/experiment/{experiment}-train.csv", sep=",", encoding="utf-8", index=False)
        df_validation.to_csv(f"/home/yamen/projects/few-shot-priming/experiment/{experiment}-validation.csv", sep=",", encoding="utf-8", index=False)

def oversample_dataset(df, experiment):

    if experiment == "ibmsc" or experiment == "perspectrum":
        if experiment == "ibmsc":
            stance_label = "claims.stance"
            pro_label = "Pro"
            con_label = "Con"
        else:
            stance_label = "stance"
            pro_label = "SUPPORT"
            con_label = "UNDERMINE"
        pro_claims = df[df[stance_label]==pro_label]
        con_claims = df[df[stance_label]==con_label]
        count_of_con_to_sample = pro_claims.shape[0] - con_claims.shape[0]
        if count_of_con_to_sample > 0:
            if count_of_con_to_sample <= len(con_claims):
                con_claims_to_add = con_claims.sample(count_of_con_to_sample)
            else:
                con_claims_to_add = con_claims.sample(count_of_con_to_sample, replace=True)
            df = pd.concat([df, con_claims_to_add])
        elif count_of_con_to_sample < 0:
            count_of_pro_to_sample = - count_of_con_to_sample
            if count_of_pro_to_sample <= len(pro_claims):
                pro_claims_to_add = pro_claims.sample(count_of_pro_to_sample)
            else:
                pro_claims_to_add = pro_claims.sample(count_of_pro_to_sample, replace=True)
            df = pd.concat([df, pro_claims_to_add])
        else:
            pass
        return df
    else:
        max_label_count = df["label"].value_counts().max()
        all_labels_to_add = []
        for label, df_label in df.groupby("label"):
            instances_to_sample = max_label_count -  len(df_label)
            if instances_to_sample <= len(df_label):
                df_label_to_add = df_label.sample(instances_to_sample)
            else:
                df_label_to_add = df_label.sample(instances_to_sample, replace=True)
            all_labels_to_add.append(df_label_to_add)
        all_labels_to_add.append(df)
        return pd.concat(all_labels_to_add)

def adapt_ibmsc(df):
    labels = {"PRO": 1, "CON":0}
    df["stance"] = df["claims.stance"].apply(lambda x: labels[x])
    df = df [["topicText", "claims.claimCorrectedText", "stance", "claims.claimId"]]
    df.rename(columns={"topicText" : "topic", "claims.claimCorrectedText": "text", "claims.claimId": "id"}, inplace=True)
    return df[["topic", "stance", "text", "id"]]

def adapt_vast(df):
    df = df[["topic_str", "post", "label", "new_id", "arc_id"]]
    df.rename(columns={"topic_str":"topic", "post": "text", "label": "stance", "new_id":"id", "ori_id": "unique_id"}, inplace=True)
    #df["topic"] = df["topic"].apply(lambda topic: " ".join(topic))
    #df["stance"] = df["stance"].apply(lambda stance: stance.caplitalize())
    return df[["topic", "stance", "text", "id", "arc_id"]]

def adapt_perspectrum(df):
    labels = {"SUPPORT": 1, "UNDERMINE":0}
    df["stance"] = df["stance"].apply(lambda x: labels[x])
    return df

def load_splits(experiment, oversample=True, validate=True, drop_duplicate_perspectives=False, adapt=True, topic_count=None, debug=False):
    """
    Load the splits of the experiments and return it in a dictionary of pandas dataframes
    :return: a dictionary containing the training, validation, and test splits
    """
    if experiment == "ibmsc":
        dataset_id="claims.claimId"
        topic_label = "topicText"
    elif experiment == "perspectrum":
        dataset_id="id"
        topic_label = "topic"
    else:
        dataset_id = "new_id"
        topic_label = "topic_str"

    path_source, path_training, path_validation, path_test = get_experiment_paths(experiment)
    if experiment == "ibmsc" and not os.path.exists(path_validation):
        save_splits()
    df_training = pd.read_csv(path_training, sep=",", encoding="utf-8")
    df_validation = pd.read_csv(path_validation, sep=",", encoding="utf-8")
    df_test = pd.read_csv(path_test, sep=",", encoding="utf-8")
    if experiment =="vast":
        if validate:
            df_validation = df_validation[df_validation["seen?"]==0]
        df_test = df_test[df_test["seen?"]==0]

    if experiment == "perspectrum":

        df_training = pd.read_csv(path_training, sep=",", encoding="utf-8")
        df_validation = pd.read_csv(path_validation, sep=",", encoding="utf-8")
        df_test = pd.read_csv(path_test, sep=",", encoding="utf-8")
        if drop_duplicate_perspectives:
            df_training = df_training[~df_training["perspective_id"].isin(df_test["perspective_id"])]
            df_validation = df_validation[~df_validation["perspective_id"].isin(df_test["perspective_id"])]
    if debug:
        #df_training = df_training.sample(400)
        df_validation = df_validation.sample(frac=0.1)
        df_test = df_test.sample(frac=0.1)

    if not validate:
        df_training = pd.concat([df_training, df_validation])
        if topic_count:
            df_training = df_training[df_training[f"topic-count-{topic_count}"]]

    dataset = {"training": df_training, "validation": df_validation, "test": df_test}

    if oversample:
        dataset["training"] = oversample_dataset(dataset["training"], experiment)
    else:
        pass
    for split in dataset:
        dataset[split].sort_values(by=dataset_id, inplace=True)
    if adapt:
        for split in dataset:
            if experiment == "ibmsc":
                dataset[split] = adapt_ibmsc(dataset[split])
            elif experiment == "perspectrum":
                dataset[split] = adapt_perspectrum(dataset[split])
            else:
                dataset[split] = adapt_vast(dataset[split])

    return dataset


def split_train_val_by_topic(part_size, experiment, split):
    train_csv_path = f"../experiment/{experiment}-train.csv"
    val_csv_path = f"../experiment/{experiment}-validation.csv"

    if experiment == "ibmsc":
        train_df = adapt_ibmsc(pd.read_csv(train_csv_path))
        val_df = adapt_ibmsc(pd.read_csv(val_csv_path))
    elif experiment == "perspectrum":
        train_df = adapt_perspectrum(pd.read_csv(train_csv_path))
        val_df = adapt_perspectrum(pd.read_csv(val_csv_path))
    elif experiment == "vast":
        train_df = adapt_vast(pd.read_csv(train_csv_path))
        val_df = adapt_vast(pd.read_csv(val_csv_path))

    if split == "merge":
        df = pd.concat([train_df, val_df], ignore_index=True)
    elif split == "train":
        df = train_df
    elif split == "val":
        df = val_df

    unique_claims = df['topic'].unique()
    num_parts = math.ceil(len(unique_claims) / part_size)

    for i in range(1, num_parts):
        df[f'topic-{i * part_size}'] = False

    for i in range(num_parts):
        start_idx = 0
        end_idx = (i + 1) * part_size
        if i == num_parts - 1:
            df['topic-all'] = True
            break
        claims_in_part = unique_claims[start_idx:end_idx]
        for claim in claims_in_part:
            df.loc[df['topic'] == claim, f'topic-{(i + 1) * part_size}'] = True

    output_csv_path = f"../experiment/split/{experiment}-split-{split}-by-topic.csv"
    df.to_csv(output_csv_path, index=False)

def save_experiment_results(experiment, df_run_results, run_name):
    path_experiment_results = get_results_path(experiment)
    df_run_results["run"] = run_name
    now = datetime.now()
    time_now = now.strftime("%m-%d-%H:%M")
    df_run_results["time"] = time_now


    if os.path.exists(path_experiment_results):
        df_results = pd.read_csv(path_experiment_results, sep="\t", encoding="utf-8")
        df_new_results = pd.concat([df_run_results, df_results])
    else:
        df_new_results = df_run_results
    df_new_results.to_csv(path_experiment_results, sep= "\t", encoding="utf-8", index=False)



