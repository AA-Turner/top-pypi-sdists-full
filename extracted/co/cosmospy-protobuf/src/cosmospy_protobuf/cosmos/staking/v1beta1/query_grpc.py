import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import cosmos
from .... import gogoproto
from .... import google

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Validators(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryValidatorsRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Validator(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryValidatorRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ValidatorDelegations(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryValidatorDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorDelegationsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ValidatorUnbondingDelegations(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryValidatorUnbondingDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorUnbondingDelegationsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Delegation(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryDelegationRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegationResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UnbondingDelegation(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryUnbondingDelegationRequest, cosmos.staking.v1beta1.query_pb2.QueryUnbondingDelegationResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DelegatorDelegations(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryDelegatorDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorDelegationsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DelegatorUnbondingDelegations(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryDelegatorUnbondingDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorUnbondingDelegationsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Redelegations(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryRedelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryRedelegationsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DelegatorValidators(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorsRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DelegatorValidator(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorResponse]') -> None:
        pass

    @abc.abstractmethod
    async def HistoricalInfo(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryHistoricalInfoRequest, cosmos.staking.v1beta1.query_pb2.QueryHistoricalInfoResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Pool(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryPoolRequest, cosmos.staking.v1beta1.query_pb2.QueryPoolResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryParamsRequest, cosmos.staking.v1beta1.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TokenizeShareRecordById(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByIdRequest, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByIdResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TokenizeShareRecordByDenom(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByDenomRequest, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TokenizeShareRecordsOwned(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordsOwnedRequest, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordsOwnedResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AllTokenizeShareRecords(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryAllTokenizeShareRecordsRequest, cosmos.staking.v1beta1.query_pb2.QueryAllTokenizeShareRecordsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LastTokenizeShareRecordId(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryLastTokenizeShareRecordIdRequest, cosmos.staking.v1beta1.query_pb2.QueryLastTokenizeShareRecordIdResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalTokenizeSharedAssets(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryTotalTokenizeSharedAssetsRequest, cosmos.staking.v1beta1.query_pb2.QueryTotalTokenizeSharedAssetsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalLiquidStaked(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryTotalLiquidStaked, cosmos.staking.v1beta1.query_pb2.QueryTotalLiquidStakedResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TokenizeShareLockInfo(self, stream: 'grpclib.server.Stream[cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareLockInfo, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareLockInfoResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/cosmos.staking.v1beta1.Query/Validators': grpclib.const.Handler(self.Validators, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryValidatorsRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorsResponse), '/cosmos.staking.v1beta1.Query/Validator': grpclib.const.Handler(self.Validator, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryValidatorRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorResponse), '/cosmos.staking.v1beta1.Query/ValidatorDelegations': grpclib.const.Handler(self.ValidatorDelegations, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryValidatorDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorDelegationsResponse), '/cosmos.staking.v1beta1.Query/ValidatorUnbondingDelegations': grpclib.const.Handler(self.ValidatorUnbondingDelegations, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryValidatorUnbondingDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorUnbondingDelegationsResponse), '/cosmos.staking.v1beta1.Query/Delegation': grpclib.const.Handler(self.Delegation, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryDelegationRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegationResponse), '/cosmos.staking.v1beta1.Query/UnbondingDelegation': grpclib.const.Handler(self.UnbondingDelegation, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryUnbondingDelegationRequest, cosmos.staking.v1beta1.query_pb2.QueryUnbondingDelegationResponse), '/cosmos.staking.v1beta1.Query/DelegatorDelegations': grpclib.const.Handler(self.DelegatorDelegations, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryDelegatorDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorDelegationsResponse), '/cosmos.staking.v1beta1.Query/DelegatorUnbondingDelegations': grpclib.const.Handler(self.DelegatorUnbondingDelegations, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryDelegatorUnbondingDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorUnbondingDelegationsResponse), '/cosmos.staking.v1beta1.Query/Redelegations': grpclib.const.Handler(self.Redelegations, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryRedelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryRedelegationsResponse), '/cosmos.staking.v1beta1.Query/DelegatorValidators': grpclib.const.Handler(self.DelegatorValidators, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorsRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorsResponse), '/cosmos.staking.v1beta1.Query/DelegatorValidator': grpclib.const.Handler(self.DelegatorValidator, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorResponse), '/cosmos.staking.v1beta1.Query/HistoricalInfo': grpclib.const.Handler(self.HistoricalInfo, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryHistoricalInfoRequest, cosmos.staking.v1beta1.query_pb2.QueryHistoricalInfoResponse), '/cosmos.staking.v1beta1.Query/Pool': grpclib.const.Handler(self.Pool, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryPoolRequest, cosmos.staking.v1beta1.query_pb2.QueryPoolResponse), '/cosmos.staking.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryParamsRequest, cosmos.staking.v1beta1.query_pb2.QueryParamsResponse), '/cosmos.staking.v1beta1.Query/TokenizeShareRecordById': grpclib.const.Handler(self.TokenizeShareRecordById, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByIdRequest, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByIdResponse), '/cosmos.staking.v1beta1.Query/TokenizeShareRecordByDenom': grpclib.const.Handler(self.TokenizeShareRecordByDenom, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByDenomRequest, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByDenomResponse), '/cosmos.staking.v1beta1.Query/TokenizeShareRecordsOwned': grpclib.const.Handler(self.TokenizeShareRecordsOwned, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordsOwnedRequest, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordsOwnedResponse), '/cosmos.staking.v1beta1.Query/AllTokenizeShareRecords': grpclib.const.Handler(self.AllTokenizeShareRecords, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryAllTokenizeShareRecordsRequest, cosmos.staking.v1beta1.query_pb2.QueryAllTokenizeShareRecordsResponse), '/cosmos.staking.v1beta1.Query/LastTokenizeShareRecordId': grpclib.const.Handler(self.LastTokenizeShareRecordId, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryLastTokenizeShareRecordIdRequest, cosmos.staking.v1beta1.query_pb2.QueryLastTokenizeShareRecordIdResponse), '/cosmos.staking.v1beta1.Query/TotalTokenizeSharedAssets': grpclib.const.Handler(self.TotalTokenizeSharedAssets, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryTotalTokenizeSharedAssetsRequest, cosmos.staking.v1beta1.query_pb2.QueryTotalTokenizeSharedAssetsResponse), '/cosmos.staking.v1beta1.Query/TotalLiquidStaked': grpclib.const.Handler(self.TotalLiquidStaked, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryTotalLiquidStaked, cosmos.staking.v1beta1.query_pb2.QueryTotalLiquidStakedResponse), '/cosmos.staking.v1beta1.Query/TokenizeShareLockInfo': grpclib.const.Handler(self.TokenizeShareLockInfo, grpclib.const.Cardinality.UNARY_UNARY, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareLockInfo, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareLockInfoResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Validators = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/Validators', cosmos.staking.v1beta1.query_pb2.QueryValidatorsRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorsResponse)
        self.Validator = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/Validator', cosmos.staking.v1beta1.query_pb2.QueryValidatorRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorResponse)
        self.ValidatorDelegations = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/ValidatorDelegations', cosmos.staking.v1beta1.query_pb2.QueryValidatorDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorDelegationsResponse)
        self.ValidatorUnbondingDelegations = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/ValidatorUnbondingDelegations', cosmos.staking.v1beta1.query_pb2.QueryValidatorUnbondingDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryValidatorUnbondingDelegationsResponse)
        self.Delegation = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/Delegation', cosmos.staking.v1beta1.query_pb2.QueryDelegationRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegationResponse)
        self.UnbondingDelegation = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/UnbondingDelegation', cosmos.staking.v1beta1.query_pb2.QueryUnbondingDelegationRequest, cosmos.staking.v1beta1.query_pb2.QueryUnbondingDelegationResponse)
        self.DelegatorDelegations = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/DelegatorDelegations', cosmos.staking.v1beta1.query_pb2.QueryDelegatorDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorDelegationsResponse)
        self.DelegatorUnbondingDelegations = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/DelegatorUnbondingDelegations', cosmos.staking.v1beta1.query_pb2.QueryDelegatorUnbondingDelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorUnbondingDelegationsResponse)
        self.Redelegations = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/Redelegations', cosmos.staking.v1beta1.query_pb2.QueryRedelegationsRequest, cosmos.staking.v1beta1.query_pb2.QueryRedelegationsResponse)
        self.DelegatorValidators = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/DelegatorValidators', cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorsRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorsResponse)
        self.DelegatorValidator = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/DelegatorValidator', cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorRequest, cosmos.staking.v1beta1.query_pb2.QueryDelegatorValidatorResponse)
        self.HistoricalInfo = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/HistoricalInfo', cosmos.staking.v1beta1.query_pb2.QueryHistoricalInfoRequest, cosmos.staking.v1beta1.query_pb2.QueryHistoricalInfoResponse)
        self.Pool = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/Pool', cosmos.staking.v1beta1.query_pb2.QueryPoolRequest, cosmos.staking.v1beta1.query_pb2.QueryPoolResponse)
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/Params', cosmos.staking.v1beta1.query_pb2.QueryParamsRequest, cosmos.staking.v1beta1.query_pb2.QueryParamsResponse)
        self.TokenizeShareRecordById = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/TokenizeShareRecordById', cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByIdRequest, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByIdResponse)
        self.TokenizeShareRecordByDenom = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/TokenizeShareRecordByDenom', cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByDenomRequest, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordByDenomResponse)
        self.TokenizeShareRecordsOwned = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/TokenizeShareRecordsOwned', cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordsOwnedRequest, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareRecordsOwnedResponse)
        self.AllTokenizeShareRecords = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/AllTokenizeShareRecords', cosmos.staking.v1beta1.query_pb2.QueryAllTokenizeShareRecordsRequest, cosmos.staking.v1beta1.query_pb2.QueryAllTokenizeShareRecordsResponse)
        self.LastTokenizeShareRecordId = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/LastTokenizeShareRecordId', cosmos.staking.v1beta1.query_pb2.QueryLastTokenizeShareRecordIdRequest, cosmos.staking.v1beta1.query_pb2.QueryLastTokenizeShareRecordIdResponse)
        self.TotalTokenizeSharedAssets = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/TotalTokenizeSharedAssets', cosmos.staking.v1beta1.query_pb2.QueryTotalTokenizeSharedAssetsRequest, cosmos.staking.v1beta1.query_pb2.QueryTotalTokenizeSharedAssetsResponse)
        self.TotalLiquidStaked = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/TotalLiquidStaked', cosmos.staking.v1beta1.query_pb2.QueryTotalLiquidStaked, cosmos.staking.v1beta1.query_pb2.QueryTotalLiquidStakedResponse)
        self.TokenizeShareLockInfo = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.staking.v1beta1.Query/TokenizeShareLockInfo', cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareLockInfo, cosmos.staking.v1beta1.query_pb2.QueryTokenizeShareLockInfoResponse)