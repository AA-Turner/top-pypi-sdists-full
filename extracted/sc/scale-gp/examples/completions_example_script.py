### completions_example_script.py ###
# This script demonstrates how to create a completion using the Scale GP API client
# 1. How to call a specified model for a completion
# 2. How to call a specified model for a chat completion, allowing for message history

import os

from scale_gp import SGPClient
from scale_gp.types.completion_create_params import ModelParameters
from scale_gp.types.chat_completion_create_params import (
    ModelParameters as ChatModelParameters,
    MessageUserMessage,
)

account_id = os.environ.get("SGP_ACCOUNT_ID", None)
api_key = os.environ.get("SGP_API_KEY", None)

assert (
    account_id is not None
), "You need to set the SGP_ACCOUNT_ID - you can find it at https://egp.dashboard.scale.com/admin/accounts"
assert api_key is not None, "You need to provide your API key - see https://egp.dashboard.scale.com/admin/api-key"

# Create an SGP Client
client = SGPClient(api_key=api_key)

model_parameters = ModelParameters(max_tokens=200, temperature=0.5, top_k=1, top_p=1)

# 1. call a specified model to perform a completion using a prompt and the parameters defined above
completion = client.completions.create(
    model="gpt-4",
    prompt="Why is the sky blue?",
    account_id=account_id,
    model_parameters=model_parameters,
)

print(completion.completion.text)
# Returns: The sky appears blue because of a process called Rayleigh scattering. As sunlight reaches Earth's atmosphere, it is scattered, or redirected, in every direction by the gases and particles in the air. Blue light is scattered more than other colors because it travels in shorter, smaller waves. This scattered blue light is what we see when we look up at the sky.

# 2. call a chat model to perform a completion using a message and the parameters defined above. Chat completion allows for a series of messages to be sent to the model,
# serving as a conversation between the user and the model
chat_model_parameters = ChatModelParameters(max_tokens=200, temperature=0.5, top_k=1, top_p=1)
message = MessageUserMessage(role="user", content="What is the capital of Canada?")

chat_completion = client.chat_completions.create(
    model="gpt-4",
    messages=[
        message
    ],  # messages is a list of historical messages in the conversation, with roles usually alternating between user, assistant and system
    account_id=account_id,
    model_parameters=model_parameters,
    instructions="Answer the question like an elementary school teacher.",
)

print(chat_completion.chat_completion.message.content)
# Returns: The capital of Canada is Ottawa. Ottawa is a beautiful city located in the eastern part of the country, in the province of Ontario. It's where the Prime Minister lives and where many important decisions for the country are made!
