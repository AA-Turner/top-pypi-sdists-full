from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01"


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


class CashAccountType4Code(Enum):
    CASH = "CASH"
    CHAR = "CHAR"
    COMM = "COMM"
    TAXE = "TAXE"
    CISH = "CISH"
    TRAS = "TRAS"
    SACC = "SACC"
    CACC = "CACC"
    SVGS = "SVGS"
    ONDP = "ONDP"
    MGLD = "MGLD"
    NREX = "NREX"
    MOMA = "MOMA"
    LOAN = "LOAN"
    SLRY = "SLRY"
    ODFT = "ODFT"


class ChargeBearerType1Code(Enum):
    DEBT = "DEBT"
    CRED = "CRED"
    SHAR = "SHAR"
    SLEV = "SLEV"


class ClearingChannel2Code(Enum):
    RTGS = "RTGS"
    RTNS = "RTNS"
    MPNS = "MPNS"
    BOOK = "BOOK"


@dataclass(kw_only=True)
class ClearingSystemMemberIdentification3Choice:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
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


@dataclass(kw_only=True)
class DateAndPlaceOfBirth:
    birth_dt: XmlDate = field(
        metadata={
            "name": "BirthDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    prvc_of_birth: None | str = field(
        default=None,
        metadata={
            "name": "PrvcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    city_of_birth: str = field(
        metadata={
            "name": "CityOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_of_birth: str = field(
        metadata={
            "name": "CtryOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


class DocumentType2Code(Enum):
    MSIN = "MSIN"
    CNFA = "CNFA"
    DNFA = "DNFA"
    CINV = "CINV"
    CREN = "CREN"
    DEBN = "DEBN"
    HIRI = "HIRI"
    SBIN = "SBIN"
    CMCN = "CMCN"
    SOAC = "SOAC"
    DISP = "DISP"


class DocumentType3Code(Enum):
    RADM = "RADM"
    RPIN = "RPIN"
    FXDR = "FXDR"
    DISP = "DISP"
    PUOR = "PUOR"
    SCOR = "SCOR"


class Frequency1Code(Enum):
    YEAR = "YEAR"
    MNTH = "MNTH"
    QURT = "QURT"
    MIAN = "MIAN"
    WEEK = "WEEK"
    DAIL = "DAIL"
    ADHO = "ADHO"
    INDA = "INDA"


@dataclass(kw_only=True)
class GenericIdentification3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    id_tp: str = field(
        metadata={
            "name": "IdTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


class Grouping1Code(Enum):
    SNGL = "SNGL"
    GRPD = "GRPD"
    MIXD = "MIXD"


@dataclass(kw_only=True)
class LocalInstrument1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


class PaymentCategoryPurpose1Code(Enum):
    CORT = "CORT"
    SALA = "SALA"
    TREA = "TREA"
    CASH = "CASH"
    DIVI = "DIVI"
    GOVT = "GOVT"
    INTE = "INTE"
    LOAN = "LOAN"
    PENS = "PENS"
    SECU = "SECU"
    SSBE = "SSBE"
    SUPP = "SUPP"
    TAXS = "TAXS"
    TRAD = "TRAD"
    VATX = "VATX"
    HEDG = "HEDG"
    INTC = "INTC"
    WHLD = "WHLD"


@dataclass(kw_only=True)
class PaymentIdentification1:
    instr_id: None | str = field(
        default=None,
        metadata={
            "name": "InstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    end_to_end_id: str = field(
        metadata={
            "name": "EndToEndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


class PaymentMethod2Code(Enum):
    DD = "DD"


class Priority2Code(Enum):
    HIGH = "HIGH"
    NORM = "NORM"


@dataclass(kw_only=True)
class Purpose1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class RegulatoryAuthority:
    authrty_nm: None | str = field(
        default=None,
        metadata={
            "name": "AuthrtyNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    authrty_ctry: None | str = field(
        default=None,
        metadata={
            "name": "AuthrtyCtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[A-Z]{2,2}",
        },
    )


class RegulatoryReportingType1Code(Enum):
    CRED = "CRED"
    DEBT = "DEBT"
    BOTH = "BOTH"


class RemittanceLocationMethod1Code(Enum):
    FAXI = "FAXI"
    EDIC = "EDIC"
    URID = "URID"
    EMAL = "EMAL"
    POST = "POST"


class SequenceType1Code(Enum):
    FRST = "FRST"
    RCUR = "RCUR"
    FNAL = "FNAL"
    OOFF = "OOFF"


class ServiceLevel2Code(Enum):
    SEPA = "SEPA"
    SDVA = "SDVA"


@dataclass(kw_only=True)
class SimpleIdentificationInformation2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 34,
        }
    )


@dataclass(kw_only=True)
class AccountIdentification3Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[a-zA-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    bban: None | str = field(
        default=None,
        metadata={
            "name": "BBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[a-zA-Z0-9]{1,30}",
        },
    )
    upic: None | str = field(
        default=None,
        metadata={
            "name": "UPIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[0-9]{8,17}",
        },
    )
    prtry_acct: None | SimpleIdentificationInformation2 = field(
        default=None,
        metadata={
            "name": "PrtryAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccountType2:
    cd: None | CashAccountType4Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceType1:
    cd: None | DocumentType3Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class OrganisationIdentification2:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    ibei: None | str = field(
        default=None,
        metadata={
            "name": "IBEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[A-Z]{2,2}[B-DF-HJ-NP-TV-XZ0-9]{7,7}[0-9]{1,1}",
        },
    )
    bei: None | str = field(
        default=None,
        metadata={
            "name": "BEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    eangln: None | str = field(
        default=None,
        metadata={
            "name": "EANGLN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[0-9]{13,13}",
        },
    )
    uschu: None | str = field(
        default=None,
        metadata={
            "name": "USCHU",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"CH[0-9]{6,6}",
        },
    )
    duns: None | str = field(
        default=None,
        metadata={
            "name": "DUNS",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[0-9]{9,9}",
        },
    )
    bk_pty_id: None | str = field(
        default=None,
        metadata={
            "name": "BkPtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class PersonIdentification3:
    drvrs_lic_nb: None | str = field(
        default=None,
        metadata={
            "name": "DrvrsLicNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cstmr_nb: None | str = field(
        default=None,
        metadata={
            "name": "CstmrNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    scl_scty_nb: None | str = field(
        default=None,
        metadata={
            "name": "SclSctyNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    aln_regn_nb: None | str = field(
        default=None,
        metadata={
            "name": "AlnRegnNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pspt_nb: None | str = field(
        default=None,
        metadata={
            "name": "PsptNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    idnty_card_nb: None | str = field(
        default=None,
        metadata={
            "name": "IdntyCardNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    mplyr_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "MplyrIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dt_and_plc_of_birth: None | DateAndPlaceOfBirth = field(
        default=None,
        metadata={
            "name": "DtAndPlcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    othr_id: None | GenericIdentification4 = field(
        default=None,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    dscnt_apld_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DscntApldAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    rmtd_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RmtdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    cdt_note_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CdtNoteAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    tax_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentType1:
    cd: None | DocumentType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ServiceLevel3Choice:
    cd: None | ServiceLevel2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class StructuredRegulatoryReporting2:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 3,
        },
    )
    amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    inf: None | str = field(
        default=None,
        metadata={
            "name": "Inf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class TaxType:
    ctgy_desc: None | str = field(
        default=None,
        metadata={
            "name": "CtgyDesc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    taxbl_base_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TaxblBaseAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchData:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccount7:
    id: AccountIdentification3Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    tp: None | CashAccountType2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceInformation1:
    cdtr_ref_tp: None | CreditorReferenceType1 = field(
        default=None,
        metadata={
            "name": "CdtrRefTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    cdtr_ref: None | str = field(
        default=None,
        metadata={
            "name": "CdtrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification3:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress3:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    adr: PostalAddress1 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class NameAndAddress7:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    pstl_adr: PostalAddress1 = field(
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Party2Choice:
    org_id: None | OrganisationIdentification2 = field(
        default=None,
        metadata={
            "name": "OrgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    prvt_id: list[PersonIdentification3] = field(
        default_factory=list,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "max_occurs": 4,
        },
    )


@dataclass(kw_only=True)
class PaymentTypeInformation2:
    instr_prty: None | Priority2Code = field(
        default=None,
        metadata={
            "name": "InstrPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    svc_lvl: None | ServiceLevel3Choice = field(
        default=None,
        metadata={
            "name": "SvcLvl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    clr_chanl: None | ClearingChannel2Code = field(
        default=None,
        metadata={
            "name": "ClrChanl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    lcl_instrm: None | LocalInstrument1Choice = field(
        default=None,
        metadata={
            "name": "LclInstrm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    seq_tp: None | SequenceType1Code = field(
        default=None,
        metadata={
            "name": "SeqTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    ctgy_purp: None | PaymentCategoryPurpose1Code = field(
        default=None,
        metadata={
            "name": "CtgyPurp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentInformation1:
    rfrd_doc_tp: None | ReferredDocumentType1 = field(
        default=None,
        metadata={
            "name": "RfrdDocTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    rfrd_doc_nb: None | str = field(
        default=None,
        metadata={
            "name": "RfrdDocNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class RegulatoryReporting2:
    dbt_cdt_rptg_ind: None | RegulatoryReportingType1Code = field(
        default=None,
        metadata={
            "name": "DbtCdtRptgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    authrty: None | RegulatoryAuthority = field(
        default=None,
        metadata={
            "name": "Authrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    rgltry_dtls: None | StructuredRegulatoryReporting2 = field(
        default=None,
        metadata={
            "name": "RgltryDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class TaxDetails:
    cert_id: None | str = field(
        default=None,
        metadata={
            "name": "CertId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_tp: None | TaxType = field(
        default=None,
        metadata={
            "name": "TaxTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification5Choice:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    nm_and_adr: None | NameAndAddress7 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    cmbnd_id: None | FinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "CmbndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification8:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    id: None | Party2Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    ctry_of_res: None | str = field(
        default=None,
        metadata={
            "name": "CtryOfRes",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "pattern": r"[A-Z]{2,2}",
        },
    )


@dataclass(kw_only=True)
class RemittanceLocation1:
    rmt_id: None | str = field(
        default=None,
        metadata={
            "name": "RmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rmt_lctn_mtd: None | RemittanceLocationMethod1Code = field(
        default=None,
        metadata={
            "name": "RmtLctnMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    rmt_lctn_elctrnc_adr: None | str = field(
        default=None,
        metadata={
            "name": "RmtLctnElctrncAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 256,
        },
    )
    rmt_lctn_pstl_adr: None | NameAndAddress3 = field(
        default=None,
        metadata={
            "name": "RmtLctnPstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class TaxInformation2:
    cdtr_tax_id: None | str = field(
        default=None,
        metadata={
            "name": "CdtrTaxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cdtr_tax_tp: None | str = field(
        default=None,
        metadata={
            "name": "CdtrTaxTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dbtr_tax_id: None | str = field(
        default=None,
        metadata={
            "name": "DbtrTaxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_ref_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxRefNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    ttl_taxbl_base_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxblBaseAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    ttl_tax_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    tax_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "TaxDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    tax_tp_inf: list[TaxDetails] = field(
        default_factory=list,
        metadata={
            "name": "TaxTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification3:
    fin_instn_id: FinancialInstitutionIdentification5Choice = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    brnch_id: None | BranchData = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class StructuredRemittanceInformation6:
    rfrd_doc_inf: None | ReferredDocumentInformation1 = field(
        default=None,
        metadata={
            "name": "RfrdDocInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    rfrd_doc_rltd_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "RfrdDocRltdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    rfrd_doc_amt: list[ReferredDocumentAmount1Choice] = field(
        default_factory=list,
        metadata={
            "name": "RfrdDocAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    cdtr_ref_inf: None | CreditorReferenceInformation1 = field(
        default=None,
        metadata={
            "name": "CdtrRefInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    invcr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Invcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    invcee: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "Invcee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    addtl_rmt_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlRmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class AmendmentInformationDetails1:
    orgnl_mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlMndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_cdtr_schme_id: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "OrgnlCdtrSchmeId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    orgnl_cdtr_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "OrgnlCdtrAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            },
        )
    )
    orgnl_cdtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "OrgnlCdtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    orgnl_dbtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "OrgnlDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    orgnl_dbtr_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "OrgnlDbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    orgnl_dbtr_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "OrgnlDbtrAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            },
        )
    )
    orgnl_dbtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "OrgnlDbtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    orgnl_fnl_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "OrgnlFnlColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    orgnl_frqcy: None | Frequency1Code = field(
        default=None,
        metadata={
            "name": "OrgnlFrqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class GroupHeader1:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    authstn: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Authstn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "max_occurs": 2,
            "min_length": 1,
            "max_length": 128,
        },
    )
    btch_bookg: None | bool = field(
        default=None,
        metadata={
            "name": "BtchBookg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    nb_of_txs: str = field(
        metadata={
            "name": "NbOfTxs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
            "pattern": r"[0-9]{1,15}",
        }
    )
    ctrl_sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "CtrlSum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    grpg: Grouping1Code = field(
        metadata={
            "name": "Grpg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    initg_pty: PartyIdentification8 = field(
        metadata={
            "name": "InitgPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    fwdg_agt: None | BranchAndFinancialInstitutionIdentification3 = field(
        default=None,
        metadata={
            "name": "FwdgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class RemittanceInformation1:
    ustrd: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    strd: list[StructuredRemittanceInformation6] = field(
        default_factory=list,
        metadata={
            "name": "Strd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class MandateRelatedInformation1:
    mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "MndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dt_of_sgntr: None | XmlDate = field(
        default=None,
        metadata={
            "name": "DtOfSgntr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    amdmnt_ind: None | bool = field(
        default=None,
        metadata={
            "name": "AmdmntInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    amdmnt_inf_dtls: None | AmendmentInformationDetails1 = field(
        default=None,
        metadata={
            "name": "AmdmntInfDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    elctrnc_sgntr: None | str = field(
        default=None,
        metadata={
            "name": "ElctrncSgntr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 1025,
        },
    )
    frst_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "FrstColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    fnl_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "FnlColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    frqcy: None | Frequency1Code = field(
        default=None,
        metadata={
            "name": "Frqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class DirectDebitTransaction1:
    mndt_rltd_inf: None | MandateRelatedInformation1 = field(
        default=None,
        metadata={
            "name": "MndtRltdInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    cdtr_schme_id: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "CdtrSchmeId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    pre_ntfctn_id: None | str = field(
        default=None,
        metadata={
            "name": "PreNtfctnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pre_ntfctn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "PreNtfctnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class DirectDebitTransactionInformation1:
    pmt_id: PaymentIdentification1 = field(
        metadata={
            "name": "PmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    pmt_tp_inf: None | PaymentTypeInformation2 = field(
        default=None,
        metadata={
            "name": "PmtTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    instd_amt: CurrencyAndAmount = field(
        metadata={
            "name": "InstdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    chrg_br: None | ChargeBearerType1Code = field(
        default=None,
        metadata={
            "name": "ChrgBr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    drct_dbt_tx: None | DirectDebitTransaction1 = field(
        default=None,
        metadata={
            "name": "DrctDbtTx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    ultmt_cdtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "UltmtCdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    dbtr_agt: BranchAndFinancialInstitutionIdentification3 = field(
        metadata={
            "name": "DbtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    dbtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "DbtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    dbtr: PartyIdentification8 = field(
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    dbtr_acct: CashAccount7 = field(
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    ultmt_dbtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    instr_for_cdtr_agt: None | str = field(
        default=None,
        metadata={
            "name": "InstrForCdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 140,
        },
    )
    purp: None | Purpose1Choice = field(
        default=None,
        metadata={
            "name": "Purp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    rgltry_rptg: list[RegulatoryReporting2] = field(
        default_factory=list,
        metadata={
            "name": "RgltryRptg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "max_occurs": 10,
        },
    )
    tax: None | TaxInformation2 = field(
        default=None,
        metadata={
            "name": "Tax",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    rltd_rmt_inf: list[RemittanceLocation1] = field(
        default_factory=list,
        metadata={
            "name": "RltdRmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "max_occurs": 10,
        },
    )
    rmt_inf: None | RemittanceInformation1 = field(
        default=None,
        metadata={
            "name": "RmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )


@dataclass(kw_only=True)
class PaymentInstructionInformation2:
    pmt_inf_id: None | str = field(
        default=None,
        metadata={
            "name": "PmtInfId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pmt_mtd: PaymentMethod2Code = field(
        metadata={
            "name": "PmtMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    pmt_tp_inf: None | PaymentTypeInformation2 = field(
        default=None,
        metadata={
            "name": "PmtTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    reqd_colltn_dt: XmlDate = field(
        metadata={
            "name": "ReqdColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    cdtr: PartyIdentification8 = field(
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    cdtr_acct: CashAccount7 = field(
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    cdtr_agt: BranchAndFinancialInstitutionIdentification3 = field(
        metadata={
            "name": "CdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    cdtr_agt_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "CdtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    ultmt_cdtr: None | PartyIdentification8 = field(
        default=None,
        metadata={
            "name": "UltmtCdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    chrg_br: None | ChargeBearerType1Code = field(
        default=None,
        metadata={
            "name": "ChrgBr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    chrgs_acct: None | CashAccount7 = field(
        default=None,
        metadata={
            "name": "ChrgsAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
        },
    )
    chrgs_acct_agt: None | BranchAndFinancialInstitutionIdentification3 = (
        field(
            default=None,
            metadata={
                "name": "ChrgsAcctAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            },
        )
    )
    drct_dbt_tx_inf: list[DirectDebitTransactionInformation1] = field(
        default_factory=list,
        metadata={
            "name": "DrctDbtTxInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Pain00800101:
    class Meta:
        name = "pain.008.001.01"

    grp_hdr: GroupHeader1 = field(
        metadata={
            "name": "GrpHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "required": True,
        }
    )
    pmt_inf: list[PaymentInstructionInformation2] = field(
        default_factory=list,
        metadata={
            "name": "PmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:pain.008.001.01"

    pain_008_001_01: Pain00800101 = field(
        metadata={
            "name": "pain.008.001.01",
            "type": "Element",
            "required": True,
        }
    )
