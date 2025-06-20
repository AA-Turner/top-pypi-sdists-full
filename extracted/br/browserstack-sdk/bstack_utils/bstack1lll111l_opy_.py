# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1111l1ll1_opy_
from bstack_utils.constants import bstack11ll11ll_opy_
bstack111l1l111ll_opy_ = bstack11ll11_opy_ (u"ࠨࡲࡦࡶࡵࡽ࡙࡫ࡳࡵࡵࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠧᶜ")
bstack111l1l1ll1l_opy_ = bstack11ll11_opy_ (u"ࠢࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨᶝ")
bstack111l1ll11ll_opy_ = bstack11ll11_opy_ (u"ࠣࡴࡸࡲࡕࡸࡥࡷ࡫ࡲࡹࡸࡲࡹࡇࡣ࡬ࡰࡪࡪࡆࡪࡴࡶࡸࠧᶞ")
bstack111l1ll111l_opy_ = bstack11ll11_opy_ (u"ࠤࡵࡩࡷࡻ࡮ࡑࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡊࡦ࡯࡬ࡦࡦࠥᶟ")
bstack111l1l11ll1_opy_ = bstack11ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡇ࡮ࡤ࡯ࡾࡧ࡮ࡥࡈࡤ࡭ࡱ࡫ࡤࠣᶠ")
bstack111l1l11l1l_opy_ = {
    bstack111l1l111ll_opy_,
    bstack111l1l1ll1l_opy_,
    bstack111l1ll11ll_opy_,
    bstack111l1ll111l_opy_,
    bstack111l1l11ll1_opy_,
}
bstack111l11ll1l1_opy_ = {bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᶡ")}
logger = bstack1111l1ll1_opy_.get_logger(__name__, bstack11ll11ll_opy_)
class bstack111l11ll111_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack111l1l1llll_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack111l11l1l_opy_:
    _1lll11l1111_opy_ = None
    def __init__(self, config):
        self.bstack111l1l1l1l1_opy_ = False
        self.bstack111l11ll1ll_opy_ = False
        self.bstack111l1l1ll11_opy_ = False
        self.bstack111l1l1l1ll_opy_ = bstack111l11ll111_opy_()
        opts = config.get(bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᶢ"), {})
        self.__111l11l1lll_opy_(opts.get(bstack111l1ll11ll_opy_, False))
        self.__111l1l1lll1_opy_(opts.get(bstack111l1ll111l_opy_, False))
        self.__111l1l1l11l_opy_(opts.get(bstack111l1l11ll1_opy_, False))
    @classmethod
    def bstack1lll11ll_opy_(cls, config=None):
        if cls._1lll11l1111_opy_ is None and config is not None:
            cls._1lll11l1111_opy_ = bstack111l11l1l_opy_(config)
        return cls._1lll11l1111_opy_
    @staticmethod
    def bstack1llll1ll11_opy_(config: dict) -> bool:
        bstack111l11lll1l_opy_ = config.get(bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᶣ"), {}).get(bstack111l1l111ll_opy_, {})
        return bstack111l11lll1l_opy_.get(bstack11ll11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨᶤ"), False)
    @staticmethod
    def bstack11ll1llll_opy_(config: dict) -> int:
        bstack111l11lll1l_opy_ = config.get(bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᶥ"), {}).get(bstack111l1l111ll_opy_, {})
        retries = 0
        if bstack111l11l1l_opy_.bstack1llll1ll11_opy_(config):
            retries = bstack111l11lll1l_opy_.get(bstack11ll11_opy_ (u"ࠩࡰࡥࡽࡘࡥࡵࡴ࡬ࡩࡸ࠭ᶦ"), 1)
        return retries
    @staticmethod
    def bstack111ll1ll_opy_(config: dict) -> dict:
        bstack111l1l11111_opy_ = config.get(bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧᶧ"), {})
        return {
            key: value for key, value in bstack111l1l11111_opy_.items() if key in bstack111l1l11l1l_opy_
        }
    @staticmethod
    def bstack111l11lllll_opy_():
        bstack11ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᶨ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠧࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡿࢂࠨᶩ").format(os.getenv(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦᶪ")))))
    @staticmethod
    def bstack111l1l111l1_opy_(test_name: str):
        bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᶫ")
        bstack111l1l11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡼࡿ࠱ࡸࡽࡺࠢᶬ").format(os.getenv(bstack11ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢᶭ"))))
        with open(bstack111l1l11lll_opy_, bstack11ll11_opy_ (u"ࠪࡥࠬᶮ")) as file:
            file.write(bstack11ll11_opy_ (u"ࠦࢀࢃ࡜࡯ࠤᶯ").format(test_name))
    @staticmethod
    def bstack111l11llll1_opy_(framework: str) -> bool:
       return framework.lower() in bstack111l11ll1l1_opy_
    @staticmethod
    def bstack11l1l1lll11_opy_(config: dict) -> bool:
        bstack111l11lll11_opy_ = config.get(bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᶰ"), {}).get(bstack111l1l1ll1l_opy_, {})
        return bstack111l11lll11_opy_.get(bstack11ll11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧᶱ"), False)
    @staticmethod
    def bstack11l1ll11lll_opy_(config: dict, bstack11l1l1ll111_opy_: int = 0) -> int:
        bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥ࠮ࠣࡻ࡭࡯ࡣࡩࠢࡦࡥࡳࠦࡢࡦࠢࡤࡲࠥࡧࡢࡴࡱ࡯ࡹࡹ࡫ࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡴࠣࡥࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧࠡࠪࡧ࡭ࡨࡺࠩ࠻ࠢࡗ࡬ࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡳࡹࡧ࡬ࡠࡶࡨࡷࡹࡹࠠࠩ࡫ࡱࡸ࠮ࡀࠠࡕࡪࡨࠤࡹࡵࡴࡢ࡮ࠣࡲࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥ࠮ࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠮࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸ࠿ࠦࡔࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᶲ")
        bstack111l11lll11_opy_ = config.get(bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᶳ"), {}).get(bstack11ll11_opy_ (u"ࠩࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠨᶴ"), {})
        bstack111l11ll11l_opy_ = 0
        bstack111l1l11l11_opy_ = 0
        if bstack111l11l1l_opy_.bstack11l1l1lll11_opy_(config):
            bstack111l1l11l11_opy_ = bstack111l11lll11_opy_.get(bstack11ll11_opy_ (u"ࠪࡱࡦࡾࡆࡢ࡫࡯ࡹࡷ࡫ࡳࠨᶵ"), 5)
            if isinstance(bstack111l1l11l11_opy_, str) and bstack111l1l11l11_opy_.endswith(bstack11ll11_opy_ (u"ࠫࠪ࠭ᶶ")):
                try:
                    percentage = int(bstack111l1l11l11_opy_.strip(bstack11ll11_opy_ (u"ࠬࠫࠧᶷ")))
                    if bstack11l1l1ll111_opy_ > 0:
                        bstack111l11ll11l_opy_ = math.ceil((percentage * bstack11l1l1ll111_opy_) / 100)
                    else:
                        raise ValueError(bstack11ll11_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡲࡻࡳࡵࠢࡥࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠲ࠧᶸ"))
                except ValueError as e:
                    raise ValueError(bstack11ll11_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡵࡲࠡ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸࡀࠠࡼࡿࠥᶹ").format(bstack111l1l11l11_opy_)) from e
            else:
                bstack111l11ll11l_opy_ = int(bstack111l1l11l11_opy_)
        logger.info(bstack11ll11_opy_ (u"ࠣࡏࡤࡼࠥ࡬ࡡࡪ࡮ࡸࡶࡪࡹࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡷࡪࡺࠠࡵࡱ࠽ࠤࢀࢃࠠࠩࡨࡵࡳࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿࠬࠦᶺ").format(bstack111l11ll11l_opy_, bstack111l1l11l11_opy_))
        return bstack111l11ll11l_opy_
    def bstack111l1l1l111_opy_(self):
        return self.bstack111l1l1l1l1_opy_
    def __111l11l1lll_opy_(self, value):
        self.bstack111l1l1l1l1_opy_ = bool(value)
        self.__111l1ll11l1_opy_()
    def bstack111l1l1111l_opy_(self):
        return self.bstack111l11ll1ll_opy_
    def __111l1l1lll1_opy_(self, value):
        self.bstack111l11ll1ll_opy_ = bool(value)
        self.__111l1ll11l1_opy_()
    def bstack111l1ll1111_opy_(self):
        return self.bstack111l1l1ll11_opy_
    def __111l1l1l11l_opy_(self, value):
        self.bstack111l1l1ll11_opy_ = bool(value)
        self.__111l1ll11l1_opy_()
    def __111l1ll11l1_opy_(self):
        if self.bstack111l1l1l1l1_opy_:
            self.bstack111l11ll1ll_opy_ = False
            self.bstack111l1l1ll11_opy_ = False
            self.bstack111l1l1l1ll_opy_.enable(bstack111l1ll11ll_opy_)
        elif self.bstack111l11ll1ll_opy_:
            self.bstack111l1l1l1l1_opy_ = False
            self.bstack111l1l1ll11_opy_ = False
            self.bstack111l1l1l1ll_opy_.enable(bstack111l1ll111l_opy_)
        elif self.bstack111l1l1ll11_opy_:
            self.bstack111l1l1l1l1_opy_ = False
            self.bstack111l11ll1ll_opy_ = False
            self.bstack111l1l1l1ll_opy_.enable(bstack111l1l11ll1_opy_)
        else:
            self.bstack111l1l1l1ll_opy_.disable()
    def bstack1111111l1_opy_(self):
        return self.bstack111l1l1l1ll_opy_.bstack111l1l1llll_opy_()
    def bstack1l1ll1l11_opy_(self):
        if self.bstack111l1l1l1ll_opy_.bstack111l1l1llll_opy_():
            return self.bstack111l1l1l1ll_opy_.get_name()
        return None