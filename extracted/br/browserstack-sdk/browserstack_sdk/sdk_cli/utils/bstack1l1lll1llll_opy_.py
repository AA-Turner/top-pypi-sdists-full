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
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1ll11ll1l1l_opy_:
    bstack11ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡱࡴࡲࡺ࡮ࡪࡥࡴࠢࡸࡸ࡮ࡲࡩࡵࡻࠣࡱࡪࡺࡨࡰࡦࡶࠤࡹࡵࠠࡴࡧࡷࠤࡦࡴࡤࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࠠ࡮ࡧࡷࡥࡩࡧࡴࡢ࠰ࠍࠤࠥࠦࠠࡊࡶࠣࡱࡦ࡯࡮ࡵࡣ࡬ࡲࡸࠦࡴࡸࡱࠣࡷࡪࡶࡡࡳࡣࡷࡩࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴ࡬ࡩࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡢࡰࡧࠤࡧࡻࡩ࡭ࡦࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹ࠮ࠋࠢࠣࠤࠥࡋࡡࡤࡪࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡫࡮ࡵࡴࡼࠤ࡮ࡹࠠࡦࡺࡳࡩࡨࡺࡥࡥࠢࡷࡳࠥࡨࡥࠡࡵࡷࡶࡺࡩࡴࡶࡴࡨࡨࠥࡧࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢ࡮ࡩࡾࡀࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡧ࡫ࡨࡰࡩࡥࡴࡺࡲࡨࠦ࠿ࠦࠢ࡮ࡷ࡯ࡸ࡮ࡥࡤࡳࡱࡳࡨࡴࡽ࡮ࠣ࠮ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡸࡤࡰࡺ࡫ࡳࠣ࠼ࠣ࡟ࡱ࡯ࡳࡵࠢࡲࡪࠥࡺࡡࡨࠢࡹࡥࡱࡻࡥࡴ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠥࠦࠧះ")
    _11l1l1ll111_opy_: Dict[str, Dict[str, Any]] = {}
    _11l1l1ll1ll_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1ll1l1lll1_opy_: str, key_value: str, bstack11l1l1lll11_opy_: bool = False) -> None:
        if not bstack1ll1l1lll1_opy_ or not key_value or bstack1ll1l1lll1_opy_.strip() == bstack11ll111_opy_ (u"ࠧࠨៈ") or key_value.strip() == bstack11ll111_opy_ (u"ࠨࠢ៉"):
            logger.error(bstack11ll111_opy_ (u"ࠢ࡬ࡧࡼࡣࡳࡧ࡭ࡦࠢࡤࡲࡩࠦ࡫ࡦࡻࡢࡺࡦࡲࡵࡦࠢࡰࡹࡸࡺࠠࡣࡧࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡧ࡮ࡥࠢࡱࡳࡳ࠳ࡥ࡮ࡲࡷࡽࠧ៊"))
        values: List[str] = bstack1ll11ll1l1l_opy_.bstack11l1l1ll11l_opy_(key_value)
        bstack11l1l1lllll_opy_ = {bstack11ll111_opy_ (u"ࠣࡨ࡬ࡩࡱࡪ࡟ࡵࡻࡳࡩࠧ់"): bstack11ll111_opy_ (u"ࠤࡰࡹࡱࡺࡩࡠࡦࡵࡳࡵࡪ࡯ࡸࡰࠥ៌"), bstack11ll111_opy_ (u"ࠥࡺࡦࡲࡵࡦࡵࠥ៍"): values}
        bstack11l1l1llll1_opy_ = bstack1ll11ll1l1l_opy_._11l1l1ll1ll_opy_ if bstack11l1l1lll11_opy_ else bstack1ll11ll1l1l_opy_._11l1l1ll111_opy_
        if bstack1ll1l1lll1_opy_ in bstack11l1l1llll1_opy_:
            bstack11l1ll11111_opy_ = bstack11l1l1llll1_opy_[bstack1ll1l1lll1_opy_]
            bstack11l1l1lll1l_opy_ = bstack11l1ll11111_opy_.get(bstack11ll111_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦ៎"), [])
            for val in values:
                if val not in bstack11l1l1lll1l_opy_:
                    bstack11l1l1lll1l_opy_.append(val)
            bstack11l1ll11111_opy_[bstack11ll111_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧ៏")] = bstack11l1l1lll1l_opy_
        else:
            bstack11l1l1llll1_opy_[bstack1ll1l1lll1_opy_] = bstack11l1l1lllll_opy_
    @staticmethod
    def bstack11ll11l1111_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1ll11ll1l1l_opy_._11l1l1ll111_opy_
    @staticmethod
    def bstack11l1l1l1lll_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1ll11ll1l1l_opy_._11l1l1ll1ll_opy_
    @staticmethod
    def bstack11l1l1ll11l_opy_(bstack11l1l1ll1l1_opy_: str) -> List[str]:
        bstack11ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡵࡲࡩࡵࡵࠣࡸ࡭࡫ࠠࡪࡰࡳࡹࡹࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡢࡺࠢࡦࡳࡲࡳࡡࡴࠢࡺ࡬࡮ࡲࡥࠡࡴࡨࡷࡵ࡫ࡣࡵ࡫ࡱ࡫ࠥࡪ࡯ࡶࡤ࡯ࡩ࠲ࡷࡵࡰࡶࡨࡨࠥࡹࡵࡣࡵࡷࡶ࡮ࡴࡧࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡧࡻࡥࡲࡶ࡬ࡦ࠼ࠣࠫࡦ࠲ࠠࠣࡤ࠯ࡧࠧ࠲ࠠࡥࠩࠣ࠱ࡃ࡛ࠦࠨࡣࠪ࠰ࠥ࠭ࡢ࠭ࡥࠪ࠰ࠥ࠭ࡤࠨ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ័")
        pattern = re.compile(bstack11ll111_opy_ (u"ࡲࠨࠤࠫ࡟ࡣࠨ࡝ࠫࠫࠥࢀ࠭ࡡ࡞࠭࡟࠮࠭ࠬ៑"))
        result = []
        for match in pattern.finditer(bstack11l1l1ll1l1_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack11ll111_opy_ (u"ࠣࡗࡷ࡭ࡱ࡯ࡴࡺࠢࡦࡰࡦࡹࡳࠡࡵ࡫ࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡵ࡫ࡤࡸࡪࡪ្ࠢ"))