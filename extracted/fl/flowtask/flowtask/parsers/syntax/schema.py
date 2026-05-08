"""Root task JSON Schema — single source of truth for syntax validation.

Used by:
- ``flowtask.tasks.abstract.AbstractTask.check_syntax`` (runtime).
- ``flowtask.parsers.syntax.checker.SyntaxChecker`` (CLI ``--syntax``).
"""

ROOT_TASK_SCHEMA: dict = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "timezone": {"type": "string"},
        "comments": {"type": "string"},
        "events": {
            "type": "object",
            "properties": {
                "publish": {"type": "boolean"},
            },
            "patternProperties": {
                "^[A-Za-z0-9_]+$": {
                    "anyOf": [
                        {"type": "boolean"},
                        {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": True
                            }
                        }
                    ]
                }
            },
            "additionalProperties": True
        },
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "minProperties": 1,
                "maxProperties": 1,
                "patternProperties": {
                    "^[A-Za-z0-9_]+$": {
                        "type": "object",
                        "additionalProperties": True,
                    }
                }
            }
        }
    },
    "required": ["name", "steps"],
    "additionalProperties": False,
}
