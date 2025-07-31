# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1l1ll11lll_opy_
from bstack_utils.constants import bstack1ll1lll1_opy_
from bstack_utils.helper import bstack11l1111lll1_opy_, get_host_info
from bstack_utils.bstack11ll111l1ll_opy_ import bstack11ll11l111l_opy_
bstack1111lllll11_opy_ = bstack1l11l11_opy_ (u"ࠢࡳࡧࡷࡶࡾ࡚ࡥࡴࡶࡶࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨṓ")
bstack1111llll1l1_opy_ = bstack1l11l11_opy_ (u"ࠣࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢṔ")
bstack1111llll11l_opy_ = bstack1l11l11_opy_ (u"ࠤࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࡇ࡫ࡵࡷࡹࠨṕ")
bstack1111ll1lll1_opy_ = bstack1l11l11_opy_ (u"ࠥࡶࡪࡸࡵ࡯ࡒࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡋࡧࡩ࡭ࡧࡧࠦṖ")
bstack111l111ll11_opy_ = bstack1l11l11_opy_ (u"ࠦࡸࡱࡩࡱࡈ࡯ࡥࡰࡿࡡ࡯ࡦࡉࡥ࡮ࡲࡥࡥࠤṗ")
bstack111l1111111_opy_ = bstack1l11l11_opy_ (u"ࠧࡸࡵ࡯ࡕࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠤṘ")
bstack1111llll111_opy_ = {
    bstack1111lllll11_opy_,
    bstack1111llll1l1_opy_,
    bstack1111llll11l_opy_,
    bstack1111ll1lll1_opy_,
    bstack111l111ll11_opy_,
    bstack111l1111111_opy_
}
bstack1111lll1ll1_opy_ = {bstack1l11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ṙ")}
logger = bstack1l1ll11lll_opy_.get_logger(__name__, bstack1ll1lll1_opy_)
class bstack111l1111l11_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack111l111111l_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack11l11l1lll_opy_:
    _1lll11ll1l1_opy_ = None
    def __init__(self, config):
        self.bstack1111lll1111_opy_ = False
        self.bstack1111lll1l1l_opy_ = False
        self.bstack111l11l11ll_opy_ = False
        self.bstack111l1111l1l_opy_ = False
        self.bstack111l111llll_opy_ = None
        self.bstack111l111l11l_opy_ = bstack111l1111l11_opy_()
        opts = config.get(bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫṚ"), {})
        self.__1111llllll1_opy_(opts.get(bstack111l1111111_opy_, {}).get(bstack1l11l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩṛ"), False),
                                       opts.get(bstack111l1111111_opy_, {}).get(bstack1l11l11_opy_ (u"ࠩࡰࡳࡩ࡫ࠧṜ"), bstack1l11l11_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪṝ")))
        self.__111l11l111l_opy_(opts.get(bstack1111llll11l_opy_, False))
        self.__1111lll111l_opy_(opts.get(bstack1111ll1lll1_opy_, False))
        self.__111l111l111_opy_(opts.get(bstack111l111ll11_opy_, False))
    @classmethod
    def bstack11l111llll_opy_(cls, config=None):
        if cls._1lll11ll1l1_opy_ is None and config is not None:
            cls._1lll11ll1l1_opy_ = bstack11l11l1lll_opy_(config)
        return cls._1lll11ll1l1_opy_
    @staticmethod
    def bstack1l11ll1l1l_opy_(config: dict) -> bool:
        bstack111l1111lll_opy_ = config.get(bstack1l11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨṞ"), {}).get(bstack1111lllll11_opy_, {})
        return bstack111l1111lll_opy_.get(bstack1l11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ṟ"), False)
    @staticmethod
    def bstack1l1lll11l1_opy_(config: dict) -> int:
        bstack111l1111lll_opy_ = config.get(bstack1l11l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪṠ"), {}).get(bstack1111lllll11_opy_, {})
        retries = 0
        if bstack11l11l1lll_opy_.bstack1l11ll1l1l_opy_(config):
            retries = bstack111l1111lll_opy_.get(bstack1l11l11_opy_ (u"ࠧ࡮ࡣࡻࡖࡪࡺࡲࡪࡧࡶࠫṡ"), 1)
        return retries
    @staticmethod
    def bstack11l111l11l_opy_(config: dict) -> dict:
        bstack111l111l1ll_opy_ = config.get(bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬṢ"), {})
        return {
            key: value for key, value in bstack111l111l1ll_opy_.items() if key in bstack1111llll111_opy_
        }
    @staticmethod
    def bstack1111lllll1l_opy_():
        bstack1l11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨṣ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦṤ").format(os.getenv(bstack1l11l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤṥ")))))
    @staticmethod
    def bstack1111lllllll_opy_(test_name: str):
        bstack1l11l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤṦ")
        bstack1111lll1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧṧ").format(os.getenv(bstack1l11l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧṨ"))))
        with open(bstack1111lll1l11_opy_, bstack1l11l11_opy_ (u"ࠨࡣࠪṩ")) as file:
            file.write(bstack1l11l11_opy_ (u"ࠤࡾࢁࡡࡴࠢṪ").format(test_name))
    @staticmethod
    def bstack1111llll1ll_opy_(framework: str) -> bool:
       return framework.lower() in bstack1111lll1ll1_opy_
    @staticmethod
    def bstack11l1l11l1ll_opy_(config: dict) -> bool:
        bstack1111lll11ll_opy_ = config.get(bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧṫ"), {}).get(bstack1111llll1l1_opy_, {})
        return bstack1111lll11ll_opy_.get(bstack1l11l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬṬ"), False)
    @staticmethod
    def bstack11l1l1l1lll_opy_(config: dict, bstack11l1l1l11l1_opy_: int = 0) -> int:
        bstack1l11l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠬࠡࡹ࡫࡭ࡨ࡮ࠠࡤࡣࡱࠤࡧ࡫ࠠࡢࡰࠣࡥࡧࡹ࡯࡭ࡷࡷࡩࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡲࠡࡣࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡱࡷࡥࡱࡥࡴࡦࡵࡷࡷࠥ࠮ࡩ࡯ࡶࠬ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࠬࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥṭ")
        bstack1111lll11ll_opy_ = config.get(bstack1l11l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪṮ"), {}).get(bstack1l11l11_opy_ (u"ࠧࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭ṯ"), {})
        bstack111l11111ll_opy_ = 0
        bstack111l1111ll1_opy_ = 0
        if bstack11l11l1lll_opy_.bstack11l1l11l1ll_opy_(config):
            bstack111l1111ll1_opy_ = bstack1111lll11ll_opy_.get(bstack1l11l11_opy_ (u"ࠨ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸ࠭Ṱ"), 5)
            if isinstance(bstack111l1111ll1_opy_, str) and bstack111l1111ll1_opy_.endswith(bstack1l11l11_opy_ (u"ࠩࠨࠫṱ")):
                try:
                    percentage = int(bstack111l1111ll1_opy_.strip(bstack1l11l11_opy_ (u"ࠪࠩࠬṲ")))
                    if bstack11l1l1l11l1_opy_ > 0:
                        bstack111l11111ll_opy_ = math.ceil((percentage * bstack11l1l1l11l1_opy_) / 100)
                    else:
                        raise ValueError(bstack1l11l11_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡰࡹࡸࡺࠠࡣࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠳ࡢࡢࡵࡨࡨࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࡴ࠰ࠥṳ"))
                except ValueError as e:
                    raise ValueError(bstack1l11l11_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧࠣࡺࡦࡲࡵࡦࠢࡩࡳࡷࠦ࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶ࠾ࠥࢁࡽࠣṴ").format(bstack111l1111ll1_opy_)) from e
            else:
                bstack111l11111ll_opy_ = int(bstack111l1111ll1_opy_)
        logger.info(bstack1l11l11_opy_ (u"ࠨࡍࡢࡺࠣࡪࡦ࡯࡬ࡶࡴࡨࡷࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡵࡨࡸࠥࡺ࡯࠻ࠢࡾࢁࠥ࠮ࡦࡳࡱࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽࠪࠤṵ").format(bstack111l11111ll_opy_, bstack111l1111ll1_opy_))
        return bstack111l11111ll_opy_
    def bstack1111lll11l1_opy_(self):
        return self.bstack111l1111l1l_opy_
    def bstack111l11l1l11_opy_(self):
        return self.bstack111l111llll_opy_
    def __1111llllll1_opy_(self, enabled, mode):
        self.bstack111l1111l1l_opy_ = bool(enabled)
        self.bstack111l111llll_opy_ = mode
        self.__111l111lll1_opy_()
    def bstack1111ll1llll_opy_(self):
        return self.bstack1111lll1111_opy_
    def __111l11l111l_opy_(self, value):
        self.bstack1111lll1111_opy_ = bool(value)
        self.__111l111lll1_opy_()
    def bstack111l11l11l1_opy_(self):
        return self.bstack1111lll1l1l_opy_
    def __1111lll111l_opy_(self, value):
        self.bstack1111lll1l1l_opy_ = bool(value)
        self.__111l111lll1_opy_()
    def bstack1111lll1lll_opy_(self):
        return self.bstack111l11l11ll_opy_
    def __111l111l111_opy_(self, value):
        self.bstack111l11l11ll_opy_ = bool(value)
        self.__111l111lll1_opy_()
    def __111l111lll1_opy_(self):
        if self.bstack111l1111l1l_opy_:
            self.bstack1111lll1111_opy_ = False
            self.bstack1111lll1l1l_opy_ = False
            self.bstack111l11l11ll_opy_ = False
            self.bstack111l111l11l_opy_.enable(bstack111l1111111_opy_)
        elif self.bstack1111lll1111_opy_:
            self.bstack1111lll1l1l_opy_ = False
            self.bstack111l11l11ll_opy_ = False
            self.bstack111l111l11l_opy_.enable(bstack1111llll11l_opy_)
        elif self.bstack1111lll1l1l_opy_:
            self.bstack1111lll1111_opy_ = False
            self.bstack111l11l11ll_opy_ = False
            self.bstack111l111l11l_opy_.enable(bstack1111ll1lll1_opy_)
        elif self.bstack111l11l11ll_opy_:
            self.bstack1111lll1111_opy_ = False
            self.bstack1111lll1l1l_opy_ = False
            self.bstack111l111l11l_opy_.enable(bstack111l111ll11_opy_)
        else:
            self.bstack111l111l11l_opy_.disable()
    def bstack11l1l1lll1_opy_(self):
        return self.bstack111l111l11l_opy_.bstack111l111111l_opy_()
    def bstack1ll11111_opy_(self):
        if self.bstack111l111l11l_opy_.bstack111l111111l_opy_():
            return self.bstack111l111l11l_opy_.get_name()
        return None
    def bstack111l11ll11l_opy_(self):
        return {
            bstack1l11l11_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭Ṷ") : {
                bstack1l11l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩṷ"): self.bstack1111lll11l1_opy_(),
                bstack1l11l11_opy_ (u"ࠩࡰࡳࡩ࡫ࠧṸ"): self.bstack111l11l1l11_opy_()
            }
        }
    def bstack111l111ll1l_opy_(self, config):
        bstack111l11l1111_opy_ = {}
        bstack111l11l1111_opy_[bstack1l11l11_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩṹ")] = {
            bstack1l11l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬṺ"): self.bstack1111lll11l1_opy_(),
            bstack1l11l11_opy_ (u"ࠬࡳ࡯ࡥࡧࠪṻ"): self.bstack111l11l1l11_opy_()
        }
        bstack111l11l1111_opy_[bstack1l11l11_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࠩṼ")] = {
            bstack1l11l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨṽ"): self.bstack111l11l11l1_opy_()
        }
        bstack111l11l1111_opy_[bstack1l11l11_opy_ (u"ࠨࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࡡࡩ࡭ࡷࡹࡴࠨṾ")] = {
            bstack1l11l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṿ"): self.bstack1111ll1llll_opy_()
        }
        bstack111l11l1111_opy_[bstack1l11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡨࡤ࡭ࡱ࡯࡮ࡨࡡࡤࡲࡩࡥࡦ࡭ࡣ࡮ࡽࠬẀ")] = {
            bstack1l11l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬẁ"): self.bstack1111lll1lll_opy_()
        }
        if self.bstack1l11ll1l1l_opy_(config):
            bstack111l11l1111_opy_[bstack1l11l11_opy_ (u"ࠬࡸࡥࡵࡴࡼࡣࡹ࡫ࡳࡵࡵࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧẂ")] = {
                bstack1l11l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧẃ"): True,
                bstack1l11l11_opy_ (u"ࠧ࡮ࡣࡻࡣࡷ࡫ࡴࡳ࡫ࡨࡷࠬẄ"): self.bstack1l1lll11l1_opy_(config)
            }
        if self.bstack11l1l11l1ll_opy_(config):
            bstack111l11l1111_opy_[bstack1l11l11_opy_ (u"ࠨࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡯࡯ࡡࡩࡥ࡮ࡲࡵࡳࡧࠪẅ")] = {
                bstack1l11l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪẆ"): True,
                bstack1l11l11_opy_ (u"ࠪࡱࡦࡾ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡴࠩẇ"): self.bstack11l1l1l1lll_opy_(config)
            }
        return bstack111l11l1111_opy_
    def bstack11lll11l11_opy_(self, config):
        bstack1l11l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡲࡰࡱ࡫ࡣࡵࡵࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡣࡻࠣࡱࡦࡱࡩ࡯ࡩࠣࡥࠥࡩࡡ࡭࡮ࠣࡸࡴࠦࡴࡩࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠡࡧࡱࡨࡵࡵࡩ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠦࠨࡴࡶࡵ࠭࠿ࠦࡔࡩࡧ࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡤࡸ࡭ࡱࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢẈ")
        bstack111l111l1l1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪẉ"), None)
        logger.debug(bstack1l11l11_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࡀࠠࡼࡿࠥẊ").format(bstack111l111l1l1_opy_))
        try:
            bstack11ll11l1l1l_opy_ = bstack1l11l11_opy_ (u"ࠢࡵࡧࡶࡸࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠧẋ").format(bstack111l111l1l1_opy_)
            payload = {
                bstack1l11l11_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨẌ"): config.get(bstack1l11l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧẍ"), bstack1l11l11_opy_ (u"ࠪࠫẎ")),
                bstack1l11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢẏ"): config.get(bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨẐ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦẑ"): os.environ.get(bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭Ẓ"), None),
                bstack1l11l11_opy_ (u"ࠣࡰࡲࡨࡪࡏ࡮ࡥࡧࡻࠦẓ"): int(os.environ.get(bstack1l11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧẔ")) or bstack1l11l11_opy_ (u"ࠥ࠴ࠧẕ")),
                bstack1l11l11_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࡑࡳࡩ࡫ࡳࠣẖ"): int(os.environ.get(bstack1l11l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢẗ")) or bstack1l11l11_opy_ (u"ࠨ࠱ࠣẘ")),
                bstack1l11l11_opy_ (u"ࠢࡩࡱࡶࡸࡎࡴࡦࡰࠤẙ"): get_host_info(),
                bstack1l11l11_opy_ (u"ࠣࡲࡵࡈࡪࡺࡡࡪ࡮ࡶࠦẚ"): bstack11l1111lll1_opy_()
            }
            logger.debug(bstack1l11l11_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡶࡡࡺ࡮ࡲࡥࡩࡀࠠࡼࡿࠥẛ").format(payload))
            response = bstack11ll11l111l_opy_.bstack111l11111l1_opy_(bstack11ll11l1l1l_opy_, payload)
            if response:
                logger.debug(bstack1l11l11_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡄࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣẜ").format(response))
                return response
            else:
                logger.error(bstack1l11l11_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣẝ").format(bstack111l111l1l1_opy_))
                return None
        except Exception as e:
            logger.error(bstack1l11l11_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇࠤࢀࢃ࠺ࠡࡽࢀࠦẞ").format(bstack111l111l1l1_opy_, e))
            return None