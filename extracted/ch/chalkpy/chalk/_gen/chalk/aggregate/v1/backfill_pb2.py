# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/aggregate/v1/backfill.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.aggregate.v1 import timeseries_pb2 as chalk_dot_aggregate_dot_v1_dot_timeseries__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n!chalk/aggregate/v1/backfill.proto\x12\x12\x63halk.aggregate.v1\x1a#chalk/aggregate/v1/timeseries.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x8c\x02\n\x1d\x41ggregateBackfillCostEstimate\x12\x1f\n\x0bmax_buckets\x18\x01 \x01(\x03R\nmaxBuckets\x12)\n\x10\x65xpected_buckets\x18\x02 \x01(\x03R\x0f\x65xpectedBuckets\x12%\n\x0e\x65xpected_bytes\x18\x03 \x01(\x03R\rexpectedBytes\x12\x32\n\x15\x65xpected_storage_cost\x18\x04 \x01(\x01R\x13\x65xpectedStorageCost\x12\x44\n\x10\x65xpected_runtime\x18\x05 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0f\x65xpectedRuntime"\xf8\x02\n\x1b\x41ggregateBackfillUserParams\x12\x1a\n\x08\x66\x65\x61tures\x18\x01 \x03(\tR\x08\x66\x65\x61tures\x12\x1f\n\x08resolver\x18\x02 \x01(\tH\x00R\x08resolver\x88\x01\x01\x12;\n\x15timestamp_column_name\x18\x03 \x01(\tB\x02\x18\x01H\x01R\x13timestampColumnName\x88\x01\x01\x12@\n\x0blower_bound\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x02R\nlowerBound\x88\x01\x01\x12@\n\x0bupper_bound\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x03R\nupperBound\x88\x01\x01\x12\x14\n\x05\x65xact\x18\x06 \x01(\x08R\x05\x65xactB\x0b\n\t_resolverB\x18\n\x16_timestamp_column_nameB\x0e\n\x0c_lower_boundB\x0e\n\x0c_upper_bound"\xe5\x03\n\x11\x41ggregateBackfill\x12?\n\x06series\x18\x01 \x03(\x0b\x32\'.chalk.aggregate.v1.AggregateTimeSeriesR\x06series\x12\x1a\n\x08resolver\x18\x02 \x01(\tR\x08resolver\x12)\n\x10\x64\x61tetime_feature\x18\x03 \x01(\tR\x0f\x64\x61tetimeFeature\x12\x42\n\x0f\x62ucket_duration\x18\x04 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0e\x62ucketDuration\x12/\n\x13\x66ilters_description\x18\x05 \x01(\tR\x12\x66iltersDescription\x12\x19\n\x08group_by\x18\x06 \x03(\tR\x07groupBy\x12>\n\rmax_retention\x18\x07 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0cmaxRetention\x12;\n\x0blower_bound\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nlowerBound\x12;\n\x0bupper_bound\x18\t \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupperBound"\xb5\x01\n!AggregateBackfillWithCostEstimate\x12\x41\n\x08\x62\x61\x63kfill\x18\x01 \x01(\x0b\x32%.chalk.aggregate.v1.AggregateBackfillR\x08\x62\x61\x63kfill\x12M\n\x08\x65stimate\x18\x02 \x01(\x0b\x32\x31.chalk.aggregate.v1.AggregateBackfillCostEstimateR\x08\x65stimate"\xa5\x04\n\x14\x41ggregateBackfillJob\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12%\n\x0e\x65nvironment_id\x18\x02 \x01(\tR\renvironmentId\x12\x1f\n\x08resolver\x18\x03 \x01(\tH\x00R\x08resolver\x88\x01\x01\x12\x1a\n\x08\x66\x65\x61tures\x18\x04 \x03(\tR\x08\x66\x65\x61tures\x12\x1e\n\x08\x61gent_id\x18\x05 \x01(\tH\x01R\x07\x61gentId\x88\x01\x01\x12(\n\rdeployment_id\x18\x06 \x01(\tH\x02R\x0c\x64\x65ploymentId\x88\x01\x01\x12\x39\n\ncreated_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x39\n\nupdated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tupdatedAt\x12\x1c\n\tresolvers\x18\t \x03(\tR\tresolvers\x12@\n\x1a\x63ron_aggregate_backfill_id\x18\n \x01(\tH\x03R\x17\x63ronAggregateBackfillId\x88\x01\x01\x12 \n\tplan_hash\x18\x0b \x01(\tH\x04R\x08planHash\x88\x01\x01\x42\x0b\n\t_resolverB\x0b\n\t_agent_idB\x10\n\x0e_deployment_idB\x1d\n\x1b_cron_aggregate_backfill_idB\x0c\n\n_plan_hash"\xdc\x02\n\x15\x43ronAggregateBackfill\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12%\n\x0e\x65nvironment_id\x18\x02 \x01(\tR\renvironmentId\x12#\n\rdeployment_id\x18\x03 \x01(\tR\x0c\x64\x65ploymentId\x12\x1a\n\x08schedule\x18\x04 \x01(\tR\x08schedule\x12\x1b\n\tplan_hash\x18\x05 \x01(\tR\x08planHash\x12\x1a\n\x08\x66\x65\x61tures\x18\x08 \x03(\tR\x08\x66\x65\x61tures\x12\x1c\n\tresolvers\x18\t \x03(\tR\tresolvers\x12\x39\n\ncreated_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x39\n\nupdated_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tupdatedAtB\xab\x01\n\x16\x63om.chalk.aggregate.v1B\rBackfillProtoP\x01Z\x18\x61ggregate/v1;aggregatev1\xa2\x02\x03\x43\x41X\xaa\x02\x12\x43halk.Aggregate.V1\xca\x02\x12\x43halk\\Aggregate\\V1\xe2\x02\x1e\x43halk\\Aggregate\\V1\\GPBMetadata\xea\x02\x14\x43halk::Aggregate::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.aggregate.v1.backfill_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\026com.chalk.aggregate.v1B\rBackfillProtoP\001Z\030aggregate/v1;aggregatev1\242\002\003CAX\252\002\022Chalk.Aggregate.V1\312\002\022Chalk\\Aggregate\\V1\342\002\036Chalk\\Aggregate\\V1\\GPBMetadata\352\002\024Chalk::Aggregate::V1"
    _globals["_AGGREGATEBACKFILLUSERPARAMS"].fields_by_name["timestamp_column_name"]._options = None
    _globals["_AGGREGATEBACKFILLUSERPARAMS"].fields_by_name["timestamp_column_name"]._serialized_options = b"\030\001"
    _globals["_AGGREGATEBACKFILLCOSTESTIMATE"]._serialized_start = 160
    _globals["_AGGREGATEBACKFILLCOSTESTIMATE"]._serialized_end = 428
    _globals["_AGGREGATEBACKFILLUSERPARAMS"]._serialized_start = 431
    _globals["_AGGREGATEBACKFILLUSERPARAMS"]._serialized_end = 807
    _globals["_AGGREGATEBACKFILL"]._serialized_start = 810
    _globals["_AGGREGATEBACKFILL"]._serialized_end = 1295
    _globals["_AGGREGATEBACKFILLWITHCOSTESTIMATE"]._serialized_start = 1298
    _globals["_AGGREGATEBACKFILLWITHCOSTESTIMATE"]._serialized_end = 1479
    _globals["_AGGREGATEBACKFILLJOB"]._serialized_start = 1482
    _globals["_AGGREGATEBACKFILLJOB"]._serialized_end = 2031
    _globals["_CRONAGGREGATEBACKFILL"]._serialized_start = 2034
    _globals["_CRONAGGREGATEBACKFILL"]._serialized_end = 2382
# @@protoc_insertion_point(module_scope)
