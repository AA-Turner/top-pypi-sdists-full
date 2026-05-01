# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1l1ll1111l1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1l1ll1l1l1l_opy_:
    bstack111l1l111l1_opy_ = bstack111ll_opy_ (u"ࠦࡧ࡫࡮ࡤࡪࡰࡥࡷࡱࠢ᭣")
    context: bstack1l1ll1111l1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1l1ll1111l1_opy_):
        self.context = context
        self.data = dict({bstack1l1ll1l1l1l_opy_.bstack111l1l111l1_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᭤"), bstack111ll_opy_ (u"࠭࠰ࠨ᭥")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1l1ll1l1l11_opy_(self, target: object):
        return bstack1l1ll1l1l1l_opy_.create_context(target) == self.context
    def bstack11lll1l1l11_opy_(self, context: bstack1l1ll1111l1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll11111l_opy_(self, key: str, value: timedelta):
        self.data[bstack1l1ll1l1l1l_opy_.bstack111l1l111l1_opy_][key] += value
    def bstack1l1l11l1ll1_opy_(self) -> dict:
        return self.data[bstack1l1ll1l1l1l_opy_.bstack111l1l111l1_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1l1ll1111l1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )