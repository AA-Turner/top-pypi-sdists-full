# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l1l1l1lll1_opy_:
    bstack1l1111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥࡻࡴࡪ࡮࡬ࡸࡾࠦ࡭ࡦࡶ࡫ࡳࡩࡹࠠࡵࡱࠣࡷࡪࡺࠠࡢࡰࡧࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࠣࡱࡪࡺࡡࡥࡣࡷࡥ࠳ࠐࠠࠡࠢࠣࡍࡹࠦ࡭ࡢ࡫ࡱࡸࡦ࡯࡮ࡴࠢࡷࡻࡴࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷ࡯ࡥࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡳࡪࠠࡣࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵ࠱ࠎࠥࠦࠠࠡࡇࡤࡧ࡭ࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡧࡱࡸࡷࡿࠠࡪࡵࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡺ࡯ࠡࡤࡨࠤࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡤࠡࡣࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࡱࡥࡺ࠼ࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡪ࡮࡫࡬ࡥࡡࡷࡽࡵ࡫ࠢ࠻ࠢࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦ࠱ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡻࡧ࡬ࡶࡧࡶࠦ࠿࡛ࠦ࡭࡫ࡶࡸࠥࡵࡦࠡࡶࡤ࡫ࠥࡼࡡ࡭ࡷࡨࡷࡢࠐࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠨࠢࠣᯫ")
    _111l111ll1l_opy_: Dict[str, Dict[str, Any]] = {}
    _111l111l11l_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1111ll11ll_opy_: str, key_value: str, bstack111l111llll_opy_: bool = False) -> None:
        if not bstack1111ll11ll_opy_ or not key_value or bstack1111ll11ll_opy_.strip() == bstack1l1111l_opy_ (u"ࠣࠤᯬ") or key_value.strip() == bstack1l1111l_opy_ (u"ࠤࠥᯭ"):
            logger.error(bstack1l1111l_opy_ (u"ࠥ࡯ࡪࡿ࡟࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢ࡮ࡩࡾࡥࡶࡢ࡮ࡸࡩࠥࡳࡵࡴࡶࠣࡦࡪࠦ࡮ࡰࡰ࠰ࡲࡺࡲ࡬ࠡࡣࡱࡨࠥࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠣᯮ"))
        values: List[str] = bstack1l1l1l1lll1_opy_.bstack111l11l1111_opy_(key_value)
        bstack111l111l1ll_opy_ = {bstack1l1111l_opy_ (u"ࠦ࡫࡯ࡥ࡭ࡦࡢࡸࡾࡶࡥࠣᯯ"): bstack1l1111l_opy_ (u"ࠧࡳࡵ࡭ࡶ࡬ࡣࡩࡸ࡯ࡱࡦࡲࡻࡳࠨᯰ"), bstack1l1111l_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᯱ"): values}
        bstack111l11l111l_opy_ = bstack1l1l1l1lll1_opy_._111l111l11l_opy_ if bstack111l111llll_opy_ else bstack1l1l1l1lll1_opy_._111l111ll1l_opy_
        if bstack1111ll11ll_opy_ in bstack111l11l111l_opy_:
            bstack111l111ll11_opy_ = bstack111l11l111l_opy_[bstack1111ll11ll_opy_]
            bstack111l111lll1_opy_ = bstack111l111ll11_opy_.get(bstack1l1111l_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹ᯲ࠢ"), [])
            for val in values:
                if val not in bstack111l111lll1_opy_:
                    bstack111l111lll1_opy_.append(val)
            bstack111l111ll11_opy_[bstack1l1111l_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳ᯳ࠣ")] = bstack111l111lll1_opy_
        else:
            bstack111l11l111l_opy_[bstack1111ll11ll_opy_] = bstack111l111l1ll_opy_
    @staticmethod
    def bstack111ll1ll11l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1l1l1lll1_opy_._111l111ll1l_opy_
    @staticmethod
    def bstack111lll1ll11_opy_() -> None:
        bstack1l1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃ࡭ࡧࡤࡶࠥࡧ࡬࡭ࠢࡷࡩࡸࡺ࠭࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤࡦࡩࡣࡶ࡯ࡸࡰࡦࡺࡥࡥࠢࡶࡳࠥ࡬ࡡࡳ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡒࡻࡳࡵࠢࡥࡩࠥࡩࡡ࡭࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡪࡧࡣࡩࠢࡷࡩࡸࡺࠧࡴࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡣࡰࡰࡶࡹࡲ࡫ࡤࠡࡣࡱࡨࠥࡹࡥ࡯ࡶ࠯ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡹ࡯ࠡࡶ࡫ࡥࡹࠦࡳࡶࡤࡶࡩࡶࡻࡥ࡯ࡶࠣࡸࡪࡹࡴࡴࠢࡧࡳࠥࡴ࡯ࡵࠢ࡬ࡲ࡭࡫ࡲࡪࡶࠣࡸࡦ࡭ࡳࠡࡨࡵࡳࡲࠦࡰࡳࡧࡹ࡭ࡴࡻࡳࠡࡶࡨࡷࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡘࡷࡪࡹࠠࡳࡧࡤࡷࡸ࡯ࡧ࡯࡯ࡨࡲࡹࠦࠨ࡯ࡱࡷࠤࡩ࡯ࡣࡵ࠰ࡦࡰࡪࡧࡲࠪࠢࡷࡳࠥࡧࡶࡰ࡫ࡧࠤࡲࡻࡴࡢࡶ࡬ࡲ࡬ࠦࡡ࡯ࡻࠣࡰ࡮ࡼࡥࠡࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡮ࡥ࡭ࡦࠣࡦࡾࠦࡡࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡴࡩࡣࡷࠤࡼࡧࡳࠡࡵࡨࡸࠥࡼࡩࡢࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠮ࠩ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᯴")
        bstack1l1l1l1lll1_opy_._111l111ll1l_opy_ = {}
    @staticmethod
    def bstack111l111l111_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1l1l1lll1_opy_._111l111l11l_opy_
    @staticmethod
    def bstack111l11l1111_opy_(bstack111l111l1l1_opy_: str) -> List[str]:
        bstack1l1111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡲ࡯࡭ࡹࡹࠠࡵࡪࡨࠤ࡮ࡴࡰࡶࡶࠣࡷࡹࡸࡩ࡯ࡩࠣࡦࡾࠦࡣࡰ࡯ࡰࡥࡸࠦࡷࡩ࡫࡯ࡩࠥࡸࡥࡴࡲࡨࡧࡹ࡯࡮ࡨࠢࡧࡳࡺࡨ࡬ࡦ࠯ࡴࡹࡴࡺࡥࡥࠢࡶࡹࡧࡹࡴࡳ࡫ࡱ࡫ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥ࡫ࡸࡢ࡯ࡳࡰࡪࡀࠠࠨࡣ࠯ࠤࠧࡨࠬࡤࠤ࠯ࠤࡩ࠭ࠠ࠮ࡀࠣ࡟ࠬࡧࠧ࠭ࠢࠪࡦ࠱ࡩࠧ࠭ࠢࠪࡨࠬࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ᯵")
        pattern = re.compile(bstack1l1111l_opy_ (u"ࡶࠬࠨࠨ࡜ࡠࠥࡡ࠯࠯ࠢࡽࠪ࡞ࡢ࠱ࡣࠫࠪࠩ᯶"))
        result = []
        for match in pattern.finditer(bstack111l111l1l1_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1l1111l_opy_ (u"࡛ࠧࡴࡪ࡮࡬ࡸࡾࠦࡣ࡭ࡣࡶࡷࠥࡹࡨࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥ࡯࡮ࡴࡶࡤࡲࡹ࡯ࡡࡵࡧࡧࠦ᯷"))