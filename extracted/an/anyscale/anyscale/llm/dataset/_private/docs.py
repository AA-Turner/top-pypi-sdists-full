GET_PY_EXAMPLE = """
import anyscale
from anyscale.llm.dataset import Dataset

dataset: Dataset = anyscale.llm.dataset.get("my_first_dataset")
print(f"Dataset name: '{dataset.name}'")  # Dataset name: 'my_first_dataset'

# Get the second latest version of the dataset
prev_dataset = anyscale.llm.dataset.get("my_first_dataset", version=-1)
"""

GET_PY_ARG_DOCSTRINGS = {
    "name": "Name of the dataset",
    "version": "Version of the dataset. If a negative integer is provided, the dataset returned is this many versions back of the latest version. Default: Latest version.",
    "project": "Name of the Anyscale project that the dataset belongs to. If not provided, all projects will be searched.",
}

UPLOAD_PY_EXAMPLE = """
import anyscale

anyscale.llm.dataset.upload("path/to/my_first_dataset.jsonl", name="my_first_dataset")
anyscale.llm.dataset.upload("my_dataset.jsonl", "second_dataset")
anyscale.llm.dataset.upload("my_dataset2.jsonl", "second_dataset", description="added 3 lines")
"""

UPLOAD_PY_ARG_DOCSTRINGS = {
    "dataset_file": "Path to the dataset file to upload.",
    "name": "Name of a new dataset, or an existing dataset, to upload a new version of.",
    "description": "Description of the dataset version.",
    "cloud": "Name of the Anyscale cloud to upload a new dataset to. If not provided, the default cloud will be used.",
    "project": "Name of the Anyscale project to upload a new dataset to. If not provided, the default project of the cloud will be used.",
}

DOWNLOAD_PY_EXAMPLE = """
import anyscale

dataset_contents: bytes = anyscale.llm.dataset.download("my_first_dataset.jsonl")
jsonl_obj = [json.loads(line) for line in dataset_contents.decode().splitlines()]

prev_dataset_contents = anyscale.llm.dataset.download("my_first_dataset.jsonl", version=-1)
"""

DOWNLOAD_PY_ARG_DOCSTRINGS = {
    "name": "Name of the dataset to download.",
    "version": "Version of the dataset to download. If a negative integer is provided, the dataset returned is this many versions back of the latest version. Default: Latest version.",
    "project": "Name of the Anyscale project to download the dataset from. If not provided, all projects will be searched.",
}

LIST_PY_EXAMPLE = """
import anyscale

datasets = anyscale.llm.dataset.list(limit=10)
for d in datasets:
    print(f"Dataset name: '{d.name}'")  # Prints 10 dataset names
"""

LIST_PY_ARG_DOCSTRINGS = {
    "limit": "Maximum number of datasets to return. Default: 1000.",
    "after": "ID of the dataset to start the listing from. If provided, the list will start from the dataset after this ID.",
    "name_contains": "Filter datasets by name. If provided, only datasets with name containing this string will be returned.",
    "cloud": "Name of the Anyscale cloud to search in. If not provided, all clouds will be searched.",
    "project": "Name of the Anyscale project to search in. If not provided, all projects will be searched.",
}
