# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.bstack1l1111ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lll111l111_opy_:
    bstack111l111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥࡻࡴࡪ࡮࡬ࡸࡾࠦ࡭ࡦࡶ࡫ࡳࡩࡹࠠࡵࡱࠣࡷࡪࡺࠠࡢࡰࡧࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࠣࡱࡪࡺࡡࡥࡣࡷࡥ࠳ࠐࠠࠡࠢࠣࡍࡹࠦ࡭ࡢ࡫ࡱࡸࡦ࡯࡮ࡴࠢࡷࡻࡴࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷ࡯ࡥࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡳࡪࠠࡣࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵ࠱ࠎࠥࠦࠠࠡࡇࡤࡧ࡭ࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡧࡱࡸࡷࡿࠠࡪࡵࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡺ࡯ࠡࡤࡨࠤࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡤࠡࡣࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࡱࡥࡺ࠼ࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡪ࡮࡫࡬ࡥࡡࡷࡽࡵ࡫ࠢ࠻ࠢࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦ࠱ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡻࡧ࡬ࡶࡧࡶࠦ࠿࡛ࠦ࡭࡫ࡶࡸࠥࡵࡦࠡࡶࡤ࡫ࠥࡼࡡ࡭ࡷࡨࡷࡢࠐࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠨࠢࠣᗙ")
    _11lll1lll1l_opy_: Dict[str, Dict[str, Any]] = {}
    _11llll111ll_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1l1l111l1l_opy_: str, key_value: str, bstack11lll1ll1ll_opy_: bool = False) -> None:
        if not bstack1l1l111l1l_opy_ or not key_value or bstack1l1l111l1l_opy_.strip() == bstack111l111_opy_ (u"ࠣࠤᗚ") or key_value.strip() == bstack111l111_opy_ (u"ࠤࠥᗛ"):
            logger.error(bstack111l111_opy_ (u"ࠥ࡯ࡪࡿ࡟࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢ࡮ࡩࡾࡥࡶࡢ࡮ࡸࡩࠥࡳࡵࡴࡶࠣࡦࡪࠦ࡮ࡰࡰ࠰ࡲࡺࡲ࡬ࠡࡣࡱࡨࠥࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠣᗜ"))
        values: List[str] = bstack1lll111l111_opy_.bstack11llll111l1_opy_(key_value)
        bstack11lll1llll1_opy_ = {bstack111l111_opy_ (u"ࠦ࡫࡯ࡥ࡭ࡦࡢࡸࡾࡶࡥࠣᗝ"): bstack111l111_opy_ (u"ࠧࡳࡵ࡭ࡶ࡬ࡣࡩࡸ࡯ࡱࡦࡲࡻࡳࠨᗞ"), bstack111l111_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᗟ"): values}
        bstack11lll1lll11_opy_ = bstack1lll111l111_opy_._11llll111ll_opy_ if bstack11lll1ll1ll_opy_ else bstack1lll111l111_opy_._11lll1lll1l_opy_
        if bstack1l1l111l1l_opy_ in bstack11lll1lll11_opy_:
            bstack11llll1111l_opy_ = bstack11lll1lll11_opy_[bstack1l1l111l1l_opy_]
            bstack11llll11111_opy_ = bstack11llll1111l_opy_.get(bstack111l111_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢᗠ"), [])
            for val in values:
                if val not in bstack11llll11111_opy_:
                    bstack11llll11111_opy_.append(val)
            bstack11llll1111l_opy_[bstack111l111_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳࠣᗡ")] = bstack11llll11111_opy_
        else:
            bstack11lll1lll11_opy_[bstack1l1l111l1l_opy_] = bstack11lll1llll1_opy_
    @staticmethod
    def bstack1l111ll111l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll111l111_opy_._11lll1lll1l_opy_
    @staticmethod
    def bstack11lll1ll1l1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll111l111_opy_._11llll111ll_opy_
    @staticmethod
    def bstack11llll111l1_opy_(bstack11lll1lllll_opy_: str) -> List[str]:
        bstack111l111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡱ࡮࡬ࡸࡸࠦࡴࡩࡧࠣ࡭ࡳࡶࡵࡵࠢࡶࡸࡷ࡯࡮ࡨࠢࡥࡽࠥࡩ࡯࡮࡯ࡤࡷࠥࡽࡨࡪ࡮ࡨࠤࡷ࡫ࡳࡱࡧࡦࡸ࡮ࡴࡧࠡࡦࡲࡹࡧࡲࡥ࠮ࡳࡸࡳࡹ࡫ࡤࠡࡵࡸࡦࡸࡺࡲࡪࡰࡪࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡪࡾࡡ࡮ࡲ࡯ࡩ࠿ࠦࠧࡢ࠮ࠣࠦࡧ࠲ࡣࠣ࠮ࠣࡨࠬࠦ࠭࠿ࠢ࡞ࠫࡦ࠭ࠬࠡࠩࡥ࠰ࡨ࠭ࠬࠡࠩࡧࠫࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᗢ")
        pattern = re.compile(bstack111l111_opy_ (u"ࡵࠫࠧ࠮࡛࡟ࠤࡠ࠮࠮ࠨࡼࠩ࡝ࡡ࠰ࡢ࠱ࠩࠨᗣ"))
        result = []
        for match in pattern.finditer(bstack11lll1lllll_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack111l111_opy_ (u"࡚ࠦࡺࡩ࡭࡫ࡷࡽࠥࡩ࡬ࡢࡵࡶࠤࡸ࡮࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤ࡮ࡴࡳࡵࡣࡱࡸ࡮ࡧࡴࡦࡦࠥᗤ"))