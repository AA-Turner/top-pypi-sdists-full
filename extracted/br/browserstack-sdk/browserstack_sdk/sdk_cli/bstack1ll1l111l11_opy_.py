# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1ll11llll1l_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1ll11lll1ll_opy_:
    bstack11l11l1llll_opy_ = bstack1ll111_opy_ (u"ࠧࡨࡥ࡯ࡥ࡫ࡱࡦࡸ࡫ࠣᥗ")
    context: bstack1ll11llll1l_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1ll11llll1l_opy_):
        self.context = context
        self.data = dict({bstack1ll11lll1ll_opy_.bstack11l11l1llll_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᥘ"), bstack1ll111_opy_ (u"ࠧ࠱ࠩᥙ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1ll1ll11l1l_opy_(self, target: object):
        return bstack1ll11lll1ll_opy_.create_context(target) == self.context
    def bstack1l11l1l1l1l_opy_(self, context: bstack1ll11llll1l_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack11l11l1ll1_opy_(self, key: str, value: timedelta):
        self.data[bstack1ll11lll1ll_opy_.bstack11l11l1llll_opy_][key] += value
    def bstack1ll11l111ll_opy_(self) -> dict:
        return self.data[bstack1ll11lll1ll_opy_.bstack11l11l1llll_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1ll11llll1l_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )