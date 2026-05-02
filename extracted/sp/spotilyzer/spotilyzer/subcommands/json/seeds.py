"""
spotilyzer seed JSON
"""

# system imports
import json

# 3rd party imports
import jsonschema

# schema
SEEDS_KEY = 'seeds'
GROUP_KEY = 'group'
CANDIDATES_KEY = 'candidates'
CANDIDATE_NAME_KEY = 'candidate-name'
INSTANCE_TYPES_KEY = 'instance-types'
_SCHEMA = {
    'type': 'object',
    'properties': {
        SEEDS_KEY: {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    GROUP_KEY: {
                        'type': 'string'
                    },
                    CANDIDATES_KEY: {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                CANDIDATE_NAME_KEY: {
                                    'type': 'string'
                                },
                                INSTANCE_TYPES_KEY: {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string',
                                        'pattern': '^[0-9a-z]+\\.[0-9a-z]+$'
                                    },
                                    'additionalItems': False,
                                    'uniqueItems': True,
                                    'minItems': 1
                                }
                            },
                            'required': [
                                CANDIDATE_NAME_KEY,
                                INSTANCE_TYPES_KEY
                            ],
                            'additionalProperties': False
                        },
                        'additionalItems': False,
                        'uniqueItems': True,
                        'minItems': 1
                    },
                },
                'required': [
                    GROUP_KEY,
                    CANDIDATES_KEY
                ],
                'additionalProperties': False
            },
            'additionalItems': False,
            'uniqueItems': True,
            'minItems': 1
        }
    },
    'required': [
        SEEDS_KEY
    ],
    'additionalProperties': False
}


def load_seeds(fseeds):
    """
    Load seeds JSON file. Perform schema and consistency checks.
    :param fseeds: path to JSON file
    :return: seeds object
    """
    with open(fseeds) as fobj:
        seeds = json.load(fobj)
    jsonschema.validate(seeds, _SCHEMA)
    _validate(seeds, fseeds)
    return seeds


def _validate(seeds, fseeds):
    _seeds = seeds[SEEDS_KEY]
    if len(_seeds) != len(set(s[GROUP_KEY] for s in _seeds)):
        raise SyntaxError(f"group names in {fseeds} are not unique")
    instance_types_set = set()
    num_instance_types = 0
    for seed in _seeds:
        candidates = seed[CANDIDATES_KEY]
        if len(candidates) != len(set(
            c[CANDIDATE_NAME_KEY] for c in candidates
        )):
            raise SyntaxError(f"candidate names for {seed[GROUP_KEY]} are not "
                              f"unique in {fseeds}")
        for candidate in candidates:
            instance_types = candidate[INSTANCE_TYPES_KEY]
            instance_types_set |= set(instance_types)
            num_instance_types += len(instance_types)
            if num_instance_types != len(instance_types_set):
                raise SyntaxError("duplicate instance type found in "
                                  f"{fseeds}: {seed[GROUP_KEY]}/"
                                  f"{candidate[CANDIDATE_NAME_KEY]}")
