# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1l111111l_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1ll1111l1_opy_:
    pass
class bstack1l11lll111_opy_:
    bstack11lll11l_opy_ = bstack1l11ll1_opy_ (u"ࠧࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠣᅩ")
    CONNECT = bstack1l11ll1_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢᅪ")
    bstack1l1111ll_opy_ = bstack1l11ll1_opy_ (u"ࠢࡴࡪࡸࡸࡩࡵࡷ࡯ࠤᅫ")
    CONFIG = bstack1l11ll1_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᅬ")
    bstack1ll1l11ll11_opy_ = bstack1l11ll1_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡸࠨᅭ")
    bstack1l11ll11_opy_ = bstack1l11ll1_opy_ (u"ࠥࡩࡽ࡯ࡴࠣᅮ")
class bstack1ll1l11llll_opy_:
    bstack1ll1l11ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡷࡹࡧࡲࡵࡧࡧࠦᅯ")
    FINISHED = bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᅰ")
class bstack1ll1l11lll1_opy_:
    bstack1ll1l11ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡵࡷࡥࡷࡺࡥࡥࠤᅱ")
    FINISHED = bstack1l11ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᅲ")
class bstack1ll1l11l1l1_opy_:
    bstack1ll1l11ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡶࡰࡢࡷࡹࡧࡲࡵࡧࡧࠦᅳ")
    FINISHED = bstack1l11ll1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᅴ")
class bstack1ll1l11l11l_opy_:
    bstack1ll1l1l1111_opy_ = bstack1l11ll1_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤᅵ")
class bstack1ll1l11l1ll_opy_:
    _1ll1llllll1_opy_ = None
    def __new__(cls):
        if not cls._1ll1llllll1_opy_:
            cls._1ll1llllll1_opy_ = super(bstack1ll1l11l1ll_opy_, cls).__new__(cls)
        return cls._1ll1llllll1_opy_
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
                raise ValueError(bstack1l11ll1_opy_ (u"ࠦࡈࡧ࡬࡭ࡤࡤࡧࡰࠦ࡭ࡶࡵࡷࠤࡧ࡫ࠠࡤࡣ࡯ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࠢᅶ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡘࡥࡨ࡫ࡶࡸࡪࡸࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᅷ") + str(pid) + bstack1l11ll1_opy_ (u"ࠨࠢᅸ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠢࡏࡱࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨᅹ") + str(pid) + bstack1l11ll1_opy_ (u"ࠣࠤᅺ"))
                return
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡌࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࡲࡥ࡯ࠪࡦࡥࡱࡲࡢࡢࡥ࡮ࡷ࠮ࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥᅻ") + str(pid) + bstack1l11ll1_opy_ (u"ࠥࠦᅼ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡎࡴࡶࡰ࡭ࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢᅽ") + str(pid) + bstack1l11ll1_opy_ (u"ࠧࠨᅾ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1l11ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࡽࡳ࡭ࡩࢃ࠺ࠡࠤᅿ") + str(e) + bstack1l11ll1_opy_ (u"ࠢࠣᆀ"))
                    traceback.print_exc()
bstack1l1111l1_opy_ = bstack1ll1l11l1ll_opy_()