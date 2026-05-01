# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import tempfile
import math
from bstack_utils import logger_utils
from bstack_utils.constants import bstack1l11l1lll1_opy_, bstack1111111ll11_opy_
from bstack_utils.helper import bstack1lll1llllll1_opy_, get_host_info
from bstack_utils.bstack11111lll1ll_opy_ import bstack11111llllll_opy_
import json
import re
import sys
bstack1lll1111llll_opy_ = bstack111ll_opy_ (u"ࠨࡲࡦࡶࡵࡽ࡙࡫ࡳࡵࡵࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠧ╙")
bstack1ll1lllllll1_opy_ = bstack111ll_opy_ (u"ࠢࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪࠨ╚")
bstack1lll111lll1l_opy_ = bstack111ll_opy_ (u"ࠣࡴࡸࡲࡕࡸࡥࡷ࡫ࡲࡹࡸࡲࡹࡇࡣ࡬ࡰࡪࡪࡆࡪࡴࡶࡸࠧ╛")
bstack1ll1llllll11_opy_ = bstack111ll_opy_ (u"ࠤࡵࡩࡷࡻ࡮ࡑࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡊࡦ࡯࡬ࡦࡦࠥ╜")
bstack1lll1111l111_opy_ = bstack111ll_opy_ (u"ࠥࡷࡰ࡯ࡰࡇ࡮ࡤ࡯ࡾࡧ࡮ࡥࡈࡤ࡭ࡱ࡫ࡤࠣ╝")
bstack1ll1lllll11l_opy_ = bstack111ll_opy_ (u"ࠦࡷࡻ࡮ࡔ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠣ╞")
bstack1lll11111lll_opy_ = {
    bstack1lll1111llll_opy_,
    bstack1ll1lllllll1_opy_,
    bstack1lll111lll1l_opy_,
    bstack1ll1llllll11_opy_,
    bstack1lll1111l111_opy_,
    bstack1ll1lllll11l_opy_
}
bstack1lll111l1111_opy_ = {bstack111ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ╟")}
logger = logger_utils.get_logger(__name__, bstack1l11l1lll1_opy_)
class bstack1lll1111ll1l_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1lll111111ll_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1ll11l1l_opy_:
    _1l1llllllll_opy_ = None
    def __init__(self, config):
        self.bstack1lll1111111l_opy_ = False
        self.bstack1lll111ll1ll_opy_ = False
        self.bstack1lll11l11l1l_opy_ = False
        self.bstack1lll11l1ll1l_opy_ = False
        self.bstack1ll1llll111l_opy_ = None
        self.bstack1lll1111lll1_opy_ = bstack1lll1111ll1l_opy_()
        self.bstack1lll111l11l1_opy_ = None
        opts = config.get(bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ╠"), {})
        self.bstack1lll111ll111_opy_ = config.get(bstack111ll_opy_ (u"ࠧࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࡇࡑ࡚ࠬ╡"), bstack111ll_opy_ (u"ࠣࠤ╢"))
        self.bstack1ll1llll11ll_opy_ = config.get(bstack111ll_opy_ (u"ࠩࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡇࡑࡏࠧ╣"), bstack111ll_opy_ (u"ࠥࠦ╤"))
        bstack1lll111l1lll_opy_ = opts.get(bstack1ll1lllll11l_opy_, {})
        bstack1lll11l1ll11_opy_ = None
        if bstack111ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ╥") in bstack1lll111l1lll_opy_:
            bstack1ll1lllll1ll_opy_ = bstack1lll111l1lll_opy_[bstack111ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ╦")]
            if bstack1ll1lllll1ll_opy_ is None or (isinstance(bstack1ll1lllll1ll_opy_, str) and bstack1ll1lllll1ll_opy_.strip() == bstack111ll_opy_ (u"࠭ࠧ╧")) or (isinstance(bstack1ll1lllll1ll_opy_, list) and len(bstack1ll1lllll1ll_opy_) == 0):
                bstack1lll11l1ll11_opy_ = []
            elif isinstance(bstack1ll1lllll1ll_opy_, list):
                bstack1lll11l1ll11_opy_ = bstack1ll1lllll1ll_opy_
            elif isinstance(bstack1ll1lllll1ll_opy_, str) and bstack1ll1lllll1ll_opy_.strip():
                bstack1lll11l1ll11_opy_ = bstack1ll1lllll1ll_opy_
            else:
                logger.warning(bstack111ll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡵࡲࡹࡷࡩࡥࠡࡸࡤࡰࡺ࡫ࠠࡪࡰࠣࡧࡴࡴࡦࡪࡩ࠽ࠤࢀࢃ࠮ࠡࡆࡨࡪࡦࡻ࡬ࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡧࡰࡴࡹࡿࠠ࡭࡫ࡶࡸ࠳ࠨ╨").format(bstack1ll1lllll1ll_opy_))
                bstack1lll11l1ll11_opy_ = []
        self.__1lll11l1l1ll_opy_(
            bstack1lll111l1lll_opy_.get(bstack111ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ╩"), False),
            bstack1lll111l1lll_opy_.get(bstack111ll_opy_ (u"ࠩࡰࡳࡩ࡫ࠧ╪"), bstack111ll_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ╫")),
            bstack1lll11l1ll11_opy_
        )
        self.__1lll111lll11_opy_(opts.get(bstack1lll111lll1l_opy_, False))
        self.__1lll11l1l1l1_opy_(opts.get(bstack1ll1llllll11_opy_, False))
        self.__1lll11l11ll1_opy_(opts.get(bstack1lll1111l111_opy_, False))
    @classmethod
    def bstack1l1l11ll1_opy_(cls, config=None):
        if cls._1l1llllllll_opy_ is None and config is not None:
            cls._1l1llllllll_opy_ = bstack1ll11l1l_opy_(config)
        return cls._1l1llllllll_opy_
    @staticmethod
    def bstack1111l11ll1_opy_(config: dict) -> bool:
        bstack1lll11111ll1_opy_ = config.get(bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ╬"), {}).get(bstack1lll1111llll_opy_, {})
        return bstack1lll11111ll1_opy_.get(bstack111ll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭╭"), False)
    @staticmethod
    def bstack111l1l11l_opy_(config: dict) -> int:
        bstack1lll11111ll1_opy_ = config.get(bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ╮"), {}).get(bstack1lll1111llll_opy_, {})
        retries = 0
        if bstack1ll11l1l_opy_.bstack1111l11ll1_opy_(config):
            retries = bstack1lll11111ll1_opy_.get(bstack111ll_opy_ (u"ࠧ࡮ࡣࡻࡖࡪࡺࡲࡪࡧࡶࠫ╯"), 1)
        return retries
    @staticmethod
    def bstack1lllll111l_opy_(config: dict) -> dict:
        bstack1lll11l111ll_opy_ = config.get(bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ╰"), {})
        return {
            key: value for key, value in bstack1lll11l111ll_opy_.items() if key in bstack1lll11111lll_opy_
        }
    @staticmethod
    def bstack1lll111llll1_opy_():
        bstack111ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ╱")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦ╲").format(os.getenv(bstack111ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ╳")))))
    @staticmethod
    def bstack1ll1llllllll_opy_(test_name: str):
        bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ╴")
        bstack1lll11l111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧ╵").format(os.getenv(bstack111ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ╶"))))
        with open(bstack1lll11l111l1_opy_, bstack111ll_opy_ (u"ࠨࡣࠪ╷")) as file:
            file.write(bstack111ll_opy_ (u"ࠤࡾࢁࡡࡴࠢ╸").format(test_name))
    @staticmethod
    def bstack1lll111l11ll_opy_(framework: str) -> bool:
       return framework.lower() in bstack1lll111l1111_opy_
    @staticmethod
    def bstack1llllllll111_opy_(config: dict) -> bool:
        bstack1lll111l1ll1_opy_ = config.get(bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ╹"), {}).get(bstack1ll1lllllll1_opy_, {})
        return bstack1lll111l1ll1_opy_.get(bstack111ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ╺"), False)
    @staticmethod
    def bstack1lllllll1l11_opy_(config: dict, bstack1llllllll1ll_opy_: int = 0) -> int:
        bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡊࡩࡹࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠬࠡࡹ࡫࡭ࡨ࡮ࠠࡤࡣࡱࠤࡧ࡫ࠠࡢࡰࠣࡥࡧࡹ࡯࡭ࡷࡷࡩࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡲࠡࡣࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡱࡷࡥࡱࡥࡴࡦࡵࡷࡷࠥ࠮ࡩ࡯ࡶࠬ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࠬࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ╻")
        bstack1lll111l1ll1_opy_ = config.get(bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ╼"), {}).get(bstack111ll_opy_ (u"ࠧࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭╽"), {})
        bstack1lll11111l1l_opy_ = 0
        bstack1lll111l1l1l_opy_ = 0
        if bstack1ll11l1l_opy_.bstack1llllllll111_opy_(config):
            bstack1lll111l1l1l_opy_ = bstack1lll111l1ll1_opy_.get(bstack111ll_opy_ (u"ࠨ࡯ࡤࡼࡋࡧࡩ࡭ࡷࡵࡩࡸ࠭╾"), 5)
            if isinstance(bstack1lll111l1l1l_opy_, str) and bstack1lll111l1l1l_opy_.endswith(bstack111ll_opy_ (u"ࠩࠨࠫ╿")):
                try:
                    percentage = int(bstack1lll111l1l1l_opy_.strip(bstack111ll_opy_ (u"ࠪࠩࠬ▀")))
                    if bstack1llllllll1ll_opy_ > 0:
                        bstack1lll11111l1l_opy_ = math.ceil((percentage * bstack1llllllll1ll_opy_) / 100)
                    else:
                        raise ValueError(bstack111ll_opy_ (u"࡙ࠦࡵࡴࡢ࡮ࠣࡸࡪࡹࡴࡴࠢࡰࡹࡸࡺࠠࡣࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠳ࡢࡢࡵࡨࡨࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࡴ࠰ࠥ▁"))
                except ValueError as e:
                    raise ValueError(bstack111ll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧࠣࡺࡦࡲࡵࡦࠢࡩࡳࡷࠦ࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶ࠾ࠥࢁࡽࠣ▂").format(bstack1lll111l1l1l_opy_)) from e
            else:
                bstack1lll11111l1l_opy_ = int(bstack1lll111l1l1l_opy_)
        logger.info(bstack111ll_opy_ (u"ࠨࡍࡢࡺࠣࡪࡦ࡯࡬ࡶࡴࡨࡷࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡵࡨࡸࠥࡺ࡯࠻ࠢࡾࢁࠥ࠮ࡦࡳࡱࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࢁࡽࠪࠤ▃").format(bstack1lll11111l1l_opy_, bstack1lll111l1l1l_opy_))
        return bstack1lll11111l1l_opy_
    def bstack1lll11l11111_opy_(self):
        return self.bstack1lll11l1ll1l_opy_
    def bstack1lll11111l11_opy_(self):
        return self.bstack1ll1llll111l_opy_
    def bstack1lll11l1111l_opy_(self):
        return self.bstack1lll111l11l1_opy_
    def __1lll11l1l1ll_opy_(self, enabled, mode, source=None):
        try:
            self.bstack1lll11l1ll1l_opy_ = bool(enabled)
            if mode not in [bstack111ll_opy_ (u"ࠧࡳࡧ࡯ࡩࡻࡧ࡮ࡵࡈ࡬ࡶࡸࡺࠧ▄"), bstack111ll_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡒࡲࡱࡿࠧ▅")]:
                logger.warning(bstack111ll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡳ࡯ࡥࡧࠣࠫࢀࢃࠧࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠤࡉ࡫ࡦࡢࡷ࡯ࡸ࡮ࡴࡧࠡࡶࡲࠤࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬ࠴ࠢ▆").format(mode))
                mode = bstack111ll_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ▇")
            self.bstack1ll1llll111l_opy_ = mode
            self.bstack1lll111l11l1_opy_ = []
            if source is None:
                self.bstack1lll111l11l1_opy_ = None
            elif isinstance(source, list):
                self.bstack1lll111l11l1_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack111ll_opy_ (u"ࠫ࠳ࡰࡳࡰࡰࠪ█")):
                self.bstack1lll111l11l1_opy_ = self._1lll1111l1l1_opy_(source)
            self.__1lll11111111_opy_()
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠ࠮ࠢࡨࡲࡦࡨ࡬ࡦࡦ࠽ࠤࢀࢃࠬࠡ࡯ࡲࡨࡪࡀࠠࡼࡿ࠯ࠤࡸࡵࡵࡳࡥࡨ࠾ࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ▉").format(enabled, mode, source, e))
    def bstack1lll1111l11l_opy_(self):
        return self.bstack1lll1111111l_opy_
    def __1lll111lll11_opy_(self, value):
        self.bstack1lll1111111l_opy_ = bool(value)
        self.__1lll11111111_opy_()
    def bstack1ll1llll11l1_opy_(self):
        return self.bstack1lll111ll1ll_opy_
    def __1lll11l1l1l1_opy_(self, value):
        self.bstack1lll111ll1ll_opy_ = bool(value)
        self.__1lll11111111_opy_()
    def bstack1lll11l11lll_opy_(self):
        return self.bstack1lll11l11l1l_opy_
    def __1lll11l11ll1_opy_(self, value):
        self.bstack1lll11l11l1l_opy_ = bool(value)
        self.__1lll11111111_opy_()
    def __1lll11111111_opy_(self):
        if self.bstack1lll11l1ll1l_opy_:
            self.bstack1lll1111111l_opy_ = False
            self.bstack1lll111ll1ll_opy_ = False
            self.bstack1lll11l11l1l_opy_ = False
            self.bstack1lll1111lll1_opy_.enable(bstack1ll1lllll11l_opy_)
        elif self.bstack1lll1111111l_opy_:
            self.bstack1lll111ll1ll_opy_ = False
            self.bstack1lll11l11l1l_opy_ = False
            self.bstack1lll11l1ll1l_opy_ = False
            self.bstack1lll1111lll1_opy_.enable(bstack1lll111lll1l_opy_)
        elif self.bstack1lll111ll1ll_opy_:
            self.bstack1lll1111111l_opy_ = False
            self.bstack1lll11l11l1l_opy_ = False
            self.bstack1lll11l1ll1l_opy_ = False
            self.bstack1lll1111lll1_opy_.enable(bstack1ll1llllll11_opy_)
        elif self.bstack1lll11l11l1l_opy_:
            self.bstack1lll1111111l_opy_ = False
            self.bstack1lll111ll1ll_opy_ = False
            self.bstack1lll11l1ll1l_opy_ = False
            self.bstack1lll1111lll1_opy_.enable(bstack1lll1111l111_opy_)
        else:
            self.bstack1lll1111lll1_opy_.disable()
    def bstack11lll11l1_opy_(self):
        return self.bstack1lll1111lll1_opy_.bstack1lll111111ll_opy_()
    def bstack1lllll111ll_opy_(self):
        if self.bstack1lll1111lll1_opy_.bstack1lll111111ll_opy_():
            return self.bstack1lll1111lll1_opy_.get_name()
        return None
    def _1lll1111l1l1_opy_(self, bstack1ll1l1l1lll_opy_):
        bstack111ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡴࡱࡸࡶࡨ࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠥࡧ࡮ࡥࠢࡩࡳࡷࡳࡡࡵࠢ࡬ࡸࠥ࡬࡯ࡳࠢࡶࡱࡦࡸࡴࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡷࡴࡻࡲࡤࡧࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠦࠨࡴࡶࡵ࠭࠿ࠦࡐࡢࡶ࡫ࠤࡹࡵࠠࡵࡪࡨࠤࡏ࡙ࡏࡏࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࡮࡬ࡷࡹࡀࠠࡇࡱࡵࡱࡦࡺࡴࡦࡦࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡷ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ▊")
        if not os.path.isfile(bstack1ll1l1l1lll_opy_):
            logger.error(bstack111ll_opy_ (u"ࠢࡔࡱࡸࡶࡨ࡫ࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡾࠩࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠧ▋").format(bstack1ll1l1l1lll_opy_))
            return []
        data = None
        try:
            with open(bstack1ll1l1l1lll_opy_, bstack111ll_opy_ (u"ࠣࡴࠥ▌")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack111ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡍࡗࡔࡔࠠࡧࡴࡲࡱࠥࡹ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧ▍").format(bstack1ll1l1l1lll_opy_, e))
            return []
        _1lll111l111l_opy_ = None
        _1ll1lllll1l1_opy_ = None
        def _1lll11l1l111_opy_():
            bstack1lll111lllll_opy_ = {}
            bstack1lll1111ll11_opy_ = {}
            try:
                if self.bstack1lll111ll111_opy_.startswith(bstack111ll_opy_ (u"ࠪࡿࠬ▎")) and self.bstack1lll111ll111_opy_.endswith(bstack111ll_opy_ (u"ࠫࢂ࠭▏")):
                    bstack1lll111lllll_opy_ = json.loads(self.bstack1lll111ll111_opy_)
                else:
                    bstack1lll111lllll_opy_ = dict(item.split(bstack111ll_opy_ (u"ࠬࡀࠧ▐")) for item in self.bstack1lll111ll111_opy_.split(bstack111ll_opy_ (u"࠭ࠬࠨ░")) if bstack111ll_opy_ (u"ࠧ࠻ࠩ▒") in item) if self.bstack1lll111ll111_opy_ else {}
                if self.bstack1ll1llll11ll_opy_.startswith(bstack111ll_opy_ (u"ࠨࡽࠪ▓")) and self.bstack1ll1llll11ll_opy_.endswith(bstack111ll_opy_ (u"ࠩࢀࠫ▔")):
                    bstack1lll1111ll11_opy_ = json.loads(self.bstack1ll1llll11ll_opy_)
                else:
                    bstack1lll1111ll11_opy_ = dict(item.split(bstack111ll_opy_ (u"ࠪ࠾ࠬ▕")) for item in self.bstack1ll1llll11ll_opy_.split(bstack111ll_opy_ (u"ࠫ࠱࠭▖")) if bstack111ll_opy_ (u"ࠬࡀࠧ▗") in item) if self.bstack1ll1llll11ll_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡦࡦࡣࡷࡹࡷ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠ࡮ࡣࡳࡴ࡮ࡴࡧࡴ࠼ࠣࡿࢂࠨ▘").format(e))
            logger.debug(bstack111ll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡ࡯ࡤࡴࡵ࡯࡮ࡨࡵࠣࡪࡷࡵ࡭ࠡࡧࡱࡺ࠿ࠦࡻࡾ࠮ࠣࡇࡑࡏ࠺ࠡࡽࢀࠦ▙").format(bstack1lll111lllll_opy_, bstack1lll1111ll11_opy_))
            return bstack1lll111lllll_opy_, bstack1lll1111ll11_opy_
        if _1lll111l111l_opy_ is None or _1ll1lllll1l1_opy_ is None:
            _1lll111l111l_opy_, _1ll1lllll1l1_opy_ = _1lll11l1l111_opy_()
        def bstack1ll1llll1lll_opy_(name, bstack1lll111ll1l1_opy_):
            if name in _1ll1lllll1l1_opy_:
                return _1ll1lllll1l1_opy_[name]
            if name in _1lll111l111l_opy_:
                return _1lll111l111l_opy_[name]
            if bstack1lll111ll1l1_opy_.get(bstack111ll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ▚")):
                return bstack1lll111ll1l1_opy_[bstack111ll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ▛")]
            return None
        if isinstance(data, dict):
            bstack1lll111l1l11_opy_ = []
            bstack1lll11l11l11_opy_ = re.compile(bstack111ll_opy_ (u"ࡵࠫࡣࡡࡁ࠮࡜࠳࠱࠾ࡥ࡝ࠬࠦࠪ▜"))
            for name, bstack1lll111ll1l1_opy_ in data.items():
                if not isinstance(bstack1lll111ll1l1_opy_, dict):
                    continue
                if not bstack1lll11l11l11_opy_.match(name):
                    logger.warning(bstack111ll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡹ࡯ࡶࡴࡦࡩࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠢࡩࡳࡷࡳࡡࡵࠢࡩࡳࡷࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ▝").format(name, bstack1lll111ll1l1_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack111ll_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠢࠪࡿࢂ࠭ࠠ࡮ࡷࡶࡸࠥ࡮ࡡࡷࡧࠣࡥࠥࡲࡥ࡯ࡩࡷ࡬ࠥࡨࡥࡵࡹࡨࡩࡳࠦ࠱ࠡࡣࡱࡨࠥ࠹࠰ࠡࡥ࡫ࡥࡷࡧࡣࡵࡧࡵࡷ࠳ࠨ▞").format(name))
                    continue
                bstack1lll111ll1l1_opy_ = bstack1lll111ll1l1_opy_.copy()
                bstack1lll111ll1l1_opy_[bstack111ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ▟")] = name
                bstack1lll111ll1l1_opy_[bstack111ll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧ■")] = bstack1ll1llll1lll_opy_(name, bstack1lll111ll1l1_opy_)
                if not bstack1lll111ll1l1_opy_.get(bstack111ll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ□")) or bstack1lll111ll1l1_opy_.get(bstack111ll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩ▢")) == bstack111ll_opy_ (u"ࠪࠫ▣"):
                    logger.warning(bstack111ll_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡴ࡯ࡵࠢࡶࡴࡪࡩࡩࡧ࡫ࡨࡨࠥ࡬࡯ࡳࠢࡶࡳࡺࡸࡣࡦࠢࠪࡿࢂ࠭࠺ࠡࡽࢀࠦ▤").format(name, bstack1lll111ll1l1_opy_))
                    continue
                if bstack1lll111ll1l1_opy_.get(bstack111ll_opy_ (u"ࠬࡨࡡࡴࡧࡅࡶࡦࡴࡣࡩࠩ▥")) and bstack1lll111ll1l1_opy_[bstack111ll_opy_ (u"࠭ࡢࡢࡵࡨࡆࡷࡧ࡮ࡤࡪࠪ▦")] == bstack1lll111ll1l1_opy_[bstack111ll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧ▧")]:
                    logger.warning(bstack111ll_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦࠢࡥࡶࡦࡴࡣࡩࠢࡤࡲࡩࠦࡢࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡨࡧ࡮࡯ࡱࡷࠤࡧ࡫ࠠࡵࡪࡨࠤࡸࡧ࡭ࡦࠢࡩࡳࡷࠦࡳࡰࡷࡵࡧࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣ▨").format(name, bstack1lll111ll1l1_opy_))
                    continue
                bstack1ll1llll1ll1_opy_ = bstack1lll111ll1l1_opy_.get(bstack111ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ▩"), bstack111ll_opy_ (u"ࠪࡥࡵࡶࠧ▪"))
                if bstack1ll1llll1ll1_opy_ not in (bstack111ll_opy_ (u"ࠫࡦࡶࡰࠨ▫"), bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࠪ▬")):
                    logger.warning(bstack111ll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡵࡻࡳࡩࠥ࠭ࡻࡾࠩࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠱ࠦࡤࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࠧࡢࡲࡳࠫࠧ▭").format(bstack1ll1llll1ll1_opy_, name))
                    bstack1ll1llll1ll1_opy_ = bstack111ll_opy_ (u"ࠧࡢࡲࡳࠫ▮")
                bstack1lll111ll1l1_opy_[bstack111ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭▯")] = bstack1ll1llll1ll1_opy_
                bstack1lll111l1l11_opy_.append(bstack1lll111ll1l1_opy_)
            bstack1ll1lllll111_opy_ = {item[bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ▰")] for item in bstack1lll111l1l11_opy_}
            for name, bstack1ll1llll1l1l_opy_ in {**_1lll111l111l_opy_, **_1ll1lllll1l1_opy_}.items():
                if name in bstack1ll1lllll111_opy_:
                    continue
                if not bstack1lll11l11l11_opy_.match(name):
                    logger.warning(bstack111ll_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡵࡵࡳࡥࡨࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࡨࡲࡶࡲࡧࡴࠡࡨࡲࡶࠥ࠭ࡻࡾࠩࠣࡪࡷࡵ࡭ࠡࡅࡏࡍ࠴࡫࡮ࡷࠤ▱").format(name))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack111ll_opy_ (u"ࠦࡘࡵࡵࡳࡥࡨࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࠩࡾࢁࠬࠦ࡭ࡶࡵࡷࠤ࡭ࡧࡶࡦࠢࡤࠤࡱ࡫࡮ࡨࡶ࡫ࠤࡧ࡫ࡴࡸࡧࡨࡲࠥ࠷ࠠࡢࡰࡧࠤ࠸࠶ࠠࡤࡪࡤࡶࡦࡩࡴࡦࡴࡶ࠲ࠧ▲").format(name))
                    continue
                if not bstack1ll1llll1l1l_opy_:
                    continue
                if not isinstance(bstack1ll1llll1l1l_opy_, str):
                    logger.warning(bstack111ll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭ࠦࡦࡰࡴࠣࠫࢀࢃࠧࠡࡨࡵࡳࡲࠦࡃࡍࡋ࠲ࡩࡳࡼ࠺ࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࠥࡹࡴࡳ࡫ࡱ࡫࠳ࠨ△").format(name))
                    continue
                bstack1lll111ll11l_opy_ = bstack1ll1llll1l1l_opy_.strip()
                if bstack1lll111ll11l_opy_ == bstack111ll_opy_ (u"࠭ࠧ▴"):
                    continue
                bstack1lll111l1l11_opy_.append({bstack111ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ▵"): name, bstack111ll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨ▶"): bstack1lll111ll11l_opy_, bstack111ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ▷"): bstack111ll_opy_ (u"ࠪࡥࡵࡶࠧ▸")})
            return bstack1lll111l1l11_opy_
        return data
    def bstack1lll11l1llll_opy_(self):
        data = {
            bstack111ll_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪ▹"): {
                bstack111ll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭►"): self.bstack1lll11l11111_opy_(),
                bstack111ll_opy_ (u"࠭࡭ࡰࡦࡨࠫ▻"): self.bstack1lll11111l11_opy_(),
                bstack111ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ▼"): self.bstack1lll11l1111l_opy_()
            }
        }
        return data
    def bstack1lll11l1l11l_opy_(self, config):
        bstack1ll1llllll1l_opy_ = {}
        bstack1ll1llllll1l_opy_[bstack111ll_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ▽")] = {
            bstack111ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ▾"): self.bstack1lll11l11111_opy_(),
            bstack111ll_opy_ (u"ࠪࡱࡴࡪࡥࠨ▿"): self.bstack1lll11111l11_opy_()
        }
        bstack1ll1llllll1l_opy_[bstack111ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡴࡷ࡫ࡶࡪࡱࡸࡷࡱࡿ࡟ࡧࡣ࡬ࡰࡪࡪࠧ◀")] = {
            bstack111ll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭◁"): self.bstack1ll1llll11l1_opy_()
        }
        bstack1ll1llllll1l_opy_[bstack111ll_opy_ (u"࠭ࡲࡶࡰࡢࡴࡷ࡫ࡶࡪࡱࡸࡷࡱࡿ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡧ࡫ࡵࡷࡹ࠭◂")] = {
            bstack111ll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ◃"): self.bstack1lll1111l11l_opy_()
        }
        bstack1ll1llllll1l_opy_[bstack111ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡦࡢ࡫࡯࡭ࡳ࡭࡟ࡢࡰࡧࡣ࡫ࡲࡡ࡬ࡻࠪ◄")] = {
            bstack111ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ◅"): self.bstack1lll11l11lll_opy_()
        }
        if self.bstack1111l11ll1_opy_(config):
            bstack1ll1llllll1l_opy_[bstack111ll_opy_ (u"ࠪࡶࡪࡺࡲࡺࡡࡷࡩࡸࡺࡳࡠࡱࡱࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠬ◆")] = {
                bstack111ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ◇"): True,
                bstack111ll_opy_ (u"ࠬࡳࡡࡹࡡࡵࡩࡹࡸࡩࡦࡵࠪ◈"): self.bstack111l1l11l_opy_(config)
            }
        if self.bstack1llllllll111_opy_(config):
            bstack1ll1llll1l11_opy_ = config.get(bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ◉"), {}).get(bstack1ll1lllllll1_opy_, {})
            bstack1lll111l1l1l_opy_ = bstack1ll1llll1l11_opy_.get(bstack111ll_opy_ (u"ࠧ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷࠬ◊"), 5)
            if isinstance(bstack1lll111l1l1l_opy_, str) and bstack1lll111l1l1l_opy_.endswith(bstack111ll_opy_ (u"ࠨࠧࠪ○")):
                bstack1lll111111l1_opy_ = 0
            else:
                bstack1lll111111l1_opy_ = int(bstack1lll111l1l1l_opy_)
            bstack1ll1llllll1l_opy_[bstack111ll_opy_ (u"ࠩࡤࡦࡴࡸࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡰࡰࡢࡪࡦ࡯࡬ࡶࡴࡨࠫ◌")] = {
                bstack111ll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ◍"): True,
                bstack111ll_opy_ (u"ࠫࡲࡧࡸࡠࡨࡤ࡭ࡱࡻࡲࡦࡵࠪ◎"): bstack1lll111111l1_opy_
            }
        return bstack1ll1llllll1l_opy_
    def bstack1l1lllll_opy_(self, config):
        bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡳࡱࡲࡥࡤࡶࡶࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡤࡼࠤࡲࡧ࡫ࡪࡰࡪࠤࡦࠦࡣࡢ࡮࡯ࠤࡹࡵࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠠࠩࡵࡷࡶ࠮ࡀࠠࡕࡪࡨࠤ࡚࡛ࡉࡅࠢࡲࡪࠥࡺࡨࡦࠢࡥࡹ࡮ࡲࡤࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠱ࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠠࡪࡨࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ●")
        if not (config.get(bstack111ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ◐"), None) in bstack1111111ll11_opy_ and self.bstack1lll11l11111_opy_()):
            return None
        bstack1lll1111l1ll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ◑"), None)
        logger.debug(bstack111ll_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡃࡰ࡮࡯ࡩࡨࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦ࡙࡚ࠣࡏࡄ࠻ࠢࡾࢁࠧ◒").format(bstack1lll1111l1ll_opy_))
        try:
            bstack1111l1111l1_opy_ = bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠢ◓").format(bstack1lll1111l1ll_opy_)
            payload = {
                bstack111ll_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣ◔"): config.get(bstack111ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ◕"), bstack111ll_opy_ (u"ࠬ࠭◖")),
                bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤ◗"): config.get(bstack111ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ◘"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨ◙"): os.environ.get(bstack111ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠣ◚"), bstack111ll_opy_ (u"ࠥࠦ◛")),
                bstack111ll_opy_ (u"ࠦࡳࡵࡤࡦࡋࡱࡨࡪࡾࠢ◜"): int(os.environ.get(bstack111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣ◝")) or bstack111ll_opy_ (u"ࠨ࠰ࠣ◞")),
                bstack111ll_opy_ (u"ࠢࡵࡱࡷࡥࡱࡔ࡯ࡥࡧࡶࠦ◟"): int(os.environ.get(bstack111ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡑࡗࡅࡑࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥ◠")) or bstack111ll_opy_ (u"ࠤ࠴ࠦ◡")),
                bstack111ll_opy_ (u"ࠥ࡬ࡴࡹࡴࡊࡰࡩࡳࠧ◢"): get_host_info(),
            }
            logger.debug(bstack111ll_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡱࡣࡼࡰࡴࡧࡤ࠻ࠢࡾࢁࠧ◣").format(payload))
            response = bstack11111llllll_opy_.bstack1ll1llll1111_opy_(bstack1111l1111l1_opy_, payload)
            if response:
                logger.debug(bstack111ll_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡆࡺ࡯࡬ࡥࠢࡧࡥࡹࡧࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ◤").format(response))
                return response
            else:
                logger.error(bstack111ll_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࡀࠠࡼࡿࠥ◥").format(bstack1lll1111l1ll_opy_))
                return None
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡗࡘࡍࡉࠦࡻࡾ࠼ࠣࡿࢂࠨ◦").format(bstack1lll1111l1ll_opy_, e))
            return None