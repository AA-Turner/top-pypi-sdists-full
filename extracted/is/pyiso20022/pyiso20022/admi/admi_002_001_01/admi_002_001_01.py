from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01"


@dataclass(kw_only=True)
class MessageReference:
    ref: str = field(
        metadata={
            "name": "Ref",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class RejectionReason2:
    rjctg_pty_rsn: str = field(
        metadata={
            "name": "RjctgPtyRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    rjctn_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "RjctnDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01",
        },
    )
    err_lctn: None | str = field(
        default=None,
        metadata={
            "name": "ErrLctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01",
            "min_length": 1,
            "max_length": 350,
        },
    )
    rsn_desc: None | str = field(
        default=None,
        metadata={
            "name": "RsnDesc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01",
            "min_length": 1,
            "max_length": 350,
        },
    )
    addtl_data: None | str = field(
        default=None,
        metadata={
            "name": "AddtlData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01",
            "min_length": 1,
            "max_length": 20000,
        },
    )


@dataclass(kw_only=True)
class Admi00200101:
    class Meta:
        name = "admi.002.001.01"

    rltd_ref: MessageReference = field(
        metadata={
            "name": "RltdRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01",
            "required": True,
        }
    )
    rsn: RejectionReason2 = field(
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:admi.002.001.01"

    admi_002_001_01: Admi00200101 = field(
        metadata={
            "name": "admi.002.001.01",
            "type": "Element",
            "required": True,
        }
    )
