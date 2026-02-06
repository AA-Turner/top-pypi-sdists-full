# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack11l11l1111_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1llllll111_opy_:
    pass
class bstack1lll11l1l_opy_:
    bstack1l11ll11l1_opy_ = bstack11lllll_opy_ (u"ࠣࡤࡲࡳࡹࡹࡴࡳࡣࡳࠦቅ")
    CONNECT = bstack11lllll_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥቆ")
    bstack11l1l11l1_opy_ = bstack11lllll_opy_ (u"ࠥࡷ࡭ࡻࡴࡥࡱࡺࡲࠧቇ")
    CONFIG = bstack11lllll_opy_ (u"ࠦࡨࡵ࡮ࡧ࡫ࡪࠦቈ")
    bstack1l1llll1l1l_opy_ = bstack11lllll_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡴࠤ቉")
    bstack11ll1111_opy_ = bstack11lllll_opy_ (u"ࠨࡥࡹ࡫ࡷࠦቊ")
class bstack1l1llll1111_opy_:
    bstack1l1llll11ll_opy_ = bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡳࡵࡣࡵࡸࡪࡪࠢቋ")
    FINISHED = bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤቌ")
class bstack1l1lll1llll_opy_:
    bstack1l1llll11ll_opy_ = bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡸࡺࡡࡳࡶࡨࡨࠧቍ")
    FINISHED = bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢ቎")
class bstack1l1lll1lll1_opy_:
    bstack1l1llll11ll_opy_ = bstack11lllll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡳࡵࡣࡵࡸࡪࡪࠢ቏")
    FINISHED = bstack11lllll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤቐ")
class bstack1l1llll11l1_opy_:
    bstack1l1llll1l11_opy_ = bstack11lllll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧቑ")
class bstack1l1llll111l_opy_:
    _1ll11llll1l_opy_ = None
    def __new__(cls):
        if not cls._1ll11llll1l_opy_:
            cls._1ll11llll1l_opy_ = super(bstack1l1llll111l_opy_, cls).__new__(cls)
        return cls._1ll11llll1l_opy_
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
                raise ValueError(bstack11lllll_opy_ (u"ࠢࡄࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡰࡹࡸࡺࠠࡣࡧࠣࡧࡦࡲ࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࠥቒ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack11lllll_opy_ (u"ࠣࡔࡨ࡫࡮ࡹࡴࡦࡴ࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣቓ") + str(pid) + bstack11lllll_opy_ (u"ࠤࠥቔ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack11lllll_opy_ (u"ࠥࡒࡴࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤቕ") + str(pid) + bstack11lllll_opy_ (u"ࠦࠧቖ"))
                return
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡏ࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡼ࡮ࡨࡲ࠭ࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠪࡿࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨ቗") + str(pid) + bstack11lllll_opy_ (u"ࠨࠢቘ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack11lllll_opy_ (u"ࠢࡊࡰࡹࡳࡰ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥ቙") + str(pid) + bstack11lllll_opy_ (u"ࠣࠤቚ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࢀࡶࡩࡥࡿ࠽ࠤࠧቛ") + str(e) + bstack11lllll_opy_ (u"ࠥࠦቜ"))
                    traceback.print_exc()
bstack11l1ll1l_opy_ = bstack1l1llll111l_opy_()