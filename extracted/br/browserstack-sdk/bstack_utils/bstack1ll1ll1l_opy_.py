# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import tempfile
import math
from bstack_utils import bstack1111ll111_opy_
from bstack_utils.constants import bstack11llll111_opy_
bstack111ll11l111_opy_ = {bstack111lll_opy_ (u"࠭ࡲࡦࡶࡵࡽ࡙࡫ࡳࡵࡵࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠬᵲ"), bstack111lll_opy_ (u"ࠧࡢࡤࡲࡶࡹࡈࡵࡪ࡮ࡧࡓࡳࡌࡡࡪ࡮ࡸࡶࡪ࠭ᵳ")}
bstack111ll11ll11_opy_ = {bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᵴ")}
logger = bstack1111ll111_opy_.get_logger(__name__, bstack11llll111_opy_)
class bstack1lllll1l11_opy_:
    @staticmethod
    def bstack1l1111111_opy_(config: dict) -> bool:
        bstack111ll11l1ll_opy_ = config.get(bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵵ"), {}).get(bstack111lll_opy_ (u"ࠪࡶࡪࡺࡲࡺࡖࡨࡷࡹࡹࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠩᵶ"), {})
        return bstack111ll11l1ll_opy_.get(bstack111lll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬᵷ"), False)
    @staticmethod
    def bstack1l1ll1l1l_opy_(config: dict) -> int:
        bstack111ll11l1ll_opy_ = config.get(bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵸ"), {}).get(bstack111lll_opy_ (u"࠭ࡲࡦࡶࡵࡽ࡙࡫ࡳࡵࡵࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠬᵹ"), {})
        retries = 0
        if bstack1lllll1l11_opy_.bstack1l1111111_opy_(config):
            retries = bstack111ll11l1ll_opy_.get(bstack111lll_opy_ (u"ࠧ࡮ࡣࡻࡖࡪࡺࡲࡪࡧࡶࠫᵺ"), 1)
        return retries
    @staticmethod
    def bstack1l111ll1_opy_(config: dict) -> dict:
        bstack111ll11ll1l_opy_ = config.get(bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᵻ"), {})
        return {
            key: value for key, value in bstack111ll11ll1l_opy_.items() if key in bstack111ll11l111_opy_
        }
    @staticmethod
    def bstack111ll11llll_opy_():
        bstack111lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᵼ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦᵽ").format(os.getenv(bstack111lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤᵾ")))))
    @staticmethod
    def bstack111ll111lll_opy_(test_name: str):
        bstack111lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᵿ")
        bstack111ll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧᶀ").format(os.getenv(bstack111lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧᶁ"))))
        with open(bstack111ll1l1111_opy_, bstack111lll_opy_ (u"ࠨࡣࠪᶂ")) as file:
            file.write(bstack111lll_opy_ (u"ࠤࡾࢁࡡࡴࠢᶃ").format(test_name))
    @staticmethod
    def bstack111ll11l1l1_opy_(framework: str) -> bool:
       return framework.lower() in bstack111ll11ll11_opy_
    @staticmethod
    def bstack11l1ll1l1l1_opy_(config: dict) -> bool:
        bstack111ll11l11l_opy_ = config.get(bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧᶄ"), {}).get(bstack111lll_opy_ (u"ࠫࡦࡨ࡯ࡳࡶࡅࡹ࡮ࡲࡤࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠪᶅ"), {})
        return bstack111ll11l11l_opy_.get(bstack111lll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭ᶆ"), False)
    @staticmethod
    def bstack11l1lll1111_opy_(config: dict, bstack11l1lll111l_opy_: int = 0) -> int:
        bstack111lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠭ࠢࡺ࡬࡮ࡩࡨࠡࡥࡤࡲࠥࡨࡥࠡࡣࡱࠤࡦࡨࡳࡰ࡮ࡸࡸࡪࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡳࠢࡤࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭ࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡲࡸࡦࡲ࡟ࡵࡧࡶࡸࡸࠦࠨࡪࡰࡷ࠭࠿ࠦࡔࡩࡧࠣࡸࡴࡺࡡ࡭ࠢࡱࡹࡲࡨࡥࡳࠢࡲࡪࠥࡺࡥࡴࡶࡶࠤ࠭ࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥ࠮ࡤࡤࡷࡪࡪࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦࡶ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᶇ")
        bstack111ll11l11l_opy_ = config.get(bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫᶈ"), {}).get(bstack111lll_opy_ (u"ࠨࡣࡥࡳࡷࡺࡂࡶ࡫࡯ࡨࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧᶉ"), {})
        bstack111ll11lll1_opy_ = 0
        if bstack1lllll1l11_opy_.bstack11l1ll1l1l1_opy_(config):
            bstack111ll1l111l_opy_ = bstack111ll11l11l_opy_.get(bstack111lll_opy_ (u"ࠩࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹࠧᶊ"), 5)
            if isinstance(bstack111ll1l111l_opy_, str) and bstack111ll1l111l_opy_.endswith(bstack111lll_opy_ (u"ࠪࠩࠬᶋ")):
                try:
                    percentage = int(bstack111ll1l111l_opy_.strip(bstack111lll_opy_ (u"ࠫࠪ࠭ᶌ")))
                    if bstack11l1lll111l_opy_ > 0:
                        bstack111ll11lll1_opy_ = bstack111ll11lll1_opy_ = math.ceil((percentage * bstack11l1lll111l_opy_) / 100)
                    else:
                        raise ValueError(bstack111lll_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡱࡺࡹࡴࠡࡤࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡴࡪࡸࡣࡦࡰࡷࡥ࡬࡫࠭ࡣࡣࡶࡩࡩࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࡵ࠱ࠦᶍ"))
                except ValueError as e:
                    raise ValueError(bstack111lll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨࠤࡻࡧ࡬ࡶࡧࠣࡪࡴࡸࠠ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷ࠿ࠦࡻࡾࠤᶎ").format(bstack111ll1l111l_opy_)) from e
            else:
                bstack111ll11lll1_opy_ = int(bstack111ll1l111l_opy_)
        logger.info(bstack111lll_opy_ (u"ࠢࡎࡣࡻࠤ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠦࡴࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡶࡩࡹࠦࡴࡰ࠼ࠣࡿࢂࠦࠨࡧࡴࡲࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡻࡾࠫࠥᶏ").format(bstack111ll11lll1_opy_, bstack111ll1l111l_opy_))
        return bstack111ll11lll1_opy_