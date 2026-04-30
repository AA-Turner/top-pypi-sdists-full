# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack11l1l1111_opy_, bstack11111l11lll_opy_
from bstack_utils.helper import bstack1llll1l11l11_opy_, get_host_info
from bstack_utils.bstack1111l11111l_opy_ import bstack1111l111111_opy_
import json
import re
import sys
bstack1lll11ll1111_opy_ = bstack1l1111l_opy_ (u"ࠤࡵࡩࡹࡸࡹࡕࡧࡶࡸࡸࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣ┏")
bstack1lll11l11111_opy_ = bstack1l1111l_opy_ (u"ࠥࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠤ┐")
bstack1lll111ll11l_opy_ = bstack1l1111l_opy_ (u"ࠦࡷࡻ࡮ࡑࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡊࡦ࡯࡬ࡦࡦࡉ࡭ࡷࡹࡴࠣ┑")
bstack1lll111l1lll_opy_ = bstack1l1111l_opy_ (u"ࠧࡸࡥࡳࡷࡱࡔࡷ࡫ࡶࡪࡱࡸࡷࡱࡿࡆࡢ࡫࡯ࡩࡩࠨ┒")
bstack1lll111l1l11_opy_ = bstack1l1111l_opy_ (u"ࠨࡳ࡬࡫ࡳࡊࡱࡧ࡫ࡺࡣࡱࡨࡋࡧࡩ࡭ࡧࡧࠦ┓")
bstack1lll1111ll1l_opy_ = bstack1l1111l_opy_ (u"ࠢࡳࡷࡱࡗࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࠦ└")
bstack1lll11l1ll1l_opy_ = {
    bstack1lll11ll1111_opy_,
    bstack1lll11l11111_opy_,
    bstack1lll111ll11l_opy_,
    bstack1lll111l1lll_opy_,
    bstack1lll111l1l11_opy_,
    bstack1lll1111ll1l_opy_
}
bstack1ll1lllll1ll_opy_ = {bstack1l1111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ┕")}
logger = logger_utils.get_logger(__name__, bstack11l1l1111_opy_)
class bstack1ll1llll1l1l_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lll11l111l1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1lll1111ll_opy_:
    _1l1llll1l11_opy_ = None
    def __init__(self, config):
        self.bstack1lll11l11l11_opy_ = False
        self.bstack1lll111lll1l_opy_ = False
        self.bstack1lll11111l1l_opy_ = False
        self.bstack1lll11l1l11l_opy_ = False
        self.bstack1lll111l11ll_opy_ = None
        self.bstack1lll11l1l111_opy_ = bstack1ll1llll1l1l_opy_()
        self.bstack1lll11l1lll1_opy_ = None
        opts = config.get(bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭┖"), {})
        self.bstack1lll1111l111_opy_ = config.get(bstack1l1111l_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡊࡔࡖࠨ┗"), bstack1l1111l_opy_ (u"ࠦࠧ┘"))
        self.bstack1lll1111l1ll_opy_ = config.get(bstack1l1111l_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡃࡍࡋࠪ┙"), bstack1l1111l_opy_ (u"ࠨࠢ┚"))
        bstack1lll1111l11l_opy_ = opts.get(bstack1lll1111ll1l_opy_, {})
        bstack1lll1111l1l1_opy_ = None
        if bstack1l1111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ┛") in bstack1lll1111l11l_opy_:
            bstack1ll1llll1lll_opy_ = bstack1lll1111l11l_opy_[bstack1l1111l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ├")]
            if bstack1ll1llll1lll_opy_ is None or (isinstance(bstack1ll1llll1lll_opy_, str) and bstack1ll1llll1lll_opy_.strip() == bstack1l1111l_opy_ (u"ࠩࠪ┝")) or (isinstance(bstack1ll1llll1lll_opy_, list) and len(bstack1ll1llll1lll_opy_) == 0):
                bstack1lll1111l1l1_opy_ = []
            elif isinstance(bstack1ll1llll1lll_opy_, list):
                bstack1lll1111l1l1_opy_ = bstack1ll1llll1lll_opy_
            elif isinstance(bstack1ll1llll1lll_opy_, str) and bstack1ll1llll1lll_opy_.strip():
                bstack1lll1111l1l1_opy_ = bstack1ll1llll1lll_opy_
            else:
                logger.warning(bstack1l1111l_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡵࡵࡳࡥࡨࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿ࠱ࠤࡉ࡫ࡦࡢࡷ࡯ࡸ࡮ࡴࡧࠡࡶࡲࠤࡪࡳࡰࡵࡻࠣࡰ࡮ࡹࡴ࠯ࠤ┞").format(bstack1ll1llll1lll_opy_))
                bstack1lll1111l1l1_opy_ = []
        self.__1lll111l11l1_opy_(
            bstack1lll1111l11l_opy_.get(bstack1l1111l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ┟"), False),
            bstack1lll1111l11l_opy_.get(bstack1l1111l_opy_ (u"ࠬࡳ࡯ࡥࡧࠪ┠"), bstack1l1111l_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭┡")),
            bstack1lll1111l1l1_opy_
        )
        self.__1lll1111111l_opy_(opts.get(bstack1lll111ll11l_opy_, False))
        self.__1ll1lllll1l1_opy_(opts.get(bstack1lll111l1lll_opy_, False))
        self.__1lll111lll11_opy_(opts.get(bstack1lll111l1l11_opy_, False))
    @classmethod
    def bstack111111l1ll_opy_(cls, config=None):
        if cls._1l1llll1l11_opy_ is None and config is not None:
            cls._1l1llll1l11_opy_ = bstack1lll1111ll_opy_(config)
        return cls._1l1llll1l11_opy_
    @staticmethod
    def bstack1111ll11l1_opy_(config: dict) -> bool:
        bstack1lll111l1ll1_opy_ = config.get(bstack1l1111l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ┢"), {}).get(bstack1lll11ll1111_opy_, {})
        return bstack1lll111l1ll1_opy_.get(bstack1l1111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ┣"), False)
    @staticmethod
    def bstack1lll1llll1_opy_(config: dict) -> int:
        bstack1lll111l1ll1_opy_ = config.get(bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭┤"), {}).get(bstack1lll11ll1111_opy_, {})
        retries = 0
        if bstack1lll1111ll_opy_.bstack1111ll11l1_opy_(config):
            retries = bstack1lll111l1ll1_opy_.get(bstack1l1111l_opy_ (u"ࠪࡱࡦࡾࡒࡦࡶࡵ࡭ࡪࡹࠧ┥"), 1)
        return retries
    @staticmethod
    def bstack111l11l11l_opy_(config: dict) -> dict:
        bstack1lll11111lll_opy_ = config.get(bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ┦"), {})
        return {
            key: value for key, value in bstack1lll11111lll_opy_.items() if key in bstack1lll11l1ll1l_opy_
        }
    @staticmethod
    def bstack1lll11l1llll_opy_():
        bstack1l1111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ┧")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l1111l_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃࠢ┨").format(os.getenv(bstack1l1111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ┩")))))
    @staticmethod
    def bstack1lll11l1l1ll_opy_(test_name: str):
        bstack1l1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ┪")
        bstack1ll1llllllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣ┫").format(os.getenv(bstack1l1111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ┬"))))
        with open(bstack1ll1llllllll_opy_, bstack1l1111l_opy_ (u"ࠫࡦ࠭┭")) as file:
            file.write(bstack1l1111l_opy_ (u"ࠧࢁࡽ࡝ࡰࠥ┮").format(test_name))
    @staticmethod
    def bstack1lll1111ll11_opy_(framework: str) -> bool:
       return framework.lower() in bstack1ll1lllll1ll_opy_
    @staticmethod
    def bstack1lllllllll11_opy_(config: dict) -> bool:
        bstack1ll1lllll11l_opy_ = config.get(bstack1l1111l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ┯"), {}).get(bstack1lll11l11111_opy_, {})
        return bstack1ll1lllll11l_opy_.get(bstack1l1111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ┰"), False)
    @staticmethod
    def bstack111111111l1_opy_(config: dict, bstack1lllllll11ll_opy_: int = 0) -> int:
        bstack1l1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠯ࠤࡼ࡮ࡩࡤࡪࠣࡧࡦࡴࠠࡣࡧࠣࡥࡳࠦࡡࡣࡵࡲࡰࡺࡺࡥࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡵࠤࡦࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡴࡺࡡ࡭ࡡࡷࡩࡸࡺࡳࠡࠪ࡬ࡲࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࠨࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡩࡳࡷࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠰ࡦࡦࡹࡥࡥࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࡸ࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ┱")
        bstack1ll1lllll11l_opy_ = config.get(bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭┲"), {}).get(bstack1l1111l_opy_ (u"ࠪࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠩ┳"), {})
        bstack1ll1llllll1l_opy_ = 0
        bstack1lll111l1l1l_opy_ = 0
        if bstack1lll1111ll_opy_.bstack1lllllllll11_opy_(config):
            bstack1lll111l1l1l_opy_ = bstack1ll1lllll11l_opy_.get(bstack1l1111l_opy_ (u"ࠫࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴࠩ┴"), 5)
            if isinstance(bstack1lll111l1l1l_opy_, str) and bstack1lll111l1l1l_opy_.endswith(bstack1l1111l_opy_ (u"ࠬࠫࠧ┵")):
                try:
                    percentage = int(bstack1lll111l1l1l_opy_.strip(bstack1l1111l_opy_ (u"࠭ࠥࠨ┶")))
                    if bstack1lllllll11ll_opy_ > 0:
                        bstack1ll1llllll1l_opy_ = math.ceil((percentage * bstack1lllllll11ll_opy_) / 100)
                    else:
                        raise ValueError(bstack1l1111l_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡳࡵࡴࡶࠣࡦࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠳ࠨ┷"))
                except ValueError as e:
                    raise ValueError(bstack1l1111l_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪࠦࡶࡢ࡮ࡸࡩࠥ࡬࡯ࡳࠢࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹ࠺ࠡࡽࢀࠦ┸").format(bstack1lll111l1l1l_opy_)) from e
            else:
                bstack1ll1llllll1l_opy_ = int(bstack1lll111l1l1l_opy_)
        logger.info(bstack1l1111l_opy_ (u"ࠤࡐࡥࡽࠦࡦࡢ࡫࡯ࡹࡷ࡫ࡳࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡸ࡫ࡴࠡࡶࡲ࠾ࠥࢁࡽࠡࠪࡩࡶࡴࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡽࢀ࠭ࠧ┹").format(bstack1ll1llllll1l_opy_, bstack1lll111l1l1l_opy_))
        return bstack1ll1llllll1l_opy_
    def bstack1ll1llllll11_opy_(self):
        return self.bstack1lll11l1l11l_opy_
    def bstack1lll111ll1l1_opy_(self):
        return self.bstack1lll111l11ll_opy_
    def bstack1lll11l11lll_opy_(self):
        return self.bstack1lll11l1lll1_opy_
    def __1lll111l11l1_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lll11l1l11l_opy_ = bool(enabled)
            if mode not in [bstack1l1111l_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ┺"), bstack1l1111l_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡕ࡮࡭ࡻࠪ┻")]:
                logger.warning(bstack1l1111l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳ࡮ࡣࡵࡸࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡ࡯ࡲࡨࡪࠦࠧࡼࡿࠪࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡅࡧࡩࡥࡺࡲࡴࡪࡰࡪࠤࡹࡵࠠࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ࠰ࠥ┼").format(mode))
                mode = bstack1l1111l_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭┽")
            self.bstack1lll111l11ll_opy_ = mode
            self.bstack1lll11l1lll1_opy_ = []
            if source is None:
                self.bstack1lll11l1lll1_opy_ = None
            elif isinstance(source, list):
                self.bstack1lll11l1lll1_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1l1111l_opy_ (u"ࠧ࠯࡬ࡶࡳࡳ࠭┾")):
                self.bstack1lll11l1lll1_opy_ = self._1lll11l11l1l_opy_(source)
            self.__1lll111lllll_opy_()
        except Exception as e:
            logger.error(bstack1l1111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣ࠱ࠥ࡫࡮ࡢࡤ࡯ࡩࡩࡀࠠࡼࡿ࠯ࠤࡲࡵࡤࡦ࠼ࠣࡿࢂ࠲ࠠࡴࡱࡸࡶࡨ࡫࠺ࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ┿").format(enabled, mode, source, e))
    def bstack1lll11111l11_opy_(self):
        return self.bstack1lll11l11l11_opy_
    def __1lll1111111l_opy_(self, value):
        self.bstack1lll11l11l11_opy_ = bool(value)
        self.__1lll111lllll_opy_()
    def bstack1lll11l11ll1_opy_(self):
        return self.bstack1lll111lll1l_opy_
    def __1ll1lllll1l1_opy_(self, value):
        self.bstack1lll111lll1l_opy_ = bool(value)
        self.__1lll111lllll_opy_()
    def bstack1lll111l1111_opy_(self):
        return self.bstack1lll11111l1l_opy_
    def __1lll111lll11_opy_(self, value):
        self.bstack1lll11111l1l_opy_ = bool(value)
        self.__1lll111lllll_opy_()
    def __1lll111lllll_opy_(self):
        if self.bstack1lll11l1l11l_opy_:
            self.bstack1lll11l11l11_opy_ = False
            self.bstack1lll111lll1l_opy_ = False
            self.bstack1lll11111l1l_opy_ = False
            self.bstack1lll11l1l111_opy_.enable(bstack1lll1111ll1l_opy_)
        elif self.bstack1lll11l11l11_opy_:
            self.bstack1lll111lll1l_opy_ = False
            self.bstack1lll11111l1l_opy_ = False
            self.bstack1lll11l1l11l_opy_ = False
            self.bstack1lll11l1l111_opy_.enable(bstack1lll111ll11l_opy_)
        elif self.bstack1lll111lll1l_opy_:
            self.bstack1lll11l11l11_opy_ = False
            self.bstack1lll11111l1l_opy_ = False
            self.bstack1lll11l1l11l_opy_ = False
            self.bstack1lll11l1l111_opy_.enable(bstack1lll111l1lll_opy_)
        elif self.bstack1lll11111l1l_opy_:
            self.bstack1lll11l11l11_opy_ = False
            self.bstack1lll111lll1l_opy_ = False
            self.bstack1lll11l1l11l_opy_ = False
            self.bstack1lll11l1l111_opy_.enable(bstack1lll111l1l11_opy_)
        else:
            self.bstack1lll11l1l111_opy_.disable()
    def bstack1ll1lllll_opy_(self):
        return self.bstack1lll11l1l111_opy_.bstack1lll11l111l1_opy_()
    def bstack11ll1llll1_opy_(self):
        if self.bstack1lll11l1l111_opy_.bstack1lll11l111l1_opy_():
            return self.bstack1lll11l1l111_opy_.get_name()
        return None
    def _1lll11l11l1l_opy_(self, bstack1ll1l1lll11_opy_):
        bstack1l1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡷࡴࡻࡲࡤࡧࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠡࡣࡱࡨࠥ࡬࡯ࡳ࡯ࡤࡸࠥ࡯ࡴࠡࡨࡲࡶࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡳࡰࡷࡵࡧࡪࡥࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠢࠫࡷࡹࡸࠩ࠻ࠢࡓࡥࡹ࡮ࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡕࡒࡒࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡊࡴࡸ࡭ࡢࡶࡷࡩࡩࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡳࡧࡳࡳࡸ࡯ࡴࡰࡴࡼࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ╀")
        if not os.path.isfile(bstack1ll1l1lll11_opy_):
            logger.error(bstack1l1111l_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࠩࡾࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠣ╁").format(bstack1ll1l1lll11_opy_))
            return []
        data = None
        try:
            with open(bstack1ll1l1lll11_opy_, bstack1l1111l_opy_ (u"ࠦࡷࠨ╂")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1l1111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡐࡓࡐࡐࠣࡪࡷࡵ࡭ࠡࡵࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ╃").format(bstack1ll1l1lll11_opy_, e))
            return []
        _1lll1111lll1_opy_ = None
        _1ll1llll11ll_opy_ = None
        def _1lll111l111l_opy_():
            bstack1ll1lllll111_opy_ = {}
            bstack1lll111llll1_opy_ = {}
            try:
                if self.bstack1lll1111l111_opy_.startswith(bstack1l1111l_opy_ (u"࠭ࡻࠨ╄")) and self.bstack1lll1111l111_opy_.endswith(bstack1l1111l_opy_ (u"ࠧࡾࠩ╅")):
                    bstack1ll1lllll111_opy_ = json.loads(self.bstack1lll1111l111_opy_)
                else:
                    bstack1ll1lllll111_opy_ = dict(item.split(bstack1l1111l_opy_ (u"ࠨ࠼ࠪ╆")) for item in self.bstack1lll1111l111_opy_.split(bstack1l1111l_opy_ (u"ࠩ࠯ࠫ╇")) if bstack1l1111l_opy_ (u"ࠪ࠾ࠬ╈") in item) if self.bstack1lll1111l111_opy_ else {}
                if self.bstack1lll1111l1ll_opy_.startswith(bstack1l1111l_opy_ (u"ࠫࢀ࠭╉")) and self.bstack1lll1111l1ll_opy_.endswith(bstack1l1111l_opy_ (u"ࠬࢃࠧ╊")):
                    bstack1lll111llll1_opy_ = json.loads(self.bstack1lll1111l1ll_opy_)
                else:
                    bstack1lll111llll1_opy_ = dict(item.split(bstack1l1111l_opy_ (u"࠭࠺ࠨ╋")) for item in self.bstack1lll1111l1ll_opy_.split(bstack1l1111l_opy_ (u"ࠧ࠭ࠩ╌")) if bstack1l1111l_opy_ (u"ࠨ࠼ࠪ╍") in item) if self.bstack1lll1111l1ll_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1l1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡩࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡱࡦࡶࡰࡪࡰࡪࡷ࠿ࠦࡻࡾࠤ╎").format(e))
            logger.debug(bstack1l1111l_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠦࡦࡳࡱࡰࠤࡪࡴࡶ࠻ࠢࡾࢁ࠱ࠦࡃࡍࡋ࠽ࠤࢀࢃࠢ╏").format(bstack1ll1lllll111_opy_, bstack1lll111llll1_opy_))
            return bstack1ll1lllll111_opy_, bstack1lll111llll1_opy_
        if _1lll1111lll1_opy_ is None or _1ll1llll11ll_opy_ is None:
            _1lll1111lll1_opy_, _1ll1llll11ll_opy_ = _1lll111l111l_opy_()
        def bstack1lll11l111ll_opy_(name, bstack1lll11l1111l_opy_):
            if name in _1ll1llll11ll_opy_:
                return _1ll1llll11ll_opy_[name]
            if name in _1lll1111lll1_opy_:
                return _1lll1111lll1_opy_[name]
            if bstack1lll11l1111l_opy_.get(bstack1l1111l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ═")):
                return bstack1lll11l1111l_opy_[bstack1l1111l_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ║")]
            return None
        if isinstance(data, dict):
            bstack1ll1lllllll1_opy_ = []
            bstack1lll11111ll1_opy_ = re.compile(bstack1l1111l_opy_ (u"ࡸࠧ࡟࡝ࡄ࠱࡟࠶࠭࠺ࡡࡠ࠯ࠩ࠭╒"))
            for name, bstack1lll11l1111l_opy_ in data.items():
                if not isinstance(bstack1lll11l1111l_opy_, dict):
                    continue
                if not bstack1lll11111ll1_opy_.match(name):
                    logger.warning(bstack1l1111l_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡵࡲࡹࡷࡩࡥࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠥ࡬࡯ࡳ࡯ࡤࡸࠥ࡬࡯ࡳࠢࠪࡿࢂ࠭࠺ࠡࡽࢀࠦ╓").format(name, bstack1lll11l1111l_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1l1111l_opy_ (u"ࠣࡕࡲࡹࡷࡩࡥࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠥ࠭ࡻࡾࠩࠣࡱࡺࡹࡴࠡࡪࡤࡺࡪࠦࡡࠡ࡮ࡨࡲ࡬ࡺࡨࠡࡤࡨࡸࡼ࡫ࡥ࡯ࠢ࠴ࠤࡦࡴࡤࠡ࠵࠳ࠤࡨ࡮ࡡࡳࡣࡦࡸࡪࡸࡳ࠯ࠤ╔").format(name))
                    continue
                bstack1lll11l1111l_opy_ = bstack1lll11l1111l_opy_.copy()
                bstack1lll11l1111l_opy_[bstack1l1111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ╕")] = name
                bstack1lll11l1111l_opy_[bstack1l1111l_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ╖")] = bstack1lll11l111ll_opy_(name, bstack1lll11l1111l_opy_)
                if not bstack1lll11l1111l_opy_.get(bstack1l1111l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ╗")) or bstack1lll11l1111l_opy_.get(bstack1l1111l_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ╘")) == bstack1l1111l_opy_ (u"࠭ࠧ╙"):
                    logger.warning(bstack1l1111l_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡࡰࡲࡸࠥࡹࡰࡦࡥ࡬ࡪ࡮࡫ࡤࠡࡨࡲࡶࠥࡹ࡯ࡶࡴࡦࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ╚").format(name, bstack1lll11l1111l_opy_))
                    continue
                if bstack1lll11l1111l_opy_.get(bstack1l1111l_opy_ (u"ࠨࡤࡤࡷࡪࡈࡲࡢࡰࡦ࡬ࠬ╛")) and bstack1lll11l1111l_opy_[bstack1l1111l_opy_ (u"ࠩࡥࡥࡸ࡫ࡂࡳࡣࡱࡧ࡭࠭╜")] == bstack1lll11l1111l_opy_[bstack1l1111l_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ╝")]:
                    logger.warning(bstack1l1111l_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡧ࡮ࡥࠢࡥࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡸ࡭࡫ࠠࡴࡣࡰࡩࠥ࡬࡯ࡳࠢࡶࡳࡺࡸࡣࡦࠢࠪࡿࢂ࠭࠺ࠡࡽࢀࠦ╞").format(name, bstack1lll11l1111l_opy_))
                    continue
                bstack1lll11111111_opy_ = bstack1lll11l1111l_opy_.get(bstack1l1111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ╟"), bstack1l1111l_opy_ (u"࠭ࡡࡱࡲࠪ╠"))
                if bstack1lll11111111_opy_ not in (bstack1l1111l_opy_ (u"ࠧࡢࡲࡳࠫ╡"), bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹ࠭╢")):
                    logger.warning(bstack1l1111l_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡸࡾࡶࡥࠡࠩࡾࢁࠬࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠭ࠢࡧࡩ࡫ࡧࡵ࡭ࡶ࡬ࡲ࡬ࠦࡴࡰࠢࠪࡥࡵࡶࠧࠣ╣").format(bstack1lll11111111_opy_, name))
                    bstack1lll11111111_opy_ = bstack1l1111l_opy_ (u"ࠪࡥࡵࡶࠧ╤")
                bstack1lll11l1111l_opy_[bstack1l1111l_opy_ (u"ࠫࡹࡿࡰࡦࠩ╥")] = bstack1lll11111111_opy_
                bstack1ll1lllllll1_opy_.append(bstack1lll11l1111l_opy_)
            bstack1ll1llll1l11_opy_ = {item[bstack1l1111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ╦")] for item in bstack1ll1lllllll1_opy_}
            for name, bstack1lll111ll111_opy_ in {**_1lll1111lll1_opy_, **_1ll1llll11ll_opy_}.items():
                if name in bstack1ll1llll1l11_opy_:
                    continue
                if not bstack1lll11111ll1_opy_.match(name):
                    logger.warning(bstack1l1111l_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡱࡸࡶࡨ࡫ࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤ࡫ࡵࡲ࡮ࡣࡷࠤ࡫ࡵࡲࠡࠩࡾࢁࠬࠦࡦࡳࡱࡰࠤࡈࡒࡉ࠰ࡧࡱࡺࠧ╧").format(name))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1l1111l_opy_ (u"ࠢࡔࡱࡸࡶࡨ࡫ࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤࠬࢁࡽࠨࠢࡰࡹࡸࡺࠠࡩࡣࡹࡩࠥࡧࠠ࡭ࡧࡱ࡫ࡹ࡮ࠠࡣࡧࡷࡻࡪ࡫࡮ࠡ࠳ࠣࡥࡳࡪࠠ࠴࠲ࠣࡧ࡭ࡧࡲࡢࡥࡷࡩࡷࡹ࠮ࠣ╨").format(name))
                    continue
                if not bstack1lll111ll111_opy_:
                    continue
                if not isinstance(bstack1lll111ll111_opy_, str):
                    logger.warning(bstack1l1111l_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࠧࡼࡿࠪࠤ࡫ࡸ࡯࡮ࠢࡆࡐࡎ࠵ࡥ࡯ࡸ࠽ࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࠡࡵࡷࡶ࡮ࡴࡧ࠯ࠤ╩").format(name))
                    continue
                bstack1lll111ll1ll_opy_ = bstack1lll111ll111_opy_.strip()
                if bstack1lll111ll1ll_opy_ == bstack1l1111l_opy_ (u"ࠩࠪ╪"):
                    continue
                bstack1ll1lllllll1_opy_.append({bstack1l1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ╫"): name, bstack1l1111l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ╬"): bstack1lll111ll1ll_opy_, bstack1l1111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ╭"): bstack1l1111l_opy_ (u"࠭ࡡࡱࡲࠪ╮")})
            return bstack1ll1lllllll1_opy_
        return data
    def bstack1lll11llll11_opy_(self):
        data = {
            bstack1l1111l_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭╯"): {
                bstack1l1111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ╰"): self.bstack1ll1llllll11_opy_(),
                bstack1l1111l_opy_ (u"ࠩࡰࡳࡩ࡫ࠧ╱"): self.bstack1lll111ll1l1_opy_(),
                bstack1l1111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ╲"): self.bstack1lll11l11lll_opy_()
            }
        }
        return data
    def bstack1ll1llll1ll1_opy_(self, config):
        bstack1lll111111l1_opy_ = {}
        bstack1lll111111l1_opy_[bstack1l1111l_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪ╳")] = {
            bstack1l1111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭╴"): self.bstack1ll1llllll11_opy_(),
            bstack1l1111l_opy_ (u"࠭࡭ࡰࡦࡨࠫ╵"): self.bstack1lll111ll1l1_opy_()
        }
        bstack1lll111111l1_opy_[bstack1l1111l_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࠪ╶")] = {
            bstack1l1111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ╷"): self.bstack1lll11l11ll1_opy_()
        }
        bstack1lll111111l1_opy_[bstack1l1111l_opy_ (u"ࠩࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࡢࡪ࡮ࡸࡳࡵࠩ╸")] = {
            bstack1l1111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ╹"): self.bstack1lll11111l11_opy_()
        }
        bstack1lll111111l1_opy_[bstack1l1111l_opy_ (u"ࠫࡸࡱࡩࡱࡡࡩࡥ࡮ࡲࡩ࡯ࡩࡢࡥࡳࡪ࡟ࡧ࡮ࡤ࡯ࡾ࠭╺")] = {
            bstack1l1111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭╻"): self.bstack1lll111l1111_opy_()
        }
        if self.bstack1111ll11l1_opy_(config):
            bstack1lll111111l1_opy_[bstack1l1111l_opy_ (u"࠭ࡲࡦࡶࡵࡽࡤࡺࡥࡴࡶࡶࡣࡴࡴ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠨ╼")] = {
                bstack1l1111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ╽"): True,
                bstack1l1111l_opy_ (u"ࠨ࡯ࡤࡼࡤࡸࡥࡵࡴ࡬ࡩࡸ࠭╾"): self.bstack1lll1llll1_opy_(config)
            }
        if self.bstack1lllllllll11_opy_(config):
            bstack1lll11l1l1l1_opy_ = config.get(bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭╿"), {}).get(bstack1lll11l11111_opy_, {})
            bstack1lll111l1l1l_opy_ = bstack1lll11l1l1l1_opy_.get(bstack1l1111l_opy_ (u"ࠪࡱࡦࡾࡆࡢ࡫࡯ࡹࡷ࡫ࡳࠨ▀"), 5)
            if isinstance(bstack1lll111l1l1l_opy_, str) and bstack1lll111l1l1l_opy_.endswith(bstack1l1111l_opy_ (u"ࠫࠪ࠭▁")):
                bstack1lll111111ll_opy_ = 0
            else:
                bstack1lll111111ll_opy_ = int(bstack1lll111l1l1l_opy_)
            bstack1lll111111l1_opy_[bstack1l1111l_opy_ (u"ࠬࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧ▂")] = {
                bstack1l1111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ▃"): True,
                bstack1l1111l_opy_ (u"ࠧ࡮ࡣࡻࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡸ࠭▄"): bstack1lll111111ll_opy_
            }
        return bstack1lll111111l1_opy_
    def bstack1l11l1ll1l_opy_(self, config):
        bstack1l1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࡹࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤࡧࡿࠠ࡮ࡣ࡮࡭ࡳ࡭ࠠࡢࠢࡦࡥࡱࡲࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡨࡵࡪ࡮ࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ▅")
        if not (config.get(bstack1l1111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ▆"), None) in bstack11111l11lll_opy_ and self.bstack1ll1llllll11_opy_()):
            return None
        bstack1lll11l1ll11_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ▇"), None)
        logger.debug(bstack1l1111l_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡆࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣ█").format(bstack1lll11l1ll11_opy_))
        try:
            bstack1111l111ll1_opy_ = bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠥ▉").format(bstack1lll11l1ll11_opy_)
            payload = {
                bstack1l1111l_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ▊"): config.get(bstack1l1111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ▋"), bstack1l1111l_opy_ (u"ࠨࠩ▌")),
                bstack1l1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ▍"): config.get(bstack1l1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭▎"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ▏"): os.environ.get(bstack1l1111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦ▐"), bstack1l1111l_opy_ (u"ࠨࠢ░")),
                bstack1l1111l_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ▒"): int(os.environ.get(bstack1l1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ▓")) or bstack1l1111l_opy_ (u"ࠤ࠳ࠦ▔")),
                bstack1l1111l_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ▕"): int(os.environ.get(bstack1l1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ▖")) or bstack1l1111l_opy_ (u"ࠧ࠷ࠢ▗")),
                bstack1l1111l_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣ▘"): get_host_info(),
            }
            logger.debug(bstack1l1111l_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡ࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡴࡦࡿ࡬ࡰࡣࡧ࠾ࠥࢁࡽࠣ▙").format(payload))
            response = bstack1111l111111_opy_.bstack1lll1111llll_opy_(bstack1111l111ll1_opy_, payload)
            if response:
                logger.debug(bstack1l1111l_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡂࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ▚").format(response))
                return response
            else:
                logger.error(bstack1l1111l_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨ▛").format(bstack1lll11l1ll11_opy_))
                return None
        except Exception as e:
            logger.error(bstack1l1111l_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅࠢࡾࢁ࠿ࠦࡻࡾࠤ▜").format(bstack1lll11l1ll11_opy_, e))
            return None