# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1lll11l1l11_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1ll1llllll1_opy_:
    bstack11l1ll111l1_opy_ = bstack11l1l11_opy_ (u"ࠦࡧ࡫࡮ࡤࡪࡰࡥࡷࡱࠢះ")
    context: bstack1lll11l1l11_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1lll11l1l11_opy_):
        self.context = context
        self.data = dict({bstack1ll1llllll1_opy_.bstack11l1ll111l1_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬៈ"), bstack11l1l11_opy_ (u"࠭࠰ࠨ៉")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1ll1ll1llll_opy_(self, target: object):
        return bstack1ll1llllll1_opy_.create_context(target) == self.context
    def bstack1l1l111111l_opy_(self, context: bstack1lll11l1l11_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack11l1lllll1_opy_(self, key: str, value: timedelta):
        self.data[bstack1ll1llllll1_opy_.bstack11l1ll111l1_opy_][key] += value
    def bstack1ll111l1lll_opy_(self) -> dict:
        return self.data[bstack1ll1llllll1_opy_.bstack11l1ll111l1_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1lll11l1l11_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )