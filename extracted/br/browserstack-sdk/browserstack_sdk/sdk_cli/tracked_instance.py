# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import threading
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1l11ll1l1l1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class TrackedInstance:
    bstack111l111l11l_opy_ = bstack1l1llll_opy_ (u"ࠧࡨࡥ࡯ࡥ࡫ࡱࡦࡸ࡫ࠣḋ")
    context: bstack1l11ll1l1l1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1l11ll1l1l1_opy_):
        self.context = context
        self.data = dict({TrackedInstance.bstack111l111l11l_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ḍ"), bstack1l1llll_opy_ (u"ࠧ࠱ࠩḍ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1l11ll111l1_opy_(self, target: object):
        return TrackedInstance.create_context(target) == self.context
    def bstack11l1lll1l1l_opy_(self, context: bstack1l11ll1l1l1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def add_benchmark(self, key: str, value: timedelta):
        self.data[TrackedInstance.bstack111l111l11l_opy_][key] += value
    def bstack1l1111l11l1_opy_(self) -> dict:
        return self.data[TrackedInstance.bstack111l111l11l_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=None,
        process_id=None,
    ):
        return bstack1l11ll1l1l1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id if thread_id is not None else threading.get_ident(),
            process_id=process_id if process_id is not None else os.getpid(),
            type=target,
        )