# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l1l111111l_opy_:
    bstack111ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡲࡵࡳࡻ࡯ࡤࡦࡵࠣࡹࡹ࡯࡬ࡪࡶࡼࠤࡲ࡫ࡴࡩࡱࡧࡷࠥࡺ࡯ࠡࡵࡨࡸࠥࡧ࡮ࡥࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࠡ࡯ࡨࡸࡦࡪࡡࡵࡣ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡲࡧࡩ࡯ࡶࡤ࡭ࡳࡹࠠࡵࡹࡲࠤࡸ࡫ࡰࡢࡴࡤࡸࡪࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵ࡭ࡪࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡱࡨࠥࡨࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࡅࡢࡥ࡫ࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡥ࡯ࡶࡵࡽࠥ࡯ࡳࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࡸࡴࠦࡢࡦࠢࡶࡸࡷࡻࡣࡵࡷࡵࡩࡩࠦࡡࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣ࡯ࡪࡿ࠺ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡨ࡬ࡩࡱࡪ࡟ࡵࡻࡳࡩࠧࡀࠠࠣ࡯ࡸࡰࡹ࡯࡟ࡥࡴࡲࡴࡩࡵࡷ࡯ࠤ࠯ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡹࡥࡱࡻࡥࡴࠤ࠽ࠤࡠࡲࡩࡴࡶࠣࡳ࡫ࠦࡴࡢࡩࠣࡺࡦࡲࡵࡦࡵࡠࠎࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨᯩ")
    _111l11l1111_opy_: Dict[str, Dict[str, Any]] = {}
    _111l11l111l_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1111l1l11_opy_: str, key_value: str, bstack111l111llll_opy_: bool = False) -> None:
        if not bstack1111l1l11_opy_ or not key_value or bstack1111l1l11_opy_.strip() == bstack111ll11_opy_ (u"ࠨࠢᯪ") or key_value.strip() == bstack111ll11_opy_ (u"ࠢࠣᯫ"):
            logger.error(bstack111ll11_opy_ (u"ࠣ࡭ࡨࡽࡤࡴࡡ࡮ࡧࠣࡥࡳࡪࠠ࡬ࡧࡼࡣࡻࡧ࡬ࡶࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡡ࡯ࡦࠣࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠨᯬ"))
        values: List[str] = bstack1l1l111111l_opy_.bstack111l11l11ll_opy_(key_value)
        bstack111l11l11l1_opy_ = {bstack111ll11_opy_ (u"ࠤࡩ࡭ࡪࡲࡤࡠࡶࡼࡴࡪࠨᯭ"): bstack111ll11_opy_ (u"ࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦᯮ"), bstack111ll11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦᯯ"): values}
        bstack111l111l1ll_opy_ = bstack1l1l111111l_opy_._111l11l111l_opy_ if bstack111l111llll_opy_ else bstack1l1l111111l_opy_._111l11l1111_opy_
        if bstack1111l1l11_opy_ in bstack111l111l1ll_opy_:
            bstack111l111ll1l_opy_ = bstack111l111l1ll_opy_[bstack1111l1l11_opy_]
            bstack111l111l1l1_opy_ = bstack111l111ll1l_opy_.get(bstack111ll11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧᯰ"), [])
            for val in values:
                if val not in bstack111l111l1l1_opy_:
                    bstack111l111l1l1_opy_.append(val)
            bstack111l111ll1l_opy_[bstack111ll11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᯱ")] = bstack111l111l1l1_opy_
        else:
            bstack111l111l1ll_opy_[bstack1111l1l11_opy_] = bstack111l11l11l1_opy_
    @staticmethod
    def bstack111ll1ll1ll_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1l111111l_opy_._111l11l1111_opy_
    @staticmethod
    def bstack111lll11lll_opy_() -> None:
        bstack111ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡲࡥࡢࡴࠣࡥࡱࡲࠠࡵࡧࡶࡸ࠲ࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡤࡧࡨࡻ࡭ࡶ࡮ࡤࡸࡪࡪࠠࡴࡱࠣࡪࡦࡸ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡐࡹࡸࡺࠠࡣࡧࠣࡧࡦࡲ࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡨࡥࡨ࡮ࠠࡵࡧࡶࡸࠬࡹࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢ࡫ࡥࡸࠦࡢࡦࡧࡱࠤࡨࡵ࡮ࡴࡷࡰࡩࡩࠦࡡ࡯ࡦࠣࡷࡪࡴࡴ࠭ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡷࡴࠦࡴࡩࡣࡷࠤࡸࡻࡢࡴࡧࡴࡹࡪࡴࡴࠡࡶࡨࡷࡹࡹࠠࡥࡱࠣࡲࡴࡺࠠࡪࡰ࡫ࡩࡷ࡯ࡴࠡࡶࡤ࡫ࡸࠦࡦࡳࡱࡰࠤࡵࡸࡥࡷ࡫ࡲࡹࡸࠦࡴࡦࡵࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡖࡵࡨࡷࠥࡸࡥࡢࡵࡶ࡭࡬ࡴ࡭ࡦࡰࡷࠤ࠭ࡴ࡯ࡵࠢࡧ࡭ࡨࡺ࠮ࡤ࡮ࡨࡥࡷ࠯ࠠࡵࡱࠣࡥࡻࡵࡩࡥࠢࡰࡹࡹࡧࡴࡪࡰࡪࠤࡦࡴࡹࠡ࡮࡬ࡺࡪࠦࡲࡦࡨࡨࡶࡪࡴࡣࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡪࡲࡤࠡࡤࡼࠤࡦࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡹ࡮ࡡࡵࠢࡺࡥࡸࠦࡳࡦࡶࠣࡺ࡮ࡧࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶࠬ࠮࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤ᯲ࠥࠦ")
        bstack1l1l111111l_opy_._111l11l1111_opy_ = {}
    @staticmethod
    def bstack111l111lll1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1l1l111111l_opy_._111l11l111l_opy_
    @staticmethod
    def bstack111l11l11ll_opy_(bstack111l111ll11_opy_: str) -> List[str]:
        bstack111ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡰ࡭࡫ࡷࡷࠥࡺࡨࡦࠢ࡬ࡲࡵࡻࡴࠡࡵࡷࡶ࡮ࡴࡧࠡࡤࡼࠤࡨࡵ࡭࡮ࡣࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡪࡹࡰࡦࡥࡷ࡭ࡳ࡭ࠠࡥࡱࡸࡦࡱ࡫࠭ࡲࡷࡲࡸࡪࡪࠠࡴࡷࡥࡷࡹࡸࡩ࡯ࡩࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡩࡽࡧ࡭ࡱ࡮ࡨ࠾ࠥ࠭ࡡ࠭ࠢࠥࡦ࠱ࡩࠢ࠭ࠢࡧࠫࠥ࠳࠾ࠡ࡝ࠪࡥࠬ࠲ࠠࠨࡤ࠯ࡧࠬ࠲ࠠࠨࡦࠪࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᯳")
        pattern = re.compile(bstack111ll11_opy_ (u"ࡴࠪࠦ࠭ࡡ࡞ࠣ࡟࠭࠭ࠧࢂࠨ࡜ࡠ࠯ࡡ࠰࠯ࠧ᯴"))
        result = []
        for match in pattern.finditer(bstack111l111ll11_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack111ll11_opy_ (u"࡙ࠥࡹ࡯࡬ࡪࡶࡼࠤࡨࡲࡡࡴࡵࠣࡷ࡭ࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣ࡭ࡳࡹࡴࡢࡰࡷ࡭ࡦࡺࡥࡥࠤ᯵"))