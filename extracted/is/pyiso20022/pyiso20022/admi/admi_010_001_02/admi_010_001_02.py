from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02"


@dataclass(kw_only=True)
class ReportParameter1:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    val: str = field(
        metadata={
            "name": "Val",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 350,
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
class RequestDetails4:
    key: str = field(
        metadata={
            "name": "Key",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    rpt_data: list[ReportParameter1] = field(
        default_factory=list,
        metadata={
            "name": "RptData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
        },
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class RequestDetails5:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    req_ref: str = field(
        metadata={
            "name": "ReqRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    rpt_key: list[RequestDetails4] = field(
        default_factory=list,
        metadata={
            "name": "RptKey",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class StaticDataReportV02:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    sttlm_ssn_idr: None | str = field(
        default=None,
        metadata={
            "name": "SttlmSsnIdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "pattern": r"[a-zA-Z0-9]{4}",
        },
    )
    rpt_dtls: RequestDetails5 = field(
        metadata={
            "name": "RptDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
            "required": True,
        }
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:admi.010.001.02"

    statc_data_rpt: StaticDataReportV02 = field(
        metadata={
            "name": "StatcDataRpt",
            "type": "Element",
            "required": True,
        }
    )
