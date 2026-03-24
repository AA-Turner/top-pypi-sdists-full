# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import re
from enum import Enum
bstack1lll111ll1_opy_ = {
  bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᯎ"): bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࠫᯏ"),
  bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᯐ"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡭ࡨࡽࠬᯑ"),
  bstack1ll1lll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᯒ"): bstack1ll1lll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᯓ"),
  bstack1ll1lll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᯔ"): bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭ᯕ"),
  bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᯖ"): bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࠩᯗ"),
  bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᯘ"): bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࠩᯙ"),
  bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᯚ"): bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᯛ"),
  bstack1ll1lll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᯜ"): bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫ࠬᯝ"),
  bstack1ll1lll_opy_ (u"ࠨࡥࡲࡲࡸࡵ࡬ࡦࡎࡲ࡫ࡸ࠭ᯞ"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡲࡸࡵ࡬ࡦࠩᯟ"),
  bstack1ll1lll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨᯠ"): bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨᯡ"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩᯢ"): bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩᯣ"),
  bstack1ll1lll_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࠭ᯤ"): bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡷ࡫ࡧࡩࡴ࠭ᯥ"),
  bstack1ll1lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨ᯦"): bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨᯧ"),
  bstack1ll1lll_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫᯨ"): bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫᯩ"),
  bstack1ll1lll_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫᯪ"): bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫᯫ"),
  bstack1ll1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪᯬ"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪᯭ"),
  bstack1ll1lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᯮ"): bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᯯ"),
  bstack1ll1lll_opy_ (u"ࠬࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫᯰ"): bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫᯱ"),
  bstack1ll1lll_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸ᯲ࠬ"): bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸ᯳ࠬ"),
  bstack1ll1lll_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩ᯴"): bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩ᯵"),
  bstack1ll1lll_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭᯶"): bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭᯷"),
  bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨ᯸"): bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨ᯹"),
  bstack1ll1lll_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧ᯺"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡪࡲࡷࡹࡹࠧ᯻"),
  bstack1ll1lll_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫ᯼"): bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦ࡫ࡩࡡࡤࡪࡨࠫ᯽"),
  bstack1ll1lll_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭᯾"): bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭᯿"),
  bstack1ll1lll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪᰀ"): bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪᰁ"),
  bstack1ll1lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᰂ"): bstack1ll1lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪᰃ"),
  bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᰄ"): bstack1ll1lll_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪᰅ"),
  bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᰆ"): bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᰇ"),
  bstack1ll1lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨᰈ"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨᰉ"),
  bstack1ll1lll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫᰊ"): bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫᰋ"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᰌ"): bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧᰍ"),
  bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᰎ"): bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᰏ"),
  bstack1ll1lll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᰐ"): bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡳࡺࡸࡣࡦࠩᰑ"),
  bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᰒ"): bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᰓ"),
  bstack1ll1lll_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨᰔ"): bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡒࡦࡳࡥࠨᰕ"),
  bstack1ll1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫᰖ"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫᰗ"),
  bstack1ll1lll_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧᰘ"): bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧᰙ"),
  bstack1ll1lll_opy_ (u"ࠬࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪᰚ"): bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪᰛ"),
  bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᰜ"): bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᰝ"),
  bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᰞ"): bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᰟ")
}
bstack111l1l11l1l_opy_ = [
  bstack1ll1lll_opy_ (u"ࠫࡴࡹࠧᰠ"),
  bstack1ll1lll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᰡ"),
  bstack1ll1lll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᰢ"),
  bstack1ll1lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᰣ"),
  bstack1ll1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᰤ"),
  bstack1ll1lll_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭ᰥ"),
  bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᰦ"),
]
bstack11111l11l1_opy_ = {
  bstack1ll1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᰧ"): [bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᰨ"), bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡢࡒࡆࡓࡅࠨᰩ")],
  bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᰪ"): bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᰫ"),
  bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᰬ"): bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊ࠭ᰭ"),
  bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᰮ"): bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠪᰯ"),
  bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᰰ"): bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᰱ"),
  bstack1ll1lll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᰲ"): bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡖࡣࡕࡋࡒࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪᰳ"),
  bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᰴ"): bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࠩᰵ"),
  bstack1ll1lll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᰶ"): bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕ᰷ࠪ"),
  bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳࠫ᰸"): [bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࡣࡎࡊࠧ᰹"), bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡓࡔࠬ᰺")],
  bstack1ll1lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ᰻"): bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡍࡑࡊࡐࡊ࡜ࡅࡍࠩ᰼"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᰽"): bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ᰾"),
  bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ᰿"): [bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠬ᱀"), bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩ᱁")],
  bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ᱂"): bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘ࡚ࡘࡂࡐࡕࡆࡅࡑࡋࠧ᱃"),
  bstack1ll1lll_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡅࡏࡘࠪ᱄"): bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡒࡄࡊࡈࡗ࡙ࡘࡁࡕࡋࡒࡒࡤ࡙ࡍࡂࡔࡗࡣࡘࡋࡌࡆࡅࡗࡍࡔࡔ࡟ࡇࡇࡄࡘ࡚ࡘࡅࡠࡄࡕࡅࡓࡉࡈࡆࡕࠪ᱅")
}
bstack11llll111_opy_ = {
  bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᱆"): [bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ᱇"), bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᱈")],
  bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭᱉"): [bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡢ࡯ࡪࡿࠧ᱊"), bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᱋")],
  bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᱌"): bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᱍ"),
  bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᱎ"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᱏ"),
  bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᱐"): bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᱑"),
  bstack1ll1lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ᱒"): [bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡰࡱࠩ᱓"), bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭᱔")],
  bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᱕"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ᱖"),
  bstack1ll1lll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧ᱗"): bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧ᱘"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࠩ᱙"): bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱࠩᱚ"),
  bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᱛ"): bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᱜ"),
  bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᱝ"): bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᱞ"),
  bstack1ll1lll_opy_ (u"ࠦࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡉࡌࡊࠤᱟ"): bstack1ll1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࡵࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࡈࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࡦࡵࠥᱠ"),
}
bstack11111ll111_opy_ = {
  bstack1ll1lll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᱡ"): bstack1ll1lll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᱢ"),
  bstack1ll1lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᱣ"): [bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᱤ"), bstack1ll1lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᱥ")],
  bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᱦ"): bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᱧ"),
  bstack1ll1lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᱨ"): bstack1ll1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᱩ"),
  bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᱪ"): [bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᱫ"), bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᱬ")],
  bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᱭ"): bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᱮ"),
  bstack1ll1lll_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪᱯ"): bstack1ll1lll_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬᱰ"),
  bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᱱ"): [bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᱲ"), bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᱳ")],
  bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪᱴ"): [bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ᱵ"), bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭ᱶ")]
}
bstack1l11l1ll1_opy_ = [
  bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ᱷ"),
  bstack1ll1lll_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫᱸ"),
  bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨᱹ"),
  bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶࠪᱺ"),
  bstack1ll1lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭ᱻ"),
  bstack1ll1lll_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻࠪᱼ"),
  bstack1ll1lll_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩᱽ"),
  bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᱾"),
  bstack1ll1lll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭᱿"),
  bstack1ll1lll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᲀ"),
  bstack1ll1lll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲁ"),
  bstack1ll1lll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬᲂ"),
]
bstack11111l1ll1_opy_ = [
  bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᲃ"),
  bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪᲄ"),
  bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᲅ"),
  bstack1ll1lll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᲆ"),
  bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᲇ"),
  bstack1ll1lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᲈ"),
  bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᲉ"),
  bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᲊ"),
  bstack1ll1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ᲋"),
  bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ᲌"),
  bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᲍"),
  bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࠩ᲎"),
  bstack1ll1lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬ᲏"),
  bstack1ll1lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡘࡦ࡭ࠧᲐ"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᲑ"),
  bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᲒ"),
  bstack1ll1lll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫᲓ"),
  bstack1ll1lll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠷ࠧᲔ"),
  bstack1ll1lll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠲ࠨᲕ"),
  bstack1ll1lll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠴ࠩᲖ"),
  bstack1ll1lll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠶ࠪᲗ"),
  bstack1ll1lll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠸ࠫᲘ"),
  bstack1ll1lll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠺ࠬᲙ"),
  bstack1ll1lll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠼࠭Ლ"),
  bstack1ll1lll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠾ࠧᲛ"),
  bstack1ll1lll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠹ࠨᲜ"),
  bstack1ll1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᲝ"),
  bstack1ll1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᲞ"),
  bstack1ll1lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᲟ"),
  bstack1ll1lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᲠ"),
  bstack1ll1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᲡ"),
  bstack1ll1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬᲢ"),
  bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭Უ"),
  bstack1ll1lll_opy_ (u"ࠪ࡬ࡺࡨࡒࡦࡩ࡬ࡳࡳ࠭Ფ")
]
bstack111l111l111_opy_ = [
  bstack1ll1lll_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᲥ"),
  bstack1ll1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᲦ"),
  bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᲧ"),
  bstack1ll1lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᲨ"),
  bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡖࡲࡪࡱࡵ࡭ࡹࡿࠧᲩ"),
  bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᲪ"),
  bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡤ࡫ࠬᲫ"),
  bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᲬ"),
  bstack1ll1lll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᲭ"),
  bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᲮ"),
  bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᲯ"),
  bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧᲰ"),
  bstack1ll1lll_opy_ (u"ࠩࡲࡷࠬᲱ"),
  bstack1ll1lll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ჲ"),
  bstack1ll1lll_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪᲳ"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᲴ"),
  bstack1ll1lll_opy_ (u"࠭ࡲࡦࡩ࡬ࡳࡳ࠭Ჵ"),
  bstack1ll1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᲶ"),
  bstack1ll1lll_opy_ (u"ࠨ࡯ࡤࡧ࡭࡯࡮ࡦࠩᲷ"),
  bstack1ll1lll_opy_ (u"ࠩࡵࡩࡸࡵ࡬ࡶࡶ࡬ࡳࡳ࠭Ჸ"),
  bstack1ll1lll_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨᲹ"),
  bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᲺ"),
  bstack1ll1lll_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫ᲻"),
  bstack1ll1lll_opy_ (u"࠭࡮ࡰࡒࡤ࡫ࡪࡒ࡯ࡢࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᲼"),
  bstack1ll1lll_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨᲽ"),
  bstack1ll1lll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᲾ"),
  bstack1ll1lll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭Ჿ"),
  bstack1ll1lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡩࡳࡪࡋࡦࡻࡶࠫ᳀"),
  bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨ᳁"),
  bstack1ll1lll_opy_ (u"ࠬࡴ࡯ࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠩ᳂"),
  bstack1ll1lll_opy_ (u"࠭ࡣࡩࡧࡦ࡯࡚ࡘࡌࠨ᳃"),
  bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᳄"),
  bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡄࡱࡲ࡯࡮࡫ࡳࠨ᳅"),
  bstack1ll1lll_opy_ (u"ࠩࡦࡥࡵࡺࡵࡳࡧࡆࡶࡦࡹࡨࠨ᳆"),
  bstack1ll1lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ᳇"),
  bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ᳈"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡘࡨࡶࡸ࡯࡯࡯ࠩ᳉"),
  bstack1ll1lll_opy_ (u"࠭࡮ࡰࡄ࡯ࡥࡳࡱࡐࡰ࡮࡯࡭ࡳ࡭ࠧ᳊"),
  bstack1ll1lll_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭᳋"),
  bstack1ll1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡍࡱࡪࡷࠬ᳌"),
  bstack1ll1lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡋࡧࠫ᳍"),
  bstack1ll1lll_opy_ (u"ࠪࡨࡪࡪࡩࡤࡣࡷࡩࡩࡊࡥࡷ࡫ࡦࡩࠬ᳎"),
  bstack1ll1lll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡔࡦࡸࡡ࡮ࡵࠪ᳏"),
  bstack1ll1lll_opy_ (u"ࠬࡶࡨࡰࡰࡨࡒࡺࡳࡢࡦࡴࠪ᳐"),
  bstack1ll1lll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫ᳑"),
  bstack1ll1lll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡔࡶࡴࡪࡱࡱࡷࠬ᳒"),
  bstack1ll1lll_opy_ (u"ࠨࡥࡲࡲࡸࡵ࡬ࡦࡎࡲ࡫ࡸ࠭᳓"),
  bstack1ll1lll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄ᳔ࠩ"),
  bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹ᳕ࠧ"),
  bstack1ll1lll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡆ࡮ࡵ࡭ࡦࡶࡵ࡭ࡨ᳖࠭"),
  bstack1ll1lll_opy_ (u"ࠬࡼࡩࡥࡧࡲ࡚࠷᳗࠭"),
  bstack1ll1lll_opy_ (u"࠭࡭ࡪࡦࡖࡩࡸࡹࡩࡰࡰࡌࡲࡸࡺࡡ࡭࡮ࡄࡴࡵࡹ᳘ࠧ"),
  bstack1ll1lll_opy_ (u"ࠧࡦࡵࡳࡶࡪࡹࡳࡰࡕࡨࡶࡻ࡫ࡲࠨ᳙"),
  bstack1ll1lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ᳚"),
  bstack1ll1lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡇࡩࡶࠧ᳛"),
  bstack1ll1lll_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵ᳜ࠪ"),
  bstack1ll1lll_opy_ (u"ࠫࡸࡿ࡮ࡤࡖ࡬ࡱࡪ࡝ࡩࡵࡪࡑࡘࡕ᳝࠭"),
  bstack1ll1lll_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰ᳞ࠪ"),
  bstack1ll1lll_opy_ (u"࠭ࡧࡱࡵࡏࡳࡨࡧࡴࡪࡱࡱ᳟ࠫ"),
  bstack1ll1lll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨ᳠"),
  bstack1ll1lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨ᳡"),
  bstack1ll1lll_opy_ (u"ࠩࡩࡳࡷࡩࡥࡄࡪࡤࡲ࡬࡫ࡊࡢࡴ᳢ࠪ"),
  bstack1ll1lll_opy_ (u"ࠪࡼࡲࡹࡊࡢࡴ᳣ࠪ"),
  bstack1ll1lll_opy_ (u"ࠫࡽࡳࡸࡋࡣࡵ᳤ࠫ"),
  bstack1ll1lll_opy_ (u"ࠬࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶ᳥ࠫ"),
  bstack1ll1lll_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭᳦࠭"),
  bstack1ll1lll_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ᳧"),
  bstack1ll1lll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶ᳨ࠫ"),
  bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᳩ"),
  bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩᳪ"),
  bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡳࡪࡩࡱࡅࡵࡶࠧᳫ"),
  bstack1ll1lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࡴࠩᳬ"),
  bstack1ll1lll_opy_ (u"࠭ࡣࡢࡰࡤࡶࡾ᳭࠭"),
  bstack1ll1lll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᳮ"),
  bstack1ll1lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᳯ"),
  bstack1ll1lll_opy_ (u"ࠩ࡬ࡩࠬᳰ"),
  bstack1ll1lll_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᳱ"),
  bstack1ll1lll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᳲ"),
  bstack1ll1lll_opy_ (u"ࠬࡷࡵࡦࡷࡨࠫᳳ"),
  bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ᳴"),
  bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳࡗࡹࡵࡲࡦࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠨᳵ"),
  bstack1ll1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡄࡣࡰࡩࡷࡧࡉ࡮ࡣࡪࡩࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧᳶ"),
  bstack1ll1lll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡅࡹࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬ᳷"),
  bstack1ll1lll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡊࡰࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭᳸"),
  bstack1ll1lll_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨ᳹"),
  bstack1ll1lll_opy_ (u"ࠬࡸࡥࡴࡧࡵࡺࡪࡊࡥࡷ࡫ࡦࡩࠬᳺ"),
  bstack1ll1lll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭᳻"),
  bstack1ll1lll_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ᳼"),
  bstack1ll1lll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡣࡶࡷࡨࡵࡤࡦࠩ᳽"),
  bstack1ll1lll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡋࡲࡷࡉ࡫ࡶࡪࡥࡨࡗࡪࡺࡴࡪࡰࡪࡷࠬ᳾"),
  bstack1ll1lll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡹࡩ࡯࡯ࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪ᳿"),
  bstack1ll1lll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡵࡶ࡬ࡦࡒࡤࡽࠬᴀ"),
  bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᴁ"),
  bstack1ll1lll_opy_ (u"࠭ࡷࡥ࡫ࡲࡗࡪࡸࡶࡪࡥࡨࠫᴂ"),
  bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴃ"),
  bstack1ll1lll_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵࡅࡵࡳࡸࡹࡓࡪࡶࡨࡘࡷࡧࡣ࡬࡫ࡱ࡫ࠬᴄ"),
  bstack1ll1lll_opy_ (u"ࠩ࡫࡭࡬࡮ࡃࡰࡰࡷࡶࡦࡹࡴࠨᴅ"),
  bstack1ll1lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡓࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࡹࠧᴆ"),
  bstack1ll1lll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧᴇ"),
  bstack1ll1lll_opy_ (u"ࠬࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴈ"),
  bstack1ll1lll_opy_ (u"࠭ࡲࡦ࡯ࡲࡺࡪࡏࡏࡔࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࡒ࡯ࡤࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫᴉ"),
  bstack1ll1lll_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩᴊ"),
  bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᴋ"),
  bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᴌ"),
  bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᴍ"),
  bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᴎ"),
  bstack1ll1lll_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨᴏ"),
  bstack1ll1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬᴐ"),
  bstack1ll1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡴࡻࡴࡴࠩᴑ"),
  bstack1ll1lll_opy_ (u"ࠨࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡔࡷࡵ࡭ࡱࡶࡅࡩ࡭ࡧࡶࡪࡱࡵࠫᴒ")
]
bstack1ll1ll1l1l_opy_ = {
  bstack1ll1lll_opy_ (u"ࠩࡹࠫᴓ"): bstack1ll1lll_opy_ (u"ࠪࡺࠬᴔ"),
  bstack1ll1lll_opy_ (u"ࠫ࡫࠭ᴕ"): bstack1ll1lll_opy_ (u"ࠬ࡬ࠧᴖ"),
  bstack1ll1lll_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬᴗ"): bstack1ll1lll_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭ᴘ"),
  bstack1ll1lll_opy_ (u"ࠨࡱࡱࡰࡾࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᴙ"): bstack1ll1lll_opy_ (u"ࠩࡲࡲࡱࡿࡁࡶࡶࡲࡱࡦࡺࡥࠨᴚ"),
  bstack1ll1lll_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧᴛ"): bstack1ll1lll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨᴜ"),
  bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨᴝ"): bstack1ll1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩᴞ"),
  bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪᴟ"): bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᴠ"),
  bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᴡ"): bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᴢ"),
  bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᴣ"): bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨᴤ"),
  bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧᴥ"): bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡌࡴࡹࡴࠨᴦ"),
  bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩᴧ"): bstack1ll1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᴨ"),
  bstack1ll1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᴩ"): bstack1ll1lll_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᴪ"),
  bstack1ll1lll_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧᴫ"): bstack1ll1lll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᴬ"),
  bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᴭ"): bstack1ll1lll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪᴮ"),
  bstack1ll1lll_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᴯ"): bstack1ll1lll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬᴰ"),
  bstack1ll1lll_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨᴱ"): bstack1ll1lll_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩᴲ"),
  bstack1ll1lll_opy_ (u"࠭ࡰࡢࡥࡩ࡭ࡱ࡫ࠧᴳ"): bstack1ll1lll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᴴ"),
  bstack1ll1lll_opy_ (u"ࠨࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᴵ"): bstack1ll1lll_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᴶ"),
  bstack1ll1lll_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᴷ"): bstack1ll1lll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᴸ"),
  bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭ᴹ"): bstack1ll1lll_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧᴺ"),
  bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᴻ"): bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᴼ"),
  bstack1ll1lll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫᴽ"): bstack1ll1lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࠫᴾ")
}
bstack111l11l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡩࡵࡪࡸࡦ࠳ࡩ࡯࡮࠱ࡳࡩࡷࡩࡹ࠰ࡥ࡯࡭࠴ࡸࡥ࡭ࡧࡤࡷࡪࡹ࠯࡭ࡣࡷࡩࡸࡺ࠯ࡥࡱࡺࡲࡱࡵࡡࡥࠤᴿ")
bstack111l11lll1l_opy_ = bstack1ll1lll_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠴࡮ࡥࡢ࡮ࡷ࡬ࡨ࡮ࡥࡤ࡭ࠥᵀ")
bstack1111ll1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡦࡦࡶ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡴࡧࡱࡨࡤࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤᵁ")
HTTPS_HUB = bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡹࡧ࠳࡭ࡻࡢࠨᵂ")
bstack1l1l11l111_opy_ = bstack1ll1lll_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠫᵃ")
bstack111l11l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠺࠴࠵࠶࠲ࡻࡩ࠵ࡨࡶࡤࠪᵄ")
bstack1llll1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡳ࡫ࡸࡵࡡ࡫ࡹࡧࡹࠧᵅ")
bstack1ll1l1ll_opy_ = {
  bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡦࡢࡷ࡯ࡸࠬᵆ"): bstack1ll1lll_opy_ (u"ࠬ࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᵇ"),
  bstack1ll1lll_opy_ (u"࠭ࡵࡴ࠯ࡨࡥࡸࡺࠧᵈ"): bstack1ll1lll_opy_ (u"ࠧࡩࡷࡥ࠱ࡺࡹࡥ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᵉ"),
  bstack1ll1lll_opy_ (u"ࠨࡷࡶࠫᵊ"): bstack1ll1lll_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡵࡴ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᵋ"),
  bstack1ll1lll_opy_ (u"ࠪࡩࡺ࠭ᵌ"): bstack1ll1lll_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡧࡸ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᵍ"),
  bstack1ll1lll_opy_ (u"ࠬ࡯࡮ࠨᵎ"): bstack1ll1lll_opy_ (u"࠭ࡨࡶࡤ࠰ࡥࡵࡹ࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᵏ"),
  bstack1ll1lll_opy_ (u"ࠧࡢࡷࠪᵐ"): bstack1ll1lll_opy_ (u"ࠨࡪࡸࡦ࠲ࡧࡰࡴࡧ࠰ࡳࡳࡲࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᵑ")
}
bstack111l111lll1_opy_ = {
  bstack1ll1lll_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫᵒ"): 50,
  bstack1ll1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᵓ"): 40,
  bstack1ll1lll_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬᵔ"): 30,
  bstack1ll1lll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᵕ"): 20,
  bstack1ll1lll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᵖ"): 10
}
bstack1111lll111_opy_ = bstack111l111lll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡪࡰࡩࡳࠬᵗ")]
bstack1l1lll11_opy_ = bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤ࠱ࠪᵘ")
bstack111l1lllll_opy_ = bstack1ll1lll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᵙ")
bstack111l11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᵚ")
bstack1lll1l1111_opy_ = bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪᵛ")
bstack111l1ll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪᵜ")
bstack11l111llll_opy_ = {
  bstack1ll1lll_opy_ (u"࠭ࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࠫᵝ"): bstack1ll1lll_opy_ (u"ࠧࠫࠬ࠭ࠤࡠ࡙ࡄࡌ࠯ࡊࡉࡓ࠳࠰࠱࠷ࡠࠤࡥࡶࡹࡵࡧࡶࡸ࠲ࡶࡡࡳࡣ࡯ࡰࡪࡲࡠࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡪࡰࠣࡽࡴࡻࡲࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹ࠴ࠠࡕࡪ࡬ࡷࠥࡳࡡࡺࠢࡦࡥࡺࡹࡥࠡࡥࡲࡲ࡫ࡲࡩࡤࡶࡶࠤࡼ࡯ࡴࡩࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡵ࡯࡫ࡱࡷࡹࡧ࡬࡭ࠢ࡬ࡸࠥࡻࡳࡪࡰࡪ࠾ࠥࡶࡩࡱࠢࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡶࡡࡳࡣ࡯ࡰࡪࡲࠠࠫࠬ࠭ࠫᵞ")
}
bstack111l1l1111l_opy_ = [bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩᵟ"), bstack1ll1lll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩᵠ")]
bstack111l11l11ll_opy_ = [bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᵡ"), bstack1ll1lll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᵢ")]
bstack1l1lll111l_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࠬࡤ࡛࡝࡞ࡺ࠱ࡢ࠱࠺࠯ࠬࠧࠫᵣ"))
bstack11l11111_opy_ = [
  bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡑࡥࡲ࡫ࠧᵤ"),
  bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᵥ"),
  bstack1ll1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᵦ"),
  bstack1ll1lll_opy_ (u"ࠩࡱࡩࡼࡉ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᵧ"),
  bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࠧᵨ"),
  bstack1ll1lll_opy_ (u"ࠫࡺࡪࡩࡥࠩᵩ"),
  bstack1ll1lll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᵪ"),
  bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࠭ᵫ"),
  bstack1ll1lll_opy_ (u"ࠧࡰࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬᵬ"),
  bstack1ll1lll_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࠭ᵭ"),
  bstack1ll1lll_opy_ (u"ࠩࡱࡳࡗ࡫ࡳࡦࡶࠪᵮ"), bstack1ll1lll_opy_ (u"ࠪࡪࡺࡲ࡬ࡓࡧࡶࡩࡹ࠭ᵯ"),
  bstack1ll1lll_opy_ (u"ࠫࡨࡲࡥࡢࡴࡖࡽࡸࡺࡥ࡮ࡈ࡬ࡰࡪࡹࠧᵰ"),
  bstack1ll1lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡘ࡮ࡳࡩ࡯ࡩࡶࠫᵱ"),
  bstack1ll1lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࡏࡳ࡬࡭ࡩ࡯ࡩࠪᵲ"),
  bstack1ll1lll_opy_ (u"ࠧࡰࡶ࡫ࡩࡷࡇࡰࡱࡵࠪᵳ"),
  bstack1ll1lll_opy_ (u"ࠨࡲࡵ࡭ࡳࡺࡐࡢࡩࡨࡗࡴࡻࡲࡤࡧࡒࡲࡋ࡯࡮ࡥࡈࡤ࡭ࡱࡻࡲࡦࠩᵴ"),
  bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧᵵ"), bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࡐࡢࡥ࡮ࡥ࡬࡫ࠧᵶ"), bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡆࡩࡴࡪࡸ࡬ࡸࡾ࠭ᵷ"), bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡖࡡࡤ࡭ࡤ࡫ࡪ࠭ᵸ"), bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡄࡶࡴࡤࡸ࡮ࡵ࡮ࠨᵹ"),
  bstack1ll1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬᵺ"),
  bstack1ll1lll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡔࡦࡵࡷࡔࡦࡩ࡫ࡢࡩࡨࡷࠬᵻ"),
  bstack1ll1lll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡆࡳࡻ࡫ࡲࡢࡩࡨࠫᵼ"), bstack1ll1lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࡊࡴࡤࡊࡰࡷࡩࡳࡺࠧᵽ"),
  bstack1ll1lll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩᵾ"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡤࡣࡒࡲࡶࡹ࠭ᵿ"),
  bstack1ll1lll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪ࡙࡯ࡤ࡭ࡨࡸࠬᶀ"),
  bstack1ll1lll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡊࡰࡶࡸࡦࡲ࡬ࡕ࡫ࡰࡩࡴࡻࡴࠨᶁ"),
  bstack1ll1lll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡸ࡭࠭ᶂ"),
  bstack1ll1lll_opy_ (u"ࠩࡤࡺࡩ࠭ᶃ"), bstack1ll1lll_opy_ (u"ࠪࡥࡻࡪࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᶄ"), bstack1ll1lll_opy_ (u"ࠫࡦࡼࡤࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᶅ"), bstack1ll1lll_opy_ (u"ࠬࡧࡶࡥࡃࡵ࡫ࡸ࠭ᶆ"),
  bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡎࡩࡾࡹࡴࡰࡴࡨࠫᶇ"), bstack1ll1lll_opy_ (u"ࠧ࡬ࡧࡼࡷࡹࡵࡲࡦࡒࡤࡸ࡭࠭ᶈ"), bstack1ll1lll_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡸࡹࡷࡰࡴࡧࠫᶉ"),
  bstack1ll1lll_opy_ (u"ࠩ࡮ࡩࡾࡇ࡬ࡪࡣࡶࠫᶊ"), bstack1ll1lll_opy_ (u"ࠪ࡯ࡪࡿࡐࡢࡵࡶࡻࡴࡸࡤࠨᶋ"),
  bstack1ll1lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭ᶌ"), bstack1ll1lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡅࡷ࡭ࡳࠨᶍ"), bstack1ll1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࡅ࡫ࡵࠫᶎ"), bstack1ll1lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡉࡨࡳࡱࡰࡩࡒࡧࡰࡱ࡫ࡱ࡫ࡋ࡯࡬ࡦࠩᶏ"), bstack1ll1lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡕࡴࡧࡖࡽࡸࡺࡥ࡮ࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࠬᶐ"),
  bstack1ll1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡑࡱࡵࡸࠬᶑ"), bstack1ll1lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹࡹࠧᶒ"),
  bstack1ll1lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡇ࡭ࡸࡧࡢ࡭ࡧࡅࡹ࡮ࡲࡤࡄࡪࡨࡧࡰ࠭ᶓ"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࡗ࡭ࡲ࡫࡯ࡶࡶࠪᶔ"),
  bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡇࡣࡵ࡫ࡲࡲࠬᶕ"), bstack1ll1lll_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡃࡢࡶࡨ࡫ࡴࡸࡹࠨᶖ"), bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡇ࡮ࡤ࡫ࡸ࠭ᶗ"), bstack1ll1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡣ࡯ࡍࡳࡺࡥ࡯ࡶࡄࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᶘ"),
  bstack1ll1lll_opy_ (u"ࠪࡨࡴࡴࡴࡔࡶࡲࡴࡆࡶࡰࡐࡰࡕࡩࡸ࡫ࡴࠨᶙ"),
  bstack1ll1lll_opy_ (u"ࠫࡺࡴࡩࡤࡱࡧࡩࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ᶚ"), bstack1ll1lll_opy_ (u"ࠬࡸࡥࡴࡧࡷࡏࡪࡿࡢࡰࡣࡵࡨࠬᶛ"),
  bstack1ll1lll_opy_ (u"࠭࡮ࡰࡕ࡬࡫ࡳ࠭ᶜ"),
  bstack1ll1lll_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡕ࡯࡫ࡰࡴࡴࡸࡴࡢࡰࡷ࡚࡮࡫ࡷࡴࠩᶝ"),
  bstack1ll1lll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱࡨࡷࡵࡩࡥ࡙ࡤࡸࡨ࡮ࡥࡳࡵࠪᶞ"),
  bstack1ll1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᶟ"),
  bstack1ll1lll_opy_ (u"ࠪࡶࡪࡩࡲࡦࡣࡷࡩࡈ࡮ࡲࡰ࡯ࡨࡈࡷ࡯ࡶࡦࡴࡖࡩࡸࡹࡩࡰࡰࡶࠫᶠ"),
  bstack1ll1lll_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᶡ"),
  bstack1ll1lll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡒࡤࡸ࡭࠭ᶢ"),
  bstack1ll1lll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡓࡱࡧࡨࡨࠬᶣ"),
  bstack1ll1lll_opy_ (u"ࠧࡨࡲࡶࡉࡳࡧࡢ࡭ࡧࡧࠫᶤ"),
  bstack1ll1lll_opy_ (u"ࠨ࡫ࡶࡌࡪࡧࡤ࡭ࡧࡶࡷࠬᶥ"),
  bstack1ll1lll_opy_ (u"ࠩࡤࡨࡧࡋࡸࡦࡥࡗ࡭ࡲ࡫࡯ࡶࡶࠪᶦ"),
  bstack1ll1lll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࡖࡧࡷ࡯ࡰࡵࠩᶧ"),
  bstack1ll1lll_opy_ (u"ࠫࡸࡱࡩࡱࡆࡨࡺ࡮ࡩࡥࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨᶨ"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱࡊࡶࡦࡴࡴࡑࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠬᶩ"),
  bstack1ll1lll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡎࡢࡶࡸࡶࡦࡲࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫᶪ"),
  bstack1ll1lll_opy_ (u"ࠧࡴࡻࡶࡸࡪࡳࡐࡰࡴࡷࠫᶫ"),
  bstack1ll1lll_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡦࡥࡌࡴࡹࡴࠨᶬ"),
  bstack1ll1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡕ࡯࡮ࡲࡧࡰ࠭ᶭ"), bstack1ll1lll_opy_ (u"ࠪࡹࡳࡲ࡯ࡤ࡭ࡗࡽࡵ࡫ࠧᶮ"), bstack1ll1lll_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡏࡪࡿࠧᶯ"),
  bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱࡏࡥࡺࡴࡣࡩࠩᶰ"),
  bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡣࡢࡶࡆࡥࡵࡺࡵࡳࡧࠪᶱ"),
  bstack1ll1lll_opy_ (u"ࠧࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࡒࡸ࡭࡫ࡲࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩᶲ"),
  bstack1ll1lll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦ࡙࡬ࡲࡩࡵࡷࡂࡰ࡬ࡱࡦࡺࡩࡰࡰࠪᶳ"),
  bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡕࡱࡲࡰࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᶴ"),
  bstack1ll1lll_opy_ (u"ࠪࡩࡳ࡬࡯ࡳࡥࡨࡅࡵࡶࡉ࡯ࡵࡷࡥࡱࡲࠧᶵ"),
  bstack1ll1lll_opy_ (u"ࠫࡪࡴࡳࡶࡴࡨ࡛ࡪࡨࡶࡪࡧࡺࡷࡍࡧࡶࡦࡒࡤ࡫ࡪࡹࠧᶶ"), bstack1ll1lll_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡊࡥࡷࡶࡲࡳࡱࡹࡐࡰࡴࡷࠫᶷ"), bstack1ll1lll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡊࡥࡵࡣ࡬ࡰࡸࡉ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠩᶸ"),
  bstack1ll1lll_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫ࡁࡱࡲࡶࡇࡦࡩࡨࡦࡎ࡬ࡱ࡮ࡺࠧᶹ"),
  bstack1ll1lll_opy_ (u"ࠨࡥࡤࡰࡪࡴࡤࡢࡴࡉࡳࡷࡳࡡࡵࠩᶺ"),
  bstack1ll1lll_opy_ (u"ࠩࡥࡹࡳࡪ࡬ࡦࡋࡧࠫᶻ"),
  bstack1ll1lll_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪᶼ"),
  bstack1ll1lll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࡙ࡥࡳࡸ࡬ࡧࡪࡹࡅ࡯ࡣࡥࡰࡪࡪࠧᶽ"), bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡂࡷࡷ࡬ࡴࡸࡩࡻࡧࡧࠫᶾ"),
  bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲࡅࡨࡩࡥࡱࡶࡄࡰࡪࡸࡴࡴࠩᶿ"), bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷࡳࡉ࡯ࡳ࡮࡫ࡶࡷࡆࡲࡥࡳࡶࡶࠫ᷀"),
  bstack1ll1lll_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡊࡰࡶࡸࡷࡻ࡭ࡦࡰࡷࡷࡑ࡯ࡢࠨ᷁"),
  bstack1ll1lll_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦ࡙ࡧࡰࠨ᷂"),
  bstack1ll1lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌࡲ࡮ࡺࡩࡢ࡮ࡘࡶࡱ࠭᷃"), bstack1ll1lll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡅࡱࡲ࡯ࡸࡒࡲࡴࡺࡶࡳࠨ᷄"), bstack1ll1lll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎ࡭࡮ࡰࡴࡨࡊࡷࡧࡵࡥ࡙ࡤࡶࡳ࡯࡮ࡨࠩ᷅"), bstack1ll1lll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡦࡰࡏ࡭ࡳࡱࡳࡊࡰࡅࡥࡨࡱࡧࡳࡱࡸࡲࡩ࠭᷆"),
  bstack1ll1lll_opy_ (u"ࠧ࡬ࡧࡨࡴࡐ࡫ࡹࡄࡪࡤ࡭ࡳࡹࠧ᷇"),
  bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡻࡣࡥࡰࡪ࡙ࡴࡳ࡫ࡱ࡫ࡸࡊࡩࡳࠩ᷈"),
  bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡩࡥࡴࡵࡄࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᷉"),
  bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡍࡨࡽࡉ࡫࡬ࡢࡻ᷊ࠪ"),
  bstack1ll1lll_opy_ (u"ࠫࡸ࡮࡯ࡸࡋࡒࡗࡑࡵࡧࠨ᷋"),
  bstack1ll1lll_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧ᷌"),
  bstack1ll1lll_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡘࡥࡴࡲࡲࡲࡸ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧ᷍"), bstack1ll1lll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷ࡛ࡦ࡯ࡴࡕ࡫ࡰࡩࡴࡻࡴࠨ᷎"),
  bstack1ll1lll_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼ᷏ࠫ"),
  bstack1ll1lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡶࡽࡳࡩࡅࡹࡧࡦࡹࡹ࡫ࡆࡳࡱࡰࡌࡹࡺࡰࡴ᷐ࠩ"),
  bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡇࡦࡶࡴࡶࡴࡨࠫ᷑"),
  bstack1ll1lll_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫ᷒"),
  bstack1ll1lll_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡆࡳࡳࡺࡥࡹࡶࡏ࡭ࡸࡺࠧᷓ"),
  bstack1ll1lll_opy_ (u"࠭ࡷࡢ࡫ࡷࡊࡴࡸࡁࡱࡲࡖࡧࡷ࡯ࡰࡵࠩᷔ"),
  bstack1ll1lll_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡄࡱࡱࡲࡪࡩࡴࡓࡧࡷࡶ࡮࡫ࡳࠨᷕ"),
  bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡓࡧ࡭ࡦࠩᷖ"),
  bstack1ll1lll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡖࡐࡈ࡫ࡲࡵࠩᷗ"),
  bstack1ll1lll_opy_ (u"ࠪࡸࡦࡶࡗࡪࡶ࡫ࡗ࡭ࡵࡲࡵࡒࡵࡩࡸࡹࡄࡶࡴࡤࡸ࡮ࡵ࡮ࠨᷘ"),
  bstack1ll1lll_opy_ (u"ࠫࡸࡩࡡ࡭ࡧࡉࡥࡨࡺ࡯ࡳࠩᷙ"),
  bstack1ll1lll_opy_ (u"ࠬࡽࡤࡢࡎࡲࡧࡦࡲࡐࡰࡴࡷࠫᷚ"),
  bstack1ll1lll_opy_ (u"࠭ࡳࡩࡱࡺ࡜ࡨࡵࡤࡦࡎࡲ࡫ࠬᷛ"),
  bstack1ll1lll_opy_ (u"ࠧࡪࡱࡶࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡻࡳࡦࠩᷜ"),
  bstack1ll1lll_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡃࡰࡰࡩ࡭࡬ࡌࡩ࡭ࡧࠪᷝ"),
  bstack1ll1lll_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡹࡳࡸࡱࡵࡨࠬᷞ"),
  bstack1ll1lll_opy_ (u"ࠪࡹࡸ࡫ࡐࡳࡧࡥࡹ࡮ࡲࡴࡘࡆࡄࠫᷟ"),
  bstack1ll1lll_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸ࡜ࡊࡁࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠬᷠ"),
  bstack1ll1lll_opy_ (u"ࠬࡽࡥࡣࡆࡵ࡭ࡻ࡫ࡲࡂࡩࡨࡲࡹ࡛ࡲ࡭ࠩᷡ"),
  bstack1ll1lll_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡷ࡬ࠬᷢ"),
  bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨࡒࡪࡽࡗࡅࡃࠪᷣ"),
  bstack1ll1lll_opy_ (u"ࠨࡹࡧࡥࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫᷤ"), bstack1ll1lll_opy_ (u"ࠩࡺࡨࡦࡉ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࡖ࡬ࡱࡪࡵࡵࡵࠩᷥ"),
  bstack1ll1lll_opy_ (u"ࠪࡼࡨࡵࡤࡦࡑࡵ࡫ࡎࡪࠧᷦ"), bstack1ll1lll_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡖ࡭࡬ࡴࡩ࡯ࡩࡌࡨࠬᷧ"),
  bstack1ll1lll_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩ࡝ࡄࡂࡄࡸࡲࡩࡲࡥࡊࡦࠪᷨ"),
  bstack1ll1lll_opy_ (u"࠭ࡲࡦࡵࡨࡸࡔࡴࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡵࡸࡔࡴ࡬ࡺࠩᷩ"),
  bstack1ll1lll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࡴࠩᷪ"),
  bstack1ll1lll_opy_ (u"ࠨࡹࡧࡥࡘࡺࡡࡳࡶࡸࡴࡗ࡫ࡴࡳ࡫ࡨࡷࠬᷫ"), bstack1ll1lll_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴࡼࡍࡳࡺࡥࡳࡸࡤࡰࠬᷬ"),
  bstack1ll1lll_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࡌࡦࡸࡤࡸࡣࡵࡩࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ᷭ"),
  bstack1ll1lll_opy_ (u"ࠫࡲࡧࡸࡕࡻࡳ࡭ࡳ࡭ࡆࡳࡧࡴࡹࡪࡴࡣࡺࠩᷮ"),
  bstack1ll1lll_opy_ (u"ࠬࡹࡩ࡮ࡲ࡯ࡩࡎࡹࡖࡪࡵ࡬ࡦࡱ࡫ࡃࡩࡧࡦ࡯ࠬᷯ"),
  bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡆࡥࡷࡺࡨࡢࡩࡨࡗࡸࡲࠧᷰ"),
  bstack1ll1lll_opy_ (u"ࠧࡴࡪࡲࡹࡱࡪࡕࡴࡧࡖ࡭ࡳ࡭࡬ࡦࡶࡲࡲ࡙࡫ࡳࡵࡏࡤࡲࡦ࡭ࡥࡳࠩᷱ"),
  bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡉࡘࡆࡓࠫᷲ"),
  bstack1ll1lll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡱࡸࡧ࡭ࡏࡤࡆࡰࡵࡳࡱࡲࠧᷳ"),
  bstack1ll1lll_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡋ࡭ࡩࡪࡥ࡯ࡃࡳ࡭ࡕࡵ࡬ࡪࡥࡼࡉࡷࡸ࡯ࡳࠩᷴ"),
  bstack1ll1lll_opy_ (u"ࠫࡲࡵࡣ࡬ࡎࡲࡧࡦࡺࡩࡰࡰࡄࡴࡵ࠭᷵"),
  bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡨࡥࡤࡸࡋࡵࡲ࡮ࡣࡷࠫ᷶"), bstack1ll1lll_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌࡩ࡭ࡶࡨࡶࡘࡶࡥࡤࡵ᷷ࠪ"),
  bstack1ll1lll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡊࡥ࡭ࡣࡼࡅࡩࡨ᷸ࠧ"),
  bstack1ll1lll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡋࡧࡐࡴࡩࡡࡵࡱࡵࡅࡺࡺ࡯ࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱ᷹ࠫ")
]
bstack11l11l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡷࡳࡰࡴࡧࡤࠨ᷺")
bstack111l111ll1_opy_ = [bstack1ll1lll_opy_ (u"ࠪ࠲ࡦࡶ࡫ࠨ᷻"), bstack1ll1lll_opy_ (u"ࠫ࠳ࡧࡡࡣࠩ᷼"), bstack1ll1lll_opy_ (u"ࠬ࠴ࡩࡱࡣ᷽ࠪ")]
bstack11l1ll1l_opy_ = [bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩ᷾"), bstack1ll1lll_opy_ (u"ࠧࡱࡣࡷ࡬᷿ࠬ"), bstack1ll1lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫḀ"), bstack1ll1lll_opy_ (u"ࠩࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤࠨḁ")]
bstack1ll1111111_opy_ = {
  bstack1ll1lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪḂ"): bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩḃ"),
  bstack1ll1lll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭Ḅ"): bstack1ll1lll_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫḅ"),
  bstack1ll1lll_opy_ (u"ࠧࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬḆ"): bstack1ll1lll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩḇ"),
  bstack1ll1lll_opy_ (u"ࠩ࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬḈ"): bstack1ll1lll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩḉ"),
  bstack1ll1lll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵࡺࡩࡰࡰࡶࠫḊ"): bstack1ll1lll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ḋ")
}
bstack11ll1lll11_opy_ = [
  bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫḌ"),
  bstack1ll1lll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬḍ"),
  bstack1ll1lll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩḎ"),
  bstack1ll1lll_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨḏ"),
  bstack1ll1lll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫḐ"),
]
bstack11llll1l11_opy_ = bstack11111l1ll1_opy_ + bstack111l111l111_opy_ + bstack11l11111_opy_
bstack1llllll11l_opy_ = [
  bstack1ll1lll_opy_ (u"ࠫࡣࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴࠥࠩḑ"),
  bstack1ll1lll_opy_ (u"ࠬࡤࡢࡴ࠯࡯ࡳࡨࡧ࡬࠯ࡥࡲࡱࠩ࠭Ḓ"),
  bstack1ll1lll_opy_ (u"࠭࡞࠲࠴࠺࠲ࠬḓ"),
  bstack1ll1lll_opy_ (u"ࠧ࡟࠳࠳࠲ࠬḔ"),
  bstack1ll1lll_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠱࡜࠸࠰࠽ࡢ࠴ࠧḕ"),
  bstack1ll1lll_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠳࡝࠳࠱࠾ࡣ࠮ࠨḖ"),
  bstack1ll1lll_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠵࡞࠴࠲࠷࡝࠯ࠩḗ"),
  bstack1ll1lll_opy_ (u"ࠫࡣ࠷࠹࠳࠰࠴࠺࠽࠴ࠧḘ")
]
bstack111ll11111l_opy_ = bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ḙ")
bstack1111ll111_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠲ࡺ࠶࠵ࡥࡷࡧࡱࡸࠬḚ")
bstack1l1l1l1l_opy_ = [ bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩḛ") ]
bstack111lllll1l_opy_ = [ bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧḜ") ]
bstack1l11l1l1l_opy_ = [bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ḝ")]
bstack1ll111l11_opy_ = [ bstack1ll1lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḞ") ]
bstack1lll11l11_opy_ = bstack1ll1lll_opy_ (u"ࠫࡘࡊࡋࡔࡧࡷࡹࡵ࠭ḟ")
bstack11111111_opy_ = bstack1ll1lll_opy_ (u"࡙ࠬࡄࡌࡖࡨࡷࡹࡇࡴࡵࡧࡰࡴࡹ࡫ࡤࠨḠ")
bstack1ll1l1l111_opy_ = bstack1ll1lll_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠪḡ")
bstack111l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠧ࠵࠰࠳࠲࠵࠭Ḣ")
bstack111ll1l1_opy_ = [
  bstack1ll1lll_opy_ (u"ࠨࡇࡕࡖࡤࡌࡁࡊࡎࡈࡈࠬḣ"),
  bstack1ll1lll_opy_ (u"ࠩࡈࡖࡗࡥࡔࡊࡏࡈࡈࡤࡕࡕࡕࠩḤ"),
  bstack1ll1lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡃࡎࡒࡇࡐࡋࡄࡠࡄ࡜ࡣࡈࡒࡉࡆࡐࡗࠫḥ"),
  bstack1ll1lll_opy_ (u"ࠫࡊࡘࡒࡠࡐࡈࡘ࡜ࡕࡒࡌࡡࡆࡌࡆࡔࡇࡆࡆࠪḦ"),
  bstack1ll1lll_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡅࡕࡡࡑࡓ࡙ࡥࡃࡐࡐࡑࡉࡈ࡚ࡅࡅࠩḧ"),
  bstack1ll1lll_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡄࡎࡒࡗࡊࡊࠧḨ"),
  bstack1ll1lll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡔࡈࡗࡊ࡚ࠧḩ"),
  bstack1ll1lll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡋ࡛ࡓࡆࡆࠪḪ"),
  bstack1ll1lll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡅࡇࡕࡒࡕࡇࡇࠫḫ"),
  bstack1ll1lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫḬ"),
  bstack1ll1lll_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡎࡐࡖࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࠬḭ"),
  bstack1ll1lll_opy_ (u"ࠬࡋࡒࡓࡡࡄࡈࡉࡘࡅࡔࡕࡢࡍࡓ࡜ࡁࡍࡋࡇࠫḮ"),
  bstack1ll1lll_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣ࡚ࡔࡒࡆࡃࡆࡌࡆࡈࡌࡆࠩḯ"),
  bstack1ll1lll_opy_ (u"ࠧࡆࡔࡕࡣ࡙࡛ࡎࡏࡇࡏࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨḰ"),
  bstack1ll1lll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡗࡍࡒࡋࡄࡠࡑࡘࡘࠬḱ"),
  bstack1ll1lll_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡗࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩḲ"),
  bstack1ll1lll_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡌࡔ࡙ࡔࡠࡗࡑࡖࡊࡇࡃࡉࡃࡅࡐࡊ࠭ḳ"),
  bstack1ll1lll_opy_ (u"ࠫࡊࡘࡒࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫḴ"),
  bstack1ll1lll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ḵ"),
  bstack1ll1lll_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡔࡈࡗࡔࡒࡕࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬḶ"),
  bstack1ll1lll_opy_ (u"ࠧࡆࡔࡕࡣࡒࡇࡎࡅࡃࡗࡓࡗ࡟࡟ࡑࡔࡒ࡜࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ḷ"),
]
bstack111l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠨ࠰࠲ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡤࡶࡹ࡯ࡦࡢࡥࡷࡷ࠴࠭Ḹ")
bstack111l11ll1_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠩࢁࠫḹ")), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪḺ"), bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪḻ"))
bstack111llll11l1_opy_ = bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴ࡮࠭Ḽ")
bstack111l11lllll_opy_ = [ bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ḽ"), bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭Ḿ"), bstack1ll1lll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧḿ"), bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩṀ")]
bstack1ll1l1l1l_opy_ = [ bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪṁ"), bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪṂ"), bstack1ll1lll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫṃ"), bstack1ll1lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭Ṅ") ]
bstack1l1ll1ll_opy_ = [ bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ṅ") ]
bstack111l11ll1l1_opy_ = [ bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨṆ") ]
bstack1llll1l1ll_opy_ = 360
bstack111l1llll1l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡤࡴࡵ࠳ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤṇ")
bstack111l1111lll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴࡯ࡳࡴࡷࡨࡷࠧṈ")
bstack111l1l11111_opy_ = bstack1ll1lll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠢṉ")
bstack111lll1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡴࡦࡵࡷࡷࠥࡧࡲࡦࠢࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡵ࡮ࠡࡑࡖࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࠫࡳࠡࡣࡱࡨࠥࡧࡢࡰࡸࡨࠤ࡫ࡵࡲࠡࡃࡱࡨࡷࡵࡩࡥࠢࡧࡩࡻ࡯ࡣࡦࡵ࠱ࠦṊ")
bstack111lll111l1_opy_ = bstack1ll1lll_opy_ (u"ࠨ࠱࠲࠰࠳ࠦṋ")
bstack1lllll1l11l_opy_ = {
  bstack1ll1lll_opy_ (u"ࠧࡑࡃࡖࡗࠬṌ"): bstack1ll1lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨṍ"),
  bstack1ll1lll_opy_ (u"ࠩࡉࡅࡎࡒࠧṎ"): bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪṏ"),
  bstack1ll1lll_opy_ (u"ࠫࡘࡑࡉࡑࠩṐ"): bstack1ll1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ṑ")
}
bstack1ll1l11lll_opy_ = [
  bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࠥṒ"),
  bstack1ll1lll_opy_ (u"ࠢࡨࡱࡅࡥࡨࡱࠢṓ"),
  bstack1ll1lll_opy_ (u"ࠣࡩࡲࡊࡴࡸࡷࡢࡴࡧࠦṔ"),
  bstack1ll1lll_opy_ (u"ࠤࡵࡩ࡫ࡸࡥࡴࡪࠥṕ"),
  bstack1ll1lll_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤṖ"),
  bstack1ll1lll_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣṗ"),
  bstack1ll1lll_opy_ (u"ࠧࡹࡵࡣ࡯࡬ࡸࡊࡲࡥ࡮ࡧࡱࡸࠧṘ"),
  bstack1ll1lll_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥṙ"),
  bstack1ll1lll_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡅࡨࡺࡩࡷࡧࡈࡰࡪࡳࡥ࡯ࡶࠥṚ"),
  bstack1ll1lll_opy_ (u"ࠣࡥ࡯ࡩࡦࡸࡅ࡭ࡧࡰࡩࡳࡺࠢṛ"),
  bstack1ll1lll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࡵࠥṜ"),
  bstack1ll1lll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠥṝ"),
  bstack1ll1lll_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡆࡹࡹ࡯ࡥࡖࡧࡷ࡯ࡰࡵࠤṞ"),
  bstack1ll1lll_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦṟ"),
  bstack1ll1lll_opy_ (u"ࠨࡱࡶ࡫ࡷࠦṠ"),
  bstack1ll1lll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡕࡱࡸࡧ࡭ࡇࡣࡵ࡫ࡲࡲࠧṡ"),
  bstack1ll1lll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡏࡸࡰࡹ࡯ࡔࡰࡷࡦ࡬ࠧṢ"),
  bstack1ll1lll_opy_ (u"ࠤࡶ࡬ࡦࡱࡥࠣṣ"),
  bstack1ll1lll_opy_ (u"ࠥࡧࡱࡵࡳࡦࡃࡳࡴࠧṤ")
]
bstack111l1l11lll_opy_ = [
  bstack1ll1lll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥṥ"),
  bstack1ll1lll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤṦ"),
  bstack1ll1lll_opy_ (u"ࠨࡡࡶࡶࡲࠦṧ"),
  bstack1ll1lll_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢṨ"),
  bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥṩ")
]
bstack11ll11lll_opy_ = {
  bstack1ll1lll_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࠣṪ"): [bstack1ll1lll_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤṫ")],
  bstack1ll1lll_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣṬ"): [bstack1ll1lll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤṭ")],
  bstack1ll1lll_opy_ (u"ࠨࡡࡶࡶࡲࠦṮ"): [bstack1ll1lll_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦṯ"), bstack1ll1lll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦṰ"), bstack1ll1lll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨṱ"), bstack1ll1lll_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤṲ")],
  bstack1ll1lll_opy_ (u"ࠦࡲࡧ࡮ࡶࡣ࡯ࠦṳ"): [bstack1ll1lll_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧṴ")],
  bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣṵ"): [bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤṶ")],
}
bstack111l11l1l1l_opy_ = {
  bstack1ll1lll_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢṷ"): bstack1ll1lll_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࠣṸ"),
  bstack1ll1lll_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢṹ"): bstack1ll1lll_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣṺ"),
  bstack1ll1lll_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡇ࡯ࡩࡲ࡫࡮ࡵࠤṻ"): bstack1ll1lll_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࠣṼ"),
  bstack1ll1lll_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡅࡨࡺࡩࡷࡧࡈࡰࡪࡳࡥ࡯ࡶࠥṽ"): bstack1ll1lll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࠥṾ"),
  bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦṿ"): bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧẀ")
}
bstack1llll1ll11l_opy_ = {
  bstack1ll1lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨẁ"): bstack1ll1lll_opy_ (u"࡙ࠬࡵࡪࡶࡨࠤࡘ࡫ࡴࡶࡲࠪẂ"),
  bstack1ll1lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩẃ"): bstack1ll1lll_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࠦࡔࡦࡣࡵࡨࡴࡽ࡮ࠨẄ"),
  bstack1ll1lll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ẅ"): bstack1ll1lll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡔࡧࡷࡹࡵ࠭Ẇ"),
  bstack1ll1lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧẇ"): bstack1ll1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡗࡩࡦࡸࡤࡰࡹࡱࠫẈ")
}
bstack111l1l1l1ll_opy_ = 65536
bstack111l1111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠬ࠴࠮࠯࡝ࡗࡖ࡚ࡔࡃࡂࡖࡈࡈࡢ࠭ẉ")
bstack111l111l1l1_opy_ = [
      bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨẊ"), bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪẋ"), bstack1ll1lll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫẌ"), bstack1ll1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ẍ"), bstack1ll1lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬẎ"),
      bstack1ll1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧẏ"), bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨẐ"), bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧẑ"), bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨẒ"),
      bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡓࡧ࡭ࡦࠩẓ"), bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫẔ"), bstack1ll1lll_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ẕ")
    ]
bstack111l11l1ll1_opy_= {
  bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨẖ"): bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩẗ"),
  bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪẘ"): bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫẙ"),
  bstack1ll1lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧẚ"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ẛ"),
  bstack1ll1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪẜ"): bstack1ll1lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫẝ"),
  bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨẞ"): bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩẟ"),
  bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩẠ"): bstack1ll1lll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪạ"),
  bstack1ll1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬẢ"): bstack1ll1lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ả"),
  bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨẤ"): bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩấ"),
  bstack1ll1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩẦ"): bstack1ll1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪầ"),
  bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭Ẩ"): bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧẩ"),
  bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧẪ"): bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨẫ"),
  bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࠬẬ"): bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭ậ"),
  bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫẮ"): bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬắ"),
  bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩẰ"): bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࡒࡴࡹ࡯࡯࡯ࡵࠪằ"),
  bstack1ll1lll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭Ẳ"): bstack1ll1lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧẳ"),
  bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪẴ"): bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩẵ"),
  bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪẶ"): bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫặ"),
  bstack1ll1lll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧẸ"): bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨẹ"),
  bstack1ll1lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫẺ"): bstack1ll1lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬẻ"),
  bstack1ll1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Ẽ"): bstack1ll1lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧẽ"),
  bstack1ll1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬẾ"): bstack1ll1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ế"),
  bstack1ll1lll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭Ề"): bstack1ll1lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧề"),
  bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ể"): bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧể"),
  bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨỄ"): bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩễ"),
  bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧỆ"): bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨệ"),
  bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩỈ"): bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪỉ"),
  bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫỊ"): bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬị"),
  bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩỌ"): bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪọ")
}
bstack111l11l1111_opy_ = [bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫỎ"), bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫỏ")]
bstack11l1l111_opy_ = (bstack1ll1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨỐ"),)
bstack111l11l1l11_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡶࡲࡧࡥࡹ࡫࡟ࡤ࡮࡬ࠫố")
bstack11l1l11ll1_opy_ = bstack1ll1lll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳࡬ࡸࡩࡥࡵ࠲ࠦỒ")
bstack111l11ll11_opy_ = bstack1ll1lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫ࡷ࡯ࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡧࡳࡩࡤࡲࡥࡷࡪ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࠣồ")
bstack1l11lllll_opy_ = bstack1ll1lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠦỔ")
class EVENTS(Enum):
  bstack111l1111l11_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡱ࠴࠵ࡾࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨổ")
  bstack11ll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰࡪࡧ࡮ࡶࡲࠪỖ")
  bstack111llll1l1_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡪ࡮ࡴࡡ࡭࡫ࡽࡩࠬỗ")
  bstack111l1l111l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫࡮ࡥ࡮ࡲ࡫ࡸ࠭Ộ")
  bstack11l11111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮ࠫộ") #shift post bstack111l1l1l1l1_opy_
  bstack1l11l1l1ll_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪỚ") #shift post bstack111l1l1l1l1_opy_
  bstack111l1l11ll1_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸ࡭ࡻࡢࠨớ") #shift
  bstack111l111ll11_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡥࡱࡺࡲࡱࡵࡡࡥࠩỜ") #shift
  bstack1l11ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪࡀࡨࡶࡤ࠰ࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠧờ")
  bstack1l1l11l11l1_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡵࡤࡺࡪ࠳ࡲࡦࡵࡸࡰࡹࡹࠧỞ")
  bstack11llll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡧࡶ࡮ࡼࡥࡳ࠯ࡳࡩࡷ࡬࡯ࡳ࡯ࡶࡧࡦࡴࠧở")
  bstack11ll1lll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺࡭ࡱࡦࡥࡱ࠭Ỡ") #shift
  bstack11l11l11l_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡧࡰࡱ࠯ࡸࡴࡱࡵࡡࡥࠩỡ") #shift
  bstack11111ll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡦ࡭࠲ࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠨỢ")
  bstack1l1ll1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡧࡦࡶ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠰ࡶࡪࡹࡵ࡭ࡶࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠬợ") #shift
  bstack1l1ll11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷࠬỤ") #shift
  bstack111l1l11l11_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺࠩụ") #shift
  bstack11llll1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧỦ")
  bstack11l1ll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡵࡷࡥࡹࡻࡳࠨủ") #shift
  bstack1lll1l11ll_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡪࡸࡦ࠲ࡳࡡ࡯ࡣࡪࡩࡲ࡫࡮ࡵࠩỨ")
  bstack111l1111ll1_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡴࡲࡼࡾ࠳ࡳࡦࡶࡸࡴࠬứ") #shift
  bstack111lll1l11_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡸࡺࡶࠧỪ")
  bstack111l111l11l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡵࡱࡥࡵࡹࡨࡰࡶࠪừ") # not bstack111l111ll1l_opy_ in python
  bstack1lll1ll111_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡵࡺ࡯ࡴࠨỬ") # used in bstack111l111llll_opy_
  bstack11l111l11ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡸࡥ࠮ࡳࡸ࡭ࡹ࠭ử")
  bstack11l111l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰ࡵࡺ࡯ࡴࠨỮ")
  bstack111ll1l11_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡧࡦࡶࠪữ") # used in bstack111l111llll_opy_
  bstack1l11lll11l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡩࡱࡲ࡯ࠬỰ")
  bstack11l11l1llll_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡩ࠲࡮࡯ࡰ࡭ࠪự")
  bstack11l11l1ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡳࡸࡺ࠭ࡩࡱࡲ࡯ࠬỲ")
  bstack1l1l1l11l1_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠫỳ")
  bstack111l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭ࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠫỴ") #
  bstack111111ll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡸࡦࡱࡥࡔࡥࡵࡩࡪࡴࡓࡩࡱࡷࠫỵ")
  bstack111l11111l_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫỶ")
  bstack11ll1111_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡴࡨ࠱ࡹ࡫ࡳࡵࠩỷ")
  bstack111l11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡲࡷࡹ࠳ࡴࡦࡵࡷࠫỸ")
  bstack1l1l1111l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡶࡪ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧỹ") #shift
  bstack11ll1l1ll_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩỺ") #shift
  bstack111l1l1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࠯ࡦࡥࡵࡺࡵࡳࡧࠪỻ")
  bstack111l11ll111_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡪࡦ࡯ࡩ࠲ࡺࡩ࡮ࡧࡲࡹࡹ࠭Ỽ")
  bstack11111l11ll_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡥࡹ࡫ࡷ࠱࡭ࡧ࡮ࡥ࡮ࡨࡶࠬỽ")
  bstack1ll111ll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡪࡾࡩࡵ࠯࡫ࡥࡳࡪ࡬ࡦࡴࠪỾ")
  bstack111l1l1l111_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩ࠳࡭ࡦࡶࡵ࡭ࡨࡹࠧỿ")
  bstack111l11l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡨࡶࡤ࠽ࡷࡹࡵࡰࠨἀ")
  bstack1ll111l1ll1_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡴࡶࡤࡶࡹ࠭ἁ")
  bstack111l11ll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪἂ")
  bstack111l1l111ll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡦ࡬ࡪࡩ࡫࠮ࡷࡳࡨࡦࡺࡥࠨἃ")
  bstack1l1l1ll11l1_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡢࡰࡱࡷࡷࡹࡸࡡࡱࠩἄ")
  bstack1l1ll11llll_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡴࡶࡤࡶࡹࡨࡩ࡯ࡣࡵࡽࠬἅ")
  bstack1l1lll1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡥࡲࡲࡳ࡫ࡣࡵࠩἆ")
  bstack1l1l1ll1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡶࡸࡴࡶࠧἇ")
  bstack1ll111l111l_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡹࡧࡲࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲࠬἈ")
  bstack1ll111l1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡵ࡮࡯ࡧࡦࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࠨἉ")
  bstack111l11l111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶࡎࡴࡩࡵࠩἊ")
  bstack111l11lll11_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡦࡪࡰࡧࡒࡪࡧࡲࡦࡵࡷࡌࡺࡨࠧἋ")
  bstack11ll11ll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࡏ࡮ࡪࡶࠪἌ")
  bstack11ll1l1l1ll_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡵࡸࠬἍ")
  bstack1l11ll11l11_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡅࡲࡲ࡫࡯ࡧࠨἎ")
  bstack111l1l1ll11_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡆࡳࡳ࡬ࡩࡨࠩἏ")
  bstack1l11l1l1111_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࡯ࡓࡦ࡮ࡩࡌࡪࡧ࡬ࡔࡶࡨࡴࠬἐ")
  bstack1l11l1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡩࡔࡧ࡯ࡪࡍ࡫ࡡ࡭ࡉࡨࡸࡗ࡫ࡳࡶ࡮ࡷࠫἑ")
  bstack1l111111l11_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࡋࡶࡦࡰࡷࠫἒ")
  bstack1l111llll11_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡊࡼࡥ࡯ࡶࠪἓ")
  bstack1l111l1l111_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡲ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࡇࡹࡩࡳࡺࠧἔ")
  bstack111l11llll1_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡥ࡯ࡳࡸࡩࡺ࡫ࡔࡦࡵࡷࡉࡻ࡫࡮ࡵࠩἕ")
  bstack11ll11ll1l1_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡳࡵ࠭἖")
  bstack1l1llll11ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮࠾ࡴࡴࡓࡵࡱࡳࠫ἗")
  bstack111lllllll1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡦࡣࡱࡹࡵ࡛ࡰ࡭ࡱࡤࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠩἘ")
  bstack1l1lll11l1_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡰࡧࡊࡺࡴ࡮ࡦ࡮ࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩἙ")
  bstack1ll1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡱࡨࡋࡻ࡮࡯ࡧ࡯ࡘࡪࡹࡴࡄࡱࡰࡴࡱ࡫ࡴࡦࡦࠪἚ")
  bstack1lll1l1111l_opy_ = bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡳࡴࡱࡿࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡖࡹࡵࡧࡶࡸࠬἛ")
  bstack1lll1111ll1_opy_ = bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡴࡩࡥࡴࡵࡄࡶ࡬ࡹࡐࡺࡶࡨࡷࡹ࠭Ἔ")
  bstack1lll11l1111_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡾࡺࡥࡴࡶࡊࡩࡹ࡚࡯ࡵࡣ࡯ࡘࡪࡹࡴࡴࠩἝ")
class STAGE(Enum):
  bstack11l11l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭἞")
  END = bstack1ll1lll_opy_ (u"ࠨࡧࡱࡨࠬ἟")
  bstack1ll1llll_opy_ = bstack1ll1lll_opy_ (u"ࠩࡶ࡭ࡳ࡭࡬ࡦࠩἠ")
bstack111l111lll_opy_ = {
  bstack1ll1lll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࠪἡ"): bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫἢ"),
  bstack1ll1lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩἣ"): bstack1ll1lll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨἤ")
}
PLAYWRIGHT_HUB_URL = bstack1ll1lll_opy_ (u"ࠢࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠤἥ")
bstack11l1111lll_opy_ = {bstack1ll1lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨἦ"), bstack1ll1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫἧ"), bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩἨ")}
MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION = 98
bstack1l11lll1ll1_opy_ = 100
bstack11l1111lll_opy_ = (bstack1ll1lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫἩ"), bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠯ࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫἪ"), bstack1ll1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠨἫ"))
bstack1lll111l11l_opy_ = {
  bstack1ll1lll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠭Ἤ"): bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡶࡪࡸࡵ࡯ࡵࠪἭ"),
  bstack1ll1lll_opy_ (u"ࠩࡧࡩࡱࡧࡹࠨἮ"): bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡸࡥࡳࡷࡱࡷ࠲ࡪࡥ࡭ࡣࡼࠫἯ"),
  bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰ࠰ࡨࡪࡲࡡࡺࠩἰ"): 0
}
bstack111l11ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧἱ")
bstack111l111l1ll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡶࡲ࡯ࡳࡦࡪ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥἲ")
bstack11l11lll11_opy_ = bstack1ll1lll_opy_ (u"ࠢࡕࡇࡖࡘࠥࡘࡅࡑࡑࡕࡘࡎࡔࡇࠡࡃࡑࡈࠥࡇࡎࡂࡎ࡜ࡘࡎࡉࡓࠣἳ")