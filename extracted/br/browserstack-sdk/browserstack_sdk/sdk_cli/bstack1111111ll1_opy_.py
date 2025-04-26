# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1111l11lll_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack11111l1111_opy_:
    bstack1l1111l1ll1_opy_ = bstack1l11lll_opy_ (u"ࠣࡤࡨࡲࡨ࡮࡭ࡢࡴ࡮ࠦᔝ")
    context: bstack1111l11lll_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1111l11lll_opy_):
        self.context = context
        self.data = dict({bstack11111l1111_opy_.bstack1l1111l1ll1_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᔞ"), bstack1l11lll_opy_ (u"ࠪ࠴ࠬᔟ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack11111l1ll1_opy_(self, target: object):
        return bstack11111l1111_opy_.create_context(target) == self.context
    def bstack1ll11l1l1ll_opy_(self, context: bstack1111l11lll_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1l11111ll1_opy_(self, key: str, value: timedelta):
        self.data[bstack11111l1111_opy_.bstack1l1111l1ll1_opy_][key] += value
    def bstack1lllll1l111_opy_(self) -> dict:
        return self.data[bstack11111l1111_opy_.bstack1l1111l1ll1_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1111l11lll_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )