# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1lllll1l1l1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1lllll11l11_opy_:
    bstack11llll1l1ll_opy_ = bstack1l1ll1_opy_ (u"ࠨࡢࡦࡰࡦ࡬ࡲࡧࡲ࡬ࠤᖙ")
    context: bstack1lllll1l1l1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1lllll1l1l1_opy_):
        self.context = context
        self.data = dict({bstack1lllll11l11_opy_.bstack11llll1l1ll_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᖚ"), bstack1l1ll1_opy_ (u"ࠨ࠲ࠪᖛ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack11111111l1_opy_(self, target: object):
        return bstack1lllll11l11_opy_.create_context(target) == self.context
    def bstack1ll11111l11_opy_(self, context: bstack1lllll1l1l1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack11l1l1111l_opy_(self, key: str, value: timedelta):
        self.data[bstack1lllll11l11_opy_.bstack11llll1l1ll_opy_][key] += value
    def bstack1lll1l111ll_opy_(self) -> dict:
        return self.data[bstack1lllll11l11_opy_.bstack11llll1l1ll_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1lllll1l1l1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )