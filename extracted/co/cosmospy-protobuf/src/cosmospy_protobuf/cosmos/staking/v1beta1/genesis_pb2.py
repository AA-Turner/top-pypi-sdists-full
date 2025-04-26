"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.staking.v1beta1 import staking_pb2 as cosmos_dot_staking_dot_v1beta1_dot_staking__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$cosmos/staking/v1beta1/genesis.proto\x12\x16cosmos.staking.v1beta1\x1a\x14gogoproto/gogo.proto\x1a$cosmos/staking/v1beta1/staking.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x9f\x07\n\x0cGenesisState\x124\n\x06params\x18\x01 \x01(\x0b2\x1e.cosmos.staking.v1beta1.ParamsB\x04\xc8\xde\x1f\x00\x12c\n\x10last_total_power\x18\x02 \x01(\x0cBI\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x17yaml:"last_total_power"\x12o\n\x15last_validator_powers\x18\x03 \x03(\x0b2*.cosmos.staking.v1beta1.LastValidatorPowerB$\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"last_validator_powers"\x12;\n\nvalidators\x18\x04 \x03(\x0b2!.cosmos.staking.v1beta1.ValidatorB\x04\xc8\xde\x1f\x00\x12=\n\x0bdelegations\x18\x05 \x03(\x0b2".cosmos.staking.v1beta1.DelegationB\x04\xc8\xde\x1f\x00\x12p\n\x15unbonding_delegations\x18\x06 \x03(\x0b2+.cosmos.staking.v1beta1.UnbondingDelegationB$\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"unbonding_delegations"\x12A\n\rredelegations\x18\x07 \x03(\x0b2$.cosmos.staking.v1beta1.RedelegationB\x04\xc8\xde\x1f\x00\x12\x10\n\x08exported\x18\x08 \x01(\x08\x12Q\n\x16tokenize_share_records\x18\t \x03(\x0b2+.cosmos.staking.v1beta1.TokenizeShareRecordB\x04\xc8\xde\x1f\x00\x12%\n\x1dlast_tokenize_share_record_id\x18\n \x01(\x04\x12w\n\x1atotal_liquid_staked_tokens\x18\x0b \x01(\x0cBS\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f!yaml:"total_liquid_staked_tokens"\x12M\n\x14tokenize_share_locks\x18\x0c \x03(\x0b2).cosmos.staking.v1beta1.TokenizeShareLockB\x04\xc8\xde\x1f\x00"\x8d\x01\n\x11TokenizeShareLock\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12W\n\x0fcompletion_time\x18\x03 \x01(\x0b2\x1a.google.protobuf.TimestampB"\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"completion_time"\x90\xdf\x1f\x01">\n\x12LastValidatorPower\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\r\n\x05power\x18\x02 \x01(\x03:\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00B.Z,github.com/cosmos/cosmos-sdk/x/staking/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.staking.v1beta1.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z,github.com/cosmos/cosmos-sdk/x/staking/types'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['last_total_power']._options = None
    _GENESISSTATE.fields_by_name['last_total_power']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x17yaml:"last_total_power"'
    _GENESISSTATE.fields_by_name['last_validator_powers']._options = None
    _GENESISSTATE.fields_by_name['last_validator_powers']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"last_validator_powers"'
    _GENESISSTATE.fields_by_name['validators']._options = None
    _GENESISSTATE.fields_by_name['validators']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['delegations']._options = None
    _GENESISSTATE.fields_by_name['delegations']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['unbonding_delegations']._options = None
    _GENESISSTATE.fields_by_name['unbonding_delegations']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"unbonding_delegations"'
    _GENESISSTATE.fields_by_name['redelegations']._options = None
    _GENESISSTATE.fields_by_name['redelegations']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['tokenize_share_records']._options = None
    _GENESISSTATE.fields_by_name['tokenize_share_records']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['total_liquid_staked_tokens']._options = None
    _GENESISSTATE.fields_by_name['total_liquid_staked_tokens']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f!yaml:"total_liquid_staked_tokens"'
    _GENESISSTATE.fields_by_name['tokenize_share_locks']._options = None
    _GENESISSTATE.fields_by_name['tokenize_share_locks']._serialized_options = b'\xc8\xde\x1f\x00'
    _TOKENIZESHARELOCK.fields_by_name['completion_time']._options = None
    _TOKENIZESHARELOCK.fields_by_name['completion_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"completion_time"\x90\xdf\x1f\x01'
    _LASTVALIDATORPOWER._options = None
    _LASTVALIDATORPOWER._serialized_options = b'\x88\xa0\x1f\x00\xe8\xa0\x1f\x00'
    _globals['_GENESISSTATE']._serialized_start = 158
    _globals['_GENESISSTATE']._serialized_end = 1085
    _globals['_TOKENIZESHARELOCK']._serialized_start = 1088
    _globals['_TOKENIZESHARELOCK']._serialized_end = 1229
    _globals['_LASTVALIDATORPOWER']._serialized_start = 1231
    _globals['_LASTVALIDATORPOWER']._serialized_end = 1293