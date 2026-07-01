from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05"


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


class AgreementFramework1Code(Enum):
    FBAA = "FBAA"
    BBAA = "BBAA"
    DERV = "DERV"
    ISDA = "ISDA"
    NONR = "NONR"


class CalculationMethod1Code(Enum):
    SIMP = "SIMP"
    COMP = "COMP"


class CollateralAccountType1Code(Enum):
    HOUS = "HOUS"
    CLIE = "CLIE"
    LIPR = "LIPR"
    MGIN = "MGIN"
    DFLT = "DFLT"


class CollateralPurpose1Code(Enum):
    VAMA = "VAMA"
    SINA = "SINA"


@dataclass(kw_only=True)
class DateAndDateTime2Choice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )


@dataclass(kw_only=True)
class DatePeriod2:
    fr_dt: XmlDate = field(
        metadata={
            "name": "FrDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    to_dt: XmlDate = field(
        metadata={
            "name": "ToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )


class ExposureType11Code(Enum):
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
class GenericIdentification30:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
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


class InterestMethod1Code(Enum):
    PHYS = "PHYS"
    ROLL = "ROLL"


class InterestRejectionReason1Code(Enum):
    VADA = "VADA"
    DIAM = "DIAM"


@dataclass(kw_only=True)
class PostalAddress2:
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd_id: str = field(
        metadata={
            "name": "PstCdId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 16,
        }
    )
    twn_nm: str = field(
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


class Status4Code(Enum):
    REJT = "REJT"
    PACK = "PACK"


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
class VariableInterest1Rate:
    indx: str = field(
        metadata={
            "name": "Indx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    bsis_pt_sprd: None | Decimal = field(
        default=None,
        metadata={
            "name": "BsisPtSprd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )


@dataclass(kw_only=True)
class AgreementFramework1Choice:
    agrmt_frmwk: None | AgreementFramework1Code = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    prtry_id: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )


@dataclass(kw_only=True)
class CollateralAccountIdentificationType3Choice:
    tp: None | CollateralAccountType1Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    prtry: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )


@dataclass(kw_only=True)
class CollateralBalance1:
    held_by_pty_a: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "HeldByPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    held_by_pty_b: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "HeldByPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CollateralPurpose1Choice:
    cd: None | CollateralPurpose1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )


@dataclass(kw_only=True)
class InterestRate1Choice:
    fxd_intrst_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "FxdIntrstRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    varbl_intrst_rate: None | VariableInterest1Rate = field(
        default=None,
        metadata={
            "name": "VarblIntrstRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress6:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    adr: PostalAddress2 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class RejectionReason21FormatChoice:
    cd: None | InterestRejectionReason1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Agreement4:
    agrmt_dtls: str = field(
        metadata={
            "name": "AgrmtDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "min_length": 1,
            "max_length": 140,
        },
    )
    agrmt_dt: XmlDate = field(
        metadata={
            "name": "AgrmtDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    base_ccy: str = field(
        metadata={
            "name": "BaseCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    agrmt_frmwk: None | AgreementFramework1Choice = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )


@dataclass(kw_only=True)
class BlockChainAddressWallet5:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 140,
        }
    )
    tp: None | CollateralAccountIdentificationType3Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class CollateralAccount3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tp: None | CollateralAccountIdentificationType3Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class InterestAmount3:
    acrd_intrst_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "AcrdIntrstAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    val_dt: DateAndDateTime2Choice = field(
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    intrst_mtd: InterestMethod1Code = field(
        metadata={
            "name": "IntrstMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    intrst_prd: DatePeriod2 = field(
        metadata={
            "name": "IntrstPrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    intrst_rate: None | InterestRate1Choice = field(
        default=None,
        metadata={
            "name": "IntrstRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    day_cnt_bsis: None | InterestComputationMethod2Code = field(
        default=None,
        metadata={
            "name": "DayCntBsis",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    apld_whldg_tax: None | bool = field(
        default=None,
        metadata={
            "name": "ApldWhldgTax",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    clctn_mtd: None | CalculationMethod1Code = field(
        default=None,
        metadata={
            "name": "ClctnMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    clctn_frqcy: None | Frequency1Code = field(
        default=None,
        metadata={
            "name": "ClctnFrqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    coll_purp: CollateralPurpose1Choice = field(
        metadata={
            "name": "CollPurp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    opng_coll_bal: None | CollateralBalance1 = field(
        default=None,
        metadata={
            "name": "OpngCollBal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    clsg_coll_bal: CollateralBalance1 = field(
        metadata={
            "name": "ClsgCollBal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    std_sttlm_instrs: None | str = field(
        default=None,
        metadata={
            "name": "StdSttlmInstrs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "min_length": 1,
            "max_length": 140,
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "min_length": 1,
            "max_length": 210,
        },
    )


@dataclass(kw_only=True)
class InterestResponse1:
    rspn_tp: Status4Code = field(
        metadata={
            "name": "RspnTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    rjctn_rsn: None | RejectionReason21FormatChoice = field(
        default=None,
        metadata={
            "name": "RjctnRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    rjctn_rsn_inf: None | str = field(
        default=None,
        metadata={
            "name": "RjctnRsnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "min_length": 1,
            "max_length": 140,
        },
    )
    intrst_pmt_req_id: str = field(
        metadata={
            "name": "IntrstPmtReqId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class PartyIdentification178Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    nm_and_adr: None | NameAndAddress6 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )


@dataclass(kw_only=True)
class Obligation9:
    pty_a: PartyIdentification178Choice = field(
        metadata={
            "name": "PtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    svcg_pty_a: None | PartyIdentification178Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    pty_b: PartyIdentification178Choice = field(
        metadata={
            "name": "PtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    svcg_pty_b: None | PartyIdentification178Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    coll_acct_id: None | CollateralAccount3 = field(
        default=None,
        metadata={
            "name": "CollAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    blck_chain_adr_or_wllt: None | BlockChainAddressWallet5 = field(
        default=None,
        metadata={
            "name": "BlckChainAdrOrWllt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    xpsr_tp: None | ExposureType11Code = field(
        default=None,
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    valtn_dt: DateAndDateTime2Choice = field(
        metadata={
            "name": "ValtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class InterestPaymentResponseV05:
    tx_id: str = field(
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    oblgtn: Obligation9 = field(
        metadata={
            "name": "Oblgtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    agrmt: Agreement4 = field(
        metadata={
            "name": "Agrmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    intrst_due_to_a: None | InterestAmount3 = field(
        default=None,
        metadata={
            "name": "IntrstDueToA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    intrst_due_to_b: None | InterestAmount3 = field(
        default=None,
        metadata={
            "name": "IntrstDueToB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )
    intrst_rspn: InterestResponse1 = field(
        metadata={
            "name": "IntrstRspn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
            "required": True,
        }
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.014.001.05"

    intrst_pmt_rspn: InterestPaymentResponseV05 = field(
        metadata={
            "name": "IntrstPmtRspn",
            "type": "Element",
            "required": True,
        }
    )
