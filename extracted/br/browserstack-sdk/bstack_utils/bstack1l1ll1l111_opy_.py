# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1l1111l1l_opy_
from bstack_utils.constants import bstack1l1ll1l11_opy_, bstack11l1111l1ll_opy_
from bstack_utils.helper import bstack111ll1ll1l1_opy_, get_host_info
from bstack_utils.bstack11l11ll1l1l_opy_ import bstack11l11lll1l1_opy_
import json
import re
import sys
bstack11111l1l111_opy_ = bstack11l1ll1_opy_ (u"ࠧࡸࡥࡵࡴࡼࡘࡪࡹࡴࡴࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦᾯ")
bstack111111111l1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡡࡣࡱࡵࡸࡇࡻࡩ࡭ࡦࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠧᾰ")
bstack11111l1l1l1_opy_ = bstack11l1ll1_opy_ (u"ࠢࡳࡷࡱࡔࡷ࡫ࡶࡪࡱࡸࡷࡱࡿࡆࡢ࡫࡯ࡩࡩࡌࡩࡳࡵࡷࠦᾱ")
bstack11111l11lll_opy_ = bstack11l1ll1_opy_ (u"ࠣࡴࡨࡶࡺࡴࡐࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡉࡥ࡮ࡲࡥࡥࠤᾲ")
bstack1lllllllllll_opy_ = bstack11l1ll1_opy_ (u"ࠤࡶ࡯࡮ࡶࡆ࡭ࡣ࡮ࡽࡦࡴࡤࡇࡣ࡬ࡰࡪࡪࠢᾳ")
bstack11111l1l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠥࡶࡺࡴࡓ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠢᾴ")
bstack1llllllll111_opy_ = {
    bstack11111l1l111_opy_,
    bstack111111111l1_opy_,
    bstack11111l1l1l1_opy_,
    bstack11111l11lll_opy_,
    bstack1lllllllllll_opy_,
    bstack11111l1l1ll_opy_
}
bstack1111111ll1l_opy_ = {bstack11l1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᾵")}
logger = bstack1l1111l1l_opy_.get_logger(__name__, bstack1l1ll1l11_opy_)
class bstack111111ll111_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack11111111l1l_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack11111l1l_opy_:
    _1ll1l1lll11_opy_ = None
    def __init__(self, config):
        self.bstack111111111ll_opy_ = False
        self.bstack111111l1111_opy_ = False
        self.bstack1lllllllll11_opy_ = False
        self.bstack11111l11l11_opy_ = False
        self.bstack11111l1l11l_opy_ = None
        self.bstack11111111111_opy_ = bstack111111ll111_opy_()
        self.bstack11111l11l1l_opy_ = None
        opts = config.get(bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᾶ"), {})
        self.bstack1lllllll1lll_opy_ = config.get(bstack11l1ll1_opy_ (u"࠭ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࡆࡐ࡙ࠫᾷ"), bstack11l1ll1_opy_ (u"ࠢࠣᾸ"))
        self.bstack11111111l11_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠨࡵࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࡈࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࡦࡵࡆࡐࡎ࠭Ᾱ"), bstack11l1ll1_opy_ (u"ࠤࠥᾺ"))
        bstack1111111lll1_opy_ = opts.get(bstack11111l1l1ll_opy_, {})
        bstack1llllllll11l_opy_ = None
        if bstack11l1ll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪΆ") in bstack1111111lll1_opy_:
            bstack111111lllll_opy_ = bstack1111111lll1_opy_[bstack11l1ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᾼ")]
            if bstack111111lllll_opy_ is None or (isinstance(bstack111111lllll_opy_, str) and bstack111111lllll_opy_.strip() == bstack11l1ll1_opy_ (u"ࠬ࠭᾽")) or (isinstance(bstack111111lllll_opy_, list) and len(bstack111111lllll_opy_) == 0):
                bstack1llllllll11l_opy_ = []
            elif isinstance(bstack111111lllll_opy_, list):
                bstack1llllllll11l_opy_ = bstack111111lllll_opy_
            elif isinstance(bstack111111lllll_opy_, str) and bstack111111lllll_opy_.strip():
                bstack1llllllll11l_opy_ = bstack111111lllll_opy_
            else:
                logger.warning(bstack11l1ll1_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡱࡸࡶࡨ࡫ࠠࡷࡣ࡯ࡹࡪࠦࡩ࡯ࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡿࢂ࠴ࠠࡅࡧࡩࡥࡺࡲࡴࡪࡰࡪࠤࡹࡵࠠࡦ࡯ࡳࡸࡾࠦ࡬ࡪࡵࡷ࠲ࠧι").format(bstack111111lllll_opy_))
                bstack1llllllll11l_opy_ = []
        self.__111111ll11l_opy_(
            bstack1111111lll1_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ᾿"), False),
            bstack1111111lll1_opy_.get(bstack11l1ll1_opy_ (u"ࠨ࡯ࡲࡨࡪ࠭῀"), bstack11l1ll1_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡊ࡮ࡸࡳࡵࠩ῁")),
            bstack1llllllll11l_opy_
        )
        self.__1111111l111_opy_(opts.get(bstack11111l1l1l1_opy_, False))
        self.__111111l1ll1_opy_(opts.get(bstack11111l11lll_opy_, False))
        self.__111111l1lll_opy_(opts.get(bstack1lllllllllll_opy_, False))
    @classmethod
    def bstack1l11l11l1_opy_(cls, config=None):
        if cls._1ll1l1lll11_opy_ is None and config is not None:
            cls._1ll1l1lll11_opy_ = bstack11111l1l_opy_(config)
        return cls._1ll1l1lll11_opy_
    @staticmethod
    def bstack1lll1l1l_opy_(config: dict) -> bool:
        bstack11111l1lll1_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧῂ"), {}).get(bstack11111l1l111_opy_, {})
        return bstack11111l1lll1_opy_.get(bstack11l1ll1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬῃ"), False)
    @staticmethod
    def bstack11ll1ll1l1_opy_(config: dict) -> int:
        bstack11111l1lll1_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩῄ"), {}).get(bstack11111l1l111_opy_, {})
        retries = 0
        if bstack11111l1l_opy_.bstack1lll1l1l_opy_(config):
            retries = bstack11111l1lll1_opy_.get(bstack11l1ll1_opy_ (u"࠭࡭ࡢࡺࡕࡩࡹࡸࡩࡦࡵࠪ῅"), 1)
        return retries
    @staticmethod
    def bstack11ll111111_opy_(config: dict) -> dict:
        bstack111111llll1_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫῆ"), {})
        return {
            key: value for key, value in bstack111111llll1_opy_.items() if key in bstack1llllllll111_opy_
        }
    @staticmethod
    def bstack111111lll1l_opy_():
        bstack11l1ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧῇ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠤࡤࡦࡴࡸࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡼࡿࠥῈ").format(os.getenv(bstack11l1ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣΈ")))))
    @staticmethod
    def bstack1lllllllll1l_opy_(test_name: str):
        bstack11l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣῊ")
        bstack11111l1ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࢀࢃ࠮ࡵࡺࡷࠦΉ").format(os.getenv(bstack11l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦῌ"))))
        with open(bstack11111l1ll11_opy_, bstack11l1ll1_opy_ (u"ࠧࡢࠩ῍")) as file:
            file.write(bstack11l1ll1_opy_ (u"ࠣࡽࢀࡠࡳࠨ῎").format(test_name))
    @staticmethod
    def bstack111111lll11_opy_(framework: str) -> bool:
       return framework.lower() in bstack1111111ll1l_opy_
    @staticmethod
    def bstack111lll1ll11_opy_(config: dict) -> bool:
        bstack1llllllllll1_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭῏"), {}).get(bstack111111111l1_opy_, {})
        return bstack1llllllllll1_opy_.get(bstack11l1ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫῐ"), False)
    @staticmethod
    def bstack111lllll11l_opy_(config: dict, bstack111llllllll_opy_: int = 0) -> int:
        bstack11l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡉࡨࡸࠥࡺࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠲ࠠࡸࡪ࡬ࡧ࡭ࠦࡣࡢࡰࠣࡦࡪࠦࡡ࡯ࠢࡤࡦࡸࡵ࡬ࡶࡶࡨࠤࡳࡻ࡭ࡣࡧࡵࠤࡴࡸࠠࡢࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࠮ࡤࡪࡥࡷ࠭࠿ࠦࡔࡩࡧࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡰࡶࡤࡰࡤࡺࡥࡴࡶࡶࠤ࠭࡯࡮ࡵࠫ࠽ࠤ࡙࡮ࡥࠡࡶࡲࡸࡦࡲࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࠫࡶࡪࡷࡵࡪࡴࡨࡨࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠳ࡢࡢࡵࡨࡨࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࡴࠫ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵ࠼ࠣࡘ࡭࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤῑ")
        bstack1llllllllll1_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩῒ"), {}).get(bstack11l1ll1_opy_ (u"࠭ࡡࡣࡱࡵࡸࡇࡻࡩ࡭ࡦࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠬΐ"), {})
        bstack111111ll1ll_opy_ = 0
        bstack111111ll1l1_opy_ = 0
        if bstack11111l1l_opy_.bstack111lll1ll11_opy_(config):
            bstack111111ll1l1_opy_ = bstack1llllllllll1_opy_.get(bstack11l1ll1_opy_ (u"ࠧ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷࠬ῔"), 5)
            if isinstance(bstack111111ll1l1_opy_, str) and bstack111111ll1l1_opy_.endswith(bstack11l1ll1_opy_ (u"ࠨࠧࠪ῕")):
                try:
                    percentage = int(bstack111111ll1l1_opy_.strip(bstack11l1ll1_opy_ (u"ࠩࠨࠫῖ")))
                    if bstack111llllllll_opy_ > 0:
                        bstack111111ll1ll_opy_ = math.ceil((percentage * bstack111llllllll_opy_) / 100)
                    else:
                        raise ValueError(bstack11l1ll1_opy_ (u"ࠥࡘࡴࡺࡡ࡭ࠢࡷࡩࡸࡺࡳࠡ࡯ࡸࡷࡹࠦࡢࡦࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤ࡫ࡵࡲࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠲ࡨࡡࡴࡧࡧࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࡳ࠯ࠤῗ"))
                except ValueError as e:
                    raise ValueError(bstack11l1ll1_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦࠢࡹࡥࡱࡻࡥࠡࡨࡲࡶࠥࡳࡡࡹࡈࡤ࡭ࡱࡻࡲࡦࡵ࠽ࠤࢀࢃࠢῘ").format(bstack111111ll1l1_opy_)) from e
            else:
                bstack111111ll1ll_opy_ = int(bstack111111ll1l1_opy_)
        logger.info(bstack11l1ll1_opy_ (u"ࠧࡓࡡࡹࠢࡩࡥ࡮ࡲࡵࡳࡧࡶࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡴࡧࡷࠤࡹࡵ࠺ࠡࡽࢀࠤ࠭࡬ࡲࡰ࡯ࠣࡧࡴࡴࡦࡪࡩ࠽ࠤࢀࢃࠩࠣῙ").format(bstack111111ll1ll_opy_, bstack111111ll1l1_opy_))
        return bstack111111ll1ll_opy_
    def bstack1111111l11l_opy_(self):
        return self.bstack11111l11l11_opy_
    def bstack111111l1l11_opy_(self):
        return self.bstack11111l1l11l_opy_
    def bstack11111l111l1_opy_(self):
        return self.bstack11111l11l1l_opy_
    def __111111ll11l_opy_(self, enabled, mode, source=None):
        try:
            self.bstack11111l11l11_opy_ = bool(enabled)
            if mode not in [bstack11l1ll1_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭Ὶ"), bstack11l1ll1_opy_ (u"ࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡑࡱࡰࡾ࠭Ί")]:
                logger.warning(bstack11l1ll1_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡶࡱࡦࡸࡴࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤࡲࡵࡤࡦࠢࠪࡿࢂ࠭ࠠࡱࡴࡲࡺ࡮ࡪࡥࡥ࠰ࠣࡈࡪ࡬ࡡࡶ࡮ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡌࡩࡳࡵࡷࠫ࠳ࠨ῜").format(mode))
                mode = bstack11l1ll1_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡊ࡮ࡸࡳࡵࠩ῝")
            self.bstack11111l1l11l_opy_ = mode
            self.bstack11111l11l1l_opy_ = []
            if source is None:
                self.bstack11111l11l1l_opy_ = None
            elif isinstance(source, list):
                self.bstack11111l11l1l_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack11l1ll1_opy_ (u"ࠪ࠲࡯ࡹ࡯࡯ࠩ῞")):
                self.bstack11111l11l1l_opy_ = self._1111111llll_opy_(source)
            self.__11111l11111_opy_()
        except Exception as e:
            logger.error(bstack11l1ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸࡳࡡࡳࡶࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦ࠭ࠡࡧࡱࡥࡧࡲࡥࡥ࠼ࠣࡿࢂ࠲ࠠ࡮ࡱࡧࡩ࠿ࠦࡻࡾ࠮ࠣࡷࡴࡻࡲࡤࡧ࠽ࠤࢀࢃ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ῟").format(enabled, mode, source, e))
    def bstack11111l1ll1l_opy_(self):
        return self.bstack111111111ll_opy_
    def __1111111l111_opy_(self, value):
        self.bstack111111111ll_opy_ = bool(value)
        self.__11111l11111_opy_()
    def bstack11111l11ll1_opy_(self):
        return self.bstack111111l1111_opy_
    def __111111l1ll1_opy_(self, value):
        self.bstack111111l1111_opy_ = bool(value)
        self.__11111l11111_opy_()
    def bstack111111l1l1l_opy_(self):
        return self.bstack1lllllllll11_opy_
    def __111111l1lll_opy_(self, value):
        self.bstack1lllllllll11_opy_ = bool(value)
        self.__11111l11111_opy_()
    def __11111l11111_opy_(self):
        if self.bstack11111l11l11_opy_:
            self.bstack111111111ll_opy_ = False
            self.bstack111111l1111_opy_ = False
            self.bstack1lllllllll11_opy_ = False
            self.bstack11111111111_opy_.enable(bstack11111l1l1ll_opy_)
        elif self.bstack111111111ll_opy_:
            self.bstack111111l1111_opy_ = False
            self.bstack1lllllllll11_opy_ = False
            self.bstack11111l11l11_opy_ = False
            self.bstack11111111111_opy_.enable(bstack11111l1l1l1_opy_)
        elif self.bstack111111l1111_opy_:
            self.bstack111111111ll_opy_ = False
            self.bstack1lllllllll11_opy_ = False
            self.bstack11111l11l11_opy_ = False
            self.bstack11111111111_opy_.enable(bstack11111l11lll_opy_)
        elif self.bstack1lllllllll11_opy_:
            self.bstack111111111ll_opy_ = False
            self.bstack111111l1111_opy_ = False
            self.bstack11111l11l11_opy_ = False
            self.bstack11111111111_opy_.enable(bstack1lllllllllll_opy_)
        else:
            self.bstack11111111111_opy_.disable()
    def bstack1ll11l1lll_opy_(self):
        return self.bstack11111111111_opy_.bstack11111111l1l_opy_()
    def bstack11llll1ll_opy_(self):
        if self.bstack11111111111_opy_.bstack11111111l1l_opy_():
            return self.bstack11111111111_opy_.get_name()
        return None
    def _1111111llll_opy_(self, bstack11111l1llll_opy_):
        bstack11l1ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡳࡰࡷࡵࡧࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠤࡦࡴࡤࠡࡨࡲࡶࡲࡧࡴࠡ࡫ࡷࠤ࡫ࡵࡲࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡶࡳࡺࡸࡣࡦࡡࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠥ࠮ࡳࡵࡴࠬ࠾ࠥࡖࡡࡵࡪࠣࡸࡴࠦࡴࡩࡧࠣࡎࡘࡕࡎࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࡭࡫ࡶࡸ࠿ࠦࡆࡰࡴࡰࡥࡹࡺࡥࡥࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡶࡪࡶ࡯ࡴ࡫ࡷࡳࡷࡿࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧῠ")
        if not os.path.isfile(bstack11111l1llll_opy_):
            logger.error(bstack11l1ll1_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡦࡪ࡮ࡨࠤࠬࢁࡽࠨࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠱ࠦῡ").format(bstack11111l1llll_opy_))
            return []
        data = None
        try:
            with open(bstack11111l1llll_opy_, bstack11l1ll1_opy_ (u"ࠢࡳࠤῢ")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack11l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡌࡖࡓࡓࠦࡦࡳࡱࡰࠤࡸࡵࡵࡳࡥࡨࠤ࡫࡯࡬ࡦࠢࠪࡿࢂ࠭࠺ࠡࡽࢀࠦΰ").format(bstack11111l1llll_opy_, e))
            return []
        _11111111lll_opy_ = None
        _1llllllll1l1_opy_ = None
        def _111111l111l_opy_():
            bstack1111111ll11_opy_ = {}
            bstack111111l11ll_opy_ = {}
            try:
                if self.bstack1lllllll1lll_opy_.startswith(bstack11l1ll1_opy_ (u"ࠩࡾࠫῤ")) and self.bstack1lllllll1lll_opy_.endswith(bstack11l1ll1_opy_ (u"ࠪࢁࠬῥ")):
                    bstack1111111ll11_opy_ = json.loads(self.bstack1lllllll1lll_opy_)
                else:
                    bstack1111111ll11_opy_ = dict(item.split(bstack11l1ll1_opy_ (u"ࠫ࠿࠭ῦ")) for item in self.bstack1lllllll1lll_opy_.split(bstack11l1ll1_opy_ (u"ࠬ࠲ࠧῧ")) if bstack11l1ll1_opy_ (u"࠭࠺ࠨῨ") in item) if self.bstack1lllllll1lll_opy_ else {}
                if self.bstack11111111l11_opy_.startswith(bstack11l1ll1_opy_ (u"ࠧࡼࠩῩ")) and self.bstack11111111l11_opy_.endswith(bstack11l1ll1_opy_ (u"ࠨࡿࠪῪ")):
                    bstack111111l11ll_opy_ = json.loads(self.bstack11111111l11_opy_)
                else:
                    bstack111111l11ll_opy_ = dict(item.split(bstack11l1ll1_opy_ (u"ࠩ࠽ࠫΎ")) for item in self.bstack11111111l11_opy_.split(bstack11l1ll1_opy_ (u"ࠪ࠰ࠬῬ")) if bstack11l1ll1_opy_ (u"ࠫ࠿࠭῭") in item) if self.bstack11111111l11_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack11l1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥ࡬ࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࡳ࠻ࠢࡾࢁࠧ΅").format(e))
            logger.debug(bstack11l1ll1_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠ࡮ࡣࡳࡴ࡮ࡴࡧࡴࠢࡩࡶࡴࡳࠠࡦࡰࡹ࠾ࠥࢁࡽ࠭ࠢࡆࡐࡎࡀࠠࡼࡿࠥ`").format(bstack1111111ll11_opy_, bstack111111l11ll_opy_))
            return bstack1111111ll11_opy_, bstack111111l11ll_opy_
        if _11111111lll_opy_ is None or _1llllllll1l1_opy_ is None:
            _11111111lll_opy_, _1llllllll1l1_opy_ = _111111l111l_opy_()
        def bstack1111111111l_opy_(name, bstack11111111ll1_opy_):
            if name in _1llllllll1l1_opy_:
                return _1llllllll1l1_opy_[name]
            if name in _11111111lll_opy_:
                return _11111111lll_opy_[name]
            if bstack11111111ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧ῰")):
                return bstack11111111ll1_opy_[bstack11l1ll1_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ῱")]
            return None
        if isinstance(data, dict):
            bstack11111l1111l_opy_ = []
            bstack111111l11l1_opy_ = re.compile(bstack11l1ll1_opy_ (u"ࡴࠪࡢࡠࡇ࡛࠭࠲࠰࠽ࡤࡣࠫࠥࠩῲ"))
            for name, bstack11111111ll1_opy_ in data.items():
                if not isinstance(bstack11111111ll1_opy_, dict):
                    continue
                url = bstack11111111ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠪࡹࡷࡲࠧῳ"))
                if url is None or (isinstance(url, str) and url.strip() == bstack11l1ll1_opy_ (u"ࠫࠬῴ")):
                    logger.warning(bstack11l1ll1_opy_ (u"ࠧࡘࡥࡱࡱࡶ࡭ࡹࡵࡲࡺࠢࡘࡖࡑࠦࡩࡴࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ῵").format(name, bstack11111111ll1_opy_))
                    continue
                if not bstack111111l11l1_opy_.match(name):
                    logger.warning(bstack11l1ll1_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡱࡸࡶࡨ࡫ࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤ࡫ࡵࡲ࡮ࡣࡷࠤ࡫ࡵࡲࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥῶ").format(name, bstack11111111ll1_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack11l1ll1_opy_ (u"ࠢࡔࡱࡸࡶࡨ࡫ࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤࠬࢁࡽࠨࠢࡰࡹࡸࡺࠠࡩࡣࡹࡩࠥࡧࠠ࡭ࡧࡱ࡫ࡹ࡮ࠠࡣࡧࡷࡻࡪ࡫࡮ࠡ࠳ࠣࡥࡳࡪࠠ࠴࠲ࠣࡧ࡭ࡧࡲࡢࡥࡷࡩࡷࡹ࠮ࠣῷ").format(name))
                    continue
                bstack11111111ll1_opy_ = bstack11111111ll1_opy_.copy()
                bstack11111111ll1_opy_[bstack11l1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ὸ")] = name
                bstack11111111ll1_opy_[bstack11l1ll1_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩΌ")] = bstack1111111111l_opy_(name, bstack11111111ll1_opy_)
                if not bstack11111111ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪῺ")) or bstack11111111ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫΏ")) == bstack11l1ll1_opy_ (u"ࠬ࠭ῼ"):
                    logger.warning(bstack11l1ll1_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠ࡯ࡱࡷࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡪࡪࠠࡧࡱࡵࠤࡸࡵࡵࡳࡥࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ´").format(name, bstack11111111ll1_opy_))
                    continue
                if bstack11111111ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡣࡣࡶࡩࡇࡸࡡ࡯ࡥ࡫ࠫ῾")) and bstack11111111ll1_opy_[bstack11l1ll1_opy_ (u"ࠨࡤࡤࡷࡪࡈࡲࡢࡰࡦ࡬ࠬ῿")] == bstack11111111ll1_opy_[bstack11l1ll1_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ ")]:
                    logger.warning(bstack11l1ll1_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡦࡴࡤࠡࡤࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡣࡢࡰࡱࡳࡹࠦࡢࡦࠢࡷ࡬ࡪࠦࡳࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡵࡲࡹࡷࡩࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥ ").format(name, bstack11111111ll1_opy_))
                    continue
                bstack11111l1111l_opy_.append(bstack11111111ll1_opy_)
            return bstack11111l1111l_opy_
        return data
    def bstack11111ll1ll1_opy_(self):
        data = {
            bstack11l1ll1_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪ "): {
                bstack11l1ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ "): self.bstack1111111l11l_opy_(),
                bstack11l1ll1_opy_ (u"࠭࡭ࡰࡦࡨࠫ "): self.bstack111111l1l11_opy_(),
                bstack11l1ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ "): self.bstack11111l111l1_opy_()
            }
        }
        return data
    def bstack1111111l1l1_opy_(self, config):
        bstack1111111l1ll_opy_ = {}
        bstack1111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ ")] = {
            bstack11l1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ "): self.bstack1111111l11l_opy_(),
            bstack11l1ll1_opy_ (u"ࠪࡱࡴࡪࡥࠨ "): self.bstack111111l1l11_opy_()
        }
        bstack1111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡴࡷ࡫ࡶࡪࡱࡸࡷࡱࡿ࡟ࡧࡣ࡬ࡰࡪࡪࠧ ")] = {
            bstack11l1ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ "): self.bstack11111l11ll1_opy_()
        }
        bstack1111111l1ll_opy_[bstack11l1ll1_opy_ (u"࠭ࡲࡶࡰࡢࡴࡷ࡫ࡶࡪࡱࡸࡷࡱࡿ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡧ࡫ࡵࡷࡹ࠭​")] = {
            bstack11l1ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ‌"): self.bstack11111l1ll1l_opy_()
        }
        bstack1111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡦࡢ࡫࡯࡭ࡳ࡭࡟ࡢࡰࡧࡣ࡫ࡲࡡ࡬ࡻࠪ‍")] = {
            bstack11l1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ‎"): self.bstack111111l1l1l_opy_()
        }
        if self.bstack1lll1l1l_opy_(config):
            bstack1111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠪࡶࡪࡺࡲࡺࡡࡷࡩࡸࡺࡳࡠࡱࡱࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠬ‏")] = {
                bstack11l1ll1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ‐"): True,
                bstack11l1ll1_opy_ (u"ࠬࡳࡡࡹࡡࡵࡩࡹࡸࡩࡦࡵࠪ‑"): self.bstack11ll1ll1l1_opy_(config)
            }
        if self.bstack111lll1ll11_opy_(config):
            bstack1111111l1ll_opy_[bstack11l1ll1_opy_ (u"࠭ࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࡴࡴ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠨ‒")] = {
                bstack11l1ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ–"): True,
                bstack11l1ll1_opy_ (u"ࠨ࡯ࡤࡼࡤ࡬ࡡࡪ࡮ࡸࡶࡪࡹࠧ—"): self.bstack111lllll11l_opy_(config)
            }
        return bstack1111111l1ll_opy_
    def bstack11llll1111_opy_(self, config):
        bstack11l1ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡰ࡮࡯ࡩࡨࡺࡳࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡨࡹࠡ࡯ࡤ࡯࡮ࡴࡧࠡࡣࠣࡧࡦࡲ࡬ࠡࡶࡲࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠤ࠭ࡹࡴࡳࠫ࠽ࠤ࡙࡮ࡥࠡࡗࡘࡍࡉࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡢࡶ࡫࡯ࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡧࡥࡹࡧࠠࡧࡱࡵ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠠࡦࡰࡧࡴࡴ࡯࡮ࡵ࠮ࠣࡳࡷࠦࡎࡰࡰࡨࠤ࡮࡬ࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ―")
        if not (config.get(bstack11l1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭‖"), None) in bstack11l1111l1ll_opy_ and self.bstack1111111l11l_opy_()):
            return None
        bstack1llllllll1ll_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ‗"), None)
        logger.debug(bstack11l1ll1_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈ࠿ࠦࡻࡾࠤ‘").format(bstack1llllllll1ll_opy_))
        try:
            bstack11l11lllll1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠦ’").format(bstack1llllllll1ll_opy_)
            payload = {
                bstack11l1ll1_opy_ (u"ࠢࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠧ‚"): config.get(bstack11l1ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭‛"), bstack11l1ll1_opy_ (u"ࠩࠪ“")),
                bstack11l1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠨ”"): config.get(bstack11l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ„"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11l1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ‟"): os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠧ†"), bstack11l1ll1_opy_ (u"ࠢࠣ‡")),
                bstack11l1ll1_opy_ (u"ࠣࡰࡲࡨࡪࡏ࡮ࡥࡧࡻࠦ•"): int(os.environ.get(bstack11l1ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧ‣")) or bstack11l1ll1_opy_ (u"ࠥ࠴ࠧ․")),
                bstack11l1ll1_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࡑࡳࡩ࡫ࡳࠣ‥"): int(os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢ…")) or bstack11l1ll1_opy_ (u"ࠨ࠱ࠣ‧")),
                bstack11l1ll1_opy_ (u"ࠢࡩࡱࡶࡸࡎࡴࡦࡰࠤ "): get_host_info(),
            }
            logger.debug(bstack11l1ll1_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤࡵࡧࡹ࡭ࡱࡤࡨ࠿ࠦࡻࡾࠤ ").format(payload))
            response = bstack11l11lll1l1_opy_.bstack11111l111ll_opy_(bstack11l11lllll1_opy_, payload)
            if response:
                logger.debug(bstack11l1ll1_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡃࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ‪").format(response))
                return response
            else:
                logger.error(bstack11l1ll1_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡢࡶ࡫࡯ࡨ࡛ࠥࡕࡊࡆ࠽ࠤࢀࢃࠢ‫").format(bstack1llllllll1ll_opy_))
                return None
        except Exception as e:
            logger.error(bstack11l1ll1_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡢࡶ࡫࡯ࡨ࡛ࠥࡕࡊࡆࠣࡿࢂࡀࠠࡼࡿࠥ‬").format(bstack1llllllll1ll_opy_, e))
            return None