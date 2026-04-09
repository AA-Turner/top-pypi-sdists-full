# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l1l1lll1l1_opy_:
    bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡲࡵࡳࡻ࡯ࡤࡦࡵࠣࡹࡹ࡯࡬ࡪࡶࡼࠤࡲ࡫ࡴࡩࡱࡧࡷࠥࡺ࡯ࠡࡵࡨࡸࠥࡧ࡮ࡥࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࠡ࡯ࡨࡸࡦࡪࡡࡵࡣ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡲࡧࡩ࡯ࡶࡤ࡭ࡳࡹࠠࡵࡹࡲࠤࡸ࡫ࡰࡢࡴࡤࡸࡪࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵ࡭ࡪࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡱࡨࠥࡨࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࡅࡢࡥ࡫ࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡥ࡯ࡶࡵࡽࠥ࡯ࡳࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࡸࡴࠦࡢࡦࠢࡶࡸࡷࡻࡣࡵࡷࡵࡩࡩࠦࡡࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣ࡯ࡪࡿ࠺ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡨ࡬ࡩࡱࡪ࡟ࡵࡻࡳࡩࠧࡀࠠࠣ࡯ࡸࡰࡹ࡯࡟ࡥࡴࡲࡴࡩࡵࡷ࡯ࠤ࠯ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡹࡥࡱࡻࡥࡴࠤ࠽ࠤࡠࡲࡩࡴࡶࠣࡳ࡫ࠦࡴࡢࡩࠣࡺࡦࡲࡵࡦࡵࡠࠎࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨᯍ")
    _111l11l1l11_opy_: Dict[str, Dict[str, Any]] = {}
    _111l11l1lll_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1llll1l1l1_opy_: str, key_value: str, bstack111l11l11ll_opy_: bool = False) -> None:
        if not bstack1llll1l1l1_opy_ or not key_value or bstack1llll1l1l1_opy_.strip() == bstack11ll11_opy_ (u"ࠨࠢᯎ") or key_value.strip() == bstack11ll11_opy_ (u"ࠢࠣᯏ"):
            logger.error(bstack11ll11_opy_ (u"ࠣ࡭ࡨࡽࡤࡴࡡ࡮ࡧࠣࡥࡳࡪࠠ࡬ࡧࡼࡣࡻࡧ࡬ࡶࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡡ࡯ࡦࠣࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠨᯐ"))
        values: List[str] = bstack1l1l1lll1l1_opy_.bstack111l11l1ll1_opy_(key_value)
        bstack111l11l111l_opy_ = {bstack11ll11_opy_ (u"ࠤࡩ࡭ࡪࡲࡤࡠࡶࡼࡴࡪࠨᯑ"): bstack11ll11_opy_ (u"ࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦᯒ"), bstack11ll11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦᯓ"): values}
        bstack111l11ll1l1_opy_ = bstack1l1l1lll1l1_opy_._111l11l1lll_opy_ if bstack111l11l11ll_opy_ else bstack1l1l1lll1l1_opy_._111l11l1l11_opy_
        if bstack1llll1l1l1_opy_ in bstack111l11ll1l1_opy_:
            bstack111l11l11l1_opy_ = bstack111l11ll1l1_opy_[bstack1llll1l1l1_opy_]
            bstack111l11l1l1l_opy_ = bstack111l11l11l1_opy_.get(bstack11ll11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧᯔ"), [])
            for val in values:
                if val not in bstack111l11l1l1l_opy_:
                    bstack111l11l1l1l_opy_.append(val)
            bstack111l11l11l1_opy_[bstack11ll11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᯕ")] = bstack111l11l1l1l_opy_
        else:
            bstack111l11ll1l1_opy_[bstack1llll1l1l1_opy_] = bstack111l11l111l_opy_
    @staticmethod
    def bstack111ll1l111l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1l1lll1l1_opy_._111l11l1l11_opy_
    @staticmethod
    def bstack11l111ll111_opy_() -> None:
        bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡲࡥࡢࡴࠣࡥࡱࡲࠠࡵࡧࡶࡸ࠲ࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡤࡧࡨࡻ࡭ࡶ࡮ࡤࡸࡪࡪࠠࡴࡱࠣࡪࡦࡸ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡐࡹࡸࡺࠠࡣࡧࠣࡧࡦࡲ࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡨࡥࡨ࡮ࠠࡵࡧࡶࡸࠬࡹࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢ࡫ࡥࡸࠦࡢࡦࡧࡱࠤࡨࡵ࡮ࡴࡷࡰࡩࡩࠦࡡ࡯ࡦࠣࡷࡪࡴࡴ࠭ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡷࡴࠦࡴࡩࡣࡷࠤࡸࡻࡢࡴࡧࡴࡹࡪࡴࡴࠡࡶࡨࡷࡹࡹࠠࡥࡱࠣࡲࡴࡺࠠࡪࡰ࡫ࡩࡷ࡯ࡴࠡࡶࡤ࡫ࡸࠦࡦࡳࡱࡰࠤࡵࡸࡥࡷ࡫ࡲࡹࡸࠦࡴࡦࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡖࡵࡨࡷࠥࡸࡥࡢࡵࡶ࡭࡬ࡴ࡭ࡦࡰࡷࠤ࠭ࡴ࡯ࡵࠢࡧ࡭ࡨࡺ࠮ࡤ࡮ࡨࡥࡷ࠯ࠠࡵࡱࠣࡥࡻࡵࡩࡥࠢࡰࡹࡹࡧࡴࡪࡰࡪࠤࡦࡴࡹࠡ࡮࡬ࡺࡪࠦࡲࡦࡨࡨࡶࡪࡴࡣࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡪࡲࡤࠡࡤࡼࠤࡦࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡹ࡮ࡡࡵࠢࡺࡥࡸࠦࡳࡦࡶࠣࡺ࡮ࡧࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶࠬ࠮࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᯖ")
        bstack1l1l1lll1l1_opy_._111l11l1l11_opy_ = {}
    @staticmethod
    def bstack111l11ll11l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1l1lll1l1_opy_._111l11l1lll_opy_
    @staticmethod
    def bstack111l11l1ll1_opy_(bstack111l11ll111_opy_: str) -> List[str]:
        bstack11ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡰ࡭࡫ࡷࡷࠥࡺࡨࡦࠢ࡬ࡲࡵࡻࡴࠡࡵࡷࡶ࡮ࡴࡧࠡࡤࡼࠤࡨࡵ࡭࡮ࡣࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡪࡹࡰࡦࡥࡷ࡭ࡳ࡭ࠠࡥࡱࡸࡦࡱ࡫࠭ࡲࡷࡲࡸࡪࡪࠠࡴࡷࡥࡷࡹࡸࡩ࡯ࡩࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡩࡽࡧ࡭ࡱ࡮ࡨ࠾ࠥ࠭ࡡ࠭ࠢࠥࡦ࠱ࡩࠢ࠭ࠢࡧࠫࠥ࠳࠾ࠡ࡝ࠪࡥࠬ࠲ࠠࠨࡤ࠯ࡧࠬ࠲ࠠࠨࡦࠪࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᯗ")
        pattern = re.compile(bstack11ll11_opy_ (u"ࡴࠪࠦ࠭ࡡ࡞ࠣ࡟࠭࠭ࠧࢂࠨ࡜ࡠ࠯ࡡ࠰࠯ࠧᯘ"))
        result = []
        for match in pattern.finditer(bstack111l11ll111_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack11ll11_opy_ (u"࡙ࠥࡹ࡯࡬ࡪࡶࡼࠤࡨࡲࡡࡴࡵࠣࡷ࡭ࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣ࡭ࡳࡹࡴࡢࡰࡷ࡭ࡦࡺࡥࡥࠤᯙ"))