# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1ll11l1ll_opy_
from bstack_utils.constants import bstack11lll11111_opy_
bstack111l11l1111_opy_ = bstackl_opy_ (u"ࠧࡸࡥࡵࡴࡼࡘࡪࡹࡴࡴࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦḄ")
bstack111l11ll1l1_opy_ = bstackl_opy_ (u"ࠨࡡࡣࡱࡵࡸࡇࡻࡩ࡭ࡦࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠧḅ")
bstack111l11l11l1_opy_ = bstackl_opy_ (u"ࠢࡳࡷࡱࡔࡷ࡫ࡶࡪࡱࡸࡷࡱࡿࡆࡢ࡫࡯ࡩࡩࡌࡩࡳࡵࡷࠦḆ")
bstack111l11lll1l_opy_ = bstackl_opy_ (u"ࠣࡴࡨࡶࡺࡴࡐࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡉࡥ࡮ࡲࡥࡥࠤḇ")
bstack111l111l11l_opy_ = bstackl_opy_ (u"ࠤࡶ࡯࡮ࡶࡆ࡭ࡣ࡮ࡽࡦࡴࡤࡇࡣ࡬ࡰࡪࡪࠢḈ")
bstack111l11l111l_opy_ = {
    bstack111l11l1111_opy_,
    bstack111l11ll1l1_opy_,
    bstack111l11l11l1_opy_,
    bstack111l11lll1l_opy_,
    bstack111l111l11l_opy_,
}
bstack111l11l1l1l_opy_ = {bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪḉ")}
logger = bstack1ll11l1ll_opy_.get_logger(__name__, bstack11lll11111_opy_)
class bstack111l111l1l1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack111l111llll_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1ll11l11l1_opy_:
    _1lll1ll111l_opy_ = None
    def __init__(self, config):
        self.bstack111l1l111l1_opy_ = False
        self.bstack111l11ll1ll_opy_ = False
        self.bstack111l111ll1l_opy_ = False
        self.bstack111l111l1ll_opy_ = bstack111l111l1l1_opy_()
        opts = config.get(bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨḊ"), {})
        self.__111l111lll1_opy_(opts.get(bstack111l11l11l1_opy_, False))
        self.__111l1l11l1l_opy_(opts.get(bstack111l11lll1l_opy_, False))
        self.__111l11llll1_opy_(opts.get(bstack111l111l11l_opy_, False))
    @classmethod
    def bstack1l1l11ll_opy_(cls, config=None):
        if cls._1lll1ll111l_opy_ is None and config is not None:
            cls._1lll1ll111l_opy_ = bstack1ll11l11l1_opy_(config)
        return cls._1lll1ll111l_opy_
    @staticmethod
    def bstack1ll11ll1l_opy_(config: dict) -> bool:
        bstack111l11l1lll_opy_ = config.get(bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩḋ"), {}).get(bstack111l11l1111_opy_, {})
        return bstack111l11l1lll_opy_.get(bstackl_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧḌ"), False)
    @staticmethod
    def bstack1ll11l1111_opy_(config: dict) -> int:
        bstack111l11l1lll_opy_ = config.get(bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫḍ"), {}).get(bstack111l11l1111_opy_, {})
        retries = 0
        if bstack1ll11l11l1_opy_.bstack1ll11ll1l_opy_(config):
            retries = bstack111l11l1lll_opy_.get(bstackl_opy_ (u"ࠨ࡯ࡤࡼࡗ࡫ࡴࡳ࡫ࡨࡷࠬḎ"), 1)
        return retries
    @staticmethod
    def bstack1l1111ll11_opy_(config: dict) -> dict:
        bstack111l1l1111l_opy_ = config.get(bstackl_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ḏ"), {})
        return {
            key: value for key, value in bstack111l1l1111l_opy_.items() if key in bstack111l11l111l_opy_
        }
    @staticmethod
    def bstack111l11l1ll1_opy_():
        bstackl_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢḐ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧḑ").format(os.getenv(bstackl_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥḒ")))))
    @staticmethod
    def bstack111l1l11l11_opy_(test_name: str):
        bstackl_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥḓ")
        bstack111l11lllll_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨḔ").format(os.getenv(bstackl_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨḕ"))))
        with open(bstack111l11lllll_opy_, bstackl_opy_ (u"ࠩࡤࠫḖ")) as file:
            file.write(bstackl_opy_ (u"ࠥࡿࢂࡢ࡮ࠣḗ").format(test_name))
    @staticmethod
    def bstack111l11l11ll_opy_(framework: str) -> bool:
       return framework.lower() in bstack111l11l1l1l_opy_
    @staticmethod
    def bstack11l1l11l11l_opy_(config: dict) -> bool:
        bstack111l1l11111_opy_ = config.get(bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨḘ"), {}).get(bstack111l11ll1l1_opy_, {})
        return bstack111l1l11111_opy_.get(bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ḙ"), False)
    @staticmethod
    def bstack11l1l11l111_opy_(config: dict, bstack11l1l1l1111_opy_: int = 0) -> int:
        bstackl_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠭ࠢࡺ࡬࡮ࡩࡨࠡࡥࡤࡲࠥࡨࡥࠡࡣࡱࠤࡦࡨࡳࡰ࡮ࡸࡸࡪࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡳࠢࡤࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭ࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡲࡸࡦࡲ࡟ࡵࡧࡶࡸࡸࠦࠨࡪࡰࡷ࠭࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤ࠭ࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦḚ")
        bstack111l1l11111_opy_ = config.get(bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫḛ"), {}).get(bstackl_opy_ (u"ࠨࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧḜ"), {})
        bstack111l11l1l11_opy_ = 0
        bstack111l1l111ll_opy_ = 0
        if bstack1ll11l11l1_opy_.bstack11l1l11l11l_opy_(config):
            bstack111l1l111ll_opy_ = bstack111l1l11111_opy_.get(bstackl_opy_ (u"ࠩࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹࠧḝ"), 5)
            if isinstance(bstack111l1l111ll_opy_, str) and bstack111l1l111ll_opy_.endswith(bstackl_opy_ (u"ࠪࠩࠬḞ")):
                try:
                    percentage = int(bstack111l1l111ll_opy_.strip(bstackl_opy_ (u"ࠫࠪ࠭ḟ")))
                    if bstack11l1l1l1111_opy_ > 0:
                        bstack111l11l1l11_opy_ = math.ceil((percentage * bstack11l1l1l1111_opy_) / 100)
                    else:
                        raise ValueError(bstackl_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡱࡺࡹࡴࠡࡤࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵ࠱ࠦḠ"))
                except ValueError as e:
                    raise ValueError(bstackl_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨࠤࡻࡧ࡬ࡶࡧࠣࡪࡴࡸࠠ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷ࠿ࠦࡻࡾࠤḡ").format(bstack111l1l111ll_opy_)) from e
            else:
                bstack111l11l1l11_opy_ = int(bstack111l1l111ll_opy_)
        logger.info(bstackl_opy_ (u"ࠢࡎࡣࡻࠤ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡶࡩࡹࠦࡴࡰ࠼ࠣࡿࢂࠦࠨࡧࡴࡲࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾࠫࠥḢ").format(bstack111l11l1l11_opy_, bstack111l1l111ll_opy_))
        return bstack111l11l1l11_opy_
    def bstack111l111ll11_opy_(self):
        return self.bstack111l1l111l1_opy_
    def __111l111lll1_opy_(self, value):
        self.bstack111l1l111l1_opy_ = bool(value)
        self.__111l11ll11l_opy_()
    def bstack111l11lll11_opy_(self):
        return self.bstack111l11ll1ll_opy_
    def __111l1l11l1l_opy_(self, value):
        self.bstack111l11ll1ll_opy_ = bool(value)
        self.__111l11ll11l_opy_()
    def bstack111l11ll111_opy_(self):
        return self.bstack111l111ll1l_opy_
    def __111l11llll1_opy_(self, value):
        self.bstack111l111ll1l_opy_ = bool(value)
        self.__111l11ll11l_opy_()
    def __111l11ll11l_opy_(self):
        if self.bstack111l1l111l1_opy_:
            self.bstack111l11ll1ll_opy_ = False
            self.bstack111l111ll1l_opy_ = False
            self.bstack111l111l1ll_opy_.enable(bstack111l11l11l1_opy_)
        elif self.bstack111l11ll1ll_opy_:
            self.bstack111l1l111l1_opy_ = False
            self.bstack111l111ll1l_opy_ = False
            self.bstack111l111l1ll_opy_.enable(bstack111l11lll1l_opy_)
        elif self.bstack111l111ll1l_opy_:
            self.bstack111l1l111l1_opy_ = False
            self.bstack111l11ll1ll_opy_ = False
            self.bstack111l111l1ll_opy_.enable(bstack111l111l11l_opy_)
        else:
            self.bstack111l111l1ll_opy_.disable()
    def bstack11l1ll1lll_opy_(self):
        return self.bstack111l111l1ll_opy_.bstack111l111llll_opy_()
    def bstack1llll1llll_opy_(self):
        if self.bstack111l111l1ll_opy_.bstack111l111llll_opy_():
            return self.bstack111l111l1ll_opy_.get_name()
        return None