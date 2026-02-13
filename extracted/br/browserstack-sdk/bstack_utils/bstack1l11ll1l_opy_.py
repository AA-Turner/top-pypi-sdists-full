# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack11ll111l_opy_, bstack111ll111l1l_opy_
from bstack_utils.helper import bstack1111l1ll11l_opy_, get_host_info
from bstack_utils.bstack111llllll1l_opy_ import bstack111lllll1ll_opy_
import json
import re
import sys
bstack1llllll1l11l_opy_ = bstack11l11_opy_ (u"ࠥࡶࡪࡺࡲࡺࡖࡨࡷࡹࡹࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠤₛ")
bstack1llllll11111_opy_ = bstack11l11_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡅࡹ࡮ࡲࡤࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠥₜ")
bstack1lllll111ll1_opy_ = bstack11l11_opy_ (u"ࠧࡸࡵ࡯ࡒࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡋࡧࡩ࡭ࡧࡧࡊ࡮ࡸࡳࡵࠤ₝")
bstack1lllllll1l11_opy_ = bstack11l11_opy_ (u"ࠨࡲࡦࡴࡸࡲࡕࡸࡥࡷ࡫ࡲࡹࡸࡲࡹࡇࡣ࡬ࡰࡪࡪࠢ₞")
bstack1lllll111l1l_opy_ = bstack11l11_opy_ (u"ࠢࡴ࡭࡬ࡴࡋࡲࡡ࡬ࡻࡤࡲࡩࡌࡡࡪ࡮ࡨࡨࠧ₟")
bstack1lllll1ll1ll_opy_ = bstack11l11_opy_ (u"ࠣࡴࡸࡲࡘࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠧ₠")
bstack1llllll1l1ll_opy_ = {
    bstack1llllll1l11l_opy_,
    bstack1llllll11111_opy_,
    bstack1lllll111ll1_opy_,
    bstack1lllllll1l11_opy_,
    bstack1lllll111l1l_opy_,
    bstack1lllll1ll1ll_opy_
}
bstack1llllll1lll1_opy_ = {bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ₡")}
logger = logger_utils.get_logger(__name__, bstack11ll111l_opy_)
class bstack1lllll1l11ll_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lllll1l1111_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l11l1l1ll_opy_:
    _1ll11111lll_opy_ = None
    def __init__(self, config):
        self.bstack1lllllll111l_opy_ = False
        self.bstack1lllll11ll11_opy_ = False
        self.bstack1llllll1ll11_opy_ = False
        self.bstack1lllll1l111l_opy_ = False
        self.bstack1lllll1l1l11_opy_ = None
        self.bstack1llllll111l1_opy_ = bstack1lllll1l11ll_opy_()
        self.bstack1lllll1lll1l_opy_ = None
        opts = config.get(bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ₢"), {})
        self.bstack1lllll11l1l1_opy_ = config.get(bstack11l11_opy_ (u"ࠫࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡋࡎࡗࠩ₣"), bstack11l11_opy_ (u"ࠧࠨ₤"))
        self.bstack1llllll1111l_opy_ = config.get(bstack11l11_opy_ (u"࠭ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࡄࡎࡌࠫ₥"), bstack11l11_opy_ (u"ࠢࠣ₦"))
        bstack1llll1lllll1_opy_ = opts.get(bstack1lllll1ll1ll_opy_, {})
        bstack1lllll11l111_opy_ = None
        if bstack11l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ₧") in bstack1llll1lllll1_opy_:
            bstack1llllll11ll1_opy_ = bstack1llll1lllll1_opy_[bstack11l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ₨")]
            if bstack1llllll11ll1_opy_ is None or (isinstance(bstack1llllll11ll1_opy_, str) and bstack1llllll11ll1_opy_.strip() == bstack11l11_opy_ (u"ࠪࠫ₩")) or (isinstance(bstack1llllll11ll1_opy_, list) and len(bstack1llllll11ll1_opy_) == 0):
                bstack1lllll11l111_opy_ = []
            elif isinstance(bstack1llllll11ll1_opy_, list):
                bstack1lllll11l111_opy_ = bstack1llllll11ll1_opy_
            elif isinstance(bstack1llllll11ll1_opy_, str) and bstack1llllll11ll1_opy_.strip():
                bstack1lllll11l111_opy_ = bstack1llllll11ll1_opy_
            else:
                logger.warning(bstack11l11_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡹ࡯ࡶࡴࡦࡩࠥࡼࡡ࡭ࡷࡨࠤ࡮ࡴࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡽࢀ࠲ࠥࡊࡥࡧࡣࡸࡰࡹ࡯࡮ࡨࠢࡷࡳࠥ࡫࡭ࡱࡶࡼࠤࡱ࡯ࡳࡵ࠰ࠥ₪").format(bstack1llllll11ll1_opy_))
                bstack1lllll11l111_opy_ = []
        self.__1lllll111lll_opy_(
            bstack1llll1lllll1_opy_.get(bstack11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭₫"), False),
            bstack1llll1lllll1_opy_.get(bstack11l11_opy_ (u"࠭࡭ࡰࡦࡨࠫ€"), bstack11l11_opy_ (u"ࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡈ࡬ࡶࡸࡺࠧ₭")),
            bstack1lllll11l111_opy_
        )
        self.__1llll1llll11_opy_(opts.get(bstack1lllll111ll1_opy_, False))
        self.__1lllll11lll1_opy_(opts.get(bstack1lllllll1l11_opy_, False))
        self.__1lllll1lllll_opy_(opts.get(bstack1lllll111l1l_opy_, False))
    @classmethod
    def bstack111l1lll_opy_(cls, config=None):
        if cls._1ll11111lll_opy_ is None and config is not None:
            cls._1ll11111lll_opy_ = bstack1l11l1l1ll_opy_(config)
        return cls._1ll11111lll_opy_
    @staticmethod
    def bstack11l11lll11_opy_(config: dict) -> bool:
        bstack1lllll1l1ll1_opy_ = config.get(bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ₮"), {}).get(bstack1llllll1l11l_opy_, {})
        return bstack1lllll1l1ll1_opy_.get(bstack11l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ₯"), False)
    @staticmethod
    def bstack11l1l1lll1_opy_(config: dict) -> int:
        bstack1lllll1l1ll1_opy_ = config.get(bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ₰"), {}).get(bstack1llllll1l11l_opy_, {})
        retries = 0
        if bstack1l11l1l1ll_opy_.bstack11l11lll11_opy_(config):
            retries = bstack1lllll1l1ll1_opy_.get(bstack11l11_opy_ (u"ࠫࡲࡧࡸࡓࡧࡷࡶ࡮࡫ࡳࠨ₱"), 1)
        return retries
    @staticmethod
    def bstack1llll11lll_opy_(config: dict) -> dict:
        bstack1lllll1ll111_opy_ = config.get(bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ₲"), {})
        return {
            key: value for key, value in bstack1lllll1ll111_opy_.items() if key in bstack1llllll1l1ll_opy_
        }
    @staticmethod
    def bstack1llll1llll1l_opy_():
        bstack11l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ₳")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣ₴").format(os.getenv(bstack11l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ₵")))))
    @staticmethod
    def bstack1lllll111l11_opy_(test_name: str):
        bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ₶")
        bstack1lllll1llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡾࢁ࠳ࡺࡸࡵࠤ₷").format(os.getenv(bstack11l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ₸"))))
        with open(bstack1lllll1llll1_opy_, bstack11l11_opy_ (u"ࠬࡧࠧ₹")) as file:
            file.write(bstack11l11_opy_ (u"ࠨࡻࡾ࡞ࡱࠦ₺").format(test_name))
    @staticmethod
    def bstack1lllll1ll1l1_opy_(framework: str) -> bool:
       return framework.lower() in bstack1llllll1lll1_opy_
    @staticmethod
    def bstack111l1ll11ll_opy_(config: dict) -> bool:
        bstack1llllll11lll_opy_ = config.get(bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ₻"), {}).get(bstack1llllll11111_opy_, {})
        return bstack1llllll11lll_opy_.get(bstack11l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ₼"), False)
    @staticmethod
    def bstack111l1ll111l_opy_(config: dict, bstack111l1ll11l1_opy_: int = 0) -> int:
        bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡇࡦࡶࠣࡸ࡭࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧ࠰ࠥࡽࡨࡪࡥ࡫ࠤࡨࡧ࡮ࠡࡤࡨࠤࡦࡴࠠࡢࡤࡶࡳࡱࡻࡴࡦࠢࡱࡹࡲࡨࡥࡳࠢࡲࡶࠥࡧࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡦࡪࡩࠣࠬࡩ࡯ࡣࡵࠫ࠽ࠤ࡙࡮ࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡵࡴࡢ࡮ࡢࡸࡪࡹࡴࡴࠢࠫ࡭ࡳࡺࠩ࠻ࠢࡗ࡬ࡪࠦࡴࡰࡶࡤࡰࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࠩࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡪࡴࡸࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨ࠱ࡧࡧࡳࡦࡦࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࡹࠩ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡭ࡳࡺ࠺ࠡࡖ࡫ࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ₽")
        bstack1llllll11lll_opy_ = config.get(bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ₾"), {}).get(bstack11l11_opy_ (u"ࠫࡦࡨ࡯ࡳࡶࡅࡹ࡮ࡲࡤࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠪ₿"), {})
        bstack1lllll1l1l1l_opy_ = 0
        bstack1lllll11llll_opy_ = 0
        if bstack1l11l1l1ll_opy_.bstack111l1ll11ll_opy_(config):
            bstack1lllll11llll_opy_ = bstack1llllll11lll_opy_.get(bstack11l11_opy_ (u"ࠬࡳࡡࡹࡈࡤ࡭ࡱࡻࡲࡦࡵࠪ⃀"), 5)
            if isinstance(bstack1lllll11llll_opy_, str) and bstack1lllll11llll_opy_.endswith(bstack11l11_opy_ (u"࠭ࠥࠨ⃁")):
                try:
                    percentage = int(bstack1lllll11llll_opy_.strip(bstack11l11_opy_ (u"ࠧࠦࠩ⃂")))
                    if bstack111l1ll11l1_opy_ > 0:
                        bstack1lllll1l1l1l_opy_ = math.ceil((percentage * bstack111l1ll11l1_opy_) / 100)
                    else:
                        raise ValueError(bstack11l11_opy_ (u"ࠣࡖࡲࡸࡦࡲࠠࡵࡧࡶࡸࡸࠦ࡭ࡶࡵࡷࠤࡧ࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡩࡳࡷࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠰ࡦࡦࡹࡥࡥࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࡸ࠴ࠢ⃃"))
                except ValueError as e:
                    raise ValueError(bstack11l11_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫ࠠࡷࡣ࡯ࡹࡪࠦࡦࡰࡴࠣࡱࡦࡾࡆࡢ࡫࡯ࡹࡷ࡫ࡳ࠻ࠢࡾࢁࠧ⃄").format(bstack1lllll11llll_opy_)) from e
            else:
                bstack1lllll1l1l1l_opy_ = int(bstack1lllll11llll_opy_)
        logger.info(bstack11l11_opy_ (u"ࠥࡑࡦࡾࠠࡧࡣ࡬ࡰࡺࡸࡥࡴࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡹࡥࡵࠢࡷࡳ࠿ࠦࡻࡾࠢࠫࡪࡷࡵ࡭ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡾࢁ࠮ࠨ⃅").format(bstack1lllll1l1l1l_opy_, bstack1lllll11llll_opy_))
        return bstack1lllll1l1l1l_opy_
    def bstack1lllll1111l1_opy_(self):
        return self.bstack1lllll1l111l_opy_
    def bstack1lllll11111l_opy_(self):
        return self.bstack1lllll1l1l11_opy_
    def bstack1lllll11l1ll_opy_(self):
        return self.bstack1lllll1lll1l_opy_
    def __1lllll111lll_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lllll1l111l_opy_ = bool(enabled)
            if mode not in [bstack11l11_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡌࡩࡳࡵࡷࠫ⃆"), bstack11l11_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡏ࡯࡮ࡼࠫ⃇")]:
                logger.warning(bstack11l11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡰࡳࡩ࡫ࠠࠨࡽࢀࠫࠥࡶࡲࡰࡸ࡬ࡨࡪࡪ࠮ࠡࡆࡨࡪࡦࡻ࡬ࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡊ࡮ࡸࡳࡵࠩ࠱ࠦ⃈").format(mode))
                mode = bstack11l11_opy_ (u"ࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡈ࡬ࡶࡸࡺࠧ⃉")
            self.bstack1lllll1l1l11_opy_ = mode
            self.bstack1lllll1lll1l_opy_ = []
            if source is None:
                self.bstack1lllll1lll1l_opy_ = None
            elif isinstance(source, list):
                self.bstack1lllll1lll1l_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack11l11_opy_ (u"ࠨ࠰࡭ࡷࡴࡴࠧ⃊")):
                self.bstack1lllll1lll1l_opy_ = self._1lllllll1111_opy_(source)
            self.__1lllll111111_opy_()
        except Exception as e:
            logger.error(bstack11l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡱࡦࡸࡴࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࠲ࠦࡥ࡯ࡣࡥࡰࡪࡪ࠺ࠡࡽࢀ࠰ࠥࡳ࡯ࡥࡧ࠽ࠤࢀࢃࠬࠡࡵࡲࡹࡷࡩࡥ࠻ࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ⃋").format(enabled, mode, source, e))
    def bstack1lllll1ll11l_opy_(self):
        return self.bstack1lllllll111l_opy_
    def __1llll1llll11_opy_(self, value):
        self.bstack1lllllll111l_opy_ = bool(value)
        self.__1lllll111111_opy_()
    def bstack1lllll11l11l_opy_(self):
        return self.bstack1lllll11ll11_opy_
    def __1lllll11lll1_opy_(self, value):
        self.bstack1lllll11ll11_opy_ = bool(value)
        self.__1lllll111111_opy_()
    def bstack1llllll11l11_opy_(self):
        return self.bstack1llllll1ll11_opy_
    def __1lllll1lllll_opy_(self, value):
        self.bstack1llllll1ll11_opy_ = bool(value)
        self.__1lllll111111_opy_()
    def __1lllll111111_opy_(self):
        if self.bstack1lllll1l111l_opy_:
            self.bstack1lllllll111l_opy_ = False
            self.bstack1lllll11ll11_opy_ = False
            self.bstack1llllll1ll11_opy_ = False
            self.bstack1llllll111l1_opy_.enable(bstack1lllll1ll1ll_opy_)
        elif self.bstack1lllllll111l_opy_:
            self.bstack1lllll11ll11_opy_ = False
            self.bstack1llllll1ll11_opy_ = False
            self.bstack1lllll1l111l_opy_ = False
            self.bstack1llllll111l1_opy_.enable(bstack1lllll111ll1_opy_)
        elif self.bstack1lllll11ll11_opy_:
            self.bstack1lllllll111l_opy_ = False
            self.bstack1llllll1ll11_opy_ = False
            self.bstack1lllll1l111l_opy_ = False
            self.bstack1llllll111l1_opy_.enable(bstack1lllllll1l11_opy_)
        elif self.bstack1llllll1ll11_opy_:
            self.bstack1lllllll111l_opy_ = False
            self.bstack1lllll11ll11_opy_ = False
            self.bstack1lllll1l111l_opy_ = False
            self.bstack1llllll111l1_opy_.enable(bstack1lllll111l1l_opy_)
        else:
            self.bstack1llllll111l1_opy_.disable()
    def bstack1l11lllll_opy_(self):
        return self.bstack1llllll111l1_opy_.bstack1lllll1l1111_opy_()
    def bstack11llllll1_opy_(self):
        if self.bstack1llllll111l1_opy_.bstack1lllll1l1111_opy_():
            return self.bstack1llllll111l1_opy_.get_name()
        return None
    def _1lllllll1111_opy_(self, bstack1llllll1llll_opy_):
        bstack11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡸࡵࡵࡳࡥࡨࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢࡤࡲࡩࠦࡦࡰࡴࡰࡥࡹࠦࡩࡵࠢࡩࡳࡷࠦࡳ࡮ࡣࡵࡸࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡴࡱࡸࡶࡨ࡫࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠣࠬࡸࡺࡲࠪ࠼ࠣࡔࡦࡺࡨࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡖࡓࡓࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡲࡩࡴࡶ࠽ࠤࡋࡵࡲ࡮ࡣࡷࡸࡪࡪࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡴࡨࡴࡴࡹࡩࡵࡱࡵࡽࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⃌")
        if not os.path.isfile(bstack1llllll1llll_opy_):
            logger.error(bstack11l11_opy_ (u"ࠦࡘࡵࡵࡳࡥࡨࠤ࡫࡯࡬ࡦࠢࠪࡿࢂ࠭ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠯ࠤ⃍").format(bstack1llllll1llll_opy_))
            return []
        data = None
        try:
            with open(bstack1llllll1llll_opy_, bstack11l11_opy_ (u"ࠧࡸࠢ⃎")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡊࡔࡑࡑࠤ࡫ࡸ࡯࡮ࠢࡶࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ⃏").format(bstack1llllll1llll_opy_, e))
            return []
        _1lllllll11l1_opy_ = None
        _1llllll1l111_opy_ = None
        def _1lllll1l1lll_opy_():
            bstack1lllll1lll11_opy_ = {}
            bstack1lllllll11ll_opy_ = {}
            try:
                if self.bstack1lllll11l1l1_opy_.startswith(bstack11l11_opy_ (u"ࠧࡼࠩ⃐")) and self.bstack1lllll11l1l1_opy_.endswith(bstack11l11_opy_ (u"ࠨࡿࠪ⃑")):
                    bstack1lllll1lll11_opy_ = json.loads(self.bstack1lllll11l1l1_opy_)
                else:
                    bstack1lllll1lll11_opy_ = dict(item.split(bstack11l11_opy_ (u"ࠩ࠽⃒ࠫ")) for item in self.bstack1lllll11l1l1_opy_.split(bstack11l11_opy_ (u"ࠪ࠰⃓ࠬ")) if bstack11l11_opy_ (u"ࠫ࠿࠭⃔") in item) if self.bstack1lllll11l1l1_opy_ else {}
                if self.bstack1llllll1111l_opy_.startswith(bstack11l11_opy_ (u"ࠬࢁࠧ⃕")) and self.bstack1llllll1111l_opy_.endswith(bstack11l11_opy_ (u"࠭ࡽࠨ⃖")):
                    bstack1lllllll11ll_opy_ = json.loads(self.bstack1llllll1111l_opy_)
                else:
                    bstack1lllllll11ll_opy_ = dict(item.split(bstack11l11_opy_ (u"ࠧ࠻ࠩ⃗")) for item in self.bstack1llllll1111l_opy_.split(bstack11l11_opy_ (u"ࠨ࠮⃘ࠪ")) if bstack11l11_opy_ (u"ࠩ࠽⃙ࠫ") in item) if self.bstack1llllll1111l_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡪࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࡀࠠࡼࡿ⃚ࠥ").format(e))
            logger.debug(bstack11l11_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡳࡡࡱࡲ࡬ࡲ࡬ࡹࠠࡧࡴࡲࡱࠥ࡫࡮ࡷ࠼ࠣࡿࢂ࠲ࠠࡄࡎࡌ࠾ࠥࢁࡽࠣ⃛").format(bstack1lllll1lll11_opy_, bstack1lllllll11ll_opy_))
            return bstack1lllll1lll11_opy_, bstack1lllllll11ll_opy_
        if _1lllllll11l1_opy_ is None or _1llllll1l111_opy_ is None:
            _1lllllll11l1_opy_, _1llllll1l111_opy_ = _1lllll1l1lll_opy_()
        def bstack1llllll1ll1l_opy_(name, bstack1llll1llllll_opy_):
            if name in _1llllll1l111_opy_:
                return _1llllll1l111_opy_[name]
            if name in _1lllllll11l1_opy_:
                return _1lllllll11l1_opy_[name]
            if bstack1llll1llllll_opy_.get(bstack11l11_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ⃜")):
                return bstack1llll1llllll_opy_[bstack11l11_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭⃝")]
            return None
        if isinstance(data, dict):
            bstack1llllll11l1l_opy_ = []
            bstack1llllll1l1l1_opy_ = re.compile(bstack11l11_opy_ (u"ࡲࠨࡠ࡞ࡅ࠲ࡠ࠰࠮࠻ࡢࡡ࠰ࠪࠧ⃞"))
            for name, bstack1llll1llllll_opy_ in data.items():
                if not isinstance(bstack1llll1llllll_opy_, dict):
                    continue
                url = bstack1llll1llllll_opy_.get(bstack11l11_opy_ (u"ࠨࡷࡵࡰࠬ⃟"))
                if url is None or (isinstance(url, str) and url.strip() == bstack11l11_opy_ (u"ࠩࠪ⃠")):
                    logger.warning(bstack11l11_opy_ (u"ࠥࡖࡪࡶ࡯ࡴ࡫ࡷࡳࡷࡿࠠࡖࡔࡏࠤ࡮ࡹࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡹ࡯ࡶࡴࡦࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ⃡").format(name, bstack1llll1llllll_opy_))
                    continue
                if not bstack1llllll1l1l1_opy_.match(name):
                    logger.warning(bstack11l11_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡹ࡯ࡶࡴࡦࡩࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠢࡩࡳࡷࡳࡡࡵࠢࡩࡳࡷࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ⃢").format(name, bstack1llll1llllll_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack11l11_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠢࠪࡿࢂ࠭ࠠ࡮ࡷࡶࡸࠥ࡮ࡡࡷࡧࠣࡥࠥࡲࡥ࡯ࡩࡷ࡬ࠥࡨࡥࡵࡹࡨࡩࡳࠦ࠱ࠡࡣࡱࡨࠥ࠹࠰ࠡࡥ࡫ࡥࡷࡧࡣࡵࡧࡵࡷ࠳ࠨ⃣").format(name))
                    continue
                bstack1llll1llllll_opy_ = bstack1llll1llllll_opy_.copy()
                bstack1llll1llllll_opy_[bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⃤")] = name
                bstack1llll1llllll_opy_[bstack11l11_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮⃥ࠧ")] = bstack1llllll1ll1l_opy_(name, bstack1llll1llllll_opy_)
                if not bstack1llll1llllll_opy_.get(bstack11l11_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ⃦")) or bstack1llll1llllll_opy_.get(bstack11l11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ⃧")) == bstack11l11_opy_ (u"⃨ࠪࠫ"):
                    logger.warning(bstack11l11_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡴ࡯ࡵࠢࡶࡴࡪࡩࡩࡧ࡫ࡨࡨࠥ࡬࡯ࡳࠢࡶࡳࡺࡸࡣࡦࠢࠪࡿࢂ࠭࠺ࠡࡽࢀࠦ⃩").format(name, bstack1llll1llllll_opy_))
                    continue
                if bstack1llll1llllll_opy_.get(bstack11l11_opy_ (u"ࠬࡨࡡࡴࡧࡅࡶࡦࡴࡣࡩ⃪ࠩ")) and bstack1llll1llllll_opy_[bstack11l11_opy_ (u"࠭ࡢࡢࡵࡨࡆࡷࡧ࡮ࡤࡪ⃫ࠪ")] == bstack1llll1llllll_opy_[bstack11l11_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮⃬ࠧ")]:
                    logger.warning(bstack11l11_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡤࡲࡩࠦࡢࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡨࡧ࡮࡯ࡱࡷࠤࡧ࡫ࠠࡵࡪࡨࠤࡸࡧ࡭ࡦࠢࡩࡳࡷࠦࡳࡰࡷࡵࡧࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽ⃭ࠣ").format(name, bstack1llll1llllll_opy_))
                    continue
                bstack1llllll11l1l_opy_.append(bstack1llll1llllll_opy_)
            return bstack1llllll11l1l_opy_
        return data
    def bstack1lllllllll11_opy_(self):
        data = {
            bstack11l11_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨ⃮"): {
                bstack11l11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧ⃯ࠫ"): self.bstack1lllll1111l1_opy_(),
                bstack11l11_opy_ (u"ࠫࡲࡵࡤࡦࠩ⃰"): self.bstack1lllll11111l_opy_(),
                bstack11l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ⃱"): self.bstack1lllll11l1ll_opy_()
            }
        }
        return data
    def bstack1llllll111ll_opy_(self, config):
        bstack1lllll1111ll_opy_ = {}
        bstack1lllll1111ll_opy_[bstack11l11_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ⃲")] = {
            bstack11l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⃳"): self.bstack1lllll1111l1_opy_(),
            bstack11l11_opy_ (u"ࠨ࡯ࡲࡨࡪ࠭⃴"): self.bstack1lllll11111l_opy_()
        }
        bstack1lllll1111ll_opy_[bstack11l11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡲࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡤ࡬ࡡࡪ࡮ࡨࡨࠬ⃵")] = {
            bstack11l11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⃶"): self.bstack1lllll11l11l_opy_()
        }
        bstack1lllll1111ll_opy_[bstack11l11_opy_ (u"ࠫࡷࡻ࡮ࡠࡲࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡤ࡬ࡡࡪ࡮ࡨࡨࡤ࡬ࡩࡳࡵࡷࠫ⃷")] = {
            bstack11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⃸"): self.bstack1lllll1ll11l_opy_()
        }
        bstack1lllll1111ll_opy_[bstack11l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡣ࡫ࡧࡩ࡭࡫ࡱ࡫ࡤࡧ࡮ࡥࡡࡩࡰࡦࡱࡹࠨ⃹")] = {
            bstack11l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⃺"): self.bstack1llllll11l11_opy_()
        }
        if self.bstack11l11lll11_opy_(config):
            bstack1lllll1111ll_opy_[bstack11l11_opy_ (u"ࠨࡴࡨࡸࡷࡿ࡟ࡵࡧࡶࡸࡸࡥ࡯࡯ࡡࡩࡥ࡮ࡲࡵࡳࡧࠪ⃻")] = {
                bstack11l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ⃼"): True,
                bstack11l11_opy_ (u"ࠪࡱࡦࡾ࡟ࡳࡧࡷࡶ࡮࡫ࡳࠨ⃽"): self.bstack11l1l1lll1_opy_(config)
            }
        if self.bstack111l1ll11ll_opy_(config):
            bstack1lllll1111ll_opy_[bstack11l11_opy_ (u"ࠫࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡲࡲࡤ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⃾")] = {
                bstack11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⃿"): True,
                bstack11l11_opy_ (u"࠭࡭ࡢࡺࡢࡪࡦ࡯࡬ࡶࡴࡨࡷࠬ℀"): self.bstack111l1ll111l_opy_(config)
            }
        return bstack1lllll1111ll_opy_
    def bstack11l1ll111_opy_(self, config):
        bstack11l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡵ࡬࡭ࡧࡦࡸࡸࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡦࡾࠦ࡭ࡢ࡭࡬ࡲ࡬ࠦࡡࠡࡥࡤࡰࡱࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠢࠫࡷࡹࡸࠩ࠻ࠢࡗ࡬ࡪࠦࡕࡖࡋࡇࠤࡴ࡬ࠠࡵࡪࡨࠤࡧࡻࡩ࡭ࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠬࠡࡱࡵࠤࡓࡵ࡮ࡦࠢ࡬ࡪࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ℁")
        if not (config.get(bstack11l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫℂ"), None) in bstack111ll111l1l_opy_ and self.bstack1lllll1111l1_opy_()):
            return None
        bstack1lllll11ll1l_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ℃"), None)
        logger.debug(bstack11l11_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡢࡶ࡫࡯ࡨ࡛ࠥࡕࡊࡆ࠽ࠤࢀࢃࠢ℄").format(bstack1lllll11ll1l_opy_))
        try:
            bstack11l111111ll_opy_ = bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠤ℅").format(bstack1lllll11ll1l_opy_)
            payload = {
                bstack11l11_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥ℆"): config.get(bstack11l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫℇ"), bstack11l11_opy_ (u"ࠧࠨ℈")),
                bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦ℉"): config.get(bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬℊ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣℋ"): os.environ.get(bstack11l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥℌ"), bstack11l11_opy_ (u"ࠧࠨℍ")),
                bstack11l11_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤℎ"): int(os.environ.get(bstack11l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥℏ")) or bstack11l11_opy_ (u"ࠣ࠲ࠥℐ")),
                bstack11l11_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨℑ"): int(os.environ.get(bstack11l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧℒ")) or bstack11l11_opy_ (u"ࠦ࠶ࠨℓ")),
                bstack11l11_opy_ (u"ࠧ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠢ℔"): get_host_info(),
            }
            logger.debug(bstack11l11_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡳࡥࡾࡲ࡯ࡢࡦ࠽ࠤࢀࢃࠢℕ").format(payload))
            response = bstack111lllll1ll_opy_.bstack1lllll1l11l1_opy_(bstack11l111111ll_opy_, payload)
            if response:
                logger.debug(bstack11l11_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡈࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ№").format(response))
                return response
            else:
                logger.error(bstack11l11_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦ࡙࡚ࠣࡏࡄ࠻ࠢࡾࢁࠧ℗").format(bstack1lllll11ll1l_opy_))
                return None
        except Exception as e:
            logger.error(bstack11l11_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡰ࡮࡯ࡩࡨࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦ࡙࡚ࠣࡏࡄࠡࡽࢀ࠾ࠥࢁࡽࠣ℘").format(bstack1lllll11ll1l_opy_, e))
            return None