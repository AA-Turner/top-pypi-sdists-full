"""
spotilyzer requests JSON
"""

# system imports
import json

# 3rd party imports
import jsonschema

# project imports
from .candidates import GROUP_NAME_KEY

# schema
REQUESTS_KEY = 'requests'
POD_NAME_KEY = 'pod-name'
REPLICAS_KEY = 'replicas'
CORE_LIMIT_KEY = 'core-limit'
MEM_LIMIT_KEY = 'mem-limit'
_SCHEMA = {
    'type': 'object',
    'properties': {
        REQUESTS_KEY: {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    POD_NAME_KEY: {
                        'type': 'string'
                    },
                    GROUP_NAME_KEY: {
                        'type': 'string'
                    },
                    REPLICAS_KEY: {
                        'type': 'integer',
                        'minimum': 1
                    },
                    CORE_LIMIT_KEY: {
                        'type': 'number',
                        'exclusiveMinimum': 0.0
                    },
                    MEM_LIMIT_KEY: {
                        'type': 'number',
                        'exclusiveMinimum': 0.0
                    }
                },
                'required': [
                    POD_NAME_KEY,
                    REPLICAS_KEY,
                    CORE_LIMIT_KEY,
                    MEM_LIMIT_KEY
                ],
                'additionalProperties': False
            },
            'additionalItems': False,
            'uniqueItems': True,
            'minItems': 1
        }
    },
    'required': [
        REQUESTS_KEY
    ],
    'additionalProperties': False
}

# constants
_JSON_INDENT = 2


def load_requests(frequests, require_group=False):
    """
    Load requests JSON file. Schema and consistency checks are performed.
    :param frequests: path to JSON file
    :param require_group: flag to require group key in JSON document
    :return: requests object
    """
    with open(frequests) as fobj:
        requests = json.load(fobj)
    jsonschema.validate(requests, _SCHEMA)
    _validate(requests, frequests, require_group)
    return requests


def save_requests(frequests, requests):
    """
    Save a requests object to a JSON file. Schema and consistency checks are
    performed before saving.
    :param frequests: path to output JSON file
    :param requests: requests object
    :return: None
    """
    jsonschema.validate(requests, _SCHEMA)
    _validate(requests, frequests, True)
    with open(frequests, 'w') as fobj:
        json.dump(requests, fobj, indent=_JSON_INDENT)


def _validate(requests, frequests, require_group):
    _requests = requests[REQUESTS_KEY]
    if len(_requests) != len(set(r[POD_NAME_KEY] for r in _requests)):
        raise SyntaxError(f"duplicate pod name in {frequests}")
    if require_group and any(GROUP_NAME_KEY not in r for r in _requests):
        raise SyntaxError(f"{GROUP_NAME_KEY} missing in request record")
