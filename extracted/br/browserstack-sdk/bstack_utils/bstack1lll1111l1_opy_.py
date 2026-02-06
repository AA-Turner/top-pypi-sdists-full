# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack111l1l11ll_opy_, bstack111lllll1l1_opy_
from bstack_utils.helper import bstack1111llll1l1_opy_, get_host_info
from bstack_utils.bstack11l11ll11l1_opy_ import bstack11l11ll1l11_opy_
import json
import re
import sys
bstack1111111l111_opy_ = bstack11lllll_opy_ (u"ࠤࡵࡩࡹࡸࡹࡕࡧࡶࡸࡸࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣ῏")
bstack1lllllll1ll1_opy_ = bstack11lllll_opy_ (u"ࠥࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠤῐ")
bstack111111lll1l_opy_ = bstack11lllll_opy_ (u"ࠦࡷࡻ࡮ࡑࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡊࡦ࡯࡬ࡦࡦࡉ࡭ࡷࡹࡴࠣῑ")
bstack11111l11l11_opy_ = bstack11lllll_opy_ (u"ࠧࡸࡥࡳࡷࡱࡔࡷ࡫ࡶࡪࡱࡸࡷࡱࡿࡆࡢ࡫࡯ࡩࡩࠨῒ")
bstack1111111l1l1_opy_ = bstack11lllll_opy_ (u"ࠨࡳ࡬࡫ࡳࡊࡱࡧ࡫ࡺࡣࡱࡨࡋࡧࡩ࡭ࡧࡧࠦΐ")
bstack111111l1ll1_opy_ = bstack11lllll_opy_ (u"ࠢࡳࡷࡱࡗࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࠦ῔")
bstack11111l111l1_opy_ = {
    bstack1111111l111_opy_,
    bstack1lllllll1ll1_opy_,
    bstack111111lll1l_opy_,
    bstack11111l11l11_opy_,
    bstack1111111l1l1_opy_,
    bstack111111l1ll1_opy_
}
bstack1111111lll1_opy_ = {bstack11lllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ῕")}
logger = logger_utils.get_logger(__name__, bstack111l1l11ll_opy_)
class bstack1llllllllll1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack111111l1l1l_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack11l1lll11_opy_:
    _1ll11llll1l_opy_ = None
    def __init__(self, config):
        self.bstack111111l11ll_opy_ = False
        self.bstack11111111l1l_opy_ = False
        self.bstack1lllllll1l1l_opy_ = False
        self.bstack11111l111ll_opy_ = False
        self.bstack111111ll11l_opy_ = None
        self.bstack11111l11111_opy_ = bstack1llllllllll1_opy_()
        self.bstack11111l11ll1_opy_ = None
        opts = config.get(bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ῖ"), {})
        self.bstack11111111ll1_opy_ = config.get(bstack11lllll_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡊࡔࡖࠨῗ"), bstack11lllll_opy_ (u"ࠦࠧῘ"))
        self.bstack1lllllll1111_opy_ = config.get(bstack11lllll_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡃࡍࡋࠪῙ"), bstack11lllll_opy_ (u"ࠨࠢῚ"))
        bstack11111l11lll_opy_ = opts.get(bstack111111l1ll1_opy_, {})
        bstack1lllllll1l11_opy_ = None
        if bstack11lllll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧΊ") in bstack11111l11lll_opy_:
            bstack11111111l11_opy_ = bstack11111l11lll_opy_[bstack11lllll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ῜")]
            if bstack11111111l11_opy_ is None or (isinstance(bstack11111111l11_opy_, str) and bstack11111111l11_opy_.strip() == bstack11lllll_opy_ (u"ࠩࠪ῝")) or (isinstance(bstack11111111l11_opy_, list) and len(bstack11111111l11_opy_) == 0):
                bstack1lllllll1l11_opy_ = []
            elif isinstance(bstack11111111l11_opy_, list):
                bstack1lllllll1l11_opy_ = bstack11111111l11_opy_
            elif isinstance(bstack11111111l11_opy_, str) and bstack11111111l11_opy_.strip():
                bstack1lllllll1l11_opy_ = bstack11111111l11_opy_
            else:
                logger.warning(bstack11lllll_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡵࡵࡳࡥࡨࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿ࠱ࠤࡉ࡫ࡦࡢࡷ࡯ࡸ࡮ࡴࡧࠡࡶࡲࠤࡪࡳࡰࡵࡻࠣࡰ࡮ࡹࡴ࠯ࠤ῞").format(bstack11111111l11_opy_))
                bstack1lllllll1l11_opy_ = []
        self.__11111111111_opy_(
            bstack11111l11lll_opy_.get(bstack11lllll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ῟"), False),
            bstack11111l11lll_opy_.get(bstack11lllll_opy_ (u"ࠬࡳ࡯ࡥࡧࠪῠ"), bstack11lllll_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭ῡ")),
            bstack1lllllll1l11_opy_
        )
        self.__1lllllllll11_opy_(opts.get(bstack111111lll1l_opy_, False))
        self.__111111l11l1_opy_(opts.get(bstack11111l11l11_opy_, False))
        self.__11111l1111l_opy_(opts.get(bstack1111111l1l1_opy_, False))
    @classmethod
    def bstack1llll1l111_opy_(cls, config=None):
        if cls._1ll11llll1l_opy_ is None and config is not None:
            cls._1ll11llll1l_opy_ = bstack11l1lll11_opy_(config)
        return cls._1ll11llll1l_opy_
    @staticmethod
    def bstack111l111l_opy_(config: dict) -> bool:
        bstack11111l1l111_opy_ = config.get(bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫῢ"), {}).get(bstack1111111l111_opy_, {})
        return bstack11111l1l111_opy_.get(bstack11lllll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩΰ"), False)
    @staticmethod
    def bstack1l1l1lll_opy_(config: dict) -> int:
        bstack11111l1l111_opy_ = config.get(bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ῤ"), {}).get(bstack1111111l111_opy_, {})
        retries = 0
        if bstack11l1lll11_opy_.bstack111l111l_opy_(config):
            retries = bstack11111l1l111_opy_.get(bstack11lllll_opy_ (u"ࠪࡱࡦࡾࡒࡦࡶࡵ࡭ࡪࡹࠧῥ"), 1)
        return retries
    @staticmethod
    def bstack111ll1l11l_opy_(config: dict) -> dict:
        bstack111111lll11_opy_ = config.get(bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨῦ"), {})
        return {
            key: value for key, value in bstack111111lll11_opy_.items() if key in bstack11111l111l1_opy_
        }
    @staticmethod
    def bstack1lllllll111l_opy_():
        bstack11lllll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤῧ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃࠢῨ").format(os.getenv(bstack11lllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧῩ")))))
    @staticmethod
    def bstack1lllllll1lll_opy_(test_name: str):
        bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧῪ")
        bstack111111111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣΎ").format(os.getenv(bstack11lllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣῬ"))))
        with open(bstack111111111ll_opy_, bstack11lllll_opy_ (u"ࠫࡦ࠭῭")) as file:
            file.write(bstack11lllll_opy_ (u"ࠧࢁࡽ࡝ࡰࠥ΅").format(test_name))
    @staticmethod
    def bstack1lllllll11l1_opy_(framework: str) -> bool:
       return framework.lower() in bstack1111111lll1_opy_
    @staticmethod
    def bstack111lll1l1l1_opy_(config: dict) -> bool:
        bstack111111lllll_opy_ = config.get(bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ`"), {}).get(bstack1lllllll1ll1_opy_, {})
        return bstack111111lllll_opy_.get(bstack11lllll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ῰"), False)
    @staticmethod
    def bstack111llll1l11_opy_(config: dict, bstack111lll1llll_opy_: int = 0) -> int:
        bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠯ࠤࡼ࡮ࡩࡤࡪࠣࡧࡦࡴࠠࡣࡧࠣࡥࡳࠦࡡࡣࡵࡲࡰࡺࡺࡥࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡵࠤࡦࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡴࡺࡡ࡭ࡡࡷࡩࡸࡺࡳࠡࠪ࡬ࡲࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࠨࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡩࡳࡷࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠰ࡦࡦࡹࡥࡥࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࡸ࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ῱")
        bstack111111lllll_opy_ = config.get(bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ῲ"), {}).get(bstack11lllll_opy_ (u"ࠪࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠩῳ"), {})
        bstack1llllllll111_opy_ = 0
        bstack111111ll1ll_opy_ = 0
        if bstack11l1lll11_opy_.bstack111lll1l1l1_opy_(config):
            bstack111111ll1ll_opy_ = bstack111111lllll_opy_.get(bstack11lllll_opy_ (u"ࠫࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴࠩῴ"), 5)
            if isinstance(bstack111111ll1ll_opy_, str) and bstack111111ll1ll_opy_.endswith(bstack11lllll_opy_ (u"ࠬࠫࠧ῵")):
                try:
                    percentage = int(bstack111111ll1ll_opy_.strip(bstack11lllll_opy_ (u"࠭ࠥࠨῶ")))
                    if bstack111lll1llll_opy_ > 0:
                        bstack1llllllll111_opy_ = math.ceil((percentage * bstack111lll1llll_opy_) / 100)
                    else:
                        raise ValueError(bstack11lllll_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡳࡵࡴࡶࠣࡦࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠳ࠨῷ"))
                except ValueError as e:
                    raise ValueError(bstack11lllll_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪࠦࡶࡢ࡮ࡸࡩࠥ࡬࡯ࡳࠢࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹ࠺ࠡࡽࢀࠦῸ").format(bstack111111ll1ll_opy_)) from e
            else:
                bstack1llllllll111_opy_ = int(bstack111111ll1ll_opy_)
        logger.info(bstack11lllll_opy_ (u"ࠤࡐࡥࡽࠦࡦࡢ࡫࡯ࡹࡷ࡫ࡳࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡸ࡫ࡴࠡࡶࡲ࠾ࠥࢁࡽࠡࠪࡩࡶࡴࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡽࢀ࠭ࠧΌ").format(bstack1llllllll111_opy_, bstack111111ll1ll_opy_))
        return bstack1llllllll111_opy_
    def bstack11111l11l1l_opy_(self):
        return self.bstack11111l111ll_opy_
    def bstack1lllllllllll_opy_(self):
        return self.bstack111111ll11l_opy_
    def bstack111111llll1_opy_(self):
        return self.bstack11111l11ll1_opy_
    def __11111111111_opy_(self, enabled, mode, source=None):
        try:
            self.bstack11111l111ll_opy_ = bool(enabled)
            if mode not in [bstack11lllll_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪῺ"), bstack11lllll_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡕ࡮࡭ࡻࠪΏ")]:
                logger.warning(bstack11lllll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳ࡮ࡣࡵࡸࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡ࡯ࡲࡨࡪࠦࠧࡼࡿࠪࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡅࡧࡩࡥࡺࡲࡴࡪࡰࡪࠤࡹࡵࠠࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ࠰ࠥῼ").format(mode))
                mode = bstack11lllll_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭´")
            self.bstack111111ll11l_opy_ = mode
            self.bstack11111l11ll1_opy_ = []
            if source is None:
                self.bstack11111l11ll1_opy_ = None
            elif isinstance(source, list):
                self.bstack11111l11ll1_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack11lllll_opy_ (u"ࠧ࠯࡬ࡶࡳࡳ࠭῾")):
                self.bstack11111l11ll1_opy_ = self._111111l1111_opy_(source)
            self.__111111l1lll_opy_()
        except Exception as e:
            logger.error(bstack11lllll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣ࠱ࠥ࡫࡮ࡢࡤ࡯ࡩࡩࡀࠠࡼࡿ࠯ࠤࡲࡵࡤࡦ࠼ࠣࡿࢂ࠲ࠠࡴࡱࡸࡶࡨ࡫࠺ࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ῿").format(enabled, mode, source, e))
    def bstack111111l1l11_opy_(self):
        return self.bstack111111l11ll_opy_
    def __1lllllllll11_opy_(self, value):
        self.bstack111111l11ll_opy_ = bool(value)
        self.__111111l1lll_opy_()
    def bstack1lllllllll1l_opy_(self):
        return self.bstack11111111l1l_opy_
    def __111111l11l1_opy_(self, value):
        self.bstack11111111l1l_opy_ = bool(value)
        self.__111111l1lll_opy_()
    def bstack1111111l1ll_opy_(self):
        return self.bstack1lllllll1l1l_opy_
    def __11111l1111l_opy_(self, value):
        self.bstack1lllllll1l1l_opy_ = bool(value)
        self.__111111l1lll_opy_()
    def __111111l1lll_opy_(self):
        if self.bstack11111l111ll_opy_:
            self.bstack111111l11ll_opy_ = False
            self.bstack11111111l1l_opy_ = False
            self.bstack1lllllll1l1l_opy_ = False
            self.bstack11111l11111_opy_.enable(bstack111111l1ll1_opy_)
        elif self.bstack111111l11ll_opy_:
            self.bstack11111111l1l_opy_ = False
            self.bstack1lllllll1l1l_opy_ = False
            self.bstack11111l111ll_opy_ = False
            self.bstack11111l11111_opy_.enable(bstack111111lll1l_opy_)
        elif self.bstack11111111l1l_opy_:
            self.bstack111111l11ll_opy_ = False
            self.bstack1lllllll1l1l_opy_ = False
            self.bstack11111l111ll_opy_ = False
            self.bstack11111l11111_opy_.enable(bstack11111l11l11_opy_)
        elif self.bstack1lllllll1l1l_opy_:
            self.bstack111111l11ll_opy_ = False
            self.bstack11111111l1l_opy_ = False
            self.bstack11111l111ll_opy_ = False
            self.bstack11111l11111_opy_.enable(bstack1111111l1l1_opy_)
        else:
            self.bstack11111l11111_opy_.disable()
    def bstack1l1ll11ll1_opy_(self):
        return self.bstack11111l11111_opy_.bstack111111l1l1l_opy_()
    def bstack1l111l11l1_opy_(self):
        if self.bstack11111l11111_opy_.bstack111111l1l1l_opy_():
            return self.bstack11111l11111_opy_.get_name()
        return None
    def _111111l1111_opy_(self, bstack1111111111l_opy_):
        bstack11lllll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡷࡴࡻࡲࡤࡧࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠡࡣࡱࡨࠥ࡬࡯ࡳ࡯ࡤࡸࠥ࡯ࡴࠡࡨࡲࡶࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡳࡰࡷࡵࡧࡪࡥࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠢࠫࡷࡹࡸࠩ࠻ࠢࡓࡥࡹ࡮ࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡕࡒࡒࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡊࡴࡸ࡭ࡢࡶࡷࡩࡩࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡳࡧࡳࡳࡸ࡯ࡴࡰࡴࡼࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ ")
        if not os.path.isfile(bstack1111111111l_opy_):
            logger.error(bstack11lllll_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࠩࡾࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠣ ").format(bstack1111111111l_opy_))
            return []
        data = None
        try:
            with open(bstack1111111111l_opy_, bstack11lllll_opy_ (u"ࠦࡷࠨ ")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack11lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡐࡓࡐࡐࠣࡪࡷࡵ࡭ࠡࡵࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ ").format(bstack1111111111l_opy_, e))
            return []
        _111111ll111_opy_ = None
        _11111111lll_opy_ = None
        def _1111111l11l_opy_():
            bstack1llllllll1l1_opy_ = {}
            bstack1111111ll11_opy_ = {}
            try:
                if self.bstack11111111ll1_opy_.startswith(bstack11lllll_opy_ (u"࠭ࡻࠨ ")) and self.bstack11111111ll1_opy_.endswith(bstack11lllll_opy_ (u"ࠧࡾࠩ ")):
                    bstack1llllllll1l1_opy_ = json.loads(self.bstack11111111ll1_opy_)
                else:
                    bstack1llllllll1l1_opy_ = dict(item.split(bstack11lllll_opy_ (u"ࠨ࠼ࠪ ")) for item in self.bstack11111111ll1_opy_.split(bstack11lllll_opy_ (u"ࠩ࠯ࠫ ")) if bstack11lllll_opy_ (u"ࠪ࠾ࠬ ") in item) if self.bstack11111111ll1_opy_ else {}
                if self.bstack1lllllll1111_opy_.startswith(bstack11lllll_opy_ (u"ࠫࢀ࠭ ")) and self.bstack1lllllll1111_opy_.endswith(bstack11lllll_opy_ (u"ࠬࢃࠧ ")):
                    bstack1111111ll11_opy_ = json.loads(self.bstack1lllllll1111_opy_)
                else:
                    bstack1111111ll11_opy_ = dict(item.split(bstack11lllll_opy_ (u"࠭࠺ࠨ​")) for item in self.bstack1lllllll1111_opy_.split(bstack11lllll_opy_ (u"ࠧ࠭ࠩ‌")) if bstack11lllll_opy_ (u"ࠨ࠼ࠪ‍") in item) if self.bstack1lllllll1111_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡩࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡱࡦࡶࡰࡪࡰࡪࡷ࠿ࠦࡻࡾࠤ‎").format(e))
            logger.debug(bstack11lllll_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠦࡦࡳࡱࡰࠤࡪࡴࡶ࠻ࠢࡾࢁ࠱ࠦࡃࡍࡋ࠽ࠤࢀࢃࠢ‏").format(bstack1llllllll1l1_opy_, bstack1111111ll11_opy_))
            return bstack1llllllll1l1_opy_, bstack1111111ll11_opy_
        if _111111ll111_opy_ is None or _11111111lll_opy_ is None:
            _111111ll111_opy_, _11111111lll_opy_ = _1111111l11l_opy_()
        def bstack1111111llll_opy_(name, bstack1llllllll1ll_opy_):
            if name in _11111111lll_opy_:
                return _11111111lll_opy_[name]
            if name in _111111ll111_opy_:
                return _111111ll111_opy_[name]
            if bstack1llllllll1ll_opy_.get(bstack11lllll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ‐")):
                return bstack1llllllll1ll_opy_[bstack11lllll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ‑")]
            return None
        if isinstance(data, dict):
            bstack1111111ll1l_opy_ = []
            bstack111111l111l_opy_ = re.compile(bstack11lllll_opy_ (u"ࡸࠧ࡟࡝ࡄ࠱࡟࠶࠭࠺ࡡࡠ࠯ࠩ࠭‒"))
            for name, bstack1llllllll1ll_opy_ in data.items():
                if not isinstance(bstack1llllllll1ll_opy_, dict):
                    continue
                url = bstack1llllllll1ll_opy_.get(bstack11lllll_opy_ (u"ࠧࡶࡴ࡯ࠫ–"))
                if url is None or (isinstance(url, str) and url.strip() == bstack11lllll_opy_ (u"ࠨࠩ—")):
                    logger.warning(bstack11lllll_opy_ (u"ࠤࡕࡩࡵࡵࡳࡪࡶࡲࡶࡾࠦࡕࡓࡎࠣ࡭ࡸࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡸࡵࡵࡳࡥࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ―").format(name, bstack1llllllll1ll_opy_))
                    continue
                if not bstack111111l111l_opy_.match(name):
                    logger.warning(bstack11lllll_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡵࡵࡳࡥࡨࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࡨࡲࡶࡲࡧࡴࠡࡨࡲࡶࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ‖").format(name, bstack1llllllll1ll_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack11lllll_opy_ (u"ࠦࡘࡵࡵࡳࡥࡨࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࠩࡾࢁࠬࠦ࡭ࡶࡵࡷࠤ࡭ࡧࡶࡦࠢࡤࠤࡱ࡫࡮ࡨࡶ࡫ࠤࡧ࡫ࡴࡸࡧࡨࡲࠥ࠷ࠠࡢࡰࡧࠤ࠸࠶ࠠࡤࡪࡤࡶࡦࡩࡴࡦࡴࡶ࠲ࠧ‗").format(name))
                    continue
                bstack1llllllll1ll_opy_ = bstack1llllllll1ll_opy_.copy()
                bstack1llllllll1ll_opy_[bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ‘")] = name
                bstack1llllllll1ll_opy_[bstack11lllll_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭’")] = bstack1111111llll_opy_(name, bstack1llllllll1ll_opy_)
                if not bstack1llllllll1ll_opy_.get(bstack11lllll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧ‚")) or bstack1llllllll1ll_opy_.get(bstack11lllll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ‛")) == bstack11lllll_opy_ (u"ࠩࠪ“"):
                    logger.warning(bstack11lllll_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡳࡵࡴࠡࡵࡳࡩࡨ࡯ࡦࡪࡧࡧࠤ࡫ࡵࡲࠡࡵࡲࡹࡷࡩࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥ”").format(name, bstack1llllllll1ll_opy_))
                    continue
                if bstack1llllllll1ll_opy_.get(bstack11lllll_opy_ (u"ࠫࡧࡧࡳࡦࡄࡵࡥࡳࡩࡨࠨ„")) and bstack1llllllll1ll_opy_[bstack11lllll_opy_ (u"ࠬࡨࡡࡴࡧࡅࡶࡦࡴࡣࡩࠩ‟")] == bstack1llllllll1ll_opy_[bstack11lllll_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭†")]:
                    logger.warning(bstack11lllll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡࡣࡱࡨࠥࡨࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡧࡦࡴ࡮ࡰࡶࠣࡦࡪࠦࡴࡩࡧࠣࡷࡦࡳࡥࠡࡨࡲࡶࠥࡹ࡯ࡶࡴࡦࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ‡").format(name, bstack1llllllll1ll_opy_))
                    continue
                bstack1111111ll1l_opy_.append(bstack1llllllll1ll_opy_)
            return bstack1111111ll1l_opy_
        return data
    def bstack11111l1ll11_opy_(self):
        data = {
            bstack11lllll_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ•"): {
                bstack11lllll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ‣"): self.bstack11111l11l1l_opy_(),
                bstack11lllll_opy_ (u"ࠪࡱࡴࡪࡥࠨ․"): self.bstack1lllllllllll_opy_(),
                bstack11lllll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ‥"): self.bstack111111llll1_opy_()
            }
        }
        return data
    def bstack111111ll1l1_opy_(self, config):
        bstack111111111l1_opy_ = {}
        bstack111111111l1_opy_[bstack11lllll_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫ…")] = {
            bstack11lllll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ‧"): self.bstack11111l11l1l_opy_(),
            bstack11lllll_opy_ (u"ࠧ࡮ࡱࡧࡩࠬ "): self.bstack1lllllllllll_opy_()
        }
        bstack111111111l1_opy_[bstack11lllll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟ࡱࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡣ࡫ࡧࡩ࡭ࡧࡧࠫ ")] = {
            bstack11lllll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ‪"): self.bstack1lllllllll1l_opy_()
        }
        bstack111111111l1_opy_[bstack11lllll_opy_ (u"ࠪࡶࡺࡴ࡟ࡱࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡣ࡫ࡧࡩ࡭ࡧࡧࡣ࡫࡯ࡲࡴࡶࠪ‫")] = {
            bstack11lllll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ‬"): self.bstack111111l1l11_opy_()
        }
        bstack111111111l1_opy_[bstack11lllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡪࡦ࡯࡬ࡪࡰࡪࡣࡦࡴࡤࡠࡨ࡯ࡥࡰࡿࠧ‭")] = {
            bstack11lllll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ‮"): self.bstack1111111l1ll_opy_()
        }
        if self.bstack111l111l_opy_(config):
            bstack111111111l1_opy_[bstack11lllll_opy_ (u"ࠧࡳࡧࡷࡶࡾࡥࡴࡦࡵࡷࡷࡤࡵ࡮ࡠࡨࡤ࡭ࡱࡻࡲࡦࠩ ")] = {
                bstack11lllll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ‰"): True,
                bstack11lllll_opy_ (u"ࠩࡰࡥࡽࡥࡲࡦࡶࡵ࡭ࡪࡹࠧ‱"): self.bstack1l1l1lll_opy_(config)
            }
        if self.bstack111lll1l1l1_opy_(config):
            bstack111111111l1_opy_[bstack11lllll_opy_ (u"ࠪࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡱࡱࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠬ′")] = {
                bstack11lllll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ″"): True,
                bstack11lllll_opy_ (u"ࠬࡳࡡࡹࡡࡩࡥ࡮ࡲࡵࡳࡧࡶࠫ‴"): self.bstack111llll1l11_opy_(config)
            }
        return bstack111111111l1_opy_
    def bstack11ll1lll1_opy_(self, config):
        bstack11lllll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡴࡲ࡬ࡦࡥࡷࡷࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡥࡽࠥࡳࡡ࡬࡫ࡱ࡫ࠥࡧࠠࡤࡣ࡯ࡰࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩ࡛ࠥࡕࡊࡆࠣࡳ࡫ࠦࡴࡩࡧࠣࡦࡺ࡯࡬ࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ‵")
        if not (config.get(bstack11lllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ‶"), None) in bstack111lllll1l1_opy_ and self.bstack11111l11l1l_opy_()):
            return None
        bstack1llllllll11l_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭‷"), None)
        logger.debug(bstack11lllll_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡄࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨ‸").format(bstack1llllllll11l_opy_))
        try:
            bstack11l11ll1ll1_opy_ = bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠣ‹").format(bstack1llllllll11l_opy_)
            payload = {
                bstack11lllll_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤ›"): config.get(bstack11lllll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ※"), bstack11lllll_opy_ (u"࠭ࠧ‼")),
                bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥ‽"): config.get(bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ‾"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ‿"): os.environ.get(bstack11lllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠤ⁀"), bstack11lllll_opy_ (u"ࠦࠧ⁁")),
                bstack11lllll_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣ⁂"): int(os.environ.get(bstack11lllll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤ⁃")) or bstack11lllll_opy_ (u"ࠢ࠱ࠤ⁄")),
                bstack11lllll_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧ⁅"): int(os.environ.get(bstack11lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦ⁆")) or bstack11lllll_opy_ (u"ࠥ࠵ࠧ⁇")),
                bstack11lllll_opy_ (u"ࠦ࡭ࡵࡳࡵࡋࡱࡪࡴࠨ⁈"): get_host_info(),
            }
            logger.debug(bstack11lllll_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡲࡤࡽࡱࡵࡡࡥ࠼ࠣࡿࢂࠨ⁉").format(payload))
            response = bstack11l11ll1l11_opy_.bstack1lllllll11ll_opy_(bstack11l11ll1ll1_opy_, payload)
            if response:
                logger.debug(bstack11lllll_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡇࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ⁊").format(response))
                return response
            else:
                logger.error(bstack11lllll_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊ࠺ࠡࡽࢀࠦ⁋").format(bstack1llllllll11l_opy_))
                return None
        except Exception as e:
            logger.error(bstack11lllll_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊࠠࡼࡿ࠽ࠤࢀࢃࠢ⁌").format(bstack1llllllll11l_opy_, e))
            return None