# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1111l1l11_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1ll1l1l1ll_opy_:
    pass
class bstack11ll11l1l_opy_:
    bstack1llll1l1l_opy_ = bstack1l11l11_opy_ (u"ࠥࡦࡴࡵࡴࡴࡶࡵࡥࡵࠨᅠ")
    CONNECT = bstack1l11l11_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᅡ")
    bstack1lll1l1l1_opy_ = bstack1l11l11_opy_ (u"ࠧࡹࡨࡶࡶࡧࡳࡼࡴࠢᅢ")
    CONFIG = bstack1l11l11_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨᅣ")
    bstack1ll1l11ll1l_opy_ = bstack1l11l11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡶࠦᅤ")
    bstack11lll11l_opy_ = bstack1l11l11_opy_ (u"ࠣࡧࡻ࡭ࡹࠨᅥ")
class bstack1ll1l1l1l11_opy_:
    bstack1ll1l1l11l1_opy_ = bstack1l11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡵࡷࡥࡷࡺࡥࡥࠤᅦ")
    FINISHED = bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᅧ")
class bstack1ll1l11llll_opy_:
    bstack1ll1l1l11l1_opy_ = bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡳࡵࡣࡵࡸࡪࡪࠢᅨ")
    FINISHED = bstack1l11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᅩ")
class bstack1ll1l1l1111_opy_:
    bstack1ll1l1l11l1_opy_ = bstack1l11l11_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡵࡷࡥࡷࡺࡥࡥࠤᅪ")
    FINISHED = bstack1l11l11_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᅫ")
class bstack1ll1l11lll1_opy_:
    bstack1ll1l1l11ll_opy_ = bstack1l11l11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢᅬ")
class bstack1ll1l1l111l_opy_:
    _1lll11ll1l1_opy_ = None
    def __new__(cls):
        if not cls._1lll11ll1l1_opy_:
            cls._1lll11ll1l1_opy_ = super(bstack1ll1l1l111l_opy_, cls).__new__(cls)
        return cls._1lll11ll1l1_opy_
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
                raise ValueError(bstack1l11l11_opy_ (u"ࠤࡆࡥࡱࡲࡢࡢࡥ࡮ࠤࡲࡻࡳࡵࠢࡥࡩࠥࡩࡡ࡭࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࠧᅭ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1l11l11_opy_ (u"ࠥࡖࡪ࡭ࡩࡴࡶࡨࡶ࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥᅮ") + str(pid) + bstack1l11l11_opy_ (u"ࠦࠧᅯ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1l11l11_opy_ (u"ࠧࡔ࡯ࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦᅰ") + str(pid) + bstack1l11l11_opy_ (u"ࠨࠢᅱ"))
                return
            self.logger.debug(bstack1l11l11_opy_ (u"ࠢࡊࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࡰࡪࡴࠨࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠬࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣᅲ") + str(pid) + bstack1l11l11_opy_ (u"ࠣࠤᅳ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡌࡲࡻࡵ࡫ࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᅴ") + str(pid) + bstack1l11l11_opy_ (u"ࠥࠦᅵ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1l11l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࡻࡱ࡫ࡧࢁ࠿ࠦࠢᅶ") + str(e) + bstack1l11l11_opy_ (u"ࠧࠨᅷ"))
                    traceback.print_exc()
bstack1llll1lll_opy_ = bstack1ll1l1l111l_opy_()