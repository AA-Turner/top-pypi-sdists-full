"""
spotilyzer group-requests subcommand
"""

# system imports
import math

# 3rd party imports
import tabulate

# project imports
from .base import SubCommand
from .utils.cli import options
from .json.candidates import load_candidates, GROUPS_KEY, GROUP_NAME_KEY, \
    MEM_CORE_RATIO_KEY
from .json.requests import load_requests as json_requests, save_requests, \
    REQUESTS_KEY, POD_NAME_KEY, MEM_LIMIT_KEY, CORE_LIMIT_KEY
from .csv.requests import load_requests as csv_requests

# constants
_DESCRIPTION = "place requested pods into node groups"
_FORMAT_OPT = 'format'
_JSON_FMT = 'json'
_CSV_FMT = 'csv'
_FORMAT_DEFAULT = _CSV_FMT
_CANDIDATES_ARG = 'candidates'
_REQUESTS_ARG = 'requests'
_OUTPUT_ARG = 'output'
_TABLE_HEADER = ('Pod', 'Group')


class GroupRequests(SubCommand):
    """
    group-requests subcommand
    """

    name = 'group-requests'

    @classmethod
    def add_parser(cls, subparsers):
        """
        Add group-requests subcommand parser.
        :param subparsers: object to attach parser
        :return: None
        """
        parser = subparsers.add_parser(cls.name, description=_DESCRIPTION,
                                       help=_DESCRIPTION)
        parser.add_argument(*options(_FORMAT_OPT),
                            choices=(_JSON_FMT, _CSV_FMT),
                            default=_FORMAT_DEFAULT,
                            help="request file format (default is "
                                 f"{_FORMAT_DEFAULT})")
        parser.add_argument(_CANDIDATES_ARG, help="JSON file with candidates")
        parser.add_argument(_REQUESTS_ARG, help="file containing requests")
        parser.add_argument(_OUTPUT_ARG,
                            help="output JSON file with grouped requests")

    def run(self):
        """
        Add groups to pod requests.
        :return: None
        """
        groups = load_candidates(self.getarg(_CANDIDATES_ARG))[GROUPS_KEY]
        requests = self._get_requests()
        results = self._group_requests(groups, requests)
        self._save_output(requests)
        self._display_results(results)

    def _get_requests(self):
        request_format = self.getarg(_FORMAT_OPT)
        if request_format == _CSV_FMT:
            return csv_requests(self.getarg(_REQUESTS_ARG))
        if request_format == _JSON_FMT:
            return json_requests(self.getarg(_REQUESTS_ARG))
        raise NotImplementedError(f"format {request_format} not implemented")

    @staticmethod
    def _group_requests(groups, requests):
        results = {}
        group_map = {g[GROUP_NAME_KEY]: g[MEM_CORE_RATIO_KEY] for g in groups}
        group_names = sorted(group_map.keys(),
                             key=lambda k: group_map[k])
        boundaries = [
            math.sqrt(group_map[group_names[i]] * group_map[group_names[i - 1]])
            for i in range(1, len(group_names))
        ]
        num_bdy = len(boundaries)
        for request in requests[REQUESTS_KEY]:
            mem_core_ratio = request[MEM_LIMIT_KEY] / request[CORE_LIMIT_KEY]
            found = False
            for i in range(num_bdy):
                if mem_core_ratio < boundaries[i]:
                    request[GROUP_NAME_KEY] = results[request[POD_NAME_KEY]] \
                        = group_names[i]
                    found = True
                    break
            if not found:
                request[GROUP_NAME_KEY] = results[request[POD_NAME_KEY]] \
                    = group_names[-1]
        return results

    def _save_output(self, requests):
        save_requests(self.getarg(_OUTPUT_ARG), requests)

    @staticmethod
    def _display_results(results):
        print()
        table = [[p, g] for p, g in results.items()]
        print(tabulate.tabulate(table, headers=_TABLE_HEADER))
