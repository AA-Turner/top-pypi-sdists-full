"""
spotilyzer create-candidates subcommand
"""

# system imports
import collections
import datetime
import heapq
import sys
import textwrap

# project imports
from .candidates_base import CandidatesBase
from .utils.cli import options, posint, csv
from .utils.paths import find_seeds_file
from .utils.stats import quality, StatCollector
from .json.seeds import load_seeds, SEEDS_KEY, GROUP_KEY, CANDIDATES_KEY, \
    CANDIDATE_NAME_KEY, INSTANCE_TYPES_KEY
from .json.candidates import save_candidates, REGION_KEY, GROUPS_KEY, \
    GROUP_NAME_KEY, MEM_CORE_RATIO_KEY, PRICE_KEY, RESOURCES_KEY, \
    AVG_CORES_KEY, AVG_MEMORY_KEY, MIN_CORES_KEY, MIN_MEMORY_KEY, \
    CANDIDATE_POOLS_KEY, INSTANCE_TYPE_KEY, AVAILABILITY_ZONES_KEY, \
    META_DATA_KEY, TIMESTAMP_KEY, DURATION_KEY, MINPOOL_KEY

# constants
_DESCRIPTION = "create candidate spot fleets from seeds"
_REGION_OPT = 'region'
_AVAILABILITY_ZONES_OPT = 'availability-zones'
_DURATION_OPT = 'duration'
_DURATION_DEFAULT = 90
_MINPOOL_OPT = 'minpool'
_MINPOOL_DEFAULT = 20
_SEEDS_OPT = 'seeds'
_CANDIDATES_ARG = 'candidates'
_SPOT_FLEETS_KEY = 'spot-fleets'
_AVG_MEM_CORE_RATIO_KEY = 'avg-mem-core-ratio'
_FLEETS_KEY = 'fleets'
_PRICE_KEY = 'price'
_MIN_STAT_COUNT = 30
_RESOURCES_KEY = 'resources'
_AVG_CORES_KEY = 'avg-cores'
_AVG_MEM_KEY = 'avg-mem'
_MIN_CORES_KEY = 'min-cores'
_MIN_MEM_KEY = 'min-mem'
_COV_LEVEL = 0.20
_MB_PER_GB = 1024
_TABLE_HEADER = ('Candidate', 'Price', 'Instance Type', 'Availability Zones')
_TABLE_FORMAT = 'grid'
_TABLE_FLOAT_FORMAT = '.3f'


class CreateCandidates(CandidatesBase):
    """
    create-candidates subcommand
    """

    name = 'create-candidates'

    @classmethod
    def add_parser(cls, subparsers):
        """
        Add create-candidates subcommand parser.
        :param subparsers: object to attach parser
        :return: None
        """
        parser = subparsers.add_parser(cls.name, description=_DESCRIPTION,
                                       help=_DESCRIPTION)
        parser.add_argument(*options(_REGION_OPT), default=None,
                            help="AWS region to query (default is from "
                                 "configuration or AWS_DEFAULT_REGION)")
        parser.add_argument(*options(_AVAILABILITY_ZONES_OPT), type=csv,
                            default=None,
                            help="comma-separated list of availability zones "
                                 "(defaults are all availability zones in the "
                                 "target region)")
        parser.add_argument(*options(_DURATION_OPT), type=posint,
                            default=_DURATION_DEFAULT,
                            help="number of days in price history (default "
                                 f"{_DURATION_DEFAULT})")
        parser.add_argument(*options(_MINPOOL_OPT), type=posint,
                            default=_MINPOOL_DEFAULT,
                            help="minimum number of pools in spot fleet "
                                 f"(default {_MINPOOL_DEFAULT})")
        parser.add_argument(*options(_SEEDS_OPT), default=None,
                            help="JSON file with seed instance types (if not "
                                 "specified use user's copy or the package "
                                 "data)")
        parser.add_argument(_CANDIDATES_ARG,
                            help="JSON file for candidates output")

    def run(self):
        """
        Create candidates from a seed file and spot price history data.
        :return: None
        """
        self._set_region()
        seeds = self._get_seeds()
        data = self._start(seeds)
        timestamp = self._collect_data(data)
        self._filter_data(data)
        candidates = self._select_candidates(data)
        self._price_candidates(candidates)
        self._get_candidate_resources(candidates)
        results = self._save_candidates(candidates, timestamp)
        self.display_candidates(results)

    def _set_region(self):
        region = self.getarg(_REGION_OPT)
        if region is not None:
            self.reconnect(region)

    def _get_seeds(self):
        seeds_file = self.getarg(_SEEDS_OPT)
        if seeds_file is None:
            seeds_file = find_seeds_file()
        return load_seeds(seeds_file)

    def _start(self, seeds):
        availability_zones = self.getarg(_AVAILABILITY_ZONES_OPT)
        if availability_zones is None:
            availability_zones = self._get_azs()
        else:
            self._validate_azs(availability_zones)
        return self._start_seed_data(seeds, availability_zones)

    def _get_azs(self):
        response = self.client.describe_availability_zones()
        return [a['ZoneName'] for a in response['AvailabilityZones']]

    def _validate_azs(self, availability_zones):
        valid_azs = set(self._get_azs())
        invalid_azs = set(availability_zones) - valid_azs
        if len(invalid_azs) > 0:
            raise ValueError("invalid availability zone(s) for region "
                             f"{self.client.meta.region_name}: "
                             f"{','.join(invalid_azs)}")

    def _start_seed_data(self, seeds, availability_zones):
        data = {}
        del_list = []
        for seed in seeds[SEEDS_KEY]:
            group_data = data[seed[GROUP_KEY]] = {}
            instance_type_map = self._map_instance_type_data(
                group_data,
                seed[CANDIDATES_KEY]
            )
            paginator \
                = self.client.get_paginator('describe_instance_type_offerings')
            for response in paginator.paginate(
                LocationType='availability-zone',
                Filters=[
                    {
                        'Name': 'location',
                        'Values': availability_zones
                    },
                    {
                        'Name': 'instance-type',
                        'Values': list(instance_type_map.keys())
                    }
                ]
            ):
                for offering in response['InstanceTypeOfferings']:
                    instance_type_map[
                        offering['InstanceType']
                    ][
                        offering['Location']
                    ] = StatCollector()
            group_del_list = [
                (c, i)
                for c, g in group_data.items()
                for i, a in g.items()
                if len(a) == 0
            ]
            for del_item in group_del_list:
                del group_data[del_item[0]][del_item[1]]
            del_list.extend(group_del_list)
        if len(del_list) > 0:
            print()
            print(
                textwrap.fill(
                    "[warning]: the following instance types are not "
                    "available in this region: "
                    f"{', '.join(d[1] for d in del_list)}"
                ), '\n'
            )
        return data

    @staticmethod
    def _map_instance_type_data(group_data, candidates):
        instance_type_map = {}
        for candidate in candidates:
            instance_type_data \
                = group_data[candidate[CANDIDATE_NAME_KEY]] = {}
            for instance_type in candidate[INSTANCE_TYPES_KEY]:
                instance_type_map[instance_type] \
                    = instance_type_data[instance_type] = {}
        return instance_type_map

    def _collect_data(self, data):
        print("collecting spot price data...")
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=self.getarg(_DURATION_OPT))
        az_map = collections.defaultdict(dict)
        for group_data in data.values():
            for instance_type_data in group_data.values():
                for instance_type, az_data in instance_type_data.items():
                    for azone, data_rec in az_data.items():
                        az_map[azone][instance_type] = data_rec
        paginator = self.client.get_paginator('describe_spot_price_history')
        for azone, az_map_data in az_map.items():
            for response in paginator.paginate(
                StartTime=start,
                EndTime=end,
                AvailabilityZone=azone,
                InstanceTypes=list(az_map_data.keys()),
                ProductDescriptions=["Linux/UNIX (Amazon VPC)"]
            ):
                for history_rec in response['SpotPriceHistory']:
                    az_map_data[history_rec['InstanceType']].add(
                        float(history_rec['SpotPrice'])
                    )
            print(f"  {azone}: {sum(d.count for d in az_map_data.values())} "
                  "records")
        return end

    def _filter_data(self, data):
        del_list = []
        for group_data in data.values():
            for instance_type_data in group_data.values():
                del_set = set(i
                    for i, ad in instance_type_data.items()
                    if any(d.count < _MIN_STAT_COUNT for d in ad.values())
                )
                for instance_type in del_set:
                    del instance_type_data[instance_type]
                del_list.extend(del_set)
            self._cleanup_dict(group_data)
        self._cleanup_dict(data)
        if len(data) == 0:
            raise RuntimeError("duration too short to collect any "
                               "statistically significant samples")
        if len(del_list) > 0:
            print()
            print(
                textwrap.fill(
                        "[warning]: removed the following instance types "
                        "because of insufficient data: "
                        f"{', '.join(del_list)}"
                ), '\n'
            )

    @staticmethod
    def _cleanup_dict(data_dict):
        del_list = [k for k,v in data_dict.items() if len(v) == 0]
        for key in del_list:
            del data_dict[key]

    def _select_candidates(self, data):
        print("selecting candidates...")
        minpool = self.getarg(_MINPOOL_OPT)
        candidates = {}
        for group, group_data in data.items():
            spot_candidates = {}
            candidates[group] = {
                _SPOT_FLEETS_KEY: spot_candidates,
                _AVG_MEM_CORE_RATIO_KEY: None
            }
            for candidate, instance_type_data in group_data.items():
                fleet_candidates = {}
                spot_candidates[candidate] = {
                    _FLEETS_KEY: fleet_candidates,
                    _RESOURCES_KEY: {},
                    _PRICE_KEY: None
                }
                if sum(len(a) for a in instance_type_data.values()) <= minpool:
                    for instance_type, az_data in instance_type_data.items():
                        fleet_candidates[instance_type] \
                            = self._convert_azdata(az_data)
                    continue
                self._select_nsmallest(fleet_candidates, instance_type_data,
                                       minpool)
        return candidates

    def _select_nsmallest(self, fleet_candidates, instance_type_data, minpool):
        heap = []
        for instance_type, az_data in instance_type_data.items():
            dyn_price = sum(
                sum(i.eval()) for i in az_data.values()
            ) / len(az_data)
            heapq.heappush(heap, (dyn_price, instance_type))
        pool_count = 0
        while pool_count < minpool:
            item = heapq.heappop(heap)
            az_data = instance_type_data[item[1]]
            fleet_candidates[item[1]] = self._convert_azdata(az_data)
            pool_count += len(az_data)

    @staticmethod
    def _convert_azdata(az_data):
        return {az: s.eval()[0] for az, s in az_data.items()}

    @staticmethod
    def _price_candidates(candidates):
        for candidate_record in candidates.values():
            for spot_candidate in candidate_record[_SPOT_FLEETS_KEY].values():
                total = sum(
                    s
                    for p in spot_candidate[_FLEETS_KEY].values()
                    for s in p.values()
                )
                count = sum(
                    len(p) for p in spot_candidate[_FLEETS_KEY].values()
                )
                spot_candidate[_PRICE_KEY] = total / count

    def _get_candidate_resources(self, candidates):
        print("getting candidate resources...")
        paginator = self.client.get_paginator('describe_instance_types')
        for group, candidate_record in candidates.items():
            mcstats = StatCollector()
            for candidate, spot_candidate in candidate_record[
                _SPOT_FLEETS_KEY
            ].items():
                self._compute_resource_stats(paginator, group, candidate,
                                             spot_candidate, mcstats)
            if not quality(mcstats, _COV_LEVEL):
                print(f"[warning]: memory/core ratios for {group} have a "
                      "large variance")
            candidate_record[_AVG_MEM_CORE_RATIO_KEY] = mcstats.eval()[0]

    @staticmethod
    def _compute_resource_stats(paginator, group, candidate, spot_candidate,
                                mcstats):
        cstats = StatCollector()
        mstats = StatCollector()
        core_min = sys.float_info.max
        mem_min = sys.float_info.max
        fleets = spot_candidate[_FLEETS_KEY]
        for response in paginator.paginate(
                InstanceTypes=list(fleets.keys())
        ):
            for instance_type_data in response['InstanceTypes']:
                cores = instance_type_data['VCpuInfo']['DefaultVCpus']
                mem = instance_type_data['MemoryInfo']['SizeInMiB']
                weight = len(
                    fleets[instance_type_data['InstanceType']]
                )
                cstats.weighted_add(cores, weight)
                mstats.weighted_add(mem, weight)
                mcstats.weighted_add(mem / cores, weight)
                core_min = min(cores, core_min)
                mem_min = min(mem, mem_min)
        if not quality(cstats, _COV_LEVEL):
            print(f"[warning]: cores for {group}/{candidate} have a "
                  "large variance")
        if not quality(mstats, _COV_LEVEL):
            print(f"[warning]: memories for {group}/{candidate} have "
                  "a large variance")
        spot_candidate[_RESOURCES_KEY].update(
            {
                _AVG_CORES_KEY: cstats.eval(sampled=False)[0],
                _AVG_MEM_KEY: mstats.eval(sampled=False)[0],
                _MIN_CORES_KEY: core_min,
                _MIN_MEM_KEY: mem_min
            }
        )

    def _save_candidates(self, candidates, timestamp):
        group_list = []
        results = {
            REGION_KEY: self.client.meta.region_name,
            META_DATA_KEY: {
                TIMESTAMP_KEY: timestamp.isoformat(),
                DURATION_KEY: self.getarg(_DURATION_OPT),
                MINPOOL_KEY: self.getarg(_MINPOOL_OPT)
            },
            GROUPS_KEY: group_list
        }
        for spot_fleet, candidate_record in candidates.items():
            candidate_list = []
            group_list.append(
                {
                    GROUP_NAME_KEY: spot_fleet,
                    MEM_CORE_RATIO_KEY: candidate_record[
                        _AVG_MEM_CORE_RATIO_KEY
                    ] / _MB_PER_GB,
                    CANDIDATES_KEY: candidate_list
                }
            )
            for candidate, fleet_candidates in candidate_record[
                _SPOT_FLEETS_KEY
            ].items():
                resources = fleet_candidates[_RESOURCES_KEY]
                pool_list = []
                candidate_list.append(
                    {
                        CANDIDATE_NAME_KEY: candidate,
                        PRICE_KEY: fleet_candidates[_PRICE_KEY],
                        RESOURCES_KEY: {
                            AVG_CORES_KEY: resources[_AVG_CORES_KEY],
                            AVG_MEMORY_KEY: resources[_AVG_MEM_KEY]
                                            / _MB_PER_GB,
                            MIN_CORES_KEY: resources[_MIN_CORES_KEY],
                            MIN_MEMORY_KEY: resources[_MIN_MEM_KEY]
                                            / _MB_PER_GB
                        },
                        CANDIDATE_POOLS_KEY: pool_list
                    }
                )
                for instance_type, instance_type_stats in fleet_candidates[
                    _FLEETS_KEY
                ].items():
                    pool_list.append(
                        {
                            INSTANCE_TYPE_KEY: instance_type,
                            AVAILABILITY_ZONES_KEY: list(
                                instance_type_stats.keys()
                            )
                        }
                    )
        save_candidates(self.getarg(_CANDIDATES_ARG), results)
        return results
