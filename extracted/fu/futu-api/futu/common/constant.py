# -*- coding: utf-8 -*-
"""
    Constant collection
"""
from .pb import Qot_GetCodeChange_pb2
from .pb import Qot_StockFilter_pb2
from .pb import Qot_ModifyUserSecurity_pb2
from .pb import GetDelayStatistics_pb2
from .pb import GetUserInfo_pb2
from .pb import Common_pb2
from .pb import Notify_pb2
from .pb import Verification_pb2
from .pb import Qot_GetReference_pb2
from .pb import Qot_Common_pb2
from .pb import Qot_GetSearchNews_pb2
from .pb import Trd_Common_pb2
from .pb import Qot_SetPriceReminder_pb2
from .pb import Qot_UpdatePriceReminder_pb2
from .pb import Qot_GetUserSecurityGroup_pb2
from .pb import Qot_GetOptionChain_pb2
from .pb import Qot_OptionCommon_pb2
from .pb import Qot_GetOptionEvent_pb2
from .pb import Qot_GetOptionEventAlert_pb2
from .pb import Qot_SetOptionEventAlert_pb2
from .pb import Qot_UpdateOptionEvent_pb2
from .pb import Qot_GetEarningsCalendar_pb2
from .pb import Qot_GetMacroIndicatorList_pb2
from .pb import Qot_GetMacroIndicatorHistory_pb2
from .pb import Qot_GetEarningsBeatRank_pb2
from .pb import Qot_GetDividendRank_pb2
from .pb import Qot_GetDividendCalendar_pb2
from .pb import Qot_GetEconomicCalendar_pb2
from .pb import Qot_GetUSPreMarketRank_pb2
from .pb import Qot_GetUSAfterHoursRank_pb2
from .pb import Qot_GetUSOvernightRank_pb2
from .pb import Qot_GetTopMoversRank_pb2
from .pb import Qot_GetHotList_pb2
from .pb import Qot_GetShortSellingRank_pb2
from .pb import Qot_GetPeriodChangeRank_pb2
from .pb import Qot_GetHighDividendSOERank_pb2
from .pb import Qot_GetInstitutionList_pb2
from .pb import Qot_GetInstitutionProfile_pb2
from .pb import Qot_GetInstitutionDistribution_pb2
from .pb import Qot_GetInstitutionHoldingChange_pb2
from .pb import Qot_GetInstitutionHoldingList_pb2
from .pb import Qot_GetArkFundHolding_pb2
from .pb import Qot_GetArkStockDynamic_pb2
from .pb import Qot_GetArkActiveTransaction_pb2
from .pb import Qot_GetRatingChange_pb2
from .pb import Qot_GetIndustrialChainList_pb2
from .pb import Qot_GetIndustrialChainDetail_pb2
from .pb import Qot_GetIndustrialChainByPlate_pb2
from .pb import Qot_GetIndustrialPlateInfo_pb2
from .pb import Qot_GetIndustrialPlateStock_pb2
from .pb import Qot_GetHeatMapData_pb2
from .pb import Qot_GetRiseFallDistribution_pb2
from .pb import Trd_FlowSummary_pb2
from copy import copy
from abc import abstractmethod

class ProtoId(object):
    InitConnect = 1001  # 初始化连接
    GetGlobalState = 1002  # 获取全局状态
    Notify = 1003  # 通知推送
    KeepAlive = 1004  # 心跳保活
    GetUserInfo = 1005  # 获取用户信息
    Verification = 1006  # 请求或输入验证码
    GetDelayStatistics = 1007  # 获取延迟统计
    TestCmd = 1008
    InitQuantMode = 1009

    Trd_GetAccList = 2001  # 获取业务账户列表
    Trd_UnlockTrade = 2005  # 解锁或锁定交易
    Trd_SubAccPush = 2008  # 订阅业务账户的交易推送数据

    Trd_GetFunds = 2101  # 获取账户资金
    Trd_GetPositionList = 2102  # 获取账户持仓

    Trd_GetOrderList = 2201  # 获取订单列表
    Trd_PlaceOrder = 2202  # 下单
    Trd_ModifyOrder = 2205  # 修改订单
    Trd_UpdateOrder = 2208  # 订单状态变动通知(推送)

    Trd_GetOrderFillList = 2211  # 获取成交列表
    Trd_UpdateOrderFill = 2218  # 成交通知(推送)

    Trd_GetHistoryOrderList = 2221  # 获取历史订单列表
    Trd_GetHistoryOrderFillList = 2222  # 获取历史成交列表
    Trd_GetMaxTrdQtys = 2111    # 查询最大买卖数量
    Trd_GetComboMaxTrdQtys = 2112    # 获取组合的可买卖信息
    Trd_GetMarginRatio = 2223  # 获取融资融券数据
    Trd_GetOrderFee = 2225  # 获取订单费用
    Trd_FlowSummary = 2226  # 获取现金流水
    Trd_PlaceComboOrder = 2227  # 组合期权下单

    # 订阅数据
    Qot_Sub = 3001  # 订阅或者反订阅
    Qot_RegQotPush = 3002  # 注册推送
    Qot_GetSubInfo = 3003  # 获取订阅信息
    Qot_GetBasicQot = 3004  # 获取股票基本行情
    Qot_UpdateBasicQot = 3005  # 推送股票基本行情
    Qot_GetKL = 3006  # 获取K线
    Qot_UpdateKL = 3007  # 推送K线
    Qot_GetRT = 3008  # 获取分时
    Qot_UpdateRT = 3009  # 推送分时
    Qot_GetTicker = 3010  # 获取逐笔
    Qot_UpdateTicker = 3011  # 推送逐笔
    Qot_GetOrderBook = 3012  # 获取买卖盘
    Qot_UpdateOrderBook = 3013  # 推送买卖盘
    Qot_GetBroker = 3014  # 获取经纪队列
    Qot_UpdateBroker = 3015  # 推送经纪队列
    Qot_UpdatePriceReminder = 3019 #到价提醒通知

    # 历史数据
    Qot_RequestHistoryKL = 3103  # 拉取历史K线
    Qot_RequestHistoryKLQuota = 3104  # 拉取历史K线已经用掉的额度
    Qot_RequestRehab = 3105  # 获取除权信息

    # 其他行情数据
    Qot_GetSuspend = 3201           # 获取股票停牌信息
    Qot_GetStaticInfo = 3202        # 获取股票列表
    Qot_GetSecuritySnapshot = 3203  # 获取股票快照
    Qot_GetPlateSet = 3204          # 获取板块集合下的板块
    Qot_GetPlateSecurity = 3205     # 获取板块下的股票
    Qot_GetReference = 3206         # 获取正股相关股票，暂时只有窝轮
    Qot_GetOwnerPlate = 3207        # 获取股票所属板块
    Qot_GetHoldingChangeList = 3208     # 获取高管持股变动
    Qot_GetOptionChain = 3209           # 获取期权链

    Qot_GetWarrant = 3210          # 拉取窝轮信息
    Qot_GetCapitalFlow = 3211          # 获取资金流向
    Qot_GetCapitalDistribution = 3212  # 获取资金分布

    Qot_GetUserSecurity = 3213  # 获取自选股分组下的股票
    Qot_ModifyUserSecurity = 3214  # 修改自选股分组下的股票
    Qot_StockFilter = 3215   # 条件选股
    Qot_GetCodeChange = 3216   # 代码变换
    Qot_GetIpoList = 3217  # 获取新股Ipo
    Qot_GetFutureInfo = 3218  # 获取期货资料
    Qot_RequestTradeDate = 3219  # 在线拉取交易日
    Qot_SetPriceReminder = 3220  # 设置到价提醒
    Qot_GetPriceReminder = 3221  # 获取到价提醒

    Qot_GetUserSecurityGroup = 3222  # 获取自选股分组
    Qot_GetMarketState = 3223  # 获取指定品种的市场状态
    Qot_GetOptionExpirationDate = 3224  # 获取期权到期日
    Qot_GetFinancialsEarningsPriceMove = 3225         # 获取个股财报日前后价格涨跌幅表现（F10）
    Qot_GetFinancialsEarningsPriceHistory = 3226      # 获取个股财报日前后股价历史（F10）
    Qot_GetFinancialsStatements = 3227                # 获取财务报表
    Qot_GetFinancialsRevenueBreakdown = 3228          # 获取主营构成
    Qot_GetResearchAnalystConsensus = 3229            # 获取分析师评级概述（F10）
    Qot_GetResearchRatingSummary = 3230               # 获取评级汇总（F10）
    Qot_GetResearchMorningstarReport = 3231           # 获取晨星研究报告（F10）
    Qot_GetValuationDetail = 3232                     # 获取个股估值详情
    Qot_GetValuationPlateStockList = 3233             # 获取板块/指数成分股估值
    Qot_GetCorporateActionsDividends = 3234           # 获取分红派息
    Qot_GetCorporateActionsBuybacks = 3235            # 获取回购
    Qot_GetCorporateActionsStockSplits = 3236         # 获取拆合股（支持港股及非港股）
    Qot_GetShareholdersOverview = 3237                # 获取持股统计（F10）
    Qot_GetShareholdersHoldingChanges = 3238          # 获取持股变动（F10）
    Qot_GetShareholdersHolderDetail = 3239            # 获取持股明细（F10）
    Qot_GetShareholdersInstitutional = 3240           # 获取机构持股（F10）
    Qot_GetInsiderHolderList = 3241                   # 获取内部人持股列表（F10）
    Qot_GetInsiderTradeList = 3242                    # 获取内部人交易列表（F10）
    Qot_GetCompanyProfile = 3243                      # 获取公司详情
    Qot_GetCompanyExecutives = 3244                   # 获取公司高管信息
    Qot_GetCompanyExecutiveBackground = 3245          # 获取公司高管背景
    Qot_GetCompanyOperationalEfficiency = 3246        # 获取公司经营效率
    Qot_GetTopTenBuySellBrokers = 3247                # 获取十大买卖经纪商
    Qot_GetDailyShortVolume = 3248                    # 获取每日卖空（美股/港股）
    Qot_GetShortInterest = 3249                       # 获取空头持仓（美股/港股）
    Qot_GetOptionVolatility = 3250                    # 获取期权波动率分析
    Qot_GetOptionExerciseProbability = 3251           # 获取期权行权概率
    Qot_StockScreen = 3252  # 条件选股V2 (int64+倍率)
    Qot_OptionScreen = 3253  # 期权选股
    Qot_WarrantScreen = 3254  # 窝轮筛选V2 (int64+倍率)
    Qot_GetOptionQuote = 3255  # 获取期权行情
    Qot_GetOptionStrategy = 3256  # 获取期权策略组合
    Qot_GetOptionStrategyAnalysis = 3257  # 获取期权策略分析
    Qot_GetOptionStrategySpread = 3258  # 获取期权策略有效价差
    Qot_GetIndicatorList = 3259  # 获取指标列表
    Qot_RequestIndicatorCalc = 3260  # 异步发起指标计算
    Qot_PushIndicatorCalc = 3261  # 指标异步计算结果推送
    Qot_GetSearchQuote = 3262  # 搜索行情
    Qot_GetSearchNews = 3263   # 搜索资讯

    Qot_GetOptionMarketStatistic = 3301      # 获取期权市场统计
    Qot_GetOptionUnderlyingHisStatistic = 3302    # 获取期权标的历史统计
    Qot_GetOptionUnderlyingOverview = 3303        # 获取批量标的最新数据
    Qot_GetOptionUnderlyingHisVolatility = 3304   # 获取历史波动率
    Qot_GetOptionUnderlyingRank = 3305            # 获取标的排行
    Qot_GetOptionRank = 3306                 # 获取期权合约排行
    Qot_GetOptionEvent = 3307                # 获取期权异动列表
    Qot_GetOptionEventAlert = 3308           # 获取期权异动告警设置
    Qot_SetOptionEventAlert = 3309           # 修改期权异动告警条件
    Qot_UpdateOptionEvent = 3310             # 期权异动推送
    Qot_GetOptionZeroDteScreener = 3311      # 获取末日期权标的列表
    Qot_GetOptionZeroDteContract = 3312      # 获取末日期权合约列表
    Qot_GetOptionEarningsScreener = 3313     # 获取财报期权标的列表
    Qot_GetOptionSellerScreener = 3314       # 获取期权卖方策略列表
    Qot_GetEarningsCalendar = 3401           # 获取财报日历
    Qot_GetMacroIndicatorList = 3402         # 获取宏观指标列表
    Qot_GetMacroIndicatorHistory = 3403      # 获取宏观指标历史数据
    Qot_GetFedWatchTargetRate = 3404         # 获取FedWatch目标利率概率
    Qot_GetFedWatchDotPlot = 3405            # 获取FedWatch点阵图
    Qot_GetEarningsBeatRank = 3406           # 获取盈利超预期排名
    Qot_GetDividendRank = 3407               # 获取股息排行
    Qot_GetDividendCalendar = 3408           # 获取派息日历
    Qot_GetEconomicCalendar = 3409           # 获取经济事件日历
    Qot_GetUSPreMarketRank = 3410            # 获取盘前榜(美股)
    Qot_GetUSAfterHoursRank = 3411           # 获取盘后榜(美股)
    Qot_GetUSOvernightRank = 3412            # 获取夜盘榜(美股)
    Qot_GetTopMoversRank = 3413              # 获取领涨/领跌榜(盘中)
    Qot_GetHotList = 3414                    # 获取热议榜
    Qot_GetShortSellingRank = 3415           # 获取卖空异动榜(美股)
    Qot_GetPeriodChangeRank = 3416           # 获取区间涨跌幅
    Qot_GetHighDividendSOERank = 3417        # 获取破净高股息国央企(港股)
    Qot_GetInstitutionList = 3418            # 获取机构列表
    Qot_GetInstitutionProfile = 3419         # 获取机构概况
    Qot_GetInstitutionDistribution = 3420    # 获取机构持仓行业分布
    Qot_GetInstitutionHoldingChange = 3421   # 获取机构持仓变动
    Qot_GetInstitutionHoldingList = 3422     # 获取机构持股列表
    Qot_GetArkFundHolding = 3423             # 获取ARK基金持仓
    Qot_GetArkStockDynamic = 3424            # 获取ARK个股交易动态
    Qot_GetArkActiveTransaction = 3425       # 获取ARK主动交易聚合
    Qot_GetRatingChange = 3426               # 获取评级变动
    Qot_GetIndustrialChainList = 3427        # 获取产业链列表
    Qot_GetIndustrialChainDetail = 3428      # 获取产业链详情
    Qot_GetIndustrialChainByPlate = 3429      # 获取板块关联产业链
    Qot_GetIndustrialPlateInfo = 3430        # 获取产业板块信息
    Qot_GetIndustrialPlateStock = 3431       # 获取产业板块成分股
    Qot_GetHeatMapData = 3432                # 获取热力图数据
    Qot_GetRiseFallDistribution = 3433       # 获取涨跌分布
    Qot_GetEventContractCategory = 3434      # 获取事件合约分类
    Qot_FilterCompetition = 3435              # 赛事筛选
    Qot_GetEventContractSeriesList = 3436    # 获取事件合约Series列表
    Qot_GetEventContractEventList = 3437     # 获取事件合约Event列表
    Qot_GetEventContract = 3438              # 获取事件合约Contract列表
    Qot_GetEventContractMilestoneList = 3439 # 获取事件合约里程碑列表
    Qot_GetEventContractSnapshot = 3445      # 获取事件合约快照
    Qot_GetEventContractOrderBook = 3446     # 获取事件合约摆盘
    Qot_GetEventContractKline = 3447         # 获取事件合约K线
    Qot_GetEventContractTicker = 3448        # 获取事件合约逐笔
    Qot_UpdateEventContractOrderBook = 3450 # 事件合约摆盘推送
    Qot_UpdateEventContractKline = 3451     # 事件合约K线推送
    Qot_UpdateEventContractTicker = 3452     # 事件合约逐笔推送
    Qot_GetEventContractComboList = 3453     # 获取可Combo事件列表
    Qot_GetEventContractComboRfq = 3454      # Combo询价
    Qot_SubEventContract = 3455              # 事件合约订阅/反订阅
    Qot_RequestHistoryEventContractKL = 3456 # 拉取事件合约历史K线
    SkillWrap_TechnicalUnusual = 3801  # 技术指标异动
    SkillWrap_FinancialUnusual = 3802  # 财务异动
    SkillWrap_DerivativeUnusual = 3803  # 衍生品异动

    All_PushId = [Notify, Trd_UpdateOrder, Trd_UpdateOrderFill, Qot_UpdateBroker,
                  Qot_UpdateOrderBook, Qot_UpdateKL, Qot_UpdateRT, Qot_UpdateBasicQot, Qot_UpdateTicker, Qot_UpdatePriceReminder,
                  Qot_UpdateOptionEvent, Qot_PushIndicatorCalc,
                  Qot_UpdateEventContractOrderBook, Qot_UpdateEventContractKline, Qot_UpdateEventContractTicker]

    @classmethod
    def is_proto_id_push(cls, proto_id):
        return proto_id in ProtoId.All_PushId


class FtEnum(object):

    def __init__(self):
        self.str_dic = self.load_dic()
        """逆转kv对"""
        self.number_dic = dict()
        for k, v in self.str_dic.items():
            self.number_dic[v] = k

    @abstractmethod
    def load_dic(self):
        return {
        }

    @classmethod
    def if_has_key(cls, str_value):
        obj = cls()
        if not isinstance(str_value, str):
            return False
        return str_value in obj.str_dic

    @classmethod
    def get_all_keys(cls):
        obj = cls()
        return ",".join([x for x in obj.str_dic.keys()])

    @classmethod
    def get_all_key_list(cls):
        obj = cls()
        key_list = list()
        for x in obj.str_dic.keys():
            key_list.append(x)
        return key_list

    @classmethod
    def to_number(cls, str_value):
        obj = cls()
        if not isinstance(str_value, str):
            return False, obj.__class__.__name__ + " input parameter must str!"

        if str_value in obj.str_dic:
            return True, obj.str_dic[str_value]
        else:
            return False, obj.__class__.__name__ + " input parameter is incorrect!"

    @classmethod
    def to_string(cls, number_value):
        obj = cls()
        if not isinstance(number_value, int):
            return False, obj.__class__.__name__ + " input parameter must int!"

        if number_value in obj.number_dic:
            return True, obj.number_dic[number_value]
        else:
            return False, str(number_value) + " cannot be converted to SortField Type!"

    @classmethod
    def to_string2(cls, number_value):
        obj = cls()
        if not isinstance(number_value, int):
            return "N/A"
        if number_value in obj.number_dic:
            return obj.number_dic[number_value]
        else:
            return "N/A"


RET_OK = 0
RET_ERROR = -1
ERROR_STR_PREFIX = 'ERROR. '
EMPTY_STRING = ''

MESSAGE_HEAD_FMT = "<1s1sI2B2I20s8s"
"""
    #pragma pack(push, APIProtoHeader, 1)
    struct APIProtoHeader
    {
        u8_t szHeaderFlag[2]; //包头起始标志，固定为“FT”
        u32_t nProtoID;  //协议ID
        u8_t nProtoFmtType; //协议格式类型，0为Protobuf格式，1为Json格式
        u8_t nProtoVer; //协议版本，用于迭代兼容
        u32_t nSerialNo; //包序列号
        u32_t nBodyLen; //包体长度
        u8_t arrBodySHA1[20]; //包体原数据(解密后)的SHA1哈希值
        u8_t arrReserved[8]; //保留8字节扩展
    };
    #pragma pack(pop, APIProtoHeader)
"""

# 默认的ClientID, 用于区分不同的api
DEFULAT_CLIENT_ID = "PyNormal"
CLIENT_VERSION = 300

# 默认的init_connect连接用的rsa private key文件路径
DEFAULT_INIT_PRI_KEY_FILE = "conn_key.txt"

# 协议格式


class ProtoFMT(object):
    """
    协议格式类型
    ..  py:class:: ProtoFMT
     ..  py:attribute:: Protobuf
      google的protobuf格式
     ..  py:attribute:: Json
      json格式
    """
    Protobuf = 0
    Json = 1


# 默认的协议格式 : set_proto_fmt 更改
DEFULAT_PROTO_FMT = ProtoFMT.Protobuf

# api的协议版本号
API_PROTO_VER = int(0)

# 市场标识字符串

class ComboLeg(object):
    def __init__(self):
        self.code = None
        self.trd_side = None
        self.qty_ratio = None
        self.position_id = None
        self.pred_side = None

    def __repr__(self):
        ret_repr_str = "ComboLeg(code={}, trd_side={}, qty_ratio={}".format(self.code, self.trd_side, self.qty_ratio)
        if self.position_id is not None:
            ret_repr_str += ", position_id={}".format(self.position_id)
        if self.pred_side is not None:
            ret_repr_str += ", pred_side={}".format(self.pred_side)
        ret_repr_str += ")"
        return ret_repr_str

# 用户归属地
class UserAttr(FtEnum):
    NONE = "N/A"                               # 未知
    CN = "CN"                                  # 大陆
    US = "US"                                  # 美国
    SG = "SG"                                  # 新加坡
    AU = "AU"                                  # 新加坡
    JP = "JP"                                  # 日本
    HK = "HK"                                  # 香港

    def load_dic(self):
        return {
            self.NONE: Common_pb2.UserAttribution_Unknown,
            self.CN: Common_pb2.UserAttribution_NN,
            self.US: Common_pb2.UserAttribution_MM,
            self.SG: Common_pb2.UserAttribution_SG,
            self.AU: Common_pb2.UserAttribution_AU,
            self.JP: Common_pb2.UserAttribution_JP,
            self.HK: Common_pb2.UserAttribution_HK,
        }

class Market(FtEnum):
    """
    标识不同的行情市场，股票名称的前缀复用该字符串,如 **'HK.00700'**, **'HK_FUTURE.999010'**
    ..  py:class:: Market
     ..  py:attribute:: HK
      港股
     ..  py:attribute:: US
      美股
     ..  py:attribute:: SH
      沪市
     ..  py:attribute:: SZ
      深市
     ..  py:attribute:: HK_FUTURE
      港股期货
     ..  py:attribute:: CC
      加密货币市场 (Crypto Currency)
     ..  py:attribute:: NONE
      未知
    """
    NONE = "N/A"
    HK = "HK"
    US = "US"
    SH = "SH"
    SZ = "SZ"
    HK_FUTURE = "HK_FUTURE"
    SG = "SG"
    JP = "JP"
    AU = "AU"
    MY = "MY"
    CA = "CA"
    FX = "FX"
    CC = "CC"  # 加密货币市场 (Crypto Currency)
    EC = "EC"  # 事件合约市场 (Event Contract)

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.QotMarket_Unknown,
            self.HK: Qot_Common_pb2.QotMarket_HK_Security,
            self.US: Qot_Common_pb2.QotMarket_US_Security,
            self.SH: Qot_Common_pb2.QotMarket_CNSH_Security,
            self.SZ: Qot_Common_pb2.QotMarket_CNSZ_Security,
            self.HK_FUTURE: Qot_Common_pb2.QotMarket_HK_Future,
            self.SG: Qot_Common_pb2.QotMarket_SG_Security,
            self.JP: Qot_Common_pb2.QotMarket_JP_Security,
            self.AU: Qot_Common_pb2.QotMarket_AU_Security,
            self.MY: Qot_Common_pb2.QotMarket_MY_Security,
            self.CA: Qot_Common_pb2.QotMarket_CA_Security,
            self.FX: Qot_Common_pb2.QotMarket_FX_Security,
            self.CC: Qot_Common_pb2.QotMarket_CC_Security,
            self.EC: Qot_Common_pb2.QotMarket_EventContract,
        }

QOT_MARKET_TO_TRD_SEC_MARKET_MAP = {
    Qot_Common_pb2.QotMarket_Unknown: Trd_Common_pb2.TrdSecMarket_Unknown,
    Qot_Common_pb2.QotMarket_CNSH_Security: Trd_Common_pb2.TrdSecMarket_CN_SH,
    Qot_Common_pb2.QotMarket_CNSZ_Security: Trd_Common_pb2.TrdSecMarket_CN_SZ,
    Qot_Common_pb2.QotMarket_HK_Security: Trd_Common_pb2.TrdSecMarket_HK,
    Qot_Common_pb2.QotMarket_HK_Future: Trd_Common_pb2.TrdSecMarket_HK,
    Qot_Common_pb2.QotMarket_US_Security: Trd_Common_pb2.TrdSecMarket_US,
    Qot_Common_pb2.QotMarket_SG_Security: Trd_Common_pb2.TrdSecMarket_SG,
    Qot_Common_pb2.QotMarket_JP_Security: Trd_Common_pb2.TrdSecMarket_JP,
    Qot_Common_pb2.QotMarket_AU_Security: Trd_Common_pb2.TrdSecMarket_AU,
    Qot_Common_pb2.QotMarket_MY_Security: Trd_Common_pb2.TrdSecMarket_MY,
    Qot_Common_pb2.QotMarket_CA_Security: Trd_Common_pb2.TrdSecMarket_CA,
    Qot_Common_pb2.QotMarket_FX_Security: Trd_Common_pb2.TrdSecMarket_FX,
    Qot_Common_pb2.QotMarket_CC_Security: Trd_Common_pb2.TrdSecMarket_CC,
    Qot_Common_pb2.QotMarket_EventContract: Trd_Common_pb2.TrdSecMarket_EC,
}


# 市场状态
class MarketState(FtEnum):
    """
    行情市场状态定义
    ..  py:class:: MarketState
     ..  py:attribute:: NONE
      无交易,美股未开盘
     ..  py:attribute:: AUCTION
      竞价
     ..  py:attribute:: WAITING_OPEN
      早盘前等待开盘
     ..  py:attribute:: MORNING
      早盘前等待开盘
     ..  py:attribute:: REST
      午间休市
     ..  py:attribute:: AFTERNOON
      午盘
     ..  py:attribute:: CLOSED
      收盘
     ..  py:attribute:: PRE_MARKET_BEGIN
      盘前开始
     ..  py:attribute:: PRE_MARKET_END
      盘前结束
     ..  py:attribute:: AFTER_HOURS_BEGIN
      盘后开始
     ..  py:attribute:: AFTER_HOURS_END
      盘后结束
     ..  py:attribute:: AFTER_HOURS_END
      盘后结束
     ..  py:attribute:: NIGHT_OPEN
      夜市开盘
     ..  py:attribute:: NIGHT_END
      夜市收盘
     ..  py:attribute:: FUTURE_DAY_OPEN
      期指日市开盘
     ..  py:attribute:: FUTURE_DAY_BREAK
      期指日市休市
     ..  py:attribute:: FUTURE_DAY_CLOSE
      期指日市收盘
     ..  py:attribute:: FUTURE_DAY_WAIT_OPEN
      期指日市等待开盘
     ..  py:attribute:: HK_CAS
      港股盘后竞价
     ..  py:attribute:: STIB_AFTER_HOURS_WAIT
      旧名保留兼容。A股盘后撮合等待时段（15:00-15:05）。适用范围：上交所A股/ETF、深交所A股及存托凭证/ETF。
     ..  py:attribute:: ASHARE_AFTER_HOURS_WAIT
      A股盘后撮合等待时段（15:00-15:05）。与 STIB_AFTER_HOURS_WAIT 同值（27）。
     ..  py:attribute:: STIB_AFTER_HOURS_BEGIN
      旧名保留兼容。A股盘后固定价格交易开始（15:05-15:30）。
     ..  py:attribute:: ASHARE_AFTER_HOURS_BEGIN
      A股盘后固定价格交易开始（15:05-15:30）。与 STIB_AFTER_HOURS_BEGIN 同值（28）。
     ..  py:attribute:: STIB_AFTER_HOURS_END
      旧名保留兼容。A股盘后固定价格交易结束（15:30之后）。
     ..  py:attribute:: ASHARE_AFTER_HOURS_END
      A股盘后固定价格交易结束（15:30之后）。与 STIB_AFTER_HOURS_END 同值（29）。
    """
    NONE = "NONE"                                   # 无交易,美股未开盘
    AUCTION = "AUCTION"                             # 竞价
    WAITING_OPEN = "WAITING_OPEN"                   # 早盘前等待开盘
    MORNING = "MORNING"                             # 早盘
    REST = "REST"                                   # 午间休市
    AFTERNOON = "AFTERNOON"                         # 午盘
    CLOSED = "CLOSED"                               # 收盘
    PRE_MARKET_BEGIN = "PRE_MARKET_BEGIN"           # 盘前
    PRE_MARKET_END = "PRE_MARKET_END"               # 盘前结束
    AFTER_HOURS_BEGIN = "AFTER_HOURS_BEGIN"         # 盘后
    AFTER_HOURS_END = "AFTER_HOURS_END"             # 盘后结束
    NIGHT_OPEN = "NIGHT_OPEN"                       # 夜市开盘
    NIGHT_END = "NIGHT_END"                         # 夜市收盘
    FUTURE_DAY_OPEN = "FUTURE_DAY_OPEN"             # 期指日市开盘
    FUTURE_DAY_BREAK = "FUTURE_DAY_BREAK"           # 期指日市休市
    FUTURE_DAY_CLOSE = "FUTURE_DAY_CLOSE"           # 期指日市收盘
    FUTURE_DAY_WAIT_OPEN = "FUTURE_DAY_WAIT_OPEN"   # 期指日市等待开盘
    HK_CAS = "HK_CAS"                               # 盘后竞价, 港股市场增加CAS机制对应的市场状态
    FUTURE_NIGHT_WAIT = "FUTURE_NIGHT_WAIT"         # 夜市等待开盘
    FUTURE_AFTERNOON = "FUTURE_AFTERNOON"           # 期货下午开盘
    FUTURE_SWITCH_DATE = "FUTURE_SWITCH_DATE"       # 期货切交易日
    FUTURE_OPEN = "FUTURE_OPEN"                     # 期货开盘
    FUTURE_BREAK = "FUTURE_BREAK"                   # 期货中盘休息
    FUTURE_BREAK_OVER = "FUTURE_BREAK_OVER"         # 期货休息后开盘
    FUTURE_CLOSE = "FUTURE_CLOSE"                   # 期货收盘
    STIB_AFTER_HOURS_WAIT = "STIB_AFTER_HOURS_WAIT"  # 旧名保留兼容；A股盘后撮合等待（15:00-15:05）
    ASHARE_AFTER_HOURS_WAIT = "ASHARE_AFTER_HOURS_WAIT"  # A股盘后撮合等待（15:00-15:05）
    STIB_AFTER_HOURS_BEGIN = "STIB_AFTER_HOURS_BEGIN"  # 旧名保留兼容；A股盘后固定价格交易开始（15:05-15:30）
    ASHARE_AFTER_HOURS_BEGIN = "ASHARE_AFTER_HOURS_BEGIN"  # A股盘后固定价格交易开始（15:05-15:30）
    STIB_AFTER_HOURS_END = "STIB_AFTER_HOURS_END"  # 旧名保留兼容；A股盘后固定价格交易结束（15:30之后）
    ASHARE_AFTER_HOURS_END = "ASHARE_AFTER_HOURS_END"  # A股盘后固定价格交易结束（15:30之后）
    NIGHT = "NIGHT"                                  #夜市
    TRADE_AT_LAST = "TRADE_AT_LAST"                  #盘尾交易
    OVERNIGHT = "OVERNIGHT"                          #美股夜盘交易

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.QotMarketState_None,
            self.AUCTION: Qot_Common_pb2.QotMarketState_Auction,
            self.WAITING_OPEN: Qot_Common_pb2.QotMarketState_WaitingOpen,
            self.MORNING: Qot_Common_pb2.QotMarketState_Morning,
            self.REST: Qot_Common_pb2.QotMarketState_Rest,
            self.AFTERNOON: Qot_Common_pb2.QotMarketState_Afternoon,
            self.CLOSED: Qot_Common_pb2.QotMarketState_Closed,
            self.PRE_MARKET_BEGIN: Qot_Common_pb2.QotMarketState_PreMarketBegin,
            self.PRE_MARKET_END: Qot_Common_pb2.QotMarketState_PreMarketEnd,
            self.AFTER_HOURS_BEGIN: Qot_Common_pb2.QotMarketState_AfterHoursBegin,
            self.AFTER_HOURS_END: Qot_Common_pb2.QotMarketState_AfterHoursEnd,
            self.NIGHT_OPEN: Qot_Common_pb2.QotMarketState_NightOpen,
            self.NIGHT_END: Qot_Common_pb2.QotMarketState_NightEnd,
            self.FUTURE_DAY_OPEN: Qot_Common_pb2.QotMarketState_FutureDayOpen,
            self.FUTURE_DAY_BREAK: Qot_Common_pb2.QotMarketState_FutureDayBreak,
            self.FUTURE_DAY_CLOSE: Qot_Common_pb2.QotMarketState_FutureDayClose,
            self.FUTURE_DAY_WAIT_OPEN: Qot_Common_pb2.QotMarketState_FutureDayWaitForOpen,
            self.HK_CAS: Qot_Common_pb2.QotMarketState_HkCas,
            self.FUTURE_NIGHT_WAIT: Qot_Common_pb2.QotMarketState_FutureNightWait,
            self.FUTURE_AFTERNOON: Qot_Common_pb2.QotMarketState_FutureAfternoon,
            self.FUTURE_SWITCH_DATE: Qot_Common_pb2.QotMarketState_FutureSwitchDate,
            self.FUTURE_OPEN: Qot_Common_pb2.QotMarketState_FutureOpen,
            self.FUTURE_BREAK: Qot_Common_pb2.QotMarketState_FutureBreak,
            self.FUTURE_BREAK_OVER: Qot_Common_pb2.QotMarketState_FutureBreakOver,
            self.FUTURE_CLOSE: Qot_Common_pb2.QotMarketState_FutureClose,
            # 新别名写在旧名之后，to_string2 反向返回新名 ASHARE_AFTER_HOURS_*
            self.STIB_AFTER_HOURS_WAIT: Qot_Common_pb2.QotMarketState_StibAfterHoursWait,
            self.ASHARE_AFTER_HOURS_WAIT: Qot_Common_pb2.QotMarketState_AShareAfterHoursWait,
            self.STIB_AFTER_HOURS_BEGIN: Qot_Common_pb2.QotMarketState_StibAfterHoursBegin,
            self.ASHARE_AFTER_HOURS_BEGIN: Qot_Common_pb2.QotMarketState_AShareAfterHoursBegin,
            self.STIB_AFTER_HOURS_END: Qot_Common_pb2.QotMarketState_StibAfterHoursEnd,
            self.ASHARE_AFTER_HOURS_END: Qot_Common_pb2.QotMarketState_AShareAfterHoursEnd,
            self.NIGHT: Qot_Common_pb2.QotMarketState_NIGHT,
            self.TRADE_AT_LAST: Qot_Common_pb2.QotMarketState_TRADE_AT_LAST,
            self.OVERNIGHT: Qot_Common_pb2.QotMarketState_OVERNIGHT,
        }

# 股票类型
class SecurityType(FtEnum):
    """
    证券类型定义
    ..  py:class:: SecurityType
     ..  py:attribute:: STOCK
      股票
     ..  py:attribute:: IDX
      指数
     ..  py:attribute:: ETF
      交易所交易基金(Exchange Traded Funds)
     ..  py:attribute:: WARRANT
      港股窝轮牛熊证
     ..  py:attribute:: BOND
      债券
    ..  py:attribute:: DRVT
      期权
    ..  py:attribute:: FUTURE
      期货
    ..  py:attribute:: CRYPTO
      加密货币币种/指数
     ..  py:attribute:: NONE
      未知
    """
    NONE = "N/A"
    BOND = "BOND"
    BWRT = "BWRT"
    STOCK = "STOCK"
    WARRANT = "WARRANT"
    IDX = "IDX"
    ETF = "ETF"
    DRVT = "DRVT"
    FUTURE = "FUTURE"
    PLATE = "PLATE"
    PLATESET = "PLATESET"
    CRYPTO = "CRYPTO"  # 加密货币币种/指数
    FOREX = "FOREX"    # 外汇

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.SecurityType_Unknown,
            self.BOND: Qot_Common_pb2.SecurityType_Bond,
            self.BWRT: Qot_Common_pb2.SecurityType_Bwrt,
            self.STOCK: Qot_Common_pb2.SecurityType_Eqty,
            self.ETF: Qot_Common_pb2.SecurityType_Trust,
            self.WARRANT: Qot_Common_pb2.SecurityType_Warrant,
            self.IDX: Qot_Common_pb2.SecurityType_Index,
            self.PLATE: Qot_Common_pb2.SecurityType_Plate,
            self.DRVT: Qot_Common_pb2.SecurityType_Drvt,
            self.PLATESET: Qot_Common_pb2.SecurityType_PlateSet,
            self.FUTURE: Qot_Common_pb2.SecurityType_Future,
            self.FOREX: Qot_Common_pb2.SecurityType_Forex,
            self.CRYPTO: Qot_Common_pb2.SecurityType_Crypto,
        }

# 实时数据定阅类型
class SubType(FtEnum):
    """
    实时数据定阅类型定义
    ..  py:class:: SubType
     ..  py:attribute:: TICKER
      逐笔
     ..  py:attribute:: QUOTE
      报价
     ..  py:attribute:: ORDER_BOOK
      买卖摆盘
     ..  py:attribute:: K_1M
      1分钟K线
     ..  py:attribute:: K_5M
      5分钟K线
     ..  py:attribute:: K_10M
      10分钟K线
     ..  py:attribute:: K_15M
      15分钟K线
     ..  py:attribute:: K_30M
      30分钟K线
     ..  py:attribute:: K_60M
      60分钟K线
     ..  py:attribute:: K_120M
      120分钟K线(2小时)
     ..  py:attribute:: K_180M
      180分钟K线(3小时)
     ..  py:attribute:: K_240M
      240分钟K线(4小时)
     ..  py:attribute:: K_DAY
      日K线
     ..  py:attribute:: K_WEEK
      周K线
     ..  py:attribute:: K_MON
      月K线
     ..  py:attribute:: RT_DATA
      分时
     ..  py:attribute:: BROKER
      买卖经纪
    """
    NONE = "N/A"
    TICKER = "TICKER"
    QUOTE = "QUOTE"
    ORDER_BOOK = "ORDER_BOOK"
    ORDER_BOOK_ODD = "ORDER_BOOK_ODD"
    K_1M = "K_1M"
    K_3M = "K_3M"
    K_5M = "K_5M"
    K_10M = "K_10M"
    K_15M = "K_15M"
    K_30M = "K_30M"
    K_60M = "K_60M"
    K_120M = "K_120M"
    K_180M = "K_180M"
    K_240M = "K_240M"
    K_DAY = "K_DAY"
    K_WEEK = "K_WEEK"
    K_MON = "K_MON"
    K_QUARTER = "K_QUARTER"
    K_YEAR = "K_YEAR"
    RT_DATA = "RT_DATA"
    BROKER = "BROKER"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.SubType_None,
            self.QUOTE: Qot_Common_pb2.SubType_Basic,
            self.ORDER_BOOK: Qot_Common_pb2.SubType_OrderBook,
            self.ORDER_BOOK_ODD: Qot_Common_pb2.SubType_OrderBook_Odd,
            self.TICKER: Qot_Common_pb2.SubType_Ticker,
            self.BROKER: Qot_Common_pb2.SubType_Broker,
            self.RT_DATA: Qot_Common_pb2.SubType_RT,
            self.K_DAY: Qot_Common_pb2.SubType_KL_Day,
            self.K_1M: Qot_Common_pb2.SubType_KL_1Min,
            self.K_3M: Qot_Common_pb2.SubType_KL_3Min,
            self.K_5M: Qot_Common_pb2.SubType_KL_5Min,
            self.K_10M: Qot_Common_pb2.SubType_KL_10Min,
            self.K_15M: Qot_Common_pb2.SubType_KL_15Min,
            self.K_30M: Qot_Common_pb2.SubType_KL_30Min,
            self.K_60M: Qot_Common_pb2.SubType_KL_60Min,
            self.K_120M: Qot_Common_pb2.SubType_KL_120Min,
            self.K_180M: Qot_Common_pb2.SubType_KL_180Min,
            self.K_240M: Qot_Common_pb2.SubType_KL_240Min,
            self.K_WEEK: Qot_Common_pb2.SubType_KL_Week,
            self.K_MON: Qot_Common_pb2.SubType_KL_Month,
            self.K_QUARTER: Qot_Common_pb2.SubType_KL_Qurater,
            self.K_YEAR: Qot_Common_pb2.SubType_KL_Year,
        }


KLINE_SUBTYPE_LIST = [SubType.K_DAY, SubType.K_MON, SubType.K_WEEK,
                      SubType.K_1M, SubType.K_3M, SubType.K_5M, SubType.K_10M, SubType.K_15M,
                      SubType.K_30M, SubType.K_60M, SubType.K_120M, SubType.K_180M, SubType.K_240M,
                      SubType.K_QUARTER, SubType.K_YEAR,
                      ]


class OrderBookType(FtEnum):
    """
    摆盘类型定义
    ..  py:class:: OrderBookType
     ..  py:attribute:: NORMAL
      整股盘
     ..  py:attribute:: ODD
      碎股盘
    """
    NONE = "N/A"
    NORMAL = "NORMAL"
    ODD = "ODD"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.OrderBookType_Normal,
            self.NORMAL: Qot_Common_pb2.OrderBookType_Normal,
            self.ODD: Qot_Common_pb2.OrderBookType_Odd,
        }


# k线类型


class KLType(FtEnum):
    """
    k线类型定义
    ..  py:class:: KLType
     ..  py:attribute:: K_1M
      1分钟K线
     ..  py:attribute:: K_5M
      5分钟K线
     ..  py:attribute:: K_10M
      10分钟K线
     ..  py:attribute:: K_15M
      15分钟K线
     ..  py:attribute:: K_30M
      30分钟K线
     ..  py:attribute:: K_60M
      60分钟K线
     ..  py:attribute:: K_120M
      120分钟K线(2小时)
     ..  py:attribute:: K_180M
      180分钟K线(3小时)
     ..  py:attribute:: K_240M
      240分钟K线(4小时)
     ..  py:attribute:: K_DAY
      日K线
     ..  py:attribute:: K_WEEK
      周K线
     ..  py:attribute:: K_MON
      月K线
    """
    NONE = "N/A"
    K_1M = "K_1M"
    K_3M = "K_3M"
    K_5M = "K_5M"
    K_10M = "K_10M"
    K_15M = "K_15M"
    K_30M = "K_30M"
    K_60M = "K_60M"
    K_120M = "K_120M"
    K_180M = "K_180M"
    K_240M = "K_240M"
    K_DAY = "K_DAY"
    K_WEEK = "K_WEEK"
    K_MON = "K_MON"
    K_QUARTER = "K_QUARTER"
    K_YEAR = "K_YEAR"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.KLType_Unknown,
            self.K_1M: Qot_Common_pb2.KLType_1Min,
            self.K_3M: Qot_Common_pb2.KLType_3Min,
            self.K_5M: Qot_Common_pb2.KLType_5Min,
            self.K_10M: Qot_Common_pb2.KLType_10Min,
            self.K_15M: Qot_Common_pb2.KLType_15Min,
            self.K_30M: Qot_Common_pb2.KLType_30Min,
            self.K_60M: Qot_Common_pb2.KLType_60Min,
            self.K_120M: Qot_Common_pb2.KLType_120Min,
            self.K_180M: Qot_Common_pb2.KLType_180Min,
            self.K_240M: Qot_Common_pb2.KLType_240Min,
            self.K_DAY: Qot_Common_pb2.KLType_Day,
            self.K_WEEK: Qot_Common_pb2.KLType_Week,
            self.K_MON: Qot_Common_pb2.KLType_Month,
            self.K_QUARTER: Qot_Common_pb2.KLType_Quarter,
            self.K_YEAR: Qot_Common_pb2.KLType_Year,
        }

# k线复权
class AuType(FtEnum):
    """
    k线复权类型定义
    ..  py:class:: AuType
     ..  py:attribute:: QFQ
      前复权
     ..  py:attribute:: HFQ
      后复权
     ..  py:attribute:: NONE
      不复权
    """
    QFQ = "qfq"
    HFQ = "hfq"
    NONE = "None"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.RehabType_None,
            self.QFQ: Qot_Common_pb2.RehabType_Forward,
            self.HFQ: Qot_Common_pb2.RehabType_Backward,
        }

# k线数据字段
class KL_FIELD(object):
    """
    获取K线数据, 可指定需返回的字段
    ..  py:class:: KL_FIELD
     ..  py:attribute:: ALL
      所有字段
     ..  py:attribute:: DATE_TIME
      日期时间
     ..  py:attribute:: OPEN
      开盘价
     ..  py:attribute:: CLOSE
      收盘价
     ..  py:attribute:: HIGH
      最高价
     ..  py:attribute:: LOW
      最低价
     ..  py:attribute:: PE_RATIO
      市盈率
     ..  py:attribute:: TURNOVER_RATE
      换手率
     ..  py:attribute:: TRADE_VOL
      成交量
     ..  py:attribute:: TRADE_VAL
      成交额
     ..  py:attribute:: CHANGE_RATE
      涨跌比率
     ..  py:attribute:: LAST_CLOSE
      昨收价
    """
    ALL = ''
    DATE_TIME = '1'
    OPEN = '2'
    CLOSE = '3'
    HIGH = '4'
    LOW = '5'
    PE_RATIO = '6'
    TURNOVER_RATE = '7'
    TRADE_VOL = '8'
    TRADE_VAL = '9'
    CHANGE_RATE = '10'
    LAST_CLOSE = '11'

    ALL_REAL = [
        DATE_TIME, OPEN, CLOSE, HIGH, LOW, PE_RATIO, TURNOVER_RATE, TRADE_VOL,
        TRADE_VAL, CHANGE_RATE, LAST_CLOSE
    ]

    FIELD_FLAG_VAL_MAP = {
        DATE_TIME: 0,
        HIGH: 1,
        OPEN: 2,
        LOW: 4,
        CLOSE: 8,
        LAST_CLOSE: 16,
        TRADE_VOL: 32,
        TRADE_VAL: 64,
        TURNOVER_RATE: 128,
        PE_RATIO: 256,
        CHANGE_RATE: 512,
    }

    DICT_KL_FIELD_STR = {
        DATE_TIME: 'time_key',
        OPEN: 'open',
        CLOSE: 'close',
        HIGH: 'high',
        LOW: 'low',
        PE_RATIO: 'pe_ratio',
        TURNOVER_RATE: 'turnover_rate',
        TRADE_VOL: 'volume',
        TRADE_VAL: 'turnover',
        CHANGE_RATE: 'change_rate',
        LAST_CLOSE: 'last_close'
    }

    @classmethod
    def get_field_list(cls, str_filed):
        ret_list = []
        data = str(str_filed).split(',')
        if KL_FIELD.ALL in data:
            ret_list = copy(KL_FIELD.ALL_REAL)
        else:
            for x in data:
                if x in KL_FIELD.ALL_REAL:
                    ret_list.append(x)
        return ret_list

    @classmethod
    def normalize_field_list(cls, fields):
        list_ret = []
        if KL_FIELD.ALL in fields:
            list_ret = copy(KL_FIELD.ALL_REAL)
        else:
            for x in fields:
                if x in KL_FIELD.ALL_REAL and x not in list_ret:
                    list_ret.append(x)
        return list_ret

    @classmethod
    def kl_fields_to_flag_val(cls, fields):
        fields_normal = KL_FIELD.normalize_field_list(fields)
        ret_flags = 0
        for x in fields_normal:
            ret_flags += KL_FIELD.FIELD_FLAG_VAL_MAP[x]
        return ret_flags


# 成交逐笔的方向
class TickerDirect(FtEnum):
    """
    逐笔方向定义
    ..  py:class:: TickerDirect
     ..  py:attribute:: BUY
      买
     ..  py:attribute:: SELL
      卖
     ..  py:attribute:: NEUTRAL
      中性
    """
    NONE = "N/A"
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.TickerDirection_Unknown,
            self.BUY: Qot_Common_pb2.TickerDirection_Bid,
            self.SELL: Qot_Common_pb2.TickerDirection_Ask,
            self.NEUTRAL: Qot_Common_pb2.TickerDirection_Neutral,
        }

class Plate(FtEnum):
    """
    板块集合分类定义
    ..  py:class:: Plate
     ..  py:attribute:: ALL
      所有板块
     ..  py:attribute:: INDUSTRY
      行业板块
     ..  py:attribute:: REGION
      地域板块
     ..  py:attribute:: CONCEPT
      概念板块
    """
    ALL = "ALL"
    INDUSTRY = "INDUSTRY"
    REGION = "REGION"
    CONCEPT = "CONCEPT"
    OTHER = "OTHER"

    def load_dic(self):
        return {
            self.ALL: Qot_Common_pb2.PlateSetType_All,
            self.INDUSTRY: Qot_Common_pb2.PlateSetType_Industry,
            self.REGION: Qot_Common_pb2.PlateSetType_Region,
            self.CONCEPT: Qot_Common_pb2.PlateSetType_Concept,
            self.OTHER: Qot_Common_pb2.PlateSetType_Other,
        }

# 股票持有者类别
class StockHolder(FtEnum):
    """
    持有者类别
    ..  py:class:: StockHolderType
     ..  py:attribute:: INSTITUTE
      机构
     ..  py:attribute:: FUND
      基金
     ..  py:attribute:: EXECUTIVE
      高管
    """
    NONE = "N/A"
    INSTITUTE = "INSTITUTE"
    FUND = "FUND"
    EXECUTIVE = "EXECUTIVE"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.HolderCategory_Unknow,
            self.INSTITUTE: Qot_Common_pb2.HolderCategory_Agency,
            self.FUND: Qot_Common_pb2.HolderCategory_Fund,
            self.EXECUTIVE: Qot_Common_pb2.HolderCategory_SeniorManager,
        }

# 期权类型
class OptionType(FtEnum):
    """
    期权类型
    ..  py:class:: OptionType
     ..  py:attribute:: ALL
      全部
     ..  py:attribute:: CALL
      涨
     ..  py:attribute:: PUT
      跌
    """
    ALL = "ALL"
    CALL = "CALL"
    PUT = "PUT"

    def load_dic(self):
        return {
            self.ALL: Qot_Common_pb2.OptionType_Unknown,
            self.CALL: Qot_Common_pb2.OptionType_Call,
            self.PUT: Qot_Common_pb2.OptionType_Put,
        }

# 价内价外
class OptionCondType(FtEnum):
    """
    价内价外
    ..  py:class:: OptionCondType
     ..  py:attribute:: ALL
      全部
     ..  py:attribute:: WITHIN
      价内
     ..  py:attribute:: OUTSIDE
      价外
    """
    ALL = "ALL"
    WITHIN = "WITHIN"
    OUTSIDE = "OUTSIDE"

    def load_dic(self):
        return {
            self.ALL: Qot_GetOptionChain_pb2.OptionCondType_Unknow,
            self.WITHIN: Qot_GetOptionChain_pb2.OptionCondType_WithIn,
            self.OUTSIDE: Qot_GetOptionChain_pb2.OptionCondType_Outside,
        }

class OptionStrategyType(FtEnum):
    NONE = "NONE"
    SINGLE = "SINGLE"
    COVERED = "COVERED"
    SPREAD = "SPREAD"
    STRADDLE = "STRADDLE"
    STRANGLE = "STRANGLE"
    COLLAR = "COLLAR"
    BUTTERFLY = "BUTTERFLY"
    CONDOR = "CONDOR"
    IRON_BUTTERFLY = "IRON_BUTTERFLY"
    IRON_CONDOR = "IRON_CONDOR"
    CALENDAR_SPREAD = "CALENDAR_SPREAD"
    DIAGONAL_SPREAD = "DIAGONAL_SPREAD"
    CUSTOM = "CUSTOM"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.OptionStrategyType_Unknown,
            self.SINGLE: Qot_Common_pb2.OptionStrategyType_SingleOption,
            self.COVERED: Qot_Common_pb2.OptionStrategyType_Covered,
            self.SPREAD: Qot_Common_pb2.OptionStrategyType_Spread,
            self.STRADDLE: Qot_Common_pb2.OptionStrategyType_Straddle,
            self.STRANGLE: Qot_Common_pb2.OptionStrategyType_Strangle,
            self.COLLAR: Qot_Common_pb2.OptionStrategyType_Collar,
            self.BUTTERFLY: Qot_Common_pb2.OptionStrategyType_Butterfly,
            self.CONDOR: Qot_Common_pb2.OptionStrategyType_Condor,
            self.IRON_BUTTERFLY: Qot_Common_pb2.OptionStrategyType_IronButterfly,
            self.IRON_CONDOR: Qot_Common_pb2.OptionStrategyType_IronCondor,
            self.CALENDAR_SPREAD: Qot_Common_pb2.OptionStrategyType_CalendarSpread,
            self.DIAGONAL_SPREAD: Qot_Common_pb2.OptionStrategyType_DiagonalSpread,
            self.CUSTOM: Qot_Common_pb2.OptionStrategyType_Customize,
        }

class StrategyLegAction(FtEnum):
    UNKNOWN = "UNKNOWN"
    BUY = "BUY"
    SELL = "SELL"

    def load_dic(self):
        return {
            self.UNKNOWN: 0,
            self.BUY: 1,
            self.SELL: 2,
        }

class DarkStatus(FtEnum):
    NONE = 'N/A'
    TRADING = 'TRADING'
    END = 'END'

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.DarkStatus_None,
            self.TRADING: Qot_Common_pb2.DarkStatus_Trading,
            self.END: Qot_Common_pb2.DarkStatus_End,
        }

class PushDataType(FtEnum):
    NONE = 'N/A'
    REALTIME = 'REALTIME'
    BYDISCONN = 'BYDISCONN'
    CACHE = 'CACHE'

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PushDataType_Unknow,
            self.REALTIME: Qot_Common_pb2.PushDataType_Realtime,
            self.BYDISCONN: Qot_Common_pb2.PushDataType_ByDisConn,
            self.CACHE: Qot_Common_pb2.PushDataType_Cache,
        }

class TickerType(FtEnum):
    UNKNOWN = 'UNKNOWN'
    AUTO_MATCH = 'AUTO_MATCH'
    LATE = 'LATE'
    NON_AUTO_MATCH = 'NON_AUTO_MATCH'
    INTER_AUTO_MATCH = 'INTER_AUTO_MATCH'
    INTER_NON_AUTO_MATCH = 'INTER_NON_AUTO_MATCH'
    ODD_LOT = 'ODD_LOT'
    AUCTION = 'AUCTION'
    BULK = 'BULK'
    CRASH = 'CRASH'
    CROSS_MARKET = 'CROSS_MARKET'
    BULK_SOLD = 'BULK_SOLD'
    FREE_ON_BOARD = 'FREE_ON_BOARD'
    RULE127_OR_155 = 'RULE127_OR_155'
    DELAY = 'DELAY'
    MARKET_CENTER_CLOSE_PRICE = 'MARKET_CENTER_CLOSE_PRICE'
    NEXT_DAY = 'NEXT_DAY'
    MARKET_CENTER_OPENING = 'MARKET_CENTER_OPENING'
    PRIOR_REFERENCE_PRICE = 'PRIOR_REFERENCE_PRICE'
    MARKET_CENTER_OPEN_PRICE = 'MARKET_CENTER_OPEN_PRICE'
    SELLER = 'SELLER'
    T = 'T'
    EXTENDED_TRADING_HOURS = 'EXTENDED_TRADING_HOURS'
    CONTINGENT = 'CONTINGENT'
    AVERAGE_PRICE = 'AVERAGE_PRICE'
    OTC_SOLD = 'OTC_SOLD'
    ODD_LOT_CROSS_MARKET = 'ODD_LOT_CROSS_MARKET'
    DERIVATIVELY_PRICED = 'DERIVATIVELY_PRICED'
    REOPENINGP_RICED = 'REOPENINGP_RICED'
    CLOSING_PRICED = 'CLOSING_PRICED'
    COMPREHENSIVE_DELAY_PRICE = 'COMPREHENSIVE_DELAY_PRICE'
    OVERSEAS = 'OVERSEAS'

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_Common_pb2.TickerType_Unknown,
            self.AUTO_MATCH: Qot_Common_pb2.TickerType_Automatch,
            self.LATE: Qot_Common_pb2.TickerType_Late,
            self.NON_AUTO_MATCH: Qot_Common_pb2.TickerType_NoneAutomatch,
            self.INTER_AUTO_MATCH: Qot_Common_pb2.TickerType_InterAutomatch,
            self.INTER_NON_AUTO_MATCH: Qot_Common_pb2.TickerType_InterNoneAutomatch,
            self.ODD_LOT: Qot_Common_pb2.TickerType_OddLot,
            self.AUCTION: Qot_Common_pb2.TickerType_Auction,
            self.BULK: Qot_Common_pb2.TickerType_Bulk,
            self.CRASH: Qot_Common_pb2.TickerType_Crash,
            self.CROSS_MARKET: Qot_Common_pb2.TickerType_CrossMarket,
            self.BULK_SOLD: Qot_Common_pb2.TickerType_BulkSold,
            self.FREE_ON_BOARD: Qot_Common_pb2.TickerType_FreeOnBoard,
            self.RULE127_OR_155: Qot_Common_pb2.TickerType_Rule127Or155,
            self.DELAY: Qot_Common_pb2.TickerType_Delay,
            self.MARKET_CENTER_CLOSE_PRICE: Qot_Common_pb2.TickerType_MarketCenterClosePrice,
            self.NEXT_DAY: Qot_Common_pb2.TickerType_NextDay,
            self.MARKET_CENTER_OPENING: Qot_Common_pb2.TickerType_MarketCenterOpening,
            self.PRIOR_REFERENCE_PRICE: Qot_Common_pb2.TickerType_PriorReferencePrice,
            self.MARKET_CENTER_OPEN_PRICE: Qot_Common_pb2.TickerType_MarketCenterOpenPrice,
            self.SELLER: Qot_Common_pb2.TickerType_Seller,
            self.T: Qot_Common_pb2.TickerType_T,
            self.EXTENDED_TRADING_HOURS: Qot_Common_pb2.TickerType_ExtendedTradingHours,
            self.CONTINGENT: Qot_Common_pb2.TickerType_Contingent,
            self.AVERAGE_PRICE: Qot_Common_pb2.TickerType_AvgPrice,
            self.OTC_SOLD: Qot_Common_pb2.TickerType_OTCSold,
            self.ODD_LOT_CROSS_MARKET: Qot_Common_pb2.TickerType_OddLotCrossMarket,
            self.DERIVATIVELY_PRICED: Qot_Common_pb2.TickerType_DerivativelyPriced,
            self.REOPENINGP_RICED: Qot_Common_pb2.TickerType_ReOpeningPriced,
            self.CLOSING_PRICED: Qot_Common_pb2.TickerType_ClosingPriced,
            self.COMPREHENSIVE_DELAY_PRICE: Qot_Common_pb2.TickerType_ComprehensiveDelayPrice,
            self.OVERSEAS: Qot_Common_pb2.TickerType_Overseas,
        }

class SysNotifyType(FtEnum):
    """
    系统异步通知类型定义
    ..  py:class:: SysNotifyType
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: GTW_EVENT
      网关事件
    """
    NONE = "N/A"
    GTW_EVENT = "GTW_EVENT"
    PROGRAM_STATUS = "PROGRAM_STATUS"
    CONN_STATUS = "CONN_STATUS"
    QOT_RIGHT = "QOT_RIGHT"
    API_LEVEL = "API_LEVEL"
    API_QUOTA = "API_QUOTA"
    USED_QUOTA = "USED_QUOTA"

    def load_dic(self):
        return {
            self.NONE: Notify_pb2.NotifyType_None,
            self.GTW_EVENT: Notify_pb2.NotifyType_GtwEvent,
            self.PROGRAM_STATUS: Notify_pb2.NotifyType_ProgramStatus,
            self.CONN_STATUS: Notify_pb2.NotifyType_ConnStatus,
            self.QOT_RIGHT: Notify_pb2.NotifyType_QotRight,
            self.API_LEVEL: Notify_pb2.NotifyType_APILevel,
            self.API_QUOTA: Notify_pb2.NotifyType_APIQuota,
            self.USED_QUOTA: Notify_pb2.NotifyType_UsedQuota,
        }

class GtwEventType(FtEnum):
    """
    网关异步通知类型定义
    ..  py:class:: GtwEventType
     ..  py:attribute:: LocalCfgLoadFailed
      本地配置文件加载失败
     ..  py:attribute:: APISvrRunFailed
      网关监听服务运行失败
     ..  py:attribute:: ForceUpdate
      强制升级网关
     ..  py:attribute:: LoginFailed
      登录牛牛服务器失败
     ..  py:attribute:: UnAgreeDisclaimer
      未同意免责声明，无法加运行
     ..  py:attribute:: NetCfgMissing
      缺少网络连接配置
     ..  py:attribute:: KickedOut
      登录被踢下线
     ..  py:attribute:: LoginPwdChanged
      登陆密码变更
     ..  py:attribute:: BanLogin
      牛牛后台不允许该账号登陆
     ..  py:attribute:: NeedPicVerifyCode
      登录需要输入图形验证码
     ..  py:attribute:: NeedPhoneVerifyCode
      登录需要输入手机验证码
     ..  py:attribute:: AppDataNotExist
      程序打包数据丢失
     ..  py:attribute:: NessaryDataMissing
      必要的数据没同步成功
     ..  py:attribute:: TradePwdChanged
      交易密码变更通知
     ..  py:attribute:: EnableDeviceLock
      需启用设备锁
    """
    NONE = "N/A"
    LocalCfgLoadFailed = "LocalCfgLoadFailed"
    APISvrRunFailed = "APISvrRunFailed"
    ForceUpdate = "ForceUpdate"
    LoginFailed = "LoginFailed"
    UnAgreeDisclaimer = "UnAgreeDisclaimer"
    NetCfgMissing = "NetCfgMissing"
    KickedOut = "KickedOut"
    LoginPwdChanged = "LoginPwdChanged"
    BanLogin = "BanLogin"
    NeedPicVerifyCode = "NeedPicVerifyCode"
    NeedPhoneVerifyCode = "NeedPhoneVerifyCode"
    AppDataNotExist = "AppDataNotExist"
    NessaryDataMissing = "NessaryDataMissing"
    TradePwdChanged = "TradePwdChanged"
    EnableDeviceLock = "EnableDeviceLock"

    def load_dic(self):
        return {
            self.NONE: Notify_pb2.GtwEventType_None,
            self.LocalCfgLoadFailed: Notify_pb2.GtwEventType_LocalCfgLoadFailed,
            self.APISvrRunFailed: Notify_pb2.GtwEventType_APISvrRunFailed,
            self.ForceUpdate: Notify_pb2.GtwEventType_ForceUpdate,
            self.LoginFailed: Notify_pb2.GtwEventType_LoginFailed,
            self.UnAgreeDisclaimer: Notify_pb2.GtwEventType_UnAgreeDisclaimer,
            self.NetCfgMissing: Notify_pb2.GtwEventType_NetCfgMissing,
            self.KickedOut: Notify_pb2.GtwEventType_KickedOut,
            self.LoginPwdChanged: Notify_pb2.GtwEventType_LoginPwdChanged,
            self.BanLogin: Notify_pb2.GtwEventType_BanLogin,
            self.NeedPicVerifyCode: Notify_pb2.GtwEventType_NeedPicVerifyCode,
            self.NeedPhoneVerifyCode: Notify_pb2.GtwEventType_NeedPhoneVerifyCode,
            self.AppDataNotExist: Notify_pb2.GtwEventType_AppDataNotExist,
            self.NessaryDataMissing: Notify_pb2.GtwEventType_NessaryDataMissing,
            self.TradePwdChanged: Notify_pb2.GtwEventType_TradePwdChanged,
            self.EnableDeviceLock: Notify_pb2.GtwEventType_EnableDeviceLock,
        }

# 交易环境
class TrdEnv(FtEnum):
    """
    交易环境类型定义
    ..  py:class:: TrdEnv
     ..  py:attribute:: REAL
      真实环境
     ..  py:attribute:: SIMULATE
      模拟环境
    """
    REAL = "REAL"
    SIMULATE = "SIMULATE"

    def load_dic(self):
        return {
            self.REAL: Trd_Common_pb2.TrdEnv_Real,
            self.SIMULATE: Trd_Common_pb2.TrdEnv_Simulate,
        }

# 交易大市场， 不是具体品种
class TrdMarket(FtEnum):
    """
    交易市场类型定义
    ..  py:class:: TrdMarket
     ..  py:attribute:: NONE
      未知not
     ..  py:attribute:: HK
      港股交易
     ..  py:attribute:: US
      美股交易
     ..  py:attribute:: CN
      A股交易
     ..  py:attribute:: HKCC
      A股通交易
    """
    NONE = "N/A"   # 未知
    HK = "HK"      # 香港市场
    US = "US"      # 美国市场
    CN = "CN"      # 大陆市场
    HKCC = "HKCC"  # 香港A股通市场
    FUTURES = "FUTURES"  # 期货市场
    FUTURES_SIMULATE_HK = "FUTURES_SIMULATE_HK"
    FUTURES_SIMULATE_US = "FUTURES_SIMULATE_US"
    FUTURES_SIMULATE_SG = "FUTURES_SIMULATE_SG"
    FUTURES_SIMULATE_JP = "FUTURES_SIMULATE_JP"
    SG = "SG"
    AU = "AU"
    JP = "JP"
    MY = "MY"
    CA = "CA"
    HKFUND = "HKFUND"
    USFUND = "USFUND"
    SGFUND = "SGFUND"
    MYFUND = "MYFUND"
    JPFUND = "JPFUND"
    CRYPTO = "CRYPTO"  # 加密货币市场
    PREDICTION = "PREDICTION"

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.TrdMarket_Unknown,
            self.HK: Trd_Common_pb2.TrdMarket_HK,
            self.US: Trd_Common_pb2.TrdMarket_US,
            self.CN: Trd_Common_pb2.TrdMarket_CN,
            self.HKCC: Trd_Common_pb2.TrdMarket_HKCC,
            self.FUTURES: Trd_Common_pb2.TrdMarket_Futures,
            self.SG: Trd_Common_pb2.TrdMarket_SG,
            self.AU: Trd_Common_pb2.TrdMarket_AU,
            self.JP: Trd_Common_pb2.TrdMarket_JP,
            self.MY: Trd_Common_pb2.TrdMarket_MY,
            self.CA: Trd_Common_pb2.TrdMarket_CA,
            self.FUTURES_SIMULATE_HK: Trd_Common_pb2.TrdMarket_Futures_Simulate_HK,
            self.FUTURES_SIMULATE_US: Trd_Common_pb2.TrdMarket_Futures_Simulate_US,
            self.FUTURES_SIMULATE_SG: Trd_Common_pb2.TrdMarket_Futures_Simulate_SG,
            self.FUTURES_SIMULATE_JP: Trd_Common_pb2.TrdMarket_Futures_Simulate_JP,
            self.HKFUND: Trd_Common_pb2.TrdMarket_HK_Fund,
            self.USFUND: Trd_Common_pb2.TrdMarket_US_Fund,
            self.SGFUND: Trd_Common_pb2.TrdMarket_SG_Fund,
            self.MYFUND: Trd_Common_pb2.TrdMarket_MY_Fund,
            self.JPFUND: Trd_Common_pb2.TrdMarket_JP_Fund,
            self.CRYPTO: Trd_Common_pb2.TrdMarket_Crypto,
            self.PREDICTION: Trd_Common_pb2.TrdMarket_Prediction,
        }

# 持仓方向
class PositionSide(FtEnum):
    """
    持仓方向类型定义
    ..  py:class:: PositionSide
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: LONG
      多仓
     ..  py:attribute:: SHORT
      空仓
    """
    NONE = "N/A"
    LONG = "LONG"    # 多仓
    SHORT = "SHORT"  # 空仓

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.PositionSide_Unknown,
            self.LONG: Trd_Common_pb2.PositionSide_Long,
            self.SHORT: Trd_Common_pb2.PositionSide_Short,
        }

# 订单类型
class OrderType(FtEnum):
    """
    订单类型定义
    ..  py:class:: OrderType
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: NORMAL
      普通订单(港股的增强限价单、A股限价委托、美股的限价单)
     ..  py:attribute:: MARKET
      市价
     ..  py:attribute:: ABSOLUTE_LIMIT
      港股限价单(只有价格完全匹配才成交)
     ..  py:attribute:: AUCTION
      港股竞价单
     ..  py:attribute:: AUCTION_LIMIT
      港股竞价限价单
     ..  py:attribute:: SPECIAL_LIMIT
      港股特别限价(即市价IOC, 订单到达交易所后，或全部成交， 或部分成交再撤单， 或下单失败)
    """
    NONE = "N/A"
    NORMAL = "NORMAL"                               # 普通订单(港股的增强限价单、A股限价委托、美股的限价单)
    MARKET = "MARKET"                               # 市价
    ABSOLUTE_LIMIT = "ABSOLUTE_LIMIT"               # 港股_限价(只有价格完全匹配才成交)
    AUCTION = "AUCTION"                             # 港股_竞价
    AUCTION_LIMIT = "AUCTION_LIMIT"                 # 港股_竞价限价
    SPECIAL_LIMIT = "SPECIAL_LIMIT"                 # 港股_特别限价(即市价IOC, 订单到达交易所后，或全部成交， 或部分成交再撤单， 或下单失败)
    SPECIAL_LIMIT_ALL = "SPECIAL_LIMIT_ALL"         # 港股_特别限价(要么全部成交，要么自动撤单)
    STOP = "STOP"                                   # 止损市价单
    STOP_LIMIT = "STOP_LIMIT"                       # 止损限价单
    MARKET_IF_TOUCHED = "MARKET_IF_TOUCHED"         # 触及市价单(止盈)
    LIMIT_IF_TOUCHED = "LIMIT_IF_TOUCHED"           # 触及限价单(止盈)
    TRAILING_STOP = "TRAILING_STOP"                 # 跟踪止损市价单
    TRAILING_STOP_LIMIT = "TRAILING_STOP_LIMIT"     # 跟踪止损限价单
    TWAP = "TWAP"                                   # 算法订单TWAP市价单(仅展示)
    TWAP_LIMIT = "TWAP_LIMIT"                       # 算法订单TWAP限价单(仅展示)
    VWAP = "VWAP"                                   # 算法订单VWAP市价单(仅展示)
    VWAP_LIMIT = "VWAP_LIMIT"                       # 算法订单VWAP限价单(仅展示)

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.OrderType_Unknown,
            self.NORMAL: Trd_Common_pb2.OrderType_Normal,
            self.MARKET: Trd_Common_pb2.OrderType_Market,
            self.ABSOLUTE_LIMIT: Trd_Common_pb2.OrderType_AbsoluteLimit,
            self.AUCTION: Trd_Common_pb2.OrderType_Auction,
            self.AUCTION_LIMIT: Trd_Common_pb2.OrderType_AuctionLimit,
            self.SPECIAL_LIMIT: Trd_Common_pb2.OrderType_SpecialLimit,
            self.SPECIAL_LIMIT_ALL: Trd_Common_pb2.OrderType_SpecialLimit_All,
            self.STOP: Trd_Common_pb2.OrderType_Stop,
            self.STOP_LIMIT: Trd_Common_pb2.OrderType_StopLimit,
            self.MARKET_IF_TOUCHED: Trd_Common_pb2.OrderType_MarketifTouched,
            self.LIMIT_IF_TOUCHED: Trd_Common_pb2.OrderType_LimitifTouched,
            self.TRAILING_STOP: Trd_Common_pb2.OrderType_TrailingStop,
            self.TRAILING_STOP_LIMIT: Trd_Common_pb2.OrderType_TrailingStopLimit,
            self.TWAP: Trd_Common_pb2.OrderType_TWAP_MARKET,
            self.TWAP_LIMIT: Trd_Common_pb2.OrderType_TWAP_LIMIT,
            self.VWAP: Trd_Common_pb2.OrderType_VWAP_MARKET,
            self.VWAP_LIMIT: Trd_Common_pb2.OrderType_VWAP_LIMIT,
        }

# 订单类型
class TrailType(FtEnum):
    """
    跟踪止损类型定义
    ..  py:class:: TrailType
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: RATIO
      跟踪百分比
     ..  py:attribute:: AMOUNT
      跟踪额
    """
    NONE = "N/A"
    RATIO = "RATIO"  # 跟踪百分比
    AMOUNT = "AMOUNT"  # 跟踪额

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.TrailType_Unknown,
            self.RATIO: Trd_Common_pb2.TrailType_Ratio,
            self.AMOUNT: Trd_Common_pb2.TrailType_Amount,
        }

# 订单状态
class OrderStatus(FtEnum):
    """
    订单状态定义
    ..  py:class:: OrderStatus
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: UNSUBMITTED
      未提交
     ..  py:attribute:: WAITING_SUBMIT
      等待提交
     ..  py:attribute:: SUBMITTING
      提交中
     ..  py:attribute:: SUBMIT_FAILED
      提交失败，下单失败
     ..  py:attribute:: SUBMITTED
      已提交，等待成交
     ..  py:attribute:: FILLED_PART
      部分成交
     ..  py:attribute:: FILLED_ALL
      全部已成
     ..  py:attribute:: CANCELLING_PART
      正在撤单部分(部分已成交，正在撤销剩余部分)
     ..  py:attribute:: CANCELLING_ALL
      正在撤单全部
     ..  py:attribute:: CANCELLED_PART
      部分成交，剩余部分已撤单
     ..  py:attribute:: CANCELLED_ALL
      全部已撤单，无成交
     ..  py:attribute:: FAILED
      下单失败，服务拒绝
     ..  py:attribute:: DISABLED
      已失效
     ..  py:attribute:: DELETED
      已删除(无成交的订单才能删除)
    """
    NONE = "N/A"                                # 未知状态
    UNSUBMITTED = "UNSUBMITTED"                 # 未提交
    WAITING_SUBMIT = "WAITING_SUBMIT"           # 等待提交
    SUBMITTING = "SUBMITTING"                   # 提交中
    SUBMIT_FAILED = "SUBMIT_FAILED"             # 提交失败，下单失败
    TIMEOUT = "TIMEOUT"                         # 处理超时，结果未知
    SUBMITTED = "SUBMITTED"                     # 已提交，等待成交
    FILLED_PART = "FILLED_PART"                 # 部分成交
    FILLED_ALL = "FILLED_ALL"                   # 全部已成
    CANCELLING_PART = "CANCELLING_PART"         # 正在撤单_部分(部分已成交，正在撤销剩余部分)
    CANCELLING_ALL = "CANCELLING_ALL"           # 正在撤单_全部
    CANCELLED_PART = "CANCELLED_PART"           # 部分成交，剩余部分已撤单
    CANCELLED_ALL = "CANCELLED_ALL"             # 全部已撤单，无成交
    FAILED = "FAILED"                           # 下单失败，服务拒绝
    DISABLED = "DISABLED"                       # 已失效
    DELETED = "DELETED"                         # 已删除，无成交的订单才能删除
    FILL_CANCELLED = "FILL_CANCELLED"           # 成交被撤销，一般遇不到，意思是已经成交的订单被回滚撤销，成交无效变为废单

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.OrderStatus_Unknown,
            self.UNSUBMITTED: Trd_Common_pb2.OrderStatus_Unsubmitted,
            self.WAITING_SUBMIT: Trd_Common_pb2.OrderStatus_WaitingSubmit,
            self.SUBMITTING: Trd_Common_pb2.OrderStatus_Submitting,
            self.SUBMIT_FAILED: Trd_Common_pb2.OrderStatus_SubmitFailed,
            self.TIMEOUT: Trd_Common_pb2.OrderStatus_TimeOut,
            self.SUBMITTED: Trd_Common_pb2.OrderStatus_Submitted,
            self.FILLED_PART: Trd_Common_pb2.OrderStatus_Filled_Part,
            self.FILLED_ALL: Trd_Common_pb2.OrderStatus_Filled_All,
            self.CANCELLING_PART: Trd_Common_pb2.OrderStatus_Cancelling_Part,
            self.CANCELLING_ALL: Trd_Common_pb2.OrderStatus_Cancelling_All,
            self.CANCELLED_PART: Trd_Common_pb2.OrderStatus_Cancelled_Part,
            self.CANCELLED_ALL: Trd_Common_pb2.OrderStatus_Cancelled_All,
            self.FAILED: Trd_Common_pb2.OrderStatus_Failed,
            self.DISABLED: Trd_Common_pb2.OrderStatus_Disabled,
            self.DELETED: Trd_Common_pb2.OrderStatus_Deleted,
            self.FILL_CANCELLED: Trd_Common_pb2.OrderStatus_FillCancelled,
        }

class DealStatus(FtEnum):
    OK = 'OK'                 # 正常
    CANCELLED = 'CANCELLED'   # 成交被取消
    CHANGED = 'CHANGED'       # 成交被更改
    PAYOUT = 'PAYOUT'       # 赔付（仅事件合约）

    def load_dic(self):
        return {
            self.OK: Trd_Common_pb2.OrderFillStatus_OK,
            self.CANCELLED: Trd_Common_pb2.OrderFillStatus_Cancelled,
            self.CHANGED: Trd_Common_pb2.OrderFillStatus_Changed,
            self.PAYOUT: Trd_Common_pb2.OrderFillStatus_Payout,
        }


# 修改订单操作
class ModifyOrderOp(FtEnum):
    """
    修改订单操作类型定义
    ..  py:class:: ModifyOrderOp
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: NORMAL
      修改订单的数量、价格
     ..  py:attribute:: CANCEL
      取消订单
     ..  py:attribute:: DISABLE
      使订单失效
     ..  py:attribute:: ENABLE
      使订单生效
     ..  py:attribute:: DELETE
      删除订单
    """
    NONE = "N/A"
    NORMAL = "NORMAL"
    CANCEL = "CANCEL"
    DISABLE = "DISABLE"
    ENABLE = "ENABLE"
    DELETE = "DELETE"

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.ModifyOrderOp_Unknown,
            self.NORMAL: Trd_Common_pb2.ModifyOrderOp_Normal,
            self.CANCEL: Trd_Common_pb2.ModifyOrderOp_Cancel,
            self.DISABLE: Trd_Common_pb2.ModifyOrderOp_Disable,
            self.ENABLE: Trd_Common_pb2.ModifyOrderOp_Enable,
            self.DELETE: Trd_Common_pb2.ModifyOrderOp_Delete,
        }

# 交易方向 (客户端下单只传Buy或Sell即可，SELL_SHORT / BUY_BACK 服务器可能会传回
class TrdSide(FtEnum):
    """
    交易方向类型定义(客户端下单只传Buy或Sell即可，SELL_SHORT / BUY_BACK 服务器可能会传回)
    ..  py:class:: TrdSide
     ..  py:attribute:: NONE
      未知
    ..  py:attribute:: BUY
      买
     ..  py:attribute:: SELL
      卖
     ..  py:attribute:: SELL_SHORT
      卖空
     ..  py:attribute:: BUY_BACK
      买回
    """
    NONE = "N/A"
    BUY = "BUY"
    SELL = "SELL"
    SELL_SHORT = "SELL_SHORT"
    BUY_BACK = "BUY_BACK"

    def load_dic(self):
        return {
            TrdSide.NONE: Trd_Common_pb2.TrdSide_Unknown,
            TrdSide.BUY: Trd_Common_pb2.TrdSide_Buy,
            TrdSide.SELL: Trd_Common_pb2.TrdSide_Sell,
            TrdSide.SELL_SHORT: Trd_Common_pb2.TrdSide_SellShort,
            TrdSide.BUY_BACK: Trd_Common_pb2.TrdSide_BuyBack,
        }


class PredSide(FtEnum):
    """事件合约预测方向"""
    NONE = "N/A"
    YES = "YES"
    NO = "NO"

    def load_dic(self):
        return {
            self.NONE: Common_pb2.PredSide_Unknown,
            self.YES: Common_pb2.PredSide_Yes,
            self.NO: Common_pb2.PredSide_No,
        }


# 交易方向 (客户端下单只传Buy或Sell即可，SELL_SHORT / BUY_BACK 服务器可能会传回
class TrdCategory(FtEnum):
    """
    交易品类
    ..  py:class:: TrdCategory
    ..  py:attribute:: NONE
      未知
    ..  py:attribute:: SECURITY
      买
     ..  py:attribute:: FUTURE
      卖
    """
    NONE = "N/A"
    SECURITY = "SECURITY"
    FUTURE = "FUTURE"
    CRYPTO = "CRYPTO"

    def load_dic(self):
        return {
            TrdCategory.NONE: Trd_Common_pb2.TrdCategory_Unknown,
            TrdCategory.SECURITY: Trd_Common_pb2.TrdCategory_Security,
            TrdCategory.FUTURE: Trd_Common_pb2.TrdCategory_Future,
            TrdCategory.CRYPTO: Trd_Common_pb2.TrdCategory_Crypto,
        }


# 交易的支持能力，持续更新中
MKT_ENV_ENABLE_MAP = {
    (TrdMarket.NONE, TrdEnv.REAL): True,
    (TrdMarket.NONE, TrdEnv.SIMULATE): True,

    (TrdMarket.HK, TrdEnv.REAL): True,
    (TrdMarket.HK, TrdEnv.SIMULATE): True,

    (TrdMarket.US, TrdEnv.REAL): True,
    (TrdMarket.US, TrdEnv.SIMULATE): True,

    (TrdMarket.HKCC, TrdEnv.REAL): True,
    (TrdMarket.HKCC, TrdEnv.SIMULATE): False,

    (TrdMarket.CN, TrdEnv.REAL): False,
    (TrdMarket.CN, TrdEnv.SIMULATE): True,

    (TrdMarket.FUTURES, TrdEnv.REAL): True,
    (TrdMarket.FUTURES, TrdEnv.SIMULATE): True,

    (TrdMarket.SG, TrdEnv.REAL): True,
    (TrdMarket.SG, TrdEnv.SIMULATE): False,

    (TrdMarket.HKFUND, TrdEnv.REAL): True,
    (TrdMarket.HKFUND, TrdEnv.SIMULATE): False,

    (TrdMarket.USFUND, TrdEnv.REAL): True,
    (TrdMarket.USFUND, TrdEnv.SIMULATE): False,

    (TrdMarket.CA, TrdEnv.REAL): True,
    (TrdMarket.CA, TrdEnv.SIMULATE): False,

    (TrdMarket.MY, TrdEnv.REAL): True,
    (TrdMarket.MY, TrdEnv.SIMULATE): False,

    (TrdMarket.JP, TrdEnv.REAL): True,
    (TrdMarket.JP, TrdEnv.SIMULATE): False,

    (TrdMarket.CRYPTO, TrdEnv.REAL): True,
    (TrdMarket.CRYPTO, TrdEnv.SIMULATE): False,

    (TrdMarket.PREDICTION, TrdEnv.REAL): True,
    (TrdMarket.PREDICTION, TrdEnv.SIMULATE): False,
}

class TRADE(object):
    @staticmethod
    def check_mkt_envtype(trd_mkt, trd_env):
        if (trd_mkt, trd_env) in MKT_ENV_ENABLE_MAP:
            return MKT_ENV_ENABLE_MAP[trd_mkt, trd_env]
        return False


class SecurityReferenceType(FtEnum):
    """
    股票关联数据类型
    ..  py:class:: SecurityReferenceType
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: WARRANT
     相关窝轮
    """
    NONE = 'N/A'
    WARRANT = 'WARRANT'
    FUTURE = 'FUTURE'

    def load_dic(self):
        return {
           self.NONE: Qot_GetReference_pb2.ReferenceType_Unknow,
           self.WARRANT: Qot_GetReference_pb2.ReferenceType_Warrant,
           self.FUTURE: Qot_GetReference_pb2.ReferenceType_Future,
        }


'''-------------------------WarrantType----------------------------'''


#
class WrtType(FtEnum):
    NONE = "N/A"                                       # 未知
    CALL = "CALL"                                      # 认购
    PUT = "PUT"                                        # 认沽
    BULL = "BULL"                                      # 牛
    BEAR = "BEAR"                                      # 熊
    INLINE = "INLINE"                                  # 界内证

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.WarrantType_Unknown,
            self.CALL: Qot_Common_pb2.WarrantType_Buy,
            self.PUT: Qot_Common_pb2.WarrantType_Sell,
            self.BULL: Qot_Common_pb2.WarrantType_Bull,
            self.BEAR: Qot_Common_pb2.WarrantType_Bear,
            self.INLINE: Qot_Common_pb2.WarrantType_InLine
        }


'''-------------------------SortField----------------------------'''


# 窝轮排序
class SortField(FtEnum):
    NONE = "N/A"                                       # 未知
    CODE = "CODE"                                      # 代码
    CUR_PRICE = "CUR_PRICE"                            # 最新价
    PRICE_CHANGE_VAL = "PRICE_CHANGE_VAL"              # 涨跌额
    CHANGE_RATE = "CHANGE_RATE"                        # 涨跌幅%
    STATUS = "STATUS"                                  # 状态
    BID_PRICE = "BID_PRICE"                            # 买入价
    ASK_PRICE = "ASK_PRICE"                            # 卖出价
    BID_VOL = "BID_VOL"                                # 买量
    ASK_VOL = "ASK_VOL"                                # 卖量
    VOLUME = "VOLUME"                                  # 成交量
    TURNOVER = "TURNOVER"                              # 成交额
    SCORE = "SCORE"                                    # 综合评分
    PREMIUM = "PREMIUM"                                # 溢价%
    EFFECTIVE_LEVERAGE = "EFFECTIVE_LEVERAGE"          # 有效杠杆
    DELTA = "DELTA"                                    # 对冲值,仅认购认沽支持该字段
    IMPLIED_VOLATILITY = "IMPLIED_VOLATILITY"          # 引伸波幅,仅认购认沽支持该字段
    TYPE = "TYPE"                                      # 类型
    STRIKE_PRICE = "STRIKE_PRICE"                      # 行权价
    BREAK_EVEN_POINT = "BREAK_EVEN_POINT"              # 打和点
    MATURITY_TIME = "MATURITY_TIME"                    # 到期日
    LIST_TIME = "LIST_TIME"                            # 上市日期
    LAST_TRADE_TIME = "LAST_TRADE_TIME"                # 最后交易日
    LEVERAGE = "LEVERAGE"                              # 杠杆比率
    IN_OUT_MONEY = "IN_OUT_MONEY"                      # 价内/价外%
    RECOVERY_PRICE = "RECOVERY_PRICE"                  # 收回价,仅牛熊证支持该字段
    CHANGE_PRICE = "CHANGE_PRICE"                      # 换股价
    CHANGE = "CHANGE"                                  # 换股比率
    STREET_RATE = "STREET_RATE"                        # 街货比%
    STREET_VOL = "STREET_VOL"                          # 街货量
    AMPLITUDE = "AMPLITUDE"                            # 振幅%
    WARRANT_NAME = "WARRANT_NAME"                      # 名称
    ISSUER = "ISSUER"                                  # 发行人
    LOT_SIZE = "LOT_SIZE"                              # 每手
    ISSUE_SIZE = "ISSUE_SIZE"                          # 发行量
    PRE_CUR_PRICE = "PRE_CUR_PRICE"  # 盘前最新价
    AFTER_CUR_PRICE = "AFTER_CUR_PRICE"  # 盘后最新价
    PRE_PRICE_CHANGE_VAL = "PRE_PRICE_CHANGE_VAL"  # 盘前涨跌额
    AFTER_PRICE_CHANGE_VAL = "AFTER_PRICE_CHANGE_VAL"  # 盘后涨跌额
    PRE_CHANGE_RATE = "PRE_CHANGE_RATE"  # 盘前涨跌幅%
    AFTER_CHANGE_RATE = "AFTER_CHANGE_RATE"  # 盘后涨跌幅%
    PRE_AMPLITUDE = "PRE_AMPLITUDE"  # 盘前振幅%
    AFTER_AMPLITUDE = "AFTER_AMPLITUDE"  # 盘后振幅%
    PRE_TURNOVER = "PRE_TURNOVER"  # 盘前成交额
    AFTER_TURNOVER = "AFTER_TURNOVER"  # 盘后成交额
    UPPER_STRIKE_PRICE = "UPPER_STRIKE_PRICE"  # 上限价，仅界内证支持该字段
    LOWER_STRIKE_PRICE = "LOWER_STRIKE_PRICE"  # 下限价，仅界内证支持该字段
    INLINE_PRICE_STATUS = "INLINE_PRICE_STATUS"  # 界内界外，仅界内证支持该字段

    LAST_SETTLE_PRICE = "LAST_SETTLE_PRICE" #期货昨结
    POSITION = "POSITION"  # 期货持仓量
    POSITION_CHANGE = "POSITION_CHANGE"  # 期货日持仓

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.SortField_Unknow,
            self.CODE: Qot_Common_pb2.SortField_Code,
            self.CUR_PRICE: Qot_Common_pb2.SortField_CurPrice,
            self.PRICE_CHANGE_VAL: Qot_Common_pb2.SortField_PriceChangeVal,
            self.CHANGE_RATE: Qot_Common_pb2.SortField_ChangeRate,
            self.STATUS: Qot_Common_pb2.SortField_Status,
            self.BID_PRICE: Qot_Common_pb2.SortField_BidPrice,
            self.ASK_PRICE: Qot_Common_pb2.SortField_AskPrice,
            self.BID_VOL: Qot_Common_pb2.SortField_BidVol,
            self.ASK_VOL: Qot_Common_pb2.SortField_AskVol,
            self.VOLUME: Qot_Common_pb2.SortField_Volume,
            self.TURNOVER: Qot_Common_pb2.SortField_Turnover,
            self.SCORE: Qot_Common_pb2.SortField_Score,
            self.PREMIUM: Qot_Common_pb2.SortField_Premium,
            self.EFFECTIVE_LEVERAGE: Qot_Common_pb2.SortField_EffectiveLeverage,
            self.DELTA: Qot_Common_pb2.SortField_Delta,
            self.IMPLIED_VOLATILITY: Qot_Common_pb2.SortField_ImpliedVolatility,
            self.TYPE: Qot_Common_pb2.SortField_Type,
            self.STRIKE_PRICE: Qot_Common_pb2.SortField_StrikePrice,
            self.BREAK_EVEN_POINT: Qot_Common_pb2.SortField_BreakEvenPoint,
            self.MATURITY_TIME: Qot_Common_pb2.SortField_MaturityTime,
            self.LIST_TIME: Qot_Common_pb2.SortField_ListTime,
            self.LAST_TRADE_TIME: Qot_Common_pb2.SortField_LastTradeTime,
            self.LEVERAGE: Qot_Common_pb2.SortField_Leverage,
            self.IN_OUT_MONEY: Qot_Common_pb2.SortField_InOutMoney,
            self.RECOVERY_PRICE: Qot_Common_pb2.SortField_RecoveryPrice,
            self.CHANGE_PRICE: Qot_Common_pb2.SortField_ChangePrice,
            self.CHANGE: Qot_Common_pb2.SortField_Change,
            self.STREET_RATE: Qot_Common_pb2.SortField_StreetRate,
            self.STREET_VOL: Qot_Common_pb2.SortField_StreetVol,
            self.AMPLITUDE: Qot_Common_pb2.SortField_Amplitude,
            self.WARRANT_NAME: Qot_Common_pb2.SortField_WarrantName,
            self.ISSUER: Qot_Common_pb2.SortField_Issuer,
            self.LOT_SIZE: Qot_Common_pb2.SortField_LotSize,
            self.ISSUE_SIZE: Qot_Common_pb2.SortField_IssueSize,
            self.PRE_CUR_PRICE: Qot_Common_pb2.SortField_PreCurPrice,
            self.AFTER_CUR_PRICE: Qot_Common_pb2.SortField_AfterCurPrice,
            self.PRE_PRICE_CHANGE_VAL: Qot_Common_pb2.SortField_PrePriceChangeVal,
            self.AFTER_PRICE_CHANGE_VAL: Qot_Common_pb2.SortField_AfterPriceChangeVal,
            self.PRE_CHANGE_RATE: Qot_Common_pb2.SortField_PreChangeRate,
            self.AFTER_CHANGE_RATE: Qot_Common_pb2.SortField_AfterChangeRate,
            self.PRE_AMPLITUDE: Qot_Common_pb2.SortField_PreAmplitude,
            self.AFTER_AMPLITUDE: Qot_Common_pb2.SortField_AfterAmplitude,
            self.PRE_TURNOVER: Qot_Common_pb2.SortField_PreTurnover,
            self.AFTER_TURNOVER: Qot_Common_pb2.SortField_AfterTurnover,
            self.UPPER_STRIKE_PRICE: Qot_Common_pb2.SortField_UpperStrikePrice,
            self.LOWER_STRIKE_PRICE: Qot_Common_pb2.SortField_LowerStrikePrice,
            self.INLINE_PRICE_STATUS: Qot_Common_pb2.SortField_InLinePriceStatus,
            self.LAST_SETTLE_PRICE: Qot_Common_pb2.SortField_LastSettlePrice,
            self.POSITION: Qot_Common_pb2.SortField_Position,
            self.POSITION_CHANGE: Qot_Common_pb2.SortField_PositionChange,
        }


'''-------------------------IpoPeriod----------------------------'''


# 窝轮上市日
class IpoPeriod(FtEnum):
    NONE = "N/A"                                       # 未知
    TODAY = "TODAY"                                    # 今日上市
    TOMORROW = "TOMORROW"                              # 明日上市
    NEXTWEEK = "NEXTWEEK"                              # 未来一周上市
    LASTWEEK = "LASTWEEK"                              # 过去一周上市
    LASTMONTH = "LASTMONTH"                            # 过去一月上市

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.IpoPeriod_Unknow,
            self.TODAY: Qot_Common_pb2.IpoPeriod_Today,
            self.TOMORROW: Qot_Common_pb2.IpoPeriod_Tomorrow,
            self.NEXTWEEK: Qot_Common_pb2.IpoPeriod_Nextweek,
            self.LASTWEEK: Qot_Common_pb2.IpoPeriod_Lastweek,
            self.LASTMONTH: Qot_Common_pb2.IpoPeriod_Lastmonth
        }


'''-------------------------PriceType----------------------------'''


# 窝轮价外/内,界内证表示界内界外
class PriceType(FtEnum):
    NONE = "N/A"                                       # 未知
    OUTSIDE = "OUTSIDE"                                # 价外,界内证表示界外
    WITH_IN = "WITH_IN"                                # 价内,界内证表示界内

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PriceType_Unknow,
            self.OUTSIDE: Qot_Common_pb2.PriceType_Outside,
            self.WITH_IN: Qot_Common_pb2.PriceType_WithIn
        }


'''-------------------------WarrantStatus----------------------------'''


# 窝轮状态
class WarrantStatus(FtEnum):
    NONE = "N/A"                                       # 未知
    NORMAL = "NORMAL"                                  # 正常状态
    SUSPEND = "SUSPEND"                                # 停牌
    STOP_TRADE = "STOP_TRADE"                          # 终止交易
    PENDING_LISTING = "PENDING_LISTING"                # 等待上市

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.WarrantStatus_Unknow,
            self.NORMAL: Qot_Common_pb2.WarrantStatus_Normal,
            self.SUSPEND: Qot_Common_pb2.WarrantStatus_Suspend,
            self.STOP_TRADE: Qot_Common_pb2.WarrantStatus_StopTrade,
            self.PENDING_LISTING: Qot_Common_pb2.WarrantStatus_PendingListing
        }


'''-------------------------Issuer----------------------------'''


# 窝轮发行人
class Issuer(FtEnum):
    NONE = "N/A"                                       # 未知
    SG = "SG"                                          # 法兴
    BP = "BP"                                          # 法巴
    CS = "CS"                                          # 瑞信
    CT = "CT"                                          # 花旗
    EA = "EA"                                          # 东亚
    GS = "GS"                                          # 高盛
    HS = "HS"                                          # 汇丰
    JP = "JP"                                          # 摩通
    MB = "MB"                                          # 麦银
    SC = "SC"                                          # 渣打
    UB = "UB"                                          # 瑞银
    BI = "BI"                                          # 中银
    DB = "DB"                                          # 德银
    DC = "DC"                                          # 大和
    ML = "ML"                                          # 美林
    NM = "NM"                                          # 野村
    RB = "RB"                                          # 荷合
    RS = "RS"                                          # 苏皇
    BC = "BC"                                          # 巴克莱
    HT = "HT"                                          # 海通
    VT = "VT"                                          # 瑞通
    KC = "KC"                                          # 比联
    MS = "MS"                                          # 摩利
    GJ = "GJ"                                          # 国君
    XZ = "XZ"                                          # 星展
    HU = "HU"                                          # 华泰
    KS = "KS"                                          # 韩投
    CI = "CI"                                          # 信证


    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.Issuer_Unknow,
            self.SG: Qot_Common_pb2.Issuer_SG,
            self.BP: Qot_Common_pb2.Issuer_BP,
            self.CS: Qot_Common_pb2.Issuer_CS,
            self.CT: Qot_Common_pb2.Issuer_CT,
            self.EA: Qot_Common_pb2.Issuer_EA,
            self.GS: Qot_Common_pb2.Issuer_GS,
            self.HS: Qot_Common_pb2.Issuer_HS,
            self.JP: Qot_Common_pb2.Issuer_JP,
            self.MB: Qot_Common_pb2.Issuer_MB,
            self.SC: Qot_Common_pb2.Issuer_SC,
            self.UB: Qot_Common_pb2.Issuer_UB,
            self.BI: Qot_Common_pb2.Issuer_BI,
            self.DB: Qot_Common_pb2.Issuer_DB,
            self.DC: Qot_Common_pb2.Issuer_DC,
            self.ML: Qot_Common_pb2.Issuer_ML,
            self.NM: Qot_Common_pb2.Issuer_NM,
            self.RB: Qot_Common_pb2.Issuer_RB,
            self.RS: Qot_Common_pb2.Issuer_RS,
            self.BC: Qot_Common_pb2.Issuer_BC,
            self.HT: Qot_Common_pb2.Issuer_HT,
            self.VT: Qot_Common_pb2.Issuer_VT,
            self.KC: Qot_Common_pb2.Issuer_KC,
            self.MS: Qot_Common_pb2.Issuer_MS,
            self.GJ: Qot_Common_pb2.Issuer_GJ,
            self.XZ: Qot_Common_pb2.Issuer_XZ,
            self.HU: Qot_Common_pb2.Issuer_HU,
            self.KS: Qot_Common_pb2.Issuer_KS,
            self.CI: Qot_Common_pb2.Issuer_CI
        }


'''-------------------------TradeDateType----------------------------'''


# 交易时间类型
class TradeDateType(FtEnum):
    WHOLE = "WHOLE"                                    # 全天交易
    MORNING = "MORNING"                                # 上午交易，下午休市
    AFTERNOON = "AFTERNOON"                            # 下午交易，上午休市

    def load_dic(self):
        return {
            self.WHOLE: Qot_Common_pb2.TradeDateType_Whole,
            self.MORNING: Qot_Common_pb2.TradeDateType_Morning,
            self.AFTERNOON: Qot_Common_pb2.TradeDateType_Afternoon
        }


'''-------------------------行情权限----------------------------'''


# 行情权限
class QotRight(FtEnum):
    NONE = "N/A"                                       # 未知
    BMP = "BMP"                                        # Bmp，无法订阅
    LEVEL1 = "LV1"                                  # Level1
    LEVEL2 = "LV2"                                  # Level2
    SF = "SF"
    NO = "NO"
    LEVEL3 = "LV3"                                  # Level3

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.QotRight_Unknow,
            self.BMP: Qot_Common_pb2.QotRight_Bmp,
            self.LEVEL1: Qot_Common_pb2.QotRight_Level1,
            self.LEVEL2: Qot_Common_pb2.QotRight_Level2,
            self.SF: Qot_Common_pb2.QotRight_SF,
            self.NO: Qot_Common_pb2.QotRight_No,
            self.LEVEL3: Qot_Common_pb2.QotRight_Level3
        }


'''-------------------------验证码操作----------------------------'''

#


class VerificationOp(FtEnum):
    NONE = "N/A"                                       # 未知操作
    REQUEST = "REQUEST"                                # 请求验证码
    INPUT_AND_LOGIN = "INPUT_AND_LOGIN"                # 输入验证码并继续登录操作

    def load_dic(self):
        return {
            self.NONE: Verification_pb2.VerificationOp_Unknow,
            self.REQUEST: Verification_pb2.VerificationOp_Request,
            self.INPUT_AND_LOGIN: Verification_pb2.VerificationOp_InputAndLogin
        }


'''-------------------------验证码类型----------------------------'''


#
class VerificationType(FtEnum):
    NONE = "N/A"                                       # 未知操作
    PICTURE = "PICTURE"                                # 图形验证码
    PHONE = "PHONE"                                    # 手机验证码

    def load_dic(self):
        return {
            self.NONE: Verification_pb2.VerificationType_Unknow,
            self.PICTURE: Verification_pb2.VerificationType_Picture,
            self.PHONE: Verification_pb2.VerificationType_Phone
        }


'''-------------------------被强制退出登录,例如修改了登录密码,中途打开设备锁等,详细原因在描述返回----------------------------'''


class ProgramStatusType(FtEnum):
    NONE = "N/A"                                       # 未知
    # 已完成类似加载配置,启动服务器等操作,服务器启动之前的状态无需返回
    LOADED = "LOADED"
    LOGING = "LOGING"                                  # 登录中
    NEED_PIC_VERIFY_CODE = "NEED_PIC_VERIFY_CODE"      # 需要图形验证码
    NEED_PHONE_VERIFY_CODE = "NEED_PHONE_VERIFY_CODE"  # 需要手机验证码
    LOGIN_FAILED = "LOGIN_FAILED"                      # 登录失败,详细原因在描述返回
    FORCE_UPDATE = "FORCE_UPDATE"                      # 客户端版本过低
    NESSARY_DATA_PREPARING = "NESSARY_DATA_PREPARING"  # 正在拉取类似免责声明等一些必要信息
    NESSARY_DATA_MISSING = "NESSARY_DATA_MISSING"      # 缺少必要信息
    UN_AGREE_DISCLAIMER = "UN_AGREE_DISCLAIMER"        # 未同意免责声明
    READY = "READY"                                    # 可以接收业务协议收发,正常可用状态
    # OpenD登录后被强制退出登录，会导致连接全部断开,需要重连后才能得到以下该状态（并且需要在ui模式下）
    FORCE_LOGOUT = "FORCE_LOGOUT"

    def load_dic(self):
        return {
            self.NONE: Common_pb2.ProgramStatusType_None,
            self.LOADED: Common_pb2.ProgramStatusType_Loaded,
            self.LOGING: Common_pb2.ProgramStatusType_Loging,
            self.NEED_PIC_VERIFY_CODE: Common_pb2.ProgramStatusType_NeedPicVerifyCode,
            self.NEED_PHONE_VERIFY_CODE: Common_pb2.ProgramStatusType_NeedPhoneVerifyCode,
            self.LOGIN_FAILED: Common_pb2.ProgramStatusType_LoginFailed,
            self.FORCE_UPDATE: Common_pb2.ProgramStatusType_ForceUpdate,
            self.NESSARY_DATA_PREPARING: Common_pb2.ProgramStatusType_NessaryDataPreparing,
            self.NESSARY_DATA_MISSING: Common_pb2.ProgramStatusType_NessaryDataMissing,
            self.UN_AGREE_DISCLAIMER: Common_pb2.ProgramStatusType_UnAgreeDisclaimer,
            self.READY: Common_pb2.ProgramStatusType_Ready,
            self.FORCE_LOGOUT: Common_pb2.ProgramStatusType_ForceLogout
        }


class ContextStatus:
    START = 'START'
    CONNECTING = 'CONNECTING'
    CONNECTED = 'CONNECTED'
    READY = 'READY'
    CLOSING = 'CLOSING'
    CLOSED = 'CLOSED'
    WAIT_RECONNECT = 'WAIT_RECONNECT'


class UserInfoField:
    BASIC = 1
    API = 2
    QOTRIGHT = 4
    DISCLAIMER = 8
    UPDATE = 16
    WEBKEY = 2048

    @classmethod
    def fields_to_flag_val(cls, fields):
        list_ret = []
        for x in fields:
            if x not in list_ret:
                list_ret.append(x)

        ret_flags = 0
        for x in list_ret:
            ret_flags += x
        return ret_flags


class UpdateType(FtEnum):
    NO = "NO"
    ADVICE = "ADVICE"
    FORCE = "FORCE"

    def load_dic(self):
        return {
            self.NO: GetUserInfo_pb2.UpdateType_None,
            self.ADVICE: GetUserInfo_pb2.UpdateType_Advice,
            self.FORCE: GetUserInfo_pb2.UpdateType_Force
        }


'''-------------------------DelayStatisticsType----------------------------'''

#


class DelayStatisticsType(FtEnum):
    NONE = "N/A"                                       # 未知类型
    QOT_PUSH = "QOT_PUSH"                              # 行情推送统计
    REQ_REPLY = "REQ_REPLY"                            # 请求回应统计
    PLACE_ORDER = "PLACE_ORDER"                        # 下单统计
    ALL = [QOT_PUSH, REQ_REPLY, PLACE_ORDER]

    describe_dict = {
        QOT_PUSH: "行情推送统计",
        REQ_REPLY: "请求回应统计",
        PLACE_ORDER: "下单统计",
    }

    def load_dic(self):
        return {
            self.NONE: GetDelayStatistics_pb2.DelayStatisticsType_Unkonw,
            self.QOT_PUSH: GetDelayStatistics_pb2.DelayStatisticsType_QotPush,
            self.REQ_REPLY: GetDelayStatistics_pb2.DelayStatisticsType_ReqReply,
            self.PLACE_ORDER: GetDelayStatistics_pb2.DelayStatisticsType_PlaceOrder
        }

    @classmethod
    def get_describe(cls, t):
        obj = cls()
        return obj.describe_dict[t]


'''-------------------------QotPushStage----------------------------'''


# 某段时间的统计数据，SR表示服务器收到数据，目前只有港股支持SR字段，SS表示服务器发出数据，CR表示OpenD收到数据，CS表示OpenD发出数据
class QotPushStage(FtEnum):
    NONE = "N/A"                                       # 未知
    SR2_SS = "SR2_SS"                                  # 统计服务端处理耗时
    SS2_CR = "SS2_CR"                                  # 统计网络耗时
    CR2_CS = "CR2_CS"                                  # 统计OpenD处理耗时
    SS2_CS = "SS2_CS"                                  # 统计服务器发出到OpenD发出的处理耗时
    SR2_CS = "SR2_CS"                                  # 统计服务器收到数据到OpenD发出的处理耗时
    ALL = [SR2_SS, SS2_CR, CR2_CS, SS2_CS, SR2_CS]

    describe_dict = {
        SR2_SS: "统计服务端处理耗时",
        SS2_CR: "统计网络耗时",
        CR2_CS: "统计OpenD处理耗时",
        SS2_CS: "统计服务器发出到OpenD发出的处理耗时",
        SR2_CS: "统计服务器收到数据到OpenD发出的处理耗时(也就是从交易所到用户的总时间，港股市场数据最全，A股和美股部分缺乏交易所下发时间）",
    }

    def load_dic(self):
        return {
            self.NONE: GetDelayStatistics_pb2.QotPushStage_Unkonw,
            self.SR2_SS: GetDelayStatistics_pb2.QotPushStage_SR2SS,
            self.SS2_CR: GetDelayStatistics_pb2.QotPushStage_SS2CR,
            self.CR2_CS: GetDelayStatistics_pb2.QotPushStage_CR2CS,
            self.SS2_CS: GetDelayStatistics_pb2.QotPushStage_SS2CS,
            self.SR2_CS: GetDelayStatistics_pb2.QotPushStage_SR2CS
        }

    @classmethod
    def get_describe(cls, t):
        obj = cls()
        return obj.describe_dict[t]


'''-------------------------QotPushType----------------------------'''


# 行情推送类型
class QotPushType(FtEnum):
    NONE = "N/A"                                       # 未知
    PRICE = "PRICE"                                    # 最新价
    TICKER = "TICKER"                                  # 逐笔
    ORDER_BOOK = "ORDER_BOOK"                          # 摆盘
    BROKER = "BROKER"                                  # 经纪队列

    describe_dict = {
        PRICE: "最新价",
        TICKER: "逐笔",
        ORDER_BOOK: "摆盘",
        BROKER: "经纪队列",
    }

    def load_dic(self):
        return {
            self.NONE: GetDelayStatistics_pb2.QotPushType_Unkonw,
            self.PRICE: GetDelayStatistics_pb2.QotPushType_Price,
            self.TICKER: GetDelayStatistics_pb2.QotPushType_Ticker,
            self.ORDER_BOOK: GetDelayStatistics_pb2.QotPushType_OrderBook,
            self.BROKER: GetDelayStatistics_pb2.QotPushType_Broker
        }

    @classmethod
    def get_describe(cls, t):
        obj = cls()
        return obj.describe_dict[t]


'''-------------------------ModifyUserSecurityOp----------------------------'''


# 自选股操作
class ModifyUserSecurityOp(FtEnum):
    NONE = "N/A"                                       # 未知
    ADD = "ADD"                                        # 新增
    DEL = "DEL"                                        # 删除
    MOVE_OUT = "MOVE_OUT"                                # 移出

    def load_dic(self):
        return {
            self.NONE: Qot_ModifyUserSecurity_pb2.ModifyUserSecurityOp_Unknown,
            self.ADD: Qot_ModifyUserSecurity_pb2.ModifyUserSecurityOp_Add,
            self.DEL: Qot_ModifyUserSecurity_pb2.ModifyUserSecurityOp_Del,
            self.MOVE_OUT: Qot_ModifyUserSecurity_pb2.ModifyUserSecurityOp_MoveOut
        }


# 账户类型
class TrdAccType(FtEnum):
    NONE = 'N/A'     # 未知类型
    CASH = 'CASH'           # 现金账户
    MARGIN = 'MARGIN'       # 保证金账户
    TFSA = 'TFSA'       # 加拿大免税账户
    RRSP = 'RRSP'       # 加拿大注册退休账户
    SRRSP = 'SRRSP'       # 加拿大配偶退休账户
    DERIVATIVES = 'DERIVATIVES'       # 日本衍生品账户

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.TrdAccType_Unknown,
            self.CASH: Trd_Common_pb2.TrdAccType_Cash,
            self.MARGIN: Trd_Common_pb2.TrdAccType_Margin,
            self.TFSA: Trd_Common_pb2.TrdAccType_TFSA,
            self.RRSP: Trd_Common_pb2.TrdAccType_RRSP,
            self.SRRSP: Trd_Common_pb2.TrdAccType_SRRSP,
            self.DERIVATIVES: Trd_Common_pb2.TrdAccType_Derivatives,
        }
    
# 账户状态
class TrdAccStatus(FtEnum):
    ACTIVE = 'ACTIVE'         # 生效账户
    DISABLED = 'DISABLED'       # 失效账户

    def load_dic(self):
        return {
            self.ACTIVE: Trd_Common_pb2.TrdAccStatus_Active,
            self.DISABLED: Trd_Common_pb2.TrdAccStatus_Disabled
        }


# 账户类型
class TrdAccRole(FtEnum):
    NONE = 'N/A'  # 未知类型
    NORMAL = 'NORMAL'  # 普通账户
    MASTER = 'MASTER'  # 主账户
    IPO = 'IPO'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.TrdAccRole_Unknown,
            self.NORMAL: Trd_Common_pb2.TrdAccRole_Normal,
            self.MASTER: Trd_Common_pb2.TrdAccRole_Master,
            self.IPO: Trd_Common_pb2.TrdAccRole_IPO,
        }


'''-------------------------StockFilter 选股----------------------------'''


# 选股排序

class SortDir(FtEnum):
    NONE = "N/A"                                       # 不排序
    ASCEND = "ASCEND"                                  # 升序
    DESCEND = "DESCEND"                                # 降序

    def load_dic(self):
        return {
            self.NONE: Qot_StockFilter_pb2.SortDir_No,
            self.ASCEND: Qot_StockFilter_pb2.SortDir_Ascend,
            self.DESCEND: Qot_StockFilter_pb2.SortDir_Descend
        }

# 简单属性


class StockField(FtEnum):
    NONE = "N/A"                                       # 未知
    # 以下是简单数据过滤所支持的枚举
    simple_enum_begin = 0
    STOCK_CODE = "STOCK_CODE"                          # 股票代码，不能填区间上下限值。
    STOCK_NAME = "STOCK_NAME"                          # 股票名称，不能填区间上下限值。
    CUR_PRICE = "CUR_PRICE"                            # 最新价 例如填写[10,20]值区间
    # (现价 - 52周最高)/52周最高，对应PC端离52周高点百分比 例如填写[-30,-10]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%，如20实际对应20%）
    CUR_PRICE_TO_HIGHEST52_WEEKS_RATIO = "CUR_PRICE_TO_HIGHEST52_WEEKS_RATIO"
    # (现价 - 52周最低)/52周最低，对应PC端离52周低点百分比 例如填写[20,40]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    CUR_PRICE_TO_LOWEST52_WEEKS_RATIO = "CUR_PRICE_TO_LOWEST52_WEEKS_RATIO"
    # (今日最高 - 52周最高)/52周最高 例如填写[-3,-1]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    HIGH_PRICE_TO_HIGHEST52_WEEKS_RATIO = "HIGH_PRICE_TO_HIGHEST52_WEEKS_RATIO"
    # (今日最低 - 52周最低)/52周最低 例如填写[10,70]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    LOW_PRICE_TO_LOWEST52_WEEKS_RATIO = "LOW_PRICE_TO_LOWEST52_WEEKS_RATIO"
    VOLUME_RATIO = "VOLUME_RATIO"                      # 量比 例如填写[0.5,30]值区间
    BID_ASK_RATIO = "BID_ASK_RATIO"                    # 委比 例如填写[-20,80.5]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    LOT_PRICE = "LOT_PRICE"                            # 每手价格 例如填写[40,100]值区间
    # 市值 例如填写[50000000,3000000000]值区间
    MARKET_VAL = "MARKET_VAL"
    # 市盈率 (静态) 例如填写[-8,65.3]值区间
    PE_ANNUAL = "PE_ANNUAL"
    # 市盈率TTM 例如填写[-10,20.5]值区间
    PE_TTM = "PE_TTM"
    PB_RATE = "PB_RATE"                                # 市净率 例如填写[0.5,20]值区间
    CHANGE_RATE_5MIN = "CHANGE_RATE_5MIN"              # 五分钟价格涨跌幅 例如填写[-5,6.3]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    CHANGE_RATE_BEGIN_YEAR = "CHANGE_RATE_BEGIN_YEAR"  # 年初至今价格涨跌幅 例如填写[-50.1,400.7]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    PS_TTM = "PS_TTM"                                  # 市销率(TTM) 例如填写 [100, 500] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    PCF_TTM = "PCF_TTM"                                # 市现率(TTM) 例如填写 [100, 1000] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    TOTAL_SHARE = "TOTAL_SHARE"                        # 总股数 例如填写 [1000000000,1000000000] 值区间 (单位：股)
    FLOAT_SHARE = "FLOAT_SHARE"                        # 流通股数 例如填写 [1000000000,1000000000] 值区间 (单位：股)
    FLOAT_MARKET_VAL = "FLOAT_MARKET_VAL"              # 流通市值 例如填写 [1000000000,1000000000] 值区间 (单位：元)

    # 以下是累积数据过滤所支持的枚举
    acc_enum_begin = 100
    CHANGE_RATE = "CHANGE_RATE"                        # 涨跌幅 例如填写[-10.2,20.4]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    AMPLITUDE = "AMPLITUDE"                            # 振幅 例如填写[0.5,20.6]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    VOLUME = "VOLUME"                                  # 日均成交量 例如填写[2000,70000]值区间
    TURNOVER = "TURNOVER"                              # 日均成交额 例如填写[1400,890000]值区间
    TURNOVER_RATE = "TURNOVER_RATE"                    # 换手率 例如填写[2,30]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）

    # 以下是财务数据过滤所支持的枚举
    financial_enum_begin = 200
    NET_PROFIT = "NET_PROFIT"                          # 净利润 例如填写[100000000,2500000000]值区间
    NET_PROFIX_GROWTH = "NET_PROFIX_GROWTH"            # 净利润增长率 例如填写[-10,300]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    SUM_OF_BUSINESS = "SUM_OF_BUSINESS"                # 营业收入 例如填写[100000000,6400000000]值区间
    SUM_OF_BUSINESS_GROWTH = "SUM_OF_BUSINESS_GROWTH"  # 营收同比增长率 例如填写[-5,200]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    NET_PROFIT_RATE = "NET_PROFIT_RATE"                # 净利率 例如填写[10,113]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    GROSS_PROFIT_RATE = "GROSS_PROFIT_RATE"            # 毛利率 例如填写[4,65]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    DEBT_ASSET_RATE = "DEBT_ASSET_RATE"                # 资产负债率 例如填写[5,470]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    RETURN_ON_EQUITY_RATE = "RETURN_ON_EQUITY_RATE"    # 净资产收益率 例如填写[20,230]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    ROIC = "ROIC"                                      # 盈利能力属性投入资本回报率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    ROA_TTM = "ROA_TTM"                                # 资产回报率(TTM) 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%。仅适用于年报。）
    EBIT_TTM = "EBIT_TTM"                              # 息税前利润(TTM) 例如填写 [1000000000,1000000000] 值区间（单位：元。仅适用于年报。）
    EBITDA = "EBITDA"                                  # 税息折旧及摊销前利润 例如填写 [1000000000,1000000000] 值区间（单位：元）
    OPERATING_MARGIN_TTM = "OPERATING_MARGIN_TTM"      # 营业利润率(TTM) 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%。仅适用于年报。）
    EBIT_MARGIN = "EBIT_MARGIN"                        # EBIT利润率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    EBITDA_MARGIN = "EBITDA_MARGIN"                    # EBITDA利润率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    FINANCIAL_COST_RATE = "FINANCIAL_COST_RATE"        # 财务成本率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_PROFIT_TTM = "OPERATING_PROFIT_TTM"      # 营业利润(TTM) 例如填写 [1000000000,1000000000] 值区间 （单位：元。仅适用于年报。）
    SHAREHOLDER_NET_PROFIT_TTM = "SHAREHOLDER_NET_PROFIT_TTM"  # 归属于母公司的净利润 例如填写 [1000000000,1000000000] 值区间 （单位：元。仅适用于年报。）
    NET_PROFIT_CASH_COVER_TTM = "NET_PROFIT_CASH_COVER_TTM" # 盈利中的现金收入比例 例如填写 [1.0,60.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%。仅适用于年报。）
    CURRENT_RATIO = "CURRENT_RATIO"                    # 偿债能力属性流动比率 例如填写 [100,250] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    QUICK_RATIO = "QUICK_RATIO"                        # 速动比率 例如填写 [100,250] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    CURRENT_ASSET_RATIO = "CURRENT_ASSET_RATIO"        # 清债能力属性流动资产率 例如填写 [10,100] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    CURRENT_DEBT_RATIO = "CURRENT_DEBT_RATIO"          # 流动负债率 例如填写 [10,100] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    EQUITY_MULTIPLIER = "EQUITY_MULTIPLIER"            # 权益乘数 例如填写 [100,180] 值区间
    PROPERTY_RATIO = "PROPERTY_RATIO"                  # 产权比率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    CASH_AND_CASH_EQUIVALENTS = "CASH_AND_CASH_EQUIVALENTS"  # 现金和现金等价 例如填写 [1000000000,1000000000] 值区间（单位：元）
    TOTAL_ASSET_TURNOVER = "TOTAL_ASSET_TURNOVER"      # 运营能力属性总资产周转率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    FIXED_ASSET_TURNOVER = "FIXED_ASSET_TURNOVER"      # 固定资产周转率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    INVENTORY_TURNOVER = "INVENTORY_TURNOVER"          # 存货周转率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_CASH_FLOW_TTM = "OPERATING_CASH_FLOW_TTM"  # 经营活动现金流(TTM) 例如填写 [1000000000,1000000000] 值区间（单位：元。仅适用于年报。）
    ACCOUNTS_RECEIVABLE = "ACCOUNTS_RECEIVABLE"        # 应收帐款净额 例如填写 [1000000000,1000000000] 值区间 例如填写 [1000000000,1000000000] 值区间 （单位：元）
    EBIT_GROWTH_RATE = "EBIT_GROWTH_RATE"              # 成长能力属性EBIT同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_PROFIT_GROWTH_RATE = "OPERATING_PROFIT_GROWTH_RATE"  # 营业利润同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    TOTAL_ASSETS_GROWTH_RATE = "TOTAL_ASSETS_GROWTH_RATE"  # 总资产同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    PROFIT_TO_SHAREHOLDERS_GROWTH_RATE = "PROFIT_TO_SHAREHOLDERS_GROWTH_RATE"  # 归母净利润同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    PROFIT_BEFORE_TAX_GROWTH_RATE = "PROFIT_BEFORE_TAX_GROWTH_RATE"  # 总利润同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    EPS_GROWTH_RATE = "EPS_GROWTH_RATE"                # EPS同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    ROE_GROWTH_RATE = "ROE_GROWTH_RATE"                # ROE同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    ROIC_GROWTH_RATE = "ROIC_GROWTH_RATE"              # ROIC同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    NOCF_GROWTH_RATE = "NOCF_GROWTH_RATE"              # 经营现金流同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    NOCF_PER_SHARE_GROWTH_RATE = "NOCF_PER_SHARE_GROWTH_RATE"  # 每股经营现金流同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_REVENUE_CASH_COVER = "OPERATING_REVENUE_CASH_COVER"  # 现金流属性经营现金收入比 例如填写 [10,100] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_PROFIT_TO_TOTAL_PROFIT = "OPERATING_PROFIT_TO_TOTAL_PROFIT"  # 营业利润占比 例如填写 [10,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    BASIC_EPS = "BASIC_EPS"                            # 市场表现属性基本每股收益 例如填写 [0.1,10] 值区间 (单位：元)
    DILUTED_EPS = "DILUTED_EPS"                        # 稀释每股收益 例如填写 [0.1,10] 值区间 (单位：元)
    NOCF_PER_SHARE = "NOCF_PER_SHARE"                  # 每股经营现金净流量 例如填写 [0.1,10] 值区间 (单位：元)
    # 以下是技术指标形态过滤所支持的枚举
    pattern_enum_begin = 300
    MA_ALIGNMENT_LONG = "MA_ALIGNMENT_LONG"  # MA多头排列（连续两天MA5>MA10>MA20>MA30>MA60，且当日收盘价大于前一天收盘价）
    MA_ALIGNMENT_SHORT = "MA_ALIGNMENT_SHORT"  # MA空头排列（连续两天MA5 <MA10 <MA20 <MA30 <MA60，且当日收盘价小于前一天收盘价）
    EMA_ALIGNMENT_LONG = "EMA_ALIGNMENT_LONG"  # EMA多头排列（连续两天EMA5>EMA10>EMA20>EMA30>EMA60，且当日收盘价大于前一天收盘价）
    EMA_ALIGNMENT_SHORT = "EMA_ALIGNMENT_SHORT"  # EMA空头排列（连续两天EMA5 <EMA10 <EMA20 <EMA30 <EMA60，且当日收盘价小于前一天收盘价）
    RSI_GOLD_CROSS_LOW = "RSI_GOLD_CROSS_LOW"  # RSI低位金叉（50以下，短线RSI上穿长线RSI（前一日短线RSI小于长线RSI，当日短线RSI大于长线RSI））
    RSI_DEATH_CROSS_HIGH = "RSI_DEATH_CROSS_HIGH"  # RSI高位死叉（50以上，短线RSI下穿长线RSI（前一日短线RSI大于长线RSI，当日短线RSI小于长线RSI））
    RSI_TOP_DIVERGENCE = "RSI_TOP_DIVERGENCE"  # RSI顶背离（相邻的两个K线波峰，后面的波峰对应的CLOSE>前面的波峰对应的CLOSE，后面波峰的RSI12值 <前面波峰的RSI12值）
    RSI_BOTTOM_DIVERGENCE = "RSI_BOTTOM_DIVERGENCE"  # RSI底背离（相邻的两个K线波谷，后面的波谷对应的CLOSE <前面的波谷对应的CLOSE，后面波谷的RSI12值>前面波谷的RSI12值）
    KDJ_GOLD_CROSS_LOW = "KDJ_GOLD_CROSS_LOW"  # KDJ低位金叉（KDJ的值都小于或等于30，且前一日K,J值分别小于D值，当日K,J值分别大于D值）
    KDJ_DEATH_CROSS_HIGH = "KDJ_DEATH_CROSS_HIGH"  # KDJ高位死叉（KDJ的值都大于或等于70，且前一日K,J值分别大于D值，当日K,J值分别小于D值）
    KDJ_TOP_DIVERGENCE = "KDJ_TOP_DIVERGENCE"  # KDJ顶背离（相邻的两个K线波峰，后面的波峰对应的CLOSE>前面的波峰对应的CLOSE，后面波峰的J值 <前面波峰的J值）
    KDJ_BOTTOM_DIVERGENCE = "KDJ_BOTTOM_DIVERGENCE"  # KDJ底背离（相邻的两个K线波谷，后面的波谷对应的CLOSE <前面的波谷对应的CLOSE，后面波谷的J值>前面波谷的J值）
    MACD_GOLD_CROSS_LOW = "MACD_GOLD_CROSS_LOW"  # MACD低位金叉（DIFF上穿DEA（前一日DIFF小于DEA，当日DIFF大于DEA））
    MACD_DEATH_CROSS_HIGH = "MACD_DEATH_CROSS_HIGH"  # MACD高位死叉（DIFF下穿DEA（前一日DIFF大于DEA，当日DIFF小于DEA））
    MACD_TOP_DIVERGENCE = "MACD_TOP_DIVERGENCE"  # MACD顶背离（相邻的两个K线波峰，后面的波峰对应的CLOSE>前面的波峰对应的CLOSE，后面波峰的macd值 <前面波峰的macd值）
    MACD_BOTTOM_DIVERGENCE = "MACD_BOTTOM_DIVERGENCE"  # MACD底背离（相邻的两个K线波谷，后面的波谷对应的CLOSE <前面的波谷对应的CLOSE，后面波谷的macd值>前面波谷的macd值）
    BOLL_BREAK_UPPER = "BOLL_BREAK_UPPER"  # BOLL突破上轨（前一日股价低于上轨值，当日股价大于上轨值）
    BOLL_BREAK_LOWER = "BOLL_BREAK_LOWER"  # BOLL突破下轨（前一日股价高于下轨值，当日股价小于下轨值）
    BOLL_CROSS_MIDDLE_UP = "BOLL_CROSS_MIDDLE_UP"  # BOLL向上破中轨（前一日股价低于中轨值，当日股价大于中轨值）
    BOLL_CROSS_MIDDLE_DOWN = "BOLL_CROSS_MIDDLE_DOWN"  # BOLL向下破中轨（前一日股价大于中轨值，当日股价小于中轨值）

    # 以下是技术指标过滤所支持的枚举
    indicator_enum_begin = 400
    PRICE = "PRICE"  # 最新价格
    MA5 = "MA5"  # 5日简单均线（不建议使用）
    MA10 = "MA10"  # 10日简单均线（不建议使用）
    MA20 = "MA20"  # 20日简单均线（不建议使用）
    MA30 = "MA30"  # 30日简单均线（不建议使用）
    MA60 = "MA60"  # 60日简单均线（不建议使用）
    MA120 = "MA120"  # 120日简单均线（不建议使用）
    MA250 = "MA250"  # 250日简单均线（不建议使用）
    RSI = "RSI"  # RSI 指标参数的默认值为12
    EMA5 = "EMA5"  # 5日指数移动均线（不建议使用）
    EMA10 = "EMA10"  # 10日指数移动均线（不建议使用）
    EMA20 = "EMA20"  # 20日指数移动均线（不建议使用）
    EMA30 = "EMA30"  # 30日指数移动均线（不建议使用）
    EMA60 = "EMA60"  # 60日指数移动均线（不建议使用）
    EMA120 = "EMA120"  # 120日指数移动均线（不建议使用）
    EMA250 = "EMA250"  # 250日指数移动均线（不建议使用）
    VALUE = "VALUE"  # 自定义数值（stock_field1 不支持此字段）
    MA = "MA" # 简单均线
    EMA = "EMA" # 指数移动均线
    KDJ_K = "KDJ_K"  # KDJ 指标的 K 值。指标参数需要根据 KDJ 进行传参。不传则默认为 [9,3,3]
    KDJ_D = "KDJ_D"  # KDJ 指标的 D 值。指标参数需要根据 KDJ 进行传参。不传则默认为 [9,3,3]
    KDJ_J = "KDJ_J"  # KDJ 指标的 J 值。指标参数需要根据 KDJ 进行传参。不传则默认为 [9,3,3]
    MACD_DIFF = "MACD_DIFF"  # MACD 指标的 DIFF 值。指标参数需要根据 MACD 进行传参。不传则默认为 [12,26,9]
    MACD_DEA = "MACD_DEA"  # MACD 指标的 DEA 值。指标参数需要根据 MACD 进行传参。不传则默认为 [12,26,9]
    MACD = "MACD"  # MACD 指标的 MACD 值。指标参数需要根据 MACD 进行传参。不传则默认为 [12,26,9]
    BOLL_UPPER = "BOLL_UPPER"  # BOLL 指标的 UPPER 值。指标参数需要根据 BOLL 进行传参。不传则默认为 [20,2]
    BOLL_MIDDLER = "BOLL_MIDDLER"  # BOLL 指标的 MIDDLER 值。指标参数需要根据 BOLL 进行传参。不传则默认为 [20,2]
    BOLL_LOWER = "BOLL_LOWER"  # BOLL 指标的 LOWER 值。指标参数需要根据 BOLL 进行传参。不传则默认为 [20,2]

    def load_dic(self):
        return {
            # 简单
            self.NONE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_Unknown,
            self.STOCK_CODE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_StockCode,
            self.STOCK_NAME: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_StockName,
            self.CUR_PRICE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_CurPrice,
            self.CUR_PRICE_TO_HIGHEST52_WEEKS_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_CurPriceToHighest52WeeksRatio,
            self.CUR_PRICE_TO_LOWEST52_WEEKS_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_CurPriceToLowest52WeeksRatio,
            self.HIGH_PRICE_TO_HIGHEST52_WEEKS_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_HighPriceToHighest52WeeksRatio,
            self.LOW_PRICE_TO_LOWEST52_WEEKS_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_LowPriceToLowest52WeeksRatio,
            self.VOLUME_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_VolumeRatio,
            self.BID_ASK_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_BidAskRatio,
            self.LOT_PRICE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_LotPrice,
            self.MARKET_VAL: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_MarketVal,
            self.PE_ANNUAL: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PeAnnual,
            self.PE_TTM: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PeTTM,
            self.PB_RATE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PbRate,
            self.CHANGE_RATE_5MIN: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_ChangeRate5min,
            self.CHANGE_RATE_BEGIN_YEAR: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_ChangeRateBeginYear,
            self.PS_TTM: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PSTTM,
            self.PCF_TTM: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PCFTTM,
            self.TOTAL_SHARE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_TotalShare,
            self.FLOAT_SHARE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_FloatShare,
            self.FLOAT_MARKET_VAL: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_FloatMarketVal,

            # 累积
            self.CHANGE_RATE: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_ChangeRate,
            self.AMPLITUDE: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_Amplitude,
            self.VOLUME: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_Volume,
            self.TURNOVER: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_Turnover,
            self.TURNOVER_RATE: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_TurnoverRate,

            # 财务
            self.NET_PROFIT: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NetProfit,
            self.NET_PROFIX_GROWTH: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NetProfitGrowth,
            self.SUM_OF_BUSINESS: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_SumOfBusiness,
            self.SUM_OF_BUSINESS_GROWTH: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_SumOfBusinessGrowth,
            self.NET_PROFIT_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NetProfitRate,
            self.GROSS_PROFIT_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_GrossProfitRate,
            self.DEBT_ASSET_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_DebtAssetsRate,
            self.RETURN_ON_EQUITY_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ReturnOnEquityRate,
            self.ROIC: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ROIC,
            self.ROA_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ROATTM,
            self.EBIT_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITTTM,
            self.EBITDA: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITDA,
            self.OPERATING_MARGIN_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingMarginTTM,
            self.EBIT_MARGIN: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITMargin,
            self.EBITDA_MARGIN: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITDAMargin,
            self.FINANCIAL_COST_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_FinancialCostRate,
            self.OPERATING_PROFIT_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingProfitTTM,
            self.SHAREHOLDER_NET_PROFIT_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ShareholderNetProfitTTM,
            self.NET_PROFIT_CASH_COVER_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NetProfitCashCoverTTM,
            self.CURRENT_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_CurrentRatio,
            self.QUICK_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_QuickRatio,
            self.CURRENT_ASSET_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_CurrentAssetRatio,
            self.CURRENT_DEBT_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_CurrentDebtRatio,
            self.EQUITY_MULTIPLIER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EquityMultiplier,
            self.PROPERTY_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_PropertyRatio,
            self.CASH_AND_CASH_EQUIVALENTS: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_CashAndCashEquivalents,
            self.TOTAL_ASSET_TURNOVER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_TotalAssetTurnover,
            self.FIXED_ASSET_TURNOVER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_FixedAssetTurnover,
            self.INVENTORY_TURNOVER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_InventoryTurnover,
            self.OPERATING_CASH_FLOW_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingCashFlowTTM,
            self.ACCOUNTS_RECEIVABLE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_AccountsReceivable,
            self.EBIT_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITGrowthRate,
            self.OPERATING_PROFIT_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingProfitGrowthRate,
            self.TOTAL_ASSETS_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_TotalAssetsGrowthRate,
            self.PROFIT_TO_SHAREHOLDERS_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ProfitToShareholdersGrowthRate,
            self.PROFIT_BEFORE_TAX_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ProfitBeforeTaxGrowthRate,
            self.EPS_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EPSGrowthRate,
            self.ROE_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ROEGrowthRate,
            self.ROIC_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ROICGrowthRate,
            self.NOCF_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NOCFGrowthRate,
            self.NOCF_PER_SHARE_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NOCFPerShareGrowthRate,
            self.OPERATING_REVENUE_CASH_COVER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingRevenueCashCover,
            self.OPERATING_PROFIT_TO_TOTAL_PROFIT: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingProfitToTotalProfit,
            self.BASIC_EPS: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_BasicEPS,
            self.DILUTED_EPS: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_DilutedEPS,
            self.NOCF_PER_SHARE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NOCFPerShare,

            # 指标形态
            self.MA_ALIGNMENT_LONG: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_MAAlignmentLong,
            self.MA_ALIGNMENT_SHORT: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_MAAlignmentShort,
            self.EMA_ALIGNMENT_LONG: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_EMAAlignmentLong,
            self.EMA_ALIGNMENT_SHORT: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_EMAAlignmentShort,
            self.RSI_GOLD_CROSS_LOW: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_RSIGoldCrossLow,
            self.RSI_DEATH_CROSS_HIGH: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_RSIDeathCrossHigh,
            self.RSI_TOP_DIVERGENCE: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_RSITopDivergence,
            self.RSI_BOTTOM_DIVERGENCE: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_RSIBottomDivergence,
            self.KDJ_GOLD_CROSS_LOW: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_KDJGoldCrossLow,
            self.KDJ_DEATH_CROSS_HIGH: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_KDJDeathCrossHigh,
            self.KDJ_TOP_DIVERGENCE: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_KDJTopDivergence,
            self.KDJ_BOTTOM_DIVERGENCE: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_KDJBottomDivergence,
            self.MACD_GOLD_CROSS_LOW: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_MACDGoldCrossLow,
            self.MACD_DEATH_CROSS_HIGH: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_MACDDeathCrossHigh,
            self.MACD_TOP_DIVERGENCE: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_MACDTopDivergence,
            self.MACD_BOTTOM_DIVERGENCE: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_MACDBottomDivergence,
            self.BOLL_BREAK_UPPER: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_BOLLBreakUpper,
            self.BOLL_BREAK_LOWER: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_BOLLLower,
            self.BOLL_CROSS_MIDDLE_UP: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_BOLLCrossMiddleUp,
            self.BOLL_CROSS_MIDDLE_DOWN: self.pattern_enum_begin + Qot_StockFilter_pb2.PatternField_BOLLCrossMiddleDown,

            # 指标
            self.PRICE: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_Price,
            self.MA5: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MA5,
            self.MA10: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MA10,
            self.MA20: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MA20,
            self.MA30: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MA30,
            self.MA60: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MA60,
            self.MA120: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MA120,
            self.MA250: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MA250,
            self.RSI: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_RSI,
            self.EMA5: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_EMA5,
            self.EMA10: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_EMA10,
            self.EMA20: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_EMA20,
            self.EMA30: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_EMA30,
            self.EMA60: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_EMA60,
            self.EMA120: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_EMA120,
            self.EMA250: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_EMA250,
            self.VALUE: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_Value,
            self.MA: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MA,
            self.EMA: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_EMA,
            self.KDJ_K: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_KDJ_K,
            self.KDJ_D: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_KDJ_D,
            self.KDJ_J: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_KDJ_J,
            self.MACD_DIFF: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MACD_DIFF,
            self.MACD_DEA: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MACD_DEA,
            self.MACD: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_MACD,
            self.BOLL_UPPER: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_BOLL_UPPER,
            self.BOLL_MIDDLER: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_BOLL_MIDDLER,
            self.BOLL_LOWER: self.indicator_enum_begin + Qot_StockFilter_pb2.CustomIndicatorField_BOLL_LOWER,
        }


#财务指标的周期
class FinancialQuarter(FtEnum):
    NONE = "N/A"
    ANNUAL = "ANNUAL"                            # 年报
    FIRST_QUARTER = "FIRST_QUARTER"              # Q1一季报
    INTERIM = "INTERIM"                          # Q6中期报
    THIRD_QUARTER = "THIRD_QUARTER"              # Q9三季报
    MOST_RECENT_QUARTER = "MOST_RECENT_QUARTER"  # 最近季报
    
    def load_dic(self):
        return {
            self.NONE: Qot_StockFilter_pb2.FinancialQuarter_Unknown,
            self.ANNUAL: Qot_StockFilter_pb2.FinancialQuarter_Annual,
            self.FIRST_QUARTER: Qot_StockFilter_pb2.FinancialQuarter_FirstQuarter,
            self.INTERIM: Qot_StockFilter_pb2.FinancialQuarter_Interim,
            self.THIRD_QUARTER: Qot_StockFilter_pb2.FinancialQuarter_ThirdQuarter,
            self.MOST_RECENT_QUARTER: Qot_StockFilter_pb2.FinancialQuarter_MostRecentQuarter,
        }

# 相对位置比较
class RelativePosition(FtEnum):
    NONE = "N/A"  # 未知
    MORE = "MORE"  # 大于，first位于second的上方
    LESS = "LESS"  # 小于，first位于second的下方
    CROSS_UP = "CROSS_UP"  # 升穿，first从下往上穿second
    CROSS_DOWN = "CROSS_DOWN"  # 跌穿，first从上往下穿second

    def load_dic(self):
        return {
            self.NONE: Qot_StockFilter_pb2.RelativePosition_Unknown,
            self.MORE: Qot_StockFilter_pb2.RelativePosition_More,
            self.LESS: Qot_StockFilter_pb2.RelativePosition_Less,
            self.CROSS_UP: Qot_StockFilter_pb2.RelativePosition_CrossUp,
            self.CROSS_DOWN: Qot_StockFilter_pb2.RelativePosition_CrossDown
        }

#
class CodeChangeType(FtEnum):
    NONE = "N/A"
    GEM_TO_MAIN = "GEM_TO_MAIN"                        # 创业板转主板
    UNPAID = "UNPAID"                                  # 买卖未缴款供股权
    CHANGE_LOT = "CHANGE_LOT"                          # 更改买卖单位
    SPLIT = "SPLIT"                                    # 拆股
    JOINT = "JOINT"                                    # 合股
    JOINT_SPLIT = "JOINT_SPLIT"                        # 股份先并后拆
    SPLIT_JOINT = "SPLIT_JOINT"                        # 股份先拆后并
    OTHER = "OTHER"                                    # 其他

    def load_dic(self):
        return {
            self.NONE: Qot_GetCodeChange_pb2.CodeChangeType_Unkown,
            self.GEM_TO_MAIN: Qot_GetCodeChange_pb2.CodeChangeType_GemToMain,
            self.UNPAID: Qot_GetCodeChange_pb2.CodeChangeType_Unpaid,
            self.CHANGE_LOT: Qot_GetCodeChange_pb2.CodeChangeType_ChangeLot,
            self.SPLIT: Qot_GetCodeChange_pb2.CodeChangeType_Split,
            self.JOINT: Qot_GetCodeChange_pb2.CodeChangeType_Joint,
            self.JOINT_SPLIT: Qot_GetCodeChange_pb2.CodeChangeType_JointSplit,
            self.SPLIT_JOINT: Qot_GetCodeChange_pb2.CodeChangeType_SplitJoint,
            self.OTHER: Qot_GetCodeChange_pb2.CodeChangeType_Other
        }

#
class TimeFilterType(FtEnum):
    NONE = "N/A"                                       # 未知
    PUBLIC = "PUBLIC"                                  # 根据公布时间过滤
    EFFECTIVE = "EFFECTIVE"                            # 根据生效时间过滤
    END = "END"                                        # 根据结束时间过滤

    def load_dic(self):
        return {
            self.NONE: Qot_GetCodeChange_pb2.TimeFilterType_Unknow,
            self.PUBLIC: Qot_GetCodeChange_pb2.TimeFilterType_Public,
            self.EFFECTIVE: Qot_GetCodeChange_pb2.TimeFilterType_Effective,
            self.END: Qot_GetCodeChange_pb2.TimeFilterType_End
        }


class TimeFilter(object):
    type = 0  # 时间筛选类型
    begin_time = ''  # 时间筛选开始点
    end_time = ''  # 时间筛选结束点

    def __init__(self, type, begin_time, end_time):
        self.type = type
        self.begin_time = begin_time
        self.end_time = end_time

#
class SecurityStatus(FtEnum):
    NONE = "N/A"                                                                 #未知
    NORMAL = "NORMAL"                                                            #正常状态
    LISTING = "LISTING"                                                          #待上市
    PURCHASING = "PURCHASING"                                                    #申购中
    SUBSCRIBING = "SUBSCRIBING"                                                  #认购中
    BEFORE_DARK_TRADE_OPEING = "BEFORE_DARK_TRADE_OPEING"                        #暗盘开盘前
    DARK_TRADING = "DARK_TRADING"                                                #暗盘交易中
    DARK_TRAD_END = "DARK_TRAD_END"                                              #暗盘已收盘
    TO_BE_OPEN = "TO_BE_OPEN"                                                    #待开盘
    SUSPENDED = "SUSPENDED"                                                      #停牌
    CALLED = "CALLED"                                                            #已收回
    EXPIRED_LAST_TRADING_DATE = "EXPIRED_LAST_TRADING_DATE"                      #已过最后交易日
    EXPIRED = "EXPIRED"                                                          #已过期
    DELISTED = "DELISTED"                                                        #已退市
    CHANGE_TO_TEMPORARY_CODE = "CHANGE_TO_TEMPORARY_CODE"                        #公司行动中，交易关闭，转至临时代码交易
    TEMPORARY_CODE_TRADE_END = "TEMPORARY_CODE_TRADE_END"                        #临时买卖结束，交易关闭
    CHANGED_PLATE_TRADE_END = "CHANGED_PLATE_TRADE_END"                          #已转板，旧代码交易关闭
    CHANGED_CODE_TRAD_END = "CHANGED_CODE_TRAD_END"                              #已换代码，旧代码交易关闭
    RECOVERABLE_CIRCUIT_BREAKER = "RECOVERABLE_CIRCUIT_BREAKER"                  #可恢复性熔断
    UNRECOVERABLE_CIRCUIT_BREAKER = "UNRECOVERABLE_CIRCUIT_BREAKER"              #不可恢复性熔断
    AFTER_COMBINATION = "AFTER_COMBINATION"                                      #盘后撮合
    AFTER_TRANSACTION = "AFTER_TRANSACTION"                                      #盘后交易

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.SecurityStatus_Unknown,
            self.NORMAL: Qot_Common_pb2.SecurityStatus_Normal,
            self.LISTING: Qot_Common_pb2.SecurityStatus_Listing,
            self.PURCHASING: Qot_Common_pb2.SecurityStatus_Purchasing,
            self.SUBSCRIBING: Qot_Common_pb2.SecurityStatus_Subscribing,
            self.BEFORE_DARK_TRADE_OPEING: Qot_Common_pb2.SecurityStatus_BeforeDrakTradeOpening,
            self.DARK_TRADING: Qot_Common_pb2.SecurityStatus_DrakTrading,
            self.DARK_TRAD_END: Qot_Common_pb2.SecurityStatus_DrakTradeEnd,
            self.TO_BE_OPEN: Qot_Common_pb2.SecurityStatus_ToBeOpen,
            self.SUSPENDED: Qot_Common_pb2.SecurityStatus_Suspended,
            self.CALLED: Qot_Common_pb2.SecurityStatus_Called,
            self.EXPIRED_LAST_TRADING_DATE: Qot_Common_pb2.SecurityStatus_ExpiredLastTradingDate,
            self.EXPIRED: Qot_Common_pb2.SecurityStatus_Expired,
            self.DELISTED: Qot_Common_pb2.SecurityStatus_Delisted,
            self.CHANGE_TO_TEMPORARY_CODE: Qot_Common_pb2.SecurityStatus_ChangeToTemporaryCode,
            self.TEMPORARY_CODE_TRADE_END: Qot_Common_pb2.SecurityStatus_TemporaryCodeTradeEnd,
            self.CHANGED_PLATE_TRADE_END: Qot_Common_pb2.SecurityStatus_ChangedPlateTradeEnd,
            self.CHANGED_CODE_TRAD_END: Qot_Common_pb2.SecurityStatus_ChangedCodeTradeEnd,
            self.RECOVERABLE_CIRCUIT_BREAKER: Qot_Common_pb2.SecurityStatus_RecoverableCircuitBreaker,
            self.UNRECOVERABLE_CIRCUIT_BREAKER: Qot_Common_pb2.SecurityStatus_UnRecoverableCircuitBreaker,
            self.AFTER_COMBINATION: Qot_Common_pb2.SecurityStatus_AfterCombination,
            self.AFTER_TRANSACTION: Qot_Common_pb2.SecurityStatus_AfterTransation
        }

#
class IndexOptionType(FtEnum):
    NONE = "N/A"                                                                 #未知
    NORMAL = "NORMAL"                                                            #正常
    SMALL = "SMALL"                                                              #小型

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.IndexOptionType_Unknown,
            self.NORMAL: Qot_Common_pb2.IndexOptionType_Normal,
            self.SMALL: Qot_Common_pb2.IndexOptionType_Small
        }


class OptionAreaType(FtEnum):
    NONE = "N/A"                                                                 #未知
    AMERICAN = "AMERICAN"                                                        #美式
    EUROPEAN = "EUROPEAN"                                                        #欧式
    BERMUDA = "BERMUDA"                                                          #百慕大

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.OptionAreaType_Unknown,
            self.AMERICAN: Qot_Common_pb2.OptionAreaType_American,
            self.EUROPEAN: Qot_Common_pb2.OptionAreaType_European,
            self.BERMUDA: Qot_Common_pb2.OptionAreaType_Bermuda
        }


class Currency(FtEnum):
    NONE = 'N/A' # 未知
    HKD = 'HKD'  # 港币
    USD = 'USD'  # 美元
    CNH = 'CNH'  # 离岸人民币
    JPY = 'JPY'  # 日元
    SGD = 'SGD'  # 新元
    AUD = 'AUD'  # 澳元
    CAD = 'CAD'  # 加元
    MYR = 'MYR'  # 马来西亚令吉
    NZD = 'NZD'  # 新西兰元

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.Currency_Unknown,
            self.HKD: Trd_Common_pb2.Currency_HKD,
            self.USD: Trd_Common_pb2.Currency_USD,
            self.CNH: Trd_Common_pb2.Currency_CNH,
            self.JPY: Trd_Common_pb2.Currency_JPY,
            self.SGD: Trd_Common_pb2.Currency_SGD,
            self.AUD: Trd_Common_pb2.Currency_AUD,
            self.CAD: Trd_Common_pb2.Currency_CAD,
            self.MYR: Trd_Common_pb2.Currency_MYR,
            self.NZD: Trd_Common_pb2.Currency_NZD,
        }

class CltRiskLevel(FtEnum):
    NONE = 'N/A'    # 未知
    SAFE = 'SAFE'   # 安全
    WARNING = 'WARNING'     # 预警
    DANGER = 'DANGER'       # 危险
    ABSOLUTE_SAFE = 'ABSOLUTE_SAFE'     # 绝对安全
    OPT_DANGER = 'OPT_DANGER'           # 危险，期权相关

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.CltRiskLevel_Unknown,
            self.SAFE: Trd_Common_pb2.CltRiskLevel_Safe,
            self.WARNING: Trd_Common_pb2.CltRiskLevel_Warning,
            self.DANGER: Trd_Common_pb2.CltRiskLevel_Danger,
            self.ABSOLUTE_SAFE: Trd_Common_pb2.CltRiskLevel_AbsoluteSafe,
            self.OPT_DANGER: Trd_Common_pb2.CltRiskLevel_OptDanger
        }


class CltRiskStatus(FtEnum):
    NONE = 'N/A'
    LEVEL1 = 'LEVEL1'
    LEVEL2: str = 'LEVEL2'
    LEVEL3 = 'LEVEL3'
    LEVEL4 = 'LEVEL4'
    LEVEL5 = 'LEVEL5'
    LEVEL6 = 'LEVEL6'
    LEVEL7 = 'LEVEL7'
    LEVEL8 = 'LEVEL8'
    LEVEL9 = 'LEVEL9'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.CltRiskStatus_Unknown,
            self.LEVEL1: Trd_Common_pb2.CltRiskStatus_Level1,
            self.LEVEL2: Trd_Common_pb2.CltRiskStatus_Level2,
            self.LEVEL3: Trd_Common_pb2.CltRiskStatus_Level3,
            self.LEVEL4: Trd_Common_pb2.CltRiskStatus_Level4,
            self.LEVEL5: Trd_Common_pb2.CltRiskStatus_Level5,
            self.LEVEL6: Trd_Common_pb2.CltRiskStatus_Level6,
            self.LEVEL7: Trd_Common_pb2.CltRiskStatus_Level7,
            self.LEVEL8: Trd_Common_pb2.CltRiskStatus_Level8,
            self.LEVEL9: Trd_Common_pb2.CltRiskStatus_Level9,
        }

class TradeDateMarket(FtEnum):
    NONE = 'N/A'  # 未知
    HK = 'HK'  # 港股市场
    US = 'US'  # 美股市场
    CN = 'CN'  # A股市场
    NT = 'NT'  # 深（沪）股通
    ST = 'ST'  # 港股通（深、沪）
    JP_FUTURE = 'JP_FUTURE'  # 日本期货
    SG_FUTURE = 'SG_FUTURE'  # 新加坡期货
    SG = 'SG'  # 新加坡
    MY = 'MY'  # 马来西亚
    JP = 'JP'  # 日本（正股/ETF）

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.TradeDateMarket_Unknown,
            self.HK: Qot_Common_pb2.TradeDateMarket_HK,
            self.US: Qot_Common_pb2.TradeDateMarket_US,
            self.CN: Qot_Common_pb2.TradeDateMarket_CN,
            self.NT: Qot_Common_pb2.TradeDateMarket_NT,
            self.ST: Qot_Common_pb2.TradeDateMarket_ST,
            self.JP_FUTURE: Qot_Common_pb2.TradeDateMarket_JP_Future,
            self.SG_FUTURE: Qot_Common_pb2.TradeDateMarket_SG_Future,
            self.SG: Qot_Common_pb2.TradeDateMarket_SG,
            self.MY: Qot_Common_pb2.TradeDateMarket_MY,
            self.JP: Qot_Common_pb2.TradeDateMarket_JP,
        }

class SetPriceReminderOp(FtEnum):
    NONE = "N/A"                                       # 未知
    ADD = "ADD"                                        # 新增
    DEL = "DEL"                                        # 删除
    ENABLE = "ENABLE"                                  # 启用
    DISABLE = "DISABLE"                                # 禁用
    MODIFY = "MODIFY"                                  # 修改
    DEL_ALL = "DEL_ALL"                                # 删除某支股票下所有到价提醒

    def load_dic(self):
        return {
            self.NONE: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Unknown,
            self.ADD: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Add,
            self.DEL: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Del,
            self.ENABLE: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Enable,
            self.DISABLE: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Disable,
            self.MODIFY: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Modify,
            self.DEL_ALL: Qot_SetPriceReminder_pb2.SetPriceReminderOp_DelAll,
        }

class PriceReminderFreq(FtEnum):
    NONE = "N/A"                                       # 未知
    ALWAYS = "ALWAYS"                                  # 持续提醒
    ONCE_A_DAY = "ONCE_A_DAY"                          # 每日一次
    ONCE = "ONCE"                                      # 仅提醒一次

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PriceReminderFreq_Unknown,
            self.ALWAYS: Qot_Common_pb2.PriceReminderFreq_Always,
            self.ONCE_A_DAY: Qot_Common_pb2.PriceReminderFreq_OnceADay,
            self.ONCE: Qot_Common_pb2.PriceReminderFreq_OnlyOnce,
        }

class PriceReminderType(FtEnum):
    NONE = "N/A"
    PRICE_UP = "PRICE_UP"  # 当前价涨到
    PRICE_DOWN = "PRICE_DOWN"  # 当前价跌到
    CHANGE_RATE_UP = "CHANGE_RATE_UP"  # 当前涨幅
    CHANGE_RATE_DOWN = "CHANGE_RATE_DOWN"  # 当前跌幅
    FIVE_MIN_CHANGE_RATE_UP = "FIVE_MIN_CHANGE_RATE_UP"  # 5分钟涨幅
    FIVE_MIN_CHANGE_RATE_DOWN = "FIVE_MIN_CHANGE_RATE_DOWN"  # 5分钟跌幅
    VOLUME_UP = "VOLUME_UP"  # 成交量大于
    TURNOVER_UP = "TURNOVER_UP"  # 成交额大于
    TURNOVER_RATE_UP = "TURNOVER_RATE_UP"  # 换手率大于
    BID_PRICE_UP = "BID_PRICE_UP"  # 买一价高于
    ASK_PRICE_DOWN = "ASK_PRICE_DOWN"  # 卖一价低于
    BID_VOL_UP = "BID_VOL_UP"  # 买一量高于
    ASK_VOL_UP = "ASK_VOL_UP"  # 卖一量高于
    THREE_MIN_CHANGE_RATE_UP = "THREE_MIN_CHANGE_RATE_UP"  # 3分钟涨幅
    THREE_MIN_CHANGE_RATE_DOWN = "THREE_MIN_CHANGE_RATE_DOWN"  # 3分钟跌幅

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PriceReminderFreq_Unknown,
            self.PRICE_UP: Qot_Common_pb2.PriceReminderType_PriceUp,
            self.PRICE_DOWN: Qot_Common_pb2.PriceReminderType_PriceDown,
            self.CHANGE_RATE_UP: Qot_Common_pb2.PriceReminderType_ChangeRateUp,
            self.CHANGE_RATE_DOWN: Qot_Common_pb2.PriceReminderType_ChangeRateDown,
            self.FIVE_MIN_CHANGE_RATE_UP: Qot_Common_pb2.PriceReminderType_5MinChangeRateUp,
            self.FIVE_MIN_CHANGE_RATE_DOWN: Qot_Common_pb2.PriceReminderType_5MinChangeRateDown,
            self.VOLUME_UP: Qot_Common_pb2.PriceReminderType_VolumeUp,
            self.TURNOVER_UP: Qot_Common_pb2.PriceReminderType_TurnoverUp,
            self.TURNOVER_RATE_UP: Qot_Common_pb2.PriceReminderType_TurnoverRateUp,
            self.BID_PRICE_UP: Qot_Common_pb2.PriceReminderType_BidPriceUp,
            self.ASK_PRICE_DOWN: Qot_Common_pb2.PriceReminderType_AskPriceDown,
            self.BID_VOL_UP: Qot_Common_pb2.PriceReminderType_BidVolUp,
            self.ASK_VOL_UP: Qot_Common_pb2.PriceReminderType_AskVolUp,
            self.THREE_MIN_CHANGE_RATE_UP: Qot_Common_pb2.PriceReminderType_3MinChangeRateUp,
            self.THREE_MIN_CHANGE_RATE_DOWN: Qot_Common_pb2.PriceReminderType_3MinChangeRateDown,
        }

# 所属交易所
class ExchType(FtEnum):
    NONE = "N/A" # 未知
    HK_MAINBOARD = "HK_MAINBOARD"  # 港交所·主板
    HK_GEMBOARD = "HK_GEMBOARD"  # 港交所·创业板
    HK_HKEX = "HK_HKEX"  # 港交所
    US_NYSE = "US_NYSE"  # 纽交所
    US_NASDAQ = "US_NASDAQ"  # 纳斯达克
    US_PINK = "US_PINK"  # OTC 市场
    US_AMEX = "US_AMEX"  # 美交所
    US_OPTION = "US_OPTION"  # 美国 [info]仅美股期权适用
    US_NYMEX = "US_NYMEX"  # NYMEX
    US_COMEX = "US_COMEX"  # COMEX
    US_CBOT = "US_CBOT"  # CBOT
    US_CME = "US_CME"  # CME
    US_CBOE = "US_CBOE"  # CBOE
    CN_SH = "CN_SH"  # 上交所
    CN_SZ = "CN_SZ"  # 深交所
    CN_STIB = "CN_STIB"  # 科创板
    SG_SGX = "SG_SGX"  # 新交所
    JP_OSE = "JP_OSE"  # 大阪交易所
    JP_TSE = "JP_TSE"  # 东京证券交易所
    JP_NIKKEI = "JP_NIKKEI"  # 日经指数
    CC_CRYPTO = "CC_CRYPTO" #加密货币交易所
    MY_MYX = "MY_MYX" # 马来西亚

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.ExchType_Unknown,
            self.HK_MAINBOARD: Qot_Common_pb2.ExchType_HK_MainBoard,
            self.HK_GEMBOARD: Qot_Common_pb2.ExchType_HK_GEMBoard,
            self.HK_HKEX: Qot_Common_pb2.ExchType_HK_HKEX,
            self.US_NYSE: Qot_Common_pb2.ExchType_US_NYSE,
            self.US_NASDAQ: Qot_Common_pb2.ExchType_US_Nasdaq,
            self.US_PINK: Qot_Common_pb2.ExchType_US_Pink,
            self.US_AMEX: Qot_Common_pb2.ExchType_US_AMEX,
            self.US_OPTION: Qot_Common_pb2.ExchType_US_Option,
            self.US_NYMEX: Qot_Common_pb2.ExchType_US_NYMEX,
            self.US_COMEX: Qot_Common_pb2.ExchType_US_COMEX,
            self.US_CBOT: Qot_Common_pb2.ExchType_US_CBOT,
            self.US_CME: Qot_Common_pb2.ExchType_US_CME,
            self.US_CBOE: Qot_Common_pb2.ExchType_US_CBOE,
            self.CN_SH: Qot_Common_pb2.ExchType_CN_SH,
            self.CN_SZ: Qot_Common_pb2.ExchType_CN_SZ,
            self.CN_STIB: Qot_Common_pb2.ExchType_CN_STIB,
            self.SG_SGX: Qot_Common_pb2.ExchType_SG_SGX,
            self.JP_OSE: Qot_Common_pb2.ExchType_JP_OSE,
            self.JP_TSE: Qot_Common_pb2.ExchType_JP_TSE,
            self.JP_NIKKEI: Qot_Common_pb2.ExchType_JP_Nikkei,
            self.CC_CRYPTO: Qot_Common_pb2.ExchType_CC_CRYPTO,
            self.MY_MYX: Qot_Common_pb2.ExchType_MY_MYX,

        }

class PriceReminderMarketStatus(FtEnum):
    NONE = "N/A"
    OPEN = "OPEN"
    US_PRE = "US_PRE"
    US_AFTER = "US_AFTER"
    US_OVERNIGHT = "US_OVERNIGHT"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PriceReminderMarketStatus_Unknow,
            self.OPEN: Qot_Common_pb2.PriceReminderMarketStatus_Open,
            self.US_PRE: Qot_Common_pb2.PriceReminderMarketStatus_USPre,
            self.US_AFTER: Qot_Common_pb2.PriceReminderMarketStatus_USAfter,
            self.US_OVERNIGHT: Qot_Common_pb2.PriceReminderMarketStatus_USOverNight
        }


# 自选股的类型
class UserSecurityGroupType(FtEnum):
    NONE = "N/A"                                       # 未知
    CUSTOM = "CUSTOM"                                  # 自定义分组
    SYSTEM = "SYSTEM"                                  # 系统分组
    ALL = "ALL"                                        # 全部分组

    def load_dic(self):
        return {
            self.NONE: Qot_GetUserSecurityGroup_pb2.GroupType_Unknown,
            self.CUSTOM: Qot_GetUserSecurityGroup_pb2.GroupType_Custom,
            self.SYSTEM: Qot_GetUserSecurityGroup_pb2.GroupType_System,
            self.ALL: Qot_GetUserSecurityGroup_pb2.GroupType_All
        }

# 资产类别
class AssetClass(FtEnum):
    NONE = "N/A"  # 未知
    STOCK = "STOCK"  # 股票
    BOND = "BOND" # 债券
    COMMODITY = "COMMODITY"  # 商品
    CURRENCY_MARKET = "CURRENCY_MARKET"  # 货币市场
    FUTURE = "FUTURE"  # 期货
    SWAP = "SWAP"  # 掉期

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.AssetClass_Unknow,
            self.STOCK: Qot_Common_pb2.AssetClass_Stock,
            self.BOND: Qot_Common_pb2.AssetClass_Bond,
            self.COMMODITY: Qot_Common_pb2.AssetClass_Commodity,
            self.CURRENCY_MARKET: Qot_Common_pb2.AssetClass_CurrencyMarket,
            self.FUTURE: Qot_Common_pb2.AssetClass_Future,
            self.SWAP: Qot_Common_pb2.AssetClass_Swap,
        }


# 订单有效期
class TimeInForce(FtEnum):
    DAY = 'DAY'   # 当日有效
    GTC = 'GTC'   # 撤单前有效
    IOC = 'IOC'   # 立即执行，否则取消
    GTD = 'GTD'   # 指定到期日前有效

    def load_dic(self):
        return {
            self.DAY: Trd_Common_pb2.TimeInForce_DAY,
            self.GTC: Trd_Common_pb2.TimeInForce_GTC,
            self.IOC: Trd_Common_pb2.TimeInForce_IOC,
            self.GTD: Trd_Common_pb2.TimeInForce_GTD,
        }


# 时段
class Session(FtEnum):
    NONE = 'N/A'   # 未知
    RTH = 'RTH'   # 盘中
    ETH = 'ETH'  # 盘中+盘前盘后
    ALL = 'ALL'  # 全时段
    OVERNIGHT = 'OVERNIGHT'  # 仅夜盘

    def load_dic(self):
        return {
            self.NONE: Common_pb2.Session_NONE,
            self.RTH: Common_pb2.Session_RTH,
            self.ETH: Common_pb2.Session_ETH,
            self.ALL: Common_pb2.Session_ALL,
            self.OVERNIGHT: Common_pb2.Session_OVERNIGHT,
        }


# 券商
class SecurityFirm(FtEnum):
    NONE = 'N/A'
    FUTUSECURITIES = 'FUTUSECURITIES'
    FUTUINC = 'FUTUINC'
    FUTUSG = 'FUTUSG'
    FUTUAU = 'FUTUAU'
    FUTUCA = 'FUTUCA'
    FUTUMY = 'FUTUMY'
    FUTUJP = 'FUTUJP'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.SecurityFirm_Unknown,
            self.FUTUSECURITIES: Trd_Common_pb2.SecurityFirm_FutuSecurities,
            self.FUTUINC: Trd_Common_pb2.SecurityFirm_FutuInc,
            self.FUTUSG: Trd_Common_pb2.SecurityFirm_FutuSG,
            self.FUTUAU: Trd_Common_pb2.SecurityFirm_FutuAU,
            self.FUTUCA: Trd_Common_pb2.SecurityFirm_FutuCA,
            self.FUTUMY: Trd_Common_pb2.SecurityFirm_FutuMY,
            self.FUTUJP: Trd_Common_pb2.SecurityFirm_FutuJP,
        }


def get_string_by_securityFirm(security_enum):
    mapping = {
        SecurityFirm.FUTUSECURITIES: "FUTU HK",
        SecurityFirm.FUTUINC: "Moomoo US",
        SecurityFirm.FUTUSG: "Moomoo SG",
        SecurityFirm.FUTUAU: "Moomoo AU",
        SecurityFirm.FUTUCA: "Moomoo CA",
        SecurityFirm.FUTUMY: "Moomoo MY",
        SecurityFirm.FUTUJP: "Moomoo JP",
    }
    return mapping.get(security_enum, "Unknown security")

# 模拟交易账号类型
class SimAccType(FtEnum):
    NONE = 'N/A'
    STOCK = 'STOCK'
    OPTION = 'OPTION'
    FUTURES = 'FUTURES'
    STOCK_AND_OPTION = 'STOCK_AND_OPTION'
    COMPETITION = 'COMPETITION'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.SimAccType_Unknown,
            self.STOCK: Trd_Common_pb2.SimAccType_Stock,
            self.OPTION: Trd_Common_pb2.SimAccType_Option,
            self.FUTURES: Trd_Common_pb2.SimAccType_Futures,
            self.STOCK_AND_OPTION: Trd_Common_pb2.SimAccType_StockAndOption,
            self.COMPETITION: Trd_Common_pb2.SimAccType_Competition,
        }

# 期权交割周期
class ExpirationCycle(FtEnum):
    NONE = 'N/A'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    ENDOFMONTH = 'END_OF_MONTH'
    QUARTERLY = 'QUARTERLY'
    WEEKMON = 'WEEKMON'
    WEEKTUE = 'WEEKTUE'
    WEEKWED = 'WEEKWED'
    WEEKTHU = 'WEEKTHU'
    WEEKFRI = 'WEEKFRI'

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.ExpirationCycle_Unknown,
            self.WEEK: Qot_Common_pb2.ExpirationCycle_Week,
            self.MONTH: Qot_Common_pb2.ExpirationCycle_Month,
            self.ENDOFMONTH: Qot_Common_pb2.ExpirationCycle_MonthEnd,
            self.QUARTERLY: Qot_Common_pb2.ExpirationCycle_Quarter,
            self.WEEKMON: Qot_Common_pb2.ExpirationCycle_WeekMon,
            self.WEEKTUE: Qot_Common_pb2.ExpirationCycle_WeekTue,
            self.WEEKWED: Qot_Common_pb2.ExpirationCycle_WeekWed,
            self.WEEKTHU: Qot_Common_pb2.ExpirationCycle_WeekThu,
            self.WEEKFRI: Qot_Common_pb2.ExpirationCycle_WeekFri,
        }


# 期权标准类型
class OptionStandardType(FtEnum):
    NONE = 'N/A'
    STANDARD = 'STANDARD'
    NON_STANDARD = 'NON_STANDARD'

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.OptionStandardType_Unknown,
            self.STANDARD: Qot_Common_pb2.OptionStandardType_Standard,
            self.NON_STANDARD: Qot_Common_pb2.OptionStandardType_NonStandard,
        }


# 期权结算方式
class OptionSettlementMode(FtEnum):
    NONE = 'N/A'
    AM = 'AM'
    PM = 'PM'

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.OptionSettlementMode_Unknown,
            self.AM: Qot_Common_pb2.OptionSettlementMode_AM,
            self.PM: Qot_Common_pb2.OptionSettlementMode_PM,
        }


# 期权市场类型
class OptionMarket(FtEnum):
    NONE = 'N/A'
    US_SECURITY = 'US_SECURITY'      # 美股股票期权
    US_INDEX = 'US_INDEX'            # 美股指数期权
    HK_SECURITY = 'HK_SECURITY'     # 港股股票期权
    HK_INDEX = 'HK_INDEX'           # 港股指数期权

    def load_dic(self):
        return {
            self.NONE: Qot_OptionCommon_pb2.OptionMarket_Unknown,
            self.US_SECURITY: Qot_OptionCommon_pb2.OptionMarket_US_Security,
            self.US_INDEX: Qot_OptionCommon_pb2.OptionMarket_US_Index,
            self.HK_SECURITY: Qot_OptionCommon_pb2.OptionMarket_HK_Security,
            self.HK_INDEX: Qot_OptionCommon_pb2.OptionMarket_HK_Index,
        }


# 期权统计数据类型
class OptionStatisticDataType(FtEnum):
    NONE = 'N/A'
    VOLUME = 'VOLUME'                # 成交量
    OPEN_INTEREST = 'OPEN_INTEREST'  # 持仓量

    def load_dic(self):
        return {
            self.NONE: Qot_OptionCommon_pb2.OptionStatisticDataType_Unknown,
            self.VOLUME: Qot_OptionCommon_pb2.OptionStatisticDataType_Volume,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.OptionStatisticDataType_OpenInterest,
        }


# 历史波动率时间范围
class OptionHVTimeRange(FtEnum):
    NONE = 'N/A'
    THIRTY_DAY = '30DAY'             # 30日
    SIXTY_DAY = '60DAY'              # 60日
    NINETY_DAY = '90DAY'             # 90日
    ONE_TWENTY_DAY = '120DAY'        # 120日
    THREE_SIXTY_FIVE_DAY = '365DAY'  # 365日

    def load_dic(self):
        return {
            self.NONE: Qot_OptionCommon_pb2.OptionHVTimeRange_Unknown,
            self.THIRTY_DAY: Qot_OptionCommon_pb2.OptionHVTimeRange_30Day,
            self.SIXTY_DAY: Qot_OptionCommon_pb2.OptionHVTimeRange_60Day,
            self.NINETY_DAY: Qot_OptionCommon_pb2.OptionHVTimeRange_90Day,
            self.ONE_TWENTY_DAY: Qot_OptionCommon_pb2.OptionHVTimeRange_120Day,
            self.THREE_SIXTY_FIVE_DAY: Qot_OptionCommon_pb2.OptionHVTimeRange_365Day,
        }


# 标的排行排序字段
class UnderlyingRankSortType(FtEnum):
    NONE = 'N/A'
    VOLUME = 'VOLUME'                          # 总成交量
    VOLUME_RATIO = 'VOLUME_RATIO'              # Put/Call成交量比值
    OPEN_INTEREST = 'OPEN_INTEREST'            # 总持仓量
    OPEN_INTEREST_RATIO = 'OPEN_INTEREST_RATIO'  # Put/Call持仓量比值
    PRICE = 'PRICE'                            # 最新价
    PRICE_CHANGE = 'PRICE_CHANGE'              # 涨跌幅
    IV = 'IV'                                  # IV
    IV_CHANGE = 'IV_CHANGE'                    # IV变化率
    HV = 'HV'                                  # HV
    HV_CHANGE = 'HV_CHANGE'                    # HV变化率
    IV_RANK = 'IV_RANK'                        # IV Rank
    IV_PERCENTILE = 'IV_PERCENTILE'            # IV Percentile
    MARKET_CAP = 'MARKET_CAP'                  # 市值

    def load_dic(self):
        return {
            self.NONE: Qot_OptionCommon_pb2.UnderlyingRankSortType_Unknown,
            self.VOLUME: Qot_OptionCommon_pb2.UnderlyingRankSortType_Volume,
            self.VOLUME_RATIO: Qot_OptionCommon_pb2.UnderlyingRankSortType_VolumeRatio,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.UnderlyingRankSortType_OpenInterest,
            self.OPEN_INTEREST_RATIO: Qot_OptionCommon_pb2.UnderlyingRankSortType_OpenInterestRatio,
            self.PRICE: Qot_OptionCommon_pb2.UnderlyingRankSortType_Price,
            self.PRICE_CHANGE: Qot_OptionCommon_pb2.UnderlyingRankSortType_PriceChange,
            self.IV: Qot_OptionCommon_pb2.UnderlyingRankSortType_IV,
            self.IV_CHANGE: Qot_OptionCommon_pb2.UnderlyingRankSortType_IVChange,
            self.HV: Qot_OptionCommon_pb2.UnderlyingRankSortType_HV,
            self.HV_CHANGE: Qot_OptionCommon_pb2.UnderlyingRankSortType_HVChange,
            self.IV_RANK: Qot_OptionCommon_pb2.UnderlyingRankSortType_IVRank,
            self.IV_PERCENTILE: Qot_OptionCommon_pb2.UnderlyingRankSortType_IVPercentile,
            self.MARKET_CAP: Qot_OptionCommon_pb2.UnderlyingRankSortType_MarketCap,
        }


# 期权合约排行类型
class OptionRankType(FtEnum):
    NONE = 'N/A'
    VOLUME = 'VOLUME'                            # 成交量排行
    TURNOVER = 'TURNOVER'                        # 成交额排行
    OI = 'OI'                                    # 持仓量排行
    OI_INCREMENT = 'OI_INCREMENT'                # 增仓量(日)排行
    OI_DECREMENT = 'OI_DECREMENT'                # 减仓量(日)排行
    OI_MARKET_CAP = 'OI_MARKET_CAP'              # 持仓额排行
    OI_MARKET_CAP_INCREMENT = 'OI_MARKET_CAP_INCREMENT'  # 增仓额(日)排行
    OI_MARKET_CAP_DECREMENT = 'OI_MARKET_CAP_DECREMENT'  # 减仓额(日)排行
    CHANGE_RATE = 'CHANGE_RATE'                  # 涨跌幅排行
    IV = 'IV'                                    # 隐含波动率排行

    def load_dic(self):
        return {
            self.NONE: Qot_OptionCommon_pb2.OptionRankType_Unknown,
            self.VOLUME: Qot_OptionCommon_pb2.OptionRankType_Volume,
            self.TURNOVER: Qot_OptionCommon_pb2.OptionRankType_Turnover,
            self.OI: Qot_OptionCommon_pb2.OptionRankType_OI,
            self.OI_INCREMENT: Qot_OptionCommon_pb2.OptionRankType_OIIncrement,
            self.OI_DECREMENT: Qot_OptionCommon_pb2.OptionRankType_OIDecrement,
            self.OI_MARKET_CAP: Qot_OptionCommon_pb2.OptionRankType_OIMarketCap,
            self.OI_MARKET_CAP_INCREMENT: Qot_OptionCommon_pb2.OptionRankType_OIMarketCapIncrement,
            self.OI_MARKET_CAP_DECREMENT: Qot_OptionCommon_pb2.OptionRankType_OIMarketCapDecrement,
            self.CHANGE_RATE: Qot_OptionCommon_pb2.OptionRankType_ChangeRate,
            self.IV: Qot_OptionCommon_pb2.OptionRankType_IV,
        }


# 末日期权标的排序
class ZeroDteSortType(FtEnum):
    UNKNOWN = 'N/A'
    VOLUME = 'VOLUME'              # 期权成交量
    IV = 'IV'                      # 隐含波动率
    CHANGE_RATIO = 'CHANGE_RATIO'  # 涨跌幅
    OPEN_INTEREST = 'OPEN_INTEREST'  # 持仓量
    MARKET_CAP = 'MARKET_CAP'      # 市值

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.ZeroDteSortType_Unknown,
            self.VOLUME: Qot_OptionCommon_pb2.ZeroDteSortType_Volume,
            self.IV: Qot_OptionCommon_pb2.ZeroDteSortType_IV,
            self.CHANGE_RATIO: Qot_OptionCommon_pb2.ZeroDteSortType_ChangeRate,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.ZeroDteSortType_OpenInterest,
            self.MARKET_CAP: Qot_OptionCommon_pb2.ZeroDteSortType_MarketCap,
        }


# 末日期权标的筛选因子类型
class ZeroDteIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    OWNER_LIST = 'OWNER_LIST'                        # 自选股列表(securityList)
    HAS_EARNINGS_THIS_WEEK = 'HAS_EARNINGS_THIS_WEEK'  # 本周是否有财报(valueList: 0=不限, 1=有, 2=无)
    VOLUME = 'VOLUME'                                # 期权总成交量
    OPEN_INTEREST = 'OPEN_INTEREST'                  # 期权总持仓量
    IV = 'IV'                                        # 隐含波动率(%)
    HV = 'HV'                                        # 历史波动率(%)
    IV_RANK = 'IV_RANK'                              # IV等级(%)
    IV_PERCENTILE = 'IV_PERCENTILE'                  # IV百分位数(%)
    PRICE = 'PRICE'                                  # 最新价
    CHANGE_RATIO = 'CHANGE_RATIO'                    # 涨跌幅(%)

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.ZeroDteIndicatorType_Unknown,
            self.OWNER_LIST: Qot_OptionCommon_pb2.ZeroDteIndicatorType_OwnerList,
            self.HAS_EARNINGS_THIS_WEEK: Qot_OptionCommon_pb2.ZeroDteIndicatorType_HasEarningsThisWeek,
            self.VOLUME: Qot_OptionCommon_pb2.ZeroDteIndicatorType_Volume,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.ZeroDteIndicatorType_OpenInterest,
            self.IV: Qot_OptionCommon_pb2.ZeroDteIndicatorType_IV,
            self.HV: Qot_OptionCommon_pb2.ZeroDteIndicatorType_HV,
            self.IV_RANK: Qot_OptionCommon_pb2.ZeroDteIndicatorType_IVRank,
            self.IV_PERCENTILE: Qot_OptionCommon_pb2.ZeroDteIndicatorType_IVPercentile,
            self.PRICE: Qot_OptionCommon_pb2.ZeroDteIndicatorType_Price,
            self.CHANGE_RATIO: Qot_OptionCommon_pb2.ZeroDteIndicatorType_ChangeRate,
        }


# 末日期权合约排序
class ZeroDteContractSortType(FtEnum):
    UNKNOWN = 'N/A'
    VOLUME = 'VOLUME'              # 成交量
    OPEN_INTEREST = 'OPEN_INTEREST'  # 持仓量
    IV = 'IV'                      # 隐含波动率
    DELTA = 'DELTA'                # Delta

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.ZeroDteContractSortType_Unknown,
            self.VOLUME: Qot_OptionCommon_pb2.ZeroDteContractSortType_Volume,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.ZeroDteContractSortType_OpenInterest,
            self.IV: Qot_OptionCommon_pb2.ZeroDteContractSortType_IV,
            self.DELTA: Qot_OptionCommon_pb2.ZeroDteContractSortType_Delta,
        }


# 末日期权合约筛选因子类型
class ZeroDteContractIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    OPTION_TYPE = 'OPTION_TYPE'                      # 期权方向(Qot_Common.OptionType: 1=Call, 2=Put)
    VOLUME = 'VOLUME'                                # 成交量
    OPEN_INTEREST = 'OPEN_INTEREST'                  # 未平仓数
    IV = 'IV'                                        # 隐含波动率(%)
    DELTA = 'DELTA'                                  # Delta
    GAMMA = 'GAMMA'                                  # Gamma
    THETA = 'THETA'                                  # Theta
    VEGA = 'VEGA'                                    # Vega
    RHO = 'RHO'                                      # Rho
    PRICE = 'PRICE'                                  # 最新价
    CHANGE_RATIO = 'CHANGE_RATIO'                    # 涨跌幅(%)
    BREAK_EVEN_POINT = 'BREAK_EVEN_POINT'            # 盈亏平衡点
    TO_BEP = 'TO_BEP'                                # 到盈亏平衡点(%)
    BUY_PROFIT_PROBABILITY = 'BUY_PROFIT_PROBABILITY'    # 买入盈利概率(%)
    SELL_PROFIT_PROBABILITY = 'SELL_PROFIT_PROBABILITY'  # 卖出盈利概率(%)

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_Unknown,
            self.OPTION_TYPE: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_OptionType,
            self.VOLUME: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_Volume,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_OpenInterest,
            self.IV: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_IV,
            self.DELTA: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_Delta,
            self.GAMMA: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_Gamma,
            self.THETA: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_Theta,
            self.VEGA: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_Vega,
            self.RHO: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_Rho,
            self.PRICE: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_Price,
            self.CHANGE_RATIO: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_ChangeRate,
            self.BREAK_EVEN_POINT: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_BreakEvenPoint,
            self.TO_BEP: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_ToBep,
            self.BUY_PROFIT_PROBABILITY: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_BuyProfitProbability,
            self.SELL_PROFIT_PROBABILITY: Qot_OptionCommon_pb2.ZeroDteContractIndicatorType_SellProfitProbability,
        }


# 财报排序
class EarningsSortType(FtEnum):
    UNKNOWN = 'N/A'
    EARNINGS_DATE = 'EARNINGS_DATE'                    # 财报日期(默认)
    VOLUME = 'VOLUME'                                  # 期权成交量
    IV = 'IV'                                          # 隐含波动率
    MARKET_CAP = 'MARKET_CAP'                          # 市值
    CHANGE_RATIO = 'CHANGE_RATIO'                      # 涨跌幅
    PRICE = 'PRICE'                                    # 最新价
    IV_RANK = 'IV_RANK'                                # IV等级
    IV_PERCENTILE = 'IV_PERCENTILE'                    # IV百分位数
    HV = 'HV'                                          # 历史波动率
    OPEN_INTEREST = 'OPEN_INTEREST'                    # 持仓量
    LAST_REPORT_IV_CRUSH = 'LAST_REPORT_IV_CRUSH'      # 上次IV Crush
    HISTORY_REPORT_IV_CRUSH = 'HISTORY_REPORT_IV_CRUSH'  # 历史IV Crush
    LAST_REPORT_CHG_RATIO = 'LAST_REPORT_CHG_RATIO'    # 上次财报日涨跌幅
    HISTORY_REPORT_CHG_RATIO = 'HISTORY_REPORT_CHG_RATIO'  # 历史财报日涨跌幅
    ESTIMATE_EPS_YOY = 'ESTIMATE_EPS_YOY'              # 预测EPS同比
    ESTIMATE_REVENUE_YOY = 'ESTIMATE_REVENUE_YOY'      # 预测营收同比
    EXPECTED_MOVE_RATIO = 'EXPECTED_MOVE_RATIO'        # 预测波动

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.EarningsSortType_Unknown,
            self.EARNINGS_DATE: Qot_OptionCommon_pb2.EarningsSortType_EarningsDate,
            self.VOLUME: Qot_OptionCommon_pb2.EarningsSortType_Volume,
            self.IV: Qot_OptionCommon_pb2.EarningsSortType_IV,
            self.MARKET_CAP: Qot_OptionCommon_pb2.EarningsSortType_MarketCap,
            self.CHANGE_RATIO: Qot_OptionCommon_pb2.EarningsSortType_ChangeRate,
            self.PRICE: Qot_OptionCommon_pb2.EarningsSortType_Price,
            self.IV_RANK: Qot_OptionCommon_pb2.EarningsSortType_IVRank,
            self.IV_PERCENTILE: Qot_OptionCommon_pb2.EarningsSortType_IVPercentile,
            self.HV: Qot_OptionCommon_pb2.EarningsSortType_HV,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.EarningsSortType_OpenInterest,
            self.LAST_REPORT_IV_CRUSH: Qot_OptionCommon_pb2.EarningsSortType_LastReportIvCrush,
            self.HISTORY_REPORT_IV_CRUSH: Qot_OptionCommon_pb2.EarningsSortType_HistoryReportIvCrush,
            self.LAST_REPORT_CHG_RATIO: Qot_OptionCommon_pb2.EarningsSortType_LastReportChgRate,
            self.HISTORY_REPORT_CHG_RATIO: Qot_OptionCommon_pb2.EarningsSortType_HistoryReportChgRate,
            self.ESTIMATE_EPS_YOY: Qot_OptionCommon_pb2.EarningsSortType_EstimateEpsYoy,
            self.ESTIMATE_REVENUE_YOY: Qot_OptionCommon_pb2.EarningsSortType_EstimateRevenueYoy,
            self.EXPECTED_MOVE_RATIO: Qot_OptionCommon_pb2.EarningsSortType_ExpectedMoveRatio,
        }


# 标的品类
class StockCategory(FtEnum):
    ALL = 'ALL'        # 全部
    EQUITY = 'EQUITY'  # 股票
    ETF = 'ETF'        # ETF

    def load_dic(self):
        return {
            self.ALL: Qot_OptionCommon_pb2.StockCategory_All,
            self.EQUITY: Qot_OptionCommon_pb2.StockCategory_Equity,
            self.ETF: Qot_OptionCommon_pb2.StockCategory_ETF,
        }


# 指数成分
class IndexComponent(FtEnum):
    UNKNOWN = 'N/A'
    DJI = 'DJI'    # 道琼斯
    IXIC = 'IXIC'  # 纳斯达克综合
    NDX = 'NDX'    # 纳斯达克100
    SPX = 'SPX'    # 标普500

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.IndexComponentType_Unknown,
            self.DJI: Qot_OptionCommon_pb2.IndexComponentType_DJI,
            self.IXIC: Qot_OptionCommon_pb2.IndexComponentType_IXIC,
            self.NDX: Qot_OptionCommon_pb2.IndexComponentType_NDX,
            self.SPX: Qot_OptionCommon_pb2.IndexComponentType_SPX,
        }


# 到期类型
class ExpirationType(FtEnum):
    UNKNOWN = 'N/A'
    MONTHLY = 'MONTHLY'          # 月期权
    WEEKLY = 'WEEKLY'            # 周期权
    END_OF_MONTH = 'END_OF_MONTH'  # 月末期权
    QUARTERLY = 'QUARTERLY'      # 季度期权

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.ExpirationType_Unknown,
            self.MONTHLY: Qot_OptionCommon_pb2.ExpirationType_Monthly,
            self.WEEKLY: Qot_OptionCommon_pb2.ExpirationType_Weekly,
            self.END_OF_MONTH: Qot_OptionCommon_pb2.ExpirationType_EndOfMonth,
            self.QUARTERLY: Qot_OptionCommon_pb2.ExpirationType_Quarterly,
        }


# 财报发布类型
class EarningsPubType(FtEnum):
    UNKNOWN = 'N/A'
    BEFORE = 'BEFORE'  # 盘前
    AFTER = 'AFTER'    # 盘后

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.EarningsPubType_Unknown,
            self.BEFORE: Qot_OptionCommon_pb2.EarningsPubType_Before,
            self.AFTER: Qot_OptionCommon_pb2.EarningsPubType_After,
        }


# 财报类型
class F10Type(FtEnum):
    NONE = 'None'
    Q1 = 'Q1'                              # 单季报，Q1
    Q2 = 'Q2'                              # 单季报，Q2
    Q3 = 'Q3'                              # 单季报，Q3
    Q4 = 'Q4'                              # 单季报，Q4
    Q6 = 'Q6'                              # 累计季报，Q6（Q1+Q2）
    Q9 = 'Q9'                              # 累计季报，Q9（Q1+Q2+Q3）
    ANNUAL = 'ANNUAL'                      # 年报
    QUARTERLY = 'QUARTERLY'                # 单季报组合（Q1, Q2, Q3, Q4）
    QUARTERLY_ANNUAL = 'QUARTERLY_ANNUAL'  # 单季报 + 年报
    MUL_QUARTERLY = 'MUL_QUARTERLY'        # 累计季报（Q1, Q6, Q9, Annual）

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.F10Type_Unknown,
            self.Q1: Qot_Common_pb2.F10Type_Q1,
            self.Q2: Qot_Common_pb2.F10Type_Q2,
            self.Q3: Qot_Common_pb2.F10Type_Q3,
            self.Q4: Qot_Common_pb2.F10Type_Q4,
            self.Q6: Qot_Common_pb2.F10Type_Q6,
            self.Q9: Qot_Common_pb2.F10Type_Q9,
            self.ANNUAL: Qot_Common_pb2.F10Type_Annual,
            self.QUARTERLY: Qot_Common_pb2.F10Type_Quarterly,
            self.QUARTERLY_ANNUAL: Qot_Common_pb2.F10Type_QuarterlyAnnual,
            self.MUL_QUARTERLY: Qot_Common_pb2.F10Type_MulQuarterly,
        }


# 财报发布时间类型
class EarningsPubTimeType(FtEnum):
    NONE = 'None'
    PRE_MARKET = 'PRE_MARKET'        # 盘前发布
    AFTER_MARKET = 'AFTER_MARKET'    # 盘后发布
    DURING_MARKET = 'DURING_MARKET'  # 盘中发布

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.EarningsPubTimeType_Unknown,
            self.PRE_MARKET: Qot_Common_pb2.EarningsPubTimeType_PreMarket,
            self.AFTER_MARKET: Qot_Common_pb2.EarningsPubTimeType_AfterMarket,
            self.DURING_MARKET: Qot_Common_pb2.EarningsPubTimeType_DuringMarket,
        }


# 主营构成维度类型
class RevenueBreakdownType(FtEnum):
    NONE = 'None'
    PRODUCT = 'PRODUCT'        # 产品
    INDUSTRY = 'INDUSTRY'      # 行业
    REGION = 'REGION'          # 地区
    BUSINESS = 'BUSINESS'      # 业务

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.RevenueBreakdownType_Unknown,
            self.PRODUCT: Qot_Common_pb2.RevenueBreakdownType_Product,
            self.INDUSTRY: Qot_Common_pb2.RevenueBreakdownType_Industry,
            self.REGION: Qot_Common_pb2.RevenueBreakdownType_Region,
            self.BUSINESS: Qot_Common_pb2.RevenueBreakdownType_Business,
        }


# 分析师综合评级类型
class ResearchRatingType(FtEnum):
    NONE = 'None'
    SELL = 'SELL'                    # Sell（卖出）
    UNDERPERFORM = 'UNDERPERFORM'    # Underperform（跑输大盘）
    HOLD = 'HOLD'                    # Hold（持有）
    BUY = 'BUY'                      # Buy（买入）
    STRONG_BUY = 'STRONG_BUY'        # Strong Buy（强力推荐）

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.ResearchRatingType_Unknown,
            self.SELL: Qot_Common_pb2.ResearchRatingType_Sell,
            self.UNDERPERFORM: Qot_Common_pb2.ResearchRatingType_Underperform,
            self.HOLD: Qot_Common_pb2.ResearchRatingType_Hold,
            self.BUY: Qot_Common_pb2.ResearchRatingType_Buy,
            self.STRONG_BUY: Qot_Common_pb2.ResearchRatingType_StrongBuy,
        }


# 评级维度类型
class ResearchRatingDimensionType(FtEnum):
    NONE = 'None'
    INSTITUTION = 'INSTITUTION'    # 机构维度（默认）
    ANALYST = 'ANALYST'            # 分析师维度

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.ResearchRatingDimensionType_Unknown,
            self.INSTITUTION: Qot_Common_pb2.ResearchRatingDimensionType_Institution,
            self.ANALYST: Qot_Common_pb2.ResearchRatingDimensionType_Analyst,
        }


# 晨星评级类型
class MorningstarRatingType(FtEnum):
    NONE = 'None'
    QUANTITATIVE = 'QUANTITATIVE'    # 定量评级（系统模型给出）
    QUALITATIVE = 'QUALITATIVE'      # 定性评级（分析师人工给出）

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.MorningstarRatingType_Unknown,
            self.QUANTITATIVE: Qot_Common_pb2.MorningstarRatingType_Quantitative,
            self.QUALITATIVE: Qot_Common_pb2.MorningstarRatingType_Qualitative,
        }


# 估值类型
class ValuationType(FtEnum):
    NONE = 'None'
    PE = 'PE'    # 市盈率
    PB = 'PB'    # 市净率
    PS = 'PS'    # 市销率

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.ValuationType_Unknown,
            self.PE: Qot_Common_pb2.ValuationType_PE,
            self.PB: Qot_Common_pb2.ValuationType_PB,
            self.PS: Qot_Common_pb2.ValuationType_PS,
        }


# 估值时间周期类型
class ValuationIntervalType(FtEnum):
    NONE = 'None'
    MONTH_3 = 'MONTH_3'        # 3个月
    MONTH_6 = 'MONTH_6'        # 6个月
    YEAR_1 = 'YEAR_1'          # 1年
    YEAR_2 = 'YEAR_2'          # 2年
    YEAR_3 = 'YEAR_3'          # 3年
    YEAR_5 = 'YEAR_5'          # 5年
    YEAR_10 = 'YEAR_10'        # 10年
    YEAR_20 = 'YEAR_20'        # 20年
    YEAR_30 = 'YEAR_30'        # 30年
    SINCE_2019 = 'SINCE_2019'  # 从2019年起

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.ValuationIntervalType_Unknown,
            self.MONTH_3: Qot_Common_pb2.ValuationIntervalType_Month3,
            self.MONTH_6: Qot_Common_pb2.ValuationIntervalType_Month6,
            self.YEAR_1: Qot_Common_pb2.ValuationIntervalType_Year1,
            self.YEAR_2: Qot_Common_pb2.ValuationIntervalType_Year2,
            self.YEAR_3: Qot_Common_pb2.ValuationIntervalType_Year3,
            self.YEAR_5: Qot_Common_pb2.ValuationIntervalType_Year5,
            self.YEAR_10: Qot_Common_pb2.ValuationIntervalType_Year10,
            self.YEAR_20: Qot_Common_pb2.ValuationIntervalType_Year20,
            self.YEAR_30: Qot_Common_pb2.ValuationIntervalType_Year30,
            self.SINCE_2019: Qot_Common_pb2.ValuationIntervalType_Since2019,
        }


# 持股变动筛选类型
class HoldingChangesFilterType(FtEnum):
    NONE = 'None'          # 全部（默认）
    INCREASE = 'INCREASE'  # 增持
    DECREASE = 'DECREASE'  # 减持
    NEW_IN = 'NEW_IN'      # 建仓
    CLOSE_OUT = 'CLOSE_OUT'  # 清仓

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.HoldingChangesFilterType_Unknown,
            self.INCREASE: Qot_Common_pb2.HoldingChangesFilterType_Increase,
            self.DECREASE: Qot_Common_pb2.HoldingChangesFilterType_Decrease,
            self.NEW_IN: Qot_Common_pb2.HoldingChangesFilterType_NewIn,
            self.CLOSE_OUT: Qot_Common_pb2.HoldingChangesFilterType_CloseOut,
        }


# 持股明细请求类型
class HolderDetailType(FtEnum):
    NONE = 'None'                            # 默认不过滤，按服务端默认逻辑返回
    ALL = 'ALL'                              # 全部
    UNCLASSIFIED = 'UNCLASSIFIED'            # 其他机构
    TRADITIONAL_INVESTMENT_MANAGER = 'TRADITIONAL_INVESTMENT_MANAGER'  # 传统投资经理
    HEDGE_FUND_MANAGER = 'HEDGE_FUND_MANAGER'  # 对冲基金
    VC_OR_PE = 'VC_OR_PE'                    # 风险资本/私募股权投资
    CORPORATE_PENSION_PLAN_SPONSOR = 'CORPORATE_PENSION_PLAN_SPONSOR'  # 企业年金
    FOUNDATION_FUND_SPONSOR = 'FOUNDATION_FUND_SPONSOR'                # 基金会基金
    INSURANCE_COMPANY = 'INSURANCE_COMPANY'  # 保险公司
    BANK_OR_INVESTMENT_BANK = 'BANK_OR_INVESTMENT_BANK'                # 银行/投资银行
    FAMILY_OFFICES_OR_TRUST = 'FAMILY_OFFICES_OR_TRUST'                # 家族办公室/信托
    SOVEREIGN_WEALTH_FUND = 'SOVEREIGN_WEALTH_FUND'                    # 主权财富基金
    REIT = 'REIT'                            # REIT
    STRUCTURED_FINANCE_POOL_MANAGER = 'STRUCTURED_FINANCE_POOL_MANAGER'  # 结构化融资经理
    UNION_PENSION_PLAN_SPONSOR = 'UNION_PENSION_PLAN_SPONSOR'          # 联合养老金
    GOVERNMENT_PENSION_PLAN_SPONSOR = 'GOVERNMENT_PENSION_PLAN_SPONSOR'  # 政府养老金
    ENDOWMENT_FUND_SPONSOR = 'ENDOWMENT_FUND_SPONSOR'                  # 捐赠基金
    INDIVIDUAL_INSIDERS = 'INDIVIDUAL_INSIDERS'                        # 个人
    ISSUE_SPONSORED_ADR = 'ISSUE_SPONSORED_ADR'                         # ADS
    CORPORATIONS_PUBLIC = 'CORPORATIONS_PUBLIC'                        # 上市公司
    CORPORATIONS_PRIVATE = 'CORPORATIONS_PRIVATE'                      # 未公开上市公司
    STATE_OWNED_SHARES = 'STATE_OWNED_SHARES'                          # 国有股

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.HolderDetailType_Default,
            self.ALL: Qot_Common_pb2.HolderDetailType_All,
            self.UNCLASSIFIED: Qot_Common_pb2.HolderDetailType_Unclassified,
            self.TRADITIONAL_INVESTMENT_MANAGER: Qot_Common_pb2.HolderDetailType_TraditionalInvestmentManager,
            self.HEDGE_FUND_MANAGER: Qot_Common_pb2.HolderDetailType_HedgeFundManager,
            self.VC_OR_PE: Qot_Common_pb2.HolderDetailType_VCOrPE,
            self.CORPORATE_PENSION_PLAN_SPONSOR: Qot_Common_pb2.HolderDetailType_CorporatePensionPlanSponsor,
            self.FOUNDATION_FUND_SPONSOR: Qot_Common_pb2.HolderDetailType_FoundationFundSponsor,
            self.INSURANCE_COMPANY: Qot_Common_pb2.HolderDetailType_InsuranceCompany,
            self.BANK_OR_INVESTMENT_BANK: Qot_Common_pb2.HolderDetailType_BankOrInvestmentBank,
            self.FAMILY_OFFICES_OR_TRUST: Qot_Common_pb2.HolderDetailType_FamilyOfficesOrTrust,
            self.SOVEREIGN_WEALTH_FUND: Qot_Common_pb2.HolderDetailType_SovereignWealthFund,
            self.REIT: Qot_Common_pb2.HolderDetailType_REIT,
            self.STRUCTURED_FINANCE_POOL_MANAGER: Qot_Common_pb2.HolderDetailType_StructuredFinancePoolManager,
            self.UNION_PENSION_PLAN_SPONSOR: Qot_Common_pb2.HolderDetailType_UnionPensionPlanSponsor,
            self.GOVERNMENT_PENSION_PLAN_SPONSOR: Qot_Common_pb2.HolderDetailType_GovernmentPensionPlanSponsor,
            self.ENDOWMENT_FUND_SPONSOR: Qot_Common_pb2.HolderDetailType_EndowmentFundSponsor,
            self.INDIVIDUAL_INSIDERS: Qot_Common_pb2.HolderDetailType_IndividualInsiders,
            self.ISSUE_SPONSORED_ADR: Qot_Common_pb2.HolderDetailType_IssueSponsoredADR,
            self.CORPORATIONS_PUBLIC: Qot_Common_pb2.HolderDetailType_CorporationsPublic,
            self.CORPORATIONS_PRIVATE: Qot_Common_pb2.HolderDetailType_CorporationsPrivate,
            self.STATE_OWNED_SHARES: Qot_Common_pb2.HolderDetailType_StateOwnedShares,
        }


# 财报日历排序类型
class EarningsCalendarSortType(FtEnum):
    UNKNOWN = 'N/A'
    HOT = 'HOT'                        # 热门(默认)
    MARKET_CAP = 'MARKET_CAP'          # 历史市值
    OPTION_VOLUME = 'OPTION_VOLUME'    # 期权成交量(仅港美股)
    IV = 'IV'                          # 隐含波动率(仅港美股)
    IV_RANK = 'IV_RANK'                # IV等级(仅港美股)
    IV_PERCENTILE = 'IV_PERCENTILE'    # IV百分位数(仅港美股)
    RT_MARKET_CAP = 'RT_MARKET_CAP'    # 实时市值

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetEarningsCalendar_pb2.EarningsCalendarSortType_Unknown,
            self.HOT: Qot_GetEarningsCalendar_pb2.EarningsCalendarSortType_Hot,
            self.MARKET_CAP: Qot_GetEarningsCalendar_pb2.EarningsCalendarSortType_MarketCap,
            self.OPTION_VOLUME: Qot_GetEarningsCalendar_pb2.EarningsCalendarSortType_OptionVolume,
            self.IV: Qot_GetEarningsCalendar_pb2.EarningsCalendarSortType_IV,
            self.IV_RANK: Qot_GetEarningsCalendar_pb2.EarningsCalendarSortType_IVRank,
            self.IV_PERCENTILE: Qot_GetEarningsCalendar_pb2.EarningsCalendarSortType_IVPercentile,
            self.RT_MARKET_CAP: Qot_GetEarningsCalendar_pb2.EarningsCalendarSortType_RtMarketCap,
        }


# 财报日历发布类型
class EarningsCalendarPubType(FtEnum):
    UNKNOWN = 'N/A'
    REGULAR = 'REGULAR'    # 盘中(未识别出时段)
    BEFORE = 'BEFORE'      # 盘前
    AFTER = 'AFTER'        # 盘后

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetEarningsCalendar_pb2.EarningsCalendarPubType_Unknown,
            self.REGULAR: Qot_GetEarningsCalendar_pb2.EarningsCalendarPubType_Regular,
            self.BEFORE: Qot_GetEarningsCalendar_pb2.EarningsCalendarPubType_Before,
            self.AFTER: Qot_GetEarningsCalendar_pb2.EarningsCalendarPubType_After,
        }


# 财报日历指标类型
class EarningsCalendarEstimateType(FtEnum):
    UNKNOWN = 'N/A'
    EPS = 'EPS'            # 每股收益(EPS GAAP)
    REVENUE = 'REVENUE'    # 总收入
    EBIT = 'EBIT'          # 息税前利润

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetEarningsCalendar_pb2.EarningsCalendarEstimateType_Unknown,
            self.EPS: Qot_GetEarningsCalendar_pb2.EarningsCalendarEstimateType_EPS,
            self.REVENUE: Qot_GetEarningsCalendar_pb2.EarningsCalendarEstimateType_Revenue,
            self.EBIT: Qot_GetEarningsCalendar_pb2.EarningsCalendarEstimateType_EBIT,
        }


# 财报日历周期类型
class EarningsCalendarPeriodType(FtEnum):
    UNKNOWN = 'N/A'
    QUARTERLY = 'QUARTERLY'        # 季度
    SEMI_ANNUAL = 'SEMI_ANNUAL'    # 半年度
    ANNUAL = 'ANNUAL'              # 年度

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetEarningsCalendar_pb2.EarningsCalendarPeriodType_Unknown,
            self.QUARTERLY: Qot_GetEarningsCalendar_pb2.EarningsCalendarPeriodType_Quarterly,
            self.SEMI_ANNUAL: Qot_GetEarningsCalendar_pb2.EarningsCalendarPeriodType_SemiAnnual,
            self.ANNUAL: Qot_GetEarningsCalendar_pb2.EarningsCalendarPeriodType_Annual,
        }


# 财报日历股票列表类型
class EarningsCalendarStockListType(FtEnum):
    UNKNOWN = 'N/A'
    WATCHLIST = 'WATCHLIST'      # 自选股
    POSITION = 'POSITION'        # 持仓
    SPECIAL = 'SPECIAL'          # 特别关注

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetEarningsCalendar_pb2.EarningsCalendarStockListType_Unknown,
            self.WATCHLIST: Qot_GetEarningsCalendar_pb2.EarningsCalendarStockListType_Watchlist,
            self.POSITION: Qot_GetEarningsCalendar_pb2.EarningsCalendarStockListType_Position,
            self.SPECIAL: Qot_GetEarningsCalendar_pb2.EarningsCalendarStockListType_Special,
        }


# 财报日历筛选因子类型
class EarningsCalendarIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    PUB_TYPE = 'PUB_TYPE'                  # 发布类型(valueList, EarningsCalendarPubType)
    ESTIMATE_TYPE = 'ESTIMATE_TYPE'        # 指标类型(valueList, EarningsCalendarEstimateType)
    MARKET_CAP = 'MARKET_CAP'              # 市值
    STOCK_LIST_TYPE = 'STOCK_LIST_TYPE'    # 股票列表类型(valueList, EarningsCalendarStockListType)
    OPTION_VOLUME = 'OPTION_VOLUME'        # 期权成交量(仅港美股)
    IV = 'IV'                              # 隐含波动率(仅港美股)
    IV_RANK = 'IV_RANK'                    # IV等级(仅港美股)
    IV_PERCENTILE = 'IV_PERCENTILE'        # IV百分位数(仅港美股)
    RT_MARKET_CAP = 'RT_MARKET_CAP'        # 实时市值

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_Unknown,
            self.PUB_TYPE: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_PubType,
            self.ESTIMATE_TYPE: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_EstimateType,
            self.MARKET_CAP: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_MarketCap,
            self.STOCK_LIST_TYPE: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_StockListType,
            self.OPTION_VOLUME: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_OptionVolume,
            self.IV: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_IV,
            self.IV_RANK: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_IVRank,
            self.IV_PERCENTILE: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_IVPercentile,
            self.RT_MARKET_CAP: Qot_GetEarningsCalendar_pb2.EarningsCalendarIndicatorType_RtMarketCap,
        }


# 财报机会筛选因子类型
class EarningsIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    OWNER_LIST = 'OWNER_LIST'                              # 自选股列表(securityList)
    INDEX_COMPONENT = 'INDEX_COMPONENT'                    # 所属指数(valueList, IndexComponentType)
    PLATE = 'PLATE'                                        # 所属行业/板块(valueList, 板块ID)
    MARKET_CAP = 'MARKET_CAP'                              # 市值
    EXPIRATION_TYPE = 'EXPIRATION_TYPE'                    # 到期类型(valueList, ExpirationType)
    IV = 'IV'                                              # 隐含波动率(%)
    LAST_REPORT_IV_CRUSH = 'LAST_REPORT_IV_CRUSH'          # 上次IV Crush(%)
    HISTORY_REPORT_IV_CRUSH = 'HISTORY_REPORT_IV_CRUSH'    # 历史IV Crush(%)
    IV_RANK = 'IV_RANK'                                    # IV等级(%)
    IV_PERCENTILE = 'IV_PERCENTILE'                        # IV百分位数(%)
    VOLUME = 'VOLUME'                                      # 期权成交量
    OPEN_INTEREST = 'OPEN_INTEREST'                        # 期权持仓量
    PRICE = 'PRICE'                                        # 最新价
    CHANGE_RATIO = 'CHANGE_RATIO'                          # 涨跌幅(%)
    EXPECTED_MOVE_RATIO = 'EXPECTED_MOVE_RATIO'            # 预测波动(%)
    LAST_REPORT_CHG_RATIO = 'LAST_REPORT_CHG_RATIO'        # 上次财报日涨跌幅(%)
    HISTORY_REPORT_CHG_RATIO = 'HISTORY_REPORT_CHG_RATIO'  # 历史财报日涨跌幅(%)
    ESTIMATE_REVENUE_YOY = 'ESTIMATE_REVENUE_YOY'          # 预测营收同比(%)
    ESTIMATE_EPS_YOY = 'ESTIMATE_EPS_YOY'                  # 预测EPS同比(%)
    EARNINGS_DAY_RANGE = 'EARNINGS_DAY_RANGE'              # 距财报日天数

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.EarningsIndicatorType_Unknown,
            self.OWNER_LIST: Qot_OptionCommon_pb2.EarningsIndicatorType_OwnerList,
            self.INDEX_COMPONENT: Qot_OptionCommon_pb2.EarningsIndicatorType_IndexComponent,
            self.PLATE: Qot_OptionCommon_pb2.EarningsIndicatorType_Plate,
            self.MARKET_CAP: Qot_OptionCommon_pb2.EarningsIndicatorType_MarketCap,
            self.EXPIRATION_TYPE: Qot_OptionCommon_pb2.EarningsIndicatorType_ExpirationType,
            self.IV: Qot_OptionCommon_pb2.EarningsIndicatorType_IV,
            self.LAST_REPORT_IV_CRUSH: Qot_OptionCommon_pb2.EarningsIndicatorType_LastReportIvCrush,
            self.HISTORY_REPORT_IV_CRUSH: Qot_OptionCommon_pb2.EarningsIndicatorType_HistoryReportIvCrush,
            self.IV_RANK: Qot_OptionCommon_pb2.EarningsIndicatorType_IVRank,
            self.IV_PERCENTILE: Qot_OptionCommon_pb2.EarningsIndicatorType_IVPercentile,
            self.VOLUME: Qot_OptionCommon_pb2.EarningsIndicatorType_Volume,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.EarningsIndicatorType_OpenInterest,
            self.PRICE: Qot_OptionCommon_pb2.EarningsIndicatorType_Price,
            self.CHANGE_RATIO: Qot_OptionCommon_pb2.EarningsIndicatorType_ChangeRate,
            self.EXPECTED_MOVE_RATIO: Qot_OptionCommon_pb2.EarningsIndicatorType_ExpectedMoveRatio,
            self.LAST_REPORT_CHG_RATIO: Qot_OptionCommon_pb2.EarningsIndicatorType_LastReportChgRate,
            self.HISTORY_REPORT_CHG_RATIO: Qot_OptionCommon_pb2.EarningsIndicatorType_HistoryReportChgRate,
            self.ESTIMATE_REVENUE_YOY: Qot_OptionCommon_pb2.EarningsIndicatorType_EstimateRevenueYoy,
            self.ESTIMATE_EPS_YOY: Qot_OptionCommon_pb2.EarningsIndicatorType_EstimateEpsYoy,
            self.EARNINGS_DAY_RANGE: Qot_OptionCommon_pb2.EarningsIndicatorType_EarningsDayRange,
        }


# 卖方策略类型
class SellerType(FtEnum):
    UNKNOWN = 'N/A'
    COVERED_CALL = 'COVERED_CALL'          # 股票担保看涨期权
    CASH_SECURED_PUT = 'CASH_SECURED_PUT'  # 现金担保看跌期权

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.SellerType_Unknown,
            self.COVERED_CALL: Qot_OptionCommon_pb2.SellerType_CoveredCall,
            self.CASH_SECURED_PUT: Qot_OptionCommon_pb2.SellerType_CashSecuredPut,
        }


# 卖方专区排序
class SellerSortType(FtEnum):
    UNKNOWN = 'N/A'
    ANNUALIZED_RETURN = 'ANNUALIZED_RETURN'  # 年化收益率
    INTERVAL_RETURN = 'INTERVAL_RETURN'      # 区间收益率
    ITM_PROBABILITY = 'ITM_PROBABILITY'      # 行权概率
    PREMIUM = 'PREMIUM'                      # 权利金

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.SellerSortType_Unknown,
            self.ANNUALIZED_RETURN: Qot_OptionCommon_pb2.SellerSortType_AnnualizedReturn,
            self.INTERVAL_RETURN: Qot_OptionCommon_pb2.SellerSortType_IntervalReturn,
            self.ITM_PROBABILITY: Qot_OptionCommon_pb2.SellerSortType_ItmProbability,
            self.PREMIUM: Qot_OptionCommon_pb2.SellerSortType_Premium,
        }


# 卖方专区筛选因子类型
class SellerIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    # ---- 标的级 ----
    OWNER_LIST = 'OWNER_LIST'                          # 自选股列表(securityList)
    STOCK_CATEGORY = 'STOCK_CATEGORY'                  # 标的品类(valueList, StockCategory)
    VOLUME = 'VOLUME'                                  # 期权总成交量(默认>0)
    OPEN_INTEREST = 'OPEN_INTEREST'                    # 期权总持仓量(默认>0)
    IV = 'IV'                                          # 标的IV(%)
    HV = 'HV'                                          # 标的HV(%)
    IV_RANK = 'IV_RANK'                                # IV等级(%)
    IV_PERCENTILE = 'IV_PERCENTILE'                    # IV百分位数(%)
    MARKET_CAP = 'MARKET_CAP'                          # 标的市值(默认>10B)
    PRICE = 'PRICE'                                    # 标的最新价(默认>$1)
    CHANGE_RATIO = 'CHANGE_RATIO'                      # 标的涨跌幅(%)
    PLATE = 'PLATE'                                    # 板块(valueList, 板块ID)
    EXPIRATION_TYPE = 'EXPIRATION_TYPE'                # 到期类型(valueList, ExpirationType)
    # ---- 期权级 ----
    LEFT_DAYS = 'LEFT_DAYS'                            # 距到期日(天)(默认>0)
    OPTION_EXPIRATION_TYPE = 'OPTION_EXPIRATION_TYPE'  # 期权到期类型(valueList, ExpirationType)
    STRIKE_DATE_TIMESTAMP = 'STRIKE_DATE_TIMESTAMP'    # 到期日时间戳(valueList, 秒)
    PREMIUM = 'PREMIUM'                                # 权利金
    ANNUALIZED_RETURN = 'ANNUALIZED_RETURN'            # 年化收益率(%)
    INTERVAL_RETURN = 'INTERVAL_RETURN'                # 区间收益率(%)
    OTM_DEGREE = 'OTM_DEGREE'                          # 价外程度(%)(默认>0)
    OTM_PROBABILITY = 'OTM_PROBABILITY'                # 价外概率(%)
    OPTION_IV = 'OPTION_IV'                            # 期权隐含波动率(%)
    BID_PRICE = 'BID_PRICE'                            # 期权买价(默认>$0.01)
    ASK_PRICE = 'ASK_PRICE'                            # 期权卖价(默认>$0.01)
    OPTION_VOLUME = 'OPTION_VOLUME'                    # 期权成交量(默认>0)
    OPTION_OPEN_INTEREST = 'OPTION_OPEN_INTEREST'      # 期权持仓量(默认>0)

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_OptionCommon_pb2.SellerIndicatorType_Unknown,
            self.OWNER_LIST: Qot_OptionCommon_pb2.SellerIndicatorType_OwnerList,
            self.STOCK_CATEGORY: Qot_OptionCommon_pb2.SellerIndicatorType_StockCategory,
            self.VOLUME: Qot_OptionCommon_pb2.SellerIndicatorType_Volume,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.SellerIndicatorType_OpenInterest,
            self.IV: Qot_OptionCommon_pb2.SellerIndicatorType_IV,
            self.HV: Qot_OptionCommon_pb2.SellerIndicatorType_HV,
            self.IV_RANK: Qot_OptionCommon_pb2.SellerIndicatorType_IVRank,
            self.IV_PERCENTILE: Qot_OptionCommon_pb2.SellerIndicatorType_IVPercentile,
            self.MARKET_CAP: Qot_OptionCommon_pb2.SellerIndicatorType_MarketCap,
            self.PRICE: Qot_OptionCommon_pb2.SellerIndicatorType_Price,
            self.CHANGE_RATIO: Qot_OptionCommon_pb2.SellerIndicatorType_ChangeRate,
            self.PLATE: Qot_OptionCommon_pb2.SellerIndicatorType_Plate,
            self.EXPIRATION_TYPE: Qot_OptionCommon_pb2.SellerIndicatorType_ExpirationType,
            self.LEFT_DAYS: Qot_OptionCommon_pb2.SellerIndicatorType_LeftDays,
            self.OPTION_EXPIRATION_TYPE: Qot_OptionCommon_pb2.SellerIndicatorType_OptionExpirationType,
            self.STRIKE_DATE_TIMESTAMP: Qot_OptionCommon_pb2.SellerIndicatorType_StrikeDateTimestamp,
            self.PREMIUM: Qot_OptionCommon_pb2.SellerIndicatorType_Premium,
            self.ANNUALIZED_RETURN: Qot_OptionCommon_pb2.SellerIndicatorType_AnnualizedReturn,
            self.INTERVAL_RETURN: Qot_OptionCommon_pb2.SellerIndicatorType_IntervalReturn,
            self.OTM_DEGREE: Qot_OptionCommon_pb2.SellerIndicatorType_OtmDegree,
            self.OTM_PROBABILITY: Qot_OptionCommon_pb2.SellerIndicatorType_OtmProbability,
            self.OPTION_IV: Qot_OptionCommon_pb2.SellerIndicatorType_OptionIV,
            self.BID_PRICE: Qot_OptionCommon_pb2.SellerIndicatorType_BidPrice,
            self.ASK_PRICE: Qot_OptionCommon_pb2.SellerIndicatorType_AskPrice,
            self.OPTION_VOLUME: Qot_OptionCommon_pb2.SellerIndicatorType_OptionVolume,
            self.OPTION_OPEN_INTEREST: Qot_OptionCommon_pb2.SellerIndicatorType_OptionOpenInterest,
        }


# 标的排行筛选因子类型
class UnderlyingRankIndicatorType(FtEnum):
    NONE = 'N/A'
    OWNER_LIST = 'OWNER_LIST'                    # 指定标的列表(securityList)
    STOCK_CATEGORY = 'STOCK_CATEGORY'            # 标的品类(valueList, StockCategory)
    VOLUME = 'VOLUME'                            # 总成交量
    OPEN_INTEREST = 'OPEN_INTEREST'              # 总持仓量
    IV = 'IV'                                    # IV(%)
    HV = 'HV'                                    # HV(%)
    IV_RANK = 'IV_RANK'                          # IV Rank(%)
    IV_PERCENTILE = 'IV_PERCENTILE'              # IV Percentile(%)
    IV_CHANGE = 'IV_CHANGE'                      # IV变化率(%)
    HV_CHANGE = 'HV_CHANGE'                      # HV变化率(%)
    VOLUME_RATIO = 'VOLUME_RATIO'                # 成交量P/C比值(%)
    OI_RATIO = 'OI_RATIO'                        # 持仓量P/C比值(%)
    MARKET_CAP = 'MARKET_CAP'                    # 市值

    def load_dic(self):
        return {
            self.NONE: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_Unknown,
            self.OWNER_LIST: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_OwnerList,
            self.STOCK_CATEGORY: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_StockCategory,
            self.VOLUME: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_Volume,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_OpenInterest,
            self.IV: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_IV,
            self.HV: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_HV,
            self.IV_RANK: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_IVRank,
            self.IV_PERCENTILE: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_IVPercentile,
            self.IV_CHANGE: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_IVChange,
            self.HV_CHANGE: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_HVChange,
            self.VOLUME_RATIO: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_VolumeRatio,
            self.OI_RATIO: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_OIRatio,
            self.MARKET_CAP: Qot_OptionCommon_pb2.UnderlyingRankIndicatorType_MarketCap,
        }


# 期权合约排行筛选因子类型
class OptionRankIndicatorType(FtEnum):
    NONE = 'N/A'
    # 标的级
    STOCK_CATEGORY = 'STOCK_CATEGORY'            # 品类(StockCategory)
    MARKET_CAP = 'MARKET_CAP'                    # 市值
    OWNER_LIST = 'OWNER_LIST'                    # 股票范围(securityList)
    UNDERLYING_IV = 'UNDERLYING_IV'              # 正股IV(%)
    UNDERLYING_HV = 'UNDERLYING_HV'              # 正股HV(%)
    IV_RANK = 'IV_RANK'                          # IV等级(%)
    IV_PERCENTILE = 'IV_PERCENTILE'              # IV百分位数(%)
    # 期权级
    IV = 'IV'                                    # 隐含波动率(%)
    OPTION_TYPE = 'OPTION_TYPE'                  # 方向(Call/Put)
    LEFT_DAYS = 'LEFT_DAYS'                      # 距到期日
    IN_THE_MONEY = 'IN_THE_MONEY'                # 价内/价外(0=价外,1=价内)
    VOLUME = 'VOLUME'                            # 成交量
    OPEN_INTEREST = 'OPEN_INTEREST'              # 持仓量
    DELTA = 'DELTA'                              # Delta
    GAMMA = 'GAMMA'                              # Gamma
    THETA = 'THETA'                              # Theta
    VEGA = 'VEGA'                                # Vega
    RHO = 'RHO'                                  # Rho

    def load_dic(self):
        return {
            self.NONE: Qot_OptionCommon_pb2.OptionRankIndicatorType_Unknown,
            self.STOCK_CATEGORY: Qot_OptionCommon_pb2.OptionRankIndicatorType_StockCategory,
            self.MARKET_CAP: Qot_OptionCommon_pb2.OptionRankIndicatorType_MarketCap,
            self.OWNER_LIST: Qot_OptionCommon_pb2.OptionRankIndicatorType_OwnerList,
            self.UNDERLYING_IV: Qot_OptionCommon_pb2.OptionRankIndicatorType_UnderlyingIV,
            self.UNDERLYING_HV: Qot_OptionCommon_pb2.OptionRankIndicatorType_UnderlyingHV,
            self.IV_RANK: Qot_OptionCommon_pb2.OptionRankIndicatorType_IVRank,
            self.IV_PERCENTILE: Qot_OptionCommon_pb2.OptionRankIndicatorType_IVPercentile,
            self.IV: Qot_OptionCommon_pb2.OptionRankIndicatorType_IV,
            self.OPTION_TYPE: Qot_OptionCommon_pb2.OptionRankIndicatorType_OptionType,
            self.LEFT_DAYS: Qot_OptionCommon_pb2.OptionRankIndicatorType_LeftDays,
            self.IN_THE_MONEY: Qot_OptionCommon_pb2.OptionRankIndicatorType_InTheMoney,
            self.VOLUME: Qot_OptionCommon_pb2.OptionRankIndicatorType_Volume,
            self.OPEN_INTEREST: Qot_OptionCommon_pb2.OptionRankIndicatorType_OpenInterest,
            self.DELTA: Qot_OptionCommon_pb2.OptionRankIndicatorType_Delta,
            self.GAMMA: Qot_OptionCommon_pb2.OptionRankIndicatorType_Gamma,
            self.THETA: Qot_OptionCommon_pb2.OptionRankIndicatorType_Theta,
            self.VEGA: Qot_OptionCommon_pb2.OptionRankIndicatorType_Vega,
            self.RHO: Qot_OptionCommon_pb2.OptionRankIndicatorType_Rho,
        }


# 期权异动筛选因子类型
class EventIndicatorType(FtEnum):
    NONE = 'N/A'
    # 标的相关 (1xx)
    OWNER_LIST = 'OWNER_LIST'                    # 指定标的列表
    INDUSTRY_PLATE = 'INDUSTRY_PLATE'            # 行业板块列表
    CONCEPT_PLATE = 'CONCEPT_PLATE'              # 概念板块列表
    CORPORATE_ACTION = 'CORPORATE_ACTION'        # 公司行动类型
    MARKET_CAP = 'MARKET_CAP'                    # 标的市值
    # 期权合约属性 (2xx)
    OPTION_TYPE = 'OPTION_TYPE'                  # CALL/PUT
    MONEY_TYPE = 'MONEY_TYPE'                    # 价内/价外
    STRIKE_PRICE = 'STRIKE_PRICE'                # 行权价
    EXPIRY_DAYS = 'EXPIRY_DAYS'                  # 距到期天数
    OTM = 'OTM'                                  # 价外比率
    # 成交信息 (3xx)
    TICKER_TYPE = 'TICKER_TYPE'                  # 成交方向
    VOLUME = 'VOLUME'                            # 成交量
    TURNOVER = 'TURNOVER'                        # 成交额
    PRICE = 'PRICE'                              # 成交价
    TIME = 'TIME'                                # 异动时间
    MAX_DAY_NUM = 'MAX_DAY_NUM'                  # 时间范围天数
    # 订单分类 (4xx)
    ORDER_TYPE = 'ORDER_TYPE'                    # 订单类型
    STRATEGY = 'STRATEGY'                        # 策略类型
    SENTIMENT = 'SENTIMENT'                      # 市场情绪
    # 期权行情统计 (5xx)
    TOTAL_VOLUME = 'TOTAL_VOLUME'                # 期权总成交量
    TOTAL_OI = 'TOTAL_OI'                        # 期权总持仓量
    VO_RATIO = 'VO_RATIO'                        # 量仓比
    IV = 'IV'                                    # 隐含波动率
    # 希腊值 (6xx)
    DELTA = 'DELTA'                              # Delta
    GAMMA = 'GAMMA'                              # Gamma
    VEGA = 'VEGA'                                # Vega
    THETA = 'THETA'                              # Theta
    RHO = 'RHO'                                  # Rho

    def load_dic(self):
        return {
            self.NONE: Qot_GetOptionEvent_pb2.EventIndicatorType_Unknown,
            self.OWNER_LIST: Qot_GetOptionEvent_pb2.EventIndicatorType_OwnerList,
            self.INDUSTRY_PLATE: Qot_GetOptionEvent_pb2.EventIndicatorType_IndustryPlate,
            self.CONCEPT_PLATE: Qot_GetOptionEvent_pb2.EventIndicatorType_ConceptPlate,
            self.CORPORATE_ACTION: Qot_GetOptionEvent_pb2.EventIndicatorType_CorporateAction,
            self.MARKET_CAP: Qot_GetOptionEvent_pb2.EventIndicatorType_MarketCap,
            self.OPTION_TYPE: Qot_GetOptionEvent_pb2.EventIndicatorType_OptionType,
            self.MONEY_TYPE: Qot_GetOptionEvent_pb2.EventIndicatorType_MoneyType,
            self.STRIKE_PRICE: Qot_GetOptionEvent_pb2.EventIndicatorType_StrikePrice,
            self.EXPIRY_DAYS: Qot_GetOptionEvent_pb2.EventIndicatorType_ExpiryDays,
            self.OTM: Qot_GetOptionEvent_pb2.EventIndicatorType_OTM,
            self.TICKER_TYPE: Qot_GetOptionEvent_pb2.EventIndicatorType_TickerType,
            self.VOLUME: Qot_GetOptionEvent_pb2.EventIndicatorType_Volume,
            self.TURNOVER: Qot_GetOptionEvent_pb2.EventIndicatorType_Turnover,
            self.PRICE: Qot_GetOptionEvent_pb2.EventIndicatorType_Price,
            self.TIME: Qot_GetOptionEvent_pb2.EventIndicatorType_Time,
            self.MAX_DAY_NUM: Qot_GetOptionEvent_pb2.EventIndicatorType_MaxDayNum,
            self.ORDER_TYPE: Qot_GetOptionEvent_pb2.EventIndicatorType_OrderType,
            self.STRATEGY: Qot_GetOptionEvent_pb2.EventIndicatorType_Strategy,
            self.SENTIMENT: Qot_GetOptionEvent_pb2.EventIndicatorType_Sentiment,
            self.TOTAL_VOLUME: Qot_GetOptionEvent_pb2.EventIndicatorType_TotalVolume,
            self.TOTAL_OI: Qot_GetOptionEvent_pb2.EventIndicatorType_TotalOI,
            self.VO_RATIO: Qot_GetOptionEvent_pb2.EventIndicatorType_VoRatio,
            self.IV: Qot_GetOptionEvent_pb2.EventIndicatorType_IV,
            self.DELTA: Qot_GetOptionEvent_pb2.EventIndicatorType_Delta,
            self.GAMMA: Qot_GetOptionEvent_pb2.EventIndicatorType_Gamma,
            self.VEGA: Qot_GetOptionEvent_pb2.EventIndicatorType_Vega,
            self.THETA: Qot_GetOptionEvent_pb2.EventIndicatorType_Theta,
            self.RHO: Qot_GetOptionEvent_pb2.EventIndicatorType_Rho,
        }


# 期权异动成交方向
class EventTickerType(FtEnum):
    NONE = 'N/A'
    BUY = 'BUY'            # 主动买入
    SELL = 'SELL'          # 主动卖出
    NEUTRAL = 'NEUTRAL'    # 中性盘

    def load_dic(self):
        return {
            self.NONE: Qot_GetOptionEvent_pb2.TickerType_Unknown,
            self.BUY: Qot_GetOptionEvent_pb2.TickerType_Buy,
            self.SELL: Qot_GetOptionEvent_pb2.TickerType_Sell,
            self.NEUTRAL: Qot_GetOptionEvent_pb2.TickerType_Neutral,
        }


# 期权异动订单类型 (proto enum: OptionOrderType)
class EventOrderType(FtEnum):
    NORMAL = 'NORMAL'      # 普通订单
    SWEEP = 'SWEEP'        # 扫单
    CROSS = 'CROSS'        # 对敲单
    FLOOR = 'FLOOR'        # 场内单

    def load_dic(self):
        return {
            self.NORMAL: Qot_GetOptionEvent_pb2.OptionOrderType_Normal,
            self.SWEEP: Qot_GetOptionEvent_pb2.OptionOrderType_Sweep,
            self.CROSS: Qot_GetOptionEvent_pb2.OptionOrderType_Cross,
            self.FLOOR: Qot_GetOptionEvent_pb2.OptionOrderType_Floor,
        }


# 期权异动策略类型
class EventTickerStrategy(FtEnum):
    NONE = 'N/A'
    SINGLE_LEG = 'SINGLE_LEG'    # 单腿交易
    MULTI_LEG = 'MULTI_LEG'      # 多腿策略交易

    def load_dic(self):
        return {
            self.NONE: Qot_GetOptionEvent_pb2.TickerStrategy_Unknown,
            self.SINGLE_LEG: Qot_GetOptionEvent_pb2.TickerStrategy_SingleLeg,
            self.MULTI_LEG: Qot_GetOptionEvent_pb2.TickerStrategy_MultiLeg,
        }


# 期权异动市场情绪
class EventMarketSentiment(FtEnum):
    NONE = 'N/A'
    BEARISH = 'BEARISH'    # 看空
    BULLISH = 'BULLISH'    # 看多
    NEUTRAL = 'NEUTRAL'    # 中性

    def load_dic(self):
        return {
            self.NONE: Qot_GetOptionEvent_pb2.MarketSentiment_Unknown,
            self.BEARISH: Qot_GetOptionEvent_pb2.MarketSentiment_Bearish,
            self.BULLISH: Qot_GetOptionEvent_pb2.MarketSentiment_Bullish,
            self.NEUTRAL: Qot_GetOptionEvent_pb2.MarketSentiment_Neutral,
        }


# 期权异动排序方向
class EventSortDir(FtEnum):
    ASCEND = 'ASCEND'      # 升序
    DESCEND = 'DESCEND'    # 降序

    def load_dic(self):
        return {
            self.ASCEND: True,
            self.DESCEND: False,
        }


# 期权异动提醒订单类型 (proto enum: OptionOrderType in Qot_GetOptionEvent)
class AlertOrderType(FtEnum):
    UNKNOWN = 'N/A'
    SWEEP = 'SWEEP'        # 扫单
    FLOOR = 'FLOOR'        # 场内单
    CROSS = 'CROSS'        # 对敲单
    NORMAL = 'NORMAL'      # 普通订单

    def load_dic(self):
        return {
            self.SWEEP: Qot_GetOptionEvent_pb2.OptionOrderType_Sweep,
            self.FLOOR: Qot_GetOptionEvent_pb2.OptionOrderType_Floor,
            self.CROSS: Qot_GetOptionEvent_pb2.OptionOrderType_Cross,
            self.NORMAL: Qot_GetOptionEvent_pb2.OptionOrderType_Normal,
        }


# 期权异动提醒操作类型
class AlertOpType(FtEnum):
    UNKNOWN = 'N/A'
    ADD = 'ADD'              # 新增
    DELETE = 'DELETE'         # 删除
    MODIFY = 'MODIFY'        # 修改
    ENABLE = 'ENABLE'        # 启用
    DISABLE = 'DISABLE'      # 禁用
    DELETE_ALL = 'DELETE_ALL' # 删除全部

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_SetOptionEventAlert_pb2.AlertOpType_Unknown,
            self.ADD: Qot_SetOptionEventAlert_pb2.AlertOpType_Add,
            self.DELETE: Qot_SetOptionEventAlert_pb2.AlertOpType_Delete,
            self.MODIFY: Qot_SetOptionEventAlert_pb2.AlertOpType_Modify,
            self.ENABLE: Qot_SetOptionEventAlert_pb2.AlertOpType_Enable,
            self.DISABLE: Qot_SetOptionEventAlert_pb2.AlertOpType_Disable,
            self.DELETE_ALL: Qot_SetOptionEventAlert_pb2.AlertOpType_DeleteAll,
        }


class RunMode(FtEnum):
    DEFAULT = 'DEFAULT'
    QUANT = 'QUANT'


# PDT Status
class DTStatus(FtEnum):
    NONE = 'N/A'
    UNLIMITED = 'UNLIMITED'
    DT_CALL = 'DT_CALL'
    EM_CALL = 'EM_CALL'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.DTStatus_Unknown,
            self.UNLIMITED: Trd_Common_pb2.DTStatus_Unlimited,
            self.DT_CALL: Trd_Common_pb2.DTStatus_DTCall,
            self.EM_CALL: Trd_Common_pb2.DTStatus_EMCall
        }

# 获取资金流向的周期类型
class PeriodType(FtEnum):
    NONE = 'N/A'
    INTRADAY = 'INTRADAY'
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PeriodType_Unknown,
            self.INTRADAY: Qot_Common_pb2.PeriodType_INTRADAY,
            self.DAY: Qot_Common_pb2.PeriodType_DAY,
            self.WEEK: Qot_Common_pb2.PeriodType_WEEK,
            self.MONTH: Qot_Common_pb2.PeriodType_MONTH
        }

# 获取资金流向的周期类型
class CashFlowDirection(FtEnum):
    NONE = 'N/A'
    IN = 'IN'
    OUT = 'OUT'

    def load_dic(self):
        return {
            self.NONE: Trd_FlowSummary_pb2.TrdCashFlowDirection_Unknown,
            self.IN: Trd_FlowSummary_pb2.TrdCashFlowDirection_In,
            self.OUT: Trd_FlowSummary_pb2.TrdCashFlowDirection_Out,
        }

# 获取资金流向的周期类型
class AssetCategory(FtEnum):
    NONE = 'N/A'
    JP = 'JP'
    US = 'US'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.TrdAssetCategory_Unknown,
            self.JP: Trd_Common_pb2.TrdAssetCategory_JP,
            self.US: Trd_Common_pb2.TrdAssetCategory_US,
        }

# JP 子账户类型
class SubAccType(FtEnum):
    NONE = 'N/A'
    JP_GENERAL = 'JP_GENERAL' # 日本 - 一般口座 - long
    JP_TOKUTEI = 'JP_TOKUTEI' # 日本 - 特定口座 - long
    JP_NISA_GENERAL = 'JP_NISA_GENERAL' # 日本 - 一般NISA
    JP_NISA_TSUMITATE = 'JP_NISA_TSUMITATE' # 日本 - 累计NISA

    JP_GENERAL_SHORT = 'JP_GENERAL_SHORT' # 日本 - 一般口座 - Short
    JP_TOKUTEI_SHORT = 'JP_TOKUTEI_SHORT' # 日本 - 特定口座 - Short
    JP_HONPO_GENERAL = 'JP_HONPO_GENERAL' # 日本 - 本国信用交易抵押品 - 一般
    JP_GAIKOKU_GENERAL = 'JP_GAIKOKU_GENERAL' # 日本 - 外国信用交易抵押品 - 一般
    JP_HONPO_TOKUTEI = 'JP_HONPO_TOKUTEI' # 日本 - 本国信用交易抵押品 - 特定
    JP_GAIKOKU_TOKUTEI = 'JP_GAIKOKU_TOKUTEI' # 日本 - 外国信用交易抵押品 - 特定

    JP_DERIVATIVE_LONG = 'JP_DERIVATIVE_LONG' # 日本 - 衍生品 - Long
    JP_DERIVATIVE_SHORT = 'JP_DERIVATIVE_SHORT' # 日本 - 衍生品 - Short
    JP_HONPO_DERIVATIVE_GENERAL = 'JP_HONPO_DERIVATIVE_GENERAL' # 日本 - 本国衍生品证据金 - 一般
    JP_GAIKOKU_DERIVATIVE_GENERAL = 'JP_GAIKOKU_DERIVATIVE_GENERAL' # 日本 - 外国衍生品证据金 - 一般
    JP_HONPO_DERIVATIVE_TOKUTEI = 'JP_HONPO_DERIVATIVE_TOKUTEI' # 日本 - 本国衍生品证据金 - 特定
    JP_GAIKOKU_DERIVATIVE_TOKUTEI = 'JP_GAIKOKU_DERIVATIVE_TOKUTEI' # 日本 - 外国衍生品证据金 - 特定

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.TrdSubAccType_None,
            self.JP_GENERAL: Trd_Common_pb2.TrdSubAccType_JP_GENERAL,
            self.JP_TOKUTEI: Trd_Common_pb2.TrdSubAccType_JP_TOKUTEI,
            self.JP_NISA_GENERAL: Trd_Common_pb2.TrdSubAccType_JP_NISA_GENERAL,
            self.JP_NISA_TSUMITATE: Trd_Common_pb2.TrdSubAccType_JP_NISA_TSUMITATE,
            self.JP_GENERAL_SHORT: Trd_Common_pb2.TrdSubAccType_JP_GENERAL_SHORT,
            self.JP_TOKUTEI_SHORT: Trd_Common_pb2.TrdSubAccType_JP_TOKUTEI_SHORT,
            self.JP_HONPO_GENERAL: Trd_Common_pb2.TrdSubAccType_JP_HONPO_GENERAL,
            self.JP_GAIKOKU_GENERAL: Trd_Common_pb2.TrdSubAccType_JP_GAIKOKU_GENERAL,
            self.JP_HONPO_TOKUTEI: Trd_Common_pb2.TrdSubAccType_JP_HONPO_TOKUTEI,
            self.JP_GAIKOKU_TOKUTEI: Trd_Common_pb2.TrdSubAccType_JP_GAIKOKU_TOKUTEI,
            self.JP_DERIVATIVE_LONG: Trd_Common_pb2.TrdSubAccType_JP_DERIVATIVE_LONG,
            self.JP_DERIVATIVE_SHORT: Trd_Common_pb2.TrdSubAccType_JP_DERIVATIVE_SHORT,
            self.JP_HONPO_DERIVATIVE_GENERAL: Trd_Common_pb2.TrdSubAccType_JP_HONPO_DERIVATIVE_GENERAL,
            self.JP_GAIKOKU_DERIVATIVE_GENERAL: Trd_Common_pb2.TrdSubAccType_JP_GAIKOKU_DERIVATIVE_GENERAL,
            self.JP_HONPO_DERIVATIVE_TOKUTEI: Trd_Common_pb2.TrdSubAccType_JP_HONPO_DERIVATIVE_TOKUTEI,
            self.JP_GAIKOKU_DERIVATIVE_TOKUTEI: Trd_Common_pb2.TrdSubAccType_JP_GAIKOKU_DERIVATIVE_TOKUTEI,
        }

class ExposureLevel(FtEnum):
    NONE = 'N/A'
    NORMAL = 'NORMAL'
    NEAR_LIMIT = 'NEAR_LIMIT'
    RESTRICTED = 'RESTRICTED'
    SAFE = 'SAFE'
    MODERATE = 'MODERATE'
    WARNING = 'WARNING'
    MARGIN_CALL = 'MARGIN_CALL'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.ExposureLevel_Unknown,
            self.NORMAL: Trd_Common_pb2.ExposureLevel_Normal,
            self.NEAR_LIMIT: Trd_Common_pb2.ExposureLevel_NearLimit,
            self.RESTRICTED: Trd_Common_pb2.ExposureLevel_Restricted,
            self.SAFE: Trd_Common_pb2.ExposureLevel_Safe,
            self.MODERATE: Trd_Common_pb2.ExposureLevel_Moderate,
            self.WARNING: Trd_Common_pb2.ExposureLevel_Warning,
            self.MARGIN_CALL: Trd_Common_pb2.ExposureLevel_MarginCall,
        }

class PositionType(FtEnum):
    NONE = 'N/A'
    COMBINED = 'COMBINED'
    LEG = 'LEG'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.PositionType_Unknown,
            self.COMBINED: Trd_Common_pb2.PositionType_Combined,
            self.LEG: Trd_Common_pb2.PositionType_Leg,
        }

class IndicatorLangType(object):
    """指标脚本语言类型，对应 Qot_Common.IndicatorLangType"""
    UNKNOWN = 0  # 不过滤
    MYLANG = 1   # 麦语言
    PYTHON = 2   # Python


class IndicatorSearchMode(object):
    """指标搜索模式，对应 Qot_Common.IndicatorSearchMode"""
    PARTIAL = 0  # 部分匹配（默认）
    EXACT = 1    # 完全匹配（同时返回 script 字段）


# 搜索资讯子类型
class NewsSubType(FtEnum):
    ALL    = "ALL"
    NEWS   = "NEWS"
    NOTICE = "NOTICE"
    RATING = "RATING"

    def load_dic(self):
        return {
            self.ALL:    Qot_GetSearchNews_pb2.NewsSubType_ALL,
            self.NEWS:   Qot_GetSearchNews_pb2.NewsSubType_NEWS,
            self.NOTICE: Qot_GetSearchNews_pb2.NewsSubType_NOTICE,
            self.RATING: Qot_GetSearchNews_pb2.NewsSubType_RATING,
        }

# 宏观数据国家/地区
class MacroRegion(FtEnum):
    UNKNOWN = 'N/A'
    HK = 'HK'
    US = 'US'
    JP = 'JP'
    SG = 'SG'
    AU = 'AU'
    CA = 'CA'
    MY = 'MY'
    CN = 'CN'

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetMacroIndicatorList_pb2.MacroRegion_Unknown,
            self.HK: Qot_GetMacroIndicatorList_pb2.MacroRegion_HK,
            self.US: Qot_GetMacroIndicatorList_pb2.MacroRegion_US,
            self.JP: Qot_GetMacroIndicatorList_pb2.MacroRegion_JP,
            self.SG: Qot_GetMacroIndicatorList_pb2.MacroRegion_SG,
            self.AU: Qot_GetMacroIndicatorList_pb2.MacroRegion_AU,
            self.CA: Qot_GetMacroIndicatorList_pb2.MacroRegion_CA,
            self.MY: Qot_GetMacroIndicatorList_pb2.MacroRegion_MY,
            self.CN: Qot_GetMacroIndicatorList_pb2.MacroRegion_CN,
        }


# 宏观数据单位类型
class MacroDataUnitType(FtEnum):
    UNKNOWN = 'N/A'
    PERCENT = 'PERCENT'
    VALUE = 'VALUE'
    INDEX = 'INDEX'

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetMacroIndicatorHistory_pb2.MacroDataUnitType_Unknown,
            self.PERCENT: Qot_GetMacroIndicatorHistory_pb2.MacroDataUnitType_Percent,
            self.VALUE: Qot_GetMacroIndicatorHistory_pb2.MacroDataUnitType_Value,
            self.INDEX: Qot_GetMacroIndicatorHistory_pb2.MacroDataUnitType_Index,
        }


# 盈利超预期类型
class BeatType(FtEnum):
    UNKNOWN = 'N/A'
    EPS = 'EPS'            # 每股收益
    REVENUE = 'REVENUE'    # 营收
    EBIT = 'EBIT'          # 息税前利润

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetEarningsBeatRank_pb2.BeatType_Unknown,
            self.EPS: Qot_GetEarningsBeatRank_pb2.BeatType_EPS,
            self.REVENUE: Qot_GetEarningsBeatRank_pb2.BeatType_REVENUE,
            self.EBIT: Qot_GetEarningsBeatRank_pb2.BeatType_EBIT,
        }


# 财报周期
class BeatTerm(FtEnum):
    LATEST = 'LATEST'                    # 最近一期 (默认)
    LATEST_QUARTER = 'LATEST_QUARTER'    # 最近一期季报
    LATEST_HALF = 'LATEST_HALF'          # 最近一期半年报
    LATEST_ANNUAL = 'LATEST_ANNUAL'      # 最近一期年报
    ALL = 'ALL'                          # 全部

    def load_dic(self):
        return {
            self.LATEST: Qot_GetEarningsBeatRank_pb2.BeatTerm_Latest,
            self.LATEST_QUARTER: Qot_GetEarningsBeatRank_pb2.BeatTerm_LatestQuarter,
            self.LATEST_HALF: Qot_GetEarningsBeatRank_pb2.BeatTerm_LatestHalf,
            self.LATEST_ANNUAL: Qot_GetEarningsBeatRank_pb2.BeatTerm_LatestAnnual,
            self.ALL: Qot_GetEarningsBeatRank_pb2.BeatTerm_All,
        }


# 财报发布时段
class PostPeriodType(FtEnum):
    REGULAR = 'REGULAR'                      # 当天(未识别出时段)
    BEFORE = 'BEFORE'                        # 盘前
    AFTER = 'AFTER'                          # 盘后
    INTRADAY_TRADING = 'INTRADAY_TRADING'    # 盘中

    def load_dic(self):
        return {
            self.REGULAR: Qot_GetEarningsBeatRank_pb2.PostPeriodType_Regular,
            self.BEFORE: Qot_GetEarningsBeatRank_pb2.PostPeriodType_Before,
            self.AFTER: Qot_GetEarningsBeatRank_pb2.PostPeriodType_After,
            self.INTRADAY_TRADING: Qot_GetEarningsBeatRank_pb2.PostPeriodType_IntradayTrading,
        }


# 盈利超预期筛选条件类型
class EarningsBeatIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    BEAT_RATIO = 'BEAT_RATIO'            # 超预期比率
    RELEASED_DATE = 'RELEASED_DATE'      # 发布时间(时间戳秒)
    MARKET_CAP = 'MARKET_CAP'            # 市值
    PRICE = 'PRICE'                      # 最新价
    PE_TTM = 'PE_TTM'                    # 市盈率TTM

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetEarningsBeatRank_pb2.IndicatorType_Unknown,
            self.BEAT_RATIO: Qot_GetEarningsBeatRank_pb2.IndicatorType_BeatRatio,
            self.RELEASED_DATE: Qot_GetEarningsBeatRank_pb2.IndicatorType_ReleasedDate,
            self.MARKET_CAP: Qot_GetEarningsBeatRank_pb2.IndicatorType_MarketCap,
            self.PRICE: Qot_GetEarningsBeatRank_pb2.IndicatorType_Price,
            self.PE_TTM: Qot_GetEarningsBeatRank_pb2.IndicatorType_PeTTM,
        }


# 盈利超预期排序字段 (固定降序)
class EarningsBeatSortField(FtEnum):
    UNKNOWN = 'N/A'
    BEAT_RATIO = 'BEAT_RATIO'            # 超预期比率
    EARNING_DAY_CHG = 'EARNING_DAY_CHG'  # 财报后首日涨幅
    RELEASED_DATE = 'RELEASED_DATE'      # 发布时间
    ACTUAL = 'ACTUAL'                    # 实际值
    ESTIMATE = 'ESTIMATE'                # 预测值
    YOY = 'YOY'                          # 去年同期
    YOY_GROWTH = 'YOY_GROWTH'            # 同比增长率
    PE_TTM = 'PE_TTM'                    # 市盈率TTM
    DIVIDENDS_TTM = 'DIVIDENDS_TTM'      # 股息率TTM
    PRICE = 'PRICE'                      # 价格
    CHANGE_RATE = 'CHANGE_RATE'          # 今日涨跌幅

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetEarningsBeatRank_pb2.SortField_Unknown,
            self.BEAT_RATIO: Qot_GetEarningsBeatRank_pb2.SortField_BeatRatio,
            self.EARNING_DAY_CHG: Qot_GetEarningsBeatRank_pb2.SortField_EarningDayChg,
            self.RELEASED_DATE: Qot_GetEarningsBeatRank_pb2.SortField_ReleasedDate,
            self.ACTUAL: Qot_GetEarningsBeatRank_pb2.SortField_Actual,
            self.ESTIMATE: Qot_GetEarningsBeatRank_pb2.SortField_Estimate,
            self.YOY: Qot_GetEarningsBeatRank_pb2.SortField_Yoy,
            self.YOY_GROWTH: Qot_GetEarningsBeatRank_pb2.SortField_YoyGrowth,
            self.PE_TTM: Qot_GetEarningsBeatRank_pb2.SortField_PeTTM,
            self.DIVIDENDS_TTM: Qot_GetEarningsBeatRank_pb2.SortField_DividendsTTM,
            self.PRICE: Qot_GetEarningsBeatRank_pb2.SortField_Price,
            self.CHANGE_RATE: Qot_GetEarningsBeatRank_pb2.SortField_ChangeRate,
        }


# 派息频率
class DistributionFrequency(FtEnum):
    UNKNOWN = 'N/A'
    ANNUAL = 'ANNUAL'              # 年派
    SEMI_ANNUAL = 'SEMI_ANNUAL'    # 半年派
    QUARTERLY = 'QUARTERLY'        # 季派
    MONTHLY = 'MONTHLY'            # 月派

    def load_dic(self):
        return {
            self.UNKNOWN: 0,
            self.ANNUAL: 1,
            self.SEMI_ANNUAL: 2,
            self.QUARTERLY: 3,
            self.MONTHLY: 4,
        }


# 股息排行类型
class DividendRankType(FtEnum):
    UNKNOWN = 'N/A'
    HIGH_YIELD = 'HIGH_YIELD'              # 高股息率
    DIVIDEND_GROWTH = 'DIVIDEND_GROWTH'    # 股息保持增长

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetDividendRank_pb2.DividendRankType_Unknown,
            self.HIGH_YIELD: Qot_GetDividendRank_pb2.DividendRankType_HighYield,
            self.DIVIDEND_GROWTH: Qot_GetDividendRank_pb2.DividendRankType_DividendGrowth,
        }


# 股息排行筛选条件类型
class DividendRankIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    DIVIDEND_YIELD_TTM = 'DIVIDEND_YIELD_TTM'            # 股息率TTM (%)
    AVG_DIVIDEND_YIELD_5Y = 'AVG_DIVIDEND_YIELD_5Y'      # 5年平均股息率 (%)
    DISTRIBUTION_FREQUENCY = 'DISTRIBUTION_FREQUENCY'    # 派息频率
    DIVIDEND_GROW_YEAR = 'DIVIDEND_GROW_YEAR'            # 股息连续增长年数
    DIVIDENDS_TTM = 'DIVIDENDS_TTM'                      # 股息TTM (金额)
    PAYOUT_RATIO_LFY = 'PAYOUT_RATIO_LFY'              # 股息支付率LFY (%)
    NEXT_PAYABLE_DATE = 'NEXT_PAYABLE_DATE'            # 下次派息日 (时间戳秒)
    PRICE = 'PRICE'                                      # 最新价
    MARKET_CAP = 'MARKET_CAP'                            # 市值

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetDividendRank_pb2.IndicatorType_Unknown,
            self.DIVIDEND_YIELD_TTM: Qot_GetDividendRank_pb2.IndicatorType_DividendYieldTTM,
            self.AVG_DIVIDEND_YIELD_5Y: Qot_GetDividendRank_pb2.IndicatorType_AvgDividendYield5Y,
            self.DISTRIBUTION_FREQUENCY: Qot_GetDividendRank_pb2.IndicatorType_DistributionFrequency,
            self.DIVIDEND_GROW_YEAR: Qot_GetDividendRank_pb2.IndicatorType_DividendGrowYear,
            self.DIVIDENDS_TTM: Qot_GetDividendRank_pb2.IndicatorType_DividendsTTM,
            self.PAYOUT_RATIO_LFY: Qot_GetDividendRank_pb2.IndicatorType_PayoutRatioLFY,
            self.NEXT_PAYABLE_DATE: Qot_GetDividendRank_pb2.IndicatorType_NextPayableDate,
            self.PRICE: Qot_GetDividendRank_pb2.IndicatorType_Price,
            self.MARKET_CAP: Qot_GetDividendRank_pb2.IndicatorType_MarketCap,
        }


# 股息排行排序字段 (固定降序)
class DividendRankSortField(FtEnum):
    UNKNOWN = 'N/A'
    DIVIDEND_YIELD_TTM = 'DIVIDEND_YIELD_TTM'            # 股息率TTM
    AVG_DIVIDEND_YIELD_5Y = 'AVG_DIVIDEND_YIELD_5Y'      # 5年平均股息率
    DISTRIBUTION_FREQUENCY = 'DISTRIBUTION_FREQUENCY'    # 派息频率
    DIVIDEND_GROW_YEAR = 'DIVIDEND_GROW_YEAR'            # 股息连续增长年数
    DIVIDENDS_TTM = 'DIVIDENDS_TTM'                      # 股息TTM
    PAYOUT_RATIO_LFY = 'PAYOUT_RATIO_LFY'              # 股息支付率LFY
    PRICE = 'PRICE'                                      # 价格
    MARKET_CAP = 'MARKET_CAP'                            # 市值
    CHANGE_RATE = 'CHANGE_RATE'                          # 今日涨跌幅
    CHANGE_AMOUNT = 'CHANGE_AMOUNT'                      # 今日涨跌额

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetDividendRank_pb2.SortField_Unknown,
            self.DIVIDEND_YIELD_TTM: Qot_GetDividendRank_pb2.SortField_DividendYieldTTM,
            self.AVG_DIVIDEND_YIELD_5Y: Qot_GetDividendRank_pb2.SortField_AvgDividendYield5Y,
            self.DISTRIBUTION_FREQUENCY: Qot_GetDividendRank_pb2.SortField_DistributionFrequency,
            self.DIVIDEND_GROW_YEAR: Qot_GetDividendRank_pb2.SortField_DividendGrowYear,
            self.DIVIDENDS_TTM: Qot_GetDividendRank_pb2.SortField_DividendsTTM,
            self.PAYOUT_RATIO_LFY: Qot_GetDividendRank_pb2.SortField_PayoutRatioLFY,
            self.PRICE: Qot_GetDividendRank_pb2.SortField_Price,
            self.MARKET_CAP: Qot_GetDividendRank_pb2.SortField_MarketCap,
            self.CHANGE_RATE: Qot_GetDividendRank_pb2.SortField_ChangeRate,
            self.CHANGE_AMOUNT: Qot_GetDividendRank_pb2.SortField_ChangeAmount,
        }


# 经济事件日历 - 事件重要性
class EconomicImportance(FtEnum):
    ALL = 'ALL'          # 全部(默认)
    LOW = 'LOW'          # 一星(低)
    MEDIUM = 'MEDIUM'    # 二星(中)
    HIGH = 'HIGH'        # 三星(高)

    def load_dic(self):
        return {
            self.ALL: Qot_GetEconomicCalendar_pb2.Importance_All,
            self.LOW: Qot_GetEconomicCalendar_pb2.Importance_Low,
            self.MEDIUM: Qot_GetEconomicCalendar_pb2.Importance_Medium,
            self.HIGH: Qot_GetEconomicCalendar_pb2.Importance_High,
        }


# ===== 特色榜单相关枚举 =====

# 盘前/盘后/夜盘/领涨 排序方向
class RankSortDir(FtEnum):
    DESCENDING = 'DESCENDING'    # 降序(领涨,默认)
    ASCENDING = 'ASCENDING'      # 升序(领跌)

    def load_dic(self):
        return {
            self.DESCENDING: Qot_GetUSPreMarketRank_pb2.SortDir_Descending,
            self.ASCENDING: Qot_GetUSPreMarketRank_pb2.SortDir_Ascending,
        }


# 盘前/盘后/夜盘/领涨榜 筛选条件类型 (共用)
class SimpleRankIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    PRICE = 'PRICE'              # 价格筛选(枚举)
    MARKET_CAP = 'MARKET_CAP'    # 市值区间
    PE = 'PE'                    # 市盈率区间

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetUSPreMarketRank_pb2.IndicatorType_Unknown,
            self.PRICE: Qot_GetUSPreMarketRank_pb2.IndicatorType_Price,
            self.MARKET_CAP: Qot_GetUSPreMarketRank_pb2.IndicatorType_MarketCap,
            self.PE: Qot_GetUSPreMarketRank_pb2.IndicatorType_PE,
        }


# 价格筛选枚举 (盘前/盘后/夜盘/领涨榜 Price类型使用)
class PriceFilter(FtEnum):
    ALL = 'ALL'                              # 所有(默认)
    LESS_THAN_1 = 'LESS_THAN_1'              # 小于1
    BETWEEN_1_AND_10 = 'BETWEEN_1_AND_10'    # 1~10之间
    BETWEEN_10_AND_100 = 'BETWEEN_10_AND_100'  # 10~100之间
    GREATER_THAN_100 = 'GREATER_THAN_100'    # 大于100
    NEAR_52_WEEK_HIGH = 'NEAR_52_WEEK_HIGH'  # 接近52周最高
    NEAR_52_WEEK_LOW = 'NEAR_52_WEEK_LOW'    # 接近52周最低

    def load_dic(self):
        return {
            self.ALL: Qot_GetUSPreMarketRank_pb2.PriceFilter_All,
            self.LESS_THAN_1: Qot_GetUSPreMarketRank_pb2.PriceFilter_LessThan1,
            self.BETWEEN_1_AND_10: Qot_GetUSPreMarketRank_pb2.PriceFilter_Between1And10,
            self.BETWEEN_10_AND_100: Qot_GetUSPreMarketRank_pb2.PriceFilter_Between10And100,
            self.GREATER_THAN_100: Qot_GetUSPreMarketRank_pb2.PriceFilter_GreaterThan100,
            self.NEAR_52_WEEK_HIGH: Qot_GetUSPreMarketRank_pb2.PriceFilter_Near52WeekHigh,
            self.NEAR_52_WEEK_LOW: Qot_GetUSPreMarketRank_pb2.PriceFilter_Near52WeekLow,
        }


# 热议榜排序字段
class HotListSortField(FtEnum):
    UNKNOWN = 'N/A'
    TRADE_HEAT = 'TRADE_HEAT'        # 交易热度
    SEARCH_HEAT = 'SEARCH_HEAT'      # 搜索热度
    NEWS_HEAT = 'NEWS_HEAT'          # 资讯热度
    AVERAGE_HEAT = 'AVERAGE_HEAT'    # 综合热度(默认)

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetHotList_pb2.HotListSortField_Unknown,
            self.TRADE_HEAT: Qot_GetHotList_pb2.HotListSortField_TradeHeat,
            self.SEARCH_HEAT: Qot_GetHotList_pb2.HotListSortField_SearchHeat,
            self.NEWS_HEAT: Qot_GetHotList_pb2.HotListSortField_NewsHeat,
            self.AVERAGE_HEAT: Qot_GetHotList_pb2.HotListSortField_AverageHeat,
        }


# 热议榜筛选条件类型
class HotListIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    MARKET_CAP = 'MARKET_CAP'    # 市值区间

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetHotList_pb2.IndicatorType_Unknown,
            self.MARKET_CAP: Qot_GetHotList_pb2.IndicatorType_MarketCap,
        }


# 卖空异动榜排序字段
class ShortSellingSortField(FtEnum):
    UNKNOWN = 'N/A'
    SHORT_NUMBER_CHANGE = 'SHORT_NUMBER_CHANGE'          # 卖空变化量(默认)
    SHORT_RATIO_CHANGE = 'SHORT_RATIO_CHANGE'            # 卖空变化比例
    SHORT_NUMBER = 'SHORT_NUMBER'                        # 卖空数量
    SHORT_RATIO = 'SHORT_RATIO'                          # 卖空比例
    VOLUME = 'VOLUME'                                    # 成交量
    POSITION_VOLUME = 'POSITION_VOLUME'                  # 空头持仓数量
    POSITION_RATIO = 'POSITION_RATIO'                    # 空头持仓比例
    DAYS_TO_COVER = 'DAYS_TO_COVER'                      # 回补天数
    WEEK_AVG_VOLUME = 'WEEK_AVG_VOLUME'                  # 近一周日均成交量
    WEEK_AVG_SHORT_NUMBER = 'WEEK_AVG_SHORT_NUMBER'      # 近一周日均卖空数量
    WEEK_AVG_SHORT_RATIO = 'WEEK_AVG_SHORT_RATIO'        # 近一周日均卖空比例
    MONTH_AVG_VOLUME = 'MONTH_AVG_VOLUME'                # 近一月日均成交量
    MONTH_AVG_SHORT_NUMBER = 'MONTH_AVG_SHORT_NUMBER'    # 近一月日均卖空数量
    MONTH_AVG_SHORT_RATIO = 'MONTH_AVG_SHORT_RATIO'      # 近一月日均卖空比例

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetShortSellingRank_pb2.ShortSellingSortField_Unknown,
            self.SHORT_NUMBER_CHANGE: Qot_GetShortSellingRank_pb2.ShortSellingSortField_ShortNumberChange,
            self.SHORT_RATIO_CHANGE: Qot_GetShortSellingRank_pb2.ShortSellingSortField_ShortRatioChange,
            self.SHORT_NUMBER: Qot_GetShortSellingRank_pb2.ShortSellingSortField_ShortNumber,
            self.SHORT_RATIO: Qot_GetShortSellingRank_pb2.ShortSellingSortField_ShortRatio,
            self.VOLUME: Qot_GetShortSellingRank_pb2.ShortSellingSortField_Volume,
            self.POSITION_VOLUME: Qot_GetShortSellingRank_pb2.ShortSellingSortField_PositionVolume,
            self.POSITION_RATIO: Qot_GetShortSellingRank_pb2.ShortSellingSortField_PositionRatio,
            self.DAYS_TO_COVER: Qot_GetShortSellingRank_pb2.ShortSellingSortField_DaysToCover,
            self.WEEK_AVG_VOLUME: Qot_GetShortSellingRank_pb2.ShortSellingSortField_WeekAvgVolume,
            self.WEEK_AVG_SHORT_NUMBER: Qot_GetShortSellingRank_pb2.ShortSellingSortField_WeekAvgShortNumber,
            self.WEEK_AVG_SHORT_RATIO: Qot_GetShortSellingRank_pb2.ShortSellingSortField_WeekAvgShortRatio,
            self.MONTH_AVG_VOLUME: Qot_GetShortSellingRank_pb2.ShortSellingSortField_MonthAvgVolume,
            self.MONTH_AVG_SHORT_NUMBER: Qot_GetShortSellingRank_pb2.ShortSellingSortField_MonthAvgShortNumber,
            self.MONTH_AVG_SHORT_RATIO: Qot_GetShortSellingRank_pb2.ShortSellingSortField_MonthAvgShortRatio,
        }


# 区间涨跌幅排序周期
class RankPeriodType(FtEnum):
    UNKNOWN = 'N/A'
    FIVE_MIN = '5MIN'        # 5分钟(默认)
    ONE_DAY = '1DAY'         # 1日
    FIVE_DAY = '5DAY'        # 5日
    TWENTY_DAY = '20DAY'     # 20日
    SIXTY_DAY = '60DAY'      # 60日
    ONE_TWENTY_DAY = '120DAY'   # 120日
    TWO_FIFTY_DAY = '250DAY'    # 250日
    YTD = 'YTD'              # 年初至今

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetPeriodChangeRank_pb2.PeriodType_Unknown,
            self.FIVE_MIN: Qot_GetPeriodChangeRank_pb2.PeriodType_5Min,
            self.ONE_DAY: Qot_GetPeriodChangeRank_pb2.PeriodType_1Day,
            self.FIVE_DAY: Qot_GetPeriodChangeRank_pb2.PeriodType_5Day,
            self.TWENTY_DAY: Qot_GetPeriodChangeRank_pb2.PeriodType_20Day,
            self.SIXTY_DAY: Qot_GetPeriodChangeRank_pb2.PeriodType_60Day,
            self.ONE_TWENTY_DAY: Qot_GetPeriodChangeRank_pb2.PeriodType_120Day,
            self.TWO_FIFTY_DAY: Qot_GetPeriodChangeRank_pb2.PeriodType_250Day,
            self.YTD: Qot_GetPeriodChangeRank_pb2.PeriodType_YTD,
        }


# 区间涨跌幅筛选条件类型
class PeriodChangeIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    PRICE = 'PRICE'                      # 最新价区间
    MARKET_CAP = 'MARKET_CAP'            # 市值区间
    CHANGE_RATIO = 'CHANGE_RATIO'        # 涨跌幅区间(按所选周期)
    VOLUME = 'VOLUME'                    # 成交量区间
    TURNOVER = 'TURNOVER'                # 成交额区间
    PE = 'PE'                            # 市盈率TTM区间
    PB = 'PB'                            # 市净率区间
    TURNOVER_RATIO = 'TURNOVER_RATIO'    # 换手率区间
    VOLUME_RATIO = 'VOLUME_RATIO'        # 量比区间
    AMPLITUDE = 'AMPLITUDE'              # 振幅区间

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetPeriodChangeRank_pb2.IndicatorType_Unknown,
            self.PRICE: Qot_GetPeriodChangeRank_pb2.IndicatorType_Price,
            self.MARKET_CAP: Qot_GetPeriodChangeRank_pb2.IndicatorType_MarketCap,
            self.CHANGE_RATIO: Qot_GetPeriodChangeRank_pb2.IndicatorType_ChangeRatio,
            self.VOLUME: Qot_GetPeriodChangeRank_pb2.IndicatorType_Volume,
            self.TURNOVER: Qot_GetPeriodChangeRank_pb2.IndicatorType_Turnover,
            self.PE: Qot_GetPeriodChangeRank_pb2.IndicatorType_PE,
            self.PB: Qot_GetPeriodChangeRank_pb2.IndicatorType_PB,
            self.TURNOVER_RATIO: Qot_GetPeriodChangeRank_pb2.IndicatorType_TurnoverRatio,
            self.VOLUME_RATIO: Qot_GetPeriodChangeRank_pb2.IndicatorType_VolumeRatio,
            self.AMPLITUDE: Qot_GetPeriodChangeRank_pb2.IndicatorType_Amplitude,
        }


# 破净高股息国央企排序字段
class HighDividendSOESortField(FtEnum):
    UNKNOWN = 'N/A'
    DIVIDEND_YIELD_TTM = 'DIVIDEND_YIELD_TTM'    # 股息率TTM
    PB = 'PB'                                    # 市净率
    PE_TTM = 'PE_TTM'                            # 市盈率TTM
    PRICE = 'PRICE'                              # 最新价
    CHANGE_RATIO = 'CHANGE_RATIO'                # 今日涨跌幅
    MARKET_CAP = 'MARKET_CAP'                    # 市值

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetHighDividendSOERank_pb2.SortField_Unknown,
            self.DIVIDEND_YIELD_TTM: Qot_GetHighDividendSOERank_pb2.SortField_DividendYieldTTM,
            self.PB: Qot_GetHighDividendSOERank_pb2.SortField_PB,
            self.PE_TTM: Qot_GetHighDividendSOERank_pb2.SortField_PeTTM,
            self.PRICE: Qot_GetHighDividendSOERank_pb2.SortField_Price,
            self.CHANGE_RATIO: Qot_GetHighDividendSOERank_pb2.SortField_ChangeRatio,
            self.MARKET_CAP: Qot_GetHighDividendSOERank_pb2.SortField_MarketCap,
        }


# 破净高股息国央企筛选条件类型
class HighDividendSOEIndicatorType(FtEnum):
    UNKNOWN = 'N/A'
    PRICE = 'PRICE'                              # 价格区间
    MARKET_CAP = 'MARKET_CAP'                    # 市值区间
    PE = 'PE'                                    # 市盈率TTM区间
    DIVIDEND_YIELD_TTM = 'DIVIDEND_YIELD_TTM'    # 股息率TTM区间
    CHANGE_RATIO = 'CHANGE_RATIO'                # 涨跌幅区间

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetHighDividendSOERank_pb2.IndicatorType_Unknown,
            self.PRICE: Qot_GetHighDividendSOERank_pb2.IndicatorType_Price,
            self.MARKET_CAP: Qot_GetHighDividendSOERank_pb2.IndicatorType_MarketCap,
            self.PE: Qot_GetHighDividendSOERank_pb2.IndicatorType_PE,
            self.DIVIDEND_YIELD_TTM: Qot_GetHighDividendSOERank_pb2.IndicatorType_DividendYieldTTM,
            self.CHANGE_RATIO: Qot_GetHighDividendSOERank_pb2.IndicatorType_ChangeRatio,
        }


class InstitutionListSortField(FtEnum):
    UNKNOWN = 'N/A'
    POSITION_VALUE = 'POSITION_VALUE'                  # 持仓市值(默认)
    POSITION_VALUE_CHANGE = 'POSITION_VALUE_CHANGE'    # 增减仓
    POSITION_COUNT = 'POSITION_COUNT'                  # 持仓股数
    POSITION_COUNT_CHANGE = 'POSITION_COUNT_CHANGE'    # 持仓股数变化

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetInstitutionList_pb2.SortField_Unknown,
            self.POSITION_VALUE: Qot_GetInstitutionList_pb2.SortField_PositionValue,
            self.POSITION_VALUE_CHANGE: Qot_GetInstitutionList_pb2.SortField_PositionValueChange,
            self.POSITION_COUNT: Qot_GetInstitutionList_pb2.SortField_PositionCount,
            self.POSITION_COUNT_CHANGE: Qot_GetInstitutionList_pb2.SortField_PositionCountChange,
        }


class InstitutionHoldingChangeType(FtEnum):
    UNKNOWN = 'N/A'
    NEW = 'NEW'                  # 建仓
    SOLD_OUT = 'SOLD_OUT'        # 清仓
    INCREASE = 'INCREASE'        # 增仓
    DECREASE = 'DECREASE'        # 减仓

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetInstitutionHoldingChange_pb2.HoldingChangeType_Unknown,
            self.NEW: Qot_GetInstitutionHoldingChange_pb2.HoldingChangeType_New,
            self.SOLD_OUT: Qot_GetInstitutionHoldingChange_pb2.HoldingChangeType_SoldOut,
            self.INCREASE: Qot_GetInstitutionHoldingChange_pb2.HoldingChangeType_Increase,
            self.DECREASE: Qot_GetInstitutionHoldingChange_pb2.HoldingChangeType_Decrease,
        }


class InstitutionHoldingChangeSortField(FtEnum):
    UNKNOWN = 'N/A'
    CHANGE_PCT = 'CHANGE_PCT'            # 变动比例(默认)
    CHANGE_SHARES = 'CHANGE_SHARES'      # 变动股数
    HOLDING_DATE = 'HOLDING_DATE'        # 持仓时间

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetInstitutionHoldingChange_pb2.SortField_Unknown,
            self.CHANGE_PCT: Qot_GetInstitutionHoldingChange_pb2.SortField_ChangePct,
            self.CHANGE_SHARES: Qot_GetInstitutionHoldingChange_pb2.SortField_ChangeShares,
            self.HOLDING_DATE: Qot_GetInstitutionHoldingChange_pb2.SortField_HoldingDate,
        }


class InstitutionHoldingListSortField(FtEnum):
    UNKNOWN = 'N/A'
    HOLDING_VALUE = 'HOLDING_VALUE'          # 持仓市值(默认)
    HOLDING_PCT = 'HOLDING_PCT'              # 持股比例(占股票总市值)
    LAST_HOLDING_PCT = 'LAST_HOLDING_PCT'    # 上期持股比例
    CHANGE_SHARES = 'CHANGE_SHARES'          # 变动股数
    CHANGE_PCT = 'CHANGE_PCT'                # 变动比例
    PORTFOLIO_PCT = 'PORTFOLIO_PCT'          # 占机构总仓位比例
    INDUSTRY = 'INDUSTRY'                    # 行业
    HOLDING_DATE = 'HOLDING_DATE'            # 持仓时间

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetInstitutionHoldingList_pb2.SortField_Unknown,
            self.HOLDING_VALUE: Qot_GetInstitutionHoldingList_pb2.SortField_HoldingValue,
            self.HOLDING_PCT: Qot_GetInstitutionHoldingList_pb2.SortField_HoldingPct,
            self.LAST_HOLDING_PCT: Qot_GetInstitutionHoldingList_pb2.SortField_LastHoldingPct,
            self.CHANGE_SHARES: Qot_GetInstitutionHoldingList_pb2.SortField_ChangeShares,
            self.CHANGE_PCT: Qot_GetInstitutionHoldingList_pb2.SortField_ChangePct,
            self.PORTFOLIO_PCT: Qot_GetInstitutionHoldingList_pb2.SortField_PortfolioPct,
            self.INDUSTRY: Qot_GetInstitutionHoldingList_pb2.SortField_Industry,
            self.HOLDING_DATE: Qot_GetInstitutionHoldingList_pb2.SortField_HoldingDate,
        }


class ArkHoldingType(FtEnum):
    POSITION = 'POSITION'        # 持仓
    INCREASE = 'INCREASE'        # 增持
    DECREASE = 'DECREASE'        # 减持
    NEW = 'NEW'                  # 建仓
    SOLD_OUT = 'SOLD_OUT'        # 清仓

    def load_dic(self):
        return {
            self.POSITION: Qot_GetArkFundHolding_pb2.ArkHoldingType_Position,
            self.INCREASE: Qot_GetArkFundHolding_pb2.ArkHoldingType_Increase,
            self.DECREASE: Qot_GetArkFundHolding_pb2.ArkHoldingType_Decrease,
            self.NEW: Qot_GetArkFundHolding_pb2.ArkHoldingType_New,
            self.SOLD_OUT: Qot_GetArkFundHolding_pb2.ArkHoldingType_SoldOut,
        }


class ArkCycleType(FtEnum):
    ONE_DAY = 'ONE_DAY'          # 近1天
    FIVE_DAY = 'FIVE_DAY'        # 近5天
    TEN_DAY = 'TEN_DAY'          # 近10天
    THIRTY_DAY = 'THIRTY_DAY'    # 近30天
    SIXTY_DAY = 'SIXTY_DAY'      # 近60天

    def load_dic(self):
        return {
            self.ONE_DAY: Qot_GetArkFundHolding_pb2.CycleType_1Day,
            self.FIVE_DAY: Qot_GetArkFundHolding_pb2.CycleType_5Day,
            self.TEN_DAY: Qot_GetArkFundHolding_pb2.CycleType_10Day,
            self.THIRTY_DAY: Qot_GetArkFundHolding_pb2.CycleType_30Day,
            self.SIXTY_DAY: Qot_GetArkFundHolding_pb2.CycleType_60Day,
        }


class ArkDynamicType(FtEnum):
    UNKNOWN = 'N/A'
    CONSECUTIVE_SAME_DIRECTION = 'CONSECUTIVE_SAME_DIRECTION'  # 连续同向交易
    RECENT_TRANSACTION = 'RECENT_TRANSACTION'                  # 近期交易
    LAST_TRANSACTION = 'LAST_TRANSACTION'                      # 最近一笔
    NO_DYNAMIC = 'NO_DYNAMIC'                                  # 无动态

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetArkStockDynamic_pb2.DynamicType_Unknown,
            self.CONSECUTIVE_SAME_DIRECTION: Qot_GetArkStockDynamic_pb2.DynamicType_ConsecutiveSameDirection,
            self.RECENT_TRANSACTION: Qot_GetArkStockDynamic_pb2.DynamicType_RecentTransaction,
            self.LAST_TRANSACTION: Qot_GetArkStockDynamic_pb2.DynamicType_LastTransaction,
            self.NO_DYNAMIC: Qot_GetArkStockDynamic_pb2.DynamicType_NoDynamic,
        }


class ArkFundHoldingSortField(FtEnum):
    SHARES = 'SHARES'                    # 持仓数量(默认)
    WEIGHT_CHANGE = 'WEIGHT_CHANGE'      # 占比变动
    SHARES_CHANGE = 'SHARES_CHANGE'      # 持仓变动
    MARKET_VALUE = 'MARKET_VALUE'        # 市值
    WEIGHT = 'WEIGHT'                    # ETF占比

    def load_dic(self):
        return {
            self.SHARES: Qot_GetArkFundHolding_pb2.SortField_Shares,
            self.WEIGHT_CHANGE: Qot_GetArkFundHolding_pb2.SortField_WeightChange,
            self.SHARES_CHANGE: Qot_GetArkFundHolding_pb2.SortField_SharesChange,
            self.MARKET_VALUE: Qot_GetArkFundHolding_pb2.SortField_MarketValue,
            self.WEIGHT: Qot_GetArkFundHolding_pb2.SortField_Weight,
        }


class ArkActiveTransactionHoldingType(FtEnum):
    INCREASE = 'INCREASE'        # 增持(默认)
    DECREASE = 'DECREASE'        # 减持
    NEW = 'NEW'                  # 建仓
    SOLD_OUT = 'SOLD_OUT'        # 清仓

    def load_dic(self):
        return {
            self.INCREASE: Qot_GetArkActiveTransaction_pb2.HoldingType_Increase,
            self.DECREASE: Qot_GetArkActiveTransaction_pb2.HoldingType_Decrease,
            self.NEW: Qot_GetArkActiveTransaction_pb2.HoldingType_New,
            self.SOLD_OUT: Qot_GetArkActiveTransaction_pb2.HoldingType_SoldOut,
        }


class ArkActiveTransactionSortField(FtEnum):
    UNKNOWN = 'N/A'
    CHANGE_AMOUNT = 'CHANGE_AMOUNT'      # 变动金额(默认)
    CHANGE_SHARES = 'CHANGE_SHARES'      # 变动股数

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetArkActiveTransaction_pb2.SortField_Unknown,
            self.CHANGE_AMOUNT: Qot_GetArkActiveTransaction_pb2.SortField_ChangeAmount,
            self.CHANGE_SHARES: Qot_GetArkActiveTransaction_pb2.SortField_ChangeShares,
        }


class RatingChangeType(FtEnum):
    UNKNOWN = 'N/A'
    UPGRADE = 'UPGRADE'             # 评级上调
    DOWNGRADE = 'DOWNGRADE'         # 评级下调
    NEW_RATING = 'NEW_RATING'       # 首次评级

    def load_dic(self):
        return {
            self.UNKNOWN: 0,
            self.UPGRADE: Qot_GetRatingChange_pb2.RatingChangeType_Upgrade,
            self.DOWNGRADE: Qot_GetRatingChange_pb2.RatingChangeType_Downgrade,
            self.NEW_RATING: Qot_GetRatingChange_pb2.RatingChangeType_NewRating,
        }


class RatingLevel(FtEnum):
    UNKNOWN = 'N/A'
    SELL = 'SELL'       # 卖出
    HOLD = 'HOLD'       # 持有
    BUY = 'BUY'         # 买入

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetRatingChange_pb2.RatingLevel_Unknown,
            self.SELL: Qot_GetRatingChange_pb2.RatingLevel_Sell,
            self.HOLD: Qot_GetRatingChange_pb2.RatingLevel_Hold,
            self.BUY: Qot_GetRatingChange_pb2.RatingLevel_Buy,
        }


class IndustrialChainType(FtEnum):
    UNKNOWN = 'N/A'
    CHAIN = 'CHAIN'             # 串联型
    PARALLEL = 'PARALLEL'       # 并列型
    UP_MID_DOWN = 'UP_MID_DOWN' # 上中下游型

    def load_dic(self):
        return {
            self.UNKNOWN: 0,
            self.CHAIN: Qot_GetIndustrialChainList_pb2.IndustrialChainType_Chain,
            self.PARALLEL: Qot_GetIndustrialChainList_pb2.IndustrialChainType_Parallel,
            self.UP_MID_DOWN: Qot_GetIndustrialChainList_pb2.IndustrialChainType_UpMidDown,
        }


class PlateStockSortField(FtEnum):
    UNKNOWN = 'N/A'
    CODE = 'CODE'                   # 代码
    CHANGE_RATE = 'CHANGE_RATE'     # 涨跌幅
    TURNOVER = 'TURNOVER'           # 成交额
    VOLUME = 'VOLUME'               # 成交量
    MARKET_VAL = 'MARKET_VAL'       # 市值(默认)

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetIndustrialPlateStock_pb2.SortField_Code,
            self.CODE: Qot_GetIndustrialPlateStock_pb2.SortField_Code,
            self.CHANGE_RATE: Qot_GetIndustrialPlateStock_pb2.SortField_ChangeRate,
            self.TURNOVER: Qot_GetIndustrialPlateStock_pb2.SortField_Turnover,
            self.VOLUME: Qot_GetIndustrialPlateStock_pb2.SortField_Volume,
            self.MARKET_VAL: Qot_GetIndustrialPlateStock_pb2.SortField_MarketVal,
        }


class HeatMapSortField(FtEnum):
    UNKNOWN = 'N/A'
    CHANGE_RATE = 'CHANGE_RATE'     # 涨跌幅
    MARKET_VAL = 'MARKET_VAL'       # 市值
    TURNOVER = 'TURNOVER'           # 成交额
    HOT = 'HOT'                     # 热度

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetHeatMapData_pb2.SortField_Unknown,
            self.CHANGE_RATE: Qot_GetHeatMapData_pb2.SortField_ChangeRate,
            self.MARKET_VAL: Qot_GetHeatMapData_pb2.SortField_MarketVal,
            self.TURNOVER: Qot_GetHeatMapData_pb2.SortField_Turnover,
            self.HOT: Qot_GetHeatMapData_pb2.SortField_Hot,
        }


# 热力图板块类型
class HeatMapPlateType(FtEnum):
    INDUSTRY = 'INDUSTRY'     # 行业板块(默认)
    CONCEPT = 'CONCEPT'       # 概念板块
    THEME = 'THEME'           # 主题板块

    def load_dic(self):
        return {
            self.INDUSTRY: Qot_GetHeatMapData_pb2.HeatMapPlateType_Industry,
            self.CONCEPT: Qot_GetHeatMapData_pb2.HeatMapPlateType_Concept,
            self.THEME: Qot_GetHeatMapData_pb2.HeatMapPlateType_Theme,
        }


class RiseFallDistributionType(FtEnum):
    UNKNOWN = 'N/A'
    RISE_LIMIT = 'RISE_LIMIT'               # 涨停(A股)
    POSITIVE_INFINITY = 'POSITIVE_INFINITY'   # (7%, +∞)
    NORMAL_RANGE = 'NORMAL_RANGE'             # 正常区间
    NEGATIVE_INFINITY = 'NEGATIVE_INFINITY'   # (-∞, -7%)
    FALL_LIMIT = 'FALL_LIMIT'               # 跌停(A股)

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_GetRiseFallDistribution_pb2.DistributionType_Unknown,
            self.RISE_LIMIT: Qot_GetRiseFallDistribution_pb2.DistributionType_RiseLimit,
            self.POSITIVE_INFINITY: Qot_GetRiseFallDistribution_pb2.DistributionType_PositiveInfinity,
            self.NORMAL_RANGE: Qot_GetRiseFallDistribution_pb2.DistributionType_NormalRange,
            self.NEGATIVE_INFINITY: Qot_GetRiseFallDistribution_pb2.DistributionType_NegativeInfinity,
            self.FALL_LIMIT: Qot_GetRiseFallDistribution_pb2.DistributionType_FallLimit,
        }


class ECStatus(FtEnum):
    """事件合约状态"""
    INITIALIZED = "INITIALIZED"
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    HALTED = "HALTED"
    SETTLED = "SETTLED"
    CANCELED = "CANCELED"
    DETERMINATION_PENDING = "DETERMINATION_PENDING"
    DETERMINED = "DETERMINED"
    FINALIZED = "FINALIZED"
    EVENT_ABNORMAL = "EVENT_ABNORMAL"
    EVENT_INITIALIZED = "EVENT_INITIALIZED"
    EVENT_ACTIVE = "EVENT_ACTIVE"
    EVENT_CLOSED = "EVENT_CLOSED"
    EVENT_SETTLED = "EVENT_SETTLED"
    EVENT_CANCELED = "EVENT_CANCELED"
    EVENT_FINALIZED = "EVENT_FINALIZED"

    def load_dic(self):
        return {
            self.INITIALIZED: Qot_Common_pb2.EC_Status_Initialized,
            self.INACTIVE: Qot_Common_pb2.EC_Status_Inactive,
            self.ACTIVE: Qot_Common_pb2.EC_Status_Active,
            self.CLOSED: Qot_Common_pb2.EC_Status_Closed,
            self.HALTED: Qot_Common_pb2.EC_Status_Halted,
            self.SETTLED: Qot_Common_pb2.EC_Status_Settled,
            self.CANCELED: Qot_Common_pb2.EC_Status_Canceled,
            self.DETERMINATION_PENDING: Qot_Common_pb2.EC_Status_DeterminationPending,
            self.DETERMINED: Qot_Common_pb2.EC_Status_Determined,
            self.FINALIZED: Qot_Common_pb2.EC_Status_Finalized,
            self.EVENT_ABNORMAL: Qot_Common_pb2.EC_Status_EventAbnormal,
            self.EVENT_INITIALIZED: Qot_Common_pb2.EC_Status_EventInitialized,
            self.EVENT_ACTIVE: Qot_Common_pb2.EC_Status_EventActive,
            self.EVENT_CLOSED: Qot_Common_pb2.EC_Status_EventClosed,
            self.EVENT_SETTLED: Qot_Common_pb2.EC_Status_EventSettled,
            self.EVENT_CANCELED: Qot_Common_pb2.EC_Status_EventCanceled,
            self.EVENT_FINALIZED: Qot_Common_pb2.EC_Status_EventFinalized,
        }


class ECContractType(FtEnum):
    """事件合约类型"""
    NONE = "N/A"
    BINARY = "BINARY"
    SCALAR = "SCALAR"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.EC_ContractType_None,
            self.BINARY: Qot_Common_pb2.EC_ContractType_Binary,
            self.SCALAR: Qot_Common_pb2.EC_ContractType_Scalar,
        }


class ECFrequency(FtEnum):
    """事件合约频率"""
    UNKNOWN = "N/A"
    ANNUAL = "ANNUAL"
    MONTHLY = "MONTHLY"
    WEEKLY = "WEEKLY"
    DAILY = "DAILY"
    HOURLY = "HOURLY"
    CUSTOM = "CUSTOM"
    ONE_OFF = "ONE_OFF"

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_Common_pb2.EC_Frequency_Unknown,
            self.ANNUAL: Qot_Common_pb2.EC_Frequency_Annual,
            self.MONTHLY: Qot_Common_pb2.EC_Frequency_Monthly,
            self.WEEKLY: Qot_Common_pb2.EC_Frequency_Weekly,
            self.DAILY: Qot_Common_pb2.EC_Frequency_Daily,
            self.HOURLY: Qot_Common_pb2.EC_Frequency_Hourly,
            self.CUSTOM: Qot_Common_pb2.EC_Frequency_Custom,
            self.ONE_OFF: Qot_Common_pb2.EC_Frequency_OneOff,
        }


class ECMilestoneType(FtEnum):
    """事件合约里程碑类型"""
    UNKNOWN = "N/A"
    FOOTBALL_GAME = "FOOTBALL_GAME"
    BASKETBALL_GAME = "BASKETBALL_GAME"
    SOCCER_TOURNAMENT_MULTI_LEG = "SOCCER_TOURNAMENT_MULTI_LEG"
    BASEBALL_TOURNAMENT = "BASEBALL_TOURNAMENT"
    BASEBALL_GAME = "BASEBALL_GAME"

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_Common_pb2.EC_MilestoneType_Unknown,
            self.FOOTBALL_GAME: Qot_Common_pb2.EC_MilestoneType_FootballGame,
            self.BASKETBALL_GAME: Qot_Common_pb2.EC_MilestoneType_BasketballGame,
            self.SOCCER_TOURNAMENT_MULTI_LEG: Qot_Common_pb2.EC_MilestoneType_SoccerTournamentMultiLeg,
            self.BASEBALL_TOURNAMENT: Qot_Common_pb2.EC_MilestoneType_BaseballTournament,
            self.BASEBALL_GAME: Qot_Common_pb2.EC_MilestoneType_BaseballGame,
        }


class ECKlineSource(FtEnum):
    """事件合约K线来源（区分合约成交价K线与子合约摆盘K线）"""
    NONE = "N/A"
    ORDER_BOOK_YES = "ORDER_BOOK_YES"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.EC_KlineSource_None,
            self.ORDER_BOOK_YES: Qot_Common_pb2.EC_KlineSource_OrderBookYes,
        }
