# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
import re
from enum import Enum
bstack11lll1lll_opy_ = {
  bstack1l1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᙸ"): bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪᙹ"),
  bstack1l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᙺ"): bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫᙻ"),
  bstack1l1lll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᙼ"): bstack1l1lll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᙽ"),
  bstack1l1lll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᙾ"): bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᙿ"),
  bstack1l1lll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ "): bstack1l1lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨᚁ"),
  bstack1l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᚂ"): bstack1l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨᚃ"),
  bstack1l1lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᚄ"): bstack1l1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᚅ"),
  bstack1l1lll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᚆ"): bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫᚇ"),
  bstack1l1lll_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬᚈ"): bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨᚉ"),
  bstack1l1lll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᚊ"): bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᚋ"),
  bstack1l1lll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᚌ"): bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᚍ"),
  bstack1l1lll_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬᚎ"): bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬᚏ"),
  bstack1l1lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᚐ"): bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᚑ"),
  bstack1l1lll_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᚒ"): bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᚓ"),
  bstack1l1lll_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᚔ"): bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᚕ"),
  bstack1l1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᚖ"): bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᚗ"),
  bstack1l1lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᚘ"): bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᚙ"),
  bstack1l1lll_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪᚚ"): bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪ᚛"),
  bstack1l1lll_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ᚜"): bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ᚝"),
  bstack1l1lll_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨ᚞"): bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨ᚟"),
  bstack1l1lll_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬᚠ"): bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬᚡ"),
  bstack1l1lll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᚢ"): bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᚣ"),
  bstack1l1lll_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ᚤ"): bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭ᚥ"),
  bstack1l1lll_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪᚦ"): bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪᚧ"),
  bstack1l1lll_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᚨ"): bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᚩ"),
  bstack1l1lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᚪ"): bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᚫ"),
  bstack1l1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᚬ"): bstack1l1lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᚭ"),
  bstack1l1lll_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᚮ"): bstack1l1lll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩᚯ"),
  bstack1l1lll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚰ"): bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᚱ"),
  bstack1l1lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᚲ"): bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᚳ"),
  bstack1l1lll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᚴ"): bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᚵ"),
  bstack1l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪᚶ"): bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ᚷ"),
  bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᚸ"): bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᚹ"),
  bstack1l1lll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᚺ"): bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨᚻ"),
  bstack1l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᚼ"): bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᚽ"),
  bstack1l1lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᚾ"): bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᚿ"),
  bstack1l1lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᛀ"): bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᛁ"),
  bstack1l1lll_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᛂ"): bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᛃ"),
  bstack1l1lll_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᛄ"): bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᛅ"),
  bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᛆ"): bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᛇ"),
  bstack1l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᛈ"): bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᛉ")
}
bstack11ll1l111ll_opy_ = [
  bstack1l1lll_opy_ (u"ࠪࡳࡸ࠭ᛊ"),
  bstack1l1lll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᛋ"),
  bstack1l1lll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᛌ"),
  bstack1l1lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᛍ"),
  bstack1l1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᛎ"),
  bstack1l1lll_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᛏ"),
  bstack1l1lll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᛐ"),
]
bstack111111111_opy_ = {
  bstack1l1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᛑ"): [bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᛒ"), bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡑࡅࡒࡋࠧᛓ")],
  bstack1l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᛔ"): bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᛕ"),
  bstack1l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᛖ"): bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬᛗ"),
  bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᛘ"): bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠩᛙ"),
  bstack1l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᛚ"): bstack1l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᛛ"),
  bstack1l1lll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᛜ"): bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡕࡢࡔࡊࡘ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩᛝ"),
  bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᛞ"): bstack1l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨᛟ"),
  bstack1l1lll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᛠ"): bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩᛡ"),
  bstack1l1lll_opy_ (u"࠭ࡡࡱࡲࠪᛢ"): [bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࡢࡍࡉ࠭ᛣ"), bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࠫᛤ")],
  bstack1l1lll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᛥ"): bstack1l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡌࡐࡉࡏࡉ࡛ࡋࡌࠨᛦ"),
  bstack1l1lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᛧ"): bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᛨ"),
  bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᛩ"): bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠫᛪ"),
  bstack1l1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᛫"): bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡘࡖࡇࡕࡓࡄࡃࡏࡉࠬ᛬")
}
bstack1ll11llll1_opy_ = {
  bstack1l1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᛭"): [bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ᛮ"), bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᛯ")],
  bstack1l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᛰ"): [bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡥ࡫ࡦࡻࠪᛱ"), bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᛲ")],
  bstack1l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᛳ"): bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᛴ"),
  bstack1l1lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᛵ"): bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᛶ"),
  bstack1l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᛷ"): bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᛸ"),
  bstack1l1lll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᛹"): [bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡳࡴࠬ᛺"), bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᛻")],
  bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ᛼"): bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ᛽"),
  bstack1l1lll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪ᛾"): bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪ᛿"),
  bstack1l1lll_opy_ (u"ࠨࡣࡳࡴࠬᜀ"): bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴࠬᜁ"),
  bstack1l1lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᜂ"): bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᜃ"),
  bstack1l1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᜄ"): bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᜅ")
}
bstack1l1111111_opy_ = {
  bstack1l1lll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᜆ"): bstack1l1lll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᜇ"),
  bstack1l1lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᜈ"): [bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᜉ"), bstack1l1lll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᜊ")],
  bstack1l1lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᜋ"): bstack1l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᜌ"),
  bstack1l1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᜍ"): bstack1l1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᜎ"),
  bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᜏ"): [bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᜐ"), bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᜑ")],
  bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᜒ"): bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᜓ"),
  bstack1l1lll_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨ᜔ࠫ"): bstack1l1lll_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ᜕࠭"),
  bstack1l1lll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᜖"): [bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᜗"), bstack1l1lll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᜘")],
  bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫ᜙"): [bstack1l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧ᜚"), bstack1l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࠧ᜛")]
}
bstack11l11l11l1_opy_ = [
  bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧ᜜"),
  bstack1l1lll_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬ᜝"),
  bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ᜞"),
  bstack1l1lll_opy_ (u"ࠫࡸ࡫ࡴࡘ࡫ࡱࡨࡴࡽࡒࡦࡥࡷࠫᜟ"),
  bstack1l1lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧᜠ"),
  bstack1l1lll_opy_ (u"࠭ࡳࡵࡴ࡬ࡧࡹࡌࡩ࡭ࡧࡌࡲࡹ࡫ࡲࡢࡥࡷࡥࡧ࡯࡬ࡪࡶࡼࠫᜡ"),
  bstack1l1lll_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪᜢ"),
  bstack1l1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜣ"),
  bstack1l1lll_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧᜤ"),
  bstack1l1lll_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᜥ"),
  bstack1l1lll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᜦ"),
  bstack1l1lll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᜧ"),
]
bstack1l11l1l1ll_opy_ = [
  bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᜨ"),
  bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᜩ"),
  bstack1l1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᜪ"),
  bstack1l1lll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᜫ"),
  bstack1l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᜬ"),
  bstack1l1lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᜭ"),
  bstack1l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᜮ"),
  bstack1l1lll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᜯ"),
  bstack1l1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᜰ"),
  bstack1l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜱ"),
  bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᜲ"),
  bstack1l1lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬᜳ"),
  bstack1l1lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡘࡦ࡭᜴ࠧ"),
  bstack1l1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᜵"),
  bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᜶"),
  bstack1l1lll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ᜷"),
  bstack1l1lll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠷ࠧ᜸"),
  bstack1l1lll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠲ࠨ᜹"),
  bstack1l1lll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠴ࠩ᜺"),
  bstack1l1lll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠶ࠪ᜻"),
  bstack1l1lll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠸ࠫ᜼"),
  bstack1l1lll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠺ࠬ᜽"),
  bstack1l1lll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠼࠭᜾"),
  bstack1l1lll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠾ࠧ᜿"),
  bstack1l1lll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠹ࠨᝀ"),
  bstack1l1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᝁ"),
  bstack1l1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᝂ"),
  bstack1l1lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᝃ"),
  bstack1l1lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᝄ"),
  bstack1l1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᝅ"),
  bstack1l1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬᝆ")
]
bstack11ll1l1l111_opy_ = [
  bstack1l1lll_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧᝇ"),
  bstack1l1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᝈ"),
  bstack1l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᝉ"),
  bstack1l1lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᝊ"),
  bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡔࡷ࡯࡯ࡳ࡫ࡷࡽࠬᝋ"),
  bstack1l1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᝌ"),
  bstack1l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡢࡩࠪᝍ"),
  bstack1l1lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᝎ"),
  bstack1l1lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᝏ"),
  bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᝐ"),
  bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᝑ"),
  bstack1l1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᝒ"),
  bstack1l1lll_opy_ (u"ࠧࡰࡵࠪᝓ"),
  bstack1l1lll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ᝔"),
  bstack1l1lll_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨ᝕"),
  bstack1l1lll_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬ᝖"),
  bstack1l1lll_opy_ (u"ࠫࡷ࡫ࡧࡪࡱࡱࠫ᝗"),
  bstack1l1lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧ᝘"),
  bstack1l1lll_opy_ (u"࠭࡭ࡢࡥ࡫࡭ࡳ࡫ࠧ᝙"),
  bstack1l1lll_opy_ (u"ࠧࡳࡧࡶࡳࡱࡻࡴࡪࡱࡱࠫ᝚"),
  bstack1l1lll_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᝛"),
  bstack1l1lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭᝜"),
  bstack1l1lll_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩ᝝"),
  bstack1l1lll_opy_ (u"ࠫࡳࡵࡐࡢࡩࡨࡐࡴࡧࡤࡕ࡫ࡰࡩࡴࡻࡴࠨ᝞"),
  bstack1l1lll_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭᝟"),
  bstack1l1lll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᝠ"),
  bstack1l1lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᝡ"),
  bstack1l1lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩᝢ"),
  bstack1l1lll_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭ᝣ"),
  bstack1l1lll_opy_ (u"ࠪࡲࡴࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠧᝤ"),
  bstack1l1lll_opy_ (u"ࠫࡨ࡮ࡥࡤ࡭ࡘࡖࡑ࠭ᝥ"),
  bstack1l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᝦ"),
  bstack1l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡉ࡯ࡰ࡭࡬ࡩࡸ࠭ᝧ"),
  bstack1l1lll_opy_ (u"ࠧࡤࡣࡳࡸࡺࡸࡥࡄࡴࡤࡷ࡭࠭ᝨ"),
  bstack1l1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᝩ"),
  bstack1l1lll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᝪ"),
  bstack1l1lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡖࡦࡴࡶ࡭ࡴࡴࠧᝫ"),
  bstack1l1lll_opy_ (u"ࠫࡳࡵࡂ࡭ࡣࡱ࡯ࡕࡵ࡬࡭࡫ࡱ࡫ࠬᝬ"),
  bstack1l1lll_opy_ (u"ࠬࡳࡡࡴ࡭ࡖࡩࡳࡪࡋࡦࡻࡶࠫ᝭"),
  bstack1l1lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡒ࡯ࡨࡵࠪᝮ"),
  bstack1l1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡉࡥࠩᝯ"),
  bstack1l1lll_opy_ (u"ࠨࡦࡨࡨ࡮ࡩࡡࡵࡧࡧࡈࡪࡼࡩࡤࡧࠪᝰ"),
  bstack1l1lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡒࡤࡶࡦࡳࡳࠨ᝱"),
  bstack1l1lll_opy_ (u"ࠪࡴ࡭ࡵ࡮ࡦࡐࡸࡱࡧ࡫ࡲࠨᝲ"),
  bstack1l1lll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩᝳ"),
  bstack1l1lll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡒࡴࡹ࡯࡯࡯ࡵࠪ᝴"),
  bstack1l1lll_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫ᝵"),
  bstack1l1lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ᝶"),
  bstack1l1lll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬ᝷"),
  bstack1l1lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡄ࡬ࡳࡲ࡫ࡴࡳ࡫ࡦࠫ᝸"),
  bstack1l1lll_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࡘ࠵ࠫ᝹"),
  bstack1l1lll_opy_ (u"ࠫࡲ࡯ࡤࡔࡧࡶࡷ࡮ࡵ࡮ࡊࡰࡶࡸࡦࡲ࡬ࡂࡲࡳࡷࠬ᝺"),
  bstack1l1lll_opy_ (u"ࠬ࡫ࡳࡱࡴࡨࡷࡸࡵࡓࡦࡴࡹࡩࡷ࠭᝻"),
  bstack1l1lll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬ᝼"),
  bstack1l1lll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡅࡧࡴࠬ᝽"),
  bstack1l1lll_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨ᝾"),
  bstack1l1lll_opy_ (u"ࠩࡶࡽࡳࡩࡔࡪ࡯ࡨ࡛࡮ࡺࡨࡏࡖࡓࠫ᝿"),
  bstack1l1lll_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨក"),
  bstack1l1lll_opy_ (u"ࠫ࡬ࡶࡳࡍࡱࡦࡥࡹ࡯࡯࡯ࠩខ"),
  bstack1l1lll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭គ"),
  bstack1l1lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ឃ"),
  bstack1l1lll_opy_ (u"ࠧࡧࡱࡵࡧࡪࡉࡨࡢࡰࡪࡩࡏࡧࡲࠨង"),
  bstack1l1lll_opy_ (u"ࠨࡺࡰࡷࡏࡧࡲࠨច"),
  bstack1l1lll_opy_ (u"ࠩࡻࡱࡽࡐࡡࡳࠩឆ"),
  bstack1l1lll_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩជ"),
  bstack1l1lll_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫឈ"),
  bstack1l1lll_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭ញ"),
  bstack1l1lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩដ"),
  bstack1l1lll_opy_ (u"ࠧࡢࡲࡳ࡚ࡪࡸࡳࡪࡱࡱࠫឋ"),
  bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧឌ"),
  bstack1l1lll_opy_ (u"ࠩࡵࡩࡸ࡯ࡧ࡯ࡃࡳࡴࠬឍ"),
  bstack1l1lll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳࡹࠧណ"),
  bstack1l1lll_opy_ (u"ࠫࡨࡧ࡮ࡢࡴࡼࠫត"),
  bstack1l1lll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ថ"),
  bstack1l1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ទ"),
  bstack1l1lll_opy_ (u"ࠧࡪࡧࠪធ"),
  bstack1l1lll_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ន"),
  bstack1l1lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩប"),
  bstack1l1lll_opy_ (u"ࠪࡵࡺ࡫ࡵࡦࠩផ"),
  bstack1l1lll_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ព"),
  bstack1l1lll_opy_ (u"ࠬࡧࡰࡱࡕࡷࡳࡷ࡫ࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳ࠭ភ"),
  bstack1l1lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡉࡡ࡮ࡧࡵࡥࡎࡳࡡࡨࡧࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬម"),
  bstack1l1lll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡊࡾࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪយ"),
  bstack1l1lll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡏ࡮ࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫរ"),
  bstack1l1lll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ល"),
  bstack1l1lll_opy_ (u"ࠪࡶࡪࡹࡥࡳࡸࡨࡈࡪࡼࡩࡤࡧࠪវ"),
  bstack1l1lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫឝ"),
  bstack1l1lll_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧឞ"),
  bstack1l1lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡡࡴࡵࡦࡳࡩ࡫ࠧស"),
  bstack1l1lll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡉࡰࡵࡇࡩࡻ࡯ࡣࡦࡕࡨࡸࡹ࡯࡮ࡨࡵࠪហ"),
  bstack1l1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡷࡧ࡭ࡴࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨឡ"),
  bstack1l1lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡳࡴࡱ࡫ࡐࡢࡻࠪអ"),
  bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫឣ"),
  bstack1l1lll_opy_ (u"ࠫࡼࡪࡩࡰࡕࡨࡶࡻ࡯ࡣࡦࠩឤ"),
  bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧឥ"),
  bstack1l1lll_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡃࡳࡱࡶࡷࡘ࡯ࡴࡦࡖࡵࡥࡨࡱࡩ࡯ࡩࠪឦ"),
  bstack1l1lll_opy_ (u"ࠧࡩ࡫ࡪ࡬ࡈࡵ࡮ࡵࡴࡤࡷࡹ࠭ឧ"),
  bstack1l1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡑࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࡷࠬឨ"),
  bstack1l1lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬឩ"),
  bstack1l1lll_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧឪ"),
  bstack1l1lll_opy_ (u"ࠫࡷ࡫࡭ࡰࡸࡨࡍࡔ࡙ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࡐࡴࡩࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩឫ"),
  bstack1l1lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧឬ"),
  bstack1l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨឭ"),
  bstack1l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩឮ"),
  bstack1l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧឯ"),
  bstack1l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫឰ"),
  bstack1l1lll_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ឱ"),
  bstack1l1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪឲ"),
  bstack1l1lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧឳ"),
  bstack1l1lll_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ឴")
]
bstack1l1l111l_opy_ = {
  bstack1l1lll_opy_ (u"ࠧࡷࠩ឵"): bstack1l1lll_opy_ (u"ࠨࡸࠪា"),
  bstack1l1lll_opy_ (u"ࠩࡩࠫិ"): bstack1l1lll_opy_ (u"ࠪࡪࠬី"),
  bstack1l1lll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪឹ"): bstack1l1lll_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫឺ"),
  bstack1l1lll_opy_ (u"࠭࡯࡯࡮ࡼࡥࡺࡺ࡯࡮ࡣࡷࡩࠬុ"): bstack1l1lll_opy_ (u"ࠧࡰࡰ࡯ࡽࡆࡻࡴࡰ࡯ࡤࡸࡪ࠭ូ"),
  bstack1l1lll_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬួ"): bstack1l1lll_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭ើ"),
  bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭ឿ"): bstack1l1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧៀ"),
  bstack1l1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨេ"): bstack1l1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩែ"),
  bstack1l1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪៃ"): bstack1l1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫោ"),
  bstack1l1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬៅ"): bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ំ"),
  bstack1l1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬះ"): bstack1l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡊࡲࡷࡹ࠭ៈ"),
  bstack1l1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧ៉"): bstack1l1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨ៊"),
  bstack1l1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩ់"): bstack1l1lll_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫ៌"),
  bstack1l1lll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬ៍"): bstack1l1lll_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭៎"),
  bstack1l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭៏"): bstack1l1lll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨ័"),
  bstack1l1lll_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩ៑"): bstack1l1lll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵ្ࠪ"),
  bstack1l1lll_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭៓"): bstack1l1lll_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧ។"),
  bstack1l1lll_opy_ (u"ࠫࡵࡧࡣࡧ࡫࡯ࡩࠬ៕"): bstack1l1lll_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨ៖"),
  bstack1l1lll_opy_ (u"࠭ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨៗ"): bstack1l1lll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ៘"),
  bstack1l1lll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ៙"): bstack1l1lll_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ៚"),
  bstack1l1lll_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫ៛"): bstack1l1lll_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬៜ"),
  bstack1l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ៝"): bstack1l1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ៞"),
  bstack1l1lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩ៟"): bstack1l1lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡳࡩࡦࡺࡥࡳࠩ០")
}
bstack11ll1l1llll_opy_ = bstack1l1lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫࡮ࡺࡨࡶࡤ࠱ࡧࡴࡳ࠯ࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫࠲ࡶࡪࡲࡥࡢࡵࡨࡷ࠴ࡲࡡࡵࡧࡶࡸ࠴ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢ១")
bstack11ll11lllll_opy_ = bstack1l1lll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠲࡬ࡪࡧ࡬ࡵࡪࡦ࡬ࡪࡩ࡫ࠣ២")
bstack11l1lll1_opy_ = bstack1l1lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡫ࡤࡴ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡹࡥ࡯ࡦࡢࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢ៣")
bstack1l1llll1l_opy_ = bstack1l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭៤")
bstack11l1lll11_opy_ = bstack1l1lll_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩ៥")
bstack1l11ll11l1_opy_ = bstack1l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡰࡨࡼࡹࡥࡨࡶࡤࡶࠫ៦")
bstack11ll1l1l1l1_opy_ = {
  bstack1l1lll_opy_ (u"ࠨࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠪ៧"): 50,
  bstack1l1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ៨"): 40,
  bstack1l1lll_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫ៩"): 30,
  bstack1l1lll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ៪"): 20,
  bstack1l1lll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫ៫"): 10
}
bstack1lll1l11l_opy_ = bstack11ll1l1l1l1_opy_[bstack1l1lll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ៬")]
bstack11lll1lll1_opy_ = bstack1l1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭៭")
bstack1ll11lllll_opy_ = bstack1l1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭៮")
bstack11l11l1ll1_opy_ = bstack1l1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ៯")
bstack1l11l11l_opy_ = bstack1l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩ៰")
bstack11ll111ll_opy_ = bstack1l1lll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡧ࡮ࡥࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡵࡧࡣ࡬ࡣࡪࡩࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩ៱")
bstack11ll1l1111l_opy_ = [bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭៲"), bstack1l1lll_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭៳")]
bstack11ll1ll11l1_opy_ = [bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ៴"), bstack1l1lll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ៵")]
bstack1l11ll11_opy_ = re.compile(bstack1l1lll_opy_ (u"ࠩࡡ࡟ࡡࡢࡷ࠮࡟࠮࠾࠳࠰ࠤࠨ៶"))
bstack1l1lll11_opy_ = [
  bstack1l1lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡎࡢ࡯ࡨࠫ៷"),
  bstack1l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭៸"),
  bstack1l1lll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ៹"),
  bstack1l1lll_opy_ (u"࠭࡮ࡦࡹࡆࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪ៺"),
  bstack1l1lll_opy_ (u"ࠧࡢࡲࡳࠫ៻"),
  bstack1l1lll_opy_ (u"ࠨࡷࡧ࡭ࡩ࠭៼"),
  bstack1l1lll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ៽"),
  bstack1l1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࠪ៾"),
  bstack1l1lll_opy_ (u"ࠫࡴࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩ៿"),
  bstack1l1lll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࠪ᠀"),
  bstack1l1lll_opy_ (u"࠭࡮ࡰࡔࡨࡷࡪࡺࠧ᠁"), bstack1l1lll_opy_ (u"ࠧࡧࡷ࡯ࡰࡗ࡫ࡳࡦࡶࠪ᠂"),
  bstack1l1lll_opy_ (u"ࠨࡥ࡯ࡩࡦࡸࡓࡺࡵࡷࡩࡲࡌࡩ࡭ࡧࡶࠫ᠃"),
  bstack1l1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡕ࡫ࡰ࡭ࡳ࡭ࡳࠨ᠄"),
  bstack1l1lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࡌࡰࡩࡪ࡭ࡳ࡭ࠧ᠅"),
  bstack1l1lll_opy_ (u"ࠫࡴࡺࡨࡦࡴࡄࡴࡵࡹࠧ᠆"),
  bstack1l1lll_opy_ (u"ࠬࡶࡲࡪࡰࡷࡔࡦ࡭ࡥࡔࡱࡸࡶࡨ࡫ࡏ࡯ࡈ࡬ࡲࡩࡌࡡࡪ࡮ࡸࡶࡪ࠭᠇"),
  bstack1l1lll_opy_ (u"࠭ࡡࡱࡲࡄࡧࡹ࡯ࡶࡪࡶࡼࠫ᠈"), bstack1l1lll_opy_ (u"ࠧࡢࡲࡳࡔࡦࡩ࡫ࡢࡩࡨࠫ᠉"), bstack1l1lll_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ᠊"), bstack1l1lll_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡓࡥࡨࡱࡡࡨࡧࠪ᠋"), bstack1l1lll_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡈࡺࡸࡡࡵ࡫ࡲࡲࠬ᠌"),
  bstack1l1lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩ᠍"),
  bstack1l1lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡪࡹࡴࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩ᠎"),
  bstack1l1lll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࠨ᠏"), bstack1l1lll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࡇࡱࡨࡎࡴࡴࡦࡰࡷࠫ᠐"),
  bstack1l1lll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᠑"),
  bstack1l1lll_opy_ (u"ࠩࡤࡨࡧࡖ࡯ࡳࡶࠪ᠒"),
  bstack1l1lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡖࡳࡨࡱࡥࡵࠩ᠓"),
  bstack1l1lll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰ࡙࡯࡭ࡦࡱࡸࡸࠬ᠔"),
  bstack1l1lll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡵࡪࠪ᠕"),
  bstack1l1lll_opy_ (u"࠭ࡡࡷࡦࠪ᠖"), bstack1l1lll_opy_ (u"ࠧࡢࡸࡧࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᠗"), bstack1l1lll_opy_ (u"ࠨࡣࡹࡨࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᠘"), bstack1l1lll_opy_ (u"ࠩࡤࡺࡩࡇࡲࡨࡵࠪ᠙"),
  bstack1l1lll_opy_ (u"ࠪࡹࡸ࡫ࡋࡦࡻࡶࡸࡴࡸࡥࠨ᠚"), bstack1l1lll_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡵࡪࠪ᠛"), bstack1l1lll_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡵࡶࡻࡴࡸࡤࠨ᠜"),
  bstack1l1lll_opy_ (u"࠭࡫ࡦࡻࡄࡰ࡮ࡧࡳࠨ᠝"), bstack1l1lll_opy_ (u"ࠧ࡬ࡧࡼࡔࡦࡹࡳࡸࡱࡵࡨࠬ᠞"),
  bstack1l1lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪ᠟"), bstack1l1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡂࡴࡪࡷࠬᠠ"), bstack1l1lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࡉ࡯ࡲࠨᠡ"), bstack1l1lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡆ࡬ࡷࡵ࡭ࡦࡏࡤࡴࡵ࡯࡮ࡨࡈ࡬ࡰࡪ࠭ᠢ"), bstack1l1lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵ࡙ࡸ࡫ࡓࡺࡵࡷࡩࡲࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩᠣ"),
  bstack1l1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࠩᠤ"), bstack1l1lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࡶࠫᠥ"),
  bstack1l1lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡄࡪࡵࡤࡦࡱ࡫ࡂࡶ࡫࡯ࡨࡈ࡮ࡥࡤ࡭ࠪᠦ"),
  bstack1l1lll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࡔࡪ࡯ࡨࡳࡺࡺࠧᠧ"),
  bstack1l1lll_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡄࡧࡹ࡯࡯࡯ࠩᠨ"), bstack1l1lll_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡇࡦࡺࡥࡨࡱࡵࡽࠬᠩ"), bstack1l1lll_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡋࡲࡡࡨࡵࠪᠪ"), bstack1l1lll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࡊࡰࡷࡩࡳࡺࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩᠫ"),
  bstack1l1lll_opy_ (u"ࠧࡥࡱࡱࡸࡘࡺ࡯ࡱࡃࡳࡴࡔࡴࡒࡦࡵࡨࡸࠬᠬ"),
  bstack1l1lll_opy_ (u"ࠨࡷࡱ࡭ࡨࡵࡤࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪᠭ"), bstack1l1lll_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡌࡧࡼࡦࡴࡧࡲࡥࠩᠮ"),
  bstack1l1lll_opy_ (u"ࠪࡲࡴ࡙ࡩࡨࡰࠪᠯ"),
  bstack1l1lll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨ࡙ࡳ࡯࡭ࡱࡱࡵࡸࡦࡴࡴࡗ࡫ࡨࡻࡸ࠭ᠰ"),
  bstack1l1lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡥࡴࡲ࡭ࡩ࡝ࡡࡵࡥ࡫ࡩࡷࡹࠧᠱ"),
  bstack1l1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᠲ"),
  bstack1l1lll_opy_ (u"ࠧࡳࡧࡦࡶࡪࡧࡴࡦࡅ࡫ࡶࡴࡳࡥࡅࡴ࡬ࡺࡪࡸࡓࡦࡵࡶ࡭ࡴࡴࡳࠨᠳ"),
  bstack1l1lll_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧᠴ"),
  bstack1l1lll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡖࡡࡵࡪࠪᠵ"),
  bstack1l1lll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡗࡵ࡫ࡥࡥࠩᠶ"),
  bstack1l1lll_opy_ (u"ࠫ࡬ࡶࡳࡆࡰࡤࡦࡱ࡫ࡤࠨᠷ"),
  bstack1l1lll_opy_ (u"ࠬ࡯ࡳࡉࡧࡤࡨࡱ࡫ࡳࡴࠩᠸ"),
  bstack1l1lll_opy_ (u"࠭ࡡࡥࡤࡈࡼࡪࡩࡔࡪ࡯ࡨࡳࡺࡺࠧᠹ"),
  bstack1l1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ᠺ"),
  bstack1l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡊࡥࡷ࡫ࡦࡩࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬᠻ"),
  bstack1l1lll_opy_ (u"ࠩࡤࡹࡹࡵࡇࡳࡣࡱࡸࡕ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠩᠼ"),
  bstack1l1lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡒࡦࡺࡵࡳࡣ࡯ࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᠽ"),
  bstack1l1lll_opy_ (u"ࠫࡸࡿࡳࡵࡧࡰࡔࡴࡸࡴࠨᠾ"),
  bstack1l1lll_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡪࡢࡉࡱࡶࡸࠬᠿ"),
  bstack1l1lll_opy_ (u"࠭ࡳ࡬࡫ࡳ࡙ࡳࡲ࡯ࡤ࡭ࠪᡀ"), bstack1l1lll_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡔࡺࡲࡨࠫᡁ"), bstack1l1lll_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡌࡧࡼࠫᡂ"),
  bstack1l1lll_opy_ (u"ࠩࡤࡹࡹࡵࡌࡢࡷࡱࡧ࡭࠭ᡃ"),
  bstack1l1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡧࡦࡺࡃࡢࡲࡷࡹࡷ࡫ࠧᡄ"),
  bstack1l1lll_opy_ (u"ࠫࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࡏࡵࡪࡨࡶࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ᡅ"),
  bstack1l1lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪ࡝ࡩ࡯ࡦࡲࡻࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࠧᡆ"),
  bstack1l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡵ࡯࡭ࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᡇ"),
  bstack1l1lll_opy_ (u"ࠧࡦࡰࡩࡳࡷࡩࡥࡂࡲࡳࡍࡳࡹࡴࡢ࡮࡯ࠫᡈ"),
  bstack1l1lll_opy_ (u"ࠨࡧࡱࡷࡺࡸࡥࡘࡧࡥࡺ࡮࡫ࡷࡴࡊࡤࡺࡪࡖࡡࡨࡧࡶࠫᡉ"), bstack1l1lll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡇࡩࡻࡺ࡯ࡰ࡮ࡶࡔࡴࡸࡴࠨᡊ"), bstack1l1lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧ࡚ࡩࡧࡼࡩࡦࡹࡇࡩࡹࡧࡩ࡭ࡵࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠭ᡋ"),
  bstack1l1lll_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡵࡶࡳࡄࡣࡦ࡬ࡪࡒࡩ࡮࡫ࡷࠫᡌ"),
  bstack1l1lll_opy_ (u"ࠬࡩࡡ࡭ࡧࡱࡨࡦࡸࡆࡰࡴࡰࡥࡹ࠭ᡍ"),
  bstack1l1lll_opy_ (u"࠭ࡢࡶࡰࡧࡰࡪࡏࡤࠨᡎ"),
  bstack1l1lll_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧᡏ"),
  bstack1l1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡉࡳࡧࡢ࡭ࡧࡧࠫᡐ"), bstack1l1lll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡆࡻࡴࡩࡱࡵ࡭ࡿ࡫ࡤࠨᡑ"),
  bstack1l1lll_opy_ (u"ࠪࡥࡺࡺ࡯ࡂࡥࡦࡩࡵࡺࡁ࡭ࡧࡵࡸࡸ࠭ᡒ"), bstack1l1lll_opy_ (u"ࠫࡦࡻࡴࡰࡆ࡬ࡷࡲ࡯ࡳࡴࡃ࡯ࡩࡷࡺࡳࠨᡓ"),
  bstack1l1lll_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡴࡎ࡬ࡦࠬᡔ"),
  bstack1l1lll_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡖࡤࡴࠬᡕ"),
  bstack1l1lll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉ࡯࡫ࡷ࡭ࡦࡲࡕࡳ࡮ࠪᡖ"), bstack1l1lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡂ࡮࡯ࡳࡼࡖ࡯ࡱࡷࡳࡷࠬᡗ"), bstack1l1lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡪࡲࡴࡸࡥࡇࡴࡤࡹࡩ࡝ࡡࡳࡰ࡬ࡲ࡬࠭ᡘ"), bstack1l1lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡪࡴࡌࡪࡰ࡮ࡷࡎࡴࡂࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠪᡙ"),
  bstack1l1lll_opy_ (u"ࠫࡰ࡫ࡥࡱࡍࡨࡽࡈ࡮ࡡࡪࡰࡶࠫᡚ"),
  bstack1l1lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡿࡧࡢ࡭ࡧࡖࡸࡷ࡯࡮ࡨࡵࡇ࡭ࡷ࠭ᡛ"),
  bstack1l1lll_opy_ (u"࠭ࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩᡜ"),
  bstack1l1lll_opy_ (u"ࠧࡪࡰࡷࡩࡷࡑࡥࡺࡆࡨࡰࡦࡿࠧᡝ"),
  bstack1l1lll_opy_ (u"ࠨࡵ࡫ࡳࡼࡏࡏࡔࡎࡲ࡫ࠬᡞ"),
  bstack1l1lll_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡖࡸࡷࡧࡴࡦࡩࡼࠫᡟ"),
  bstack1l1lll_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡕࡩࡸࡶ࡯࡯ࡵࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᡠ"), bstack1l1lll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡘࡣ࡬ࡸ࡙࡯࡭ࡦࡱࡸࡸࠬᡡ"),
  bstack1l1lll_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࠨᡢ"),
  bstack1l1lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡳࡺࡰࡦࡉࡽ࡫ࡣࡶࡶࡨࡊࡷࡵ࡭ࡉࡶࡷࡴࡸ࠭ᡣ"),
  bstack1l1lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡄࡣࡳࡸࡺࡸࡥࠨᡤ"),
  bstack1l1lll_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨᡥ"),
  bstack1l1lll_opy_ (u"ࠩࡩࡹࡱࡲࡃࡰࡰࡷࡩࡽࡺࡌࡪࡵࡷࠫᡦ"),
  bstack1l1lll_opy_ (u"ࠪࡻࡦ࡯ࡴࡇࡱࡵࡅࡵࡶࡓࡤࡴ࡬ࡴࡹ࠭ᡧ"),
  bstack1l1lll_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡈࡵ࡮࡯ࡧࡦࡸࡗ࡫ࡴࡳ࡫ࡨࡷࠬᡨ"),
  bstack1l1lll_opy_ (u"ࠬࡧࡰࡱࡐࡤࡱࡪ࠭ᡩ"),
  bstack1l1lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡓࡍࡅࡨࡶࡹ࠭ᡪ"),
  bstack1l1lll_opy_ (u"ࠧࡵࡣࡳ࡛࡮ࡺࡨࡔࡪࡲࡶࡹࡖࡲࡦࡵࡶࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᡫ"),
  bstack1l1lll_opy_ (u"ࠨࡵࡦࡥࡱ࡫ࡆࡢࡥࡷࡳࡷ࠭ᡬ"),
  bstack1l1lll_opy_ (u"ࠩࡺࡨࡦࡒ࡯ࡤࡣ࡯ࡔࡴࡸࡴࠨᡭ"),
  bstack1l1lll_opy_ (u"ࠪࡷ࡭ࡵࡷ࡙ࡥࡲࡨࡪࡒ࡯ࡨࠩᡮ"),
  bstack1l1lll_opy_ (u"ࠫ࡮ࡵࡳࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡸࡷࡪ࠭ᡯ"),
  bstack1l1lll_opy_ (u"ࠬࡾࡣࡰࡦࡨࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠧᡰ"),
  bstack1l1lll_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡶࡷࡼࡵࡲࡥࠩᡱ"),
  bstack1l1lll_opy_ (u"ࠧࡶࡵࡨࡔࡷ࡫ࡢࡶ࡫࡯ࡸ࡜ࡊࡁࠨᡲ"),
  bstack1l1lll_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵ࡙ࡇࡅࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠩᡳ"),
  bstack1l1lll_opy_ (u"ࠩࡺࡩࡧࡊࡲࡪࡸࡨࡶࡆ࡭ࡥ࡯ࡶࡘࡶࡱ࠭ᡴ"),
  bstack1l1lll_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡴࡩࠩᡵ"),
  bstack1l1lll_opy_ (u"ࠫࡺࡹࡥࡏࡧࡺ࡛ࡉࡇࠧᡶ"),
  bstack1l1lll_opy_ (u"ࠬࡽࡤࡢࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᡷ"), bstack1l1lll_opy_ (u"࠭ࡷࡥࡣࡆࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᡸ"),
  bstack1l1lll_opy_ (u"ࠧࡹࡥࡲࡨࡪࡕࡲࡨࡋࡧࠫ᡹"), bstack1l1lll_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡓࡪࡩࡱ࡭ࡳ࡭ࡉࡥࠩ᡺"),
  bstack1l1lll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦ࡚ࡈࡆࡈࡵ࡯ࡦ࡯ࡩࡎࡪࠧ᡻"),
  bstack1l1lll_opy_ (u"ࠪࡶࡪࡹࡥࡵࡑࡱࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡲࡵࡑࡱࡰࡾ࠭᡼"),
  bstack1l1lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࡸ࠭᡽"),
  bstack1l1lll_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷ࡯ࡥࡴࠩ᡾"), bstack1l1lll_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡹࡊࡰࡷࡩࡷࡼࡡ࡭ࠩ᡿"),
  bstack1l1lll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࡉࡣࡵࡨࡼࡧࡲࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪᢀ"),
  bstack1l1lll_opy_ (u"ࠨ࡯ࡤࡼ࡙ࡿࡰࡪࡰࡪࡊࡷ࡫ࡱࡶࡧࡱࡧࡾ࠭ᢁ"),
  bstack1l1lll_opy_ (u"ࠩࡶ࡭ࡲࡶ࡬ࡦࡋࡶ࡚࡮ࡹࡩࡣ࡮ࡨࡇ࡭࡫ࡣ࡬ࠩᢂ"),
  bstack1l1lll_opy_ (u"ࠪࡹࡸ࡫ࡃࡢࡴࡷ࡬ࡦ࡭ࡥࡔࡵ࡯ࠫᢃ"),
  bstack1l1lll_opy_ (u"ࠫࡸ࡮࡯ࡶ࡮ࡧ࡙ࡸ࡫ࡓࡪࡰࡪࡰࡪࡺ࡯࡯ࡖࡨࡷࡹࡓࡡ࡯ࡣࡪࡩࡷ࠭ᢄ"),
  bstack1l1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡍ࡜ࡊࡐࠨᢅ"),
  bstack1l1lll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙ࡵࡵࡤࡪࡌࡨࡊࡴࡲࡰ࡮࡯ࠫᢆ"),
  bstack1l1lll_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡈࡪࡦࡧࡩࡳࡇࡰࡪࡒࡲࡰ࡮ࡩࡹࡆࡴࡵࡳࡷ࠭ᢇ"),
  bstack1l1lll_opy_ (u"ࠨ࡯ࡲࡧࡰࡒ࡯ࡤࡣࡷ࡭ࡴࡴࡁࡱࡲࠪᢈ"),
  bstack1l1lll_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈࡲࡶࡲࡧࡴࠨᢉ"), bstack1l1lll_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉ࡭ࡱࡺࡥࡳࡕࡳࡩࡨࡹࠧᢊ"),
  bstack1l1lll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡇࡩࡱࡧࡹࡂࡦࡥࠫᢋ"),
  bstack1l1lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡏࡤࡍࡱࡦࡥࡹࡵࡲࡂࡷࡷࡳࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠨᢌ")
]
bstack1111llll1_opy_ = bstack1l1lll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡻࡰ࡭ࡱࡤࡨࠬᢍ")
bstack1l1l111l11_opy_ = [bstack1l1lll_opy_ (u"ࠧ࠯ࡣࡳ࡯ࠬᢎ"), bstack1l1lll_opy_ (u"ࠨ࠰ࡤࡥࡧ࠭ᢏ"), bstack1l1lll_opy_ (u"ࠩ࠱࡭ࡵࡧࠧᢐ")]
bstack1ll11l11l_opy_ = [bstack1l1lll_opy_ (u"ࠪ࡭ࡩ࠭ᢑ"), bstack1l1lll_opy_ (u"ࠫࡵࡧࡴࡩࠩᢒ"), bstack1l1lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨᢓ"), bstack1l1lll_opy_ (u"࠭ࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࠬᢔ")]
bstack111llll1_opy_ = {
  bstack1l1lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᢕ"): bstack1l1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢖ"),
  bstack1l1lll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪᢗ"): bstack1l1lll_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᢘ"),
  bstack1l1lll_opy_ (u"ࠫࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢙ"): bstack1l1lll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢚ"),
  bstack1l1lll_opy_ (u"࠭ࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢛ"): bstack1l1lll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢜ"),
  bstack1l1lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡷ࡭ࡴࡴࡳࠨᢝ"): bstack1l1lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᢞ")
}
bstack1l1ll1lll_opy_ = [
  bstack1l1lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᢟ"),
  bstack1l1lll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢠ"),
  bstack1l1lll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢡ"),
  bstack1l1lll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬᢢ"),
  bstack1l1lll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨᢣ"),
]
bstack1lllllll1_opy_ = bstack1l11l1l1ll_opy_ + bstack11ll1l1l111_opy_ + bstack1l1lll11_opy_
bstack11ll1l11l1_opy_ = [
  bstack1l1lll_opy_ (u"ࠨࡠ࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸࠩ࠭ᢤ"),
  bstack1l1lll_opy_ (u"ࠩࡡࡦࡸ࠳࡬ࡰࡥࡤࡰ࠳ࡩ࡯࡮ࠦࠪᢥ"),
  bstack1l1lll_opy_ (u"ࠪࡢ࠶࠸࠷࠯ࠩᢦ"),
  bstack1l1lll_opy_ (u"ࠫࡣ࠷࠰࠯ࠩᢧ"),
  bstack1l1lll_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠵ࡠ࠼࠭࠺࡟࠱ࠫᢨ"),
  bstack1l1lll_opy_ (u"࠭࡞࠲࠹࠵࠲࠷ࡡ࠰࠮࠻ࡠ࠲ᢩࠬ"),
  bstack1l1lll_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠹࡛࠱࠯࠴ࡡ࠳࠭ᢪ"),
  bstack1l1lll_opy_ (u"ࠨࡠ࠴࠽࠷࠴࠱࠷࠺࠱ࠫ᢫")
]
bstack11ll1l1ll1l_opy_ = bstack1l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ᢬")
bstack1ll11ll1l_opy_ = bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠯ࡷ࠳࠲ࡩࡻ࡫࡮ࡵࠩ᢭")
bstack111111l1l_opy_ = [ bstack1l1lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᢮") ]
bstack1llll1111l_opy_ = [ bstack1l1lll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᢯") ]
bstack1ll11l1111_opy_ = [bstack1l1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᢰ")]
bstack11111111_opy_ = [ bstack1l1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᢱ") ]
bstack1l1ll11ll1_opy_ = bstack1l1lll_opy_ (u"ࠨࡕࡇࡏࡘ࡫ࡴࡶࡲࠪᢲ")
bstack11111lll_opy_ = bstack1l1lll_opy_ (u"ࠩࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠬᢳ")
bstack1111l11ll_opy_ = bstack1l1lll_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠧᢴ")
bstack1l11l1llll_opy_ = bstack1l1lll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࠪᢵ")
bstack1l1l1l11l1_opy_ = [
  bstack1l1lll_opy_ (u"ࠬࡋࡒࡓࡡࡉࡅࡎࡒࡅࡅࠩᢶ"),
  bstack1l1lll_opy_ (u"࠭ࡅࡓࡔࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ᢷ"),
  bstack1l1lll_opy_ (u"ࠧࡆࡔࡕࡣࡇࡒࡏࡄࡍࡈࡈࡤࡈ࡙ࡠࡅࡏࡍࡊࡔࡔࠨᢸ"),
  bstack1l1lll_opy_ (u"ࠨࡇࡕࡖࡤࡔࡅࡕ࡙ࡒࡖࡐࡥࡃࡉࡃࡑࡋࡊࡊࠧᢹ"),
  bstack1l1lll_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡉ࡙ࡥࡎࡐࡖࡢࡇࡔࡔࡎࡆࡅࡗࡉࡉ࠭ᢺ"),
  bstack1l1lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡈࡒࡏࡔࡇࡇࠫᢻ"),
  bstack1l1lll_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡘࡅࡔࡇࡗࠫᢼ"),
  bstack1l1lll_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡈࡘࡗࡊࡊࠧᢽ"),
  bstack1l1lll_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡂࡄࡒࡖ࡙ࡋࡄࠨᢾ"),
  bstack1l1lll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᢿ"),
  bstack1l1lll_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡒࡔ࡚࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࠩᣀ"),
  bstack1l1lll_opy_ (u"ࠩࡈࡖࡗࡥࡁࡅࡆࡕࡉࡘ࡙࡟ࡊࡐ࡙ࡅࡑࡏࡄࠨᣁ"),
  bstack1l1lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡗࡑࡖࡊࡇࡃࡉࡃࡅࡐࡊ࠭ᣂ"),
  bstack1l1lll_opy_ (u"ࠫࡊࡘࡒࡠࡖࡘࡒࡓࡋࡌࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬᣃ"),
  bstack1l1lll_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡔࡊࡏࡈࡈࡤࡕࡕࡕࠩᣄ"),
  bstack1l1lll_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡔࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᣅ"),
  bstack1l1lll_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡉࡑࡖࡘࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪᣆ"),
  bstack1l1lll_opy_ (u"ࠨࡇࡕࡖࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᣇ"),
  bstack1l1lll_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪᣈ"),
  bstack1l1lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡘࡅࡔࡑࡏ࡙࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᣉ"),
  bstack1l1lll_opy_ (u"ࠫࡊࡘࡒࡠࡏࡄࡒࡉࡇࡔࡐࡔ࡜ࡣࡕࡘࡏ࡙࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᣊ"),
]
bstack11ll1llll1_opy_ = bstack1l1lll_opy_ (u"ࠬ࠴࠯ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠱ࠪᣋ")
bstack111l11lll_opy_ = os.path.join(os.path.expanduser(bstack1l1lll_opy_ (u"࠭ࡾࠨᣌ")), bstack1l1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᣍ"), bstack1l1lll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᣎ"))
bstack11llll1llll_opy_ = bstack1l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱ࡫ࠪᣏ")
bstack11ll1lll111_opy_ = [ bstack1l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᣐ"), bstack1l1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᣑ"), bstack1l1lll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫᣒ"), bstack1l1lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᣓ")]
bstack1l111l111l_opy_ = [ bstack1l1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᣔ"), bstack1l1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᣕ"), bstack1l1lll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨᣖ"), bstack1l1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᣗ") ]
bstack1ll1l1l1l_opy_ = [ bstack1l1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᣘ") ]
bstack111ll111_opy_ = 360
bstack11lll1l11ll_opy_ = bstack1l1lll_opy_ (u"ࠧࡧࡰࡱ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧᣙ")
bstack11ll1l111l1_opy_ = bstack1l1lll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡫ࡶࡷࡺ࡫ࡳࠣᣚ")
bstack11ll1ll1ll1_opy_ = bstack1l1lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠥᣛ")
bstack11llll11ll1_opy_ = bstack1l1lll_opy_ (u"ࠣࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡷࡩࡸࡺࡳࠡࡣࡵࡩࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡔ࡙ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠧࡶࠤࡦࡴࡤࠡࡣࡥࡳࡻ࡫ࠠࡧࡱࡵࠤࡆࡴࡤࡳࡱ࡬ࡨࠥࡪࡥࡷ࡫ࡦࡩࡸ࠴ࠢᣜ")
bstack11lll1lll11_opy_ = bstack1l1lll_opy_ (u"ࠤ࠴࠵࠳࠶ࠢᣝ")
bstack111ll1l1ll_opy_ = {
  bstack1l1lll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨᣞ"): bstack1l1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᣟ"),
  bstack1l1lll_opy_ (u"ࠬࡌࡁࡊࡎࠪᣠ"): bstack1l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᣡ"),
  bstack1l1lll_opy_ (u"ࠧࡔࡍࡌࡔࠬᣢ"): bstack1l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᣣ")
}
bstack11l11l1l1_opy_ = [
  bstack1l1lll_opy_ (u"ࠤࡪࡩࡹࠨᣤ"),
  bstack1l1lll_opy_ (u"ࠥ࡫ࡴࡈࡡࡤ࡭ࠥᣥ"),
  bstack1l1lll_opy_ (u"ࠦ࡬ࡵࡆࡰࡴࡺࡥࡷࡪࠢᣦ"),
  bstack1l1lll_opy_ (u"ࠧࡸࡥࡧࡴࡨࡷ࡭ࠨᣧ"),
  bstack1l1lll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧᣨ"),
  bstack1l1lll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᣩ"),
  bstack1l1lll_opy_ (u"ࠣࡵࡸࡦࡲ࡯ࡴࡆ࡮ࡨࡱࡪࡴࡴࠣᣪ"),
  bstack1l1lll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨᣫ"),
  bstack1l1lll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨᣬ"),
  bstack1l1lll_opy_ (u"ࠦࡨࡲࡥࡢࡴࡈࡰࡪࡳࡥ࡯ࡶࠥᣭ"),
  bstack1l1lll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࡸࠨᣮ"),
  bstack1l1lll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹࠨᣯ"),
  bstack1l1lll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡂࡵࡼࡲࡨ࡙ࡣࡳ࡫ࡳࡸࠧᣰ"),
  bstack1l1lll_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢᣱ"),
  bstack1l1lll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᣲ"),
  bstack1l1lll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡘࡴࡻࡣࡩࡃࡦࡸ࡮ࡵ࡮ࠣᣳ"),
  bstack1l1lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡒࡻ࡬ࡵ࡫ࡗࡳࡺࡩࡨࠣᣴ"),
  bstack1l1lll_opy_ (u"ࠧࡹࡨࡢ࡭ࡨࠦᣵ"),
  bstack1l1lll_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࡆࡶࡰࠣ᣶")
]
bstack11ll1ll11ll_opy_ = [
  bstack1l1lll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨ᣷"),
  bstack1l1lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᣸"),
  bstack1l1lll_opy_ (u"ࠤࡤࡹࡹࡵࠢ᣹"),
  bstack1l1lll_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥ᣺"),
  bstack1l1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᣻")
]
bstack111l1lll_opy_ = {
  bstack1l1lll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦ᣼"): [bstack1l1lll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ᣽")],
  bstack1l1lll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᣾"): [bstack1l1lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᣿")],
  bstack1l1lll_opy_ (u"ࠤࡤࡹࡹࡵࠢᤀ"): [bstack1l1lll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢᤁ"), bstack1l1lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢᤂ"), bstack1l1lll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᤃ"), bstack1l1lll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧᤄ")],
  bstack1l1lll_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢᤅ"): [bstack1l1lll_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣᤆ")],
  bstack1l1lll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᤇ"): [bstack1l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᤈ")],
}
bstack11ll1l1ll11_opy_ = {
  bstack1l1lll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥᤉ"): bstack1l1lll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦᤊ"),
  bstack1l1lll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᤋ"): bstack1l1lll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᤌ"),
  bstack1l1lll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧᤍ"): bstack1l1lll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦᤎ"),
  bstack1l1lll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨᤏ"): bstack1l1lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨᤐ"),
  bstack1l1lll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᤑ"): bstack1l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᤒ")
}
bstack111l11ll1l_opy_ = {
  bstack1l1lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᤓ"): bstack1l1lll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡔࡧࡷࡹࡵ࠭ᤔ"),
  bstack1l1lll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᤕ"): bstack1l1lll_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡗࡩࡦࡸࡤࡰࡹࡱࠫᤖ"),
  bstack1l1lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᤗ"): bstack1l1lll_opy_ (u"࡚ࠬࡥࡴࡶࠣࡗࡪࡺࡵࡱࠩᤘ"),
  bstack1l1lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᤙ"): bstack1l1lll_opy_ (u"ࠧࡕࡧࡶࡸ࡚ࠥࡥࡢࡴࡧࡳࡼࡴࠧᤚ")
}
bstack11ll1l11l11_opy_ = 65536
bstack11ll1l1lll1_opy_ = bstack1l1lll_opy_ (u"ࠨ࠰࠱࠲ࡠ࡚ࡒࡖࡐࡆࡅ࡙ࡋࡄ࡞ࠩᤛ")
bstack11ll1l1l1ll_opy_ = [
      bstack1l1lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᤜ"), bstack1l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᤝ"), bstack1l1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᤞ"), bstack1l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ᤟"), bstack1l1lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨᤠ"),
      bstack1l1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᤡ"), bstack1l1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫᤢ"), bstack1l1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᤣ"), bstack1l1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫᤤ"),
      bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᤥ"), bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᤦ"), bstack1l1lll_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩᤧ")
    ]
bstack11ll11lll1l_opy_= {
  bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᤨ"): bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᤩ"),
  bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᤪ"): bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᤫ"),
  bstack1l1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ᤬"): bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᤭"),
  bstack1l1lll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭᤮"): bstack1l1lll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᤯"),
  bstack1l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᤰ"): bstack1l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᤱ"),
  bstack1l1lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᤲ"): bstack1l1lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᤳ"),
  bstack1l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᤴ"): bstack1l1lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᤵ"),
  bstack1l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᤶ"): bstack1l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᤷ"),
  bstack1l1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᤸ"): bstack1l1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ᤹࠭"),
  bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᤺"): bstack1l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵ᤻ࠪ"),
  bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᤼"): bstack1l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ᤽"),
  bstack1l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᤾"): bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᤿"),
  bstack1l1lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬ᥀"): bstack1l1lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭᥁"),
  bstack1l1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᥂"): bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᥃"),
  bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᥄"): bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᥅"),
  bstack1l1lll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭᥆"): bstack1l1lll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧ᥇"),
  bstack1l1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ᥈"): bstack1l1lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᥉"),
  bstack1l1lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬ᥊"): bstack1l1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᥋"),
  bstack1l1lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫ᥌"): bstack1l1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ᥍"),
  bstack1l1lll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ᥎"): bstack1l1lll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭᥏"),
  bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᥐ"): bstack1l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᥑ"),
  bstack1l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᥒ"): bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᥓ"),
  bstack1l1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᥔ"): bstack1l1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᥕ"),
  bstack1l1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᥖ"): bstack1l1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᥗ"),
  bstack1l1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᥘ"): bstack1l1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᥙ")
}
bstack11ll1lll1ll_opy_ = [bstack1l1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᥚ"), bstack1l1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᥛ")]
bstack1ll11l11ll_opy_ = (bstack1l1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᥜ"),)
bstack11ll1lllll1_opy_ = bstack1l1lll_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡺࡶࡤࡢࡶࡨࡣࡨࡲࡩࠨᥝ")
bstack1lll1ll1l_opy_ = bstack1l1lll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡩࡵ࡭ࡩࡹ࠯ࠣᥞ")
bstack1111lll1l_opy_ = bstack1l1lll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨࡴ࡬ࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡤࡷ࡭ࡨ࡯ࡢࡴࡧ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࠧᥟ")
bstack1l11111ll_opy_ = bstack1l1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠰ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠣᥠ")
class EVENTS(Enum):
  bstack11ll1l11111_opy_ = bstack1l1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࠱࠲ࡻ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬᥡ")
  bstack1l11l111l1_opy_ = bstack1l1lll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࠧᥢ") # final bstack11ll1l11lll_opy_
  bstack11ll1llll1l_opy_ = bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡱࡨࡱࡵࡧࡴࠩᥣ")
  bstack1111ll11l_opy_ = bstack1l1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠿ࡶࡲࡪࡰࡷ࠱ࡧࡻࡩ࡭ࡦ࡯࡭ࡳࡱࠧᥤ") #shift post bstack11ll1ll1111_opy_
  bstack1ll1l1ll1_opy_ = bstack1l1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭ᥥ") #shift post bstack11ll1ll1111_opy_
  bstack11ll1llllll_opy_ = bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡩࡷࡥࠫᥦ") #shift
  bstack11ll11llll1_opy_ = bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡨࡴࡽ࡮࡭ࡱࡤࡨࠬᥧ") #shift
  bstack11llll1l1_opy_ = bstack1l1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪᥨ")
  bstack1ll1l1ll1ll_opy_ = bstack1l1lll_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾ࡸࡧࡶࡦ࠯ࡵࡩࡸࡻ࡬ࡵࡵࠪᥩ")
  bstack1ll11l1l11_opy_ = bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡶࡥࡳࡨࡲࡶࡲࡹࡣࡢࡰࠪᥪ")
  bstack1llllll11l_opy_ = bstack1l1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡰࡴࡩࡡ࡭ࠩᥫ") #shift
  bstack11lll1l1l_opy_ = bstack1l1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡣࡳࡴ࠲ࡻࡰ࡭ࡱࡤࡨࠬᥬ") #shift
  bstack1llll1ll11_opy_ = bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡩࡩ࠮ࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠫᥭ")
  bstack1l111ll1ll_opy_ = bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡪࡩࡹ࠳ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠳ࡲࡦࡵࡸࡰࡹࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨ᥮") #shift
  bstack1111111l_opy_ = bstack1l1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠭ࡳࡧࡶࡹࡱࡺࡳࠨ᥯") #shift
  bstack11lll1111l1_opy_ = bstack1l1lll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽࠬᥰ") #shift
  bstack1l1ll1l111l_opy_ = bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᥱ")
  bstack11l1l1lll_opy_ = bstack1l1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡸࡺࡡࡵࡷࡶࠫᥲ") #shift
  bstack1l111l1l11_opy_ = bstack1l1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾࡭ࡻࡢ࠮࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠬᥳ")
  bstack11ll1lll1l1_opy_ = bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷࡵࡸࡺ࠯ࡶࡩࡹࡻࡰࠨᥴ") #shift
  bstack1l1lllll_opy_ = bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫ࡴࡶࡲࠪ᥵")
  bstack11lll11111l_opy_ = bstack1l1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡴࡡࡱࡵ࡫ࡳࡹ࠭᥶") # not bstack11ll1ll1l11_opy_ in python
  bstack1l11lll1ll_opy_ = bstack1l1lll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡱࡶ࡫ࡷࠫ᥷") # used in bstack11ll1llll11_opy_
  bstack1l1ll11l_opy_ = bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡨࡧࡷࠫ᥸") # used in bstack11ll1llll11_opy_
  bstack1l111ll1l1_opy_ = bstack1l1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡪࡲࡳࡰ࠭᥹")
  bstack1l1ll1l11_opy_ = bstack1l1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠪ᥺")
  bstack1l1111lll_opy_ = bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠪ᥻") #
  bstack1lllll111l_opy_ = bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡴ࠷࠱ࡺ࠼ࡧࡶ࡮ࡼࡥࡳ࠯ࡷࡥࡰ࡫ࡓࡤࡴࡨࡩࡳ࡙ࡨࡰࡶࠪ᥼")
  bstack1l1l1l1ll1_opy_ = bstack1l1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡦࡻࡴࡰ࠯ࡦࡥࡵࡺࡵࡳࡧࠪ᥽")
  bstack1llll1l11_opy_ = bstack1l1lll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡧ࠰ࡸࡪࡹࡴࠨ᥾")
  bstack1ll1lll111_opy_ = bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡱࡶࡸ࠲ࡺࡥࡴࡶࠪ᥿")
  bstack11lll1l1ll_opy_ = bstack1l1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡵࡩ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᦀ") #shift
  bstack1l11ll111l_opy_ = bstack1l1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡳࡸࡺ࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨᦁ") #shift
  bstack11ll1ll111l_opy_ = bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࠮ࡥࡤࡴࡹࡻࡲࡦࠩᦂ")
  bstack11ll1l1l11l_opy_ = bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡩࡥ࡮ࡨ࠱ࡹ࡯࡭ࡦࡱࡸࡸࠬᦃ")
  bstack1lll1111111_opy_ = bstack1l1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡶࡸࡦࡸࡴࠨᦄ")
  bstack11ll1ll1l1l_opy_ = bstack1l1lll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡨࡴࡽ࡮࡭ࡱࡤࡨࠬᦅ")
  bstack11ll1lll11l_opy_ = bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡨ࡮ࡥࡤ࡭࠰ࡹࡵࡪࡡࡵࡧࠪᦆ")
  bstack1lll111l11l_opy_ = bstack1l1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡤࡲࡳࡹࡹࡴࡳࡣࡳࠫᦇ")
  bstack1llll1l1l11_opy_ = bstack1l1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡦࡳࡳࡴࡥࡤࡶࠪᦈ")
  bstack1lllll1llll_opy_ = bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡷࡹࡵࡰࠨᦉ")
  bstack1lllll1l11l_opy_ = bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭ᦊ")
  bstack1ll1llll11l_opy_ = bstack1l1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩᦋ")
  bstack11ll1l11ll1_opy_ = bstack1l1lll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠪᦌ")
  bstack11ll1ll1lll_opy_ = bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡨࡓ࡫ࡡࡳࡧࡶࡸࡍࡻࡢࠨᦍ")
  bstack1l1l11ll1ll_opy_ = bstack1l1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡉ࡯࡫ࡷࠫᦎ")
  bstack1l1l11lll11_opy_ = bstack1l1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡶࡹ࠭ᦏ")
  bstack1ll1ll111l1_opy_ = bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡆࡳࡳ࡬ࡩࡨࠩᦐ")
  bstack11ll1l11l1l_opy_ = bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪᦑ")
  bstack1ll11ll11ll_opy_ = bstack1l1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡩࡔࡧ࡯ࡪࡍ࡫ࡡ࡭ࡕࡷࡩࡵ࠭ᦒ")
  bstack1ll11l1llll_opy_ = bstack1l1lll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡊࡩࡹࡘࡥࡴࡷ࡯ࡸࠬᦓ")
  bstack1ll11111ll1_opy_ = bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡅࡷࡧࡱࡸࠬᦔ")
  bstack1l1lll1l11l_opy_ = bstack1l1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠫᦕ")
  bstack1ll111111ll_opy_ = bstack1l1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡬ࡰࡩࡆࡶࡪࡧࡴࡦࡦࡈࡺࡪࡴࡴࠨᦖ")
  bstack11lll111111_opy_ = bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡦࡰࡴࡹࡪࡻࡥࡕࡧࡶࡸࡊࡼࡥ࡯ࡶࠪᦗ")
  bstack1l1l11llll1_opy_ = bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡴࡶࠧᦘ")
  bstack1lll11ll1ll_opy_ = bstack1l1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࡮ࡔࡶࡲࡴࠬᦙ")
class STAGE(Enum):
  bstack1ll1l1l1_opy_ = bstack1l1lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨᦚ")
  END = bstack1l1lll_opy_ (u"ࠪࡩࡳࡪࠧᦛ")
  bstack1111lll1_opy_ = bstack1l1lll_opy_ (u"ࠫࡸ࡯࡮ࡨ࡮ࡨࠫᦜ")
bstack1lll1lll11_opy_ = {
  bstack1l1lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬᦝ"): bstack1l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᦞ"),
  bstack1l1lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫᦟ"): bstack1l1lll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᦠ")
}
PLAYWRIGHT_HUB_URL = bstack1l1lll_opy_ (u"ࠤࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠦᦡ")