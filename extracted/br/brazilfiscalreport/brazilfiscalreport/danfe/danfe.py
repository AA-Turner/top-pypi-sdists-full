# Copyright (C) 2021-2022 Edson Bernardino <edsones at yahoo.com.br>
# Copyright (C) 2024 Engenere - Antônio S. Pereira Neto <neto@engenere.one>

# Each DANFE layout lives in its own module; this one only picks which of them
# prints the NF-e. When the MOC 7.0 layout is removed, danfe_moc_7_0.py and
# DanfeLayout.MOC_7_0 go away and AUTO always picks NT 2026.010.

import warnings
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

from ..utils import get_tag_text
from .config import DanfeConfig, DanfeLayout
from .danfe_conf import URL
from .danfe_moc_7_0 import DanfeMoc70
from .danfe_nt_2026_010 import DanfeNt2026010

BRASILIA = timezone(timedelta(hours=-3))
# Production date of NT 2026.010.
NT_2026_010_START = datetime(2026, 12, 1, tzinfo=BRASILIA)


def get_issue_datetime(xml):
    """
    Issue date of the NF-e (ide/dhEmi, or ide/dEmi before layout 3.10), or
    None when it is absent or invalid. A date without UTC offset is taken as
    Brasília time.
    """
    ide = ET.fromstring(xml).find(f"{URL}ide")
    text = get_tag_text(ide, URL, "dhEmi") or get_tag_text(ide, URL, "dEmi")
    try:
        issued = datetime.fromisoformat(text)
    except (TypeError, ValueError):
        return None
    if issued.tzinfo is None:
        issued = issued.replace(tzinfo=BRASILIA)
    return issued


def resolve_layout(xml, layout=DanfeLayout.AUTO):
    """
    AUTO prints the NF-e in the layout in force on its issue date, so the
    same XML always gives the same DANFE. Without an issue date, the
    printing date decides.
    """
    if layout != DanfeLayout.AUTO:
        return layout
    issued = get_issue_datetime(xml) or datetime.now(BRASILIA)
    if issued < NT_2026_010_START:
        return DanfeLayout.MOC_7_0
    return DanfeLayout.NT_2026_010


class Danfe:
    """
    DANFE of the NF-e, in the layout chosen by `DanfeConfig.layout`. Returns
    an instance of the class of that layout.
    """

    def __new__(cls, xml, config: DanfeConfig = None):
        config = config if config is not None else DanfeConfig()
        if config.layout == DanfeLayout.MOC_7_0:
            warnings.warn(
                "The MOC 7.0 DANFE layout is deprecated and will be removed in "
                "a future version. NF-e issued from 2026-12-01 on must be "
                "printed in the NT 2026.010 layout.",
                DeprecationWarning,
                stacklevel=2,
            )
        if resolve_layout(xml, config.layout) == DanfeLayout.MOC_7_0:
            return DanfeMoc70(xml, config=config)
        return DanfeNt2026010(xml, config=config)
