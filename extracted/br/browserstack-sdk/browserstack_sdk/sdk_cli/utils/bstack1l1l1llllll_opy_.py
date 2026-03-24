# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l1llll1l1l_opy_:
    bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡳࡶࡴࡼࡩࡥࡧࡶࠤࡺࡺࡩ࡭࡫ࡷࡽࠥࡳࡥࡵࡪࡲࡨࡸࠦࡴࡰࠢࡶࡩࡹࠦࡡ࡯ࡦࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࠢࡰࡩࡹࡧࡤࡢࡶࡤ࠲ࠏࠦࠠࠡࠢࡌࡸࠥࡳࡡࡪࡰࡷࡥ࡮ࡴࡳࠡࡶࡺࡳࠥࡹࡥࡱࡣࡵࡥࡹ࡫ࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶ࡮࡫ࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡤࡲࡩࠦࡢࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴ࠰ࠍࠤࠥࠦࠠࡆࡣࡦ࡬ࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡦࡰࡷࡶࡾࠦࡩࡴࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡹࡵࠠࡣࡧࠣࡷࡹࡸࡵࡤࡶࡸࡶࡪࡪࠠࡢࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࡰ࡫ࡹ࠻ࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡩ࡭ࡪࡲࡤࡠࡶࡼࡴࡪࠨ࠺ࠡࠤࡰࡹࡱࡺࡩࡠࡦࡵࡳࡵࡪ࡯ࡸࡰࠥ࠰ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡺࡦࡲࡵࡦࡵࠥ࠾ࠥࡡ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡵࡣࡪࠤࡻࡧ࡬ࡶࡧࡶࡡࠏࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠧࠨࠢ᧝")
    _11l1111l11l_opy_: Dict[str, Dict[str, Any]] = {}
    _11l1111lll1_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack111ll11ll_opy_: str, key_value: str, bstack11l11111ll1_opy_: bool = False) -> None:
        if not bstack111ll11ll_opy_ or not key_value or bstack111ll11ll_opy_.strip() == bstack1ll1lll_opy_ (u"ࠢࠣ᧞") or key_value.strip() == bstack1ll1lll_opy_ (u"ࠣࠤ᧟"):
            logger.error(bstack1ll1lll_opy_ (u"ࠤ࡮ࡩࡾࡥ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡ࡭ࡨࡽࡤࡼࡡ࡭ࡷࡨࠤࡲࡻࡳࡵࠢࡥࡩࠥࡴ࡯࡯࠯ࡱࡹࡱࡲࠠࡢࡰࡧࠤࡳࡵ࡮࠮ࡧࡰࡴࡹࡿࠢ᧠"))
        values: List[str] = bstack1l1llll1l1l_opy_.bstack11l1111l111_opy_(key_value)
        bstack11l1111llll_opy_ = {bstack1ll1lll_opy_ (u"ࠥࡪ࡮࡫࡬ࡥࡡࡷࡽࡵ࡫ࠢ᧡"): bstack1ll1lll_opy_ (u"ࠦࡲࡻ࡬ࡵ࡫ࡢࡨࡷࡵࡰࡥࡱࡺࡲࠧ᧢"), bstack1ll1lll_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧ᧣"): values}
        bstack11l1111l1l1_opy_ = bstack1l1llll1l1l_opy_._11l1111lll1_opy_ if bstack11l11111ll1_opy_ else bstack1l1llll1l1l_opy_._11l1111l11l_opy_
        if bstack111ll11ll_opy_ in bstack11l1111l1l1_opy_:
            bstack11l1111l1ll_opy_ = bstack11l1111l1l1_opy_[bstack111ll11ll_opy_]
            bstack11l11111lll_opy_ = bstack11l1111l1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨ᧤"), [])
            for val in values:
                if val not in bstack11l11111lll_opy_:
                    bstack11l11111lll_opy_.append(val)
            bstack11l1111l1ll_opy_[bstack1ll1lll_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢ᧥")] = bstack11l11111lll_opy_
        else:
            bstack11l1111l1l1_opy_[bstack111ll11ll_opy_] = bstack11l1111llll_opy_
    @staticmethod
    def bstack11l11llll1l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1llll1l1l_opy_._11l1111l11l_opy_
    @staticmethod
    def bstack11l1111ll1l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1llll1l1l_opy_._11l1111lll1_opy_
    @staticmethod
    def bstack11l1111l111_opy_(bstack11l1111ll11_opy_: str) -> List[str]:
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡰ࡭࡫ࡷࡷࠥࡺࡨࡦࠢ࡬ࡲࡵࡻࡴࠡࡵࡷࡶ࡮ࡴࡧࠡࡤࡼࠤࡨࡵ࡭࡮ࡣࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡪࡹࡰࡦࡥࡷ࡭ࡳ࡭ࠠࡥࡱࡸࡦࡱ࡫࠭ࡲࡷࡲࡸࡪࡪࠠࡴࡷࡥࡷࡹࡸࡩ࡯ࡩࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡩࡽࡧ࡭ࡱ࡮ࡨ࠾ࠥ࠭ࡡ࠭ࠢࠥࡦ࠱ࡩࠢ࠭ࠢࡧࠫࠥ࠳࠾ࠡ࡝ࠪࡥࠬ࠲ࠠࠨࡤ࠯ࡧࠬ࠲ࠠࠨࡦࠪࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᧦")
        pattern = re.compile(bstack1ll1lll_opy_ (u"ࡴࠪࠦ࠭ࡡ࡞ࠣ࡟࠭࠭ࠧࢂࠨ࡜ࡠ࠯ࡡ࠰࠯ࠧ᧧"))
        result = []
        for match in pattern.finditer(bstack11l1111ll11_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1ll1lll_opy_ (u"࡙ࠥࡹ࡯࡬ࡪࡶࡼࠤࡨࡲࡡࡴࡵࠣࡷ࡭ࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣ࡭ࡳࡹࡴࡢࡰࡷ࡭ࡦࡺࡥࡥࠤ᧨"))