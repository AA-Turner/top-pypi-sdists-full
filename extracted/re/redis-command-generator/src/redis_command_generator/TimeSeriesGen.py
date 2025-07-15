import redis
import sys
import random
import time
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class TimeSeriesGen(BaseGen):
    max_float = sys.maxsize
    labels_dict = {
        "furniture": ["chair", "table", "desk", "mouse", "keyboard", "monitor", "printer", "scanner"],
        "fruits": ["apple", "banana", "orange", "grape", "mango"],
        "animals": ["dog", "cat", "elephant", "lion", "tiger"]
    }
    is_additive ={}
    
    def __post_init__(self):
        # Initialize timestamp in post_init to ensure it's unique per instance
        self.timestamp = int(random.uniform(0, 1000000))
        # Store timestamps per key to ensure consistency across hosts
        self.key_timestamps = {}

        self.is_additive = {
            "tscreate": True,
            "tsadd": True,
            "tsalter": False,
            "tsqueryindex": False,
            "tsmget": False,
            "tsmrange_tsmrevrange": False,
            "tsdel": False,
            "tsdelkey": False
        }

    @cg_method(cmd_type="TSDB-TYPE", can_create_key=True)
    def tscreate(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.ts().create(key)

    @cg_method(cmd_type="TSDB-TYPE", can_create_key=True)
    def tsadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Ensure key_timestamps exists
        if not hasattr(self, 'key_timestamps'):
            self.key_timestamps = {}

        # Pre-generate all timestamps and values
        timestamp = random.randint(0, 1000000)
        value = random.uniform(1, self.max_float)
        
        # Add all values to the time series
        pipe.ts().add(key=key, timestamp=timestamp, value=value, duplicate_policy="last")

    @cg_method(cmd_type="TSDB-TYPE", can_create_key=False)
    def tsalter(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Generate labels and retention
        label1 = random.choice(list(self.labels_dict.keys()))
        label2 = random.choice([l for l in self.labels_dict.keys() if l != label1])
        label3 = random.choice([l for l in self.labels_dict.keys() if l not in [label1, label2]])
        
        label1_value = random.choice(self.labels_dict[label1])
        label2_value = random.choice(self.labels_dict[label2])
        label3_value = random.choice(self.labels_dict[label3])
        
        labels = {label1: label1_value, label2: label2_value, label3: label3_value}
        retention = random.randint(1000, 100000)

        pipe.ts().alter(key, retention_msecs=retention, labels=labels)

    @cg_method(cmd_type="TSDB-TYPE", can_create_key=False)
    def tsqueryindex(self, pipe: redis.client.Pipeline, key: str) -> None:
        filter_expr = self._generate_filter()
        pipe.ts().queryindex(filter_expr)

    @cg_method(cmd_type="TSDB-TYPE", can_create_key=False)
    def tsmget(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Generate filter and other parameters
        filter_expr = self._generate_filter()
        latest = random.choice([True, False])
        withlabels = random.choice([True, False])
        select_labels = [random.choice(list(self.labels_dict.keys()))] if not withlabels else None
        
        pipe.ts().mget(filters=filter_expr, latest=latest, with_labels=withlabels, select_labels=select_labels)

    @cg_method(cmd_type="TSDB-TYPE", can_create_key=False)
    def tsmrange_tsmrevrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Generate parameters
        filter_expr = self._generate_filter()
        from_timestamp = random.randint(0, 500000)
        to_timestamp = random.randint(from_timestamp, 1000000)
        aggregation_type = random.choice(["avg", "sum", "min", "max", None])
        bucket_size_msec = random.randint(1000, 10000) if aggregation_type else None
        count = random.randint(1, 100) if random.choice([True, False]) else None
        with_labels = random.choice([True, False])
        group_by = random.choice(list(self.labels_dict.keys())) if random.choice([True, False]) else None
        latest = random.choice([True, False])
        command = random.choice(["mrange", "mrevrange"])
        
        # Execute the command
        if command == "mrange":
            pipe.ts().mrange(from_time=from_timestamp, to_time=to_timestamp, aggregation_type=aggregation_type,
                         bucket_size_msec=bucket_size_msec, count=count, with_labels=with_labels, filters=filter_expr,
                         groupby=group_by, latest=latest)
        else:
            pipe.ts().mrevrange(from_time=from_timestamp, to_time=to_timestamp, aggregation_type=aggregation_type,
                         bucket_size_msec=bucket_size_msec, count=count, with_labels=with_labels, filters=filter_expr,
                         groupby=group_by, latest=latest)

    @cg_method(cmd_type="TSDB-TYPE", can_create_key=False)
    def tsdel(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.ts().delete(key, 0, int(1e12))

    @cg_method(cmd_type="TSDB-TYPE", can_create_key=False)
    def tsdelkey(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.delete(key)

    def _generate_filter(self):
        filter = []

        # Choosing a filter (label!=, label=value, label=(value1, value2), label=, label!=value, label!=(value1,value2))
        matcher_label = random.choice(list(self.labels_dict.keys()))
        filter.append(f"{matcher_label}={random.choice(self.labels_dict[matcher_label])}")

        filter_label = random.choice([label for label in self.labels_dict.keys() if label != matcher_label])
        value_filter_label_1 = random.choice(self.labels_dict[filter_label])
        value_filter_label_2 = random.choice(
            [value for value in self.labels_dict[filter_label] if value != value_filter_label_1] + [None]
        )
        filter_label2 = random.choice([label for label in self.labels_dict.keys() if label not in {matcher_label, filter_label}])
        value_filter_label2_1= random.choice(self.labels_dict[filter_label2] + [None]) if filter_label2 else None
        equal_filter_2 = random.choice(["=", "!="])

        if value_filter_label_2:
                filter.append(f"{filter_label}=({value_filter_label_1},{value_filter_label_2})")
        else:
                filter.append(f"{filter_label}={value_filter_label_1}")

        if filter_label2:
            if value_filter_label2_1:
                filter.append(f"{filter_label2}{equal_filter_2}{value_filter_label2_1}")
            else:
                filter.append(f"{filter_label2}{equal_filter_2}")

        return filter

if __name__ == "__main__":
    ts_gen = parse(TimeSeriesGen)
    ts_gen.distributions = '{"tscreate":100, "tsadd": 100, "tsdel": 100, "tsalter":100, "tsqueryindex":100, "tsmget":100, "tsmrange_tsmrevrange":100}'
    ts_gen._run()
