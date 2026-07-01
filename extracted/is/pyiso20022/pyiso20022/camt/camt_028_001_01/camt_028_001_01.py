from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01"


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


@dataclass(kw_only=True)
class Case:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cretr: str = field(
        metadata={
            "name": "Cretr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        }
    )
    reop_case_indctn: None | bool = field(
        default=None,
        metadata={
            "name": "ReopCaseIndctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class CaseAssignment:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    assgnr: str = field(
        metadata={
            "name": "Assgnr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        }
    )
    assgne: str = field(
        metadata={
            "name": "Assgne",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )


class CashAccountType3Code(Enum):
    CASH = "CASH"
    CHAR = "CHAR"
    SACC = "SACC"
    CACC = "CACC"
    SVGS = "SVGS"


@dataclass(kw_only=True)
class ClearingSystemMemberIdentificationChoice:
    uschu: None | str = field(
        default=None,
        metadata={
            "name": "USCHU",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"CH[0-9]{6,6}",
        },
    )
    nzncc: None | str = field(
        default=None,
        metadata={
            "name": "NZNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"NZ[0-9]{6,6}",
        },
    )
    iensc: None | str = field(
        default=None,
        metadata={
            "name": "IENSC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"IE[0-9]{6,6}",
        },
    )
    gbsc: None | str = field(
        default=None,
        metadata={
            "name": "GBSC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"SC[0-9]{6,6}",
        },
    )
    usch: None | str = field(
        default=None,
        metadata={
            "name": "USCH",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"CP[0-9]{4,4}",
        },
    )
    chbc: None | str = field(
        default=None,
        metadata={
            "name": "CHBC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"SW[0-9]{3,5}",
        },
    )
    usfw: None | str = field(
        default=None,
        metadata={
            "name": "USFW",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"FW[0-9]{9,9}",
        },
    )
    ptncc: None | str = field(
        default=None,
        metadata={
            "name": "PTNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"PT[0-9]{8,8}",
        },
    )
    rucb: None | str = field(
        default=None,
        metadata={
            "name": "RUCB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"RU[0-9]{9,9}",
        },
    )
    itncc: None | str = field(
        default=None,
        metadata={
            "name": "ITNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"IT[0-9]{10,10}",
        },
    )
    atblz: None | str = field(
        default=None,
        metadata={
            "name": "ATBLZ",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"AT[0-9]{5,5}",
        },
    )
    cacpa: None | str = field(
        default=None,
        metadata={
            "name": "CACPA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"CA[0-9]{9,9}",
        },
    )
    chsic: None | str = field(
        default=None,
        metadata={
            "name": "CHSIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"SW[0-9]{6,6}",
        },
    )
    deblz: None | str = field(
        default=None,
        metadata={
            "name": "DEBLZ",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"BL[0-9]{8,8}",
        },
    )
    esncc: None | str = field(
        default=None,
        metadata={
            "name": "ESNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"ES[0-9]{8,9}",
        },
    )
    zancc: None | str = field(
        default=None,
        metadata={
            "name": "ZANCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"ZA[0-9]{6,6}",
        },
    )
    hkncc: None | str = field(
        default=None,
        metadata={
            "name": "HKNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"HK[0-9]{3,3}",
        },
    )
    aubsbx: None | str = field(
        default=None,
        metadata={
            "name": "AUBSBx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"AU[0-9]{6,6}",
        },
    )
    aubsbs: None | str = field(
        default=None,
        metadata={
            "name": "AUBSBs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"AU[0-9]{6,6}",
        },
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


class DocumentType1Code(Enum):
    MSIN = "MSIN"
    CNFA = "CNFA"
    DNFA = "DNFA"
    CINV = "CINV"
    CREN = "CREN"
    DEBN = "DEBN"
    HIRI = "HIRI"
    SBIN = "SBIN"
    RADM = "RADM"
    RPIN = "RPIN"
    CMCN = "CMCN"
    FXDR = "FXDR"
    SOAC = "SOAC"


@dataclass(kw_only=True)
class GenericIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification4:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    id_tp: str = field(
        metadata={
            "name": "IdTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class SimpleIdentificationInformation:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class StructuredLongPostalAddress1:
    bldg_nm: None | str = field(
        default=None,
        metadata={
            "name": "BldgNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    strt_bldg_id: None | str = field(
        default=None,
        metadata={
            "name": "StrtBldgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    flr: None | str = field(
        default=None,
        metadata={
            "name": "Flr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: str = field(
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    dstrct_nm: None | str = field(
        default=None,
        metadata={
            "name": "DstrctNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rgn_id: None | str = field(
        default=None,
        metadata={
            "name": "RgnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    stat: None | str = field(
        default=None,
        metadata={
            "name": "Stat",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cty_id: None | str = field(
        default=None,
        metadata={
            "name": "CtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )
    pst_cd_id: str = field(
        metadata={
            "name": "PstCdId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 16,
        }
    )
    pob: None | str = field(
        default=None,
        metadata={
            "name": "POB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )


@dataclass(kw_only=True)
class AccountIdentification1:
    prtry: SimpleIdentificationInformation = field(
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class AccountIdentification1Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"[a-zA-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    bban: None | str = field(
        default=None,
        metadata={
            "name": "BBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"[a-zA-Z0-9]{1,30}",
        },
    )
    upic: None | str = field(
        default=None,
        metadata={
            "name": "UPIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"[0-9]{8,17}",
        },
    )
    dmst_acct: None | SimpleIdentificationInformation = field(
        default=None,
        metadata={
            "name": "DmstAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class EquivalentAmount:
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )
    ccy_of_trf: str = field(
        metadata={
            "name": "CcyOfTrf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )


@dataclass(kw_only=True)
class LongPostalAddress1Choice:
    ustrd: None | str = field(
        default=None,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    strd: None | StructuredLongPostalAddress1 = field(
        default=None,
        metadata={
            "name": "Strd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class NonFinancialInstitutionIdentification1:
    bei: None | str = field(
        default=None,
        metadata={
            "name": "BEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    eangln: None | str = field(
        default=None,
        metadata={
            "name": "EANGLN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"[0-9]{13,13}",
        },
    )
    uschu: None | str = field(
        default=None,
        metadata={
            "name": "USCHU",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"CH[0-9]{6,6}",
        },
    )
    duns: None | str = field(
        default=None,
        metadata={
            "name": "DUNS",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"[0-9]{9,9}",
        },
    )
    bk_pty_id: None | str = field(
        default=None,
        metadata={
            "name": "BkPtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class PaymentInstructionExtract:
    assgnr_instr_id: None | str = field(
        default=None,
        metadata={
            "name": "AssgnrInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    assgne_instr_id: None | str = field(
        default=None,
        metadata={
            "name": "AssgneInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ccy_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CcyAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    val_dt: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class PersonIdentification2:
    drvrs_lic_nb: None | str = field(
        default=None,
        metadata={
            "name": "DrvrsLicNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    scl_scty_nb: None | str = field(
        default=None,
        metadata={
            "name": "SclSctyNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    aln_regn_nb: None | str = field(
        default=None,
        metadata={
            "name": "AlnRegnNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pspt_nb: None | str = field(
        default=None,
        metadata={
            "name": "PsptNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    idnty_card_nb: None | str = field(
        default=None,
        metadata={
            "name": "IdntyCardNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    mplyr_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "MplyrIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    othr_id: None | GenericIdentification4 = field(
        default=None,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PostalAddress1:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class ReferredDocumentAmount1Choice:
    due_pybl_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DuePyblAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    dscnt_apld_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DscntApldAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    rmtd_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RmtdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    cdt_note_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CdtNoteAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    tax_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class AmountType1Choice:
    instd_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "InstdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    eqvt_amt: None | EquivalentAmount = field(
        default=None,
        metadata={
            "name": "EqvtAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchData:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccount3:
    id: AccountIdentification1Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )
    tp: None | CashAccountType3Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification1:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentificationChoice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress2:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    adr: None | LongPostalAddress1Choice = field(
        default=None,
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class Party1Choice:
    org_id: None | NonFinancialInstitutionIdentification1 = field(
        default=None,
        metadata={
            "name": "OrgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    prvt_id: list[PersonIdentification2] = field(
        default_factory=list,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "max_occurs": 2,
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification:
    fin_instn_id: FinancialInstitutionIdentification1 = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )
    brnch_id: None | BranchData = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification1:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    id: None | Party1Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification1Choice:
    bicor_bei: None | str = field(
        default=None,
        metadata={
            "name": "BICOrBEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification1 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    nm_and_adr: None | NameAndAddress2 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class Account1:
    id: None | AccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    acct_svcr: PartyIdentification1Choice = field(
        metadata={
            "name": "AcctSvcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class StructuredRemittanceInformation2:
    rfrd_doc_tp: None | DocumentType1Code = field(
        default=None,
        metadata={
            "name": "RfrdDocTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    rfrd_doc_rltd_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "RfrdDocRltdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    rfrd_doc_amt: list[ReferredDocumentAmount1Choice] = field(
        default_factory=list,
        metadata={
            "name": "RfrdDocAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    doc_ref_nb: None | str = field(
        default=None,
        metadata={
            "name": "DocRefNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cdtr_ref: None | str = field(
        default=None,
        metadata={
            "name": "CdtrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    invcr: None | PartyIdentification1 = field(
        default=None,
        metadata={
            "name": "Invcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    invcee: None | PartyIdentification1 = field(
        default=None,
        metadata={
            "name": "Invcee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class Intermediary1:
    id: PartyIdentification1Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )
    acct: None | Account1 = field(
        default=None,
        metadata={
            "name": "Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    role: None | str = field(
        default=None,
        metadata={
            "name": "Role",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class RemittanceInformation3Choice:
    ustrd: None | str = field(
        default=None,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    strd: None | StructuredRemittanceInformation2 = field(
        default=None,
        metadata={
            "name": "Strd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )


@dataclass(kw_only=True)
class PaymentComplementaryInformation:
    rmt_chc: None | RemittanceInformation3Choice = field(
        default=None,
        metadata={
            "name": "RmtChc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    dbtr: None | PartyIdentification1 = field(
        default=None,
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    dbtr_acct: None | CashAccount3 = field(
        default=None,
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    frst_agt: None | BranchAndFinancialInstitutionIdentification = field(
        default=None,
        metadata={
            "name": "FrstAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    amt: None | AmountType1Choice = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    nstr_vstr_acct: None | CashAccount3 = field(
        default=None,
        metadata={
            "name": "NstrVstrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    intrmy: None | Intermediary1 = field(
        default=None,
        metadata={
            "name": "Intrmy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    frst_sttlm_agt: None | BranchAndFinancialInstitutionIdentification = field(
        default=None,
        metadata={
            "name": "FrstSttlmAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    last_sttlm_agt: None | BranchAndFinancialInstitutionIdentification = field(
        default=None,
        metadata={
            "name": "LastSttlmAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    intrmy_sttlm_agt: None | BranchAndFinancialInstitutionIdentification = (
        field(
            default=None,
            metadata={
                "name": "IntrmySttlmAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            },
        )
    )
    cdtr: None | PartyIdentification1 = field(
        default=None,
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    cdtr_acct: None | CashAccount3 = field(
        default=None,
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
        },
    )
    sndr_to_rcvr_inf: list[str] = field(
        default_factory=list,
        metadata={
            "name": "SndrToRcvrInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "max_occurs": 6,
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class Camt02800101:
    class Meta:
        name = "camt.028.001.01"

    assgnmt: CaseAssignment = field(
        metadata={
            "name": "Assgnmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )
    case: Case = field(
        metadata={
            "name": "Case",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )
    undrlyg: PaymentInstructionExtract = field(
        metadata={
            "name": "Undrlyg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )
    inf: PaymentComplementaryInformation = field(
        metadata={
            "name": "Inf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:camt.028.001.01"

    camt_028_001_01: Camt02800101 = field(
        metadata={
            "name": "camt.028.001.01",
            "type": "Element",
            "required": True,
        }
    )
