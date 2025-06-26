# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack11lllllll_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1111111ll_opy_:
    pass
class bstack1llllll1l1_opy_:
    bstack1l111ll1l_opy_ = bstack11ll1l1_opy_ (u"ࠣࡤࡲࡳࡹࡹࡴࡳࡣࡳࠦᄦ")
    CONNECT = bstack11ll1l1_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥᄧ")
    bstack11l1l1ll1l_opy_ = bstack11ll1l1_opy_ (u"ࠥࡷ࡭ࡻࡴࡥࡱࡺࡲࠧᄨ")
    CONFIG = bstack11ll1l1_opy_ (u"ࠦࡨࡵ࡮ࡧ࡫ࡪࠦᄩ")
    bstack1ll1l1l1ll1_opy_ = bstack11ll1l1_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡴࠤᄪ")
    bstack11l1ll11l_opy_ = bstack11ll1l1_opy_ (u"ࠨࡥࡹ࡫ࡷࠦᄫ")
class bstack1ll1l1ll11l_opy_:
    bstack1ll1l1l1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡳࡵࡣࡵࡸࡪࡪࠢᄬ")
    FINISHED = bstack11ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᄭ")
class bstack1ll1l1ll111_opy_:
    bstack1ll1l1l1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡸࡺࡡࡳࡶࡨࡨࠧᄮ")
    FINISHED = bstack11ll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᄯ")
class bstack1ll1l1l1lll_opy_:
    bstack1ll1l1l1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡳࡵࡣࡵࡸࡪࡪࠢᄰ")
    FINISHED = bstack11ll1l1_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᄱ")
class bstack1ll1l1l1l11_opy_:
    bstack1ll1l1l11ll_opy_ = bstack11ll1l1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧᄲ")
class bstack1ll1l1l11l1_opy_:
    _1llll11l1l1_opy_ = None
    def __new__(cls):
        if not cls._1llll11l1l1_opy_:
            cls._1llll11l1l1_opy_ = super(bstack1ll1l1l11l1_opy_, cls).__new__(cls)
        return cls._1llll11l1l1_opy_
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
                raise ValueError(bstack11ll1l1_opy_ (u"ࠢࡄࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡰࡹࡸࡺࠠࡣࡧࠣࡧࡦࡲ࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࠥᄳ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡔࡨ࡫࡮ࡹࡴࡦࡴ࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣᄴ") + str(pid) + bstack11ll1l1_opy_ (u"ࠤࠥᄵ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠥࡒࡴࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤᄶ") + str(pid) + bstack11ll1l1_opy_ (u"ࠦࠧᄷ"))
                return
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡏ࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡼ࡮ࡨࡲ࠭ࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠪࡿࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨᄸ") + str(pid) + bstack11ll1l1_opy_ (u"ࠨࠢᄹ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡊࡰࡹࡳࡰ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥᄺ") + str(pid) + bstack11ll1l1_opy_ (u"ࠣࠤᄻ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack11ll1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࢀࡶࡩࡥࡿ࠽ࠤࠧᄼ") + str(e) + bstack11ll1l1_opy_ (u"ࠥࠦᄽ"))
                    traceback.print_exc()
bstack11l11lll1l_opy_ = bstack1ll1l1l11l1_opy_()