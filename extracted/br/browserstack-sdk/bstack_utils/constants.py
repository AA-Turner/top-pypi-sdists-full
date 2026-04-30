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
import os
import re
from enum import Enum
bstack1lllll1lll_opy_ = {
  bstack1l1111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᷪ"): bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࠬᷫ"),
  bstack1l1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᷬ"): bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡮ࡩࡾ࠭ᷭ"),
  bstack1l1111l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᷮ"): bstack1l1111l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᷯ"),
  bstack1l1111l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᷰ"): bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧᷱ"),
  bstack1l1111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᷲ"): bstack1l1111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࠪᷳ"),
  bstack1l1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᷴ"): bstack1l1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪ᷵"),
  bstack1l1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᷶"): bstack1l1111l_opy_ (u"࠭࡮ࡢ࡯ࡨ᷷ࠫ"),
  bstack1l1111l_opy_ (u"ࠧࡥࡧࡥࡹ࡬᷸࠭"): bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬᷹࠭"),
  bstack1l1111l_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹ᷺ࠧ"): bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡳࡹ࡯࡭ࡧࠪ᷻"),
  bstack1l1111l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩ᷼"): bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴ᷽ࠩ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪ᷾"): bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵ᷿ࠪ"),
  bstack1l1111l_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧḀ"): bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡸ࡬ࡨࡪࡵࠧḁ"),
  bstack1l1111l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩḂ"): bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩḃ"),
  bstack1l1111l_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬḄ"): bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬḅ"),
  bstack1l1111l_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬḆ"): bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬḇ"),
  bstack1l1111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫḈ"): bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫḉ"),
  bstack1l1111l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ḋ"): bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧḋ"),
  bstack1l1111l_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬḌ"): bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬḍ"),
  bstack1l1111l_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭Ḏ"): bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ḏ"),
  bstack1l1111l_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪḐ"): bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪḑ"),
  bstack1l1111l_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧḒ"): bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡯ࡦࡎࡩࡾࡹࠧḓ"),
  bstack1l1111l_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩḔ"): bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳ࡜ࡧࡩࡵࠩḕ"),
  bstack1l1111l_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨḖ"): bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡳࠨḗ"),
  bstack1l1111l_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬḘ"): bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧ࡬ࡣࡢࡥ࡫ࡩࠬḙ"),
  bstack1l1111l_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧḚ"): bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧḛ"),
  bstack1l1111l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫḜ"): bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫḝ"),
  bstack1l1111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧḞ"): bstack1l1111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫḟ"),
  bstack1l1111l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩḠ"): bstack1l1111l_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫḡ"),
  bstack1l1111l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧḢ"): bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨḣ"),
  bstack1l1111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩḤ"): bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩḥ"),
  bstack1l1111l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬḦ"): bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬḧ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬḨ"): bstack1l1111l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨḩ"),
  bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪḪ"): bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪḫ"),
  bstack1l1111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪḬ"): bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡴࡻࡲࡤࡧࠪḭ"),
  bstack1l1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧḮ"): bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧḯ"),
  bstack1l1111l_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩḰ"): bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡓࡧ࡭ࡦࠩḱ"),
  bstack1l1111l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬḲ"): bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬḳ"),
  bstack1l1111l_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨḴ"): bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨḵ"),
  bstack1l1111l_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫḶ"): bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫḷ"),
  bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫḸ"): bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫḹ"),
  bstack1l1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬḺ"): bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬḻ")
}
bstack11111l1lll1_opy_ = [
  bstack1l1111l_opy_ (u"ࠬࡵࡳࠨḼ"),
  bstack1l1111l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩḽ"),
  bstack1l1111l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩḾ"),
  bstack1l1111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ḿ"),
  bstack1l1111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭Ṁ"),
  bstack1l1111l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧṁ"),
  bstack1l1111l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫṂ"),
]
bstack111ll1l11l_opy_ = {
  bstack1l1111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧṃ"): [bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧṄ"), bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡓࡇࡍࡆࠩṅ")],
  bstack1l1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫṆ"): bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬṇ"),
  bstack1l1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭Ṉ"): bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠧṉ"),
  bstack1l1111l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪṊ"): bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠫṋ"),
  bstack1l1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩṌ"): bstack1l1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪṍ"),
  bstack1l1111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩṎ"): bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡗࡤࡖࡅࡓࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫṏ"),
  bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨṐ"): bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࠪṑ"),
  bstack1l1111l_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪṒ"): bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫṓ"),
  bstack1l1111l_opy_ (u"ࠨࡣࡳࡴࠬṔ"): [bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡓࡔࡤࡏࡄࠨṕ"), bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕ࠭Ṗ")],
  bstack1l1111l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ṗ"): bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡎࡒࡋࡑࡋࡖࡆࡎࠪṘ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪṙ"): bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪṚ"),
  bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬṛ"): [bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞࠭Ṝ"), bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪṝ")],
  bstack1l1111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨṞ"): bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙࡛ࡒࡃࡑࡖࡇࡆࡒࡅࠨṟ"),
  bstack1l1111l_opy_ (u"࠭ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࡆࡐ࡙ࠫṠ"): bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡏࡓࡅࡋࡉࡘ࡚ࡒࡂࡖࡌࡓࡓࡥࡓࡎࡃࡕࡘࡤ࡙ࡅࡍࡇࡆࡘࡎࡕࡎࡠࡈࡈࡅ࡙࡛ࡒࡆࡡࡅࡖࡆࡔࡃࡉࡇࡖࠫṡ")
}
bstack11l1llll_opy_ = {
  bstack1l1111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪṢ"): [bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫṣ"), bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫṤ")],
  bstack1l1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧṥ"): [bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡣࡰ࡫ࡹࠨṦ"), bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨṧ")],
  bstack1l1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪṨ"): bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪṩ"),
  bstack1l1111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧṪ"): bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧṫ"),
  bstack1l1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ṭ"): bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ṭ"),
  bstack1l1111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭Ṯ"): [bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡱࡲࠪṯ"), bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧṰ")],
  bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ṱ"): bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨṲ"),
  bstack1l1111l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨṳ"): bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨṴ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡱࡲࠪṵ"): bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲࠪṶ"),
  bstack1l1111l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪṷ"): bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪṸ"),
  bstack1l1111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧṹ"): bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧṺ"),
  bstack1l1111l_opy_ (u"ࠧࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡃࡍࡋࠥṻ"): bstack1l1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࠦṼ"),
}
bstack1l1l1lll1l_opy_ = {
  bstack1l1111l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪṽ"): bstack1l1111l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬṾ"),
  bstack1l1111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫṿ"): [bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬẀ"), bstack1l1111l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧẁ")],
  bstack1l1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪẂ"): bstack1l1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫẃ"),
  bstack1l1111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫẄ"): bstack1l1111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨẅ"),
  bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧẆ"): [bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫẇ"), bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪẈ")],
  bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ẉ"): bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨẊ"),
  bstack1l1111l_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫẋ"): bstack1l1111l_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭Ẍ"),
  bstack1l1111l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩẍ"): [bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪẎ"), bstack1l1111l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬẏ")],
  bstack1l1111l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫẐ"): [bstack1l1111l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧẑ"), bstack1l1111l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࠧẒ")]
}
bstack1l11l1l1l1_opy_ = [
  bstack1l1111l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧẓ"),
  bstack1l1111l_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬẔ"),
  bstack1l1111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩẕ"),
  bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡴࡘ࡫ࡱࡨࡴࡽࡒࡦࡥࡷࠫẖ"),
  bstack1l1111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧẗ"),
  bstack1l1111l_opy_ (u"࠭ࡳࡵࡴ࡬ࡧࡹࡌࡩ࡭ࡧࡌࡲࡹ࡫ࡲࡢࡥࡷࡥࡧ࡯࡬ࡪࡶࡼࠫẘ"),
  bstack1l1111l_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪẙ"),
  bstack1l1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ẚ"),
  bstack1l1111l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧẛ"),
  bstack1l1111l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫẜ"),
  bstack1l1111l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪẝ"),
  bstack1l1111l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ẞ"),
]
bstack1ll1l1l1_opy_ = [
  bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪẟ"),
  bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫẠ"),
  bstack1l1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧạ"),
  bstack1l1111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩẢ"),
  bstack1l1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ả"),
  bstack1l1111l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭Ấ"),
  bstack1l1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨấ"),
  bstack1l1111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪẦ"),
  bstack1l1111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪầ"),
  bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭Ẩ"),
  bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ẩ"),
  bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪẪ"),
  bstack1l1111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ẫ"),
  bstack1l1111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡙ࡧࡧࠨẬ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪậ"),
  bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩẮ"),
  bstack1l1111l_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬắ"),
  bstack1l1111l_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠱ࠨẰ"),
  bstack1l1111l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠳ࠩằ"),
  bstack1l1111l_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠵ࠪẲ"),
  bstack1l1111l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠷ࠫẳ"),
  bstack1l1111l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠹ࠬẴ"),
  bstack1l1111l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠻࠭ẵ"),
  bstack1l1111l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠽ࠧẶ"),
  bstack1l1111l_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠸ࠨặ"),
  bstack1l1111l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠺ࠩẸ"),
  bstack1l1111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪẹ"),
  bstack1l1111l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫẺ"),
  bstack1l1111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩẻ"),
  bstack1l1111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩẼ"),
  bstack1l1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬẽ"),
  bstack1l1111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭Ế"),
  bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧế"),
  bstack1l1111l_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧỀ")
]
bstack11111l1l11l_opy_ = [
  bstack1l1111l_opy_ (u"ࠬࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪề"),
  bstack1l1111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨỂ"),
  bstack1l1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪể"),
  bstack1l1111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ễ"),
  bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡐࡳ࡫ࡲࡶ࡮ࡺࡹࠨễ"),
  bstack1l1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭Ệ"),
  bstack1l1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡥ࡬࠭ệ"),
  bstack1l1111l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪỈ"),
  bstack1l1111l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨỉ"),
  bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬỊ"),
  bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩị"),
  bstack1l1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨỌ"),
  bstack1l1111l_opy_ (u"ࠪࡳࡸ࠭ọ"),
  bstack1l1111l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧỎ"),
  bstack1l1111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫỏ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨỐ"),
  bstack1l1111l_opy_ (u"ࠧࡳࡧࡪ࡭ࡴࡴࠧố"),
  bstack1l1111l_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪỒ"),
  bstack1l1111l_opy_ (u"ࠩࡰࡥࡨ࡮ࡩ࡯ࡧࠪồ"),
  bstack1l1111l_opy_ (u"ࠪࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠧỔ"),
  bstack1l1111l_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩổ"),
  bstack1l1111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩỖ"),
  bstack1l1111l_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬỗ"),
  bstack1l1111l_opy_ (u"ࠧ࡯ࡱࡓࡥ࡬࡫ࡌࡰࡣࡧࡘ࡮ࡳࡥࡰࡷࡷࠫỘ"),
  bstack1l1111l_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩộ"),
  bstack1l1111l_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨỚ"),
  bstack1l1111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧớ"),
  bstack1l1111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡪࡴࡤࡌࡧࡼࡷࠬỜ"),
  bstack1l1111l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩờ"),
  bstack1l1111l_opy_ (u"࠭࡮ࡰࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠪỞ"),
  bstack1l1111l_opy_ (u"ࠧࡤࡪࡨࡧࡰ࡛ࡒࡍࠩở"),
  bstack1l1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪỠ"),
  bstack1l1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡅࡲࡳࡰ࡯ࡥࡴࠩỡ"),
  bstack1l1111l_opy_ (u"ࠪࡧࡦࡶࡴࡶࡴࡨࡇࡷࡧࡳࡩࠩỢ"),
  bstack1l1111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨợ"),
  bstack1l1111l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬỤ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࡙ࡩࡷࡹࡩࡰࡰࠪụ"),
  bstack1l1111l_opy_ (u"ࠧ࡯ࡱࡅࡰࡦࡴ࡫ࡑࡱ࡯ࡰ࡮ࡴࡧࠨỦ"),
  bstack1l1111l_opy_ (u"ࠨ࡯ࡤࡷࡰ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧủ"),
  bstack1l1111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡎࡲ࡫ࡸ࠭Ứ"),
  bstack1l1111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡌࡨࠬứ"),
  bstack1l1111l_opy_ (u"ࠫࡩ࡫ࡤࡪࡥࡤࡸࡪࡪࡄࡦࡸ࡬ࡧࡪ࠭Ừ"),
  bstack1l1111l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡕࡧࡲࡢ࡯ࡶࠫừ"),
  bstack1l1111l_opy_ (u"࠭ࡰࡩࡱࡱࡩࡓࡻ࡭ࡣࡧࡵࠫỬ"),
  bstack1l1111l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬử"),
  bstack1l1111l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡕࡰࡵ࡫ࡲࡲࡸ࠭Ữ"),
  bstack1l1111l_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧữ"),
  bstack1l1111l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪỰ"),
  bstack1l1111l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨự"),
  bstack1l1111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡇ࡯࡯࡮ࡧࡷࡶ࡮ࡩࠧỲ"),
  bstack1l1111l_opy_ (u"࠭ࡶࡪࡦࡨࡳ࡛࠸ࠧỳ"),
  bstack1l1111l_opy_ (u"ࠧ࡮࡫ࡧࡗࡪࡹࡳࡪࡱࡱࡍࡳࡹࡴࡢ࡮࡯ࡅࡵࡶࡳࠨỴ"),
  bstack1l1111l_opy_ (u"ࠨࡧࡶࡴࡷ࡫ࡳࡴࡱࡖࡩࡷࡼࡥࡳࠩỵ"),
  bstack1l1111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨỶ"),
  bstack1l1111l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡈࡪࡰࠨỷ"),
  bstack1l1111l_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫỸ"),
  bstack1l1111l_opy_ (u"ࠬࡹࡹ࡯ࡥࡗ࡭ࡲ࡫ࡗࡪࡶ࡫ࡒ࡙ࡖࠧỹ"),
  bstack1l1111l_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫỺ"),
  bstack1l1111l_opy_ (u"ࠧࡨࡲࡶࡐࡴࡩࡡࡵ࡫ࡲࡲࠬỻ"),
  bstack1l1111l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩỼ"),
  bstack1l1111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩỽ"),
  bstack1l1111l_opy_ (u"ࠪࡪࡴࡸࡣࡦࡅ࡫ࡥࡳ࡭ࡥࡋࡣࡵࠫỾ"),
  bstack1l1111l_opy_ (u"ࠫࡽࡳࡳࡋࡣࡵࠫỿ"),
  bstack1l1111l_opy_ (u"ࠬࡾ࡭ࡹࡌࡤࡶࠬἀ"),
  bstack1l1111l_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬἁ"),
  bstack1l1111l_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧἂ"),
  bstack1l1111l_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩἃ"),
  bstack1l1111l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬἄ"),
  bstack1l1111l_opy_ (u"ࠪࡥࡵࡶࡖࡦࡴࡶ࡭ࡴࡴࠧἅ"),
  bstack1l1111l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪἆ"),
  bstack1l1111l_opy_ (u"ࠬࡸࡥࡴ࡫ࡪࡲࡆࡶࡰࠨἇ"),
  bstack1l1111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯࡫ࡰࡥࡹ࡯࡯࡯ࡵࠪἈ"),
  bstack1l1111l_opy_ (u"ࠧࡤࡣࡱࡥࡷࡿࠧἉ"),
  bstack1l1111l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩἊ"),
  bstack1l1111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩἋ"),
  bstack1l1111l_opy_ (u"ࠪ࡭ࡪ࠭Ἄ"),
  bstack1l1111l_opy_ (u"ࠫࡪࡪࡧࡦࠩἍ"),
  bstack1l1111l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬἎ"),
  bstack1l1111l_opy_ (u"࠭ࡱࡶࡧࡸࡩࠬἏ"),
  bstack1l1111l_opy_ (u"ࠧࡪࡰࡷࡩࡷࡴࡡ࡭ࠩἐ"),
  bstack1l1111l_opy_ (u"ࠨࡣࡳࡴࡘࡺ࡯ࡳࡧࡆࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠩἑ"),
  bstack1l1111l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡅࡤࡱࡪࡸࡡࡊ࡯ࡤ࡫ࡪࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨἒ"),
  bstack1l1111l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡆࡺࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭ἓ"),
  bstack1l1111l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡋࡱࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧἔ"),
  bstack1l1111l_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࠩἕ"),
  bstack1l1111l_opy_ (u"࠭ࡲࡦࡵࡨࡶࡻ࡫ࡄࡦࡸ࡬ࡧࡪ࠭἖"),
  bstack1l1111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ἗"),
  bstack1l1111l_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪἘ"),
  bstack1l1111l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡤࡷࡸࡩ࡯ࡥࡧࠪἙ"),
  bstack1l1111l_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡌࡳࡸࡊࡥࡷ࡫ࡦࡩࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭Ἒ"),
  bstack1l1111l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡺࡪࡩࡰࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫἛ"),
  bstack1l1111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡶࡰ࡭ࡧࡓࡥࡾ࠭Ἔ"),
  bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧἝ"),
  bstack1l1111l_opy_ (u"ࠧࡸࡦ࡬ࡳࡘ࡫ࡲࡷ࡫ࡦࡩࠬ἞"),
  bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ἟"),
  bstack1l1111l_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶࡆࡶࡴࡹࡳࡔ࡫ࡷࡩ࡙ࡸࡡࡤ࡭࡬ࡲ࡬࠭ἠ"),
  bstack1l1111l_opy_ (u"ࠪ࡬࡮࡭ࡨࡄࡱࡱࡸࡷࡧࡳࡵࠩἡ"),
  bstack1l1111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡔࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࡳࠨἢ"),
  bstack1l1111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨἣ"),
  bstack1l1111l_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪἤ"),
  bstack1l1111l_opy_ (u"ࠧࡳࡧࡰࡳࡻ࡫ࡉࡐࡕࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࡌࡰࡥࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬἥ"),
  bstack1l1111l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪἦ"),
  bstack1l1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫἧ"),
  bstack1l1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬἨ"),
  bstack1l1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪἩ"),
  bstack1l1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧἪ"),
  bstack1l1111l_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩἫ"),
  bstack1l1111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭Ἤ"),
  bstack1l1111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪἭ"),
  bstack1l1111l_opy_ (u"ࠩࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡕࡸ࡯࡮ࡲࡷࡆࡪ࡮ࡡࡷ࡫ࡲࡶࠬἮ")
]
bstack1ll1l11lll_opy_ = {
  bstack1l1111l_opy_ (u"ࠪࡺࠬἯ"): bstack1l1111l_opy_ (u"ࠫࡻ࠭ἰ"),
  bstack1l1111l_opy_ (u"ࠬ࡬ࠧἱ"): bstack1l1111l_opy_ (u"࠭ࡦࠨἲ"),
  bstack1l1111l_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭ἳ"): bstack1l1111l_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧἴ"),
  bstack1l1111l_opy_ (u"ࠩࡲࡲࡱࡿࡡࡶࡶࡲࡱࡦࡺࡥࠨἵ"): bstack1l1111l_opy_ (u"ࠪࡳࡳࡲࡹࡂࡷࡷࡳࡲࡧࡴࡦࠩἶ"),
  bstack1l1111l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨἷ"): bstack1l1111l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩἸ"),
  bstack1l1111l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩἹ"): bstack1l1111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪἺ"),
  bstack1l1111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡰࡴࡷࠫἻ"): bstack1l1111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬἼ"),
  bstack1l1111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭Ἵ"): bstack1l1111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧἾ"),
  bstack1l1111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨἿ"): bstack1l1111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩὀ"),
  bstack1l1111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨὁ"): bstack1l1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡍࡵࡳࡵࠩὂ"),
  bstack1l1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪὃ"): bstack1l1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫὄ"),
  bstack1l1111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬὅ"): bstack1l1111l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧ὆"),
  bstack1l1111l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨ὇"): bstack1l1111l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩὈ"),
  bstack1l1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩὉ"): bstack1l1111l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫὊ"),
  bstack1l1111l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬὋ"): bstack1l1111l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭Ὄ"),
  bstack1l1111l_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩὍ"): bstack1l1111l_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪࠪ὎"),
  bstack1l1111l_opy_ (u"ࠧࡱࡣࡦࡪ࡮ࡲࡥࠨ὏"): bstack1l1111l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫὐ"),
  bstack1l1111l_opy_ (u"ࠩࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫὑ"): bstack1l1111l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ὒ"),
  bstack1l1111l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧὓ"): bstack1l1111l_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨὔ"),
  bstack1l1111l_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧὕ"): bstack1l1111l_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨὖ"),
  bstack1l1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪὗ"): bstack1l1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ὘"),
  bstack1l1111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬὙ"): bstack1l1111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡶࡥࡢࡶࡨࡶࠬ὚")
}
bstack111111l111l_opy_ = bstack1l1111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡧࡪࡶ࡫ࡹࡧ࠴ࡣࡰ࡯࠲ࡴࡪࡸࡣࡺ࠱ࡦࡰ࡮࠵ࡲࡦ࡮ࡨࡥࡸ࡫ࡳ࠰࡮ࡤࡸࡪࡹࡴ࠰ࡦࡲࡻࡳࡲ࡯ࡢࡦࠥὛ")
bstack1111111ll11_opy_ = bstack1l1111l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠵ࡨࡦࡣ࡯ࡸ࡭ࡩࡨࡦࡥ࡮ࠦ὜")
bstack11l1111l1_opy_ = bstack1l1111l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡧࡧࡷ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡵࡨࡲࡩࡥࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥὝ")
bstack111l11ll1l_opy_ = bstack1l1111l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡺࡨ࠴࡮ࡵࡣࠩ὞")
bstack111l111lll_opy_ = bstack1l1111l_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠬὟ")
bstack1l111l11ll_opy_ = bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠴࠵࠶࠷࠳ࡼࡪ࠯ࡩࡷࡥࠫὠ")
bstack11ll1l1l1l_opy_ = bstack1l1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡴࡥࡹࡶࡢ࡬ࡺࡨࡳࠨὡ")
bstack1l11lll1l1_opy_ = {
  bstack1l1111l_opy_ (u"ࠬࡪࡥࡧࡣࡸࡰࡹ࠭ὢ"): bstack1l1111l_opy_ (u"࠭ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ὣ"),
  bstack1l1111l_opy_ (u"ࠧࡶࡵ࠰ࡩࡦࡹࡴࠨὤ"): bstack1l1111l_opy_ (u"ࠨࡪࡸࡦ࠲ࡻࡳࡦ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪὥ"),
  bstack1l1111l_opy_ (u"ࠩࡸࡷࠬὦ"): bstack1l1111l_opy_ (u"ࠪ࡬ࡺࡨ࠭ࡶࡵ࠰ࡳࡳࡲࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫὧ"),
  bstack1l1111l_opy_ (u"ࠫࡪࡻࠧὨ"): bstack1l1111l_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡨࡹ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭Ὡ"),
  bstack1l1111l_opy_ (u"࠭ࡩ࡯ࠩὪ"): bstack1l1111l_opy_ (u"ࠧࡩࡷࡥ࠱ࡦࡶࡳ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩὫ"),
  bstack1l1111l_opy_ (u"ࠨࡣࡸࠫὬ"): bstack1l1111l_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡡࡱࡵࡨ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬὭ")
}
bstack111111lll1l_opy_ = {
  bstack1l1111l_opy_ (u"ࠪࡧࡷ࡯ࡴࡪࡥࡤࡰࠬὮ"): 50,
  bstack1l1111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪὯ"): 40,
  bstack1l1111l_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ὰ"): 30,
  bstack1l1111l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫά"): 20,
  bstack1l1111l_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ὲ"): 10
}
bstack11l1l1111_opy_ = bstack111111lll1l_opy_[bstack1l1111l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭έ")]
bstack1lll1llll_opy_ = bstack1l1111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥ࠲ࠫὴ")
bstack1l1ll1l1_opy_ = bstack1l1111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨή")
bstack111l111ll_opy_ = bstack1l1111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪὶ")
bstack1l1ll1ll1_opy_ = bstack1l1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫί")
bstack1l1l111l_opy_ = bstack1l1111l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡢࡰࡧࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫὸ")
bstack111lll11l_opy_ = {
  bstack1l1111l_opy_ (u"ࠧࡔࡆࡎ࠱ࡌࡋࡎ࠮࠲࠳࠹ࠬό"): bstack1l1111l_opy_ (u"ࠨࠬ࠭࠮ࠥࡡࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࡡࠥࡦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࡡࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡ࡫ࡱࠤࡾࡵࡵࡳࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠮ࠡࡖ࡫࡭ࡸࠦ࡭ࡢࡻࠣࡧࡦࡻࡳࡦࠢࡦࡳࡳ࡬࡬ࡪࡥࡷࡷࠥࡽࡩࡵࡪࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡭ࡹࠦࡵࡴ࡫ࡱ࡫࠿ࠦࡰࡪࡲࠣࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࠡࠬ࠭࠮ࠬὺ")
}
bstack1111111llll_opy_ = [bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪύ"), bstack1l1111l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪὼ")]
bstack11111l1ll11_opy_ = [bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧώ"), bstack1l1111l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ὾")]
bstack1lllll1l1ll_opy_ = re.compile(bstack1l1111l_opy_ (u"࠭࡞࡜࡞࡟ࡻ࠲ࡣࠫ࠻࠰࠭ࠨࠬ὿"))
bstack11lll11ll1_opy_ = [
  bstack1l1111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨᾀ"),
  bstack1l1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᾁ"),
  bstack1l1111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᾂ"),
  bstack1l1111l_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧᾃ"),
  bstack1l1111l_opy_ (u"ࠫࡦࡶࡰࠨᾄ"),
  bstack1l1111l_opy_ (u"ࠬࡻࡤࡪࡦࠪᾅ"),
  bstack1l1111l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᾆ"),
  bstack1l1111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧᾇ"),
  bstack1l1111l_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ᾈ"),
  bstack1l1111l_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧᾉ"),
  bstack1l1111l_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫᾊ"), bstack1l1111l_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧᾋ"),
  bstack1l1111l_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨᾌ"),
  bstack1l1111l_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬᾍ"),
  bstack1l1111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫᾎ"),
  bstack1l1111l_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫᾏ"),
  bstack1l1111l_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪᾐ"),
  bstack1l1111l_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨᾑ"), bstack1l1111l_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨᾒ"), bstack1l1111l_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧᾓ"), bstack1l1111l_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧᾔ"), bstack1l1111l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩᾕ"),
  bstack1l1111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᾖ"),
  bstack1l1111l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ᾗ"),
  bstack1l1111l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬᾘ"), bstack1l1111l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨᾙ"),
  bstack1l1111l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪᾚ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧᾛ"),
  bstack1l1111l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ࠭ᾜ"),
  bstack1l1111l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩᾝ"),
  bstack1l1111l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧᾞ"),
  bstack1l1111l_opy_ (u"ࠪࡥࡻࡪࠧᾟ"), bstack1l1111l_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧᾠ"), bstack1l1111l_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧᾡ"), bstack1l1111l_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧᾢ"),
  bstack1l1111l_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬᾣ"), bstack1l1111l_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧᾤ"), bstack1l1111l_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬᾥ"),
  bstack1l1111l_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬᾦ"), bstack1l1111l_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩᾧ"),
  bstack1l1111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧᾨ"), bstack1l1111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩᾩ"), bstack1l1111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬᾪ"), bstack1l1111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪᾫ"), bstack1l1111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭ᾬ"),
  bstack1l1111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭ᾭ"), bstack1l1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨᾮ"),
  bstack1l1111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧᾯ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫᾰ"),
  bstack1l1111l_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭ᾱ"), bstack1l1111l_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩᾲ"), bstack1l1111l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧᾳ"), bstack1l1111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᾴ"),
  bstack1l1111l_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩ᾵"),
  bstack1l1111l_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧᾶ"), bstack1l1111l_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ᾷ"),
  bstack1l1111l_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧᾸ"),
  bstack1l1111l_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪᾹ"),
  bstack1l1111l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫᾺ"),
  bstack1l1111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪΆ"),
  bstack1l1111l_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬᾼ"),
  bstack1l1111l_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ᾽"),
  bstack1l1111l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮ࠧι"),
  bstack1l1111l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭᾿"),
  bstack1l1111l_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬ῀"),
  bstack1l1111l_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭῁"),
  bstack1l1111l_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫῂ"),
  bstack1l1111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪῃ"),
  bstack1l1111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩῄ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭῅"),
  bstack1l1111l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬῆ"),
  bstack1l1111l_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬῇ"),
  bstack1l1111l_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩῈ"),
  bstack1l1111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧΈ"), bstack1l1111l_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨῊ"), bstack1l1111l_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨΉ"),
  bstack1l1111l_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪῌ"),
  bstack1l1111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫ῍"),
  bstack1l1111l_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪ῎"),
  bstack1l1111l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫ῏"),
  bstack1l1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧῐ"),
  bstack1l1111l_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨῑ"),
  bstack1l1111l_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨῒ"), bstack1l1111l_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸࠬΐ"), bstack1l1111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠪ῔"),
  bstack1l1111l_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨ῕"),
  bstack1l1111l_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶࠪῖ"),
  bstack1l1111l_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨࠬῗ"),
  bstack1l1111l_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫῘ"),
  bstack1l1111l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨῙ"), bstack1l1111l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨࠬῚ"),
  bstack1l1111l_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪΊ"), bstack1l1111l_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷࠬ῜"),
  bstack1l1111l_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣࠩ῝"),
  bstack1l1111l_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩ῞"),
  bstack1l1111l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧ῟"), bstack1l1111l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴࠩῠ"), bstack1l1111l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩࠪῡ"), bstack1l1111l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧῢ"),
  bstack1l1111l_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨΰ"),
  bstack1l1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪῤ"),
  bstack1l1111l_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ῥ"),
  bstack1l1111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫῦ"),
  bstack1l1111l_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨࠩῧ"),
  bstack1l1111l_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨῨ"),
  bstack1l1111l_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨῩ"), bstack1l1111l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩῪ"),
  bstack1l1111l_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬΎ"),
  bstack1l1111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪῬ"),
  bstack1l1111l_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬ῭"),
  bstack1l1111l_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬ΅"),
  bstack1l1111l_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨ`"),
  bstack1l1111l_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪ῰"),
  bstack1l1111l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩ῱"),
  bstack1l1111l_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧࠪῲ"),
  bstack1l1111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪῳ"),
  bstack1l1111l_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩῴ"),
  bstack1l1111l_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪ῵"),
  bstack1l1111l_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬῶ"),
  bstack1l1111l_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭ῷ"),
  bstack1l1111l_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪῸ"),
  bstack1l1111l_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫΌ"),
  bstack1l1111l_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ࠭Ὼ"),
  bstack1l1111l_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬΏ"),
  bstack1l1111l_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭ῼ"),
  bstack1l1111l_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮ࠪ´"),
  bstack1l1111l_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭῾"),
  bstack1l1111l_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫ῿"),
  bstack1l1111l_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ "), bstack1l1111l_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪ "),
  bstack1l1111l_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨ "), bstack1l1111l_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭ "),
  bstack1l1111l_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫ "),
  bstack1l1111l_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪ "),
  bstack1l1111l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪ "),
  bstack1l1111l_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭ "), bstack1l1111l_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭ "),
  bstack1l1111l_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ "),
  bstack1l1111l_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪ "),
  bstack1l1111l_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭​"),
  bstack1l1111l_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨ‌"),
  bstack1l1111l_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪ‍"),
  bstack1l1111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬ‎"),
  bstack1l1111l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨ‏"),
  bstack1l1111l_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪ‐"),
  bstack1l1111l_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧ‑"),
  bstack1l1111l_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬ‒"), bstack1l1111l_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫ–"),
  bstack1l1111l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨ—"),
  bstack1l1111l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡌࡨࡑࡵࡣࡢࡶࡲࡶࡆࡻࡴࡰࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠬ―")
]
bstack1l11l1111_opy_ = bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡸࡴࡱࡵࡡࡥࠩ‖")
bstack11ll1llll_opy_ = [bstack1l1111l_opy_ (u"ࠫ࠳ࡧࡰ࡬ࠩ‗"), bstack1l1111l_opy_ (u"ࠬ࠴ࡡࡢࡤࠪ‘"), bstack1l1111l_opy_ (u"࠭࠮ࡪࡲࡤࠫ’")]
bstack1lll1l11l_opy_ = [bstack1l1111l_opy_ (u"ࠧࡪࡦࠪ‚"), bstack1l1111l_opy_ (u"ࠨࡲࡤࡸ࡭࠭‛"), bstack1l1111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ“"), bstack1l1111l_opy_ (u"ࠪࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥࠩ”")]
bstack1l11l1ll1_opy_ = {
  bstack1l1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ„"): bstack1l1111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ‟"),
  bstack1l1111l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ†"): bstack1l1111l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ‡"),
  bstack1l1111l_opy_ (u"ࠨࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭•"): bstack1l1111l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ‣"),
  bstack1l1111l_opy_ (u"ࠪ࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭․"): bstack1l1111l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ‥"),
  bstack1l1111l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡴࡪࡱࡱࡷࠬ…"): bstack1l1111l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ‧")
}
bstack1ll111llll_opy_ = [
  bstack1l1111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ "),
  bstack1l1111l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ "),
  bstack1l1111l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ‪"),
  bstack1l1111l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ‫"),
  bstack1l1111l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ‬"),
]
bstack111l1lll11_opy_ = bstack1ll1l1l1_opy_ + bstack11111l1l11l_opy_ + bstack11lll11ll1_opy_
bstack11lllll111_opy_ = [
  bstack1l1111l_opy_ (u"ࠬࡤ࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵࠦࠪ‭"),
  bstack1l1111l_opy_ (u"࠭࡞ࡣࡵ࠰ࡰࡴࡩࡡ࡭࠰ࡦࡳࡲࠪࠧ‮"),
  bstack1l1111l_opy_ (u"ࠧ࡟࠳࠵࠻࠳࠭ "),
  bstack1l1111l_opy_ (u"ࠨࡠ࠴࠴࠳࠭‰"),
  bstack1l1111l_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠲࡝࠹࠱࠾ࡣ࠮ࠨ‱"),
  bstack1l1111l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠴࡞࠴࠲࠿࡝࠯ࠩ′"),
  bstack1l1111l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠶࡟࠵࠳࠱࡞࠰ࠪ″"),
  bstack1l1111l_opy_ (u"ࠬࡤ࠱࠺࠴࠱࠵࠻࠾࠮ࠨ‴")
]
bstack1111l111l1l_opy_ = bstack1l1111l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ‵")
bstack11ll11ll1_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡦࡸࡨࡲࡹ࠭‶")
bstack1l1l1l1lll_opy_ = [ bstack1l1111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ‷") ]
bstack1l1lll11l_opy_ = [ bstack1l1111l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ‸") ]
bstack1ll1l1llll_opy_ = [bstack1l1111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ‹")]
bstack1l11ll11_opy_ = [ bstack1l1111l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ›") ]
bstack1lll1111l1_opy_ = bstack1l1111l_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ※")
bstack1l11ll1l11_opy_ = bstack1l1111l_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩ‼")
bstack1l1ll1l111_opy_ = bstack1l1111l_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫ‽")
bstack111l11l11_opy_ = bstack1l1111l_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ‾")
bstack1111llll1_opy_ = [
  bstack1l1111l_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭‿"),
  bstack1l1111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪ⁀"),
  bstack1l1111l_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬ⁁"),
  bstack1l1111l_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫ⁂"),
  bstack1l1111l_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪ⁃"),
  bstack1l1111l_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨ⁄"),
  bstack1l1111l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨ⁅"),
  bstack1l1111l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫ⁆"),
  bstack1l1111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬ⁇"),
  bstack1l1111l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ⁈"),
  bstack1l1111l_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭⁉"),
  bstack1l1111l_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬ⁊"),
  bstack1l1111l_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪ⁋"),
  bstack1l1111l_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ⁌"),
  bstack1l1111l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭⁍"),
  bstack1l1111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ⁎"),
  bstack1l1111l_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧ⁏"),
  bstack1l1111l_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ⁐"),
  bstack1l1111l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧ⁑"),
  bstack1l1111l_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭⁒"),
  bstack1l1111l_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ⁓"),
]
bstack111lll111l_opy_ = bstack1l1111l_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧ⁔")
bstack1llllllll11_opy_ = os.path.join(os.path.expanduser(bstack1l1111l_opy_ (u"ࠪࢂࠬ⁕")), bstack1l1111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⁖"), bstack1l1111l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ⁗"))
bstack1111l1l1ll1_opy_ = bstack1l1111l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵ࡯ࠧ⁘")
bstack1111111l1ll_opy_ = [ bstack1l1111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⁙"), bstack1l1111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ⁚"), bstack1l1111l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ⁛"), bstack1l1111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ⁜")]
bstack1ll1l11l_opy_ = [ bstack1l1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⁝"), bstack1l1111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ⁞"), bstack1l1111l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ "), bstack1l1111l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ⁠"), bstack1l1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ⁡") ]
bstack11ll1ll111_opy_ = [ bstack1l1111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ⁢"), bstack1l1111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ⁣") ]
bstack11111l11lll_opy_ = [ bstack1l1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⁤"), bstack1l1111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ⁥") ]
bstack1l111111ll_opy_ = 360
bstack11111lllll1_opy_ = bstack1l1111l_opy_ (u"ࠨࡡࡱࡲ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨ⁦")
bstack1111111l11l_opy_ = bstack1l1111l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡬ࡷࡸࡻࡥࡴࠤ⁧")
bstack11111l1ll1l_opy_ = bstack1l1111l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠦ⁨")
bstack1111ll1l11l_opy_ = bstack1l1111l_opy_ (u"ࠤࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡸࡪࡹࡴࡴࠢࡤࡶࡪࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡲࡲࠥࡕࡓࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࠨࡷࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥࠡࡨࡲࡶࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦࡤࡦࡸ࡬ࡧࡪࡹ࠮ࠣ⁩")
bstack1111lll1l1l_opy_ = bstack1l1111l_opy_ (u"ࠥ࠵࠶࠴࠰ࠣ⁪")
bstack1lll11lllll_opy_ = {
  bstack1l1111l_opy_ (u"ࠫࡕࡇࡓࡔࠩ⁫"): bstack1l1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⁬"),
  bstack1l1111l_opy_ (u"࠭ࡆࡂࡋࡏࠫ⁭"): bstack1l1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⁮"),
  bstack1l1111l_opy_ (u"ࠨࡕࡎࡍࡕ࠭⁯"): bstack1l1111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⁰")
}
bstack1ll1l1111_opy_ = [
  bstack1l1111l_opy_ (u"ࠥ࡫ࡪࡺࠢⁱ"),
  bstack1l1111l_opy_ (u"ࠦ࡬ࡵࡂࡢࡥ࡮ࠦ⁲"),
  bstack1l1111l_opy_ (u"ࠧ࡭࡯ࡇࡱࡵࡻࡦࡸࡤࠣ⁳"),
  bstack1l1111l_opy_ (u"ࠨࡲࡦࡨࡵࡩࡸ࡮ࠢ⁴"),
  bstack1l1111l_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨ⁵"),
  bstack1l1111l_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ⁶"),
  bstack1l1111l_opy_ (u"ࠤࡶࡹࡧࡳࡩࡵࡇ࡯ࡩࡲ࡫࡮ࡵࠤ⁷"),
  bstack1l1111l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢ⁸"),
  bstack1l1111l_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢ⁹"),
  bstack1l1111l_opy_ (u"ࠧࡩ࡬ࡦࡣࡵࡉࡱ࡫࡭ࡦࡰࡷࠦ⁺"),
  bstack1l1111l_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࡹࠢ⁻"),
  bstack1l1111l_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠢ⁼"),
  bstack1l1111l_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡃࡶࡽࡳࡩࡓࡤࡴ࡬ࡴࡹࠨ⁽"),
  bstack1l1111l_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣ⁾"),
  bstack1l1111l_opy_ (u"ࠥࡵࡺ࡯ࡴࠣⁿ"),
  bstack1l1111l_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱ࡙ࡵࡵࡤࡪࡄࡧࡹ࡯࡯࡯ࠤ₀"),
  bstack1l1111l_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡓࡵ࡭ࡶ࡬ࡘࡴࡻࡣࡩࠤ₁"),
  bstack1l1111l_opy_ (u"ࠨࡳࡩࡣ࡮ࡩࠧ₂"),
  bstack1l1111l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࡇࡰࡱࠤ₃")
]
bstack111111l1ll1_opy_ = [
  bstack1l1111l_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࠢ₄"),
  bstack1l1111l_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ₅"),
  bstack1l1111l_opy_ (u"ࠥࡥࡺࡺ࡯ࠣ₆"),
  bstack1l1111l_opy_ (u"ࠦࡲࡧ࡮ࡶࡣ࡯ࠦ₇"),
  bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ₈")
]
bstack1l11lll1l_opy_ = {
  bstack1l1111l_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧ₉"): [bstack1l1111l_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨ₊")],
  bstack1l1111l_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ₋"): [bstack1l1111l_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ₌")],
  bstack1l1111l_opy_ (u"ࠥࡥࡺࡺ࡯ࠣ₍"): [bstack1l1111l_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣ₎"), bstack1l1111l_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣ₏"), bstack1l1111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥₐ"), bstack1l1111l_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨₑ")],
  bstack1l1111l_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣₒ"): [bstack1l1111l_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤₓ")],
  bstack1l1111l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧₔ"): [bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨₕ")],
}
bstack111111ll1l1_opy_ = {
  bstack1l1111l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦₖ"): bstack1l1111l_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧₗ"),
  bstack1l1111l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦₘ"): bstack1l1111l_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧₙ"),
  bstack1l1111l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨₚ"): bstack1l1111l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧₛ"),
  bstack1l1111l_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢₜ"): bstack1l1111l_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࠢ₝"),
  bstack1l1111l_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ₞"): bstack1l1111l_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ₟")
}
bstack1lll1ll1ll1_opy_ = {
  bstack1l1111l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ₠"): bstack1l1111l_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡕࡨࡸࡺࡶࠧ₡"),
  bstack1l1111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭₢"): bstack1l1111l_opy_ (u"ࠫࡘࡻࡩࡵࡧࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬ₣"),
  bstack1l1111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ₤"): bstack1l1111l_opy_ (u"࠭ࡔࡦࡵࡷࠤࡘ࡫ࡴࡶࡲࠪ₥"),
  bstack1l1111l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ₦"): bstack1l1111l_opy_ (u"ࠨࡖࡨࡷࡹࠦࡔࡦࡣࡵࡨࡴࡽ࡮ࠨ₧")
}
bstack111111l1l1l_opy_ = 65536
bstack1111111lll1_opy_ = bstack1l1111l_opy_ (u"ࠩ࠱࠲࠳ࡡࡔࡓࡗࡑࡇࡆ࡚ࡅࡅ࡟ࠪ₨")
bstack111111lllll_opy_ = [
      bstack1l1111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ₩"), bstack1l1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ₪"), bstack1l1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ₫"), bstack1l1111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ€"), bstack1l1111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩ₭"),
      bstack1l1111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ₮"), bstack1l1111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ₯"), bstack1l1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫ₰"), bstack1l1111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬ₱"),
      bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡐࡤࡱࡪ࠭₲"), bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ₳"), bstack1l1111l_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ₴"), bstack1l1111l_opy_ (u"ࠨࡷࡶࡩࡷࡥࡤࡢࡶࡤࠫ₵"), bstack1l1111l_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ₶"),
      bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࠧ₷"), bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡯ࡪࡿࠧ₸"), bstack1l1111l_opy_ (u"ࠬࡰࡷࡵࠩ₹")
    ]
bstack111111l1l11_opy_= {
  bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ₺"): bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ₻"),
  bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ₼"): bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭₽"),
  bstack1l1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ₾"): bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ₿"),
  bstack1l1111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⃀"): bstack1l1111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⃁"),
  bstack1l1111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⃂"): bstack1l1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⃃"),
  bstack1l1111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ⃄"): bstack1l1111l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ⃅"),
  bstack1l1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⃆"): bstack1l1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⃇"),
  bstack1l1111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⃈"): bstack1l1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⃉"),
  bstack1l1111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⃊"): bstack1l1111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⃋"),
  bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ⃌"): bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⃍"),
  bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⃎"): bstack1l1111l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⃏"),
  bstack1l1111l_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧ⃐"): bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨ⃑"),
  bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ⃒࠭"): bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ⃓ࠧ"),
  bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫ⃔"): bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࡔࡶࡴࡪࡱࡱࡷࠬ⃕"),
  bstack1l1111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ⃖"): bstack1l1111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩ⃗"),
  bstack1l1111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ⃘ࠬ"): bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ⃙ࠫ"),
  bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ⃚ࠬ"): bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⃛"),
  bstack1l1111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩ⃜"): bstack1l1111l_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪ⃝"),
  bstack1l1111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⃞"): bstack1l1111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⃟"),
  bstack1l1111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⃠"): bstack1l1111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⃡"),
  bstack1l1111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ⃢"): bstack1l1111l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨ⃣"),
  bstack1l1111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ⃤"): bstack1l1111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴ⃥ࠩ"),
  bstack1l1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃦"): bstack1l1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⃧"),
  bstack1l1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ⃨ࠪ"): bstack1l1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ⃩"),
  bstack1l1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦ⃪ࠩ"): bstack1l1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧ⃫ࠪ"),
  bstack1l1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶ⃬ࠫ"): bstack1l1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷ⃭ࠬ"),
  bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ⃮࠭"): bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹ⃯ࠧ"),
  bstack1l1111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ⃰"): bstack1l1111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬ⃱")
}
bstack111111lll11_opy_ = [bstack1l1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⃲"), bstack1l1111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭⃳")]
bstack11ll1l111_opy_ = (bstack1l1111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣ⃴"),)
bstack11111l11l1l_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡸࡴࡩࡧࡴࡦࡡࡦࡰ࡮࠭⃵")
bstack111ll11l11_opy_ = bstack1l1111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡧࡳ࡫ࡧࡷ࠴ࠨ⃶")
bstack111ll111_opy_ = bstack1l1111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡲࡪࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡢࡵ࡫ࡦࡴࡧࡲࡥ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࠥ⃷")
bstack11ll11l1ll_opy_ = bstack1l1111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳࠨ⃸")
class EVENTS(Enum):
  bstack11111l111l1_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪ⃹")
  bstack11l1l11lll_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡥࡢࡰࡸࡴࠬ⃺")
  bstack111ll11l1_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿࡬ࡩ࡯ࡣ࡯࡭ࡿ࡫ࠧ⃻")
  bstack111111l11l1_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡰࡧࡰࡴ࡭ࡳࠨ⃼")
  bstack1ll1l111_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭⃽") #shift post bstack111111l11ll_opy_
  bstack1ll11l11_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬ⃾") #shift post bstack111111l11ll_opy_
  bstack111111llll1_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡨࡶࡤࠪ⃿") #shift
  bstack111111ll11l_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡧࡳࡼࡴ࡬ࡰࡣࡧࠫ℀") #shift
  bstack1lll1ll1ll_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠻ࡪࡸࡦ࠲ࡳࡡ࡯ࡣࡪࡩࡲ࡫࡮ࡵࠩ℁")
  bstack1l1111llll1_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡷࡦࡼࡥ࠮ࡴࡨࡷࡺࡲࡴࡴࠩℂ")
  bstack11lllll1_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡵ࡫ࡲࡧࡱࡵࡱࡸࡩࡡ࡯ࠩ℃")
  bstack1111lll11_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡯ࡳࡨࡧ࡬ࠨ℄") #shift
  bstack1ll1l11ll1_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡢࡲࡳ࠱ࡺࡶ࡬ࡰࡣࡧࠫ℅") #shift
  bstack1l11l11l11_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡨ࡯࠭ࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠪ℆")
  bstack1ll11lll1l_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧℇ") #shift
  bstack1lll11lll1_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡪࡩࡹ࠳ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠳ࡲࡦࡵࡸࡰࡹࡹࠧ℈") #shift
  bstack11111l1l1ll_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼࠫ℉") #shift
  bstack11ll111111l_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩℊ")
  bstack1ll11ll1l1_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡶࡩࡸࡹࡩࡰࡰ࠰ࡷࡹࡧࡴࡶࡵࠪℋ") #shift
  bstack11lll11ll_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽࡬ࡺࡨ࠭࡮ࡣࡱࡥ࡬࡫࡭ࡦࡰࡷࠫℌ")
  bstack1111111ll1l_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡴࡾࡹ࠮ࡵࡨࡸࡺࡶࠧℍ") #shift
  bstack1l11l1lll_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡺࡵࡱࠩℎ")
  bstack11111l11111_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡷࡳࡧࡰࡴࡪࡲࡸࠬℏ") # not bstack1111111l1l1_opy_ in python
  bstack1l1l1l11ll_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡷࡵࡪࡶࠪℐ") # used in bstack111111l1111_opy_
  bstack111l1l1l1ll_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡳࡧ࠰ࡵࡺ࡯ࡴࠨℑ")
  bstack111l1l1l1l1_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲ࡷࡵࡪࡶࠪℒ")
  bstack111l1111_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡩࡨࡸࠬℓ") # used in bstack111111l1111_opy_
  bstack1ll1ll1ll_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼࡫ࡳࡴࡱࠧ℔")
  bstack111ll111l1l_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷ࡫࠭ࡩࡱࡲ࡯ࠬℕ")
  bstack111ll111l11_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡵࡳࡵ࠯࡫ࡳࡴࡱࠧ№")
  bstack1l1ll1l11l_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪ࠭℗")
  bstack1l11lll11l_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳ࠭℘") #
  bstack1ll1ll1l_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡰ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡺࡡ࡬ࡧࡖࡧࡷ࡫ࡥ࡯ࡕ࡫ࡳࡹ࠭ℙ")
  bstack1lllll11l1_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡢࡷࡷࡳ࠲ࡩࡡࡱࡶࡸࡶࡪ࠭ℚ")
  bstack1lllllll111_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡴࡦࡵࡷࠫℛ")
  bstack111l11l1l1_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡶࡨࡷࡹ࠭ℜ")
  bstack111l11l1ll_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡸࡥ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩℝ") #shift
  bstack1ll1ll1l1l_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫ℞") #shift
  bstack111111ll111_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬ℟")
  bstack111111l1lll_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡬ࡨࡱ࡫࠭ࡵ࡫ࡰࡩࡴࡻࡴࠨ℠")
  bstack11l1111l1l_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡧࡻ࡭ࡹ࠳ࡨࡢࡰࡧࡰࡪࡸࠧ℡")
  bstack1l1l1l1l1l1_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡥࡹ࡫ࡷ࠱࡭ࡧ࡮ࡥ࡮ࡨࡶࠬ™")
  bstack11111l11ll1_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡴࡤ࠮࡯ࡨࡸࡷ࡯ࡣࡴࠩ℣")
  bstack11111l111ll_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡪࡸࡦ࠿ࡹࡴࡰࡲࠪℤ")
  bstack1l11llllll1_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡶࡸࡦࡸࡴࠨ℥")
  bstack111111ll1ll_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡨࡴࡽ࡮࡭ࡱࡤࡨࠬΩ")
  bstack11111l1111l_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡨ࡮ࡥࡤ࡭࠰ࡹࡵࡪࡡࡵࡧࠪ℧")
  bstack1l1l111l1ll_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡤࡲࡳࡹࡹࡴࡳࡣࡳࠫℨ")
  bstack1l11llll111_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡶࡸࡦࡸࡴࡣ࡫ࡱࡥࡷࡿࠧ℩")
  bstack1l1l111l1l1_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡧࡴࡴ࡮ࡦࡥࡷࠫK")
  bstack1l1l11l11l1_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡸࡺ࡯ࡱࠩÅ")
  bstack1l1l1l11l11_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠧℬ")
  bstack1l11ll1111l_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡣࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰࠪℭ")
  bstack11111l1l111_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠫ℮")
  bstack11111l1l1l1_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡨ࡬ࡲࡩࡔࡥࡢࡴࡨࡷࡹࡎࡵࡣࠩℯ")
  bstack11l1l11lll1_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡊࡰ࡬ࡸࠬℰ")
  bstack11l1l111l1l_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡷࡺࠧℱ")
  bstack1l111l1ll11_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪℲ")
  bstack1111111l111_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡈࡵ࡮ࡧ࡫ࡪࠫℳ")
  bstack11llll1l1ll_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡖࡸࡪࡶࠧℴ")
  bstack11llll1ll11_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࡫ࡖࡩࡱ࡬ࡈࡦࡣ࡯ࡋࡪࡺࡒࡦࡵࡸࡰࡹ࠭ℵ")
  bstack11lll1l1l1l_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡆࡸࡨࡲࡹ࠭ℶ")
  bstack11ll1ll1l1l_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠬℷ")
  bstack11ll111ll1l_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺࡭ࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࡉࡻ࡫࡮ࡵࠩℸ")
  bstack11111l11l11_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡧࡱࡵࡺ࡫ࡵࡦࡖࡨࡷࡹࡋࡶࡦࡰࡷࠫℹ")
  bstack11l11ll11ll_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡵࡰࠨ℺")
  bstack1l11lllllll_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀ࡯࡯ࡕࡷࡳࡵ࠭℻")
  bstack1111llll1ll_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮ࡨࡥࡳࡻࡰࡖࡲ࡯ࡳࡦࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠫℼ")
  bstack1l1lll111l_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡌࡵ࡯ࡰࡨࡰ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠫℽ")
  bstack11l1ll111_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪࡆࡶࡰࡱࡩࡱ࡚ࡥࡴࡶࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࠬℾ")
  bstack1ll11ll1111_opy_ = bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡵࡶ࡬ࡺࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡑࡻࡷࡩࡸࡺࠧℿ")
  bstack1llll1lll1l_opy_ = bstack1l1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡶࡰ࡭ࡻࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡄࡨ࡬ࡦࡼࡥࠨ⅀")
  bstack1ll11l11l1l_opy_ = bstack1l1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡵࡓࡽࡹ࡫ࡳࡵࠩ⅁")
  bstack1ll11l1lll1_opy_ = bstack1l1111l_opy_ (u"ࠩࡶࡨࡰࡀࡰࡺࡶࡨࡷࡹࡍࡥࡵࡖࡲࡸࡦࡲࡔࡦࡵࡷࡷࠬ⅂")
class STAGE(Enum):
  bstack1l1lll1lll_opy_ = bstack1l1111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩ⅃")
  END = bstack1l1111l_opy_ (u"ࠫࡪࡴࡤࠨ⅄")
  bstack111ll11111_opy_ = bstack1l1111l_opy_ (u"ࠬࡹࡩ࡯ࡩ࡯ࡩࠬⅅ")
bstack1l1l11llll_opy_ = {
  bstack1l1111l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭ⅆ"): bstack1l1111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧⅇ"),
  bstack1l1111l_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬⅈ"): bstack1l1111l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫⅉ"),
  bstack1l1111l_opy_ (u"ࠪࡆࡊࡎࡁࡗࡇࠪ⅊"): bstack1l1111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ⅋")
}
PLAYWRIGHT_HUB_URL = bstack1l1111l_opy_ (u"ࠧࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠢ⅌")
bstack11l1111ll_opy_ = {bstack1l1111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭⅍"), bstack1l1111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩⅎ"), bstack1l1111l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩࡨࡳࡱࡰ࡭ࡺࡳࠧ⅏")}
MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION = 98
bstack1l1111l1lll_opy_ = 100
bstack11l1111ll_opy_ = (bstack1l1111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ⅐"), bstack1l1111l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩ⅑"), bstack1l1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠭⅒"))
bstack1ll11ll1l11_opy_ = {
  bstack1l1111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫ⅓"): bstack1l1111l_opy_ (u"࠭࠭࠮ࡴࡨࡶࡺࡴࡳࠨ⅔"),
  bstack1l1111l_opy_ (u"ࠧࡥࡧ࡯ࡥࡾ࠭⅕"): bstack1l1111l_opy_ (u"ࠨ࠯࠰ࡶࡪࡸࡵ࡯ࡵ࠰ࡨࡪࡲࡡࡺࠩ⅖"),
  bstack1l1111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧ⅗"): 0
}
bstack11111ll1111_opy_ = bstack1l1111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥ⅘")
bstack11111l1llll_opy_ = bstack1l1111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣ⅙")
bstack1l11l1l1_opy_ = bstack1l1111l_opy_ (u"࡚ࠧࡅࡔࡖࠣࡖࡊࡖࡏࡓࡖࡌࡒࡌࠦࡁࡏࡆࠣࡅࡓࡇࡌ࡚ࡖࡌࡇࡘࠨ⅚")