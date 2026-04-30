# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1l1ll1ll11l_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1l1ll11lll1_opy_:
    bstack111l1l11l1l_opy_ = bstack1l1111l_opy_ (u"ࠥࡦࡪࡴࡣࡩ࡯ࡤࡶࡰࠨ᭔")
    context: bstack1l1ll1ll11l_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1l1ll1ll11l_opy_):
        self.context = context
        self.data = dict({bstack1l1ll11lll1_opy_.bstack111l1l11l1l_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᭕"), bstack1l1111l_opy_ (u"ࠬ࠶ࠧ᭖")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1l1ll11l11l_opy_(self, target: object):
        return bstack1l1ll11lll1_opy_.create_context(target) == self.context
    def bstack11lll1ll1l1_opy_(self, context: bstack1l1ll1ll11l_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll11l11l_opy_(self, key: str, value: timedelta):
        self.data[bstack1l1ll11lll1_opy_.bstack111l1l11l1l_opy_][key] += value
    def bstack1l11ll1ll11_opy_(self) -> dict:
        return self.data[bstack1l1ll11lll1_opy_.bstack111l1l11l1l_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1l1ll1ll11l_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )