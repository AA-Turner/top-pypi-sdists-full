# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
import re
from enum import Enum
bstack1ll111111_opy_ = {
  bstack1l11lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᙱ"): bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪᙲ"),
  bstack1l11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᙳ"): bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫᙴ"),
  bstack1l11lll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᙵ"): bstack1l11lll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᙶ"),
  bstack1l11lll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᙷ"): bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᙸ"),
  bstack1l11lll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᙹ"): bstack1l11lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨᙺ"),
  bstack1l11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᙻ"): bstack1l11lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨᙼ"),
  bstack1l11lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᙽ"): bstack1l11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᙾ"),
  bstack1l11lll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᙿ"): bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫ "),
  bstack1l11lll_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬᚁ"): bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨᚂ"),
  bstack1l11lll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᚃ"): bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᚄ"),
  bstack1l11lll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᚅ"): bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᚆ"),
  bstack1l11lll_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬᚇ"): bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬᚈ"),
  bstack1l11lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᚉ"): bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᚊ"),
  bstack1l11lll_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᚋ"): bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᚌ"),
  bstack1l11lll_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᚍ"): bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᚎ"),
  bstack1l11lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᚏ"): bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᚐ"),
  bstack1l11lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᚑ"): bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᚒ"),
  bstack1l11lll_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪᚓ"): bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪᚔ"),
  bstack1l11lll_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᚕ"): bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᚖ"),
  bstack1l11lll_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᚗ"): bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᚘ"),
  bstack1l11lll_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬᚙ"): bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬᚚ"),
  bstack1l11lll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧ᚛"): bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧ᚜"),
  bstack1l11lll_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭᚝"): bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭᚞"),
  bstack1l11lll_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ᚟"): bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪᚠ"),
  bstack1l11lll_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᚡ"): bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᚢ"),
  bstack1l11lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᚣ"): bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᚤ"),
  bstack1l11lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᚥ"): bstack1l11lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᚦ"),
  bstack1l11lll_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᚧ"): bstack1l11lll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩᚨ"),
  bstack1l11lll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚩ"): bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᚪ"),
  bstack1l11lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᚫ"): bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᚬ"),
  bstack1l11lll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᚭ"): bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᚮ"),
  bstack1l11lll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪᚯ"): bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ᚰ"),
  bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᚱ"): bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᚲ"),
  bstack1l11lll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᚳ"): bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨᚴ"),
  bstack1l11lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᚵ"): bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᚶ"),
  bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᚷ"): bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᚸ"),
  bstack1l11lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᚹ"): bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᚺ"),
  bstack1l11lll_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚻ"): bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚼ"),
  bstack1l11lll_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᚽ"): bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᚾ"),
  bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᚿ"): bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᛀ"),
  bstack1l11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᛁ"): bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᛂ")
}
bstack11ll1l1ll11_opy_ = [
  bstack1l11lll_opy_ (u"ࠪࡳࡸ࠭ᛃ"),
  bstack1l11lll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᛄ"),
  bstack1l11lll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᛅ"),
  bstack1l11lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᛆ"),
  bstack1l11lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᛇ"),
  bstack1l11lll_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᛈ"),
  bstack1l11lll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᛉ"),
]
bstack1ll11l1lll_opy_ = {
  bstack1l11lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᛊ"): [bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᛋ"), bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡑࡅࡒࡋࠧᛌ")],
  bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᛍ"): bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᛎ"),
  bstack1l11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᛏ"): bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬᛐ"),
  bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᛑ"): bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠩᛒ"),
  bstack1l11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᛓ"): bstack1l11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᛔ"),
  bstack1l11lll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᛕ"): bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡕࡢࡔࡊࡘ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩᛖ"),
  bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᛗ"): bstack1l11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨᛘ"),
  bstack1l11lll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᛙ"): bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩᛚ"),
  bstack1l11lll_opy_ (u"࠭ࡡࡱࡲࠪᛛ"): [bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࡢࡍࡉ࠭ᛜ"), bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࠫᛝ")],
  bstack1l11lll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᛞ"): bstack1l11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡌࡐࡉࡏࡉ࡛ࡋࡌࠨᛟ"),
  bstack1l11lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᛠ"): bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᛡ"),
  bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᛢ"): bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠫᛣ"),
  bstack1l11lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᛤ"): bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡘࡖࡇࡕࡓࡄࡃࡏࡉࠬᛥ")
}
bstack1lll1l111l_opy_ = {
  bstack1l11lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᛦ"): [bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ᛧ"), bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᛨ")],
  bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᛩ"): [bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡥ࡫ࡦࡻࠪᛪ"), bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ᛫")],
  bstack1l11lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ᛬"): bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ᛭"),
  bstack1l11lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᛮ"): bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᛯ"),
  bstack1l11lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᛰ"): bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᛱ"),
  bstack1l11lll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᛲ"): [bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡳࡴࠬᛳ"), bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᛴ")],
  bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᛵ"): bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᛶ"),
  bstack1l11lll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪᛷ"): bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪᛸ"),
  bstack1l11lll_opy_ (u"ࠨࡣࡳࡴࠬ᛹"): bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴࠬ᛺"),
  bstack1l11lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ᛻"): bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ᛼"),
  bstack1l11lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᛽"): bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᛾")
}
bstack1l11111l1l_opy_ = {
  bstack1l11lll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ᛿"): bstack1l11lll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᜀ"),
  bstack1l11lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᜁ"): [bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᜂ"), bstack1l11lll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᜃ")],
  bstack1l11lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᜄ"): bstack1l11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᜅ"),
  bstack1l11lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᜆ"): bstack1l11lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᜇ"),
  bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᜈ"): [bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᜉ"), bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᜊ")],
  bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᜋ"): bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᜌ"),
  bstack1l11lll_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫᜍ"): bstack1l11lll_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭ᜎ"),
  bstack1l11lll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᜏ"): [bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᜐ"), bstack1l11lll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᜑ")],
  bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᜒ"): [bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧᜓ"), bstack1l11lll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺ᜔ࠧ")]
}
bstack1ll1l1lll1_opy_ = [
  bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹ᜕ࠧ"),
  bstack1l11lll_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬ᜖"),
  bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ᜗"),
  bstack1l11lll_opy_ (u"ࠫࡸ࡫ࡴࡘ࡫ࡱࡨࡴࡽࡒࡦࡥࡷࠫ᜘"),
  bstack1l11lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧ᜙"),
  bstack1l11lll_opy_ (u"࠭ࡳࡵࡴ࡬ࡧࡹࡌࡩ࡭ࡧࡌࡲࡹ࡫ࡲࡢࡥࡷࡥࡧ࡯࡬ࡪࡶࡼࠫ᜚"),
  bstack1l11lll_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪ᜛"),
  bstack1l11lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᜜"),
  bstack1l11lll_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ᜝"),
  bstack1l11lll_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ᜞"),
  bstack1l11lll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᜟ"),
  bstack1l11lll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᜠ"),
]
bstack1l1ll11111_opy_ = [
  bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᜡ"),
  bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᜢ"),
  bstack1l11lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᜣ"),
  bstack1l11lll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᜤ"),
  bstack1l11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᜥ"),
  bstack1l11lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᜦ"),
  bstack1l11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᜧ"),
  bstack1l11lll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᜨ"),
  bstack1l11lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᜩ"),
  bstack1l11lll_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜪ"),
  bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᜫ"),
  bstack1l11lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬᜬ"),
  bstack1l11lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡘࡦ࡭ࠧᜭ"),
  bstack1l11lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᜮ"),
  bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᜯ"),
  bstack1l11lll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫᜰ"),
  bstack1l11lll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠷ࠧᜱ"),
  bstack1l11lll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠲ࠨᜲ"),
  bstack1l11lll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠴ࠩᜳ"),
  bstack1l11lll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠶᜴ࠪ"),
  bstack1l11lll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠸ࠫ᜵"),
  bstack1l11lll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠺ࠬ᜶"),
  bstack1l11lll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠼࠭᜷"),
  bstack1l11lll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠾ࠧ᜸"),
  bstack1l11lll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠹ࠨ᜹"),
  bstack1l11lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ᜺"),
  bstack1l11lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᜻"),
  bstack1l11lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨ᜼"),
  bstack1l11lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ᜽"),
  bstack1l11lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ᜾"),
  bstack1l11lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬ᜿")
]
bstack11ll1l11111_opy_ = [
  bstack1l11lll_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧᝀ"),
  bstack1l11lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᝁ"),
  bstack1l11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᝂ"),
  bstack1l11lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᝃ"),
  bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡔࡷ࡯࡯ࡳ࡫ࡷࡽࠬᝄ"),
  bstack1l11lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᝅ"),
  bstack1l11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡢࡩࠪᝆ"),
  bstack1l11lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᝇ"),
  bstack1l11lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᝈ"),
  bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᝉ"),
  bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᝊ"),
  bstack1l11lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᝋ"),
  bstack1l11lll_opy_ (u"ࠧࡰࡵࠪᝌ"),
  bstack1l11lll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᝍ"),
  bstack1l11lll_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨᝎ"),
  bstack1l11lll_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᝏ"),
  bstack1l11lll_opy_ (u"ࠫࡷ࡫ࡧࡪࡱࡱࠫᝐ"),
  bstack1l11lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧᝑ"),
  bstack1l11lll_opy_ (u"࠭࡭ࡢࡥ࡫࡭ࡳ࡫ࠧᝒ"),
  bstack1l11lll_opy_ (u"ࠧࡳࡧࡶࡳࡱࡻࡴࡪࡱࡱࠫᝓ"),
  bstack1l11lll_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᝔"),
  bstack1l11lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭᝕"),
  bstack1l11lll_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩ᝖"),
  bstack1l11lll_opy_ (u"ࠫࡳࡵࡐࡢࡩࡨࡐࡴࡧࡤࡕ࡫ࡰࡩࡴࡻࡴࠨ᝗"),
  bstack1l11lll_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭᝘"),
  bstack1l11lll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬ᝙"),
  bstack1l11lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ᝚"),
  bstack1l11lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩ᝛"),
  bstack1l11lll_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭᝜"),
  bstack1l11lll_opy_ (u"ࠪࡲࡴࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠧ᝝"),
  bstack1l11lll_opy_ (u"ࠫࡨ࡮ࡥࡤ࡭ࡘࡖࡑ࠭᝞"),
  bstack1l11lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᝟"),
  bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡉ࡯ࡰ࡭࡬ࡩࡸ࠭ᝠ"),
  bstack1l11lll_opy_ (u"ࠧࡤࡣࡳࡸࡺࡸࡥࡄࡴࡤࡷ࡭࠭ᝡ"),
  bstack1l11lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᝢ"),
  bstack1l11lll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᝣ"),
  bstack1l11lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡖࡦࡴࡶ࡭ࡴࡴࠧᝤ"),
  bstack1l11lll_opy_ (u"ࠫࡳࡵࡂ࡭ࡣࡱ࡯ࡕࡵ࡬࡭࡫ࡱ࡫ࠬᝥ"),
  bstack1l11lll_opy_ (u"ࠬࡳࡡࡴ࡭ࡖࡩࡳࡪࡋࡦࡻࡶࠫᝦ"),
  bstack1l11lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡒ࡯ࡨࡵࠪᝧ"),
  bstack1l11lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡉࡥࠩᝨ"),
  bstack1l11lll_opy_ (u"ࠨࡦࡨࡨ࡮ࡩࡡࡵࡧࡧࡈࡪࡼࡩࡤࡧࠪᝩ"),
  bstack1l11lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡒࡤࡶࡦࡳࡳࠨᝪ"),
  bstack1l11lll_opy_ (u"ࠪࡴ࡭ࡵ࡮ࡦࡐࡸࡱࡧ࡫ࡲࠨᝫ"),
  bstack1l11lll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩᝬ"),
  bstack1l11lll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡒࡴࡹ࡯࡯࡯ࡵࠪ᝭"),
  bstack1l11lll_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫᝮ"),
  bstack1l11lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᝯ"),
  bstack1l11lll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬᝰ"),
  bstack1l11lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡄ࡬ࡳࡲ࡫ࡴࡳ࡫ࡦࠫ᝱"),
  bstack1l11lll_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࡘ࠵ࠫᝲ"),
  bstack1l11lll_opy_ (u"ࠫࡲ࡯ࡤࡔࡧࡶࡷ࡮ࡵ࡮ࡊࡰࡶࡸࡦࡲ࡬ࡂࡲࡳࡷࠬᝳ"),
  bstack1l11lll_opy_ (u"ࠬ࡫ࡳࡱࡴࡨࡷࡸࡵࡓࡦࡴࡹࡩࡷ࠭᝴"),
  bstack1l11lll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬ᝵"),
  bstack1l11lll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡅࡧࡴࠬ᝶"),
  bstack1l11lll_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨ᝷"),
  bstack1l11lll_opy_ (u"ࠩࡶࡽࡳࡩࡔࡪ࡯ࡨ࡛࡮ࡺࡨࡏࡖࡓࠫ᝸"),
  bstack1l11lll_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨ᝹"),
  bstack1l11lll_opy_ (u"ࠫ࡬ࡶࡳࡍࡱࡦࡥࡹ࡯࡯࡯ࠩ᝺"),
  bstack1l11lll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭᝻"),
  bstack1l11lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭᝼"),
  bstack1l11lll_opy_ (u"ࠧࡧࡱࡵࡧࡪࡉࡨࡢࡰࡪࡩࡏࡧࡲࠨ᝽"),
  bstack1l11lll_opy_ (u"ࠨࡺࡰࡷࡏࡧࡲࠨ᝾"),
  bstack1l11lll_opy_ (u"ࠩࡻࡱࡽࡐࡡࡳࠩ᝿"),
  bstack1l11lll_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩក"),
  bstack1l11lll_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫខ"),
  bstack1l11lll_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭គ"),
  bstack1l11lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩឃ"),
  bstack1l11lll_opy_ (u"ࠧࡢࡲࡳ࡚ࡪࡸࡳࡪࡱࡱࠫង"),
  bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧច"),
  bstack1l11lll_opy_ (u"ࠩࡵࡩࡸ࡯ࡧ࡯ࡃࡳࡴࠬឆ"),
  bstack1l11lll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳࡹࠧជ"),
  bstack1l11lll_opy_ (u"ࠫࡨࡧ࡮ࡢࡴࡼࠫឈ"),
  bstack1l11lll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ញ"),
  bstack1l11lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ដ"),
  bstack1l11lll_opy_ (u"ࠧࡪࡧࠪឋ"),
  bstack1l11lll_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ឌ"),
  bstack1l11lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩឍ"),
  bstack1l11lll_opy_ (u"ࠪࡵࡺ࡫ࡵࡦࠩណ"),
  bstack1l11lll_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ត"),
  bstack1l11lll_opy_ (u"ࠬࡧࡰࡱࡕࡷࡳࡷ࡫ࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳ࠭ថ"),
  bstack1l11lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡉࡡ࡮ࡧࡵࡥࡎࡳࡡࡨࡧࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬទ"),
  bstack1l11lll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡊࡾࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪធ"),
  bstack1l11lll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡏ࡮ࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫន"),
  bstack1l11lll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ប"),
  bstack1l11lll_opy_ (u"ࠪࡶࡪࡹࡥࡳࡸࡨࡈࡪࡼࡩࡤࡧࠪផ"),
  bstack1l11lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫព"),
  bstack1l11lll_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧភ"),
  bstack1l11lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡡࡴࡵࡦࡳࡩ࡫ࠧម"),
  bstack1l11lll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡉࡰࡵࡇࡩࡻ࡯ࡣࡦࡕࡨࡸࡹ࡯࡮ࡨࡵࠪយ"),
  bstack1l11lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡷࡧ࡭ࡴࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨរ"),
  bstack1l11lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡳࡴࡱ࡫ࡐࡢࡻࠪល"),
  bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫវ"),
  bstack1l11lll_opy_ (u"ࠫࡼࡪࡩࡰࡕࡨࡶࡻ࡯ࡣࡦࠩឝ"),
  bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧឞ"),
  bstack1l11lll_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡃࡳࡱࡶࡷࡘ࡯ࡴࡦࡖࡵࡥࡨࡱࡩ࡯ࡩࠪស"),
  bstack1l11lll_opy_ (u"ࠧࡩ࡫ࡪ࡬ࡈࡵ࡮ࡵࡴࡤࡷࡹ࠭ហ"),
  bstack1l11lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡑࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࡷࠬឡ"),
  bstack1l11lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬអ"),
  bstack1l11lll_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧឣ"),
  bstack1l11lll_opy_ (u"ࠫࡷ࡫࡭ࡰࡸࡨࡍࡔ࡙ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࡐࡴࡩࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩឤ"),
  bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧឥ"),
  bstack1l11lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨឦ"),
  bstack1l11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩឧ"),
  bstack1l11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧឨ"),
  bstack1l11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫឩ"),
  bstack1l11lll_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ឪ"),
  bstack1l11lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪឫ"),
  bstack1l11lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧឬ"),
  bstack1l11lll_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩឭ")
]
bstack11ll1l1l_opy_ = {
  bstack1l11lll_opy_ (u"ࠧࡷࠩឮ"): bstack1l11lll_opy_ (u"ࠨࡸࠪឯ"),
  bstack1l11lll_opy_ (u"ࠩࡩࠫឰ"): bstack1l11lll_opy_ (u"ࠪࡪࠬឱ"),
  bstack1l11lll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪឲ"): bstack1l11lll_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫឳ"),
  bstack1l11lll_opy_ (u"࠭࡯࡯࡮ࡼࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ឴"): bstack1l11lll_opy_ (u"ࠧࡰࡰ࡯ࡽࡆࡻࡴࡰ࡯ࡤࡸࡪ࠭឵"),
  bstack1l11lll_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬា"): bstack1l11lll_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭ិ"),
  bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭ី"): bstack1l11lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧឹ"),
  bstack1l11lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨឺ"): bstack1l11lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩុ"),
  bstack1l11lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪូ"): bstack1l11lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫួ"),
  bstack1l11lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬើ"): bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ឿ"),
  bstack1l11lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬៀ"): bstack1l11lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡊࡲࡷࡹ࠭េ"),
  bstack1l11lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧែ"): bstack1l11lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨៃ"),
  bstack1l11lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩោ"): bstack1l11lll_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫៅ"),
  bstack1l11lll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬំ"): bstack1l11lll_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ះ"),
  bstack1l11lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ៈ"): bstack1l11lll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨ៉"),
  bstack1l11lll_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩ៊"): bstack1l11lll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪ់"),
  bstack1l11lll_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭៌"): bstack1l11lll_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧ៍"),
  bstack1l11lll_opy_ (u"ࠫࡵࡧࡣࡧ࡫࡯ࡩࠬ៎"): bstack1l11lll_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨ៏"),
  bstack1l11lll_opy_ (u"࠭ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨ័"): bstack1l11lll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ៑"),
  bstack1l11lll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨ្ࠫ"): bstack1l11lll_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ៓"),
  bstack1l11lll_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫ។"): bstack1l11lll_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬ៕"),
  bstack1l11lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ៖"): bstack1l11lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨៗ"),
  bstack1l11lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩ៘"): bstack1l11lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡳࡩࡦࡺࡥࡳࠩ៙")
}
bstack11ll11lllll_opy_ = bstack1l11lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫࡮ࡺࡨࡶࡤ࠱ࡧࡴࡳ࠯ࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫࠲ࡶࡪࡲࡥࡢࡵࡨࡷ࠴ࡲࡡࡵࡧࡶࡸ࠴ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢ៚")
bstack11lll111111_opy_ = bstack1l11lll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠲࡬ࡪࡧ࡬ࡵࡪࡦ࡬ࡪࡩ࡫ࠣ៛")
bstack11lll1ll11_opy_ = bstack1l11lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡫ࡤࡴ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡹࡥ࡯ࡦࡢࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢៜ")
bstack1lll1ll1_opy_ = bstack1l11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭៝")
bstack1l111l1l1l_opy_ = bstack1l11lll_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩ៞")
bstack11l11l11l1_opy_ = bstack1l11lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡰࡨࡼࡹࡥࡨࡶࡤࡶࠫ៟")
bstack11ll1lll11l_opy_ = {
  bstack1l11lll_opy_ (u"ࠨࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠪ០"): 50,
  bstack1l11lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ១"): 40,
  bstack1l11lll_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫ២"): 30,
  bstack1l11lll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ៣"): 20,
  bstack1l11lll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫ៤"): 10
}
bstack111111111_opy_ = bstack11ll1lll11l_opy_[bstack1l11lll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ៥")]
bstack1l11ll1l_opy_ = bstack1l11lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭៦")
bstack1ll111l1_opy_ = bstack1l11lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭៧")
bstack1ll1111ll1_opy_ = bstack1l11lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ៨")
bstack1111l1ll1_opy_ = bstack1l11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩ៩")
bstack1l1l1lll1_opy_ = bstack1l11lll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡧ࡮ࡥࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡵࡧࡣ࡬ࡣࡪࡩࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩ៪")
bstack11ll1l11lll_opy_ = [bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭៫"), bstack1l11lll_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭៬")]
bstack11ll1lll1ll_opy_ = [bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ៭"), bstack1l11lll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ៮")]
bstack11111lll1_opy_ = re.compile(bstack1l11lll_opy_ (u"ࠩࡡ࡟ࡡࡢࡷ࠮࡟࠮࠾࠳࠰ࠤࠨ៯"))
bstack11ll11ll1_opy_ = [
  bstack1l11lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡎࡢ࡯ࡨࠫ៰"),
  bstack1l11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭៱"),
  bstack1l11lll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ៲"),
  bstack1l11lll_opy_ (u"࠭࡮ࡦࡹࡆࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪ៳"),
  bstack1l11lll_opy_ (u"ࠧࡢࡲࡳࠫ៴"),
  bstack1l11lll_opy_ (u"ࠨࡷࡧ࡭ࡩ࠭៵"),
  bstack1l11lll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ៶"),
  bstack1l11lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࠪ៷"),
  bstack1l11lll_opy_ (u"ࠫࡴࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩ៸"),
  bstack1l11lll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࠪ៹"),
  bstack1l11lll_opy_ (u"࠭࡮ࡰࡔࡨࡷࡪࡺࠧ៺"), bstack1l11lll_opy_ (u"ࠧࡧࡷ࡯ࡰࡗ࡫ࡳࡦࡶࠪ៻"),
  bstack1l11lll_opy_ (u"ࠨࡥ࡯ࡩࡦࡸࡓࡺࡵࡷࡩࡲࡌࡩ࡭ࡧࡶࠫ៼"),
  bstack1l11lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡕ࡫ࡰ࡭ࡳ࡭ࡳࠨ៽"),
  bstack1l11lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࡌࡰࡩࡪ࡭ࡳ࡭ࠧ៾"),
  bstack1l11lll_opy_ (u"ࠫࡴࡺࡨࡦࡴࡄࡴࡵࡹࠧ៿"),
  bstack1l11lll_opy_ (u"ࠬࡶࡲࡪࡰࡷࡔࡦ࡭ࡥࡔࡱࡸࡶࡨ࡫ࡏ࡯ࡈ࡬ࡲࡩࡌࡡࡪ࡮ࡸࡶࡪ࠭᠀"),
  bstack1l11lll_opy_ (u"࠭ࡡࡱࡲࡄࡧࡹ࡯ࡶࡪࡶࡼࠫ᠁"), bstack1l11lll_opy_ (u"ࠧࡢࡲࡳࡔࡦࡩ࡫ࡢࡩࡨࠫ᠂"), bstack1l11lll_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ᠃"), bstack1l11lll_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡓࡥࡨࡱࡡࡨࡧࠪ᠄"), bstack1l11lll_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡈࡺࡸࡡࡵ࡫ࡲࡲࠬ᠅"),
  bstack1l11lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩ᠆"),
  bstack1l11lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡪࡹࡴࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩ᠇"),
  bstack1l11lll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࠨ᠈"), bstack1l11lll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࡇࡱࡨࡎࡴࡴࡦࡰࡷࠫ᠉"),
  bstack1l11lll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᠊"),
  bstack1l11lll_opy_ (u"ࠩࡤࡨࡧࡖ࡯ࡳࡶࠪ᠋"),
  bstack1l11lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡖࡳࡨࡱࡥࡵࠩ᠌"),
  bstack1l11lll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰ࡙࡯࡭ࡦࡱࡸࡸࠬ᠍"),
  bstack1l11lll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡵࡪࠪ᠎"),
  bstack1l11lll_opy_ (u"࠭ࡡࡷࡦࠪ᠏"), bstack1l11lll_opy_ (u"ࠧࡢࡸࡧࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᠐"), bstack1l11lll_opy_ (u"ࠨࡣࡹࡨࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᠑"), bstack1l11lll_opy_ (u"ࠩࡤࡺࡩࡇࡲࡨࡵࠪ᠒"),
  bstack1l11lll_opy_ (u"ࠪࡹࡸ࡫ࡋࡦࡻࡶࡸࡴࡸࡥࠨ᠓"), bstack1l11lll_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡵࡪࠪ᠔"), bstack1l11lll_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡵࡶࡻࡴࡸࡤࠨ᠕"),
  bstack1l11lll_opy_ (u"࠭࡫ࡦࡻࡄࡰ࡮ࡧࡳࠨ᠖"), bstack1l11lll_opy_ (u"ࠧ࡬ࡧࡼࡔࡦࡹࡳࡸࡱࡵࡨࠬ᠗"),
  bstack1l11lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪ᠘"), bstack1l11lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡂࡴࡪࡷࠬ᠙"), bstack1l11lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࡉ࡯ࡲࠨ᠚"), bstack1l11lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡆ࡬ࡷࡵ࡭ࡦࡏࡤࡴࡵ࡯࡮ࡨࡈ࡬ࡰࡪ࠭᠛"), bstack1l11lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵ࡙ࡸ࡫ࡓࡺࡵࡷࡩࡲࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩ᠜"),
  bstack1l11lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࠩ᠝"), bstack1l11lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࡶࠫ᠞"),
  bstack1l11lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡄࡪࡵࡤࡦࡱ࡫ࡂࡶ࡫࡯ࡨࡈ࡮ࡥࡤ࡭ࠪ᠟"),
  bstack1l11lll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࡔࡪ࡯ࡨࡳࡺࡺࠧᠠ"),
  bstack1l11lll_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡄࡧࡹ࡯࡯࡯ࠩᠡ"), bstack1l11lll_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡇࡦࡺࡥࡨࡱࡵࡽࠬᠢ"), bstack1l11lll_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡋࡲࡡࡨࡵࠪᠣ"), bstack1l11lll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࡊࡰࡷࡩࡳࡺࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩᠤ"),
  bstack1l11lll_opy_ (u"ࠧࡥࡱࡱࡸࡘࡺ࡯ࡱࡃࡳࡴࡔࡴࡒࡦࡵࡨࡸࠬᠥ"),
  bstack1l11lll_opy_ (u"ࠨࡷࡱ࡭ࡨࡵࡤࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪᠦ"), bstack1l11lll_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡌࡧࡼࡦࡴࡧࡲࡥࠩᠧ"),
  bstack1l11lll_opy_ (u"ࠪࡲࡴ࡙ࡩࡨࡰࠪᠨ"),
  bstack1l11lll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨ࡙ࡳ࡯࡭ࡱࡱࡵࡸࡦࡴࡴࡗ࡫ࡨࡻࡸ࠭ᠩ"),
  bstack1l11lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡥࡴࡲ࡭ࡩ࡝ࡡࡵࡥ࡫ࡩࡷࡹࠧᠪ"),
  bstack1l11lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᠫ"),
  bstack1l11lll_opy_ (u"ࠧࡳࡧࡦࡶࡪࡧࡴࡦࡅ࡫ࡶࡴࡳࡥࡅࡴ࡬ࡺࡪࡸࡓࡦࡵࡶ࡭ࡴࡴࡳࠨᠬ"),
  bstack1l11lll_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧᠭ"),
  bstack1l11lll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡖࡡࡵࡪࠪᠮ"),
  bstack1l11lll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡗࡵ࡫ࡥࡥࠩᠯ"),
  bstack1l11lll_opy_ (u"ࠫ࡬ࡶࡳࡆࡰࡤࡦࡱ࡫ࡤࠨᠰ"),
  bstack1l11lll_opy_ (u"ࠬ࡯ࡳࡉࡧࡤࡨࡱ࡫ࡳࡴࠩᠱ"),
  bstack1l11lll_opy_ (u"࠭ࡡࡥࡤࡈࡼࡪࡩࡔࡪ࡯ࡨࡳࡺࡺࠧᠲ"),
  bstack1l11lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ᠳ"),
  bstack1l11lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡊࡥࡷ࡫ࡦࡩࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬᠴ"),
  bstack1l11lll_opy_ (u"ࠩࡤࡹࡹࡵࡇࡳࡣࡱࡸࡕ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠩᠵ"),
  bstack1l11lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡒࡦࡺࡵࡳࡣ࡯ࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᠶ"),
  bstack1l11lll_opy_ (u"ࠫࡸࡿࡳࡵࡧࡰࡔࡴࡸࡴࠨᠷ"),
  bstack1l11lll_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡪࡢࡉࡱࡶࡸࠬᠸ"),
  bstack1l11lll_opy_ (u"࠭ࡳ࡬࡫ࡳ࡙ࡳࡲ࡯ࡤ࡭ࠪᠹ"), bstack1l11lll_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡔࡺࡲࡨࠫᠺ"), bstack1l11lll_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡌࡧࡼࠫᠻ"),
  bstack1l11lll_opy_ (u"ࠩࡤࡹࡹࡵࡌࡢࡷࡱࡧ࡭࠭ᠼ"),
  bstack1l11lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡧࡦࡺࡃࡢࡲࡷࡹࡷ࡫ࠧᠽ"),
  bstack1l11lll_opy_ (u"ࠫࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࡏࡵࡪࡨࡶࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ᠾ"),
  bstack1l11lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪ࡝ࡩ࡯ࡦࡲࡻࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࠧᠿ"),
  bstack1l11lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡵ࡯࡭ࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᡀ"),
  bstack1l11lll_opy_ (u"ࠧࡦࡰࡩࡳࡷࡩࡥࡂࡲࡳࡍࡳࡹࡴࡢ࡮࡯ࠫᡁ"),
  bstack1l11lll_opy_ (u"ࠨࡧࡱࡷࡺࡸࡥࡘࡧࡥࡺ࡮࡫ࡷࡴࡊࡤࡺࡪࡖࡡࡨࡧࡶࠫᡂ"), bstack1l11lll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡇࡩࡻࡺ࡯ࡰ࡮ࡶࡔࡴࡸࡴࠨᡃ"), bstack1l11lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧ࡚ࡩࡧࡼࡩࡦࡹࡇࡩࡹࡧࡩ࡭ࡵࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠭ᡄ"),
  bstack1l11lll_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡵࡶࡳࡄࡣࡦ࡬ࡪࡒࡩ࡮࡫ࡷࠫᡅ"),
  bstack1l11lll_opy_ (u"ࠬࡩࡡ࡭ࡧࡱࡨࡦࡸࡆࡰࡴࡰࡥࡹ࠭ᡆ"),
  bstack1l11lll_opy_ (u"࠭ࡢࡶࡰࡧࡰࡪࡏࡤࠨᡇ"),
  bstack1l11lll_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧᡈ"),
  bstack1l11lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡉࡳࡧࡢ࡭ࡧࡧࠫᡉ"), bstack1l11lll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡆࡻࡴࡩࡱࡵ࡭ࡿ࡫ࡤࠨᡊ"),
  bstack1l11lll_opy_ (u"ࠪࡥࡺࡺ࡯ࡂࡥࡦࡩࡵࡺࡁ࡭ࡧࡵࡸࡸ࠭ᡋ"), bstack1l11lll_opy_ (u"ࠫࡦࡻࡴࡰࡆ࡬ࡷࡲ࡯ࡳࡴࡃ࡯ࡩࡷࡺࡳࠨᡌ"),
  bstack1l11lll_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡴࡎ࡬ࡦࠬᡍ"),
  bstack1l11lll_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡖࡤࡴࠬᡎ"),
  bstack1l11lll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉ࡯࡫ࡷ࡭ࡦࡲࡕࡳ࡮ࠪᡏ"), bstack1l11lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡂ࡮࡯ࡳࡼࡖ࡯ࡱࡷࡳࡷࠬᡐ"), bstack1l11lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡪࡲࡴࡸࡥࡇࡴࡤࡹࡩ࡝ࡡࡳࡰ࡬ࡲ࡬࠭ᡑ"), bstack1l11lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡪࡴࡌࡪࡰ࡮ࡷࡎࡴࡂࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠪᡒ"),
  bstack1l11lll_opy_ (u"ࠫࡰ࡫ࡥࡱࡍࡨࡽࡈ࡮ࡡࡪࡰࡶࠫᡓ"),
  bstack1l11lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡿࡧࡢ࡭ࡧࡖࡸࡷ࡯࡮ࡨࡵࡇ࡭ࡷ࠭ᡔ"),
  bstack1l11lll_opy_ (u"࠭ࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩᡕ"),
  bstack1l11lll_opy_ (u"ࠧࡪࡰࡷࡩࡷࡑࡥࡺࡆࡨࡰࡦࡿࠧᡖ"),
  bstack1l11lll_opy_ (u"ࠨࡵ࡫ࡳࡼࡏࡏࡔࡎࡲ࡫ࠬᡗ"),
  bstack1l11lll_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡖࡸࡷࡧࡴࡦࡩࡼࠫᡘ"),
  bstack1l11lll_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡕࡩࡸࡶ࡯࡯ࡵࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᡙ"), bstack1l11lll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡘࡣ࡬ࡸ࡙࡯࡭ࡦࡱࡸࡸࠬᡚ"),
  bstack1l11lll_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࠨᡛ"),
  bstack1l11lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡳࡺࡰࡦࡉࡽ࡫ࡣࡶࡶࡨࡊࡷࡵ࡭ࡉࡶࡷࡴࡸ࠭ᡜ"),
  bstack1l11lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡄࡣࡳࡸࡺࡸࡥࠨᡝ"),
  bstack1l11lll_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨᡞ"),
  bstack1l11lll_opy_ (u"ࠩࡩࡹࡱࡲࡃࡰࡰࡷࡩࡽࡺࡌࡪࡵࡷࠫᡟ"),
  bstack1l11lll_opy_ (u"ࠪࡻࡦ࡯ࡴࡇࡱࡵࡅࡵࡶࡓࡤࡴ࡬ࡴࡹ࠭ᡠ"),
  bstack1l11lll_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡈࡵ࡮࡯ࡧࡦࡸࡗ࡫ࡴࡳ࡫ࡨࡷࠬᡡ"),
  bstack1l11lll_opy_ (u"ࠬࡧࡰࡱࡐࡤࡱࡪ࠭ᡢ"),
  bstack1l11lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡓࡍࡅࡨࡶࡹ࠭ᡣ"),
  bstack1l11lll_opy_ (u"ࠧࡵࡣࡳ࡛࡮ࡺࡨࡔࡪࡲࡶࡹࡖࡲࡦࡵࡶࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᡤ"),
  bstack1l11lll_opy_ (u"ࠨࡵࡦࡥࡱ࡫ࡆࡢࡥࡷࡳࡷ࠭ᡥ"),
  bstack1l11lll_opy_ (u"ࠩࡺࡨࡦࡒ࡯ࡤࡣ࡯ࡔࡴࡸࡴࠨᡦ"),
  bstack1l11lll_opy_ (u"ࠪࡷ࡭ࡵࡷ࡙ࡥࡲࡨࡪࡒ࡯ࡨࠩᡧ"),
  bstack1l11lll_opy_ (u"ࠫ࡮ࡵࡳࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡸࡷࡪ࠭ᡨ"),
  bstack1l11lll_opy_ (u"ࠬࡾࡣࡰࡦࡨࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠧᡩ"),
  bstack1l11lll_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡶࡷࡼࡵࡲࡥࠩᡪ"),
  bstack1l11lll_opy_ (u"ࠧࡶࡵࡨࡔࡷ࡫ࡢࡶ࡫࡯ࡸ࡜ࡊࡁࠨᡫ"),
  bstack1l11lll_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵ࡙ࡇࡅࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠩᡬ"),
  bstack1l11lll_opy_ (u"ࠩࡺࡩࡧࡊࡲࡪࡸࡨࡶࡆ࡭ࡥ࡯ࡶࡘࡶࡱ࠭ᡭ"),
  bstack1l11lll_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡴࡩࠩᡮ"),
  bstack1l11lll_opy_ (u"ࠫࡺࡹࡥࡏࡧࡺ࡛ࡉࡇࠧᡯ"),
  bstack1l11lll_opy_ (u"ࠬࡽࡤࡢࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᡰ"), bstack1l11lll_opy_ (u"࠭ࡷࡥࡣࡆࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᡱ"),
  bstack1l11lll_opy_ (u"ࠧࡹࡥࡲࡨࡪࡕࡲࡨࡋࡧࠫᡲ"), bstack1l11lll_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡓࡪࡩࡱ࡭ࡳ࡭ࡉࡥࠩᡳ"),
  bstack1l11lll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦ࡚ࡈࡆࡈࡵ࡯ࡦ࡯ࡩࡎࡪࠧᡴ"),
  bstack1l11lll_opy_ (u"ࠪࡶࡪࡹࡥࡵࡑࡱࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡲࡵࡑࡱࡰࡾ࠭ᡵ"),
  bstack1l11lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࡸ࠭ᡶ"),
  bstack1l11lll_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷ࡯ࡥࡴࠩᡷ"), bstack1l11lll_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡹࡊࡰࡷࡩࡷࡼࡡ࡭ࠩᡸ"),
  bstack1l11lll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࡉࡣࡵࡨࡼࡧࡲࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪ᡹"),
  bstack1l11lll_opy_ (u"ࠨ࡯ࡤࡼ࡙ࡿࡰࡪࡰࡪࡊࡷ࡫ࡱࡶࡧࡱࡧࡾ࠭᡺"),
  bstack1l11lll_opy_ (u"ࠩࡶ࡭ࡲࡶ࡬ࡦࡋࡶ࡚࡮ࡹࡩࡣ࡮ࡨࡇ࡭࡫ࡣ࡬ࠩ᡻"),
  bstack1l11lll_opy_ (u"ࠪࡹࡸ࡫ࡃࡢࡴࡷ࡬ࡦ࡭ࡥࡔࡵ࡯ࠫ᡼"),
  bstack1l11lll_opy_ (u"ࠫࡸ࡮࡯ࡶ࡮ࡧ࡙ࡸ࡫ࡓࡪࡰࡪࡰࡪࡺ࡯࡯ࡖࡨࡷࡹࡓࡡ࡯ࡣࡪࡩࡷ࠭᡽"),
  bstack1l11lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡍ࡜ࡊࡐࠨ᡾"),
  bstack1l11lll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙ࡵࡵࡤࡪࡌࡨࡊࡴࡲࡰ࡮࡯ࠫ᡿"),
  bstack1l11lll_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡈࡪࡦࡧࡩࡳࡇࡰࡪࡒࡲࡰ࡮ࡩࡹࡆࡴࡵࡳࡷ࠭ᢀ"),
  bstack1l11lll_opy_ (u"ࠨ࡯ࡲࡧࡰࡒ࡯ࡤࡣࡷ࡭ࡴࡴࡁࡱࡲࠪᢁ"),
  bstack1l11lll_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈࡲࡶࡲࡧࡴࠨᢂ"), bstack1l11lll_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉ࡭ࡱࡺࡥࡳࡕࡳࡩࡨࡹࠧᢃ"),
  bstack1l11lll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡇࡩࡱࡧࡹࡂࡦࡥࠫᢄ"),
  bstack1l11lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡏࡤࡍࡱࡦࡥࡹࡵࡲࡂࡷࡷࡳࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠨᢅ")
]
bstack1l1l1l11l_opy_ = bstack1l11lll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡻࡰ࡭ࡱࡤࡨࠬᢆ")
bstack1lllll111_opy_ = [bstack1l11lll_opy_ (u"ࠧ࠯ࡣࡳ࡯ࠬᢇ"), bstack1l11lll_opy_ (u"ࠨ࠰ࡤࡥࡧ࠭ᢈ"), bstack1l11lll_opy_ (u"ࠩ࠱࡭ࡵࡧࠧᢉ")]
bstack1l11ll1ll1_opy_ = [bstack1l11lll_opy_ (u"ࠪ࡭ࡩ࠭ᢊ"), bstack1l11lll_opy_ (u"ࠫࡵࡧࡴࡩࠩᢋ"), bstack1l11lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨᢌ"), bstack1l11lll_opy_ (u"࠭ࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࠬᢍ")]
bstack1lll1ll1l1_opy_ = {
  bstack1l11lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᢎ"): bstack1l11lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢏ"),
  bstack1l11lll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪᢐ"): bstack1l11lll_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᢑ"),
  bstack1l11lll_opy_ (u"ࠫࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢒ"): bstack1l11lll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢓ"),
  bstack1l11lll_opy_ (u"࠭ࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢔ"): bstack1l11lll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢕ"),
  bstack1l11lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡷ࡭ࡴࡴࡳࠨᢖ"): bstack1l11lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᢗ")
}
bstack11l1l1lll_opy_ = [
  bstack1l11lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᢘ"),
  bstack1l11lll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩᢙ"),
  bstack1l11lll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢚ"),
  bstack1l11lll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬᢛ"),
  bstack1l11lll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨᢜ"),
]
bstack1l1111l1l_opy_ = bstack1l1ll11111_opy_ + bstack11ll1l11111_opy_ + bstack11ll11ll1_opy_
bstack11l11lll_opy_ = [
  bstack1l11lll_opy_ (u"ࠨࡠ࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸࠩ࠭ᢝ"),
  bstack1l11lll_opy_ (u"ࠩࡡࡦࡸ࠳࡬ࡰࡥࡤࡰ࠳ࡩ࡯࡮ࠦࠪᢞ"),
  bstack1l11lll_opy_ (u"ࠪࡢ࠶࠸࠷࠯ࠩᢟ"),
  bstack1l11lll_opy_ (u"ࠫࡣ࠷࠰࠯ࠩᢠ"),
  bstack1l11lll_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠵ࡠ࠼࠭࠺࡟࠱ࠫᢡ"),
  bstack1l11lll_opy_ (u"࠭࡞࠲࠹࠵࠲࠷ࡡ࠰࠮࠻ࡠ࠲ࠬᢢ"),
  bstack1l11lll_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠹࡛࠱࠯࠴ࡡ࠳࠭ᢣ"),
  bstack1l11lll_opy_ (u"ࠨࡠ࠴࠽࠷࠴࠱࠷࠺࠱ࠫᢤ")
]
bstack11ll1l1l1ll_opy_ = bstack1l11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᢥ")
bstack1l1111ll1_opy_ = bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠯ࡷ࠳࠲ࡩࡻ࡫࡮ࡵࠩᢦ")
bstack1l111lll1l_opy_ = [ bstack1l11lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᢧ") ]
bstack11l1ll1l_opy_ = [ bstack1l11lll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᢨ") ]
bstack1ll111l11_opy_ = [bstack1l11lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧᢩࠪ")]
bstack1llll11lll_opy_ = [ bstack1l11lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᢪ") ]
bstack111l11ll_opy_ = bstack1l11lll_opy_ (u"ࠨࡕࡇࡏࡘ࡫ࡴࡶࡲࠪ᢫")
bstack111l1l1l1_opy_ = bstack1l11lll_opy_ (u"ࠩࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠬ᢬")
bstack1ll1l1lll_opy_ = bstack1l11lll_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠧ᢭")
bstack11l1lll11l_opy_ = bstack1l11lll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࠪ᢮")
bstack1ll1l1ll1l_opy_ = [
  bstack1l11lll_opy_ (u"ࠬࡋࡒࡓࡡࡉࡅࡎࡒࡅࡅࠩ᢯"),
  bstack1l11lll_opy_ (u"࠭ࡅࡓࡔࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ᢰ"),
  bstack1l11lll_opy_ (u"ࠧࡆࡔࡕࡣࡇࡒࡏࡄࡍࡈࡈࡤࡈ࡙ࡠࡅࡏࡍࡊࡔࡔࠨᢱ"),
  bstack1l11lll_opy_ (u"ࠨࡇࡕࡖࡤࡔࡅࡕ࡙ࡒࡖࡐࡥࡃࡉࡃࡑࡋࡊࡊࠧᢲ"),
  bstack1l11lll_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡉ࡙ࡥࡎࡐࡖࡢࡇࡔࡔࡎࡆࡅࡗࡉࡉ࠭ᢳ"),
  bstack1l11lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡈࡒࡏࡔࡇࡇࠫᢴ"),
  bstack1l11lll_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡘࡅࡔࡇࡗࠫᢵ"),
  bstack1l11lll_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡈࡘࡗࡊࡊࠧᢶ"),
  bstack1l11lll_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡂࡄࡒࡖ࡙ࡋࡄࠨᢷ"),
  bstack1l11lll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᢸ"),
  bstack1l11lll_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡒࡔ࡚࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࠩᢹ"),
  bstack1l11lll_opy_ (u"ࠩࡈࡖࡗࡥࡁࡅࡆࡕࡉࡘ࡙࡟ࡊࡐ࡙ࡅࡑࡏࡄࠨᢺ"),
  bstack1l11lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡗࡑࡖࡊࡇࡃࡉࡃࡅࡐࡊ࠭ᢻ"),
  bstack1l11lll_opy_ (u"ࠫࡊࡘࡒࡠࡖࡘࡒࡓࡋࡌࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬᢼ"),
  bstack1l11lll_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡔࡊࡏࡈࡈࡤࡕࡕࡕࠩᢽ"),
  bstack1l11lll_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡔࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᢾ"),
  bstack1l11lll_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡉࡑࡖࡘࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪᢿ"),
  bstack1l11lll_opy_ (u"ࠨࡇࡕࡖࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᣀ"),
  bstack1l11lll_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪᣁ"),
  bstack1l11lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡘࡅࡔࡑࡏ࡙࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᣂ"),
  bstack1l11lll_opy_ (u"ࠫࡊࡘࡒࡠࡏࡄࡒࡉࡇࡔࡐࡔ࡜ࡣࡕࡘࡏ࡙࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᣃ"),
]
bstack1ll11l1l_opy_ = bstack1l11lll_opy_ (u"ࠬ࠴࠯ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠱ࠪᣄ")
bstack1l1ll1ll1l_opy_ = os.path.join(os.path.expanduser(bstack1l11lll_opy_ (u"࠭ࡾࠨᣅ")), bstack1l11lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᣆ"), bstack1l11lll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᣇ"))
bstack11llll11l1l_opy_ = bstack1l11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱ࡫ࠪᣈ")
bstack11ll1ll1l1l_opy_ = [ bstack1l11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᣉ"), bstack1l11lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᣊ"), bstack1l11lll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫᣋ"), bstack1l11lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᣌ")]
bstack1111l1ll_opy_ = [ bstack1l11lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᣍ"), bstack1l11lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᣎ"), bstack1l11lll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨᣏ"), bstack1l11lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᣐ") ]
bstack11llll1ll1_opy_ = [ bstack1l11lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᣑ") ]
bstack1l1l111111_opy_ = 360
bstack11lll1l1111_opy_ = bstack1l11lll_opy_ (u"ࠧࡧࡰࡱ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧᣒ")
bstack11ll1ll1ll1_opy_ = bstack1l11lll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡫ࡶࡷࡺ࡫ࡳࠣᣓ")
bstack11ll1ll1lll_opy_ = bstack1l11lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠥᣔ")
bstack11llll11lll_opy_ = bstack1l11lll_opy_ (u"ࠣࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡷࡩࡸࡺࡳࠡࡣࡵࡩࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡔ࡙ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠧࡶࠤࡦࡴࡤࠡࡣࡥࡳࡻ࡫ࠠࡧࡱࡵࠤࡆࡴࡤࡳࡱ࡬ࡨࠥࡪࡥࡷ࡫ࡦࡩࡸ࠴ࠢᣕ")
bstack11llllll111_opy_ = bstack1l11lll_opy_ (u"ࠤ࠴࠵࠳࠶ࠢᣖ")
bstack111ll1111l_opy_ = {
  bstack1l11lll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨᣗ"): bstack1l11lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᣘ"),
  bstack1l11lll_opy_ (u"ࠬࡌࡁࡊࡎࠪᣙ"): bstack1l11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᣚ"),
  bstack1l11lll_opy_ (u"ࠧࡔࡍࡌࡔࠬᣛ"): bstack1l11lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᣜ")
}
bstack1lll1llll1_opy_ = [
  bstack1l11lll_opy_ (u"ࠤࡪࡩࡹࠨᣝ"),
  bstack1l11lll_opy_ (u"ࠥ࡫ࡴࡈࡡࡤ࡭ࠥᣞ"),
  bstack1l11lll_opy_ (u"ࠦ࡬ࡵࡆࡰࡴࡺࡥࡷࡪࠢᣟ"),
  bstack1l11lll_opy_ (u"ࠧࡸࡥࡧࡴࡨࡷ࡭ࠨᣠ"),
  bstack1l11lll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧᣡ"),
  bstack1l11lll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᣢ"),
  bstack1l11lll_opy_ (u"ࠣࡵࡸࡦࡲ࡯ࡴࡆ࡮ࡨࡱࡪࡴࡴࠣᣣ"),
  bstack1l11lll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨᣤ"),
  bstack1l11lll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨᣥ"),
  bstack1l11lll_opy_ (u"ࠦࡨࡲࡥࡢࡴࡈࡰࡪࡳࡥ࡯ࡶࠥᣦ"),
  bstack1l11lll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࡸࠨᣧ"),
  bstack1l11lll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹࠨᣨ"),
  bstack1l11lll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡂࡵࡼࡲࡨ࡙ࡣࡳ࡫ࡳࡸࠧᣩ"),
  bstack1l11lll_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢᣪ"),
  bstack1l11lll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᣫ"),
  bstack1l11lll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡘࡴࡻࡣࡩࡃࡦࡸ࡮ࡵ࡮ࠣᣬ"),
  bstack1l11lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡒࡻ࡬ࡵ࡫ࡗࡳࡺࡩࡨࠣᣭ"),
  bstack1l11lll_opy_ (u"ࠧࡹࡨࡢ࡭ࡨࠦᣮ"),
  bstack1l11lll_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࡆࡶࡰࠣᣯ")
]
bstack11lll11111l_opy_ = [
  bstack1l11lll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨᣰ"),
  bstack1l11lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᣱ"),
  bstack1l11lll_opy_ (u"ࠤࡤࡹࡹࡵࠢᣲ"),
  bstack1l11lll_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥᣳ"),
  bstack1l11lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᣴ")
]
bstack1l11llll1l_opy_ = {
  bstack1l11lll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦᣵ"): [bstack1l11lll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ᣶")],
  bstack1l11lll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᣷"): [bstack1l11lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᣸")],
  bstack1l11lll_opy_ (u"ࠤࡤࡹࡹࡵࠢ᣹"): [bstack1l11lll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢ᣺"), bstack1l11lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢ᣻"), bstack1l11lll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ᣼"), bstack1l11lll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ᣽")],
  bstack1l11lll_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢ᣾"): [bstack1l11lll_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣ᣿")],
  bstack1l11lll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᤀ"): [bstack1l11lll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᤁ")],
}
bstack11ll1ll1l11_opy_ = {
  bstack1l11lll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥᤂ"): bstack1l11lll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦᤃ"),
  bstack1l11lll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᤄ"): bstack1l11lll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᤅ"),
  bstack1l11lll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧᤆ"): bstack1l11lll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦᤇ"),
  bstack1l11lll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨᤈ"): bstack1l11lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨᤉ"),
  bstack1l11lll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᤊ"): bstack1l11lll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᤋ")
}
bstack111ll111ll_opy_ = {
  bstack1l11lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᤌ"): bstack1l11lll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡔࡧࡷࡹࡵ࠭ᤍ"),
  bstack1l11lll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᤎ"): bstack1l11lll_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡗࡩࡦࡸࡤࡰࡹࡱࠫᤏ"),
  bstack1l11lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᤐ"): bstack1l11lll_opy_ (u"࡚ࠬࡥࡴࡶࠣࡗࡪࡺࡵࡱࠩᤑ"),
  bstack1l11lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᤒ"): bstack1l11lll_opy_ (u"ࠧࡕࡧࡶࡸ࡚ࠥࡥࡢࡴࡧࡳࡼࡴࠧᤓ")
}
bstack11ll1lll111_opy_ = 65536
bstack11ll1l1ll1l_opy_ = bstack1l11lll_opy_ (u"ࠨ࠰࠱࠲ࡠ࡚ࡒࡖࡐࡆࡅ࡙ࡋࡄ࡞ࠩᤔ")
bstack11ll1l1lll1_opy_ = [
      bstack1l11lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᤕ"), bstack1l11lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᤖ"), bstack1l11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᤗ"), bstack1l11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᤘ"), bstack1l11lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨᤙ"),
      bstack1l11lll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᤚ"), bstack1l11lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫᤛ"), bstack1l11lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᤜ"), bstack1l11lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫᤝ"),
      bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᤞ"), bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᤟"), bstack1l11lll_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩᤠ")
    ]
bstack11ll1l111l1_opy_= {
  bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᤡ"): bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᤢ"),
  bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᤣ"): bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᤤ"),
  bstack1l11lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪᤥ"): bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤦ"),
  bstack1l11lll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᤧ"): bstack1l11lll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᤨ"),
  bstack1l11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᤩ"): bstack1l11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᤪ"),
  bstack1l11lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᤫ"): bstack1l11lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭᤬"),
  bstack1l11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ᤭"): bstack1l11lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᤮"),
  bstack1l11lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᤯"): bstack1l11lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᤰ"),
  bstack1l11lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᤱ"): bstack1l11lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᤲ"),
  bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤳ"): bstack1l11lll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᤴ"),
  bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᤵ"): bstack1l11lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᤶ"),
  bstack1l11lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᤷ"): bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᤸ"),
  bstack1l11lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷ᤹ࠬ"): bstack1l11lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭᤺"),
  bstack1l11lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯᤻ࠩ"): bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᤼"),
  bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᤽"): bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᤾"),
  bstack1l11lll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭᤿"): bstack1l11lll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧ᥀"),
  bstack1l11lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ᥁"): bstack1l11lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᥂"),
  bstack1l11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬ᥃"): bstack1l11lll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᥄"),
  bstack1l11lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫ᥅"): bstack1l11lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ᥆"),
  bstack1l11lll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ᥇"): bstack1l11lll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭᥈"),
  bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᥉"): bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᥊"),
  bstack1l11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᥋"): bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᥌"),
  bstack1l11lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭᥍"): bstack1l11lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ᥎"),
  bstack1l11lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᥏"): bstack1l11lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᥐ"),
  bstack1l11lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᥑ"): bstack1l11lll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᥒ")
}
bstack11ll1l111ll_opy_ = [bstack1l11lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᥓ"), bstack1l11lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᥔ")]
bstack11ll1l1l1_opy_ = (bstack1l11lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᥕ"),)
bstack11ll1l11l1l_opy_ = bstack1l11lll_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡺࡶࡤࡢࡶࡨࡣࡨࡲࡩࠨᥖ")
bstack1llllll1l1_opy_ = bstack1l11lll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡩࡵ࡭ࡩࡹ࠯ࠣᥗ")
bstack1lll111ll1_opy_ = bstack1l11lll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨࡴ࡬ࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡤࡷ࡭ࡨ࡯ࡢࡴࡧ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࠧᥘ")
bstack1111lll1l_opy_ = bstack1l11lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠰ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠣᥙ")
class EVENTS(Enum):
  bstack11ll1l1l111_opy_ = bstack1l11lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࠱࠲ࡻ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬᥚ")
  bstack111l11111_opy_ = bstack1l11lll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࠧᥛ") # final bstack11ll11lll1l_opy_
  bstack11ll1lll1l1_opy_ = bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡱࡨࡱࡵࡧࡴࠩᥜ")
  bstack1lll1llll_opy_ = bstack1l11lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠿ࡶࡲࡪࡰࡷ࠱ࡧࡻࡩ࡭ࡦ࡯࡭ࡳࡱࠧᥝ") #shift post bstack11ll1llllll_opy_
  bstack1ll11l1ll1_opy_ = bstack1l11lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭ᥞ") #shift post bstack11ll1llllll_opy_
  bstack11ll1llll1l_opy_ = bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡩࡷࡥࠫᥟ") #shift
  bstack11ll1l11ll1_opy_ = bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡨࡴࡽ࡮࡭ࡱࡤࡨࠬᥠ") #shift
  bstack11l11l1l1l_opy_ = bstack1l11lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪᥡ")
  bstack1ll1l1l1ll1_opy_ = bstack1l11lll_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾ࡸࡧࡶࡦ࠯ࡵࡩࡸࡻ࡬ࡵࡵࠪᥢ")
  bstack1111l11ll_opy_ = bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡶࡥࡳࡨࡲࡶࡲࡹࡣࡢࡰࠪᥣ")
  bstack1lllll1ll1_opy_ = bstack1l11lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡰࡴࡩࡡ࡭ࠩᥤ") #shift
  bstack1111l11l_opy_ = bstack1l11lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡣࡳࡴ࠲ࡻࡰ࡭ࡱࡤࡨࠬᥥ") #shift
  bstack1ll1lll11_opy_ = bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡩࡩ࠮ࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠫᥦ")
  bstack1ll111lll_opy_ = bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡪࡩࡹ࠳ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠳ࡲࡦࡵࡸࡰࡹࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨᥧ") #shift
  bstack11l1llll11_opy_ = bstack1l11lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠭ࡳࡧࡶࡹࡱࡺࡳࠨᥨ") #shift
  bstack11ll1ll11ll_opy_ = bstack1l11lll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽࠬᥩ") #shift
  bstack1l1ll1l111l_opy_ = bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᥪ")
  bstack11l1lll11_opy_ = bstack1l11lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡸࡺࡡࡵࡷࡶࠫᥫ") #shift
  bstack1l1llllll1_opy_ = bstack1l11lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾࡭ࡻࡢ࠮࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠬᥬ")
  bstack11ll1l11l11_opy_ = bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷࡵࡸࡺ࠯ࡶࡩࡹࡻࡰࠨᥭ") #shift
  bstack1llll11l1_opy_ = bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫ࡴࡶࡲࠪ᥮")
  bstack11lll1111l1_opy_ = bstack1l11lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡴࡡࡱࡵ࡫ࡳࡹ࠭᥯") # not bstack11ll1l1llll_opy_ in python
  bstack11ll1111l1_opy_ = bstack1l11lll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡱࡶ࡫ࡷࠫᥰ") # used in bstack11ll1ll11l1_opy_
  bstack1l1l11ll1_opy_ = bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡨࡧࡷࠫᥱ") # used in bstack11ll1ll11l1_opy_
  bstack11l111l1_opy_ = bstack1l11lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡪࡲࡳࡰ࠭ᥲ")
  bstack1llll1l111_opy_ = bstack1l11lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠪᥳ")
  bstack1l1ll1l1ll_opy_ = bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠪᥴ") #
  bstack11lll1ll1_opy_ = bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡴ࠷࠱ࡺ࠼ࡧࡶ࡮ࡼࡥࡳ࠯ࡷࡥࡰ࡫ࡓࡤࡴࡨࡩࡳ࡙ࡨࡰࡶࠪ᥵")
  bstack1l11ll1l1l_opy_ = bstack1l11lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡦࡻࡴࡰ࠯ࡦࡥࡵࡺࡵࡳࡧࠪ᥶")
  bstack1111l1l1l_opy_ = bstack1l11lll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡧ࠰ࡸࡪࡹࡴࠨ᥷")
  bstack1l1lllllll_opy_ = bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡱࡶࡸ࠲ࡺࡥࡴࡶࠪ᥸")
  bstack11lll1l11l_opy_ = bstack1l11lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡵࡩ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᥹") #shift
  bstack11l1111ll_opy_ = bstack1l11lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡳࡸࡺ࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨ᥺") #shift
  bstack11ll1llll11_opy_ = bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࠮ࡥࡤࡴࡹࡻࡲࡦࠩ᥻")
  bstack11ll1lllll1_opy_ = bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡩࡥ࡮ࡨ࠱ࡹ࡯࡭ࡦࡱࡸࡸࠬ᥼")
  bstack1lll1ll1111_opy_ = bstack1l11lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡶࡸࡦࡸࡴࠨ᥽")
  bstack11ll1ll111l_opy_ = bstack1l11lll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡨࡴࡽ࡮࡭ࡱࡤࡨࠬ᥾")
  bstack11ll1l1l11l_opy_ = bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡨ࡮ࡥࡤ࡭࠰ࡹࡵࡪࡡࡵࡧࠪ᥿")
  bstack1lll1111ll1_opy_ = bstack1l11lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡤࡲࡳࡹࡹࡴࡳࡣࡳࠫᦀ")
  bstack1lll111111l_opy_ = bstack1l11lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡦࡳࡳࡴࡥࡤࡶࠪᦁ")
  bstack1lll11l11l1_opy_ = bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡷࡹࡵࡰࠨᦂ")
  bstack1lll111l11l_opy_ = bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭ᦃ")
  bstack1ll1llllll1_opy_ = bstack1l11lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩᦄ")
  bstack11ll1l1111l_opy_ = bstack1l11lll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠪᦅ")
  bstack11ll1ll1111_opy_ = bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡨࡓ࡫ࡡࡳࡧࡶࡸࡍࡻࡢࠨᦆ")
  bstack1l1l11ll11l_opy_ = bstack1l11lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡉ࡯࡫ࡷࠫᦇ")
  bstack1l1l1l1111l_opy_ = bstack1l11lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡶࡹ࠭ᦈ")
  bstack1ll1l1111l1_opy_ = bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡆࡳࡳ࡬ࡩࡨࠩᦉ")
  bstack11ll1l1l1l1_opy_ = bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪᦊ")
  bstack1ll11ll1l1l_opy_ = bstack1l11lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡩࡔࡧ࡯ࡪࡍ࡫ࡡ࡭ࡕࡷࡩࡵ࠭ᦋ")
  bstack1ll11ll1lll_opy_ = bstack1l11lll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡊࡩࡹࡘࡥࡴࡷ࡯ࡸࠬᦌ")
  bstack1l1lll111l1_opy_ = bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡅࡷࡧࡱࡸࠬᦍ")
  bstack1ll1111llll_opy_ = bstack1l11lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠫᦎ")
  bstack1l1lll11111_opy_ = bstack1l11lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡬ࡰࡩࡆࡶࡪࡧࡴࡦࡦࡈࡺࡪࡴࡴࠨᦏ")
  bstack11ll11llll1_opy_ = bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡦࡰࡴࡹࡪࡻࡥࡕࡧࡶࡸࡊࡼࡥ࡯ࡶࠪᦐ")
  bstack1l1l11ll111_opy_ = bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡴࡶࠧᦑ")
  bstack1llllll1lll_opy_ = bstack1l11lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࡮ࡔࡶࡲࡴࠬᦒ")
class STAGE(Enum):
  bstack1l1111l1_opy_ = bstack1l11lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨᦓ")
  END = bstack1l11lll_opy_ (u"ࠪࡩࡳࡪࠧᦔ")
  bstack1l1ll11ll1_opy_ = bstack1l11lll_opy_ (u"ࠫࡸ࡯࡮ࡨ࡮ࡨࠫᦕ")
bstack1llllll11l_opy_ = {
  bstack1l11lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬᦖ"): bstack1l11lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᦗ"),
  bstack1l11lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫᦘ"): bstack1l11lll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᦙ")
}
PLAYWRIGHT_HUB_URL = bstack1l11lll_opy_ (u"ࠤࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠦᦚ")