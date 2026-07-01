from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05"


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


class CollateralAccountType1Code(Enum):
    HOUS = "HOUS"
    CLIE = "CLIE"
    LIPR = "LIPR"
    MGIN = "MGIN"
    DFLT = "DFLT"


@dataclass(kw_only=True)
class DateAndDateTime2Choice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
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


@dataclass(kw_only=True)
class GenericIdentification30:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd_id: str = field(
        metadata={
            "name": "PstCdId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 16,
        }
    )
    twn_nm: str = field(
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


class RejectionReason68Code(Enum):
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
class AgreementFramework1Choice:
    agrmt_frmwk: None | AgreementFramework1Code = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    prtry_id: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )


@dataclass(kw_only=True)
class CollateralAccountIdentificationType3Choice:
    tp: None | CollateralAccountType1Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    prtry: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )


@dataclass(kw_only=True)
class CollateralSubstitutionResponse1:
    coll_sbstitn_req_id: str = field(
        metadata={
            "name": "CollSbstitnReqId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    accptd_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "AccptdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )


@dataclass(kw_only=True)
class CollateralSubstitutionResponse3:
    coll_sbstitn_req_id: str = field(
        metadata={
            "name": "CollSbstitnReqId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    rjctd_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "RjctdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )
    rjctn_rsn: RejectionReason68Code = field(
        metadata={
            "name": "RjctnRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )
    rjctn_rsn_inf: None | str = field(
        default=None,
        metadata={
            "name": "RjctnRsnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class NameAndAddress6:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    adr: PostalAddress2 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Agreement4:
    agrmt_dtls: str = field(
        metadata={
            "name": "AgrmtDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "min_length": 1,
            "max_length": 140,
        },
    )
    agrmt_dt: XmlDate = field(
        metadata={
            "name": "AgrmtDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )
    base_ccy: str = field(
        metadata={
            "name": "BaseCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    agrmt_frmwk: None | AgreementFramework1Choice = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )


@dataclass(kw_only=True)
class BlockChainAddressWallet5:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class PartyIdentification178Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    nm_and_adr: None | NameAndAddress6 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )


@dataclass(kw_only=True)
class SubstitutionResponse2:
    rspn_tp: Status4Code = field(
        metadata={
            "name": "RspnTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )
    coll_sbstitn_accptnc_dtls: None | CollateralSubstitutionResponse1 = field(
        default=None,
        metadata={
            "name": "CollSbstitnAccptncDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    coll_sbstitn_rjctn_dtls: None | CollateralSubstitutionResponse3 = field(
        default=None,
        metadata={
            "name": "CollSbstitnRjctnDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )


@dataclass(kw_only=True)
class Obligation9:
    pty_a: PartyIdentification178Choice = field(
        metadata={
            "name": "PtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )
    svcg_pty_a: None | PartyIdentification178Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    pty_b: PartyIdentification178Choice = field(
        metadata={
            "name": "PtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )
    svcg_pty_b: None | PartyIdentification178Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    coll_acct_id: None | CollateralAccount3 = field(
        default=None,
        metadata={
            "name": "CollAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    blck_chain_adr_or_wllt: None | BlockChainAddressWallet5 = field(
        default=None,
        metadata={
            "name": "BlckChainAdrOrWllt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    xpsr_tp: None | ExposureType11Code = field(
        default=None,
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    valtn_dt: DateAndDateTime2Choice = field(
        metadata={
            "name": "ValtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CollateralSubstitutionResponseV05:
    tx_id: str = field(
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    oblgtn: Obligation9 = field(
        metadata={
            "name": "Oblgtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )
    agrmt: None | Agreement4 = field(
        default=None,
        metadata={
            "name": "Agrmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )
    sbstitn_rspn: SubstitutionResponse2 = field(
        metadata={
            "name": "SbstitnRspn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
            "required": True,
        }
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.011.001.05"

    coll_sbstitn_rspn: CollateralSubstitutionResponseV05 = field(
        metadata={
            "name": "CollSbstitnRspn",
            "type": "Element",
            "required": True,
        }
    )
