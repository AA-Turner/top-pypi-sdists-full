# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import re
from typing import List, Dict, Any
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class CustomTagManager:
    bstack1l1llll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡳࠡࡷࡷ࡭ࡱ࡯ࡴࡺࠢࡰࡩࡹ࡮࡯ࡥࡵࠣࡸࡴࠦࡳࡦࡶࠣࡥࡳࡪࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࠦ࡭ࡦࡶࡤࡨࡦࡺࡡ࠯ࠌࠣࠤࠥࠦࡉࡵࠢࡰࡥ࡮ࡴࡴࡢ࡫ࡱࡷࠥࡺࡷࡰࠢࡶࡩࡵࡧࡲࡢࡶࡨࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳ࡫ࡨࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡡ࡯ࡦࠣࡦࡺ࡯࡬ࡥࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸ࠴ࠊࠡࠢࠣࠤࡊࡧࡣࡩࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡪࡴࡴࡳࡻࠣ࡭ࡸࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡶࡲࠤࡧ࡫ࠠࡴࡶࡵࡹࡨࡺࡵࡳࡧࡧࠤࡦࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡ࡭ࡨࡽ࠿ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡦࡪࡧ࡯ࡨࡤࡺࡹࡱࡧࠥ࠾ࠥࠨ࡭ࡶ࡮ࡷ࡭ࡤࡪࡲࡰࡲࡧࡳࡼࡴࠢ࠭ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡷࡣ࡯ࡹࡪࡹࠢ࠻ࠢ࡞ࡰ࡮ࡹࡴࠡࡱࡩࠤࡹࡧࡧࠡࡸࡤࡰࡺ࡫ࡳ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠤࠥࠦả")
    _1111lll1111_opy_: Dict[str, Dict[str, Any]] = {}
    _1111ll1ll1l_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1lll1llllll_opy_: str, key_value: str, bstack1111lll11ll_opy_: bool = False) -> None:
        if not bstack1lll1llllll_opy_ or not key_value or bstack1lll1llllll_opy_.strip() == bstack1l1llll_opy_ (u"ࠦࠧẤ") or key_value.strip() == bstack1l1llll_opy_ (u"ࠧࠨấ"):
            logger.error(bstack1l1llll_opy_ (u"ࠨ࡫ࡦࡻࡢࡲࡦࡳࡥࠡࡣࡱࡨࠥࡱࡥࡺࡡࡹࡥࡱࡻࡥࠡ࡯ࡸࡷࡹࠦࡢࡦࠢࡱࡳࡳ࠳࡮ࡶ࡮࡯ࠤࡦࡴࡤࠡࡰࡲࡲ࠲࡫࡭ࡱࡶࡼࠦẦ"))
            return
        values: List[str] = CustomTagManager.bstack1111lll111l_opy_(key_value)
        if not values:
            return
        bstack1111ll1llll_opy_ = {bstack1l1llll_opy_ (u"ࠢࡧ࡫ࡨࡰࡩࡥࡴࡺࡲࡨࠦầ"): bstack1l1llll_opy_ (u"ࠣ࡯ࡸࡰࡹ࡯࡟ࡥࡴࡲࡴࡩࡵࡷ࡯ࠤẨ"), bstack1l1llll_opy_ (u"ࠤࡹࡥࡱࡻࡥࡴࠤẩ"): values}
        bstack1111lll1l11_opy_ = CustomTagManager._1111ll1ll1l_opy_ if bstack1111lll11ll_opy_ else CustomTagManager._1111lll1111_opy_
        if bstack1lll1llllll_opy_ in bstack1111lll1l11_opy_:
            bstack1111lll11l1_opy_ = bstack1111lll1l11_opy_[bstack1lll1llllll_opy_]
            bstack1111lll1l1l_opy_ = bstack1111lll11l1_opy_.get(bstack1l1llll_opy_ (u"ࠥࡺࡦࡲࡵࡦࡵࠥẪ"), [])
            for val in values:
                if val not in bstack1111lll1l1l_opy_:
                    bstack1111lll1l1l_opy_.append(val)
            bstack1111lll11l1_opy_[bstack1l1llll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦẫ")] = bstack1111lll1l1l_opy_
        else:
            bstack1111lll1l11_opy_[bstack1lll1llllll_opy_] = bstack1111ll1llll_opy_
    @staticmethod
    def get_test_level_custom_metadata() -> Dict[str, Dict[str, Any]]:
        return CustomTagManager._1111lll1111_opy_
    @staticmethod
    def reset_test_level_custom_metadata() -> None:
        bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡰࡪࡧࡲࠡࡣ࡯ࡰࠥࡺࡥࡴࡶ࠰ࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡢࡥࡦࡹࡲࡻ࡬ࡢࡶࡨࡨࠥࡹ࡯ࠡࡨࡤࡶ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡎࡷࡶࡸࠥࡨࡥࠡࡥࡤࡰࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡦࡣࡦ࡬ࠥࡺࡥࡴࡶࠪࡷࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡦࡳࡳࡹࡵ࡮ࡧࡧࠤࡦࡴࡤࠡࡵࡨࡲࡹ࠲ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡵࡲࠤࡹ࡮ࡡࡵࠢࡶࡹࡧࡹࡥࡲࡷࡨࡲࡹࠦࡴࡦࡵࡷࡷࠥࡪ࡯ࠡࡰࡲࡸࠥ࡯࡮ࡩࡧࡵ࡭ࡹࠦࡴࡢࡩࡶࠤ࡫ࡸ࡯࡮ࠢࡳࡶࡪࡼࡩࡰࡷࡶࠤࡹ࡫ࡳࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡛ࠥࡳࡦࡵࠣࡶࡪࡧࡳࡴ࡫ࡪࡲࡲ࡫࡮ࡵࠢࠫࡲࡴࡺࠠࡥ࡫ࡦࡸ࠳ࡩ࡬ࡦࡣࡵ࠭ࠥࡺ࡯ࠡࡣࡹࡳ࡮ࡪࠠ࡮ࡷࡷࡥࡹ࡯࡮ࡨࠢࡤࡲࡾࠦ࡬ࡪࡸࡨࠤࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡪࡨࡰࡩࠦࡢࡺࠢࡤࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡷ࡬ࡦࡺࠠࡸࡣࡶࠤࡸ࡫ࡴࠡࡸ࡬ࡥࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴࠪࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤẬ")
        CustomTagManager._1111lll1111_opy_ = {}
    @staticmethod
    def bstack1111ll1ll11_opy_() -> Dict[str, Dict[str, Any]]:
        return CustomTagManager._1111ll1ll1l_opy_
    @staticmethod
    def bstack1111lll111l_opy_(bstack1111ll1lll1_opy_: str) -> List[str]:
        bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘࡴࡱࡥ࡯࡫ࡽࡩࠥࡧࠠࡤࡱࡰࡱࡦ࠳ࡳࡦࡲࡤࡶࡦࡺࡥࡥࠢࡶࡸࡷ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡴࡨࡷࡵ࡫ࡣࡵ࡫ࡱ࡫ࠥࡪ࡯ࡶࡤ࡯ࡩ࠲ࡷࡵࡰࡶࡨࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࡳࡶࡤࡶࡸࡷ࡯࡮ࡨࡵ࠱ࠤࡒࡧࡴࡤࡪࡨࡷࠥࡺࡨࡦࠢࡦࡶࡴࡹࡳ࠮ࡕࡇࡏࠥ࠮࡮ࡰࡦࡨ࠭ࠥࡺ࡯࡬ࡧࡱ࡭ࡿ࡫ࡲࠡࡨࡲࡶࠥࡨࡹࡵࡧ࠰࡭ࡩ࡫࡮ࡵ࡫ࡦࡥࡱࠐࠠࠡࠢࠣࠤࠥࠦࠠࡰࡷࡷࡴࡺࡺ࠺ࠡࡳࡸࡳࡹ࡫ࡤࠡࡵࡨ࡫ࡲ࡫࡮ࡵࡵࠣࡴࡷ࡫ࡳࡦࡴࡹࡩࠥࡺࡨࡦ࡫ࡵࠤࡪࡳࡢࡦࡦࡧࡩࡩࠦࡣࡰ࡯ࡰࡥࡸࠦࡶࡦࡴࡥࡥࡹ࡯࡭࠭ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡹࡳࡷࡵࡰࡶࡨࡨࠥࡺ࡯࡬ࡧࡱࡷࠥࡧࡲࡦࠢࡷࡶ࡮ࡳ࡭ࡦࡦ࠯ࠤࡦࡴࡤࠡࡧࡰࡴࡹࡿࠠࡵࡱ࡮ࡩࡳࡹࠠࡢࡴࡨࠤࡩࡸ࡯ࡱࡲࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡆࡺࡤࡱࡵࡲࡥࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠩࡤ࠰ࠥࠨࡢ࠭ࡥࠥ࠰ࠥࡪࠧࠡࠢࠣ࠱ࡃ࡛ࠦࠨࡣࠪ࠰ࠥ࠭ࡢ࠭ࡥࠪ࠰ࠥ࠭ࡤࠨ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠩࡗࡇ࠲࠷ࠬࠡ࠮ࠣࡘࡈ࠳࠲ࠨࠢࠣ࠱ࡃ࡛ࠦࠨࡖࡆ࠱࠶࠭ࠬࠡࠩࡗࡇ࠲࠸ࠧ࡞ࠢࠣࠤࠥࠦࠨࡦ࡯ࡳࡸࡾࠦࡴࡰ࡭ࡨࡲࠥࡪࡲࡰࡲࡳࡩࡩ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠭ࡨࡦࡣࡧࡩࡷ࠲ࠠࠣࡣ࠯ࡦࠧ࠭ࠠ࠮ࡀࠣ࡟ࠬ࡮ࡥࡢࡦࡨࡶࠬ࠲ࠠࠨࡣ࠯ࡦࠬࡣࠠࠡࠢࠣࠬࡶࡻ࡯ࡵࡧࠣࡥ࡫ࡺࡥࡳࠢࡤࠤࡸࡶࡡࡤࡧࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣậ")
        pattern = re.compile(bstack1l1llll_opy_ (u"ࡲࠨ࡞ࡶ࠮ࠧ࠮࡛࡟ࠤࡠ࠮࠮ࠨ࡜ࡴࠬࡿ࡟ࡣ࠲࡝ࠬࠩẮ"))
        result = []
        for match in pattern.finditer(bstack1111ll1lll1_opy_):
            if match.group(1) is not None:
                token = match.group(1)
            else:
                token = match.group(0).strip()
            if token != bstack1l1llll_opy_ (u"ࠣࠤắ"):
                result.append(token)
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1l1llll_opy_ (u"ࠤࡘࡸ࡮ࡲࡩࡵࡻࠣࡧࡱࡧࡳࡴࠢࡶ࡬ࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡶ࡬ࡥࡹ࡫ࡤࠣẰ"))