# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1llllllll11_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1lllllll1l1_opy_:
    bstack11llll11lll_opy_ = bstack11l1_opy_ (u"ࠨࡢࡦࡰࡦ࡬ࡲࡧࡲ࡬ࠤᗘ")
    context: bstack1llllllll11_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1llllllll11_opy_):
        self.context = context
        self.data = dict({bstack1lllllll1l1_opy_.bstack11llll11lll_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᗙ"), bstack11l1_opy_ (u"ࠨ࠲ࠪᗚ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack111111l111_opy_(self, target: object):
        return bstack1lllllll1l1_opy_.create_context(target) == self.context
    def bstack1l1lllllll1_opy_(self, context: bstack1llllllll11_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll11lll11_opy_(self, key: str, value: timedelta):
        self.data[bstack1lllllll1l1_opy_.bstack11llll11lll_opy_][key] += value
    def bstack1ll1ll11l11_opy_(self) -> dict:
        return self.data[bstack1lllllll1l1_opy_.bstack11llll11lll_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1llllllll11_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )