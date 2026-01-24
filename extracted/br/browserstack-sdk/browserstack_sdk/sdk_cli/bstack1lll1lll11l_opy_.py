# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1lll11lll11_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1lll1l1llll_opy_:
    bstack11ll111llll_opy_ = bstack1l1111_opy_ (u"ࠥࡦࡪࡴࡣࡩ࡯ࡤࡶࡰࠨ᛭")
    context: bstack1lll11lll11_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1lll11lll11_opy_):
        self.context = context
        self.data = dict({bstack1lll1l1llll_opy_.bstack11ll111llll_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᛮ"), bstack1l1111_opy_ (u"ࠬ࠶ࠧᛯ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1lll1l1l1ll_opy_(self, target: object):
        return bstack1lll1l1llll_opy_.create_context(target) == self.context
    def bstack1l1l1l11l11_opy_(self, context: bstack1lll11lll11_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack11l1l11ll_opy_(self, key: str, value: timedelta):
        self.data[bstack1lll1l1llll_opy_.bstack11ll111llll_opy_][key] += value
    def bstack1ll11l1111l_opy_(self) -> dict:
        return self.data[bstack1lll1l1llll_opy_.bstack11ll111llll_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1lll11lll11_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )