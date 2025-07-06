
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from collections import defaultdict
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from scipy.spatial.distance import cosine


def calc_similarity_sentence_transformer(df_test, df_training):
    model = SentenceTransformer('all-mpnet-base-v2')
    df_test["topic-text"] = df_test.apply(lambda record: record["topic"] + "[SEP]" + record["text"], axis=1)
    df_training["topic-text"] = df_training.apply(lambda record: record["topic"] + "[SEP]" + record["text"],  axis=1)
    test_text = df_test["topic-text"]
    training_text = df_training["topic-text"]
    #test_text = df_test["text"]
    #training_text = df_training["text"]
    test_embeddings = model.encode(test_text.values.tolist())
    training_embeddings = model.encode(training_text.values.tolist())
    cosine_scores = util.cos_sim(test_embeddings, training_embeddings)
    positve_cosine_scores = np.absolute(cosine_scores)
    similarities = defaultdict(dict)
    i=0
    j=0
    for _, test_record in df_test.iterrows():
        for _, train_record in df_training.iterrows():
            similarities[test_record["id"]][train_record["id"]] = float(positve_cosine_scores[i,j])
            j = j + 1
        i = i + 1
        j = 0
    return similarities

