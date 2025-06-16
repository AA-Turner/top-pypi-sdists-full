import asyncio
from functools import wraps
from typing import Any
import os
from mcp.types import CallToolResult, ReadResourceResult

def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(f(*args, **kwargs))

    return wrapper


def expand_env_vars(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: expand_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [expand_env_vars(i) for i in obj]
    elif isinstance(obj, str):
        return os.path.expandvars(obj)
    else:
        return obj
    

def parse_tool_result(result: CallToolResult) -> str:
    tool_result_text = ""
    if result and hasattr(result, 'content') and result.content:
        for content_item in result.content:
            if hasattr(content_item, 'text') and content_item.text: # type: ignore
                tool_result_text += str(content_item.text) + "\n" # type: ignore
            elif isinstance(content_item, str):
                tool_result_text += content_item + "\n"
            elif isinstance(content_item, dict) and "text" in content_item:
                tool_result_text += str(content_item["text"]) + "\n"
            elif hasattr(content_item, '__str__'): # Fallback to string representation
                tool_result_text += str(content_item) + "\n"

    return tool_result_text.strip()

def parse_resource_result(result: ReadResourceResult) -> str:
    resource_result_text = ""
    if result and hasattr(result, 'contents') and result.contents:
        for content_item in result.contents:
            # Assuming TextResourceContents has a 'text' attribute
            if hasattr(content_item, 'text') and content_item.text: # type: ignore
                resource_result_text += str(content_item.text) + "\n" # type: ignore
            # Add handling for BlobResourceContents or other types if necessary
            elif hasattr(content_item, '__str__'): # Fallback to string representation
                 resource_result_text += str(content_item) + "\n"
            # Placeholder for unhandled types
            else:
                resource_result_text += "[Unhandled resource content type]\n"

    return resource_result_text.strip()
