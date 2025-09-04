# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack11l1lll1l_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack11l11l11l1_opy_:
    pass
class bstack1l111l1111_opy_:
    bstack11l11ll1ll_opy_ = bstack1111l1l_opy_ (u"ࠢࡣࡱࡲࡸࡸࡺࡲࡢࡲࠥᅫ")
    CONNECT = bstack1111l1l_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤᅬ")
    bstack1l11111ll1_opy_ = bstack1111l1l_opy_ (u"ࠤࡶ࡬ࡺࡺࡤࡰࡹࡱࠦᅭ")
    CONFIG = bstack1111l1l_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥᅮ")
    bstack1ll1l11l1l1_opy_ = bstack1111l1l_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡳࠣᅯ")
    bstack1l11111l_opy_ = bstack1111l1l_opy_ (u"ࠧ࡫ࡸࡪࡶࠥᅰ")
class bstack1ll1l11l1ll_opy_:
    bstack1ll1l11ll11_opy_ = bstack1111l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡹࡴࡢࡴࡷࡩࡩࠨᅱ")
    FINISHED = bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᅲ")
class bstack1ll1l11llll_opy_:
    bstack1ll1l11ll11_opy_ = bstack1111l1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡷࡹࡧࡲࡵࡧࡧࠦᅳ")
    FINISHED = bstack1111l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᅴ")
class bstack1ll1l11ll1l_opy_:
    bstack1ll1l11ll11_opy_ = bstack1111l1l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡹࡴࡢࡴࡷࡩࡩࠨᅵ")
    FINISHED = bstack1111l1l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᅶ")
class bstack1ll1l11lll1_opy_:
    bstack1ll1l1l111l_opy_ = bstack1111l1l_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦᅷ")
class bstack1ll1l1l1111_opy_:
    _1lll11l11l1_opy_ = None
    def __new__(cls):
        if not cls._1lll11l11l1_opy_:
            cls._1lll11l11l1_opy_ = super(bstack1ll1l1l1111_opy_, cls).__new__(cls)
        return cls._1lll11l11l1_opy_
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
                raise ValueError(bstack1111l1l_opy_ (u"ࠨࡃࡢ࡮࡯ࡦࡦࡩ࡫ࠡ࡯ࡸࡷࡹࠦࡢࡦࠢࡦࡥࡱࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࠤᅸ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡓࡧࡪ࡭ࡸࡺࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢᅹ") + str(pid) + bstack1111l1l_opy_ (u"ࠣࠤᅺ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1111l1l_opy_ (u"ࠤࡑࡳࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣᅻ") + str(pid) + bstack1111l1l_opy_ (u"ࠥࠦᅼ"))
                return
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡎࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠩࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᅽ") + str(pid) + bstack1111l1l_opy_ (u"ࠧࠨᅾ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡉ࡯ࡸࡲ࡯ࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤᅿ") + str(pid) + bstack1111l1l_opy_ (u"ࠢࠣᆀ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1111l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࡿࡵ࡯ࡤࡾ࠼ࠣࠦᆁ") + str(e) + bstack1111l1l_opy_ (u"ࠤࠥᆂ"))
                    traceback.print_exc()
bstack11lllll1ll_opy_ = bstack1ll1l1l1111_opy_()