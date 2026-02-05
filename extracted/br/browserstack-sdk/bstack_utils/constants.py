# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import re
from enum import Enum
bstack1l1lll1111_opy_ = {
  bstack11l1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭᢮"): bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩ᢯"),
  bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᢰ"): bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪᢱ"),
  bstack11l1ll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᢲ"): bstack11l1ll1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᢳ"),
  bstack11l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᢴ"): bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫᢵ"),
  bstack11l1ll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᢶ"): bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧᢷ"),
  bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᢸ"): bstack11l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᢹ"),
  bstack11l1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᢺ"): bstack11l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨᢻ"),
  bstack11l1ll1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᢼ"): bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪᢽ"),
  bstack11l1ll1_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫᢾ"): bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧᢿ"),
  bstack11l1ll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᣀ"): bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᣁ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᣂ"): bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᣃ"),
  bstack11l1ll1_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫᣄ"): bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫᣅ"),
  bstack11l1ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᣆ"): bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᣇ"),
  bstack11l1ll1_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᣈ"): bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᣉ"),
  bstack11l1ll1_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᣊ"): bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᣋ"),
  bstack11l1ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨᣌ"): bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨᣍ"),
  bstack11l1ll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᣎ"): bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᣏ"),
  bstack11l1ll1_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩᣐ"): bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩᣑ"),
  bstack11l1ll1_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᣒ"): bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᣓ"),
  bstack11l1ll1_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧᣔ"): bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧᣕ"),
  bstack11l1ll1_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫᣖ"): bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫᣗ"),
  bstack11l1ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ᣘ"): bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ᣙ"),
  bstack11l1ll1_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬᣚ"): bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬᣛ"),
  bstack11l1ll1_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩᣜ"): bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩᣝ"),
  bstack11l1ll1_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫᣞ"): bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫᣟ"),
  bstack11l1ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨᣠ"): bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨᣡ"),
  bstack11l1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᣢ"): bstack11l1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᣣ"),
  bstack11l1ll1_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭ᣤ"): bstack11l1ll1_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨᣥ"),
  bstack11l1ll1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᣦ"): bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᣧ"),
  bstack11l1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ᣨ"): bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ᣩ"),
  bstack11l1ll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩᣪ"): bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩᣫ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩᣬ"): bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬᣭ"),
  bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᣮ"): bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᣯ"),
  bstack11l1ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᣰ"): bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧᣱ"),
  bstack11l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᣲ"): bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᣳ"),
  bstack11l1ll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ᣴ"): bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ᣵ"),
  bstack11l1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩ᣶"): bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩ᣷"),
  bstack11l1ll1_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬ᣸"): bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬ᣹"),
  bstack11l1ll1_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨ᣺"): bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨ᣻"),
  bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᣼"): bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᣽"),
  bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᣾"): bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᣿")
}
bstack11l111ll111_opy_ = [
  bstack11l1ll1_opy_ (u"ࠩࡲࡷࠬᤀ"),
  bstack11l1ll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᤁ"),
  bstack11l1ll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᤂ"),
  bstack11l1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᤃ"),
  bstack11l1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᤄ"),
  bstack11l1ll1_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫᤅ"),
  bstack11l1ll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᤆ"),
]
bstack1ll11lll11_opy_ = {
  bstack11l1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᤇ"): [bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᤈ"), bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡐࡄࡑࡊ࠭ᤉ")],
  bstack11l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᤊ"): bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᤋ"),
  bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᤌ"): bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠫᤍ"),
  bstack11l1ll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᤎ"): bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠨᤏ"),
  bstack11l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᤐ"): bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᤑ"),
  bstack11l1ll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᤒ"): bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡔࡡࡓࡉࡗࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨᤓ"),
  bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᤔ"): bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧᤕ"),
  bstack11l1ll1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧᤖ"): bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨᤗ"),
  bstack11l1ll1_opy_ (u"ࠬࡧࡰࡱࠩᤘ"): [bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࡡࡌࡈࠬᤙ"), bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࠪᤚ")],
  bstack11l1ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᤛ"): bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡒࡏࡈࡎࡈ࡚ࡊࡒࠧᤜ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᤝ"): bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᤞ"),
  bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᤟"): [bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠪᤠ"), bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧᤡ")],
  bstack11l1ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᤢ"): bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡘࡖࡇࡕࡓࡄࡃࡏࡉࠬᤣ"),
  bstack11l1ll1_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡊࡔࡖࠨᤤ"): bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡓࡗࡉࡈࡆࡕࡗࡖࡆ࡚ࡉࡐࡐࡢࡗࡒࡇࡒࡕࡡࡖࡉࡑࡋࡃࡕࡋࡒࡒࡤࡌࡅࡂࡖࡘࡖࡊࡥࡂࡓࡃࡑࡇࡍࡋࡓࠨᤥ")
}
bstack111l1l1l1_opy_ = {
  bstack11l1ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᤦ"): [bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡢࡲࡦࡳࡥࠨᤧ"), bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡒࡦࡳࡥࠨᤨ")],
  bstack11l1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᤩ"): [bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡠ࡭ࡨࡽࠬᤪ"), bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᤫ")],
  bstack11l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᤬"): bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᤭"),
  bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᤮"): bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᤯"),
  bstack11l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᤰ"): bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᤱ"),
  bstack11l1ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᤲ"): [bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡵࡶࠧᤳ"), bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᤴ")],
  bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᤵ"): bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬᤶ"),
  bstack11l1ll1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᤷ"): bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᤸ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡵࡶ᤹ࠧ"): bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࠧ᤺"),
  bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲ᤻ࠧ"): bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ᤼"),
  bstack11l1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᤽"): bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᤾"),
  bstack11l1ll1_opy_ (u"ࠤࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡇࡑࡏࠢ᤿"): bstack11l1ll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࠣ᥀"),
}
bstack11l1111111_opy_ = {
  bstack11l1ll1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ᥁"): bstack11l1ll1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᥂"),
  bstack11l1ll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᥃"): [bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᥄"), bstack11l1ll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᥅")],
  bstack11l1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᥆"): bstack11l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ᥇"),
  bstack11l1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ᥈"): bstack11l1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ᥉"),
  bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ᥊"): [bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ᥋"), bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ᥌")],
  bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᥍"): bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᥎"),
  bstack11l1ll1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨ᥏"): bstack11l1ll1_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪᥐ"),
  bstack11l1ll1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᥑ"): [bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᥒ"), bstack11l1ll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᥓ")],
  bstack11l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᥔ"): [bstack11l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫᥕ"), bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫᥖ")]
}
bstack111l11ll1l_opy_ = [
  bstack11l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᥗ"),
  bstack11l1ll1_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᥘ"),
  bstack11l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ᥙ"),
  bstack11l1ll1_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨᥚ"),
  bstack11l1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫᥛ"),
  bstack11l1ll1_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨᥜ"),
  bstack11l1ll1_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧᥝ"),
  bstack11l1ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᥞ"),
  bstack11l1ll1_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᥟ"),
  bstack11l1ll1_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᥠ"),
  bstack11l1ll1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᥡ"),
  bstack11l1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᥢ"),
]
bstack1ll11111l_opy_ = [
  bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᥣ"),
  bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᥤ"),
  bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᥥ"),
  bstack11l1ll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᥦ"),
  bstack11l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᥧ"),
  bstack11l1ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᥨ"),
  bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᥩ"),
  bstack11l1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᥪ"),
  bstack11l1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᥫ"),
  bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᥬ"),
  bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᥭ"),
  bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧ᥮"),
  bstack11l1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪ᥯"),
  bstack11l1ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡖࡤ࡫ࠬᥰ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᥱ"),
  bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᥲ"),
  bstack11l1ll1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᥳ"),
  bstack11l1ll1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠵ࠬᥴ"),
  bstack11l1ll1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠷࠭᥵"),
  bstack11l1ll1_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠹ࠧ᥶"),
  bstack11l1ll1_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠴ࠨ᥷"),
  bstack11l1ll1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠶ࠩ᥸"),
  bstack11l1ll1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠸ࠪ᥹"),
  bstack11l1ll1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠺ࠫ᥺"),
  bstack11l1ll1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠼ࠬ᥻"),
  bstack11l1ll1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠾࠭᥼"),
  bstack11l1ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ᥽"),
  bstack11l1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᥾"),
  bstack11l1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭᥿"),
  bstack11l1ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᦀ"),
  bstack11l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᦁ"),
  bstack11l1ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᦂ"),
  bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫᦃ"),
  bstack11l1ll1_opy_ (u"ࠨࡪࡸࡦࡗ࡫ࡧࡪࡱࡱࠫᦄ")
]
bstack11l1111llll_opy_ = [
  bstack11l1ll1_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧᦅ"),
  bstack11l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᦆ"),
  bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᦇ"),
  bstack11l1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᦈ"),
  bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡔࡷ࡯࡯ࡳ࡫ࡷࡽࠬᦉ"),
  bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᦊ"),
  bstack11l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡢࡩࠪᦋ"),
  bstack11l1ll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᦌ"),
  bstack11l1ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᦍ"),
  bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᦎ"),
  bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᦏ"),
  bstack11l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᦐ"),
  bstack11l1ll1_opy_ (u"ࠧࡰࡵࠪᦑ"),
  bstack11l1ll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᦒ"),
  bstack11l1ll1_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨᦓ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᦔ"),
  bstack11l1ll1_opy_ (u"ࠫࡷ࡫ࡧࡪࡱࡱࠫᦕ"),
  bstack11l1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧᦖ"),
  bstack11l1ll1_opy_ (u"࠭࡭ࡢࡥ࡫࡭ࡳ࡫ࠧᦗ"),
  bstack11l1ll1_opy_ (u"ࠧࡳࡧࡶࡳࡱࡻࡴࡪࡱࡱࠫᦘ"),
  bstack11l1ll1_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᦙ"),
  bstack11l1ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ᦚ"),
  bstack11l1ll1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩᦛ"),
  bstack11l1ll1_opy_ (u"ࠫࡳࡵࡐࡢࡩࡨࡐࡴࡧࡤࡕ࡫ࡰࡩࡴࡻࡴࠨᦜ"),
  bstack11l1ll1_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭ᦝ"),
  bstack11l1ll1_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᦞ"),
  bstack11l1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᦟ"),
  bstack11l1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩᦠ"),
  bstack11l1ll1_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭ᦡ"),
  bstack11l1ll1_opy_ (u"ࠪࡲࡴࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠧᦢ"),
  bstack11l1ll1_opy_ (u"ࠫࡨ࡮ࡥࡤ࡭ࡘࡖࡑ࠭ᦣ"),
  bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᦤ"),
  bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡉ࡯ࡰ࡭࡬ࡩࡸ࠭ᦥ"),
  bstack11l1ll1_opy_ (u"ࠧࡤࡣࡳࡸࡺࡸࡥࡄࡴࡤࡷ࡭࠭ᦦ"),
  bstack11l1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᦧ"),
  bstack11l1ll1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᦨ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡖࡦࡴࡶ࡭ࡴࡴࠧᦩ"),
  bstack11l1ll1_opy_ (u"ࠫࡳࡵࡂ࡭ࡣࡱ࡯ࡕࡵ࡬࡭࡫ࡱ࡫ࠬᦪ"),
  bstack11l1ll1_opy_ (u"ࠬࡳࡡࡴ࡭ࡖࡩࡳࡪࡋࡦࡻࡶࠫᦫ"),
  bstack11l1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡒ࡯ࡨࡵࠪ᦬"),
  bstack11l1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡉࡥࠩ᦭"),
  bstack11l1ll1_opy_ (u"ࠨࡦࡨࡨ࡮ࡩࡡࡵࡧࡧࡈࡪࡼࡩࡤࡧࠪ᦮"),
  bstack11l1ll1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡒࡤࡶࡦࡳࡳࠨ᦯"),
  bstack11l1ll1_opy_ (u"ࠪࡴ࡭ࡵ࡮ࡦࡐࡸࡱࡧ࡫ࡲࠨᦰ"),
  bstack11l1ll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩᦱ"),
  bstack11l1ll1_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡒࡴࡹ࡯࡯࡯ࡵࠪᦲ"),
  bstack11l1ll1_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫᦳ"),
  bstack11l1ll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᦴ"),
  bstack11l1ll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬᦵ"),
  bstack11l1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡄ࡬ࡳࡲ࡫ࡴࡳ࡫ࡦࠫᦶ"),
  bstack11l1ll1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࡘ࠵ࠫᦷ"),
  bstack11l1ll1_opy_ (u"ࠫࡲ࡯ࡤࡔࡧࡶࡷ࡮ࡵ࡮ࡊࡰࡶࡸࡦࡲ࡬ࡂࡲࡳࡷࠬᦸ"),
  bstack11l1ll1_opy_ (u"ࠬ࡫ࡳࡱࡴࡨࡷࡸࡵࡓࡦࡴࡹࡩࡷ࠭ᦹ"),
  bstack11l1ll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬᦺ"),
  bstack11l1ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡅࡧࡴࠬᦻ"),
  bstack11l1ll1_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨᦼ"),
  bstack11l1ll1_opy_ (u"ࠩࡶࡽࡳࡩࡔࡪ࡯ࡨ࡛࡮ࡺࡨࡏࡖࡓࠫᦽ"),
  bstack11l1ll1_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᦾ"),
  bstack11l1ll1_opy_ (u"ࠫ࡬ࡶࡳࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᦿ"),
  bstack11l1ll1_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ᧀ"),
  bstack11l1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ᧁ"),
  bstack11l1ll1_opy_ (u"ࠧࡧࡱࡵࡧࡪࡉࡨࡢࡰࡪࡩࡏࡧࡲࠨᧂ"),
  bstack11l1ll1_opy_ (u"ࠨࡺࡰࡷࡏࡧࡲࠨᧃ"),
  bstack11l1ll1_opy_ (u"ࠩࡻࡱࡽࡐࡡࡳࠩᧄ"),
  bstack11l1ll1_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩᧅ"),
  bstack11l1ll1_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫᧆ"),
  bstack11l1ll1_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭ᧇ"),
  bstack11l1ll1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᧈ"),
  bstack11l1ll1_opy_ (u"ࠧࡢࡲࡳ࡚ࡪࡸࡳࡪࡱࡱࠫᧉ"),
  bstack11l1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧ᧊"),
  bstack11l1ll1_opy_ (u"ࠩࡵࡩࡸ࡯ࡧ࡯ࡃࡳࡴࠬ᧋"),
  bstack11l1ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳࡹࠧ᧌"),
  bstack11l1ll1_opy_ (u"ࠫࡨࡧ࡮ࡢࡴࡼࠫ᧍"),
  bstack11l1ll1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭᧎"),
  bstack11l1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭᧏"),
  bstack11l1ll1_opy_ (u"ࠧࡪࡧࠪ᧐"),
  bstack11l1ll1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭᧑"),
  bstack11l1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ᧒"),
  bstack11l1ll1_opy_ (u"ࠪࡵࡺ࡫ࡵࡦࠩ᧓"),
  bstack11l1ll1_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡱࡥࡱ࠭᧔"),
  bstack11l1ll1_opy_ (u"ࠬࡧࡰࡱࡕࡷࡳࡷ࡫ࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳ࠭᧕"),
  bstack11l1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡉࡡ࡮ࡧࡵࡥࡎࡳࡡࡨࡧࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬ᧖"),
  bstack11l1ll1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡊࡾࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪ᧗"),
  bstack11l1ll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡏ࡮ࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫ᧘"),
  bstack11l1ll1_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭᧙"),
  bstack11l1ll1_opy_ (u"ࠪࡶࡪࡹࡥࡳࡸࡨࡈࡪࡼࡩࡤࡧࠪ᧚"),
  bstack11l1ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ᧛"),
  bstack11l1ll1_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧ᧜"),
  bstack11l1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡡࡴࡵࡦࡳࡩ࡫ࠧ᧝"),
  bstack11l1ll1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡉࡰࡵࡇࡩࡻ࡯ࡣࡦࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ᧞"),
  bstack11l1ll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡷࡧ࡭ࡴࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨ᧟"),
  bstack11l1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡳࡴࡱ࡫ࡐࡢࡻࠪ᧠"),
  bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ᧡"),
  bstack11l1ll1_opy_ (u"ࠫࡼࡪࡩࡰࡕࡨࡶࡻ࡯ࡣࡦࠩ᧢"),
  bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᧣"),
  bstack11l1ll1_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡃࡳࡱࡶࡷࡘ࡯ࡴࡦࡖࡵࡥࡨࡱࡩ࡯ࡩࠪ᧤"),
  bstack11l1ll1_opy_ (u"ࠧࡩ࡫ࡪ࡬ࡈࡵ࡮ࡵࡴࡤࡷࡹ࠭᧥"),
  bstack11l1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡑࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࡷࠬ᧦"),
  bstack11l1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬ᧧"),
  bstack11l1ll1_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧ᧨"),
  bstack11l1ll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡸࡨࡍࡔ࡙ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࡐࡴࡩࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ᧩"),
  bstack11l1ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ᧪"),
  bstack11l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᧫"),
  bstack11l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᧬"),
  bstack11l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧ᧭"),
  bstack11l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ᧮"),
  bstack11l1ll1_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭᧯"),
  bstack11l1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ᧰"),
  bstack11l1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧ᧱"),
  bstack11l1ll1_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ᧲")
]
bstack1ll11lll1_opy_ = {
  bstack11l1ll1_opy_ (u"ࠧࡷࠩ᧳"): bstack11l1ll1_opy_ (u"ࠨࡸࠪ᧴"),
  bstack11l1ll1_opy_ (u"ࠩࡩࠫ᧵"): bstack11l1ll1_opy_ (u"ࠪࡪࠬ᧶"),
  bstack11l1ll1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪ᧷"): bstack11l1ll1_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫ᧸"),
  bstack11l1ll1_opy_ (u"࠭࡯࡯࡮ࡼࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᧹"): bstack11l1ll1_opy_ (u"ࠧࡰࡰ࡯ࡽࡆࡻࡴࡰ࡯ࡤࡸࡪ࠭᧺"),
  bstack11l1ll1_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬ᧻"): bstack11l1ll1_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭᧼"),
  bstack11l1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭᧽"): bstack11l1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧ᧾"),
  bstack11l1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨ᧿"): bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩᨀ"),
  bstack11l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᨁ"): bstack11l1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᨂ"),
  bstack11l1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᨃ"): bstack11l1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᨄ"),
  bstack11l1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬᨅ"): bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡊࡲࡷࡹ࠭ᨆ"),
  bstack11l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧᨇ"): bstack11l1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨᨈ"),
  bstack11l1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᨉ"): bstack11l1ll1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫᨊ"),
  bstack11l1ll1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᨋ"): bstack11l1ll1_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᨌ"),
  bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᨍ"): bstack11l1ll1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨᨎ"),
  bstack11l1ll1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᨏ"): bstack11l1ll1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪᨐ"),
  bstack11l1ll1_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ᨑ"): bstack11l1ll1_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧᨒ"),
  bstack11l1ll1_opy_ (u"ࠫࡵࡧࡣࡧ࡫࡯ࡩࠬᨓ"): bstack11l1ll1_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᨔ"),
  bstack11l1ll1_opy_ (u"࠭ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᨕ"): bstack11l1ll1_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᨖ"),
  bstack11l1ll1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᨗ"): bstack11l1ll1_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩᨘࠬ"),
  bstack11l1ll1_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫᨙ"): bstack11l1ll1_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬᨚ"),
  bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᨛ"): bstack11l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᨜"),
  bstack11l1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩ᨝"): bstack11l1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡳࡩࡦࡺࡥࡳࠩ᨞")
}
bstack11l111ll1l1_opy_ = bstack11l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫࡮ࡺࡨࡶࡤ࠱ࡧࡴࡳ࠯ࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫࠲ࡶࡪࡲࡥࡢࡵࡨࡷ࠴ࡲࡡࡵࡧࡶࡸ࠴ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢ᨟")
bstack11l1111111l_opy_ = bstack11l1ll1_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠲࡬ࡪࡧ࡬ࡵࡪࡦ࡬ࡪࡩ࡫ࠣᨠ")
bstack1llll1lll_opy_ = bstack11l1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡫ࡤࡴ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡹࡥ࡯ࡦࡢࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢᨡ")
bstack1lll1111l_opy_ = bstack11l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ᨢ")
bstack111ll1l1l_opy_ = bstack11l1ll1_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩᨣ")
bstack1ll1l11lll_opy_ = bstack11l1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡰࡨࡼࡹࡥࡨࡶࡤࡶࠫᨤ")
bstack11lll1lll_opy_ = {
  bstack11l1ll1_opy_ (u"ࠨࡦࡨࡪࡦࡻ࡬ࡵࠩᨥ"): bstack11l1ll1_opy_ (u"ࠩ࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᨦ"),
  bstack11l1ll1_opy_ (u"ࠪࡹࡸ࠳ࡥࡢࡵࡷࠫᨧ"): bstack11l1ll1_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡷࡶࡩ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᨨ"),
  bstack11l1ll1_opy_ (u"ࠬࡻࡳࠨᨩ"): bstack11l1ll1_opy_ (u"࠭ࡨࡶࡤ࠰ࡹࡸ࠳࡯࡯࡮ࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᨪ"),
  bstack11l1ll1_opy_ (u"ࠧࡦࡷࠪᨫ"): bstack11l1ll1_opy_ (u"ࠨࡪࡸࡦ࠲࡫ࡵ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᨬ"),
  bstack11l1ll1_opy_ (u"ࠩ࡬ࡲࠬᨭ"): bstack11l1ll1_opy_ (u"ࠪ࡬ࡺࡨ࠭ࡢࡲࡶ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᨮ"),
  bstack11l1ll1_opy_ (u"ࠫࡦࡻࠧᨯ"): bstack11l1ll1_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡤࡴࡸ࡫࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᨰ")
}
bstack11l11l11111_opy_ = {
  bstack11l1ll1_opy_ (u"࠭ࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠨᨱ"): 50,
  bstack11l1ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᨲ"): 40,
  bstack11l1ll1_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩᨳ"): 30,
  bstack11l1ll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᨴ"): 20,
  bstack11l1ll1_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᨵ"): 10
}
bstack1l1ll1l11_opy_ = bstack11l11l11111_opy_[bstack11l1ll1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᨶ")]
bstack1l1l1111_opy_ = bstack11l1ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᨷ")
bstack1ll11ll1_opy_ = bstack11l1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᨸ")
bstack111l1l1l_opy_ = bstack11l1ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᨹ")
bstack111l1ll1l_opy_ = bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᨺ")
bstack1ll1l111ll_opy_ = bstack11l1ll1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡥࡳࡪࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡳࡥࡨࡱࡡࡨࡧࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧᨻ")
bstack11l11111l1_opy_ = {
  bstack11l1ll1_opy_ (u"ࠪࡗࡉࡑ࠭ࡈࡇࡑ࠱࠵࠶࠵ࠨᨼ"): bstack11l1ll1_opy_ (u"ࠫ࠯࠰ࠪࠡ࡝ࡖࡈࡐ࠳ࡇࡆࡐ࠰࠴࠵࠻࡝ࠡࡢࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡤࠥ࡯ࡳࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠤ࡮ࡴࠠࡺࡱࡸࡶࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠱ࠤ࡙࡮ࡩࡴࠢࡰࡥࡾࠦࡣࡢࡷࡶࡩࠥࡩ࡯࡯ࡨ࡯࡭ࡨࡺࡳࠡࡹ࡬ࡸ࡭ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࠦࡩࡵࠢࡸࡷ࡮ࡴࡧ࠻ࠢࡳ࡭ࡵࠦࡵ࡯࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠤ࠯࠰ࠪࠨᨽ")
}
bstack11l11l11lll_opy_ = [bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᨾ"), bstack11l1ll1_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᨿ")]
bstack11l11l1l111_opy_ = [bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᩀ"), bstack11l1ll1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᩁ")]
bstack1l1l1l11l_opy_ = re.compile(bstack11l1ll1_opy_ (u"ࠩࡡ࡟ࡡࡢࡷ࠮࡟࠮࠾࠳࠰ࠤࠨᩂ"))
bstack1l11l111ll_opy_ = [
  bstack11l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡎࡢ࡯ࡨࠫᩃ"),
  bstack11l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᩄ"),
  bstack11l1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᩅ"),
  bstack11l1ll1_opy_ (u"࠭࡮ࡦࡹࡆࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪᩆ"),
  bstack11l1ll1_opy_ (u"ࠧࡢࡲࡳࠫᩇ"),
  bstack11l1ll1_opy_ (u"ࠨࡷࡧ࡭ࡩ࠭ᩈ"),
  bstack11l1ll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫᩉ"),
  bstack11l1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࠪᩊ"),
  bstack11l1ll1_opy_ (u"ࠫࡴࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᩋ"),
  bstack11l1ll1_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࠪᩌ"),
  bstack11l1ll1_opy_ (u"࠭࡮ࡰࡔࡨࡷࡪࡺࠧᩍ"), bstack11l1ll1_opy_ (u"ࠧࡧࡷ࡯ࡰࡗ࡫ࡳࡦࡶࠪᩎ"),
  bstack11l1ll1_opy_ (u"ࠨࡥ࡯ࡩࡦࡸࡓࡺࡵࡷࡩࡲࡌࡩ࡭ࡧࡶࠫᩏ"),
  bstack11l1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡕ࡫ࡰ࡭ࡳ࡭ࡳࠨᩐ"),
  bstack11l1ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࡌࡰࡩࡪ࡭ࡳ࡭ࠧᩑ"),
  bstack11l1ll1_opy_ (u"ࠫࡴࡺࡨࡦࡴࡄࡴࡵࡹࠧᩒ"),
  bstack11l1ll1_opy_ (u"ࠬࡶࡲࡪࡰࡷࡔࡦ࡭ࡥࡔࡱࡸࡶࡨ࡫ࡏ࡯ࡈ࡬ࡲࡩࡌࡡࡪ࡮ࡸࡶࡪ࠭ᩓ"),
  bstack11l1ll1_opy_ (u"࠭ࡡࡱࡲࡄࡧࡹ࡯ࡶࡪࡶࡼࠫᩔ"), bstack11l1ll1_opy_ (u"ࠧࡢࡲࡳࡔࡦࡩ࡫ࡢࡩࡨࠫᩕ"), bstack11l1ll1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡃࡦࡸ࡮ࡼࡩࡵࡻࠪᩖ"), bstack11l1ll1_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡓࡥࡨࡱࡡࡨࡧࠪᩗ"), bstack11l1ll1_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᩘ"),
  bstack11l1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩᩙ"),
  bstack11l1ll1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡪࡹࡴࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩᩚ"),
  bstack11l1ll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࠨᩛ"), bstack11l1ll1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࡇࡱࡨࡎࡴࡴࡦࡰࡷࠫᩜ"),
  bstack11l1ll1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᩝ"),
  bstack11l1ll1_opy_ (u"ࠩࡤࡨࡧࡖ࡯ࡳࡶࠪᩞ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡖࡳࡨࡱࡥࡵࠩ᩟"),
  bstack11l1ll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰ࡙࡯࡭ࡦࡱࡸࡸ᩠ࠬ"),
  bstack11l1ll1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡵࡪࠪᩡ"),
  bstack11l1ll1_opy_ (u"࠭ࡡࡷࡦࠪᩢ"), bstack11l1ll1_opy_ (u"ࠧࡢࡸࡧࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪᩣ"), bstack11l1ll1_opy_ (u"ࠨࡣࡹࡨࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪᩤ"), bstack11l1ll1_opy_ (u"ࠩࡤࡺࡩࡇࡲࡨࡵࠪᩥ"),
  bstack11l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡋࡦࡻࡶࡸࡴࡸࡥࠨᩦ"), bstack11l1ll1_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡵࡪࠪᩧ"), bstack11l1ll1_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡵࡶࡻࡴࡸࡤࠨᩨ"),
  bstack11l1ll1_opy_ (u"࠭࡫ࡦࡻࡄࡰ࡮ࡧࡳࠨᩩ"), bstack11l1ll1_opy_ (u"ࠧ࡬ࡧࡼࡔࡦࡹࡳࡸࡱࡵࡨࠬᩪ"),
  bstack11l1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪᩫ"), bstack11l1ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡂࡴࡪࡷࠬᩬ"), bstack11l1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࡉ࡯ࡲࠨᩭ"), bstack11l1ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡆ࡬ࡷࡵ࡭ࡦࡏࡤࡴࡵ࡯࡮ࡨࡈ࡬ࡰࡪ࠭ᩮ"), bstack11l1ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵ࡙ࡸ࡫ࡓࡺࡵࡷࡩࡲࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩᩯ"),
  bstack11l1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࠩᩰ"), bstack11l1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࡶࠫᩱ"),
  bstack11l1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡄࡪࡵࡤࡦࡱ࡫ࡂࡶ࡫࡯ࡨࡈ࡮ࡥࡤ࡭ࠪᩲ"),
  bstack11l1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࡔࡪ࡯ࡨࡳࡺࡺࠧᩳ"),
  bstack11l1ll1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡄࡧࡹ࡯࡯࡯ࠩᩴ"), bstack11l1ll1_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡇࡦࡺࡥࡨࡱࡵࡽࠬ᩵"), bstack11l1ll1_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡋࡲࡡࡨࡵࠪ᩶"), bstack11l1ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࡊࡰࡷࡩࡳࡺࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩ᩷"),
  bstack11l1ll1_opy_ (u"ࠧࡥࡱࡱࡸࡘࡺ࡯ࡱࡃࡳࡴࡔࡴࡒࡦࡵࡨࡸࠬ᩸"),
  bstack11l1ll1_opy_ (u"ࠨࡷࡱ࡭ࡨࡵࡤࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪ᩹"), bstack11l1ll1_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡌࡧࡼࡦࡴࡧࡲࡥࠩ᩺"),
  bstack11l1ll1_opy_ (u"ࠪࡲࡴ࡙ࡩࡨࡰࠪ᩻"),
  bstack11l1ll1_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨ࡙ࡳ࡯࡭ࡱࡱࡵࡸࡦࡴࡴࡗ࡫ࡨࡻࡸ࠭᩼"),
  bstack11l1ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡥࡴࡲ࡭ࡩ࡝ࡡࡵࡥ࡫ࡩࡷࡹࠧ᩽"),
  bstack11l1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᩾"),
  bstack11l1ll1_opy_ (u"ࠧࡳࡧࡦࡶࡪࡧࡴࡦࡅ࡫ࡶࡴࡳࡥࡅࡴ࡬ࡺࡪࡸࡓࡦࡵࡶ࡭ࡴࡴࡳࠨ᩿"),
  bstack11l1ll1_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ᪀"),
  bstack11l1ll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡖࡡࡵࡪࠪ᪁"),
  bstack11l1ll1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡗࡵ࡫ࡥࡥࠩ᪂"),
  bstack11l1ll1_opy_ (u"ࠫ࡬ࡶࡳࡆࡰࡤࡦࡱ࡫ࡤࠨ᪃"),
  bstack11l1ll1_opy_ (u"ࠬ࡯ࡳࡉࡧࡤࡨࡱ࡫ࡳࡴࠩ᪄"),
  bstack11l1ll1_opy_ (u"࠭ࡡࡥࡤࡈࡼࡪࡩࡔࡪ࡯ࡨࡳࡺࡺࠧ᪅"),
  bstack11l1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࡓࡤࡴ࡬ࡴࡹ࠭᪆"),
  bstack11l1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡊࡥࡷ࡫ࡦࡩࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬ᪇"),
  bstack11l1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡇࡳࡣࡱࡸࡕ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠩ᪈"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡒࡦࡺࡵࡳࡣ࡯ࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨ᪉"),
  bstack11l1ll1_opy_ (u"ࠫࡸࡿࡳࡵࡧࡰࡔࡴࡸࡴࠨ᪊"),
  bstack11l1ll1_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡪࡢࡉࡱࡶࡸࠬ᪋"),
  bstack11l1ll1_opy_ (u"࠭ࡳ࡬࡫ࡳ࡙ࡳࡲ࡯ࡤ࡭ࠪ᪌"), bstack11l1ll1_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡔࡺࡲࡨࠫ᪍"), bstack11l1ll1_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡌࡧࡼࠫ᪎"),
  bstack11l1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡌࡢࡷࡱࡧ࡭࠭᪏"),
  bstack11l1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡧࡦࡺࡃࡢࡲࡷࡹࡷ࡫ࠧ᪐"),
  bstack11l1ll1_opy_ (u"ࠫࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࡏࡵࡪࡨࡶࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭᪑"),
  bstack11l1ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪ࡝ࡩ࡯ࡦࡲࡻࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࠧ᪒"),
  bstack11l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡵ࡯࡭ࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ᪓"),
  bstack11l1ll1_opy_ (u"ࠧࡦࡰࡩࡳࡷࡩࡥࡂࡲࡳࡍࡳࡹࡴࡢ࡮࡯ࠫ᪔"),
  bstack11l1ll1_opy_ (u"ࠨࡧࡱࡷࡺࡸࡥࡘࡧࡥࡺ࡮࡫ࡷࡴࡊࡤࡺࡪࡖࡡࡨࡧࡶࠫ᪕"), bstack11l1ll1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡇࡩࡻࡺ࡯ࡰ࡮ࡶࡔࡴࡸࡴࠨ᪖"), bstack11l1ll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧ࡚ࡩࡧࡼࡩࡦࡹࡇࡩࡹࡧࡩ࡭ࡵࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠭᪗"),
  bstack11l1ll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡵࡶࡳࡄࡣࡦ࡬ࡪࡒࡩ࡮࡫ࡷࠫ᪘"),
  bstack11l1ll1_opy_ (u"ࠬࡩࡡ࡭ࡧࡱࡨࡦࡸࡆࡰࡴࡰࡥࡹ࠭᪙"),
  bstack11l1ll1_opy_ (u"࠭ࡢࡶࡰࡧࡰࡪࡏࡤࠨ᪚"),
  bstack11l1ll1_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ᪛"),
  bstack11l1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡉࡳࡧࡢ࡭ࡧࡧࠫ᪜"), bstack11l1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡆࡻࡴࡩࡱࡵ࡭ࡿ࡫ࡤࠨ᪝"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯ࡂࡥࡦࡩࡵࡺࡁ࡭ࡧࡵࡸࡸ࠭᪞"), bstack11l1ll1_opy_ (u"ࠫࡦࡻࡴࡰࡆ࡬ࡷࡲ࡯ࡳࡴࡃ࡯ࡩࡷࡺࡳࠨ᪟"),
  bstack11l1ll1_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡴࡎ࡬ࡦࠬ᪠"),
  bstack11l1ll1_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡖࡤࡴࠬ᪡"),
  bstack11l1ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉ࡯࡫ࡷ࡭ࡦࡲࡕࡳ࡮ࠪ᪢"), bstack11l1ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡂ࡮࡯ࡳࡼࡖ࡯ࡱࡷࡳࡷࠬ᪣"), bstack11l1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡪࡲࡴࡸࡥࡇࡴࡤࡹࡩ࡝ࡡࡳࡰ࡬ࡲ࡬࠭᪤"), bstack11l1ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡪࡴࡌࡪࡰ࡮ࡷࡎࡴࡂࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠪ᪥"),
  bstack11l1ll1_opy_ (u"ࠫࡰ࡫ࡥࡱࡍࡨࡽࡈ࡮ࡡࡪࡰࡶࠫ᪦"),
  bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡿࡧࡢ࡭ࡧࡖࡸࡷ࡯࡮ࡨࡵࡇ࡭ࡷ࠭ᪧ"),
  bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩ᪨"),
  bstack11l1ll1_opy_ (u"ࠧࡪࡰࡷࡩࡷࡑࡥࡺࡆࡨࡰࡦࡿࠧ᪩"),
  bstack11l1ll1_opy_ (u"ࠨࡵ࡫ࡳࡼࡏࡏࡔࡎࡲ࡫ࠬ᪪"),
  bstack11l1ll1_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡖࡸࡷࡧࡴࡦࡩࡼࠫ᪫"),
  bstack11l1ll1_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡕࡩࡸࡶ࡯࡯ࡵࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ᪬"), bstack11l1ll1_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡘࡣ࡬ࡸ࡙࡯࡭ࡦࡱࡸࡸࠬ᪭"),
  bstack11l1ll1_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࠨ᪮"),
  bstack11l1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡳࡺࡰࡦࡉࡽ࡫ࡣࡶࡶࡨࡊࡷࡵ࡭ࡉࡶࡷࡴࡸ࠭᪯"),
  bstack11l1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡄࡣࡳࡸࡺࡸࡥࠨ᪰"),
  bstack11l1ll1_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨ᪱"),
  bstack11l1ll1_opy_ (u"ࠩࡩࡹࡱࡲࡃࡰࡰࡷࡩࡽࡺࡌࡪࡵࡷࠫ᪲"),
  bstack11l1ll1_opy_ (u"ࠪࡻࡦ࡯ࡴࡇࡱࡵࡅࡵࡶࡓࡤࡴ࡬ࡴࡹ࠭᪳"),
  bstack11l1ll1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡈࡵ࡮࡯ࡧࡦࡸࡗ࡫ࡴࡳ࡫ࡨࡷࠬ᪴"),
  bstack11l1ll1_opy_ (u"ࠬࡧࡰࡱࡐࡤࡱࡪ᪵࠭"),
  bstack11l1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡓࡍࡅࡨࡶࡹ᪶࠭"),
  bstack11l1ll1_opy_ (u"ࠧࡵࡣࡳ࡛࡮ࡺࡨࡔࡪࡲࡶࡹࡖࡲࡦࡵࡶࡈࡺࡸࡡࡵ࡫ࡲࡲ᪷ࠬ"),
  bstack11l1ll1_opy_ (u"ࠨࡵࡦࡥࡱ࡫ࡆࡢࡥࡷࡳࡷ᪸࠭"),
  bstack11l1ll1_opy_ (u"ࠩࡺࡨࡦࡒ࡯ࡤࡣ࡯ࡔࡴࡸࡴࠨ᪹"),
  bstack11l1ll1_opy_ (u"ࠪࡷ࡭ࡵࡷ࡙ࡥࡲࡨࡪࡒ࡯ࡨ᪺ࠩ"),
  bstack11l1ll1_opy_ (u"ࠫ࡮ࡵࡳࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡸࡷࡪ࠭᪻"),
  bstack11l1ll1_opy_ (u"ࠬࡾࡣࡰࡦࡨࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠧ᪼"),
  bstack11l1ll1_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡶࡷࡼࡵࡲࡥ᪽ࠩ"),
  bstack11l1ll1_opy_ (u"ࠧࡶࡵࡨࡔࡷ࡫ࡢࡶ࡫࡯ࡸ࡜ࡊࡁࠨ᪾"),
  bstack11l1ll1_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵ࡙ࡇࡅࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴᪿࠩ"),
  bstack11l1ll1_opy_ (u"ࠩࡺࡩࡧࡊࡲࡪࡸࡨࡶࡆ࡭ࡥ࡯ࡶࡘࡶࡱᫀ࠭"),
  bstack11l1ll1_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡴࡩࠩ᫁"),
  bstack11l1ll1_opy_ (u"ࠫࡺࡹࡥࡏࡧࡺ࡛ࡉࡇࠧ᫂"),
  bstack11l1ll1_opy_ (u"ࠬࡽࡤࡢࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨ᫃"), bstack11l1ll1_opy_ (u"࠭ࡷࡥࡣࡆࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࡚ࡩ࡮ࡧࡲࡹࡹ᫄࠭"),
  bstack11l1ll1_opy_ (u"ࠧࡹࡥࡲࡨࡪࡕࡲࡨࡋࡧࠫ᫅"), bstack11l1ll1_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡓࡪࡩࡱ࡭ࡳ࡭ࡉࡥࠩ᫆"),
  bstack11l1ll1_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦ࡚ࡈࡆࡈࡵ࡯ࡦ࡯ࡩࡎࡪࠧ᫇"),
  bstack11l1ll1_opy_ (u"ࠪࡶࡪࡹࡥࡵࡑࡱࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡲࡵࡑࡱࡰࡾ࠭᫈"),
  bstack11l1ll1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࡸ࠭᫉"),
  bstack11l1ll1_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷ࡯ࡥࡴ᫊ࠩ"), bstack11l1ll1_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡹࡊࡰࡷࡩࡷࡼࡡ࡭ࠩ᫋"),
  bstack11l1ll1_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࡉࡣࡵࡨࡼࡧࡲࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪᫌ"),
  bstack11l1ll1_opy_ (u"ࠨ࡯ࡤࡼ࡙ࡿࡰࡪࡰࡪࡊࡷ࡫ࡱࡶࡧࡱࡧࡾ࠭ᫍ"),
  bstack11l1ll1_opy_ (u"ࠩࡶ࡭ࡲࡶ࡬ࡦࡋࡶ࡚࡮ࡹࡩࡣ࡮ࡨࡇ࡭࡫ࡣ࡬ࠩᫎ"),
  bstack11l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡃࡢࡴࡷ࡬ࡦ࡭ࡥࡔࡵ࡯ࠫ᫏"),
  bstack11l1ll1_opy_ (u"ࠫࡸ࡮࡯ࡶ࡮ࡧ࡙ࡸ࡫ࡓࡪࡰࡪࡰࡪࡺ࡯࡯ࡖࡨࡷࡹࡓࡡ࡯ࡣࡪࡩࡷ࠭᫐"),
  bstack11l1ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡍ࡜ࡊࡐࠨ᫑"),
  bstack11l1ll1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙ࡵࡵࡤࡪࡌࡨࡊࡴࡲࡰ࡮࡯ࠫ᫒"),
  bstack11l1ll1_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡈࡪࡦࡧࡩࡳࡇࡰࡪࡒࡲࡰ࡮ࡩࡹࡆࡴࡵࡳࡷ࠭᫓"),
  bstack11l1ll1_opy_ (u"ࠨ࡯ࡲࡧࡰࡒ࡯ࡤࡣࡷ࡭ࡴࡴࡁࡱࡲࠪ᫔"),
  bstack11l1ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈࡲࡶࡲࡧࡴࠨ᫕"), bstack11l1ll1_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉ࡭ࡱࡺࡥࡳࡕࡳࡩࡨࡹࠧ᫖"),
  bstack11l1ll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡇࡩࡱࡧࡹࡂࡦࡥࠫ᫗"),
  bstack11l1ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡏࡤࡍࡱࡦࡥࡹࡵࡲࡂࡷࡷࡳࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠨ᫘")
]
bstack1llll11lll_opy_ = bstack11l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡻࡰ࡭ࡱࡤࡨࠬ᫙")
bstack11l11lllll_opy_ = [bstack11l1ll1_opy_ (u"ࠧ࠯ࡣࡳ࡯ࠬ᫚"), bstack11l1ll1_opy_ (u"ࠨ࠰ࡤࡥࡧ࠭᫛"), bstack11l1ll1_opy_ (u"ࠩ࠱࡭ࡵࡧࠧ᫜")]
bstack1l1ll11lll_opy_ = [bstack11l1ll1_opy_ (u"ࠪ࡭ࡩ࠭᫝"), bstack11l1ll1_opy_ (u"ࠫࡵࡧࡴࡩࠩ᫞"), bstack11l1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ᫟"), bstack11l1ll1_opy_ (u"࠭ࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࠬ᫠")]
bstack1l11l1l1l1_opy_ = {
  bstack11l1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᫡"): bstack11l1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᫢"),
  bstack11l1ll1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ᫣"): bstack11l1ll1_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ᫤"),
  bstack11l1ll1_opy_ (u"ࠫࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫥"): bstack11l1ll1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᫦"),
  bstack11l1ll1_opy_ (u"࠭ࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫧"): bstack11l1ll1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᫨"),
  bstack11l1ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡷ࡭ࡴࡴࡳࠨ᫩"): bstack11l1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ᫪")
}
bstack1l111l1lll_opy_ = [
  bstack11l1ll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᫫"),
  bstack11l1ll1_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫬"),
  bstack11l1ll1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᫭"),
  bstack11l1ll1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ᫮"),
  bstack11l1ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ᫯"),
]
bstack111111lll_opy_ = bstack1ll11111l_opy_ + bstack11l1111llll_opy_ + bstack1l11l111ll_opy_
bstack1ll1111l_opy_ = [
  bstack11l1ll1_opy_ (u"ࠨࡠ࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸࠩ࠭᫰"),
  bstack11l1ll1_opy_ (u"ࠩࡡࡦࡸ࠳࡬ࡰࡥࡤࡰ࠳ࡩ࡯࡮ࠦࠪ᫱"),
  bstack11l1ll1_opy_ (u"ࠪࡢ࠶࠸࠷࠯ࠩ᫲"),
  bstack11l1ll1_opy_ (u"ࠫࡣ࠷࠰࠯ࠩ᫳"),
  bstack11l1ll1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠵ࡠ࠼࠭࠺࡟࠱ࠫ᫴"),
  bstack11l1ll1_opy_ (u"࠭࡞࠲࠹࠵࠲࠷ࡡ࠰࠮࠻ࡠ࠲ࠬ᫵"),
  bstack11l1ll1_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠹࡛࠱࠯࠴ࡡ࠳࠭᫶"),
  bstack11l1ll1_opy_ (u"ࠨࡠ࠴࠽࠷࠴࠱࠷࠺࠱ࠫ᫷")
]
bstack11l11llll1l_opy_ = bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ᫸")
bstack11l11ll11_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠯ࡷ࠳࠲ࡩࡻ࡫࡮ࡵࠩ᫹")
bstack111lll1ll1_opy_ = [ bstack11l1ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᫺") ]
bstack111llll11l_opy_ = [ bstack11l1ll1_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᫻") ]
bstack11llll111l_opy_ = [bstack11l1ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᫼")]
bstack1ll1l1lll1_opy_ = [ bstack11l1ll1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᫽") ]
bstack11l1l11l_opy_ = bstack11l1ll1_opy_ (u"ࠨࡕࡇࡏࡘ࡫ࡴࡶࡲࠪ᫾")
bstack11lll11l11_opy_ = bstack11l1ll1_opy_ (u"ࠩࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠬ᫿")
bstack1ll1l11111_opy_ = bstack11l1ll1_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠧᬀ")
bstack1l1l1ll1ll_opy_ = bstack11l1ll1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࠪᬁ")
bstack111l11ll11_opy_ = [
  bstack11l1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡉࡅࡎࡒࡅࡅࠩᬂ"),
  bstack11l1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ᬃ"),
  bstack11l1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡇࡒࡏࡄࡍࡈࡈࡤࡈ࡙ࡠࡅࡏࡍࡊࡔࡔࠨᬄ"),
  bstack11l1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡔࡅࡕ࡙ࡒࡖࡐࡥࡃࡉࡃࡑࡋࡊࡊࠧᬅ"),
  bstack11l1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡉ࡙ࡥࡎࡐࡖࡢࡇࡔࡔࡎࡆࡅࡗࡉࡉ࠭ᬆ"),
  bstack11l1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡈࡒࡏࡔࡇࡇࠫᬇ"),
  bstack11l1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡘࡅࡔࡇࡗࠫᬈ"),
  bstack11l1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡈࡘࡗࡊࡊࠧᬉ"),
  bstack11l1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡂࡄࡒࡖ࡙ࡋࡄࠨᬊ"),
  bstack11l1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᬋ"),
  bstack11l1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡒࡔ࡚࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࠩᬌ"),
  bstack11l1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡁࡅࡆࡕࡉࡘ࡙࡟ࡊࡐ࡙ࡅࡑࡏࡄࠨᬍ"),
  bstack11l1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡗࡑࡖࡊࡇࡃࡉࡃࡅࡐࡊ࠭ᬎ"),
  bstack11l1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡖࡘࡒࡓࡋࡌࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬᬏ"),
  bstack11l1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡔࡊࡏࡈࡈࡤࡕࡕࡕࠩᬐ"),
  bstack11l1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡔࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᬑ"),
  bstack11l1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡉࡑࡖࡘࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪᬒ"),
  bstack11l1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᬓ"),
  bstack11l1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪᬔ"),
  bstack11l1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡘࡅࡔࡑࡏ࡙࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᬕ"),
  bstack11l1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡏࡄࡒࡉࡇࡔࡐࡔ࡜ࡣࡕࡘࡏ࡙࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᬖ"),
]
bstack111ll11l1_opy_ = bstack11l1ll1_opy_ (u"ࠬ࠴࠯ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠱ࠪᬗ")
bstack1l1l11l11l_opy_ = os.path.join(os.path.expanduser(bstack11l1ll1_opy_ (u"࠭ࡾࠨᬘ")), bstack11l1ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᬙ"), bstack11l1ll1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᬚ"))
bstack11l1l11l111_opy_ = bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱ࡫ࠪᬛ")
bstack11l111l1111_opy_ = [ bstack11l1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᬜ"), bstack11l1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᬝ"), bstack11l1ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫᬞ"), bstack11l1ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᬟ")]
bstack1ll111ll1_opy_ = [ bstack11l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᬠ"), bstack11l1ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᬡ"), bstack11l1ll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨᬢ"), bstack11l1ll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᬣ") ]
bstack11ll11l1l1_opy_ = [ bstack11l1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᬤ") ]
bstack11l1111l1ll_opy_ = [ bstack11l1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᬥ") ]
bstack1l11ll111_opy_ = 360
bstack11l11lll1ll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡡࡱࡲ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᬦ")
bstack11l111l1l1l_opy_ = bstack11l1ll1_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡬ࡷࡸࡻࡥࡴࠤᬧ")
bstack11l111ll11l_opy_ = bstack11l1ll1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠦᬨ")
bstack11l1ll11ll1_opy_ = bstack11l1ll1_opy_ (u"ࠤࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡸࡪࡹࡴࡴࠢࡤࡶࡪࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡲࡲࠥࡕࡓࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࠨࡷࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥࠡࡨࡲࡶࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦࡤࡦࡸ࡬ࡧࡪࡹ࠮ࠣᬩ")
bstack11l1ll1111l_opy_ = bstack11l1ll1_opy_ (u"ࠥ࠵࠶࠴࠰ࠣᬪ")
bstack1lllllll1l1_opy_ = {
  bstack11l1ll1_opy_ (u"ࠫࡕࡇࡓࡔࠩᬫ"): bstack11l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᬬ"),
  bstack11l1ll1_opy_ (u"࠭ࡆࡂࡋࡏࠫᬭ"): bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᬮ"),
  bstack11l1ll1_opy_ (u"ࠨࡕࡎࡍࡕ࠭ᬯ"): bstack11l1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᬰ")
}
bstack1lll1lllll_opy_ = [
  bstack11l1ll1_opy_ (u"ࠥ࡫ࡪࡺࠢᬱ"),
  bstack11l1ll1_opy_ (u"ࠦ࡬ࡵࡂࡢࡥ࡮ࠦᬲ"),
  bstack11l1ll1_opy_ (u"ࠧ࡭࡯ࡇࡱࡵࡻࡦࡸࡤࠣᬳ"),
  bstack11l1ll1_opy_ (u"ࠨࡲࡦࡨࡵࡩࡸ࡮᬴ࠢ"),
  bstack11l1ll1_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨᬵ"),
  bstack11l1ll1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᬶ"),
  bstack11l1ll1_opy_ (u"ࠤࡶࡹࡧࡳࡩࡵࡇ࡯ࡩࡲ࡫࡮ࡵࠤᬷ"),
  bstack11l1ll1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢᬸ"),
  bstack11l1ll1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢᬹ"),
  bstack11l1ll1_opy_ (u"ࠧࡩ࡬ࡦࡣࡵࡉࡱ࡫࡭ࡦࡰࡷࠦᬺ"),
  bstack11l1ll1_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࡹࠢᬻ"),
  bstack11l1ll1_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠢᬼ"),
  bstack11l1ll1_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡃࡶࡽࡳࡩࡓࡤࡴ࡬ࡴࡹࠨᬽ"),
  bstack11l1ll1_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣᬾ"),
  bstack11l1ll1_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᬿ"),
  bstack11l1ll1_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱ࡙ࡵࡵࡤࡪࡄࡧࡹ࡯࡯࡯ࠤᭀ"),
  bstack11l1ll1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡓࡵ࡭ࡶ࡬ࡘࡴࡻࡣࡩࠤᭁ"),
  bstack11l1ll1_opy_ (u"ࠨࡳࡩࡣ࡮ࡩࠧᭂ"),
  bstack11l1ll1_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࡇࡰࡱࠤᭃ")
]
bstack11l111l1ll1_opy_ = [
  bstack11l1ll1_opy_ (u"ࠣࡥ࡯࡭ࡨࡱ᭄ࠢ"),
  bstack11l1ll1_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᭅ"),
  bstack11l1ll1_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᭆ"),
  bstack11l1ll1_opy_ (u"ࠦࡲࡧ࡮ࡶࡣ࡯ࠦᭇ"),
  bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᭈ")
]
bstack1111ll1l_opy_ = {
  bstack11l1ll1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧᭉ"): [bstack11l1ll1_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨᭊ")],
  bstack11l1ll1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᭋ"): [bstack11l1ll1_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᭌ")],
  bstack11l1ll1_opy_ (u"ࠥࡥࡺࡺ࡯ࠣ᭍"): [bstack11l1ll1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣ᭎"), bstack11l1ll1_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣ᭏"), bstack11l1ll1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ᭐"), bstack11l1ll1_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨ᭑")],
  bstack11l1ll1_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣ᭒"): [bstack11l1ll1_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤ᭓")],
  bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ᭔"): [bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᭕")],
}
bstack11l111ll1ll_opy_ = {
  bstack11l1ll1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦ᭖"): bstack11l1ll1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧ᭗"),
  bstack11l1ll1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᭘"): bstack11l1ll1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᭙"),
  bstack11l1ll1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨ᭚"): bstack11l1ll1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧ᭛"),
  bstack11l1ll1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢ᭜"): bstack11l1ll1_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࠢ᭝"),
  bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ᭞"): bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ᭟")
}
bstack1111l11l11_opy_ = {
  bstack11l1ll1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ᭠"): bstack11l1ll1_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡕࡨࡸࡺࡶࠧ᭡"),
  bstack11l1ll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭᭢"): bstack11l1ll1_opy_ (u"ࠫࡘࡻࡩࡵࡧࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬ᭣"),
  bstack11l1ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ᭤"): bstack11l1ll1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡘ࡫ࡴࡶࡲࠪ᭥"),
  bstack11l1ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ᭦"): bstack11l1ll1_opy_ (u"ࠨࡖࡨࡷࡹࠦࡔࡦࡣࡵࡨࡴࡽ࡮ࠨ᭧")
}
bstack11l11111lll_opy_ = 65536
bstack11l1111l111_opy_ = bstack11l1ll1_opy_ (u"ࠩ࠱࠲࠳ࡡࡔࡓࡗࡑࡇࡆ࡚ࡅࡅ࡟ࠪ᭨")
bstack11l111l11ll_opy_ = [
      bstack11l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᭩"), bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᭪"), bstack11l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ᭫"), bstack11l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻ᭬ࠪ"), bstack11l1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩ᭭"),
      bstack11l1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ᭮"), bstack11l1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ᭯"), bstack11l1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫ᭰"), bstack11l1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬ᭱"),
      bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡐࡤࡱࡪ࠭᭲"), bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᭳"), bstack11l1ll1_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ᭴")
    ]
bstack11l11l11l11_opy_= {
  bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᭵"): bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᭶"),
  bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ᭷"): bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ᭸"),
  bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ᭹"): bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ᭺"),
  bstack11l1ll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᭻"): bstack11l1ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᭼"),
  bstack11l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᭽"): bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᭾"),
  bstack11l1ll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭᭿"): bstack11l1ll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᮀ"),
  bstack11l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᮁ"): bstack11l1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᮂ"),
  bstack11l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᮃ"): bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᮄ"),
  bstack11l1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᮅ"): bstack11l1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᮆ"),
  bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᮇ"): bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᮈ"),
  bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᮉ"): bstack11l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᮊ"),
  bstack11l1ll1_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࠩᮋ"): bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪᮌ"),
  bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᮍ"): bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᮎ"),
  bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࡕࡰࡵ࡫ࡲࡲࡸ࠭ᮏ"): bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࠧᮐ"),
  bstack11l1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᮑ"): bstack11l1ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᮒ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᮓ"): bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᮔ"),
  bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᮕ"): bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᮖ"),
  bstack11l1ll1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫᮗ"): bstack11l1ll1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᮘ"),
  bstack11l1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᮙ"): bstack11l1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᮚ"),
  bstack11l1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᮛ"): bstack11l1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᮜ"),
  bstack11l1ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᮝ"): bstack11l1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᮞ"),
  bstack11l1ll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᮟ"): bstack11l1ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᮠ"),
  bstack11l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᮡ"): bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᮢ"),
  bstack11l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᮣ"): bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᮤ"),
  bstack11l1ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᮥ"): bstack11l1ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᮦ"),
  bstack11l1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᮧ"): bstack11l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᮨ"),
  bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᮩ"): bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴ᮪ࠩ"),
  bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ᮫࠭"): bstack11l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᮬ")
}
bstack11l111lllll_opy_ = [bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᮭ"), bstack11l1ll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᮮ")]
bstack1l11l1111l_opy_ = (bstack11l1ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᮯ"),)
bstack11l11l111ll_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡺࡶࡤࡢࡶࡨࡣࡨࡲࡩࠨ᮰")
bstack1ll11lll_opy_ = bstack11l1ll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡩࡵ࡭ࡩࡹ࠯ࠣ᮱")
bstack11l11111ll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨࡴ࡬ࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡤࡷ࡭ࡨ࡯ࡢࡴࡧ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࠧ᮲")
bstack1l111lll1_opy_ = bstack11l1ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠰ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠣ᮳")
class EVENTS(Enum):
  bstack11l11111l11_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࠱࠲ࡻ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬ᮴")
  bstack11lll1111l_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࠧ᮵")
  bstack11111llll_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡥࡱ࡯ࡺࡦࠩ᮶")
  bstack11l111l111l_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡲ࡯ࡨࡵࠪ᮷")
  bstack1l11l1l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨ᮸") #shift post bstack11l111lll1l_opy_
  bstack1l1lll11l_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡶࡲࡪࡰࡷ࠱ࡧࡻࡩ࡭ࡦ࡯࡭ࡳࡱࠧ᮹") #shift post bstack11l111lll1l_opy_
  bstack11l11111ll1_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡪࡸࡦࠬᮺ") #shift
  bstack11l11l11l1l_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡩࡵࡷ࡯࡮ࡲࡥࡩ࠭ᮻ") #shift
  bstack11l1ll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽࡬ࡺࡨ࠭࡮ࡣࡱࡥ࡬࡫࡭ࡦࡰࡷࠫᮼ")
  bstack1l1ll1llll1_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿ࡹࡡࡷࡧ࠰ࡶࡪࡹࡵ࡭ࡶࡶࠫᮽ")
  bstack1l1l11llll_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡤࡳ࡫ࡹࡩࡷ࠳ࡰࡦࡴࡩࡳࡷࡳࡳࡤࡣࡱࠫᮾ")
  bstack1llll1llll_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡱࡵࡣࡢ࡮ࠪᮿ") #shift
  bstack1lll11l1ll_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡤࡴࡵ࠳ࡵࡱ࡮ࡲࡥࡩ࠭ᯀ") #shift
  bstack11l11l11ll_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡣࡪ࠯ࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠬᯁ")
  bstack1llll1l11l_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠭ࡳࡧࡶࡹࡱࡺࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠩᯂ") #shift
  bstack1lll11ll_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴࠩᯃ") #shift
  bstack11l111l11l1_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾ࠭ᯄ") #shift
  bstack1l11l1ll111_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫᯅ")
  bstack11l11l1lll_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡹࡴࡢࡶࡸࡷࠬᯆ") #shift
  bstack1l11ll11ll_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿࡮ࡵࡣ࠯ࡰࡥࡳࡧࡧࡦ࡯ࡨࡲࡹ࠭ᯇ")
  bstack11l11l1l11l_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸ࡯ࡹࡻ࠰ࡷࡪࡺࡵࡱࠩᯈ") #shift
  bstack11llll1l1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥࡵࡷࡳࠫᯉ")
  bstack11l11111l1l_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡹ࡮ࡢࡲࡶ࡬ࡴࡺࠧᯊ") # not bstack11l111111l1_opy_ in python
  bstack1lll111l_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡲࡷ࡬ࡸࠬᯋ") # used in bstack11l111111ll_opy_
  bstack11ll11l1l1l_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡵࡩ࠲ࡷࡵࡪࡶࠪᯌ")
  bstack11ll11l11ll_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡳࡸࡺ࠭ࡲࡷ࡬ࡸࠬᯍ")
  bstack1lllll111l_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽࡫ࡪࡺࠧᯎ") # used in bstack11l111111ll_opy_
  bstack11l111ll11_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾࡭ࡵ࡯࡬ࠩᯏ")
  bstack11ll11ll1l1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡦ࠯࡫ࡳࡴࡱࠧᯐ")
  bstack11ll11ll1ll_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡰࡰࡵࡷ࠱࡭ࡵ࡯࡬ࠩᯑ")
  bstack1l11l11l1l_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠨᯒ")
  bstack1111l1lll_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠨᯓ") #
  bstack1ll111ll_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡵࡣ࡮ࡩࡘࡩࡲࡦࡧࡱࡗ࡭ࡵࡴࠨᯔ")
  bstack1ll1l1l11_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡤࡹࡹࡵ࠭ࡤࡣࡳࡸࡺࡸࡥࠨᯕ")
  bstack1111l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸࡥ࠮ࡶࡨࡷࡹ࠭ᯖ")
  bstack111l1l1ll1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡶ࡯ࡴࡶ࠰ࡸࡪࡹࡴࠨᯗ")
  bstack111lll11ll_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡳࡧ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫᯘ") #shift
  bstack111lll11_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᯙ") #shift
  bstack11l111l1l11_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴ࠳ࡣࡢࡲࡷࡹࡷ࡫ࠧᯚ")
  bstack11l1111l1l1_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾࡮ࡪ࡬ࡦ࠯ࡷ࡭ࡲ࡫࡯ࡶࡶࠪᯛ")
  bstack11ll1l11l_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡩࡽ࡯ࡴ࠮ࡪࡤࡲࡩࡲࡥࡳࠩᯜ")
  bstack1ll11llllll_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡧࡻ࡭ࡹ࠳ࡨࡢࡰࡧࡰࡪࡸࠧᯝ")
  bstack11l111l1lll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࠰ࡱࡪࡺࡲࡪࡥࡶࠫᯞ")
  bstack11l1111ll11_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡴࡦࡵࡷ࡬ࡺࡨ࠺ࡴࡶࡲࡴࠬᯟ")
  bstack1ll11ll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡸࡺࡡࡳࡶࠪᯠ")
  bstack11l11l1111l_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧᯡ")
  bstack11l11l11ll1_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡣࡩࡧࡦ࡯࠲ࡻࡰࡥࡣࡷࡩࠬᯢ")
  bstack1ll11l1ll1l_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠭ᯣ")
  bstack1ll111l11ll_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡸࡺࡡࡳࡶࡥ࡭ࡳࡧࡲࡺࠩᯤ")
  bstack1ll11l1l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡩ࡯࡯ࡰࡨࡧࡹ࠭ᯥ")
  bstack1ll11lll1ll_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡳࡵࡱࡳ᯦ࠫ")
  bstack1ll1ll111ll_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡶࡤࡶࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩᯧ")
  bstack1ll11l11l11_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡥࡲࡲࡳ࡫ࡣࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲࠬᯨ")
  bstack11l111lll11_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹ࠭ᯩ")
  bstack11l11l111l1_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡪ࡮ࡴࡤࡏࡧࡤࡶࡪࡹࡴࡉࡷࡥࠫᯪ")
  bstack1l111l11l1l_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡌࡲ࡮ࡺࠧᯫ")
  bstack1l1111llll1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡲࡵࠩᯬ")
  bstack1l1ll1ll111_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡉ࡯࡯ࡨ࡬࡫ࠬᯭ")
  bstack11l111llll1_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡃࡰࡰࡩ࡭࡬࠭ᯮ")
  bstack1l1l1ll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࡬ࡗࡪࡲࡦࡉࡧࡤࡰࡘࡺࡥࡱࠩᯯ")
  bstack1l1l1ll11ll_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࡭ࡘ࡫࡬ࡧࡊࡨࡥࡱࡍࡥࡵࡔࡨࡷࡺࡲࡴࠨᯰ")
  bstack1l11lll1111_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡈࡺࡪࡴࡴࠨᯱ")
  bstack1l11ll11ll1_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺ᯲ࠧ")
  bstack1l11l1lll1l_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼࡯ࡳ࡬ࡉࡲࡦࡣࡷࡩࡩࡋࡶࡦࡰࡷ᯳ࠫ")
  bstack11l1111l11l_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡩࡳࡷࡵࡦࡷࡨࡘࡪࡹࡴࡆࡸࡨࡲࡹ࠭᯴")
  bstack1l11111ll1l_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡰࡲࠪ᯵")
  bstack1ll11ll1ll1_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡱࡱࡗࡹࡵࡰࠨ᯶")
  bstack11l1lllll1l_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰࡪࡧ࡮ࡶࡲࡘࡴࡱࡵࡡࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭᯷")
  bstack111ll1l1ll_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡴࡤࡇࡷࡱࡲࡪࡲࡔࡦࡵࡷࡅࡹࡺࡥ࡮ࡲࡷࡩࡩ࠭᯸")
  bstack1l1l11ll1_opy_ = bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫࡮ࡥࡈࡸࡲࡳ࡫࡬ࡕࡧࡶࡸࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠧ᯹")
  bstack1lllll11l1l_opy_ = bstack11l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡰࡱ࡮ࡼࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡓࡽࡹ࡫ࡳࡵࠩ᯺")
  bstack1llll11l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡶࡔࡾࡺࡥࡴࡶࠪ᯻")
  bstack1llll11l1l1_opy_ = bstack11l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡻࡷࡩࡸࡺࡇࡦࡶࡗࡳࡹࡧ࡬ࡕࡧࡶࡸࡸ࠭᯼")
class STAGE(Enum):
  bstack11ll1lll1l_opy_ = bstack11l1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪ᯽")
  END = bstack11l1ll1_opy_ (u"ࠬ࡫࡮ࡥࠩ᯾")
  bstack11lll1l1l1_opy_ = bstack11l1ll1_opy_ (u"࠭ࡳࡪࡰࡪࡰࡪ࠭᯿")
bstack1l1l1l11l1_opy_ = {
  bstack11l1ll1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧᰀ"): bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᰁ"),
  bstack11l1ll1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ᰂ"): bstack11l1ll1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᰃ")
}
PLAYWRIGHT_HUB_URL = bstack11l1ll1_opy_ (u"ࠦࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂࠨᰄ")
bstack1l1lllll111_opy_ = 98
bstack1l1ll1l1lll_opy_ = 100
bstack1llll1ll11l_opy_ = {
  bstack11l1ll1_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫᰅ"): bstack11l1ll1_opy_ (u"࠭࠭࠮ࡴࡨࡶࡺࡴࡳࠨᰆ"),
  bstack11l1ll1_opy_ (u"ࠧࡥࡧ࡯ࡥࡾ࠭ᰇ"): bstack11l1ll1_opy_ (u"ࠨ࠯࠰ࡶࡪࡸࡵ࡯ࡵ࠰ࡨࡪࡲࡡࡺࠩᰈ"),
  bstack11l1ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧᰉ"): 0
}
bstack11l1111ll1l_opy_ = bstack11l1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥᰊ")
bstack11l1111lll1_opy_ = bstack11l1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣᰋ")
bstack1l1llll11_opy_ = bstack11l1ll1_opy_ (u"࡚ࠧࡅࡔࡖࠣࡖࡊࡖࡏࡓࡖࡌࡒࡌࠦࡁࡏࡆࠣࡅࡓࡇࡌ࡚ࡖࡌࡇࡘࠨᰌ")