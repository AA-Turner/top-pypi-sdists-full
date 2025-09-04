# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.bstack11l1111l1_opy_ import get_logger
logger = get_logger(__name__)
class bstack1ll1lll11l1_opy_:
    bstack1111l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡳࡶࡴࡼࡩࡥࡧࡶࠤࡺࡺࡩ࡭࡫ࡷࡽࠥࡳࡥࡵࡪࡲࡨࡸࠦࡴࡰࠢࡶࡩࡹࠦࡡ࡯ࡦࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࠢࡰࡩࡹࡧࡤࡢࡶࡤ࠲ࠏࠦࠠࠡࠢࡌࡸࠥࡳࡡࡪࡰࡷࡥ࡮ࡴࡳࠡࡶࡺࡳࠥࡹࡥࡱࡣࡵࡥࡹ࡫ࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶ࡮࡫ࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡤࡲࡩࠦࡢࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴ࠰ࠍࠤࠥࠦࠠࡆࡣࡦ࡬ࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡦࡰࡷࡶࡾࠦࡩࡴࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡹࡵࠠࡣࡧࠣࡷࡹࡸࡵࡤࡶࡸࡶࡪࡪࠠࡢࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࡰ࡫ࡹ࠻ࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡩ࡭ࡪࡲࡤࡠࡶࡼࡴࡪࠨ࠺ࠡࠤࡰࡹࡱࡺࡩࡠࡦࡵࡳࡵࡪ࡯ࡸࡰࠥ࠰ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡺࡦࡲࡵࡦࡵࠥ࠾ࠥࡡ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡵࡣࡪࠤࡻࡧ࡬ࡶࡧࡶࡡࠏࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠧࠨࠢᗦ")
    _11lll1l1ll1_opy_: Dict[str, Dict[str, Any]] = {}
    _11lll1ll11l_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack11l11l1ll1_opy_: str, key_value: str, bstack11lll1l1lll_opy_: bool = False) -> None:
        if not bstack11l11l1ll1_opy_ or not key_value or bstack11l11l1ll1_opy_.strip() == bstack1111l1l_opy_ (u"ࠢࠣᗧ") or key_value.strip() == bstack1111l1l_opy_ (u"ࠣࠤᗨ"):
            logger.error(bstack1111l1l_opy_ (u"ࠤ࡮ࡩࡾࡥ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡ࡭ࡨࡽࡤࡼࡡ࡭ࡷࡨࠤࡲࡻࡳࡵࠢࡥࡩࠥࡴ࡯࡯࠯ࡱࡹࡱࡲࠠࡢࡰࡧࠤࡳࡵ࡮࠮ࡧࡰࡴࡹࡿࠢᗩ"))
        values: List[str] = bstack1ll1lll11l1_opy_.bstack11lll1ll1l1_opy_(key_value)
        bstack11lll1ll111_opy_ = {bstack1111l1l_opy_ (u"ࠥࡪ࡮࡫࡬ࡥࡡࡷࡽࡵ࡫ࠢᗪ"): bstack1111l1l_opy_ (u"ࠦࡲࡻ࡬ࡵ࡫ࡢࡨࡷࡵࡰࡥࡱࡺࡲࠧᗫ"), bstack1111l1l_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧᗬ"): values}
        bstack11lll1lll11_opy_ = bstack1ll1lll11l1_opy_._11lll1ll11l_opy_ if bstack11lll1l1lll_opy_ else bstack1ll1lll11l1_opy_._11lll1l1ll1_opy_
        if bstack11l11l1ll1_opy_ in bstack11lll1lll11_opy_:
            bstack11lll1ll1ll_opy_ = bstack11lll1lll11_opy_[bstack11l11l1ll1_opy_]
            bstack11lll1lllll_opy_ = bstack11lll1ll1ll_opy_.get(bstack1111l1l_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᗭ"), [])
            for val in values:
                if val not in bstack11lll1lllll_opy_:
                    bstack11lll1lllll_opy_.append(val)
            bstack11lll1ll1ll_opy_[bstack1111l1l_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢᗮ")] = bstack11lll1lllll_opy_
        else:
            bstack11lll1lll11_opy_[bstack11l11l1ll1_opy_] = bstack11lll1ll111_opy_
    @staticmethod
    def bstack1l111lll1ll_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1ll1lll11l1_opy_._11lll1l1ll1_opy_
    @staticmethod
    def bstack11lll1lll1l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1ll1lll11l1_opy_._11lll1ll11l_opy_
    @staticmethod
    def bstack11lll1ll1l1_opy_(bstack11lll1llll1_opy_: str) -> List[str]:
        bstack1111l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡰ࡭࡫ࡷࡷࠥࡺࡨࡦࠢ࡬ࡲࡵࡻࡴࠡࡵࡷࡶ࡮ࡴࡧࠡࡤࡼࠤࡨࡵ࡭࡮ࡣࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡪࡹࡰࡦࡥࡷ࡭ࡳ࡭ࠠࡥࡱࡸࡦࡱ࡫࠭ࡲࡷࡲࡸࡪࡪࠠࡴࡷࡥࡷࡹࡸࡩ࡯ࡩࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡩࡽࡧ࡭ࡱ࡮ࡨ࠾ࠥ࠭ࡡ࠭ࠢࠥࡦ࠱ࡩࠢ࠭ࠢࡧࠫࠥ࠳࠾ࠡ࡝ࠪࡥࠬ࠲ࠠࠨࡤ࠯ࡧࠬ࠲ࠠࠨࡦࠪࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᗯ")
        pattern = re.compile(bstack1111l1l_opy_ (u"ࡴࠪࠦ࠭ࡡ࡞ࠣ࡟࠭࠭ࠧࢂࠨ࡜ࡠ࠯ࡡ࠰࠯ࠧᗰ"))
        result = []
        for match in pattern.finditer(bstack11lll1llll1_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1111l1l_opy_ (u"࡙ࠥࡹ࡯࡬ࡪࡶࡼࠤࡨࡲࡡࡴࡵࠣࡷ࡭ࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣ࡭ࡳࡹࡴࡢࡰࡷ࡭ࡦࡺࡥࡥࠤᗱ"))