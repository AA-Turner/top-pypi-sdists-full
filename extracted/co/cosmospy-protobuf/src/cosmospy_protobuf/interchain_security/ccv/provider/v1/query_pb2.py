"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from .....interchain_security.ccv.v1 import ccv_pb2 as interchain__security_dot_ccv_dot_v1_dot_ccv__pb2
from .....interchain_security.ccv.consumer.v1 import genesis_pb2 as interchain__security_dot_ccv_dot_consumer_dot_v1_dot_genesis__pb2
from .....interchain_security.ccv.provider.v1 import provider_pb2 as interchain__security_dot_ccv_dot_provider_dot_v1_dot_provider__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/interchain_security/ccv/provider/v1/query.proto\x12#interchain_security.ccv.provider.v1\x1a\x1cgoogle/api/annotations.proto\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a$interchain_security/ccv/v1/ccv.proto\x1a1interchain_security/ccv/consumer/v1/genesis.proto\x1a2interchain_security/ccv/provider/v1/provider.proto"/\n\x1bQueryConsumerGenesisRequest\x12\x10\n\x08chain_id\x18\x01 \x01(\t"n\n\x1cQueryConsumerGenesisResponse\x12N\n\rgenesis_state\x18\x01 \x01(\x0b21.interchain_security.ccv.consumer.v1.GenesisStateB\x04\xc8\xde\x1f\x00"\x1c\n\x1aQueryConsumerChainsRequest"Y\n\x1bQueryConsumerChainsResponse\x12:\n\x06chains\x18\x01 \x03(\x0b2*.interchain_security.ccv.provider.v1.Chain")\n\'QueryConsumerChainStartProposalsRequest"}\n(QueryConsumerChainStartProposalsResponse\x12Q\n\tproposals\x18\x01 \x01(\x0b2>.interchain_security.ccv.provider.v1.ConsumerAdditionProposals"(\n&QueryConsumerChainStopProposalsRequest"{\n\'QueryConsumerChainStopProposalsResponse\x12P\n\tproposals\x18\x01 \x01(\x0b2=.interchain_security.ccv.provider.v1.ConsumerRemovalProposals",\n\x05Chain\x12\x10\n\x08chain_id\x18\x01 \x01(\t\x12\x11\n\tclient_id\x18\x02 \x01(\t"m\n!QueryValidatorConsumerAddrRequest\x12\x10\n\x08chain_id\x18\x01 \x01(\t\x12,\n\x10provider_address\x18\x02 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address":\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00">\n"QueryValidatorConsumerAddrResponse\x12\x18\n\x10consumer_address\x18\x01 \x01(\t"m\n!QueryValidatorProviderAddrRequest\x12\x10\n\x08chain_id\x18\x01 \x01(\t\x12,\n\x10consumer_address\x18\x02 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address":\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00">\n"QueryValidatorProviderAddrResponse\x12\x18\n\x10provider_address\x18\x01 \x01(\t"\x1b\n\x19QueryThrottleStateRequest"\xe4\x01\n\x1aQueryThrottleStateResponse\x12\x13\n\x0bslash_meter\x18\x01 \x01(\x03\x12\x1d\n\x15slash_meter_allowance\x18\x02 \x01(\x03\x12F\n\x18next_replenish_candidate\x18\x03 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12J\n\x07packets\x18\x04 \x03(\x0b29.interchain_security.ccv.provider.v1.ThrottledSlashPacket";\n\'QueryThrottledConsumerPacketDataRequest\x12\x10\n\x08chain_id\x18\x01 \x01(\t"\xae\x01\n(QueryThrottledConsumerPacketDataResponse\x12\x10\n\x08chain_id\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x04\x12b\n\x13packetDataInstances\x18\x03 \x03(\x0b2?.interchain_security.ccv.provider.v1.ThrottledPacketDataWrapperB\x04\xc8\xde\x1f\x00"\xaa\x01\n\x14ThrottledSlashPacket\x12Q\n\x0cglobal_entry\x18\x01 \x01(\x0b25.interchain_security.ccv.provider.v1.GlobalSlashEntryB\x04\xc8\xde\x1f\x00\x12?\n\x04data\x18\x02 \x01(\x0b2+.interchain_security.ccv.v1.SlashPacketDataB\x04\xc8\xde\x1f\x00"\xb9\x01\n\x1aThrottledPacketDataWrapper\x12C\n\x0cslash_packet\x18\x01 \x01(\x0b2+.interchain_security.ccv.v1.SlashPacketDataH\x00\x12N\n\x12vsc_matured_packet\x18\x02 \x01(\x0b20.interchain_security.ccv.v1.VSCMaturedPacketDataH\x00B\x06\n\x04data",\n*QueryRegisteredConsumerRewardDenomsRequest"=\n+QueryRegisteredConsumerRewardDenomsResponse\x12\x0e\n\x06denoms\x18\x01 \x03(\t2\x9c\x11\n\x05Query\x12\xe2\x01\n\x14QueryConsumerGenesis\x12@.interchain_security.ccv.provider.v1.QueryConsumerGenesisRequest\x1aA.interchain_security.ccv.provider.v1.QueryConsumerGenesisResponse"E\x82\xd3\xe4\x93\x02?\x12=/interchain_security/ccv/provider/consumer_genesis/{chain_id}\x12\xd3\x01\n\x13QueryConsumerChains\x12?.interchain_security.ccv.provider.v1.QueryConsumerChainsRequest\x1a@.interchain_security.ccv.provider.v1.QueryConsumerChainsResponse"9\x82\xd3\xe4\x93\x023\x121/interchain_security/ccv/provider/consumer_chains\x12\x81\x02\n\x18QueryConsumerChainStarts\x12L.interchain_security.ccv.provider.v1.QueryConsumerChainStartProposalsRequest\x1aM.interchain_security.ccv.provider.v1.QueryConsumerChainStartProposalsResponse"H\x82\xd3\xe4\x93\x02B\x12@/interchain_security/ccv/provider/consumer_chain_start_proposals\x12\xfd\x01\n\x17QueryConsumerChainStops\x12K.interchain_security.ccv.provider.v1.QueryConsumerChainStopProposalsRequest\x1aL.interchain_security.ccv.provider.v1.QueryConsumerChainStopProposalsResponse"G\x82\xd3\xe4\x93\x02A\x12?/interchain_security/ccv/provider/consumer_chain_stop_proposals\x12\xf0\x01\n\x1aQueryValidatorConsumerAddr\x12F.interchain_security.ccv.provider.v1.QueryValidatorConsumerAddrRequest\x1aG.interchain_security.ccv.provider.v1.QueryValidatorConsumerAddrResponse"A\x82\xd3\xe4\x93\x02;\x129/interchain_security/ccv/provider/validator_consumer_addr\x12\xf0\x01\n\x1aQueryValidatorProviderAddr\x12F.interchain_security.ccv.provider.v1.QueryValidatorProviderAddrRequest\x1aG.interchain_security.ccv.provider.v1.QueryValidatorProviderAddrResponse"A\x82\xd3\xe4\x93\x02;\x129/interchain_security/ccv/provider/validator_provider_addr\x12\xcf\x01\n\x12QueryThrottleState\x12>.interchain_security.ccv.provider.v1.QueryThrottleStateRequest\x1a?.interchain_security.ccv.provider.v1.QueryThrottleStateResponse"8\x82\xd3\xe4\x93\x022\x120/interchain_security/ccv/provider/throttle_state\x12\x83\x02\n QueryThrottledConsumerPacketData\x12L.interchain_security.ccv.provider.v1.QueryThrottledConsumerPacketDataRequest\x1aM.interchain_security.ccv.provider.v1.QueryThrottledConsumerPacketDataResponse"B\x82\xd3\xe4\x93\x02<\x12:/interchain_security/ccv/provider/pending_consumer_packets\x12\x95\x02\n#QueryRegisteredConsumerRewardDenoms\x12O.interchain_security.ccv.provider.v1.QueryRegisteredConsumerRewardDenomsRequest\x1aP.interchain_security.ccv.provider.v1.QueryRegisteredConsumerRewardDenomsResponse"K\x82\xd3\xe4\x93\x02E\x12C/interchain_security/ccv/provider/registered_consumer_reward_denomsB?Z=github.com/cosmos/interchain-security/v2/x/ccv/provider/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'interchain_security.ccv.provider.v1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z=github.com/cosmos/interchain-security/v2/x/ccv/provider/types'
    _QUERYCONSUMERGENESISRESPONSE.fields_by_name['genesis_state']._options = None
    _QUERYCONSUMERGENESISRESPONSE.fields_by_name['genesis_state']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYVALIDATORCONSUMERADDRREQUEST.fields_by_name['provider_address']._options = None
    _QUERYVALIDATORCONSUMERADDRREQUEST.fields_by_name['provider_address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _QUERYVALIDATORCONSUMERADDRREQUEST._options = None
    _QUERYVALIDATORCONSUMERADDRREQUEST._serialized_options = b'\x88\xa0\x1f\x00\xe8\xa0\x1f\x00'
    _QUERYVALIDATORPROVIDERADDRREQUEST.fields_by_name['consumer_address']._options = None
    _QUERYVALIDATORPROVIDERADDRREQUEST.fields_by_name['consumer_address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _QUERYVALIDATORPROVIDERADDRREQUEST._options = None
    _QUERYVALIDATORPROVIDERADDRREQUEST._serialized_options = b'\x88\xa0\x1f\x00\xe8\xa0\x1f\x00'
    _QUERYTHROTTLESTATERESPONSE.fields_by_name['next_replenish_candidate']._options = None
    _QUERYTHROTTLESTATERESPONSE.fields_by_name['next_replenish_candidate']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _QUERYTHROTTLEDCONSUMERPACKETDATARESPONSE.fields_by_name['packetDataInstances']._options = None
    _QUERYTHROTTLEDCONSUMERPACKETDATARESPONSE.fields_by_name['packetDataInstances']._serialized_options = b'\xc8\xde\x1f\x00'
    _THROTTLEDSLASHPACKET.fields_by_name['global_entry']._options = None
    _THROTTLEDSLASHPACKET.fields_by_name['global_entry']._serialized_options = b'\xc8\xde\x1f\x00'
    _THROTTLEDSLASHPACKET.fields_by_name['data']._options = None
    _THROTTLEDSLASHPACKET.fields_by_name['data']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERY.methods_by_name['QueryConsumerGenesis']._options = None
    _QUERY.methods_by_name['QueryConsumerGenesis']._serialized_options = b'\x82\xd3\xe4\x93\x02?\x12=/interchain_security/ccv/provider/consumer_genesis/{chain_id}'
    _QUERY.methods_by_name['QueryConsumerChains']._options = None
    _QUERY.methods_by_name['QueryConsumerChains']._serialized_options = b'\x82\xd3\xe4\x93\x023\x121/interchain_security/ccv/provider/consumer_chains'
    _QUERY.methods_by_name['QueryConsumerChainStarts']._options = None
    _QUERY.methods_by_name['QueryConsumerChainStarts']._serialized_options = b'\x82\xd3\xe4\x93\x02B\x12@/interchain_security/ccv/provider/consumer_chain_start_proposals'
    _QUERY.methods_by_name['QueryConsumerChainStops']._options = None
    _QUERY.methods_by_name['QueryConsumerChainStops']._serialized_options = b'\x82\xd3\xe4\x93\x02A\x12?/interchain_security/ccv/provider/consumer_chain_stop_proposals'
    _QUERY.methods_by_name['QueryValidatorConsumerAddr']._options = None
    _QUERY.methods_by_name['QueryValidatorConsumerAddr']._serialized_options = b'\x82\xd3\xe4\x93\x02;\x129/interchain_security/ccv/provider/validator_consumer_addr'
    _QUERY.methods_by_name['QueryValidatorProviderAddr']._options = None
    _QUERY.methods_by_name['QueryValidatorProviderAddr']._serialized_options = b'\x82\xd3\xe4\x93\x02;\x129/interchain_security/ccv/provider/validator_provider_addr'
    _QUERY.methods_by_name['QueryThrottleState']._options = None
    _QUERY.methods_by_name['QueryThrottleState']._serialized_options = b'\x82\xd3\xe4\x93\x022\x120/interchain_security/ccv/provider/throttle_state'
    _QUERY.methods_by_name['QueryThrottledConsumerPacketData']._options = None
    _QUERY.methods_by_name['QueryThrottledConsumerPacketData']._serialized_options = b'\x82\xd3\xe4\x93\x02<\x12:/interchain_security/ccv/provider/pending_consumer_packets'
    _QUERY.methods_by_name['QueryRegisteredConsumerRewardDenoms']._options = None
    _QUERY.methods_by_name['QueryRegisteredConsumerRewardDenoms']._serialized_options = b'\x82\xd3\xe4\x93\x02E\x12C/interchain_security/ccv/provider/registered_consumer_reward_denoms'
    _globals['_QUERYCONSUMERGENESISREQUEST']._serialized_start = 314
    _globals['_QUERYCONSUMERGENESISREQUEST']._serialized_end = 361
    _globals['_QUERYCONSUMERGENESISRESPONSE']._serialized_start = 363
    _globals['_QUERYCONSUMERGENESISRESPONSE']._serialized_end = 473
    _globals['_QUERYCONSUMERCHAINSREQUEST']._serialized_start = 475
    _globals['_QUERYCONSUMERCHAINSREQUEST']._serialized_end = 503
    _globals['_QUERYCONSUMERCHAINSRESPONSE']._serialized_start = 505
    _globals['_QUERYCONSUMERCHAINSRESPONSE']._serialized_end = 594
    _globals['_QUERYCONSUMERCHAINSTARTPROPOSALSREQUEST']._serialized_start = 596
    _globals['_QUERYCONSUMERCHAINSTARTPROPOSALSREQUEST']._serialized_end = 637
    _globals['_QUERYCONSUMERCHAINSTARTPROPOSALSRESPONSE']._serialized_start = 639
    _globals['_QUERYCONSUMERCHAINSTARTPROPOSALSRESPONSE']._serialized_end = 764
    _globals['_QUERYCONSUMERCHAINSTOPPROPOSALSREQUEST']._serialized_start = 766
    _globals['_QUERYCONSUMERCHAINSTOPPROPOSALSREQUEST']._serialized_end = 806
    _globals['_QUERYCONSUMERCHAINSTOPPROPOSALSRESPONSE']._serialized_start = 808
    _globals['_QUERYCONSUMERCHAINSTOPPROPOSALSRESPONSE']._serialized_end = 931
    _globals['_CHAIN']._serialized_start = 933
    _globals['_CHAIN']._serialized_end = 977
    _globals['_QUERYVALIDATORCONSUMERADDRREQUEST']._serialized_start = 979
    _globals['_QUERYVALIDATORCONSUMERADDRREQUEST']._serialized_end = 1088
    _globals['_QUERYVALIDATORCONSUMERADDRRESPONSE']._serialized_start = 1090
    _globals['_QUERYVALIDATORCONSUMERADDRRESPONSE']._serialized_end = 1152
    _globals['_QUERYVALIDATORPROVIDERADDRREQUEST']._serialized_start = 1154
    _globals['_QUERYVALIDATORPROVIDERADDRREQUEST']._serialized_end = 1263
    _globals['_QUERYVALIDATORPROVIDERADDRRESPONSE']._serialized_start = 1265
    _globals['_QUERYVALIDATORPROVIDERADDRRESPONSE']._serialized_end = 1327
    _globals['_QUERYTHROTTLESTATEREQUEST']._serialized_start = 1329
    _globals['_QUERYTHROTTLESTATEREQUEST']._serialized_end = 1356
    _globals['_QUERYTHROTTLESTATERESPONSE']._serialized_start = 1359
    _globals['_QUERYTHROTTLESTATERESPONSE']._serialized_end = 1587
    _globals['_QUERYTHROTTLEDCONSUMERPACKETDATAREQUEST']._serialized_start = 1589
    _globals['_QUERYTHROTTLEDCONSUMERPACKETDATAREQUEST']._serialized_end = 1648
    _globals['_QUERYTHROTTLEDCONSUMERPACKETDATARESPONSE']._serialized_start = 1651
    _globals['_QUERYTHROTTLEDCONSUMERPACKETDATARESPONSE']._serialized_end = 1825
    _globals['_THROTTLEDSLASHPACKET']._serialized_start = 1828
    _globals['_THROTTLEDSLASHPACKET']._serialized_end = 1998
    _globals['_THROTTLEDPACKETDATAWRAPPER']._serialized_start = 2001
    _globals['_THROTTLEDPACKETDATAWRAPPER']._serialized_end = 2186
    _globals['_QUERYREGISTEREDCONSUMERREWARDDENOMSREQUEST']._serialized_start = 2188
    _globals['_QUERYREGISTEREDCONSUMERREWARDDENOMSREQUEST']._serialized_end = 2232
    _globals['_QUERYREGISTEREDCONSUMERREWARDDENOMSRESPONSE']._serialized_start = 2234
    _globals['_QUERYREGISTEREDCONSUMERREWARDDENOMSRESPONSE']._serialized_end = 2295
    _globals['_QUERY']._serialized_start = 2298
    _globals['_QUERY']._serialized_end = 4502