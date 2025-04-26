"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...tendermint.crypto import proof_pb2 as tendermint_dot_crypto_dot_proof__pb2
from ...tendermint.types import types_pb2 as tendermint_dot_types_dot_types__pb2
from ...tendermint.crypto import keys_pb2 as tendermint_dot_crypto_dot_keys__pb2
from ...tendermint.types import params_pb2 as tendermint_dot_types_dot_params__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1btendermint/abci/types.proto\x12\x0ftendermint.abci\x1a\x1dtendermint/crypto/proof.proto\x1a\x1ctendermint/types/types.proto\x1a\x1ctendermint/crypto/keys.proto\x1a\x1dtendermint/types/params.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x14gogoproto/gogo.proto"\xea\x06\n\x07Request\x12,\n\x04echo\x18\x01 \x01(\x0b2\x1c.tendermint.abci.RequestEchoH\x00\x12.\n\x05flush\x18\x02 \x01(\x0b2\x1d.tendermint.abci.RequestFlushH\x00\x12,\n\x04info\x18\x03 \x01(\x0b2\x1c.tendermint.abci.RequestInfoH\x00\x127\n\nset_option\x18\x04 \x01(\x0b2!.tendermint.abci.RequestSetOptionH\x00\x127\n\ninit_chain\x18\x05 \x01(\x0b2!.tendermint.abci.RequestInitChainH\x00\x12.\n\x05query\x18\x06 \x01(\x0b2\x1d.tendermint.abci.RequestQueryH\x00\x129\n\x0bbegin_block\x18\x07 \x01(\x0b2".tendermint.abci.RequestBeginBlockH\x00\x123\n\x08check_tx\x18\x08 \x01(\x0b2\x1f.tendermint.abci.RequestCheckTxH\x00\x127\n\ndeliver_tx\x18\t \x01(\x0b2!.tendermint.abci.RequestDeliverTxH\x00\x125\n\tend_block\x18\n \x01(\x0b2 .tendermint.abci.RequestEndBlockH\x00\x120\n\x06commit\x18\x0b \x01(\x0b2\x1e.tendermint.abci.RequestCommitH\x00\x12?\n\x0elist_snapshots\x18\x0c \x01(\x0b2%.tendermint.abci.RequestListSnapshotsH\x00\x12?\n\x0eoffer_snapshot\x18\r \x01(\x0b2%.tendermint.abci.RequestOfferSnapshotH\x00\x12H\n\x13load_snapshot_chunk\x18\x0e \x01(\x0b2).tendermint.abci.RequestLoadSnapshotChunkH\x00\x12J\n\x14apply_snapshot_chunk\x18\x0f \x01(\x0b2*.tendermint.abci.RequestApplySnapshotChunkH\x00B\x07\n\x05value"\x1e\n\x0bRequestEcho\x12\x0f\n\x07message\x18\x01 \x01(\t"\x0e\n\x0cRequestFlush"J\n\x0bRequestInfo\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x15\n\rblock_version\x18\x02 \x01(\x04\x12\x13\n\x0bp2p_version\x18\x03 \x01(\x04".\n\x10RequestSetOption\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t"\x81\x02\n\x10RequestInitChain\x122\n\x04time\x18\x01 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12\x10\n\x08chain_id\x18\x02 \x01(\t\x12:\n\x10consensus_params\x18\x03 \x01(\x0b2 .tendermint.abci.ConsensusParams\x12:\n\nvalidators\x18\x04 \x03(\x0b2 .tendermint.abci.ValidatorUpdateB\x04\xc8\xde\x1f\x00\x12\x17\n\x0fapp_state_bytes\x18\x05 \x01(\x0c\x12\x16\n\x0einitial_height\x18\x06 \x01(\x03"I\n\x0cRequestQuery\x12\x0c\n\x04data\x18\x01 \x01(\x0c\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x0e\n\x06height\x18\x03 \x01(\x03\x12\r\n\x05prove\x18\x04 \x01(\x08"\xd1\x01\n\x11RequestBeginBlock\x12\x0c\n\x04hash\x18\x01 \x01(\x0c\x12.\n\x06header\x18\x02 \x01(\x0b2\x18.tendermint.types.HeaderB\x04\xc8\xde\x1f\x00\x12?\n\x10last_commit_info\x18\x03 \x01(\x0b2\x1f.tendermint.abci.LastCommitInfoB\x04\xc8\xde\x1f\x00\x12=\n\x14byzantine_validators\x18\x04 \x03(\x0b2\x19.tendermint.abci.EvidenceB\x04\xc8\xde\x1f\x00"H\n\x0eRequestCheckTx\x12\n\n\x02tx\x18\x01 \x01(\x0c\x12*\n\x04type\x18\x02 \x01(\x0e2\x1c.tendermint.abci.CheckTxType"\x1e\n\x10RequestDeliverTx\x12\n\n\x02tx\x18\x01 \x01(\x0c"!\n\x0fRequestEndBlock\x12\x0e\n\x06height\x18\x01 \x01(\x03"\x0f\n\rRequestCommit"\x16\n\x14RequestListSnapshots"U\n\x14RequestOfferSnapshot\x12+\n\x08snapshot\x18\x01 \x01(\x0b2\x19.tendermint.abci.Snapshot\x12\x10\n\x08app_hash\x18\x02 \x01(\x0c"I\n\x18RequestLoadSnapshotChunk\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x0e\n\x06format\x18\x02 \x01(\r\x12\r\n\x05chunk\x18\x03 \x01(\r"I\n\x19RequestApplySnapshotChunk\x12\r\n\x05index\x18\x01 \x01(\r\x12\r\n\x05chunk\x18\x02 \x01(\x0c\x12\x0e\n\x06sender\x18\x03 \x01(\t"\xb3\x07\n\x08Response\x127\n\texception\x18\x01 \x01(\x0b2".tendermint.abci.ResponseExceptionH\x00\x12-\n\x04echo\x18\x02 \x01(\x0b2\x1d.tendermint.abci.ResponseEchoH\x00\x12/\n\x05flush\x18\x03 \x01(\x0b2\x1e.tendermint.abci.ResponseFlushH\x00\x12-\n\x04info\x18\x04 \x01(\x0b2\x1d.tendermint.abci.ResponseInfoH\x00\x128\n\nset_option\x18\x05 \x01(\x0b2".tendermint.abci.ResponseSetOptionH\x00\x128\n\ninit_chain\x18\x06 \x01(\x0b2".tendermint.abci.ResponseInitChainH\x00\x12/\n\x05query\x18\x07 \x01(\x0b2\x1e.tendermint.abci.ResponseQueryH\x00\x12:\n\x0bbegin_block\x18\x08 \x01(\x0b2#.tendermint.abci.ResponseBeginBlockH\x00\x124\n\x08check_tx\x18\t \x01(\x0b2 .tendermint.abci.ResponseCheckTxH\x00\x128\n\ndeliver_tx\x18\n \x01(\x0b2".tendermint.abci.ResponseDeliverTxH\x00\x126\n\tend_block\x18\x0b \x01(\x0b2!.tendermint.abci.ResponseEndBlockH\x00\x121\n\x06commit\x18\x0c \x01(\x0b2\x1f.tendermint.abci.ResponseCommitH\x00\x12@\n\x0elist_snapshots\x18\r \x01(\x0b2&.tendermint.abci.ResponseListSnapshotsH\x00\x12@\n\x0eoffer_snapshot\x18\x0e \x01(\x0b2&.tendermint.abci.ResponseOfferSnapshotH\x00\x12I\n\x13load_snapshot_chunk\x18\x0f \x01(\x0b2*.tendermint.abci.ResponseLoadSnapshotChunkH\x00\x12K\n\x14apply_snapshot_chunk\x18\x10 \x01(\x0b2+.tendermint.abci.ResponseApplySnapshotChunkH\x00B\x07\n\x05value""\n\x11ResponseException\x12\r\n\x05error\x18\x01 \x01(\t"\x1f\n\x0cResponseEcho\x12\x0f\n\x07message\x18\x01 \x01(\t"\x0f\n\rResponseFlush"z\n\x0cResponseInfo\x12\x0c\n\x04data\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x13\n\x0bapp_version\x18\x03 \x01(\x04\x12\x19\n\x11last_block_height\x18\x04 \x01(\x03\x12\x1b\n\x13last_block_app_hash\x18\x05 \x01(\x0c"<\n\x11ResponseSetOption\x12\x0c\n\x04code\x18\x01 \x01(\r\x12\x0b\n\x03log\x18\x03 \x01(\t\x12\x0c\n\x04info\x18\x04 \x01(\t"\x9d\x01\n\x11ResponseInitChain\x12:\n\x10consensus_params\x18\x01 \x01(\x0b2 .tendermint.abci.ConsensusParams\x12:\n\nvalidators\x18\x02 \x03(\x0b2 .tendermint.abci.ValidatorUpdateB\x04\xc8\xde\x1f\x00\x12\x10\n\x08app_hash\x18\x03 \x01(\x0c"\xb6\x01\n\rResponseQuery\x12\x0c\n\x04code\x18\x01 \x01(\r\x12\x0b\n\x03log\x18\x03 \x01(\t\x12\x0c\n\x04info\x18\x04 \x01(\t\x12\r\n\x05index\x18\x05 \x01(\x03\x12\x0b\n\x03key\x18\x06 \x01(\x0c\x12\r\n\x05value\x18\x07 \x01(\x0c\x12.\n\tproof_ops\x18\x08 \x01(\x0b2\x1b.tendermint.crypto.ProofOps\x12\x0e\n\x06height\x18\t \x01(\x03\x12\x11\n\tcodespace\x18\n \x01(\t"V\n\x12ResponseBeginBlock\x12@\n\x06events\x18\x01 \x03(\x0b2\x16.tendermint.abci.EventB\x18\xc8\xde\x1f\x00\xea\xde\x1f\x10events,omitempty"\x92\x02\n\x0fResponseCheckTx\x12\x0c\n\x04code\x18\x01 \x01(\r\x12\x0c\n\x04data\x18\x02 \x01(\x0c\x12\x0b\n\x03log\x18\x03 \x01(\t\x12\x0c\n\x04info\x18\x04 \x01(\t\x12\x1e\n\ngas_wanted\x18\x05 \x01(\x03R\ngas_wanted\x12\x1a\n\x08gas_used\x18\x06 \x01(\x03R\x08gas_used\x12@\n\x06events\x18\x07 \x03(\x0b2\x16.tendermint.abci.EventB\x18\xc8\xde\x1f\x00\xea\xde\x1f\x10events,omitempty\x12\x11\n\tcodespace\x18\x08 \x01(\t\x12\x0e\n\x06sender\x18\t \x01(\t\x12\x10\n\x08priority\x18\n \x01(\x03\x12\x15\n\rmempool_error\x18\x0b \x01(\t"\xdb\x01\n\x11ResponseDeliverTx\x12\x0c\n\x04code\x18\x01 \x01(\r\x12\x0c\n\x04data\x18\x02 \x01(\x0c\x12\x0b\n\x03log\x18\x03 \x01(\t\x12\x0c\n\x04info\x18\x04 \x01(\t\x12\x1e\n\ngas_wanted\x18\x05 \x01(\x03R\ngas_wanted\x12\x1a\n\x08gas_used\x18\x06 \x01(\x03R\x08gas_used\x12@\n\x06events\x18\x07 \x03(\x0b2\x16.tendermint.abci.EventB\x18\xc8\xde\x1f\x00\xea\xde\x1f\x10events,omitempty\x12\x11\n\tcodespace\x18\x08 \x01(\t"\xda\x01\n\x10ResponseEndBlock\x12A\n\x11validator_updates\x18\x01 \x03(\x0b2 .tendermint.abci.ValidatorUpdateB\x04\xc8\xde\x1f\x00\x12A\n\x17consensus_param_updates\x18\x02 \x01(\x0b2 .tendermint.abci.ConsensusParams\x12@\n\x06events\x18\x03 \x03(\x0b2\x16.tendermint.abci.EventB\x18\xc8\xde\x1f\x00\xea\xde\x1f\x10events,omitempty"5\n\x0eResponseCommit\x12\x0c\n\x04data\x18\x02 \x01(\x0c\x12\x15\n\rretain_height\x18\x03 \x01(\x03"E\n\x15ResponseListSnapshots\x12,\n\tsnapshots\x18\x01 \x03(\x0b2\x19.tendermint.abci.Snapshot"\xb6\x01\n\x15ResponseOfferSnapshot\x12=\n\x06result\x18\x01 \x01(\x0e2-.tendermint.abci.ResponseOfferSnapshot.Result"^\n\x06Result\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06ACCEPT\x10\x01\x12\t\n\x05ABORT\x10\x02\x12\n\n\x06REJECT\x10\x03\x12\x11\n\rREJECT_FORMAT\x10\x04\x12\x11\n\rREJECT_SENDER\x10\x05"*\n\x19ResponseLoadSnapshotChunk\x12\r\n\x05chunk\x18\x01 \x01(\x0c"\xf2\x01\n\x1aResponseApplySnapshotChunk\x12B\n\x06result\x18\x01 \x01(\x0e22.tendermint.abci.ResponseApplySnapshotChunk.Result\x12\x16\n\x0erefetch_chunks\x18\x02 \x03(\r\x12\x16\n\x0ereject_senders\x18\x03 \x03(\t"`\n\x06Result\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06ACCEPT\x10\x01\x12\t\n\x05ABORT\x10\x02\x12\t\n\x05RETRY\x10\x03\x12\x12\n\x0eRETRY_SNAPSHOT\x10\x04\x12\x13\n\x0fREJECT_SNAPSHOT\x10\x05"\xda\x01\n\x0fConsensusParams\x12+\n\x05block\x18\x01 \x01(\x0b2\x1c.tendermint.abci.BlockParams\x122\n\x08evidence\x18\x02 \x01(\x0b2 .tendermint.types.EvidenceParams\x124\n\tvalidator\x18\x03 \x01(\x0b2!.tendermint.types.ValidatorParams\x120\n\x07version\x18\x04 \x01(\x0b2\x1f.tendermint.types.VersionParams"1\n\x0bBlockParams\x12\x11\n\tmax_bytes\x18\x01 \x01(\x03\x12\x0f\n\x07max_gas\x18\x02 \x01(\x03"O\n\x0eLastCommitInfo\x12\r\n\x05round\x18\x01 \x01(\x05\x12.\n\x05votes\x18\x02 \x03(\x0b2\x19.tendermint.abci.VoteInfoB\x04\xc8\xde\x1f\x00"h\n\x05Event\x12\x0c\n\x04type\x18\x01 \x01(\t\x12Q\n\nattributes\x18\x02 \x03(\x0b2\x1f.tendermint.abci.EventAttributeB\x1c\xc8\xde\x1f\x00\xea\xde\x1f\x14attributes,omitempty";\n\x0eEventAttribute\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\r\n\x05index\x18\x03 \x01(\x08"o\n\x08TxResult\x12\x0e\n\x06height\x18\x01 \x01(\x03\x12\r\n\x05index\x18\x02 \x01(\r\x12\n\n\x02tx\x18\x03 \x01(\x0c\x128\n\x06result\x18\x04 \x01(\x0b2".tendermint.abci.ResponseDeliverTxB\x04\xc8\xde\x1f\x00"+\n\tValidator\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12\r\n\x05power\x18\x03 \x01(\x03"U\n\x0fValidatorUpdate\x123\n\x07pub_key\x18\x01 \x01(\x0b2\x1c.tendermint.crypto.PublicKeyB\x04\xc8\xde\x1f\x00\x12\r\n\x05power\x18\x02 \x01(\x03"Z\n\x08VoteInfo\x123\n\tvalidator\x18\x01 \x01(\x0b2\x1a.tendermint.abci.ValidatorB\x04\xc8\xde\x1f\x00\x12\x19\n\x11signed_last_block\x18\x02 \x01(\x08"\xcc\x01\n\x08Evidence\x12+\n\x04type\x18\x01 \x01(\x0e2\x1d.tendermint.abci.EvidenceType\x123\n\tvalidator\x18\x02 \x01(\x0b2\x1a.tendermint.abci.ValidatorB\x04\xc8\xde\x1f\x00\x12\x0e\n\x06height\x18\x03 \x01(\x03\x122\n\x04time\x18\x04 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12\x1a\n\x12total_voting_power\x18\x05 \x01(\x03"Z\n\x08Snapshot\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x0e\n\x06format\x18\x02 \x01(\r\x12\x0e\n\x06chunks\x18\x03 \x01(\r\x12\x0c\n\x04hash\x18\x04 \x01(\x0c\x12\x10\n\x08metadata\x18\x05 \x01(\x0c*9\n\x0bCheckTxType\x12\x10\n\x03NEW\x10\x00\x1a\x07\x8a\x9d \x03New\x12\x18\n\x07RECHECK\x10\x01\x1a\x0b\x8a\x9d \x07Recheck*H\n\x0cEvidenceType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x12\n\x0eDUPLICATE_VOTE\x10\x01\x12\x17\n\x13LIGHT_CLIENT_ATTACK\x10\x022\x83\n\n\x0fABCIApplication\x12C\n\x04Echo\x12\x1c.tendermint.abci.RequestEcho\x1a\x1d.tendermint.abci.ResponseEcho\x12F\n\x05Flush\x12\x1d.tendermint.abci.RequestFlush\x1a\x1e.tendermint.abci.ResponseFlush\x12C\n\x04Info\x12\x1c.tendermint.abci.RequestInfo\x1a\x1d.tendermint.abci.ResponseInfo\x12R\n\tSetOption\x12!.tendermint.abci.RequestSetOption\x1a".tendermint.abci.ResponseSetOption\x12R\n\tDeliverTx\x12!.tendermint.abci.RequestDeliverTx\x1a".tendermint.abci.ResponseDeliverTx\x12L\n\x07CheckTx\x12\x1f.tendermint.abci.RequestCheckTx\x1a .tendermint.abci.ResponseCheckTx\x12F\n\x05Query\x12\x1d.tendermint.abci.RequestQuery\x1a\x1e.tendermint.abci.ResponseQuery\x12I\n\x06Commit\x12\x1e.tendermint.abci.RequestCommit\x1a\x1f.tendermint.abci.ResponseCommit\x12R\n\tInitChain\x12!.tendermint.abci.RequestInitChain\x1a".tendermint.abci.ResponseInitChain\x12U\n\nBeginBlock\x12".tendermint.abci.RequestBeginBlock\x1a#.tendermint.abci.ResponseBeginBlock\x12O\n\x08EndBlock\x12 .tendermint.abci.RequestEndBlock\x1a!.tendermint.abci.ResponseEndBlock\x12^\n\rListSnapshots\x12%.tendermint.abci.RequestListSnapshots\x1a&.tendermint.abci.ResponseListSnapshots\x12^\n\rOfferSnapshot\x12%.tendermint.abci.RequestOfferSnapshot\x1a&.tendermint.abci.ResponseOfferSnapshot\x12j\n\x11LoadSnapshotChunk\x12).tendermint.abci.RequestLoadSnapshotChunk\x1a*.tendermint.abci.ResponseLoadSnapshotChunk\x12m\n\x12ApplySnapshotChunk\x12*.tendermint.abci.RequestApplySnapshotChunk\x1a+.tendermint.abci.ResponseApplySnapshotChunkB-Z+github.com/tendermint/tendermint/abci/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tendermint.abci.types_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z+github.com/tendermint/tendermint/abci/types'
    _CHECKTXTYPE.values_by_name['NEW']._options = None
    _CHECKTXTYPE.values_by_name['NEW']._serialized_options = b'\x8a\x9d \x03New'
    _CHECKTXTYPE.values_by_name['RECHECK']._options = None
    _CHECKTXTYPE.values_by_name['RECHECK']._serialized_options = b'\x8a\x9d \x07Recheck'
    _REQUESTINITCHAIN.fields_by_name['time']._options = None
    _REQUESTINITCHAIN.fields_by_name['time']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _REQUESTINITCHAIN.fields_by_name['validators']._options = None
    _REQUESTINITCHAIN.fields_by_name['validators']._serialized_options = b'\xc8\xde\x1f\x00'
    _REQUESTBEGINBLOCK.fields_by_name['header']._options = None
    _REQUESTBEGINBLOCK.fields_by_name['header']._serialized_options = b'\xc8\xde\x1f\x00'
    _REQUESTBEGINBLOCK.fields_by_name['last_commit_info']._options = None
    _REQUESTBEGINBLOCK.fields_by_name['last_commit_info']._serialized_options = b'\xc8\xde\x1f\x00'
    _REQUESTBEGINBLOCK.fields_by_name['byzantine_validators']._options = None
    _REQUESTBEGINBLOCK.fields_by_name['byzantine_validators']._serialized_options = b'\xc8\xde\x1f\x00'
    _RESPONSEINITCHAIN.fields_by_name['validators']._options = None
    _RESPONSEINITCHAIN.fields_by_name['validators']._serialized_options = b'\xc8\xde\x1f\x00'
    _RESPONSEBEGINBLOCK.fields_by_name['events']._options = None
    _RESPONSEBEGINBLOCK.fields_by_name['events']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x10events,omitempty'
    _RESPONSECHECKTX.fields_by_name['events']._options = None
    _RESPONSECHECKTX.fields_by_name['events']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x10events,omitempty'
    _RESPONSEDELIVERTX.fields_by_name['events']._options = None
    _RESPONSEDELIVERTX.fields_by_name['events']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x10events,omitempty'
    _RESPONSEENDBLOCK.fields_by_name['validator_updates']._options = None
    _RESPONSEENDBLOCK.fields_by_name['validator_updates']._serialized_options = b'\xc8\xde\x1f\x00'
    _RESPONSEENDBLOCK.fields_by_name['events']._options = None
    _RESPONSEENDBLOCK.fields_by_name['events']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x10events,omitempty'
    _LASTCOMMITINFO.fields_by_name['votes']._options = None
    _LASTCOMMITINFO.fields_by_name['votes']._serialized_options = b'\xc8\xde\x1f\x00'
    _EVENT.fields_by_name['attributes']._options = None
    _EVENT.fields_by_name['attributes']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x14attributes,omitempty'
    _TXRESULT.fields_by_name['result']._options = None
    _TXRESULT.fields_by_name['result']._serialized_options = b'\xc8\xde\x1f\x00'
    _VALIDATORUPDATE.fields_by_name['pub_key']._options = None
    _VALIDATORUPDATE.fields_by_name['pub_key']._serialized_options = b'\xc8\xde\x1f\x00'
    _VOTEINFO.fields_by_name['validator']._options = None
    _VOTEINFO.fields_by_name['validator']._serialized_options = b'\xc8\xde\x1f\x00'
    _EVIDENCE.fields_by_name['validator']._options = None
    _EVIDENCE.fields_by_name['validator']._serialized_options = b'\xc8\xde\x1f\x00'
    _EVIDENCE.fields_by_name['time']._options = None
    _EVIDENCE.fields_by_name['time']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _globals['_CHECKTXTYPE']._serialized_start = 6371
    _globals['_CHECKTXTYPE']._serialized_end = 6428
    _globals['_EVIDENCETYPE']._serialized_start = 6430
    _globals['_EVIDENCETYPE']._serialized_end = 6502
    _globals['_REQUEST']._serialized_start = 226
    _globals['_REQUEST']._serialized_end = 1100
    _globals['_REQUESTECHO']._serialized_start = 1102
    _globals['_REQUESTECHO']._serialized_end = 1132
    _globals['_REQUESTFLUSH']._serialized_start = 1134
    _globals['_REQUESTFLUSH']._serialized_end = 1148
    _globals['_REQUESTINFO']._serialized_start = 1150
    _globals['_REQUESTINFO']._serialized_end = 1224
    _globals['_REQUESTSETOPTION']._serialized_start = 1226
    _globals['_REQUESTSETOPTION']._serialized_end = 1272
    _globals['_REQUESTINITCHAIN']._serialized_start = 1275
    _globals['_REQUESTINITCHAIN']._serialized_end = 1532
    _globals['_REQUESTQUERY']._serialized_start = 1534
    _globals['_REQUESTQUERY']._serialized_end = 1607
    _globals['_REQUESTBEGINBLOCK']._serialized_start = 1610
    _globals['_REQUESTBEGINBLOCK']._serialized_end = 1819
    _globals['_REQUESTCHECKTX']._serialized_start = 1821
    _globals['_REQUESTCHECKTX']._serialized_end = 1893
    _globals['_REQUESTDELIVERTX']._serialized_start = 1895
    _globals['_REQUESTDELIVERTX']._serialized_end = 1925
    _globals['_REQUESTENDBLOCK']._serialized_start = 1927
    _globals['_REQUESTENDBLOCK']._serialized_end = 1960
    _globals['_REQUESTCOMMIT']._serialized_start = 1962
    _globals['_REQUESTCOMMIT']._serialized_end = 1977
    _globals['_REQUESTLISTSNAPSHOTS']._serialized_start = 1979
    _globals['_REQUESTLISTSNAPSHOTS']._serialized_end = 2001
    _globals['_REQUESTOFFERSNAPSHOT']._serialized_start = 2003
    _globals['_REQUESTOFFERSNAPSHOT']._serialized_end = 2088
    _globals['_REQUESTLOADSNAPSHOTCHUNK']._serialized_start = 2090
    _globals['_REQUESTLOADSNAPSHOTCHUNK']._serialized_end = 2163
    _globals['_REQUESTAPPLYSNAPSHOTCHUNK']._serialized_start = 2165
    _globals['_REQUESTAPPLYSNAPSHOTCHUNK']._serialized_end = 2238
    _globals['_RESPONSE']._serialized_start = 2241
    _globals['_RESPONSE']._serialized_end = 3188
    _globals['_RESPONSEEXCEPTION']._serialized_start = 3190
    _globals['_RESPONSEEXCEPTION']._serialized_end = 3224
    _globals['_RESPONSEECHO']._serialized_start = 3226
    _globals['_RESPONSEECHO']._serialized_end = 3257
    _globals['_RESPONSEFLUSH']._serialized_start = 3259
    _globals['_RESPONSEFLUSH']._serialized_end = 3274
    _globals['_RESPONSEINFO']._serialized_start = 3276
    _globals['_RESPONSEINFO']._serialized_end = 3398
    _globals['_RESPONSESETOPTION']._serialized_start = 3400
    _globals['_RESPONSESETOPTION']._serialized_end = 3460
    _globals['_RESPONSEINITCHAIN']._serialized_start = 3463
    _globals['_RESPONSEINITCHAIN']._serialized_end = 3620
    _globals['_RESPONSEQUERY']._serialized_start = 3623
    _globals['_RESPONSEQUERY']._serialized_end = 3805
    _globals['_RESPONSEBEGINBLOCK']._serialized_start = 3807
    _globals['_RESPONSEBEGINBLOCK']._serialized_end = 3893
    _globals['_RESPONSECHECKTX']._serialized_start = 3896
    _globals['_RESPONSECHECKTX']._serialized_end = 4170
    _globals['_RESPONSEDELIVERTX']._serialized_start = 4173
    _globals['_RESPONSEDELIVERTX']._serialized_end = 4392
    _globals['_RESPONSEENDBLOCK']._serialized_start = 4395
    _globals['_RESPONSEENDBLOCK']._serialized_end = 4613
    _globals['_RESPONSECOMMIT']._serialized_start = 4615
    _globals['_RESPONSECOMMIT']._serialized_end = 4668
    _globals['_RESPONSELISTSNAPSHOTS']._serialized_start = 4670
    _globals['_RESPONSELISTSNAPSHOTS']._serialized_end = 4739
    _globals['_RESPONSEOFFERSNAPSHOT']._serialized_start = 4742
    _globals['_RESPONSEOFFERSNAPSHOT']._serialized_end = 4924
    _globals['_RESPONSEOFFERSNAPSHOT_RESULT']._serialized_start = 4830
    _globals['_RESPONSEOFFERSNAPSHOT_RESULT']._serialized_end = 4924
    _globals['_RESPONSELOADSNAPSHOTCHUNK']._serialized_start = 4926
    _globals['_RESPONSELOADSNAPSHOTCHUNK']._serialized_end = 4968
    _globals['_RESPONSEAPPLYSNAPSHOTCHUNK']._serialized_start = 4971
    _globals['_RESPONSEAPPLYSNAPSHOTCHUNK']._serialized_end = 5213
    _globals['_RESPONSEAPPLYSNAPSHOTCHUNK_RESULT']._serialized_start = 5117
    _globals['_RESPONSEAPPLYSNAPSHOTCHUNK_RESULT']._serialized_end = 5213
    _globals['_CONSENSUSPARAMS']._serialized_start = 5216
    _globals['_CONSENSUSPARAMS']._serialized_end = 5434
    _globals['_BLOCKPARAMS']._serialized_start = 5436
    _globals['_BLOCKPARAMS']._serialized_end = 5485
    _globals['_LASTCOMMITINFO']._serialized_start = 5487
    _globals['_LASTCOMMITINFO']._serialized_end = 5566
    _globals['_EVENT']._serialized_start = 5568
    _globals['_EVENT']._serialized_end = 5672
    _globals['_EVENTATTRIBUTE']._serialized_start = 5674
    _globals['_EVENTATTRIBUTE']._serialized_end = 5733
    _globals['_TXRESULT']._serialized_start = 5735
    _globals['_TXRESULT']._serialized_end = 5846
    _globals['_VALIDATOR']._serialized_start = 5848
    _globals['_VALIDATOR']._serialized_end = 5891
    _globals['_VALIDATORUPDATE']._serialized_start = 5893
    _globals['_VALIDATORUPDATE']._serialized_end = 5978
    _globals['_VOTEINFO']._serialized_start = 5980
    _globals['_VOTEINFO']._serialized_end = 6070
    _globals['_EVIDENCE']._serialized_start = 6073
    _globals['_EVIDENCE']._serialized_end = 6277
    _globals['_SNAPSHOT']._serialized_start = 6279
    _globals['_SNAPSHOT']._serialized_end = 6369
    _globals['_ABCIAPPLICATION']._serialized_start = 6505
    _globals['_ABCIAPPLICATION']._serialized_end = 7788