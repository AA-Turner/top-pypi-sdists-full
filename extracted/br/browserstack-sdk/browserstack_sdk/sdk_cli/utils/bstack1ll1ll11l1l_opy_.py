# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.bstack1l1ll11lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lll11llll1_opy_:
    bstack1l11l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡵࡵ࡫࡯࡭ࡹࡿࠠ࡮ࡧࡷ࡬ࡴࡪࡳࠡࡶࡲࠤࡸ࡫ࡴࠡࡣࡱࡨࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࠤࡲ࡫ࡴࡢࡦࡤࡸࡦ࠴ࠊࠡࠢࠣࠤࡎࡺࠠ࡮ࡣ࡬ࡲࡹࡧࡩ࡯ࡵࠣࡸࡼࡵࠠࡴࡧࡳࡥࡷࡧࡴࡦࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡩࡦࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡦࡴࡤࠡࡤࡸ࡭ࡱࡪࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶ࠲ࠏࠦࠠࠡࠢࡈࡥࡨ࡮ࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡨࡲࡹࡸࡹࠡ࡫ࡶࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦࡴࡰࠢࡥࡩࠥࡹࡴࡳࡷࡦࡸࡺࡸࡥࡥࠢࡤࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦ࡫ࡦࡻ࠽ࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦ࡫࡯ࡥ࡭ࡦࡢࡸࡾࡶࡥࠣ࠼ࠣࠦࡲࡻ࡬ࡵ࡫ࡢࡨࡷࡵࡰࡥࡱࡺࡲࠧ࠲ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡼࡡ࡭ࡷࡨࡷࠧࡀࠠ࡜࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡥ࡬ࠦࡶࡢ࡮ࡸࡩࡸࡣࠊࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠢࠣࠤᗚ")
    _11lll1ll11l_opy_: Dict[str, Dict[str, Any]] = {}
    _11lll1ll1l1_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1ll1ll11l_opy_: str, key_value: str, bstack11lll1ll111_opy_: bool = False) -> None:
        if not bstack1ll1ll11l_opy_ or not key_value or bstack1ll1ll11l_opy_.strip() == bstack1l11l11_opy_ (u"ࠤࠥᗛ") or key_value.strip() == bstack1l11l11_opy_ (u"ࠥࠦᗜ"):
            logger.error(bstack1l11l11_opy_ (u"ࠦࡰ࡫ࡹࡠࡰࡤࡱࡪࠦࡡ࡯ࡦࠣ࡯ࡪࡿ࡟ࡷࡣ࡯ࡹࡪࠦ࡭ࡶࡵࡷࠤࡧ࡫ࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡤࡲࡩࠦ࡮ࡰࡰ࠰ࡩࡲࡶࡴࡺࠤᗝ"))
        values: List[str] = bstack1lll11llll1_opy_.bstack11lll1ll1ll_opy_(key_value)
        bstack11llll11111_opy_ = {bstack1l11l11_opy_ (u"ࠧ࡬ࡩࡦ࡮ࡧࡣࡹࡿࡰࡦࠤᗞ"): bstack1l11l11_opy_ (u"ࠨ࡭ࡶ࡮ࡷ࡭ࡤࡪࡲࡰࡲࡧࡳࡼࡴࠢᗟ"), bstack1l11l11_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢᗠ"): values}
        bstack11llll1111l_opy_ = bstack1lll11llll1_opy_._11lll1ll1l1_opy_ if bstack11lll1ll111_opy_ else bstack1lll11llll1_opy_._11lll1ll11l_opy_
        if bstack1ll1ll11l_opy_ in bstack11llll1111l_opy_:
            bstack11lll1lllll_opy_ = bstack11llll1111l_opy_[bstack1ll1ll11l_opy_]
            bstack11lll1lll11_opy_ = bstack11lll1lllll_opy_.get(bstack1l11l11_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳࠣᗡ"), [])
            for val in values:
                if val not in bstack11lll1lll11_opy_:
                    bstack11lll1lll11_opy_.append(val)
            bstack11lll1lllll_opy_[bstack1l11l11_opy_ (u"ࠤࡹࡥࡱࡻࡥࡴࠤᗢ")] = bstack11lll1lll11_opy_
        else:
            bstack11llll1111l_opy_[bstack1ll1ll11l_opy_] = bstack11llll11111_opy_
    @staticmethod
    def bstack1l111ll11l1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll11llll1_opy_._11lll1ll11l_opy_
    @staticmethod
    def bstack11lll1llll1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll11llll1_opy_._11lll1ll1l1_opy_
    @staticmethod
    def bstack11lll1ll1ll_opy_(bstack11lll1lll1l_opy_: str) -> List[str]:
        bstack1l11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡲ࡯࡭ࡹࡹࠠࡵࡪࡨࠤ࡮ࡴࡰࡶࡶࠣࡷࡹࡸࡩ࡯ࡩࠣࡦࡾࠦࡣࡰ࡯ࡰࡥࡸࠦࡷࡩ࡫࡯ࡩࠥࡸࡥࡴࡲࡨࡧࡹ࡯࡮ࡨࠢࡧࡳࡺࡨ࡬ࡦ࠯ࡴࡹࡴࡺࡥࡥࠢࡶࡹࡧࡹࡴࡳ࡫ࡱ࡫ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥ࡫ࡸࡢ࡯ࡳࡰࡪࡀࠠࠨࡣ࠯ࠤࠧࡨࠬࡤࠤ࠯ࠤࡩ࠭ࠠ࠮ࡀࠣ࡟ࠬࡧࠧ࠭ࠢࠪࡦ࠱ࡩࠧ࠭ࠢࠪࡨࠬࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᗣ")
        pattern = re.compile(bstack1l11l11_opy_ (u"ࡶࠬࠨࠨ࡜ࡠࠥࡡ࠯࠯ࠢࡽࠪ࡞ࡢ࠱ࡣࠫࠪࠩᗤ"))
        result = []
        for match in pattern.finditer(bstack11lll1lll1l_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1l11l11_opy_ (u"࡛ࠧࡴࡪ࡮࡬ࡸࡾࠦࡣ࡭ࡣࡶࡷࠥࡹࡨࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥ࡯࡮ࡴࡶࡤࡲࡹ࡯ࡡࡵࡧࡧࠦᗥ"))