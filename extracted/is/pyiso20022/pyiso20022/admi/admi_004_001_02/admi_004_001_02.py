from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:admi.004.001.02"


@dataclass(kw_only=True)
class Event2:
    evt_cd: str = field(
        metadata={
            "name": "EvtCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.004.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 4,
            "pattern": r"[a-zA-Z0-9]{1,4}",
        }
    )
    evt_param: list[str] = field(
        default_factory=list,
        metadata={
            "name": "EvtParam",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.004.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    evt_desc: None | str = field(
        default=None,
        metadata={
            "name": "EvtDesc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.004.001.02",
            "min_length": 1,
            "max_length": 1000,
        },
    )
    evt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "EvtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.004.001.02",
        },
    )


@dataclass(kw_only=True)
class SystemEventNotificationV02:
    evt_inf: Event2 = field(
        metadata={
            "name": "EvtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.004.001.02",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:admi.004.001.02"

    sys_evt_ntfctn: SystemEventNotificationV02 = field(
        metadata={
            "name": "SysEvtNtfctn",
            "type": "Element",
            "required": True,
        }
    )
