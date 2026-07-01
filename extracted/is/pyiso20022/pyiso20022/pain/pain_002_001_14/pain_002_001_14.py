from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlPeriod

__NAMESPACE__ = "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14"


@dataclass(kw_only=True)
class AccountSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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


@dataclass(kw_only=True)
class CashAccountType2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CategoryPurpose1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


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
class ClearingSystemIdentification2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 5,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 3,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


class CreditDebitCode(Enum):
    CRDT = "CRDT"
    DBIT = "DBIT"


@dataclass(kw_only=True)
class CreditorReferenceType2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class CurrencyExchange13:
    src_ccy: str = field(
        metadata={
            "name": "SrcCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    trgt_ccy: str = field(
        metadata={
            "name": "TrgtCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )
    xchg_rate: Decimal = field(
        metadata={
            "name": "XchgRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "total_digits": 11,
            "fraction_digits": 10,
        }
    )
    unit_ccy: None | str = field(
        default=None,
        metadata={
            "name": "UnitCcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z]{3,3}",
        },
    )


@dataclass(kw_only=True)
class DateAndDateTime2Choice:
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class DateAndPlaceOfBirth1:
    birth_dt: XmlDate = field(
        metadata={
            "name": "BirthDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    prvc_of_birth: None | str = field(
        default=None,
        metadata={
            "name": "PrvcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    city_of_birth: str = field(
        metadata={
            "name": "CityOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    ctry_of_birth: str = field(
        metadata={
            "name": "CtryOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class DatePeriod2:
    fr_dt: XmlDate = field(
        metadata={
            "name": "FrDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    to_dt: XmlDate = field(
        metadata={
            "name": "ToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DateType2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DocumentAmountType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DocumentLineType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DocumentType2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class FinancialIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


class Frequency6Code(Enum):
    YEAR = "YEAR"
    MNTH = "MNTH"
    QURT = "QURT"
    MIAN = "MIAN"
    WEEK = "WEEK"
    DAIL = "DAIL"
    ADHO = "ADHO"
    INDA = "INDA"
    FRTN = "FRTN"


@dataclass(kw_only=True)
class GarnishmentType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "pattern": r"[a-zA-Z0-9]{4}",
        }
    )
    issr: str = field(
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class LocalInstrument2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


class MandateClassification1Code(Enum):
    FIXE = "FIXE"
    USGB = "USGB"
    VARI = "VARI"


@dataclass(kw_only=True)
class MandateSetupReason1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 70,
        },
    )


class NamePrefix2Code(Enum):
    DOCT = "DOCT"
    MADM = "MADM"
    MISS = "MISS"
    MIST = "MIST"
    MIKS = "MIKS"


@dataclass(kw_only=True)
class NumberOfTransactionsPerStatus5:
    dtld_nb_of_txs: str = field(
        metadata={
            "name": "DtldNbOfTxs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "pattern": r"[0-9]{1,15}",
        }
    )
    dtld_sts: str = field(
        metadata={
            "name": "DtldSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "min_length": 1,
            "max_length": 4,
        }
    )
    dtld_ctrl_sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "DtldCtrlSum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )


@dataclass(kw_only=True)
class OrganisationIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 128,
        },
    )


class PaymentMethod4Code(Enum):
    CHK = "CHK"
    TRF = "TRF"
    DD = "DD"
    TRA = "TRA"


@dataclass(kw_only=True)
class PersonIdentificationSchemeName1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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


class Priority2Code(Enum):
    HIGH = "HIGH"
    NORM = "NORM"


@dataclass(kw_only=True)
class ProxyAccountType1Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class Purpose2Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


class SequenceType3Code(Enum):
    FRST = "FRST"
    RCUR = "RCUR"
    FNAL = "FNAL"
    OOFF = "OOFF"
    RPRE = "RPRE"


@dataclass(kw_only=True)
class ServiceLevel8Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


class SettlementMethod1Code(Enum):
    INDA = "INDA"
    INGA = "INGA"
    COVE = "COVE"
    CLRG = "CLRG"


@dataclass(kw_only=True)
class StatusReason6Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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


@dataclass(kw_only=True)
class TaxAuthorisation1:
    titl: None | str = field(
        default=None,
        metadata={
            "name": "Titl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class TaxParty1:
    tax_id: None | str = field(
        default=None,
        metadata={
            "name": "TaxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    regn_id: None | str = field(
        default=None,
        metadata={
            "name": "RegnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_tp: None | str = field(
        default=None,
        metadata={
            "name": "TaxTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


class TaxRecordPeriod1Code(Enum):
    MM01 = "MM01"
    MM02 = "MM02"
    MM03 = "MM03"
    MM04 = "MM04"
    MM05 = "MM05"
    MM06 = "MM06"
    MM07 = "MM07"
    MM08 = "MM08"
    MM09 = "MM09"
    MM10 = "MM10"
    MM11 = "MM11"
    MM12 = "MM12"
    QTR1 = "QTR1"
    QTR2 = "QTR2"
    QTR3 = "QTR3"
    QTR4 = "QTR4"
    HLF1 = "HLF1"
    HLF2 = "HLF2"


@dataclass(kw_only=True)
class AddressType3Choice:
    cd: None | AddressType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    prtry: None | GenericIdentification30 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class ChargeType3Choice:
    cd: None | str = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    prtry: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class ClearingSystemMemberIdentification2:
    clr_sys_id: None | ClearingSystemIdentification2Choice = field(
        default=None,
        metadata={
            "name": "ClrSysId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    mmb_id: str = field(
        metadata={
            "name": "MmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    phne_nb: None | str = field(
        default=None,
        metadata={
            "name": "PhneNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    mob_nb: None | str = field(
        default=None,
        metadata={
            "name": "MobNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    fax_nb: None | str = field(
        default=None,
        metadata={
            "name": "FaxNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"\+[0-9]{1,3}-[0-9()+\-]{1,30}",
        },
    )
    urladr: None | str = field(
        default=None,
        metadata={
            "name": "URLAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 2048,
        },
    )
    email_adr: None | str = field(
        default=None,
        metadata={
            "name": "EmailAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 256,
        },
    )
    email_purp: None | str = field(
        default=None,
        metadata={
            "name": "EmailPurp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    job_titl: None | str = field(
        default=None,
        metadata={
            "name": "JobTitl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rspnsblty: None | str = field(
        default=None,
        metadata={
            "name": "Rspnsblty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dept: None | str = field(
        default=None,
        metadata={
            "name": "Dept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 70,
        },
    )
    othr: list[OtherContact1] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    prefrd_mtd: None | PreferredContactMethod2Code = field(
        default=None,
        metadata={
            "name": "PrefrdMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceType3:
    cd_or_prtry: CreditorReferenceType2Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DateAndType1:
    tp: DateType2Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    dt: XmlDate = field(
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DocumentAdjustment1:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    cdt_dbt_ind: None | CreditDebitCode = field(
        default=None,
        metadata={
            "name": "CdtDbtInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    rsn: None | str = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class DocumentAmount1:
    tp: DocumentAmountType1Choice = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DocumentLineType1:
    cd_or_prtry: DocumentLineType1Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DocumentType1:
    cd_or_prtry: DocumentType2Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class EquivalentAmount2:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    ccy_of_trf: str = field(
        metadata={
            "name": "CcyOfTrf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )


@dataclass(kw_only=True)
class FrequencyAndMoment1:
    tp: Frequency6Code = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    pt_in_tm: str = field(
        metadata={
            "name": "PtInTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "pattern": r"[0-9]{2}",
        }
    )


@dataclass(kw_only=True)
class FrequencyPeriod1:
    tp: Frequency6Code = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    cnt_per_prd: Decimal = field(
        metadata={
            "name": "CntPerPrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "total_digits": 18,
            "fraction_digits": 17,
        }
    )


@dataclass(kw_only=True)
class GarnishmentType1:
    cd_or_prtry: GarnishmentType1Choice = field(
        metadata={
            "name": "CdOrPrtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class GenericAccountIdentification1:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class MandateClassification1Choice:
    cd: None | MandateClassification1Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    prtry: None | str = field(
        default=None,
        metadata={
            "name": "Prtry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PaymentTypeInformation27:
    instr_prty: None | Priority2Code = field(
        default=None,
        metadata={
            "name": "InstrPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    clr_chanl: None | ClearingChannel2Code = field(
        default=None,
        metadata={
            "name": "ClrChanl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    svc_lvl: list[ServiceLevel8Choice] = field(
        default_factory=list,
        metadata={
            "name": "SvcLvl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    lcl_instrm: None | LocalInstrument2Choice = field(
        default=None,
        metadata={
            "name": "LclInstrm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    seq_tp: None | SequenceType3Code = field(
        default=None,
        metadata={
            "name": "SeqTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ctgy_purp: None | CategoryPurpose1Choice = field(
        default=None,
        metadata={
            "name": "CtgyPurp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class ProxyAccountIdentification1:
    tp: None | ProxyAccountType1Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
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
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 350,
        },
    )
    envlp: SupplementaryDataEnvelope1 = field(
        metadata={
            "name": "Envlp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class TaxParty2:
    tax_id: None | str = field(
        default=None,
        metadata={
            "name": "TaxId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    regn_id: None | str = field(
        default=None,
        metadata={
            "name": "RegnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_tp: None | str = field(
        default=None,
        metadata={
            "name": "TaxTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    authstn: None | TaxAuthorisation1 = field(
        default=None,
        metadata={
            "name": "Authstn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class TaxPeriod3:
    yr: None | XmlPeriod = field(
        default=None,
        metadata={
            "name": "Yr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    tp: None | TaxRecordPeriod1Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    fr_to_dt: None | DatePeriod2 = field(
        default=None,
        metadata={
            "name": "FrToDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class AccountIdentification4Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    othr: None | GenericAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class AmountType4Choice:
    instd_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "InstdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    eqvt_amt: None | EquivalentAmount2 = field(
        default=None,
        metadata={
            "name": "EqvtAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class CreditorReferenceInformation3:
    tp: None | CreditorReferenceType3 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ref: None | str = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class DocumentLineIdentification1:
    tp: None | DocumentLineType1 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    nb: None | str = field(
        default=None,
        metadata={
            "name": "Nb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rltd_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "RltdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class Frequency36Choice:
    tp: None | Frequency6Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    prd: None | FrequencyPeriod1 = field(
        default=None,
        metadata={
            "name": "Prd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    pt_in_tm: None | FrequencyAndMoment1 = field(
        default=None,
        metadata={
            "name": "PtInTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class MandateTypeInformation2:
    svc_lvl: None | ServiceLevel8Choice = field(
        default=None,
        metadata={
            "name": "SvcLvl",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    lcl_instrm: None | LocalInstrument2Choice = field(
        default=None,
        metadata={
            "name": "LclInstrm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ctgy_purp: None | CategoryPurpose1Choice = field(
        default=None,
        metadata={
            "name": "CtgyPurp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    clssfctn: None | MandateClassification1Choice = field(
        default=None,
        metadata={
            "name": "Clssfctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class OrganisationIdentification39:
    any_bic: None | str = field(
        default=None,
        metadata={
            "name": "AnyBIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    othr: list[GenericOrganisationIdentification3] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class PersonIdentification18:
    dt_and_plc_of_birth: None | DateAndPlaceOfBirth1 = field(
        default=None,
        metadata={
            "name": "DtAndPlcOfBirth",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    othr: list[GenericPersonIdentification2] = field(
        default_factory=list,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class PostalAddress27:
    adr_tp: None | AddressType3Choice = field(
        default=None,
        metadata={
            "name": "AdrTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    care_of: None | str = field(
        default=None,
        metadata={
            "name": "CareOf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    dept: None | str = field(
        default=None,
        metadata={
            "name": "Dept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 70,
        },
    )
    sub_dept: None | str = field(
        default=None,
        metadata={
            "name": "SubDept",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 70,
        },
    )
    strt_nm: None | str = field(
        default=None,
        metadata={
            "name": "StrtNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 16,
        },
    )
    bldg_nm: None | str = field(
        default=None,
        metadata={
            "name": "BldgNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    flr: None | str = field(
        default=None,
        metadata={
            "name": "Flr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 70,
        },
    )
    unit_nb: None | str = field(
        default=None,
        metadata={
            "name": "UnitNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_bx: None | str = field(
        default=None,
        metadata={
            "name": "PstBx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 16,
        },
    )
    room: None | str = field(
        default=None,
        metadata={
            "name": "Room",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    twn_lctn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnLctnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    dstrct_nm: None | str = field(
        default=None,
        metadata={
            "name": "DstrctNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: None | str = field(
        default=None,
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "max_occurs": 7,
            "min_length": 1,
            "max_length": 70,
        },
    )


@dataclass(kw_only=True)
class RemittanceAmount4:
    rmt_amt_and_tp: list[DocumentAmount1] = field(
        default_factory=list,
        metadata={
            "name": "RmtAmtAndTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    adjstmnt_amt_and_rsn: list[DocumentAdjustment1] = field(
        default_factory=list,
        metadata={
            "name": "AdjstmntAmtAndRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class TaxRecordDetails3:
    prd: None | TaxPeriod3 = field(
        default=None,
        metadata={
            "name": "Prd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class BranchData5:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress27 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class CashAccount40:
    id: None | AccountIdentification4Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    tp: None | CashAccountType2Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 70,
        },
    )
    prxy: None | ProxyAccountIdentification1 = field(
        default=None,
        metadata={
            "name": "Prxy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class CreditTransferMandateData1:
    mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "MndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tp: None | MandateTypeInformation2 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dt_of_sgntr: None | XmlDate = field(
        default=None,
        metadata={
            "name": "DtOfSgntr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dt_of_vrfctn: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "DtOfVrfctn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    elctrnc_sgntr: None | bytes = field(
        default=None,
        metadata={
            "name": "ElctrncSgntr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 10240,
            "format": "base64",
        },
    )
    frst_pmt_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "FrstPmtDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    fnl_pmt_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "FnlPmtDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    frqcy: None | Frequency36Choice = field(
        default=None,
        metadata={
            "name": "Frqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    rsn: None | MandateSetupReason1Choice = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class DocumentLineInformation2:
    id: list[DocumentLineIdentification1] = field(
        default_factory=list,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_occurs": 1,
        },
    )
    desc: None | str = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 2048,
        },
    )
    amt: None | RemittanceAmount4 = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class FinancialInstitutionIdentification23:
    bicfi: None | str = field(
        default=None,
        metadata={
            "name": "BICFI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentification2 = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    lei: None | str = field(
        default=None,
        metadata={
            "name": "LEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z0-9]{18,18}[0-9]{2,2}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress27 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    othr: None | GenericFinancialIdentification1 = field(
        default=None,
        metadata={
            "name": "Othr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class Party52Choice:
    org_id: None | OrganisationIdentification39 = field(
        default=None,
        metadata={
            "name": "OrgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    prvt_id: None | PersonIdentification18 = field(
        default=None,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class TaxAmount3:
    rate: None | Decimal = field(
        default=None,
        metadata={
            "name": "Rate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "total_digits": 11,
            "fraction_digits": 10,
        },
    )
    taxbl_base_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TaxblBaseAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ttl_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dtls: list[TaxRecordDetails3] = field(
        default_factory=list,
        metadata={
            "name": "Dtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification8:
    fin_instn_id: FinancialInstitutionIdentification23 = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    brnch_id: None | BranchData5 = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification272:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    pstl_adr: None | PostalAddress27 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    id: None | Party52Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ctry_of_res: None | str = field(
        default=None,
        metadata={
            "name": "CtryOfRes",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[A-Z]{2,2}",
        },
    )
    ctct_dtls: None | Contact13 = field(
        default=None,
        metadata={
            "name": "CtctDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class ReferredDocumentInformation8:
    tp: None | DocumentType1 = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    nb: None | str = field(
        default=None,
        metadata={
            "name": "Nb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    rltd_dt: None | DateAndType1 = field(
        default=None,
        metadata={
            "name": "RltdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    line_dtls: list[DocumentLineInformation2] = field(
        default_factory=list,
        metadata={
            "name": "LineDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class TaxRecord3:
    tp: None | str = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctgy: None | str = field(
        default=None,
        metadata={
            "name": "Ctgy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctgy_dtls: None | str = field(
        default=None,
        metadata={
            "name": "CtgyDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dbtr_sts: None | str = field(
        default=None,
        metadata={
            "name": "DbtrSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    cert_id: None | str = field(
        default=None,
        metadata={
            "name": "CertId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    frms_cd: None | str = field(
        default=None,
        metadata={
            "name": "FrmsCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prd: None | TaxPeriod3 = field(
        default=None,
        metadata={
            "name": "Prd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    tax_amt: None | TaxAmount3 = field(
        default=None,
        metadata={
            "name": "TaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class AmendmentInformationDetails15:
    orgnl_mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlMndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_cdtr_schme_id: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "OrgnlCdtrSchmeId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    orgnl_cdtr_agt: None | BranchAndFinancialInstitutionIdentification8 = (
        field(
            default=None,
            metadata={
                "name": "OrgnlCdtrAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            },
        )
    )
    orgnl_cdtr_agt_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "OrgnlCdtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    orgnl_dbtr: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "OrgnlDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    orgnl_dbtr_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "OrgnlDbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    orgnl_dbtr_agt: None | BranchAndFinancialInstitutionIdentification8 = (
        field(
            default=None,
            metadata={
                "name": "OrgnlDbtrAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            },
        )
    )
    orgnl_dbtr_agt_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "OrgnlDbtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    orgnl_fnl_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "OrgnlFnlColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    orgnl_frqcy: None | Frequency36Choice = field(
        default=None,
        metadata={
            "name": "OrgnlFrqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    orgnl_rsn: None | MandateSetupReason1Choice = field(
        default=None,
        metadata={
            "name": "OrgnlRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    orgnl_trckg_days: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlTrckgDays",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[0-9]{2}",
        },
    )


@dataclass(kw_only=True)
class Charges16:
    amt: ActiveOrHistoricCurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    agt: BranchAndFinancialInstitutionIdentification8 = field(
        metadata={
            "name": "Agt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    tp: None | ChargeType3Choice = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class Garnishment4:
    tp: GarnishmentType1 = field(
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    grnshee: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "Grnshee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    grnshmt_admstr: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "GrnshmtAdmstr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ref_nb: None | str = field(
        default=None,
        metadata={
            "name": "RefNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    rmtd_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "RmtdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    fmly_mdcl_insrnc_ind: None | bool = field(
        default=None,
        metadata={
            "name": "FmlyMdclInsrncInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    mplyee_termntn_ind: None | bool = field(
        default=None,
        metadata={
            "name": "MplyeeTermntnInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class GroupHeader128:
    msg_id: str = field(
        metadata={
            "name": "MsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    initg_pty: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "InitgPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    fwdg_agt: None | BranchAndFinancialInstitutionIdentification8 = field(
        default=None,
        metadata={
            "name": "FwdgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dbtr_agt: None | BranchAndFinancialInstitutionIdentification8 = field(
        default=None,
        metadata={
            "name": "DbtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    cdtr_agt: None | BranchAndFinancialInstitutionIdentification8 = field(
        default=None,
        metadata={
            "name": "CdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class Party50Choice:
    pty: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "Pty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    agt: None | BranchAndFinancialInstitutionIdentification8 = field(
        default=None,
        metadata={
            "name": "Agt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class SettlementInstruction15:
    sttlm_mtd: SettlementMethod1Code = field(
        metadata={
            "name": "SttlmMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    sttlm_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "SttlmAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    clr_sys: None | ClearingSystemIdentification3Choice = field(
        default=None,
        metadata={
            "name": "ClrSys",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    instg_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification8 = (
        field(
            default=None,
            metadata={
                "name": "InstgRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            },
        )
    )
    instg_rmbrsmnt_agt_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "InstgRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    instd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification8 = (
        field(
            default=None,
            metadata={
                "name": "InstdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            },
        )
    )
    instd_rmbrsmnt_agt_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "InstdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    thrd_rmbrsmnt_agt: None | BranchAndFinancialInstitutionIdentification8 = (
        field(
            default=None,
            metadata={
                "name": "ThrdRmbrsmntAgt",
                "type": "Element",
                "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            },
        )
    )
    thrd_rmbrsmnt_agt_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "ThrdRmbrsmntAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class StatusReasonInformation14:
    orgtr: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "Orgtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    rsn: None | StatusReason6Choice = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    addtl_inf: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 105,
        },
    )


@dataclass(kw_only=True)
class TaxData1:
    cdtr: None | TaxParty1 = field(
        default=None,
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dbtr: None | TaxParty2 = field(
        default=None,
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ultmt_dbtr: None | TaxParty2 = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    admstn_zone: None | str = field(
        default=None,
        metadata={
            "name": "AdmstnZone",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ref_nb: None | str = field(
        default=None,
        metadata={
            "name": "RefNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    mtd: None | str = field(
        default=None,
        metadata={
            "name": "Mtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ttl_taxbl_base_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxblBaseAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ttl_tax_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "TtlTaxAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Dt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    seq_nb: None | Decimal = field(
        default=None,
        metadata={
            "name": "SeqNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "total_digits": 18,
            "fraction_digits": 0,
        },
    )
    rcrd: list[TaxRecord3] = field(
        default_factory=list,
        metadata={
            "name": "Rcrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class TrackerRecord5:
    agt: BranchAndFinancialInstitutionIdentification8 = field(
        metadata={
            "name": "Agt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    chrg_br: None | ChargeBearerType1Code = field(
        default=None,
        metadata={
            "name": "ChrgBr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    chrgs_amt: None | ActiveCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "ChrgsAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    xchg_rate_data: None | CurrencyExchange13 = field(
        default=None,
        metadata={
            "name": "XchgRateData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class MandateRelatedInformation16:
    mndt_id: None | str = field(
        default=None,
        metadata={
            "name": "MndtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    dt_of_sgntr: None | XmlDate = field(
        default=None,
        metadata={
            "name": "DtOfSgntr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    amdmnt_ind: None | bool = field(
        default=None,
        metadata={
            "name": "AmdmntInd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    amdmnt_inf_dtls: None | AmendmentInformationDetails15 = field(
        default=None,
        metadata={
            "name": "AmdmntInfDtls",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    elctrnc_sgntr: None | str = field(
        default=None,
        metadata={
            "name": "ElctrncSgntr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 1025,
        },
    )
    frst_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "FrstColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    fnl_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "FnlColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    frqcy: None | Frequency36Choice = field(
        default=None,
        metadata={
            "name": "Frqcy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    rsn: None | MandateSetupReason1Choice = field(
        default=None,
        metadata={
            "name": "Rsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    trckg_days: None | str = field(
        default=None,
        metadata={
            "name": "TrckgDays",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[0-9]{2}",
        },
    )


@dataclass(kw_only=True)
class OriginalGroupHeader22:
    orgnl_msg_id: str = field(
        metadata={
            "name": "OrgnlMsgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    orgnl_msg_nm_id: str = field(
        metadata={
            "name": "OrgnlMsgNmId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    orgnl_cre_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "OrgnlCreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    orgnl_nb_of_txs: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlNbOfTxs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[0-9]{1,15}",
        },
    )
    orgnl_ctrl_sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "OrgnlCtrlSum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    grp_sts: None | str = field(
        default=None,
        metadata={
            "name": "GrpSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    sts_rsn_inf: list[StatusReasonInformation14] = field(
        default_factory=list,
        metadata={
            "name": "StsRsnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    nb_of_txs_per_sts: list[NumberOfTransactionsPerStatus5] = field(
        default_factory=list,
        metadata={
            "name": "NbOfTxsPerSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class StructuredRemittanceInformation18:
    rfrd_doc_inf: list[ReferredDocumentInformation8] = field(
        default_factory=list,
        metadata={
            "name": "RfrdDocInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    rfrd_doc_amt: None | RemittanceAmount4 = field(
        default=None,
        metadata={
            "name": "RfrdDocAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    cdtr_ref_inf: None | CreditorReferenceInformation3 = field(
        default=None,
        metadata={
            "name": "CdtrRefInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    invcr: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "Invcr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    invcee: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "Invcee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    tax_rmt: None | TaxData1 = field(
        default=None,
        metadata={
            "name": "TaxRmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    grnshmt_rmt: None | Garnishment4 = field(
        default=None,
        metadata={
            "name": "GrnshmtRmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    addtl_rmt_inf: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AddtlRmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "max_occurs": 3,
            "min_length": 1,
            "max_length": 140,
        },
    )


@dataclass(kw_only=True)
class TrackerData7:
    confd_dt: DateAndDateTime2Choice = field(
        metadata={
            "name": "ConfdDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    confd_amt: ActiveCurrencyAndAmount = field(
        metadata={
            "name": "ConfdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    trckr_rcrd: list[TrackerRecord5] = field(
        default_factory=list,
        metadata={
            "name": "TrckrRcrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class MandateRelatedData3Choice:
    drct_dbt_mndt: None | MandateRelatedInformation16 = field(
        default=None,
        metadata={
            "name": "DrctDbtMndt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    cdt_trf_mndt: None | CreditTransferMandateData1 = field(
        default=None,
        metadata={
            "name": "CdtTrfMndt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class RemittanceInformation22:
    ustrd: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Ustrd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 140,
        },
    )
    strd: list[StructuredRemittanceInformation18] = field(
        default_factory=list,
        metadata={
            "name": "Strd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class OriginalTransactionReference42:
    intr_bk_sttlm_amt: None | ActiveOrHistoricCurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    amt: None | AmountType4Choice = field(
        default=None,
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    intr_bk_sttlm_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "IntrBkSttlmDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    reqd_colltn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ReqdColltnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    reqd_exctn_dt: None | DateAndDateTime2Choice = field(
        default=None,
        metadata={
            "name": "ReqdExctnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    cdtr_schme_id: None | PartyIdentification272 = field(
        default=None,
        metadata={
            "name": "CdtrSchmeId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    sttlm_inf: None | SettlementInstruction15 = field(
        default=None,
        metadata={
            "name": "SttlmInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    pmt_tp_inf: None | PaymentTypeInformation27 = field(
        default=None,
        metadata={
            "name": "PmtTpInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    pmt_mtd: None | PaymentMethod4Code = field(
        default=None,
        metadata={
            "name": "PmtMtd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    mndt_rltd_inf: None | MandateRelatedData3Choice = field(
        default=None,
        metadata={
            "name": "MndtRltdInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    rmt_inf: None | RemittanceInformation22 = field(
        default=None,
        metadata={
            "name": "RmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ultmt_dbtr: None | Party50Choice = field(
        default=None,
        metadata={
            "name": "UltmtDbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dbtr: None | Party50Choice = field(
        default=None,
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dbtr_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dbtr_agt: None | BranchAndFinancialInstitutionIdentification8 = field(
        default=None,
        metadata={
            "name": "DbtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    dbtr_agt_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "DbtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    cdtr_agt: None | BranchAndFinancialInstitutionIdentification8 = field(
        default=None,
        metadata={
            "name": "CdtrAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    cdtr_agt_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "CdtrAgtAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    cdtr: None | Party50Choice = field(
        default=None,
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    cdtr_acct: None | CashAccount40 = field(
        default=None,
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    ultmt_cdtr: None | Party50Choice = field(
        default=None,
        metadata={
            "name": "UltmtCdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    purp: None | Purpose2Choice = field(
        default=None,
        metadata={
            "name": "Purp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class PaymentTransaction160:
    sts_id: None | str = field(
        default=None,
        metadata={
            "name": "StsId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_instr_id: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlInstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_end_to_end_id: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlEndToEndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_uetr: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlUETR",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}",
        },
    )
    tx_sts: None | str = field(
        default=None,
        metadata={
            "name": "TxSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    sts_rsn_inf: list[StatusReasonInformation14] = field(
        default_factory=list,
        metadata={
            "name": "StsRsnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    chrgs_inf: list[Charges16] = field(
        default_factory=list,
        metadata={
            "name": "ChrgsInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    trckr_data: None | TrackerData7 = field(
        default=None,
        metadata={
            "name": "TrckrData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    accptnc_dt_tm: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "AccptncDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    acct_svcr_ref: None | str = field(
        default=None,
        metadata={
            "name": "AcctSvcrRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    clr_sys_ref: None | str = field(
        default=None,
        metadata={
            "name": "ClrSysRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 35,
        },
    )
    orgnl_tx_ref: None | OriginalTransactionReference42 = field(
        default=None,
        metadata={
            "name": "OrgnlTxRef",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class OriginalPaymentInstruction51:
    orgnl_pmt_inf_id: str = field(
        metadata={
            "name": "OrgnlPmtInfId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    orgnl_nb_of_txs: None | str = field(
        default=None,
        metadata={
            "name": "OrgnlNbOfTxs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "pattern": r"[0-9]{1,15}",
        },
    )
    orgnl_ctrl_sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "OrgnlCtrlSum",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "total_digits": 18,
            "fraction_digits": 17,
        },
    )
    pmt_inf_sts: None | str = field(
        default=None,
        metadata={
            "name": "PmtInfSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "min_length": 1,
            "max_length": 4,
        },
    )
    sts_rsn_inf: list[StatusReasonInformation14] = field(
        default_factory=list,
        metadata={
            "name": "StsRsnInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    nb_of_txs_per_sts: list[NumberOfTransactionsPerStatus5] = field(
        default_factory=list,
        metadata={
            "name": "NbOfTxsPerSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    tx_inf_and_sts: list[PaymentTransaction160] = field(
        default_factory=list,
        metadata={
            "name": "TxInfAndSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class CustomerPaymentStatusReportV14:
    grp_hdr: GroupHeader128 = field(
        metadata={
            "name": "GrpHdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    orgnl_grp_inf_and_sts: OriginalGroupHeader22 = field(
        metadata={
            "name": "OrgnlGrpInfAndSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
            "required": True,
        }
    )
    orgnl_pmt_inf_and_sts: list[OriginalPaymentInstruction51] = field(
        default_factory=list,
        metadata={
            "name": "OrgnlPmtInfAndSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )
    splmtry_data: list[SupplementaryData1] = field(
        default_factory=list,
        metadata={
            "name": "SplmtryData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:tech:xsd:pain.002.001.14"

    cstmr_pmt_sts_rpt: CustomerPaymentStatusReportV14 = field(
        metadata={
            "name": "CstmrPmtStsRpt",
            "type": "Element",
            "required": True,
        }
    )
