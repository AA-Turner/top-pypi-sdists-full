from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04"


@dataclass(kw_only=True)
class AccountSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
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
class ActiveOrHistoricCurrencyAnd13DecimalAmount:
    value: Decimal = field(
        metadata={
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 13,
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


class AgreementFramework1Code(Enum):
    FBAA = "FBAA"
    BBAA = "BBAA"
    DERV = "DERV"
    ISDA = "ISDA"
    NONR = "NONR"


class CollateralAccountType1Code(Enum):
    HOUS = "HOUS"
    CLIE = "CLIE"
    LIPR = "LIPR"
    MGIN = "MGIN"
    DFLT = "DFLT"


@dataclass(kw_only=True)
class DateAndDateTimeChoice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


class DateType2Code(Enum):
    OPEN = "OPEN"


class DepositType1Code(Enum):
    FITE = "FITE"
    CALL = "CALL"


class ExposureType5Code(Enum):
    BFWD = "BFWD"
    PAYM = "PAYM"
    CCPC = "CCPC"
    COMM = "COMM"
    CRDS = "CRDS"
    CRTL = "CRTL"
    CRSP = "CRSP"
    CCIR = "CCIR"
    CRPR = "CRPR"
    EQUI = "EQUI"
    EQPT = "EQPT"
    EQUS = "EQUS"
    EXTD = "EXTD"
    EXPT = "EXPT"
    FIXI = "FIXI"
    FORX = "FORX"
    FORW = "FORW"
    FUTR = "FUTR"
    OPTN = "OPTN"
    LIQU = "LIQU"
    OTCD = "OTCD"
    REPO = "REPO"
    RVPO = "RVPO"
    SLOA = "SLOA"
    SBSC = "SBSC"
    SCRP = "SCRP"
    SLEB = "SLEB"
    SHSL = "SHSL"
    SCIR = "SCIR"
    SCIE = "SCIE"
    SWPT = "SWPT"
    TBAS = "TBAS"
    TRBD = "TRBD"
    TRCP = "TRCP"


@dataclass(kw_only=True)
class FinancialInstrumentQuantity1Choice:
    unit: None | Decimal = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    face_amt: None | Decimal = field(
        default=None,
        metadata={
            "name": "FaceAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )
    amtsd_val: None | Decimal = field(
        default=None,
        metadata={
            "name": "AmtsdVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_inclusive": Decimal("0"),
            "total_digits": 18,
            "fraction_digits": 5,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification30:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class IdentificationSource3Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
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
class PartyTextInformation1:
    dclrtn_dtls: None | str = field(
        default=None,
        metadata={
            "name": "DclrtnDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 350,
        },
    )
    pty_ctct_dtls: None | str = field(
        default=None,
        metadata={
            "name": "PtyCtctDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 140,
        },
    )
    regn_dtls: None | str = field(
        default=None,
        metadata={
            "name": "RegnDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 350,
        },
    )


@dataclass(kw_only=True)
class PostalAddress2:
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd_id: str = field(
        metadata={
            "name": "PstCdId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 16,
        }
    )
    twn_nm: str = field(
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


class PriceValueType1Code(Enum):
    DISC = "DISC"
    PREM = "PREM"
    PARV = "PARV"


class ProposalType1Code(Enum):
    INIT = "INIT"
    COUN = "COUN"


class SafekeepingPlace1Code(Enum):
    CUST = "CUST"
    ICSD = "ICSD"
    NCSD = "NCSD"
    SHHE = "SHHE"


class SafekeepingPlace3Code(Enum):
    SHHE = "SHHE"


@dataclass(kw_only=True)
class SubAccount5:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    chrtc: None | str = field(
        default=None,
        metadata={
            "name": "Chrtc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
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


class TypeOfIdentification2Code(Enum):
    ARNU = "ARNU"
    CHTY = "CHTY"
    CORP = "CORP"
    FIIN = "FIIN"
    TXID = "TXID"


@dataclass(kw_only=True)
class AgreementFramework1Choice:
    agrmt_frmwk: None | AgreementFramework1Code = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    prtry_id: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralAccountIdentificationType2Choice:
    tp: None | CollateralAccountType1Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    prtry: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class ContactIdentification2:
    nm_prfx: None | NamePrefix1Code = field(
        default=None,
        metadata={
            "name": "NmPrfx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    gvn_nm: None | str = field(
        default=None,
        metadata={
            "name": "GvnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    phne_nb: None | str = field(
        default=None,
        metadata={
            "name": "PhneNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    mob_nb: None | str = field(
        default=None,
        metadata={
            "name": "MobNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    fax_nb: None | str = field(
        default=None,
        metadata={
            "name": "FaxNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    email_adr: None | str = field(
        default=None,
        metadata={
            "name": "EmailAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 256,
        },
    )


@dataclass(kw_only=True)
class DateCode9Choice:
    cd: None | DateType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class GenericAccountIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericIdentification78:
    tp: GenericIdentification30 = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class IdentificationType43Choice:
    cd: None | TypeOfIdentification2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    prtry: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress6:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    adr: PostalAddress2 = field(
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class OtherIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    sfx: None | str = field(
        default=None,
        metadata={
            "name": "Sfx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 16,
        },
    )
    tp: IdentificationSource3Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class OtherTypeOfCollateral2:
    desc: str = field(
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 140,
        }
    )
    qty: None | FinancialInstrumentQuantity1Choice = field(
        default=None,
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class PostalAddress1:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class PostalAddress8:
    adr_tp: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class PriceRateOrAmountChoice:
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    amt: None | ActiveOrHistoricCurrencyAnd13DecimalAmount = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class SafekeepingPlaceTypeAndAnyBicidentifier1:
    class Meta:
        name = "SafekeepingPlaceTypeAndAnyBICIdentifier1"

    sfkpg_plc_tp: SafekeepingPlace1Code = field(
        metadata={
            "name": "SfkpgPlcTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        }
    )


@dataclass(kw_only=True)
class SafekeepingPlaceTypeAndText8:
    sfkpg_plc_tp: SafekeepingPlace3Code = field(
        metadata={
            "name": "SfkpgPlcTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class SecuritiesAccount19:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tp: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class SupplementaryData1:
    plc_and_nm: None | str = field(
        default=None,
        metadata={
            "name": "PlcAndNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class YieldedOrValueType1Choice:
    yldd: None | bool = field(
        default=None,
        metadata={
            "name": "Yldd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    val_tp: None | PriceValueType1Code = field(
        default=None,
        metadata={
            "name": "ValTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class AccountIdentification4Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    othr: None | GenericAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class Agreement4:
    agrmt_dtls: str = field(
        metadata={
            "name": "AgrmtDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 140,
        }
    )
    agrmt_id: None | str = field(
        default=None,
        metadata={
            "name": "AgrmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 140,
        },
    )
    agrmt_dt: XmlDate = field(
        metadata={
            "name": "AgrmtDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    base_ccy: str = field(
        metadata={
            "name": "BaseCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    agrmt_frmwk: None | AgreementFramework1Choice = field(
        default=None,
        metadata={
            "name": "AgrmtFrmwk",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class AlternatePartyIdentification8:
    id_tp: IdentificationType43Choice = field(
        metadata={
            "name": "IdTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )
    altrn_id: str = field(
        metadata={
            "name": "AltrnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class CollateralAccount2:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    tp: None | CollateralAccountIdentificationType2Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class DateFormat14Choice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    dt_cd: None | DateCode9Choice = field(
        default=None,
        metadata={
            "name": "DtCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress13:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 350,
        }
    )
    adr: None | PostalAddress8 = field(
        default=None,
        metadata={
            "name": "Adr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class NameAndAddress5:
    nm: str = field(
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification100Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    nm_and_adr: None | NameAndAddress6 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class Price2:
    tp: YieldedOrValueType1Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    val: PriceRateOrAmountChoice = field(
        metadata={
            "name": "Val",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SafekeepingPlaceFormat10Choice:
    id: None | SafekeepingPlaceTypeAndText8 = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    tp_and_id: None | SafekeepingPlaceTypeAndAnyBicidentifier1 = field(
        default=None,
        metadata={
            "name": "TpAndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    prtry: None | GenericIdentification78 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class SecurityIdentification19:
    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"[A-Z]{2,2}[A-Z0-9]{9,9}[0-9]{1,1}",
        },
    )
    othr_id: list[OtherIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class CashCollateral2:
    coll_id: None | str = field(
        default=None,
        metadata={
            "name": "CollId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    csh_acct_id: None | AccountIdentification4Choice = field(
        default=None,
        metadata={
            "name": "CshAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    rtr_xcss: None | bool = field(
        default=None,
        metadata={
            "name": "RtrXcss",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    dpst_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DpstAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    dpst_tp: None | DepositType1Code = field(
        default=None,
        metadata={
            "name": "DpstTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    mtrty_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "MtrtyDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    val_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    xchg_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    coll_val: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "CollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    hrcut: None | Decimal = field(
        default=None,
        metadata={
            "name": "Hrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )


@dataclass(kw_only=True)
class CashCollateral3:
    coll_id: None | str = field(
        default=None,
        metadata={
            "name": "CollId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    csh_acct_id: None | AccountIdentification4Choice = field(
        default=None,
        metadata={
            "name": "CshAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    dpst_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "DpstAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    dpst_tp: None | DepositType1Code = field(
        default=None,
        metadata={
            "name": "DpstTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    mtrty_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "MtrtyDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    val_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    xchg_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    coll_val: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "CollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    hrcut: None | Decimal = field(
        default=None,
        metadata={
            "name": "Hrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )


@dataclass(kw_only=True)
class CollateralOwnership2:
    prtry: bool = field(
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    clnt_nm: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "ClntNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class Obligation4:
    pty_a: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    svcg_pty_a: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    pty_b: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    svcg_pty_b: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "SvcgPtyB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    coll_acct_id: None | CollateralAccount2 = field(
        default=None,
        metadata={
            "name": "CollAcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    xpsr_tp: None | ExposureType5Code = field(
        default=None,
        metadata={
            "name": "XpsrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    valtn_dt: DateAndDateTimeChoice = field(
        metadata={
            "name": "ValtnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class OtherCollateral5:
    coll_id: None | str = field(
        default=None,
        metadata={
            "name": "CollId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    lttr_of_cdt_id: None | str = field(
        default=None,
        metadata={
            "name": "LttrOfCdtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    lttr_of_cdt_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "LttrOfCdtAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    grnt_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "GrntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    othr_tp_of_coll: None | OtherTypeOfCollateral2 = field(
        default=None,
        metadata={
            "name": "OthrTpOfColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    isse_dt: None | DateFormat14Choice = field(
        default=None,
        metadata={
            "name": "IsseDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    xpry_dt: None | DateFormat14Choice = field(
        default=None,
        metadata={
            "name": "XpryDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    ltd_cvrg_ind: None | bool = field(
        default=None,
        metadata={
            "name": "LtdCvrgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    issr: None | PartyIdentification100Choice = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    val_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    xchg_rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    mkt_val: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "MktVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    hrcut: None | Decimal = field(
        default=None,
        metadata={
            "name": "Hrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    coll_val: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "CollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    sfkpg_plc: None | SafekeepingPlaceFormat10Choice = field(
        default=None,
        metadata={
            "name": "SfkpgPlc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    sfkpg_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification101Choice:
    bic: None | str = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    prtry_id: None | GenericIdentification36 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    nm_and_adr: None | NameAndAddress13 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification102Choice:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    nm_and_adr: None | NameAndAddress5 = field(
        default=None,
        metadata={
            "name": "NmAndAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "pattern": r"[A-Z]{2,2}",
        },
    )


@dataclass(kw_only=True)
class PartyIdentificationAndAccount126:
    pty_id: PartyIdentification100Choice = field(
        metadata={
            "name": "PtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    acct_id: None | str = field(
        default=None,
        metadata={
            "name": "AcctId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prcg_id: None | str = field(
        default=None,
        metadata={
            "name": "PrcgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prcg_dt: None | DateAndDateTimeChoice = field(
        default=None,
        metadata={
            "name": "PrcgDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    sub_acct: None | SubAccount5 = field(
        default=None,
        metadata={
            "name": "SubAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    ctct_prsn: None | ContactIdentification2 = field(
        default=None,
        metadata={
            "name": "CtctPrsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class PartyIdentificationAndAccount127:
    id: PartyIdentification101Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    altrn_id: None | AlternatePartyIdentification8 = field(
        default=None,
        metadata={
            "name": "AltrnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    sfkpg_acct: None | str = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prcg_id: None | str = field(
        default=None,
        metadata={
            "name": "PrcgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    addtl_inf: None | PartyTextInformation1 = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class DeliveringPartiesAndAccount15:
    dpstry: PartyIdentification102Choice = field(
        metadata={
            "name": "Dpstry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    pty1: PartyIdentificationAndAccount126 = field(
        metadata={
            "name": "Pty1",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    pty2: None | PartyIdentificationAndAccount127 = field(
        default=None,
        metadata={
            "name": "Pty2",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class ReceivingPartiesAndAccount15:
    dpstry: PartyIdentification102Choice = field(
        metadata={
            "name": "Dpstry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    pty1: PartyIdentificationAndAccount126 = field(
        metadata={
            "name": "Pty1",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    pty2: None | PartyIdentificationAndAccount127 = field(
        default=None,
        metadata={
            "name": "Pty2",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class SettlementParties5Choice:
    dlvrg_sttlm_pties: None | DeliveringPartiesAndAccount15 = field(
        default=None,
        metadata={
            "name": "DlvrgSttlmPties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    rcvg_sttlm_pties: None | ReceivingPartiesAndAccount15 = field(
        default=None,
        metadata={
            "name": "RcvgSttlmPties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class SettlementDetails102:
    trad_dt: XmlDateTime = field(
        metadata={
            "name": "TradDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    sttlm_pties: None | SettlementParties5Choice = field(
        default=None,
        metadata={
            "name": "SttlmPties",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    coll_ownrsh: CollateralOwnership2 = field(
        metadata={
            "name": "CollOwnrsh",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SecuritiesCollateral5:
    coll_id: None | str = field(
        default=None,
        metadata={
            "name": "CollId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    scty_id: SecurityIdentification19 = field(
        metadata={
            "name": "SctyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    mtrty_dt: None | DateAndDateTimeChoice = field(
        default=None,
        metadata={
            "name": "MtrtyDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    ltd_cvrg_ind: None | bool = field(
        default=None,
        metadata={
            "name": "LtdCvrgInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    qty: FinancialInstrumentQuantity1Choice = field(
        metadata={
            "name": "Qty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    pric: None | Price2 = field(
        default=None,
        metadata={
            "name": "Pric",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    mkt_val: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "MktVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    hrcut: None | Decimal = field(
        default=None,
        metadata={
            "name": "Hrcut",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    coll_val: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "CollVal",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    val_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ValDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    sfkpg_acct: None | SecuritiesAccount19 = field(
        default=None,
        metadata={
            "name": "SfkpgAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    sfkpg_plc: SafekeepingPlaceFormat10Choice = field(
        metadata={
            "name": "SfkpgPlc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    sttlm_params: None | SettlementDetails102 = field(
        default=None,
        metadata={
            "name": "SttlmParams",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class Collateral11:
    mrgn_call_req_id: str = field(
        metadata={
            "name": "MrgnCallReqId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    mrgn_call_rspn_id: None | str = field(
        default=None,
        metadata={
            "name": "MrgnCallRspnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    std_sttlm_instrs: None | str = field(
        default=None,
        metadata={
            "name": "StdSttlmInstrs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 140,
        },
    )
    coll_prpsl_rspn_id: None | str = field(
        default=None,
        metadata={
            "name": "CollPrpslRspnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    scties_coll: list[SecuritiesCollateral5] = field(
        default_factory=list,
        metadata={
            "name": "SctiesColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    csh_coll: list[CashCollateral2] = field(
        default_factory=list,
        metadata={
            "name": "CshColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    othr_coll: list[OtherCollateral5] = field(
        default_factory=list,
        metadata={
            "name": "OthrColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class Collateral12:
    mrgn_call_req_id: str = field(
        metadata={
            "name": "MrgnCallReqId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    mrgn_call_rspn_id: None | str = field(
        default=None,
        metadata={
            "name": "MrgnCallRspnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    std_sttlm_instrs: None | str = field(
        default=None,
        metadata={
            "name": "StdSttlmInstrs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 140,
        },
    )
    coll_prpsl_rspn_id: None | str = field(
        default=None,
        metadata={
            "name": "CollPrpslRspnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "min_length": 1,
            "max_length": 35,
        },
    )
    scties_coll: list[SecuritiesCollateral5] = field(
        default_factory=list,
        metadata={
            "name": "SctiesColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    csh_coll: list[CashCollateral3] = field(
        default_factory=list,
        metadata={
            "name": "CshColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    othr_coll: list[OtherCollateral5] = field(
        default_factory=list,
        metadata={
            "name": "OthrColl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralMovement8:
    dlvr: Collateral12 = field(
        metadata={
            "name": "Dlvr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    rtr: None | Collateral11 = field(
        default=None,
        metadata={
            "name": "Rtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralMovement4Choice:
    coll_mvmnt_drctn: None | CollateralMovement8 = field(
        default=None,
        metadata={
            "name": "CollMvmntDrctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    rtr: None | Collateral11 = field(
        default=None,
        metadata={
            "name": "Rtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralMovement7:
    agrd_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "AgrdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    mvmnt_drctn: list[CollateralMovement4Choice] = field(
        default_factory=list,
        metadata={
            "name": "MvmntDrctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralProposal5:
    vartn_mrgn: CollateralMovement7 = field(
        metadata={
            "name": "VartnMrgn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    sgrtd_indpdnt_amt: None | CollateralMovement7 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class CollateralProposal4Choice:
    coll_prpsl_dtls: None | CollateralProposal5 = field(
        default=None,
        metadata={
            "name": "CollPrpslDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    sgrtd_indpdnt_amt: None | CollateralMovement7 = field(
        default=None,
        metadata={
            "name": "SgrtdIndpdntAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class Proposal4:
    coll_prpsl_tp: ProposalType1Code = field(
        metadata={
            "name": "CollPrpslTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    coll_prpsl: CollateralProposal4Choice = field(
        metadata={
            "name": "CollPrpsl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CollateralProposalV04:
    tx_id: str = field(
        metadata={
            "name": "TxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    oblgtn: Obligation4 = field(
        metadata={
            "name": "Oblgtn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    agrmt: None | Agreement4 = field(
        default=None,
        metadata={
            "name": "Agrmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )
    tp_and_dtls: Proposal4 = field(
        metadata={
            "name": "TpAndDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
            "required": True,
        }
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:colr.007.001.04"

    coll_prpsl: CollateralProposalV04 = field(
        metadata={
            "name": "CollPrpsl",
            "type": "Element",
            "required": True,
        }
    )
