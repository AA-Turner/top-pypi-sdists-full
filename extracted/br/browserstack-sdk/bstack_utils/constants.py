# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
import re
from enum import Enum
bstack11l111l1_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫឍ"): bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࠧណ"),
  bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧត"): bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡰ࡫ࡹࠨថ"),
  bstack1l1l1ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩទ"): bstack1l1l1ll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫធ"),
  bstack1l1l1ll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨន"): bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩប"),
  bstack1l1l1ll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨផ"): bstack1l1l1ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࠬព"),
  bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨភ"): bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬម"),
  bstack1l1l1ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬយ"): bstack1l1l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭រ"),
  bstack1l1l1ll_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨល"): bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧࠨវ"),
  bstack1l1l1ll_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩឝ"): bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡴࡱ࡯ࡩࠬឞ"),
  bstack1l1l1ll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫស"): bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫហ"),
  bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬឡ"): bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬអ"),
  bstack1l1l1ll_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩឣ"): bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡺ࡮ࡪࡥࡰࠩឤ"),
  bstack1l1l1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫឥ"): bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫឦ"),
  bstack1l1l1ll_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧឧ"): bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧឨ"),
  bstack1l1l1ll_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧឩ"): bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧឪ"),
  bstack1l1l1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ឫ"): bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ឬ"),
  bstack1l1l1ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨឭ"): bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩឮ"),
  bstack1l1l1ll_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧឯ"): bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧឰ"),
  bstack1l1l1ll_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨឱ"): bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨឲ"),
  bstack1l1l1ll_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬឳ"): bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬ឴"),
  bstack1l1l1ll_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ឵"): bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧࡱࡨࡐ࡫ࡹࡴࠩា"),
  bstack1l1l1ll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫិ"): bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵࡗࡢ࡫ࡷࠫី"),
  bstack1l1l1ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪឹ"): bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡵࠪឺ"),
  bstack1l1l1ll_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧុ"): bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡧࡥࡤࡧ࡭࡫ࠧូ"),
  bstack1l1l1ll_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩួ"): bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩើ"),
  bstack1l1l1ll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ឿ"): bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ៀ"),
  bstack1l1l1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩេ"): bstack1l1l1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ែ"),
  bstack1l1l1ll_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫៃ"): bstack1l1l1ll_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭ោ"),
  bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩៅ"): bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪំ"),
  bstack1l1l1ll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫះ"): bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫៈ"),
  bstack1l1l1ll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧ៉"): bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧ៊"),
  bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧ់"): bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪ៌"),
  bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ៍"): bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ៎"),
  bstack1l1l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ៏"): bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹ࡯ࡶࡴࡦࡩࠬ័"),
  bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ៑"): bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ្ࠩ"),
  bstack1l1l1ll_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫ៓"): bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫ។"),
  bstack1l1l1ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧ៕"): bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧ៖"),
  bstack1l1l1ll_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪៗ"): bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪ៘"),
  bstack1l1l1ll_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭៙"): bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭៚"),
  bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭៛"): bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ៜ"),
  bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ៝"): bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ៞")
}
bstack11ll11111ll_opy_ = [
  bstack1l1l1ll_opy_ (u"ࠧࡰࡵࠪ៟"),
  bstack1l1l1ll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ០"),
  bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ១"),
  bstack1l1l1ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ២"),
  bstack1l1l1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ៣"),
  bstack1l1l1ll_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ៤"),
  bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭៥"),
]
bstack111lllll_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ៦"): [bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ៧"), bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫ៨")],
  bstack1l1l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭៩"): bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ៪"),
  bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ៫"): bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩ៬"),
  bstack1l1l1ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ៭"): bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭៮"),
  bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ៯"): bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ៰"),
  bstack1l1l1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ៱"): bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭៲"),
  bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ៳"): bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ៴"),
  bstack1l1l1ll_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ៵"): bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭៶"),
  bstack1l1l1ll_opy_ (u"ࠪࡥࡵࡶࠧ៷"): [bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖ࡟ࡊࡆࠪ៸"), bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࠨ៹")],
  bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ៺"): bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡐࡔࡍࡌࡆࡘࡈࡐࠬ៻"),
  bstack1l1l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ៼"): bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ៽"),
  bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ៾"): [bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡑࡅࡗࡊࡘࡖࡂࡄࡌࡐࡎ࡚࡙ࠨ៿"), bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬ᠀")],
  bstack1l1l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᠁"): bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡖࡔࡅࡓࡘࡉࡁࡍࡇࠪ᠂")
}
bstack111ll1l11_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᠃"): [bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫ᠄"), bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ᠅")],
  bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᠆"): [bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡣࡰ࡫ࡹࠨ᠇"), bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᠈")],
  bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ᠉"): bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ᠊"),
  bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ᠋"): bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ᠌"),
  bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭᠍"): bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭᠎"),
  bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭᠏"): [bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡱࡲࠪ᠐"), bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᠑")],
  bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᠒"): bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ᠓"),
  bstack1l1l1ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ᠔"): bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ᠕"),
  bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲࠪ᠖"): bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲࠪ᠗"),
  bstack1l1l1ll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ᠘"): bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ᠙"),
  bstack1l1l1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᠚"): bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᠛")
}
bstack1l1111ll1l_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᠜"): bstack1l1l1ll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ᠝"),
  bstack1l1l1ll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᠞"): [bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᠟"), bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᠠ")],
  bstack1l1l1ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᠡ"): bstack1l1l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᠢ"),
  bstack1l1l1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᠣ"): bstack1l1l1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᠤ"),
  bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᠥ"): [bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᠦ"), bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᠧ")],
  bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᠨ"): bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᠩ"),
  bstack1l1l1ll_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩᠪ"): bstack1l1l1ll_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫᠫ"),
  bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᠬ"): [bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᠭ"), bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᠮ")],
  bstack1l1l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩᠯ"): [bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬᠰ"), bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬᠱ")]
}
bstack11l1lll111_opy_ = [
  bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᠲ"),
  bstack1l1l1ll_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪᠳ"),
  bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧᠴ"),
  bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩᠵ"),
  bstack1l1l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬᠶ"),
  bstack1l1l1ll_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩᠷ"),
  bstack1l1l1ll_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨᠸ"),
  bstack1l1l1ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᠹ"),
  bstack1l1l1ll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬᠺ"),
  bstack1l1l1ll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᠻ"),
  bstack1l1l1ll_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᠼ"),
  bstack1l1l1ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫᠽ"),
]
bstack1l1l11ll1_opy_ = [
  bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᠾ"),
  bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᠿ"),
  bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᡀ"),
  bstack1l1l1ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᡁ"),
  bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᡂ"),
  bstack1l1l1ll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᡃ"),
  bstack1l1l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᡄ"),
  bstack1l1l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᡅ"),
  bstack1l1l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᡆ"),
  bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᡇ"),
  bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᡈ"),
  bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨᡉ"),
  bstack1l1l1ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᡊ"),
  bstack1l1l1ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡗࡥ࡬࠭ᡋ"),
  bstack1l1l1ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᡌ"),
  bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᡍ"),
  bstack1l1l1ll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪᡎ"),
  bstack1l1l1ll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠶࠭ᡏ"),
  bstack1l1l1ll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠸ࠧᡐ"),
  bstack1l1l1ll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠳ࠨᡑ"),
  bstack1l1l1ll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠵ࠩᡒ"),
  bstack1l1l1ll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠷ࠪᡓ"),
  bstack1l1l1ll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠹ࠫᡔ"),
  bstack1l1l1ll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠻ࠬᡕ"),
  bstack1l1l1ll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠽࠭ᡖ"),
  bstack1l1l1ll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠿ࠧᡗ"),
  bstack1l1l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᡘ"),
  bstack1l1l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᡙ"),
  bstack1l1l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᡚ"),
  bstack1l1l1ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᡛ"),
  bstack1l1l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᡜ"),
  bstack1l1l1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫᡝ"),
  bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᡞ")
]
bstack11l1lll111l_opy_ = [
  bstack1l1l1ll_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧᡟ"),
  bstack1l1l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᡠ"),
  bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᡡ"),
  bstack1l1l1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᡢ"),
  bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡔࡷ࡯࡯ࡳ࡫ࡷࡽࠬᡣ"),
  bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᡤ"),
  bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡢࡩࠪᡥ"),
  bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᡦ"),
  bstack1l1l1ll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᡧ"),
  bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᡨ"),
  bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᡩ"),
  bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᡪ"),
  bstack1l1l1ll_opy_ (u"ࠧࡰࡵࠪᡫ"),
  bstack1l1l1ll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᡬ"),
  bstack1l1l1ll_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨᡭ"),
  bstack1l1l1ll_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᡮ"),
  bstack1l1l1ll_opy_ (u"ࠫࡷ࡫ࡧࡪࡱࡱࠫᡯ"),
  bstack1l1l1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧᡰ"),
  bstack1l1l1ll_opy_ (u"࠭࡭ࡢࡥ࡫࡭ࡳ࡫ࠧᡱ"),
  bstack1l1l1ll_opy_ (u"ࠧࡳࡧࡶࡳࡱࡻࡴࡪࡱࡱࠫᡲ"),
  bstack1l1l1ll_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᡳ"),
  bstack1l1l1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ᡴ"),
  bstack1l1l1ll_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩᡵ"),
  bstack1l1l1ll_opy_ (u"ࠫࡳࡵࡐࡢࡩࡨࡐࡴࡧࡤࡕ࡫ࡰࡩࡴࡻࡴࠨᡶ"),
  bstack1l1l1ll_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭ᡷ"),
  bstack1l1l1ll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᡸ"),
  bstack1l1l1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ᡹"),
  bstack1l1l1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩ᡺"),
  bstack1l1l1ll_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭᡻"),
  bstack1l1l1ll_opy_ (u"ࠪࡲࡴࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠧ᡼"),
  bstack1l1l1ll_opy_ (u"ࠫࡨ࡮ࡥࡤ࡭ࡘࡖࡑ࠭᡽"),
  bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᡾"),
  bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡉ࡯ࡰ࡭࡬ࡩࡸ࠭᡿"),
  bstack1l1l1ll_opy_ (u"ࠧࡤࡣࡳࡸࡺࡸࡥࡄࡴࡤࡷ࡭࠭ᢀ"),
  bstack1l1l1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᢁ"),
  bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᢂ"),
  bstack1l1l1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡖࡦࡴࡶ࡭ࡴࡴࠧᢃ"),
  bstack1l1l1ll_opy_ (u"ࠫࡳࡵࡂ࡭ࡣࡱ࡯ࡕࡵ࡬࡭࡫ࡱ࡫ࠬᢄ"),
  bstack1l1l1ll_opy_ (u"ࠬࡳࡡࡴ࡭ࡖࡩࡳࡪࡋࡦࡻࡶࠫᢅ"),
  bstack1l1l1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡒ࡯ࡨࡵࠪᢆ"),
  bstack1l1l1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡉࡥࠩᢇ"),
  bstack1l1l1ll_opy_ (u"ࠨࡦࡨࡨ࡮ࡩࡡࡵࡧࡧࡈࡪࡼࡩࡤࡧࠪᢈ"),
  bstack1l1l1ll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡒࡤࡶࡦࡳࡳࠨᢉ"),
  bstack1l1l1ll_opy_ (u"ࠪࡴ࡭ࡵ࡮ࡦࡐࡸࡱࡧ࡫ࡲࠨᢊ"),
  bstack1l1l1ll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩᢋ"),
  bstack1l1l1ll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡒࡴࡹ࡯࡯࡯ࡵࠪᢌ"),
  bstack1l1l1ll_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫᢍ"),
  bstack1l1l1ll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᢎ"),
  bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬᢏ"),
  bstack1l1l1ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡄ࡬ࡳࡲ࡫ࡴࡳ࡫ࡦࠫᢐ"),
  bstack1l1l1ll_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࡘ࠵ࠫᢑ"),
  bstack1l1l1ll_opy_ (u"ࠫࡲ࡯ࡤࡔࡧࡶࡷ࡮ࡵ࡮ࡊࡰࡶࡸࡦࡲ࡬ࡂࡲࡳࡷࠬᢒ"),
  bstack1l1l1ll_opy_ (u"ࠬ࡫ࡳࡱࡴࡨࡷࡸࡵࡓࡦࡴࡹࡩࡷ࠭ᢓ"),
  bstack1l1l1ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬᢔ"),
  bstack1l1l1ll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡅࡧࡴࠬᢕ"),
  bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨᢖ"),
  bstack1l1l1ll_opy_ (u"ࠩࡶࡽࡳࡩࡔࡪ࡯ࡨ࡛࡮ࡺࡨࡏࡖࡓࠫᢗ"),
  bstack1l1l1ll_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᢘ"),
  bstack1l1l1ll_opy_ (u"ࠫ࡬ࡶࡳࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᢙ"),
  bstack1l1l1ll_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ᢚ"),
  bstack1l1l1ll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ᢛ"),
  bstack1l1l1ll_opy_ (u"ࠧࡧࡱࡵࡧࡪࡉࡨࡢࡰࡪࡩࡏࡧࡲࠨᢜ"),
  bstack1l1l1ll_opy_ (u"ࠨࡺࡰࡷࡏࡧࡲࠨᢝ"),
  bstack1l1l1ll_opy_ (u"ࠩࡻࡱࡽࡐࡡࡳࠩᢞ"),
  bstack1l1l1ll_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩᢟ"),
  bstack1l1l1ll_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫᢠ"),
  bstack1l1l1ll_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭ᢡ"),
  bstack1l1l1ll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᢢ"),
  bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳ࡚ࡪࡸࡳࡪࡱࡱࠫᢣ"),
  bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧᢤ"),
  bstack1l1l1ll_opy_ (u"ࠩࡵࡩࡸ࡯ࡧ࡯ࡃࡳࡴࠬᢥ"),
  bstack1l1l1ll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳࡹࠧᢦ"),
  bstack1l1l1ll_opy_ (u"ࠫࡨࡧ࡮ࡢࡴࡼࠫᢧ"),
  bstack1l1l1ll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ᢨ"),
  bstack1l1l1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪᢩ࠭"),
  bstack1l1l1ll_opy_ (u"ࠧࡪࡧࠪᢪ"),
  bstack1l1l1ll_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭᢫"),
  bstack1l1l1ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ᢬"),
  bstack1l1l1ll_opy_ (u"ࠪࡵࡺ࡫ࡵࡦࠩ᢭"),
  bstack1l1l1ll_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡱࡥࡱ࠭᢮"),
  bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡱࡕࡷࡳࡷ࡫ࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳ࠭᢯"),
  bstack1l1l1ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡉࡡ࡮ࡧࡵࡥࡎࡳࡡࡨࡧࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬᢰ"),
  bstack1l1l1ll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡊࡾࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪᢱ"),
  bstack1l1l1ll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡏ࡮ࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫᢲ"),
  bstack1l1l1ll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᢳ"),
  bstack1l1l1ll_opy_ (u"ࠪࡶࡪࡹࡥࡳࡸࡨࡈࡪࡼࡩࡤࡧࠪᢴ"),
  bstack1l1l1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᢵ"),
  bstack1l1l1ll_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧᢶ"),
  bstack1l1l1ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡡࡴࡵࡦࡳࡩ࡫ࠧᢷ"),
  bstack1l1l1ll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡉࡰࡵࡇࡩࡻ࡯ࡣࡦࡕࡨࡸࡹ࡯࡮ࡨࡵࠪᢸ"),
  bstack1l1l1ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡷࡧ࡭ࡴࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨᢹ"),
  bstack1l1l1ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡳࡴࡱ࡫ࡐࡢࡻࠪᢺ"),
  bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᢻ"),
  bstack1l1l1ll_opy_ (u"ࠫࡼࡪࡩࡰࡕࡨࡶࡻ࡯ࡣࡦࠩᢼ"),
  bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᢽ"),
  bstack1l1l1ll_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡃࡳࡱࡶࡷࡘ࡯ࡴࡦࡖࡵࡥࡨࡱࡩ࡯ࡩࠪᢾ"),
  bstack1l1l1ll_opy_ (u"ࠧࡩ࡫ࡪ࡬ࡈࡵ࡮ࡵࡴࡤࡷࡹ࠭ᢿ"),
  bstack1l1l1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡑࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࡷࠬᣀ"),
  bstack1l1l1ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬᣁ"),
  bstack1l1l1ll_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧᣂ"),
  bstack1l1l1ll_opy_ (u"ࠫࡷ࡫࡭ࡰࡸࡨࡍࡔ࡙ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࡐࡴࡩࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩᣃ"),
  bstack1l1l1ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᣄ"),
  bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᣅ"),
  bstack1l1l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᣆ"),
  bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᣇ"),
  bstack1l1l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᣈ"),
  bstack1l1l1ll_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ᣉ"),
  bstack1l1l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪᣊ"),
  bstack1l1l1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧᣋ"),
  bstack1l1l1ll_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩᣌ")
]
bstack1ll1l1l1_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠧࡷࠩᣍ"): bstack1l1l1ll_opy_ (u"ࠨࡸࠪᣎ"),
  bstack1l1l1ll_opy_ (u"ࠩࡩࠫᣏ"): bstack1l1l1ll_opy_ (u"ࠪࡪࠬᣐ"),
  bstack1l1l1ll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪᣑ"): bstack1l1l1ll_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫᣒ"),
  bstack1l1l1ll_opy_ (u"࠭࡯࡯࡮ࡼࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᣓ"): bstack1l1l1ll_opy_ (u"ࠧࡰࡰ࡯ࡽࡆࡻࡴࡰ࡯ࡤࡸࡪ࠭ᣔ"),
  bstack1l1l1ll_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬᣕ"): bstack1l1l1ll_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭ᣖ"),
  bstack1l1l1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭ᣗ"): bstack1l1l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᣘ"),
  bstack1l1l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨᣙ"): bstack1l1l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩᣚ"),
  bstack1l1l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᣛ"): bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᣜ"),
  bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᣝ"): bstack1l1l1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᣞ"),
  bstack1l1l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬᣟ"): bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡊࡲࡷࡹ࠭ᣠ"),
  bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧᣡ"): bstack1l1l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨᣢ"),
  bstack1l1l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᣣ"): bstack1l1l1ll_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫᣤ"),
  bstack1l1l1ll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᣥ"): bstack1l1l1ll_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᣦ"),
  bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᣧ"): bstack1l1l1ll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨᣨ"),
  bstack1l1l1ll_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᣩ"): bstack1l1l1ll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪᣪ"),
  bstack1l1l1ll_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ᣫ"): bstack1l1l1ll_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧᣬ"),
  bstack1l1l1ll_opy_ (u"ࠫࡵࡧࡣࡧ࡫࡯ࡩࠬᣭ"): bstack1l1l1ll_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᣮ"),
  bstack1l1l1ll_opy_ (u"࠭ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᣯ"): bstack1l1l1ll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᣰ"),
  bstack1l1l1ll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᣱ"): bstack1l1l1ll_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᣲ"),
  bstack1l1l1ll_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫᣳ"): bstack1l1l1ll_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬᣴ"),
  bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᣵ"): bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᣶"),
  bstack1l1l1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩ᣷"): bstack1l1l1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡳࡩࡦࡺࡥࡳࠩ᣸")
}
bstack11l1lllll11_opy_ = bstack1l1l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫࡮ࡺࡨࡶࡤ࠱ࡧࡴࡳ࠯ࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫࠲ࡶࡪࡲࡥࡢࡵࡨࡷ࠴ࡲࡡࡵࡧࡶࡸ࠴ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢ᣹")
bstack11l1llllll1_opy_ = bstack1l1l1ll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠲࡬ࡪࡧ࡬ࡵࡪࡦ࡬ࡪࡩ࡫ࠣ᣺")
bstack1111lllll_opy_ = bstack1l1l1ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡫ࡤࡴ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡹࡥ࡯ࡦࡢࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢ᣻")
bstack1lllllllll_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭᣼")
bstack11l11l1l_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩ᣽")
bstack1l1ll1111_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡰࡨࡼࡹࡥࡨࡶࡤࡶࠫ᣾")
bstack11l1lll11ll_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠨࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠪ᣿"): 50,
  bstack1l1l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᤀ"): 40,
  bstack1l1l1ll_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫᤁ"): 30,
  bstack1l1l1ll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᤂ"): 20,
  bstack1l1l1ll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᤃ"): 10
}
bstack1l111lll11_opy_ = bstack11l1lll11ll_opy_[bstack1l1l1ll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᤄ")]
bstack11111111l_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᤅ")
bstack11l1lll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᤆ")
bstack1l111l111_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᤇ")
bstack1l1111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᤈ")
bstack1l1l1111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡧ࡮ࡥࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡵࡧࡣ࡬ࡣࡪࡩࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩᤉ")
bstack11ll11111l1_opy_ = [bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᤊ"), bstack1l1l1ll_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᤋ")]
bstack11l1lllll1l_opy_ = [bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᤌ"), bstack1l1l1ll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᤍ")]
bstack11ll1l1ll_opy_ = re.compile(bstack1l1l1ll_opy_ (u"ࠩࡡ࡟ࡡࡢࡷ࠮࡟࠮࠾࠳࠰ࠤࠨᤎ"))
bstack1l1llll1_opy_ = [
  bstack1l1l1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡎࡢ࡯ࡨࠫᤏ"),
  bstack1l1l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᤐ"),
  bstack1l1l1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᤑ"),
  bstack1l1l1ll_opy_ (u"࠭࡮ࡦࡹࡆࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪᤒ"),
  bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳࠫᤓ"),
  bstack1l1l1ll_opy_ (u"ࠨࡷࡧ࡭ࡩ࠭ᤔ"),
  bstack1l1l1ll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫᤕ"),
  bstack1l1l1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࠪᤖ"),
  bstack1l1l1ll_opy_ (u"ࠫࡴࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᤗ"),
  bstack1l1l1ll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࠪᤘ"),
  bstack1l1l1ll_opy_ (u"࠭࡮ࡰࡔࡨࡷࡪࡺࠧᤙ"), bstack1l1l1ll_opy_ (u"ࠧࡧࡷ࡯ࡰࡗ࡫ࡳࡦࡶࠪᤚ"),
  bstack1l1l1ll_opy_ (u"ࠨࡥ࡯ࡩࡦࡸࡓࡺࡵࡷࡩࡲࡌࡩ࡭ࡧࡶࠫᤛ"),
  bstack1l1l1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡕ࡫ࡰ࡭ࡳ࡭ࡳࠨᤜ"),
  bstack1l1l1ll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࡌࡰࡩࡪ࡭ࡳ࡭ࠧᤝ"),
  bstack1l1l1ll_opy_ (u"ࠫࡴࡺࡨࡦࡴࡄࡴࡵࡹࠧᤞ"),
  bstack1l1l1ll_opy_ (u"ࠬࡶࡲࡪࡰࡷࡔࡦ࡭ࡥࡔࡱࡸࡶࡨ࡫ࡏ࡯ࡈ࡬ࡲࡩࡌࡡࡪ࡮ࡸࡶࡪ࠭᤟"),
  bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲࡄࡧࡹ࡯ࡶࡪࡶࡼࠫᤠ"), bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳࡔࡦࡩ࡫ࡢࡩࡨࠫᤡ"), bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡃࡦࡸ࡮ࡼࡩࡵࡻࠪᤢ"), bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡓࡥࡨࡱࡡࡨࡧࠪᤣ"), bstack1l1l1ll_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᤤ"),
  bstack1l1l1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩᤥ"),
  bstack1l1l1ll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡪࡹࡴࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩᤦ"),
  bstack1l1l1ll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࠨᤧ"), bstack1l1l1ll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࡇࡱࡨࡎࡴࡴࡦࡰࡷࠫᤨ"),
  bstack1l1l1ll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᤩ"),
  bstack1l1l1ll_opy_ (u"ࠩࡤࡨࡧࡖ࡯ࡳࡶࠪᤪ"),
  bstack1l1l1ll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡖࡳࡨࡱࡥࡵࠩᤫ"),
  bstack1l1l1ll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰ࡙࡯࡭ࡦࡱࡸࡸࠬ᤬"),
  bstack1l1l1ll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡵࡪࠪ᤭"),
  bstack1l1l1ll_opy_ (u"࠭ࡡࡷࡦࠪ᤮"), bstack1l1l1ll_opy_ (u"ࠧࡢࡸࡧࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᤯"), bstack1l1l1ll_opy_ (u"ࠨࡣࡹࡨࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪᤰ"), bstack1l1l1ll_opy_ (u"ࠩࡤࡺࡩࡇࡲࡨࡵࠪᤱ"),
  bstack1l1l1ll_opy_ (u"ࠪࡹࡸ࡫ࡋࡦࡻࡶࡸࡴࡸࡥࠨᤲ"), bstack1l1l1ll_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡵࡪࠪᤳ"), bstack1l1l1ll_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡵࡶࡻࡴࡸࡤࠨᤴ"),
  bstack1l1l1ll_opy_ (u"࠭࡫ࡦࡻࡄࡰ࡮ࡧࡳࠨᤵ"), bstack1l1l1ll_opy_ (u"ࠧ࡬ࡧࡼࡔࡦࡹࡳࡸࡱࡵࡨࠬᤶ"),
  bstack1l1l1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪᤷ"), bstack1l1l1ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡂࡴࡪࡷࠬᤸ"), bstack1l1l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࡉ࡯ࡲࠨ᤹"), bstack1l1l1ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡆ࡬ࡷࡵ࡭ࡦࡏࡤࡴࡵ࡯࡮ࡨࡈ࡬ࡰࡪ࠭᤺"), bstack1l1l1ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵ࡙ࡸ࡫ࡓࡺࡵࡷࡩࡲࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦ᤻ࠩ"),
  bstack1l1l1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࠩ᤼"), bstack1l1l1ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࡶࠫ᤽"),
  bstack1l1l1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡄࡪࡵࡤࡦࡱ࡫ࡂࡶ࡫࡯ࡨࡈ࡮ࡥࡤ࡭ࠪ᤾"),
  bstack1l1l1ll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࡔࡪ࡯ࡨࡳࡺࡺࠧ᤿"),
  bstack1l1l1ll_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡄࡧࡹ࡯࡯࡯ࠩ᥀"), bstack1l1l1ll_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡇࡦࡺࡥࡨࡱࡵࡽࠬ᥁"), bstack1l1l1ll_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡋࡲࡡࡨࡵࠪ᥂"), bstack1l1l1ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࡊࡰࡷࡩࡳࡺࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩ᥃"),
  bstack1l1l1ll_opy_ (u"ࠧࡥࡱࡱࡸࡘࡺ࡯ࡱࡃࡳࡴࡔࡴࡒࡦࡵࡨࡸࠬ᥄"),
  bstack1l1l1ll_opy_ (u"ࠨࡷࡱ࡭ࡨࡵࡤࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪ᥅"), bstack1l1l1ll_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡌࡧࡼࡦࡴࡧࡲࡥࠩ᥆"),
  bstack1l1l1ll_opy_ (u"ࠪࡲࡴ࡙ࡩࡨࡰࠪ᥇"),
  bstack1l1l1ll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨ࡙ࡳ࡯࡭ࡱࡱࡵࡸࡦࡴࡴࡗ࡫ࡨࡻࡸ࠭᥈"),
  bstack1l1l1ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡥࡴࡲ࡭ࡩ࡝ࡡࡵࡥ࡫ࡩࡷࡹࠧ᥉"),
  bstack1l1l1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᥊"),
  bstack1l1l1ll_opy_ (u"ࠧࡳࡧࡦࡶࡪࡧࡴࡦࡅ࡫ࡶࡴࡳࡥࡅࡴ࡬ࡺࡪࡸࡓࡦࡵࡶ࡭ࡴࡴࡳࠨ᥋"),
  bstack1l1l1ll_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ᥌"),
  bstack1l1l1ll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡖࡡࡵࡪࠪ᥍"),
  bstack1l1l1ll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡗࡵ࡫ࡥࡥࠩ᥎"),
  bstack1l1l1ll_opy_ (u"ࠫ࡬ࡶࡳࡆࡰࡤࡦࡱ࡫ࡤࠨ᥏"),
  bstack1l1l1ll_opy_ (u"ࠬ࡯ࡳࡉࡧࡤࡨࡱ࡫ࡳࡴࠩᥐ"),
  bstack1l1l1ll_opy_ (u"࠭ࡡࡥࡤࡈࡼࡪࡩࡔࡪ࡯ࡨࡳࡺࡺࠧᥑ"),
  bstack1l1l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ᥒ"),
  bstack1l1l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡊࡥࡷ࡫ࡦࡩࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬᥓ"),
  bstack1l1l1ll_opy_ (u"ࠩࡤࡹࡹࡵࡇࡳࡣࡱࡸࡕ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠩᥔ"),
  bstack1l1l1ll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡒࡦࡺࡵࡳࡣ࡯ࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᥕ"),
  bstack1l1l1ll_opy_ (u"ࠫࡸࡿࡳࡵࡧࡰࡔࡴࡸࡴࠨᥖ"),
  bstack1l1l1ll_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡪࡢࡉࡱࡶࡸࠬᥗ"),
  bstack1l1l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳ࡙ࡳࡲ࡯ࡤ࡭ࠪᥘ"), bstack1l1l1ll_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡔࡺࡲࡨࠫᥙ"), bstack1l1l1ll_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡌࡧࡼࠫᥚ"),
  bstack1l1l1ll_opy_ (u"ࠩࡤࡹࡹࡵࡌࡢࡷࡱࡧ࡭࠭ᥛ"),
  bstack1l1l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡧࡦࡺࡃࡢࡲࡷࡹࡷ࡫ࠧᥜ"),
  bstack1l1l1ll_opy_ (u"ࠫࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࡏࡵࡪࡨࡶࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ᥝ"),
  bstack1l1l1ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪ࡝ࡩ࡯ࡦࡲࡻࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࠧᥞ"),
  bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡵ࡯࡭ࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᥟ"),
  bstack1l1l1ll_opy_ (u"ࠧࡦࡰࡩࡳࡷࡩࡥࡂࡲࡳࡍࡳࡹࡴࡢ࡮࡯ࠫᥠ"),
  bstack1l1l1ll_opy_ (u"ࠨࡧࡱࡷࡺࡸࡥࡘࡧࡥࡺ࡮࡫ࡷࡴࡊࡤࡺࡪࡖࡡࡨࡧࡶࠫᥡ"), bstack1l1l1ll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡇࡩࡻࡺ࡯ࡰ࡮ࡶࡔࡴࡸࡴࠨᥢ"), bstack1l1l1ll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧ࡚ࡩࡧࡼࡩࡦࡹࡇࡩࡹࡧࡩ࡭ࡵࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠭ᥣ"),
  bstack1l1l1ll_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡵࡶࡳࡄࡣࡦ࡬ࡪࡒࡩ࡮࡫ࡷࠫᥤ"),
  bstack1l1l1ll_opy_ (u"ࠬࡩࡡ࡭ࡧࡱࡨࡦࡸࡆࡰࡴࡰࡥࡹ࠭ᥥ"),
  bstack1l1l1ll_opy_ (u"࠭ࡢࡶࡰࡧࡰࡪࡏࡤࠨᥦ"),
  bstack1l1l1ll_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧᥧ"),
  bstack1l1l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡉࡳࡧࡢ࡭ࡧࡧࠫᥨ"), bstack1l1l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡆࡻࡴࡩࡱࡵ࡭ࡿ࡫ࡤࠨᥩ"),
  bstack1l1l1ll_opy_ (u"ࠪࡥࡺࡺ࡯ࡂࡥࡦࡩࡵࡺࡁ࡭ࡧࡵࡸࡸ࠭ᥪ"), bstack1l1l1ll_opy_ (u"ࠫࡦࡻࡴࡰࡆ࡬ࡷࡲ࡯ࡳࡴࡃ࡯ࡩࡷࡺࡳࠨᥫ"),
  bstack1l1l1ll_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡴࡎ࡬ࡦࠬᥬ"),
  bstack1l1l1ll_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡖࡤࡴࠬᥭ"),
  bstack1l1l1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉ࡯࡫ࡷ࡭ࡦࡲࡕࡳ࡮ࠪ᥮"), bstack1l1l1ll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡂ࡮࡯ࡳࡼࡖ࡯ࡱࡷࡳࡷࠬ᥯"), bstack1l1l1ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡪࡲࡴࡸࡥࡇࡴࡤࡹࡩ࡝ࡡࡳࡰ࡬ࡲ࡬࠭ᥰ"), bstack1l1l1ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡪࡴࡌࡪࡰ࡮ࡷࡎࡴࡂࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠪᥱ"),
  bstack1l1l1ll_opy_ (u"ࠫࡰ࡫ࡥࡱࡍࡨࡽࡈ࡮ࡡࡪࡰࡶࠫᥲ"),
  bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡿࡧࡢ࡭ࡧࡖࡸࡷ࡯࡮ࡨࡵࡇ࡭ࡷ࠭ᥳ"),
  bstack1l1l1ll_opy_ (u"࠭ࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩᥴ"),
  bstack1l1l1ll_opy_ (u"ࠧࡪࡰࡷࡩࡷࡑࡥࡺࡆࡨࡰࡦࡿࠧ᥵"),
  bstack1l1l1ll_opy_ (u"ࠨࡵ࡫ࡳࡼࡏࡏࡔࡎࡲ࡫ࠬ᥶"),
  bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡖࡸࡷࡧࡴࡦࡩࡼࠫ᥷"),
  bstack1l1l1ll_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡕࡩࡸࡶ࡯࡯ࡵࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ᥸"), bstack1l1l1ll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡘࡣ࡬ࡸ࡙࡯࡭ࡦࡱࡸࡸࠬ᥹"),
  bstack1l1l1ll_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࠨ᥺"),
  bstack1l1l1ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡳࡺࡰࡦࡉࡽ࡫ࡣࡶࡶࡨࡊࡷࡵ࡭ࡉࡶࡷࡴࡸ࠭᥻"),
  bstack1l1l1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡄࡣࡳࡸࡺࡸࡥࠨ᥼"),
  bstack1l1l1ll_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨ᥽"),
  bstack1l1l1ll_opy_ (u"ࠩࡩࡹࡱࡲࡃࡰࡰࡷࡩࡽࡺࡌࡪࡵࡷࠫ᥾"),
  bstack1l1l1ll_opy_ (u"ࠪࡻࡦ࡯ࡴࡇࡱࡵࡅࡵࡶࡓࡤࡴ࡬ࡴࡹ࠭᥿"),
  bstack1l1l1ll_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡈࡵ࡮࡯ࡧࡦࡸࡗ࡫ࡴࡳ࡫ࡨࡷࠬᦀ"),
  bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡱࡐࡤࡱࡪ࠭ᦁ"),
  bstack1l1l1ll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡓࡍࡅࡨࡶࡹ࠭ᦂ"),
  bstack1l1l1ll_opy_ (u"ࠧࡵࡣࡳ࡛࡮ࡺࡨࡔࡪࡲࡶࡹࡖࡲࡦࡵࡶࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᦃ"),
  bstack1l1l1ll_opy_ (u"ࠨࡵࡦࡥࡱ࡫ࡆࡢࡥࡷࡳࡷ࠭ᦄ"),
  bstack1l1l1ll_opy_ (u"ࠩࡺࡨࡦࡒ࡯ࡤࡣ࡯ࡔࡴࡸࡴࠨᦅ"),
  bstack1l1l1ll_opy_ (u"ࠪࡷ࡭ࡵࡷ࡙ࡥࡲࡨࡪࡒ࡯ࡨࠩᦆ"),
  bstack1l1l1ll_opy_ (u"ࠫ࡮ࡵࡳࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡸࡷࡪ࠭ᦇ"),
  bstack1l1l1ll_opy_ (u"ࠬࡾࡣࡰࡦࡨࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠧᦈ"),
  bstack1l1l1ll_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡶࡷࡼࡵࡲࡥࠩᦉ"),
  bstack1l1l1ll_opy_ (u"ࠧࡶࡵࡨࡔࡷ࡫ࡢࡶ࡫࡯ࡸ࡜ࡊࡁࠨᦊ"),
  bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵ࡙ࡇࡅࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠩᦋ"),
  bstack1l1l1ll_opy_ (u"ࠩࡺࡩࡧࡊࡲࡪࡸࡨࡶࡆ࡭ࡥ࡯ࡶࡘࡶࡱ࠭ᦌ"),
  bstack1l1l1ll_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡴࡩࠩᦍ"),
  bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡏࡧࡺ࡛ࡉࡇࠧᦎ"),
  bstack1l1l1ll_opy_ (u"ࠬࡽࡤࡢࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᦏ"), bstack1l1l1ll_opy_ (u"࠭ࡷࡥࡣࡆࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᦐ"),
  bstack1l1l1ll_opy_ (u"ࠧࡹࡥࡲࡨࡪࡕࡲࡨࡋࡧࠫᦑ"), bstack1l1l1ll_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡓࡪࡩࡱ࡭ࡳ࡭ࡉࡥࠩᦒ"),
  bstack1l1l1ll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦ࡚ࡈࡆࡈࡵ࡯ࡦ࡯ࡩࡎࡪࠧᦓ"),
  bstack1l1l1ll_opy_ (u"ࠪࡶࡪࡹࡥࡵࡑࡱࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡲࡵࡑࡱࡰࡾ࠭ᦔ"),
  bstack1l1l1ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࡸ࠭ᦕ"),
  bstack1l1l1ll_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷ࡯ࡥࡴࠩᦖ"), bstack1l1l1ll_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡹࡊࡰࡷࡩࡷࡼࡡ࡭ࠩᦗ"),
  bstack1l1l1ll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࡉࡣࡵࡨࡼࡧࡲࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪᦘ"),
  bstack1l1l1ll_opy_ (u"ࠨ࡯ࡤࡼ࡙ࡿࡰࡪࡰࡪࡊࡷ࡫ࡱࡶࡧࡱࡧࡾ࠭ᦙ"),
  bstack1l1l1ll_opy_ (u"ࠩࡶ࡭ࡲࡶ࡬ࡦࡋࡶ࡚࡮ࡹࡩࡣ࡮ࡨࡇ࡭࡫ࡣ࡬ࠩᦚ"),
  bstack1l1l1ll_opy_ (u"ࠪࡹࡸ࡫ࡃࡢࡴࡷ࡬ࡦ࡭ࡥࡔࡵ࡯ࠫᦛ"),
  bstack1l1l1ll_opy_ (u"ࠫࡸ࡮࡯ࡶ࡮ࡧ࡙ࡸ࡫ࡓࡪࡰࡪࡰࡪࡺ࡯࡯ࡖࡨࡷࡹࡓࡡ࡯ࡣࡪࡩࡷ࠭ᦜ"),
  bstack1l1l1ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡍ࡜ࡊࡐࠨᦝ"),
  bstack1l1l1ll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙ࡵࡵࡤࡪࡌࡨࡊࡴࡲࡰ࡮࡯ࠫᦞ"),
  bstack1l1l1ll_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡈࡪࡦࡧࡩࡳࡇࡰࡪࡒࡲࡰ࡮ࡩࡹࡆࡴࡵࡳࡷ࠭ᦟ"),
  bstack1l1l1ll_opy_ (u"ࠨ࡯ࡲࡧࡰࡒ࡯ࡤࡣࡷ࡭ࡴࡴࡁࡱࡲࠪᦠ"),
  bstack1l1l1ll_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈࡲࡶࡲࡧࡴࠨᦡ"), bstack1l1l1ll_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉ࡭ࡱࡺࡥࡳࡕࡳࡩࡨࡹࠧᦢ"),
  bstack1l1l1ll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡇࡩࡱࡧࡹࡂࡦࡥࠫᦣ"),
  bstack1l1l1ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡏࡤࡍࡱࡦࡥࡹࡵࡲࡂࡷࡷࡳࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠨᦤ")
]
bstack1l11ll1l11_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡻࡰ࡭ࡱࡤࡨࠬᦥ")
bstack1l111ll1l1_opy_ = [bstack1l1l1ll_opy_ (u"ࠧ࠯ࡣࡳ࡯ࠬᦦ"), bstack1l1l1ll_opy_ (u"ࠨ࠰ࡤࡥࡧ࠭ᦧ"), bstack1l1l1ll_opy_ (u"ࠩ࠱࡭ࡵࡧࠧᦨ")]
bstack1l1l1ll1ll_opy_ = [bstack1l1l1ll_opy_ (u"ࠪ࡭ࡩ࠭ᦩ"), bstack1l1l1ll_opy_ (u"ࠫࡵࡧࡴࡩࠩᦪ"), bstack1l1l1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨᦫ"), bstack1l1l1ll_opy_ (u"࠭ࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࠬ᦬")]
bstack11l1l11lll_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᦭"): bstack1l1l1ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᦮"),
  bstack1l1l1ll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ᦯"): bstack1l1l1ll_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᦰ"),
  bstack1l1l1ll_opy_ (u"ࠫࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᦱ"): bstack1l1l1ll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦲ"),
  bstack1l1l1ll_opy_ (u"࠭ࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᦳ"): bstack1l1l1ll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦴ"),
  bstack1l1l1ll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡷ࡭ࡴࡴࡳࠨᦵ"): bstack1l1l1ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᦶ")
}
bstack11ll1lll1_opy_ = [
  bstack1l1l1ll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᦷ"),
  bstack1l1l1ll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩᦸ"),
  bstack1l1l1ll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦹ"),
  bstack1l1l1ll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬᦺ"),
  bstack1l1l1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨᦻ"),
]
bstack1l11l1lll1_opy_ = bstack1l1l11ll1_opy_ + bstack11l1lll111l_opy_ + bstack1l1llll1_opy_
bstack11lllll11_opy_ = [
  bstack1l1l1ll_opy_ (u"ࠨࡠ࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸࠩ࠭ᦼ"),
  bstack1l1l1ll_opy_ (u"ࠩࡡࡦࡸ࠳࡬ࡰࡥࡤࡰ࠳ࡩ࡯࡮ࠦࠪᦽ"),
  bstack1l1l1ll_opy_ (u"ࠪࡢ࠶࠸࠷࠯ࠩᦾ"),
  bstack1l1l1ll_opy_ (u"ࠫࡣ࠷࠰࠯ࠩᦿ"),
  bstack1l1l1ll_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠵ࡠ࠼࠭࠺࡟࠱ࠫᧀ"),
  bstack1l1l1ll_opy_ (u"࠭࡞࠲࠹࠵࠲࠷ࡡ࠰࠮࠻ࡠ࠲ࠬᧁ"),
  bstack1l1l1ll_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠹࡛࠱࠯࠴ࡡ࠳࠭ᧂ"),
  bstack1l1l1ll_opy_ (u"ࠨࡠ࠴࠽࠷࠴࠱࠷࠺࠱ࠫᧃ")
]
bstack11ll11l1lll_opy_ = bstack1l1l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᧄ")
bstack1l1l1ll111_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱ࠯ࡷ࠳࠲ࡩࡻ࡫࡮ࡵࠩᧅ")
bstack1l1llll11_opy_ = [ bstack1l1l1ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᧆ") ]
bstack1ll11ll1l1_opy_ = [ bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᧇ") ]
bstack1llll11ll_opy_ = [bstack1l1l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᧈ")]
bstack11l1111l1_opy_ = [ bstack1l1l1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᧉ") ]
bstack11l1ll111l_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡕࡇࡏࡘ࡫ࡴࡶࡲࠪ᧊")
bstack1l1l1ll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠬ᧋")
bstack1lll1ll11_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠧ᧌")
bstack1111l1l11_opy_ = bstack1l1l1ll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࠪ᧍")
bstack11lll1l1l_opy_ = [
  bstack1l1l1ll_opy_ (u"ࠬࡋࡒࡓࡡࡉࡅࡎࡒࡅࡅࠩ᧎"),
  bstack1l1l1ll_opy_ (u"࠭ࡅࡓࡔࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭᧏"),
  bstack1l1l1ll_opy_ (u"ࠧࡆࡔࡕࡣࡇࡒࡏࡄࡍࡈࡈࡤࡈ࡙ࡠࡅࡏࡍࡊࡔࡔࠨ᧐"),
  bstack1l1l1ll_opy_ (u"ࠨࡇࡕࡖࡤࡔࡅࡕ࡙ࡒࡖࡐࡥࡃࡉࡃࡑࡋࡊࡊࠧ᧑"),
  bstack1l1l1ll_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡉ࡙ࡥࡎࡐࡖࡢࡇࡔࡔࡎࡆࡅࡗࡉࡉ࠭᧒"),
  bstack1l1l1ll_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡈࡒࡏࡔࡇࡇࠫ᧓"),
  bstack1l1l1ll_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡘࡅࡔࡇࡗࠫ᧔"),
  bstack1l1l1ll_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡈࡘࡗࡊࡊࠧ᧕"),
  bstack1l1l1ll_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡂࡄࡒࡖ࡙ࡋࡄࠨ᧖"),
  bstack1l1l1ll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨ᧗"),
  bstack1l1l1ll_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡒࡔ࡚࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࠩ᧘"),
  bstack1l1l1ll_opy_ (u"ࠩࡈࡖࡗࡥࡁࡅࡆࡕࡉࡘ࡙࡟ࡊࡐ࡙ࡅࡑࡏࡄࠨ᧙"),
  bstack1l1l1ll_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡗࡑࡖࡊࡇࡃࡉࡃࡅࡐࡊ࠭᧚"),
  bstack1l1l1ll_opy_ (u"ࠫࡊࡘࡒࡠࡖࡘࡒࡓࡋࡌࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ᧛"),
  bstack1l1l1ll_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡔࡊࡏࡈࡈࡤࡕࡕࡕࠩ᧜"),
  bstack1l1l1ll_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡔࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭᧝"),
  bstack1l1l1ll_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡉࡑࡖࡘࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪ᧞"),
  bstack1l1l1ll_opy_ (u"ࠨࡇࡕࡖࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨ᧟"),
  bstack1l1l1ll_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪ᧠"),
  bstack1l1l1ll_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡘࡅࡔࡑࡏ࡙࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ᧡"),
  bstack1l1l1ll_opy_ (u"ࠫࡊࡘࡒࡠࡏࡄࡒࡉࡇࡔࡐࡔ࡜ࡣࡕࡘࡏ࡙࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ᧢"),
]
bstack1l111l111l_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠴࠯ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠱ࠪ᧣")
bstack1ll1ll1l11_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"࠭ࡾࠨ᧤")), bstack1l1l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ᧥"), bstack1l1l1ll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ᧦"))
bstack11ll1ll111l_opy_ = bstack1l1l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱ࡫ࠪ᧧")
bstack11l1lll1l1l_opy_ = [ bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᧨"), bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ᧩"), bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ᧪"), bstack1l1l1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭᧫")]
bstack11l1l11ll_opy_ = [ bstack1l1l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᧬"), bstack1l1l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ᧭"), bstack1l1l1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ᧮"), bstack1l1l1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ᧯") ]
bstack11l11l1ll1_opy_ = [ bstack1l1l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ᧰") ]
bstack11l1ll1l1l1_opy_ = [ bstack1l1l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᧱") ]
bstack11l111111_opy_ = 360
bstack11ll11l1l11_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡡࡱࡲ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨ᧲")
bstack11l1lll1ll1_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡬ࡷࡸࡻࡥࡴࠤ᧳")
bstack11l1ll11lll_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠦ᧴")
bstack11ll1llll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠤࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡸࡪࡹࡴࡴࠢࡤࡶࡪࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡲࡲࠥࡕࡓࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࠨࡷࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥࠡࡨࡲࡶࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦࡤࡦࡸ࡬ࡧࡪࡹ࠮ࠣ᧵")
bstack11ll1ll1111_opy_ = bstack1l1l1ll_opy_ (u"ࠥ࠵࠶࠴࠰ࠣ᧶")
bstack111l1l11ll_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠫࡕࡇࡓࡔࠩ᧷"): bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᧸"),
  bstack1l1l1ll_opy_ (u"࠭ࡆࡂࡋࡏࠫ᧹"): bstack1l1l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᧺"),
  bstack1l1l1ll_opy_ (u"ࠨࡕࡎࡍࡕ࠭᧻"): bstack1l1l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ᧼")
}
bstack11l11l11_opy_ = [
  bstack1l1l1ll_opy_ (u"ࠥ࡫ࡪࡺࠢ᧽"),
  bstack1l1l1ll_opy_ (u"ࠦ࡬ࡵࡂࡢࡥ࡮ࠦ᧾"),
  bstack1l1l1ll_opy_ (u"ࠧ࡭࡯ࡇࡱࡵࡻࡦࡸࡤࠣ᧿"),
  bstack1l1l1ll_opy_ (u"ࠨࡲࡦࡨࡵࡩࡸ࡮ࠢᨀ"),
  bstack1l1l1ll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨᨁ"),
  bstack1l1l1ll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᨂ"),
  bstack1l1l1ll_opy_ (u"ࠤࡶࡹࡧࡳࡩࡵࡇ࡯ࡩࡲ࡫࡮ࡵࠤᨃ"),
  bstack1l1l1ll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢᨄ"),
  bstack1l1l1ll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢᨅ"),
  bstack1l1l1ll_opy_ (u"ࠧࡩ࡬ࡦࡣࡵࡉࡱ࡫࡭ࡦࡰࡷࠦᨆ"),
  bstack1l1l1ll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࡹࠢᨇ"),
  bstack1l1l1ll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠢᨈ"),
  bstack1l1l1ll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡃࡶࡽࡳࡩࡓࡤࡴ࡬ࡴࡹࠨᨉ"),
  bstack1l1l1ll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣᨊ"),
  bstack1l1l1ll_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᨋ"),
  bstack1l1l1ll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱ࡙ࡵࡵࡤࡪࡄࡧࡹ࡯࡯࡯ࠤᨌ"),
  bstack1l1l1ll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡓࡵ࡭ࡶ࡬ࡘࡴࡻࡣࡩࠤᨍ"),
  bstack1l1l1ll_opy_ (u"ࠨࡳࡩࡣ࡮ࡩࠧᨎ"),
  bstack1l1l1ll_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࡇࡰࡱࠤᨏ")
]
bstack11l1ll11111_opy_ = [
  bstack1l1l1ll_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࠢᨐ"),
  bstack1l1l1ll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᨑ"),
  bstack1l1l1ll_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᨒ"),
  bstack1l1l1ll_opy_ (u"ࠦࡲࡧ࡮ࡶࡣ࡯ࠦᨓ"),
  bstack1l1l1ll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᨔ")
]
bstack11ll1l11l1_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧᨕ"): [bstack1l1l1ll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨᨖ")],
  bstack1l1l1ll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᨗ"): [bstack1l1l1ll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᨘ")],
  bstack1l1l1ll_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᨙ"): [bstack1l1l1ll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣᨚ"), bstack1l1l1ll_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣᨛ"), bstack1l1l1ll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ᨜"), bstack1l1l1ll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨ᨝")],
  bstack1l1l1ll_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣ᨞"): [bstack1l1l1ll_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤ᨟")],
  bstack1l1l1ll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᨠ"): [bstack1l1l1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᨡ")],
}
bstack11l1ll1ll1l_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦᨢ"): bstack1l1l1ll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧᨣ"),
  bstack1l1l1ll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᨤ"): bstack1l1l1ll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᨥ"),
  bstack1l1l1ll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨᨦ"): bstack1l1l1ll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧᨧ"),
  bstack1l1l1ll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢᨨ"): bstack1l1l1ll_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࠢᨩ"),
  bstack1l1l1ll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᨪ"): bstack1l1l1ll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᨫ")
}
bstack111l11lll1_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᨬ"): bstack1l1l1ll_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡕࡨࡸࡺࡶࠧᨭ"),
  bstack1l1l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᨮ"): bstack1l1l1ll_opy_ (u"ࠫࡘࡻࡩࡵࡧࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬᨯ"),
  bstack1l1l1ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᨰ"): bstack1l1l1ll_opy_ (u"࠭ࡔࡦࡵࡷࠤࡘ࡫ࡴࡶࡲࠪᨱ"),
  bstack1l1l1ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᨲ"): bstack1l1l1ll_opy_ (u"ࠨࡖࡨࡷࡹࠦࡔࡦࡣࡵࡨࡴࡽ࡮ࠨᨳ")
}
bstack11l1llll1ll_opy_ = 65536
bstack11l1ll1111l_opy_ = bstack1l1l1ll_opy_ (u"ࠩ࠱࠲࠳ࡡࡔࡓࡗࡑࡇࡆ࡚ࡅࡅ࡟ࠪᨴ")
bstack11l1lll11l1_opy_ = [
      bstack1l1l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᨵ"), bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᨶ"), bstack1l1l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᨷ"), bstack1l1l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᨸ"), bstack1l1l1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩᨹ"),
      bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᨺ"), bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᨻ"), bstack1l1l1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫᨼ"), bstack1l1l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬᨽ"),
      bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᨾ"), bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᨿ"), bstack1l1l1ll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᩀ")
    ]
bstack11l1ll1l1ll_opy_= {
  bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᩁ"): bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᩂ"),
  bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᩃ"): bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᩄ"),
  bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᩅ"): bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪᩆ"),
  bstack1l1l1ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᩇ"): bstack1l1l1ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᩈ"),
  bstack1l1l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᩉ"): bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᩊ"),
  bstack1l1l1ll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᩋ"): bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᩌ"),
  bstack1l1l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᩍ"): bstack1l1l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᩎ"),
  bstack1l1l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᩏ"): bstack1l1l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᩐ"),
  bstack1l1l1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᩑ"): bstack1l1l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᩒ"),
  bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᩓ"): bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᩔ"),
  bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᩕ"): bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᩖ"),
  bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࠩᩗ"): bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪᩘ"),
  bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᩙ"): bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩚ"),
  bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩛ"): bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࠧᩜ"),
  bstack1l1l1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᩝ"): bstack1l1l1ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᩞ"),
  bstack1l1l1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᩟"): bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ᩠࠭"),
  bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᩡ"): bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᩢ"),
  bstack1l1l1ll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫᩣ"): bstack1l1l1ll_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᩤ"),
  bstack1l1l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᩥ"): bstack1l1l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᩦ"),
  bstack1l1l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᩧ"): bstack1l1l1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᩨ"),
  bstack1l1l1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᩩ"): bstack1l1l1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᩪ"),
  bstack1l1l1ll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᩫ"): bstack1l1l1ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᩬ"),
  bstack1l1l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᩭ"): bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᩮ"),
  bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᩯ"): bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩰ"),
  bstack1l1l1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᩱ"): bstack1l1l1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᩲ"),
  bstack1l1l1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩳ"): bstack1l1l1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩴ"),
  bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ᩵"): bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᩶"),
  bstack1l1l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭᩷"): bstack1l1l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧ᩸")
}
bstack11l1ll11l1l_opy_ = [bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᩹"), bstack1l1l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᩺")]
bstack1l1111l1l1_opy_ = (bstack1l1l1ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥ᩻"),)
bstack11l1ll111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡺࡶࡤࡢࡶࡨࡣࡨࡲࡩࠨ᩼")
bstack1l1l1111l_opy_ = bstack1l1l1ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡩࡵ࡭ࡩࡹ࠯ࠣ᩽")
bstack1lll1l11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨࡴ࡬ࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡤࡷ࡭ࡨ࡯ࡢࡴࡧ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࠧ᩾")
bstack1llll1l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠰ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮᩿ࠣ")
class EVENTS(Enum):
  bstack11l1ll111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࠱࠲ࡻ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬ᪀")
  bstack111l1ll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࠧ᪁") # final bstack11l1llll111_opy_
  bstack11l1ll1l111_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡱࡨࡱࡵࡧࡴࠩ᪂")
  bstack11l1l1llll_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠿ࡶࡲࡪࡰࡷ࠱ࡧࡻࡩ࡭ࡦ࡯࡭ࡳࡱࠧ᪃") #shift post bstack11l1l1llll1_opy_
  bstack1ll111111l_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭᪄") #shift post bstack11l1l1llll1_opy_
  bstack11l1lll1lll_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡩࡷࡥࠫ᪅") #shift
  bstack11l1ll11ll1_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡨࡴࡽ࡮࡭ࡱࡤࡨࠬ᪆") #shift
  bstack1l111llll1_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪ᪇")
  bstack1ll11l1l1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾ࡸࡧࡶࡦ࠯ࡵࡩࡸࡻ࡬ࡵࡵࠪ᪈")
  bstack1l1l1l1ll1_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡶࡥࡳࡨࡲࡶࡲࡹࡣࡢࡰࠪ᪉")
  bstack11lllll11l_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡰࡴࡩࡡ࡭ࠩ᪊") #shift
  bstack1111llll_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡣࡳࡴ࠲ࡻࡰ࡭ࡱࡤࡨࠬ᪋") #shift
  bstack1l11111ll1_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡩࡩ࠮ࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠫ᪌")
  bstack11l1l11l11_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡪࡩࡹ࠳ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠳ࡲࡦࡵࡸࡰࡹࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨ᪍") #shift
  bstack1l111l1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠭ࡳࡧࡶࡹࡱࡺࡳࠨ᪎") #shift
  bstack11l1lllllll_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽࠬ᪏") #shift
  bstack1l1l1l1ll11_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ᪐")
  bstack1lll11111_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡸࡺࡡࡵࡷࡶࠫ᪑") #shift
  bstack1l1llll1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾࡭ࡻࡢ࠮࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠬ᪒")
  bstack11l1lll1111_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷࡵࡸࡺ࠯ࡶࡩࡹࡻࡰࠨ᪓") #shift
  bstack1l1111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫ࡴࡶࡲࠪ᪔")
  bstack11ll111111l_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡴࡡࡱࡵ࡫ࡳࡹ࠭᪕") # not bstack11l1lll1l11_opy_ in python
  bstack11lll111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡱࡶ࡫ࡷࠫ᪖") # used in bstack11ll1111111_opy_
  bstack11ll1lll11_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡨࡧࡷࠫ᪗") # used in bstack11ll1111111_opy_
  bstack11l1lll11l_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡪࡲࡳࡰ࠭᪘")
  bstack11lllll1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠪ᪙")
  bstack1llll1l1ll_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠪ᪚") #
  bstack1l11l1111l_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡴ࠷࠱ࡺ࠼ࡧࡶ࡮ࡼࡥࡳ࠯ࡷࡥࡰ࡫ࡓࡤࡴࡨࡩࡳ࡙ࡨࡰࡶࠪ᪛")
  bstack1l11111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡦࡻࡴࡰ࠯ࡦࡥࡵࡺࡵࡳࡧࠪ᪜")
  bstack1l1l111lll_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡧ࠰ࡸࡪࡹࡴࠨ᪝")
  bstack111lll111_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡱࡶࡸ࠲ࡺࡥࡴࡶࠪ᪞")
  bstack1lll111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡵࡩ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᪟") #shift
  bstack111l1l1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡳࡸࡺ࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨ᪠") #shift
  bstack11l1ll1lll1_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࠮ࡥࡤࡴࡹࡻࡲࡦࠩ᪡")
  bstack11l1llll11l_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡩࡥ࡮ࡨ࠱ࡹ࡯࡭ࡦࡱࡸࡸࠬ᪢")
  bstack1lll11l1ll1_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡶࡸࡦࡸࡴࠨ᪣")
  bstack11l1ll1l11l_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡨࡴࡽ࡮࡭ࡱࡤࡨࠬ᪤")
  bstack11l1llll1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡨ࡮ࡥࡤ࡭࠰ࡹࡵࡪࡡࡵࡧࠪ᪥")
  bstack1ll1l1l1lll_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡤࡲࡳࡹࡹࡴࡳࡣࡳࠫ᪦")
  bstack1llll11llll_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡦࡳࡳࡴࡥࡤࡶࠪᪧ")
  bstack1ll1llll1ll_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡷࡹࡵࡰࠨ᪨")
  bstack1lll1lllll1_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭᪩")
  bstack1llll11l111_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩ᪪")
  bstack11l1l1lllll_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠪ᪫")
  bstack11l1l1lll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡨࡓ࡫ࡡࡳࡧࡶࡸࡍࡻࡢࠨ᪬")
  bstack1l11llll111_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡉ࡯࡫ࡷࠫ᪭")
  bstack1l11lll1ll1_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡶࡹ࠭᪮")
  bstack1ll1l11ll1l_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡆࡳࡳ࡬ࡩࡨࠩ᪯")
  bstack11l1ll1ll11_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪ᪰")
  bstack1ll1111l11l_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡩࡔࡧ࡯ࡪࡍ࡫ࡡ࡭ࡕࡷࡩࡵ࠭᪱")
  bstack1ll111111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡊࡩࡹࡘࡥࡴࡷ࡯ࡸࠬ᪲")
  bstack1l1ll111l11_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡅࡷࡧࡱࡸࠬ᪳")
  bstack1l1l1l1lll1_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠫ᪴")
  bstack1l1l1lll111_opy_ = bstack1l1l1ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡬ࡰࡩࡆࡶࡪࡧࡴࡦࡦࡈࡺࡪࡴࡴࠨ᪵")
  bstack11l1ll1llll_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡦࡰࡴࡹࡪࡻࡥࡕࡧࡶࡸࡊࡼࡥ࡯ࡶ᪶ࠪ")
  bstack1l11ll1ll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡴࡶ᪷ࠧ")
  bstack1lll1ll1l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࡮ࡔࡶࡲࡴ᪸ࠬ")
class STAGE(Enum):
  bstack11llll11l1_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ᪹")
  END = bstack1l1l1ll_opy_ (u"ࠪࡩࡳࡪ᪺ࠧ")
  bstack1l1ll11l1_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡸ࡯࡮ࡨ࡮ࡨࠫ᪻")
bstack1llll1lll_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬ᪼"): bstack1l1l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ᪽࠭"),
  bstack1l1l1ll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫ᪾"): bstack1l1l1ll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴᪿࠪ")
}
PLAYWRIGHT_HUB_URL = bstack1l1l1ll_opy_ (u"ࠤࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀᫀࠦ")
bstack1ll11ll111l_opy_ = 98
bstack1ll11l1ll1l_opy_ = 100
bstack1111l1ll1l_opy_ = {
  bstack1l1l1ll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࠩ᫁"): bstack1l1l1ll_opy_ (u"ࠫ࠲࠳ࡲࡦࡴࡸࡲࡸ࠭᫂"),
  bstack1l1l1ll_opy_ (u"ࠬࡪࡥ࡭ࡣࡼ᫃ࠫ"): bstack1l1l1ll_opy_ (u"࠭࠭࠮ࡴࡨࡶࡺࡴࡳ࠮ࡦࡨࡰࡦࡿ᫄ࠧ"),
  bstack1l1l1ll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠳ࡤࡦ࡮ࡤࡽࠬ᫅"): 0
}
bstack11l1ll11l11_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣ᫆")
bstack11ll1111l11_opy_ = bstack1l1l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡹࡵࡲ࡯ࡢࡦ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨ᫇")
bstack1l11l11111_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡘࡊ࡙ࡔࠡࡔࡈࡔࡔࡘࡔࡊࡐࡊࠤࡆࡔࡄࠡࡃࡑࡅࡑ࡟ࡔࡊࡅࡖࠦ᫈")