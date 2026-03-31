# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l1ll1l11ll_opy_:
    bstack1ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡲࡵࡳࡻ࡯ࡤࡦࡵࠣࡹࡹ࡯࡬ࡪࡶࡼࠤࡲ࡫ࡴࡩࡱࡧࡷࠥࡺ࡯ࠡࡵࡨࡸࠥࡧ࡮ࡥࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࠡ࡯ࡨࡸࡦࡪࡡࡵࡣ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡲࡧࡩ࡯ࡶࡤ࡭ࡳࡹࠠࡵࡹࡲࠤࡸ࡫ࡰࡢࡴࡤࡸࡪࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵ࡭ࡪࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡱࡨࠥࡨࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࡅࡢࡥ࡫ࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡥ࡯ࡶࡵࡽࠥ࡯ࡳࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࡸࡴࠦࡢࡦࠢࡶࡸࡷࡻࡣࡵࡷࡵࡩࡩࠦࡡࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣ࡯ࡪࡿ࠺ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡨ࡬ࡩࡱࡪ࡟ࡵࡻࡳࡩࠧࡀࠠࠣ࡯ࡸࡰࡹ࡯࡟ࡥࡴࡲࡴࡩࡵࡷ࡯ࠤ࠯ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡹࡥࡱࡻࡥࡴࠤ࠽ࠤࡠࡲࡩࡴࡶࠣࡳ࡫ࠦࡴࡢࡩࠣࡺࡦࡲࡵࡦࡵࡠࠎࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨᨆ")
    _11l1111111l_opy_: Dict[str, Dict[str, Any]] = {}
    _111lllllll1_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1l1l1l1lll_opy_: str, key_value: str, bstack11l111111ll_opy_: bool = False) -> None:
        if not bstack1l1l1l1lll_opy_ or not key_value or bstack1l1l1l1lll_opy_.strip() == bstack1ll11_opy_ (u"ࠨࠢᨇ") or key_value.strip() == bstack1ll11_opy_ (u"ࠢࠣᨈ"):
            logger.error(bstack1ll11_opy_ (u"ࠣ࡭ࡨࡽࡤࡴࡡ࡮ࡧࠣࡥࡳࡪࠠ࡬ࡧࡼࡣࡻࡧ࡬ࡶࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡡ࡯ࡦࠣࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠨᨉ"))
        values: List[str] = bstack1l1ll1l11ll_opy_.bstack11l11111l11_opy_(key_value)
        bstack11l111111l1_opy_ = {bstack1ll11_opy_ (u"ࠤࡩ࡭ࡪࡲࡤࡠࡶࡼࡴࡪࠨᨊ"): bstack1ll11_opy_ (u"ࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦᨋ"), bstack1ll11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦᨌ"): values}
        bstack111llllll1l_opy_ = bstack1l1ll1l11ll_opy_._111lllllll1_opy_ if bstack11l111111ll_opy_ else bstack1l1ll1l11ll_opy_._11l1111111l_opy_
        if bstack1l1l1l1lll_opy_ in bstack111llllll1l_opy_:
            bstack111llllll11_opy_ = bstack111llllll1l_opy_[bstack1l1l1l1lll_opy_]
            bstack11l11111l1l_opy_ = bstack111llllll11_opy_.get(bstack1ll11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧᨍ"), [])
            for val in values:
                if val not in bstack11l11111l1l_opy_:
                    bstack11l11111l1l_opy_.append(val)
            bstack111llllll11_opy_[bstack1ll11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᨎ")] = bstack11l11111l1l_opy_
        else:
            bstack111llllll1l_opy_[bstack1l1l1l1lll_opy_] = bstack11l111111l1_opy_
    @staticmethod
    def bstack11l1ll11l11_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1ll1l11ll_opy_._11l1111111l_opy_
    @staticmethod
    def bstack111llllllll_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1ll1l11ll_opy_._111lllllll1_opy_
    @staticmethod
    def bstack11l11111l11_opy_(bstack11l11111111_opy_: str) -> List[str]:
        bstack1ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘࡶ࡬ࡪࡶࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡴࡺࡺࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡣࡻࠣࡧࡴࡳ࡭ࡢࡵࠣࡻ࡭࡯࡬ࡦࠢࡵࡩࡸࡶࡥࡤࡶ࡬ࡲ࡬ࠦࡤࡰࡷࡥࡰࡪ࠳ࡱࡶࡱࡷࡩࡩࠦࡳࡶࡤࡶࡸࡷ࡯࡮ࡨࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡨࡼࡦࡳࡰ࡭ࡧ࠽ࠤࠬࡧࠬࠡࠤࡥ࠰ࡨࠨࠬࠡࡦࠪࠤ࠲ࡄࠠ࡜ࠩࡤࠫ࠱ࠦࠧࡣ࠮ࡦࠫ࠱ࠦࠧࡥࠩࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᨏ")
        pattern = re.compile(bstack1ll11_opy_ (u"ࡳࠩࠥࠬࡠࡤࠢ࡞ࠬࠬࠦࢁ࠮࡛࡟࠮ࡠ࠯࠮࠭ᨐ"))
        result = []
        for match in pattern.finditer(bstack11l11111111_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1ll11_opy_ (u"ࠤࡘࡸ࡮ࡲࡩࡵࡻࠣࡧࡱࡧࡳࡴࠢࡶ࡬ࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡶ࡬ࡥࡹ࡫ࡤࠣᨑ"))