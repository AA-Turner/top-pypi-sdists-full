# -*- coding: utf-8 -*-
"""
    Quote query
"""

from .quote_stockfilter_info import *
from .quote_option_event_info import *
from .quote_get_warrant import *
from ..common.err import make_wrong_type_msg

# 无数据时的值
NoneDataType = 'N/A'


def get_optional_from_pb(pb, field_name, conv=None):
    if pb.HasField(field_name):
        val = getattr(pb, field_name)
        if conv:
            val = conv(val)
        return val
    return NoneDataType


def set_item_from_pb(item, pb, field_map):
    for python_name, pb_name, is_required, conv in field_map:
        exist_val = item.get(python_name, None)
        if exist_val is not None and exist_val != NoneDataType:
            continue
        if is_required:
            val = getattr(pb, pb_name)
            if conv:
                val = conv(val)
            item[python_name] = val
        else:
            item[python_name] = get_optional_from_pb(pb, pb_name, conv)


def set_item_none(item, field_map):
    for row in field_map:
        exist_val = item.get(row[0], None)
        if exist_val is None or exist_val == NoneDataType:
            item[row[0]] = NoneDataType


def _enum_or_int(enum_cls, value, name):
    """
    兼容枚举字符串或数值的入参转换。
    :param enum_cls: FtEnum 子类
    :param value:    枚举字符串 / 枚举成员 / 数值 / None
    :param name:     参数名（用于错误提示）
    :return: 数值（None 保持 None）；参数非法时返回 (RET_ERROR, error_str, None, 0, 0)
    """
    if value is None:
        return None
    if isinstance(value, str):
        if not enum_cls.if_has_key(value):
            error_str = ERROR_STR_PREFIX + "%s is %s, which is not valid. (%s)" \
                % (name, value, enum_cls.get_all_keys())
            return RET_ERROR, error_str, None, 0, 0
        _, num = enum_cls.to_number(value)
        return num
    return value


def conv_pb_security_to_code(security):
    return merge_qot_mkt_stock_str(security.market, security.code)

def merge_pb_cnipoexdata_winningnumdata(winningnumdata):
    data = ''
    for item in winningnumdata:
        if data == '':
            data = item.winningName + ":" + item.winningInfo
        else:
            data = data + '\n' + item.winningName + ":" + item.winningInfo

    data = data.rstrip()
    return data


def set_qot_header(req, security_firm):
    """设置行情请求的公共参数头
    :param req: protobuf请求对象
    :param security_firm: 券商标识，SecurityFirm枚举值
    """
    if security_firm is not None:
        ret, firm_num = SecurityFirm.to_number(security_firm)
        if ret:
            req.c2s.header.securityFirm = firm_num


# python_name, pb_name, is_required, conv_func
pb_field_map_OptionBasicQotExData = [
    ('strike_price', 'strikePrice', True, None),
    ('contract_size', 'contractSizeFloat', True, None),
    ('open_interest', 'openInterest', True, None),
    ('implied_volatility', 'impliedVolatility', True, None),
    ('premium', 'premium', True, None),
    ('delta', 'delta', True, None),
    ('gamma', 'gamma', True, None),
    ('vega', 'vega', True, None),
    ('theta', 'theta', True, None),
    ('rho', 'rho', True, None),
    ('net_open_interest', 'netOpenInterest', False, None),
    ('expiry_date_distance', 'expiryDateDistance', False, None),
    ('contract_nominal_value', 'contractNominalValue', False, None),
    ('owner_lot_multiplier', 'ownerLotMultiplier', False, None),
    ('option_area_type', 'optionAreaType', False, OptionAreaType.to_string2), # 初始化枚举类型
    ('contract_multiplier', 'contractMultiplier', False, None),
    ('index_option_type', 'indexOptionType', False, IndexOptionType.to_string2), # 初始化枚举类型
]

pb_field_map_FutureBasicQotExData = [
    ('last_settle_price', 'lastSettlePrice', True, None),
    ('position', 'position', True, None),
    ('position_change', 'positionChange', True, None),
    ('expiry_date_distance', 'expiryDateDistance', False, None),
]

pb_field_map_PreAfterMarketData_pre = [
    ("pre_price", "price", False, None),
    ("pre_high_price", "highPrice", False, None),
    ("pre_low_price", "lowPrice", False, None),
    ("pre_volume", "volume", False, None),
    ("pre_turnover", "turnover", False, None),
    ("pre_change_val", "changeVal", False, None),
    ("pre_change_rate", "changeRate", False, None),
    ("pre_amplitude", "amplitude", False, None),
]

pb_field_map_PreAfterMarketData_after = [
    ("after_price", "price", False, None),
    ("after_high_price", "highPrice", False, None),
    ("after_low_price", "lowPrice", False, None),
    ("after_volume", "volume", False, None),
    ("after_turnover", "turnover", False, None),
    ("after_change_val", "changeVal", False, None),
    ("after_change_rate", "changeRate", False, None),
    ("after_amplitude", "amplitude", False, None),
]

pb_field_map_PreAfterMarketData_overnight = [
    ("overnight_price", "price", False, None),
    ("overnight_high_price", "highPrice", False, None),
    ("overnight_low_price", "lowPrice", False, None),
    ("overnight_volume", "volume", False, None),
    ("overnight_turnover", "turnover", False, None),
    ("overnight_change_val", "changeVal", False, None),
    ("overnight_change_rate", "changeRate", False, None),
    ("overnight_amplitude", "amplitude", False, None),
]

pb_field_map_BasicIpoData = [
    ("code", "security", True, conv_pb_security_to_code),
    ("name", "name", True, None),
    ("list_time", "listTime", False, None),
    ("list_timestamp", "listTimestamp", False, None),
]

pb_field_map_CNIpoExData = [
    ("apply_code", "applyCode", True, None),
    ("issue_size", "issueSize", True, None),
    ("online_issue_size", "onlineIssueSize", True, None),
    ("apply_upper_limit", "applyUpperLimit", True, None),
    ("apply_limit_market_value", "applyLimitMarketValue", True, None),
    ("is_estimate_ipo_price", "isEstimateIpoPrice", True, None),
    ("ipo_price", "ipoPrice", True, None),
    ("industry_pe_rate", "industryPeRate", True, None),
    ("is_estimate_winning_ratio", "isEstimateWinningRatio", True, None),
    ("winning_ratio", "winningRatio", True, None),
    ("issue_pe_rate", "issuePeRate", True, None),
    ("apply_time", "applyTime", False, None),
    ("apply_timestamp", "applyTimestamp", False, None),
    ("winning_time", "winningTime", False, None),
    ("winning_timestamp", "winningTimestamp", False, None),
    ("is_has_won", "isHasWon", True, None),
    ("winning_num_data", "winningNumData", True, merge_pb_cnipoexdata_winningnumdata),
]

pb_field_map_HKIpoExData = [
    ("ipo_price_min", "ipoPriceMin", True, None),
    ("ipo_price_max", "ipoPriceMax", True, None),
    ("list_price", "listPrice", True, None),
    ("lot_size", "lotSize", True, None),
    ("entrance_price", "entrancePrice", True, None),
    ("is_subscribe_status", "isSubscribeStatus", True, None),
    ("apply_end_time", "applyEndTime", False, None),
    ("apply_end_timestamp", "applyEndTimestamp", False, None),
]

pb_field_map_USIpoExData = [
    ("ipo_price_min", "ipoPriceMin", True, None),
    ("ipo_price_max", "ipoPriceMax", True, None),
    ("issue_size", "issueSize", True, None)
]

pb_field_map_SGIpoExData = [
    ("ipo_price_min", "ipoPriceMin", True, None),
    ("ipo_price_max", "ipoPriceMax", True, None),
    ("issue_size", "issueSize", True, None),
    ("apply_start_time", "applyStartTime", False, None),
    ("apply_start_timestamp", "applyStartTimestamp", False, None),
    ("apply_end_time", "applyEndTime", False, None),
    ("apply_end_timestamp", "applyEndTimestamp", False, None),
    ("winning_time", "winningTime", False, None),
    ("winning_timestamp", "winningTimestamp", False, None),
]

pb_field_map_MYIpoExData = [
    ("offer_price", "offerPrice", True, None),
    ("issue_size", "issueSize", True, None),
    ("apply_start_time", "applyStartTime", False, None),
    ("apply_start_timestamp", "applyStartTimestamp", False, None),
    ("apply_end_time", "applyEndTime", False, None),
    ("apply_end_timestamp", "applyEndTimestamp", False, None),
    ("winning_time", "winningTime", False, None),
    ("winning_timestamp", "winningTimestamp", False, None),
]

pb_field_map_JPIpoExData = [
    ("ipo_price_min", "ipoPriceMin", True, None),
    ("ipo_price_max", "ipoPriceMax", True, None),
    ("issue_size", "issueSize", True, None),
]

class OptionStrategyLeg(object):
    def __init__(self):
        self.code = None
        self.action = None
        self.quantity = None

    def __repr__(self):
        return "OptionStrategyLeg(code={}, action={}, quantity={})".format(self.code, self.action, self.quantity)

class InitConnect:
    """
    A InitConnect request must be sent first
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, client_ver, client_id, recv_notify, is_encrypt, push_proto_fmt, ai_type=0):

        from ..common.pb.InitConnect_pb2 import Request
        req = Request()
        req.c2s.clientVer = client_ver
        req.c2s.clientID = client_id
        req.c2s.recvNotify = recv_notify
        req.c2s.pushProtoFmt = push_proto_fmt
        req.c2s.programmingLanguage = 'Python'
        req.c2s.aiType = ai_type

        if is_encrypt:
            req.c2s.packetEncAlgo = Common_pb2.PacketEncAlgo_AES_CBC
        else:
            req.c2s.packetEncAlgo = Common_pb2.PacketEncAlgo_None

        return pack_pb_req(req, ProtoId.InitConnect, 0)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Unpack the init connect response"""
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        res = {}
        if rsp_pb.HasField('s2c'):
            res['server_version'] = rsp_pb.s2c.serverVer
            res['login_user_id'] = rsp_pb.s2c.loginUserID
            res['conn_id'] = rsp_pb.s2c.connID
            res['conn_key'] = rsp_pb.s2c.connAESKey
            res['conn_iv'] = rsp_pb.s2c.aesCBCiv if rsp_pb.s2c.HasField('aesCBCiv') else None
            res['keep_alive_interval'] = rsp_pb.s2c.keepAliveInterval
        else:
            return RET_ERROR, "rsp_pb error", None

        return RET_OK, "", res
class RequestTradeDayQuery:
    """
    Query Conversion for getting trading days.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, conn_id, start_date=None, end_date=None, code=None, security_firm=SecurityFirm.NONE):

        # '''Parameter check'''
        r, v = TradeDateMarket.to_number(market)
        if not r:
            error_str = ERROR_STR_PREFIX + " market is %s, which is not valid." \
                                           % (market)
            return RET_ERROR, error_str, None, 0, 0

        if start_date is None: # start为往前365天
            today = datetime.today()
            start = today - timedelta(days=365)

            start_date = start.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(start_date)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            start_date = msg

        if end_date is None: # end为当前时间
            today = datetime.today()
            end_date = today.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(end_date)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            end_date = msg

        """check stock_code 股票"""
        market_code = None
        stock_code = None
        if code is not None:
            ret, content = split_stock_str(code)
            if ret == RET_ERROR:
                error_str = content
                return RET_ERROR, error_str, None, 0, 0
            market_code, stock_code = content

        # pack to json
        from ..common.pb.Qot_RequestTradeDate_pb2 import Request
        req = Request()
        req.c2s.market = v
        req.c2s.beginTime = start_date
        req.c2s.endTime = end_date
        if market_code is not None:
            req.c2s.security.market = market_code
        if stock_code is not None:
            req.c2s.security.code = stock_code
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_RequestTradeDate, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        # response check and unpack response json to objects
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        raw_trading_day_list = rsp_pb.s2c.tradeDateList
        trading_day_list = list()

        for x in raw_trading_day_list:
            if x.time is not None and len(x.time) > 0:
                trading_day_list.append(
                    {"time": x.time, "trade_date_type": TradeDateType.to_string2(x.tradeDateType)})

        return RET_OK, "", trading_day_list

class StockBasicInfoQuery:
    """
    Query Conversion for getting stock basic information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, conn_id, stock_type='STOCK', code_list=None, security_firm=SecurityFirm.NONE):
        query_code = code_list is not None and len(code_list) > 0
        if not query_code:
            if not Market.if_has_key(market):
                error_str = ERROR_STR_PREFIX + " market is %s, which is not valid. (%s)" \
                                               % (market, Market.get_all_keys())
                return RET_ERROR, error_str, None, 0, 0

            if not SecurityType.if_has_key(stock_type) and code_list is None:
                error_str = ERROR_STR_PREFIX + " stock_type is %s, which is not valid. (%s)" \
                                               % (stock_type, SecurityType.get_all_keys())
                return RET_ERROR, error_str, None, 0, 0

        from ..common.pb.Qot_GetStaticInfo_pb2 import Request
        req = Request()
        if query_code:
            req.c2s.market = 0
            req.c2s.secType = 0
            for code in code_list:
                sec = req.c2s.securityList.add()
                ret, data = split_stock_str(code)
                if ret == RET_OK:
                    sec.market, sec.code = data
                else:
                    return RET_ERROR, data, None, 0, 0
        else:
            _, req.c2s.market = Market.to_number(market)
            _, req.c2s.secType = SecurityType.to_number(stock_type)
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetStaticInfo, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        raw_basic_info_list = rsp_pb.s2c.staticInfoList
        basic_info_list = [{
            "code": merge_qot_mkt_stock_str(record.basic.security.market,
                                            record.basic.security.code),
            "stock_id": record.basic.id,
            "name": record.basic.name,
            "lot_size": record.basic.lotSize,
            "stock_type": SecurityType.to_string2(record.basic.secType) if record.basic.HasField('secType') else 'N/A',# 初始化枚举类型
            "stock_child_type": WrtType.to_string2(record.warrantExData.type)if record.warrantExData.HasField('type') else 'N/A',# 初始化枚举类型
            "stock_owner":merge_qot_mkt_stock_str(
                record.warrantExData.owner.market,
                record.warrantExData.owner.code) if record.HasField('warrantExData') else (
                merge_qot_mkt_stock_str(
                    record.optionExData.owner.market,
                    record.optionExData.owner.code) if record.HasField('optionExData')
                else ""),
            "listing_date": "N/A" if record.HasField('optionExData') else record.basic.listTime,
            "option_type": OptionType.to_string2(record.optionExData.type) if record.HasField('optionExData') else 'N/A',# 初始化枚举类型
            "strike_time": record.optionExData.strikeTime,
            "strike_price": record.optionExData.strikePrice if record.HasField('optionExData') else NoneDataType,
            "suspension": record.optionExData.suspend if record.HasField('optionExData') else NoneDataType,
            "delisting": record.basic.delisting if record.basic.HasField('delisting') else NoneDataType,
            "index_option_type": IndexOptionType.to_string2(record.optionExData.indexOptionType) if record.HasField('optionExData') else NoneDataType,
            "main_contract": record.futureExData.isMainContract,
            "last_trade_time": record.futureExData.lastTradeTime,
            'exchange_type': ExchType.to_string2(record.basic.exchType) if record.basic.HasField('exchType') else 'N/A',# 初始化枚举类型
        } for record in raw_basic_info_list]
        return RET_OK, "", basic_info_list


class MarketSnapshotQuery:
    """
    Query Conversion for getting market snapshot.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, stock_list, conn_id, security_firm=SecurityFirm.NONE):
        """Convert from user request for trading days to PLS request"""
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in stock_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue

            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None, ProtoId.Qot_GetSecuritySnapshot, 0

        from ..common.pb.Qot_GetSecuritySnapshot_pb2 import Request
        req = Request()
        for market, code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market
            stock_inst.code = code
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetSecuritySnapshot, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        raw_snapshot_list = rsp_pb.s2c.snapshotList

        snapshot_list = []
        for record in raw_snapshot_list:
            snapshot_tmp = {}
            snapshot_tmp['code'] = merge_qot_mkt_stock_str(
                int(record.basic.security.market), record.basic.security.code)
            snapshot_tmp['name'] = record.basic.name if record.basic.HasField('name') else 'N/A'
            snapshot_tmp['update_time'] = record.basic.updateTime
            snapshot_tmp['last_price'] = record.basic.curPrice
            snapshot_tmp['open_price'] = record.basic.openPrice
            snapshot_tmp['high_price'] = record.basic.highPrice
            snapshot_tmp['low_price'] = record.basic.lowPrice
            snapshot_tmp['prev_close_price'] = record.basic.lastClosePrice

            # 成交量：优先使用高精度字段 hpVolume，如果没有则使用 volume
            if record.basic.HasField('hpVolume'):
                snapshot_tmp['volume'] = record.basic.hpVolume
            else:
                snapshot_tmp['volume'] = record.basic.volume

            snapshot_tmp['turnover'] = record.basic.turnover
            snapshot_tmp['turnover_rate'] = record.basic.turnoverRate
            snapshot_tmp['suspension'] = record.basic.isSuspend
            snapshot_tmp['listing_date'] = "N/A" if record.HasField(
                'optionExData') else record.basic.listTime
            snapshot_tmp['price_spread'] = record.basic.priceSpread
            snapshot_tmp['lot_size'] = record.basic.lotSize
            snapshot_tmp['ask_price'] = record.basic.askPrice if record.basic.HasField('askPrice') else 'N/A'
            snapshot_tmp['bid_price'] = record.basic.bidPrice if record.basic.HasField('bidPrice') else 'N/A'

            # 卖量：优先使用高精度字段 hpAskVol，如果没有则使用 askVol
            if record.basic.HasField('hpAskVol'):
                snapshot_tmp['ask_vol'] = record.basic.hpAskVol
            elif record.basic.HasField('askVol'):
                snapshot_tmp['ask_vol'] = record.basic.askVol
            else:
                snapshot_tmp['ask_vol'] = 'N/A'

            # 买量：优先使用高精度字段 hpBidVol，如果没有则使用 bidVol
            if record.basic.HasField('hpBidVol'):
                snapshot_tmp['bid_vol'] = record.basic.hpBidVol
            elif record.basic.HasField('bidVol'):
                snapshot_tmp['bid_vol'] = record.basic.bidVol
            else:
                snapshot_tmp['bid_vol'] = 'N/A'

            # 窝轮 统一对枚举类型，初始化
            snapshot_tmp['wrt_type'] = WrtType.to_string2(
                record.warrantExData.warrantType) if record.warrantExData.HasField('warrantType') else 'N/A'# 初始化枚举类型
            #  界内界外，仅界内证支持该字段 type=double
            snapshot_tmp["wrt_inline_price_status"] = PriceType.to_string2(
                record.warrantExData.inLinePriceStatus) if record.warrantExData.HasField('inLinePriceStatus') else 'N/A'# 初始化枚举类型

            # 期权 统一对枚举类型，初始化
            snapshot_tmp['option_type'] = OptionType.to_string2(
                record.optionExData.type) if record.optionExData.HasField('type') else 'N/A'# 初始化枚举类型
            snapshot_tmp['index_option_type'] = IndexOptionType.to_string2(
                record.optionExData.indexOptionType) if record.optionExData.HasField('indexOptionType') else 'N/A'# 初始化枚举类型
            snapshot_tmp['option_area_type'] = OptionAreaType.to_string2(
                record.optionExData.optionAreaType) if record.optionExData.HasField('optionAreaType') else 'N/A'# 初始化枚举类型

            # 基金 统一对枚举类型，初始化
            snapshot_tmp['trust_assetClass'] = AssetClass.to_string2(record.trustExData.assetClass) if record.trustExData.HasField('assetClass') else 'N/A'# 初始化枚举类型

            # 2019.02.25 增加一批数据
            if record.basic.HasField("enableMargin"):
                # 是否可融资，如果为true，后两个字段才有意
                snapshot_tmp['enable_margin'] = record.basic.enableMargin
                if snapshot_tmp['enable_margin'] is True:
                    snapshot_tmp['mortgage_ratio'] = record.basic.mortgageRatio
                    snapshot_tmp['long_margin_initial_ratio'] = record.basic.longMarginInitialRatio
            if record.basic.HasField("enableShortSell"):
                # 是否可卖空，如果为true，后三个字段才有意义
                snapshot_tmp['enable_short_sell'] = record.basic.enableShortSell
                if snapshot_tmp['enable_short_sell'] is True:
                    snapshot_tmp['short_sell_rate'] = record.basic.shortSellRate
                    snapshot_tmp['short_available_volume'] = record.basic.shortAvailableVolume
                    snapshot_tmp['short_margin_initial_ratio'] = record.basic.shortMarginInitialRatio
            # 2019.05.10 增加一批数据================================
            #  振幅（该字段为百分比字段，默认不展示%） type=double
            snapshot_tmp["amplitude"] = record.basic.amplitude
            #  平均价 type=double
            snapshot_tmp["avg_price"] = record.basic.avgPrice
            #  委比（该字段为百分比字段，默认不展示%） type=double
            snapshot_tmp["bid_ask_ratio"] = record.basic.bidAskRatio
            #  量比 type=double
            snapshot_tmp["volume_ratio"] = record.basic.volumeRatio
            #  52周最高价 type=double
            snapshot_tmp["highest52weeks_price"] = record.basic.highest52WeeksPrice
            #  52周最低价 type=double
            snapshot_tmp["lowest52weeks_price"] = record.basic.lowest52WeeksPrice
            #  历史最高价 type=double
            snapshot_tmp["highest_history_price"] = record.basic.highestHistoryPrice
            #  历史最低价 type=double
            snapshot_tmp["lowest_history_price"] = record.basic.lowestHistoryPrice
            #  盘后成交量 type=int64
            snapshot_tmp["after_volume"] = record.basic.afterMarket.volume
            #  盘后成交额 type=double
            snapshot_tmp["after_turnover"] = record.basic.afterMarket.turnover   
            #  股票状态 type=str
            snapshot_tmp["sec_status"] = SecurityStatus.to_string2(record.basic.secStatus) if record.basic.HasField('secStatus') else 'N/A'# 初始化枚举类型
            #  5分组收盘价 type=double
            snapshot_tmp["close_price_5min"] = record.basic.closePrice5Minute

            if record.basic.HasField('preMarket'):
                set_item_from_pb(snapshot_tmp, record.basic.preMarket, pb_field_map_PreAfterMarketData_pre)
            else:
                set_item_none(snapshot_tmp, pb_field_map_PreAfterMarketData_pre)

            if record.basic.HasField('afterMarket'):
                set_item_from_pb(snapshot_tmp, record.basic.afterMarket, pb_field_map_PreAfterMarketData_after)
            else:
                set_item_none(snapshot_tmp, pb_field_map_PreAfterMarketData_after)

            if record.basic.HasField('overnight'):
                set_item_from_pb(snapshot_tmp, record.basic.overnight, pb_field_map_PreAfterMarketData_overnight)
            else:
                set_item_none(snapshot_tmp, pb_field_map_PreAfterMarketData_overnight)
            # ================================

            snapshot_tmp['equity_valid'] = False
            # equityExData
            if record.HasField('equityExData'):
                snapshot_tmp['equity_valid'] = True
                snapshot_tmp['issued_shares'] = record.equityExData.issuedShares
                snapshot_tmp['total_market_val'] = record.equityExData.issuedMarketVal
                snapshot_tmp['net_asset'] = record.equityExData.netAsset
                snapshot_tmp['net_profit'] = record.equityExData.netProfit
                snapshot_tmp['earning_per_share'] = record.equityExData.earningsPershare
                snapshot_tmp['outstanding_shares'] = record.equityExData.outstandingShares
                snapshot_tmp['circular_market_val'] = record.equityExData.outstandingMarketVal
                snapshot_tmp['net_asset_per_share'] = record.equityExData.netAssetPershare
                snapshot_tmp['ey_ratio'] = record.equityExData.eyRate
                snapshot_tmp['pe_ratio'] = record.equityExData.peRate
                snapshot_tmp['pb_ratio'] = record.equityExData.pbRate
                snapshot_tmp['pe_ttm_ratio'] = record.equityExData.peTTMRate
                snapshot_tmp["dividend_ttm"] = record.equityExData.dividendTTM
                #  股息率TTM（该字段为百分比字段，默认不展示%） type=double
                snapshot_tmp["dividend_ratio_ttm"] = record.equityExData.dividendRatioTTM
                #  股息LFY，上一年度派息 type=double
                snapshot_tmp["dividend_lfy"] = record.equityExData.dividendLFY
                #  股息率LFY（该字段为百分比字段，默认不展示%） type=double
                snapshot_tmp["dividend_lfy_ratio"] = record.equityExData.dividendLFYRatio

            snapshot_tmp['wrt_valid'] = False
            if SecurityType.to_string2(record.basic.type) == SecurityType.WARRANT:
                snapshot_tmp['wrt_valid'] = True
                snapshot_tmp['wrt_conversion_ratio'] = record.warrantExData.conversionRate
                snapshot_tmp['wrt_strike_price'] = record.warrantExData.strikePrice
                snapshot_tmp['wrt_maturity_date'] = record.warrantExData.maturityTime
                snapshot_tmp['wrt_end_trade'] = record.warrantExData.endTradeTime
                snapshot_tmp['stock_owner'] = merge_qot_mkt_stock_str(
                    record.warrantExData.owner.market,
                    record.warrantExData.owner.code)
                snapshot_tmp['wrt_recovery_price'] = record.warrantExData.recoveryPrice
                snapshot_tmp['wrt_street_vol'] = record.warrantExData.streetVolumn
                snapshot_tmp['wrt_issue_vol'] = record.warrantExData.issueVolumn
                snapshot_tmp['wrt_street_ratio'] = record.warrantExData.streetRate
                snapshot_tmp['wrt_delta'] = record.warrantExData.delta
                snapshot_tmp['wrt_implied_volatility'] = record.warrantExData.impliedVolatility
                snapshot_tmp['wrt_premium'] = record.warrantExData.premium
                #  杠杆比率（倍） type=double
                snapshot_tmp["wrt_leverage"] = record.warrantExData.leverage
                #  价内/价外（该字段为百分比字段，默认不展示%） type=double
                snapshot_tmp["wrt_ipop"] = record.warrantExData.ipop
                #  打和点 type=double
                snapshot_tmp["wrt_break_even_point"] = record.warrantExData.breakEvenPoint
                #  换股价 type=double
                snapshot_tmp["wrt_conversion_price"] = record.warrantExData.conversionPrice
                #  距收回价（该字段为百分比字段，默认不展示%） type=double
                snapshot_tmp["wrt_price_recovery_ratio"] = record.warrantExData.priceRecoveryRatio
                #  综合评分 type=double
                snapshot_tmp["wrt_score"] = record.warrantExData.score
                #  上限价，仅界内证支持该字段 type=double
                snapshot_tmp["wrt_upper_strike_price"] = record.warrantExData.upperStrikePrice
                #  下限价，仅界内证支持该字段 type=double
                snapshot_tmp["wrt_lower_strike_price"] = record.warrantExData.lowerStrikePrice
                snapshot_tmp["wrt_issuer_code"] = record.warrantExData.issuerCode

            snapshot_tmp['option_valid'] = False
            if SecurityType.to_string2(record.basic.type) == SecurityType.DRVT:
                snapshot_tmp['option_valid'] = True

                snapshot_tmp['stock_owner'] = merge_qot_mkt_stock_str(
                    record.optionExData.owner.market, record.optionExData.owner.code)
                snapshot_tmp['strike_time'] = record.optionExData.strikeTime
                snapshot_tmp['option_strike_price'] = record.optionExData.strikePrice
                snapshot_tmp['option_contract_size'] = record.optionExData.contractSizeFloat
                snapshot_tmp['option_open_interest'] = record.optionExData.openInterest
                snapshot_tmp['option_implied_volatility'] = record.optionExData.impliedVolatility
                snapshot_tmp['option_premium'] = record.optionExData.premium
                snapshot_tmp['option_delta'] = record.optionExData.delta
                snapshot_tmp['option_gamma'] = record.optionExData.gamma
                snapshot_tmp['option_vega'] = record.optionExData.vega
                snapshot_tmp['option_theta'] = record.optionExData.theta
                snapshot_tmp['option_rho'] = record.optionExData.rho
                snapshot_tmp['option_net_open_interest'] = record.optionExData.netOpenInterest if record.optionExData.HasField('netOpenInterest') else 'N/A'
                snapshot_tmp['option_expiry_date_distance'] = record.optionExData.expiryDateDistance if record.optionExData.HasField('expiryDateDistance') else 'N/A'
                snapshot_tmp['option_contract_nominal_value'] = record.optionExData.contractNominalValue if record.optionExData.HasField('contractNominalValue') else 'N/A'
                snapshot_tmp['option_owner_lot_multiplier'] = record.optionExData.ownerLotMultiplier if record.optionExData.HasField('ownerLotMultiplier') else 'N/A'
                snapshot_tmp['option_contract_multiplier'] = record.optionExData.contractMultiplier if record.optionExData.HasField('contractMultiplier') else 'N/A'

            snapshot_tmp['index_valid'] = False
            if record.HasField('indexExData'):
                snapshot_tmp['index_valid'] = True
                #  指数类型上涨支数 type=int32
                snapshot_tmp["index_raise_count"] = record.indexExData.raiseCount
                #  指数类型下跌支数 type=int32
                snapshot_tmp["index_fall_count"] = record.indexExData.fallCount
                #  指数类型平盘支数 type=int32
                snapshot_tmp["index_equal_count"] = record.indexExData.equalCount

            snapshot_tmp['plate_valid'] = False
            if record.HasField('plateExData'):
                snapshot_tmp['plate_valid'] = True
                #  板块类型上涨支数 type=int32
                snapshot_tmp["plate_raise_count"] = record.plateExData.raiseCount
                #  板块类型下跌支数 type=int32
                snapshot_tmp["plate_fall_count"] = record.plateExData.fallCount
                #  板块类型平盘支数 type=int32
                snapshot_tmp["plate_equal_count"] = record.plateExData.equalCount

            snapshot_tmp['future_valid'] = False
            if SecurityType.to_string2(record.basic.type) == SecurityType.FUTURE:
                snapshot_tmp['future_valid'] = True
                snapshot_tmp['future_last_settle_price'] = record.futureExData.lastSettlePrice
                snapshot_tmp['future_position'] = record.futureExData.position
                snapshot_tmp['future_position_change'] = record.futureExData.positionChange
                snapshot_tmp['future_main_contract'] = record.futureExData.isMainContract
                snapshot_tmp['future_last_trade_time'] = record.futureExData.lastTradeTime

            snapshot_tmp['trust_valid'] = False
            if record.HasField('trustExData'):
                snapshot_tmp['trust_valid'] = True
                snapshot_tmp['trust_dividend_yield'] = record.trustExData.dividendYield
                snapshot_tmp['trust_aum'] = record.trustExData.aum
                snapshot_tmp['trust_outstanding_units'] = record.trustExData.outstandingUnits
                snapshot_tmp['trust_netAssetValue'] = record.trustExData.netAssetValue
                snapshot_tmp['trust_premium'] = record.trustExData.premium

            snapshot_list.append(snapshot_tmp)

        return RET_OK, "", snapshot_list


class RtDataQuery:
    """
    Query Conversion for getting stock real-time data.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, security_firm=SecurityFirm.NONE):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0

        market_code, stock_code = content
        from ..common.pb.Qot_GetRT_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetRT, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        raw_rt_data_list = rsp_pb.s2c.rtList
        rt_list = [
            {
                "code": merge_qot_mkt_stock_str(rsp_pb.s2c.security.market, rsp_pb.s2c.security.code),
                "name": rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else 'N/A',
                "time": record.time,
                "is_blank":  True if record.isBlank else False,
                "opened_mins": record.minute,
                "cur_price": record.price,
                "last_close": record.lastClosePrice,
                # 期权没有计算这个均价，应该是N/A
                # 期权是正股的衍生品，其价格完全依赖正股的波动，而不是期权自身的博弈。
                # 所以不会因为期权价格回踩均线就怎么样的，均线也就没啥用了。
                "avg_price": record.avgPrice if record.HasField('avgPrice') else 'N/A', # 初始化枚举类型
                "turnover": record.turnover,
                # 成交量：优先使用高精度字段 hpVolume，如果没有则使用 volume
                "volume": record.hpVolume if record.HasField('hpVolume') else record.volume
            } for record in raw_rt_data_list
        ]
        return RET_OK, "", rt_list


class SubplateQuery:
    """
    Query Conversion for getting sub-plate stock list.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, plate_class, conn_id, security_firm=SecurityFirm.NONE):

        from ..common.pb.Qot_GetPlateSet_pb2 import Request
        req = Request()
        _, req.c2s.market = Market.to_number(market)
        _, req.c2s.plateSetType = Plate.to_number(plate_class)
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetPlateSet, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_plate_list = rsp_pb.s2c.plateInfoList

        plate_list = [{
            "code": merge_qot_mkt_stock_str(record.plate.market, record.plate.code),
            "plate_name":
            record.name,
            "plate_id":
            record.plate.code
        } for record in raw_plate_list]

        return RET_OK, "", plate_list


class PlateStockQuery:
    """
    Query Conversion for getting all the stock list of a given plate.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, plate_code, sort_field, ascend, conn_id, security_firm=SecurityFirm.NONE):

        ret_code, content = split_stock_str(plate_code)
        if ret_code != RET_OK:
            msg = content
            error_str = ERROR_STR_PREFIX + msg
            return RET_ERROR, error_str, None, 0, 0

        market, code = content
        r, v = SortField.to_number(sort_field)
        from ..common.pb.Qot_GetPlateSecurity_pb2 import Request
        req = Request()
        req.c2s.plate.market = market
        req.c2s.plate.code = code
        req.c2s.sortField = v
        req.c2s.ascend = ascend
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetPlateSecurity, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_stock_list = rsp_pb.s2c.staticInfoList

        stock_list = []
        for record in raw_stock_list:
            stock_tmp = {}
            stock_tmp['stock_id'] = record.basic.id
            stock_tmp['lot_size'] = record.basic.lotSize
            stock_tmp['code'] = merge_qot_mkt_stock_str(
                record.basic.security.market, record.basic.security.code)
            stock_tmp['stock_name'] = record.basic.name
            stock_tmp['list_time'] = record.basic.listTime
            stock_tmp['stock_type'] = SecurityType.to_string2(record.basic.secType) if record.basic.HasField('secType') else 'N/A' # 初始化枚举类型
            stock_tmp['main_contract'] = record.futureExData.isMainContract
            stock_tmp['last_trade_time'] = record.futureExData.lastTradeTime
            stock_list.append(stock_tmp)

        return RET_OK, "", stock_list


class BrokerQueueQuery:
    """
    Query Conversion for getting broker queue information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, security_firm=SecurityFirm.NONE):

        ret_code, content = split_stock_str(code)
        if ret_code == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0

        market, code = content
        from ..common.pb.Qot_GetBroker_pb2 import Request
        req = Request()
        req.c2s.security.market = market
        req.c2s.security.code = code
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetBroker, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)

        raw_broker_bid = rsp_pb.s2c.brokerBidList
        bid_list = []
        if raw_broker_bid is not None:
            bid_list = [{
                "bid_broker_id": record.id,
                "bid_broker_name": record.name,
                "bid_broker_pos": record.pos,
                "code": merge_qot_mkt_stock_str(rsp_pb.s2c.security.market, rsp_pb.s2c.security.code),
                "name": rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else 'N/A',
                "order_id": record.orderID if record.HasField('orderID') else 'N/A',
                "order_volume": record.volume if record.HasField('volume') else 'N/A'
            } for record in raw_broker_bid]

        raw_broker_ask = rsp_pb.s2c.brokerAskList
        ask_list = []
        if raw_broker_ask is not None:
            ask_list = [{
                "ask_broker_id": record.id,
                "ask_broker_name": record.name,
                "ask_broker_pos": record.pos,
                "code": merge_qot_mkt_stock_str(rsp_pb.s2c.security.market, rsp_pb.s2c.security.code),
                "name": rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else 'N/A',
                "order_id": record.orderID if record.HasField('orderID') else 'N/A',
                "order_volume": record.volume if record.HasField('volume') else 'N/A'
            } for record in raw_broker_ask]

        return RET_OK, "", (stock_code, bid_list, ask_list)



class RequestHistoryKlineQuery:
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, start_date, end_date, ktype, autype, fields,
                 max_num, conn_id, next_req_key, extended_time, session, security_firm=SecurityFirm.NONE):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0

        market_code, stock_code = content

        # check k line type
        if not KLType.if_has_key(ktype):
            error_str = ERROR_STR_PREFIX + "ktype is %s, which is not valid. (%s)" \
                % (ktype, KLType.get_all_keys())
            return RET_ERROR, error_str, None, 0, 0

        if not AuType.if_has_key(autype):
            error_str = ERROR_STR_PREFIX + "autype is %s, which is not valid. (%s)" \
                % (autype, AuType.get_all_keys())
            return RET_ERROR, error_str, None, 0, 0

        from ..common.pb.Qot_RequestHistoryKL_pb2 import Request

        req = Request()
        _, req.c2s.rehabType = AuType.to_number(autype)
        _, req.c2s.klType = KLType.to_number(ktype)
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if start_date:
            req.c2s.beginTime = start_date
        if end_date:
            req.c2s.endTime = end_date
        req.c2s.maxAckKLNum = max_num
        req.c2s.needKLFieldsFlag = KL_FIELD.kl_fields_to_flag_val(fields)
        if next_req_key is not None:
            req.c2s.nextReqKey = next_req_key
        if extended_time:
            req.c2s.extendedTime = True
        _, req.c2s.session = Session.to_number(session)
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_RequestHistoryKL, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        has_next = False
        next_req_key = None
        if rsp_pb.s2c.HasField('nextReqKey'):
            has_next = True
            next_req_key = bytes(rsp_pb.s2c.nextReqKey)

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)
        stock_name = rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else "N/A"

        list_ret = []
        dict_data = {}
        raw_kline_list = rsp_pb.s2c.klList
        for record in raw_kline_list:
            dict_data['code'] = stock_code
            dict_data['name'] = stock_name
            dict_data['time_key'] = record.time
            if record.isBlank:
                continue
            if record.HasField('openPrice'):
                dict_data['open'] = record.openPrice
            if record.HasField('highPrice'):
                dict_data['high'] = record.highPrice
            if record.HasField('lowPrice'):
                dict_data['low'] = record.lowPrice
            if record.HasField('closePrice'):
                dict_data['close'] = record.closePrice
            if record.HasField('hpVolume'):
                dict_data['volume'] = record.hpVolume
            elif record.HasField('volume'):
                dict_data['volume'] = record.volume
            if record.HasField('turnover'):
                dict_data['turnover'] = record.turnover
            if record.HasField('pe'):
                dict_data['pe_ratio'] = record.pe
            if record.HasField('turnoverRate'):
                dict_data['turnover_rate'] = record.turnoverRate
            if record.HasField('changeRate'):
                dict_data['change_rate'] = record.changeRate
            if record.HasField('lastClosePrice'):
                dict_data['last_close'] = record.lastClosePrice
            list_ret.append(dict_data.copy())

        return RET_OK, "", (list_ret, has_next, next_req_key)



class SubscriptionQuery:
    """
    Query Conversion for getting user's subscription information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_sub_or_unsub_req(cls,
                              code_list,
                              subtype_list,
                              is_sub,
                              conn_id,
                              is_first_push,
                              is_detailed_orderbook,
                              extended_time,
                              reg_or_unreg_push,
                              unsub_all=False,
                              session=Session.NONE,
                              security_firm=SecurityFirm.NONE):

        stock_tuple_list = []

        if code_list is not None:
            for code in code_list:
                ret_code, content = split_stock_str(code)
                if ret_code != RET_OK:
                    return ret_code, content, None
                market_code, stock_code = content
                stock_tuple_list.append((market_code, stock_code))

        from ..common.pb.Qot_Sub_pb2 import Request
        req = Request()

        if unsub_all is True:
            req.c2s.isUnsubAll = True
            req.c2s.isSubOrUnSub = False
        else:
            for market_code, stock_code in stock_tuple_list:
                stock_inst = req.c2s.securityList.add()
                stock_inst.code = stock_code
                stock_inst.market = market_code
            for subtype in subtype_list:
                r, v = SubType.to_number(subtype)
                req.c2s.subTypeList.append(v)
            req.c2s.isSubOrUnSub = is_sub
            req.c2s.isFirstPush = is_first_push
            req.c2s.isRegOrUnRegPush = reg_or_unreg_push
            req.c2s.isSubOrderBookDetail = is_detailed_orderbook
            req.c2s.extendedTime = extended_time
            b, n = Session.to_number(session)
            req.c2s.session = n

        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_Sub, conn_id)

    @classmethod
    def pack_subscribe_req(cls, code_list, subtype_list, conn_id, is_first_push, subscribe_push, is_detailed_orderbook, extended_time, session=Session.NONE, security_firm=SecurityFirm.NONE):
        return SubscriptionQuery.pack_sub_or_unsub_req(code_list,
                                                       subtype_list,
                                                       True,
                                                       conn_id,
                                                       is_first_push,
                                                       is_detailed_orderbook,
                                                       extended_time,
                                                       subscribe_push,
                                                       session=session,
                                                       security_firm=security_firm)

    @classmethod
    def unpack_subscribe_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        return RET_OK, "", None

    @classmethod
    def pack_unsubscribe_req(cls, code_list, subtype_list, unsubscribe_all, conn_id, security_firm=SecurityFirm.NONE):

        return SubscriptionQuery.pack_sub_or_unsub_req(code_list,
                                                       subtype_list,
                                                       False,
                                                       conn_id,
                                                       False,
                                                       False,
                                                       False,
                                                       False,
                                                       unsubscribe_all,
                                                       security_firm=security_firm)

    @classmethod
    def unpack_unsubscribe_rsp(cls, rsp_pb):
        """Unpack the un-subscribed response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        return RET_OK, "", None

    @classmethod
    def pack_subscription_query_req(cls, is_all_conn, conn_id):

        from ..common.pb.Qot_GetSubInfo_pb2 import Request
        req = Request()
        req.c2s.isReqAllConn = is_all_conn

        return pack_pb_req(req, ProtoId.Qot_GetSubInfo, conn_id)

    @classmethod
    def unpack_subscription_query_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        raw_sub_info = rsp_pb.s2c
        result = {}
        result['total_used'] = raw_sub_info.totalUsedQuota
        result['remain'] = raw_sub_info.remainQuota
        result['option_used_quota'] = raw_sub_info.optionUsedQuota if raw_sub_info.HasField('optionUsedQuota') else 0
        result['option_remain_quota'] = raw_sub_info.optionRemainQuota if raw_sub_info.HasField('optionRemainQuota') else 0
        result['conn_sub_list'] = []
        for conn_sub_info in raw_sub_info.connSubInfoList:
            conn_sub_info_tmp = {}
            conn_sub_info_tmp['used'] = conn_sub_info.usedQuota
            conn_sub_info_tmp['is_own_conn'] = conn_sub_info.isOwnConnData

            # Handle securityFirm field if present
            if conn_sub_info.HasField('securityFirm'):
                r, str_security_firm = SecurityFirm.to_string(conn_sub_info.securityFirm)
                if r:
                    conn_sub_info_tmp['security_firm'] = str_security_firm
                else:
                    conn_sub_info_tmp['security_firm'] = SecurityFirm.NONE
            else:
                conn_sub_info_tmp['security_firm'] = SecurityFirm.NONE

            conn_sub_info_tmp['option_used_quota'] = conn_sub_info.optionUsedQuota if conn_sub_info.HasField('optionUsedQuota') else 0

            conn_sub_info_tmp['sub_list'] = []
            for sub_info in conn_sub_info.subInfoList:
                sub_info_tmp = {}
                r, str_sub_type = SubType.to_string(sub_info.subType)
                if not r:
                    logger.error("error subtype:{}".format(sub_info.subType))
                    continue

                sub_info_tmp['subtype'] = str_sub_type
                sub_info_tmp['code_list'] = []
                for stock in sub_info.securityList:
                    sub_info_tmp['code_list'].append(
                        merge_qot_mkt_stock_str(int(stock.market), stock.code),)

                conn_sub_info_tmp['sub_list'].append(sub_info_tmp)

            result['conn_sub_list'].append(conn_sub_info_tmp)

        return RET_OK, "", result

    @classmethod
    def pack_push_or_unpush_req(cls, code_list, subtype_list, is_push, conn_id, is_first_push, security_firm=SecurityFirm.NONE):
        stock_tuple_list = []
        for code in code_list:
            ret_code, content = split_stock_str(code)
            if ret_code != RET_OK:
                return ret_code, content, None
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        from ..common.pb.Qot_RegQotPush_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.code = stock_code
            stock_inst.market = market_code
        for subtype in subtype_list:
            _, v = SubType.to_number(subtype)
            req.c2s.subTypeList.append(v)
        req.c2s.isRegOrUnReg = is_push
        req.c2s.isFirstPush = True if is_first_push else False

        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_RegQotPush, conn_id)

    @classmethod
    def pack_push_req(cls, code_list, subtype_list, conn_id, is_first_push, security_firm=SecurityFirm.NONE):

        return SubscriptionQuery.pack_push_or_unpush_req(code_list, subtype_list, True, conn_id, is_first_push, security_firm=security_firm)

    @classmethod
    def pack_unpush_req(cls, code_list, subtype_list, conn_id, is_first_push=False, security_firm=SecurityFirm.NONE):

        return SubscriptionQuery.pack_push_or_unpush_req(code_list, subtype_list, False, conn_id, is_first_push, security_firm=security_firm)

    @classmethod
    def unpack_unpush_query_rsp(cls, rsp_pb):
        return RET_OK, "", None


def parse_pb_BasicQot(pb):
    # 成交量：优先使用高精度字段 hpVolume，如果没有则使用 volume
    volume = pb.hpVolume if pb.HasField('hpVolume') else pb.volume

    item = {
        'code': merge_qot_mkt_stock_str(int(pb.security.market), pb.security.code),
        'name': "N/A" if not pb.HasField('name') else pb.name,
        'data_date':pb.updateTime.split()[0] if len(pb.updateTime) > 0 else '',
        'data_time': pb.updateTime.split()[1] if len(pb.updateTime) > 0 else '',
        'last_price': pb.curPrice,
        'open_price': pb.openPrice,
        'high_price': pb.highPrice,
        'low_price': pb.lowPrice,
        'prev_close_price': pb.lastClosePrice,
        'volume': volume,
        'turnover': pb.turnover,
        'turnover_rate': pb.turnoverRate,
        'amplitude': pb.amplitude,
        'suspension': pb.isSuspended,
        'listing_date': "N/A" if pb.HasField('optionExData') else pb.listTime,
        'price_spread': pb.priceSpread,
        'dark_status': DarkStatus.to_string2(pb.darkStatus) if pb.HasField('darkStatus') else 'N/A',# 初始化枚举类型
        'sec_status': SecurityStatus.to_string2(pb.secStatus) if pb.HasField(
            'secStatus') else 'N/A',# 初始化枚举类型
    }

    if pb.HasField('optionExData'):
        set_item_from_pb(item, pb.optionExData, pb_field_map_OptionBasicQotExData)
    else:
        set_item_none(item, pb_field_map_OptionBasicQotExData) # 这里设置了 'N/A' # 初始化枚举类型

    if pb.HasField('futureExData'):
        set_item_from_pb(item, pb.futureExData, pb_field_map_FutureBasicQotExData)
    else:
        set_item_none(item, pb_field_map_FutureBasicQotExData)

    if pb.HasField('preMarket'):
        set_item_from_pb(item, pb.preMarket, pb_field_map_PreAfterMarketData_pre)
    else:
        set_item_none(item, pb_field_map_PreAfterMarketData_pre)

    if pb.HasField('afterMarket'):
        set_item_from_pb(item, pb.afterMarket, pb_field_map_PreAfterMarketData_after)
    else:
        set_item_none(item, pb_field_map_PreAfterMarketData_after)

    if pb.HasField('overnight'):
        set_item_from_pb(item, pb.overnight, pb_field_map_PreAfterMarketData_overnight)
    else:
        set_item_none(item, pb_field_map_PreAfterMarketData_overnight)

    return item

class StockQuoteQuery:
    """
    Query Conversion for getting stock quote data.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, stock_list, conn_id, security_firm=SecurityFirm.NONE):

        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in stock_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                msg = content
                error_str = ERROR_STR_PREFIX + msg
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None, 0, 0

        from ..common.pb.Qot_GetBasicQot_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetBasicQot, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []
        raw_quote_list = rsp_pb.s2c.basicQotList

        quote_list = list()
        for record in raw_quote_list:
            item = parse_pb_BasicQot(record)
            if item:
                quote_list.append(item)
        return RET_OK, "", quote_list


class TickerQuery:
    """Stick ticker data query class"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, num, conn_id, security_firm=SecurityFirm.NONE):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0

        if isinstance(num, int) is False:
            error_str = ERROR_STR_PREFIX + "num is %s of type %s, and the type shoud be %s" \
                                           % (num, str(type(num)), str(int))
            return RET_ERROR, error_str, None, 0, 0

        if num < 0:
            error_str = ERROR_STR_PREFIX + "num is %s, which is less than 0" % num
            return RET_ERROR, error_str, None, 0, 0

        market_code, stock_code = content
        from ..common.pb.Qot_GetTicker_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        req.c2s.maxRetNum = num
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetTicker, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)
        stock_name = rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else "N/A"
        raw_ticker_list = rsp_pb.s2c.tickerList
        ticker_list = [{
            "code": stock_code,
            "name": stock_name,
            "time": record.time,
            "price": record.price,
            # 成交量：优先使用高精度字段 hpVolume，如果没有则使用 volume
            "volume": record.hpVolume if record.HasField('hpVolume') else record.volume,
            "turnover": record.turnover,
            "ticker_direction": TickerDirect.to_string2(record.dir) if record.HasField('dir') else 'N/A',# 初始化枚举类型
            "sequence": record.sequence,
            "recv_timestamp":record.recvTime,
            "type": TickerType.to_string2(record.type) if record.HasField('type') else 'N/A',# 初始化枚举类型
            "push_data_type": PushDataType.to_string2(record.pushDataType),
        } for record in raw_ticker_list]
        return RET_OK, "", ticker_list


class CurKlineQuery:
    """Stock Kline data query class"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, num, ktype, autype, conn_id, security_firm=SecurityFirm.NONE):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0

        market_code, stock_code = content

        if not KLType.if_has_key(ktype):
            error_str = ERROR_STR_PREFIX + "ktype is %s, which is not valid. (%s)" \
                                           % (ktype, KLType.get_all_keys())
            return RET_ERROR, error_str, None, 0, 0

        if not AuType.if_has_key(autype):
            error_str = ERROR_STR_PREFIX + "autype is %s, which is not valid. (%s)" \
                                           % (autype, AuType.get_all_keys())
            return RET_ERROR, error_str, None, 0, 0

        if isinstance(num, int) is False:
            error_str = ERROR_STR_PREFIX + "num is %s of type %s, which type should be %s" \
                                           % (num, str(type(num)), str(int))
            return RET_ERROR, error_str, None, 0, 0

        if num < 0:
            error_str = ERROR_STR_PREFIX + "num is %s, which is less than 0" % num
            return RET_ERROR, error_str, None, 0, 0
        from ..common.pb.Qot_GetKL_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        _, req.c2s.rehabType = AuType.to_number(autype)
        req.c2s.reqNum = num
        _, req.c2s.klType = KLType.to_number(ktype)
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetKL, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)
        stock_name = rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else "N/A"
        raw_kline_list = rsp_pb.s2c.klList
        kline_list = [{
            "code": stock_code,
            "name": stock_name,
            "time_key": record.time,
            "open": record.openPrice,
            "high": record.highPrice,
            "low": record.lowPrice,
            "close": record.closePrice,
            # 成交量：优先使用高精度字段 hpVolume，如果没有则使用 volume
            "volume": record.hpVolume if record.HasField('hpVolume') else record.volume,
            "turnover": record.turnover,
            "pe_ratio": record.pe,
            "turnover_rate": record.turnoverRate,
            "last_close": record.lastClosePrice,
        } for record in raw_kline_list]

        return RET_OK, "", kline_list


class CurKlinePush:
    """Stock Kline data push class"""

    def __init__(self):
        pass

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        r, kl_type = KLType.to_string(rsp_pb.s2c.klType);
        if not r:
            return RET_ERROR, "kline push error kltype", None

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)
        stock_name = rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else "N/A"
        raw_kline_list = rsp_pb.s2c.klList
        kline_list = [{
            "k_type": kl_type,
            "code": stock_code,
            "name": stock_name,
            "time_key": record.time,
            "open": record.openPrice,
            "high": record.highPrice,
            "low": record.lowPrice,
            "close": record.closePrice,
            # 成交量：优先使用高精度字段 hpVolume，如果没有则使用 volume
            "volume": record.hpVolume if record.HasField('hpVolume') else record.volume,
            "turnover": record.turnover,
            "pe_ratio": record.pe,
            "turnover_rate": record.turnoverRate,
            "last_close": record.lastClosePrice,
        } for record in raw_kline_list]

        return RET_OK, "", kline_list


class OrderBookQuery:
    """
    Query Conversion for getting stock order book data.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, num, conn_id, security_firm=SecurityFirm.NONE, order_book_type=None):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0

        market_code, stock_code = content
        from ..common.pb.Qot_GetOrderBook_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        req.c2s.num = num
        if order_book_type is not None:
            from ..common.constant import OrderBookType
            r, v = OrderBookType.to_number(order_book_type)
            if r:
                req.c2s.orderBookType = v
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetOrderBook, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        raw_order_book_ask = rsp_pb.s2c.orderBookAskList
        raw_order_book_bid = rsp_pb.s2c.orderBookBidList

        order_book = {}
        order_book['code'] = merge_qot_mkt_stock_str(
            rsp_pb.s2c.security.market, rsp_pb.s2c.security.code)
        order_book['name'] = rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else 'N/A'
        order_book['svr_recv_time_bid'] = rsp_pb.s2c.svrRecvTimeBid
        order_book['svr_recv_time_ask'] = rsp_pb.s2c.svrRecvTimeAsk
        if rsp_pb.s2c.HasField('orderBookType'):
            from ..common.constant import OrderBookType
            order_book['order_book_type'] = OrderBookType.to_string2(rsp_pb.s2c.orderBookType)
        order_book['Bid'] = []
        order_book['Ask'] = []

        for record in raw_order_book_bid:
            detail = {}
            for info in record.detailList:
                detail[info.orderID] = info.volume
            # 成交量：优先使用高精度字段 hpVolume，如果没有则使用 volume
            volume = record.hpVolume if record.HasField('hpVolume') else record.volume
            order_book['Bid'].append((record.price, volume,
                                      record.orederCount, detail))
        for record in raw_order_book_ask:
            detail = {}
            for info in record.detailList:
                detail[info.orderID] = info.volume
            # 成交量：优先使用高精度字段 hpVolume，如果没有则使用 volume
            volume = record.hpVolume if record.HasField('hpVolume') else record.volume
            order_book['Ask'].append((record.price, volume,
                                      record.orederCount, detail))
        return RET_OK, "", order_book


class SuspensionQuery:
    """
    Query SuspensionQuery.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, start, end, conn_id, security_firm=SecurityFirm.NONE):

        list_req_stock = []
        for stock_str in code_list:
            ret, content = split_stock_str(stock_str)
            if ret == RET_ERROR:
                return RET_ERROR, content, None, 0, 0
            else:
                list_req_stock.append(content)

        from ..common.pb.Qot_GetSuspend_pb2 import Request
        req = Request()
        if start:
            req.c2s.beginTime = start
        if end:
            req.c2s.endTime = end
        for market, code in list_req_stock:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market
            stock_inst.code = code
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetSuspend, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_susp_list = []
        for record in rsp_pb.s2c.SecuritySuspendList:
            suspend_info_tmp = {}
            code = merge_qot_mkt_stock_str(
                record.security.market, record.security.code)
            for suspend_info in record.suspendList:
                suspend_info_tmp['code'] = code
                suspend_info_tmp['suspension_dates'] = suspend_info.time
            ret_susp_list.append(suspend_info_tmp)

        return RET_OK, "", ret_susp_list


class GlobalStateQuery:
    """
    Query process "FTNN.exe" global state : market state & logined state
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, user_id, conn_id):

        from ..common.pb.GetGlobalState_pb2 import Request
        req = Request()
        req.c2s.userID = user_id
        return pack_pb_req(req, ProtoId.GetGlobalState, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        state = rsp_pb.s2c
        program_status_type = ProgramStatusType.to_string2(
            state.programStatus.type) if state.HasField('programStatus') else 'N/A'# 初始化枚举类型
        program_status_desc = ""
        if state.programStatus.HasField("strExtDesc"):
            program_status_desc = state.programStatus.strExtDesc

        state_dict = {
            'market_sz': MarketState.to_string2(state.marketSZ) if state.HasField('marketSZ') else 'N/A',# 初始化枚举类型
            'market_us': MarketState.to_string2(state.marketUS) if state.HasField('marketUS') else 'N/A',# 初始化枚举类型
            'market_sh': MarketState.to_string2(state.marketSH) if state.HasField('marketSH') else 'N/A',# 初始化枚举类型
            'market_hk': MarketState.to_string2(state.marketHK) if state.HasField('marketHK') else 'N/A',# 初始化枚举类型
            'market_hkfuture': MarketState.to_string2(state.marketHKFuture) if state.HasField('marketHKFuture') else 'N/A',# 初始化枚举类型
            'market_usfuture': MarketState.to_string2(state.marketUSFuture) if state.HasField('marketUSFuture') else 'N/A',# 初始化枚举类型
            'market_sgfuture': MarketState.to_string2(state.marketSGFuture) if state.HasField(
                'marketSGFuture') else 'N/A',  # 初始化枚举类型
            'market_jpfuture': MarketState.to_string2(state.marketJPFuture) if state.HasField(
                'marketJPFuture') else 'N/A',  # 初始化枚举类型
            'market_sg': MarketState.to_string2(state.marketSG) if state.HasField(
                'marketSG') else 'N/A',  # 初始化枚举类型
            'market_my': MarketState.to_string2(state.marketMY) if state.HasField(
                'marketMY') else 'N/A',  # 初始化枚举类型
            'market_jp': MarketState.to_string2(state.marketJP) if state.HasField(
                'marketJP') else 'N/A',  # 初始化枚举类型
            'server_ver': str(state.serverVer),
            'trd_logined': state.trdLogined,
            'timestamp': str(state.time),
            'qot_logined': state.qotLogined,
            'local_timestamp': state.localTime if state.HasField('localTime') else time.time(),
            'program_status_type': program_status_type,
            'program_status_desc': program_status_desc
        }
        return RET_OK, "", state_dict


class KeepAlive:
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, conn_id):

        from ..common.pb.KeepAlive_pb2 import Request
        req = Request()
        req.c2s.time = int(time.time())
        return pack_pb_req(req, ProtoId.KeepAlive, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        return RET_OK, '', rsp_pb.s2c.time


class SysNotifyPush:
    """ SysNotifyPush """

    def __init__(self):
        pass

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg,

        pb_type = rsp_pb.s2c.type
        sub_type = None
        data = None
        notify_type = SysNotifyType.to_string2(pb_type)
        if notify_type == SysNotifyType.GTW_EVENT:
            if rsp_pb.s2c.HasField('event'):
                sub_type = GtwEventType.to_string2(rsp_pb.s2c.event.eventType)
                data = rsp_pb.s2c.event.desc
        elif notify_type == SysNotifyType.PROGRAM_STATUS:
            if rsp_pb.s2c.HasField('programStatus'):
                ret, status_type = ProgramStatusType.to_string(
                    rsp_pb.s2c.programStatus.programStatus.type)
                if not ret:
                    status_type = ProgramStatusType.NONE
                if rsp_pb.s2c.programStatus.programStatus.HasField('strExtDesc'):
                    status_desc = rsp_pb.s2c.programStatus.programStatus.strExtDesc
                else:
                    status_desc = ''
                sub_type = status_type
                data = status_desc
        elif notify_type == SysNotifyType.CONN_STATUS:
            if rsp_pb.s2c.HasField('connectStatus'):
                data = {'qot_logined': rsp_pb.s2c.connectStatus.qotLogined,
                        'trd_logined': rsp_pb.s2c.connectStatus.trdLogined}
        elif notify_type == SysNotifyType.QOT_RIGHT:
            if rsp_pb.s2c.HasField('qotRight'):
                qot_right = rsp_pb.s2c.qotRight
                data = {
                    'hk_qot_right': QotRight.to_string2(qot_right.hkQotRight) if qot_right.HasField('hkQotRight') else 'N/A',
                    'hk_option_qot_right': QotRight.to_string2(qot_right.hkOptionQotRight) if qot_right.HasField('hkOptionQotRight') else 'N/A',
                    'hk_future_qot_right': QotRight.to_string2(qot_right.hkFutureQotRight) if qot_right.HasField('hkFutureQotRight') else 'N/A',
                    'us_qot_right': QotRight.to_string2(qot_right.usQotRight) if qot_right.HasField('usQotRight') else 'N/A',
                    'has_us_option_qot_right': QotRight.to_string2(qot_right.hasUSOptionQotRight) if qot_right.HasField('hasUSOptionQotRight') else False,
                    'us_option_qot_right': QotRight.to_string2(qot_right.usOptionQotRight) if qot_right.HasField('usOptionQotRight') else 'N/A',
                    'us_future_qot_right': QotRight.to_string2(qot_right.usFutureQotRight) if qot_right.HasField('usFutureQotRight') else 'N/A',
                    'us_index_qot_right': QotRight.to_string2(qot_right.usIndexQotRight) if qot_right.HasField('usIndexQotRight') else 'N/A',
                    'us_otc_qot_right': QotRight.to_string2(qot_right.usOtcQotRight) if qot_right.HasField('usOtcQotRight') else 'N/A',
                    'cn_qot_right': QotRight.to_string2(qot_right.cnQotRight) if qot_right.HasField('cnQotRight') else 'N/A',
                    'sg_future_qot_right': QotRight.to_string2(qot_right.sgFutureQotRight) if qot_right.HasField('sgFutureQotRight') else 'N/A',
                    'jp_future_qot_right': QotRight.to_string2(qot_right.jpFutureQotRight) if qot_right.HasField('jpFutureQotRight') else 'N/A',
                    'us_future_qot_right_cme': QotRight.to_string2(qot_right.usCMEFutureQotRight) if qot_right.HasField('usCMEFutureQotRight') else 'N/A',
                    'us_future_qot_right_cbot': QotRight.to_string2(qot_right.usCBOTFutureQotRight) if qot_right.HasField('usCBOTFutureQotRight') else 'N/A',
                    'us_future_qot_right_nymex': QotRight.to_string2(qot_right.usNYMEXFutureQotRight) if qot_right.HasField('usNYMEXFutureQotRight') else 'N/A',
                    'us_future_qot_right_comex': QotRight.to_string2(qot_right.usCOMEXFutureQotRight) if qot_right.HasField('usCOMEXFutureQotRight') else 'N/A',
                    'us_future_qot_right_cboe': QotRight.to_string2(qot_right.usCBOEFutureQotRight) if qot_right.HasField('usCBOEFutureQotRight') else 'N/A',
                    'sh_qot_right': QotRight.to_string2(qot_right.shQotRight) if qot_right.HasField('shQotRight') else 'N/A',
                    'sz_qot_right': QotRight.to_string2(qot_right.szQotRight) if qot_right.HasField('szQotRight') else 'N/A',
                    'cc_qot_right': QotRight.to_string2(qot_right.ccQotRight) if qot_right.HasField('ccQotRight') else 'N/A',
                    'sg_stock_qot_right': QotRight.to_string2(qot_right.sgStockQotRight) if qot_right.HasField('sgStockQotRight') else 'N/A',
                    'my_stock_qot_right': QotRight.to_string2(qot_right.myStockQotRight) if qot_right.HasField('myStockQotRight') else 'N/A',
                    'jp_stock_qot_right': QotRight.to_string2(qot_right.jpStockQotRight) if qot_right.HasField('jpStockQotRight') else 'N/A',
                    'ec_qot_right': QotRight.to_string2(qot_right.ecQotRight) if qot_right.HasField('ecQotRight') else 'N/A',
                }
        elif notify_type == SysNotifyType.API_LEVEL:
            if rsp_pb.s2c.HasField('apiLevel'):
                data = {'api_level': rsp_pb.s2c.apiLevel.apiLevel}

        return RET_OK, (notify_type, sub_type, data)



class StockReferenceList:
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, ref_type, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetReference_pb2 import Request

        ret, content = split_stock_str(code)
        if ret != RET_OK:
            return ret, content, None, 0, 0

        req = Request()
        req.c2s.security.market = content[0]
        req.c2s.security.code = content[1]
        _, req.c2s.referenceType = SecurityReferenceType.to_number(ref_type)
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetReference, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        if not rsp_pb.HasField('s2c'):
            return RET_OK, '', None

        data_list = []
        for info in rsp_pb.s2c.staticInfoList:
            data = {}
            data['code'] = merge_qot_mkt_stock_str(
                info.basic.security.market, info.basic.security.code)
            # item['stock_id'] = info.basic.id
            data['lot_size'] = info.basic.lotSize
            data['stock_type'] = SecurityType.to_string2(info.basic.secType) if info.basic.HasField('secType') else 'N/A'# 初始化枚举类型
            data['stock_name'] = info.basic.name
            data['list_time'] = info.basic.listTime
            if info.HasField('warrantExData'):
                data['wrt_valid'] = True
                data['wrt_type'] = WrtType.to_string2(info.warrantExData.type) if info.warrantExData.HasField('type') else 'N/A'# 初始化枚举类型
                data['wrt_code'] = merge_qot_mkt_stock_str(info.warrantExData.owner.market,
                                                           info.warrantExData.owner.code)
            else:
                data['wrt_valid'] = False

            if info.HasField('futureExData'):
                data['future_valid'] = True
                data['future_main_contract'] = info.futureExData.isMainContract
                data['future_last_trade_time'] = info.futureExData.lastTradeTime
            else:
                data['future_valid'] = False

            data_list.append(data)

        return RET_OK, '', data_list


class OwnerPlateQuery:
    """
    Query Conversion for getting owner plate information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, conn_id, security_firm=SecurityFirm.NONE):

        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None, 0, 0

        from ..common.pb.Qot_GetOwnerPlate_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetOwnerPlate, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []
        raw_quote_list = rsp_pb.s2c.ownerPlateList

        data_list = []
        for record in raw_quote_list:
            plate_info_list = record.plateInfoList
            for plate_info in plate_info_list:
                quote_list = {
                    'code': merge_qot_mkt_stock_str(record.security.market, record.security.code),
                    'name': record.name if record.HasField('name') else 'N/A',
                    'plate_code': merge_qot_mkt_stock_str(plate_info.plate.market, plate_info.plate.code),
                    'plate_name': str(plate_info.name),
                    'plate_type': Plate.to_string2(plate_info.plateType) if plate_info.HasField('plateType') else 'N/A' # 初始化枚举类型
                }
                data_list.append(quote_list)

        return RET_OK, "", data_list


class HoldingChangeList:
    """
    Query Conversion for getting holding change list.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, holder_type, conn_id, start_date, end_date=None, security_firm=SecurityFirm.NONE):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0

        market_code, stock_code = content

        if start_date is None:
            msg = "The start date is none."
            return RET_ERROR, msg, None, 0, 0
        else:
            ret, msg = normalize_date_format(start_date)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            start_date = msg

        if end_date is None:
            today = datetime.today()
            end_date = today.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(end_date)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            end_date = msg

        from ..common.pb.Qot_GetHoldingChangeList_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        req.c2s.holderCategory = holder_type
        req.c2s.beginTime = start_date
        if end_date:
            req.c2s.endTime = end_date
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetHoldingChangeList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []
        raw_quote_list = rsp_pb.s2c.holdingChangeList

        data_list = []
        for record in raw_quote_list:
            quote_list = {
                'holder_name': record.holderName,
                'holding_qty': record.holdingQty,
                'holding_ratio': record.holdingRatio,
                'change_qty': record.changeQty,
                'change_ratio': record.changeRatio,
                'time': record.time,
            }
            data_list.append(quote_list)

        return RET_OK, "", data_list

class OptionDataFilter:
    def __init__(self,
                 implied_volatility_min=None, implied_volatility_max=None,
                 delta_min=None, delta_max=None,
                 gamma_min=None, gamma_max=None,
                 vega_min=None, vega_max=None,
                 theta_min=None, theta_max=None,
                 rho_min=None, rho_max=None,
                 net_open_interest_min=None, net_open_interest_max=None,
                 open_interest_min=None, open_interest_max=None,
                 vol_min=None, vol_max=None):
        """
        初始化 OptionDataFilter 类的实例。

        :param implied_volatility_min: 隐含波动率过滤起点 %
        :param implied_volatility_max: 隐含波动率过滤终点 %
        :param delta_min: 希腊值 Delta 过滤起点
        :param delta_max: 希腊值 Delta 过滤终点
        :param gamma_min: 希腊值 Gamma 过滤起点
        :param gamma_max: 希腊值 Gamma 过滤终点
        :param vega_min: 希腊值 Vega 过滤起点
        :param vega_max: 希腊值 Vega 过滤终点
        :param theta_min: 希腊值 Theta 过滤起点
        :param theta_max: 希腊值 Theta 过滤终点
        :param rho_min: 希腊值 Rho 过滤起点
        :param rho_max: 希腊值 Rho 过滤终点
        :param net_open_interest_min: 净未平仓合约数过滤起点
        :param net_open_interest_max: 净未平仓合约数过滤终点
        :param open_interest_min: 未平仓合约数过滤起点
        :param open_interest_max: 未平仓合约数过滤终点
        :param vol_min: 成交量过滤起点
        :param vol_max: 成交量过滤终点
        """
        self.implied_volatility_min = implied_volatility_min
        self.implied_volatility_max = implied_volatility_max
        self.delta_min = delta_min
        self.delta_max = delta_max
        self.gamma_min = gamma_min
        self.gamma_max = gamma_max
        self.vega_min = vega_min
        self.vega_max = vega_max
        self.theta_min = theta_min
        self.theta_max = theta_max
        self.rho_min = rho_min
        self.rho_max = rho_max
        self.net_open_interest_min = net_open_interest_min
        self.net_open_interest_max = net_open_interest_max
        self.open_interest_min = open_interest_min
        self.open_interest_max = open_interest_max
        self.vol_min = vol_min
        self.vol_max = vol_max

class OptionChain:
    """
    Query Conversion for getting option chain information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, index_option_type, conn_id, start_date, end_date=None, option_type=OptionType.ALL, option_cond_type=OptionCondType.ALL, data_filter = None, security_firm=SecurityFirm.NONE):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0

        market_code, stock_code = content

        if start_date is None:
            msg = "The start date is none."
            return RET_ERROR, msg, None, 0, 0
        else:
            ret, msg = normalize_date_format(start_date)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            start_date = msg

        if end_date is None:
            today = datetime.today()
            end_date = today.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(end_date)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            end_date = msg

        r, option_cond_type = OptionCondType.to_number(option_cond_type)
        if r is False:
            option_cond_type = None

        r, option_type = OptionType.to_number(option_type)
        if r is False:
            option_type = None

        r, index_option_type = IndexOptionType.to_number(index_option_type)
        if r is False:
            index_option_type = None

        from ..common.pb.Qot_GetOptionChain_pb2 import Request
        req = Request()
        req.c2s.owner.market = market_code
        req.c2s.owner.code = stock_code
        if index_option_type is not None:
            req.c2s.indexOptionType = index_option_type
        req.c2s.beginTime = start_date
        req.c2s.endTime = end_date
        if option_type is not None:
            req.c2s.type = option_type
        if option_cond_type is not None:
            req.c2s.condition = option_cond_type

        if data_filter is not None:
            if data_filter.implied_volatility_min is not None:
                req.c2s.dataFilter.impliedVolatilityMin = data_filter.implied_volatility_min
            if data_filter.implied_volatility_max is not None:
                req.c2s.dataFilter.impliedVolatilityMax = data_filter.implied_volatility_max

            if data_filter.delta_min is not None:
                req.c2s.dataFilter.deltaMin = data_filter.delta_min
            if data_filter.delta_max is not None:
                req.c2s.dataFilter.deltaMax = data_filter.delta_max

            if data_filter.gamma_min is not None:
                req.c2s.dataFilter.gammaMin = data_filter.gamma_min
            if data_filter.gamma_max is not None:
                req.c2s.dataFilter.gammaMax = data_filter.gamma_max

            if data_filter.vega_min is not None:
                req.c2s.dataFilter.vegaMin = data_filter.vega_min
            if data_filter.vega_max is not None:
                req.c2s.dataFilter.vegaMax = data_filter.vega_max

            if data_filter.theta_min is not None:
                req.c2s.dataFilter.thetaMin = data_filter.theta_min
            if data_filter.theta_max is not None:
                req.c2s.dataFilter.thetaMax = data_filter.theta_max

            if data_filter.rho_min is not None:
                req.c2s.dataFilter.rhoMin = data_filter.rho_min
            if data_filter.rho_max is not None:
                req.c2s.dataFilter.rhoMax = data_filter.rho_max

            if data_filter.net_open_interest_min is not None:
                req.c2s.dataFilter.netOpenInterestMin = data_filter.net_open_interest_min
            if data_filter.net_open_interest_max is not None:
                req.c2s.dataFilter.netOpenInterestMax = data_filter.net_open_interest_max

            if data_filter.open_interest_min is not None:
                req.c2s.dataFilter.openInterestMin = data_filter.open_interest_min
            if data_filter.open_interest_max is not None:
                req.c2s.dataFilter.openInterestMax = data_filter.open_interest_max

            if data_filter.vol_min is not None:
                req.c2s.dataFilter.volMin = data_filter.vol_min
            if data_filter.vol_max is not None:
                req.c2s.dataFilter.volMax = data_filter.vol_max
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetOptionChain, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []
        raw_quote_list = rsp_pb.s2c.optionChain

        data_list = []
        for OptionItem in raw_quote_list:
            for record_all in OptionItem.option:
                record_list = []
                if record_all.HasField('call'):
                    record_list.append(record_all.call)
                if record_all.HasField('put'):
                    record_list.append(record_all.put)

                for record in record_list:
                    quote_list = {
                        'code': merge_qot_mkt_stock_str(int(record.basic.security.market), record.basic.security.code),
                        "stock_id": record.basic.id,
                        "name": record.basic.name,
                        "lot_size": record.basic.lotSize,
                        "stock_type": SecurityType.to_string2(record.basic.secType) if record.basic.HasField('secType') else NoneDataType,# 初始化枚举类型
                        "option_type": OptionType.to_string2(record.optionExData.type) if record.HasField('optionExData') else NoneDataType,# 初始化枚举类型
                        "stock_owner": merge_qot_mkt_stock_str(int(record.optionExData.owner.market), record.optionExData.owner.code)
                        if record.HasField('optionExData') else "",
                        "strike_time": record.optionExData.strikeTime,
                        "strike_price": record.optionExData.strikePrice if record.HasField('optionExData') else NoneDataType,
                        "suspension": record.optionExData.suspend if record.HasField('optionExData') else NoneDataType,
                        "index_option_type": IndexOptionType.to_string2(record.optionExData.indexOptionType) if record.HasField('optionExData') else NoneDataType,# 初始化枚举类型
                        "expiration_cycle": ExpirationCycle.to_string2(record.optionExData.expirationCycle) if record.optionExData.HasField('expirationCycle') else NoneDataType,
                        "option_standard_type": OptionStandardType.to_string2(record.optionExData.optionStandardType) if record.optionExData.HasField('optionStandardType') else NoneDataType,
                        "option_settlement_mode": OptionSettlementMode.to_string2(record.optionExData.optionSettlementMode) if record.optionExData.HasField('optionSettlementMode') else NoneDataType,
                    }
                    data_list.append(quote_list)

        return RET_OK, "", data_list

class QuoteWarrant:
    """
    拉取窝轮
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, req, conn_id, security_firm=SecurityFirm.NONE):
        from ..quote.quote_get_warrant import Request as WarrantRequest
        if (req is None) or (not isinstance(req, WarrantRequest)):
            req = WarrantRequest()
        ret, context = req.fill_request_pb()
        if ret == RET_OK:
            return pack_pb_req(context, ProtoId.Qot_GetWarrant, conn_id)
        else:
            return ret, context, None

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        from ..quote.quote_get_warrant import Response as WarrantResponse
        return WarrantResponse.unpack_response_pb(rsp_pb)


class HistoryKLQuota:
    """
    拉取限额
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, get_detail, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_RequestHistoryKLQuota_pb2 import Request
        req = Request()
        req.c2s.bGetDetail = get_detail
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_RequestHistoryKLQuota, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        used_quota = rsp_pb.s2c.usedQuota
        remain_quota = rsp_pb.s2c.remainQuota
        detail_list = []

        details = rsp_pb.s2c.detailList
        for item in details:
            code = merge_qot_mkt_stock_str(
                int(item.security.market), item.security.code)
            name = item.name if item.HasField('name') else "N/A"
            request_time = str(item.requestTime)
            detail_list.append({"code": code, "name": name, "request_time": request_time})

        data = {
            "used_quota": used_quota,
            "remain_quota": remain_quota,
            "detail_list": detail_list
        }
        return RET_OK, "", data


class RequestRehab:
    """
    获取除权信息
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, stock, conn_id, security_firm=SecurityFirm.NONE):
        ret_code, content = split_stock_str(stock)
        if ret_code != RET_OK:
            msg = content
            error_str = ERROR_STR_PREFIX + msg
            return RET_ERROR, error_str, None, 0, 0
        market, code = content

        from ..common.pb.Qot_RequestRehab_pb2 import Request
        req = Request()
        req.c2s.security.market = market
        req.c2s.security.code = code
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_RequestRehab, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        class KLRehabFlag(object):
            SPLIT = 1
            JOIN = 2
            BONUS = 4
            TRANSFER = 8
            ALLOT = 16
            ADD = 32
            DIVIDED = 64
            SP_DIVIDED = 128
            SPIN_OFF = 256

        rehab_list = list()
        for rehab in rsp_pb.s2c.rehabList:
            stock_rehab_tmp = {}
            stock_rehab_tmp['ex_div_date'] = rehab.time.split()[0]  # 时间字符串
            stock_rehab_tmp['forward_adj_factorA'] = rehab.fwdFactorA
            stock_rehab_tmp['forward_adj_factorB'] = rehab.fwdFactorB
            stock_rehab_tmp['backward_adj_factorA'] = rehab.bwdFactorA
            stock_rehab_tmp['backward_adj_factorB'] = rehab.bwdFactorB

            act_flag = rehab.companyActFlag
            if act_flag & KLRehabFlag.SPIN_OFF:
                stock_rehab_tmp['spin_off_ratio'] = rehab.spinOffBase / rehab.spinOffErt
                stock_rehab_tmp['spin_off_base'] = rehab.spinOffBase
                stock_rehab_tmp['spin_off_ert'] = rehab.spinOffErt
            if act_flag & KLRehabFlag.SP_DIVIDED:
                stock_rehab_tmp['special_dividend'] = rehab.spDividend
            if act_flag & KLRehabFlag.DIVIDED:
                stock_rehab_tmp['per_cash_div'] = rehab.dividend
            if act_flag & KLRehabFlag.ADD:
                stock_rehab_tmp['stk_spo_ratio'] = rehab.addBase / rehab.addErt
                stock_rehab_tmp['stk_spo_price'] = rehab.addPrice
                stock_rehab_tmp['add_base'] = rehab.addBase
                stock_rehab_tmp['add_ert'] = rehab.ert
            if act_flag & KLRehabFlag.ALLOT:
                stock_rehab_tmp['allotment_ratio'] = rehab.allotBase / \
                    rehab.allotErt
                stock_rehab_tmp['allotment_price'] = rehab.allotPrice
                stock_rehab_tmp['allot_base'] = rehab.allotBase
                stock_rehab_tmp['allot_ert'] = rehab.allotErt
            if act_flag & KLRehabFlag.TRANSFER:
                stock_rehab_tmp['per_share_trans_ratio'] = rehab.transferBase / \
                    rehab.transferErt
                stock_rehab_tmp['transfer_base'] = rehab.transferBase
                stock_rehab_tmp['transfer_ert'] = rehab.transferErt
            if act_flag & KLRehabFlag.BONUS:
                stock_rehab_tmp['per_share_div_ratio'] = rehab.bonusBase / \
                    rehab.bonusErt
                stock_rehab_tmp['bonus_base'] = rehab.bonusBase
                stock_rehab_tmp['bonus_ert'] = rehab.bonusErt
            if act_flag & KLRehabFlag.JOIN:
                stock_rehab_tmp['split_ratio'] = rehab.joinBase / rehab.joinErt
                stock_rehab_tmp['join_base'] = rehab.joinBase
                stock_rehab_tmp['join_ert'] = rehab.joinErt
            if act_flag & KLRehabFlag.SPLIT:
                stock_rehab_tmp['split_ratio'] = rehab.splitBase / \
                    rehab.splitErt
                stock_rehab_tmp['split_base'] = rehab.splitBase
                stock_rehab_tmp['split_ert'] = rehab.splitErt
            rehab_list.append(stock_rehab_tmp)

        return RET_OK, "", rehab_list


"""-------------------------------------------------------------"""


class GetUserInfo:
    """
    拉取用户信息
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, info_field, conn_id):
        from ..common.pb.GetUserInfo_pb2 import Request
        req = Request()
        if info_field is None:
            req.c2s.flag = 0
        else:
            req.c2s.flag = UserInfoField.fields_to_flag_val(info_field)
        return pack_pb_req(req, ProtoId.GetUserInfo, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        nick_name = rsp_pb.s2c.nickName if rsp_pb.s2c.HasField(
            'nickName') else "N/A"
        avatar_url = rsp_pb.s2c.avatarUrl if rsp_pb.s2c.HasField(
            'avatarUrl') else "N/A"
        user_attr = rsp_pb.s2c.userAttribution if rsp_pb.s2c.HasField(
            'userAttribution') else "N/A"
        api_level = rsp_pb.s2c.apiLevel if rsp_pb.s2c.HasField(
            'apiLevel') else "N/A"
        hk_qot_right = rsp_pb.s2c.hkQotRight if rsp_pb.s2c.HasField(
            'hkQotRight') else "N/A"
        hk_option_qot_right = rsp_pb.s2c.hkOptionQotRight if rsp_pb.s2c.HasField(
            'hkOptionQotRight') else "N/A"
        hk_future_qot_right = rsp_pb.s2c.hkFutureQotRight if rsp_pb.s2c.HasField(
            'hkFutureQotRight') else "N/A"
        us_qot_right = rsp_pb.s2c.usQotRight if rsp_pb.s2c.HasField(
            'usQotRight') else "N/A"
        us_option_qot_right = rsp_pb.s2c.usOptionQotRight if rsp_pb.s2c.HasField(
            'usOptionQotRight') else "N/A"
        us_future_qot_right = rsp_pb.s2c.usFutureQotRight if rsp_pb.s2c.HasField(
            'usFutureQotRight') else "N/A"
        cn_qot_right = rsp_pb.s2c.cnQotRight if rsp_pb.s2c.HasField(
            'cnQotRight') else "N/A"
        sg_future_qot_right = rsp_pb.s2c.sgFutureQotRight if rsp_pb.s2c.HasField(
            'sgFutureQotRight') else 'N/A'
        jp_future_qot_right = rsp_pb.s2c.jpFutureQotRight if rsp_pb.s2c.HasField(
            'jpFutureQotRight') else 'N/A'
        us_future_qot_right_cme = rsp_pb.s2c.usCMEFutureQotRight if rsp_pb.s2c.HasField(
            'usCMEFutureQotRight') else 'N/A'
        us_future_qot_right_cbot = rsp_pb.s2c.usCBOTFutureQotRight if rsp_pb.s2c.HasField(
            'usCBOTFutureQotRight') else 'N/A'
        us_future_qot_right_nymex = rsp_pb.s2c.usNYMEXFutureQotRight if rsp_pb.s2c.HasField(
            'usNYMEXFutureQotRight') else 'N/A'
        us_future_qot_right_comex = rsp_pb.s2c.usCOMEXFutureQotRight if rsp_pb.s2c.HasField(
            'usCOMEXFutureQotRight') else 'N/A'
        us_future_qot_right_cboe = rsp_pb.s2c.usCBOEFutureQotRight if rsp_pb.s2c.HasField(
            'usCBOEFutureQotRight') else 'N/A'
        cc_qot_right = rsp_pb.s2c.ccQotRight if rsp_pb.s2c.HasField(
            'ccQotRight') else 'N/A'
        sg_stock_qot_right = rsp_pb.s2c.sgStockQotRight if rsp_pb.s2c.HasField(
            'sgStockQotRight') else 'N/A'
        my_stock_qot_right = rsp_pb.s2c.myStockQotRight if rsp_pb.s2c.HasField(
            'myStockQotRight') else 'N/A'
        jp_stock_qot_right = rsp_pb.s2c.jpStockQotRight if rsp_pb.s2c.HasField(
            'jpStockQotRight') else 'N/A'
        ec_qot_right = rsp_pb.s2c.ecQotRight if rsp_pb.s2c.HasField(
            'ecQotRight') else 'N/A'
        is_need_agree_disclaimer = rsp_pb.s2c.isNeedAgreeDisclaimer if rsp_pb.s2c.HasField(
            'isNeedAgreeDisclaimer') else "N/A"
        user_id = rsp_pb.s2c.userID if rsp_pb.s2c.HasField('userID') else "N/A"
        update_type = rsp_pb.s2c.updateType if rsp_pb.s2c.HasField(
            'updateType') else "N/A"
        web_key = rsp_pb.s2c.webKey if rsp_pb.s2c.HasField('webKey') else "N/A"
        sub_quota = rsp_pb.s2c.subQuota if rsp_pb.s2c.HasField('subQuota') else "N/A"
        history_kl_quota = rsp_pb.s2c.historyKLQuota if rsp_pb.s2c.HasField('historyKLQuota') else "N/A"
        data = {
            "nick_name": nick_name,
            "avatar_url": avatar_url,
            "user_attr": UserAttr.to_string2(user_attr),
            "api_level": api_level,
            "hk_qot_right": QotRight.to_string2(hk_qot_right),
            "hk_option_qot_right": QotRight.to_string2(hk_option_qot_right),
            "hk_future_qot_right": QotRight.to_string2(hk_future_qot_right),
            "us_qot_right": QotRight.to_string2(us_qot_right),
            "us_option_qot_right": QotRight.to_string2(us_option_qot_right),
            "us_future_qot_right": QotRight.to_string2(us_future_qot_right),
            "cn_qot_right": QotRight.to_string2(cn_qot_right),
            'sg_future_qot_right': QotRight.to_string2(sg_future_qot_right),
            'jp_future_qot_right': QotRight.to_string2(jp_future_qot_right),
            'us_future_qot_right_cme': QotRight.to_string2(us_future_qot_right_cme),
            'us_future_qot_right_cbot': QotRight.to_string2(us_future_qot_right_cbot),
            'us_future_qot_right_nymex': QotRight.to_string2(us_future_qot_right_nymex),
            'us_future_qot_right_comex': QotRight.to_string2(us_future_qot_right_comex),
            'us_future_qot_right_cboe': QotRight.to_string2(us_future_qot_right_cboe),
            'cc_qot_right': QotRight.to_string2(cc_qot_right),
            'sg_stock_qot_right': QotRight.to_string2(sg_stock_qot_right),
            'my_stock_qot_right': QotRight.to_string2(my_stock_qot_right),
            'jp_stock_qot_right': QotRight.to_string2(jp_stock_qot_right),
            'ec_qot_right': QotRight.to_string2(ec_qot_right),
            "is_need_agree_disclaimer": is_need_agree_disclaimer,
            "user_id": user_id,
            "update_type": UpdateType.to_string2(update_type),
            "web_key": web_key,
            "sub_quota": sub_quota,
            "history_kl_quota": history_kl_quota,
        }
        return RET_OK, "", data


class GetCapitalDistributionQuery:
    """
    Query GetCapitalDistribution.
    个股资金分布
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, security_firm=SecurityFirm.NONE):
        """check stock_code 股票"""
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0
        market_code, stock_code = content

        # 开始组包
        from ..common.pb.Qot_GetCapitalDistribution_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetCapitalDistribution, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret = dict()
        #  流入资金额度，特大单 type=double
        ret["capital_in_super"] = rsp_pb.s2c.capitalInSuper if rsp_pb.s2c.HasField("capitalInSuper") else "N/A"
        #  流入资金额度，大单 type=double
        ret["capital_in_big"] = rsp_pb.s2c.capitalInBig
        #  流入资金额度，中单 type=double
        ret["capital_in_mid"] = rsp_pb.s2c.capitalInMid
        #  流入资金额度，小单 type=double
        ret["capital_in_small"] = rsp_pb.s2c.capitalInSmall
        #  流出资金额度，特大单 type=double
        ret["capital_out_super"] = rsp_pb.s2c.capitalOutSuper if rsp_pb.s2c.HasField("capitalOutSuper") else "N/A"
        #  流出资金额度，大单 type=double
        ret["capital_out_big"] = rsp_pb.s2c.capitalOutBig
        #  流出资金额度，中单 type=double
        ret["capital_out_mid"] = rsp_pb.s2c.capitalOutMid
        #  流出资金额度，小单 type=double
        ret["capital_out_small"] = rsp_pb.s2c.capitalOutSmall
        #  更新时间字符串 type=string
        ret["update_time"] = rsp_pb.s2c.updateTime
        return RET_OK, "", ret


class GetCapitalFlowQuery:
    """
    Query GetCapitalFlow.
    个股资金流入流出
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, start_date=None, end_date=None, period_type=PeriodType.INTRADAY, security_firm=SecurityFirm.NONE):
        # check period type
        if not PeriodType.if_has_key(period_type):
            error_str = ERROR_STR_PREFIX + "period_type is %s, which is not valid. (%s)" \
                % (period_type, PeriodType.get_all_keys())
            return RET_ERROR, error_str, None, 0, 0

        """check stock_code 股票"""
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0
        market_code, stock_code = content

        # 开始组包
        from ..common.pb.Qot_GetCapitalFlow_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        _, req.c2s.periodType = PeriodType.to_number(period_type)
        if start_date:
            req.c2s.beginTime = start_date
        if end_date:
            req.c2s.endTime = end_date
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetCapitalFlow, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = list()
        #  资金流向 type = Qot_GetCapitalFlow.CapitalFlowItem
        flow_item_list = rsp_pb.s2c.flowItemList
        #  数据最后有效时间字符串 type = string
        last_valid_time = rsp_pb.s2c.lastValidTime if rsp_pb.s2c.HasField("lastValidTime") else "N/A"
        for item in flow_item_list:
            data = dict()
            ret_list.append(data)
            #  净流入的资金额度 type = double
            data["in_flow"] = item.inFlow
            data["super_in_flow"] = item.superInFlow
            data["big_in_flow"] = item.bigInFlow
            data["mid_in_flow"] = item.midInFlow
            data["sml_in_flow"] = item.smlInFlow
            data["main_in_flow"] = item.mainInFlow if item.HasField("mainInFlow") else "N/A"
            #  开始时间字符串,以分钟为单位 type = string
            data["capital_flow_item_time"] = item.time
            data["last_valid_time"] = last_valid_time
        return RET_OK, "", ret_list


class GetFinancialsEarningsPriceMoveQuery:
    """
    Query `Qot_GetFinancialsEarningsPriceMove`。
    对应 Moomoo CEarningsMoveChartDataService::RequestReportCycleQuoteData（财报周期内价格/波动率表现）
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, period_count=None):
        """check stock_code 股票"""
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetFinancialsEarningsPriceMove_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if period_count is not None:
            req.c2s.periodCount = int(period_count)

        return pack_pb_req(req, ProtoId.Qot_GetFinancialsEarningsPriceMove, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        from ..common.constant import F10Type, EarningsPubTimeType
        ret_list = []
        for d in rsp_pb.s2c.detailList:
            price_info_index = d.priceInfoIndex if d.HasField("priceInfoIndex") else 0
            for idx, it in enumerate(d.itemList):
                row = {}
                if d.HasField("fiscalYear"):
                    row["fiscal_year"] = d.fiscalYear
                if d.HasField("financialType"):
                    row["financial_type"] = F10Type.to_string2(d.financialType)
                if d.HasField("pubTradingDay"):
                    row["pub_trading_day"] = d.pubTradingDay
                if d.HasField("pubType"):
                    row["pub_type"] = EarningsPubTimeType.to_string2(d.pubType)
                if d.HasField("priceInfoIndex"):
                    row["price_info_index"] = d.priceInfoIndex
                if d.HasField("periodText"):
                    row["period_text"] = d.periodText
                if d.HasField("pubTradingDayStr"):
                    row["pub_trading_day_str"] = d.pubTradingDayStr
                row["day_offset"] = idx - price_info_index
                if it.HasField("tradingDay"):
                    row["trading_day"] = it.tradingDay
                if it.HasField("tradingDayStr"):
                    row["trading_day_str"] = it.tradingDayStr
                if it.HasField("closePrice"):
                    row["close_price"] = it.closePrice
                if it.HasField("openPrice"):
                    row["open_price"] = it.openPrice
                if it.HasField("highestPrice"):
                    row["highest_price"] = it.highestPrice
                if it.HasField("lowestPrice"):
                    row["lowest_price"] = it.lowestPrice
                if it.HasField("lastClosePrice"):
                    row["last_close_price"] = it.lastClosePrice
                if it.HasField("optionIV"):
                    row["option_iv"] = it.optionIV
                if it.HasField("optionHV"):
                    row["option_hv"] = it.optionHV
                ret_list.append(row)

        return RET_OK, "", ret_list


class GetFinancialsEarningsPriceHistoryQuery:
    """
    Query `Qot_GetFinancialsEarningsPriceHistory`。
    对应 Moomoo CS_CmdID_PriceHistoryOnEarningsDays（财报日前后股价历史）
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):
        """check stock_code 股票"""
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetFinancialsEarningsPriceHistory_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetFinancialsEarningsPriceHistory, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        from ..common.constant import F10Type, EarningsPubTimeType
        ret_list = []
        for d in rsp_pb.s2c.detailList:
            base = {}
            if d.HasField("fiscalYear"):
                base["fiscal_year"] = d.fiscalYear
            if d.HasField("financialType"):
                base["financial_type"] = F10Type.to_string2(d.financialType)
            if d.HasField("periodText"):
                base["period_text"] = d.periodText
            if d.HasField("isCurrent"):
                base["is_current"] = d.isCurrent
            if d.HasField("pubTradingDay"):
                base["pub_trading_day"] = d.pubTradingDay
            if d.HasField("pubTradingDayStr"):
                base["pub_trading_day_str"] = d.pubTradingDayStr
            if d.HasField("pubTime"):
                base["pub_time"] = d.pubTime
            if d.HasField("pubTimeStr"):
                base["pub_time_str"] = d.pubTimeStr
            if d.HasField("pubType"):
                base["pub_type"] = EarningsPubTimeType.to_string2(d.pubType)
            if d.HasField("predictVolaRatioNewest"):
                base["predict_vola_ratio_newest"] = d.predictVolaRatioNewest
            if d.HasField("predictVolaRatioHighest"):
                base["predict_vola_ratio_highest"] = d.predictVolaRatioHighest
            if d.HasField("predictVolaValNewest"):
                base["predict_vola_val_newest"] = d.predictVolaValNewest
            if d.HasField("predictVolaValHighest"):
                base["predict_vola_val_highest"] = d.predictVolaValHighest
            if d.HasField("optionIVCrush"):
                base["option_iv_crush"] = d.optionIVCrush
            if d.HasField("optionStrikeDateIVCrush"):
                base["option_strike_date_iv_crush"] = d.optionStrikeDateIVCrush
            if d.HasField("priceInfo"):
                price_info = d.priceInfo
                if price_info.HasField("tradingDay"):
                    base["trading_day"] = price_info.tradingDay
                if price_info.HasField("tradingDayStr"):
                    base["trading_day_str"] = price_info.tradingDayStr
                if price_info.HasField("closePrice"):
                    base["close_price"] = price_info.closePrice
                if price_info.HasField("openPrice"):
                    base["open_price"] = price_info.openPrice
                if price_info.HasField("highestPrice"):
                    base["highest_price"] = price_info.highestPrice
                if price_info.HasField("lowestPrice"):
                    base["lowest_price"] = price_info.lowestPrice
                if price_info.HasField("lastClosePrice"):
                    base["last_close_price"] = price_info.lastClosePrice
                if price_info.HasField("volume"):
                    base["volume"] = price_info.volume
            if d.scheduleInfoList:
                for it in d.scheduleInfoList:
                    row = base.copy()
                    if it.HasField("delta"):
                        row["schedule_delta"] = it.delta
                    if it.HasField("closePrice"):
                        row["schedule_close_price"] = it.closePrice
                    ret_list.append(row)
            else:
                ret_list.append(base)

        return RET_OK, "", ret_list


class GetDelayStatisticsQuery:
    """
    Query GetDelayStatistics.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, type_list, qot_push_stage, segment_list, conn_id):
        """check type_list 统计数据类型，DelayStatisticsType"""
        """check qot_push_stage 行情推送统计的区间，行情推送统计时有效，QotPushStage"""
        """check segment_list 统计分段，默认100ms以下以2ms分段，100ms以上以500，1000，2000，-1分段，-1表示无穷大。"""

        # 开始组包
        from ..common.pb.GetDelayStatistics_pb2 import Request
        req = Request()
        for t in type_list:
            r, v = DelayStatisticsType.to_number(t)
            if r:
                req.c2s.typeList.append(v)

        r, v = QotPushStage.to_number(qot_push_stage)
        if r:
            req.c2s.qotPushStage = v

        for t in segment_list:
            req.c2s.segmentList.append(t)

        return pack_pb_req(req, ProtoId.GetDelayStatistics, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_dic = dict()
        #  行情推送延迟统计 type = GetDelayStatistics.DelayStatistics
        qot_push_statistics_list = rsp_pb.s2c.qotPushStatisticsList
        #  请求延迟统计 type = GetDelayStatistics.ReqReplyStatisticsItem
        req_reply_statistics_list = rsp_pb.s2c.reqReplyStatisticsList
        #  下单延迟统计 type = GetDelayStatistics.PlaceOrderStatisticsItem
        place_order_statistics_list = rsp_pb.s2c.placeOrderStatisticsList
        # 请求延迟统计  列表类型
        ret_list_req_reply_statistics_list = list()
        ret_dic["req_reply_statistics_list"] = ret_list_req_reply_statistics_list
        # 下单延迟统计  列表类型
        ret_list_place_order_statistics_list = list()
        ret_dic["place_order_statistics_list"] = ret_list_place_order_statistics_list

        # 行情推送延迟统计 总表  列表类型
        qot_push_all_statistics_list = list()
        ret_dic["qot_push_all_statistics_list"] = qot_push_all_statistics_list

        for item in qot_push_statistics_list:
            #  平均延迟和总包数加入总表
            info = dict()
            qot_push_all_statistics_list.append(info)

            #  行情推送类型,QotPushType type = int32
            qot_push_type = item.qotPushType
            info["qot_push_type"] = qot_push_type
            #  统计信息 type = GetDelayStatistics.DelayStatisticsItem
            item_list = item.itemList
            #  平均延迟 type = float
            delay_avg = item.delayAvg
            info["delay_avg"] = delay_avg
            #  总包数 type = int32
            count = item.count
            info["count"] = count
            #  区段列表
            ls = list()
            info["list"] = ls

            for sub_item in item_list:
                data = dict()
                ls.append(data)
                #  范围左闭右开，[begin,end)耗时范围起点，毫秒单位 type = int32
                data["begin"] = sub_item.begin
                #  耗时范围结束，毫秒单位 type = int32
                data["end"] = sub_item.end
                #  个数 type = int32
                data["count"] = sub_item.count
                #  占比, % type = float
                data["proportion"] = sub_item.proportion
                #  累计占比, % type = float
                data["cumulative_ratio"] = sub_item.cumulativeRatio
        for item in req_reply_statistics_list:
            data = dict()
            ret_list_req_reply_statistics_list.append(data)
            #  协议ID type = int32
            data["proto_id"] = item.protoID
            #  请求个数 type = int32
            data["count"] = item.count
            #  平均总耗时，毫秒单位 type = float
            data["total_cost_avg"] = item.totalCostAvg
            #  平均OpenD耗时，毫秒单位 type = float
            data["open_d_cost_avg"] = item.openDCostAvg
            #  平均网络耗时，非当时实际请求网络耗时，毫秒单位 type = float
            data["net_delay_avg"] = item.netDelayAvg
            #  是否本地直接回包，没有向服务器请求数据 type = bool
            data["is_local_reply"] = item.isLocalReply
        for item in place_order_statistics_list:
            data = dict()
            ret_list_place_order_statistics_list.append(data)
            #  订单ID type = string
            data["order_id"] = item.orderID
            #  总耗时，毫秒单位 type = float
            data["total_cost"] = item.totalCost
            #  OpenD耗时，毫秒单位 type = float
            data["open_d_cost"] = item.openDCost
            #  网络耗时，非当时实际请求网络耗时，毫秒单位 type = float
            data["net_delay"] = item.netDelay
            #  订单回包后到接收到订单下到交易所的耗时，毫秒单位 type = float
            data["update_cost"] = item.updateCost
        return RET_OK, "", ret_dic


class Verification:
    """
    拉验证码
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, verification_type, verification_op, code, conn_id):
        from ..common.pb.Verification_pb2 import Request
        req = Request()
        ret, data = VerificationType.to_number(verification_type)
        if ret:
            req.c2s.type = data
        else:
            return RET_ERROR, data, None, 0, 0

        ret, data = VerificationOp.to_number(verification_op)
        if ret:
            req.c2s.op = data
        else:
            return RET_ERROR, data, None, 0, 0

        if code is not None and len(code) != 0:
            req.c2s.code = code
        return pack_pb_req(req, ProtoId.Verification, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        return rsp_pb.retType, rsp_pb.retMsg, None

    """
    ===============================================================================
    ===============================================================================
    """


class ModifyUserSecurityQuery:
    """
    Query ModifyUserSecurity.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, group_name, op, code_list, conn_id, security_firm=SecurityFirm.NONE):
        """check group_name 分组名,有同名的返回首个"""
        """check op ModifyUserSecurityOp,操作类型"""
        """check code_list 新增或删除该分组下的股票"""
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))
        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None, 0, 0

        # 开始组包
        from ..common.pb.Qot_ModifyUserSecurity_pb2 import Request
        req = Request()
        req.c2s.groupName = group_name
        req.c2s.op = op
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_ModifyUserSecurity, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        return RET_OK, "", None


class GetUserSecurityQuery:
    """
    Query GetUserSecurity.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, group_name, conn_id, security_firm=SecurityFirm.NONE):
        """check group_name 分组名,有同名的返回首个"""
        # 开始组包
        from ..common.pb.Qot_GetUserSecurity_pb2 import Request
        req = Request()
        req.c2s.groupName = group_name
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetUserSecurity, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        #  自选股分组下的股票列表 type = Qot_Common.SecurityStaticInfo
        static_info_list = rsp_pb.s2c.staticInfoList
        #  基本股票静态信息 type = SecurityStaticBasic
        basic_info_list = [{
            "code": merge_qot_mkt_stock_str(record.basic.security.market,
                                            record.basic.security.code),
            "stock_id": record.basic.id,
            "name": record.basic.name,
            "lot_size": record.basic.lotSize,
            "stock_type": SecurityType.to_string2(record.basic.secType) if record.basic.HasField('secType') else 'N/A',# 初始化枚举类型,
            "stock_child_type": WrtType.to_string2(record.warrantExData.type) if record.warrantExData.HasField('type') else 'N/A',# 初始化枚举类型
            "stock_owner": merge_qot_mkt_stock_str(
                record.warrantExData.owner.market,
                record.warrantExData.owner.code) if record.HasField('warrantExData') else (
                merge_qot_mkt_stock_str(
                    record.optionExData.owner.market,
                    record.optionExData.owner.code) if record.HasField('optionExData')
                else ""),
            "listing_date": "N/A" if record.HasField('optionExData') else record.basic.listTime,
            "option_type": OptionType.to_string2(record.optionExData.type) if record.optionExData.HasField('type') else 'N/A',# 初始化枚举类型,
            "strike_time": record.optionExData.strikeTime,
            "strike_price": record.optionExData.strikePrice if record.HasField(
                'optionExData') else NoneDataType,
            "suspension": record.optionExData.suspend if record.HasField('optionExData') else NoneDataType,
            "delisting": record.basic.delisting if record.basic.HasField('delisting') else NoneDataType,
            "main_contract": record.futureExData.isMainContract,
            "last_trade_time": record.futureExData.lastTradeTime,
        } for record in static_info_list]
        return RET_OK, "", basic_info_list


class StockFilterQuery:
    """
    Query StockFilterQuery.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, filter_list, plate_code, begin, num, conn_id, security_firm=SecurityFirm.NONE):
        """check group_name 分组名,有同名的返回首个"""
        # 开始组包
        from ..common.pb.Qot_StockFilter_pb2 import Request
        req = Request()
        req.c2s.begin = begin
        req.c2s.num = num

        """拆解market"""
        r, req.c2s.market = Market.to_number(market)

        """拆解plate_code"""
        if plate_code is not None:
            ret, content = split_stock_str(plate_code)
            if ret != RET_OK:
                msg = str(content)
                error_str = ERROR_STR_PREFIX + msg
                return RET_ERROR, error_str, None, 0, 0
            market, code = content
            req.c2s.plate.code = code
            req.c2s.plate.market = market

        ret = RET_OK
        error_str = ""
        if filter_list is not None:
            for filter_item in filter_list:
                if isinstance(filter_item, SimpleFilter):
                    filter_req = req.c2s.baseFilterList.add()
                    ret, error_str = filter_item.fill_request_pb(filter_req)
                elif isinstance(filter_item, AccumulateFilter):
                    filter_req = req.c2s.accumulateFilterList.add()
                    ret, error_str = filter_item.fill_request_pb(filter_req)
                elif isinstance(filter_item, FinancialFilter):
                    filter_req = req.c2s.financialFilterList.add()
                    ret, error_str = filter_item.fill_request_pb(filter_req)
                elif isinstance(filter_item, PatternFilter):
                    filter_req = req.c2s.patternFilterList.add()
                    ret, error_str = filter_item.fill_request_pb(filter_req)
                elif isinstance(filter_item, CustomIndicatorFilter):
                    filter_req = req.c2s.customIndicatorFilterList.add()
                    ret, error_str = filter_item.fill_request_pb(filter_req)
                else:
                    ret = RET_ERROR
                    error_str = ERROR_STR_PREFIX + "the item in filter_list is wrong"

        if (ret == RET_ERROR):
            return RET_ERROR, error_str, None, 0, 0
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_StockFilter, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        #  是否最后一页了,false:非最后一页,还有窝轮记录未返回; true:已是最后一页 type = bool
        last_page = rsp_pb.s2c.lastPage
        #  该条件请求所有数据的个数 type = int32
        all_count = rsp_pb.s2c.allCount
        #   type = Qot_StockFilter.StockData
        data_list = rsp_pb.s2c.dataList
        ret_list = list()
        for item in data_list:
            data = FilterStockData(item)
            ret_list.append(data)
        return RET_OK, "", (last_page, all_count, ret_list)


class GetCodeChangeQuery:
    """
    Query GetCodeChange.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, time_filter_list, type_list, conn_id, security_firm=SecurityFirm.NONE):
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))
        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None, 0, 0

        # 开始组包
        from ..common.pb.Qot_GetCodeChange_pb2 import Request
        req = Request()
        req.c2s.placeHolder = 0
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code

        for type in type_list:
            _, n = CodeChangeType.to_number(type)
            req.c2s.typeList.append(n)

        for time_filter in time_filter_list:
            time_filter_inst = req.c2s.timeFilterList.add()
            _, time_filter_inst.type = TimeFilterType.to_number(time_filter.type)
            time_filter_inst.beginTime = time_filter.begin_time
            time_filter_inst.endTime = time_filter.end_time
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetCodeChange, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = list()
        #  股票代码更换信息，目前仅有港股数据 type = Qot_GetCodeChange.CodeChangeInfo
        code_change_list = rsp_pb.s2c.codeChangeList
        for item in code_change_list:
            data = {}
            #  CodeChangeType,代码变化或者新增临时代码的事件类型 type = int32
            data["code_change_info_type"] = CodeChangeType.to_string2(
                item.type)
            #  主代码，在创业板转主板中表示主板 type = code
            data["code"] = merge_qot_mkt_stock_str(
                item.security.market, item.security.code)
            #  关联代码，在创业板转主板中表示创业板，在剩余事件中表示临时代码 type = code
            data["related_code"] = merge_qot_mkt_stock_str(
                item.relatedSecurity.market, item.relatedSecurity.code)
            #  公布时间 type = string
            data["public_time"] = item.publicTime
            #  生效时间 type = string
            data["effective_time"] = item.effectiveTime
            #  结束时间，在创业板转主板事件不存在该字段，在剩余事件表示临时代码交易结束时间 type = string
            data["end_time"] = item.endTime
            ret_list.append(data)
        return RET_OK, "", ret_list


class GetIpoListQuery:
    """
    Query GetIpoListQuery.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, conn_id, market, security_firm=SecurityFirm.NONE):
        # 开始组包
        from ..common.pb.Qot_GetIpoList_pb2 import Request
        req = Request()
        _, req.c2s.market = Market.to_number(market)
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetIpoList, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = []
        for pb_item in rsp_pb.s2c.ipoList:
            data = {}

            set_item_from_pb(data, pb_item.basic, pb_field_map_BasicIpoData)
            if pb_item.HasField('cnExData'):
                set_item_from_pb(data, pb_item.cnExData, pb_field_map_CNIpoExData)
            else:
                set_item_none(data, pb_field_map_CNIpoExData)

            if pb_item.HasField('hkExData'):
                set_item_from_pb(data, pb_item.hkExData, pb_field_map_HKIpoExData)
            else:
                set_item_none(data, pb_field_map_HKIpoExData)

            if pb_item.HasField('usExData'):
                set_item_from_pb(data, pb_item.usExData, pb_field_map_USIpoExData)
            else:
                set_item_none(data, pb_field_map_USIpoExData)

            if pb_item.HasField('sgExData'):
                set_item_from_pb(data, pb_item.sgExData, pb_field_map_SGIpoExData)
            else:
                set_item_none(data, pb_field_map_SGIpoExData)

            if pb_item.HasField('myExData'):
                set_item_from_pb(data, pb_item.myExData, pb_field_map_MYIpoExData)
            else:
                set_item_none(data, pb_field_map_MYIpoExData)

            if pb_item.HasField('jpExData'):
                set_item_from_pb(data, pb_item.jpExData, pb_field_map_JPIpoExData)
            else:
                set_item_none(data, pb_field_map_JPIpoExData)

            ret_list.append(data)
        return RET_OK, "", ret_list

class GetFutureInfoQuery:
    """
    Query GetFutureInfo.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, conn_id, security_firm=SecurityFirm.NONE):
        """check code_list 股票列表"""
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))
        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None, 0, 0

        # 开始组包
        from ..common.pb.Qot_GetFutureInfo_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetFutureInfo, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = list()
        #  期货合约资料 type = Qot_GetFutureInfo.FutureInfo
        future_info_list = rsp_pb.s2c.futureInfoList
        for item in future_info_list:
            data = {}
            #  合约名称 type = string
            data['name'] = item.name
            #  合约代码 type = string
            data['code'] = merge_qot_mkt_stock_str(item.security.market,item.security.code)
            #  最后交易日，只有非主连期货合约才有该字段 type = string
            data['last_trade_time'] = item.lastTradeTime
            if item.HasField('owner'):
                data['owner'] = merge_qot_mkt_stock_str(item.owner.market,item.owner.code)
            else:
                data['owner'] = item.ownerOther
            #  交易所 type = string
            data['exchange'] = item.exchange
            #  合约类型 type = string
            data['type'] = item.contractType
            #  合约规模 type = double
            data['size'] = item.contractSize
            #  合约规模的单位 type = string
            data['size_unit'] = item.contractSizeUnit
            #  报价货币 type = string
            data['price_currency'] = item.quoteCurrency
            #  报价单位 type = string
            data['price_unit'] = item.quoteUnit
            #  最小变动单位 type = double
            data['min_change'] = item.minVar
            #  最小变动单位的单位 type = string
            data['min_change_unit'] = item.minVarUnit
            #  交易时间 type = Qot_GetFutureInfo.TradeTime
            trade_time = ''
            for time_range in item.tradeTime:
                if (len(trade_time) > 0):
                    trade_time += ', '
                begin_neg = time_range.begin < 0
                if begin_neg:
                    begin = time.strftime("%M:%S", time.localtime(24 * 60 + time_range.begin))
                else:
                    begin = time.strftime("%M:%S", time.localtime(time_range.begin))
                end = time.strftime("%M:%S", time.localtime(abs(time_range.end)))
                trade_time += '(%s%s - %s)' % (begin, '(T-1)' if begin_neg else '', end)

            data['trade_time'] = trade_time
            #  所在时区 type = string
            data['time_zone'] = item.timeZone
            #  交易所规格 type = string
            data['exchange_format_url'] = item.exchangeFormatUrl
            data['origin_code'] = merge_qot_mkt_stock_str(item.origin.market,item.origin.code)
            ret_list.append(data)
        return RET_OK, "", ret_list

class TestCmd:
    @classmethod
    def pack_req(cls, cmd, params):

        from ..common.pb.TestCmd_pb2 import Request
        req = Request()
        req.c2s.cmd = cmd
        req.c2s.params = params

        return pack_pb_req(req, ProtoId.TestCmd, 0)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Unpack the init connect response"""
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        res = {}
        if rsp_pb.HasField('s2c'):
            res['cmd'] = rsp_pb.s2c.cmd
            res['result'] = rsp_pb.s2c.result
        else:
            return RET_ERROR, "rsp_pb error", None

        return RET_OK, "", res


class UpdatePriceReminder:
    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Unpack the init connect response"""
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        res = {}
        if rsp_pb.HasField('s2c'):
            res['code'] = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                                  rsp_pb.s2c.security.code)
            res['name'] = rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else 'N/A'
            res['price'] = rsp_pb.s2c.price
            res['change_rate'] = rsp_pb.s2c.changeRate
            res['market_status'] = PriceReminderMarketStatus.to_string2(rsp_pb.s2c.marketStatus) if rsp_pb.s2c.HasField('marketStatus') else 'N/A' # 初始化枚举类型
            res['content'] = rsp_pb.s2c.content
            res['note'] = rsp_pb.s2c.note
            if rsp_pb.s2c.key is not None:
                res['key'] = rsp_pb.s2c.key
            if rsp_pb.s2c.type is not None:
                res['reminder_type'] = PriceReminderType.to_string2(rsp_pb.s2c.type) if rsp_pb.s2c.HasField('type') else 'N/A' # 初始化枚举类型
            if rsp_pb.s2c.setValue is not None:
                res['set_value'] = rsp_pb.s2c.setValue
            if rsp_pb.s2c.curValue is not None:
                res['cur_value'] = rsp_pb.s2c.curValue
        else:
            return RET_ERROR, "rsp_pb error", None

        return RET_OK, "", res


class UpdateOptionEvent:
    """Unpack push notification for option event (期权异动推送)."""

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        res = {}
        if rsp_pb.HasField('s2c'):
            res['owner_code'] = merge_qot_mkt_stock_str(
                int(rsp_pb.s2c.owner.market), rsp_pb.s2c.owner.code) if rsp_pb.s2c.HasField('owner') else NoneDataType
            res['option_code'] = merge_qot_mkt_stock_str(
                int(rsp_pb.s2c.option.market), rsp_pb.s2c.option.code) if rsp_pb.s2c.HasField('option') else NoneDataType
            res['message'] = rsp_pb.s2c.message if rsp_pb.s2c.HasField('message') else NoneDataType
        else:
            return RET_ERROR, "rsp_pb error", None

        return RET_OK, "", res


class SetPriceReminderQuery:
    """
    Query SetPriceReminder.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, op, key, reminder_type, reminder_freq, value, note, conn_id, reminder_session_list, security_firm=SecurityFirm.NONE):
        """check stock_code 股票"""
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0
        market_code, stock_code = content

        # 开始组包
        from ..common.pb.Qot_SetPriceReminder_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        _, req.c2s.op = SetPriceReminderOp.to_number(op)

        if key is not None:
            req.c2s.key = key
        if reminder_type is not None:
            _, req.c2s.type = PriceReminderType.to_number(reminder_type)
        if reminder_freq is not None:
            _, req.c2s.freq = PriceReminderFreq.to_number(reminder_freq)
        if value is not None:
            req.c2s.value = value
        if note is not None:
            req.c2s.note = note
        for _remind_session in reminder_session_list:
            _, _rs_enum = PriceReminderMarketStatus.to_number(_remind_session)
            req.c2s.reminderSessionList.append(_rs_enum)
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_SetPriceReminder, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        key = rsp_pb.s2c.key
        return RET_OK, "", key


class GetPriceReminderQuery:
    """
    Query GetPriceReminder.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, market, conn_id, security_firm=SecurityFirm.NONE):
        """check stock_code 查询股票下的到价提醒项"""
        market_code = 0
        stock_code = ''
        if code is not None:
            ret, content = split_stock_str(code)
            if ret == RET_ERROR:
                error_str = content
                return RET_ERROR, error_str, None, 0, 0
            market_code, stock_code = content

        # 开始组包
        from ..common.pb.Qot_GetPriceReminder_pb2 import Request
        req = Request()
        if code is not None:
            req.c2s.security.market = market_code
            req.c2s.security.code = stock_code
        elif market is not None and market is not Market.NONE:
            _, req.c2s.market = Market.to_number(market)
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetPriceReminder, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = list()
        #  到价提醒 type = Qot_GetPriceReminder.PriceReminder
        for item in rsp_pb.s2c.priceReminderList:
            stock_code = merge_qot_mkt_stock_str(item.security.market, item.security.code)
            stock_name = item.name if item.HasField('name') else 'N/A'
            #  提醒信息列表 type = Qot_GetPriceReminder.PriceReminderItem
            for sub_item in item.itemList:
                data = {}
                data["code"] = stock_code
                data["name"] = stock_name
                #  每个提醒的唯一标识 type = int64
                data["key"] = sub_item.key
                #  Qot_Common::PriceReminderType 提醒类型 type = int32
                data["reminder_type"] = PriceReminderType.to_string2(sub_item.type) if sub_item.HasField('type') else 'N/A' # 初始化枚举类型
                #  Qot_Common::PriceReminderFreq 提醒频率类型 type = int32
                data["reminder_freq"] = PriceReminderFreq.to_string2(sub_item.freq) if sub_item.HasField('freq') else 'N/A' # 初始化枚举类型
                #  提醒参数值 type = double
                data["value"] = sub_item.value
                #  该提醒设置是否生效。false不生效，true生效 type = bool
                data["enable"] = sub_item.isEnable
                #  用户设置到价提醒时的标注 type = string
                data["note"] = sub_item.note
                #  用户设置到价提醒时的时段信息 type = list
                data["reminder_session_list"] = []
                for _rs_enum in sub_item.reminderSessionList:
                    data["reminder_session_list"].append(PriceReminderMarketStatus.to_string2(_rs_enum))
                ret_list.append(data)
        return RET_OK, "", ret_list

class GetUserSecurityGroupQuery:
    """
    Query GetUserSecurityGroup.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, group_type, conn_id, security_firm=SecurityFirm.NONE):
        """check group_type GroupType,自选股分组类型。"""

        # 开始组包
        from ..common.pb.Qot_GetUserSecurityGroup_pb2 import Request
        req = Request()
        _, req.c2s.groupType = UserSecurityGroupType.to_number(group_type)
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetUserSecurityGroup, conn_id)


    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = list()
        #  自选股分组列表 type = Qot_GetUserSecurityGroup.GroupData
        group_list = rsp_pb.s2c.groupList
        for item in group_list:
            data = {}
            #  自选股分组名字 type = string
            data["group_name"] = item.groupName
            #  GroupType,自选股分组类型。 type = int32
            data["group_type"] = UserSecurityGroupType.to_string2(item.groupType) if item.HasField('groupType') else 'N/A' # 初始化枚举类型
            ret_list.append(data)

        return RET_OK, "", ret_list

class GetMarketStateQuery:
    """
    Query GetMarketState.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, conn_id, security_firm=SecurityFirm.NONE):
        """check code_list 股票列表"""
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))
        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None, 0, 0

        # 开始组包
        from ..common.pb.Qot_GetMarketState_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetMarketState, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = list()
        #  市场状态信息 type = Qot_GetMarketState.MarketInfo
        market_info_list = rsp_pb.s2c.marketInfoList
        for item in market_info_list:
            data = {}
            ret_list.append(data)
            #  股票代码 type = code
            data["code"] = merge_qot_mkt_stock_str(item.security.market, item.security.code)
            #  股票名称 type = string
            data["stock_name"] = item.name
            #  Qot_Common.QotMarketState,市场状态 type = int32
            data["market_state"] = MarketState.to_string2(item.marketState)if item.HasField('marketState') else 'N/A' # 初始化枚举类型
        return RET_OK, "", ret_list

class GetOptionExpirationDate:
    """
    Query GetOptionExpirationDate.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, index_option_type, conn_id, security_firm=SecurityFirm.NONE):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0

        market_code, stock_code = content

        r, index_option_type = IndexOptionType.to_number(index_option_type)
        if r is False:
            index_option_type = None

        from ..common.pb.Qot_GetOptionExpirationDate_pb2 import Request
        req = Request()
        req.c2s.owner.market = market_code
        req.c2s.owner.code = stock_code
        if index_option_type is not None:
            req.c2s.indexOptionType = index_option_type
        set_qot_header(req, security_firm)

        return pack_pb_req(req, ProtoId.Qot_GetOptionExpirationDate, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = list()
        expiration_date_list = rsp_pb.s2c.dateList
        for item in expiration_date_list:
            data = {}
            ret_list.append(data)
            data["strike_time"] = item.strikeTime if item.HasField('strikeTime') else ' '
            data["option_expiry_date_distance"] = item.optionExpiryDateDistance
            data["expiration_cycle"] = ExpirationCycle.to_string2(item.cycle) if item.HasField('cycle') else 'N/A'
        return RET_OK, "", ret_list


class GetOptionMarketStatistic:
    """Query Conversion for getting option market statistic data."""

    @classmethod
    def pack_req(cls, option_market, data_type, begin_time, end_time, next_page_key, conn_id):
        r, v = OptionMarket.to_number(option_market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of option_market param is wrong", None, 0, 0

        r, dt = OptionStatisticDataType.to_number(data_type)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of data_type param is wrong", None, 0, 0

        if begin_time is not None:
            ret, msg = normalize_date_format(begin_time)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            begin_time = msg

        if end_time is not None:
            ret, msg = normalize_date_format(end_time)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            end_time = msg

        from ..common.pb.Qot_GetOptionMarketStatistic_pb2 import Request
        req = Request()
        req.c2s.optionMarket = v
        req.c2s.dataType = dt
        if begin_time is not None:
            req.c2s.beginTime = begin_time
        if end_time is not None:
            req.c2s.endTime = end_time
        if next_page_key is not None:
            req.c2s.nextPageKey = next_page_key

        return pack_pb_req(req, ProtoId.Qot_GetOptionMarketStatistic, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        has_next = False
        next_page_key = None
        if rsp_pb.s2c.HasField('nextPageKey'):
            has_next = True
            next_page_key = bytes(rsp_pb.s2c.nextPageKey)

        ret_list = []
        for item in rsp_pb.s2c.statisticList:
            data = {
                "time": item.time,
                "timestamp": item.timestamp if item.HasField('timestamp') else NoneDataType,
                "call_value": item.callValue,
                "put_value": item.putValue,
                "total_value": item.totalValue if item.HasField('totalValue') else NoneDataType,
                "ratio": item.ratio if item.HasField('ratio') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, has_next, next_page_key)


class GetOptionUnderlyingHisStatistic:
    """Query Conversion for getting option underlying historical statistic data."""

    @classmethod
    def pack_req(cls, code, begin_time, end_time, index_option_type, next_page_key, conn_id):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        if begin_time is not None:
            ret, msg = normalize_date_format(begin_time)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            begin_time = msg

        if end_time is not None:
            ret, msg = normalize_date_format(end_time)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            end_time = msg

        from ..common.pb.Qot_GetOptionUnderlyingHisStatistic_pb2 import Request
        req = Request()
        req.c2s.owner.market = market_code
        req.c2s.owner.code = stock_code
        if index_option_type is not None:
            r, v = IndexOptionType.to_number(index_option_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of index_option_type param is wrong", None, 0, 0
            req.c2s.indexOptionType = v
        if begin_time is not None:
            req.c2s.beginTime = begin_time
        if end_time is not None:
            req.c2s.endTime = end_time
        if next_page_key is not None:
            req.c2s.nextPageKey = next_page_key

        return pack_pb_req(req, ProtoId.Qot_GetOptionUnderlyingHisStatistic, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        has_next = False
        next_page_key = None
        if rsp_pb.s2c.HasField('nextPageKey'):
            has_next = True
            next_page_key = bytes(rsp_pb.s2c.nextPageKey)

        stock_code = rsp_pb.s2c.code if rsp_pb.s2c.HasField('code') else NoneDataType
        stock_name = rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else NoneDataType

        ret_list = []
        for item in rsp_pb.s2c.statisticList:
            data = {
                "code": stock_code,
                "name": stock_name,
                "time": item.time,
                "timestamp": item.timestamp if item.HasField('timestamp') else NoneDataType,
                "option_volume": item.optionVolume if item.HasField('optionVolume') else NoneDataType,
                "call_volume": item.callVolume,
                "put_volume": item.putVolume,
                "put_call_volume_ratio": item.putCallVolumeRatio if item.HasField('putCallVolumeRatio') else NoneDataType,
                "option_open_interest": item.optionOpenInterest if item.HasField('optionOpenInterest') else NoneDataType,
                "call_open_interest": item.callOpenInterest,
                "put_open_interest": item.putOpenInterest,
                "put_call_open_interest_ratio": item.putCallOpenInterestRatio if item.HasField('putCallOpenInterestRatio') else NoneDataType,
                "underlying_price": item.underlyingPrice if item.HasField('underlyingPrice') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, has_next, next_page_key)


# HV 时间范围 → 列名后缀 映射
_HV_TIME_RANGE_SUFFIX = {
    Qot_OptionCommon_pb2.OptionHVTimeRange_30Day: '30d',
    Qot_OptionCommon_pb2.OptionHVTimeRange_60Day: '60d',
    Qot_OptionCommon_pb2.OptionHVTimeRange_90Day: '90d',
    Qot_OptionCommon_pb2.OptionHVTimeRange_120Day: '120d',
    Qot_OptionCommon_pb2.OptionHVTimeRange_365Day: '365d',
}


class GetOptionUnderlyingOverview:
    """Query Conversion for getting option underlying overview data in batch."""

    @classmethod
    def pack_req(cls, code_list, index_option_type, conn_id):
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                failure_tuple_list.append(content)
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        if len(failure_tuple_list) > 0:
            error_str = ERROR_STR_PREFIX + '\n'.join(failure_tuple_list)
            return RET_ERROR, error_str, None, 0, 0

        if len(stock_tuple_list) > 500:
            return RET_ERROR, ERROR_STR_PREFIX + "ownerList max count is 500", None, 0, 0

        from ..common.pb.Qot_GetOptionUnderlyingOverview_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            owner = req.c2s.ownerList.add()
            owner.market = market_code
            owner.code = stock_code
        if index_option_type is not None:
            r, v = IndexOptionType.to_number(index_option_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of index_option_type param is wrong", None, 0, 0
            req.c2s.indexOptionType = v

        return pack_pb_req(req, ProtoId.Qot_GetOptionUnderlyingOverview, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        ret_list = []
        for item in rsp_pb.s2c.underlyingDataList:
            data = {
                "code": item.code if item.HasField('code') else merge_qot_mkt_stock_str(int(item.owner.market), item.owner.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "call_volume": item.callVolume if item.HasField('callVolume') else NoneDataType,
                "put_volume": item.putVolume if item.HasField('putVolume') else NoneDataType,
                "call_open_interest": item.callOpenInterest if item.HasField('callOpenInterest') else NoneDataType,
                "put_open_interest": item.putOpenInterest if item.HasField('putOpenInterest') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "iv_rank": item.ivRank if item.HasField('ivRank') else NoneDataType,
                "iv_percentile": item.ivPercentile if item.HasField('ivPercentile') else NoneDataType,
                "pre_iv": item.preIV if item.HasField('preIV') else NoneDataType,
            }

            # 展平 HV 列表为独立列
            hv_map = {}
            for hv_item in item.hvList:
                suffix = _HV_TIME_RANGE_SUFFIX.get(hv_item.timeRange)
                if suffix:
                    hv_map['hv_' + suffix] = hv_item.hv
                    hv_map['hv_' + suffix + '_percentile'] = hv_item.hvPercentile if hv_item.HasField('hvPercentile') else NoneDataType

            for suffix in ['30d', '60d', '90d', '120d', '365d']:
                data['hv_' + suffix] = hv_map.get('hv_' + suffix, NoneDataType)
                data['hv_' + suffix + '_percentile'] = hv_map.get('hv_' + suffix + '_percentile', NoneDataType)

            ret_list.append(data)

        return RET_OK, "", ret_list


class GetOptionUnderlyingHisVolatility:
    """Query Conversion for getting option underlying historical volatility data."""

    @classmethod
    def pack_req(cls, code, begin_time, end_time, index_option_type, next_page_key, conn_id):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        if begin_time is not None:
            ret, msg = normalize_date_format(begin_time)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            begin_time = msg

        if end_time is not None:
            ret, msg = normalize_date_format(end_time)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            end_time = msg

        from ..common.pb.Qot_GetOptionUnderlyingHisVolatility_pb2 import Request
        req = Request()
        req.c2s.owner.market = market_code
        req.c2s.owner.code = stock_code
        if index_option_type is not None:
            r, v = IndexOptionType.to_number(index_option_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of index_option_type param is wrong", None, 0, 0
            req.c2s.indexOptionType = v
        if begin_time is not None:
            req.c2s.beginTime = begin_time
        if end_time is not None:
            req.c2s.endTime = end_time
        if next_page_key is not None:
            req.c2s.nextPageKey = next_page_key

        return pack_pb_req(req, ProtoId.Qot_GetOptionUnderlyingHisVolatility, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        has_next = False
        next_page_key = None
        if rsp_pb.s2c.HasField('nextPageKey'):
            has_next = True
            next_page_key = bytes(rsp_pb.s2c.nextPageKey)

        stock_code = rsp_pb.s2c.code if rsp_pb.s2c.HasField('code') else NoneDataType
        stock_name = rsp_pb.s2c.name if rsp_pb.s2c.HasField('name') else NoneDataType

        ret_list = []
        for item in rsp_pb.s2c.volatilityList:
            data = {
                "code": stock_code,
                "name": stock_name,
                "time": item.time,
                "timestamp": item.timestamp if item.HasField('timestamp') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "hv": item.hv if item.HasField('hv') else NoneDataType,
                "underlying_price": item.underlyingPrice if item.HasField('underlyingPrice') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, has_next, next_page_key)


class GetOptionUnderlyingRank:
    """Query Conversion for getting option underlying rank data."""

    @classmethod
    def pack_req(cls, option_market, sort_type, sort_direction, count, trading_date, filter_list, page, conn_id):
        r, v = OptionMarket.to_number(option_market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of option_market param is wrong", None, 0, 0

        r, st = UnderlyingRankSortType.to_number(sort_type)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_type param is wrong", None, 0, 0

        from ..common.pb.Qot_GetOptionUnderlyingRank_pb2 import Request
        req = Request()
        req.c2s.optionMarket = v
        req.c2s.sortType = st
        if sort_direction is not None:
            req.c2s.isAsc = bool(sort_direction)
        if count is not None:
            req.c2s.count = int(count)
        if trading_date is not None:
            ret, msg = normalize_date_format(trading_date)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            req.c2s.tradingDate = msg
        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0
        if page is not None:
            req.c2s.page = str(page)

        return pack_pb_req(req, ProtoId.Qot_GetOptionUnderlyingRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        s2c = rsp_pb.s2c
        trading_date = s2c.tradingDate if s2c.HasField('tradingDate') else NoneDataType
        trading_timestamp = s2c.tradingTimestamp if s2c.HasField('tradingTimestamp') else NoneDataType
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else NoneDataType

        ret_list = []
        for item in s2c.rankList:
            data = {
                "code": merge_qot_mkt_stock_str(int(item.owner.market), item.owner.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "total_volume": item.totalVolume if item.HasField('totalVolume') else NoneDataType,
                "total_open_interest": item.totalOpenInterest if item.HasField('totalOpenInterest') else NoneDataType,
                "volume_ratio": item.volumeRatio if item.HasField('volumeRatio') else NoneDataType,
                "open_interest_ratio": item.openInterestRatio if item.HasField('openInterestRatio') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "iv_rank": item.ivRank if item.HasField('ivRank') else NoneDataType,
                "iv_percentile": item.ivPercentile if item.HasField('ivPercentile') else NoneDataType,
                "price": item.price if item.HasField('price') else NoneDataType,
                "change_ratio": item.changeRate if item.HasField('changeRate') else NoneDataType,
                "iv_change": item.ivChange if item.HasField('ivChange') else NoneDataType,
                "hv": item.hv if item.HasField('hv') else NoneDataType,
                "hv_change": item.hvChange if item.HasField('hvChange') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "trading_date": trading_date,
                "trading_timestamp": trading_timestamp,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetOptionRank:
    """Query Conversion for getting option contract rank data."""

    @classmethod
    def pack_req(cls, option_market, sort_type, count, trading_date, sort_direction, page, filter_list, conn_id):
        r, v = OptionMarket.to_number(option_market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of option_market param is wrong", None, 0, 0

        r, rt = OptionRankType.to_number(sort_type)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_type param is wrong", None, 0, 0

        from ..common.pb.Qot_GetOptionRank_pb2 import Request
        req = Request()
        req.c2s.optionMarket = v
        req.c2s.sortType = rt
        if count is not None:
            req.c2s.count = int(count)
        if trading_date is not None:
            ret, msg = normalize_date_format(trading_date)
            if ret != RET_OK:
                return ret, msg, None, 0, 0
            req.c2s.tradingDate = msg
        if sort_direction is not None:
            req.c2s.isAsc = bool(sort_direction)
        if page is not None:
            req.c2s.page = str(page)
        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetOptionRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        s2c = rsp_pb.s2c
        trading_date = s2c.tradingDate if s2c.HasField('tradingDate') else NoneDataType
        trading_timestamp = s2c.tradingTimestamp if s2c.HasField('tradingTimestamp') else NoneDataType
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else NoneDataType

        ret_list = []
        for item in s2c.rankList:
            data = {
                "code": merge_qot_mkt_stock_str(int(item.option.market), item.option.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "option_type": OptionType.to_string2(item.optionType) if item.HasField('optionType') else NoneDataType,
                # 数据字段
                "oi_increment": item.oiIncrement if item.HasField('oiIncrement') else NoneDataType,
                "oi_decrement": item.oiDecrement if item.HasField('oiDecrement') else NoneDataType,
                "oi_market_cap_increment": item.oiMarketCapIncrement if item.HasField('oiMarketCapIncrement') else NoneDataType,
                "oi_market_cap_decrement": item.oiMarketCapDecrement if item.HasField('oiMarketCapDecrement') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "turnover": item.turnover if item.HasField('turnover') else NoneDataType,
                "open_interest": item.openInterest if item.HasField('openInterest') else NoneDataType,
                "open_interest_market_cap": item.openInterestMarketCap if item.HasField('openInterestMarketCap') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "option_price": item.optionPrice if item.HasField('optionPrice') else NoneDataType,
                "change_ratio": item.changeRate if item.HasField('changeRate') else NoneDataType,
                # 盘口
                "mid_price": item.midPrice if item.HasField('midPrice') else NoneDataType,
                "bid_price": item.bidPrice if item.HasField('bidPrice') else NoneDataType,
                "bid_volume": item.bidVolume if item.HasField('bidVolume') else NoneDataType,
                "ask_price": item.askPrice if item.HasField('askPrice') else NoneDataType,
                "ask_volume": item.askVolume if item.HasField('askVolume') else NoneDataType,
                # 希腊值
                "delta": item.delta if item.HasField('delta') else NoneDataType,
                "gamma": item.gamma if item.HasField('gamma') else NoneDataType,
                "theta": item.theta if item.HasField('theta') else NoneDataType,
                "vega": item.vega if item.HasField('vega') else NoneDataType,
                "rho": item.rho if item.HasField('rho') else NoneDataType,
                # 交易日
                "trading_date": trading_date,
                "trading_timestamp": trading_timestamp,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetOptionEventQuery:
    """Query Conversion for getting option event (期权异动) data."""

    @classmethod
    def pack_req(cls, option_market, count, page, filter_list, sort, conn_id):
        r, v = OptionMarket.to_number(option_market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of option_market param is wrong", None, 0, 0

        from ..common.pb.Qot_GetOptionEvent_pb2 import Request
        req = Request()
        req.c2s.optionMarket = v

        if count is not None:
            req.c2s.count = int(count)

        if page is not None and page != '':
            req.c2s.page = str(page)

        # 填充筛选条件
        if filter_list is not None:
            for filter_item in filter_list:
                if not isinstance(filter_item, OptionEventFilter):
                    return RET_ERROR, ERROR_STR_PREFIX + "the item in filter_list must be OptionEventFilter", None, 0, 0
                filter_req = req.c2s.filterList.add()
                ret, error_str = filter_item.fill_request_pb(filter_req)
                if ret == RET_ERROR:
                    return RET_ERROR, error_str, None, 0, 0

        # 填充排序条件
        if sort is not None:
            if not isinstance(sort, OptionEventSort):
                return RET_ERROR, ERROR_STR_PREFIX + "sort must be OptionEventSort", None, 0, 0
            ret, error_str = sort.fill_request_pb(req.c2s.sort)
            if ret == RET_ERROR:
                return RET_ERROR, error_str, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetOptionEvent, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else ''
        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        update_timestamp = s2c.updateTimestamp if s2c.HasField('updateTimestamp') else NoneDataType

        ret_list = []
        for item in s2c.eventList:
            data = {
                "option_code": merge_qot_mkt_stock_str(int(item.option.market), item.option.code) if item.HasField('option') else NoneDataType,
                "owner_code": merge_qot_mkt_stock_str(int(item.owner.market), item.owner.code) if item.HasField('owner') else NoneDataType,
                "symbol": item.symbol if item.HasField('symbol') else NoneDataType,
                # 成交信息
                "fill_time": item.fillTime if item.HasField('fillTime') else NoneDataType,
                "fill_timestamp": item.fillTimestamp if item.HasField('fillTimestamp') else NoneDataType,
                "ticker_type": EventTickerType.to_string2(item.tickerType) if item.HasField('tickerType') else NoneDataType,
                "price": item.price if item.HasField('price') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "turnover": item.turnover if item.HasField('turnover') else NoneDataType,
                # 期权合约属性
                "option_type": OptionType.to_string2(item.optionType) if item.HasField('optionType') else NoneDataType,
                "strike_price": item.strikePrice if item.HasField('strikePrice') else NoneDataType,
                "strike_time": item.strikeTime if item.HasField('strikeTime') else NoneDataType,
                "strike_timestamp": item.strikeTimestamp if item.HasField('strikeTimestamp') else NoneDataType,
                "dte": item.dte if item.HasField('dte') else NoneDataType,
                # 行情快照
                "underlying_price": item.underlyingPrice if item.HasField('underlyingPrice') else NoneDataType,
                "otm": item.otm if item.HasField('otm') else NoneDataType,
                "bid_price": item.bidPrice if item.HasField('bidPrice') else NoneDataType,
                "ask_price": item.askPrice if item.HasField('askPrice') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "total_volume": item.totalVolume if item.HasField('totalVolume') else NoneDataType,
                "total_open_interest": item.totalOpenInterest if item.HasField('totalOpenInterest') else NoneDataType,
                "vo_ratio": item.voRatio if item.HasField('voRatio') else NoneDataType,
                # 希腊值
                "delta": item.delta if item.HasField('delta') else NoneDataType,
                "gamma": item.gamma if item.HasField('gamma') else NoneDataType,
                "vega": item.vega if item.HasField('vega') else NoneDataType,
                "theta": item.theta if item.HasField('theta') else NoneDataType,
                "rho": item.rho if item.HasField('rho') else NoneDataType,
                # 市场情绪与订单分类
                "sentiment": EventMarketSentiment.to_string2(item.sentiment) if item.HasField('sentiment') else NoneDataType,
                "order_type_list": [AlertOrderType.to_string2(v) for v in item.orderTypeList] if len(item.orderTypeList) > 0 else NoneDataType,
                "strategy_type": EventTickerStrategy.to_string2(item.strategyType) if item.HasField('strategyType') else NoneDataType,
                # 关联信息
                "earnings_time": item.earningsTime if item.HasField('earningsTime') else NoneDataType,
                "earnings_pub_type": item.earningsPubType if item.HasField('earningsPubType') else NoneDataType,
                "corporate_action_list": [{"action_type": a.actionType if a.HasField('actionType') else NoneDataType,
                                           "action_time": a.actionTime if a.HasField('actionTime') else NoneDataType,
                                           "action_timestamp": a.actionTimestamp if a.HasField('actionTimestamp') else NoneDataType}
                                          for a in item.corporateActionList] if len(item.corporateActionList) > 0 else NoneDataType,
                "industry_plate_list": [merge_qot_mkt_stock_str(int(s.market), s.code) for s in item.industryPlateList] if len(item.industryPlateList) > 0 else NoneDataType,
                "concept_plate_list": [merge_qot_mkt_stock_str(int(s.market), s.code) for s in item.conceptPlateList] if len(item.conceptPlateList) > 0 else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count, update_timestamp)


class GetOptionEventAlertQuery:
    """Query for getting option event alert settings (期权异动提醒设置)."""

    @classmethod
    def pack_req(cls, count, page, conn_id):
        from ..common.pb.Qot_GetOptionEventAlert_pb2 import Request
        req = Request()

        if count is not None:
            req.c2s.count = int(count)
        if page is not None and page != '':
            req.c2s.page = str(page)

        return pack_pb_req(req, ProtoId.Qot_GetOptionEventAlert, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else ''
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.alertList:
            data = {
                "key": item.key if item.HasField('key') else NoneDataType,
                "enable": item.enable if item.HasField('enable') else NoneDataType,
                "option_market": OptionMarket.to_string2(item.optionMarket) if item.HasField('optionMarket') else NoneDataType,
                "watchlist_group_name": item.watchlistGroupName if item.HasField('watchlistGroupName') else NoneDataType,
                "underlying": merge_qot_mkt_stock_str(int(item.underlying.market), item.underlying.code) if item.HasField('underlying') else NoneDataType,
                "option_type": OptionType.to_string2(item.optionType) if item.HasField('optionType') else NoneDataType,
                "side_type_list": [EventTickerType.to_string2(v) for v in item.sideTypeList] if len(item.sideTypeList) > 0 else NoneDataType,
                "order_type_list": [AlertOrderType.to_string2(v) for v in item.orderTypeList] if len(item.orderTypeList) > 0 else NoneDataType,
                "market_cap_range_min": item.marketCapRange.filterMin.value if item.HasField('marketCapRange') and item.marketCapRange.HasField('filterMin') else NoneDataType,
                "market_cap_range_max": item.marketCapRange.filterMax.value if item.HasField('marketCapRange') and item.marketCapRange.HasField('filterMax') else NoneDataType,
                "market_cap_min_inclusive": item.marketCapRange.filterMin.includes if item.HasField('marketCapRange') and item.marketCapRange.HasField('filterMin') else NoneDataType,
                "market_cap_max_inclusive": item.marketCapRange.filterMax.includes if item.HasField('marketCapRange') and item.marketCapRange.HasField('filterMax') else NoneDataType,
                "expiry_days_range_min": item.expiryDaysRange.filterMin.value if item.HasField('expiryDaysRange') and item.expiryDaysRange.HasField('filterMin') else NoneDataType,
                "expiry_days_range_max": item.expiryDaysRange.filterMax.value if item.HasField('expiryDaysRange') and item.expiryDaysRange.HasField('filterMax') else NoneDataType,
                "expiry_days_min_inclusive": item.expiryDaysRange.filterMin.includes if item.HasField('expiryDaysRange') and item.expiryDaysRange.HasField('filterMin') else NoneDataType,
                "expiry_days_max_inclusive": item.expiryDaysRange.filterMax.includes if item.HasField('expiryDaysRange') and item.expiryDaysRange.HasField('filterMax') else NoneDataType,
                "price_range_min": item.priceRange.filterMin.value if item.HasField('priceRange') and item.priceRange.HasField('filterMin') else NoneDataType,
                "price_range_max": item.priceRange.filterMax.value if item.HasField('priceRange') and item.priceRange.HasField('filterMax') else NoneDataType,
                "price_min_inclusive": item.priceRange.filterMin.includes if item.HasField('priceRange') and item.priceRange.HasField('filterMin') else NoneDataType,
                "price_max_inclusive": item.priceRange.filterMax.includes if item.HasField('priceRange') and item.priceRange.HasField('filterMax') else NoneDataType,
                "size_range_min": item.sizeRange.filterMin.value if item.HasField('sizeRange') and item.sizeRange.HasField('filterMin') else NoneDataType,
                "size_range_max": item.sizeRange.filterMax.value if item.HasField('sizeRange') and item.sizeRange.HasField('filterMax') else NoneDataType,
                "size_min_inclusive": item.sizeRange.filterMin.includes if item.HasField('sizeRange') and item.sizeRange.HasField('filterMin') else NoneDataType,
                "size_max_inclusive": item.sizeRange.filterMax.includes if item.HasField('sizeRange') and item.sizeRange.HasField('filterMax') else NoneDataType,
                "premium_range_min": item.premiumRange.filterMin.value if item.HasField('premiumRange') and item.premiumRange.HasField('filterMin') else NoneDataType,
                "premium_range_max": item.premiumRange.filterMax.value if item.HasField('premiumRange') and item.premiumRange.HasField('filterMax') else NoneDataType,
                "premium_min_inclusive": item.premiumRange.filterMin.includes if item.HasField('premiumRange') and item.premiumRange.HasField('filterMin') else NoneDataType,
                "premium_max_inclusive": item.premiumRange.filterMax.includes if item.HasField('premiumRange') and item.premiumRange.HasField('filterMax') else NoneDataType,
                "iv_range_min": item.ivRange.filterMin.value if item.HasField('ivRange') and item.ivRange.HasField('filterMin') else NoneDataType,
                "iv_range_max": item.ivRange.filterMax.value if item.HasField('ivRange') and item.ivRange.HasField('filterMax') else NoneDataType,
                "iv_min_inclusive": item.ivRange.filterMin.includes if item.HasField('ivRange') and item.ivRange.HasField('filterMin') else NoneDataType,
                "iv_max_inclusive": item.ivRange.filterMax.includes if item.HasField('ivRange') and item.ivRange.HasField('filterMax') else NoneDataType,
                "earnings_date_begin": item.earningsDateBegin if item.HasField('earningsDateBegin') else NoneDataType,
                "earnings_date_end": item.earningsDateEnd if item.HasField('earningsDateEnd') else NoneDataType,
                "note": item.note if item.HasField('note') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (next_page, all_count, ret_list)


class SetOptionEventAlertQuery:
    """Query for setting option event alert (设置期权异动提醒)."""

    @classmethod
    def pack_req(cls, op, alert_list, conn_id):
        from ..common.pb.Qot_SetOptionEventAlert_pb2 import Request
        req = Request()

        r, v = AlertOpType.to_number(op)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of op param is wrong", None, 0, 0
        req.c2s.operType = v

        if alert_list is not None:
            for alert_item in alert_list:
                if not isinstance(alert_item, OptionEventAlertItem):
                    return RET_ERROR, ERROR_STR_PREFIX + "alert_list items must be OptionEventAlertItem", None, 0, 0
                pb_item = req.c2s.alertList.add()
                ret, error_str = alert_item.fill_request_pb(pb_item)
                if ret == RET_ERROR:
                    return RET_ERROR, error_str, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_SetOptionEventAlert, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        return RET_OK, "", None


class GetOptionZeroDteScreenerQuery:
    """Query for getting zero-DTE option underlying screener (末日期权标的筛选)."""

    @classmethod
    def pack_req(cls, market, sort_type, is_asc, count, page, filter_list, conn_id):
        from ..common.pb.Qot_GetOptionZeroDteScreener_pb2 import Request
        req = Request()

        r, v = OptionMarket.to_number(market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of market param is wrong", None, 0, 0
        req.c2s.optionMarket = v

        if sort_type is not None:
            r, v = ZeroDteSortType.to_number(sort_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_type param is wrong", None, 0, 0
            req.c2s.sortType = v

        if is_asc is not None:
            req.c2s.isAsc = bool(is_asc)

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = str(page)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetOptionZeroDteScreener, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        update_timestamp = s2c.updateTimestamp if s2c.HasField('updateTimestamp') else 0

        ret_list = []
        for item in s2c.itemList:
            chain_info_data = NoneDataType
            if item.HasField('chainInfo'):
                ci = item.chainInfo
                chain_info_data = {
                    "strike_date_timestamp": ci.strikeDateTimestamp if ci.HasField('strikeDateTimestamp') else NoneDataType,
                    "product_code": ci.productCode if ci.HasField('productCode') else NoneDataType,
                    "multiplier": ci.multiplier if ci.HasField('multiplier') else NoneDataType,
                    "contract_share_size": ci.contractShareSize if ci.HasField('contractShareSize') else NoneDataType,
                    "expiration_type": ci.expirationType if ci.HasField('expirationType') else NoneDataType,
                    "underlying": merge_qot_mkt_stock_str(int(ci.underlying.market), ci.underlying.code) if ci.HasField('underlying') else NoneDataType,
                }

            data = {
                "owner": merge_qot_mkt_stock_str(int(item.owner.market), item.owner.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "price": item.price if item.HasField('price') else NoneDataType,
                "change_ratio": item.changeRate if item.HasField('changeRate') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "iv_rank": item.ivRank if item.HasField('ivRank') else NoneDataType,
                "iv_percentile": item.ivPercentile if item.HasField('ivPercentile') else NoneDataType,
                "hv": item.hv if item.HasField('hv') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "open_interest": item.openInterest if item.HasField('openInterest') else NoneDataType,
                "last_trading_time": item.lastTradingTime if item.HasField('lastTradingTime') else NoneDataType,
                "earnings_timestamp": item.earningsTimestamp if item.HasField('earningsTimestamp') else NoneDataType,
                "earnings_time": item.earningsTime if item.HasField('earningsTime') else NoneDataType,
                "earnings_pub_type": EarningsPubType.to_string2(item.earningsPubType) if item.HasField('earningsPubType') else NoneDataType,
                "chain_info": chain_info_data,
            }
            ret_list.append(data)

        return RET_OK, "", (next_page, update_timestamp, ret_list)


class GetOptionZeroDteContractQuery:
    """Query for getting zero-DTE option contract list (末日期权合约列表)."""

    @classmethod
    def pack_req(cls, owner, strike_date_timestamp, chain_info, sort_type, is_asc, filter_list, conn_id):
        from ..common.pb.Qot_GetOptionZeroDteContract_pb2 import Request
        req = Request()

        ret, content = split_stock_str(owner)
        if ret != RET_OK:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content
        req.c2s.owner.market = market_code
        req.c2s.owner.code = stock_code

        req.c2s.strikeDateTimestamp = int(strike_date_timestamp)

        if chain_info is None or not isinstance(chain_info, dict):
            return RET_ERROR, ERROR_STR_PREFIX + "chain_info is required and must be a dict", None, 0, 0
        ci = req.c2s.chainInfo
        if 'strike_date_timestamp' in chain_info and chain_info['strike_date_timestamp'] is not None:
            ci.strikeDateTimestamp = int(chain_info['strike_date_timestamp'])
        if 'product_code' in chain_info and chain_info['product_code'] is not None:
            ci.productCode = str(chain_info['product_code'])
        if 'multiplier' in chain_info and chain_info['multiplier'] is not None:
            ci.multiplier = float(chain_info['multiplier'])
        if 'contract_share_size' in chain_info and chain_info['contract_share_size'] is not None:
            ci.contractShareSize = float(chain_info['contract_share_size'])
        if 'expiration_type' in chain_info and chain_info['expiration_type'] is not None:
            ci.expirationType = int(chain_info['expiration_type'])
        if 'underlying' in chain_info and chain_info['underlying'] is not None:
            ret2, content2 = split_stock_str(chain_info['underlying'])
            if ret2 == RET_OK:
                ci.underlying.market = content2[0]
                ci.underlying.code = content2[1]

        if sort_type is not None:
            r, v = ZeroDteContractSortType.to_number(sort_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_type param is wrong", None, 0, 0
            req.c2s.sortType = v

        if is_asc is not None:
            req.c2s.isAsc = bool(is_asc)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetOptionZeroDteContract, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.itemList:
            data = {
                "option": merge_qot_mkt_stock_str(int(item.option.market), item.option.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "option_type": OptionType.to_string2(item.optionType) if item.HasField('optionType') else NoneDataType,
                "option_price": item.optionPrice if item.HasField('optionPrice') else NoneDataType,
                "change_ratio": item.changeRate if item.HasField('changeRate') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "open_interest": item.openInterest if item.HasField('openInterest') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "delta": item.delta if item.HasField('delta') else NoneDataType,
                "gamma": item.gamma if item.HasField('gamma') else NoneDataType,
                "vega": item.vega if item.HasField('vega') else NoneDataType,
                "theta": item.theta if item.HasField('theta') else NoneDataType,
                "rho": item.rho if item.HasField('rho') else NoneDataType,
                "buy_break_even_point": item.buyBreakEvenPoint if item.HasField('buyBreakEvenPoint') else NoneDataType,
                "buy_to_bep": item.buyToBep if item.HasField('buyToBep') else NoneDataType,
                "buy_profit_probability": item.buyProfitProbability if item.HasField('buyProfitProbability') else NoneDataType,
                "sell_profit_probability": item.sellProfitProbability if item.HasField('sellProfitProbability') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", ret_list


class GetOptionEarningsScreenerQuery:
    """Query for getting option earnings screener (财报标的筛选)."""

    @classmethod
    def pack_req(cls, market, sort_type, is_asc, count, page, filter_list, conn_id):
        from ..common.pb.Qot_GetOptionEarningsScreener_pb2 import Request
        req = Request()

        r, v = OptionMarket.to_number(market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of market param is wrong", None, 0, 0
        req.c2s.optionMarket = v

        if sort_type is not None:
            r, v = EarningsSortType.to_number(sort_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_type param is wrong", None, 0, 0
            req.c2s.sortType = v

        if is_asc is not None:
            req.c2s.isAsc = bool(is_asc)

        if count is not None:
            req.c2s.count = int(count)

        if page is not None and page != '':
            req.c2s.page = str(page)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetOptionEarningsScreener, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else ''
        update_timestamp = s2c.updateTimestamp if s2c.HasField('updateTimestamp') else 0
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.itemList:
            data = {
                "owner": merge_qot_mkt_stock_str(int(item.owner.market), item.owner.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "price": item.price if item.HasField('price') else NoneDataType,
                "change_ratio": item.changeRate if item.HasField('changeRate') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "iv_rank": item.ivRank if item.HasField('ivRank') else NoneDataType,
                "iv_percentile": item.ivPercentile if item.HasField('ivPercentile') else NoneDataType,
                "hv": item.hv if item.HasField('hv') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "open_interest": item.openInterest if item.HasField('openInterest') else NoneDataType,
                "earnings_timestamp": item.earningsTimestamp if item.HasField('earningsTimestamp') else NoneDataType,
                "earnings_time": item.earningsTime if item.HasField('earningsTime') else NoneDataType,
                "earnings_pub_type": EarningsPubType.to_string2(item.earningsPubType) if item.HasField('earningsPubType') else NoneDataType,
                "earnings_quarter": item.earningsQuarter if item.HasField('earningsQuarter') else NoneDataType,
                "last_report_iv_crush": item.lastReportIvCrush if item.HasField('lastReportIvCrush') else NoneDataType,
                "history_report_iv_crush": item.historyReportIvCrush if item.HasField('historyReportIvCrush') else NoneDataType,
                "last_report_chg_ratio": item.lastReportChgRate if item.HasField('lastReportChgRate') else NoneDataType,
                "history_report_chg_ratio": item.historyReportChgRate if item.HasField('historyReportChgRate') else NoneDataType,
                "estimate_eps_yoy": item.estimateEpsYoy if item.HasField('estimateEpsYoy') else NoneDataType,
                "estimate_revenue_yoy": item.estimateRevenueYoy if item.HasField('estimateRevenueYoy') else NoneDataType,
                "expected_move_ratio": item.expectedMoveRatio if item.HasField('expectedMoveRatio') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (next_page, update_timestamp, all_count, ret_list)


class GetOptionSellerScreenerQuery:
    """Query for getting option seller screener (期权卖方筛选)."""

    @classmethod
    def pack_req(cls, market, seller_type, sort_type, is_asc, filter_list, conn_id):
        from ..common.pb.Qot_GetOptionSellerScreener_pb2 import Request
        req = Request()

        r, v = OptionMarket.to_number(market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of market param is wrong", None, 0, 0
        req.c2s.optionMarket = v

        r, v = SellerType.to_number(seller_type)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of seller_type param is wrong", None, 0, 0
        req.c2s.sellerType = v

        if sort_type is not None:
            r, v = SellerSortType.to_number(sort_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_type param is wrong", None, 0, 0
            req.c2s.sortType = v

        if is_asc is not None:
            req.c2s.isAsc = bool(is_asc)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetOptionSellerScreener, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c

        ret_list = []
        for item in s2c.itemList:
            data = {
                "option": merge_qot_mkt_stock_str(int(item.option.market), item.option.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "option_type": OptionType.to_string2(item.optionType) if item.HasField('optionType') else NoneDataType,
                "strike_price": item.strikePrice if item.HasField('strikePrice') else NoneDataType,
                "strike_time": item.strikeTime if item.HasField('strikeTime') else NoneDataType,
                "strike_timestamp": item.strikeTimestamp if item.HasField('strikeTimestamp') else NoneDataType,
                "left_days": item.leftDays if item.HasField('leftDays') else NoneDataType,
                "option_price": item.optionPrice if item.HasField('optionPrice') else NoneDataType,
                "stock_price": item.stockPrice if item.HasField('stockPrice') else NoneDataType,
                "premium": item.premium if item.HasField('premium') else NoneDataType,
                "otm_degree": item.otmDegree if item.HasField('otmDegree') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "interval_return": item.intervalReturn if item.HasField('intervalReturn') else NoneDataType,
                "annualized_return": item.annualizedReturn if item.HasField('annualizedReturn') else NoneDataType,
                "itm_probability": item.itmProbability if item.HasField('itmProbability') else NoneDataType,
                "striked_interval_return": item.strikedIntervalReturn if item.HasField('strikedIntervalReturn') else NoneDataType,
                "striked_annualized_return": item.strikedAnnualizedReturn if item.HasField('strikedAnnualizedReturn') else NoneDataType,
                "owner": merge_qot_mkt_stock_str(int(item.owner.market), item.owner.code) if item.HasField('owner') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", ret_list


class GetEarningsCalendarQuery:
    """Query for getting earnings calendar (财报日历)."""

    @classmethod
    def pack_req(cls, market, sort_type, begin_date, end_date, filter_list, conn_id):
        from ..common.pb.Qot_GetEarningsCalendar_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)

        if sort_type is not None:
            r, v = EarningsCalendarSortType.to_number(sort_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_type param is wrong", None, 0, 0
            req.c2s.sortType = v

        if begin_date is not None and begin_date != '':
            req.c2s.beginDate = str(begin_date)

        if end_date is not None and end_date != '':
            req.c2s.endDate = str(end_date)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetEarningsCalendar, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c

        ret_list = []
        for item in s2c.itemList:
            # 拆分预测数据列表为具体字段
            eps_actual = NoneDataType
            eps_predict = NoneDataType
            revenue_actual = NoneDataType
            revenue_predict = NoneDataType
            ebit_actual = NoneDataType
            ebit_predict = NoneDataType
            for est in item.estimateList:
                est_type = EarningsCalendarEstimateType.to_string2(est.estimateType) if est.HasField('estimateType') else None
                actual = est.actualValue if est.HasField('actualValue') else NoneDataType
                predict = est.predictValue if est.HasField('predictValue') else NoneDataType
                if est_type == EarningsCalendarEstimateType.EPS:
                    eps_actual = actual
                    eps_predict = predict
                elif est_type == EarningsCalendarEstimateType.REVENUE:
                    revenue_actual = actual
                    revenue_predict = predict
                elif est_type == EarningsCalendarEstimateType.EBIT:
                    ebit_actual = actual
                    ebit_predict = predict

            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "earnings_date": item.earningsDate if item.HasField('earningsDate') else NoneDataType,
                "earnings_timestamp": item.earningsTimestamp if item.HasField('earningsTimestamp') else NoneDataType,
                "pub_type": EarningsCalendarPubType.to_string2(item.pubType) if item.HasField('pubType') else NoneDataType,
                "period_text": item.periodText if item.HasField('periodText') else NoneDataType,
                "eps_actual": eps_actual,
                "eps_predict": eps_predict,
                "revenue_actual": revenue_actual,
                "revenue_predict": revenue_predict,
                "ebit_actual": ebit_actual,
                "ebit_predict": ebit_predict,
                "option_volume": item.optionVolume if item.HasField('optionVolume') else NoneDataType,
                "iv": item.iv if item.HasField('iv') else NoneDataType,
                "iv_rank": item.ivRank if item.HasField('ivRank') else NoneDataType,
                "iv_percentile": item.ivPercentile if item.HasField('ivPercentile') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "price": item.price if item.HasField('price') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", ret_list


class GetMacroIndicatorListQuery:
    """Query for getting macro indicator list (宏观指标列表)."""

    @classmethod
    def pack_req(cls, region, conn_id):
        from ..common.pb.Qot_GetMacroIndicatorList_pb2 import Request
        req = Request()

        r, v = MacroRegion.to_number(region)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of region param is wrong", None, 0, 0
        req.c2s.region = v

        return pack_pb_req(req, ProtoId.Qot_GetMacroIndicatorList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c

        ret_list = []
        for category in s2c.indicatorList:
            category_name = category.categoryName
            for indicator in category.indicatorList:
                data = {
                    "category_name": category_name,
                    "indicator_id": indicator.indicatorId,
                    "name": indicator.name if indicator.HasField('name') else NoneDataType,
                }
                ret_list.append(data)

        return RET_OK, "", ret_list


class GetMacroIndicatorHistoryQuery:
    """Query for getting macro indicator history (宏观指标历史数据)."""

    @classmethod
    def pack_req(cls, indicator_id, time, max_count, conn_id):
        from ..common.pb.Qot_GetMacroIndicatorHistory_pb2 import Request
        req = Request()

        req.c2s.indicatorId = int(indicator_id)

        if time is not None and time != '':
            req.c2s.time = str(time)

        if max_count is not None:
            req.c2s.maxCount = int(max_count)

        return pack_pb_req(req, ProtoId.Qot_GetMacroIndicatorHistory, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c

        ret_list = []
        for point in s2c.dataList:
            data = {
                "data_time": point.dataTime if point.HasField('dataTime') else NoneDataType,
                "release_time": point.releaseTime if point.HasField('releaseTime') else NoneDataType,
                "value": point.value if point.HasField('value') else NoneDataType,
                "predict_value": point.predictValue if point.HasField('predictValue') else NoneDataType,
                "previous_value": point.previousValue if point.HasField('previousValue') else NoneDataType,
                "unit_type": MacroDataUnitType.to_string2(point.unitType) if point.HasField('unitType') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", ret_list


class GetFedWatchTargetRateQuery:
    """Query for getting FedWatch target rate probabilities (FedWatch目标利率概率)."""

    @classmethod
    def pack_req(cls, conn_id):
        from ..common.pb.Qot_GetFedWatchTargetRate_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        return pack_pb_req(req, ProtoId.Qot_GetFedWatchTargetRate, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c

        ret_list = []
        for meeting in s2c.meetingList:
            meeting_date = meeting.meetingDate
            for item in meeting.targetRateList:
                data = {
                    "meeting_date": meeting_date,
                    "target_range": item.targetRange,
                    "probability": item.probability,
                }
                ret_list.append(data)

        return RET_OK, "", ret_list


class GetFedWatchDotPlotQuery:
    """Query for getting FedWatch dot plot (FedWatch点阵图)."""

    @classmethod
    def pack_req(cls, conn_id):
        from ..common.pb.Qot_GetFedWatchDotPlot_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        return pack_pb_req(req, ProtoId.Qot_GetFedWatchDotPlot, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        current_rate = s2c.currentRate if s2c.HasField('currentRate') else NoneDataType

        ret_list = []
        for year_data in s2c.yearList:
            year = year_data.year
            median_rate = year_data.medianRate if year_data.HasField('medianRate') else NoneDataType
            for dot in year_data.dotList:
                data = {
                    "year": year,
                    "rate": dot.rate,
                    "vote_count": dot.voteCount,
                    "is_median": dot.isMedian if dot.HasField('isMedian') else False,
                    "median_rate": median_rate,
                    "current_rate": current_rate,
                }
                ret_list.append(data)

        return RET_OK, "", ret_list


class GetEconomicCalendarQuery:
    """Query for getting economic calendar (经济事件日历)."""

    @classmethod
    def pack_req(cls, begin_date, end_date, market_list, importance, count, next_page, conn_id):
        from ..common.pb.Qot_GetEconomicCalendar_pb2 import Request
        req = Request()

        req.c2s.beginDate = begin_date

        if end_date is not None:
            req.c2s.endDate = end_date

        if market_list is not None:
            for market in market_list:
                r, v = Market.to_number(market)
                if r is False:
                    return RET_ERROR, ERROR_STR_PREFIX + "the type of market param is wrong", None, 0, 0
                req.c2s.marketList.append(v)

        if importance is not None:
            r, v = EconomicImportance.to_number(importance)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of importance param is wrong", None, 0, 0
            req.c2s.importance = v

        if count is not None:
            req.c2s.count = int(count)

        if next_page is not None:
            req.c2s.nextPage = next_page

        return pack_pb_req(req, ProtoId.Qot_GetEconomicCalendar, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        has_more = s2c.hasMore if s2c.HasField('hasMore') else False

        ret_list = []
        for item in s2c.itemList:
            data = {
                "title": item.title if item.HasField('title') else NoneDataType,
                "timestamp": item.timestamp if item.HasField('timestamp') else NoneDataType,
                "country": item.country if item.HasField('country') else NoneDataType,
                "star": EconomicImportance.to_string2(item.star) if item.HasField('star') else NoneDataType,
                "previous": item.previous if item.HasField('previous') else "--",
                "consensus": item.consensus if item.HasField('consensus') else "--",
                "actual": item.actual if item.HasField('actual') else "--",
            }
            ret_list.append(data)

        return RET_OK, "", (next_page, has_more, ret_list)


class GetEarningsBeatRankQuery:
    """Query for getting earnings beat rank (盈利超预期排名)."""

    @classmethod
    def pack_req(cls, market, beat_type, count, term, filter_list, sort_field, conn_id):
        from ..common.pb.Qot_GetEarningsBeatRank_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)

        r, v = BeatType.to_number(beat_type)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of beat_type param is wrong", None, 0, 0
        req.c2s.beatType = v

        if count is not None:
            req.c2s.count = int(count)

        if term is not None:
            r, v = BeatTerm.to_number(term)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of term param is wrong", None, 0, 0
            req.c2s.term = v

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        if sort_field is not None:
            r, v = EarningsBeatSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        return pack_pb_req(req, ProtoId.Qot_GetEarningsBeatRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c

        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "industry": item.industry if item.HasField('industry') else NoneDataType,
                "cur_price": item.curPrice if item.HasField('curPrice') else NoneDataType,
                "last_close_price": item.lastClosePrice if item.HasField('lastClosePrice') else NoneDataType,
                "change_rate": item.changeRate if item.HasField('changeRate') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "pe_ttm": item.peTTM if item.HasField('peTTM') else NoneDataType,
                "dividends_ttm": item.dividendsTTM if item.HasField('dividendsTTM') else NoneDataType,
                "released_date": item.releasedDate if item.HasField('releasedDate') else NoneDataType,
                "beat_ratio": item.beatRatio if item.HasField('beatRatio') else NoneDataType,
                "actual": item.actual if item.HasField('actual') else NoneDataType,
                "estimate": item.estimate if item.HasField('estimate') else NoneDataType,
                "yoy": item.yoy if item.HasField('yoy') else NoneDataType,
                "yoy_growth": item.yoyGrowth if item.HasField('yoyGrowth') else NoneDataType,
                "earning_day_chg": item.earningDayChg if item.HasField('earningDayChg') else NoneDataType,
                "term": item.term if item.HasField('term') else NoneDataType,
                "detail_post_period": PostPeriodType.to_string2(item.detailPostPeriod) if item.HasField('detailPostPeriod') else NoneDataType,
            }
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetDividendRankQuery:
    """Query for getting dividend rank (股息排行)."""

    @classmethod
    def pack_req(cls, market, rank_type, count, filter_list, sort_field, conn_id):
        from ..common.pb.Qot_GetDividendRank_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)

        r, v = DividendRankType.to_number(rank_type)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of rank_type param is wrong", None, 0, 0
        req.c2s.rankType = v

        if count is not None:
            req.c2s.count = int(count)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        if sort_field is not None:
            r, v = DividendRankSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        return pack_pb_req(req, ProtoId.Qot_GetDividendRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c

        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "industry": item.industry if item.HasField('industry') else NoneDataType,
                "cur_price": item.curPrice if item.HasField('curPrice') else NoneDataType,
                "change_rate": item.changeRate if item.HasField('changeRate') else NoneDataType,
                "change_amount": item.changeAmount if item.HasField('changeAmount') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "dividend_yield_ttm": item.dividendYieldTTM if item.HasField('dividendYieldTTM') else NoneDataType,
                "avg_dividend_yield_5y": item.avgDividendYield5Y if item.HasField('avgDividendYield5Y') else NoneDataType,
                "distribution_frequency": DistributionFrequency.to_string2(item.distributionFrequency) if item.HasField('distributionFrequency') else NoneDataType,
                "dividend_grow_year": item.dividendGrowYear if item.HasField('dividendGrowYear') else NoneDataType,
                "dividends_ttm": item.dividendsTTM if item.HasField('dividendsTTM') else NoneDataType,
                "payout_ratio_lfy": item.payoutRatioLFY if item.HasField('payoutRatioLFY') else NoneDataType,
                "next_payable_date": item.nextPayableDate if item.HasField('nextPayableDate') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", ret_list


class GetDividendCalendarQuery:
    """Query for getting dividend calendar (派息日历)."""

    @classmethod
    def pack_req(cls, market, date, data_from, count, conn_id):
        from ..common.pb.Qot_GetDividendCalendar_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)
        req.c2s.date = date

        if data_from is not None:
            req.c2s.dataFrom = int(data_from)

        if count is not None:
            req.c2s.count = int(count)

        return pack_pb_req(req, ProtoId.Qot_GetDividendCalendar, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c

        ret_list = []
        for item in s2c.itemList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "statement": item.statement if item.HasField('statement') else NoneDataType,
                "record_date": item.recordDate if item.HasField('recordDate') else NoneDataType,
                "ex_date": item.exDate if item.HasField('exDate') else NoneDataType,
                "dividend_payable_date": item.dividendPayableDate if item.HasField('dividendPayableDate') else NoneDataType,
            }
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetUSPreMarketRankQuery:
    """Query for getting US pre-market rank (美股盘前榜)."""

    @classmethod
    def pack_req(cls, sort_dir, offset, count, filter_list, conn_id):
        from ..common.pb.Qot_GetUSPreMarketRank_pb2 import Request
        req = Request()
        req.c2s.SetInParent()

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if offset is not None:
            req.c2s.offset = int(offset)

        if count is not None:
            req.c2s.count = int(count)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetUSPreMarketRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "pre_market_price": item.preMarketPrice if item.HasField('preMarketPrice') else NoneDataType,
                "pre_market_change_ratio": item.preMarketChangeRatio if item.HasField('preMarketChangeRatio') else NoneDataType,
                "pre_market_change_amount": item.preMarketChangeAmount if item.HasField('preMarketChangeAmount') else NoneDataType,
                "pre_market_turnover": item.preMarketTurnover if item.HasField('preMarketTurnover') else NoneDataType,
                "pre_market_volume": item.preMarketVolume if item.HasField('preMarketVolume') else NoneDataType,
                "close_price": item.closePrice if item.HasField('closePrice') else NoneDataType,
                "change_ratio": item.changeRatio if item.HasField('changeRatio') else NoneDataType,
                "change_amount": item.changeAmount if item.HasField('changeAmount') else NoneDataType,
            }
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetUSAfterHoursRankQuery:
    """Query for getting US after-hours rank (美股盘后榜)."""

    @classmethod
    def pack_req(cls, sort_dir, offset, count, filter_list, conn_id):
        from ..common.pb.Qot_GetUSAfterHoursRank_pb2 import Request
        req = Request()
        req.c2s.SetInParent()

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if offset is not None:
            req.c2s.offset = int(offset)

        if count is not None:
            req.c2s.count = int(count)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetUSAfterHoursRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "after_hours_price": item.afterHoursPrice if item.HasField('afterHoursPrice') else NoneDataType,
                "after_hours_change_ratio": item.afterHoursChangeRatio if item.HasField('afterHoursChangeRatio') else NoneDataType,
                "after_hours_change_amount": item.afterHoursChangeAmount if item.HasField('afterHoursChangeAmount') else NoneDataType,
                "after_hours_turnover": item.afterHoursTurnover if item.HasField('afterHoursTurnover') else NoneDataType,
                "after_hours_volume": item.afterHoursVolume if item.HasField('afterHoursVolume') else NoneDataType,
                "close_price": item.closePrice if item.HasField('closePrice') else NoneDataType,
                "change_ratio": item.changeRatio if item.HasField('changeRatio') else NoneDataType,
                "change_amount": item.changeAmount if item.HasField('changeAmount') else NoneDataType,
            }
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetUSOvernightRankQuery:
    """Query for getting US overnight rank (美股夜盘榜)."""

    @classmethod
    def pack_req(cls, sort_dir, offset, count, filter_list, conn_id):
        from ..common.pb.Qot_GetUSOvernightRank_pb2 import Request
        req = Request()
        req.c2s.SetInParent()

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if offset is not None:
            req.c2s.offset = int(offset)

        if count is not None:
            req.c2s.count = int(count)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetUSOvernightRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "overnight_price": item.overnightPrice if item.HasField('overnightPrice') else NoneDataType,
                "overnight_change_ratio": item.overnightChangeRatio if item.HasField('overnightChangeRatio') else NoneDataType,
                "overnight_change_amount": item.overnightChangeAmount if item.HasField('overnightChangeAmount') else NoneDataType,
                "overnight_turnover": item.overnightTurnover if item.HasField('overnightTurnover') else NoneDataType,
                "overnight_volume": item.overnightVolume if item.HasField('overnightVolume') else NoneDataType,
                "close_price": item.closePrice if item.HasField('closePrice') else NoneDataType,
                "change_ratio": item.changeRatio if item.HasField('changeRatio') else NoneDataType,
                "change_amount": item.changeAmount if item.HasField('changeAmount') else NoneDataType,
            }
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetTopMoversRankQuery:
    """Query for getting top movers rank (领涨/领跌榜-盘中)."""

    @classmethod
    def pack_req(cls, market, sort_dir, offset, count, filter_list, conn_id):
        from ..common.pb.Qot_GetTopMoversRank_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if offset is not None:
            req.c2s.offset = int(offset)

        if count is not None:
            req.c2s.count = int(count)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetTopMoversRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "cur_price": item.curPrice if item.HasField('curPrice') else NoneDataType,
                "change_ratio": item.changeRatio if item.HasField('changeRatio') else NoneDataType,
                "change_amount": item.changeAmount if item.HasField('changeAmount') else NoneDataType,
                "turnover": item.turnover if item.HasField('turnover') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "turnover_ratio": item.turnoverRatio if item.HasField('turnoverRatio') else NoneDataType,
                "pe_ttm": item.peTTM if item.HasField('peTTM') else NoneDataType,
                "amplitude": item.amplitude if item.HasField('amplitude') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "volume_ratio": item.volumeRatio if item.HasField('volumeRatio') else NoneDataType,
            }
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetHotListQuery:
    """Query for getting hot list (热议榜)."""

    @classmethod
    def pack_req(cls, market, sort_field, sort_dir, offset, count, filter_list, conn_id):
        from ..common.pb.Qot_GetHotList_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)

        if sort_field is not None:
            r, v = HotListSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if offset is not None:
            req.c2s.offset = int(offset)

        if count is not None:
            req.c2s.count = int(count)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetHotList, conn_id)

    _NEWS_TYPE_MAP = {1: "Community", 2: "News"}

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "trade_heat": item.tradeHeat if item.HasField('tradeHeat') else NoneDataType,
                "trade_heat_change": item.tradeHeatChange if item.HasField('tradeHeatChange') else NoneDataType,
                "search_heat": item.searchHeat if item.HasField('searchHeat') else NoneDataType,
                "search_heat_change": item.searchHeatChange if item.HasField('searchHeatChange') else NoneDataType,
                "news_heat": item.newsHeat if item.HasField('newsHeat') else NoneDataType,
                "news_heat_change": item.newsHeatChange if item.HasField('newsHeatChange') else NoneDataType,
                "average_heat": item.averageHeat if item.HasField('averageHeat') else NoneDataType,
                "average_heat_change": item.averageHeatChange if item.HasField('averageHeatChange') else NoneDataType,
            }
            # 解析关联新闻
            if item.HasField('newsInfo'):
                news = item.newsInfo
                news_type_val = news.newsType if news.HasField('newsType') else None
                data["news_type"] = cls._NEWS_TYPE_MAP.get(news_type_val, NoneDataType)
                data["news_title"] = news.title if news.HasField('title') else NoneDataType
                data["news_url"] = news.newsUrl if news.HasField('newsUrl') else NoneDataType
            else:
                data["news_type"] = NoneDataType
                data["news_title"] = NoneDataType
                data["news_url"] = NoneDataType
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetShortSellingRankQuery:
    """Query for getting short selling rank (卖空异动榜)."""

    @classmethod
    def pack_req(cls, market, sort_field, sort_dir, offset, count, plate_list, conn_id):
        from ..common.pb.Qot_GetShortSellingRank_pb2 import Request
        req = Request()
        req.c2s.SetInParent()

        if market is not None:
            _, req.c2s.market = Market.to_number(market)

        if sort_field is not None:
            r, v = ShortSellingSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if offset is not None:
            req.c2s.offset = int(offset)

        if count is not None:
            req.c2s.count = int(count)

        if plate_list is not None:
            for plate_code in plate_list:
                ret, content = split_stock_str(plate_code)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + content, None, 0, 0
                market_code, stock_code = content
                plate_pb = req.c2s.plateList.add()
                plate_pb.market = market_code
                plate_pb.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetShortSellingRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "close_price": item.closePrice if item.HasField('closePrice') else NoneDataType,
                "change_ratio": item.changeRatio if item.HasField('changeRatio') else NoneDataType,
                "change_ratio_5d": item.changeRatio5D if item.HasField('changeRatio5D') else NoneDataType,
                "change_ratio_10d": item.changeRatio10D if item.HasField('changeRatio10D') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "short_number": item.shortNumber if item.HasField('shortNumber') else NoneDataType,
                "short_number_change": item.shortNumberChange if item.HasField('shortNumberChange') else NoneDataType,
                "short_ratio": item.shortRatio if item.HasField('shortRatio') else NoneDataType,
                "short_ratio_change": item.shortRatioChange if item.HasField('shortRatioChange') else NoneDataType,
                "short_position_volume": item.shortPositionVolume if item.HasField('shortPositionVolume') else NoneDataType,
                "short_position_ratio": item.shortPositionRatio if item.HasField('shortPositionRatio') else NoneDataType,
                "days_to_cover": item.daysToCover if item.HasField('daysToCover') else NoneDataType,
                "week_avg_short_number": item.weekAvgShortNumber if item.HasField('weekAvgShortNumber') else NoneDataType,
                "week_avg_short_ratio": item.weekAvgShortRatio if item.HasField('weekAvgShortRatio') else NoneDataType,
                "month_avg_short_number": item.monthAvgShortNumber if item.HasField('monthAvgShortNumber') else NoneDataType,
                "month_avg_short_ratio": item.monthAvgShortRatio if item.HasField('monthAvgShortRatio') else NoneDataType,
            }
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetPeriodChangeRankQuery:
    """Query for getting period change rank (区间涨跌幅)."""

    @classmethod
    def pack_req(cls, market, period_type, sort_dir, offset, count, filter_list, conn_id):
        from ..common.pb.Qot_GetPeriodChangeRank_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)

        if period_type is not None:
            r, v = RankPeriodType.to_number(period_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of period_type param is wrong", None, 0, 0
            req.c2s.periodType = v

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if offset is not None:
            req.c2s.offset = int(offset)

        if count is not None:
            req.c2s.count = int(count)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetPeriodChangeRank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "cur_price": item.curPrice if item.HasField('curPrice') else NoneDataType,
                "change_ratio": item.changeRatio if item.HasField('changeRatio') else NoneDataType,
                "turnover": item.turnover if item.HasField('turnover') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "change_rate_5min": item.changeRate5Min if item.HasField('changeRate5Min') else NoneDataType,
                "change_rate_5d": item.changeRate5D if item.HasField('changeRate5D') else NoneDataType,
                "change_rate_10d": item.changeRate10D if item.HasField('changeRate10D') else NoneDataType,
                "change_rate_20d": item.changeRate20D if item.HasField('changeRate20D') else NoneDataType,
                "change_rate_60d": item.changeRate60D if item.HasField('changeRate60D') else NoneDataType,
                "change_rate_120d": item.changeRate120D if item.HasField('changeRate120D') else NoneDataType,
                "change_rate_250d": item.changeRate250D if item.HasField('changeRate250D') else NoneDataType,
                "change_rate_ytd": item.changeRateYTD if item.HasField('changeRateYTD') else NoneDataType,
                "pe_ttm": item.peTTM if item.HasField('peTTM') else NoneDataType,
                "pb": item.pb if item.HasField('pb') else NoneDataType,
                "turnover_ratio": item.turnoverRatio if item.HasField('turnoverRatio') else NoneDataType,
                "volume_ratio": item.volumeRatio if item.HasField('volumeRatio') else NoneDataType,
                "amplitude": item.amplitude if item.HasField('amplitude') else NoneDataType,
            }
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetHighDividendSOERankQuery:
    """Query for getting high dividend SOE rank (破净高股息国央企)."""

    @classmethod
    def pack_req(cls, sort_field, sort_dir, offset, count, filter_list, conn_id):
        from ..common.pb.Qot_GetHighDividendSOERank_pb2 import Request
        req = Request()
        req.c2s.SetInParent()

        if sort_field is not None:
            r, v = HighDividendSOESortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if offset is not None:
            req.c2s.offset = int(offset)

        if count is not None:
            req.c2s.count = int(count)

        if filter_list is not None:
            for f in filter_list:
                filter_pb = req.c2s.filterList.add()
                ret, msg = f.fill_request_pb(filter_pb)
                if ret != RET_OK:
                    return RET_ERROR, ERROR_STR_PREFIX + msg, None, 0, 0

        return pack_pb_req(req, ProtoId.Qot_GetHighDividendSOERank, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "industry": item.industry if item.HasField('industry') else NoneDataType,
                "cur_price": item.curPrice if item.HasField('curPrice') else NoneDataType,
                "change_ratio": item.changeRatio if item.HasField('changeRatio') else NoneDataType,
                "turnover": item.turnover if item.HasField('turnover') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "pe_ttm": item.peTTM if item.HasField('peTTM') else NoneDataType,
                "pb": item.pb if item.HasField('pb') else NoneDataType,
                "dividend_yield_ttm": item.dividendYieldTTM if item.HasField('dividendYieldTTM') else NoneDataType,
                "turnover_ratio": item.turnoverRatio if item.HasField('turnoverRatio') else NoneDataType,
                "change_rate_5d": item.changeRate5D if item.HasField('changeRate5D') else NoneDataType,
                "change_rate_10d": item.changeRate10D if item.HasField('changeRate10D') else NoneDataType,
                "change_rate_20d": item.changeRate20D if item.HasField('changeRate20D') else NoneDataType,
                "change_rate_60d": item.changeRate60D if item.HasField('changeRate60D') else NoneDataType,
                "change_rate_120d": item.changeRate120D if item.HasField('changeRate120D') else NoneDataType,
                "change_rate_250d": item.changeRate250D if item.HasField('changeRate250D') else NoneDataType,
            }
            ret_list.append(data)

        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        return RET_OK, "", (all_count, ret_list)


class GetInstitutionListQuery:
    """Query for getting institution list (机构列表)."""

    @classmethod
    def pack_req(cls, market, sort_field, sort_dir, count, page, name_part, conn_id):
        from ..common.pb.Qot_GetInstitutionList_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)

        if sort_field is not None:
            r, v = InstitutionListSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = str(page)

        if name_part is not None:
            req.c2s.namePart = str(name_part)

        return pack_pb_req(req, ProtoId.Qot_GetInstitutionList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        currency = s2c.currency if s2c.HasField('currency') else NoneDataType

        ret_list = []
        for item in s2c.dataList:
            data = {
                "institution_id": item.institutionId,
                "institution_name": item.institutionName if item.HasField('institutionName') else NoneDataType,
                "position_value": item.positionValue if item.HasField('positionValue') else NoneDataType,
                "position_value_change": item.positionValueChange if item.HasField('positionValueChange') else NoneDataType,
                "position_count": item.positionCount if item.HasField('positionCount') else NoneDataType,
                "position_count_change": item.positionCountChange if item.HasField('positionCountChange') else NoneDataType,
                "disclosure_date": item.disclosureDate if item.HasField('disclosureDate') else NoneDataType,
                "currency": currency,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetInstitutionProfileQuery:
    """Query for getting institution profile (机构概况)."""

    @classmethod
    def pack_req(cls, market, institution_id, conn_id):
        from ..common.pb.Qot_GetInstitutionProfile_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)
        req.c2s.institutionId = int(institution_id)

        return pack_pb_req(req, ProtoId.Qot_GetInstitutionProfile, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        data = {
            "institution_name": s2c.institutionName if s2c.HasField('institutionName') else NoneDataType,
            "description": s2c.description if s2c.HasField('description') else NoneDataType,
            "position_value": s2c.positionValue if s2c.HasField('positionValue') else NoneDataType,
            "last_position_value": s2c.lastPositionValue if s2c.HasField('lastPositionValue') else NoneDataType,
            "position_value_change_pct": s2c.positionValueChangePct if s2c.HasField('positionValueChangePct') else NoneDataType,
            "total_holding_count": s2c.totalHoldingCount if s2c.HasField('totalHoldingCount') else NoneDataType,
            "holding_change_count": s2c.holdingChangeCount if s2c.HasField('holdingChangeCount') else NoneDataType,
            "new_count": s2c.newCount if s2c.HasField('newCount') else NoneDataType,
            "sold_out_count": s2c.soldOutCount if s2c.HasField('soldOutCount') else NoneDataType,
            "increase_count": s2c.increaseCount if s2c.HasField('increaseCount') else NoneDataType,
            "decrease_count": s2c.decreaseCount if s2c.HasField('decreaseCount') else NoneDataType,
            "top10_pct": s2c.top10Pct if s2c.HasField('top10Pct') else NoneDataType,
            "top10_pct_change": s2c.top10PctChange if s2c.HasField('top10PctChange') else NoneDataType,
            "disclosure_date": s2c.disclosureDate if s2c.HasField('disclosureDate') else NoneDataType,
            "currency": s2c.currency if s2c.HasField('currency') else NoneDataType,
        }

        return RET_OK, "", data


class GetInstitutionDistributionQuery:
    """Query for getting institution holding distribution (机构持仓行业分布)."""

    @classmethod
    def pack_req(cls, market, institution_id, conn_id):
        from ..common.pb.Qot_GetInstitutionDistribution_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)
        req.c2s.institutionId = int(institution_id)

        return pack_pb_req(req, ProtoId.Qot_GetInstitutionDistribution, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dataList:
            data = {
                "industry_id": item.industryId if item.HasField('industryId') else NoneDataType,
                "industry_name": item.industryName if item.HasField('industryName') else NoneDataType,
                "position_value": item.positionValue if item.HasField('positionValue') else NoneDataType,
                "portfolio_pct": item.portfolioPct if item.HasField('portfolioPct') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", ret_list


class GetInstitutionHoldingChangeQuery:
    """Query for getting institution holding change (机构持仓变动)."""

    @classmethod
    def pack_req(cls, market, institution_id, change_type, sort_field, sort_dir, count, page, conn_id):
        from ..common.pb.Qot_GetInstitutionHoldingChange_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)
        req.c2s.institutionId = int(institution_id)

        if change_type is not None:
            r, v = InstitutionHoldingChangeType.to_number(change_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of change_type param is wrong", None, 0, 0
            req.c2s.changeType = v

        if sort_field is not None:
            r, v = InstitutionHoldingChangeSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = str(page)

        return pack_pb_req(req, ProtoId.Qot_GetInstitutionHoldingChange, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "portfolio_pct": item.portfolioPct if item.HasField('portfolioPct') else NoneDataType,
                "change_shares": item.changeShares if item.HasField('changeShares') else NoneDataType,
                "change_pct": item.changePct if item.HasField('changePct') else NoneDataType,
                "holding_date": item.holdingDate if item.HasField('holdingDate') else NoneDataType,
                "source": item.source if item.HasField('source') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetInstitutionHoldingListQuery:
    """Query for getting institution holding list (机构持股列表)."""

    @classmethod
    def pack_req(cls, market, institution_id, change_type, sort_field, sort_dir, count, page, keyword, conn_id):
        from ..common.pb.Qot_GetInstitutionHoldingList_pb2 import Request
        req = Request()

        _, req.c2s.market = Market.to_number(market)
        req.c2s.institutionId = int(institution_id)

        if change_type is not None:
            r, v = InstitutionHoldingChangeType.to_number(change_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of change_type param is wrong", None, 0, 0
            req.c2s.changeType = v

        if sort_field is not None:
            r, v = InstitutionHoldingListSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = str(page)

        if keyword is not None:
            req.c2s.keyword = str(keyword)

        return pack_pb_req(req, ProtoId.Qot_GetInstitutionHoldingList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else 0
        currency = s2c.currency if s2c.HasField('currency') else NoneDataType

        ret_list = []
        for item in s2c.dataList:
            data = {
                "security": merge_qot_mkt_stock_str(int(item.security.market), item.security.code),
                "name": item.name if item.HasField('name') else NoneDataType,
                "industry_name": item.industryName if item.HasField('industryName') else NoneDataType,
                "holding_value": item.holdingValue if item.HasField('holdingValue') else NoneDataType,
                "holding_pct": item.holdingPct if item.HasField('holdingPct') else NoneDataType,
                "last_holding_pct": item.lastHoldingPct if item.HasField('lastHoldingPct') else NoneDataType,
                "change_shares": item.changeShares if item.HasField('changeShares') else NoneDataType,
                "portfolio_pct": item.portfolioPct if item.HasField('portfolioPct') else NoneDataType,
                "change_pct": item.changePct if item.HasField('changePct') else NoneDataType,
                "holding_date": item.holdingDate if item.HasField('holdingDate') else NoneDataType,
                "source": item.source if item.HasField('source') else NoneDataType,
                "currency": currency,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetArkFundHoldingQuery:
    """Query for getting ARK fund holding (ARK基金持仓)."""

    @classmethod
    def pack_req(cls, holding_type, cycle_type, sort_field, sort_dir, count, page, conn_id):
        from ..common.pb.Qot_GetArkFundHolding_pb2 import Request
        req = Request()
        req.c2s.SetInParent()

        if holding_type is not None:
            r, v = ArkHoldingType.to_number(holding_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of holding_type param is wrong", None, 0, 0
            req.c2s.holdingType = v

        if cycle_type is not None:
            r, v = ArkCycleType.to_number(cycle_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of cycle_type param is wrong", None, 0, 0
            req.c2s.cycleType = v

        if sort_field is not None:
            r, v = ArkFundHoldingSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = str(page)

        return pack_pb_req(req, ProtoId.Qot_GetArkFundHolding, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.dataList:
            security = NoneDataType
            if item.HasField('security'):
                security = merge_qot_mkt_stock_str(int(item.security.market), item.security.code)
            data = {
                "security": security,
                "name": item.name if item.HasField('name') else NoneDataType,
                "shares": item.shares if item.HasField('shares') else NoneDataType,
                "shares_change": item.sharesChange if item.HasField('sharesChange') else NoneDataType,
                "market_value": item.marketValue if item.HasField('marketValue') else NoneDataType,
                "weight": item.weight if item.HasField('weight') else NoneDataType,
                "weight_change": item.weightChange if item.HasField('weightChange') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetArkStockDynamicQuery:
    """Query for getting ARK stock dynamic (ARK个股交易动态)."""

    @classmethod
    def pack_req(cls, security, conn_id):
        from ..common.pb.Qot_GetArkStockDynamic_pb2 import Request
        req = Request()

        ret, content = split_stock_str(security)
        if ret != RET_OK:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetArkStockDynamic, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        data = {
            "dynamic_type": ArkDynamicType.to_string2(s2c.dynamicType) if s2c.HasField('dynamicType') else NoneDataType,
            "transaction_count": s2c.transactionCount if s2c.HasField('transactionCount') else NoneDataType,
            "net_shares": s2c.netShares if s2c.HasField('netShares') else NoneDataType,
            "last_transaction_time": s2c.lastTransactionTime if s2c.HasField('lastTransactionTime') else NoneDataType,
        }

        return RET_OK, "", data


class GetArkActiveTransactionQuery:
    """Query for getting ARK active transaction (ARK主动交易聚合)."""

    @classmethod
    def pack_req(cls, holding_type, cycle_type, sort_field, sort_dir, count, page, conn_id):
        from ..common.pb.Qot_GetArkActiveTransaction_pb2 import Request
        req = Request()
        req.c2s.SetInParent()

        if holding_type is not None:
            r, v = ArkActiveTransactionHoldingType.to_number(holding_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of holding_type param is wrong", None, 0, 0
            req.c2s.holdingType = v

        if cycle_type is not None:
            r, v = ArkCycleType.to_number(cycle_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of cycle_type param is wrong", None, 0, 0
            req.c2s.cycleType = v

        if sort_field is not None:
            r, v = ArkActiveTransactionSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if sort_dir is not None:
            r, v = RankSortDir.to_number(sort_dir)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_dir param is wrong", None, 0, 0
            req.c2s.sortDir = v

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = str(page)

        return pack_pb_req(req, ProtoId.Qot_GetArkActiveTransaction, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.dataList:
            security = NoneDataType
            if item.HasField('security'):
                security = merge_qot_mkt_stock_str(int(item.security.market), item.security.code)
            data = {
                "security": security,
                "name": item.name if item.HasField('name') else NoneDataType,
                "change_amount": item.changeAmount if item.HasField('changeAmount') else NoneDataType,
                "change_shares": item.changeShares if item.HasField('changeShares') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetRatingChangeQuery:
    """Query for getting rating change (获取评级变动)."""

    @classmethod
    def pack_req(cls, market, change_type, count, page, conn_id):
        from ..common.pb.Qot_GetRatingChange_pb2 import Request
        req = Request()

        r, v = Market.to_number(market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of market param is wrong", None, 0, 0
        req.c2s.market = v

        if change_type is not None:
            r, v = RatingChangeType.to_number(change_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of change_type param is wrong", None, 0, 0
            req.c2s.changeType = v

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = str(page)

        return pack_pb_req(req, ProtoId.Qot_GetRatingChange, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.dataList:
            security = NoneDataType
            if item.HasField('security'):
                security = merge_qot_mkt_stock_str(int(item.security.market), item.security.code)
            data = {
                "security": security,
                "name": item.name if item.HasField('name') else NoneDataType,
                "rating": RatingLevel.to_string2(item.rating) if item.HasField('rating') else NoneDataType,
                "last_rating": RatingLevel.to_string2(item.lastRating) if item.HasField('lastRating') else NoneDataType,
                "target_price": item.targetPrice if item.HasField('targetPrice') else NoneDataType,
                "last_target_price": item.lastTargetPrice if item.HasField('lastTargetPrice') else NoneDataType,
                "change_type": RatingChangeType.to_string2(item.changeType) if item.HasField('changeType') else NoneDataType,
                "institution_name": item.institutionName if item.HasField('institutionName') else NoneDataType,
                "recommendation_date": item.recommendationDate if item.HasField('recommendationDate') else NoneDataType,
                "last_recommendation_date": item.lastRecommendationDate if item.HasField('lastRecommendationDate') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetIndustrialChainListQuery:
    """Query for getting industrial chain list (获取产业链列表)."""

    @classmethod
    def pack_req(cls, market, keyword, count, page, conn_id):
        from ..common.pb.Qot_GetIndustrialChainList_pb2 import Request
        req = Request()

        r, v = Market.to_number(market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of market param is wrong", None, 0, 0
        req.c2s.market = v

        if keyword is not None:
            req.c2s.keyword = str(keyword)

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = str(page)

        return pack_pb_req(req, ProtoId.Qot_GetIndustrialChainList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.dataList:
            relation_securities = []
            for sec in item.relationSecurityList:
                relation_securities.append(merge_qot_mkt_stock_str(int(sec.market), sec.code))
            data = {
                "chain_id": item.chainId if item.HasField('chainId') else NoneDataType,
                "chain_type": IndustrialChainType.to_string2(item.chainType) if item.HasField('chainType') else NoneDataType,
                "name": item.name if item.HasField('name') else NoneDataType,
                "detail": item.detail if item.HasField('detail') else NoneDataType,
                "market_cap": item.marketCap if item.HasField('marketCap') else NoneDataType,
                "stocks_num": item.stocksNum if item.HasField('stocksNum') else NoneDataType,
                "relation_security_list": relation_securities,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetIndustrialChainDetailQuery:
    """Query for getting industrial chain detail (获取产业链详情)."""

    @classmethod
    def pack_req(cls, chain_id, conn_id):
        from ..common.pb.Qot_GetIndustrialChainDetail_pb2 import Request
        req = Request()
        req.c2s.chainId = int(chain_id)
        return pack_pb_req(req, ProtoId.Qot_GetIndustrialChainDetail, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        node_list = []
        for node in s2c.nodeList:
            node_data = {
                "node_id": node.nodeId if node.HasField('nodeId') else NoneDataType,
                "parent_node_id": node.parentNodeId if node.HasField('parentNodeId') else NoneDataType,
                "layer": node.layerSth if node.HasField('layerSth') else NoneDataType,
                "name": node.name if node.HasField('name') else NoneDataType,
                "plate_id": node.plateId if node.HasField('plateId') else NoneDataType,
            }
            node_list.append(node_data)

        information_list = []
        for info in s2c.informationList:
            information_list.append({
                "title": info.title if info.HasField('title') else NoneDataType,
                "url": info.url if info.HasField('url') else NoneDataType,
            })

        data = {
            "chain_id": s2c.chainId if s2c.HasField('chainId') else NoneDataType,
            "chain_type": IndustrialChainType.to_string2(s2c.chainType) if s2c.HasField('chainType') else NoneDataType,
            "name": s2c.name if s2c.HasField('name') else NoneDataType,
            "node_list": node_list,
            "information_list": information_list,
        }

        return RET_OK, "", data


class GetIndustrialChainByPlateQuery:
    """Query for getting industrial chain by plate (获取板块关联产业链)."""

    @classmethod
    def pack_req(cls, plate_id, conn_id):
        from ..common.pb.Qot_GetIndustrialChainByPlate_pb2 import Request
        req = Request()
        req.c2s.plateId = int(plate_id)
        return pack_pb_req(req, ProtoId.Qot_GetIndustrialChainByPlate, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for chain in s2c.relatedChainList:
            ret_list.append({
                "chain_id": chain.chainId if chain.HasField('chainId') else NoneDataType,
                "chain_type": IndustrialChainType.to_string2(chain.chainType) if chain.HasField('chainType') else NoneDataType,
                "name": chain.name if chain.HasField('name') else NoneDataType,
                "market_cap": chain.marketCap if chain.HasField('marketCap') else NoneDataType,
                "stocks_num": chain.stocksNum if chain.HasField('stocksNum') else NoneDataType,
            })

        return RET_OK, "", ret_list


class GetIndustrialPlateInfoQuery:
    """Query for getting industrial plate info (获取产业板块信息)."""

    @classmethod
    def pack_req(cls, plate_id, conn_id):
        from ..common.pb.Qot_GetIndustrialPlateInfo_pb2 import Request
        req = Request()
        req.c2s.plateId = int(plate_id)
        return pack_pb_req(req, ProtoId.Qot_GetIndustrialPlateInfo, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        data = {
            "plate_id": s2c.plateId if s2c.HasField('plateId') else NoneDataType,
            "summary": s2c.summary if s2c.HasField('summary') else NoneDataType,
        }

        return RET_OK, "", data


class GetIndustrialPlateStockQuery:
    """Query for getting industrial plate stock (获取产业板块成分股)."""

    @classmethod
    def pack_req(cls, chain_id, plate_id, market_list, sort_field, ascend, count, page, conn_id):
        from ..common.pb.Qot_GetIndustrialPlateStock_pb2 import Request
        req = Request()

        if chain_id is not None:
            req.c2s.chainId = int(chain_id)
        if plate_id is not None:
            req.c2s.plateId = int(plate_id)

        if market_list is not None:
            for market in market_list:
                r, v = Market.to_number(market)
                if r is False:
                    return RET_ERROR, ERROR_STR_PREFIX + "the type of market param is wrong", None, 0, 0
                req.c2s.marketList.append(v)

        if sort_field is not None:
            r, v = PlateStockSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if ascend is not None:
            req.c2s.ascend = ascend

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = page

        return pack_pb_req(req, ProtoId.Qot_GetIndustrialPlateStock, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.page if s2c.HasField('page') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.stockList:
            security = NoneDataType
            if item.HasField('security'):
                security = merge_qot_mkt_stock_str(int(item.security.market), item.security.code)
            ret_list.append({
                "security": security,
                "name": item.name if item.HasField('name') else NoneDataType,
            })

        return RET_OK, "", (ret_list, next_page, all_count)


class GetHeatMapDataQuery:
    """Query for getting heat map data (获取热力图数据)."""

    @classmethod
    def pack_req(cls, market, sort_field, ascend, count, page, plate_type, conn_id):
        from ..common.pb.Qot_GetHeatMapData_pb2 import Request
        req = Request()

        r, v = Market.to_number(market)
        if r is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of market param is wrong", None, 0, 0
        req.c2s.market = v

        if sort_field is not None:
            r, v = HeatMapSortField.to_number(sort_field)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of sort_field param is wrong", None, 0, 0
            req.c2s.sortField = v

        if ascend is not None:
            req.c2s.ascend = bool(ascend)

        if count is not None:
            req.c2s.count = int(count)

        if page is not None:
            req.c2s.page = str(page)

        if plate_type is not None:
            r, v = HeatMapPlateType.to_number(plate_type)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of plate_type param is wrong", None, 0, 0
            req.c2s.plateType = v

        return pack_pb_req(req, ProtoId.Qot_GetHeatMapData, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        next_page = s2c.nextPage if s2c.HasField('nextPage') else None
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.plateDataList:
            plate = NoneDataType
            if item.HasField('plate'):
                plate = merge_qot_mkt_stock_str(int(item.plate.market), item.plate.code)
            leader_stock = NoneDataType
            if item.HasField('leaderStock'):
                leader_stock = merge_qot_mkt_stock_str(int(item.leaderStock.market), item.leaderStock.code)
            data = {
                "plate": plate,
                "plate_name": item.plateName if item.HasField('plateName') else NoneDataType,
                "cur_price": item.curPrice if item.HasField('curPrice') else NoneDataType,
                "change_rate": item.changeRate if item.HasField('changeRate') else NoneDataType,
                "turnover": item.turnover if item.HasField('turnover') else NoneDataType,
                "volume": item.volume if item.HasField('volume') else NoneDataType,
                "market_val": item.marketVal if item.HasField('marketVal') else NoneDataType,
                "pe_avg": item.peAvg if item.HasField('peAvg') else NoneDataType,
                "rise_count": item.riseCount if item.HasField('riseCount') else NoneDataType,
                "fall_count": item.fallCount if item.HasField('fallCount') else NoneDataType,
                "equal_count": item.equalCount if item.HasField('equalCount') else NoneDataType,
                "leader_stock": leader_stock,
                "description": item.description if item.HasField('description') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", (ret_list, next_page, all_count)


class GetRiseFallDistributionQuery:
    """Query for getting rise/fall distribution (获取涨跌分布)."""

    @classmethod
    def pack_req(cls, security, market, conn_id):
        from ..common.pb.Qot_GetRiseFallDistribution_pb2 import Request
        req = Request()
        req.c2s.SetInParent()

        if security is not None:
            ret, content = split_stock_str(security)
            if ret != RET_OK:
                return RET_ERROR, content, None, 0, 0
            market_code, stock_code = content
            req.c2s.security.market = market_code
            req.c2s.security.code = stock_code
        elif market is not None:
            r, v = Market.to_number(market)
            if r is False:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of market param is wrong", None, 0, 0
            req.c2s.market = v

        return pack_pb_req(req, ProtoId.Qot_GetRiseFallDistribution, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        plate = NoneDataType
        if s2c.HasField('plate'):
            plate = merge_qot_mkt_stock_str(int(s2c.plate.market), s2c.plate.code)

        ret_list = []
        for item in s2c.rangeList:
            data = {
                "type": RiseFallDistributionType.to_string2(item.type) if item.HasField('type') else NoneDataType,
                "left_border": item.leftBorder if item.HasField('leftBorder') else NoneDataType,
                "right_border": item.rightBorder if item.HasField('rightBorder') else NoneDataType,
                "stock_count": item.stockCount if item.HasField('stockCount') else NoneDataType,
            }
            ret_list.append(data)

        return RET_OK, "", {"plate": plate, "range_list": ret_list}


class GetFinancialsStatementsQuery:
    """
    Query ``Qot_GetFinancialsStatements`` (ProtoID 3227).
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id,
                 statement_type=None,
                 financial_type=None,
                 currency_code=None,
                 next_key=None,
                 num=None):
        """
        :param code:            股票代码，如 "US.AAPL"
        :param conn_id:         连接 ID
        :param statement_type:  报表类型（1=利润表 2=资产负债表 3=现金流量表 4=关键指标）
        :param financial_type:  财报类型，F10Type 枚举字符串（如 'Q1'、'ANNUAL'、'QUARTERLY_ANNUAL'）
        :param currency_code:   币种代码，参考ISO 4217，不填返回原始货币数据
        :param next_key:        分页key，首次不填或填0，续拉填上次回包的next_key
        :param num:             请求数量，默认10，范围1~50
        """
        # 兼容传入枚举字符串或数值
        from ..common.constant import F10Type
        financial_type_num = _enum_or_int(F10Type, financial_type, "financial_type")
        if isinstance(financial_type_num, tuple):
            return financial_type_num

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetFinancialsStatements_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if statement_type is not None:
            req.c2s.statementType = statement_type
        if financial_type_num is not None:
            req.c2s.financialType = financial_type_num
        if currency_code:
            req.c2s.currencyCode = currency_code
        if next_key is not None:
            req.c2s.nextKey = next_key
        if num is not None:
            req.c2s.num = num

        return pack_pb_req(req, ProtoId.Qot_GetFinancialsStatements, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        """
        返回 (ret_code, err_msg, result)。
        result 是一个 dict，包含：
          - structure_list:    list[dict]
          - report_list:       list[dict]
          - next_key:          int，-1 表示无更多数据
        """
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        result = {
            "next_key": s2c.nextKey if s2c.HasField("nextKey") else "-1",
            "structure_list": [],
            "report_list": [],
        }

        # 字段结构：仅保留返回数据中实际出现的字段，按 field_id 升序
        structure_list = []
        for fi in s2c.structureList:
            field_id = fi.fieldId if fi.HasField("fieldId") else 0
            if field_id <= 0:
                continue
            structure_list.append({
                "field_id": field_id,
                "display_name": fi.displayName if fi.HasField("displayName") else "",
            })
        result["structure_list"] = sorted(structure_list, key=lambda x: x["field_id"])

        # field_id -> display_name 映射，供 item_list 直接内嵌展示名
        id_to_name = {e["field_id"]: e["display_name"] for e in result["structure_list"]}

        # 财报数据
        from ..common.constant import F10Type
        for rpt in s2c.reportList:
            report = {
                "date_time":            rpt.dateTime if rpt.HasField("dateTime") else 0,
                "date_time_str":        rpt.dateTimeStr if rpt.HasField("dateTimeStr") else "",
                "fiscal_year":          rpt.fiscalYear if rpt.HasField("fiscalYear") else 0,
                "financial_type":       F10Type.to_string2(rpt.financialType) if rpt.HasField("financialType") else F10Type.NONE,
                "period_text":          rpt.periodText if rpt.HasField("periodText") else "",
                "currency_info":        rpt.currencyInfo if rpt.HasField("currencyInfo") else "",
                "currency_code":        rpt.currencyCode if rpt.HasField("currencyCode") else "",
                "accounting_standards": rpt.accountingStandards if rpt.HasField("accountingStandards") else "",
                "auditor_report":       rpt.auditorReport if rpt.HasField("auditorReport") else "",
                "item_list":            [],
            }
            for item in rpt.itemList:
                entry = {
                    "field_id":    item.fieldId,
                    "display_name": id_to_name.get(item.fieldId, ""),
                }
                if item.HasField("data"):
                    entry["data"] = item.data
                if item.HasField("yoy"):
                    entry["yoy"] = item.yoy
                if item.HasField("qoq"):
                    entry["qoq"] = item.qoq
                report["item_list"].append(entry)
            result["report_list"].append(report)

        return RET_OK, "", result


class GetFinancialsRevenueBreakdownQuery:
    """
    Query ``Qot_GetFinancialsRevenueBreakdown`` (ProtoID 3228).
    主营构成
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, date=None, financial_type=None, currency_code=None):
        """
        :param code:           股票代码，如 "US.AAPL"
        :param conn_id:        连接 ID
        :param date:           时间戳（0=最新）
        :param financial_type: 财报类型，支持 F10Type 枚举字符串（如 'Q1'）或数值（1-7/9-11）
        :param currency_code:  币种代码，参考ISO 4217，不填返回原始货币数据
        """
        # 兼容传入枚举字符串或数值
        from ..common.constant import F10Type
        financial_type_num = _enum_or_int(F10Type, financial_type, "financial_type")
        if isinstance(financial_type_num, tuple):
            return financial_type_num

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetFinancialsRevenueBreakdown_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if date is not None:
            req.c2s.date = date
        if financial_type_num is not None:
            req.c2s.financialType = financial_type_num
        if currency_code is not None:
            req.c2s.currencyCode = currency_code

        return pack_pb_req(req, ProtoId.Qot_GetFinancialsRevenueBreakdown, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        from ..common.constant import RevenueBreakdownType, F10Type

        s2c = rsp_pb.s2c

        breakdown_list = []
        for group in s2c.breakdownList:
            item_list = []
            for item in group.itemList:
                row = {}
                if item.HasField("name"):
                    row["name"] = item.name
                if item.HasField("mainOperIncome"):
                    row["main_oper_income"] = item.mainOperIncome
                if item.HasField("ratio"):
                    row["ratio"] = item.ratio
                item_list.append(row)
            breakdown_list.append({
                "type": RevenueBreakdownType.to_string2(group.type) if group.HasField("type") else RevenueBreakdownType.NONE,
                "item_list": item_list,
            })

        screen_date_list = []
        for sd in s2c.screenDateList:
            screen_date_list.append({
                "date": sd.date if sd.HasField("date") else 0,
                "period_text": sd.periodText if sd.HasField("periodText") else "",
                "financial_type": F10Type.to_string2(sd.financialType) if sd.HasField("financialType") else F10Type.NONE,
            })

        result = {
            "period": s2c.period if s2c.HasField("period") else "",
            "currency_code": s2c.currencyCode if s2c.HasField("currencyCode") else "",
            "breakdown_list": breakdown_list,
            "screen_date_list": screen_date_list,
        }
        return RET_OK, "", result


class GetResearchAnalystConsensusQuery:
    """
    Query `Qot_GetResearchAnalystConsensus`。
    对应分析师评级概述接口
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetResearchAnalystConsensus_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        return pack_pb_req(req, ProtoId.Qot_GetResearchAnalystConsensus, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        from ..common.constant import ResearchRatingType

        result = {}
        s2c = rsp_pb.s2c
        if s2c.HasField("highest"):
            result["highest"] = s2c.highest
        if s2c.HasField("average"):
            result["average"] = s2c.average
        if s2c.HasField("lowest"):
            result["lowest"] = s2c.lowest
        if s2c.HasField("rating"):
            result["rating"] = ResearchRatingType.to_string2(s2c.rating)
        if s2c.HasField("total"):
            result["total"] = s2c.total
        if s2c.HasField("updateTime"):
            result["update_time"] = s2c.updateTime
        if s2c.HasField("updateTimeStr"):
            result["update_time_str"] = s2c.updateTimeStr
        if s2c.HasField("buy"):
            result["buy"] = s2c.buy
        if s2c.HasField("hold"):
            result["hold"] = s2c.hold
        if s2c.HasField("sell"):
            result["sell"] = s2c.sell
        if s2c.HasField("strongBuy"):
            result["strong_buy"] = s2c.strongBuy
        if s2c.HasField("underperform"):
            result["underperform"] = s2c.underperform
        return RET_OK, "", result


def _analyst_rating_inst_pb_to_dict(inst):
    out = {}
    if inst is None:
        return out
    for proto_name, key in (
        ("institutionUid",        "institution_uid"),
        ("institutionPictureUrl", "institution_picture_url"),
        ("institutionName",       "institution_name"),
        ("updateTime",            "update_time"),
        ("updateTimeStr",         "update_time_str"),
        ("institutionSourceName", "institution_source_name"),
        ("institutionEnName",     "institution_en_name"),
    ):
        if inst.HasField(proto_name):
            out[key] = getattr(inst, proto_name)
    return out


def _analyst_rating_analyst_pb_to_dict(an):
    out = {}
    if an is None:
        return out
    for proto_name, key in (
        ("analystUid",       "analyst_uid"),
        ("analystName",      "analyst_name"),
        ("analystPictureUrl","analyst_picture_url"),
        ("numOfStars",       "num_of_stars"),
        ("successRate",      "success_rate"),
        ("excessReturn",     "excess_return"),
        ("stockSuccessRate", "stock_success_rate"),
        ("stockAvgReturn",   "stock_avg_return"),
        ("updateTime",       "update_time"),
        ("updateTimeStr",    "update_time_str"),
    ):
        if an.HasField(proto_name):
            out[key] = getattr(an, proto_name)
    if an.HasField("institutionInfo"):
        out["institution_info"] = _analyst_rating_inst_pb_to_dict(an.institutionInfo)
    return out


def _analyst_rating_item_pb_to_dict(it):
    out = {}
    if it is None:
        return out
    for proto_name, key in (
        ("analystUid",           "analyst_uid"),
        ("institutionUid",       "institution_uid"),
        ("recommendationDate",   "recommendation_date"),
        ("recommendationDateStr","recommendation_date_str"),
        ("ratingUrl",            "rating_url"),
        ("updateTime",           "update_time"),
        ("updateTimeStr",        "update_time_str"),
    ):
        if it.HasField(proto_name):
            out[key] = getattr(it, proto_name)
    if it.HasField("rating"):
        from ..common.constant import ResearchRatingType
        out["rating"] = ResearchRatingType.to_string2(it.rating)
    if it.HasField("targetPrice"):
        out["target_price"] = it.targetPrice
    return out


class GetResearchRatingSummaryQuery:
    """
    Query `Qot_GetResearchRatingSummary` (ProtoID 3230).
    统一评级查询：机构/分析师维度的汇总列表或指定 uid 的评级详情。
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, rating_dimension_type=None, uid=None, num=None, next_key=None):
        """
        :param code:                  股票代码，如 "US.AAPL"
        :param conn_id:               连接 ID
        :param rating_dimension_type: 评级维度，支持 ResearchRatingDimensionType 枚举字符串（如 'INSTITUTION'、'ANALYST'）或数值（1=机构，2=分析师）
        :param uid:                   空=汇总列表；非空=指定机构/分析师的评级详情
        :param num:                   单页条数
        :param next_key:              分页游标，首页传空；服务端回 "-1" 表示已取完
        """
        # 兼容传入枚举字符串或数值
        from ..common.constant import ResearchRatingDimensionType
        rating_dimension_type_num = _enum_or_int(ResearchRatingDimensionType, rating_dimension_type, "rating_dimension_type")
        if isinstance(rating_dimension_type_num, tuple):
            return rating_dimension_type_num

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetResearchRatingSummary_pb2 import Request

        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if rating_dimension_type_num is not None:
            req.c2s.ratingDimensionType = rating_dimension_type_num
        if uid is not None:
            req.c2s.uid = uid
        if num is not None:
            req.c2s.num = num
        if next_key is not None:
            req.c2s.nextKey = next_key
        return pack_pb_req(req, ProtoId.Qot_GetResearchRatingSummary, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        result = {}
        s2c = rsp_pb.s2c
        result["next_key"] = s2c.nextKey if s2c.HasField("nextKey") else "-1"

        if s2c.instRatingSummaryList:
            rows = []
            for row in s2c.instRatingSummaryList:
                rd = {}
                if row.HasField("institutionInfo"):
                    rd["institution_info"] = _analyst_rating_inst_pb_to_dict(row.institutionInfo)
                if row.ratingItemList:
                    rd["rating_item_list"] = [_analyst_rating_item_pb_to_dict(x) for x in row.ratingItemList]
                rows.append(rd)
            result["inst_rating_summary_list"] = rows

        if s2c.analystRatingSummaryList:
            rows = []
            for row in s2c.analystRatingSummaryList:
                rd = {}
                if row.HasField("analystInfo"):
                    rd["analyst_info"] = _analyst_rating_analyst_pb_to_dict(row.analystInfo)
                if row.ratingItemList:
                    rd["rating_item_list"] = [_analyst_rating_item_pb_to_dict(x) for x in row.ratingItemList]
                rows.append(rd)
            result["analyst_rating_summary_list"] = rows

        if s2c.HasField("instRatingDetail"):
            d = s2c.instRatingDetail
            det = {}
            if d.HasField("institutionInfo"):
                det["institution_info"] = _analyst_rating_inst_pb_to_dict(d.institutionInfo)
            if d.analystInfoList:
                det["analyst_info_list"] = [_analyst_rating_analyst_pb_to_dict(x) for x in d.analystInfoList]
            if d.ratingItemList:
                det["rating_item_list"] = [_analyst_rating_item_pb_to_dict(x) for x in d.ratingItemList]
            result["inst_rating_detail"] = det

        if s2c.HasField("analystRatingDetail"):
            d = s2c.analystRatingDetail
            det = {}
            if d.HasField("analystInfo"):
                det["analyst_info"] = _analyst_rating_analyst_pb_to_dict(d.analystInfo)
            if d.ratingItemList:
                det["rating_item_list"] = [_analyst_rating_item_pb_to_dict(x) for x in d.ratingItemList]
            result["analyst_rating_detail"] = det

        return RET_OK, "", result


class GetResearchMorningstarReportQuery:
    """
    Query `Qot_GetResearchMorningstarReport`。
    对应晨星研究详情接口
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetResearchMorningstarReport_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        return pack_pb_req(req, ProtoId.Qot_GetResearchMorningstarReport, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        def _swut(msg):
            d = {}
            if msg.HasField("context"):       d["context"] = msg.context
            if msg.HasField("updateTime"):    d["update_time"] = msg.updateTime
            if msg.HasField("updateTimeStr"): d["update_time_str"] = msg.updateTimeStr
            return d

        from ..common.constant import MorningstarRatingType

        result = {}
        s2c = rsp_pb.s2c
        if s2c.HasField("ratingType"):
            result["rating_type"] = MorningstarRatingType.to_string2(s2c.ratingType)
        if s2c.HasField("starRating"):
            result["star_rating"] = s2c.starRating
        if s2c.HasField("starUpdateTime"):
            result["star_update_time"] = s2c.starUpdateTime
        if s2c.HasField("starUpdateTimeStr"):
            result["star_update_time_str"] = s2c.starUpdateTimeStr
        if s2c.HasField("fairValue"):
            result["fair_value"] = s2c.fairValue
        if s2c.HasField("fairValueContent"):
            result["fair_value_content"] = _swut(s2c.fairValueContent)
        if s2c.HasField("economicMoatLabel"):
            result["economic_moat_label"] = s2c.economicMoatLabel
        if s2c.HasField("economicMoatContent"):
            result["economic_moat_content"] = _swut(s2c.economicMoatContent)
        if s2c.HasField("uncertaintyLabel"):
            result["uncertainty_label"] = s2c.uncertaintyLabel
        if s2c.HasField("uncertaintyContent"):
            result["uncertainty_content"] = _swut(s2c.uncertaintyContent)
        if s2c.HasField("financialHealthLabel"):
            result["financial_health_label"] = s2c.financialHealthLabel
        if s2c.HasField("financialHealthContent"):
            result["financial_health_content"] = _swut(s2c.financialHealthContent)
        result["analyst_report_by_line"] = list(s2c.analystReportByLine)
        if s2c.HasField("analystReportUpdateTime"):
            result["analyst_report_update_time"] = s2c.analystReportUpdateTime
        if s2c.HasField("analystReportUpdateTimeStr"):
            result["analyst_report_update_time_str"] = s2c.analystReportUpdateTimeStr
        result["bull_say"] = [_swut(item) for item in s2c.bullSay]
        result["bear_say"] = [_swut(item) for item in s2c.bearSay]
        if s2c.HasField("capitalAllocationLabel"):
            result["capital_allocation_label"] = s2c.capitalAllocationLabel
        if s2c.HasField("capitalAllocationContent"):
            result["capital_allocation_content"] = _swut(s2c.capitalAllocationContent)
        if s2c.HasField("analystNoteTitle"):
            result["analyst_note_title"] = _swut(s2c.analystNoteTitle)
        if s2c.HasField("analystNoteContent"):
            result["analyst_note_content"] = _swut(s2c.analystNoteContent)
        if s2c.HasField("investmentThesisContent"):
            result["investment_thesis_content"] = _swut(s2c.investmentThesisContent)
        if s2c.HasField("fundamentalsContent"):
            result["fundamentals_content"] = _swut(s2c.fundamentalsContent)
        if s2c.HasField("valuationContent"):
            result["valuation_content"] = _swut(s2c.valuationContent)
        if s2c.HasField("pdfUrl"):
            result["pdf_url"] = s2c.pdfUrl
        return RET_OK, "", result


class GetValuationDetailQuery:
    """
    Query ``Qot_GetValuationDetail`` (ProtoID 3232).
    个股/指数估值详情（合并 trend / marketDistribution / plateDistribution / profitGrowthRate）
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, valuation_type=None, interval_type=None):
        # 兼容传入枚举字符串或数值
        from ..common.constant import ValuationType, ValuationIntervalType
        valuation_type_num = _enum_or_int(ValuationType, valuation_type, "valuation_type")
        if isinstance(valuation_type_num, tuple):
            return valuation_type_num
        interval_type_num = _enum_or_int(ValuationIntervalType, interval_type, "interval_type")
        if isinstance(interval_type_num, tuple):
            return interval_type_num

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetValuationDetail_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if valuation_type_num is not None:
            req.c2s.valuationType = valuation_type_num
        if interval_type_num is not None:
            req.c2s.intervalType = interval_type_num

        return pack_pb_req(req, ProtoId.Qot_GetValuationDetail, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        from ..common.constant import ValuationType

        s2c = rsp_pb.s2c
        ret = {}
        if s2c.HasField("valuationType"):
            ret["valuation_type"] = ValuationType.to_string2(s2c.valuationType)
        if s2c.HasField("lastUpdateTime"):
            ret["last_update_time"] = s2c.lastUpdateTime
        if s2c.HasField("lastUpdateTimeStr"):
            ret["last_update_time_str"] = s2c.lastUpdateTimeStr

        # trend
        if s2c.HasField("trend"):
            t = s2c.trend
            trend = {}
            if t.HasField("currentValue"):         trend["current_value"] = t.currentValue
            if t.HasField("averageValue"):         trend["average_value"] = t.averageValue
            if t.HasField("avgMinus1Stddev"):      trend["avg_minus_1_stddev"] = t.avgMinus1Stddev
            if t.HasField("avgPlus1Stddev"):       trend["avg_plus_1_stddev"] = t.avgPlus1Stddev
            if t.HasField("valuationPercentile"):  trend["valuation_percentile"] = t.valuationPercentile
            if t.HasField("forwardValue"):         trend["forward_value"] = t.forwardValue
            hist_list = []
            for item in t.historicalItems:
                row = {}
                if item.HasField("value"):     row["value"] = item.value
                if item.HasField("time"):      row["time"] = item.time
                if item.HasField("timeStr"):   row["time_str"] = item.timeStr
                if item.HasField("plateValue"):row["plate_value"] = item.plateValue
                hist_list.append(row)
            trend["historical_items"] = hist_list
            ret["trend"] = trend

        # marketDistribution
        if s2c.HasField("marketDistribution"):
            md = s2c.marketDistribution
            mkt = {}
            sections = []
            for sec in md.sections:
                s = {}
                if sec.HasField("start"):  s["start"] = sec.start
                if sec.HasField("end"):    s["end"] = sec.end
                if sec.HasField("number"): s["number"] = sec.number
                sections.append(s)
            mkt["sections"] = sections
            if md.HasField("total"):        mkt["total"] = md.total
            if md.HasField("ranking"):      mkt["ranking"] = md.ranking
            if md.HasField("averageValue"): mkt["average_value"] = md.averageValue
            if md.HasField("medianValue"):  mkt["median_value"] = md.medianValue
            ret["market_distribution"] = mkt

        # plateDistribution（仅个股）
        if s2c.HasField("plateDistribution"):
            pd = s2c.plateDistribution
            plate = {}
            if pd.HasField("plate"):              plate["plate"] = merge_qot_mkt_stock_str(pd.plate.market, pd.plate.code)
            if pd.HasField("plateName"):          plate["plate_name"] = pd.plateName
            if pd.HasField("plateAverageValue"):  plate["plate_average_value"] = pd.plateAverageValue
            if pd.HasField("plateRanking"):       plate["plate_ranking"] = pd.plateRanking
            if pd.HasField("plateStockItemCount"):plate["plate_stock_item_count"] = pd.plateStockItemCount
            stock_items = []
            for item in pd.stockItems:
                row = {}
                if item.HasField("security"):  row["symbol"] = merge_qot_mkt_stock_str(item.security.market, item.security.code)
                if item.HasField("name"):      row["name"] = item.name
                if item.HasField("value"):     row["value"] = item.value
                if item.HasField("marketCap"): row["market_cap"] = item.marketCap
                stock_items.append(row)
            plate["stock_items"] = stock_items
            ret["plate_distribution"] = plate

        # profitGrowthRate（仅个股 PE/PS）
        if s2c.HasField("profitGrowthRate"):
            pgr = s2c.profitGrowthRate
            pgr_dict = {}
            if pgr.HasField("financialTtmMultiple"): pgr_dict["financial_ttm_multiple"] = pgr.financialTtmMultiple
            if pgr.HasField("marketCapMultiple"):    pgr_dict["market_cap_multiple"] = pgr.marketCapMultiple
            if pgr.HasField("yearCount"):            pgr_dict["year_count"] = pgr.yearCount
            if pgr.HasField("conclusionDetailed"):   pgr_dict["conclusion_detailed"] = pgr.conclusionDetailed
            profit_data = []
            for item in pgr.profitData:
                row = {}
                if item.HasField("financialYear"):      row["financial_year"] = item.financialYear
                if item.HasField("financialQuarter"):   row["financial_quarter"] = item.financialQuarter
                if item.HasField("periodStr"):          row["period_str"] = item.periodStr
                if item.HasField("reportDate"):         row["report_date"] = item.reportDate
                if item.HasField("reportDateStr"):      row["report_date_str"] = item.reportDateStr
                if item.HasField("marketCapMultiple"):  row["market_cap_multiple"] = item.marketCapMultiple
                if item.HasField("financeDataMultiple"):row["finance_data_multiple"] = item.financeDataMultiple
                profit_data.append(row)
            pgr_dict["profit_data"] = profit_data
            ret["profit_growth_rate"] = pgr_dict

        return RET_OK, "", ret


class GetValuationPlateStockListQuery:
    """
    Query ``Qot_GetValuationPlateStockList`` (ProtoID 3233).
    板块/指数成分股估值（板块如 HK.LIST23363；指数如 HK.800000）
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, valuation_type, next_key, num, sort_type, sort_id, filter_security, conn_id):
        # 兼容传入枚举字符串或数值
        from ..common.constant import ValuationType
        valuation_type_num = _enum_or_int(ValuationType, valuation_type, "valuation_type")
        if isinstance(valuation_type_num, tuple):
            return valuation_type_num

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetValuationPlateStockList_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if valuation_type_num is not None:
            req.c2s.valuationType = valuation_type_num
        if next_key is not None:
            req.c2s.nextKey = str(next_key)
        if num is not None:
            req.c2s.num = num
        if sort_type is not None:
            req.c2s.sortType = sort_type
        if sort_id is not None:
            req.c2s.sortId = sort_id
        if filter_security is not None:
            filter_ret, filter_content = split_stock_str(filter_security)
            if filter_ret == RET_OK:
                fmkt, fcode = filter_content
                req.c2s.filterSecurity.market = fmkt
                req.c2s.filterSecurity.code = fcode

        return pack_pb_req(req, ProtoId.Qot_GetValuationPlateStockList, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        if s2c.HasField("count"):   ret["count"] = s2c.count
        ret["next_key"] = s2c.nextKey if s2c.HasField("nextKey") else "-1"

        stock_list = []
        for item in s2c.stockList:
            row = {}
            if item.HasField("security"):              row["symbol"] = merge_qot_mkt_stock_str(item.security.market, item.security.code)
            if item.HasField("name") or item.name:     row["name"] = item.name
            if item.HasField("valuationVal"):          row["valuation_val"] = item.valuationVal
            if item.HasField("forwardValue"):          row["forward_value"] = item.forwardValue
            if item.HasField("valuationPercentile"):   row["valuation_percentile"] = item.valuationPercentile
            if item.HasField("marketCap"):             row["market_cap"] = item.marketCap
            stock_list.append(row)
        ret["stock_list"] = stock_list

        plate_list = []
        for item in s2c.plateList:
            entry = {}
            if item.HasField("security"):
                entry["symbol"] = merge_qot_mkt_stock_str(item.security.market, item.security.code)
            if item.name:
                entry["name"] = item.name
            plate_list.append(entry)
        ret["plate_list"] = plate_list

        return RET_OK, "", ret
class GetCorporateActionsDividendsQuery:
    """
    Query ``Qot_GetCorporateActionsDividends`` (ProtoID 3234).
    分红派息
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetCorporateActionsDividends_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetCorporateActionsDividends, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.dividendList:
            row = {}
            if item.HasField("pubDate"):             row["pub_date"] = item.pubDate
            if item.HasField("statement"):           row["statement"] = item.statement
            if item.HasField("process"):             row["process"] = item.process
            if item.HasField("recordDate"):          row["record_date"] = item.recordDate
            if item.HasField("exDate"):              row["ex_date"] = item.exDate
            if item.HasField("dividendPayableDate"): row["dividend_payable_date"] = item.dividendPayableDate
            if item.HasField("fiscalYear"):           row["fiscal_year"] = item.fiscalYear
            ret_list.append(row)

        return RET_OK, "", {"dividend_list": ret_list}


class GetCorporateActionsBuybacksQuery:
    """
    Query ``Qot_GetCorporateActionsBuybacks`` (ProtoID 3235).
    回购
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, next_key=None, num=None):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetCorporateActionsBuybacks_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if next_key is not None:
            req.c2s.nextKey = next_key
        if num is not None:
            req.c2s.num = int(num)

        return pack_pb_req(req, ProtoId.Qot_GetCorporateActionsBuybacks, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        hk_list = []
        for item in s2c.hkBuyBackList:
            row = {}
            if item.HasField("publDate"):             row["publ_date"] = item.publDate
            if item.HasField("publDateStr"):          row["publ_date_str"] = item.publDateStr
            if item.HasField("endDate"):              row["end_date"] = item.endDate
            if item.HasField("endDateStr"):           row["end_date_str"] = item.endDateStr
            if item.HasField("buyBackMoney"):         row["buy_back_money"] = item.buyBackMoney
            if item.HasField("buyBackSum"):           row["buy_back_sum"] = item.buyBackSum
            if item.HasField("percentage"):           row["percentage"] = item.percentage
            if item.HasField("highPrice"):            row["high_price"] = item.highPrice
            if item.HasField("lowPrice"):             row["low_price"] = item.lowPrice
            if item.HasField("cumulativeSum"):        row["cumulative_sum"] = item.cumulativeSum
            if item.HasField("cumulativePercentage"): row["cumulative_percentage"] = item.cumulativePercentage
            if item.HasField("shareType"):            row["share_type"] = item.shareType
            hk_list.append(row)

        a_list = []
        for item in s2c.aBuyBackList:
            row = {}
            if item.HasField("changeRegDate"):    row["change_reg_date"] = item.changeRegDate
            if item.HasField("changeRegDateStr"): row["change_reg_date_str"] = item.changeRegDateStr
            if item.HasField("changeDate"):       row["change_date"] = item.changeDate
            if item.HasField("changeDateStr"):    row["change_date_str"] = item.changeDateStr
            if item.HasField("eventProceDesc"):   row["event_proce_desc"] = item.eventProceDesc
            if item.HasField("advanceDate"):      row["advance_date"] = item.advanceDate
            if item.HasField("advanceDateStr"):   row["advance_date_str"] = item.advanceDateStr
            if item.HasField("meetPassDate"):     row["meet_pass_date"] = item.meetPassDate
            if item.HasField("meetPassDateStr"):  row["meet_pass_date_str"] = item.meetPassDateStr
            if item.HasField("startDate"):        row["start_date"] = item.startDate
            if item.HasField("startDateStr"):     row["start_date_str"] = item.startDateStr
            if item.HasField("endDate"):          row["end_date"] = item.endDate
            if item.HasField("endDateStr"):       row["end_date_str"] = item.endDateStr
            if item.HasField("payDate"):          row["pay_date"] = item.payDate
            if item.HasField("payDateStr"):       row["pay_date_str"] = item.payDateStr
            if item.HasField("seller"):           row["seller"] = item.seller
            if item.HasField("buyBackMode"):      row["buy_back_mode"] = item.buyBackMode
            if item.HasField("shareType"):        row["share_type"] = item.shareType
            if item.HasField("buyBackSum"):       row["buy_back_sum"] = item.buyBackSum
            if item.HasField("buyBackMoney"):     row["buy_back_money"] = item.buyBackMoney
            if item.HasField("percentage"):       row["percentage"] = item.percentage
            if item.HasField("valueFloor"):       row["value_floor"] = item.valueFloor
            if item.HasField("valueCeiling"):     row["value_ceiling"] = item.valueCeiling
            if item.HasField("priceFloor"):       row["price_floor"] = item.priceFloor
            if item.HasField("priceCeiling"):     row["price_ceiling"] = item.priceCeiling
            if item.HasField("volumeFloor"):      row["volume_floor"] = item.volumeFloor
            if item.HasField("volumeCeiling"):    row["volume_ceiling"] = item.volumeCeiling
            a_list.append(row)

        next_key = s2c.nextKey if s2c.HasField("nextKey") else "-1"
        return RET_OK, "", {"next_key": next_key, "hk_buy_back_list": hk_list, "a_buy_back_list": a_list}


class GetCorporateActionsStockSplitsQuery:
    """
    Query ``Qot_GetCorporateActionsStockSplits`` (ProtoID 3236).
    拆合股（支持港股及非港股，服务端按 security.market 自动路由）
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, next_key=None, num=None):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetCorporateActionsStockSplits_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if next_key is not None:
            req.c2s.nextKey = next_key
        if num is not None:
            req.c2s.num = int(num)

        return pack_pb_req(req, ProtoId.Qot_GetCorporateActionsStockSplits, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.splitItemList:
            row = {}
            # 通用字段
            if item.HasField("dirDeciPubDate"):        row["dir_deci_pub_date"] = item.dirDeciPubDate
            if item.HasField("dirDeciPubDateStr"):     row["dir_deci_pub_date_str"] = item.dirDeciPubDateStr
            if item.HasField("reformType"):            row["reform_type"] = item.reformType
            if item.HasField("rate"):                  row["rate"] = item.rate
            # 港股专有字段
            if item.HasField("exDate"):                row["ex_date"] = item.exDate
            if item.HasField("exDateStr"):             row["ex_date_str"] = item.exDateStr
            if item.HasField("smDeciDate"):            row["sm_deci_date"] = item.smDeciDate
            if item.HasField("smDeciDateStr"):         row["sm_deci_date_str"] = item.smDeciDateStr
            if item.HasField("tempTradeBeginDate"):    row["temp_trade_begin_date"] = item.tempTradeBeginDate
            if item.HasField("tempTradeBeginDateStr"): row["temp_trade_begin_date_str"] = item.tempTradeBeginDateStr
            if item.HasField("simulTradeBeginDate"):   row["simul_trade_begin_date"] = item.simulTradeBeginDate
            if item.HasField("simulTradeBeginDateStr"):row["simul_trade_begin_date_str"] = item.simulTradeBeginDateStr
            if item.HasField("simulTradeEndDate"):     row["simul_trade_end_date"] = item.simulTradeEndDate
            if item.HasField("simulTradeEndDateStr"):  row["simul_trade_end_date_str"] = item.simulTradeEndDateStr
            if item.HasField("eventStatus"):           row["event_status"] = item.eventStatus
            if item.HasField("newParValue"):           row["new_par_value"] = item.newParValue
            if item.HasField("tempShareCode"):         row["temp_share_code"] = item.tempShareCode
            if item.HasField("tempShareAbbrName"):     row["temp_share_abbr_name"] = item.tempShareAbbrName
            if item.HasField("newTradeUnit"):          row["new_trade_unit"] = item.newTradeUnit
            if item.HasField("sharesAfterEffect"):     row["shares_after_effect"] = item.sharesAfterEffect
            ret_list.append(row)

        next_key = s2c.nextKey if s2c.HasField("nextKey") else "-1"
        return RET_OK, "", {"next_key": next_key, "split_list": ret_list}




class GetShareholdersOverviewQuery:
    """
    Query ``Qot_GetShareholdersOverview`` (ProtoID 3237).
    持股统计：一次请求同时返回主要股东和持股类型数据
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, period_id=None):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetShareholdersOverview_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if period_id is not None and period_id != 0:
            req.c2s.periodId = period_id

        return pack_pb_req(req, ProtoId.Qot_GetShareholdersOverview, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c

        def _parse_info_list(proto_list):
            out = []
            for info in proto_list:
                row_info = {}
                if info.HasField("staticDate"):
                    row_info["static_date"] = info.staticDate
                if info.HasField("staticDateStr"):
                    row_info["static_date_str"] = info.staticDateStr
                items = []
                for it in info.itemList:
                    row = {}
                    if it.HasField("name"):
                        row["name"] = it.name
                    if it.HasField("holderPct"):
                        row["holder_pct"] = round(it.holderPct, 6)
                    if it.HasField("holderId"):
                        row["holder_id"] = it.holderId
                    items.append(row)
                row_info["item_list"] = items
                out.append(row_info)
            return out

        hp_list = []
        for it in s2c.holdingPeriodList:
            row = {
                "period_id": it.periodId,
                "period_text": it.periodText if it.HasField("periodText") else "",
            }
            hp_list.append(row)

        return RET_OK, "", {
            "main_holder_list": _parse_info_list(s2c.mainHolderInfoList),
            "holder_type_list": _parse_info_list(s2c.holderTypeInfoList),
            "holding_period_list": hp_list,
        }


class GetShareholdersHoldingChangesQuery:
    """
    Query ``Qot_GetShareholdersHoldingChanges`` (ProtoID 3238).
    持股变动
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, next_key=None, num=None, sort_type=None, sort_column=None, filter_type=None):
        # 兼容传入枚举字符串或数值
        from ..common.constant import HoldingChangesFilterType
        filter_type_num = _enum_or_int(HoldingChangesFilterType, filter_type, "filter_type")
        if isinstance(filter_type_num, tuple):
            return filter_type_num

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetShareholdersHoldingChanges_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if next_key is not None and next_key != 0:
            req.c2s.nextKey = next_key
        if num is not None:
            req.c2s.num = num
        if sort_type is not None:
            req.c2s.sortType = sort_type
        if sort_column is not None and sort_column != 0:
            req.c2s.sortColumn = sort_column
        if filter_type_num is not None and filter_type_num != 0:
            req.c2s.filterType = filter_type_num

        return pack_pb_req(req, ProtoId.Qot_GetShareholdersHoldingChanges, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        ret["next_key"] = s2c.nextKey if s2c.HasField("nextKey") else "-1"
        item_list = []
        for item in s2c.itemList:
            row = {}
            if item.HasField("periodText"):
                row["period_text"] = item.periodText
            if item.HasField("name"):
                row["name"] = item.name
            if item.HasField("holderId"):
                row["holder_id"] = item.holderId
            if item.HasField("shareChangeNum"):
                row["share_change_num"] = item.shareChangeNum
            if item.HasField("sharesChangePrice"):
                row["shares_change_price"] = item.sharesChangePrice
            if item.HasField("holderPct"):
                row["holder_pct"] = item.holderPct
            if item.HasField("holderType"):
                row["holder_type"] = item.holderType
            if item.HasField("holderTypeId"):
                row["holder_type_id"] = item.holderTypeId
            if item.HasField("holdingDate"):
                row["holding_date"] = item.holdingDate
            if item.HasField("holdingDateStr"):
                row["holding_date_str"] = item.holdingDateStr
            if item.HasField("holderPctChange"):
                row["holder_pct_change"] = item.holderPctChange
            if item.HasField("holderQuantity"):
                row["holder_quantity"] = item.holderQuantity
            item_list.append(row)
        ret["item_list"] = item_list

        return RET_OK, "", ret


class GetShareholdersHolderDetailQuery:
    """
    Query ``Qot_GetShareholdersHolderDetail`` (ProtoID 3239).
    持股明细
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, request_type=None, next_key=None, num=None, sort_column=None, sort_type=None, period_id=None, holder_id=None):
        # 兼容传入枚举字符串或数值
        from ..common.constant import HolderDetailType
        request_type_num = _enum_or_int(HolderDetailType, request_type, "request_type")
        if isinstance(request_type_num, tuple):
            return request_type_num

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetShareholdersHolderDetail_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if request_type_num is not None and request_type_num != 0:
            req.c2s.requestType = request_type_num
        if next_key:
            req.c2s.nextKey = next_key
        if num is not None:
            req.c2s.num = num
        if sort_column is not None and sort_column != 0:
            req.c2s.sortColumn = sort_column
        if sort_type is not None:
            req.c2s.sortType = sort_type
        if period_id is not None and period_id != 0:
            req.c2s.periodId = period_id
        if holder_id is not None and holder_id != 0:
            req.c2s.holderId = holder_id

        return pack_pb_req(req, ProtoId.Qot_GetShareholdersHolderDetail, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        if s2c.HasField("updateTime"):
            ret["update_time"] = s2c.updateTime
        if s2c.HasField("updateTimeStr"):
            ret["update_time_str"] = s2c.updateTimeStr
        ret["next_key"] = s2c.nextKey if s2c.HasField("nextKey") else "-1"
        item_list = []
        for item in s2c.itemList:
            row = {}
            if item.HasField("periodText"):
                row["period_text"] = item.periodText
            if item.HasField("holderId"):
                row["holder_id"] = item.holderId
            if item.HasField("name"):
                row["name"] = item.name
            if item.HasField("holderQuantity"):
                row["holder_quantity"] = item.holderQuantity
            if item.HasField("holderQuantityChange"):
                row["holder_quantity_change"] = item.holderQuantityChange
            if item.HasField("holderPct"):
                row["holder_pct"] = item.holderPct
            if item.HasField("holderPctChange"):
                row["holder_pct_change"] = item.holderPctChange
            if item.HasField("holdingDate"):
                row["holding_date"] = item.holdingDate
            if item.HasField("holdingDateStr"):
                row["holding_date_str"] = item.holdingDateStr
            if item.HasField("closePrice"):
                row["close_price"] = item.closePrice
            if item.HasField("priceChangePct"):
                row["price_change_pct"] = item.priceChangePct
            if item.HasField("sourceGroupName"):
                row["source_group_name"] = item.sourceGroupName
            item_list.append(row)
        ret["item_list"] = item_list

        return RET_OK, "", ret


class GetShareholdersInstitutionalQuery:
    """
    Query ``Qot_GetShareholdersInstitutional`` (ProtoID 3240).
    机构持股
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, next_key, num, conn_id):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetShareholdersInstitutional_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if next_key is not None:
            req.c2s.nextKey = next_key
        req.c2s.num = int(num) if num is not None else 10

        return pack_pb_req(req, ProtoId.Qot_GetShareholdersInstitutional, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        if s2c.HasField("updateTime"):
            ret["update_time"] = s2c.updateTime
        if s2c.HasField("updateTimeStr"):
            ret["update_time_str"] = s2c.updateTimeStr
        ret["next_key"] = s2c.nextKey if s2c.HasField("nextKey") else "-1"
        item_rows = []
        for item in s2c.itemList:
            row = {}
            if item.HasField("periodText"):
                row["period_text"] = item.periodText
            if item.HasField("institutionQuantity"):
                row["institution_quantity"] = item.institutionQuantity
            if item.HasField("institutionQuantityChange"):
                row["institution_quantity_change"] = item.institutionQuantityChange
            if item.HasField("holderQuantity"):
                row["holder_quantity"] = item.holderQuantity
            if item.HasField("holderQuantityChange"):
                row["holder_quantity_change"] = item.holderQuantityChange
            if item.HasField("holderPct"):
                row["holder_pct"] = item.holderPct
            if item.HasField("holderPctChange"):
                row["holder_pct_change"] = item.holderPctChange
            item_rows.append(row)
        ret["item_list"] = item_rows
        return RET_OK, "", ret


class GetInsiderHolderListQuery:
    """
    Query ``Qot_GetInsiderHolderList`` (ProtoID 3241).
    内部人持股列表
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, next_key=None, num=None):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetInsiderHolderList_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if next_key is not None:
            req.c2s.nextKey = next_key
        if num is not None:
            req.c2s.num = num

        return pack_pb_req(req, ProtoId.Qot_GetInsiderHolderList, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        if s2c.HasField("allCount"):
            ret["all_count"] = s2c.allCount
        ret["next_key"] = s2c.nextKey if s2c.HasField("nextKey") else "-1"
        if s2c.HasField("insiderTotalCount"):
            ret["insider_total_count"] = s2c.insiderTotalCount
        if s2c.HasField("insiderBoughtCount"):
            ret["insider_bought_count"] = s2c.insiderBoughtCount
        if s2c.HasField("insiderSoldCount"):
            ret["insider_sold_count"] = s2c.insiderSoldCount
        item_list = []
        for item in s2c.itemList:
            row = {}
            if item.HasField("holderId"):
                row["holder_id"] = item.holderId
            if item.HasField("holderQuantity"):
                row["holder_quantity"] = item.holderQuantity
            if item.HasField("holderPct"):
                row["holder_pct"] = item.holderPct
            if item.HasField("name"):
                row["name"] = item.name
            if item.HasField("title"):
                row["title"] = item.title
            item_list.append(row)
        ret["item_list"] = item_list

        return RET_OK, "", ret


class GetInsiderTradeListQuery:
    """
    Query ``Qot_GetInsiderTradeList`` (ProtoID 3242).
    内部人交易列表
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, holder_id=None, num=None, next_key=None):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetInsiderTradeList_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if holder_id is not None:
            req.c2s.holderId = holder_id
        if num is not None:
            req.c2s.num = num
        if next_key is not None:
            req.c2s.nextKey = str(next_key)

        return pack_pb_req(req, ProtoId.Qot_GetInsiderTradeList, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        if s2c.HasField("allCount"):
            ret["all_count"] = s2c.allCount
        ret["next_key"] = s2c.nextKey if s2c.HasField("nextKey") else "-1"
        item_list = []
        for item in s2c.itemList:
            row = {}
            if item.HasField("tradeShares"):
                row["trade_shares"] = item.tradeShares
            if item.HasField("minTradeDate"):
                row["min_trade_date"] = item.minTradeDate
            if item.HasField("minTradeDateStr"):
                row["min_trade_date_str"] = item.minTradeDateStr
            if item.HasField("maxTradeDate"):
                row["max_trade_date"] = item.maxTradeDate
            if item.HasField("maxTradeDateStr"):
                row["max_trade_date_str"] = item.maxTradeDateStr
            if item.HasField("minPrice"):
                row["min_price"] = item.minPrice
            if item.HasField("maxPrice"):
                row["max_price"] = item.maxPrice
            if item.HasField("securityHolderQuantity"):
                row["security_holder_quantity"] = item.securityHolderQuantity
            if item.HasField("isProposedSaleOfSecurities"):
                row["is_proposed_sale_of_securities"] = item.isProposedSaleOfSecurities
            if item.HasField("holderId"):
                row["holder_id"] = item.holderId
            if item.HasField("name"):
                row["name"] = item.name
            if item.HasField("title"):
                row["title"] = item.title
            if item.HasField("securityDescription"):
                row["security_description"] = item.securityDescription
            if item.HasField("transactionType"):
                row["transaction_type"] = item.transactionType
            if item.HasField("sourceGroupName"):
                row["source_group_name"] = item.sourceGroupName
            item_list.append(row)
        ret["item_list"] = item_list

        return RET_OK, "", ret


class GetCompanyProfileQuery:
    """
    Query ``Qot_GetCompanyProfile`` (ProtoID 3243).
    公司详情
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):
        """
        :param code:    股票代码，如 "US.AAPL"
        :param conn_id: 连接 ID
        """
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetCompanyProfile_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetCompanyProfile, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = []
        for item in rsp_pb.s2c.itemList:
            row = {}
            if item.HasField("name"):
                row["name"] = item.name
            if item.HasField("value"):
                row["value"] = item.value
            if item.HasField("fieldType"):
                row["field_type"] = item.fieldType
            ret_list.append(row)

        return RET_OK, "", ret_list


class GetCompanyExecutivesQuery:
    """
    Query ``Qot_GetCompanyExecutives`` (ProtoID 3244).
    公司高管信息
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):
        """
        :param code:    股票代码，如 "US.AAPL"
        :param conn_id: 连接 ID
        """
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetCompanyExecutives_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetCompanyExecutives, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = []
        for d in rsp_pb.s2c.directorList:
            row = {}
            if d.HasField("displayLeaderName"):
                row["display_leader_name"] = d.displayLeaderName
            if d.HasField("leaderName"):
                row["leader_name"] = d.leaderName
            if d.HasField("positionName"):
                row["position_name"] = d.positionName
            if d.HasField("beginDate"):
                row["begin_date"] = d.beginDate
            if d.HasField("beginDateStr"):
                row["begin_date_str"] = d.beginDateStr
            if d.HasField("leaderGender"):
                row["leader_gender"] = d.leaderGender
            if d.HasField("leaderAge"):
                row["leader_age"] = d.leaderAge
            if d.HasField("highestEducation"):
                row["highest_education"] = d.highestEducation
            if d.HasField("annualSalary"):
                row["annual_salary"] = d.annualSalary
            if d.HasField("issueDate"):
                row["issue_date"] = d.issueDate
            if d.HasField("issueDateStr"):
                row["issue_date_str"] = d.issueDateStr
            ret_list.append(row)

        return RET_OK, "", ret_list


class GetCompanyExecutiveBackgroundQuery:
    """
    Query ``Qot_GetCompanyExecutiveBackground`` (ProtoID 3245).
    公司高管背景信息
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, leader_name=None):
        """
        :param code:         股票代码，如 "US.AAPL"
        :param conn_id:      连接 ID
        :param leader_name:  高管姓名（使用 get_company_executives 返回的 leader_name 字段）
        """
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetCompanyExecutiveBackground_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if leader_name is not None:
            req.c2s.leaderName = leader_name

        return pack_pb_req(req, ProtoId.Qot_GetCompanyExecutiveBackground, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        result = {
            "brief_background": s2c.briefBackground if s2c.HasField("briefBackground") else "",
        }
        return RET_OK, "", result


class GetCompanyOperationalEfficiencyQuery:
    """
    Query ``Qot_GetCompanyOperationalEfficiency`` (ProtoID 3246).
    公司经营效率
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, num=None, next_key=None, currency_code=None):
        """
        :param code:           股票代码，如 "US.AAPL"
        :param conn_id:        连接 ID
        :param num:            请求条数（默认 10，最大 100）
        :param next_key:       分页标识（首次传 None）
        :param currency_code:  货币代码（ISO 4217，不传返回默认货币）
        """
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetCompanyOperationalEfficiency_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if num is not None:
            req.c2s.num = num
        if next_key is not None:
            req.c2s.nextKey = next_key
        if currency_code is not None:
            req.c2s.currencyCode = currency_code

        return pack_pb_req(req, ProtoId.Qot_GetCompanyOperationalEfficiency, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.itemList:
            row = {}
            if item.HasField("fiscalYear"):
                row["fiscal_year"] = item.fiscalYear
            if item.HasField("financialType"):
                row["financial_type"] = item.financialType
            if item.HasField("periodText"):
                row["period_text"] = item.periodText
            if item.HasField("endDate"):
                row["end_date"] = item.endDate
            if item.HasField("endDateStr"):
                row["end_date_str"] = item.endDateStr
            if item.HasField("employeeNum"):
                row["employee_num"] = item.employeeNum
            if item.HasField("employeeNumYoy"):
                row["employee_num_yoy"] = item.employeeNumYoy
            if item.HasField("incomePerCapita"):
                row["income_per_capita"] = item.incomePerCapita
            if item.HasField("incomePerCapitaYoy"):
                row["income_per_capita_yoy"] = item.incomePerCapitaYoy
            if item.HasField("profitPerCapita"):
                row["profit_per_capita"] = item.profitPerCapita
            if item.HasField("profitPerCapitaYoy"):
                row["profit_per_capita_yoy"] = item.profitPerCapitaYoy
            if item.HasField("netProfitPerCapita"):
                row["net_profit_per_capita"] = item.netProfitPerCapita
            if item.HasField("netProfitPerCapitaYoy"):
                row["net_profit_per_capita_yoy"] = item.netProfitPerCapitaYoy
            ret_list.append(row)

        result = {
            "item_list": ret_list,
            "next_key": s2c.nextKey if s2c.HasField("nextKey") else "-1",
            "currency_code": s2c.currencyCode if s2c.HasField("currencyCode") else "",
        }
        return RET_OK, "", result


class GetTopTenBuySellBrokersQuery:
    """
    Query `Qot_GetTopTenBuySellBrokers`。
    获取十大买卖经纪商。daysBefore=0 走实时（SecCapTrack），daysBefore>0 走历史第 N 个交易日（TenBrokerHold）
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, days_before=None):
        """check stock_code 股票"""
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetTopTenBuySellBrokers_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if days_before is not None:
            req.c2s.daysBefore = days_before

        return pack_pb_req(req, ProtoId.Qot_GetTopTenBuySellBrokers, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret_list = []
        for item in s2c.brokerList:
            data = {}
            data["net_vol"] = item.netVol
            data["is_real_time"] = s2c.isRealTime
            data["buy_sell_type"] = item.buySellType
            data["data_time"] = s2c.dataTime if s2c.HasField("dataTime") else 0
            data["data_time_str"] = s2c.dataTimeStr if s2c.HasField("dataTimeStr") else ""
            data["broker_name"] = item.brokerName if item.HasField("brokerName") else ""
            if s2c.isRealTime:
                data["avg_price"] = item.avgPrice if item.HasField("avgPrice") else 0.0
                data["total_vol"] = item.totalVol if item.HasField("totalVol") else 0.0
                data["total_turnover"] = item.totalTurnover if item.HasField("totalTurnover") else 0.0
            ret_list.append(data)
        return RET_OK, "", ret_list


class GetDailyShortVolumeQuery:
    """
    Query ``Qot_GetDailyShortVolume`` (ProtoID 3248).
    每日卖空（美股/港股）
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, next_key=None, num=None):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetDailyShortVolume_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if next_key is not None:
            req.c2s.nextKey = next_key
        if num is not None:
            req.c2s.num = num

        return pack_pb_req(req, ProtoId.Qot_GetDailyShortVolume, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        ret["next_key"] = s2c.nextKey if s2c.HasField("nextKey") else "-1"
        if s2c.HasField("aggregatedShort"):
            ret["aggregated_short"] = s2c.aggregatedShort
        if s2c.HasField("aggregatedShortRatio"):
            ret["aggregated_short_ratio"] = s2c.aggregatedShortRatio
        if s2c.HasField("newTimeStr"):
            ret["new_time_str"] = s2c.newTimeStr

        us_item_list = []
        for item in s2c.usItemList:
            row = {}
            if item.HasField("timestamp"):
                row["timestamp"] = item.timestamp
            if item.HasField("timestampStr"):
                row["timestamp_str"] = item.timestampStr
            if item.HasField("totalSharesShort"):
                row["total_shares_short"] = item.totalSharesShort
            if item.HasField("nasdaqSharesShort"):
                row["nasdaq_shares_short"] = item.nasdaqSharesShort
            if item.HasField("nyseSharesShort"):
                row["nyse_shares_short"] = item.nyseSharesShort
            if item.HasField("shortPercent"):
                row["short_percent"] = item.shortPercent
            if item.HasField("volume"):
                row["volume"] = item.volume
            if item.HasField("closePrice"):
                row["close_price"] = item.closePrice
            if item.HasField("lastClosePrice"):
                row["last_close_price"] = item.lastClosePrice
            if item.HasField("dailyTradeAvgRatio"):
                row["daily_trade_avg_ratio"] = item.dailyTradeAvgRatio
            us_item_list.append(row)
        ret["us_item_list"] = us_item_list

        hk_item_list = []
        for item in s2c.hkItemList:
            row = {}
            if item.HasField("timestamp"):
                row["timestamp"] = item.timestamp
            if item.HasField("timestampStr"):
                row["timestamp_str"] = item.timestampStr
            if item.HasField("sharesTraded"):
                row["shares_traded"] = item.sharesTraded
            if item.HasField("turnover"):
                row["turnover"] = item.turnover
            if item.HasField("shortSellSharesTraded"):
                row["short_sell_shares_traded"] = item.shortSellSharesTraded
            if item.HasField("shortSellTurnover"):
                row["short_sell_turnover"] = item.shortSellTurnover
            if item.HasField("openPrice"):
                row["open_price"] = item.openPrice
            if item.HasField("closePrice"):
                row["close_price"] = item.closePrice
            if item.HasField("lastClosePrice"):
                row["last_close_price"] = item.lastClosePrice
            if item.HasField("dailyTradeAvgRatio"):
                row["daily_trade_avg_ratio"] = item.dailyTradeAvgRatio
            hk_item_list.append(row)
        ret["hk_item_list"] = hk_item_list

        return RET_OK, "", ret


class GetShortInterestQuery:
    """
    Query ``Qot_GetShortInterest`` (ProtoID 3249).
    空头持仓（美股/港股）
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, next_key=None, num=None):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetShortInterest_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if next_key is not None and next_key != "":
            req.c2s.nextKey = next_key
        if num is not None:
            req.c2s.num = num

        return pack_pb_req(req, ProtoId.Qot_GetShortInterest, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        ret["next_key"] = s2c.nextKey if s2c.HasField("nextKey") else "-1"

        us_item_list = []
        for item in s2c.usItemList:
            row = {}
            if item.HasField("timestamp"):
                row["timestamp"] = item.timestamp
            if item.HasField("timestampStr"):
                row["timestamp_str"] = item.timestampStr
            if item.HasField("sharesShort"):
                row["shares_short"] = item.sharesShort
            if item.HasField("shortPercent"):
                row["short_percent"] = item.shortPercent
            if item.HasField("avgDailyShareVolume"):
                row["avg_daily_share_volume"] = item.avgDailyShareVolume
            if item.HasField("daysToCover"):
                row["days_to_cover"] = item.daysToCover
            if item.HasField("closePrice"):
                row["close_price"] = item.closePrice
            if item.HasField("lastClosePrice"):
                row["last_close_price"] = item.lastClosePrice
            us_item_list.append(row)
        ret["us_item_list"] = us_item_list

        hk_item_list = []
        for item in s2c.hkItemList:
            row = {}
            if item.HasField("timestamp"):
                row["timestamp"] = item.timestamp
            if item.HasField("timestampStr"):
                row["timestamp_str"] = item.timestampStr
            if item.HasField("closePrice"):
                row["close_price"] = item.closePrice
            if item.HasField("lastClosePrice"):
                row["last_close_price"] = item.lastClosePrice
            if item.HasField("aggregatedShort"):
                row["aggregated_short"] = item.aggregatedShort
            if item.HasField("aggregatedShortRatio"):
                row["aggregated_short_ratio"] = item.aggregatedShortRatio
            hk_item_list.append(row)
        ret["hk_item_list"] = hk_item_list

        return RET_OK, "", ret


class GetOptionVolatilityQuery:
    """
    Query ``Qot_GetOptionVolatility`` (ProtoID 3250).
    期权波动率分析
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, query_time_period=None, hv_time_period=None):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetOptionVolatility_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if query_time_period is not None:
            req.c2s.queryTimePeriod = query_time_period
        if hv_time_period is not None:
            req.c2s.hvTimePeriod = hv_time_period

        return pack_pb_req(req, ProtoId.Qot_GetOptionVolatility, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        if s2c.HasField("averageImpvol"):
            ret["average_impvol"] = s2c.averageImpvol
        if s2c.HasField("impvolStatus"):
            ret["impvol_status"] = s2c.impvolStatus
        if s2c.HasField("analysis"):
            ret["analysis"] = s2c.analysis
        item_list = []
        for item in s2c.itemList:
            row = {}
            if item.HasField("timestamp"):
                row["timestamp"] = item.timestamp
            if item.HasField("impliedVolatility"):
                row["implied_volatility"] = item.impliedVolatility
            if item.HasField("historyVolatility"):
                row["history_volatility"] = item.historyVolatility
            if item.HasField("volatilityPremium"):
                row["volatility_premium"] = item.volatilityPremium
            if item.HasField("timestampStr"):
                row["timestamp_str"] = item.timestampStr
            item_list.append(row)
        ret["item_list"] = item_list

        return RET_OK, "", ret


class GetOptionExerciseProbabilityQuery:
    """
    Query ``Qot_GetOptionExerciseProbability`` (ProtoID 3251).
    期权行权概率
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        from ..common.pb.Qot_GetOptionExerciseProbability_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetOptionExerciseProbability, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        ret = {}
        item_list = []
        for item in s2c.itemList:
            row = {}
            if item.HasField("timestamp"):
                row["timestamp"] = item.timestamp
            if item.HasField("securityPrice"):
                row["security_price"] = item.securityPrice
            if item.HasField("strikeProbability"):
                row["strike_probability"] = item.strikeProbability
            if item.HasField("timestampStr"):
                row["timestamp_str"] = item.timestampStr
            item_list.append(row)
        ret["item_list"] = item_list

        return RET_OK, "", ret

# =================== StockScreen (3252) — Builder 类 ===================


class StockScreenRequest(object):
    """条件选股V2 请求构建器 (ProtoID 3252)

    值字段使用 float/double, OpenD 负责与后端 int64 倍率互转。

    所有可枚举参数都建议直接用 ``futu.quote.stock_screen_const`` 里的 ``IntEnum``,
    避免裸数字魔法值; ``IntEnum`` 可以直接当 ``int`` 使用。

    用法::

        from futu import OpenQuoteContext, RET_OK, StockScreenRequest
        from futu.quote.stock_screen_const import (
            ScrMarket, ScrSortDir, SimpleField, SimpleProperty,
            CumulativeProperty, FinancialProperty, Term,
            Indicator, Period, Position, Pattern,
            FeaturedProperty, BrokerProperty,
            KlineShapeProperty, KlineShapeType,
            OptionProperty, OptionHVPeriod, BasicProperty,
        )

        req = StockScreenRequest()
        # 市场 (枚举值传 ScrMarket, 不要传 QotMarket)
        req.add_simple_field(field=SimpleField.MARKET, values=[ScrMarket.HK])
        # 简单属性 (lower/upper 直接传原始值, OpenD 负责倍率)
        req.add_simple_property(name=SimpleProperty.PRICE, lower=10.0)
        req.add_simple_property(name=SimpleProperty.MARKET_CAP, lower=10_000_000_000.0)
        # 累计属性
        req.add_cumulative_property(
            name=CumulativeProperty.PRICE_CHANGE_PCT, days=5, lower=5.0)
        # 财务属性 (term 用 Term 枚举)
        req.add_financial_property(
            name=FinancialProperty.NET_PROFIT, term=Term.ANNUAL,
            lower=100_000_000.0)
        # 技术指标位置: MA5 上穿 MA20 (日K)
        req.add_indicator_positional(
            first_indicator_name=Indicator.MA5,
            period_type=Period.DAY,
            position=Position.CROSS_UP,
            second_indicator=Indicator.MA20)
        # 形态: MACD 低位金叉
        req.add_indicator_pattern(
            name=Pattern.MACD_GOLD_CROSS, period_type=Period.DAY)
        # 特色因子: 筹码获利比例 50~100
        req.add_featured_property(
            name=FeaturedProperty.CHIPS_PROFIT_RATIO,
            intervals=[{
                'filterMin': {'value': 50.0, 'includes': True},
                'filterMax': {'value': 100.0, 'includes': True},
            }])
        # 经纪商: 集中度 (近30日, 取前10名经纪商)
        req.add_broker_holdings(
            name=BrokerProperty.CONCENTRATED_DISTRIBUTION,
            days=30, param='10',
            intervals=[{'filterMin': {'value': 50.0, 'includes': True}}])
        # K线形态: W型底 + 头肩底 (日K)
        req.add_kline_shape(
            name=KlineShapeProperty.SHAPE_TYPE,
            period=Period.DAY,
            value_set=[KlineShapeType.DOUBLE_BOTTOMS,
                       KlineShapeType.HEAD_SHOULDERS_BOTTOM])
        # 期权属性: 正股IV 20%~100%, HV 周期 30 天
        req.add_option(
            name=OptionProperty.STOCK_IV,
            period=OptionHVPeriod.HV_30D,
            intervals=[{
                'filterMin': {'value': 20.0, 'includes': True},
                'filterMax': {'value': 100.0, 'includes': True},
            }])

        # 取回属性 (枚举类型字段会自动解码 enum_name)
        req.add_retrieve_basic(name=BasicProperty.CODE)
        req.add_retrieve_basic(name=BasicProperty.NAME)
        req.add_retrieve_simple(name=SimpleProperty.PRICE)
        req.add_retrieve_simple(name=SimpleProperty.MARKET_CAP)
        req.add_retrieve_financial(
            name=FinancialProperty.NET_PROFIT, term=Term.ANNUAL)
        req.add_retrieve_kline_shape(
            name=KlineShapeProperty.SHAPE_TYPE, period=Period.DAY)

        # 排序: 单字段
        req.set_sort(
            direction=ScrSortDir.DESC,
            property_type='simple',
            property_params={'name': int(SimpleProperty.MARKET_CAP)})
        # 或多字段 (有值时优先于 set_sort)
        req.add_sort(direction=ScrSortDir.ASC, property_type='simple',
                     property_params={'name': int(SimpleProperty.PE_TTM)})
        req.add_sort(direction=ScrSortDir.DESC, property_type='simple',
                     property_params={'name': int(SimpleProperty.MARKET_CAP)})

        # 分页
        req.page_from = 0
        req.page_count = 50

        ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        ret, data = ctx.get_stock_screen(req)
        if ret == RET_OK:
            last_page, all_count, items = data
    """

    def __init__(self):
        self.page_from = 0
        self.page_count = 200
        self._queries = []      # list of (type_str, params_dict)
        self._retrieves = []    # list of (type_str, params_dict)
        self._sort = None       # (direction, type_str, params_dict)
        self._sorts = []        # list of (direction, type_str, params_dict)

    # ---------- 筛选条件 (ScreenQuery) ----------

    def add_simple_field(self, field, values):
        """市场/交易所/指数/自选股等简单字段筛选

        :param field: int, SimpleField 枚举 (1=市场, 2=交易所, 3=指数, 4=自选股, ...)
        :param values: list of int, 筛选值列表 (并集关系)
        """
        self._queries.append(('simpleFieldQuery', {
            'simpleField': int(field), 'screenValueList': [int(v) for v in values]}))

    def add_plate(self, plate_ids, parent_plate_id=None):
        """板块筛选

        :param plate_ids: list of str, 板块代码列表 (如 ["BK1001","BK1002"]), 与 get_plate_list 返回的 plate_id 一致
        :param parent_plate_id: str or None, 父板块代码 (如 "BK1000")
        """
        plate = {
            'plateIdList': [str(pid) for pid in plate_ids]
        }
        if parent_plate_id is not None:
            plate['parentPlateId'] = str(parent_plate_id)
        self._queries.append(('plateQuery', {'plateList': [plate]}))

    def add_simple_property(self, name, lower=None, upper=None,
                            lower_included=True, upper_included=True, unit=None):
        """简单属性区间筛选 (最新价/市值/换手率等)

        :param name: int, PropertyNameSimple (2201=最新价, 2301=总市值, ...)
        :param lower: float or None, 区间下限 (直接传原始值, OpenD 负责倍率转换)
        :param upper: float or None, 区间上限
        """
        d = {'property': {'name': int(name)}}
        if lower is not None:
            d['filterMin'] = {'value': float(lower), 'includes': bool(lower_included)}
        if upper is not None:
            d['filterMax'] = {'value': float(upper), 'includes': bool(upper_included)}
        if unit is not None:
            d['unit'] = int(unit)
        self._queries.append(('simplePropertyQuery', d))

    def add_cumulative_property(self, name, days=1, lower=None, upper=None,
                                lower_included=True, upper_included=True,
                                continuous_period=None, unit=None):
        """累计属性区间筛选 (涨跌额/涨跌幅等)

        :param name: int, PropertyNameCumulative (3101=涨跌额, 3102=涨跌幅, ...)
        :param days: int, 天数 (默认1)
        :param lower: float or None, 区间下限 (直接传原始值, OpenD 负责倍率转换)
        :param upper: float or None, 区间上限
        """
        d = {'property': {'name': int(name), 'days': int(days)}}
        if lower is not None:
            d['filterMin'] = {'value': float(lower), 'includes': bool(lower_included)}
        if upper is not None:
            d['filterMax'] = {'value': float(upper), 'includes': bool(upper_included)}
        if continuous_period is not None:
            d['continuousPeriod'] = int(continuous_period)
        if unit is not None:
            d['unit'] = int(unit)
        self._queries.append(('cumulativePropertyQuery', d))

    def add_financial_property(self, name, term=None, year=None,
                               lower=None, upper=None,
                               lower_included=True, upper_included=True,
                               duration=None, continuous_period=None,
                               period_average=None, future_duration=None, unit=None):
        """财务属性区间筛选 (净利润/PE/ROE等)

        :param name: int, PropertyNameFinancial (4101=净利润, 4102=净利润增长率, ...)
        :param term: int, 报告期 (1=Q1, 2=Q2, 100=年报, 10=最新单季, ...)
        :param year: int, 年份 (2024/2023/...)
        :param lower: float or None, 区间下限 (直接传原始值, OpenD 负责倍率转换)
        :param upper: float or None, 区间上限
        """
        prop = {'name': int(name)}
        if term is not None:
            prop['term'] = int(term)
        if year is not None:
            prop['year'] = int(year)
        if duration is not None:
            prop['duration'] = int(duration)
        if period_average is not None:
            prop['periodAverage'] = int(period_average)
        if future_duration is not None:
            prop['futureDuration'] = int(future_duration)
        d = {'property': prop}
        if lower is not None:
            d['filterMin'] = {'value': float(lower), 'includes': bool(lower_included)}
        if upper is not None:
            d['filterMax'] = {'value': float(upper), 'includes': bool(upper_included)}
        if continuous_period is not None:
            d['continuousPeriod'] = int(continuous_period)
        if unit is not None:
            d['unit'] = int(unit)
        self._queries.append(('financialPropertyQuery', d))

    def add_indicator_positional(self, first_indicator_name, period_type,
                                 position, second_indicator=None,
                                 second_value=None,
                                 first_indicator_params=None,
                                 second_indicator_params=None,
                                 continuous_period=None, intervals=None):
        """指标位置关系筛选 (MA5 上穿 MA10 等)

        :param first_indicator_name: int, Indicator 枚举 (1=最新价, 11=MA5, ...)
        :param period_type: int, Period 枚举 (1=1分, 11=日, 21=周, ...)
        :param position: int, Position (1=上方, 2=下方, 3=上穿, 4=下穿)
        """
        d = {
            'firstIndicatorName': int(first_indicator_name),
            'periodType': int(period_type),
            'position': int(position),
            'period': int(period_type),
            'firstIndicator': int(first_indicator_name),
        }
        if second_indicator is not None:
            d['secondIndicator'] = int(second_indicator)
        if second_value is not None:
            d['secondValue'] = int(second_value)
        if first_indicator_params is not None:
            d['firstIndicatorParams'] = [int(p) for p in first_indicator_params]
        if second_indicator_params is not None:
            d['secondIndicatorParams'] = [int(p) for p in second_indicator_params]
        if continuous_period is not None:
            d['continuousPeriod'] = int(continuous_period)
        if intervals is not None:
            d['intervals'] = intervals
        self._queries.append(('indicatorPositionalQuery', d))

    def add_indicator_pattern(self, name, period_type,
                              continuous_period=None, is_matching=None,
                              sub_patterns=None):
        """指标形态筛选 (金叉/死叉等)

        :param name: int, Pattern 枚举
        :param period_type: int, Period 枚举
        """
        d = {
            'name': int(name),
            'periodType': int(period_type),
            'period': int(period_type),
        }
        if continuous_period is not None:
            d['continuousPeriod'] = int(continuous_period)
        if is_matching is not None:
            d['isMatching'] = bool(is_matching)
        if sub_patterns is not None:
            d['subPatterns'] = [int(p) for p in sub_patterns]
        self._queries.append(('indicatorPatternQuery', d))

    def add_featured_property(self, name, intervals=None, value_set=None,
                              period=None, range_period=None,
                              first_custom_param=None):
        """特色属性筛选 (筹码获利比例/指标解读等)

        :param name: int, Featured 枚举 (5101=筹码获利比例, 5201=指标解读, ...)
        :param intervals: list of dict, 区间列表 [{'lower': {'value':v,'includes':b}, 'upper':...}, ...]
        :param value_set: list of int, 值集合
        """
        prop = {'name': int(name)}
        if period is not None:
            prop['period'] = int(period)
        if range_period is not None:
            prop['rangePeriod'] = int(range_period)
        if first_custom_param is not None:
            prop['firstCustomParam'] = int(first_custom_param)
        d = {'property': prop}
        if intervals is not None:
            d['intervals'] = intervals
        if value_set is not None:
            d['valueSet'] = [int(v) for v in value_set]
        self._queries.append(('featuredPropertyQuery', d))

    def add_broker_holdings(self, name, days=None, param=None, intervals=None):
        """经纪人持仓筛选

        :param name: int, Broker 枚举 (6101=集中度, 6102=变动, 6103=数量, ...)
        :param days: int, 近n日
        :param param: str, 参数 (broker_id 等)
        :param intervals: list of dict, 区间列表
        """
        prop = {'name': int(name)}
        if days is not None:
            prop['days'] = int(days)
        if param is not None:
            prop['param'] = str(param)
        d = {'property': prop}
        if intervals is not None:
            d['intervals'] = intervals
        self._queries.append(('brokerHoldingsQuery', d))

    def add_kline_shape(self, name, period=None, value_set=None):
        """K 线形态筛选

        :param name: int, KlineShape 枚举 (6200=形态, ...)
        :param period: int, K线周期
        :param value_set: list of int, K线形态类型集合
        """
        prop = {'name': int(name)}
        if period is not None:
            prop['period'] = int(period)
        d = {'property': prop}
        if value_set is not None:
            d['valueSet'] = [int(v) for v in value_set]
        self._queries.append(('klineShapeQuery', d))

    def add_option(self, name, intervals=None, param=None, period=None):
        """期权属性筛选

        :param name: int, Option 枚举 (1000=正股IV, 1001=IV排名, ...)
        :param intervals: list of dict, 区间列表
        """
        prop = {'name': int(name)}
        if period is not None:
            prop['period'] = int(period)
        d = {'property': prop}
        if param is not None:
            d['property']['param'] = param
        if intervals is not None:
            d['intervals'] = intervals
        self._queries.append(('optionQuery', d))

    # ---------- 取回属性 (RetrieveQuery) ----------

    def add_retrieve_basic(self, name):
        """取回基础属性 (代码/名称/行业)"""
        self._retrieves.append(('basicProperty', {'name': int(name)}))

    def add_retrieve_simple(self, name):
        """取回简单属性"""
        self._retrieves.append(('simpleProperty', {'name': int(name)}))

    def add_retrieve_cumulative(self, name, days=1, period_average=None):
        """取回累计属性"""
        d = {'name': int(name), 'days': int(days)}
        if period_average is not None:
            d['periodAverage'] = int(period_average)
        self._retrieves.append(('cumulativeProperty', d))

    def add_retrieve_financial(self, name, term=None, year=None,
                               duration=None, period_average=None,
                               future_duration=None):
        """取回财务属性"""
        d = {'name': int(name)}
        if term is not None:
            d['term'] = int(term)
        if year is not None:
            d['year'] = int(year)
        if duration is not None:
            d['duration'] = int(duration)
        if period_average is not None:
            d['periodAverage'] = int(period_average)
        if future_duration is not None:
            d['futureDuration'] = int(future_duration)
        self._retrieves.append(('financialProperty', d))

    def add_retrieve_indicator(self, name, period=None, indicator_params=None):
        """取回指标属性"""
        d = {'name': int(name)}
        if period is not None:
            d['period'] = int(period)
        if indicator_params is not None:
            d['indicatorParams'] = [int(p) for p in indicator_params]
        self._retrieves.append(('indicatorProperty', d))

    def add_retrieve_featured(self, name, period=None, range_period=None,
                              first_custom_param=None):
        """取回特色属性"""
        d = {'name': int(name)}
        if period is not None:
            d['period'] = int(period)
        if range_period is not None:
            d['rangePeriod'] = int(range_period)
        if first_custom_param is not None:
            d['firstCustomParam'] = int(first_custom_param)
        self._retrieves.append(('featuredProperty', d))

    def add_retrieve_broker(self, name, days=None, param=None):
        """取回经纪人属性"""
        d = {'name': int(name)}
        if days is not None:
            d['days'] = int(days)
        if param is not None:
            d['param'] = str(param)
        self._retrieves.append(('brokerProperty', d))

    def add_retrieve_option(self, name, param=None, period=None):
        """取回期权属性"""
        d = {'name': int(name)}
        if period is not None:
            d['period'] = int(period)
        self._retrieves.append(('optionProperty', d))

    def add_retrieve_kline_shape(self, name, period=None):
        """取回K线形态属性

        :param name: KlineShapeProperty 枚举, 如 SHAPE_TYPE=6200
        :param period: K线周期 (KLType), 必传, 否则后端不返回结果。
                       目前仅支持 11 (日K) 和 21 (1小时K)。
        """
        d = {'name': int(name)}
        if period is not None:
            d['period'] = int(period)
        self._retrieves.append(('klineShapeProperty', d))

    # ---------- 排序 ----------

    def set_sort(self, direction, property_type, property_params):
        """设置单字段排序

        :param direction: int, 1=升序, 2=降序, 3=绝对值升序, 4=绝对值降序
        :param property_type: str, 属性类型 ('simple'/'cumulative'/'financial'/...)
        :param property_params: dict, 属性参数 (如 {'name': 2201})
        """
        self._sort = (int(direction), str(property_type), property_params)

    def add_sort(self, direction, property_type, property_params):
        """添加多字段排序 (有值时优先于 set_sort)"""
        self._sorts.append((int(direction), str(property_type), property_params))


class StockScreenQuery:
    """条件选股V2 内部 Query 处理类 (ProtoID 3252)"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, request, conn_id):
        from ..common.pb import Qot_StockScreen_pb2
        req = Qot_StockScreen_pb2.Request()
        c2s = req.c2s

        c2s.pageFrom = int(request.page_from)
        c2s.pageCount = int(request.page_count)

        # filterList (proto field: filterList)
        for q_type, q_params in request._queries:
            sq = c2s.filterList.add()
            sub_pb = getattr(sq, q_type)
            _dict_to_pb(q_params, sub_pb)

        # retrieveList (proto field: retrieveList)
        for r_type, r_params in request._retrieves:
            rq = c2s.retrieveList.add()
            sub_pb = getattr(rq, r_type)
            _dict_to_pb(r_params, sub_pb)

        # sort (单字段)
        if request._sort is not None:
            direction, prop_type, prop_params = request._sort
            c2s.sort.direction = direction
            _SORT_TYPE_MAP = {
                'basic': 'basicProperty', 'simple': 'simpleProperty',
                'cumulative': 'cumulativeProperty', 'financial': 'financialProperty',
                'indicator': 'indicatorProperty', 'featured': 'featuredProperty',
                'broker': 'brokerProperty', 'option': 'optionProperty',
                'kline_shape': 'klineShapeProperty',
            }
            pb_field = _SORT_TYPE_MAP.get(prop_type)
            if pb_field is not None:
                _dict_to_pb(prop_params, getattr(c2s.sort, pb_field))

        # sortList (多字段)
        for direction, prop_type, prop_params in request._sorts:
            s_pb = c2s.sortList.add()
            s_pb.direction = direction
            _SORT_TYPE_MAP = {
                'basic': 'basicProperty', 'simple': 'simpleProperty',
                'cumulative': 'cumulativeProperty', 'financial': 'financialProperty',
                'indicator': 'indicatorProperty', 'featured': 'featuredProperty',
                'broker': 'brokerProperty', 'option': 'optionProperty',
                'kline_shape': 'klineShapeProperty',
            }
            pb_field = _SORT_TYPE_MAP.get(prop_type)
            if pb_field is not None:
                _dict_to_pb(prop_params, getattr(s_pb, pb_field))

        return pack_pb_req(req, ProtoId.Qot_StockScreen, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        last_page = s2c.lastPage if s2c.HasField('lastPage') else True
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.dataList:
            data = {
                'stock_id': item.stockId if item.HasField('stockId') else 0,
                'results': [],
            }
            for res_item in item.results:
                result_data = cls._parse_rsp_item_result(res_item)
                if result_data is not None:
                    data['results'].append(result_data)
            ret_list.append(data)
        return RET_OK, "", (last_page, all_count, ret_list)

    @staticmethod
    def _parse_rsp_item_result(res_item):
        """解析 RspItemResult，返回 dict

        新结构: 每个 ResultPropertyXxx 含 property + 扁平 valueType/sval/ival/aval/dval
        valueType: 1=string(sval), 2=int64(ival), 3=int64数组(aval), 4=double(dval)
        """
        result_type_map = [
            ('basicPropertyResult', 'basic'),
            ('simplePropertyResult', 'simple'),
            ('cumulativePropertyResult', 'cumulative'),
            ('financialPropertyResult', 'financial'),
            ('indicatorPropertyResult', 'indicator'),
            ('featuredPropertyResult', 'featured'),
            ('brokerPropertyResult', 'broker'),
            ('optionPropertyResult', 'option'),
            ('klineShapePropertyResult', 'kline_shape'),
        ]
        for pb_field, type_name in result_type_map:
            if res_item.HasField(pb_field):
                sub = getattr(res_item, pb_field)
                d = {'type': type_name}

                # property
                if sub.HasField('property'):
                    prop = sub.property
                    prop_dict = {}
                    for field in prop.DESCRIPTOR.fields:
                        if field.label == field.LABEL_REPEATED:
                            val = getattr(prop, field.name)
                            if len(val) > 0:
                                prop_dict[field.name] = list(val)
                        elif prop.HasField(field.name):
                            prop_dict[field.name] = getattr(prop, field.name)
                    d['property'] = prop_dict

                # 扁平值字段
                if sub.HasField('valueType'):
                    d['value_type'] = sub.valueType
                if sub.HasField('sval'):
                    d['sval'] = sub.sval
                if sub.HasField('ival'):
                    d['ival'] = sub.ival
                if len(sub.aval) > 0:
                    d['aval'] = list(sub.aval)
                if sub.HasField('dval'):
                    d['dval'] = sub.dval

                # Financial 专有字段
                if type_name == 'financial' and sub.HasField('endTime'):
                    d['end_time'] = sub.endTime

                # 枚举字段: OpenD 在 ival 是枚举码时下发
                #   enumTypeName: SDK 侧枚举类名 (如 KlineShapeType)
                #   enumName:     OpenD 已通过 protobuf 反射解出的可读名 (如 DOUBLE_PEAKS)
                # 优先采用 OpenD 下发的 enumName; 若旧版 OpenD 未下发, 再用本地枚举 fallback 解码
                if sub.HasField('enumTypeName') and sub.enumTypeName:
                    d['enum_type_name'] = sub.enumTypeName
                if sub.HasField('enumName') and sub.enumName:
                    d['enum_name'] = sub.enumName
                elif 'enum_type_name' in d and 'ival' in d:
                    try:
                        from . import stock_screen_const as _sc
                        enum_cls = getattr(_sc, d['enum_type_name'], None)
                        if enum_cls is not None:
                            d['enum_name'] = enum_cls(d['ival']).name
                    except (ValueError, AttributeError, ImportError):
                        pass

                return d
        return None


# =================== dict → protobuf 通用转换 (内部使用) ===================

def _dict_to_pb(d, pb_msg):
    """将 dict 递归填充到 protobuf message"""
    if d is None:
        return
    for key, value in d.items():
        field_desc = pb_msg.DESCRIPTOR.fields_by_name.get(key)
        if field_desc is None:
            continue
        if value is None:
            continue
        if field_desc.message_type:
            if field_desc.label == field_desc.LABEL_REPEATED:
                for item in value:
                    sub = getattr(pb_msg, key).add()
                    _dict_to_pb(item, sub)
            else:
                _dict_to_pb(value, getattr(pb_msg, key))
        else:
            if field_desc.label == field_desc.LABEL_REPEATED:
                getattr(pb_msg, key).extend(value)
            else:
                setattr(pb_msg, key, value)


# =================== WarrantScreen (3254) — Builder 类 ===================


class WarrantScreenRequest(object):
    """窝轮筛选V2 请求构建器 (ProtoID 3254)

    用法::

        from futu import WarrantScreenRequest, WarrantMarket

        req = WarrantScreenRequest(warrant_market=WarrantMarket.HK)
        req.add_interval_filter(field_id=21, min_val=0.1, max_val=5.0)  # 最新价, 直接传 float
        req.add_choice_filter(field_id=6, choices=[1, 2])
        req.add_sort(field_id=23, desc=True)
        req.page_count = 50
    """

    def __init__(self, warrant_market):
        """
        :param warrant_market: WarrantMarket 枚举 (HK=1, SG=4, MY=15)
        """
        from .stock_screen_const import WarrantMarket
        try:
            WarrantMarket(int(warrant_market))
        except ValueError:
            raise ValueError(
                f"warrant_market must be a WarrantMarket enum (HK/SG/MY), got {warrant_market!r}"
            )
        self.warrant_market = int(warrant_market)
        self.is_delay = False
        self.only_count = False
        self.page_from = 0
        self.page_count = 200
        self._filters = []
        self._sorts = []

    def add_interval_filter(self, field_id, min_val=None, max_val=None,
                            min_included=True, max_included=True):
        """添加区间筛选

        :param field_id: int, FieldId 枚举 (8=最新价, 28=街货占比, ...)
        :param min_val: float or None, 下限 (直接传原始值, OpenD 负责倍率转换)
        :param max_val: float or None, 上限
        """
        self._filters.append({
            'type': 'interval', 'field_id': int(field_id),
            'min_val': min_val, 'max_val': max_val,
            'min_included': min_included, 'max_included': max_included,
        })

    # WarrantStatus 字符串枚举 (futu.common.constant) → V2 紧凑 int 映射；
    # 兼容老用户直接传 ``WarrantStatus.NORMAL`` 等枚举值
    _STATUS_STR_TO_INT = {
        'NORMAL': 0,
        'STOP_TRADE': 1,
        'PENDING_LISTING': 2,
    }
    _FIELD_CODE = 1     # WarrantField.CODE
    _FIELD_STATUS = 19  # WarrantField.STATUS

    def add_choice_filter(self, field_id, choices):
        """添加多选筛选

        :param field_id: int, FieldId 枚举 (4=发行人, 6=类型, ...)
        :param choices: list, 选项列表 (int 或 str)

        特殊字段:
            CODE (1) 证券代码: 推荐传带市场前缀的 code 字符串, 例如
                ``choices=["HK.57161"]``. SDK 会自动剥离前缀传给 OpenD.
                也兼容传纯数字 code 字符串 ("57161")。
            STOCK_OWNER (5) 正股过滤: 推荐直接传 code 字符串, 例如
                ``choices=["HK.00700"]``. OpenD 会自动翻译成对应 stock_id.
                也兼容传数值 stock_id (int).
            STATUS (19) 窝轮状态: 可传 ``stock_screen_const.WarrantStatus`` 的 IntEnum,
                也兼容传 ``common.constant.WarrantStatus`` 的字符串枚举
                ("NORMAL" / "STOP_TRADE" / "PENDING_LISTING")。
        """
        fid = int(field_id)
        norm_choices = []
        for c in choices:
            if fid == self._FIELD_STATUS and isinstance(c, str) and c in self._STATUS_STR_TO_INT:
                norm_choices.append(self._STATUS_STR_TO_INT[c])
            elif fid == self._FIELD_CODE and isinstance(c, str) and '.' in c:
                # 兼容传入带市场前缀的 code (如 "HK.57161")，OpenD 内部按纯数字精确匹配
                norm_choices.append(c.split('.', 1)[1])
            else:
                norm_choices.append(c)
        self._filters.append({
            'type': 'choice', 'field_id': fid,
            'choices': norm_choices,
        })

    def add_sort(self, field_id, desc=False):
        """添加排序

        :param field_id: int, FieldId 枚举
        :param desc: bool, True=降序, False=升序
        """
        self._sorts.append({'field_id': int(field_id), 'desc': bool(desc)})


# WarrantItem 字段映射: (python_name, proto_name)
# 注: 倍率转换已移至 OpenD 层, SDK 直接读取 double 值
_WARRANT_FIELD_MAP = [
    ('issuer_id', 'issuerId'), ('warrant_type', 'warrantType'),
    ('strike_price', 'strikePrice'), ('maturity_date', 'maturityDate'),
    ('last_trade_date', 'lastTradeDate'), ('conversion_ratio', 'conversionRatio'),
    ('last_close_price', 'lastclosePrice'), ('recovery_price', 'recoveryPrice'),
    ('stock_owner_price', 'stockOwnerPrice'), ('current_price', 'currentPrice'),
    ('volume', 'volume'), ('turnover', 'turnover'),
    ('sell_vol', 'sellVol'), ('buy_vol', 'buyVol'),
    ('sell_price', 'sellPrice'), ('buy_price', 'buyPrice'),
    ('street_rate', 'streetRate'), ('high_price', 'highPrice'),
    ('low_price', 'lowPrice'), ('implied_volatility', 'impliedVolatility'),
    ('delta', 'delta'), ('status', 'status'),
    ('street_rate_new', 'streetRateNew'), ('score', 'score'),
    ('premium', 'premium'), ('leverage', 'leverage'),
    ('effective_leverage', 'effectiveLeverage'), ('break_even_point', 'breakEvenPoint'),
    ('ipop', 'ipop'), ('amplitude', 'amplitude'),
    ('fx_score', 'fxScore'), ('ipo_time', 'ipoTime'),
    ('street_vol', 'streetVol'), ('lot_size', 'lotSize'),
    ('issue_size', 'issueSize'), ('ipo_price', 'ipoPrice'),
    ('upper_strike_price', 'upperStrikePrice'), ('lower_strike_price', 'lowerStrikePrice'),
    ('iw_price_status', 'iwPriceStatus'), ('sensitivity', 'sensitivity'),
    ('price_recovery_ratio', 'priceRecoveryRatio'),
]


class WarrantScreenQuery:
    """窝轮筛选V2 内部 Query 处理类 (ProtoID 3227)"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, request, conn_id):
        from ..common.pb import Qot_WarrantScreen_pb2
        req = Qot_WarrantScreen_pb2.Request()
        c2s = req.c2s

        c2s.marketType = request.warrant_market
        if request.is_delay:
            c2s.isDelay = True
        if request.only_count:
            c2s.onlyCount = True
        c2s.pageFrom = int(request.page_from)
        c2s.pageCount = int(request.page_count)

        for f in request._filters:
            sg = c2s.filterList.add()
            sg.fieldId = f['field_id']
            if f['type'] == 'interval':
                if f.get('min_val') is not None:
                    sg.interval.filterMin.value = float(f['min_val'])
                    sg.interval.filterMin.includes = f.get('min_included', True)
                if f.get('max_val') is not None:
                    sg.interval.filterMax.value = float(f['max_val'])
                    sg.interval.filterMax.includes = f.get('max_included', True)
            elif f['type'] == 'choice':
                for c_val in f['choices']:
                    choice = sg.choices.add()
                    if isinstance(c_val, str):
                        choice.contentType = 2
                        choice.text = c_val
                    else:
                        choice.contentType = 1
                        choice.value = int(c_val)

        for s in request._sorts:
            sort_pb = c2s.sortList.add()
            sort_pb.sortFieldId = s['field_id']
            sort_pb.direction = 1 if s['desc'] else 0

        return pack_pb_req(req, ProtoId.Qot_WarrantScreen, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        last_page = s2c.lastPage if s2c.HasField('lastPage') else True
        all_count = s2c.allCount if s2c.HasField('allCount') else 0

        ret_list = []
        for item in s2c.warrants:
            data = cls._parse_warrant_item(item)
            ret_list.append(data)
        return RET_OK, "", (last_page, all_count, ret_list)

    @staticmethod
    def _parse_warrant_item(item):
        """解析 WarrantItem, OpenD 已处理倍率转换, 直接读取值"""
        data = {}
        for py_name, pb_name in _WARRANT_FIELD_MAP:
            if item.HasField(pb_name):
                data[py_name] = getattr(item, pb_name)
            else:
                data[py_name] = NoneDataType

        # OpenD 反查后下发的 code/name, 避免客户端再用 stock_id hash 反查
        if item.HasField('security'):
            sec = item.security
            data['code'] = merge_qot_mkt_stock_str(sec.market, sec.code)
        else:
            data['code'] = NoneDataType
        if item.HasField('ownerSecurity'):
            owner = item.ownerSecurity
            data['owner_code'] = merge_qot_mkt_stock_str(owner.market, owner.code)
        else:
            data['owner_code'] = NoneDataType
        data['name'] = item.name if item.HasField('name') else NoneDataType
        data['owner_name'] = item.ownerName if item.HasField('ownerName') else NoneDataType

        return data


# ============================================================
#  OptionScreen (ProtoID 3253) — 期权选股
# ============================================================

# OptUnderlyingIndicator 分类 (来自 Qot_OptionScreen.proto 注释)
# 枚举型: 必须传 values, 不接受 lower/upper
_OPT_UNDERLYING_DISCRETE = frozenset((101, 106))  # STOCK_LIST / INDEX_LIST
# 范围型: 必须传 lower 或 upper, 不接受 values
_OPT_UNDERLYING_RANGE = frozenset((
    201, 202,                         # Volume / OpenInterest
    203, 204, 205, 206, 207, 208, 209, 210,  # IV / HV / Rank / Percentile / 变化系列 / HVRatio / HVSpread
    401, 402, 403,                    # MarketCap / StockPrice / ChangeRatio
))

# OptIndicator 分类
# 枚举型: 必须传 values
_OPT_OPTION_DISCRETE = frozenset((
    1003, 1004, 1005, 1007,           # OptionType / ExerciseType / ExpirationType / StrikeDateTimestamp
    2001,                             # InTheMoney
))
# 范围型: 必须传 lower 或 upper
_OPT_OPTION_RANGE = frozenset((
    1001, 1002,                       # StrikePrice / LeftDay
    2002, 2003, 2004, 2005, 2006,     # Price / MidPrice / BidPrice / AskPrice / BidAskSpread
    2007, 2008, 2009, 2010,           # BidVolume / AskVolume / BidAskVolumeRatio / ChangeRatio
    2011, 2012, 2013, 2014,           # Volume / Turnover / OpenInterest / OpenInterestMarketCap
    2018, 2021,                       # VolOIRatio / Premium (filter 已入口拦截)
    3001, 3002, 3003,                 # IV / HV / IV_HV_Ratio
    3004, 3005, 3006, 3007, 3008,     # Delta / Gamma / Vega / Theta / Rho
    3009, 3010,                       # LeverageRatio / EffectiveGearing
    3011, 3012,                       # BuyToBep / SellToBep
    3013, 3014,                       # BuyProfitProbability / SellProfitProbability
    3015, 3016,                       # IntrinsicValuePer / TimeValuePer
    3017, 3018,                       # ITMDegree / OTMDegree
    3019, 3020,                       # ITMProbability / OTMProbability
    3021, 3022,                       # SellAnnualizedReturn / IntervalReturn
))


class OptionScreenRequest(object):
    """期权选股 请求构建器 (ProtoID 3253)

    值字段使用 float/double, OpenD 负责与后端 int64 倍率互转。

    筛选语义: 多次 add_*_filter 默认按 AND 拼接 (自动拆组), 同一 indicator_type 多次
    取值的 OR 场景使用 or_with_previous=True 显式声明。

    用法::

        from futu import OptionScreenRequest, OptMarketCategory, OptIndicator, OptUnderlyingIndicator

        req = OptionScreenRequest(market_categories=[OptMarketCategory.US_STOCK])
        # 以下三个条件按 AND 组合 (SDK 自动开组)
        req.add_underlying_filter(OptUnderlyingIndicator.IV, lower=30.0)
        req.add_option_filter(OptIndicator.OPTION_TYPE, values=[1])  # CALL
        req.add_option_filter(OptIndicator.DELTA, lower=0.3, upper=0.7)
        req.add_sort(OptIndicator.VOLUME, desc=True)
        req.page_count = 50
    """

    def __init__(self, market_categories):
        """
        :param market_categories: list of int, 期权市场品类列表 (OptMarketCategory 枚举)
        """
        if not market_categories:
            raise ValueError("market_categories must not be empty")
        self.market_categories = [int(m) for m in market_categories]
        self.page_from = 0
        self.page_count = 200
        self._current_group = {'underlying': [], 'option': []}
        self._filter_groups = [self._current_group]
        self._sorts = []
        self._option_retrieves = []      # list of int (OptIndicator)
        self._underlying_retrieves = []  # list of int (OptUnderlyingIndicator)

    def add_underlying_filter(self, indicator_type, values=None,
                              lower=None, upper=None,
                              lower_included=True, upper_included=True,
                              plate_list=None, parent_plate_id=None,
                              or_with_previous=False):
        """添加标的筛选条件 (默认与之前条件 AND)

        :param indicator_type: int, OptUnderlyingIndicator 枚举
        :param values: 确切值列表, 二选一传一种 (不允许 int / str 混传):
            - list of int: OpenD 内部 stockID
            - list of str: 标的代码 (仅 STOCK_LIST(101) / INDEX_LIST(106) 支持,
              如 ["US.AAPL","HK.00700"]), OpenD 收到后翻译成 stockID
        :param lower: float or None, 区间下限 (直接传原始值, OpenD 负责倍率转换)
        :param upper: float or None, 区间上限
        :param plate_list: list of str, 板块代码列表 (仅PLATE类型, 如 ["BK1001","BK1002"])
        :param parent_plate_id: str or None, 父板块代码 (仅PLATE类型, 如 "BK1000")
        :param or_with_previous: bool, True=与当前组上一条件做 OR (要求同 indicator_type),
            默认 False=与之前条件 AND, 自动开新组
        """
        ind_type = int(indicator_type)
        # values 类型分流: 全 int 走 value_list (stockID), 全 str 走 code_list ("US.AAPL"), 不允许混传
        value_list = None
        code_list = None
        if values is not None:
            seq = list(values)
            if len(seq) > 0:
                has_str = any(isinstance(v, str) for v in seq)
                has_num = any(not isinstance(v, str) for v in seq)
                if has_str and has_num:
                    raise ValueError(
                        "add_underlying_filter: 'values' cannot mix str and int (got both)")
                if has_str:
                    if ind_type not in (101, 106):
                        raise ValueError(
                            "add_underlying_filter: str values only supported for STOCK_LIST(101) / INDEX_LIST(106), got %d" % ind_type)
                    code_list = [str(c) for c in seq]
                else:
                    value_list = [int(v) for v in seq]
        # 后端禁止同组混 underlying + option, 必须开新组保持 AND 语义
        # 不同 indicator_type 之间默认 AND, 也开新组; 仅同 indicator_type 且显式 or_with_previous 才 OR
        if self._current_group['option']:
            self.new_filter_group()
        elif self._current_group['underlying']:
            same_type = all(
                ind['indicator_type'] == ind_type
                for ind in self._current_group['underlying']
            )
            if not (or_with_previous and same_type):
                self.new_filter_group()
        # 按 indicator 类型强校验 入参形态
        has_values = (value_list is not None or code_list is not None)
        has_interval = (lower is not None or upper is not None)
        has_plate = (plate_list is not None)
        if ind_type in _OPT_UNDERLYING_RANGE:
            if has_values:
                raise ValueError(
                    "add_underlying_filter: indicator=%d is a range filter, use lower/upper instead of values"
                    % ind_type)
            if not has_interval:
                raise ValueError(
                    "add_underlying_filter: indicator=%d is a range filter, requires lower and/or upper"
                    % ind_type)
        elif ind_type in _OPT_UNDERLYING_DISCRETE:
            if has_interval:
                raise ValueError(
                    "add_underlying_filter: indicator=%d is a discrete filter, use values instead of lower/upper"
                    % ind_type)
            if not has_values:
                raise ValueError(
                    "add_underlying_filter: indicator=%d is a discrete filter, requires values"
                    % ind_type)
        elif ind_type == 103:
            if not has_plate:
                raise ValueError("add_underlying_filter: PLATE(103) requires plate_list")
        else:
            # 未知 indicator: 至少要有一种筛选条件, 真正的合法性交给 OpenD 拦截
            if not has_values and not has_interval and not has_plate:
                raise ValueError(
                    "add_underlying_filter: indicator=%d requires at least one of values/lower/upper/plate_list"
                    % ind_type)
        indicator = {'indicator_type': ind_type}
        if value_list is not None:
            indicator['value_list'] = value_list
        if code_list is not None:
            indicator['code_list'] = code_list
        if lower is not None or upper is not None:
            interval = {}
            if lower is not None:
                interval['lower'] = {'value': float(lower), 'includes': bool(lower_included)}
            if upper is not None:
                interval['upper'] = {'value': float(upper), 'includes': bool(upper_included)}
            indicator['interval'] = interval
        if plate_list is not None:
            plate = {'plateIdList': [str(pid) for pid in plate_list]}
            if parent_plate_id is not None:
                plate['parentPlateId'] = str(parent_plate_id)
            indicator['plate_list'] = [plate]
        self._current_group['underlying'].append(indicator)

    def add_option_filter(self, indicator_type, values=None,
                          lower=None, upper=None,
                          lower_included=True, upper_included=True,
                          or_with_previous=False):
        """添加期权筛选条件 (默认与之前条件 AND)

        :param indicator_type: int, OptIndicator 枚举
        :param values: list of int, 确切值列表 (用于 OPTION_TYPE/EXERCISE_TYPE 等)
        :param lower: float or None, 区间下限 (直接传原始值, OpenD 负责倍率转换)
        :param upper: float or None, 区间上限
        :param or_with_previous: bool, True=与当前组上一条件做 OR (要求同 indicator_type),
            默认 False=与之前条件 AND, 自动开新组
        """
        ind_type = int(indicator_type)
        # 按 indicator 类型强校验 入参形态
        has_values = (values is not None)
        has_interval = (lower is not None or upper is not None)
        if ind_type in _OPT_OPTION_RANGE:
            if has_values:
                raise ValueError(
                    "add_option_filter: indicator=%d is a range filter, use lower/upper instead of values"
                    % ind_type)
            if not has_interval:
                raise ValueError(
                    "add_option_filter: indicator=%d is a range filter, requires lower and/or upper"
                    % ind_type)
        elif ind_type in _OPT_OPTION_DISCRETE:
            if has_interval:
                raise ValueError(
                    "add_option_filter: indicator=%d is a discrete filter, use values instead of lower/upper"
                    % ind_type)
            if not has_values:
                raise ValueError(
                    "add_option_filter: indicator=%d is a discrete filter, requires values"
                    % ind_type)
        else:
            # 未知 indicator: 至少要有一种筛选条件, 真正的合法性交给 OpenD 拦截
            if not has_values and not has_interval:
                raise ValueError(
                    "add_option_filter: indicator=%d requires at least one of values/lower/upper"
                    % ind_type)
        value_list = None
        if values is not None:
            seq = list(values)
            if len(seq) == 0:
                raise ValueError(
                    "add_option_filter: 'values' must not be empty (indicator=%d)" % ind_type)
            value_list = [int(v) for v in seq]
        # 后端禁止同组混 underlying + option, 必须开新组保持 AND 语义
        # 不同 indicator_type 之间默认 AND, 也开新组; 仅同 indicator_type 且显式 or_with_previous 才 OR
        if self._current_group['underlying']:
            self.new_filter_group()
        elif self._current_group['option']:
            same_type = all(
                ind['indicator_type'] == ind_type
                for ind in self._current_group['option']
            )
            if not (or_with_previous and same_type):
                self.new_filter_group()
        indicator = {'indicator_type': ind_type}
        if value_list is not None:
            indicator['value_list'] = value_list
        if lower is not None or upper is not None:
            interval = {}
            if lower is not None:
                interval['lower'] = {'value': float(lower), 'includes': bool(lower_included)}
            if upper is not None:
                interval['upper'] = {'value': float(upper), 'includes': bool(upper_included)}
            indicator['interval'] = interval
        self._current_group['option'].append(indicator)

    def new_filter_group(self):
        """开始新的筛选组 (组间 AND, 组内 OR)"""
        self._current_group = {'underlying': [], 'option': []}
        self._filter_groups.append(self._current_group)

    def add_sort(self, indicator_type, desc=False):
        """添加排序

        :param indicator_type: int, OptIndicator 枚举 (排序字段)
        :param desc: bool, True=降序, False=升序
        """
        self._sorts.append({
            'indicator_type': int(indicator_type),
            'direction': 1 if desc else 0,
        })

    def add_option_retrieve(self, indicator_type):
        """声明要返回的期权字段 (OptIndicator 枚举)。未调用时返回默认基础字段集。

        code/option_name/strike_date 始终返回，无需声明。
        """
        self._option_retrieves.append(int(indicator_type))

    def add_underlying_retrieve(self, indicator_type):
        """声明要返回的标的字段 (OptUnderlyingIndicator 枚举)。调用后返回 underlying_info。

        支持的值: IV(203)/HV(204)/IVRank(205)/IVPercentile(206)/MarketCap(401)/StockPrice(402)/ChangeRate(403)
        """
        self._underlying_retrieves.append(int(indicator_type))


# OptionScreenItem 字段映射: (python_name, proto_name)
# 注: 倍率转换已移至 OpenD 层, SDK 直接读取 double 值
_OPTION_SCREEN_FIELD_MAP = [
    # 基本信息
    ('option_name', 'optionName'),
    ('strike_price', 'strikePrice'),
    ('strike_date', 'strikeDate'),
    ('option_type', 'optionType'),
    ('exercise_type', 'exerciseType'),
    ('expiration_type', 'expirationType'),
    ('in_the_money', 'inTheMoney'),
    ('left_day', 'leftDay'),
    # 行情
    ('price', 'price'),
    ('mid_price', 'midPrice'),
    ('bid_price', 'bidPrice'),
    ('ask_price', 'askPrice'),
    ('bid_ask_spread', 'bidAskSpread'),
    ('bid_volume', 'bidVolume'),
    ('ask_volume', 'askVolume'),
    ('bid_ask_volume_ratio', 'bidAskVolumeRatio'),
    ('change_ratio', 'changeRate'),
    ('volume', 'volume'),
    ('turnover', 'turnover'),
    ('open_interest', 'openInterest'),
    ('open_interest_market_cap', 'openInterestMarketCap'),
    ('vol_oi_ratio', 'volOIRatio'),
    ('premium', 'premium'),
    # Greeks
    ('implied_volatility', 'impliedVolatility'),
    ('history_volatility', 'historyVolatility'),
    ('iv_hv_ratio', 'ivHvRatio'),
    ('delta', 'delta'),
    ('gamma', 'gamma'),
    ('vega', 'vega'),
    ('theta', 'theta'),
    ('rho', 'rho'),
    ('leverage_ratio', 'leverageRatio'),
    ('effective_gearing', 'effectiveGearing'),
    ('itm_probability', 'itmProbability'),
    # 期权分析指标 (续)
    ('buy_to_bep', 'buyToBep'),
    ('sell_to_bep', 'sellToBep'),
    ('buy_profit_probability', 'buyProfitProbability'),
    ('sell_profit_probability', 'sellProfitProbability'),
    ('intrinsic_value_per', 'intrinsicValuePer'),
    ('time_value_per', 'timeValuePer'),
    ('itm_degree', 'itmDegree'),
    ('otm_degree', 'otmDegree'),
    ('otm_probability', 'otmProbability'),
    ('sell_annualized_return', 'sellAnnualizedReturn'),
    ('interval_return', 'intervalReturn'),
]

# UnderlyingInfo 字段映射
_UNDERLYING_INFO_FIELD_MAP = [
    ('stock_id', 'stockID'),
    ('iv', 'iv'), ('hv', 'hv'),
    ('iv_rank', 'ivRank'), ('iv_percentile', 'ivPercentile'),
    ('market_cap', 'marketCap'), ('price', 'price'),
    ('change_ratio', 'changeRate'),
]


class OptionScreenQuery:
    """期权选股查询处理 (ProtoID 3253)"""

    @classmethod
    def pack_req(cls, request, conn_id):
        from ..common.pb import Qot_OptionScreen_pb2
        req = Qot_OptionScreen_pb2.Request()
        c2s = req.c2s

        # 市场品类
        c2s.marketCategoryList.extend(request.market_categories)

        # 筛选条件组
        for group_data in request._filter_groups:
            underlying_list = group_data.get('underlying', [])
            option_list = group_data.get('option', [])
            if not underlying_list and not option_list:
                continue
            group = c2s.filterList.add()
            for ind_data in underlying_list:
                ind = group.underlyingList.add()
                ind.indicatorType = ind_data['indicator_type']
                # PLATE(103): 使用 plateList 字段
                plate_data_list = ind_data.get('plate_list')
                if plate_data_list is not None:
                    for plate_data in plate_data_list:
                        plate = ind.plateList.add()
                        if 'parentPlateId' in plate_data:
                            plate.parentPlateId = plate_data['parentPlateId']
                        for pid in plate_data.get('plateIdList', []):
                            plate.plateIdList.append(pid)
                else:
                    cls._fill_indicator_value(ind.indicatorValue, ind_data)
            for ind_data in option_list:
                ind = group.optionList.add()
                ind.indicatorType = ind_data['indicator_type']
                cls._fill_indicator_value(ind.indicatorValue, ind_data)

        # 排序
        for sort_data in request._sorts:
            sort = c2s.sortList.add()
            sort.indicatorType = sort_data['indicator_type']
            sort.direction = sort_data['direction']

        # 分页 (始终设置，避免后端使用不同默认值)
        c2s.pageFrom = int(request.page_from)
        c2s.pageCount = int(request.page_count)

        # retrieve (返回字段声明)
        for ind in request._option_retrieves:
            c2s.optionRetrieveList.append(int(ind))
        for ind in request._underlying_retrieves:
            c2s.underlyingRetrieveList.append(int(ind))

        return pack_pb_req(req, ProtoId.Qot_OptionScreen, conn_id)

    @classmethod
    def _fill_indicator_value(cls, pb_value, ind_data):
        """填充 OptionIndicatorValue"""
        value_list = ind_data.get('value_list')
        if value_list is not None:
            pb_value.valueList.extend(value_list)
        code_list = ind_data.get('code_list')
        if code_list is not None:
            pb_value.strValueList.extend(code_list)
        interval = ind_data.get('interval')
        if interval is not None:
            iv = pb_value.valueInterval
            lower = interval.get('lower')
            if lower is not None:
                iv.filterMin.value = lower['value']
                iv.filterMin.includes = lower.get('includes', True)
            upper = interval.get('upper')
            if upper is not None:
                iv.filterMax.value = upper['value']
                iv.filterMax.includes = upper.get('includes', True)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        s2c = rsp_pb.s2c
        last_page = s2c.lastPage
        all_count = s2c.allCount

        ret_list = []
        for item in s2c.dataList:
            data = cls._parse_option_item(item)
            ret_list.append(data)
        return RET_OK, "", (last_page, all_count, ret_list)

    @staticmethod
    def _parse_option_item(item):
        """解析 OptionScreenItem, OpenD 已处理倍率转换, 直接读取值"""
        data = {}

        # security 特殊处理
        if item.HasField('security'):
            sec = item.security
            data['code'] = merge_qot_mkt_stock_str(sec.market, sec.code)
        else:
            data['code'] = NoneDataType

        # 标量字段
        for py_name, pb_name in _OPTION_SCREEN_FIELD_MAP:
            if item.HasField(pb_name):
                data[py_name] = getattr(item, pb_name)
            else:
                data[py_name] = NoneDataType

        # underlyingInfo 嵌套消息
        if item.HasField('underlyingInfo'):
            ui = item.underlyingInfo
            underlying = {}
            for py_name, pb_name in _UNDERLYING_INFO_FIELD_MAP:
                if ui.HasField(pb_name):
                    underlying[py_name] = getattr(ui, pb_name)
                else:
                    underlying[py_name] = NoneDataType
            data['underlying'] = underlying
        else:
            data['underlying'] = NoneDataType

        return data

def _pack_option_strategy_legs(req_legs, option_legs):
    if not isinstance(option_legs, list) or len(option_legs) == 0:
        return RET_ERROR, ERROR_STR_PREFIX + "option_legs must be a non-empty list"

    for leg in option_legs:
        if not isinstance(leg, OptionStrategyLeg):
            return RET_ERROR, ERROR_STR_PREFIX + "each item in option_legs must be OptionStrategyLeg"

        ret, content = split_stock_str(leg.code)
        if ret != RET_OK:
            return RET_ERROR, content
        market_code, stock_code = content

        ret, action = StrategyLegAction.to_number(leg.action)
        if ret is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of action in option_legs is wrong"

        try:
            quantity = float(leg.quantity)
        except (TypeError, ValueError):
            return RET_ERROR, ERROR_STR_PREFIX + "the quantity in option_legs must be numeric"

        req_leg = req_legs.add()
        req_leg.security.market = market_code
        req_leg.security.code = stock_code
        req_leg.side = action
        req_leg.qtyRatio = quantity

    return RET_OK, ""


def _parse_option_strategy_leg(pb_leg):
    leg = OptionStrategyLeg()
    leg.code = merge_qot_mkt_stock_str(pb_leg.security.market, pb_leg.security.code)
    leg.action = StrategyLegAction.to_string2(pb_leg.side) if pb_leg.HasField('side') else NoneDataType
    leg.quantity = pb_leg.qtyRatio if pb_leg.HasField('qtyRatio') else NoneDataType
    return leg


class GetOptionQuoteQuery:
    """
    Query GetOptionQuote.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, option_legs, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetOptionQuote_pb2 import Request
        req = Request()
        ret, msg = _pack_option_strategy_legs(req.c2s.multi_legs, option_legs)
        if ret != RET_OK:
            return ret, msg, None, 0, 0
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetOptionQuote, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = []
        for item in rsp_pb.s2c.optionQuoteList:
            data = {}
            data["price"] = item.price if item.HasField('price') else NoneDataType
            data["change_val"] = item.chg if item.HasField('chg') else NoneDataType
            data["change_rate"] = item.chg_rate if item.HasField('chg_rate') else NoneDataType
            data["volume"] = item.vol if item.HasField('vol') else NoneDataType
            data["turnover"] = item.turnover if item.HasField('turnover') else NoneDataType
            data["high_price"] = item.high if item.HasField('high') else NoneDataType
            data["low_price"] = item.low if item.HasField('low') else NoneDataType
            data["mid_price"] = item.mid if item.HasField('mid') else NoneDataType
            data["open_price"] = item.open if item.HasField('open') else NoneDataType
            data["last_close_price"] = item.pre_close if item.HasField('pre_close') else NoneDataType
            data["open_interest"] = item.open_interest if item.HasField('open_interest') else NoneDataType
            data["premium"] = item.premium if item.HasField('premium') else NoneDataType
            data["implied_volatility"] = item.IV if item.HasField('IV') else NoneDataType
            data["delta"] = item.delta if item.HasField('delta') else NoneDataType
            data["gamma"] = item.gamma if item.HasField('gamma') else NoneDataType
            data["vega"] = item.vega if item.HasField('vega') else NoneDataType
            data["theta"] = item.theta if item.HasField('theta') else NoneDataType
            data["rho"] = item.rho if item.HasField('rho') else NoneDataType
            data["option_type"] = OptionType.to_string2(item.option_type) if item.HasField('option_type') else NoneDataType
            data["expire_time"] = item.expire_time if item.HasField('expire_time') else NoneDataType
            data["strike_price"] = item.strike if item.HasField('strike') else NoneDataType
            data["contract_size"] = item.contract_size if item.HasField('contract_size') else NoneDataType
            data["contract_multiplier"] = item.contract_multiplier if item.HasField('contract_multiplier') else NoneDataType
            data["exercise_type"] = OptionAreaType.to_string2(item.exercise_type) if item.HasField('exercise_type') else NoneDataType
            data["days_to_expiry"] = item.days_to_expiry if item.HasField('days_to_expiry') else NoneDataType
            data["net_open_interest"] = item.net_open_interest if item.HasField('net_open_interest') else NoneDataType
            data["contract_value"] = item.contract_value if item.HasField('contract_value') else NoneDataType
            data["equal_underlying"] = item.equal_underlying if item.HasField('equal_underlying') else NoneDataType
            data["index_option_type"] = IndexOptionType.to_string2(item.index_option_type) if item.HasField('index_option_type') else NoneDataType
            data["intrinsic_value"] = item.intrinsic_value if item.HasField('intrinsic_value') else NoneDataType
            data["time_value"] = item.time_value if item.HasField('time_value') else NoneDataType
            data["breakeven_point"] = list(item.breakeven_point)
            data["dist_to_breakeven"] = list(item.dist_to_breakeven)
            data["prob_of_profit"] = item.prob_of_profit if item.HasField('prob_of_profit') else NoneDataType
            data["seller_roi"] = item.seller_roi if item.HasField('seller_roi') else NoneDataType
            data["mark_price"] = item.mark_price if item.HasField('mark_price') else NoneDataType
            data["leverage_ratio"] = item.leverage_ratio if item.HasField('leverage_ratio') else NoneDataType
            data["effective_gearing"] = item.effective_gearing if item.HasField('effective_gearing') else NoneDataType
            ret_list.append(data)
        return RET_OK, "", ret_list


class GetOptionStrategyQuery:
    """
    Query GetOptionStrategy.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, option_strategy, conn_id, expire_time=None, far_expire_time=None, spread=None,
                 index_option_type=IndexOptionType.NORMAL, option_type=OptionType.ALL, strike_price=None,
                 security_firm=SecurityFirm.NONE):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        ret, option_strategy = OptionStrategyType.to_number(option_strategy)
        if ret is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of strategy_type param is wrong", None, 0, 0

        ret, index_option_type = IndexOptionType.to_number(index_option_type)
        if ret is False:
            index_option_type = None

        ret, option_type = OptionType.to_number(option_type)
        if ret is False:
            option_type = None

        from ..common.pb.Qot_GetOptionStrategy_pb2 import Request
        req = Request()
        req.c2s.owner.market = market_code
        req.c2s.owner.code = stock_code
        req.c2s.option_strategy = option_strategy
        if expire_time is not None:
            req.c2s.expire_time = expire_time
        if far_expire_time is not None:
            req.c2s.far_expire_time = far_expire_time
        if spread is not None:
            req.c2s.spread = spread
        if index_option_type is not None:
            req.c2s.index_option_type = index_option_type
        if option_type is not None:
            req.c2s.option_type = option_type
        if strike_price is not None:
            req.c2s.strike_price = strike_price
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetOptionStrategy, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = []
        for item in rsp_pb.s2c.strategyList:
            data = {}
            data["code"] = item.code
            data["name"] = item.name
            data["option_strategy"] = OptionStrategyType.to_string2(item.option_strategy)
            data["stock_owner"] = merge_qot_mkt_stock_str(item.stock_owner.market, item.stock_owner.code)
            data["legs"] = [_parse_option_strategy_leg(leg) for leg in item.multi_legs]
            ret_list.append(data)
        return RET_OK, "", ret_list


class GetOptionStrategyAnalysisQuery:
    """
    Query GetOptionStrategyAnalysis.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, option_legs, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetOptionStrategyAnalysis_pb2 import Request
        req = Request()
        ret, msg = _pack_option_strategy_legs(req.c2s.multi_legs, option_legs)
        if ret != RET_OK:
            return ret, msg, None, 0, 0
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetOptionStrategyAnalysis, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        item = rsp_pb.s2c
        data = {}
        data["code"] = item.code
        data["name"] = item.name
        data["option_strategy"] = OptionStrategyType.to_string2(item.option_strategy)
        data["bid1"] = item.bid1 if item.HasField('bid1') else NoneDataType
        data["ask1"] = item.ask1 if item.HasField('ask1') else NoneDataType
        data["max_profit"] = item.max_profit if item.HasField('max_profit') else NoneDataType
        data["max_loss"] = item.max_loss if item.HasField('max_loss') else NoneDataType
        data["breakeven_points"] = list(item.breakeven_points)
        data["prob_of_profit"] = item.prob_of_profit if item.HasField('prob_of_profit') else NoneDataType
        data["delta"] = item.delta if item.HasField('delta') else NoneDataType
        data["theta"] = item.theta if item.HasField('theta') else NoneDataType
        return RET_OK, "", [data]


class GetOptionStrategySpreadQuery:
    """
    Query GetOptionStrategySpread.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, option_strategy, conn_id, expire_time=None, far_expire_time=None,
                 index_option_type=IndexOptionType.NORMAL, security_firm=SecurityFirm.NONE):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content

        ret, option_strategy = OptionStrategyType.to_number(option_strategy)
        if ret is False:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of strategy_type param is wrong", None, 0, 0

        ret, index_option_type = IndexOptionType.to_number(index_option_type)
        if ret is False:
            index_option_type = None

        from ..common.pb.Qot_GetOptionStrategySpread_pb2 import Request
        req = Request()
        req.c2s.owner.market = market_code
        req.c2s.owner.code = stock_code
        req.c2s.option_strategy = option_strategy
        if expire_time is not None:
            req.c2s.expire_time = expire_time
        if far_expire_time is not None:
            req.c2s.far_expire_time = far_expire_time
        if index_option_type is not None:
            req.c2s.index_option_type = index_option_type
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetOptionStrategySpread, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = []
        for spread in rsp_pb.s2c.spreadList:
            ret_list.append({"spread": spread})
        return RET_OK, "", ret_list


class GetSearchQuoteQuery:
    """Query GetSearchQuote."""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, keyword, max_count, conn_id, security_firm=SecurityFirm.NONE):
        if not keyword:
            return RET_ERROR, ERROR_STR_PREFIX + "keyword is required", None, 0, 0
        from ..common.pb.Qot_GetSearchQuote_pb2 import Request
        req = Request()
        req.c2s.keyword = keyword
        if max_count is not None:
            req.c2s.max_count = max_count
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_GetSearchQuote, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = []
        for item in rsp_pb.s2c.search_quote_list:
            data = {
                "market": Market.to_string2(item.market) if item.HasField('market') else NoneDataType,
                "code": item.code if item.HasField('code') else NoneDataType,
                "name": item.name if item.HasField('name') else NoneDataType,
                "sec_type": SecurityType.to_string2(item.sec_type) if item.HasField('sec_type') else NoneDataType,
                "is_watched": item.is_watched if item.HasField('is_watched') else NoneDataType,
            }
            ret_list.append(data)
        return RET_OK, "", ret_list


class GetSearchNewsQuery:
    """Query GetSearchNews."""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, keyword, max_count, news_sub_type, conn_id):
        if not keyword:
            return RET_ERROR, ERROR_STR_PREFIX + "keyword is required", None, 0, 0
        from ..common.pb.Qot_GetSearchNews_pb2 import Request
        req = Request()
        req.c2s.keyword = keyword
        if max_count is not None:
            req.c2s.max_count = max_count
        if news_sub_type is not None:
            r, news_sub_type_num = NewsSubType.to_number(news_sub_type)
            if not r:
                return RET_ERROR, ERROR_STR_PREFIX + "the type of news_sub_type param is wrong", None, 0, 0
            req.c2s.news_sub_type = news_sub_type_num
        return pack_pb_req(req, ProtoId.Qot_GetSearchNews, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = []
        for item in rsp_pb.s2c.search_news_list:
            data = {
                "title": item.title if item.HasField('title') else NoneDataType,
                "news_sub_type": NewsSubType.to_string2(item.news_sub_type) if item.HasField('news_sub_type') else NoneDataType,
                "source": item.source if item.HasField('source') else NoneDataType,
                "publish_time": item.publish_time if item.HasField('publish_time') else NoneDataType,
                "view_count": item.view_count if item.HasField('view_count') else NoneDataType,
                "related_securities": list(item.related_securities),
                "url": item.url if item.HasField('url') else NoneDataType,
            }
            ret_list.append(data)
        return RET_OK, "", ret_list


def _skill_wrap_unusual_rsp_unpack(rsp_pb):
    """解析 SkillWrapAPI 中 *UnusualRsp（与 Qot_RequestHistoryKL Response 一致使用 retType/retMsg）。"""
    if rsp_pb is None:
        return RET_ERROR, "empty response", None
    if rsp_pb.retType != RET_OK:
        return RET_ERROR, rsp_pb.retMsg, None
    data = {}
    if rsp_pb.HasField("errCode"):
        data["err_code"] = rsp_pb.errCode
    data["retMsg"] = rsp_pb.retMsg if rsp_pb.HasField("retMsg") else ""
    data["time_range"] = rsp_pb.time_range if rsp_pb.HasField("time_range") else ""
    data["content"] = rsp_pb.content if rsp_pb.HasField("content") else ""
    return RET_OK, "", data


class SkillWrapTechnicalUnusualQuery:
    """技术指标异动。"""

    @classmethod
    def pack_req(cls, code, time_range, indicator_filters, language_id, conn_id):
        if code is None:
            return RET_ERROR, ERROR_STR_PREFIX + "code is required", None, 0, 0
        from ..common.pb.SkillWrapAPI_pb2 import TechnicalUnusualReq
        req = TechnicalUnusualReq()
        req.stock_symbol = code if isinstance(code, str) else str(code)
        if time_range is not None:
            req.time_range = int(time_range)
        if indicator_filters:
            for s in indicator_filters:
                req.indicator_filters.append(str(s))
        if language_id is not None:
            req.language_id = int(language_id)
        return pack_pb_req(req, ProtoId.SkillWrap_TechnicalUnusual, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        return _skill_wrap_unusual_rsp_unpack(rsp_pb)


class SkillWrapFinancialUnusualQuery:
    """财务异动。"""

    @classmethod
    def pack_req(cls, code, time_range, analysis_dimensions, language_id, conn_id):
        if code is None:
            return RET_ERROR, ERROR_STR_PREFIX + "code is required", None, 0, 0
        from ..common.pb.SkillWrapAPI_pb2 import FinancialUnusualReq
        req = FinancialUnusualReq()
        req.stock_symbol = code if isinstance(code, str) else str(code)
        if time_range is not None:
            req.time_range = int(time_range)
        if analysis_dimensions:
            for s in analysis_dimensions:
                req.analysis_dimensions.append(str(s))
        if language_id is not None:
            req.language_id = int(language_id)
        return pack_pb_req(req, ProtoId.SkillWrap_FinancialUnusual, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        return _skill_wrap_unusual_rsp_unpack(rsp_pb)


class SkillWrapDerivativeUnusualQuery:
    """衍生品异动。"""

    @classmethod
    def pack_req(cls, code, time_range, analysis_dimensions, language_id, conn_id):
        if code is None:
            return RET_ERROR, ERROR_STR_PREFIX + "code is required", None, 0, 0
        from ..common.pb.SkillWrapAPI_pb2 import DerivativeUnusualReq
        req = DerivativeUnusualReq()
        req.stock_symbol = code if isinstance(code, str) else str(code)
        if time_range is not None:
            req.time_range = int(time_range)
        if analysis_dimensions:
            for s in analysis_dimensions:
                req.analysis_dimensions.append(str(s))
        if language_id is not None:
            req.language_id = int(language_id)
        return pack_pb_req(req, ProtoId.SkillWrap_DerivativeUnusual, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        return _skill_wrap_unusual_rsp_unpack(rsp_pb)
        



class GetIndicatorListQuery:
    """
    Query GetIndicatorList.
    获取全部可用指标列表

    返回 list of dict，每个 dict 表示一个 IndicatorEntry，含：
      - my_lang: dict 或 None（麦语言版本）
      - python:  dict 或 None（Python 版本）

    每个语言版本 dict 字段：
      - short_name: str
      - full_name:  str
      - inputs:     list of dict，每条 {index, name, value[, var_name]}（var_name 仅麦语言）
      - outputs:    list of dict，每条 {index, name}

    input 中 value 为 dict {type, value}：
      - type: 'INT'/'FLOAT'/'STRING'/'BOOL'/'COLOR'/'SHAPE'/'LINE'/'UNKNOWN'
      - value: 对应类型的 Python 值；COLOR 是 {alpha,red,green,blue}；SHAPE/LINE 是枚举名字符串
    """

    # 类型枚举值 → 字符串名（去前缀）
    _TYPE_NAME = {
        0: 'UNKNOWN',
        1: 'INT',
        2: 'FLOAT',
        3: 'STRING',
        4: 'COLOR',
        5: 'SHAPE',
        6: 'LINE',
        7: 'BOOL',
    }

    _SHAPE_NAME = {
        0: 'UNKNOWN',
        1: 'XCROSS',
        2: 'CROSS',
        3: 'CIRCLE',
        4: 'TRIANGLE_UP',
        5: 'TRIANGLE_DOWN',
        6: 'FLAG',
        7: 'ARROW_UP',
        8: 'ARROW_DOWN',
        9: 'SQUARE',
        10: 'DIAMOND',
        11: 'LABEL_UP',
        12: 'LABEL_DOWN',
    }

    _LINE_NAME = {
        0: 'UNKNOWN',
        1: 'SOLID',
        2: 'DASHED',
        3: 'DOT',
        4: 'CROSS',
        5: 'CIRCLE',
        6: 'HISTOGRAM',
        7: 'HISTOGRAM_LINE',
        8: 'STEP',
        9: 'STEP_DIAMONDS',
    }

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, conn_id, search_key=None, lang_type=0, search_mode=0):
        from ..common.pb.Qot_GetIndicatorList_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        if search_key:
            req.c2s.searchKey = search_key
        if lang_type is not None:
            req.c2s.langType = int(lang_type)
        if search_mode is not None:
            req.c2s.searchMode = int(search_mode)
        return pack_pb_req(req, ProtoId.Qot_GetIndicatorList, conn_id)

    @classmethod
    def _conv_value(cls, pb_val):
        """把 IndicatorParamValue PB 转成 {'type': str, 'value': ...}"""
        if pb_val is None:
            return None
        type_int = pb_val.type if pb_val.HasField('type') else 0
        type_name = cls._TYPE_NAME.get(type_int, 'UNKNOWN')
        result = {'type': type_name}

        if type_name == 'INT':
            result['value'] = pb_val.intValue if pb_val.HasField('intValue') else 0
        elif type_name == 'FLOAT':
            result['value'] = pb_val.floatValue if pb_val.HasField('floatValue') else 0.0
        elif type_name == 'STRING':
            result['value'] = pb_val.stringValue if pb_val.HasField('stringValue') else ''
        elif type_name == 'BOOL':
            result['value'] = pb_val.boolValue if pb_val.HasField('boolValue') else False
        elif type_name == 'COLOR':
            if pb_val.HasField('colorValue'):
                result['value'] = pb_val.colorValue   # 服务端输出格式 "#RRGGBB"
            else:
                result['value'] = ''
        elif type_name == 'SHAPE':
            shape_int = pb_val.shapeValue if pb_val.HasField('shapeValue') else 0
            result['value'] = cls._SHAPE_NAME.get(shape_int, 'UNKNOWN')
        elif type_name == 'LINE':
            line_int = pb_val.lineValue if pb_val.HasField('lineValue') else 0
            result['value'] = cls._LINE_NAME.get(line_int, 'UNKNOWN')
        else:
            result['value'] = None
        return result

    @classmethod
    def _conv_info(cls, pb_info):
        """把 IndicatorInfo PB 转成 dict；pb_info 为 None 返回 None"""
        if pb_info is None:
            return None
        inputs = []
        for ipt in pb_info.inputs:
            item = {
                'index': ipt.index if ipt.HasField('index') else 0,
                'name':  ipt.name  if ipt.HasField('name')  else '',
                'value': cls._conv_value(ipt.value) if ipt.HasField('value') else None,
            }
            # var_name 仅麦语言指标有效，Python 指标缺失
            if ipt.HasField('varName'):
                item['var_name'] = ipt.varName
            inputs.append(item)
        outputs = []
        for opt in pb_info.outputs:
            outputs.append({
                'index': opt.index if opt.HasField('index') else 0,
                'name':  opt.name  if opt.HasField('name')  else '',
            })
        return {
            'short_name': pb_info.shortName if pb_info.HasField('shortName') else '',
            'full_name':  pb_info.fullName  if pb_info.HasField('fullName')  else '',
            'inputs':     inputs,
            'outputs':    outputs,
            'script':     pb_info.script if pb_info.HasField('script') else '',
        }

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = list()
        for entry in rsp_pb.s2c.indicatorList:
            my_lang_info = cls._conv_info(entry.myLang) if entry.HasField('myLang') else None
            python_info  = cls._conv_info(entry.python) if entry.HasField('python') else None
            ret_list.append({
                'my_lang': my_lang_info,
                'python':  python_info,
            })
        return RET_OK, "", ret_list


def _unpack_indicator_output_param(opt):
    """把 Qot_Common.IndicatorOutputParam PB 转成 dict"""
    return {
        "index": opt.index if opt.HasField("index") else 0,
        "name":  opt.name  if opt.HasField("name")  else "",
    }


class RequestIndicatorCalcQuery:
    """
    Query Qot_RequestIndicatorCalc(3254)：异步发起指标计算，立即收到 calcId。
    结果通过 Qot_PushIndicatorCalc(3255) 推送，由 IndicatorCalcHandlerBase 处理。
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, short_name, lang_type, klines, conn_id, security=None, kl_type=None, num=None, input_params=None):
        if not short_name:
            return RET_ERROR, "short_name is empty", None, 0, 0
        if not security:
            return RET_ERROR, "security is required (need market+code for calc context)", None, 0, 0
        if kl_type is None:
            return RET_ERROR, "kl_type is required (Qot_Common.KLType wire value)", None, 0, 0

        from ..common.pb.Qot_RequestIndicatorCalc_pb2 import Request
        req = Request()
        req.c2s.shortName = short_name
        req.c2s.langType = int(lang_type)

        if isinstance(security, dict):
            sec_market = security.get("market")
            sec_code = security.get("code")
        elif isinstance(security, (tuple, list)) and len(security) >= 2:
            sec_market, sec_code = int(security[0]), str(security[1])
        else:
            return RET_ERROR, "security must be dict{market,code} or (market, code)", None, 0, 0
        if sec_market is None or sec_code is None or sec_code == "":
            return RET_ERROR, "security.market / security.code is required", None, 0, 0
        req.c2s.data.security.market = int(sec_market)
        req.c2s.data.security.code = str(sec_code)
        req.c2s.data.klType = int(kl_type)

        # 入参规范 = SDK 行情列名（与 request_history_kline 返回的 DataFrame 列对齐）：
        #   time_key, open, high, low, close, last_close, volume, turnover,
        #   turnover_rate, pe_ratio, is_blank, timestamp
        # 用户可直接 df.to_dict(orient="records") 喂入，无需中间转换。
        for kl in klines:
            pb_kl = req.c2s.data.kLine.add()
            pb_kl.time = str(kl.get("time_key", "") or "")
            pb_kl.isBlank = bool(kl.get("is_blank", False))
            if kl.get("timestamp") is not None:
                pb_kl.timestamp = float(kl["timestamp"])
            if kl.get("open") is not None:
                pb_kl.openPrice = float(kl["open"])
            if kl.get("high") is not None:
                pb_kl.highPrice = float(kl["high"])
            if kl.get("low") is not None:
                pb_kl.lowPrice = float(kl["low"])
            if kl.get("close") is not None:
                pb_kl.closePrice = float(kl["close"])
            if kl.get("last_close") is not None:
                pb_kl.lastClosePrice = float(kl["last_close"])
            if kl.get("volume") is not None:
                pb_kl.volume = int(kl["volume"])
            if kl.get("turnover") is not None:
                pb_kl.turnover = float(kl["turnover"])
            if kl.get("turnover_rate") is not None:
                pb_kl.turnoverRate = float(kl["turnover_rate"])
            if kl.get("pe_ratio") is not None:
                pb_kl.pe = float(kl["pe_ratio"])

        if num is not None:
            if not isinstance(num, int) or num <= 0:
                return RET_ERROR, "num must be None or a positive integer", None, 0, 0
            req.c2s.num = num

        for ip in (input_params or []):
            if not isinstance(ip, dict):
                return RET_ERROR, "input_params item must be dict", None, 0, 0
            idx = ip.get("index")
            value = ip.get("value")
            if idx is None or value is None:
                return RET_ERROR, "input_params item requires index and value", None, 0, 0
            if int(idx) < 0:
                return RET_ERROR, "input_params index must be >= 0 (0-based)", None, 0, 0
            pb_ip = req.c2s.inputs.add()
            pb_ip.index = int(idx)
            pb_ip.value = str(value)

        return pack_pb_req(req, ProtoId.Qot_RequestIndicatorCalc, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            calc_id = rsp_pb.s2c.calcId if rsp_pb.HasField("s2c") else ""
            return RET_ERROR, rsp_pb.retMsg, {"calc_id": calc_id}
        return RET_OK, "", {"calc_id": rsp_pb.s2c.calcId}


class PushIndicatorCalcQuery:
    """
    Parse Qot_PushIndicatorCalc(3255) push payload.
    用于 IndicatorCalcHandlerBase.parse_rsp_pb。
    """

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        s2c = rsp_pb.s2c
        if rsp_pb.retType != RET_OK:
            # calcId is a required scalar field — HasField is invalid on it in
            # protobuf2 Python and raises ValueError.  Access it directly; if
            # the server omitted s2c entirely the default-constructed message
            # returns "" which is handled by the caller's routing guard.
            return RET_ERROR, rsp_pb.retMsg, {
                "calc_id":     s2c.calcId,
                "outputs":     [],
                "output_rows": [],
            }
        outputs = [_unpack_indicator_output_param(o) for o in s2c.outputs]
        rows = []
        for item in s2c.outputRows:
            rows.append({
                "time":   item.time if item.HasField("time") else "",
                "values": list(item.values),
            })
        return RET_OK, "", {
            "calc_id":     s2c.calcId,
            "outputs":     outputs,
            "output_rows": rows,
        }


# ============================================================
# 事件合约 (Event Contract) Query 类
# ============================================================

class GetEventContractCategoryQuery:
    """获取事件合约分类"""

    @classmethod
    def pack_req(cls, category, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractCategory_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        if category is not None:
            req.c2s.category = category
        return pack_pb_req(req, ProtoId.Qot_GetEventContractCategory, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = []
        for item in rsp_pb.s2c.categoryList:
            data = {
                'category': item.category,
                'category_name': get_optional_from_pb(item, 'categoryName'),
                'tags': list(item.tags),
            }
            ret_list.append(data)
        return RET_OK, "", ret_list


class FilterCompetitionQuery:
    """赛事筛选"""

    @classmethod
    def pack_req(cls, category, tag, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_FilterCompetition_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        if category is not None:
            req.c2s.category = category
        if tag is not None:
            req.c2s.tag = tag
        return pack_pb_req(req, ProtoId.Qot_FilterCompetition, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = []
        for item in rsp_pb.s2c.tagFilterList:
            data = {
                'category': get_optional_from_pb(item, 'category'),
                'tag': item.tag,
                'competition': list(item.competitionList),
                'scope': list(item.scopeList),
            }
            ret_list.append(data)
        return RET_OK, "", ret_list


class GetEventContractSeriesListQuery:
    """获取事件合约Series列表"""

    @classmethod
    def pack_req(cls, category, tag, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractSeriesList_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        if category is not None:
            req.c2s.category = category
        if tag is not None:
            req.c2s.tag = tag
        return pack_pb_req(req, ProtoId.Qot_GetEventContractSeriesList, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = []
        for item in rsp_pb.s2c.seriesList:
            data = {
                'series_code': merge_qot_mkt_stock_str(item.seriesSecurity.market, item.seriesSecurity.code),
                'series_name': get_optional_from_pb(item, 'seriesName'),
                'category': get_optional_from_pb(item, 'category'),
                'tags': list(item.tags),
                'frequency': ECFrequency.to_string2(item.frequency) if item.HasField('frequency') else NoneDataType,
            }
            ret_list.append(data)
        return RET_OK, "", ret_list


class GetEventContractEventListQuery:
    """获取事件合约Event列表"""

    @classmethod
    def pack_req(cls, series_code, status, next_page, count, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractEventList_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        ret_code, content = split_stock_str(series_code)
        if ret_code != RET_OK:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content
        req.c2s.series.market = market_code
        req.c2s.series.code = stock_code
        if status is not None:
            ret, val = ECStatus.to_number(status)
            if not ret:
                return RET_ERROR, val, None, 0, 0
            req.c2s.status = val
        if next_page is not None:
            req.c2s.nextPage = next_page
        if count is not None:
            req.c2s.count = count
        return pack_pb_req(req, ProtoId.Qot_GetEventContractEventList, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = []
        for item in rsp_pb.s2c.eventList:
            data = {
                'event_code': merge_qot_mkt_stock_str(item.eventSecurity.market, item.eventSecurity.code),
                'event_name': get_optional_from_pb(item, 'eventName'),
                'event_sub_name': get_optional_from_pb(item, 'eventSubName'),
                'status': ECStatus.to_string2(item.status) if item.HasField('status') else NoneDataType,
                'series_code': merge_qot_mkt_stock_str(item.seriesSecurity.market, item.seriesSecurity.code) if item.HasField('seriesSecurity') else NoneDataType,
                'start_date': get_optional_from_pb(item, 'startDate'),
                'end_date': get_optional_from_pb(item, 'endDate'),
                'category': get_optional_from_pb(item, 'category'),
                'tags': list(item.tags),
                'mutually_exclusive': get_optional_from_pb(item, 'mutuallyExclusive'),
                'competition': get_optional_from_pb(item, 'competition'),
                'competition_scope': get_optional_from_pb(item, 'competitionScope'),
            }
            ret_list.append(data)
        next_page = get_optional_from_pb(rsp_pb.s2c, 'nextPage')
        return RET_OK, "", (ret_list, next_page)


class GetEventContractQuery:
    """获取事件合约Contract列表"""

    @classmethod
    def pack_req(cls, event_code, next_page, count, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContract_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        ret_code, content = split_stock_str(event_code)
        if ret_code != RET_OK:
            return RET_ERROR, content, None, 0, 0
        market_code, stock_code = content
        req.c2s.event.market = market_code
        req.c2s.event.code = stock_code
        if next_page is not None:
            req.c2s.nextPage = next_page
        if count is not None:
            req.c2s.count = count
        return pack_pb_req(req, ProtoId.Qot_GetEventContract, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = []
        for item in rsp_pb.s2c.contractList:
            data = {
                'contract_code': merge_qot_mkt_stock_str(item.contractSecurity.market, item.contractSecurity.code),
                'event_code': merge_qot_mkt_stock_str(item.eventSecurity.market, item.eventSecurity.code) if item.HasField('eventSecurity') else NoneDataType,
                'series_code': merge_qot_mkt_stock_str(item.seriesSecurity.market, item.seriesSecurity.code) if item.HasField('seriesSecurity') else NoneDataType,
                'contract_type': ECContractType.to_string2(item.contractType) if item.HasField('contractType') else NoneDataType,
                'title': get_optional_from_pb(item, 'title'),
                'yes_sub_title': get_optional_from_pb(item, 'yesSubTitle'),
                'open_time': get_optional_from_pb(item, 'openTime'),
                'close_time': get_optional_from_pb(item, 'closeTime'),
                'determination_time': get_optional_from_pb(item, 'determinationTime'),
                'settled_time': get_optional_from_pb(item, 'settledTime'),
                'latest_expiration_time': get_optional_from_pb(item, 'latestExpirationTime'),
                'status': ECStatus.to_string2(item.status) if item.HasField('status') else NoneDataType,
                'result': get_optional_from_pb(item, 'result'),
                'settlement_value': get_optional_from_pb(item, 'settlementValue'),
                'expiration_value': get_optional_from_pb(item, 'expirationValue'),
                'volume': get_optional_from_pb(item, 'volume'),
                'can_close_early': get_optional_from_pb(item, 'canCloseEarly'),
                'tick_size': get_optional_from_pb(item, 'tickSize'),
                'category': get_optional_from_pb(item, 'category'),
                'tag': get_optional_from_pb(item, 'tag'),
            }
            ret_list.append(data)
        recommend_list = []
        for item in rsp_pb.s2c.recommendContracts:
            recommend_list.append({
                'contract_code': merge_qot_mkt_stock_str(item.contractSecurity.market, item.contractSecurity.code),
            })
        next_page = get_optional_from_pb(rsp_pb.s2c, 'nextPage')
        return RET_OK, "", (ret_list, recommend_list, next_page)


class GetEventContractMilestoneListQuery:
    """获取事件合约里程碑列表"""

    @classmethod
    def pack_req(cls, category, competition, related_event, next_page, count, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractMilestoneList_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        if category is not None:
            req.c2s.category = category
        if competition is not None:
            req.c2s.competition = competition
        if related_event is not None:
            ret_code, content = split_stock_str(related_event)
            if ret_code != RET_OK:
                return RET_ERROR, content, None, 0, 0
            market_code, stock_code = content
            req.c2s.relatedEvent.market = market_code
            req.c2s.relatedEvent.code = stock_code
        if next_page is not None:
            req.c2s.nextPage = next_page
        if count is not None:
            req.c2s.count = count
        return pack_pb_req(req, ProtoId.Qot_GetEventContractMilestoneList, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = []
        for item in rsp_pb.s2c.milestoneList:
            related_events = []
            for sec in item.relatedEventList:
                related_events.append(merge_qot_mkt_stock_str(sec.market, sec.code))
            data = {
                'milestone_code': merge_qot_mkt_stock_str(item.milestoneSecurity.market, item.milestoneSecurity.code),
                'title': get_optional_from_pb(item, 'title'),
                'category': get_optional_from_pb(item, 'category'),
                'type': ECMilestoneType.to_string2(item.type) if item.HasField('type') else NoneDataType,
                'start_date': get_optional_from_pb(item, 'startDate'),
                'end_date': get_optional_from_pb(item, 'endDate'),
                'primary_event_code': merge_qot_mkt_stock_str(item.primaryEventSecurity.market, item.primaryEventSecurity.code) if item.HasField('primaryEventSecurity') else NoneDataType,
                'related_events': related_events,
                'notification_message': get_optional_from_pb(item, 'notificationMessage'),
            }
            ret_list.append(data)
        next_page = get_optional_from_pb(rsp_pb.s2c, 'nextPage')
        return RET_OK, "", (ret_list, next_page)


class GetEventContractComboListQuery:
    """获取可Combo事件列表"""

    @classmethod
    def pack_req(cls, category, competition, series, next_page, count, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractComboList_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        if category is not None:
            req.c2s.category = category
        if competition is not None:
            req.c2s.competition = competition
        if series is not None:
            ret_code, content = split_stock_str(series)
            if ret_code != RET_OK:
                return RET_ERROR, content, None, 0, 0
            market_code, stock_code = content
            req.c2s.series.market = market_code
            req.c2s.series.code = stock_code
        if next_page is not None:
            req.c2s.nextPage = next_page
        if count is not None:
            req.c2s.count = count
        return pack_pb_req(req, ProtoId.Qot_GetEventContractComboList, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = []
        for item in rsp_pb.s2c.comboEventList:
            combo_contracts = []
            for sec in item.comboContracts:
                combo_contracts.append(merge_qot_mkt_stock_str(sec.market, sec.code))
            data = {
                'event_code': merge_qot_mkt_stock_str(item.eventSecurity.market, item.eventSecurity.code),
                'event_name': get_optional_from_pb(item, 'eventName'),
                'combo_contracts': combo_contracts,
                'series_code': merge_qot_mkt_stock_str(item.seriesSecurity.market, item.seriesSecurity.code) if item.HasField('seriesSecurity') else NoneDataType,
                'category': get_optional_from_pb(item, 'category'),
                'competition': get_optional_from_pb(item, 'competition'),
                'competition_scope': get_optional_from_pb(item, 'competitionScope'),
            }
            ret_list.append(data)
        mvc = get_optional_from_pb(rsp_pb.s2c, 'mvc')
        next_page = get_optional_from_pb(rsp_pb.s2c, 'nextPage')
        return RET_OK, "", (ret_list, mvc, next_page)


class GetEventContractComboRfqQuery:
    """Combo询价"""

    @classmethod
    def _pack_combo_leg(cls, combo_leg, pb_leg):
        if not isinstance(combo_leg, ComboLeg):
            return RET_ERROR, make_wrong_type_msg('combo_leg_list item', 'ComboLeg')
        if combo_leg.code is None:
            return RET_ERROR, "ComboLeg.code is required"
        ret_code, content = split_stock_str(combo_leg.code)
        if ret_code != RET_OK:
            return ret_code, content
        market_code, stock_code = content
        pb_leg.security.market = market_code
        pb_leg.security.code = stock_code
        if combo_leg.trd_side is not None:
            ret, val = TrdSide.to_number(combo_leg.trd_side)
            if not ret:
                return RET_ERROR, val
            pb_leg.side = val
        if combo_leg.qty_ratio is not None:
            pb_leg.qtyRatio = float(combo_leg.qty_ratio)
        if combo_leg.position_id is not None:
            pb_leg.positionID = combo_leg.position_id
        if combo_leg.pred_side is not None:
            ret, val = PredSide.to_number(combo_leg.pred_side)
            if not ret:
                return RET_ERROR, val
            pb_leg.predSide = val
        return RET_OK, ""

    @classmethod
    def _parse_combo_leg(cls, pb_leg):
        combo_leg = ComboLeg()
        combo_leg.code = merge_qot_mkt_stock_str(pb_leg.security.market, pb_leg.security.code)
        combo_leg.trd_side = TrdSide.to_string2(pb_leg.side) if pb_leg.HasField('side') else None
        combo_leg.qty_ratio = pb_leg.qtyRatio if pb_leg.HasField('qtyRatio') else None
        combo_leg.position_id = pb_leg.positionID if pb_leg.HasField('positionID') else None
        combo_leg.pred_side = PredSide.to_string2(pb_leg.predSide) if pb_leg.HasField('predSide') else None
        return combo_leg

    @classmethod
    def pack_req(cls, combo_leg_list, mvc, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractComboRfq_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        for combo_leg in combo_leg_list:
            pb_leg = req.c2s.comboLegList.add()
            ret_code, msg = cls._pack_combo_leg(combo_leg, pb_leg)
            if ret_code != RET_OK:
                return ret_code, msg, None, 0, 0
        req.c2s.mvc = mvc
        return pack_pb_req(req, ProtoId.Qot_GetEventContractComboRfq, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        combo_leg_list = [cls._parse_combo_leg(leg) for leg in rsp_pb.s2c.comboLegList]
        data = {
            'combo_leg_list': combo_leg_list,
            'bid_price': get_optional_from_pb(rsp_pb.s2c, 'bidPrice'),
            'ask_price': get_optional_from_pb(rsp_pb.s2c, 'askPrice'),
            'quote_id': get_optional_from_pb(rsp_pb.s2c, 'quoteId'),
            'should_retry': get_optional_from_pb(rsp_pb.s2c, 'shouldRetry'),
        }
        return RET_OK, "", data


class SubEventContractQuery:
    """事件合约订阅/反订阅"""

    @classmethod
    def pack_req(cls, code_list, subtype_list, is_sub, conn_id, is_first_push,
                 subscribe_push, kline_source_list, unsub_all, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_SubEventContract_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        if unsub_all:
            req.c2s.isUnsubAll = True
            req.c2s.isSubOrUnSub = False
        else:
            for code in code_list:
                ret_code, content = split_stock_str(code)
                if ret_code != RET_OK:
                    return ret_code, content, None
                market_code, stock_code = content
                stock_inst = req.c2s.securityList.add()
                stock_inst.code = stock_code
                stock_inst.market = market_code
            for subtype in subtype_list:
                r, v = SubType.to_number(subtype)
                if not r:
                    return RET_ERROR, v, None
                req.c2s.subTypeList.append(v)
            req.c2s.isSubOrUnSub = is_sub
            req.c2s.isRegOrUnRegPush = subscribe_push
            req.c2s.isFirstPush = is_first_push
            if kline_source_list:
                for src in kline_source_list:
                    r, v = ECKlineSource.to_number(src)
                    if not r:
                        return RET_ERROR, v, None
                    req.c2s.klineSource.append(v)
        set_qot_header(req, security_firm)
        return pack_pb_req(req, ProtoId.Qot_SubEventContract, conn_id)

    @classmethod
    def pack_subscribe_req(cls, code_list, subtype_list, conn_id, is_first_push, subscribe_push,
                           kline_source_list, security_firm=SecurityFirm.NONE):
        return cls.pack_req(code_list, subtype_list, True, conn_id, is_first_push,
                            subscribe_push, kline_source_list, False, security_firm)

    @classmethod
    def pack_unsubscribe_req(cls, code_list, subtype_list, conn_id, subscribe_push,
                             kline_source_list, security_firm=SecurityFirm.NONE):
        return cls.pack_req(code_list, subtype_list, False, conn_id, True,
                            subscribe_push, kline_source_list, False, security_firm)

    @classmethod
    def pack_unsub_all_req(cls, conn_id, security_firm=SecurityFirm.NONE):
        return cls.pack_req(None, None, False, conn_id, True, False, None, True, security_firm)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        return RET_OK, "", None


class GetEventContractSnapshotQuery:
    """获取事件合约快照"""

    @classmethod
    def pack_req(cls, code_list, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractSnapshot_pb2 import Request
        req = Request()
        req.c2s.SetInParent()
        for code in code_list:
            ret_code, content = split_stock_str(code)
            if ret_code != RET_OK:
                return ret_code, content, None, 0, 0
            market_code, stock_code = content
            stock_inst = req.c2s.securityList.add()
            stock_inst.code = stock_code
            stock_inst.market = market_code
        return pack_pb_req(req, ProtoId.Qot_GetEventContractSnapshot, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = []
        for item in rsp_pb.s2c.snapshotList:
            data = {
                'code': merge_qot_mkt_stock_str(item.code.market, item.code.code),
                'name': get_optional_from_pb(item, 'name'),
                'event_code': merge_qot_mkt_stock_str(item.event_code.market, item.event_code.code) if item.HasField('event_code') else NoneDataType,
                'yes_sub_title': get_optional_from_pb(item, 'yes_sub_title'),
                'no_sub_title': get_optional_from_pb(item, 'no_sub_title'),
                'status': ECStatus.to_string2(item.status) if item.HasField('status') else NoneDataType,
                'price': get_optional_from_pb(item, 'price'),
                'cumulative_volume': get_optional_from_pb(item, 'cumulative_volume'),
                'yes_bid': get_optional_from_pb(item, 'yes_bid'),
                'yes_bid_size': get_optional_from_pb(item, 'yes_bid_size'),
                'yes_ask': get_optional_from_pb(item, 'yes_ask'),
                'yes_ask_size': get_optional_from_pb(item, 'yes_ask_size'),
                'no_bid': get_optional_from_pb(item, 'no_bid'),
                'no_bid_size': get_optional_from_pb(item, 'no_bid_size'),
                'no_ask': get_optional_from_pb(item, 'no_ask'),
                'no_ask_size': get_optional_from_pb(item, 'no_ask_size'),
                'last_trade_time': get_optional_from_pb(item, 'last_trade_time'),
                'volume_24h': get_optional_from_pb(item, 'volume_24h'),
                'open_interest': get_optional_from_pb(item, 'open_interest'),
            }
            ret_list.append(data)
        return RET_OK, "", ret_list


class GetEventContractOrderBookQuery:
    """获取事件合约摆盘"""

    @classmethod
    def pack_req(cls, code, num, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractOrderBook_pb2 import Request
        ret_code, content = split_stock_str(code)
        if ret_code != RET_OK:
            return ret_code, content, None, 0, 0
        market_code, stock_code = content
        if isinstance(num, int) is False:
            error_str = ERROR_STR_PREFIX + "num is %s of type %s, and the type should be %s" \
                                           % (num, str(type(num)), str(int))
            return RET_ERROR, error_str, None, 0, 0
        if num <= 0:
            error_str = ERROR_STR_PREFIX + "num is %s, which should be greater than 0" % num
            return RET_ERROR, error_str, None, 0, 0
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        req.c2s.num = num
        return pack_pb_req(req, ProtoId.Qot_GetEventContractOrderBook, conn_id)

    @classmethod
    def _parse_order_book(cls, item):
        return {
            'code': merge_qot_mkt_stock_str(item.code.market, item.code.code),
            'yes_bids': [(lv.price, lv.size) for lv in item.yesBids],
            'yes_asks': [(lv.price, lv.size) for lv in item.yesAsks],
            'no_bids': [(lv.price, lv.size) for lv in item.noBids],
            'no_asks': [(lv.price, lv.size) for lv in item.noAsks],
        }

    @classmethod
    def _parse_order_book_list(cls, rsp_pb):
        return [cls._parse_order_book(item) for item in rsp_pb.s2c.orderBookList]

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        order_book_list = cls._parse_order_book_list(rsp_pb)
        # 查询接口入参为单只合约，回包取第一项（与通用 get_order_book 对齐，返回单层 dict）
        if not order_book_list:
            return RET_ERROR, "no event contract order book data", None
        order_book = order_book_list[0]
        return RET_OK, "", order_book


class GetEventContractKlineQuery:
    """获取事件合约K线"""

    @classmethod
    def pack_req(cls, code, pre_side, ktype, kline_source, max_count, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractKline_pb2 import Request
        ret_code, content = split_stock_str(code)
        if ret_code != RET_OK:
            return ret_code, content, None, 0, 0
        market_code, stock_code = content
        if not KLType.if_has_key(ktype):
            error_str = ERROR_STR_PREFIX + "ktype is %s, which is not valid. (%s)" \
                % (ktype, KLType.get_all_keys())
            return RET_ERROR, error_str, None, 0, 0
        # EC 具体支持哪些 K 线类型由后端决定，不支持时由后端报错
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if pre_side is not None:
            r, v = PredSide.to_number(pre_side)
            if not r:
                return RET_ERROR, v, None, 0, 0
            req.c2s.preSide = v
        _, req.c2s.ktype = KLType.to_number(ktype)
        if kline_source is not None:
            r, v = ECKlineSource.to_number(kline_source)
            if not r:
                return RET_ERROR, v, None, 0, 0
            req.c2s.klineSource = v
        if max_count is not None:
            req.c2s.maxCount = max_count
        return pack_pb_req(req, ProtoId.Qot_GetEventContractKline, conn_id)

    @classmethod
    def _parse_kline_item(cls, item):
        code = merge_qot_mkt_stock_str(item.code.market, item.code.code)
        pre_side = PredSide.to_string2(item.pre_side) if item.HasField('pre_side') else NoneDataType
        name = get_optional_from_pb(item, 'name')
        kline_list = [{
            'code': code,
            'pre_side': pre_side,
            'name': name,
            'time_key': point.time_key,
            'open': point.open if point.HasField('open') else NoneDataType,
            'high': point.high if point.HasField('high') else NoneDataType,
            'low': point.low if point.HasField('low') else NoneDataType,
            'close': point.close if point.HasField('close') else NoneDataType,
            'volume': point.volume if point.HasField('volume') else NoneDataType,
        } for point in item.klineList]
        return kline_list

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        kline_list = []
        for item in rsp_pb.s2c.klineList:
            kline_list.extend(cls._parse_kline_item(item))
        return RET_OK, "", kline_list


class GetEventContractTickerQuery:
    """获取事件合约逐笔"""

    @classmethod
    def pack_req(cls, code, count, conn_id, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_GetEventContractTicker_pb2 import Request
        ret_code, content = split_stock_str(code)
        if ret_code != RET_OK:
            return ret_code, content, None, 0, 0
        market_code, stock_code = content
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if count is not None:
            req.c2s.count = count
        return pack_pb_req(req, ProtoId.Qot_GetEventContractTicker, conn_id)

    @classmethod
    def _parse_ticker_item(cls, item):
        code = merge_qot_mkt_stock_str(item.code.market, item.code.code)
        ticker_list = [{
            'code': code,
            'time': point.time,
            'yes_price': point.yesPrice if point.HasField('yesPrice') else NoneDataType,
            'no_price': point.noPrice if point.HasField('noPrice') else NoneDataType,
            'volume': point.volume if point.HasField('volume') else NoneDataType,
            'side': PredSide.to_string2(point.side) if point.HasField('side') else NoneDataType,
            'sequence': point.sequence if point.HasField('sequence') else NoneDataType,
        } for point in item.tickerList]
        return ticker_list

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ticker_list = []
        for item in rsp_pb.s2c.tickerList:
            ticker_list.extend(cls._parse_ticker_item(item))
        return RET_OK, "", ticker_list


class RequestHistoryEventContractKlQuery:
    """拉取事件合约历史K线"""

    @classmethod
    def pack_req(cls, code, pre_side, kl_type, kline_source, begin_time, end_time,
                 max_ack_kl_num, conn_id, next_req_key, security_firm=SecurityFirm.NONE):
        from ..common.pb.Qot_RequestHistoryEventContractKL_pb2 import Request
        ret_code, content = split_stock_str(code)
        if ret_code != RET_OK:
            return ret_code, content, None, 0, 0
        market_code, stock_code = content
        if not KLType.if_has_key(kl_type):
            error_str = ERROR_STR_PREFIX + "kl_type is %s, which is not valid. (%s)" \
                % (kl_type, KLType.get_all_keys())
            return RET_ERROR, error_str, None, 0, 0
        # EC 具体支持哪些 K 线类型由后端决定，不支持时由后端报错
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if kline_source is not None:
            r, v = ECKlineSource.to_number(kline_source)
            if not r:
                return RET_ERROR, v, None, 0, 0
            req.c2s.klineSource = v
        if pre_side is not None:
            r, v_dir = PredSide.to_number(pre_side)
            if not r:
                return RET_ERROR, v_dir, None, 0, 0
            req.c2s.preSide = v_dir
        _, req.c2s.klType = KLType.to_number(kl_type)
        req.c2s.beginTime = begin_time
        req.c2s.endTime = end_time
        if max_ack_kl_num is not None:
            req.c2s.maxAckKLNum = max_ack_kl_num
        if next_req_key is not None:
            req.c2s.nextReqKey = next_req_key
        return pack_pb_req(req, ProtoId.Qot_RequestHistoryEventContractKL, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        has_next = False
        next_req_key = None
        if rsp_pb.s2c.HasField('nextReqKey'):
            has_next = True
            next_req_key = bytes(rsp_pb.s2c.nextReqKey)

        list_ret = []
        for item in rsp_pb.s2c.klineList:
            list_ret.extend(GetEventContractKlineQuery._parse_kline_item(item))

        return RET_OK, "", (list_ret, has_next, next_req_key)


class EventContractKlinePush:
    """事件合约K线推送"""

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        kline_list = []
        for item in rsp_pb.s2c.klineList:
            kline_list.extend(GetEventContractKlineQuery._parse_kline_item(item))
        return RET_OK, "", kline_list


class EventContractOrderBookPush:
    """事件合约摆盘推送"""

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        order_book_list = GetEventContractOrderBookQuery._parse_order_book_list(rsp_pb)
        return RET_OK, "", order_book_list


class EventContractTickerPush:
    """事件合约逐笔推送"""

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ticker_list = []
        for item in rsp_pb.s2c.tickerList:
            ticker_list.extend(GetEventContractTickerQuery._parse_ticker_item(item))
        return RET_OK, "", ticker_list



