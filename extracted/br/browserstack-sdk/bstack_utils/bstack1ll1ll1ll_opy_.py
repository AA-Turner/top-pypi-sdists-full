# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack11lll1l1l1_opy_, bstack11111ll11ll_opy_
from bstack_utils.helper import bstack1llll1ll111l_opy_, get_host_info
from bstack_utils.bstack1111l111ll1_opy_ import bstack1111l111l1l_opy_
import json
import re
import sys
bstack1lll11lll111_opy_ = bstack1ll_opy_ (u"ࠦࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠥⓧ")
bstack1lll11l11l11_opy_ = bstack1ll_opy_ (u"ࠧࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦⓨ")
bstack1lll111l1ll1_opy_ = bstack1ll_opy_ (u"ࠨࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࡋ࡯ࡲࡴࡶࠥⓩ")
bstack1lll11l1l111_opy_ = bstack1ll_opy_ (u"ࠢࡳࡧࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࠣ⓪")
bstack1lll111l111l_opy_ = bstack1ll_opy_ (u"ࠣࡵ࡮࡭ࡵࡌ࡬ࡢ࡭ࡼࡥࡳࡪࡆࡢ࡫࡯ࡩࡩࠨ⓫")
bstack1lll11111l11_opy_ = bstack1ll_opy_ (u"ࠤࡵࡹࡳ࡙࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࠨ⓬")
bstack1lll11l1l1l1_opy_ = {
    bstack1lll11lll111_opy_,
    bstack1lll11l11l11_opy_,
    bstack1lll111l1ll1_opy_,
    bstack1lll11l1l111_opy_,
    bstack1lll111l111l_opy_,
    bstack1lll11111l11_opy_
}
bstack1lll111lll11_opy_ = {bstack1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⓭")}
logger = logger_utils.get_logger(__name__, bstack11lll1l1l1_opy_)
class bstack1lll11l11lll_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lll1111l111_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l111111ll_opy_:
    _1ll1111l111_opy_ = None
    def __init__(self, config):
        self.bstack1lll11l1ll11_opy_ = False
        self.bstack1lll11lll1ll_opy_ = False
        self.bstack1lll111lll1l_opy_ = False
        self.bstack1lll11ll1ll1_opy_ = False
        self.bstack1lll11111ll1_opy_ = None
        self.bstack1lll111l1lll_opy_ = bstack1lll11l11lll_opy_()
        self.bstack1lll111l1111_opy_ = None
        opts = config.get(bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ⓮"), {})
        self.bstack1lll11l111ll_opy_ = config.get(bstack1ll_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡅࡏࡘࠪ⓯"), bstack1ll_opy_ (u"ࠨࠢ⓰"))
        self.bstack1lll11l11111_opy_ = config.get(bstack1ll_opy_ (u"ࠧࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࡅࡏࡍࠬ⓱"), bstack1ll_opy_ (u"ࠣࠤ⓲"))
        bstack1lll111llll1_opy_ = opts.get(bstack1lll11111l11_opy_, {})
        bstack1lll11ll1l1l_opy_ = None
        if bstack1ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ⓳") in bstack1lll111llll1_opy_:
            bstack1lll11ll1111_opy_ = bstack1lll111llll1_opy_[bstack1ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ⓴")]
            if bstack1lll11ll1111_opy_ is None or (isinstance(bstack1lll11ll1111_opy_, str) and bstack1lll11ll1111_opy_.strip() == bstack1ll_opy_ (u"ࠫࠬ⓵")) or (isinstance(bstack1lll11ll1111_opy_, list) and len(bstack1lll11ll1111_opy_) == 0):
                bstack1lll11ll1l1l_opy_ = []
            elif isinstance(bstack1lll11ll1111_opy_, list):
                bstack1lll11ll1l1l_opy_ = bstack1lll11ll1111_opy_
            elif isinstance(bstack1lll11ll1111_opy_, str) and bstack1lll11ll1111_opy_.strip():
                bstack1lll11ll1l1l_opy_ = bstack1lll11ll1111_opy_
            else:
                logger.warning(bstack1ll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡶࡢ࡮ࡸࡩࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡾࢁ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࡥ࡮ࡲࡷࡽࠥࡲࡩࡴࡶ࠱ࠦ⓶").format(bstack1lll11ll1111_opy_))
                bstack1lll11ll1l1l_opy_ = []
        self.__1lll11111l1l_opy_(
            bstack1lll111llll1_opy_.get(bstack1ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⓷"), False),
            bstack1lll111llll1_opy_.get(bstack1ll_opy_ (u"ࠧ࡮ࡱࡧࡩࠬ⓸"), bstack1ll_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ⓹")),
            bstack1lll11ll1l1l_opy_
        )
        self.__1lll1111l1ll_opy_(opts.get(bstack1lll111l1ll1_opy_, False))
        self.__1lll11ll11ll_opy_(opts.get(bstack1lll11l1l111_opy_, False))
        self.__1lll111ll111_opy_(opts.get(bstack1lll111l111l_opy_, False))
    @classmethod
    def bstack1l111l1111_opy_(cls, config=None):
        if cls._1ll1111l111_opy_ is None and config is not None:
            cls._1ll1111l111_opy_ = bstack1l111111ll_opy_(config)
        return cls._1ll1111l111_opy_
    @staticmethod
    def bstack1ll11llll_opy_(config: dict) -> bool:
        bstack1lll1111l1l1_opy_ = config.get(bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭⓺"), {}).get(bstack1lll11lll111_opy_, {})
        return bstack1lll1111l1l1_opy_.get(bstack1ll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⓻"), False)
    @staticmethod
    def bstack1111l11111_opy_(config: dict) -> int:
        bstack1lll1111l1l1_opy_ = config.get(bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ⓼"), {}).get(bstack1lll11lll111_opy_, {})
        retries = 0
        if bstack1l111111ll_opy_.bstack1ll11llll_opy_(config):
            retries = bstack1lll1111l1l1_opy_.get(bstack1ll_opy_ (u"ࠬࡳࡡࡹࡔࡨࡸࡷ࡯ࡥࡴࠩ⓽"), 1)
        return retries
    @staticmethod
    def bstack1lll11l11l_opy_(config: dict) -> dict:
        bstack1lll1111l11l_opy_ = config.get(bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ⓾"), {})
        return {
            key: value for key, value in bstack1lll1111l11l_opy_.items() if key in bstack1lll11l1l1l1_opy_
        }
    @staticmethod
    def bstack1lll11l1llll_opy_():
        bstack1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⓿")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤ─").format(os.getenv(bstack1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ━")))))
    @staticmethod
    def bstack1lll11lll1l1_opy_(test_name: str):
        bstack1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ│")
        bstack1lll1111lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶࠥ┃").format(os.getenv(bstack1ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ┄"))))
        with open(bstack1lll1111lll1_opy_, bstack1ll_opy_ (u"࠭ࡡࠨ┅")) as file:
            file.write(bstack1ll_opy_ (u"ࠢࡼࡿ࡟ࡲࠧ┆").format(test_name))
    @staticmethod
    def bstack1lll11l1l11l_opy_(framework: str) -> bool:
       return framework.lower() in bstack1lll111lll11_opy_
    @staticmethod
    def bstack1llllllll111_opy_(config: dict) -> bool:
        bstack1lll111ll1l1_opy_ = config.get(bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ┇"), {}).get(bstack1lll11l11l11_opy_, {})
        return bstack1lll111ll1l1_opy_.get(bstack1ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ┈"), False)
    @staticmethod
    def bstack11111111l11_opy_(config: dict, bstack1llllllllll1_opy_: int = 0) -> int:
        bstack1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠱ࠦࡷࡩ࡫ࡦ࡬ࠥࡩࡡ࡯ࠢࡥࡩࠥࡧ࡮ࠡࡣࡥࡷࡴࡲࡵࡵࡧࠣࡲࡺࡳࡢࡦࡴࠣࡳࡷࠦࡡࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺ࡯ࡵࡣ࡯ࡣࡹ࡫ࡳࡵࡵࠣࠬ࡮ࡴࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࠪࡵࡩࡶࡻࡩࡳࡧࡧࠤ࡫ࡵࡲࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠲ࡨࡡࡴࡧࡧࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࡳࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ┉")
        bstack1lll111ll1l1_opy_ = config.get(bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ┊"), {}).get(bstack1ll_opy_ (u"ࠬࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠫ┋"), {})
        bstack1lll111l1l1l_opy_ = 0
        bstack1lll111ll1ll_opy_ = 0
        if bstack1l111111ll_opy_.bstack1llllllll111_opy_(config):
            bstack1lll111ll1ll_opy_ = bstack1lll111ll1l1_opy_.get(bstack1ll_opy_ (u"࠭࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶࠫ┌"), 5)
            if isinstance(bstack1lll111ll1ll_opy_, str) and bstack1lll111ll1ll_opy_.endswith(bstack1ll_opy_ (u"ࠧࠦࠩ┍")):
                try:
                    percentage = int(bstack1lll111ll1ll_opy_.strip(bstack1ll_opy_ (u"ࠨࠧࠪ┎")))
                    if bstack1llllllllll1_opy_ > 0:
                        bstack1lll111l1l1l_opy_ = math.ceil((percentage * bstack1llllllllll1_opy_) / 100)
                    else:
                        raise ValueError(bstack1ll_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨ࠱ࡧࡧࡳࡦࡦࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࡹ࠮ࠣ┏"))
                except ValueError as e:
                    raise ValueError(bstack1ll_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥࠡࡸࡤࡰࡺ࡫ࠠࡧࡱࡵࠤࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴ࠼ࠣࡿࢂࠨ┐").format(bstack1lll111ll1ll_opy_)) from e
            else:
                bstack1lll111l1l1l_opy_ = int(bstack1lll111ll1ll_opy_)
        logger.info(bstack1ll_opy_ (u"ࠦࡒࡧࡸࠡࡨࡤ࡭ࡱࡻࡲࡦࡵࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡳࡦࡶࠣࡸࡴࡀࠠࡼࡿࠣࠬ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡿࢂ࠯ࠢ┑").format(bstack1lll111l1l1l_opy_, bstack1lll111ll1ll_opy_))
        return bstack1lll111l1l1l_opy_
    def bstack1lll1111ll1l_opy_(self):
        return self.bstack1lll11ll1ll1_opy_
    def bstack1lll11111lll_opy_(self):
        return self.bstack1lll11111ll1_opy_
    def bstack1lll11ll1l11_opy_(self):
        return self.bstack1lll111l1111_opy_
    def __1lll11111l1l_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lll11ll1ll1_opy_ = bool(enabled)
            if mode not in [bstack1ll_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ┒"), bstack1ll_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡐࡰ࡯ࡽࠬ┓")]:
                logger.warning(bstack1ll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡱࡴࡪࡥࠡࠩࡾࢁࠬࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠢࡇࡩ࡫ࡧࡵ࡭ࡶ࡬ࡲ࡬ࠦࡴࡰࠢࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ࠲ࠧ└").format(mode))
                mode = bstack1ll_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ┕")
            self.bstack1lll11111ll1_opy_ = mode
            self.bstack1lll111l1111_opy_ = []
            if source is None:
                self.bstack1lll111l1111_opy_ = None
            elif isinstance(source, list):
                self.bstack1lll111l1111_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1ll_opy_ (u"ࠩ࠱࡮ࡸࡵ࡮ࠨ┖")):
                self.bstack1lll111l1111_opy_ = self._1lll111111l1_opy_(source)
            self.__1lll11ll1lll_opy_()
        except Exception as e:
            logger.error(bstack1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࠳ࠠࡦࡰࡤࡦࡱ࡫ࡤ࠻ࠢࡾࢁ࠱ࠦ࡭ࡰࡦࡨ࠾ࠥࢁࡽ࠭ࠢࡶࡳࡺࡸࡣࡦ࠼ࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥ┗").format(enabled, mode, source, e))
    def bstack1lll11ll111l_opy_(self):
        return self.bstack1lll11l1ll11_opy_
    def __1lll1111l1ll_opy_(self, value):
        self.bstack1lll11l1ll11_opy_ = bool(value)
        self.__1lll11ll1lll_opy_()
    def bstack1lll111l1l11_opy_(self):
        return self.bstack1lll11lll1ll_opy_
    def __1lll11ll11ll_opy_(self, value):
        self.bstack1lll11lll1ll_opy_ = bool(value)
        self.__1lll11ll1lll_opy_()
    def bstack1lll111ll11l_opy_(self):
        return self.bstack1lll111lll1l_opy_
    def __1lll111ll111_opy_(self, value):
        self.bstack1lll111lll1l_opy_ = bool(value)
        self.__1lll11ll1lll_opy_()
    def __1lll11ll1lll_opy_(self):
        if self.bstack1lll11ll1ll1_opy_:
            self.bstack1lll11l1ll11_opy_ = False
            self.bstack1lll11lll1ll_opy_ = False
            self.bstack1lll111lll1l_opy_ = False
            self.bstack1lll111l1lll_opy_.enable(bstack1lll11111l11_opy_)
        elif self.bstack1lll11l1ll11_opy_:
            self.bstack1lll11lll1ll_opy_ = False
            self.bstack1lll111lll1l_opy_ = False
            self.bstack1lll11ll1ll1_opy_ = False
            self.bstack1lll111l1lll_opy_.enable(bstack1lll111l1ll1_opy_)
        elif self.bstack1lll11lll1ll_opy_:
            self.bstack1lll11l1ll11_opy_ = False
            self.bstack1lll111lll1l_opy_ = False
            self.bstack1lll11ll1ll1_opy_ = False
            self.bstack1lll111l1lll_opy_.enable(bstack1lll11l1l111_opy_)
        elif self.bstack1lll111lll1l_opy_:
            self.bstack1lll11l1ll11_opy_ = False
            self.bstack1lll11lll1ll_opy_ = False
            self.bstack1lll11ll1ll1_opy_ = False
            self.bstack1lll111l1lll_opy_.enable(bstack1lll111l111l_opy_)
        else:
            self.bstack1lll111l1lll_opy_.disable()
    def bstack1llll111ll_opy_(self):
        return self.bstack1lll111l1lll_opy_.bstack1lll1111l111_opy_()
    def bstack1l1l11ll1_opy_(self):
        if self.bstack1lll111l1lll_opy_.bstack1lll1111l111_opy_():
            return self.bstack1lll111l1lll_opy_.get_name()
        return None
    def _1lll111111l1_opy_(self, bstack1lll111l111_opy_):
        bstack1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡹ࡯ࡶࡴࡦࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣࡥࡳࡪࠠࡧࡱࡵࡱࡦࡺࠠࡪࡶࠣࡪࡴࡸࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡲࡹࡷࡩࡥࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠤ࠭ࡹࡴࡳࠫ࠽ࠤࡕࡧࡴࡩࠢࡷࡳࠥࡺࡨࡦࠢࡍࡗࡔࡔࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࡬ࡪࡵࡷ࠾ࠥࡌ࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡵࡩࡵࡵࡳࡪࡶࡲࡶࡾࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ┘")
        if not os.path.isfile(bstack1lll111l111_opy_):
            logger.error(bstack1ll_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࠫࢀࢃࠧࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠥ┙").format(bstack1lll111l111_opy_))
            return []
        data = None
        try:
            with open(bstack1lll111l111_opy_, bstack1ll_opy_ (u"ࠨࡲࠣ┚")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡋࡕࡒࡒࠥ࡬ࡲࡰ࡯ࠣࡷࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥ┛").format(bstack1lll111l111_opy_, e))
            return []
        _1lll11l1lll1_opy_ = None
        _1lll111l11ll_opy_ = None
        def _1lll11l11ll1_opy_():
            bstack1lll111l11l1_opy_ = {}
            bstack1lll1111llll_opy_ = {}
            try:
                if self.bstack1lll11l111ll_opy_.startswith(bstack1ll_opy_ (u"ࠨࡽࠪ├")) and self.bstack1lll11l111ll_opy_.endswith(bstack1ll_opy_ (u"ࠩࢀࠫ┝")):
                    bstack1lll111l11l1_opy_ = json.loads(self.bstack1lll11l111ll_opy_)
                else:
                    bstack1lll111l11l1_opy_ = dict(item.split(bstack1ll_opy_ (u"ࠪ࠾ࠬ┞")) for item in self.bstack1lll11l111ll_opy_.split(bstack1ll_opy_ (u"ࠫ࠱࠭┟")) if bstack1ll_opy_ (u"ࠬࡀࠧ┠") in item) if self.bstack1lll11l111ll_opy_ else {}
                if self.bstack1lll11l11111_opy_.startswith(bstack1ll_opy_ (u"࠭ࡻࠨ┡")) and self.bstack1lll11l11111_opy_.endswith(bstack1ll_opy_ (u"ࠧࡾࠩ┢")):
                    bstack1lll1111llll_opy_ = json.loads(self.bstack1lll11l11111_opy_)
                else:
                    bstack1lll1111llll_opy_ = dict(item.split(bstack1ll_opy_ (u"ࠨ࠼ࠪ┣")) for item in self.bstack1lll11l11111_opy_.split(bstack1ll_opy_ (u"ࠩ࠯ࠫ┤")) if bstack1ll_opy_ (u"ࠪ࠾ࠬ┥") in item) if self.bstack1lll11l11111_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤ࡫࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡳࡡࡱࡲ࡬ࡲ࡬ࡹ࠺ࠡࡽࢀࠦ┦").format(e))
            logger.debug(bstack1ll_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࡳࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࠽ࠤࢀࢃࠬࠡࡅࡏࡍ࠿ࠦࡻࡾࠤ┧").format(bstack1lll111l11l1_opy_, bstack1lll1111llll_opy_))
            return bstack1lll111l11l1_opy_, bstack1lll1111llll_opy_
        if _1lll11l1lll1_opy_ is None or _1lll111l11ll_opy_ is None:
            _1lll11l1lll1_opy_, _1lll111l11ll_opy_ = _1lll11l11ll1_opy_()
        def bstack1lll11lll11l_opy_(name, bstack1lll11ll11l1_opy_):
            if name in _1lll111l11ll_opy_:
                return _1lll111l11ll_opy_[name]
            if name in _1lll11l1lll1_opy_:
                return _1lll11l1lll1_opy_[name]
            if bstack1lll11ll11l1_opy_.get(bstack1ll_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭┨")):
                return bstack1lll11ll11l1_opy_[bstack1ll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧ┩")]
            return None
        if isinstance(data, dict):
            bstack1lll111111ll_opy_ = []
            bstack1lll11l11l1l_opy_ = re.compile(bstack1ll_opy_ (u"ࡳࠩࡡ࡟ࡆ࠳࡚࠱࠯࠼ࡣࡢ࠱ࠤࠨ┪"))
            for name, bstack1lll11ll11l1_opy_ in data.items():
                if not isinstance(bstack1lll11ll11l1_opy_, dict):
                    continue
                url = bstack1lll11ll11l1_opy_.get(bstack1ll_opy_ (u"ࠩࡸࡶࡱ࠭┫"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1ll_opy_ (u"ࠪࠫ┬")):
                    logger.warning(bstack1ll_opy_ (u"ࠦࡗ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹࠡࡗࡕࡐࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡳࡰࡷࡵࡧࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ┭").format(name, bstack1lll11ll11l1_opy_))
                    continue
                if not bstack1lll11l11l1l_opy_.match(name):
                    logger.warning(bstack1ll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸ࡭ࡢࡶࠣࡪࡴࡸࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ┮").format(name, bstack1lll11ll11l1_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1ll_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࠫࢀࢃࠧࠡ࡯ࡸࡷࡹࠦࡨࡢࡸࡨࠤࡦࠦ࡬ࡦࡰࡪࡸ࡭ࠦࡢࡦࡶࡺࡩࡪࡴࠠ࠲ࠢࡤࡲࡩࠦ࠳࠱ࠢࡦ࡬ࡦࡸࡡࡤࡶࡨࡶࡸ࠴ࠢ┯").format(name))
                    continue
                bstack1lll11ll11l1_opy_ = bstack1lll11ll11l1_opy_.copy()
                bstack1lll11ll11l1_opy_[bstack1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ┰")] = name
                bstack1lll11ll11l1_opy_[bstack1ll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ┱")] = bstack1lll11lll11l_opy_(name, bstack1lll11ll11l1_opy_)
                if not bstack1lll11ll11l1_opy_.get(bstack1ll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ┲")) or bstack1lll11ll11l1_opy_.get(bstack1ll_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ┳")) == bstack1ll_opy_ (u"ࠫࠬ┴"):
                    logger.warning(bstack1ll_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡮ࡰࡶࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡩࡩࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ┵").format(name, bstack1lll11ll11l1_opy_))
                    continue
                if bstack1lll11ll11l1_opy_.get(bstack1ll_opy_ (u"࠭ࡢࡢࡵࡨࡆࡷࡧ࡮ࡤࡪࠪ┶")) and bstack1lll11ll11l1_opy_[bstack1ll_opy_ (u"ࠧࡣࡣࡶࡩࡇࡸࡡ࡯ࡥ࡫ࠫ┷")] == bstack1lll11ll11l1_opy_[bstack1ll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ┸")]:
                    logger.warning(bstack1ll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡥࡳࡪࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡶ࡫ࡩࠥࡹࡡ࡮ࡧࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ┹").format(name, bstack1lll11ll11l1_opy_))
                    continue
                bstack1lll111111ll_opy_.append(bstack1lll11ll11l1_opy_)
            return bstack1lll111111ll_opy_
        return data
    def bstack1lll11llll11_opy_(self):
        data = {
            bstack1ll_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ┺"): {
                bstack1ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ┻"): self.bstack1lll1111ll1l_opy_(),
                bstack1ll_opy_ (u"ࠬࡳ࡯ࡥࡧࠪ┼"): self.bstack1lll11111lll_opy_(),
                bstack1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭┽"): self.bstack1lll11ll1l11_opy_()
            }
        }
        return data
    def bstack1lll11l111l1_opy_(self, config):
        bstack1lll11l1111l_opy_ = {}
        bstack1lll11l1111l_opy_[bstack1ll_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭┾")] = {
            bstack1ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ┿"): self.bstack1lll1111ll1l_opy_(),
            bstack1ll_opy_ (u"ࠩࡰࡳࡩ࡫ࠧ╀"): self.bstack1lll11111lll_opy_()
        }
        bstack1lll11l1111l_opy_[bstack1ll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩ࠭╁")] = {
            bstack1ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ╂"): self.bstack1lll111l1l11_opy_()
        }
        bstack1lll11l1111l_opy_[bstack1ll_opy_ (u"ࠬࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩࡥࡦࡪࡴࡶࡸࠬ╃")] = {
            bstack1ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ╄"): self.bstack1lll11ll111l_opy_()
        }
        bstack1lll11l1111l_opy_[bstack1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡤ࡬ࡡࡪ࡮࡬ࡲ࡬ࡥࡡ࡯ࡦࡢࡪࡱࡧ࡫ࡺࠩ╅")] = {
            bstack1ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ╆"): self.bstack1lll111ll11l_opy_()
        }
        if self.bstack1ll11llll_opy_(config):
            bstack1lll11l1111l_opy_[bstack1ll_opy_ (u"ࠩࡵࡩࡹࡸࡹࡠࡶࡨࡷࡹࡹ࡟ࡰࡰࡢࡪࡦ࡯࡬ࡶࡴࡨࠫ╇")] = {
                bstack1ll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ╈"): True,
                bstack1ll_opy_ (u"ࠫࡲࡧࡸࡠࡴࡨࡸࡷ࡯ࡥࡴࠩ╉"): self.bstack1111l11111_opy_(config)
            }
        if self.bstack1llllllll111_opy_(config):
            bstack1lll111lllll_opy_ = config.get(bstack1ll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ╊"), {}).get(bstack1lll11l11l11_opy_, {})
            bstack1lll111ll1ll_opy_ = bstack1lll111lllll_opy_.get(bstack1ll_opy_ (u"࠭࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶࠫ╋"), 5)
            if isinstance(bstack1lll111ll1ll_opy_, str) and bstack1lll111ll1ll_opy_.endswith(bstack1ll_opy_ (u"ࠧࠦࠩ╌")):
                bstack1lll1111ll11_opy_ = 0
            else:
                bstack1lll1111ll11_opy_ = int(bstack1lll111ll1ll_opy_)
            bstack1lll11l1111l_opy_[bstack1ll_opy_ (u"ࠨࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡯࡯ࡡࡩࡥ࡮ࡲࡵࡳࡧࠪ╍")] = {
                bstack1ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ╎"): True,
                bstack1ll_opy_ (u"ࠪࡱࡦࡾ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡴࠩ╏"): bstack1lll1111ll11_opy_
            }
        return bstack1lll11l1111l_opy_
    def bstack1l1111ll11_opy_(self, config):
        bstack1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡲࡰࡱ࡫ࡣࡵࡵࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡣࡻࠣࡱࡦࡱࡩ࡯ࡩࠣࡥࠥࡩࡡ࡭࡮ࠣࡸࡴࠦࡴࡩࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠡࡧࡱࡨࡵࡵࡩ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠦࠨࡴࡶࡵ࠭࠿ࠦࡔࡩࡧ࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡤࡸ࡭ࡱࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ═")
        if not (config.get(bstack1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ║"), None) in bstack11111ll11ll_opy_ and self.bstack1lll1111ll1l_opy_()):
            return None
        bstack1lll11l1l1ll_opy_ = os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ╒"), None)
        logger.debug(bstack1ll_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡉ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊ࠺ࠡࡽࢀࠦ╓").format(bstack1lll11l1l1ll_opy_))
        try:
            bstack1111l11l11l_opy_ = bstack1ll_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠨ╔").format(bstack1lll11l1l1ll_opy_)
            payload = {
                bstack1ll_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢ╕"): config.get(bstack1ll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ╖"), bstack1ll_opy_ (u"ࠫࠬ╗")),
                bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ╘"): config.get(bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ╙"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ╚"): os.environ.get(bstack1ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ╛"), bstack1ll_opy_ (u"ࠤࠥ╜")),
                bstack1ll_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨ╝"): int(os.environ.get(bstack1ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ╞")) or bstack1ll_opy_ (u"ࠧ࠶ࠢ╟")),
                bstack1ll_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥ╠"): int(os.environ.get(bstack1ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ╡")) or bstack1ll_opy_ (u"ࠣ࠳ࠥ╢")),
                bstack1ll_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦ╣"): get_host_info(),
            }
            logger.debug(bstack1ll_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡰࡢࡻ࡯ࡳࡦࡪ࠺ࠡࡽࢀࠦ╤").format(payload))
            response = bstack1111l111l1l_opy_.bstack1lll11l1ll1l_opy_(bstack1111l11l11l_opy_, payload)
            if response:
                logger.debug(bstack1ll_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡅࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ╥").format(response))
                return response
            else:
                logger.error(bstack1ll_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈ࠿ࠦࡻࡾࠤ╦").format(bstack1lll11l1l1ll_opy_))
                return None
        except Exception as e:
            logger.error(bstack1ll_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈࠥࢁࡽ࠻ࠢࡾࢁࠧ╧").format(bstack1lll11l1l1ll_opy_, e))
            return None