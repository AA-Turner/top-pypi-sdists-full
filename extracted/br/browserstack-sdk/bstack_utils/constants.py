# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import re
from enum import Enum
bstack11l1l1ll11_opy_ = {
  bstack1l111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᷨ"): bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪᷩ"),
  bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᷪ"): bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫᷫ"),
  bstack1l111l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᷬ"): bstack1l111l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᷭ"),
  bstack1l111l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᷮ"): bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᷯ"),
  bstack1l111l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᷰ"): bstack1l111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨᷱ"),
  bstack1l111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᷲ"): bstack1l111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨᷳ"),
  bstack1l111l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᷴ"): bstack1l111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᷵"),
  bstack1l111l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫ᷶"): bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪ᷷ࠫ"),
  bstack1l111l_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷ᷸ࠬ"): bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨ᷹"),
  bstack1l111l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹ᷺ࠧ"): bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧ᷻"),
  bstack1l111l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨ᷼"): bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨ᷽"),
  bstack1l111l_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬ᷾"): bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳ᷿ࠬ"),
  bstack1l111l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧḀ"): bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧḁ"),
  bstack1l111l_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪḂ"): bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪḃ"),
  bstack1l111l_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪḄ"): bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪḅ"),
  bstack1l111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩḆ"): bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩḇ"),
  bstack1l111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫḈ"): bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬḉ"),
  bstack1l111l_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪḊ"): bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪḋ"),
  bstack1l111l_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫḌ"): bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫḍ"),
  bstack1l111l_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨḎ"): bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨḏ"),
  bstack1l111l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬḐ"): bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬḑ"),
  bstack1l111l_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧḒ"): bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧḓ"),
  bstack1l111l_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭Ḕ"): bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭ḕ"),
  bstack1l111l_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪḖ"): bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪḗ"),
  bstack1l111l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬḘ"): bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬḙ"),
  bstack1l111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩḚ"): bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩḛ"),
  bstack1l111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬḜ"): bstack1l111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩḝ"),
  bstack1l111l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧḞ"): bstack1l111l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩḟ"),
  bstack1l111l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬḠ"): bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ḡ"),
  bstack1l111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧḢ"): bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧḣ"),
  bstack1l111l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪḤ"): bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪḥ"),
  bstack1l111l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪḦ"): bstack1l111l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ḧ"),
  bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨḨ"): bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨḩ"),
  bstack1l111l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨḪ"): bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨḫ"),
  bstack1l111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬḬ"): bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬḭ"),
  bstack1l111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧḮ"): bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧḯ"),
  bstack1l111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪḰ"): bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪḱ"),
  bstack1l111l_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭Ḳ"): bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ḳ"),
  bstack1l111l_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩḴ"): bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩḵ"),
  bstack1l111l_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩḶ"): bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩḷ"),
  bstack1l111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪḸ"): bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪḹ")
}
bstack1111111llll_opy_ = [
  bstack1l111l_opy_ (u"ࠪࡳࡸ࠭Ḻ"),
  bstack1l111l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧḻ"),
  bstack1l111l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧḼ"),
  bstack1l111l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫḽ"),
  bstack1l111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫḾ"),
  bstack1l111l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬḿ"),
  bstack1l111l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩṀ"),
]
bstack111l1lll1l_opy_ = {
  bstack1l111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬṁ"): [bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬṂ"), bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡑࡅࡒࡋࠧṃ")],
  bstack1l111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩṄ"): bstack1l111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪṅ"),
  bstack1l111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫṆ"): bstack1l111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬṇ"),
  bstack1l111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨṈ"): bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠩṉ"),
  bstack1l111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧṊ"): bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨṋ"),
  bstack1l111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧṌ"): bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡕࡢࡔࡊࡘ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩṍ"),
  bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭Ṏ"): bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨṏ"),
  bstack1l111l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨṐ"): bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩṑ"),
  bstack1l111l_opy_ (u"࠭ࡡࡱࡲࠪṒ"): [bstack1l111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࡢࡍࡉ࠭ṓ"), bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࠫṔ")],
  bstack1l111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫṕ"): bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡌࡐࡉࡏࡉ࡛ࡋࡌࠨṖ"),
  bstack1l111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨṗ"): bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨṘ"),
  bstack1l111l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪṙ"): [bstack1l111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠫṚ"), bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨṛ")],
  bstack1l111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Ṝ"): bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗ࡙ࡗࡈࡏࡔࡅࡄࡐࡊ࠭ṝ"),
  bstack1l111l_opy_ (u"ࠫࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡋࡎࡗࠩṞ"): bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡔࡘࡃࡉࡇࡖࡘࡗࡇࡔࡊࡑࡑࡣࡘࡓࡁࡓࡖࡢࡗࡊࡒࡅࡄࡖࡌࡓࡓࡥࡆࡆࡃࡗ࡙ࡗࡋ࡟ࡃࡔࡄࡒࡈࡎࡅࡔࠩṟ")
}
bstack111l1lll1_opy_ = {
  bstack1l111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨṠ"): [bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡣࡳࡧ࡭ࡦࠩṡ"), bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡓࡧ࡭ࡦࠩṢ")],
  bstack1l111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬṣ"): [bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡡ࡮ࡩࡾ࠭Ṥ"), bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ṥ")],
  bstack1l111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨṦ"): bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨṧ"),
  bstack1l111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬṨ"): bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬṩ"),
  bstack1l111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫṪ"): bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫṫ"),
  bstack1l111l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫṬ"): [bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡶࡰࠨṭ"), bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬṮ")],
  bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫṯ"): bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭Ṱ"),
  bstack1l111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ṱ"): bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭Ṳ"),
  bstack1l111l_opy_ (u"ࠫࡦࡶࡰࠨṳ"): bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࠨṴ"),
  bstack1l111l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨṵ"): bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨṶ"),
  bstack1l111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬṷ"): bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬṸ"),
  bstack1l111l_opy_ (u"ࠥࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡈࡒࡉࠣṹ"): bstack1l111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࠤṺ"),
}
bstack111l111l1l_opy_ = {
  bstack1l111l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨṻ"): bstack1l111l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪṼ"),
  bstack1l111l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩṽ"): [bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪṾ"), bstack1l111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬṿ")],
  bstack1l111l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨẀ"): bstack1l111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩẁ"),
  bstack1l111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩẂ"): bstack1l111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ẃ"),
  bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬẄ"): [bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩẅ"), bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨẆ")],
  bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫẇ"): bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭Ẉ"),
  bstack1l111l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩẉ"): bstack1l111l_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫẊ"),
  bstack1l111l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧẋ"): [bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨẌ"), bstack1l111l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪẍ")],
  bstack1l111l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩẎ"): [bstack1l111l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬẏ"), bstack1l111l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬẐ")]
}
bstack1lll1l111_opy_ = [
  bstack1l111l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬẑ"),
  bstack1l111l_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪẒ"),
  bstack1l111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧẓ"),
  bstack1l111l_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩẔ"),
  bstack1l111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬẕ"),
  bstack1l111l_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩẖ"),
  bstack1l111l_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨẗ"),
  bstack1l111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫẘ"),
  bstack1l111l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬẙ"),
  bstack1l111l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩẚ"),
  bstack1l111l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨẛ"),
  bstack1l111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫẜ"),
]
bstack11lll1l1ll_opy_ = [
  bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨẝ"),
  bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩẞ"),
  bstack1l111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬẟ"),
  bstack1l111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧẠ"),
  bstack1l111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫạ"),
  bstack1l111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫẢ"),
  bstack1l111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ả"),
  bstack1l111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨẤ"),
  bstack1l111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨấ"),
  bstack1l111l_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫẦ"),
  bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫầ"),
  bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨẨ"),
  bstack1l111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫẩ"),
  bstack1l111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡗࡥ࡬࠭Ẫ"),
  bstack1l111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨẫ"),
  bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧẬ"),
  bstack1l111l_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪậ"),
  bstack1l111l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠶࠭Ắ"),
  bstack1l111l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠸ࠧắ"),
  bstack1l111l_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠳ࠨẰ"),
  bstack1l111l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠵ࠩằ"),
  bstack1l111l_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠷ࠪẲ"),
  bstack1l111l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠹ࠫẳ"),
  bstack1l111l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠻ࠬẴ"),
  bstack1l111l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠽࠭ẵ"),
  bstack1l111l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠿ࠧẶ"),
  bstack1l111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨặ"),
  bstack1l111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩẸ"),
  bstack1l111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧẹ"),
  bstack1l111l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧẺ"),
  bstack1l111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪẻ"),
  bstack1l111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫẼ"),
  bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬẽ"),
  bstack1l111l_opy_ (u"ࠩ࡫ࡹࡧࡘࡥࡨ࡫ࡲࡲࠬẾ")
]
bstack111111ll1ll_opy_ = [
  bstack1l111l_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨế"),
  bstack1l111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ề"),
  bstack1l111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨề"),
  bstack1l111l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫỂ"),
  bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡕࡸࡩࡰࡴ࡬ࡸࡾ࠭ể"),
  bstack1l111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫỄ"),
  bstack1l111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡕࡣࡪࠫễ"),
  bstack1l111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨỆ"),
  bstack1l111l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ệ"),
  bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪỈ"),
  bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧỉ"),
  bstack1l111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭Ị"),
  bstack1l111l_opy_ (u"ࠨࡱࡶࠫị"),
  bstack1l111l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬỌ"),
  bstack1l111l_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩọ"),
  bstack1l111l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭Ỏ"),
  bstack1l111l_opy_ (u"ࠬࡸࡥࡨ࡫ࡲࡲࠬỏ"),
  bstack1l111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨỐ"),
  bstack1l111l_opy_ (u"ࠧ࡮ࡣࡦ࡬࡮ࡴࡥࠨố"),
  bstack1l111l_opy_ (u"ࠨࡴࡨࡷࡴࡲࡵࡵ࡫ࡲࡲࠬỒ"),
  bstack1l111l_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧồ"),
  bstack1l111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧỔ"),
  bstack1l111l_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪổ"),
  bstack1l111l_opy_ (u"ࠬࡴ࡯ࡑࡣࡪࡩࡑࡵࡡࡥࡖ࡬ࡱࡪࡵࡵࡵࠩỖ"),
  bstack1l111l_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧỗ"),
  bstack1l111l_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭Ộ"),
  bstack1l111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬộ"),
  bstack1l111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡨࡲࡩࡑࡥࡺࡵࠪỚ"),
  bstack1l111l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧớ"),
  bstack1l111l_opy_ (u"ࠫࡳࡵࡐࡪࡲࡨࡰ࡮ࡴࡥࠨỜ"),
  bstack1l111l_opy_ (u"ࠬࡩࡨࡦࡥ࡮࡙ࡗࡒࠧờ"),
  bstack1l111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨỞ"),
  bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡃࡰࡱ࡮࡭ࡪࡹࠧở"),
  bstack1l111l_opy_ (u"ࠨࡥࡤࡴࡹࡻࡲࡦࡅࡵࡥࡸ࡮ࠧỠ"),
  bstack1l111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ỡ"),
  bstack1l111l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪỢ"),
  bstack1l111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡗࡧࡵࡷ࡮ࡵ࡮ࠨợ"),
  bstack1l111l_opy_ (u"ࠬࡴ࡯ࡃ࡮ࡤࡲࡰࡖ࡯࡭࡮࡬ࡲ࡬࠭Ụ"),
  bstack1l111l_opy_ (u"࠭࡭ࡢࡵ࡮ࡗࡪࡴࡤࡌࡧࡼࡷࠬụ"),
  bstack1l111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡌࡰࡩࡶࠫỦ"),
  bstack1l111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡊࡦࠪủ"),
  bstack1l111l_opy_ (u"ࠩࡧࡩࡩ࡯ࡣࡢࡶࡨࡨࡉ࡫ࡶࡪࡥࡨࠫỨ"),
  bstack1l111l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡓࡥࡷࡧ࡭ࡴࠩứ"),
  bstack1l111l_opy_ (u"ࠫࡵ࡮࡯࡯ࡧࡑࡹࡲࡨࡥࡳࠩỪ"),
  bstack1l111l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪừ"),
  bstack1l111l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡓࡵࡺࡩࡰࡰࡶࠫỬ"),
  bstack1l111l_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬử"),
  bstack1l111l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨỮ"),
  bstack1l111l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ữ"),
  bstack1l111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡅ࡭ࡴࡳࡥࡵࡴ࡬ࡧࠬỰ"),
  bstack1l111l_opy_ (u"ࠫࡻ࡯ࡤࡦࡱ࡙࠶ࠬự"),
  bstack1l111l_opy_ (u"ࠬࡳࡩࡥࡕࡨࡷࡸ࡯࡯࡯ࡋࡱࡷࡹࡧ࡬࡭ࡃࡳࡴࡸ࠭Ỳ"),
  bstack1l111l_opy_ (u"࠭ࡥࡴࡲࡵࡩࡸࡹ࡯ࡔࡧࡵࡺࡪࡸࠧỳ"),
  bstack1l111l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭Ỵ"),
  bstack1l111l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡆࡨࡵ࠭ỵ"),
  bstack1l111l_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩỶ"),
  bstack1l111l_opy_ (u"ࠪࡷࡾࡴࡣࡕ࡫ࡰࡩ࡜࡯ࡴࡩࡐࡗࡔࠬỷ"),
  bstack1l111l_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩỸ"),
  bstack1l111l_opy_ (u"ࠬ࡭ࡰࡴࡎࡲࡧࡦࡺࡩࡰࡰࠪỹ"),
  bstack1l111l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧỺ"),
  bstack1l111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧỻ"),
  bstack1l111l_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࡃࡩࡣࡱ࡫ࡪࡐࡡࡳࠩỼ"),
  bstack1l111l_opy_ (u"ࠩࡻࡱࡸࡐࡡࡳࠩỽ"),
  bstack1l111l_opy_ (u"ࠪࡼࡲࡾࡊࡢࡴࠪỾ"),
  bstack1l111l_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪỿ"),
  bstack1l111l_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬἀ"),
  bstack1l111l_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧἁ"),
  bstack1l111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪἂ"),
  bstack1l111l_opy_ (u"ࠨࡣࡳࡴ࡛࡫ࡲࡴ࡫ࡲࡲࠬἃ"),
  bstack1l111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨἄ"),
  bstack1l111l_opy_ (u"ࠪࡶࡪࡹࡩࡨࡰࡄࡴࡵ࠭ἅ"),
  bstack1l111l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࡳࠨἆ"),
  bstack1l111l_opy_ (u"ࠬࡩࡡ࡯ࡣࡵࡽࠬἇ"),
  bstack1l111l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧἈ"),
  bstack1l111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧἉ"),
  bstack1l111l_opy_ (u"ࠨ࡫ࡨࠫἊ"),
  bstack1l111l_opy_ (u"ࠩࡨࡨ࡬࡫ࠧἋ"),
  bstack1l111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪἌ"),
  bstack1l111l_opy_ (u"ࠫࡶࡻࡥࡶࡧࠪἍ"),
  bstack1l111l_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡲࡦࡲࠧἎ"),
  bstack1l111l_opy_ (u"࠭ࡡࡱࡲࡖࡸࡴࡸࡥࡄࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠧἏ"),
  bstack1l111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡃࡢ࡯ࡨࡶࡦࡏ࡭ࡢࡩࡨࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭ἐ"),
  bstack1l111l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡋࡸࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫἑ"),
  bstack1l111l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡉ࡯ࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬἒ"),
  bstack1l111l_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧἓ"),
  bstack1l111l_opy_ (u"ࠫࡷ࡫ࡳࡦࡴࡹࡩࡉ࡫ࡶࡪࡥࡨࠫἔ"),
  bstack1l111l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬἕ"),
  bstack1l111l_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨ἖"),
  bstack1l111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡢࡵࡶࡧࡴࡪࡥࠨ἗"),
  bstack1l111l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡊࡱࡶࡈࡪࡼࡩࡤࡧࡖࡩࡹࡺࡩ࡯ࡩࡶࠫἘ"),
  bstack1l111l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡸࡨ࡮ࡵࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩἙ"),
  bstack1l111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡴࡵࡲࡥࡑࡣࡼࠫἚ"),
  bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬἛ"),
  bstack1l111l_opy_ (u"ࠬࡽࡤࡪࡱࡖࡩࡷࡼࡩࡤࡧࠪἜ"),
  bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨἝ"),
  bstack1l111l_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡄࡴࡲࡷࡸ࡙ࡩࡵࡧࡗࡶࡦࡩ࡫ࡪࡰࡪࠫ἞"),
  bstack1l111l_opy_ (u"ࠨࡪ࡬࡫࡭ࡉ࡯࡯ࡶࡵࡥࡸࡺࠧ἟"),
  bstack1l111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡒࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࡸ࠭ἠ"),
  bstack1l111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ἡ"),
  bstack1l111l_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨἢ"),
  bstack1l111l_opy_ (u"ࠬࡸࡥ࡮ࡱࡹࡩࡎࡕࡓࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࡑࡵࡣࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪἣ"),
  bstack1l111l_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨἤ"),
  bstack1l111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩἥ"),
  bstack1l111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪἦ"),
  bstack1l111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨἧ"),
  bstack1l111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬἨ"),
  bstack1l111l_opy_ (u"ࠫࡵࡧࡧࡦࡎࡲࡥࡩ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧἩ"),
  bstack1l111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫἪ"),
  bstack1l111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࡳࠨἫ"),
  bstack1l111l_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪἬ")
]
bstack1lllll111l_opy_ = {
  bstack1l111l_opy_ (u"ࠨࡸࠪἭ"): bstack1l111l_opy_ (u"ࠩࡹࠫἮ"),
  bstack1l111l_opy_ (u"ࠪࡪࠬἯ"): bstack1l111l_opy_ (u"ࠫ࡫࠭ἰ"),
  bstack1l111l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫἱ"): bstack1l111l_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬἲ"),
  bstack1l111l_opy_ (u"ࠧࡰࡰ࡯ࡽࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ἳ"): bstack1l111l_opy_ (u"ࠨࡱࡱࡰࡾࡇࡵࡵࡱࡰࡥࡹ࡫ࠧἴ"),
  bstack1l111l_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭ἵ"): bstack1l111l_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧἶ"),
  bstack1l111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧἷ"): bstack1l111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨἸ"),
  bstack1l111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩἹ"): bstack1l111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪἺ"),
  bstack1l111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫἻ"): bstack1l111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬἼ"),
  bstack1l111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭Ἵ"): bstack1l111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧἾ"),
  bstack1l111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭Ἷ"): bstack1l111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡋࡳࡸࡺࠧὀ"),
  bstack1l111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨὁ"): bstack1l111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩὂ"),
  bstack1l111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪὃ"): bstack1l111l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬὄ"),
  bstack1l111l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ὅ"): bstack1l111l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧ὆"),
  bstack1l111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧ὇"): bstack1l111l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩὈ"),
  bstack1l111l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪὉ"): bstack1l111l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫὊ"),
  bstack1l111l_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧὋ"): bstack1l111l_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨὌ"),
  bstack1l111l_opy_ (u"ࠬࡶࡡࡤࡨ࡬ࡰࡪ࠭Ὅ"): bstack1l111l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ὎"),
  bstack1l111l_opy_ (u"ࠧࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ὏"): bstack1l111l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫὐ"),
  bstack1l111l_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬὑ"): bstack1l111l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ὒ"),
  bstack1l111l_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬὓ"): bstack1l111l_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭ὔ"),
  bstack1l111l_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨὕ"): bstack1l111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩὖ"),
  bstack1l111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠪὗ"): bstack1l111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡴࡪࡧࡴࡦࡴࠪ὘")
}
bstack11111ll111l_opy_ = bstack1l111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬࡯ࡴࡩࡷࡥ࠲ࡨࡵ࡭࠰ࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬࠳ࡷ࡫࡬ࡦࡣࡶࡩࡸ࠵࡬ࡢࡶࡨࡷࡹ࠵ࡤࡰࡹࡱࡰࡴࡧࡤࠣὙ")
bstack11111l1ll1l_opy_ = bstack1l111l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠳࡭࡫ࡡ࡭ࡶ࡫ࡧ࡭࡫ࡣ࡬ࠤ὚")
bstack11llll1111_opy_ = bstack1l111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡥࡥࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡳࡦࡰࡧࡣࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣὛ")
bstack1llllllll1_opy_ = bstack1l111l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧ὜")
bstack11ll1l1lll_opy_ = bstack1l111l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪὝ")
bstack1ll1ll11_opy_ = bstack1l111l_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠹࠺࠴࠵࠱ࡺࡨ࠴࡮ࡵࡣࠩ὞")
bstack1llllllll1l_opy_ = bstack1l111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡲࡪࡾࡴࡠࡪࡸࡦࡸ࠭Ὗ")
bstack1lllllll111_opy_ = {
  bstack1l111l_opy_ (u"ࠪࡨࡪ࡬ࡡࡶ࡮ࡷࠫὠ"): bstack1l111l_opy_ (u"ࠫ࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫὡ"),
  bstack1l111l_opy_ (u"ࠬࡻࡳ࠮ࡧࡤࡷࡹ࠭ὢ"): bstack1l111l_opy_ (u"࠭ࡨࡶࡤ࠰ࡹࡸ࡫࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨὣ"),
  bstack1l111l_opy_ (u"ࠧࡶࡵࠪὤ"): bstack1l111l_opy_ (u"ࠨࡪࡸࡦ࠲ࡻࡳ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩὥ"),
  bstack1l111l_opy_ (u"ࠩࡨࡹࠬὦ"): bstack1l111l_opy_ (u"ࠪ࡬ࡺࡨ࠭ࡦࡷ࠰ࡳࡳࡲࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫὧ"),
  bstack1l111l_opy_ (u"ࠫ࡮ࡴࠧὨ"): bstack1l111l_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡤࡴࡸ࠳࡯࡯࡮ࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧὩ"),
  bstack1l111l_opy_ (u"࠭ࡡࡶࠩὪ"): bstack1l111l_opy_ (u"ࠧࡩࡷࡥ࠱ࡦࡶࡳࡦ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪὫ")
}
bstack1111111ll11_opy_ = {
  bstack1l111l_opy_ (u"ࠨࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠪὬ"): 50,
  bstack1l111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨὭ"): 40,
  bstack1l111l_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫὮ"): 30,
  bstack1l111l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩὯ"): 20,
  bstack1l111l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫὰ"): 10
}
bstack1l1lllll1l_opy_ = bstack1111111ll11_opy_[bstack1l111l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫά")]
bstack1111ll11l_opy_ = bstack1l111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣ࠰ࠩὲ")
bstack1111l11111_opy_ = bstack1l111l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭έ")
bstack1ll1l111_opy_ = bstack1l111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨὴ")
bstack111l1l11l_opy_ = bstack1l111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩή")
bstack1l11l111_opy_ = bstack1l111l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡧ࡮ࡥࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡵࡧࡣ࡬ࡣࡪࡩࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩὶ")
bstack111l11l1ll_opy_ = {
  bstack1l111l_opy_ (u"࡙ࠬࡄࡌ࠯ࡊࡉࡓ࠳࠰࠱࠷ࠪί"): bstack1l111l_opy_ (u"࠭ࠪࠫࠬࠣ࡟ࡘࡊࡋ࠮ࡉࡈࡒ࠲࠶࠰࠶࡟ࠣࡤࡵࡿࡴࡦࡵࡷ࠱ࡵࡧࡲࡢ࡮࡯ࡩࡱࡦࠠࡪࡵࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡩ࡯ࠢࡼࡳࡺࡸࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸ࠳ࠦࡔࡩ࡫ࡶࠤࡲࡧࡹࠡࡥࡤࡹࡸ࡫ࠠࡤࡱࡱࡪࡱ࡯ࡣࡵࡵࠣࡻ࡮ࡺࡨࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡻ࡮ࡪࡰࡶࡸࡦࡲ࡬ࠡ࡫ࡷࠤࡺࡹࡩ࡯ࡩ࠽ࠤࡵ࡯ࡰࠡࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡵࡧࡲࡢ࡮࡯ࡩࡱࠦࠪࠫࠬࠪὸ")
}
bstack1111111l1ll_opy_ = [bstack1l111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨό"), bstack1l111l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨὺ")]
bstack111111lll1l_opy_ = [bstack1l111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬύ"), bstack1l111l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬὼ")]
bstack1111l111ll_opy_ = re.compile(bstack1l111l_opy_ (u"ࠫࡣࡡ࡜࡝ࡹ࠰ࡡ࠰ࡀ࠮ࠫࠦࠪώ"))
bstack11llllll11_opy_ = [
  bstack1l111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡐࡤࡱࡪ࠭὾"),
  bstack1l111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ὿"),
  bstack1l111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᾀ"),
  bstack1l111l_opy_ (u"ࠨࡰࡨࡻࡈࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࠬᾁ"),
  bstack1l111l_opy_ (u"ࠩࡤࡴࡵ࠭ᾂ"),
  bstack1l111l_opy_ (u"ࠪࡹࡩ࡯ࡤࠨᾃ"),
  bstack1l111l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᾄ"),
  bstack1l111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࠬᾅ"),
  bstack1l111l_opy_ (u"࠭࡯ࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫᾆ"),
  bstack1l111l_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻࠬᾇ"),
  bstack1l111l_opy_ (u"ࠨࡰࡲࡖࡪࡹࡥࡵࠩᾈ"), bstack1l111l_opy_ (u"ࠩࡩࡹࡱࡲࡒࡦࡵࡨࡸࠬᾉ"),
  bstack1l111l_opy_ (u"ࠪࡧࡱ࡫ࡡࡳࡕࡼࡷࡹ࡫࡭ࡇ࡫࡯ࡩࡸ࠭ᾊ"),
  bstack1l111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡗ࡭ࡲ࡯࡮ࡨࡵࠪᾋ"),
  bstack1l111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕ࡫ࡲࡧࡱࡵࡱࡦࡴࡣࡦࡎࡲ࡫࡬࡯࡮ࡨࠩᾌ"),
  bstack1l111l_opy_ (u"࠭࡯ࡵࡪࡨࡶࡆࡶࡰࡴࠩᾍ"),
  bstack1l111l_opy_ (u"ࠧࡱࡴ࡬ࡲࡹࡖࡡࡨࡧࡖࡳࡺࡸࡣࡦࡑࡱࡊ࡮ࡴࡤࡇࡣ࡬ࡰࡺࡸࡥࠨᾎ"),
  bstack1l111l_opy_ (u"ࠨࡣࡳࡴࡆࡩࡴࡪࡸ࡬ࡸࡾ࠭ᾏ"), bstack1l111l_opy_ (u"ࠩࡤࡴࡵࡖࡡࡤ࡭ࡤ࡫ࡪ࠭ᾐ"), bstack1l111l_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡅࡨࡺࡩࡷ࡫ࡷࡽࠬᾑ"), bstack1l111l_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡕࡧࡣ࡬ࡣࡪࡩࠬᾒ"), bstack1l111l_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡊࡵࡳࡣࡷ࡭ࡴࡴࠧᾓ"),
  bstack1l111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫᾔ"),
  bstack1l111l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼ࡚ࡥࡴࡶࡓࡥࡨࡱࡡࡨࡧࡶࠫᾕ"),
  bstack1l111l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡅࡲࡺࡪࡸࡡࡨࡧࠪᾖ"), bstack1l111l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡆࡳࡻ࡫ࡲࡢࡩࡨࡉࡳࡪࡉ࡯ࡶࡨࡲࡹ࠭ᾗ"),
  bstack1l111l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨᾘ"),
  bstack1l111l_opy_ (u"ࠫࡦࡪࡢࡑࡱࡵࡸࠬᾙ"),
  bstack1l111l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡘࡵࡣ࡬ࡧࡷࠫᾚ"),
  bstack1l111l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡉ࡯ࡵࡷࡥࡱࡲࡔࡪ࡯ࡨࡳࡺࡺࠧᾛ"),
  bstack1l111l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡷ࡬ࠬᾜ"),
  bstack1l111l_opy_ (u"ࠨࡣࡹࡨࠬᾝ"), bstack1l111l_opy_ (u"ࠩࡤࡺࡩࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬᾞ"), bstack1l111l_opy_ (u"ࠪࡥࡻࡪࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬᾟ"), bstack1l111l_opy_ (u"ࠫࡦࡼࡤࡂࡴࡪࡷࠬᾠ"),
  bstack1l111l_opy_ (u"ࠬࡻࡳࡦࡍࡨࡽࡸࡺ࡯ࡳࡧࠪᾡ"), bstack1l111l_opy_ (u"࠭࡫ࡦࡻࡶࡸࡴࡸࡥࡑࡣࡷ࡬ࠬᾢ"), bstack1l111l_opy_ (u"ࠧ࡬ࡧࡼࡷࡹࡵࡲࡦࡒࡤࡷࡸࡽ࡯ࡳࡦࠪᾣ"),
  bstack1l111l_opy_ (u"ࠨ࡭ࡨࡽࡆࡲࡩࡢࡵࠪᾤ"), bstack1l111l_opy_ (u"ࠩ࡮ࡩࡾࡖࡡࡴࡵࡺࡳࡷࡪࠧᾥ"),
  bstack1l111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࠬᾦ"), bstack1l111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡄࡶ࡬ࡹࠧᾧ"), bstack1l111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࡄࡪࡴࠪᾨ"), bstack1l111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡈ࡮ࡲࡰ࡯ࡨࡑࡦࡶࡰࡪࡰࡪࡊ࡮ࡲࡥࠨᾩ"), bstack1l111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷ࡛ࡳࡦࡕࡼࡷࡹ࡫࡭ࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࠫᾪ"),
  bstack1l111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡐࡰࡴࡷࠫᾫ"), bstack1l111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡑࡱࡵࡸࡸ࠭ᾬ"),
  bstack1l111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡆ࡬ࡷࡦࡨ࡬ࡦࡄࡸ࡭ࡱࡪࡃࡩࡧࡦ࡯ࠬᾭ"),
  bstack1l111l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࡖ࡬ࡱࡪࡵࡵࡵࠩᾮ"),
  bstack1l111l_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡆࡩࡴࡪࡱࡱࠫᾯ"), bstack1l111l_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡉࡡࡵࡧࡪࡳࡷࡿࠧᾰ"), bstack1l111l_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡆ࡭ࡣࡪࡷࠬᾱ"), bstack1l111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࡌࡲࡹ࡫࡮ࡵࡃࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᾲ"),
  bstack1l111l_opy_ (u"ࠩࡧࡳࡳࡺࡓࡵࡱࡳࡅࡵࡶࡏ࡯ࡔࡨࡷࡪࡺࠧᾳ"),
  bstack1l111l_opy_ (u"ࠪࡹࡳ࡯ࡣࡰࡦࡨࡏࡪࡿࡢࡰࡣࡵࡨࠬᾴ"), bstack1l111l_opy_ (u"ࠫࡷ࡫ࡳࡦࡶࡎࡩࡾࡨ࡯ࡢࡴࡧࠫ᾵"),
  bstack1l111l_opy_ (u"ࠬࡴ࡯ࡔ࡫ࡪࡲࠬᾶ"),
  bstack1l111l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࡛࡮ࡪ࡯ࡳࡳࡷࡺࡡ࡯ࡶ࡙࡭ࡪࡽࡳࠨᾷ"),
  bstack1l111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡰࡧࡶࡴ࡯ࡤࡘࡣࡷࡧ࡭࡫ࡲࡴࠩᾸ"),
  bstack1l111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᾹ"),
  bstack1l111l_opy_ (u"ࠩࡵࡩࡨࡸࡥࡢࡶࡨࡇ࡭ࡸ࡯࡮ࡧࡇࡶ࡮ࡼࡥࡳࡕࡨࡷࡸ࡯࡯࡯ࡵࠪᾺ"),
  bstack1l111l_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩΆ"),
  bstack1l111l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡑࡣࡷ࡬ࠬᾼ"),
  bstack1l111l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰ࡙ࡰࡦࡧࡧࠫ᾽"),
  bstack1l111l_opy_ (u"࠭ࡧࡱࡵࡈࡲࡦࡨ࡬ࡦࡦࠪι"),
  bstack1l111l_opy_ (u"ࠧࡪࡵࡋࡩࡦࡪ࡬ࡦࡵࡶࠫ᾿"),
  bstack1l111l_opy_ (u"ࠨࡣࡧࡦࡊࡾࡥࡤࡖ࡬ࡱࡪࡵࡵࡵࠩ῀"),
  bstack1l111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࡕࡦࡶ࡮ࡶࡴࠨ῁"),
  bstack1l111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡅࡧࡹ࡭ࡨ࡫ࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧῂ"),
  bstack1l111l_opy_ (u"ࠫࡦࡻࡴࡰࡉࡵࡥࡳࡺࡐࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠫῃ"),
  bstack1l111l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡔࡡࡵࡷࡵࡥࡱࡕࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪῄ"),
  bstack1l111l_opy_ (u"࠭ࡳࡺࡵࡷࡩࡲࡖ࡯ࡳࡶࠪ῅"),
  bstack1l111l_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫ࡁࡥࡤࡋࡳࡸࡺࠧῆ"),
  bstack1l111l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡛࡮࡭ࡱࡦ࡯ࠬῇ"), bstack1l111l_opy_ (u"ࠩࡸࡲࡱࡵࡣ࡬ࡖࡼࡴࡪ࠭Ὲ"), bstack1l111l_opy_ (u"ࠪࡹࡳࡲ࡯ࡤ࡭ࡎࡩࡾ࠭Έ"),
  bstack1l111l_opy_ (u"ࠫࡦࡻࡴࡰࡎࡤࡹࡳࡩࡨࠨῊ"),
  bstack1l111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡩࡡࡵࡅࡤࡴࡹࡻࡲࡦࠩΉ"),
  bstack1l111l_opy_ (u"࠭ࡵ࡯࡫ࡱࡷࡹࡧ࡬࡭ࡑࡷ࡬ࡪࡸࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨῌ"),
  bstack1l111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡘ࡫ࡱࡨࡴࡽࡁ࡯࡫ࡰࡥࡹ࡯࡯࡯ࠩ῍"),
  bstack1l111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡰࡱ࡯ࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ῎"),
  bstack1l111l_opy_ (u"ࠩࡨࡲ࡫ࡵࡲࡤࡧࡄࡴࡵࡏ࡮ࡴࡶࡤࡰࡱ࠭῏"),
  bstack1l111l_opy_ (u"ࠪࡩࡳࡹࡵࡳࡧ࡚ࡩࡧࡼࡩࡦࡹࡶࡌࡦࡼࡥࡑࡣࡪࡩࡸ࠭ῐ"), bstack1l111l_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡉ࡫ࡶࡵࡱࡲࡰࡸࡖ࡯ࡳࡶࠪῑ"), bstack1l111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡉ࡫ࡴࡢ࡫࡯ࡷࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠨῒ"),
  bstack1l111l_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡇࡰࡱࡵࡆࡥࡨ࡮ࡥࡍ࡫ࡰ࡭ࡹ࠭ΐ"),
  bstack1l111l_opy_ (u"ࠧࡤࡣ࡯ࡩࡳࡪࡡࡳࡈࡲࡶࡲࡧࡴࠨ῔"),
  bstack1l111l_opy_ (u"ࠨࡤࡸࡲࡩࡲࡥࡊࡦࠪ῕"),
  bstack1l111l_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩῖ"),
  bstack1l111l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࡘ࡫ࡲࡷ࡫ࡦࡩࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ῗ"), bstack1l111l_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࡙ࡥࡳࡸ࡬ࡧࡪࡹࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡦࡦࠪῘ"),
  bstack1l111l_opy_ (u"ࠬࡧࡵࡵࡱࡄࡧࡨ࡫ࡰࡵࡃ࡯ࡩࡷࡺࡳࠨῙ"), bstack1l111l_opy_ (u"࠭ࡡࡶࡶࡲࡈ࡮ࡹ࡭ࡪࡵࡶࡅࡱ࡫ࡲࡵࡵࠪῚ"),
  bstack1l111l_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡉ࡯ࡵࡷࡶࡺࡳࡥ࡯ࡶࡶࡐ࡮ࡨࠧΊ"),
  bstack1l111l_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡘࡦࡶࠧ῜"),
  bstack1l111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡱ࡭ࡹ࡯ࡡ࡭ࡗࡵࡰࠬ῝"), bstack1l111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡄࡰࡱࡵࡷࡑࡱࡳࡹࡵࡹࠧ῞"), bstack1l111l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍ࡬ࡴ࡯ࡳࡧࡉࡶࡦࡻࡤࡘࡣࡵࡲ࡮ࡴࡧࠨ῟"), bstack1l111l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡥ࡯ࡎ࡬ࡲࡰࡹࡉ࡯ࡄࡤࡧࡰ࡭ࡲࡰࡷࡱࡨࠬῠ"),
  bstack1l111l_opy_ (u"࠭࡫ࡦࡧࡳࡏࡪࡿࡃࡩࡣ࡬ࡲࡸ࠭ῡ"),
  bstack1l111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡯ࡺࡢࡤ࡯ࡩࡘࡺࡲࡪࡰࡪࡷࡉ࡯ࡲࠨῢ"),
  bstack1l111l_opy_ (u"ࠨࡲࡵࡳࡨ࡫ࡳࡴࡃࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫΰ"),
  bstack1l111l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲࡌࡧࡼࡈࡪࡲࡡࡺࠩῤ"),
  bstack1l111l_opy_ (u"ࠪࡷ࡭ࡵࡷࡊࡑࡖࡐࡴ࡭ࠧῥ"),
  bstack1l111l_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ῦ"),
  bstack1l111l_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡗ࡫ࡳࡱࡱࡱࡷࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ῧ"), bstack1l111l_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶ࡚ࡥ࡮ࡺࡔࡪ࡯ࡨࡳࡺࡺࠧῨ"),
  bstack1l111l_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫ࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࠪῩ"),
  bstack1l111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡵࡼࡲࡨࡋࡸࡦࡥࡸࡸࡪࡌࡲࡰ࡯ࡋࡸࡹࡶࡳࠨῪ"),
  bstack1l111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡆࡥࡵࡺࡵࡳࡧࠪΎ"),
  bstack1l111l_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾࡖ࡯ࡳࡶࠪῬ"),
  bstack1l111l_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡅࡲࡲࡹ࡫ࡸࡵࡎ࡬ࡷࡹ࠭῭"),
  bstack1l111l_opy_ (u"ࠬࡽࡡࡪࡶࡉࡳࡷࡇࡰࡱࡕࡦࡶ࡮ࡶࡴࠨ΅"),
  bstack1l111l_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡃࡰࡰࡱࡩࡨࡺࡒࡦࡶࡵ࡭ࡪࡹࠧ`"),
  bstack1l111l_opy_ (u"ࠧࡢࡲࡳࡒࡦࡳࡥࠨ῰"),
  bstack1l111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡕࡏࡇࡪࡸࡴࠨ῱"),
  bstack1l111l_opy_ (u"ࠩࡷࡥࡵ࡝ࡩࡵࡪࡖ࡬ࡴࡸࡴࡑࡴࡨࡷࡸࡊࡵࡳࡣࡷ࡭ࡴࡴࠧῲ"),
  bstack1l111l_opy_ (u"ࠪࡷࡨࡧ࡬ࡦࡈࡤࡧࡹࡵࡲࠨῳ"),
  bstack1l111l_opy_ (u"ࠫࡼࡪࡡࡍࡱࡦࡥࡱࡖ࡯ࡳࡶࠪῴ"),
  bstack1l111l_opy_ (u"ࠬࡹࡨࡰࡹ࡛ࡧࡴࡪࡥࡍࡱࡪࠫ῵"),
  bstack1l111l_opy_ (u"࠭ࡩࡰࡵࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡺࡹࡥࠨῶ"),
  bstack1l111l_opy_ (u"ࠧࡹࡥࡲࡨࡪࡉ࡯࡯ࡨ࡬࡫ࡋ࡯࡬ࡦࠩῷ"),
  bstack1l111l_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡸࡹࡷࡰࡴࡧࠫῸ"),
  bstack1l111l_opy_ (u"ࠩࡸࡷࡪࡖࡲࡦࡤࡸ࡭ࡱࡺࡗࡅࡃࠪΌ"),
  bstack1l111l_opy_ (u"ࠪࡴࡷ࡫ࡶࡦࡰࡷ࡛ࡉࡇࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠫῺ"),
  bstack1l111l_opy_ (u"ࠫࡼ࡫ࡢࡅࡴ࡬ࡺࡪࡸࡁࡨࡧࡱࡸ࡚ࡸ࡬ࠨΏ"),
  bstack1l111l_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡶ࡫ࠫῼ"),
  bstack1l111l_opy_ (u"࠭ࡵࡴࡧࡑࡩࡼ࡝ࡄࡂࠩ´"),
  bstack1l111l_opy_ (u"ࠧࡸࡦࡤࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪ῾"), bstack1l111l_opy_ (u"ࠨࡹࡧࡥࡈࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࡕ࡫ࡰࡩࡴࡻࡴࠨ῿"),
  bstack1l111l_opy_ (u"ࠩࡻࡧࡴࡪࡥࡐࡴࡪࡍࡩ࠭ "), bstack1l111l_opy_ (u"ࠪࡼࡨࡵࡤࡦࡕ࡬࡫ࡳ࡯࡮ࡨࡋࡧࠫ "),
  bstack1l111l_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨ࡜ࡊࡁࡃࡷࡱࡨࡱ࡫ࡉࡥࠩ "),
  bstack1l111l_opy_ (u"ࠬࡸࡥࡴࡧࡷࡓࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡴࡷࡓࡳࡲࡹࠨ "),
  bstack1l111l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࡳࠨ "),
  bstack1l111l_opy_ (u"ࠧࡸࡦࡤࡗࡹࡧࡲࡵࡷࡳࡖࡪࡺࡲࡪࡧࡶࠫ "), bstack1l111l_opy_ (u"ࠨࡹࡧࡥࡘࡺࡡࡳࡶࡸࡴࡗ࡫ࡴࡳࡻࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠫ "),
  bstack1l111l_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࡋࡥࡷࡪࡷࡢࡴࡨࡏࡪࡿࡢࡰࡣࡵࡨࠬ "),
  bstack1l111l_opy_ (u"ࠪࡱࡦࡾࡔࡺࡲ࡬ࡲ࡬ࡌࡲࡦࡳࡸࡩࡳࡩࡹࠨ "),
  bstack1l111l_opy_ (u"ࠫࡸ࡯࡭ࡱ࡮ࡨࡍࡸ࡜ࡩࡴ࡫ࡥࡰࡪࡉࡨࡦࡥ࡮ࠫ "),
  bstack1l111l_opy_ (u"ࠬࡻࡳࡦࡅࡤࡶࡹ࡮ࡡࡨࡧࡖࡷࡱ࠭ "),
  bstack1l111l_opy_ (u"࠭ࡳࡩࡱࡸࡰࡩ࡛ࡳࡦࡕ࡬ࡲ࡬ࡲࡥࡵࡱࡱࡘࡪࡹࡴࡎࡣࡱࡥ࡬࡫ࡲࠨ​"),
  bstack1l111l_opy_ (u"ࠧࡴࡶࡤࡶࡹࡏࡗࡅࡒࠪ‌"),
  bstack1l111l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡔࡰࡷࡦ࡬ࡎࡪࡅ࡯ࡴࡲࡰࡱ࠭‍"),
  bstack1l111l_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡊ࡬ࡨࡩ࡫࡮ࡂࡲ࡬ࡔࡴࡲࡩࡤࡻࡈࡶࡷࡵࡲࠨ‎"),
  bstack1l111l_opy_ (u"ࠪࡱࡴࡩ࡫ࡍࡱࡦࡥࡹ࡯࡯࡯ࡃࡳࡴࠬ‏"),
  bstack1l111l_opy_ (u"ࠫࡱࡵࡧࡤࡣࡷࡊࡴࡸ࡭ࡢࡶࠪ‐"), bstack1l111l_opy_ (u"ࠬࡲ࡯ࡨࡥࡤࡸࡋ࡯࡬ࡵࡧࡵࡗࡵ࡫ࡣࡴࠩ‑"),
  bstack1l111l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡉ࡫࡬ࡢࡻࡄࡨࡧ࠭‒"),
  bstack1l111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡊࡦࡏࡳࡨࡧࡴࡰࡴࡄࡹࡹࡵࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠪ–")
]
bstack1llll1ll1_opy_ = bstack1l111l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡶࡲ࡯ࡳࡦࡪࠧ—")
bstack1l111ll111_opy_ = [bstack1l111l_opy_ (u"ࠩ࠱ࡥࡵࡱࠧ―"), bstack1l111l_opy_ (u"ࠪ࠲ࡦࡧࡢࠨ‖"), bstack1l111l_opy_ (u"ࠫ࠳࡯ࡰࡢࠩ‗")]
bstack11l111ll_opy_ = [bstack1l111l_opy_ (u"ࠬ࡯ࡤࠨ‘"), bstack1l111l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ’"), bstack1l111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ‚"), bstack1l111l_opy_ (u"ࠨࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪࠧ‛")]
bstack111llll1l1_opy_ = {
  bstack1l111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ“"): bstack1l111l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ”"),
  bstack1l111l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ„"): bstack1l111l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ‟"),
  bstack1l111l_opy_ (u"࠭ࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ†"): bstack1l111l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ‡"),
  bstack1l111l_opy_ (u"ࠨ࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ•"): bstack1l111l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ‣"),
  bstack1l111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡹ࡯࡯࡯ࡵࠪ․"): bstack1l111l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ‥")
}
bstack1l11111111_opy_ = [
  bstack1l111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ…"),
  bstack1l111l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ‧"),
  bstack1l111l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ "),
  bstack1l111l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ "),
  bstack1l111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ‪"),
]
bstack1l1llll11l_opy_ = bstack11lll1l1ll_opy_ + bstack111111ll1ll_opy_ + bstack11llllll11_opy_
bstack1111ll1l1_opy_ = [
  bstack1l111l_opy_ (u"ࠪࡢࡱࡵࡣࡢ࡮࡫ࡳࡸࡺࠤࠨ‫"),
  bstack1l111l_opy_ (u"ࠫࡣࡨࡳ࠮࡮ࡲࡧࡦࡲ࠮ࡤࡱࡰࠨࠬ‬"),
  bstack1l111l_opy_ (u"ࠬࡤ࠱࠳࠹࠱ࠫ‭"),
  bstack1l111l_opy_ (u"࠭࡞࠲࠲࠱ࠫ‮"),
  bstack1l111l_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠷࡛࠷࠯࠼ࡡ࠳࠭ "),
  bstack1l111l_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠲࡜࠲࠰࠽ࡢ࠴ࠧ‰"),
  bstack1l111l_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠴࡝࠳࠱࠶ࡣ࠮ࠨ‱"),
  bstack1l111l_opy_ (u"ࠪࡢ࠶࠿࠲࠯࠳࠹࠼࠳࠭′")
]
bstack1111l11l111_opy_ = bstack1l111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ″")
bstack1llll11l11_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠱ࡹ࠵࠴࡫ࡶࡦࡰࡷࠫ‴")
bstack1l1l1l1ll1_opy_ = [ bstack1l111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ‵") ]
bstack1l111111_opy_ = [ bstack1l111l_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭‶") ]
bstack11ll11lll_opy_ = [bstack1l111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ‷")]
bstack11111l11ll_opy_ = [ bstack1l111l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ‸") ]
bstack1lll1l1l1_opy_ = bstack1l111l_opy_ (u"ࠪࡗࡉࡑࡓࡦࡶࡸࡴࠬ‹")
bstack11l1l1l11_opy_ = bstack1l111l_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠧ›")
bstack11ll1lll_opy_ = bstack1l111l_opy_ (u"࡙ࠬࡄࡌࡖࡨࡷࡹ࡙ࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠩ※")
bstack111lll1l1l_opy_ = bstack1l111l_opy_ (u"࠭࠴࠯࠲࠱࠴ࠬ‼")
bstack1l1ll11ll1_opy_ = [
  bstack1l111l_opy_ (u"ࠧࡆࡔࡕࡣࡋࡇࡉࡍࡇࡇࠫ‽"),
  bstack1l111l_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡉࡎࡇࡇࡣࡔ࡛ࡔࠨ‾"),
  bstack1l111l_opy_ (u"ࠩࡈࡖࡗࡥࡂࡍࡑࡆࡏࡊࡊ࡟ࡃ࡛ࡢࡇࡑࡏࡅࡏࡖࠪ‿"),
  bstack1l111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡇࡗ࡛ࡔࡘࡋࡠࡅࡋࡅࡓࡍࡅࡅࠩ⁀"),
  bstack1l111l_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐࡋࡔࡠࡐࡒࡘࡤࡉࡏࡏࡐࡈࡇ࡙ࡋࡄࠨ⁁"),
  bstack1l111l_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡃࡍࡑࡖࡉࡉ࠭⁂"),
  bstack1l111l_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡓࡇࡖࡉ࡙࠭⁃"),
  bstack1l111l_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡔࡈࡊ࡚࡙ࡅࡅࠩ⁄"),
  bstack1l111l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡄࡆࡔࡘࡔࡆࡆࠪ⁅"),
  bstack1l111l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ⁆"),
  bstack1l111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡔࡏࡕࡡࡕࡉࡘࡕࡌࡗࡇࡇࠫ⁇"),
  bstack1l111l_opy_ (u"ࠫࡊࡘࡒࡠࡃࡇࡈࡗࡋࡓࡔࡡࡌࡒ࡛ࡇࡌࡊࡆࠪ⁈"),
  bstack1l111l_opy_ (u"ࠬࡋࡒࡓࡡࡄࡈࡉࡘࡅࡔࡕࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨ⁉"),
  bstack1l111l_opy_ (u"࠭ࡅࡓࡔࡢࡘ࡚ࡔࡎࡆࡎࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ⁊"),
  bstack1l111l_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫ⁋"),
  bstack1l111l_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡖࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨ⁌"),
  bstack1l111l_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡗࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡋࡓࡘ࡚࡟ࡖࡐࡕࡉࡆࡉࡈࡂࡄࡏࡉࠬ⁍"),
  bstack1l111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡑࡔࡒ࡜࡞ࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ⁎"),
  bstack1l111l_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡎࡐࡖࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࠬ⁏"),
  bstack1l111l_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡓࡇࡖࡓࡑ࡛ࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫ⁐"),
  bstack1l111l_opy_ (u"࠭ࡅࡓࡔࡢࡑࡆࡔࡄࡂࡖࡒࡖ࡞ࡥࡐࡓࡑ࡛࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ⁑"),
]
bstack11ll1111l_opy_ = bstack1l111l_opy_ (u"ࠧ࠯࠱ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡣࡵࡸ࡮࡬ࡡࡤࡶࡶ࠳ࠬ⁒")
bstack1lll1ll111_opy_ = os.path.join(os.path.expanduser(bstack1l111l_opy_ (u"ࠨࢀࠪ⁓")), bstack1l111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⁔"), bstack1l111l_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩ⁕"))
bstack1111ll1111l_opy_ = bstack1l111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡳ࡭ࠬ⁖")
bstack11111l1l11l_opy_ = [ bstack1l111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⁗"), bstack1l111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ⁘"), bstack1l111l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭⁙"), bstack1l111l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ⁚")]
bstack111ll111_opy_ = [ bstack1l111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⁛"), bstack1l111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ⁜"), bstack1l111l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ⁝"), bstack1l111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ⁞"), bstack1l111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ ") ]
bstack1ll111llll_opy_ = [ bstack1l111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭⁠"), bstack1l111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ⁡") ]
bstack11111l1111l_opy_ = [ bstack1l111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⁢"), bstack1l111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ⁣") ]
bstack1l1ll1l11_opy_ = 360
bstack1111l111111_opy_ = bstack1l111l_opy_ (u"ࠦࡦࡶࡰ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦ⁤")
bstack11111l1l1ll_opy_ = bstack1l111l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡪࡵࡶࡹࡪࡹࠢ⁥")
bstack11111ll11l1_opy_ = bstack1l111l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡫ࡶࡷࡺ࡫ࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠤ⁦")
bstack1111l1l11l1_opy_ = bstack1l111l_opy_ (u"ࠢࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡶࡨࡷࡹࡹࠠࡢࡴࡨࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡰࡰࠣࡓࡘࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠦࡵࠣࡥࡳࡪࠠࡢࡤࡲࡺࡪࠦࡦࡰࡴࠣࡅࡳࡪࡲࡰ࡫ࡧࠤࡩ࡫ࡶࡪࡥࡨࡷ࠳ࠨ⁧")
bstack1111ll11111_opy_ = bstack1l111l_opy_ (u"ࠣ࠳࠴࠲࠵ࠨ⁨")
bstack1lll11ll1ll_opy_ = {
  bstack1l111l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ⁩"): bstack1l111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⁪"),
  bstack1l111l_opy_ (u"ࠫࡋࡇࡉࡍࠩ⁫"): bstack1l111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⁬"),
  bstack1l111l_opy_ (u"࠭ࡓࡌࡋࡓࠫ⁭"): bstack1l111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⁮")
}
bstack1lllllll11l_opy_ = [
  bstack1l111l_opy_ (u"ࠣࡩࡨࡸࠧ⁯"),
  bstack1l111l_opy_ (u"ࠤࡪࡳࡇࡧࡣ࡬ࠤ⁰"),
  bstack1l111l_opy_ (u"ࠥ࡫ࡴࡌ࡯ࡳࡹࡤࡶࡩࠨⁱ"),
  bstack1l111l_opy_ (u"ࠦࡷ࡫ࡦࡳࡧࡶ࡬ࠧ⁲"),
  bstack1l111l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦ⁳"),
  bstack1l111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ⁴"),
  bstack1l111l_opy_ (u"ࠢࡴࡷࡥࡱ࡮ࡺࡅ࡭ࡧࡰࡩࡳࡺࠢ⁵"),
  bstack1l111l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ⁶"),
  bstack1l111l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧ⁷"),
  bstack1l111l_opy_ (u"ࠥࡧࡱ࡫ࡡࡳࡇ࡯ࡩࡲ࡫࡮ࡵࠤ⁸"),
  bstack1l111l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࡷࠧ⁹"),
  bstack1l111l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠧ⁺"),
  bstack1l111l_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡁࡴࡻࡱࡧࡘࡩࡲࡪࡲࡷࠦ⁻"),
  bstack1l111l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨ⁼"),
  bstack1l111l_opy_ (u"ࠣࡳࡸ࡭ࡹࠨ⁽"),
  bstack1l111l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡗࡳࡺࡩࡨࡂࡥࡷ࡭ࡴࡴࠢ⁾"),
  bstack1l111l_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡑࡺࡲࡴࡪࡖࡲࡹࡨ࡮ࠢⁿ"),
  bstack1l111l_opy_ (u"ࠦࡸ࡮ࡡ࡬ࡧࠥ₀"),
  bstack1l111l_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࡅࡵࡶࠢ₁")
]
bstack11111l11111_opy_ = [
  bstack1l111l_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧ₂"),
  bstack1l111l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ₃"),
  bstack1l111l_opy_ (u"ࠣࡣࡸࡸࡴࠨ₄"),
  bstack1l111l_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤ₅"),
  bstack1l111l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ₆")
]
bstack111l111ll1_opy_ = {
  bstack1l111l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥ₇"): [bstack1l111l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦ₈")],
  bstack1l111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ₉"): [bstack1l111l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ₊")],
  bstack1l111l_opy_ (u"ࠣࡣࡸࡸࡴࠨ₋"): [bstack1l111l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨ₌"), bstack1l111l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨ₍"), bstack1l111l_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣ₎"), bstack1l111l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦ₏")],
  bstack1l111l_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨₐ"): [bstack1l111l_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢₑ")],
  bstack1l111l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥₒ"): [bstack1l111l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦₓ")],
}
bstack1111111lll1_opy_ = {
  bstack1l111l_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤₔ"): bstack1l111l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥₕ"),
  bstack1l111l_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤₖ"): bstack1l111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥₗ"),
  bstack1l111l_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦₘ"): bstack1l111l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࠥₙ"),
  bstack1l111l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧₚ"): bstack1l111l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧₛ"),
  bstack1l111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨₜ"): bstack1l111l_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ₝")
}
bstack1lll1l1ll11_opy_ = {
  bstack1l111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ₞"): bstack1l111l_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࠦࡓࡦࡶࡸࡴࠬ₟"),
  bstack1l111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ₠"): bstack1l111l_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡖࡨࡥࡷࡪ࡯ࡸࡰࠪ₡"),
  bstack1l111l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ₢"): bstack1l111l_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡖࡩࡹࡻࡰࠨ₣"),
  bstack1l111l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ₤"): bstack1l111l_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭₥")
}
bstack111111ll11l_opy_ = 65536
bstack111111l11ll_opy_ = bstack1l111l_opy_ (u"ࠧ࠯࠰࠱࡟࡙ࡘࡕࡏࡅࡄࡘࡊࡊ࡝ࠨ₦")
bstack111111l1l1l_opy_ = [
      bstack1l111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ₧"), bstack1l111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ₨"), bstack1l111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭₩"), bstack1l111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ₪"), bstack1l111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧ₫"),
      bstack1l111l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ€"), bstack1l111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ₭"), bstack1l111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ₮"), bstack1l111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪ₯"),
      bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ₰"), bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭₱"), bstack1l111l_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨ₲")
    ]
bstack11111l111ll_opy_= {
  bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ₳"): bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ₴"),
  bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ₵"): bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭₶"),
  bstack1l111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ₷"): bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ₸"),
  bstack1l111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ₹"): bstack1l111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭₺"),
  bstack1l111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ₻"): bstack1l111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ₼"),
  bstack1l111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ₽"): bstack1l111l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ₾"),
  bstack1l111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ₿"): bstack1l111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⃀"),
  bstack1l111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⃁"): bstack1l111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⃂"),
  bstack1l111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⃃"): bstack1l111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⃄"),
  bstack1l111l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ⃅"): bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⃆"),
  bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⃇"): bstack1l111l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⃈"),
  bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧ⃉"): bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨ⃊"),
  bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⃋"): bstack1l111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⃌"),
  bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫ⃍"): bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࡔࡶࡴࡪࡱࡱࡷࠬ⃎"),
  bstack1l111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ⃏"): bstack1l111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩ⃐"),
  bstack1l111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⃑"): bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ⃒ࠫ"),
  bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ⃓ࠬ"): bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⃔"),
  bstack1l111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩ⃕"): bstack1l111l_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪ⃖"),
  bstack1l111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⃗"): bstack1l111l_opy_ (u"ࠨࡲࡨࡶࡨࡿ⃘ࠧ"),
  bstack1l111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⃙"): bstack1l111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴ⃚ࠩ"),
  bstack1l111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ⃛"): bstack1l111l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨ⃜"),
  bstack1l111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ⃝"): bstack1l111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ⃞"),
  bstack1l111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃟"): bstack1l111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⃠"),
  bstack1l111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ⃡"): bstack1l111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ⃢"),
  bstack1l111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⃣"): bstack1l111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⃤"),
  bstack1l111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶ⃥ࠫ"): bstack1l111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷ⃦ࠬ"),
  bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭⃧"): bstack1l111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹ⃨ࠧ"),
  bstack1l111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ⃩"): bstack1l111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷ⃪ࠬ")
}
bstack11111l1l1l1_opy_ = [bstack1l111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ⃫࠭"), bstack1l111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ⃬࠭")]
bstack111lll1ll1_opy_ = (bstack1l111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ⃭ࠣ"),)
bstack1111111ll1l_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡸࡴࡩࡧࡴࡦࡡࡦࡰ࡮⃮࠭")
bstack11l11ll11l_opy_ = bstack1l111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡧࡳ࡫ࡧࡷ࠴ࠨ⃯")
bstack111111l1ll_opy_ = bstack1l111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡲࡪࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡢࡵ࡫ࡦࡴࡧࡲࡥ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࠥ⃰")
bstack11ll11ll1l_opy_ = bstack1l111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳࠨ⃱")
class EVENTS(Enum):
  bstack11111l1lll1_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪ⃲")
  bstack1111ll11l1_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡥࡢࡰࡸࡴࠬ⃳")
  bstack1l1lllll11_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿࡬ࡩ࡯ࡣ࡯࡭ࡿ࡫ࠧ⃴")
  bstack11111l111l1_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡰࡧࡰࡴ࡭ࡳࠨ⃵")
  bstack11l11l1ll_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭⃶") #shift post bstack11111l1l111_opy_
  bstack111l11l1l_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬ⃷") #shift post bstack11111l1l111_opy_
  bstack11111l11l11_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡨࡶࡤࠪ⃸") #shift
  bstack111111ll1l1_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡧࡳࡼࡴ࡬ࡰࡣࡧࠫ⃹") #shift
  bstack1l11l1lll1_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠻ࡪࡸࡦ࠲ࡳࡡ࡯ࡣࡪࡩࡲ࡫࡮ࡵࠩ⃺")
  bstack1l111ll111l_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡷࡦࡼࡥ࠮ࡴࡨࡷࡺࡲࡴࡴࠩ⃻")
  bstack1ll111l1l1_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡵ࡫ࡲࡧࡱࡵࡱࡸࡩࡡ࡯ࠩ⃼")
  bstack1lll1111ll_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡯ࡳࡨࡧ࡬ࠨ⃽") #shift
  bstack11l1ll1l_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡢࡲࡳ࠱ࡺࡶ࡬ࡰࡣࡧࠫ⃾") #shift
  bstack111l1111l1_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡨ࡯࠭ࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠪ⃿")
  bstack1l111lll1l_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧ℀") #shift
  bstack1l1lll1lll_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡪࡩࡹ࠳ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠳ࡲࡦࡵࡸࡰࡹࡹࠧ℁") #shift
  bstack111111l1l11_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼࠫℂ") #shift
  bstack11ll1111111_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ℃")
  bstack1lllll1lll_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡶࡩࡸࡹࡩࡰࡰ࠰ࡷࡹࡧࡴࡶࡵࠪ℄") #shift
  bstack1lll11l1_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽࡬ࡺࡨ࠭࡮ࡣࡱࡥ࡬࡫࡭ࡦࡰࡷࠫ℅")
  bstack11111l11l1l_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡴࡾࡹ࠮ࡵࡨࡸࡺࡶࠧ℆") #shift
  bstack111l1111ll_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡺࡵࡱࠩℇ")
  bstack11111l1ll11_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡷࡳࡧࡰࡴࡪࡲࡸࠬ℈") # not bstack1111111l1l1_opy_ in python
  bstack111l11ll_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡷࡵࡪࡶࠪ℉") # used in bstack111111lll11_opy_
  bstack111l1l1llll_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡳࡧ࠰ࡵࡺ࡯ࡴࠨℊ")
  bstack111l1ll1111_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲ࡷࡵࡪࡶࠪℋ")
  bstack1l1lll1ll1_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡩࡨࡸࠬℌ") # used in bstack111111lll11_opy_
  bstack11l1l1l11l_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼࡫ࡳࡴࡱࠧℍ")
  bstack111ll111l1l_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷ࡫࠭ࡩࡱࡲ࡯ࠬℎ")
  bstack111ll111ll1_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡵࡳࡵ࠯࡫ࡳࡴࡱࠧℏ")
  bstack111l1ll111_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪ࠭ℐ")
  bstack1l1l11lll_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳ࠭ℑ") #
  bstack1lll1111_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡰ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡺࡡ࡬ࡧࡖࡧࡷ࡫ࡥ࡯ࡕ࡫ࡳࡹ࠭ℒ")
  bstack11l1l111_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡢࡷࡷࡳ࠲ࡩࡡࡱࡶࡸࡶࡪ࠭ℓ")
  bstack1l1ll11l_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡴࡦࡵࡷࠫ℔")
  bstack11l1l1l111_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡶࡨࡷࡹ࠭ℕ")
  bstack1lll1ll11l_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡸࡥ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ№") #shift
  bstack1l1l1l11l_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫ℗") #shift
  bstack111111l1lll_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬ℘")
  bstack11111l11ll1_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡬ࡨࡱ࡫࠭ࡵ࡫ࡰࡩࡴࡻࡴࠨℙ")
  bstack1l11l1l11_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡧࡻ࡭ࡹ࠳ࡨࡢࡰࡧࡰࡪࡸࠧℚ")
  bstack1l11l1111l1_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡥࡹ࡫ࡷ࠱࡭ࡧ࡮ࡥ࡮ࡨࡶࠬℛ")
  bstack111111l1ll1_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡴࡤ࠮࡯ࡨࡸࡷ࡯ࡣࡴࠩℜ")
  bstack11111ll1111_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡪࡸࡦ࠿ࡹࡴࡰࡲࠪℝ")
  bstack1l11ll1l1l1_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡶࡸࡦࡸࡴࠨ℞")
  bstack111111ll111_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡨࡴࡽ࡮࡭ࡱࡤࡨࠬ℟")
  bstack11111l11lll_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡨ࡮ࡥࡤ࡭࠰ࡹࡵࡪࡡࡵࡧࠪ℠")
  bstack1l11lll111l_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡤࡲࡳࡹࡹࡴࡳࡣࡳࠫ℡")
  bstack1l1l1ll1l11_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡶࡸࡦࡸࡴࡣ࡫ࡱࡥࡷࡿࠧ™")
  bstack1l1l1l1ll1l_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡧࡴࡴ࡮ࡦࡥࡷࠫ℣")
  bstack1l111llll11_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡸࡺ࡯ࡱࠩℤ")
  bstack1l11lll11ll_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠧ℥")
  bstack1l1l11ll1l1_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡣࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰࠪΩ")
  bstack111111l1111_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠫ℧")
  bstack11111l1llll_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡨ࡬ࡲࡩࡔࡥࡢࡴࡨࡷࡹࡎࡵࡣࠩℨ")
  bstack11l1l111ll1_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡊࡰ࡬ࡸࠬ℩")
  bstack11l1l111111_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡷࡺࠧK")
  bstack11llllll111_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪÅ")
  bstack111111l111l_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡈࡵ࡮ࡧ࡫ࡪࠫℬ")
  bstack11llll1ll1l_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡖࡸࡪࡶࠧℭ")
  bstack11llll1l1ll_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࡫ࡖࡩࡱ࡬ࡈࡦࡣ࡯ࡋࡪࡺࡒࡦࡵࡸࡰࡹ࠭℮")
  bstack11ll1l1ll1l_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡆࡸࡨࡲࡹ࠭ℯ")
  bstack11lll1111ll_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠬℰ")
  bstack11ll111lll1_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺࡭ࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࡉࡻ࡫࡮ࡵࠩℱ")
  bstack111111lllll_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡧࡱࡵࡺ࡫ࡵࡦࡖࡨࡷࡹࡋࡶࡦࡰࡷࠫℲ")
  bstack11l11ll111l_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡵࡰࠨℳ")
  bstack1l1l1l1ll11_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀ࡯࡯ࡕࡷࡳࡵ࠭ℴ")
  bstack111l11111l1_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮ࡨࡥࡳࡻࡰࡖࡲ࡯ࡳࡦࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠫℵ")
  bstack11llll1ll1_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡌࡵ࡯ࡰࡨࡰ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠫℶ")
  bstack11l11111l_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪࡆࡶࡰࡱࡩࡱ࡚ࡥࡴࡶࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࠬℷ")
  bstack1ll11ll1l1l_opy_ = bstack1l111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡵࡶ࡬ࡺࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡑࡻࡷࡩࡸࡺࠧℸ")
  bstack1lllll111l1_opy_ = bstack1l111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡶࡰ࡭ࡻࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡄࡨ࡬ࡦࡼࡥࠨℹ")
  bstack1ll11l11l11_opy_ = bstack1l111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡵࡓࡽࡹ࡫ࡳࡵࠩ℺")
  bstack1ll11lll111_opy_ = bstack1l111l_opy_ (u"ࠩࡶࡨࡰࡀࡰࡺࡶࡨࡷࡹࡍࡥࡵࡖࡲࡸࡦࡲࡔࡦࡵࡷࡷࠬ℻")
class STAGE(Enum):
  bstack11111ll1l1_opy_ = bstack1l111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩℼ")
  END = bstack1l111l_opy_ (u"ࠫࡪࡴࡤࠨℽ")
  bstack1l11llll1_opy_ = bstack1l111l_opy_ (u"ࠬࡹࡩ࡯ࡩ࡯ࡩࠬℾ")
bstack1111111l1_opy_ = {
  bstack1l111l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭ℿ"): bstack1l111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⅀"),
  bstack1l111l_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬ⅁"): bstack1l111l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ⅂"),
  bstack1l111l_opy_ (u"ࠪࡆࡊࡎࡁࡗࡇࠪ⅃"): bstack1l111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ⅄")
}
PLAYWRIGHT_HUB_URL = bstack1l111l_opy_ (u"ࠧࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠢⅅ")
bstack1ll1111l1_opy_ = {bstack1l111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ⅆ"), bstack1l111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩⅇ"), bstack1l111l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩࡨࡳࡱࡰ࡭ࡺࡳࠧⅈ")}
MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION = 98
bstack1l11111l111_opy_ = 100
bstack1ll1111l1_opy_ = (bstack1l111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩⅉ"), bstack1l111l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩ⅊"), bstack1l111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠭⅋"))
bstack1ll11l1l1l1_opy_ = {
  bstack1l111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫ⅌"): bstack1l111l_opy_ (u"࠭࠭࠮ࡴࡨࡶࡺࡴࡳࠨ⅍"),
  bstack1l111l_opy_ (u"ࠧࡥࡧ࡯ࡥࡾ࠭ⅎ"): bstack1l111l_opy_ (u"ࠨ࠯࠰ࡶࡪࡸࡵ࡯ࡵ࠰ࡨࡪࡲࡡࡺࠩ⅏"),
  bstack1l111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧ⅐"): 0
}
bstack111111llll1_opy_ = bstack1l111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥ⅑")
bstack111111l11l1_opy_ = bstack1l111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣ⅒")
bstack11l111ll1_opy_ = bstack1l111l_opy_ (u"࡚ࠧࡅࡔࡖࠣࡖࡊࡖࡏࡓࡖࡌࡒࡌࠦࡁࡏࡆࠣࡅࡓࡇࡌ࡚ࡖࡌࡇࡘࠨ⅓")