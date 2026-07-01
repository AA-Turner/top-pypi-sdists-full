from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01"


@dataclass(kw_only=True)
class ActiveOrHistoricCurrencyAnd13DecimalAmount:
    value: Decimal = field(
        metadata={
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 13,
        }
    )
    ccy: str = field(
        metadata={
            "name": "Ccy",
            "type": "Attribute",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )


@dataclass(kw_only=True)
class ActiveOrHistoricCurrencyAndAmount:
    value: Decimal = field(
        metadata={
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        }
    )
    ccy: str = field(
        metadata={
            "name": "Ccy",
            "type": "Attribute",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


class BenchmarkCurveName7Code(Enum):
    BBSW = "BBSW"
    BUBO = "BUBO"
    BCOL = "BCOL"
    CDOR = "CDOR"
    CIBO = "CIBO"
    CORA = "CORA"
    CZNA = "CZNA"
    EONA = "EONA"
    EONS = "EONS"
    ESTR = "ESTR"
    EURI = "EURI"
    EUUS = "EUUS"
    EUCH = "EUCH"
    EFFR = "EFFR"
    FUSW = "FUSW"
    GCFR = "GCFR"
    HKIO = "HKIO"
    ISDA = "ISDA"
    ETIO = "ETIO"
    JIBA = "JIBA"
    LIBI = "LIBI"
    LIBO = "LIBO"
    MOSP = "MOSP"
    MAAA = "MAAA"
    BJUO = "BJUO"
    NIBO = "NIBO"
    OBFR = "OBFR"
    PFAN = "PFAN"
    PRBO = "PRBO"
    RCTR = "RCTR"
    SOFR = "SOFR"
    SONA = "SONA"
    STBO = "STBO"
    SWAP = "SWAP"
    TLBO = "TLBO"
    TIBO = "TIBO"
    TOAR = "TOAR"
    TREA = "TREA"
    WIBO = "WIBO"


@dataclass(kw_only=True)
class CashAccountIdentification5Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 34,
        },
    )


class CollateralRole1Code(Enum):
    GIVE = "GIVE"
    TAKE = "TAKE"


class CollateralStatus1Code(Enum):
    EXCS = "EXCS"
    DEFI = "DEFI"
    FLAT = "FLAT"


@dataclass(kw_only=True)
class CrystallisationDay1:
    day: bool = field(
        metadata={
            "name": "Day",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    prd: None | str = field(
        default=None,
        metadata={
            "name": "Prd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[0-9]{1,3}",
        },
    )


@dataclass(kw_only=True)
class DateAndDateTime2Choice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


class DateType2Code(Enum):
    OPEN = "OPEN"


class EventFrequency7Code(Enum):
    YEAR = "YEAR"
    ADHO = "ADHO"
    MNTH = "MNTH"
    DAIL = "DAIL"
    INDA = "INDA"
    WEEK = "WEEK"
    SEMI = "SEMI"
    QUTR = "QUTR"
    TOMN = "TOMN"
    TOWK = "TOWK"
    TWMN = "TWMN"
    OVNG = "OVNG"
    ONDE = "ONDE"


class ExecutionStatus1Code(Enum):
    INTD = "INTD"
    PINT = "PINT"


class ExposureType14Code(Enum):
    BFWD = "BFWD"
    PAYM = "PAYM"
    CBCO = "CBCO"
    COMM = "COMM"
    CRDS = "CRDS"
    CRTL = "CRTL"
    CRSP = "CRSP"
    CCIR = "CCIR"
    CRPR = "CRPR"
    EQPT = "EQPT"
    EQUS = "EQUS"
    EXTD = "EXTD"
    EXPT = "EXPT"
    FIXI = "FIXI"
    FORX = "FORX"
    FORW = "FORW"
    FUTR = "FUTR"
    OPTN = "OPTN"
    LIQU = "LIQU"
    OTCD = "OTCD"
    RVPO = "RVPO"
    SLOA = "SLOA"
    SBSC = "SBSC"
    SCRP = "SCRP"
    SLEB = "SLEB"
    SCIR = "SCIR"
    SCIE = "SCIE"
    SWPT = "SWPT"
    TBAS = "TBAS"
    TRCP = "TRCP"
    UDMS = "UDMS"
    CCPC = "CCPC"
    EQUI = "EQUI"
    TRBD = "TRBD"
    REPO = "REPO"
    SHSL = "SHSL"
    MGLD = "MGLD"


@dataclass(kw_only=True)
class FinancialInstrumentQuantity33Choice:
    unit: None | Decimal = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    face_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "FaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )
    amtsd_val: None | Decimal = field(
        default=None,
        metadata={
            "name": "AmtsdVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )
    dgtl_tkn_unit: None | Decimal = field(
        default=None,
        metadata={
            "name": "DgtlTknUnit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 30,
            "fraction_digits": 29,
        },
    )


@dataclass(kw_only=True)
class ForeignExchangeTerms19:
    unit_ccy: str = field(
        metadata={
            "name": "UnitCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    qtd_ccy: str = field(
        metadata={
            "name": "QtdCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    xchg_rate: Decimal = field(
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "total_digits": 11,
            "fraction_digits": 10,
        }
    )


@dataclass(kw_only=True)
class GenericIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | str = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification178:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification30:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | str = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification36:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | str = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification56:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | str = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    bal: Decimal = field(
        metadata={
            "name": "Bal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "total_digits": 18,
            "fraction_digits": 17,
        }
    )


@dataclass(kw_only=True)
class IdentificationSource3Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


class InterestComputationMethod2Code(Enum):
    A001 = "A001"
    A002 = "A002"
    A003 = "A003"
    A004 = "A004"
    A005 = "A005"
    A006 = "A006"
    A007 = "A007"
    A008 = "A008"
    A009 = "A009"
    A010 = "A010"
    A011 = "A011"
    A012 = "A012"
    A013 = "A013"
    A014 = "A014"
    NARR = "NARR"


class InterestRateIndexTenor2Code(Enum):
    INDA = "INDA"
    MNTH = "MNTH"
    YEAR = "YEAR"
    TOMN = "TOMN"
    QUTR = "QUTR"
    FOMN = "FOMN"
    SEMI = "SEMI"
    OVNG = "OVNG"
    WEEK = "WEEK"
    TOWK = "TOWK"


@dataclass(kw_only=True)
class MarketIdentification1Choice:
    mkt_idr_cd: None | str = field(
        default=None,
        metadata={
            "name": "MktIdrCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z0-9]{4,4}",
        },
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


class MarketType4Code(Enum):
    FUND = "FUND"
    LMAR = "LMAR"
    THEO = "THEO"
    VEND = "VEND"


@dataclass(kw_only=True)
class Number3Choice:
    shrt: None | str = field(
        default=None,
        metadata={
            "name": "Shrt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[0-9]{3}",
        },
    )
    lng: None | str = field(
        default=None,
        metadata={
            "name": "Lng",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[0-9]{5}",
        },
    )


class OptionType1Code(Enum):
    CALL = "CALL"
    PUTO = "PUTO"


@dataclass(kw_only=True)
class OriginalAndCurrentQuantities1:
    face_amt: Decimal = field(
        metadata={
            "name": "FaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        }
    )
    amtsd_val: Decimal = field(
        metadata={
            "name": "AmtsdVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        }
    )


@dataclass(kw_only=True)
class Pagination1:
    pg_nb: str = field(
        metadata={
            "name": "PgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "pattern": r"[0-9]{1,5}",
        }
    )
    last_pg_ind: bool = field(
        metadata={
            "name": "LastPgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Period2:
    fr_dt: XmlDate = field(
        metadata={
            "name": "FrDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    to_dt: XmlDate = field(
        metadata={
            "name": "ToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )


class PriceValueType1Code(Enum):
    DISC = "DISC"
    PREM = "PREM"
    PARV = "PARV"


class RepoTerminationOption1Code(Enum):
    EGRN = "EGRN"
    ETSB = "ETSB"


class SafekeepingPlace1Code(Enum):
    CUST = "CUST"
    ICSD = "ICSD"
    NCSD = "NCSD"
    SHHE = "SHHE"


class SafekeepingPlace3Code(Enum):
    SHHE = "SHHE"


class SecuritiesSettlementStatus3Code(Enum):
    PEND = "PEND"
    SETT = "SETT"


class StatementBasis3Code(Enum):
    EOSP = "EOSP"
    FUTM = "FUTM"


class StatementStatusType1Code(Enum):
    CONF = "CONF"
    PEND = "PEND"


class StatementUpdateType1Code(Enum):
    COMP = "COMP"
    DELT = "DELT"


@dataclass(kw_only=True)
class SupplementaryDataEnvelope1:
    any_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


class TradingCapacity7Code(Enum):
    AGEN = "AGEN"
    PRIN = "PRIN"


class TypeOfIdentification1Code(Enum):
    ARNU = "ARNU"
    CCPT = "CCPT"
    CHTY = "CHTY"
    CORP = "CORP"
    DRLC = "DRLC"
    FIIN = "FIIN"
    TXID = "TXID"


@dataclass(kw_only=True)
class ValuationFactorBreakdown1:
    valtn_fctr: None | Decimal = field(
        default=None,
        metadata={
            "name": "ValtnFctr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    infltn_fctr: None | Decimal = field(
        default=None,
        metadata={
            "name": "InfltnFctr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    hrcut: None | Decimal = field(
        default=None,
        metadata={
            "name": "Hrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    pool_fctr: None | Decimal = field(
        default=None,
        metadata={
            "name": "PoolFctr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )


@dataclass(kw_only=True)
class AmountAndDirection53:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    sgn: None | bool = field(
        default=None,
        metadata={
            "name": "Sgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class BasketIdentificationAndEligibilitySetProfile1:
    prfrntl_bskt_id_nb: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "PrfrntlBsktIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    fllbck_startg_bskt_id: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "FllbckStartgBsktId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    exclsn_bskt_id: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "ExclsnBsktId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    elgblty_set_prfl: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "ElgbltySetPrfl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class BenchmarkCurveName13Choice:
    cd: None | BenchmarkCurveName7Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class BlockChainAddressWallet3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 140,
        }
    )
    tp: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class CollateralAmount4:
    actl_mkt_val_pst_valtn_fctr: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "ActlMktValPstValtnFctr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    actl_mkt_val_bfr_valtn_fctr: None | ActiveOrHistoricCurrencyAndAmount = (
        field(
            default=None,
            metadata={
                "name": "ActlMktValBfrValtnFctr",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            },
        )
    )
    xpsr_coll_in_tx_ccy: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "XpsrCollInTxCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    xpsr_coll_in_rptg_ccy: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "XpsrCollInRptgCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    mkt_val_amt_pst_valtn_fctr: None | ActiveOrHistoricCurrencyAndAmount = (
        field(
            default=None,
            metadata={
                "name": "MktValAmtPstValtnFctr",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            },
        )
    )
    mkt_val_amt_bfr_valtn_fctr: None | ActiveOrHistoricCurrencyAndAmount = (
        field(
            default=None,
            metadata={
                "name": "MktValAmtBfrValtnFctr",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            },
        )
    )
    ttl_val_of_own_coll: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlValOfOwnColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_val_of_reusd_coll: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlValOfReusdColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralAmount9:
    actl_mkt_val_pst_hrcut: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "ActlMktValPstHrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    actl_mkt_val_bfr_hrcut: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "ActlMktValBfrHrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    xpsr_coll_in_tx_ccy: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "XpsrCollInTxCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    xpsr_coll_in_rptg_ccy: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "XpsrCollInRptgCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    mkt_val_amt_pst_hrcut: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "MktValAmtPstHrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    mkt_val_amt_bfr_hrcut: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "MktValAmtBfrHrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralStatus2Choice:
    cd: None | ExecutionStatus1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class Date3Choice:
    cd: None | DateType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class ExposureType23Choice:
    cd: None | ExposureType14Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class Frequency22Choice:
    cd: None | EventFrequency7Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class GenericIdentification78:
    tp: GenericIdentification30 = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class IdentificationType42Choice:
    cd: None | TypeOfIdentification1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class InterestComputationMethodFormat4Choice:
    cd: None | InterestComputationMethod2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class MarketType15Choice:
    cd: None | MarketType4Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class OptionType6Choice:
    cd: None | OptionType1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class OtherIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    sfx: None | str = field(
        default=None,
        metadata={
            "name": "Sfx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    tp: IdentificationSource3Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Period4Choice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    fr_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "FrDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    to_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    fr_dt_to_dt: None | Period2 = field(
        default=None,
        metadata={
            "name": "FrDtToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class PostalAddress1:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "max_occurs": 5,
            "min_length": 1,
            "max_length": 70,
        },
    )
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class PriceRateOrAmount3Choice:
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    amt: None | ActiveOrHistoricCurrencyAnd13DecimalAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class Quantity51Choice:
    qty: None | FinancialInstrumentQuantity33Choice = field(
        default=None,
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    orgnl_and_cur_face: None | OriginalAndCurrentQuantities1 = field(
        default=None,
        metadata={
            "name": "OrgnlAndCurFace",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class SafekeepingPlaceTypeAndIdentification1:
    sfkpg_plc_tp: SafekeepingPlace1Code = field(
        metadata={
            "name": "SfkpgPlcTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        }
    )


@dataclass(kw_only=True)
class SafekeepingPlaceTypeAndText8:
    sfkpg_plc_tp: SafekeepingPlace3Code = field(
        metadata={
            "name": "SfkpgPlcTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class SecuritiesAccount19:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tp: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class StatementBasis14Choice:
    cd: None | StatementBasis3Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class TotalValueInPageAndStatement5:
    ttl_xpsr_val_of_pg: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlXpsrValOfPg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_coll_held_val_of_pg: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlCollHeldValOfPg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class TradingPartyCapacity5Choice:
    cd: None | TradingCapacity7Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class UpdateType15Choice:
    cd: None | StatementUpdateType1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class YieldedOrValueType1Choice:
    yldd: None | bool = field(
        default=None,
        metadata={
            "name": "Yldd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    val_tp: None | PriceValueType1Code = field(
        default=None,
        metadata={
            "name": "ValTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class AlternatePartyIdentification7:
    id_tp: IdentificationType42Choice = field(
        metadata={
            "name": "IdTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )
    altrn_id: str = field(
        metadata={
            "name": "AltrnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class BalanceQuantity13Choice:
    qty: None | Quantity51Choice = field(
        default=None,
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification56 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class ClosingDate4Choice:
    dt: None | DateAndDateTime2Choice = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    cd: None | Date3Choice = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralAmount15:
    val_of_coll_held: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "ValOfCollHeld",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    ttl_xpsr: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "TtlXpsr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    mrgn: None | AmountAndDirection53 = field(
        default=None,
        metadata={
            "name": "Mrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_coll_reqrd: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlCollReqrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_acrd_intrst: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlAcrdIntrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_fees_comssns: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlFeesComssns",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_of_prncpls: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlOfPrncpls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_pdg_coll_in: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlPdgCollIn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_pdg_coll_out: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlPdgCollOut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_val_of_own_coll: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlValOfOwnColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_val_of_reusd_coll: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlValOfReusdColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_csh_faild: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlCshFaild",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralAmount16:
    val_of_coll_held: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "ValOfCollHeld",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    ttl_xpsr: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "TtlXpsr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    mrgn: None | AmountAndDirection53 = field(
        default=None,
        metadata={
            "name": "Mrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_coll_reqrd: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlCollReqrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_acrd_intrst: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlAcrdIntrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_val_of_own_coll: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlValOfOwnColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_val_of_reusd_coll: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlValOfReusdColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_of_prncpls: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlOfPrncpls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_pdg_coll_in: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlPdgCollIn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_pdg_coll_out: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlPdgCollOut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_csh_faild: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlCshFaild",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralTransactionAmountBreakdown2:
    lot_nb: GenericIdentification178 = field(
        metadata={
            "name": "LotNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    tx_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prd: None | Period4Choice = field(
        default=None,
        metadata={
            "name": "Prd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class MarketIdentification89:
    id: None | MarketIdentification1Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    tp: MarketType15Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class NameAndAddress5:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 350,
        }
    )
    adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class Price7:
    tp: YieldedOrValueType1Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    val: PriceRateOrAmount3Choice = field(
        metadata={
            "name": "Val",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class RateTypeAndLookback2:
    tp: BenchmarkCurveName13Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    look_bck_days: None | str = field(
        default=None,
        metadata={
            "name": "LookBckDays",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[0-9]{1,3}",
        },
    )
    crstllstn_dt: None | CrystallisationDay1 = field(
        default=None,
        metadata={
            "name": "CrstllstnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    tnr: None | InterestRateIndexTenor2Code = field(
        default=None,
        metadata={
            "name": "Tnr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )


@dataclass(kw_only=True)
class SafekeepingPlaceFormat29Choice:
    id: None | SafekeepingPlaceTypeAndText8 = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    tp_and_id: None | SafekeepingPlaceTypeAndIdentification1 = field(
        default=None,
        metadata={
            "name": "TpAndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    prtry: None | GenericIdentification78 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class SecurityIdentification19:
    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z]{2,2}[A-Z0-9]{9,9}[0-9]{1,1}",
        },
    )
    othr_id: list[OtherIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class Statement78:
    stmt_id: str = field(
        metadata={
            "name": "StmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    rpt_nb: None | Number3Choice = field(
        default=None,
        metadata={
            "name": "RptNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    qry_ref: None | str = field(
        default=None,
        metadata={
            "name": "QryRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    stmt_dt_tm: DateAndDateTime2Choice = field(
        metadata={
            "name": "StmtDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    frqcy: Frequency22Choice = field(
        metadata={
            "name": "Frqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    upd_tp: UpdateType15Choice = field(
        metadata={
            "name": "UpdTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    coll_sd: CollateralRole1Code = field(
        metadata={
            "name": "CollSd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    stmt_bsis: StatementBasis14Choice = field(
        metadata={
            "name": "StmtBsis",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    sts_tp: None | StatementStatusType1Code = field(
        default=None,
        metadata={
            "name": "StsTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    summry_ind: bool = field(
        metadata={
            "name": "SummryInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    actvty_ind: bool = field(
        metadata={
            "name": "ActvtyInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class TransactionStatus6:
    cvrg_sts: None | CollateralStatus1Code = field(
        default=None,
        metadata={
            "name": "CvrgSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    exctn_sts: None | CollateralStatus2Choice = field(
        default=None,
        metadata={
            "name": "ExctnSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class ValuationsDetails2:
    valtn_dtls_amt: list[CollateralAmount9] = field(
        default_factory=list,
        metadata={
            "name": "ValtnDtlsAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_occurs": 1,
        },
    )
    hrcut: Decimal = field(
        metadata={
            "name": "Hrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "total_digits": 11,
            "fraction_digits": 10,
        }
    )


@dataclass(kw_only=True)
class CashBalance15:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    fxdtls: None | ForeignExchangeTerms19 = field(
        default=None,
        metadata={
            "name": "FXDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    csh_acct: None | CashAccountIdentification5Choice = field(
        default=None,
        metadata={
            "name": "CshAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    valtn_dtls: None | ValuationsDetails2 = field(
        default=None,
        metadata={
            "name": "ValtnDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    tx_lot_nb: list[GenericIdentification178] = field(
        default_factory=list,
        metadata={
            "name": "TxLotNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralAmount17:
    val_of_coll_held: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "ValOfCollHeld",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    ttl_xpsr: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "TtlXpsr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    tx_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    tx_amt_brkdwn: list[CollateralTransactionAmountBreakdown2] = field(
        default_factory=list,
        metadata={
            "name": "TxAmtBrkdwn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    mrgn: None | AmountAndDirection53 = field(
        default=None,
        metadata={
            "name": "Mrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_acrd_intrst: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlAcrdIntrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_coll_reqrd: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlCollReqrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_val_of_own_coll: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlValOfOwnColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_val_of_reusd_coll: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlValOfReusdColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_pdg_coll_in: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlPdgCollIn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_pdg_coll_out: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlPdgCollOut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_of_prncpls: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlOfPrncpls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    termntn_tx_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TermntnTxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ttl_csh_faild: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlCshFaild",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class ExposureTypeAggregation3:
    xpsr_tp: ExposureType23Choice = field(
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    sttlm_prc: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "SttlmPrc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    valtn_amts: list[CollateralAmount16] = field(
        default_factory=list,
        metadata={
            "name": "ValtnAmts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_occurs": 1,
        },
    )
    mrgn_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "MrgnRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    gbl_xpsr_tp_sts: None | CollateralStatus1Code = field(
        default=None,
        metadata={
            "name": "GblXpsrTpSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class OverallCollateralDetails2:
    valtn_amts: CollateralAmount15 = field(
        metadata={
            "name": "ValtnAmts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    mrgn_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "MrgnRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    gbl_coll_sts: None | CollateralStatus1Code = field(
        default=None,
        metadata={
            "name": "GblCollSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    valtn_dt: DateAndDateTime2Choice = field(
        metadata={
            "name": "ValtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    coll_addtl_dtls: None | str = field(
        default=None,
        metadata={
            "name": "CollAddtlDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 350,
        },
    )


@dataclass(kw_only=True)
class PartyIdentification120Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    nm_and_adr: None | NameAndAddress5 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class RateOrName4Choice:
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    rate_indx_dtls: None | RateTypeAndLookback2 = field(
        default=None,
        metadata={
            "name": "RateIndxDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class Rating2:
    ratg: str = field(
        metadata={
            "name": "Ratg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 10,
        }
    )
    src_of_ratg: MarketIdentification89 = field(
        metadata={
            "name": "SrcOfRatg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SafeKeepingPlace3:
    sfkpg_plc_frmt: None | SafekeepingPlaceFormat29Choice = field(
        default=None,
        metadata={
            "name": "SfkpgPlcFrmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )


@dataclass(kw_only=True)
class ValuationsDetails1:
    mkt_pric: None | Price7 = field(
        default=None,
        metadata={
            "name": "MktPric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    src_of_pric: None | MarketIdentification89 = field(
        default=None,
        metadata={
            "name": "SrcOfPric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    sttlm_dt: None | DateAndDateTime2Choice = field(
        default=None,
        metadata={
            "name": "SttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    valtn_dtls_amt: CollateralAmount4 = field(
        metadata={
            "name": "ValtnDtlsAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    acrd_intrst: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "AcrdIntrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    clean_pric: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CleanPric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    valtn_fctr_brkdwn: ValuationFactorBreakdown1 = field(
        metadata={
            "name": "ValtnFctrBrkdwn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    nb_of_days_acrd: None | Decimal = field(
        default=None,
        metadata={
            "name": "NbOfDaysAcrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    qtn_age: None | Decimal = field(
        default=None,
        metadata={
            "name": "QtnAge",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )


@dataclass(kw_only=True)
class PartyIdentification136:
    id: PartyIdentification120Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification232:
    id: PartyIdentification120Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    altrn_id: None | AlternatePartyIdentification7 = field(
        default=None,
        metadata={
            "name": "AltrnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralParties11:
    pty_b: PartyIdentification232 = field(
        metadata={
            "name": "PtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    clnt_pty_b: None | PartyIdentification232 = field(
        default=None,
        metadata={
            "name": "ClntPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    trpty_agt: None | PartyIdentification136 = field(
        default=None,
        metadata={
            "name": "TrptyAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    coll_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "CollAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    blck_chain_adr_or_wllt: None | BlockChainAddressWallet3 = field(
        default=None,
        metadata={
            "name": "BlckChainAdrOrWllt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentificationAndAccount202:
    id: PartyIdentification120Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    altrn_id: None | AlternatePartyIdentification7 = field(
        default=None,
        metadata={
            "name": "AltrnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    sfkpg_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    blck_chain_adr_or_wllt: None | BlockChainAddressWallet3 = field(
        default=None,
        metadata={
            "name": "BlckChainAdrOrWllt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    acct_ownr: None | PartyIdentification136 = field(
        default=None,
        metadata={
            "name": "AcctOwnr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    pty_cpcty: None | TradingPartyCapacity5Choice = field(
        default=None,
        metadata={
            "name": "PtyCpcty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class SecuritiesBalance3:
    fin_instrm_id: SecurityIdentification19 = field(
        metadata={
            "name": "FinInstrmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    qty: BalanceQuantity13Choice = field(
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    coll_ind: None | bool = field(
        default=None,
        metadata={
            "name": "CollInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    sfkpg_plc: None | SafeKeepingPlace3 = field(
        default=None,
        metadata={
            "name": "SfkpgPlc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    acct_ownr: None | PartyIdentification232 = field(
        default=None,
        metadata={
            "name": "AcctOwnr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    sfkpg_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    blck_chain_adr_or_wllt: None | BlockChainAddressWallet3 = field(
        default=None,
        metadata={
            "name": "BlckChainAdrOrWllt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    sttlm_sts: None | SecuritiesSettlementStatus3Code = field(
        default=None,
        metadata={
            "name": "SttlmSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    dnmtn_ccy: None | str = field(
        default=None,
        metadata={
            "name": "DnmtnCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    ratg_dtls: list[Rating2] = field(
        default_factory=list,
        metadata={
            "name": "RatgDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    fxdtls: None | ForeignExchangeTerms19 = field(
        default=None,
        metadata={
            "name": "FXDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    valtn_dtls: None | ValuationsDetails1 = field(
        default=None,
        metadata={
            "name": "ValtnDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    tx_lot_nb: list[GenericIdentification178] = field(
        default_factory=list,
        metadata={
            "name": "TxLotNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralParties9:
    pty_a: None | PartyIdentificationAndAccount202 = field(
        default=None,
        metadata={
            "name": "PtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    clnt_pty_a: None | PartyIdentificationAndAccount202 = field(
        default=None,
        metadata={
            "name": "ClntPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    trpty_agt: None | PartyIdentification136 = field(
        default=None,
        metadata={
            "name": "TrptyAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class CounterpartyAggregation3:
    optn_tp: None | OptionType6Choice = field(
        default=None,
        metadata={
            "name": "OptnTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    termntn_optn: None | RepoTerminationOption1Code = field(
        default=None,
        metadata={
            "name": "TermntnOptn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    bskt_id_and_elgblty_set_prfl: (
        None | BasketIdentificationAndEligibilitySetProfile1
    ) = field(
        default=None,
        metadata={
            "name": "BsktIdAndElgbltySetPrfl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    coll_pties: CollateralParties11 = field(
        metadata={
            "name": "CollPties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    valtn_amts: list[CollateralAmount16] = field(
        default_factory=list,
        metadata={
            "name": "ValtnAmts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_occurs": 1,
        },
    )
    mrgn_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "MrgnRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    gbl_ctr_pty_sts: None | CollateralStatus1Code = field(
        default=None,
        metadata={
            "name": "GblCtrPtySts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class Transaction124:
    clnt_trpty_coll_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "ClntTrptyCollTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    trpty_agt_svc_prvdr_coll_tx_id: str = field(
        metadata={
            "name": "TrptyAgtSvcPrvdrCollTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctr_pty_coll_tx_ref: None | str = field(
        default=None,
        metadata={
            "name": "CtrPtyCollTxRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cmon_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "CmonTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "min_length": 1,
            "max_length": 52,
        },
    )
    xpsr_tp: ExposureType23Choice = field(
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    optn_tp: None | OptionType6Choice = field(
        default=None,
        metadata={
            "name": "OptnTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    termntn_optn: None | RepoTerminationOption1Code = field(
        default=None,
        metadata={
            "name": "TermntnOptn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    bskt_id_and_elgblty_set_prfl: (
        None | BasketIdentificationAndEligibilitySetProfile1
    ) = field(
        default=None,
        metadata={
            "name": "BsktIdAndElgbltySetPrfl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    coll_pties: CollateralParties11 = field(
        metadata={
            "name": "CollPties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    exctn_reqd_dt: ClosingDate4Choice = field(
        metadata={
            "name": "ExctnReqdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    clsg_dt: ClosingDate4Choice = field(
        metadata={
            "name": "ClsgDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    valtn_amts: CollateralAmount17 = field(
        metadata={
            "name": "ValtnAmts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    pricg_rate: None | RateOrName4Choice = field(
        default=None,
        metadata={
            "name": "PricgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    mrgn_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "MrgnRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    sprd_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "SprdRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    day_cnt_bsis: None | InterestComputationMethodFormat4Choice = field(
        default=None,
        metadata={
            "name": "DayCntBsis",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    automtc_allcn: None | bool = field(
        default=None,
        metadata={
            "name": "AutomtcAllcn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    tx_sts: list[TransactionStatus6] = field(
        default_factory=list,
        metadata={
            "name": "TxSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "max_occurs": 2,
        },
    )
    scties_bal: list[SecuritiesBalance3] = field(
        default_factory=list,
        metadata={
            "name": "SctiesBal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    csh_bal: list[CashBalance15] = field(
        default_factory=list,
        metadata={
            "name": "CshBal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class TripartyCollateralAndExposureReportV01:
    pgntn: Pagination1 = field(
        metadata={
            "name": "Pgntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    stmt_gnl_dtls: Statement78 = field(
        metadata={
            "name": "StmtGnlDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    coll_pties: CollateralParties9 = field(
        metadata={
            "name": "CollPties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
            "required": True,
        }
    )
    ovrll_coll_aggtn: None | OverallCollateralDetails2 = field(
        default=None,
        metadata={
            "name": "OvrllCollAggtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    xpsr_tp_aggtn: list[ExposureTypeAggregation3] = field(
        default_factory=list,
        metadata={
            "name": "XpsrTpAggtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    ctr_pty_aggtn: list[CounterpartyAggregation3] = field(
        default_factory=list,
        metadata={
            "name": "CtrPtyAggtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    txs: list[Transaction124] = field(
        default_factory=list,
        metadata={
            "name": "Txs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    acct_base_ccy_ttl_amts: None | TotalValueInPageAndStatement5 = field(
        default=None,
        metadata={
            "name": "AcctBaseCcyTtlAmts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.022.001.01"

    trpty_coll_and_xpsr_rpt: TripartyCollateralAndExposureReportV01 = field(
        metadata={
            "name": "TrptyCollAndXpsrRpt",
            "type": "Element",
            "required": True,
        }
    )
