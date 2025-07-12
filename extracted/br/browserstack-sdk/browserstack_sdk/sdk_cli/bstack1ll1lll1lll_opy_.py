# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1ll1ll1l11l_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1l1lll111ll_opy_:
    bstack1l1l111l111_opy_ = bstack11l1111_opy_ (u"ࠦࡧ࡫࡮ࡤࡪࡰࡥࡷࡱࠢᑀ")
    context: bstack1ll1ll1l11l_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1ll1ll1l11l_opy_):
        self.context = context
        self.data = dict({bstack1l1lll111ll_opy_.bstack1l1l111l111_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᑁ"), bstack11l1111_opy_ (u"࠭࠰ࠨᑂ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1l1l111l11l_opy_(self, target: object):
        return bstack1l1lll111ll_opy_.create_context(target) == self.context
    def bstack1ll1ll1lll1_opy_(self, context: bstack1ll1ll1l11l_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1llll1l1l_opy_(self, key: str, value: timedelta):
        self.data[bstack1l1lll111ll_opy_.bstack1l1l111l111_opy_][key] += value
    def bstack1l1l1111lll_opy_(self) -> dict:
        return self.data[bstack1l1lll111ll_opy_.bstack1l1l111l111_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1ll1ll1l11l_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )