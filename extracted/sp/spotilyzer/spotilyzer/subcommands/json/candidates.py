"""
spotilyzer candidates JSON
"""

# system imports
import json

# 3rd party imports
import jsonschema

# project imports
from .seeds import CANDIDATES_KEY, CANDIDATE_NAME_KEY

# schema
REGION_KEY = 'region'
GROUPS_KEY = 'groups'
GROUP_NAME_KEY = 'group-name'
MEM_CORE_RATIO_KEY = 'mem-core-ratio'
PRICE_KEY = 'price'
RESOURCES_KEY = 'resources'
AVG_CORES_KEY = 'avg-cores'
AVG_MEMORY_KEY = 'avg-memory'
MIN_CORES_KEY = 'min-cores'
MIN_MEMORY_KEY = 'min-memory'
CANDIDATE_POOLS_KEY = 'pools'
INSTANCE_TYPE_KEY = 'instance-type'
AVAILABILITY_ZONES_KEY = 'availability-zones'
META_DATA_KEY = 'metadata'
TIMESTAMP_KEY = 'timestamp'
DURATION_KEY = 'duration'
MINPOOL_KEY = 'minpool'

_SCHEMA = {
    'type': 'object',
    'properties': {
        REGION_KEY: {
            'type': 'string'
        },
        GROUPS_KEY: {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    GROUP_NAME_KEY: {
                        'type': 'string'
                    },
                    MEM_CORE_RATIO_KEY: {
                        'type': 'number',
                        'exclusiveMinimum': 0.0
                    },
                    CANDIDATES_KEY: {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                CANDIDATE_NAME_KEY: {
                                    'type': 'string'
                                },
                                PRICE_KEY: {
                                    'type': 'number',
                                    'minimum': 0.0
                                },
                                RESOURCES_KEY: {
                                    'type': 'object',
                                    'properties': {
                                        AVG_CORES_KEY: {
                                            'type': 'number',
                                            'exclusiveMinimum': 0.0
                                        },
                                        AVG_MEMORY_KEY: {
                                            'type': 'number',
                                            'exclusiveMinimum': 0.0
                                        },
                                        MIN_CORES_KEY: {
                                            'type': 'number',
                                            'minimum': 0.0
                                        },
                                        MIN_MEMORY_KEY: {
                                            'type': 'number',
                                            'minimum': 0.0
                                        }
                                    },
                                    'required': [
                                        AVG_CORES_KEY,
                                        AVG_MEMORY_KEY,
                                        MIN_CORES_KEY,
                                        MIN_MEMORY_KEY
                                    ],
                                    'additionalProperties': False
                                },
                                CANDIDATE_POOLS_KEY: {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            INSTANCE_TYPE_KEY: {
                                                'type': 'string'
                                            },
                                            AVAILABILITY_ZONES_KEY: {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'string'
                                                },
                                                'additionalItems': False,
                                                'uniqueItems': True,
                                                'minItems': 1
                                            }
                                        },
                                        'required': [
                                            INSTANCE_TYPE_KEY,
                                            AVAILABILITY_ZONES_KEY
                                        ],
                                        'additionalProperties': False
                                    },
                                    'additionalItems': False,
                                    'uniqueItems': True,
                                    'minItems': 1
                                }
                            },
                            'required': [
                                CANDIDATE_NAME_KEY,
                                PRICE_KEY,
                                RESOURCES_KEY,
                                CANDIDATE_POOLS_KEY
                            ],
                            'additionalProperties': False
                        },
                        'additionalItems': False,
                        'uniqueItems': True,
                        'minItems': 1
                    }
                },
                'required': [
                    GROUP_NAME_KEY,
                    MEM_CORE_RATIO_KEY,
                    CANDIDATES_KEY
                ],
                'additionalProperties': False
            },
            'additionalItems': False,
            'uniqueItems': True,
            'minItems': 1
        },
        META_DATA_KEY: {
            'type': 'object',
            'properties': {
                TIMESTAMP_KEY: {
                    'type': 'string',
                    'format': 'date-time'
                },
                DURATION_KEY: {
                    'type': 'integer',
                    'minimum': 1
                },
                MINPOOL_KEY: {
                    'type': 'integer',
                    'minimum': 1
                }
            },
            'required': [
                TIMESTAMP_KEY,
                DURATION_KEY,
                MINPOOL_KEY
            ],
            'additionalProperties': False
        }
    },
    'required': [
        REGION_KEY,
        GROUPS_KEY,
        META_DATA_KEY
    ],
    'additionalProperties': False
}

# constants
_JSON_INDENT = 2


def save_candidates(fcandidates, candidates):
    """
    Save candidates object to a JSON file. Schema and consistency checks are
    performed before saving.
    :param fcandidates: path to output file
    :param candidates: candidates object
    :return: None
    """
    jsonschema.validate(candidates, _SCHEMA)
    _validate(candidates, fcandidates)
    with open(fcandidates, 'w') as fobj:
        json.dump(candidates, fobj, indent=_JSON_INDENT)


def load_candidates(fcandidates):
    """
    Load candidates JSON file. Perform schema and consistency checks.
    :param fcandidates: path to JSON file
    :return: candidates object
    """
    with open(fcandidates) as fobj:
        candidates = json.load(fobj)
    jsonschema.validate(candidates, _SCHEMA)
    _validate(candidates, fcandidates)
    return candidates


def _validate(candidates, fname):
    groups = candidates[GROUPS_KEY]
    if len(groups) != len(set(g[GROUP_NAME_KEY] for g in groups)):
        raise SyntaxError(f"duplicate group name in {fname}")
    instance_types = set()
    num_instance_types = 0
    for group in groups:
        _candidates = group[CANDIDATES_KEY]
        if len(_candidates) != len(set(c[CANDIDATE_NAME_KEY]
                                       for c in _candidates)):
            raise SyntaxError("duplicate candidate name for group "
                              f"{group[GROUP_NAME_KEY]} in {fname}")
        for candidate in _candidates:
            add_set = set(p[INSTANCE_TYPE_KEY]
                          for p in candidate[CANDIDATE_POOLS_KEY])
            instance_types |= add_set
            num_instance_types += len(add_set)
            if num_instance_types != len(instance_types):
                raise SyntaxError("duplicate instance types for "
                                  f"{group[GROUP_NAME_KEY]}/"
                                  f"{candidate[CANDIDATE_NAME_KEY]} in "
                                  f"{fname}")
