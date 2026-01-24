# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import re
from enum import Enum
bstack11lll11l_opy_ = {
  bstack1l1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᢨ"): bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴᢩࠪ"),
  bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᢪ"): bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫ᢫"),
  bstack1l1111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᢬"): bstack1l1111_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᢭"),
  bstack1l1111_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ᢮"): bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬ᢯"),
  bstack1l1111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᢰ"): bstack1l1111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨᢱ"),
  bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᢲ"): bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨᢳ"),
  bstack1l1111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᢴ"): bstack1l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᢵ"),
  bstack1l1111_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᢶ"): bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫᢷ"),
  bstack1l1111_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬᢸ"): bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨᢹ"),
  bstack1l1111_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᢺ"): bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᢻ"),
  bstack1l1111_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᢼ"): bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᢽ"),
  bstack1l1111_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬᢾ"): bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬᢿ"),
  bstack1l1111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᣀ"): bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᣁ"),
  bstack1l1111_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᣂ"): bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᣃ"),
  bstack1l1111_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᣄ"): bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᣅ"),
  bstack1l1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᣆ"): bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᣇ"),
  bstack1l1111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᣈ"): bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᣉ"),
  bstack1l1111_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪᣊ"): bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪᣋ"),
  bstack1l1111_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᣌ"): bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᣍ"),
  bstack1l1111_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᣎ"): bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᣏ"),
  bstack1l1111_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬᣐ"): bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬᣑ"),
  bstack1l1111_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᣒ"): bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᣓ"),
  bstack1l1111_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ᣔ"): bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭ᣕ"),
  bstack1l1111_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪᣖ"): bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪᣗ"),
  bstack1l1111_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᣘ"): bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᣙ"),
  bstack1l1111_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᣚ"): bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᣛ"),
  bstack1l1111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᣜ"): bstack1l1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᣝ"),
  bstack1l1111_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᣞ"): bstack1l1111_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩᣟ"),
  bstack1l1111_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᣠ"): bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᣡ"),
  bstack1l1111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᣢ"): bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᣣ"),
  bstack1l1111_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᣤ"): bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᣥ"),
  bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪᣦ"): bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ᣧ"),
  bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᣨ"): bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᣩ"),
  bstack1l1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᣪ"): bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨᣫ"),
  bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᣬ"): bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᣭ"),
  bstack1l1111_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᣮ"): bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᣯ"),
  bstack1l1111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᣰ"): bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᣱ"),
  bstack1l1111_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᣲ"): bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᣳ"),
  bstack1l1111_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᣴ"): bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩᣵ"),
  bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᣶"): bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᣷"),
  bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᣸"): bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᣹")
}
bstack11l11l111l1_opy_ = [
  bstack1l1111_opy_ (u"ࠪࡳࡸ࠭᣺"),
  bstack1l1111_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ᣻"),
  bstack1l1111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᣼"),
  bstack1l1111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᣽"),
  bstack1l1111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ᣾"),
  bstack1l1111_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬ᣿"),
  bstack1l1111_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᤀ"),
]
bstack1l1lll1l1_opy_ = {
  bstack1l1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᤁ"): [bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᤂ"), bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡑࡅࡒࡋࠧᤃ")],
  bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᤄ"): bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᤅ"),
  bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᤆ"): bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬᤇ"),
  bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᤈ"): bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠩᤉ"),
  bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᤊ"): bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᤋ"),
  bstack1l1111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᤌ"): bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡕࡢࡔࡊࡘ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩᤍ"),
  bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᤎ"): bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨᤏ"),
  bstack1l1111_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᤐ"): bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩᤑ"),
  bstack1l1111_opy_ (u"࠭ࡡࡱࡲࠪᤒ"): [bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࡢࡍࡉ࠭ᤓ"), bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࠫᤔ")],
  bstack1l1111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᤕ"): bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡌࡐࡉࡏࡉ࡛ࡋࡌࠨᤖ"),
  bstack1l1111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᤗ"): bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᤘ"),
  bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᤙ"): [bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠫᤚ"), bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨᤛ")],
  bstack1l1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᤜ"): bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗ࡙ࡗࡈࡏࡔࡅࡄࡐࡊ࠭ᤝ"),
  bstack1l1111_opy_ (u"ࠫࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡋࡎࡗࠩᤞ"): bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡔࡘࡃࡉࡇࡖࡘࡗࡇࡔࡊࡑࡑࡣࡘࡓࡁࡓࡖࡢࡗࡊࡒࡅࡄࡖࡌࡓࡓࡥࡆࡆࡃࡗ࡙ࡗࡋ࡟ࡃࡔࡄࡒࡈࡎࡅࡔࠩ᤟")
}
bstack1l11l11ll1_opy_ = {
  bstack1l1111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᤠ"): [bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᤡ"), bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᤢ")],
  bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᤣ"): [bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡡ࡮ࡩࡾ࠭ᤤ"), bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᤥ")],
  bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᤦ"): bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᤧ"),
  bstack1l1111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᤨ"): bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᤩ"),
  bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᤪ"): bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᤫ"),
  bstack1l1111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ᤬"): [bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡶࡰࠨ᤭"), bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ᤮")],
  bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᤯"): bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᤰ"),
  bstack1l1111_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᤱ"): bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᤲ"),
  bstack1l1111_opy_ (u"ࠫࡦࡶࡰࠨᤳ"): bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࠨᤴ"),
  bstack1l1111_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᤵ"): bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᤶ"),
  bstack1l1111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᤷ"): bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᤸ"),
  bstack1l1111_opy_ (u"ࠥࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡈࡒࡉ᤹ࠣ"): bstack1l1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࠤ᤺"),
}
bstack111lll1ll_opy_ = {
  bstack1l1111_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᤻"): bstack1l1111_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ᤼"),
  bstack1l1111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᤽"): [bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᤾"), bstack1l1111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᤿")],
  bstack1l1111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᥀"): bstack1l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᥁"),
  bstack1l1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ᥂"): bstack1l1111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭᥃"),
  bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᥄"): [bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ᥅"), bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨ᥆")],
  bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᥇"): bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᥈"),
  bstack1l1111_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ᥉"): bstack1l1111_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫ᥊"),
  bstack1l1111_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᥋"): [bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᥌"), bstack1l1111_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᥍")],
  bstack1l1111_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩ᥎"): [bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬ᥏"), bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬᥐ")]
}
bstack11l11l1l11_opy_ = [
  bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᥑ"),
  bstack1l1111_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪᥒ"),
  bstack1l1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧᥓ"),
  bstack1l1111_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩᥔ"),
  bstack1l1111_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬᥕ"),
  bstack1l1111_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩᥖ"),
  bstack1l1111_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨᥗ"),
  bstack1l1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᥘ"),
  bstack1l1111_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬᥙ"),
  bstack1l1111_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᥚ"),
  bstack1l1111_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᥛ"),
  bstack1l1111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫᥜ"),
]
bstack1ll1l11ll_opy_ = [
  bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᥝ"),
  bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᥞ"),
  bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᥟ"),
  bstack1l1111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᥠ"),
  bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᥡ"),
  bstack1l1111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᥢ"),
  bstack1l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᥣ"),
  bstack1l1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᥤ"),
  bstack1l1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᥥ"),
  bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᥦ"),
  bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᥧ"),
  bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨᥨ"),
  bstack1l1111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᥩ"),
  bstack1l1111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡗࡥ࡬࠭ᥪ"),
  bstack1l1111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᥫ"),
  bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᥬ"),
  bstack1l1111_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪᥭ"),
  bstack1l1111_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠶࠭᥮"),
  bstack1l1111_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠸ࠧ᥯"),
  bstack1l1111_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠳ࠨᥰ"),
  bstack1l1111_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠵ࠩᥱ"),
  bstack1l1111_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠷ࠪᥲ"),
  bstack1l1111_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠹ࠫᥳ"),
  bstack1l1111_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠻ࠬᥴ"),
  bstack1l1111_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠽࠭᥵"),
  bstack1l1111_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠿ࠧ᥶"),
  bstack1l1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ᥷"),
  bstack1l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᥸"),
  bstack1l1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ᥹"),
  bstack1l1111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ᥺"),
  bstack1l1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᥻"),
  bstack1l1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᥼"),
  bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ᥽"),
  bstack1l1111_opy_ (u"ࠩ࡫ࡹࡧࡘࡥࡨ࡫ࡲࡲࠬ᥾")
]
bstack11l1111l11l_opy_ = [
  bstack1l1111_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨ᥿"),
  bstack1l1111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᦀ"),
  bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᦁ"),
  bstack1l1111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᦂ"),
  bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡕࡸࡩࡰࡴ࡬ࡸࡾ࠭ᦃ"),
  bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᦄ"),
  bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡕࡣࡪࠫᦅ"),
  bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᦆ"),
  bstack1l1111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᦇ"),
  bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᦈ"),
  bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᦉ"),
  bstack1l1111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᦊ"),
  bstack1l1111_opy_ (u"ࠨࡱࡶࠫᦋ"),
  bstack1l1111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᦌ"),
  bstack1l1111_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩᦍ"),
  bstack1l1111_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ᦎ"),
  bstack1l1111_opy_ (u"ࠬࡸࡥࡨ࡫ࡲࡲࠬᦏ"),
  bstack1l1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨᦐ"),
  bstack1l1111_opy_ (u"ࠧ࡮ࡣࡦ࡬࡮ࡴࡥࠨᦑ"),
  bstack1l1111_opy_ (u"ࠨࡴࡨࡷࡴࡲࡵࡵ࡫ࡲࡲࠬᦒ"),
  bstack1l1111_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧᦓ"),
  bstack1l1111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧᦔ"),
  bstack1l1111_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪᦕ"),
  bstack1l1111_opy_ (u"ࠬࡴ࡯ࡑࡣࡪࡩࡑࡵࡡࡥࡖ࡬ࡱࡪࡵࡵࡵࠩᦖ"),
  bstack1l1111_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧᦗ"),
  bstack1l1111_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᦘ"),
  bstack1l1111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᦙ"),
  bstack1l1111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡨࡲࡩࡑࡥࡺࡵࠪᦚ"),
  bstack1l1111_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᦛ"),
  bstack1l1111_opy_ (u"ࠫࡳࡵࡐࡪࡲࡨࡰ࡮ࡴࡥࠨᦜ"),
  bstack1l1111_opy_ (u"ࠬࡩࡨࡦࡥ࡮࡙ࡗࡒࠧᦝ"),
  bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᦞ"),
  bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡃࡰࡱ࡮࡭ࡪࡹࠧᦟ"),
  bstack1l1111_opy_ (u"ࠨࡥࡤࡴࡹࡻࡲࡦࡅࡵࡥࡸ࡮ࠧᦠ"),
  bstack1l1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᦡ"),
  bstack1l1111_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᦢ"),
  bstack1l1111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᦣ"),
  bstack1l1111_opy_ (u"ࠬࡴ࡯ࡃ࡮ࡤࡲࡰࡖ࡯࡭࡮࡬ࡲ࡬࠭ᦤ"),
  bstack1l1111_opy_ (u"࠭࡭ࡢࡵ࡮ࡗࡪࡴࡤࡌࡧࡼࡷࠬᦥ"),
  bstack1l1111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡌࡰࡩࡶࠫᦦ"),
  bstack1l1111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡊࡦࠪᦧ"),
  bstack1l1111_opy_ (u"ࠩࡧࡩࡩ࡯ࡣࡢࡶࡨࡨࡉ࡫ࡶࡪࡥࡨࠫᦨ"),
  bstack1l1111_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡓࡥࡷࡧ࡭ࡴࠩᦩ"),
  bstack1l1111_opy_ (u"ࠫࡵ࡮࡯࡯ࡧࡑࡹࡲࡨࡥࡳࠩᦪ"),
  bstack1l1111_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪᦫ"),
  bstack1l1111_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡓࡵࡺࡩࡰࡰࡶࠫ᦬"),
  bstack1l1111_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬ᦭"),
  bstack1l1111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ᦮"),
  bstack1l1111_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭᦯"),
  bstack1l1111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡅ࡭ࡴࡳࡥࡵࡴ࡬ࡧࠬᦰ"),
  bstack1l1111_opy_ (u"ࠫࡻ࡯ࡤࡦࡱ࡙࠶ࠬᦱ"),
  bstack1l1111_opy_ (u"ࠬࡳࡩࡥࡕࡨࡷࡸ࡯࡯࡯ࡋࡱࡷࡹࡧ࡬࡭ࡃࡳࡴࡸ࠭ᦲ"),
  bstack1l1111_opy_ (u"࠭ࡥࡴࡲࡵࡩࡸࡹ࡯ࡔࡧࡵࡺࡪࡸࠧᦳ"),
  bstack1l1111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᦴ"),
  bstack1l1111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡆࡨࡵ࠭ᦵ"),
  bstack1l1111_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᦶ"),
  bstack1l1111_opy_ (u"ࠪࡷࡾࡴࡣࡕ࡫ࡰࡩ࡜࡯ࡴࡩࡐࡗࡔࠬᦷ"),
  bstack1l1111_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᦸ"),
  bstack1l1111_opy_ (u"ࠬ࡭ࡰࡴࡎࡲࡧࡦࡺࡩࡰࡰࠪᦹ"),
  bstack1l1111_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧᦺ"),
  bstack1l1111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᦻ"),
  bstack1l1111_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࡃࡩࡣࡱ࡫ࡪࡐࡡࡳࠩᦼ"),
  bstack1l1111_opy_ (u"ࠩࡻࡱࡸࡐࡡࡳࠩᦽ"),
  bstack1l1111_opy_ (u"ࠪࡼࡲࡾࡊࡢࡴࠪᦾ"),
  bstack1l1111_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪᦿ"),
  bstack1l1111_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬᧀ"),
  bstack1l1111_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧᧁ"),
  bstack1l1111_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪᧂ"),
  bstack1l1111_opy_ (u"ࠨࡣࡳࡴ࡛࡫ࡲࡴ࡫ࡲࡲࠬᧃ"),
  bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᧄ"),
  bstack1l1111_opy_ (u"ࠪࡶࡪࡹࡩࡨࡰࡄࡴࡵ࠭ᧅ"),
  bstack1l1111_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࡳࠨᧆ"),
  bstack1l1111_opy_ (u"ࠬࡩࡡ࡯ࡣࡵࡽࠬᧇ"),
  bstack1l1111_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᧈ"),
  bstack1l1111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᧉ"),
  bstack1l1111_opy_ (u"ࠨ࡫ࡨࠫ᧊"),
  bstack1l1111_opy_ (u"ࠩࡨࡨ࡬࡫ࠧ᧋"),
  bstack1l1111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ᧌"),
  bstack1l1111_opy_ (u"ࠫࡶࡻࡥࡶࡧࠪ᧍"),
  bstack1l1111_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡲࡦࡲࠧ᧎"),
  bstack1l1111_opy_ (u"࠭ࡡࡱࡲࡖࡸࡴࡸࡥࡄࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠧ᧏"),
  bstack1l1111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡃࡢ࡯ࡨࡶࡦࡏ࡭ࡢࡩࡨࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭᧐"),
  bstack1l1111_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡋࡸࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫ᧑"),
  bstack1l1111_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡉ࡯ࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬ᧒"),
  bstack1l1111_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧ᧓"),
  bstack1l1111_opy_ (u"ࠫࡷ࡫ࡳࡦࡴࡹࡩࡉ࡫ࡶࡪࡥࡨࠫ᧔"),
  bstack1l1111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ᧕"),
  bstack1l1111_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨ᧖"),
  bstack1l1111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡢࡵࡶࡧࡴࡪࡥࠨ᧗"),
  bstack1l1111_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡊࡱࡶࡈࡪࡼࡩࡤࡧࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ᧘"),
  bstack1l1111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡸࡨ࡮ࡵࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩ᧙"),
  bstack1l1111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡴࡵࡲࡥࡑࡣࡼࠫ᧚"),
  bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ᧛"),
  bstack1l1111_opy_ (u"ࠬࡽࡤࡪࡱࡖࡩࡷࡼࡩࡤࡧࠪ᧜"),
  bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᧝"),
  bstack1l1111_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡄࡴࡲࡷࡸ࡙ࡩࡵࡧࡗࡶࡦࡩ࡫ࡪࡰࡪࠫ᧞"),
  bstack1l1111_opy_ (u"ࠨࡪ࡬࡫࡭ࡉ࡯࡯ࡶࡵࡥࡸࡺࠧ᧟"),
  bstack1l1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡒࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࡸ࠭᧠"),
  bstack1l1111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭᧡"),
  bstack1l1111_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨ᧢"),
  bstack1l1111_opy_ (u"ࠬࡸࡥ࡮ࡱࡹࡩࡎࡕࡓࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࡑࡵࡣࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪ᧣"),
  bstack1l1111_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨ᧤"),
  bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᧥"),
  bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᧦"),
  bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᧧"),
  bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᧨"),
  bstack1l1111_opy_ (u"ࠫࡵࡧࡧࡦࡎࡲࡥࡩ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧ᧩"),
  bstack1l1111_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ᧪"),
  bstack1l1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࡳࠨ᧫"),
  bstack1l1111_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪ᧬")
]
bstack1ll11l11_opy_ = {
  bstack1l1111_opy_ (u"ࠨࡸࠪ᧭"): bstack1l1111_opy_ (u"ࠩࡹࠫ᧮"),
  bstack1l1111_opy_ (u"ࠪࡪࠬ᧯"): bstack1l1111_opy_ (u"ࠫ࡫࠭᧰"),
  bstack1l1111_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫ᧱"): bstack1l1111_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬ᧲"),
  bstack1l1111_opy_ (u"ࠧࡰࡰ࡯ࡽࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᧳"): bstack1l1111_opy_ (u"ࠨࡱࡱࡰࡾࡇࡵࡵࡱࡰࡥࡹ࡫ࠧ᧴"),
  bstack1l1111_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭᧵"): bstack1l1111_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧ᧶"),
  bstack1l1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧ᧷"): bstack1l1111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ᧸"),
  bstack1l1111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩ᧹"): bstack1l1111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪ᧺"),
  bstack1l1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫ᧻"): bstack1l1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ᧼"),
  bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭᧽"): bstack1l1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧ᧾"),
  bstack1l1111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭᧿"): bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᨀ"),
  bstack1l1111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨᨁ"): bstack1l1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩᨂ"),
  bstack1l1111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᨃ"): bstack1l1111_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᨄ"),
  bstack1l1111_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᨅ"): bstack1l1111_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᨆ"),
  bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᨇ"): bstack1l1111_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᨈ"),
  bstack1l1111_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᨉ"): bstack1l1111_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫᨊ"),
  bstack1l1111_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧᨋ"): bstack1l1111_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨᨌ"),
  bstack1l1111_opy_ (u"ࠬࡶࡡࡤࡨ࡬ࡰࡪ࠭ᨍ"): bstack1l1111_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᨎ"),
  bstack1l1111_opy_ (u"ࠧࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᨏ"): bstack1l1111_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᨐ"),
  bstack1l1111_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᨑ"): bstack1l1111_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᨒ"),
  bstack1l1111_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬᨓ"): bstack1l1111_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭ᨔ"),
  bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᨕ"): bstack1l1111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᨖ"),
  bstack1l1111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠪᨗ"): bstack1l1111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡴࡪࡧࡴࡦࡴᨘࠪ")
}
bstack11l111l11l1_opy_ = bstack1l1111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬࡯ࡴࡩࡷࡥ࠲ࡨࡵ࡭࠰ࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬࠳ࡷ࡫࡬ࡦࡣࡶࡩࡸ࠵࡬ࡢࡶࡨࡷࡹ࠵ࡤࡰࡹࡱࡰࡴࡧࡤࠣᨙ")
bstack11l11l11lll_opy_ = bstack1l1111_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠳࡭࡫ࡡ࡭ࡶ࡫ࡧ࡭࡫ࡣ࡬ࠤᨚ")
bstack1111ll11l_opy_ = bstack1l1111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡥࡥࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡳࡦࡰࡧࡣࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣᨛ")
bstack1l1l1l1ll1_opy_ = bstack1l1111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧ᨜")
bstack111ll11l_opy_ = bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪ᨝")
bstack1l1ll11lll_opy_ = bstack1l1111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬ᨞")
bstack111l111l1_opy_ = {
  bstack1l1111_opy_ (u"ࠩࡧࡩ࡫ࡧࡵ࡭ࡶࠪ᨟"): bstack1l1111_opy_ (u"ࠪ࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᨠ"),
  bstack1l1111_opy_ (u"ࠫࡺࡹ࠭ࡦࡣࡶࡸࠬᨡ"): bstack1l1111_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡸࡷࡪ࠳࡯࡯࡮ࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᨢ"),
  bstack1l1111_opy_ (u"࠭ࡵࡴࠩᨣ"): bstack1l1111_opy_ (u"ࠧࡩࡷࡥ࠱ࡺࡹ࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᨤ"),
  bstack1l1111_opy_ (u"ࠨࡧࡸࠫᨥ"): bstack1l1111_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡥࡶ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᨦ"),
  bstack1l1111_opy_ (u"ࠪ࡭ࡳ࠭ᨧ"): bstack1l1111_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡣࡳࡷ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᨨ"),
  bstack1l1111_opy_ (u"ࠬࡧࡵࠨᨩ"): bstack1l1111_opy_ (u"࠭ࡨࡶࡤ࠰ࡥࡵࡹࡥ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᨪ")
}
bstack11l11l11l1l_opy_ = {
  bstack1l1111_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩᨫ"): 50,
  bstack1l1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᨬ"): 40,
  bstack1l1111_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᨭ"): 30,
  bstack1l1111_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᨮ"): 20,
  bstack1l1111_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᨯ"): 10
}
bstack1lllll11_opy_ = bstack11l11l11l1l_opy_[bstack1l1111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᨰ")]
bstack111llll111_opy_ = bstack1l1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᨱ")
bstack11llll11ll_opy_ = bstack1l1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᨲ")
bstack1ll11llll_opy_ = bstack1l1111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᨳ")
bstack11ll1111ll_opy_ = bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᨴ")
bstack11l1l1111l_opy_ = bstack1l1111_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡦࡴࡤࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡴࡦࡩ࡫ࡢࡩࡨࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡠࠨᨵ")
bstack11l11l111_opy_ = {
  bstack1l1111_opy_ (u"ࠫࡘࡊࡋ࠮ࡉࡈࡒ࠲࠶࠰࠶ࠩᨶ"): bstack1l1111_opy_ (u"ࠬ࠰ࠪࠫࠢ࡞ࡗࡉࡑ࠭ࡈࡇࡑ࠱࠵࠶࠵࡞ࠢࡣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࡥࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥ࡯࡮ࠡࡻࡲࡹࡷࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠲࡚ࠥࡨࡪࡵࠣࡱࡦࡿࠠࡤࡣࡸࡷࡪࠦࡣࡰࡰࡩࡰ࡮ࡩࡴࡴࠢࡺ࡭ࡹ࡮ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࠠࡪࡶࠣࡹࡸ࡯࡮ࡨ࠼ࠣࡴ࡮ࡶࠠࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࠥ࠰ࠪࠫࠩᨷ")
}
bstack11l1111l1l1_opy_ = [bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᨸ"), bstack1l1111_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᨹ")]
bstack11l111l1l11_opy_ = [bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᨺ"), bstack1l1111_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᨻ")]
bstack1l11ll111_opy_ = re.compile(bstack1l1111_opy_ (u"ࠪࡢࡠࡢ࡜ࡸ࠯ࡠ࠯࠿࠴ࠪࠥࠩᨼ"))
bstack1l111ll11_opy_ = [
  bstack1l1111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡏࡣࡰࡩࠬᨽ"),
  bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᨾ"),
  bstack1l1111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᨿ"),
  bstack1l1111_opy_ (u"ࠧ࡯ࡧࡺࡇࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࠫᩀ"),
  bstack1l1111_opy_ (u"ࠨࡣࡳࡴࠬᩁ"),
  bstack1l1111_opy_ (u"ࠩࡸࡨ࡮ࡪࠧᩂ"),
  bstack1l1111_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬᩃ"),
  bstack1l1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࠫᩄ"),
  bstack1l1111_opy_ (u"ࠬࡵࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪᩅ"),
  bstack1l1111_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࠫᩆ"),
  bstack1l1111_opy_ (u"ࠧ࡯ࡱࡕࡩࡸ࡫ࡴࠨᩇ"), bstack1l1111_opy_ (u"ࠨࡨࡸࡰࡱࡘࡥࡴࡧࡷࠫᩈ"),
  bstack1l1111_opy_ (u"ࠩࡦࡰࡪࡧࡲࡔࡻࡶࡸࡪࡳࡆࡪ࡮ࡨࡷࠬᩉ"),
  bstack1l1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡖ࡬ࡱ࡮ࡴࡧࡴࠩᩊ"),
  bstack1l1111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࡍࡱࡪ࡫࡮ࡴࡧࠨᩋ"),
  bstack1l1111_opy_ (u"ࠬࡵࡴࡩࡧࡵࡅࡵࡶࡳࠨᩌ"),
  bstack1l1111_opy_ (u"࠭ࡰࡳ࡫ࡱࡸࡕࡧࡧࡦࡕࡲࡹࡷࡩࡥࡐࡰࡉ࡭ࡳࡪࡆࡢ࡫࡯ࡹࡷ࡫ࠧᩍ"),
  bstack1l1111_opy_ (u"ࠧࡢࡲࡳࡅࡨࡺࡩࡷ࡫ࡷࡽࠬᩎ"), bstack1l1111_opy_ (u"ࠨࡣࡳࡴࡕࡧࡣ࡬ࡣࡪࡩࠬᩏ"), bstack1l1111_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡄࡧࡹ࡯ࡶࡪࡶࡼࠫᩐ"), bstack1l1111_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡔࡦࡩ࡫ࡢࡩࡨࠫᩑ"), bstack1l1111_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭ᩒ"),
  bstack1l1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪᩓ"),
  bstack1l1111_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙࡫ࡳࡵࡒࡤࡧࡰࡧࡧࡦࡵࠪᩔ"),
  bstack1l1111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࠩᩕ"), bstack1l1111_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡅࡲࡺࡪࡸࡡࡨࡧࡈࡲࡩࡏ࡮ࡵࡧࡱࡸࠬᩖ"),
  bstack1l1111_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧᩗ"),
  bstack1l1111_opy_ (u"ࠪࡥࡩࡨࡐࡰࡴࡷࠫᩘ"),
  bstack1l1111_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡗࡴࡩ࡫ࡦࡶࠪᩙ"),
  bstack1l1111_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᩚ"),
  bstack1l1111_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡶ࡫ࠫᩛ"),
  bstack1l1111_opy_ (u"ࠧࡢࡸࡧࠫᩜ"), bstack1l1111_opy_ (u"ࠨࡣࡹࡨࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫᩝ"), bstack1l1111_opy_ (u"ࠩࡤࡺࡩࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫᩞ"), bstack1l1111_opy_ (u"ࠪࡥࡻࡪࡁࡳࡩࡶࠫ᩟"),
  bstack1l1111_opy_ (u"ࠫࡺࡹࡥࡌࡧࡼࡷࡹࡵࡲࡦ᩠ࠩ"), bstack1l1111_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡶ࡫ࠫᩡ"), bstack1l1111_opy_ (u"࠭࡫ࡦࡻࡶࡸࡴࡸࡥࡑࡣࡶࡷࡼࡵࡲࡥࠩᩢ"),
  bstack1l1111_opy_ (u"ࠧ࡬ࡧࡼࡅࡱ࡯ࡡࡴࠩᩣ"), bstack1l1111_opy_ (u"ࠨ࡭ࡨࡽࡕࡧࡳࡴࡹࡲࡶࡩ࠭ᩤ"),
  bstack1l1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࠫᩥ"), bstack1l1111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡃࡵ࡫ࡸ࠭ᩦ"), bstack1l1111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪࡊࡩࡳࠩᩧ"), bstack1l1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡇ࡭ࡸ࡯࡮ࡧࡐࡥࡵࡶࡩ࡯ࡩࡉ࡭ࡱ࡫ࠧᩨ"), bstack1l1111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶ࡚ࡹࡥࡔࡻࡶࡸࡪࡳࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪᩩ"),
  bstack1l1111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࠪᩪ"), bstack1l1111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡐࡰࡴࡷࡷࠬᩫ"),
  bstack1l1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡅ࡫ࡶࡥࡧࡲࡥࡃࡷ࡬ࡰࡩࡉࡨࡦࡥ࡮ࠫᩬ"),
  bstack1l1111_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࡕ࡫ࡰࡩࡴࡻࡴࠨᩭ"),
  bstack1l1111_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡅࡨࡺࡩࡰࡰࠪᩮ"), bstack1l1111_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡈࡧࡴࡦࡩࡲࡶࡾ࠭ᩯ"), bstack1l1111_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡌ࡬ࡢࡩࡶࠫᩰ"), bstack1l1111_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡡ࡭ࡋࡱࡸࡪࡴࡴࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᩱ"),
  bstack1l1111_opy_ (u"ࠨࡦࡲࡲࡹ࡙ࡴࡰࡲࡄࡴࡵࡕ࡮ࡓࡧࡶࡩࡹ࠭ᩲ"),
  bstack1l1111_opy_ (u"ࠩࡸࡲ࡮ࡩ࡯ࡥࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫᩳ"), bstack1l1111_opy_ (u"ࠪࡶࡪࡹࡥࡵࡍࡨࡽࡧࡵࡡࡳࡦࠪᩴ"),
  bstack1l1111_opy_ (u"ࠫࡳࡵࡓࡪࡩࡱࠫ᩵"),
  bstack1l1111_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩ࡚ࡴࡩ࡮ࡲࡲࡶࡹࡧ࡮ࡵࡘ࡬ࡩࡼࡹࠧ᩶"),
  bstack1l1111_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯ࡦࡵࡳ࡮ࡪࡗࡢࡶࡦ࡬ࡪࡸࡳࠨ᩷"),
  bstack1l1111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᩸"),
  bstack1l1111_opy_ (u"ࠨࡴࡨࡧࡷ࡫ࡡࡵࡧࡆ࡬ࡷࡵ࡭ࡦࡆࡵ࡭ࡻ࡫ࡲࡔࡧࡶࡷ࡮ࡵ࡮ࡴࠩ᩹"),
  bstack1l1111_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ᩺"),
  bstack1l1111_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡐࡢࡶ࡫ࠫ᩻"),
  bstack1l1111_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡘࡶࡥࡦࡦࠪ᩼"),
  bstack1l1111_opy_ (u"ࠬ࡭ࡰࡴࡇࡱࡥࡧࡲࡥࡥࠩ᩽"),
  bstack1l1111_opy_ (u"࠭ࡩࡴࡊࡨࡥࡩࡲࡥࡴࡵࠪ᩾"),
  bstack1l1111_opy_ (u"ࠧࡢࡦࡥࡉࡽ࡫ࡣࡕ࡫ࡰࡩࡴࡻࡴࠨ᩿"),
  bstack1l1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࡔࡥࡵ࡭ࡵࡺࠧ᪀"),
  bstack1l1111_opy_ (u"ࠩࡶ࡯࡮ࡶࡄࡦࡸ࡬ࡧࡪࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᪁"),
  bstack1l1111_opy_ (u"ࠪࡥࡺࡺ࡯ࡈࡴࡤࡲࡹࡖࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠪ᪂"),
  bstack1l1111_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡓࡧࡴࡶࡴࡤࡰࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩ᪃"),
  bstack1l1111_opy_ (u"ࠬࡹࡹࡴࡶࡨࡱࡕࡵࡲࡵࠩ᪄"),
  bstack1l1111_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡇࡤࡣࡊࡲࡷࡹ࠭᪅"),
  bstack1l1111_opy_ (u"ࠧࡴ࡭࡬ࡴ࡚ࡴ࡬ࡰࡥ࡮ࠫ᪆"), bstack1l1111_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡕࡻࡳࡩࠬ᪇"), bstack1l1111_opy_ (u"ࠩࡸࡲࡱࡵࡣ࡬ࡍࡨࡽࠬ᪈"),
  bstack1l1111_opy_ (u"ࠪࡥࡺࡺ࡯ࡍࡣࡸࡲࡨ࡮ࠧ᪉"),
  bstack1l1111_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡨࡧࡴࡄࡣࡳࡸࡺࡸࡥࠨ᪊"),
  bstack1l1111_opy_ (u"ࠬࡻ࡮ࡪࡰࡶࡸࡦࡲ࡬ࡐࡶ࡫ࡩࡷࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧ᪋"),
  bstack1l1111_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡗࡪࡰࡧࡳࡼࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࠨ᪌"),
  bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚࡯ࡰ࡮ࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ᪍"),
  bstack1l1111_opy_ (u"ࠨࡧࡱࡪࡴࡸࡣࡦࡃࡳࡴࡎࡴࡳࡵࡣ࡯ࡰࠬ᪎"),
  bstack1l1111_opy_ (u"ࠩࡨࡲࡸࡻࡲࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡵࡋࡥࡻ࡫ࡐࡢࡩࡨࡷࠬ᪏"), bstack1l1111_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡈࡪࡼࡴࡰࡱ࡯ࡷࡕࡵࡲࡵࠩ᪐"), bstack1l1111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨ࡛ࡪࡨࡶࡪࡧࡺࡈࡪࡺࡡࡪ࡮ࡶࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠧ᪑"),
  bstack1l1111_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡶࡰࡴࡅࡤࡧ࡭࡫ࡌࡪ࡯࡬ࡸࠬ᪒"),
  bstack1l1111_opy_ (u"࠭ࡣࡢ࡮ࡨࡲࡩࡧࡲࡇࡱࡵࡱࡦࡺࠧ᪓"),
  bstack1l1111_opy_ (u"ࠧࡣࡷࡱࡨࡱ࡫ࡉࡥࠩ᪔"),
  bstack1l1111_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨ᪕"),
  bstack1l1111_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡊࡴࡡࡣ࡮ࡨࡨࠬ᪖"), bstack1l1111_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࡘ࡫ࡲࡷ࡫ࡦࡩࡸࡇࡵࡵࡪࡲࡶ࡮ࢀࡥࡥࠩ᪗"),
  bstack1l1111_opy_ (u"ࠫࡦࡻࡴࡰࡃࡦࡧࡪࡶࡴࡂ࡮ࡨࡶࡹࡹࠧ᪘"), bstack1l1111_opy_ (u"ࠬࡧࡵࡵࡱࡇ࡭ࡸࡳࡩࡴࡵࡄࡰࡪࡸࡴࡴࠩ᪙"),
  bstack1l1111_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡵࡏ࡭ࡧ࠭᪚"),
  bstack1l1111_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡗࡥࡵ࠭᪛"),
  bstack1l1111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡰ࡬ࡸ࡮ࡧ࡬ࡖࡴ࡯ࠫ᪜"), bstack1l1111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡃ࡯ࡰࡴࡽࡐࡰࡲࡸࡴࡸ࠭᪝"), bstack1l1111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌ࡫ࡳࡵࡲࡦࡈࡵࡥࡺࡪࡗࡢࡴࡱ࡭ࡳ࡭ࠧ᪞"), bstack1l1111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵ࡫࡮ࡍ࡫ࡱ࡯ࡸࡏ࡮ࡃࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧࠫ᪟"),
  bstack1l1111_opy_ (u"ࠬࡱࡥࡦࡲࡎࡩࡾࡉࡨࡢ࡫ࡱࡷࠬ᪠"),
  bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࢀࡡࡣ࡮ࡨࡗࡹࡸࡩ࡯ࡩࡶࡈ࡮ࡸࠧ᪡"),
  bstack1l1111_opy_ (u"ࠧࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᪢"),
  bstack1l1111_opy_ (u"ࠨ࡫ࡱࡸࡪࡸࡋࡦࡻࡇࡩࡱࡧࡹࠨ᪣"),
  bstack1l1111_opy_ (u"ࠩࡶ࡬ࡴࡽࡉࡐࡕࡏࡳ࡬࠭᪤"),
  bstack1l1111_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡗࡹࡸࡡࡵࡧࡪࡽࠬ᪥"),
  bstack1l1111_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡖࡪࡹࡰࡰࡰࡶࡩ࡙࡯࡭ࡦࡱࡸࡸࠬ᪦"), bstack1l1111_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࡙ࡤ࡭ࡹ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᪧ"),
  bstack1l1111_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࠩ᪨"),
  bstack1l1111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡴࡻࡱࡧࡊࡾࡥࡤࡷࡷࡩࡋࡸ࡯࡮ࡊࡷࡸࡵࡹࠧ᪩"),
  bstack1l1111_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡅࡤࡴࡹࡻࡲࡦࠩ᪪"),
  bstack1l1111_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩ᪫"),
  bstack1l1111_opy_ (u"ࠪࡪࡺࡲ࡬ࡄࡱࡱࡸࡪࡾࡴࡍ࡫ࡶࡸࠬ᪬"),
  bstack1l1111_opy_ (u"ࠫࡼࡧࡩࡵࡈࡲࡶࡆࡶࡰࡔࡥࡵ࡭ࡵࡺࠧ᪭"),
  bstack1l1111_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡉ࡯࡯ࡰࡨࡧࡹࡘࡥࡵࡴ࡬ࡩࡸ࠭᪮"),
  bstack1l1111_opy_ (u"࠭ࡡࡱࡲࡑࡥࡲ࡫ࠧ᪯"),
  bstack1l1111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡔࡎࡆࡩࡷࡺࠧ᪰"),
  bstack1l1111_opy_ (u"ࠨࡶࡤࡴ࡜࡯ࡴࡩࡕ࡫ࡳࡷࡺࡐࡳࡧࡶࡷࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭᪱"),
  bstack1l1111_opy_ (u"ࠩࡶࡧࡦࡲࡥࡇࡣࡦࡸࡴࡸࠧ᪲"),
  bstack1l1111_opy_ (u"ࠪࡻࡩࡧࡌࡰࡥࡤࡰࡕࡵࡲࡵࠩ᪳"),
  bstack1l1111_opy_ (u"ࠫࡸ࡮࡯ࡸ࡚ࡦࡳࡩ࡫ࡌࡰࡩࠪ᪴"),
  bstack1l1111_opy_ (u"ࠬ࡯࡯ࡴࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡹࡸ࡫᪵ࠧ"),
  bstack1l1111_opy_ (u"࠭ࡸࡤࡱࡧࡩࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠨ᪶"),
  bstack1l1111_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡷࡸࡽ࡯ࡳࡦ᪷ࠪ"),
  bstack1l1111_opy_ (u"ࠨࡷࡶࡩࡕࡸࡥࡣࡷ࡬ࡰࡹ࡝ࡄࡂ᪸ࠩ"),
  bstack1l1111_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶ࡚ࡈࡆࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ᪹ࠪ"),
  bstack1l1111_opy_ (u"ࠪࡻࡪࡨࡄࡳ࡫ࡹࡩࡷࡇࡧࡦࡰࡷ࡙ࡷࡲ᪺ࠧ"),
  bstack1l1111_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡵࡪࠪ᪻"),
  bstack1l1111_opy_ (u"ࠬࡻࡳࡦࡐࡨࡻ࡜ࡊࡁࠨ᪼"),
  bstack1l1111_opy_ (u"࠭ࡷࡥࡣࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵ᪽ࠩ"), bstack1l1111_opy_ (u"ࠧࡸࡦࡤࡇࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࡔࡪ࡯ࡨࡳࡺࡺࠧ᪾"),
  bstack1l1111_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡏࡳࡩࡌࡨᪿࠬ"), bstack1l1111_opy_ (u"ࠩࡻࡧࡴࡪࡥࡔ࡫ࡪࡲ࡮ࡴࡧࡊࡦᫀࠪ"),
  bstack1l1111_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧ࡛ࡉࡇࡂࡶࡰࡧࡰࡪࡏࡤࠨ᫁"),
  bstack1l1111_opy_ (u"ࠫࡷ࡫ࡳࡦࡶࡒࡲࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡳࡶࡒࡲࡱࡿࠧ᫂"),
  bstack1l1111_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹࡹ᫃ࠧ"),
  bstack1l1111_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡩࡦࡵ᫄ࠪ"), bstack1l1111_opy_ (u"ࠧࡸࡦࡤࡗࡹࡧࡲࡵࡷࡳࡖࡪࡺࡲࡺࡋࡱࡸࡪࡸࡶࡢ࡮ࠪ᫅"),
  bstack1l1111_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࡊࡤࡶࡩࡽࡡࡳࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫ᫆"),
  bstack1l1111_opy_ (u"ࠩࡰࡥࡽ࡚ࡹࡱ࡫ࡱ࡫ࡋࡸࡥࡲࡷࡨࡲࡨࡿࠧ᫇"),
  bstack1l1111_opy_ (u"ࠪࡷ࡮ࡳࡰ࡭ࡧࡌࡷ࡛࡯ࡳࡪࡤ࡯ࡩࡈ࡮ࡥࡤ࡭ࠪ᫈"),
  bstack1l1111_opy_ (u"ࠫࡺࡹࡥࡄࡣࡵࡸ࡭ࡧࡧࡦࡕࡶࡰࠬ᫉"),
  bstack1l1111_opy_ (u"ࠬࡹࡨࡰࡷ࡯ࡨ࡚ࡹࡥࡔ࡫ࡱ࡫ࡱ࡫ࡴࡰࡰࡗࡩࡸࡺࡍࡢࡰࡤ࡫ࡪࡸ᫊ࠧ"),
  bstack1l1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡎ࡝ࡄࡑࠩ᫋"),
  bstack1l1111_opy_ (u"ࠧࡢ࡮࡯ࡳࡼ࡚࡯ࡶࡥ࡫ࡍࡩࡋ࡮ࡳࡱ࡯ࡰࠬᫌ"),
  bstack1l1111_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡉ࡫ࡧࡨࡪࡴࡁࡱ࡫ࡓࡳࡱ࡯ࡣࡺࡇࡵࡶࡴࡸࠧᫍ"),
  bstack1l1111_opy_ (u"ࠩࡰࡳࡨࡱࡌࡰࡥࡤࡸ࡮ࡵ࡮ࡂࡲࡳࠫᫎ"),
  bstack1l1111_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉࡳࡷࡳࡡࡵࠩ᫏"), bstack1l1111_opy_ (u"ࠫࡱࡵࡧࡤࡣࡷࡊ࡮ࡲࡴࡦࡴࡖࡴࡪࡩࡳࠨ᫐"),
  bstack1l1111_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡈࡪࡲࡡࡺࡃࡧࡦࠬ᫑"),
  bstack1l1111_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡉࡥࡎࡲࡧࡦࡺ࡯ࡳࡃࡸࡸࡴࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠩ᫒")
]
bstack11l1ll1l1_opy_ = bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡵࡱ࡮ࡲࡥࡩ࠭᫓")
bstack1l1ll1l1l1_opy_ = [bstack1l1111_opy_ (u"ࠨ࠰ࡤࡴࡰ࠭᫔"), bstack1l1111_opy_ (u"ࠩ࠱ࡥࡦࡨࠧ᫕"), bstack1l1111_opy_ (u"ࠪ࠲࡮ࡶࡡࠨ᫖")]
bstack1l11lll11_opy_ = [bstack1l1111_opy_ (u"ࠫ࡮ࡪࠧ᫗"), bstack1l1111_opy_ (u"ࠬࡶࡡࡵࡪࠪ᫘"), bstack1l1111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ᫙"), bstack1l1111_opy_ (u"ࠧࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩ࠭᫚")]
bstack11l11ll1l_opy_ = {
  bstack1l1111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᫛"): bstack1l1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᫜"),
  bstack1l1111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ᫝"): bstack1l1111_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫞"),
  bstack1l1111_opy_ (u"ࠬ࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᫟"): bstack1l1111_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᫠"),
  bstack1l1111_opy_ (u"ࠧࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᫡"): bstack1l1111_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᫢"),
  bstack1l1111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫣"): bstack1l1111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ᫤")
}
bstack111lll11l_opy_ = [
  bstack1l1111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫥"),
  bstack1l1111_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ᫦"),
  bstack1l1111_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᫧"),
  bstack1l1111_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᫨"),
  bstack1l1111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᫩"),
]
bstack1ll11ll1l_opy_ = bstack1ll1l11ll_opy_ + bstack11l1111l11l_opy_ + bstack1l111ll11_opy_
bstack1ll111l1l_opy_ = [
  bstack1l1111_opy_ (u"ࠩࡡࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࠪࠧ᫪"),
  bstack1l1111_opy_ (u"ࠪࡢࡧࡹ࠭࡭ࡱࡦࡥࡱ࠴ࡣࡰ࡯ࠧࠫ᫫"),
  bstack1l1111_opy_ (u"ࠫࡣ࠷࠲࠸࠰ࠪ᫬"),
  bstack1l1111_opy_ (u"ࠬࡤ࠱࠱࠰ࠪ᫭"),
  bstack1l1111_opy_ (u"࠭࡞࠲࠹࠵࠲࠶ࡡ࠶࠮࠻ࡠ࠲ࠬ᫮"),
  bstack1l1111_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠸࡛࠱࠯࠼ࡡ࠳࠭᫯"),
  bstack1l1111_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠳࡜࠲࠰࠵ࡢ࠴ࠧ᫰"),
  bstack1l1111_opy_ (u"ࠩࡡ࠵࠾࠸࠮࠲࠸࠻࠲ࠬ᫱")
]
bstack11l1l111111_opy_ = bstack1l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ᫲")
bstack1lll1l111_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡪࡼࡥ࡯ࡶࠪ᫳")
bstack1l11111ll1_opy_ = [ bstack1l1111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᫴") ]
bstack1lll111l11_opy_ = [ bstack1l1111_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᫵") ]
bstack1llllllll_opy_ = [bstack1l1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ᫶")]
bstack11l11l1l1_opy_ = [ bstack1l1111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᫷") ]
bstack1l1ll1ll11_opy_ = bstack1l1111_opy_ (u"ࠩࡖࡈࡐ࡙ࡥࡵࡷࡳࠫ᫸")
bstack1lll1ll111_opy_ = bstack1l1111_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡅࡹࡺࡥ࡮ࡲࡷࡩࡩ࠭᫹")
bstack11l11l1111_opy_ = bstack1l1111_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠨ᫺")
bstack11ll111l11_opy_ = bstack1l1111_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࠫ᫻")
bstack11l11ll1ll_opy_ = [
  bstack1l1111_opy_ (u"࠭ࡅࡓࡔࡢࡊࡆࡏࡌࡆࡆࠪ᫼"),
  bstack1l1111_opy_ (u"ࠧࡆࡔࡕࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧ᫽"),
  bstack1l1111_opy_ (u"ࠨࡇࡕࡖࡤࡈࡌࡐࡅࡎࡉࡉࡥࡂ࡚ࡡࡆࡐࡎࡋࡎࡕࠩ᫾"),
  bstack1l1111_opy_ (u"ࠩࡈࡖࡗࡥࡎࡆࡖ࡚ࡓࡗࡑ࡟ࡄࡊࡄࡒࡌࡋࡄࠨ᫿"),
  bstack1l1111_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡊ࡚࡟ࡏࡑࡗࡣࡈࡕࡎࡏࡇࡆࡘࡊࡊࠧᬀ"),
  bstack1l1111_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡉࡌࡐࡕࡈࡈࠬᬁ"),
  bstack1l1111_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡕࡈࡘࠬᬂ"),
  bstack1l1111_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡓࡇࡉ࡙ࡘࡋࡄࠨᬃ"),
  bstack1l1111_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡃࡅࡓࡗ࡚ࡅࡅࠩᬄ"),
  bstack1l1111_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᬅ"),
  bstack1l1111_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪᬆ"),
  bstack1l1111_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡋࡑ࡚ࡆࡒࡉࡅࠩᬇ"),
  bstack1l1111_opy_ (u"ࠫࡊࡘࡒࡠࡃࡇࡈࡗࡋࡓࡔࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧᬈ"),
  bstack1l1111_opy_ (u"ࠬࡋࡒࡓࡡࡗ࡙ࡓࡔࡅࡍࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᬉ"),
  bstack1l1111_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪᬊ"),
  bstack1l1111_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᬋ"),
  bstack1l1111_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡖࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡊࡒࡗ࡙ࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫᬌ"),
  bstack1l1111_opy_ (u"ࠩࡈࡖࡗࡥࡐࡓࡑ࡛࡝ࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᬍ"),
  bstack1l1111_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡔࡏࡕࡡࡕࡉࡘࡕࡌࡗࡇࡇࠫᬎ"),
  bstack1l1111_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡒࡆࡕࡒࡐ࡚࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᬏ"),
  bstack1l1111_opy_ (u"ࠬࡋࡒࡓࡡࡐࡅࡓࡊࡁࡕࡑࡕ࡝ࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫᬐ"),
]
bstack1lll11l1l_opy_ = bstack1l1111_opy_ (u"࠭࠮࠰ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡢࡴࡷ࡭࡫ࡧࡣࡵࡵ࠲ࠫᬑ")
bstack11l111lll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠧࡿࠩᬒ")), bstack1l1111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᬓ"), bstack1l1111_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᬔ"))
bstack11l1l1lll11_opy_ = bstack1l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲ࡬ࠫᬕ")
bstack11l11l1ll11_opy_ = [ bstack1l1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᬖ"), bstack1l1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᬗ"), bstack1l1111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬᬘ"), bstack1l1111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᬙ")]
bstack1l1ll1l1ll_opy_ = [ bstack1l1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᬚ"), bstack1l1111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᬛ"), bstack1l1111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩᬜ"), bstack1l1111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫᬝ") ]
bstack1l111lll1l_opy_ = [ bstack1l1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᬞ") ]
bstack11l1111llll_opy_ = [ bstack1l1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᬟ") ]
bstack11l11llll1_opy_ = 360
bstack11l11lll1ll_opy_ = bstack1l1111_opy_ (u"ࠢࡢࡲࡳ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᬠ")
bstack11l111ll1l1_opy_ = bstack1l1111_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵࠥᬡ")
bstack11l111l1l1l_opy_ = bstack1l1111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠧᬢ")
bstack11l1l1ll11l_opy_ = bstack1l1111_opy_ (u"ࠥࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡹ࡫ࡳࡵࡵࠣࡥࡷ࡫ࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡏࡔࠢࡹࡩࡷࡹࡩࡰࡰࠣࠩࡸࠦࡡ࡯ࡦࠣࡥࡧࡵࡶࡦࠢࡩࡳࡷࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠࡥࡧࡹ࡭ࡨ࡫ࡳ࠯ࠤᬣ")
bstack11l1ll1ll1l_opy_ = bstack1l1111_opy_ (u"ࠦ࠶࠷࠮࠱ࠤᬤ")
bstack1llllllll1l_opy_ = {
  bstack1l1111_opy_ (u"ࠬࡖࡁࡔࡕࠪᬥ"): bstack1l1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᬦ"),
  bstack1l1111_opy_ (u"ࠧࡇࡃࡌࡐࠬᬧ"): bstack1l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᬨ"),
  bstack1l1111_opy_ (u"ࠩࡖࡏࡎࡖࠧᬩ"): bstack1l1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᬪ")
}
bstack111ll1l1l1_opy_ = [
  bstack1l1111_opy_ (u"ࠦ࡬࡫ࡴࠣᬫ"),
  bstack1l1111_opy_ (u"ࠧ࡭࡯ࡃࡣࡦ࡯ࠧᬬ"),
  bstack1l1111_opy_ (u"ࠨࡧࡰࡈࡲࡶࡼࡧࡲࡥࠤᬭ"),
  bstack1l1111_opy_ (u"ࠢࡳࡧࡩࡶࡪࡹࡨࠣᬮ"),
  bstack1l1111_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢᬯ"),
  bstack1l1111_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᬰ"),
  bstack1l1111_opy_ (u"ࠥࡷࡺࡨ࡭ࡪࡶࡈࡰࡪࡳࡥ࡯ࡶࠥᬱ"),
  bstack1l1111_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣᬲ"),
  bstack1l1111_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣᬳ"),
  bstack1l1111_opy_ (u"ࠨࡣ࡭ࡧࡤࡶࡊࡲࡥ࡮ࡧࡱࡸ᬴ࠧ"),
  bstack1l1111_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࡳࠣᬵ"),
  bstack1l1111_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠣᬶ"),
  bstack1l1111_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࡄࡷࡾࡴࡣࡔࡥࡵ࡭ࡵࡺࠢᬷ"),
  bstack1l1111_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤᬸ"),
  bstack1l1111_opy_ (u"ࠦࡶࡻࡩࡵࠤᬹ"),
  bstack1l1111_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲ࡚࡯ࡶࡥ࡫ࡅࡨࡺࡩࡰࡰࠥᬺ"),
  bstack1l1111_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳࡍࡶ࡮ࡷ࡭࡙ࡵࡵࡤࡪࠥᬻ"),
  bstack1l1111_opy_ (u"ࠢࡴࡪࡤ࡯ࡪࠨᬼ"),
  bstack1l1111_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࡁࡱࡲࠥᬽ")
]
bstack11l1111ll11_opy_ = [
  bstack1l1111_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࠣᬾ"),
  bstack1l1111_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᬿ"),
  bstack1l1111_opy_ (u"ࠦࡦࡻࡴࡰࠤᭀ"),
  bstack1l1111_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧᭁ"),
  bstack1l1111_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᭂ")
]
bstack1l11lllll_opy_ = {
  bstack1l1111_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨᭃ"): [bstack1l1111_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺ᭄ࠢ")],
  bstack1l1111_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᭅ"): [bstack1l1111_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᭆ")],
  bstack1l1111_opy_ (u"ࠦࡦࡻࡴࡰࠤᭇ"): [bstack1l1111_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡇ࡯ࡩࡲ࡫࡮ࡵࠤᭈ"), bstack1l1111_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡄࡧࡹ࡯ࡶࡦࡇ࡯ࡩࡲ࡫࡮ࡵࠤᭉ"), bstack1l1111_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᭊ"), bstack1l1111_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢᭋ")],
  bstack1l1111_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤᭌ"): [bstack1l1111_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥ᭍")],
  bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᭎"): [bstack1l1111_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ᭏")],
}
bstack11l111ll111_opy_ = {
  bstack1l1111_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ᭐"): bstack1l1111_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨ᭑"),
  bstack1l1111_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᭒"): bstack1l1111_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ᭓"),
  bstack1l1111_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢ᭔"): bstack1l1111_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨ᭕"),
  bstack1l1111_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣ᭖"): bstack1l1111_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࠣ᭗"),
  bstack1l1111_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ᭘"): bstack1l1111_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ᭙")
}
bstack11111l1ll1_opy_ = {
  bstack1l1111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭᭚"): bstack1l1111_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡖࡩࡹࡻࡰࠨ᭛"),
  bstack1l1111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ᭜"): bstack1l1111_opy_ (u"࡙ࠬࡵࡪࡶࡨࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭᭝"),
  bstack1l1111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ᭞"): bstack1l1111_opy_ (u"ࠧࡕࡧࡶࡸ࡙ࠥࡥࡵࡷࡳࠫ᭟"),
  bstack1l1111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ᭠"): bstack1l1111_opy_ (u"ࠩࡗࡩࡸࡺࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩ᭡")
}
bstack11l111ll1ll_opy_ = 65536
bstack11l11l1l1ll_opy_ = bstack1l1111_opy_ (u"ࠪ࠲࠳࠴࡛ࡕࡔࡘࡒࡈࡇࡔࡆࡆࡠࠫ᭢")
bstack11l11111l1l_opy_ = [
      bstack1l1111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭᭣"), bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᭤"), bstack1l1111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᭥"), bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᭦"), bstack1l1111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪ᭧"),
      bstack1l1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ᭨"), bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭᭩"), bstack1l1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬ᭪"), bstack1l1111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭᭫"),
      bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫᭬ࠧ"), bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ᭭"), bstack1l1111_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ᭮")
    ]
bstack11l111llll1_opy_= {
  bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᭯"): bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ᭰"),
  bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ᭱"): bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᭲"),
  bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ᭳"): bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ᭴"),
  bstack1l1111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᭵"): bstack1l1111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᭶"),
  bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᭷"): bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᭸"),
  bstack1l1111_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ᭹"): bstack1l1111_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ᭺"),
  bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᭻"): bstack1l1111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ᭼"),
  bstack1l1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭᭽"): bstack1l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᭾"),
  bstack1l1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ᭿"): bstack1l1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᮀ"),
  bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᮁ"): bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬᮂ"),
  bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᮃ"): bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᮄ"),
  bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪᮅ"): bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫᮆ"),
  bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᮇ"): bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᮈ"),
  bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࠧᮉ"): bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࡐࡲࡷ࡭ࡴࡴࡳࠨᮊ"),
  bstack1l1111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᮋ"): bstack1l1111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬᮌ"),
  bstack1l1111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᮍ"): bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᮎ"),
  bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᮏ"): bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᮐ"),
  bstack1l1111_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᮑ"): bstack1l1111_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᮒ"),
  bstack1l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᮓ"): bstack1l1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᮔ"),
  bstack1l1111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᮕ"): bstack1l1111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᮖ"),
  bstack1l1111_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᮗ"): bstack1l1111_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᮘ"),
  bstack1l1111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᮙ"): bstack1l1111_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᮚ"),
  bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᮛ"): bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᮜ"),
  bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᮝ"): bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᮞ"),
  bstack1l1111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᮟ"): bstack1l1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᮠ"),
  bstack1l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᮡ"): bstack1l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᮢ"),
  bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᮣ"): bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᮤ"),
  bstack1l1111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᮥ"): bstack1l1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᮦ")
}
bstack11l111l1ll1_opy_ = [bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᮧ"), bstack1l1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᮨ")]
bstack111ll1111_opy_ = (bstack1l1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᮩ"),)
bstack11l11111ll1_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠱ࡹ࠵࠴ࡻࡰࡥࡣࡷࡩࡤࡩ࡬ࡪ᮪ࠩ")
bstack1l11l1lll_opy_ = bstack1l1111_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠯ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠵ࡶ࠲࠱ࡪࡶ࡮ࡪࡳ࠰ࠤ᮫")
bstack1l111ll1l1_opy_ = bstack1l1111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩࡵ࡭ࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࠨᮬ")
bstack11ll11ll_opy_ = bstack1l1111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠤᮭ")
class EVENTS(Enum):
  bstack11l111lllll_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭ᮮ")
  bstack1l11l11l_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮ࡨࡥࡳࡻࡰࠨᮯ")
  bstack1ll111ll1l_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡨ࡬ࡲࡦࡲࡩࡻࡧࠪ᮰")
  bstack11l11l1l111_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࡬ࡰࡩࡶࠫ᮱")
  bstack1ll1lllll1_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩ᮲") #shift post bstack11l11l111ll_opy_
  bstack11111lll1_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨ᮳") #shift post bstack11l11l111ll_opy_
  bstack11l111lll1l_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶ࡫ࡹࡧ࠭᮴") #shift
  bstack11l1111l111_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧ᮵") #shift
  bstack1ll111ll11_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠾࡭ࡻࡢ࠮࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠬ᮶")
  bstack1l1lllll111_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡳࡢࡸࡨ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷࠬ᮷")
  bstack11l1l1llll_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡱࡧࡵࡪࡴࡸ࡭ࡴࡥࡤࡲࠬ᮸")
  bstack11111ll1l_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡲ࡯ࡤࡣ࡯ࠫ᮹") #shift
  bstack1lll1l11l_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡥࡵࡶ࠭ࡶࡲ࡯ࡳࡦࡪࠧᮺ") #shift
  bstack1l1l1l1111_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡤ࡫࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠭ᮻ")
  bstack1llll1ll1l_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪᮼ") #shift
  bstack1ll111ll1_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵࠪᮽ") #shift
  bstack11l11l11l11_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿࠧᮾ") #shift
  bstack1l11l1l11ll_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᮿ")
  bstack1llll11ll_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡳࡵࡣࡷࡹࡸ࠭ᯀ") #shift
  bstack11lllll111_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡨࡶࡤ࠰ࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠧᯁ")
  bstack11l11111l11_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡰࡺࡼ࠱ࡸ࡫ࡴࡶࡲࠪᯂ") #shift
  bstack11lllll1l1_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡶࡸࡴࠬᯃ")
  bstack11l111l1lll_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡳ࡯ࡣࡳࡷ࡭ࡵࡴࠨᯄ") # not bstack11l11l1l11l_opy_ in python
  bstack11lll1ll1l_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡳࡸ࡭ࡹ࠭ᯅ") # used in bstack11l11l1111l_opy_
  bstack11ll11ll11l_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡶࡪ࠳ࡱࡶ࡫ࡷࠫᯆ")
  bstack11ll11l1l11_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮ࡳࡸ࡭ࡹ࠭ᯇ")
  bstack1llll1l1l_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾࡬࡫ࡴࠨᯈ") # used in bstack11l11l1111l_opy_
  bstack11ll11l111_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿࡮࡯ࡰ࡭ࠪᯉ")
  bstack11ll1l11111_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡧ࠰࡬ࡴࡵ࡫ࠨᯊ")
  bstack11ll11llll1_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡱࡶࡸ࠲࡮࡯ࡰ࡭ࠪᯋ")
  bstack11l1l111_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠩᯌ")
  bstack111lll1l11_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠩᯍ") #
  bstack111l11ll1l_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡦࡵ࡭ࡻ࡫ࡲ࠮ࡶࡤ࡯ࡪ࡙ࡣࡳࡧࡨࡲࡘ࡮࡯ࡵࠩᯎ")
  bstack1l11111ll_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡥࡺࡺ࡯࠮ࡥࡤࡴࡹࡻࡲࡦࠩᯏ")
  bstack111lll111l_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡦ࠯ࡷࡩࡸࡺࠧᯐ")
  bstack11llllll1_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡰࡰࡵࡷ࠱ࡹ࡫ࡳࡵࠩᯑ")
  bstack1lllllll1l_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡴࡨ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬᯒ") #shift
  bstack11ll111l1_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧᯓ") #shift
  bstack11l11l11111_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࠭ࡤࡣࡳࡸࡺࡸࡥࠨᯔ")
  bstack11l111ll11l_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿࡯ࡤ࡭ࡧ࠰ࡸ࡮ࡳࡥࡰࡷࡷࠫᯕ")
  bstack1ll1l1111l_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾ࡪࡾࡩࡵ࠯࡫ࡥࡳࡪ࡬ࡦࡴࠪᯖ")
  bstack1ll11llll11_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡨࡼ࡮ࡺ࠭ࡩࡣࡱࡨࡱ࡫ࡲࠨᯗ")
  bstack11l111l1111_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡰࡧ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷࠬᯘ")
  bstack11l111l11ll_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸ࡭ࡻࡢ࠻ࡵࡷࡳࡵ࠭ᯙ")
  bstack1ll11l11111_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡹࡴࡢࡴࡷࠫᯚ")
  bstack11l1111lll1_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨᯛ")
  bstack11l11l1l1l1_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡤࡪࡨࡧࡰ࠳ࡵࡱࡦࡤࡸࡪ࠭ᯜ")
  bstack1ll11lll1l1_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠧᯝ")
  bstack1ll1l1111l1_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡹࡴࡢࡴࡷࡦ࡮ࡴࡡࡳࡻࠪᯞ")
  bstack1ll11ll1l1l_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡣࡰࡰࡱࡩࡨࡺࠧᯟ")
  bstack1ll1ll1111l_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡴࡶࡲࡴࠬᯠ")
  bstack1ll1l1ll1l1_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡷࡥࡷࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰࠪᯡ")
  bstack1ll1111l1l1_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡳࡳࡴࡥࡤࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭ᯢ")
  bstack11l111l111l_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠧᯣ")
  bstack11l1111l1ll_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡥࡐࡨࡥࡷ࡫ࡳࡵࡊࡸࡦࠬᯤ")
  bstack1l111l11l11_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡍࡳ࡯ࡴࠨᯥ")
  bstack1l111l1l111_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡳࡶ᯦ࠪ")
  bstack1l1ll1l1l11_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡃࡰࡰࡩ࡭࡬࠭ᯧ")
  bstack11l11l11ll1_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡄࡱࡱࡪ࡮࡭ࠧᯨ")
  bstack1l1l1lll111_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࡭ࡘ࡫࡬ࡧࡊࡨࡥࡱ࡙ࡴࡦࡲࠪᯩ")
  bstack1l1l1lll1ll_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࡮࡙ࡥ࡭ࡨࡋࡩࡦࡲࡇࡦࡶࡕࡩࡸࡻ࡬ࡵࠩᯪ")
  bstack1l1l11111l1_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡉࡻ࡫࡮ࡵࠩᯫ")
  bstack1l11ll1l111_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠨᯬ")
  bstack1l11l1lll1l_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡰࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࡅࡷࡧࡱࡸࠬᯭ")
  bstack11l1111ll1l_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡪࡴࡱࡶࡧࡸࡩ࡙࡫ࡳࡵࡇࡹࡩࡳࡺࠧᯮ")
  bstack1l1111l111l_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡱࡳࠫᯯ")
  bstack1ll1111lll1_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡤ࡬࠼ࡲࡲࡘࡺ࡯ࡱࠩᯰ")
  bstack11ll111111l_opy_ = bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳ࡙ࡵࡲ࡯ࡢࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧᯱ")
  bstack1ll1lll1l_opy_ = bstack1l1111_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫࡮ࡥࡈࡸࡲࡳ࡫࡬ࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪ᯲ࠧ")
  bstack1ll1111l1_opy_ = bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦࡉࡹࡳࡴࡥ࡭ࡖࡨࡷࡹࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠨ᯳")
  bstack1llll1ll111_opy_ = bstack1l1111_opy_ (u"ࠩࡶࡨࡰࡀࡡࡱࡲ࡯ࡽࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡔࡾࡺࡥࡴࡶࠪ᯴")
  bstack1llll1l1l1l_opy_ = bstack1l1111_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡷࡕࡿࡴࡦࡵࡷࠫ᯵")
  bstack1lllll1l1l1_opy_ = bstack1l1111_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡼࡸࡪࡹࡴࡈࡧࡷࡘࡴࡺࡡ࡭ࡖࡨࡷࡹࡹࠧ᯶")
class STAGE(Enum):
  bstack1l111ll1_opy_ = bstack1l1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫ᯷")
  END = bstack1l1111_opy_ (u"࠭ࡥ࡯ࡦࠪ᯸")
  bstack1111lll11_opy_ = bstack1l1111_opy_ (u"ࠧࡴ࡫ࡱ࡫ࡱ࡫ࠧ᯹")
bstack11l1lllll_opy_ = {
  bstack1l1111_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࠨ᯺"): bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᯻"),
  bstack1l1111_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ᯼"): bstack1l1111_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭᯽")
}
PLAYWRIGHT_HUB_URL = bstack1l1111_opy_ (u"ࠧࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠢ᯾")
bstack1l1llll11l1_opy_ = 98
bstack1l1ll11ll11_opy_ = 100
bstack1lllll111ll_opy_ = {
  bstack1l1111_opy_ (u"࠭ࡲࡦࡴࡸࡲࠬ᯿"): bstack1l1111_opy_ (u"ࠧ࠮࠯ࡵࡩࡷࡻ࡮ࡴࠩᰀ"),
  bstack1l1111_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧᰁ"): bstack1l1111_opy_ (u"ࠩ࠰࠱ࡷ࡫ࡲࡶࡰࡶ࠱ࡩ࡫࡬ࡢࡻࠪᰂ"),
  bstack1l1111_opy_ (u"ࠪࡶࡪࡸࡵ࡯࠯ࡧࡩࡱࡧࡹࠨᰃ"): 0
}
bstack11l11111lll_opy_ = bstack1l1111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦᰄ")
bstack11l111lll11_opy_ = bstack1l1111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡵࡱ࡮ࡲࡥࡩ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᰅ")
bstack1ll1lll111_opy_ = bstack1l1111_opy_ (u"ࠨࡔࡆࡕࡗࠤࡗࡋࡐࡐࡔࡗࡍࡓࡍࠠࡂࡐࡇࠤࡆࡔࡁࡍ࡛ࡗࡍࡈ࡙ࠢᰆ")