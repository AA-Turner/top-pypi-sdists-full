# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack1l11ll11l1_opy_, bstack111ll111lll_opy_
from bstack_utils.helper import bstack111l11ll11l_opy_, get_host_info
from bstack_utils.bstack111lll1l11l_opy_ import bstack111lll1lll1_opy_
import json
import re
import sys
bstack1llll1ll111l_opy_ = bstack1111_opy_ (u"ࠤࡵࡩࡹࡸࡹࡕࡧࡶࡸࡸࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣ⇎")
bstack1lllll1llll1_opy_ = bstack1111_opy_ (u"ࠥࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠤ⇏")
bstack1lllll1111ll_opy_ = bstack1111_opy_ (u"ࠦࡷࡻ࡮ࡑࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡊࡦ࡯࡬ࡦࡦࡉ࡭ࡷࡹࡴࠣ⇐")
bstack1llllll111ll_opy_ = bstack1111_opy_ (u"ࠧࡸࡥࡳࡷࡱࡔࡷ࡫ࡶࡪࡱࡸࡷࡱࡿࡆࡢ࡫࡯ࡩࡩࠨ⇑")
bstack1llll1ll11l1_opy_ = bstack1111_opy_ (u"ࠨࡳ࡬࡫ࡳࡊࡱࡧ࡫ࡺࡣࡱࡨࡋࡧࡩ࡭ࡧࡧࠦ⇒")
bstack1llll1l1llll_opy_ = bstack1111_opy_ (u"ࠢࡳࡷࡱࡗࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࠦ⇓")
bstack1lllll1111l1_opy_ = {
    bstack1llll1ll111l_opy_,
    bstack1lllll1llll1_opy_,
    bstack1lllll1111ll_opy_,
    bstack1llllll111ll_opy_,
    bstack1llll1ll11l1_opy_,
    bstack1llll1l1llll_opy_
}
bstack1llllll1111l_opy_ = {bstack1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⇔")}
logger = logger_utils.get_logger(__name__, bstack1l11ll11l1_opy_)
class bstack1lllll1ll1l1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1llll1ll1l11_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack11l111lll1_opy_:
    _1ll1l11l1ll_opy_ = None
    def __init__(self, config):
        self.bstack1lllll1lll11_opy_ = False
        self.bstack1lllll11111l_opy_ = False
        self.bstack1lllll1l1ll1_opy_ = False
        self.bstack1lllll11l111_opy_ = False
        self.bstack1lllll111l1l_opy_ = None
        self.bstack1llll1l1ll11_opy_ = bstack1lllll1ll1l1_opy_()
        self.bstack1llll1ll11ll_opy_ = None
        opts = config.get(bstack1111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭⇕"), {})
        self.bstack1lllll1l1111_opy_ = config.get(bstack1111_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡊࡔࡖࠨ⇖"), bstack1111_opy_ (u"ࠦࠧ⇗"))
        self.bstack1lllll111111_opy_ = config.get(bstack1111_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡃࡍࡋࠪ⇘"), bstack1111_opy_ (u"ࠨࠢ⇙"))
        bstack1llll1lll11l_opy_ = opts.get(bstack1llll1l1llll_opy_, {})
        bstack1llll1lllll1_opy_ = None
        if bstack1111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ⇚") in bstack1llll1lll11l_opy_:
            bstack1llll1llll1l_opy_ = bstack1llll1lll11l_opy_[bstack1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ⇛")]
            if bstack1llll1llll1l_opy_ is None or (isinstance(bstack1llll1llll1l_opy_, str) and bstack1llll1llll1l_opy_.strip() == bstack1111_opy_ (u"ࠩࠪ⇜")) or (isinstance(bstack1llll1llll1l_opy_, list) and len(bstack1llll1llll1l_opy_) == 0):
                bstack1llll1lllll1_opy_ = []
            elif isinstance(bstack1llll1llll1l_opy_, list):
                bstack1llll1lllll1_opy_ = bstack1llll1llll1l_opy_
            elif isinstance(bstack1llll1llll1l_opy_, str) and bstack1llll1llll1l_opy_.strip():
                bstack1llll1lllll1_opy_ = bstack1llll1llll1l_opy_
            else:
                logger.warning(bstack1111_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡵࡵࡳࡥࡨࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿ࠱ࠤࡉ࡫ࡦࡢࡷ࡯ࡸ࡮ࡴࡧࠡࡶࡲࠤࡪࡳࡰࡵࡻࠣࡰ࡮ࡹࡴ࠯ࠤ⇝").format(bstack1llll1llll1l_opy_))
                bstack1llll1lllll1_opy_ = []
        self.__1lllll11ll11_opy_(
            bstack1llll1lll11l_opy_.get(bstack1111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⇞"), False),
            bstack1llll1lll11l_opy_.get(bstack1111_opy_ (u"ࠬࡳ࡯ࡥࡧࠪ⇟"), bstack1111_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭⇠")),
            bstack1llll1lllll1_opy_
        )
        self.__1llll1ll1ll1_opy_(opts.get(bstack1lllll1111ll_opy_, False))
        self.__1lllll1ll11l_opy_(opts.get(bstack1llllll111ll_opy_, False))
        self.__1llll1lll1ll_opy_(opts.get(bstack1llll1ll11l1_opy_, False))
    @classmethod
    def get_instance(cls, config=None):
        if cls._1ll1l11l1ll_opy_ is None and config is not None:
            cls._1ll1l11l1ll_opy_ = bstack11l111lll1_opy_(config)
        return cls._1ll1l11l1ll_opy_
    @staticmethod
    def bstack11111l11_opy_(config: dict) -> bool:
        bstack1lllll11l1l1_opy_ = config.get(bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ⇡"), {}).get(bstack1llll1ll111l_opy_, {})
        return bstack1lllll11l1l1_opy_.get(bstack1111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⇢"), False)
    @staticmethod
    def bstack1ll11111ll_opy_(config: dict) -> int:
        bstack1lllll11l1l1_opy_ = config.get(bstack1111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭⇣"), {}).get(bstack1llll1ll111l_opy_, {})
        retries = 0
        if bstack11l111lll1_opy_.bstack11111l11_opy_(config):
            retries = bstack1lllll11l1l1_opy_.get(bstack1111_opy_ (u"ࠪࡱࡦࡾࡒࡦࡶࡵ࡭ࡪࡹࠧ⇤"), 1)
        return retries
    @staticmethod
    def bstack111l11llll_opy_(config: dict) -> dict:
        bstack1lllll1l11ll_opy_ = config.get(bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ⇥"), {})
        return {
            key: value for key, value in bstack1lllll1l11ll_opy_.items() if key in bstack1lllll1111l1_opy_
        }
    @staticmethod
    def bstack1lllll1ll111_opy_():
        bstack1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⇦")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃࠢ⇧").format(os.getenv(bstack1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⇨")))))
    @staticmethod
    def bstack1lllll11llll_opy_(test_name: str):
        bstack1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⇩")
        bstack1llll1l1l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣ⇪").format(os.getenv(bstack1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⇫"))))
        with open(bstack1llll1l1l1ll_opy_, bstack1111_opy_ (u"ࠫࡦ࠭⇬")) as file:
            file.write(bstack1111_opy_ (u"ࠧࢁࡽ࡝ࡰࠥ⇭").format(test_name))
    @staticmethod
    def bstack1lllll111ll1_opy_(framework: str) -> bool:
       return framework.lower() in bstack1llllll1111l_opy_
    @staticmethod
    def bstack111l1l11111_opy_(config: dict) -> bool:
        bstack1llll1llllll_opy_ = config.get(bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ⇮"), {}).get(bstack1lllll1llll1_opy_, {})
        return bstack1llll1llllll_opy_.get(bstack1111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⇯"), False)
    @staticmethod
    def bstack111l1l11lll_opy_(config: dict, bstack111l1l11ll1_opy_: int = 0) -> int:
        bstack1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠯ࠤࡼ࡮ࡩࡤࡪࠣࡧࡦࡴࠠࡣࡧࠣࡥࡳࠦࡡࡣࡵࡲࡰࡺࡺࡥࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡵࠤࡦࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡴࡺࡡ࡭ࡡࡷࡩࡸࡺࡳࠡࠪ࡬ࡲࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࠨࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡩࡳࡷࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠰ࡦࡦࡹࡥࡥࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࡸ࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⇰")
        bstack1llll1llllll_opy_ = config.get(bstack1111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭⇱"), {}).get(bstack1111_opy_ (u"ࠪࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠩ⇲"), {})
        bstack1lllll1lll1l_opy_ = 0
        bstack1llll1llll11_opy_ = 0
        if bstack11l111lll1_opy_.bstack111l1l11111_opy_(config):
            bstack1llll1llll11_opy_ = bstack1llll1llllll_opy_.get(bstack1111_opy_ (u"ࠫࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴࠩ⇳"), 5)
            if isinstance(bstack1llll1llll11_opy_, str) and bstack1llll1llll11_opy_.endswith(bstack1111_opy_ (u"ࠬࠫࠧ⇴")):
                try:
                    percentage = int(bstack1llll1llll11_opy_.strip(bstack1111_opy_ (u"࠭ࠥࠨ⇵")))
                    if bstack111l1l11ll1_opy_ > 0:
                        bstack1lllll1lll1l_opy_ = math.ceil((percentage * bstack111l1l11ll1_opy_) / 100)
                    else:
                        raise ValueError(bstack1111_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡳࡵࡴࡶࠣࡦࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠳ࠨ⇶"))
                except ValueError as e:
                    raise ValueError(bstack1111_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪࠦࡶࡢ࡮ࡸࡩࠥ࡬࡯ࡳࠢࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹ࠺ࠡࡽࢀࠦ⇷").format(bstack1llll1llll11_opy_)) from e
            else:
                bstack1lllll1lll1l_opy_ = int(bstack1llll1llll11_opy_)
        logger.info(bstack1111_opy_ (u"ࠤࡐࡥࡽࠦࡦࡢ࡫࡯ࡹࡷ࡫ࡳࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡸ࡫ࡴࠡࡶࡲ࠾ࠥࢁࡽࠡࠪࡩࡶࡴࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡽࢀ࠭ࠧ⇸").format(bstack1lllll1lll1l_opy_, bstack1llll1llll11_opy_))
        return bstack1lllll1lll1l_opy_
    def bstack1llll1ll1111_opy_(self):
        return self.bstack1lllll11l111_opy_
    def bstack1llll1ll1l1l_opy_(self):
        return self.bstack1lllll111l1l_opy_
    def bstack1lllll11l11l_opy_(self):
        return self.bstack1llll1ll11ll_opy_
    def __1lllll11ll11_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lllll11l111_opy_ = bool(enabled)
            if mode not in [bstack1111_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ⇹"), bstack1111_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡕ࡮࡭ࡻࠪ⇺")]:
                logger.warning(bstack1111_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳ࡮ࡣࡵࡸࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡ࡯ࡲࡨࡪࠦࠧࡼࡿࠪࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡅࡧࡩࡥࡺࡲࡴࡪࡰࡪࠤࡹࡵࠠࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ࠰ࠥ⇻").format(mode))
                mode = bstack1111_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭⇼")
            self.bstack1lllll111l1l_opy_ = mode
            self.bstack1llll1ll11ll_opy_ = []
            if source is None:
                self.bstack1llll1ll11ll_opy_ = None
            elif isinstance(source, list):
                self.bstack1llll1ll11ll_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1111_opy_ (u"ࠧ࠯࡬ࡶࡳࡳ࠭⇽")):
                self.bstack1llll1ll11ll_opy_ = self._1lllll11lll1_opy_(source)
            self.__1llllll111l1_opy_()
        except Exception as e:
            logger.error(bstack1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣ࠱ࠥ࡫࡮ࡢࡤ࡯ࡩࡩࡀࠠࡼࡿ࠯ࠤࡲࡵࡤࡦ࠼ࠣࡿࢂ࠲ࠠࡴࡱࡸࡶࡨ࡫࠺ࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ⇾").format(enabled, mode, source, e))
    def bstack1lllll1l111l_opy_(self):
        return self.bstack1lllll1lll11_opy_
    def __1llll1ll1ll1_opy_(self, value):
        self.bstack1lllll1lll11_opy_ = bool(value)
        self.__1llllll111l1_opy_()
    def bstack1lllll11ll1l_opy_(self):
        return self.bstack1lllll11111l_opy_
    def __1lllll1ll11l_opy_(self, value):
        self.bstack1lllll11111l_opy_ = bool(value)
        self.__1llllll111l1_opy_()
    def bstack1lllll11l1ll_opy_(self):
        return self.bstack1lllll1l1ll1_opy_
    def __1llll1lll1ll_opy_(self, value):
        self.bstack1lllll1l1ll1_opy_ = bool(value)
        self.__1llllll111l1_opy_()
    def __1llllll111l1_opy_(self):
        if self.bstack1lllll11l111_opy_:
            self.bstack1lllll1lll11_opy_ = False
            self.bstack1lllll11111l_opy_ = False
            self.bstack1lllll1l1ll1_opy_ = False
            self.bstack1llll1l1ll11_opy_.enable(bstack1llll1l1llll_opy_)
        elif self.bstack1lllll1lll11_opy_:
            self.bstack1lllll11111l_opy_ = False
            self.bstack1lllll1l1ll1_opy_ = False
            self.bstack1lllll11l111_opy_ = False
            self.bstack1llll1l1ll11_opy_.enable(bstack1lllll1111ll_opy_)
        elif self.bstack1lllll11111l_opy_:
            self.bstack1lllll1lll11_opy_ = False
            self.bstack1lllll1l1ll1_opy_ = False
            self.bstack1lllll11l111_opy_ = False
            self.bstack1llll1l1ll11_opy_.enable(bstack1llllll111ll_opy_)
        elif self.bstack1lllll1l1ll1_opy_:
            self.bstack1lllll1lll11_opy_ = False
            self.bstack1lllll11111l_opy_ = False
            self.bstack1lllll11l111_opy_ = False
            self.bstack1llll1l1ll11_opy_.enable(bstack1llll1ll11l1_opy_)
        else:
            self.bstack1llll1l1ll11_opy_.disable()
    def bstack1lll111111_opy_(self):
        return self.bstack1llll1l1ll11_opy_.bstack1llll1ll1l11_opy_()
    def bstack1ll11ll111_opy_(self):
        if self.bstack1llll1l1ll11_opy_.bstack1llll1ll1l11_opy_():
            return self.bstack1llll1l1ll11_opy_.get_name()
        return None
    def _1lllll11lll1_opy_(self, bstack1lllll1l1l11_opy_):
        bstack1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡷࡴࡻࡲࡤࡧࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠡࡣࡱࡨࠥ࡬࡯ࡳ࡯ࡤࡸࠥ࡯ࡴࠡࡨࡲࡶࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡳࡰࡷࡵࡧࡪࡥࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠢࠫࡷࡹࡸࠩ࠻ࠢࡓࡥࡹ࡮ࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡕࡒࡒࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡊࡴࡸ࡭ࡢࡶࡷࡩࡩࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡳࡧࡳࡳࡸ࡯ࡴࡰࡴࡼࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⇿")
        if not os.path.isfile(bstack1lllll1l1l11_opy_):
            logger.error(bstack1111_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࠩࡾࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠣ∀").format(bstack1lllll1l1l11_opy_))
            return []
        data = None
        try:
            with open(bstack1lllll1l1l11_opy_, bstack1111_opy_ (u"ࠦࡷࠨ∁")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡐࡓࡐࡐࠣࡪࡷࡵ࡭ࠡࡵࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ∂").format(bstack1lllll1l1l11_opy_, e))
            return []
        _1lllll1l1l1l_opy_ = None
        _1llllll11111_opy_ = None
        def _1llll1lll1l1_opy_():
            bstack1lllll1l11l1_opy_ = {}
            bstack1llll1l1lll1_opy_ = {}
            try:
                if self.bstack1lllll1l1111_opy_.startswith(bstack1111_opy_ (u"࠭ࡻࠨ∃")) and self.bstack1lllll1l1111_opy_.endswith(bstack1111_opy_ (u"ࠧࡾࠩ∄")):
                    bstack1lllll1l11l1_opy_ = json.loads(self.bstack1lllll1l1111_opy_)
                else:
                    bstack1lllll1l11l1_opy_ = dict(item.split(bstack1111_opy_ (u"ࠨ࠼ࠪ∅")) for item in self.bstack1lllll1l1111_opy_.split(bstack1111_opy_ (u"ࠩ࠯ࠫ∆")) if bstack1111_opy_ (u"ࠪ࠾ࠬ∇") in item) if self.bstack1lllll1l1111_opy_ else {}
                if self.bstack1lllll111111_opy_.startswith(bstack1111_opy_ (u"ࠫࢀ࠭∈")) and self.bstack1lllll111111_opy_.endswith(bstack1111_opy_ (u"ࠬࢃࠧ∉")):
                    bstack1llll1l1lll1_opy_ = json.loads(self.bstack1lllll111111_opy_)
                else:
                    bstack1llll1l1lll1_opy_ = dict(item.split(bstack1111_opy_ (u"࠭࠺ࠨ∊")) for item in self.bstack1lllll111111_opy_.split(bstack1111_opy_ (u"ࠧ࠭ࠩ∋")) if bstack1111_opy_ (u"ࠨ࠼ࠪ∌") in item) if self.bstack1lllll111111_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡩࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡱࡦࡶࡰࡪࡰࡪࡷ࠿ࠦࡻࡾࠤ∍").format(e))
            logger.debug(bstack1111_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠦࡦࡳࡱࡰࠤࡪࡴࡶ࠻ࠢࡾࢁ࠱ࠦࡃࡍࡋ࠽ࠤࢀࢃࠢ∎").format(bstack1lllll1l11l1_opy_, bstack1llll1l1lll1_opy_))
            return bstack1lllll1l11l1_opy_, bstack1llll1l1lll1_opy_
        if _1lllll1l1l1l_opy_ is None or _1llllll11111_opy_ is None:
            _1lllll1l1l1l_opy_, _1llllll11111_opy_ = _1llll1lll1l1_opy_()
        def bstack1lllll1ll1ll_opy_(name, bstack1lllll111l11_opy_):
            if name in _1llllll11111_opy_:
                return _1llllll11111_opy_[name]
            if name in _1lllll1l1l1l_opy_:
                return _1lllll1l1l1l_opy_[name]
            if bstack1lllll111l11_opy_.get(bstack1111_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ∏")):
                return bstack1lllll111l11_opy_[bstack1111_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ∐")]
            return None
        if isinstance(data, dict):
            bstack1llll1lll111_opy_ = []
            bstack1lllll111lll_opy_ = re.compile(bstack1111_opy_ (u"ࡸࠧ࡟࡝ࡄ࠱࡟࠶࠭࠺ࡡࡠ࠯ࠩ࠭∑"))
            for name, bstack1lllll111l11_opy_ in data.items():
                if not isinstance(bstack1lllll111l11_opy_, dict):
                    continue
                url = bstack1lllll111l11_opy_.get(bstack1111_opy_ (u"ࠧࡶࡴ࡯ࠫ−"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1111_opy_ (u"ࠨࠩ∓")):
                    logger.warning(bstack1111_opy_ (u"ࠤࡕࡩࡵࡵࡳࡪࡶࡲࡶࡾࠦࡕࡓࡎࠣ࡭ࡸࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡸࡵࡵࡳࡥࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ∔").format(name, bstack1lllll111l11_opy_))
                    continue
                if not bstack1lllll111lll_opy_.match(name):
                    logger.warning(bstack1111_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡵࡵࡳࡥࡨࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࡨࡲࡶࡲࡧࡴࠡࡨࡲࡶࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ∕").format(name, bstack1lllll111l11_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1111_opy_ (u"ࠦࡘࡵࡵࡳࡥࡨࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࠩࡾࢁࠬࠦ࡭ࡶࡵࡷࠤ࡭ࡧࡶࡦࠢࡤࠤࡱ࡫࡮ࡨࡶ࡫ࠤࡧ࡫ࡴࡸࡧࡨࡲࠥ࠷ࠠࡢࡰࡧࠤ࠸࠶ࠠࡤࡪࡤࡶࡦࡩࡴࡦࡴࡶ࠲ࠧ∖").format(name))
                    continue
                bstack1lllll111l11_opy_ = bstack1lllll111l11_opy_.copy()
                bstack1lllll111l11_opy_[bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ∗")] = name
                bstack1lllll111l11_opy_[bstack1111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭∘")] = bstack1lllll1ll1ll_opy_(name, bstack1lllll111l11_opy_)
                if not bstack1lllll111l11_opy_.get(bstack1111_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧ∙")) or bstack1lllll111l11_opy_.get(bstack1111_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ√")) == bstack1111_opy_ (u"ࠩࠪ∛"):
                    logger.warning(bstack1111_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡳࡵࡴࠡࡵࡳࡩࡨ࡯ࡦࡪࡧࡧࠤ࡫ࡵࡲࠡࡵࡲࡹࡷࡩࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥ∜").format(name, bstack1lllll111l11_opy_))
                    continue
                if bstack1lllll111l11_opy_.get(bstack1111_opy_ (u"ࠫࡧࡧࡳࡦࡄࡵࡥࡳࡩࡨࠨ∝")) and bstack1lllll111l11_opy_[bstack1111_opy_ (u"ࠬࡨࡡࡴࡧࡅࡶࡦࡴࡣࡩࠩ∞")] == bstack1lllll111l11_opy_[bstack1111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭∟")]:
                    logger.warning(bstack1111_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡࡣࡱࡨࠥࡨࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡧࡦࡴ࡮ࡰࡶࠣࡦࡪࠦࡴࡩࡧࠣࡷࡦࡳࡥࠡࡨࡲࡶࠥࡹ࡯ࡶࡴࡦࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ∠").format(name, bstack1lllll111l11_opy_))
                    continue
                bstack1llll1lll111_opy_.append(bstack1lllll111l11_opy_)
            return bstack1llll1lll111_opy_
        return data
    def bstack1lllllll111l_opy_(self):
        data = {
            bstack1111_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ∡"): {
                bstack1111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ∢"): self.bstack1llll1ll1111_opy_(),
                bstack1111_opy_ (u"ࠪࡱࡴࡪࡥࠨ∣"): self.bstack1llll1ll1l1l_opy_(),
                bstack1111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ∤"): self.bstack1lllll11l11l_opy_()
            }
        }
        return data
    def bstack1llll1l1ll1l_opy_(self, config):
        bstack1lllll1lllll_opy_ = {}
        bstack1lllll1lllll_opy_[bstack1111_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫ∥")] = {
            bstack1111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ∦"): self.bstack1llll1ll1111_opy_(),
            bstack1111_opy_ (u"ࠧ࡮ࡱࡧࡩࠬ∧"): self.bstack1llll1ll1l1l_opy_()
        }
        bstack1lllll1lllll_opy_[bstack1111_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟ࡱࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡣ࡫ࡧࡩ࡭ࡧࡧࠫ∨")] = {
            bstack1111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ∩"): self.bstack1lllll11ll1l_opy_()
        }
        bstack1lllll1lllll_opy_[bstack1111_opy_ (u"ࠪࡶࡺࡴ࡟ࡱࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡣ࡫ࡧࡩ࡭ࡧࡧࡣ࡫࡯ࡲࡴࡶࠪ∪")] = {
            bstack1111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ∫"): self.bstack1lllll1l111l_opy_()
        }
        bstack1lllll1lllll_opy_[bstack1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡪࡦ࡯࡬ࡪࡰࡪࡣࡦࡴࡤࡠࡨ࡯ࡥࡰࡿࠧ∬")] = {
            bstack1111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ∭"): self.bstack1lllll11l1ll_opy_()
        }
        if self.bstack11111l11_opy_(config):
            bstack1lllll1lllll_opy_[bstack1111_opy_ (u"ࠧࡳࡧࡷࡶࡾࡥࡴࡦࡵࡷࡷࡤࡵ࡮ࡠࡨࡤ࡭ࡱࡻࡲࡦࠩ∮")] = {
                bstack1111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ∯"): True,
                bstack1111_opy_ (u"ࠩࡰࡥࡽࡥࡲࡦࡶࡵ࡭ࡪࡹࠧ∰"): self.bstack1ll11111ll_opy_(config)
            }
        if self.bstack111l1l11111_opy_(config):
            bstack1lllll1lllll_opy_[bstack1111_opy_ (u"ࠪࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡱࡱࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠬ∱")] = {
                bstack1111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ∲"): True,
                bstack1111_opy_ (u"ࠬࡳࡡࡹࡡࡩࡥ࡮ࡲࡵࡳࡧࡶࠫ∳"): self.bstack111l1l11lll_opy_(config)
            }
        return bstack1lllll1lllll_opy_
    def bstack1lll11ll_opy_(self, config):
        bstack1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡴࡲ࡬ࡦࡥࡷࡷࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡥࡽࠥࡳࡡ࡬࡫ࡱ࡫ࠥࡧࠠࡤࡣ࡯ࡰࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩ࡛ࠥࡕࡊࡆࠣࡳ࡫ࠦࡴࡩࡧࠣࡦࡺ࡯࡬ࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ∴")
        if not (config.get(bstack1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ∵"), None) in bstack111ll111lll_opy_ and self.bstack1llll1ll1111_opy_()):
            return None
        bstack1llll1ll1lll_opy_ = os.environ.get(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭∶"), None)
        logger.debug(bstack1111_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡄࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨ∷").format(bstack1llll1ll1lll_opy_))
        try:
            bstack111llll11l1_opy_ = bstack1111_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠣ∸").format(bstack1llll1ll1lll_opy_)
            payload = {
                bstack1111_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤ∹"): config.get(bstack1111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ∺"), bstack1111_opy_ (u"࠭ࠧ∻")),
                bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥ∼"): config.get(bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ∽"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ∾"): os.environ.get(bstack1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠤ∿"), bstack1111_opy_ (u"ࠦࠧ≀")),
                bstack1111_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣ≁"): int(os.environ.get(bstack1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤ≂")) or bstack1111_opy_ (u"ࠢ࠱ࠤ≃")),
                bstack1111_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧ≄"): int(os.environ.get(bstack1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦ≅")) or bstack1111_opy_ (u"ࠥ࠵ࠧ≆")),
                bstack1111_opy_ (u"ࠦ࡭ࡵࡳࡵࡋࡱࡪࡴࠨ≇"): get_host_info(),
            }
            logger.debug(bstack1111_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡲࡤࡽࡱࡵࡡࡥ࠼ࠣࡿࢂࠨ≈").format(payload))
            response = bstack111lll1lll1_opy_.bstack1lllll1l1lll_opy_(bstack111llll11l1_opy_, payload)
            if response:
                logger.debug(bstack1111_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡇࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ≉").format(response))
                return response
            else:
                logger.error(bstack1111_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊ࠺ࠡࡽࢀࠦ≊").format(bstack1llll1ll1lll_opy_))
                return None
        except Exception as e:
            logger.error(bstack1111_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊࠠࡼࡿ࠽ࠤࢀࢃࠢ≋").format(bstack1llll1ll1lll_opy_, e))
            return None