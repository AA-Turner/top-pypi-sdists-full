from enum import Enum


class DatasetFormat(str, Enum):
    csv = "csv"
    feather = "feather"
    jsonl = "jsonl"
