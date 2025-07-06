import json
import os
import pandas as pd
from few_shot_priming.config import *
from tqdm import tqdm
from few_shot_priming.experiments import *
from few_shot_priming.argument_sampling.stance_priming import *
# from config import *
import argparse


def adapt_ibmsc(df):
    labels = {"PRO": 1, "CON": 0}
    df["stance"] = df["claims.stance"].apply(lambda x: labels[x])
    df = df[["topicText", "claims.claimCorrectedText", "stance", "claims.claimId"]]
    df.rename(columns={"topicText": "topic", "claims.claimCorrectedText": "text", "claims.claimId": "id"}, inplace=True)
    return df[["topic", "stance", "text", "id"]]


def adapt_vast(df):
    df = df[["topic_str", "post", "label", "new_id", "arc_id"]]
    df.rename(columns={"topic_str": "topic", "post": "text", "label": "stance", "new_id": "id", "arc_id": "unique_id"},
              inplace=True)
    # df.drop_duplicates(subset=["text"], inplace=True)
    # df = df[df['stance'] != 2]
    return df[["topic", "stance", "text", "id", "unique_id"]]



def adapt_perspectrum(df):
    labels = {"SUPPORT": 1, "UNDERMINE": 0}
    df["stance"] = df["stance"].apply(lambda x: labels[x])
    return df[["topic", "stance", "text", "id"]]


def load_dataset(experiment):

    csv_file_train_path = f"../../experiment/{experiment}-train.csv"
    csv_file_val_path = f"../../experiment/{experiment}-validation.csv"
    csv_file_test_path = f"../../experiment/{experiment}-test.csv"

    df_training = pd.read_csv(csv_file_train_path)
    df_validation = pd.read_csv(csv_file_val_path)
    df_test = pd.read_csv(csv_file_test_path)

    return {"training": df_training, "validation": df_validation, "test": df_test}


def get_most_similar(ks, experiment):
    file_path = f"similarity/similarities-{experiment}-test-sentence-transformer.json"
    with open(file_path, "r") as file:
        similarities = json.load(file)

    dataset = load_dataset(experiment)
    for split in dataset:
        if experiment == "ibmsc":
            dataset[split] = adapt_ibmsc(dataset[split])
        elif experiment == "perspectrum":
            dataset[split] = adapt_perspectrum(dataset[split])
        else:
            dataset[split] = adapt_vast(dataset[split])
    csv_df = dataset["training"]
    val_id_list = list(dataset["validation"]["id"])
    train_id_list = list(dataset["training"]["id"])

    rows = []
    for key, similarity_dict in similarities.items():
        max_pids = sorted(similarity_dict, key=similarity_dict.get, reverse=True)
        max_pids = [id for id in max_pids if int(id) not in val_id_list]
        max_pids = [id for id in max_pids if int(id) in train_id_list]

        ks_count = 0
        for id in max_pids:
            topic = csv_df.loc[csv_df['id'] == int(id), 'topic'].iloc[0]
            text = csv_df.loc[csv_df['id'] == int(id), 'text'].iloc[0]
            stance = csv_df.loc[csv_df['id'] == int(id), 'stance'].iloc[0]

            row = {
                'topic': topic,
                'stance': stance,
                'text': text,
                'id': id,
                'score': similarity_dict[id],
                'test-id': key,
                'k': ks
            }
            rows.append(row)
            ks_count += 1
            if ks_count == ks:
                break

    df = pd.DataFrame(rows)
    save_file_path = f"sampling_strategies/{experiment}-most-similar.tsv"
    mode = 'a' if os.path.exists(save_file_path) else 'w'
    with open(save_file_path, mode, newline='') as file:
        df.to_csv(file, sep='\t', index=False, header=not os.path.exists(save_file_path))

def get_most_similar_balanced(ks, experiment):
    file_path = f"similarity/similarities-{experiment}-test-sentence-transformer.json"
    with open(file_path, "r") as file:
        similarities = json.load(file)

    dataset = load_dataset(experiment)
    split_n = 2
    for split in dataset:
        if experiment == "ibmsc":
            dataset[split] = adapt_ibmsc(dataset[split])
        elif experiment == "perspectrum":
            dataset[split] = adapt_perspectrum(dataset[split])
        else:
            dataset[split] = adapt_vast(dataset[split])
            split_n = 3

    csv_df = dataset["training"]
    val_id_list = list(dataset["validation"]["id"])
    train_id_list = list(dataset["training"]["id"])

    rows = []
    for key, similarity_dict in tqdm(similarities.items()):
        max_pids = sorted(similarity_dict, key=similarity_dict.get, reverse=True)
        max_pids = [id for id in max_pids if int(id) not in val_id_list]
        max_pids = [id for id in max_pids if int(id) in train_id_list]

        pro_count, con_count, neutral_count = 0, 0, 0
        pro_rows, con_rows, neutral_rows = [], [], []
        for id in max_pids:
            topic = csv_df.loc[csv_df['id'] == int(id), 'topic'].iloc[0]
            text = csv_df.loc[csv_df['id'] == int(id), 'text'].iloc[0]
            stance = csv_df.loc[csv_df['id'] == int(id), 'stance'].iloc[0]

            row = {
                'topic': topic,
                'stance': stance,
                'text': text,
                'id': id,
                'score': similarity_dict[id],
                'test-id': key,
                'k': ks
            }

            if stance == 1 and pro_count < ks / split_n:
                pro_rows.append(row)
                pro_count += 1
            elif stance == 0 and con_count < ks / split_n:
                con_rows.append(row)
                con_count += 1
            elif stance == 2 and neutral_count < ks / split_n:
                neutral_rows.append(row)
                neutral_count += 1

            if pro_count == ks / split_n and con_count == ks / split_n and (split_n == 2 or neutral_count == ks / split_n):
                rows.extend(pro_rows + con_rows + neutral_rows)
                break

    df = pd.DataFrame(rows)
    save_file_path = f"sampling_strategies/{experiment}-most-similar-balanced.tsv"
    mode = 'a' if os.path.exists(save_file_path) else 'w'
    with open(save_file_path, mode, newline='') as file:
        df.to_csv(file, sep='\t', index=False, header=not os.path.exists(save_file_path))


def get_most_similar_different_topics(experiment, drop_duplicates=False, max_threshold=None):
    config = load_config()
    file_path = config["topic-similarity"]["sentence-transformer-similarity-path"][f"{experiment}-test"]
    save_file_path = config["topic-similarity"]["similar-examples-ks"][f"{experiment}-test"]

    if drop_duplicates:
        save_file_path = save_file_path.replace(".tsv", "-no-duplicates.tsv")
    print(save_file_path)
    if experiment == "vast":
        ks = [3, 6, 12, 24, 48, 96]
    else:
        ks = [2, 4, 8, 16, 32, 64]

    #f"similarity/similarities-{experiment}-test-sentence-transformer.json"
    with open(file_path, "r") as file:
        similarities = json.load(file)
    ## drop duplicates apply only to perspectrum
    dataset =  load_splits(experiment, oversample=False, validate=False, drop_duplicate_perspectives=drop_duplicates)

    split_n = 2
    if experiment == "vast":
        split_n = 3
    csv_df = dataset["training"]
    #val_id_list = list(dataset["validation"]["id"])
    train_id_list = list(dataset["training"]["id"])

    rows = []
    for k in ks:
        for key, similarity_dict in tqdm(similarities.items()):
            max_pids = sorted(similarity_dict, key=similarity_dict.get, reverse=True)
            #max_pids = [id for id in max_pids if int(id) not in val_id_list]
            if max_threshold:
                max_pids = [id for id in max_pids if int(id) in train_id_list and similarity_dict[id]<=max_threshold]
            else:
                max_pids = [id for id in max_pids if int(id) in train_id_list]

            pro_rows, con_rows, neutral_rows = [], [], []
            pro_count, con_count, neutral_count = 0, 0, 0
            pro_topics, con_topics, neutral_topics = set(), set(), set()
            for id in max_pids:
                topic = csv_df.loc[csv_df['id'] == int(id), 'topic'].iloc[0]
                text = csv_df.loc[csv_df['id'] == int(id), 'text'].iloc[0]
                stance = csv_df.loc[csv_df['id'] == int(id), 'stance'].iloc[0]

                row = {
                    'topic': topic,
                    'stance': stance,
                    'text': text,
                    'id': id,
                    'score': similarity_dict[id],
                    'test-id': key,
                    'k': k
                }

                if stance == 1 and pro_count < k / split_n and topic not in pro_topics:
                    pro_rows.append(row)
                    pro_topics.add(topic)
                    pro_count += 1
                elif stance == 0 and con_count < k / split_n and topic not in con_topics:
                    con_rows.append(row)
                    con_topics.add(topic)
                    con_count += 1
                elif stance == 2 and neutral_count < k / split_n and topic not in neutral_topics:
                    neutral_rows.append(row)
                    neutral_topics.add(topic)
                    neutral_count += 1

                if pro_count == k / split_n and con_count == k / split_n and (split_n == 2 or neutral_count == k / split_n):
                    rows.extend(pro_rows + con_rows + neutral_rows)
                    break

    df = pd.DataFrame(rows)

    if max_threshold:
        save_file_path = save_file_path.replace(".tsv", f"-{max_threshold:.2}.tsv")
    if len(rows):
        df.to_csv(save_file_path, sep='\t', index=False)


def get_most_similar_majority_stance_different_topic_balanced(ks, experiment):
    file_path = f"similarity/similarities-{experiment}-test-sentence-transformer.json"
    with open(file_path, "r") as file:
        similarities = json.load(file)

    dataset = load_dataset(experiment)
    split_n = 2
    for split in dataset:
        if experiment == "ibmsc":
            dataset[split] = adapt_ibmsc(dataset[split])
        elif experiment == "perspectrum":
            dataset[split] = adapt_perspectrum(dataset[split])
        else:
            split_n = 3
            dataset[split] = adapt_vast(dataset[split])
    csv_df = dataset["training"]
    val_id_list = list(dataset["validation"]["id"])
    train_id_list = list(dataset["training"]["id"])

    rows = []
    for key, similarity_dict in similarities.items():
        max_pids = sorted(similarity_dict, key=similarity_dict.get, reverse=True)
        max_pids = [id for id in max_pids if int(id) not in val_id_list]
        max_pids = [id for id in max_pids if int(id) in train_id_list]
        max_100_pids = [id for id in max_pids if int(id) in train_id_list][:100]

        topic_count = {}
        for id in max_100_pids:
            topic = csv_df.loc[csv_df['id'] == int(id), 'topic'].iloc[0]
            if topic not in topic_count:
                topic_count[topic] = 0
            topic_count[topic] += 1
        top_topics = sorted(topic_count, key=topic_count.get, reverse=True)

        # If there are less than ks of top-topics, the loop recursively takes enough ks, top topics can repeat.
        top_topics_ks = []
        for count in range(max(ks, len(top_topics))):
            for topic in top_topics:
                if topic_count[topic] == 0:
                    continue
                topic_count[topic] -= 1
                top_topics_ks.append(topic)

        pro_rows, con_rows, neutral_rows = [], [], []
        temp_max_pids = []
        for topic in top_topics_ks:
            pro_rows_topic, con_rows_topic, neutral_rows_topic = [], [], []
            for id in max_pids:
                if csv_df.loc[csv_df['id'] == int(id), 'topic'].iloc[0] == topic:
                    temp_max_pids.append(id)
                    stance = csv_df.loc[csv_df['id'] == int(id), 'stance'].iloc[0]
                    text = csv_df.loc[csv_df['id'] == int(id), 'text'].iloc[0]
                    score = similarity_dict[id]
                    row = {
                        'topic': topic,
                        'stance': stance,
                        'text': text,
                        'id': id,
                        'score': score,
                        'test-id': key,
                        'k': ks
                    }
                    if stance == 1:
                        pro_rows_topic.append(row)
                    elif stance == 0:
                        con_rows_topic.append(row)
                    elif stance == 2:
                        neutral_rows_topic.append(row)
                    break
            max_pids = [item for item in max_pids if item not in temp_max_pids]

            pro_rows.extend(sorted(pro_rows_topic, key=lambda x: x['score'], reverse=True))
            con_rows.extend(sorted(con_rows_topic, key=lambda x: x['score'], reverse=True))
            neutral_rows.extend(sorted(neutral_rows_topic, key=lambda x: x['score'], reverse=True))

        rows.extend(pro_rows[:ks // split_n] + con_rows[:ks // split_n] + neutral_rows[:ks // split_n])

    df = pd.DataFrame(rows)
    save_file_path = f"sampling_strategies/{experiment}-most-similar-majority-stance-different-topic.tsv"
    mode = 'a' if os.path.exists(save_file_path) else 'w'
    with open(save_file_path, mode, newline='') as file:
        df.to_csv(file, sep='\t', index=False, header=not os.path.exists(save_file_path))


if __name__ == '__main__':
    # vast  perspectrum  ibmsc

    parser = argparse.ArgumentParser()
    parser.add_argument("--vast", action="store_true")
    parser.add_argument("--perspectrum", action="store_true")
    parser.add_argument("--ibmsc", action="store_true")
    parser.add_argument("--drop-duplicate-perspectives", action="store_true")
    parser.add_argument("--percentiles", type=int)
    args =  parser.parse_args()
    if args.vast:
        experiment = "vast"
    elif args.perspectrum:
        experiment = "perspectrum"
    elif args.ibmsc:
        experiment = "ibmsc"
    else:
        experiment = None

    if experiment:
        if args.percentiles:
            config = load_config()
            file_path = config["topic-similarity"]["sentence-transformer-similarity-path"][f"{experiment}-test"]
            thresholds = get_thresholds_for_percentiles(file_path, args.percentiles)
            for threshold in thresholds:
                get_most_similar_different_topics(experiment=experiment, drop_duplicates=args.drop_duplicate_perspectives, max_threshold=threshold)
        else:
            get_most_similar_different_topics(experiment=experiment, drop_duplicates=args.drop_duplicate_perspectives)

    else:
        for possible_e in ["perspectrum", "ibmsc", "vast"]:
            get_most_similar_different_topics(experiment=possible_e, drop_duplicates=args.drop_duplicate_perspectives)
            print(f"finished-{possible_e}")


    # get_most_similar(ks=24, experiment="vast")
    # get_most_similar_balanced(ks=24, experiment="vast")
    # get_most_similar_different_topics(ks=24, experiment="vast")
    # get_most_similar_majority_stance_different_topic(ks=24, experiment="vast")

    # get_most_similar_majority_stance_different_topic_balanced(16, "perspectrum")
    # get_most_similar_majority_stance_different_topic_balanced(16, "vast")
    # get_most_similar_majority_stance_different_topic_balanced(16, "ibmsc")
    # get_most_similar(ks=2, experiment="perspectrum")
    # get_most_similar(ks=4, experiment="perspectrum")
    # get_most_similar(ks=8, experiment="perspectrum")
