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
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l11ll1111l_opy_:
    bstack111ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡵࡵ࡫࡯࡭ࡹࡿࠠ࡮ࡧࡷ࡬ࡴࡪࡳࠡࡶࡲࠤࡸ࡫ࡴࠡࡣࡱࡨࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࠤࡲ࡫ࡴࡢࡦࡤࡸࡦ࠴ࠊࠡࠢࠣࠤࡎࡺࠠ࡮ࡣ࡬ࡲࡹࡧࡩ࡯ࡵࠣࡸࡼࡵࠠࡴࡧࡳࡥࡷࡧࡴࡦࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡩࡦࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡦࡴࡤࠡࡤࡸ࡭ࡱࡪࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶ࠲ࠏࠦࠠࠡࠢࡈࡥࡨ࡮ࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡨࡲࡹࡸࡹࠡ࡫ࡶࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦࡴࡰࠢࡥࡩࠥࡹࡴࡳࡷࡦࡸࡺࡸࡥࡥࠢࡤࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦ࡫ࡦࡻ࠽ࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦ࡫࡯ࡥ࡭ࡦࡢࡸࡾࡶࡥࠣ࠼ࠣࠦࡲࡻ࡬ࡵ࡫ࡢࡨࡷࡵࡰࡥࡱࡺࡲࠧ࠲ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡼࡡ࡭ࡷࡨࡷࠧࡀࠠ࡜࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡥ࡬ࠦࡶࡢ࡮ࡸࡩࡸࡣࠊࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠢࠣࠤ᯺")
    _111l111ll1l_opy_: Dict[str, Dict[str, Any]] = {}
    _111l111l111_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1111l1lll1_opy_: str, key_value: str, bstack111l111l11l_opy_: bool = False) -> None:
        if not bstack1111l1lll1_opy_ or not key_value or bstack1111l1lll1_opy_.strip() == bstack111ll_opy_ (u"ࠤࠥ᯻") or key_value.strip() == bstack111ll_opy_ (u"ࠥࠦ᯼"):
            logger.error(bstack111ll_opy_ (u"ࠦࡰ࡫ࡹࡠࡰࡤࡱࡪࠦࡡ࡯ࡦࠣ࡯ࡪࡿ࡟ࡷࡣ࡯ࡹࡪࠦ࡭ࡶࡵࡷࠤࡧ࡫ࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡤࡲࡩࠦ࡮ࡰࡰ࠰ࡩࡲࡶࡴࡺࠤ᯽"))
        values: List[str] = bstack1l11ll1111l_opy_.bstack111l111l1ll_opy_(key_value)
        bstack111l111l1l1_opy_ = {bstack111ll_opy_ (u"ࠧ࡬ࡩࡦ࡮ࡧࡣࡹࡿࡰࡦࠤ᯾"): bstack111ll_opy_ (u"ࠨ࡭ࡶ࡮ࡷ࡭ࡤࡪࡲࡰࡲࡧࡳࡼࡴࠢ᯿"), bstack111ll_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢᰀ"): values}
        bstack111l1111ll1_opy_ = bstack1l11ll1111l_opy_._111l111l111_opy_ if bstack111l111l11l_opy_ else bstack1l11ll1111l_opy_._111l111ll1l_opy_
        if bstack1111l1lll1_opy_ in bstack111l1111ll1_opy_:
            bstack111l1111l1l_opy_ = bstack111l1111ll1_opy_[bstack1111l1lll1_opy_]
            bstack111l1111lll_opy_ = bstack111l1111l1l_opy_.get(bstack111ll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳࠣᰁ"), [])
            for val in values:
                if val not in bstack111l1111lll_opy_:
                    bstack111l1111lll_opy_.append(val)
            bstack111l1111l1l_opy_[bstack111ll_opy_ (u"ࠤࡹࡥࡱࡻࡥࡴࠤᰂ")] = bstack111l1111lll_opy_
        else:
            bstack111l1111ll1_opy_[bstack1111l1lll1_opy_] = bstack111l111l1l1_opy_
    @staticmethod
    def bstack11l11111ll1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l11ll1111l_opy_._111l111ll1l_opy_
    @staticmethod
    def bstack111lll11lll_opy_() -> None:
        bstack111ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄ࡮ࡨࡥࡷࠦࡡ࡭࡮ࠣࡸࡪࡹࡴ࠮࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥࡧࡣࡤࡷࡰࡹࡱࡧࡴࡦࡦࠣࡷࡴࠦࡦࡢࡴ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡓࡵࡴࡶࠣࡦࡪࠦࡣࡢ࡮࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥ࡫ࡡࡤࡪࠣࡸࡪࡹࡴࠨࡵࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡤࡱࡱࡷࡺࡳࡥࡥࠢࡤࡲࡩࠦࡳࡦࡰࡷ࠰ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡳࡰࠢࡷ࡬ࡦࡺࠠࡴࡷࡥࡷࡪࡷࡵࡦࡰࡷࠤࡹ࡫ࡳࡵࡵࠣࡨࡴࠦ࡮ࡰࡶࠣ࡭ࡳ࡮ࡥࡳ࡫ࡷࠤࡹࡧࡧࡴࠢࡩࡶࡴࡳࠠࡱࡴࡨࡺ࡮ࡵࡵࡴࠢࡷࡩࡸࡺࡳ࠯ࠌࠣࠤ࡙ࠥࠦࠠࠡࠢࠣࡸ࡫ࡳࠡࡴࡨࡥࡸࡹࡩࡨࡰࡰࡩࡳࡺࠠࠩࡰࡲࡸࠥࡪࡩࡤࡶ࠱ࡧࡱ࡫ࡡࡳࠫࠣࡸࡴࠦࡡࡷࡱ࡬ࡨࠥࡳࡵࡵࡣࡷ࡭ࡳ࡭ࠠࡢࡰࡼࠤࡱ࡯ࡶࡦࠢࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡨࡦ࡮ࡧࠤࡧࡿࠠࡢࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡵࡪࡤࡸࠥࡽࡡࡴࠢࡶࡩࡹࠦࡶࡪࡣࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹࠨࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᰃ")
        bstack1l11ll1111l_opy_._111l111ll1l_opy_ = {}
    @staticmethod
    def bstack111l111ll11_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l11ll1111l_opy_._111l111l111_opy_
    @staticmethod
    def bstack111l111l1ll_opy_(bstack111l111lll1_opy_: str) -> List[str]:
        bstack111ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡳࡰ࡮ࡺࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡱࡷࡷࠤࡸࡺࡲࡪࡰࡪࠤࡧࡿࠠࡤࡱࡰࡱࡦࡹࠠࡸࡪ࡬ࡰࡪࠦࡲࡦࡵࡳࡩࡨࡺࡩ࡯ࡩࠣࡨࡴࡻࡢ࡭ࡧ࠰ࡵࡺࡵࡴࡦࡦࠣࡷࡺࡨࡳࡵࡴ࡬ࡲ࡬ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡥࡹࡣࡰࡴࡱ࡫࠺ࠡࠩࡤ࠰ࠥࠨࡢ࠭ࡥࠥ࠰ࠥࡪࠧࠡ࠯ࡁࠤࡠ࠭ࡡࠨ࠮ࠣࠫࡧ࠲ࡣࠨ࠮ࠣࠫࡩ࠭࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᰄ")
        pattern = re.compile(bstack111ll_opy_ (u"ࡷ࠭ࠢࠩ࡝ࡡࠦࡢ࠰ࠩࠣࡾࠫ࡟ࡣ࠲࡝ࠬࠫࠪᰅ"))
        result = []
        for match in pattern.finditer(bstack111l111lll1_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack111ll_opy_ (u"ࠨࡕࡵ࡫࡯࡭ࡹࡿࠠࡤ࡮ࡤࡷࡸࠦࡳࡩࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡩ࡯ࡵࡷࡥࡳࡺࡩࡢࡶࡨࡨࠧᰆ"))