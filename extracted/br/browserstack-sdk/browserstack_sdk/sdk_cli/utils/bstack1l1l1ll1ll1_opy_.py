# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l1l111111l_opy_:
    bstack1ll1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡲࡵࡳࡻ࡯ࡤࡦࡵࠣࡹࡹ࡯࡬ࡪࡶࡼࠤࡲ࡫ࡴࡩࡱࡧࡷࠥࡺ࡯ࠡࡵࡨࡸࠥࡧ࡮ࡥࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࠡ࡯ࡨࡸࡦࡪࡡࡵࡣ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡲࡧࡩ࡯ࡶࡤ࡭ࡳࡹࠠࡵࡹࡲࠤࡸ࡫ࡰࡢࡴࡤࡸࡪࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵ࡭ࡪࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡱࡨࠥࡨࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࡅࡢࡥ࡫ࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡥ࡯ࡶࡵࡽࠥ࡯ࡳࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࡸࡴࠦࡢࡦࠢࡶࡸࡷࡻࡣࡵࡷࡵࡩࡩࠦࡡࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣ࡯ࡪࡿ࠺ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡨ࡬ࡩࡱࡪ࡟ࡵࡻࡳࡩࠧࡀࠠࠣ࡯ࡸࡰࡹ࡯࡟ࡥࡴࡲࡴࡩࡵࡷ࡯ࠤ࠯ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡹࡥࡱࡻࡥࡴࠤ࠽ࠤࡠࡲࡩࡴࡶࠣࡳ࡫ࠦࡴࡢࡩࠣࡺࡦࡲࡵࡦࡵࡠࠎࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨᯍ")
    _111l11l1lll_opy_: Dict[str, Dict[str, Any]] = {}
    _111l11l1l11_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1l1l1l111l_opy_: str, key_value: str, bstack111l11l1ll1_opy_: bool = False) -> None:
        if not bstack1l1l1l111l_opy_ or not key_value or bstack1l1l1l111l_opy_.strip() == bstack1ll1l11_opy_ (u"ࠨࠢᯎ") or key_value.strip() == bstack1ll1l11_opy_ (u"ࠢࠣᯏ"):
            logger.error(bstack1ll1l11_opy_ (u"ࠣ࡭ࡨࡽࡤࡴࡡ࡮ࡧࠣࡥࡳࡪࠠ࡬ࡧࡼࡣࡻࡧ࡬ࡶࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡡ࡯ࡦࠣࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠨᯐ"))
        values: List[str] = bstack1l1l111111l_opy_.bstack111l11l11ll_opy_(key_value)
        bstack111l11ll1l1_opy_ = {bstack1ll1l11_opy_ (u"ࠤࡩ࡭ࡪࡲࡤࡠࡶࡼࡴࡪࠨᯑ"): bstack1ll1l11_opy_ (u"ࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦᯒ"), bstack1ll1l11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦᯓ"): values}
        bstack111l11ll1ll_opy_ = bstack1l1l111111l_opy_._111l11l1l11_opy_ if bstack111l11l1ll1_opy_ else bstack1l1l111111l_opy_._111l11l1lll_opy_
        if bstack1l1l1l111l_opy_ in bstack111l11ll1ll_opy_:
            bstack111l11l11l1_opy_ = bstack111l11ll1ll_opy_[bstack1l1l1l111l_opy_]
            bstack111l11l1l1l_opy_ = bstack111l11l11l1_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧᯔ"), [])
            for val in values:
                if val not in bstack111l11l1l1l_opy_:
                    bstack111l11l1l1l_opy_.append(val)
            bstack111l11l11l1_opy_[bstack1ll1l11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᯕ")] = bstack111l11l1l1l_opy_
        else:
            bstack111l11ll1ll_opy_[bstack1l1l1l111l_opy_] = bstack111l11ll1l1_opy_
    @staticmethod
    def bstack111lll1ll11_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1l111111l_opy_._111l11l1lll_opy_
    @staticmethod
    def bstack111l11ll111_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1l111111l_opy_._111l11l1l11_opy_
    @staticmethod
    def bstack111l11l11ll_opy_(bstack111l11ll11l_opy_: str) -> List[str]:
        bstack1ll1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘࡶ࡬ࡪࡶࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡴࡺࡺࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡣࡻࠣࡧࡴࡳ࡭ࡢࡵࠣࡻ࡭࡯࡬ࡦࠢࡵࡩࡸࡶࡥࡤࡶ࡬ࡲ࡬ࠦࡤࡰࡷࡥࡰࡪ࠳ࡱࡶࡱࡷࡩࡩࠦࡳࡶࡤࡶࡸࡷ࡯࡮ࡨࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡨࡼࡦࡳࡰ࡭ࡧ࠽ࠤࠬࡧࠬࠡࠤࡥ࠰ࡨࠨࠬࠡࡦࠪࠤ࠲ࡄࠠ࡜ࠩࡤࠫ࠱ࠦࠧࡣ࠮ࡦࠫ࠱ࠦࠧࡥࠩࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᯖ")
        pattern = re.compile(bstack1ll1l11_opy_ (u"ࡳࠩࠥࠬࡠࡤࠢ࡞ࠬࠬࠦࢁ࠮࡛࡟࠮ࡠ࠯࠮࠭ᯗ"))
        result = []
        for match in pattern.finditer(bstack111l11ll11l_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1ll1l11_opy_ (u"ࠤࡘࡸ࡮ࡲࡩࡵࡻࠣࡧࡱࡧࡳࡴࠢࡶ࡬ࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡶ࡬ࡥࡹ࡫ࡤࠣᯘ"))