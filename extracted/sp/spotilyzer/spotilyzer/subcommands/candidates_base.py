"""
spotilyzer candidates base class
"""

# 3rd party imports
import tabulate

# project imports
from .base import SubCommand
from .json.candidates import REGION_KEY, GROUPS_KEY, GROUP_NAME_KEY, \
    CANDIDATE_NAME_KEY, PRICE_KEY, CANDIDATE_POOLS_KEY, CANDIDATES_KEY, \
    INSTANCE_TYPE_KEY, AVAILABILITY_ZONES_KEY, META_DATA_KEY, TIMESTAMP_KEY, \
    DURATION_KEY, MINPOOL_KEY

# constants
_TABLE_HEADER = ('Candidate', 'Price', 'Instance Type', 'Availability Zones')
_TABLE_FORMAT = 'grid'
_TABLE_FLOAT_FORMAT = '.3f'


class CandidatesBase(SubCommand):
    """
    Candidates base class.
    """

    @staticmethod
    def display_candidates(candidates):
        """
        Display candidates in a summary table.
        :param candidates: candidates output from create-candidates
        :return: None
        """
        print()
        print(f"{REGION_KEY}: {candidates[REGION_KEY]}")
        print(f"{META_DATA_KEY}:")
        print(f"  {TIMESTAMP_KEY}: {candidates[META_DATA_KEY][TIMESTAMP_KEY]}")
        print(f"  {DURATION_KEY}: {candidates[META_DATA_KEY][DURATION_KEY]} "
              "days")
        print(f"  {MINPOOL_KEY}: {candidates[META_DATA_KEY][MINPOOL_KEY]}")
        for group in candidates[GROUPS_KEY]:
            print()
            print(f"group: {group[GROUP_NAME_KEY]}")
            table = [
                [
                    c[CANDIDATE_NAME_KEY],
                    c[PRICE_KEY],
                    '\n'.join(
                        p[INSTANCE_TYPE_KEY] for p in c[CANDIDATE_POOLS_KEY]
                    ),
                    '\n'.join(
                        ','.join(p[AVAILABILITY_ZONES_KEY])
                        for p in c[CANDIDATE_POOLS_KEY]
                    )
                ]
                for c in group[CANDIDATES_KEY]
            ]
            print(tabulate.tabulate(table, headers=_TABLE_HEADER,
                                    tablefmt=_TABLE_FORMAT,
                                    floatfmt=_TABLE_FLOAT_FORMAT))
