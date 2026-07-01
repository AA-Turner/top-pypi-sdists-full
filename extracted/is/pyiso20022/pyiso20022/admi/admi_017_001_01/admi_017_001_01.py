from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01"


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


@dataclass(kw_only=True)
class ClearingSystemIdentification2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 5,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PartyIdentification44:
    any_bic: str = field(
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "required": True,
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        }
    )
    altrntv_idr: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AltrntvIdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "max_occurs": 10,
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PartyIdentification59:
    pty_nm: None | str = field(
        default=None,
        metadata={
            "name": "PtyNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 34,
        },
    )
    any_bic: None | PartyIdentification44 = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
        },
    )
    acct_nb: None | str = field(
        default=None,
        metadata={
            "name": "AcctNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 34,
        },
    )
    adr: None | str = field(
        default=None,
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 105,
        },
    )
    clr_sys_id: None | ClearingSystemIdentification2Choice = field(
        default=None,
        metadata={
            "name": "ClrSysId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
        },
    )
    lgl_ntty_idr: None | str = field(
        default=None,
        metadata={
            "name": "LglNttyIdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )


@dataclass(kw_only=True)
class PostalAddress1:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "max_occurs": 5,
            "min_length": 1,
            "max_length": 70,
        },
    )
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class NameAndAddress8:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 350,
        }
    )
    adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
        },
    )
    altrntv_idr: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AltrntvIdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "max_occurs": 10,
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PartyIdentification73Choice:
    nm_and_adr: None | NameAndAddress8 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
        },
    )
    any_bic: None | PartyIdentification44 = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
        },
    )
    pty_id: None | PartyIdentification59 = field(
        default=None,
        metadata={
            "name": "PtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
        },
    )


@dataclass(kw_only=True)
class RequestDetails19:
    tp: str = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    rqstr_id: None | PartyIdentification73Choice = field(
        default=None,
        metadata={
            "name": "RqstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
        },
    )
    addtl_req_inf: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AddtlReqInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ProcessingRequestV01:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "pattern": r"[a-zA-Z0-9]{4}",
        },
    )
    req: RequestDetails19 = field(
        metadata={
            "name": "Req",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:admi.017.001.01"

    prcg_req: ProcessingRequestV01 = field(
        metadata={
            "name": "PrcgReq",
            "type": "Element",
            "required": True,
        }
    )
