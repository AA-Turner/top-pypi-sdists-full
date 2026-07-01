from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01"


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


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


class CashClearingSystem3Code(Enum):
    ABE = "ABE"
    ART = "ART"
    AVP = "AVP"
    AZM = "AZM"
    BAP = "BAP"
    BEL = "BEL"
    BOF = "BOF"
    BRL = "BRL"
    CAD = "CAD"
    CAM = "CAM"
    CBJ = "CBJ"
    CHP = "CHP"
    DKC = "DKC"
    RTP = "RTP"
    EBA = "EBA"
    ELS = "ELS"
    ERP = "ERP"
    XCT = "XCT"
    HRK = "HRK"
    HRM = "HRM"
    HUF = "HUF"
    LGS = "LGS"
    LVL = "LVL"
    MUP = "MUP"
    NOC = "NOC"
    PCH = "PCH"
    PDS = "PDS"
    PEG = "PEG"
    PNS = "PNS"
    PVE = "PVE"
    SEC = "SEC"
    SIT = "SIT"
    SLB = "SLB"
    SPG = "SPG"
    SSK = "SSK"
    TBF = "TBF"
    TGT = "TGT"
    TOP = "TOP"
    FDW = "FDW"
    BOJ = "BOJ"
    FEY = "FEY"
    ZEN = "ZEN"
    DDK = "DDK"
    AIP = "AIP"
    BCC = "BCC"
    BDS = "BDS"
    BGN = "BGN"
    BHS = "BHS"
    BIS = "BIS"
    BSP = "BSP"
    EPM = "EPM"
    EPN = "EPN"
    FDA = "FDA"
    GIS = "GIS"
    INC = "INC"
    JOD = "JOD"
    KPS = "KPS"
    LKB = "LKB"
    MEP = "MEP"
    MRS = "MRS"
    NAM = "NAM"
    PTR = "PTR"
    ROL = "ROL"
    ROS = "ROS"
    SCP = "SCP"
    STG = "STG"
    THB = "THB"
    TIS = "TIS"
    TTD = "TTD"
    UIS = "UIS"
    MOS = "MOS"
    ZET = "ZET"
    ZIS = "ZIS"
    CHI = "CHI"
    COP = "COP"


class ChargeBearerType1Code(Enum):
    DEBT = "DEBT"
    CRED = "CRED"
    SHAR = "SHAR"
    SLEV = "SLEV"


class ClearingChannel2Code(Enum):
    RTGS = "RTGS"
    RTNS = "RTNS"
    MPNS = "MPNS"
    BOOK = "BOOK"


@dataclass(kw_only=True)
class ClearingSystemMemberIdentification3Choice:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


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
class DateAndPlaceOfBirth:
    birth_dt: XmlDate = field(
        metadata={
            "name": "BirthDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    prvc_of_birth: None | str = field(
        default=None,
        metadata={
            "name": "PrvcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    city_of_birth: str = field(
        metadata={
            "name": "CityOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_of_birth: str = field(
        metadata={
            "name": "CtryOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
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


class Frequency1Code(Enum):
    YEAR = "YEAR"
    MNTH = "MNTH"
    QURT = "QURT"
    MIAN = "MIAN"
    WEEK = "WEEK"
    DAIL = "DAIL"
    ADHO = "ADHO"
    INDA = "INDA"


@dataclass(kw_only=True)
class GenericIdentification3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    id_tp: str = field(
        metadata={
            "name": "IdTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class LocalInstrument1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class OriginalGroupInformation3:
    orgnl_msg_id: str = field(
        metadata={
            "name": "OrgnlMsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    orgnl_msg_nm_id: str = field(
        metadata={
            "name": "OrgnlMsgNmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    orgnl_cre_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "OrgnlCreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


class PaymentCategoryPurpose1Code(Enum):
    CORT = "CORT"
    SALA = "SALA"
    TREA = "TREA"
    CASH = "CASH"
    DIVI = "DIVI"
    GOVT = "GOVT"
    INTE = "INTE"
    LOAN = "LOAN"
    PENS = "PENS"
    SECU = "SECU"
    SSBE = "SSBE"
    SUPP = "SUPP"
    TAXS = "TAXS"
    TRAD = "TRAD"
    VATX = "VATX"
    HEDG = "HEDG"
    INTC = "INTC"
    WHLD = "WHLD"


class PaymentMethod4Code(Enum):
    CHK = "CHK"
    TRF = "TRF"
    DD = "DD"
    TRA = "TRA"


class Priority2Code(Enum):
    HIGH = "HIGH"
    NORM = "NORM"


class SequenceType1Code(Enum):
    FRST = "FRST"
    RCUR = "RCUR"
    FNAL = "FNAL"
    OOFF = "OOFF"


class ServiceLevel1Code(Enum):
    SEPA = "SEPA"
    SDVA = "SDVA"
    PRPT = "PRPT"


class SettlementMethod1Code(Enum):
    INDA = "INDA"
    INGA = "INGA"
    COVE = "COVE"
    CLRG = "CLRG"


@dataclass(kw_only=True)
class SimpleIdentificationInformation2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[a-zA-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    bban: None | str = field(
        default=None,
        metadata={
            "name": "BBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[a-zA-Z0-9]{1,30}",
        },
    )
    upic: None | str = field(
        default=None,
        metadata={
            "name": "UPIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[0-9]{8,17}",
        },
    )
    prtry_acct: None | SimpleIdentificationInformation2 = field(
        default=None,
        metadata={
            "name": "PrtryAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccountType2:
    cd: None | CashAccountType4Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ClearingSystemIdentification1Choice:
    clr_sys_id: None | CashClearingSystem3Code = field(
        default=None,
        metadata={
            "name": "ClrSysId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceType1:
    cd: None | DocumentType3Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class EquivalentAmount:
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    ccy_of_trf: str = field(
        metadata={
            "name": "CcyOfTrf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )


@dataclass(kw_only=True)
class OrganisationIdentification2:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    ibei: None | str = field(
        default=None,
        metadata={
            "name": "IBEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[A-Z]{2,2}[B-DF-HJ-NP-TV-XZ0-9]{7,7}[0-9]{1,1}",
        },
    )
    bei: None | str = field(
        default=None,
        metadata={
            "name": "BEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    eangln: None | str = field(
        default=None,
        metadata={
            "name": "EANGLN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[0-9]{13,13}",
        },
    )
    uschu: None | str = field(
        default=None,
        metadata={
            "name": "USCHU",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"CH[0-9]{6,6}",
        },
    )
    duns: None | str = field(
        default=None,
        metadata={
            "name": "DUNS",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[0-9]{9,9}",
        },
    )
    bk_pty_id: None | str = field(
        default=None,
        metadata={
            "name": "BkPtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class PersonIdentification3:
    drvrs_lic_nb: None | str = field(
        default=None,
        metadata={
            "name": "DrvrsLicNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cstmr_nb: None | str = field(
        default=None,
        metadata={
            "name": "CstmrNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    scl_scty_nb: None | str = field(
        default=None,
        metadata={
            "name": "SclSctyNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    aln_regn_nb: None | str = field(
        default=None,
        metadata={
            "name": "AlnRegnNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pspt_nb: None | str = field(
        default=None,
        metadata={
            "name": "PsptNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    idnty_card_nb: None | str = field(
        default=None,
        metadata={
            "name": "IdntyCardNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    mplyr_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "MplyrIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dt_and_plc_of_birth: None | DateAndPlaceOfBirth = field(
        default=None,
        metadata={
            "name": "DtAndPlcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    othr_id: None | GenericIdentification4 = field(
        default=None,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class ReferredDocumentAmount1Choice:
    due_pybl_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DuePyblAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    dscnt_apld_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DscntApldAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rmtd_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RmtdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    cdt_note_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CdtNoteAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    tax_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentType1:
    cd: None | DocumentType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ServiceLevel2Choice:
    cd: None | ServiceLevel1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class AmountType2Choice:
    instd_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "InstdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    eqvt_amt: None | EquivalentAmount = field(
        default=None,
        metadata={
            "name": "EqvtAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchData:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccount7:
    id: AccountIdentification3Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    tp: None | CashAccountType2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceInformation1:
    cdtr_ref_tp: None | CreditorReferenceType1 = field(
        default=None,
        metadata={
            "name": "CdtrRefTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    cdtr_ref: None | str = field(
        default=None,
        metadata={
            "name": "CdtrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress7:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    pstl_adr: PostalAddress1 = field(
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    prvt_id: list[PersonIdentification3] = field(
        default_factory=list,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "max_occurs": 4,
        },
    )


@dataclass(kw_only=True)
class PaymentTypeInformation6:
    instr_prty: None | Priority2Code = field(
        default=None,
        metadata={
            "name": "InstrPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    svc_lvl: None | ServiceLevel2Choice = field(
        default=None,
        metadata={
            "name": "SvcLvl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    clr_chanl: None | ClearingChannel2Code = field(
        default=None,
        metadata={
            "name": "ClrChanl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    lcl_instrm: None | LocalInstrument1Choice = field(
        default=None,
        metadata={
            "name": "LclInstrm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    seq_tp: None | SequenceType1Code = field(
        default=None,
        metadata={
            "name": "SeqTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    ctgy_purp: None | PaymentCategoryPurpose1Code = field(
        default=None,
        metadata={
            "name": "CtgyPurp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentInformation1:
    rfrd_doc_tp: None | ReferredDocumentType1 = field(
        default=None,
        metadata={
            "name": "RfrdDocTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rfrd_doc_nb: None | str = field(
        default=None,
        metadata={
            "name": "RfrdDocNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification5Choice:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    nm_and_adr: None | NameAndAddress7 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    cmbnd_id: None | FinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "CmbndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification8:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    id: None | Party2Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    ctry_of_res: None | str = field(
        default=None,
        metadata={
            "name": "CtryOfRes",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "pattern": r"[A-Z]{2,2}",
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification3:
    fin_instn_id: FinancialInstitutionIdentification5Choice = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    brnch_id: None | BranchData = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class ReturnReasonInformation1:
    rtr_orgtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "RtrOrgtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rtr_rsn: None | ReturnReason1Choice = field(
        default=None,
        metadata={
            "name": "RtrRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    addtl_rtr_rsn_inf: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AddtlRtrRsnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rfrd_doc_rltd_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "RfrdDocRltdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rfrd_doc_amt: list[ReferredDocumentAmount1Choice] = field(
        default_factory=list,
        metadata={
            "name": "RfrdDocAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    cdtr_ref_inf: None | CreditorReferenceInformation1 = field(
        default=None,
        metadata={
            "name": "CdtrRefInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    invcr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Invcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    invcee: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Invcee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    addtl_rmt_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlRmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class AmendmentInformationDetails1:
    orgnl_mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlMndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_cdtr_schme_id: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "OrgnlCdtrSchmeId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    orgnl_cdtr_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "OrgnlCdtrAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            },
        )
    )
    orgnl_cdtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "OrgnlCdtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    orgnl_dbtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "OrgnlDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    orgnl_dbtr_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "OrgnlDbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    orgnl_dbtr_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "OrgnlDbtrAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            },
        )
    )
    orgnl_dbtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "OrgnlDbtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    orgnl_fnl_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "OrgnlFnlColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    orgnl_frqcy: None | Frequency1Code = field(
        default=None,
        metadata={
            "name": "OrgnlFrqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class ChargesInformation1:
    chrgs_amt: CurrencyAndAmount = field(
        metadata={
            "name": "ChrgsAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    chrgs_pty: BranchAndFinancialInstitutionIdentification3 = field(
        metadata={
            "name": "ChrgsPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class OriginalGroupInformation2:
    orgnl_msg_id: str = field(
        metadata={
            "name": "OrgnlMsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    orgnl_msg_nm_id: str = field(
        metadata={
            "name": "OrgnlMsgNmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    orgnl_cre_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "OrgnlCreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rtr_rsn_inf: list[ReturnReasonInformation1] = field(
        default_factory=list,
        metadata={
            "name": "RtrRsnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class RemittanceInformation1:
    ustrd: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    strd: list[StructuredRemittanceInformation6] = field(
        default_factory=list,
        metadata={
            "name": "Strd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class SettlementInformation1:
    sttlm_mtd: SettlementMethod1Code = field(
        metadata={
            "name": "SttlmMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    sttlm_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "SttlmAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    clr_sys: None | ClearingSystemIdentification1Choice = field(
        default=None,
        metadata={
            "name": "ClrSys",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    instg_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "InstgRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            },
        )
    )
    instg_rmbrsmnt_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "InstgRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    instd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "InstdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            },
        )
    )
    instd_rmbrsmnt_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "InstdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    thrd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "ThrdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            },
        )
    )
    thrd_rmbrsmnt_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "ThrdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class SettlementInformation3:
    sttlm_mtd: SettlementMethod1Code = field(
        metadata={
            "name": "SttlmMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    sttlm_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "SttlmAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    clr_sys: None | ClearingSystemIdentification1Choice = field(
        default=None,
        metadata={
            "name": "ClrSys",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    instg_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "InstgRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            },
        )
    )
    instg_rmbrsmnt_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "InstgRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    instd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "InstdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            },
        )
    )
    instd_rmbrsmnt_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "InstdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    thrd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "ThrdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            },
        )
    )
    thrd_rmbrsmnt_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "ThrdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class GroupHeader6:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    authstn: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Authstn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "max_occurs": 2,
            "min_length": 1,
            "max_length": 128,
        },
    )
    btch_bookg: None | bool = field(
        default=None,
        metadata={
            "name": "BtchBookg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    nb_of_txs: str = field(
        metadata={
            "name": "NbOfTxs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
            "pattern": r"[0-9]{1,15}",
        }
    )
    ctrl_sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "CtrlSum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    grp_rtr: None | bool = field(
        default=None,
        metadata={
            "name": "GrpRtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    ttl_rtrd_intr_bk_sttlm_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlRtrdIntrBkSttlmAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    sttlm_inf: SettlementInformation1 = field(
        metadata={
            "name": "SttlmInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    instg_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "InstgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    instd_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "InstdAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class MandateRelatedInformation1:
    mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "MndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dt_of_sgntr: None | XmlDate = field(
        default=None,
        metadata={
            "name": "DtOfSgntr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    amdmnt_ind: None | bool = field(
        default=None,
        metadata={
            "name": "AmdmntInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    amdmnt_inf_dtls: None | AmendmentInformationDetails1 = field(
        default=None,
        metadata={
            "name": "AmdmntInfDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    elctrnc_sgntr: None | str = field(
        default=None,
        metadata={
            "name": "ElctrncSgntr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 1025,
        },
    )
    frst_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "FrstColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    fnl_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "FnlColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    frqcy: None | Frequency1Code = field(
        default=None,
        metadata={
            "name": "Frqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class OriginalTransactionReference1:
    intr_bk_sttlm_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    amt: None | AmountType2Choice = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    reqd_exctn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ReqdExctnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    reqd_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ReqdColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    cdtr_schme_id: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "CdtrSchmeId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    sttlm_inf: None | SettlementInformation3 = field(
        default=None,
        metadata={
            "name": "SttlmInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    pmt_tp_inf: None | PaymentTypeInformation6 = field(
        default=None,
        metadata={
            "name": "PmtTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    pmt_mtd: None | PaymentMethod4Code = field(
        default=None,
        metadata={
            "name": "PmtMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    mndt_rltd_inf: None | MandateRelatedInformation1 = field(
        default=None,
        metadata={
            "name": "MndtRltdInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rmt_inf: None | RemittanceInformation1 = field(
        default=None,
        metadata={
            "name": "RmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    ultmt_dbtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    dbtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    dbtr_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    dbtr_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "DbtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    dbtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "DbtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    cdtr_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "CdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    cdtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "CdtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    cdtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    cdtr_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    ultmt_cdtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "UltmtCdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class PaymentTransactionInformation2:
    rtr_id: None | str = field(
        default=None,
        metadata={
            "name": "RtrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_grp_inf: None | OriginalGroupInformation3 = field(
        default=None,
        metadata={
            "name": "OrgnlGrpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    orgnl_instr_id: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_end_to_end_id: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlEndToEndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_tx_id: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlTxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_intr_bk_sttlm_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "OrgnlIntrBkSttlmAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rtrd_intr_bk_sttlm_amt: CurrencyAndAmount = field(
        metadata={
            "name": "RtrdIntrBkSttlmAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rtrd_instd_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RtrdInstdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    xchg_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    compstn_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CompstnAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    chrg_br: None | ChargeBearerType1Code = field(
        default=None,
        metadata={
            "name": "ChrgBr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    chrgs_inf: list[ChargesInformation1] = field(
        default_factory=list,
        metadata={
            "name": "ChrgsInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    instg_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "InstgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    instd_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "InstdAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    rtr_rsn_inf: list[ReturnReasonInformation1] = field(
        default_factory=list,
        metadata={
            "name": "RtrRsnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    orgnl_tx_ref: None | OriginalTransactionReference1 = field(
        default=None,
        metadata={
            "name": "OrgnlTxRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class Pacs00400101:
    class Meta:
        name = "pacs.004.001.01"

    grp_hdr: GroupHeader6 = field(
        metadata={
            "name": "GrpHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
            "required": True,
        }
    )
    orgnl_grp_inf: None | OriginalGroupInformation2 = field(
        default=None,
        metadata={
            "name": "OrgnlGrpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )
    tx_inf: list[PaymentTransactionInformation2] = field(
        default_factory=list,
        metadata={
            "name": "TxInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.01"

    pacs_004_001_01: Pacs00400101 = field(
        metadata={
            "name": "pacs.004.001.01",
            "type": "Element",
            "required": True,
        }
    )
