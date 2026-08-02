from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from numbers import Number
from typing import Union


class FontType(Enum):
    COURIER = "Courier"
    TIMES = "Times"


@dataclass
class Margins:
    top: Number = 5
    right: Number = 5
    bottom: Number = 5
    left: Number = 5


class ModalType(Enum):
    RODOVIARIO = "RODOVIÁRIO"
    AEREO = "AÉREO"
    AQUAVIARIO = "AQUAVIÁRIO"
    FERROVIARIO = "FERROVIÁRIO"
    DUTOVIARIO = "DUTOVIÁRIO"
    MULTIMODAL = "MULTIMODAL"


@dataclass
class DecimalConfig:
    price_precision: int = 4
    quantity_precision: int = 4


class ReceiptPosition(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"


@dataclass
class DacteConfig:
    logo: Union[str, BytesIO, bytes] = None
    margins: Margins = field(default_factory=Margins)
    receipt_pos: ReceiptPosition = ReceiptPosition.TOP
    decimal_config: DecimalConfig = field(default_factory=DecimalConfig)
    font_type: FontType = FontType.TIMES
    watermark_cancelled: bool = False
    display_ibs_cbs: bool = False
