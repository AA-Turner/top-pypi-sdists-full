# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack11llllllll_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack11l111lll_opy_:
    pass
class bstack11ll1111ll_opy_:
    bstack1ll111l1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠤࡥࡳࡴࡺࡳࡵࡴࡤࡴࠧᅦ")
    CONNECT = bstack1l1l1ll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᅧ")
    bstack1ll1l1lll1_opy_ = bstack1l1l1ll_opy_ (u"ࠦࡸ࡮ࡵࡵࡦࡲࡻࡳࠨᅨ")
    CONFIG = bstack1l1l1ll_opy_ (u"ࠧࡩ࡯࡯ࡨ࡬࡫ࠧᅩ")
    bstack1ll1l1l1l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡵࠥᅪ")
    bstack1ll111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡦࡺ࡬ࡸࠧᅫ")
class bstack1ll1l1l111l_opy_:
    bstack1ll1l1l11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᅬ")
    FINISHED = bstack1l1l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᅭ")
class bstack1ll1l11llll_opy_:
    bstack1ll1l1l11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡹࡴࡢࡴࡷࡩࡩࠨᅮ")
    FINISHED = bstack1l1l1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᅯ")
class bstack1ll1l1l1111_opy_:
    bstack1ll1l1l11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᅰ")
    FINISHED = bstack1l1l1ll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᅱ")
class bstack1ll1l1l1ll1_opy_:
    bstack1ll1l1l11l1_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨᅲ")
class bstack1ll1l1l1l11_opy_:
    _1llll11ll11_opy_ = None
    def __new__(cls):
        if not cls._1llll11ll11_opy_:
            cls._1llll11ll11_opy_ = super(bstack1ll1l1l1l11_opy_, cls).__new__(cls)
        return cls._1llll11ll11_opy_
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
                raise ValueError(bstack1l1l1ll_opy_ (u"ࠣࡅࡤࡰࡱࡨࡡࡤ࡭ࠣࡱࡺࡹࡴࠡࡤࡨࠤࡨࡧ࡬࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࠦᅳ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡕࡩ࡬࡯ࡳࡵࡧࡵ࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤᅴ") + str(pid) + bstack1l1l1ll_opy_ (u"ࠥࠦᅵ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1l1l1ll_opy_ (u"ࠦࡓࡵࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥᅶ") + str(pid) + bstack1l1l1ll_opy_ (u"ࠧࠨᅷ"))
                return
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡉ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽ࡯ࡩࡳ࠮ࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠫࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢᅸ") + str(pid) + bstack1l1l1ll_opy_ (u"ࠢࠣᅹ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡋࡱࡺࡴࡱࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦᅺ") + str(pid) + bstack1l1l1ll_opy_ (u"ࠤࠥᅻ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1l1l1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࢁࡰࡪࡦࢀ࠾ࠥࠨᅼ") + str(e) + bstack1l1l1ll_opy_ (u"ࠦࠧᅽ"))
                    traceback.print_exc()
bstack1111lll11_opy_ = bstack1ll1l1l1l11_opy_()