from langchain_core.tools import StructuredTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
import json
import os
import requests

"""
Converts a list of langchain tool objects into a JSON string.

:param tools: List of tool objects to be serialized.
:return: JSON string representation of the tools.
"""
def create_tools_json(tools):
    tools_json = []
    for tool in tools:
        schema = tool.args_schema

        if hasattr(schema, "model_json_schema"):
            args_schema = schema.model_json_schema()
        elif isinstance(schema, dict):
            args_schema = schema
        else:
            raise TypeError(f"Unsupported args_schema type: {type(schema)}")

        tool_info = {
            "name": tool.name,
            "description": tool.description,
            "args_schema": args_schema
        }
        tools_json.append(tool_info)

    return tools_json




"""
Converts JSON formatted langchain tool into structured tool objects.
@param json_tools: A list or single JSON object representing tools.
@return: A list of StructuredTool objects or a single StructuredTool if only one is provided.
"""
def json_to_structured_tools(json_tools):
    if not isinstance(json_tools, list):
        json_tools = [json_tools]
    
    structured_tools = []
    for tool_json in json_tools:
            
        structured_tool = StructuredTool(
            name=tool_json['name'],
            description=tool_json['description'],
            func=None,
            args_schema=tool_json['args_schema']
        )
        structured_tools.append(structured_tool)
    
    return structured_tools if len(structured_tools) > 1 else structured_tools[0]



def call_model(llm, provider, messages, tools=None, params={}):
    """
    Calls an external LLM API via AWS API Gateway.

    Parameters:
    - llm (str): The model name to call.
    - provider (str): The LLM provider (e.g., OpenAI, Anthropic).
    - messages (list): Conversation history in message format.
    - tools (list, optional): List of tool definitions for the LLM to use.
    - params (dict, optional): Additional parameters for the LLM call (e.g., temperature, max tokens).

    Returns:
    - AIMessage object: The response from the LLM API.
    """
    # Prepare the payload for the API request
    data = {
        "provider": provider,
        "model_name": llm,
        "params": params,
        "messages": [msg.model_dump() for msg in messages],
        "tools": tools
    }

    # Fetch API Gateway credentials from environment variables
    api_key = os.environ.get('API_GW_KEY')
    api_url = os.environ.get('API_GW_URL')

    if not api_key or not api_url:
        raise ValueError("Missing API Gateway key or URL. Ensure API_GW_KEY and API_GW_URL are set.")

    # Set the request headers
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    try:
        # Send a POST request to the API Gateway
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        ai_message = AIMessage(**response.json())
        return ai_message
    except requests.RequestException as e:
        raise RuntimeError(f"Error while calling LLM API: {e}")
    

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
    return ChatPromptTemplate.from_messages(messages)
