from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "urn:iso:std:iso:20022:xsd:pain.002.001.01"


class AddressType2Code(Enum):
    ADDR = "ADDR"
    PBOX = "PBOX"
    HOME = "HOME"
    BIZZ = "BIZZ"
    MLTO = "MLTO"
    DLVY = "DLVY"


class CashAccountType3Code(Enum):
    CASH = "CASH"
    CHAR = "CHAR"
    SACC = "SACC"
    CACC = "CACC"
    SVGS = "SVGS"


class CashClearingSystem2Code(Enum):
    RTG = "RTG"
    ACH = "ACH"
    CHI = "CHI"
    FDN = "FDN"


@dataclass(kw_only=True)
class ClearingSystemMemberIdentificationChoice:
    uschu: None | str = field(
        default=None,
        metadata={
            "name": "USCHU",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"CH[0-9]{6,6}",
        },
    )
    nzncc: None | str = field(
        default=None,
        metadata={
            "name": "NZNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"NZ[0-9]{6,6}",
        },
    )
    iensc: None | str = field(
        default=None,
        metadata={
            "name": "IENSC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"IE[0-9]{6,6}",
        },
    )
    gbsc: None | str = field(
        default=None,
        metadata={
            "name": "GBSC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"SC[0-9]{6,6}",
        },
    )
    usch: None | str = field(
        default=None,
        metadata={
            "name": "USCH",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"CP[0-9]{4,4}",
        },
    )
    chbc: None | str = field(
        default=None,
        metadata={
            "name": "CHBC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"SW[0-9]{3,5}",
        },
    )
    usfw: None | str = field(
        default=None,
        metadata={
            "name": "USFW",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"FW[0-9]{9,9}",
        },
    )
    ptncc: None | str = field(
        default=None,
        metadata={
            "name": "PTNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"PT[0-9]{8,8}",
        },
    )
    rucb: None | str = field(
        default=None,
        metadata={
            "name": "RUCB",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"RU[0-9]{9,9}",
        },
    )
    itncc: None | str = field(
        default=None,
        metadata={
            "name": "ITNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"IT[0-9]{10,10}",
        },
    )
    atblz: None | str = field(
        default=None,
        metadata={
            "name": "ATBLZ",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"AT[0-9]{5,5}",
        },
    )
    cacpa: None | str = field(
        default=None,
        metadata={
            "name": "CACPA",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"CA[0-9]{9,9}",
        },
    )
    chsic: None | str = field(
        default=None,
        metadata={
            "name": "CHSIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"SW[0-9]{6,6}",
        },
    )
    deblz: None | str = field(
        default=None,
        metadata={
            "name": "DEBLZ",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"BL[0-9]{8,8}",
        },
    )
    esncc: None | str = field(
        default=None,
        metadata={
            "name": "ESNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"ES[0-9]{8,9}",
        },
    )
    zancc: None | str = field(
        default=None,
        metadata={
            "name": "ZANCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"ZA[0-9]{6,6}",
        },
    )
    hkncc: None | str = field(
        default=None,
        metadata={
            "name": "HKNCC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"HK[0-9]{3,3}",
        },
    )
    aubsbx: None | str = field(
        default=None,
        metadata={
            "name": "AUBSBx",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"AU[0-9]{6,6}",
        },
    )
    aubsbs: None | str = field(
        default=None,
        metadata={
            "name": "AUBSBs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"AU[0-9]{6,6}",
        },
    )


class CreditTransferType2Code(Enum):
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
class GenericIdentification3:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    id_tp: str = field(
        metadata={
            "name": "IdTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


class PaymentGroupStatusCode(Enum):
    ACTC = "ACTC"
    RCVD = "RCVD"
    PART = "PART"
    RJCT = "RJCT"
    PDNG = "PDNG"
    ACCP = "ACCP"
    ACSP = "ACSP"
    ACSC = "ACSC"


@dataclass(kw_only=True)
class PaymentIdentification:
    instr_id: None | str = field(
        default=None,
        metadata={
            "name": "InstrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    end_to_end_id: str = field(
        metadata={
            "name": "EndToEndId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    pmt_rmt_id: None | str = field(
        default=None,
        metadata={
            "name": "PmtRmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


class PaymentMethod1Code(Enum):
    CHK = "CHK"
    TRF = "TRF"


class PaymentReject1Code(Enum):
    AC01 = "AC01"
    AC02 = "AC02"
    AC03 = "AC03"
    AC04 = "AC04"
    AC05 = "AC05"
    AC06 = "AC06"
    AM01 = "AM01"
    AM02 = "AM02"
    AM03 = "AM03"
    AM04 = "AM04"
    AM05 = "AM05"
    AM06 = "AM06"
    AM07 = "AM07"
    AM08 = "AM08"
    BE01 = "BE01"
    BE02 = "BE02"
    BE03 = "BE03"
    BE04 = "BE04"
    BE05 = "BE05"
    AG01 = "AG01"
    AG02 = "AG02"
    DT01 = "DT01"
    MS01 = "MS01"
    PY01 = "PY01"
    RF01 = "RF01"
    RC01 = "RC01"
    RC02 = "RC02"
    RC03 = "RC03"
    RC04 = "RC04"
    TM01 = "TM01"
    ED01 = "ED01"
    ED02 = "ED02"
    ED03 = "ED03"
    ED04 = "ED04"


class PaymentTransactionStatusCode(Enum):
    ACTC = "ACTC"
    RJCT = "RJCT"
    PDNG = "PDNG"
    ACCP = "ACCP"
    ACSP = "ACSP"
    ACSC = "ACSC"


class Priority2Code(Enum):
    HIGH = "HIGH"
    NORM = "NORM"


@dataclass(kw_only=True)
class SimpleIdentificationInformation:
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )


@dataclass(kw_only=True)
class AccountIdentification1Choice:
    iban: None | str = field(
        default=None,
        metadata={
            "name": "IBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"[a-zA-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}",
        },
    )
    bban: None | str = field(
        default=None,
        metadata={
            "name": "BBAN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"[a-zA-Z0-9]{1,30}",
        },
    )
    upic: None | str = field(
        default=None,
        metadata={
            "name": "UPIC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"[0-9]{8,17}",
        },
    )
    dmst_acct: None | SimpleIdentificationInformation = field(
        default=None,
        metadata={
            "name": "DmstAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class EquivalentAmount:
    amt: CurrencyAndAmount = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
        }
    )
    ccy_of_trf: str = field(
        metadata={
            "name": "CcyOfTrf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
            "pattern": r"[A-Z]{3,3}",
        }
    )


@dataclass(kw_only=True)
class NonFinancialInstitutionIdentification1:
    bei: None | str = field(
        default=None,
        metadata={
            "name": "BEI",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    eangln: None | str = field(
        default=None,
        metadata={
            "name": "EANGLN",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"[0-9]{13,13}",
        },
    )
    uschu: None | str = field(
        default=None,
        metadata={
            "name": "USCHU",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"CH[0-9]{6,6}",
        },
    )
    duns: None | str = field(
        default=None,
        metadata={
            "name": "DUNS",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"[0-9]{9,9}",
        },
    )
    bk_pty_id: None | str = field(
        default=None,
        metadata={
            "name": "BkPtyId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class OriginalGroupReferenceInformation1:
    grp_id: str = field(
        metadata={
            "name": "GrpId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    orgnl_msg_tp: str = field(
        metadata={
            "name": "OrgnlMsgTp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    grp_sts: None | PaymentGroupStatusCode = field(
        default=None,
        metadata={
            "name": "GrpSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    sts_rsn: None | PaymentReject1Code = field(
        default=None,
        metadata={
            "name": "StsRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 105,
        },
    )


@dataclass(kw_only=True)
class PaymentSchemeChoice:
    cd: None | CashClearingSystem2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    prtry_inf: None | str = field(
        default=None,
        metadata={
            "name": "PrtryInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )


@dataclass(kw_only=True)
class PersonIdentification2:
    drvrs_lic_nb: None | str = field(
        default=None,
        metadata={
            "name": "DrvrsLicNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    scl_scty_nb: None | str = field(
        default=None,
        metadata={
            "name": "SclSctyNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    aln_regn_nb: None | str = field(
        default=None,
        metadata={
            "name": "AlnRegnNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pspt_nb: None | str = field(
        default=None,
        metadata={
            "name": "PsptNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    tax_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "TaxIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    idnty_card_nb: None | str = field(
        default=None,
        metadata={
            "name": "IdntyCardNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    mplyr_id_nb: None | str = field(
        default=None,
        metadata={
            "name": "MplyrIdNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    othr_id: None | GenericIdentification4 = field(
        default=None,
        metadata={
            "name": "OthrId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    issr: None | str = field(
        default=None,
        metadata={
            "name": "Issr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    adr_line: list[str] = field(
        default_factory=list,
        metadata={
            "name": "AdrLine",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    bldg_nb: None | str = field(
        default=None,
        metadata={
            "name": "BldgNb",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    pst_cd: None | str = field(
        default=None,
        metadata={
            "name": "PstCd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 16,
        },
    )
    twn_nm: None | str = field(
        default=None,
        metadata={
            "name": "TwnNm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry_sub_dvsn: None | str = field(
        default=None,
        metadata={
            "name": "CtrySubDvsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    ctry: str = field(
        metadata={
            "name": "Ctry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
            "pattern": r"[A-Z]{2,2}",
        }
    )


@dataclass(kw_only=True)
class AmountType1Choice:
    instd_amt: None | CurrencyAndAmount = field(
        default=None,
        metadata={
            "name": "InstdAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    eqvt_amt: None | EquivalentAmount = field(
        default=None,
        metadata={
            "name": "EqvtAmt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchData:
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class CashAccount3:
    id: AccountIdentification1Choice = field(
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
        }
    )
    tp: None | CashAccountType3Code = field(
        default=None,
        metadata={
            "name": "Tp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    ccy: None | str = field(
        default=None,
        metadata={
            "name": "Ccy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"[A-Z]{3,3}",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
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
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "pattern": r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}",
        },
    )
    clr_sys_mmb_id: None | ClearingSystemMemberIdentificationChoice = field(
        default=None,
        metadata={
            "name": "ClrSysMmbId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    prtry_id: None | GenericIdentification3 = field(
        default=None,
        metadata={
            "name": "PrtryId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class Party1Choice:
    org_id: None | NonFinancialInstitutionIdentification1 = field(
        default=None,
        metadata={
            "name": "OrgId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    prvt_id: list[PersonIdentification2] = field(
        default_factory=list,
        metadata={
            "name": "PrvtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "max_occurs": 2,
        },
    )


@dataclass(kw_only=True)
class SettlementPriorityChoice:
    prty: None | Priority2Code = field(
        default=None,
        metadata={
            "name": "Prty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    pmt_schme: None | PaymentSchemeChoice = field(
        default=None,
        metadata={
            "name": "PmtSchme",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class BranchAndFinancialInstitutionIdentification:
    fin_instn_id: FinancialInstitutionIdentification1 = field(
        metadata={
            "name": "FinInstnId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
        }
    )
    brnch_id: None | BranchData = field(
        default=None,
        metadata={
            "name": "BrnchId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class CreditTransferTypeIdentification:
    cd: None | CreditTransferType2Code = field(
        default=None,
        metadata={
            "name": "Cd",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    lcl_instrm: None | str = field(
        default=None,
        metadata={
            "name": "LclInstrm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 35,
        },
    )
    instr_prty: None | Priority2Code = field(
        default=None,
        metadata={
            "name": "InstrPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    sttlm_prty: None | SettlementPriorityChoice = field(
        default=None,
        metadata={
            "name": "SttlmPrty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class PartyIdentification1:
    nm: None | str = field(
        default=None,
        metadata={
            "name": "Nm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 70,
        },
    )
    pstl_adr: None | PostalAddress1 = field(
        default=None,
        metadata={
            "name": "PstlAdr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    id: None | Party1Choice = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class GeneralInformation1:
    pmt_initn_sts_id: str = field(
        metadata={
            "name": "PmtInitnStsId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
            "min_length": 1,
            "max_length": 35,
        }
    )
    cre_dt_tm: XmlDateTime = field(
        metadata={
            "name": "CreDtTm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
        }
    )
    fwdg_agt: None | BranchAndFinancialInstitutionIdentification = field(
        default=None,
        metadata={
            "name": "FwdgAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    initg_pty: PartyIdentification1 = field(
        metadata={
            "name": "InitgPty",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
        }
    )
    frst_agt: None | BranchAndFinancialInstitutionIdentification = field(
        default=None,
        metadata={
            "name": "FrstAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class OriginalTransactionInformation1:
    amt: AmountType1Choice = field(
        metadata={
            "name": "Amt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
        }
    )
    cdtr: None | PartyIdentification1 = field(
        default=None,
        metadata={
            "name": "Cdtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    cdtr_acct: None | CashAccount3 = field(
        default=None,
        metadata={
            "name": "CdtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    fnl_agt: None | BranchAndFinancialInstitutionIdentification = field(
        default=None,
        metadata={
            "name": "FnlAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class PaymentReference1:
    pmt_id: PaymentIdentification = field(
        metadata={
            "name": "PmtId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
        }
    )
    tx_sts: None | PaymentTransactionStatusCode = field(
        default=None,
        metadata={
            "name": "TxSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    sts_rsn: None | PaymentReject1Code = field(
        default=None,
        metadata={
            "name": "StsRsn",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    addtl_inf: None | str = field(
        default=None,
        metadata={
            "name": "AddtlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "min_length": 1,
            "max_length": 105,
        },
    )
    orgnl_tx_inf: None | OriginalTransactionInformation1 = field(
        default=None,
        metadata={
            "name": "OrgnlTxInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class PaymentInformation9:
    reqd_exctn_dt: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ReqdExctnDt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    pmt_mtd_by_frst_agt: None | PaymentMethod1Code = field(
        default=None,
        metadata={
            "name": "PmtMtdByFrstAgt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    cdt_trf_tp_id: None | CreditTransferTypeIdentification = field(
        default=None,
        metadata={
            "name": "CdtTrfTpId",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    dbtr: None | PartyIdentification1 = field(
        default=None,
        metadata={
            "name": "Dbtr",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    dbtr_acct: None | CashAccount3 = field(
        default=None,
        metadata={
            "name": "DbtrAcct",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )
    orgnl_tx_ref_inf_and_sts: list[PaymentReference1] = field(
        default_factory=list,
        metadata={
            "name": "OrgnlTxRefInfAndSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class Pain00200101:
    class Meta:
        name = "pain.002.001.01"

    gnl_inf: GeneralInformation1 = field(
        metadata={
            "name": "GnlInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
        }
    )
    orgnl_grp_ref_inf_and_sts: OriginalGroupReferenceInformation1 = field(
        metadata={
            "name": "OrgnlGrpRefInfAndSts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
            "required": True,
        }
    )
    orgnl_pmt_inf: list[PaymentInformation9] = field(
        default_factory=list,
        metadata={
            "name": "OrgnlPmtInf",
            "type": "Element",
            "namespace": "urn:iso:std:iso:20022:xsd:pain.002.001.01",
        },
    )


@dataclass(kw_only=True)
class Document:
    class Meta:
        namespace = "urn:iso:std:iso:20022:xsd:pain.002.001.01"

    pain_002_001_01: Pain00200101 = field(
        metadata={
            "name": "pain.002.001.01",
            "type": "Element",
            "required": True,
        }
    )
