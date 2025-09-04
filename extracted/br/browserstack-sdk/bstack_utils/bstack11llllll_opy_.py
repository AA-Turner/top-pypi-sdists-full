# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import tempfile
import math
from bstack_utils import bstack11l1111l1_opy_
from bstack_utils.constants import bstack1ll111ll11_opy_, bstack11l1l1llll1_opy_
from bstack_utils.helper import bstack11l11l1ll11_opy_, get_host_info
from bstack_utils.bstack11ll111lll1_opy_ import bstack11ll11l1111_opy_
bstack1111ll1llll_opy_ = bstack1111l1l_opy_ (u"ࠤࡵࡩࡹࡸࡹࡕࡧࡶࡸࡸࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣṎ")
bstack111l111l1l1_opy_ = bstack1111l1l_opy_ (u"ࠥࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠤṏ")
bstack1111ll111ll_opy_ = bstack1111l1l_opy_ (u"ࠦࡷࡻ࡮ࡑࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡊࡦ࡯࡬ࡦࡦࡉ࡭ࡷࡹࡴࠣṐ")
bstack111l111lll1_opy_ = bstack1111l1l_opy_ (u"ࠧࡸࡥࡳࡷࡱࡔࡷ࡫ࡶࡪࡱࡸࡷࡱࡿࡆࡢ࡫࡯ࡩࡩࠨṑ")
bstack1111ll1lll1_opy_ = bstack1111l1l_opy_ (u"ࠨࡳ࡬࡫ࡳࡊࡱࡧ࡫ࡺࡣࡱࡨࡋࡧࡩ࡭ࡧࡧࠦṒ")
bstack1111ll11l11_opy_ = bstack1111l1l_opy_ (u"ࠢࡳࡷࡱࡗࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࠦṓ")
bstack111l111l111_opy_ = {
    bstack1111ll1llll_opy_,
    bstack111l111l1l1_opy_,
    bstack1111ll111ll_opy_,
    bstack111l111lll1_opy_,
    bstack1111ll1lll1_opy_,
    bstack1111ll11l11_opy_
}
bstack1111ll1l1ll_opy_ = {bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨṔ")}
logger = bstack11l1111l1_opy_.get_logger(__name__, bstack1ll111ll11_opy_)
class bstack1111lllllll_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1111ll11ll1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack111l1llll_opy_:
    _1lll11l11l1_opy_ = None
    def __init__(self, config):
        self.bstack1111lll1111_opy_ = False
        self.bstack1111llll1ll_opy_ = False
        self.bstack111l111ll1l_opy_ = False
        self.bstack1111llll11l_opy_ = False
        self.bstack1111lll1ll1_opy_ = None
        self.bstack111l111l11l_opy_ = bstack1111lllllll_opy_()
        self.bstack111l11111l1_opy_ = None
        opts = config.get(bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ṕ"), {})
        bstack1111lll1lll_opy_ = opts.get(bstack1111ll11l11_opy_, {})
        self.__1111lll11l1_opy_(
            bstack1111lll1lll_opy_.get(bstack1111l1l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫṖ"), False),
            bstack1111lll1lll_opy_.get(bstack1111l1l_opy_ (u"ࠫࡲࡵࡤࡦࠩṗ"), bstack1111l1l_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬṘ")),
            bstack1111lll1lll_opy_.get(bstack1111l1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ṙ"), None)
        )
        self.__1111ll11l1l_opy_(opts.get(bstack1111ll111ll_opy_, False))
        self.__111l11111ll_opy_(opts.get(bstack111l111lll1_opy_, False))
        self.__1111ll1l1l1_opy_(opts.get(bstack1111ll1lll1_opy_, False))
    @classmethod
    def bstack1l11llll1_opy_(cls, config=None):
        if cls._1lll11l11l1_opy_ is None and config is not None:
            cls._1lll11l11l1_opy_ = bstack111l1llll_opy_(config)
        return cls._1lll11l11l1_opy_
    @staticmethod
    def bstack11111ll1l_opy_(config: dict) -> bool:
        bstack1111lllll11_opy_ = config.get(bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫṚ"), {}).get(bstack1111ll1llll_opy_, {})
        return bstack1111lllll11_opy_.get(bstack1111l1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩṛ"), False)
    @staticmethod
    def bstack1l1ll1llll_opy_(config: dict) -> int:
        bstack1111lllll11_opy_ = config.get(bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭Ṝ"), {}).get(bstack1111ll1llll_opy_, {})
        retries = 0
        if bstack111l1llll_opy_.bstack11111ll1l_opy_(config):
            retries = bstack1111lllll11_opy_.get(bstack1111l1l_opy_ (u"ࠪࡱࡦࡾࡒࡦࡶࡵ࡭ࡪࡹࠧṝ"), 1)
        return retries
    @staticmethod
    def bstack1l11l1111l_opy_(config: dict) -> dict:
        bstack111l1111l1l_opy_ = config.get(bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨṞ"), {})
        return {
            key: value for key, value in bstack111l1111l1l_opy_.items() if key in bstack111l111l111_opy_
        }
    @staticmethod
    def bstack111l1111lll_opy_():
        bstack1111l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤṟ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃࠢṠ").format(os.getenv(bstack1111l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧṡ")))))
    @staticmethod
    def bstack111l111llll_opy_(test_name: str):
        bstack1111l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧṢ")
        bstack1111llll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣṣ").format(os.getenv(bstack1111l1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣṤ"))))
        with open(bstack1111llll111_opy_, bstack1111l1l_opy_ (u"ࠫࡦ࠭ṥ")) as file:
            file.write(bstack1111l1l_opy_ (u"ࠧࢁࡽ࡝ࡰࠥṦ").format(test_name))
    @staticmethod
    def bstack1111llll1l1_opy_(framework: str) -> bool:
       return framework.lower() in bstack1111ll1l1ll_opy_
    @staticmethod
    def bstack11l1l111l11_opy_(config: dict) -> bool:
        bstack1111ll1l111_opy_ = config.get(bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪṧ"), {}).get(bstack111l111l1l1_opy_, {})
        return bstack1111ll1l111_opy_.get(bstack1111l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨṨ"), False)
    @staticmethod
    def bstack11l1l1111ll_opy_(config: dict, bstack11l1l1l1ll1_opy_: int = 0) -> int:
        bstack1111l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠯ࠤࡼ࡮ࡩࡤࡪࠣࡧࡦࡴࠠࡣࡧࠣࡥࡳࠦࡡࡣࡵࡲࡰࡺࡺࡥࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡵࠤࡦࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡴࡺࡡ࡭ࡡࡷࡩࡸࡺࡳࠡࠪ࡬ࡲࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࠨࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡩࡳࡷࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠰ࡦࡦࡹࡥࡥࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࡸ࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨṩ")
        bstack1111ll1l111_opy_ = config.get(bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭Ṫ"), {}).get(bstack1111l1l_opy_ (u"ࠪࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠩṫ"), {})
        bstack1111lll1l11_opy_ = 0
        bstack1111ll1l11l_opy_ = 0
        if bstack111l1llll_opy_.bstack11l1l111l11_opy_(config):
            bstack1111ll1l11l_opy_ = bstack1111ll1l111_opy_.get(bstack1111l1l_opy_ (u"ࠫࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴࠩṬ"), 5)
            if isinstance(bstack1111ll1l11l_opy_, str) and bstack1111ll1l11l_opy_.endswith(bstack1111l1l_opy_ (u"ࠬࠫࠧṭ")):
                try:
                    percentage = int(bstack1111ll1l11l_opy_.strip(bstack1111l1l_opy_ (u"࠭ࠥࠨṮ")))
                    if bstack11l1l1l1ll1_opy_ > 0:
                        bstack1111lll1l11_opy_ = math.ceil((percentage * bstack11l1l1l1ll1_opy_) / 100)
                    else:
                        raise ValueError(bstack1111l1l_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡳࡵࡴࡶࠣࡦࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠳ࠨṯ"))
                except ValueError as e:
                    raise ValueError(bstack1111l1l_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪࠦࡶࡢ࡮ࡸࡩࠥ࡬࡯ࡳࠢࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹ࠺ࠡࡽࢀࠦṰ").format(bstack1111ll1l11l_opy_)) from e
            else:
                bstack1111lll1l11_opy_ = int(bstack1111ll1l11l_opy_)
        logger.info(bstack1111l1l_opy_ (u"ࠤࡐࡥࡽࠦࡦࡢ࡫࡯ࡹࡷ࡫ࡳࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡸ࡫ࡴࠡࡶࡲ࠾ࠥࢁࡽࠡࠪࡩࡶࡴࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡽࢀ࠭ࠧṱ").format(bstack1111lll1l11_opy_, bstack1111ll1l11l_opy_))
        return bstack1111lll1l11_opy_
    def bstack1111ll1ll1l_opy_(self):
        return self.bstack1111llll11l_opy_
    def bstack111l1111l11_opy_(self):
        return self.bstack1111lll1ll1_opy_
    def bstack111l111111l_opy_(self):
        return self.bstack111l11111l1_opy_
    def __1111lll11l1_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1111llll11l_opy_ = bool(enabled)
            self.bstack1111lll1ll1_opy_ = mode
            if source is None:
                self.bstack111l11111l1_opy_ = []
            elif isinstance(source, list):
                self.bstack111l11111l1_opy_ = source
            self.__111l1111111_opy_()
        except Exception as e:
            logger.error(bstack1111l1l_opy_ (u"ࠥ࡟ࡤࡥࡳࡦࡶࡢࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯࡟ࠣࠤࢀࢃࠢṲ").format(e))
    def bstack1111lll111l_opy_(self):
        return self.bstack1111lll1111_opy_
    def __1111ll11l1l_opy_(self, value):
        self.bstack1111lll1111_opy_ = bool(value)
        self.__111l1111111_opy_()
    def bstack1111lll1l1l_opy_(self):
        return self.bstack1111llll1ll_opy_
    def __111l11111ll_opy_(self, value):
        self.bstack1111llll1ll_opy_ = bool(value)
        self.__111l1111111_opy_()
    def bstack111l1111ll1_opy_(self):
        return self.bstack111l111ll1l_opy_
    def __1111ll1l1l1_opy_(self, value):
        self.bstack111l111ll1l_opy_ = bool(value)
        self.__111l1111111_opy_()
    def __111l1111111_opy_(self):
        if self.bstack1111llll11l_opy_:
            self.bstack1111lll1111_opy_ = False
            self.bstack1111llll1ll_opy_ = False
            self.bstack111l111ll1l_opy_ = False
            self.bstack111l111l11l_opy_.enable(bstack1111ll11l11_opy_)
        elif self.bstack1111lll1111_opy_:
            self.bstack1111llll1ll_opy_ = False
            self.bstack111l111ll1l_opy_ = False
            self.bstack1111llll11l_opy_ = False
            self.bstack111l111l11l_opy_.enable(bstack1111ll111ll_opy_)
        elif self.bstack1111llll1ll_opy_:
            self.bstack1111lll1111_opy_ = False
            self.bstack111l111ll1l_opy_ = False
            self.bstack1111llll11l_opy_ = False
            self.bstack111l111l11l_opy_.enable(bstack111l111lll1_opy_)
        elif self.bstack111l111ll1l_opy_:
            self.bstack1111lll1111_opy_ = False
            self.bstack1111llll1ll_opy_ = False
            self.bstack1111llll11l_opy_ = False
            self.bstack111l111l11l_opy_.enable(bstack1111ll1lll1_opy_)
        else:
            self.bstack111l111l11l_opy_.disable()
    def bstack1ll11llll1_opy_(self):
        return self.bstack111l111l11l_opy_.bstack1111ll11ll1_opy_()
    def bstack1lll111111_opy_(self):
        if self.bstack111l111l11l_opy_.bstack1111ll11ll1_opy_():
            return self.bstack111l111l11l_opy_.get_name()
        return None
    def bstack111l11l111l_opy_(self):
        data = {
            bstack1111l1l_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪṳ"): {
                bstack1111l1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭Ṵ"): self.bstack1111ll1ll1l_opy_(),
                bstack1111l1l_opy_ (u"࠭࡭ࡰࡦࡨࠫṵ"): self.bstack111l1111l11_opy_(),
                bstack1111l1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧṶ"): self.bstack111l111111l_opy_()
            }
        }
        return data
    def bstack1111llllll1_opy_(self, config):
        bstack1111lll11ll_opy_ = {}
        bstack1111lll11ll_opy_[bstack1111l1l_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧṷ")] = {
            bstack1111l1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṸ"): self.bstack1111ll1ll1l_opy_(),
            bstack1111l1l_opy_ (u"ࠪࡱࡴࡪࡥࠨṹ"): self.bstack111l1111l11_opy_()
        }
        bstack1111lll11ll_opy_[bstack1111l1l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡴࡷ࡫ࡶࡪࡱࡸࡷࡱࡿ࡟ࡧࡣ࡬ࡰࡪࡪࠧṺ")] = {
            bstack1111l1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ṻ"): self.bstack1111lll1l1l_opy_()
        }
        bstack1111lll11ll_opy_[bstack1111l1l_opy_ (u"࠭ࡲࡶࡰࡢࡴࡷ࡫ࡶࡪࡱࡸࡷࡱࡿ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡧ࡫ࡵࡷࡹ࠭Ṽ")] = {
            bstack1111l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨṽ"): self.bstack1111lll111l_opy_()
        }
        bstack1111lll11ll_opy_[bstack1111l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡦࡢ࡫࡯࡭ࡳ࡭࡟ࡢࡰࡧࡣ࡫ࡲࡡ࡬ࡻࠪṾ")] = {
            bstack1111l1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪṿ"): self.bstack111l1111ll1_opy_()
        }
        if self.bstack11111ll1l_opy_(config):
            bstack1111lll11ll_opy_[bstack1111l1l_opy_ (u"ࠪࡶࡪࡺࡲࡺࡡࡷࡩࡸࡺࡳࡠࡱࡱࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠬẀ")] = {
                bstack1111l1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬẁ"): True,
                bstack1111l1l_opy_ (u"ࠬࡳࡡࡹࡡࡵࡩࡹࡸࡩࡦࡵࠪẂ"): self.bstack1l1ll1llll_opy_(config)
            }
        if self.bstack11l1l111l11_opy_(config):
            bstack1111lll11ll_opy_[bstack1111l1l_opy_ (u"࠭ࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࡴࡴ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠨẃ")] = {
                bstack1111l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨẄ"): True,
                bstack1111l1l_opy_ (u"ࠨ࡯ࡤࡼࡤ࡬ࡡࡪ࡮ࡸࡶࡪࡹࠧẅ"): self.bstack11l1l1111ll_opy_(config)
            }
        return bstack1111lll11ll_opy_
    def bstack1l1l1l11l1_opy_(self, config):
        bstack1111l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡰ࡮࡯ࡩࡨࡺࡳࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡨࡹࠡ࡯ࡤ࡯࡮ࡴࡧࠡࡣࠣࡧࡦࡲ࡬ࠡࡶࡲࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠤ࠭ࡹࡴࡳࠫ࠽ࠤ࡙࡮ࡥࠡࡗࡘࡍࡉࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡢࡶ࡫࡯ࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡧࡥࡹࡧࠠࡧࡱࡵ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠠࡦࡰࡧࡴࡴ࡯࡮ࡵ࠮ࠣࡳࡷࠦࡎࡰࡰࡨࠤ࡮࡬ࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧẆ")
        if not (config.get(bstack1111l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ẇ"), None) in bstack11l1l1llll1_opy_ and self.bstack1111ll1ll1l_opy_()):
            return None
        bstack1111ll11lll_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩẈ"), None)
        logger.debug(bstack1111l1l_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈ࠿ࠦࡻࡾࠤẉ").format(bstack1111ll11lll_opy_))
        try:
            bstack11ll11l11l1_opy_ = bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠦẊ").format(bstack1111ll11lll_opy_)
            bstack1111lllll1l_opy_ = self.bstack111l111111l_opy_() or [] # for multi-repo
            bstack111l111ll11_opy_ = bstack11l11l1ll11_opy_(bstack1111lllll1l_opy_) # bstack111ll1l1ll1_opy_-repo is handled bstack111l111l1ll_opy_
            payload = {
                bstack1111l1l_opy_ (u"ࠢࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠧẋ"): config.get(bstack1111l1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ẍ"), bstack1111l1l_opy_ (u"ࠩࠪẍ")),
                bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠨẎ"): config.get(bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧẏ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1111l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥẐ"): config.get(bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨẑ"), bstack1111l1l_opy_ (u"ࠧࠨẒ")),
                bstack1111l1l_opy_ (u"ࠣࡰࡲࡨࡪࡏ࡮ࡥࡧࡻࠦẓ"): int(os.environ.get(bstack1111l1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧẔ")) or bstack1111l1l_opy_ (u"ࠥ࠴ࠧẕ")),
                bstack1111l1l_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࡑࡳࡩ࡫ࡳࠣẖ"): int(os.environ.get(bstack1111l1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢẗ")) or bstack1111l1l_opy_ (u"ࠨ࠱ࠣẘ")),
                bstack1111l1l_opy_ (u"ࠢࡩࡱࡶࡸࡎࡴࡦࡰࠤẙ"): get_host_info(),
                bstack1111l1l_opy_ (u"ࠣࡲࡵࡈࡪࡺࡡࡪ࡮ࡶࠦẚ"): bstack111l111ll11_opy_
            }
            logger.debug(bstack1111l1l_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡶࡡࡺ࡮ࡲࡥࡩࡀࠠࡼࡿࠥẛ").format(payload))
            response = bstack11ll11l1111_opy_.bstack1111ll1ll11_opy_(bstack11ll11l11l1_opy_, payload)
            if response:
                logger.debug(bstack1111l1l_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡄࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣẜ").format(response))
                return response
            else:
                logger.error(bstack1111l1l_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣẝ").format(bstack1111ll11lll_opy_))
                return None
        except Exception as e:
            logger.error(bstack1111l1l_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇࠤࢀࢃ࠺ࠡࡽࢀࠦẞ").format(bstack1111ll11lll_opy_, e))
            return None