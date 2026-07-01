### application_processing_example_script.py ###
# This script demonstrates how to:
# 1. Create an application spec
# 2. Define node and edges for the application configuration
# 3. Create an application variant with the specified nodes and edges configuration
# 4. Process the application variant with an input
# This is the SDK equivalent of create an application in the Scale GenAI Web Platform:
# https://egp.dashboard.scale.com/applications

import os
import time

from scale_gp import SGPClient
from scale_gp.types.application_edge_param import ApplicationEdgeParam
from scale_gp.types.application_node_param import ApplicationNodeParam
from scale_gp.types.model_template_create_params import (
    VendorConfiguration,
    VendorConfigurationBundleConfig,
    VendorConfigurationEndpointConfig,
)
from scale_gp.types.application_configuration_param import ApplicationConfigurationParam

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
### SETUP END ###

# 1. Create an application spec
application_spec = client.application_specs.create(
    account_id=account_id,
    description="Test application spec",
    name="test-application-spec" + str(time.time()),
)

# 2. Define edge and node parameters to be used the in the application variant graph
# for reference on how to create a model deployment, refer to ./create_model_example_script.py

input_node_id = "input_node"
completion_node_id = "completion_node"
output_node_id = "output_node"

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

# define the nodes. Currently each node requires the following fields:
# id: a unique identifier for the node
# application_node_schema_id: the schema id of the node. This is the type of node that is being created. Current options include:
# - text_input_schema
# - completion_model_schema
# - text_output_schema
# - knowledge_base_schema
# - reranker_schema
# - prompt_engineering_schema
# - external_endpoint_schema
# - document_input_schema
# - map_reduce_schema
# - document_search_schema
# - document_prompt_schema
# configuration: a dictionary of the configuration for the node. The keys and values of the dictionary are dependent on the schema of the node
# for example, the text_input_schema requires a "input-text" field, which is a dictionary with a "type" TEXT and "value" input type fields

# The following nodes are defined in this example:
# 1. input_node: a text input node with the input field "input-text". Each app needs at least one input node which is the entrypoint to the app
# 2. completion_node: a completion model node with the configuration field "completion_model_id" which is the id of the deployed completion model we want to use inside the application
# 3. output_node: a text output node, which defines what processing the application will return. Each app needs at least one output node which is the exitpoint of the app

# overall, we are creating a very basic completion application that takes in a text input, processes it with a completion model, and returns the completion result
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

# 3. create an application variant with the specified nodes and edges configuration
application_variant = client.application_variants.create(
    account_id=account_id,
    application_spec_id=application_spec.id,
    name="test-application-variant",
    version="V0",
    description="Test application variant",
    configuration=configuration,
)

# 4. To interact with the variant, we need to provide an input for each input node in the graph configuration.
# Input nodes are an node with the application_node_schema_id of text_input_schema
# In this case, the input node has id "input_node" and the input field is "input-text"
client.application_variants.process(
    application_variant_id=application_variant.id,
    inputs={"input_node": {"input-text": "Why is the sky blue?"}},
)

# Returns:
# {'output-text': "The sky appears blue due to a phenomenon called Rayleigh scattering", 'session_data': None, 'application_interaction_id': '479b8374-6ca2-40f6-a9ef-be5020e8100e'}
