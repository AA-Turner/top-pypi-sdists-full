# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1llll1ll11l_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1lllllll1ll_opy_:
    bstack11llll11l11_opy_ = bstack111l111_opy_ (u"ࠦࡧ࡫࡮ࡤࡪࡰࡥࡷࡱࠢᗖ")
    context: bstack1llll1ll11l_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1llll1ll11l_opy_):
        self.context = context
        self.data = dict({bstack1lllllll1ll_opy_.bstack11llll11l11_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᗗ"), bstack111l111_opy_ (u"࠭࠰ࠨᗘ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1lllll111l1_opy_(self, target: object):
        return bstack1lllllll1ll_opy_.create_context(target) == self.context
    def bstack1l1llllll11_opy_(self, context: bstack1llll1ll11l_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack111111l1_opy_(self, key: str, value: timedelta):
        self.data[bstack1lllllll1ll_opy_.bstack11llll11l11_opy_][key] += value
    def bstack1ll1l1lllll_opy_(self) -> dict:
        return self.data[bstack1lllllll1ll_opy_.bstack11llll11l11_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1llll1ll11l_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )