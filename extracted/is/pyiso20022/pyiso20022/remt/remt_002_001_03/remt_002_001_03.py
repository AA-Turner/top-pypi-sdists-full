from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03"


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


class Authorisation1Code(Enum):
    AUTH = "AUTH"
    FDET = "FDET"
    FSUM = "FSUM"
    ILEV = "ILEV"


@dataclass(kw_only=True)
class ClearingSystemIdentification2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 5,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )


class CopyDuplicate1Code(Enum):
    CODU = "CODU"
    COPY = "COPY"
    DUPL = "DUPL"


@dataclass(kw_only=True)
class DateAndPlaceOfBirth1:
    birth_dt: XmlDate = field(
        metadata={
            "name": "BirthDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
        }
    )
    prvc_of_birth: None | str = field(
        default=None,
        metadata={
            "name": "PrvcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    city_of_birth: str = field(
        metadata={
            "name": "CityOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_of_birth: str = field(
        metadata={
            "name": "CtryOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class FinancialIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification30:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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


class RemittanceLocationMethod2Code(Enum):
    FAXI = "FAXI"
    EDIC = "EDIC"
    URID = "URID"
    EMAL = "EMAL"
    POST = "POST"
    SMSM = "SMSM"


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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class Authorisation1Choice:
    cd: None | Authorisation1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 128,
        },
    )


@dataclass(kw_only=True)
class ClearingSystemMemberIdentification2:
    clr_sys_id: None | ClearingSystemIdentification2Choice = field(
        default=None,
        metadata={
            "name": "ClrSysId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    mmb_id: str = field(
        metadata={
            "name": "MmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class Contact13:
    nm_prfx: None | NamePrefix2Code = field(
        default=None,
        metadata={
            "name": "NmPrfx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    phne_nb: None | str = field(
        default=None,
        metadata={
            "name": "PhneNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    mob_nb: None | str = field(
        default=None,
        metadata={
            "name": "MobNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    fax_nb: None | str = field(
        default=None,
        metadata={
            "name": "FaxNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    urladr: None | str = field(
        default=None,
        metadata={
            "name": "URLAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 2048,
        },
    )
    email_adr: None | str = field(
        default=None,
        metadata={
            "name": "EmailAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 256,
        },
    )
    email_purp: None | str = field(
        default=None,
        metadata={
            "name": "EmailPurp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    job_titl: None | str = field(
        default=None,
        metadata={
            "name": "JobTitl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rspnsblty: None | str = field(
        default=None,
        metadata={
            "name": "Rspnsblty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dept: None | str = field(
        default=None,
        metadata={
            "name": "Dept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 70,
        },
    )
    othr: list[OtherContact1] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    prefrd_mtd: None | PreferredContactMethod2Code = field(
        default=None,
        metadata={
            "name": "PrefrdMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class GenericFinancialIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class OrganisationIdentification39:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    othr: list[GenericOrganisationIdentification3] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class PersonIdentification18:
    dt_and_plc_of_birth: None | DateAndPlaceOfBirth1 = field(
        default=None,
        metadata={
            "name": "DtAndPlcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    othr: list[GenericPersonIdentification2] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class PostalAddress27:
    adr_tp: None | AddressType3Choice = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    care_of: None | str = field(
        default=None,
        metadata={
            "name": "CareOf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    dept: None | str = field(
        default=None,
        metadata={
            "name": "Dept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 70,
        },
    )
    sub_dept: None | str = field(
        default=None,
        metadata={
            "name": "SubDept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 70,
        },
    )
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 16,
        },
    )
    bldg_nm: None | str = field(
        default=None,
        metadata={
            "name": "BldgNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    flr: None | str = field(
        default=None,
        metadata={
            "name": "Flr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 70,
        },
    )
    unit_nb: None | str = field(
        default=None,
        metadata={
            "name": "UnitNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_bx: None | str = field(
        default=None,
        metadata={
            "name": "PstBx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 16,
        },
    )
    room: None | str = field(
        default=None,
        metadata={
            "name": "Room",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    twn_lctn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnLctnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    dstrct_nm: None | str = field(
        default=None,
        metadata={
            "name": "DstrctNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "max_occurs": 7,
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class BranchData5:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress27 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification23:
    bicfi: None | str = field(
        default=None,
        metadata={
            "name": "BICFI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification2 = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress27 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    othr: None | GenericFinancialIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress18:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 140,
        }
    )
    adr: PostalAddress27 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Party52Choice:
    org_id: None | OrganisationIdentification39 = field(
        default=None,
        metadata={
            "name": "OrgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    prvt_id: None | PersonIdentification18 = field(
        default=None,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification8:
    fin_instn_id: FinancialInstitutionIdentification23 = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
        }
    )
    brnch_id: None | BranchData5 = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification272:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress27 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    id: None | Party52Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    ctry_of_res: None | str = field(
        default=None,
        metadata={
            "name": "CtryOfRes",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    ctct_dtls: None | Contact13 = field(
        default=None,
        metadata={
            "name": "CtctDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class RemittanceLocationData2:
    mtd: RemittanceLocationMethod2Code = field(
        metadata={
            "name": "Mtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
        }
    )
    elctrnc_adr: None | str = field(
        default=None,
        metadata={
            "name": "ElctrncAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 2048,
        },
    )
    pstl_adr: None | NameAndAddress18 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class GroupHeader122:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
        }
    )
    authstn: list[Authorisation1Choice] = field(
        default_factory=list,
        metadata={
            "name": "Authstn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "max_occurs": 2,
        },
    )
    cpy_ind: None | CopyDuplicate1Code = field(
        default=None,
        metadata={
            "name": "CpyInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    initg_pty: PartyIdentification272 = field(
        metadata={
            "name": "InitgPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
        }
    )
    msg_rcpt: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "MsgRcpt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )
    fwdg_agt: None | BranchAndFinancialInstitutionIdentification8 = field(
        default=None,
        metadata={
            "name": "FwdgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class TransactionReferences8:
    pmt_inf_id: None | str = field(
        default=None,
        metadata={
            "name": "PmtInfId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    instr_id: None | str = field(
        default=None,
        metadata={
            "name": "InstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    end_to_end_id: str = field(
        metadata={
            "name": "EndToEndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tx_id: None | str = field(
        default=None,
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    uetr: None | str = field(
        default=None,
        metadata={
            "name": "UETR",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "pattern": r"[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}",
        },
    )
    mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "MndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cdtr_schme_id: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "CdtrSchmeId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class RemittanceLocation10:
    rmt_id: None | str = field(
        default=None,
        metadata={
            "name": "RmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rmt_lctn_dtls: list[RemittanceLocationData2] = field(
        default_factory=list,
        metadata={
            "name": "RmtLctnDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_occurs": 1,
        },
    )
    refs: TransactionReferences8 = field(
        metadata={
            "name": "Refs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class RemittanceLocationAdviceV03:
    grp_hdr: GroupHeader122 = field(
        metadata={
            "name": "GrpHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "required": True,
        }
    )
    rmt_lctn: list[RemittanceLocation10] = field(
        default_factory=list,
        metadata={
            "name": "RmtLctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
            "min_occurs": 1,
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:remt.002.001.03"

    rmt_lctn_advc: RemittanceLocationAdviceV03 = field(
        metadata={
            "name": "RmtLctnAdvc",
            "type": "Element",
            "required": True,
        }
    )
