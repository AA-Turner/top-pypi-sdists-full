from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02"


@dataclass(kw_only=True)
class AccountSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


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


@dataclass(kw_only=True)
class ActiveOrHistoricCurrencyAndAmount:
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


class ClearingChannel2Code(Enum):
    RTGS = "RTGS"
    RTNS = "RTNS"
    MPNS = "MPNS"
    BOOK = "BOOK"


@dataclass(kw_only=True)
class ClearingSystemIdentification2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 5,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ClearingSystemIdentification3Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 3,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


class CreditDebitCode(Enum):
    CRDT = "CRDT"
    DBIT = "DBIT"


@dataclass(kw_only=True)
class DateAndPlaceOfBirth:
    birth_dt: XmlDate = field(
        metadata={
            "name": "BirthDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    prvc_of_birth: None | str = field(
        default=None,
        metadata={
            "name": "PrvcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    city_of_birth: str = field(
        metadata={
            "name": "CityOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_of_birth: str = field(
        metadata={
            "name": "CtryOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


class DocumentType3Code(Enum):
    RADM = "RADM"
    RPIN = "RPIN"
    FXDR = "FXDR"
    DISP = "DISP"
    PUOR = "PUOR"
    SCOR = "SCOR"


class DocumentType5Code(Enum):
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
    BOLD = "BOLD"
    VCHR = "VCHR"
    AROI = "AROI"
    TSUT = "TSUT"


@dataclass(kw_only=True)
class FinancialIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


class Instruction4Code(Enum):
    PHOA = "PHOA"
    TELA = "TELA"


class Instruction5Code(Enum):
    PHOB = "PHOB"
    TELB = "TELB"


@dataclass(kw_only=True)
class LocalInstrument2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


class NamePrefix1Code(Enum):
    DOCT = "DOCT"
    MIST = "MIST"
    MISS = "MISS"
    MADM = "MADM"


@dataclass(kw_only=True)
class OrganisationIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PaymentIdentification3:
    instr_id: None | str = field(
        default=None,
        metadata={
            "name": "InstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    end_to_end_id: str = field(
        metadata={
            "name": "EndToEndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tx_id: str = field(
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    clr_sys_ref: None | str = field(
        default=None,
        metadata={
            "name": "ClrSysRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PersonIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


class Priority2Code(Enum):
    HIGH = "HIGH"
    NORM = "NORM"


class Priority3Code(Enum):
    URGT = "URGT"
    HIGH = "HIGH"
    NORM = "NORM"


@dataclass(kw_only=True)
class RemittanceInformation2:
    ustrd: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class ServiceLevel8Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class SettlementDateTimeIndication1:
    dbt_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DbtDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    cdt_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "CdtDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


class SettlementMethod1Code(Enum):
    INDA = "INDA"
    INGA = "INGA"
    COVE = "COVE"
    CLRG = "CLRG"


@dataclass(kw_only=True)
class SettlementTimeRequest2:
    clstm: None | XmlTime = field(
        default=None,
        metadata={
            "name": "CLSTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    till_tm: None | XmlTime = field(
        default=None,
        metadata={
            "name": "TillTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    fr_tm: None | XmlTime = field(
        default=None,
        metadata={
            "name": "FrTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    rjct_tm: None | XmlTime = field(
        default=None,
        metadata={
            "name": "RjctTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class CashAccountType2:
    cd: None | CashAccountType4Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ClearingSystemMemberIdentification2:
    clr_sys_id: None | ClearingSystemIdentification2Choice = field(
        default=None,
        metadata={
            "name": "ClrSysId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    mmb_id: str = field(
        metadata={
            "name": "MmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class ContactDetails2:
    nm_prfx: None | NamePrefix1Code = field(
        default=None,
        metadata={
            "name": "NmPrfx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    phne_nb: None | str = field(
        default=None,
        metadata={
            "name": "PhneNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    mob_nb: None | str = field(
        default=None,
        metadata={
            "name": "MobNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    fax_nb: None | str = field(
        default=None,
        metadata={
            "name": "FaxNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    email_adr: None | str = field(
        default=None,
        metadata={
            "name": "EmailAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 2048,
        },
    )
    othr: None | str = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceType1Choice:
    cd: None | DocumentType3Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DocumentAdjustment1:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    rsn: None | str = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class GenericAccountIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 34,
        }
    )
    schme_nm: None | AccountSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericFinancialIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | FinancialIdentificationSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericOrganisationIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | OrganisationIdentificationSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericPersonIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    schme_nm: None | PersonIdentificationSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class InstructionForCreditorAgent2:
    cd: None | Instruction5Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instr_inf: None | str = field(
        default=None,
        metadata={
            "name": "InstrInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class InstructionForNextAgent1:
    cd: None | Instruction4Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instr_inf: None | str = field(
        default=None,
        metadata={
            "name": "InstrInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class PaymentTypeInformation23:
    instr_prty: None | Priority2Code = field(
        default=None,
        metadata={
            "name": "InstrPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    clr_chanl: None | ClearingChannel2Code = field(
        default=None,
        metadata={
            "name": "ClrChanl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    svc_lvl: None | ServiceLevel8Choice = field(
        default=None,
        metadata={
            "name": "SvcLvl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    lcl_instrm: None | LocalInstrument2Choice = field(
        default=None,
        metadata={
            "name": "LclInstrm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class PostalAddress6:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    dept: None | str = field(
        default=None,
        metadata={
            "name": "Dept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )
    sub_dept: None | str = field(
        default=None,
        metadata={
            "name": "SubDept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "max_occurs": 7,
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentType1Choice:
    cd: None | DocumentType5Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class AccountIdentification4Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "pattern": r"[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    othr: None | GenericAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class BranchData2:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress6 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceType2:
    cd_or_prtry: CreditorReferenceType1Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification7:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification2 = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress6 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    othr: None | GenericFinancialIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class OrganisationIdentification4:
    bicor_bei: None | str = field(
        default=None,
        metadata={
            "name": "BICOrBEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    othr: list[GenericOrganisationIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class PersonIdentification5:
    dt_and_plc_of_birth: None | DateAndPlaceOfBirth = field(
        default=None,
        metadata={
            "name": "DtAndPlcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    othr: list[GenericPersonIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentType2:
    cd_or_prtry: ReferredDocumentType1Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class RemittanceAmount1:
    due_pybl_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DuePyblAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    dscnt_apld_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DscntApldAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    cdt_note_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CdtNoteAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    tax_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    adjstmnt_amt_and_rsn: list[DocumentAdjustment1] = field(
        default_factory=list,
        metadata={
            "name": "AdjstmntAmtAndRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    rmtd_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RmtdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification4:
    fin_instn_id: FinancialInstitutionIdentification7 = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    brnch_id: None | BranchData2 = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class CashAccount16:
    id: AccountIdentification4Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    tp: None | CashAccountType2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceInformation2:
    tp: None | CreditorReferenceType2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    ref: None | str = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class Party6Choice:
    org_id: None | OrganisationIdentification4 = field(
        default=None,
        metadata={
            "name": "OrgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    prvt_id: None | PersonIdentification5 = field(
        default=None,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentInformation3:
    tp: None | ReferredDocumentType2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    nb: None | str = field(
        default=None,
        metadata={
            "name": "Nb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rltd_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "RltdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification32:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress6 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    id: None | Party6Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    ctry_of_res: None | str = field(
        default=None,
        metadata={
            "name": "CtryOfRes",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    ctct_dtls: None | ContactDetails2 = field(
        default=None,
        metadata={
            "name": "CtctDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class SettlementInformation13:
    sttlm_mtd: SettlementMethod1Code = field(
        metadata={
            "name": "SttlmMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    sttlm_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "SttlmAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    clr_sys: None | ClearingSystemIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSys",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instg_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification4 = (
        field(
            default=None,
            metadata={
                "name": "InstgRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            },
        )
    )
    instg_rmbrsmnt_agt_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "InstgRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification4 = (
        field(
            default=None,
            metadata={
                "name": "InstdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            },
        )
    )
    instd_rmbrsmnt_agt_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "InstdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    thrd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification4 = (
        field(
            default=None,
            metadata={
                "name": "ThrdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            },
        )
    )
    thrd_rmbrsmnt_agt_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "ThrdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class GroupHeader35:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    btch_bookg: None | bool = field(
        default=None,
        metadata={
            "name": "BtchBookg",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    nb_of_txs: str = field(
        metadata={
            "name": "NbOfTxs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
            "pattern": r"[0-9]{1,15}",
        }
    )
    ctrl_sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "CtrlSum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    ttl_intr_bk_sttlm_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlIntrBkSttlmAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    sttlm_inf: SettlementInformation13 = field(
        metadata={
            "name": "SttlmInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    pmt_tp_inf: None | PaymentTypeInformation23 = field(
        default=None,
        metadata={
            "name": "PmtTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instg_agt: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "InstgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instd_agt: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "InstdAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class StructuredRemittanceInformation7:
    rfrd_doc_inf: list[ReferredDocumentInformation3] = field(
        default_factory=list,
        metadata={
            "name": "RfrdDocInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    rfrd_doc_amt: None | RemittanceAmount1 = field(
        default=None,
        metadata={
            "name": "RfrdDocAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    cdtr_ref_inf: None | CreditorReferenceInformation2 = field(
        default=None,
        metadata={
            "name": "CdtrRefInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    invcr: None | PartyIdentification32 = field(
        default=None,
        metadata={
            "name": "Invcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    invcee: None | PartyIdentification32 = field(
        default=None,
        metadata={
            "name": "Invcee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    addtl_rmt_inf: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AddtlRmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "max_occurs": 3,
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class RemittanceInformation5:
    ustrd: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    strd: list[StructuredRemittanceInformation7] = field(
        default_factory=list,
        metadata={
            "name": "Strd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class CreditTransferTransactionInformation12:
    ultmt_dbtr: None | PartyIdentification32 = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    initg_pty: None | PartyIdentification32 = field(
        default=None,
        metadata={
            "name": "InitgPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    dbtr: PartyIdentification32 = field(
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    dbtr_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    dbtr_agt: BranchAndFinancialInstitutionIdentification4 = field(
        metadata={
            "name": "DbtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    dbtr_agt_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "DbtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    prvs_instg_agt: None | BranchAndFinancialInstitutionIdentification4 = (
        field(
            default=None,
            metadata={
                "name": "PrvsInstgAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            },
        )
    )
    prvs_instg_agt_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "PrvsInstgAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt1: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt1",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt1_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt1Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt2: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt2",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt2_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt2Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt3: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt3",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt3_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt3Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    cdtr_agt: BranchAndFinancialInstitutionIdentification4 = field(
        metadata={
            "name": "CdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    cdtr_agt_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "CdtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    cdtr: PartyIdentification32 = field(
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    cdtr_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    ultmt_cdtr: None | PartyIdentification32 = field(
        default=None,
        metadata={
            "name": "UltmtCdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    rmt_inf: None | RemittanceInformation5 = field(
        default=None,
        metadata={
            "name": "RmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instd_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "InstdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )


@dataclass(kw_only=True)
class CreditTransferTransactionInformation13:
    pmt_id: PaymentIdentification3 = field(
        metadata={
            "name": "PmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    pmt_tp_inf: None | PaymentTypeInformation23 = field(
        default=None,
        metadata={
            "name": "PmtTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intr_bk_sttlm_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "IntrBkSttlmAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    sttlm_prty: None | Priority3Code = field(
        default=None,
        metadata={
            "name": "SttlmPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    sttlm_tm_indctn: None | SettlementDateTimeIndication1 = field(
        default=None,
        metadata={
            "name": "SttlmTmIndctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    sttlm_tm_req: None | SettlementTimeRequest2 = field(
        default=None,
        metadata={
            "name": "SttlmTmReq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    prvs_instg_agt: None | BranchAndFinancialInstitutionIdentification4 = (
        field(
            default=None,
            metadata={
                "name": "PrvsInstgAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            },
        )
    )
    prvs_instg_agt_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "PrvsInstgAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instg_agt: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "InstgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instd_agt: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "InstdAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt1: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt1",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt1_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt1Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt2: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt2",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt2_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt2Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt3: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt3",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    intrmy_agt3_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "IntrmyAgt3Acct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    ultmt_dbtr: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    dbtr: BranchAndFinancialInstitutionIdentification4 = field(
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    dbtr_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    dbtr_agt: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "DbtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    dbtr_agt_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "DbtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    cdtr_agt: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "CdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    cdtr_agt_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "CdtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    cdtr: BranchAndFinancialInstitutionIdentification4 = field(
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    cdtr_acct: None | CashAccount16 = field(
        default=None,
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    ultmt_cdtr: None | BranchAndFinancialInstitutionIdentification4 = field(
        default=None,
        metadata={
            "name": "UltmtCdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instr_for_cdtr_agt: list[InstructionForCreditorAgent2] = field(
        default_factory=list,
        metadata={
            "name": "InstrForCdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    instr_for_nxt_agt: list[InstructionForNextAgent1] = field(
        default_factory=list,
        metadata={
            "name": "InstrForNxtAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    rmt_inf: None | RemittanceInformation2 = field(
        default=None,
        metadata={
            "name": "RmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
        },
    )
    undrlyg_cstmr_cdt_trf: None | CreditTransferTransactionInformation12 = (
        field(
            default=None,
            metadata={
                "name": "UndrlygCstmrCdtTrf",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            },
        )
    )


@dataclass(kw_only=True)
class FinancialInstitutionCreditTransferV02:
    grp_hdr: GroupHeader35 = field(
        metadata={
            "name": "GrpHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "required": True,
        }
    )
    cdt_trf_tx_inf: list[CreditTransferTransactionInformation13] = field(
        default_factory=list,
        metadata={
            "name": "CdtTrfTxInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:pacs.009.001.02"

    fin_instn_cdt_trf: FinancialInstitutionCreditTransferV02 = field(
        metadata={
            "name": "FinInstnCdtTrf",
            "type": "Element",
            "required": True,
        }
    )
