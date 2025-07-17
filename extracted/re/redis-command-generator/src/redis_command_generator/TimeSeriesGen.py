import redis
import sys
import random
import time
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

KEY_TYPE = "TSDB-TYPE"
@dataclass
class TimeSeriesGen(BaseGen):
    max_float = sys.maxsize
    labels_dict = {
        "furniture": ["chair", "table", "desk", "mouse", "keyboard", "monitor", "printer", "scanner"],
        "fruits": ["apple", "banana", "orange", "grape", "mango"],
        "animals": ["dog", "cat", "elephant", "lion", "tiger"]
    }
    
    def __post_init__(self):
        # Initialize timestamp in post_init to ensure it's unique per instance
        self.timestamp = int(random.uniform(0, 1000000))
        # Store timestamps per key to ensure consistency across hosts
        self.key_timestamps = {}
        # Store created time series keys for compaction rules
        self.created_keys = set()

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def tscreate(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Enhanced TS.CREATE with more optional parameters
        retention = random.randint(60000, 3600000) if random.choice([True, False]) else None
        chunk_size = random.choice([1024, 2048, 4096, 8192]) if random.choice([True, False]) else None
        duplicate_policy = random.choice(["BLOCK", "FIRST", "LAST", "MIN", "MAX", "SUM"]) if random.choice([True, False]) else None
        ignore_max_val_diff = random.randint(0, 1000) if random.choice([True, False]) and duplicate_policy == "LAST" else None
        ignore_max_time_diff = random.randint(0, 1000) if ignore_max_val_diff is not None else None
        
        # Generate labels
        labels = {}
        if random.choice([True, False]):
            num_labels = random.randint(1, 3)
            for _ in range(num_labels):
                label_key = random.choice(list(self.labels_dict.keys()))
                label_value = random.choice(self.labels_dict[label_key])
                labels[label_key] = label_value
        
        # Track created keys for compaction rules
        if not hasattr(self, 'created_keys'):
            self.created_keys = set()
        self.created_keys.add(key)
        
        pipe.ts().create(
            key=key,
            retention_msecs=retention,
            chunk_size=chunk_size,
            duplicate_policy=duplicate_policy,
            labels=labels if labels else None,
            ignore_max_val_diff=ignore_max_val_diff,
            ignore_max_time_diff=ignore_max_time_diff
        )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def tsadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Enhanced TS.ADD with more optional parameters
        if not hasattr(self, 'key_timestamps'):
            self.key_timestamps = {}

        timestamp = random.randint(0, 1000000)
        value = random.uniform(1, self.max_float)
        
        # Optional parameters for TS.ADD
        retention = random.randint(60000, 3600000) if random.choice([True, False]) else None
        chunk_size = random.choice([1024, 2048, 4096, 8192]) if random.choice([True, False]) else None
        duplicate_policy = random.choice(["BLOCK", "FIRST", "LAST", "MIN", "MAX", "SUM"]) if random.choice([True, False]) else None
        on_duplicate = random.choice(["BLOCK", "FIRST", "LAST", "MIN", "MAX", "SUM"]) if random.choice([True, False]) else None
        ignore_max_val_diff = random.randint(0, 1000) if random.choice([True, False]) and duplicate_policy == "LAST" else None
        ignore_max_time_diff = random.randint(0, 1000) if ignore_max_val_diff is not None else None
        
        # Generate labels for new time series
        labels = {}
        if random.choice([True, False]):
            num_labels = random.randint(1, 3)
            for i in range(num_labels):
                label_key = random.choice(list(self.labels_dict.keys()))
                label_value = random.choice(self.labels_dict[label_key])
                labels[label_key] = label_value

        pipe.ts().add(
            key=key,
            timestamp=timestamp,
            value=value,
            retention_msecs=retention,
            chunk_size=chunk_size,
            duplicate_policy=duplicate_policy,
            on_duplicate=on_duplicate,
            labels=labels if labels else None,
            ignore_max_val_diff=ignore_max_val_diff,
            ignore_max_time_diff=ignore_max_time_diff
        )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsget(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Get the last sample from a time series"""
        latest = random.choice([True, False])
        pipe.ts().get(key, latest=latest)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsincrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Increment a value in a time series"""
        redis_obj = self._pipe_to_redis(pipe)
        latest_ts = redis_obj.ts().get(key, latest=True)
        value = random.uniform(latest_ts[0], latest_ts[0] + 100) if latest_ts else random.uniform(1, 1000)

        # Optional parameters
        timestamp = random.randint(latest_ts[0], latest_ts[0] + 1000000) if random.choice([True, False]) and latest_ts  else None
        retention = random.randint(60000, 3600000) if random.choice([True, False]) else None
        chunk_size = random.choice([1024, 2048, 4096, 8192]) if random.choice([True, False]) else None
        duplicate_policy = random.choice(["BLOCK", "FIRST", "LAST", "MIN", "MAX", "SUM"]) if random.choice([True, False]) else None
        ignore_max_val_diff = random.randint(0, 1000) if random.choice([True, False]) and duplicate_policy == "LAST" else None
        ignore_max_time_diff = random.randint(0, 1000) if ignore_max_val_diff is not None else None
        
        # Generate labels for new time series
        labels = {}
        if random.choice([True, False]):
            num_labels = random.randint(1, 3)
            for i in range(num_labels):
                label_key = random.choice(list(self.labels_dict.keys()))
                label_value = random.choice(self.labels_dict[label_key])
                labels[label_key] = label_value

        pipe.ts().incrby(
            key=key,
            value=value,
            timestamp=timestamp,
            retention_msecs=retention,
            chunk_size=chunk_size,
            duplicate_policy=duplicate_policy,
            labels=labels if labels else None,
            ignore_max_val_diff=ignore_max_val_diff,
            ignore_max_time_diff=ignore_max_time_diff
        )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def tsdecrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Decrement a value in a time series"""
        value = random.uniform(1, 100)
        timestamp = random.randint(0, 1000000) if random.choice([True, False]) else "*"
        
        # Optional parameters
        retention = random.randint(60000, 3600000) if random.choice([True, False]) else None
        chunk_size = random.choice([1024, 2048, 4096, 8192]) if random.choice([True, False]) else None
        duplicate_policy = random.choice(["BLOCK", "FIRST", "LAST", "MIN", "MAX", "SUM"]) if random.choice([True, False]) else None
        ignore_max_val_diff = random.randint(0, 1000) if random.choice([True, False]) and duplicate_policy == "LAST" else None
        ignore_max_time_diff = random.randint(0, 1000) if ignore_max_val_diff is not None else None
        
        # Generate labels for new time series
        labels = {}
        if random.choice([True, False]):
            num_labels = random.randint(1, 3)
            for i in range(num_labels):
                label_key = random.choice(list(self.labels_dict.keys()))
                label_value = random.choice(self.labels_dict[label_key])
                labels[label_key] = label_value

        pipe.ts().decrby(
            key=key,
            value=value,
            timestamp=timestamp,
            retention_msecs=retention,
            chunk_size=chunk_size,
            duplicate_policy=duplicate_policy,
            labels=labels if labels else None,
            ignore_max_val_diff=ignore_max_val_diff,
            ignore_max_time_diff=ignore_max_time_diff
        )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Query a range in forward direction"""
        from_timestamp = random.randint(0, 500000)
        to_timestamp = random.randint(from_timestamp, 1000000)
        
        # Optional aggregation
        aggregation_type = random.choice(["avg", "sum", "min", "max", "range", "count", "first", "last", "std.p", "std.s", "var.p", "var.s", "twa", None])
        bucket_size_msec = random.randint(1000, 10000) if aggregation_type else None
        count = random.randint(1, 100) if random.choice([True, False]) else None
        align = random.choice(["+", "-", "start", "end"]) if aggregation_type and random.choice([True, False]) else None
        empty = random.choice([True, False])
        latest = random.choice([True, False])
        filter_by_min_value = random.choice([random.randint(0, 1000), None])
        filter_by_max_value = random.randint(filter_by_min_value, filter_by_min_value * 10) if filter_by_min_value else None
        filter_by_ts = [random.randint(0, 1000000)] * 10  if random.choice([True, False]) else None
        
        pipe.ts().range(
            key=key,
            from_time=from_timestamp,
            to_time=to_timestamp,
            count=count,
            aggregation_type=aggregation_type,
            bucket_size_msec=bucket_size_msec,
            align=align,
            empty=empty,
            latest=latest,
            filter_by_min_value=filter_by_min_value,
            filter_by_max_value=filter_by_max_value,
            filter_by_ts=filter_by_ts
        )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsrevrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Query a range in reverse direction"""
        from_timestamp = random.randint(0, 500000)
        to_timestamp = random.randint(from_timestamp, 1000000)
        
        # Optional aggregation
        aggregation_type = random.choice(["avg", "sum", "min", "max", "range", "count", "first", "last", "std.p", "std.s", "var.p", "var.s", "twa", None])
        bucket_size_msec = random.randint(1000, 10000) if aggregation_type else None
        count = random.randint(1, 100) if random.choice([True, False]) else None
        align = random.choice(["+", "-", "start", "end"]) if aggregation_type and random.choice([True, False]) else None
        empty = random.choice([True, False])
        latest = random.choice([True, False])
        filter_by_min_value = random.choice([random.randint(0, 1000), None])
        filter_by_max_value = random.randint(filter_by_min_value, filter_by_min_value * 10) if filter_by_min_value else None
        filter_by_ts = [random.randint(0, 1000000)] * 10  if random.choice([True, False]) else None
        
        pipe.ts().revrange(
            key=key,
            from_time=from_timestamp,
            to_time=to_timestamp,
            count=count,
            aggregation_type=aggregation_type,
            bucket_size_msec=bucket_size_msec,
            align=align,
            empty=empty,
            latest=latest,
            filter_by_min_value=filter_by_min_value,
            filter_by_max_value=filter_by_max_value,
            filter_by_ts=filter_by_ts
        )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsinfo(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Get information about a time series"""
        pipe.ts().info(key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def tsmadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Add multiple samples to multiple time series"""
        samples = []
        
        # Generate 2-5 samples for different keys
        num_samples = random.randint(2, 5)
        for i in range(num_samples):
            sample_key = f"{key}_{i}" if i > 0 else key
            timestamp = random.randint(0, 1000000)
            value = random.uniform(1, self.max_float)
            samples.append((sample_key, timestamp, value))
        
        pipe.ts().madd(samples)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tscreaterule(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Create a compaction rule"""
        if not hasattr(self, 'created_keys'):
            self.created_keys = set()
        
        # Only create rules if we have multiple keys available
        if len(self.created_keys) < 2:
            # If not enough keys, create a destination key first
            dest_key = f"{key}_compacted"
            self.created_keys.add(dest_key)
            pipe.ts().create(dest_key)
        else:
            dest_key = random.choice(list(self.created_keys - {key})) if key in self.created_keys else f"{key}_compacted"
        
        # Aggregation parameters
        aggregator = random.choice(["avg", "sum", "min", "max", "range", "count", "first", "last", "std.p", "std.s", "var.p", "var.s", "twa"])
        bucket_duration = random.choice([60000, 300000, 3600000, 86400000])  # 1min, 5min, 1hour, 1day
        align_timestamp = random.randint(0, bucket_duration) if random.choice([True, False]) else None
        
        pipe.ts().createrule(
            source_key=key,
            dest_key=dest_key,
            aggregation_type=aggregator,
            bucket_size_msec=bucket_duration,
            align_timestamp=align_timestamp
        )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsdeleterule(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Delete a compaction rule"""
        # Generate a potential destination key
        dest_key = f"{key}_compacted"
        key = str(key).removesuffix("_compacted")
        pipe.ts().deleterule(source_key=key, dest_key=dest_key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsalter(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Enhanced TS.ALTER with more comprehensive parameters
        retention = random.randint(1000, 100000) if random.choice([True, False]) else None
        chunk_size = random.choice([1024, 2048, 4096, 8192]) if random.choice([True, False]) else None
        duplicate_policy = random.choice(["BLOCK", "FIRST", "LAST", "MIN", "MAX", "SUM"]) if random.choice([True, False]) else None
        ignore_max_val_diff = random.randint(0, 1000) if random.choice([True, False]) and duplicate_policy == "LAST" else None
        ignore_max_time_diff = random.randint(0, 1000) if ignore_max_val_diff is not None else None
        
        # Generate labels
        labels = {}
        if random.choice([True, False]):
            num_labels = random.randint(1, 3)
            for i in range(num_labels):
                label_key = random.choice(list(self.labels_dict.keys()))
                label_value = random.choice(self.labels_dict[label_key])
                labels[label_key] = label_value

        pipe.ts().alter(
            key=key,
            retention_msecs=retention,
            chunk_size=chunk_size,
            duplicate_policy=duplicate_policy,
            labels=labels if labels else None,
            ignore_max_val_diff=ignore_max_val_diff,
            ignore_max_time_diff=ignore_max_time_diff
        )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsqueryindex(self, pipe: redis.client.Pipeline, key: str) -> None:
        filter_expr = self._generate_filter()
        pipe.ts().queryindex(filter_expr)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsmget(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Enhanced TS.MGET with more parameters
        filter_expr = self._generate_filter()
        latest = random.choice([True, False])
        withlabels = random.choice([True, False])
        select_labels = [random.choice(list(self.labels_dict.keys()))] if not withlabels and random.choice([True, False]) else None
        
        pipe.ts().mget(
            filters=filter_expr,
            latest=latest,
            with_labels=withlabels,
            select_labels=select_labels,
        )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsmrange_tsmrevrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        filter_expr = self._generate_filter()
        from_timestamp = random.randint(0, 500000)
        to_timestamp = random.randint(from_timestamp, 1000000)
        aggregation_type = random.choice(["avg", "sum", "min", "max", "range", "count", "first", "last", "std.p", "std.s", "var.p", "var.s", "twa", None])
        bucket_size_msec = random.randint(1000, 10000) if aggregation_type else None
        count = random.randint(1, 100) if random.choice([True, False]) else None
        with_labels = random.choice([True, False])
        select_labels = [random.choice(list(self.labels_dict.keys()))] if not with_labels and random.choice([True, False]) else None
        group_by = random.choice(list(self.labels_dict.keys())) if random.choice([True, False]) else None
        reduce = random.choice(["sum", "min", "max"]) if group_by else None
        latest = random.choice([True, False])
        align = random.choice(["+", "-", "start", "end"]) if aggregation_type and random.choice([True, False]) else None
        command = random.choice(["mrange", "mrevrange"])
        empty = random.choice([True, False])
        
        # Execute the command
        if command == "mrange":
            pipe.ts().mrange(
                from_time=from_timestamp,
                to_time=to_timestamp,
                aggregation_type=aggregation_type,
                bucket_size_msec=bucket_size_msec,
                count=count,
                with_labels=with_labels,
                select_labels=select_labels,
                filters=filter_expr,
                groupby=group_by,
                reduce=reduce,
                latest=latest,
                align=align,
                empty=empty,
            )
        else:
            pipe.ts().mrevrange(
                from_time=from_timestamp,
                to_time=to_timestamp,
                aggregation_type=aggregation_type,
                bucket_size_msec=bucket_size_msec,
                count=count,
                with_labels=with_labels,
                select_labels=select_labels,
                filters=filter_expr,
                groupby=group_by,
                reduce=reduce,
                latest=latest,
                align=align,
                empty=empty,
            )

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsdel(self, pipe: redis.client.Pipeline, key: str) -> None:
        from_timestamp = random.randint(0, 500000)
        to_timestamp = random.randint(from_timestamp, 1000000)
        pipe.ts().delete(key, from_timestamp, to_timestamp)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tsdelkey(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.delete(key)

    def _generate_filter(self):
        """Enhanced filter generation with more varied expressions"""
        filter_expressions = []

        # Base matcher
        matcher_label = random.choice(list(self.labels_dict.keys()))
        matcher_value = random.choice(self.labels_dict[matcher_label])
        filter_expressions.append(f"{matcher_label}={matcher_value}")

        # Additional filters with different operators
        remaining_labels = [label for label in self.labels_dict.keys() if label != matcher_label]
        
        if remaining_labels and random.choice([True, False]):
            filter_label = random.choice(remaining_labels)
            operator = random.choice(["=", "!="])
            
            if random.choice([True, False]):
                # Single value filter
                value = random.choice(self.labels_dict[filter_label])
                filter_expressions.append(f"{filter_label}{operator}{value}")
            else:
                # Multi-value filter
                values = random.sample(self.labels_dict[filter_label], min(2, len(self.labels_dict[filter_label])))
                if len(values) > 1:
                    values_str = ",".join(values)
                    filter_expressions.append(f"{filter_label}{operator}({values_str})")
                else:
                    filter_expressions.append(f"{filter_label}{operator}{values[0]}")

        # Empty value filter
        if len(remaining_labels) > 1 and random.choice([True, False]):
            empty_label = random.choice([label for label in remaining_labels if label not in [expr.split('=')[0].split('!')[0] for expr in filter_expressions[1:]]])
            operator = random.choice(["=", "!="])
            filter_expressions.append(f"{empty_label}{operator}")

        return filter_expressions

if __name__ == "__main__":
    ts_gen = parse(TimeSeriesGen)
    # Updated distributions to include all new commands
    ts_gen.distributions = '{"tscreate":100, "tsadd": 100, "tsget": 50, "tsincrby": 80, "tsdecrby": 80, "tsrange": 60, "tsrevrange": 60, "tsinfo": 40, "tsmadd": 70, "tscreaterule": 30, "tsdeleterule": 20, "tsdel": 100, "tsalter":100, "tsqueryindex":100, "tsmget":100, "tsmrange_tsmrevrange":100}'
    ts_gen._run()
