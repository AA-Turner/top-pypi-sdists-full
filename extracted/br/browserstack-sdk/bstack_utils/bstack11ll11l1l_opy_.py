# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack1llllll1l_opy_, bstack111ll1ll1l1_opy_
from bstack_utils.helper import bstack111l111111l_opy_, get_host_info
from bstack_utils.bstack11l1111ll1l_opy_ import bstack11l1111l1ll_opy_
import json
import re
import sys
bstack1lllll1l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠢࡳࡧࡷࡶࡾ࡚ࡥࡴࡶࡶࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨ₦")
bstack1lllll11ll1l_opy_ = bstack11l1l11_opy_ (u"ࠣࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢ₧")
bstack1lllllllll11_opy_ = bstack11l1l11_opy_ (u"ࠤࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࡇ࡫ࡵࡷࡹࠨ₨")
bstack1llllllllll1_opy_ = bstack11l1l11_opy_ (u"ࠥࡶࡪࡸࡵ࡯ࡒࡵࡩࡻ࡯࡯ࡶࡵ࡯ࡽࡋࡧࡩ࡭ࡧࡧࠦ₩")
bstack1lllll1ll1l1_opy_ = bstack11l1l11_opy_ (u"ࠦࡸࡱࡩࡱࡈ࡯ࡥࡰࡿࡡ࡯ࡦࡉࡥ࡮ࡲࡥࡥࠤ₪")
bstack1llllll1llll_opy_ = bstack11l1l11_opy_ (u"ࠧࡸࡵ࡯ࡕࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠤ₫")
bstack1111111111l_opy_ = {
    bstack1lllll1l1ll1_opy_,
    bstack1lllll11ll1l_opy_,
    bstack1lllllllll11_opy_,
    bstack1llllllllll1_opy_,
    bstack1lllll1ll1l1_opy_,
    bstack1llllll1llll_opy_
}
bstack1lllll1l11l1_opy_ = {bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭€")}
logger = logger_utils.get_logger(__name__, bstack1llllll1l_opy_)
class bstack1lllllll11l1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lllllll1ll1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l1l11l11l_opy_:
    _1ll1l11l111_opy_ = None
    def __init__(self, config):
        self.bstack1lllll1lllll_opy_ = False
        self.bstack1lllllllll1l_opy_ = False
        self.bstack111111111l1_opy_ = False
        self.bstack1llllll11l11_opy_ = False
        self.bstack1lllllll11ll_opy_ = None
        self.bstack1llllll11lll_opy_ = bstack1lllllll11l1_opy_()
        self.bstack1lllll1l1l11_opy_ = None
        opts = config.get(bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ₭"), {})
        self.bstack1lllllll1l11_opy_ = config.get(bstack11l1l11_opy_ (u"ࠨࡵࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࡈࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࡦࡵࡈࡒ࡛࠭₮"), bstack11l1l11_opy_ (u"ࠤࠥ₯"))
        self.bstack1lllll1l1111_opy_ = config.get(bstack11l1l11_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡈࡒࡉࠨ₰"), bstack11l1l11_opy_ (u"ࠦࠧ₱"))
        bstack1lllllllllll_opy_ = opts.get(bstack1llllll1llll_opy_, {})
        bstack1lllll1lll1l_opy_ = None
        if bstack11l1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ₲") in bstack1lllllllllll_opy_:
            bstack1llllll1ll11_opy_ = bstack1lllllllllll_opy_[bstack11l1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭₳")]
            if bstack1llllll1ll11_opy_ is None or (isinstance(bstack1llllll1ll11_opy_, str) and bstack1llllll1ll11_opy_.strip() == bstack11l1l11_opy_ (u"ࠧࠨ₴")) or (isinstance(bstack1llllll1ll11_opy_, list) and len(bstack1llllll1ll11_opy_) == 0):
                bstack1lllll1lll1l_opy_ = []
            elif isinstance(bstack1llllll1ll11_opy_, list):
                bstack1lllll1lll1l_opy_ = bstack1llllll1ll11_opy_
            elif isinstance(bstack1llllll1ll11_opy_, str) and bstack1llllll1ll11_opy_.strip():
                bstack1lllll1lll1l_opy_ = bstack1llllll1ll11_opy_
            else:
                logger.warning(bstack11l1l11_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡶࡳࡺࡸࡣࡦࠢࡹࡥࡱࡻࡥࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽ࠯ࠢࡇࡩ࡫ࡧࡵ࡭ࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡨࡱࡵࡺࡹࠡ࡮࡬ࡷࡹ࠴ࠢ₵").format(bstack1llllll1ll11_opy_))
                bstack1lllll1lll1l_opy_ = []
        self.__11111111l1l_opy_(
            bstack1lllllllllll_opy_.get(bstack11l1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ₶"), False),
            bstack1lllllllllll_opy_.get(bstack11l1l11_opy_ (u"ࠪࡱࡴࡪࡥࠨ₷"), bstack11l1l11_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡌࡩࡳࡵࡷࠫ₸")),
            bstack1lllll1lll1l_opy_
        )
        self.__1lllll1ll1ll_opy_(opts.get(bstack1lllllllll11_opy_, False))
        self.__1llllll11111_opy_(opts.get(bstack1llllllllll1_opy_, False))
        self.__1llllll1l1ll_opy_(opts.get(bstack1lllll1ll1l1_opy_, False))
    @classmethod
    def get_instance(cls, config=None):
        if cls._1ll1l11l111_opy_ is None and config is not None:
            cls._1ll1l11l111_opy_ = bstack1l1l11l11l_opy_(config)
        return cls._1ll1l11l111_opy_
    @staticmethod
    def bstack111lll1l11_opy_(config: dict) -> bool:
        bstack1lllllll1111_opy_ = config.get(bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ₹"), {}).get(bstack1lllll1l1ll1_opy_, {})
        return bstack1lllllll1111_opy_.get(bstack11l1l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ₺"), False)
    @staticmethod
    def bstack111lll1ll1_opy_(config: dict) -> int:
        bstack1lllllll1111_opy_ = config.get(bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ₻"), {}).get(bstack1lllll1l1ll1_opy_, {})
        retries = 0
        if bstack1l1l11l11l_opy_.bstack111lll1l11_opy_(config):
            retries = bstack1lllllll1111_opy_.get(bstack11l1l11_opy_ (u"ࠨ࡯ࡤࡼࡗ࡫ࡴࡳ࡫ࡨࡷࠬ₼"), 1)
        return retries
    @staticmethod
    def bstack1111lll1_opy_(config: dict) -> dict:
        bstack1lllll1l111l_opy_ = config.get(bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭₽"), {})
        return {
            key: value for key, value in bstack1lllll1l111l_opy_.items() if key in bstack1111111111l_opy_
        }
    @staticmethod
    def bstack11111111111_opy_():
        bstack11l1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ₾")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧ₿").format(os.getenv(bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⃀")))))
    @staticmethod
    def bstack1llllll1111l_opy_(test_name: str):
        bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⃁")
        bstack1llllll1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨ⃂").format(os.getenv(bstack11l1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ⃃"))))
        with open(bstack1llllll1ll1l_opy_, bstack11l1l11_opy_ (u"ࠩࡤࠫ⃄")) as file:
            file.write(bstack11l1l11_opy_ (u"ࠥࡿࢂࡢ࡮ࠣ⃅").format(test_name))
    @staticmethod
    def bstack11111111l11_opy_(framework: str) -> bool:
       return framework.lower() in bstack1lllll1l11l1_opy_
    @staticmethod
    def bstack111ll111l1l_opy_(config: dict) -> bool:
        bstack1lllllll111l_opy_ = config.get(bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ⃆"), {}).get(bstack1lllll11ll1l_opy_, {})
        return bstack1lllllll111l_opy_.get(bstack11l1l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⃇"), False)
    @staticmethod
    def bstack111ll11l1l1_opy_(config: dict, bstack111ll11llll_opy_: int = 0) -> int:
        bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠭ࠢࡺ࡬࡮ࡩࡨࠡࡥࡤࡲࠥࡨࡥࠡࡣࡱࠤࡦࡨࡳࡰ࡮ࡸࡸࡪࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡳࠢࡤࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭ࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡲࡸࡦࡲ࡟ࡵࡧࡶࡸࡸࠦࠨࡪࡰࡷ࠭࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤ࠭ࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⃈")
        bstack1lllllll111l_opy_ = config.get(bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ⃉"), {}).get(bstack11l1l11_opy_ (u"ࠨࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧ⃊"), {})
        bstack1lllll1ll11l_opy_ = 0
        bstack1llllllll1l1_opy_ = 0
        if bstack1l1l11l11l_opy_.bstack111ll111l1l_opy_(config):
            bstack1llllllll1l1_opy_ = bstack1lllllll111l_opy_.get(bstack11l1l11_opy_ (u"ࠩࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹࠧ⃋"), 5)
            if isinstance(bstack1llllllll1l1_opy_, str) and bstack1llllllll1l1_opy_.endswith(bstack11l1l11_opy_ (u"ࠪࠩࠬ⃌")):
                try:
                    percentage = int(bstack1llllllll1l1_opy_.strip(bstack11l1l11_opy_ (u"ࠫࠪ࠭⃍")))
                    if bstack111ll11llll_opy_ > 0:
                        bstack1lllll1ll11l_opy_ = math.ceil((percentage * bstack111ll11llll_opy_) / 100)
                    else:
                        raise ValueError(bstack11l1l11_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡱࡺࡹࡴࠡࡤࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵ࠱ࠦ⃎"))
                except ValueError as e:
                    raise ValueError(bstack11l1l11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨࠤࡻࡧ࡬ࡶࡧࠣࡪࡴࡸࠠ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷ࠿ࠦࡻࡾࠤ⃏").format(bstack1llllllll1l1_opy_)) from e
            else:
                bstack1lllll1ll11l_opy_ = int(bstack1llllllll1l1_opy_)
        logger.info(bstack11l1l11_opy_ (u"ࠢࡎࡣࡻࠤ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡶࡩࡹࠦࡴࡰ࠼ࠣࡿࢂࠦࠨࡧࡴࡲࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾࠫࠥ⃐").format(bstack1lllll1ll11l_opy_, bstack1llllllll1l1_opy_))
        return bstack1lllll1ll11l_opy_
    def bstack1lllll1l1lll_opy_(self):
        return self.bstack1llllll11l11_opy_
    def bstack1llllllll11l_opy_(self):
        return self.bstack1lllllll11ll_opy_
    def bstack1llllllll111_opy_(self):
        return self.bstack1lllll1l1l11_opy_
    def __11111111l1l_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1llllll11l11_opy_ = bool(enabled)
            if mode not in [bstack11l1l11_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ⃑"), bstack11l1l11_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡓࡳࡲࡹࠨ⃒")]:
                logger.warning(bstack11l1l11_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡳࡡࡳࡶࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦ࡭ࡰࡦࡨࠤࠬࢁࡽࠨࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠥࡊࡥࡧࡣࡸࡰࡹ࡯࡮ࡨࠢࡷࡳࠥ࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭࠮⃓ࠣ").format(mode))
                mode = bstack11l1l11_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡌࡩࡳࡵࡷࠫ⃔")
            self.bstack1lllllll11ll_opy_ = mode
            self.bstack1lllll1l1l11_opy_ = []
            if source is None:
                self.bstack1lllll1l1l11_opy_ = None
            elif isinstance(source, list):
                self.bstack1lllll1l1l11_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack11l1l11_opy_ (u"ࠬ࠴ࡪࡴࡱࡱࠫ⃕")):
                self.bstack1lllll1l1l11_opy_ = self._1llllll1l1l1_opy_(source)
            self.__1llllll111ll_opy_()
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳ࡮ࡣࡵࡸࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡ࠯ࠣࡩࡳࡧࡢ࡭ࡧࡧ࠾ࠥࢁࡽ࠭ࠢࡰࡳࡩ࡫࠺ࠡࡽࢀ࠰ࠥࡹ࡯ࡶࡴࡦࡩ࠿ࠦࡻࡾ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ⃖").format(enabled, mode, source, e))
    def bstack1lllll1l1l1l_opy_(self):
        return self.bstack1lllll1lllll_opy_
    def __1lllll1ll1ll_opy_(self, value):
        self.bstack1lllll1lllll_opy_ = bool(value)
        self.__1llllll111ll_opy_()
    def bstack111111111ll_opy_(self):
        return self.bstack1lllllllll1l_opy_
    def __1llllll11111_opy_(self, value):
        self.bstack1lllllllll1l_opy_ = bool(value)
        self.__1llllll111ll_opy_()
    def bstack1llllll1lll1_opy_(self):
        return self.bstack111111111l1_opy_
    def __1llllll1l1ll_opy_(self, value):
        self.bstack111111111l1_opy_ = bool(value)
        self.__1llllll111ll_opy_()
    def __1llllll111ll_opy_(self):
        if self.bstack1llllll11l11_opy_:
            self.bstack1lllll1lllll_opy_ = False
            self.bstack1lllllllll1l_opy_ = False
            self.bstack111111111l1_opy_ = False
            self.bstack1llllll11lll_opy_.enable(bstack1llllll1llll_opy_)
        elif self.bstack1lllll1lllll_opy_:
            self.bstack1lllllllll1l_opy_ = False
            self.bstack111111111l1_opy_ = False
            self.bstack1llllll11l11_opy_ = False
            self.bstack1llllll11lll_opy_.enable(bstack1lllllllll11_opy_)
        elif self.bstack1lllllllll1l_opy_:
            self.bstack1lllll1lllll_opy_ = False
            self.bstack111111111l1_opy_ = False
            self.bstack1llllll11l11_opy_ = False
            self.bstack1llllll11lll_opy_.enable(bstack1llllllllll1_opy_)
        elif self.bstack111111111l1_opy_:
            self.bstack1lllll1lllll_opy_ = False
            self.bstack1lllllllll1l_opy_ = False
            self.bstack1llllll11l11_opy_ = False
            self.bstack1llllll11lll_opy_.enable(bstack1lllll1ll1l1_opy_)
        else:
            self.bstack1llllll11lll_opy_.disable()
    def bstack1l1ll111ll_opy_(self):
        return self.bstack1llllll11lll_opy_.bstack1lllllll1ll1_opy_()
    def bstack1ll11llll_opy_(self):
        if self.bstack1llllll11lll_opy_.bstack1lllllll1ll1_opy_():
            return self.bstack1llllll11lll_opy_.get_name()
        return None
    def _1llllll1l1l1_opy_(self, bstack1llllll111l1_opy_):
        bstack11l1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡵࡲࡹࡷࡩࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠦࡡ࡯ࡦࠣࡪࡴࡸ࡭ࡢࡶࠣ࡭ࡹࠦࡦࡰࡴࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡸࡵࡵࡳࡥࡨࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠠࠩࡵࡷࡶ࠮ࡀࠠࡑࡣࡷ࡬ࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡓࡐࡐࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡯࡭ࡸࡺ࠺ࠡࡈࡲࡶࡲࡧࡴࡵࡧࡧࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡸࡥࡱࡱࡶ࡭ࡹࡵࡲࡺࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⃗")
        if not os.path.isfile(bstack1llllll111l1_opy_):
            logger.error(bstack11l1l11_opy_ (u"ࠣࡕࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠦࠧࡼࡿࠪࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠳ࠨ⃘").format(bstack1llllll111l1_opy_))
            return []
        data = None
        try:
            with open(bstack1llllll111l1_opy_, bstack11l1l11_opy_ (u"ࠤࡵ⃙ࠦ")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡎࡘࡕࡎࠡࡨࡵࡳࡲࠦࡳࡰࡷࡵࡧࡪࠦࡦࡪ࡮ࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ⃚").format(bstack1llllll111l1_opy_, e))
            return []
        _1lllllll1l1l_opy_ = None
        _1llllll11ll1_opy_ = None
        def _1lllllll1lll_opy_():
            bstack1llllllll1ll_opy_ = {}
            bstack1llllll1l111_opy_ = {}
            try:
                if self.bstack1lllllll1l11_opy_.startswith(bstack11l1l11_opy_ (u"ࠫࢀ࠭⃛")) and self.bstack1lllllll1l11_opy_.endswith(bstack11l1l11_opy_ (u"ࠬࢃࠧ⃜")):
                    bstack1llllllll1ll_opy_ = json.loads(self.bstack1lllllll1l11_opy_)
                else:
                    bstack1llllllll1ll_opy_ = dict(item.split(bstack11l1l11_opy_ (u"࠭࠺ࠨ⃝")) for item in self.bstack1lllllll1l11_opy_.split(bstack11l1l11_opy_ (u"ࠧ࠭ࠩ⃞")) if bstack11l1l11_opy_ (u"ࠨ࠼ࠪ⃟") in item) if self.bstack1lllllll1l11_opy_ else {}
                if self.bstack1lllll1l1111_opy_.startswith(bstack11l1l11_opy_ (u"ࠩࡾࠫ⃠")) and self.bstack1lllll1l1111_opy_.endswith(bstack11l1l11_opy_ (u"ࠪࢁࠬ⃡")):
                    bstack1llllll1l111_opy_ = json.loads(self.bstack1lllll1l1111_opy_)
                else:
                    bstack1llllll1l111_opy_ = dict(item.split(bstack11l1l11_opy_ (u"ࠫ࠿࠭⃢")) for item in self.bstack1lllll1l1111_opy_.split(bstack11l1l11_opy_ (u"ࠬ࠲ࠧ⃣")) if bstack11l1l11_opy_ (u"࠭࠺ࠨ⃤") in item) if self.bstack1lllll1l1111_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡧࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡ࡯ࡤࡴࡵ࡯࡮ࡨࡵ࠽ࠤࢀࢃ⃥ࠢ").format(e))
            logger.debug(bstack11l1l11_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡰࡥࡵࡶࡩ࡯ࡩࡶࠤ࡫ࡸ࡯࡮ࠢࡨࡲࡻࡀࠠࡼࡿ࠯ࠤࡈࡒࡉ࠻ࠢࡾࢁ⃦ࠧ").format(bstack1llllllll1ll_opy_, bstack1llllll1l111_opy_))
            return bstack1llllllll1ll_opy_, bstack1llllll1l111_opy_
        if _1lllllll1l1l_opy_ is None or _1llllll11ll1_opy_ is None:
            _1lllllll1l1l_opy_, _1llllll11ll1_opy_ = _1lllllll1lll_opy_()
        def bstack1lllll1llll1_opy_(name, bstack1lllll11llll_opy_):
            if name in _1llllll11ll1_opy_:
                return _1llllll11ll1_opy_[name]
            if name in _1lllllll1l1l_opy_:
                return _1lllllll1l1l_opy_[name]
            if bstack1lllll11llll_opy_.get(bstack11l1l11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ⃧")):
                return bstack1lllll11llll_opy_[bstack11l1l11_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪ⃨ࠪ")]
            return None
        if isinstance(data, dict):
            bstack1llllll1l11l_opy_ = []
            bstack1lllll11lll1_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡶࠬࡤ࡛ࡂ࠯࡝࠴࠲࠿࡟࡞࠭ࠧࠫ⃩"))
            for name, bstack1lllll11llll_opy_ in data.items():
                if not isinstance(bstack1lllll11llll_opy_, dict):
                    continue
                url = bstack1lllll11llll_opy_.get(bstack11l1l11_opy_ (u"ࠬࡻࡲ࡭⃪ࠩ"))
                if url is None or (isinstance(url, str) and url.strip() == bstack11l1l11_opy_ (u"⃫࠭ࠧ")):
                    logger.warning(bstack11l1l11_opy_ (u"ࠢࡓࡧࡳࡳࡸ࡯ࡴࡰࡴࡼࠤ࡚ࡘࡌࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡶࡳࡺࡸࡣࡦࠢࠪࡿࢂ࠭࠺ࠡࡽࢀ⃬ࠦ").format(name, bstack1lllll11llll_opy_))
                    continue
                if not bstack1lllll11lll1_opy_.match(name):
                    logger.warning(bstack11l1l11_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡶࡳࡺࡸࡣࡦࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠦࡦࡰࡴࡰࡥࡹࠦࡦࡰࡴࠣࠫࢀࢃࠧ࠻ࠢࡾࢁ⃭ࠧ").format(name, bstack1lllll11llll_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack11l1l11_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠦࠧࡼࡿࠪࠤࡲࡻࡳࡵࠢ࡫ࡥࡻ࡫ࠠࡢࠢ࡯ࡩࡳ࡭ࡴࡩࠢࡥࡩࡹࡽࡥࡦࡰࠣ࠵ࠥࡧ࡮ࡥࠢ࠶࠴ࠥࡩࡨࡢࡴࡤࡧࡹ࡫ࡲࡴ࠰⃮ࠥ").format(name))
                    continue
                bstack1lllll11llll_opy_ = bstack1lllll11llll_opy_.copy()
                bstack1lllll11llll_opy_[bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⃯")] = name
                bstack1lllll11llll_opy_[bstack11l1l11_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ⃰")] = bstack1lllll1llll1_opy_(name, bstack1lllll11llll_opy_)
                if not bstack1lllll11llll_opy_.get(bstack11l1l11_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ⃱")) or bstack1lllll11llll_opy_.get(bstack11l1l11_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭⃲")) == bstack11l1l11_opy_ (u"ࠧࠨ⃳"):
                    logger.warning(bstack11l1l11_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡱࡳࡹࠦࡳࡱࡧࡦ࡭࡫࡯ࡥࡥࠢࡩࡳࡷࠦࡳࡰࡷࡵࡧࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ⃴").format(name, bstack1lllll11llll_opy_))
                    continue
                if bstack1lllll11llll_opy_.get(bstack11l1l11_opy_ (u"ࠩࡥࡥࡸ࡫ࡂࡳࡣࡱࡧ࡭࠭⃵")) and bstack1lllll11llll_opy_[bstack11l1l11_opy_ (u"ࠪࡦࡦࡹࡥࡃࡴࡤࡲࡨ࡮ࠧ⃶")] == bstack1lllll11llll_opy_[bstack11l1l11_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ⃷")]:
                    logger.warning(bstack11l1l11_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡡ࡯ࡦࠣࡦࡦࡹࡥࠡࡤࡵࡥࡳࡩࡨࠡࡥࡤࡲࡳࡵࡴࠡࡤࡨࠤࡹ࡮ࡥࠡࡵࡤࡱࡪࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ⃸").format(name, bstack1lllll11llll_opy_))
                    continue
                bstack1llllll1l11l_opy_.append(bstack1lllll11llll_opy_)
            return bstack1llllll1l11l_opy_
        return data
    def bstack1111111llll_opy_(self):
        data = {
            bstack11l1l11_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ⃹"): {
                bstack11l1l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⃺"): self.bstack1lllll1l1lll_opy_(),
                bstack11l1l11_opy_ (u"ࠨ࡯ࡲࡨࡪ࠭⃻"): self.bstack1llllllll11l_opy_(),
                bstack11l1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ⃼"): self.bstack1llllllll111_opy_()
            }
        }
        return data
    def bstack1lllll1ll111_opy_(self, config):
        bstack1lllll1lll11_opy_ = {}
        bstack1lllll1lll11_opy_[bstack11l1l11_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ⃽")] = {
            bstack11l1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⃾"): self.bstack1lllll1l1lll_opy_(),
            bstack11l1l11_opy_ (u"ࠬࡳ࡯ࡥࡧࠪ⃿"): self.bstack1llllllll11l_opy_()
        }
        bstack1lllll1lll11_opy_[bstack11l1l11_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࠩ℀")] = {
            bstack11l1l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ℁"): self.bstack111111111ll_opy_()
        }
        bstack1lllll1lll11_opy_[bstack11l1l11_opy_ (u"ࠨࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࡡࡩ࡭ࡷࡹࡴࠨℂ")] = {
            bstack11l1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ℃"): self.bstack1lllll1l1l1l_opy_()
        }
        bstack1lllll1lll11_opy_[bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡨࡤ࡭ࡱ࡯࡮ࡨࡡࡤࡲࡩࡥࡦ࡭ࡣ࡮ࡽࠬ℄")] = {
            bstack11l1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ℅"): self.bstack1llllll1lll1_opy_()
        }
        if self.bstack111lll1l11_opy_(config):
            bstack1lllll1lll11_opy_[bstack11l1l11_opy_ (u"ࠬࡸࡥࡵࡴࡼࡣࡹ࡫ࡳࡵࡵࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧ℆")] = {
                bstack11l1l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧℇ"): True,
                bstack11l1l11_opy_ (u"ࠧ࡮ࡣࡻࡣࡷ࡫ࡴࡳ࡫ࡨࡷࠬ℈"): self.bstack111lll1ll1_opy_(config)
            }
        if self.bstack111ll111l1l_opy_(config):
            bstack1lllll1lll11_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡯࡯ࡡࡩࡥ࡮ࡲࡵࡳࡧࠪ℉")] = {
                bstack11l1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪℊ"): True,
                bstack11l1l11_opy_ (u"ࠪࡱࡦࡾ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡴࠩℋ"): self.bstack111ll11l1l1_opy_(config)
            }
        return bstack1lllll1lll11_opy_
    def bstack11llll111l_opy_(self, config):
        bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡲࡰࡱ࡫ࡣࡵࡵࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡣࡻࠣࡱࡦࡱࡩ࡯ࡩࠣࡥࠥࡩࡡ࡭࡮ࠣࡸࡴࠦࡴࡩࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠡࡧࡱࡨࡵࡵࡩ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠦࠨࡴࡶࡵ࠭࠿ࠦࡔࡩࡧ࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡤࡸ࡭ࡱࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢℌ")
        if not (config.get(bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨℍ"), None) in bstack111ll1ll1l1_opy_ and self.bstack1lllll1l1lll_opy_()):
            return None
        bstack1lllll1l11ll_opy_ = os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫℎ"), None)
        logger.debug(bstack11l1l11_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡉ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊ࠺ࠡࡽࢀࠦℏ").format(bstack1lllll1l11ll_opy_))
        try:
            bstack11l111l11ll_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠨℐ").format(bstack1lllll1l11ll_opy_)
            payload = {
                bstack11l1l11_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢℑ"): config.get(bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨℒ"), bstack11l1l11_opy_ (u"ࠫࠬℓ")),
                bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ℔"): config.get(bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩℕ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ№"): os.environ.get(bstack11l1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ℗"), bstack11l1l11_opy_ (u"ࠤࠥ℘")),
                bstack11l1l11_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨℙ"): int(os.environ.get(bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢℚ")) or bstack11l1l11_opy_ (u"ࠧ࠶ࠢℛ")),
                bstack11l1l11_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥℜ"): int(os.environ.get(bstack11l1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤℝ")) or bstack11l1l11_opy_ (u"ࠣ࠳ࠥ℞")),
                bstack11l1l11_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦ℟"): get_host_info(),
            }
            logger.debug(bstack11l1l11_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡰࡢࡻ࡯ࡳࡦࡪ࠺ࠡࡽࢀࠦ℠").format(payload))
            response = bstack11l1111l1ll_opy_.bstack1llllll11l1l_opy_(bstack11l111l11ll_opy_, payload)
            if response:
                logger.debug(bstack11l1l11_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡅࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ℡").format(response))
                return response
            else:
                logger.error(bstack11l1l11_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈ࠿ࠦࡻࡾࠤ™").format(bstack1lllll1l11ll_opy_))
                return None
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡖࡗࡌࡈࠥࢁࡽ࠻ࠢࡾࢁࠧ℣").format(bstack1lllll1l11ll_opy_, e))
            return None