# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1llll1l111_opy_
from bstack_utils.constants import bstack1ll1ll1l_opy_
bstack111l1l11l11_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡷࡶࡾ࡚ࡥࡴࡶࡶࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨᶝ")
bstack111l11ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢᶞ")
bstack111l1l111ll_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࡇ࡫ࡵࡷࡹࠨᶟ")
bstack111l11lll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡶࡪࡸࡵ࡯ࡒࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡋࡧࡩ࡭ࡧࡧࠦᶠ")
bstack111l11ll11l_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡸࡱࡩࡱࡈ࡯ࡥࡰࡿࡡ࡯ࡦࡉࡥ࡮ࡲࡥࡥࠤᶡ")
bstack111l11ll1l1_opy_ = {
    bstack111l1l11l11_opy_,
    bstack111l11ll111_opy_,
    bstack111l1l111ll_opy_,
    bstack111l11lll1l_opy_,
    bstack111l11ll11l_opy_,
}
bstack111l1l1l1l1_opy_ = {bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᶢ")}
logger = bstack1llll1l111_opy_.get_logger(__name__, bstack1ll1ll1l_opy_)
class bstack111l11l1lll_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack111l1l111l1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1ll11111l_opy_:
    _1lll1111l1l_opy_ = None
    def __init__(self, config):
        self.bstack111l1l1lll1_opy_ = False
        self.bstack111l11lll11_opy_ = False
        self.bstack111l1ll1111_opy_ = False
        self.bstack111l11lllll_opy_ = bstack111l11l1lll_opy_()
        opts = config.get(bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᶣ"), {})
        self.__111l1l1llll_opy_(opts.get(bstack111l1l111ll_opy_, False))
        self.__111l1l1111l_opy_(opts.get(bstack111l11lll1l_opy_, False))
        self.__111l1l1l111_opy_(opts.get(bstack111l11ll11l_opy_, False))
    @classmethod
    def bstack1ll11lll_opy_(cls, config=None):
        if cls._1lll1111l1l_opy_ is None and config is not None:
            cls._1lll1111l1l_opy_ = bstack1ll11111l_opy_(config)
        return cls._1lll1111l1l_opy_
    @staticmethod
    def bstack1ll11l11l1_opy_(config: dict) -> bool:
        bstack111l1l1l11l_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫᶤ"), {}).get(bstack111l1l11l11_opy_, {})
        return bstack111l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩᶥ"), False)
    @staticmethod
    def bstack1l11ll1l1l_opy_(config: dict) -> int:
        bstack111l1l1l11l_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ᶦ"), {}).get(bstack111l1l11l11_opy_, {})
        retries = 0
        if bstack1ll11111l_opy_.bstack1ll11l11l1_opy_(config):
            retries = bstack111l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠪࡱࡦࡾࡒࡦࡶࡵ࡭ࡪࡹࠧᶧ"), 1)
        return retries
    @staticmethod
    def bstack1l11l11l_opy_(config: dict) -> dict:
        bstack111l1l11lll_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᶨ"), {})
        return {
            key: value for key, value in bstack111l1l11lll_opy_.items() if key in bstack111l11ll1l1_opy_
        }
    @staticmethod
    def bstack111l11llll1_opy_():
        bstack1l1l1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᶩ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃࠢᶪ").format(os.getenv(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧᶫ")))))
    @staticmethod
    def bstack111l11ll1ll_opy_(test_name: str):
        bstack1l1l1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᶬ")
        bstack111l1l1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣᶭ").format(os.getenv(bstack1l1l1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣᶮ"))))
        with open(bstack111l1l1ll1l_opy_, bstack1l1l1l1_opy_ (u"ࠫࡦ࠭ᶯ")) as file:
            file.write(bstack1l1l1l1_opy_ (u"ࠧࢁࡽ࡝ࡰࠥᶰ").format(test_name))
    @staticmethod
    def bstack111l1l11l1l_opy_(framework: str) -> bool:
       return framework.lower() in bstack111l1l1l1l1_opy_
    @staticmethod
    def bstack11l1l1lll1l_opy_(config: dict) -> bool:
        bstack111l1l1ll11_opy_ = config.get(bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᶱ"), {}).get(bstack111l11ll111_opy_, {})
        return bstack111l1l1ll11_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨᶲ"), False)
    @staticmethod
    def bstack11l1l1ll111_opy_(config: dict, bstack11l1l1l1l11_opy_: int = 0) -> int:
        bstack1l1l1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠯ࠤࡼ࡮ࡩࡤࡪࠣࡧࡦࡴࠠࡣࡧࠣࡥࡳࠦࡡࡣࡵࡲࡰࡺࡺࡥࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡵࠤࡦࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡴࡺࡡ࡭ࡡࡷࡩࡸࡺࡳࠡࠪ࡬ࡲࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࠨࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡩࡳࡷࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠰ࡦࡦࡹࡥࡥࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࡸ࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᶳ")
        bstack111l1l1ll11_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ᶴ"), {}).get(bstack1l1l1l1_opy_ (u"ࠪࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠩᶵ"), {})
        bstack111l1ll11l1_opy_ = 0
        bstack111l1l11111_opy_ = 0
        if bstack1ll11111l_opy_.bstack11l1l1lll1l_opy_(config):
            bstack111l1l11111_opy_ = bstack111l1l1ll11_opy_.get(bstack1l1l1l1_opy_ (u"ࠫࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴࠩᶶ"), 5)
            if isinstance(bstack111l1l11111_opy_, str) and bstack111l1l11111_opy_.endswith(bstack1l1l1l1_opy_ (u"ࠬࠫࠧᶷ")):
                try:
                    percentage = int(bstack111l1l11111_opy_.strip(bstack1l1l1l1_opy_ (u"࠭ࠥࠨᶸ")))
                    if bstack11l1l1l1l11_opy_ > 0:
                        bstack111l1ll11l1_opy_ = math.ceil((percentage * bstack11l1l1l1l11_opy_) / 100)
                    else:
                        raise ValueError(bstack1l1l1l1_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡳࡵࡴࡶࠣࡦࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠳ࠨᶹ"))
                except ValueError as e:
                    raise ValueError(bstack1l1l1l1_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪࠦࡶࡢ࡮ࡸࡩࠥ࡬࡯ࡳࠢࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹ࠺ࠡࡽࢀࠦᶺ").format(bstack111l1l11111_opy_)) from e
            else:
                bstack111l1ll11l1_opy_ = int(bstack111l1l11111_opy_)
        logger.info(bstack1l1l1l1_opy_ (u"ࠤࡐࡥࡽࠦࡦࡢ࡫࡯ࡹࡷ࡫ࡳࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡸ࡫ࡴࠡࡶࡲ࠾ࠥࢁࡽࠡࠪࡩࡶࡴࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡽࢀ࠭ࠧᶻ").format(bstack111l1ll11l1_opy_, bstack111l1l11111_opy_))
        return bstack111l1ll11l1_opy_
    def bstack111l1l1l1ll_opy_(self):
        return self.bstack111l1l1lll1_opy_
    def __111l1l1llll_opy_(self, value):
        self.bstack111l1l1lll1_opy_ = bool(value)
        self.__111l1ll111l_opy_()
    def bstack111l1ll11ll_opy_(self):
        return self.bstack111l11lll11_opy_
    def __111l1l1111l_opy_(self, value):
        self.bstack111l11lll11_opy_ = bool(value)
        self.__111l1ll111l_opy_()
    def bstack111l1l11ll1_opy_(self):
        return self.bstack111l1ll1111_opy_
    def __111l1l1l111_opy_(self, value):
        self.bstack111l1ll1111_opy_ = bool(value)
        self.__111l1ll111l_opy_()
    def __111l1ll111l_opy_(self):
        if self.bstack111l1l1lll1_opy_:
            self.bstack111l11lll11_opy_ = False
            self.bstack111l1ll1111_opy_ = False
            self.bstack111l11lllll_opy_.enable(bstack111l1l111ll_opy_)
        elif self.bstack111l11lll11_opy_:
            self.bstack111l1l1lll1_opy_ = False
            self.bstack111l1ll1111_opy_ = False
            self.bstack111l11lllll_opy_.enable(bstack111l11lll1l_opy_)
        elif self.bstack111l1ll1111_opy_:
            self.bstack111l1l1lll1_opy_ = False
            self.bstack111l11lll11_opy_ = False
            self.bstack111l11lllll_opy_.enable(bstack111l11ll11l_opy_)
        else:
            self.bstack111l11lllll_opy_.disable()
    def bstack1ll1111l_opy_(self):
        return self.bstack111l11lllll_opy_.bstack111l1l111l1_opy_()
    def bstack1l1111llll_opy_(self):
        if self.bstack111l11lllll_opy_.bstack111l1l111l1_opy_():
            return self.bstack111l11lllll_opy_.get_name()
        return None