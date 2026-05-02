### manual_evaluation_dataset_creation_example_script.py ###
# This script demonstrates how to create a manual evaluation dataset
# For manual evaluation datasets, all test cases are uploaded manually, with input, expected_output, and expected_extra_info fields
# Evaluation datasets, once published, can be used for application variant runs and report card generation

import os
from typing import List

from scale_gp import SGPClient
from scale_gp.types.evaluation_datasets.test_case import TestCase
from scale_gp.types.evaluation_datasets.test_case_batch_params import Item
from scale_gp.types.evaluation_datasets.test_case_create_params import TestCaseData

account_id = os.environ.get("SGP_ACCOUNT_ID", None)
api_key = os.environ.get("SGP_API_KEY", None)

assert (
    account_id is not None
), "You need to set the SGP_ACCOUNT_ID - you can find it at https://egp.dashboard.scale.com/admin/accounts"
assert api_key is not None, "You need to provide your API key - see https://egp.dashboard.scale.com/admin/api-key"

# Create an SGP Client
client = SGPClient(api_key=api_key)

### manual evaluation dataset ###
DATASET: List[TestCaseData] = [
    {
        "input": "What is the capital of France?",
        "expected_output": "The capital of France is Paris.",
        "expected_extra_info": {
            "info": "Paris, located in the northern part of France along the Seine River, is not only the country’s capital but also its largest city. Known for its art, fashion, gastronomy, and culture, Paris has a significant influence both in France and globally.",
            "schema_type": "STRING",
        },
    },
    {
        "input": "What color is an apple?",
        "expected_output": "An apple is typically red when ripe, though green and yellow varieties also exist depending on the species and maturity.",
        "expected_extra_info": {
            "info": "Apples come in various colors including red, green, and yellow. Red apples are one of the most common, with varieties like Red Delicious being very popular. Green apples, like Granny Smith, are tart and used often in baking. Yellow apples such as Golden Delicious are sweet and softer.",
            "schema_type": "STRING",
        },
    },
    {
        "input": "Who is the first president of the USA?",
        "expected_output": "The first president of the USA is George Washington.",
        "expected_extra_info": {
            "info": "George Washington served as the first president of the United States from 1789 to 1797. He is a pivotal figure in American history, recognized for his leadership during the Revolutionary War and setting many precedents for the national government.",
            "schema_type": "STRING",
        },
    },
]

# create evaluation dataset to contain your test cases
manual_evaluation_dataset = client.evaluation_datasets.create(
    account_id=account_id,
    name="manual_evaluation_dataset",
    schema_type="GENERATION",
    type="manual",
)

# iteratively upload test cases
test_cases: List[TestCase] = []
for test_case in DATASET:
    uploaded_test_case = client.evaluation_datasets.test_cases.create(
        account_id=account_id,
        evaluation_dataset_id=manual_evaluation_dataset.id,
        test_case_data=test_case,
    )
    test_cases.append(uploaded_test_case)

items: List[Item] = [Item({"account_id": account_id, "test_case_data": item}) for item in DATASET]

# alternatively you can use batching for faster uploads
uploaded_test_cases = client.evaluation_datasets.test_cases.batch(
    evaluation_dataset_id=manual_evaluation_dataset.id,
    items=items,
)
test_cases.extend(uploaded_test_cases)

# snapshot into a dataset version
manual_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.create(
    evaluation_dataset_id=manual_evaluation_dataset.id
)

# publish the dataset. datasets must be published before they can be used in evaluations.
published_dataset_response = client.evaluation_datasets.publish(
    evaluation_dataset_id=manual_evaluation_dataset.id,
)

print("Published manual evaluation dataset with id:", manual_evaluation_dataset.id)
print(manual_dataset_version)

published_test_cases = client.evaluation_datasets.test_cases.list(
    evaluation_dataset_id=manual_evaluation_dataset.id, account_id=account_id
)

print("Created the following test cases:")
print(published_test_cases.items)
