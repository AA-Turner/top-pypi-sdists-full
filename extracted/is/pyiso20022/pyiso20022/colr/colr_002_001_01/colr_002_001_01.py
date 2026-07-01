from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01"


@dataclass(kw_only=True)
class AccountSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


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


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


@dataclass(kw_only=True)
class CashAccountType2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ClearingSystemIdentification2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 5,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ErrorHandling3Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class FinancialIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class FinancialInstrumentQuantity1Choice:
    unit: None | Decimal = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    face_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "FaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification15:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 4,
            "pattern": r"[a-zA-Z0-9]{1,4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    bal: Decimal = field(
        metadata={
            "name": "Bal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "total_digits": 18,
            "fraction_digits": 0,
        }
    )


@dataclass(kw_only=True)
class GenericIdentification30:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class OriginalBusinessQuery1:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    msg_nm_id: None | str = field(
        default=None,
        metadata={
            "name": "MsgNmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cre_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


class PriceValueType1Code(Enum):
    DISC = "DISC"
    PREM = "PREM"
    PARV = "PARV"


@dataclass(kw_only=True)
class ProxyAccountType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


class RequestType1Code(Enum):
    RT01 = "RT01"
    RT02 = "RT02"
    RT03 = "RT03"
    RT04 = "RT04"
    RT05 = "RT05"


class RequestType2Code(Enum):
    RT11 = "RT11"
    RT12 = "RT12"
    RT13 = "RT13"
    RT14 = "RT14"
    RT15 = "RT15"


@dataclass(kw_only=True)
class SupplementaryDataEnvelope1:
    any_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass(kw_only=True)
class AddressType3Choice:
    cd: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class ClearingSystemMemberIdentification2:
    clr_sys_id: None | ClearingSystemIdentification2Choice = field(
        default=None,
        metadata={
            "name": "ClrSysId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    mmb_id: str = field(
        metadata={
            "name": "MmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class ErrorHandling5:
    err: ErrorHandling3Choice = field(
        metadata={
            "name": "Err",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class GenericAccountIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 34,
        }
    )
    schme_nm: None | AccountSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericFinancialIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | FinancialIdentificationSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class OtherIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    tp: IdentificationSource3Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class PostalAddress1:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    amt: None | ActiveOrHistoricCurrencyAnd13DecimalAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class ProxyAccountIdentification1:
    tp: None | ProxyAccountType1Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 2048,
        }
    )


@dataclass(kw_only=True)
class QuantityAndAvailability1:
    qty: FinancialInstrumentQuantity1Choice = field(
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    avlbty_ind: bool = field(
        metadata={
            "name": "AvlbtyInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class RequestType2Choice:
    pmt_ctrl: None | RequestType1Code = field(
        default=None,
        metadata={
            "name": "PmtCtrl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    enqry: None | RequestType2Code = field(
        default=None,
        metadata={
            "name": "Enqry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    prtry: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class SecuritiesAccount19:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    val_tp: None | PriceValueType1Code = field(
        default=None,
        metadata={
            "name": "ValTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class AccountIdentification4Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "pattern": r"[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    othr: None | GenericAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class AmountPricePerFinancialInstrumentQuantity9:
    amt_pric_tp: YieldedOrValueType1Choice = field(
        metadata={
            "name": "AmtPricTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    pric_val: PriceRateOrAmount3Choice = field(
        metadata={
            "name": "PricVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    fin_instrm_qty: FinancialInstrumentQuantity1Choice = field(
        metadata={
            "name": "FinInstrmQty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    pric_fxg_dt: XmlDate = field(
        metadata={
            "name": "PricFxgDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class MessageHeader3:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    req_tp: None | RequestType2Choice = field(
        default=None,
        metadata={
            "name": "ReqTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    orgnl_biz_qry: None | OriginalBusinessQuery1 = field(
        default=None,
        metadata={
            "name": "OrgnlBizQry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    qry_nm: None | str = field(
        default=None,
        metadata={
            "name": "QryNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class NameAndAddress5:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class PostalAddress24:
    adr_tp: None | AddressType3Choice = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    dept: None | str = field(
        default=None,
        metadata={
            "name": "Dept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    sub_dept: None | str = field(
        default=None,
        metadata={
            "name": "SubDept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    bldg_nm: None | str = field(
        default=None,
        metadata={
            "name": "BldgNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    flr: None | str = field(
        default=None,
        metadata={
            "name": "Flr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_bx: None | str = field(
        default=None,
        metadata={
            "name": "PstBx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    room: None | str = field(
        default=None,
        metadata={
            "name": "Room",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    twn_lctn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnLctnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dstrct_nm: None | str = field(
        default=None,
        metadata={
            "name": "DstrctNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "max_occurs": 7,
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class SecurityIdentification19:
    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "pattern": r"[A-Z]{2,2}[A-Z0-9]{9,9}[0-9]{1,1}",
        },
    )
    othr_id: list[OtherIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class SubBalanceQuantity2Choice:
    qty: None | FinancialInstrumentQuantity1Choice = field(
        default=None,
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    prtry: None | GenericIdentification15 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    qty_and_avlbty: None | QuantityAndAvailability1 = field(
        default=None,
        metadata={
            "name": "QtyAndAvlbty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchData3:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress24 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccount38:
    id: AccountIdentification4Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    tp: None | CashAccountType2Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    prxy: None | ProxyAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Prxy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification18:
    bicfi: None | str = field(
        default=None,
        metadata={
            "name": "BICFI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification2 = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress24 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    othr: None | GenericFinancialIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification120Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    nm_and_adr: None | NameAndAddress5 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class SecuritiesPosition1:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 4,
            "pattern": r"[a-zA-Z0-9]{1,4}",
        }
    )
    qty: SubBalanceQuantity2Choice = field(
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification6:
    fin_instn_id: FinancialInstitutionIdentification18 = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    brnch_id: None | BranchData3 = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification136:
    id: PartyIdentification120Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )


@dataclass(kw_only=True)
class SecurityCharacteristics3:
    id: list[SecurityIdentification19] = field(
        default_factory=list,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    pos: list[SecuritiesPosition1] = field(
        default_factory=list,
        metadata={
            "name": "Pos",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    valtn_pric: AmountPricePerFinancialInstrumentQuantity9 = field(
        metadata={
            "name": "ValtnPric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    coll_val: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "CollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CollateralValuePosition3:
    data_accs_tm: XmlDateTime = field(
        metadata={
            "name": "DataAccsTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    ttl_coll_valtn: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlCollValtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    scties_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SctiesAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    scties: list[SecurityCharacteristics3] = field(
        default_factory=list,
        metadata={
            "name": "Scties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class SystemPartyIdentification11:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    id: PartyIdentification136 = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    rspnsbl_pty_id: None | PartyIdentification136 = field(
        default=None,
        metadata={
            "name": "RspnsblPtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class SystemPartyIdentification8:
    id: PartyIdentification136 = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    rspnsbl_pty_id: None | PartyIdentification136 = field(
        default=None,
        metadata={
            "name": "RspnsblPtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralValueReportOrError6Choice:
    biz_err: None | ErrorHandling5 = field(
        default=None,
        metadata={
            "name": "BizErr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    coll_val: None | CollateralValuePosition3 = field(
        default=None,
        metadata={
            "name": "CollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralValueReport3:
    csh_acct: CashAccount38 = field(
        metadata={
            "name": "CshAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    csh_acct_ownr: None | SystemPartyIdentification11 = field(
        default=None,
        metadata={
            "name": "CshAcctOwnr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    csh_acct_svcr: None | BranchAndFinancialInstitutionIdentification6 = field(
        default=None,
        metadata={
            "name": "CshAcctSvcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    scties_acct_ownr: None | SystemPartyIdentification8 = field(
        default=None,
        metadata={
            "name": "SctiesAcctOwnr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    scties_acct_svcr: None | PartyIdentification136 = field(
        default=None,
        metadata={
            "name": "SctiesAcctSvcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    coll_val_rpt: list[CollateralValueReportOrError6Choice] = field(
        default_factory=list,
        metadata={
            "name": "CollValRpt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralValueReportOrError5Choice:
    biz_rpt: list[CollateralValueReport3] = field(
        default_factory=list,
        metadata={
            "name": "BizRpt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )
    oprl_err: list[ErrorHandling5] = field(
        default_factory=list,
        metadata={
            "name": "OprlErr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralValueReportV01:
    msg_hdr: MessageHeader3 = field(
        metadata={
            "name": "MsgHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    rpt_or_err: CollateralValueReportOrError5Choice = field(
        metadata={
            "name": "RptOrErr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
            "required": True,
        }
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.002.001.01"

    coll_val_rpt: CollateralValueReportV01 = field(
        metadata={
            "name": "CollValRpt",
            "type": "Element",
            "required": True,
        }
    )
