from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01"


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


@dataclass(kw_only=True)
class AlternateSecurityIdentification2:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class AmountRangeBoundary1:
    bdry_amt: Decimal = field(
        metadata={
            "name": "BdryAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


class BalanceType9Code(Enum):
    OPBD = "OPBD"
    ITBD = "ITBD"
    CLBD = "CLBD"
    OPAV = "OPAV"
    ITAV = "ITAV"
    CLAV = "CLAV"
    FWAV = "FWAV"
    PRCD = "PRCD"
    IOPA = "IOPA"
    IITA = "IITA"
    ICLA = "ICLA"
    IFWA = "IFWA"
    ICLB = "ICLB"
    IITB = "IITB"
    IOPB = "IOPB"
    DOPA = "DOPA"
    DITA = "DITA"
    DCLA = "DCLA"
    DFWA = "DFWA"
    DCLB = "DCLB"
    DITB = "DITB"
    DOPB = "DOPB"
    COPA = "COPA"
    CITA = "CITA"
    CCLA = "CCLA"
    CFWA = "CFWA"
    CCLB = "CCLB"
    CITB = "CITB"
    COPB = "COPB"


@dataclass(kw_only=True)
class BankTransactionCodeStructure3:
    cd: str = field(
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 4,
        }
    )
    sub_fmly_cd: str = field(
        metadata={
            "name": "SubFmlyCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 4,
        }
    )


@dataclass(kw_only=True)
class BatchInformation1:
    msg_id: None | str = field(
        default=None,
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pmt_inf_id: None | str = field(
        default=None,
        metadata={
            "name": "PmtInfId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nb_of_txs: None | str = field(
        default=None,
        metadata={
            "name": "NbOfTxs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[0-9]{1,15}",
        },
    )


class CashAccountType4Code(Enum):
    CASH = "CASH"
    CHAR = "CHAR"
    COMM = "COMM"
    TAXE = "TAXE"
    CISH = "CISH"
    TRAS = "TRAS"
    SACC = "SACC"
    CACC = "CACC"
    SVGS = "SVGS"
    ONDP = "ONDP"
    MGLD = "MGLD"
    NREX = "NREX"
    MOMA = "MOMA"
    LOAN = "LOAN"
    SLRY = "SLRY"
    ODFT = "ODFT"


@dataclass(kw_only=True)
class CashBalanceAvailabilityDate1:
    nb_of_days: None | str = field(
        default=None,
        metadata={
            "name": "NbOfDays",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[+]{0,1}[0-9]{1,15}",
        },
    )
    actl_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ActlDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


class ChargeBearerType1Code(Enum):
    DEBT = "DEBT"
    CRED = "CRED"
    SHAR = "SHAR"
    SLEV = "SLEV"


class ChargeType1Code(Enum):
    BRKF = "BRKF"
    COMM = "COMM"


@dataclass(kw_only=True)
class ClearingSystemMemberIdentification3Choice:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


class CopyDuplicate1Code(Enum):
    CODU = "CODU"
    COPY = "COPY"
    DUPL = "DUPL"


@dataclass(kw_only=True)
class CorporateAction1:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nb: None | str = field(
        default=None,
        metadata={
            "name": "Nb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


class CreditDebitCode(Enum):
    CRDT = "CRDT"
    DBIT = "DBIT"


@dataclass(kw_only=True)
class CurrencyAndAmount:
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
class CurrencyExchange3:
    src_ccy: str = field(
        metadata={
            "name": "SrcCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    trgt_ccy: None | str = field(
        default=None,
        metadata={
            "name": "TrgtCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    unit_ccy: None | str = field(
        default=None,
        metadata={
            "name": "UnitCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    xchg_rate: Decimal = field(
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    qtn_dt: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "QtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class DateAndDateTimeChoice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class DateAndPlaceOfBirth:
    birth_dt: XmlDate = field(
        metadata={
            "name": "BirthDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    prvc_of_birth: None | str = field(
        default=None,
        metadata={
            "name": "PrvcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    city_of_birth: str = field(
        metadata={
            "name": "CityOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_of_birth: str = field(
        metadata={
            "name": "CtryOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class DateTimePeriodDetails:
    fr_dt_tm: XmlDateTime = field(
        metadata={
            "name": "FrDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    to_dt_tm: XmlDateTime = field(
        metadata={
            "name": "ToDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


class DocumentType2Code(Enum):
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


class DocumentType3Code(Enum):
    RADM = "RADM"
    RPIN = "RPIN"
    FXDR = "FXDR"
    DISP = "DISP"
    PUOR = "PUOR"
    SCOR = "SCOR"


class EntryStatus3Code(Enum):
    BOOK = "BOOK"


@dataclass(kw_only=True)
class FinancialInstrumentQuantityChoice:
    unit: None | Decimal = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    face_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "FaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification4:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    id_tp: str = field(
        metadata={
            "name": "IdTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    msg_id: None | str = field(
        default=None,
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class NumberAndSumOfTransactions1:
    nb_of_ntries: None | str = field(
        default=None,
        metadata={
            "name": "NbOfNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[0-9]{1,15}",
        },
    )
    sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )


@dataclass(kw_only=True)
class Pagination:
    pg_nb: str = field(
        metadata={
            "name": "PgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "pattern": r"[0-9]{1,5}",
        }
    )
    last_pg_ind: bool = field(
        metadata={
            "name": "LastPgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ProprietaryBankTransactionCodeStructure1:
    cd: str = field(
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ProprietaryDate1:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class ProprietaryQuantity1:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    qty: str = field(
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ref: str = field(
        metadata={
            "name": "Ref",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class Purpose1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class RateTypeChoice:
    pctg_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "PctgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    txtl_rate: None | str = field(
        default=None,
        metadata={
            "name": "TxtlRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


class RemittanceLocationMethod1Code(Enum):
    FAXI = "FAXI"
    EDIC = "EDIC"
    URID = "URID"
    EMAL = "EMAL"
    POST = "POST"


@dataclass(kw_only=True)
class SimpleIdentificationInformation2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 34,
        }
    )


class TransactionRejectReason2Code(Enum):
    AC01 = "AC01"
    AC04 = "AC04"
    AC06 = "AC06"
    AM01 = "AM01"
    AM02 = "AM02"
    AM03 = "AM03"
    AM04 = "AM04"
    AM05 = "AM05"
    AM06 = "AM06"
    AM07 = "AM07"
    BE01 = "BE01"
    BE04 = "BE04"
    BE05 = "BE05"
    AG01 = "AG01"
    AG02 = "AG02"
    DT01 = "DT01"
    RF01 = "RF01"
    RC01 = "RC01"
    TM01 = "TM01"
    ED01 = "ED01"
    ED03 = "ED03"
    MS03 = "MS03"
    MS02 = "MS02"
    BE06 = "BE06"
    BE07 = "BE07"
    AM09 = "AM09"
    AM10 = "AM10"
    MD01 = "MD01"
    MD02 = "MD02"
    MD03 = "MD03"
    MD04 = "MD04"
    MD06 = "MD06"
    MD07 = "MD07"
    ED05 = "ED05"
    NARR = "NARR"


@dataclass(kw_only=True)
class AccountIdentification3Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[a-zA-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    bban: None | str = field(
        default=None,
        metadata={
            "name": "BBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[a-zA-Z0-9]{1,30}",
        },
    )
    upic: None | str = field(
        default=None,
        metadata={
            "name": "UPIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[0-9]{8,17}",
        },
    )
    prtry_acct: None | SimpleIdentificationInformation2 = field(
        default=None,
        metadata={
            "name": "PrtryAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class AmountAndCurrencyExchangeDetails1:
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    ccy_xchg: None | CurrencyExchange3 = field(
        default=None,
        metadata={
            "name": "CcyXchg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class AmountAndCurrencyExchangeDetails2:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    ccy_xchg: None | CurrencyExchange3 = field(
        default=None,
        metadata={
            "name": "CcyXchg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class BalanceType2Choice:
    cd: None | BalanceType9Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class BankTransactionCodeStructure2:
    cd: str = field(
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 4,
        }
    )
    fmly: BankTransactionCodeStructure3 = field(
        metadata={
            "name": "Fmly",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CashAccountType2:
    cd: None | CashAccountType4Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CashBalanceAvailability1:
    dt: CashBalanceAvailabilityDate1 = field(
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    cdt_dbt_ind: CreditDebitCode = field(
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ChargeTypeChoice:
    cd: None | ChargeType1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry_cd: None | str = field(
        default=None,
        metadata={
            "name": "PrtryCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[a-zA-Z0-9]{1,4}",
        },
    )


@dataclass(kw_only=True)
class CreditLine1:
    incl: bool = field(
        metadata={
            "name": "Incl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceType1:
    cd: None | DocumentType3Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    to_amt: AmountRangeBoundary1 = field(
        metadata={
            "name": "ToAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class InterestType1Choice:
    cd: None | InterestType1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class NumberAndSumOfTransactions2:
    nb_of_ntries: None | str = field(
        default=None,
        metadata={
            "name": "NbOfNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[0-9]{1,15}",
        },
    )
    sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    ttl_net_ntry_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "TtlNetNtryAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class OrganisationIdentification2:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    ibei: None | str = field(
        default=None,
        metadata={
            "name": "IBEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{2,2}[B-DF-HJ-NP-TV-XZ0-9]{7,7}[0-9]{1,1}",
        },
    )
    bei: None | str = field(
        default=None,
        metadata={
            "name": "BEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    eangln: None | str = field(
        default=None,
        metadata={
            "name": "EANGLN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[0-9]{13,13}",
        },
    )
    uschu: None | str = field(
        default=None,
        metadata={
            "name": "USCHU",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"CH[0-9]{6,6}",
        },
    )
    duns: None | str = field(
        default=None,
        metadata={
            "name": "DUNS",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[0-9]{9,9}",
        },
    )
    bk_pty_id: None | str = field(
        default=None,
        metadata={
            "name": "BkPtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class PersonIdentification3:
    drvrs_lic_nb: None | str = field(
        default=None,
        metadata={
            "name": "DrvrsLicNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cstmr_nb: None | str = field(
        default=None,
        metadata={
            "name": "CstmrNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    scl_scty_nb: None | str = field(
        default=None,
        metadata={
            "name": "SclSctyNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    aln_regn_nb: None | str = field(
        default=None,
        metadata={
            "name": "AlnRegnNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pspt_nb: None | str = field(
        default=None,
        metadata={
            "name": "PsptNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    idnty_card_nb: None | str = field(
        default=None,
        metadata={
            "name": "IdntyCardNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    mplyr_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "MplyrIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dt_and_plc_of_birth: None | DateAndPlaceOfBirth = field(
        default=None,
        metadata={
            "name": "DtAndPlcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    othr_id: None | GenericIdentification4 = field(
        default=None,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PostalAddress1:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class ProprietaryPrice1:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    pric: CurrencyAndAmount = field(
        metadata={
            "name": "Pric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ReferredDocumentAmount1Choice:
    due_pybl_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DuePyblAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    dscnt_apld_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DscntApldAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rmtd_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RmtdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    cdt_note_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CdtNoteAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    tax_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentType1:
    cd: None | DocumentType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ReturnReason1Choice:
    cd: None | TransactionRejectReason2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class SecurityIdentification4Choice:
    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z0-9]{12,12}",
        },
    )
    prtry: None | AlternateSecurityIdentification2 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class TaxCharges1:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class TaxType:
    ctgy_desc: None | str = field(
        default=None,
        metadata={
            "name": "CtgyDesc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    taxbl_base_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TaxblBaseAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class TransactionDates1:
    accptnc_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "AccptncDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    trad_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "TradDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    start_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "StartDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    end_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "EndDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    tx_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "TxDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: list[ProprietaryDate1] = field(
        default_factory=list,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class TransactionQuantities1Choice:
    qty: None | FinancialInstrumentQuantityChoice = field(
        default=None,
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: None | ProprietaryQuantity1 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class TransactionReferences1:
    msg_id: None | str = field(
        default=None,
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    acct_svcr_ref: None | str = field(
        default=None,
        metadata={
            "name": "AcctSvcrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    instr_id: None | str = field(
        default=None,
        metadata={
            "name": "InstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    end_to_end_id: None | str = field(
        default=None,
        metadata={
            "name": "EndToEndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tx_id: None | str = field(
        default=None,
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "MndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    chq_nb: None | str = field(
        default=None,
        metadata={
            "name": "ChqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    clr_sys_ref: None | str = field(
        default=None,
        metadata={
            "name": "ClrSysRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | ProprietaryReference1 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class AmountAndCurrencyExchange2:
    instd_amt: None | AmountAndCurrencyExchangeDetails1 = field(
        default=None,
        metadata={
            "name": "InstdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    tx_amt: None | AmountAndCurrencyExchangeDetails1 = field(
        default=None,
        metadata={
            "name": "TxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    cntr_val_amt: None | AmountAndCurrencyExchangeDetails1 = field(
        default=None,
        metadata={
            "name": "CntrValAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    anncd_pstng_amt: None | AmountAndCurrencyExchangeDetails1 = field(
        default=None,
        metadata={
            "name": "AnncdPstngAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry_amt: list[AmountAndCurrencyExchangeDetails2] = field(
        default_factory=list,
        metadata={
            "name": "PrtryAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class BankTransactionCodeStructure1:
    domn: None | BankTransactionCodeStructure2 = field(
        default=None,
        metadata={
            "name": "Domn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: None | ProprietaryBankTransactionCodeStructure1 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchData:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccount7:
    id: AccountIdentification3Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    tp: None | CashAccountType2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class CashBalance2:
    tp: BalanceType2Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    cdt_line: None | CreditLine1 = field(
        default=None,
        metadata={
            "name": "CdtLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    cdt_dbt_ind: CreditDebitCode = field(
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    dt: DateAndDateTimeChoice = field(
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    avlbty: list[CashBalanceAvailability1] = field(
        default_factory=list,
        metadata={
            "name": "Avlbty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceInformation1:
    cdtr_ref_tp: None | CreditorReferenceType1 = field(
        default=None,
        metadata={
            "name": "CdtrRefTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    cdtr_ref: None | str = field(
        default=None,
        metadata={
            "name": "CdtrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification3:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class ImpliedCurrencyAmountRangeChoice:
    fr_amt: None | AmountRangeBoundary1 = field(
        default=None,
        metadata={
            "name": "FrAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    to_amt: None | AmountRangeBoundary1 = field(
        default=None,
        metadata={
            "name": "ToAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    fr_to_amt: None | FromToAmountRange = field(
        default=None,
        metadata={
            "name": "FrToAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    eqamt: None | Decimal = field(
        default=None,
        metadata={
            "name": "EQAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )


@dataclass(kw_only=True)
class NameAndAddress3:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    adr: PostalAddress1 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class NameAndAddress7:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    pstl_adr: PostalAddress1 = field(
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Party2Choice:
    org_id: None | OrganisationIdentification2 = field(
        default=None,
        metadata={
            "name": "OrgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prvt_id: list[PersonIdentification3] = field(
        default_factory=list,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "max_occurs": 4,
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentInformation1:
    rfrd_doc_tp: None | ReferredDocumentType1 = field(
        default=None,
        metadata={
            "name": "RfrdDocTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rfrd_doc_nb: None | str = field(
        default=None,
        metadata={
            "name": "RfrdDocNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class TaxDetails:
    cert_id: None | str = field(
        default=None,
        metadata={
            "name": "CertId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_tp: None | TaxType = field(
        default=None,
        metadata={
            "name": "TaxTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class TransactionPrice1Choice:
    deal_pric: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DealPric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: list[ProprietaryPrice1] = field(
        default_factory=list,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class CurrencyAndAmountRange:
    amt: ImpliedCurrencyAmountRangeChoice = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ccy: str = field(
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification5Choice:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    nm_and_adr: None | NameAndAddress7 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    cmbnd_id: None | FinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "CmbndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class NumberAndSumOfTransactionsPerBankTransactionCode1:
    nb_of_ntries: None | str = field(
        default=None,
        metadata={
            "name": "NbOfNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[0-9]{1,15}",
        },
    )
    sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    ttl_net_ntry_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "TtlNetNtryAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    bk_tx_cd: BankTransactionCodeStructure1 = field(
        metadata={
            "name": "BkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    avlbty: list[CashBalanceAvailability1] = field(
        default_factory=list,
        metadata={
            "name": "Avlbty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification8:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    id: None | Party2Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ctry_of_res: None | str = field(
        default=None,
        metadata={
            "name": "CtryOfRes",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{2,2}",
        },
    )


@dataclass(kw_only=True)
class RemittanceLocation1:
    rmt_id: None | str = field(
        default=None,
        metadata={
            "name": "RmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rmt_lctn_mtd: None | RemittanceLocationMethod1Code = field(
        default=None,
        metadata={
            "name": "RmtLctnMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rmt_lctn_elctrnc_adr: None | str = field(
        default=None,
        metadata={
            "name": "RmtLctnElctrncAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 256,
        },
    )
    rmt_lctn_pstl_adr: None | NameAndAddress3 = field(
        default=None,
        metadata={
            "name": "RmtLctnPstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class TaxInformation2:
    cdtr_tax_id: None | str = field(
        default=None,
        metadata={
            "name": "CdtrTaxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cdtr_tax_tp: None | str = field(
        default=None,
        metadata={
            "name": "CdtrTaxTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dbtr_tax_id: None | str = field(
        default=None,
        metadata={
            "name": "DbtrTaxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_ref_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxRefNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    ttl_taxbl_base_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxblBaseAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ttl_tax_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    tax_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "TaxDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    tax_tp_inf: list[TaxDetails] = field(
        default_factory=list,
        metadata={
            "name": "TaxTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification3:
    fin_instn_id: FinancialInstitutionIdentification5Choice = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    brnch_id: None | BranchData = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class GroupHeader23:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    msg_rcpt: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "MsgRcpt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    msg_pgntn: None | Pagination = field(
        default=None,
        metadata={
            "name": "MsgPgntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 500,
        },
    )


@dataclass(kw_only=True)
class ProprietaryParty1:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    pty: PartyIdentification8 = field(
        metadata={
            "name": "Pty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Rate1:
    rate: RateTypeChoice = field(
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    vldty_rg: None | CurrencyAndAmountRange = field(
        default=None,
        metadata={
            "name": "VldtyRg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class ReturnReasonInformation5:
    orgnl_bk_tx_cd: None | BankTransactionCodeStructure1 = field(
        default=None,
        metadata={
            "name": "OrgnlBkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rtr_orgtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "RtrOrgtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rtr_rsn: None | ReturnReason1Choice = field(
        default=None,
        metadata={
            "name": "RtrRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    addtl_rtr_rsn_inf: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AddtlRtrRsnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 105,
        },
    )


@dataclass(kw_only=True)
class StructuredRemittanceInformation6:
    rfrd_doc_inf: None | ReferredDocumentInformation1 = field(
        default=None,
        metadata={
            "name": "RfrdDocInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rfrd_doc_rltd_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "RfrdDocRltdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rfrd_doc_amt: list[ReferredDocumentAmount1Choice] = field(
        default_factory=list,
        metadata={
            "name": "RfrdDocAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    cdtr_ref_inf: None | CreditorReferenceInformation1 = field(
        default=None,
        metadata={
            "name": "CdtrRefInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    invcr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Invcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    invcee: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Invcee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    addtl_rmt_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlRmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class TotalTransactions1:
    ttl_ntries: None | NumberAndSumOfTransactions2 = field(
        default=None,
        metadata={
            "name": "TtlNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ttl_cdt_ntries: None | NumberAndSumOfTransactions1 = field(
        default=None,
        metadata={
            "name": "TtlCdtNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ttl_dbt_ntries: None | NumberAndSumOfTransactions1 = field(
        default=None,
        metadata={
            "name": "TtlDbtNtries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ttl_ntries_per_bk_tx_cd: list[
        NumberAndSumOfTransactionsPerBankTransactionCode1
    ] = field(
        default_factory=list,
        metadata={
            "name": "TtlNtriesPerBkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class AccountInterest1:
    tp: None | InterestType1Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rate: list[Rate1] = field(
        default_factory=list,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    fr_to_dt: None | DateTimePeriodDetails = field(
        default=None,
        metadata={
            "name": "FrToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rsn: None | str = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CashAccount13:
    id: AccountIdentification3Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    tp: None | CashAccountType2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    ownr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Ownr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    svcr: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "Svcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class ChargesInformation3:
    ttl_chrgs_and_tax_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlChrgsAndTaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    tp: None | ChargeTypeChoice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    br: None | ChargeBearerType1Code = field(
        default=None,
        metadata={
            "name": "Br",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    pty: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "Pty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    tax: None | TaxCharges1 = field(
        default=None,
        metadata={
            "name": "Tax",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class ProprietaryAgent1:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    agt: BranchAndFinancialInstitutionIdentification3 = field(
        metadata={
            "name": "Agt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class RemittanceInformation1:
    ustrd: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    strd: list[StructuredRemittanceInformation6] = field(
        default_factory=list,
        metadata={
            "name": "Strd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class TransactionInterest1:
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    cdt_dbt_ind: CreditDebitCode = field(
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    tp: None | InterestType1Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rate: list[Rate1] = field(
        default_factory=list,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    fr_to_dt: None | DateTimePeriodDetails = field(
        default=None,
        metadata={
            "name": "FrToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rsn: None | str = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class TransactionParty1:
    initg_pty: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "InitgPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    dbtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    dbtr_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ultmt_dbtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    cdtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    cdtr_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ultmt_cdtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "UltmtCdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    tradg_pty: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "TradgPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: list[ProprietaryParty1] = field(
        default_factory=list,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class TransactionAgents1:
    dbtr_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "DbtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    cdtr_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "CdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    intrmy_agt1: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt1",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    intrmy_agt2: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt2",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    intrmy_agt3: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt3",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rcvg_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "RcvgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    dlvrg_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "DlvrgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    issg_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "IssgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    sttlm_plc: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "SttlmPlc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    prtry: list[ProprietaryAgent1] = field(
        default_factory=list,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )


@dataclass(kw_only=True)
class EntryTransaction1:
    refs: None | TransactionReferences1 = field(
        default=None,
        metadata={
            "name": "Refs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    amt_dtls: None | AmountAndCurrencyExchange2 = field(
        default=None,
        metadata={
            "name": "AmtDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    avlbty: list[CashBalanceAvailability1] = field(
        default_factory=list,
        metadata={
            "name": "Avlbty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    bk_tx_cd: None | BankTransactionCodeStructure1 = field(
        default=None,
        metadata={
            "name": "BkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    chrgs: list[ChargesInformation3] = field(
        default_factory=list,
        metadata={
            "name": "Chrgs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    intrst: list[TransactionInterest1] = field(
        default_factory=list,
        metadata={
            "name": "Intrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rltd_pties: None | TransactionParty1 = field(
        default=None,
        metadata={
            "name": "RltdPties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rltd_agts: None | TransactionAgents1 = field(
        default=None,
        metadata={
            "name": "RltdAgts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    purp: None | Purpose1Choice = field(
        default=None,
        metadata={
            "name": "Purp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rltd_rmt_inf: list[RemittanceLocation1] = field(
        default_factory=list,
        metadata={
            "name": "RltdRmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "max_occurs": 10,
        },
    )
    rmt_inf: None | RemittanceInformation1 = field(
        default=None,
        metadata={
            "name": "RmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rltd_dts: None | TransactionDates1 = field(
        default=None,
        metadata={
            "name": "RltdDts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rltd_pric: None | TransactionPrice1Choice = field(
        default=None,
        metadata={
            "name": "RltdPric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rltd_qties: list[TransactionQuantities1Choice] = field(
        default_factory=list,
        metadata={
            "name": "RltdQties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    fin_instrm_id: None | SecurityIdentification4Choice = field(
        default=None,
        metadata={
            "name": "FinInstrmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    tax: None | TaxInformation2 = field(
        default=None,
        metadata={
            "name": "Tax",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    rtr_inf: None | ReturnReasonInformation5 = field(
        default=None,
        metadata={
            "name": "RtrInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    corp_actn: None | CorporateAction1 = field(
        default=None,
        metadata={
            "name": "CorpActn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    sfkpg_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    addtl_tx_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlTxInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 500,
        },
    )


@dataclass(kw_only=True)
class StatementEntry1:
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    cdt_dbt_ind: CreditDebitCode = field(
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    rvsl_ind: None | bool = field(
        default=None,
        metadata={
            "name": "RvslInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    sts: EntryStatus3Code = field(
        metadata={
            "name": "Sts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    bookg_dt: None | DateAndDateTimeChoice = field(
        default=None,
        metadata={
            "name": "BookgDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    val_dt: None | DateAndDateTimeChoice = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    acct_svcr_ref: None | str = field(
        default=None,
        metadata={
            "name": "AcctSvcrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    avlbty: list[CashBalanceAvailability1] = field(
        default_factory=list,
        metadata={
            "name": "Avlbty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    bk_tx_cd: BankTransactionCodeStructure1 = field(
        metadata={
            "name": "BkTxCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    comssn_wvr_ind: None | bool = field(
        default=None,
        metadata={
            "name": "ComssnWvrInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    addtl_inf_ind: None | MessageIdentification2 = field(
        default=None,
        metadata={
            "name": "AddtlInfInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    btch: list[BatchInformation1] = field(
        default_factory=list,
        metadata={
            "name": "Btch",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    amt_dtls: None | AmountAndCurrencyExchange2 = field(
        default=None,
        metadata={
            "name": "AmtDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    chrgs: list[ChargesInformation3] = field(
        default_factory=list,
        metadata={
            "name": "Chrgs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    intrst: list[TransactionInterest1] = field(
        default_factory=list,
        metadata={
            "name": "Intrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    tx_dtls: list[EntryTransaction1] = field(
        default_factory=list,
        metadata={
            "name": "TxDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    addtl_ntry_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlNtryInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 500,
        },
    )


@dataclass(kw_only=True)
class AccountStatement1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    elctrnc_seq_nb: None | Decimal = field(
        default=None,
        metadata={
            "name": "ElctrncSeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    lgl_seq_nb: None | Decimal = field(
        default=None,
        metadata={
            "name": "LglSeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    fr_to_dt: None | DateTimePeriodDetails = field(
        default=None,
        metadata={
            "name": "FrToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    cpy_dplct_ind: None | CopyDuplicate1Code = field(
        default=None,
        metadata={
            "name": "CpyDplctInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    acct: CashAccount13 = field(
        metadata={
            "name": "Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    rltd_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "RltdAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    intrst: list[AccountInterest1] = field(
        default_factory=list,
        metadata={
            "name": "Intrst",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    bal: list[CashBalance2] = field(
        default_factory=list,
        metadata={
            "name": "Bal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_occurs": 1,
        },
    )
    txs_summry: None | TotalTransactions1 = field(
        default=None,
        metadata={
            "name": "TxsSummry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    ntry: list[StatementEntry1] = field(
        default_factory=list,
        metadata={
            "name": "Ntry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
        },
    )
    addtl_stmt_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlStmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_length": 1,
            "max_length": 500,
        },
    )


@dataclass(kw_only=True)
class BankToCustomerStatementV01:
    grp_hdr: GroupHeader23 = field(
        metadata={
            "name": "GrpHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "required": True,
        }
    )
    stmt: list[AccountStatement1] = field(
        default_factory=list,
        metadata={
            "name": "Stmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:camt.053.001.01"

    bk_to_cstmr_stmt_v01: BankToCustomerStatementV01 = field(
        metadata={
            "name": "BkToCstmrStmtV01",
            "type": "Element",
            "required": True,
        }
    )
