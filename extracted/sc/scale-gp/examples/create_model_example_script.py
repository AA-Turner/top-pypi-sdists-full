### create_model_example_script.py ###
# This script demonstrates how to deploy and execute a gemini-pro completio model
# 1. Define model template with bundle and endpoint configs
# 2. Create a model instance using the model template
# 3. Create a model deployment using the model instance
# 4. Execute the model deployment to perform a completion
# More information on models can be found at https://egp.dashboard.scale.com/models

import os

from scale_gp import SGPClient
from scale_gp.types.model_template_create_params import (
    VendorConfiguration,
    VendorConfigurationBundleConfig,
    VendorConfigurationEndpointConfig,
)

account_id = os.environ.get("SGP_ACCOUNT_ID", None)
api_key = os.environ.get("SGP_API_KEY", None)

assert (
    account_id is not None
), "You need to set the SGP_ACCOUNT_ID - you can find it at https://egp.dashboard.scale.com/admin/accounts"
assert api_key is not None, "You need to provide your API key - see https://egp.dashboard.scale.com/admin/api-key"

# Create an SGP Client
client = SGPClient(api_key=api_key)

# 1. Define model template
# Before creating a model, you must first create a model template. A model
# template serves 2 purposes. First, it provides common scaffolding that is static
# across multiple models. Second, it exposes several variables that can be
# injected at model creation time to customize the model.
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

# 2. Create a model instance using the model template created above
model_instance = client.models.create(
    account_id=account_id,
    model_type="COMPLETION",
    name="gemini-pro",
    model_vendor="GOOGLE",
    model_template_id=model_template.id,
)

# 3. Create a model deployment using the model instance created above
model_deployment = client.models.deployments.create(
    model_instance_id=model_instance.id, name="Gemini-Pro Deployment", account_id=account_id
)

# 4. Execute the model deployment. In this case, we are executing a completion model with a list of prompts.
execute_result = client.models.deployments.execute(
    model_deployment_id=model_deployment.id,
    model_instance_id=model_instance.id,
    extra_body={"prompts": ["What is the capital of Canada?"]},
)

# Print the result
print(str(execute_result.__dict__["completions"]))
# Returns: [['What is the capital of Canada?', ['The capital of Canada is Ottawa. It is located in the province of Ontario, on the south bank of the Ottawa River. The city has a population of about 1 million people.']]]
