from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01"


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


class CalculationMethod1Code(Enum):
    SIMP = "SIMP"
    COMP = "COMP"


class CollateralEntryType1Code(Enum):
    DELI = "DELI"
    RECE = "RECE"


class CollateralRole1Code(Enum):
    GIVE = "GIVE"
    TAKE = "TAKE"


class CollateralTransactionType1Code(Enum):
    AADJ = "AADJ"
    CDTA = "CDTA"
    CADJ = "CADJ"
    DADJ = "DADJ"
    DBVT = "DBVT"
    INIT = "INIT"
    MADJ = "MADJ"
    PADJ = "PADJ"
    RATA = "RATA"
    TERM = "TERM"


class CreditDebitCode(Enum):
    CRDT = "CRDT"
    DBIT = "DBIT"


@dataclass(kw_only=True)
class CrystallisationDay1:
    day: bool = field(
        metadata={
            "name": "Day",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    prd: None | str = field(
        default=None,
        metadata={
            "name": "Prd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


class DateType2Code(Enum):
    OPEN = "OPEN"


class DeliveryReceiptType2Code(Enum):
    FREE = "FREE"
    APMT = "APMT"


class EventFrequency12Code(Enum):
    ADHO = "ADHO"
    YEAR = "YEAR"
    DAIL = "DAIL"
    TOMN = "TOMN"
    TOWK = "TOWK"
    INDA = "INDA"
    MNTH = "MNTH"
    QUTR = "QUTR"
    SEMI = "SEMI"
    TWMN = "TWMN"
    WEEK = "WEEK"
    ONDE = "ONDE"


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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    face_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "FaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "total_digits": 30,
            "fraction_digits": 29,
        },
    )


class FrequencyRateFixing1Code(Enum):
    NONE = "NONE"
    OVNG = "OVNG"
    PRDC = "PRDC"


@dataclass(kw_only=True)
class GenericIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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


class OptionType1Code(Enum):
    CALL = "CALL"
    PUTO = "PUTO"


@dataclass(kw_only=True)
class Pagination1:
    pg_nb: str = field(
        metadata={
            "name": "PgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "pattern": r"[0-9]{1,5}",
        }
    )
    last_pg_ind: bool = field(
        metadata={
            "name": "LastPgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )


class RepoTerminationOption1Code(Enum):
    EGRN = "EGRN"
    ETSB = "ETSB"


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


@dataclass(kw_only=True)
class TransactionIdentifications44:
    trpty_agt_svc_prvdr_coll_instr_id: str = field(
        metadata={
            "name": "TrptyAgtSvcPrvdrCollInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    trpty_agt_svc_prvdr_coll_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "TrptyAgtSvcPrvdrCollTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    clnt_coll_instr_id: None | str = field(
        default=None,
        metadata={
            "name": "ClntCollInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    clnt_coll_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "ClntCollTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctr_pty_coll_instr_id: None | str = field(
        default=None,
        metadata={
            "name": "CtrPtyCollInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctr_pty_coll_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "CtrPtyCollTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cmon_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "CmonTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 52,
        },
    )


class TypeOfIdentification1Code(Enum):
    ARNU = "ARNU"
    CCPT = "CCPT"
    CHTY = "CHTY"
    CORP = "CORP"
    DRLC = "DRLC"
    FIIN = "FIIN"
    TXID = "TXID"


@dataclass(kw_only=True)
class BenchmarkCurveName13Choice:
    cd: None | BenchmarkCurveName7Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    prtry: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class BlockChainAddressWallet3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class CashMovement5:
    csh_mvmnt: CollateralEntryType1Code = field(
        metadata={
            "name": "CshMvmnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    csh_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "CshAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    coll_mvmnt: bool = field(
        metadata={
            "name": "CollMvmnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    clnt_csh_mvmnt_id: None | str = field(
        default=None,
        metadata={
            "name": "ClntCshMvmntId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    trpty_agt_svc_prvdr_csh_mvmnt_id: None | str = field(
        default=None,
        metadata={
            "name": "TrptyAgtSvcPrvdrCshMvmntId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CollateralDate2:
    trad_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "TradDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    reqd_exctn_dt: None | DateAndDateTime2Choice = field(
        default=None,
        metadata={
            "name": "ReqdExctnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "SttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralTransactionType1Choice:
    cd: None | CollateralTransactionType1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class Date3Choice:
    cd: None | DateType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class ExposureType23Choice:
    cd: None | ExposureType14Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class ForeignExchangeTerms23:
    unit_ccy: str = field(
        metadata={
            "name": "UnitCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    qtd_ccy: str = field(
        metadata={
            "name": "QtdCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    xchg_rate: Decimal = field(
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "total_digits": 11,
            "fraction_digits": 10,
        }
    )
    rsltg_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "RsltgAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Frequency38Choice:
    cd: None | EventFrequency12Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class FrequencyRateFixing1Choice:
    cd: None | FrequencyRateFixing1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    nb_of_days: None | str = field(
        default=None,
        metadata={
            "name": "NbOfDays",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[0-9]{1,3}",
        },
    )


@dataclass(kw_only=True)
class IdentificationType42Choice:
    cd: None | TypeOfIdentification1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class InterestComputationMethodFormat4Choice:
    cd: None | InterestComputationMethod2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class OptionType6Choice:
    cd: None | OptionType1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class OtherIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    tp: IdentificationSource3Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class RateOrType1Choice:
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    tp: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class SecuritiesAccount19:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class TradingPartyCapacity5Choice:
    cd: None | TradingCapacity7Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class AlternatePartyIdentification7:
    id_tp: IdentificationType42Choice = field(
        metadata={
            "name": "IdTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )
    altrn_id: str = field(
        metadata={
            "name": "AltrnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class AmountAndDirection49:
    amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    orgnl_ccy_and_ordrd_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "OrgnlCcyAndOrdrdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    fxdtls: None | ForeignExchangeTerms23 = field(
        default=None,
        metadata={
            "name": "FXDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class ClosingDate4Choice:
    dt: None | DateAndDateTime2Choice = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    cd: None | Date3Choice = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralParameters11:
    coll_instr_tp: CollateralTransactionType1Choice = field(
        metadata={
            "name": "CollInstrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    xpsr_tp: ExposureType23Choice = field(
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    coll_sd: CollateralRole1Code = field(
        metadata={
            "name": "CollSd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    val_sght_mrgn_rate: None | RateOrType1Choice = field(
        default=None,
        metadata={
            "name": "ValSghtMrgnRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    elgblty_set_prfl: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "ElgbltySetPrfl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    trf_titl: None | bool = field(
        default=None,
        metadata={
            "name": "TrfTitl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    sttlm_prc: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "SttlmPrc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress5:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class RateTypeAndLookback2:
    tp: BenchmarkCurveName13Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    look_bck_days: None | str = field(
        default=None,
        metadata={
            "name": "LookBckDays",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[0-9]{1,3}",
        },
    )
    crstllstn_dt: None | CrystallisationDay1 = field(
        default=None,
        metadata={
            "name": "CrstllstnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    tnr: None | InterestRateIndexTenor2Code = field(
        default=None,
        metadata={
            "name": "Tnr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )


@dataclass(kw_only=True)
class SecurityIdentification19:
    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[A-Z]{2,2}[A-Z0-9]{9,9}[0-9]{1,1}",
        },
    )
    othr_id: list[OtherIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class CollateralAmount12:
    tx: None | AmountAndDirection49 = field(
        default=None,
        metadata={
            "name": "Tx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    termntn: None | AmountAndDirection49 = field(
        default=None,
        metadata={
            "name": "Termntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    acrd: None | AmountAndDirection49 = field(
        default=None,
        metadata={
            "name": "Acrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    cmpnd_smpl_acrl_clctn: None | CalculationMethod1Code = field(
        default=None,
        metadata={
            "name": "CmpndSmplAcrlClctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    pmt_frqcy: None | Frequency38Choice = field(
        default=None,
        metadata={
            "name": "PmtFrqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    intrst_pmt_dely: None | str = field(
        default=None,
        metadata={
            "name": "IntrstPmtDely",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[0-9]{1,3}",
        },
    )
    val_sght: None | AmountAndDirection49 = field(
        default=None,
        metadata={
            "name": "ValSght",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification120Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    nm_and_adr: None | NameAndAddress5 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class RateOrName4Choice:
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    rate_indx_dtls: None | RateTypeAndLookback2 = field(
        default=None,
        metadata={
            "name": "RateIndxDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class SecuritiesMovement7:
    scties_mvmnt_tp: CollateralEntryType1Code = field(
        metadata={
            "name": "SctiesMvmntTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    fin_instrm_id: SecurityIdentification19 = field(
        metadata={
            "name": "FinInstrmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    qty: FinancialInstrumentQuantity33Choice = field(
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    coll_mvmnt: bool = field(
        metadata={
            "name": "CollMvmnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    clnt_scties_mvmnt_id: None | str = field(
        default=None,
        metadata={
            "name": "ClntSctiesMvmntId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    trpty_agt_svc_prvdr_scties_mvmnt_id: None | str = field(
        default=None,
        metadata={
            "name": "TrptyAgtSvcPrvdrSctiesMvmntId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DealTransactionDetails6:
    min_ntce_prd: None | str = field(
        default=None,
        metadata={
            "name": "MinNtcePrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[0-9]{3}",
        },
    )
    clsg_dt: ClosingDate4Choice = field(
        metadata={
            "name": "ClsgDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    deal_dtls_amt: None | CollateralAmount12 = field(
        default=None,
        metadata={
            "name": "DealDtlsAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    pricg_rate_and_indx: None | RateOrName4Choice = field(
        default=None,
        metadata={
            "name": "PricgRateAndIndx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    ovrnght_frqcy_rate_fxg: None | FrequencyRateFixing1Choice = field(
        default=None,
        metadata={
            "name": "OvrnghtFrqcyRateFxg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    sprd: None | Decimal = field(
        default=None,
        metadata={
            "name": "Sprd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    day_cnt_bsis: None | InterestComputationMethodFormat4Choice = field(
        default=None,
        metadata={
            "name": "DayCntBsis",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    pmt: None | DeliveryReceiptType2Code = field(
        default=None,
        metadata={
            "name": "Pmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    optn_tp: None | OptionType6Choice = field(
        default=None,
        metadata={
            "name": "OptnTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    termntn_optn: None | RepoTerminationOption1Code = field(
        default=None,
        metadata={
            "name": "TermntnOptn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification136:
    id: PartyIdentification120Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )


@dataclass(kw_only=True)
class PartyIdentificationAndAccount193:
    id: PartyIdentification120Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    altrn_id: None | AlternatePartyIdentification7 = field(
        default=None,
        metadata={
            "name": "AltrnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentificationAndAccount203:
    id: PartyIdentification120Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    altrn_id: None | AlternatePartyIdentification7 = field(
        default=None,
        metadata={
            "name": "AltrnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    sfkpg_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    blck_chain_adr_or_wllt: None | BlockChainAddressWallet3 = field(
        default=None,
        metadata={
            "name": "BlckChainAdrOrWllt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    pty_cpcty: None | TradingPartyCapacity5Choice = field(
        default=None,
        metadata={
            "name": "PtyCpcty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentificationAndAccount202:
    id: PartyIdentification120Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    altrn_id: None | AlternatePartyIdentification7 = field(
        default=None,
        metadata={
            "name": "AltrnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    sfkpg_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    blck_chain_adr_or_wllt: None | BlockChainAddressWallet3 = field(
        default=None,
        metadata={
            "name": "BlckChainAdrOrWllt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    acct_ownr: None | PartyIdentification136 = field(
        default=None,
        metadata={
            "name": "AcctOwnr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    pty_cpcty: None | TradingPartyCapacity5Choice = field(
        default=None,
        metadata={
            "name": "PtyCpcty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class CollateralParties8:
    pty_a: PartyIdentificationAndAccount202 = field(
        metadata={
            "name": "PtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    clnt_pty_a: None | PartyIdentificationAndAccount193 = field(
        default=None,
        metadata={
            "name": "ClntPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    pty_b: PartyIdentificationAndAccount203 = field(
        metadata={
            "name": "PtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    clnt_pty_b: None | PartyIdentificationAndAccount193 = field(
        default=None,
        metadata={
            "name": "ClntPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    trpty_agt: None | PartyIdentification136 = field(
        default=None,
        metadata={
            "name": "TrptyAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class TripartyCollateralAllegementNotificationV01:
    tx_instr_id: TransactionIdentifications44 = field(
        metadata={
            "name": "TxInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    pgntn: Pagination1 = field(
        metadata={
            "name": "Pgntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    gnl_params: CollateralParameters11 = field(
        metadata={
            "name": "GnlParams",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    coll_pties: CollateralParties8 = field(
        metadata={
            "name": "CollPties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    deal_tx_dtls: DealTransactionDetails6 = field(
        metadata={
            "name": "DealTxDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    deal_tx_dt: CollateralDate2 = field(
        metadata={
            "name": "DealTxDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
            "required": True,
        }
    )
    scties_mvmnt: list[SecuritiesMovement7] = field(
        default_factory=list,
        metadata={
            "name": "SctiesMvmnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    csh_mvmnt: list[CashMovement5] = field(
        default_factory=list,
        metadata={
            "name": "CshMvmnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.021.001.01"

    trpty_coll_allgmt_ntfctn: TripartyCollateralAllegementNotificationV01 = (
        field(
            metadata={
                "name": "TrptyCollAllgmtNtfctn",
                "type": "Element",
                "required": True,
            }
        )
    )
