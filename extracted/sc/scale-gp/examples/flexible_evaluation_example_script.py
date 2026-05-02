### flexible_evaluation_example_script.py ###
# This script demonstrates how to create a flexible dataset and evaluation

# What is flexible dataset?

# A flexible dataset is a dataset that can be used to evaluate an application's performance against a set of test cases.
# Flexible datasets are able to perform anything a regular GENERATION dataset can do (covered by evaluation_example_script.py),
# but support a larger range of datatypes for both test case input and outputs.

# Flexible evaluation is only available for external/offline applications

# Schema for test case data:
# Input: Str | Dict[str, str | int | float | chunks | messages | list[any] | Dict[any, any]
# Expected_output: same as input but optional

# What is an evaluation?

# Evaluate an application variant against a rubric (question set) to determine how well the application variant performs.
# Depending on the evaluation type, either use a LLM, human, or mixed (LLM Benchmark) to answer questions comparing the
# response of an application variant to an expected response (test case expected output). Flexible evaluation support human evaluations only currently
# The results of the evaluation can be used to help generate a report card for the application variant, benchmark performance, and compare variants.

# Required steps to perform a flexible evaluation:
# 1. Create a flexible evaluation dataset
# 2. Insert test cases into the flexible evaluation dataset and snapshot into a dataset version.
# 3. Create at question set with at least one question. The question set will be used to evaluate the the responses to the test cases.
# 4. Create an evaluation config using the question set and a desired evaluation type (human, llm or hybrid)
# 5. Create an offline application spec and variant.
# 6. Use the ExternalApplication class and a generator function which calls your offline application to generate outputs
# 7. Create an annotation config. This helps customize the annotation UI per question.
# 8. Create an evaluation using the evaluation config, and the desired offline application variant.

import os
import time
from typing import Any, Dict, List
from datetime import datetime

from scale_gp import SGPClient
from scale_gp.lib.external_applications import ExternalApplication, ExternalApplicationOutputCompletion
from scale_gp.types.annotation_config_param import AnnotationConfigParam
from scale_gp.types.evaluation_datasets.test_case import TestCase
from scale_gp.types.application_test_case_output_batch_params import (
    ItemTraceSpan,
)
from scale_gp.types.evaluation_datasets.test_case_batch_params import Item
from scale_gp.types.evaluation_datasets.test_case_create_params import TestCaseData

account_id = os.environ.get("SGP_ACCOUNT_ID", None)
api_key = os.environ.get("SGP_API_KEY", None)

# Either set these environment variables, or a default application variant and spec will be created
external_application_variant = os.environ.get("SGP_EXTERNAL_APPLICATION_VARIANT_ID", None)
external_application_spec = os.environ.get("SGP_EXTERNAL_APPLICATION_SPEC_ID", None)

assert (
    account_id is not None
), "You need to set the SGP_ACCOUNT_ID - you can find it at https://egp.dashboard.scale.com/admin/accounts"
assert api_key is not None, "You need to provide your API key - see https://egp.dashboard.scale.com/admin/api-key"

# Create an SGP Client
client = SGPClient(api_key=api_key)

# 1. Create a flexible evaluation dataset
flexible_evaluation_dataset = client.evaluation_datasets.create(
    account_id=account_id,
    name="flexible_evaluation_dataset",
    schema_type="FLEXIBLE",
    type="manual",
)

# 2. Batch insert test cases into the flexible evaluation dataset and create a snapshot
# Below are the currently supported types for test case input and output
#     "example_bool": False,
#     "example_float": 3.14,
#     "example_int": 23,
#     "example_messages": [
#         {"role": "user", "content": "What is the capital of France?"},
#         {"role": "assistant", "content": "The capital of France is Paris."},
#         {"role": "assistant", "content": "The capital of France is Paris."},
#         {"role": "user", "content": "Thank you!"},
#         {"role": "user", "content": "Thank you!"},
#     ],
#     "example_dictionary": {
#         "title": "The Great Gatsby",
#         "author": "F. Scott Fitzgerald",
#         "published_year": 1925,
#         "genres": ["Tragedy", "Historical"],
#         "characters": {"protagonist": "Jay Gatsby", "narrator": "Nick Carraway"},
#     },
#     "example_mixed_array": [42, "banana", 3.14, True, {"name": "Alice"}],
#     "example_chunks": [
#         {
#             "text": "I have a dream that one day this nation will rise up and live out the true meaning of its creed.",
#             "metadata": {"speaker": "Martin Luther King Jr.", "year": 1963},
#         },
#         {
#             "text": "Ask not what your country can do for you – ask what you can do for your country.",
#             "metadata": {"speaker": "John F. Kennedy", "year": 1961},
#         },
#         {"text": "The only thing we have to fear is fear itself."},
#     ],
#     "example_document": """**Lorem** ipsum dolor sit amet, consectetur adipiscing elit. Donec ac feugiat metus. Morbi imperdiet eget ante vel interdum. Vestibulum finibus dolor a congue luctus. Aenean hendrerit nec orci ac pulvinar. Mauris feugiat arcu nec placerat vestibulum. Phasellus at diam gravida, rhoncus elit et, rutrum nunc. Pellentesque fermentum iaculis ligula ac rhoncus. Duis pulvinar dolor id hendrerit placerat. Sed vel suscipit sem, ac finibus tortor. Suspendisse commodo, quam sed molestie condimentum, tellus lorem suscipit mi, a fermentum dolor felis in tellus. Nullam diam felis, aliquet ac sagittis in, mattis sed sapien. Duis tempor urna eget aliquet vehicula. Suspendisse nec fermentum erat, sed molestie magna. Nullam laoreet sit amet est sed maximus. Nam eu blandit magna, ut pulvinar quam. Cras dictum eros sed mattis scelerisque.
# Cras mi mauris, pellentesque sit amet pharetra ut, viverra sed dui. Nullam elementum placerat scelerisque. Duis a libero ac purus faucibus dictum id vitae ex. Interdum et malesuada fames ac ante ipsum primis in faucibus. Suspendisse quis egestas odio. Nam non ornare augue, id ullamcorper orci. Praesent faucibus eget lectus sed sodales. Donec sed urna eget odio ornare consequat.
# **Praesent** suscipit massa a justo tempus suscipit. Aenean cursus nunc eget accumsan lacinia. Duis sit amet erat euismod, euismod est vitae, rhoncus sem. Donec aliquam quam facilisis leo accumsan, in tincidunt erat molestie. Cras accumsan convallis erat, id volutpat augue consectetur vel. Proin quis tincidunt tellus. Proin lobortis velit vel arcu commodo hendrerit. Phasellus imperdiet elementum nisl, a rutrum metus facilisis id. Cras placerat arcu sem, a porta orci luctus vitae. Aenean commodo aliquam lectus, vel dignissim augue rutrum ac. Nam pharetra at sem sit amet ultricies. Fusce quis metus et ex euismod malesuada.
# Aenean quis augue a ex cursus pretium. Aenean quis arcu tortor. Phasellus nunc nunc, pulvinar non ornare sed, imperdiet sit amet ipsum. Curabitur commodo maximus metus. Donec imperdiet, felis nec faucibus aliquet, urna nulla interdum enim, vel aliquam nunc lectus condimentum ex. Integer ac tempor mi. Nullam vel convallis massa. Vestibulum cursus odio euismod arcu varius finibus. Vestibulum in diam sit amet ex vehicula pharetra. Morbi sed orci risus. Duis venenatis pellentesque ante id ultricies. Praesent eleifend tempor tristique. Suspendisse tristique gravida metus vel rhoncus.
# **Suspendisse** ut felis gravida, molestie tellus quis, ornare enim. Aliquam bibendum sapien purus, eget posuere diam varius sed. Donec bibendum porta orci, sed scelerisque elit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In augue turpis, tempor sed gravida a, consequat sit amet urna. Vivamus vitae iaculis nibh, in dapibus lacus. Suspendisse interdum tortor enim, in ultrices enim mollis eget. Morbi nisl massa, hendrerit nec velit pretium, vulputate vulputate nunc. Donec vitae tellus et enim sagittis dapibus. Vestibulum consequat semper diam, vitae gravida arcu semper et. Vestibulum id efficitur justo. Suspendisse a suscipit purus. Curabitur turpis quam, vestibulum et posuere eget, gravida sed dui. Sed tellus dolor, dignissim eu odio vitae, gravida facilisis risus. Pellentesque accumsan mi ante, sed finibus ligula accumsan eget. Etiam auctor mauris lectus.""",

TEST_CASES: List[TestCaseData] = [
    {
        "input": "Who is the first president of the united states?",
        "expected_output": "George Washington",
    },
    {
        "input": {"What is the name for this many dollars?": 1000000},
        "expected_output": "The number of dollars in a megadollar",
    },
    {
        "input": {
            "question_type": "who",
            "question": "Who is the second president of the united states?",
        },
        "expected_output": {
            "percieved_mode": "declaratory",
            "answer": "John Adams",
        },
    },
]
items: List[Item] = [Item({"account_id": account_id, "test_case_data": item}) for item in TEST_CASES]

uploaded_test_cases = client.evaluation_datasets.test_cases.batch(
    evaluation_dataset_id=flexible_evaluation_dataset.id,
    items=[{"account_id": account_id, "test_case_data": test_case} for test_case in TEST_CASES],
)
test_case_ids = [test_case.id for test_case in uploaded_test_cases]

# publish the dataset
client.evaluation_datasets.publish(evaluation_dataset_id=flexible_evaluation_dataset.id)

# 3. Create at question set with at least one question. The question set will be used to evaluate the the responses to the test cases.
questions = [
    {
        "account_id": account_id,
        "title": "Test Question",
        "prompt": "Test Prompt",
        "choices": [{"label": "No", "value": 0}, {"label": "Yes", "value": 1}],
    },
    {
        "account_id": account_id,
        "title": "Question only about the document",
        "prompt": "What is the document about?",
    },
]

question_ids: List[str] = []
for question in questions:
    created_question = client.questions.create(
        account_id=str(question["account_id"]),
        type="categorical" if question.get("choices") else "free_text",
        title=str(question["title"]),
        prompt=str(question["prompt"]),
        choices=question.get("choices", []),
    )
    question_ids.append(created_question.id)

# create a question set using the desired questions
question_set = client.question_sets.create(
    account_id=account_id,
    name="US Presidents Question Set",
    question_ids=question_ids,
)

# 4. Create an evaluation config using the question set and a desired evaluation type (human only right now)
evaluation_config = client.evaluation_configs.create(
    account_id=account_id,
    evaluation_type="human",
    question_set_id=question_set.id,
)

# 5. Create an offline application spec and variant if no application spec id and variant id are provided
if not external_application_spec:
    application_spec = client.application_specs.create(
        account_id=account_id,
        description="Test application spec",
        name="test-application-spec" + str(time.time()),
    )
    external_application_spec = application_spec.id

if not external_application_variant:
    application_variant = client.application_variants.create(
        account_id=account_id,
        application_spec_id=external_application_spec,
        name="test offline application variant",
        version="OFFLINE",
        description="Test application variant",
        configuration={},
    )
    external_application_variant = application_variant.id

print("Created external application variant with id: ", external_application_variant)


# 6. Use the ExternalApplication class and a generator function which calls your offline application to generate outputs
def application(prompt: Dict[str, Any], test_case: TestCase) -> ExternalApplicationOutputCompletion:
    response = "application response from external application"  # Call your application with test case input here (test_case.test_case_data.input)
    print("prompt: ", prompt)
    print("test_case: ", test_case)
    print("generated output: ", response)
    metrics = {"accuracy": 0.9}  # whatever metrics you want to track
    trace_spans: List[
        ItemTraceSpan
    ] = [  # whatever traces you want to track, such as what the output of each node inside the application was
        {
            "node_id": "completion",
            "start_timestamp": datetime.now().replace(microsecond=5000),
            "operation_input": {"input": "test input"},
            "operation_output": {"completion_output": "test output"},
            "duration_ms": 1000,
        },
        {
            "node_id": "retrieval",
            "start_timestamp": datetime.now().replace(microsecond=5000),
            "operation_input": {"input": "test input"},
            "operation_output": {"output": "test output"},
            "duration_ms": 1000,
        },
    ]
    return ExternalApplicationOutputCompletion(generation_output=response, metrics=metrics, trace_spans=trace_spans)


external_application = ExternalApplication(client).initialize(
    application_variant_id=external_application_variant,
    application=application,
)

print("Generating test case outputs:")
external_application.generate_outputs(
    evaluation_dataset_id=flexible_evaluation_dataset.id,
    evaluation_dataset_version=1,
)

# 7. Create an annotation config. This helps customize the annotation UI per question.
# - components are a 2D layout of data (row major - can switch to column major with direction: col)
# - max width of a row are 2 items side by side
# - max number of columns are 2 when using the `direction = 'col'` layout
annotation_config_dict: AnnotationConfigParam = {
    "annotation_config_type": "flexible",
    "direction": "row",  # this is by default - try switching to "col"
    "components": [
        [
            {
                "data_loc": ["test_case_data", "input"],
            },
            {
                "data_loc": ["test_case_data", "expected_output"],
            },
        ],
        [
            {
                "data_loc": ["test_case_output", "output"],
            },
        ],
    ],
}

# try clicking on the second question to see the annotation UI change
question_id_to_annotation_config_dict: Dict[str, AnnotationConfigParam] = {
    question_ids[1]: {
        "annotation_config_type": "flexible",  # NOTE: this has to be a flexible annotation config
        "components": [
            [
                {
                    "data_loc": ["test_case_data", "input"],
                },
                {
                    "data_loc": [
                        "trace",
                        "completion",
                        "output",
                        "completion_output",
                    ],  # show a trace span of format ["trace", <node_id>, "output", <key, optionally>]
                },
            ]
        ],
    }
}

# 8. Create an evaluation using the evaluation config, and the desired offline application variant.
# In this case, we are creating a human evaluation using the evaluation config created in step 4.
# Since this is a human evaluation, human annotators will be asked the questions defined in the question set about
# the test case outputs that we batch inserted in step 6. The results will be used to determine the performance of the application
# and generate repord cards and metrics

print("Creating evaluation with flexible evaluation dataset")
evaluation = client.evaluations.create(
    type="builder",
    account_id=account_id,
    application_spec_id=external_application_spec,
    application_variant_id=external_application_variant,
    description="description",
    evaluation_dataset_id=flexible_evaluation_dataset.id,
    annotation_config=annotation_config_dict,
    question_id_to_annotation_config=question_id_to_annotation_config_dict,
    name="Flexible eval",
    evaluation_config_id=evaluation_config.id,
)
