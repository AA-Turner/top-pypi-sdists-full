# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1ll1ll11l11_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1ll1llll1l1_opy_:
    bstack11l1l111111_opy_ = bstack1111_opy_ (u"ࠨࡢࡦࡰࡦ࡬ࡲࡧࡲ࡬ࠤᣯ")
    context: bstack1ll1ll11l11_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1ll1ll11l11_opy_):
        self.context = context
        self.data = dict({bstack1ll1llll1l1_opy_.bstack11l1l111111_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᣰ"), bstack1111_opy_ (u"ࠨ࠲ࠪᣱ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1ll1l1l1l11_opy_(self, target: object):
        return bstack1ll1llll1l1_opy_.create_context(target) == self.context
    def bstack1l11lll1l1l_opy_(self, context: bstack1ll1ll11l11_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack11ll1llll_opy_(self, key: str, value: timedelta):
        self.data[bstack1ll1llll1l1_opy_.bstack11l1l111111_opy_][key] += value
    def bstack1ll11111ll1_opy_(self) -> dict:
        return self.data[bstack1ll1llll1l1_opy_.bstack11l1l111111_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1ll1ll11l11_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )