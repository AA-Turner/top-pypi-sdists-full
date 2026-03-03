# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack111ll1l11_opy_, bstack111lll1l1ll_opy_
from bstack_utils.helper import bstack1111lll1111_opy_, get_host_info
from bstack_utils.bstack11l111l1111_opy_ import bstack11l1111lll1_opy_
import json
import re
import sys
bstack1llllllll1l1_opy_ = bstack11ll111_opy_ (u"ࠦࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠥ₣")
bstack1lllll1l1l11_opy_ = bstack11ll111_opy_ (u"ࠧࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦ₤")
bstack1llllllllll1_opy_ = bstack11ll111_opy_ (u"ࠨࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࡋ࡯ࡲࡴࡶࠥ₥")
bstack111111111ll_opy_ = bstack11ll111_opy_ (u"ࠢࡳࡧࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࠣ₦")
bstack1llllll1llll_opy_ = bstack11ll111_opy_ (u"ࠣࡵ࡮࡭ࡵࡌ࡬ࡢ࡭ࡼࡥࡳࡪࡆࡢ࡫࡯ࡩࡩࠨ₧")
bstack1lllllllllll_opy_ = bstack11ll111_opy_ (u"ࠤࡵࡹࡳ࡙࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࠨ₨")
bstack1lllllll1ll1_opy_ = {
    bstack1llllllll1l1_opy_,
    bstack1lllll1l1l11_opy_,
    bstack1llllllllll1_opy_,
    bstack111111111ll_opy_,
    bstack1llllll1llll_opy_,
    bstack1lllllllllll_opy_
}
bstack1lllll1l11l1_opy_ = {bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ₩")}
logger = logger_utils.get_logger(__name__, bstack111ll1l11_opy_)
class bstack1llllll1lll1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lllllll11ll_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1111lll11_opy_:
    _1ll1l1llll1_opy_ = None
    def __init__(self, config):
        self.bstack1lllll1l11ll_opy_ = False
        self.bstack1lllll1l1l1l_opy_ = False
        self.bstack1lllll1l1111_opy_ = False
        self.bstack1lllllll1l11_opy_ = False
        self.bstack1lllllll11l1_opy_ = None
        self.bstack1llllll11ll1_opy_ = bstack1llllll1lll1_opy_()
        self.bstack1lllllll1l1l_opy_ = None
        opts = config.get(bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ₪"), {})
        self.bstack1llllll111ll_opy_ = config.get(bstack11ll111_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡅࡏࡘࠪ₫"), bstack11ll111_opy_ (u"ࠨࠢ€"))
        self.bstack1llllll1111l_opy_ = config.get(bstack11ll111_opy_ (u"ࠧࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࡅࡏࡍࠬ₭"), bstack11ll111_opy_ (u"ࠣࠤ₮"))
        bstack1lllll1ll11l_opy_ = opts.get(bstack1lllllllllll_opy_, {})
        bstack1llllll11lll_opy_ = None
        if bstack11ll111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ₯") in bstack1lllll1ll11l_opy_:
            bstack1lllllll1lll_opy_ = bstack1lllll1ll11l_opy_[bstack11ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ₰")]
            if bstack1lllllll1lll_opy_ is None or (isinstance(bstack1lllllll1lll_opy_, str) and bstack1lllllll1lll_opy_.strip() == bstack11ll111_opy_ (u"ࠫࠬ₱")) or (isinstance(bstack1lllllll1lll_opy_, list) and len(bstack1lllllll1lll_opy_) == 0):
                bstack1llllll11lll_opy_ = []
            elif isinstance(bstack1lllllll1lll_opy_, list):
                bstack1llllll11lll_opy_ = bstack1lllllll1lll_opy_
            elif isinstance(bstack1lllllll1lll_opy_, str) and bstack1lllllll1lll_opy_.strip():
                bstack1llllll11lll_opy_ = bstack1lllllll1lll_opy_
            else:
                logger.warning(bstack11ll111_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡶࡢ࡮ࡸࡩࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡾࢁ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࡥ࡮ࡲࡷࡽࠥࡲࡩࡴࡶ࠱ࠦ₲").format(bstack1lllllll1lll_opy_))
                bstack1llllll11lll_opy_ = []
        self.__1lllll1ll1ll_opy_(
            bstack1lllll1ll11l_opy_.get(bstack11ll111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ₳"), False),
            bstack1lllll1ll11l_opy_.get(bstack11ll111_opy_ (u"ࠧ࡮ࡱࡧࡩࠬ₴"), bstack11ll111_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ₵")),
            bstack1llllll11lll_opy_
        )
        self.__1llllll1l1l1_opy_(opts.get(bstack1llllllllll1_opy_, False))
        self.__1llllll1l11l_opy_(opts.get(bstack111111111ll_opy_, False))
        self.__1lllll1l111l_opy_(opts.get(bstack1llllll1llll_opy_, False))
    @classmethod
    def get_instance(cls, config=None):
        if cls._1ll1l1llll1_opy_ is None and config is not None:
            cls._1ll1l1llll1_opy_ = bstack1111lll11_opy_(config)
        return cls._1ll1l1llll1_opy_
    @staticmethod
    def bstack111ll11111_opy_(config: dict) -> bool:
        bstack111111111l1_opy_ = config.get(bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭₶"), {}).get(bstack1llllllll1l1_opy_, {})
        return bstack111111111l1_opy_.get(bstack11ll111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ₷"), False)
    @staticmethod
    def bstack11llllll_opy_(config: dict) -> int:
        bstack111111111l1_opy_ = config.get(bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ₸"), {}).get(bstack1llllllll1l1_opy_, {})
        retries = 0
        if bstack1111lll11_opy_.bstack111ll11111_opy_(config):
            retries = bstack111111111l1_opy_.get(bstack11ll111_opy_ (u"ࠬࡳࡡࡹࡔࡨࡸࡷ࡯ࡥࡴࠩ₹"), 1)
        return retries
    @staticmethod
    def bstack11l1l1lll1_opy_(config: dict) -> dict:
        bstack1llllll1ll1l_opy_ = config.get(bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ₺"), {})
        return {
            key: value for key, value in bstack1llllll1ll1l_opy_.items() if key in bstack1lllllll1ll1_opy_
        }
    @staticmethod
    def bstack1llllll11l11_opy_():
        bstack11ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ₻")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤ₼").format(os.getenv(bstack11ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ₽")))))
    @staticmethod
    def bstack1llllll1ll11_opy_(test_name: str):
        bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ₾")
        bstack1llllllll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶࠥ₿").format(os.getenv(bstack11ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⃀"))))
        with open(bstack1llllllll111_opy_, bstack11ll111_opy_ (u"࠭ࡡࠨ⃁")) as file:
            file.write(bstack11ll111_opy_ (u"ࠢࡼࡿ࡟ࡲࠧ⃂").format(test_name))
    @staticmethod
    def bstack1lllll1llll1_opy_(framework: str) -> bool:
       return framework.lower() in bstack1lllll1l11l1_opy_
    @staticmethod
    def bstack111ll1111ll_opy_(config: dict) -> bool:
        bstack1111111111l_opy_ = config.get(bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⃃"), {}).get(bstack1lllll1l1l11_opy_, {})
        return bstack1111111111l_opy_.get(bstack11ll111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ⃄"), False)
    @staticmethod
    def bstack111l1lllll1_opy_(config: dict, bstack111ll11111l_opy_: int = 0) -> int:
        bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠱ࠦࡷࡩ࡫ࡦ࡬ࠥࡩࡡ࡯ࠢࡥࡩࠥࡧ࡮ࠡࡣࡥࡷࡴࡲࡵࡵࡧࠣࡲࡺࡳࡢࡦࡴࠣࡳࡷࠦࡡࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺ࡯ࡵࡣ࡯ࡣࡹ࡫ࡳࡵࡵࠣࠬ࡮ࡴࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࠪࡵࡩࡶࡻࡩࡳࡧࡧࠤ࡫ࡵࡲࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠲ࡨࡡࡴࡧࡧࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࡳࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⃅")
        bstack1111111111l_opy_ = config.get(bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ⃆"), {}).get(bstack11ll111_opy_ (u"ࠬࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠫ⃇"), {})
        bstack1llllll1l1ll_opy_ = 0
        bstack1lllll11ll11_opy_ = 0
        if bstack1111lll11_opy_.bstack111ll1111ll_opy_(config):
            bstack1lllll11ll11_opy_ = bstack1111111111l_opy_.get(bstack11ll111_opy_ (u"࠭࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶࠫ⃈"), 5)
            if isinstance(bstack1lllll11ll11_opy_, str) and bstack1lllll11ll11_opy_.endswith(bstack11ll111_opy_ (u"ࠧࠦࠩ⃉")):
                try:
                    percentage = int(bstack1lllll11ll11_opy_.strip(bstack11ll111_opy_ (u"ࠨࠧࠪ⃊")))
                    if bstack111ll11111l_opy_ > 0:
                        bstack1llllll1l1ll_opy_ = math.ceil((percentage * bstack111ll11111l_opy_) / 100)
                    else:
                        raise ValueError(bstack11ll111_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨ࠱ࡧࡧࡳࡦࡦࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࡹ࠮ࠣ⃋"))
                except ValueError as e:
                    raise ValueError(bstack11ll111_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥࠡࡸࡤࡰࡺ࡫ࠠࡧࡱࡵࠤࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴ࠼ࠣࡿࢂࠨ⃌").format(bstack1lllll11ll11_opy_)) from e
            else:
                bstack1llllll1l1ll_opy_ = int(bstack1lllll11ll11_opy_)
        logger.info(bstack11ll111_opy_ (u"ࠦࡒࡧࡸࠡࡨࡤ࡭ࡱࡻࡲࡦࡵࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡳࡦࡶࠣࡸࡴࡀࠠࡼࡿࠣࠬ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡿࢂ࠯ࠢ⃍").format(bstack1llllll1l1ll_opy_, bstack1lllll11ll11_opy_))
        return bstack1llllll1l1ll_opy_
    def bstack1lllll1lll1l_opy_(self):
        return self.bstack1lllllll1l11_opy_
    def bstack1lllll1lllll_opy_(self):
        return self.bstack1lllllll11l1_opy_
    def bstack1lllll11lll1_opy_(self):
        return self.bstack1lllllll1l1l_opy_
    def __1lllll1ll1ll_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lllllll1l11_opy_ = bool(enabled)
            if mode not in [bstack11ll111_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ⃎"), bstack11ll111_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡐࡰ࡯ࡽࠬ⃏")]:
                logger.warning(bstack11ll111_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡱࡴࡪࡥࠡࠩࡾࢁࠬࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠢࡇࡩ࡫ࡧࡵ࡭ࡶ࡬ࡲ࡬ࠦࡴࡰࠢࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ࠲ࠧ⃐").format(mode))
                mode = bstack11ll111_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ⃑")
            self.bstack1lllllll11l1_opy_ = mode
            self.bstack1lllllll1l1l_opy_ = []
            if source is None:
                self.bstack1lllllll1l1l_opy_ = None
            elif isinstance(source, list):
                self.bstack1lllllll1l1l_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack11ll111_opy_ (u"ࠩ࠱࡮ࡸࡵ࡮ࠨ⃒")):
                self.bstack1lllllll1l1l_opy_ = self._1llllll111l1_opy_(source)
            self.__1llllll1l111_opy_()
        except Exception as e:
            logger.error(bstack11ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࠳ࠠࡦࡰࡤࡦࡱ࡫ࡤ࠻ࠢࡾࢁ࠱ࠦ࡭ࡰࡦࡨ࠾ࠥࢁࡽ࠭ࠢࡶࡳࡺࡸࡣࡦ࠼ࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࡼࡿ⃓ࠥ").format(enabled, mode, source, e))
    def bstack1lllll1ll1l1_opy_(self):
        return self.bstack1lllll1l11ll_opy_
    def __1llllll1l1l1_opy_(self, value):
        self.bstack1lllll1l11ll_opy_ = bool(value)
        self.__1llllll1l111_opy_()
    def bstack1llllll11111_opy_(self):
        return self.bstack1lllll1l1l1l_opy_
    def __1llllll1l11l_opy_(self, value):
        self.bstack1lllll1l1l1l_opy_ = bool(value)
        self.__1llllll1l111_opy_()
    def bstack1lllllll111l_opy_(self):
        return self.bstack1lllll1l1111_opy_
    def __1lllll1l111l_opy_(self, value):
        self.bstack1lllll1l1111_opy_ = bool(value)
        self.__1llllll1l111_opy_()
    def __1llllll1l111_opy_(self):
        if self.bstack1lllllll1l11_opy_:
            self.bstack1lllll1l11ll_opy_ = False
            self.bstack1lllll1l1l1l_opy_ = False
            self.bstack1lllll1l1111_opy_ = False
            self.bstack1llllll11ll1_opy_.enable(bstack1lllllllllll_opy_)
        elif self.bstack1lllll1l11ll_opy_:
            self.bstack1lllll1l1l1l_opy_ = False
            self.bstack1lllll1l1111_opy_ = False
            self.bstack1lllllll1l11_opy_ = False
            self.bstack1llllll11ll1_opy_.enable(bstack1llllllllll1_opy_)
        elif self.bstack1lllll1l1l1l_opy_:
            self.bstack1lllll1l11ll_opy_ = False
            self.bstack1lllll1l1111_opy_ = False
            self.bstack1lllllll1l11_opy_ = False
            self.bstack1llllll11ll1_opy_.enable(bstack111111111ll_opy_)
        elif self.bstack1lllll1l1111_opy_:
            self.bstack1lllll1l11ll_opy_ = False
            self.bstack1lllll1l1l1l_opy_ = False
            self.bstack1lllllll1l11_opy_ = False
            self.bstack1llllll11ll1_opy_.enable(bstack1llllll1llll_opy_)
        else:
            self.bstack1llllll11ll1_opy_.disable()
    def bstack11l1ll1l_opy_(self):
        return self.bstack1llllll11ll1_opy_.bstack1lllllll11ll_opy_()
    def bstack1l11111l11_opy_(self):
        if self.bstack1llllll11ll1_opy_.bstack1lllllll11ll_opy_():
            return self.bstack1llllll11ll1_opy_.get_name()
        return None
    def _1llllll111l1_opy_(self, bstack1llllllll11l_opy_):
        bstack11ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡹ࡯ࡶࡴࡦࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣࡥࡳࡪࠠࡧࡱࡵࡱࡦࡺࠠࡪࡶࠣࡪࡴࡸࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡲࡹࡷࡩࡥࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠤ࠭ࡹࡴࡳࠫ࠽ࠤࡕࡧࡴࡩࠢࡷࡳࠥࡺࡨࡦࠢࡍࡗࡔࡔࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࡬ࡪࡵࡷ࠾ࠥࡌ࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡵࡩࡵࡵࡳࡪࡶࡲࡶࡾࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⃔")
        if not os.path.isfile(bstack1llllllll11l_opy_):
            logger.error(bstack11ll111_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࠫࢀࢃࠧࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠥ⃕").format(bstack1llllllll11l_opy_))
            return []
        data = None
        try:
            with open(bstack1llllllll11l_opy_, bstack11ll111_opy_ (u"ࠨࡲࠣ⃖")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack11ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡋࡕࡒࡒࠥ࡬ࡲࡰ࡯ࠣࡷࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥ⃗").format(bstack1llllllll11l_opy_, e))
            return []
        _1lllll11llll_opy_ = None
        _1llllll11l1l_opy_ = None
        def _1lllllll1111_opy_():
            bstack1lllll11ll1l_opy_ = {}
            bstack1lllllllll11_opy_ = {}
            try:
                if self.bstack1llllll111ll_opy_.startswith(bstack11ll111_opy_ (u"ࠨࡽ⃘ࠪ")) and self.bstack1llllll111ll_opy_.endswith(bstack11ll111_opy_ (u"ࠩࢀ⃙ࠫ")):
                    bstack1lllll11ll1l_opy_ = json.loads(self.bstack1llllll111ll_opy_)
                else:
                    bstack1lllll11ll1l_opy_ = dict(item.split(bstack11ll111_opy_ (u"ࠪ࠾⃚ࠬ")) for item in self.bstack1llllll111ll_opy_.split(bstack11ll111_opy_ (u"ࠫ࠱࠭⃛")) if bstack11ll111_opy_ (u"ࠬࡀࠧ⃜") in item) if self.bstack1llllll111ll_opy_ else {}
                if self.bstack1llllll1111l_opy_.startswith(bstack11ll111_opy_ (u"࠭ࡻࠨ⃝")) and self.bstack1llllll1111l_opy_.endswith(bstack11ll111_opy_ (u"ࠧࡾࠩ⃞")):
                    bstack1lllllllll11_opy_ = json.loads(self.bstack1llllll1111l_opy_)
                else:
                    bstack1lllllllll11_opy_ = dict(item.split(bstack11ll111_opy_ (u"ࠨ࠼ࠪ⃟")) for item in self.bstack1llllll1111l_opy_.split(bstack11ll111_opy_ (u"ࠩ࠯ࠫ⃠")) if bstack11ll111_opy_ (u"ࠪ࠾ࠬ⃡") in item) if self.bstack1llllll1111l_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤ࡫࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡳࡡࡱࡲ࡬ࡲ࡬ࡹ࠺ࠡࡽࢀࠦ⃢").format(e))
            logger.debug(bstack11ll111_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࡳࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࠽ࠤࢀࢃࠬࠡࡅࡏࡍ࠿ࠦࡻࡾࠤ⃣").format(bstack1lllll11ll1l_opy_, bstack1lllllllll11_opy_))
            return bstack1lllll11ll1l_opy_, bstack1lllllllll11_opy_
        if _1lllll11llll_opy_ is None or _1llllll11l1l_opy_ is None:
            _1lllll11llll_opy_, _1llllll11l1l_opy_ = _1lllllll1111_opy_()
        def bstack1lllll1lll11_opy_(name, bstack1lllllllll1l_opy_):
            if name in _1llllll11l1l_opy_:
                return _1llllll11l1l_opy_[name]
            if name in _1lllll11llll_opy_:
                return _1lllll11llll_opy_[name]
            if bstack1lllllllll1l_opy_.get(bstack11ll111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭⃤")):
                return bstack1lllllllll1l_opy_[bstack11ll111_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮⃥ࠧ")]
            return None
        if isinstance(data, dict):
            bstack11111111l11_opy_ = []
            bstack1lllll1l1lll_opy_ = re.compile(bstack11ll111_opy_ (u"ࡳࠩࡡ࡟ࡆ࠳࡚࠱࠯࠼ࡣࡢ࠱ࠤࠨ⃦"))
            for name, bstack1lllllllll1l_opy_ in data.items():
                if not isinstance(bstack1lllllllll1l_opy_, dict):
                    continue
                url = bstack1lllllllll1l_opy_.get(bstack11ll111_opy_ (u"ࠩࡸࡶࡱ࠭⃧"))
                if url is None or (isinstance(url, str) and url.strip() == bstack11ll111_opy_ (u"⃨ࠪࠫ")):
                    logger.warning(bstack11ll111_opy_ (u"ࠦࡗ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹࠡࡗࡕࡐࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡳࡰࡷࡵࡧࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ⃩").format(name, bstack1lllllllll1l_opy_))
                    continue
                if not bstack1lllll1l1lll_opy_.match(name):
                    logger.warning(bstack11ll111_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸ࡭ࡢࡶࠣࡪࡴࡸࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ⃪").format(name, bstack1lllllllll1l_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack11ll111_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࠫࢀࢃࠧࠡ࡯ࡸࡷࡹࠦࡨࡢࡸࡨࠤࡦࠦ࡬ࡦࡰࡪࡸ࡭ࠦࡢࡦࡶࡺࡩࡪࡴࠠ࠲ࠢࡤࡲࡩࠦ࠳࠱ࠢࡦ࡬ࡦࡸࡡࡤࡶࡨࡶࡸ࠴⃫ࠢ").format(name))
                    continue
                bstack1lllllllll1l_opy_ = bstack1lllllllll1l_opy_.copy()
                bstack1lllllllll1l_opy_[bstack11ll111_opy_ (u"ࠧ࡯ࡣࡰࡩ⃬ࠬ")] = name
                bstack1lllllllll1l_opy_[bstack11ll111_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ⃭")] = bstack1lllll1lll11_opy_(name, bstack1lllllllll1l_opy_)
                if not bstack1lllllllll1l_opy_.get(bstack11ll111_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩ⃮ࠩ")) or bstack1lllllllll1l_opy_.get(bstack11ll111_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪ⃯ࠪ")) == bstack11ll111_opy_ (u"ࠫࠬ⃰"):
                    logger.warning(bstack11ll111_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡮ࡰࡶࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡩࡩࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ⃱").format(name, bstack1lllllllll1l_opy_))
                    continue
                if bstack1lllllllll1l_opy_.get(bstack11ll111_opy_ (u"࠭ࡢࡢࡵࡨࡆࡷࡧ࡮ࡤࡪࠪ⃲")) and bstack1lllllllll1l_opy_[bstack11ll111_opy_ (u"ࠧࡣࡣࡶࡩࡇࡸࡡ࡯ࡥ࡫ࠫ⃳")] == bstack1lllllllll1l_opy_[bstack11ll111_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ⃴")]:
                    logger.warning(bstack11ll111_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡥࡳࡪࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡶ࡫ࡩࠥࡹࡡ࡮ࡧࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ⃵").format(name, bstack1lllllllll1l_opy_))
                    continue
                bstack11111111l11_opy_.append(bstack1lllllllll1l_opy_)
            return bstack11111111l11_opy_
        return data
    def bstack1111111l111_opy_(self):
        data = {
            bstack11ll111_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ⃶"): {
                bstack11ll111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⃷"): self.bstack1lllll1lll1l_opy_(),
                bstack11ll111_opy_ (u"ࠬࡳ࡯ࡥࡧࠪ⃸"): self.bstack1lllll1lllll_opy_(),
                bstack11ll111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭⃹"): self.bstack1lllll11lll1_opy_()
            }
        }
        return data
    def bstack11111111111_opy_(self, config):
        bstack1lllll1l1ll1_opy_ = {}
        bstack1lllll1l1ll1_opy_[bstack11ll111_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭⃺")] = {
            bstack11ll111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⃻"): self.bstack1lllll1lll1l_opy_(),
            bstack11ll111_opy_ (u"ࠩࡰࡳࡩ࡫ࠧ⃼"): self.bstack1lllll1lllll_opy_()
        }
        bstack1lllll1l1ll1_opy_[bstack11ll111_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩ࠭⃽")] = {
            bstack11ll111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⃾"): self.bstack1llllll11111_opy_()
        }
        bstack1lllll1l1ll1_opy_[bstack11ll111_opy_ (u"ࠬࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩࡥࡦࡪࡴࡶࡸࠬ⃿")] = {
            bstack11ll111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ℀"): self.bstack1lllll1ll1l1_opy_()
        }
        bstack1lllll1l1ll1_opy_[bstack11ll111_opy_ (u"ࠧࡴ࡭࡬ࡴࡤ࡬ࡡࡪ࡮࡬ࡲ࡬ࡥࡡ࡯ࡦࡢࡪࡱࡧ࡫ࡺࠩ℁")] = {
            bstack11ll111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩℂ"): self.bstack1lllllll111l_opy_()
        }
        if self.bstack111ll11111_opy_(config):
            bstack1lllll1l1ll1_opy_[bstack11ll111_opy_ (u"ࠩࡵࡩࡹࡸࡹࡠࡶࡨࡷࡹࡹ࡟ࡰࡰࡢࡪࡦ࡯࡬ࡶࡴࡨࠫ℃")] = {
                bstack11ll111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ℄"): True,
                bstack11ll111_opy_ (u"ࠫࡲࡧࡸࡠࡴࡨࡸࡷ࡯ࡥࡴࠩ℅"): self.bstack11llllll_opy_(config)
            }
        if self.bstack111ll1111ll_opy_(config):
            bstack1lllll1l1ll1_opy_[bstack11ll111_opy_ (u"ࠬࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧ℆")] = {
                bstack11ll111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧℇ"): True,
                bstack11ll111_opy_ (u"ࠧ࡮ࡣࡻࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡸ࠭℈"): self.bstack111l1lllll1_opy_(config)
            }
        return bstack1lllll1l1ll1_opy_
    def bstack111l11l11l_opy_(self, config):
        bstack11ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࡹࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤࡧࡿࠠ࡮ࡣ࡮࡭ࡳ࡭ࠠࡢࠢࡦࡥࡱࡲࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡨࡵࡪ࡮ࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ℉")
        if not (config.get(bstack11ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬℊ"), None) in bstack111lll1l1ll_opy_ and self.bstack1lllll1lll1l_opy_()):
            return None
        bstack1lllll1ll111_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨℋ"), None)
        logger.debug(bstack11ll111_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡆࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣℌ").format(bstack1lllll1ll111_opy_))
        try:
            bstack11l111l11l1_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠥℍ").format(bstack1lllll1ll111_opy_)
            payload = {
                bstack11ll111_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦℎ"): config.get(bstack11ll111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬℏ"), bstack11ll111_opy_ (u"ࠨࠩℐ")),
                bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧℑ"): config.get(bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ℒ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤℓ"): os.environ.get(bstack11ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦ℔"), bstack11ll111_opy_ (u"ࠨࠢℕ")),
                bstack11ll111_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ№"): int(os.environ.get(bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ℗")) or bstack11ll111_opy_ (u"ࠤ࠳ࠦ℘")),
                bstack11ll111_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢℙ"): int(os.environ.get(bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨℚ")) or bstack11ll111_opy_ (u"ࠧ࠷ࠢℛ")),
                bstack11ll111_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣℜ"): get_host_info(),
            }
            logger.debug(bstack11ll111_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡ࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡴࡦࡿ࡬ࡰࡣࡧ࠾ࠥࢁࡽࠣℝ").format(payload))
            response = bstack11l1111lll1_opy_.bstack1llllllll1ll_opy_(bstack11l111l11l1_opy_, payload)
            if response:
                logger.debug(bstack11ll111_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡂࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ℞").format(response))
                return response
            else:
                logger.error(bstack11ll111_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨ℟").format(bstack1lllll1ll111_opy_))
                return None
        except Exception as e:
            logger.error(bstack11ll111_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅࠢࡾࢁ࠿ࠦࡻࡾࠤ℠").format(bstack1lllll1ll111_opy_, e))
            return None