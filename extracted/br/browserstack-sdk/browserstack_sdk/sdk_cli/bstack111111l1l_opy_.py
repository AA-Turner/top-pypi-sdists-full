# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1ll111lll1_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1ll1ll1l_opy_:
    pass
class Events:
    bstack1l11ll1l_opy_ = bstack1ll1l11_opy_ (u"ࠦࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠢᕻ")
    CONNECT = bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨᕼ")
    bstack1111ll11_opy_ = bstack1ll1l11_opy_ (u"ࠨࡳࡩࡷࡷࡨࡴࡽ࡮ࠣᕽ")
    CONFIG = bstack1ll1l11_opy_ (u"ࠢࡤࡱࡱࡪ࡮࡭ࠢᕾ")
    bstack1l111ll1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡷࠧᕿ")
    bstack1l11l1lll1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡨࡼ࡮ࡺࠢᖀ")
class bstack1l111lll1l1_opy_:
    bstack1l111ll1lll_opy_ = bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡶࡸࡦࡸࡴࡦࡦࠥᖁ")
    FINISHED = bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᖂ")
class bstack1l111lll1ll_opy_:
    bstack1l111ll1lll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᖃ")
    FINISHED = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᖄ")
class bstack1l111lll111_opy_:
    bstack1l111ll1lll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡶࡸࡦࡸࡴࡦࡦࠥᖅ")
    FINISHED = bstack1ll1l11_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡶࡰࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᖆ")
class bstack1l111llll11_opy_:
    bstack1l111llll1l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣᖇ")
class bstack1l111lll11l_opy_:
    _1ll11111111_opy_ = None
    def __new__(cls):
        if not cls._1ll11111111_opy_:
            cls._1ll11111111_opy_ = super(bstack1l111lll11l_opy_, cls).__new__(cls)
        return cls._1ll11111111_opy_
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
                raise ValueError(bstack1ll1l11_opy_ (u"ࠥࡇࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡳࡵࡴࡶࠣࡦࡪࠦࡣࡢ࡮࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࠨᖈ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡗ࡫ࡧࡪࡵࡷࡩࡷ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦᖉ") + str(pid) + bstack1ll1l11_opy_ (u"ࠧࠨᖊ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡎࡰࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᖋ") + str(pid) + bstack1ll1l11_opy_ (u"ࠢࠣᖌ"))
                return
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡋࡱࡺࡴࡱࡩ࡯ࡩࠣࡿࡱ࡫࡮ࠩࡥࡤࡰࡱࡨࡡࡤ࡭ࡶ࠭ࢂࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤᖍ") + str(pid) + bstack1ll1l11_opy_ (u"ࠤࠥᖎ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡍࡳࡼ࡯࡬ࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨᖏ") + str(pid) + bstack1ll1l11_opy_ (u"ࠦࠧᖐ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࡼࡲ࡬ࡨࢂࡀࠠࠣᖑ") + str(e) + bstack1ll1l11_opy_ (u"ࠨࠢᖒ"))
                    traceback.print_exc()
bstack111111l1l_opy_ = bstack1l111lll11l_opy_()