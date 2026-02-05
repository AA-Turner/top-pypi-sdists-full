# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1lll1lll11l_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1lll1l1l111_opy_:
    bstack11ll111ll11_opy_ = bstack11l1ll1_opy_ (u"ࠤࡥࡩࡳࡩࡨ࡮ࡣࡵ࡯ࠧᛳ")
    context: bstack1lll1lll11l_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1lll1lll11l_opy_):
        self.context = context
        self.data = dict({bstack1lll1l1l111_opy_.bstack11ll111ll11_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᛴ"), bstack11l1ll1_opy_ (u"ࠫ࠵࠭ᛵ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1lll11l111l_opy_(self, target: object):
        return bstack1lll1l1l111_opy_.create_context(target) == self.context
    def bstack1l1l1l11111_opy_(self, context: bstack1lll1lll11l_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll1l11l_opy_(self, key: str, value: timedelta):
        self.data[bstack1lll1l1l111_opy_.bstack11ll111ll11_opy_][key] += value
    def bstack1ll1ll11ll1_opy_(self) -> dict:
        return self.data[bstack1lll1l1l111_opy_.bstack11ll111ll11_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1lll1lll11l_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )