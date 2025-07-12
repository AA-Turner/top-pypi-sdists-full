# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1l1ll111_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack11lll1l1l_opy_:
    pass
class bstack11l1ll1ll_opy_:
    bstack11ll1l1ll1_opy_ = bstack11l1111_opy_ (u"ࠣࡤࡲࡳࡹࡹࡴࡳࡣࡳࠦᔖ")
    CONNECT = bstack11l1111_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥᔗ")
    bstack1ll11l1l_opy_ = bstack11l1111_opy_ (u"ࠥࡷ࡭ࡻࡴࡥࡱࡺࡲࠧᔘ")
    CONFIG = bstack11l1111_opy_ (u"ࠦࡨࡵ࡮ࡧ࡫ࡪࠦᔙ")
    bstack1l1111l1l11_opy_ = bstack11l1111_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡴࠤᔚ")
    bstack1ll11ll1l_opy_ = bstack11l1111_opy_ (u"ࠨࡥࡹ࡫ࡷࠦᔛ")
class bstack1l1111l11ll_opy_:
    bstack1l11111llll_opy_ = bstack11l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡳࡵࡣࡵࡸࡪࡪࠢᔜ")
    FINISHED = bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᔝ")
class bstack1l1111l111l_opy_:
    bstack1l11111llll_opy_ = bstack11l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡸࡺࡡࡳࡶࡨࡨࠧᔞ")
    FINISHED = bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᔟ")
class bstack1l1111l1ll1_opy_:
    bstack1l11111llll_opy_ = bstack11l1111_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡳࡵࡣࡵࡸࡪࡪࠢᔠ")
    FINISHED = bstack11l1111_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᔡ")
class bstack1l1111l11l1_opy_:
    bstack1l1111l1111_opy_ = bstack11l1111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧᔢ")
class bstack1l1111l1l1l_opy_:
    _1l111l111ll_opy_ = None
    def __new__(cls):
        if not cls._1l111l111ll_opy_:
            cls._1l111l111ll_opy_ = super(bstack1l1111l1l1l_opy_, cls).__new__(cls)
        return cls._1l111l111ll_opy_
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
                raise ValueError(bstack11l1111_opy_ (u"ࠢࡄࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡰࡹࡸࡺࠠࡣࡧࠣࡧࡦࡲ࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࠥᔣ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack11l1111_opy_ (u"ࠣࡔࡨ࡫࡮ࡹࡴࡦࡴ࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣᔤ") + str(pid) + bstack11l1111_opy_ (u"ࠤࠥᔥ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack11l1111_opy_ (u"ࠥࡒࡴࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤᔦ") + str(pid) + bstack11l1111_opy_ (u"ࠦࠧᔧ"))
                return
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡏ࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡼ࡮ࡨࡲ࠭ࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠪࡿࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨᔨ") + str(pid) + bstack11l1111_opy_ (u"ࠨࠢᔩ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack11l1111_opy_ (u"ࠢࡊࡰࡹࡳࡰ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥᔪ") + str(pid) + bstack11l1111_opy_ (u"ࠣࠤᔫ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack11l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࢀࡶࡩࡥࡿ࠽ࠤࠧᔬ") + str(e) + bstack11l1111_opy_ (u"ࠥࠦᔭ"))
                    traceback.print_exc()
bstack111lllllll_opy_ = bstack1l1111l1l1l_opy_()