# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1l1l11lll1_opy_
from bstack_utils.constants import bstack1l111lll11_opy_
from bstack_utils.helper import bstack11l111ll1l1_opy_, get_host_info
from bstack_utils.bstack11ll11l1ll1_opy_ import bstack11ll11l1l1l_opy_
bstack111l1111lll_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡳࡧࡷࡶࡾ࡚ࡥࡴࡶࡶࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨṡ")
bstack1111lll111l_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢṢ")
bstack111l11l11l1_opy_ = bstack1l1l1ll_opy_ (u"ࠤࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࡇ࡫ࡵࡷࡹࠨṣ")
bstack111l1111ll1_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡶࡪࡸࡵ࡯ࡒࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡋࡧࡩ࡭ࡧࡧࠦṤ")
bstack1111lll1l11_opy_ = bstack1l1l1ll_opy_ (u"ࠦࡸࡱࡩࡱࡈ࡯ࡥࡰࡿࡡ࡯ࡦࡉࡥ࡮ࡲࡥࡥࠤṥ")
bstack1111lll1lll_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡸࡵ࡯ࡕࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠤṦ")
bstack111l11l11ll_opy_ = {
    bstack111l1111lll_opy_,
    bstack1111lll111l_opy_,
    bstack111l11l11l1_opy_,
    bstack111l1111ll1_opy_,
    bstack1111lll1l11_opy_,
    bstack1111lll1lll_opy_
}
bstack111l11l1ll1_opy_ = {bstack1l1l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ṧ")}
logger = bstack1l1l11lll1_opy_.get_logger(__name__, bstack1l111lll11_opy_)
class bstack1111lllll11_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack111l11111ll_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l1l1llll1_opy_:
    _1llll11ll11_opy_ = None
    def __init__(self, config):
        self.bstack111l11l1l1l_opy_ = False
        self.bstack111l1111l1l_opy_ = False
        self.bstack111l1111l11_opy_ = False
        self.bstack1111llllll1_opy_ = False
        self.bstack111l111lll1_opy_ = None
        self.bstack1111llll11l_opy_ = bstack1111lllll11_opy_()
        opts = config.get(bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫṨ"), {})
        self.__1111lll11ll_opy_(opts.get(bstack1111lll1lll_opy_, {}).get(bstack1l1l1ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩṩ"), False),
                                       opts.get(bstack1111lll1lll_opy_, {}).get(bstack1l1l1ll_opy_ (u"ࠩࡰࡳࡩ࡫ࠧṪ"), bstack1l1l1ll_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪṫ")))
        self.__111l111ll1l_opy_(opts.get(bstack111l11l11l1_opy_, False))
        self.__111l111llll_opy_(opts.get(bstack111l1111ll1_opy_, False))
        self.__111l111l11l_opy_(opts.get(bstack1111lll1l11_opy_, False))
    @classmethod
    def bstack11l1lllll1_opy_(cls, config=None):
        if cls._1llll11ll11_opy_ is None and config is not None:
            cls._1llll11ll11_opy_ = bstack1l1l1llll1_opy_(config)
        return cls._1llll11ll11_opy_
    @staticmethod
    def bstack11111llll_opy_(config: dict) -> bool:
        bstack1111lllll1l_opy_ = config.get(bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨṬ"), {}).get(bstack111l1111lll_opy_, {})
        return bstack1111lllll1l_opy_.get(bstack1l1l1ll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ṭ"), False)
    @staticmethod
    def bstack1l11l111_opy_(config: dict) -> int:
        bstack1111lllll1l_opy_ = config.get(bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪṮ"), {}).get(bstack111l1111lll_opy_, {})
        retries = 0
        if bstack1l1l1llll1_opy_.bstack11111llll_opy_(config):
            retries = bstack1111lllll1l_opy_.get(bstack1l1l1ll_opy_ (u"ࠧ࡮ࡣࡻࡖࡪࡺࡲࡪࡧࡶࠫṯ"), 1)
        return retries
    @staticmethod
    def bstack1l1lllll1l_opy_(config: dict) -> dict:
        bstack1111lll1ll1_opy_ = config.get(bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬṰ"), {})
        return {
            key: value for key, value in bstack1111lll1ll1_opy_.items() if key in bstack111l11l11ll_opy_
        }
    @staticmethod
    def bstack1111lllllll_opy_():
        bstack1l1l1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨṱ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦṲ").format(os.getenv(bstack1l1l1ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤṳ")))))
    @staticmethod
    def bstack111l111l1ll_opy_(test_name: str):
        bstack1l1l1ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤṴ")
        bstack111l111l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧṵ").format(os.getenv(bstack1l1l1ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧṶ"))))
        with open(bstack111l111l1l1_opy_, bstack1l1l1ll_opy_ (u"ࠨࡣࠪṷ")) as file:
            file.write(bstack1l1l1ll_opy_ (u"ࠤࡾࢁࡡࡴࠢṸ").format(test_name))
    @staticmethod
    def bstack1111lll1l1l_opy_(framework: str) -> bool:
       return framework.lower() in bstack111l11l1ll1_opy_
    @staticmethod
    def bstack11l1l1l1lll_opy_(config: dict) -> bool:
        bstack1111lll11l1_opy_ = config.get(bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧṹ"), {}).get(bstack1111lll111l_opy_, {})
        return bstack1111lll11l1_opy_.get(bstack1l1l1ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬṺ"), False)
    @staticmethod
    def bstack11l1l1l111l_opy_(config: dict, bstack11l1l1ll11l_opy_: int = 0) -> int:
        bstack1l1l1ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠬࠡࡹ࡫࡭ࡨ࡮ࠠࡤࡣࡱࠤࡧ࡫ࠠࡢࡰࠣࡥࡧࡹ࡯࡭ࡷࡷࡩࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡲࠡࡣࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡱࡷࡥࡱࡥࡴࡦࡵࡷࡷࠥ࠮ࡩ࡯ࡶࠬ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࠬࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥṻ")
        bstack1111lll11l1_opy_ = config.get(bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪṼ"), {}).get(bstack1l1l1ll_opy_ (u"ࠧࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭ṽ"), {})
        bstack111l11l111l_opy_ = 0
        bstack1111llll1ll_opy_ = 0
        if bstack1l1l1llll1_opy_.bstack11l1l1l1lll_opy_(config):
            bstack1111llll1ll_opy_ = bstack1111lll11l1_opy_.get(bstack1l1l1ll_opy_ (u"ࠨ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸ࠭Ṿ"), 5)
            if isinstance(bstack1111llll1ll_opy_, str) and bstack1111llll1ll_opy_.endswith(bstack1l1l1ll_opy_ (u"ࠩࠨࠫṿ")):
                try:
                    percentage = int(bstack1111llll1ll_opy_.strip(bstack1l1l1ll_opy_ (u"ࠪࠩࠬẀ")))
                    if bstack11l1l1ll11l_opy_ > 0:
                        bstack111l11l111l_opy_ = math.ceil((percentage * bstack11l1l1ll11l_opy_) / 100)
                    else:
                        raise ValueError(bstack1l1l1ll_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡰࡹࡸࡺࠠࡣࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠳ࡢࡢࡵࡨࡨࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࡴ࠰ࠥẁ"))
                except ValueError as e:
                    raise ValueError(bstack1l1l1ll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧࠣࡺࡦࡲࡵࡦࠢࡩࡳࡷࠦ࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶ࠾ࠥࢁࡽࠣẂ").format(bstack1111llll1ll_opy_)) from e
            else:
                bstack111l11l111l_opy_ = int(bstack1111llll1ll_opy_)
        logger.info(bstack1l1l1ll_opy_ (u"ࠨࡍࡢࡺࠣࡪࡦ࡯࡬ࡶࡴࡨࡷࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡵࡨࡸࠥࡺ࡯࠻ࠢࡾࢁࠥ࠮ࡦࡳࡱࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽࠪࠤẃ").format(bstack111l11l111l_opy_, bstack1111llll1ll_opy_))
        return bstack111l11l111l_opy_
    def bstack111l11l1111_opy_(self):
        return self.bstack1111llllll1_opy_
    def bstack111l11111l1_opy_(self):
        return self.bstack111l111lll1_opy_
    def __1111lll11ll_opy_(self, enabled, mode):
        self.bstack1111llllll1_opy_ = bool(enabled)
        self.bstack111l111lll1_opy_ = mode
        self.__1111llll111_opy_()
    def bstack111l111ll11_opy_(self):
        return self.bstack111l11l1l1l_opy_
    def __111l111ll1l_opy_(self, value):
        self.bstack111l11l1l1l_opy_ = bool(value)
        self.__1111llll111_opy_()
    def bstack111l111111l_opy_(self):
        return self.bstack111l1111l1l_opy_
    def __111l111llll_opy_(self, value):
        self.bstack111l1111l1l_opy_ = bool(value)
        self.__1111llll111_opy_()
    def bstack1111llll1l1_opy_(self):
        return self.bstack111l1111l11_opy_
    def __111l111l11l_opy_(self, value):
        self.bstack111l1111l11_opy_ = bool(value)
        self.__1111llll111_opy_()
    def __1111llll111_opy_(self):
        if self.bstack1111llllll1_opy_:
            self.bstack111l11l1l1l_opy_ = False
            self.bstack111l1111l1l_opy_ = False
            self.bstack111l1111l11_opy_ = False
            self.bstack1111llll11l_opy_.enable(bstack1111lll1lll_opy_)
        elif self.bstack111l11l1l1l_opy_:
            self.bstack111l1111l1l_opy_ = False
            self.bstack111l1111l11_opy_ = False
            self.bstack1111llll11l_opy_.enable(bstack111l11l11l1_opy_)
        elif self.bstack111l1111l1l_opy_:
            self.bstack111l11l1l1l_opy_ = False
            self.bstack111l1111l11_opy_ = False
            self.bstack1111llll11l_opy_.enable(bstack111l1111ll1_opy_)
        elif self.bstack111l1111l11_opy_:
            self.bstack111l11l1l1l_opy_ = False
            self.bstack111l1111l1l_opy_ = False
            self.bstack1111llll11l_opy_.enable(bstack1111lll1l11_opy_)
        else:
            self.bstack1111llll11l_opy_.disable()
    def bstack111111lll_opy_(self):
        return self.bstack1111llll11l_opy_.bstack111l11111ll_opy_()
    def bstack11llll1l_opy_(self):
        if self.bstack1111llll11l_opy_.bstack111l11111ll_opy_():
            return self.bstack1111llll11l_opy_.get_name()
        return None
    def bstack111l1l111ll_opy_(self):
        return {
            bstack1l1l1ll_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭Ẅ") : {
                bstack1l1l1ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩẅ"): self.bstack111l11l1111_opy_(),
                bstack1l1l1ll_opy_ (u"ࠩࡰࡳࡩ࡫ࠧẆ"): self.bstack111l11111l1_opy_()
            }
        }
    def bstack111l111l111_opy_(self, config):
        bstack111l11l1l11_opy_ = {}
        bstack111l11l1l11_opy_[bstack1l1l1ll_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩẇ")] = {
            bstack1l1l1ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬẈ"): self.bstack111l11l1111_opy_(),
            bstack1l1l1ll_opy_ (u"ࠬࡳ࡯ࡥࡧࠪẉ"): self.bstack111l11111l1_opy_()
        }
        bstack111l11l1l11_opy_[bstack1l1l1ll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࠩẊ")] = {
            bstack1l1l1ll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨẋ"): self.bstack111l111111l_opy_()
        }
        bstack111l11l1l11_opy_[bstack1l1l1ll_opy_ (u"ࠨࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࡡࡩ࡭ࡷࡹࡴࠨẌ")] = {
            bstack1l1l1ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪẍ"): self.bstack111l111ll11_opy_()
        }
        bstack111l11l1l11_opy_[bstack1l1l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡨࡤ࡭ࡱ࡯࡮ࡨࡡࡤࡲࡩࡥࡦ࡭ࡣ࡮ࡽࠬẎ")] = {
            bstack1l1l1ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬẏ"): self.bstack1111llll1l1_opy_()
        }
        if self.bstack11111llll_opy_(config):
            bstack111l11l1l11_opy_[bstack1l1l1ll_opy_ (u"ࠬࡸࡥࡵࡴࡼࡣࡹ࡫ࡳࡵࡵࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧẐ")] = {
                bstack1l1l1ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧẑ"): True,
                bstack1l1l1ll_opy_ (u"ࠧ࡮ࡣࡻࡣࡷ࡫ࡴࡳ࡫ࡨࡷࠬẒ"): self.bstack1l11l111_opy_(config)
            }
        if self.bstack11l1l1l1lll_opy_(config):
            bstack111l11l1l11_opy_[bstack1l1l1ll_opy_ (u"ࠨࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡯࡯ࡡࡩࡥ࡮ࡲࡵࡳࡧࠪẓ")] = {
                bstack1l1l1ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪẔ"): True,
                bstack1l1l1ll_opy_ (u"ࠪࡱࡦࡾ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡴࠩẕ"): self.bstack11l1l1l111l_opy_(config)
            }
        return bstack111l11l1l11_opy_
    def bstack1ll1111l_opy_(self, config):
        bstack1l1l1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡲࡰࡱ࡫ࡣࡵࡵࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡣࡻࠣࡱࡦࡱࡩ࡯ࡩࠣࡥࠥࡩࡡ࡭࡮ࠣࡸࡴࠦࡴࡩࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠡࡧࡱࡨࡵࡵࡩ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠦࠨࡴࡶࡵ࠭࠿ࠦࡔࡩࡧ࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡤࡸ࡭ࡱࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢẖ")
        bstack111l11l1lll_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪẗ"), None)
        logger.debug(bstack1l1l1ll_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࡀࠠࡼࡿࠥẘ").format(bstack111l11l1lll_opy_))
        try:
            bstack11ll11ll111_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡵࡧࡶࡸࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠧẙ").format(bstack111l11l1lll_opy_)
            payload = {
                bstack1l1l1ll_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨẚ"): config.get(bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧẛ"), bstack1l1l1ll_opy_ (u"ࠪࠫẜ")),
                bstack1l1l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢẝ"): config.get(bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨẞ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦẟ"): os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭Ạ"), None),
                bstack1l1l1ll_opy_ (u"ࠣࡰࡲࡨࡪࡏ࡮ࡥࡧࡻࠦạ"): int(os.environ.get(bstack1l1l1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧẢ")) or bstack1l1l1ll_opy_ (u"ࠥ࠴ࠧả")),
                bstack1l1l1ll_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࡑࡳࡩ࡫ࡳࠣẤ"): int(os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢấ")) or bstack1l1l1ll_opy_ (u"ࠨ࠱ࠣẦ")),
                bstack1l1l1ll_opy_ (u"ࠢࡩࡱࡶࡸࡎࡴࡦࡰࠤầ"): get_host_info(),
                bstack1l1l1ll_opy_ (u"ࠣࡲࡵࡈࡪࡺࡡࡪ࡮ࡶࠦẨ"): bstack11l111ll1l1_opy_()
            }
            logger.debug(bstack1l1l1ll_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡶࡡࡺ࡮ࡲࡥࡩࡀࠠࡼࡿࠥẩ").format(payload))
            response = bstack11ll11l1l1l_opy_.bstack111l1111111_opy_(bstack11ll11ll111_opy_, payload)
            if response:
                logger.debug(bstack1l1l1ll_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡄࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣẪ").format(response))
                return response
            else:
                logger.error(bstack1l1l1ll_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣẫ").format(bstack111l11l1lll_opy_))
                return None
        except Exception as e:
            logger.error(bstack1l1l1ll_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇࠤࢀࢃ࠺ࠡࡽࢀࠦẬ").format(bstack111l11l1lll_opy_, e))
            return None