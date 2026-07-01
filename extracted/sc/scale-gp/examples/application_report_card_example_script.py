### application_report_card_example_script.py ###
# This script demonstrates how to create an application report card for an application variant
# A report card will provide a summary of the performance of the application variant against an evaluation dataset
# Three main scores will be produced: Accuracy, Quality and Trust & Safety.
# The performance in each category will contribute to an overall Scale Confidence Score for the variant.


# You can view generated report cards in the UI at:
# https://egp.dashboard.scale.com/applications/<application_spec_id>/<application_variant_id>/report-card/overview

import os
import time
from typing import List

from scale_gp import SGPClient
from scale_gp.types.application_edge_param import ApplicationEdgeParam
from scale_gp.types.application_node_param import ApplicationNodeParam
from scale_gp.types.model_template_create_params import (
    VendorConfiguration,
    VendorConfigurationBundleConfig,
    VendorConfigurationEndpointConfig,
)
from scale_gp.types.application_configuration_param import ApplicationConfigurationParam
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

### SETUP ###
bundle_config = VendorConfigurationBundleConfig(image="gemini-pro", registry="aws-registry", tag="latest")
endpoint_config = VendorConfigurationEndpointConfig(
    max_workers=3,
)

vendor_configuration = VendorConfiguration(
    bundle_config=bundle_config,
    endpoint_config=endpoint_config,
)
model_template = client.model_templates.create(
    account_id=account_id,
    endpoint_type="SYNC",
    model_type="COMPLETION",
    name="Gemini-Pro Template",
    vendor_configuration=vendor_configuration,
)

model_instance = client.models.create(
    account_id=account_id,
    model_type="COMPLETION",
    name="gemini-pro",
    model_vendor="GOOGLE",
    model_template_id=model_template.id,
)
model_deployment = client.models.deployments.create(
    model_instance_id=model_instance.id, name="Gemini-Pro Deployment", account_id=account_id
)

input_node_id = "input_node"
completion_node_id = "completion_node"
output_node_id = "output_node"
application_spec = client.application_specs.create(
    account_id=account_id,
    description="Test application spec",
    name="test-application-spec" + str(time.time()),
)
edges = [
    ApplicationEdgeParam(
        from_node=input_node_id,
        to_node=completion_node_id,
        from_field="input-text",
        to_field="prompt",
    ),
    ApplicationEdgeParam(
        from_node=completion_node_id,
        to_node=output_node_id,
        from_field="completion",
        to_field="output-text",
    ),
]

nodes = [
    ApplicationNodeParam(
        id=input_node_id,
        application_node_schema_id="text_input_schema",
        configuration={"input-text": {"value": "Completion prompt"}},
    ),
    ApplicationNodeParam(
        id=completion_node_id,
        application_node_schema_id="completion_model_schema",
        configuration={
            "completion_model_id": {
                "value": model_deployment.id,  # define the deployed completion model we want to use inside the application
            }
        },
    ),
    ApplicationNodeParam(
        id=output_node_id,
        application_node_schema_id="text_output_schema",
        configuration={"completion": {"value": "completion result"}},
    ),
]
configuration = ApplicationConfigurationParam(edges=edges, nodes=nodes)
application_variant = client.application_variants.create(
    account_id=account_id,
    application_spec_id=application_spec.id,
    name="test-application-variant",
    version="V0",
    description="Test application variant",
    configuration=configuration,
)

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

evaluation_dataset = client.evaluation_datasets.create(
    account_id=account_id,
    name="evaluation_dataset",
    schema_type="GENERATION",
    type="manual",
)
items: List[Item] = [Item({"account_id": account_id, "test_case_data": item}) for item in DATASET]
uploaded_test_cases = client.evaluation_datasets.test_cases.batch(
    evaluation_dataset_id=evaluation_dataset.id,
    items=[{"account_id": account_id, "test_case_data": item} for item in DATASET],
)

manual_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.create(
    evaluation_dataset_id=evaluation_dataset.id
)

published_dataset_response = client.evaluation_datasets.publish(
    evaluation_dataset_id=evaluation_dataset.id,
)
### SETUP END ###

# create an application variant report
application_variant_report_create_response = client.application_variant_reports.create(
    application_variant_id=application_variant.id,
    evaluation_dataset_ids=[evaluation_dataset.id],
    account_id=account_id,
)

# retrieve the application variant report, will still be PENDING if immediately retrieved
while True:
    application_variant_report = client.application_variant_reports.retrieve(
        application_variant_report_id=application_variant_report_create_response.id,
        view=["AsyncJobs"],
    )
    if (
        application_variant_report
        and application_variant_report.async_jobs
        and application_variant_report.async_jobs[0].status != "Completed"
    ):
        print("Creating application variant report... this might take a while")
        time.sleep(20)
    else:
        break

print("Generated application variant report:")
print(application_variant_report)
