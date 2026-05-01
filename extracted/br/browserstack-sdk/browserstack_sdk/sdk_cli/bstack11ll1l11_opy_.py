# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1l1l1lllll_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1ll11l1l11_opy_:
    pass
class Events:
    bstack1ll111l1_opy_ = bstack111ll_opy_ (u"ࠥࡦࡴࡵࡴࡴࡶࡵࡥࡵࠨᖤ")
    CONNECT = bstack111ll_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧᖥ")
    bstack1l111lll11_opy_ = bstack111ll_opy_ (u"ࠧࡹࡨࡶࡶࡧࡳࡼࡴࠢᖦ")
    CONFIG = bstack111ll_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨᖧ")
    bstack1l111ll11ll_opy_ = bstack111ll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡶࠦᖨ")
    bstack111ll1ll11_opy_ = bstack111ll_opy_ (u"ࠣࡧࡻ࡭ࡹࠨᖩ")
class bstack1l111l1llll_opy_:
    bstack1l111ll1l1l_opy_ = bstack111ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡵࡷࡥࡷࡺࡥࡥࠤᖪ")
    FINISHED = bstack111ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᖫ")
class bstack1l111ll1ll1_opy_:
    bstack1l111ll1l1l_opy_ = bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡳࡵࡣࡵࡸࡪࡪࠢᖬ")
    FINISHED = bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᖭ")
class bstack1l111ll1l11_opy_:
    bstack1l111ll1l1l_opy_ = bstack111ll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡵࡷࡥࡷࡺࡥࡥࠤᖮ")
    FINISHED = bstack111ll_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᖯ")
class bstack1l111ll11l1_opy_:
    bstack1l111ll111l_opy_ = bstack111ll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢᖰ")
class bstack1l111ll1111_opy_:
    _1l1llllllll_opy_ = None
    def __new__(cls):
        if not cls._1l1llllllll_opy_:
            cls._1l1llllllll_opy_ = super(bstack1l111ll1111_opy_, cls).__new__(cls)
        return cls._1l1llllllll_opy_
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
                raise ValueError(bstack111ll_opy_ (u"ࠤࡆࡥࡱࡲࡢࡢࡥ࡮ࠤࡲࡻࡳࡵࠢࡥࡩࠥࡩࡡ࡭࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࠧᖱ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡖࡪ࡭ࡩࡴࡶࡨࡶ࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥᖲ") + str(pid) + bstack111ll_opy_ (u"ࠦࠧᖳ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack111ll_opy_ (u"ࠧࡔ࡯ࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦᖴ") + str(pid) + bstack111ll_opy_ (u"ࠨࠢᖵ"))
                return
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡊࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࡰࡪࡴࠨࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠬࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣᖶ") + str(pid) + bstack111ll_opy_ (u"ࠣࠤᖷ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack111ll_opy_ (u"ࠤࡌࡲࡻࡵ࡫ࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᖸ") + str(pid) + bstack111ll_opy_ (u"ࠥࠦᖹ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࡻࡱ࡫ࡧࢁ࠿ࠦࠢᖺ") + str(e) + bstack111ll_opy_ (u"ࠧࠨᖻ"))
                    traceback.print_exc()
bstack11ll1l11_opy_ = bstack1l111ll1111_opy_()