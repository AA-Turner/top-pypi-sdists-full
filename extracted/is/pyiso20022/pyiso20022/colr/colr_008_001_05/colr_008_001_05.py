from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05"


@dataclass(kw_only=True)
class AccountSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )


class CollateralAccountType1Code(Enum):
    HOUS = "HOUS"
    CLIE = "CLIE"
    LIPR = "LIPR"
    MGIN = "MGIN"
    DFLT = "DFLT"


class CollateralProposalResponse1Code(Enum):
    INPR = "INPR"
    COPR = "COPR"


@dataclass(kw_only=True)
class DateAndDateTimeChoice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )


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
class GenericIdentification36:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PostalAddress2:
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd_id: str = field(
        metadata={
            "name": "PstCdId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 16,
        }
    )
    twn_nm: str = field(
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


class RejectionReasonV021Code(Enum):
    DSEC = "DSEC"
    EVNM = "EVNM"
    UKWN = "UKWN"
    ICOL = "ICOL"
    CONL = "CONL"
    ELIG = "ELIG"
    INID = "INID"
    OTHR = "OTHR"


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
class CollateralAccountIdentificationType3Choice:
    tp: None | CollateralAccountType1Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    prtry: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )


@dataclass(kw_only=True)
class GenericAccountIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    adr: PostalAddress2 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class OtherCollateralResponse2:
    rspn_tp: Status4Code = field(
        metadata={
            "name": "RspnTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )
    coll_id: None | str = field(
        default=None,
        metadata={
            "name": "CollId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )
    asst_nb: None | str = field(
        default=None,
        metadata={
            "name": "AsstNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rjctn_rsn: None | RejectionReasonV021Code = field(
        default=None,
        metadata={
            "name": "RjctnRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    rjctn_inf: None | str = field(
        default=None,
        metadata={
            "name": "RjctnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class SecuritiesCollateralResponse1:
    coll_id: None | str = field(
        default=None,
        metadata={
            "name": "CollId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )
    asst_nb: None | str = field(
        default=None,
        metadata={
            "name": "AsstNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rspn_tp: Status4Code = field(
        metadata={
            "name": "RspnTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )
    rjctn_rsn: None | RejectionReasonV021Code = field(
        default=None,
        metadata={
            "name": "RjctnRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    rjctn_inf: None | str = field(
        default=None,
        metadata={
            "name": "RjctnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class AccountIdentification4Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "pattern": r"[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    othr: None | GenericAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )


@dataclass(kw_only=True)
class CollateralAccount3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class PartyIdentification100Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    nm_and_adr: None | NameAndAddress6 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )


@dataclass(kw_only=True)
class CashCollateralResponse2:
    rspn_tp: Status4Code = field(
        metadata={
            "name": "RspnTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )
    coll_id: None | str = field(
        default=None,
        metadata={
            "name": "CollId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )
    asst_nb: None | str = field(
        default=None,
        metadata={
            "name": "AsstNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )
    csh_acct_id: None | AccountIdentification4Choice = field(
        default=None,
        metadata={
            "name": "CshAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    rjctn_rsn: None | RejectionReasonV021Code = field(
        default=None,
        metadata={
            "name": "RjctnRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    rjctn_inf: None | str = field(
        default=None,
        metadata={
            "name": "RjctnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class Obligation5:
    pty_a: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )
    svcg_pty_a: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    pty_b: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )
    svcg_pty_b: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    coll_acct_id: None | CollateralAccount3 = field(
        default=None,
        metadata={
            "name": "CollAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    xpsr_tp: None | ExposureType5Code = field(
        default=None,
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    valtn_dt: DateAndDateTimeChoice = field(
        metadata={
            "name": "ValtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CollateralResponse2:
    scties_coll_rspn: list[SecuritiesCollateralResponse1] = field(
        default_factory=list,
        metadata={
            "name": "SctiesCollRspn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    csh_coll_rspn: list[CashCollateralResponse2] = field(
        default_factory=list,
        metadata={
            "name": "CshCollRspn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    othr_coll_rspn: list[OtherCollateralResponse2] = field(
        default_factory=list,
        metadata={
            "name": "OthrCollRspn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )


@dataclass(kw_only=True)
class CollateralProposalResponseType3:
    coll_prpsl_id: str = field(
        metadata={
            "name": "CollPrpslId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tp: CollateralProposalResponse1Code = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )
    rspn: CollateralResponse2 = field(
        metadata={
            "name": "Rspn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CollateralProposalResponse3:
    vartn_mrgn: CollateralProposalResponseType3 = field(
        metadata={
            "name": "VartnMrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )
    sgrtd_indpdnt_amt: None | CollateralProposalResponseType3 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )


@dataclass(kw_only=True)
class CollateralProposalResponse3Choice:
    coll_prpsl: None | CollateralProposalResponse3 = field(
        default=None,
        metadata={
            "name": "CollPrpsl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )
    sgrtd_indpdnt_amt: None | CollateralProposalResponseType3 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )


@dataclass(kw_only=True)
class CollateralProposalResponseV05:
    tx_id: str = field(
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    oblgtn: Obligation5 = field(
        metadata={
            "name": "Oblgtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )
    prpsl_rspn: CollateralProposalResponse3Choice = field(
        metadata={
            "name": "PrpslRspn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
            "required": True,
        }
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.008.001.05"

    coll_prpsl_rspn: CollateralProposalResponseV05 = field(
        metadata={
            "name": "CollPrpslRspn",
            "type": "Element",
            "required": True,
        }
    )
