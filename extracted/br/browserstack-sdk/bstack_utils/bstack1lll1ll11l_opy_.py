# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1l11l1l1l_opy_
from bstack_utils.constants import bstack1l11l111l1_opy_
bstack11ll1l11lll_opy_ = bstack11l1111_opy_ (u"ࠧࡸࡥࡵࡴࡼࡘࡪࡹࡴࡴࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦᘤ")
bstack11ll1l1l11l_opy_ = bstack11l1111_opy_ (u"ࠨࡡࡣࡱࡵࡸࡇࡻࡩ࡭ࡦࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠧᘥ")
bstack11ll11ll1l1_opy_ = bstack11l1111_opy_ (u"ࠢࡳࡷࡱࡔࡷ࡫ࡶࡪࡱࡸࡷࡱࡿࡆࡢ࡫࡯ࡩࡩࡌࡩࡳࡵࡷࠦᘦ")
bstack11ll11ll1ll_opy_ = bstack11l1111_opy_ (u"ࠣࡴࡨࡶࡺࡴࡐࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡉࡥ࡮ࡲࡥࡥࠤᘧ")
bstack11ll1ll1lll_opy_ = bstack11l1111_opy_ (u"ࠤࡶ࡯࡮ࡶࡆ࡭ࡣ࡮ࡽࡦࡴࡤࡇࡣ࡬ࡰࡪࡪࠢᘨ")
bstack11ll1ll11ll_opy_ = {
    bstack11ll1l11lll_opy_,
    bstack11ll1l1l11l_opy_,
    bstack11ll11ll1l1_opy_,
    bstack11ll11ll1ll_opy_,
    bstack11ll1ll1lll_opy_,
}
bstack11ll1l111ll_opy_ = {bstack11l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᘩ")}
logger = bstack1l11l1l1l_opy_.get_logger(__name__, bstack1l11l111l1_opy_)
class bstack11ll1l11l11_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack11ll1ll1l11_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1lllll111_opy_:
    _1l111l111ll_opy_ = None
    def __init__(self, config):
        self.bstack11ll1l1lll1_opy_ = False
        self.bstack11ll1l1llll_opy_ = False
        self.bstack11ll1l1l1ll_opy_ = False
        self.bstack11ll1lll111_opy_ = bstack11ll1l11l11_opy_()
        opts = config.get(bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᘪ"), {})
        self.__11ll1l1ll11_opy_(opts.get(bstack11ll11ll1l1_opy_, False))
        self.__11ll1l1l1l1_opy_(opts.get(bstack11ll11ll1ll_opy_, False))
        self.__11ll11lll11_opy_(opts.get(bstack11ll1ll1lll_opy_, False))
    @classmethod
    def bstack11l1l11l11_opy_(cls, config=None):
        if cls._1l111l111ll_opy_ is None and config is not None:
            cls._1l111l111ll_opy_ = bstack1lllll111_opy_(config)
        return cls._1l111l111ll_opy_
    @staticmethod
    def bstack11ll111ll1_opy_(config: dict) -> bool:
        bstack11ll11llll1_opy_ = config.get(bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᘫ"), {}).get(bstack11ll1l11lll_opy_, {})
        return bstack11ll11llll1_opy_.get(bstack11l1111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧᘬ"), False)
    @staticmethod
    def bstack1l11ll1lll_opy_(config: dict) -> int:
        bstack11ll11llll1_opy_ = config.get(bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫᘭ"), {}).get(bstack11ll1l11lll_opy_, {})
        retries = 0
        if bstack1lllll111_opy_.bstack11ll111ll1_opy_(config):
            retries = bstack11ll11llll1_opy_.get(bstack11l1111_opy_ (u"ࠨ࡯ࡤࡼࡗ࡫ࡴࡳ࡫ࡨࡷࠬᘮ"), 1)
        return retries
    @staticmethod
    def bstack1l1l1l11_opy_(config: dict) -> dict:
        bstack11ll1l1ll1l_opy_ = config.get(bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ᘯ"), {})
        return {
            key: value for key, value in bstack11ll1l1ll1l_opy_.items() if key in bstack11ll1ll11ll_opy_
        }
    @staticmethod
    def bstack11ll1l1l111_opy_():
        bstack11l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᘰ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧᘱ").format(os.getenv(bstack11l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥᘲ")))))
    @staticmethod
    def bstack11ll1ll1l1l_opy_(test_name: str):
        bstack11l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᘳ")
        bstack11ll1ll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨᘴ").format(os.getenv(bstack11l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨᘵ"))))
        with open(bstack11ll1ll11l1_opy_, bstack11l1111_opy_ (u"ࠩࡤࠫᘶ")) as file:
            file.write(bstack11l1111_opy_ (u"ࠥࡿࢂࡢ࡮ࠣᘷ").format(test_name))
    @staticmethod
    def bstack11ll1l11111_opy_(framework: str) -> bool:
       return framework.lower() in bstack11ll1l111ll_opy_
    @staticmethod
    def bstack11ll1ll111l_opy_(config: dict) -> bool:
        bstack11ll1l11l1l_opy_ = config.get(bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᘸ"), {}).get(bstack11ll1l1l11l_opy_, {})
        return bstack11ll1l11l1l_opy_.get(bstack11l1111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ᘹ"), False)
    @staticmethod
    def bstack11ll11lll1l_opy_(config: dict, bstack11ll1ll1ll1_opy_: int = 0) -> int:
        bstack11l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠭ࠢࡺ࡬࡮ࡩࡨࠡࡥࡤࡲࠥࡨࡥࠡࡣࡱࠤࡦࡨࡳࡰ࡮ࡸࡸࡪࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡳࠢࡤࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭ࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡲࡸࡦࡲ࡟ࡵࡧࡶࡸࡸࠦࠨࡪࡰࡷ࠭࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤ࠭ࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᘺ")
        bstack11ll1l11l1l_opy_ = config.get(bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫᘻ"), {}).get(bstack11l1111_opy_ (u"ࠨࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧᘼ"), {})
        bstack11ll1l111l1_opy_ = 0
        bstack11ll11lllll_opy_ = 0
        if bstack1lllll111_opy_.bstack11ll1ll111l_opy_(config):
            bstack11ll11lllll_opy_ = bstack11ll1l11l1l_opy_.get(bstack11l1111_opy_ (u"ࠩࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹࠧᘽ"), 5)
            if isinstance(bstack11ll11lllll_opy_, str) and bstack11ll11lllll_opy_.endswith(bstack11l1111_opy_ (u"ࠪࠩࠬᘾ")):
                try:
                    percentage = int(bstack11ll11lllll_opy_.strip(bstack11l1111_opy_ (u"ࠫࠪ࠭ᘿ")))
                    if bstack11ll1ll1ll1_opy_ > 0:
                        bstack11ll1l111l1_opy_ = math.ceil((percentage * bstack11ll1ll1ll1_opy_) / 100)
                    else:
                        raise ValueError(bstack11l1111_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡱࡺࡹࡴࠡࡤࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵ࠱ࠦᙀ"))
                except ValueError as e:
                    raise ValueError(bstack11l1111_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨࠤࡻࡧ࡬ࡶࡧࠣࡪࡴࡸࠠ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷ࠿ࠦࡻࡾࠤᙁ").format(bstack11ll11lllll_opy_)) from e
            else:
                bstack11ll1l111l1_opy_ = int(bstack11ll11lllll_opy_)
        logger.info(bstack11l1111_opy_ (u"ࠢࡎࡣࡻࠤ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡶࡩࡹࠦࡴࡰ࠼ࠣࡿࢂࠦࠨࡧࡴࡲࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾࠫࠥᙂ").format(bstack11ll1l111l1_opy_, bstack11ll11lllll_opy_))
        return bstack11ll1l111l1_opy_
    def bstack11ll1ll1111_opy_(self):
        return self.bstack11ll1l1lll1_opy_
    def __11ll1l1ll11_opy_(self, value):
        self.bstack11ll1l1lll1_opy_ = bool(value)
        self.__11ll1l11ll1_opy_()
    def bstack11ll11ll11l_opy_(self):
        return self.bstack11ll1l1llll_opy_
    def __11ll1l1l1l1_opy_(self, value):
        self.bstack11ll1l1llll_opy_ = bool(value)
        self.__11ll1l11ll1_opy_()
    def bstack11ll1l1111l_opy_(self):
        return self.bstack11ll1l1l1ll_opy_
    def __11ll11lll11_opy_(self, value):
        self.bstack11ll1l1l1ll_opy_ = bool(value)
        self.__11ll1l11ll1_opy_()
    def __11ll1l11ll1_opy_(self):
        if self.bstack11ll1l1lll1_opy_:
            self.bstack11ll1l1llll_opy_ = False
            self.bstack11ll1l1l1ll_opy_ = False
            self.bstack11ll1lll111_opy_.enable(bstack11ll11ll1l1_opy_)
        elif self.bstack11ll1l1llll_opy_:
            self.bstack11ll1l1lll1_opy_ = False
            self.bstack11ll1l1l1ll_opy_ = False
            self.bstack11ll1lll111_opy_.enable(bstack11ll11ll1ll_opy_)
        elif self.bstack11ll1l1l1ll_opy_:
            self.bstack11ll1l1lll1_opy_ = False
            self.bstack11ll1l1llll_opy_ = False
            self.bstack11ll1lll111_opy_.enable(bstack11ll1ll1lll_opy_)
        else:
            self.bstack11ll1lll111_opy_.disable()
    def bstack1ll1ll1l_opy_(self):
        return self.bstack11ll1lll111_opy_.bstack11ll1ll1l11_opy_()
    def bstack11l11lll11_opy_(self):
        if self.bstack11ll1lll111_opy_.bstack11ll1ll1l11_opy_():
            return self.bstack11ll1lll111_opy_.get_name()
        return None