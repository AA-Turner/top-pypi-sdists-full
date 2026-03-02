from langgraph_utils import create_tools_json, json_to_structured_tools, call_model
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_core.messages import utils

# @! create simple tool to add two numbers and genberate random hash from passed string 

import hashlib
import random

from langchain_core.tools import tool

def messages_to_chatprompt(message_dicts):
    """
    Convert a list of message dictionaries to a ChatPromptValue object.

    Args:
        message_dicts (list): List of dictionaries with 'type' and 'content'.

    Returns:
        ChatPromptValue: A ChatPromptValue object containing the messages.
    """
    message_map = {
        'human': HumanMessage,
        'ai': AIMessage,
        'tool': ToolMessage,
        'system': SystemMessage
    }

    messages = []

    for msg in message_dicts:
        msg_type = msg.get('type')
        content = msg.get('content')

        if msg_type not in message_map:
            raise ValueError(f"Invalid message type: {msg_type}")

        # Create corresponding message object
        message_class = message_map[msg_type]
        messages.append(message_class(**msg))

    # Convert to ChatPromptValue
    return ChatPromptValue(messages=messages)

@tool
def add_numbers(num1, num2):
    """
    This function adds two numbers.

    Parameters:
    num1 (int): The first number to add.
    num2 (int): The second number to add.

    Returns:
    The sum of num1 and num2.
    """
    return num1 + num2

@tool
def generate_hash(input_string):
    """
    This function generates a unique hash for a given input string.

    Parameters:
    input_string (str): The string for which the hash is to be generated.

    Returns:
    str: The generated hash of the input string.
    """
    random.seed(input_string)
    return hashlib.sha256(str(random.random()).encode()).hexdigest()

tools = [add_numbers, generate_hash]
json_tools = create_tools_json(tools)
import json
tools_from_json = json_to_structured_tools(json_tools)
messages = [HumanMessage("whats 23 plus 74")]

response = call_model("gpt-4o", "openai", tools=json_tools, messages=messages)
from langchain_core.prompt_values import ChatPromptValue

#chat_prompt = ChatPromptTemplate.from_messages([AIMessage(**response)])

tm = [ToolMessage(content='nyc, sf', name='get_coolest_cities', tool_call_id='tool_call_id_1').model_dump(), HumanMessage("whats 2 plus 3").model_dump()]
print(tm)
print(messages_to_chatprompt(tm))
