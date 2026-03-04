# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1ll1l1l1l1_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1l1l111l11_opy_:
    pass
class bstack1111ll11_opy_:
    bstack1ll1lll1l_opy_ = bstack1lll1l_opy_ (u"ࠢࡣࡱࡲࡸࡸࡺࡲࡢࡲࠥ፜")
    CONNECT = bstack1lll1l_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤ፝")
    bstack1ll11l111l_opy_ = bstack1lll1l_opy_ (u"ࠤࡶ࡬ࡺࡺࡤࡰࡹࡱࠦ፞")
    CONFIG = bstack1lll1l_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥ፟")
    bstack1l1ll1l111l_opy_ = bstack1lll1l_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡳࠣ፠")
    bstack1lll1l1l1_opy_ = bstack1lll1l_opy_ (u"ࠧ࡫ࡸࡪࡶࠥ፡")
class bstack1l1ll11llll_opy_:
    bstack1l1ll11ll1l_opy_ = bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡹࡴࡢࡴࡷࡩࡩࠨ።")
    FINISHED = bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣ፣")
class bstack1l1ll11l1l1_opy_:
    bstack1l1ll11ll1l_opy_ = bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡷࡹࡧࡲࡵࡧࡧࠦ፤")
    FINISHED = bstack1lll1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨ፥")
class bstack1l1ll1l1111_opy_:
    bstack1l1ll11ll1l_opy_ = bstack1lll1l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡹࡴࡢࡴࡷࡩࡩࠨ፦")
    FINISHED = bstack1lll1l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣ፧")
class bstack1l1ll11ll11_opy_:
    bstack1l1ll11l1ll_opy_ = bstack1lll1l_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦ፨")
class bstack1l1ll11lll1_opy_:
    _1l1llll111l_opy_ = None
    def __new__(cls):
        if not cls._1l1llll111l_opy_:
            cls._1l1llll111l_opy_ = super(bstack1l1ll11lll1_opy_, cls).__new__(cls)
        return cls._1l1llll111l_opy_
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
                raise ValueError(bstack1lll1l_opy_ (u"ࠨࡃࡢ࡮࡯ࡦࡦࡩ࡫ࠡ࡯ࡸࡷࡹࠦࡢࡦࠢࡦࡥࡱࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࠤ፩") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡓࡧࡪ࡭ࡸࡺࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࠢ፪") + str(pid) + bstack1lll1l_opy_ (u"ࠣࠤ፫"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1lll1l_opy_ (u"ࠤࡑࡳࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣ፬") + str(pid) + bstack1lll1l_opy_ (u"ࠥࠦ፭"))
                return
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡎࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠩࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧ፮") + str(pid) + bstack1lll1l_opy_ (u"ࠧࠨ፯"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡉ࡯ࡸࡲ࡯ࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤ፰") + str(pid) + bstack1lll1l_opy_ (u"ࠢࠣ፱"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1lll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࡿࡵ࡯ࡤࡾ࠼ࠣࠦ፲") + str(e) + bstack1lll1l_opy_ (u"ࠤࠥ፳"))
                    traceback.print_exc()
bstack1l11lll1_opy_ = bstack1l1ll11lll1_opy_()