# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack11l111l11_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1l11l111ll_opy_:
    pass
class Events:
    bstack11111l11l_opy_ = bstack111l_opy_ (u"ࠧࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠣᘏ")
    CONNECT = bstack111l_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢᘐ")
    bstack1l1ll1l111_opy_ = bstack111l_opy_ (u"ࠢࡴࡪࡸࡸࡩࡵࡷ࡯ࠤᘑ")
    CONFIG = bstack111l_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᘒ")
    bstack11lllll11l1_opy_ = bstack111l_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡸࠨᘓ")
    bstack11ll1l11l1_opy_ = bstack111l_opy_ (u"ࠥࡩࡽ࡯ࡴࠣᘔ")
class bstack11llllll11l_opy_:
    bstack11llllll111_opy_ = bstack111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡷࡹࡧࡲࡵࡧࡧࠦᘕ")
    FINISHED = bstack111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᘖ")
class bstack11lllll1lll_opy_:
    bstack11llllll111_opy_ = bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡵࡷࡥࡷࡺࡥࡥࠤᘗ")
    FINISHED = bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᘘ")
class bstack11lllll1ll1_opy_:
    bstack11llllll111_opy_ = bstack111l_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡶࡰࡢࡷࡹࡧࡲࡵࡧࡧࠦᘙ")
    FINISHED = bstack111l_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᘚ")
class bstack11lllll1l11_opy_:
    bstack11lllll1l1l_opy_ = bstack111l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤᘛ")
class bstack11lllll11ll_opy_:
    _1ll1111111l_opy_ = None
    def __new__(cls):
        if not cls._1ll1111111l_opy_:
            cls._1ll1111111l_opy_ = super(bstack11lllll11ll_opy_, cls).__new__(cls)
        return cls._1ll1111111l_opy_
    def __init__(self):
        self._hooks = defaultdict(lambda: defaultdict(list))
        self._lock = Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def clear(self):
        with self._lock:
            self._hooks = defaultdict(list)
    def register(self, event_name, callback):
        with self._lock:
            if not callable(callback):
                raise ValueError(bstack111l_opy_ (u"ࠦࡈࡧ࡬࡭ࡤࡤࡧࡰࠦ࡭ࡶࡵࡷࠤࡧ࡫ࠠࡤࡣ࡯ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࠢᘜ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack111l_opy_ (u"ࠧࡘࡥࡨ࡫ࡶࡸࡪࡸࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᘝ") + str(pid) + bstack111l_opy_ (u"ࠨࠢᘞ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack111l_opy_ (u"ࠢࡏࡱࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨᘟ") + str(pid) + bstack111l_opy_ (u"ࠣࠤᘠ"))
                return
            self.logger.debug(bstack111l_opy_ (u"ࠤࡌࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࡲࡥ࡯ࠪࡦࡥࡱࡲࡢࡢࡥ࡮ࡷ࠮ࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥᘡ") + str(pid) + bstack111l_opy_ (u"ࠥࠦᘢ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack111l_opy_ (u"ࠦࡎࡴࡶࡰ࡭ࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢᘣ") + str(pid) + bstack111l_opy_ (u"ࠧࠨᘤ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࡽࡳ࡭ࡩࢃ࠺ࠡࠤᘥ") + str(e) + bstack111l_opy_ (u"ࠢࠣᘦ"))
                    traceback.print_exc()
bstack111ll1111l_opy_ = bstack11lllll11ll_opy_()