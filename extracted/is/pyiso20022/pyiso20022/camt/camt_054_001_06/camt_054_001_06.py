from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlPeriod

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06"


@dataclass(kw_only=True)
class AccountSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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


@dataclass(kw_only=True)
class AmountRangeBoundary1:
    bdry_amt: Decimal = field(
        metadata={
            "name": "BdryAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        }
    )
    incl: bool = field(
        metadata={
            "name": "Incl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


class AttendanceContext1Code(Enum):
    ATTD = "ATTD"
    SATT = "SATT"
    UATT = "UATT"


class AuthenticationEntity1Code(Enum):
    ICCD = "ICCD"
    AGNT = "AGNT"
    MERC = "MERC"


class AuthenticationMethod1Code(Enum):
    UKNW = "UKNW"
    BYPS = "BYPS"
    NPIN = "NPIN"
    FPIN = "FPIN"
    CPSG = "CPSG"
    PPSG = "PPSG"
    MANU = "MANU"
    MERC = "MERC"
    SCRT = "SCRT"
    SNCT = "SNCT"
    SCNL = "SCNL"


@dataclass(kw_only=True)
class BankTransactionCodeStructure6:
    cd: str = field(
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 4,
        }
    )
    sub_fmly_cd: str = field(
        metadata={
            "name": "SubFmlyCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 4,
        }
    )


class Cscmanagement1Code(Enum):
    PRST = "PRST"
    BYPS = "BYPS"
    UNRD = "UNRD"
    NCSC = "NCSC"


class CardDataReading1Code(Enum):
    TAGC = "TAGC"
    PHYS = "PHYS"
    BRCD = "BRCD"
    MGST = "MGST"
    CICC = "CICC"
    DFLE = "DFLE"
    CTLS = "CTLS"
    ECTL = "ECTL"


class CardPaymentServiceType2Code(Enum):
    AGGR = "AGGR"
    DCCV = "DCCV"
    GRTT = "GRTT"
    INSP = "INSP"
    LOYT = "LOYT"
    NRES = "NRES"
    PUCO = "PUCO"
    RECP = "RECP"
    SOAF = "SOAF"
    UNAF = "UNAF"
    VCAU = "VCAU"


@dataclass(kw_only=True)
class CardSequenceNumberRange1:
    frst_tx: None | str = field(
        default=None,
        metadata={
            "name": "FrstTx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    last_tx: None | str = field(
        default=None,
        metadata={
            "name": "LastTx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


class CardholderVerificationCapability1Code(Enum):
    MNSG = "MNSG"
    NPIN = "NPIN"
    FCPN = "FCPN"
    FEPN = "FEPN"
    FDSG = "FDSG"
    FBIO = "FBIO"
    MNVR = "MNVR"
    FBIG = "FBIG"
    APKI = "APKI"
    PKIS = "PKIS"
    CHDT = "CHDT"
    SCEC = "SCEC"


@dataclass(kw_only=True)
class CashAccountType2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CashAvailabilityDate1Choice:
    nb_of_days: None | str = field(
        default=None,
        metadata={
            "name": "NbOfDays",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[\+]{0,1}[0-9]{1,15}",
        },
    )
    actl_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ActlDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


class ChargeBearerType1Code(Enum):
    DEBT = "DEBT"
    CRED = "CRED"
    SHAR = "SHAR"
    SLEV = "SLEV"


@dataclass(kw_only=True)
class ClearingSystemIdentification2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 5,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


class CopyDuplicate1Code(Enum):
    CODU = "CODU"
    COPY = "COPY"
    DUPL = "DUPL"


@dataclass(kw_only=True)
class CorporateAction9:
    evt_tp: str = field(
        metadata={
            "name": "EvtTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    evt_id: str = field(
        metadata={
            "name": "EvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


class CreditDebitCode(Enum):
    CRDT = "CRDT"
    DBIT = "DBIT"


@dataclass(kw_only=True)
class CurrencyExchange5:
    src_ccy: str = field(
        metadata={
            "name": "SrcCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    trgt_ccy: None | str = field(
        default=None,
        metadata={
            "name": "TrgtCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    unit_ccy: None | str = field(
        default=None,
        metadata={
            "name": "UnitCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    xchg_rate: Decimal = field(
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "total_digits": 11,
            "fraction_digits": 10,
        }
    )
    ctrct_id: None | str = field(
        default=None,
        metadata={
            "name": "CtrctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    qtn_dt: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "QtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class DateAndDateTimeChoice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class DateAndPlaceOfBirth:
    birth_dt: XmlDate = field(
        metadata={
            "name": "BirthDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    prvc_of_birth: None | str = field(
        default=None,
        metadata={
            "name": "PrvcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    city_of_birth: str = field(
        metadata={
            "name": "CityOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_of_birth: str = field(
        metadata={
            "name": "CtryOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class DatePeriodDetails:
    fr_dt: XmlDate = field(
        metadata={
            "name": "FrDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    to_dt: XmlDate = field(
        metadata={
            "name": "ToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DateTimePeriodDetails:
    fr_dt_tm: XmlDateTime = field(
        metadata={
            "name": "FrDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    to_dt_tm: XmlDateTime = field(
        metadata={
            "name": "ToDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DiscountAmountType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DocumentLineType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


class DocumentType3Code(Enum):
    RADM = "RADM"
    RPIN = "RPIN"
    FXDR = "FXDR"
    DISP = "DISP"
    PUOR = "PUOR"
    SCOR = "SCOR"


class DocumentType6Code(Enum):
    MSIN = "MSIN"
    CNFA = "CNFA"
    DNFA = "DNFA"
    CINV = "CINV"
    CREN = "CREN"
    DEBN = "DEBN"
    HIRI = "HIRI"
    SBIN = "SBIN"
    CMCN = "CMCN"
    SOAC = "SOAC"
    DISP = "DISP"
    BOLD = "BOLD"
    VCHR = "VCHR"
    AROI = "AROI"
    TSUT = "TSUT"
    PUOR = "PUOR"


class EntryStatus2Code(Enum):
    BOOK = "BOOK"
    PDNG = "PDNG"
    INFO = "INFO"


@dataclass(kw_only=True)
class FinancialIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class FinancialInstrumentQuantityChoice:
    unit: None | Decimal = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    face_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "FaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )


@dataclass(kw_only=True)
class GarnishmentType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


class InterestType1Code(Enum):
    INDY = "INDY"
    OVRN = "OVRN"


@dataclass(kw_only=True)
class MessageIdentification2:
    msg_nm_id: None | str = field(
        default=None,
        metadata={
            "name": "MsgNmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    msg_id: None | str = field(
        default=None,
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


class NamePrefix1Code(Enum):
    DOCT = "DOCT"
    MIST = "MIST"
    MISS = "MISS"
    MADM = "MADM"


@dataclass(kw_only=True)
class NumberAndSumOfTransactions1:
    nb_of_ntries: None | str = field(
        default=None,
        metadata={
            "name": "NbOfNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]{1,15}",
        },
    )
    sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )


class OnLineCapability1Code(Enum):
    OFLN = "OFLN"
    ONLN = "ONLN"
    SMON = "SMON"


@dataclass(kw_only=True)
class OrganisationIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class OriginalAndCurrentQuantities1:
    face_amt: Decimal = field(
        metadata={
            "name": "FaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        }
    )


@dataclass(kw_only=True)
class OriginalBusinessQuery1:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cre_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


class PoicomponentType1Code(Enum):
    SOFT = "SOFT"
    EMVK = "EMVK"
    EMVO = "EMVO"
    MRIT = "MRIT"
    CHIT = "CHIT"
    SECM = "SECM"
    PEDV = "PEDV"


@dataclass(kw_only=True)
class Pagination:
    pg_nb: str = field(
        metadata={
            "name": "PgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "pattern": r"[0-9]{1,5}",
        }
    )
    last_pg_ind: bool = field(
        metadata={
            "name": "LastPgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


class PartyType3Code(Enum):
    OPOI = "OPOI"
    MERC = "MERC"
    ACCP = "ACCP"
    ITAG = "ITAG"
    ACQR = "ACQR"
    CISS = "CISS"
    DLIS = "DLIS"


class PartyType4Code(Enum):
    MERC = "MERC"
    ACCP = "ACCP"
    ITAG = "ITAG"
    ACQR = "ACQR"
    CISS = "CISS"
    TAXH = "TAXH"


@dataclass(kw_only=True)
class PersonIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


class PriceValueType1Code(Enum):
    DISC = "DISC"
    PREM = "PREM"
    PARV = "PARV"


@dataclass(kw_only=True)
class ProprietaryBankTransactionCodeStructure1:
    cd: str = field(
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ProprietaryQuantity1:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    qty: str = field(
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class ProprietaryReference1:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ref: str = field(
        metadata={
            "name": "Ref",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class Purpose2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class RateType4Choice:
    pctg: None | Decimal = field(
        default=None,
        metadata={
            "name": "Pctg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    othr: None | str = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


class RemittanceLocationMethod2Code(Enum):
    FAXI = "FAXI"
    EDIC = "EDIC"
    URID = "URID"
    EMAL = "EMAL"
    POST = "POST"
    SMSM = "SMSM"


@dataclass(kw_only=True)
class ReportingSource1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ReturnReason5Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


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
class TaxAmountType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class TaxAuthorisation1:
    titl: None | str = field(
        default=None,
        metadata={
            "name": "Titl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class TaxParty1:
    tax_id: None | str = field(
        default=None,
        metadata={
            "name": "TaxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    regn_id: None | str = field(
        default=None,
        metadata={
            "name": "RegnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_tp: None | str = field(
        default=None,
        metadata={
            "name": "TaxTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


class TaxRecordPeriod1Code(Enum):
    MM01 = "MM01"
    MM02 = "MM02"
    MM03 = "MM03"
    MM04 = "MM04"
    MM05 = "MM05"
    MM06 = "MM06"
    MM07 = "MM07"
    MM08 = "MM08"
    MM09 = "MM09"
    MM10 = "MM10"
    MM11 = "MM11"
    MM12 = "MM12"
    QTR1 = "QTR1"
    QTR2 = "QTR2"
    QTR3 = "QTR3"
    QTR4 = "QTR4"
    HLF1 = "HLF1"
    HLF2 = "HLF2"


@dataclass(kw_only=True)
class TechnicalInputChannel1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class TrackData1:
    trck_nb: None | str = field(
        default=None,
        metadata={
            "name": "TrckNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]",
        },
    )
    trck_val: str = field(
        metadata={
            "name": "TrckVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 140,
        }
    )


class TransactionChannel1Code(Enum):
    MAIL = "MAIL"
    TLPH = "TLPH"
    ECOM = "ECOM"
    TVPY = "TVPY"


class TransactionEnvironment1Code(Enum):
    MERC = "MERC"
    PRIV = "PRIV"
    PUBL = "PUBL"


@dataclass(kw_only=True)
class TransactionIdentifier1:
    tx_dt_tm: XmlDateTime = field(
        metadata={
            "name": "TxDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    tx_ref: str = field(
        metadata={
            "name": "TxRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


class UnitOfMeasure1Code(Enum):
    PIEC = "PIEC"
    TONS = "TONS"
    FOOT = "FOOT"
    GBGA = "GBGA"
    USGA = "USGA"
    GRAM = "GRAM"
    INCH = "INCH"
    KILO = "KILO"
    PUND = "PUND"
    METR = "METR"
    CMET = "CMET"
    MMET = "MMET"
    LITR = "LITR"
    CELI = "CELI"
    MILI = "MILI"
    GBOU = "GBOU"
    USOU = "USOU"
    GBQA = "GBQA"
    USQA = "USQA"
    GBPI = "GBPI"
    USPI = "USPI"
    MILE = "MILE"
    KMET = "KMET"
    YARD = "YARD"
    SQKI = "SQKI"
    HECT = "HECT"
    ARES = "ARES"
    SMET = "SMET"
    SCMT = "SCMT"
    SMIL = "SMIL"
    SQMI = "SQMI"
    SQYA = "SQYA"
    SQFO = "SQFO"
    SQIN = "SQIN"
    ACRE = "ACRE"


class UserInterface2Code(Enum):
    MDSP = "MDSP"
    CDSP = "CDSP"


@dataclass(kw_only=True)
class AmountAndCurrencyExchangeDetails3:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    ccy_xchg: None | CurrencyExchange5 = field(
        default=None,
        metadata={
            "name": "CcyXchg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class AmountAndCurrencyExchangeDetails4:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    ccy_xchg: None | CurrencyExchange5 = field(
        default=None,
        metadata={
            "name": "CcyXchg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class AmountAndDirection35:
    amt: Decimal = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 17,
        }
    )
    cdt_dbt_ind: CreditDebitCode = field(
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class BankTransactionCodeStructure5:
    cd: str = field(
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 4,
        }
    )
    fmly: BankTransactionCodeStructure6 = field(
        metadata={
            "name": "Fmly",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class BatchInformation2:
    msg_id: None | str = field(
        default=None,
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pmt_inf_id: None | str = field(
        default=None,
        metadata={
            "name": "PmtInfId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nb_of_txs: None | str = field(
        default=None,
        metadata={
            "name": "NbOfTxs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]{1,15}",
        },
    )
    ttl_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class CardSecurityInformation1:
    cscmgmt: Cscmanagement1Code = field(
        metadata={
            "name": "CSCMgmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    cscval: None | str = field(
        default=None,
        metadata={
            "name": "CSCVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]{3,4}",
        },
    )


@dataclass(kw_only=True)
class CardholderAuthentication2:
    authntcn_mtd: AuthenticationMethod1Code = field(
        metadata={
            "name": "AuthntcnMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    authntcn_ntty: AuthenticationEntity1Code = field(
        metadata={
            "name": "AuthntcnNtty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CashAvailability1:
    dt: CashAvailabilityDate1Choice = field(
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    cdt_dbt_ind: CreditDebitCode = field(
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CashDeposit1:
    note_dnmtn: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "NoteDnmtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    nb_of_notes: str = field(
        metadata={
            "name": "NbOfNotes",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "pattern": r"[0-9]{1,15}",
        }
    )
    amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ChargeType3Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class ClearingSystemMemberIdentification2:
    clr_sys_id: None | ClearingSystemIdentification2Choice = field(
        default=None,
        metadata={
            "name": "ClrSysId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    mmb_id: str = field(
        metadata={
            "name": "MmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class ContactDetails2:
    nm_prfx: None | NamePrefix1Code = field(
        default=None,
        metadata={
            "name": "NmPrfx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )
    phne_nb: None | str = field(
        default=None,
        metadata={
            "name": "PhneNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    mob_nb: None | str = field(
        default=None,
        metadata={
            "name": "MobNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    fax_nb: None | str = field(
        default=None,
        metadata={
            "name": "FaxNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    email_adr: None | str = field(
        default=None,
        metadata={
            "name": "EmailAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 2048,
        },
    )
    othr: None | str = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceType1Choice:
    cd: None | DocumentType3Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DateOrDateTimePeriodChoice:
    dt: None | DatePeriodDetails = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dt_tm: None | DateTimePeriodDetails = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class DiscountAmountAndType1:
    tp: None | DiscountAmountType1Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DisplayCapabilities1:
    disp_tp: UserInterface2Code = field(
        metadata={
            "name": "DispTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    nb_of_lines: str = field(
        metadata={
            "name": "NbOfLines",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "pattern": r"[0-9]{1,3}",
        }
    )
    line_width: str = field(
        metadata={
            "name": "LineWidth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "pattern": r"[0-9]{1,3}",
        }
    )


@dataclass(kw_only=True)
class DocumentAdjustment1:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rsn: None | str = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class DocumentLineType1:
    cd_or_prtry: DocumentLineType1Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class FromToAmountRange:
    fr_amt: AmountRangeBoundary1 = field(
        metadata={
            "name": "FrAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    to_amt: AmountRangeBoundary1 = field(
        metadata={
            "name": "ToAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class GarnishmentType1:
    cd_or_prtry: GarnishmentType1Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericAccountIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification32:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tp: None | PartyType3Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    issr: None | PartyType4Code = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    shrt_nm: None | str = field(
        default=None,
        metadata={
            "name": "ShrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericOrganisationIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | OrganisationIdentificationSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericPersonIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | PersonIdentificationSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class InterestType1Choice:
    cd: None | InterestType1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 16,
        },
    )
    tp: IdentificationSource3Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class PointOfInteractionComponent1:
    poicmpnt_tp: PoicomponentType1Code = field(
        metadata={
            "name": "POICmpntTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    manfctr_id: None | str = field(
        default=None,
        metadata={
            "name": "ManfctrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    mdl: None | str = field(
        default=None,
        metadata={
            "name": "Mdl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    vrsn_nb: None | str = field(
        default=None,
        metadata={
            "name": "VrsnNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 16,
        },
    )
    srl_nb: None | str = field(
        default=None,
        metadata={
            "name": "SrlNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    apprvl_nb: list[str] = field(
        default_factory=list,
        metadata={
            "name": "ApprvlNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class PostalAddress6:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dept: None | str = field(
        default=None,
        metadata={
            "name": "Dept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 70,
        },
    )
    sub_dept: None | str = field(
        default=None,
        metadata={
            "name": "SubDept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 70,
        },
    )
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "max_occurs": 7,
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class PriceRateOrAmountChoice:
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    amt: None | ActiveOrHistoricCurrencyAnd13DecimalAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class Product2:
    pdct_cd: str = field(
        metadata={
            "name": "PdctCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    unit_of_measr: None | UnitOfMeasure1Code = field(
        default=None,
        metadata={
            "name": "UnitOfMeasr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    pdct_qty: None | Decimal = field(
        default=None,
        metadata={
            "name": "PdctQty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    unit_pric: None | Decimal = field(
        default=None,
        metadata={
            "name": "UnitPric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )
    pdct_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "PdctAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )
    tax_tp: None | str = field(
        default=None,
        metadata={
            "name": "TaxTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    addtl_pdct_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlPdctInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ProprietaryDate2:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    dt: DateAndDateTimeChoice = field(
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ProprietaryPrice2:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    pric: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Pric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ReferredDocumentType3Choice:
    cd: None | DocumentType6Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class TaxAmountAndType1:
    tp: None | TaxAmountType1Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class TaxCharges2:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TaxParty2:
    tax_id: None | str = field(
        default=None,
        metadata={
            "name": "TaxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    regn_id: None | str = field(
        default=None,
        metadata={
            "name": "RegnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_tp: None | str = field(
        default=None,
        metadata={
            "name": "TaxTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    authstn: None | TaxAuthorisation1 = field(
        default=None,
        metadata={
            "name": "Authstn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TaxPeriod1:
    yr: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Yr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tp: None | TaxRecordPeriod1Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    fr_to_dt: None | DatePeriodDetails = field(
        default=None,
        metadata={
            "name": "FrToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TransactionQuantities2Choice:
    qty: None | FinancialInstrumentQuantityChoice = field(
        default=None,
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    orgnl_and_cur_face_amt: None | OriginalAndCurrentQuantities1 = field(
        default=None,
        metadata={
            "name": "OrgnlAndCurFaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry: None | ProprietaryQuantity1 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TransactionReferences3:
    msg_id: None | str = field(
        default=None,
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    acct_svcr_ref: None | str = field(
        default=None,
        metadata={
            "name": "AcctSvcrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pmt_inf_id: None | str = field(
        default=None,
        metadata={
            "name": "PmtInfId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    instr_id: None | str = field(
        default=None,
        metadata={
            "name": "InstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    end_to_end_id: None | str = field(
        default=None,
        metadata={
            "name": "EndToEndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tx_id: None | str = field(
        default=None,
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "MndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    chq_nb: None | str = field(
        default=None,
        metadata={
            "name": "ChqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    clr_sys_ref: None | str = field(
        default=None,
        metadata={
            "name": "ClrSysRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    acct_ownr_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "AcctOwnrTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    acct_svcr_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "AcctSvcrTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    mkt_infrstrctr_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "MktInfrstrctrTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prcg_id: None | str = field(
        default=None,
        metadata={
            "name": "PrcgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: list[ProprietaryReference1] = field(
        default_factory=list,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class YieldedOrValueType1Choice:
    yldd: None | bool = field(
        default=None,
        metadata={
            "name": "Yldd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    val_tp: None | PriceValueType1Code = field(
        default=None,
        metadata={
            "name": "ValTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class AccountIdentification4Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    othr: None | GenericAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class AmountAndCurrencyExchange3:
    instd_amt: None | AmountAndCurrencyExchangeDetails3 = field(
        default=None,
        metadata={
            "name": "InstdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tx_amt: None | AmountAndCurrencyExchangeDetails3 = field(
        default=None,
        metadata={
            "name": "TxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cntr_val_amt: None | AmountAndCurrencyExchangeDetails3 = field(
        default=None,
        metadata={
            "name": "CntrValAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    anncd_pstng_amt: None | AmountAndCurrencyExchangeDetails3 = field(
        default=None,
        metadata={
            "name": "AnncdPstngAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry_amt: list[AmountAndCurrencyExchangeDetails4] = field(
        default_factory=list,
        metadata={
            "name": "PrtryAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class BankTransactionCodeStructure4:
    domn: None | BankTransactionCodeStructure5 = field(
        default=None,
        metadata={
            "name": "Domn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry: None | ProprietaryBankTransactionCodeStructure1 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class BranchData2:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress6 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class CardAggregated1:
    addtl_svc: None | CardPaymentServiceType2Code = field(
        default=None,
        metadata={
            "name": "AddtlSvc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tx_ctgy: None | str = field(
        default=None,
        metadata={
            "name": "TxCtgy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    sale_rcncltn_id: None | str = field(
        default=None,
        metadata={
            "name": "SaleRcncltnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    seq_nb_rg: None | CardSequenceNumberRange1 = field(
        default=None,
        metadata={
            "name": "SeqNbRg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tx_dt_rg: None | DateOrDateTimePeriodChoice = field(
        default=None,
        metadata={
            "name": "TxDtRg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceType2:
    cd_or_prtry: CreditorReferenceType1Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DocumentLineIdentification1:
    tp: None | DocumentLineType1 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    nb: None | str = field(
        default=None,
        metadata={
            "name": "Nb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rltd_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "RltdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification8:
    bicfi: None | str = field(
        default=None,
        metadata={
            "name": "BICFI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification2 = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress6 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    othr: None | GenericFinancialIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class ImpliedCurrencyAmountRangeChoice:
    fr_amt: None | AmountRangeBoundary1 = field(
        default=None,
        metadata={
            "name": "FrAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    to_amt: None | AmountRangeBoundary1 = field(
        default=None,
        metadata={
            "name": "ToAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    fr_to_amt: None | FromToAmountRange = field(
        default=None,
        metadata={
            "name": "FrToAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    eqamt: None | Decimal = field(
        default=None,
        metadata={
            "name": "EQAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )
    neqamt: None | Decimal = field(
        default=None,
        metadata={
            "name": "NEQAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )


@dataclass(kw_only=True)
class NameAndAddress10:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 140,
        }
    )
    adr: PostalAddress6 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class NumberAndSumOfTransactions4:
    nb_of_ntries: None | str = field(
        default=None,
        metadata={
            "name": "NbOfNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]{1,15}",
        },
    )
    sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    ttl_net_ntry: None | AmountAndDirection35 = field(
        default=None,
        metadata={
            "name": "TtlNetNtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class OrganisationIdentification8:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    othr: list[GenericOrganisationIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class PaymentContext3:
    card_pres: None | bool = field(
        default=None,
        metadata={
            "name": "CardPres",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    crdhldr_pres: None | bool = field(
        default=None,
        metadata={
            "name": "CrdhldrPres",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    on_line_cntxt: None | bool = field(
        default=None,
        metadata={
            "name": "OnLineCntxt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    attndnc_cntxt: None | AttendanceContext1Code = field(
        default=None,
        metadata={
            "name": "AttndncCntxt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tx_envt: None | TransactionEnvironment1Code = field(
        default=None,
        metadata={
            "name": "TxEnvt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tx_chanl: None | TransactionChannel1Code = field(
        default=None,
        metadata={
            "name": "TxChanl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    attndnt_msg_cpbl: None | bool = field(
        default=None,
        metadata={
            "name": "AttndntMsgCpbl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    attndnt_lang: None | str = field(
        default=None,
        metadata={
            "name": "AttndntLang",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[a-z]{2,2}",
        },
    )
    card_data_ntry_md: CardDataReading1Code = field(
        metadata={
            "name": "CardDataNtryMd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    fllbck_ind: None | bool = field(
        default=None,
        metadata={
            "name": "FllbckInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    authntcn_mtd: None | CardholderAuthentication2 = field(
        default=None,
        metadata={
            "name": "AuthntcnMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class PersonIdentification5:
    dt_and_plc_of_birth: None | DateAndPlaceOfBirth = field(
        default=None,
        metadata={
            "name": "DtAndPlcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    othr: list[GenericPersonIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class PlainCardData1:
    pan: str = field(
        metadata={
            "name": "PAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "pattern": r"[0-9]{8,28}",
        }
    )
    card_seq_nb: None | str = field(
        default=None,
        metadata={
            "name": "CardSeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]{2,3}",
        },
    )
    fctv_dt: None | XmlPeriod = field(
        default=None,
        metadata={
            "name": "FctvDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    xpry_dt: XmlPeriod = field(
        metadata={
            "name": "XpryDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    svc_cd: None | str = field(
        default=None,
        metadata={
            "name": "SvcCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]{3}",
        },
    )
    trck_data: list[TrackData1] = field(
        default_factory=list,
        metadata={
            "name": "TrckData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    card_scty_cd: None | CardSecurityInformation1 = field(
        default=None,
        metadata={
            "name": "CardSctyCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class PointOfInteractionCapabilities1:
    card_rdng_cpblties: list[CardDataReading1Code] = field(
        default_factory=list,
        metadata={
            "name": "CardRdngCpblties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    crdhldr_vrfctn_cpblties: list[CardholderVerificationCapability1Code] = (
        field(
            default_factory=list,
            metadata={
                "name": "CrdhldrVrfctnCpblties",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            },
        )
    )
    on_line_cpblties: None | OnLineCapability1Code = field(
        default=None,
        metadata={
            "name": "OnLineCpblties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    disp_cpblties: list[DisplayCapabilities1] = field(
        default_factory=list,
        metadata={
            "name": "DispCpblties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prt_line_width: None | str = field(
        default=None,
        metadata={
            "name": "PrtLineWidth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]{1,3}",
        },
    )


@dataclass(kw_only=True)
class Price2:
    tp: YieldedOrValueType1Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    val: PriceRateOrAmountChoice = field(
        metadata={
            "name": "Val",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ReferredDocumentType4:
    cd_or_prtry: ReferredDocumentType3Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class RemittanceAmount2:
    due_pybl_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DuePyblAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dscnt_apld_amt: list[DiscountAmountAndType1] = field(
        default_factory=list,
        metadata={
            "name": "DscntApldAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cdt_note_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CdtNoteAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tax_amt: list[TaxAmountAndType1] = field(
        default_factory=list,
        metadata={
            "name": "TaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    adjstmnt_amt_and_rsn: list[DocumentAdjustment1] = field(
        default_factory=list,
        metadata={
            "name": "AdjstmntAmtAndRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rmtd_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RmtdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class RemittanceAmount3:
    due_pybl_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DuePyblAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dscnt_apld_amt: list[DiscountAmountAndType1] = field(
        default_factory=list,
        metadata={
            "name": "DscntApldAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cdt_note_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CdtNoteAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tax_amt: list[TaxAmountAndType1] = field(
        default_factory=list,
        metadata={
            "name": "TaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    adjstmnt_amt_and_rsn: list[DocumentAdjustment1] = field(
        default_factory=list,
        metadata={
            "name": "AdjstmntAmtAndRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rmtd_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RmtdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class SecurityIdentification19:
    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{2,2}[A-Z0-9]{9,9}[0-9]{1,1}",
        },
    )
    othr_id: list[OtherIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class TaxRecordDetails1:
    prd: None | TaxPeriod1 = field(
        default=None,
        metadata={
            "name": "Prd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class TransactionDates2:
    accptnc_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "AccptncDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    trad_actvty_ctrctl_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "TradActvtyCtrctlSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    trad_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "TradDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    start_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "StartDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    end_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "EndDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tx_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "TxDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry: list[ProprietaryDate2] = field(
        default_factory=list,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification5:
    fin_instn_id: FinancialInstitutionIdentification8 = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    brnch_id: None | BranchData2 = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class CardIndividualTransaction2:
    iccrltd_data: None | str = field(
        default=None,
        metadata={
            "name": "ICCRltdData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 1025,
        },
    )
    pmt_cntxt: None | PaymentContext3 = field(
        default=None,
        metadata={
            "name": "PmtCntxt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_svc: None | CardPaymentServiceType2Code = field(
        default=None,
        metadata={
            "name": "AddtlSvc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tx_ctgy: None | str = field(
        default=None,
        metadata={
            "name": "TxCtgy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    sale_rcncltn_id: None | str = field(
        default=None,
        metadata={
            "name": "SaleRcncltnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    sale_ref_nb: None | str = field(
        default=None,
        metadata={
            "name": "SaleRefNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    re_presntmnt_rsn: None | str = field(
        default=None,
        metadata={
            "name": "RePresntmntRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 4,
        },
    )
    seq_nb: None | str = field(
        default=None,
        metadata={
            "name": "SeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tx_id: None | TransactionIdentifier1 = field(
        default=None,
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    pdct: None | Product2 = field(
        default=None,
        metadata={
            "name": "Pdct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    vldtn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "VldtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    vldtn_seq_nb: None | str = field(
        default=None,
        metadata={
            "name": "VldtnSeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CashAccount24:
    id: AccountIdentification4Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    tp: None | CashAccountType2Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceInformation2:
    tp: None | CreditorReferenceType2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ref: None | str = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CurrencyAndAmountRange2:
    amt: ImpliedCurrencyAmountRangeChoice = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ccy: str = field(
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )


@dataclass(kw_only=True)
class DocumentLineInformation1:
    id: list[DocumentLineIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_occurs": 1,
        },
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 2048,
        },
    )
    amt: None | RemittanceAmount3 = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class Party11Choice:
    org_id: None | OrganisationIdentification8 = field(
        default=None,
        metadata={
            "name": "OrgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prvt_id: None | PersonIdentification5 = field(
        default=None,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class PaymentCard4:
    plain_card_data: None | PlainCardData1 = field(
        default=None,
        metadata={
            "name": "PlainCardData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    card_ctry_cd: None | str = field(
        default=None,
        metadata={
            "name": "CardCtryCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]{3}",
        },
    )
    card_brnd: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "CardBrnd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_card_data: None | str = field(
        default=None,
        metadata={
            "name": "AddtlCardData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class PointOfInteraction1:
    id: GenericIdentification32 = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    sys_nm: None | str = field(
        default=None,
        metadata={
            "name": "SysNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 70,
        },
    )
    grp_id: None | str = field(
        default=None,
        metadata={
            "name": "GrpId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cpblties: None | PointOfInteractionCapabilities1 = field(
        default=None,
        metadata={
            "name": "Cpblties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cmpnt: list[PointOfInteractionComponent1] = field(
        default_factory=list,
        metadata={
            "name": "Cmpnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class RemittanceLocationDetails1:
    mtd: RemittanceLocationMethod2Code = field(
        metadata={
            "name": "Mtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    elctrnc_adr: None | str = field(
        default=None,
        metadata={
            "name": "ElctrncAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 2048,
        },
    )
    pstl_adr: None | NameAndAddress10 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TaxAmount1:
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    taxbl_base_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TaxblBaseAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ttl_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dtls: list[TaxRecordDetails1] = field(
        default_factory=list,
        metadata={
            "name": "Dtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TotalsPerBankTransactionCode4:
    nb_of_ntries: None | str = field(
        default=None,
        metadata={
            "name": "NbOfNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[0-9]{1,15}",
        },
    )
    sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    ttl_net_ntry: None | AmountAndDirection35 = field(
        default=None,
        metadata={
            "name": "TtlNetNtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    fcst_ind: None | bool = field(
        default=None,
        metadata={
            "name": "FcstInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    bk_tx_cd: BankTransactionCodeStructure4 = field(
        metadata={
            "name": "BkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    avlbty: list[CashAvailability1] = field(
        default_factory=list,
        metadata={
            "name": "Avlbty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TransactionPrice3Choice:
    deal_pric: None | Price2 = field(
        default=None,
        metadata={
            "name": "DealPric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry: list[ProprietaryPrice2] = field(
        default_factory=list,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class CardEntry2:
    card: None | PaymentCard4 = field(
        default=None,
        metadata={
            "name": "Card",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    poi: None | PointOfInteraction1 = field(
        default=None,
        metadata={
            "name": "POI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    aggtd_ntry: None | CardAggregated1 = field(
        default=None,
        metadata={
            "name": "AggtdNtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    pre_pd_acct: None | CashAccount24 = field(
        default=None,
        metadata={
            "name": "PrePdAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class CardTransaction2Choice:
    aggtd: None | CardAggregated1 = field(
        default=None,
        metadata={
            "name": "Aggtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    indv: None | CardIndividualTransaction2 = field(
        default=None,
        metadata={
            "name": "Indv",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class ChargesRecord2:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    chrg_incl_ind: None | bool = field(
        default=None,
        metadata={
            "name": "ChrgInclInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tp: None | ChargeType3Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    br: None | ChargeBearerType1Code = field(
        default=None,
        metadata={
            "name": "Br",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    agt: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "Agt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tax: None | TaxCharges2 = field(
        default=None,
        metadata={
            "name": "Tax",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification43:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress6 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    id: None | Party11Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ctry_of_res: None | str = field(
        default=None,
        metadata={
            "name": "CtryOfRes",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    ctct_dtls: None | ContactDetails2 = field(
        default=None,
        metadata={
            "name": "CtctDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class ProprietaryAgent3:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    agt: BranchAndFinancialInstitutionIdentification5 = field(
        metadata={
            "name": "Agt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Rate3:
    tp: RateType4Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    vldty_rg: None | CurrencyAndAmountRange2 = field(
        default=None,
        metadata={
            "name": "VldtyRg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentInformation7:
    tp: None | ReferredDocumentType4 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    nb: None | str = field(
        default=None,
        metadata={
            "name": "Nb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rltd_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "RltdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    line_dtls: list[DocumentLineInformation1] = field(
        default_factory=list,
        metadata={
            "name": "LineDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class RemittanceLocation4:
    rmt_id: None | str = field(
        default=None,
        metadata={
            "name": "RmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rmt_lctn_dtls: list[RemittanceLocationDetails1] = field(
        default_factory=list,
        metadata={
            "name": "RmtLctnDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TaxRecord1:
    tp: None | str = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctgy: None | str = field(
        default=None,
        metadata={
            "name": "Ctgy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctgy_dtls: None | str = field(
        default=None,
        metadata={
            "name": "CtgyDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dbtr_sts: None | str = field(
        default=None,
        metadata={
            "name": "DbtrSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cert_id: None | str = field(
        default=None,
        metadata={
            "name": "CertId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    frms_cd: None | str = field(
        default=None,
        metadata={
            "name": "FrmsCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prd: None | TaxPeriod1 = field(
        default=None,
        metadata={
            "name": "Prd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tax_amt: None | TaxAmount1 = field(
        default=None,
        metadata={
            "name": "TaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class TotalTransactions5:
    ttl_ntries: None | NumberAndSumOfTransactions4 = field(
        default=None,
        metadata={
            "name": "TtlNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ttl_cdt_ntries: None | NumberAndSumOfTransactions1 = field(
        default=None,
        metadata={
            "name": "TtlCdtNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ttl_dbt_ntries: None | NumberAndSumOfTransactions1 = field(
        default=None,
        metadata={
            "name": "TtlDbtNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ttl_ntries_per_bk_tx_cd: list[TotalsPerBankTransactionCode4] = field(
        default_factory=list,
        metadata={
            "name": "TtlNtriesPerBkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class AccountInterest3:
    tp: None | InterestType1Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rate: list[Rate3] = field(
        default_factory=list,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    fr_to_dt: None | DateTimePeriodDetails = field(
        default=None,
        metadata={
            "name": "FrToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rsn: None | str = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax: None | TaxCharges2 = field(
        default=None,
        metadata={
            "name": "Tax",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class CardTransaction2:
    card: None | PaymentCard4 = field(
        default=None,
        metadata={
            "name": "Card",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    poi: None | PointOfInteraction1 = field(
        default=None,
        metadata={
            "name": "POI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tx: None | CardTransaction2Choice = field(
        default=None,
        metadata={
            "name": "Tx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    pre_pd_acct: None | CashAccount24 = field(
        default=None,
        metadata={
            "name": "PrePdAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class CashAccount25:
    id: AccountIdentification4Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    tp: None | CashAccountType2Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 70,
        },
    )
    ownr: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "Ownr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    svcr: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "Svcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class Charges4:
    ttl_chrgs_and_tax_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlChrgsAndTaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rcrd: list[ChargesRecord2] = field(
        default_factory=list,
        metadata={
            "name": "Rcrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class Garnishment1:
    tp: GarnishmentType1 = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    grnshee: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "Grnshee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    grnshmt_admstr: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "GrnshmtAdmstr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ref_nb: None | str = field(
        default=None,
        metadata={
            "name": "RefNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rmtd_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RmtdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    fmly_mdcl_insrnc_ind: None | bool = field(
        default=None,
        metadata={
            "name": "FmlyMdclInsrncInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    mplyee_termntn_ind: None | bool = field(
        default=None,
        metadata={
            "name": "MplyeeTermntnInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class GroupHeader58:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    msg_rcpt: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "MsgRcpt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    msg_pgntn: None | Pagination = field(
        default=None,
        metadata={
            "name": "MsgPgntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    orgnl_biz_qry: None | OriginalBusinessQuery1 = field(
        default=None,
        metadata={
            "name": "OrgnlBizQry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 500,
        },
    )


@dataclass(kw_only=True)
class InterestRecord1:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    cdt_dbt_ind: CreditDebitCode = field(
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    tp: None | InterestType1Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rate: None | Rate3 = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    fr_to_dt: None | DateTimePeriodDetails = field(
        default=None,
        metadata={
            "name": "FrToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rsn: None | str = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax: None | TaxCharges2 = field(
        default=None,
        metadata={
            "name": "Tax",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class PaymentReturnReason2:
    orgnl_bk_tx_cd: None | BankTransactionCodeStructure4 = field(
        default=None,
        metadata={
            "name": "OrgnlBkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    orgtr: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "Orgtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rsn: None | ReturnReason5Choice = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_inf: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 105,
        },
    )


@dataclass(kw_only=True)
class ProprietaryParty3:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    pty: PartyIdentification43 = field(
        metadata={
            "name": "Pty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class TaxInformation3:
    cdtr: None | TaxParty1 = field(
        default=None,
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dbtr: None | TaxParty2 = field(
        default=None,
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    admstn_zn: None | str = field(
        default=None,
        metadata={
            "name": "AdmstnZn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ref_nb: None | str = field(
        default=None,
        metadata={
            "name": "RefNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )
    mtd: None | str = field(
        default=None,
        metadata={
            "name": "Mtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ttl_taxbl_base_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxblBaseAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ttl_tax_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    seq_nb: None | Decimal = field(
        default=None,
        metadata={
            "name": "SeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    rcrd: list[TaxRecord1] = field(
        default_factory=list,
        metadata={
            "name": "Rcrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TaxInformation4:
    cdtr: None | TaxParty1 = field(
        default=None,
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dbtr: None | TaxParty2 = field(
        default=None,
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ultmt_dbtr: None | TaxParty2 = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    admstn_zone: None | str = field(
        default=None,
        metadata={
            "name": "AdmstnZone",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ref_nb: None | str = field(
        default=None,
        metadata={
            "name": "RefNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )
    mtd: None | str = field(
        default=None,
        metadata={
            "name": "Mtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ttl_taxbl_base_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxblBaseAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ttl_tax_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    seq_nb: None | Decimal = field(
        default=None,
        metadata={
            "name": "SeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    rcrd: list[TaxRecord1] = field(
        default_factory=list,
        metadata={
            "name": "Rcrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TransactionAgents3:
    dbtr_agt: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "DbtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cdtr_agt: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "CdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    intrmy_agt1: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt1",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    intrmy_agt2: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt2",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    intrmy_agt3: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt3",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rcvg_agt: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "RcvgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dlvrg_agt: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "DlvrgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    issg_agt: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "IssgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    sttlm_plc: None | BranchAndFinancialInstitutionIdentification5 = field(
        default=None,
        metadata={
            "name": "SttlmPlc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry: list[ProprietaryAgent3] = field(
        default_factory=list,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class StructuredRemittanceInformation13:
    rfrd_doc_inf: list[ReferredDocumentInformation7] = field(
        default_factory=list,
        metadata={
            "name": "RfrdDocInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rfrd_doc_amt: None | RemittanceAmount2 = field(
        default=None,
        metadata={
            "name": "RfrdDocAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cdtr_ref_inf: None | CreditorReferenceInformation2 = field(
        default=None,
        metadata={
            "name": "CdtrRefInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    invcr: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "Invcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    invcee: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "Invcee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tax_rmt: None | TaxInformation4 = field(
        default=None,
        metadata={
            "name": "TaxRmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    grnshmt_rmt: None | Garnishment1 = field(
        default=None,
        metadata={
            "name": "GrnshmtRmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_rmt_inf: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AddtlRmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "max_occurs": 3,
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class TransactionInterest3:
    ttl_intrst_and_tax_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlIntrstAndTaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rcrd: list[InterestRecord1] = field(
        default_factory=list,
        metadata={
            "name": "Rcrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class TransactionParties3:
    initg_pty: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "InitgPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dbtr: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    dbtr_acct: None | CashAccount24 = field(
        default=None,
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ultmt_dbtr: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cdtr: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cdtr_acct: None | CashAccount24 = field(
        default=None,
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ultmt_cdtr: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "UltmtCdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tradg_pty: None | PartyIdentification43 = field(
        default=None,
        metadata={
            "name": "TradgPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    prtry: list[ProprietaryParty3] = field(
        default_factory=list,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class RemittanceInformation11:
    ustrd: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 140,
        },
    )
    strd: list[StructuredRemittanceInformation13] = field(
        default_factory=list,
        metadata={
            "name": "Strd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class EntryTransaction8:
    refs: None | TransactionReferences3 = field(
        default=None,
        metadata={
            "name": "Refs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    cdt_dbt_ind: CreditDebitCode = field(
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    amt_dtls: None | AmountAndCurrencyExchange3 = field(
        default=None,
        metadata={
            "name": "AmtDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    avlbty: list[CashAvailability1] = field(
        default_factory=list,
        metadata={
            "name": "Avlbty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    bk_tx_cd: None | BankTransactionCodeStructure4 = field(
        default=None,
        metadata={
            "name": "BkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    chrgs: None | Charges4 = field(
        default=None,
        metadata={
            "name": "Chrgs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    intrst: None | TransactionInterest3 = field(
        default=None,
        metadata={
            "name": "Intrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rltd_pties: None | TransactionParties3 = field(
        default=None,
        metadata={
            "name": "RltdPties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rltd_agts: None | TransactionAgents3 = field(
        default=None,
        metadata={
            "name": "RltdAgts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    purp: None | Purpose2Choice = field(
        default=None,
        metadata={
            "name": "Purp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rltd_rmt_inf: list[RemittanceLocation4] = field(
        default_factory=list,
        metadata={
            "name": "RltdRmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "max_occurs": 10,
        },
    )
    rmt_inf: None | RemittanceInformation11 = field(
        default=None,
        metadata={
            "name": "RmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rltd_dts: None | TransactionDates2 = field(
        default=None,
        metadata={
            "name": "RltdDts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rltd_pric: None | TransactionPrice3Choice = field(
        default=None,
        metadata={
            "name": "RltdPric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rltd_qties: list[TransactionQuantities2Choice] = field(
        default_factory=list,
        metadata={
            "name": "RltdQties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    fin_instrm_id: None | SecurityIdentification19 = field(
        default=None,
        metadata={
            "name": "FinInstrmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tax: None | TaxInformation3 = field(
        default=None,
        metadata={
            "name": "Tax",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rtr_inf: None | PaymentReturnReason2 = field(
        default=None,
        metadata={
            "name": "RtrInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    corp_actn: None | CorporateAction9 = field(
        default=None,
        metadata={
            "name": "CorpActn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    sfkpg_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    csh_dpst: list[CashDeposit1] = field(
        default_factory=list,
        metadata={
            "name": "CshDpst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    card_tx: None | CardTransaction2 = field(
        default=None,
        metadata={
            "name": "CardTx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_tx_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlTxInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 500,
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class EntryDetails7:
    btch: None | BatchInformation2 = field(
        default=None,
        metadata={
            "name": "Btch",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tx_dtls: list[EntryTransaction8] = field(
        default_factory=list,
        metadata={
            "name": "TxDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class ReportEntry8:
    ntry_ref: None | str = field(
        default=None,
        metadata={
            "name": "NtryRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    cdt_dbt_ind: CreditDebitCode = field(
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    rvsl_ind: None | bool = field(
        default=None,
        metadata={
            "name": "RvslInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    sts: EntryStatus2Code = field(
        metadata={
            "name": "Sts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    bookg_dt: None | DateAndDateTimeChoice = field(
        default=None,
        metadata={
            "name": "BookgDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    val_dt: None | DateAndDateTimeChoice = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    acct_svcr_ref: None | str = field(
        default=None,
        metadata={
            "name": "AcctSvcrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 35,
        },
    )
    avlbty: list[CashAvailability1] = field(
        default_factory=list,
        metadata={
            "name": "Avlbty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    bk_tx_cd: BankTransactionCodeStructure4 = field(
        metadata={
            "name": "BkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    comssn_wvr_ind: None | bool = field(
        default=None,
        metadata={
            "name": "ComssnWvrInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_inf_ind: None | MessageIdentification2 = field(
        default=None,
        metadata={
            "name": "AddtlInfInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    amt_dtls: None | AmountAndCurrencyExchange3 = field(
        default=None,
        metadata={
            "name": "AmtDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    chrgs: None | Charges4 = field(
        default=None,
        metadata={
            "name": "Chrgs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    tech_inpt_chanl: None | TechnicalInputChannel1Choice = field(
        default=None,
        metadata={
            "name": "TechInptChanl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    intrst: None | TransactionInterest3 = field(
        default=None,
        metadata={
            "name": "Intrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    card_tx: None | CardEntry2 = field(
        default=None,
        metadata={
            "name": "CardTx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ntry_dtls: list[EntryDetails7] = field(
        default_factory=list,
        metadata={
            "name": "NtryDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_ntry_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlNtryInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 500,
        },
    )


@dataclass(kw_only=True)
class AccountNotification12:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ntfctn_pgntn: None | Pagination = field(
        default=None,
        metadata={
            "name": "NtfctnPgntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    elctrnc_seq_nb: None | Decimal = field(
        default=None,
        metadata={
            "name": "ElctrncSeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    lgl_seq_nb: None | Decimal = field(
        default=None,
        metadata={
            "name": "LglSeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    fr_to_dt: None | DateTimePeriodDetails = field(
        default=None,
        metadata={
            "name": "FrToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    cpy_dplct_ind: None | CopyDuplicate1Code = field(
        default=None,
        metadata={
            "name": "CpyDplctInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    rptg_src: None | ReportingSource1Choice = field(
        default=None,
        metadata={
            "name": "RptgSrc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    acct: CashAccount25 = field(
        metadata={
            "name": "Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    rltd_acct: None | CashAccount24 = field(
        default=None,
        metadata={
            "name": "RltdAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    intrst: list[AccountInterest3] = field(
        default_factory=list,
        metadata={
            "name": "Intrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    txs_summry: None | TotalTransactions5 = field(
        default=None,
        metadata={
            "name": "TxsSummry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    ntry: list[ReportEntry8] = field(
        default_factory=list,
        metadata={
            "name": "Ntry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )
    addtl_ntfctn_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlNtfctnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_length": 1,
            "max_length": 500,
        },
    )


@dataclass(kw_only=True)
class BankToCustomerDebitCreditNotificationV06:
    grp_hdr: GroupHeader58 = field(
        metadata={
            "name": "GrpHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "required": True,
        }
    )
    ntfctn: list[AccountNotification12] = field(
        default_factory=list,
        metadata={
            "name": "Ntfctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
            "min_occurs": 1,
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:camt.054.001.06"

    bk_to_cstmr_dbt_cdt_ntfctn: BankToCustomerDebitCreditNotificationV06 = (
        field(
            metadata={
                "name": "BkToCstmrDbtCdtNtfctn",
                "type": "Element",
                "required": True,
            }
        )
    )
