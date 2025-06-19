# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import re
from enum import Enum
bstack11ll1l1l1l_opy_ = {
  bstack111lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ᜙"): bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪ᜚"),
  bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ᜛"): bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫ᜜"),
  bstack111lll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᜝"): bstack111lll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᜞"),
  bstack111lll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᜟ"): bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᜠ"),
  bstack111lll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᜡ"): bstack111lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨᜢ"),
  bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᜣ"): bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨᜤ"),
  bstack111lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᜥ"): bstack111lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᜦ"),
  bstack111lll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᜧ"): bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫᜨ"),
  bstack111lll_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬᜩ"): bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨᜪ"),
  bstack111lll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᜫ"): bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᜬ"),
  bstack111lll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᜭ"): bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᜮ"),
  bstack111lll_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬᜯ"): bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬᜰ"),
  bstack111lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᜱ"): bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᜲ"),
  bstack111lll_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᜳ"): bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵ᜴ࠪ"),
  bstack111lll_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪ᜵"): bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪ᜶"),
  bstack111lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩ᜷"): bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩ᜸"),
  bstack111lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ᜹"): bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᜺"),
  bstack111lll_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪ᜻"): bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪ᜼"),
  bstack111lll_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ᜽"): bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ᜾"),
  bstack111lll_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨ᜿"): bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᝀ"),
  bstack111lll_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬᝁ"): bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬᝂ"),
  bstack111lll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᝃ"): bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᝄ"),
  bstack111lll_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ᝅ"): bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭ᝆ"),
  bstack111lll_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪᝇ"): bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪᝈ"),
  bstack111lll_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᝉ"): bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᝊ"),
  bstack111lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᝋ"): bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᝌ"),
  bstack111lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᝍ"): bstack111lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᝎ"),
  bstack111lll_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᝏ"): bstack111lll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩᝐ"),
  bstack111lll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᝑ"): bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᝒ"),
  bstack111lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᝓ"): bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ᝔"),
  bstack111lll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ᝕"): bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ᝖"),
  bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ᝗"): bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭᝘"),
  bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᝙"): bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᝚"),
  bstack111lll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ᝛"): bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨ᝜"),
  bstack111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᝝"): bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᝞"),
  bstack111lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ᝟"): bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᝠ"),
  bstack111lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᝡ"): bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᝢ"),
  bstack111lll_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᝣ"): bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᝤ"),
  bstack111lll_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᝥ"): bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᝦ"),
  bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᝧ"): bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᝨ"),
  bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᝩ"): bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᝪ")
}
bstack11ll111ll1l_opy_ = [
  bstack111lll_opy_ (u"ࠪࡳࡸ࠭ᝫ"),
  bstack111lll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᝬ"),
  bstack111lll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᝭"),
  bstack111lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᝮ"),
  bstack111lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᝯ"),
  bstack111lll_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᝰ"),
  bstack111lll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᝱"),
]
bstack1111l11l1_opy_ = {
  bstack111lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᝲ"): [bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᝳ"), bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡑࡅࡒࡋࠧ᝴")],
  bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ᝵"): bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ᝶"),
  bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ᝷"): bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬ᝸"),
  bstack111lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ᝹"): bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠩ᝺"),
  bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᝻"): bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ᝼"),
  bstack111lll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᝽"): bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡕࡢࡔࡊࡘ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩ᝾"),
  bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᝿"): bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨក"),
  bstack111lll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨខ"): bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩគ"),
  bstack111lll_opy_ (u"࠭ࡡࡱࡲࠪឃ"): [bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࡢࡍࡉ࠭ង"), bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࠫច")],
  bstack111lll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫឆ"): bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡌࡐࡉࡏࡉ࡛ࡋࡌࠨជ"),
  bstack111lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨឈ"): bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨញ"),
  bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪដ"): bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠫឋ"),
  bstack111lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬឌ"): bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡘࡖࡇࡕࡓࡄࡃࡏࡉࠬឍ")
}
bstack1l11l1ll1_opy_ = {
  bstack111lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬណ"): [bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ត"), bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡐࡤࡱࡪ࠭ថ")],
  bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩទ"): [bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡥ࡫ࡦࡻࠪធ"), bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪន")],
  bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬប"): bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬផ"),
  bstack111lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩព"): bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩភ"),
  bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨម"): bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨយ"),
  bstack111lll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨរ"): [bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡳࡴࠬល"), bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩវ")],
  bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨឝ"): bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪឞ"),
  bstack111lll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪស"): bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪហ"),
  bstack111lll_opy_ (u"ࠨࡣࡳࡴࠬឡ"): bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴࠬអ"),
  bstack111lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬឣ"): bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴ࡭ࡌࡦࡸࡨࡰࠬឤ"),
  bstack111lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩឥ"): bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩឦ")
}
bstack1lll1l1l11_opy_ = {
  bstack111lll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪឧ"): bstack111lll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬឨ"),
  bstack111lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫឩ"): [bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬឪ"), bstack111lll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧឫ")],
  bstack111lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪឬ"): bstack111lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫឭ"),
  bstack111lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫឮ"): bstack111lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨឯ"),
  bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧឰ"): [bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫឱ"), bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪឲ")],
  bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ឳ"): bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ឴"),
  bstack111lll_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ឵"): bstack111lll_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭ា"),
  bstack111lll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩិ"): [bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪី"), bstack111lll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬឹ")],
  bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫឺ"): [bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧុ"), bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࠧូ")]
}
bstack11ll1l1l_opy_ = [
  bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧួ"),
  bstack111lll_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬើ"),
  bstack111lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩឿ"),
  bstack111lll_opy_ (u"ࠫࡸ࡫ࡴࡘ࡫ࡱࡨࡴࡽࡒࡦࡥࡷࠫៀ"),
  bstack111lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧេ"),
  bstack111lll_opy_ (u"࠭ࡳࡵࡴ࡬ࡧࡹࡌࡩ࡭ࡧࡌࡲࡹ࡫ࡲࡢࡥࡷࡥࡧ࡯࡬ࡪࡶࡼࠫែ"),
  bstack111lll_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪៃ"),
  bstack111lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ោ"),
  bstack111lll_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧៅ"),
  bstack111lll_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫំ"),
  bstack111lll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪះ"),
  bstack111lll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ៈ"),
]
bstack11ll1l11l1_opy_ = [
  bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ៉"),
  bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ៊"),
  bstack111lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ់"),
  bstack111lll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ៌"),
  bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭៍"),
  bstack111lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭៎"),
  bstack111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ៏"),
  bstack111lll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ័"),
  bstack111lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ៑"),
  bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ្࠭"),
  bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭៓"),
  bstack111lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬ។"),
  bstack111lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡘࡦ࡭ࠧ៕"),
  bstack111lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ៖"),
  bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨៗ"),
  bstack111lll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ៘"),
  bstack111lll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠷ࠧ៙"),
  bstack111lll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠲ࠨ៚"),
  bstack111lll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠴ࠩ៛"),
  bstack111lll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠶ࠪៜ"),
  bstack111lll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠸ࠫ៝"),
  bstack111lll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠺ࠬ៞"),
  bstack111lll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠼࠭៟"),
  bstack111lll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠾ࠧ០"),
  bstack111lll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠹ࠨ១"),
  bstack111lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ២"),
  bstack111lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ៣"),
  bstack111lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨ៤"),
  bstack111lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ៥"),
  bstack111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ៦"),
  bstack111lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬ៧"),
  bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭៨")
]
bstack11ll11l1l1l_opy_ = [
  bstack111lll_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨ៩"),
  bstack111lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭៪"),
  bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ៫"),
  bstack111lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ៬"),
  bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡕࡸࡩࡰࡴ࡬ࡸࡾ࠭៭"),
  bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ៮"),
  bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡕࡣࡪࠫ៯"),
  bstack111lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ៰"),
  bstack111lll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭៱"),
  bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ៲"),
  bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ៳"),
  bstack111lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭៴"),
  bstack111lll_opy_ (u"ࠨࡱࡶࠫ៵"),
  bstack111lll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ៶"),
  bstack111lll_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩ៷"),
  bstack111lll_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭៸"),
  bstack111lll_opy_ (u"ࠬࡸࡥࡨ࡫ࡲࡲࠬ៹"),
  bstack111lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨ៺"),
  bstack111lll_opy_ (u"ࠧ࡮ࡣࡦ࡬࡮ࡴࡥࠨ៻"),
  bstack111lll_opy_ (u"ࠨࡴࡨࡷࡴࡲࡵࡵ࡫ࡲࡲࠬ៼"),
  bstack111lll_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧ៽"),
  bstack111lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧ៾"),
  bstack111lll_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪ៿"),
  bstack111lll_opy_ (u"ࠬࡴ࡯ࡑࡣࡪࡩࡑࡵࡡࡥࡖ࡬ࡱࡪࡵࡵࡵࠩ᠀"),
  bstack111lll_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧ᠁"),
  bstack111lll_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭᠂"),
  bstack111lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ᠃"),
  bstack111lll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡨࡲࡩࡑࡥࡺࡵࠪ᠄"),
  bstack111lll_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ᠅"),
  bstack111lll_opy_ (u"ࠫࡳࡵࡐࡪࡲࡨࡰ࡮ࡴࡥࠨ᠆"),
  bstack111lll_opy_ (u"ࠬࡩࡨࡦࡥ࡮࡙ࡗࡒࠧ᠇"),
  bstack111lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᠈"),
  bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡃࡰࡱ࡮࡭ࡪࡹࠧ᠉"),
  bstack111lll_opy_ (u"ࠨࡥࡤࡴࡹࡻࡲࡦࡅࡵࡥࡸ࡮ࠧ᠊"),
  bstack111lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭᠋"),
  bstack111lll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ᠌"),
  bstack111lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᠍"),
  bstack111lll_opy_ (u"ࠬࡴ࡯ࡃ࡮ࡤࡲࡰࡖ࡯࡭࡮࡬ࡲ࡬࠭᠎"),
  bstack111lll_opy_ (u"࠭࡭ࡢࡵ࡮ࡗࡪࡴࡤࡌࡧࡼࡷࠬ᠏"),
  bstack111lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡌࡰࡩࡶࠫ᠐"),
  bstack111lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡊࡦࠪ᠑"),
  bstack111lll_opy_ (u"ࠩࡧࡩࡩ࡯ࡣࡢࡶࡨࡨࡉ࡫ࡶࡪࡥࡨࠫ᠒"),
  bstack111lll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡓࡥࡷࡧ࡭ࡴࠩ᠓"),
  bstack111lll_opy_ (u"ࠫࡵ࡮࡯࡯ࡧࡑࡹࡲࡨࡥࡳࠩ᠔"),
  bstack111lll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪ᠕"),
  bstack111lll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡓࡵࡺࡩࡰࡰࡶࠫ᠖"),
  bstack111lll_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬ᠗"),
  bstack111lll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ᠘"),
  bstack111lll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭᠙"),
  bstack111lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡅ࡭ࡴࡳࡥࡵࡴ࡬ࡧࠬ᠚"),
  bstack111lll_opy_ (u"ࠫࡻ࡯ࡤࡦࡱ࡙࠶ࠬ᠛"),
  bstack111lll_opy_ (u"ࠬࡳࡩࡥࡕࡨࡷࡸ࡯࡯࡯ࡋࡱࡷࡹࡧ࡬࡭ࡃࡳࡴࡸ࠭᠜"),
  bstack111lll_opy_ (u"࠭ࡥࡴࡲࡵࡩࡸࡹ࡯ࡔࡧࡵࡺࡪࡸࠧ᠝"),
  bstack111lll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭᠞"),
  bstack111lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡆࡨࡵ࠭᠟"),
  bstack111lll_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᠠ"),
  bstack111lll_opy_ (u"ࠪࡷࡾࡴࡣࡕ࡫ࡰࡩ࡜࡯ࡴࡩࡐࡗࡔࠬᠡ"),
  bstack111lll_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᠢ"),
  bstack111lll_opy_ (u"ࠬ࡭ࡰࡴࡎࡲࡧࡦࡺࡩࡰࡰࠪᠣ"),
  bstack111lll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧᠤ"),
  bstack111lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᠥ"),
  bstack111lll_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࡃࡩࡣࡱ࡫ࡪࡐࡡࡳࠩᠦ"),
  bstack111lll_opy_ (u"ࠩࡻࡱࡸࡐࡡࡳࠩᠧ"),
  bstack111lll_opy_ (u"ࠪࡼࡲࡾࡊࡢࡴࠪᠨ"),
  bstack111lll_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪᠩ"),
  bstack111lll_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬᠪ"),
  bstack111lll_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧᠫ"),
  bstack111lll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪᠬ"),
  bstack111lll_opy_ (u"ࠨࡣࡳࡴ࡛࡫ࡲࡴ࡫ࡲࡲࠬᠭ"),
  bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᠮ"),
  bstack111lll_opy_ (u"ࠪࡶࡪࡹࡩࡨࡰࡄࡴࡵ࠭ᠯ"),
  bstack111lll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࡳࠨᠰ"),
  bstack111lll_opy_ (u"ࠬࡩࡡ࡯ࡣࡵࡽࠬᠱ"),
  bstack111lll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᠲ"),
  bstack111lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᠳ"),
  bstack111lll_opy_ (u"ࠨ࡫ࡨࠫᠴ"),
  bstack111lll_opy_ (u"ࠩࡨࡨ࡬࡫ࠧᠵ"),
  bstack111lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪᠶ"),
  bstack111lll_opy_ (u"ࠫࡶࡻࡥࡶࡧࠪᠷ"),
  bstack111lll_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡲࡦࡲࠧᠸ"),
  bstack111lll_opy_ (u"࠭ࡡࡱࡲࡖࡸࡴࡸࡥࡄࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠧᠹ"),
  bstack111lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡃࡢ࡯ࡨࡶࡦࡏ࡭ࡢࡩࡨࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭ᠺ"),
  bstack111lll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡋࡸࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫᠻ"),
  bstack111lll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡉ࡯ࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬᠼ"),
  bstack111lll_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᠽ"),
  bstack111lll_opy_ (u"ࠫࡷ࡫ࡳࡦࡴࡹࡩࡉ࡫ࡶࡪࡥࡨࠫᠾ"),
  bstack111lll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᠿ"),
  bstack111lll_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨᡀ"),
  bstack111lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡢࡵࡶࡧࡴࡪࡥࠨᡁ"),
  bstack111lll_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡊࡱࡶࡈࡪࡼࡩࡤࡧࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᡂ"),
  bstack111lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡸࡨ࡮ࡵࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩᡃ"),
  bstack111lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡴࡵࡲࡥࡑࡣࡼࠫᡄ"),
  bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᡅ"),
  bstack111lll_opy_ (u"ࠬࡽࡤࡪࡱࡖࡩࡷࡼࡩࡤࡧࠪᡆ"),
  bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᡇ"),
  bstack111lll_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡄࡴࡲࡷࡸ࡙ࡩࡵࡧࡗࡶࡦࡩ࡫ࡪࡰࡪࠫᡈ"),
  bstack111lll_opy_ (u"ࠨࡪ࡬࡫࡭ࡉ࡯࡯ࡶࡵࡥࡸࡺࠧᡉ"),
  bstack111lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡒࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࡸ࠭ᡊ"),
  bstack111lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ᡋ"),
  bstack111lll_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨᡌ"),
  bstack111lll_opy_ (u"ࠬࡸࡥ࡮ࡱࡹࡩࡎࡕࡓࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࡑࡵࡣࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᡍ"),
  bstack111lll_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨᡎ"),
  bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᡏ"),
  bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᡐ"),
  bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᡑ"),
  bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᡒ"),
  bstack111lll_opy_ (u"ࠫࡵࡧࡧࡦࡎࡲࡥࡩ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧᡓ"),
  bstack111lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫᡔ"),
  bstack111lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࡳࠨᡕ"),
  bstack111lll_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪᡖ")
]
bstack1111ll11_opy_ = {
  bstack111lll_opy_ (u"ࠨࡸࠪᡗ"): bstack111lll_opy_ (u"ࠩࡹࠫᡘ"),
  bstack111lll_opy_ (u"ࠪࡪࠬᡙ"): bstack111lll_opy_ (u"ࠫ࡫࠭ᡚ"),
  bstack111lll_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫᡛ"): bstack111lll_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬᡜ"),
  bstack111lll_opy_ (u"ࠧࡰࡰ࡯ࡽࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᡝ"): bstack111lll_opy_ (u"ࠨࡱࡱࡰࡾࡇࡵࡵࡱࡰࡥࡹ࡫ࠧᡞ"),
  bstack111lll_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭ᡟ"): bstack111lll_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧᡠ"),
  bstack111lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧᡡ"): bstack111lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨᡢ"),
  bstack111lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩᡣ"): bstack111lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᡤ"),
  bstack111lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᡥ"): bstack111lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᡦ"),
  bstack111lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᡧ"): bstack111lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᡨ"),
  bstack111lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭ᡩ"): bstack111lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᡪ"),
  bstack111lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨᡫ"): bstack111lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩᡬ"),
  bstack111lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᡭ"): bstack111lll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᡮ"),
  bstack111lll_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᡯ"): bstack111lll_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᡰ"),
  bstack111lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᡱ"): bstack111lll_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᡲ"),
  bstack111lll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᡳ"): bstack111lll_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫᡴ"),
  bstack111lll_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧᡵ"): bstack111lll_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨᡶ"),
  bstack111lll_opy_ (u"ࠬࡶࡡࡤࡨ࡬ࡰࡪ࠭ᡷ"): bstack111lll_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᡸ"),
  bstack111lll_opy_ (u"ࠧࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ᡹"): bstack111lll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ᡺"),
  bstack111lll_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ᡻"): bstack111lll_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭᡼"),
  bstack111lll_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬ᡽"): bstack111lll_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭᡾"),
  bstack111lll_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᡿"): bstack111lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᢀ"),
  bstack111lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠪᢁ"): bstack111lll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡴࡪࡧࡴࡦࡴࠪᢂ")
}
bstack11l1lllllll_opy_ = bstack111lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬࡯ࡴࡩࡷࡥ࠲ࡨࡵ࡭࠰ࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬࠳ࡷ࡫࡬ࡦࡣࡶࡩࡸ࠵࡬ࡢࡶࡨࡷࡹ࠵ࡤࡰࡹࡱࡰࡴࡧࡤࠣᢃ")
bstack11ll1111l1l_opy_ = bstack111lll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠳࡭࡫ࡡ࡭ࡶ࡫ࡧ࡭࡫ࡣ࡬ࠤᢄ")
bstack111l11l11_opy_ = bstack111lll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡥࡥࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡳࡦࡰࡧࡣࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣᢅ")
bstack1l1ll1ll_opy_ = bstack111lll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧᢆ")
bstack11ll1lll_opy_ = bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪᢇ")
bstack11111l1l_opy_ = bstack111lll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬᢈ")
bstack11ll111111l_opy_ = {
  bstack111lll_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫᢉ"): 50,
  bstack111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᢊ"): 40,
  bstack111lll_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬᢋ"): 30,
  bstack111lll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᢌ"): 20,
  bstack111lll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᢍ"): 10
}
bstack11llll111_opy_ = bstack11ll111111l_opy_[bstack111lll_opy_ (u"ࠧࡪࡰࡩࡳࠬᢎ")]
bstack111l11111_opy_ = bstack111lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᢏ")
bstack1l111l1l_opy_ = bstack111lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᢐ")
bstack111l1ll1_opy_ = bstack111lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᢑ")
bstack111lllll_opy_ = bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪᢒ")
bstack11l1l1ll1l_opy_ = bstack111lll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪᢓ")
bstack11l1lllll11_opy_ = [bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᢔ"), bstack111lll_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᢕ")]
bstack11l1lllll1l_opy_ = [bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᢖ"), bstack111lll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᢗ")]
bstack1l1lll111l_opy_ = re.compile(bstack111lll_opy_ (u"ࠪࡢࡠࡢ࡜ࡸ࠯ࡠ࠯࠿࠴ࠪࠥࠩᢘ"))
bstack1llll11lll_opy_ = [
  bstack111lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡏࡣࡰࡩࠬᢙ"),
  bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᢚ"),
  bstack111lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᢛ"),
  bstack111lll_opy_ (u"ࠧ࡯ࡧࡺࡇࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࠫᢜ"),
  bstack111lll_opy_ (u"ࠨࡣࡳࡴࠬᢝ"),
  bstack111lll_opy_ (u"ࠩࡸࡨ࡮ࡪࠧᢞ"),
  bstack111lll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬᢟ"),
  bstack111lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࠫᢠ"),
  bstack111lll_opy_ (u"ࠬࡵࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪᢡ"),
  bstack111lll_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࠫᢢ"),
  bstack111lll_opy_ (u"ࠧ࡯ࡱࡕࡩࡸ࡫ࡴࠨᢣ"), bstack111lll_opy_ (u"ࠨࡨࡸࡰࡱࡘࡥࡴࡧࡷࠫᢤ"),
  bstack111lll_opy_ (u"ࠩࡦࡰࡪࡧࡲࡔࡻࡶࡸࡪࡳࡆࡪ࡮ࡨࡷࠬᢥ"),
  bstack111lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡖ࡬ࡱ࡮ࡴࡧࡴࠩᢦ"),
  bstack111lll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࡍࡱࡪ࡫࡮ࡴࡧࠨᢧ"),
  bstack111lll_opy_ (u"ࠬࡵࡴࡩࡧࡵࡅࡵࡶࡳࠨᢨ"),
  bstack111lll_opy_ (u"࠭ࡰࡳ࡫ࡱࡸࡕࡧࡧࡦࡕࡲࡹࡷࡩࡥࡐࡰࡉ࡭ࡳࡪࡆࡢ࡫࡯ࡹࡷ࡫ᢩࠧ"),
  bstack111lll_opy_ (u"ࠧࡢࡲࡳࡅࡨࡺࡩࡷ࡫ࡷࡽࠬᢪ"), bstack111lll_opy_ (u"ࠨࡣࡳࡴࡕࡧࡣ࡬ࡣࡪࡩࠬ᢫"), bstack111lll_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡄࡧࡹ࡯ࡶࡪࡶࡼࠫ᢬"), bstack111lll_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡔࡦࡩ࡫ࡢࡩࡨࠫ᢭"), bstack111lll_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭᢮"),
  bstack111lll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᢯"),
  bstack111lll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙࡫ࡳࡵࡒࡤࡧࡰࡧࡧࡦࡵࠪᢰ"),
  bstack111lll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࠩᢱ"), bstack111lll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡅࡲࡺࡪࡸࡡࡨࡧࡈࡲࡩࡏ࡮ࡵࡧࡱࡸࠬᢲ"),
  bstack111lll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧᢳ"),
  bstack111lll_opy_ (u"ࠪࡥࡩࡨࡐࡰࡴࡷࠫᢴ"),
  bstack111lll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡗࡴࡩ࡫ࡦࡶࠪᢵ"),
  bstack111lll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᢶ"),
  bstack111lll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡶ࡫ࠫᢷ"),
  bstack111lll_opy_ (u"ࠧࡢࡸࡧࠫᢸ"), bstack111lll_opy_ (u"ࠨࡣࡹࡨࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫᢹ"), bstack111lll_opy_ (u"ࠩࡤࡺࡩࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫᢺ"), bstack111lll_opy_ (u"ࠪࡥࡻࡪࡁࡳࡩࡶࠫᢻ"),
  bstack111lll_opy_ (u"ࠫࡺࡹࡥࡌࡧࡼࡷࡹࡵࡲࡦࠩᢼ"), bstack111lll_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡶ࡫ࠫᢽ"), bstack111lll_opy_ (u"࠭࡫ࡦࡻࡶࡸࡴࡸࡥࡑࡣࡶࡷࡼࡵࡲࡥࠩᢾ"),
  bstack111lll_opy_ (u"ࠧ࡬ࡧࡼࡅࡱ࡯ࡡࡴࠩᢿ"), bstack111lll_opy_ (u"ࠨ࡭ࡨࡽࡕࡧࡳࡴࡹࡲࡶࡩ࠭ᣀ"),
  bstack111lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࠫᣁ"), bstack111lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡃࡵ࡫ࡸ࠭ᣂ"), bstack111lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪࡊࡩࡳࠩᣃ"), bstack111lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡇ࡭ࡸ࡯࡮ࡧࡐࡥࡵࡶࡩ࡯ࡩࡉ࡭ࡱ࡫ࠧᣄ"), bstack111lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶ࡚ࡹࡥࡔࡻࡶࡸࡪࡳࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪᣅ"),
  bstack111lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࠪᣆ"), bstack111lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡐࡰࡴࡷࡷࠬᣇ"),
  bstack111lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡅ࡫ࡶࡥࡧࡲࡥࡃࡷ࡬ࡰࡩࡉࡨࡦࡥ࡮ࠫᣈ"),
  bstack111lll_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࡕ࡫ࡰࡩࡴࡻࡴࠨᣉ"),
  bstack111lll_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡅࡨࡺࡩࡰࡰࠪᣊ"), bstack111lll_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡈࡧࡴࡦࡩࡲࡶࡾ࠭ᣋ"), bstack111lll_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡌ࡬ࡢࡩࡶࠫᣌ"), bstack111lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡡ࡭ࡋࡱࡸࡪࡴࡴࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᣍ"),
  bstack111lll_opy_ (u"ࠨࡦࡲࡲࡹ࡙ࡴࡰࡲࡄࡴࡵࡕ࡮ࡓࡧࡶࡩࡹ࠭ᣎ"),
  bstack111lll_opy_ (u"ࠩࡸࡲ࡮ࡩ࡯ࡥࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫᣏ"), bstack111lll_opy_ (u"ࠪࡶࡪࡹࡥࡵࡍࡨࡽࡧࡵࡡࡳࡦࠪᣐ"),
  bstack111lll_opy_ (u"ࠫࡳࡵࡓࡪࡩࡱࠫᣑ"),
  bstack111lll_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩ࡚ࡴࡩ࡮ࡲࡲࡶࡹࡧ࡮ࡵࡘ࡬ࡩࡼࡹࠧᣒ"),
  bstack111lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯ࡦࡵࡳ࡮ࡪࡗࡢࡶࡦ࡬ࡪࡸࡳࠨᣓ"),
  bstack111lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᣔ"),
  bstack111lll_opy_ (u"ࠨࡴࡨࡧࡷ࡫ࡡࡵࡧࡆ࡬ࡷࡵ࡭ࡦࡆࡵ࡭ࡻ࡫ࡲࡔࡧࡶࡷ࡮ࡵ࡮ࡴࠩᣕ"),
  bstack111lll_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᣖ"),
  bstack111lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡐࡢࡶ࡫ࠫᣗ"),
  bstack111lll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡘࡶࡥࡦࡦࠪᣘ"),
  bstack111lll_opy_ (u"ࠬ࡭ࡰࡴࡇࡱࡥࡧࡲࡥࡥࠩᣙ"),
  bstack111lll_opy_ (u"࠭ࡩࡴࡊࡨࡥࡩࡲࡥࡴࡵࠪᣚ"),
  bstack111lll_opy_ (u"ࠧࡢࡦࡥࡉࡽ࡫ࡣࡕ࡫ࡰࡩࡴࡻࡴࠨᣛ"),
  bstack111lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࡔࡥࡵ࡭ࡵࡺࠧᣜ"),
  bstack111lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡄࡦࡸ࡬ࡧࡪࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᣝ"),
  bstack111lll_opy_ (u"ࠪࡥࡺࡺ࡯ࡈࡴࡤࡲࡹࡖࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠪᣞ"),
  bstack111lll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡓࡧࡴࡶࡴࡤࡰࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᣟ"),
  bstack111lll_opy_ (u"ࠬࡹࡹࡴࡶࡨࡱࡕࡵࡲࡵࠩᣠ"),
  bstack111lll_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡇࡤࡣࡊࡲࡷࡹ࠭ᣡ"),
  bstack111lll_opy_ (u"ࠧࡴ࡭࡬ࡴ࡚ࡴ࡬ࡰࡥ࡮ࠫᣢ"), bstack111lll_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡕࡻࡳࡩࠬᣣ"), bstack111lll_opy_ (u"ࠩࡸࡲࡱࡵࡣ࡬ࡍࡨࡽࠬᣤ"),
  bstack111lll_opy_ (u"ࠪࡥࡺࡺ࡯ࡍࡣࡸࡲࡨ࡮ࠧᣥ"),
  bstack111lll_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡨࡧࡴࡄࡣࡳࡸࡺࡸࡥࠨᣦ"),
  bstack111lll_opy_ (u"ࠬࡻ࡮ࡪࡰࡶࡸࡦࡲ࡬ࡐࡶ࡫ࡩࡷࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧᣧ"),
  bstack111lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡗࡪࡰࡧࡳࡼࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࠨᣨ"),
  bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚࡯ࡰ࡮ࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᣩ"),
  bstack111lll_opy_ (u"ࠨࡧࡱࡪࡴࡸࡣࡦࡃࡳࡴࡎࡴࡳࡵࡣ࡯ࡰࠬᣪ"),
  bstack111lll_opy_ (u"ࠩࡨࡲࡸࡻࡲࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡵࡋࡥࡻ࡫ࡐࡢࡩࡨࡷࠬᣫ"), bstack111lll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡈࡪࡼࡴࡰࡱ࡯ࡷࡕࡵࡲࡵࠩᣬ"), bstack111lll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨ࡛ࡪࡨࡶࡪࡧࡺࡈࡪࡺࡡࡪ࡮ࡶࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠧᣭ"),
  bstack111lll_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡶࡰࡴࡅࡤࡧ࡭࡫ࡌࡪ࡯࡬ࡸࠬᣮ"),
  bstack111lll_opy_ (u"࠭ࡣࡢ࡮ࡨࡲࡩࡧࡲࡇࡱࡵࡱࡦࡺࠧᣯ"),
  bstack111lll_opy_ (u"ࠧࡣࡷࡱࡨࡱ࡫ࡉࡥࠩᣰ"),
  bstack111lll_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᣱ"),
  bstack111lll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡊࡴࡡࡣ࡮ࡨࡨࠬᣲ"), bstack111lll_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࡘ࡫ࡲࡷ࡫ࡦࡩࡸࡇࡵࡵࡪࡲࡶ࡮ࢀࡥࡥࠩᣳ"),
  bstack111lll_opy_ (u"ࠫࡦࡻࡴࡰࡃࡦࡧࡪࡶࡴࡂ࡮ࡨࡶࡹࡹࠧᣴ"), bstack111lll_opy_ (u"ࠬࡧࡵࡵࡱࡇ࡭ࡸࡳࡩࡴࡵࡄࡰࡪࡸࡴࡴࠩᣵ"),
  bstack111lll_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡵࡏ࡭ࡧ࠭᣶"),
  bstack111lll_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡗࡥࡵ࠭᣷"),
  bstack111lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡰ࡬ࡸ࡮ࡧ࡬ࡖࡴ࡯ࠫ᣸"), bstack111lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡃ࡯ࡰࡴࡽࡐࡰࡲࡸࡴࡸ࠭᣹"), bstack111lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌ࡫ࡳࡵࡲࡦࡈࡵࡥࡺࡪࡗࡢࡴࡱ࡭ࡳ࡭ࠧ᣺"), bstack111lll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵ࡫࡮ࡍ࡫ࡱ࡯ࡸࡏ࡮ࡃࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧࠫ᣻"),
  bstack111lll_opy_ (u"ࠬࡱࡥࡦࡲࡎࡩࡾࡉࡨࡢ࡫ࡱࡷࠬ᣼"),
  bstack111lll_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࢀࡡࡣ࡮ࡨࡗࡹࡸࡩ࡯ࡩࡶࡈ࡮ࡸࠧ᣽"),
  bstack111lll_opy_ (u"ࠧࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᣾"),
  bstack111lll_opy_ (u"ࠨ࡫ࡱࡸࡪࡸࡋࡦࡻࡇࡩࡱࡧࡹࠨ᣿"),
  bstack111lll_opy_ (u"ࠩࡶ࡬ࡴࡽࡉࡐࡕࡏࡳ࡬࠭ᤀ"),
  bstack111lll_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡗࡹࡸࡡࡵࡧࡪࡽࠬᤁ"),
  bstack111lll_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡖࡪࡹࡰࡰࡰࡶࡩ࡙࡯࡭ࡦࡱࡸࡸࠬᤂ"), bstack111lll_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࡙ࡤ࡭ࡹ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᤃ"),
  bstack111lll_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࠩᤄ"),
  bstack111lll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡴࡻࡱࡧࡊࡾࡥࡤࡷࡷࡩࡋࡸ࡯࡮ࡊࡷࡸࡵࡹࠧᤅ"),
  bstack111lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡅࡤࡴࡹࡻࡲࡦࠩᤆ"),
  bstack111lll_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩᤇ"),
  bstack111lll_opy_ (u"ࠪࡪࡺࡲ࡬ࡄࡱࡱࡸࡪࡾࡴࡍ࡫ࡶࡸࠬᤈ"),
  bstack111lll_opy_ (u"ࠫࡼࡧࡩࡵࡈࡲࡶࡆࡶࡰࡔࡥࡵ࡭ࡵࡺࠧᤉ"),
  bstack111lll_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡉ࡯࡯ࡰࡨࡧࡹࡘࡥࡵࡴ࡬ࡩࡸ࠭ᤊ"),
  bstack111lll_opy_ (u"࠭ࡡࡱࡲࡑࡥࡲ࡫ࠧᤋ"),
  bstack111lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡔࡎࡆࡩࡷࡺࠧᤌ"),
  bstack111lll_opy_ (u"ࠨࡶࡤࡴ࡜࡯ࡴࡩࡕ࡫ࡳࡷࡺࡐࡳࡧࡶࡷࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭ᤍ"),
  bstack111lll_opy_ (u"ࠩࡶࡧࡦࡲࡥࡇࡣࡦࡸࡴࡸࠧᤎ"),
  bstack111lll_opy_ (u"ࠪࡻࡩࡧࡌࡰࡥࡤࡰࡕࡵࡲࡵࠩᤏ"),
  bstack111lll_opy_ (u"ࠫࡸ࡮࡯ࡸ࡚ࡦࡳࡩ࡫ࡌࡰࡩࠪᤐ"),
  bstack111lll_opy_ (u"ࠬ࡯࡯ࡴࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡹࡸ࡫ࠧᤑ"),
  bstack111lll_opy_ (u"࠭ࡸࡤࡱࡧࡩࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠨᤒ"),
  bstack111lll_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡷࡸࡽ࡯ࡳࡦࠪᤓ"),
  bstack111lll_opy_ (u"ࠨࡷࡶࡩࡕࡸࡥࡣࡷ࡬ࡰࡹ࡝ࡄࡂࠩᤔ"),
  bstack111lll_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶ࡚ࡈࡆࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪᤕ"),
  bstack111lll_opy_ (u"ࠪࡻࡪࡨࡄࡳ࡫ࡹࡩࡷࡇࡧࡦࡰࡷ࡙ࡷࡲࠧᤖ"),
  bstack111lll_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡵࡪࠪᤗ"),
  bstack111lll_opy_ (u"ࠬࡻࡳࡦࡐࡨࡻ࡜ࡊࡁࠨᤘ"),
  bstack111lll_opy_ (u"࠭ࡷࡥࡣࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩᤙ"), bstack111lll_opy_ (u"ࠧࡸࡦࡤࡇࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࡔࡪ࡯ࡨࡳࡺࡺࠧᤚ"),
  bstack111lll_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡏࡳࡩࡌࡨࠬᤛ"), bstack111lll_opy_ (u"ࠩࡻࡧࡴࡪࡥࡔ࡫ࡪࡲ࡮ࡴࡧࡊࡦࠪᤜ"),
  bstack111lll_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧ࡛ࡉࡇࡂࡶࡰࡧࡰࡪࡏࡤࠨᤝ"),
  bstack111lll_opy_ (u"ࠫࡷ࡫ࡳࡦࡶࡒࡲࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡳࡶࡒࡲࡱࡿࠧᤞ"),
  bstack111lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹࡹࠧ᤟"),
  bstack111lll_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡩࡦࡵࠪᤠ"), bstack111lll_opy_ (u"ࠧࡸࡦࡤࡗࡹࡧࡲࡵࡷࡳࡖࡪࡺࡲࡺࡋࡱࡸࡪࡸࡶࡢ࡮ࠪᤡ"),
  bstack111lll_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࡊࡤࡶࡩࡽࡡࡳࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫᤢ"),
  bstack111lll_opy_ (u"ࠩࡰࡥࡽ࡚ࡹࡱ࡫ࡱ࡫ࡋࡸࡥࡲࡷࡨࡲࡨࡿࠧᤣ"),
  bstack111lll_opy_ (u"ࠪࡷ࡮ࡳࡰ࡭ࡧࡌࡷ࡛࡯ࡳࡪࡤ࡯ࡩࡈ࡮ࡥࡤ࡭ࠪᤤ"),
  bstack111lll_opy_ (u"ࠫࡺࡹࡥࡄࡣࡵࡸ࡭ࡧࡧࡦࡕࡶࡰࠬᤥ"),
  bstack111lll_opy_ (u"ࠬࡹࡨࡰࡷ࡯ࡨ࡚ࡹࡥࡔ࡫ࡱ࡫ࡱ࡫ࡴࡰࡰࡗࡩࡸࡺࡍࡢࡰࡤ࡫ࡪࡸࠧᤦ"),
  bstack111lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡎ࡝ࡄࡑࠩᤧ"),
  bstack111lll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼ࡚࡯ࡶࡥ࡫ࡍࡩࡋ࡮ࡳࡱ࡯ࡰࠬᤨ"),
  bstack111lll_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡉ࡫ࡧࡨࡪࡴࡁࡱ࡫ࡓࡳࡱ࡯ࡣࡺࡇࡵࡶࡴࡸࠧᤩ"),
  bstack111lll_opy_ (u"ࠩࡰࡳࡨࡱࡌࡰࡥࡤࡸ࡮ࡵ࡮ࡂࡲࡳࠫᤪ"),
  bstack111lll_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉࡳࡷࡳࡡࡵࠩᤫ"), bstack111lll_opy_ (u"ࠫࡱࡵࡧࡤࡣࡷࡊ࡮ࡲࡴࡦࡴࡖࡴࡪࡩࡳࠨ᤬"),
  bstack111lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡈࡪࡲࡡࡺࡃࡧࡦࠬ᤭"),
  bstack111lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡉࡥࡎࡲࡧࡦࡺ࡯ࡳࡃࡸࡸࡴࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠩ᤮")
]
bstack1l11l111l_opy_ = bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡵࡱ࡮ࡲࡥࡩ࠭᤯")
bstack11l11l1l1_opy_ = [bstack111lll_opy_ (u"ࠨ࠰ࡤࡴࡰ࠭ᤰ"), bstack111lll_opy_ (u"ࠩ࠱ࡥࡦࡨࠧᤱ"), bstack111lll_opy_ (u"ࠪ࠲࡮ࡶࡡࠨᤲ")]
bstack11111ll1_opy_ = [bstack111lll_opy_ (u"ࠫ࡮ࡪࠧᤳ"), bstack111lll_opy_ (u"ࠬࡶࡡࡵࡪࠪᤴ"), bstack111lll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩᤵ"), bstack111lll_opy_ (u"ࠧࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩ࠭ᤶ")]
bstack11l1l111l_opy_ = {
  bstack111lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᤷ"): bstack111lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᤸ"),
  bstack111lll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶ᤹ࠫ"): bstack111lll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᤺"),
  bstack111lll_opy_ (u"ࠬ࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵ᤻ࠪ"): bstack111lll_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᤼"),
  bstack111lll_opy_ (u"ࠧࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᤽"): bstack111lll_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᤾"),
  bstack111lll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᤿"): bstack111lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ᥀")
}
bstack11lllll11_opy_ = [
  bstack111lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᥁"),
  bstack111lll_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ᥂"),
  bstack111lll_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᥃"),
  bstack111lll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᥄"),
  bstack111lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᥅"),
]
bstack1l11ll1l11_opy_ = bstack11ll1l11l1_opy_ + bstack11ll11l1l1l_opy_ + bstack1llll11lll_opy_
bstack1ll1l111l1_opy_ = [
  bstack111lll_opy_ (u"ࠩࡡࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࠪࠧ᥆"),
  bstack111lll_opy_ (u"ࠪࡢࡧࡹ࠭࡭ࡱࡦࡥࡱ࠴ࡣࡰ࡯ࠧࠫ᥇"),
  bstack111lll_opy_ (u"ࠫࡣ࠷࠲࠸࠰ࠪ᥈"),
  bstack111lll_opy_ (u"ࠬࡤ࠱࠱࠰ࠪ᥉"),
  bstack111lll_opy_ (u"࠭࡞࠲࠹࠵࠲࠶ࡡ࠶࠮࠻ࡠ࠲ࠬ᥊"),
  bstack111lll_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠸࡛࠱࠯࠼ࡡ࠳࠭᥋"),
  bstack111lll_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠳࡜࠲࠰࠵ࡢ࠴ࠧ᥌"),
  bstack111lll_opy_ (u"ࠩࡡ࠵࠾࠸࠮࠲࠸࠻࠲ࠬ᥍")
]
bstack11ll1ll11ll_opy_ = bstack111lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ᥎")
bstack11lll11ll1_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡪࡼࡥ࡯ࡶࠪ᥏")
bstack111l11l1_opy_ = [ bstack111lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᥐ") ]
bstack1l1l11ll_opy_ = [ bstack111lll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᥑ") ]
bstack11l1lll11_opy_ = [bstack111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᥒ")]
bstack11111l1ll_opy_ = [ bstack111lll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᥓ") ]
bstack1111l1111_opy_ = bstack111lll_opy_ (u"ࠩࡖࡈࡐ࡙ࡥࡵࡷࡳࠫᥔ")
bstack1ll111l1ll_opy_ = bstack111lll_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡅࡹࡺࡥ࡮ࡲࡷࡩࡩ࠭ᥕ")
bstack1l1ll1l1ll_opy_ = bstack111lll_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠨᥖ")
bstack11l1l1111_opy_ = bstack111lll_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࠫᥗ")
bstack1ll11ll11l_opy_ = [
  bstack111lll_opy_ (u"࠭ࡅࡓࡔࡢࡊࡆࡏࡌࡆࡆࠪᥘ"),
  bstack111lll_opy_ (u"ࠧࡆࡔࡕࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧᥙ"),
  bstack111lll_opy_ (u"ࠨࡇࡕࡖࡤࡈࡌࡐࡅࡎࡉࡉࡥࡂ࡚ࡡࡆࡐࡎࡋࡎࡕࠩᥚ"),
  bstack111lll_opy_ (u"ࠩࡈࡖࡗࡥࡎࡆࡖ࡚ࡓࡗࡑ࡟ࡄࡊࡄࡒࡌࡋࡄࠨᥛ"),
  bstack111lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡊ࡚࡟ࡏࡑࡗࡣࡈࡕࡎࡏࡇࡆࡘࡊࡊࠧᥜ"),
  bstack111lll_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡉࡌࡐࡕࡈࡈࠬᥝ"),
  bstack111lll_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡕࡈࡘࠬᥞ"),
  bstack111lll_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡓࡇࡉ࡙ࡘࡋࡄࠨᥟ"),
  bstack111lll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡃࡅࡓࡗ࡚ࡅࡅࠩᥠ"),
  bstack111lll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᥡ"),
  bstack111lll_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪᥢ"),
  bstack111lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡋࡑ࡚ࡆࡒࡉࡅࠩᥣ"),
  bstack111lll_opy_ (u"ࠫࡊࡘࡒࡠࡃࡇࡈࡗࡋࡓࡔࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧᥤ"),
  bstack111lll_opy_ (u"ࠬࡋࡒࡓࡡࡗ࡙ࡓࡔࡅࡍࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᥥ"),
  bstack111lll_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪᥦ"),
  bstack111lll_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᥧ"),
  bstack111lll_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡖࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡊࡒࡗ࡙ࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫᥨ"),
  bstack111lll_opy_ (u"ࠩࡈࡖࡗࡥࡐࡓࡑ࡛࡝ࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᥩ"),
  bstack111lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡔࡏࡕࡡࡕࡉࡘࡕࡌࡗࡇࡇࠫᥪ"),
  bstack111lll_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡒࡆࡕࡒࡐ࡚࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᥫ"),
  bstack111lll_opy_ (u"ࠬࡋࡒࡓࡡࡐࡅࡓࡊࡁࡕࡑࡕ࡝ࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫᥬ"),
]
bstack1llll11l11_opy_ = bstack111lll_opy_ (u"࠭࠮࠰ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡢࡴࡷ࡭࡫ࡧࡣࡵࡵ࠲ࠫᥭ")
bstack1l1llll1l_opy_ = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠧࡿࠩ᥮")), bstack111lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᥯"), bstack111lll_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᥰ"))
bstack11lll111l11_opy_ = bstack111lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲ࡬ࠫᥱ")
bstack11ll11l11ll_opy_ = [ bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᥲ"), bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᥳ"), bstack111lll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬᥴ"), bstack111lll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ᥵")]
bstack111ll1l1l_opy_ = [ bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᥶"), bstack111lll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᥷"), bstack111lll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ᥸"), bstack111lll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᥹") ]
bstack1l1ll11l_opy_ = [ bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ᥺") ]
bstack11l1lll1_opy_ = 360
bstack11ll1l1l11l_opy_ = bstack111lll_opy_ (u"ࠨࡡࡱࡲ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨ᥻")
bstack11ll11lllll_opy_ = bstack111lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡬ࡷࡸࡻࡥࡴࠤ᥼")
bstack11ll1111111_opy_ = bstack111lll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠦ᥽")
bstack11lll1l1lll_opy_ = bstack111lll_opy_ (u"ࠤࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡸࡪࡹࡴࡴࠢࡤࡶࡪࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡲࡲࠥࡕࡓࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࠨࡷࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥࠡࡨࡲࡶࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦࡤࡦࡸ࡬ࡧࡪࡹ࠮ࠣ᥾")
bstack11lll1l111l_opy_ = bstack111lll_opy_ (u"ࠥ࠵࠶࠴࠰ࠣ᥿")
bstack111ll1l11l_opy_ = {
  bstack111lll_opy_ (u"ࠫࡕࡇࡓࡔࠩᦀ"): bstack111lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᦁ"),
  bstack111lll_opy_ (u"࠭ࡆࡂࡋࡏࠫᦂ"): bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᦃ"),
  bstack111lll_opy_ (u"ࠨࡕࡎࡍࡕ࠭ᦄ"): bstack111lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᦅ")
}
bstack1llll111l_opy_ = [
  bstack111lll_opy_ (u"ࠥ࡫ࡪࡺࠢᦆ"),
  bstack111lll_opy_ (u"ࠦ࡬ࡵࡂࡢࡥ࡮ࠦᦇ"),
  bstack111lll_opy_ (u"ࠧ࡭࡯ࡇࡱࡵࡻࡦࡸࡤࠣᦈ"),
  bstack111lll_opy_ (u"ࠨࡲࡦࡨࡵࡩࡸ࡮ࠢᦉ"),
  bstack111lll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨᦊ"),
  bstack111lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᦋ"),
  bstack111lll_opy_ (u"ࠤࡶࡹࡧࡳࡩࡵࡇ࡯ࡩࡲ࡫࡮ࡵࠤᦌ"),
  bstack111lll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢᦍ"),
  bstack111lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢᦎ"),
  bstack111lll_opy_ (u"ࠧࡩ࡬ࡦࡣࡵࡉࡱ࡫࡭ࡦࡰࡷࠦᦏ"),
  bstack111lll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࡹࠢᦐ"),
  bstack111lll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠢᦑ"),
  bstack111lll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡃࡶࡽࡳࡩࡓࡤࡴ࡬ࡴࡹࠨᦒ"),
  bstack111lll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣᦓ"),
  bstack111lll_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᦔ"),
  bstack111lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱ࡙ࡵࡵࡤࡪࡄࡧࡹ࡯࡯࡯ࠤᦕ"),
  bstack111lll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡓࡵ࡭ࡶ࡬ࡘࡴࡻࡣࡩࠤᦖ"),
  bstack111lll_opy_ (u"ࠨࡳࡩࡣ࡮ࡩࠧᦗ"),
  bstack111lll_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࡇࡰࡱࠤᦘ")
]
bstack11ll1111l11_opy_ = [
  bstack111lll_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࠢᦙ"),
  bstack111lll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᦚ"),
  bstack111lll_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᦛ"),
  bstack111lll_opy_ (u"ࠦࡲࡧ࡮ࡶࡣ࡯ࠦᦜ"),
  bstack111lll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᦝ")
]
bstack1l11111lll_opy_ = {
  bstack111lll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧᦞ"): [bstack111lll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨᦟ")],
  bstack111lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᦠ"): [bstack111lll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᦡ")],
  bstack111lll_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᦢ"): [bstack111lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣᦣ"), bstack111lll_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣᦤ"), bstack111lll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᦥ"), bstack111lll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨᦦ")],
  bstack111lll_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣᦧ"): [bstack111lll_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤᦨ")],
  bstack111lll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᦩ"): [bstack111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᦪ")],
}
bstack11l1llll1l1_opy_ = {
  bstack111lll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦᦫ"): bstack111lll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧ᦬"),
  bstack111lll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᦭"): bstack111lll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᦮"),
  bstack111lll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨ᦯"): bstack111lll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧᦰ"),
  bstack111lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢᦱ"): bstack111lll_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࠢᦲ"),
  bstack111lll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᦳ"): bstack111lll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᦴ")
}
bstack111l111111_opy_ = {
  bstack111lll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᦵ"): bstack111lll_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡕࡨࡸࡺࡶࠧᦶ"),
  bstack111lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᦷ"): bstack111lll_opy_ (u"ࠫࡘࡻࡩࡵࡧࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬᦸ"),
  bstack111lll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᦹ"): bstack111lll_opy_ (u"࠭ࡔࡦࡵࡷࠤࡘ࡫ࡴࡶࡲࠪᦺ"),
  bstack111lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᦻ"): bstack111lll_opy_ (u"ࠨࡖࡨࡷࡹࠦࡔࡦࡣࡵࡨࡴࡽ࡮ࠨᦼ")
}
bstack11ll11lll11_opy_ = 65536
bstack11ll111l11l_opy_ = bstack111lll_opy_ (u"ࠩ࠱࠲࠳ࡡࡔࡓࡗࡑࡇࡆ࡚ࡅࡅ࡟ࠪᦽ")
bstack11ll111lll1_opy_ = [
      bstack111lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᦾ"), bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᦿ"), bstack111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᧀ"), bstack111lll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᧁ"), bstack111lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩᧂ"),
      bstack111lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᧃ"), bstack111lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᧄ"), bstack111lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫᧅ"), bstack111lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬᧆ"),
      bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᧇ"), bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᧈ"), bstack111lll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᧉ")
    ]
bstack11ll11l11l1_opy_= {
  bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᧊"): bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᧋"),
  bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ᧌"): bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ᧍"),
  bstack111lll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ᧎"): bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ᧏"),
  bstack111lll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᧐"): bstack111lll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᧑"),
  bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᧒"): bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᧓"),
  bstack111lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭᧔"): bstack111lll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ᧕"),
  bstack111lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᧖"): bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᧗"),
  bstack111lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ᧘"): bstack111lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭᧙"),
  bstack111lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭᧚"): bstack111lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ᧛"),
  bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ᧜"): bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ᧝"),
  bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ᧞"): bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᧟"),
  bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᧠"): bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᧡"),
  bstack111lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭᧢"): bstack111lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧ᧣"),
  bstack111lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᧤"): bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᧥"),
  bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᧦"): bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᧧"),
  bstack111lll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧ᧨"): bstack111lll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ᧩"),
  bstack111lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᧪"): bstack111lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ᧫"),
  bstack111lll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᧬"): bstack111lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᧭"),
  bstack111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ᧮"): bstack111lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭᧯"),
  bstack111lll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭᧰"): bstack111lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ᧱"),
  bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᧲"): bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᧳"),
  bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᧴"): bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᧵"),
  bstack111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ᧶"): bstack111lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᧷"),
  bstack111lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᧸"): bstack111lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᧹"),
  bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ᧺"): bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ᧻"),
  bstack111lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩ᧼"): bstack111lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ᧽")
}
bstack11ll11111l1_opy_ = [bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᧾"), bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ᧿")]
bstack1l1111ll11_opy_ = (bstack111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᨀ"),)
bstack11ll11ll11l_opy_ = bstack111lll_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡶࡲࡧࡥࡹ࡫࡟ࡤ࡮࡬ࠫᨁ")
bstack1l111ll11l_opy_ = bstack111lll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳࡬ࡸࡩࡥࡵ࠲ࠦᨂ")
bstack1l111l11l1_opy_ = bstack111lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫ࡷ࡯ࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡧࡳࡩࡤࡲࡥࡷࡪ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࠣᨃ")
bstack1l1ll11lll_opy_ = bstack111lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠦᨄ")
class EVENTS(Enum):
  bstack11l1llll11l_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡱ࠴࠵ࡾࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨᨅ")
  bstack1lll11111_opy_ = bstack111lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰࡪࡧ࡮ࡶࡲࠪᨆ") # final bstack11ll11111ll_opy_
  bstack11ll11l111l_opy_ = bstack111lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡴࡤ࡭ࡱࡪࡷࠬᨇ")
  bstack11l11lll11_opy_ = bstack111lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪᨈ") #shift post bstack11ll111l1ll_opy_
  bstack11l11l1111_opy_ = bstack111lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩᨉ") #shift post bstack11ll111l1ll_opy_
  bstack11ll11l1111_opy_ = bstack111lll_opy_ (u"ࠩࡶࡨࡰࡀࡴࡦࡵࡷ࡬ࡺࡨࠧᨊ") #shift
  bstack11ll111l111_opy_ = bstack111lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨᨋ") #shift
  bstack1l11111l11_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠿࡮ࡵࡣ࠯ࡰࡥࡳࡧࡧࡦ࡯ࡨࡲࡹ࠭ᨌ")
  bstack1ll11lll111_opy_ = bstack111lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡴࡣࡹࡩ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭ᨍ")
  bstack1ll1l1l1_opy_ = bstack111lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡦࡵ࡭ࡻ࡫ࡲ࠮ࡲࡨࡶ࡫ࡵࡲ࡮ࡵࡦࡥࡳ࠭ᨎ")
  bstack11lll1ll1l_opy_ = bstack111lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀ࡬ࡰࡥࡤࡰࠬᨏ") #shift
  bstack11lllll1ll_opy_ = bstack111lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡦࡶࡰ࠮ࡷࡳࡰࡴࡧࡤࠨᨐ") #shift
  bstack11ll11lll1_opy_ = bstack111lll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡥ࡬࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹࠧᨑ")
  bstack1ll1l1lll_opy_ = bstack111lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠫᨒ") #shift
  bstack1l1l111111_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡧࡦࡶ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠰ࡶࡪࡹࡵ࡭ࡶࡶࠫᨓ") #shift
  bstack11ll1111ll1_opy_ = bstack111lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹࠨᨔ") #shift
  bstack1l1ll111lll_opy_ = bstack111lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᨕ")
  bstack11lllll111_opy_ = bstack111lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭ࡴࡶࡤࡸࡺࡹࠧᨖ") #shift
  bstack1l1llll1_opy_ = bstack111lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨᨗ")
  bstack11ll1111lll_opy_ = bstack111lll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡱࡻࡽ࠲ࡹࡥࡵࡷࡳᨘࠫ") #shift
  bstack1l1ll1llll_opy_ = bstack111lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡷࡹࡵ࠭ᨙ")
  bstack11ll11l1ll1_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡴࡰࡤࡴࡸ࡮࡯ࡵࠩᨚ") # not bstack11ll111ll11_opy_ in python
  bstack111l11ll_opy_ = bstack111lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡴࡹ࡮ࡺࠧᨛ") # used in bstack11ll11l1lll_opy_
  bstack11l1l111ll_opy_ = bstack111lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽࡫ࡪࡺࠧ᨜") # used in bstack11ll11l1lll_opy_
  bstack1lll111l11_opy_ = bstack111lll_opy_ (u"ࠧࡴࡦ࡮࠾࡭ࡵ࡯࡬ࠩ᨝")
  bstack1l111l11ll_opy_ = bstack111lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪ࠭᨞")
  bstack111l1l1l_opy_ = bstack111lll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳ࠭᨟") #
  bstack11l1111ll1_opy_ = bstack111lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡰ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡺࡡ࡬ࡧࡖࡧࡷ࡫ࡥ࡯ࡕ࡫ࡳࡹ࠭ᨠ")
  bstack1ll111l11l_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡢࡷࡷࡳ࠲ࡩࡡࡱࡶࡸࡶࡪ࠭ᨡ")
  bstack1l11lll1l_opy_ = bstack111lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡴࡦࡵࡷࠫᨢ")
  bstack1l1l11lll1_opy_ = bstack111lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡶࡨࡷࡹ࠭ᨣ")
  bstack1l1l1l11l_opy_ = bstack111lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡸࡥ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩᨤ") #shift
  bstack111ll11l_opy_ = bstack111lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫᨥ") #shift
  bstack11l1llll1ll_opy_ = bstack111lll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬᨦ")
  bstack11ll11ll111_opy_ = bstack111lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡬ࡨࡱ࡫࠭ࡵ࡫ࡰࡩࡴࡻࡴࠨᨧ")
  bstack1ll1lll1lll_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡹࡴࡢࡴࡷࠫᨨ")
  bstack11ll11ll1l1_opy_ = bstack111lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨᨩ")
  bstack11ll111l1l1_opy_ = bstack111lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡤࡪࡨࡧࡰ࠳ࡵࡱࡦࡤࡸࡪ࠭ᨪ")
  bstack1lll1l111l1_opy_ = bstack111lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠧᨫ")
  bstack1lll1l11l11_opy_ = bstack111lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡩ࡯࡯ࡰࡨࡧࡹ࠭ᨬ")
  bstack1lll11l1ll1_opy_ = bstack111lll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡳࡵࡱࡳࠫᨭ")
  bstack1lll11111ll_opy_ = bstack111lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡶࡤࡶࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩᨮ")
  bstack1lll1111111_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥࡲࡲࡳ࡫ࡣࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲࠬᨯ")
  bstack11ll11lll1l_opy_ = bstack111lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹ࠭ᨰ")
  bstack11ll11llll1_opy_ = bstack111lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡪ࡮ࡴࡤࡏࡧࡤࡶࡪࡹࡴࡉࡷࡥࠫᨱ")
  bstack1l11lllll1l_opy_ = bstack111lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡌࡲ࡮ࡺࠧᨲ")
  bstack1l1l11l11l1_opy_ = bstack111lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡲࡵࠩᨳ")
  bstack1ll1l1l1ll1_opy_ = bstack111lll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡉ࡯࡯ࡨ࡬࡫ࠬᨴ")
  bstack11ll111llll_opy_ = bstack111lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡃࡰࡰࡩ࡭࡬࠭ᨵ")
  bstack1ll11l11l11_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࡬ࡗࡪࡲࡦࡉࡧࡤࡰࡘࡺࡥࡱࠩᨶ")
  bstack1ll11l111l1_opy_ = bstack111lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࡭ࡘ࡫࡬ࡧࡊࡨࡥࡱࡍࡥࡵࡔࡨࡷࡺࡲࡴࠨᨷ")
  bstack1l1llll1l11_opy_ = bstack111lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡈࡺࡪࡴࡴࠨᨸ")
  bstack1l1ll1ll111_opy_ = bstack111lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺࠧᨹ")
  bstack1ll1111ll1l_opy_ = bstack111lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼࡯ࡳ࡬ࡉࡲࡦࡣࡷࡩࡩࡋࡶࡦࡰࡷࠫᨺ")
  bstack11l1llllll1_opy_ = bstack111lll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡩࡳࡷࡵࡦࡷࡨࡘࡪࡹࡴࡆࡸࡨࡲࡹ࠭ᨻ")
  bstack1l1l11l1lll_opy_ = bstack111lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡰࡲࠪᨼ")
  bstack1ll1lll111l_opy_ = bstack111lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡱࡱࡗࡹࡵࡰࠨᨽ")
class STAGE(Enum):
  bstack1ll11l111l_opy_ = bstack111lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫᨾ")
  END = bstack111lll_opy_ (u"࠭ࡥ࡯ࡦࠪᨿ")
  bstack111ll11l1_opy_ = bstack111lll_opy_ (u"ࠧࡴ࡫ࡱ࡫ࡱ࡫ࠧᩀ")
bstack1ll1l1l111_opy_ = {
  bstack111lll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࠨᩁ"): bstack111lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᩂ"),
  bstack111lll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧᩃ"): bstack111lll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ᩄ")
}
PLAYWRIGHT_HUB_URL = bstack111lll_opy_ (u"ࠧࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠢᩅ")
bstack1ll1l1ll111_opy_ = 98
bstack1ll1l1l1111_opy_ = 100
bstack1111ll111l_opy_ = {
  bstack111lll_opy_ (u"࠭ࡲࡦࡴࡸࡲࠬᩆ"): bstack111lll_opy_ (u"ࠧ࠮࠯ࡵࡩࡷࡻ࡮ࡴࠩᩇ"),
  bstack111lll_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧᩈ"): bstack111lll_opy_ (u"ࠩ࠰࠱ࡷ࡫ࡲࡶࡰࡶ࠱ࡩ࡫࡬ࡢࡻࠪᩉ"),
  bstack111lll_opy_ (u"ࠪࡶࡪࡸࡵ࡯࠯ࡧࡩࡱࡧࡹࠨᩊ"): 0
}
bstack11ll11l1l11_opy_ = bstack111lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠣᩋ")
bstack11ll11ll1ll_opy_ = bstack111lll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡵࡱ࡮ࡲࡥࡩ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᩌ")