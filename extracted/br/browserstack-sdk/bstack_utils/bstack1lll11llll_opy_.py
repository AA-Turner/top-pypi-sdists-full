# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack1111lll111_opy_, bstack111l11ll1l1_opy_
from bstack_utils.helper import bstack1lllllllllll_opy_, get_host_info
from bstack_utils.bstack111l1lll11l_opy_ import bstack111l1llll11_opy_
import json
import re
import sys
bstack1llll1l11l11_opy_ = bstack1ll1lll_opy_ (u"ࠣࡴࡨࡸࡷࡿࡔࡦࡵࡷࡷࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢ⋞")
bstack1llll11ll111_opy_ = bstack1ll1lll_opy_ (u"ࠤࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣ⋟")
bstack1lll1lllllll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡶࡺࡴࡐࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡉࡥ࡮ࡲࡥࡥࡈ࡬ࡶࡸࡺࠢ⋠")
bstack1llll1l1llll_opy_ = bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࠧ⋡")
bstack1lll1llll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡉࡰࡦࡱࡹࡢࡰࡧࡊࡦ࡯࡬ࡦࡦࠥ⋢")
bstack1llll1l1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡲࡶࡰࡖࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࠥ⋣")
bstack1llll111ll1l_opy_ = {
    bstack1llll1l11l11_opy_,
    bstack1llll11ll111_opy_,
    bstack1lll1lllllll_opy_,
    bstack1llll1l1llll_opy_,
    bstack1lll1llll1ll_opy_,
    bstack1llll1l1lll1_opy_
}
bstack1llll1l1ll1l_opy_ = {bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⋤")}
logger = logger_utils.get_logger(__name__, bstack1111lll111_opy_)
class bstack1llll11l11l1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1llll1111l11_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l11ll1ll1_opy_:
    _1ll1ll1ll11_opy_ = None
    def __init__(self, config):
        self.bstack1llll11111ll_opy_ = False
        self.bstack1llll1l1111l_opy_ = False
        self.bstack1llll111l1ll_opy_ = False
        self.bstack1llll1111l1l_opy_ = False
        self.bstack1llll11111l1_opy_ = None
        self.bstack1llll1l1l11l_opy_ = bstack1llll11l11l1_opy_()
        self.bstack1llll11llll1_opy_ = None
        opts = config.get(bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⋥"), {})
        self.bstack1llll111l11l_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠩࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡉࡓ࡜ࠧ⋦"), bstack1ll1lll_opy_ (u"ࠥࠦ⋧"))
        self.bstack1llll1l11111_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠫࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡉࡌࡊࠩ⋨"), bstack1ll1lll_opy_ (u"ࠧࠨ⋩"))
        bstack1llll11l1l11_opy_ = opts.get(bstack1llll1l1lll1_opy_, {})
        bstack1llll11l11ll_opy_ = None
        if bstack1ll1lll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭⋪") in bstack1llll11l1l11_opy_:
            bstack1llll1111ll1_opy_ = bstack1llll11l1l11_opy_[bstack1ll1lll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ⋫")]
            if bstack1llll1111ll1_opy_ is None or (isinstance(bstack1llll1111ll1_opy_, str) and bstack1llll1111ll1_opy_.strip() == bstack1ll1lll_opy_ (u"ࠨࠩ⋬")) or (isinstance(bstack1llll1111ll1_opy_, list) and len(bstack1llll1111ll1_opy_) == 0):
                bstack1llll11l11ll_opy_ = []
            elif isinstance(bstack1llll1111ll1_opy_, list):
                bstack1llll11l11ll_opy_ = bstack1llll1111ll1_opy_
            elif isinstance(bstack1llll1111ll1_opy_, str) and bstack1llll1111ll1_opy_.strip():
                bstack1llll11l11ll_opy_ = bstack1llll1111ll1_opy_
            else:
                logger.warning(bstack1ll1lll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡷࡴࡻࡲࡤࡧࠣࡺࡦࡲࡵࡦࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾ࠰ࠣࡈࡪ࡬ࡡࡶ࡮ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡩࡲࡶࡴࡺࠢ࡯࡭ࡸࡺ࠮ࠣ⋭").format(bstack1llll1111ll1_opy_))
                bstack1llll11l11ll_opy_ = []
        self.__1llll11l1ll1_opy_(
            bstack1llll11l1l11_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⋮"), False),
            bstack1llll11l1l11_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡲࡵࡤࡦࠩ⋯"), bstack1ll1lll_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ⋰")),
            bstack1llll11l11ll_opy_
        )
        self.__1llll11ll1ll_opy_(opts.get(bstack1lll1lllllll_opy_, False))
        self.__1llll1l11l1l_opy_(opts.get(bstack1llll1l1llll_opy_, False))
        self.__1llll1l111ll_opy_(opts.get(bstack1lll1llll1ll_opy_, False))
    @classmethod
    def get_instance(cls, config=None):
        if cls._1ll1ll1ll11_opy_ is None and config is not None:
            cls._1ll1ll1ll11_opy_ = bstack1l11ll1ll1_opy_(config)
        return cls._1ll1ll1ll11_opy_
    @staticmethod
    def bstack1llll1lll1_opy_(config: dict) -> bool:
        bstack1llll111ll11_opy_ = config.get(bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ⋱"), {}).get(bstack1llll1l11l11_opy_, {})
        return bstack1llll111ll11_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⋲"), False)
    @staticmethod
    def bstack1ll111l1_opy_(config: dict) -> int:
        bstack1llll111ll11_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⋳"), {}).get(bstack1llll1l11l11_opy_, {})
        retries = 0
        if bstack1l11ll1ll1_opy_.bstack1llll1lll1_opy_(config):
            retries = bstack1llll111ll11_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡰࡥࡽࡘࡥࡵࡴ࡬ࡩࡸ࠭⋴"), 1)
        return retries
    @staticmethod
    def bstack1lllll11l1_opy_(config: dict) -> dict:
        bstack1llll1l1l111_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ⋵"), {})
        return {
            key: value for key, value in bstack1llll1l1l111_opy_.items() if key in bstack1llll111ll1l_opy_
        }
    @staticmethod
    def bstack1llll1ll1111_opy_():
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⋶")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠧࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡿࢂࠨ⋷").format(os.getenv(bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⋸")))))
    @staticmethod
    def bstack1llll1ll11l1_opy_(test_name: str):
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⋹")
        bstack1llll1l11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡼࡿ࠱ࡸࡽࡺࠢ⋺").format(os.getenv(bstack1ll1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⋻"))))
        with open(bstack1llll1l11lll_opy_, bstack1ll1lll_opy_ (u"ࠪࡥࠬ⋼")) as file:
            file.write(bstack1ll1lll_opy_ (u"ࠦࢀࢃ࡜࡯ࠤ⋽").format(test_name))
    @staticmethod
    def bstack1llll1l11ll1_opy_(framework: str) -> bool:
       return framework.lower() in bstack1llll1l1ll1l_opy_
    @staticmethod
    def bstack1111ll1llll_opy_(config: dict) -> bool:
        bstack1llll1111111_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⋾"), {}).get(bstack1llll11ll111_opy_, {})
        return bstack1llll1111111_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⋿"), False)
    @staticmethod
    def bstack1111llllll1_opy_(config: dict, bstack111l11111l1_opy_: int = 0) -> int:
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥ࠮ࠣࡻ࡭࡯ࡣࡩࠢࡦࡥࡳࠦࡢࡦࠢࡤࡲࠥࡧࡢࡴࡱ࡯ࡹࡹ࡫ࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡴࠣࡥࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧࠡࠪࡧ࡭ࡨࡺࠩ࠻ࠢࡗ࡬ࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡳࡹࡧ࡬ࡠࡶࡨࡷࡹࡹࠠࠩ࡫ࡱࡸ࠮ࡀࠠࡕࡪࡨࠤࡹࡵࡴࡢ࡮ࠣࡲࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥ࠮ࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠮࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸ࠿ࠦࡔࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⌀")
        bstack1llll1111111_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⌁"), {}).get(bstack1ll1lll_opy_ (u"ࠩࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠨ⌂"), {})
        bstack1llll111l1l1_opy_ = 0
        bstack1llll111lll1_opy_ = 0
        if bstack1l11ll1ll1_opy_.bstack1111ll1llll_opy_(config):
            bstack1llll111lll1_opy_ = bstack1llll1111111_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡱࡦࡾࡆࡢ࡫࡯ࡹࡷ࡫ࡳࠨ⌃"), 5)
            if isinstance(bstack1llll111lll1_opy_, str) and bstack1llll111lll1_opy_.endswith(bstack1ll1lll_opy_ (u"ࠫࠪ࠭⌄")):
                try:
                    percentage = int(bstack1llll111lll1_opy_.strip(bstack1ll1lll_opy_ (u"ࠬࠫࠧ⌅")))
                    if bstack111l11111l1_opy_ > 0:
                        bstack1llll111l1l1_opy_ = math.ceil((percentage * bstack111l11111l1_opy_) / 100)
                    else:
                        raise ValueError(bstack1ll1lll_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡲࡻࡳࡵࠢࡥࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠲ࠧ⌆"))
                except ValueError as e:
                    raise ValueError(bstack1ll1lll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡵࡲࠡ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸࡀࠠࡼࡿࠥ⌇").format(bstack1llll111lll1_opy_)) from e
            else:
                bstack1llll111l1l1_opy_ = int(bstack1llll111lll1_opy_)
        logger.info(bstack1ll1lll_opy_ (u"ࠣࡏࡤࡼࠥ࡬ࡡࡪ࡮ࡸࡶࡪࡹࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡷࡪࡺࠠࡵࡱ࠽ࠤࢀࢃࠠࠩࡨࡵࡳࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿࠬࠦ⌈").format(bstack1llll111l1l1_opy_, bstack1llll111lll1_opy_))
        return bstack1llll111l1l1_opy_
    def bstack1llll1l1ll11_opy_(self):
        return self.bstack1llll1111l1l_opy_
    def bstack1llll1l1l1l1_opy_(self):
        return self.bstack1llll11111l1_opy_
    def bstack1llll11l1lll_opy_(self):
        return self.bstack1llll11llll1_opy_
    def __1llll11l1ll1_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1llll1111l1l_opy_ = bool(enabled)
            if mode not in [bstack1ll1lll_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡊ࡮ࡸࡳࡵࠩ⌉"), bstack1ll1lll_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡔࡴ࡬ࡺࠩ⌊")]:
                logger.warning(bstack1ll1lll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠ࡮ࡱࡧࡩࠥ࠭ࡻࡾࠩࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡈ࡬ࡶࡸࡺࠧ࠯ࠤ⌋").format(mode))
                mode = bstack1ll1lll_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ⌌")
            self.bstack1llll11111l1_opy_ = mode
            self.bstack1llll11llll1_opy_ = []
            if source is None:
                self.bstack1llll11llll1_opy_ = None
            elif isinstance(source, list):
                self.bstack1llll11llll1_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1ll1lll_opy_ (u"࠭࠮࡫ࡵࡲࡲࠬ⌍")):
                self.bstack1llll11llll1_opy_ = self._1llll111l111_opy_(source)
            self.__1llll111111l_opy_()
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢ࠰ࠤࡪࡴࡡࡣ࡮ࡨࡨ࠿ࠦࡻࡾ࠮ࠣࡱࡴࡪࡥ࠻ࠢࡾࢁ࠱ࠦࡳࡰࡷࡵࡧࡪࡀࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ⌎").format(enabled, mode, source, e))
    def bstack1llll1111lll_opy_(self):
        return self.bstack1llll11111ll_opy_
    def __1llll11ll1ll_opy_(self, value):
        self.bstack1llll11111ll_opy_ = bool(value)
        self.__1llll111111l_opy_()
    def bstack1lll1lllll1l_opy_(self):
        return self.bstack1llll1l1111l_opy_
    def __1llll1l11l1l_opy_(self, value):
        self.bstack1llll1l1111l_opy_ = bool(value)
        self.__1llll111111l_opy_()
    def bstack1llll11l1l1l_opy_(self):
        return self.bstack1llll111l1ll_opy_
    def __1llll1l111ll_opy_(self, value):
        self.bstack1llll111l1ll_opy_ = bool(value)
        self.__1llll111111l_opy_()
    def __1llll111111l_opy_(self):
        if self.bstack1llll1111l1l_opy_:
            self.bstack1llll11111ll_opy_ = False
            self.bstack1llll1l1111l_opy_ = False
            self.bstack1llll111l1ll_opy_ = False
            self.bstack1llll1l1l11l_opy_.enable(bstack1llll1l1lll1_opy_)
        elif self.bstack1llll11111ll_opy_:
            self.bstack1llll1l1111l_opy_ = False
            self.bstack1llll111l1ll_opy_ = False
            self.bstack1llll1111l1l_opy_ = False
            self.bstack1llll1l1l11l_opy_.enable(bstack1lll1lllllll_opy_)
        elif self.bstack1llll1l1111l_opy_:
            self.bstack1llll11111ll_opy_ = False
            self.bstack1llll111l1ll_opy_ = False
            self.bstack1llll1111l1l_opy_ = False
            self.bstack1llll1l1l11l_opy_.enable(bstack1llll1l1llll_opy_)
        elif self.bstack1llll111l1ll_opy_:
            self.bstack1llll11111ll_opy_ = False
            self.bstack1llll1l1111l_opy_ = False
            self.bstack1llll1111l1l_opy_ = False
            self.bstack1llll1l1l11l_opy_.enable(bstack1lll1llll1ll_opy_)
        else:
            self.bstack1llll1l1l11l_opy_.disable()
    def bstack1l11lll11_opy_(self):
        return self.bstack1llll1l1l11l_opy_.bstack1llll1111l11_opy_()
    def bstack1111llll_opy_(self):
        if self.bstack1llll1l1l11l_opy_.bstack1llll1111l11_opy_():
            return self.bstack1llll1l1l11l_opy_.get_name()
        return None
    def _1llll111l111_opy_(self, bstack1llll11l111l_opy_):
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡶࡳࡺࡸࡣࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠠࡢࡰࡧࠤ࡫ࡵࡲ࡮ࡣࡷࠤ࡮ࡺࠠࡧࡱࡵࠤࡸࡳࡡࡳࡶࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡹ࡯ࡶࡴࡦࡩࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠡࠪࡶࡸࡷ࠯࠺ࠡࡒࡤࡸ࡭ࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡔࡑࡑࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡰ࡮ࡹࡴ࠻ࠢࡉࡳࡷࡳࡡࡵࡶࡨࡨࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡲࡦࡲࡲࡷ࡮ࡺ࡯ࡳࡻࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⌏")
        if not os.path.isfile(bstack1llll11l111l_opy_):
            logger.error(bstack1ll1lll_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࠨࡽࢀࠫࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠢ⌐").format(bstack1llll11l111l_opy_))
            return []
        data = None
        try:
            with open(bstack1llll11l111l_opy_, bstack1ll1lll_opy_ (u"ࠥࡶࠧ⌑")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤࡏ࡙ࡏࡏࠢࡩࡶࡴࡳࠠࡴࡱࡸࡶࡨ࡫ࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ⌒").format(bstack1llll11l111l_opy_, e))
            return []
        _1lll1lllll11_opy_ = None
        _1llll11ll11l_opy_ = None
        def _1llll11lll11_opy_():
            bstack1lll1llll1l1_opy_ = {}
            bstack1llll11lllll_opy_ = {}
            try:
                if self.bstack1llll111l11l_opy_.startswith(bstack1ll1lll_opy_ (u"ࠬࢁࠧ⌓")) and self.bstack1llll111l11l_opy_.endswith(bstack1ll1lll_opy_ (u"࠭ࡽࠨ⌔")):
                    bstack1lll1llll1l1_opy_ = json.loads(self.bstack1llll111l11l_opy_)
                else:
                    bstack1lll1llll1l1_opy_ = dict(item.split(bstack1ll1lll_opy_ (u"ࠧ࠻ࠩ⌕")) for item in self.bstack1llll111l11l_opy_.split(bstack1ll1lll_opy_ (u"ࠨ࠮ࠪ⌖")) if bstack1ll1lll_opy_ (u"ࠩ࠽ࠫ⌗") in item) if self.bstack1llll111l11l_opy_ else {}
                if self.bstack1llll1l11111_opy_.startswith(bstack1ll1lll_opy_ (u"ࠪࡿࠬ⌘")) and self.bstack1llll1l11111_opy_.endswith(bstack1ll1lll_opy_ (u"ࠫࢂ࠭⌙")):
                    bstack1llll11lllll_opy_ = json.loads(self.bstack1llll1l11111_opy_)
                else:
                    bstack1llll11lllll_opy_ = dict(item.split(bstack1ll1lll_opy_ (u"ࠬࡀࠧ⌚")) for item in self.bstack1llll1l11111_opy_.split(bstack1ll1lll_opy_ (u"࠭ࠬࠨ⌛")) if bstack1ll1lll_opy_ (u"ࠧ࠻ࠩ⌜") in item) if self.bstack1llll1l11111_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡨࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡰࡥࡵࡶࡩ࡯ࡩࡶ࠾ࠥࢁࡽࠣ⌝").format(e))
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡱࡦࡶࡰࡪࡰࡪࡷࠥ࡬ࡲࡰ࡯ࠣࡩࡳࡼ࠺ࠡࡽࢀ࠰ࠥࡉࡌࡊ࠼ࠣࡿࢂࠨ⌞").format(bstack1lll1llll1l1_opy_, bstack1llll11lllll_opy_))
            return bstack1lll1llll1l1_opy_, bstack1llll11lllll_opy_
        if _1lll1lllll11_opy_ is None or _1llll11ll11l_opy_ is None:
            _1lll1lllll11_opy_, _1llll11ll11l_opy_ = _1llll11lll11_opy_()
        def bstack1llll1ll111l_opy_(name, bstack1llll11lll1l_opy_):
            if name in _1llll11ll11l_opy_:
                return _1llll11ll11l_opy_[name]
            if name in _1lll1lllll11_opy_:
                return _1lll1lllll11_opy_[name]
            if bstack1llll11lll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ⌟")):
                return bstack1llll11lll1l_opy_[bstack1ll1lll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ⌠")]
            return None
        if isinstance(data, dict):
            bstack1llll11l1111_opy_ = []
            bstack1llll1l1l1ll_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡷ࠭࡞࡜ࡃ࠰࡞࠵࠳࠹ࡠ࡟࠮ࠨࠬ⌡"))
            for name, bstack1llll11lll1l_opy_ in data.items():
                if not isinstance(bstack1llll11lll1l_opy_, dict):
                    continue
                url = bstack1llll11lll1l_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡵࡳ࡮ࠪ⌢"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1ll1lll_opy_ (u"ࠧࠨ⌣")):
                    logger.warning(bstack1ll1lll_opy_ (u"ࠣࡔࡨࡴࡴࡹࡩࡵࡱࡵࡽ࡛ࠥࡒࡍࠢ࡬ࡷࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ⌤").format(name, bstack1llll11lll1l_opy_))
                    continue
                if not bstack1llll1l1l1ll_opy_.match(name):
                    logger.warning(bstack1ll1lll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡷࡴࡻࡲࡤࡧࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࡧࡱࡵࡱࡦࡺࠠࡧࡱࡵࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ⌥").format(name, bstack1llll11lll1l_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1ll1lll_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࠨࡽࢀࠫࠥࡳࡵࡴࡶࠣ࡬ࡦࡼࡥࠡࡣࠣࡰࡪࡴࡧࡵࡪࠣࡦࡪࡺࡷࡦࡧࡱࠤ࠶ࠦࡡ࡯ࡦࠣ࠷࠵ࠦࡣࡩࡣࡵࡥࡨࡺࡥࡳࡵ࠱ࠦ⌦").format(name))
                    continue
                bstack1llll11lll1l_opy_ = bstack1llll11lll1l_opy_.copy()
                bstack1llll11lll1l_opy_[bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⌧")] = name
                bstack1llll11lll1l_opy_[bstack1ll1lll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ⌨")] = bstack1llll1ll111l_opy_(name, bstack1llll11lll1l_opy_)
                if not bstack1llll11lll1l_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭〈")) or bstack1llll11lll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧ〉")) == bstack1ll1lll_opy_ (u"ࠨࠩ⌫"):
                    logger.warning(bstack1ll1lll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡲࡴࡺࠠࡴࡲࡨࡧ࡮࡬ࡩࡦࡦࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ⌬").format(name, bstack1llll11lll1l_opy_))
                    continue
                if bstack1llll11lll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡦࡦࡹࡥࡃࡴࡤࡲࡨ࡮ࠧ⌭")) and bstack1llll11lll1l_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡧࡳࡦࡄࡵࡥࡳࡩࡨࠨ⌮")] == bstack1llll11lll1l_opy_[bstack1ll1lll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ⌯")]:
                    logger.warning(bstack1ll1lll_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡢࡰࡧࠤࡧࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡺࡨࡦࠢࡶࡥࡲ࡫ࠠࡧࡱࡵࠤࡸࡵࡵࡳࡥࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ⌰").format(name, bstack1llll11lll1l_opy_))
                    continue
                bstack1llll11l1111_opy_.append(bstack1llll11lll1l_opy_)
            return bstack1llll11l1111_opy_
        return data
    def bstack1llll1lll11l_opy_(self):
        data = {
            bstack1ll1lll_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭⌱"): {
                bstack1ll1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⌲"): self.bstack1llll1l1ll11_opy_(),
                bstack1ll1lll_opy_ (u"ࠩࡰࡳࡩ࡫ࠧ⌳"): self.bstack1llll1l1l1l1_opy_(),
                bstack1ll1lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ⌴"): self.bstack1llll11l1lll_opy_()
            }
        }
        return data
    def bstack1llll11ll1l1_opy_(self, config):
        bstack1llll1l111l1_opy_ = {}
        bstack1llll1l111l1_opy_[bstack1ll1lll_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪ⌵")] = {
            bstack1ll1lll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⌶"): self.bstack1llll1l1ll11_opy_(),
            bstack1ll1lll_opy_ (u"࠭࡭ࡰࡦࡨࠫ⌷"): self.bstack1llll1l1l1l1_opy_()
        }
        bstack1llll1l111l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࠪ⌸")] = {
            bstack1ll1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⌹"): self.bstack1lll1lllll1l_opy_()
        }
        bstack1llll1l111l1_opy_[bstack1ll1lll_opy_ (u"ࠩࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࡢࡪ࡮ࡸࡳࡵࠩ⌺")] = {
            bstack1ll1lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⌻"): self.bstack1llll1111lll_opy_()
        }
        bstack1llll1l111l1_opy_[bstack1ll1lll_opy_ (u"ࠫࡸࡱࡩࡱࡡࡩࡥ࡮ࡲࡩ࡯ࡩࡢࡥࡳࡪ࡟ࡧ࡮ࡤ࡯ࡾ࠭⌼")] = {
            bstack1ll1lll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⌽"): self.bstack1llll11l1l1l_opy_()
        }
        if self.bstack1llll1lll1_opy_(config):
            bstack1llll1l111l1_opy_[bstack1ll1lll_opy_ (u"࠭ࡲࡦࡶࡵࡽࡤࡺࡥࡴࡶࡶࡣࡴࡴ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠨ⌾")] = {
                bstack1ll1lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⌿"): True,
                bstack1ll1lll_opy_ (u"ࠨ࡯ࡤࡼࡤࡸࡥࡵࡴ࡬ࡩࡸ࠭⍀"): self.bstack1ll111l1_opy_(config)
            }
        if self.bstack1111ll1llll_opy_(config):
            bstack1llll1l111l1_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡦࡴࡸࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡰࡰࡢࡪࡦ࡯࡬ࡶࡴࡨࠫ⍁")] = {
                bstack1ll1lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⍂"): True,
                bstack1ll1lll_opy_ (u"ࠫࡲࡧࡸࡠࡨࡤ࡭ࡱࡻࡲࡦࡵࠪ⍃"): self.bstack1111llllll1_opy_(config)
            }
        return bstack1llll1l111l1_opy_
    def bstack111llll1_opy_(self, config):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡳࡱࡲࡥࡤࡶࡶࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡤࡼࠤࡲࡧ࡫ࡪࡰࡪࠤࡦࠦࡣࡢ࡮࡯ࠤࡹࡵࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠠࠩࡵࡷࡶ࠮ࡀࠠࡕࡪࡨࠤ࡚࡛ࡉࡅࠢࡲࡪࠥࡺࡨࡦࠢࡥࡹ࡮ࡲࡤࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠱ࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠠࡪࡨࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⍄")
        if not (config.get(bstack1ll1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⍅"), None) in bstack111l11ll1l1_opy_ and self.bstack1llll1l1ll11_opy_()):
            return None
        bstack1llll111llll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⍆"), None)
        logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡃࡰ࡮࡯ࡩࡨࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦ࡙࡚ࠣࡏࡄ࠻ࠢࡾࢁࠧ⍇").format(bstack1llll111llll_opy_))
        try:
            bstack111ll1111l1_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠢ⍈").format(bstack1llll111llll_opy_)
            payload = {
                bstack1ll1lll_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣ⍉"): config.get(bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ⍊"), bstack1ll1lll_opy_ (u"ࠬ࠭⍋")),
                bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤ⍌"): config.get(bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ⍍"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨ⍎"): os.environ.get(bstack1ll1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠣ⍏"), bstack1ll1lll_opy_ (u"ࠥࠦ⍐")),
                bstack1ll1lll_opy_ (u"ࠦࡳࡵࡤࡦࡋࡱࡨࡪࡾࠢ⍑"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣ⍒")) or bstack1ll1lll_opy_ (u"ࠨ࠰ࠣ⍓")),
                bstack1ll1lll_opy_ (u"ࠢࡵࡱࡷࡥࡱࡔ࡯ࡥࡧࡶࠦ⍔"): int(os.environ.get(bstack1ll1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡑࡗࡅࡑࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥ⍕")) or bstack1ll1lll_opy_ (u"ࠤ࠴ࠦ⍖")),
                bstack1ll1lll_opy_ (u"ࠥ࡬ࡴࡹࡴࡊࡰࡩࡳࠧ⍗"): get_host_info(),
            }
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡱࡣࡼࡰࡴࡧࡤ࠻ࠢࡾࢁࠧ⍘").format(payload))
            response = bstack111l1llll11_opy_.bstack1lll1llllll1_opy_(bstack111ll1111l1_opy_, payload)
            if response:
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡆࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⍙").format(response))
                return response
            else:
                logger.error(bstack1ll1lll_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࡀࠠࡼࡿࠥ⍚").format(bstack1llll111llll_opy_))
                return None
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࠦࡻࡾ࠼ࠣࡿࢂࠨ⍛").format(bstack1llll111llll_opy_, e))
            return None