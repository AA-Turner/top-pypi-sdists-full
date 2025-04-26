"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from .....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from .....interchain_security.ccv.consumer.v1 import consumer_pb2 as interchain__security_dot_ccv_dot_consumer_dot_v1_dot_consumer__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/interchain_security/ccv/consumer/v1/query.proto\x12#interchain_security.ccv.consumer.v1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a2interchain_security/ccv/consumer/v1/consumer.proto"\xb2\x01\n\x1bNextFeeDistributionEstimate\x12\x15\n\rcurrentHeight\x18\x01 \x01(\x03\x12\x12\n\nlastHeight\x18\x02 \x01(\x03\x12\x12\n\nnextHeight\x18\x03 \x01(\x03\x12\x1d\n\x15distribution_fraction\x18\x04 \x01(\t\x12\r\n\x05total\x18\x05 \x01(\t\x12\x12\n\ntoProvider\x18\x06 \x01(\t\x12\x12\n\ntoConsumer\x18\x07 \x01(\t")\n\'QueryNextFeeDistributionEstimateRequest"z\n(QueryNextFeeDistributionEstimateResponse\x12N\n\x04data\x18\x01 \x01(\x0b2@.interchain_security.ccv.consumer.v1.NextFeeDistributionEstimate"\x14\n\x12QueryParamsRequest"X\n\x13QueryParamsResponse\x12A\n\x06params\x18\x01 \x01(\x0b2+.interchain_security.ccv.consumer.v1.ParamsB\x04\xc8\xde\x1f\x002\xb7\x03\n\x05Query\x12\xf8\x01\n\x18QueryNextFeeDistribution\x12L.interchain_security.ccv.consumer.v1.QueryNextFeeDistributionEstimateRequest\x1aM.interchain_security.ccv.consumer.v1.QueryNextFeeDistributionEstimateResponse"?\x82\xd3\xe4\x93\x029\x127/interchain_security/ccv/consumer/next-fee-distribution\x12\xb2\x01\n\x0bQueryParams\x127.interchain_security.ccv.consumer.v1.QueryParamsRequest\x1a8.interchain_security.ccv.consumer.v1.QueryParamsResponse"0\x82\xd3\xe4\x93\x02*\x12(/interchain_security/ccv/consumer/paramsB?Z=github.com/cosmos/interchain-security/v2/x/ccv/consumer/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'interchain_security.ccv.consumer.v1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z=github.com/cosmos/interchain-security/v2/x/ccv/consumer/types'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERY.methods_by_name['QueryNextFeeDistribution']._options = None
    _QUERY.methods_by_name['QueryNextFeeDistribution']._serialized_options = b'\x82\xd3\xe4\x93\x029\x127/interchain_security/ccv/consumer/next-fee-distribution'
    _QUERY.methods_by_name['QueryParams']._options = None
    _QUERY.methods_by_name['QueryParams']._serialized_options = b'\x82\xd3\xe4\x93\x02*\x12(/interchain_security/ccv/consumer/params'
    _globals['_NEXTFEEDISTRIBUTIONESTIMATE']._serialized_start = 193
    _globals['_NEXTFEEDISTRIBUTIONESTIMATE']._serialized_end = 371
    _globals['_QUERYNEXTFEEDISTRIBUTIONESTIMATEREQUEST']._serialized_start = 373
    _globals['_QUERYNEXTFEEDISTRIBUTIONESTIMATEREQUEST']._serialized_end = 414
    _globals['_QUERYNEXTFEEDISTRIBUTIONESTIMATERESPONSE']._serialized_start = 416
    _globals['_QUERYNEXTFEEDISTRIBUTIONESTIMATERESPONSE']._serialized_end = 538
    _globals['_QUERYPARAMSREQUEST']._serialized_start = 540
    _globals['_QUERYPARAMSREQUEST']._serialized_end = 560
    _globals['_QUERYPARAMSRESPONSE']._serialized_start = 562
    _globals['_QUERYPARAMSRESPONSE']._serialized_end = 650
    _globals['_QUERY']._serialized_start = 653
    _globals['_QUERY']._serialized_end = 1092