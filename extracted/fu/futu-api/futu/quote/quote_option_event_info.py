# -*- coding: utf-8 -*-
"""
    Option event filter and sort helpers
"""
from ..common.utils import *


class UnderlyingRankFilter(object):
    """标的排行筛选条件

    用法示例:
        # 确切值筛选 — 指定品类为ETF
        f1 = UnderlyingRankFilter(UnderlyingRankIndicatorType.STOCK_CATEGORY, value_list=[StockCategory.ETF])

        # 范围筛选 — IV > 30%
        f2 = UnderlyingRankFilter(UnderlyingRankIndicatorType.IV, interval_min=30.0)

        # 确切值筛选 — 指定标的列表
        f3 = UnderlyingRankFilter(UnderlyingRankIndicatorType.OWNER_LIST, security_list=['US.TSLA', 'US.AAPL'])

    """

    # 确切值筛选时，indicatorType -> 枚举类的映射
    _VALUE_ENUM_MAP = {
        UnderlyingRankIndicatorType.STOCK_CATEGORY: StockCategory,
    }

    def __init__(self, indicator_type=UnderlyingRankIndicatorType.NONE,
                 value_list=None,
                 interval_min=None, interval_max=None,
                 min_inclusive=True, max_inclusive=True,
                 security_list=None):
        self.indicator_type = indicator_type
        self.value_list = value_list
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.security_list = security_list

    def fill_request_pb(self, filter_req):
        """填充 UnderlyingRankIndicator protobuf 消息"""
        if self.indicator_type == UnderlyingRankIndicatorType.NONE:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = UnderlyingRankIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be UnderlyingRankIndicatorType'
        filter_req.indicatorType = v

        # 填充筛选值
        has_value = False

        if self.value_list is not None and len(self.value_list) > 0:
            has_value = True
            enum_cls = self._VALUE_ENUM_MAP.get(self.indicator_type)
            for val in self.value_list:
                if enum_cls is not None and isinstance(val, str):
                    r2, num = enum_cls.to_number(val)
                    if not r2:
                        return RET_ERROR, 'Invalid value in value_list: {}'.format(val)
                    filter_req.indicatorValue.valueList.append(num)
                else:
                    filter_req.indicatorValue.valueList.append(int(val))

        if self.security_list is not None and len(self.security_list) > 0:
            has_value = True
            for stock_str in self.security_list:
                ret_code, content = split_stock_str(stock_str)
                if ret_code != RET_OK:
                    return RET_ERROR, 'Invalid security in security_list: {}'.format(stock_str)
                market_code, stock_code = content
                sec = filter_req.indicatorValue.securityList.add()
                sec.market = market_code
                sec.code = stock_code

        if self.interval_min is not None or self.interval_max is not None:
            has_value = True
            if self.interval_min is not None:
                filter_req.indicatorValue.valueInterval.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.valueInterval.filterMin.includes = self.min_inclusive
            if self.interval_max is not None:
                filter_req.indicatorValue.valueInterval.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.valueInterval.filterMax.includes = self.max_inclusive

        if not has_value:
            return RET_ERROR, 'UnderlyingRankFilter must have at least one value set'

        return RET_OK, ""


class ZeroDteFilter(object):
    """末日期权标的筛选条件

    用法示例:
        # 确切值筛选 — 指定标的列表
        f1 = ZeroDteFilter(ZeroDteIndicatorType.OWNER_LIST, security_list=['US.TSLA', 'US.AAPL'])

        # 确切值筛选 — 本周有财报
        f2 = ZeroDteFilter(ZeroDteIndicatorType.HAS_EARNINGS_THIS_WEEK, value_list=[1])

        # 范围筛选 — IV > 30%
        f3 = ZeroDteFilter(ZeroDteIndicatorType.IV, interval_min=30.0)
    """

    def __init__(self, indicator_type=ZeroDteIndicatorType.UNKNOWN,
                 value_list=None,
                 interval_min=None, interval_max=None,
                 min_inclusive=True, max_inclusive=True,
                 security_list=None):
        self.indicator_type = indicator_type
        self.value_list = value_list
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.security_list = security_list

    def fill_request_pb(self, filter_req):
        """填充 ZeroDteIndicator protobuf 消息"""
        if self.indicator_type == ZeroDteIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = ZeroDteIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be ZeroDteIndicatorType'
        filter_req.indicatorType = v

        has_value = False

        if self.value_list is not None and len(self.value_list) > 0:
            has_value = True
            for val in self.value_list:
                filter_req.indicatorValue.valueList.append(int(val))

        if self.security_list is not None and len(self.security_list) > 0:
            has_value = True
            for stock_str in self.security_list:
                ret_code, content = split_stock_str(stock_str)
                if ret_code != RET_OK:
                    return RET_ERROR, 'Invalid security in security_list: {}'.format(stock_str)
                market_code, stock_code = content
                sec = filter_req.indicatorValue.securityList.add()
                sec.market = market_code
                sec.code = stock_code

        if self.interval_min is not None or self.interval_max is not None:
            has_value = True
            if self.interval_min is not None:
                filter_req.indicatorValue.valueInterval.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.valueInterval.filterMin.includes = self.min_inclusive
            if self.interval_max is not None:
                filter_req.indicatorValue.valueInterval.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.valueInterval.filterMax.includes = self.max_inclusive

        if not has_value:
            return RET_ERROR, 'ZeroDteFilter must have at least one value set'

        return RET_OK, ""


class ZeroDteContractFilter(object):
    """末日期权合约筛选条件

    用法示例:
        # 确切值筛选 — 只看 CALL
        f1 = ZeroDteContractFilter(ZeroDteContractIndicatorType.OPTION_TYPE, value_list=[1])

        # 范围筛选 — Delta 0.3~0.7
        f2 = ZeroDteContractFilter(ZeroDteContractIndicatorType.DELTA, interval_min=0.3, interval_max=0.7)

        # 范围筛选 — 买入盈利概率 > 40%
        f3 = ZeroDteContractFilter(ZeroDteContractIndicatorType.BUY_PROFIT_PROBABILITY, interval_min=40.0)
    """

    def __init__(self, indicator_type=ZeroDteContractIndicatorType.UNKNOWN,
                 value_list=None,
                 interval_min=None, interval_max=None,
                 min_inclusive=True, max_inclusive=True):
        self.indicator_type = indicator_type
        self.value_list = value_list
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def fill_request_pb(self, filter_req):
        """填充 ZeroDteContractIndicator protobuf 消息"""
        if self.indicator_type == ZeroDteContractIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = ZeroDteContractIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be ZeroDteContractIndicatorType'
        filter_req.indicatorType = v

        has_value = False

        if self.value_list is not None and len(self.value_list) > 0:
            has_value = True
            for val in self.value_list:
                filter_req.indicatorValue.valueList.append(int(val))

        if self.interval_min is not None or self.interval_max is not None:
            has_value = True
            if self.interval_min is not None:
                filter_req.indicatorValue.valueInterval.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.valueInterval.filterMin.includes = self.min_inclusive
            if self.interval_max is not None:
                filter_req.indicatorValue.valueInterval.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.valueInterval.filterMax.includes = self.max_inclusive

        if not has_value:
            return RET_ERROR, 'ZeroDteContractFilter must have at least one value set'

        return RET_OK, ""


class OptionRankFilter(object):
    """期权合约排行筛选条件

    用法示例:
        # 确切值筛选 — 指定品类为ETF
        f1 = OptionRankFilter(OptionRankIndicatorType.STOCK_CATEGORY, value_list=[StockCategory.ETF])

        # 范围筛选 — IV > 30%
        f2 = OptionRankFilter(OptionRankIndicatorType.IV, interval_min=30.0)

        # 确切值筛选 — 指定标的列表
        f3 = OptionRankFilter(OptionRankIndicatorType.OWNER_LIST, security_list=['US.TSLA', 'US.AAPL'])

        # 确切值筛选 — 方向为CALL
        f4 = OptionRankFilter(OptionRankIndicatorType.OPTION_TYPE, value_list=[1])

        # 范围筛选 — 距到期日 1~30天
        f5 = OptionRankFilter(OptionRankIndicatorType.LEFT_DAYS, interval_min=1, interval_max=30)
    """

    _VALUE_ENUM_MAP = {
        OptionRankIndicatorType.STOCK_CATEGORY: StockCategory,
    }

    def __init__(self, indicator_type=OptionRankIndicatorType.NONE,
                 value_list=None,
                 interval_min=None, interval_max=None,
                 min_inclusive=True, max_inclusive=True,
                 security_list=None):
        self.indicator_type = indicator_type
        self.value_list = value_list
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.security_list = security_list

    def fill_request_pb(self, filter_req):
        """填充 OptionRankIndicator protobuf 消息"""
        if self.indicator_type == OptionRankIndicatorType.NONE:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = OptionRankIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be OptionRankIndicatorType'
        filter_req.indicatorType = v

        # 填充筛选值
        has_value = False

        if self.value_list is not None and len(self.value_list) > 0:
            has_value = True
            enum_cls = self._VALUE_ENUM_MAP.get(self.indicator_type)
            for val in self.value_list:
                if enum_cls is not None and isinstance(val, str):
                    r2, num = enum_cls.to_number(val)
                    if not r2:
                        return RET_ERROR, 'Invalid value in value_list: {}'.format(val)
                    filter_req.indicatorValue.valueList.append(num)
                else:
                    filter_req.indicatorValue.valueList.append(int(val))

        if self.security_list is not None and len(self.security_list) > 0:
            has_value = True
            for stock_str in self.security_list:
                ret_code, content = split_stock_str(stock_str)
                if ret_code != RET_OK:
                    return RET_ERROR, 'Invalid security in security_list: {}'.format(stock_str)
                market_code, stock_code = content
                sec = filter_req.indicatorValue.securityList.add()
                sec.market = market_code
                sec.code = stock_code

        if self.interval_min is not None or self.interval_max is not None:
            has_value = True
            if self.interval_min is not None:
                filter_req.indicatorValue.valueInterval.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.valueInterval.filterMin.includes = self.min_inclusive
            if self.interval_max is not None:
                filter_req.indicatorValue.valueInterval.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.valueInterval.filterMax.includes = self.max_inclusive

        if not has_value:
            return RET_ERROR, 'OptionRankFilter must have at least one value set'

        return RET_OK, ""


class EarningsFilter(object):
    """财报机会筛选条件

    用法示例:
        # 确切值筛选 — 指定标的列表
        f2 = EarningsFilter(EarningsIndicatorType.OWNER_LIST, security_list=['US.TSLA', 'US.AAPL'])

        # 范围筛选 — IV > 30%
        f3 = EarningsFilter(EarningsIndicatorType.IV, interval_min=30.0)

        # 范围筛选 — 距财报日 1~7天
        f4 = EarningsFilter(EarningsIndicatorType.EARNINGS_DAY_RANGE, interval_min=1, interval_max=7)
    """

    _VALUE_ENUM_MAP = {
    }

    def __init__(self, indicator_type=EarningsIndicatorType.UNKNOWN,
                 value_list=None,
                 interval_min=None, interval_max=None,
                 min_inclusive=True, max_inclusive=True,
                 security_list=None):
        self.indicator_type = indicator_type
        self.value_list = value_list
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.security_list = security_list

    def fill_request_pb(self, filter_req):
        """填充 EarningsIndicator protobuf 消息"""
        if self.indicator_type == EarningsIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = EarningsIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be EarningsIndicatorType'
        filter_req.indicatorType = v

        has_value = False

        if self.value_list is not None and len(self.value_list) > 0:
            has_value = True
            enum_cls = self._VALUE_ENUM_MAP.get(self.indicator_type)
            for val in self.value_list:
                if enum_cls is not None and isinstance(val, str):
                    r2, num = enum_cls.to_number(val)
                    if not r2:
                        return RET_ERROR, 'Invalid value in value_list: {}'.format(val)
                    filter_req.indicatorValue.valueList.append(num)
                else:
                    filter_req.indicatorValue.valueList.append(int(val))

        if self.security_list is not None and len(self.security_list) > 0:
            has_value = True
            for stock_str in self.security_list:
                ret_code, content = split_stock_str(stock_str)
                if ret_code != RET_OK:
                    return RET_ERROR, 'Invalid security in security_list: {}'.format(stock_str)
                market_code, stock_code = content
                sec = filter_req.indicatorValue.securityList.add()
                sec.market = market_code
                sec.code = stock_code

        if self.interval_min is not None or self.interval_max is not None:
            has_value = True
            if self.interval_min is not None:
                filter_req.indicatorValue.valueInterval.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.valueInterval.filterMin.includes = self.min_inclusive
            if self.interval_max is not None:
                filter_req.indicatorValue.valueInterval.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.valueInterval.filterMax.includes = self.max_inclusive

        if not has_value:
            return RET_ERROR, 'EarningsFilter must have at least one value set'

        return RET_OK, ""


class SellerFilter(object):
    """卖方专区筛选条件

    用法示例:
        # 确切值筛选 — 指定品类为ETF
        f1 = SellerFilter(SellerIndicatorType.STOCK_CATEGORY, value_list=[StockCategory.ETF])

        # 确切值筛选 — 指定标的列表
        f2 = SellerFilter(SellerIndicatorType.OWNER_LIST, security_list=['US.TSLA', 'US.AAPL'])

        # 范围筛选 — 年化收益率 > 20%
        f3 = SellerFilter(SellerIndicatorType.ANNUALIZED_RETURN, interval_min=20.0)

        # 确切值筛选 — 方向为CALL
        f4 = SellerFilter(SellerIndicatorType.OPTION_TYPE, value_list=[1])

        # 范围筛选 — 距到期日 1~30天
        f5 = SellerFilter(SellerIndicatorType.LEFT_DAYS, interval_min=1, interval_max=30)
    """

    _VALUE_ENUM_MAP = {
        SellerIndicatorType.STOCK_CATEGORY: StockCategory,
    }

    def __init__(self, indicator_type=SellerIndicatorType.UNKNOWN,
                 value_list=None,
                 interval_min=None, interval_max=None,
                 min_inclusive=True, max_inclusive=True,
                 security_list=None):
        self.indicator_type = indicator_type
        self.value_list = value_list
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.security_list = security_list

    def fill_request_pb(self, filter_req):
        """填充 SellerIndicator protobuf 消息"""
        if self.indicator_type == SellerIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = SellerIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be SellerIndicatorType'
        filter_req.indicatorType = v

        has_value = False

        if self.value_list is not None and len(self.value_list) > 0:
            has_value = True
            enum_cls = self._VALUE_ENUM_MAP.get(self.indicator_type)
            for val in self.value_list:
                if enum_cls is not None and isinstance(val, str):
                    r2, num = enum_cls.to_number(val)
                    if not r2:
                        return RET_ERROR, 'Invalid value in value_list: {}'.format(val)
                    filter_req.indicatorValue.valueList.append(num)
                else:
                    filter_req.indicatorValue.valueList.append(int(val))

        if self.security_list is not None and len(self.security_list) > 0:
            has_value = True
            for stock_str in self.security_list:
                ret_code, content = split_stock_str(stock_str)
                if ret_code != RET_OK:
                    return RET_ERROR, 'Invalid security in security_list: {}'.format(stock_str)
                market_code, stock_code = content
                sec = filter_req.indicatorValue.securityList.add()
                sec.market = market_code
                sec.code = stock_code

        if self.interval_min is not None or self.interval_max is not None:
            has_value = True
            if self.interval_min is not None:
                filter_req.indicatorValue.valueInterval.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.valueInterval.filterMin.includes = self.min_inclusive
            if self.interval_max is not None:
                filter_req.indicatorValue.valueInterval.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.valueInterval.filterMax.includes = self.max_inclusive

        if not has_value:
            return RET_ERROR, 'SellerFilter must have at least one value set'

        return RET_OK, ""


class EarningsCalendarFilter(object):
    """财报日历筛选条件

    用法示例:
        # 确切值筛选 — 盘前发布
        f1 = EarningsCalendarFilter(EarningsCalendarIndicatorType.PUB_TYPE, value_list=[EarningsCalendarPubType.BEFORE])

        # 确切值筛选 — 股票列表类型(自选股)
        f2 = EarningsCalendarFilter(EarningsCalendarIndicatorType.STOCK_LIST_TYPE, value_list=[EarningsCalendarStockListType.WATCHLIST])

        # 范围筛选 — 市值 > 1000000000
        f3 = EarningsCalendarFilter(EarningsCalendarIndicatorType.MARKET_CAP, interval_min=1000000000)
    """

    _VALUE_ENUM_MAP = {
        EarningsCalendarIndicatorType.PUB_TYPE: EarningsCalendarPubType,
        EarningsCalendarIndicatorType.ESTIMATE_TYPE: EarningsCalendarEstimateType,
        EarningsCalendarIndicatorType.STOCK_LIST_TYPE: EarningsCalendarStockListType,
    }

    def __init__(self, indicator_type=EarningsCalendarIndicatorType.UNKNOWN,
                 value_list=None,
                 interval_min=None, interval_max=None,
                 min_inclusive=True, max_inclusive=True):
        self.indicator_type = indicator_type
        self.value_list = value_list
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def fill_request_pb(self, filter_req):
        """填充 EarningsCalendarIndicator protobuf 消息"""
        if self.indicator_type == EarningsCalendarIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = EarningsCalendarIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be EarningsCalendarIndicatorType'
        filter_req.indicatorType = v

        has_value = False

        if self.value_list is not None and len(self.value_list) > 0:
            has_value = True
            enum_cls = self._VALUE_ENUM_MAP.get(self.indicator_type)
            for val in self.value_list:
                if enum_cls is not None and isinstance(val, str):
                    r2, num = enum_cls.to_number(val)
                    if not r2:
                        return RET_ERROR, 'Invalid value in value_list: {}'.format(val)
                    filter_req.indicatorValue.valueList.append(num)
                else:
                    filter_req.indicatorValue.valueList.append(int(val))

        if self.interval_min is not None or self.interval_max is not None:
            has_value = True
            if self.interval_min is not None:
                filter_req.indicatorValue.valueInterval.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.valueInterval.filterMin.includes = self.min_inclusive
            if self.interval_max is not None:
                filter_req.indicatorValue.valueInterval.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.valueInterval.filterMax.includes = self.max_inclusive

        if not has_value:
            return RET_ERROR, 'EarningsCalendarFilter must have at least one value set'

        return RET_OK, ""


class OptionEventFilter(object):
    """期权异动筛选条件

    用法示例:
        # 确切值筛选 — CALL期权
        f1 = OptionEventFilter(EventIndicatorType.OPTION_TYPE, value_list=[1])

        # 范围筛选 — 成交额 > 100000
        f2 = OptionEventFilter(EventIndicatorType.TURNOVER, interval_min=100000.0)

        # 范围筛选 — Delta 0.3 ~ 0.7
        f3 = OptionEventFilter(EventIndicatorType.DELTA, interval_min=0.3, interval_max=0.7)

        # 确切值筛选 — 指定标的列表
        f4 = OptionEventFilter(EventIndicatorType.OWNER_LIST, security_list=['US.TSLA', 'US.AAPL'])

        # 确切值筛选 — 行业板块列表
        f5 = OptionEventFilter(EventIndicatorType.INDUSTRY_PLATE, security_list=['US.BK1001', 'US.BK1002'])
    """

    def __init__(self, indicator_type=EventIndicatorType.NONE,
                 value_list=None,
                 interval_min=None, interval_max=None,
                 min_inclusive=True, max_inclusive=True,
                 string_value_list=None,
                 security_list=None):
        self.indicator_type = indicator_type
        self.value_list = value_list
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.string_value_list = string_value_list
        self.security_list = security_list

    def fill_request_pb(self, filter_req):
        """填充 EventIndicator protobuf 消息"""
        if self.indicator_type == EventIndicatorType.NONE:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = EventIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be EventIndicatorType'
        filter_req.indicatorType = v

        # 填充筛选值
        has_value = False

        if self.value_list is not None and len(self.value_list) > 0:
            has_value = True
            for val in self.value_list:
                filter_req.indicatorValue.valueList.append(int(val))

        if self.string_value_list is not None and len(self.string_value_list) > 0:
            has_value = True
            for val in self.string_value_list:
                filter_req.indicatorValue.stringValueList.append(str(val))

        if self.security_list is not None and len(self.security_list) > 0:
            has_value = True
            for stock_str in self.security_list:
                ret_code, content = split_stock_str(stock_str)
                if ret_code != RET_OK:
                    return RET_ERROR, 'Invalid security in security_list: {}'.format(stock_str)
                market_code, stock_code = content
                sec = filter_req.indicatorValue.securityList.add()
                sec.market = market_code
                sec.code = stock_code

        if self.interval_min is not None or self.interval_max is not None:
            has_value = True
            if self.interval_min is not None:
                filter_req.indicatorValue.valueInterval.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.valueInterval.filterMin.includes = self.min_inclusive
            if self.interval_max is not None:
                filter_req.indicatorValue.valueInterval.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.valueInterval.filterMax.includes = self.max_inclusive

        if not has_value:
            return RET_ERROR, 'OptionEventFilter must have at least one value set'

        return RET_OK, ""


class OptionEventSort(object):
    """期权异动排序条件

    用法示例:
        # 按成交额降序
        sort = OptionEventSort(EventIndicatorType.TURNOVER, EventSortDir.DESCEND)

        # 按时间升序
        sort = OptionEventSort(EventIndicatorType.TIME, EventSortDir.ASCEND)
    """

    def __init__(self, indicator_type=EventIndicatorType.NONE, sort_dir=EventSortDir.DESCEND):
        self.indicator_type = indicator_type
        self.sort_dir = sort_dir

    def fill_request_pb(self, sort_req):
        """填充 EventSort protobuf 消息"""
        if self.indicator_type == EventIndicatorType.NONE:
            return RET_ERROR, 'Missing necessary parameter: indicator_type for sort'

        r, v = EventIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be EventIndicatorType'
        sort_req.indicatorType = v

        r2, v2 = EventSortDir.to_number(self.sort_dir)
        if not r2:
            return RET_ERROR, 'sort_dir is wrong. It must be EventSortDir'
        sort_req.isAsc = v2

        return RET_OK, ""


class OptionEventAlertItem(object):
    """期权异动提醒条件项

    用法示例:
        # 新增一个提醒（按市场）
        item = OptionEventAlertItem(
            option_market=OptionMarket.US_SECURITY,
            option_type=OptionType.CALL,
            order_type_list=[AlertOrderType.SWEEP],
            size_range_min=100,
        )

        # 新增一个提醒（按标的）
        item = OptionEventAlertItem(
            underlying='US.AAPL',
            side_type_list=[EventTickerType.BUY],
        )

        # 修改现有提醒（需传入 key）
        item = OptionEventAlertItem(key=12345, enable=True, note='updated')
    """

    def __init__(self, key=None, enable=None, option_market=None,
                 watchlist_group_name=None, underlying=None,
                 option_type=None, side_type_list=None, order_type_list=None,
                 market_cap_range_min=None, market_cap_range_max=None,
                 expiry_days_range_min=None, expiry_days_range_max=None,
                 price_range_min=None, price_range_max=None,
                 size_range_min=None, size_range_max=None,
                 premium_range_min=None, premium_range_max=None,
                 iv_range_min=None, iv_range_max=None,
                 market_cap_min_inclusive=True, market_cap_max_inclusive=True,
                 expiry_days_min_inclusive=True, expiry_days_max_inclusive=True,
                 price_min_inclusive=True, price_max_inclusive=True,
                 size_min_inclusive=True, size_max_inclusive=True,
                 premium_min_inclusive=True, premium_max_inclusive=True,
                 iv_min_inclusive=True, iv_max_inclusive=True,
                 earnings_date_begin=None, earnings_date_end=None, note=None):
        self.key = key
        self.enable = enable
        self.option_market = option_market
        self.watchlist_group_name = watchlist_group_name
        self.underlying = underlying
        self.option_type = option_type
        self.side_type_list = side_type_list
        self.order_type_list = order_type_list
        self.market_cap_range_min = market_cap_range_min
        self.market_cap_range_max = market_cap_range_max
        self.expiry_days_range_min = expiry_days_range_min
        self.expiry_days_range_max = expiry_days_range_max
        self.price_range_min = price_range_min
        self.price_range_max = price_range_max
        self.size_range_min = size_range_min
        self.size_range_max = size_range_max
        self.premium_range_min = premium_range_min
        self.premium_range_max = premium_range_max
        self.iv_range_min = iv_range_min
        self.iv_range_max = iv_range_max
        self.market_cap_min_inclusive = market_cap_min_inclusive
        self.market_cap_max_inclusive = market_cap_max_inclusive
        self.expiry_days_min_inclusive = expiry_days_min_inclusive
        self.expiry_days_max_inclusive = expiry_days_max_inclusive
        self.price_min_inclusive = price_min_inclusive
        self.price_max_inclusive = price_max_inclusive
        self.size_min_inclusive = size_min_inclusive
        self.size_max_inclusive = size_max_inclusive
        self.premium_min_inclusive = premium_min_inclusive
        self.premium_max_inclusive = premium_max_inclusive
        self.iv_min_inclusive = iv_min_inclusive
        self.iv_max_inclusive = iv_max_inclusive
        self.earnings_date_begin = earnings_date_begin
        self.earnings_date_end = earnings_date_end
        self.note = note

    def fill_request_pb(self, pb_item):
        """填充 EventAlertItem protobuf 消息"""
        if self.key is not None:
            pb_item.key = int(self.key)
        if self.enable is not None:
            pb_item.enable = bool(self.enable)
        if self.option_market is not None:
            r, v = OptionMarket.to_number(self.option_market)
            if not r:
                return RET_ERROR, 'option_market is wrong. It must be OptionMarket'
            pb_item.optionMarket = v
        if self.watchlist_group_name is not None:
            pb_item.watchlistGroupName = str(self.watchlist_group_name)
        if self.underlying is not None:
            ret_code, content = split_stock_str(self.underlying)
            if ret_code != RET_OK:
                return RET_ERROR, 'Invalid underlying: {}'.format(self.underlying)
            market_code, stock_code = content
            pb_item.underlying.market = market_code
            pb_item.underlying.code = stock_code
        if self.option_type is not None:
            r, v = OptionType.to_number(self.option_type)
            if not r:
                return RET_ERROR, 'option_type is wrong. It must be OptionType'
            pb_item.optionType = v
        if self.side_type_list is not None:
            for side in self.side_type_list:
                r, v = EventTickerType.to_number(side)
                if not r:
                    return RET_ERROR, 'side_type_list item is wrong. It must be EventTickerType'
                pb_item.sideTypeList.append(v)
        if self.order_type_list is not None:
            for ot in self.order_type_list:
                r, v = AlertOrderType.to_number(ot)
                if not r:
                    return RET_ERROR, 'order_type_list item is wrong. It must be AlertOrderType'
                pb_item.orderTypeList.append(v)
        # Interval range fields
        self._fill_interval(pb_item.marketCapRange, self.market_cap_range_min, self.market_cap_range_max,
                            self.market_cap_min_inclusive, self.market_cap_max_inclusive)
        self._fill_interval(pb_item.expiryDaysRange, self.expiry_days_range_min, self.expiry_days_range_max,
                            self.expiry_days_min_inclusive, self.expiry_days_max_inclusive)
        self._fill_interval(pb_item.priceRange, self.price_range_min, self.price_range_max,
                            self.price_min_inclusive, self.price_max_inclusive)
        self._fill_interval(pb_item.sizeRange, self.size_range_min, self.size_range_max,
                            self.size_min_inclusive, self.size_max_inclusive)
        self._fill_interval(pb_item.premiumRange, self.premium_range_min, self.premium_range_max,
                            self.premium_min_inclusive, self.premium_max_inclusive)
        self._fill_interval(pb_item.ivRange, self.iv_range_min, self.iv_range_max,
                            self.iv_min_inclusive, self.iv_max_inclusive)
        if self.earnings_date_begin is not None:
            pb_item.earningsDateBegin = str(self.earnings_date_begin)
        if self.earnings_date_end is not None:
            pb_item.earningsDateEnd = str(self.earnings_date_end)
        if self.note is not None:
            pb_item.note = str(self.note)

        return RET_OK, ""

    def _fill_interval(self, interval_pb, min_val, max_val, min_incl=True, max_incl=True):
        """Fill an Interval protobuf message."""
        if min_val is not None:
            interval_pb.filterMin.value = float(min_val)
            interval_pb.filterMin.includes = min_incl
        if max_val is not None:
            interval_pb.filterMax.value = float(max_val)
            interval_pb.filterMax.includes = max_incl
            

class EarningsBeatRankFilter(object):
    """盈利超预期排名筛选条件

    用法示例:
        # 超预期比率 > 0
        f1 = EarningsBeatRankFilter(EarningsBeatIndicatorType.BEAT_RATIO, interval_min=0)

        # 市值 > 10亿
        f2 = EarningsBeatRankFilter(EarningsBeatIndicatorType.MARKET_CAP, interval_min=1000000000)
    """

    def __init__(self, indicator_type=EarningsBeatIndicatorType.UNKNOWN,
                 interval_min=None, interval_max=None):
        self.indicator_type = indicator_type
        self.interval_min = interval_min
        self.interval_max = interval_max

    def fill_request_pb(self, filter_req):
        """填充 Indicator protobuf 消息"""
        if self.indicator_type == EarningsBeatIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = EarningsBeatIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be EarningsBeatIndicatorType'
        filter_req.indicatorType = v

        if self.interval_min is None and self.interval_max is None:
            return RET_ERROR, 'EarningsBeatRankFilter must have at least one interval value set'

        if self.interval_min is not None:
            filter_req.indicatorValue.filterMin.value = float(self.interval_min)
            filter_req.indicatorValue.filterMin.includes = True
        if self.interval_max is not None:
            filter_req.indicatorValue.filterMax.value = float(self.interval_max)
            filter_req.indicatorValue.filterMax.includes = True

        return RET_OK, ""


class DividendRankFilter(object):
    """股息排行筛选条件

    用法示例:
        # 股息率TTM > 3%
        f1 = DividendRankFilter(DividendRankIndicatorType.DIVIDEND_YIELD_TTM, interval_min=3)

        # 市值 > 10亿
        f2 = DividendRankFilter(DividendRankIndicatorType.MARKET_CAP, interval_min=1000000000)

        # 派息频率为季派或月派
        f3 = DividendRankFilter(DividendRankIndicatorType.DISTRIBUTION_FREQUENCY,
                                value_list=[DistributionFrequency.QUARTERLY, DistributionFrequency.MONTHLY])
    """

    _VALUE_ENUM_MAP = {
        DividendRankIndicatorType.DISTRIBUTION_FREQUENCY: DistributionFrequency,
    }

    def __init__(self, indicator_type=DividendRankIndicatorType.UNKNOWN,
                 value_list=None,
                 interval_min=None, interval_max=None,
                 min_inclusive=True, max_inclusive=True):
        self.indicator_type = indicator_type
        self.value_list = value_list
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def fill_request_pb(self, filter_req):
        """填充 Indicator protobuf 消息"""
        if self.indicator_type == DividendRankIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = DividendRankIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be DividendRankIndicatorType'
        filter_req.indicatorType = v

        has_value = False

        if self.value_list is not None and len(self.value_list) > 0:
            has_value = True
            enum_cls = self._VALUE_ENUM_MAP.get(self.indicator_type)
            for val in self.value_list:
                if enum_cls is not None and isinstance(val, str):
                    r2, num = enum_cls.to_number(val)
                    if not r2:
                        return RET_ERROR, 'Invalid value in value_list: {}'.format(val)
                    filter_req.indicatorValue.valueList.append(num)
                else:
                    filter_req.indicatorValue.valueList.append(int(val))

        if self.interval_min is not None or self.interval_max is not None:
            has_value = True
            if self.interval_min is not None:
                filter_req.indicatorValue.valueInterval.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.valueInterval.filterMin.includes = self.min_inclusive
            if self.interval_max is not None:
                filter_req.indicatorValue.valueInterval.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.valueInterval.filterMax.includes = self.max_inclusive

        if not has_value:
            return RET_ERROR, 'DividendRankFilter must have value_list or interval set'

        return RET_OK, ""


class SimpleRankFilter(object):
    """盘前/盘后/夜盘/领涨榜通用筛选条件

    用法示例:
        # 市值 > 10亿
        f = SimpleRankFilter(SimpleRankIndicatorType.MARKET_CAP, interval_min=1000000000)
        # 价格筛选: 10~100之间
        f = SimpleRankFilter(SimpleRankIndicatorType.PRICE, price_filter=PriceFilter.BETWEEN_10_AND_100)
    """

    def __init__(self, indicator_type=SimpleRankIndicatorType.UNKNOWN,
                 interval_min=None, interval_max=None, price_filter=None):
        self.indicator_type = indicator_type
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.price_filter = price_filter

    def fill_request_pb(self, filter_req):
        if self.indicator_type == SimpleRankIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = SimpleRankIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be SimpleRankIndicatorType'
        filter_req.indicatorType = v

        if self.indicator_type == SimpleRankIndicatorType.PRICE:
            if self.price_filter is None:
                return RET_ERROR, 'SimpleRankFilter with PRICE type must set price_filter'
            r, pv = PriceFilter.to_number(self.price_filter)
            if not r:
                return RET_ERROR, 'price_filter is wrong. It must be PriceFilter'
            filter_req.priceFilter = pv
        else:
            if self.interval_min is None and self.interval_max is None:
                return RET_ERROR, 'SimpleRankFilter must have at least one interval value set'

            if self.interval_min is not None:
                filter_req.indicatorValue.filterMin.value = float(self.interval_min)
                filter_req.indicatorValue.filterMin.includes = True
            if self.interval_max is not None:
                filter_req.indicatorValue.filterMax.value = float(self.interval_max)
                filter_req.indicatorValue.filterMax.includes = True

        return RET_OK, ""


class HotListFilter(object):
    """热议榜筛选条件

    用法示例:
        # 市值 > 100亿
        f = HotListFilter(HotListIndicatorType.MARKET_CAP, interval_min=10000000000)
    """

    def __init__(self, indicator_type=HotListIndicatorType.UNKNOWN,
                 interval_min=None, interval_max=None):
        self.indicator_type = indicator_type
        self.interval_min = interval_min
        self.interval_max = interval_max

    def fill_request_pb(self, filter_req):
        if self.indicator_type == HotListIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = HotListIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be HotListIndicatorType'
        filter_req.indicatorType = v

        if self.interval_min is None and self.interval_max is None:
            return RET_ERROR, 'HotListFilter must have at least one interval value set'

        if self.interval_min is not None:
            filter_req.indicatorValue.filterMin.value = float(self.interval_min)
            filter_req.indicatorValue.filterMin.includes = True
        if self.interval_max is not None:
            filter_req.indicatorValue.filterMax.value = float(self.interval_max)
            filter_req.indicatorValue.filterMax.includes = True

        return RET_OK, ""


class PeriodChangeRankFilter(object):
    """区间涨跌幅筛选条件

    用法示例:
        # 市值 > 10亿
        f1 = PeriodChangeRankFilter(PeriodChangeIndicatorType.MARKET_CAP, interval_min=1000000000)
        # 换手率 > 1%
        f2 = PeriodChangeRankFilter(PeriodChangeIndicatorType.TURNOVER_RATIO, interval_min=1)
    """

    def __init__(self, indicator_type=PeriodChangeIndicatorType.UNKNOWN,
                 interval_min=None, interval_max=None):
        self.indicator_type = indicator_type
        self.interval_min = interval_min
        self.interval_max = interval_max

    def fill_request_pb(self, filter_req):
        if self.indicator_type == PeriodChangeIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = PeriodChangeIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be PeriodChangeIndicatorType'
        filter_req.indicatorType = v

        if self.interval_min is None and self.interval_max is None:
            return RET_ERROR, 'PeriodChangeRankFilter must have at least one interval value set'

        if self.interval_min is not None:
            filter_req.indicatorValue.filterMin.value = float(self.interval_min)
            filter_req.indicatorValue.filterMin.includes = True
        if self.interval_max is not None:
            filter_req.indicatorValue.filterMax.value = float(self.interval_max)
            filter_req.indicatorValue.filterMax.includes = True

        return RET_OK, ""


class HighDividendSOERankFilter(object):
    """破净高股息国央企筛选条件

    用法示例:
        # 股息率TTM >= 6%
        f = HighDividendSOERankFilter(HighDividendSOEIndicatorType.DIVIDEND_YIELD_TTM, interval_min=6)
    """

    def __init__(self, indicator_type=HighDividendSOEIndicatorType.UNKNOWN,
                 interval_min=None, interval_max=None):
        self.indicator_type = indicator_type
        self.interval_min = interval_min
        self.interval_max = interval_max

    def fill_request_pb(self, filter_req):
        if self.indicator_type == HighDividendSOEIndicatorType.UNKNOWN:
            return RET_ERROR, 'Missing necessary parameter: indicator_type'

        r, v = HighDividendSOEIndicatorType.to_number(self.indicator_type)
        if not r:
            return RET_ERROR, 'indicator_type is wrong. It must be HighDividendSOEIndicatorType'
        filter_req.indicatorType = v

        if self.interval_min is None and self.interval_max is None:
            return RET_ERROR, 'HighDividendSOERankFilter must have at least one interval value set'

        if self.interval_min is not None:
            filter_req.indicatorValue.filterMin.value = float(self.interval_min)
            filter_req.indicatorValue.filterMin.includes = True
        if self.interval_max is not None:
            filter_req.indicatorValue.filterMax.value = float(self.interval_max)
            filter_req.indicatorValue.filterMax.includes = True

        return RET_OK, ""
