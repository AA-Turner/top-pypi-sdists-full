# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack11l1l1ll1_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1l1111l1l_opy_:
    pass
class bstack1lllllll1_opy_:
    bstack111l11ll_opy_ = bstack11l1l11_opy_ (u"ࠤࡥࡳࡴࡺࡳࡵࡴࡤࡴࠧዒ")
    CONNECT = bstack11l1l11_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦዓ")
    bstack1l111l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠦࡸ࡮ࡵࡵࡦࡲࡻࡳࠨዔ")
    CONFIG = bstack11l1l11_opy_ (u"ࠧࡩ࡯࡯ࡨ࡬࡫ࠧዕ")
    bstack1l1lll11l1l_opy_ = bstack11l1l11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡵࠥዖ")
    bstack1l1111ll1l_opy_ = bstack11l1l11_opy_ (u"ࠢࡦࡺ࡬ࡸࠧ዗")
class bstack1l1ll1llll1_opy_:
    bstack1l1lll111ll_opy_ = bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣዘ")
    FINISHED = bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥዙ")
class bstack1l1lll11111_opy_:
    bstack1l1lll111ll_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡹࡴࡢࡴࡷࡩࡩࠨዚ")
    FINISHED = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣዛ")
class bstack1l1lll1111l_opy_:
    bstack1l1lll111ll_opy_ = bstack11l1l11_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣዜ")
    FINISHED = bstack11l1l11_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥዝ")
class bstack1l1lll111l1_opy_:
    bstack1l1lll11l11_opy_ = bstack11l1l11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨዞ")
class bstack1l1ll1lllll_opy_:
    _1ll1l11l111_opy_ = None
    def __new__(cls):
        if not cls._1ll1l11l111_opy_:
            cls._1ll1l11l111_opy_ = super(bstack1l1ll1lllll_opy_, cls).__new__(cls)
        return cls._1ll1l11l111_opy_
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
                raise ValueError(bstack11l1l11_opy_ (u"ࠣࡅࡤࡰࡱࡨࡡࡤ࡭ࠣࡱࡺࡹࡴࠡࡤࡨࠤࡨࡧ࡬࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࠦዟ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡕࡩ࡬࡯ࡳࡵࡧࡵ࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤዠ") + str(pid) + bstack11l1l11_opy_ (u"ࠥࠦዡ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠦࡓࡵࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥዢ") + str(pid) + bstack11l1l11_opy_ (u"ࠧࠨዣ"))
                return
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡉ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽ࡯ࡩࡳ࠮ࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠫࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢዤ") + str(pid) + bstack11l1l11_opy_ (u"ࠢࠣዥ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡋࡱࡺࡴࡱࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦዦ") + str(pid) + bstack11l1l11_opy_ (u"ࠤࠥዧ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࢁࡰࡪࡦࢀ࠾ࠥࠨየ") + str(e) + bstack11l1l11_opy_ (u"ࠦࠧዩ"))
                    traceback.print_exc()
bstack11l1l1l11_opy_ = bstack1l1ll1lllll_opy_()