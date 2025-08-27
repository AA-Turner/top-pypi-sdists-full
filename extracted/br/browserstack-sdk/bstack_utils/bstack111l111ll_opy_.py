# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1l1l11111_opy_
from bstack_utils.constants import bstack111111lll_opy_, bstack11l1ll1l1l1_opy_
from bstack_utils.helper import bstack11l11ll1lll_opy_, get_host_info
from bstack_utils.bstack11ll111llll_opy_ import bstack11ll11l1ll1_opy_
bstack111l11l1l11_opy_ = bstack1111lll_opy_ (u"ࠦࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠥṉ")
bstack1111llll111_opy_ = bstack1111lll_opy_ (u"ࠧࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦṊ")
bstack111l111ll1l_opy_ = bstack1111lll_opy_ (u"ࠨࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࡋ࡯ࡲࡴࡶࠥṋ")
bstack111l11l11ll_opy_ = bstack1111lll_opy_ (u"ࠢࡳࡧࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࠣṌ")
bstack111l111111l_opy_ = bstack1111lll_opy_ (u"ࠣࡵ࡮࡭ࡵࡌ࡬ࡢ࡭ࡼࡥࡳࡪࡆࡢ࡫࡯ࡩࡩࠨṍ")
bstack1111ll1ll1l_opy_ = bstack1111lll_opy_ (u"ࠤࡵࡹࡳ࡙࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࠨṎ")
bstack1111ll1l11l_opy_ = {
    bstack111l11l1l11_opy_,
    bstack1111llll111_opy_,
    bstack111l111ll1l_opy_,
    bstack111l11l11ll_opy_,
    bstack111l111111l_opy_,
    bstack1111ll1ll1l_opy_
}
bstack111l111l111_opy_ = {bstack1111lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪṏ")}
logger = bstack1l1l11111_opy_.get_logger(__name__, bstack111111lll_opy_)
class bstack1111lll1l11_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1111llll1l1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l11llll1_opy_:
    _1ll1ll11l11_opy_ = None
    def __init__(self, config):
        self.bstack111l1111111_opy_ = False
        self.bstack111l1111l1l_opy_ = False
        self.bstack111l1111lll_opy_ = False
        self.bstack111l11l1111_opy_ = False
        self.bstack1111ll1lll1_opy_ = None
        self.bstack1111ll1l111_opy_ = bstack1111lll1l11_opy_()
        self.bstack1111ll1l1ll_opy_ = None
        opts = config.get(bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨṐ"), {})
        bstack111l1111l11_opy_ = opts.get(bstack1111ll1ll1l_opy_, {})
        self.__1111ll1llll_opy_(
            bstack111l1111l11_opy_.get(bstack1111lll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ṑ"), False),
            bstack111l1111l11_opy_.get(bstack1111lll_opy_ (u"࠭࡭ࡰࡦࡨࠫṒ"), bstack1111lll_opy_ (u"ࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡈ࡬ࡶࡸࡺࠧṓ")),
            bstack111l1111l11_opy_.get(bstack1111lll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨṔ"), None)
        )
        self.__1111lll1111_opy_(opts.get(bstack111l111ll1l_opy_, False))
        self.__111l1111ll1_opy_(opts.get(bstack111l11l11ll_opy_, False))
        self.__1111lll11l1_opy_(opts.get(bstack111l111111l_opy_, False))
    @classmethod
    def bstack1ll1lll1l1_opy_(cls, config=None):
        if cls._1ll1ll11l11_opy_ is None and config is not None:
            cls._1ll1ll11l11_opy_ = bstack1l11llll1_opy_(config)
        return cls._1ll1ll11l11_opy_
    @staticmethod
    def bstack1l1llllll1_opy_(config: dict) -> bool:
        bstack1111lllll11_opy_ = config.get(bstack1111lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ṕ"), {}).get(bstack111l11l1l11_opy_, {})
        return bstack1111lllll11_opy_.get(bstack1111lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫṖ"), False)
    @staticmethod
    def bstack11ll1llll_opy_(config: dict) -> int:
        bstack1111lllll11_opy_ = config.get(bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨṗ"), {}).get(bstack111l11l1l11_opy_, {})
        retries = 0
        if bstack1l11llll1_opy_.bstack1l1llllll1_opy_(config):
            retries = bstack1111lllll11_opy_.get(bstack1111lll_opy_ (u"ࠬࡳࡡࡹࡔࡨࡸࡷ࡯ࡥࡴࠩṘ"), 1)
        return retries
    @staticmethod
    def bstack11l11l1l1_opy_(config: dict) -> dict:
        bstack1111llllll1_opy_ = config.get(bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪṙ"), {})
        return {
            key: value for key, value in bstack1111llllll1_opy_.items() if key in bstack1111ll1l11l_opy_
        }
    @staticmethod
    def bstack111l111ll11_opy_():
        bstack1111lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦṚ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤṛ").format(os.getenv(bstack1111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢṜ")))))
    @staticmethod
    def bstack111l111l1ll_opy_(test_name: str):
        bstack1111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢṝ")
        bstack1111lll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶࠥṞ").format(os.getenv(bstack1111lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥṟ"))))
        with open(bstack1111lll1ll1_opy_, bstack1111lll_opy_ (u"࠭ࡡࠨṠ")) as file:
            file.write(bstack1111lll_opy_ (u"ࠢࡼࡿ࡟ࡲࠧṡ").format(test_name))
    @staticmethod
    def bstack1111lll11ll_opy_(framework: str) -> bool:
       return framework.lower() in bstack111l111l111_opy_
    @staticmethod
    def bstack11l1l1ll1l1_opy_(config: dict) -> bool:
        bstack111l111lll1_opy_ = config.get(bstack1111lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬṢ"), {}).get(bstack1111llll111_opy_, {})
        return bstack111l111lll1_opy_.get(bstack1111lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṣ"), False)
    @staticmethod
    def bstack11l1l1l111l_opy_(config: dict, bstack11l1l1l1l11_opy_: int = 0) -> int:
        bstack1111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠱ࠦࡷࡩ࡫ࡦ࡬ࠥࡩࡡ࡯ࠢࡥࡩࠥࡧ࡮ࠡࡣࡥࡷࡴࡲࡵࡵࡧࠣࡲࡺࡳࡢࡦࡴࠣࡳࡷࠦࡡࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺ࡯ࡵࡣ࡯ࡣࡹ࡫ࡳࡵࡵࠣࠬ࡮ࡴࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࠪࡵࡩࡶࡻࡩࡳࡧࡧࠤ࡫ࡵࡲࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠲ࡨࡡࡴࡧࡧࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࡳࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣṤ")
        bstack111l111lll1_opy_ = config.get(bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨṥ"), {}).get(bstack1111lll_opy_ (u"ࠬࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠫṦ"), {})
        bstack1111ll1ll11_opy_ = 0
        bstack1111llll11l_opy_ = 0
        if bstack1l11llll1_opy_.bstack11l1l1ll1l1_opy_(config):
            bstack1111llll11l_opy_ = bstack111l111lll1_opy_.get(bstack1111lll_opy_ (u"࠭࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶࠫṧ"), 5)
            if isinstance(bstack1111llll11l_opy_, str) and bstack1111llll11l_opy_.endswith(bstack1111lll_opy_ (u"ࠧࠦࠩṨ")):
                try:
                    percentage = int(bstack1111llll11l_opy_.strip(bstack1111lll_opy_ (u"ࠨࠧࠪṩ")))
                    if bstack11l1l1l1l11_opy_ > 0:
                        bstack1111ll1ll11_opy_ = math.ceil((percentage * bstack11l1l1l1l11_opy_) / 100)
                    else:
                        raise ValueError(bstack1111lll_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨ࠱ࡧࡧࡳࡦࡦࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࡹ࠮ࠣṪ"))
                except ValueError as e:
                    raise ValueError(bstack1111lll_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥࠡࡸࡤࡰࡺ࡫ࠠࡧࡱࡵࠤࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴ࠼ࠣࡿࢂࠨṫ").format(bstack1111llll11l_opy_)) from e
            else:
                bstack1111ll1ll11_opy_ = int(bstack1111llll11l_opy_)
        logger.info(bstack1111lll_opy_ (u"ࠦࡒࡧࡸࠡࡨࡤ࡭ࡱࡻࡲࡦࡵࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡳࡦࡶࠣࡸࡴࡀࠠࡼࡿࠣࠬ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡿࢂ࠯ࠢṬ").format(bstack1111ll1ll11_opy_, bstack1111llll11l_opy_))
        return bstack1111ll1ll11_opy_
    def bstack1111lllllll_opy_(self):
        return self.bstack111l11l1111_opy_
    def bstack1111lllll1l_opy_(self):
        return self.bstack1111ll1lll1_opy_
    def bstack1111lll1lll_opy_(self):
        return self.bstack1111ll1l1ll_opy_
    def __1111ll1llll_opy_(self, enabled, mode, source=None):
        try:
            self.bstack111l11l1111_opy_ = bool(enabled)
            self.bstack1111ll1lll1_opy_ = mode
            if source is None:
                self.bstack1111ll1l1ll_opy_ = []
            elif isinstance(source, list):
                self.bstack1111ll1l1ll_opy_ = source
            self.__111l111l11l_opy_()
        except Exception as e:
            logger.error(bstack1111lll_opy_ (u"ࠧࡡ࡟ࡠࡵࡨࡸࡤࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࡡࠥࠦࡻࡾࠤṭ").format(e))
    def bstack1111lll1l1l_opy_(self):
        return self.bstack111l1111111_opy_
    def __1111lll1111_opy_(self, value):
        self.bstack111l1111111_opy_ = bool(value)
        self.__111l111l11l_opy_()
    def bstack111l111l1l1_opy_(self):
        return self.bstack111l1111l1l_opy_
    def __111l1111ll1_opy_(self, value):
        self.bstack111l1111l1l_opy_ = bool(value)
        self.__111l111l11l_opy_()
    def bstack111l11l11l1_opy_(self):
        return self.bstack111l1111lll_opy_
    def __1111lll11l1_opy_(self, value):
        self.bstack111l1111lll_opy_ = bool(value)
        self.__111l111l11l_opy_()
    def __111l111l11l_opy_(self):
        if self.bstack111l11l1111_opy_:
            self.bstack111l1111111_opy_ = False
            self.bstack111l1111l1l_opy_ = False
            self.bstack111l1111lll_opy_ = False
            self.bstack1111ll1l111_opy_.enable(bstack1111ll1ll1l_opy_)
        elif self.bstack111l1111111_opy_:
            self.bstack111l1111l1l_opy_ = False
            self.bstack111l1111lll_opy_ = False
            self.bstack111l11l1111_opy_ = False
            self.bstack1111ll1l111_opy_.enable(bstack111l111ll1l_opy_)
        elif self.bstack111l1111l1l_opy_:
            self.bstack111l1111111_opy_ = False
            self.bstack111l1111lll_opy_ = False
            self.bstack111l11l1111_opy_ = False
            self.bstack1111ll1l111_opy_.enable(bstack111l11l11ll_opy_)
        elif self.bstack111l1111lll_opy_:
            self.bstack111l1111111_opy_ = False
            self.bstack111l1111l1l_opy_ = False
            self.bstack111l11l1111_opy_ = False
            self.bstack1111ll1l111_opy_.enable(bstack111l111111l_opy_)
        else:
            self.bstack1111ll1l111_opy_.disable()
    def bstack1lll1111_opy_(self):
        return self.bstack1111ll1l111_opy_.bstack1111llll1l1_opy_()
    def bstack111ll1l1l_opy_(self):
        if self.bstack1111ll1l111_opy_.bstack1111llll1l1_opy_():
            return self.bstack1111ll1l111_opy_.get_name()
        return None
    def bstack111l1l111l1_opy_(self):
        data = {
            bstack1111lll_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬṮ"): {
                bstack1111lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨṯ"): self.bstack1111lllllll_opy_(),
                bstack1111lll_opy_ (u"ࠨ࡯ࡲࡨࡪ࠭Ṱ"): self.bstack1111lllll1l_opy_(),
                bstack1111lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩṱ"): self.bstack1111lll1lll_opy_()
            }
        }
        return data
    def bstack1111llll1ll_opy_(self, config):
        bstack111l11l111l_opy_ = {}
        bstack111l11l111l_opy_[bstack1111lll_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩṲ")] = {
            bstack1111lll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬṳ"): self.bstack1111lllllll_opy_(),
            bstack1111lll_opy_ (u"ࠬࡳ࡯ࡥࡧࠪṴ"): self.bstack1111lllll1l_opy_()
        }
        bstack111l11l111l_opy_[bstack1111lll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࠩṵ")] = {
            bstack1111lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨṶ"): self.bstack111l111l1l1_opy_()
        }
        bstack111l11l111l_opy_[bstack1111lll_opy_ (u"ࠨࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࡡࡩ࡭ࡷࡹࡴࠨṷ")] = {
            bstack1111lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṸ"): self.bstack1111lll1l1l_opy_()
        }
        bstack111l11l111l_opy_[bstack1111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡨࡤ࡭ࡱ࡯࡮ࡨࡡࡤࡲࡩࡥࡦ࡭ࡣ࡮ࡽࠬṹ")] = {
            bstack1111lll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬṺ"): self.bstack111l11l11l1_opy_()
        }
        if self.bstack1l1llllll1_opy_(config):
            bstack111l11l111l_opy_[bstack1111lll_opy_ (u"ࠬࡸࡥࡵࡴࡼࡣࡹ࡫ࡳࡵࡵࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧṻ")] = {
                bstack1111lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧṼ"): True,
                bstack1111lll_opy_ (u"ࠧ࡮ࡣࡻࡣࡷ࡫ࡴࡳ࡫ࡨࡷࠬṽ"): self.bstack11ll1llll_opy_(config)
            }
        if self.bstack11l1l1ll1l1_opy_(config):
            bstack111l11l111l_opy_[bstack1111lll_opy_ (u"ࠨࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡯࡯ࡡࡩࡥ࡮ࡲࡵࡳࡧࠪṾ")] = {
                bstack1111lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṿ"): True,
                bstack1111lll_opy_ (u"ࠪࡱࡦࡾ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡴࠩẀ"): self.bstack11l1l1l111l_opy_(config)
            }
        return bstack111l11l111l_opy_
    def bstack11111111l_opy_(self, config):
        bstack1111lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡲࡰࡱ࡫ࡣࡵࡵࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡣࡻࠣࡱࡦࡱࡩ࡯ࡩࠣࡥࠥࡩࡡ࡭࡮ࠣࡸࡴࠦࡴࡩࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠡࡧࡱࡨࡵࡵࡩ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠦࠨࡴࡶࡵ࠭࠿ࠦࡔࡩࡧ࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡤࡸ࡭ࡱࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢẁ")
        if not (config.get(bstack1111lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨẂ"), None) in bstack11l1ll1l1l1_opy_ and self.bstack1111lllllll_opy_()):
            return None
        bstack1111ll1l1l1_opy_ = os.environ.get(bstack1111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫẃ"), None)
        logger.debug(bstack1111lll_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡉ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊ࠺ࠡࡽࢀࠦẄ").format(bstack1111ll1l1l1_opy_))
        try:
            bstack11ll11ll111_opy_ = bstack1111lll_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠨẅ").format(bstack1111ll1l1l1_opy_)
            bstack111l11111l1_opy_ = self.bstack1111lll1lll_opy_() or [] # for multi-repo
            bstack111l111llll_opy_ = bstack11l11ll1lll_opy_(bstack111l11111l1_opy_) # bstack11l111111l1_opy_-repo is handled bstack111l11111ll_opy_
            payload = {
                bstack1111lll_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢẆ"): config.get(bstack1111lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨẇ"), bstack1111lll_opy_ (u"ࠫࠬẈ")),
                bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣẉ"): config.get(bstack1111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩẊ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧẋ"): config.get(bstack1111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪẌ"), bstack1111lll_opy_ (u"ࠩࠪẍ")),
                bstack1111lll_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨẎ"): int(os.environ.get(bstack1111lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢẏ")) or bstack1111lll_opy_ (u"ࠧ࠶ࠢẐ")),
                bstack1111lll_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥẑ"): int(os.environ.get(bstack1111lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤẒ")) or bstack1111lll_opy_ (u"ࠣ࠳ࠥẓ")),
                bstack1111lll_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦẔ"): get_host_info(),
                bstack1111lll_opy_ (u"ࠥࡴࡷࡊࡥࡵࡣ࡬ࡰࡸࠨẕ"): bstack111l111llll_opy_
            }
            logger.debug(bstack1111lll_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡱࡣࡼࡰࡴࡧࡤ࠻ࠢࡾࢁࠧẖ").format(payload))
            response = bstack11ll11l1ll1_opy_.bstack1111lll111l_opy_(bstack11ll11ll111_opy_, payload)
            if response:
                logger.debug(bstack1111lll_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡆࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥẗ").format(response))
                return response
            else:
                logger.error(bstack1111lll_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࡀࠠࡼࡿࠥẘ").format(bstack1111ll1l1l1_opy_))
                return None
        except Exception as e:
            logger.error(bstack1111lll_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࠦࡻࡾ࠼ࠣࡿࢂࠨẙ").format(bstack1111ll1l1l1_opy_, e))
            return None