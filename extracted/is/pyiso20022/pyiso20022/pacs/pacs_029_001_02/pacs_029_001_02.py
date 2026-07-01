from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02"


@dataclass(kw_only=True)
class AccountSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
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


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


@dataclass(kw_only=True)
class CashAccountType2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 3,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


class CreditDebitCode(Enum):
    CRDT = "CRDT"
    DBIT = "DBIT"


@dataclass(kw_only=True)
class DateAndPlaceOfBirth1:
    birth_dt: XmlDate = field(
        metadata={
            "name": "BirthDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
        }
    )
    prvc_of_birth: None | str = field(
        default=None,
        metadata={
            "name": "PrvcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    city_of_birth: str = field(
        metadata={
            "name": "CityOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_of_birth: str = field(
        metadata={
            "name": "CtryOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class GenericIdentification30:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


class NamePrefix2Code(Enum):
    DOCT = "DOCT"
    MADM = "MADM"
    MISS = "MISS"
    MIST = "MIST"
    MIKS = "MIKS"


@dataclass(kw_only=True)
class OrganisationIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class OtherContact1:
    chanl_tp: str = field(
        metadata={
            "name": "ChanlTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 4,
        }
    )
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 128,
        },
    )


@dataclass(kw_only=True)
class PersonIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


class PreferredContactMethod2Code(Enum):
    MAIL = "MAIL"
    FAXX = "FAXX"
    LETT = "LETT"
    CELL = "CELL"
    ONLI = "ONLI"
    PHON = "PHON"


class Priority3Code(Enum):
    URGT = "URGT"
    HIGH = "HIGH"
    NORM = "NORM"


@dataclass(kw_only=True)
class ProxyAccountType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


class SettlementMethod2Code(Enum):
    INDA = "INDA"
    INGA = "INGA"
    CLRG = "CLRG"


@dataclass(kw_only=True)
class SettlementTimeRequest2:
    clstm: None | XmlTime = field(
        default=None,
        metadata={
            "name": "CLSTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    till_tm: None | XmlTime = field(
        default=None,
        metadata={
            "name": "TillTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    fr_tm: None | XmlTime = field(
        default=None,
        metadata={
            "name": "FrTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    rjct_tm: None | XmlTime = field(
        default=None,
        metadata={
            "name": "RjctTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
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
class AddressType3Choice:
    cd: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class AmountAndDirection5:
    amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
        }
    )
    cdt_dbt: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class Contact13:
    nm_prfx: None | NamePrefix2Code = field(
        default=None,
        metadata={
            "name": "NmPrfx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    phne_nb: None | str = field(
        default=None,
        metadata={
            "name": "PhneNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    mob_nb: None | str = field(
        default=None,
        metadata={
            "name": "MobNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    fax_nb: None | str = field(
        default=None,
        metadata={
            "name": "FaxNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    urladr: None | str = field(
        default=None,
        metadata={
            "name": "URLAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 2048,
        },
    )
    email_adr: None | str = field(
        default=None,
        metadata={
            "name": "EmailAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 256,
        },
    )
    email_purp: None | str = field(
        default=None,
        metadata={
            "name": "EmailPurp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    job_titl: None | str = field(
        default=None,
        metadata={
            "name": "JobTitl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rspnsblty: None | str = field(
        default=None,
        metadata={
            "name": "Rspnsblty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dept: None | str = field(
        default=None,
        metadata={
            "name": "Dept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )
    othr: list[OtherContact1] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    prefrd_mtd: None | PreferredContactMethod2Code = field(
        default=None,
        metadata={
            "name": "PrefrdMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class GenericAccountIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericOrganisationIdentification3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 256,
        }
    )
    schme_nm: None | OrganisationIdentificationSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericPersonIdentification2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 256,
        }
    )
    schme_nm: None | PersonIdentificationSchemeName1Choice = field(
        default=None,
        metadata={
            "name": "SchmeNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class ProxyAccountIdentification1:
    tp: None | ProxyAccountType1Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 2048,
        }
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class AccountIdentification4Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "pattern": r"[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    othr: None | GenericAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class OrganisationIdentification39:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    othr: list[GenericOrganisationIdentification3] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class PersonIdentification18:
    dt_and_plc_of_birth: None | DateAndPlaceOfBirth1 = field(
        default=None,
        metadata={
            "name": "DtAndPlcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    othr: list[GenericPersonIdentification2] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class PostalAddress27:
    adr_tp: None | AddressType3Choice = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    care_of: None | str = field(
        default=None,
        metadata={
            "name": "CareOf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    dept: None | str = field(
        default=None,
        metadata={
            "name": "Dept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )
    sub_dept: None | str = field(
        default=None,
        metadata={
            "name": "SubDept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 16,
        },
    )
    bldg_nm: None | str = field(
        default=None,
        metadata={
            "name": "BldgNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    flr: None | str = field(
        default=None,
        metadata={
            "name": "Flr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )
    unit_nb: None | str = field(
        default=None,
        metadata={
            "name": "UnitNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_bx: None | str = field(
        default=None,
        metadata={
            "name": "PstBx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 16,
        },
    )
    room: None | str = field(
        default=None,
        metadata={
            "name": "Room",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    twn_lctn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnLctnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    dstrct_nm: None | str = field(
        default=None,
        metadata={
            "name": "DstrctNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "max_occurs": 7,
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class CashAccount40:
    id: None | AccountIdentification4Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    tp: None | CashAccountType2Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 70,
        },
    )
    prxy: None | ProxyAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Prxy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class Party52Choice:
    org_id: None | OrganisationIdentification39 = field(
        default=None,
        metadata={
            "name": "OrgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    prvt_id: None | PersonIdentification18 = field(
        default=None,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification272:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress27 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    id: None | Party52Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    ctry_of_res: None | str = field(
        default=None,
        metadata={
            "name": "CtryOfRes",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    ctct_dtls: None | Contact13 = field(
        default=None,
        metadata={
            "name": "CtctDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class SettlementInstruction14:
    sttlm_mtd: SettlementMethod2Code = field(
        metadata={
            "name": "SttlmMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
        }
    )
    sttlm_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "SttlmAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    clr_sys: None | ClearingSystemIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSys",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class GroupHeader104:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
        }
    )
    nb_of_sttlm_reqs: str = field(
        metadata={
            "name": "NbOfSttlmReqs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "pattern": r"[0-9]{1,15}",
        }
    )
    ctrl_sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "CtrlSum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    sttlm_inf: None | SettlementInstruction14 = field(
        default=None,
        metadata={
            "name": "SttlmInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class MovementRecord2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    seq_nb: None | Decimal = field(
        default=None,
        metadata={
            "name": "SeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    amt: AmountAndDirection5 = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
        }
    )
    sttlm_agt: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "SttlmAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    sttlm_agt_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "SttlmAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    ptcpt: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "Ptcpt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    ptcpt_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "PtcptAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    ref: None | str = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class MultilateralSettlementRequest3:
    instr_id: str = field(
        metadata={
            "name": "InstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    instr_prty: None | Priority3Code = field(
        default=None,
        metadata={
            "name": "InstrPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    sttlm_tm_req: None | SettlementTimeRequest2 = field(
        default=None,
        metadata={
            "name": "SttlmTmReq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    sttlm_prty: None | Priority3Code = field(
        default=None,
        metadata={
            "name": "SttlmPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )
    sttlm_cycl: None | str = field(
        default=None,
        metadata={
            "name": "SttlmCycl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nb_of_mvmnt_rcrds: None | Decimal = field(
        default=None,
        metadata={
            "name": "NbOfMvmntRcrds",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    mvmnt_rcrd: list[MovementRecord2] = field(
        default_factory=list,
        metadata={
            "name": "MvmntRcrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_occurs": 2,
        },
    )


@dataclass(kw_only=True)
class MultilateralSettlementRequestV02:
    grp_hdr: GroupHeader104 = field(
        metadata={
            "name": "GrpHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "required": True,
        }
    )
    sttlm_req: list[MultilateralSettlementRequest3] = field(
        default_factory=list,
        metadata={
            "name": "SttlmReq",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
            "min_occurs": 1,
        },
    )
    splmtry_data: None | SupplementaryData1 = field(
        default=None,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:pacs.029.001.02"

    mul_sttlm_req: MultilateralSettlementRequestV02 = field(
        metadata={
            "name": "MulSttlmReq",
            "type": "Element",
            "required": True,
        }
    )
