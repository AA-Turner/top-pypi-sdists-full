"""Basic usage of CustomFunction for evaluation tasks.

This example shows how to:
1. Define a custom scoring function
2. Test it with a dry run
3. Create a full evaluation
4. Inspect results

Prerequisites:
    pip install scale-gp-beta

    Set environment variables or pass directly:
    - SGP_API_KEY
    - SGP_ACCOUNT_ID
"""

import os
import time
from typing import Dict, List

from scale_gp_beta import SGPClient
from scale_gp_beta.lib import CustomFunction, get_evaluation_columns

client = SGPClient(
    api_key=os.environ["SGP_API_KEY"],
    account_id=os.environ["SGP_ACCOUNT_ID"],
    environment="development",
)

# --- 1. Define functions ---
# Imports must be INSIDE the function body.


def string_similarity(expected: str, actual: str) -> float:
    import difflib

    return difflib.SequenceMatcher(None, expected, actual).ratio()


def length_ratio(expected: str, actual: str) -> float:
    if len(expected) == 0:
        return 0.0
    return len(actual) / len(expected)


# --- 2. Wrap in CustomFunction ---

cf_similarity = CustomFunction(func=string_similarity, alias="similarity")

# Use arg_mapping when function params don't match column names
cf_length = CustomFunction(
    func=length_ratio,
    alias="length_ratio",
    arg_mapping={"expected": "reference", "actual": "response"},
)

# Inspect serialized output
print("Serialized task config:")
print(cf_similarity.serialize())
print(cf_length.serialize())

# --- 3. Dry run ---

sample_data: List[Dict[str, object]] = [
    {"expected": "The capital of France is Paris.", "actual": "Paris is the capital of France."},
    {"expected": "Hello world", "actual": "Hello wrold"},
]

print("\nDry run (similarity):")
print(cf_similarity.dry_run(client=client, sample_data=sample_data))

mapped_data: List[Dict[str, object]] = [
    {"reference": "The capital of France is Paris.", "response": "Paris is the capital of France."},
    {"reference": "Hello world", "response": "Hello wrold"},
]

print("\nDry run (length_ratio with arg_mapping):")
print(cf_length.dry_run(client=client, sample_data=mapped_data))

# --- 4. Create evaluation ---

evaluation = client.evaluations.create(
    evaluation={
        "name": "custom_function_example",
        "tasks": [cf_similarity.serialize()],
        "data": sample_data,
    },
)
print(f"\nEvaluation created: {evaluation.id}")

# Poll until done
while True:
    evaluation = client.evaluations.retrieve(evaluation.id)
    print(f"  Status: {evaluation.status}")
    if evaluation.status in ("completed", "failed"):
        break
    time.sleep(5)

# --- 5. Inspect results ---

print("\nResults:")
items = client.evaluation_items.list(evaluation_id=evaluation.id)
for item in items:
    print(f"  data: {item.data}, errors: {item.task_errors}")

# --- 6. Discover columns from an existing evaluation ---

print("\nAvailable columns:")
columns = get_evaluation_columns(client, evaluation.id)
for col in columns:
    print(f"  {col.field_name} ({col.data_type})")
