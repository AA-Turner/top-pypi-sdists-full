# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l11lll1lll_opy_:
    bstack1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡵࡵ࡫࡯࡭ࡹࡿࠠ࡮ࡧࡷ࡬ࡴࡪࡳࠡࡶࡲࠤࡸ࡫ࡴࠡࡣࡱࡨࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࠤࡲ࡫ࡴࡢࡦࡤࡸࡦ࠴ࠊࠡࠢࠣࠤࡎࡺࠠ࡮ࡣ࡬ࡲࡹࡧࡩ࡯ࡵࠣࡸࡼࡵࠠࡴࡧࡳࡥࡷࡧࡴࡦࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡩࡦࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡦࡴࡤࠡࡤࡸ࡭ࡱࡪࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶ࠲ࠏࠦࠠࠡࠢࡈࡥࡨ࡮ࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡨࡲࡹࡸࡹࠡ࡫ࡶࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦࡴࡰࠢࡥࡩࠥࡹࡴࡳࡷࡦࡸࡺࡸࡥࡥࠢࡤࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦ࡫ࡦࡻ࠽ࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦ࡫࡯ࡥ࡭ࡦࡢࡸࡾࡶࡥࠣ࠼ࠣࠦࡲࡻ࡬ࡵ࡫ࡢࡨࡷࡵࡰࡥࡱࡺࡲࠧ࠲ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡼࡡ࡭ࡷࡨࡷࠧࡀࠠ࡜࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡥ࡬ࠦࡶࡢ࡮ࡸࡩࡸࡣࠊࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠢࠣࠤᯐ")
    _111l11l11ll_opy_: Dict[str, Dict[str, Any]] = {}
    _111l111ll1l_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack111l1111l_opy_: str, key_value: str, bstack111l11l1l1l_opy_: bool = False) -> None:
        if not bstack111l1111l_opy_ or not key_value or bstack111l1111l_opy_.strip() == bstack1ll_opy_ (u"ࠤࠥᯑ") or key_value.strip() == bstack1ll_opy_ (u"ࠥࠦᯒ"):
            logger.error(bstack1ll_opy_ (u"ࠦࡰ࡫ࡹࡠࡰࡤࡱࡪࠦࡡ࡯ࡦࠣ࡯ࡪࡿ࡟ࡷࡣ࡯ࡹࡪࠦ࡭ࡶࡵࡷࠤࡧ࡫ࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡤࡲࡩࠦ࡮ࡰࡰ࠰ࡩࡲࡶࡴࡺࠤᯓ"))
        values: List[str] = bstack1l11lll1lll_opy_.bstack111l111lll1_opy_(key_value)
        bstack111l111ll11_opy_ = {bstack1ll_opy_ (u"ࠧ࡬ࡩࡦ࡮ࡧࡣࡹࡿࡰࡦࠤᯔ"): bstack1ll_opy_ (u"ࠨ࡭ࡶ࡮ࡷ࡭ࡤࡪࡲࡰࡲࡧࡳࡼࡴࠢᯕ"), bstack1ll_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢᯖ"): values}
        bstack111l11l11l1_opy_ = bstack1l11lll1lll_opy_._111l111ll1l_opy_ if bstack111l11l1l1l_opy_ else bstack1l11lll1lll_opy_._111l11l11ll_opy_
        if bstack111l1111l_opy_ in bstack111l11l11l1_opy_:
            bstack111l11l111l_opy_ = bstack111l11l11l1_opy_[bstack111l1111l_opy_]
            bstack111l11l1111_opy_ = bstack111l11l111l_opy_.get(bstack1ll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳࠣᯗ"), [])
            for val in values:
                if val not in bstack111l11l1111_opy_:
                    bstack111l11l1111_opy_.append(val)
            bstack111l11l111l_opy_[bstack1ll_opy_ (u"ࠤࡹࡥࡱࡻࡥࡴࠤᯘ")] = bstack111l11l1111_opy_
        else:
            bstack111l11l11l1_opy_[bstack111l1111l_opy_] = bstack111l111ll11_opy_
    @staticmethod
    def bstack11l111111l1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l11lll1lll_opy_._111l11l11ll_opy_
    @staticmethod
    def bstack111llll11l1_opy_() -> None:
        bstack1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄ࡮ࡨࡥࡷࠦࡡ࡭࡮ࠣࡸࡪࡹࡴ࠮࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥࡧࡣࡤࡷࡰࡹࡱࡧࡴࡦࡦࠣࡷࡴࠦࡦࡢࡴ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡓࡵࡴࡶࠣࡦࡪࠦࡣࡢ࡮࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥ࡫ࡡࡤࡪࠣࡸࡪࡹࡴࠨࡵࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡤࡱࡱࡷࡺࡳࡥࡥࠢࡤࡲࡩࠦࡳࡦࡰࡷ࠰ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡳࡰࠢࡷ࡬ࡦࡺࠠࡴࡷࡥࡷࡪࡷࡵࡦࡰࡷࠤࡹ࡫ࡳࡵࡵࠣࡨࡴࠦ࡮ࡰࡶࠣ࡭ࡳ࡮ࡥࡳ࡫ࡷࠤࡹࡧࡧࡴࠢࡩࡶࡴࡳࠠࡱࡴࡨࡺ࡮ࡵࡵࡴࠢࡷࡩࡸࡺࡳ࠯ࠌࠣࠤ࡙ࠥࠦࠠࠡࠢࠣࡸ࡫ࡳࠡࡴࡨࡥࡸࡹࡩࡨࡰࡰࡩࡳࡺࠠࠩࡰࡲࡸࠥࡪࡩࡤࡶ࠱ࡧࡱ࡫ࡡࡳࠫࠣࡸࡴࠦࡡࡷࡱ࡬ࡨࠥࡳࡵࡵࡣࡷ࡭ࡳ࡭ࠠࡢࡰࡼࠤࡱ࡯ࡶࡦࠢࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡨࡦ࡮ࡧࠤࡧࡿࠠࡢࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡵࡪࡤࡸࠥࡽࡡࡴࠢࡶࡩࡹࠦࡶࡪࡣࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹࠨࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᯙ")
        bstack1l11lll1lll_opy_._111l11l11ll_opy_ = {}
    @staticmethod
    def bstack111l111llll_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l11lll1lll_opy_._111l111ll1l_opy_
    @staticmethod
    def bstack111l111lll1_opy_(bstack111l11l1l11_opy_: str) -> List[str]:
        bstack1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡳࡰ࡮ࡺࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡱࡷࡷࠤࡸࡺࡲࡪࡰࡪࠤࡧࡿࠠࡤࡱࡰࡱࡦࡹࠠࡸࡪ࡬ࡰࡪࠦࡲࡦࡵࡳࡩࡨࡺࡩ࡯ࡩࠣࡨࡴࡻࡢ࡭ࡧ࠰ࡵࡺࡵࡴࡦࡦࠣࡷࡺࡨࡳࡵࡴ࡬ࡲ࡬ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡥࡹࡣࡰࡴࡱ࡫࠺ࠡࠩࡤ࠰ࠥࠨࡢ࠭ࡥࠥ࠰ࠥࡪࠧࠡ࠯ࡁࠤࡠ࠭ࡡࠨ࠮ࠣࠫࡧ࠲ࡣࠨ࠮ࠣࠫࡩ࠭࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᯚ")
        pattern = re.compile(bstack1ll_opy_ (u"ࡷ࠭ࠢࠩ࡝ࡡࠦࡢ࠰ࠩࠣࡾࠫ࡟ࡣ࠲࡝ࠬࠫࠪᯛ"))
        result = []
        for match in pattern.finditer(bstack111l11l1l11_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1ll_opy_ (u"ࠨࡕࡵ࡫࡯࡭ࡹࡿࠠࡤ࡮ࡤࡷࡸࠦࡳࡩࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡩ࡯ࡵࡷࡥࡳࡺࡩࡢࡶࡨࡨࠧᯜ"))