# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1l1111111_opy_
from bstack_utils.constants import bstack11ll1lll_opy_
from bstack_utils.helper import bstack111ll1ll11l_opy_, get_host_info
from bstack_utils.bstack11ll11l1l11_opy_ import bstack11ll11l1111_opy_
bstack111l111l111_opy_ = bstack11l1_opy_ (u"ࠣࡴࡨࡸࡷࡿࡔࡦࡵࡷࡷࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢṔ")
bstack111l111l1ll_opy_ = bstack11l1_opy_ (u"ࠤࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣṕ")
bstack111l1111111_opy_ = bstack11l1_opy_ (u"ࠥࡶࡺࡴࡐࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡉࡥ࡮ࡲࡥࡥࡈ࡬ࡶࡸࡺࠢṖ")
bstack1111lll1lll_opy_ = bstack11l1_opy_ (u"ࠦࡷ࡫ࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࠧṗ")
bstack111l11l1l11_opy_ = bstack11l1_opy_ (u"ࠧࡹ࡫ࡪࡲࡉࡰࡦࡱࡹࡢࡰࡧࡊࡦ࡯࡬ࡦࡦࠥṘ")
bstack111l11l11l1_opy_ = bstack11l1_opy_ (u"ࠨࡲࡶࡰࡖࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࠥṙ")
bstack111l111lll1_opy_ = {
    bstack111l111l111_opy_,
    bstack111l111l1ll_opy_,
    bstack111l1111111_opy_,
    bstack1111lll1lll_opy_,
    bstack111l11l1l11_opy_,
    bstack111l11l11l1_opy_
}
bstack111l11ll11l_opy_ = {bstack11l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧṚ")}
logger = bstack1l1111111_opy_.get_logger(__name__, bstack11ll1lll_opy_)
class bstack1111llll1ll_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack111l11111l1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l111ll11l_opy_:
    _1llll11ll1l_opy_ = None
    def __init__(self, config):
        self.bstack111l11l1ll1_opy_ = False
        self.bstack111l11l1lll_opy_ = False
        self.bstack111l111l11l_opy_ = False
        self.bstack111l11l11ll_opy_ = False
        self.bstack111l111l1l1_opy_ = None
        self.bstack1111lll1l1l_opy_ = bstack1111llll1ll_opy_()
        opts = config.get(bstack11l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬṛ"), {})
        self.__111l11l1111_opy_(opts.get(bstack111l11l11l1_opy_, {}).get(bstack11l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṜ"), False),
                                       opts.get(bstack111l11l11l1_opy_, {}).get(bstack11l1_opy_ (u"ࠪࡱࡴࡪࡥࠨṝ"), bstack11l1_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡌࡩࡳࡵࡷࠫṞ")))
        self.__111l111ll11_opy_(opts.get(bstack111l1111111_opy_, False))
        self.__1111lllll1l_opy_(opts.get(bstack1111lll1lll_opy_, False))
        self.__1111llll11l_opy_(opts.get(bstack111l11l1l11_opy_, False))
    @classmethod
    def bstack1l1lll11l_opy_(cls, config=None):
        if cls._1llll11ll1l_opy_ is None and config is not None:
            cls._1llll11ll1l_opy_ = bstack1l111ll11l_opy_(config)
        return cls._1llll11ll1l_opy_
    @staticmethod
    def bstack11l1l11l1l_opy_(config: dict) -> bool:
        bstack111l1111l1l_opy_ = config.get(bstack11l1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩṟ"), {}).get(bstack111l111l111_opy_, {})
        return bstack111l1111l1l_opy_.get(bstack11l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧṠ"), False)
    @staticmethod
    def bstack11l1l11ll_opy_(config: dict) -> int:
        bstack111l1111l1l_opy_ = config.get(bstack11l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫṡ"), {}).get(bstack111l111l111_opy_, {})
        retries = 0
        if bstack1l111ll11l_opy_.bstack11l1l11l1l_opy_(config):
            retries = bstack111l1111l1l_opy_.get(bstack11l1_opy_ (u"ࠨ࡯ࡤࡼࡗ࡫ࡴࡳ࡫ࡨࡷࠬṢ"), 1)
        return retries
    @staticmethod
    def bstack11ll1ll11l_opy_(config: dict) -> dict:
        bstack111l11l111l_opy_ = config.get(bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ṣ"), {})
        return {
            key: value for key, value in bstack111l11l111l_opy_.items() if key in bstack111l111lll1_opy_
        }
    @staticmethod
    def bstack111l1111ll1_opy_():
        bstack11l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢṤ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧṥ").format(os.getenv(bstack11l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥṦ")))))
    @staticmethod
    def bstack111l111llll_opy_(test_name: str):
        bstack11l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥṧ")
        bstack111l11l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨṨ").format(os.getenv(bstack11l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨṩ"))))
        with open(bstack111l11l1l1l_opy_, bstack11l1_opy_ (u"ࠩࡤࠫṪ")) as file:
            file.write(bstack11l1_opy_ (u"ࠥࡿࢂࡢ࡮ࠣṫ").format(test_name))
    @staticmethod
    def bstack111l1111lll_opy_(framework: str) -> bool:
       return framework.lower() in bstack111l11ll11l_opy_
    @staticmethod
    def bstack11l1l11ll1l_opy_(config: dict) -> bool:
        bstack111l111ll1l_opy_ = config.get(bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨṬ"), {}).get(bstack111l111l1ll_opy_, {})
        return bstack111l111ll1l_opy_.get(bstack11l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ṭ"), False)
    @staticmethod
    def bstack11l1l1ll111_opy_(config: dict, bstack11l1l1l1l1l_opy_: int = 0) -> int:
        bstack11l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠭ࠢࡺ࡬࡮ࡩࡨࠡࡥࡤࡲࠥࡨࡥࠡࡣࡱࠤࡦࡨࡳࡰ࡮ࡸࡸࡪࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡳࠢࡤࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭ࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡲࡸࡦࡲ࡟ࡵࡧࡶࡸࡸࠦࠨࡪࡰࡷ࠭࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤ࠭ࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦṮ")
        bstack111l111ll1l_opy_ = config.get(bstack11l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫṯ"), {}).get(bstack11l1_opy_ (u"ࠨࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧṰ"), {})
        bstack1111lllll11_opy_ = 0
        bstack1111lll11ll_opy_ = 0
        if bstack1l111ll11l_opy_.bstack11l1l11ll1l_opy_(config):
            bstack1111lll11ll_opy_ = bstack111l111ll1l_opy_.get(bstack11l1_opy_ (u"ࠩࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹࠧṱ"), 5)
            if isinstance(bstack1111lll11ll_opy_, str) and bstack1111lll11ll_opy_.endswith(bstack11l1_opy_ (u"ࠪࠩࠬṲ")):
                try:
                    percentage = int(bstack1111lll11ll_opy_.strip(bstack11l1_opy_ (u"ࠫࠪ࠭ṳ")))
                    if bstack11l1l1l1l1l_opy_ > 0:
                        bstack1111lllll11_opy_ = math.ceil((percentage * bstack11l1l1l1l1l_opy_) / 100)
                    else:
                        raise ValueError(bstack11l1_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡱࡺࡹࡴࠡࡤࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵ࠱ࠦṴ"))
                except ValueError as e:
                    raise ValueError(bstack11l1_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨࠤࡻࡧ࡬ࡶࡧࠣࡪࡴࡸࠠ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷ࠿ࠦࡻࡾࠤṵ").format(bstack1111lll11ll_opy_)) from e
            else:
                bstack1111lllll11_opy_ = int(bstack1111lll11ll_opy_)
        logger.info(bstack11l1_opy_ (u"ࠢࡎࡣࡻࠤ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡶࡩࡹࠦࡴࡰ࠼ࠣࡿࢂࠦࠨࡧࡴࡲࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾࠫࠥṶ").format(bstack1111lllll11_opy_, bstack1111lll11ll_opy_))
        return bstack1111lllll11_opy_
    def bstack1111lllllll_opy_(self):
        return self.bstack111l11l11ll_opy_
    def bstack1111lll1ll1_opy_(self):
        return self.bstack111l111l1l1_opy_
    def __111l11l1111_opy_(self, enabled, mode):
        self.bstack111l11l11ll_opy_ = bool(enabled)
        self.bstack111l111l1l1_opy_ = mode
        self.__111l11ll111_opy_()
    def bstack111l11111ll_opy_(self):
        return self.bstack111l11l1ll1_opy_
    def __111l111ll11_opy_(self, value):
        self.bstack111l11l1ll1_opy_ = bool(value)
        self.__111l11ll111_opy_()
    def bstack1111llll1l1_opy_(self):
        return self.bstack111l11l1lll_opy_
    def __1111lllll1l_opy_(self, value):
        self.bstack111l11l1lll_opy_ = bool(value)
        self.__111l11ll111_opy_()
    def bstack111l1111l11_opy_(self):
        return self.bstack111l111l11l_opy_
    def __1111llll11l_opy_(self, value):
        self.bstack111l111l11l_opy_ = bool(value)
        self.__111l11ll111_opy_()
    def __111l11ll111_opy_(self):
        if self.bstack111l11l11ll_opy_:
            self.bstack111l11l1ll1_opy_ = False
            self.bstack111l11l1lll_opy_ = False
            self.bstack111l111l11l_opy_ = False
            self.bstack1111lll1l1l_opy_.enable(bstack111l11l11l1_opy_)
        elif self.bstack111l11l1ll1_opy_:
            self.bstack111l11l1lll_opy_ = False
            self.bstack111l111l11l_opy_ = False
            self.bstack1111lll1l1l_opy_.enable(bstack111l1111111_opy_)
        elif self.bstack111l11l1lll_opy_:
            self.bstack111l11l1ll1_opy_ = False
            self.bstack111l111l11l_opy_ = False
            self.bstack1111lll1l1l_opy_.enable(bstack1111lll1lll_opy_)
        elif self.bstack111l111l11l_opy_:
            self.bstack111l11l1ll1_opy_ = False
            self.bstack111l11l1lll_opy_ = False
            self.bstack1111lll1l1l_opy_.enable(bstack111l11l1l11_opy_)
        else:
            self.bstack1111lll1l1l_opy_.disable()
    def bstack1ll11llll1_opy_(self):
        return self.bstack1111lll1l1l_opy_.bstack111l11111l1_opy_()
    def bstack111lllllll_opy_(self):
        if self.bstack1111lll1l1l_opy_.bstack111l11111l1_opy_():
            return self.bstack1111lll1l1l_opy_.get_name()
        return None
    def bstack111l11lll1l_opy_(self):
        return {
            bstack11l1_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧṷ") : {
                bstack11l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṸ"): self.bstack1111lllllll_opy_(),
                bstack11l1_opy_ (u"ࠪࡱࡴࡪࡥࠨṹ"): self.bstack1111lll1ll1_opy_()
            }
        }
    def bstack1111lll1l11_opy_(self, config):
        bstack1111llllll1_opy_ = {}
        bstack1111llllll1_opy_[bstack11l1_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪṺ")] = {
            bstack11l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ṻ"): self.bstack1111lllllll_opy_(),
            bstack11l1_opy_ (u"࠭࡭ࡰࡦࡨࠫṼ"): self.bstack1111lll1ll1_opy_()
        }
        bstack1111llllll1_opy_[bstack11l1_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࠪṽ")] = {
            bstack11l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩṾ"): self.bstack1111llll1l1_opy_()
        }
        bstack1111llllll1_opy_[bstack11l1_opy_ (u"ࠩࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࡢࡪ࡮ࡸࡳࡵࠩṿ")] = {
            bstack11l1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫẀ"): self.bstack111l11111ll_opy_()
        }
        bstack1111llllll1_opy_[bstack11l1_opy_ (u"ࠫࡸࡱࡩࡱࡡࡩࡥ࡮ࡲࡩ࡯ࡩࡢࡥࡳࡪ࡟ࡧ࡮ࡤ࡯ࡾ࠭ẁ")] = {
            bstack11l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭Ẃ"): self.bstack111l1111l11_opy_()
        }
        if self.bstack11l1l11l1l_opy_(config):
            bstack1111llllll1_opy_[bstack11l1_opy_ (u"࠭ࡲࡦࡶࡵࡽࡤࡺࡥࡴࡶࡶࡣࡴࡴ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠨẃ")] = {
                bstack11l1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨẄ"): True,
                bstack11l1_opy_ (u"ࠨ࡯ࡤࡼࡤࡸࡥࡵࡴ࡬ࡩࡸ࠭ẅ"): self.bstack11l1l11ll_opy_(config)
            }
        if self.bstack11l1l11ll1l_opy_(config):
            bstack1111llllll1_opy_[bstack11l1_opy_ (u"ࠩࡤࡦࡴࡸࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡰࡰࡢࡪࡦ࡯࡬ࡶࡴࡨࠫẆ")] = {
                bstack11l1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫẇ"): True,
                bstack11l1_opy_ (u"ࠫࡲࡧࡸࡠࡨࡤ࡭ࡱࡻࡲࡦࡵࠪẈ"): self.bstack11l1l1ll111_opy_(config)
            }
        return bstack1111llllll1_opy_
    def bstack1ll11l1ll_opy_(self, config):
        bstack11l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡳࡱࡲࡥࡤࡶࡶࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡤࡼࠤࡲࡧ࡫ࡪࡰࡪࠤࡦࠦࡣࡢ࡮࡯ࠤࡹࡵࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠠࠩࡵࡷࡶ࠮ࡀࠠࡕࡪࡨࠤ࡚࡛ࡉࡅࠢࡲࡪࠥࡺࡨࡦࠢࡥࡹ࡮ࡲࡤࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠱ࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠠࡪࡨࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣẉ")
        bstack111l111111l_opy_ = os.environ.get(bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫẊ"), None)
        logger.debug(bstack11l1_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡉ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊ࠺ࠡࡽࢀࠦẋ").format(bstack111l111111l_opy_))
        try:
            bstack11ll11ll11l_opy_ = bstack11l1_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠨẌ").format(bstack111l111111l_opy_)
            payload = {
                bstack11l1_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢẍ"): config.get(bstack11l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨẎ"), bstack11l1_opy_ (u"ࠫࠬẏ")),
                bstack11l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣẐ"): config.get(bstack11l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩẑ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧẒ"): os.environ.get(bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧẓ"), None),
                bstack11l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧẔ"): int(os.environ.get(bstack11l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨẕ")) or bstack11l1_opy_ (u"ࠦ࠵ࠨẖ")),
                bstack11l1_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤẗ"): int(os.environ.get(bstack11l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣẘ")) or bstack11l1_opy_ (u"ࠢ࠲ࠤẙ")),
                bstack11l1_opy_ (u"ࠣࡪࡲࡷࡹࡏ࡮ࡧࡱࠥẚ"): get_host_info(),
                bstack11l1_opy_ (u"ࠤࡳࡶࡉ࡫ࡴࡢ࡫࡯ࡷࠧẛ"): bstack111ll1ll11l_opy_()
            }
            logger.debug(bstack11l1_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡰࡢࡻ࡯ࡳࡦࡪ࠺ࠡࡽࢀࠦẜ").format(payload))
            response = bstack11ll11l1111_opy_.bstack1111llll111_opy_(bstack11ll11ll11l_opy_, payload)
            if response:
                logger.debug(bstack11l1_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡅࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤẝ").format(response))
                return response
            else:
                logger.error(bstack11l1_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈ࠿ࠦࡻࡾࠤẞ").format(bstack111l111111l_opy_))
                return None
        except Exception as e:
            logger.error(bstack11l1_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈࠥࢁࡽ࠻ࠢࡾࢁࠧẟ").format(bstack111l111111l_opy_, e))
            return None