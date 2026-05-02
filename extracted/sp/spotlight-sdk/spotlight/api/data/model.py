"""
Data classes for API requests.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from pydantic import Field as PyField, root_validator

from spotlight.core.common.base import Base
from spotlight.core.common.base_enum import BaseEnum
from spotlight.core.common.decorators.serializable import (
    serializable_base_class,
    serializable,
)
from spotlight.core.common.enum import (
    Order,
    ComparisonOperator,
    LogicalOperator,
    SqlFunction,
)


class Sort(Base):
    field: str
    order: Order


class Filter(Base):
    field: str
    operator: ComparisonOperator
    value: Any


class WhereClause(Base):
    filter: Optional[Filter] = PyField(default=None)
    operator: Optional[LogicalOperator] = PyField(default=None)
    left: Optional["WhereClause"] = PyField(default=None)
    right: Optional["WhereClause"] = PyField(default=None)


class TimeseriesQueryRequest(Base):
    id: Optional[str] = PyField(default=None)
    dataset_name: Optional[str] = PyField(default=None)
    reference_name: Optional[str] = PyField(default=None)
    page: Optional[int] = PyField(default=None)
    limit: Optional[int] = PyField(default=None)
    fields: Optional[List[str]] = PyField(default=None)
    sort: Optional[List[Sort]] = PyField(default=None)
    where: Optional[WhereClause] = PyField(default=None)


class DistinctQueryRequest(Base):
    id: Optional[str] = PyField(default=None)
    dataset_name: Optional[str] = PyField(default=None)
    reference_name: Optional[str] = PyField(default=None)
    field: str = PyField(default=None)
    sort: Optional[List[Sort]] = PyField(default=None)
    where: Optional[WhereClause] = PyField(default=None)


@serializable_base_class
class Expression(Base):
    pass


@serializable
class FieldExpression(Expression):
    pass


@serializable
class FunctionExpression(FieldExpression):
    pass


@serializable
class Field(FieldExpression):
    name: str
    alias: Optional[str] = PyField(default=None)


@serializable
class SingleExpression(FunctionExpression):
    parameter: FieldExpression
    operator: SqlFunction
    alias: Optional[str] = PyField(default=None)


@serializable
class MultiExpression(FunctionExpression):
    parameters: List[FieldExpression]
    operator: SqlFunction
    alias: Optional[str] = PyField(default=None)


class QueryRequest(Base):
    id: Optional[str] = PyField(default=None)
    dataset_name: Optional[str] = PyField(default=None)
    reference_name: Optional[str] = PyField(default=None)
    fields: Optional[List[FieldExpression]] = PyField(default=None)
    where: Optional[WhereClause] = PyField(default=None)
    groups: Optional[List[str]] = PyField(default=None)
    page: Optional[int] = PyField(default=None)
    limit: Optional[int] = PyField(default=None)
    sort: Optional[List[Sort]] = PyField(default=None)


class TimeUnit(BaseEnum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"
    YTD = "YTD"


class Period(Base):
    n: Optional[int] = PyField(default=None)
    unit: TimeUnit


class InstrumentType(BaseEnum):
    EXOTIC = "EXOTIC"
    FORWARD = "FORWARD"
    MULTI_COMMODITY_EXOTIC = "MULTI_COMMODITY_EXOTIC"
    OPTION = "OPTION"
    SWAP = "SWAP"
    SWAPTION = "SWAPTION"


class Currency(BaseEnum):
    ACU = "ACU"
    ADP = "ADP"
    AED = "AED"
    AFA = "AFA"
    ALL = "ALL"
    AMD = "AMD"
    ANG = "ANG"
    AOA = "AOA"
    AOK = "AOK"
    AON = "AON"
    ARA = "ARA"
    ARS = "ARS"
    ARZ = "ARZ"
    ATS = "ATS"
    AUD = "AUD"
    AUZ = "AUZ"
    AZM = "AZM"
    AZN = "AZN"
    B03 = "B03"
    BAD = "BAD"
    BAK = "BAK"
    BAM = "BAM"
    BBD = "BBD"
    BDN = "BDN"
    BDT = "BDT"
    BEF = "BEF"
    BGL = "BGL"
    BGN = "BGN"
    BHD = "BHD"
    BIF = "BIF"
    BMD = "BMD"
    BND = "BND"
    BOB = "BOB"
    BR6 = "BR6"
    BRE = "BRE"
    BRF = "BRF"
    BRL = "BRL"
    BRR = "BRR"
    BSD = "BSD"
    BTC = "BTC"
    BTN = "BTN"
    BTR = "BTR"
    BWP = "BWP"
    BYR = "BYR"
    BZD = "BZD"
    C23 = "C23"
    CAC = "CAC"
    CAD = "CAD"
    CAZ = "CAZ"
    CCI = "CCI"
    CDF = "CDF"
    CFA = "CFA"
    CHF = "CHF"
    CHZ = "CHZ"
    CLF = "CLF"
    CLP = "CLP"
    CLZ = "CLZ"
    CNH = "CNH"
    CNO = "CNO"
    CNY = "CNY"
    CNZ = "CNZ"
    COP = "COP"
    COZ = "COZ"
    CPB = "CPB"
    CPI = "CPI"
    CRC = "CRC"
    CUP = "CUP"
    CVE = "CVE"
    CYP = "CYP"
    CZH = "CZH"
    CZK = "CZK"
    DAX = "DAX"
    DEM = "DEM"
    DIJ = "DIJ"
    DJF = "DJF"
    DKK = "DKK"
    DOP = "DOP"
    DZD = "DZD"
    E51 = "E51"
    E52 = "E52"
    E53 = "E53"
    E54 = "E54"
    ECI = "ECI"
    ECS = "ECS"
    ECU = "ECU"
    EEK = "EEK"
    EF0 = "EF0"
    EGP = "EGP"
    ESP = "ESP"
    ETB = "ETB"
    EUR = "EUR"
    EUZ = "EUZ"
    F06 = "F06"
    FED = "FED"
    FIM = "FIM"
    FJD = "FJD"
    FKP = "FKP"
    FRF = "FRF"
    FT1 = "FT1"
    GBP = "GBP"
    GBZ = "GBZ"
    GEK = "GEK"
    GEL = "GEL"
    GHC = "GHC"
    GHS = "GHS"
    GHY = "GHY"
    GIP = "GIP"
    GLD = "GLD"
    GLR = "GLR"
    GMD = "GMD"
    GNF = "GNF"
    GQE = "GQE"
    GRD = "GRD"
    GTQ = "GTQ"
    GWP = "GWP"
    GYD = "GYD"
    HKB = "HKB"
    HKD = "HKD"
    HNL = "HNL"
    HRK = "HRK"
    HSI = "HSI"
    HTG = "HTG"
    HUF = "HUF"
    IDB = "IDB"
    IDO = "IDO"
    IDR = "IDR"
    IEP = "IEP"
    IGP = "IGP"
    ILS = "ILS"
    INO = "INO"
    INP = "INP"
    INR = "INR"
    IPA = "IPA"
    IPX = "IPX"
    IQD = "IQD"
    IRR = "IRR"
    IRS = "IRS"
    ISI = "ISI"
    ISK = "ISK"
    ISO = "ISO"
    ITL = "ITL"
    J05 = "J05"
    JMD = "JMD"
    JNI = "JNI"
    JOD = "JOD"
    JPY = "JPY"
    JPZ = "JPZ"
    JZ9 = "JZ9"
    KES = "KES"
    KGS = "KGS"
    KHR = "KHR"
    KMF = "KMF"
    KOR = "KOR"
    KPW = "KPW"
    KRW = "KRW"
    KWD = "KWD"
    KYD = "KYD"
    KZT = "KZT"
    LAK = "LAK"
    LBA = "LBA"
    LBP = "LBP"
    LHY = "LHY"
    LKR = "LKR"
    LRD = "LRD"
    LSL = "LSL"
    LSM = "LSM"
    LTL = "LTL"
    LUF = "LUF"
    LVL = "LVL"
    LYD = "LYD"
    MAD = "MAD"
    MDL = "MDL"
    MGF = "MGF"
    MKD = "MKD"
    MMK = "MMK"
    MNT = "MNT"
    MOP = "MOP"
    MRO = "MRO"
    MTP = "MTP"
    MUR = "MUR"
    MVR = "MVR"
    MWK = "MWK"
    MXB = "MXB"
    MXN = "MXN"
    MXP = "MXP"
    MXW = "MXW"
    MXZ = "MXZ"
    MYO = "MYO"
    MYR = "MYR"
    MZM = "MZM"
    MZN = "MZN"
    NAD = "NAD"
    ND3 = "ND3"
    NGF = "NGF"
    NGI = "NGI"
    NGN = "NGN"
    NIC = "NIC"
    NLG = "NLG"
    NOK = "NOK"
    NOZ = "NOZ"
    NPR = "NPR"
    NZD = "NZD"
    NZZ = "NZZ"
    O08 = "O08"
    OMR = "OMR"
    PAB = "PAB"
    PEI = "PEI"
    PEN = "PEN"
    PEZ = "PEZ"
    PGK = "PGK"
    PHP = "PHP"
    PKR = "PKR"
    PLN = "PLN"
    PLZ = "PLZ"
    PSI = "PSI"
    PTE = "PTE"
    PYG = "PYG"
    QAR = "QAR"
    R2K = "R2K"
    ROL = "ROL"
    RON = "RON"
    RSD = "RSD"
    RUB = "RUB"
    RUF = "RUF"
    RUR = "RUR"
    RWF = "RWF"
    SAR = "SAR"
    SBD = "SBD"
    SCR = "SCR"
    SDP = "SDP"
    SDR = "SDR"
    SEK = "SEK"
    SET = "SET"
    SGD = "SGD"
    SGS = "SGS"
    SHP = "SHP"
    SKK = "SKK"
    SLL = "SLL"
    SRG = "SRG"
    SSI = "SSI"
    STD = "STD"
    SUR = "SUR"
    SVC = "SVC"
    SVT = "SVT"
    SYP = "SYP"
    SZL = "SZL"
    T21 = "T21"
    T51 = "T51"
    T52 = "T52"
    T53 = "T53"
    T54 = "T54"
    T55 = "T55"
    T71 = "T71"
    TE0 = "TE0"
    TED = "TED"
    TF9 = "TF9"
    THB = "THB"
    THO = "THO"
    TMM = "TMM"
    TND = "TND"
    TNT = "TNT"
    TOP = "TOP"
    TPE = "TPE"
    TPX = "TPX"
    TRB = "TRB"
    TRL = "TRL"
    TRY = "TRY"
    TRZ = "TRZ"
    TTD = "TTD"
    TWD = "TWD"
    TZS = "TZS"
    UAH = "UAH"
    UCB = "UCB"
    UDI = "UDI"
    UFC = "UFC"
    UFZ = "UFZ"
    UGS = "UGS"
    UGX = "UGX"
    USB = "USB"
    USD = "USD"
    UVR = "UVR"
    UYP = "UYP"
    UYU = "UYU"
    UZS = "UZS"
    VAC = "VAC"
    VEB = "VEB"
    VEF = "VEF"
    VES = "VES"
    VND = "VND"
    VUV = "VUV"
    WST = "WST"
    XAF = "XAF"
    XAG = "XAG"
    XAU = "XAU"
    XPD = "XPD"
    XPT = "XPT"
    XCD = "XCD"
    XDR = "XDR"
    XEU = "XEU"
    XOF = "XOF"
    XPF = "XPF"
    YDD = "YDD"
    YER = "YER"
    YUD = "YUD"
    YUN = "YUN"
    ZAL = "ZAL"
    ZAR = "ZAR"
    ZAZ = "ZAZ"
    ZMK = "ZMK"
    ZMW = "ZMW"
    ZRN = "ZRN"
    ZRZ = "ZRZ"
    ZWD = "ZWD"


class SubProduct(BaseEnum):
    DAIRY = "Dairy"
    ELECTRICITY = "Electricity"
    GRAINS_OILSEEDS = "Grains Oilseeds"
    LIVESTOCK = "Livestock"
    NATURAL_GAS = "Natural Gas"
    OIL = "Oil"
    SOFTS = "Softs"


class AssetCategory(BaseEnum):
    BARREL_CHEESE_MONTHLY_AVERAGE = "Barrel Cheese Monthly Average"
    BLOCK_CHEESE = "Block Cheese"
    BUTTER = "Butter"
    CASH_SETTLED_CHEESE = "Cash-Settled Cheese"
    CLASS_I_MILK = "Class I Milk"
    CLASS_III_MILK = "Class III Milk"
    CLASS_IV_MILK = "Class IV Milk"
    DRY_WHEY = "Dry Whey"
    EEX_EUROPEAN_BUTTER = "EEX European Butter"
    EEX_EUROPEAN_SKIMMED_MILK_POWDER = "EEX European Skimmed Milk Powder"
    EEX_EUROPEAN_WHEY_POWDER = "EEX European Whey Powder"
    LACTOSE = "Lactose"
    NON_FAT_DRY_MILK = "Non Fat Dry Milk"
    SGX_NZX_GLOBAL_BUTTER = "SGX-NZX Global Butter"
    SGX_NZX_GLOBAL_WHOLE_MILK_POWDER = "SGX-NZX Global Whole Milk Powder"
    SKIMMED_MILK_POWDER = "Skimmed Milk Powder"
    BASE_LOAD = "Base Load"
    OFF_PEAK = "Off Peak"
    OTHER = "Other"
    PEAK_LOAD = "Peak Load"
    CORN = "Corn"
    CRUDE_PALM_KERNEL_OIL_CIF_ROTTERDAM = "Crude Palm Kernel Oil CIF Rotterdam"
    CRUDE_PALM_OIL = "Crude Palm Oil"
    DALIAN_RBD_PALM_OLEIN = "Dalian RBD Palm Olein"
    FEED_WHEAT = "Feed Wheat"
    MILLING_WHEAT = "Milling Wheat"
    OATS = "Oats"
    PALM_KERNEL_OIL_MALAYSIA = "Palm Kernel Oil Malaysia"
    RAPESEED = "Rapeseed"
    SOYBEAN = "Soybean"
    SOYBEAN_MEAL = "Soybean Meal"
    SOYBEAN_OIL = "Soybean Oil"
    C_23_27_TRMD_SELECTED_HAM = "23-27# Trmd Selected Ham"
    CASH_SETTLED_LIVE_CATTLE = "Cash Settled Live Cattle"
    FEEDER_CATTLE = "Feeder Cattle"
    LEAN_HOG = "Lean Hog"
    LIVE_CATTLE = "Live Cattle"
    PORK_42_TRIMMINGS = "Pork 42 Trimmings"
    BEEF_50_TRIMMINGS = "Beef 50 Trimmings"
    PORK_72_TRIMMINGS = "Pork 72 Trimmings"
    BEEF_90_TRIMMINGS = "Beef 90 Trimmings"
    PORK_PRIMAL_BELLY = "Pork Primal Belly"
    GAS_POOL = "Gas Pool"
    LIQUEFIED_NATURAL_GAS = "Liquefied Natural Gas"
    NATIONAL_BALANCING_POINT_GAS = "National Balancing Point Gas"
    NON_CONDENSABLE_GAS = "Non Condensable Gas"
    TITLE_TRANSFER_FACILITY_GAS = "Title Transfer Facility Gas"
    BAKKEN = "Bakken"
    BIODIESEL = "Biodiesel"
    BRENT = "Brent"
    BRENT_1ST_LINE = "Brent 1st Line"
    BRENT_CRUDE = "Brent Crude"
    CONDENSATE = "Condensate"
    DIESEL = "Diesel"
    EIA_FLAT_TAX_ON_HIGHWAY_DIESEL = "EIA Flat Tax On-Highway Diesel"
    ETHANOL = "Ethanol"
    FUEL = "Fuel"
    FUEL_OIL = "Fuel Oil"
    GAS_OIL = "Gas Oil"
    GASOLINE = "Gasoline"
    HEATING_OIL = "Heating Oil"
    NATURAL_GAS_LIQUIDS_OIL = "Natural Gas Liquids Oil"
    WEST_TEXAS_INTERMEDIATE_OIL = "West Texas Intermediate Oil"
    WTI_FINANCIAL = "WTI Financial"
    ARABICA_COFFEE = "Arabica Coffee"
    COCOA = "Cocoa"
    COFFEE = "Coffee"
    COTTON = "Cotton"
    LONDON_COCOA = "London Cocoa"
    NO_11_SUGAR = "No. 11 Sugar"
    ROBUSTA_COFFEE = "Robusta Coffee"
    SHANGHAI_NATURAL_RUBBER = "Shanghai Natural Rubber"
    SHANGHAI_TSR_20 = "Shanghai TSR 20"
    SICOM_TSR_20_FOB_RUBBER = "SICOM TSR 20 (FOB) Rubber"
    WHITE_SUGAR = "White Sugar"


_SUB_PRODUCT_TO_ASSET_CATEGORY_MAP: Dict[SubProduct, Set[AssetCategory]] = {
    SubProduct.DAIRY: {
        AssetCategory.BARREL_CHEESE_MONTHLY_AVERAGE,
        AssetCategory.BLOCK_CHEESE,
        AssetCategory.BUTTER,
        AssetCategory.CASH_SETTLED_CHEESE,
        AssetCategory.CLASS_I_MILK,
        AssetCategory.CLASS_III_MILK,
        AssetCategory.CLASS_IV_MILK,
        AssetCategory.DRY_WHEY,
        AssetCategory.EEX_EUROPEAN_BUTTER,
        AssetCategory.EEX_EUROPEAN_SKIMMED_MILK_POWDER,
        AssetCategory.EEX_EUROPEAN_WHEY_POWDER,
        AssetCategory.LACTOSE,
        AssetCategory.NON_FAT_DRY_MILK,
        AssetCategory.SGX_NZX_GLOBAL_BUTTER,
        AssetCategory.SGX_NZX_GLOBAL_WHOLE_MILK_POWDER,
        AssetCategory.SKIMMED_MILK_POWDER,
    },
    SubProduct.ELECTRICITY: {
        AssetCategory.BASE_LOAD,
        AssetCategory.OFF_PEAK,
        AssetCategory.OTHER,
        AssetCategory.PEAK_LOAD,
    },
    SubProduct.GRAINS_OILSEEDS: {
        AssetCategory.CORN,
        AssetCategory.CRUDE_PALM_KERNEL_OIL_CIF_ROTTERDAM,
        AssetCategory.CRUDE_PALM_OIL,
        AssetCategory.DALIAN_RBD_PALM_OLEIN,
        AssetCategory.FEED_WHEAT,
        AssetCategory.MILLING_WHEAT,
        AssetCategory.OATS,
        AssetCategory.PALM_KERNEL_OIL_MALAYSIA,
        AssetCategory.RAPESEED,
        AssetCategory.SOYBEAN,
        AssetCategory.SOYBEAN_MEAL,
        AssetCategory.SOYBEAN_OIL,
    },
    SubProduct.LIVESTOCK: {
        AssetCategory.C_23_27_TRMD_SELECTED_HAM,
        AssetCategory.CASH_SETTLED_LIVE_CATTLE,
        AssetCategory.FEEDER_CATTLE,
        AssetCategory.LEAN_HOG,
        AssetCategory.LIVE_CATTLE,
        AssetCategory.PORK_42_TRIMMINGS,
        AssetCategory.BEEF_50_TRIMMINGS,
        AssetCategory.PORK_72_TRIMMINGS,
        AssetCategory.BEEF_90_TRIMMINGS,
        AssetCategory.PORK_PRIMAL_BELLY,
    },
    SubProduct.NATURAL_GAS: {
        AssetCategory.GAS_POOL,
        AssetCategory.LIQUEFIED_NATURAL_GAS,
        AssetCategory.NATIONAL_BALANCING_POINT_GAS,
        AssetCategory.NON_CONDENSABLE_GAS,
        AssetCategory.TITLE_TRANSFER_FACILITY_GAS,
    },
    SubProduct.OIL: {
        AssetCategory.BAKKEN,
        AssetCategory.BIODIESEL,
        AssetCategory.BRENT,
        AssetCategory.BRENT_1ST_LINE,
        AssetCategory.BRENT_CRUDE,
        AssetCategory.CONDENSATE,
        AssetCategory.DIESEL,
        AssetCategory.EIA_FLAT_TAX_ON_HIGHWAY_DIESEL,
        AssetCategory.ETHANOL,
        AssetCategory.FUEL,
        AssetCategory.FUEL_OIL,
        AssetCategory.GAS_OIL,
        AssetCategory.GASOLINE,
        AssetCategory.HEATING_OIL,
        AssetCategory.NATURAL_GAS_LIQUIDS_OIL,
        AssetCategory.WEST_TEXAS_INTERMEDIATE_OIL,
        AssetCategory.WTI_FINANCIAL,
    },
    SubProduct.SOFTS: {
        AssetCategory.ARABICA_COFFEE,
        AssetCategory.COCOA,
        AssetCategory.COFFEE,
        AssetCategory.COTTON,
        AssetCategory.CRUDE_PALM_OIL,
        AssetCategory.LONDON_COCOA,
        AssetCategory.NO_11_SUGAR,
        AssetCategory.ROBUSTA_COFFEE,
        AssetCategory.SHANGHAI_NATURAL_RUBBER,
        AssetCategory.SHANGHAI_TSR_20,
        AssetCategory.SICOM_TSR_20_FOB_RUBBER,
        AssetCategory.WHITE_SUGAR,
    },
}


class AssetFilter(Base):
    sub_product: Optional[SubProduct] = PyField(default=None)
    asset_category: Optional[AssetCategory] = PyField(default=None)

    @root_validator
    def _validate_asset_category_matches_sub_product(
        cls, values: Dict[str, Optional[BaseEnum]]
    ) -> Dict[str, Optional[BaseEnum]]:
        sub_product = values.get("sub_product")
        asset_category = values.get("asset_category")

        if sub_product is None or asset_category is None:
            return values

        if isinstance(sub_product, str):
            sub_product = SubProduct(sub_product)

        if isinstance(asset_category, str):
            asset_category = AssetCategory(asset_category)

        allowed_categories = _SUB_PRODUCT_TO_ASSET_CATEGORY_MAP.get(sub_product, set())
        if asset_category in allowed_categories:
            return values

        allowed_values = sorted(category.value for category in allowed_categories)
        raise ValueError(
            f"asset_category '{asset_category.value}' is invalid for sub_product "
            f"'{sub_product.value}'. Allowed categories: {', '.join(allowed_values)}"
        )


class TradeCountByTenorQuery(Base):
    assets: List[AssetFilter]
    instrument: List[InstrumentType]
    currency: List[Optional[Currency]]
    group_by: TimeUnit
    history: Period


class MarketShareQuery(Base):
    assets: List[AssetFilter]
    currency: Optional[List[Optional[Currency]]] = PyField(default=None)
    group_by: TimeUnit
    history: Period
    target: str = PyField(default="C", const=True)


class MarketShareSummaryQuery(Base):
    assets: List[AssetFilter]
    group_by: TimeUnit = PyField(default=TimeUnit.MONTH)
    target: str = PyField(default="C", const=True)


class TradeCountByTenorResponse(Base):
    execution_date: datetime
    weeks_1: int
    weeks_2: int
    weeks_3: int
    months_1: int
    months_2: int
    months_3: int
    months_6: int
    years_1: int
    years_2: int
    years_3: int
    years_5: int
    years_5_plus: int


class TradeCountByCurrencyResponse(Base):
    execution_date: datetime
    currency: Optional[str] = PyField(default=None)
    count: int


class MarketShareAssetResponse(Base):
    execution_date: datetime
    sub_product: Optional[str] = PyField(default=None)
    asset_category: Optional[str] = PyField(default=None)
    total_trades_target: float
    total_trades_other: float
    total_contracts_target: float
    total_contracts_other: float
    percent_trades_target: float
    percent_contracts_target: float


class MarketShareTotalsResponse(Base):
    execution_date: datetime
    total_trades_target: float
    total_trades_other: float
    total_contracts_target: float
    total_contracts_other: float
    percent_trades_target: float
    percent_contracts_target: float


class MarketShareSummaryResponse(Base):
    current_market_share_trades_percent: float
    current_market_share_contracts_percent: float
    yoy_change_trades_percent: float
    yoy_change_contracts_percent: float
