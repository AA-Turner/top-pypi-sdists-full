# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack1111ll1111_opy_, bstack111111l1111_opy_
from bstack_utils.helper import bstack1llll11ll111_opy_, get_host_info
from bstack_utils.bstack1111l111l1l_opy_ import bstack1111l1111ll_opy_
import json
import re
import sys
bstack1lll11l1111l_opy_ = bstack111ll11_opy_ (u"ࠢࡳࡧࡷࡶࡾ࡚ࡥࡴࡶࡶࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨ┍")
bstack1lll11l1l11l_opy_ = bstack111ll11_opy_ (u"ࠣࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢ┎")
bstack1lll111l111l_opy_ = bstack111ll11_opy_ (u"ࠤࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࡇ࡫ࡵࡷࡹࠨ┏")
bstack1lll1111l11l_opy_ = bstack111ll11_opy_ (u"ࠥࡶࡪࡸࡵ࡯ࡒࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡋࡧࡩ࡭ࡧࡧࠦ┐")
bstack1lll11111ll1_opy_ = bstack111ll11_opy_ (u"ࠦࡸࡱࡩࡱࡈ࡯ࡥࡰࡿࡡ࡯ࡦࡉࡥ࡮ࡲࡥࡥࠤ┑")
bstack1lll11l1lll1_opy_ = bstack111ll11_opy_ (u"ࠧࡸࡵ࡯ࡕࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠤ┒")
bstack1lll111ll11l_opy_ = {
    bstack1lll11l1111l_opy_,
    bstack1lll11l1l11l_opy_,
    bstack1lll111l111l_opy_,
    bstack1lll1111l11l_opy_,
    bstack1lll11111ll1_opy_,
    bstack1lll11l1lll1_opy_
}
bstack1ll1llllllll_opy_ = {bstack111ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭┓")}
logger = logger_utils.get_logger(__name__, bstack1111ll1111_opy_)
class bstack1lll111l1ll1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lll111llll1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l1111ll11_opy_:
    _1l1lllll111_opy_ = None
    def __init__(self, config):
        self.bstack1lll11l1l1ll_opy_ = False
        self.bstack1lll1111l1l1_opy_ = False
        self.bstack1ll1lllllll1_opy_ = False
        self.bstack1lll111l11ll_opy_ = False
        self.bstack1lll11l11lll_opy_ = None
        self.bstack1lll11l1l1l1_opy_ = bstack1lll111l1ll1_opy_()
        self.bstack1lll11ll11l1_opy_ = None
        opts = config.get(bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ└"), {})
        self.bstack1ll1llllll1l_opy_ = config.get(bstack111ll11_opy_ (u"ࠨࡵࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࡈࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࡦࡵࡈࡒ࡛࠭┕"), bstack111ll11_opy_ (u"ࠤࠥ┖"))
        self.bstack1lll111l1l11_opy_ = config.get(bstack111ll11_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡈࡒࡉࠨ┗"), bstack111ll11_opy_ (u"ࠦࠧ┘"))
        bstack1ll1llll1ll1_opy_ = opts.get(bstack1lll11l1lll1_opy_, {})
        bstack1lll11l1ll1l_opy_ = None
        if bstack111ll11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ┙") in bstack1ll1llll1ll1_opy_:
            bstack1lll11l1llll_opy_ = bstack1ll1llll1ll1_opy_[bstack111ll11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭┚")]
            if bstack1lll11l1llll_opy_ is None or (isinstance(bstack1lll11l1llll_opy_, str) and bstack1lll11l1llll_opy_.strip() == bstack111ll11_opy_ (u"ࠧࠨ┛")) or (isinstance(bstack1lll11l1llll_opy_, list) and len(bstack1lll11l1llll_opy_) == 0):
                bstack1lll11l1ll1l_opy_ = []
            elif isinstance(bstack1lll11l1llll_opy_, list):
                bstack1lll11l1ll1l_opy_ = bstack1lll11l1llll_opy_
            elif isinstance(bstack1lll11l1llll_opy_, str) and bstack1lll11l1llll_opy_.strip():
                bstack1lll11l1ll1l_opy_ = bstack1lll11l1llll_opy_
            else:
                logger.warning(bstack111ll11_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡶࡳࡺࡸࡣࡦࠢࡹࡥࡱࡻࡥࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽ࠯ࠢࡇࡩ࡫ࡧࡵ࡭ࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡨࡱࡵࡺࡹࠡ࡮࡬ࡷࡹ࠴ࠢ├").format(bstack1lll11l1llll_opy_))
                bstack1lll11l1ll1l_opy_ = []
        self.__1lll1111ll11_opy_(
            bstack1ll1llll1ll1_opy_.get(bstack111ll11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ┝"), False),
            bstack1ll1llll1ll1_opy_.get(bstack111ll11_opy_ (u"ࠪࡱࡴࡪࡥࠨ┞"), bstack111ll11_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡌࡩࡳࡵࡷࠫ┟")),
            bstack1lll11l1ll1l_opy_
        )
        self.__1lll111l11l1_opy_(opts.get(bstack1lll111l111l_opy_, False))
        self.__1ll1llllll11_opy_(opts.get(bstack1lll1111l11l_opy_, False))
        self.__1lll11l1l111_opy_(opts.get(bstack1lll11111ll1_opy_, False))
    @classmethod
    def bstack1lllll1lll1_opy_(cls, config=None):
        if cls._1l1lllll111_opy_ is None and config is not None:
            cls._1l1lllll111_opy_ = bstack1l1111ll11_opy_(config)
        return cls._1l1lllll111_opy_
    @staticmethod
    def bstack11111lll1l_opy_(config: dict) -> bool:
        bstack1ll1lllll11l_opy_ = config.get(bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ┠"), {}).get(bstack1lll11l1111l_opy_, {})
        return bstack1ll1lllll11l_opy_.get(bstack111ll11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ┡"), False)
    @staticmethod
    def bstack1l11l1l1l_opy_(config: dict) -> int:
        bstack1ll1lllll11l_opy_ = config.get(bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ┢"), {}).get(bstack1lll11l1111l_opy_, {})
        retries = 0
        if bstack1l1111ll11_opy_.bstack11111lll1l_opy_(config):
            retries = bstack1ll1lllll11l_opy_.get(bstack111ll11_opy_ (u"ࠨ࡯ࡤࡼࡗ࡫ࡴࡳ࡫ࡨࡷࠬ┣"), 1)
        return retries
    @staticmethod
    def bstack111llll111_opy_(config: dict) -> dict:
        bstack1lll11ll1111_opy_ = config.get(bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭┤"), {})
        return {
            key: value for key, value in bstack1lll11ll1111_opy_.items() if key in bstack1lll111ll11l_opy_
        }
    @staticmethod
    def bstack1lll11l11111_opy_():
        bstack111ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ┥")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧ┦").format(os.getenv(bstack111ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ┧")))))
    @staticmethod
    def bstack1lll111l1lll_opy_(test_name: str):
        bstack111ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ┨")
        bstack1ll1llll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨ┩").format(os.getenv(bstack111ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ┪"))))
        with open(bstack1ll1llll1lll_opy_, bstack111ll11_opy_ (u"ࠩࡤࠫ┫")) as file:
            file.write(bstack111ll11_opy_ (u"ࠥࡿࢂࡢ࡮ࠣ┬").format(test_name))
    @staticmethod
    def bstack1lll11111l11_opy_(framework: str) -> bool:
       return framework.lower() in bstack1ll1llllllll_opy_
    @staticmethod
    def bstack11111111ll1_opy_(config: dict) -> bool:
        bstack1lll11l111l1_opy_ = config.get(bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ┭"), {}).get(bstack1lll11l1l11l_opy_, {})
        return bstack1lll11l111l1_opy_.get(bstack111ll11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭┮"), False)
    @staticmethod
    def bstack1llllllll1ll_opy_(config: dict, bstack11111111l11_opy_: int = 0) -> int:
        bstack111ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠭ࠢࡺ࡬࡮ࡩࡨࠡࡥࡤࡲࠥࡨࡥࠡࡣࡱࠤࡦࡨࡳࡰ࡮ࡸࡸࡪࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡳࠢࡤࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭ࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡲࡸࡦࡲ࡟ࡵࡧࡶࡸࡸࠦࠨࡪࡰࡷ࠭࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤ࠭ࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ┯")
        bstack1lll11l111l1_opy_ = config.get(bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ┰"), {}).get(bstack111ll11_opy_ (u"ࠨࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧ┱"), {})
        bstack1lll11l11l11_opy_ = 0
        bstack1lll11ll111l_opy_ = 0
        if bstack1l1111ll11_opy_.bstack11111111ll1_opy_(config):
            bstack1lll11ll111l_opy_ = bstack1lll11l111l1_opy_.get(bstack111ll11_opy_ (u"ࠩࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹࠧ┲"), 5)
            if isinstance(bstack1lll11ll111l_opy_, str) and bstack1lll11ll111l_opy_.endswith(bstack111ll11_opy_ (u"ࠪࠩࠬ┳")):
                try:
                    percentage = int(bstack1lll11ll111l_opy_.strip(bstack111ll11_opy_ (u"ࠫࠪ࠭┴")))
                    if bstack11111111l11_opy_ > 0:
                        bstack1lll11l11l11_opy_ = math.ceil((percentage * bstack11111111l11_opy_) / 100)
                    else:
                        raise ValueError(bstack111ll11_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡱࡺࡹࡴࠡࡤࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵ࠱ࠦ┵"))
                except ValueError as e:
                    raise ValueError(bstack111ll11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨࠤࡻࡧ࡬ࡶࡧࠣࡪࡴࡸࠠ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷ࠿ࠦࡻࡾࠤ┶").format(bstack1lll11ll111l_opy_)) from e
            else:
                bstack1lll11l11l11_opy_ = int(bstack1lll11ll111l_opy_)
        logger.info(bstack111ll11_opy_ (u"ࠢࡎࡣࡻࠤ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡶࡩࡹࠦࡴࡰ࠼ࠣࡿࢂࠦࠨࡧࡴࡲࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾࠫࠥ┷").format(bstack1lll11l11l11_opy_, bstack1lll11ll111l_opy_))
        return bstack1lll11l11l11_opy_
    def bstack1ll1lllll1ll_opy_(self):
        return self.bstack1lll111l11ll_opy_
    def bstack1ll1lllll111_opy_(self):
        return self.bstack1lll11l11lll_opy_
    def bstack1lll1111l111_opy_(self):
        return self.bstack1lll11ll11l1_opy_
    def __1lll1111ll11_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lll111l11ll_opy_ = bool(enabled)
            if mode not in [bstack111ll11_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ┸"), bstack111ll11_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡓࡳࡲࡹࠨ┹")]:
                logger.warning(bstack111ll11_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡳࡡࡳࡶࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦ࡭ࡰࡦࡨࠤࠬࢁࡽࠨࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠥࡊࡥࡧࡣࡸࡰࡹ࡯࡮ࡨࠢࡷࡳࠥ࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭࠮ࠣ┺").format(mode))
                mode = bstack111ll11_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡌࡩࡳࡵࡷࠫ┻")
            self.bstack1lll11l11lll_opy_ = mode
            self.bstack1lll11ll11l1_opy_ = []
            if source is None:
                self.bstack1lll11ll11l1_opy_ = None
            elif isinstance(source, list):
                self.bstack1lll11ll11l1_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack111ll11_opy_ (u"ࠬ࠴ࡪࡴࡱࡱࠫ┼")):
                self.bstack1lll11ll11l1_opy_ = self._1lll111111ll_opy_(source)
            self.__1lll11l11ll1_opy_()
        except Exception as e:
            logger.error(bstack111ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳ࡮ࡣࡵࡸࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡ࠯ࠣࡩࡳࡧࡢ࡭ࡧࡧ࠾ࠥࢁࡽ࠭ࠢࡰࡳࡩ࡫࠺ࠡࡽࢀ࠰ࠥࡹ࡯ࡶࡴࡦࡩ࠿ࠦࡻࡾ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ┽").format(enabled, mode, source, e))
    def bstack1lll111ll1l1_opy_(self):
        return self.bstack1lll11l1l1ll_opy_
    def __1lll111l11l1_opy_(self, value):
        self.bstack1lll11l1l1ll_opy_ = bool(value)
        self.__1lll11l11ll1_opy_()
    def bstack1lll1111lll1_opy_(self):
        return self.bstack1lll1111l1l1_opy_
    def __1ll1llllll11_opy_(self, value):
        self.bstack1lll1111l1l1_opy_ = bool(value)
        self.__1lll11l11ll1_opy_()
    def bstack1lll111ll1ll_opy_(self):
        return self.bstack1ll1lllllll1_opy_
    def __1lll11l1l111_opy_(self, value):
        self.bstack1ll1lllllll1_opy_ = bool(value)
        self.__1lll11l11ll1_opy_()
    def __1lll11l11ll1_opy_(self):
        if self.bstack1lll111l11ll_opy_:
            self.bstack1lll11l1l1ll_opy_ = False
            self.bstack1lll1111l1l1_opy_ = False
            self.bstack1ll1lllllll1_opy_ = False
            self.bstack1lll11l1l1l1_opy_.enable(bstack1lll11l1lll1_opy_)
        elif self.bstack1lll11l1l1ll_opy_:
            self.bstack1lll1111l1l1_opy_ = False
            self.bstack1ll1lllllll1_opy_ = False
            self.bstack1lll111l11ll_opy_ = False
            self.bstack1lll11l1l1l1_opy_.enable(bstack1lll111l111l_opy_)
        elif self.bstack1lll1111l1l1_opy_:
            self.bstack1lll11l1l1ll_opy_ = False
            self.bstack1ll1lllllll1_opy_ = False
            self.bstack1lll111l11ll_opy_ = False
            self.bstack1lll11l1l1l1_opy_.enable(bstack1lll1111l11l_opy_)
        elif self.bstack1ll1lllllll1_opy_:
            self.bstack1lll11l1l1ll_opy_ = False
            self.bstack1lll1111l1l1_opy_ = False
            self.bstack1lll111l11ll_opy_ = False
            self.bstack1lll11l1l1l1_opy_.enable(bstack1lll11111ll1_opy_)
        else:
            self.bstack1lll11l1l1l1_opy_.disable()
    def bstack1l111l1ll_opy_(self):
        return self.bstack1lll11l1l1l1_opy_.bstack1lll111llll1_opy_()
    def bstack1l11l1111l_opy_(self):
        if self.bstack1lll11l1l1l1_opy_.bstack1lll111llll1_opy_():
            return self.bstack1lll11l1l1l1_opy_.get_name()
        return None
    def _1lll111111ll_opy_(self, bstack1ll1ll11l1l_opy_):
        bstack111ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡵࡲࡹࡷࡩࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠦࡡ࡯ࡦࠣࡪࡴࡸ࡭ࡢࡶࠣ࡭ࡹࠦࡦࡰࡴࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡸࡵࡵࡳࡥࡨࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠠࠩࡵࡷࡶ࠮ࡀࠠࡑࡣࡷ࡬ࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡓࡐࡐࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡯࡭ࡸࡺ࠺ࠡࡈࡲࡶࡲࡧࡴࡵࡧࡧࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡸࡥࡱࡱࡶ࡭ࡹࡵࡲࡺࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ┾")
        if not os.path.isfile(bstack1ll1ll11l1l_opy_):
            logger.error(bstack111ll11_opy_ (u"ࠣࡕࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠦࠧࡼࡿࠪࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠳ࠨ┿").format(bstack1ll1ll11l1l_opy_))
            return []
        data = None
        try:
            with open(bstack1ll1ll11l1l_opy_, bstack111ll11_opy_ (u"ࠤࡵࠦ╀")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack111ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡎࡘࡕࡎࠡࡨࡵࡳࡲࠦࡳࡰࡷࡵࡧࡪࠦࡦࡪ࡮ࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ╁").format(bstack1ll1ll11l1l_opy_, e))
            return []
        _1lll11111lll_opy_ = None
        _1lll111111l1_opy_ = None
        def _1lll11l111ll_opy_():
            bstack1lll111lllll_opy_ = {}
            bstack1lll1111111l_opy_ = {}
            try:
                if self.bstack1ll1llllll1l_opy_.startswith(bstack111ll11_opy_ (u"ࠫࢀ࠭╂")) and self.bstack1ll1llllll1l_opy_.endswith(bstack111ll11_opy_ (u"ࠬࢃࠧ╃")):
                    bstack1lll111lllll_opy_ = json.loads(self.bstack1ll1llllll1l_opy_)
                else:
                    bstack1lll111lllll_opy_ = dict(item.split(bstack111ll11_opy_ (u"࠭࠺ࠨ╄")) for item in self.bstack1ll1llllll1l_opy_.split(bstack111ll11_opy_ (u"ࠧ࠭ࠩ╅")) if bstack111ll11_opy_ (u"ࠨ࠼ࠪ╆") in item) if self.bstack1ll1llllll1l_opy_ else {}
                if self.bstack1lll111l1l11_opy_.startswith(bstack111ll11_opy_ (u"ࠩࡾࠫ╇")) and self.bstack1lll111l1l11_opy_.endswith(bstack111ll11_opy_ (u"ࠪࢁࠬ╈")):
                    bstack1lll1111111l_opy_ = json.loads(self.bstack1lll111l1l11_opy_)
                else:
                    bstack1lll1111111l_opy_ = dict(item.split(bstack111ll11_opy_ (u"ࠫ࠿࠭╉")) for item in self.bstack1lll111l1l11_opy_.split(bstack111ll11_opy_ (u"ࠬ࠲ࠧ╊")) if bstack111ll11_opy_ (u"࠭࠺ࠨ╋") in item) if self.bstack1lll111l1l11_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack111ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡧࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡ࡯ࡤࡴࡵ࡯࡮ࡨࡵ࠽ࠤࢀࢃࠢ╌").format(e))
            logger.debug(bstack111ll11_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡰࡥࡵࡶࡩ࡯ࡩࡶࠤ࡫ࡸ࡯࡮ࠢࡨࡲࡻࡀࠠࡼࡿ࠯ࠤࡈࡒࡉ࠻ࠢࡾࢁࠧ╍").format(bstack1lll111lllll_opy_, bstack1lll1111111l_opy_))
            return bstack1lll111lllll_opy_, bstack1lll1111111l_opy_
        if _1lll11111lll_opy_ is None or _1lll111111l1_opy_ is None:
            _1lll11111lll_opy_, _1lll111111l1_opy_ = _1lll11l111ll_opy_()
        def bstack1lll111lll1l_opy_(name, bstack1lll1111llll_opy_):
            if name in _1lll111111l1_opy_:
                return _1lll111111l1_opy_[name]
            if name in _1lll11111lll_opy_:
                return _1lll11111lll_opy_[name]
            if bstack1lll1111llll_opy_.get(bstack111ll11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ╎")):
                return bstack1lll1111llll_opy_[bstack111ll11_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ╏")]
            return None
        if isinstance(data, dict):
            bstack1lll111l1111_opy_ = []
            bstack1lll111lll11_opy_ = re.compile(bstack111ll11_opy_ (u"ࡶࠬࡤ࡛ࡂ࠯࡝࠴࠲࠿࡟࡞࠭ࠧࠫ═"))
            for name, bstack1lll1111llll_opy_ in data.items():
                if not isinstance(bstack1lll1111llll_opy_, dict):
                    continue
                if not bstack1lll111lll11_opy_.match(name):
                    logger.warning(bstack111ll11_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸ࡭ࡢࡶࠣࡪࡴࡸࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ║").format(name, bstack1lll1111llll_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack111ll11_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࠫࢀࢃࠧࠡ࡯ࡸࡷࡹࠦࡨࡢࡸࡨࠤࡦࠦ࡬ࡦࡰࡪࡸ࡭ࠦࡢࡦࡶࡺࡩࡪࡴࠠ࠲ࠢࡤࡲࡩࠦ࠳࠱ࠢࡦ࡬ࡦࡸࡡࡤࡶࡨࡶࡸ࠴ࠢ╒").format(name))
                    continue
                bstack1lll1111llll_opy_ = bstack1lll1111llll_opy_.copy()
                bstack1lll1111llll_opy_[bstack111ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ╓")] = name
                bstack1lll1111llll_opy_[bstack111ll11_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ╔")] = bstack1lll111lll1l_opy_(name, bstack1lll1111llll_opy_)
                if not bstack1lll1111llll_opy_.get(bstack111ll11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ╕")) or bstack1lll1111llll_opy_.get(bstack111ll11_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ╖")) == bstack111ll11_opy_ (u"ࠫࠬ╗"):
                    logger.warning(bstack111ll11_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡮ࡰࡶࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡩࡩࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ╘").format(name, bstack1lll1111llll_opy_))
                    continue
                if bstack1lll1111llll_opy_.get(bstack111ll11_opy_ (u"࠭ࡢࡢࡵࡨࡆࡷࡧ࡮ࡤࡪࠪ╙")) and bstack1lll1111llll_opy_[bstack111ll11_opy_ (u"ࠧࡣࡣࡶࡩࡇࡸࡡ࡯ࡥ࡫ࠫ╚")] == bstack1lll1111llll_opy_[bstack111ll11_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ╛")]:
                    logger.warning(bstack111ll11_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡥࡳࡪࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡶ࡫ࡩࠥࡹࡡ࡮ࡧࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ╜").format(name, bstack1lll1111llll_opy_))
                    continue
                bstack1lll11111l1l_opy_ = bstack1lll1111llll_opy_.get(bstack111ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨ╝"), bstack111ll11_opy_ (u"ࠫࡦࡶࡰࠨ╞"))
                if bstack1lll11111l1l_opy_ not in (bstack111ll11_opy_ (u"ࠬࡧࡰࡱࠩ╟"), bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࠫ╠")):
                    logger.warning(bstack111ll11_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡶࡼࡴࡪࠦࠧࡼࡿࠪࠤ࡫ࡵࡲࠡࡵࡲࡹࡷࡩࡥࠡࠩࡾࢁࠬ࠲ࠠࡥࡧࡩࡥࡺࡲࡴࡪࡰࡪࠤࡹࡵࠠࠨࡣࡳࡴࠬࠨ╡").format(bstack1lll11111l1l_opy_, name))
                    bstack1lll11111l1l_opy_ = bstack111ll11_opy_ (u"ࠨࡣࡳࡴࠬ╢")
                bstack1lll1111llll_opy_[bstack111ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ╣")] = bstack1lll11111l1l_opy_
                bstack1lll111l1111_opy_.append(bstack1lll1111llll_opy_)
            bstack1lll111l1l1l_opy_ = {item[bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ╤")] for item in bstack1lll111l1111_opy_}
            for name, bstack1lll11l1ll11_opy_ in {**_1lll11111lll_opy_, **_1lll111111l1_opy_}.items():
                if name in bstack1lll111l1l1l_opy_:
                    continue
                if not bstack1lll111lll11_opy_.match(name):
                    logger.warning(bstack111ll11_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡹ࡯ࡶࡴࡦࡩࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠢࡩࡳࡷࡳࡡࡵࠢࡩࡳࡷࠦࠧࡼࡿࠪࠤ࡫ࡸ࡯࡮ࠢࡆࡐࡎ࠵ࡥ࡯ࡸࠥ╥").format(name))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack111ll11_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠢࠪࡿࢂ࠭ࠠ࡮ࡷࡶࡸࠥ࡮ࡡࡷࡧࠣࡥࠥࡲࡥ࡯ࡩࡷ࡬ࠥࡨࡥࡵࡹࡨࡩࡳࠦ࠱ࠡࡣࡱࡨࠥ࠹࠰ࠡࡥ࡫ࡥࡷࡧࡣࡵࡧࡵࡷ࠳ࠨ╦").format(name))
                    continue
                if not bstack1lll11l1ll11_opy_:
                    continue
                if not isinstance(bstack1lll11l1ll11_opy_, str):
                    logger.warning(bstack111ll11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࠬࢁࡽࠨࠢࡩࡶࡴࡳࠠࡄࡎࡌ࠳ࡪࡴࡶ࠻ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࠦࡳࡵࡴ࡬ࡲ࡬࠴ࠢ╧").format(name))
                    continue
                bstack1lll11111111_opy_ = bstack1lll11l1ll11_opy_.strip()
                if bstack1lll11111111_opy_ == bstack111ll11_opy_ (u"ࠧࠨ╨"):
                    continue
                bstack1lll111l1111_opy_.append({bstack111ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭╩"): name, bstack111ll11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ╪"): bstack1lll11111111_opy_, bstack111ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨ╫"): bstack111ll11_opy_ (u"ࠫࡦࡶࡰࠨ╬")})
            return bstack1lll111l1111_opy_
        return data
    def bstack1lll1l1111l1_opy_(self):
        data = {
            bstack111ll11_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫ╭"): {
                bstack111ll11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ╮"): self.bstack1ll1lllll1ll_opy_(),
                bstack111ll11_opy_ (u"ࠧ࡮ࡱࡧࡩࠬ╯"): self.bstack1ll1lllll111_opy_(),
                bstack111ll11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ╰"): self.bstack1lll1111l111_opy_()
            }
        }
        return data
    def bstack1ll1lllll1l1_opy_(self, config):
        bstack1lll11l11l1l_opy_ = {}
        bstack1lll11l11l1l_opy_[bstack111ll11_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨ╱")] = {
            bstack111ll11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ╲"): self.bstack1ll1lllll1ll_opy_(),
            bstack111ll11_opy_ (u"ࠫࡲࡵࡤࡦࠩ╳"): self.bstack1ll1lllll111_opy_()
        }
        bstack1lll11l11l1l_opy_[bstack111ll11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡵࡸࡥࡷ࡫ࡲࡹࡸࡲࡹࡠࡨࡤ࡭ࡱ࡫ࡤࠨ╴")] = {
            bstack111ll11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ╵"): self.bstack1lll1111lll1_opy_()
        }
        bstack1lll11l11l1l_opy_[bstack111ll11_opy_ (u"ࠧࡳࡷࡱࡣࡵࡸࡥࡷ࡫ࡲࡹࡸࡲࡹࡠࡨࡤ࡭ࡱ࡫ࡤࡠࡨ࡬ࡶࡸࡺࠧ╶")] = {
            bstack111ll11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ╷"): self.bstack1lll111ll1l1_opy_()
        }
        bstack1lll11l11l1l_opy_[bstack111ll11_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡧࡣ࡬ࡰ࡮ࡴࡧࡠࡣࡱࡨࡤ࡬࡬ࡢ࡭ࡼࠫ╸")] = {
            bstack111ll11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ╹"): self.bstack1lll111ll1ll_opy_()
        }
        if self.bstack11111lll1l_opy_(config):
            bstack1lll11l11l1l_opy_[bstack111ll11_opy_ (u"ࠫࡷ࡫ࡴࡳࡻࡢࡸࡪࡹࡴࡴࡡࡲࡲࡤ࡬ࡡࡪ࡮ࡸࡶࡪ࠭╺")] = {
                bstack111ll11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭╻"): True,
                bstack111ll11_opy_ (u"࠭࡭ࡢࡺࡢࡶࡪࡺࡲࡪࡧࡶࠫ╼"): self.bstack1l11l1l1l_opy_(config)
            }
        if self.bstack11111111ll1_opy_(config):
            bstack1ll1llll1l1l_opy_ = config.get(bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ╽"), {}).get(bstack1lll11l1l11l_opy_, {})
            bstack1lll11ll111l_opy_ = bstack1ll1llll1l1l_opy_.get(bstack111ll11_opy_ (u"ࠨ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸ࠭╾"), 5)
            if isinstance(bstack1lll11ll111l_opy_, str) and bstack1lll11ll111l_opy_.endswith(bstack111ll11_opy_ (u"ࠩࠨࠫ╿")):
                bstack1lll1111ll1l_opy_ = 0
            else:
                bstack1lll1111ll1l_opy_ = int(bstack1lll11ll111l_opy_)
            bstack1lll11l11l1l_opy_[bstack111ll11_opy_ (u"ࠪࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡱࡱࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠬ▀")] = {
                bstack111ll11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ▁"): True,
                bstack111ll11_opy_ (u"ࠬࡳࡡࡹࡡࡩࡥ࡮ࡲࡵࡳࡧࡶࠫ▂"): bstack1lll1111ll1l_opy_
            }
        return bstack1lll11l11l1l_opy_
    def bstack1l1l1l1ll1_opy_(self, config):
        bstack111ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡴࡲ࡬ࡦࡥࡷࡷࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡥࡽࠥࡳࡡ࡬࡫ࡱ࡫ࠥࡧࠠࡤࡣ࡯ࡰࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩ࡛ࠥࡕࡊࡆࠣࡳ࡫ࠦࡴࡩࡧࠣࡦࡺ࡯࡬ࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ▃")
        if not (config.get(bstack111ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ▄"), None) in bstack111111l1111_opy_ and self.bstack1ll1lllll1ll_opy_()):
            return None
        bstack1lll1111l1ll_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭▅"), None)
        logger.debug(bstack111ll11_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡄࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨ▆").format(bstack1lll1111l1ll_opy_))
        try:
            bstack1111l11l111_opy_ = bstack111ll11_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠣ▇").format(bstack1lll1111l1ll_opy_)
            payload = {
                bstack111ll11_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤ█"): config.get(bstack111ll11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ▉"), bstack111ll11_opy_ (u"࠭ࠧ▊")),
                bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥ▋"): config.get(bstack111ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ▌"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ▍"): os.environ.get(bstack111ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠤ▎"), bstack111ll11_opy_ (u"ࠦࠧ▏")),
                bstack111ll11_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣ▐"): int(os.environ.get(bstack111ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤ░")) or bstack111ll11_opy_ (u"ࠢ࠱ࠤ▒")),
                bstack111ll11_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧ▓"): int(os.environ.get(bstack111ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦ▔")) or bstack111ll11_opy_ (u"ࠥ࠵ࠧ▕")),
                bstack111ll11_opy_ (u"ࠦ࡭ࡵࡳࡵࡋࡱࡪࡴࠨ▖"): get_host_info(),
            }
            logger.debug(bstack111ll11_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡲࡤࡽࡱࡵࡡࡥ࠼ࠣࡿࢂࠨ▗").format(payload))
            response = bstack1111l1111ll_opy_.bstack1lll111ll111_opy_(bstack1111l11l111_opy_, payload)
            if response:
                logger.debug(bstack111ll11_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡇࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ▘").format(response))
                return response
            else:
                logger.error(bstack111ll11_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊ࠺ࠡࡽࢀࠦ▙").format(bstack1lll1111l1ll_opy_))
                return None
        except Exception as e:
            logger.error(bstack111ll11_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊࠠࡼࡿ࠽ࠤࢀࢃࠢ▚").format(bstack1lll1111l1ll_opy_, e))
            return None