# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1llll1l1ll1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1lllll11lll_opy_:
    bstack11llll11111_opy_ = bstack1111l1l_opy_ (u"ࠥࡦࡪࡴࡣࡩ࡯ࡤࡶࡰࠨᗣ")
    context: bstack1llll1l1ll1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1llll1l1ll1_opy_):
        self.context = context
        self.data = dict({bstack1lllll11lll_opy_.bstack11llll11111_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᗤ"), bstack1111l1l_opy_ (u"ࠬ࠶ࠧᗥ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1llllll1l11_opy_(self, target: object):
        return bstack1lllll11lll_opy_.create_context(target) == self.context
    def bstack1l1llll1l1l_opy_(self, context: bstack1llll1l1ll1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack11l11lll_opy_(self, key: str, value: timedelta):
        self.data[bstack1lllll11lll_opy_.bstack11llll11111_opy_][key] += value
    def bstack1llll11l1l1_opy_(self) -> dict:
        return self.data[bstack1lllll11lll_opy_.bstack11llll11111_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1llll1l1ll1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )