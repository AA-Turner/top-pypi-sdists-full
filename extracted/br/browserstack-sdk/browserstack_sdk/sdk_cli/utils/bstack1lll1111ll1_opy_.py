# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.bstack1l1111l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack1ll1ll1ll11_opy_:
    bstack11l1ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡲࡵࡳࡻ࡯ࡤࡦࡵࠣࡹࡹ࡯࡬ࡪࡶࡼࠤࡲ࡫ࡴࡩࡱࡧࡷࠥࡺ࡯ࠡࡵࡨࡸࠥࡧ࡮ࡥࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࠡ࡯ࡨࡸࡦࡪࡡࡵࡣ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡲࡧࡩ࡯ࡶࡤ࡭ࡳࡹࠠࡵࡹࡲࠤࡸ࡫ࡰࡢࡴࡤࡸࡪࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵ࡭ࡪࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡱࡨࠥࡨࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࡅࡢࡥ࡫ࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡥ࡯ࡶࡵࡽࠥ࡯ࡳࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࡸࡴࠦࡢࡦࠢࡶࡸࡷࡻࡣࡵࡷࡵࡩࡩࠦࡡࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣ࡯ࡪࡿ࠺ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡨ࡬ࡩࡱࡪ࡟ࡵࡻࡳࡩࠧࡀࠠࠣ࡯ࡸࡰࡹ࡯࡟ࡥࡴࡲࡴࡩࡵࡷ࡯ࠤ࠯ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡹࡥࡱࡻࡥࡴࠤ࠽ࠤࡠࡲࡩࡴࡶࠣࡳ࡫ࠦࡴࡢࡩࠣࡺࡦࡲࡵࡦࡵࡠࠎࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨᛶ")
    _11ll1111l1l_opy_: Dict[str, Dict[str, Any]] = {}
    _11ll111l1l1_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack11l11ll1_opy_: str, key_value: str, bstack11ll1111l11_opy_: bool = False) -> None:
        if not bstack11l11ll1_opy_ or not key_value or bstack11l11ll1_opy_.strip() == bstack11l1ll1_opy_ (u"ࠨࠢᛷ") or key_value.strip() == bstack11l1ll1_opy_ (u"ࠢࠣᛸ"):
            logger.error(bstack11l1ll1_opy_ (u"ࠣ࡭ࡨࡽࡤࡴࡡ࡮ࡧࠣࡥࡳࡪࠠ࡬ࡧࡼࡣࡻࡧ࡬ࡶࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡡ࡯ࡦࠣࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠨ᛹"))
        values: List[str] = bstack1ll1ll1ll11_opy_.bstack11ll111l11l_opy_(key_value)
        bstack11ll11111l1_opy_ = {bstack11l1ll1_opy_ (u"ࠤࡩ࡭ࡪࡲࡤࡠࡶࡼࡴࡪࠨ᛺"): bstack11l1ll1_opy_ (u"ࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦ᛻"), bstack11l1ll1_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦ᛼"): values}
        bstack11ll111l1ll_opy_ = bstack1ll1ll1ll11_opy_._11ll111l1l1_opy_ if bstack11ll1111l11_opy_ else bstack1ll1ll1ll11_opy_._11ll1111l1l_opy_
        if bstack11l11ll1_opy_ in bstack11ll111l1ll_opy_:
            bstack11ll11111ll_opy_ = bstack11ll111l1ll_opy_[bstack11l11ll1_opy_]
            bstack11ll1111ll1_opy_ = bstack11ll11111ll_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧ᛽"), [])
            for val in values:
                if val not in bstack11ll1111ll1_opy_:
                    bstack11ll1111ll1_opy_.append(val)
            bstack11ll11111ll_opy_[bstack11l1ll1_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨ᛾")] = bstack11ll1111ll1_opy_
        else:
            bstack11ll111l1ll_opy_[bstack11l11ll1_opy_] = bstack11ll11111l1_opy_
    @staticmethod
    def bstack11ll1l111l1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1ll1ll1ll11_opy_._11ll1111l1l_opy_
    @staticmethod
    def bstack11ll111l111_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1ll1ll1ll11_opy_._11ll111l1l1_opy_
    @staticmethod
    def bstack11ll111l11l_opy_(bstack11ll1111lll_opy_: str) -> List[str]:
        bstack11l1ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘࡶ࡬ࡪࡶࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡴࡺࡺࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡣࡻࠣࡧࡴࡳ࡭ࡢࡵࠣࡻ࡭࡯࡬ࡦࠢࡵࡩࡸࡶࡥࡤࡶ࡬ࡲ࡬ࠦࡤࡰࡷࡥࡰࡪ࠳ࡱࡶࡱࡷࡩࡩࠦࡳࡶࡤࡶࡸࡷ࡯࡮ࡨࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡨࡼࡦࡳࡰ࡭ࡧ࠽ࠤࠬࡧࠬࠡࠤࡥ࠰ࡨࠨࠬࠡࡦࠪࠤ࠲ࡄࠠ࡜ࠩࡤࠫ࠱ࠦࠧࡣ࠮ࡦࠫ࠱ࠦࠧࡥࠩࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᛿")
        pattern = re.compile(bstack11l1ll1_opy_ (u"ࡳࠩࠥࠬࡠࡤࠢ࡞ࠬࠬࠦࢁ࠮࡛࡟࠮ࡠ࠯࠮࠭ᜀ"))
        result = []
        for match in pattern.finditer(bstack11ll1111lll_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack11l1ll1_opy_ (u"ࠤࡘࡸ࡮ࡲࡩࡵࡻࠣࡧࡱࡧࡳࡴࠢࡶ࡬ࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡶ࡬ࡥࡹ࡫ࡤࠣᜁ"))