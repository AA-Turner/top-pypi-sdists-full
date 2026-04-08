# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import re
from enum import Enum
bstack111ll111_opy_ = {
  bstack111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭᷋"): bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩ᷌"),
  bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ᷍"): bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻ᷎ࠪ"),
  bstack111l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱ᷏ࠫ"): bstack111l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ᷐࠭"),
  bstack111l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ᷑"): bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫ᷒"),
  bstack111l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᷓ"): bstack111l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧᷔ"),
  bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᷕ"): bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᷖ"),
  bstack111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᷗ"): bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨᷘ"),
  bstack111l_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᷙ"): bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪᷚ"),
  bstack111l_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫᷛ"): bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧᷜ"),
  bstack111l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᷝ"): bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᷞ"),
  bstack111l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᷟ"): bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᷠ"),
  bstack111l_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫᷡ"): bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫᷢ"),
  bstack111l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᷣ"): bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᷤ"),
  bstack111l_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᷥ"): bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᷦ"),
  bstack111l_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᷧ"): bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᷨ"),
  bstack111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨᷩ"): bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨᷪ"),
  bstack111l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᷫ"): bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᷬ"),
  bstack111l_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩᷭ"): bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩᷮ"),
  bstack111l_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᷯ"): bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᷰ"),
  bstack111l_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧᷱ"): bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧᷲ"),
  bstack111l_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫᷳ"): bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫᷴ"),
  bstack111l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭᷵"): bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭᷶"),
  bstack111l_opy_ (u"࠭ࡨࡰࡵࡷࡷ᷷ࠬ"): bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷ᷸ࠬ"),
  bstack111l_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦ᷹ࠩ"): bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦ᷺ࠩ"),
  bstack111l_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ᷻"): bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ᷼"),
  bstack111l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ᷽"): bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ᷾"),
  bstack111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨ᷿ࠫ"): bstack111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨḀ"),
  bstack111l_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭ḁ"): bstack111l_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨḂ"),
  bstack111l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫḃ"): bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬḄ"),
  bstack111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ḅ"): bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭Ḇ"),
  bstack111l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩḇ"): bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩḈ"),
  bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩḉ"): bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬḊ"),
  bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧḋ"): bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧḌ"),
  bstack111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧḍ"): bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧḎ"),
  bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫḏ"): bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫḐ"),
  bstack111l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ḑ"): bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭Ḓ"),
  bstack111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩḓ"): bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩḔ"),
  bstack111l_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬḕ"): bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬḖ"),
  bstack111l_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨḗ"): bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨḘ"),
  bstack111l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨḙ"): bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨḚ"),
  bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩḛ"): bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩḜ")
}
bstack11111l1ll1l_opy_ = [
  bstack111l_opy_ (u"ࠩࡲࡷࠬḝ"),
  bstack111l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ḟ"),
  bstack111l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ḟ"),
  bstack111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪḠ"),
  bstack111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪḡ"),
  bstack111l_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫḢ"),
  bstack111l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨḣ"),
]
bstack11l1l11ll_opy_ = {
  bstack111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫḤ"): [bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫḥ"), bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡐࡄࡑࡊ࠭Ḧ")],
  bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨḧ"): bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩḨ"),
  bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪḩ"): bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠫḪ"),
  bstack111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧḫ"): bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠨḬ"),
  bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ḭ"): bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧḮ"),
  bstack111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ḯ"): bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡔࡡࡓࡉࡗࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨḰ"),
  bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬḱ"): bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧḲ"),
  bstack111l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧḳ"): bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨḴ"),
  bstack111l_opy_ (u"ࠬࡧࡰࡱࠩḵ"): [bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࡡࡌࡈࠬḶ"), bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࠪḷ")],
  bstack111l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪḸ"): bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡒࡏࡈࡎࡈ࡚ࡊࡒࠧḹ"),
  bstack111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧḺ"): bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧḻ"),
  bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḼ"): [bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠪḽ"), bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧḾ")],
  bstack111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬḿ"): bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡘࡖࡇࡕࡓࡄࡃࡏࡉࠬṀ"),
  bstack111l_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡊࡔࡖࠨṁ"): bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡓࡗࡉࡈࡆࡕࡗࡖࡆ࡚ࡉࡐࡐࡢࡗࡒࡇࡒࡕࡡࡖࡉࡑࡋࡃࡕࡋࡒࡒࡤࡌࡅࡂࡖࡘࡖࡊࡥࡂࡓࡃࡑࡇࡍࡋࡓࠨṂ")
}
bstack111l1l111l_opy_ = {
  bstack111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧṃ"): [bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡢࡲࡦࡳࡥࠨṄ"), bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡒࡦࡳࡥࠨṅ")],
  bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫṆ"): [bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡠ࡭ࡨࡽࠬṇ"), bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬṈ")],
  bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧṉ"): bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧṊ"),
  bstack111l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫṋ"): bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫṌ"),
  bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪṍ"): bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪṎ"),
  bstack111l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪṏ"): [bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡵࡶࠧṐ"), bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫṑ")],
  bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪṒ"): bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬṓ"),
  bstack111l_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬṔ"): bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬṕ"),
  bstack111l_opy_ (u"ࠪࡥࡵࡶࠧṖ"): bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࠧṗ"),
  bstack111l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧṘ"): bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡨࡎࡨࡺࡪࡲࠧṙ"),
  bstack111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫṚ"): bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫṛ"),
  bstack111l_opy_ (u"ࠤࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡇࡑࡏࠢṜ"): bstack111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࠣṝ"),
}
bstack1llll111ll_opy_ = {
  bstack111l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧṞ"): bstack111l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩṟ"),
  bstack111l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨṠ"): [bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩṡ"), bstack111l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫṢ")],
  bstack111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧṣ"): bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨṤ"),
  bstack111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨṥ"): bstack111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬṦ"),
  bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫṧ"): [bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨṨ"), bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧṩ")],
  bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪṪ"): bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬṫ"),
  bstack111l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨṬ"): bstack111l_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪṭ"),
  bstack111l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ṯ"): [bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧṯ"), bstack111l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩṰ")],
  bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨṱ"): [bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫṲ"), bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫṳ")]
}
bstack1l11llll1_opy_ = [
  bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫṴ"),
  bstack111l_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩṵ"),
  bstack111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭Ṷ"),
  bstack111l_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨṷ"),
  bstack111l_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫṸ"),
  bstack111l_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨṹ"),
  bstack111l_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧṺ"),
  bstack111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪṻ"),
  bstack111l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫṼ"),
  bstack111l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨṽ"),
  bstack111l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧṾ"),
  bstack111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪṿ"),
]
bstack1111lllll1_opy_ = [
  bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧẀ"),
  bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨẁ"),
  bstack111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫẂ"),
  bstack111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ẃ"),
  bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪẄ"),
  bstack111l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪẅ"),
  bstack111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬẆ"),
  bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧẇ"),
  bstack111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧẈ"),
  bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪẉ"),
  bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪẊ"),
  bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧẋ"),
  bstack111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪẌ"),
  bstack111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡖࡤ࡫ࠬẍ"),
  bstack111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧẎ"),
  bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ẏ"),
  bstack111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩẐ"),
  bstack111l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠵ࠬẑ"),
  bstack111l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠷࠭Ẓ"),
  bstack111l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠹ࠧẓ"),
  bstack111l_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠴ࠨẔ"),
  bstack111l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠶ࠩẕ"),
  bstack111l_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠸ࠪẖ"),
  bstack111l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠺ࠫẗ"),
  bstack111l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠼ࠬẘ"),
  bstack111l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠾࠭ẙ"),
  bstack111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧẚ"),
  bstack111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨẛ"),
  bstack111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ẜ"),
  bstack111l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ẝ"),
  bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩẞ"),
  bstack111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪẟ"),
  bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫẠ"),
  bstack111l_opy_ (u"ࠨࡪࡸࡦࡗ࡫ࡧࡪࡱࡱࠫạ")
]
bstack11111l11111_opy_ = [
  bstack111l_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧẢ"),
  bstack111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬả"),
  bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧẤ"),
  bstack111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪấ"),
  bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡔࡷ࡯࡯ࡳ࡫ࡷࡽࠬẦ"),
  bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪầ"),
  bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡢࡩࠪẨ"),
  bstack111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧẩ"),
  bstack111l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬẪ"),
  bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩẫ"),
  bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ậ"),
  bstack111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬậ"),
  bstack111l_opy_ (u"ࠧࡰࡵࠪẮ"),
  bstack111l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫắ"),
  bstack111l_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨẰ"),
  bstack111l_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬằ"),
  bstack111l_opy_ (u"ࠫࡷ࡫ࡧࡪࡱࡱࠫẲ"),
  bstack111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧẳ"),
  bstack111l_opy_ (u"࠭࡭ࡢࡥ࡫࡭ࡳ࡫ࠧẴ"),
  bstack111l_opy_ (u"ࠧࡳࡧࡶࡳࡱࡻࡴࡪࡱࡱࠫẵ"),
  bstack111l_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭Ặ"),
  bstack111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ặ"),
  bstack111l_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩẸ"),
  bstack111l_opy_ (u"ࠫࡳࡵࡐࡢࡩࡨࡐࡴࡧࡤࡕ࡫ࡰࡩࡴࡻࡴࠨẹ"),
  bstack111l_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭Ẻ"),
  bstack111l_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬẻ"),
  bstack111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫẼ"),
  bstack111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩẽ"),
  bstack111l_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭Ế"),
  bstack111l_opy_ (u"ࠪࡲࡴࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠧế"),
  bstack111l_opy_ (u"ࠫࡨ࡮ࡥࡤ࡭ࡘࡖࡑ࠭Ề"),
  bstack111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧề"),
  bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡉ࡯ࡰ࡭࡬ࡩࡸ࠭Ể"),
  bstack111l_opy_ (u"ࠧࡤࡣࡳࡸࡺࡸࡥࡄࡴࡤࡷ࡭࠭ể"),
  bstack111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬỄ"),
  bstack111l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩễ"),
  bstack111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡖࡦࡴࡶ࡭ࡴࡴࠧỆ"),
  bstack111l_opy_ (u"ࠫࡳࡵࡂ࡭ࡣࡱ࡯ࡕࡵ࡬࡭࡫ࡱ࡫ࠬệ"),
  bstack111l_opy_ (u"ࠬࡳࡡࡴ࡭ࡖࡩࡳࡪࡋࡦࡻࡶࠫỈ"),
  bstack111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡒ࡯ࡨࡵࠪỉ"),
  bstack111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡉࡥࠩỊ"),
  bstack111l_opy_ (u"ࠨࡦࡨࡨ࡮ࡩࡡࡵࡧࡧࡈࡪࡼࡩࡤࡧࠪị"),
  bstack111l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡒࡤࡶࡦࡳࡳࠨỌ"),
  bstack111l_opy_ (u"ࠪࡴ࡭ࡵ࡮ࡦࡐࡸࡱࡧ࡫ࡲࠨọ"),
  bstack111l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩỎ"),
  bstack111l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡒࡴࡹ࡯࡯࡯ࡵࠪỏ"),
  bstack111l_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫỐ"),
  bstack111l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧố"),
  bstack111l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬỒ"),
  bstack111l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡄ࡬ࡳࡲ࡫ࡴࡳ࡫ࡦࠫồ"),
  bstack111l_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࡘ࠵ࠫỔ"),
  bstack111l_opy_ (u"ࠫࡲ࡯ࡤࡔࡧࡶࡷ࡮ࡵ࡮ࡊࡰࡶࡸࡦࡲ࡬ࡂࡲࡳࡷࠬổ"),
  bstack111l_opy_ (u"ࠬ࡫ࡳࡱࡴࡨࡷࡸࡵࡓࡦࡴࡹࡩࡷ࠭Ỗ"),
  bstack111l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬỗ"),
  bstack111l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡅࡧࡴࠬỘ"),
  bstack111l_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨộ"),
  bstack111l_opy_ (u"ࠩࡶࡽࡳࡩࡔࡪ࡯ࡨ࡛࡮ࡺࡨࡏࡖࡓࠫỚ"),
  bstack111l_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨớ"),
  bstack111l_opy_ (u"ࠫ࡬ࡶࡳࡍࡱࡦࡥࡹ࡯࡯࡯ࠩỜ"),
  bstack111l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ờ"),
  bstack111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭Ở"),
  bstack111l_opy_ (u"ࠧࡧࡱࡵࡧࡪࡉࡨࡢࡰࡪࡩࡏࡧࡲࠨở"),
  bstack111l_opy_ (u"ࠨࡺࡰࡷࡏࡧࡲࠨỠ"),
  bstack111l_opy_ (u"ࠩࡻࡱࡽࡐࡡࡳࠩỡ"),
  bstack111l_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩỢ"),
  bstack111l_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫợ"),
  bstack111l_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭Ụ"),
  bstack111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩụ"),
  bstack111l_opy_ (u"ࠧࡢࡲࡳ࡚ࡪࡸࡳࡪࡱࡱࠫỦ"),
  bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧủ"),
  bstack111l_opy_ (u"ࠩࡵࡩࡸ࡯ࡧ࡯ࡃࡳࡴࠬỨ"),
  bstack111l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳࡹࠧứ"),
  bstack111l_opy_ (u"ࠫࡨࡧ࡮ࡢࡴࡼࠫỪ"),
  bstack111l_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ừ"),
  bstack111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭Ử"),
  bstack111l_opy_ (u"ࠧࡪࡧࠪử"),
  bstack111l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭Ữ"),
  bstack111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩữ"),
  bstack111l_opy_ (u"ࠪࡵࡺ࡫ࡵࡦࠩỰ"),
  bstack111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ự"),
  bstack111l_opy_ (u"ࠬࡧࡰࡱࡕࡷࡳࡷ࡫ࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳ࠭Ỳ"),
  bstack111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡉࡡ࡮ࡧࡵࡥࡎࡳࡡࡨࡧࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬỳ"),
  bstack111l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡊࡾࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪỴ"),
  bstack111l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡏ࡮ࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫỵ"),
  bstack111l_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭Ỷ"),
  bstack111l_opy_ (u"ࠪࡶࡪࡹࡥࡳࡸࡨࡈࡪࡼࡩࡤࡧࠪỷ"),
  bstack111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫỸ"),
  bstack111l_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧỹ"),
  bstack111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡡࡴࡵࡦࡳࡩ࡫ࠧỺ"),
  bstack111l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡉࡰࡵࡇࡩࡻ࡯ࡣࡦࡕࡨࡸࡹ࡯࡮ࡨࡵࠪỻ"),
  bstack111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡷࡧ࡭ࡴࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨỼ"),
  bstack111l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡳࡴࡱ࡫ࡐࡢࡻࠪỽ"),
  bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫỾ"),
  bstack111l_opy_ (u"ࠫࡼࡪࡩࡰࡕࡨࡶࡻ࡯ࡣࡦࠩỿ"),
  bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧἀ"),
  bstack111l_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡃࡳࡱࡶࡷࡘ࡯ࡴࡦࡖࡵࡥࡨࡱࡩ࡯ࡩࠪἁ"),
  bstack111l_opy_ (u"ࠧࡩ࡫ࡪ࡬ࡈࡵ࡮ࡵࡴࡤࡷࡹ࠭ἂ"),
  bstack111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡑࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࡷࠬἃ"),
  bstack111l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬἄ"),
  bstack111l_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧἅ"),
  bstack111l_opy_ (u"ࠫࡷ࡫࡭ࡰࡸࡨࡍࡔ࡙ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࡐࡴࡩࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩἆ"),
  bstack111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧἇ"),
  bstack111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨἈ"),
  bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩἉ"),
  bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧἊ"),
  bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫἋ"),
  bstack111l_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭Ἄ"),
  bstack111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪἍ"),
  bstack111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧἎ"),
  bstack111l_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩἏ")
]
bstack11ll11lll1_opy_ = {
  bstack111l_opy_ (u"ࠧࡷࠩἐ"): bstack111l_opy_ (u"ࠨࡸࠪἑ"),
  bstack111l_opy_ (u"ࠩࡩࠫἒ"): bstack111l_opy_ (u"ࠪࡪࠬἓ"),
  bstack111l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪἔ"): bstack111l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫἕ"),
  bstack111l_opy_ (u"࠭࡯࡯࡮ࡼࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ἖"): bstack111l_opy_ (u"ࠧࡰࡰ࡯ࡽࡆࡻࡴࡰ࡯ࡤࡸࡪ࠭἗"),
  bstack111l_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬἘ"): bstack111l_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭Ἑ"),
  bstack111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭Ἒ"): bstack111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧἛ"),
  bstack111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨἜ"): bstack111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩἝ"),
  bstack111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪ἞"): bstack111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ἟"),
  bstack111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬἠ"): bstack111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ἡ"),
  bstack111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬἢ"): bstack111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡊࡲࡷࡹ࠭ἣ"),
  bstack111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧἤ"): bstack111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨἥ"),
  bstack111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩἦ"): bstack111l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫἧ"),
  bstack111l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬἨ"): bstack111l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭Ἡ"),
  bstack111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭Ἢ"): bstack111l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨἫ"),
  bstack111l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩἬ"): bstack111l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪἭ"),
  bstack111l_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭Ἦ"): bstack111l_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧἯ"),
  bstack111l_opy_ (u"ࠫࡵࡧࡣࡧ࡫࡯ࡩࠬἰ"): bstack111l_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨἱ"),
  bstack111l_opy_ (u"࠭ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨἲ"): bstack111l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪἳ"),
  bstack111l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫἴ"): bstack111l_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬἵ"),
  bstack111l_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫἶ"): bstack111l_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬἷ"),
  bstack111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧἸ"): bstack111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨἹ"),
  bstack111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩἺ"): bstack111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡳࡩࡦࡺࡥࡳࠩἻ")
}
bstack11111l11lll_opy_ = bstack111l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫࡮ࡺࡨࡶࡤ࠱ࡧࡴࡳ࠯ࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫࠲ࡶࡪࡲࡥࡢࡵࡨࡷ࠴ࡲࡡࡵࡧࡶࡸ࠴ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢἼ")
bstack11111l1l1ll_opy_ = bstack111l_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠲࡬ࡪࡧ࡬ࡵࡪࡦ࡬ࡪࡩ࡫ࠣἽ")
bstack111111ll11_opy_ = bstack111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡫ࡤࡴ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡹࡥ࡯ࡦࡢࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢἾ")
bstack1ll11111l_opy_ = bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭Ἷ")
bstack1l111ll11l_opy_ = bstack111l_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩὀ")
bstack111ll1lll_opy_ = bstack111l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠸࠹࠺࠴࠰ࡹࡧ࠳࡭ࡻࡢࠨὁ")
bstack111l1111_opy_ = bstack111l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬὂ")
bstack1llll1111l_opy_ = {
  bstack111l_opy_ (u"ࠩࡧࡩ࡫ࡧࡵ࡭ࡶࠪὃ"): bstack111l_opy_ (u"ࠪ࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪὄ"),
  bstack111l_opy_ (u"ࠫࡺࡹ࠭ࡦࡣࡶࡸࠬὅ"): bstack111l_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡸࡷࡪ࠳࡯࡯࡮ࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ὆"),
  bstack111l_opy_ (u"࠭ࡵࡴࠩ὇"): bstack111l_opy_ (u"ࠧࡩࡷࡥ࠱ࡺࡹ࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨὈ"),
  bstack111l_opy_ (u"ࠨࡧࡸࠫὉ"): bstack111l_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡥࡶ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪὊ"),
  bstack111l_opy_ (u"ࠪ࡭ࡳ࠭Ὃ"): bstack111l_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡣࡳࡷ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭Ὄ"),
  bstack111l_opy_ (u"ࠬࡧࡵࠨὍ"): bstack111l_opy_ (u"࠭ࡨࡶࡤ࠰ࡥࡵࡹࡥ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ὎")
}
bstack111111l1ll1_opy_ = {
  bstack111l_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩ὏"): 50,
  bstack111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧὐ"): 40,
  bstack111l_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪὑ"): 30,
  bstack111l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨὒ"): 20,
  bstack111l_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪὓ"): 10
}
bstack111lllll1_opy_ = bstack111111l1ll1_opy_[bstack111l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪὔ")]
bstack11lllll11l_opy_ = bstack111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩ࠯ࠨὕ")
bstack1ll1ll11l1_opy_ = bstack111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬὖ")
bstack1l1l11lll_opy_ = bstack111l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧὗ")
bstack1ll11l1ll_opy_ = bstack111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ὘")
bstack1lll11l11_opy_ = bstack111l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡦࡴࡤࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡴࡦࡩ࡫ࡢࡩࡨࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡠࠨὙ")
bstack1l11l1lll_opy_ = {
  bstack111l_opy_ (u"ࠫࡘࡊࡋ࠮ࡉࡈࡒ࠲࠶࠰࠶ࠩ὚"): bstack111l_opy_ (u"ࠬ࠰ࠪࠫࠢ࡞ࡗࡉࡑ࠭ࡈࡇࡑ࠱࠵࠶࠵࡞ࠢࡣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࡥࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥ࡯࡮ࠡࡻࡲࡹࡷࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠲࡚ࠥࡨࡪࡵࠣࡱࡦࡿࠠࡤࡣࡸࡷࡪࠦࡣࡰࡰࡩࡰ࡮ࡩࡴࡴࠢࡺ࡭ࡹ࡮ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࠠࡪࡶࠣࡹࡸ࡯࡮ࡨ࠼ࠣࡴ࡮ࡶࠠࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࠥ࠰ࠪࠫࠩὛ")
}
bstack11111l1ll11_opy_ = [bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ὜"), bstack111l_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧὝ")]
bstack111111l1l11_opy_ = [bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ὞"), bstack111l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫὟ")]
bstack11ll111111_opy_ = re.compile(bstack111l_opy_ (u"ࠪࡢࡠࡢ࡜ࡸ࠯ࡠ࠯࠿࠴ࠪࠥࠩὠ"))
bstack1l1l11ll1l_opy_ = [
  bstack111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡏࡣࡰࡩࠬὡ"),
  bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧὢ"),
  bstack111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪὣ"),
  bstack111l_opy_ (u"ࠧ࡯ࡧࡺࡇࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࠫὤ"),
  bstack111l_opy_ (u"ࠨࡣࡳࡴࠬὥ"),
  bstack111l_opy_ (u"ࠩࡸࡨ࡮ࡪࠧὦ"),
  bstack111l_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬὧ"),
  bstack111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࠫὨ"),
  bstack111l_opy_ (u"ࠬࡵࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪὩ"),
  bstack111l_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࠫὪ"),
  bstack111l_opy_ (u"ࠧ࡯ࡱࡕࡩࡸ࡫ࡴࠨὫ"), bstack111l_opy_ (u"ࠨࡨࡸࡰࡱࡘࡥࡴࡧࡷࠫὬ"),
  bstack111l_opy_ (u"ࠩࡦࡰࡪࡧࡲࡔࡻࡶࡸࡪࡳࡆࡪ࡮ࡨࡷࠬὭ"),
  bstack111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡖ࡬ࡱ࡮ࡴࡧࡴࠩὮ"),
  bstack111l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࡍࡱࡪ࡫࡮ࡴࡧࠨὯ"),
  bstack111l_opy_ (u"ࠬࡵࡴࡩࡧࡵࡅࡵࡶࡳࠨὰ"),
  bstack111l_opy_ (u"࠭ࡰࡳ࡫ࡱࡸࡕࡧࡧࡦࡕࡲࡹࡷࡩࡥࡐࡰࡉ࡭ࡳࡪࡆࡢ࡫࡯ࡹࡷ࡫ࠧά"),
  bstack111l_opy_ (u"ࠧࡢࡲࡳࡅࡨࡺࡩࡷ࡫ࡷࡽࠬὲ"), bstack111l_opy_ (u"ࠨࡣࡳࡴࡕࡧࡣ࡬ࡣࡪࡩࠬέ"), bstack111l_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡄࡧࡹ࡯ࡶࡪࡶࡼࠫὴ"), bstack111l_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡔࡦࡩ࡫ࡢࡩࡨࠫή"), bstack111l_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭ὶ"),
  bstack111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪί"),
  bstack111l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙࡫ࡳࡵࡒࡤࡧࡰࡧࡧࡦࡵࠪὸ"),
  bstack111l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࠩό"), bstack111l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡅࡲࡺࡪࡸࡡࡨࡧࡈࡲࡩࡏ࡮ࡵࡧࡱࡸࠬὺ"),
  bstack111l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧύ"),
  bstack111l_opy_ (u"ࠪࡥࡩࡨࡐࡰࡴࡷࠫὼ"),
  bstack111l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡗࡴࡩ࡫ࡦࡶࠪώ"),
  bstack111l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱ࡚ࡩ࡮ࡧࡲࡹࡹ࠭὾"),
  bstack111l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡶ࡫ࠫ὿"),
  bstack111l_opy_ (u"ࠧࡢࡸࡧࠫᾀ"), bstack111l_opy_ (u"ࠨࡣࡹࡨࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫᾁ"), bstack111l_opy_ (u"ࠩࡤࡺࡩࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫᾂ"), bstack111l_opy_ (u"ࠪࡥࡻࡪࡁࡳࡩࡶࠫᾃ"),
  bstack111l_opy_ (u"ࠫࡺࡹࡥࡌࡧࡼࡷࡹࡵࡲࡦࠩᾄ"), bstack111l_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡶ࡫ࠫᾅ"), bstack111l_opy_ (u"࠭࡫ࡦࡻࡶࡸࡴࡸࡥࡑࡣࡶࡷࡼࡵࡲࡥࠩᾆ"),
  bstack111l_opy_ (u"ࠧ࡬ࡧࡼࡅࡱ࡯ࡡࡴࠩᾇ"), bstack111l_opy_ (u"ࠨ࡭ࡨࡽࡕࡧࡳࡴࡹࡲࡶࡩ࠭ᾈ"),
  bstack111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࠫᾉ"), bstack111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡃࡵ࡫ࡸ࠭ᾊ"), bstack111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪࡊࡩࡳࠩᾋ"), bstack111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡇ࡭ࡸ࡯࡮ࡧࡐࡥࡵࡶࡩ࡯ࡩࡉ࡭ࡱ࡫ࠧᾌ"), bstack111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶ࡚ࡹࡥࡔࡻࡶࡸࡪࡳࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪᾍ"),
  bstack111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࠪᾎ"), bstack111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡐࡰࡴࡷࡷࠬᾏ"),
  bstack111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡅ࡫ࡶࡥࡧࡲࡥࡃࡷ࡬ࡰࡩࡉࡨࡦࡥ࡮ࠫᾐ"),
  bstack111l_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࡕ࡫ࡰࡩࡴࡻࡴࠨᾑ"),
  bstack111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡅࡨࡺࡩࡰࡰࠪᾒ"), bstack111l_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡈࡧࡴࡦࡩࡲࡶࡾ࠭ᾓ"), bstack111l_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡌ࡬ࡢࡩࡶࠫᾔ"), bstack111l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡡ࡭ࡋࡱࡸࡪࡴࡴࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᾕ"),
  bstack111l_opy_ (u"ࠨࡦࡲࡲࡹ࡙ࡴࡰࡲࡄࡴࡵࡕ࡮ࡓࡧࡶࡩࡹ࠭ᾖ"),
  bstack111l_opy_ (u"ࠩࡸࡲ࡮ࡩ࡯ࡥࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫᾗ"), bstack111l_opy_ (u"ࠪࡶࡪࡹࡥࡵࡍࡨࡽࡧࡵࡡࡳࡦࠪᾘ"),
  bstack111l_opy_ (u"ࠫࡳࡵࡓࡪࡩࡱࠫᾙ"),
  bstack111l_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩ࡚ࡴࡩ࡮ࡲࡲࡶࡹࡧ࡮ࡵࡘ࡬ࡩࡼࡹࠧᾚ"),
  bstack111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯ࡦࡵࡳ࡮ࡪࡗࡢࡶࡦ࡬ࡪࡸࡳࠨᾛ"),
  bstack111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᾜ"),
  bstack111l_opy_ (u"ࠨࡴࡨࡧࡷ࡫ࡡࡵࡧࡆ࡬ࡷࡵ࡭ࡦࡆࡵ࡭ࡻ࡫ࡲࡔࡧࡶࡷ࡮ࡵ࡮ࡴࠩᾝ"),
  bstack111l_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᾞ"),
  bstack111l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡐࡢࡶ࡫ࠫᾟ"),
  bstack111l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡘࡶࡥࡦࡦࠪᾠ"),
  bstack111l_opy_ (u"ࠬ࡭ࡰࡴࡇࡱࡥࡧࡲࡥࡥࠩᾡ"),
  bstack111l_opy_ (u"࠭ࡩࡴࡊࡨࡥࡩࡲࡥࡴࡵࠪᾢ"),
  bstack111l_opy_ (u"ࠧࡢࡦࡥࡉࡽ࡫ࡣࡕ࡫ࡰࡩࡴࡻࡴࠨᾣ"),
  bstack111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࡔࡥࡵ࡭ࡵࡺࠧᾤ"),
  bstack111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡄࡦࡸ࡬ࡧࡪࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᾥ"),
  bstack111l_opy_ (u"ࠪࡥࡺࡺ࡯ࡈࡴࡤࡲࡹࡖࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠪᾦ"),
  bstack111l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡓࡧࡴࡶࡴࡤࡰࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᾧ"),
  bstack111l_opy_ (u"ࠬࡹࡹࡴࡶࡨࡱࡕࡵࡲࡵࠩᾨ"),
  bstack111l_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡇࡤࡣࡊࡲࡷࡹ࠭ᾩ"),
  bstack111l_opy_ (u"ࠧࡴ࡭࡬ࡴ࡚ࡴ࡬ࡰࡥ࡮ࠫᾪ"), bstack111l_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡕࡻࡳࡩࠬᾫ"), bstack111l_opy_ (u"ࠩࡸࡲࡱࡵࡣ࡬ࡍࡨࡽࠬᾬ"),
  bstack111l_opy_ (u"ࠪࡥࡺࡺ࡯ࡍࡣࡸࡲࡨ࡮ࠧᾭ"),
  bstack111l_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡨࡧࡴࡄࡣࡳࡸࡺࡸࡥࠨᾮ"),
  bstack111l_opy_ (u"ࠬࡻ࡮ࡪࡰࡶࡸࡦࡲ࡬ࡐࡶ࡫ࡩࡷࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧᾯ"),
  bstack111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡗࡪࡰࡧࡳࡼࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࠨᾰ"),
  bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚࡯ࡰ࡮ࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᾱ"),
  bstack111l_opy_ (u"ࠨࡧࡱࡪࡴࡸࡣࡦࡃࡳࡴࡎࡴࡳࡵࡣ࡯ࡰࠬᾲ"),
  bstack111l_opy_ (u"ࠩࡨࡲࡸࡻࡲࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡵࡋࡥࡻ࡫ࡐࡢࡩࡨࡷࠬᾳ"), bstack111l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡈࡪࡼࡴࡰࡱ࡯ࡷࡕࡵࡲࡵࠩᾴ"), bstack111l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨ࡛ࡪࡨࡶࡪࡧࡺࡈࡪࡺࡡࡪ࡮ࡶࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠧ᾵"),
  bstack111l_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡶࡰࡴࡅࡤࡧ࡭࡫ࡌࡪ࡯࡬ࡸࠬᾶ"),
  bstack111l_opy_ (u"࠭ࡣࡢ࡮ࡨࡲࡩࡧࡲࡇࡱࡵࡱࡦࡺࠧᾷ"),
  bstack111l_opy_ (u"ࠧࡣࡷࡱࡨࡱ࡫ࡉࡥࠩᾸ"),
  bstack111l_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᾹ"),
  bstack111l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡊࡴࡡࡣ࡮ࡨࡨࠬᾺ"), bstack111l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࡘ࡫ࡲࡷ࡫ࡦࡩࡸࡇࡵࡵࡪࡲࡶ࡮ࢀࡥࡥࠩΆ"),
  bstack111l_opy_ (u"ࠫࡦࡻࡴࡰࡃࡦࡧࡪࡶࡴࡂ࡮ࡨࡶࡹࡹࠧᾼ"), bstack111l_opy_ (u"ࠬࡧࡵࡵࡱࡇ࡭ࡸࡳࡩࡴࡵࡄࡰࡪࡸࡴࡴࠩ᾽"),
  bstack111l_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡵࡏ࡭ࡧ࠭ι"),
  bstack111l_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡗࡥࡵ࠭᾿"),
  bstack111l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡰ࡬ࡸ࡮ࡧ࡬ࡖࡴ࡯ࠫ῀"), bstack111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡃ࡯ࡰࡴࡽࡐࡰࡲࡸࡴࡸ࠭῁"), bstack111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌ࡫ࡳࡵࡲࡦࡈࡵࡥࡺࡪࡗࡢࡴࡱ࡭ࡳ࡭ࠧῂ"), bstack111l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵ࡫࡮ࡍ࡫ࡱ࡯ࡸࡏ࡮ࡃࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧࠫῃ"),
  bstack111l_opy_ (u"ࠬࡱࡥࡦࡲࡎࡩࡾࡉࡨࡢ࡫ࡱࡷࠬῄ"),
  bstack111l_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࢀࡡࡣ࡮ࡨࡗࡹࡸࡩ࡯ࡩࡶࡈ࡮ࡸࠧ῅"),
  bstack111l_opy_ (u"ࠧࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪῆ"),
  bstack111l_opy_ (u"ࠨ࡫ࡱࡸࡪࡸࡋࡦࡻࡇࡩࡱࡧࡹࠨῇ"),
  bstack111l_opy_ (u"ࠩࡶ࡬ࡴࡽࡉࡐࡕࡏࡳ࡬࠭Ὲ"),
  bstack111l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡗࡹࡸࡡࡵࡧࡪࡽࠬΈ"),
  bstack111l_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡖࡪࡹࡰࡰࡰࡶࡩ࡙࡯࡭ࡦࡱࡸࡸࠬῊ"), bstack111l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࡙ࡤ࡭ࡹ࡚ࡩ࡮ࡧࡲࡹࡹ࠭Ή"),
  bstack111l_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࠩῌ"),
  bstack111l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡴࡻࡱࡧࡊࡾࡥࡤࡷࡷࡩࡋࡸ࡯࡮ࡊࡷࡸࡵࡹࠧ῍"),
  bstack111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡅࡤࡴࡹࡻࡲࡦࠩ῎"),
  bstack111l_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩ῏"),
  bstack111l_opy_ (u"ࠪࡪࡺࡲ࡬ࡄࡱࡱࡸࡪࡾࡴࡍ࡫ࡶࡸࠬῐ"),
  bstack111l_opy_ (u"ࠫࡼࡧࡩࡵࡈࡲࡶࡆࡶࡰࡔࡥࡵ࡭ࡵࡺࠧῑ"),
  bstack111l_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡉ࡯࡯ࡰࡨࡧࡹࡘࡥࡵࡴ࡬ࡩࡸ࠭ῒ"),
  bstack111l_opy_ (u"࠭ࡡࡱࡲࡑࡥࡲ࡫ࠧΐ"),
  bstack111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡔࡎࡆࡩࡷࡺࠧ῔"),
  bstack111l_opy_ (u"ࠨࡶࡤࡴ࡜࡯ࡴࡩࡕ࡫ࡳࡷࡺࡐࡳࡧࡶࡷࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭῕"),
  bstack111l_opy_ (u"ࠩࡶࡧࡦࡲࡥࡇࡣࡦࡸࡴࡸࠧῖ"),
  bstack111l_opy_ (u"ࠪࡻࡩࡧࡌࡰࡥࡤࡰࡕࡵࡲࡵࠩῗ"),
  bstack111l_opy_ (u"ࠫࡸ࡮࡯ࡸ࡚ࡦࡳࡩ࡫ࡌࡰࡩࠪῘ"),
  bstack111l_opy_ (u"ࠬ࡯࡯ࡴࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡹࡸ࡫ࠧῙ"),
  bstack111l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠨῚ"),
  bstack111l_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡷࡸࡽ࡯ࡳࡦࠪΊ"),
  bstack111l_opy_ (u"ࠨࡷࡶࡩࡕࡸࡥࡣࡷ࡬ࡰࡹ࡝ࡄࡂࠩ῜"),
  bstack111l_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶ࡚ࡈࡆࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪ῝"),
  bstack111l_opy_ (u"ࠪࡻࡪࡨࡄࡳ࡫ࡹࡩࡷࡇࡧࡦࡰࡷ࡙ࡷࡲࠧ῞"),
  bstack111l_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡵࡪࠪ῟"),
  bstack111l_opy_ (u"ࠬࡻࡳࡦࡐࡨࡻ࡜ࡊࡁࠨῠ"),
  bstack111l_opy_ (u"࠭ࡷࡥࡣࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩῡ"), bstack111l_opy_ (u"ࠧࡸࡦࡤࡇࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࡔࡪ࡯ࡨࡳࡺࡺࠧῢ"),
  bstack111l_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡏࡳࡩࡌࡨࠬΰ"), bstack111l_opy_ (u"ࠩࡻࡧࡴࡪࡥࡔ࡫ࡪࡲ࡮ࡴࡧࡊࡦࠪῤ"),
  bstack111l_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧ࡛ࡉࡇࡂࡶࡰࡧࡰࡪࡏࡤࠨῥ"),
  bstack111l_opy_ (u"ࠫࡷ࡫ࡳࡦࡶࡒࡲࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡳࡶࡒࡲࡱࡿࠧῦ"),
  bstack111l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹࡹࠧῧ"),
  bstack111l_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡩࡦࡵࠪῨ"), bstack111l_opy_ (u"ࠧࡸࡦࡤࡗࡹࡧࡲࡵࡷࡳࡖࡪࡺࡲࡺࡋࡱࡸࡪࡸࡶࡢ࡮ࠪῩ"),
  bstack111l_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࡊࡤࡶࡩࡽࡡࡳࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫῪ"),
  bstack111l_opy_ (u"ࠩࡰࡥࡽ࡚ࡹࡱ࡫ࡱ࡫ࡋࡸࡥࡲࡷࡨࡲࡨࡿࠧΎ"),
  bstack111l_opy_ (u"ࠪࡷ࡮ࡳࡰ࡭ࡧࡌࡷ࡛࡯ࡳࡪࡤ࡯ࡩࡈ࡮ࡥࡤ࡭ࠪῬ"),
  bstack111l_opy_ (u"ࠫࡺࡹࡥࡄࡣࡵࡸ࡭ࡧࡧࡦࡕࡶࡰࠬ῭"),
  bstack111l_opy_ (u"ࠬࡹࡨࡰࡷ࡯ࡨ࡚ࡹࡥࡔ࡫ࡱ࡫ࡱ࡫ࡴࡰࡰࡗࡩࡸࡺࡍࡢࡰࡤ࡫ࡪࡸࠧ΅"),
  bstack111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡎ࡝ࡄࡑࠩ`"),
  bstack111l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼ࡚࡯ࡶࡥ࡫ࡍࡩࡋ࡮ࡳࡱ࡯ࡰࠬ῰"),
  bstack111l_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡉ࡫ࡧࡨࡪࡴࡁࡱ࡫ࡓࡳࡱ࡯ࡣࡺࡇࡵࡶࡴࡸࠧ῱"),
  bstack111l_opy_ (u"ࠩࡰࡳࡨࡱࡌࡰࡥࡤࡸ࡮ࡵ࡮ࡂࡲࡳࠫῲ"),
  bstack111l_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉࡳࡷࡳࡡࡵࠩῳ"), bstack111l_opy_ (u"ࠫࡱࡵࡧࡤࡣࡷࡊ࡮ࡲࡴࡦࡴࡖࡴࡪࡩࡳࠨῴ"),
  bstack111l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡈࡪࡲࡡࡺࡃࡧࡦࠬ῵"),
  bstack111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡉࡥࡎࡲࡧࡦࡺ࡯ࡳࡃࡸࡸࡴࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠩῶ")
]
bstack1ll11l11ll_opy_ = bstack111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡵࡱ࡮ࡲࡥࡩ࠭ῷ")
bstack1111ll1l11_opy_ = [bstack111l_opy_ (u"ࠨ࠰ࡤࡴࡰ࠭Ὸ"), bstack111l_opy_ (u"ࠩ࠱ࡥࡦࡨࠧΌ"), bstack111l_opy_ (u"ࠪ࠲࡮ࡶࡡࠨῺ")]
bstack11ll111lll_opy_ = [bstack111l_opy_ (u"ࠫ࡮ࡪࠧΏ"), bstack111l_opy_ (u"ࠬࡶࡡࡵࡪࠪῼ"), bstack111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ´"), bstack111l_opy_ (u"ࠧࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩ࠭῾")]
bstack111111ll1l_opy_ = {
  bstack111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ῿"): bstack111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ "),
  bstack111l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ "): bstack111l_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩ "),
  bstack111l_opy_ (u"ࠬ࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ "): bstack111l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ "),
  bstack111l_opy_ (u"ࠧࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ "): bstack111l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ "),
  bstack111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡸ࡮ࡵ࡮ࡴࠩ "): bstack111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ ")
}
bstack1lllllll111_opy_ = [
  bstack111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ "),
  bstack111l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ "),
  bstack111l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ​"),
  bstack111l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭‌"),
  bstack111l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ‍"),
]
bstack1llllllll11_opy_ = bstack1111lllll1_opy_ + bstack11111l11111_opy_ + bstack1l1l11ll1l_opy_
bstack1l11ll1l1l_opy_ = [
  bstack111l_opy_ (u"ࠩࡡࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࠪࠧ‎"),
  bstack111l_opy_ (u"ࠪࡢࡧࡹ࠭࡭ࡱࡦࡥࡱ࠴ࡣࡰ࡯ࠧࠫ‏"),
  bstack111l_opy_ (u"ࠫࡣ࠷࠲࠸࠰ࠪ‐"),
  bstack111l_opy_ (u"ࠬࡤ࠱࠱࠰ࠪ‑"),
  bstack111l_opy_ (u"࠭࡞࠲࠹࠵࠲࠶ࡡ࠶࠮࠻ࡠ࠲ࠬ‒"),
  bstack111l_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠸࡛࠱࠯࠼ࡡ࠳࠭–"),
  bstack111l_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠳࡜࠲࠰࠵ࡢ࠴ࠧ—"),
  bstack111l_opy_ (u"ࠩࡡ࠵࠾࠸࠮࠲࠸࠻࠲ࠬ―")
]
bstack1111l1l1111_opy_ = bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ‖")
bstack111lll111_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡪࡼࡥ࡯ࡶࠪ‗")
bstack1l1ll11lll_opy_ = [ bstack111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ‘") ]
bstack1l1l1l11l_opy_ = [ bstack111l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ’") ]
bstack1ll1ll1l1l_opy_ = [bstack111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ‚")]
bstack111lll1l1l_opy_ = [ bstack111l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ‛") ]
bstack11l1l1l1l_opy_ = bstack111l_opy_ (u"ࠩࡖࡈࡐ࡙ࡥࡵࡷࡳࠫ“")
bstack1l11lllll1_opy_ = bstack111l_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡅࡹࡺࡥ࡮ࡲࡷࡩࡩ࠭”")
bstack11111ll1l1_opy_ = bstack111l_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠨ„")
bstack1l1ll11l11_opy_ = bstack111l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࠫ‟")
bstack11lllllll_opy_ = [
  bstack111l_opy_ (u"࠭ࡅࡓࡔࡢࡊࡆࡏࡌࡆࡆࠪ†"),
  bstack111l_opy_ (u"ࠧࡆࡔࡕࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧ‡"),
  bstack111l_opy_ (u"ࠨࡇࡕࡖࡤࡈࡌࡐࡅࡎࡉࡉࡥࡂ࡚ࡡࡆࡐࡎࡋࡎࡕࠩ•"),
  bstack111l_opy_ (u"ࠩࡈࡖࡗࡥࡎࡆࡖ࡚ࡓࡗࡑ࡟ࡄࡊࡄࡒࡌࡋࡄࠨ‣"),
  bstack111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡊ࡚࡟ࡏࡑࡗࡣࡈࡕࡎࡏࡇࡆࡘࡊࡊࠧ․"),
  bstack111l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡉࡌࡐࡕࡈࡈࠬ‥"),
  bstack111l_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡕࡈࡘࠬ…"),
  bstack111l_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡓࡇࡉ࡙ࡘࡋࡄࠨ‧"),
  bstack111l_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡃࡅࡓࡗ࡚ࡅࡅࠩ "),
  bstack111l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ "),
  bstack111l_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪ‪"),
  bstack111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡋࡑ࡚ࡆࡒࡉࡅࠩ‫"),
  bstack111l_opy_ (u"ࠫࡊࡘࡒࡠࡃࡇࡈࡗࡋࡓࡔࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧ‬"),
  bstack111l_opy_ (u"ࠬࡋࡒࡓࡡࡗ࡙ࡓࡔࡅࡍࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭‭"),
  bstack111l_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪ‮"),
  bstack111l_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ "),
  bstack111l_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡖࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡊࡒࡗ࡙ࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫ‰"),
  bstack111l_opy_ (u"ࠩࡈࡖࡗࡥࡐࡓࡑ࡛࡝ࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ‱"),
  bstack111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡔࡏࡕࡡࡕࡉࡘࡕࡌࡗࡇࡇࠫ′"),
  bstack111l_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡒࡆࡕࡒࡐ࡚࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ″"),
  bstack111l_opy_ (u"ࠬࡋࡒࡓࡡࡐࡅࡓࡊࡁࡕࡑࡕ࡝ࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫ‴"),
]
bstack111llll111_opy_ = bstack111l_opy_ (u"࠭࠮࠰ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡢࡴࡷ࡭࡫ࡧࡣࡵࡵ࠲ࠫ‵")
bstack11ll11l1ll_opy_ = os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠧࡿࠩ‶")), bstack111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ‷"), bstack111l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ‸"))
bstack1111ll1lll1_opy_ = bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲ࡬ࠫ‹")
bstack11111l1l1l1_opy_ = [ bstack111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ›"), bstack111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ※"), bstack111l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ‼"), bstack111l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ‽")]
bstack1llll11l1_opy_ = [ bstack111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ‾"), bstack111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ‿"), bstack111l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ⁀"), bstack111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ⁁"), bstack111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭⁂") ]
bstack11lll1ll11_opy_ = [ bstack111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ⁃"), bstack111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨ⁄") ]
bstack11111l1llll_opy_ = [ bstack111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⁅"), bstack111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ⁆") ]
bstack1l1l1l1l1l_opy_ = 360
bstack1111l11ll1l_opy_ = bstack111l_opy_ (u"ࠥࡥࡵࡶ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥ⁇")
bstack11111ll1lll_opy_ = bstack111l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡩࡴࡵࡸࡩࡸࠨ⁈")
bstack11111l11ll1_opy_ = bstack111l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠣ⁉")
bstack1111l1l1lll_opy_ = bstack111l_opy_ (u"ࠨࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡵࡧࡶࡸࡸࠦࡡࡳࡧࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦ࡯࡯ࠢࡒࡗࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࠥࡴࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩࠥ࡬࡯ࡳࠢࡄࡲࡩࡸ࡯ࡪࡦࠣࡨࡪࡼࡩࡤࡧࡶ࠲ࠧ⁊")
bstack1111l1ll1l1_opy_ = bstack111l_opy_ (u"ࠢ࠲࠳࠱࠴ࠧ⁋")
bstack1lll1llll11_opy_ = {
  bstack111l_opy_ (u"ࠨࡒࡄࡗࡘ࠭⁌"): bstack111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⁍"),
  bstack111l_opy_ (u"ࠪࡊࡆࡏࡌࠨ⁎"): bstack111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⁏"),
  bstack111l_opy_ (u"࡙ࠬࡋࡊࡒࠪ⁐"): bstack111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⁑")
}
bstack11l1ll1ll_opy_ = [
  bstack111l_opy_ (u"ࠢࡨࡧࡷࠦ⁒"),
  bstack111l_opy_ (u"ࠣࡩࡲࡆࡦࡩ࡫ࠣ⁓"),
  bstack111l_opy_ (u"ࠤࡪࡳࡋࡵࡲࡸࡣࡵࡨࠧ⁔"),
  bstack111l_opy_ (u"ࠥࡶࡪ࡬ࡲࡦࡵ࡫ࠦ⁕"),
  bstack111l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ⁖"),
  bstack111l_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ⁗"),
  bstack111l_opy_ (u"ࠨࡳࡶࡤࡰ࡭ࡹࡋ࡬ࡦ࡯ࡨࡲࡹࠨ⁘"),
  bstack111l_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦ⁙"),
  bstack111l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦ⁚"),
  bstack111l_opy_ (u"ࠤࡦࡰࡪࡧࡲࡆ࡮ࡨࡱࡪࡴࡴࠣ⁛"),
  bstack111l_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࡶࠦ⁜"),
  bstack111l_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠦ⁝"),
  bstack111l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࡇࡳࡺࡰࡦࡗࡨࡸࡩࡱࡶࠥ⁞"),
  bstack111l_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧ "),
  bstack111l_opy_ (u"ࠢࡲࡷ࡬ࡸࠧ⁠"),
  bstack111l_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡖࡲࡹࡨ࡮ࡁࡤࡶ࡬ࡳࡳࠨ⁡"),
  bstack111l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡐࡹࡱࡺࡩࡕࡱࡸࡧ࡭ࠨ⁢"),
  bstack111l_opy_ (u"ࠥࡷ࡭ࡧ࡫ࡦࠤ⁣"),
  bstack111l_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡄࡴࡵࠨ⁤")
]
bstack111111ll1ll_opy_ = [
  bstack111l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦ⁥"),
  bstack111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ⁦"),
  bstack111l_opy_ (u"ࠢࡢࡷࡷࡳࠧ⁧"),
  bstack111l_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣ⁨"),
  bstack111l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ⁩")
]
bstack1l11ll11ll_opy_ = {
  bstack111l_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤ⁪"): [bstack111l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ⁫")],
  bstack111l_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ⁬"): [bstack111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ⁭")],
  bstack111l_opy_ (u"ࠢࡢࡷࡷࡳࠧ⁮"): [bstack111l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ⁯"), bstack111l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧ⁰"), bstack111l_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢⁱ"), bstack111l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ⁲")],
  bstack111l_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧ⁳"): [bstack111l_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨ⁴")],
  bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ⁵"): [bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ⁶")],
}
bstack11111ll11ll_opy_ = {
  bstack111l_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣ⁷"): bstack111l_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤ⁸"),
  bstack111l_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣ⁹"): bstack111l_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ⁺"),
  bstack111l_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥ⁻"): bstack111l_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࠤ⁼"),
  bstack111l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦ⁽"): bstack111l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦ⁾"),
  bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧⁿ"): bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ₀")
}
bstack1lll1l1111l_opy_ = {
  bstack111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ₁"): bstack111l_opy_ (u"࠭ࡓࡶ࡫ࡷࡩ࡙ࠥࡥࡵࡷࡳࠫ₂"),
  bstack111l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ₃"): bstack111l_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩ₄"),
  bstack111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ₅"): bstack111l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡕࡨࡸࡺࡶࠧ₆"),
  bstack111l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ₇"): bstack111l_opy_ (u"࡚ࠬࡥࡴࡶࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬ₈")
}
bstack11111l1111l_opy_ = 65536
bstack111111l11ll_opy_ = bstack111l_opy_ (u"࠭࠮࠯࠰࡞ࡘࡗ࡛ࡎࡄࡃࡗࡉࡉࡣࠧ₉")
bstack11111l111l1_opy_ = [
      bstack111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ₊"), bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ₋"), bstack111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ₌"), bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ₍"), bstack111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭₎"),
      bstack111l_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ₏"), bstack111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩₐ"), bstack111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨₑ"), bstack111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩₒ"),
      bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪₓ"), bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬₔ"), bstack111l_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧₕ")
    ]
bstack11111lll1l1_opy_= {
  bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩₖ"): bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪₗ"),
  bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫₘ"): bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬₙ"),
  bstack111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨₚ"): bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧₛ"),
  bstack111l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫₜ"): bstack111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ₝"),
  bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ₞"): bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ₟"),
  bstack111l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ₠"): bstack111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ₡"),
  bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭₢"): bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ₣"),
  bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ₤"): bstack111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ₥"),
  bstack111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ₦"): bstack111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ₧"),
  bstack111l_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ₨"): bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ₩"),
  bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ₪"): bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ₫"),
  bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭€"): bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧ₭"),
  bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ₮"): bstack111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭₯"),
  bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࡒࡴࡹ࡯࡯࡯ࡵࠪ₰"): bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫ₱"),
  bstack111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧ₲"): bstack111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ₳"),
  bstack111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ₴"): bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ₵"),
  bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ₶"): bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ₷"),
  bstack111l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ₸"): bstack111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩ₹"),
  bstack111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ₺"): bstack111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭₻"),
  bstack111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ₼"): bstack111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ₽"),
  bstack111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭₾"): bstack111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ₿"),
  bstack111l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ⃀"): bstack111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ⃁"),
  bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃂"): bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃃"),
  bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⃄"): bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ⃅"),
  bstack111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⃆"): bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⃇"),
  bstack111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⃈"): bstack111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫ⃉"),
  bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ⃊"): bstack111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭⃋"),
  bstack111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ⃌"): bstack111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ⃍")
}
bstack11111lll11l_opy_ = [bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⃎"), bstack111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ⃏")]
bstack1ll1l1l1l_opy_ = (bstack111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢ⃐"),)
bstack111111lll11_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡷࡳࡨࡦࡺࡥࡠࡥ࡯࡭ࠬ⃑")
bstack1l11ll1ll1_opy_ = bstack111l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠲ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠱ࡹ࠵࠴࡭ࡲࡪࡦࡶ࠳⃒ࠧ")
bstack1l11l111l_opy_ = bstack111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬ࡸࡩࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࠤ⃓")
bstack11l1l111l1_opy_ = bstack111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠭ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠧ⃔")
class EVENTS(Enum):
  bstack11111l1l11l_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩ⃕")
  bstack1l11lll1_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳࠫ⃖")
  bstack11l11lllll_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡢ࡮࡬ࡾࡪ࠭⃗")
  bstack11111ll11l1_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࡯ࡳ࡬ࡹ⃘ࠧ")
  bstack11lll11l1l_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯⃙ࠬ") #shift post bstack11111ll111l_opy_
  bstack1ll1l11l1l_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮⃚ࠫ") #shift post bstack11111ll111l_opy_
  bstack11111l111ll_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡮ࡵࡣࠩ⃛") #shift
  bstack11111ll1ll1_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪ⃜") #shift
  bstack1ll11lll1_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨ⃝")
  bstack11ll1lll11l_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡶࡥࡻ࡫࠭ࡳࡧࡶࡹࡱࡺࡳࠨ⃞")
  bstack11l1111111_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡴࡪࡸࡦࡰࡴࡰࡷࡨࡧ࡮ࠨ⃟")
  bstack11l1llll_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡮ࡲࡧࡦࡲࠧ⃠") #shift
  bstack1lll11l1_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡡࡱࡲ࠰ࡹࡵࡲ࡯ࡢࡦࠪ⃡") #shift
  bstack11ll11l11l_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡧ࡮࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠩ⃢")
  bstack1l1lll11ll_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭⃣") #shift
  bstack111lll11_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭⃤") #shift
  bstack11111ll1l11_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ⃥ࠪ") #shift
  bstack11l1l1l1ll1_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ⃦")
  bstack11llllll11_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡶࡸࡦࡺࡵࡴࠩ⃧") #shift
  bstack11111111l1_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶ⃨ࠪ")
  bstack11111l1lll1_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡽࡿ࠭ࡴࡧࡷࡹࡵ࠭⃩") #shift
  bstack11l11lll1l_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡹࡻࡰࠨ⃪")
  bstack11111l1l111_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡲࡦࡶࡳࡩࡱࡷ⃫ࠫ") # not bstack111111lll1l_opy_ in python
  bstack1lll11l1l1_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡶࡻࡩࡵ⃬ࠩ") # used in bstack11111ll1111_opy_
  bstack111l1l111ll_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶࡲࡦ࠯ࡴࡹ࡮ࡺ⃭ࠧ")
  bstack111l1l1l111_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱ࡶࡻࡩࡵ⃮ࠩ")
  bstack1l1l11llll_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡨࡧࡷ⃯ࠫ") # used in bstack11111ll1111_opy_
  bstack111ll1l111_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡪࡲࡳࡰ࠭⃰")
  bstack111l1llll11_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡨࡰࡱ࡮ࠫ⃱")
  bstack111l1lll1ll_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡪࡲࡳࡰ࠭⃲")
  bstack1l1lllll11_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠬ⃳")
  bstack1ll1ll111l_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠬ⃴") #
  bstack11ll11111_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡹࡧ࡫ࡦࡕࡦࡶࡪ࡫࡮ࡔࡪࡲࡸࠬ⃵")
  bstack1l1l1l1lll_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬ⃶")
  bstack11ll11l1l1_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡩ࠲ࡺࡥࡴࡶࠪ⃷")
  bstack11l11l111_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡳࡸࡺ࠭ࡵࡧࡶࡸࠬ⃸")
  bstack1l1l1lll_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡷ࡫࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨ⃹") #shift
  bstack11l11l1l11_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪ⃺") #shift
  bstack111111ll111_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫ⃻")
  bstack11111lll111_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡫ࡧࡰࡪ࠳ࡴࡪ࡯ࡨࡳࡺࡺࠧ⃼")
  bstack1l11ll1ll_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡦࡺ࡬ࡸ࠲࡮ࡡ࡯ࡦ࡯ࡩࡷ࠭⃽")
  bstack1l111l11111_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿࡫ࡸࡪࡶ࠰࡬ࡦࡴࡤ࡭ࡧࡵࠫ⃾")
  bstack111111llll1_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࠭࡮ࡧࡷࡶ࡮ࡩࡳࠨ⃿")
  bstack111111ll1l1_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡩࡷࡥ࠾ࡸࡺ࡯ࡱࠩ℀")
  bstack1l11ll1ll11_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡵࡷࡥࡷࡺࠧ℁")
  bstack111111l1lll_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡧࡳࡼࡴ࡬ࡰࡣࡧࠫℂ")
  bstack111111l1l1l_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡧ࡭࡫ࡣ࡬࠯ࡸࡴࡩࡧࡴࡦࠩ℃")
  bstack1l111llllll_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡣࡱࡲࡸࡸࡺࡲࡢࡲࠪ℄")
  bstack1l111ll1ll1_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡵࡷࡥࡷࡺࡢࡪࡰࡤࡶࡾ࠭℅")
  bstack1l1111lll1l_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡦࡳࡳࡴࡥࡤࡶࠪ℆")
  bstack1l1111ll1ll_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡷࡹࡵࡰࠨℇ")
  bstack1l111l1l1l1_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡸࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭℈")
  bstack1l1111111l1_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩ℉")
  bstack111111lllll_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠪℊ")
  bstack11111l11l11_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡨࡓ࡫ࡡࡳࡧࡶࡸࡍࡻࡢࠨℋ")
  bstack11l11l11ll1_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡉ࡯࡫ࡷࠫℌ")
  bstack11l111l11l1_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡶࡹ࠭ℍ")
  bstack11lll1l1111_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡆࡳࡳ࡬ࡩࡨࠩℎ")
  bstack11111l11l1l_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪℏ")
  bstack11ll1ll1111_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡩࡔࡧ࡯ࡪࡍ࡫ࡡ࡭ࡕࡷࡩࡵ࠭ℐ")
  bstack11ll1ll111l_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡊࡩࡹࡘࡥࡴࡷ࡯ࡸࠬℑ")
  bstack11l1ll11lll_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡅࡷࡧࡱࡸࠬℒ")
  bstack11l1ll1llll_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠫℓ")
  bstack11ll111l111_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡬ࡰࡩࡆࡶࡪࡧࡴࡦࡦࡈࡺࡪࡴࡴࠨ℔")
  bstack111111l11l1_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡦࡰࡴࡹࡪࡻࡥࡕࡧࡶࡸࡊࡼࡥ࡯ࡶࠪℕ")
  bstack11l111llll1_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡴࡶࠧ№")
  bstack1l11l111111_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࡮ࡔࡶࡲࡴࠬ℗")
  bstack111l111l1ll_opy_ = bstack111l_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࡕࡱ࡮ࡲࡥࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪ℘")
  bstack11l1111l_opy_ = bstack111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡱࡨࡋࡻ࡮࡯ࡧ࡯ࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪℙ")
  bstack1l11lll11_opy_ = bstack111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡌࡵ࡯ࡰࡨࡰ࡙࡫ࡳࡵࡅࡲࡱࡵࡲࡥࡵࡧࡧࠫℚ")
  bstack1ll11l1l1l1_opy_ = bstack111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡴࡵࡲࡹࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡐࡺࡶࡨࡷࡹ࠭ℛ")
  bstack1llll1lll1l_opy_ = bstack111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡵࡶ࡬ࡺࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡃࡧ࡫ࡥࡻ࡫ࠧℜ")
  bstack1ll11ll111l_opy_ = bstack111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡴࡒࡼࡸࡪࡹࡴࠨℝ")
  bstack1ll11l11l11_opy_ = bstack111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡹࡵࡧࡶࡸࡌ࡫ࡴࡕࡱࡷࡥࡱ࡚ࡥࡴࡶࡶࠫ℞")
class STAGE(Enum):
  bstack1lllll1l1_opy_ = bstack111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ℟")
  END = bstack111l_opy_ (u"ࠪࡩࡳࡪࠧ℠")
  bstack1l1l11ll11_opy_ = bstack111l_opy_ (u"ࠫࡸ࡯࡮ࡨ࡮ࡨࠫ℡")
bstack11l111llll_opy_ = {
  bstack111l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬ™"): bstack111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭℣"),
  bstack111l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫℤ"): bstack111l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ℥"),
  bstack111l_opy_ (u"ࠩࡅࡉࡍࡇࡖࡆࠩΩ"): bstack111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ℧")
}
PLAYWRIGHT_HUB_URL = bstack111l_opy_ (u"ࠦࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂࠨℨ")
bstack1l11111lll_opy_ = {bstack111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ℩"), bstack111l_opy_ (u"࠭ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠨK"), bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠱ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠭Å")}
MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION = 98
bstack11llll1l1ll_opy_ = 100
bstack1l11111lll_opy_ = (bstack111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨℬ"), bstack111l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠨℭ"), bstack111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮࡫ࡸࡱࠬ℮"))
bstack1ll111lllll_opy_ = {
  bstack111l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪℯ"): bstack111l_opy_ (u"ࠬ࠳࠭ࡳࡧࡵࡹࡳࡹࠧℰ"),
  bstack111l_opy_ (u"࠭ࡤࡦ࡮ࡤࡽࠬℱ"): bstack111l_opy_ (u"ࠧ࠮࠯ࡵࡩࡷࡻ࡮ࡴ࠯ࡧࡩࡱࡧࡹࠨℲ"),
  bstack111l_opy_ (u"ࠨࡴࡨࡶࡺࡴ࠭ࡥࡧ࡯ࡥࡾ࠭ℳ"): 0
}
bstack11111ll1l1l_opy_ = bstack111l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤℴ")
bstack111111ll11l_opy_ = bstack111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢℵ")
bstack1111l1ll_opy_ = bstack111l_opy_ (u"࡙ࠦࡋࡓࡕࠢࡕࡉࡕࡕࡒࡕࡋࡑࡋࠥࡇࡎࡅࠢࡄࡒࡆࡒ࡙ࡕࡋࡆࡗࠧℶ")