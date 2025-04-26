# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.bstack11111llll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1llll11llll_opy_:
    bstack1l11lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡱࡴࡲࡺ࡮ࡪࡥࡴࠢࡸࡸ࡮ࡲࡩࡵࡻࠣࡱࡪࡺࡨࡰࡦࡶࠤࡹࡵࠠࡴࡧࡷࠤࡦࡴࡤࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࠠ࡮ࡧࡷࡥࡩࡧࡴࡢ࠰ࠍࠤࠥࠦࠠࡊࡶࠣࡱࡦ࡯࡮ࡵࡣ࡬ࡲࡸࠦࡴࡸࡱࠣࡷࡪࡶࡡࡳࡣࡷࡩࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴ࡬ࡩࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡢࡰࡧࠤࡧࡻࡩ࡭ࡦࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹ࠮ࠋࠢࠣࠤࠥࡋࡡࡤࡪࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡫࡮ࡵࡴࡼࠤ࡮ࡹࠠࡦࡺࡳࡩࡨࡺࡥࡥࠢࡷࡳࠥࡨࡥࠡࡵࡷࡶࡺࡩࡴࡶࡴࡨࡨࠥࡧࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢ࡮ࡩࡾࡀࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡧ࡫ࡨࡰࡩࡥࡴࡺࡲࡨࠦ࠿ࠦࠢ࡮ࡷ࡯ࡸ࡮ࡥࡤࡳࡱࡳࡨࡴࡽ࡮ࠣ࠮ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡸࡤࡰࡺ࡫ࡳࠣ࠼ࠣ࡟ࡱ࡯ࡳࡵࠢࡲࡪࠥࡺࡡࡨࠢࡹࡥࡱࡻࡥࡴ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠥࠦࠧᔠ")
    _1l1111l1l11_opy_: Dict[str, Dict[str, Any]] = {}
    _1l1111l11ll_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1l1ll111l_opy_: str, key_value: str, bstack1l1111l111l_opy_: bool = False) -> None:
        if not bstack1l1ll111l_opy_ or not key_value or bstack1l1ll111l_opy_.strip() == bstack1l11lll_opy_ (u"ࠧࠨᔡ") or key_value.strip() == bstack1l11lll_opy_ (u"ࠨࠢᔢ"):
            logger.error(bstack1l11lll_opy_ (u"ࠢ࡬ࡧࡼࡣࡳࡧ࡭ࡦࠢࡤࡲࡩࠦ࡫ࡦࡻࡢࡺࡦࡲࡵࡦࠢࡰࡹࡸࡺࠠࡣࡧࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡧ࡮ࡥࠢࡱࡳࡳ࠳ࡥ࡮ࡲࡷࡽࠧᔣ"))
        values: List[str] = bstack1llll11llll_opy_.bstack1l1111l1l1l_opy_(key_value)
        bstack1l1111l1111_opy_ = {bstack1l11lll_opy_ (u"ࠣࡨ࡬ࡩࡱࡪ࡟ࡵࡻࡳࡩࠧᔤ"): bstack1l11lll_opy_ (u"ࠤࡰࡹࡱࡺࡩࡠࡦࡵࡳࡵࡪ࡯ࡸࡰࠥᔥ"), bstack1l11lll_opy_ (u"ࠥࡺࡦࡲࡵࡦࡵࠥᔦ"): values}
        bstack1l11111ll1l_opy_ = bstack1llll11llll_opy_._1l1111l11ll_opy_ if bstack1l1111l111l_opy_ else bstack1llll11llll_opy_._1l1111l1l11_opy_
        if bstack1l1ll111l_opy_ in bstack1l11111ll1l_opy_:
            bstack1l11111llll_opy_ = bstack1l11111ll1l_opy_[bstack1l1ll111l_opy_]
            bstack1l11111lll1_opy_ = bstack1l11111llll_opy_.get(bstack1l11lll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦᔧ"), [])
            for val in values:
                if val not in bstack1l11111lll1_opy_:
                    bstack1l11111lll1_opy_.append(val)
            bstack1l11111llll_opy_[bstack1l11lll_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧᔨ")] = bstack1l11111lll1_opy_
        else:
            bstack1l11111ll1l_opy_[bstack1l1ll111l_opy_] = bstack1l1111l1111_opy_
    @staticmethod
    def bstack1l11l1ll11l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1llll11llll_opy_._1l1111l1l11_opy_
    @staticmethod
    def bstack1l11111ll11_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1llll11llll_opy_._1l1111l11ll_opy_
    @staticmethod
    def bstack1l1111l1l1l_opy_(bstack1l1111l11l1_opy_: str) -> List[str]:
        bstack1l11lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡵࡲࡩࡵࡵࠣࡸ࡭࡫ࠠࡪࡰࡳࡹࡹࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡢࡺࠢࡦࡳࡲࡳࡡࡴࠢࡺ࡬࡮ࡲࡥࠡࡴࡨࡷࡵ࡫ࡣࡵ࡫ࡱ࡫ࠥࡪ࡯ࡶࡤ࡯ࡩ࠲ࡷࡵࡰࡶࡨࡨࠥࡹࡵࡣࡵࡷࡶ࡮ࡴࡧࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡧࡻࡥࡲࡶ࡬ࡦ࠼ࠣࠫࡦ࠲ࠠࠣࡤ࠯ࡧࠧ࠲ࠠࡥࠩࠣ࠱ࡃ࡛ࠦࠨࡣࠪ࠰ࠥ࠭ࡢ࠭ࡥࠪ࠰ࠥ࠭ࡤࠨ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᔩ")
        pattern = re.compile(bstack1l11lll_opy_ (u"ࡲࠨࠤࠫ࡟ࡣࠨ࡝ࠫࠫࠥࢀ࠭ࡡ࡞࠭࡟࠮࠭ࠬᔪ"))
        result = []
        for match in pattern.finditer(bstack1l1111l11l1_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1l11lll_opy_ (u"ࠣࡗࡷ࡭ࡱ࡯ࡴࡺࠢࡦࡰࡦࡹࡳࠡࡵ࡫ࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡵ࡫ࡤࡸࡪࡪࠢᔫ"))