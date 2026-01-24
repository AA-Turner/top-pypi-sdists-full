# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import tempfile
import math
from bstack_utils import bstack111llll1ll_opy_
from bstack_utils.constants import bstack1lllll11_opy_, bstack11l1111llll_opy_
from bstack_utils.helper import bstack111ll1l1l1l_opy_, get_host_info
from bstack_utils.bstack11l11lllll1_opy_ import bstack11l11lll11l_opy_
import json
import re
import sys
bstack111111l1l1l_opy_ = bstack1l1111_opy_ (u"ࠦࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠥᾧ")
bstack111111l1lll_opy_ = bstack1l1111_opy_ (u"ࠧࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦᾨ")
bstack11111l11111_opy_ = bstack1l1111_opy_ (u"ࠨࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࡋ࡯ࡲࡴࡶࠥᾩ")
bstack11111ll11l1_opy_ = bstack1l1111_opy_ (u"ࠢࡳࡧࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࠣᾪ")
bstack1lllllllllll_opy_ = bstack1l1111_opy_ (u"ࠣࡵ࡮࡭ࡵࡌ࡬ࡢ࡭ࡼࡥࡳࡪࡆࡢ࡫࡯ࡩࡩࠨᾫ")
bstack11111l11l11_opy_ = bstack1l1111_opy_ (u"ࠤࡵࡹࡳ࡙࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࠨᾬ")
bstack1111111ll11_opy_ = {
    bstack111111l1l1l_opy_,
    bstack111111l1lll_opy_,
    bstack11111l11111_opy_,
    bstack11111ll11l1_opy_,
    bstack1lllllllllll_opy_,
    bstack11111l11l11_opy_
}
bstack1111111111l_opy_ = {bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᾭ")}
logger = bstack111llll1ll_opy_.get_logger(__name__, bstack1lllll11_opy_)
class bstack111111ll111_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1111111l1l1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l1llll1l_opy_:
    _1ll1ll1l11l_opy_ = None
    def __init__(self, config):
        self.bstack11111l1111l_opy_ = False
        self.bstack111111lll1l_opy_ = False
        self.bstack1lllllllll1l_opy_ = False
        self.bstack111111l1ll1_opy_ = False
        self.bstack11111l11lll_opy_ = None
        self.bstack111111l1l11_opy_ = bstack111111ll111_opy_()
        self.bstack11111l1llll_opy_ = None
        opts = config.get(bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᾮ"), {})
        self.bstack111111ll1l1_opy_ = config.get(bstack1l1111_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡅࡏࡘࠪᾯ"), bstack1l1111_opy_ (u"ࠨࠢᾰ"))
        self.bstack11111l1l1ll_opy_ = config.get(bstack1l1111_opy_ (u"ࠧࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࡅࡏࡍࠬᾱ"), bstack1l1111_opy_ (u"ࠣࠤᾲ"))
        bstack1111111ll1l_opy_ = opts.get(bstack11111l11l11_opy_, {})
        bstack11111l11ll1_opy_ = None
        if bstack1l1111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᾳ") in bstack1111111ll1l_opy_:
            bstack1111111l1ll_opy_ = bstack1111111ll1l_opy_[bstack1l1111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᾴ")]
            if bstack1111111l1ll_opy_ is None or (isinstance(bstack1111111l1ll_opy_, str) and bstack1111111l1ll_opy_.strip() == bstack1l1111_opy_ (u"ࠫࠬ᾵")) or (isinstance(bstack1111111l1ll_opy_, list) and len(bstack1111111l1ll_opy_) == 0):
                bstack11111l11ll1_opy_ = []
            elif isinstance(bstack1111111l1ll_opy_, list):
                bstack11111l11ll1_opy_ = bstack1111111l1ll_opy_
            elif isinstance(bstack1111111l1ll_opy_, str) and bstack1111111l1ll_opy_.strip():
                bstack11111l11ll1_opy_ = bstack1111111l1ll_opy_
            else:
                logger.warning(bstack1l1111_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡶࡢ࡮ࡸࡩࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡾࢁ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࡥ࡮ࡲࡷࡽࠥࡲࡩࡴࡶ࠱ࠦᾶ").format(bstack1111111l1ll_opy_))
                bstack11111l11ll1_opy_ = []
        self.__111111lll11_opy_(
            bstack1111111ll1l_opy_.get(bstack1l1111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧᾷ"), False),
            bstack1111111ll1l_opy_.get(bstack1l1111_opy_ (u"ࠧ࡮ࡱࡧࡩࠬᾸ"), bstack1l1111_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨᾹ")),
            bstack11111l11ll1_opy_
        )
        self.__11111ll1111_opy_(opts.get(bstack11111l11111_opy_, False))
        self.__111111l11ll_opy_(opts.get(bstack11111ll11l1_opy_, False))
        self.__11111l11l1l_opy_(opts.get(bstack1lllllllllll_opy_, False))
    @classmethod
    def bstack111ll1lll1_opy_(cls, config=None):
        if cls._1ll1ll1l11l_opy_ is None and config is not None:
            cls._1ll1ll1l11l_opy_ = bstack1l1llll1l_opy_(config)
        return cls._1ll1ll1l11l_opy_
    @staticmethod
    def bstack1lllll1l1l_opy_(config: dict) -> bool:
        bstack111111l1111_opy_ = config.get(bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭Ὰ"), {}).get(bstack111111l1l1l_opy_, {})
        return bstack111111l1111_opy_.get(bstack1l1111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫΆ"), False)
    @staticmethod
    def bstack1llll111l_opy_(config: dict) -> int:
        bstack111111l1111_opy_ = config.get(bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᾼ"), {}).get(bstack111111l1l1l_opy_, {})
        retries = 0
        if bstack1l1llll1l_opy_.bstack1lllll1l1l_opy_(config):
            retries = bstack111111l1111_opy_.get(bstack1l1111_opy_ (u"ࠬࡳࡡࡹࡔࡨࡸࡷ࡯ࡥࡴࠩ᾽"), 1)
        return retries
    @staticmethod
    def bstack1ll1ll1l1l_opy_(config: dict) -> dict:
        bstack11111111lll_opy_ = config.get(bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪι"), {})
        return {
            key: value for key, value in bstack11111111lll_opy_.items() if key in bstack1111111ll11_opy_
        }
    @staticmethod
    def bstack111111111l1_opy_():
        bstack1l1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ᾿")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤ῀").format(os.getenv(bstack1l1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ῁")))))
    @staticmethod
    def bstack1111111llll_opy_(test_name: str):
        bstack1l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢῂ")
        bstack11111111l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶࠥῃ").format(os.getenv(bstack1l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥῄ"))))
        with open(bstack11111111l11_opy_, bstack1l1111_opy_ (u"࠭ࡡࠨ῅")) as file:
            file.write(bstack1l1111_opy_ (u"ࠢࡼࡿ࡟ࡲࠧῆ").format(test_name))
    @staticmethod
    def bstack11111l111ll_opy_(framework: str) -> bool:
       return framework.lower() in bstack1111111111l_opy_
    @staticmethod
    def bstack111lll1llll_opy_(config: dict) -> bool:
        bstack1111111lll1_opy_ = config.get(bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬῇ"), {}).get(bstack111111l1lll_opy_, {})
        return bstack1111111lll1_opy_.get(bstack1l1111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪῈ"), False)
    @staticmethod
    def bstack111lllll111_opy_(config: dict, bstack111llll1ll1_opy_: int = 0) -> int:
        bstack1l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠱ࠦࡷࡩ࡫ࡦ࡬ࠥࡩࡡ࡯ࠢࡥࡩࠥࡧ࡮ࠡࡣࡥࡷࡴࡲࡵࡵࡧࠣࡲࡺࡳࡢࡦࡴࠣࡳࡷࠦࡡࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺ࡯ࡵࡣ࡯ࡣࡹ࡫ࡳࡵࡵࠣࠬ࡮ࡴࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࠪࡵࡩࡶࡻࡩࡳࡧࡧࠤ࡫ࡵࡲࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠲ࡨࡡࡴࡧࡧࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࡳࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣΈ")
        bstack1111111lll1_opy_ = config.get(bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨῊ"), {}).get(bstack1l1111_opy_ (u"ࠬࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠫΉ"), {})
        bstack111111l111l_opy_ = 0
        bstack11111l1ll11_opy_ = 0
        if bstack1l1llll1l_opy_.bstack111lll1llll_opy_(config):
            bstack11111l1ll11_opy_ = bstack1111111lll1_opy_.get(bstack1l1111_opy_ (u"࠭࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶࠫῌ"), 5)
            if isinstance(bstack11111l1ll11_opy_, str) and bstack11111l1ll11_opy_.endswith(bstack1l1111_opy_ (u"ࠧࠦࠩ῍")):
                try:
                    percentage = int(bstack11111l1ll11_opy_.strip(bstack1l1111_opy_ (u"ࠨࠧࠪ῎")))
                    if bstack111llll1ll1_opy_ > 0:
                        bstack111111l111l_opy_ = math.ceil((percentage * bstack111llll1ll1_opy_) / 100)
                    else:
                        raise ValueError(bstack1l1111_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨ࠱ࡧࡧࡳࡦࡦࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࡹ࠮ࠣ῏"))
                except ValueError as e:
                    raise ValueError(bstack1l1111_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥࠡࡸࡤࡰࡺ࡫ࠠࡧࡱࡵࠤࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴ࠼ࠣࡿࢂࠨῐ").format(bstack11111l1ll11_opy_)) from e
            else:
                bstack111111l111l_opy_ = int(bstack11111l1ll11_opy_)
        logger.info(bstack1l1111_opy_ (u"ࠦࡒࡧࡸࠡࡨࡤ࡭ࡱࡻࡲࡦࡵࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡳࡦࡶࠣࡸࡴࡀࠠࡼࡿࠣࠬ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡿࢂ࠯ࠢῑ").format(bstack111111l111l_opy_, bstack11111l1ll11_opy_))
        return bstack111111l111l_opy_
    def bstack1lllllllll11_opy_(self):
        return self.bstack111111l1ll1_opy_
    def bstack11111ll111l_opy_(self):
        return self.bstack11111l11lll_opy_
    def bstack1111111l111_opy_(self):
        return self.bstack11111l1llll_opy_
    def __111111lll11_opy_(self, enabled, mode, source=None):
        try:
            self.bstack111111l1ll1_opy_ = bool(enabled)
            if mode not in [bstack1l1111_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬῒ"), bstack1l1111_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡐࡰ࡯ࡽࠬΐ")]:
                logger.warning(bstack1l1111_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡱࡴࡪࡥࠡࠩࡾࢁࠬࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠢࡇࡩ࡫ࡧࡵ࡭ࡶ࡬ࡲ࡬ࠦࡴࡰࠢࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ࠲ࠧ῔").format(mode))
                mode = bstack1l1111_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ῕")
            self.bstack11111l11lll_opy_ = mode
            self.bstack11111l1llll_opy_ = []
            if source is None:
                self.bstack11111l1llll_opy_ = None
            elif isinstance(source, list):
                self.bstack11111l1llll_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1l1111_opy_ (u"ࠩ࠱࡮ࡸࡵ࡮ࠨῖ")):
                self.bstack11111l1llll_opy_ = self._111111ll1ll_opy_(source)
            self.__1llllllll1ll_opy_()
        except Exception as e:
            logger.error(bstack1l1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࠳ࠠࡦࡰࡤࡦࡱ࡫ࡤ࠻ࠢࡾࢁ࠱ࠦ࡭ࡰࡦࡨ࠾ࠥࢁࡽ࠭ࠢࡶࡳࡺࡸࡣࡦ࠼ࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥῗ").format(enabled, mode, source, e))
    def bstack11111l1l111_opy_(self):
        return self.bstack11111l1111l_opy_
    def __11111ll1111_opy_(self, value):
        self.bstack11111l1111l_opy_ = bool(value)
        self.__1llllllll1ll_opy_()
    def bstack111111111ll_opy_(self):
        return self.bstack111111lll1l_opy_
    def __111111l11ll_opy_(self, value):
        self.bstack111111lll1l_opy_ = bool(value)
        self.__1llllllll1ll_opy_()
    def bstack11111l1ll1l_opy_(self):
        return self.bstack1lllllllll1l_opy_
    def __11111l11l1l_opy_(self, value):
        self.bstack1lllllllll1l_opy_ = bool(value)
        self.__1llllllll1ll_opy_()
    def __1llllllll1ll_opy_(self):
        if self.bstack111111l1ll1_opy_:
            self.bstack11111l1111l_opy_ = False
            self.bstack111111lll1l_opy_ = False
            self.bstack1lllllllll1l_opy_ = False
            self.bstack111111l1l11_opy_.enable(bstack11111l11l11_opy_)
        elif self.bstack11111l1111l_opy_:
            self.bstack111111lll1l_opy_ = False
            self.bstack1lllllllll1l_opy_ = False
            self.bstack111111l1ll1_opy_ = False
            self.bstack111111l1l11_opy_.enable(bstack11111l11111_opy_)
        elif self.bstack111111lll1l_opy_:
            self.bstack11111l1111l_opy_ = False
            self.bstack1lllllllll1l_opy_ = False
            self.bstack111111l1ll1_opy_ = False
            self.bstack111111l1l11_opy_.enable(bstack11111ll11l1_opy_)
        elif self.bstack1lllllllll1l_opy_:
            self.bstack11111l1111l_opy_ = False
            self.bstack111111lll1l_opy_ = False
            self.bstack111111l1ll1_opy_ = False
            self.bstack111111l1l11_opy_.enable(bstack1lllllllllll_opy_)
        else:
            self.bstack111111l1l11_opy_.disable()
    def bstack1l11111l_opy_(self):
        return self.bstack111111l1l11_opy_.bstack1111111l1l1_opy_()
    def bstack1ll1l11111_opy_(self):
        if self.bstack111111l1l11_opy_.bstack1111111l1l1_opy_():
            return self.bstack111111l1l11_opy_.get_name()
        return None
    def _111111ll1ll_opy_(self, bstack1111111l11l_opy_):
        bstack1l1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡹ࡯ࡶࡴࡦࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣࡥࡳࡪࠠࡧࡱࡵࡱࡦࡺࠠࡪࡶࠣࡪࡴࡸࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡲࡹࡷࡩࡥࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠤ࠭ࡹࡴࡳࠫ࠽ࠤࡕࡧࡴࡩࠢࡷࡳࠥࡺࡨࡦࠢࡍࡗࡔࡔࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࡬ࡪࡵࡷ࠾ࠥࡌ࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡵࡩࡵࡵࡳࡪࡶࡲࡶࡾࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦῘ")
        if not os.path.isfile(bstack1111111l11l_opy_):
            logger.error(bstack1l1111_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࠫࢀࢃࠧࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠥῙ").format(bstack1111111l11l_opy_))
            return []
        data = None
        try:
            with open(bstack1111111l11l_opy_, bstack1l1111_opy_ (u"ࠨࡲࠣῚ")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡋࡕࡒࡒࠥ࡬ࡲࡰ࡯ࠣࡷࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥΊ").format(bstack1111111l11l_opy_, e))
            return []
        _111111ll11l_opy_ = None
        _1llllllllll1_opy_ = None
        def _11111111l1l_opy_():
            bstack11111l111l1_opy_ = {}
            bstack11111ll11ll_opy_ = {}
            try:
                if self.bstack111111ll1l1_opy_.startswith(bstack1l1111_opy_ (u"ࠨࡽࠪ῜")) and self.bstack111111ll1l1_opy_.endswith(bstack1l1111_opy_ (u"ࠩࢀࠫ῝")):
                    bstack11111l111l1_opy_ = json.loads(self.bstack111111ll1l1_opy_)
                else:
                    bstack11111l111l1_opy_ = dict(item.split(bstack1l1111_opy_ (u"ࠪ࠾ࠬ῞")) for item in self.bstack111111ll1l1_opy_.split(bstack1l1111_opy_ (u"ࠫ࠱࠭῟")) if bstack1l1111_opy_ (u"ࠬࡀࠧῠ") in item) if self.bstack111111ll1l1_opy_ else {}
                if self.bstack11111l1l1ll_opy_.startswith(bstack1l1111_opy_ (u"࠭ࡻࠨῡ")) and self.bstack11111l1l1ll_opy_.endswith(bstack1l1111_opy_ (u"ࠧࡾࠩῢ")):
                    bstack11111ll11ll_opy_ = json.loads(self.bstack11111l1l1ll_opy_)
                else:
                    bstack11111ll11ll_opy_ = dict(item.split(bstack1l1111_opy_ (u"ࠨ࠼ࠪΰ")) for item in self.bstack11111l1l1ll_opy_.split(bstack1l1111_opy_ (u"ࠩ࠯ࠫῤ")) if bstack1l1111_opy_ (u"ࠪ࠾ࠬῥ") in item) if self.bstack11111l1l1ll_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤ࡫࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡳࡡࡱࡲ࡬ࡲ࡬ࡹ࠺ࠡࡽࢀࠦῦ").format(e))
            logger.debug(bstack1l1111_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࡳࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࠽ࠤࢀࢃࠬࠡࡅࡏࡍ࠿ࠦࡻࡾࠤῧ").format(bstack11111l111l1_opy_, bstack11111ll11ll_opy_))
            return bstack11111l111l1_opy_, bstack11111ll11ll_opy_
        if _111111ll11l_opy_ is None or _1llllllllll1_opy_ is None:
            _111111ll11l_opy_, _1llllllllll1_opy_ = _11111111l1l_opy_()
        def bstack11111111ll1_opy_(name, bstack111111l11l1_opy_):
            if name in _1llllllllll1_opy_:
                return _1llllllllll1_opy_[name]
            if name in _111111ll11l_opy_:
                return _111111ll11l_opy_[name]
            if bstack111111l11l1_opy_.get(bstack1l1111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭Ῠ")):
                return bstack111111l11l1_opy_[bstack1l1111_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧῩ")]
            return None
        if isinstance(data, dict):
            bstack11111l1lll1_opy_ = []
            bstack11111l1l11l_opy_ = re.compile(bstack1l1111_opy_ (u"ࡳࠩࡡ࡟ࡆ࠳࡚࠱࠯࠼ࡣࡢ࠱ࠤࠨῪ"))
            for name, bstack111111l11l1_opy_ in data.items():
                if not isinstance(bstack111111l11l1_opy_, dict):
                    continue
                url = bstack111111l11l1_opy_.get(bstack1l1111_opy_ (u"ࠩࡸࡶࡱ࠭Ύ"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1l1111_opy_ (u"ࠪࠫῬ")):
                    logger.warning(bstack1l1111_opy_ (u"ࠦࡗ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹࠡࡗࡕࡐࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡳࡰࡷࡵࡧࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ῭").format(name, bstack111111l11l1_opy_))
                    continue
                if not bstack11111l1l11l_opy_.match(name):
                    logger.warning(bstack1l1111_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸ࡭ࡢࡶࠣࡪࡴࡸࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ΅").format(name, bstack111111l11l1_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1l1111_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࠫࢀࢃࠧࠡ࡯ࡸࡷࡹࠦࡨࡢࡸࡨࠤࡦࠦ࡬ࡦࡰࡪࡸ࡭ࠦࡢࡦࡶࡺࡩࡪࡴࠠ࠲ࠢࡤࡲࡩࠦ࠳࠱ࠢࡦ࡬ࡦࡸࡡࡤࡶࡨࡶࡸ࠴ࠢ`").format(name))
                    continue
                bstack111111l11l1_opy_ = bstack111111l11l1_opy_.copy()
                bstack111111l11l1_opy_[bstack1l1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ῰")] = name
                bstack111111l11l1_opy_[bstack1l1111_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ῱")] = bstack11111111ll1_opy_(name, bstack111111l11l1_opy_)
                if not bstack111111l11l1_opy_.get(bstack1l1111_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩῲ")) or bstack111111l11l1_opy_.get(bstack1l1111_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪῳ")) == bstack1l1111_opy_ (u"ࠫࠬῴ"):
                    logger.warning(bstack1l1111_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡮ࡰࡶࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡩࡩࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ῵").format(name, bstack111111l11l1_opy_))
                    continue
                if bstack111111l11l1_opy_.get(bstack1l1111_opy_ (u"࠭ࡢࡢࡵࡨࡆࡷࡧ࡮ࡤࡪࠪῶ")) and bstack111111l11l1_opy_[bstack1l1111_opy_ (u"ࠧࡣࡣࡶࡩࡇࡸࡡ࡯ࡥ࡫ࠫῷ")] == bstack111111l11l1_opy_[bstack1l1111_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨῸ")]:
                    logger.warning(bstack1l1111_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡥࡳࡪࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡶ࡫ࡩࠥࡹࡡ࡮ࡧࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤΌ").format(name, bstack111111l11l1_opy_))
                    continue
                bstack11111l1lll1_opy_.append(bstack111111l11l1_opy_)
            return bstack11111l1lll1_opy_
        return data
    def bstack11111lll111_opy_(self):
        data = {
            bstack1l1111_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩῺ"): {
                bstack1l1111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬΏ"): self.bstack1lllllllll11_opy_(),
                bstack1l1111_opy_ (u"ࠬࡳ࡯ࡥࡧࠪῼ"): self.bstack11111ll111l_opy_(),
                bstack1l1111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭´"): self.bstack1111111l111_opy_()
            }
        }
        return data
    def bstack111111llll1_opy_(self, config):
        bstack111111lllll_opy_ = {}
        bstack111111lllll_opy_[bstack1l1111_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭῾")] = {
            bstack1l1111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ῿"): self.bstack1lllllllll11_opy_(),
            bstack1l1111_opy_ (u"ࠩࡰࡳࡩ࡫ࠧ "): self.bstack11111ll111l_opy_()
        }
        bstack111111lllll_opy_[bstack1l1111_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩ࠭ ")] = {
            bstack1l1111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ "): self.bstack111111111ll_opy_()
        }
        bstack111111lllll_opy_[bstack1l1111_opy_ (u"ࠬࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩࡥࡦࡪࡴࡶࡸࠬ ")] = {
            bstack1l1111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ "): self.bstack11111l1l111_opy_()
        }
        bstack111111lllll_opy_[bstack1l1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡤ࡬ࡡࡪ࡮࡬ࡲ࡬ࡥࡡ࡯ࡦࡢࡪࡱࡧ࡫ࡺࠩ ")] = {
            bstack1l1111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ "): self.bstack11111l1ll1l_opy_()
        }
        if self.bstack1lllll1l1l_opy_(config):
            bstack111111lllll_opy_[bstack1l1111_opy_ (u"ࠩࡵࡩࡹࡸࡹࡠࡶࡨࡷࡹࡹ࡟ࡰࡰࡢࡪࡦ࡯࡬ࡶࡴࡨࠫ ")] = {
                bstack1l1111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ "): True,
                bstack1l1111_opy_ (u"ࠫࡲࡧࡸࡠࡴࡨࡸࡷ࡯ࡥࡴࠩ "): self.bstack1llll111l_opy_(config)
            }
        if self.bstack111lll1llll_opy_(config):
            bstack111111lllll_opy_[bstack1l1111_opy_ (u"ࠬࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧ ")] = {
                bstack1l1111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ​"): True,
                bstack1l1111_opy_ (u"ࠧ࡮ࡣࡻࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡸ࠭‌"): self.bstack111lllll111_opy_(config)
            }
        return bstack111111lllll_opy_
    def bstack1l11l11111_opy_(self, config):
        bstack1l1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࡹࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤࡧࡿࠠ࡮ࡣ࡮࡭ࡳ࡭ࠠࡢࠢࡦࡥࡱࡲࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡨࡵࡪ࡮ࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ‍")
        if not (config.get(bstack1l1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ‎"), None) in bstack11l1111llll_opy_ and self.bstack1lllllllll11_opy_()):
            return None
        bstack11111l1l1l1_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ‏"), None)
        logger.debug(bstack1l1111_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡆࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣ‐").format(bstack11111l1l1l1_opy_))
        try:
            bstack11l1l11111l_opy_ = bstack1l1111_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠥ‑").format(bstack11111l1l1l1_opy_)
            payload = {
                bstack1l1111_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ‒"): config.get(bstack1l1111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ–"), bstack1l1111_opy_ (u"ࠨࠩ—")),
                bstack1l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ―"): config.get(bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭‖"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ‗"): os.environ.get(bstack1l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦ‘"), bstack1l1111_opy_ (u"ࠨࠢ’")),
                bstack1l1111_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ‚"): int(os.environ.get(bstack1l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ‛")) or bstack1l1111_opy_ (u"ࠤ࠳ࠦ“")),
                bstack1l1111_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ”"): int(os.environ.get(bstack1l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ„")) or bstack1l1111_opy_ (u"ࠧ࠷ࠢ‟")),
                bstack1l1111_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣ†"): get_host_info(),
            }
            logger.debug(bstack1l1111_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡ࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡴࡦࡿ࡬ࡰࡣࡧ࠾ࠥࢁࡽࠣ‡").format(payload))
            response = bstack11l11lll11l_opy_.bstack11111111111_opy_(bstack11l1l11111l_opy_, payload)
            if response:
                logger.debug(bstack1l1111_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡂࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ•").format(response))
                return response
            else:
                logger.error(bstack1l1111_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨ‣").format(bstack11111l1l1l1_opy_))
                return None
        except Exception as e:
            logger.error(bstack1l1111_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅࠢࡾࢁ࠿ࠦࡻࡾࠤ․").format(bstack11111l1l1l1_opy_, e))
            return None