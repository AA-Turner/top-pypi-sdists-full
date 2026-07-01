from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01"


@dataclass(kw_only=True)
class Case:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cretr: str = field(
        metadata={
            "name": "Cretr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "required": True,
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        }
    )
    reop_case_indctn: None | bool = field(
        default=None,
        metadata={
            "name": "ReopCaseIndctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
        },
    )


@dataclass(kw_only=True)
class CaseAssignment:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    assgnr: str = field(
        metadata={
            "name": "Assgnr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "required": True,
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        }
    )
    assgne: str = field(
        metadata={
            "name": "Assgne",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "required": True,
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "required": True,
        }
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


class InvestigationExecutionConfirmation1Code(Enum):
    CNCL = "CNCL"
    MODI = "MODI"
    ACDA = "ACDA"
    IPAY = "IPAY"
    ICOV = "ICOV"
    MCOV = "MCOV"
    IPYI = "IPYI"
    INFO = "INFO"
    CONF = "CONF"
    CWFW = "CWFW"


class PaymentCancellationRejection1Code(Enum):
    LEGL = "LEGL"
    AGNT = "AGNT"
    CUST = "CUST"


class PaymentModificationRejection1Code(Enum):
    UM01 = "UM01"
    UM02 = "UM02"
    UM03 = "UM03"
    UM04 = "UM04"
    UM05 = "UM05"
    UM06 = "UM06"
    UM07 = "UM07"
    UM08 = "UM08"
    UM09 = "UM09"
    UM10 = "UM10"
    UM11 = "UM11"
    UM12 = "UM12"
    UM13 = "UM13"
    UM14 = "UM14"
    UM15 = "UM15"
    UM16 = "UM16"
    UM17 = "UM17"
    UM18 = "UM18"
    UM19 = "UM19"
    UM20 = "UM20"
    UM21 = "UM21"


@dataclass(kw_only=True)
class PaymentInstructionExtract:
    assgnr_instr_id: None | str = field(
        default=None,
        metadata={
            "name": "AssgnrInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    assgne_instr_id: None | str = field(
        default=None,
        metadata={
            "name": "AssgneInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ccy_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CcyAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
        },
    )
    val_dt: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
        },
    )


@dataclass(kw_only=True)
class RejectedCancellationJustification:
    rsn_cd: PaymentCancellationRejection1Code = field(
        metadata={
            "name": "RsnCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "required": True,
        }
    )
    rsn: None | str = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class InvestigationStatusChoice:
    conf: None | InvestigationExecutionConfirmation1Code = field(
        default=None,
        metadata={
            "name": "Conf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
        },
    )
    rjctd_mod: list[PaymentModificationRejection1Code] = field(
        default_factory=list,
        metadata={
            "name": "RjctdMod",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "max_occurs": 14,
        },
    )
    rjctd_cxl: None | RejectedCancellationJustification = field(
        default=None,
        metadata={
            "name": "RjctdCxl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
        },
    )
    dplct_of: None | Case = field(
        default=None,
        metadata={
            "name": "DplctOf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
        },
    )
    assgnmt_cxl_conf: None | bool = field(
        default=None,
        metadata={
            "name": "AssgnmtCxlConf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
        },
    )


@dataclass(kw_only=True)
class Camt02900101:
    class Meta:
        name = "camt.029.001.01"

    assgnmt: CaseAssignment = field(
        metadata={
            "name": "Assgnmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "required": True,
        }
    )
    rslvd_case: Case = field(
        metadata={
            "name": "RslvdCase",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
            "required": True,
        }
    )
    sts: None | InvestigationStatusChoice = field(
        default=None,
        metadata={
            "name": "Sts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
        },
    )
    crrctn_tx: None | PaymentInstructionExtract = field(
        default=None,
        metadata={
            "name": "CrrctnTx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:camt.029.001.01"

    camt_029_001_01: Camt02900101 = field(
        metadata={
            "name": "camt.029.001.01",
            "type": "Element",
            "required": True,
        }
    )
