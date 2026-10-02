"""
Extra functions missing from each application - need to understand and set after.
"""

__all__ = ["schemes"]

schemes = {
    "imgt": {
        "state_string": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",  # noqa: E501
        "region_string": "11111111111111111111111111222222222222333333333333333334444444444555555555555555555555555555555555555555666666666666677777777777",  # noqa: E501
        "region_index_dict": {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6},
        "rels": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0},
        "n_regions": 7,
    },
    "chothia_heavy": {
        "state_string": "XXXXXXXXXIXXXXXXXXXXXXXXXXXXXXIIIIXXXXXXXXXXXXXXXXXXXXXXXIXIIXXXXXXXXXXXIXXXXXXXXXXXXXXXXXXIIIXXXXXXXXXXXXXXXXXXIIIXXXXXXXXXXXXX",  # noqa: E501
        "region_string": "11111111112222222222222333333333333333444444444444444455555555555666666666666666666666666666666666666666777777777777788888888888",  # noqa: E501
        "region_index_dict": {
            "1": 0,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "7": 6,
            "8": 7,
        },
        "rels": {0: 0, 1: -1, 2: -1, 3: -5, 4: -5, 5: -8, 6: -12, 7: -15},
        "n_regions": 8,
    },
    "kabat_heavy": {
        "state_string": "XXXXXXXXXIXXXXXXXXXXXXXXXXXXXXIIIIXXXXXXXXXXXXXXXXXXXXXXXIXIIXXXXXXXXXXXIXXXXXXXXXXXXXXXXXXIIIXXXXXXXXXXXXXXXXXXIIIXXXXXXXXXXXXX",  # noqa: E501
        "region_string": "11111111112222222222222333333333333333334444444444444455555555555666666666666666666666666666666666666666777777777777788888888888",  # noqa: E501
        "region_index_dict": {
            "1": 0,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "7": 6,
            "8": 7,
        },
        "rels": {0: 0, 1: -1, 2: -1, 3: -5, 4: -5, 5: -8, 6: -12, 7: -15},
        "n_regions": 8,
    },
    "kabat_light": {
        "state_string": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXIIIIIIXXXXXXXXXXXXXXXXXXXXXXIIIIIIIXXXXXXXXIXXXXXXXIIXXXXXXXXXXXXXXXXXXXXXXXXXXXIIIIXXXXXXXXXXXXXXX",  # noqa: E501
        "region_string": "11111111111111111111111222222222222222223333333333333333444444444445555555555555555555555555555555555555666666666666677777777777",  # noqa: E501
        "region_index_dict": {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6},
        "rels": {
            0: 0,
            1: 0,
            2: -6,
            3: -6,
            4: -13,
            5: -16,
            6: -20,
        },
        "n_regions": 7,
    },
    "chothia_light": {
        "state_string": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXIIIIIIXXXXXXXXXXXXXXXXXXXXXXIIIIIIIXXXXXXXXIXXXXXXXIIXXXXXXXXXXXXXXXXXXXXXXXXXXXIIIIXXXXXXXXXXXXXXX",  # noqa: E501
        "region_string": "11111111111111111111111222222222222222223333333333333333444444444445555555555555555555555555555555555555666666666666677777777777",  # noqa: E501
        "region_index_dict": {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6},
        "rels": {
            0: 0,
            1: 0,
            2: -6,
            3: -6,
            4: -13,
            5: -16,
            6: -20,
        },
        "n_regions": 7,
    },
    "martin_heavy": {
        "state_string": "XXXXXXXXXIXXXXXXXXXXXXXXXXXXXXIIIIXXXXXXXXXXXXXXXXXXXXXXXIXIIXXXXXXXXXXXIXXXXXXXXIIIXXXXXXXXXXXXXXXXXXXXXXXXXXXXIIIXXXXXXXXXXXXX",  # noqa: E501
        "region_string": "11111111112222222222222333333333333333444444444444444455555555555666666666666666666666666666666666666666777777777777788888888888",  # noqa: E501
        "region_index_dict": {
            "1": 0,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "7": 6,
            "8": 7,
        },
        "rels": {0: 0, 1: -1, 2: -1, 3: -5, 4: -5, 5: -8, 6: -12, 7: -15},
        "n_regions": 8,
    },
    # Martin light should be the same as chothia light
    "martin_light": {
        "state_string": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXIIIIIIXXXXXXXXXXXXXXXXXXXXXXIIIIIIIXXXXXXXXIXXXXXXXIIXXXXXXXXXXXXXXXXXXXXXXXXXXXIIIIXXXXXXXXXXXXXXX",  # noqa: E501
        "region_string": "11111111111111111111111222222222222222223333333333333333444444444445555555555555555555555555555555555555666666666666677777777777",  # noqa: E501
        "region_index_dict": {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6},
        "rels": {
            0: 0,
            1: 0,
            2: -6,
            3: -6,
            4: -13,
            5: -16,
            6: -20,
        },
        "n_regions": 7,
    },
    # AHo is very complicated to implement - however the heavy and light should be the
    # same... Code duplication...
    "aho_heavy": {
        "state_string": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",  # noqa: E501
        "region_string": "BBBBBBBBBBCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDEEEEEEEEEEEEEEEFFFFFFFFFFFFFFFFFFFFHHHHHHHHHHHHHHHHIIIIIIIIIIIIIJJJJJJJJJJJJJKKKKKKKKKKK",  # noqa: E501
        "region_index_dict": dict(zip("ABCDEFGHIJK", range(11))),
        "rels": {0: 0, 1: 0, 2: 0, 3: 0, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 21},
        "n_regions": 11,
    },
    "aho_light": {
        "state_string": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",  # noqa: E501
        "region_string": "BBBBBBBBBBCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDEEEEEEEEEEEEEEEFFFFFFFFFFFFFFFFFFFFHHHHHHHHHHHHHHHHIIIIIIIIIIIIIJJJJJJJJJJJJJKKKKKKKKKKK",  # noqa: E501
        "region_index_dict": dict(zip("ABCDEFGHIJK", range(11))),
        "rels": {0: 0, 1: 0, 2: 0, 3: 0, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 21},
        "n_regions": 11,
    },
}
