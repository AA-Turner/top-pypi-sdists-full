from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03"


@dataclass(kw_only=True)
class ActiveCurrencyAndAmount:
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


class AgreementFramework1Code(Enum):
    FBAA = "FBAA"
    BBAA = "BBAA"
    DERV = "DERV"
    ISDA = "ISDA"
    NONR = "NONR"


class CollateralAccountType1Code(Enum):
    HOUS = "HOUS"
    CLIE = "CLIE"
    LIPR = "LIPR"
    MGIN = "MGIN"
    DFLT = "DFLT"


class CollateralType1Code(Enum):
    CASH = "CASH"
    SECU = "SECU"
    LCRE = "LCRE"
    OTHR = "OTHR"


@dataclass(kw_only=True)
class DateAndDateTimeChoice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


class DateType2Code(Enum):
    OPEN = "OPEN"


class DepositType1Code(Enum):
    FITE = "FITE"
    CALL = "CALL"


class EventFrequency6Code(Enum):
    DAIL = "DAIL"
    INDA = "INDA"
    ONDE = "ONDE"


class ExposureType1Code(Enum):
    CCIR = "CCIR"
    COMM = "COMM"
    CRDS = "CRDS"
    CRPR = "CRPR"
    CRSP = "CRSP"
    CRTL = "CRTL"
    EQPT = "EQPT"
    EQUS = "EQUS"
    EXPT = "EXPT"
    EXTD = "EXTD"
    FIXI = "FIXI"
    FORW = "FORW"
    FORX = "FORX"
    FUTR = "FUTR"
    LIQU = "LIQU"
    OPTN = "OPTN"
    OTCD = "OTCD"
    PAYM = "PAYM"
    REPO = "REPO"
    SBSC = "SBSC"
    SCIE = "SCIE"
    SCIR = "SCIR"
    SCRP = "SCRP"
    SLEB = "SLEB"
    SLOA = "SLOA"
    SWPT = "SWPT"
    TRCP = "TRCP"
    BFWD = "BFWD"
    RVPO = "RVPO"
    TBAS = "TBAS"


class ExposureType5Code(Enum):
    BFWD = "BFWD"
    PAYM = "PAYM"
    CCPC = "CCPC"
    COMM = "COMM"
    CRDS = "CRDS"
    CRTL = "CRTL"
    CRSP = "CRSP"
    CCIR = "CCIR"
    CRPR = "CRPR"
    EQUI = "EQUI"
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
    REPO = "REPO"
    RVPO = "RVPO"
    SLOA = "SLOA"
    SBSC = "SBSC"
    SCRP = "SCRP"
    SLEB = "SLEB"
    SHSL = "SHSL"
    SCIR = "SCIR"
    SCIE = "SCIE"
    SWPT = "SWPT"
    TBAS = "TBAS"
    TRBD = "TRBD"
    TRCP = "TRCP"


@dataclass(kw_only=True)
class FinancialInstrumentQuantity1Choice:
    unit: None | Decimal = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    face_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "FaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification30:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class IdentificationSource3Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
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


@dataclass(kw_only=True)
class Pagination:
    pg_nb: str = field(
        metadata={
            "name": "PgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "pattern": r"[0-9]{1,5}",
        }
    )
    last_pg_ind: bool = field(
        metadata={
            "name": "LastPgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class PostalAddress2:
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd_id: str = field(
        metadata={
            "name": "PstCdId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 16,
        }
    )
    twn_nm: str = field(
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


class PriceValueType1Code(Enum):
    DISC = "DISC"
    PREM = "PREM"
    PARV = "PARV"


class SafekeepingPlace1Code(Enum):
    CUST = "CUST"
    ICSD = "ICSD"
    NCSD = "NCSD"
    SHHE = "SHHE"


class SafekeepingPlace3Code(Enum):
    SHHE = "SHHE"


class SettlementStatus2Code(Enum):
    AAUT = "AAUT"
    ASTL = "ASTL"
    STCR = "STCR"
    STLD = "STLD"
    ACCF = "ACCF"
    ARCF = "ARCF"


class ShortLong1Code(Enum):
    SHOR = "SHOR"
    LONG = "LONG"


@dataclass(kw_only=True)
class SupplementaryDataEnvelope1:
    any_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


class ThresholdType1Code(Enum):
    SECU = "SECU"
    UNSE = "UNSE"


@dataclass(kw_only=True)
class AgreementFramework1Choice:
    agrmt_frmwk: None | AgreementFramework1Code = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    prtry_id: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class CashCollateral4:
    asst_nb: None | str = field(
        default=None,
        metadata={
            "name": "AsstNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dpst_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DpstAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    dpst_tp: None | DepositType1Code = field(
        default=None,
        metadata={
            "name": "DpstTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    blckd_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "BlckdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    mtrty_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "MtrtyDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    val_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    xchg_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    coll_val: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "CollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    hrcut: None | Decimal = field(
        default=None,
        metadata={
            "name": "Hrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )


@dataclass(kw_only=True)
class CollateralAccountIdentificationType2Choice:
    tp: None | CollateralAccountType1Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    prtry: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class CollateralAmount1:
    coll_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "CollAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    rptd_ccy_and_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "RptdCcyAndAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    mkt_val_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "MktValAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    acrd_intrst_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "AcrdIntrstAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    fees_and_comssns: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "FeesAndComssns",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class DateCode9Choice:
    cd: None | DateType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class GenericIdentification78:
    tp: GenericIdentification30 = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class NameAndAddress6:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    adr: PostalAddress2 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class OtherIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 16,
        },
    )
    tp: IdentificationSource3Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class OtherTypeOfCollateral2:
    desc: str = field(
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 140,
        }
    )
    qty: None | FinancialInstrumentQuantity1Choice = field(
        default=None,
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class PriceRateOrAmountChoice:
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    amt: None | ActiveOrHistoricCurrencyAnd13DecimalAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class ReportParameters5:
    rpt_id: str = field(
        metadata={
            "name": "RptId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    rpt_dt_and_tm: DateAndDateTimeChoice = field(
        metadata={
            "name": "RptDtAndTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    frqcy: EventFrequency6Code = field(
        metadata={
            "name": "Frqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    rpt_ccy: str = field(
        metadata={
            "name": "RptCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    clctn_dt: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "ClctnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class SafekeepingPlaceTypeAndAnyBicidentifier1:
    class Meta:
        name = "SafekeepingPlaceTypeAndAnyBICIdentifier1"

    sfkpg_plc_tp: SafekeepingPlace1Code = field(
        metadata={
            "name": "SfkpgPlcTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        }
    )


@dataclass(kw_only=True)
class SafekeepingPlaceTypeAndText8:
    sfkpg_plc_tp: SafekeepingPlace3Code = field(
        metadata={
            "name": "SfkpgPlcTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class SummaryAmounts1:
    thrshld_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "ThrshldAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    thrshld_tp: None | ThresholdType1Code = field(
        default=None,
        metadata={
            "name": "ThrshldTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    pre_hrcut_coll_val: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "PreHrcutCollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    adjstd_xpsr: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "AdjstdXpsr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    coll_reqrd: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CollReqrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    min_trf_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "MinTrfAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    rndg_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RndgAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    prvs_xpsr_val: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "PrvsXpsrVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    prvs_coll_val: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "PrvsCollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    ttl_pdg_incmg_coll: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlPdgIncmgColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    ttl_pdg_outgng_coll: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlPdgOutgngColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    ttl_acrd_intrst_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlAcrdIntrstAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    ttl_fees: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlFees",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class YieldedOrValueType1Choice:
    yldd: None | bool = field(
        default=None,
        metadata={
            "name": "Yldd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    val_tp: None | PriceValueType1Code = field(
        default=None,
        metadata={
            "name": "ValTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class Agreement4:
    agrmt_dtls: str = field(
        metadata={
            "name": "AgrmtDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 140,
        }
    )
    agrmt_id: None | str = field(
        default=None,
        metadata={
            "name": "AgrmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    agrmt_dt: XmlDate = field(
        metadata={
            "name": "AgrmtDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    base_ccy: str = field(
        metadata={
            "name": "BaseCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    agrmt_frmwk: None | AgreementFramework1Choice = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class CollateralAccount2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tp: None | CollateralAccountIdentificationType2Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class DateFormat14Choice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    dt_cd: None | DateCode9Choice = field(
        default=None,
        metadata={
            "name": "DtCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification100Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    nm_and_adr: None | NameAndAddress6 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class Price2:
    tp: YieldedOrValueType1Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    val: PriceRateOrAmountChoice = field(
        metadata={
            "name": "Val",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SafekeepingPlaceFormat10Choice:
    id: None | SafekeepingPlaceTypeAndText8 = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    tp_and_id: None | SafekeepingPlaceTypeAndAnyBicidentifier1 = field(
        default=None,
        metadata={
            "name": "TpAndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    prtry: None | GenericIdentification78 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class SecurityIdentification19:
    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "pattern": r"[A-Z]{2,2}[A-Z0-9]{9,9}[0-9]{1,1}",
        },
    )
    othr_id: list[OtherIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class Summary1:
    xpsd_amt_pty_a: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "XpsdAmtPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    xpsd_amt_pty_b: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "XpsdAmtPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    xpsr_tp: ExposureType1Code = field(
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    ttl_val_of_coll: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "TtlValOfColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    net_xcss_dfcit: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "NetXcssDfcit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    net_xcss_dfcit_ind: None | ShortLong1Code = field(
        default=None,
        metadata={
            "name": "NetXcssDfcitInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    valtn_dt_tm: XmlDateTime = field(
        metadata={
            "name": "ValtnDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    reqd_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ReqdSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    summry_dtls: None | SummaryAmounts1 = field(
        default=None,
        metadata={
            "name": "SummryDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class CollateralOwnership2:
    prtry: bool = field(
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    clnt_nm: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "ClntNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class Obligation4:
    pty_a: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    svcg_pty_a: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    pty_b: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    svcg_pty_b: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    coll_acct_id: None | CollateralAccount2 = field(
        default=None,
        metadata={
            "name": "CollAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    xpsr_tp: None | ExposureType5Code = field(
        default=None,
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    valtn_dt: DateAndDateTimeChoice = field(
        metadata={
            "name": "ValtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class OtherCollateral6:
    asst_nb: None | str = field(
        default=None,
        metadata={
            "name": "AsstNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    lttr_of_cdt_id: None | str = field(
        default=None,
        metadata={
            "name": "LttrOfCdtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    lttr_of_cdt_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "LttrOfCdtAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    grnt_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "GrntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    othr_tp_of_coll: None | OtherTypeOfCollateral2 = field(
        default=None,
        metadata={
            "name": "OthrTpOfColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    coll_ownrsh: None | CollateralOwnership2 = field(
        default=None,
        metadata={
            "name": "CollOwnrsh",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    isse_dt: None | DateFormat14Choice = field(
        default=None,
        metadata={
            "name": "IsseDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    xpry_dt: None | DateFormat14Choice = field(
        default=None,
        metadata={
            "name": "XpryDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    ltd_cvrg_ind: None | bool = field(
        default=None,
        metadata={
            "name": "LtdCvrgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    issr: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    blckd_qty: None | FinancialInstrumentQuantity1Choice = field(
        default=None,
        metadata={
            "name": "BlckdQty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    val_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    xchg_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    mkt_val: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "MktVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    hrcut: None | Decimal = field(
        default=None,
        metadata={
            "name": "Hrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    coll_val: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "CollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    sfkpg_plc: None | SafekeepingPlaceFormat10Choice = field(
        default=None,
        metadata={
            "name": "SfkpgPlc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    sfkpg_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class SecuritiesCollateral6:
    asst_nb: None | str = field(
        default=None,
        metadata={
            "name": "AsstNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    scty_id: SecurityIdentification19 = field(
        metadata={
            "name": "SctyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    mtrty_dt: None | DateAndDateTimeChoice = field(
        default=None,
        metadata={
            "name": "MtrtyDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    coll_ownrsh: None | CollateralOwnership2 = field(
        default=None,
        metadata={
            "name": "CollOwnrsh",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    ltd_cvrg_ind: None | bool = field(
        default=None,
        metadata={
            "name": "LtdCvrgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    qty: FinancialInstrumentQuantity1Choice = field(
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    blckd_qty: None | FinancialInstrumentQuantity1Choice = field(
        default=None,
        metadata={
            "name": "BlckdQty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    pric: None | Price2 = field(
        default=None,
        metadata={
            "name": "Pric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    mkt_val: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "MktVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    hrcut: None | Decimal = field(
        default=None,
        metadata={
            "name": "Hrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    coll_val: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    val_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    sfkpg_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    sfkpg_plc: SafekeepingPlaceFormat10Choice = field(
        metadata={
            "name": "SfkpgPlc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CollateralValuation5:
    coll_id: None | str = field(
        default=None,
        metadata={
            "name": "CollId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    coll_tp: CollateralType1Code = field(
        metadata={
            "name": "CollTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    sttlm_sts: SettlementStatus2Code = field(
        metadata={
            "name": "SttlmSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    nb_of_days_acrd: Decimal = field(
        metadata={
            "name": "NbOfDaysAcrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
            "total_digits": 18,
            "fraction_digits": 0,
        }
    )
    valtn_amts: CollateralAmount1 = field(
        metadata={
            "name": "ValtnAmts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    day_cnt_bsis: InterestComputationMethod2Code = field(
        metadata={
            "name": "DayCntBsis",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    xchg_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    ccy_hrcut: None | Decimal = field(
        default=None,
        metadata={
            "name": "CcyHrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    adjstd_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "AdjstdRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    scties_coll: None | SecuritiesCollateral6 = field(
        default=None,
        metadata={
            "name": "SctiesColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    csh_coll: None | CashCollateral4 = field(
        default=None,
        metadata={
            "name": "CshColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    othr_coll: None | OtherCollateral6 = field(
        default=None,
        metadata={
            "name": "OthrColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class Collateral13:
    acct_id: CollateralAccount2 = field(
        metadata={
            "name": "AcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    rpt_summry: Summary1 = field(
        metadata={
            "name": "RptSummry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    coll_valtn: list[CollateralValuation5] = field(
        default_factory=list,
        metadata={
            "name": "CollValtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class CollateralAndExposureReportV03:
    rpt_params: ReportParameters5 = field(
        metadata={
            "name": "RptParams",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    pgntn: None | Pagination = field(
        default=None,
        metadata={
            "name": "Pgntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    oblgtn: Obligation4 = field(
        metadata={
            "name": "Oblgtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "required": True,
        }
    )
    agrmt: None | Agreement4 = field(
        default=None,
        metadata={
            "name": "Agrmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )
    coll_rpt: list[Collateral13] = field(
        default_factory=list,
        metadata={
            "name": "CollRpt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
            "min_occurs": 1,
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.016.001.03"

    coll_and_xpsr_rpt: CollateralAndExposureReportV03 = field(
        metadata={
            "name": "CollAndXpsrRpt",
            "type": "Element",
            "required": True,
        }
    )
