# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack1ll11l1111_opy_, bstack11111ll11ll_opy_
from bstack_utils.helper import bstack1lllllll1l1l_opy_, get_host_info
from bstack_utils.bstack1111l11ll1l_opy_ import bstack1111l11l11l_opy_
import json
import re
import sys
bstack1lll1111ll11_opy_ = bstack1ll1l11_opy_ (u"ࠢࡳࡧࡷࡶࡾ࡚ࡥࡴࡶࡶࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨⓣ")
bstack1lll11ll1lll_opy_ = bstack1ll1l11_opy_ (u"ࠣࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢⓤ")
bstack1lll11ll111l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࡇ࡫ࡵࡷࡹࠨⓥ")
bstack1lll111ll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠥࡶࡪࡸࡵ࡯ࡒࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡋࡧࡩ࡭ࡧࡧࠦⓦ")
bstack1lll11l1l1ll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡸࡱࡩࡱࡈ࡯ࡥࡰࡿࡡ࡯ࡦࡉࡥ࡮ࡲࡥࡥࠤⓧ")
bstack1lll11l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠧࡸࡵ࡯ࡕࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠤⓨ")
bstack1lll111ll111_opy_ = {
    bstack1lll1111ll11_opy_,
    bstack1lll11ll1lll_opy_,
    bstack1lll11ll111l_opy_,
    bstack1lll111ll1ll_opy_,
    bstack1lll11l1l1ll_opy_,
    bstack1lll11l11ll1_opy_
}
bstack1lll11l1ll11_opy_ = {bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ⓩ")}
logger = logger_utils.get_logger(__name__, bstack1ll11l1111_opy_)
class bstack1lll11ll1l11_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lll11l1l1l1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack11l1ll1ll_opy_:
    _1ll11111111_opy_ = None
    def __init__(self, config):
        self.bstack1lll1l111111_opy_ = False
        self.bstack1lll111lllll_opy_ = False
        self.bstack1lll11l11l11_opy_ = False
        self.bstack1lll11l11111_opy_ = False
        self.bstack1lll11l11l1l_opy_ = None
        self.bstack1lll111lll11_opy_ = bstack1lll11ll1l11_opy_()
        self.bstack1lll111l111l_opy_ = None
        opts = config.get(bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ⓪"), {})
        self.bstack1lll1111l1ll_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠨࡵࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࡈࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࡦࡵࡈࡒ࡛࠭⓫"), bstack1ll1l11_opy_ (u"ࠤࠥ⓬"))
        self.bstack1lll11l111ll_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡈࡒࡉࠨ⓭"), bstack1ll1l11_opy_ (u"ࠦࠧ⓮"))
        bstack1lll111l1l11_opy_ = opts.get(bstack1lll11l11ll1_opy_, {})
        bstack1lll11llllll_opy_ = None
        if bstack1ll1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ⓯") in bstack1lll111l1l11_opy_:
            bstack1lll11llll11_opy_ = bstack1lll111l1l11_opy_[bstack1ll1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭⓰")]
            if bstack1lll11llll11_opy_ is None or (isinstance(bstack1lll11llll11_opy_, str) and bstack1lll11llll11_opy_.strip() == bstack1ll1l11_opy_ (u"ࠧࠨ⓱")) or (isinstance(bstack1lll11llll11_opy_, list) and len(bstack1lll11llll11_opy_) == 0):
                bstack1lll11llllll_opy_ = []
            elif isinstance(bstack1lll11llll11_opy_, list):
                bstack1lll11llllll_opy_ = bstack1lll11llll11_opy_
            elif isinstance(bstack1lll11llll11_opy_, str) and bstack1lll11llll11_opy_.strip():
                bstack1lll11llllll_opy_ = bstack1lll11llll11_opy_
            else:
                logger.warning(bstack1ll1l11_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡶࡳࡺࡸࡣࡦࠢࡹࡥࡱࡻࡥࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽ࠯ࠢࡇࡩ࡫ࡧࡵ࡭ࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡨࡱࡵࡺࡹࠡ࡮࡬ࡷࡹ࠴ࠢ⓲").format(bstack1lll11llll11_opy_))
                bstack1lll11llllll_opy_ = []
        self.__1lll11l11lll_opy_(
            bstack1lll111l1l11_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ⓳"), False),
            bstack1lll111l1l11_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡱࡴࡪࡥࠨ⓴"), bstack1ll1l11_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡌࡩࡳࡵࡷࠫ⓵")),
            bstack1lll11llllll_opy_
        )
        self.__1lll11lll11l_opy_(opts.get(bstack1lll11ll111l_opy_, False))
        self.__1lll11lll1ll_opy_(opts.get(bstack1lll111ll1ll_opy_, False))
        self.__1lll11l1lll1_opy_(opts.get(bstack1lll11l1l1ll_opy_, False))
    @classmethod
    def bstack1lllllll1_opy_(cls, config=None):
        if cls._1ll11111111_opy_ is None and config is not None:
            cls._1ll11111111_opy_ = bstack11l1ll1ll_opy_(config)
        return cls._1ll11111111_opy_
    @staticmethod
    def bstack111llll11l_opy_(config: dict) -> bool:
        bstack1lll11l1ll1l_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⓶"), {}).get(bstack1lll1111ll11_opy_, {})
        return bstack1lll11l1ll1l_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⓷"), False)
    @staticmethod
    def bstack1l1lll11_opy_(config: dict) -> int:
        bstack1lll11l1ll1l_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ⓸"), {}).get(bstack1lll1111ll11_opy_, {})
        retries = 0
        if bstack11l1ll1ll_opy_.bstack111llll11l_opy_(config):
            retries = bstack1lll11l1ll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡤࡼࡗ࡫ࡴࡳ࡫ࡨࡷࠬ⓹"), 1)
        return retries
    @staticmethod
    def bstack1ll1lll1ll_opy_(config: dict) -> dict:
        bstack1lll111l11l1_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭⓺"), {})
        return {
            key: value for key, value in bstack1lll111l11l1_opy_.items() if key in bstack1lll111ll111_opy_
        }
    @staticmethod
    def bstack1lll111l1l1l_opy_():
        bstack1ll1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⓻")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧ⓼").format(os.getenv(bstack1ll1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⓽")))))
    @staticmethod
    def bstack1lll1111ll1l_opy_(test_name: str):
        bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⓾")
        bstack1lll11ll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨ⓿").format(os.getenv(bstack1ll1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ─"))))
        with open(bstack1lll11ll1l1l_opy_, bstack1ll1l11_opy_ (u"ࠩࡤࠫ━")) as file:
            file.write(bstack1ll1l11_opy_ (u"ࠥࡿࢂࡢ࡮ࠣ│").format(test_name))
    @staticmethod
    def bstack1lll11ll1ll1_opy_(framework: str) -> bool:
       return framework.lower() in bstack1lll11l1ll11_opy_
    @staticmethod
    def bstack11111111l1l_opy_(config: dict) -> bool:
        bstack1lll11l1l111_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ┃"), {}).get(bstack1lll11ll1lll_opy_, {})
        return bstack1lll11l1l111_opy_.get(bstack1ll1l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭┄"), False)
    @staticmethod
    def bstack1111111l1ll_opy_(config: dict, bstack1111111l11l_opy_: int = 0) -> int:
        bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠭ࠢࡺ࡬࡮ࡩࡨࠡࡥࡤࡲࠥࡨࡥࠡࡣࡱࠤࡦࡨࡳࡰ࡮ࡸࡸࡪࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡳࠢࡤࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭ࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡲࡸࡦࡲ࡟ࡵࡧࡶࡸࡸࠦࠨࡪࡰࡷ࠭࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤ࠭ࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ┅")
        bstack1lll11l1l111_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ┆"), {}).get(bstack1ll1l11_opy_ (u"ࠨࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧ┇"), {})
        bstack1lll111l1ll1_opy_ = 0
        bstack1lll11llll1l_opy_ = 0
        if bstack11l1ll1ll_opy_.bstack11111111l1l_opy_(config):
            bstack1lll11llll1l_opy_ = bstack1lll11l1l111_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹࠧ┈"), 5)
            if isinstance(bstack1lll11llll1l_opy_, str) and bstack1lll11llll1l_opy_.endswith(bstack1ll1l11_opy_ (u"ࠪࠩࠬ┉")):
                try:
                    percentage = int(bstack1lll11llll1l_opy_.strip(bstack1ll1l11_opy_ (u"ࠫࠪ࠭┊")))
                    if bstack1111111l11l_opy_ > 0:
                        bstack1lll111l1ll1_opy_ = math.ceil((percentage * bstack1111111l11l_opy_) / 100)
                    else:
                        raise ValueError(bstack1ll1l11_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡱࡺࡹࡴࠡࡤࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵ࠱ࠦ┋"))
                except ValueError as e:
                    raise ValueError(bstack1ll1l11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨࠤࡻࡧ࡬ࡶࡧࠣࡪࡴࡸࠠ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷ࠿ࠦࡻࡾࠤ┌").format(bstack1lll11llll1l_opy_)) from e
            else:
                bstack1lll111l1ll1_opy_ = int(bstack1lll11llll1l_opy_)
        logger.info(bstack1ll1l11_opy_ (u"ࠢࡎࡣࡻࠤ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡶࡩࡹࠦࡴࡰ࠼ࠣࡿࢂࠦࠨࡧࡴࡲࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾࠫࠥ┍").format(bstack1lll111l1ll1_opy_, bstack1lll11llll1l_opy_))
        return bstack1lll111l1ll1_opy_
    def bstack1lll111llll1_opy_(self):
        return self.bstack1lll11l11111_opy_
    def bstack1lll11lllll1_opy_(self):
        return self.bstack1lll11l11l1l_opy_
    def bstack1lll111lll1l_opy_(self):
        return self.bstack1lll111l111l_opy_
    def __1lll11l11lll_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lll11l11111_opy_ = bool(enabled)
            if mode not in [bstack1ll1l11_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ┎"), bstack1ll1l11_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡓࡳࡲࡹࠨ┏")]:
                logger.warning(bstack1ll1l11_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡳࡡࡳࡶࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦ࡭ࡰࡦࡨࠤࠬࢁࡽࠨࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠥࡊࡥࡧࡣࡸࡰࡹ࡯࡮ࡨࠢࡷࡳࠥ࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭࠮ࠣ┐").format(mode))
                mode = bstack1ll1l11_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡌࡩࡳࡵࡷࠫ┑")
            self.bstack1lll11l11l1l_opy_ = mode
            self.bstack1lll111l111l_opy_ = []
            if source is None:
                self.bstack1lll111l111l_opy_ = None
            elif isinstance(source, list):
                self.bstack1lll111l111l_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1ll1l11_opy_ (u"ࠬ࠴ࡪࡴࡱࡱࠫ┒")):
                self.bstack1lll111l111l_opy_ = self._1lll1111l1l1_opy_(source)
            self.__1lll11l1llll_opy_()
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳ࡮ࡣࡵࡸࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡ࠯ࠣࡩࡳࡧࡢ࡭ࡧࡧ࠾ࠥࢁࡽ࠭ࠢࡰࡳࡩ࡫࠺ࠡࡽࢀ࠰ࠥࡹ࡯ࡶࡴࡦࡩ࠿ࠦࡻࡾ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ┓").format(enabled, mode, source, e))
    def bstack1lll111l1111_opy_(self):
        return self.bstack1lll1l111111_opy_
    def __1lll11lll11l_opy_(self, value):
        self.bstack1lll1l111111_opy_ = bool(value)
        self.__1lll11l1llll_opy_()
    def bstack1lll1l11111l_opy_(self):
        return self.bstack1lll111lllll_opy_
    def __1lll11lll1ll_opy_(self, value):
        self.bstack1lll111lllll_opy_ = bool(value)
        self.__1lll11l1llll_opy_()
    def bstack1lll11ll11ll_opy_(self):
        return self.bstack1lll11l11l11_opy_
    def __1lll11l1lll1_opy_(self, value):
        self.bstack1lll11l11l11_opy_ = bool(value)
        self.__1lll11l1llll_opy_()
    def __1lll11l1llll_opy_(self):
        if self.bstack1lll11l11111_opy_:
            self.bstack1lll1l111111_opy_ = False
            self.bstack1lll111lllll_opy_ = False
            self.bstack1lll11l11l11_opy_ = False
            self.bstack1lll111lll11_opy_.enable(bstack1lll11l11ll1_opy_)
        elif self.bstack1lll1l111111_opy_:
            self.bstack1lll111lllll_opy_ = False
            self.bstack1lll11l11l11_opy_ = False
            self.bstack1lll11l11111_opy_ = False
            self.bstack1lll111lll11_opy_.enable(bstack1lll11ll111l_opy_)
        elif self.bstack1lll111lllll_opy_:
            self.bstack1lll1l111111_opy_ = False
            self.bstack1lll11l11l11_opy_ = False
            self.bstack1lll11l11111_opy_ = False
            self.bstack1lll111lll11_opy_.enable(bstack1lll111ll1ll_opy_)
        elif self.bstack1lll11l11l11_opy_:
            self.bstack1lll1l111111_opy_ = False
            self.bstack1lll111lllll_opy_ = False
            self.bstack1lll11l11111_opy_ = False
            self.bstack1lll111lll11_opy_.enable(bstack1lll11l1l1ll_opy_)
        else:
            self.bstack1lll111lll11_opy_.disable()
    def bstack1l11111ll1_opy_(self):
        return self.bstack1lll111lll11_opy_.bstack1lll11l1l1l1_opy_()
    def bstack111l11111_opy_(self):
        if self.bstack1lll111lll11_opy_.bstack1lll11l1l1l1_opy_():
            return self.bstack1lll111lll11_opy_.get_name()
        return None
    def _1lll1111l1l1_opy_(self, bstack1ll1lll1l11_opy_):
        bstack1ll1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡵࡲࡹࡷࡩࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠦࡡ࡯ࡦࠣࡪࡴࡸ࡭ࡢࡶࠣ࡭ࡹࠦࡦࡰࡴࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡸࡵࡵࡳࡥࡨࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠠࠩࡵࡷࡶ࠮ࡀࠠࡑࡣࡷ࡬ࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡓࡐࡐࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡯࡭ࡸࡺ࠺ࠡࡈࡲࡶࡲࡧࡴࡵࡧࡧࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡸࡥࡱࡱࡶ࡭ࡹࡵࡲࡺࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ└")
        if not os.path.isfile(bstack1ll1lll1l11_opy_):
            logger.error(bstack1ll1l11_opy_ (u"ࠣࡕࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠦࠧࡼࡿࠪࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠳ࠨ┕").format(bstack1ll1lll1l11_opy_))
            return []
        data = None
        try:
            with open(bstack1ll1lll1l11_opy_, bstack1ll1l11_opy_ (u"ࠤࡵࠦ┖")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡎࡘࡕࡎࠡࡨࡵࡳࡲࠦࡳࡰࡷࡵࡧࡪࠦࡦࡪ࡮ࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ┗").format(bstack1ll1lll1l11_opy_, e))
            return []
        _1lll111ll11l_opy_ = None
        _1lll11lll1l1_opy_ = None
        def _1lll11ll11l1_opy_():
            bstack1lll1111lll1_opy_ = {}
            bstack1lll111ll1l1_opy_ = {}
            try:
                if self.bstack1lll1111l1ll_opy_.startswith(bstack1ll1l11_opy_ (u"ࠫࢀ࠭┘")) and self.bstack1lll1111l1ll_opy_.endswith(bstack1ll1l11_opy_ (u"ࠬࢃࠧ┙")):
                    bstack1lll1111lll1_opy_ = json.loads(self.bstack1lll1111l1ll_opy_)
                else:
                    bstack1lll1111lll1_opy_ = dict(item.split(bstack1ll1l11_opy_ (u"࠭࠺ࠨ┚")) for item in self.bstack1lll1111l1ll_opy_.split(bstack1ll1l11_opy_ (u"ࠧ࠭ࠩ┛")) if bstack1ll1l11_opy_ (u"ࠨ࠼ࠪ├") in item) if self.bstack1lll1111l1ll_opy_ else {}
                if self.bstack1lll11l111ll_opy_.startswith(bstack1ll1l11_opy_ (u"ࠩࡾࠫ┝")) and self.bstack1lll11l111ll_opy_.endswith(bstack1ll1l11_opy_ (u"ࠪࢁࠬ┞")):
                    bstack1lll111ll1l1_opy_ = json.loads(self.bstack1lll11l111ll_opy_)
                else:
                    bstack1lll111ll1l1_opy_ = dict(item.split(bstack1ll1l11_opy_ (u"ࠫ࠿࠭┟")) for item in self.bstack1lll11l111ll_opy_.split(bstack1ll1l11_opy_ (u"ࠬ࠲ࠧ┠")) if bstack1ll1l11_opy_ (u"࠭࠺ࠨ┡") in item) if self.bstack1lll11l111ll_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡧࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡ࡯ࡤࡴࡵ࡯࡮ࡨࡵ࠽ࠤࢀࢃࠢ┢").format(e))
            logger.debug(bstack1ll1l11_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡰࡥࡵࡶࡩ࡯ࡩࡶࠤ࡫ࡸ࡯࡮ࠢࡨࡲࡻࡀࠠࡼࡿ࠯ࠤࡈࡒࡉ࠻ࠢࡾࢁࠧ┣").format(bstack1lll1111lll1_opy_, bstack1lll111ll1l1_opy_))
            return bstack1lll1111lll1_opy_, bstack1lll111ll1l1_opy_
        if _1lll111ll11l_opy_ is None or _1lll11lll1l1_opy_ is None:
            _1lll111ll11l_opy_, _1lll11lll1l1_opy_ = _1lll11ll11l1_opy_()
        def bstack1lll1111llll_opy_(name, bstack1lll11l1l11l_opy_):
            if name in _1lll11lll1l1_opy_:
                return _1lll11lll1l1_opy_[name]
            if name in _1lll111ll11l_opy_:
                return _1lll111ll11l_opy_[name]
            if bstack1lll11l1l11l_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ┤")):
                return bstack1lll11l1l11l_opy_[bstack1ll1l11_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ┥")]
            return None
        if isinstance(data, dict):
            bstack1lll11l111l1_opy_ = []
            bstack1lll111l11ll_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡶࠬࡤ࡛ࡂ࠯࡝࠴࠲࠿࡟࡞࠭ࠧࠫ┦"))
            for name, bstack1lll11l1l11l_opy_ in data.items():
                if not isinstance(bstack1lll11l1l11l_opy_, dict):
                    continue
                url = bstack1lll11l1l11l_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡻࡲ࡭ࠩ┧"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1ll1l11_opy_ (u"࠭ࠧ┨")):
                    logger.warning(bstack1ll1l11_opy_ (u"ࠢࡓࡧࡳࡳࡸ࡯ࡴࡰࡴࡼࠤ࡚ࡘࡌࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡶࡳࡺࡸࡣࡦࠢࠪࡿࢂ࠭࠺ࠡࡽࢀࠦ┩").format(name, bstack1lll11l1l11l_opy_))
                    continue
                if not bstack1lll111l11ll_opy_.match(name):
                    logger.warning(bstack1ll1l11_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡶࡳࡺࡸࡣࡦࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠦࡦࡰࡴࡰࡥࡹࠦࡦࡰࡴࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ┪").format(name, bstack1lll11l1l11l_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1ll1l11_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠦࠧࡼࡿࠪࠤࡲࡻࡳࡵࠢ࡫ࡥࡻ࡫ࠠࡢࠢ࡯ࡩࡳ࡭ࡴࡩࠢࡥࡩࡹࡽࡥࡦࡰࠣ࠵ࠥࡧ࡮ࡥࠢ࠶࠴ࠥࡩࡨࡢࡴࡤࡧࡹ࡫ࡲࡴ࠰ࠥ┫").format(name))
                    continue
                bstack1lll11l1l11l_opy_ = bstack1lll11l1l11l_opy_.copy()
                bstack1lll11l1l11l_opy_[bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ┬")] = name
                bstack1lll11l1l11l_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ┭")] = bstack1lll1111llll_opy_(name, bstack1lll11l1l11l_opy_)
                if not bstack1lll11l1l11l_opy_.get(bstack1ll1l11_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ┮")) or bstack1lll11l1l11l_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭┯")) == bstack1ll1l11_opy_ (u"ࠧࠨ┰"):
                    logger.warning(bstack1ll1l11_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡱࡳࡹࠦࡳࡱࡧࡦ࡭࡫࡯ࡥࡥࠢࡩࡳࡷࠦࡳࡰࡷࡵࡧࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ┱").format(name, bstack1lll11l1l11l_opy_))
                    continue
                if bstack1lll11l1l11l_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡥࡥࡸ࡫ࡂࡳࡣࡱࡧ࡭࠭┲")) and bstack1lll11l1l11l_opy_[bstack1ll1l11_opy_ (u"ࠪࡦࡦࡹࡥࡃࡴࡤࡲࡨ࡮ࠧ┳")] == bstack1lll11l1l11l_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ┴")]:
                    logger.warning(bstack1ll1l11_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡡ࡯ࡦࠣࡦࡦࡹࡥࠡࡤࡵࡥࡳࡩࡨࠡࡥࡤࡲࡳࡵࡴࠡࡤࡨࠤࡹ࡮ࡥࠡࡵࡤࡱࡪࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ┵").format(name, bstack1lll11l1l11l_opy_))
                    continue
                bstack1lll11l111l1_opy_.append(bstack1lll11l1l11l_opy_)
            return bstack1lll11l111l1_opy_
        return data
    def bstack1lll1l11ll1l_opy_(self):
        data = {
            bstack1ll1l11_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ┶"): {
                bstack1ll1l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ┷"): self.bstack1lll111llll1_opy_(),
                bstack1ll1l11_opy_ (u"ࠨ࡯ࡲࡨࡪ࠭┸"): self.bstack1lll11lllll1_opy_(),
                bstack1ll1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ┹"): self.bstack1lll111lll1l_opy_()
            }
        }
        return data
    def bstack1lll111l1lll_opy_(self, config):
        bstack1lll11l1111l_opy_ = {}
        bstack1lll11l1111l_opy_[bstack1ll1l11_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ┺")] = {
            bstack1ll1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ┻"): self.bstack1lll111llll1_opy_(),
            bstack1ll1l11_opy_ (u"ࠬࡳ࡯ࡥࡧࠪ┼"): self.bstack1lll11lllll1_opy_()
        }
        bstack1lll11l1111l_opy_[bstack1ll1l11_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࠩ┽")] = {
            bstack1ll1l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ┾"): self.bstack1lll1l11111l_opy_()
        }
        bstack1lll11l1111l_opy_[bstack1ll1l11_opy_ (u"ࠨࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࡡࡩ࡭ࡷࡹࡴࠨ┿")] = {
            bstack1ll1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ╀"): self.bstack1lll111l1111_opy_()
        }
        bstack1lll11l1111l_opy_[bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡨࡤ࡭ࡱ࡯࡮ࡨࡡࡤࡲࡩࡥࡦ࡭ࡣ࡮ࡽࠬ╁")] = {
            bstack1ll1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ╂"): self.bstack1lll11ll11ll_opy_()
        }
        if self.bstack111llll11l_opy_(config):
            bstack1lll11l1111l_opy_[bstack1ll1l11_opy_ (u"ࠬࡸࡥࡵࡴࡼࡣࡹ࡫ࡳࡵࡵࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧ╃")] = {
                bstack1ll1l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ╄"): True,
                bstack1ll1l11_opy_ (u"ࠧ࡮ࡣࡻࡣࡷ࡫ࡴࡳ࡫ࡨࡷࠬ╅"): self.bstack1l1lll11_opy_(config)
            }
        if self.bstack11111111l1l_opy_(config):
            bstack1lll11l1111l_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡯࡯ࡡࡩࡥ࡮ࡲࡵࡳࡧࠪ╆")] = {
                bstack1ll1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ╇"): True,
                bstack1ll1l11_opy_ (u"ࠪࡱࡦࡾ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡴࠩ╈"): self.bstack1111111l1ll_opy_(config)
            }
        return bstack1lll11l1111l_opy_
    def bstack1l111ll111_opy_(self, config):
        bstack1ll1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡲࡰࡱ࡫ࡣࡵࡵࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡣࡻࠣࡱࡦࡱࡩ࡯ࡩࠣࡥࠥࡩࡡ࡭࡮ࠣࡸࡴࠦࡴࡩࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠡࡧࡱࡨࡵࡵࡩ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠦࠨࡴࡶࡵ࠭࠿ࠦࡔࡩࡧ࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡤࡸ࡭ࡱࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ╉")
        if not (config.get(bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ╊"), None) in bstack11111ll11ll_opy_ and self.bstack1lll111llll1_opy_()):
            return None
        bstack1lll11ll1111_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ╋"), None)
        logger.debug(bstack1ll1l11_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡉ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊ࠺ࠡࡽࢀࠦ╌").format(bstack1lll11ll1111_opy_))
        try:
            bstack1111l1l1111_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠨ╍").format(bstack1lll11ll1111_opy_)
            payload = {
                bstack1ll1l11_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢ╎"): config.get(bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ╏"), bstack1ll1l11_opy_ (u"ࠫࠬ═")),
                bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ║"): config.get(bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ╒"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ╓"): os.environ.get(bstack1ll1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ╔"), bstack1ll1l11_opy_ (u"ࠤࠥ╕")),
                bstack1ll1l11_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨ╖"): int(os.environ.get(bstack1ll1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ╗")) or bstack1ll1l11_opy_ (u"ࠧ࠶ࠢ╘")),
                bstack1ll1l11_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥ╙"): int(os.environ.get(bstack1ll1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ╚")) or bstack1ll1l11_opy_ (u"ࠣ࠳ࠥ╛")),
                bstack1ll1l11_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦ╜"): get_host_info(),
            }
            logger.debug(bstack1ll1l11_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡰࡢࡻ࡯ࡳࡦࡪ࠺ࠡࡽࢀࠦ╝").format(payload))
            response = bstack1111l11l11l_opy_.bstack1lll11lll111_opy_(bstack1111l1l1111_opy_, payload)
            if response:
                logger.debug(bstack1ll1l11_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡅࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ╞").format(response))
                return response
            else:
                logger.error(bstack1ll1l11_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈ࠿ࠦࡻࡾࠤ╟").format(bstack1lll11ll1111_opy_))
                return None
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈࠥࢁࡽ࠻ࠢࡾࢁࠧ╠").format(bstack1lll11ll1111_opy_, e))
            return None