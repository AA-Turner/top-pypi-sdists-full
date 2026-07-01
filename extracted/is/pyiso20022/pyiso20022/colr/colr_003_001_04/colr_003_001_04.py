from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04"


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


class CollateralType1Code(Enum):
    CASH = "CASH"
    SECU = "SECU"
    LCRE = "LCRE"
    OTHR = "OTHR"


@dataclass(kw_only=True)
class DateAndDateTimeChoice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


class ExposureConventionType1Code(Enum):
    GROS = "GROS"
    NET1 = "NET1"


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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )


class IndependentAmountConventionType1Code(Enum):
    NBTR = "NBTR"
    NATR = "NATR"
    SEGR = "SEGR"


@dataclass(kw_only=True)
class PostalAddress2:
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd_id: str = field(
        metadata={
            "name": "PstCdId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 16,
        }
    )
    twn_nm: str = field(
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


class RoundingMethod1Code(Enum):
    DRDW = "DRDW"
    DRUP = "DRUP"
    NONE = "NONE"
    CLSR = "CLSR"


@dataclass(kw_only=True)
class SupplementaryDataEnvelope1:
    any_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


class ThresholdType1Code(Enum):
    SECU = "SECU"
    UNSE = "UNSE"


@dataclass(kw_only=True)
class AgreementFramework1Choice:
    agrmt_frmwk: None | AgreementFramework1Code = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    prtry_id: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralAccountIdentificationType2Choice:
    tp: None | CollateralAccountType1Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    prtry: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralMovement9:
    coll_tp: CollateralType1Code = field(
        metadata={
            "name": "CollTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class IndependentAmount1:
    amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    cnvntn: IndependentAmountConventionType1Code = field(
        metadata={
            "name": "Cnvntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class IndependentAmount2:
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "min_length": 1,
            "max_length": 140,
        },
    )
    amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    cnvntn: IndependentAmountConventionType1Code = field(
        metadata={
            "name": "Cnvntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class MarginCollateral1:
    held_by_pty_a: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "HeldByPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    held_by_pty_b: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "HeldByPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    prr_agrd_to_pty_a: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "PrrAgrdToPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    prr_agrd_to_pty_b: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "PrrAgrdToPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    in_trnst_to_pty_a: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "InTrnstToPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    in_trnst_to_pty_b: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "InTrnstToPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class MarginRequirement1:
    dlvr_mrgn_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DlvrMrgnAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    rtr_mrgn_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RtrMrgnAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress6:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    adr: PostalAddress2 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Result1:
    due_to_pty_a: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DueToPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    due_to_pty_b: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DueToPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "min_length": 1,
            "max_length": 210,
        },
    )


@dataclass(kw_only=True)
class SegregatedIndependentAmountMargin1:
    min_trf_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "MinTrfAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    rndg_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RndgAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    rndg_mtd: None | RoundingMethod1Code = field(
        default=None,
        metadata={
            "name": "RndgMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class VariationMargin1:
    thrshld_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "ThrshldAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    thrshld_tp: None | ThresholdType1Code = field(
        default=None,
        metadata={
            "name": "ThrshldTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    min_trf_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "MinTrfAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    rndg_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "RndgAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    rndg_mtd: RoundingMethod1Code = field(
        metadata={
            "name": "RndgMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class AggregatedIndependentAmount1:
    trad: None | IndependentAmount1 = field(
        default=None,
        metadata={
            "name": "Trad",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    val_at_rsk: None | IndependentAmount1 = field(
        default=None,
        metadata={
            "name": "ValAtRsk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    net_opn_pos: None | IndependentAmount1 = field(
        default=None,
        metadata={
            "name": "NetOpnPos",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    othr_amt: list[IndependentAmount2] = field(
        default_factory=list,
        metadata={
            "name": "OthrAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class Agreement4:
    agrmt_dtls: str = field(
        metadata={
            "name": "AgrmtDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "min_length": 1,
            "max_length": 140,
        },
    )
    agrmt_dt: XmlDate = field(
        metadata={
            "name": "AgrmtDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    base_ccy: str = field(
        metadata={
            "name": "BaseCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    agrmt_frmwk: None | AgreementFramework1Choice = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class Collateral1:
    vartn_mrgn: MarginCollateral1 = field(
        metadata={
            "name": "VartnMrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    sgrtd_indpdnt_amt: None | MarginCollateral1 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralAccount2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class ExpectedCollateralMovement2:
    dlvry: list[CollateralMovement9] = field(
        default_factory=list,
        metadata={
            "name": "Dlvry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    rtr: list[CollateralMovement9] = field(
        default_factory=list,
        metadata={
            "name": "Rtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class Margin1:
    vartn_mrgn: VariationMargin1 = field(
        metadata={
            "name": "VartnMrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    sgrtd_indpdnt_amt_mrgn: None | SegregatedIndependentAmountMargin1 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmtMrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class MarginCallResult2:
    vartn_mrgn_rslt: Result1 = field(
        metadata={
            "name": "VartnMrgnRslt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    sgrtd_indpdnt_amt: None | Result1 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification100Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    nm_and_adr: None | NameAndAddress6 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class Requirement1:
    vartn_mrgn_rqrmnt: MarginRequirement1 = field(
        metadata={
            "name": "VartnMrgnRqrmnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    sgrtd_indpdnt_amt_rqrmnt: None | MarginRequirement1 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmtRqrmnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralBalance1Choice:
    ttl_coll: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    coll_dtls: None | Collateral1 = field(
        default=None,
        metadata={
            "name": "CollDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    sgrtd_indpdnt_amt: None | MarginCollateral1 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class ExpectedCollateral2:
    vartn_mrgn: ExpectedCollateralMovement2 = field(
        metadata={
            "name": "VartnMrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    sgrtd_indpdnt_amt: None | ExpectedCollateralMovement2 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class MarginCallResult2Choice:
    mrgn_call_rslt_dtls: None | MarginCallResult2 = field(
        default=None,
        metadata={
            "name": "MrgnCallRsltDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    mrgn_call_amt: None | Result1 = field(
        default=None,
        metadata={
            "name": "MrgnCallAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    sgrtd_indpdnt_amt: None | Result1 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class MarginRequirement1Choice:
    mrgn_rqrmnt: None | Requirement1 = field(
        default=None,
        metadata={
            "name": "MrgnRqrmnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    sgrtd_indpdnt_amt_rqrmnt: None | MarginRequirement1 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmtRqrmnt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class MarginTerms1Choice:
    mrgn_dtls: None | Margin1 = field(
        default=None,
        metadata={
            "name": "MrgnDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    sgrtd_indpdnt_amt_mrgn: None | SegregatedIndependentAmountMargin1 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmtMrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class Obligation4:
    pty_a: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    svcg_pty_a: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    pty_b: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    svcg_pty_b: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    coll_acct_id: None | CollateralAccount2 = field(
        default=None,
        metadata={
            "name": "CollAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    xpsr_tp: None | ExposureType5Code = field(
        default=None,
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    valtn_dt: DateAndDateTimeChoice = field(
        metadata={
            "name": "ValtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ExpectedCollateral2Choice:
    xpctd_coll_dtls: None | ExpectedCollateral2 = field(
        default=None,
        metadata={
            "name": "XpctdCollDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    sgrtd_indpdnt_amt: None | ExpectedCollateralMovement2 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class MarginCall1:
    xpsd_amt_pty_a: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "XpsdAmtPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    xpsd_amt_pty_b: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "XpsdAmtPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    xpsr_cnvntn: None | ExposureConventionType1Code = field(
        default=None,
        metadata={
            "name": "XpsrCnvntn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    indpdnt_amt_pty_a: None | AggregatedIndependentAmount1 = field(
        default=None,
        metadata={
            "name": "IndpdntAmtPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    indpdnt_amt_pty_b: None | AggregatedIndependentAmount1 = field(
        default=None,
        metadata={
            "name": "IndpdntAmtPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    mrgn_terms: None | MarginTerms1Choice = field(
        default=None,
        metadata={
            "name": "MrgnTerms",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    coll_bal: None | CollateralBalance1Choice = field(
        default=None,
        metadata={
            "name": "CollBal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class MarginCallResult3:
    dflt_fnd_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DfltFndAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    mrgn_call_rslt: MarginCallResult2Choice = field(
        metadata={
            "name": "MrgnCallRslt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class MarginCall2:
    coll_acct_id: None | CollateralAccount2 = field(
        default=None,
        metadata={
            "name": "CollAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    mrgn_call_rslt: MarginCallResult3 = field(
        metadata={
            "name": "MrgnCallRslt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    mrgn_dtl_due_to_a: None | MarginCall1 = field(
        default=None,
        metadata={
            "name": "MrgnDtlDueToA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    mrgn_dtl_due_to_b: None | MarginCall1 = field(
        default=None,
        metadata={
            "name": "MrgnDtlDueToB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    rqrmnt_dtls_due_to_a: None | MarginRequirement1Choice = field(
        default=None,
        metadata={
            "name": "RqrmntDtlsDueToA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    rqrmnt_dtls_due_to_b: None | MarginRequirement1Choice = field(
        default=None,
        metadata={
            "name": "RqrmntDtlsDueToB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    xpctd_coll_due_to_a: None | ExpectedCollateral2Choice = field(
        default=None,
        metadata={
            "name": "XpctdCollDueToA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    xpctd_coll_due_to_b: None | ExpectedCollateral2Choice = field(
        default=None,
        metadata={
            "name": "XpctdCollDueToB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class MarginCallRequestV04:
    tx_id: str = field(
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    oblgtn: Obligation4 = field(
        metadata={
            "name": "Oblgtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    agrmt: None | Agreement4 = field(
        default=None,
        metadata={
            "name": "Agrmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    mrgn_call_rslt: MarginCallResult3 = field(
        metadata={
            "name": "MrgnCallRslt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
            "required": True,
        }
    )
    mrgn_dtls_due_to_a: None | MarginCall1 = field(
        default=None,
        metadata={
            "name": "MrgnDtlsDueToA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    mrgn_dtls_due_to_b: None | MarginCall1 = field(
        default=None,
        metadata={
            "name": "MrgnDtlsDueToB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    rqrmnt_dtls_due_to_a: None | MarginRequirement1Choice = field(
        default=None,
        metadata={
            "name": "RqrmntDtlsDueToA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    rqrmnt_dtls_due_to_b: None | MarginRequirement1Choice = field(
        default=None,
        metadata={
            "name": "RqrmntDtlsDueToB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    xpctd_coll_due_to_a: None | ExpectedCollateral2Choice = field(
        default=None,
        metadata={
            "name": "XpctdCollDueToA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    xpctd_coll_due_to_b: None | ExpectedCollateral2Choice = field(
        default=None,
        metadata={
            "name": "XpctdCollDueToB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    mrgn_call_dtls: list[MarginCall2] = field(
        default_factory=list,
        metadata={
            "name": "MrgnCallDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.003.001.04"

    mrgn_call_req: MarginCallRequestV04 = field(
        metadata={
            "name": "MrgnCallReq",
            "type": "Element",
            "required": True,
        }
    )
