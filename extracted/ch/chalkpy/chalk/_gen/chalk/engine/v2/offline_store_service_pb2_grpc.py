# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

from chalk._gen.chalk.engine.v2 import (
    feature_values_chart_pb2 as chalk_dot_engine_dot_v2_dot_feature__values__chart__pb2,
)
from chalk._gen.chalk.engine.v2 import feature_values_pb2 as chalk_dot_engine_dot_v2_dot_feature__values__pb2
from chalk._gen.chalk.engine.v2 import query_log_pb2 as chalk_dot_engine_dot_v2_dot_query__log__pb2
from chalk._gen.chalk.engine.v2 import query_values_pb2 as chalk_dot_engine_dot_v2_dot_query__values__pb2


class OfflineStoreServiceStub(object):
    """This service exposes endpoints for dealing with the offline store. It should never depend on the python graph.
    v2 introduces two breaking changes:
    Uses messages from engine.v2 instead of common.v1 (common is not meant for engine-specific messages)
    Removes certain endpoints added and had to be immediately deprecated due to deprecation
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetQueryLogEntries = channel.unary_unary(
            "/chalk.engine.v2.OfflineStoreService/GetQueryLogEntries",
            request_serializer=chalk_dot_engine_dot_v2_dot_query__log__pb2.GetQueryLogEntriesRequest.SerializeToString,
            response_deserializer=chalk_dot_engine_dot_v2_dot_query__log__pb2.GetQueryLogEntriesResponse.FromString,
        )
        self.GetQueryValues = channel.unary_unary(
            "/chalk.engine.v2.OfflineStoreService/GetQueryValues",
            request_serializer=chalk_dot_engine_dot_v2_dot_query__values__pb2.GetQueryValuesRequest.SerializeToString,
            response_deserializer=chalk_dot_engine_dot_v2_dot_query__values__pb2.GetQueryValuesResponse.FromString,
        )
        self.GetFeatureValuesTimeSeriesChart = channel.unary_unary(
            "/chalk.engine.v2.OfflineStoreService/GetFeatureValuesTimeSeriesChart",
            request_serializer=chalk_dot_engine_dot_v2_dot_feature__values__chart__pb2.GetFeatureValuesTimeSeriesChartRequest.SerializeToString,
            response_deserializer=chalk_dot_engine_dot_v2_dot_feature__values__chart__pb2.GetFeatureValuesTimeSeriesChartResponse.FromString,
        )
        self.GetFeatureValues = channel.unary_unary(
            "/chalk.engine.v2.OfflineStoreService/GetFeatureValues",
            request_serializer=chalk_dot_engine_dot_v2_dot_feature__values__pb2.GetFeatureValuesRequest.SerializeToString,
            response_deserializer=chalk_dot_engine_dot_v2_dot_feature__values__pb2.GetFeatureValuesResponse.FromString,
        )


class OfflineStoreServiceServicer(object):
    """This service exposes endpoints for dealing with the offline store. It should never depend on the python graph.
    v2 introduces two breaking changes:
    Uses messages from engine.v2 instead of common.v1 (common is not meant for engine-specific messages)
    Removes certain endpoints added and had to be immediately deprecated due to deprecation
    """

    def GetQueryLogEntries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetQueryValues(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetFeatureValuesTimeSeriesChart(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetFeatureValues(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_OfflineStoreServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetQueryLogEntries": grpc.unary_unary_rpc_method_handler(
            servicer.GetQueryLogEntries,
            request_deserializer=chalk_dot_engine_dot_v2_dot_query__log__pb2.GetQueryLogEntriesRequest.FromString,
            response_serializer=chalk_dot_engine_dot_v2_dot_query__log__pb2.GetQueryLogEntriesResponse.SerializeToString,
        ),
        "GetQueryValues": grpc.unary_unary_rpc_method_handler(
            servicer.GetQueryValues,
            request_deserializer=chalk_dot_engine_dot_v2_dot_query__values__pb2.GetQueryValuesRequest.FromString,
            response_serializer=chalk_dot_engine_dot_v2_dot_query__values__pb2.GetQueryValuesResponse.SerializeToString,
        ),
        "GetFeatureValuesTimeSeriesChart": grpc.unary_unary_rpc_method_handler(
            servicer.GetFeatureValuesTimeSeriesChart,
            request_deserializer=chalk_dot_engine_dot_v2_dot_feature__values__chart__pb2.GetFeatureValuesTimeSeriesChartRequest.FromString,
            response_serializer=chalk_dot_engine_dot_v2_dot_feature__values__chart__pb2.GetFeatureValuesTimeSeriesChartResponse.SerializeToString,
        ),
        "GetFeatureValues": grpc.unary_unary_rpc_method_handler(
            servicer.GetFeatureValues,
            request_deserializer=chalk_dot_engine_dot_v2_dot_feature__values__pb2.GetFeatureValuesRequest.FromString,
            response_serializer=chalk_dot_engine_dot_v2_dot_feature__values__pb2.GetFeatureValuesResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("chalk.engine.v2.OfflineStoreService", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class OfflineStoreService(object):
    """This service exposes endpoints for dealing with the offline store. It should never depend on the python graph.
    v2 introduces two breaking changes:
    Uses messages from engine.v2 instead of common.v1 (common is not meant for engine-specific messages)
    Removes certain endpoints added and had to be immediately deprecated due to deprecation
    """

    @staticmethod
    def GetQueryLogEntries(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v2.OfflineStoreService/GetQueryLogEntries",
            chalk_dot_engine_dot_v2_dot_query__log__pb2.GetQueryLogEntriesRequest.SerializeToString,
            chalk_dot_engine_dot_v2_dot_query__log__pb2.GetQueryLogEntriesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetQueryValues(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v2.OfflineStoreService/GetQueryValues",
            chalk_dot_engine_dot_v2_dot_query__values__pb2.GetQueryValuesRequest.SerializeToString,
            chalk_dot_engine_dot_v2_dot_query__values__pb2.GetQueryValuesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetFeatureValuesTimeSeriesChart(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v2.OfflineStoreService/GetFeatureValuesTimeSeriesChart",
            chalk_dot_engine_dot_v2_dot_feature__values__chart__pb2.GetFeatureValuesTimeSeriesChartRequest.SerializeToString,
            chalk_dot_engine_dot_v2_dot_feature__values__chart__pb2.GetFeatureValuesTimeSeriesChartResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetFeatureValues(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v2.OfflineStoreService/GetFeatureValues",
            chalk_dot_engine_dot_v2_dot_feature__values__pb2.GetFeatureValuesRequest.SerializeToString,
            chalk_dot_engine_dot_v2_dot_feature__values__pb2.GetFeatureValuesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
