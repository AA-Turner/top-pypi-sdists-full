from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01"


@dataclass(kw_only=True)
class Event1:
    evt_cd: str = field(
        metadata={
            "name": "EvtCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    evt_desc: None | str = field(
        default=None,
        metadata={
            "name": "EvtDesc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
            "min_length": 1,
            "max_length": 350,
        },
    )
    evt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "EvtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
        },
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
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SystemEventAcknowledgementV01:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    orgtr_ref: None | str = field(
        default=None,
        metadata={
            "name": "OrgtrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    sttlm_ssn_idr: None | str = field(
        default=None,
        metadata={
            "name": "SttlmSsnIdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
            "pattern": r"[a-zA-Z0-9]{4}",
        },
    )
    ack_dtls: None | Event1 = field(
        default=None,
        metadata={
            "name": "AckDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:admi.011.001.01"

    sys_evt_ack: SystemEventAcknowledgementV01 = field(
        metadata={
            "name": "SysEvtAck",
            "type": "Element",
            "required": True,
        }
    )
