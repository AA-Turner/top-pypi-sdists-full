from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01"


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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
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
class GenericIdentification3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


class Instruction4Code(Enum):
    PHOA = "PHOA"
    TELA = "TELA"


class Instruction5Code(Enum):
    PHOB = "PHOB"
    TELB = "TELB"


@dataclass(kw_only=True)
class PaymentIdentification2:
    instr_id: None | str = field(
        default=None,
        metadata={
            "name": "InstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    end_to_end_id: str = field(
        metadata={
            "name": "EndToEndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tx_id: str = field(
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


class Priority2Code(Enum):
    HIGH = "HIGH"
    NORM = "NORM"


@dataclass(kw_only=True)
class RemittanceInformation2:
    ustrd: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class RestrictedProprietaryChoice:
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class SettlementDateTimeIndication1:
    dbt_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DbtDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    cdt_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "CdtDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


class SettlementMethod1Code(Enum):
    INDA = "INDA"
    INGA = "INGA"
    COVE = "COVE"
    CLRG = "CLRG"


@dataclass(kw_only=True)
class SettlementTimeRequest1:
    clstm: XmlTime = field(
        metadata={
            "name": "CLSTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SimpleIdentificationInformation2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 34,
        }
    )


@dataclass(kw_only=True)
class AccountIdentification3Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "pattern": r"[a-zA-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    bban: None | str = field(
        default=None,
        metadata={
            "name": "BBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "pattern": r"[a-zA-Z0-9]{1,30}",
        },
    )
    upic: None | str = field(
        default=None,
        metadata={
            "name": "UPIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "pattern": r"[0-9]{8,17}",
        },
    )
    prtry_acct: None | SimpleIdentificationInformation2 = field(
        default=None,
        metadata={
            "name": "PrtryAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccountType2:
    cd: None | CashAccountType4Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class InstructionForCreditorAgent2:
    cd: None | Instruction5Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instr_inf: None | str = field(
        default=None,
        metadata={
            "name": "InstrInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class InstructionForNextAgent1:
    cd: None | Instruction4Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instr_inf: None | str = field(
        default=None,
        metadata={
            "name": "InstrInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class PaymentTypeInformation5:
    instr_prty: None | Priority2Code = field(
        default=None,
        metadata={
            "name": "InstrPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    svc_lvl: None | RestrictedProprietaryChoice = field(
        default=None,
        metadata={
            "name": "SvcLvl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    clr_chanl: None | ClearingChannel2Code = field(
        default=None,
        metadata={
            "name": "ClrChanl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    lcl_instrm: None | RestrictedProprietaryChoice = field(
        default=None,
        metadata={
            "name": "LclInstrm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


@dataclass(kw_only=True)
class PostalAddress1:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class BranchData:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccount7:
    id: AccountIdentification3Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    tp: None | CashAccountType2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification3:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress7:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    pstl_adr: PostalAddress1 = field(
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification5Choice:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    nm_and_adr: None | NameAndAddress7 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    cmbnd_id: None | FinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "CmbndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification3:
    fin_instn_id: FinancialInstitutionIdentification5Choice = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    brnch_id: None | BranchData = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


@dataclass(kw_only=True)
class CreditTransferTransactionInformation3:
    pmt_id: PaymentIdentification2 = field(
        metadata={
            "name": "PmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    pmt_tp_inf: None | PaymentTypeInformation5 = field(
        default=None,
        metadata={
            "name": "PmtTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    intr_bk_sttlm_amt: CurrencyAndAmount = field(
        metadata={
            "name": "IntrBkSttlmAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    sttlm_tm_indctn: None | SettlementDateTimeIndication1 = field(
        default=None,
        metadata={
            "name": "SttlmTmIndctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    sttlm_tm_req: None | SettlementTimeRequest1 = field(
        default=None,
        metadata={
            "name": "SttlmTmReq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    prvs_instg_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "PrvsInstgAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            },
        )
    )
    prvs_instg_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "PrvsInstgAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instg_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "InstgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instd_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "InstdAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    intrmy_agt1: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt1",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    intrmy_agt1_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt1Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    intrmy_agt2: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt2",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    intrmy_agt2_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt2Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    intrmy_agt3: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt3",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    intrmy_agt3_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt3Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    ultmt_dbtr: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    dbtr: BranchAndFinancialInstitutionIdentification3 = field(
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    dbtr_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    dbtr_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "DbtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    dbtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "DbtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    cdtr_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "CdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    cdtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "CdtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    cdtr: BranchAndFinancialInstitutionIdentification3 = field(
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    cdtr_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    ultmt_cdtr: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "UltmtCdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instr_for_cdtr_agt: list[InstructionForCreditorAgent2] = field(
        default_factory=list,
        metadata={
            "name": "InstrForCdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instr_for_nxt_agt: list[InstructionForNextAgent1] = field(
        default_factory=list,
        metadata={
            "name": "InstrForNxtAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    rmt_inf: None | RemittanceInformation2 = field(
        default=None,
        metadata={
            "name": "RmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


@dataclass(kw_only=True)
class SettlementInformation1:
    sttlm_mtd: SettlementMethod1Code = field(
        metadata={
            "name": "SttlmMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    sttlm_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "SttlmAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    clr_sys: None | ClearingSystemIdentification1Choice = field(
        default=None,
        metadata={
            "name": "ClrSys",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instg_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "InstgRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            },
        )
    )
    instg_rmbrsmnt_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "InstgRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "InstdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            },
        )
    )
    instd_rmbrsmnt_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "InstdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    thrd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "ThrdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            },
        )
    )
    thrd_rmbrsmnt_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "ThrdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


@dataclass(kw_only=True)
class GroupHeader4:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    btch_bookg: None | bool = field(
        default=None,
        metadata={
            "name": "BtchBookg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    nb_of_txs: str = field(
        metadata={
            "name": "NbOfTxs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
            "pattern": r"[0-9]{1,15}",
        }
    )
    ctrl_sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "CtrlSum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    ttl_intr_bk_sttlm_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlIntrBkSttlmAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    sttlm_inf: SettlementInformation1 = field(
        metadata={
            "name": "SttlmInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    pmt_tp_inf: None | PaymentTypeInformation5 = field(
        default=None,
        metadata={
            "name": "PmtTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instg_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "InstgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )
    instd_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "InstdAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
        },
    )


@dataclass(kw_only=True)
class Pacs00900101:
    class Meta:
        name = "pacs.009.001.01"

    grp_hdr: GroupHeader4 = field(
        metadata={
            "name": "GrpHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "required": True,
        }
    )
    cdt_trf_tx_inf: list[CreditTransferTransactionInformation3] = field(
        default_factory=list,
        metadata={
            "name": "CdtTrfTxInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.01"

    pacs_009_001_01: Pacs00900101 = field(
        metadata={
            "name": "pacs.009.001.01",
            "type": "Element",
            "required": True,
        }
    )
