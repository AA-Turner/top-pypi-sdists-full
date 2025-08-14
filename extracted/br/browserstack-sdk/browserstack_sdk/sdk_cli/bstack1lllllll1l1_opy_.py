# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1lllll11111_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1llll1ll11l_opy_:
    bstack11llll11l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡨࡥ࡯ࡥ࡫ࡱࡦࡸ࡫ࠣᗞ")
    context: bstack1lllll11111_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1lllll11111_opy_):
        self.context = context
        self.data = dict({bstack1llll1ll11l_opy_.bstack11llll11l1l_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᗟ"), bstack1l1l1ll_opy_ (u"ࠧ࠱ࠩᗠ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1llllll111l_opy_(self, target: object):
        return bstack1llll1ll11l_opy_.create_context(target) == self.context
    def bstack1l1llll1l1l_opy_(self, context: bstack1lllll11111_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll1ll11ll_opy_(self, key: str, value: timedelta):
        self.data[bstack1llll1ll11l_opy_.bstack11llll11l1l_opy_][key] += value
    def bstack1ll1ll1llll_opy_(self) -> dict:
        return self.data[bstack1llll1ll11l_opy_.bstack11llll11l1l_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1lllll11111_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )