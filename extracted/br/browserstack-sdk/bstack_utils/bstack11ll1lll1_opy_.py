# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack111l11l111_opy_, bstack1lllllllll1l_opy_
from bstack_utils.helper import bstack1lll1lll1lll_opy_, get_host_info
from bstack_utils.bstack111111lllll_opy_ import bstack11111l111ll_opy_
import json
import re
import sys
bstack1ll1ll11lll1_opy_ = bstack1l1llll_opy_ (u"ࠣࡴࡨࡸࡷࡿࡔࡦࡵࡷࡷࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢ⢎")
bstack1ll1ll111l11_opy_ = bstack1l1llll_opy_ (u"ࠤࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣ⢏")
bstack1ll1l1l1l1l1_opy_ = bstack1l1llll_opy_ (u"ࠥࡶࡺࡴࡐࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡉࡥ࡮ࡲࡥࡥࡈ࡬ࡶࡸࡺࠢ⢐")
bstack1ll1ll1111ll_opy_ = bstack1l1llll_opy_ (u"ࠦࡷ࡫ࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࠧ⢑")
bstack1ll1l1llllll_opy_ = bstack1l1llll_opy_ (u"ࠧࡹ࡫ࡪࡲࡉࡰࡦࡱࡹࡢࡰࡧࡊࡦ࡯࡬ࡦࡦࠥ⢒")
bstack1ll1ll1lllll_opy_ = bstack1l1llll_opy_ (u"ࠨࡲࡶࡰࡖࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࠥ⢓")
bstack1ll1ll1ll1ll_opy_ = {
    bstack1ll1ll11lll1_opy_,
    bstack1ll1ll111l11_opy_,
    bstack1ll1l1l1l1l1_opy_,
    bstack1ll1ll1111ll_opy_,
    bstack1ll1l1llllll_opy_,
    bstack1ll1ll1lllll_opy_
}
bstack1ll1ll1l1ll1_opy_ = {bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⢔")}
logger = logger_utils.get_logger(__name__, bstack111l11l111_opy_)
class bstack1ll1l1lll11l_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1ll1ll11llll_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack11ll1111l_opy_:
    _instance = None
    def __init__(self, config):
        self.bstack1ll1l1l1ll11_opy_ = False
        self.bstack1ll1ll11ll11_opy_ = False
        self.bstack1ll1ll1ll1l1_opy_ = False
        self.bstack1ll1ll1ll111_opy_ = False
        self.bstack1ll1l1l1llll_opy_ = None
        self.bstack1ll1l1lll111_opy_ = bstack1ll1l1lll11l_opy_()
        self.bstack1ll1ll1l1l1l_opy_ = None
        opts = config.get(bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⢕"), {})
        self.bstack1ll1ll111ll1_opy_ = config.get(bstack1l1llll_opy_ (u"ࠩࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡉࡓ࡜ࠧ⢖"), bstack1l1llll_opy_ (u"ࠥࠦ⢗"))
        self.bstack1ll1ll1l111l_opy_ = config.get(bstack1l1llll_opy_ (u"ࠫࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡉࡌࡊࠩ⢘"), bstack1l1llll_opy_ (u"ࠧࠨ⢙"))
        bstack1ll1l1l1l111_opy_ = opts.get(bstack1ll1ll1lllll_opy_, {})
        bstack1ll1l1l1l11l_opy_ = None
        if bstack1l1llll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭⢚") in bstack1ll1l1l1l111_opy_:
            bstack1ll1l1l1l1ll_opy_ = bstack1ll1l1l1l111_opy_[bstack1l1llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ⢛")]
            if bstack1ll1l1l1l1ll_opy_ is None or (isinstance(bstack1ll1l1l1l1ll_opy_, str) and bstack1ll1l1l1l1ll_opy_.strip() == bstack1l1llll_opy_ (u"ࠨࠩ⢜")) or (isinstance(bstack1ll1l1l1l1ll_opy_, list) and len(bstack1ll1l1l1l1ll_opy_) == 0):
                bstack1ll1l1l1l11l_opy_ = []
            elif isinstance(bstack1ll1l1l1l1ll_opy_, list):
                bstack1ll1l1l1l11l_opy_ = bstack1ll1l1l1l1ll_opy_
            elif isinstance(bstack1ll1l1l1l1ll_opy_, str) and bstack1ll1l1l1l1ll_opy_.strip():
                bstack1ll1l1l1l11l_opy_ = bstack1ll1l1l1l1ll_opy_
            else:
                logger.warning(bstack1l1llll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡷࡴࡻࡲࡤࡧࠣࡺࡦࡲࡵࡦࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾ࠰ࠣࡈࡪ࡬ࡡࡶ࡮ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡩࡲࡶࡴࡺࠢ࡯࡭ࡸࡺ࠮ࠣ⢝").format(bstack1ll1l1l1l1ll_opy_))
                bstack1ll1l1l1l11l_opy_ = []
        self.__1ll1l1l11ll1_opy_(
            bstack1ll1l1l1l111_opy_.get(bstack1l1llll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ⢞"), False),
            bstack1ll1l1l1l111_opy_.get(bstack1l1llll_opy_ (u"ࠫࡲࡵࡤࡦࠩ⢟"), bstack1l1llll_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ⢠")),
            bstack1ll1l1l1l11l_opy_
        )
        self.__1ll1ll1llll1_opy_(opts.get(bstack1ll1l1l1l1l1_opy_, False))
        self.__1ll1lll11111_opy_(opts.get(bstack1ll1ll1111ll_opy_, False))
        self.__1ll1lll1111l_opy_(opts.get(bstack1ll1l1llllll_opy_, False))
    @classmethod
    def bstack1lll1l11_opy_(cls, config=None):
        if cls._instance is None and config is not None:
            cls._instance = bstack11ll1111l_opy_(config)
        return cls._instance
    @staticmethod
    def bstack11lll1l1l_opy_(config: dict) -> bool:
        bstack1ll1ll1lll1l_opy_ = config.get(bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ⢡"), {}).get(bstack1ll1ll11lll1_opy_, {})
        return bstack1ll1ll1lll1l_opy_.get(bstack1l1llll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⢢"), False)
    @staticmethod
    def bstack1l1111111_opy_(config: dict) -> int:
        bstack1ll1ll1lll1l_opy_ = config.get(bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⢣"), {}).get(bstack1ll1ll11lll1_opy_, {})
        retries = 0
        if bstack11ll1111l_opy_.bstack11lll1l1l_opy_(config):
            retries = bstack1ll1ll1lll1l_opy_.get(bstack1l1llll_opy_ (u"ࠩࡰࡥࡽࡘࡥࡵࡴ࡬ࡩࡸ࠭⢤"), 1)
        return retries
    @staticmethod
    def bstack11111111ll_opy_(config: dict) -> dict:
        bstack1ll1ll1l1lll_opy_ = config.get(bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ⢥"), {})
        return {
            key: value for key, value in bstack1ll1ll1l1lll_opy_.items() if key in bstack1ll1ll1ll1ll_opy_
        }
    @staticmethod
    def bstack1ll1ll1ll11l_opy_():
        bstack1l1llll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⢦")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠧࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡿࢂࠨ⢧").format(os.getenv(bstack1l1llll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⢨")))))
    @staticmethod
    def bstack1ll1ll11ll1l_opy_(test_name: str):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⢩")
        bstack1ll1l1l11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡼࡿ࠱ࡸࡽࡺࠢ⢪").format(os.getenv(bstack1l1llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⢫"))))
        with open(bstack1ll1l1l11lll_opy_, bstack1l1llll_opy_ (u"ࠪࡥࠬ⢬")) as file:
            file.write(bstack1l1llll_opy_ (u"ࠦࢀࢃ࡜࡯ࠤ⢭").format(test_name))
    @staticmethod
    def bstack1ll1l1l1lll1_opy_(framework: str) -> bool:
       return framework.lower() in bstack1ll1ll1l1ll1_opy_
    @staticmethod
    def bstack1lllll1l1l1l_opy_(config: dict) -> bool:
        bstack1ll1ll111111_opy_ = config.get(bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⢮"), {}).get(bstack1ll1ll111l11_opy_, {})
        return bstack1ll1ll111111_opy_.get(bstack1l1llll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⢯"), False)
    @staticmethod
    def bstack1lllll1ll11l_opy_(config: dict, bstack1lllll1ll1ll_opy_: int = 0) -> int:
        bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥ࠮ࠣࡻ࡭࡯ࡣࡩࠢࡦࡥࡳࠦࡢࡦࠢࡤࡲࠥࡧࡢࡴࡱ࡯ࡹࡹ࡫ࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡴࠣࡥࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧࠡࠪࡧ࡭ࡨࡺࠩ࠻ࠢࡗ࡬ࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡳࡹࡧ࡬ࡠࡶࡨࡷࡹࡹࠠࠩ࡫ࡱࡸ࠮ࡀࠠࡕࡪࡨࠤࡹࡵࡴࡢ࡮ࠣࡲࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥ࠮ࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠮࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸ࠿ࠦࡔࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⢰")
        bstack1ll1ll111111_opy_ = config.get(bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⢱"), {}).get(bstack1l1llll_opy_ (u"ࠩࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠨ⢲"), {})
        bstack1ll1l1ll1l11_opy_ = 0
        bstack1ll1ll11l11l_opy_ = 0
        if bstack11ll1111l_opy_.bstack1lllll1l1l1l_opy_(config):
            bstack1ll1ll11l11l_opy_ = bstack1ll1ll111111_opy_.get(bstack1l1llll_opy_ (u"ࠪࡱࡦࡾࡆࡢ࡫࡯ࡹࡷ࡫ࡳࠨ⢳"), 5)
            if isinstance(bstack1ll1ll11l11l_opy_, str) and bstack1ll1ll11l11l_opy_.endswith(bstack1l1llll_opy_ (u"ࠫࠪ࠭⢴")):
                try:
                    percentage = int(bstack1ll1ll11l11l_opy_.strip(bstack1l1llll_opy_ (u"ࠬࠫࠧ⢵")))
                    if bstack1lllll1ll1ll_opy_ > 0:
                        bstack1ll1l1ll1l11_opy_ = math.ceil((percentage * bstack1lllll1ll1ll_opy_) / 100)
                    else:
                        raise ValueError(bstack1l1llll_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡲࡻࡳࡵࠢࡥࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠲ࠧ⢶"))
                except ValueError as e:
                    raise ValueError(bstack1l1llll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡵࡲࠡ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸࡀࠠࡼࡿࠥ⢷").format(bstack1ll1ll11l11l_opy_)) from e
            else:
                bstack1ll1l1ll1l11_opy_ = int(bstack1ll1ll11l11l_opy_)
        logger.info(bstack1l1llll_opy_ (u"ࠣࡏࡤࡼࠥ࡬ࡡࡪ࡮ࡸࡶࡪࡹࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡷࡪࡺࠠࡵࡱ࠽ࠤࢀࢃࠠࠩࡨࡵࡳࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿࠬࠦ⢸").format(bstack1ll1l1ll1l11_opy_, bstack1ll1ll11l11l_opy_))
        return bstack1ll1l1ll1l11_opy_
    def bstack1ll1l1ll1l1l_opy_(self):
        return self.bstack1ll1ll1ll111_opy_
    def bstack1ll1l1l11l1l_opy_(self):
        return self.bstack1ll1l1l1llll_opy_
    def bstack1ll1ll1l11ll_opy_(self):
        return self.bstack1ll1ll1l1l1l_opy_
    def __1ll1l1l11ll1_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1ll1ll1ll111_opy_ = bool(enabled)
            if mode not in [bstack1l1llll_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡊ࡮ࡸࡳࡵࠩ⢹"), bstack1l1llll_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡔࡴ࡬ࡺࠩ⢺")]:
                logger.warning(bstack1l1llll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠ࡮ࡱࡧࡩࠥ࠭ࡻࡾࠩࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡈ࡬ࡶࡸࡺࠧ࠯ࠤ⢻").format(mode))
                mode = bstack1l1llll_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ⢼")
            self.bstack1ll1l1l1llll_opy_ = mode
            self.bstack1ll1ll1l1l1l_opy_ = []
            if source is None:
                self.bstack1ll1ll1l1l1l_opy_ = None
            elif isinstance(source, list):
                self.bstack1ll1ll1l1l1l_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1l1llll_opy_ (u"࠭࠮࡫ࡵࡲࡲࠬ⢽")):
                self.bstack1ll1ll1l1l1l_opy_ = self._1ll1l1ll111l_opy_(source)
            self.__1ll1ll11l111_opy_()
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢ࠰ࠤࡪࡴࡡࡣ࡮ࡨࡨ࠿ࠦࡻࡾ࠮ࠣࡱࡴࡪࡥ࠻ࠢࡾࢁ࠱ࠦࡳࡰࡷࡵࡧࡪࡀࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ⢾").format(enabled, mode, source, e))
    def bstack1ll1ll1l1l11_opy_(self):
        return self.bstack1ll1l1l1ll11_opy_
    def __1ll1ll1llll1_opy_(self, value):
        self.bstack1ll1l1l1ll11_opy_ = bool(value)
        self.__1ll1ll11l111_opy_()
    def bstack1ll1l1ll11ll_opy_(self):
        return self.bstack1ll1ll11ll11_opy_
    def __1ll1lll11111_opy_(self, value):
        self.bstack1ll1ll11ll11_opy_ = bool(value)
        self.__1ll1ll11l111_opy_()
    def bstack1ll1l1ll1lll_opy_(self):
        return self.bstack1ll1ll1ll1l1_opy_
    def __1ll1lll1111l_opy_(self, value):
        self.bstack1ll1ll1ll1l1_opy_ = bool(value)
        self.__1ll1ll11l111_opy_()
    def __1ll1ll11l111_opy_(self):
        if self.bstack1ll1ll1ll111_opy_:
            self.bstack1ll1l1l1ll11_opy_ = False
            self.bstack1ll1ll11ll11_opy_ = False
            self.bstack1ll1ll1ll1l1_opy_ = False
            self.bstack1ll1l1lll111_opy_.enable(bstack1ll1ll1lllll_opy_)
        elif self.bstack1ll1l1l1ll11_opy_:
            self.bstack1ll1ll11ll11_opy_ = False
            self.bstack1ll1ll1ll1l1_opy_ = False
            self.bstack1ll1ll1ll111_opy_ = False
            self.bstack1ll1l1lll111_opy_.enable(bstack1ll1l1l1l1l1_opy_)
        elif self.bstack1ll1ll11ll11_opy_:
            self.bstack1ll1l1l1ll11_opy_ = False
            self.bstack1ll1ll1ll1l1_opy_ = False
            self.bstack1ll1ll1ll111_opy_ = False
            self.bstack1ll1l1lll111_opy_.enable(bstack1ll1ll1111ll_opy_)
        elif self.bstack1ll1ll1ll1l1_opy_:
            self.bstack1ll1l1l1ll11_opy_ = False
            self.bstack1ll1ll11ll11_opy_ = False
            self.bstack1ll1ll1ll111_opy_ = False
            self.bstack1ll1l1lll111_opy_.enable(bstack1ll1l1llllll_opy_)
        else:
            self.bstack1ll1l1lll111_opy_.disable()
    def bstack1ll1lll1_opy_(self):
        return self.bstack1ll1l1lll111_opy_.bstack1ll1ll11llll_opy_()
    def bstack1lll1111111_opy_(self):
        if self.bstack1ll1l1lll111_opy_.bstack1ll1ll11llll_opy_():
            return self.bstack1ll1l1lll111_opy_.get_name()
        return None
    def _1ll1l1ll111l_opy_(self, bstack1ll111ll1_opy_):
        bstack1l1llll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡶࡳࡺࡸࡣࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠠࡢࡰࡧࠤ࡫ࡵࡲ࡮ࡣࡷࠤ࡮ࡺࠠࡧࡱࡵࠤࡸࡳࡡࡳࡶࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡹ࡯ࡶࡴࡦࡩࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠡࠪࡶࡸࡷ࠯࠺ࠡࡒࡤࡸ࡭ࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡔࡑࡑࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡰ࡮ࡹࡴ࠻ࠢࡉࡳࡷࡳࡡࡵࡶࡨࡨࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡲࡦࡲࡲࡷ࡮ࡺ࡯ࡳࡻࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⢿")
        if not os.path.isfile(bstack1ll111ll1_opy_):
            logger.error(bstack1l1llll_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࠨࡽࢀࠫࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠢ⣀").format(bstack1ll111ll1_opy_))
            return []
        data = None
        try:
            with open(bstack1ll111ll1_opy_, bstack1l1llll_opy_ (u"ࠥࡶࠧ⣁")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤࡏ࡙ࡏࡏࠢࡩࡶࡴࡳࠠࡴࡱࡸࡶࡨ࡫ࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ⣂").format(bstack1ll111ll1_opy_, e))
            return []
        _1ll1l1lll1ll_opy_ = None
        _1ll1lll111l1_opy_ = None
        def _1ll1l1lllll1_opy_():
            bstack1ll1ll11l1ll_opy_ = {}
            bstack1ll1l1llll11_opy_ = {}
            try:
                if self.bstack1ll1ll111ll1_opy_.startswith(bstack1l1llll_opy_ (u"ࠬࢁࠧ⣃")) and self.bstack1ll1ll111ll1_opy_.endswith(bstack1l1llll_opy_ (u"࠭ࡽࠨ⣄")):
                    bstack1ll1ll11l1ll_opy_ = json.loads(self.bstack1ll1ll111ll1_opy_)
                else:
                    bstack1ll1ll11l1ll_opy_ = dict(item.split(bstack1l1llll_opy_ (u"ࠧ࠻ࠩ⣅")) for item in self.bstack1ll1ll111ll1_opy_.split(bstack1l1llll_opy_ (u"ࠨ࠮ࠪ⣆")) if bstack1l1llll_opy_ (u"ࠩ࠽ࠫ⣇") in item) if self.bstack1ll1ll111ll1_opy_ else {}
                if self.bstack1ll1ll1l111l_opy_.startswith(bstack1l1llll_opy_ (u"ࠪࡿࠬ⣈")) and self.bstack1ll1ll1l111l_opy_.endswith(bstack1l1llll_opy_ (u"ࠫࢂ࠭⣉")):
                    bstack1ll1l1llll11_opy_ = json.loads(self.bstack1ll1ll1l111l_opy_)
                else:
                    bstack1ll1l1llll11_opy_ = dict(item.split(bstack1l1llll_opy_ (u"ࠬࡀࠧ⣊")) for item in self.bstack1ll1ll1l111l_opy_.split(bstack1l1llll_opy_ (u"࠭ࠬࠨ⣋")) if bstack1l1llll_opy_ (u"ࠧ࠻ࠩ⣌") in item) if self.bstack1ll1ll1l111l_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡨࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡰࡥࡵࡶࡩ࡯ࡩࡶ࠾ࠥࢁࡽࠣ⣍").format(e))
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡱࡦࡶࡰࡪࡰࡪࡷࠥ࡬ࡲࡰ࡯ࠣࡩࡳࡼ࠺ࠡࡽࢀ࠰ࠥࡉࡌࡊ࠼ࠣࡿࢂࠨ⣎").format(bstack1ll1ll11l1ll_opy_, bstack1ll1l1llll11_opy_))
            return bstack1ll1ll11l1ll_opy_, bstack1ll1l1llll11_opy_
        if _1ll1l1lll1ll_opy_ is None or _1ll1lll111l1_opy_ is None:
            _1ll1l1lll1ll_opy_, _1ll1lll111l1_opy_ = _1ll1l1lllll1_opy_()
        def bstack1ll1l1ll1ll1_opy_(name, bstack1ll1ll1l1111_opy_):
            if name in _1ll1lll111l1_opy_:
                return _1ll1lll111l1_opy_[name]
            if name in _1ll1l1lll1ll_opy_:
                return _1ll1l1lll1ll_opy_[name]
            if bstack1ll1ll1l1111_opy_.get(bstack1l1llll_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ⣏")):
                return bstack1ll1ll1l1111_opy_[bstack1l1llll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ⣐")]
            return None
        if isinstance(data, dict):
            bstack1ll1ll111l1l_opy_ = []
            bstack1ll1l1llll1l_opy_ = re.compile(bstack1l1llll_opy_ (u"ࡷ࠭࡞࡜ࡃ࠰࡞࠵࠳࠹ࡠ࡟࠮ࠨࠬ⣑"))
            for name, bstack1ll1ll1l1111_opy_ in data.items():
                if not isinstance(bstack1ll1ll1l1111_opy_, dict):
                    continue
                if not bstack1ll1l1llll1l_opy_.match(name):
                    logger.warning(bstack1l1llll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡱࡸࡶࡨ࡫ࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤ࡫ࡵࡲ࡮ࡣࡷࠤ࡫ࡵࡲࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥ⣒").format(name, bstack1ll1ll1l1111_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1l1llll_opy_ (u"ࠢࡔࡱࡸࡶࡨ࡫ࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤࠬࢁࡽࠨࠢࡰࡹࡸࡺࠠࡩࡣࡹࡩࠥࡧࠠ࡭ࡧࡱ࡫ࡹ࡮ࠠࡣࡧࡷࡻࡪ࡫࡮ࠡ࠳ࠣࡥࡳࡪࠠ࠴࠲ࠣࡧ࡭ࡧࡲࡢࡥࡷࡩࡷࡹ࠮ࠣ⣓").format(name))
                    continue
                bstack1ll1ll1l1111_opy_ = bstack1ll1ll1l1111_opy_.copy()
                bstack1ll1ll1l1111_opy_[bstack1l1llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭⣔")] = name
                bstack1ll1ll1l1111_opy_[bstack1l1llll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ⣕")] = bstack1ll1l1ll1ll1_opy_(name, bstack1ll1ll1l1111_opy_)
                if not bstack1ll1ll1l1111_opy_.get(bstack1l1llll_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ⣖")) or bstack1ll1ll1l1111_opy_.get(bstack1l1llll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ⣗")) == bstack1l1llll_opy_ (u"ࠬ࠭⣘"):
                    logger.warning(bstack1l1llll_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠ࡯ࡱࡷࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡪࡪࠠࡧࡱࡵࠤࡸࡵࡵࡳࡥࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ⣙").format(name, bstack1ll1ll1l1111_opy_))
                    continue
                if bstack1ll1ll1l1111_opy_.get(bstack1l1llll_opy_ (u"ࠧࡣࡣࡶࡩࡇࡸࡡ࡯ࡥ࡫ࠫ⣚")) and bstack1ll1ll1l1111_opy_[bstack1l1llll_opy_ (u"ࠨࡤࡤࡷࡪࡈࡲࡢࡰࡦ࡬ࠬ⣛")] == bstack1ll1ll1l1111_opy_[bstack1l1llll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ⣜")]:
                    logger.warning(bstack1l1llll_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡦࡴࡤࠡࡤࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡣࡢࡰࡱࡳࡹࠦࡢࡦࠢࡷ࡬ࡪࠦࡳࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡵࡲࡹࡷࡩࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥ⣝").format(name, bstack1ll1ll1l1111_opy_))
                    continue
                bstack1ll1l1lll1l1_opy_ = bstack1ll1ll1l1111_opy_.get(bstack1l1llll_opy_ (u"ࠫࡹࡿࡰࡦࠩ⣞"), bstack1l1llll_opy_ (u"ࠬࡧࡰࡱࠩ⣟"))
                if bstack1ll1l1lll1l1_opy_ not in (bstack1l1llll_opy_ (u"࠭ࡡࡱࡲࠪ⣠"), bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࠬ⣡")):
                    logger.warning(bstack1l1llll_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡷࡽࡵ࡫ࠠࠨࡽࢀࠫࠥ࡬࡯ࡳࠢࡶࡳࡺࡸࡣࡦࠢࠪࡿࢂ࠭ࠬࠡࡦࡨࡪࡦࡻ࡬ࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࠩࡤࡴࡵ࠭ࠢ⣢").format(bstack1ll1l1lll1l1_opy_, name))
                    bstack1ll1l1lll1l1_opy_ = bstack1l1llll_opy_ (u"ࠩࡤࡴࡵ࠭⣣")
                bstack1ll1ll1l1111_opy_[bstack1l1llll_opy_ (u"ࠪࡸࡾࡶࡥࠨ⣤")] = bstack1ll1l1lll1l1_opy_
                bstack1ll1ll111l1l_opy_.append(bstack1ll1ll1l1111_opy_)
            bstack1ll1ll1111l1_opy_ = {item[bstack1l1llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⣥")] for item in bstack1ll1ll111l1l_opy_}
            for name, bstack1ll1ll1lll11_opy_ in {**_1ll1l1lll1ll_opy_, **_1ll1lll111l1_opy_}.items():
                if name in bstack1ll1ll1111l1_opy_:
                    continue
                if not bstack1ll1l1llll1l_opy_.match(name):
                    logger.warning(bstack1l1llll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸ࡭ࡢࡶࠣࡪࡴࡸࠠࠨࡽࢀࠫࠥ࡬ࡲࡰ࡯ࠣࡇࡑࡏ࠯ࡦࡰࡹࠦ⣦").format(name))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1l1llll_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࠫࢀࢃࠧࠡ࡯ࡸࡷࡹࠦࡨࡢࡸࡨࠤࡦࠦ࡬ࡦࡰࡪࡸ࡭ࠦࡢࡦࡶࡺࡩࡪࡴࠠ࠲ࠢࡤࡲࡩࠦ࠳࠱ࠢࡦ࡬ࡦࡸࡡࡤࡶࡨࡶࡸ࠴ࠢ⣧").format(name))
                    continue
                if not bstack1ll1ll1lll11_opy_:
                    continue
                if not isinstance(bstack1ll1ll1lll11_opy_, str):
                    logger.warning(bstack1l1llll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠡࡨࡲࡶࠥ࠭ࡻࡾࠩࠣࡪࡷࡵ࡭ࠡࡅࡏࡍ࠴࡫࡮ࡷ࠼ࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࠠࡴࡶࡵ࡭ࡳ࡭࠮ࠣ⣨").format(name))
                    continue
                bstack1ll1ll11111l_opy_ = bstack1ll1ll1lll11_opy_.strip()
                if bstack1ll1ll11111l_opy_ == bstack1l1llll_opy_ (u"ࠨࠩ⣩"):
                    continue
                bstack1ll1ll111l1l_opy_.append({bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⣪"): name, bstack1l1llll_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ⣫"): bstack1ll1ll11111l_opy_, bstack1l1llll_opy_ (u"ࠫࡹࡿࡰࡦࠩ⣬"): bstack1l1llll_opy_ (u"ࠬࡧࡰࡱࠩ⣭")})
            return bstack1ll1ll111l1l_opy_
        return data
    def bstack1ll1lll1l11l_opy_(self):
        data = {
            bstack1l1llll_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ⣮"): {
                bstack1l1llll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⣯"): self.bstack1ll1l1ll1l1l_opy_(),
                bstack1l1llll_opy_ (u"ࠨ࡯ࡲࡨࡪ࠭⣰"): self.bstack1ll1l1l11l1l_opy_(),
                bstack1l1llll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ⣱"): self.bstack1ll1ll1l11ll_opy_()
            }
        }
        return data
    def bstack1ll1l1l1ll1l_opy_(self, config):
        bstack1ll1l1ll11l1_opy_ = {}
        bstack1ll1l1ll11l1_opy_[bstack1l1llll_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ⣲")] = {
            bstack1l1llll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⣳"): self.bstack1ll1l1ll1l1l_opy_(),
            bstack1l1llll_opy_ (u"ࠬࡳ࡯ࡥࡧࠪ⣴"): self.bstack1ll1l1l11l1l_opy_()
        }
        bstack1ll1l1ll11l1_opy_[bstack1l1llll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࠩ⣵")] = {
            bstack1l1llll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⣶"): self.bstack1ll1l1ll11ll_opy_()
        }
        bstack1ll1l1ll11l1_opy_[bstack1l1llll_opy_ (u"ࠨࡴࡸࡲࡤࡶࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡡࡩࡥ࡮ࡲࡥࡥࡡࡩ࡭ࡷࡹࡴࠨ⣷")] = {
            bstack1l1llll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ⣸"): self.bstack1ll1ll1l1l11_opy_()
        }
        bstack1ll1l1ll11l1_opy_[bstack1l1llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡨࡤ࡭ࡱ࡯࡮ࡨࡡࡤࡲࡩࡥࡦ࡭ࡣ࡮ࡽࠬ⣹")] = {
            bstack1l1llll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⣺"): self.bstack1ll1l1ll1lll_opy_()
        }
        if self.bstack11lll1l1l_opy_(config):
            bstack1ll1l1ll11l1_opy_[bstack1l1llll_opy_ (u"ࠬࡸࡥࡵࡴࡼࡣࡹ࡫ࡳࡵࡵࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⣻")] = {
                bstack1l1llll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⣼"): True,
                bstack1l1llll_opy_ (u"ࠧ࡮ࡣࡻࡣࡷ࡫ࡴࡳ࡫ࡨࡷࠬ⣽"): self.bstack1l1111111_opy_(config)
            }
        if self.bstack1lllll1l1l1l_opy_(config):
            bstack1ll1ll111lll_opy_ = config.get(bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⣾"), {}).get(bstack1ll1ll111l11_opy_, {})
            bstack1ll1ll11l11l_opy_ = bstack1ll1ll111lll_opy_.get(bstack1l1llll_opy_ (u"ࠩࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹࠧ⣿"), 5)
            if isinstance(bstack1ll1ll11l11l_opy_, str) and bstack1ll1ll11l11l_opy_.endswith(bstack1l1llll_opy_ (u"ࠪࠩࠬ⤀")):
                bstack1ll1l1ll1111_opy_ = 0
            else:
                bstack1ll1l1ll1111_opy_ = int(bstack1ll1ll11l11l_opy_)
            bstack1ll1l1ll11l1_opy_[bstack1l1llll_opy_ (u"ࠫࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡲࡲࡤ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⤁")] = {
                bstack1l1llll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⤂"): True,
                bstack1l1llll_opy_ (u"࠭࡭ࡢࡺࡢࡪࡦ࡯࡬ࡶࡴࡨࡷࠬ⤃"): bstack1ll1l1ll1111_opy_
            }
        return bstack1ll1l1ll11l1_opy_
    def bstack1ll1l111l11_opy_(self, config):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡵ࡬࡭ࡧࡦࡸࡸࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡦࡾࠦ࡭ࡢ࡭࡬ࡲ࡬ࠦࡡࠡࡥࡤࡰࡱࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠢࠫࡷࡹࡸࠩ࠻ࠢࡗ࡬ࡪࠦࡕࡖࡋࡇࠤࡴ࡬ࠠࡵࡪࡨࠤࡧࡻࡩ࡭ࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠬࠡࡱࡵࠤࡓࡵ࡮ࡦࠢ࡬ࡪࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⤄")
        if not (config.get(bstack1l1llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⤅"), None) in bstack1lllllllll1l_opy_ and self.bstack1ll1l1ll1l1l_opy_()):
            return None
        bstack1ll1ll11l1l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⤆"), None)
        logger.debug(bstack1l1llll_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡢࡶ࡫࡯ࡨ࡛ࠥࡕࡊࡆ࠽ࠤࢀࢃࠢ⤇").format(bstack1ll1ll11l1l1_opy_))
        try:
            bstack11111l11lll_opy_ = bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠤ⤈").format(bstack1ll1ll11l1l1_opy_)
            payload = {
                bstack1l1llll_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥ⤉"): config.get(bstack1l1llll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ⤊"), bstack1l1llll_opy_ (u"ࠧࠨ⤋")),
                bstack1l1llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦ⤌"): config.get(bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ⤍"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ⤎"): os.environ.get(bstack1l1llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥ⤏"), bstack1l1llll_opy_ (u"ࠧࠨ⤐")),
                bstack1l1llll_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤ⤑"): int(os.environ.get(bstack1l1llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥ⤒")) or bstack1l1llll_opy_ (u"ࠣ࠲ࠥ⤓")),
                bstack1l1llll_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨ⤔"): int(os.environ.get(bstack1l1llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ⤕")) or bstack1l1llll_opy_ (u"ࠦ࠶ࠨ⤖")),
                bstack1l1llll_opy_ (u"ࠧ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠢ⤗"): get_host_info(),
            }
            logger.debug(bstack1l1llll_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡳࡥࡾࡲ࡯ࡢࡦ࠽ࠤࢀࢃࠢ⤘").format(payload))
            response = bstack11111l111ll_opy_.bstack1ll1ll1l11l1_opy_(bstack11111l11lll_opy_, payload)
            if response:
                logger.debug(bstack1l1llll_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡈࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⤙").format(response))
                return response
            else:
                logger.error(bstack1l1llll_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦ࡙࡚ࠣࡏࡄ࠻ࠢࡾࢁࠧ⤚").format(bstack1ll1ll11l1l1_opy_))
                return None
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡰ࡮࡯ࡩࡨࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦ࡙࡚ࠣࡏࡄࠡࡽࢀ࠾ࠥࢁࡽࠣ⤛").format(bstack1ll1ll11l1l1_opy_, e))
            return None