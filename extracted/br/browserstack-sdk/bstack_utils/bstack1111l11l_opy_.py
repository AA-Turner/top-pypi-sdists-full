# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack1l1lllll1l_opy_, bstack11111l1111l_opy_
from bstack_utils.helper import bstack1llll1l1lll1_opy_, get_host_info
from bstack_utils.bstack1111l111l11_opy_ import bstack1111l111l1l_opy_
import json
import re
import sys
bstack1lll11111l1l_opy_ = bstack1l111l_opy_ (u"ࠣࡴࡨࡸࡷࡿࡔࡦࡵࡷࡷࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠢ─")
bstack1lll111llll1_opy_ = bstack1l111l_opy_ (u"ࠤࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣ━")
bstack1lll1111l111_opy_ = bstack1l111l_opy_ (u"ࠥࡶࡺࡴࡐࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡉࡥ࡮ࡲࡥࡥࡈ࡬ࡶࡸࡺࠢ│")
bstack1lll11111ll1_opy_ = bstack1l111l_opy_ (u"ࠦࡷ࡫ࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࠧ┃")
bstack1lll111l1l1l_opy_ = bstack1l111l_opy_ (u"ࠧࡹ࡫ࡪࡲࡉࡰࡦࡱࡹࡢࡰࡧࡊࡦ࡯࡬ࡦࡦࠥ┄")
bstack1lll11l1l111_opy_ = bstack1l111l_opy_ (u"ࠨࡲࡶࡰࡖࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࠥ┅")
bstack1lll11l111ll_opy_ = {
    bstack1lll11111l1l_opy_,
    bstack1lll111llll1_opy_,
    bstack1lll1111l111_opy_,
    bstack1lll11111ll1_opy_,
    bstack1lll111l1l1l_opy_,
    bstack1lll11l1l111_opy_
}
bstack1lll11l11lll_opy_ = {bstack1l111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ┆")}
logger = logger_utils.get_logger(__name__, bstack1l1lllll1l_opy_)
class bstack1lll111l1ll1_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lll11l111l1_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1l1l111111_opy_:
    _1l1lll1l1ll_opy_ = None
    def __init__(self, config):
        self.bstack1lll111l1l11_opy_ = False
        self.bstack1lll1111l1l1_opy_ = False
        self.bstack1lll11ll1111_opy_ = False
        self.bstack1lll11l1l1l1_opy_ = False
        self.bstack1lll11l1111l_opy_ = None
        self.bstack1lll111l1lll_opy_ = bstack1lll111l1ll1_opy_()
        self.bstack1lll111lll11_opy_ = None
        opts = config.get(bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ┇"), {})
        self.bstack1lll1111ll1l_opy_ = config.get(bstack1l111l_opy_ (u"ࠩࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡉࡓ࡜ࠧ┈"), bstack1l111l_opy_ (u"ࠥࠦ┉"))
        self.bstack1lll111ll1l1_opy_ = config.get(bstack1l111l_opy_ (u"ࠫࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡉࡌࡊࠩ┊"), bstack1l111l_opy_ (u"ࠧࠨ┋"))
        bstack1lll1111l11l_opy_ = opts.get(bstack1lll11l1l111_opy_, {})
        bstack1lll11l11111_opy_ = None
        if bstack1l111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭┌") in bstack1lll1111l11l_opy_:
            bstack1lll11l1lll1_opy_ = bstack1lll1111l11l_opy_[bstack1l111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ┍")]
            if bstack1lll11l1lll1_opy_ is None or (isinstance(bstack1lll11l1lll1_opy_, str) and bstack1lll11l1lll1_opy_.strip() == bstack1l111l_opy_ (u"ࠨࠩ┎")) or (isinstance(bstack1lll11l1lll1_opy_, list) and len(bstack1lll11l1lll1_opy_) == 0):
                bstack1lll11l11111_opy_ = []
            elif isinstance(bstack1lll11l1lll1_opy_, list):
                bstack1lll11l11111_opy_ = bstack1lll11l1lll1_opy_
            elif isinstance(bstack1lll11l1lll1_opy_, str) and bstack1lll11l1lll1_opy_.strip():
                bstack1lll11l11111_opy_ = bstack1lll11l1lll1_opy_
            else:
                logger.warning(bstack1l111l_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡷࡴࡻࡲࡤࡧࠣࡺࡦࡲࡵࡦࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾ࠰ࠣࡈࡪ࡬ࡡࡶ࡮ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡩࡲࡶࡴࡺࠢ࡯࡭ࡸࡺ࠮ࠣ┏").format(bstack1lll11l1lll1_opy_))
                bstack1lll11l11111_opy_ = []
        self.__1lll11l1llll_opy_(
            bstack1lll1111l11l_opy_.get(bstack1l111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ┐"), False),
            bstack1lll1111l11l_opy_.get(bstack1l111l_opy_ (u"ࠫࡲࡵࡤࡦࠩ┑"), bstack1l111l_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ┒")),
            bstack1lll11l11111_opy_
        )
        self.__1lll11111lll_opy_(opts.get(bstack1lll1111l111_opy_, False))
        self.__1lll11111111_opy_(opts.get(bstack1lll11111ll1_opy_, False))
        self.__1lll11l1ll1l_opy_(opts.get(bstack1lll111l1l1l_opy_, False))
    @classmethod
    def bstack1ll11ll111_opy_(cls, config=None):
        if cls._1l1lll1l1ll_opy_ is None and config is not None:
            cls._1l1lll1l1ll_opy_ = bstack1l1l111111_opy_(config)
        return cls._1l1lll1l1ll_opy_
    @staticmethod
    def bstack11l111l11_opy_(config: dict) -> bool:
        bstack1lll11l11l1l_opy_ = config.get(bstack1l111l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ┓"), {}).get(bstack1lll11111l1l_opy_, {})
        return bstack1lll11l11l1l_opy_.get(bstack1l111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ└"), False)
    @staticmethod
    def bstack1l1l111l_opy_(config: dict) -> int:
        bstack1lll11l11l1l_opy_ = config.get(bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ┕"), {}).get(bstack1lll11111l1l_opy_, {})
        retries = 0
        if bstack1l1l111111_opy_.bstack11l111l11_opy_(config):
            retries = bstack1lll11l11l1l_opy_.get(bstack1l111l_opy_ (u"ࠩࡰࡥࡽࡘࡥࡵࡴ࡬ࡩࡸ࠭┖"), 1)
        return retries
    @staticmethod
    def bstack1l11l111l_opy_(config: dict) -> dict:
        bstack1lll11111l11_opy_ = config.get(bstack1l111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ┗"), {})
        return {
            key: value for key, value in bstack1lll11111l11_opy_.items() if key in bstack1lll11l111ll_opy_
        }
    @staticmethod
    def bstack1lll11l1l1ll_opy_():
        bstack1l111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ┘")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠧࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡿࢂࠨ┙").format(os.getenv(bstack1l111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ┚")))))
    @staticmethod
    def bstack1lll1111l1ll_opy_(test_name: str):
        bstack1l111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ┛")
        bstack1lll111lll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡼࡿ࠱ࡸࡽࡺࠢ├").format(os.getenv(bstack1l111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ┝"))))
        with open(bstack1lll111lll1l_opy_, bstack1l111l_opy_ (u"ࠪࡥࠬ┞")) as file:
            file.write(bstack1l111l_opy_ (u"ࠦࢀࢃ࡜࡯ࠤ┟").format(test_name))
    @staticmethod
    def bstack1lll11lll111_opy_(framework: str) -> bool:
       return framework.lower() in bstack1lll11l11lll_opy_
    @staticmethod
    def bstack1llllllll11l_opy_(config: dict) -> bool:
        bstack1lll111l11ll_opy_ = config.get(bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ┠"), {}).get(bstack1lll111llll1_opy_, {})
        return bstack1lll111l11ll_opy_.get(bstack1l111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ┡"), False)
    @staticmethod
    def bstack11111111ll1_opy_(config: dict, bstack1lllllllllll_opy_: int = 0) -> int:
        bstack1l111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥ࠮ࠣࡻ࡭࡯ࡣࡩࠢࡦࡥࡳࠦࡢࡦࠢࡤࡲࠥࡧࡢࡴࡱ࡯ࡹࡹ࡫ࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡴࠣࡥࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧࠡࠪࡧ࡭ࡨࡺࠩ࠻ࠢࡗ࡬ࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡳࡹࡧ࡬ࡠࡶࡨࡷࡹࡹࠠࠩ࡫ࡱࡸ࠮ࡀࠠࡕࡪࡨࠤࡹࡵࡴࡢ࡮ࠣࡲࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥ࠮ࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠮࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸ࠿ࠦࡔࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ┢")
        bstack1lll111l11ll_opy_ = config.get(bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ┣"), {}).get(bstack1l111l_opy_ (u"ࠩࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠨ┤"), {})
        bstack1lll1111lll1_opy_ = 0
        bstack1lll11lll11l_opy_ = 0
        if bstack1l1l111111_opy_.bstack1llllllll11l_opy_(config):
            bstack1lll11lll11l_opy_ = bstack1lll111l11ll_opy_.get(bstack1l111l_opy_ (u"ࠪࡱࡦࡾࡆࡢ࡫࡯ࡹࡷ࡫ࡳࠨ┥"), 5)
            if isinstance(bstack1lll11lll11l_opy_, str) and bstack1lll11lll11l_opy_.endswith(bstack1l111l_opy_ (u"ࠫࠪ࠭┦")):
                try:
                    percentage = int(bstack1lll11lll11l_opy_.strip(bstack1l111l_opy_ (u"ࠬࠫࠧ┧")))
                    if bstack1lllllllllll_opy_ > 0:
                        bstack1lll1111lll1_opy_ = math.ceil((percentage * bstack1lllllllllll_opy_) / 100)
                    else:
                        raise ValueError(bstack1l111l_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡲࡻࡳࡵࠢࡥࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠲ࠧ┨"))
                except ValueError as e:
                    raise ValueError(bstack1l111l_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡵࡲࠡ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸࡀࠠࡼࡿࠥ┩").format(bstack1lll11lll11l_opy_)) from e
            else:
                bstack1lll1111lll1_opy_ = int(bstack1lll11lll11l_opy_)
        logger.info(bstack1l111l_opy_ (u"ࠣࡏࡤࡼࠥ࡬ࡡࡪ࡮ࡸࡶࡪࡹࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡷࡪࡺࠠࡵࡱ࠽ࠤࢀࢃࠠࠩࡨࡵࡳࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿࠬࠦ┪").format(bstack1lll1111lll1_opy_, bstack1lll11lll11l_opy_))
        return bstack1lll1111lll1_opy_
    def bstack1lll11ll11l1_opy_(self):
        return self.bstack1lll11l1l1l1_opy_
    def bstack1lll11ll1lll_opy_(self):
        return self.bstack1lll11l1111l_opy_
    def bstack1lll111l1111_opy_(self):
        return self.bstack1lll111lll11_opy_
    def __1lll11l1llll_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lll11l1l1l1_opy_ = bool(enabled)
            if mode not in [bstack1l111l_opy_ (u"ࠩࡵࡩࡱ࡫ࡶࡢࡰࡷࡊ࡮ࡸࡳࡵࠩ┫"), bstack1l111l_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡔࡴ࡬ࡺࠩ┬")]:
                logger.warning(bstack1l111l_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠ࡮ࡱࡧࡩࠥ࠭ࡻࡾࠩࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡈ࡬ࡶࡸࡺࠧ࠯ࠤ┭").format(mode))
                mode = bstack1l111l_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ┮")
            self.bstack1lll11l1111l_opy_ = mode
            self.bstack1lll111lll11_opy_ = []
            if source is None:
                self.bstack1lll111lll11_opy_ = None
            elif isinstance(source, list):
                self.bstack1lll111lll11_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1l111l_opy_ (u"࠭࠮࡫ࡵࡲࡲࠬ┯")):
                self.bstack1lll111lll11_opy_ = self._1lll111ll1ll_opy_(source)
            self.__1lll111ll111_opy_()
        except Exception as e:
            logger.error(bstack1l111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢ࠰ࠤࡪࡴࡡࡣ࡮ࡨࡨ࠿ࠦࡻࡾ࠮ࠣࡱࡴࡪࡥ࠻ࠢࡾࢁ࠱ࠦࡳࡰࡷࡵࡧࡪࡀࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ┰").format(enabled, mode, source, e))
    def bstack1lll11ll1l1l_opy_(self):
        return self.bstack1lll111l1l11_opy_
    def __1lll11111lll_opy_(self, value):
        self.bstack1lll111l1l11_opy_ = bool(value)
        self.__1lll111ll111_opy_()
    def bstack1lll11l1ll11_opy_(self):
        return self.bstack1lll1111l1l1_opy_
    def __1lll11111111_opy_(self, value):
        self.bstack1lll1111l1l1_opy_ = bool(value)
        self.__1lll111ll111_opy_()
    def bstack1lll11l11ll1_opy_(self):
        return self.bstack1lll11ll1111_opy_
    def __1lll11l1ll1l_opy_(self, value):
        self.bstack1lll11ll1111_opy_ = bool(value)
        self.__1lll111ll111_opy_()
    def __1lll111ll111_opy_(self):
        if self.bstack1lll11l1l1l1_opy_:
            self.bstack1lll111l1l11_opy_ = False
            self.bstack1lll1111l1l1_opy_ = False
            self.bstack1lll11ll1111_opy_ = False
            self.bstack1lll111l1lll_opy_.enable(bstack1lll11l1l111_opy_)
        elif self.bstack1lll111l1l11_opy_:
            self.bstack1lll1111l1l1_opy_ = False
            self.bstack1lll11ll1111_opy_ = False
            self.bstack1lll11l1l1l1_opy_ = False
            self.bstack1lll111l1lll_opy_.enable(bstack1lll1111l111_opy_)
        elif self.bstack1lll1111l1l1_opy_:
            self.bstack1lll111l1l11_opy_ = False
            self.bstack1lll11ll1111_opy_ = False
            self.bstack1lll11l1l1l1_opy_ = False
            self.bstack1lll111l1lll_opy_.enable(bstack1lll11111ll1_opy_)
        elif self.bstack1lll11ll1111_opy_:
            self.bstack1lll111l1l11_opy_ = False
            self.bstack1lll1111l1l1_opy_ = False
            self.bstack1lll11l1l1l1_opy_ = False
            self.bstack1lll111l1lll_opy_.enable(bstack1lll111l1l1l_opy_)
        else:
            self.bstack1lll111l1lll_opy_.disable()
    def bstack1lll1lll1_opy_(self):
        return self.bstack1lll111l1lll_opy_.bstack1lll11l111l1_opy_()
    def bstack1111ll1l_opy_(self):
        if self.bstack1lll111l1lll_opy_.bstack1lll11l111l1_opy_():
            return self.bstack1lll111l1lll_opy_.get_name()
        return None
    def _1lll111ll1ll_opy_(self, bstack1ll1ll1ll1l_opy_):
        bstack1l111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡶࡳࡺࡸࡣࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠠࡢࡰࡧࠤ࡫ࡵࡲ࡮ࡣࡷࠤ࡮ࡺࠠࡧࡱࡵࠤࡸࡳࡡࡳࡶࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡹ࡯ࡶࡴࡦࡩࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠡࠪࡶࡸࡷ࠯࠺ࠡࡒࡤࡸ࡭ࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡔࡑࡑࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡰ࡮ࡹࡴ࠻ࠢࡉࡳࡷࡳࡡࡵࡶࡨࡨࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡲࡦࡲࡲࡷ࡮ࡺ࡯ࡳࡻࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ┱")
        if not os.path.isfile(bstack1ll1ll1ll1l_opy_):
            logger.error(bstack1l111l_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࠨࡽࢀࠫࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠢ┲").format(bstack1ll1ll1ll1l_opy_))
            return []
        data = None
        try:
            with open(bstack1ll1ll1ll1l_opy_, bstack1l111l_opy_ (u"ࠥࡶࠧ┳")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1l111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤࡏ࡙ࡏࡏࠢࡩࡶࡴࡳࠠࡴࡱࡸࡶࡨ࡫ࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢ┴").format(bstack1ll1ll1ll1l_opy_, e))
            return []
        _1lll111l111l_opy_ = None
        _1lll1111ll11_opy_ = None
        def _1lll1111111l_opy_():
            bstack1lll11l1l11l_opy_ = {}
            bstack1lll11ll1l11_opy_ = {}
            try:
                if self.bstack1lll1111ll1l_opy_.startswith(bstack1l111l_opy_ (u"ࠬࢁࠧ┵")) and self.bstack1lll1111ll1l_opy_.endswith(bstack1l111l_opy_ (u"࠭ࡽࠨ┶")):
                    bstack1lll11l1l11l_opy_ = json.loads(self.bstack1lll1111ll1l_opy_)
                else:
                    bstack1lll11l1l11l_opy_ = dict(item.split(bstack1l111l_opy_ (u"ࠧ࠻ࠩ┷")) for item in self.bstack1lll1111ll1l_opy_.split(bstack1l111l_opy_ (u"ࠨ࠮ࠪ┸")) if bstack1l111l_opy_ (u"ࠩ࠽ࠫ┹") in item) if self.bstack1lll1111ll1l_opy_ else {}
                if self.bstack1lll111ll1l1_opy_.startswith(bstack1l111l_opy_ (u"ࠪࡿࠬ┺")) and self.bstack1lll111ll1l1_opy_.endswith(bstack1l111l_opy_ (u"ࠫࢂ࠭┻")):
                    bstack1lll11ll1l11_opy_ = json.loads(self.bstack1lll111ll1l1_opy_)
                else:
                    bstack1lll11ll1l11_opy_ = dict(item.split(bstack1l111l_opy_ (u"ࠬࡀࠧ┼")) for item in self.bstack1lll111ll1l1_opy_.split(bstack1l111l_opy_ (u"࠭ࠬࠨ┽")) if bstack1l111l_opy_ (u"ࠧ࠻ࠩ┾") in item) if self.bstack1lll111ll1l1_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1l111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡨࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡰࡥࡵࡶࡩ࡯ࡩࡶ࠾ࠥࢁࡽࠣ┿").format(e))
            logger.debug(bstack1l111l_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡱࡦࡶࡰࡪࡰࡪࡷࠥ࡬ࡲࡰ࡯ࠣࡩࡳࡼ࠺ࠡࡽࢀ࠰ࠥࡉࡌࡊ࠼ࠣࡿࢂࠨ╀").format(bstack1lll11l1l11l_opy_, bstack1lll11ll1l11_opy_))
            return bstack1lll11l1l11l_opy_, bstack1lll11ll1l11_opy_
        if _1lll111l111l_opy_ is None or _1lll1111ll11_opy_ is None:
            _1lll111l111l_opy_, _1lll1111ll11_opy_ = _1lll1111111l_opy_()
        def bstack1lll111lllll_opy_(name, bstack1lll111111l1_opy_):
            if name in _1lll1111ll11_opy_:
                return _1lll1111ll11_opy_[name]
            if name in _1lll111l111l_opy_:
                return _1lll111l111l_opy_[name]
            if bstack1lll111111l1_opy_.get(bstack1l111l_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪ╁")):
                return bstack1lll111111l1_opy_[bstack1l111l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫ╂")]
            return None
        if isinstance(data, dict):
            bstack1lll111111ll_opy_ = []
            bstack1lll11l11l11_opy_ = re.compile(bstack1l111l_opy_ (u"ࡷ࠭࡞࡜ࡃ࠰࡞࠵࠳࠹ࡠ࡟࠮ࠨࠬ╃"))
            for name, bstack1lll111111l1_opy_ in data.items():
                if not isinstance(bstack1lll111111l1_opy_, dict):
                    continue
                url = bstack1lll111111l1_opy_.get(bstack1l111l_opy_ (u"࠭ࡵࡳ࡮ࠪ╄"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1l111l_opy_ (u"ࠧࠨ╅")):
                    logger.warning(bstack1l111l_opy_ (u"ࠣࡔࡨࡴࡴࡹࡩࡵࡱࡵࡽ࡛ࠥࡒࡍࠢ࡬ࡷࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ╆").format(name, bstack1lll111111l1_opy_))
                    continue
                if not bstack1lll11l11l11_opy_.match(name):
                    logger.warning(bstack1l111l_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡷࡴࡻࡲࡤࡧࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࡧࡱࡵࡱࡦࡺࠠࡧࡱࡵࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ╇").format(name, bstack1lll111111l1_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1l111l_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࠨࡽࢀࠫࠥࡳࡵࡴࡶࠣ࡬ࡦࡼࡥࠡࡣࠣࡰࡪࡴࡧࡵࡪࠣࡦࡪࡺࡷࡦࡧࡱࠤ࠶ࠦࡡ࡯ࡦࠣ࠷࠵ࠦࡣࡩࡣࡵࡥࡨࡺࡥࡳࡵ࠱ࠦ╈").format(name))
                    continue
                bstack1lll111111l1_opy_ = bstack1lll111111l1_opy_.copy()
                bstack1lll111111l1_opy_[bstack1l111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ╉")] = name
                bstack1lll111111l1_opy_[bstack1l111l_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ╊")] = bstack1lll111lllll_opy_(name, bstack1lll111111l1_opy_)
                if not bstack1lll111111l1_opy_.get(bstack1l111l_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭╋")) or bstack1lll111111l1_opy_.get(bstack1l111l_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧ╌")) == bstack1l111l_opy_ (u"ࠨࠩ╍"):
                    logger.warning(bstack1l111l_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡲࡴࡺࠠࡴࡲࡨࡧ࡮࡬ࡩࡦࡦࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤ╎").format(name, bstack1lll111111l1_opy_))
                    continue
                if bstack1lll111111l1_opy_.get(bstack1l111l_opy_ (u"ࠪࡦࡦࡹࡥࡃࡴࡤࡲࡨ࡮ࠧ╏")) and bstack1lll111111l1_opy_[bstack1l111l_opy_ (u"ࠫࡧࡧࡳࡦࡄࡵࡥࡳࡩࡨࠨ═")] == bstack1lll111111l1_opy_[bstack1l111l_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬ║")]:
                    logger.warning(bstack1l111l_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡢࡰࡧࠤࡧࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡺࡨࡦࠢࡶࡥࡲ࡫ࠠࡧࡱࡵࠤࡸࡵࡵࡳࡥࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨ╒").format(name, bstack1lll111111l1_opy_))
                    continue
                bstack1lll111111ll_opy_.append(bstack1lll111111l1_opy_)
            return bstack1lll111111ll_opy_
        return data
    def bstack1lll1l1111l1_opy_(self):
        data = {
            bstack1l111l_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭╓"): {
                bstack1l111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ╔"): self.bstack1lll11ll11l1_opy_(),
                bstack1l111l_opy_ (u"ࠩࡰࡳࡩ࡫ࠧ╕"): self.bstack1lll11ll1lll_opy_(),
                bstack1l111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ╖"): self.bstack1lll111l1111_opy_()
            }
        }
        return data
    def bstack1lll111l11l1_opy_(self, config):
        bstack1lll11ll1ll1_opy_ = {}
        bstack1lll11ll1ll1_opy_[bstack1l111l_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪ╗")] = {
            bstack1l111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭╘"): self.bstack1lll11ll11l1_opy_(),
            bstack1l111l_opy_ (u"࠭࡭ࡰࡦࡨࠫ╙"): self.bstack1lll11ll1lll_opy_()
        }
        bstack1lll11ll1ll1_opy_[bstack1l111l_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࠪ╚")] = {
            bstack1l111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ╛"): self.bstack1lll11l1ll11_opy_()
        }
        bstack1lll11ll1ll1_opy_[bstack1l111l_opy_ (u"ࠩࡵࡹࡳࡥࡰࡳࡧࡹ࡭ࡴࡻࡳ࡭ࡻࡢࡪࡦ࡯࡬ࡦࡦࡢࡪ࡮ࡸࡳࡵࠩ╜")] = {
            bstack1l111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ╝"): self.bstack1lll11ll1l1l_opy_()
        }
        bstack1lll11ll1ll1_opy_[bstack1l111l_opy_ (u"ࠫࡸࡱࡩࡱࡡࡩࡥ࡮ࡲࡩ࡯ࡩࡢࡥࡳࡪ࡟ࡧ࡮ࡤ࡯ࡾ࠭╞")] = {
            bstack1l111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭╟"): self.bstack1lll11l11ll1_opy_()
        }
        if self.bstack11l111l11_opy_(config):
            bstack1lll11ll1ll1_opy_[bstack1l111l_opy_ (u"࠭ࡲࡦࡶࡵࡽࡤࡺࡥࡴࡶࡶࡣࡴࡴ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠨ╠")] = {
                bstack1l111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ╡"): True,
                bstack1l111l_opy_ (u"ࠨ࡯ࡤࡼࡤࡸࡥࡵࡴ࡬ࡩࡸ࠭╢"): self.bstack1l1l111l_opy_(config)
            }
        if self.bstack1llllllll11l_opy_(config):
            bstack1lll11ll111l_opy_ = config.get(bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭╣"), {}).get(bstack1lll111llll1_opy_, {})
            bstack1lll11lll11l_opy_ = bstack1lll11ll111l_opy_.get(bstack1l111l_opy_ (u"ࠪࡱࡦࡾࡆࡢ࡫࡯ࡹࡷ࡫ࡳࠨ╤"), 5)
            if isinstance(bstack1lll11lll11l_opy_, str) and bstack1lll11lll11l_opy_.endswith(bstack1l111l_opy_ (u"ࠫࠪ࠭╥")):
                bstack1lll111ll11l_opy_ = 0
            else:
                bstack1lll111ll11l_opy_ = int(bstack1lll11lll11l_opy_)
            bstack1lll11ll1ll1_opy_[bstack1l111l_opy_ (u"ࠬࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧ╦")] = {
                bstack1l111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ╧"): True,
                bstack1l111l_opy_ (u"ࠧ࡮ࡣࡻࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡸ࠭╨"): bstack1lll111ll11l_opy_
            }
        return bstack1lll11ll1ll1_opy_
    def bstack1111lllll1_opy_(self, config):
        bstack1l111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࡹࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤࡧࡿࠠ࡮ࡣ࡮࡭ࡳ࡭ࠠࡢࠢࡦࡥࡱࡲࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡨࡵࡪ࡮ࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ╩")
        if not (config.get(bstack1l111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ╪"), None) in bstack11111l1111l_opy_ and self.bstack1lll11ll11l1_opy_()):
            return None
        bstack1lll11ll11ll_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ╫"), None)
        logger.debug(bstack1l111l_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡆࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣ╬").format(bstack1lll11ll11ll_opy_))
        try:
            bstack1111l111lll_opy_ = bstack1l111l_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠥ╭").format(bstack1lll11ll11ll_opy_)
            payload = {
                bstack1l111l_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ╮"): config.get(bstack1l111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ╯"), bstack1l111l_opy_ (u"ࠨࠩ╰")),
                bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ╱"): config.get(bstack1l111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭╲"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ╳"): os.environ.get(bstack1l111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦ╴"), bstack1l111l_opy_ (u"ࠨࠢ╵")),
                bstack1l111l_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ╶"): int(os.environ.get(bstack1l111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ╷")) or bstack1l111l_opy_ (u"ࠤ࠳ࠦ╸")),
                bstack1l111l_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ╹"): int(os.environ.get(bstack1l111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ╺")) or bstack1l111l_opy_ (u"ࠧ࠷ࠢ╻")),
                bstack1l111l_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣ╼"): get_host_info(),
            }
            logger.debug(bstack1l111l_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡ࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡴࡦࡿ࡬ࡰࡣࡧ࠾ࠥࢁࡽࠣ╽").format(payload))
            response = bstack1111l111l1l_opy_.bstack1lll1111llll_opy_(bstack1111l111lll_opy_, payload)
            if response:
                logger.debug(bstack1l111l_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡂࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ╾").format(response))
                return response
            else:
                logger.error(bstack1l111l_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨ╿").format(bstack1lll11ll11ll_opy_))
                return None
        except Exception as e:
            logger.error(bstack1l111l_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅࠢࡾࢁ࠿ࠦࡻࡾࠤ▀").format(bstack1lll11ll11ll_opy_, e))
            return None