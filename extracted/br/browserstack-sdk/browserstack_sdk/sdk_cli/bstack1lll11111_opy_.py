# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1lll11ll11_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1lll1111_opy_:
    pass
class Events:
    bstack11l1111l11_opy_ = bstack1ll111_opy_ (u"ࠢࡣࡱࡲࡸࡸࡺࡲࡢࡲࠥᏅ")
    CONNECT = bstack1ll111_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤᏆ")
    bstack111l11ll1l_opy_ = bstack1ll111_opy_ (u"ࠤࡶ࡬ࡺࡺࡤࡰࡹࡱࠦᏇ")
    CONFIG = bstack1ll111_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥᏈ")
    bstack1l1l1lll1l1_opy_ = bstack1ll111_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡳࠣᏉ")
    bstack1l111111ll_opy_ = bstack1ll111_opy_ (u"ࠧ࡫ࡸࡪࡶࠥᏊ")
class bstack1l1l1lll11l_opy_:
    bstack1l1l1ll1l11_opy_ = bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡹࡴࡢࡴࡷࡩࡩࠨᏋ")
    FINISHED = bstack1ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᏌ")
class bstack1l1l1ll1l1l_opy_:
    bstack1l1l1ll1l11_opy_ = bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡷࡹࡧࡲࡵࡧࡧࠦᏍ")
    FINISHED = bstack1ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᏎ")
class bstack1l1l1ll1lll_opy_:
    bstack1l1l1ll1l11_opy_ = bstack1ll111_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡹࡴࡢࡴࡷࡩࡩࠨᏏ")
    FINISHED = bstack1ll111_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᏐ")
class bstack1l1l1lll111_opy_:
    bstack1l1l1lll1ll_opy_ = bstack1ll111_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᏑ")
class bstack1l1l1ll1ll1_opy_:
    _1ll1111llll_opy_ = None
    def __new__(cls):
        if not cls._1ll1111llll_opy_:
            cls._1ll1111llll_opy_ = super(bstack1l1l1ll1ll1_opy_, cls).__new__(cls)
        return cls._1ll1111llll_opy_
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
                raise ValueError(bstack1ll111_opy_ (u"ࠨࡃࡢ࡮࡯ࡦࡦࡩ࡫ࠡ࡯ࡸࡷࡹࠦࡢࡦࠢࡦࡥࡱࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࠤᏒ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1ll111_opy_ (u"ࠢࡓࡧࡪ࡭ࡸࡺࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢᏓ") + str(pid) + bstack1ll111_opy_ (u"ࠣࠤᏔ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1ll111_opy_ (u"ࠤࡑࡳࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣᏕ") + str(pid) + bstack1ll111_opy_ (u"ࠥࠦᏖ"))
                return
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡎࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠩࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᏗ") + str(pid) + bstack1ll111_opy_ (u"ࠧࠨᏘ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1ll111_opy_ (u"ࠨࡉ࡯ࡸࡲ࡯ࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤᏙ") + str(pid) + bstack1ll111_opy_ (u"ࠢࠣᏚ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࡿࡵ࡯ࡤࡾ࠼ࠣࠦᏛ") + str(e) + bstack1ll111_opy_ (u"ࠤࠥᏜ"))
                    traceback.print_exc()
bstack1lll11111_opy_ = bstack1l1l1ll1ll1_opy_()