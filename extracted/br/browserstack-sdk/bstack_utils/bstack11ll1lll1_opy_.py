# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1lll1l1l1l_opy_
from bstack_utils.constants import bstack11lllll1l1_opy_, bstack11l1l1ll11l_opy_
from bstack_utils.helper import bstack111llll1lll_opy_, get_host_info
from bstack_utils.bstack11ll111ll1l_opy_ import bstack11ll111l1ll_opy_
bstack1111ll111l1_opy_ = bstack1l11ll1_opy_ (u"ࠢࡳࡧࡷࡶࡾ࡚ࡥࡴࡶࡶࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨṌ")
bstack111l1111ll1_opy_ = bstack1l11ll1_opy_ (u"ࠣࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢṍ")
bstack1111ll1l1l1_opy_ = bstack1l11ll1_opy_ (u"ࠤࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࡇ࡫ࡵࡷࡹࠨṎ")
bstack111l1111l11_opy_ = bstack1l11ll1_opy_ (u"ࠥࡶࡪࡸࡵ࡯ࡒࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡋࡧࡩ࡭ࡧࡧࠦṏ")
bstack1111llllll1_opy_ = bstack1l11ll1_opy_ (u"ࠦࡸࡱࡩࡱࡈ࡯ࡥࡰࡿࡡ࡯ࡦࡉࡥ࡮ࡲࡥࡥࠤṐ")
bstack1111ll11l11_opy_ = bstack1l11ll1_opy_ (u"ࠧࡸࡵ࡯ࡕࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠤṑ")
bstack1111lll111l_opy_ = {
    bstack1111ll111l1_opy_,
    bstack111l1111ll1_opy_,
    bstack1111ll1l1l1_opy_,
    bstack111l1111l11_opy_,
    bstack1111llllll1_opy_,
    bstack1111ll11l11_opy_
}
bstack111l111l111_opy_ = {bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭Ṓ")}
logger = bstack1lll1l1l1l_opy_.get_logger(__name__, bstack11lllll1l1_opy_)
class bstack111l1111l1l_opy_:
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
class bstack11llll1111_opy_:
    _1ll1llllll1_opy_ = None
    def __init__(self, config):
        self.bstack1111lllll1l_opy_ = False
        self.bstack1111lll11l1_opy_ = False
        self.bstack1111ll1ll11_opy_ = False
        self.bstack111l11111ll_opy_ = False
        self.bstack111l111l11l_opy_ = None
        self.bstack1111llll1l1_opy_ = bstack111l1111l1l_opy_()
        self.bstack111l111l1l1_opy_ = None
        opts = config.get(bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫṓ"), {})
        bstack1111lll1111_opy_ = opts.get(bstack1111ll11l11_opy_, {})
        self.__1111lll11ll_opy_(
            bstack1111lll1111_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩṔ"), False),
            bstack1111lll1111_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡰࡳࡩ࡫ࠧṕ"), bstack1l11ll1_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪṖ")),
            bstack1111lll1111_opy_.get(bstack1l11ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫṗ"), None)
        )
        self.__1111lll1lll_opy_(opts.get(bstack1111ll1l1l1_opy_, False))
        self.__1111lllll11_opy_(opts.get(bstack111l1111l11_opy_, False))
        self.__1111lllllll_opy_(opts.get(bstack1111llllll1_opy_, False))
    @classmethod
    def bstack1lll111l1l_opy_(cls, config=None):
        if cls._1ll1llllll1_opy_ is None and config is not None:
            cls._1ll1llllll1_opy_ = bstack11llll1111_opy_(config)
        return cls._1ll1llllll1_opy_
    @staticmethod
    def bstack1ll1l111l_opy_(config: dict) -> bool:
        bstack111l111ll1l_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩṘ"), {}).get(bstack1111ll111l1_opy_, {})
        return bstack111l111ll1l_opy_.get(bstack1l11ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧṙ"), False)
    @staticmethod
    def bstack11l1l1l1ll_opy_(config: dict) -> int:
        bstack111l111ll1l_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫṚ"), {}).get(bstack1111ll111l1_opy_, {})
        retries = 0
        if bstack11llll1111_opy_.bstack1ll1l111l_opy_(config):
            retries = bstack111l111ll1l_opy_.get(bstack1l11ll1_opy_ (u"ࠨ࡯ࡤࡼࡗ࡫ࡴࡳ࡫ࡨࡷࠬṛ"), 1)
        return retries
    @staticmethod
    def bstack111lll1l1_opy_(config: dict) -> dict:
        bstack111l111111l_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭Ṝ"), {})
        return {
            key: value for key, value in bstack111l111111l_opy_.items() if key in bstack1111lll111l_opy_
        }
    @staticmethod
    def bstack1111llll11l_opy_():
        bstack1l11ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢṝ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧṞ").format(os.getenv(bstack1l11ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥṟ")))))
    @staticmethod
    def bstack1111ll1llll_opy_(test_name: str):
        bstack1l11ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥṠ")
        bstack1111llll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨṡ").format(os.getenv(bstack1l11ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨṢ"))))
        with open(bstack1111llll1ll_opy_, bstack1l11ll1_opy_ (u"ࠩࡤࠫṣ")) as file:
            file.write(bstack1l11ll1_opy_ (u"ࠥࡿࢂࡢ࡮ࠣṤ").format(test_name))
    @staticmethod
    def bstack1111lll1ll1_opy_(framework: str) -> bool:
       return framework.lower() in bstack111l111l111_opy_
    @staticmethod
    def bstack11l1l1111ll_opy_(config: dict) -> bool:
        bstack1111llll111_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨṥ"), {}).get(bstack111l1111ll1_opy_, {})
        return bstack1111llll111_opy_.get(bstack1l11ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭Ṧ"), False)
    @staticmethod
    def bstack11l1l111lll_opy_(config: dict, bstack11l1l1l1l11_opy_: int = 0) -> int:
        bstack1l11ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠭ࠢࡺ࡬࡮ࡩࡨࠡࡥࡤࡲࠥࡨࡥࠡࡣࡱࠤࡦࡨࡳࡰ࡮ࡸࡸࡪࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡳࠢࡤࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭ࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡲࡸࡦࡲ࡟ࡵࡧࡶࡸࡸࠦࠨࡪࡰࡷ࠭࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤ࠭ࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦṧ")
        bstack1111llll111_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫṨ"), {}).get(bstack1l11ll1_opy_ (u"ࠨࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧṩ"), {})
        bstack1111lll1l11_opy_ = 0
        bstack1111ll111ll_opy_ = 0
        if bstack11llll1111_opy_.bstack11l1l1111ll_opy_(config):
            bstack1111ll111ll_opy_ = bstack1111llll111_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹࠧṪ"), 5)
            if isinstance(bstack1111ll111ll_opy_, str) and bstack1111ll111ll_opy_.endswith(bstack1l11ll1_opy_ (u"ࠪࠩࠬṫ")):
                try:
                    percentage = int(bstack1111ll111ll_opy_.strip(bstack1l11ll1_opy_ (u"ࠫࠪ࠭Ṭ")))
                    if bstack11l1l1l1l11_opy_ > 0:
                        bstack1111lll1l11_opy_ = math.ceil((percentage * bstack11l1l1l1l11_opy_) / 100)
                    else:
                        raise ValueError(bstack1l11ll1_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡱࡺࡹࡴࠡࡤࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵ࠱ࠦṭ"))
                except ValueError as e:
                    raise ValueError(bstack1l11ll1_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨࠤࡻࡧ࡬ࡶࡧࠣࡪࡴࡸࠠ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷ࠿ࠦࡻࡾࠤṮ").format(bstack1111ll111ll_opy_)) from e
            else:
                bstack1111lll1l11_opy_ = int(bstack1111ll111ll_opy_)
        logger.info(bstack1l11ll1_opy_ (u"ࠢࡎࡣࡻࠤ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡶࡩࡹࠦࡴࡰ࠼ࠣࡿࢂࠦࠨࡧࡴࡲࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾࠫࠥṯ").format(bstack1111lll1l11_opy_, bstack1111ll111ll_opy_))
        return bstack1111lll1l11_opy_
    def bstack1111ll1l11l_opy_(self):
        return self.bstack111l11111ll_opy_
    def bstack1111ll11l1l_opy_(self):
        return self.bstack111l111l11l_opy_
    def bstack111l1111111_opy_(self):
        return self.bstack111l111l1l1_opy_
    def __1111lll11ll_opy_(self, enabled, mode, source=None):
        try:
            self.bstack111l11111ll_opy_ = bool(enabled)
            self.bstack111l111l11l_opy_ = mode
            if source is None:
                self.bstack111l111l1l1_opy_ = []
            elif isinstance(source, list):
                self.bstack111l111l1l1_opy_ = source
            self.__111l111l1ll_opy_()
        except Exception as e:
            logger.error(bstack1l11ll1_opy_ (u"ࠣ࡝ࡢࡣࡸ࡫ࡴࡠࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴ࡝ࠡࠢࡾࢁࠧṰ").format(e))
    def bstack1111lll1l1l_opy_(self):
        return self.bstack1111lllll1l_opy_
    def __1111lll1lll_opy_(self, value):
        self.bstack1111lllll1l_opy_ = bool(value)
        self.__111l111l1ll_opy_()
    def bstack111l1111lll_opy_(self):
        return self.bstack1111lll11l1_opy_
    def __1111lllll11_opy_(self, value):
        self.bstack1111lll11l1_opy_ = bool(value)
        self.__111l111l1ll_opy_()
    def bstack1111ll1ll1l_opy_(self):
        return self.bstack1111ll1ll11_opy_
    def __1111lllllll_opy_(self, value):
        self.bstack1111ll1ll11_opy_ = bool(value)
        self.__111l111l1ll_opy_()
    def __111l111l1ll_opy_(self):
        if self.bstack111l11111ll_opy_:
            self.bstack1111lllll1l_opy_ = False
            self.bstack1111lll11l1_opy_ = False
            self.bstack1111ll1ll11_opy_ = False
            self.bstack1111llll1l1_opy_.enable(bstack1111ll11l11_opy_)
        elif self.bstack1111lllll1l_opy_:
            self.bstack1111lll11l1_opy_ = False
            self.bstack1111ll1ll11_opy_ = False
            self.bstack111l11111ll_opy_ = False
            self.bstack1111llll1l1_opy_.enable(bstack1111ll1l1l1_opy_)
        elif self.bstack1111lll11l1_opy_:
            self.bstack1111lllll1l_opy_ = False
            self.bstack1111ll1ll11_opy_ = False
            self.bstack111l11111ll_opy_ = False
            self.bstack1111llll1l1_opy_.enable(bstack111l1111l11_opy_)
        elif self.bstack1111ll1ll11_opy_:
            self.bstack1111lllll1l_opy_ = False
            self.bstack1111lll11l1_opy_ = False
            self.bstack111l11111ll_opy_ = False
            self.bstack1111llll1l1_opy_.enable(bstack1111llllll1_opy_)
        else:
            self.bstack1111llll1l1_opy_.disable()
    def bstack1l1lll1lll_opy_(self):
        return self.bstack1111llll1l1_opy_.bstack111l11111l1_opy_()
    def bstack111l1llll_opy_(self):
        if self.bstack1111llll1l1_opy_.bstack111l11111l1_opy_():
            return self.bstack1111llll1l1_opy_.get_name()
        return None
    def bstack111l11lll11_opy_(self):
        data = {
            bstack1l11ll1_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨṱ"): {
                bstack1l11ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫṲ"): self.bstack1111ll1l11l_opy_(),
                bstack1l11ll1_opy_ (u"ࠫࡲࡵࡤࡦࠩṳ"): self.bstack1111ll11l1l_opy_(),
                bstack1l11ll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬṴ"): self.bstack111l1111111_opy_()
            }
        }
        return data
    def bstack1111ll11ll1_opy_(self, config):
        bstack111l111ll11_opy_ = {}
        bstack111l111ll11_opy_[bstack1l11ll1_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬṵ")] = {
            bstack1l11ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨṶ"): self.bstack1111ll1l11l_opy_(),
            bstack1l11ll1_opy_ (u"ࠨ࡯ࡲࡨࡪ࠭ṷ"): self.bstack1111ll11l1l_opy_()
        }
        bstack111l111ll11_opy_[bstack1l11ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡲࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡤ࡬ࡡࡪ࡮ࡨࡨࠬṸ")] = {
            bstack1l11ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫṹ"): self.bstack111l1111lll_opy_()
        }
        bstack111l111ll11_opy_[bstack1l11ll1_opy_ (u"ࠫࡷࡻ࡮ࡠࡲࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡤ࡬ࡡࡪ࡮ࡨࡨࡤ࡬ࡩࡳࡵࡷࠫṺ")] = {
            bstack1l11ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ṻ"): self.bstack1111lll1l1l_opy_()
        }
        bstack111l111ll11_opy_[bstack1l11ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡣ࡫ࡧࡩ࡭࡫ࡱ࡫ࡤࡧ࡮ࡥࡡࡩࡰࡦࡱࡹࠨṼ")] = {
            bstack1l11ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨṽ"): self.bstack1111ll1ll1l_opy_()
        }
        if self.bstack1ll1l111l_opy_(config):
            bstack111l111ll11_opy_[bstack1l11ll1_opy_ (u"ࠨࡴࡨࡸࡷࡿ࡟ࡵࡧࡶࡸࡸࡥ࡯࡯ࡡࡩࡥ࡮ࡲࡵࡳࡧࠪṾ")] = {
                bstack1l11ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṿ"): True,
                bstack1l11ll1_opy_ (u"ࠪࡱࡦࡾ࡟ࡳࡧࡷࡶ࡮࡫ࡳࠨẀ"): self.bstack11l1l1l1ll_opy_(config)
            }
        if self.bstack11l1l1111ll_opy_(config):
            bstack111l111ll11_opy_[bstack1l11ll1_opy_ (u"ࠫࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡲࡲࡤ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ẁ")] = {
                bstack1l11ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭Ẃ"): True,
                bstack1l11ll1_opy_ (u"࠭࡭ࡢࡺࡢࡪࡦ࡯࡬ࡶࡴࡨࡷࠬẃ"): self.bstack11l1l111lll_opy_(config)
            }
        return bstack111l111ll11_opy_
    def bstack1llll1l1l1_opy_(self, config):
        bstack1l11ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡵ࡬࡭ࡧࡦࡸࡸࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡦࡾࠦ࡭ࡢ࡭࡬ࡲ࡬ࠦࡡࠡࡥࡤࡰࡱࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠢࠫࡷࡹࡸࠩ࠻ࠢࡗ࡬ࡪࠦࡕࡖࡋࡇࠤࡴ࡬ࠠࡵࡪࡨࠤࡧࡻࡩ࡭ࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠬࠡࡱࡵࠤࡓࡵ࡮ࡦࠢ࡬ࡪࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥẄ")
        if not (config.get(bstack1l11ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫẅ"), None) in bstack11l1l1ll11l_opy_ and self.bstack1111ll1l11l_opy_()):
            return None
        bstack1111ll1l111_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧẆ"), None)
        logger.debug(bstack1l11ll1_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡢࡶ࡫࡯ࡨ࡛ࠥࡕࡊࡆ࠽ࠤࢀࢃࠢẇ").format(bstack1111ll1l111_opy_))
        try:
            bstack11ll11l111l_opy_ = bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠤẈ").format(bstack1111ll1l111_opy_)
            bstack1111ll11lll_opy_ = self.bstack111l1111111_opy_() or [] # for multi-repo
            bstack1111ll1l1ll_opy_ = bstack111llll1lll_opy_(bstack1111ll11lll_opy_) # bstack11l11111l11_opy_-repo is handled bstack111l111lll1_opy_
            payload = {
                bstack1l11ll1_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥẉ"): config.get(bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫẊ"), bstack1l11ll1_opy_ (u"ࠧࠨẋ")),
                bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦẌ"): config.get(bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬẍ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l11ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣẎ"): config.get(bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ẏ"), bstack1l11ll1_opy_ (u"ࠬ࠭Ẑ")),
                bstack1l11ll1_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤẑ"): int(os.environ.get(bstack1l11ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥẒ")) or bstack1l11ll1_opy_ (u"ࠣ࠲ࠥẓ")),
                bstack1l11ll1_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨẔ"): int(os.environ.get(bstack1l11ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧẕ")) or bstack1l11ll1_opy_ (u"ࠦ࠶ࠨẖ")),
                bstack1l11ll1_opy_ (u"ࠧ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠢẗ"): get_host_info(),
                bstack1l11ll1_opy_ (u"ࠨࡰࡳࡆࡨࡸࡦ࡯࡬ࡴࠤẘ"): bstack1111ll1l1ll_opy_
            }
            logger.debug(bstack1l11ll1_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡ࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡴࡦࡿ࡬ࡰࡣࡧ࠾ࠥࢁࡽࠣẙ").format(payload))
            response = bstack11ll111l1ll_opy_.bstack1111ll1lll1_opy_(bstack11ll11l111l_opy_, payload)
            if response:
                logger.debug(bstack1l11ll1_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡂࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨẚ").format(response))
                return response
            else:
                logger.error(bstack1l11ll1_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨẛ").format(bstack1111ll1l111_opy_))
                return None
        except Exception as e:
            logger.error(bstack1l11ll1_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅࠢࡾࢁ࠿ࠦࡻࡾࠤẜ").format(bstack1111ll1l111_opy_, e))
            return None