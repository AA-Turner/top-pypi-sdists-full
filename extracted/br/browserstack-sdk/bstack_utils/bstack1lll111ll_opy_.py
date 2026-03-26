# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack1l1111ll_opy_, bstack1111lllll11_opy_
from bstack_utils.helper import bstack1111l1l1l11_opy_, get_host_info
from bstack_utils.bstack111l1ll11ll_opy_ import bstack111l1ll11l1_opy_
import json
import re
import sys
bstack1llll11ll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡲࡦࡶࡵࡽ࡙࡫ࡳࡵࡵࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠧ⋿")
bstack1lll1lll11l1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨ⌀")
bstack1llll111ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡴࡸࡲࡕࡸࡥࡷ࡫ࡲࡹࡸࡲࡹࡇࡣ࡬ࡰࡪࡪࡆࡪࡴࡶࡸࠧ⌁")
bstack1llll1111ll1_opy_ = bstack1ll1lll_opy_ (u"ࠤࡵࡩࡷࡻ࡮ࡑࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡊࡦ࡯࡬ࡦࡦࠥ⌂")
bstack1llll11l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠥࡷࡰ࡯ࡰࡇ࡮ࡤ࡯ࡾࡧ࡮ࡥࡈࡤ࡭ࡱ࡫ࡤࠣ⌃")
bstack1llll11l1l11_opy_ = bstack1ll1lll_opy_ (u"ࠦࡷࡻ࡮ࡔ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠣ⌄")
bstack1llll111ll11_opy_ = {
    bstack1llll11ll1l1_opy_,
    bstack1lll1lll11l1_opy_,
    bstack1llll111ll1l_opy_,
    bstack1llll1111ll1_opy_,
    bstack1llll11l11l1_opy_,
    bstack1llll11l1l11_opy_
}
bstack1llll11l1ll1_opy_ = {bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⌅")}
logger = logger_utils.get_logger(__name__, bstack1l1111ll_opy_)
class bstack1llll111l11l_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lll1llll1l1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l111111l1_opy_:
    _1ll1l111ll1_opy_ = None
    def __init__(self, config):
        self.bstack1llll1l1l111_opy_ = False
        self.bstack1llll11lll1l_opy_ = False
        self.bstack1lll1llll111_opy_ = False
        self.bstack1llll11l1l1l_opy_ = False
        self.bstack1llll1111lll_opy_ = None
        self.bstack1llll1l11l1l_opy_ = bstack1llll111l11l_opy_()
        self.bstack1llll11111ll_opy_ = None
        opts = config.get(bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ⌆"), {})
        self.bstack1lll1llllll1_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠧࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࡇࡑ࡚ࠬ⌇"), bstack1ll1lll_opy_ (u"ࠣࠤ⌈"))
        self.bstack1llll1l11111_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠩࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡇࡑࡏࠧ⌉"), bstack1ll1lll_opy_ (u"ࠥࠦ⌊"))
        bstack1llll11lll11_opy_ = opts.get(bstack1llll11l1l11_opy_, {})
        bstack1llll1l11lll_opy_ = None
        if bstack1ll1lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ⌋") in bstack1llll11lll11_opy_:
            bstack1llll111l1ll_opy_ = bstack1llll11lll11_opy_[bstack1ll1lll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ⌌")]
            if bstack1llll111l1ll_opy_ is None or (isinstance(bstack1llll111l1ll_opy_, str) and bstack1llll111l1ll_opy_.strip() == bstack1ll1lll_opy_ (u"࠭ࠧ⌍")) or (isinstance(bstack1llll111l1ll_opy_, list) and len(bstack1llll111l1ll_opy_) == 0):
                bstack1llll1l11lll_opy_ = []
            elif isinstance(bstack1llll111l1ll_opy_, list):
                bstack1llll1l11lll_opy_ = bstack1llll111l1ll_opy_
            elif isinstance(bstack1llll111l1ll_opy_, str) and bstack1llll111l1ll_opy_.strip():
                bstack1llll1l11lll_opy_ = bstack1llll111l1ll_opy_
            else:
                logger.warning(bstack1ll1lll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡵࡲࡹࡷࡩࡥࠡࡸࡤࡰࡺ࡫ࠠࡪࡰࠣࡧࡴࡴࡦࡪࡩ࠽ࠤࢀࢃ࠮ࠡࡆࡨࡪࡦࡻ࡬ࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡧࡰࡴࡹࡿࠠ࡭࡫ࡶࡸ࠳ࠨ⌎").format(bstack1llll111l1ll_opy_))
                bstack1llll1l11lll_opy_ = []
        self.__1llll111l111_opy_(
            bstack1llll11lll11_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⌏"), False),
            bstack1llll11lll11_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡰࡳࡩ࡫ࠧ⌐"), bstack1ll1lll_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ⌑")),
            bstack1llll1l11lll_opy_
        )
        self.__1llll11ll11l_opy_(opts.get(bstack1llll111ll1l_opy_, False))
        self.__1llll1l11l11_opy_(opts.get(bstack1llll1111ll1_opy_, False))
        self.__1lll1lllll1l_opy_(opts.get(bstack1llll11l11l1_opy_, False))
    @classmethod
    def get_instance(cls, config=None):
        if cls._1ll1l111ll1_opy_ is None and config is not None:
            cls._1ll1l111ll1_opy_ = bstack1l111111l1_opy_(config)
        return cls._1ll1l111ll1_opy_
    @staticmethod
    def bstack11111l1l1_opy_(config: dict) -> bool:
        bstack1llll11lllll_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ⌒"), {}).get(bstack1llll11ll1l1_opy_, {})
        return bstack1llll11lllll_opy_.get(bstack1ll1lll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⌓"), False)
    @staticmethod
    def bstack1ll111111_opy_(config: dict) -> int:
        bstack1llll11lllll_opy_ = config.get(bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ⌔"), {}).get(bstack1llll11ll1l1_opy_, {})
        retries = 0
        if bstack1l111111l1_opy_.bstack11111l1l1_opy_(config):
            retries = bstack1llll11lllll_opy_.get(bstack1ll1lll_opy_ (u"ࠧ࡮ࡣࡻࡖࡪࡺࡲࡪࡧࡶࠫ⌕"), 1)
        return retries
    @staticmethod
    def bstack1lll1llll1_opy_(config: dict) -> dict:
        bstack1llll1l111l1_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⌖"), {})
        return {
            key: value for key, value in bstack1llll1l111l1_opy_.items() if key in bstack1llll111ll11_opy_
        }
    @staticmethod
    def bstack1lll1lll1l1l_opy_():
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⌗")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦ⌘").format(os.getenv(bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⌙")))))
    @staticmethod
    def bstack1llll111l1l1_opy_(test_name: str):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⌚")
        bstack1llll1111l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧ⌛").format(os.getenv(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⌜"))))
        with open(bstack1llll1111l11_opy_, bstack1ll1lll_opy_ (u"ࠨࡣࠪ⌝")) as file:
            file.write(bstack1ll1lll_opy_ (u"ࠤࡾࢁࡡࡴࠢ⌞").format(test_name))
    @staticmethod
    def bstack1llll111llll_opy_(framework: str) -> bool:
       return framework.lower() in bstack1llll11l1ll1_opy_
    @staticmethod
    def bstack1111ll11l1l_opy_(config: dict) -> bool:
        bstack1lll1llll1ll_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ⌟"), {}).get(bstack1lll1lll11l1_opy_, {})
        return bstack1lll1llll1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⌠"), False)
    @staticmethod
    def bstack1111ll1l111_opy_(config: dict, bstack1111lll11l1_opy_: int = 0) -> int:
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠬࠡࡹ࡫࡭ࡨ࡮ࠠࡤࡣࡱࠤࡧ࡫ࠠࡢࡰࠣࡥࡧࡹ࡯࡭ࡷࡷࡩࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡲࠡࡣࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡱࡷࡥࡱࡥࡴࡦࡵࡷࡷࠥ࠮ࡩ࡯ࡶࠬ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࠬࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⌡")
        bstack1lll1llll1ll_opy_ = config.get(bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ⌢"), {}).get(bstack1ll1lll_opy_ (u"ࠧࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭⌣"), {})
        bstack1llll111lll1_opy_ = 0
        bstack1llll11l1lll_opy_ = 0
        if bstack1l111111l1_opy_.bstack1111ll11l1l_opy_(config):
            bstack1llll11l1lll_opy_ = bstack1lll1llll1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠨ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸ࠭⌤"), 5)
            if isinstance(bstack1llll11l1lll_opy_, str) and bstack1llll11l1lll_opy_.endswith(bstack1ll1lll_opy_ (u"ࠩࠨࠫ⌥")):
                try:
                    percentage = int(bstack1llll11l1lll_opy_.strip(bstack1ll1lll_opy_ (u"ࠪࠩࠬ⌦")))
                    if bstack1111lll11l1_opy_ > 0:
                        bstack1llll111lll1_opy_ = math.ceil((percentage * bstack1111lll11l1_opy_) / 100)
                    else:
                        raise ValueError(bstack1ll1lll_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡰࡹࡸࡺࠠࡣࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠳ࡢࡢࡵࡨࡨࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࡴ࠰ࠥ⌧"))
                except ValueError as e:
                    raise ValueError(bstack1ll1lll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧࠣࡺࡦࡲࡵࡦࠢࡩࡳࡷࠦ࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶ࠾ࠥࢁࡽࠣ⌨").format(bstack1llll11l1lll_opy_)) from e
            else:
                bstack1llll111lll1_opy_ = int(bstack1llll11l1lll_opy_)
        logger.info(bstack1ll1lll_opy_ (u"ࠨࡍࡢࡺࠣࡪࡦ࡯࡬ࡶࡴࡨࡷࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡵࡨࡸࠥࡺ࡯࠻ࠢࡾࢁࠥ࠮ࡦࡳࡱࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽࠪࠤ〈").format(bstack1llll111lll1_opy_, bstack1llll11l1lll_opy_))
        return bstack1llll111lll1_opy_
    def bstack1lll1lll1ll1_opy_(self):
        return self.bstack1llll11l1l1l_opy_
    def bstack1llll1l11ll1_opy_(self):
        return self.bstack1llll1111lll_opy_
    def bstack1lll1lllllll_opy_(self):
        return self.bstack1llll11111ll_opy_
    def __1llll111l111_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1llll11l1l1l_opy_ = bool(enabled)
            if mode not in [bstack1ll1lll_opy_ (u"ࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡈ࡬ࡶࡸࡺࠧ〉"), bstack1ll1lll_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡒࡲࡱࡿࠧ⌫")]:
                logger.warning(bstack1ll1lll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡳ࡯ࡥࡧࠣࠫࢀࢃࠧࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠤࡉ࡫ࡦࡢࡷ࡯ࡸ࡮ࡴࡧࠡࡶࡲࠤࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ࠴ࠢ⌬").format(mode))
                mode = bstack1ll1lll_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ⌭")
            self.bstack1llll1111lll_opy_ = mode
            self.bstack1llll11111ll_opy_ = []
            if source is None:
                self.bstack1llll11111ll_opy_ = None
            elif isinstance(source, list):
                self.bstack1llll11111ll_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1ll1lll_opy_ (u"ࠫ࠳ࡰࡳࡰࡰࠪ⌮")):
                self.bstack1llll11111ll_opy_ = self._1lll1lll1lll_opy_(source)
            self.__1llll11ll111_opy_()
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠ࠮ࠢࡨࡲࡦࡨ࡬ࡦࡦ࠽ࠤࢀࢃࠬࠡ࡯ࡲࡨࡪࡀࠠࡼࡿ࠯ࠤࡸࡵࡵࡳࡥࡨ࠾ࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ⌯").format(enabled, mode, source, e))
    def bstack1lll1llll11l_opy_(self):
        return self.bstack1llll1l1l111_opy_
    def __1llll11ll11l_opy_(self, value):
        self.bstack1llll1l1l111_opy_ = bool(value)
        self.__1llll11ll111_opy_()
    def bstack1llll111111l_opy_(self):
        return self.bstack1llll11lll1l_opy_
    def __1llll1l11l11_opy_(self, value):
        self.bstack1llll11lll1l_opy_ = bool(value)
        self.__1llll11ll111_opy_()
    def bstack1llll1l1111l_opy_(self):
        return self.bstack1lll1llll111_opy_
    def __1lll1lllll1l_opy_(self, value):
        self.bstack1lll1llll111_opy_ = bool(value)
        self.__1llll11ll111_opy_()
    def __1llll11ll111_opy_(self):
        if self.bstack1llll11l1l1l_opy_:
            self.bstack1llll1l1l111_opy_ = False
            self.bstack1llll11lll1l_opy_ = False
            self.bstack1lll1llll111_opy_ = False
            self.bstack1llll1l11l1l_opy_.enable(bstack1llll11l1l11_opy_)
        elif self.bstack1llll1l1l111_opy_:
            self.bstack1llll11lll1l_opy_ = False
            self.bstack1lll1llll111_opy_ = False
            self.bstack1llll11l1l1l_opy_ = False
            self.bstack1llll1l11l1l_opy_.enable(bstack1llll111ll1l_opy_)
        elif self.bstack1llll11lll1l_opy_:
            self.bstack1llll1l1l111_opy_ = False
            self.bstack1lll1llll111_opy_ = False
            self.bstack1llll11l1l1l_opy_ = False
            self.bstack1llll1l11l1l_opy_.enable(bstack1llll1111ll1_opy_)
        elif self.bstack1lll1llll111_opy_:
            self.bstack1llll1l1l111_opy_ = False
            self.bstack1llll11lll1l_opy_ = False
            self.bstack1llll11l1l1l_opy_ = False
            self.bstack1llll1l11l1l_opy_.enable(bstack1llll11l11l1_opy_)
        else:
            self.bstack1llll1l11l1l_opy_.disable()
    def bstack1l11llll_opy_(self):
        return self.bstack1llll1l11l1l_opy_.bstack1lll1llll1l1_opy_()
    def bstack1l1lll1ll1_opy_(self):
        if self.bstack1llll1l11l1l_opy_.bstack1lll1llll1l1_opy_():
            return self.bstack1llll1l11l1l_opy_.get_name()
        return None
    def _1lll1lll1lll_opy_(self, bstack1lll1lll111l_opy_):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡴࡱࡸࡶࡨ࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠥࡧ࡮ࡥࠢࡩࡳࡷࡳࡡࡵࠢ࡬ࡸࠥ࡬࡯ࡳࠢࡶࡱࡦࡸࡴࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡷࡴࡻࡲࡤࡧࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠦࠨࡴࡶࡵ࠭࠿ࠦࡐࡢࡶ࡫ࠤࡹࡵࠠࡵࡪࡨࠤࡏ࡙ࡏࡏࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡮࡬ࡷࡹࡀࠠࡇࡱࡵࡱࡦࡺࡴࡦࡦࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡷ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⌰")
        if not os.path.isfile(bstack1lll1lll111l_opy_):
            logger.error(bstack1ll1lll_opy_ (u"ࠢࡔࡱࡸࡶࡨ࡫ࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡾࠩࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠧ⌱").format(bstack1lll1lll111l_opy_))
            return []
        data = None
        try:
            with open(bstack1lll1lll111l_opy_, bstack1ll1lll_opy_ (u"ࠣࡴࠥ⌲")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡍࡗࡔࡔࠠࡧࡴࡲࡱࠥࡹ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ⌳").format(bstack1lll1lll111l_opy_, e))
            return []
        _1lll1lll1l11_opy_ = None
        _1llll1l1l11l_opy_ = None
        def _1lll1lllll11_opy_():
            bstack1llll11111l1_opy_ = {}
            bstack1lll1lll11ll_opy_ = {}
            try:
                if self.bstack1lll1llllll1_opy_.startswith(bstack1ll1lll_opy_ (u"ࠪࡿࠬ⌴")) and self.bstack1lll1llllll1_opy_.endswith(bstack1ll1lll_opy_ (u"ࠫࢂ࠭⌵")):
                    bstack1llll11111l1_opy_ = json.loads(self.bstack1lll1llllll1_opy_)
                else:
                    bstack1llll11111l1_opy_ = dict(item.split(bstack1ll1lll_opy_ (u"ࠬࡀࠧ⌶")) for item in self.bstack1lll1llllll1_opy_.split(bstack1ll1lll_opy_ (u"࠭ࠬࠨ⌷")) if bstack1ll1lll_opy_ (u"ࠧ࠻ࠩ⌸") in item) if self.bstack1lll1llllll1_opy_ else {}
                if self.bstack1llll1l11111_opy_.startswith(bstack1ll1lll_opy_ (u"ࠨࡽࠪ⌹")) and self.bstack1llll1l11111_opy_.endswith(bstack1ll1lll_opy_ (u"ࠩࢀࠫ⌺")):
                    bstack1lll1lll11ll_opy_ = json.loads(self.bstack1llll1l11111_opy_)
                else:
                    bstack1lll1lll11ll_opy_ = dict(item.split(bstack1ll1lll_opy_ (u"ࠪ࠾ࠬ⌻")) for item in self.bstack1llll1l11111_opy_.split(bstack1ll1lll_opy_ (u"ࠫ࠱࠭⌼")) if bstack1ll1lll_opy_ (u"ࠬࡀࠧ⌽") in item) if self.bstack1llll1l11111_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡦࡦࡣࡷࡹࡷ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠ࡮ࡣࡳࡴ࡮ࡴࡧࡴ࠼ࠣࡿࢂࠨ⌾").format(e))
            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡ࡯ࡤࡴࡵ࡯࡮ࡨࡵࠣࡪࡷࡵ࡭ࠡࡧࡱࡺ࠿ࠦࡻࡾ࠮ࠣࡇࡑࡏ࠺ࠡࡽࢀࠦ⌿").format(bstack1llll11111l1_opy_, bstack1lll1lll11ll_opy_))
            return bstack1llll11111l1_opy_, bstack1lll1lll11ll_opy_
        if _1lll1lll1l11_opy_ is None or _1llll1l1l11l_opy_ is None:
            _1lll1lll1l11_opy_, _1llll1l1l11l_opy_ = _1lll1lllll11_opy_()
        def bstack1llll11llll1_opy_(name, bstack1llll11l1111_opy_):
            if name in _1llll1l1l11l_opy_:
                return _1llll1l1l11l_opy_[name]
            if name in _1lll1lll1l11_opy_:
                return _1lll1lll1l11_opy_[name]
            if bstack1llll11l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ⍀")):
                return bstack1llll11l1111_opy_[bstack1ll1lll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ⍁")]
            return None
        if isinstance(data, dict):
            bstack1llll11l111l_opy_ = []
            bstack1llll1l111ll_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡵࠫࡣࡡࡁ࠮࡜࠳࠱࠾ࡥ࡝ࠬࠦࠪ⍂"))
            for name, bstack1llll11l1111_opy_ in data.items():
                if not isinstance(bstack1llll11l1111_opy_, dict):
                    continue
                url = bstack1llll11l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡺࡸ࡬ࠨ⍃"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1ll1lll_opy_ (u"ࠬ࠭⍄")):
                    logger.warning(bstack1ll1lll_opy_ (u"ࠨࡒࡦࡲࡲࡷ࡮ࡺ࡯ࡳࡻ࡙ࠣࡗࡒࠠࡪࡵࠣࡱ࡮ࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡵࡲࡹࡷࡩࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥ⍅").format(name, bstack1llll11l1111_opy_))
                    continue
                if not bstack1llll1l111ll_opy_.match(name):
                    logger.warning(bstack1ll1lll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡵࡲࡹࡷࡩࡥࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠥ࡬࡯ࡳ࡯ࡤࡸࠥ࡬࡯ࡳࠢࠪࡿࢂ࠭࠺ࠡࡽࢀࠦ⍆").format(name, bstack1llll11l1111_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1ll1lll_opy_ (u"ࠣࡕࡲࡹࡷࡩࡥࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠥ࠭ࡻࡾࠩࠣࡱࡺࡹࡴࠡࡪࡤࡺࡪࠦࡡࠡ࡮ࡨࡲ࡬ࡺࡨࠡࡤࡨࡸࡼ࡫ࡥ࡯ࠢ࠴ࠤࡦࡴࡤࠡ࠵࠳ࠤࡨ࡮ࡡࡳࡣࡦࡸࡪࡸࡳ࠯ࠤ⍇").format(name))
                    continue
                bstack1llll11l1111_opy_ = bstack1llll11l1111_opy_.copy()
                bstack1llll11l1111_opy_[bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⍈")] = name
                bstack1llll11l1111_opy_[bstack1ll1lll_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ⍉")] = bstack1llll11llll1_opy_(name, bstack1llll11l1111_opy_)
                if not bstack1llll11l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ⍊")) or bstack1llll11l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ⍋")) == bstack1ll1lll_opy_ (u"࠭ࠧ⍌"):
                    logger.warning(bstack1ll1lll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡࡰࡲࡸࠥࡹࡰࡦࡥ࡬ࡪ࡮࡫ࡤࠡࡨࡲࡶࠥࡹ࡯ࡶࡴࡦࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ⍍").format(name, bstack1llll11l1111_opy_))
                    continue
                if bstack1llll11l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡤࡤࡷࡪࡈࡲࡢࡰࡦ࡬ࠬ⍎")) and bstack1llll11l1111_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡥࡸ࡫ࡂࡳࡣࡱࡧ࡭࠭⍏")] == bstack1llll11l1111_opy_[bstack1ll1lll_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ⍐")]:
                    logger.warning(bstack1ll1lll_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡧ࡮ࡥࠢࡥࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡸ࡭࡫ࠠࡴࡣࡰࡩࠥ࡬࡯ࡳࠢࡶࡳࡺࡸࡣࡦࠢࠪࡿࢂ࠭࠺ࠡࡽࢀࠦ⍑").format(name, bstack1llll11l1111_opy_))
                    continue
                bstack1llll11l111l_opy_.append(bstack1llll11l1111_opy_)
            return bstack1llll11l111l_opy_
        return data
    def bstack1llll1lll111_opy_(self):
        data = {
            bstack1ll1lll_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫ⍒"): {
                bstack1ll1lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⍓"): self.bstack1lll1lll1ll1_opy_(),
                bstack1ll1lll_opy_ (u"ࠧ࡮ࡱࡧࡩࠬ⍔"): self.bstack1llll1l11ll1_opy_(),
                bstack1ll1lll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ⍕"): self.bstack1lll1lllllll_opy_()
            }
        }
        return data
    def bstack1llll11ll1ll_opy_(self, config):
        bstack1llll11l11ll_opy_ = {}
        bstack1llll11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨ⍖")] = {
            bstack1ll1lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⍗"): self.bstack1lll1lll1ll1_opy_(),
            bstack1ll1lll_opy_ (u"ࠫࡲࡵࡤࡦࠩ⍘"): self.bstack1llll1l11ll1_opy_()
        }
        bstack1llll11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡵࡸࡥࡷ࡫ࡲࡹࡸࡲࡹࡠࡨࡤ࡭ࡱ࡫ࡤࠨ⍙")] = {
            bstack1ll1lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⍚"): self.bstack1llll111111l_opy_()
        }
        bstack1llll11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠧࡳࡷࡱࡣࡵࡸࡥࡷ࡫ࡲࡹࡸࡲࡹࡠࡨࡤ࡭ࡱ࡫ࡤࡠࡨ࡬ࡶࡸࡺࠧ⍛")] = {
            bstack1ll1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⍜"): self.bstack1lll1llll11l_opy_()
        }
        bstack1llll11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡧࡣ࡬ࡰ࡮ࡴࡧࡠࡣࡱࡨࡤ࡬࡬ࡢ࡭ࡼࠫ⍝")] = {
            bstack1ll1lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⍞"): self.bstack1llll1l1111l_opy_()
        }
        if self.bstack11111l1l1_opy_(config):
            bstack1llll11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡴࡳࡻࡢࡸࡪࡹࡴࡴࡡࡲࡲࡤ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⍟")] = {
                bstack1ll1lll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⍠"): True,
                bstack1ll1lll_opy_ (u"࠭࡭ࡢࡺࡢࡶࡪࡺࡲࡪࡧࡶࠫ⍡"): self.bstack1ll111111_opy_(config)
            }
        if self.bstack1111ll11l1l_opy_(config):
            bstack1llll11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࡵ࡮ࡠࡨࡤ࡭ࡱࡻࡲࡦࠩ⍢")] = {
                bstack1ll1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⍣"): True,
                bstack1ll1lll_opy_ (u"ࠩࡰࡥࡽࡥࡦࡢ࡫࡯ࡹࡷ࡫ࡳࠨ⍤"): self.bstack1111ll1l111_opy_(config)
            }
        return bstack1llll11l11ll_opy_
    def bstack1ll1ll1l1l_opy_(self, config):
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡱ࡯ࡰࡪࡩࡴࡴࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡢࡺࠢࡰࡥࡰ࡯࡮ࡨࠢࡤࠤࡨࡧ࡬࡭ࠢࡷࡳࠥࡺࡨࡦࠢࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠠࡦࡰࡧࡴࡴ࡯࡮ࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟ࡶࡷ࡬ࡨࠥ࠮ࡳࡵࡴࠬ࠾࡚ࠥࡨࡦࠢࡘ࡙ࡎࡊࠠࡰࡨࠣࡸ࡭࡫ࠠࡣࡷ࡬ࡰࡩࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡨࡦࡺࡡࠡࡨࡲࡶ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠡࡧࡱࡨࡵࡵࡩ࡯ࡶ࠯ࠤࡴࡸࠠࡏࡱࡱࡩࠥ࡯ࡦࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⍥")
        if not (config.get(bstack1ll1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⍦"), None) in bstack1111lllll11_opy_ and self.bstack1lll1lll1ll1_opy_()):
            return None
        bstack1llll1111111_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⍧"), None)
        logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࡀࠠࡼࡿࠥ⍨").format(bstack1llll1111111_opy_))
        try:
            bstack111l1lll111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠧ⍩").format(bstack1llll1111111_opy_)
            payload = {
                bstack1ll1lll_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨ⍪"): config.get(bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⍫"), bstack1ll1lll_opy_ (u"ࠪࠫ⍬")),
                bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢ⍭"): config.get(bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ⍮"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ⍯"): os.environ.get(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࠨ⍰"), bstack1ll1lll_opy_ (u"ࠣࠤ⍱")),
                bstack1ll1lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧ⍲"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨ⍳")) or bstack1ll1lll_opy_ (u"ࠦ࠵ࠨ⍴")),
                bstack1ll1lll_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤ⍵"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣ⍶")) or bstack1ll1lll_opy_ (u"ࠢ࠲ࠤ⍷")),
                bstack1ll1lll_opy_ (u"ࠣࡪࡲࡷࡹࡏ࡮ࡧࡱࠥ⍸"): get_host_info(),
            }
            logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡶࡡࡺ࡮ࡲࡥࡩࡀࠠࡼࡿࠥ⍹").format(payload))
            response = bstack111l1ll11l1_opy_.bstack1llll1111l1l_opy_(bstack111l1lll111_opy_, payload)
            if response:
                logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡄࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⍺").format(response))
                return response
            else:
                logger.error(bstack1ll1lll_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣ⍻").format(bstack1llll1111111_opy_))
                return None
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇࠤࢀࢃ࠺ࠡࡽࢀࠦ⍼").format(bstack1llll1111111_opy_, e))
            return None