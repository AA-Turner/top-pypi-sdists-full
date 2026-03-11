# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack1l1lllll1_opy_, bstack1111l111l11_opy_
from bstack_utils.helper import bstack111l11l111l_opy_, get_host_info
from bstack_utils.bstack11111l11l11_opy_ import bstack111111ll111_opy_
import json
import re
import sys
bstack1111111lll1_opy_ = bstack1ll111_opy_ (u"ࠣࡴࡨࡸࡷࡿࡔࡦࡵࡷࡷࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢ᳽")
bstack11111ll1lll_opy_ = bstack1ll111_opy_ (u"ࠤࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣ᳾")
bstack1111111l1l1_opy_ = bstack1ll111_opy_ (u"ࠥࡶࡺࡴࡐࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡉࡥ࡮ࡲࡥࡥࡈ࡬ࡶࡸࡺࠢ᳿")
bstack1111l11111l_opy_ = bstack1ll111_opy_ (u"ࠦࡷ࡫ࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࠧᴀ")
bstack11111l1lll1_opy_ = bstack1ll111_opy_ (u"ࠧࡹ࡫ࡪࡲࡉࡰࡦࡱࡹࡢࡰࡧࡊࡦ࡯࡬ࡦࡦࠥᴁ")
bstack111111l111l_opy_ = bstack1ll111_opy_ (u"ࠨࡲࡶࡰࡖࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࠥᴂ")
bstack1111111ll11_opy_ = {
    bstack1111111lll1_opy_,
    bstack11111ll1lll_opy_,
    bstack1111111l1l1_opy_,
    bstack1111l11111l_opy_,
    bstack11111l1lll1_opy_,
    bstack111111l111l_opy_
}
bstack11111lll1l1_opy_ = {bstack1ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᴃ")}
logger = logger_utils.get_logger(__name__, bstack1l1lllll1_opy_)
class bstack111111llll1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1111111l11l_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l1ll111l_opy_:
    _1ll1111llll_opy_ = None
    def __init__(self, config):
        self.bstack11111lll1ll_opy_ = False
        self.bstack11111l1l11l_opy_ = False
        self.bstack11111ll11ll_opy_ = False
        self.bstack11111l111l1_opy_ = False
        self.bstack11111l11ll1_opy_ = None
        self.bstack111111lll1l_opy_ = bstack111111llll1_opy_()
        self.bstack11111l1ll11_opy_ = None
        opts = config.get(bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᴄ"), {})
        self.bstack111111ll11l_opy_ = config.get(bstack1ll111_opy_ (u"ࠩࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡉࡓ࡜ࠧᴅ"), bstack1ll111_opy_ (u"ࠥࠦᴆ"))
        self.bstack111111l1111_opy_ = config.get(bstack1ll111_opy_ (u"ࠫࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡉࡌࡊࠩᴇ"), bstack1ll111_opy_ (u"ࠧࠨᴈ"))
        bstack111111l1l11_opy_ = opts.get(bstack111111l111l_opy_, {})
        bstack11111111l11_opy_ = None
        if bstack1ll111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᴉ") in bstack111111l1l11_opy_:
            bstack111111l11ll_opy_ = bstack111111l1l11_opy_[bstack1ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᴊ")]
            if bstack111111l11ll_opy_ is None or (isinstance(bstack111111l11ll_opy_, str) and bstack111111l11ll_opy_.strip() == bstack1ll111_opy_ (u"ࠨࠩᴋ")) or (isinstance(bstack111111l11ll_opy_, list) and len(bstack111111l11ll_opy_) == 0):
                bstack11111111l11_opy_ = []
            elif isinstance(bstack111111l11ll_opy_, list):
                bstack11111111l11_opy_ = bstack111111l11ll_opy_
            elif isinstance(bstack111111l11ll_opy_, str) and bstack111111l11ll_opy_.strip():
                bstack11111111l11_opy_ = bstack111111l11ll_opy_
            else:
                logger.warning(bstack1ll111_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡷࡴࡻࡲࡤࡧࠣࡺࡦࡲࡵࡦࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾ࠰ࠣࡈࡪ࡬ࡡࡶ࡮ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡩࡲࡶࡴࡺࠢ࡯࡭ࡸࡺ࠮ࠣᴌ").format(bstack111111l11ll_opy_))
                bstack11111111l11_opy_ = []
        self.__111111l1ll1_opy_(
            bstack111111l1l11_opy_.get(bstack1ll111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫᴍ"), False),
            bstack111111l1l11_opy_.get(bstack1ll111_opy_ (u"ࠫࡲࡵࡤࡦࠩᴎ"), bstack1ll111_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬᴏ")),
            bstack11111111l11_opy_
        )
        self.__1111l111111_opy_(opts.get(bstack1111111l1l1_opy_, False))
        self.__111111ll1ll_opy_(opts.get(bstack1111l11111l_opy_, False))
        self.__1111111l1ll_opy_(opts.get(bstack11111l1lll1_opy_, False))
    @classmethod
    def get_instance(cls, config=None):
        if cls._1ll1111llll_opy_ is None and config is not None:
            cls._1ll1111llll_opy_ = bstack1l1ll111l_opy_(config)
        return cls._1ll1111llll_opy_
    @staticmethod
    def bstack1lll11l11_opy_(config: dict) -> bool:
        bstack11111111ll1_opy_ = config.get(bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᴐ"), {}).get(bstack1111111lll1_opy_, {})
        return bstack11111111ll1_opy_.get(bstack1ll111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨᴑ"), False)
    @staticmethod
    def bstack1l1l11ll1l_opy_(config: dict) -> int:
        bstack11111111ll1_opy_ = config.get(bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᴒ"), {}).get(bstack1111111lll1_opy_, {})
        retries = 0
        if bstack1l1ll111l_opy_.bstack1lll11l11_opy_(config):
            retries = bstack11111111ll1_opy_.get(bstack1ll111_opy_ (u"ࠩࡰࡥࡽࡘࡥࡵࡴ࡬ࡩࡸ࠭ᴓ"), 1)
        return retries
    @staticmethod
    def bstack11lll1l1ll_opy_(config: dict) -> dict:
        bstack11111llll1l_opy_ = config.get(bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧᴔ"), {})
        return {
            key: value for key, value in bstack11111llll1l_opy_.items() if key in bstack1111111ll11_opy_
        }
    @staticmethod
    def bstack11111l1l1l1_opy_():
        bstack1ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᴕ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠧࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡿࢂࠨᴖ").format(os.getenv(bstack1ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦᴗ")))))
    @staticmethod
    def bstack11111l1llll_opy_(test_name: str):
        bstack1ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᴘ")
        bstack11111ll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡼࡿ࠱ࡸࡽࡺࠢᴙ").format(os.getenv(bstack1ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢᴚ"))))
        with open(bstack11111ll1l1l_opy_, bstack1ll111_opy_ (u"ࠪࡥࠬᴛ")) as file:
            file.write(bstack1ll111_opy_ (u"ࠦࢀࢃ࡜࡯ࠤᴜ").format(test_name))
    @staticmethod
    def bstack11111l1111l_opy_(framework: str) -> bool:
       return framework.lower() in bstack11111lll1l1_opy_
    @staticmethod
    def bstack11111ll1l11_opy_(config: dict) -> bool:
        bstack111111l1lll_opy_ = config.get(bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴝ"), {}).get(bstack11111ll1lll_opy_, {})
        return bstack111111l1lll_opy_.get(bstack1ll111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧᴞ"), False)
    @staticmethod
    def bstack11111111l1l_opy_(config: dict, bstack11111111lll_opy_: int = 0) -> int:
        bstack1ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥ࠮ࠣࡻ࡭࡯ࡣࡩࠢࡦࡥࡳࠦࡢࡦࠢࡤࡲࠥࡧࡢࡴࡱ࡯ࡹࡹ࡫ࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡴࠣࡥࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧࠡࠪࡧ࡭ࡨࡺࠩ࠻ࠢࡗ࡬ࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡳࡹࡧ࡬ࡠࡶࡨࡷࡹࡹࠠࠩ࡫ࡱࡸ࠮ࡀࠠࡕࡪࡨࠤࡹࡵࡴࡢ࡮ࠣࡲࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥ࠮ࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠮࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸ࠿ࠦࡔࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᴟ")
        bstack111111l1lll_opy_ = config.get(bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᴠ"), {}).get(bstack1ll111_opy_ (u"ࠩࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠨᴡ"), {})
        bstack11111ll111l_opy_ = 0
        bstack11111l1ll1l_opy_ = 0
        if bstack1l1ll111l_opy_.bstack11111ll1l11_opy_(config):
            bstack11111l1ll1l_opy_ = bstack111111l1lll_opy_.get(bstack1ll111_opy_ (u"ࠪࡱࡦࡾࡆࡢ࡫࡯ࡹࡷ࡫ࡳࠨᴢ"), 5)
            if isinstance(bstack11111l1ll1l_opy_, str) and bstack11111l1ll1l_opy_.endswith(bstack1ll111_opy_ (u"ࠫࠪ࠭ᴣ")):
                try:
                    percentage = int(bstack11111l1ll1l_opy_.strip(bstack1ll111_opy_ (u"ࠬࠫࠧᴤ")))
                    if bstack11111111lll_opy_ > 0:
                        bstack11111ll111l_opy_ = math.ceil((percentage * bstack11111111lll_opy_) / 100)
                    else:
                        raise ValueError(bstack1ll111_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡲࡻࡳࡵࠢࡥࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠲ࠧᴥ"))
                except ValueError as e:
                    raise ValueError(bstack1ll111_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡵࡲࠡ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸࡀࠠࡼࡿࠥᴦ").format(bstack11111l1ll1l_opy_)) from e
            else:
                bstack11111ll111l_opy_ = int(bstack11111l1ll1l_opy_)
        logger.info(bstack1ll111_opy_ (u"ࠣࡏࡤࡼࠥ࡬ࡡࡪ࡮ࡸࡶࡪࡹࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡷࡪࡺࠠࡵࡱ࠽ࠤࢀࢃࠠࠩࡨࡵࡳࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿࠬࠦᴧ").format(bstack11111ll111l_opy_, bstack11111l1ll1l_opy_))
        return bstack11111ll111l_opy_
    def bstack1111111llll_opy_(self):
        return self.bstack11111l111l1_opy_
    def bstack111111l11l1_opy_(self):
        return self.bstack11111l11ll1_opy_
    def bstack111111lll11_opy_(self):
        return self.bstack11111l1ll11_opy_
    def __111111l1ll1_opy_(self, enabled, mode, source=None):
        try:
            self.bstack11111l111l1_opy_ = bool(enabled)
            if mode not in [bstack1ll111_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡊ࡮ࡸࡳࡵࠩᴨ"), bstack1ll111_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡔࡴ࡬ࡺࠩᴩ")]:
                logger.warning(bstack1ll111_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠ࡮ࡱࡧࡩࠥ࠭ࡻࡾࠩࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡈ࡬ࡶࡸࡺࠧ࠯ࠤᴪ").format(mode))
                mode = bstack1ll111_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬᴫ")
            self.bstack11111l11ll1_opy_ = mode
            self.bstack11111l1ll11_opy_ = []
            if source is None:
                self.bstack11111l1ll11_opy_ = None
            elif isinstance(source, list):
                self.bstack11111l1ll11_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1ll111_opy_ (u"࠭࠮࡫ࡵࡲࡲࠬᴬ")):
                self.bstack11111l1ll11_opy_ = self._11111lllll1_opy_(source)
            self.__11111llll11_opy_()
        except Exception as e:
            logger.error(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢ࠰ࠤࡪࡴࡡࡣ࡮ࡨࡨ࠿ࠦࡻࡾ࠮ࠣࡱࡴࡪࡥ࠻ࠢࡾࢁ࠱ࠦࡳࡰࡷࡵࡧࡪࡀࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᴭ").format(enabled, mode, source, e))
    def bstack111111ll1l1_opy_(self):
        return self.bstack11111lll1ll_opy_
    def __1111l111111_opy_(self, value):
        self.bstack11111lll1ll_opy_ = bool(value)
        self.__11111llll11_opy_()
    def bstack1111l1111l1_opy_(self):
        return self.bstack11111l1l11l_opy_
    def __111111ll1ll_opy_(self, value):
        self.bstack11111l1l11l_opy_ = bool(value)
        self.__11111llll11_opy_()
    def bstack1111111l111_opy_(self):
        return self.bstack11111ll11ll_opy_
    def __1111111l1ll_opy_(self, value):
        self.bstack11111ll11ll_opy_ = bool(value)
        self.__11111llll11_opy_()
    def __11111llll11_opy_(self):
        if self.bstack11111l111l1_opy_:
            self.bstack11111lll1ll_opy_ = False
            self.bstack11111l1l11l_opy_ = False
            self.bstack11111ll11ll_opy_ = False
            self.bstack111111lll1l_opy_.enable(bstack111111l111l_opy_)
        elif self.bstack11111lll1ll_opy_:
            self.bstack11111l1l11l_opy_ = False
            self.bstack11111ll11ll_opy_ = False
            self.bstack11111l111l1_opy_ = False
            self.bstack111111lll1l_opy_.enable(bstack1111111l1l1_opy_)
        elif self.bstack11111l1l11l_opy_:
            self.bstack11111lll1ll_opy_ = False
            self.bstack11111ll11ll_opy_ = False
            self.bstack11111l111l1_opy_ = False
            self.bstack111111lll1l_opy_.enable(bstack1111l11111l_opy_)
        elif self.bstack11111ll11ll_opy_:
            self.bstack11111lll1ll_opy_ = False
            self.bstack11111l1l11l_opy_ = False
            self.bstack11111l111l1_opy_ = False
            self.bstack111111lll1l_opy_.enable(bstack11111l1lll1_opy_)
        else:
            self.bstack111111lll1l_opy_.disable()
    def bstack11l1ll11ll_opy_(self):
        return self.bstack111111lll1l_opy_.bstack1111111l11l_opy_()
    def bstack1111lll1l1_opy_(self):
        if self.bstack111111lll1l_opy_.bstack1111111l11l_opy_():
            return self.bstack111111lll1l_opy_.get_name()
        return None
    def _11111lllll1_opy_(self, bstack11111l111ll_opy_):
        bstack1ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡶࡳࡺࡸࡣࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠠࡢࡰࡧࠤ࡫ࡵࡲ࡮ࡣࡷࠤ࡮ࡺࠠࡧࡱࡵࠤࡸࡳࡡࡳࡶࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡹ࡯ࡶࡴࡦࡩࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠡࠪࡶࡸࡷ࠯࠺ࠡࡒࡤࡸ࡭ࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡔࡑࡑࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡰ࡮ࡹࡴ࠻ࠢࡉࡳࡷࡳࡡࡵࡶࡨࡨࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡲࡦࡲࡲࡷ࡮ࡺ࡯ࡳࡻࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᴮ")
        if not os.path.isfile(bstack11111l111ll_opy_):
            logger.error(bstack1ll111_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࠨࡽࢀࠫࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠢᴯ").format(bstack11111l111ll_opy_))
            return []
        data = None
        try:
            with open(bstack11111l111ll_opy_, bstack1ll111_opy_ (u"ࠥࡶࠧᴰ")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤࡏ࡙ࡏࡏࠢࡩࡶࡴࡳࠠࡴࡱࡸࡶࡨ࡫ࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢᴱ").format(bstack11111l111ll_opy_, e))
            return []
        _11111ll11l1_opy_ = None
        _11111l1l111_opy_ = None
        def _111111lllll_opy_():
            bstack11111l1l1ll_opy_ = {}
            bstack111111l1l1l_opy_ = {}
            try:
                if self.bstack111111ll11l_opy_.startswith(bstack1ll111_opy_ (u"ࠬࢁࠧᴲ")) and self.bstack111111ll11l_opy_.endswith(bstack1ll111_opy_ (u"࠭ࡽࠨᴳ")):
                    bstack11111l1l1ll_opy_ = json.loads(self.bstack111111ll11l_opy_)
                else:
                    bstack11111l1l1ll_opy_ = dict(item.split(bstack1ll111_opy_ (u"ࠧ࠻ࠩᴴ")) for item in self.bstack111111ll11l_opy_.split(bstack1ll111_opy_ (u"ࠨ࠮ࠪᴵ")) if bstack1ll111_opy_ (u"ࠩ࠽ࠫᴶ") in item) if self.bstack111111ll11l_opy_ else {}
                if self.bstack111111l1111_opy_.startswith(bstack1ll111_opy_ (u"ࠪࡿࠬᴷ")) and self.bstack111111l1111_opy_.endswith(bstack1ll111_opy_ (u"ࠫࢂ࠭ᴸ")):
                    bstack111111l1l1l_opy_ = json.loads(self.bstack111111l1111_opy_)
                else:
                    bstack111111l1l1l_opy_ = dict(item.split(bstack1ll111_opy_ (u"ࠬࡀࠧᴹ")) for item in self.bstack111111l1111_opy_.split(bstack1ll111_opy_ (u"࠭ࠬࠨᴺ")) if bstack1ll111_opy_ (u"ࠧ࠻ࠩᴻ") in item) if self.bstack111111l1111_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡨࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡰࡥࡵࡶࡩ࡯ࡩࡶ࠾ࠥࢁࡽࠣᴼ").format(e))
            logger.debug(bstack1ll111_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡱࡦࡶࡰࡪࡰࡪࡷࠥ࡬ࡲࡰ࡯ࠣࡩࡳࡼ࠺ࠡࡽࢀ࠰ࠥࡉࡌࡊ࠼ࠣࡿࢂࠨᴽ").format(bstack11111l1l1ll_opy_, bstack111111l1l1l_opy_))
            return bstack11111l1l1ll_opy_, bstack111111l1l1l_opy_
        if _11111ll11l1_opy_ is None or _11111l1l111_opy_ is None:
            _11111ll11l1_opy_, _11111l1l111_opy_ = _111111lllll_opy_()
        def bstack11111l11111_opy_(name, bstack11111l11lll_opy_):
            if name in _11111l1l111_opy_:
                return _11111l1l111_opy_[name]
            if name in _11111ll11l1_opy_:
                return _11111ll11l1_opy_[name]
            if bstack11111l11lll_opy_.get(bstack1ll111_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪᴾ")):
                return bstack11111l11lll_opy_[bstack1ll111_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫᴿ")]
            return None
        if isinstance(data, dict):
            bstack11111ll1111_opy_ = []
            bstack11111lll111_opy_ = re.compile(bstack1ll111_opy_ (u"ࡷ࠭࡞࡜ࡃ࠰࡞࠵࠳࠹ࡠ࡟࠮ࠨࠬᵀ"))
            for name, bstack11111l11lll_opy_ in data.items():
                if not isinstance(bstack11111l11lll_opy_, dict):
                    continue
                url = bstack11111l11lll_opy_.get(bstack1ll111_opy_ (u"࠭ࡵࡳ࡮ࠪᵁ"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1ll111_opy_ (u"ࠧࠨᵂ")):
                    logger.warning(bstack1ll111_opy_ (u"ࠣࡔࡨࡴࡴࡹࡩࡵࡱࡵࡽ࡛ࠥࡒࡍࠢ࡬ࡷࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧᵃ").format(name, bstack11111l11lll_opy_))
                    continue
                if not bstack11111lll111_opy_.match(name):
                    logger.warning(bstack1ll111_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡷࡴࡻࡲࡤࡧࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࡧࡱࡵࡱࡦࡺࠠࡧࡱࡵࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨᵄ").format(name, bstack11111l11lll_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1ll111_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࠨࡽࢀࠫࠥࡳࡵࡴࡶࠣ࡬ࡦࡼࡥࠡࡣࠣࡰࡪࡴࡧࡵࡪࠣࡦࡪࡺࡷࡦࡧࡱࠤ࠶ࠦࡡ࡯ࡦࠣ࠷࠵ࠦࡣࡩࡣࡵࡥࡨࡺࡥࡳࡵ࠱ࠦᵅ").format(name))
                    continue
                bstack11111l11lll_opy_ = bstack11111l11lll_opy_.copy()
                bstack11111l11lll_opy_[bstack1ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᵆ")] = name
                bstack11111l11lll_opy_[bstack1ll111_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬᵇ")] = bstack11111l11111_opy_(name, bstack11111l11lll_opy_)
                if not bstack11111l11lll_opy_.get(bstack1ll111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭ᵈ")) or bstack11111l11lll_opy_.get(bstack1ll111_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧᵉ")) == bstack1ll111_opy_ (u"ࠨࠩᵊ"):
                    logger.warning(bstack1ll111_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡲࡴࡺࠠࡴࡲࡨࡧ࡮࡬ࡩࡦࡦࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤᵋ").format(name, bstack11111l11lll_opy_))
                    continue
                if bstack11111l11lll_opy_.get(bstack1ll111_opy_ (u"ࠪࡦࡦࡹࡥࡃࡴࡤࡲࡨ࡮ࠧᵌ")) and bstack11111l11lll_opy_[bstack1ll111_opy_ (u"ࠫࡧࡧࡳࡦࡄࡵࡥࡳࡩࡨࠨᵍ")] == bstack11111l11lll_opy_[bstack1ll111_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬᵎ")]:
                    logger.warning(bstack1ll111_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡢࡰࡧࠤࡧࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡺࡨࡦࠢࡶࡥࡲ࡫ࠠࡧࡱࡵࠤࡸࡵࡵࡳࡥࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨᵏ").format(name, bstack11111l11lll_opy_))
                    continue
                bstack11111ll1111_opy_.append(bstack11111l11lll_opy_)
            return bstack11111ll1111_opy_
        return data
    def bstack1111l11l11l_opy_(self):
        data = {
            bstack1ll111_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭ᵐ"): {
                bstack1ll111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩᵑ"): self.bstack1111111llll_opy_(),
                bstack1ll111_opy_ (u"ࠩࡰࡳࡩ࡫ࠧᵒ"): self.bstack111111l11l1_opy_(),
                bstack1ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᵓ"): self.bstack111111lll11_opy_()
            }
        }
        return data
    def bstack11111l11l1l_opy_(self, config):
        bstack11111ll1ll1_opy_ = {}
        bstack11111ll1ll1_opy_[bstack1ll111_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪᵔ")] = {
            bstack1ll111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ᵕ"): self.bstack1111111llll_opy_(),
            bstack1ll111_opy_ (u"࠭࡭ࡰࡦࡨࠫᵖ"): self.bstack111111l11l1_opy_()
        }
        bstack11111ll1ll1_opy_[bstack1ll111_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࠪᵗ")] = {
            bstack1ll111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩᵘ"): self.bstack1111l1111l1_opy_()
        }
        bstack11111ll1ll1_opy_[bstack1ll111_opy_ (u"ࠩࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࡢࡪ࡮ࡸࡳࡵࠩᵙ")] = {
            bstack1ll111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫᵚ"): self.bstack111111ll1l1_opy_()
        }
        bstack11111ll1ll1_opy_[bstack1ll111_opy_ (u"ࠫࡸࡱࡩࡱࡡࡩࡥ࡮ࡲࡩ࡯ࡩࡢࡥࡳࡪ࡟ࡧ࡮ࡤ࡯ࡾ࠭ᵛ")] = {
            bstack1ll111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ᵜ"): self.bstack1111111l111_opy_()
        }
        if self.bstack1lll11l11_opy_(config):
            bstack11111ll1ll1_opy_[bstack1ll111_opy_ (u"࠭ࡲࡦࡶࡵࡽࡤࡺࡥࡴࡶࡶࡣࡴࡴ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠨᵝ")] = {
                bstack1ll111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨᵞ"): True,
                bstack1ll111_opy_ (u"ࠨ࡯ࡤࡼࡤࡸࡥࡵࡴ࡬ࡩࡸ࠭ᵟ"): self.bstack1l1l11ll1l_opy_(config)
            }
        if self.bstack11111ll1l11_opy_(config):
            bstack11111ll1ll1_opy_[bstack1ll111_opy_ (u"ࠩࡤࡦࡴࡸࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡰࡰࡢࡪࡦ࡯࡬ࡶࡴࡨࠫᵠ")] = {
                bstack1ll111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫᵡ"): True,
                bstack1ll111_opy_ (u"ࠫࡲࡧࡸࡠࡨࡤ࡭ࡱࡻࡲࡦࡵࠪᵢ"): self.bstack11111111l1l_opy_(config)
            }
        return bstack11111ll1ll1_opy_
    def bstack11l111ll1_opy_(self, config):
        bstack1ll111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡳࡱࡲࡥࡤࡶࡶࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡤࡼࠤࡲࡧ࡫ࡪࡰࡪࠤࡦࠦࡣࡢ࡮࡯ࠤࡹࡵࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠠࠩࡵࡷࡶ࠮ࡀࠠࡕࡪࡨࠤ࡚࡛ࡉࡅࠢࡲࡪࠥࡺࡨࡦࠢࡥࡹ࡮ࡲࡤࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠱ࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠠࡪࡨࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᵣ")
        if not (config.get(bstack1ll111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᵤ"), None) in bstack1111l111l11_opy_ and self.bstack1111111llll_opy_()):
            return None
        bstack1111111ll1l_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᵥ"), None)
        logger.debug(bstack1ll111_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡃࡰ࡮࡯ࡩࡨࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦ࡙࡚ࠣࡏࡄ࠻ࠢࡾࢁࠧᵦ").format(bstack1111111ll1l_opy_))
        try:
            bstack11111llllll_opy_ = bstack1ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠢᵧ").format(bstack1111111ll1l_opy_)
            payload = {
                bstack1ll111_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣᵨ"): config.get(bstack1ll111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᵩ"), bstack1ll111_opy_ (u"ࠬ࠭ᵪ")),
                bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤᵫ"): config.get(bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᵬ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨᵭ"): os.environ.get(bstack1ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠣᵮ"), bstack1ll111_opy_ (u"ࠥࠦᵯ")),
                bstack1ll111_opy_ (u"ࠦࡳࡵࡤࡦࡋࡱࡨࡪࡾࠢᵰ"): int(os.environ.get(bstack1ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣᵱ")) or bstack1ll111_opy_ (u"ࠨ࠰ࠣᵲ")),
                bstack1ll111_opy_ (u"ࠢࡵࡱࡷࡥࡱࡔ࡯ࡥࡧࡶࠦᵳ"): int(os.environ.get(bstack1ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡑࡗࡅࡑࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥᵴ")) or bstack1ll111_opy_ (u"ࠤ࠴ࠦᵵ")),
                bstack1ll111_opy_ (u"ࠥ࡬ࡴࡹࡴࡊࡰࡩࡳࠧᵶ"): get_host_info(),
            }
            logger.debug(bstack1ll111_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡱࡣࡼࡰࡴࡧࡤ࠻ࠢࡾࢁࠧᵷ").format(payload))
            response = bstack111111ll111_opy_.bstack11111lll11l_opy_(bstack11111llllll_opy_, payload)
            if response:
                logger.debug(bstack1ll111_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡆࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥᵸ").format(response))
                return response
            else:
                logger.error(bstack1ll111_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࡀࠠࡼࡿࠥᵹ").format(bstack1111111ll1l_opy_))
                return None
        except Exception as e:
            logger.error(bstack1ll111_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࠦࡻࡾ࠼ࠣࡿࢂࠨᵺ").format(bstack1111111ll1l_opy_, e))
            return None