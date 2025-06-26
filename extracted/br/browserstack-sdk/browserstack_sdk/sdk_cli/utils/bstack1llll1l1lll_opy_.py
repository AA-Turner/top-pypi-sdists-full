# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.bstack11l1l1l111_opy_ import get_logger
logger = get_logger(__name__)
class bstack1llll1l11l1_opy_:
    bstack11ll1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡶࡲࡰࡸ࡬ࡨࡪࡹࠠࡶࡶ࡬ࡰ࡮ࡺࡹࠡ࡯ࡨࡸ࡭ࡵࡤࡴࠢࡷࡳࠥࡹࡥࡵࠢࡤࡲࡩࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࠥࡳࡥࡵࡣࡧࡥࡹࡧ࠮ࠋࠢࠣࠤࠥࡏࡴࠡ࡯ࡤ࡭ࡳࡺࡡࡪࡰࡶࠤࡹࡽ࡯ࠡࡵࡨࡴࡦࡸࡡࡵࡧࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡪࡧࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡧ࡮ࡥࠢࡥࡹ࡮ࡲࡤࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷ࠳ࠐࠠࠡࠢࠣࡉࡦࡩࡨࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡩࡳࡺࡲࡺࠢ࡬ࡷࠥ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡵࡱࠣࡦࡪࠦࡳࡵࡴࡸࡧࡹࡻࡲࡦࡦࠣࡥࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠ࡬ࡧࡼ࠾ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧ࡬ࡩࡦ࡮ࡧࡣࡹࡿࡰࡦࠤ࠽ࠤࠧࡳࡵ࡭ࡶ࡬ࡣࡩࡸ࡯ࡱࡦࡲࡻࡳࠨࠬࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡶࡢ࡮ࡸࡩࡸࠨ࠺ࠡ࡝࡯࡭ࡸࡺࠠࡰࡨࠣࡸࡦ࡭ࠠࡷࡣ࡯ࡹࡪࡹ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࡿࠍࠤࠥࠦࠠࠣࠤࠥᖜ")
    _11llll111ll_opy_: Dict[str, Dict[str, Any]] = {}
    _11llll11ll1_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack11l111ll1l_opy_: str, key_value: str, bstack11llll1l111_opy_: bool = False) -> None:
        if not bstack11l111ll1l_opy_ or not key_value or bstack11l111ll1l_opy_.strip() == bstack11ll1l1_opy_ (u"ࠥࠦᖝ") or key_value.strip() == bstack11ll1l1_opy_ (u"ࠦࠧᖞ"):
            logger.error(bstack11ll1l1_opy_ (u"ࠧࡱࡥࡺࡡࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡰ࡫ࡹࡠࡸࡤࡰࡺ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡰࡲࡲ࠲ࡴࡵ࡭࡮ࠣࡥࡳࡪࠠ࡯ࡱࡱ࠱ࡪࡳࡰࡵࡻࠥᖟ"))
        values: List[str] = bstack1llll1l11l1_opy_.bstack11llll11l11_opy_(key_value)
        bstack11llll1l11l_opy_ = {bstack11ll1l1_opy_ (u"ࠨࡦࡪࡧ࡯ࡨࡤࡺࡹࡱࡧࠥᖠ"): bstack11ll1l1_opy_ (u"ࠢ࡮ࡷ࡯ࡸ࡮ࡥࡤࡳࡱࡳࡨࡴࡽ࡮ࠣᖡ"), bstack11ll1l1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࡳࠣᖢ"): values}
        bstack11llll1111l_opy_ = bstack1llll1l11l1_opy_._11llll11ll1_opy_ if bstack11llll1l111_opy_ else bstack1llll1l11l1_opy_._11llll111ll_opy_
        if bstack11l111ll1l_opy_ in bstack11llll1111l_opy_:
            bstack11llll11l1l_opy_ = bstack11llll1111l_opy_[bstack11l111ll1l_opy_]
            bstack11llll11111_opy_ = bstack11llll11l1l_opy_.get(bstack11ll1l1_opy_ (u"ࠤࡹࡥࡱࡻࡥࡴࠤᖣ"), [])
            for val in values:
                if val not in bstack11llll11111_opy_:
                    bstack11llll11111_opy_.append(val)
            bstack11llll11l1l_opy_[bstack11ll1l1_opy_ (u"ࠥࡺࡦࡲࡵࡦࡵࠥᖤ")] = bstack11llll11111_opy_
        else:
            bstack11llll1111l_opy_[bstack11l111ll1l_opy_] = bstack11llll1l11l_opy_
    @staticmethod
    def bstack1l11l111l11_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1llll1l11l1_opy_._11llll111ll_opy_
    @staticmethod
    def bstack11llll111l1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1llll1l11l1_opy_._11llll11ll1_opy_
    @staticmethod
    def bstack11llll11l11_opy_(bstack11llll11lll_opy_: str) -> List[str]:
        bstack11ll1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡳࡰ࡮ࡺࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡱࡷࡷࠤࡸࡺࡲࡪࡰࡪࠤࡧࡿࠠࡤࡱࡰࡱࡦࡹࠠࡸࡪ࡬ࡰࡪࠦࡲࡦࡵࡳࡩࡨࡺࡩ࡯ࡩࠣࡨࡴࡻࡢ࡭ࡧ࠰ࡵࡺࡵࡴࡦࡦࠣࡷࡺࡨࡳࡵࡴ࡬ࡲ࡬ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡥࡹࡣࡰࡴࡱ࡫࠺ࠡࠩࡤ࠰ࠥࠨࡢ࠭ࡥࠥ࠰ࠥࡪࠧࠡ࠯ࡁࠤࡠ࠭ࡡࠨ࠮ࠣࠫࡧ࠲ࡣࠨ࠮ࠣࠫࡩ࠭࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᖥ")
        pattern = re.compile(bstack11ll1l1_opy_ (u"ࡷ࠭ࠢࠩ࡝ࡡࠦࡢ࠰ࠩࠣࡾࠫ࡟ࡣ࠲࡝ࠬࠫࠪᖦ"))
        result = []
        for match in pattern.finditer(bstack11llll11lll_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack11ll1l1_opy_ (u"ࠨࡕࡵ࡫࡯࡭ࡹࡿࠠࡤ࡮ࡤࡷࡸࠦࡳࡩࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡩ࡯ࡵࡷࡥࡳࡺࡩࡢࡶࡨࡨࠧᖧ"))