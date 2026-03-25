# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
import re
from enum import Enum
bstack1l111l1lll_opy_ = {
  bstack1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᯓ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩᯔ"),
  bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᯕ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪᯖ"),
  bstack1l1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᯗ"): bstack1l1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᯘ"),
  bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᯙ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫᯚ"),
  bstack1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᯛ"): bstack1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧᯜ"),
  bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᯝ"): bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᯞ"),
  bstack1l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᯟ"): bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᯠ"),
  bstack1l1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᯡ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪᯢ"),
  bstack1l1_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫᯣ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧᯤ"),
  bstack1l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᯥ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ᯦࠭"),
  bstack1l1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᯧ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᯨ"),
  bstack1l1_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫᯩ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫᯪ"),
  bstack1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᯫ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᯬ"),
  bstack1l1_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᯭ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᯮ"),
  bstack1l1_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᯯ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᯰ"),
  bstack1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨᯱ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨ᯲"),
  bstack1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰ᯳ࠪ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᯴"),
  bstack1l1_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩ᯵"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩ᯶"),
  bstack1l1_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᯷"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᯸"),
  bstack1l1_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧ᯹"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧ᯺"),
  bstack1l1_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫ᯻"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫ᯼"),
  bstack1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭᯽"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭᯾"),
  bstack1l1_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬ᯿"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬᰀ"),
  bstack1l1_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩᰁ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩᰂ"),
  bstack1l1_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫᰃ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫᰄ"),
  bstack1l1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨᰅ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨᰆ"),
  bstack1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᰇ"): bstack1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᰈ"),
  bstack1l1_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭ᰉ"): bstack1l1_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨᰊ"),
  bstack1l1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᰋ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᰌ"),
  bstack1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ᰍ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ᰎ"),
  bstack1l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩᰏ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩᰐ"),
  bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩᰑ"): bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬᰒ"),
  bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᰓ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᰔ"),
  bstack1l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᰕ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧᰖ"),
  bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᰗ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᰘ"),
  bstack1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ᰙ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ᰚ"),
  bstack1l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩᰛ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩᰜ"),
  bstack1l1_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬᰝ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬᰞ"),
  bstack1l1_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨᰟ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨᰠ"),
  bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᰡ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᰢ"),
  bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᰣ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᰤ")
}
bstack111l1111l11_opy_ = [
  bstack1l1_opy_ (u"ࠩࡲࡷࠬᰥ"),
  bstack1l1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᰦ"),
  bstack1l1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᰧ"),
  bstack1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᰨ"),
  bstack1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᰩ"),
  bstack1l1_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫᰪ"),
  bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᰫ"),
]
bstack1111l1ll11_opy_ = {
  bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᰬ"): [bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᰭ"), bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡐࡄࡑࡊ࠭ᰮ")],
  bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᰯ"): bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᰰ"),
  bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᰱ"): bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠫᰲ"),
  bstack1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᰳ"): bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠨᰴ"),
  bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᰵ"): bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᰶ"),
  bstack1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ᰷࠭"): bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡔࡡࡓࡉࡗࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨ᰸"),
  bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᰹"): bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧ᰺"),
  bstack1l1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧ᰻"): bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨ᰼"),
  bstack1l1_opy_ (u"ࠬࡧࡰࡱࠩ᰽"): [bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࡡࡌࡈࠬ᰾"), bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࠪ᰿")],
  bstack1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ᱀"): bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡒࡏࡈࡎࡈ࡚ࡊࡒࠧ᱁"),
  bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᱂"): bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᱃"),
  bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᱄"): [bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠪ᱅"), bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧ᱆")],
  bstack1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᱇"): bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡘࡖࡇࡕࡓࡄࡃࡏࡉࠬ᱈"),
  bstack1l1_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡊࡔࡖࠨ᱉"): bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡓࡗࡉࡈࡆࡕࡗࡖࡆ࡚ࡉࡐࡐࡢࡗࡒࡇࡒࡕࡡࡖࡉࡑࡋࡃࡕࡋࡒࡒࡤࡌࡅࡂࡖࡘࡖࡊࡥࡂࡓࡃࡑࡇࡍࡋࡓࠨ᱊")
}
bstack1l1l1ll1ll_opy_ = {
  bstack1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ᱋"): [bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡢࡲࡦࡳࡥࠨ᱌"), bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡒࡦࡳࡥࠨᱍ")],
  bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᱎ"): [bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡠ࡭ࡨࡽࠬᱏ"), bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᱐")],
  bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᱑"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᱒"),
  bstack1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᱓"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᱔"),
  bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᱕"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᱖"),
  bstack1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᱗"): [bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡵࡶࠧ᱘"), bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ᱙")],
  bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᱚ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬᱛ"),
  bstack1l1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᱜ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᱝ"),
  bstack1l1_opy_ (u"ࠪࡥࡵࡶࠧᱞ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࠧᱟ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᱠ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᱡ"),
  bstack1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᱢ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᱣ"),
  bstack1l1_opy_ (u"ࠤࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡇࡑࡏࠢᱤ"): bstack1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࠣᱥ"),
}
bstack1ll1ll111_opy_ = {
  bstack1l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᱦ"): bstack1l1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᱧ"),
  bstack1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᱨ"): [bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᱩ"), bstack1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᱪ")],
  bstack1l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᱫ"): bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᱬ"),
  bstack1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᱭ"): bstack1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᱮ"),
  bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᱯ"): [bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᱰ"), bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᱱ")],
  bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᱲ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᱳ"),
  bstack1l1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᱴ"): bstack1l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪᱵ"),
  bstack1l1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᱶ"): [bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᱷ"), bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᱸ")],
  bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᱹ"): [bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫᱺ"), bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫᱻ")]
}
bstack111l1l1l_opy_ = [
  bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᱼ"),
  bstack1l1_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᱽ"),
  bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭᱾"),
  bstack1l1_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨ᱿"),
  bstack1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫᲀ"),
  bstack1l1_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨᲁ"),
  bstack1l1_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧᲂ"),
  bstack1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᲃ"),
  bstack1l1_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᲄ"),
  bstack1l1_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᲅ"),
  bstack1l1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᲆ"),
  bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᲇ"),
]
bstack11lllll1ll_opy_ = [
  bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᲈ"),
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᲉ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᲊ"),
  bstack1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭᲋"),
  bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᲌"),
  bstack1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ᲍"),
  bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᲎"),
  bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᲏"),
  bstack1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᲐ"),
  bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᲑ"),
  bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᲒ"),
  bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧᲓ"),
  bstack1l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᲔ"),
  bstack1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡖࡤ࡫ࠬᲕ"),
  bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᲖ"),
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Თ"),
  bstack1l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᲘ"),
  bstack1l1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠵ࠬᲙ"),
  bstack1l1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠷࠭Ლ"),
  bstack1l1_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠹ࠧᲛ"),
  bstack1l1_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠴ࠨᲜ"),
  bstack1l1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠶ࠩᲝ"),
  bstack1l1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠸ࠪᲞ"),
  bstack1l1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠺ࠫᲟ"),
  bstack1l1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠼ࠬᲠ"),
  bstack1l1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠾࠭Ს"),
  bstack1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᲢ"),
  bstack1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᲣ"),
  bstack1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭Ფ"),
  bstack1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭Ქ"),
  bstack1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᲦ"),
  bstack1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᲧ"),
  bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫᲨ"),
  bstack1l1_opy_ (u"ࠨࡪࡸࡦࡗ࡫ࡧࡪࡱࡱࠫᲩ")
]
bstack111l111l1l1_opy_ = [
  bstack1l1_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧᲪ"),
  bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᲫ"),
  bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᲬ"),
  bstack1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᲭ"),
  bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡔࡷ࡯࡯ࡳ࡫ࡷࡽࠬᲮ"),
  bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᲯ"),
  bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡢࡩࠪᲰ"),
  bstack1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᲱ"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᲲ"),
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᲳ"),
  bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ჴ"),
  bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᲵ"),
  bstack1l1_opy_ (u"ࠧࡰࡵࠪᲶ"),
  bstack1l1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᲷ"),
  bstack1l1_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨᲸ"),
  bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᲹ"),
  bstack1l1_opy_ (u"ࠫࡷ࡫ࡧࡪࡱࡱࠫᲺ"),
  bstack1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧ᲻"),
  bstack1l1_opy_ (u"࠭࡭ࡢࡥ࡫࡭ࡳ࡫ࠧ᲼"),
  bstack1l1_opy_ (u"ࠧࡳࡧࡶࡳࡱࡻࡴࡪࡱࡱࠫᲽ"),
  bstack1l1_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭Ჾ"),
  bstack1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭Ჿ"),
  bstack1l1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩ᳀"),
  bstack1l1_opy_ (u"ࠫࡳࡵࡐࡢࡩࡨࡐࡴࡧࡤࡕ࡫ࡰࡩࡴࡻࡴࠨ᳁"),
  bstack1l1_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭᳂"),
  bstack1l1_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬ᳃"),
  bstack1l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ᳄"),
  bstack1l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩ᳅"),
  bstack1l1_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭᳆"),
  bstack1l1_opy_ (u"ࠪࡲࡴࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠧ᳇"),
  bstack1l1_opy_ (u"ࠫࡨ࡮ࡥࡤ࡭ࡘࡖࡑ࠭᳈"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᳉"),
  bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡉ࡯ࡰ࡭࡬ࡩࡸ࠭᳊"),
  bstack1l1_opy_ (u"ࠧࡤࡣࡳࡸࡺࡸࡥࡄࡴࡤࡷ࡭࠭᳋"),
  bstack1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ᳌"),
  bstack1l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᳍"),
  bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡖࡦࡴࡶ࡭ࡴࡴࠧ᳎"),
  bstack1l1_opy_ (u"ࠫࡳࡵࡂ࡭ࡣࡱ࡯ࡕࡵ࡬࡭࡫ࡱ࡫ࠬ᳏"),
  bstack1l1_opy_ (u"ࠬࡳࡡࡴ࡭ࡖࡩࡳࡪࡋࡦࡻࡶࠫ᳐"),
  bstack1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡒ࡯ࡨࡵࠪ᳑"),
  bstack1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡉࡥࠩ᳒"),
  bstack1l1_opy_ (u"ࠨࡦࡨࡨ࡮ࡩࡡࡵࡧࡧࡈࡪࡼࡩࡤࡧࠪ᳓"),
  bstack1l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡒࡤࡶࡦࡳࡳࠨ᳔"),
  bstack1l1_opy_ (u"ࠪࡴ࡭ࡵ࡮ࡦࡐࡸࡱࡧ࡫ࡲࠨ᳕"),
  bstack1l1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴ᳖ࠩ"),
  bstack1l1_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡒࡴࡹ࡯࡯࡯ࡵ᳗ࠪ"),
  bstack1l1_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶ᳘ࠫ"),
  bstack1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉ᳙ࠧ"),
  bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬ᳚"),
  bstack1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡄ࡬ࡳࡲ࡫ࡴࡳ࡫ࡦࠫ᳛"),
  bstack1l1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࡘ࠵᳜ࠫ"),
  bstack1l1_opy_ (u"ࠫࡲ࡯ࡤࡔࡧࡶࡷ࡮ࡵ࡮ࡊࡰࡶࡸࡦࡲ࡬ࡂࡲࡳࡷ᳝ࠬ"),
  bstack1l1_opy_ (u"ࠬ࡫ࡳࡱࡴࡨࡷࡸࡵࡓࡦࡴࡹࡩࡷ᳞࠭"),
  bstack1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷ᳟ࠬ"),
  bstack1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡅࡧࡴࠬ᳠"),
  bstack1l1_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨ᳡"),
  bstack1l1_opy_ (u"ࠩࡶࡽࡳࡩࡔࡪ࡯ࡨ࡛࡮ࡺࡨࡏࡖࡓ᳢ࠫ"),
  bstack1l1_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨ᳣"),
  bstack1l1_opy_ (u"ࠫ࡬ࡶࡳࡍࡱࡦࡥࡹ࡯࡯࡯᳤ࠩ"),
  bstack1l1_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ᳥࠭"),
  bstack1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ᳦࠭"),
  bstack1l1_opy_ (u"ࠧࡧࡱࡵࡧࡪࡉࡨࡢࡰࡪࡩࡏࡧࡲࠨ᳧"),
  bstack1l1_opy_ (u"ࠨࡺࡰࡷࡏࡧࡲࠨ᳨"),
  bstack1l1_opy_ (u"ࠩࡻࡱࡽࡐࡡࡳࠩᳩ"),
  bstack1l1_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩᳪ"),
  bstack1l1_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫᳫ"),
  bstack1l1_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭ᳬ"),
  bstack1l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴ᳭ࠩ"),
  bstack1l1_opy_ (u"ࠧࡢࡲࡳ࡚ࡪࡸࡳࡪࡱࡱࠫᳮ"),
  bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧᳯ"),
  bstack1l1_opy_ (u"ࠩࡵࡩࡸ࡯ࡧ࡯ࡃࡳࡴࠬᳰ"),
  bstack1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳࡹࠧᳱ"),
  bstack1l1_opy_ (u"ࠫࡨࡧ࡮ࡢࡴࡼࠫᳲ"),
  bstack1l1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ᳳ"),
  bstack1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭᳴"),
  bstack1l1_opy_ (u"ࠧࡪࡧࠪᳵ"),
  bstack1l1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ᳶ"),
  bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ᳷"),
  bstack1l1_opy_ (u"ࠪࡵࡺ࡫ࡵࡦࠩ᳸"),
  bstack1l1_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡱࡥࡱ࠭᳹"),
  bstack1l1_opy_ (u"ࠬࡧࡰࡱࡕࡷࡳࡷ࡫ࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳ࠭ᳺ"),
  bstack1l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡉࡡ࡮ࡧࡵࡥࡎࡳࡡࡨࡧࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬ᳻"),
  bstack1l1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡊࡾࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪ᳼"),
  bstack1l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡏ࡮ࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫ᳽"),
  bstack1l1_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭᳾"),
  bstack1l1_opy_ (u"ࠪࡶࡪࡹࡥࡳࡸࡨࡈࡪࡼࡩࡤࡧࠪ᳿"),
  bstack1l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᴀ"),
  bstack1l1_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧᴁ"),
  bstack1l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡡࡴࡵࡦࡳࡩ࡫ࠧᴂ"),
  bstack1l1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡉࡰࡵࡇࡩࡻ࡯ࡣࡦࡕࡨࡸࡹ࡯࡮ࡨࡵࠪᴃ"),
  bstack1l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡷࡧ࡭ࡴࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨᴄ"),
  bstack1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡳࡴࡱ࡫ࡐࡢࡻࠪᴅ"),
  bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᴆ"),
  bstack1l1_opy_ (u"ࠫࡼࡪࡩࡰࡕࡨࡶࡻ࡯ࡣࡦࠩᴇ"),
  bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᴈ"),
  bstack1l1_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡃࡳࡱࡶࡷࡘ࡯ࡴࡦࡖࡵࡥࡨࡱࡩ࡯ࡩࠪᴉ"),
  bstack1l1_opy_ (u"ࠧࡩ࡫ࡪ࡬ࡈࡵ࡮ࡵࡴࡤࡷࡹ࠭ᴊ"),
  bstack1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡑࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࡷࠬᴋ"),
  bstack1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬᴌ"),
  bstack1l1_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧᴍ"),
  bstack1l1_opy_ (u"ࠫࡷ࡫࡭ࡰࡸࡨࡍࡔ࡙ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࡐࡴࡩࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩᴎ"),
  bstack1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᴏ"),
  bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᴐ"),
  bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᴑ"),
  bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᴒ"),
  bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᴓ"),
  bstack1l1_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ᴔ"),
  bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪᴕ"),
  bstack1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧᴖ"),
  bstack1l1_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩᴗ")
]
bstack1l11l11l11_opy_ = {
  bstack1l1_opy_ (u"ࠧࡷࠩᴘ"): bstack1l1_opy_ (u"ࠨࡸࠪᴙ"),
  bstack1l1_opy_ (u"ࠩࡩࠫᴚ"): bstack1l1_opy_ (u"ࠪࡪࠬᴛ"),
  bstack1l1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪᴜ"): bstack1l1_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫᴝ"),
  bstack1l1_opy_ (u"࠭࡯࡯࡮ࡼࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᴞ"): bstack1l1_opy_ (u"ࠧࡰࡰ࡯ࡽࡆࡻࡴࡰ࡯ࡤࡸࡪ࠭ᴟ"),
  bstack1l1_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬᴠ"): bstack1l1_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭ᴡ"),
  bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭ᴢ"): bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᴣ"),
  bstack1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨᴤ"): bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩᴥ"),
  bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᴦ"): bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᴧ"),
  bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᴨ"): bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᴩ"),
  bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬᴪ"): bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡊࡲࡷࡹ࠭ᴫ"),
  bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧᴬ"): bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨᴭ"),
  bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᴮ"): bstack1l1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫᴯ"),
  bstack1l1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᴰ"): bstack1l1_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᴱ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᴲ"): bstack1l1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨᴳ"),
  bstack1l1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᴴ"): bstack1l1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪᴵ"),
  bstack1l1_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ᴶ"): bstack1l1_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧᴷ"),
  bstack1l1_opy_ (u"ࠫࡵࡧࡣࡧ࡫࡯ࡩࠬᴸ"): bstack1l1_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᴹ"),
  bstack1l1_opy_ (u"࠭ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᴺ"): bstack1l1_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᴻ"),
  bstack1l1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᴼ"): bstack1l1_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᴽ"),
  bstack1l1_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫᴾ"): bstack1l1_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬᴿ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᵀ"): bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᵁ"),
  bstack1l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩᵂ"): bstack1l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡳࡩࡦࡺࡥࡳࠩᵃ")
}
bstack111l1l1l1l1_opy_ = bstack1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫࡮ࡺࡨࡶࡤ࠱ࡧࡴࡳ࠯ࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫࠲ࡶࡪࡲࡥࡢࡵࡨࡷ࠴ࡲࡡࡵࡧࡶࡸ࠴ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᵄ")
bstack111l1111lll_opy_ = bstack1l1_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠲࡬ࡪࡧ࡬ࡵࡪࡦ࡬ࡪࡩ࡫ࠣᵅ")
bstack1ll11lll1_opy_ = bstack1l1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡫ࡤࡴ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡹࡥ࡯ࡦࡢࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢᵆ")
HTTPS_HUB = bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ᵇ")
bstack1l1l11ll11_opy_ = bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩᵈ")
bstack111lllll11_opy_ = bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠸࠹࠺࠴࠰ࡹࡧ࠳࡭ࡻࡢࠨᵉ")
bstack11111l1lll_opy_ = bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬᵊ")
bstack1ll11lll1l_opy_ = {
  bstack1l1_opy_ (u"ࠩࡧࡩ࡫ࡧࡵ࡭ࡶࠪᵋ"): bstack1l1_opy_ (u"ࠪ࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᵌ"),
  bstack1l1_opy_ (u"ࠫࡺࡹ࠭ࡦࡣࡶࡸࠬᵍ"): bstack1l1_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡸࡷࡪ࠳࡯࡯࡮ࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᵎ"),
  bstack1l1_opy_ (u"࠭ࡵࡴࠩᵏ"): bstack1l1_opy_ (u"ࠧࡩࡷࡥ࠱ࡺࡹ࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᵐ"),
  bstack1l1_opy_ (u"ࠨࡧࡸࠫᵑ"): bstack1l1_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡥࡶ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᵒ"),
  bstack1l1_opy_ (u"ࠪ࡭ࡳ࠭ᵓ"): bstack1l1_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡣࡳࡷ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᵔ"),
  bstack1l1_opy_ (u"ࠬࡧࡵࠨᵕ"): bstack1l1_opy_ (u"࠭ࡨࡶࡤ࠰ࡥࡵࡹࡥ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᵖ")
}
bstack111l11lll11_opy_ = {
  bstack1l1_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩᵗ"): 50,
  bstack1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᵘ"): 40,
  bstack1l1_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᵙ"): 30,
  bstack1l1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᵚ"): 20,
  bstack1l1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᵛ"): 10
}
bstack1l1l1l1ll1_opy_ = bstack111l11lll11_opy_[bstack1l1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᵜ")]
bstack1l11ll11_opy_ = bstack1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩ࠯ࠨᵝ")
bstack11l1l1lll_opy_ = bstack1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᵞ")
bstack1l11l1lll1_opy_ = bstack1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᵟ")
bstack1111ll1l_opy_ = bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᵠ")
bstack11llllll1l_opy_ = bstack1l1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡦࡴࡤࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡴࡦࡩ࡫ࡢࡩࡨࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡠࠨᵡ")
bstack1llll1111l_opy_ = {
  bstack1l1_opy_ (u"ࠫࡘࡊࡋ࠮ࡉࡈࡒ࠲࠶࠰࠶ࠩᵢ"): bstack1l1_opy_ (u"ࠬ࠰ࠪࠫࠢ࡞ࡗࡉࡑ࠭ࡈࡇࡑ࠱࠵࠶࠵࡞ࠢࡣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࡥࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥ࡯࡮ࠡࡻࡲࡹࡷࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠲࡚ࠥࡨࡪࡵࠣࡱࡦࡿࠠࡤࡣࡸࡷࡪࠦࡣࡰࡰࡩࡰ࡮ࡩࡴࡴࠢࡺ࡭ࡹ࡮ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࠠࡪࡶࠣࡹࡸ࡯࡮ࡨ࠼ࠣࡴ࡮ࡶࠠࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࠥ࠰ࠪࠫࠩᵣ")
}
bstack111l1l1l1ll_opy_ = [bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᵤ"), bstack1l1_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᵥ")]
bstack111l11ll111_opy_ = [bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᵦ"), bstack1l1_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᵧ")]
bstack11111llll_opy_ = re.compile(bstack1l1_opy_ (u"ࠪࡢࡠࡢ࡜ࡸ࠯ࡠ࠯࠿࠴ࠪࠥࠩᵨ"))
bstack11l1ll1l11_opy_ = [
  bstack1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡏࡣࡰࡩࠬᵩ"),
  bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᵪ"),
  bstack1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᵫ"),
  bstack1l1_opy_ (u"ࠧ࡯ࡧࡺࡇࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࠫᵬ"),
  bstack1l1_opy_ (u"ࠨࡣࡳࡴࠬᵭ"),
  bstack1l1_opy_ (u"ࠩࡸࡨ࡮ࡪࠧᵮ"),
  bstack1l1_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬᵯ"),
  bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࠫᵰ"),
  bstack1l1_opy_ (u"ࠬࡵࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪᵱ"),
  bstack1l1_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࠫᵲ"),
  bstack1l1_opy_ (u"ࠧ࡯ࡱࡕࡩࡸ࡫ࡴࠨᵳ"), bstack1l1_opy_ (u"ࠨࡨࡸࡰࡱࡘࡥࡴࡧࡷࠫᵴ"),
  bstack1l1_opy_ (u"ࠩࡦࡰࡪࡧࡲࡔࡻࡶࡸࡪࡳࡆࡪ࡮ࡨࡷࠬᵵ"),
  bstack1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡖ࡬ࡱ࡮ࡴࡧࡴࠩᵶ"),
  bstack1l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࡍࡱࡪ࡫࡮ࡴࡧࠨᵷ"),
  bstack1l1_opy_ (u"ࠬࡵࡴࡩࡧࡵࡅࡵࡶࡳࠨᵸ"),
  bstack1l1_opy_ (u"࠭ࡰࡳ࡫ࡱࡸࡕࡧࡧࡦࡕࡲࡹࡷࡩࡥࡐࡰࡉ࡭ࡳࡪࡆࡢ࡫࡯ࡹࡷ࡫ࠧᵹ"),
  bstack1l1_opy_ (u"ࠧࡢࡲࡳࡅࡨࡺࡩࡷ࡫ࡷࡽࠬᵺ"), bstack1l1_opy_ (u"ࠨࡣࡳࡴࡕࡧࡣ࡬ࡣࡪࡩࠬᵻ"), bstack1l1_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡄࡧࡹ࡯ࡶࡪࡶࡼࠫᵼ"), bstack1l1_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡔࡦࡩ࡫ࡢࡩࡨࠫᵽ"), bstack1l1_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭ᵾ"),
  bstack1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪᵿ"),
  bstack1l1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙࡫ࡳࡵࡒࡤࡧࡰࡧࡧࡦࡵࠪᶀ"),
  bstack1l1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࠩᶁ"), bstack1l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡅࡲࡺࡪࡸࡡࡨࡧࡈࡲࡩࡏ࡮ࡵࡧࡱࡸࠬᶂ"),
  bstack1l1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧᶃ"),
  bstack1l1_opy_ (u"ࠪࡥࡩࡨࡐࡰࡴࡷࠫᶄ"),
  bstack1l1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡗࡴࡩ࡫ࡦࡶࠪᶅ"),
  bstack1l1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᶆ"),
  bstack1l1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡶ࡫ࠫᶇ"),
  bstack1l1_opy_ (u"ࠧࡢࡸࡧࠫᶈ"), bstack1l1_opy_ (u"ࠨࡣࡹࡨࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫᶉ"), bstack1l1_opy_ (u"ࠩࡤࡺࡩࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫᶊ"), bstack1l1_opy_ (u"ࠪࡥࡻࡪࡁࡳࡩࡶࠫᶋ"),
  bstack1l1_opy_ (u"ࠫࡺࡹࡥࡌࡧࡼࡷࡹࡵࡲࡦࠩᶌ"), bstack1l1_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡶ࡫ࠫᶍ"), bstack1l1_opy_ (u"࠭࡫ࡦࡻࡶࡸࡴࡸࡥࡑࡣࡶࡷࡼࡵࡲࡥࠩᶎ"),
  bstack1l1_opy_ (u"ࠧ࡬ࡧࡼࡅࡱ࡯ࡡࡴࠩᶏ"), bstack1l1_opy_ (u"ࠨ࡭ࡨࡽࡕࡧࡳࡴࡹࡲࡶࡩ࠭ᶐ"),
  bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࠫᶑ"), bstack1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡃࡵ࡫ࡸ࠭ᶒ"), bstack1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪࡊࡩࡳࠩᶓ"), bstack1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡇ࡭ࡸ࡯࡮ࡧࡐࡥࡵࡶࡩ࡯ࡩࡉ࡭ࡱ࡫ࠧᶔ"), bstack1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶ࡚ࡹࡥࡔࡻࡶࡸࡪࡳࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪᶕ"),
  bstack1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࠪᶖ"), bstack1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡐࡰࡴࡷࡷࠬᶗ"),
  bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡅ࡫ࡶࡥࡧࡲࡥࡃࡷ࡬ࡰࡩࡉࡨࡦࡥ࡮ࠫᶘ"),
  bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࡕ࡫ࡰࡩࡴࡻࡴࠨᶙ"),
  bstack1l1_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡅࡨࡺࡩࡰࡰࠪᶚ"), bstack1l1_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡈࡧࡴࡦࡩࡲࡶࡾ࠭ᶛ"), bstack1l1_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡌ࡬ࡢࡩࡶࠫᶜ"), bstack1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡡ࡭ࡋࡱࡸࡪࡴࡴࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᶝ"),
  bstack1l1_opy_ (u"ࠨࡦࡲࡲࡹ࡙ࡴࡰࡲࡄࡴࡵࡕ࡮ࡓࡧࡶࡩࡹ࠭ᶞ"),
  bstack1l1_opy_ (u"ࠩࡸࡲ࡮ࡩ࡯ࡥࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫᶟ"), bstack1l1_opy_ (u"ࠪࡶࡪࡹࡥࡵࡍࡨࡽࡧࡵࡡࡳࡦࠪᶠ"),
  bstack1l1_opy_ (u"ࠫࡳࡵࡓࡪࡩࡱࠫᶡ"),
  bstack1l1_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩ࡚ࡴࡩ࡮ࡲࡲࡶࡹࡧ࡮ࡵࡘ࡬ࡩࡼࡹࠧᶢ"),
  bstack1l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯ࡦࡵࡳ࡮ࡪࡗࡢࡶࡦ࡬ࡪࡸࡳࠨᶣ"),
  bstack1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᶤ"),
  bstack1l1_opy_ (u"ࠨࡴࡨࡧࡷ࡫ࡡࡵࡧࡆ࡬ࡷࡵ࡭ࡦࡆࡵ࡭ࡻ࡫ࡲࡔࡧࡶࡷ࡮ࡵ࡮ࡴࠩᶥ"),
  bstack1l1_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᶦ"),
  bstack1l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡐࡢࡶ࡫ࠫᶧ"),
  bstack1l1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡘࡶࡥࡦࡦࠪᶨ"),
  bstack1l1_opy_ (u"ࠬ࡭ࡰࡴࡇࡱࡥࡧࡲࡥࡥࠩᶩ"),
  bstack1l1_opy_ (u"࠭ࡩࡴࡊࡨࡥࡩࡲࡥࡴࡵࠪᶪ"),
  bstack1l1_opy_ (u"ࠧࡢࡦࡥࡉࡽ࡫ࡣࡕ࡫ࡰࡩࡴࡻࡴࠨᶫ"),
  bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࡔࡥࡵ࡭ࡵࡺࠧᶬ"),
  bstack1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡄࡦࡸ࡬ࡧࡪࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᶭ"),
  bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡈࡴࡤࡲࡹࡖࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠪᶮ"),
  bstack1l1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡓࡧࡴࡶࡴࡤࡰࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᶯ"),
  bstack1l1_opy_ (u"ࠬࡹࡹࡴࡶࡨࡱࡕࡵࡲࡵࠩᶰ"),
  bstack1l1_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡇࡤࡣࡊࡲࡷࡹ࠭ᶱ"),
  bstack1l1_opy_ (u"ࠧࡴ࡭࡬ࡴ࡚ࡴ࡬ࡰࡥ࡮ࠫᶲ"), bstack1l1_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡕࡻࡳࡩࠬᶳ"), bstack1l1_opy_ (u"ࠩࡸࡲࡱࡵࡣ࡬ࡍࡨࡽࠬᶴ"),
  bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡍࡣࡸࡲࡨ࡮ࠧᶵ"),
  bstack1l1_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡨࡧࡴࡄࡣࡳࡸࡺࡸࡥࠨᶶ"),
  bstack1l1_opy_ (u"ࠬࡻ࡮ࡪࡰࡶࡸࡦࡲ࡬ࡐࡶ࡫ࡩࡷࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧᶷ"),
  bstack1l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡗࡪࡰࡧࡳࡼࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࠨᶸ"),
  bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚࡯ࡰ࡮ࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᶹ"),
  bstack1l1_opy_ (u"ࠨࡧࡱࡪࡴࡸࡣࡦࡃࡳࡴࡎࡴࡳࡵࡣ࡯ࡰࠬᶺ"),
  bstack1l1_opy_ (u"ࠩࡨࡲࡸࡻࡲࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡵࡋࡥࡻ࡫ࡐࡢࡩࡨࡷࠬᶻ"), bstack1l1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡈࡪࡼࡴࡰࡱ࡯ࡷࡕࡵࡲࡵࠩᶼ"), bstack1l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨ࡛ࡪࡨࡶࡪࡧࡺࡈࡪࡺࡡࡪ࡮ࡶࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠧᶽ"),
  bstack1l1_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡶࡰࡴࡅࡤࡧ࡭࡫ࡌࡪ࡯࡬ࡸࠬᶾ"),
  bstack1l1_opy_ (u"࠭ࡣࡢ࡮ࡨࡲࡩࡧࡲࡇࡱࡵࡱࡦࡺࠧᶿ"),
  bstack1l1_opy_ (u"ࠧࡣࡷࡱࡨࡱ࡫ࡉࡥࠩ᷀"),
  bstack1l1_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨ᷁"),
  bstack1l1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡊࡴࡡࡣ࡮ࡨࡨ᷂ࠬ"), bstack1l1_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࡘ࡫ࡲࡷ࡫ࡦࡩࡸࡇࡵࡵࡪࡲࡶ࡮ࢀࡥࡥࠩ᷃"),
  bstack1l1_opy_ (u"ࠫࡦࡻࡴࡰࡃࡦࡧࡪࡶࡴࡂ࡮ࡨࡶࡹࡹࠧ᷄"), bstack1l1_opy_ (u"ࠬࡧࡵࡵࡱࡇ࡭ࡸࡳࡩࡴࡵࡄࡰࡪࡸࡴࡴࠩ᷅"),
  bstack1l1_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡵࡏ࡭ࡧ࠭᷆"),
  bstack1l1_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡗࡥࡵ࠭᷇"),
  bstack1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡰ࡬ࡸ࡮ࡧ࡬ࡖࡴ࡯ࠫ᷈"), bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡃ࡯ࡰࡴࡽࡐࡰࡲࡸࡴࡸ࠭᷉"), bstack1l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌ࡫ࡳࡵࡲࡦࡈࡵࡥࡺࡪࡗࡢࡴࡱ࡭ࡳ࡭᷊ࠧ"), bstack1l1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵ࡫࡮ࡍ࡫ࡱ࡯ࡸࡏ࡮ࡃࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧࠫ᷋"),
  bstack1l1_opy_ (u"ࠬࡱࡥࡦࡲࡎࡩࡾࡉࡨࡢ࡫ࡱࡷࠬ᷌"),
  bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࢀࡡࡣ࡮ࡨࡗࡹࡸࡩ࡯ࡩࡶࡈ࡮ࡸࠧ᷍"),
  bstack1l1_opy_ (u"ࠧࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡹࡲ࡫࡮ࡵࡵ᷎ࠪ"),
  bstack1l1_opy_ (u"ࠨ࡫ࡱࡸࡪࡸࡋࡦࡻࡇࡩࡱࡧࡹࠨ᷏"),
  bstack1l1_opy_ (u"ࠩࡶ࡬ࡴࡽࡉࡐࡕࡏࡳ࡬᷐࠭"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡗࡹࡸࡡࡵࡧࡪࡽࠬ᷑"),
  bstack1l1_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡖࡪࡹࡰࡰࡰࡶࡩ࡙࡯࡭ࡦࡱࡸࡸࠬ᷒"), bstack1l1_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࡙ࡤ࡭ࡹ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᷓ"),
  bstack1l1_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࠩᷔ"),
  bstack1l1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡴࡻࡱࡧࡊࡾࡥࡤࡷࡷࡩࡋࡸ࡯࡮ࡊࡷࡸࡵࡹࠧᷕ"),
  bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡅࡤࡴࡹࡻࡲࡦࠩᷖ"),
  bstack1l1_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩᷗ"),
  bstack1l1_opy_ (u"ࠪࡪࡺࡲ࡬ࡄࡱࡱࡸࡪࡾࡴࡍ࡫ࡶࡸࠬᷘ"),
  bstack1l1_opy_ (u"ࠫࡼࡧࡩࡵࡈࡲࡶࡆࡶࡰࡔࡥࡵ࡭ࡵࡺࠧᷙ"),
  bstack1l1_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡉ࡯࡯ࡰࡨࡧࡹࡘࡥࡵࡴ࡬ࡩࡸ࠭ᷚ"),
  bstack1l1_opy_ (u"࠭ࡡࡱࡲࡑࡥࡲ࡫ࠧᷛ"),
  bstack1l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡔࡎࡆࡩࡷࡺࠧᷜ"),
  bstack1l1_opy_ (u"ࠨࡶࡤࡴ࡜࡯ࡴࡩࡕ࡫ࡳࡷࡺࡐࡳࡧࡶࡷࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭ᷝ"),
  bstack1l1_opy_ (u"ࠩࡶࡧࡦࡲࡥࡇࡣࡦࡸࡴࡸࠧᷞ"),
  bstack1l1_opy_ (u"ࠪࡻࡩࡧࡌࡰࡥࡤࡰࡕࡵࡲࡵࠩᷟ"),
  bstack1l1_opy_ (u"ࠫࡸ࡮࡯ࡸ࡚ࡦࡳࡩ࡫ࡌࡰࡩࠪᷠ"),
  bstack1l1_opy_ (u"ࠬ࡯࡯ࡴࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡹࡸ࡫ࠧᷡ"),
  bstack1l1_opy_ (u"࠭ࡸࡤࡱࡧࡩࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠨᷢ"),
  bstack1l1_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡷࡸࡽ࡯ࡳࡦࠪᷣ"),
  bstack1l1_opy_ (u"ࠨࡷࡶࡩࡕࡸࡥࡣࡷ࡬ࡰࡹ࡝ࡄࡂࠩᷤ"),
  bstack1l1_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶ࡚ࡈࡆࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪᷥ"),
  bstack1l1_opy_ (u"ࠪࡻࡪࡨࡄࡳ࡫ࡹࡩࡷࡇࡧࡦࡰࡷ࡙ࡷࡲࠧᷦ"),
  bstack1l1_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡵࡪࠪᷧ"),
  bstack1l1_opy_ (u"ࠬࡻࡳࡦࡐࡨࡻ࡜ࡊࡁࠨᷨ"),
  bstack1l1_opy_ (u"࠭ࡷࡥࡣࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩᷩ"), bstack1l1_opy_ (u"ࠧࡸࡦࡤࡇࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࡔࡪ࡯ࡨࡳࡺࡺࠧᷪ"),
  bstack1l1_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡏࡳࡩࡌࡨࠬᷫ"), bstack1l1_opy_ (u"ࠩࡻࡧࡴࡪࡥࡔ࡫ࡪࡲ࡮ࡴࡧࡊࡦࠪᷬ"),
  bstack1l1_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧ࡛ࡉࡇࡂࡶࡰࡧࡰࡪࡏࡤࠨᷭ"),
  bstack1l1_opy_ (u"ࠫࡷ࡫ࡳࡦࡶࡒࡲࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡳࡶࡒࡲࡱࡿࠧᷮ"),
  bstack1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹࡹࠧᷯ"),
  bstack1l1_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡩࡦࡵࠪᷰ"), bstack1l1_opy_ (u"ࠧࡸࡦࡤࡗࡹࡧࡲࡵࡷࡳࡖࡪࡺࡲࡺࡋࡱࡸࡪࡸࡶࡢ࡮ࠪᷱ"),
  bstack1l1_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࡊࡤࡶࡩࡽࡡࡳࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫᷲ"),
  bstack1l1_opy_ (u"ࠩࡰࡥࡽ࡚ࡹࡱ࡫ࡱ࡫ࡋࡸࡥࡲࡷࡨࡲࡨࡿࠧᷳ"),
  bstack1l1_opy_ (u"ࠪࡷ࡮ࡳࡰ࡭ࡧࡌࡷ࡛࡯ࡳࡪࡤ࡯ࡩࡈ࡮ࡥࡤ࡭ࠪᷴ"),
  bstack1l1_opy_ (u"ࠫࡺࡹࡥࡄࡣࡵࡸ࡭ࡧࡧࡦࡕࡶࡰࠬ᷵"),
  bstack1l1_opy_ (u"ࠬࡹࡨࡰࡷ࡯ࡨ࡚ࡹࡥࡔ࡫ࡱ࡫ࡱ࡫ࡴࡰࡰࡗࡩࡸࡺࡍࡢࡰࡤ࡫ࡪࡸࠧ᷶"),
  bstack1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡎ࡝ࡄࡑ᷷ࠩ"),
  bstack1l1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼ࡚࡯ࡶࡥ࡫ࡍࡩࡋ࡮ࡳࡱ࡯ࡰ᷸ࠬ"),
  bstack1l1_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡉ࡫ࡧࡨࡪࡴࡁࡱ࡫ࡓࡳࡱ࡯ࡣࡺࡇࡵࡶࡴࡸ᷹ࠧ"),
  bstack1l1_opy_ (u"ࠩࡰࡳࡨࡱࡌࡰࡥࡤࡸ࡮ࡵ࡮ࡂࡲࡳ᷺ࠫ"),
  bstack1l1_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉࡳࡷࡳࡡࡵࠩ᷻"), bstack1l1_opy_ (u"ࠫࡱࡵࡧࡤࡣࡷࡊ࡮ࡲࡴࡦࡴࡖࡴࡪࡩࡳࠨ᷼"),
  bstack1l1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡈࡪࡲࡡࡺࡃࡧࡦ᷽ࠬ"),
  bstack1l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡉࡥࡎࡲࡧࡦࡺ࡯ࡳࡃࡸࡸࡴࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠩ᷾")
]
bstack1l1l11l11l_opy_ = bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡵࡱ࡮ࡲࡥࡩ᷿࠭")
bstack1l11lll1l1_opy_ = [bstack1l1_opy_ (u"ࠨ࠰ࡤࡴࡰ࠭Ḁ"), bstack1l1_opy_ (u"ࠩ࠱ࡥࡦࡨࠧḁ"), bstack1l1_opy_ (u"ࠪ࠲࡮ࡶࡡࠨḂ")]
bstack1ll1l1111_opy_ = [bstack1l1_opy_ (u"ࠫ࡮ࡪࠧḃ"), bstack1l1_opy_ (u"ࠬࡶࡡࡵࡪࠪḄ"), bstack1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩḅ"), bstack1l1_opy_ (u"ࠧࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩ࠭Ḇ")]
bstack11l11ll111_opy_ = {
  bstack1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨḇ"): bstack1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧḈ"),
  bstack1l1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫḉ"): bstack1l1_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩḊ"),
  bstack1l1_opy_ (u"ࠬ࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪḋ"): bstack1l1_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧḌ"),
  bstack1l1_opy_ (u"ࠧࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪḍ"): bstack1l1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧḎ"),
  bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡸ࡮ࡵ࡮ࡴࠩḏ"): bstack1l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫḐ")
}
bstack1l11111ll_opy_ = [
  bstack1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩḑ"),
  bstack1l1_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪḒ"),
  bstack1l1_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧḓ"),
  bstack1l1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭Ḕ"),
  bstack1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩḕ"),
]
bstack11ll11lll1_opy_ = bstack11lllll1ll_opy_ + bstack111l111l1l1_opy_ + bstack11l1ll1l11_opy_
bstack11llll1l1l_opy_ = [
  bstack1l1_opy_ (u"ࠩࡡࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࠪࠧḖ"),
  bstack1l1_opy_ (u"ࠪࡢࡧࡹ࠭࡭ࡱࡦࡥࡱ࠴ࡣࡰ࡯ࠧࠫḗ"),
  bstack1l1_opy_ (u"ࠫࡣ࠷࠲࠸࠰ࠪḘ"),
  bstack1l1_opy_ (u"ࠬࡤ࠱࠱࠰ࠪḙ"),
  bstack1l1_opy_ (u"࠭࡞࠲࠹࠵࠲࠶ࡡ࠶࠮࠻ࡠ࠲ࠬḚ"),
  bstack1l1_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠸࡛࠱࠯࠼ࡡ࠳࠭ḛ"),
  bstack1l1_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠳࡜࠲࠰࠵ࡢ࠴ࠧḜ"),
  bstack1l1_opy_ (u"ࠩࡡ࠵࠾࠸࠮࠲࠸࠻࠲ࠬḝ")
]
bstack111ll11111l_opy_ = bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫḞ")
bstack1111ll11_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡪࡼࡥ࡯ࡶࠪḟ")
bstack1llllll111_opy_ = [ bstack1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧḠ") ]
bstack111ll1l1ll_opy_ = [ bstack1l1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬḡ") ]
bstack11l1l11lll_opy_ = [bstack1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫḢ")]
bstack1111lll111_opy_ = [ bstack1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḣ") ]
bstack1l11llll11_opy_ = bstack1l1_opy_ (u"ࠩࡖࡈࡐ࡙ࡥࡵࡷࡳࠫḤ")
bstack1l1l11ll1_opy_ = bstack1l1_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡅࡹࡺࡥ࡮ࡲࡷࡩࡩ࠭ḥ")
bstack1l1l1lll1l_opy_ = bstack1l1_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠨḦ")
bstack11l1l1ll11_opy_ = bstack1l1_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࠫḧ")
bstack11lll1l111_opy_ = [
  bstack1l1_opy_ (u"࠭ࡅࡓࡔࡢࡊࡆࡏࡌࡆࡆࠪḨ"),
  bstack1l1_opy_ (u"ࠧࡆࡔࡕࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧḩ"),
  bstack1l1_opy_ (u"ࠨࡇࡕࡖࡤࡈࡌࡐࡅࡎࡉࡉࡥࡂ࡚ࡡࡆࡐࡎࡋࡎࡕࠩḪ"),
  bstack1l1_opy_ (u"ࠩࡈࡖࡗࡥࡎࡆࡖ࡚ࡓࡗࡑ࡟ࡄࡊࡄࡒࡌࡋࡄࠨḫ"),
  bstack1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡊ࡚࡟ࡏࡑࡗࡣࡈࡕࡎࡏࡇࡆࡘࡊࡊࠧḬ"),
  bstack1l1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡉࡌࡐࡕࡈࡈࠬḭ"),
  bstack1l1_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡕࡈࡘࠬḮ"),
  bstack1l1_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡓࡇࡉ࡙ࡘࡋࡄࠨḯ"),
  bstack1l1_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡃࡅࡓࡗ࡚ࡅࡅࠩḰ"),
  bstack1l1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩḱ"),
  bstack1l1_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪḲ"),
  bstack1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡋࡑ࡚ࡆࡒࡉࡅࠩḳ"),
  bstack1l1_opy_ (u"ࠫࡊࡘࡒࡠࡃࡇࡈࡗࡋࡓࡔࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧḴ"),
  bstack1l1_opy_ (u"ࠬࡋࡒࡓࡡࡗ࡙ࡓࡔࡅࡍࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ḵ"),
  bstack1l1_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪḶ"),
  bstack1l1_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧḷ"),
  bstack1l1_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡖࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡊࡒࡗ࡙ࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫḸ"),
  bstack1l1_opy_ (u"ࠩࡈࡖࡗࡥࡐࡓࡑ࡛࡝ࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩḹ"),
  bstack1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡔࡏࡕࡡࡕࡉࡘࡕࡌࡗࡇࡇࠫḺ"),
  bstack1l1_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡒࡆࡕࡒࡐ࡚࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪḻ"),
  bstack1l1_opy_ (u"ࠬࡋࡒࡓࡡࡐࡅࡓࡊࡁࡕࡑࡕ࡝ࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫḼ"),
]
bstack1ll1l11ll_opy_ = bstack1l1_opy_ (u"࠭࠮࠰ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡢࡴࡷ࡭࡫ࡧࡣࡵࡵ࠲ࠫḽ")
bstack111111l1_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠧࡿࠩḾ")), bstack1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨḿ"), bstack1l1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨṀ"))
bstack111lll1ll1l_opy_ = bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲ࡬ࠫṁ")
bstack111l111l1ll_opy_ = [ bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫṂ"), bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫṃ"), bstack1l1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬṄ"), bstack1l1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧṅ")]
bstack11llll1l_opy_ = [ bstack1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨṆ"), bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨṇ"), bstack1l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩṈ"), bstack1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫṉ") ]
bstack1lll11ll11_opy_ = [ bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫṊ") ]
bstack111l1l11l11_opy_ = [ bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ṋ") ]
bstack1lll11l11l_opy_ = 360
bstack111l1lll1ll_opy_ = bstack1l1_opy_ (u"ࠢࡢࡲࡳ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢṌ")
bstack111l111ll11_opy_ = bstack1l1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵࠥṍ")
bstack111l11l11ll_opy_ = bstack1l1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠧṎ")
bstack111ll11l11l_opy_ = bstack1l1_opy_ (u"ࠥࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡹ࡫ࡳࡵࡵࠣࡥࡷ࡫ࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡏࡔࠢࡹࡩࡷࡹࡩࡰࡰࠣࠩࡸࠦࡡ࡯ࡦࠣࡥࡧࡵࡶࡦࠢࡩࡳࡷࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠࡥࡧࡹ࡭ࡨ࡫ࡳ࠯ࠤṏ")
bstack111ll11ll11_opy_ = bstack1l1_opy_ (u"ࠦ࠶࠷࠮࠱ࠤṐ")
bstack1llll11lll1_opy_ = {
  bstack1l1_opy_ (u"ࠬࡖࡁࡔࡕࠪṑ"): bstack1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ṓ"),
  bstack1l1_opy_ (u"ࠧࡇࡃࡌࡐࠬṓ"): bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨṔ"),
  bstack1l1_opy_ (u"ࠩࡖࡏࡎࡖࠧṕ"): bstack1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫṖ")
}
bstack1ll11ll1l_opy_ = [
  bstack1l1_opy_ (u"ࠦ࡬࡫ࡴࠣṗ"),
  bstack1l1_opy_ (u"ࠧ࡭࡯ࡃࡣࡦ࡯ࠧṘ"),
  bstack1l1_opy_ (u"ࠨࡧࡰࡈࡲࡶࡼࡧࡲࡥࠤṙ"),
  bstack1l1_opy_ (u"ࠢࡳࡧࡩࡶࡪࡹࡨࠣṚ"),
  bstack1l1_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢṛ"),
  bstack1l1_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨṜ"),
  bstack1l1_opy_ (u"ࠥࡷࡺࡨ࡭ࡪࡶࡈࡰࡪࡳࡥ࡯ࡶࠥṝ"),
  bstack1l1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣṞ"),
  bstack1l1_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣṟ"),
  bstack1l1_opy_ (u"ࠨࡣ࡭ࡧࡤࡶࡊࡲࡥ࡮ࡧࡱࡸࠧṠ"),
  bstack1l1_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࡳࠣṡ"),
  bstack1l1_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠣṢ"),
  bstack1l1_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࡄࡷࡾࡴࡣࡔࡥࡵ࡭ࡵࡺࠢṣ"),
  bstack1l1_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤṤ"),
  bstack1l1_opy_ (u"ࠦࡶࡻࡩࡵࠤṥ"),
  bstack1l1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲ࡚࡯ࡶࡥ࡫ࡅࡨࡺࡩࡰࡰࠥṦ"),
  bstack1l1_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳࡍࡶ࡮ࡷ࡭࡙ࡵࡵࡤࡪࠥṧ"),
  bstack1l1_opy_ (u"ࠢࡴࡪࡤ࡯ࡪࠨṨ"),
  bstack1l1_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࡁࡱࡲࠥṩ")
]
bstack111l11l1lll_opy_ = [
  bstack1l1_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࠣṪ"),
  bstack1l1_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢṫ"),
  bstack1l1_opy_ (u"ࠦࡦࡻࡴࡰࠤṬ"),
  bstack1l1_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧṭ"),
  bstack1l1_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣṮ")
]
bstack1111l1ll1l_opy_ = {
  bstack1l1_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨṯ"): [bstack1l1_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢṰ")],
  bstack1l1_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨṱ"): [bstack1l1_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢṲ")],
  bstack1l1_opy_ (u"ࠦࡦࡻࡴࡰࠤṳ"): [bstack1l1_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡇ࡯ࡩࡲ࡫࡮ࡵࠤṴ"), bstack1l1_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡄࡧࡹ࡯ࡶࡦࡇ࡯ࡩࡲ࡫࡮ࡵࠤṵ"), bstack1l1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦṶ"), bstack1l1_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢṷ")],
  bstack1l1_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤṸ"): [bstack1l1_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥṹ")],
  bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨṺ"): [bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢṻ")],
}
bstack111l1l11111_opy_ = {
  bstack1l1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧṼ"): bstack1l1_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨṽ"),
  bstack1l1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧṾ"): bstack1l1_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨṿ"),
  bstack1l1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢẀ"): bstack1l1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨẁ"),
  bstack1l1_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣẂ"): bstack1l1_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࠣẃ"),
  bstack1l1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤẄ"): bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥẅ")
}
bstack1lllll1l11l_opy_ = {
  bstack1l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭Ẇ"): bstack1l1_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡖࡩࡹࡻࡰࠨẇ"),
  bstack1l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧẈ"): bstack1l1_opy_ (u"࡙ࠬࡵࡪࡶࡨࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭ẉ"),
  bstack1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫẊ"): bstack1l1_opy_ (u"ࠧࡕࡧࡶࡸ࡙ࠥࡥࡵࡷࡳࠫẋ"),
  bstack1l1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬẌ"): bstack1l1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩẍ")
}
bstack111l11llll1_opy_ = 65536
bstack111l1l1l111_opy_ = bstack1l1_opy_ (u"ࠪ࠲࠳࠴࡛ࡕࡔࡘࡒࡈࡇࡔࡆࡆࡠࠫẎ")
bstack111l11l111l_opy_ = [
      bstack1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ẏ"), bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨẐ"), bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩẑ"), bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫẒ"), bstack1l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪẓ"),
      bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬẔ"), bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ẕ"), bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬẖ"), bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ẗ"),
      bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫ࠧẘ"), bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩẙ"), bstack1l1_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫẚ")
    ]
bstack111l1111ll1_opy_= {
  bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ẛ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧẜ"),
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨẝ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩẞ"),
  bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬẟ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫẠ"),
  bstack1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨạ"): bstack1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩẢ"),
  bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ả"): bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧẤ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧấ"): bstack1l1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨẦ"),
  bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪầ"): bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫẨ"),
  bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ẩ"): bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧẪ"),
  bstack1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧẫ"): bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨẬ"),
  bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫậ"): bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬẮ"),
  bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬắ"): bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ằ"),
  bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪằ"): bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫẲ"),
  bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩẳ"): bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪẴ"),
  bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࠧẵ"): bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࡐࡲࡷ࡭ࡴࡴࡳࠨẶ"),
  bstack1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫặ"): bstack1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬẸ"),
  bstack1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨẹ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧẺ"),
  bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨẻ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩẼ"),
  bstack1l1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬẽ"): bstack1l1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭Ế"),
  bstack1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩế"): bstack1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪỀ"),
  bstack1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫề"): bstack1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬỂ"),
  bstack1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪể"): bstack1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫỄ"),
  bstack1l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫễ"): bstack1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬỆ"),
  bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫệ"): bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬỈ"),
  bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ỉ"): bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧỊ"),
  bstack1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬị"): bstack1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Ọ"),
  bstack1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧọ"): bstack1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨỎ"),
  bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩỏ"): bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪỐ"),
  bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧố"): bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨỒ")
}
bstack111l11l1ll1_opy_ = [bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩồ"), bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩỔ")]
bstack111111llll_opy_ = (bstack1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦổ"),)
bstack111l1l111ll_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠱ࡹ࠵࠴ࡻࡰࡥࡣࡷࡩࡤࡩ࡬ࡪࠩỖ")
bstack11ll11111_opy_ = bstack1l1_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠯ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠵ࡶ࠲࠱ࡪࡶ࡮ࡪࡳ࠰ࠤỗ")
bstack111ll1l1_opy_ = bstack1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩࡵ࡭ࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࠨỘ")
bstack1l1llll11l_opy_ = bstack1l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠤộ")
class EVENTS(Enum):
  bstack111l1111l1l_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭Ớ")
  bstack1l1111l11l_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮ࡨࡥࡳࡻࡰࠨớ")
  bstack1l1llllll_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡨ࡬ࡲࡦࡲࡩࡻࡧࠪỜ")
  bstack111l11ll1l1_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࡬ࡰࡩࡶࠫờ")
  bstack1l111111ll_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩỞ") #shift post bstack111l11l1l11_opy_
  bstack111ll111l_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨở") #shift post bstack111l11l1l11_opy_
  bstack111l1l11l1l_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶ࡫ࡹࡧ࠭Ỡ") #shift
  bstack111l11lllll_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧỡ") #shift
  bstack1ll1lll11l_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠾࡭ࡻࡢ࠮࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠬỢ")
  bstack1l1l111ll1l_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡳࡢࡸࡨ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷࠬợ")
  bstack11l1l11l11_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡱࡧࡵࡪࡴࡸ࡭ࡴࡥࡤࡲࠬỤ")
  bstack1l1l1ll11l_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡲ࡯ࡤࡣ࡯ࠫụ") #shift
  bstack11l11ll1l_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡥࡵࡶ࠭ࡶࡲ࡯ࡳࡦࡪࠧỦ") #shift
  bstack1l1l11lll1_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡤ࡫࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠭ủ")
  bstack11ll1l1l1l_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪỨ") #shift
  bstack11ll11ll1l_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵࠪứ") #shift
  bstack111l11l1l1l_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿࠧỪ") #shift
  bstack11llll11lll_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬừ")
  bstack1lll11l1_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡳࡵࡣࡷࡹࡸ࠭Ử") #shift
  bstack11llllll1_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡨࡶࡤ࠰ࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠧử")
  bstack111l111lll1_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡰࡺࡼ࠱ࡸ࡫ࡴࡶࡲࠪỮ") #shift
  bstack1lll1ll1l_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡶࡸࡴࠬữ")
  bstack111l11l1111_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡳ࡯ࡣࡳࡷ࡭ࡵࡴࠨỰ") # not bstack111l111llll_opy_ in python
  bstack111ll11ll_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡳࡸ࡭ࡹ࠭ự") # used in bstack111l1l111l1_opy_
  bstack11l111l11ll_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡶࡪ࠳ࡱࡶ࡫ࡷࠫỲ")
  bstack11l111l11l1_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮ࡳࡸ࡭ࡹ࠭ỳ")
  bstack1lllll11_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾࡬࡫ࡴࠨỴ") # used in bstack111l1l111l1_opy_
  bstack1l1l11l1_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿࡮࡯ࡰ࡭ࠪỵ")
  bstack11l11l1ll1l_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡧ࠰࡬ࡴࡵ࡫ࠨỶ")
  bstack11l11l1l1ll_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡱࡶࡸ࠲࡮࡯ࡰ࡭ࠪỷ")
  bstack1l1lll1l1l_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠩỸ")
  bstack1l1111ll1_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠩỹ") #
  bstack1l1111l1_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡦࡵ࡭ࡻ࡫ࡲ࠮ࡶࡤ࡯ࡪ࡙ࡣࡳࡧࡨࡲࡘ࡮࡯ࡵࠩỺ")
  bstack11ll1lll_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡥࡺࡺ࡯࠮ࡥࡤࡴࡹࡻࡲࡦࠩỻ")
  bstack1l1l1l11ll_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡦ࠯ࡷࡩࡸࡺࠧỼ")
  bstack111lll11l1_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡰࡰࡵࡷ࠱ࡹ࡫ࡳࡵࠩỽ")
  bstack1lll1l1l11_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡴࡨ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬỾ") #shift
  bstack1ll1l1llll_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧỿ") #shift
  bstack111l11ll11l_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࠭ࡤࡣࡳࡸࡺࡸࡥࠨἀ")
  bstack111l1l1l11l_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿࡯ࡤ࡭ࡧ࠰ࡸ࡮ࡳࡥࡰࡷࡷࠫἁ")
  bstack1ll11111l_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡪࡾࡩࡵ࠯࡫ࡥࡳࡪ࡬ࡦࡴࠪἂ")
  bstack1ll1111111l_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡨࡼ࡮ࡺ࠭ࡩࡣࡱࡨࡱ࡫ࡲࠨἃ")
  bstack111l111l11l_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡰࡧ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷࠬἄ")
  bstack111l11lll1l_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸ࡭ࡻࡢ࠻ࡵࡷࡳࡵ࠭ἅ")
  bstack1l1ll1l11l1_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡹࡴࡢࡴࡷࠫἆ")
  bstack111l11l11l1_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨἇ")
  bstack111l11ll1ll_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡤࡪࡨࡧࡰ࠳ࡵࡱࡦࡤࡸࡪ࠭Ἀ")
  bstack1l1ll1ll11l_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠧἉ")
  bstack1l1lllll111_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡹࡴࡢࡴࡷࡦ࡮ࡴࡡࡳࡻࠪἊ")
  bstack1l1l1l1ll1l_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡣࡰࡰࡱࡩࡨࡺࠧἋ")
  bstack1l1ll1lllll_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡴࡶࡲࡴࠬἌ")
  bstack1l1lll11111_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡷࡥࡷࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰࠪἍ")
  bstack1l1ll111lll_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡳࡳࡴࡥࡤࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭Ἆ")
  bstack111l1l11ll1_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠧἏ")
  bstack111l1l1111l_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡥࡐࡨࡥࡷ࡫ࡳࡵࡊࡸࡦࠬἐ")
  bstack11ll11ll11l_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡍࡳ࡯ࡴࠨἑ")
  bstack11ll1l11111_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡳࡶࠪἒ")
  bstack1l1l1111lll_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡃࡰࡰࡩ࡭࡬࠭ἓ")
  bstack111l111ll1l_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡄࡱࡱࡪ࡮࡭ࠧἔ")
  bstack1l11l1l1111_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࡭ࡘ࡫࡬ࡧࡊࡨࡥࡱ࡙ࡴࡦࡲࠪἕ")
  bstack1l11l1l1l1l_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࡮࡙ࡥ࡭ࡨࡋࡩࡦࡲࡇࡦࡶࡕࡩࡸࡻ࡬ࡵࠩ἖")
  bstack1l111l1l111_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡉࡻ࡫࡮ࡵࠩ἗")
  bstack1l111l111ll_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠨἘ")
  bstack1l1111l111l_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡰࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࡅࡷࡧࡱࡸࠬἙ")
  bstack111l1l11lll_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡪࡴࡱࡶࡧࡸࡩ࡙࡫ࡳࡵࡇࡹࡩࡳࡺࠧἚ")
  bstack11ll11lllll_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡱࡳࠫἛ")
  bstack1ll111ll111_opy_ = bstack1l1_opy_ (u"ࠬࡹࡤ࡬࠼ࡲࡲࡘࡺ࡯ࡱࠩἜ")
  bstack111lllll11l_opy_ = bstack1l1_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳ࡙ࡵࡲ࡯ࡢࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧἝ")
  bstack1ll1111ll1_opy_ = bstack1l1_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫࡮ࡥࡈࡸࡲࡳ࡫࡬ࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠧ἞")
  bstack11ll11111l_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦࡉࡹࡳࡴࡥ࡭ࡖࡨࡷࡹࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠨ἟")
  bstack1lll1l111ll_opy_ = bstack1l1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡱࡲ࡯ࡽࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡔࡾࡺࡥࡴࡶࠪἠ")
  bstack1lll1l111l1_opy_ = bstack1l1_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡷࡕࡿࡴࡦࡵࡷࠫἡ")
  bstack1lll1l1111l_opy_ = bstack1l1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡼࡸࡪࡹࡴࡈࡧࡷࡘࡴࡺࡡ࡭ࡖࡨࡷࡹࡹࠧἢ")
class STAGE(Enum):
  bstack11ll1ll1_opy_ = bstack1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫἣ")
  END = bstack1l1_opy_ (u"࠭ࡥ࡯ࡦࠪἤ")
  bstack1ll1llll_opy_ = bstack1l1_opy_ (u"ࠧࡴ࡫ࡱ࡫ࡱ࡫ࠧἥ")
bstack111l11l1l1_opy_ = {
  bstack1l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࠨἦ"): bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩἧ"),
  bstack1l1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧἨ"): bstack1l1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭Ἡ")
}
PLAYWRIGHT_HUB_URL = bstack1l1_opy_ (u"ࠧࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠢἪ")
bstack1lllll1l1l_opy_ = {bstack1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭Ἣ"), bstack1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩἬ"), bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩࡨࡳࡱࡰ࡭ࡺࡳࠧἭ")}
MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION = 98
bstack1l11ll1l11l_opy_ = 100
bstack1lllll1l1l_opy_ = (bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩἮ"), bstack1l1_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩἯ"), bstack1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠭ἰ"))
bstack1lll111l111_opy_ = {
  bstack1l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫἱ"): bstack1l1_opy_ (u"࠭࠭࠮ࡴࡨࡶࡺࡴࡳࠨἲ"),
  bstack1l1_opy_ (u"ࠧࡥࡧ࡯ࡥࡾ࠭ἳ"): bstack1l1_opy_ (u"ࠨ࠯࠰ࡶࡪࡸࡵ࡯ࡵ࠰ࡨࡪࡲࡡࡺࠩἴ"),
  bstack1l1_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧἵ"): 0
}
bstack111l111l111_opy_ = bstack1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥἶ")
bstack111l11111ll_opy_ = bstack1l1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣἷ")
bstack1ll1l111_opy_ = bstack1l1_opy_ (u"࡚ࠧࡅࡔࡖࠣࡖࡊࡖࡏࡓࡖࡌࡒࡌࠦࡁࡏࡆࠣࡅࡓࡇࡌ࡚ࡖࡌࡇࡘࠨἸ")