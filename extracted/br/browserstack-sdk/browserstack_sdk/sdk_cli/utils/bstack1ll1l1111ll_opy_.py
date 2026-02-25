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
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1ll11l1l1l1_opy_:
    bstack11l1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥࡻࡴࡪ࡮࡬ࡸࡾࠦ࡭ࡦࡶ࡫ࡳࡩࡹࠠࡵࡱࠣࡷࡪࡺࠠࡢࡰࡧࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࠣࡱࡪࡺࡡࡥࡣࡷࡥ࠳ࠐࠠࠡࠢࠣࡍࡹࠦ࡭ࡢ࡫ࡱࡸࡦ࡯࡮ࡴࠢࡷࡻࡴࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷ࡯ࡥࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡳࡪࠠࡣࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵ࠱ࠎࠥࠦࠠࠡࡇࡤࡧ࡭ࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡧࡱࡸࡷࡿࠠࡪࡵࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡺ࡯ࠡࡤࡨࠤࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡤࠡࡣࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࡱࡥࡺ࠼ࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡪ࡮࡫࡬ࡥࡡࡷࡽࡵ࡫ࠢ࠻ࠢࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦ࠱ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡻࡧ࡬ࡶࡧࡶࠦ࠿࡛ࠦ࡭࡫ࡶࡸࠥࡵࡦࠡࡶࡤ࡫ࠥࡼࡡ࡭ࡷࡨࡷࡢࠐࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠨࠢࠣ៊")
    _11l1l1lllll_opy_: Dict[str, Dict[str, Any]] = {}
    _11l1l1ll111_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1l1ll1lll_opy_: str, key_value: str, bstack11l1l1lll11_opy_: bool = False) -> None:
        if not bstack1l1ll1lll_opy_ or not key_value or bstack1l1ll1lll_opy_.strip() == bstack11l1l11_opy_ (u"ࠣࠤ់") or key_value.strip() == bstack11l1l11_opy_ (u"ࠤࠥ៌"):
            logger.error(bstack11l1l11_opy_ (u"ࠥ࡯ࡪࡿ࡟࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢ࡮ࡩࡾࡥࡶࡢ࡮ࡸࡩࠥࡳࡵࡴࡶࠣࡦࡪࠦ࡮ࡰࡰ࠰ࡲࡺࡲ࡬ࠡࡣࡱࡨࠥࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠣ៍"))
        values: List[str] = bstack1ll11l1l1l1_opy_.bstack11l1l1lll1l_opy_(key_value)
        bstack11l1l1llll1_opy_ = {bstack11l1l11_opy_ (u"ࠦ࡫࡯ࡥ࡭ࡦࡢࡸࡾࡶࡥࠣ៎"): bstack11l1l11_opy_ (u"ࠧࡳࡵ࡭ࡶ࡬ࡣࡩࡸ࡯ࡱࡦࡲࡻࡳࠨ៏"), bstack11l1l11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨ័"): values}
        bstack11l1l1ll1ll_opy_ = bstack1ll11l1l1l1_opy_._11l1l1ll111_opy_ if bstack11l1l1lll11_opy_ else bstack1ll11l1l1l1_opy_._11l1l1lllll_opy_
        if bstack1l1ll1lll_opy_ in bstack11l1l1ll1ll_opy_:
            bstack11l1ll1111l_opy_ = bstack11l1l1ll1ll_opy_[bstack1l1ll1lll_opy_]
            bstack11l1ll11111_opy_ = bstack11l1ll1111l_opy_.get(bstack11l1l11_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢ៑"), [])
            for val in values:
                if val not in bstack11l1ll11111_opy_:
                    bstack11l1ll11111_opy_.append(val)
            bstack11l1ll1111l_opy_[bstack11l1l11_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳ្ࠣ")] = bstack11l1ll11111_opy_
        else:
            bstack11l1l1ll1ll_opy_[bstack1l1ll1lll_opy_] = bstack11l1l1llll1_opy_
    @staticmethod
    def bstack11ll11l111l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1ll11l1l1l1_opy_._11l1l1lllll_opy_
    @staticmethod
    def bstack11l1l1ll11l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1ll11l1l1l1_opy_._11l1l1ll111_opy_
    @staticmethod
    def bstack11l1l1lll1l_opy_(bstack11l1l1ll1l1_opy_: str) -> List[str]:
        bstack11l1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡱ࡮࡬ࡸࡸࠦࡴࡩࡧࠣ࡭ࡳࡶࡵࡵࠢࡶࡸࡷ࡯࡮ࡨࠢࡥࡽࠥࡩ࡯࡮࡯ࡤࡷࠥࡽࡨࡪ࡮ࡨࠤࡷ࡫ࡳࡱࡧࡦࡸ࡮ࡴࡧࠡࡦࡲࡹࡧࡲࡥ࠮ࡳࡸࡳࡹ࡫ࡤࠡࡵࡸࡦࡸࡺࡲࡪࡰࡪࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡪࡾࡡ࡮ࡲ࡯ࡩ࠿ࠦࠧࡢ࠮ࠣࠦࡧ࠲ࡣࠣ࠮ࠣࡨࠬࠦ࠭࠿ࠢ࡞ࠫࡦ࠭ࠬࠡࠩࡥ࠰ࡨ࠭ࠬࠡࠩࡧࠫࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ៓")
        pattern = re.compile(bstack11l1l11_opy_ (u"ࡵࠫࠧ࠮࡛࡟ࠤࡠ࠮࠮ࠨࡼࠩ࡝ࡡ࠰ࡢ࠱ࠩࠨ។"))
        result = []
        for match in pattern.finditer(bstack11l1l1ll1l1_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack11l1l11_opy_ (u"࡚ࠦࡺࡩ࡭࡫ࡷࡽࠥࡩ࡬ࡢࡵࡶࠤࡸ࡮࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤ࡮ࡴࡳࡵࡣࡱࡸ࡮ࡧࡴࡦࡦࠥ៕"))