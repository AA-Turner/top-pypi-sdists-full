# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1lll1llll_opy_
from bstack_utils.constants import bstack1ll1l1lll_opy_, bstack11l1l1l11l1_opy_
from bstack_utils.helper import bstack111ll111l11_opy_, get_host_info
from bstack_utils.bstack11ll1111l11_opy_ import bstack11ll11111l1_opy_
bstack1111l1ll11l_opy_ = bstack1ll11ll_opy_ (u"ࠨࡲࡦࡶࡵࡽ࡙࡫ࡳࡵࡵࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠧṒ")
bstack1111ll11111_opy_ = bstack1ll11ll_opy_ (u"ࠢࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨṓ")
bstack1111lllll1l_opy_ = bstack1ll11ll_opy_ (u"ࠣࡴࡸࡲࡕࡸࡥࡷ࡫ࡲࡹࡸࡲࡹࡇࡣ࡬ࡰࡪࡪࡆࡪࡴࡶࡸࠧṔ")
bstack1111ll1l11l_opy_ = bstack1ll11ll_opy_ (u"ࠤࡵࡩࡷࡻ࡮ࡑࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡊࡦ࡯࡬ࡦࡦࠥṕ")
bstack1111lll1l1l_opy_ = bstack1ll11ll_opy_ (u"ࠥࡷࡰ࡯ࡰࡇ࡮ࡤ࡯ࡾࡧ࡮ࡥࡈࡤ࡭ࡱ࡫ࡤࠣṖ")
bstack111l11111ll_opy_ = bstack1ll11ll_opy_ (u"ࠦࡷࡻ࡮ࡔ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠣṗ")
bstack1111ll1ll1l_opy_ = {
    bstack1111l1ll11l_opy_,
    bstack1111ll11111_opy_,
    bstack1111lllll1l_opy_,
    bstack1111ll1l11l_opy_,
    bstack1111lll1l1l_opy_,
    bstack111l11111ll_opy_
}
bstack1111lll11ll_opy_ = {bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬṘ")}
logger = bstack1lll1llll_opy_.get_logger(__name__, bstack1ll1l1lll_opy_)
class bstack1111lll1111_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1111ll111ll_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1ll1l111_opy_:
    _1lll111l11l_opy_ = None
    def __init__(self, config):
        self.bstack1111l1l1lll_opy_ = False
        self.bstack1111lllllll_opy_ = False
        self.bstack111l111111l_opy_ = False
        self.bstack1111ll1lll1_opy_ = False
        self.bstack1111ll1ll11_opy_ = None
        self.bstack1111ll11lll_opy_ = bstack1111lll1111_opy_()
        self.bstack1111ll11l1l_opy_ = None
        opts = config.get(bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪṙ"), {})
        bstack1111llll11l_opy_ = opts.get(bstack111l11111ll_opy_, {})
        self.__1111ll1l1ll_opy_(
            bstack1111llll11l_opy_.get(bstack1ll11ll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨṚ"), False),
            bstack1111llll11l_opy_.get(bstack1ll11ll_opy_ (u"ࠨ࡯ࡲࡨࡪ࠭ṛ"), bstack1ll11ll_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡊ࡮ࡸࡳࡵࠩṜ")),
            bstack1111llll11l_opy_.get(bstack1ll11ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪṝ"), None)
        )
        self.__1111ll1l111_opy_(opts.get(bstack1111lllll1l_opy_, False))
        self.__111l1111111_opy_(opts.get(bstack1111ll1l11l_opy_, False))
        self.__1111llll111_opy_(opts.get(bstack1111lll1l1l_opy_, False))
    @classmethod
    def bstack11l11lllll_opy_(cls, config=None):
        if cls._1lll111l11l_opy_ is None and config is not None:
            cls._1lll111l11l_opy_ = bstack1ll1l111_opy_(config)
        return cls._1lll111l11l_opy_
    @staticmethod
    def bstack11l1lll11_opy_(config: dict) -> bool:
        bstack1111lll1lll_opy_ = config.get(bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨṞ"), {}).get(bstack1111l1ll11l_opy_, {})
        return bstack1111lll1lll_opy_.get(bstack1ll11ll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ṟ"), False)
    @staticmethod
    def bstack1ll11ll1l_opy_(config: dict) -> int:
        bstack1111lll1lll_opy_ = config.get(bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪṠ"), {}).get(bstack1111l1ll11l_opy_, {})
        retries = 0
        if bstack1ll1l111_opy_.bstack11l1lll11_opy_(config):
            retries = bstack1111lll1lll_opy_.get(bstack1ll11ll_opy_ (u"ࠧ࡮ࡣࡻࡖࡪࡺࡲࡪࡧࡶࠫṡ"), 1)
        return retries
    @staticmethod
    def bstack11l1ll1l1l_opy_(config: dict) -> dict:
        bstack1111l1ll1l1_opy_ = config.get(bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬṢ"), {})
        return {
            key: value for key, value in bstack1111l1ll1l1_opy_.items() if key in bstack1111ll1ll1l_opy_
        }
    @staticmethod
    def bstack1111lll111l_opy_():
        bstack1ll11ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨṣ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦṤ").format(os.getenv(bstack1ll11ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤṥ")))))
    @staticmethod
    def bstack1111l1lllll_opy_(test_name: str):
        bstack1ll11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤṦ")
        bstack1111l1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧṧ").format(os.getenv(bstack1ll11ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧṨ"))))
        with open(bstack1111l1ll111_opy_, bstack1ll11ll_opy_ (u"ࠨࡣࠪṩ")) as file:
            file.write(bstack1ll11ll_opy_ (u"ࠤࡾࢁࡡࡴࠢṪ").format(test_name))
    @staticmethod
    def bstack1111l1lll1l_opy_(framework: str) -> bool:
       return framework.lower() in bstack1111lll11ll_opy_
    @staticmethod
    def bstack11l11ll1ll1_opy_(config: dict) -> bool:
        bstack1111ll1llll_opy_ = config.get(bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧṫ"), {}).get(bstack1111ll11111_opy_, {})
        return bstack1111ll1llll_opy_.get(bstack1ll11ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬṬ"), False)
    @staticmethod
    def bstack11l1l11l1ll_opy_(config: dict, bstack11l1l11l11l_opy_: int = 0) -> int:
        bstack1ll11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠬࠡࡹ࡫࡭ࡨ࡮ࠠࡤࡣࡱࠤࡧ࡫ࠠࡢࡰࠣࡥࡧࡹ࡯࡭ࡷࡷࡩࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡲࠡࡣࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡱࡷࡥࡱࡥࡴࡦࡵࡷࡷࠥ࠮ࡩ࡯ࡶࠬ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࠬࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥṭ")
        bstack1111ll1llll_opy_ = config.get(bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪṮ"), {}).get(bstack1ll11ll_opy_ (u"ࠧࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭ṯ"), {})
        bstack1111llll1l1_opy_ = 0
        bstack1111ll111l1_opy_ = 0
        if bstack1ll1l111_opy_.bstack11l11ll1ll1_opy_(config):
            bstack1111ll111l1_opy_ = bstack1111ll1llll_opy_.get(bstack1ll11ll_opy_ (u"ࠨ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸ࠭Ṱ"), 5)
            if isinstance(bstack1111ll111l1_opy_, str) and bstack1111ll111l1_opy_.endswith(bstack1ll11ll_opy_ (u"ࠩࠨࠫṱ")):
                try:
                    percentage = int(bstack1111ll111l1_opy_.strip(bstack1ll11ll_opy_ (u"ࠪࠩࠬṲ")))
                    if bstack11l1l11l11l_opy_ > 0:
                        bstack1111llll1l1_opy_ = math.ceil((percentage * bstack11l1l11l11l_opy_) / 100)
                    else:
                        raise ValueError(bstack1ll11ll_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡰࡹࡸࡺࠠࡣࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠳ࡢࡢࡵࡨࡨࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࡴ࠰ࠥṳ"))
                except ValueError as e:
                    raise ValueError(bstack1ll11ll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧࠣࡺࡦࡲࡵࡦࠢࡩࡳࡷࠦ࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶ࠾ࠥࢁࡽࠣṴ").format(bstack1111ll111l1_opy_)) from e
            else:
                bstack1111llll1l1_opy_ = int(bstack1111ll111l1_opy_)
        logger.info(bstack1ll11ll_opy_ (u"ࠨࡍࡢࡺࠣࡪࡦ࡯࡬ࡶࡴࡨࡷࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡵࡨࡸࠥࡺ࡯࠻ࠢࡾࢁࠥ࠮ࡦࡳࡱࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽࠪࠤṵ").format(bstack1111llll1l1_opy_, bstack1111ll111l1_opy_))
        return bstack1111llll1l1_opy_
    def bstack1111llllll1_opy_(self):
        return self.bstack1111ll1lll1_opy_
    def bstack1111lll1ll1_opy_(self):
        return self.bstack1111ll1ll11_opy_
    def bstack1111l1ll1ll_opy_(self):
        return self.bstack1111ll11l1l_opy_
    def __1111ll1l1ll_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1111ll1lll1_opy_ = bool(enabled)
            self.bstack1111ll1ll11_opy_ = mode
            if source is None:
                self.bstack1111ll11l1l_opy_ = []
            elif isinstance(source, list):
                self.bstack1111ll11l1l_opy_ = source
            self.__1111lllll11_opy_()
        except Exception as e:
            logger.error(bstack1ll11ll_opy_ (u"ࠢ࡜ࡡࡢࡷࡪࡺ࡟ࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࡣࠠࠡࡽࢀࠦṶ").format(e))
    def bstack1111ll11l11_opy_(self):
        return self.bstack1111l1l1lll_opy_
    def __1111ll1l111_opy_(self, value):
        self.bstack1111l1l1lll_opy_ = bool(value)
        self.__1111lllll11_opy_()
    def bstack111l11111l1_opy_(self):
        return self.bstack1111lllllll_opy_
    def __111l1111111_opy_(self, value):
        self.bstack1111lllllll_opy_ = bool(value)
        self.__1111lllll11_opy_()
    def bstack1111ll1111l_opy_(self):
        return self.bstack111l111111l_opy_
    def __1111llll111_opy_(self, value):
        self.bstack111l111111l_opy_ = bool(value)
        self.__1111lllll11_opy_()
    def __1111lllll11_opy_(self):
        if self.bstack1111ll1lll1_opy_:
            self.bstack1111l1l1lll_opy_ = False
            self.bstack1111lllllll_opy_ = False
            self.bstack111l111111l_opy_ = False
            self.bstack1111ll11lll_opy_.enable(bstack111l11111ll_opy_)
        elif self.bstack1111l1l1lll_opy_:
            self.bstack1111lllllll_opy_ = False
            self.bstack111l111111l_opy_ = False
            self.bstack1111ll1lll1_opy_ = False
            self.bstack1111ll11lll_opy_.enable(bstack1111lllll1l_opy_)
        elif self.bstack1111lllllll_opy_:
            self.bstack1111l1l1lll_opy_ = False
            self.bstack111l111111l_opy_ = False
            self.bstack1111ll1lll1_opy_ = False
            self.bstack1111ll11lll_opy_.enable(bstack1111ll1l11l_opy_)
        elif self.bstack111l111111l_opy_:
            self.bstack1111l1l1lll_opy_ = False
            self.bstack1111lllllll_opy_ = False
            self.bstack1111ll1lll1_opy_ = False
            self.bstack1111ll11lll_opy_.enable(bstack1111lll1l1l_opy_)
        else:
            self.bstack1111ll11lll_opy_.disable()
    def bstack11l11l11ll_opy_(self):
        return self.bstack1111ll11lll_opy_.bstack1111ll111ll_opy_()
    def bstack1l1ll1l111_opy_(self):
        if self.bstack1111ll11lll_opy_.bstack1111ll111ll_opy_():
            return self.bstack1111ll11lll_opy_.get_name()
        return None
    def bstack111l11l11l1_opy_(self):
        data = {
            bstack1ll11ll_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧṷ"): {
                bstack1ll11ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṸ"): self.bstack1111llllll1_opy_(),
                bstack1ll11ll_opy_ (u"ࠪࡱࡴࡪࡥࠨṹ"): self.bstack1111lll1ll1_opy_(),
                bstack1ll11ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫṺ"): self.bstack1111l1ll1ll_opy_()
            }
        }
        return data
    def bstack1111lll11l1_opy_(self, config):
        bstack1111lll1l11_opy_ = {}
        bstack1111lll1l11_opy_[bstack1ll11ll_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫṻ")] = {
            bstack1ll11ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧṼ"): self.bstack1111llllll1_opy_(),
            bstack1ll11ll_opy_ (u"ࠧ࡮ࡱࡧࡩࠬṽ"): self.bstack1111lll1ll1_opy_()
        }
        bstack1111lll1l11_opy_[bstack1ll11ll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟ࡱࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡣ࡫ࡧࡩ࡭ࡧࡧࠫṾ")] = {
            bstack1ll11ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṿ"): self.bstack111l11111l1_opy_()
        }
        bstack1111lll1l11_opy_[bstack1ll11ll_opy_ (u"ࠪࡶࡺࡴ࡟ࡱࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡣ࡫ࡧࡩ࡭ࡧࡧࡣ࡫࡯ࡲࡴࡶࠪẀ")] = {
            bstack1ll11ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬẁ"): self.bstack1111ll11l11_opy_()
        }
        bstack1111lll1l11_opy_[bstack1ll11ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡪࡦ࡯࡬ࡪࡰࡪࡣࡦࡴࡤࡠࡨ࡯ࡥࡰࡿࠧẂ")] = {
            bstack1ll11ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧẃ"): self.bstack1111ll1111l_opy_()
        }
        if self.bstack11l1lll11_opy_(config):
            bstack1111lll1l11_opy_[bstack1ll11ll_opy_ (u"ࠧࡳࡧࡷࡶࡾࡥࡴࡦࡵࡷࡷࡤࡵ࡮ࡠࡨࡤ࡭ࡱࡻࡲࡦࠩẄ")] = {
                bstack1ll11ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩẅ"): True,
                bstack1ll11ll_opy_ (u"ࠩࡰࡥࡽࡥࡲࡦࡶࡵ࡭ࡪࡹࠧẆ"): self.bstack1ll11ll1l_opy_(config)
            }
        if self.bstack11l11ll1ll1_opy_(config):
            bstack1111lll1l11_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡱࡱࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠬẇ")] = {
                bstack1ll11ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬẈ"): True,
                bstack1ll11ll_opy_ (u"ࠬࡳࡡࡹࡡࡩࡥ࡮ࡲࡵࡳࡧࡶࠫẉ"): self.bstack11l1l11l1ll_opy_(config)
            }
        return bstack1111lll1l11_opy_
    def bstack111ll11ll_opy_(self, config):
        bstack1ll11ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡴࡲ࡬ࡦࡥࡷࡷࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡥࡽࠥࡳࡡ࡬࡫ࡱ࡫ࠥࡧࠠࡤࡣ࡯ࡰࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩ࡛ࠥࡕࡊࡆࠣࡳ࡫ࠦࡴࡩࡧࠣࡦࡺ࡯࡬ࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤẊ")
        if not (config.get(bstack1ll11ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪẋ"), None) in bstack11l1l1l11l1_opy_ and self.bstack1111llllll1_opy_()):
            return None
        bstack1111ll1l1l1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭Ẍ"), None)
        logger.debug(bstack1ll11ll_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡄࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨẍ").format(bstack1111ll1l1l1_opy_))
        try:
            bstack11ll1111ll1_opy_ = bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠣẎ").format(bstack1111ll1l1l1_opy_)
            bstack1111l1lll11_opy_ = self.bstack1111l1ll1ll_opy_() or [] # for multi-repo
            bstack1111ll11ll1_opy_ = bstack111ll111l11_opy_(bstack1111l1lll11_opy_) # bstack111ll11ll1l_opy_-repo is handled bstack1111l1llll1_opy_
            payload = {
                bstack1ll11ll_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤẏ"): config.get(bstack1ll11ll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪẐ"), bstack1ll11ll_opy_ (u"࠭ࠧẑ")),
                bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥẒ"): config.get(bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫẓ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢẔ"): config.get(bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬẕ"), bstack1ll11ll_opy_ (u"ࠫࠬẖ")),
                bstack1ll11ll_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣẗ"): int(os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤẘ")) or bstack1ll11ll_opy_ (u"ࠢ࠱ࠤẙ")),
                bstack1ll11ll_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧẚ"): int(os.environ.get(bstack1ll11ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦẛ")) or bstack1ll11ll_opy_ (u"ࠥ࠵ࠧẜ")),
                bstack1ll11ll_opy_ (u"ࠦ࡭ࡵࡳࡵࡋࡱࡪࡴࠨẝ"): get_host_info(),
                bstack1ll11ll_opy_ (u"ࠧࡶࡲࡅࡧࡷࡥ࡮ࡲࡳࠣẞ"): bstack1111ll11ll1_opy_
            }
            logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡳࡥࡾࡲ࡯ࡢࡦ࠽ࠤࢀࢃࠢẟ").format(payload))
            response = bstack11ll11111l1_opy_.bstack1111llll1ll_opy_(bstack11ll1111ll1_opy_, payload)
            if response:
                logger.debug(bstack1ll11ll_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡈࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧẠ").format(response))
                return response
            else:
                logger.error(bstack1ll11ll_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦ࡙࡚ࠣࡏࡄ࠻ࠢࡾࢁࠧạ").format(bstack1111ll1l1l1_opy_))
                return None
        except Exception as e:
            logger.error(bstack1ll11ll_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡰ࡮࡯ࡩࡨࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦ࡙࡚ࠣࡏࡄࠡࡽࢀ࠾ࠥࢁࡽࠣẢ").format(bstack1111ll1l1l1_opy_, e))
            return None