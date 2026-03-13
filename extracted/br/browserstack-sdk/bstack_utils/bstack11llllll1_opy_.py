# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack11l1111lll_opy_, bstack111l1l1llll_opy_
from bstack_utils.helper import bstack1111lll11l1_opy_, get_host_info
from bstack_utils.bstack111ll1l1ll1_opy_ import bstack111ll1ll1ll_opy_
import json
import re
import sys
bstack1llll11llll1_opy_ = bstack1111l_opy_ (u"ࠦࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠥ⊍")
bstack1lllll11l111_opy_ = bstack1111l_opy_ (u"ࠧࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦ⊎")
bstack1llll11l1ll1_opy_ = bstack1111l_opy_ (u"ࠨࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࡋ࡯ࡲࡴࡶࠥ⊏")
bstack1llll1ll111l_opy_ = bstack1111l_opy_ (u"ࠢࡳࡧࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࠣ⊐")
bstack1llll1l11111_opy_ = bstack1111l_opy_ (u"ࠣࡵ࡮࡭ࡵࡌ࡬ࡢ࡭ࡼࡥࡳࡪࡆࡢ࡫࡯ࡩࡩࠨ⊑")
bstack1llll1llllll_opy_ = bstack1111l_opy_ (u"ࠤࡵࡹࡳ࡙࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࠨ⊒")
bstack1llll1l11l11_opy_ = {
    bstack1llll11llll1_opy_,
    bstack1lllll11l111_opy_,
    bstack1llll11l1ll1_opy_,
    bstack1llll1ll111l_opy_,
    bstack1llll1l11111_opy_,
    bstack1llll1llllll_opy_
}
bstack1lllll11111l_opy_ = {bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⊓")}
logger = logger_utils.get_logger(__name__, bstack11l1111lll_opy_)
class bstack1llll1l111l1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1llll1l1l1l1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack11ll11l11l_opy_:
    _1ll11l111ll_opy_ = None
    def __init__(self, config):
        self.bstack1llll1l11ll1_opy_ = False
        self.bstack1llll1l11l1l_opy_ = False
        self.bstack1llll11l1lll_opy_ = False
        self.bstack1lllll111lll_opy_ = False
        self.bstack1llll1l1l1ll_opy_ = None
        self.bstack1llll1llll11_opy_ = bstack1llll1l111l1_opy_()
        self.bstack1lllll11lll1_opy_ = None
        opts = config.get(bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ⊔"), {})
        self.bstack1llll1l1l111_opy_ = config.get(bstack1111l_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡅࡏࡘࠪ⊕"), bstack1111l_opy_ (u"ࠨࠢ⊖"))
        self.bstack1llll1lll11l_opy_ = config.get(bstack1111l_opy_ (u"ࠧࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࡅࡏࡍࠬ⊗"), bstack1111l_opy_ (u"ࠣࠤ⊘"))
        bstack1llll1l1ll1l_opy_ = opts.get(bstack1llll1llllll_opy_, {})
        bstack1llll1lllll1_opy_ = None
        if bstack1111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ⊙") in bstack1llll1l1ll1l_opy_:
            bstack1llll1ll1111_opy_ = bstack1llll1l1ll1l_opy_[bstack1111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ⊚")]
            if bstack1llll1ll1111_opy_ is None or (isinstance(bstack1llll1ll1111_opy_, str) and bstack1llll1ll1111_opy_.strip() == bstack1111l_opy_ (u"ࠫࠬ⊛")) or (isinstance(bstack1llll1ll1111_opy_, list) and len(bstack1llll1ll1111_opy_) == 0):
                bstack1llll1lllll1_opy_ = []
            elif isinstance(bstack1llll1ll1111_opy_, list):
                bstack1llll1lllll1_opy_ = bstack1llll1ll1111_opy_
            elif isinstance(bstack1llll1ll1111_opy_, str) and bstack1llll1ll1111_opy_.strip():
                bstack1llll1lllll1_opy_ = bstack1llll1ll1111_opy_
            else:
                logger.warning(bstack1111l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡶࡢ࡮ࡸࡩࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡾࢁ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࡥ࡮ࡲࡷࡽࠥࡲࡩࡴࡶ࠱ࠦ⊜").format(bstack1llll1ll1111_opy_))
                bstack1llll1lllll1_opy_ = []
        self.__1llll1l111ll_opy_(
            bstack1llll1l1ll1l_opy_.get(bstack1111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⊝"), False),
            bstack1llll1l1ll1l_opy_.get(bstack1111l_opy_ (u"ࠧ࡮ࡱࡧࡩࠬ⊞"), bstack1111l_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ⊟")),
            bstack1llll1lllll1_opy_
        )
        self.__1lllll111l1l_opy_(opts.get(bstack1llll11l1ll1_opy_, False))
        self.__1llll1ll1l11_opy_(opts.get(bstack1llll1ll111l_opy_, False))
        self.__1llll1l1l11l_opy_(opts.get(bstack1llll1l11111_opy_, False))
    @classmethod
    def get_instance(cls, config=None):
        if cls._1ll11l111ll_opy_ is None and config is not None:
            cls._1ll11l111ll_opy_ = bstack11ll11l11l_opy_(config)
        return cls._1ll11l111ll_opy_
    @staticmethod
    def bstack11lllll111_opy_(config: dict) -> bool:
        bstack1llll11lll11_opy_ = config.get(bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭⊠"), {}).get(bstack1llll11llll1_opy_, {})
        return bstack1llll11lll11_opy_.get(bstack1111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⊡"), False)
    @staticmethod
    def bstack1l11l11l1l_opy_(config: dict) -> int:
        bstack1llll11lll11_opy_ = config.get(bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ⊢"), {}).get(bstack1llll11llll1_opy_, {})
        retries = 0
        if bstack11ll11l11l_opy_.bstack11lllll111_opy_(config):
            retries = bstack1llll11lll11_opy_.get(bstack1111l_opy_ (u"ࠬࡳࡡࡹࡔࡨࡸࡷ࡯ࡥࡴࠩ⊣"), 1)
        return retries
    @staticmethod
    def bstack1l1l11ll11_opy_(config: dict) -> dict:
        bstack1llll1l11lll_opy_ = config.get(bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ⊤"), {})
        return {
            key: value for key, value in bstack1llll1l11lll_opy_.items() if key in bstack1llll1l11l11_opy_
        }
    @staticmethod
    def bstack1llll1llll1l_opy_():
        bstack1111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⊥")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤ⊦").format(os.getenv(bstack1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⊧")))))
    @staticmethod
    def bstack1lllll1111ll_opy_(test_name: str):
        bstack1111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⊨")
        bstack1lllll11ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶࠥ⊩").format(os.getenv(bstack1111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⊪"))))
        with open(bstack1lllll11ll1l_opy_, bstack1111l_opy_ (u"࠭ࡡࠨ⊫")) as file:
            file.write(bstack1111l_opy_ (u"ࠢࡼࡿ࡟ࡲࠧ⊬").format(test_name))
    @staticmethod
    def bstack1llll11ll111_opy_(framework: str) -> bool:
       return framework.lower() in bstack1lllll11111l_opy_
    @staticmethod
    def bstack111l11l111l_opy_(config: dict) -> bool:
        bstack1llll11ll1ll_opy_ = config.get(bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⊭"), {}).get(bstack1lllll11l111_opy_, {})
        return bstack1llll11ll1ll_opy_.get(bstack1111l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ⊮"), False)
    @staticmethod
    def bstack111l11l1lll_opy_(config: dict, bstack111l11ll1l1_opy_: int = 0) -> int:
        bstack1111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠱ࠦࡷࡩ࡫ࡦ࡬ࠥࡩࡡ࡯ࠢࡥࡩࠥࡧ࡮ࠡࡣࡥࡷࡴࡲࡵࡵࡧࠣࡲࡺࡳࡢࡦࡴࠣࡳࡷࠦࡡࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺ࡯ࡵࡣ࡯ࡣࡹ࡫ࡳࡵࡵࠣࠬ࡮ࡴࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࠪࡵࡩࡶࡻࡩࡳࡧࡧࠤ࡫ࡵࡲࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠲ࡨࡡࡴࡧࡧࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࡳࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⊯")
        bstack1llll11ll1ll_opy_ = config.get(bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ⊰"), {}).get(bstack1111l_opy_ (u"ࠬࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠫ⊱"), {})
        bstack1llll1ll11ll_opy_ = 0
        bstack1lllll11l11l_opy_ = 0
        if bstack11ll11l11l_opy_.bstack111l11l111l_opy_(config):
            bstack1lllll11l11l_opy_ = bstack1llll11ll1ll_opy_.get(bstack1111l_opy_ (u"࠭࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶࠫ⊲"), 5)
            if isinstance(bstack1lllll11l11l_opy_, str) and bstack1lllll11l11l_opy_.endswith(bstack1111l_opy_ (u"ࠧࠦࠩ⊳")):
                try:
                    percentage = int(bstack1lllll11l11l_opy_.strip(bstack1111l_opy_ (u"ࠨࠧࠪ⊴")))
                    if bstack111l11ll1l1_opy_ > 0:
                        bstack1llll1ll11ll_opy_ = math.ceil((percentage * bstack111l11ll1l1_opy_) / 100)
                    else:
                        raise ValueError(bstack1111l_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨ࠱ࡧࡧࡳࡦࡦࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࡹ࠮ࠣ⊵"))
                except ValueError as e:
                    raise ValueError(bstack1111l_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥࠡࡸࡤࡰࡺ࡫ࠠࡧࡱࡵࠤࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴ࠼ࠣࡿࢂࠨ⊶").format(bstack1lllll11l11l_opy_)) from e
            else:
                bstack1llll1ll11ll_opy_ = int(bstack1lllll11l11l_opy_)
        logger.info(bstack1111l_opy_ (u"ࠦࡒࡧࡸࠡࡨࡤ࡭ࡱࡻࡲࡦࡵࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡳࡦࡶࠣࡸࡴࡀࠠࡼࡿࠣࠬ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡿࢂ࠯ࠢ⊷").format(bstack1llll1ll11ll_opy_, bstack1lllll11l11l_opy_))
        return bstack1llll1ll11ll_opy_
    def bstack1llll1l1llll_opy_(self):
        return self.bstack1lllll111lll_opy_
    def bstack1lllll11l1ll_opy_(self):
        return self.bstack1llll1l1l1ll_opy_
    def bstack1lllll111ll1_opy_(self):
        return self.bstack1lllll11lll1_opy_
    def __1llll1l111ll_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lllll111lll_opy_ = bool(enabled)
            if mode not in [bstack1111l_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ⊸"), bstack1111l_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡐࡰ࡯ࡽࠬ⊹")]:
                logger.warning(bstack1111l_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡱࡴࡪࡥࠡࠩࡾࢁࠬࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠢࡇࡩ࡫ࡧࡵ࡭ࡶ࡬ࡲ࡬ࠦࡴࡰࠢࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ࠲ࠧ⊺").format(mode))
                mode = bstack1111l_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ⊻")
            self.bstack1llll1l1l1ll_opy_ = mode
            self.bstack1lllll11lll1_opy_ = []
            if source is None:
                self.bstack1lllll11lll1_opy_ = None
            elif isinstance(source, list):
                self.bstack1lllll11lll1_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1111l_opy_ (u"ࠩ࠱࡮ࡸࡵ࡮ࠨ⊼")):
                self.bstack1lllll11lll1_opy_ = self._1lllll111l11_opy_(source)
            self.__1llll1lll111_opy_()
        except Exception as e:
            logger.error(bstack1111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࠳ࠠࡦࡰࡤࡦࡱ࡫ࡤ࠻ࠢࡾࢁ࠱ࠦ࡭ࡰࡦࡨ࠾ࠥࢁࡽ࠭ࠢࡶࡳࡺࡸࡣࡦ࠼ࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥ⊽").format(enabled, mode, source, e))
    def bstack1llll1ll11l1_opy_(self):
        return self.bstack1llll1l11ll1_opy_
    def __1lllll111l1l_opy_(self, value):
        self.bstack1llll1l11ll1_opy_ = bool(value)
        self.__1llll1lll111_opy_()
    def bstack1llll1l1lll1_opy_(self):
        return self.bstack1llll1l11l1l_opy_
    def __1llll1ll1l11_opy_(self, value):
        self.bstack1llll1l11l1l_opy_ = bool(value)
        self.__1llll1lll111_opy_()
    def bstack1llll11ll11l_opy_(self):
        return self.bstack1llll11l1lll_opy_
    def __1llll1l1l11l_opy_(self, value):
        self.bstack1llll11l1lll_opy_ = bool(value)
        self.__1llll1lll111_opy_()
    def __1llll1lll111_opy_(self):
        if self.bstack1lllll111lll_opy_:
            self.bstack1llll1l11ll1_opy_ = False
            self.bstack1llll1l11l1l_opy_ = False
            self.bstack1llll11l1lll_opy_ = False
            self.bstack1llll1llll11_opy_.enable(bstack1llll1llllll_opy_)
        elif self.bstack1llll1l11ll1_opy_:
            self.bstack1llll1l11l1l_opy_ = False
            self.bstack1llll11l1lll_opy_ = False
            self.bstack1lllll111lll_opy_ = False
            self.bstack1llll1llll11_opy_.enable(bstack1llll11l1ll1_opy_)
        elif self.bstack1llll1l11l1l_opy_:
            self.bstack1llll1l11ll1_opy_ = False
            self.bstack1llll11l1lll_opy_ = False
            self.bstack1lllll111lll_opy_ = False
            self.bstack1llll1llll11_opy_.enable(bstack1llll1ll111l_opy_)
        elif self.bstack1llll11l1lll_opy_:
            self.bstack1llll1l11ll1_opy_ = False
            self.bstack1llll1l11l1l_opy_ = False
            self.bstack1lllll111lll_opy_ = False
            self.bstack1llll1llll11_opy_.enable(bstack1llll1l11111_opy_)
        else:
            self.bstack1llll1llll11_opy_.disable()
    def bstack11l111l1ll_opy_(self):
        return self.bstack1llll1llll11_opy_.bstack1llll1l1l1l1_opy_()
    def bstack11111l11l_opy_(self):
        if self.bstack1llll1llll11_opy_.bstack1llll1l1l1l1_opy_():
            return self.bstack1llll1llll11_opy_.get_name()
        return None
    def _1lllll111l11_opy_(self, bstack1llll1ll1lll_opy_):
        bstack1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡹ࡯ࡶࡴࡦࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣࡥࡳࡪࠠࡧࡱࡵࡱࡦࡺࠠࡪࡶࠣࡪࡴࡸࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡲࡹࡷࡩࡥࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠤ࠭ࡹࡴࡳࠫ࠽ࠤࡕࡧࡴࡩࠢࡷࡳࠥࡺࡨࡦࠢࡍࡗࡔࡔࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࡬ࡪࡵࡷ࠾ࠥࡌ࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡵࡩࡵࡵࡳࡪࡶࡲࡶࡾࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⊾")
        if not os.path.isfile(bstack1llll1ll1lll_opy_):
            logger.error(bstack1111l_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࠫࢀࢃࠧࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠥ⊿").format(bstack1llll1ll1lll_opy_))
            return []
        data = None
        try:
            with open(bstack1llll1ll1lll_opy_, bstack1111l_opy_ (u"ࠨࡲࠣ⋀")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡋࡕࡒࡒࠥ࡬ࡲࡰ࡯ࠣࡷࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥ⋁").format(bstack1llll1ll1lll_opy_, e))
            return []
        _1llll11lll1l_opy_ = None
        _1lllll1111l1_opy_ = None
        def _1llll1l1ll11_opy_():
            bstack1llll11ll1l1_opy_ = {}
            bstack1llll11lllll_opy_ = {}
            try:
                if self.bstack1llll1l1l111_opy_.startswith(bstack1111l_opy_ (u"ࠨࡽࠪ⋂")) and self.bstack1llll1l1l111_opy_.endswith(bstack1111l_opy_ (u"ࠩࢀࠫ⋃")):
                    bstack1llll11ll1l1_opy_ = json.loads(self.bstack1llll1l1l111_opy_)
                else:
                    bstack1llll11ll1l1_opy_ = dict(item.split(bstack1111l_opy_ (u"ࠪ࠾ࠬ⋄")) for item in self.bstack1llll1l1l111_opy_.split(bstack1111l_opy_ (u"ࠫ࠱࠭⋅")) if bstack1111l_opy_ (u"ࠬࡀࠧ⋆") in item) if self.bstack1llll1l1l111_opy_ else {}
                if self.bstack1llll1lll11l_opy_.startswith(bstack1111l_opy_ (u"࠭ࡻࠨ⋇")) and self.bstack1llll1lll11l_opy_.endswith(bstack1111l_opy_ (u"ࠧࡾࠩ⋈")):
                    bstack1llll11lllll_opy_ = json.loads(self.bstack1llll1lll11l_opy_)
                else:
                    bstack1llll11lllll_opy_ = dict(item.split(bstack1111l_opy_ (u"ࠨ࠼ࠪ⋉")) for item in self.bstack1llll1lll11l_opy_.split(bstack1111l_opy_ (u"ࠩ࠯ࠫ⋊")) if bstack1111l_opy_ (u"ࠪ࠾ࠬ⋋") in item) if self.bstack1llll1lll11l_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤ࡫࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡳࡡࡱࡲ࡬ࡲ࡬ࡹ࠺ࠡࡽࢀࠦ⋌").format(e))
            logger.debug(bstack1111l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࡳࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࠽ࠤࢀࢃࠬࠡࡅࡏࡍ࠿ࠦࡻࡾࠤ⋍").format(bstack1llll11ll1l1_opy_, bstack1llll11lllll_opy_))
            return bstack1llll11ll1l1_opy_, bstack1llll11lllll_opy_
        if _1llll11lll1l_opy_ is None or _1lllll1111l1_opy_ is None:
            _1llll11lll1l_opy_, _1lllll1111l1_opy_ = _1llll1l1ll11_opy_()
        def bstack1lllll111111_opy_(name, bstack1lllll11ll11_opy_):
            if name in _1lllll1111l1_opy_:
                return _1lllll1111l1_opy_[name]
            if name in _1llll11lll1l_opy_:
                return _1llll11lll1l_opy_[name]
            if bstack1lllll11ll11_opy_.get(bstack1111l_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭⋎")):
                return bstack1lllll11ll11_opy_[bstack1111l_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧ⋏")]
            return None
        if isinstance(data, dict):
            bstack1llll1ll1l1l_opy_ = []
            bstack1lllll11l1l1_opy_ = re.compile(bstack1111l_opy_ (u"ࡳࠩࡡ࡟ࡆ࠳࡚࠱࠯࠼ࡣࡢ࠱ࠤࠨ⋐"))
            for name, bstack1lllll11ll11_opy_ in data.items():
                if not isinstance(bstack1lllll11ll11_opy_, dict):
                    continue
                url = bstack1lllll11ll11_opy_.get(bstack1111l_opy_ (u"ࠩࡸࡶࡱ࠭⋑"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1111l_opy_ (u"ࠪࠫ⋒")):
                    logger.warning(bstack1111l_opy_ (u"ࠦࡗ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹࠡࡗࡕࡐࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡳࡰࡷࡵࡧࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ⋓").format(name, bstack1lllll11ll11_opy_))
                    continue
                if not bstack1lllll11l1l1_opy_.match(name):
                    logger.warning(bstack1111l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸ࡭ࡢࡶࠣࡪࡴࡸࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ⋔").format(name, bstack1lllll11ll11_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1111l_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࠫࢀࢃࠧࠡ࡯ࡸࡷࡹࠦࡨࡢࡸࡨࠤࡦࠦ࡬ࡦࡰࡪࡸ࡭ࠦࡢࡦࡶࡺࡩࡪࡴࠠ࠲ࠢࡤࡲࡩࠦ࠳࠱ࠢࡦ࡬ࡦࡸࡡࡤࡶࡨࡶࡸ࠴ࠢ⋕").format(name))
                    continue
                bstack1lllll11ll11_opy_ = bstack1lllll11ll11_opy_.copy()
                bstack1lllll11ll11_opy_[bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⋖")] = name
                bstack1lllll11ll11_opy_[bstack1111l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ⋗")] = bstack1lllll111111_opy_(name, bstack1lllll11ll11_opy_)
                if not bstack1lllll11ll11_opy_.get(bstack1111l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ⋘")) or bstack1lllll11ll11_opy_.get(bstack1111l_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ⋙")) == bstack1111l_opy_ (u"ࠫࠬ⋚"):
                    logger.warning(bstack1111l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡮ࡰࡶࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡩࡩࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ⋛").format(name, bstack1lllll11ll11_opy_))
                    continue
                if bstack1lllll11ll11_opy_.get(bstack1111l_opy_ (u"࠭ࡢࡢࡵࡨࡆࡷࡧ࡮ࡤࡪࠪ⋜")) and bstack1lllll11ll11_opy_[bstack1111l_opy_ (u"ࠧࡣࡣࡶࡩࡇࡸࡡ࡯ࡥ࡫ࠫ⋝")] == bstack1lllll11ll11_opy_[bstack1111l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ⋞")]:
                    logger.warning(bstack1111l_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡥࡳࡪࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡶ࡫ࡩࠥࡹࡡ࡮ࡧࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ⋟").format(name, bstack1lllll11ll11_opy_))
                    continue
                bstack1llll1ll1l1l_opy_.append(bstack1lllll11ll11_opy_)
            return bstack1llll1ll1l1l_opy_
        return data
    def bstack1lllll1lll1l_opy_(self):
        data = {
            bstack1111l_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ⋠"): {
                bstack1111l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⋡"): self.bstack1llll1l1llll_opy_(),
                bstack1111l_opy_ (u"ࠬࡳ࡯ࡥࡧࠪ⋢"): self.bstack1lllll11l1ll_opy_(),
                bstack1111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭⋣"): self.bstack1lllll111ll1_opy_()
            }
        }
        return data
    def bstack1llll1l1111l_opy_(self, config):
        bstack1llll1lll1l1_opy_ = {}
        bstack1llll1lll1l1_opy_[bstack1111l_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭⋤")] = {
            bstack1111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⋥"): self.bstack1llll1l1llll_opy_(),
            bstack1111l_opy_ (u"ࠩࡰࡳࡩ࡫ࠧ⋦"): self.bstack1lllll11l1ll_opy_()
        }
        bstack1llll1lll1l1_opy_[bstack1111l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩ࠭⋧")] = {
            bstack1111l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⋨"): self.bstack1llll1l1lll1_opy_()
        }
        bstack1llll1lll1l1_opy_[bstack1111l_opy_ (u"ࠬࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩࡥࡦࡪࡴࡶࡸࠬ⋩")] = {
            bstack1111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⋪"): self.bstack1llll1ll11l1_opy_()
        }
        bstack1llll1lll1l1_opy_[bstack1111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡤ࡬ࡡࡪ࡮࡬ࡲ࡬ࡥࡡ࡯ࡦࡢࡪࡱࡧ࡫ࡺࠩ⋫")] = {
            bstack1111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⋬"): self.bstack1llll11ll11l_opy_()
        }
        if self.bstack11lllll111_opy_(config):
            bstack1llll1lll1l1_opy_[bstack1111l_opy_ (u"ࠩࡵࡩࡹࡸࡹࡠࡶࡨࡷࡹࡹ࡟ࡰࡰࡢࡪࡦ࡯࡬ࡶࡴࡨࠫ⋭")] = {
                bstack1111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⋮"): True,
                bstack1111l_opy_ (u"ࠫࡲࡧࡸࡠࡴࡨࡸࡷ࡯ࡥࡴࠩ⋯"): self.bstack1l11l11l1l_opy_(config)
            }
        if self.bstack111l11l111l_opy_(config):
            bstack1llll1lll1l1_opy_[bstack1111l_opy_ (u"ࠬࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⋰")] = {
                bstack1111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⋱"): True,
                bstack1111l_opy_ (u"ࠧ࡮ࡣࡻࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡸ࠭⋲"): self.bstack111l11l1lll_opy_(config)
            }
        return bstack1llll1lll1l1_opy_
    def bstack1l1llll111_opy_(self, config):
        bstack1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࡹࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤࡧࡿࠠ࡮ࡣ࡮࡭ࡳ࡭ࠠࡢࠢࡦࡥࡱࡲࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡨࡵࡪ࡮ࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⋳")
        if not (config.get(bstack1111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⋴"), None) in bstack111l1l1llll_opy_ and self.bstack1llll1l1llll_opy_()):
            return None
        bstack1llll1lll1ll_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⋵"), None)
        logger.debug(bstack1111l_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡆࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣ⋶").format(bstack1llll1lll1ll_opy_))
        try:
            bstack111ll1lll1l_opy_ = bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠥ⋷").format(bstack1llll1lll1ll_opy_)
            payload = {
                bstack1111l_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ⋸"): config.get(bstack1111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ⋹"), bstack1111l_opy_ (u"ࠨࠩ⋺")),
                bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ⋻"): config.get(bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⋼"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ⋽"): os.environ.get(bstack1111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦ⋾"), bstack1111l_opy_ (u"ࠨࠢ⋿")),
                bstack1111l_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ⌀"): int(os.environ.get(bstack1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ⌁")) or bstack1111l_opy_ (u"ࠤ࠳ࠦ⌂")),
                bstack1111l_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ⌃"): int(os.environ.get(bstack1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ⌄")) or bstack1111l_opy_ (u"ࠧ࠷ࠢ⌅")),
                bstack1111l_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣ⌆"): get_host_info(),
            }
            logger.debug(bstack1111l_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡ࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡴࡦࡿ࡬ࡰࡣࡧ࠾ࠥࢁࡽࠣ⌇").format(payload))
            response = bstack111ll1ll1ll_opy_.bstack1llll1ll1ll1_opy_(bstack111ll1lll1l_opy_, payload)
            if response:
                logger.debug(bstack1111l_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡂࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⌈").format(response))
                return response
            else:
                logger.error(bstack1111l_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨ⌉").format(bstack1llll1lll1ll_opy_))
                return None
        except Exception as e:
            logger.error(bstack1111l_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅࠢࡾࢁ࠿ࠦࡻࡾࠤ⌊").format(bstack1llll1lll1ll_opy_, e))
            return None