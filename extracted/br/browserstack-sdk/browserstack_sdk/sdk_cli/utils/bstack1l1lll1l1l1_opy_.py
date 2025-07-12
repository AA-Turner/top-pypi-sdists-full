# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.bstack1l11l1l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l1lll1l1ll_opy_:
    bstack11l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡳࠡࡷࡷ࡭ࡱ࡯ࡴࡺࠢࡰࡩࡹ࡮࡯ࡥࡵࠣࡸࡴࠦࡳࡦࡶࠣࡥࡳࡪࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࠦ࡭ࡦࡶࡤࡨࡦࡺࡡ࠯ࠌࠣࠤࠥࠦࡉࡵࠢࡰࡥ࡮ࡴࡴࡢ࡫ࡱࡷࠥࡺࡷࡰࠢࡶࡩࡵࡧࡲࡢࡶࡨࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳ࡫ࡨࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡡ࡯ࡦࠣࡦࡺ࡯࡬ࡥࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸ࠴ࠊࠡࠢࠣࠤࡊࡧࡣࡩࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡪࡴࡴࡳࡻࠣ࡭ࡸࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡶࡲࠤࡧ࡫ࠠࡴࡶࡵࡹࡨࡺࡵࡳࡧࡧࠤࡦࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡ࡭ࡨࡽ࠿ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡦࡪࡧ࡯ࡨࡤࡺࡹࡱࡧࠥ࠾ࠥࠨ࡭ࡶ࡮ࡷ࡭ࡤࡪࡲࡰࡲࡧࡳࡼࡴࠢ࠭ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡷࡣ࡯ࡹࡪࡹࠢ࠻ࠢ࡞ࡰ࡮ࡹࡴࠡࡱࡩࠤࡹࡧࡧࠡࡸࡤࡰࡺ࡫ࡳ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠤࠥࠦᗕ")
    _11lll1llll1_opy_: Dict[str, Dict[str, Any]] = {}
    _11lll1lllll_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1l1l11ll_opy_: str, key_value: str, bstack11llll11l11_opy_: bool = False) -> None:
        if not bstack1l1l11ll_opy_ or not key_value or bstack1l1l11ll_opy_.strip() == bstack11l1111_opy_ (u"ࠦࠧᗖ") or key_value.strip() == bstack11l1111_opy_ (u"ࠧࠨᗗ"):
            logger.error(bstack11l1111_opy_ (u"ࠨ࡫ࡦࡻࡢࡲࡦࡳࡥࠡࡣࡱࡨࠥࡱࡥࡺࡡࡹࡥࡱࡻࡥࠡ࡯ࡸࡷࡹࠦࡢࡦࠢࡱࡳࡳ࠳࡮ࡶ࡮࡯ࠤࡦࡴࡤࠡࡰࡲࡲ࠲࡫࡭ࡱࡶࡼࠦᗘ"))
        values: List[str] = bstack1l1lll1l1ll_opy_.bstack11lll1lll11_opy_(key_value)
        bstack11llll1111l_opy_ = {bstack11l1111_opy_ (u"ࠢࡧ࡫ࡨࡰࡩࡥࡴࡺࡲࡨࠦᗙ"): bstack11l1111_opy_ (u"ࠣ࡯ࡸࡰࡹ࡯࡟ࡥࡴࡲࡴࡩࡵࡷ࡯ࠤᗚ"), bstack11l1111_opy_ (u"ࠤࡹࡥࡱࡻࡥࡴࠤᗛ"): values}
        bstack11llll11l1l_opy_ = bstack1l1lll1l1ll_opy_._11lll1lllll_opy_ if bstack11llll11l11_opy_ else bstack1l1lll1l1ll_opy_._11lll1llll1_opy_
        if bstack1l1l11ll_opy_ in bstack11llll11l1l_opy_:
            bstack11llll111l1_opy_ = bstack11llll11l1l_opy_[bstack1l1l11ll_opy_]
            bstack11llll11111_opy_ = bstack11llll111l1_opy_.get(bstack11l1111_opy_ (u"ࠥࡺࡦࡲࡵࡦࡵࠥᗜ"), [])
            for val in values:
                if val not in bstack11llll11111_opy_:
                    bstack11llll11111_opy_.append(val)
            bstack11llll111l1_opy_[bstack11l1111_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦᗝ")] = bstack11llll11111_opy_
        else:
            bstack11llll11l1l_opy_[bstack1l1l11ll_opy_] = bstack11llll1111l_opy_
    @staticmethod
    def bstack1l1ll1l1lll_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1lll1l1ll_opy_._11lll1llll1_opy_
    @staticmethod
    def bstack11lll1lll1l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1lll1l1ll_opy_._11lll1lllll_opy_
    @staticmethod
    def bstack11lll1lll11_opy_(bstack11llll111ll_opy_: str) -> List[str]:
        bstack11l1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡴࡱ࡯ࡴࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡲࡸࡸࠥࡹࡴࡳ࡫ࡱ࡫ࠥࡨࡹࠡࡥࡲࡱࡲࡧࡳࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡧࡶࡴࡪࡩࡴࡪࡰࡪࠤࡩࡵࡵࡣ࡮ࡨ࠱ࡶࡻ࡯ࡵࡧࡧࠤࡸࡻࡢࡴࡶࡵ࡭ࡳ࡭ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡦࡺࡤࡱࡵࡲࡥ࠻ࠢࠪࡥ࠱ࠦࠢࡣ࠮ࡦࠦ࠱ࠦࡤࠨࠢ࠰ࡂࠥࡡࠧࡢࠩ࠯ࠤࠬࡨࠬࡤࠩ࠯ࠤࠬࡪࠧ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᗞ")
        pattern = re.compile(bstack11l1111_opy_ (u"ࡸࠧࠣࠪ࡞ࡢࠧࡣࠪࠪࠤࡿࠬࡠࡤࠬ࡞࠭ࠬࠫᗟ"))
        result = []
        for match in pattern.finditer(bstack11llll111ll_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack11l1111_opy_ (u"ࠢࡖࡶ࡬ࡰ࡮ࡺࡹࠡࡥ࡯ࡥࡸࡹࠠࡴࡪࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡪࡰࡶࡸࡦࡴࡴࡪࡣࡷࡩࡩࠨᗠ"))