from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01"


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


@dataclass(kw_only=True)
class GenericIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class OriginalBusinessQuery1:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    msg_nm_id: None | str = field(
        default=None,
        metadata={
            "name": "MsgNmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cre_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )


@dataclass(kw_only=True)
class SequenceRange1:
    fr_seq: str = field(
        metadata={
            "name": "FrSeq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    to_seq: str = field(
        metadata={
            "name": "ToSeq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
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
class PostalAddress1:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class RequestType4Choice:
    pmt_ctrl: None | str = field(
        default=None,
        metadata={
            "name": "PmtCtrl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    enqry: None | str = field(
        default=None,
        metadata={
            "name": "Enqry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )


@dataclass(kw_only=True)
class SequenceRange1Choice:
    fr_seq: None | str = field(
        default=None,
        metadata={
            "name": "FrSeq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    to_seq: None | str = field(
        default=None,
        metadata={
            "name": "ToSeq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    fr_to_seq: list[SequenceRange1] = field(
        default_factory=list,
        metadata={
            "name": "FrToSeq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )
    eqseq: list[str] = field(
        default_factory=list,
        metadata={
            "name": "EQSeq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    neqseq: list[str] = field(
        default_factory=list,
        metadata={
            "name": "NEQSeq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class MessageHeader7:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )
    req_tp: None | RequestType4Choice = field(
        default=None,
        metadata={
            "name": "ReqTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )
    orgnl_biz_qry: None | OriginalBusinessQuery1 = field(
        default=None,
        metadata={
            "name": "OrgnlBizQry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )
    qry_nm: None | str = field(
        default=None,
        metadata={
            "name": "QryNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class NameAndAddress5:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification120Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )
    nm_and_adr: None | NameAndAddress5 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification136:
    id: PartyIdentification120Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
        }
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )


@dataclass(kw_only=True)
class ResendSearchCriteria2:
    biz_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "BizDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )
    seq_nb: None | str = field(
        default=None,
        metadata={
            "name": "SeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    seq_rg: None | SequenceRange1Choice = field(
        default=None,
        metadata={
            "name": "SeqRg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )
    orgnl_msg_nm_id: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlMsgNmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    file_ref: None | str = field(
        default=None,
        metadata={
            "name": "FileRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rcpt: PartyIdentification136 = field(
        metadata={
            "name": "Rcpt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ResendRequestV01:
    msg_hdr: MessageHeader7 = field(
        metadata={
            "name": "MsgHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "required": True,
        }
    )
    rsnd_sch_crit: list[ResendSearchCriteria2] = field(
        default_factory=list,
        metadata={
            "name": "RsndSchCrit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
            "min_occurs": 1,
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:admi.006.001.01"

    rsnd_req: ResendRequestV01 = field(
        metadata={
            "name": "RsndReq",
            "type": "Element",
            "required": True,
        }
    )
