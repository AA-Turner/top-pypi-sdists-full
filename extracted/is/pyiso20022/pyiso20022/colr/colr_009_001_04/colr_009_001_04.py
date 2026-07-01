from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04"


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


class CollateralAccountType1Code(Enum):
    HOUS = "HOUS"
    CLIE = "CLIE"
    LIPR = "LIPR"
    MGIN = "MGIN"
    DFLT = "DFLT"


@dataclass(kw_only=True)
class DateAndDateTimeChoice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )


class DisputeResolutionType1Code(Enum):
    RECO = "RECO"
    RMTA = "RMTA"
    RERO = "RERO"
    REVF = "REVF"
    RESA = "RESA"


class DisputeResolutionType2Code(Enum):
    RECO = "RECO"
    REEX = "REEX"
    RETH = "RETH"
    RMTA = "RMTA"
    RERO = "RERO"
    REVF = "REVF"
    RNIA = "RNIA"


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
class GenericIdentification30:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd_id: str = field(
        metadata={
            "name": "PstCdId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 16,
        }
    )
    twn_nm: str = field(
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
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
class CollateralAccountIdentificationType2Choice:
    tp: None | CollateralAccountType1Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    prtry: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )


@dataclass(kw_only=True)
class Dispute1:
    mrgn_call_req_id: str = field(
        metadata={
            "name": "MrgnCallReqId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    dsptd_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "DsptdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )
    dspt_dt: XmlDate = field(
        metadata={
            "name": "DsptDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DisputeResolutionType1Choice:
    cd: None | DisputeResolutionType1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    prtry_id: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )


@dataclass(kw_only=True)
class DisputeResolutionType2Choice:
    cd: None | DisputeResolutionType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    prtry_id: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress6:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    adr: PostalAddress2 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CollateralAccount2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    nm_and_adr: None | NameAndAddress6 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )


@dataclass(kw_only=True)
class SegregatedIndependentAmountDispute1:
    dspt_dtls: Dispute1 = field(
        metadata={
            "name": "DsptDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )
    dspt_rsltn_tp1_chc: list[DisputeResolutionType1Choice] = field(
        default_factory=list,
        metadata={
            "name": "DsptRsltnTp1Chc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )


@dataclass(kw_only=True)
class VariationMarginDispute1:
    dspt_dtls: Dispute1 = field(
        metadata={
            "name": "DsptDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )
    rsltn_tp_dtls: list[DisputeResolutionType2Choice] = field(
        default_factory=list,
        metadata={
            "name": "RsltnTpDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )


@dataclass(kw_only=True)
class DisputeNotification1:
    vartn_mrgn_dspt: VariationMarginDispute1 = field(
        metadata={
            "name": "VartnMrgnDspt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )
    sgrtd_indpdnt_amt_dspt: None | SegregatedIndependentAmountDispute1 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmtDspt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )


@dataclass(kw_only=True)
class Obligation4:
    pty_a: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )
    svcg_pty_a: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    pty_b: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )
    svcg_pty_b: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    coll_acct_id: None | CollateralAccount2 = field(
        default=None,
        metadata={
            "name": "CollAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    xpsr_tp: None | ExposureType5Code = field(
        default=None,
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    valtn_dt: DateAndDateTimeChoice = field(
        metadata={
            "name": "ValtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DisputeNotification1Choice:
    dspt_ntfctn_dtls: None | DisputeNotification1 = field(
        default=None,
        metadata={
            "name": "DsptNtfctnDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )
    sgrtd_indpdnt_amt_dspt_dtls: None | SegregatedIndependentAmountDispute1 = (
        field(
            default=None,
            metadata={
                "name": "SgrtdIndpdntAmtDsptDtls",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            },
        )
    )


@dataclass(kw_only=True)
class MarginCallDisputeNotificationV04:
    tx_id: str = field(
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    oblgtn: Obligation4 = field(
        metadata={
            "name": "Oblgtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )
    dspt_ntfctn: DisputeNotification1Choice = field(
        metadata={
            "name": "DsptNtfctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
            "required": True,
        }
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.009.001.04"

    mrgn_call_dspt_ntfctn: MarginCallDisputeNotificationV04 = field(
        metadata={
            "name": "MrgnCallDsptNtfctn",
            "type": "Element",
            "required": True,
        }
    )
