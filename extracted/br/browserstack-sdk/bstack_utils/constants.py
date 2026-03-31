# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import re
from enum import Enum
bstack1llll11l1l_opy_ = {
  bstack1ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᯼"): bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࠨ᯽"),
  bstack1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᯾"): bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡱࡥࡺࠩ᯿"),
  bstack1ll11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᰀ"): bstack1ll11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᰁ"),
  bstack1ll11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᰂ"): bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪᰃ"),
  bstack1ll11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᰄ"): bstack1ll11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹ࠭ᰅ"),
  bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᰆ"): bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࠭ᰇ"),
  bstack1ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᰈ"): bstack1ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᰉ"),
  bstack1ll11_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᰊ"): bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨࠩᰋ"),
  bstack1ll11_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪᰌ"): bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡯ࡵࡲࡰࡪ࠭ᰍ"),
  bstack1ll11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬᰎ"): bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬᰏ"),
  bstack1ll11_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᰐ"): bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᰑ"),
  bstack1ll11_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪᰒ"): bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡻ࡯ࡤࡦࡱࠪᰓ"),
  bstack1ll11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬᰔ"): bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬᰕ"),
  bstack1ll11_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨᰖ"): bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨᰗ"),
  bstack1ll11_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᰘ"): bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᰙ"),
  bstack1ll11_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧᰚ"): bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧᰛ"),
  bstack1ll11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᰜ"): bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᰝ"),
  bstack1ll11_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨᰞ"): bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨᰟ"),
  bstack1ll11_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩᰠ"): bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩᰡ"),
  bstack1ll11_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭ᰢ"): bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭ᰣ"),
  bstack1ll11_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪᰤ"): bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡲࡩࡑࡥࡺࡵࠪᰥ"),
  bstack1ll11_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᰦ"): bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᰧ"),
  bstack1ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫᰨ"): bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡶࠫᰩ"),
  bstack1ll11_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨᰪ"): bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡨࡦࡥࡨ࡮ࡥࠨᰫ"),
  bstack1ll11_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪᰬ"): bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪᰭ"),
  bstack1ll11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧᰮ"): bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧᰯ"),
  bstack1ll11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᰰ"): bstack1ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᰱ"),
  bstack1ll11_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᰲ"): bstack1ll11_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧᰳ"),
  bstack1ll11_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᰴ"): bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᰵ"),
  bstack1ll11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬᰶ"): bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯᰷ࠬ"),
  bstack1ll11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨ᰸"): bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨ᰹"),
  bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨ᰺"): bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫ᰻"),
  bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᰼"): bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᰽"),
  bstack1ll11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭᰾"): bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡰࡷࡵࡧࡪ࠭᰿"),
  bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᱀"): bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᱁"),
  bstack1ll11_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬ᱂"): bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡏࡣࡰࡩࠬ᱃"),
  bstack1ll11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨ᱄"): bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨ᱅"),
  bstack1ll11_opy_ (u"ࠧࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫ᱆"): bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫ᱇"),
  bstack1ll11_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧ᱈"): bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧ᱉"),
  bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ᱊"): bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ᱋"),
  bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᱌"): bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᱍ")
}
bstack111l1111lll_opy_ = [
  bstack1ll11_opy_ (u"ࠨࡱࡶࠫᱎ"),
  bstack1ll11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᱏ"),
  bstack1ll11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᱐"),
  bstack1ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ᱑"),
  bstack1ll11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ᱒"),
  bstack1ll11_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪ᱓"),
  bstack1ll11_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᱔"),
]
bstack11ll1ll1l_opy_ = {
  bstack1ll11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᱕"): [bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ᱖"), bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡏࡃࡐࡉࠬ᱗")],
  bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᱘"): bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ᱙"),
  bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᱚ"): bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠪᱛ"),
  bstack1ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᱜ"): bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠧᱝ"),
  bstack1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᱞ"): bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᱟ"),
  bstack1ll11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᱠ"): bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡁࡓࡃࡏࡐࡊࡒࡓࡠࡒࡈࡖࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧᱡ"),
  bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᱢ"): bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑ࠭ᱣ"),
  bstack1ll11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᱤ"): bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧᱥ"),
  bstack1ll11_opy_ (u"ࠫࡦࡶࡰࠨᱦ"): [bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࡠࡋࡇࠫᱧ"), bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࠩᱨ")],
  bstack1ll11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᱩ"): bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡑࡕࡇࡍࡇ࡙ࡉࡑ࠭ᱪ"),
  bstack1ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᱫ"): bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᱬ"),
  bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᱭ"): [bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡒࡆࡘࡋࡒࡗࡃࡅࡍࡑࡏࡔ࡚ࠩᱮ"), bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭ᱯ")],
  bstack1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᱰ"): bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡗࡕࡆࡔ࡙ࡃࡂࡎࡈࠫᱱ"),
  bstack1ll11_opy_ (u"ࠩࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡉࡓ࡜ࠧᱲ"): bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡒࡖࡈࡎࡅࡔࡖࡕࡅ࡙ࡏࡏࡏࡡࡖࡑࡆࡘࡔࡠࡕࡈࡐࡊࡉࡔࡊࡑࡑࡣࡋࡋࡁࡕࡗࡕࡉࡤࡈࡒࡂࡐࡆࡌࡊ࡙ࠧᱳ")
}
bstack11l111l1l_opy_ = {
  bstack1ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᱴ"): [bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᱵ"), bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᱶ")],
  bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᱷ"): [bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹ࡟࡬ࡧࡼࠫᱸ"), bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᱹ")],
  bstack1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᱺ"): bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᱻ"),
  bstack1ll11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᱼ"): bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᱽ"),
  bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᱾"): bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᱿"),
  bstack1ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᲀ"): [bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡴࡵ࠭ᲁ"), bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᲂ")],
  bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᲃ"): bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫᲄ"),
  bstack1ll11_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫᲅ"): bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫᲆ"),
  bstack1ll11_opy_ (u"ࠩࡤࡴࡵ࠭ᲇ"): bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࠭ᲈ"),
  bstack1ll11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭Ᲊ"): bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᲊ"),
  bstack1ll11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᲋"): bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᲌"),
  bstack1ll11_opy_ (u"ࠣࡵࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࡈࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࡦࡵࡆࡐࡎࠨ᲍"): bstack1ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࠢ᲎"),
}
bstack1ll1111ll_opy_ = {
  bstack1ll11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᲏"): bstack1ll11_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᲐ"),
  bstack1ll11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᲑ"): [bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᲒ"), bstack1ll11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᲓ")],
  bstack1ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ე"): bstack1ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᲕ"),
  bstack1ll11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᲖ"): bstack1ll11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᲗ"),
  bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᲘ"): [bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᲙ"), bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭Ლ")],
  bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᲛ"): bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᲜ"),
  bstack1ll11_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᲝ"): bstack1ll11_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩᲞ"),
  bstack1ll11_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᲟ"): [bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭Რ"), bstack1ll11_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᲡ")],
  bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧᲢ"): [bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪᲣ"), bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࠪᲤ")]
}
bstack1111l1l1l_opy_ = [
  bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪᲥ"),
  bstack1ll11_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨᲦ"),
  bstack1ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬᲧ"),
  bstack1ll11_opy_ (u"ࠧࡴࡧࡷ࡛࡮ࡴࡤࡰࡹࡕࡩࡨࡺࠧᲨ"),
  bstack1ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪᲩ"),
  bstack1ll11_opy_ (u"ࠩࡶࡸࡷ࡯ࡣࡵࡈ࡬ࡰࡪࡏ࡮ࡵࡧࡵࡥࡨࡺࡡࡣ࡫࡯࡭ࡹࡿࠧᲪ"),
  bstack1ll11_opy_ (u"ࠪࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡖࡲࡰ࡯ࡳࡸࡇ࡫ࡨࡢࡸ࡬ࡳࡷ࠭Ძ"),
  bstack1ll11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲬ"),
  bstack1ll11_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪᲭ"),
  bstack1ll11_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᲮ"),
  bstack1ll11_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭Ჯ"),
  bstack1ll11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᲰ"),
]
bstack111ll111l1_opy_ = [
  bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭Ჱ"),
  bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᲲ"),
  bstack1ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪᲳ"),
  bstack1ll11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᲴ"),
  bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᲵ"),
  bstack1ll11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᲶ"),
  bstack1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᲷ"),
  bstack1ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭Ჸ"),
  bstack1ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭Ჹ"),
  bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲺ"),
  bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᲻"),
  bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭᲼"),
  bstack1ll11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩᲽ"),
  bstack1ll11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡕࡣࡪࠫᲾ"),
  bstack1ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ჿ"),
  bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᳀"),
  bstack1ll11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ᳁"),
  bstack1ll11_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠴ࠫ᳂"),
  bstack1ll11_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠶ࠬ᳃"),
  bstack1ll11_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠸࠭᳄"),
  bstack1ll11_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠺ࠧ᳅"),
  bstack1ll11_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠵ࠨ᳆"),
  bstack1ll11_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠷ࠩ᳇"),
  bstack1ll11_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠹ࠪ᳈"),
  bstack1ll11_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠻ࠫ᳉"),
  bstack1ll11_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠽ࠬ᳊"),
  bstack1ll11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭᳋"),
  bstack1ll11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᳌"),
  bstack1ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ᳍"),
  bstack1ll11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ᳎"),
  bstack1ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᳏"),
  bstack1ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳐"),
  bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ᳑"),
  bstack1ll11_opy_ (u"ࠧࡩࡷࡥࡖࡪ࡭ࡩࡰࡰࠪ᳒")
]
bstack111l11llll1_opy_ = [
  bstack1ll11_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭᳓"),
  bstack1ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨ᳔ࠫ"),
  bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ᳕࠭"),
  bstack1ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦ᳖ࠩ"),
  bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼ᳗ࠫ"),
  bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦ᳘ࠩ"),
  bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨ᳙ࠩ"),
  bstack1ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᳚"),
  bstack1ll11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ᳛"),
  bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᳜"),
  bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ᳝ࠬ"),
  bstack1ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯᳞ࠫ"),
  bstack1ll11_opy_ (u"࠭࡯ࡴ᳟ࠩ"),
  bstack1ll11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ᳠"),
  bstack1ll11_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧ᳡"),
  bstack1ll11_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷ᳢ࠫ"),
  bstack1ll11_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰ᳣ࠪ"),
  bstack1ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ᳤࠭"),
  bstack1ll11_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ᳥࠭"),
  bstack1ll11_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰ᳦ࠪ"),
  bstack1ll11_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸ᳧ࠬ"),
  bstack1ll11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲ᳨ࠬ"),
  bstack1ll11_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨᳩ"),
  bstack1ll11_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧᳪ"),
  bstack1ll11_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬᳫ"),
  bstack1ll11_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᳬ"),
  bstack1ll11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵ᳭ࠪ"),
  bstack1ll11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨᳮ"),
  bstack1ll11_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᳯ"),
  bstack1ll11_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ᳰ"),
  bstack1ll11_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬᳱ"),
  bstack1ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᳲ"),
  bstack1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬᳳ"),
  bstack1ll11_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ᳴"),
  bstack1ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᳵ"),
  bstack1ll11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᳶ"),
  bstack1ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᳷"),
  bstack1ll11_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪࠫ᳸"),
  bstack1ll11_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵࠪ᳹"),
  bstack1ll11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴࠩᳺ"),
  bstack1ll11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨ᳻"),
  bstack1ll11_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩ᳼"),
  bstack1ll11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧ᳽"),
  bstack1ll11_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧ᳾"),
  bstack1ll11_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨ᳿"),
  bstack1ll11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴀ"),
  bstack1ll11_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪᴁ"),
  bstack1ll11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᴂ"),
  bstack1ll11_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫᴃ"),
  bstack1ll11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪᴄ"),
  bstack1ll11_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪᴅ"),
  bstack1ll11_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫᴆ"),
  bstack1ll11_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬᴇ"),
  bstack1ll11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫᴈ"),
  bstack1ll11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫᴉ"),
  bstack1ll11_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧᴊ"),
  bstack1ll11_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪᴋ"),
  bstack1ll11_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧᴌ"),
  bstack1ll11_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᴍ"),
  bstack1ll11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬᴎ"),
  bstack1ll11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬᴏ"),
  bstack1ll11_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࠧᴐ"),
  bstack1ll11_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧᴑ"),
  bstack1ll11_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨᴒ"),
  bstack1ll11_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨᴓ"),
  bstack1ll11_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪᴔ"),
  bstack1ll11_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᴕ"),
  bstack1ll11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨᴖ"),
  bstack1ll11_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࠪᴗ"),
  bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ᴘ"),
  bstack1ll11_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࠫᴙ"),
  bstack1ll11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ᴚ"),
  bstack1ll11_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪᴛ"),
  bstack1ll11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬᴜ"),
  bstack1ll11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᴝ"),
  bstack1ll11_opy_ (u"࠭ࡩࡦࠩᴞ"),
  bstack1ll11_opy_ (u"ࠧࡦࡦࡪࡩࠬᴟ"),
  bstack1ll11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᴠ"),
  bstack1ll11_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨᴡ"),
  bstack1ll11_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬᴢ"),
  bstack1ll11_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬᴣ"),
  bstack1ll11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫᴤ"),
  bstack1ll11_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩᴥ"),
  bstack1ll11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪᴦ"),
  bstack1ll11_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬᴧ"),
  bstack1ll11_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩᴨ"),
  bstack1ll11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᴩ"),
  bstack1ll11_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ᴪ"),
  bstack1ll11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ᴫ"),
  bstack1ll11_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᴬ"),
  bstack1ll11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧᴭ"),
  bstack1ll11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩᴮ"),
  bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᴯ"),
  bstack1ll11_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨᴰ"),
  bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᴱ"),
  bstack1ll11_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩᴲ"),
  bstack1ll11_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬᴳ"),
  bstack1ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫᴴ"),
  bstack1ll11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫᴵ"),
  bstack1ll11_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴶ"),
  bstack1ll11_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨᴷ"),
  bstack1ll11_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ᴸ"),
  bstack1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᴹ"),
  bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨᴺ"),
  bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᴻ"),
  bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᴼ"),
  bstack1ll11_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬᴽ"),
  bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩᴾ"),
  bstack1ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭ᴿ"),
  bstack1ll11_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨᵀ")
]
bstack1lllll1111_opy_ = {
  bstack1ll11_opy_ (u"࠭ࡶࠨᵁ"): bstack1ll11_opy_ (u"ࠧࡷࠩᵂ"),
  bstack1ll11_opy_ (u"ࠨࡨࠪᵃ"): bstack1ll11_opy_ (u"ࠩࡩࠫᵄ"),
  bstack1ll11_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩᵅ"): bstack1ll11_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪᵆ"),
  bstack1ll11_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᵇ"): bstack1ll11_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬᵈ"),
  bstack1ll11_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫᵉ"): bstack1ll11_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬᵊ"),
  bstack1ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬᵋ"): bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ᵌ"),
  bstack1ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧᵍ"): bstack1ll11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨᵎ"),
  bstack1ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᵏ"): bstack1ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᵐ"),
  bstack1ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᵑ"): bstack1ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᵒ"),
  bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫᵓ"): bstack1ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬᵔ"),
  bstack1ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ᵕ"): bstack1ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᵖ"),
  bstack1ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᵗ"): bstack1ll11_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᵘ"),
  bstack1ll11_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᵙ"): bstack1ll11_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᵚ"),
  bstack1ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᵛ"): bstack1ll11_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᵜ"),
  bstack1ll11_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᵝ"): bstack1ll11_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᵞ"),
  bstack1ll11_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬᵟ"): bstack1ll11_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ᵠ"),
  bstack1ll11_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫᵡ"): bstack1ll11_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᵢ"),
  bstack1ll11_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᵣ"): bstack1ll11_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᵤ"),
  bstack1ll11_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᵥ"): bstack1ll11_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᵦ"),
  bstack1ll11_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪᵧ"): bstack1ll11_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫᵨ"),
  bstack1ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᵩ"): bstack1ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᵪ"),
  bstack1ll11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨᵫ"): bstack1ll11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࠨᵬ")
}
bstack111l111l11l_opy_ = bstack1ll11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡪ࡭ࡹ࡮ࡵࡣ࠰ࡦࡳࡲ࠵ࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪ࠱ࡵࡩࡱ࡫ࡡࡴࡧࡶ࠳ࡱࡧࡴࡦࡵࡷ࠳ࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᵭ")
bstack111l1l11111_opy_ = bstack1ll11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠱࡫ࡩࡦࡲࡴࡩࡥ࡫ࡩࡨࡱࠢᵮ")
bstack1lll1ll1ll_opy_ = bstack1ll11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡪࡪࡳ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡸ࡫࡮ࡥࡡࡶࡨࡰࡥࡥࡷࡧࡱࡸࡸࠨᵯ")
HTTPS_HUB = bstack1ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡽࡤ࠰ࡪࡸࡦࠬᵰ")
bstack111l111ll_opy_ = bstack1ll11_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠨᵱ")
bstack111l11lll1_opy_ = bstack1ll11_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵ࠼࠷࠸࠹࠺࠯ࡸࡦ࠲࡬ࡺࡨࠧᵲ")
bstack1ll11ll1l_opy_ = bstack1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡰࡨࡼࡹࡥࡨࡶࡤࡶࠫᵳ")
bstack11l1l111l_opy_ = {
  bstack1ll11_opy_ (u"ࠨࡦࡨࡪࡦࡻ࡬ࡵࠩᵴ"): bstack1ll11_opy_ (u"ࠩ࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᵵ"),
  bstack1ll11_opy_ (u"ࠪࡹࡸ࠳ࡥࡢࡵࡷࠫᵶ"): bstack1ll11_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡷࡶࡩ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᵷ"),
  bstack1ll11_opy_ (u"ࠬࡻࡳࠨᵸ"): bstack1ll11_opy_ (u"࠭ࡨࡶࡤ࠰ࡹࡸ࠳࡯࡯࡮ࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᵹ"),
  bstack1ll11_opy_ (u"ࠧࡦࡷࠪᵺ"): bstack1ll11_opy_ (u"ࠨࡪࡸࡦ࠲࡫ࡵ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᵻ"),
  bstack1ll11_opy_ (u"ࠩ࡬ࡲࠬᵼ"): bstack1ll11_opy_ (u"ࠪ࡬ࡺࡨ࠭ࡢࡲࡶ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᵽ"),
  bstack1ll11_opy_ (u"ࠫࡦࡻࠧᵾ"): bstack1ll11_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡤࡴࡸ࡫࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᵿ")
}
bstack111l11lll11_opy_ = {
  bstack1ll11_opy_ (u"࠭ࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠨᶀ"): 50,
  bstack1ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᶁ"): 40,
  bstack1ll11_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩᶂ"): 30,
  bstack1ll11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᶃ"): 20,
  bstack1ll11_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᶄ"): 10
}
bstack11l11llll1_opy_ = bstack111l11lll11_opy_[bstack1ll11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᶅ")]
bstack1l111llll_opy_ = bstack1ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠵ࠧᶆ")
bstack1l1l11l1l1_opy_ = bstack1ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᶇ")
bstack111ll1111_opy_ = bstack1ll11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᶈ")
bstack11111l1l_opy_ = bstack1ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᶉ")
bstack1l1ll1111l_opy_ = bstack1ll11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡥࡳࡪࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡳࡥࡨࡱࡡࡨࡧࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧᶊ")
bstack11llllll1l_opy_ = {
  bstack1ll11_opy_ (u"ࠪࡗࡉࡑ࠭ࡈࡇࡑ࠱࠵࠶࠵ࠨᶋ"): bstack1ll11_opy_ (u"ࠫ࠯࠰ࠪࠡ࡝ࡖࡈࡐ࠳ࡇࡆࡐ࠰࠴࠵࠻࡝ࠡࡢࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡤࠥ࡯ࡳࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠤ࡮ࡴࠠࡺࡱࡸࡶࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠱ࠤ࡙࡮ࡩࡴࠢࡰࡥࡾࠦࡣࡢࡷࡶࡩࠥࡩ࡯࡯ࡨ࡯࡭ࡨࡺࡳࠡࡹ࡬ࡸ࡭ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࠦࡩࡵࠢࡸࡷ࡮ࡴࡧ࠻ࠢࡳ࡭ࡵࠦࡵ࡯࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠤ࠯࠰ࠪࠨᶌ")
}
bstack111l11l11ll_opy_ = [bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᶍ"), bstack1ll11_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᶎ")]
bstack111l1111ll1_opy_ = [bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᶏ"), bstack1ll11_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᶐ")]
bstack1lll11l1_opy_ = re.compile(bstack1ll11_opy_ (u"ࠩࡡ࡟ࡡࡢࡷ࠮࡟࠮࠾࠳࠰ࠤࠨᶑ"))
bstack111l111ll1_opy_ = [
  bstack1ll11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡎࡢ࡯ࡨࠫᶒ"),
  bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᶓ"),
  bstack1ll11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᶔ"),
  bstack1ll11_opy_ (u"࠭࡮ࡦࡹࡆࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪᶕ"),
  bstack1ll11_opy_ (u"ࠧࡢࡲࡳࠫᶖ"),
  bstack1ll11_opy_ (u"ࠨࡷࡧ࡭ࡩ࠭ᶗ"),
  bstack1ll11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫᶘ"),
  bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࠪᶙ"),
  bstack1ll11_opy_ (u"ࠫࡴࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᶚ"),
  bstack1ll11_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࠪᶛ"),
  bstack1ll11_opy_ (u"࠭࡮ࡰࡔࡨࡷࡪࡺࠧᶜ"), bstack1ll11_opy_ (u"ࠧࡧࡷ࡯ࡰࡗ࡫ࡳࡦࡶࠪᶝ"),
  bstack1ll11_opy_ (u"ࠨࡥ࡯ࡩࡦࡸࡓࡺࡵࡷࡩࡲࡌࡩ࡭ࡧࡶࠫᶞ"),
  bstack1ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡕ࡫ࡰ࡭ࡳ࡭ࡳࠨᶟ"),
  bstack1ll11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࡌࡰࡩࡪ࡭ࡳ࡭ࠧᶠ"),
  bstack1ll11_opy_ (u"ࠫࡴࡺࡨࡦࡴࡄࡴࡵࡹࠧᶡ"),
  bstack1ll11_opy_ (u"ࠬࡶࡲࡪࡰࡷࡔࡦ࡭ࡥࡔࡱࡸࡶࡨ࡫ࡏ࡯ࡈ࡬ࡲࡩࡌࡡࡪ࡮ࡸࡶࡪ࠭ᶢ"),
  bstack1ll11_opy_ (u"࠭ࡡࡱࡲࡄࡧࡹ࡯ࡶࡪࡶࡼࠫᶣ"), bstack1ll11_opy_ (u"ࠧࡢࡲࡳࡔࡦࡩ࡫ࡢࡩࡨࠫᶤ"), bstack1ll11_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡃࡦࡸ࡮ࡼࡩࡵࡻࠪᶥ"), bstack1ll11_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡓࡥࡨࡱࡡࡨࡧࠪᶦ"), bstack1ll11_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᶧ"),
  bstack1ll11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩᶨ"),
  bstack1ll11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡪࡹࡴࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩᶩ"),
  bstack1ll11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࠨᶪ"), bstack1ll11_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࡇࡱࡨࡎࡴࡴࡦࡰࡷࠫᶫ"),
  bstack1ll11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᶬ"),
  bstack1ll11_opy_ (u"ࠩࡤࡨࡧࡖ࡯ࡳࡶࠪᶭ"),
  bstack1ll11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡖࡳࡨࡱࡥࡵࠩᶮ"),
  bstack1ll11_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰ࡙࡯࡭ࡦࡱࡸࡸࠬᶯ"),
  bstack1ll11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡵࡪࠪᶰ"),
  bstack1ll11_opy_ (u"࠭ࡡࡷࡦࠪᶱ"), bstack1ll11_opy_ (u"ࠧࡢࡸࡧࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪᶲ"), bstack1ll11_opy_ (u"ࠨࡣࡹࡨࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪᶳ"), bstack1ll11_opy_ (u"ࠩࡤࡺࡩࡇࡲࡨࡵࠪᶴ"),
  bstack1ll11_opy_ (u"ࠪࡹࡸ࡫ࡋࡦࡻࡶࡸࡴࡸࡥࠨᶵ"), bstack1ll11_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡵࡪࠪᶶ"), bstack1ll11_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡵࡶࡻࡴࡸࡤࠨᶷ"),
  bstack1ll11_opy_ (u"࠭࡫ࡦࡻࡄࡰ࡮ࡧࡳࠨᶸ"), bstack1ll11_opy_ (u"ࠧ࡬ࡧࡼࡔࡦࡹࡳࡸࡱࡵࡨࠬᶹ"),
  bstack1ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪᶺ"), bstack1ll11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡂࡴࡪࡷࠬᶻ"), bstack1ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࡉ࡯ࡲࠨᶼ"), bstack1ll11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡆ࡬ࡷࡵ࡭ࡦࡏࡤࡴࡵ࡯࡮ࡨࡈ࡬ࡰࡪ࠭ᶽ"), bstack1ll11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵ࡙ࡸ࡫ࡓࡺࡵࡷࡩࡲࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩᶾ"),
  bstack1ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࠩᶿ"), bstack1ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࡶࠫ᷀"),
  bstack1ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡄࡪࡵࡤࡦࡱ࡫ࡂࡶ࡫࡯ࡨࡈ࡮ࡥࡤ࡭ࠪ᷁"),
  bstack1ll11_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࡔࡪ࡯ࡨࡳࡺࡺ᷂ࠧ"),
  bstack1ll11_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡄࡧࡹ࡯࡯࡯ࠩ᷃"), bstack1ll11_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡇࡦࡺࡥࡨࡱࡵࡽࠬ᷄"), bstack1ll11_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡋࡲࡡࡨࡵࠪ᷅"), bstack1ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࡊࡰࡷࡩࡳࡺࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩ᷆"),
  bstack1ll11_opy_ (u"ࠧࡥࡱࡱࡸࡘࡺ࡯ࡱࡃࡳࡴࡔࡴࡒࡦࡵࡨࡸࠬ᷇"),
  bstack1ll11_opy_ (u"ࠨࡷࡱ࡭ࡨࡵࡤࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪ᷈"), bstack1ll11_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡌࡧࡼࡦࡴࡧࡲࡥࠩ᷉"),
  bstack1ll11_opy_ (u"ࠪࡲࡴ࡙ࡩࡨࡰ᷊ࠪ"),
  bstack1ll11_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨ࡙ࡳ࡯࡭ࡱࡱࡵࡸࡦࡴࡴࡗ࡫ࡨࡻࡸ࠭᷋"),
  bstack1ll11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡥࡴࡲ࡭ࡩ࡝ࡡࡵࡥ࡫ࡩࡷࡹࠧ᷌"),
  bstack1ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᷍"),
  bstack1ll11_opy_ (u"ࠧࡳࡧࡦࡶࡪࡧࡴࡦࡅ࡫ࡶࡴࡳࡥࡅࡴ࡬ࡺࡪࡸࡓࡦࡵࡶ࡭ࡴࡴࡳࠨ᷎"),
  bstack1ll11_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺ᷏ࠧ"),
  bstack1ll11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡖࡡࡵࡪ᷐ࠪ"),
  bstack1ll11_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡗࡵ࡫ࡥࡥࠩ᷑"),
  bstack1ll11_opy_ (u"ࠫ࡬ࡶࡳࡆࡰࡤࡦࡱ࡫ࡤࠨ᷒"),
  bstack1ll11_opy_ (u"ࠬ࡯ࡳࡉࡧࡤࡨࡱ࡫ࡳࡴࠩᷓ"),
  bstack1ll11_opy_ (u"࠭ࡡࡥࡤࡈࡼࡪࡩࡔࡪ࡯ࡨࡳࡺࡺࠧᷔ"),
  bstack1ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ᷕ"),
  bstack1ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡊࡥࡷ࡫ࡦࡩࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬᷖ"),
  bstack1ll11_opy_ (u"ࠩࡤࡹࡹࡵࡇࡳࡣࡱࡸࡕ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠩᷗ"),
  bstack1ll11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡒࡦࡺࡵࡳࡣ࡯ࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᷘ"),
  bstack1ll11_opy_ (u"ࠫࡸࡿࡳࡵࡧࡰࡔࡴࡸࡴࠨᷙ"),
  bstack1ll11_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡪࡢࡉࡱࡶࡸࠬᷚ"),
  bstack1ll11_opy_ (u"࠭ࡳ࡬࡫ࡳ࡙ࡳࡲ࡯ࡤ࡭ࠪᷛ"), bstack1ll11_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡔࡺࡲࡨࠫᷜ"), bstack1ll11_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡌࡧࡼࠫᷝ"),
  bstack1ll11_opy_ (u"ࠩࡤࡹࡹࡵࡌࡢࡷࡱࡧ࡭࠭ᷞ"),
  bstack1ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡧࡦࡺࡃࡢࡲࡷࡹࡷ࡫ࠧᷟ"),
  bstack1ll11_opy_ (u"ࠫࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࡏࡵࡪࡨࡶࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ᷠ"),
  bstack1ll11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪ࡝ࡩ࡯ࡦࡲࡻࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࠧᷡ"),
  bstack1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡵ࡯࡭ࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᷢ"),
  bstack1ll11_opy_ (u"ࠧࡦࡰࡩࡳࡷࡩࡥࡂࡲࡳࡍࡳࡹࡴࡢ࡮࡯ࠫᷣ"),
  bstack1ll11_opy_ (u"ࠨࡧࡱࡷࡺࡸࡥࡘࡧࡥࡺ࡮࡫ࡷࡴࡊࡤࡺࡪࡖࡡࡨࡧࡶࠫᷤ"), bstack1ll11_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡇࡩࡻࡺ࡯ࡰ࡮ࡶࡔࡴࡸࡴࠨᷥ"), bstack1ll11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧ࡚ࡩࡧࡼࡩࡦࡹࡇࡩࡹࡧࡩ࡭ࡵࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠭ᷦ"),
  bstack1ll11_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡵࡶࡳࡄࡣࡦ࡬ࡪࡒࡩ࡮࡫ࡷࠫᷧ"),
  bstack1ll11_opy_ (u"ࠬࡩࡡ࡭ࡧࡱࡨࡦࡸࡆࡰࡴࡰࡥࡹ࠭ᷨ"),
  bstack1ll11_opy_ (u"࠭ࡢࡶࡰࡧࡰࡪࡏࡤࠨᷩ"),
  bstack1ll11_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧᷪ"),
  bstack1ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡉࡳࡧࡢ࡭ࡧࡧࠫᷫ"), bstack1ll11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡆࡻࡴࡩࡱࡵ࡭ࡿ࡫ࡤࠨᷬ"),
  bstack1ll11_opy_ (u"ࠪࡥࡺࡺ࡯ࡂࡥࡦࡩࡵࡺࡁ࡭ࡧࡵࡸࡸ࠭ᷭ"), bstack1ll11_opy_ (u"ࠫࡦࡻࡴࡰࡆ࡬ࡷࡲ࡯ࡳࡴࡃ࡯ࡩࡷࡺࡳࠨᷮ"),
  bstack1ll11_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡴࡎ࡬ࡦࠬᷯ"),
  bstack1ll11_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡖࡤࡴࠬᷰ"),
  bstack1ll11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉ࡯࡫ࡷ࡭ࡦࡲࡕࡳ࡮ࠪᷱ"), bstack1ll11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡂ࡮࡯ࡳࡼࡖ࡯ࡱࡷࡳࡷࠬᷲ"), bstack1ll11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡪࡲࡴࡸࡥࡇࡴࡤࡹࡩ࡝ࡡࡳࡰ࡬ࡲ࡬࠭ᷳ"), bstack1ll11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡪࡴࡌࡪࡰ࡮ࡷࡎࡴࡂࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠪᷴ"),
  bstack1ll11_opy_ (u"ࠫࡰ࡫ࡥࡱࡍࡨࡽࡈ࡮ࡡࡪࡰࡶࠫ᷵"),
  bstack1ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡿࡧࡢ࡭ࡧࡖࡸࡷ࡯࡮ࡨࡵࡇ࡭ࡷ࠭᷶"),
  bstack1ll11_opy_ (u"࠭ࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡸࡱࡪࡴࡴࡴ᷷ࠩ"),
  bstack1ll11_opy_ (u"ࠧࡪࡰࡷࡩࡷࡑࡥࡺࡆࡨࡰࡦࡿ᷸ࠧ"),
  bstack1ll11_opy_ (u"ࠨࡵ࡫ࡳࡼࡏࡏࡔࡎࡲ࡫᷹ࠬ"),
  bstack1ll11_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡖࡸࡷࡧࡴࡦࡩࡼ᷺ࠫ"),
  bstack1ll11_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡕࡩࡸࡶ࡯࡯ࡵࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ᷻"), bstack1ll11_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡘࡣ࡬ࡸ࡙࡯࡭ࡦࡱࡸࡸࠬ᷼"),
  bstack1ll11_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࠨ᷽"),
  bstack1ll11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡳࡺࡰࡦࡉࡽ࡫ࡣࡶࡶࡨࡊࡷࡵ࡭ࡉࡶࡷࡴࡸ࠭᷾"),
  bstack1ll11_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡄࡣࡳࡸࡺࡸࡥࠨ᷿"),
  bstack1ll11_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨḀ"),
  bstack1ll11_opy_ (u"ࠩࡩࡹࡱࡲࡃࡰࡰࡷࡩࡽࡺࡌࡪࡵࡷࠫḁ"),
  bstack1ll11_opy_ (u"ࠪࡻࡦ࡯ࡴࡇࡱࡵࡅࡵࡶࡓࡤࡴ࡬ࡴࡹ࠭Ḃ"),
  bstack1ll11_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡈࡵ࡮࡯ࡧࡦࡸࡗ࡫ࡴࡳ࡫ࡨࡷࠬḃ"),
  bstack1ll11_opy_ (u"ࠬࡧࡰࡱࡐࡤࡱࡪ࠭Ḅ"),
  bstack1ll11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡓࡍࡅࡨࡶࡹ࠭ḅ"),
  bstack1ll11_opy_ (u"ࠧࡵࡣࡳ࡛࡮ࡺࡨࡔࡪࡲࡶࡹࡖࡲࡦࡵࡶࡈࡺࡸࡡࡵ࡫ࡲࡲࠬḆ"),
  bstack1ll11_opy_ (u"ࠨࡵࡦࡥࡱ࡫ࡆࡢࡥࡷࡳࡷ࠭ḇ"),
  bstack1ll11_opy_ (u"ࠩࡺࡨࡦࡒ࡯ࡤࡣ࡯ࡔࡴࡸࡴࠨḈ"),
  bstack1ll11_opy_ (u"ࠪࡷ࡭ࡵࡷ࡙ࡥࡲࡨࡪࡒ࡯ࡨࠩḉ"),
  bstack1ll11_opy_ (u"ࠫ࡮ࡵࡳࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡸࡷࡪ࠭Ḋ"),
  bstack1ll11_opy_ (u"ࠬࡾࡣࡰࡦࡨࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠧḋ"),
  bstack1ll11_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡶࡷࡼࡵࡲࡥࠩḌ"),
  bstack1ll11_opy_ (u"ࠧࡶࡵࡨࡔࡷ࡫ࡢࡶ࡫࡯ࡸ࡜ࡊࡁࠨḍ"),
  bstack1ll11_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵ࡙ࡇࡅࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠩḎ"),
  bstack1ll11_opy_ (u"ࠩࡺࡩࡧࡊࡲࡪࡸࡨࡶࡆ࡭ࡥ࡯ࡶࡘࡶࡱ࠭ḏ"),
  bstack1ll11_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡴࡩࠩḐ"),
  bstack1ll11_opy_ (u"ࠫࡺࡹࡥࡏࡧࡺ࡛ࡉࡇࠧḑ"),
  bstack1ll11_opy_ (u"ࠬࡽࡤࡢࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨḒ"), bstack1ll11_opy_ (u"࠭ࡷࡥࡣࡆࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ḓ"),
  bstack1ll11_opy_ (u"ࠧࡹࡥࡲࡨࡪࡕࡲࡨࡋࡧࠫḔ"), bstack1ll11_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡓࡪࡩࡱ࡭ࡳ࡭ࡉࡥࠩḕ"),
  bstack1ll11_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦ࡚ࡈࡆࡈࡵ࡯ࡦ࡯ࡩࡎࡪࠧḖ"),
  bstack1ll11_opy_ (u"ࠪࡶࡪࡹࡥࡵࡑࡱࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡲࡵࡑࡱࡰࡾ࠭ḗ"),
  bstack1ll11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࡸ࠭Ḙ"),
  bstack1ll11_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷ࡯ࡥࡴࠩḙ"), bstack1ll11_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡹࡊࡰࡷࡩࡷࡼࡡ࡭ࠩḚ"),
  bstack1ll11_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࡉࡣࡵࡨࡼࡧࡲࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪḛ"),
  bstack1ll11_opy_ (u"ࠨ࡯ࡤࡼ࡙ࡿࡰࡪࡰࡪࡊࡷ࡫ࡱࡶࡧࡱࡧࡾ࠭Ḝ"),
  bstack1ll11_opy_ (u"ࠩࡶ࡭ࡲࡶ࡬ࡦࡋࡶ࡚࡮ࡹࡩࡣ࡮ࡨࡇ࡭࡫ࡣ࡬ࠩḝ"),
  bstack1ll11_opy_ (u"ࠪࡹࡸ࡫ࡃࡢࡴࡷ࡬ࡦ࡭ࡥࡔࡵ࡯ࠫḞ"),
  bstack1ll11_opy_ (u"ࠫࡸ࡮࡯ࡶ࡮ࡧ࡙ࡸ࡫ࡓࡪࡰࡪࡰࡪࡺ࡯࡯ࡖࡨࡷࡹࡓࡡ࡯ࡣࡪࡩࡷ࠭ḟ"),
  bstack1ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡍ࡜ࡊࡐࠨḠ"),
  bstack1ll11_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙ࡵࡵࡤࡪࡌࡨࡊࡴࡲࡰ࡮࡯ࠫḡ"),
  bstack1ll11_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡈࡪࡦࡧࡩࡳࡇࡰࡪࡒࡲࡰ࡮ࡩࡹࡆࡴࡵࡳࡷ࠭Ḣ"),
  bstack1ll11_opy_ (u"ࠨ࡯ࡲࡧࡰࡒ࡯ࡤࡣࡷ࡭ࡴࡴࡁࡱࡲࠪḣ"),
  bstack1ll11_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈࡲࡶࡲࡧࡴࠨḤ"), bstack1ll11_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉ࡭ࡱࡺࡥࡳࡕࡳࡩࡨࡹࠧḥ"),
  bstack1ll11_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡇࡩࡱࡧࡹࡂࡦࡥࠫḦ"),
  bstack1ll11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡏࡤࡍࡱࡦࡥࡹࡵࡲࡂࡷࡷࡳࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠨḧ")
]
bstack1l11l1111l_opy_ = bstack1ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡻࡰ࡭ࡱࡤࡨࠬḨ")
bstack11111l111l_opy_ = [bstack1ll11_opy_ (u"ࠧ࠯ࡣࡳ࡯ࠬḩ"), bstack1ll11_opy_ (u"ࠨ࠰ࡤࡥࡧ࠭Ḫ"), bstack1ll11_opy_ (u"ࠩ࠱࡭ࡵࡧࠧḫ")]
bstack11l111l1_opy_ = [bstack1ll11_opy_ (u"ࠪ࡭ࡩ࠭Ḭ"), bstack1ll11_opy_ (u"ࠫࡵࡧࡴࡩࠩḭ"), bstack1ll11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨḮ"), bstack1ll11_opy_ (u"࠭ࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࠬḯ")]
bstack1llllll1l_opy_ = {
  bstack1ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧḰ"): bstack1ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ḱ"),
  bstack1ll11_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪḲ"): bstack1ll11_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨḳ"),
  bstack1ll11_opy_ (u"ࠫࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩḴ"): bstack1ll11_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ḵ"),
  bstack1ll11_opy_ (u"࠭ࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩḶ"): bstack1ll11_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ḷ"),
  bstack1ll11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡷ࡭ࡴࡴࡳࠨḸ"): bstack1ll11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪḹ")
}
bstack1l1ll11ll_opy_ = [
  bstack1ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨḺ"),
  bstack1ll11_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩḻ"),
  bstack1ll11_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭Ḽ"),
  bstack1ll11_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬḽ"),
  bstack1ll11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨḾ"),
]
bstack1l1l1ll11l_opy_ = bstack111ll111l1_opy_ + bstack111l11llll1_opy_ + bstack111l111ll1_opy_
bstack1111ll1lll_opy_ = [
  bstack1ll11_opy_ (u"ࠨࡠ࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸࠩ࠭ḿ"),
  bstack1ll11_opy_ (u"ࠩࡡࡦࡸ࠳࡬ࡰࡥࡤࡰ࠳ࡩ࡯࡮ࠦࠪṀ"),
  bstack1ll11_opy_ (u"ࠪࡢ࠶࠸࠷࠯ࠩṁ"),
  bstack1ll11_opy_ (u"ࠫࡣ࠷࠰࠯ࠩṂ"),
  bstack1ll11_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠵ࡠ࠼࠭࠺࡟࠱ࠫṃ"),
  bstack1ll11_opy_ (u"࠭࡞࠲࠹࠵࠲࠷ࡡ࠰࠮࠻ࡠ࠲ࠬṄ"),
  bstack1ll11_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠹࡛࠱࠯࠴ࡡ࠳࠭ṅ"),
  bstack1ll11_opy_ (u"ࠨࡠ࠴࠽࠷࠴࠱࠷࠺࠱ࠫṆ")
]
bstack111l1ll1ll1_opy_ = bstack1ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪṇ")
bstack11l11l1l11_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠯ࡷ࠳࠲ࡩࡻ࡫࡮ࡵࠩṈ")
bstack1ll1l111_opy_ = [ bstack1ll11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ṉ") ]
bstack11llll1ll_opy_ = [ bstack1ll11_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫṊ") ]
bstack1111lll1_opy_ = [bstack1ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪṋ")]
bstack1llllll111_opy_ = [ bstack1ll11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧṌ") ]
bstack1111l1111_opy_ = bstack1ll11_opy_ (u"ࠨࡕࡇࡏࡘ࡫ࡴࡶࡲࠪṍ")
bstack111l111l1l_opy_ = bstack1ll11_opy_ (u"ࠩࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠬṎ")
bstack11ll11ll11_opy_ = bstack1ll11_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠧṏ")
bstack1l11l1l11l_opy_ = bstack1ll11_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࠪṐ")
bstack1lll1ll11l_opy_ = [
  bstack1ll11_opy_ (u"ࠬࡋࡒࡓࡡࡉࡅࡎࡒࡅࡅࠩṑ"),
  bstack1ll11_opy_ (u"࠭ࡅࡓࡔࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭Ṓ"),
  bstack1ll11_opy_ (u"ࠧࡆࡔࡕࡣࡇࡒࡏࡄࡍࡈࡈࡤࡈ࡙ࡠࡅࡏࡍࡊࡔࡔࠨṓ"),
  bstack1ll11_opy_ (u"ࠨࡇࡕࡖࡤࡔࡅࡕ࡙ࡒࡖࡐࡥࡃࡉࡃࡑࡋࡊࡊࠧṔ"),
  bstack1ll11_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡉ࡙ࡥࡎࡐࡖࡢࡇࡔࡔࡎࡆࡅࡗࡉࡉ࠭ṕ"),
  bstack1ll11_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡈࡒࡏࡔࡇࡇࠫṖ"),
  bstack1ll11_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡘࡅࡔࡇࡗࠫṗ"),
  bstack1ll11_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡈࡘࡗࡊࡊࠧṘ"),
  bstack1ll11_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡂࡄࡒࡖ࡙ࡋࡄࠨṙ"),
  bstack1ll11_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨṚ"),
  bstack1ll11_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡒࡔ࡚࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࠩṛ"),
  bstack1ll11_opy_ (u"ࠩࡈࡖࡗࡥࡁࡅࡆࡕࡉࡘ࡙࡟ࡊࡐ࡙ࡅࡑࡏࡄࠨṜ"),
  bstack1ll11_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡗࡑࡖࡊࡇࡃࡉࡃࡅࡐࡊ࠭ṝ"),
  bstack1ll11_opy_ (u"ࠫࡊࡘࡒࡠࡖࡘࡒࡓࡋࡌࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬṞ"),
  bstack1ll11_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡔࡊࡏࡈࡈࡤࡕࡕࡕࠩṟ"),
  bstack1ll11_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡔࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭Ṡ"),
  bstack1ll11_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡉࡑࡖࡘࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪṡ"),
  bstack1ll11_opy_ (u"ࠨࡇࡕࡖࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨṢ"),
  bstack1ll11_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪṣ"),
  bstack1ll11_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡘࡅࡔࡑࡏ࡙࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩṤ"),
  bstack1ll11_opy_ (u"ࠫࡊࡘࡒࡠࡏࡄࡒࡉࡇࡔࡐࡔ࡜ࡣࡕࡘࡏ࡙࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪṥ"),
]
bstack1l11l111l1_opy_ = bstack1ll11_opy_ (u"ࠬ࠴࠯ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠱ࠪṦ")
bstack1l111l11_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"࠭ࡾࠨṧ")), bstack1ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧṨ"), bstack1ll11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧṩ"))
bstack111ll1ll111_opy_ = bstack1ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱ࡫ࠪṪ")
bstack111l1l1111l_opy_ = [ bstack1ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪṫ"), bstack1ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪṬ"), bstack1ll11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫṭ"), bstack1ll11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭Ṯ")]
bstack1l1ll111_opy_ = [ bstack1ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧṯ"), bstack1ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧṰ"), bstack1ll11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨṱ"), bstack1ll11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪṲ") ]
bstack111ll1ll_opy_ = [ bstack1ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪṳ") ]
bstack111l11ll11l_opy_ = [ bstack1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬṴ"), bstack1ll11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ṵ") ]
bstack1l1lll1ll1_opy_ = 360
bstack111l1ll1l11_opy_ = bstack1ll11_opy_ (u"ࠢࡢࡲࡳ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢṶ")
bstack1111llll11l_opy_ = bstack1ll11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵࠥṷ")
bstack111l111l1ll_opy_ = bstack1ll11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠧṸ")
bstack111ll11l1l1_opy_ = bstack1ll11_opy_ (u"ࠥࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡹ࡫ࡳࡵࡵࠣࡥࡷ࡫ࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡏࡔࠢࡹࡩࡷࡹࡩࡰࡰࠣࠩࡸࠦࡡ࡯ࡦࠣࡥࡧࡵࡶࡦࠢࡩࡳࡷࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠࡥࡧࡹ࡭ࡨ࡫ࡳ࠯ࠤṹ")
bstack111ll1l1l1l_opy_ = bstack1ll11_opy_ (u"ࠦ࠶࠷࠮࠱ࠤṺ")
bstack1lll1l1llll_opy_ = {
  bstack1ll11_opy_ (u"ࠬࡖࡁࡔࡕࠪṻ"): bstack1ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ṽ"),
  bstack1ll11_opy_ (u"ࠧࡇࡃࡌࡐࠬṽ"): bstack1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨṾ"),
  bstack1ll11_opy_ (u"ࠩࡖࡏࡎࡖࠧṿ"): bstack1ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫẀ")
}
bstack111llll111_opy_ = [
  bstack1ll11_opy_ (u"ࠦ࡬࡫ࡴࠣẁ"),
  bstack1ll11_opy_ (u"ࠧ࡭࡯ࡃࡣࡦ࡯ࠧẂ"),
  bstack1ll11_opy_ (u"ࠨࡧࡰࡈࡲࡶࡼࡧࡲࡥࠤẃ"),
  bstack1ll11_opy_ (u"ࠢࡳࡧࡩࡶࡪࡹࡨࠣẄ"),
  bstack1ll11_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢẅ"),
  bstack1ll11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨẆ"),
  bstack1ll11_opy_ (u"ࠥࡷࡺࡨ࡭ࡪࡶࡈࡰࡪࡳࡥ࡯ࡶࠥẇ"),
  bstack1ll11_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣẈ"),
  bstack1ll11_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣẉ"),
  bstack1ll11_opy_ (u"ࠨࡣ࡭ࡧࡤࡶࡊࡲࡥ࡮ࡧࡱࡸࠧẊ"),
  bstack1ll11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࡳࠣẋ"),
  bstack1ll11_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠣẌ"),
  bstack1ll11_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࡄࡷࡾࡴࡣࡔࡥࡵ࡭ࡵࡺࠢẍ"),
  bstack1ll11_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤẎ"),
  bstack1ll11_opy_ (u"ࠦࡶࡻࡩࡵࠤẏ"),
  bstack1ll11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲ࡚࡯ࡶࡥ࡫ࡅࡨࡺࡩࡰࡰࠥẐ"),
  bstack1ll11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳࡍࡶ࡮ࡷ࡭࡙ࡵࡵࡤࡪࠥẑ"),
  bstack1ll11_opy_ (u"ࠢࡴࡪࡤ࡯ࡪࠨẒ"),
  bstack1ll11_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࡁࡱࡲࠥẓ")
]
bstack111l11111l1_opy_ = [
  bstack1ll11_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࠣẔ"),
  bstack1ll11_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢẕ"),
  bstack1ll11_opy_ (u"ࠦࡦࡻࡴࡰࠤẖ"),
  bstack1ll11_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧẗ"),
  bstack1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣẘ")
]
bstack1l1l11llll_opy_ = {
  bstack1ll11_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨẙ"): [bstack1ll11_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢẚ")],
  bstack1ll11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨẛ"): [bstack1ll11_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢẜ")],
  bstack1ll11_opy_ (u"ࠦࡦࡻࡴࡰࠤẝ"): [bstack1ll11_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡇ࡯ࡩࡲ࡫࡮ࡵࠤẞ"), bstack1ll11_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡄࡧࡹ࡯ࡶࡦࡇ࡯ࡩࡲ࡫࡮ࡵࠤẟ"), bstack1ll11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦẠ"), bstack1ll11_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢạ")],
  bstack1ll11_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤẢ"): [bstack1ll11_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥả")],
  bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨẤ"): [bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢấ")],
}
bstack111l11l1111_opy_ = {
  bstack1ll11_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧẦ"): bstack1ll11_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨầ"),
  bstack1ll11_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧẨ"): bstack1ll11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨẩ"),
  bstack1ll11_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢẪ"): bstack1ll11_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨẫ"),
  bstack1ll11_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣẬ"): bstack1ll11_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࠣậ"),
  bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤẮ"): bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥắ")
}
bstack1llll1111l1_opy_ = {
  bstack1ll11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭Ằ"): bstack1ll11_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡖࡩࡹࡻࡰࠨằ"),
  bstack1ll11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧẲ"): bstack1ll11_opy_ (u"࡙ࠬࡵࡪࡶࡨࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭ẳ"),
  bstack1ll11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫẴ"): bstack1ll11_opy_ (u"ࠧࡕࡧࡶࡸ࡙ࠥࡥࡵࡷࡳࠫẵ"),
  bstack1ll11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬẶ"): bstack1ll11_opy_ (u"ࠩࡗࡩࡸࡺࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩặ")
}
bstack111l111llll_opy_ = 65536
bstack111l111lll1_opy_ = bstack1ll11_opy_ (u"ࠪ࠲࠳࠴࡛ࡕࡔࡘࡒࡈࡇࡔࡆࡆࡠࠫẸ")
bstack111l111l111_opy_ = [
      bstack1ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ẹ"), bstack1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨẺ"), bstack1ll11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩẻ"), bstack1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫẼ"), bstack1ll11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪẽ"),
      bstack1ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬẾ"), bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ế"), bstack1ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬỀ"), bstack1ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ề"),
      bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫ࠧỂ"), bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩể"), bstack1ll11_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫỄ")
    ]
bstack111l11111ll_opy_= {
  bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ễ"): bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧỆ"),
  bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨệ"): bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩỈ"),
  bstack1ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬỉ"): bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫỊ"),
  bstack1ll11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨị"): bstack1ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩỌ"),
  bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ọ"): bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧỎ"),
  bstack1ll11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧỏ"): bstack1ll11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨỐ"),
  bstack1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪố"): bstack1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫỒ"),
  bstack1ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ồ"): bstack1ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧỔ"),
  bstack1ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧổ"): bstack1ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨỖ"),
  bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫỗ"): bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬỘ"),
  bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬộ"): bstack1ll11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ớ"),
  bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪớ"): bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫỜ"),
  bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩờ"): bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪỞ"),
  bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࠧở"): bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࡐࡲࡷ࡭ࡴࡴࡳࠨỠ"),
  bstack1ll11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫỡ"): bstack1ll11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬỢ"),
  bstack1ll11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨợ"): bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧỤ"),
  bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨụ"): bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩỦ"),
  bstack1ll11_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬủ"): bstack1ll11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭Ứ"),
  bstack1ll11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩứ"): bstack1ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪỪ"),
  bstack1ll11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫừ"): bstack1ll11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬỬ"),
  bstack1ll11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪử"): bstack1ll11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫỮ"),
  bstack1ll11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫữ"): bstack1ll11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬỰ"),
  bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫự"): bstack1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬỲ"),
  bstack1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ỳ"): bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧỴ"),
  bstack1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬỵ"): bstack1ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Ỷ"),
  bstack1ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧỷ"): bstack1ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨỸ"),
  bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩỹ"): bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪỺ"),
  bstack1ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧỻ"): bstack1ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨỼ")
}
bstack111l111ll1l_opy_ = [bstack1ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩỽ"), bstack1ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩỾ")]
bstack11l111ll11_opy_ = (bstack1ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦỿ"),)
bstack1111llllll1_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠱ࡹ࠵࠴ࡻࡰࡥࡣࡷࡩࡤࡩ࡬ࡪࠩἀ")
bstack11l111ll1l_opy_ = bstack1ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠯ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠵ࡶ࠲࠱ࡪࡶ࡮ࡪࡳ࠰ࠤἁ")
bstack1llll11l1_opy_ = bstack1ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩࡵ࡭ࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࠨἂ")
bstack11l1ll11ll_opy_ = bstack1ll11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠤἃ")
class EVENTS(Enum):
  bstack111l11ll111_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭ἄ")
  bstack1111ll1ll_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮ࡨࡥࡳࡻࡰࠨἅ")
  bstack111l1ll11_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡨ࡬ࡲࡦࡲࡩࡻࡧࠪἆ")
  bstack1111lllll11_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࡬ࡰࡩࡶࠫἇ")
  bstack11l11lll_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩἈ") #shift post bstack111l111l1l1_opy_
  bstack1111l11l11_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨἉ") #shift post bstack111l111l1l1_opy_
  bstack1111llll1l1_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶ࡫ࡹࡧ࠭Ἂ") #shift
  bstack111l111ll11_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧἋ") #shift
  bstack1lllll1ll1_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠾࡭ࡻࡢ࠮࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠬἌ")
  bstack1l11l1ll1ll_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡳࡢࡸࡨ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷࠬἍ")
  bstack11ll1ll1l1_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡱࡧࡵࡪࡴࡸ࡭ࡴࡥࡤࡲࠬἎ")
  bstack1ll1lllll_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡲ࡯ࡤࡣ࡯ࠫἏ") #shift
  bstack1lllll11ll_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡥࡵࡶ࠭ࡶࡲ࡯ࡳࡦࡪࠧἐ") #shift
  bstack1lll11111l_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡤ࡫࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠭ἑ")
  bstack11l1l111ll_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪἒ") #shift
  bstack11lllll111_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵࠪἓ") #shift
  bstack111l11l1lll_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿࠧἔ") #shift
  bstack11llll11ll1_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬἕ")
  bstack111l11llll_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡳࡵࡣࡷࡹࡸ࠭἖") #shift
  bstack1l11ll11l_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡨࡶࡤ࠰ࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠧ἗")
  bstack111l1111l11_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡰࡺࡼ࠱ࡸ࡫ࡴࡶࡲࠪἘ") #shift
  bstack11ll1l111l_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡶࡸࡴࠬἙ")
  bstack111l11l1l1l_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡳ࡯ࡣࡳࡷ࡭ࡵࡴࠨἚ") # not bstack1111llll1ll_opy_ in python
  bstack111ll1l1l_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡳࡸ࡭ࡹ࠭Ἓ") # used in bstack111l11lllll_opy_
  bstack11l1111lll1_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡶࡪ࠳ࡱࡶ࡫ࡷࠫἜ")
  bstack11l1111ll1l_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮ࡳࡸ࡭ࡹ࠭Ἕ")
  bstack1ll111111_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾࡬࡫ࡴࠨ἞") # used in bstack111l11lllll_opy_
  bstack11l1l1l1_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿࡮࡯ࡰ࡭ࠪ἟")
  bstack11l11l11l11_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡧ࠰࡬ࡴࡵ࡫ࠨἠ")
  bstack11l11l111l1_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡱࡶࡸ࠲࡮࡯ࡰ࡭ࠪἡ")
  bstack1111ll1l1l_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠩἢ")
  bstack11ll1111l_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠩἣ") #
  bstack1l11l1ll11_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡦࡵ࡭ࡻ࡫ࡲ࠮ࡶࡤ࡯ࡪ࡙ࡣࡳࡧࡨࡲࡘ࡮࡯ࡵࠩἤ")
  bstack11ll11l111_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡥࡺࡺ࡯࠮ࡥࡤࡴࡹࡻࡲࡦࠩἥ")
  bstack1l1llll1_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡦ࠯ࡷࡩࡸࡺࠧἦ")
  bstack11lll111_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡰࡰࡵࡷ࠱ࡹ࡫ࡳࡵࠩἧ")
  bstack1lll1ll111_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡴࡨ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬἨ") #shift
  bstack1ll11llll_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧἩ") #shift
  bstack111l1111l1l_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࠭ࡤࡣࡳࡸࡺࡸࡥࠨἪ")
  bstack111l11l111l_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿࡯ࡤ࡭ࡧ࠰ࡸ࡮ࡳࡥࡰࡷࡷࠫἫ")
  bstack1l1lllll_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾ࡪࡾࡩࡵ࠯࡫ࡥࡳࡪ࡬ࡦࡴࠪἬ")
  bstack1ll11111ll1_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡨࡼ࡮ࡺ࠭ࡩࡣࡱࡨࡱ࡫ࡲࠨἭ")
  bstack111l111111l_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡰࡧ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷࠬἮ")
  bstack1111lllllll_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸ࡭ࡻࡢ࠻ࡵࡷࡳࡵ࠭Ἧ")
  bstack1l1l1ll1l11_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡹࡴࡢࡴࡷࠫἰ")
  bstack111l11lll1l_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨἱ")
  bstack111l11l1ll1_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡤࡪࡨࡧࡰ࠳ࡵࡱࡦࡤࡸࡪ࠭ἲ")
  bstack1l1llllll11_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠧἳ")
  bstack1l1lll1ll11_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡹࡴࡢࡴࡷࡦ࡮ࡴࡡࡳࡻࠪἴ")
  bstack1l1lll1111l_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡣࡰࡰࡱࡩࡨࡺࠧἵ")
  bstack1l1ll111l11_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡴࡶࡲࡴࠬἶ")
  bstack1l1ll1l1111_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡷࡥࡷࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰࠪἷ")
  bstack1l1l1l1111l_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡳࡳࡴࡥࡤࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭Ἰ")
  bstack111l1111111_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠧἹ")
  bstack111l11ll1l1_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡥࡐࡨࡥࡷ࡫ࡳࡵࡊࡸࡦࠬἺ")
  bstack11ll11ll11l_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡍࡳ࡯ࡴࠨἻ")
  bstack11ll1l11l1l_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡳࡶࠪἼ")
  bstack1l11lll1ll1_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡃࡰࡰࡩ࡭࡬࠭Ἵ")
  bstack111l11l11l1_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡄࡱࡱࡪ࡮࡭ࠧἾ")
  bstack1l11l11l111_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࡭ࡘ࡫࡬ࡧࡊࡨࡥࡱ࡙ࡴࡦࡲࠪἿ")
  bstack1l11l111l1l_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࡮࡙ࡥ࡭ࡨࡋࡩࡦࡲࡇࡦࡶࡕࡩࡸࡻ࡬ࡵࠩὀ")
  bstack1l1111l1l11_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡉࡻ࡫࡮ࡵࠩὁ")
  bstack11llllll11l_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠨὂ")
  bstack1l1111l1111_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡰࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࡅࡷࡧࡱࡸࠬὃ")
  bstack111l11l1l11_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡪࡴࡱࡶࡧࡸࡩ࡙࡫ࡳࡵࡇࡹࡩࡳࡺࠧὄ")
  bstack11ll11l11l1_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡱࡳࠫὅ")
  bstack1l1llll1lll_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡲࡲࡘࡺ࡯ࡱࠩ὆")
  bstack111lllll1ll_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳ࡙ࡵࡲ࡯ࡢࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧ὇")
  bstack1l111lll11_opy_ = bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫࡮ࡥࡈࡸࡲࡳ࡫࡬ࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠧὈ")
  bstack11l111ll_opy_ = bstack1ll11_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦࡉࡹࡳࡴࡥ࡭ࡖࡨࡷࡹࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠨὉ")
  bstack1ll1llll1ll_opy_ = bstack1ll11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡱࡲ࡯ࡽࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡔࡾࡺࡥࡴࡶࠪὊ")
  bstack1llllll111l_opy_ = bstack1ll11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳࡰࡾࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡇ࡫ࡨࡢࡸࡨࠫὋ")
  bstack1lll111lll1_opy_ = bstack1ll11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡨ࡫ࡳࡴࡃࡵ࡫ࡸࡖࡹࡵࡧࡶࡸࠬὌ")
  bstack1lll111l1ll_opy_ = bstack1ll11_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡽࡹ࡫ࡳࡵࡉࡨࡸ࡙ࡵࡴࡢ࡮ࡗࡩࡸࡺࡳࠨὍ")
class STAGE(Enum):
  bstack1l111l1l_opy_ = bstack1ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬ὎")
  END = bstack1ll11_opy_ (u"ࠧࡦࡰࡧࠫ὏")
  bstack11111llll_opy_ = bstack1ll11_opy_ (u"ࠨࡵ࡬ࡲ࡬ࡲࡥࠨὐ")
bstack11111l1lll_opy_ = {
  bstack1ll11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࠩὑ"): bstack1ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪὒ"),
  bstack1ll11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨὓ"): bstack1ll11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧὔ"),
  bstack1ll11_opy_ (u"࠭ࡂࡆࡊࡄ࡚ࡊ࠭ὕ"): bstack1ll11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧὖ")
}
PLAYWRIGHT_HUB_URL = bstack1ll11_opy_ (u"ࠣࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠥὗ")
bstack1111l111l1_opy_ = {bstack1ll11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ὘"), bstack1ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮࡫ࡸࡱࠬὙ"), bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠮ࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠪ὚")}
MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION = 98
bstack1l1l11l1111_opy_ = 100
bstack1111l111l1_opy_ = (bstack1ll11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬὛ"), bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠰ࡧ࡭ࡸ࡯࡮࡫ࡸࡱࠬ὜"), bstack1ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩὝ"))
bstack1lll1111111_opy_ = {
  bstack1ll11_opy_ (u"ࠨࡴࡨࡶࡺࡴࠧ὞"): bstack1ll11_opy_ (u"ࠩ࠰࠱ࡷ࡫ࡲࡶࡰࡶࠫὟ"),
  bstack1ll11_opy_ (u"ࠪࡨࡪࡲࡡࡺࠩὠ"): bstack1ll11_opy_ (u"ࠫ࠲࠳ࡲࡦࡴࡸࡲࡸ࠳ࡤࡦ࡮ࡤࡽࠬὡ"),
  bstack1ll11_opy_ (u"ࠬࡸࡥࡳࡷࡱ࠱ࡩ࡫࡬ࡢࡻࠪὢ"): 0
}
bstack111l11ll1ll_opy_ = bstack1ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨὣ")
bstack1111lllll1l_opy_ = bstack1ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡷࡳࡰࡴࡧࡤ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦὤ")
bstack1ll1l1lll_opy_ = bstack1ll11_opy_ (u"ࠣࡖࡈࡗ࡙ࠦࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠢࡄࡒࡉࠦࡁࡏࡃࡏ࡝࡙ࡏࡃࡔࠤὥ")