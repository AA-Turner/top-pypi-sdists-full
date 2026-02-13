# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack11ll1lllll_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack111l1ll1l_opy_:
    pass
class bstack11ll111111_opy_:
    bstack1l1llllll1_opy_ = bstack11l11_opy_ (u"ࠨࡢࡰࡱࡷࡷࡹࡸࡡࡱࠤወ")
    CONNECT = bstack11l11_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣዉ")
    bstack11l1l111l1_opy_ = bstack11l11_opy_ (u"ࠣࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠥዊ")
    CONFIG = bstack11l11_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤዋ")
    bstack1l1ll1l1l1l_opy_ = bstack11l11_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡹࠢዌ")
    bstack111111l1l_opy_ = bstack11l11_opy_ (u"ࠦࡪࡾࡩࡵࠤው")
class bstack1l1ll1l11ll_opy_:
    bstack1l1ll1l11l1_opy_ = bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡸࡺࡡࡳࡶࡨࡨࠧዎ")
    FINISHED = bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢዏ")
class bstack1l1ll1l1111_opy_:
    bstack1l1ll1l11l1_opy_ = bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡶࡸࡦࡸࡴࡦࡦࠥዐ")
    FINISHED = bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧዑ")
class bstack1l1ll1l1l11_opy_:
    bstack1l1ll1l11l1_opy_ = bstack11l11_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡸࡺࡡࡳࡶࡨࡨࠧዒ")
    FINISHED = bstack11l11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢዓ")
class bstack1l1ll11llll_opy_:
    bstack1l1ll1l111l_opy_ = bstack11l11_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥዔ")
class bstack1l1ll1l1ll1_opy_:
    _1ll11111lll_opy_ = None
    def __new__(cls):
        if not cls._1ll11111lll_opy_:
            cls._1ll11111lll_opy_ = super(bstack1l1ll1l1ll1_opy_, cls).__new__(cls)
        return cls._1ll11111lll_opy_
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
                raise ValueError(bstack11l11_opy_ (u"ࠧࡉࡡ࡭࡮ࡥࡥࡨࡱࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡥࡤࡰࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࠣዕ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack11l11_opy_ (u"ࠨࡒࡦࡩ࡬ࡷࡹ࡫ࡲࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨዖ") + str(pid) + bstack11l11_opy_ (u"ࠢࠣ዗"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack11l11_opy_ (u"ࠣࡐࡲࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢዘ") + str(pid) + bstack11l11_opy_ (u"ࠤࠥዙ"))
                return
            self.logger.debug(bstack11l11_opy_ (u"ࠥࡍࡳࡼ࡯࡬࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸ࠯ࡽࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦዚ") + str(pid) + bstack11l11_opy_ (u"ࠦࠧዛ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack11l11_opy_ (u"ࠧࡏ࡮ࡷࡱ࡮ࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣዜ") + str(pid) + bstack11l11_opy_ (u"ࠨࠢዝ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࡾࡴ࡮ࡪࡽ࠻ࠢࠥዞ") + str(e) + bstack11l11_opy_ (u"ࠣࠤዟ"))
                    traceback.print_exc()
bstack1l11l11111_opy_ = bstack1l1ll1l1ll1_opy_()