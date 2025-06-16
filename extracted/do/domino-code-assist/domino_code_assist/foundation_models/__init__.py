from itertools import chain

import datasets
import pandas as pd


def df_to_ds(df, text_col, label_col):
    df = df[[label_col, text_col]]

    labels = df[label_col].unique().tolist()
    features = datasets.Features({text_col: datasets.Value("string"), label_col: datasets.ClassLabel(num_classes=len(labels), names=labels)})
    return datasets.Dataset.from_pandas(df, features=features)


def df_to_ds_ner(hf_data: pd.DataFrame, ner_tags_col: str):
    """Converts a pandas df of huggingface data into a well-formed Dataset

    ex input:
                 tokens         ner_tags
          0      [sentence, 1]      [U-word, O]
          1  [sentence, Apple]  [U-word, U-ORG]

    This will create a huggingface dataset from the input, and also map the `ner_tags`
    into a ClassLabel object which is required for training.
    """
    labels = sorted(set(chain.from_iterable(hf_data[ner_tags_col].tolist())))
    # O is typically the first tag. Move it there
    if "O" in labels:
        labels.remove("O")
        labels.insert(0, "O")
    ds = datasets.Dataset.from_pandas(hf_data)
    # https://github.com/python/mypy/issues/6239
    class_label = datasets.Sequence(feature=datasets.ClassLabel(num_classes=len(labels), names=labels))
    # First need to string index the ner_tags
    label_to_idx = dict(zip(labels, range(len(labels))))
    ds = ds.map(lambda row: {ner_tags_col: [label_to_idx[tag] for tag in row[ner_tags_col]]})
    # Then we can create the ClassLabel
    ds = ds.cast_column(ner_tags_col, class_label)
    return ds


def img_df_to_ds(df, label_col):
    ds = datasets.Dataset.from_pandas(df)
    labels = sorted(df[label_col].unique())
    class_label = datasets.ClassLabel(num_classes=len(labels), names=labels)
    return ds.cast_column(label_col, class_label)
