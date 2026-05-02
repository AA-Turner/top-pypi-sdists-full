"""
spotilyzer size-fleets subcommand
"""

# system imports
import collections
import math

# 3rd party imports
import tabulate

# project imports
from .base import SubCommand
from .utils.cli import options, posfloat
from .json.candidates import load_candidates, GROUPS_KEY, GROUP_NAME_KEY, \
    CANDIDATES_KEY, CANDIDATE_NAME_KEY, PRICE_KEY, RESOURCES_KEY, \
    MIN_CORES_KEY, MIN_MEMORY_KEY, AVG_CORES_KEY, AVG_MEMORY_KEY, REGION_KEY, \
    META_DATA_KEY, TIMESTAMP_KEY, DURATION_KEY
from .json.requests import load_requests, REPLICAS_KEY, REQUESTS_KEY, \
    CORE_LIMIT_KEY, MEM_LIMIT_KEY

# constants
_DESCRIPTION = "size fleets based on a request"
_BUFFER_OPT = 'buffer'
_BUFFER_DEFAULT = 20
_CANDIDATES_ARG = 'candidates'
_REQUESTS_ARG = 'requests'
_OUTPUT_ARG = 'output'
_TOTAL_CORES_KEY = 'total-cores'
_TOTAL_MEM_KEY = 'total-mem'
_MAX_CORES_KEY = 'max-cores'
_MAX_MEM_KEY = 'max-mem'
_INSTANCE_COUNT = 'instance-count'
_TOTAL_COST = 'total-cost'
_TABLE_HEADER = ('Group', 'Fleet', 'Instance Count', 'Total Cost')
_TABLE_FORMAT = 'grid'
_TABLE_COL_ALIGN = ('left', 'left', 'right', 'right')


class SizeFleets(SubCommand):
    """
    size-fleets subcommand
    """

    name = 'size-fleets'

    @classmethod
    def add_parser(cls, subparsers):
        """
        Add size-fleets subcommand parser.
        :param subparsers: object to attach parser
        :return: None
        """
        parser = subparsers.add_parser(cls.name, description=_DESCRIPTION,
                                       help=_DESCRIPTION)
        parser.add_argument(*options(_BUFFER_OPT), type=posfloat,
                            default=_BUFFER_DEFAULT,
                            help="percentage buffer on request (default is "
                                 f"{_BUFFER_DEFAULT}%%)")
        parser.add_argument(_CANDIDATES_ARG, help="JSON file with candidates")
        parser.add_argument(_REQUESTS_ARG,
                            help="file containing grouped requests")

    def run(self):
        """
        Generate instance count and price estimates from candidates and
        requests.
        :return: None
        """
        groups, candidates = self._get_groups()
        requirements = self._get_requirements()
        results = self._size_fleets(groups, requirements)
        self._display_results(results, candidates)

    def _get_groups(self):
        groups = {}
        candidates = load_candidates(self.getarg(_CANDIDATES_ARG))
        for group in candidates[GROUPS_KEY]:
            fleets = groups[group[GROUP_NAME_KEY]] = {}
            for candidate in group[CANDIDATES_KEY]:
                fleets[candidate[CANDIDATE_NAME_KEY]] = {
                    PRICE_KEY: candidate[PRICE_KEY],
                    RESOURCES_KEY: candidate[RESOURCES_KEY]
                }
        return groups, candidates

    def _get_requirements(self):
        requirements = collections.defaultdict(
            lambda: {
                _TOTAL_CORES_KEY: 0.0,
                _TOTAL_MEM_KEY: 0.0,
                _MAX_CORES_KEY: 0.0,
                _MAX_MEM_KEY:  0.0
            }
        )
        requests = load_requests(self.getarg(_REQUESTS_ARG),
                                 require_group=True)[REQUESTS_KEY]
        for request in requests:
            replicas = request[REPLICAS_KEY]
            cores = request[CORE_LIMIT_KEY]
            mem = request[MEM_LIMIT_KEY]
            requirement = requirements[request[GROUP_NAME_KEY]]
            requirement[_TOTAL_CORES_KEY] += replicas * cores
            requirement[_TOTAL_MEM_KEY] += replicas * mem
            requirement[_MAX_CORES_KEY] = max(cores,
                                              requirement[_MAX_CORES_KEY])
            requirement[_MAX_MEM_KEY] = max(mem, requirement[_MAX_MEM_KEY])
        return requirements

    def _size_fleets(self, groups, requirements):
        results = {}
        buffer = 1 + self.getarg(_BUFFER_OPT) / 100
        for group_name, fleets in groups.items():
            self._set_fleets(results, buffer, requirements, group_name, fleets)
        return results

    @staticmethod
    def _set_fleets(results, buffer, requirements, group_name, fleets):
        group_data = results[group_name] = {}
        requirement = requirements[group_name]
        required_cores = buffer * requirement[_MAX_CORES_KEY]
        required_mem = buffer * requirement[_MAX_MEM_KEY]
        total_cores = buffer * requirement[_TOTAL_CORES_KEY]
        total_mem = buffer * requirement[_TOTAL_MEM_KEY]
        for fleet_name, fleet_data in fleets.items():
            resources = fleet_data[RESOURCES_KEY]
            if required_cores > resources[MIN_CORES_KEY] \
                    or required_mem > resources[MIN_MEMORY_KEY]:
                continue
            count = max(
                math.ceil(total_cores / resources[AVG_CORES_KEY]),
                math.ceil(total_mem / resources[AVG_MEMORY_KEY])
            )
            group_data[fleet_name] = {
                _INSTANCE_COUNT: count,
                _TOTAL_COST: count * fleet_data[PRICE_KEY]
            }

    def _display_results(self, results, candidates):
        sorted_fleets = {
            group_name: sorted(
                fleets.keys(), key=lambda k: fleets[k][_TOTAL_COST]
            )
            for group_name, fleets in results.items()
        }
        print()
        print(f"{REGION_KEY}: {candidates[REGION_KEY]}")
        print(f"{META_DATA_KEY}:")
        print(f"  {TIMESTAMP_KEY}: {candidates[META_DATA_KEY][TIMESTAMP_KEY]}")
        print(f"  {DURATION_KEY}: {candidates[META_DATA_KEY][DURATION_KEY]} "
              "days")
        print(f"  {_BUFFER_OPT}: {self.getarg(_BUFFER_OPT)}%")
        print()
        table = [
            [
                group_name,
                '\n'.join(fleet_names),
                '\n'.join(
                    f"{results[group_name][f][_INSTANCE_COUNT]}"
                    for f in fleet_names
                ),
                '\n'.join(
                    f"{results[group_name][f][_TOTAL_COST]:.3f}"
                    for f in fleet_names
                )
            ]
            for group_name, fleet_names in sorted_fleets.items()
        ]
        print(tabulate.tabulate(table, headers=_TABLE_HEADER,
                                tablefmt=_TABLE_FORMAT,
                                colalign=_TABLE_COL_ALIGN))
