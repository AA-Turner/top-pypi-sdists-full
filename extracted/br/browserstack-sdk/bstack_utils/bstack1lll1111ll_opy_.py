# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1l1111ll_opy_
from bstack_utils.constants import bstack11l1ll11ll_opy_
bstack111l11l1lll_opy_ = bstack111l111_opy_ (u"ࠦࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠥḃ")
bstack111l1l11l11_opy_ = bstack111l111_opy_ (u"ࠧࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦḄ")
bstack111l1l1111l_opy_ = bstack111l111_opy_ (u"ࠨࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࡋ࡯ࡲࡴࡶࠥḅ")
bstack111l11l111l_opy_ = bstack111l111_opy_ (u"ࠢࡳࡧࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࠣḆ")
bstack111l11ll111_opy_ = bstack111l111_opy_ (u"ࠣࡵ࡮࡭ࡵࡌ࡬ࡢ࡭ࡼࡥࡳࡪࡆࡢ࡫࡯ࡩࡩࠨḇ")
bstack111l111ll1l_opy_ = {
    bstack111l11l1lll_opy_,
    bstack111l1l11l11_opy_,
    bstack111l1l1111l_opy_,
    bstack111l11l111l_opy_,
    bstack111l11ll111_opy_,
}
bstack111l1l111ll_opy_ = {bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩḈ")}
logger = bstack1l1111ll_opy_.get_logger(__name__, bstack11l1ll11ll_opy_)
class bstack111l11l11l1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack111l11l1ll1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack11llllll_opy_:
    _1llll11l1ll_opy_ = None
    def __init__(self, config):
        self.bstack111l11lll1l_opy_ = False
        self.bstack111l111l1ll_opy_ = False
        self.bstack111l1l11ll1_opy_ = False
        self.bstack111l1l11l1l_opy_ = bstack111l11l11l1_opy_()
        opts = config.get(bstack111l111_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧḉ"), {})
        self.__111l11l1l11_opy_(opts.get(bstack111l1l1111l_opy_, False))
        self.__111l11llll1_opy_(opts.get(bstack111l11l111l_opy_, False))
        self.__111l111llll_opy_(opts.get(bstack111l11ll111_opy_, False))
    @classmethod
    def bstack1ll11ll1_opy_(cls, config=None):
        if cls._1llll11l1ll_opy_ is None and config is not None:
            cls._1llll11l1ll_opy_ = bstack11llllll_opy_(config)
        return cls._1llll11l1ll_opy_
    @staticmethod
    def bstack1lll1l1lll_opy_(config: dict) -> bool:
        bstack111l111lll1_opy_ = config.get(bstack111l111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨḊ"), {}).get(bstack111l11l1lll_opy_, {})
        return bstack111l111lll1_opy_.get(bstack111l111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ḋ"), False)
    @staticmethod
    def bstack1l111ll1l_opy_(config: dict) -> int:
        bstack111l111lll1_opy_ = config.get(bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪḌ"), {}).get(bstack111l11l1lll_opy_, {})
        retries = 0
        if bstack11llllll_opy_.bstack1lll1l1lll_opy_(config):
            retries = bstack111l111lll1_opy_.get(bstack111l111_opy_ (u"ࠧ࡮ࡣࡻࡖࡪࡺࡲࡪࡧࡶࠫḍ"), 1)
        return retries
    @staticmethod
    def bstack11lll11lll_opy_(config: dict) -> dict:
        bstack111l1l111l1_opy_ = config.get(bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬḎ"), {})
        return {
            key: value for key, value in bstack111l1l111l1_opy_.items() if key in bstack111l111ll1l_opy_
        }
    @staticmethod
    def bstack111l11l11ll_opy_():
        bstack111l111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨḏ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦḐ").format(os.getenv(bstack111l111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤḑ")))))
    @staticmethod
    def bstack111l11lll11_opy_(test_name: str):
        bstack111l111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤḒ")
        bstack111l11l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧḓ").format(os.getenv(bstack111l111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧḔ"))))
        with open(bstack111l11l1l1l_opy_, bstack111l111_opy_ (u"ࠨࡣࠪḕ")) as file:
            file.write(bstack111l111_opy_ (u"ࠤࡾࢁࡡࡴࠢḖ").format(test_name))
    @staticmethod
    def bstack111l11ll1l1_opy_(framework: str) -> bool:
       return framework.lower() in bstack111l1l111ll_opy_
    @staticmethod
    def bstack11l1l11l111_opy_(config: dict) -> bool:
        bstack111l11l1111_opy_ = config.get(bstack111l111_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧḗ"), {}).get(bstack111l1l11l11_opy_, {})
        return bstack111l11l1111_opy_.get(bstack111l111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬḘ"), False)
    @staticmethod
    def bstack11l1l1l111l_opy_(config: dict, bstack11l1l1ll1l1_opy_: int = 0) -> int:
        bstack111l111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠬࠡࡹ࡫࡭ࡨ࡮ࠠࡤࡣࡱࠤࡧ࡫ࠠࡢࡰࠣࡥࡧࡹ࡯࡭ࡷࡷࡩࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡲࠡࡣࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡱࡷࡥࡱࡥࡴࡦࡵࡷࡷࠥ࠮ࡩ࡯ࡶࠬ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࠬࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥḙ")
        bstack111l11l1111_opy_ = config.get(bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪḚ"), {}).get(bstack111l111_opy_ (u"ࠧࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭ḛ"), {})
        bstack111l11lllll_opy_ = 0
        bstack111l11ll1ll_opy_ = 0
        if bstack11llllll_opy_.bstack11l1l11l111_opy_(config):
            bstack111l11ll1ll_opy_ = bstack111l11l1111_opy_.get(bstack111l111_opy_ (u"ࠨ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸ࠭Ḝ"), 5)
            if isinstance(bstack111l11ll1ll_opy_, str) and bstack111l11ll1ll_opy_.endswith(bstack111l111_opy_ (u"ࠩࠨࠫḝ")):
                try:
                    percentage = int(bstack111l11ll1ll_opy_.strip(bstack111l111_opy_ (u"ࠪࠩࠬḞ")))
                    if bstack11l1l1ll1l1_opy_ > 0:
                        bstack111l11lllll_opy_ = math.ceil((percentage * bstack11l1l1ll1l1_opy_) / 100)
                    else:
                        raise ValueError(bstack111l111_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡰࡹࡸࡺࠠࡣࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠳ࡢࡢࡵࡨࡨࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࡴ࠰ࠥḟ"))
                except ValueError as e:
                    raise ValueError(bstack111l111_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧࠣࡺࡦࡲࡵࡦࠢࡩࡳࡷࠦ࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶ࠾ࠥࢁࡽࠣḠ").format(bstack111l11ll1ll_opy_)) from e
            else:
                bstack111l11lllll_opy_ = int(bstack111l11ll1ll_opy_)
        logger.info(bstack111l111_opy_ (u"ࠨࡍࡢࡺࠣࡪࡦ࡯࡬ࡶࡴࡨࡷࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡵࡨࡸࠥࡺ࡯࠻ࠢࡾࢁࠥ࠮ࡦࡳࡱࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽࠪࠤḡ").format(bstack111l11lllll_opy_, bstack111l11ll1ll_opy_))
        return bstack111l11lllll_opy_
    def bstack111l1l11111_opy_(self):
        return self.bstack111l11lll1l_opy_
    def __111l11l1l11_opy_(self, value):
        self.bstack111l11lll1l_opy_ = bool(value)
        self.__111l111l1l1_opy_()
    def bstack111l111ll11_opy_(self):
        return self.bstack111l111l1ll_opy_
    def __111l11llll1_opy_(self, value):
        self.bstack111l111l1ll_opy_ = bool(value)
        self.__111l111l1l1_opy_()
    def bstack111l11ll11l_opy_(self):
        return self.bstack111l1l11ll1_opy_
    def __111l111llll_opy_(self, value):
        self.bstack111l1l11ll1_opy_ = bool(value)
        self.__111l111l1l1_opy_()
    def __111l111l1l1_opy_(self):
        if self.bstack111l11lll1l_opy_:
            self.bstack111l111l1ll_opy_ = False
            self.bstack111l1l11ll1_opy_ = False
            self.bstack111l1l11l1l_opy_.enable(bstack111l1l1111l_opy_)
        elif self.bstack111l111l1ll_opy_:
            self.bstack111l11lll1l_opy_ = False
            self.bstack111l1l11ll1_opy_ = False
            self.bstack111l1l11l1l_opy_.enable(bstack111l11l111l_opy_)
        elif self.bstack111l1l11ll1_opy_:
            self.bstack111l11lll1l_opy_ = False
            self.bstack111l111l1ll_opy_ = False
            self.bstack111l1l11l1l_opy_.enable(bstack111l11ll111_opy_)
        else:
            self.bstack111l1l11l1l_opy_.disable()
    def bstack1l111l1l1l_opy_(self):
        return self.bstack111l1l11l1l_opy_.bstack111l11l1ll1_opy_()
    def bstack11llll11_opy_(self):
        if self.bstack111l1l11l1l_opy_.bstack111l11l1ll1_opy_():
            return self.bstack111l1l11l1l_opy_.get_name()
        return None