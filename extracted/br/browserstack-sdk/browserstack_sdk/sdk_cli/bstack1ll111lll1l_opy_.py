# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1ll11l11ll1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1ll11ll11ll_opy_:
    bstack11l11111ll1_opy_ = bstack1ll11_opy_ (u"ࠤࡥࡩࡳࡩࡨ࡮ࡣࡵ࡯ࠧᨃ")
    context: bstack1ll11l11ll1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1ll11l11ll1_opy_):
        self.context = context
        self.data = dict({bstack1ll11ll11ll_opy_.bstack11l11111ll1_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᨄ"), bstack1ll11_opy_ (u"ࠫ࠵࠭ᨅ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1ll11ll1l11_opy_(self, target: object):
        return bstack1ll11ll11ll_opy_.create_context(target) == self.context
    def bstack1l111llll11_opy_(self, context: bstack1ll11l11ll1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1111111ll1_opy_(self, key: str, value: timedelta):
        self.data[bstack1ll11ll11ll_opy_.bstack11l11111ll1_opy_][key] += value
    def bstack1l1lll1llll_opy_(self) -> dict:
        return self.data[bstack1ll11ll11ll_opy_.bstack11l11111ll1_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1ll11l11ll1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )