# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import os
import re
from enum import Enum
bstack1l1l1l1l11_opy_ = {
  bstack1l11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫឆ"): bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࠧជ"),
  bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧឈ"): bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡰ࡫ࡹࠨញ"),
  bstack1l11l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩដ"): bstack1l11l11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫឋ"),
  bstack1l11l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨឌ"): bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩឍ"),
  bstack1l11l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨណ"): bstack1l11l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࠬត"),
  bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨថ"): bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬទ"),
  bstack1l11l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬធ"): bstack1l11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ន"),
  bstack1l11l11_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨប"): bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧࠨផ"),
  bstack1l11l11_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩព"): bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡴࡱ࡯ࡩࠬភ"),
  bstack1l11l11_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫម"): bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫយ"),
  bstack1l11l11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬរ"): bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬល"),
  bstack1l11l11_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩវ"): bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡺ࡮ࡪࡥࡰࠩឝ"),
  bstack1l11l11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫឞ"): bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫស"),
  bstack1l11l11_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧហ"): bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧឡ"),
  bstack1l11l11_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧអ"): bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧឣ"),
  bstack1l11l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ឤ"): bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ឥ"),
  bstack1l11l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨឦ"): bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩឧ"),
  bstack1l11l11_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧឨ"): bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧឩ"),
  bstack1l11l11_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨឪ"): bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨឫ"),
  bstack1l11l11_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬឬ"): bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬឭ"),
  bstack1l11l11_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩឮ"): bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧࡱࡨࡐ࡫ࡹࡴࠩឯ"),
  bstack1l11l11_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫឰ"): bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵࡗࡢ࡫ࡷࠫឱ"),
  bstack1l11l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪឲ"): bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡵࠪឳ"),
  bstack1l11l11_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧ឴"): bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡧࡥࡤࡧ࡭࡫ࠧ឵"),
  bstack1l11l11_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩា"): bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩិ"),
  bstack1l11l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ី"): bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ឹ"),
  bstack1l11l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩឺ"): bstack1l11l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ុ"),
  bstack1l11l11_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫូ"): bstack1l11l11_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭ួ"),
  bstack1l11l11_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩើ"): bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪឿ"),
  bstack1l11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫៀ"): bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫេ"),
  bstack1l11l11_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧែ"): bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧៃ"),
  bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧោ"): bstack1l11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪៅ"),
  bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬំ"): bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬះ"),
  bstack1l11l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬៈ"): bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹ࡯ࡶࡴࡦࡩࠬ៉"),
  bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ៊"): bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ់"),
  bstack1l11l11_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫ៌"): bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫ៍"),
  bstack1l11l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧ៎"): bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧ៏"),
  bstack1l11l11_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪ័"): bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪ៑"),
  bstack1l11l11_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ្࠭"): bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭៓"),
  bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭។"): bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭៕"),
  bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ៖"): bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧៗ")
}
bstack11l1ll11l11_opy_ = [
  bstack1l11l11_opy_ (u"ࠧࡰࡵࠪ៘"),
  bstack1l11l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ៙"),
  bstack1l11l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ៚"),
  bstack1l11l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ៛"),
  bstack1l11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨៜ"),
  bstack1l11l11_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ៝"),
  bstack1l11l11_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭៞"),
]
bstack1l11ll11_opy_ = {
  bstack1l11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ៟"): [bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ០"), bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫ១")],
  bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭២"): bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ៣"),
  bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ៤"): bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩ៥"),
  bstack1l11l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ៦"): bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭៧"),
  bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ៨"): bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ៩"),
  bstack1l11l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ៪"): bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭៫"),
  bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ៬"): bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ៭"),
  bstack1l11l11_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ៮"): bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭៯"),
  bstack1l11l11_opy_ (u"ࠪࡥࡵࡶࠧ៰"): [bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖ࡟ࡊࡆࠪ៱"), bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࠨ៲")],
  bstack1l11l11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ៳"): bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡐࡔࡍࡌࡆࡘࡈࡐࠬ៴"),
  bstack1l11l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ៵"): bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ៶"),
  bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ៷"): bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡑࡅࡗࡊࡘࡖࡂࡄࡌࡐࡎ࡚࡙ࠨ៸"),
  bstack1l11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ៹"): bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡕࡓࡄࡒࡗࡈࡇࡌࡆࠩ៺")
}
bstack1llllll1l1_opy_ = {
  bstack1l11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ៻"): [bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ៼"), bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ៽")],
  bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭៾"): [bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡢ࡯ࡪࡿࠧ៿"), bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᠀")],
  bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᠁"): bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᠂"),
  bstack1l11l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᠃"): bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᠄"),
  bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᠅"): bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᠆"),
  bstack1l11l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ᠇"): [bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡰࡱࠩ᠈"), bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭᠉")],
  bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᠊"): bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ᠋"),
  bstack1l11l11_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧ᠌"): bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧ᠍"),
  bstack1l11l11_opy_ (u"ࠬࡧࡰࡱࠩ᠎"): bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱࠩ᠏"),
  bstack1l11l11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ᠐"): bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ᠑"),
  bstack1l11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᠒"): bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᠓")
}
bstack1l111lll11_opy_ = {
  bstack1l11l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ᠔"): bstack1l11l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᠕"),
  bstack1l11l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᠖"): [bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᠗"), bstack1l11l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᠘")],
  bstack1l11l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᠙"): bstack1l11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ᠚"),
  bstack1l11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ᠛"): bstack1l11l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ᠜"),
  bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ᠝"): [bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ᠞"), bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ᠟")],
  bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᠠ"): bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᠡ"),
  bstack1l11l11_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᠢ"): bstack1l11l11_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪᠣ"),
  bstack1l11l11_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᠤ"): [bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᠥ"), bstack1l11l11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᠦ")],
  bstack1l11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᠧ"): [bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫᠨ"), bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫᠩ")]
}
bstack11ll1l1l11_opy_ = [
  bstack1l11l11_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᠪ"),
  bstack1l11l11_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᠫ"),
  bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ᠬ"),
  bstack1l11l11_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨᠭ"),
  bstack1l11l11_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫᠮ"),
  bstack1l11l11_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨᠯ"),
  bstack1l11l11_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧᠰ"),
  bstack1l11l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᠱ"),
  bstack1l11l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᠲ"),
  bstack1l11l11_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᠳ"),
  bstack1l11l11_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᠴ"),
  bstack1l11l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᠵ"),
]
bstack1llll11l1l_opy_ = [
  bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᠶ"),
  bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᠷ"),
  bstack1l11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᠸ"),
  bstack1l11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᠹ"),
  bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᠺ"),
  bstack1l11l11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᠻ"),
  bstack1l11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᠼ"),
  bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᠽ"),
  bstack1l11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᠾ"),
  bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᠿ"),
  bstack1l11l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᡀ"),
  bstack1l11l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩᡁ"),
  bstack1l11l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡕࡣࡪࠫᡂ"),
  bstack1l11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᡃ"),
  bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᡄ"),
  bstack1l11l11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᡅ"),
  bstack1l11l11_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠴ࠫᡆ"),
  bstack1l11l11_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠶ࠬᡇ"),
  bstack1l11l11_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠸࠭ᡈ"),
  bstack1l11l11_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠺ࠧᡉ"),
  bstack1l11l11_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠵ࠨᡊ"),
  bstack1l11l11_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠷ࠩᡋ"),
  bstack1l11l11_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠹ࠪᡌ"),
  bstack1l11l11_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠻ࠫᡍ"),
  bstack1l11l11_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠽ࠬᡎ"),
  bstack1l11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᡏ"),
  bstack1l11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᡐ"),
  bstack1l11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᡑ"),
  bstack1l11l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᡒ"),
  bstack1l11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᡓ"),
  bstack1l11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᡔ"),
  bstack1l11l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᡕ")
]
bstack11l1ll1llll_opy_ = [
  bstack1l11l11_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬᡖ"),
  bstack1l11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᡗ"),
  bstack1l11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᡘ"),
  bstack1l11l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᡙ"),
  bstack1l11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡒࡵ࡭ࡴࡸࡩࡵࡻࠪᡚ"),
  bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᡛ"),
  bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡧࡧࠨᡜ"),
  bstack1l11l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᡝ"),
  bstack1l11l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᡞ"),
  bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᡟ"),
  bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᡠ"),
  bstack1l11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪᡡ"),
  bstack1l11l11_opy_ (u"ࠬࡵࡳࠨᡢ"),
  bstack1l11l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᡣ"),
  bstack1l11l11_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ᡤ"),
  bstack1l11l11_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪᡥ"),
  bstack1l11l11_opy_ (u"ࠩࡵࡩ࡬࡯࡯࡯ࠩᡦ"),
  bstack1l11l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬᡧ"),
  bstack1l11l11_opy_ (u"ࠫࡲࡧࡣࡩ࡫ࡱࡩࠬᡨ"),
  bstack1l11l11_opy_ (u"ࠬࡸࡥࡴࡱ࡯ࡹࡹ࡯࡯࡯ࠩᡩ"),
  bstack1l11l11_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᡪ"),
  bstack1l11l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫᡫ"),
  bstack1l11l11_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧᡬ"),
  bstack1l11l11_opy_ (u"ࠩࡱࡳࡕࡧࡧࡦࡎࡲࡥࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᡭ"),
  bstack1l11l11_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫᡮ"),
  bstack1l11l11_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᡯ"),
  bstack1l11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᡰ"),
  bstack1l11l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧᡱ"),
  bstack1l11l11_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫᡲ"),
  bstack1l11l11_opy_ (u"ࠨࡰࡲࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠬᡳ"),
  bstack1l11l11_opy_ (u"ࠩࡦ࡬ࡪࡩ࡫ࡖࡔࡏࠫᡴ"),
  bstack1l11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᡵ"),
  bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡇࡴࡵ࡫ࡪࡧࡶࠫᡶ"),
  bstack1l11l11_opy_ (u"ࠬࡩࡡࡱࡶࡸࡶࡪࡉࡲࡢࡵ࡫ࠫᡷ"),
  bstack1l11l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᡸ"),
  bstack1l11l11_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᡹"),
  bstack1l11l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᡺"),
  bstack1l11l11_opy_ (u"ࠩࡱࡳࡇࡲࡡ࡯࡭ࡓࡳࡱࡲࡩ࡯ࡩࠪ᡻"),
  bstack1l11l11_opy_ (u"ࠪࡱࡦࡹ࡫ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩ᡼"),
  bstack1l11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡐࡴ࡭ࡳࠨ᡽"),
  bstack1l11l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡎࡪࠧ᡾"),
  bstack1l11l11_opy_ (u"࠭ࡤࡦࡦ࡬ࡧࡦࡺࡥࡥࡆࡨࡺ࡮ࡩࡥࠨ᡿"),
  bstack1l11l11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡐࡢࡴࡤࡱࡸ࠭ᢀ"),
  bstack1l11l11_opy_ (u"ࠨࡲ࡫ࡳࡳ࡫ࡎࡶ࡯ࡥࡩࡷ࠭ᢁ"),
  bstack1l11l11_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᢂ"),
  bstack1l11l11_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡐࡲࡷ࡭ࡴࡴࡳࠨᢃ"),
  bstack1l11l11_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩᢄ"),
  bstack1l11l11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᢅ"),
  bstack1l11l11_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪᢆ"),
  bstack1l11l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡂࡪࡱࡰࡩࡹࡸࡩࡤࠩᢇ"),
  bstack1l11l11_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࡖ࠳ࠩᢈ"),
  bstack1l11l11_opy_ (u"ࠩࡰ࡭ࡩ࡙ࡥࡴࡵ࡬ࡳࡳࡏ࡮ࡴࡶࡤࡰࡱࡇࡰࡱࡵࠪᢉ"),
  bstack1l11l11_opy_ (u"ࠪࡩࡸࡶࡲࡦࡵࡶࡳࡘ࡫ࡲࡷࡧࡵࠫᢊ"),
  bstack1l11l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪᢋ"),
  bstack1l11l11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡃࡥࡲࠪᢌ"),
  bstack1l11l11_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ᢍ"),
  bstack1l11l11_opy_ (u"ࠧࡴࡻࡱࡧ࡙࡯࡭ࡦ࡙࡬ࡸ࡭ࡔࡔࡑࠩᢎ"),
  bstack1l11l11_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᢏ"),
  bstack1l11l11_opy_ (u"ࠩࡪࡴࡸࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧᢐ"),
  bstack1l11l11_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫᢑ"),
  bstack1l11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫᢒ"),
  bstack1l11l11_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡇ࡭ࡧ࡮ࡨࡧࡍࡥࡷ࠭ᢓ"),
  bstack1l11l11_opy_ (u"࠭ࡸ࡮ࡵࡍࡥࡷ࠭ᢔ"),
  bstack1l11l11_opy_ (u"ࠧࡹ࡯ࡻࡎࡦࡸࠧᢕ"),
  bstack1l11l11_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧᢖ"),
  bstack1l11l11_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩᢗ"),
  bstack1l11l11_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫᢘ"),
  bstack1l11l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧᢙ"),
  bstack1l11l11_opy_ (u"ࠬࡧࡰࡱࡘࡨࡶࡸ࡯࡯࡯ࠩᢚ"),
  bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᢛ"),
  bstack1l11l11_opy_ (u"ࠧࡳࡧࡶ࡭࡬ࡴࡁࡱࡲࠪᢜ"),
  bstack1l11l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࡷࠬᢝ"),
  bstack1l11l11_opy_ (u"ࠩࡦࡥࡳࡧࡲࡺࠩᢞ"),
  bstack1l11l11_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫᢟ"),
  bstack1l11l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᢠ"),
  bstack1l11l11_opy_ (u"ࠬ࡯ࡥࠨᢡ"),
  bstack1l11l11_opy_ (u"࠭ࡥࡥࡩࡨࠫᢢ"),
  bstack1l11l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᢣ"),
  bstack1l11l11_opy_ (u"ࠨࡳࡸࡩࡺ࡫ࠧᢤ"),
  bstack1l11l11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫᢥ"),
  bstack1l11l11_opy_ (u"ࠪࡥࡵࡶࡓࡵࡱࡵࡩࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠫᢦ"),
  bstack1l11l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡇࡦࡳࡥࡳࡣࡌࡱࡦ࡭ࡥࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪᢧ"),
  bstack1l11l11_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡈࡼࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨᢨ"),
  bstack1l11l11_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡍࡳࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴᢩࠩ"),
  bstack1l11l11_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᢪ"),
  bstack1l11l11_opy_ (u"ࠨࡴࡨࡷࡪࡸࡶࡦࡆࡨࡺ࡮ࡩࡥࠨ᢫"),
  bstack1l11l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ᢬"),
  bstack1l11l11_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬ᢭"),
  bstack1l11l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡦࡹࡳࡤࡱࡧࡩࠬ᢮"),
  bstack1l11l11_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡎࡵࡳࡅࡧࡹ࡭ࡨ࡫ࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨ᢯"),
  bstack1l11l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡵࡥ࡫ࡲࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭ᢰ"),
  bstack1l11l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡱࡲ࡯ࡩࡕࡧࡹࠨᢱ"),
  bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᢲ"),
  bstack1l11l11_opy_ (u"ࠩࡺࡨ࡮ࡵࡓࡦࡴࡹ࡭ࡨ࡫ࠧᢳ"),
  bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᢴ"),
  bstack1l11l11_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸࡈࡸ࡯ࡴࡵࡖ࡭ࡹ࡫ࡔࡳࡣࡦ࡯࡮ࡴࡧࠨᢵ"),
  bstack1l11l11_opy_ (u"ࠬ࡮ࡩࡨࡪࡆࡳࡳࡺࡲࡢࡵࡷࠫᢶ"),
  bstack1l11l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡖࡲࡦࡨࡨࡶࡪࡴࡣࡦࡵࠪᢷ"),
  bstack1l11l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᢸ"),
  bstack1l11l11_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬᢹ"),
  bstack1l11l11_opy_ (u"ࠩࡵࡩࡲࡵࡶࡦࡋࡒࡗࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࡎࡲࡧࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧᢺ"),
  bstack1l11l11_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬᢻ"),
  bstack1l11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᢼ"),
  bstack1l11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧᢽ"),
  bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᢾ"),
  bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᢿ"),
  bstack1l11l11_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫᣀ"),
  bstack1l11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨᣁ"),
  bstack1l11l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬᣂ"),
  bstack1l11l11_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧᣃ")
]
bstack111ll1111_opy_ = {
  bstack1l11l11_opy_ (u"ࠬࡼࠧᣄ"): bstack1l11l11_opy_ (u"࠭ࡶࠨᣅ"),
  bstack1l11l11_opy_ (u"ࠧࡧࠩᣆ"): bstack1l11l11_opy_ (u"ࠨࡨࠪᣇ"),
  bstack1l11l11_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨᣈ"): bstack1l11l11_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩᣉ"),
  bstack1l11l11_opy_ (u"ࠫࡴࡴ࡬ࡺࡣࡸࡸࡴࡳࡡࡵࡧࠪᣊ"): bstack1l11l11_opy_ (u"ࠬࡵ࡮࡭ࡻࡄࡹࡹࡵ࡭ࡢࡶࡨࠫᣋ"),
  bstack1l11l11_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪᣌ"): bstack1l11l11_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫᣍ"),
  bstack1l11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫᣎ"): bstack1l11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬᣏ"),
  bstack1l11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ᣐ"): bstack1l11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᣑ"),
  bstack1l11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᣒ"): bstack1l11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᣓ"),
  bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᣔ"): bstack1l11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫᣕ"),
  bstack1l11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪᣖ"): bstack1l11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡈࡰࡵࡷࠫᣗ"),
  bstack1l11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬᣘ"): bstack1l11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᣙ"),
  bstack1l11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧᣚ"): bstack1l11l11_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᣛ"),
  bstack1l11l11_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᣜ"): bstack1l11l11_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫᣝ"),
  bstack1l11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᣞ"): bstack1l11l11_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᣟ"),
  bstack1l11l11_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᣠ"): bstack1l11l11_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨᣡ"),
  bstack1l11l11_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫᣢ"): bstack1l11l11_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬᣣ"),
  bstack1l11l11_opy_ (u"ࠩࡳࡥࡨ࡬ࡩ࡭ࡧࠪᣤ"): bstack1l11l11_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᣥ"),
  bstack1l11l11_opy_ (u"ࠫࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᣦ"): bstack1l11l11_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᣧ"),
  bstack1l11l11_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᣨ"): bstack1l11l11_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᣩ"),
  bstack1l11l11_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩᣪ"): bstack1l11l11_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪᣫ"),
  bstack1l11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᣬ"): bstack1l11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᣭ"),
  bstack1l11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࠲ࡸࡥࡱࡧࡤࡸࡪࡸࠧᣮ"): bstack1l11l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡱࡧࡤࡸࡪࡸࠧᣯ")
}
bstack11l1ll1l1l1_opy_ = bstack1l11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩ࡬ࡸ࡭ࡻࡢ࠯ࡥࡲࡱ࠴ࡶࡥࡳࡥࡼ࠳ࡨࡲࡩ࠰ࡴࡨࡰࡪࡧࡳࡦࡵ࠲ࡰࡦࡺࡥࡴࡶ࠲ࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᣰ")
bstack11l1llll111_opy_ = bstack1l11l11_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠰ࡪࡨࡥࡱࡺࡨࡤࡪࡨࡧࡰࠨᣱ")
bstack111l111l_opy_ = bstack1l11l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡩࡩࡹ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡷࡪࡴࡤࡠࡵࡧ࡯ࡤ࡫ࡶࡦࡰࡷࡷࠧᣲ")
bstack1l111111ll_opy_ = bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡼࡪ࠯ࡩࡷࡥࠫᣳ")
bstack1llll1llll_opy_ = bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠧᣴ")
bstack1111lll1l_opy_ = bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠩᣵ")
bstack11l1llll11l_opy_ = {
  bstack1l11l11_opy_ (u"࠭ࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠨ᣶"): 50,
  bstack1l11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᣷"): 40,
  bstack1l11l11_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩ᣸"): 30,
  bstack1l11l11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ᣹"): 20,
  bstack1l11l11_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩ᣺"): 10
}
bstack1ll1lll1_opy_ = bstack11l1llll11l_opy_[bstack1l11l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ᣻")]
bstack1l1l1111ll_opy_ = bstack1l11l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫ᣼")
bstack1l11ll1l_opy_ = bstack1l11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫ᣽")
bstack1l1l11ll_opy_ = bstack1l11l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭᣾")
bstack11lll11ll_opy_ = bstack1l11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧ᣿")
bstack11lll1ll_opy_ = bstack1l11l11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡥࡳࡪࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡳࡥࡨࡱࡡࡨࡧࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧᤀ")
bstack11l1lll1111_opy_ = [bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᤁ"), bstack1l11l11_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᤂ")]
bstack11l1llll1l1_opy_ = [bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᤃ"), bstack1l11l11_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᤄ")]
bstack1l1111l1l1_opy_ = re.compile(bstack1l11l11_opy_ (u"ࠧ࡟࡝࡟ࡠࡼ࠳࡝ࠬ࠼࠱࠮ࠩ࠭ᤅ"))
bstack1ll1l11lll_opy_ = [
  bstack1l11l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡓࡧ࡭ࡦࠩᤆ"),
  bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᤇ"),
  bstack1l11l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᤈ"),
  bstack1l11l11_opy_ (u"ࠫࡳ࡫ࡷࡄࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࠨᤉ"),
  bstack1l11l11_opy_ (u"ࠬࡧࡰࡱࠩᤊ"),
  bstack1l11l11_opy_ (u"࠭ࡵࡥ࡫ࡧࠫᤋ"),
  bstack1l11l11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᤌ"),
  bstack1l11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࠨᤍ"),
  bstack1l11l11_opy_ (u"ࠩࡲࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧᤎ"),
  bstack1l11l11_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࠨᤏ"),
  bstack1l11l11_opy_ (u"ࠫࡳࡵࡒࡦࡵࡨࡸࠬᤐ"), bstack1l11l11_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡕࡩࡸ࡫ࡴࠨᤑ"),
  bstack1l11l11_opy_ (u"࠭ࡣ࡭ࡧࡤࡶࡘࡿࡳࡵࡧࡰࡊ࡮ࡲࡥࡴࠩᤒ"),
  bstack1l11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹ࡚ࡩ࡮࡫ࡱ࡫ࡸ࠭ᤓ"),
  bstack1l11l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࡑࡵࡧࡨ࡫ࡱ࡫ࠬᤔ"),
  bstack1l11l11_opy_ (u"ࠩࡲࡸ࡭࡫ࡲࡂࡲࡳࡷࠬᤕ"),
  bstack1l11l11_opy_ (u"ࠪࡴࡷ࡯࡮ࡵࡒࡤ࡫ࡪ࡙࡯ࡶࡴࡦࡩࡔࡴࡆࡪࡰࡧࡊࡦ࡯࡬ࡶࡴࡨࠫᤖ"),
  bstack1l11l11_opy_ (u"ࠫࡦࡶࡰࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩᤗ"), bstack1l11l11_opy_ (u"ࠬࡧࡰࡱࡒࡤࡧࡰࡧࡧࡦࠩᤘ"), bstack1l11l11_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨᤙ"), bstack1l11l11_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡑࡣࡦ࡯ࡦ࡭ࡥࠨᤚ"), bstack1l11l11_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡆࡸࡶࡦࡺࡩࡰࡰࠪᤛ"),
  bstack1l11l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧᤜ"),
  bstack1l11l11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡨࡷࡹࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧᤝ"),
  bstack1l11l11_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪ࠭ᤞ"), bstack1l11l11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࡅ࡯ࡦࡌࡲࡹ࡫࡮ࡵࠩ᤟"),
  bstack1l11l11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫᤠ"),
  bstack1l11l11_opy_ (u"ࠧࡢࡦࡥࡔࡴࡸࡴࠨᤡ"),
  bstack1l11l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡔࡱࡦ࡯ࡪࡺࠧᤢ"),
  bstack1l11l11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡗ࡭ࡲ࡫࡯ࡶࡶࠪᤣ"),
  bstack1l11l11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡺࡨࠨᤤ"),
  bstack1l11l11_opy_ (u"ࠫࡦࡼࡤࠨᤥ"), bstack1l11l11_opy_ (u"ࠬࡧࡶࡥࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᤦ"), bstack1l11l11_opy_ (u"࠭ࡡࡷࡦࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨᤧ"), bstack1l11l11_opy_ (u"ࠧࡢࡸࡧࡅࡷ࡭ࡳࠨᤨ"),
  bstack1l11l11_opy_ (u"ࠨࡷࡶࡩࡐ࡫ࡹࡴࡶࡲࡶࡪ࠭ᤩ"), bstack1l11l11_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡺࡨࠨᤪ"), bstack1l11l11_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡳࡴࡹࡲࡶࡩ࠭ᤫ"),
  bstack1l11l11_opy_ (u"ࠫࡰ࡫ࡹࡂ࡮࡬ࡥࡸ࠭᤬"), bstack1l11l11_opy_ (u"ࠬࡱࡥࡺࡒࡤࡷࡸࡽ࡯ࡳࡦࠪ᤭"),
  bstack1l11l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨ᤮"), bstack1l11l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡇࡲࡨࡵࠪ᤯"), bstack1l11l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࡇ࡭ࡷ࠭ᤰ"), bstack1l11l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡄࡪࡵࡳࡲ࡫ࡍࡢࡲࡳ࡭ࡳ࡭ࡆࡪ࡮ࡨࠫᤱ"), bstack1l11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡗࡶࡩࡘࡿࡳࡵࡧࡰࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧᤲ"),
  bstack1l11l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࠧᤳ"), bstack1l11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࡴࠩᤴ"),
  bstack1l11l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡉ࡯ࡳࡢࡤ࡯ࡩࡇࡻࡩ࡭ࡦࡆ࡬ࡪࡩ࡫ࠨᤵ"),
  bstack1l11l11_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻ࡙࡯࡭ࡦࡱࡸࡸࠬᤶ"),
  bstack1l11l11_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡂࡥࡷ࡭ࡴࡴࠧᤷ"), bstack1l11l11_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡅࡤࡸࡪ࡭࡯ࡳࡻࠪᤸ"), bstack1l11l11_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡉࡰࡦ࡭ࡳࠨ᤹"), bstack1l11l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡥࡱࡏ࡮ࡵࡧࡱࡸࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ᤺"),
  bstack1l11l11_opy_ (u"ࠬࡪ࡯࡯ࡶࡖࡸࡴࡶࡁࡱࡲࡒࡲࡗ࡫ࡳࡦࡶ᤻ࠪ"),
  bstack1l11l11_opy_ (u"࠭ࡵ࡯࡫ࡦࡳࡩ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨ᤼"), bstack1l11l11_opy_ (u"ࠧࡳࡧࡶࡩࡹࡑࡥࡺࡤࡲࡥࡷࡪࠧ᤽"),
  bstack1l11l11_opy_ (u"ࠨࡰࡲࡗ࡮࡭࡮ࠨ᤾"),
  bstack1l11l11_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡗࡱ࡭ࡲࡶ࡯ࡳࡶࡤࡲࡹ࡜ࡩࡦࡹࡶࠫ᤿"),
  bstack1l11l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳࡪࡲࡰ࡫ࡧ࡛ࡦࡺࡣࡩࡧࡵࡷࠬ᥀"),
  bstack1l11l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᥁"),
  bstack1l11l11_opy_ (u"ࠬࡸࡥࡤࡴࡨࡥࡹ࡫ࡃࡩࡴࡲࡱࡪࡊࡲࡪࡸࡨࡶࡘ࡫ࡳࡴ࡫ࡲࡲࡸ࠭᥂"),
  bstack1l11l11_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ᥃"),
  bstack1l11l11_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡔࡦࡺࡨࠨ᥄"),
  bstack1l11l11_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡕࡳࡩࡪࡪࠧ᥅"),
  bstack1l11l11_opy_ (u"ࠩࡪࡴࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭᥆"),
  bstack1l11l11_opy_ (u"ࠪ࡭ࡸࡎࡥࡢࡦ࡯ࡩࡸࡹࠧ᥇"),
  bstack1l11l11_opy_ (u"ࠫࡦࡪࡢࡆࡺࡨࡧ࡙࡯࡭ࡦࡱࡸࡸࠬ᥈"),
  bstack1l11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࡘࡩࡲࡪࡲࡷࠫ᥉"),
  bstack1l11l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡈࡪࡼࡩࡤࡧࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪ᥊"),
  bstack1l11l11_opy_ (u"ࠧࡢࡷࡷࡳࡌࡸࡡ࡯ࡶࡓࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠧ᥋"),
  bstack1l11l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡐࡤࡸࡺࡸࡡ࡭ࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭᥌"),
  bstack1l11l11_opy_ (u"ࠩࡶࡽࡸࡺࡥ࡮ࡒࡲࡶࡹ࠭᥍"),
  bstack1l11l11_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡨࡧࡎ࡯ࡴࡶࠪ᥎"),
  bstack1l11l11_opy_ (u"ࠫࡸࡱࡩࡱࡗࡱࡰࡴࡩ࡫ࠨ᥏"), bstack1l11l11_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯࡙ࡿࡰࡦࠩᥐ"), bstack1l11l11_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰࡑࡥࡺࠩᥑ"),
  bstack1l11l11_opy_ (u"ࠧࡢࡷࡷࡳࡑࡧࡵ࡯ࡥ࡫ࠫᥒ"),
  bstack1l11l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡥࡤࡸࡈࡧࡰࡵࡷࡵࡩࠬᥓ"),
  bstack1l11l11_opy_ (u"ࠩࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࡔࡺࡨࡦࡴࡓࡥࡨࡱࡡࡨࡧࡶࠫᥔ"),
  bstack1l11l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨ࡛࡮ࡴࡤࡰࡹࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࠬᥕ"),
  bstack1l11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡳࡴࡲࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᥖ"),
  bstack1l11l11_opy_ (u"ࠬ࡫࡮ࡧࡱࡵࡧࡪࡇࡰࡱࡋࡱࡷࡹࡧ࡬࡭ࠩᥗ"),
  bstack1l11l11_opy_ (u"࠭ࡥ࡯ࡵࡸࡶࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡹࡈࡢࡸࡨࡔࡦ࡭ࡥࡴࠩᥘ"), bstack1l11l11_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡅࡧࡹࡸࡴࡵ࡬ࡴࡒࡲࡶࡹ࠭ᥙ"), bstack1l11l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡘࡧࡥࡺ࡮࡫ࡷࡅࡧࡷࡥ࡮ࡲࡳࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠫᥚ"),
  bstack1l11l11_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡳࡴࡸࡉࡡࡤࡪࡨࡐ࡮ࡳࡩࡵࠩᥛ"),
  bstack1l11l11_opy_ (u"ࠪࡧࡦࡲࡥ࡯ࡦࡤࡶࡋࡵࡲ࡮ࡣࡷࠫᥜ"),
  bstack1l11l11_opy_ (u"ࠫࡧࡻ࡮ࡥ࡮ࡨࡍࡩ࠭ᥝ"),
  bstack1l11l11_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬᥞ"),
  bstack1l11l11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡇࡱࡥࡧࡲࡥࡥࠩᥟ"), bstack1l11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡩࡩ࠭ᥠ"),
  bstack1l11l11_opy_ (u"ࠨࡣࡸࡸࡴࡇࡣࡤࡧࡳࡸࡆࡲࡥࡳࡶࡶࠫᥡ"), bstack1l11l11_opy_ (u"ࠩࡤࡹࡹࡵࡄࡪࡵࡰ࡭ࡸࡹࡁ࡭ࡧࡵࡸࡸ࠭ᥢ"),
  bstack1l11l11_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡹࡌࡪࡤࠪᥣ"),
  bstack1l11l11_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡔࡢࡲࠪᥤ"),
  bstack1l11l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎࡴࡩࡵ࡫ࡤࡰ࡚ࡸ࡬ࠨᥥ"), bstack1l11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡇ࡬࡭ࡱࡺࡔࡴࡶࡵࡱࡵࠪᥦ"), bstack1l11l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉࡨࡰࡲࡶࡪࡌࡲࡢࡷࡧ࡛ࡦࡸ࡮ࡪࡰࡪࠫᥧ"), bstack1l11l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡨࡲࡑ࡯࡮࡬ࡵࡌࡲࡇࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠨᥨ"),
  bstack1l11l11_opy_ (u"ࠩ࡮ࡩࡪࡶࡋࡦࡻࡆ࡬ࡦ࡯࡮ࡴࠩᥩ"),
  bstack1l11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡽࡥࡧࡲࡥࡔࡶࡵ࡭ࡳ࡭ࡳࡅ࡫ࡵࠫᥪ"),
  bstack1l11l11_opy_ (u"ࠫࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᥫ"),
  bstack1l11l11_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡏࡪࡿࡄࡦ࡮ࡤࡽࠬᥬ"),
  bstack1l11l11_opy_ (u"࠭ࡳࡩࡱࡺࡍࡔ࡙ࡌࡰࡩࠪᥭ"),
  bstack1l11l11_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡔࡶࡵࡥࡹ࡫ࡧࡺࠩ᥮"),
  bstack1l11l11_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡓࡧࡶࡴࡴࡴࡳࡦࡖ࡬ࡱࡪࡵࡵࡵࠩ᥯"), bstack1l11l11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࡝ࡡࡪࡶࡗ࡭ࡲ࡫࡯ࡶࡶࠪᥰ"),
  bstack1l11l11_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾ࠭ᥱ"),
  bstack1l11l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡸࡿ࡮ࡤࡇࡻࡩࡨࡻࡴࡦࡈࡵࡳࡲࡎࡴࡵࡲࡶࠫᥲ"),
  bstack1l11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡉࡡࡱࡶࡸࡶࡪ࠭ᥳ"),
  bstack1l11l11_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᥴ"),
  bstack1l11l11_opy_ (u"ࠧࡧࡷ࡯ࡰࡈࡵ࡮ࡵࡧࡻࡸࡑ࡯ࡳࡵࠩ᥵"),
  bstack1l11l11_opy_ (u"ࠨࡹࡤ࡭ࡹࡌ࡯ࡳࡃࡳࡴࡘࡩࡲࡪࡲࡷࠫ᥶"),
  bstack1l11l11_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡆࡳࡳࡴࡥࡤࡶࡕࡩࡹࡸࡩࡦࡵࠪ᥷"),
  bstack1l11l11_opy_ (u"ࠪࡥࡵࡶࡎࡢ࡯ࡨࠫ᥸"),
  bstack1l11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡘࡒࡃࡦࡴࡷࠫ᥹"),
  bstack1l11l11_opy_ (u"ࠬࡺࡡࡱ࡙࡬ࡸ࡭࡙ࡨࡰࡴࡷࡔࡷ࡫ࡳࡴࡆࡸࡶࡦࡺࡩࡰࡰࠪ᥺"),
  bstack1l11l11_opy_ (u"࠭ࡳࡤࡣ࡯ࡩࡋࡧࡣࡵࡱࡵࠫ᥻"),
  bstack1l11l11_opy_ (u"ࠧࡸࡦࡤࡐࡴࡩࡡ࡭ࡒࡲࡶࡹ࠭᥼"),
  bstack1l11l11_opy_ (u"ࠨࡵ࡫ࡳࡼ࡞ࡣࡰࡦࡨࡐࡴ࡭ࠧ᥽"),
  bstack1l11l11_opy_ (u"ࠩ࡬ࡳࡸࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡶࡵࡨࠫ᥾"),
  bstack1l11l11_opy_ (u"ࠪࡼࡨࡵࡤࡦࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠬ᥿"),
  bstack1l11l11_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡴࡵࡺࡳࡷࡪࠧᦀ"),
  bstack1l11l11_opy_ (u"ࠬࡻࡳࡦࡒࡵࡩࡧࡻࡩ࡭ࡶ࡚ࡈࡆ࠭ᦁ"),
  bstack1l11l11_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡗࡅࡃࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧᦂ"),
  bstack1l11l11_opy_ (u"ࠧࡸࡧࡥࡈࡷ࡯ࡶࡦࡴࡄ࡫ࡪࡴࡴࡖࡴ࡯ࠫᦃ"),
  bstack1l11l11_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡹ࡮ࠧᦄ"),
  bstack1l11l11_opy_ (u"ࠩࡸࡷࡪࡔࡥࡸ࡙ࡇࡅࠬᦅ"),
  bstack1l11l11_opy_ (u"ࠪࡻࡩࡧࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᦆ"), bstack1l11l11_opy_ (u"ࠫࡼࡪࡡࡄࡱࡱࡲࡪࡩࡴࡪࡱࡱࡘ࡮ࡳࡥࡰࡷࡷࠫᦇ"),
  bstack1l11l11_opy_ (u"ࠬࡾࡣࡰࡦࡨࡓࡷ࡭ࡉࡥࠩᦈ"), bstack1l11l11_opy_ (u"࠭ࡸࡤࡱࡧࡩࡘ࡯ࡧ࡯࡫ࡱ࡫ࡎࡪࠧᦉ"),
  bstack1l11l11_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡘࡆࡄࡆࡺࡴࡤ࡭ࡧࡌࡨࠬᦊ"),
  bstack1l11l11_opy_ (u"ࠨࡴࡨࡷࡪࡺࡏ࡯ࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡷࡺࡏ࡯࡮ࡼࠫᦋ"),
  bstack1l11l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࡶࠫᦌ"),
  bstack1l11l11_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵ࡭ࡪࡹࠧᦍ"), bstack1l11l11_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶࡾࡏ࡮ࡵࡧࡵࡺࡦࡲࠧᦎ"),
  bstack1l11l11_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹࡎࡡࡳࡦࡺࡥࡷ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨᦏ"),
  bstack1l11l11_opy_ (u"࠭࡭ࡢࡺࡗࡽࡵ࡯࡮ࡨࡈࡵࡩࡶࡻࡥ࡯ࡥࡼࠫᦐ"),
  bstack1l11l11_opy_ (u"ࠧࡴ࡫ࡰࡴࡱ࡫ࡉࡴࡘ࡬ࡷ࡮ࡨ࡬ࡦࡅ࡫ࡩࡨࡱࠧᦑ"),
  bstack1l11l11_opy_ (u"ࠨࡷࡶࡩࡈࡧࡲࡵࡪࡤ࡫ࡪ࡙ࡳ࡭ࠩᦒ"),
  bstack1l11l11_opy_ (u"ࠩࡶ࡬ࡴࡻ࡬ࡥࡗࡶࡩࡘ࡯࡮ࡨ࡮ࡨࡸࡴࡴࡔࡦࡵࡷࡑࡦࡴࡡࡨࡧࡵࠫᦓ"),
  bstack1l11l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡋ࡚ࡈࡕ࠭ᦔ"),
  bstack1l11l11_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡳࡺࡩࡨࡊࡦࡈࡲࡷࡵ࡬࡭ࠩᦕ"),
  bstack1l11l11_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࡍ࡯ࡤࡥࡧࡱࡅࡵ࡯ࡐࡰ࡮࡬ࡧࡾࡋࡲࡳࡱࡵࠫᦖ"),
  bstack1l11l11_opy_ (u"࠭࡭ࡰࡥ࡮ࡐࡴࡩࡡࡵ࡫ࡲࡲࡆࡶࡰࠨᦗ"),
  bstack1l11l11_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡰࡴࡰࡥࡹ࠭ᦘ"), bstack1l11l11_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇ࡫࡯ࡸࡪࡸࡓࡱࡧࡦࡷࠬᦙ"),
  bstack1l11l11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡅࡧ࡯ࡥࡾࡇࡤࡣࠩᦚ"),
  bstack1l11l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡍࡩࡒ࡯ࡤࡣࡷࡳࡷࡇࡵࡵࡱࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳ࠭ᦛ")
]
bstack1l11ll11ll_opy_ = bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪᦜ")
bstack111111lll_opy_ = [bstack1l11l11_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪᦝ"), bstack1l11l11_opy_ (u"࠭࠮ࡢࡣࡥࠫᦞ"), bstack1l11l11_opy_ (u"ࠧ࠯࡫ࡳࡥࠬᦟ")]
bstack11ll1l11_opy_ = [bstack1l11l11_opy_ (u"ࠨ࡫ࡧࠫᦠ"), bstack1l11l11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᦡ"), bstack1l11l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ᦢ"), bstack1l11l11_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪᦣ")]
bstack11ll11ll11_opy_ = {
  bstack1l11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᦤ"): bstack1l11l11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᦥ"),
  bstack1l11l11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᦦ"): bstack1l11l11_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦧ"),
  bstack1l11l11_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᦨ"): bstack1l11l11_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᦩ"),
  bstack1l11l11_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᦪ"): bstack1l11l11_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫᦫ"),
  bstack1l11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭᦬"): bstack1l11l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ᦭")
}
bstack1lllll11l_opy_ = [
  bstack1l11l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᦮"),
  bstack1l11l11_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ᦯"),
  bstack1l11l11_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᦰ"),
  bstack1l11l11_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᦱ"),
  bstack1l11l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᦲ"),
]
bstack11l111l111_opy_ = bstack1llll11l1l_opy_ + bstack11l1ll1llll_opy_ + bstack1ll1l11lll_opy_
bstack11l11111_opy_ = [
  bstack1l11l11_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫᦳ"),
  bstack1l11l11_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨᦴ"),
  bstack1l11l11_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧᦵ"),
  bstack1l11l11_opy_ (u"ࠩࡡ࠵࠵࠴ࠧᦶ"),
  bstack1l11l11_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩᦷ"),
  bstack1l11l11_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪᦸ"),
  bstack1l11l11_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫᦹ"),
  bstack1l11l11_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩᦺ")
]
bstack11ll11l1l11_opy_ = bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᦻ")
bstack11ll1l11l1_opy_ = bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧᦼ")
bstack1l1lll1111_opy_ = [ bstack1l11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᦽ") ]
bstack1lll11ll1_opy_ = [ bstack1l11l11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩᦾ") ]
bstack1ll111111l_opy_ = [bstack1l11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᦿ")]
bstack1lll1111l_opy_ = [ bstack1l11l11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᧀ") ]
bstack1ll11l1l11_opy_ = bstack1l11l11_opy_ (u"࠭ࡓࡅࡍࡖࡩࡹࡻࡰࠨᧁ")
bstack1l1111llll_opy_ = bstack1l11l11_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪᧂ")
bstack1111ll11_opy_ = bstack1l11l11_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠬᧃ")
bstack111111l1l_opy_ = bstack1l11l11_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࠨᧄ")
bstack11lll11111_opy_ = [
  bstack1l11l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡇࡃࡌࡐࡊࡊࠧᧅ"),
  bstack1l11l11_opy_ (u"ࠫࡊࡘࡒࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫᧆ"),
  bstack1l11l11_opy_ (u"ࠬࡋࡒࡓࡡࡅࡐࡔࡉࡋࡆࡆࡢࡆ࡞ࡥࡃࡍࡋࡈࡒ࡙࠭ᧇ"),
  bstack1l11l11_opy_ (u"࠭ࡅࡓࡔࡢࡒࡊ࡚ࡗࡐࡔࡎࡣࡈࡎࡁࡏࡉࡈࡈࠬᧈ"),
  bstack1l11l11_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡇࡗࡣࡓࡕࡔࡠࡅࡒࡒࡓࡋࡃࡕࡇࡇࠫᧉ"),
  bstack1l11l11_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡆࡐࡔ࡙ࡅࡅࠩ᧊"),
  bstack1l11l11_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊ࡙ࡅࡕࠩ᧋"),
  bstack1l11l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡆࡖࡕࡈࡈࠬ᧌"),
  bstack1l11l11_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡇࡂࡐࡔࡗࡉࡉ࠭᧍"),
  bstack1l11l11_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭᧎"),
  bstack1l11l11_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧ᧏"),
  bstack1l11l11_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤࡏࡎࡗࡃࡏࡍࡉ࠭᧐"),
  bstack1l11l11_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫ᧑"),
  bstack1l11l11_opy_ (u"ࠩࡈࡖࡗࡥࡔࡖࡐࡑࡉࡑࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ᧒"),
  bstack1l11l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧ᧓"),
  bstack1l11l11_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫ᧔"),
  bstack1l11l11_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡎࡏࡔࡖࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨ᧕"),
  bstack1l11l11_opy_ (u"࠭ࡅࡓࡔࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭᧖"),
  bstack1l11l11_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨ᧗"),
  bstack1l11l11_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡖࡊ࡙ࡏࡍࡗࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ᧘"),
  bstack1l11l11_opy_ (u"ࠩࡈࡖࡗࡥࡍࡂࡐࡇࡅ࡙ࡕࡒ࡚ࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨ᧙"),
]
bstack1ll1ll1111_opy_ = bstack1l11l11_opy_ (u"ࠪ࠲࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠯ࠨ᧚")
bstack1llll1111_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠫࢃ࠭᧛")), bstack1l11l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ᧜"), bstack1l11l11_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ᧝"))
bstack11ll1lll1ll_opy_ = bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡩࠨ᧞")
bstack11l1ll11lll_opy_ = [ bstack1l11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᧟"), bstack1l11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᧠"), bstack1l11l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ᧡"), bstack1l11l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᧢")]
bstack1111llll1_opy_ = [ bstack1l11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᧣"), bstack1l11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ᧤"), bstack1l11l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭᧥"), bstack1l11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ᧦") ]
bstack1l11l11lll_opy_ = [ bstack1l11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᧧") ]
bstack11l1ll1ll1l_opy_ = [ bstack1l11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᧨") ]
bstack11l1111l1l_opy_ = 360
bstack11ll11l11l1_opy_ = bstack1l11l11_opy_ (u"ࠦࡦࡶࡰ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦ᧩")
bstack11l1lllll11_opy_ = bstack1l11l11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡪࡵࡶࡹࡪࡹࠢ᧪")
bstack11l1l1lll1l_opy_ = bstack1l11l11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡫ࡶࡷࡺ࡫ࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠤ᧫")
bstack11ll1lll11l_opy_ = bstack1l11l11_opy_ (u"ࠢࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡶࡨࡷࡹࡹࠠࡢࡴࡨࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡰࡰࠣࡓࡘࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠦࡵࠣࡥࡳࡪࠠࡢࡤࡲࡺࡪࠦࡦࡰࡴࠣࡅࡳࡪࡲࡰ࡫ࡧࠤࡩ࡫ࡶࡪࡥࡨࡷ࠳ࠨ᧬")
bstack11ll1l11l11_opy_ = bstack1l11l11_opy_ (u"ࠣ࠳࠴࠲࠵ࠨ᧭")
bstack1111ll111l_opy_ = {
  bstack1l11l11_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ᧮"): bstack1l11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᧯"),
  bstack1l11l11_opy_ (u"ࠫࡋࡇࡉࡍࠩ᧰"): bstack1l11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᧱"),
  bstack1l11l11_opy_ (u"࠭ࡓࡌࡋࡓࠫ᧲"): bstack1l11l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ᧳")
}
bstack11ll11l11_opy_ = [
  bstack1l11l11_opy_ (u"ࠣࡩࡨࡸࠧ᧴"),
  bstack1l11l11_opy_ (u"ࠤࡪࡳࡇࡧࡣ࡬ࠤ᧵"),
  bstack1l11l11_opy_ (u"ࠥ࡫ࡴࡌ࡯ࡳࡹࡤࡶࡩࠨ᧶"),
  bstack1l11l11_opy_ (u"ࠦࡷ࡫ࡦࡳࡧࡶ࡬ࠧ᧷"),
  bstack1l11l11_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦ᧸"),
  bstack1l11l11_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ᧹"),
  bstack1l11l11_opy_ (u"ࠢࡴࡷࡥࡱ࡮ࡺࡅ࡭ࡧࡰࡩࡳࡺࠢ᧺"),
  bstack1l11l11_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ᧻"),
  bstack1l11l11_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧ᧼"),
  bstack1l11l11_opy_ (u"ࠥࡧࡱ࡫ࡡࡳࡇ࡯ࡩࡲ࡫࡮ࡵࠤ᧽"),
  bstack1l11l11_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࡷࠧ᧾"),
  bstack1l11l11_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠧ᧿"),
  bstack1l11l11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡁࡴࡻࡱࡧࡘࡩࡲࡪࡲࡷࠦᨀ"),
  bstack1l11l11_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᨁ"),
  bstack1l11l11_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᨂ"),
  bstack1l11l11_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡗࡳࡺࡩࡨࡂࡥࡷ࡭ࡴࡴࠢᨃ"),
  bstack1l11l11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡑࡺࡲࡴࡪࡖࡲࡹࡨ࡮ࠢᨄ"),
  bstack1l11l11_opy_ (u"ࠦࡸ࡮ࡡ࡬ࡧࠥᨅ"),
  bstack1l11l11_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࡅࡵࡶࠢᨆ")
]
bstack11ll1111111_opy_ = [
  bstack1l11l11_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧᨇ"),
  bstack1l11l11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᨈ"),
  bstack1l11l11_opy_ (u"ࠣࡣࡸࡸࡴࠨᨉ"),
  bstack1l11l11_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤᨊ"),
  bstack1l11l11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᨋ")
]
bstack1l11l1111_opy_ = {
  bstack1l11l11_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥᨌ"): [bstack1l11l11_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦᨍ")],
  bstack1l11l11_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᨎ"): [bstack1l11l11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᨏ")],
  bstack1l11l11_opy_ (u"ࠣࡣࡸࡸࡴࠨᨐ"): [bstack1l11l11_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨᨑ"), bstack1l11l11_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨᨒ"), bstack1l11l11_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᨓ"), bstack1l11l11_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦᨔ")],
  bstack1l11l11_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨᨕ"): [bstack1l11l11_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢᨖ")],
  bstack1l11l11_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᨗ"): [bstack1l11l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨᨘࠦ")],
}
bstack11l1lll1ll1_opy_ = {
  bstack1l11l11_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤᨙ"): bstack1l11l11_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥᨚ"),
  bstack1l11l11_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᨛ"): bstack1l11l11_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ᨜"),
  bstack1l11l11_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦ᨝"): bstack1l11l11_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࠥ᨞"),
  bstack1l11l11_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧ᨟"): bstack1l11l11_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧᨠ"),
  bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᨡ"): bstack1l11l11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᨢ")
}
bstack111l1ll11l_opy_ = {
  bstack1l11l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᨣ"): bstack1l11l11_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࠦࡓࡦࡶࡸࡴࠬᨤ"),
  bstack1l11l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᨥ"): bstack1l11l11_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡖࡨࡥࡷࡪ࡯ࡸࡰࠪᨦ"),
  bstack1l11l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᨧ"): bstack1l11l11_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡖࡩࡹࡻࡰࠨᨨ"),
  bstack1l11l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᨩ"): bstack1l11l11_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭ᨪ")
}
bstack11l1lllll1l_opy_ = 65536
bstack11l1lll1lll_opy_ = bstack1l11l11_opy_ (u"ࠧ࠯࠰࠱࡟࡙ࡘࡕࡏࡅࡄࡘࡊࡊ࡝ࠨᨫ")
bstack11l1ll11ll1_opy_ = [
      bstack1l11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᨬ"), bstack1l11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᨭ"), bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᨮ"), bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᨯ"), bstack1l11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧᨰ"),
      bstack1l11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᨱ"), bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᨲ"), bstack1l11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᨳ"), bstack1l11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪᨴ"),
      bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᨵ"), bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᨶ"), bstack1l11l11_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨᨷ")
    ]
bstack11l1ll1l111_opy_= {
  bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᨸ"): bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᨹ"),
  bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᨺ"): bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᨻ"),
  bstack1l11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᨼ"): bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᨽ"),
  bstack1l11l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᨾ"): bstack1l11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᨿ"),
  bstack1l11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᩀ"): bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᩁ"),
  bstack1l11l11_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᩂ"): bstack1l11l11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᩃ"),
  bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᩄ"): bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᩅ"),
  bstack1l11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᩆ"): bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᩇ"),
  bstack1l11l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᩈ"): bstack1l11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᩉ"),
  bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨᩊ"): bstack1l11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩋ"),
  bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᩌ"): bstack1l11l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᩍ"),
  bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᩎ"): bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᩏ"),
  bstack1l11l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᩐ"): bstack1l11l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬᩑ"),
  bstack1l11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᩒ"): bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᩓ"),
  bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᩔ"): bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᩕ"),
  bstack1l11l11_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᩖ"): bstack1l11l11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᩗ"),
  bstack1l11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᩘ"): bstack1l11l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᩙ"),
  bstack1l11l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᩚ"): bstack1l11l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᩛ"),
  bstack1l11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᩜ"): bstack1l11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᩝ"),
  bstack1l11l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᩞ"): bstack1l11l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ᩟"),
  bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ᩠ࠫ"): bstack1l11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᩡ"),
  bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩢ"): bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᩣ"),
  bstack1l11l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᩤ"): bstack1l11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᩥ"),
  bstack1l11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩦ"): bstack1l11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᩧ"),
  bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩨ"): bstack1l11l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᩩ"),
  bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᩪ"): bstack1l11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᩫ")
}
bstack11l1ll1l11l_opy_ = [bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᩬ"), bstack1l11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᩭ")]
bstack1l11l11l1_opy_ = (bstack1l11l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᩮ"),)
bstack11l1ll1lll1_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬࠱ࡹ࠵࠴ࡻࡰࡥࡣࡷࡩࡤࡩ࡬ࡪࠩᩯ")
bstack1lll11111l_opy_ = bstack1l11l11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠯ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠵ࡶ࠲࠱ࡪࡶ࡮ࡪࡳ࠰ࠤᩰ")
bstack1ll1l11l1_opy_ = bstack1l11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩࡵ࡭ࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࠨᩱ")
bstack1ll1l1llll_opy_ = bstack1l11l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠤᩲ")
class EVENTS(Enum):
  bstack11l1ll1l1ll_opy_ = bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭ᩳ")
  bstack1ll1l111l_opy_ = bstack1l11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮ࡨࡥࡳࡻࡰࠨᩴ") # final bstack11l1lll1l11_opy_
  bstack11ll111111l_opy_ = bstack1l11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡲ࡯ࡨࡵࠪ᩵")
  bstack1l1111ll1_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨ᩶") #shift post bstack11l1ll111ll_opy_
  bstack1ll111l1ll_opy_ = bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡶࡲࡪࡰࡷ࠱ࡧࡻࡩ࡭ࡦ࡯࡭ࡳࡱࠧ᩷") #shift post bstack11l1ll111ll_opy_
  bstack11l1l1lll11_opy_ = bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡪࡸࡦࠬ᩸") #shift
  bstack11l1ll11l1l_opy_ = bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡩࡵࡷ࡯࡮ࡲࡥࡩ࠭᩹") #shift
  bstack1l1l111l1_opy_ = bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽࡬ࡺࡨ࠭࡮ࡣࡱࡥ࡬࡫࡭ࡦࡰࡷࠫ᩺")
  bstack1ll111l111l_opy_ = bstack1l11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿ࡹࡡࡷࡧ࠰ࡶࡪࡹࡵ࡭ࡶࡶࠫ᩻")
  bstack1l1l1ll111_opy_ = bstack1l11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡤࡳ࡫ࡹࡩࡷ࠳ࡰࡦࡴࡩࡳࡷࡳࡳࡤࡣࡱࠫ᩼")
  bstack1l1ll1llll_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡱࡵࡣࡢ࡮ࠪ᩽") #shift
  bstack1l1l1l1111_opy_ = bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡤࡴࡵ࠳ࡵࡱ࡮ࡲࡥࡩ࠭᩾") #shift
  bstack1l11l1l1_opy_ = bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡣࡪ࠯ࡤࡶࡹ࡯ࡦࡢࡥࡷࡷ᩿ࠬ")
  bstack1l1111ll_opy_ = bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠭ࡳࡧࡶࡹࡱࡺࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠩ᪀") #shift
  bstack11l1l1l11l_opy_ = bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴࠩ᪁") #shift
  bstack11l1ll111l1_opy_ = bstack1l11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾ࠭᪂") #shift
  bstack1l1l1l11l11_opy_ = bstack1l11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ᪃")
  bstack1l1lll111l_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡹࡴࡢࡶࡸࡷࠬ᪄") #shift
  bstack1l1ll1l1ll_opy_ = bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿࡮ࡵࡣ࠯ࡰࡥࡳࡧࡧࡦ࡯ࡨࡲࡹ࠭᪅")
  bstack11l1llllll1_opy_ = bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸ࡯ࡹࡻ࠰ࡷࡪࡺࡵࡱࠩ᪆") #shift
  bstack11ll1ll1l_opy_ = bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥࡵࡷࡳࠫ᪇")
  bstack11l1ll11111_opy_ = bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡹ࡮ࡢࡲࡶ࡬ࡴࡺࠧ᪈") # not bstack11l1lll1l1l_opy_ in python
  bstack1l11l11l1l_opy_ = bstack1l11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡲࡷ࡬ࡸࠬ᪉") # used in bstack11l1lll11ll_opy_
  bstack1ll11lll1_opy_ = bstack1l11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡩࡨࡸࠬ᪊") # used in bstack11l1lll11ll_opy_
  bstack1111lll11_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬࠼࡫ࡳࡴࡱࠧ᪋")
  bstack1llll1l1ll_opy_ = bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠫ᪌")
  bstack1l1111l1l_opy_ = bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭ࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠫ᪍") #
  bstack1l1l1111_opy_ = bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡸࡦࡱࡥࡔࡥࡵࡩࡪࡴࡓࡩࡱࡷࠫ᪎")
  bstack11ll11l111_opy_ = bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫ᪏")
  bstack1l1l1lllll_opy_ = bstack1l11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡴࡨ࠱ࡹ࡫ࡳࡵࠩ᪐")
  bstack1l11l11ll1_opy_ = bstack1l11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡲࡷࡹ࠳ࡴࡦࡵࡷࠫ᪑")
  bstack1l1l11ll11_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡶࡪ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧ᪒") #shift
  bstack1lll11lll_opy_ = bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ᪓") #shift
  bstack11l1lll11l1_opy_ = bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࠯ࡦࡥࡵࡺࡵࡳࡧࠪ᪔")
  bstack11l1l1ll1l1_opy_ = bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡪࡦ࡯ࡩ࠲ࡺࡩ࡮ࡧࡲࡹࡹ࠭᪕")
  bstack1ll1l1l1lll_opy_ = bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡷࡹࡧࡲࡵࠩ᪖")
  bstack11l1llll1ll_opy_ = bstack1l11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡩࡵࡷ࡯࡮ࡲࡥࡩ࠭᪗")
  bstack11l1l1ll1ll_opy_ = bstack1l11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡩࡨࡦࡥ࡮࠱ࡺࡶࡤࡢࡶࡨࠫ᪘")
  bstack1lll111l1l1_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡥࡳࡴࡺࡳࡵࡴࡤࡴࠬ᪙")
  bstack1ll1ll1ll11_opy_ = bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡧࡴࡴ࡮ࡦࡥࡷࠫ᪚")
  bstack1ll1ll1l1l1_opy_ = bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡸࡺ࡯ࡱࠩ᪛")
  bstack1lll1l1l1l1_opy_ = bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠧ᪜")
  bstack1lll1llllll_opy_ = bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡀࡣࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰࠪ᪝")
  bstack11l1l1llll1_opy_ = bstack1l11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠫ᪞")
  bstack11l1l1lllll_opy_ = bstack1l11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡨ࡬ࡲࡩࡔࡥࡢࡴࡨࡷࡹࡎࡵࡣࠩ᪟")
  bstack1l11ll1111l_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡊࡰ࡬ࡸࠬ᪠")
  bstack1l11ll11l1l_opy_ = bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡷࡺࠧ᪡")
  bstack1ll111l1ll1_opy_ = bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪ᪢")
  bstack11l1ll1ll11_opy_ = bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡈࡵ࡮ࡧ࡫ࡪࠫ᪣")
  bstack1ll11111l1l_opy_ = bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡖࡸࡪࡶࠧ᪤")
  bstack1ll111111l1_opy_ = bstack1l11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࡫ࡖࡩࡱ࡬ࡈࡦࡣ࡯ࡋࡪࡺࡒࡦࡵࡸࡰࡹ࠭᪥")
  bstack1l1lll111ll_opy_ = bstack1l11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡆࡸࡨࡲࡹ࠭᪦")
  bstack1l1l1ll1ll1_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠬᪧ")
  bstack1l1ll1ll11l_opy_ = bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺࡭ࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࡉࡻ࡫࡮ࡵࠩ᪨")
  bstack11l1ll1111l_opy_ = bstack1l11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡧࡱࡵࡺ࡫ࡵࡦࡖࡨࡷࡹࡋࡶࡦࡰࡷࠫ᪩")
  bstack1l11lll1ll1_opy_ = bstack1l11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡵࡰࠨ᪪")
  bstack1ll1lllll1l_opy_ = bstack1l11l11_opy_ (u"ࠩࡶࡨࡰࡀ࡯࡯ࡕࡷࡳࡵ࠭᪫")
class STAGE(Enum):
  bstack11l1l11l_opy_ = bstack1l11l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩ᪬")
  END = bstack1l11l11_opy_ (u"ࠫࡪࡴࡤࠨ᪭")
  bstack1lll11l1_opy_ = bstack1l11l11_opy_ (u"ࠬࡹࡩ࡯ࡩ࡯ࡩࠬ᪮")
bstack111l11ll1_opy_ = {
  bstack1l11l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭᪯"): bstack1l11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᪰"),
  bstack1l11l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬ᪱"): bstack1l11l11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ᪲")
}
PLAYWRIGHT_HUB_URL = bstack1l11l11_opy_ (u"ࠥࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠧ᪳")
bstack1ll11l1ll11_opy_ = 98
bstack1ll111l1lll_opy_ = 100
bstack1111l1l111_opy_ = {
  bstack1l11l11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪ᪴"): bstack1l11l11_opy_ (u"ࠬ࠳࠭ࡳࡧࡵࡹࡳࡹ᪵ࠧ"),
  bstack1l11l11_opy_ (u"࠭ࡤࡦ࡮ࡤࡽ᪶ࠬ"): bstack1l11l11_opy_ (u"ࠧ࠮࠯ࡵࡩࡷࡻ࡮ࡴ࠯ࡧࡩࡱࡧࡹࠨ᪷"),
  bstack1l11l11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࠭ࡥࡧ࡯ࡥࡾ᪸࠭"): 0
}
bstack11l1lllllll_opy_ = bstack1l11l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ᪹")
bstack11l1lll111l_opy_ = bstack1l11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ᪺ࠢ")