# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import re
from enum import Enum
bstack111ll111l1_opy_ = {
  bstack11lllll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᣎ"): bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷ࠭ᣏ"),
  bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᣐ"): bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡯ࡪࡿࠧᣑ"),
  bstack11lllll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᣒ"): bstack11lllll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᣓ"),
  bstack11lllll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᣔ"): bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᣕ"),
  bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᣖ"): bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࠫᣗ"),
  bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᣘ"): bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫᣙ"),
  bstack11lllll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᣚ"): bstack11lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᣛ"),
  bstack11lllll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᣜ"): bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭ࠧᣝ"),
  bstack11lllll_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨᣞ"): bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡳࡰ࡮ࡨࠫᣟ"),
  bstack11lllll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪᣠ"): bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪᣡ"),
  bstack11lllll_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫᣢ"): bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫᣣ"),
  bstack11lllll_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨᣤ"): bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡹ࡭ࡩ࡫࡯ࠨᣥ"),
  bstack11lllll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪᣦ"): bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪᣧ"),
  bstack11lllll_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ᣨ"): bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ᣩ"),
  bstack11lllll_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᣪ"): bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᣫ"),
  bstack11lllll_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬᣬ"): bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸ࡮ࡳࡥࡻࡱࡱࡩࠬᣭ"),
  bstack11lllll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᣮ"): bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᣯ"),
  bstack11lllll_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭ᣰ"): bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭ᣱ"),
  bstack11lllll_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧᣲ"): bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧᣳ"),
  bstack11lllll_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫᣴ"): bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫᣵ"),
  bstack11lllll_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨ᣶"): bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦࡰࡧࡏࡪࡿࡳࠨ᣷"),
  bstack11lllll_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪ᣸"): bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴ࡝ࡡࡪࡶࠪ᣹"),
  bstack11lllll_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩ᣺"): bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡴࠩ᣻"),
  bstack11lllll_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭᣼"): bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡦࡤࡣࡦ࡬ࡪ࠭᣽"),
  bstack11lllll_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ᣾"): bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ᣿"),
  bstack11lllll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬᤀ"): bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬᤁ"),
  bstack11lllll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᤂ"): bstack11lllll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᤃ"),
  bstack11lllll_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪᤄ"): bstack11lllll_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬᤅ"),
  bstack11lllll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᤆ"): bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᤇ"),
  bstack11lllll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪᤈ"): bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪᤉ"),
  bstack11lllll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ᤊ"): bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ᤋ"),
  bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ᤌ"): bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࡴࠩᤍ"),
  bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᤎ"): bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᤏ"),
  bstack11lllll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᤐ"): bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸࡵࡵࡳࡥࡨࠫᤑ"),
  bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᤒ"): bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᤓ"),
  bstack11lllll_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪᤔ"): bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡪࡲࡷࡹࡔࡡ࡮ࡧࠪᤕ"),
  bstack11lllll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ᤖ"): bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ᤗ"),
  bstack11lllll_opy_ (u"ࠬࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤘ"): bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤙ"),
  bstack11lllll_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬᤚ"): bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬᤛ"),
  bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᤜ"): bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᤝ"),
  bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᤞ"): bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᤟")
}
bstack11l111ll11l_opy_ = [
  bstack11lllll_opy_ (u"࠭࡯ࡴࠩᤠ"),
  bstack11lllll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᤡ"),
  bstack11lllll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᤢ"),
  bstack11lllll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᤣ"),
  bstack11lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᤤ"),
  bstack11lllll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᤥ"),
  bstack11lllll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᤦ"),
]
bstack1ll1ll1ll1_opy_ = {
  bstack11lllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᤧ"): [bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨᤨ"), bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡔࡁࡎࡇࠪᤩ")],
  bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᤪ"): bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᤫ"),
  bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᤬"): bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨ᤭"),
  bstack11lllll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᤮"): bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠬ᤯"),
  bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᤰ"): bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᤱ"),
  bstack11lllll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᤲ"): bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡘࡥࡐࡆࡔࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬᤳ"),
  bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᤴ"): bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫᤵ"),
  bstack11lllll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫᤶ"): bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬᤷ"),
  bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠭ᤸ"): [bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕࡥࡉࡅ᤹ࠩ"), bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧ᤺")],
  bstack11lllll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲ᤻ࠧ"): bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡙ࡄࡌࡡࡏࡓࡌࡒࡅࡗࡇࡏࠫ᤼"),
  bstack11lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᤽"): bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ᤾"),
  bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᤿"): [bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡐࡄࡖࡉࡗ࡜ࡁࡃࡋࡏࡍ࡙࡟ࠧ᥀"), bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫ᥁")],
  bstack11lllll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᥂"): bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡕࡓࡄࡒࡗࡈࡇࡌࡆࠩ᥃"),
  bstack11lllll_opy_ (u"ࠧࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࡇࡑ࡚ࠬ᥄"): bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡐࡔࡆࡌࡊ࡙ࡔࡓࡃࡗࡍࡔࡔ࡟ࡔࡏࡄࡖ࡙ࡥࡓࡆࡎࡈࡇ࡙ࡏࡏࡏࡡࡉࡉࡆ࡚ࡕࡓࡇࡢࡆࡗࡇࡎࡄࡊࡈࡗࠬ᥅")
}
bstack11l11l1l1l_opy_ = {
  bstack11lllll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ᥆"): [bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬ᥇"), bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᥈")],
  bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᥉"): [bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ᥊"), bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ᥋")],
  bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ᥌"): bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ᥍"),
  bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ᥎"): bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ᥏"),
  bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᥐ"): bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᥑ"),
  bstack11lllll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᥒ"): [bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫᥓ"), bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᥔ")],
  bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᥕ"): bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᥖ"),
  bstack11lllll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᥗ"): bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᥘ"),
  bstack11lllll_opy_ (u"ࠧࡢࡲࡳࠫᥙ"): bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫᥚ"),
  bstack11lllll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᥛ"): bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᥜ"),
  bstack11lllll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᥝ"): bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᥞ"),
  bstack11lllll_opy_ (u"ࠨࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࡄࡎࡌࠦᥟ"): bstack11lllll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࠧᥠ"),
}
bstack11l11l1ll1_opy_ = {
  bstack11lllll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᥡ"): bstack11lllll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᥢ"),
  bstack11lllll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᥣ"): [bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᥤ"), bstack11lllll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᥥ")],
  bstack11lllll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᥦ"): bstack11lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᥧ"),
  bstack11lllll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᥨ"): bstack11lllll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᥩ"),
  bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᥪ"): [bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᥫ"), bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᥬ")],
  bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᥭ"): bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᥮"),
  bstack11lllll_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬ᥯"): bstack11lllll_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧᥰ"),
  bstack11lllll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᥱ"): [bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᥲ"), bstack11lllll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᥳ")],
  bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᥴ"): [bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨ᥵"), bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࠨ᥶")]
}
bstack1l1l11ll1l_opy_ = [
  bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨ᥷"),
  bstack11lllll_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭᥸"),
  bstack11lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ᥹"),
  bstack11lllll_opy_ (u"ࠬࡹࡥࡵ࡙࡬ࡲࡩࡵࡷࡓࡧࡦࡸࠬ᥺"),
  bstack11lllll_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࡳࠨ᥻"),
  bstack11lllll_opy_ (u"ࠧࡴࡶࡵ࡭ࡨࡺࡆࡪ࡮ࡨࡍࡳࡺࡥࡳࡣࡦࡸࡦࡨࡩ࡭࡫ࡷࡽࠬ᥼"),
  bstack11lllll_opy_ (u"ࠨࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡔࡷࡵ࡭ࡱࡶࡅࡩ࡭ࡧࡶࡪࡱࡵࠫ᥽"),
  bstack11lllll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᥾"),
  bstack11lllll_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ᥿"),
  bstack11lllll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬᦀ"),
  bstack11lllll_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫᦁ"),
  bstack11lllll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧᦂ"),
]
bstack1l111l1ll1_opy_ = [
  bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᦃ"),
  bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᦄ"),
  bstack11lllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᦅ"),
  bstack11lllll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᦆ"),
  bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᦇ"),
  bstack11lllll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᦈ"),
  bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᦉ"),
  bstack11lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᦊ"),
  bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᦋ"),
  bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧᦌ"),
  bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᦍ"),
  bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫᦎ"),
  bstack11lllll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧᦏ"),
  bstack11lllll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡚ࡡࡨࠩᦐ"),
  bstack11lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᦑ"),
  bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᦒ"),
  bstack11lllll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᦓ"),
  bstack11lllll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠲ࠩᦔ"),
  bstack11lllll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠴ࠪᦕ"),
  bstack11lllll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠶ࠫᦖ"),
  bstack11lllll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠸ࠬᦗ"),
  bstack11lllll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠺࠭ᦘ"),
  bstack11lllll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠼ࠧᦙ"),
  bstack11lllll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠷ࠨᦚ"),
  bstack11lllll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠹ࠩᦛ"),
  bstack11lllll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠻ࠪᦜ"),
  bstack11lllll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᦝ"),
  bstack11lllll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᦞ"),
  bstack11lllll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᦟ"),
  bstack11lllll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᦠ"),
  bstack11lllll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᦡ"),
  bstack11lllll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᦢ"),
  bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᦣ"),
  bstack11lllll_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨᦤ")
]
bstack11l11111l11_opy_ = [
  bstack11lllll_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫᦥ"),
  bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᦦ"),
  bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᦧ"),
  bstack11lllll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᦨ"),
  bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡑࡴ࡬ࡳࡷ࡯ࡴࡺࠩᦩ"),
  bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᦪ"),
  bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡦ࡭ࠧᦫ"),
  bstack11lllll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᦬"),
  bstack11lllll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᦭"),
  bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭᦮"),
  bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᦯"),
  bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᦰ"),
  bstack11lllll_opy_ (u"ࠫࡴࡹࠧᦱ"),
  bstack11lllll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᦲ"),
  bstack11lllll_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬᦳ"),
  bstack11lllll_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩᦴ"),
  bstack11lllll_opy_ (u"ࠨࡴࡨ࡫࡮ࡵ࡮ࠨᦵ"),
  bstack11lllll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫᦶ"),
  bstack11lllll_opy_ (u"ࠪࡱࡦࡩࡨࡪࡰࡨࠫᦷ"),
  bstack11lllll_opy_ (u"ࠫࡷ࡫ࡳࡰ࡮ࡸࡸ࡮ࡵ࡮ࠨᦸ"),
  bstack11lllll_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᦹ"),
  bstack11lllll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡕࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪᦺ"),
  bstack11lllll_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࠭ᦻ"),
  bstack11lllll_opy_ (u"ࠨࡰࡲࡔࡦ࡭ࡥࡍࡱࡤࡨ࡙࡯࡭ࡦࡱࡸࡸࠬᦼ"),
  bstack11lllll_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪᦽ"),
  bstack11lllll_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᦾ"),
  bstack11lllll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᦿ"),
  bstack11lllll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭ᧀ"),
  bstack11lllll_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪᧁ"),
  bstack11lllll_opy_ (u"ࠧ࡯ࡱࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠫᧂ"),
  bstack11lllll_opy_ (u"ࠨࡥ࡫ࡩࡨࡱࡕࡓࡎࠪᧃ"),
  bstack11lllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᧄ"),
  bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡆࡳࡴࡱࡩࡦࡵࠪᧅ"),
  bstack11lllll_opy_ (u"ࠫࡨࡧࡰࡵࡷࡵࡩࡈࡸࡡࡴࡪࠪᧆ"),
  bstack11lllll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᧇ"),
  bstack11lllll_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᧈ"),
  bstack11lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࡚ࡪࡸࡳࡪࡱࡱࠫᧉ"),
  bstack11lllll_opy_ (u"ࠨࡰࡲࡆࡱࡧ࡮࡬ࡒࡲࡰࡱ࡯࡮ࡨࠩ᧊"),
  bstack11lllll_opy_ (u"ࠩࡰࡥࡸࡱࡓࡦࡰࡧࡏࡪࡿࡳࠨ᧋"),
  bstack11lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡏࡳ࡬ࡹࠧ᧌"),
  bstack11lllll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡍࡩ࠭᧍"),
  bstack11lllll_opy_ (u"ࠬࡪࡥࡥ࡫ࡦࡥࡹ࡫ࡤࡅࡧࡹ࡭ࡨ࡫ࠧ᧎"),
  bstack11lllll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡖࡡࡳࡣࡰࡷࠬ᧏"),
  bstack11lllll_opy_ (u"ࠧࡱࡪࡲࡲࡪࡔࡵ࡮ࡤࡨࡶࠬ᧐"),
  bstack11lllll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭᧑"),
  bstack11lllll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡏࡱࡶ࡬ࡳࡳࡹࠧ᧒"),
  bstack11lllll_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨ᧓"),
  bstack11lllll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ᧔"),
  bstack11lllll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩ᧕"),
  bstack11lllll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡈࡩࡰ࡯ࡨࡸࡷ࡯ࡣࠨ᧖"),
  bstack11lllll_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࡜࠲ࠨ᧗"),
  bstack11lllll_opy_ (u"ࠨ࡯࡬ࡨࡘ࡫ࡳࡴ࡫ࡲࡲࡎࡴࡳࡵࡣ࡯ࡰࡆࡶࡰࡴࠩ᧘"),
  bstack11lllll_opy_ (u"ࠩࡨࡷࡵࡸࡥࡴࡵࡲࡗࡪࡸࡶࡦࡴࠪ᧙"),
  bstack11lllll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩ᧚"),
  bstack11lllll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡉࡤࡱࠩ᧛"),
  bstack11lllll_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬ᧜"),
  bstack11lllll_opy_ (u"࠭ࡳࡺࡰࡦࡘ࡮ࡳࡥࡘ࡫ࡷ࡬ࡓ࡚ࡐࠨ᧝"),
  bstack11lllll_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬ᧞"),
  bstack11lllll_opy_ (u"ࠨࡩࡳࡷࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭᧟"),
  bstack11lllll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ᧠"),
  bstack11lllll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪ᧡"),
  bstack11lllll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࡆ࡬ࡦࡴࡧࡦࡌࡤࡶࠬ᧢"),
  bstack11lllll_opy_ (u"ࠬࡾ࡭ࡴࡌࡤࡶࠬ᧣"),
  bstack11lllll_opy_ (u"࠭ࡸ࡮ࡺࡍࡥࡷ࠭᧤"),
  bstack11lllll_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭᧥"),
  bstack11lllll_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨ᧦"),
  bstack11lllll_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪ᧧"),
  bstack11lllll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭᧨"),
  bstack11lllll_opy_ (u"ࠫࡦࡶࡰࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᧩"),
  bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫ᧪"),
  bstack11lllll_opy_ (u"࠭ࡲࡦࡵ࡬࡫ࡳࡇࡰࡱࠩ᧫"),
  bstack11lllll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡰ࡬ࡱࡦࡺࡩࡰࡰࡶࠫ᧬"),
  bstack11lllll_opy_ (u"ࠨࡥࡤࡲࡦࡸࡹࠨ᧭"),
  bstack11lllll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ᧮"),
  bstack11lllll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ᧯"),
  bstack11lllll_opy_ (u"ࠫ࡮࡫ࠧ᧰"),
  bstack11lllll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪ᧱"),
  bstack11lllll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭᧲"),
  bstack11lllll_opy_ (u"ࠧࡲࡷࡨࡹࡪ࠭᧳"),
  bstack11lllll_opy_ (u"ࠨ࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ᧴"),
  bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࡙ࡴࡰࡴࡨࡇࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠪ᧵"),
  bstack11lllll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡆࡥࡲ࡫ࡲࡢࡋࡰࡥ࡬࡫ࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩ᧶"),
  bstack11lllll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡇࡻࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧ᧷"),
  bstack11lllll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡌࡲࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨ᧸"),
  bstack11lllll_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ᧹"),
  bstack11lllll_opy_ (u"ࠧࡳࡧࡶࡩࡷࡼࡥࡅࡧࡹ࡭ࡨ࡫ࠧ᧺"),
  bstack11lllll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ᧻"),
  bstack11lllll_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫ᧼"),
  bstack11lllll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡥࡸࡹࡣࡰࡦࡨࠫ᧽"),
  bstack11lllll_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡍࡴࡹࡄࡦࡸ࡬ࡧࡪ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧ᧾"),
  bstack11lllll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡻࡤࡪࡱࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬ᧿"),
  bstack11lllll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡰࡱ࡮ࡨࡔࡦࡿࠧᨀ"),
  bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᨁ"),
  bstack11lllll_opy_ (u"ࠨࡹࡧ࡭ࡴ࡙ࡥࡳࡸ࡬ࡧࡪ࠭ᨂ"),
  bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᨃ"),
  bstack11lllll_opy_ (u"ࠪࡴࡷ࡫ࡶࡦࡰࡷࡇࡷࡵࡳࡴࡕ࡬ࡸࡪ࡚ࡲࡢࡥ࡮࡭ࡳ࡭ࠧᨄ"),
  bstack11lllll_opy_ (u"ࠫ࡭࡯ࡧࡩࡅࡲࡲࡹࡸࡡࡴࡶࠪᨅ"),
  bstack11lllll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡕࡸࡥࡧࡧࡵࡩࡳࡩࡥࡴࠩᨆ"),
  bstack11lllll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩᨇ"),
  bstack11lllll_opy_ (u"ࠧࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫᨈ"),
  bstack11lllll_opy_ (u"ࠨࡴࡨࡱࡴࡼࡥࡊࡑࡖࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࡍࡱࡦࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᨉ"),
  bstack11lllll_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫᨊ"),
  bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᨋ"),
  bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭ᨌ"),
  bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᨍ"),
  bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᨎ"),
  bstack11lllll_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪᨏ"),
  bstack11lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧᨐ"),
  bstack11lllll_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫᨑ"),
  bstack11lllll_opy_ (u"ࠪࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡖࡲࡰ࡯ࡳࡸࡇ࡫ࡨࡢࡸ࡬ࡳࡷ࠭ᨒ")
]
bstack111l1l111_opy_ = {
  bstack11lllll_opy_ (u"ࠫࡻ࠭ᨓ"): bstack11lllll_opy_ (u"ࠬࡼࠧᨔ"),
  bstack11lllll_opy_ (u"࠭ࡦࠨᨕ"): bstack11lllll_opy_ (u"ࠧࡧࠩᨖ"),
  bstack11lllll_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧᨗ"): bstack11lllll_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨᨘ"),
  bstack11lllll_opy_ (u"ࠪࡳࡳࡲࡹࡢࡷࡷࡳࡲࡧࡴࡦࠩᨙ"): bstack11lllll_opy_ (u"ࠫࡴࡴ࡬ࡺࡃࡸࡸࡴࡳࡡࡵࡧࠪᨚ"),
  bstack11lllll_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩᨛ"): bstack11lllll_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪ᨜"),
  bstack11lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪ᨝"): bstack11lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫ᨞"),
  bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬ᨟"): bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᨠ"),
  bstack11lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧᨡ"): bstack11lllll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᨢ"),
  bstack11lllll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᨣ"): bstack11lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᨤ"),
  bstack11lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩᨥ"): bstack11lllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᨦ"),
  bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡰࡴࡷࠫᨧ"): bstack11lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬᨨ"),
  bstack11lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᨩ"): bstack11lllll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᨪ"),
  bstack11lllll_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᨫ"): bstack11lllll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᨬ"),
  bstack11lllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᨭ"): bstack11lllll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬᨮ"),
  bstack11lllll_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᨯ"): bstack11lllll_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᨰ"),
  bstack11lllll_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪࠪᨱ"): bstack11lllll_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫᨲ"),
  bstack11lllll_opy_ (u"ࠨࡲࡤࡧ࡫࡯࡬ࡦࠩᨳ"): bstack11lllll_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᨴ"),
  bstack11lllll_opy_ (u"ࠪࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᨵ"): bstack11lllll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᨶ"),
  bstack11lllll_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᨷ"): bstack11lllll_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᨸ"),
  bstack11lllll_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨᨹ"): bstack11lllll_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩᨺ"),
  bstack11lllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᨻ"): bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᨼ"),
  bstack11lllll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷ࠭ᨽ"): bstack11lllll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡰࡦࡣࡷࡩࡷ࠭ᨾ")
}
bstack11l11111l1l_opy_ = bstack11lllll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨ࡫ࡷ࡬ࡺࡨ࠮ࡤࡱࡰ࠳ࡵ࡫ࡲࡤࡻ࠲ࡧࡱ࡯࠯ࡳࡧ࡯ࡩࡦࡹࡥࡴ࠱࡯ࡥࡹ࡫ࡳࡵ࠱ࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᨿ")
bstack11l1111111l_opy_ = bstack11lllll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠯ࡩࡧࡤࡰࡹ࡮ࡣࡩࡧࡦ࡯ࠧᩀ")
bstack111l111ll_opy_ = bstack11lllll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡨࡨࡸ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡶࡩࡳࡪ࡟ࡴࡦ࡮ࡣࡪࡼࡥ࡯ࡶࡶࠦᩁ")
bstack1ll1111l_opy_ = bstack11lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡻࡩ࠵ࡨࡶࡤࠪᩂ")
bstack11l11ll11l_opy_ = bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧ࠭ᩃ")
bstack1lll1llll_opy_ = bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡴࡥࡹࡶࡢ࡬ࡺࡨࡳࠨᩄ")
bstack111l11l1_opy_ = {
  bstack11lllll_opy_ (u"ࠬࡪࡥࡧࡣࡸࡰࡹ࠭ᩅ"): bstack11lllll_opy_ (u"࠭ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᩆ"),
  bstack11lllll_opy_ (u"ࠧࡶࡵ࠰ࡩࡦࡹࡴࠨᩇ"): bstack11lllll_opy_ (u"ࠨࡪࡸࡦ࠲ࡻࡳࡦ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᩈ"),
  bstack11lllll_opy_ (u"ࠩࡸࡷࠬᩉ"): bstack11lllll_opy_ (u"ࠪ࡬ࡺࡨ࠭ࡶࡵ࠰ࡳࡳࡲࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᩊ"),
  bstack11lllll_opy_ (u"ࠫࡪࡻࠧᩋ"): bstack11lllll_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡨࡹ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᩌ"),
  bstack11lllll_opy_ (u"࠭ࡩ࡯ࠩᩍ"): bstack11lllll_opy_ (u"ࠧࡩࡷࡥ࠱ࡦࡶࡳ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᩎ"),
  bstack11lllll_opy_ (u"ࠨࡣࡸࠫᩏ"): bstack11lllll_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡡࡱࡵࡨ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᩐ")
}
bstack11l111l11l1_opy_ = {
  bstack11lllll_opy_ (u"ࠪࡧࡷ࡯ࡴࡪࡥࡤࡰࠬᩑ"): 50,
  bstack11lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᩒ"): 40,
  bstack11lllll_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ᩓ"): 30,
  bstack11lllll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᩔ"): 20,
  bstack11lllll_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᩕ"): 10
}
bstack111l1l11ll_opy_ = bstack11l111l11l1_opy_[bstack11lllll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᩖ")]
bstack1lll11l11l_opy_ = bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᩗ")
bstack1l1lllll_opy_ = bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᩘ")
bstack1lll11111l_opy_ = bstack11lllll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪᩙ")
bstack11llllll1_opy_ = bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᩚ")
bstack1l111ll1_opy_ = bstack11lllll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡢࡰࡧࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫᩛ")
bstack1llllll1l_opy_ = {
  bstack11lllll_opy_ (u"ࠧࡔࡆࡎ࠱ࡌࡋࡎ࠮࠲࠳࠹ࠬᩜ"): bstack11lllll_opy_ (u"ࠨࠬ࠭࠮ࠥࡡࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࡡࠥࡦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࡡࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡ࡫ࡱࠤࡾࡵࡵࡳࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠮ࠡࡖ࡫࡭ࡸࠦ࡭ࡢࡻࠣࡧࡦࡻࡳࡦࠢࡦࡳࡳ࡬࡬ࡪࡥࡷࡷࠥࡽࡩࡵࡪࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡭ࡹࠦࡵࡴ࡫ࡱ࡫࠿ࠦࡰࡪࡲࠣࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࠡࠬ࠭࠮ࠬᩝ")
}
bstack11l1111l1ll_opy_ = [bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪᩞ"), bstack11lllll_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ᩟")]
bstack11l111l1lll_opy_ = [bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟᩠ࠧ"), bstack11lllll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧᩡ")]
bstack111ll1l111_opy_ = re.compile(bstack11lllll_opy_ (u"࠭࡞࡜࡞࡟ࡻ࠲ࡣࠫ࠻࠰࠭ࠨࠬᩢ"))
bstack11111ll1l_opy_ = [
  bstack11lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨᩣ"),
  bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᩤ"),
  bstack11lllll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᩥ"),
  bstack11lllll_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧᩦ"),
  bstack11lllll_opy_ (u"ࠫࡦࡶࡰࠨᩧ"),
  bstack11lllll_opy_ (u"ࠬࡻࡤࡪࡦࠪᩨ"),
  bstack11lllll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᩩ"),
  bstack11lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧᩪ"),
  bstack11lllll_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ᩫ"),
  bstack11lllll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧᩬ"),
  bstack11lllll_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫᩭ"), bstack11lllll_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧᩮ"),
  bstack11lllll_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨᩯ"),
  bstack11lllll_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬᩰ"),
  bstack11lllll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫᩱ"),
  bstack11lllll_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫᩲ"),
  bstack11lllll_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪᩳ"),
  bstack11lllll_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨᩴ"), bstack11lllll_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨ᩵"), bstack11lllll_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧ᩶"), bstack11lllll_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧ᩷"), bstack11lllll_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ᩸"),
  bstack11lllll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᩹"),
  bstack11lllll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭᩺"),
  bstack11lllll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬ᩻"), bstack11lllll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨ᩼"),
  bstack11lllll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᩽"),
  bstack11lllll_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧ᩾"),
  bstack11lllll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ᩿࠭"),
  bstack11lllll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩ᪀"),
  bstack11lllll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧ᪁"),
  bstack11lllll_opy_ (u"ࠪࡥࡻࡪࠧ᪂"), bstack11lllll_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ᪃"), bstack11lllll_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧ᪄"), bstack11lllll_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧ᪅"),
  bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬ᪆"), bstack11lllll_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧ᪇"), bstack11lllll_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬ᪈"),
  bstack11lllll_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬ᪉"), bstack11lllll_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩ᪊"),
  bstack11lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧ᪋"), bstack11lllll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩ᪌"), bstack11lllll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬ᪍"), bstack11lllll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪ᪎"), bstack11lllll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭᪏"),
  bstack11lllll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭᪐"), bstack11lllll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨ᪑"),
  bstack11lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧ᪒"),
  bstack11lllll_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫ᪓"),
  bstack11lllll_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭᪔"), bstack11lllll_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩ᪕"), bstack11lllll_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧ᪖"), bstack11lllll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᪗"),
  bstack11lllll_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩ᪘"),
  bstack11lllll_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ᪙"), bstack11lllll_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭᪚"),
  bstack11lllll_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧ᪛"),
  bstack11lllll_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪ᪜"),
  bstack11lllll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫ᪝"),
  bstack11lllll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᪞"),
  bstack11lllll_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬ᪟"),
  bstack11lllll_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ᪠"),
  bstack11lllll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮ࠧ᪡"),
  bstack11lllll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭᪢"),
  bstack11lllll_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬ᪣"),
  bstack11lllll_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭᪤"),
  bstack11lllll_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫ᪥"),
  bstack11lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪ᪦"),
  bstack11lllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩᪧ"),
  bstack11lllll_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭᪨"),
  bstack11lllll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬ᪩"),
  bstack11lllll_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬ᪪"),
  bstack11lllll_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩ᪫"),
  bstack11lllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧ᪬"), bstack11lllll_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨ᪭"), bstack11lllll_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨ᪮"),
  bstack11lllll_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪ᪯"),
  bstack11lllll_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫ᪰"),
  bstack11lllll_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪ᪱"),
  bstack11lllll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫ᪲"),
  bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ᪳"),
  bstack11lllll_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨ᪴"),
  bstack11lllll_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨ᪵"), bstack11lllll_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸ᪶ࠬ"), bstack11lllll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ᪷ࠪ"),
  bstack11lllll_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨ᪸"),
  bstack11lllll_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶ᪹ࠪ"),
  bstack11lllll_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨ᪺ࠬ"),
  bstack11lllll_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫ᪻"),
  bstack11lllll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨ᪼"), bstack11lllll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨ᪽ࠬ"),
  bstack11lllll_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪ᪾"), bstack11lllll_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷᪿࠬ"),
  bstack11lllll_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣᫀࠩ"),
  bstack11lllll_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩ᫁"),
  bstack11lllll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧ᫂"), bstack11lllll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴ᫃ࠩ"), bstack11lllll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩ᫄ࠪ"), bstack11lllll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧ᫅"),
  bstack11lllll_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨ᫆"),
  bstack11lllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪ᫇"),
  bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᫈"),
  bstack11lllll_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫ᫉"),
  bstack11lllll_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨ᫊ࠩ"),
  bstack11lllll_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨ᫋"),
  bstack11lllll_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨᫌ"), bstack11lllll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩᫍ"),
  bstack11lllll_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬᫎ"),
  bstack11lllll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪ᫏"),
  bstack11lllll_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬ᫐"),
  bstack11lllll_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬ᫑"),
  bstack11lllll_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨ᫒"),
  bstack11lllll_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪ᫓"),
  bstack11lllll_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩ᫔"),
  bstack11lllll_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧࠪ᫕"),
  bstack11lllll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪ᫖"),
  bstack11lllll_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ᫗"),
  bstack11lllll_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪ᫘"),
  bstack11lllll_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬ᫙"),
  bstack11lllll_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭᫚"),
  bstack11lllll_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪ᫛"),
  bstack11lllll_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫ᫜"),
  bstack11lllll_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ࠭᫝"),
  bstack11lllll_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬ᫞"),
  bstack11lllll_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭᫟"),
  bstack11lllll_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮ࠪ᫠"),
  bstack11lllll_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭᫡"),
  bstack11lllll_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫ᫢"),
  bstack11lllll_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ᫣"), bstack11lllll_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᫤"),
  bstack11lllll_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨ᫥"), bstack11lllll_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭᫦"),
  bstack11lllll_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫ᫧"),
  bstack11lllll_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪ᫨"),
  bstack11lllll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪ᫩"),
  bstack11lllll_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭᫪"), bstack11lllll_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭᫫"),
  bstack11lllll_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ᫬"),
  bstack11lllll_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪ᫭"),
  bstack11lllll_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭᫮"),
  bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨ᫯"),
  bstack11lllll_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪ᫰"),
  bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬ᫱"),
  bstack11lllll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨ᫲"),
  bstack11lllll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪ᫳"),
  bstack11lllll_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧ᫴"),
  bstack11lllll_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬ᫵"), bstack11lllll_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫ᫶"),
  bstack11lllll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨ᫷"),
  bstack11lllll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡌࡨࡑࡵࡣࡢࡶࡲࡶࡆࡻࡴࡰࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠬ᫸")
]
bstack1ll1l11111_opy_ = bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡸࡴࡱࡵࡡࡥࠩ᫹")
bstack1l1lll1l_opy_ = [bstack11lllll_opy_ (u"ࠫ࠳ࡧࡰ࡬ࠩ᫺"), bstack11lllll_opy_ (u"ࠬ࠴ࡡࡢࡤࠪ᫻"), bstack11lllll_opy_ (u"࠭࠮ࡪࡲࡤࠫ᫼")]
bstack11llll1l11_opy_ = [bstack11lllll_opy_ (u"ࠧࡪࡦࠪ᫽"), bstack11lllll_opy_ (u"ࠨࡲࡤࡸ࡭࠭᫾"), bstack11lllll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ᫿"), bstack11lllll_opy_ (u"ࠪࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥࠩᬀ")]
bstack1l11l1l11l_opy_ = {
  bstack11lllll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᬁ"): bstack11lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᬂ"),
  bstack11lllll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧᬃ"): bstack11lllll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬᬄ"),
  bstack11lllll_opy_ (u"ࠨࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᬅ"): bstack11lllll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᬆ"),
  bstack11lllll_opy_ (u"ࠪ࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᬇ"): bstack11lllll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᬈ"),
  bstack11lllll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡴࡪࡱࡱࡷࠬᬉ"): bstack11lllll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧᬊ")
}
bstack1ll11l11ll_opy_ = [
  bstack11lllll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᬋ"),
  bstack11lllll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᬌ"),
  bstack11lllll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᬍ"),
  bstack11lllll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᬎ"),
  bstack11lllll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬᬏ"),
]
bstack11l11lllll_opy_ = bstack1l111l1ll1_opy_ + bstack11l11111l11_opy_ + bstack11111ll1l_opy_
bstack1l1111l11_opy_ = [
  bstack11lllll_opy_ (u"ࠬࡤ࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵࠦࠪᬐ"),
  bstack11lllll_opy_ (u"࠭࡞ࡣࡵ࠰ࡰࡴࡩࡡ࡭࠰ࡦࡳࡲࠪࠧᬑ"),
  bstack11lllll_opy_ (u"ࠧ࡟࠳࠵࠻࠳࠭ᬒ"),
  bstack11lllll_opy_ (u"ࠨࡠ࠴࠴࠳࠭ᬓ"),
  bstack11lllll_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠲࡝࠹࠱࠾ࡣ࠮ࠨᬔ"),
  bstack11lllll_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠴࡞࠴࠲࠿࡝࠯ࠩᬕ"),
  bstack11lllll_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠶࡟࠵࠳࠱࡞࠰ࠪᬖ"),
  bstack11lllll_opy_ (u"ࠬࡤ࠱࠺࠴࠱࠵࠻࠾࠮ࠨᬗ")
]
bstack11l11ll1lll_opy_ = bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᬘ")
bstack1lll1111l_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡦࡸࡨࡲࡹ࠭ᬙ")
bstack11ll111lll_opy_ = [ bstack11lllll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᬚ") ]
bstack1lllll1lll_opy_ = [ bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨᬛ") ]
bstack111l11l1l_opy_ = [bstack11lllll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᬜ")]
bstack11l11l1l11_opy_ = [ bstack11lllll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᬝ") ]
bstack1llll1l11l_opy_ = bstack11lllll_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧᬞ")
bstack111lll1ll_opy_ = bstack11lllll_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩᬟ")
bstack111lllll_opy_ = bstack11lllll_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫᬠ")
bstack1ll11l1lll_opy_ = bstack11lllll_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧᬡ")
bstack1l11l1111l_opy_ = [
  bstack11lllll_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭ᬢ"),
  bstack11lllll_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪᬣ"),
  bstack11lllll_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬᬤ"),
  bstack11lllll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫᬥ"),
  bstack11lllll_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪᬦ"),
  bstack11lllll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨᬧ"),
  bstack11lllll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨᬨ"),
  bstack11lllll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫᬩ"),
  bstack11lllll_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬᬪ"),
  bstack11lllll_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬᬫ"),
  bstack11lllll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ᬬ"),
  bstack11lllll_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬᬭ"),
  bstack11lllll_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪᬮ"),
  bstack11lllll_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᬯ"),
  bstack11lllll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ᬰ"),
  bstack11lllll_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᬱ"),
  bstack11lllll_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧᬲ"),
  bstack11lllll_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬᬳ"),
  bstack11lllll_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ᬴ࠧ"),
  bstack11lllll_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᬵ"),
  bstack11lllll_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᬶ"),
]
bstack1lll1l1l_opy_ = bstack11lllll_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧᬷ")
bstack1ll1111111_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠪࢂࠬᬸ")), bstack11lllll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᬹ"), bstack11lllll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᬺ"))
bstack11l1l1ll1l1_opy_ = bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵ࡯ࠧᬻ")
bstack11l111lll11_opy_ = [ bstack11lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᬼ"), bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᬽ"), bstack11lllll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨᬾ"), bstack11lllll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᬿ")]
bstack11lll11l1_opy_ = [ bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᭀ"), bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᭁ"), bstack11lllll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬᭂ"), bstack11lllll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᭃ") ]
bstack1ll1l1l1l1_opy_ = [ bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺ᭄ࠧ") ]
bstack111lllll1l1_opy_ = [ bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᭅ") ]
bstack1l11111l1l_opy_ = 360
bstack11l11ll11ll_opy_ = bstack11lllll_opy_ (u"ࠥࡥࡵࡶ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥᭆ")
bstack11l1111lll1_opy_ = bstack11lllll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡩࡴࡵࡸࡩࡸࠨᭇ")
bstack11l111llll1_opy_ = bstack11lllll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠣᭈ")
bstack11l1l1lll1l_opy_ = bstack11lllll_opy_ (u"ࠨࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡵࡧࡶࡸࡸࠦࡡࡳࡧࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦ࡯࡯ࠢࡒࡗࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࠥࡴࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩࠥ࡬࡯ࡳࠢࡄࡲࡩࡸ࡯ࡪࡦࠣࡨࡪࡼࡩࡤࡧࡶ࠲ࠧᭉ")
bstack11l1l11111l_opy_ = bstack11lllll_opy_ (u"ࠢ࠲࠳࠱࠴ࠧᭊ")
bstack11111l1l1l_opy_ = {
  bstack11lllll_opy_ (u"ࠨࡒࡄࡗࡘ࠭ᭋ"): bstack11lllll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᭌ"),
  bstack11lllll_opy_ (u"ࠪࡊࡆࡏࡌࠨ᭍"): bstack11lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᭎"),
  bstack11lllll_opy_ (u"࡙ࠬࡋࡊࡒࠪ᭏"): bstack11lllll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᭐")
}
bstack11ll1ll1l_opy_ = [
  bstack11lllll_opy_ (u"ࠢࡨࡧࡷࠦ᭑"),
  bstack11lllll_opy_ (u"ࠣࡩࡲࡆࡦࡩ࡫ࠣ᭒"),
  bstack11lllll_opy_ (u"ࠤࡪࡳࡋࡵࡲࡸࡣࡵࡨࠧ᭓"),
  bstack11lllll_opy_ (u"ࠥࡶࡪ࡬ࡲࡦࡵ࡫ࠦ᭔"),
  bstack11lllll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ᭕"),
  bstack11lllll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ᭖"),
  bstack11lllll_opy_ (u"ࠨࡳࡶࡤࡰ࡭ࡹࡋ࡬ࡦ࡯ࡨࡲࡹࠨ᭗"),
  bstack11lllll_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦ᭘"),
  bstack11lllll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦ᭙"),
  bstack11lllll_opy_ (u"ࠤࡦࡰࡪࡧࡲࡆ࡮ࡨࡱࡪࡴࡴࠣ᭚"),
  bstack11lllll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࡶࠦ᭛"),
  bstack11lllll_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠦ᭜"),
  bstack11lllll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࡇࡳࡺࡰࡦࡗࡨࡸࡩࡱࡶࠥ᭝"),
  bstack11lllll_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧ᭞"),
  bstack11lllll_opy_ (u"ࠢࡲࡷ࡬ࡸࠧ᭟"),
  bstack11lllll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡖࡲࡹࡨ࡮ࡁࡤࡶ࡬ࡳࡳࠨ᭠"),
  bstack11lllll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡐࡹࡱࡺࡩࡕࡱࡸࡧ࡭ࠨ᭡"),
  bstack11lllll_opy_ (u"ࠥࡷ࡭ࡧ࡫ࡦࠤ᭢"),
  bstack11lllll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡄࡴࡵࠨ᭣")
]
bstack11l111l1ll1_opy_ = [
  bstack11lllll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦ᭤"),
  bstack11lllll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ᭥"),
  bstack11lllll_opy_ (u"ࠢࡢࡷࡷࡳࠧ᭦"),
  bstack11lllll_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣ᭧"),
  bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ᭨")
]
bstack111lll1ll1_opy_ = {
  bstack11lllll_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤ᭩"): [bstack11lllll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ᭪")],
  bstack11lllll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ᭫"): [bstack11lllll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶ᭬ࠥ")],
  bstack11lllll_opy_ (u"ࠢࡢࡷࡷࡳࠧ᭭"): [bstack11lllll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ᭮"), bstack11lllll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧ᭯"), bstack11lllll_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢ᭰"), bstack11lllll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ᭱")],
  bstack11lllll_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧ᭲"): [bstack11lllll_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨ᭳")],
  bstack11lllll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ᭴"): [bstack11lllll_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ᭵")],
}
bstack11l11111ll1_opy_ = {
  bstack11lllll_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣ᭶"): bstack11lllll_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤ᭷"),
  bstack11lllll_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣ᭸"): bstack11lllll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ᭹"),
  bstack11lllll_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥ᭺"): bstack11lllll_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࠤ᭻"),
  bstack11lllll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦ᭼"): bstack11lllll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦ᭽"),
  bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ᭾"): bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᭿")
}
bstack111111l11l_opy_ = {
  bstack11lllll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᮀ"): bstack11lllll_opy_ (u"࠭ࡓࡶ࡫ࡷࡩ࡙ࠥࡥࡵࡷࡳࠫᮁ"),
  bstack11lllll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᮂ"): bstack11lllll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩᮃ"),
  bstack11lllll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᮄ"): bstack11lllll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡕࡨࡸࡺࡶࠧᮅ"),
  bstack11lllll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᮆ"): bstack11lllll_opy_ (u"࡚ࠬࡥࡴࡶࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬᮇ")
}
bstack11l11l11111_opy_ = 65536
bstack11l1111l11l_opy_ = bstack11lllll_opy_ (u"࠭࠮࠯࠰࡞ࡘࡗ࡛ࡎࡄࡃࡗࡉࡉࡣࠧᮈ")
bstack111llllll11_opy_ = [
      bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᮉ"), bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᮊ"), bstack11lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᮋ"), bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᮌ"), bstack11lllll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ᮍ"),
      bstack11lllll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᮎ"), bstack11lllll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩᮏ"), bstack11lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᮐ"), bstack11lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᮑ"),
      bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᮒ"), bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᮓ"), bstack11lllll_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᮔ")
    ]
bstack11l111lllll_opy_= {
  bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᮕ"): bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᮖ"),
  bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᮗ"): bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᮘ"),
  bstack11lllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᮙ"): bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᮚ"),
  bstack11lllll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᮛ"): bstack11lllll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᮜ"),
  bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᮝ"): bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᮞ"),
  bstack11lllll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᮟ"): bstack11lllll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᮠ"),
  bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᮡ"): bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᮢ"),
  bstack11lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᮣ"): bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᮤ"),
  bstack11lllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᮥ"): bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᮦ"),
  bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧᮧ"): bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨᮨ"),
  bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᮩ"): bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ᮪ࠩ"),
  bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬᮫࠭"): bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧᮬ"),
  bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᮭ"): bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᮮ"),
  bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࡒࡴࡹ࡯࡯࡯ࡵࠪᮯ"): bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫ᮰"),
  bstack11lllll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧ᮱"): bstack11lllll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ᮲"),
  bstack11lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᮳"): bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᮴"),
  bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᮵"): bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᮶"),
  bstack11lllll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ᮷"): bstack11lllll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩ᮸"),
  bstack11lllll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ᮹"): bstack11lllll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᮺ"),
  bstack11lllll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᮻ"): bstack11lllll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᮼ"),
  bstack11lllll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ᮽ"): bstack11lllll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᮾ"),
  bstack11lllll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᮿ"): bstack11lllll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᯀ"),
  bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᯁ"): bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᯂ"),
  bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᯃ"): bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᯄ"),
  bstack11lllll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᯅ"): bstack11lllll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᯆ"),
  bstack11lllll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᯇ"): bstack11lllll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫᯈ"),
  bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᯉ"): bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ᯊ"),
  bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪᯋ"): bstack11lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᯌ")
}
bstack11l111ll111_opy_ = [bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᯍ"), bstack11lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᯎ")]
bstack1ll1l11l11_opy_ = (bstack11lllll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᯏ"),)
bstack11l1111ll11_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡷࡳࡨࡦࡺࡥࡠࡥ࡯࡭ࠬᯐ")
bstack1l111l111_opy_ = bstack11lllll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠲ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠱ࡹ࠵࠴࡭ࡲࡪࡦࡶ࠳ࠧᯑ")
bstack11lllll1l1_opy_ = bstack11lllll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬ࡸࡩࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࠤᯒ")
bstack111lll111l_opy_ = bstack11lllll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠭ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠧᯓ")
class EVENTS(Enum):
  bstack11l111l1l11_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩᯔ")
  bstack1l11l1l1ll_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳࠫᯕ")
  bstack1l1l11l1ll_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡢ࡮࡬ࡾࡪ࠭ᯖ")
  bstack11l11l111l1_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࡯ࡳ࡬ࡹࠧᯗ")
  bstack11l1l11ll1_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬᯘ") #shift post bstack11l1111l1l1_opy_
  bstack11l1l11l1l_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮ࠫᯙ") #shift post bstack11l1111l1l1_opy_
  bstack11l11111111_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡮ࡵࡣࠩᯚ") #shift
  bstack11l1111llll_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪᯛ") #shift
  bstack1l1l11ll11_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨᯜ")
  bstack1l1l1l1l11l_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡶࡥࡻ࡫࠭ࡳࡧࡶࡹࡱࡺࡳࠨᯝ")
  bstack1ll1l111l1_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡴࡪࡸࡦࡰࡴࡰࡷࡨࡧ࡮ࠨᯞ")
  bstack1l1ll111l1_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡮ࡲࡧࡦࡲࠧᯟ") #shift
  bstack11llll111l_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡡࡱࡲ࠰ࡹࡵࡲ࡯ࡢࡦࠪᯠ") #shift
  bstack1l1ll1lll1_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡧ࡮࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠩᯡ")
  bstack1l1l11lll_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭ᯢ") #shift
  bstack1ll111ll11_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭ᯣ") #shift
  bstack111llllll1l_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻࠪᯤ") #shift
  bstack1l11l1l111l_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᯥ")
  bstack1l11ll1lll_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡶࡸࡦࡺࡵࡴ᯦ࠩ") #shift
  bstack111lllll1_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪᯧ")
  bstack11l1111ll1l_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡽࡿ࠭ࡴࡧࡷࡹࡵ࠭ᯨ") #shift
  bstack11111111_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡹࡻࡰࠨᯩ")
  bstack11l111ll1l1_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡲࡦࡶࡳࡩࡱࡷࠫᯪ") # not bstack11l11111lll_opy_ in python
  bstack11l1l1l11l_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡶࡻࡩࡵࠩᯫ") # used in bstack11l1111l111_opy_
  bstack11ll111ll11_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶࡲࡦ࠯ࡴࡹ࡮ࡺࠧᯬ")
  bstack11ll111l1l1_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱ࡶࡻࡩࡵࠩᯭ")
  bstack111l11llll_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡨࡧࡷࠫᯮ") # used in bstack11l1111l111_opy_
  bstack1ll1l1l11l_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡪࡲࡳࡰ࠭ᯯ")
  bstack11ll11l1ll1_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡨࡰࡱ࡮ࠫᯰ")
  bstack11ll11l1l11_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡪࡲࡳࡰ࠭ᯱ")
  bstack11ll11l11_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩ᯲ࠬ")
  bstack1111l111l_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲ᯳ࠬ") #
  bstack11l1ll11ll_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡹࡧ࡫ࡦࡕࡦࡶࡪ࡫࡮ࡔࡪࡲࡸࠬ᯴")
  bstack111l1l11l_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬ᯵")
  bstack1ll1l11ll_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡩ࠲ࡺࡥࡴࡶࠪ᯶")
  bstack1l11l11l_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡳࡸࡺ࠭ࡵࡧࡶࡸࠬ᯷")
  bstack1ll11ll1_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡷ࡫࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨ᯸") #shift
  bstack111lll1111_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪ᯹") #shift
  bstack111llllllll_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫ᯺")
  bstack11l111l1l1l_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡫ࡧࡰࡪ࠳ࡴࡪ࡯ࡨࡳࡺࡺࠧ᯻")
  bstack1ll111lll1_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡦࡺ࡬ࡸ࠲࡮ࡡ࡯ࡦ࡯ࡩࡷ࠭᯼")
  bstack1ll11lllll1_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿࡫ࡸࡪࡶ࠰࡬ࡦࡴࡤ࡭ࡧࡵࠫ᯽")
  bstack11l11l1111l_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࠭࡮ࡧࡷࡶ࡮ࡩࡳࠨ᯾")
  bstack11l111l11ll_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡩࡷࡥ࠾ࡸࡺ࡯ࡱࠩ᯿")
  bstack1ll1111l11l_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡵࡷࡥࡷࡺࠧᰀ")
  bstack11l111lll1l_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡧࡳࡼࡴ࡬ࡰࡣࡧࠫᰁ")
  bstack111lllll1ll_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡧ࡭࡫ࡣ࡬࠯ࡸࡴࡩࡧࡴࡦࠩᰂ")
  bstack1ll11l1l1ll_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡣࡱࡲࡸࡸࡺࡲࡢࡲࠪᰃ")
  bstack1ll111l1l1l_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡵࡷࡥࡷࡺࡢࡪࡰࡤࡶࡾ࠭ᰄ")
  bstack1ll111llll1_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡦࡳࡳࡴࡥࡤࡶࠪᰅ")
  bstack1ll1ll11111_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡷࡹࡵࡰࠨᰆ")
  bstack1ll11111111_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭ᰇ")
  bstack1ll1ll1ll1l_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩᰈ")
  bstack11l111l111l_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠪᰉ")
  bstack11l111l1111_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡨࡓ࡫ࡡࡳࡧࡶࡸࡍࡻࡢࠨᰊ")
  bstack1l111l1111l_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡉ࡯࡫ࡷࠫᰋ")
  bstack1l11111llll_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡶࡹ࠭ᰌ")
  bstack1l1lll11lll_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡆࡳࡳ࡬ࡩࡨࠩᰍ")
  bstack11l111111l1_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪᰎ")
  bstack1l1l1l111l1_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡩࡔࡧ࡯ࡪࡍ࡫ࡡ࡭ࡕࡷࡩࡵ࠭ᰏ")
  bstack1l1l1l1111l_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡊࡩࡹࡘࡥࡴࡷ࡯ࡸࠬᰐ")
  bstack1l1l111l111_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡅࡷࡧࡱࡸࠬᰑ")
  bstack1l11lll111l_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠫᰒ")
  bstack1l11ll1l1ll_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡬ࡰࡩࡆࡶࡪࡧࡴࡦࡦࡈࡺࡪࡴࡴࠨᰓ")
  bstack111lllllll1_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡦࡰࡴࡹࡪࡻࡥࡕࡧࡶࡸࡊࡼࡥ࡯ࡶࠪᰔ")
  bstack1l1111ll1ll_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡴࡶࠧᰕ")
  bstack1ll11l11ll1_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࡮ࡔࡶࡲࡴࠬᰖ")
  bstack11l1lll1ll1_opy_ = bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࡕࡱ࡮ࡲࡥࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪᰗ")
  bstack1llll1ll1_opy_ = bstack11lllll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡱࡨࡋࡻ࡮࡯ࡧ࡯ࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪᰘ")
  bstack1ll1l1lll_opy_ = bstack11lllll_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡌࡵ࡯ࡰࡨࡰ࡙࡫ࡳࡵࡅࡲࡱࡵࡲࡥࡵࡧࡧࠫᰙ")
  bstack1llll1l1l11_opy_ = bstack11lllll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡴࡵࡲࡹࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡐࡺࡶࡨࡷࡹ࠭ᰚ")
  bstack1llll1ll1ll_opy_ = bstack11lllll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡳࡑࡻࡷࡩࡸࡺࠧᰛ")
  bstack1lllll11lll_opy_ = bstack11lllll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡿࡴࡦࡵࡷࡋࡪࡺࡔࡰࡶࡤࡰ࡙࡫ࡳࡵࡵࠪᰜ")
class STAGE(Enum):
  bstack111111l1l_opy_ = bstack11lllll_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧᰝ")
  END = bstack11lllll_opy_ (u"ࠩࡨࡲࡩ࠭ᰞ")
  bstack1llll11111_opy_ = bstack11lllll_opy_ (u"ࠪࡷ࡮ࡴࡧ࡭ࡧࠪᰟ")
bstack1l1l1l1l_opy_ = {
  bstack11lllll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࠫᰠ"): bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᰡ"),
  bstack11lllll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪᰢ"): bstack11lllll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᰣ")
}
PLAYWRIGHT_HUB_URL = bstack11lllll_opy_ (u"ࠣࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠥᰤ")
bstack1l1l1ll1111_opy_ = 98
bstack1l1ll11l11l_opy_ = 100
bstack1llll11ll1l_opy_ = {
  bstack11lllll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࠨᰥ"): bstack11lllll_opy_ (u"ࠪ࠱࠲ࡸࡥࡳࡷࡱࡷࠬᰦ"),
  bstack11lllll_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪᰧ"): bstack11lllll_opy_ (u"ࠬ࠳࠭ࡳࡧࡵࡹࡳࡹ࠭ࡥࡧ࡯ࡥࡾ࠭ᰨ"),
  bstack11lllll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫᰩ"): 0
}
bstack11l111ll1ll_opy_ = bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᰪ")
bstack11l111111ll_opy_ = bstack11lllll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡸࡴࡱࡵࡡࡥ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧᰫ")
bstack11ll11lll1_opy_ = bstack11lllll_opy_ (u"ࠤࡗࡉࡘ࡚ࠠࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠣࡅࡓࡊࠠࡂࡐࡄࡐ࡞࡚ࡉࡄࡕࠥᰬ")