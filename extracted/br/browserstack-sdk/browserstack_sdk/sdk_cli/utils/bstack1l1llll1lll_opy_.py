# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l1ll1l1lll_opy_:
    bstack1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡶࡲࡰࡸ࡬ࡨࡪࡹࠠࡶࡶ࡬ࡰ࡮ࡺࡹࠡ࡯ࡨࡸ࡭ࡵࡤࡴࠢࡷࡳࠥࡹࡥࡵࠢࡤࡲࡩࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࠥࡳࡥࡵࡣࡧࡥࡹࡧ࠮ࠋࠢࠣࠤࠥࡏࡴࠡ࡯ࡤ࡭ࡳࡺࡡࡪࡰࡶࠤࡹࡽ࡯ࠡࡵࡨࡴࡦࡸࡡࡵࡧࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡪࡧࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡧ࡮ࡥࠢࡥࡹ࡮ࡲࡤࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷ࠳ࠐࠠࠡࠢࠣࡉࡦࡩࡨࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡩࡳࡺࡲࡺࠢ࡬ࡷࠥ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡵࡱࠣࡦࡪࠦࡳࡵࡴࡸࡧࡹࡻࡲࡦࡦࠣࡥࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠ࡬ࡧࡼ࠾ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧ࡬ࡩࡦ࡮ࡧࡣࡹࡿࡰࡦࠤ࠽ࠤࠧࡳࡵ࡭ࡶ࡬ࡣࡩࡸ࡯ࡱࡦࡲࡻࡳࠨࠬࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡶࡢ࡮ࡸࡩࡸࠨ࠺ࠡ࡝࡯࡭ࡸࡺࠠࡰࡨࠣࡸࡦ࡭ࠠࡷࡣ࡯ࡹࡪࡹ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࡿࠍࠤࠥࠦࠠࠣࠤࠥᣲ")
    _11l11lll1ll_opy_: Dict[str, Dict[str, Any]] = {}
    _11l11ll1lll_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack111lllllll_opy_: str, key_value: str, bstack11l11llll1l_opy_: bool = False) -> None:
        if not bstack111lllllll_opy_ or not key_value or bstack111lllllll_opy_.strip() == bstack1111_opy_ (u"ࠥࠦᣳ") or key_value.strip() == bstack1111_opy_ (u"ࠦࠧᣴ"):
            logger.error(bstack1111_opy_ (u"ࠧࡱࡥࡺࡡࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡰ࡫ࡹࡠࡸࡤࡰࡺ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡰࡲࡲ࠲ࡴࡵ࡭࡮ࠣࡥࡳࡪࠠ࡯ࡱࡱ࠱ࡪࡳࡰࡵࡻࠥᣵ"))
        values: List[str] = bstack1l1ll1l1lll_opy_.bstack11l11ll1ll1_opy_(key_value)
        bstack11l11llll11_opy_ = {bstack1111_opy_ (u"ࠨࡦࡪࡧ࡯ࡨࡤࡺࡹࡱࡧࠥ᣶"): bstack1111_opy_ (u"ࠢ࡮ࡷ࡯ࡸ࡮ࡥࡤࡳࡱࡳࡨࡴࡽ࡮ࠣ᣷"), bstack1111_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳࠣ᣸"): values}
        bstack11l11lll111_opy_ = bstack1l1ll1l1lll_opy_._11l11ll1lll_opy_ if bstack11l11llll1l_opy_ else bstack1l1ll1l1lll_opy_._11l11lll1ll_opy_
        if bstack111lllllll_opy_ in bstack11l11lll111_opy_:
            bstack11l11lll11l_opy_ = bstack11l11lll111_opy_[bstack111lllllll_opy_]
            bstack11l11llllll_opy_ = bstack11l11lll11l_opy_.get(bstack1111_opy_ (u"ࠤࡹࡥࡱࡻࡥࡴࠤ᣹"), [])
            for val in values:
                if val not in bstack11l11llllll_opy_:
                    bstack11l11llllll_opy_.append(val)
            bstack11l11lll11l_opy_[bstack1111_opy_ (u"ࠥࡺࡦࡲࡵࡦࡵࠥ᣺")] = bstack11l11llllll_opy_
        else:
            bstack11l11lll111_opy_[bstack111lllllll_opy_] = bstack11l11llll11_opy_
    @staticmethod
    def bstack11l1ll1l1l1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1ll1l1lll_opy_._11l11lll1ll_opy_
    @staticmethod
    def bstack11l11lll1l1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1ll1l1lll_opy_._11l11ll1lll_opy_
    @staticmethod
    def bstack11l11ll1ll1_opy_(bstack11l11lllll1_opy_: str) -> List[str]:
        bstack1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡳࡰ࡮ࡺࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡱࡷࡷࠤࡸࡺࡲࡪࡰࡪࠤࡧࡿࠠࡤࡱࡰࡱࡦࡹࠠࡸࡪ࡬ࡰࡪࠦࡲࡦࡵࡳࡩࡨࡺࡩ࡯ࡩࠣࡨࡴࡻࡢ࡭ࡧ࠰ࡵࡺࡵࡴࡦࡦࠣࡷࡺࡨࡳࡵࡴ࡬ࡲ࡬ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡥࡹࡣࡰࡴࡱ࡫࠺ࠡࠩࡤ࠰ࠥࠨࡢ࠭ࡥࠥ࠰ࠥࡪࠧࠡ࠯ࡁࠤࡠ࠭ࡡࠨ࠮ࠣࠫࡧ࠲ࡣࠨ࠮ࠣࠫࡩ࠭࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ᣻")
        pattern = re.compile(bstack1111_opy_ (u"ࡷ࠭ࠢࠩ࡝ࡡࠦࡢ࠰ࠩࠣࡾࠫ࡟ࡣ࠲࡝ࠬࠫࠪ᣼"))
        result = []
        for match in pattern.finditer(bstack11l11lllll1_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1111_opy_ (u"ࠨࡕࡵ࡫࡯࡭ࡹࡿࠠࡤ࡮ࡤࡷࡸࠦࡳࡩࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡩ࡯ࡵࡷࡥࡳࡺࡩࡢࡶࡨࡨࠧ᣽"))