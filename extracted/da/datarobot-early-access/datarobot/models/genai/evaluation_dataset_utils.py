#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

import json
from typing import Any, Dict, List, Union


class ReferenceToolCall:
    """Reference tool call for an evaluation dataset.  This is a convenience stand in
    for the Ragas ToolCall class."""

    def __init__(self, name: str, args: Dict[str, Any]):
        self.name = name
        self.args = args

    def dict(self) -> Dict[str, Union[str, Dict[str, Any]]]:
        return {
            "name": self.name,
            "args": self.args,
        }

    def json(self) -> str:
        """Convert the tool call to a JSON string."""
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "ReferenceToolCall":
        """Create a ReferenceToolCall object from a JSON string."""
        data = json.loads(json_str)
        return cls(name=data["name"], args=data["args"])


class ReferenceToolCalls:
    """Utility for creating a list of reference tool calls for an evaluation dataset. This
    class represents a list of tool calls for a single row in the evaluation dataset.

    Example usage:
    >>> df = pandas.DataFrame()
    >>> tool_calls_1 = ReferenceToolCalls([
    >>>     ReferenceToolCall(name="get_weather", args={"location": "New York"}),
    >>>     ReferenceToolCall(name="get_news", args={"topic": "technology"})
    >>> ])
    >>> tool_calls_2 = ReferenceToolCalls([
    >>>     ReferenceToolCall(name="get_weather", args={"location": "Los Angeles"}),
    >>>     ReferenceToolCall(name="get_news", args={"topic": "sports"})
    >>> ])
    >>> df['prompts'] = ['what is the weather for the tech conference in NYC?',
    >>> 'what is the weather in LA?, and will it affect the game?']
    >>> df['reference_tool_calls'] = [tool_calls_1.json(), tool_calls_2.json()]
    """

    def __init__(self, tool_calls: List[ReferenceToolCall]):
        self.tool_calls = tool_calls

    def json(self) -> str:
        return json.dumps([tool_call.dict() for tool_call in self.tool_calls])

    @classmethod
    def from_json(cls, json_str: str) -> "ReferenceToolCalls":
        """Create a ReferenceToolCalls object from a JSON string."""
        data = json.loads(json_str)
        tool_calls = [ReferenceToolCall(name=item["name"], args=item["args"]) for item in data]
        return cls(tool_calls)
