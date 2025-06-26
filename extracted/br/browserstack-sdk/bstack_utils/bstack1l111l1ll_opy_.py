# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
import tempfile
import math
from bstack_utils import bstack11l1l1l111_opy_
from bstack_utils.constants import bstack1l11l1111_opy_
bstack111l1l11l1l_opy_ = bstack11ll1l1_opy_ (u"ࠦࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠥᶽ")
bstack111l11l111l_opy_ = bstack11ll1l1_opy_ (u"ࠧࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦᶾ")
bstack111l11ll1l1_opy_ = bstack11ll1l1_opy_ (u"ࠨࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࡋ࡯ࡲࡴࡶࠥᶿ")
bstack111l1l11l11_opy_ = bstack11ll1l1_opy_ (u"ࠢࡳࡧࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࠣ᷀")
bstack111l11lll11_opy_ = bstack11ll1l1_opy_ (u"ࠣࡵ࡮࡭ࡵࡌ࡬ࡢ࡭ࡼࡥࡳࡪࡆࡢ࡫࡯ࡩࡩࠨ᷁")
bstack111l11l1111_opy_ = {
    bstack111l1l11l1l_opy_,
    bstack111l11l111l_opy_,
    bstack111l11ll1l1_opy_,
    bstack111l1l11l11_opy_,
    bstack111l11lll11_opy_,
}
bstack111l1l1l11l_opy_ = {bstack11ll1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ᷂ࠩ")}
logger = bstack11l1l1l111_opy_.get_logger(__name__, bstack1l11l1111_opy_)
class bstack111l1l11ll1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack111l1l1l111_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1ll1lll1_opy_:
    _1llll11l1l1_opy_ = None
    def __init__(self, config):
        self.bstack111l11lll1l_opy_ = False
        self.bstack111l1l111l1_opy_ = False
        self.bstack111l11l1l1l_opy_ = False
        self.bstack111l11l1l11_opy_ = bstack111l1l11ll1_opy_()
        opts = config.get(bstack11ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ᷃"), {})
        self.__111l11ll11l_opy_(opts.get(bstack111l11ll1l1_opy_, False))
        self.__111l11lllll_opy_(opts.get(bstack111l1l11l11_opy_, False))
        self.__111l11ll1ll_opy_(opts.get(bstack111l11lll11_opy_, False))
    @classmethod
    def bstack1lllll111l_opy_(cls, config=None):
        if cls._1llll11l1l1_opy_ is None and config is not None:
            cls._1llll11l1l1_opy_ = bstack1ll1lll1_opy_(config)
        return cls._1llll11l1l1_opy_
    @staticmethod
    def bstack1lll1l1l11_opy_(config: dict) -> bool:
        bstack111l1l1111l_opy_ = config.get(bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ᷄"), {}).get(bstack111l1l11l1l_opy_, {})
        return bstack111l1l1111l_opy_.get(bstack11ll1l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭᷅"), False)
    @staticmethod
    def bstack1ll11l1111_opy_(config: dict) -> int:
        bstack111l1l1111l_opy_ = config.get(bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ᷆"), {}).get(bstack111l1l11l1l_opy_, {})
        retries = 0
        if bstack1ll1lll1_opy_.bstack1lll1l1l11_opy_(config):
            retries = bstack111l1l1111l_opy_.get(bstack11ll1l1_opy_ (u"ࠧ࡮ࡣࡻࡖࡪࡺࡲࡪࡧࡶࠫ᷇"), 1)
        return retries
    @staticmethod
    def bstack11l1llll1_opy_(config: dict) -> dict:
        bstack111l1l111ll_opy_ = config.get(bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ᷈"), {})
        return {
            key: value for key, value in bstack111l1l111ll_opy_.items() if key in bstack111l11l1111_opy_
        }
    @staticmethod
    def bstack111l1l1l1ll_opy_():
        bstack11ll1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᷉")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀ᷊ࠦ").format(os.getenv(bstack11ll1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ᷋")))))
    @staticmethod
    def bstack111l11ll111_opy_(test_name: str):
        bstack11ll1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᷌")
        bstack111l11llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧ᷍").format(os.getenv(bstack11ll1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈ᷎ࠧ"))))
        with open(bstack111l11llll1_opy_, bstack11ll1l1_opy_ (u"ࠨࡣ᷏ࠪ")) as file:
            file.write(bstack11ll1l1_opy_ (u"ࠤࡾࢁࡡࡴ᷐ࠢ").format(test_name))
    @staticmethod
    def bstack111l11l1lll_opy_(framework: str) -> bool:
       return framework.lower() in bstack111l1l1l11l_opy_
    @staticmethod
    def bstack11l1ll1111l_opy_(config: dict) -> bool:
        bstack111l1l1l1l1_opy_ = config.get(bstack11ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ᷑"), {}).get(bstack111l11l111l_opy_, {})
        return bstack111l1l1l1l1_opy_.get(bstack11ll1l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ᷒"), False)
    @staticmethod
    def bstack11l1l1l1l11_opy_(config: dict, bstack11l1l1l111l_opy_: int = 0) -> int:
        bstack11ll1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠬࠡࡹ࡫࡭ࡨ࡮ࠠࡤࡣࡱࠤࡧ࡫ࠠࡢࡰࠣࡥࡧࡹ࡯࡭ࡷࡷࡩࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡲࠡࡣࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡱࡷࡥࡱࡥࡴࡦࡵࡷࡷࠥ࠮ࡩ࡯ࡶࠬ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࠬࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᷓ")
        bstack111l1l1l1l1_opy_ = config.get(bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᷔ"), {}).get(bstack11ll1l1_opy_ (u"ࠧࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭ᷕ"), {})
        bstack111l1l11lll_opy_ = 0
        bstack111l11l1ll1_opy_ = 0
        if bstack1ll1lll1_opy_.bstack11l1ll1111l_opy_(config):
            bstack111l11l1ll1_opy_ = bstack111l1l1l1l1_opy_.get(bstack11ll1l1_opy_ (u"ࠨ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸ࠭ᷖ"), 5)
            if isinstance(bstack111l11l1ll1_opy_, str) and bstack111l11l1ll1_opy_.endswith(bstack11ll1l1_opy_ (u"ࠩࠨࠫᷗ")):
                try:
                    percentage = int(bstack111l11l1ll1_opy_.strip(bstack11ll1l1_opy_ (u"ࠪࠩࠬᷘ")))
                    if bstack11l1l1l111l_opy_ > 0:
                        bstack111l1l11lll_opy_ = math.ceil((percentage * bstack11l1l1l111l_opy_) / 100)
                    else:
                        raise ValueError(bstack11ll1l1_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡰࡹࡸࡺࠠࡣࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠳ࡢࡢࡵࡨࡨࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࡴ࠰ࠥᷙ"))
                except ValueError as e:
                    raise ValueError(bstack11ll1l1_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧࠣࡺࡦࡲࡵࡦࠢࡩࡳࡷࠦ࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶ࠾ࠥࢁࡽࠣᷚ").format(bstack111l11l1ll1_opy_)) from e
            else:
                bstack111l1l11lll_opy_ = int(bstack111l11l1ll1_opy_)
        logger.info(bstack11ll1l1_opy_ (u"ࠨࡍࡢࡺࠣࡪࡦ࡯࡬ࡶࡴࡨࡷࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡵࡨࡸࠥࡺ࡯࠻ࠢࡾࢁࠥ࠮ࡦࡳࡱࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽࠪࠤᷛ").format(bstack111l1l11lll_opy_, bstack111l11l1ll1_opy_))
        return bstack111l1l11lll_opy_
    def bstack111l11l11ll_opy_(self):
        return self.bstack111l11lll1l_opy_
    def __111l11ll11l_opy_(self, value):
        self.bstack111l11lll1l_opy_ = bool(value)
        self.__111l1l1ll11_opy_()
    def bstack111l11l11l1_opy_(self):
        return self.bstack111l1l111l1_opy_
    def __111l11lllll_opy_(self, value):
        self.bstack111l1l111l1_opy_ = bool(value)
        self.__111l1l1ll11_opy_()
    def bstack111l1l11111_opy_(self):
        return self.bstack111l11l1l1l_opy_
    def __111l11ll1ll_opy_(self, value):
        self.bstack111l11l1l1l_opy_ = bool(value)
        self.__111l1l1ll11_opy_()
    def __111l1l1ll11_opy_(self):
        if self.bstack111l11lll1l_opy_:
            self.bstack111l1l111l1_opy_ = False
            self.bstack111l11l1l1l_opy_ = False
            self.bstack111l11l1l11_opy_.enable(bstack111l11ll1l1_opy_)
        elif self.bstack111l1l111l1_opy_:
            self.bstack111l11lll1l_opy_ = False
            self.bstack111l11l1l1l_opy_ = False
            self.bstack111l11l1l11_opy_.enable(bstack111l1l11l11_opy_)
        elif self.bstack111l11l1l1l_opy_:
            self.bstack111l11lll1l_opy_ = False
            self.bstack111l1l111l1_opy_ = False
            self.bstack111l11l1l11_opy_.enable(bstack111l11lll11_opy_)
        else:
            self.bstack111l11l1l11_opy_.disable()
    def bstack1ll1lll11_opy_(self):
        return self.bstack111l11l1l11_opy_.bstack111l1l1l111_opy_()
    def bstack1ll1lllll_opy_(self):
        if self.bstack111l11l1l11_opy_.bstack111l1l1l111_opy_():
            return self.bstack111l11l1l11_opy_.get_name()
        return None