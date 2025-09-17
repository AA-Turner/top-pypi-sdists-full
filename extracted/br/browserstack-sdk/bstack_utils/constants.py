# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import re
from enum import Enum
bstack1ll1ll111_opy_ = {
  bstack1l11ll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧថ"): bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪទ"),
  bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪធ"): bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫន"),
  bstack1l11ll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬប"): bstack1l11ll1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧផ"),
  bstack1l11ll1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫព"): bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬភ"),
  bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫម"): bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨយ"),
  bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫរ"): bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨល"),
  bstack1l11ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨវ"): bstack1l11ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩឝ"),
  bstack1l11ll1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫឞ"): bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫស"),
  bstack1l11ll1_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬហ"): bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨឡ"),
  bstack1l11ll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧអ"): bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧឣ"),
  bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨឤ"): bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨឥ"),
  bstack1l11ll1_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬឦ"): bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬឧ"),
  bstack1l11ll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧឨ"): bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧឩ"),
  bstack1l11ll1_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪឪ"): bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪឫ"),
  bstack1l11ll1_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪឬ"): bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪឭ"),
  bstack1l11ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩឮ"): bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩឯ"),
  bstack1l11ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫឰ"): bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬឱ"),
  bstack1l11ll1_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪឲ"): bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪឳ"),
  bstack1l11ll1_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ឴"): bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ឵"),
  bstack1l11ll1_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨា"): bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨិ"),
  bstack1l11ll1_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬី"): bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬឹ"),
  bstack1l11ll1_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧឺ"): bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧុ"),
  bstack1l11ll1_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ូ"): bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭ួ"),
  bstack1l11ll1_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪើ"): bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪឿ"),
  bstack1l11ll1_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬៀ"): bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬេ"),
  bstack1l11ll1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩែ"): bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩៃ"),
  bstack1l11ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬោ"): bstack1l11ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩៅ"),
  bstack1l11ll1_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧំ"): bstack1l11ll1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩះ"),
  bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬៈ"): bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭៉"),
  bstack1l11ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ៊"): bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ់"),
  bstack1l11ll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ៌"): bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ៍"),
  bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ៎"): bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭៏"),
  bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ័"): bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ៑"),
  bstack1l11ll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ្"): bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨ៓"),
  bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ។"): bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ៕"),
  bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ៖"): bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧៗ"),
  bstack1l11ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪ៘"): bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪ៙"),
  bstack1l11ll1_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭៚"): bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭៛"),
  bstack1l11ll1_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩៜ"): bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩ៝"),
  bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ៞"): bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ៟"),
  bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ០"): bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ១")
}
bstack11l1l1lll1l_opy_ = [
  bstack1l11ll1_opy_ (u"ࠪࡳࡸ࠭២"),
  bstack1l11ll1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ៣"),
  bstack1l11ll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ៤"),
  bstack1l11ll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ៥"),
  bstack1l11ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ៦"),
  bstack1l11ll1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬ៧"),
  bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ៨"),
]
bstack1l11111111_opy_ = {
  bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ៩"): [bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ៪"), bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡑࡅࡒࡋࠧ៫")],
  bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ៬"): bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ៭"),
  bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ៮"): bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬ៯"),
  bstack1l11ll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ៰"): bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠩ៱"),
  bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ៲"): bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ៳"),
  bstack1l11ll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ៴"): bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡕࡢࡔࡊࡘ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩ៵"),
  bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭៶"): bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨ៷"),
  bstack1l11ll1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ៸"): bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩ៹"),
  bstack1l11ll1_opy_ (u"࠭ࡡࡱࡲࠪ៺"): [bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࡢࡍࡉ࠭៻"), bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࠫ៼")],
  bstack1l11ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ៽"): bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡌࡐࡉࡏࡉ࡛ࡋࡌࠨ៾"),
  bstack1l11ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ៿"): bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᠀"),
  bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᠁"): [bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠫ᠂"), bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨ᠃")],
  bstack1l11ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭᠄"): bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗ࡙ࡗࡈࡏࡔࡅࡄࡐࡊ࠭᠅")
}
bstack11l11111ll_opy_ = {
  bstack1l11ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭᠆"): [bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ᠇"), bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ᠈")],
  bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ᠉"): [bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹ࡟࡬ࡧࡼࠫ᠊"), bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᠋")],
  bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᠌"): bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᠍"),
  bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ᠎"): bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ᠏"),
  bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᠐"): bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᠑"),
  bstack1l11ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᠒"): [bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡴࡵ࠭᠓"), bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᠔")],
  bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ᠕"): bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ᠖"),
  bstack1l11ll1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ᠗"): bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ᠘"),
  bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵ࠭᠙"): bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࠭᠚"),
  bstack1l11ll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭᠛"): bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡧࡍࡧࡹࡩࡱ࠭᠜"),
  bstack1l11ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᠝"): bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᠞")
}
bstack11l1l1111l_opy_ = {
  bstack1l11ll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ᠟"): bstack1l11ll1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᠠ"),
  bstack1l11ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᠡ"): [bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᠢ"), bstack1l11ll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᠣ")],
  bstack1l11ll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᠤ"): bstack1l11ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᠥ"),
  bstack1l11ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᠦ"): bstack1l11ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᠧ"),
  bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᠨ"): [bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᠩ"), bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᠪ")],
  bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᠫ"): bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᠬ"),
  bstack1l11ll1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᠭ"): bstack1l11ll1_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧᠮ"),
  bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᠯ"): [bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᠰ"), bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᠱ")],
  bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᠲ"): [bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨᠳ"), bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࠨᠴ")]
}
bstack1ll11lllll_opy_ = [
  bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᠵ"),
  bstack1l11ll1_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ᠶ"),
  bstack1l11ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪᠷ"),
  bstack1l11ll1_opy_ (u"ࠬࡹࡥࡵ࡙࡬ࡲࡩࡵࡷࡓࡧࡦࡸࠬᠸ"),
  bstack1l11ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࡳࠨᠹ"),
  bstack1l11ll1_opy_ (u"ࠧࡴࡶࡵ࡭ࡨࡺࡆࡪ࡮ࡨࡍࡳࡺࡥࡳࡣࡦࡸࡦࡨࡩ࡭࡫ࡷࡽࠬᠺ"),
  bstack1l11ll1_opy_ (u"ࠨࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡔࡷࡵ࡭ࡱࡶࡅࡩ࡭ࡧࡶࡪࡱࡵࠫᠻ"),
  bstack1l11ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᠼ"),
  bstack1l11ll1_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᠽ"),
  bstack1l11ll1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬᠾ"),
  bstack1l11ll1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫᠿ"),
  bstack1l11ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧᡀ"),
]
bstack1ll11lll1_opy_ = [
  bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᡁ"),
  bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᡂ"),
  bstack1l11ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᡃ"),
  bstack1l11ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᡄ"),
  bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᡅ"),
  bstack1l11ll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᡆ"),
  bstack1l11ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᡇ"),
  bstack1l11ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᡈ"),
  bstack1l11ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᡉ"),
  bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧᡊ"),
  bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᡋ"),
  bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫᡌ"),
  bstack1l11ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧᡍ"),
  bstack1l11ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡚ࡡࡨࠩᡎ"),
  bstack1l11ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᡏ"),
  bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᡐ"),
  bstack1l11ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᡑ"),
  bstack1l11ll1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠲ࠩᡒ"),
  bstack1l11ll1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠴ࠪᡓ"),
  bstack1l11ll1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠶ࠫᡔ"),
  bstack1l11ll1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠸ࠬᡕ"),
  bstack1l11ll1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠺࠭ᡖ"),
  bstack1l11ll1_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠼ࠧᡗ"),
  bstack1l11ll1_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠷ࠨᡘ"),
  bstack1l11ll1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠹ࠩᡙ"),
  bstack1l11ll1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠻ࠪᡚ"),
  bstack1l11ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᡛ"),
  bstack1l11ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᡜ"),
  bstack1l11ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᡝ"),
  bstack1l11ll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᡞ"),
  bstack1l11ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᡟ"),
  bstack1l11ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᡠ"),
  bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᡡ")
]
bstack11l1lll11l1_opy_ = [
  bstack1l11ll1_opy_ (u"ࠬࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪᡢ"),
  bstack1l11ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᡣ"),
  bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᡤ"),
  bstack1l11ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᡥ"),
  bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺࡐࡳ࡫ࡲࡶ࡮ࡺࡹࠨᡦ"),
  bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᡧ"),
  bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡥ࡬࠭ᡨ"),
  bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᡩ"),
  bstack1l11ll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᡪ"),
  bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᡫ"),
  bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᡬ"),
  bstack1l11ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᡭ"),
  bstack1l11ll1_opy_ (u"ࠪࡳࡸ࠭ᡮ"),
  bstack1l11ll1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᡯ"),
  bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫᡰ"),
  bstack1l11ll1_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨᡱ"),
  bstack1l11ll1_opy_ (u"ࠧࡳࡧࡪ࡭ࡴࡴࠧᡲ"),
  bstack1l11ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪᡳ"),
  bstack1l11ll1_opy_ (u"ࠩࡰࡥࡨ࡮ࡩ࡯ࡧࠪᡴ"),
  bstack1l11ll1_opy_ (u"ࠪࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠧᡵ"),
  bstack1l11ll1_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩᡶ"),
  bstack1l11ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᡷ"),
  bstack1l11ll1_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬᡸ"),
  bstack1l11ll1_opy_ (u"ࠧ࡯ࡱࡓࡥ࡬࡫ࡌࡰࡣࡧࡘ࡮ࡳࡥࡰࡷࡷࠫ᡹"),
  bstack1l11ll1_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩ᡺"),
  bstack1l11ll1_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ᡻"),
  bstack1l11ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ᡼"),
  bstack1l11ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡪࡴࡤࡌࡧࡼࡷࠬ᡽"),
  bstack1l11ll1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ᡾"),
  bstack1l11ll1_opy_ (u"࠭࡮ࡰࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠪ᡿"),
  bstack1l11ll1_opy_ (u"ࠧࡤࡪࡨࡧࡰ࡛ࡒࡍࠩᢀ"),
  bstack1l11ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᢁ"),
  bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡅࡲࡳࡰ࡯ࡥࡴࠩᢂ"),
  bstack1l11ll1_opy_ (u"ࠪࡧࡦࡶࡴࡶࡴࡨࡇࡷࡧࡳࡩࠩᢃ"),
  bstack1l11ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᢄ"),
  bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᢅ"),
  bstack1l11ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࡙ࡩࡷࡹࡩࡰࡰࠪᢆ"),
  bstack1l11ll1_opy_ (u"ࠧ࡯ࡱࡅࡰࡦࡴ࡫ࡑࡱ࡯ࡰ࡮ࡴࡧࠨᢇ"),
  bstack1l11ll1_opy_ (u"ࠨ࡯ࡤࡷࡰ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧᢈ"),
  bstack1l11ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡎࡲ࡫ࡸ࠭ᢉ"),
  bstack1l11ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡌࡨࠬᢊ"),
  bstack1l11ll1_opy_ (u"ࠫࡩ࡫ࡤࡪࡥࡤࡸࡪࡪࡄࡦࡸ࡬ࡧࡪ࠭ᢋ"),
  bstack1l11ll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡕࡧࡲࡢ࡯ࡶࠫᢌ"),
  bstack1l11ll1_opy_ (u"࠭ࡰࡩࡱࡱࡩࡓࡻ࡭ࡣࡧࡵࠫᢍ"),
  bstack1l11ll1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬᢎ"),
  bstack1l11ll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡕࡰࡵ࡫ࡲࡲࡸ࠭ᢏ"),
  bstack1l11ll1_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧᢐ"),
  bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᢑ"),
  bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᢒ"),
  bstack1l11ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡇ࡯࡯࡮ࡧࡷࡶ࡮ࡩࠧᢓ"),
  bstack1l11ll1_opy_ (u"࠭ࡶࡪࡦࡨࡳ࡛࠸ࠧᢔ"),
  bstack1l11ll1_opy_ (u"ࠧ࡮࡫ࡧࡗࡪࡹࡳࡪࡱࡱࡍࡳࡹࡴࡢ࡮࡯ࡅࡵࡶࡳࠨᢕ"),
  bstack1l11ll1_opy_ (u"ࠨࡧࡶࡴࡷ࡫ࡳࡴࡱࡖࡩࡷࡼࡥࡳࠩᢖ"),
  bstack1l11ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨᢗ"),
  bstack1l11ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡈࡪࡰࠨᢘ"),
  bstack1l11ll1_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫᢙ"),
  bstack1l11ll1_opy_ (u"ࠬࡹࡹ࡯ࡥࡗ࡭ࡲ࡫ࡗࡪࡶ࡫ࡒ࡙ࡖࠧᢚ"),
  bstack1l11ll1_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫᢛ"),
  bstack1l11ll1_opy_ (u"ࠧࡨࡲࡶࡐࡴࡩࡡࡵ࡫ࡲࡲࠬᢜ"),
  bstack1l11ll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩᢝ"),
  bstack1l11ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩᢞ"),
  bstack1l11ll1_opy_ (u"ࠪࡪࡴࡸࡣࡦࡅ࡫ࡥࡳ࡭ࡥࡋࡣࡵࠫᢟ"),
  bstack1l11ll1_opy_ (u"ࠫࡽࡳࡳࡋࡣࡵࠫᢠ"),
  bstack1l11ll1_opy_ (u"ࠬࡾ࡭ࡹࡌࡤࡶࠬᢡ"),
  bstack1l11ll1_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬᢢ"),
  bstack1l11ll1_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧᢣ"),
  bstack1l11ll1_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩᢤ"),
  bstack1l11ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬᢥ"),
  bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶࡖࡦࡴࡶ࡭ࡴࡴࠧᢦ"),
  bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪᢧ"),
  bstack1l11ll1_opy_ (u"ࠬࡸࡥࡴ࡫ࡪࡲࡆࡶࡰࠨᢨ"),
  bstack1l11ll1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯࡫ࡰࡥࡹ࡯࡯࡯ࡵᢩࠪ"),
  bstack1l11ll1_opy_ (u"ࠧࡤࡣࡱࡥࡷࡿࠧᢪ"),
  bstack1l11ll1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ᢫"),
  bstack1l11ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ᢬"),
  bstack1l11ll1_opy_ (u"ࠪ࡭ࡪ࠭᢭"),
  bstack1l11ll1_opy_ (u"ࠫࡪࡪࡧࡦࠩ᢮"),
  bstack1l11ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ᢯"),
  bstack1l11ll1_opy_ (u"࠭ࡱࡶࡧࡸࡩࠬᢰ"),
  bstack1l11ll1_opy_ (u"ࠧࡪࡰࡷࡩࡷࡴࡡ࡭ࠩᢱ"),
  bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴࡘࡺ࡯ࡳࡧࡆࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠩᢲ"),
  bstack1l11ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡅࡤࡱࡪࡸࡡࡊ࡯ࡤ࡫ࡪࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨᢳ"),
  bstack1l11ll1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡆࡺࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭ᢴ"),
  bstack1l11ll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡋࡱࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧᢵ"),
  bstack1l11ll1_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᢶ"),
  bstack1l11ll1_opy_ (u"࠭ࡲࡦࡵࡨࡶࡻ࡫ࡄࡦࡸ࡬ࡧࡪ࠭ᢷ"),
  bstack1l11ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᢸ"),
  bstack1l11ll1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪᢹ"),
  bstack1l11ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡤࡷࡸࡩ࡯ࡥࡧࠪᢺ"),
  bstack1l11ll1_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡌࡳࡸࡊࡥࡷ࡫ࡦࡩࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᢻ"),
  bstack1l11ll1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡺࡪࡩࡰࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫᢼ"),
  bstack1l11ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡶࡰ࡭ࡧࡓࡥࡾ࠭ᢽ"),
  bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᢾ"),
  bstack1l11ll1_opy_ (u"ࠧࡸࡦ࡬ࡳࡘ࡫ࡲࡷ࡫ࡦࡩࠬᢿ"),
  bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᣀ"),
  bstack1l11ll1_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶࡆࡶࡴࡹࡳࡔ࡫ࡷࡩ࡙ࡸࡡࡤ࡭࡬ࡲ࡬࠭ᣁ"),
  bstack1l11ll1_opy_ (u"ࠪ࡬࡮࡭ࡨࡄࡱࡱࡸࡷࡧࡳࡵࠩᣂ"),
  bstack1l11ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡔࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࡳࠨᣃ"),
  bstack1l11ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨᣄ"),
  bstack1l11ll1_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪᣅ"),
  bstack1l11ll1_opy_ (u"ࠧࡳࡧࡰࡳࡻ࡫ࡉࡐࡕࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࡌࡰࡥࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬᣆ"),
  bstack1l11ll1_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪᣇ"),
  bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᣈ"),
  bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬᣉ"),
  bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᣊ"),
  bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᣋ"),
  bstack1l11ll1_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᣌ"),
  bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ᣍ"),
  bstack1l11ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪᣎ"),
  bstack1l11ll1_opy_ (u"ࠩࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡕࡸ࡯࡮ࡲࡷࡆࡪ࡮ࡡࡷ࡫ࡲࡶࠬᣏ")
]
bstack1l11ll1l1_opy_ = {
  bstack1l11ll1_opy_ (u"ࠪࡺࠬᣐ"): bstack1l11ll1_opy_ (u"ࠫࡻ࠭ᣑ"),
  bstack1l11ll1_opy_ (u"ࠬ࡬ࠧᣒ"): bstack1l11ll1_opy_ (u"࠭ࡦࠨᣓ"),
  bstack1l11ll1_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭ᣔ"): bstack1l11ll1_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧᣕ"),
  bstack1l11ll1_opy_ (u"ࠩࡲࡲࡱࡿࡡࡶࡶࡲࡱࡦࡺࡥࠨᣖ"): bstack1l11ll1_opy_ (u"ࠪࡳࡳࡲࡹࡂࡷࡷࡳࡲࡧࡴࡦࠩᣗ"),
  bstack1l11ll1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨᣘ"): bstack1l11ll1_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩᣙ"),
  bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩᣚ"): bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᣛ"),
  bstack1l11ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡰࡴࡷࠫᣜ"): bstack1l11ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᣝ"),
  bstack1l11ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᣞ"): bstack1l11ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᣟ"),
  bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᣠ"): bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩᣡ"),
  bstack1l11ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨᣢ"): bstack1l11ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡍࡵࡳࡵࠩᣣ"),
  bstack1l11ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪᣤ"): bstack1l11ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫᣥ"),
  bstack1l11ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᣦ"): bstack1l11ll1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᣧ"),
  bstack1l11ll1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᣨ"): bstack1l11ll1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᣩ"),
  bstack1l11ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᣪ"): bstack1l11ll1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫᣫ"),
  bstack1l11ll1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᣬ"): bstack1l11ll1_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᣭ"),
  bstack1l11ll1_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩᣮ"): bstack1l11ll1_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪࠪᣯ"),
  bstack1l11ll1_opy_ (u"ࠧࡱࡣࡦࡪ࡮ࡲࡥࠨᣰ"): bstack1l11ll1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᣱ"),
  bstack1l11ll1_opy_ (u"ࠩࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᣲ"): bstack1l11ll1_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᣳ"),
  bstack1l11ll1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᣴ"): bstack1l11ll1_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᣵ"),
  bstack1l11ll1_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧ᣶"): bstack1l11ll1_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨ᣷"),
  bstack1l11ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᣸"): bstack1l11ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᣹"),
  bstack1l11ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬ᣺"): bstack1l11ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡶࡥࡢࡶࡨࡶࠬ᣻")
}
bstack11l1l1llll1_opy_ = bstack1l11ll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡧࡪࡶ࡫ࡹࡧ࠴ࡣࡰ࡯࠲ࡴࡪࡸࡣࡺ࠱ࡦࡰ࡮࠵ࡲࡦ࡮ࡨࡥࡸ࡫ࡳ࠰࡮ࡤࡸࡪࡹࡴ࠰ࡦࡲࡻࡳࡲ࡯ࡢࡦࠥ᣼")
bstack11l1lll1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠵ࡨࡦࡣ࡯ࡸ࡭ࡩࡨࡦࡥ࡮ࠦ᣽")
bstack1lll11lll1_opy_ = bstack1l11ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡧࡧࡷ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡵࡨࡲࡩࡥࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥ᣾")
bstack11111l1l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡺࡨ࠴࡮ࡵࡣࠩ᣿")
bstack1ll11lll1l_opy_ = bstack1l11ll1_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠬᤀ")
bstack1l1lllll1l_opy_ = bstack1l11ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡳ࡫ࡸࡵࡡ࡫ࡹࡧࡹࠧᤁ")
bstack11l1llllll1_opy_ = {
  bstack1l11ll1_opy_ (u"ࠫࡨࡸࡩࡵ࡫ࡦࡥࡱ࠭ᤂ"): 50,
  bstack1l11ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᤃ"): 40,
  bstack1l11ll1_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧᤄ"): 30,
  bstack1l11ll1_opy_ (u"ࠧࡪࡰࡩࡳࠬᤅ"): 20,
  bstack1l11ll1_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᤆ"): 10
}
bstack11lllll1l1_opy_ = bstack11l1llllll1_opy_[bstack1l11ll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᤇ")]
bstack1llll11111_opy_ = bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᤈ")
bstack1l1111l11l_opy_ = bstack1l11ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᤉ")
bstack1l1ll11ll_opy_ = bstack1l11ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᤊ")
bstack1l11lll11l_opy_ = bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᤋ")
bstack1l11ll11ll_opy_ = bstack1l11ll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬᤌ")
bstack11l1lllll11_opy_ = [bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩᤍ"), bstack1l11ll1_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩᤎ")]
bstack11l1ll1llll_opy_ = [bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᤏ"), bstack1l11ll1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᤐ")]
bstack1lll11l11l_opy_ = re.compile(bstack1l11ll1_opy_ (u"ࠬࡤ࡛࡝࡞ࡺ࠱ࡢ࠱࠺࠯ࠬࠧࠫᤑ"))
bstack1l1lll1ll1_opy_ = [
  bstack1l11ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡑࡥࡲ࡫ࠧᤒ"),
  bstack1l11ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᤓ"),
  bstack1l11ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᤔ"),
  bstack1l11ll1_opy_ (u"ࠩࡱࡩࡼࡉ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᤕ"),
  bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶࠧᤖ"),
  bstack1l11ll1_opy_ (u"ࠫࡺࡪࡩࡥࠩᤗ"),
  bstack1l11ll1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᤘ"),
  bstack1l11ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࠭ᤙ"),
  bstack1l11ll1_opy_ (u"ࠧࡰࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬᤚ"),
  bstack1l11ll1_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࠭ᤛ"),
  bstack1l11ll1_opy_ (u"ࠩࡱࡳࡗ࡫ࡳࡦࡶࠪᤜ"), bstack1l11ll1_opy_ (u"ࠪࡪࡺࡲ࡬ࡓࡧࡶࡩࡹ࠭ᤝ"),
  bstack1l11ll1_opy_ (u"ࠫࡨࡲࡥࡢࡴࡖࡽࡸࡺࡥ࡮ࡈ࡬ࡰࡪࡹࠧᤞ"),
  bstack1l11ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡘ࡮ࡳࡩ࡯ࡩࡶࠫ᤟"),
  bstack1l11ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࡏࡳ࡬࡭ࡩ࡯ࡩࠪᤠ"),
  bstack1l11ll1_opy_ (u"ࠧࡰࡶ࡫ࡩࡷࡇࡰࡱࡵࠪᤡ"),
  bstack1l11ll1_opy_ (u"ࠨࡲࡵ࡭ࡳࡺࡐࡢࡩࡨࡗࡴࡻࡲࡤࡧࡒࡲࡋ࡯࡮ࡥࡈࡤ࡭ࡱࡻࡲࡦࠩᤢ"),
  bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧᤣ"), bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶࡐࡢࡥ࡮ࡥ࡬࡫ࠧᤤ"), bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡆࡩࡴࡪࡸ࡬ࡸࡾ࠭ᤥ"), bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡖࡡࡤ࡭ࡤ࡫ࡪ࠭ᤦ"), bstack1l11ll1_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡄࡶࡴࡤࡸ࡮ࡵ࡮ࠨᤧ"),
  bstack1l11ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬᤨ"),
  bstack1l11ll1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡔࡦࡵࡷࡔࡦࡩ࡫ࡢࡩࡨࡷࠬᤩ"),
  bstack1l11ll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡆࡳࡻ࡫ࡲࡢࡩࡨࠫᤪ"), bstack1l11ll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࡊࡴࡤࡊࡰࡷࡩࡳࡺࠧᤫ"),
  bstack1l11ll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩ᤬"),
  bstack1l11ll1_opy_ (u"ࠬࡧࡤࡣࡒࡲࡶࡹ࠭᤭"),
  bstack1l11ll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪ࡙࡯ࡤ࡭ࡨࡸࠬ᤮"),
  bstack1l11ll1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡊࡰࡶࡸࡦࡲ࡬ࡕ࡫ࡰࡩࡴࡻࡴࠨ᤯"),
  bstack1l11ll1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡸ࡭࠭ᤰ"),
  bstack1l11ll1_opy_ (u"ࠩࡤࡺࡩ࠭ᤱ"), bstack1l11ll1_opy_ (u"ࠪࡥࡻࡪࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᤲ"), bstack1l11ll1_opy_ (u"ࠫࡦࡼࡤࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᤳ"), bstack1l11ll1_opy_ (u"ࠬࡧࡶࡥࡃࡵ࡫ࡸ࠭ᤴ"),
  bstack1l11ll1_opy_ (u"࠭ࡵࡴࡧࡎࡩࡾࡹࡴࡰࡴࡨࠫᤵ"), bstack1l11ll1_opy_ (u"ࠧ࡬ࡧࡼࡷࡹࡵࡲࡦࡒࡤࡸ࡭࠭ᤶ"), bstack1l11ll1_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡸࡹࡷࡰࡴࡧࠫᤷ"),
  bstack1l11ll1_opy_ (u"ࠩ࡮ࡩࡾࡇ࡬ࡪࡣࡶࠫᤸ"), bstack1l11ll1_opy_ (u"ࠪ࡯ࡪࡿࡐࡢࡵࡶࡻࡴࡸࡤࠨ᤹"),
  bstack1l11ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭᤺"), bstack1l11ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡅࡷ࡭ࡳࠨ᤻"), bstack1l11ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࡅ࡫ࡵࠫ᤼"), bstack1l11ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡉࡨࡳࡱࡰࡩࡒࡧࡰࡱ࡫ࡱ࡫ࡋ࡯࡬ࡦࠩ᤽"), bstack1l11ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡕࡴࡧࡖࡽࡸࡺࡥ࡮ࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࠬ᤾"),
  bstack1l11ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡑࡱࡵࡸࠬ᤿"), bstack1l11ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹࡹࠧ᥀"),
  bstack1l11ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡇ࡭ࡸࡧࡢ࡭ࡧࡅࡹ࡮ࡲࡤࡄࡪࡨࡧࡰ࠭᥁"),
  bstack1l11ll1_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᥂"),
  bstack1l11ll1_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡇࡣࡵ࡫ࡲࡲࠬ᥃"), bstack1l11ll1_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡃࡢࡶࡨ࡫ࡴࡸࡹࠨ᥄"), bstack1l11ll1_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡇ࡮ࡤ࡫ࡸ࠭᥅"), bstack1l11ll1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡣ࡯ࡍࡳࡺࡥ࡯ࡶࡄࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᥆"),
  bstack1l11ll1_opy_ (u"ࠪࡨࡴࡴࡴࡔࡶࡲࡴࡆࡶࡰࡐࡰࡕࡩࡸ࡫ࡴࠨ᥇"),
  bstack1l11ll1_opy_ (u"ࠫࡺࡴࡩࡤࡱࡧࡩࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭᥈"), bstack1l11ll1_opy_ (u"ࠬࡸࡥࡴࡧࡷࡏࡪࡿࡢࡰࡣࡵࡨࠬ᥉"),
  bstack1l11ll1_opy_ (u"࠭࡮ࡰࡕ࡬࡫ࡳ࠭᥊"),
  bstack1l11ll1_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡕ࡯࡫ࡰࡴࡴࡸࡴࡢࡰࡷ࡚࡮࡫ࡷࡴࠩ᥋"),
  bstack1l11ll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱࡨࡷࡵࡩࡥ࡙ࡤࡸࡨ࡮ࡥࡳࡵࠪ᥌"),
  bstack1l11ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᥍"),
  bstack1l11ll1_opy_ (u"ࠪࡶࡪࡩࡲࡦࡣࡷࡩࡈ࡮ࡲࡰ࡯ࡨࡈࡷ࡯ࡶࡦࡴࡖࡩࡸࡹࡩࡰࡰࡶࠫ᥎"),
  bstack1l11ll1_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ᥏"),
  bstack1l11ll1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡒࡤࡸ࡭࠭ᥐ"),
  bstack1l11ll1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡓࡱࡧࡨࡨࠬᥑ"),
  bstack1l11ll1_opy_ (u"ࠧࡨࡲࡶࡉࡳࡧࡢ࡭ࡧࡧࠫᥒ"),
  bstack1l11ll1_opy_ (u"ࠨ࡫ࡶࡌࡪࡧࡤ࡭ࡧࡶࡷࠬᥓ"),
  bstack1l11ll1_opy_ (u"ࠩࡤࡨࡧࡋࡸࡦࡥࡗ࡭ࡲ࡫࡯ࡶࡶࠪᥔ"),
  bstack1l11ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࡖࡧࡷ࡯ࡰࡵࠩᥕ"),
  bstack1l11ll1_opy_ (u"ࠫࡸࡱࡩࡱࡆࡨࡺ࡮ࡩࡥࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨᥖ"),
  bstack1l11ll1_opy_ (u"ࠬࡧࡵࡵࡱࡊࡶࡦࡴࡴࡑࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠬᥗ"),
  bstack1l11ll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡎࡢࡶࡸࡶࡦࡲࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫᥘ"),
  bstack1l11ll1_opy_ (u"ࠧࡴࡻࡶࡸࡪࡳࡐࡰࡴࡷࠫᥙ"),
  bstack1l11ll1_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡦࡥࡌࡴࡹࡴࠨᥚ"),
  bstack1l11ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡕ࡯࡮ࡲࡧࡰ࠭ᥛ"), bstack1l11ll1_opy_ (u"ࠪࡹࡳࡲ࡯ࡤ࡭ࡗࡽࡵ࡫ࠧᥜ"), bstack1l11ll1_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡏࡪࡿࠧᥝ"),
  bstack1l11ll1_opy_ (u"ࠬࡧࡵࡵࡱࡏࡥࡺࡴࡣࡩࠩᥞ"),
  bstack1l11ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡣࡢࡶࡆࡥࡵࡺࡵࡳࡧࠪᥟ"),
  bstack1l11ll1_opy_ (u"ࠧࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࡒࡸ࡭࡫ࡲࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩᥠ"),
  bstack1l11ll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦ࡙࡬ࡲࡩࡵࡷࡂࡰ࡬ࡱࡦࡺࡩࡰࡰࠪᥡ"),
  bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡕࡱࡲࡰࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᥢ"),
  bstack1l11ll1_opy_ (u"ࠪࡩࡳ࡬࡯ࡳࡥࡨࡅࡵࡶࡉ࡯ࡵࡷࡥࡱࡲࠧᥣ"),
  bstack1l11ll1_opy_ (u"ࠫࡪࡴࡳࡶࡴࡨ࡛ࡪࡨࡶࡪࡧࡺࡷࡍࡧࡶࡦࡒࡤ࡫ࡪࡹࠧᥤ"), bstack1l11ll1_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡊࡥࡷࡶࡲࡳࡱࡹࡐࡰࡴࡷࠫᥥ"), bstack1l11ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡊࡥࡵࡣ࡬ࡰࡸࡉ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠩᥦ"),
  bstack1l11ll1_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫ࡁࡱࡲࡶࡇࡦࡩࡨࡦࡎ࡬ࡱ࡮ࡺࠧᥧ"),
  bstack1l11ll1_opy_ (u"ࠨࡥࡤࡰࡪࡴࡤࡢࡴࡉࡳࡷࡳࡡࡵࠩᥨ"),
  bstack1l11ll1_opy_ (u"ࠩࡥࡹࡳࡪ࡬ࡦࡋࡧࠫᥩ"),
  bstack1l11ll1_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪᥪ"),
  bstack1l11ll1_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࡙ࡥࡳࡸ࡬ࡧࡪࡹࡅ࡯ࡣࡥࡰࡪࡪࠧᥫ"), bstack1l11ll1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡂࡷࡷ࡬ࡴࡸࡩࡻࡧࡧࠫᥬ"),
  bstack1l11ll1_opy_ (u"࠭ࡡࡶࡶࡲࡅࡨࡩࡥࡱࡶࡄࡰࡪࡸࡴࡴࠩᥭ"), bstack1l11ll1_opy_ (u"ࠧࡢࡷࡷࡳࡉ࡯ࡳ࡮࡫ࡶࡷࡆࡲࡥࡳࡶࡶࠫ᥮"),
  bstack1l11ll1_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡊࡰࡶࡸࡷࡻ࡭ࡦࡰࡷࡷࡑ࡯ࡢࠨ᥯"),
  bstack1l11ll1_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦ࡙ࡧࡰࠨᥰ"),
  bstack1l11ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌࡲ࡮ࡺࡩࡢ࡮ࡘࡶࡱ࠭ᥱ"), bstack1l11ll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡅࡱࡲ࡯ࡸࡒࡲࡴࡺࡶࡳࠨᥲ"), bstack1l11ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎ࡭࡮ࡰࡴࡨࡊࡷࡧࡵࡥ࡙ࡤࡶࡳ࡯࡮ࡨࠩᥳ"), bstack1l11ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡦࡰࡏ࡭ࡳࡱࡳࡊࡰࡅࡥࡨࡱࡧࡳࡱࡸࡲࡩ࠭ᥴ"),
  bstack1l11ll1_opy_ (u"ࠧ࡬ࡧࡨࡴࡐ࡫ࡹࡄࡪࡤ࡭ࡳࡹࠧ᥵"),
  bstack1l11ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡻࡣࡥࡰࡪ࡙ࡴࡳ࡫ࡱ࡫ࡸࡊࡩࡳࠩ᥶"),
  bstack1l11ll1_opy_ (u"ࠩࡳࡶࡴࡩࡥࡴࡵࡄࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᥷"),
  bstack1l11ll1_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡍࡨࡽࡉ࡫࡬ࡢࡻࠪ᥸"),
  bstack1l11ll1_opy_ (u"ࠫࡸ࡮࡯ࡸࡋࡒࡗࡑࡵࡧࠨ᥹"),
  bstack1l11ll1_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧ᥺"),
  bstack1l11ll1_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡘࡥࡴࡲࡲࡲࡸ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧ᥻"), bstack1l11ll1_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷ࡛ࡦ࡯ࡴࡕ࡫ࡰࡩࡴࡻࡴࠨ᥼"),
  bstack1l11ll1_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࠫ᥽"),
  bstack1l11ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡶࡽࡳࡩࡅࡹࡧࡦࡹࡹ࡫ࡆࡳࡱࡰࡌࡹࡺࡰࡴࠩ᥾"),
  bstack1l11ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡇࡦࡶࡴࡶࡴࡨࠫ᥿"),
  bstack1l11ll1_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫᦀ"),
  bstack1l11ll1_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡆࡳࡳࡺࡥࡹࡶࡏ࡭ࡸࡺࠧᦁ"),
  bstack1l11ll1_opy_ (u"࠭ࡷࡢ࡫ࡷࡊࡴࡸࡁࡱࡲࡖࡧࡷ࡯ࡰࡵࠩᦂ"),
  bstack1l11ll1_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡄࡱࡱࡲࡪࡩࡴࡓࡧࡷࡶ࡮࡫ࡳࠨᦃ"),
  bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴࡓࡧ࡭ࡦࠩᦄ"),
  bstack1l11ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡖࡐࡈ࡫ࡲࡵࠩᦅ"),
  bstack1l11ll1_opy_ (u"ࠪࡸࡦࡶࡗࡪࡶ࡫ࡗ࡭ࡵࡲࡵࡒࡵࡩࡸࡹࡄࡶࡴࡤࡸ࡮ࡵ࡮ࠨᦆ"),
  bstack1l11ll1_opy_ (u"ࠫࡸࡩࡡ࡭ࡧࡉࡥࡨࡺ࡯ࡳࠩᦇ"),
  bstack1l11ll1_opy_ (u"ࠬࡽࡤࡢࡎࡲࡧࡦࡲࡐࡰࡴࡷࠫᦈ"),
  bstack1l11ll1_opy_ (u"࠭ࡳࡩࡱࡺ࡜ࡨࡵࡤࡦࡎࡲ࡫ࠬᦉ"),
  bstack1l11ll1_opy_ (u"ࠧࡪࡱࡶࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡻࡳࡦࠩᦊ"),
  bstack1l11ll1_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡃࡰࡰࡩ࡭࡬ࡌࡩ࡭ࡧࠪᦋ"),
  bstack1l11ll1_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡹࡳࡸࡱࡵࡨࠬᦌ"),
  bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡐࡳࡧࡥࡹ࡮ࡲࡴࡘࡆࡄࠫᦍ"),
  bstack1l11ll1_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸ࡜ࡊࡁࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠬᦎ"),
  bstack1l11ll1_opy_ (u"ࠬࡽࡥࡣࡆࡵ࡭ࡻ࡫ࡲࡂࡩࡨࡲࡹ࡛ࡲ࡭ࠩᦏ"),
  bstack1l11ll1_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡷ࡬ࠬᦐ"),
  bstack1l11ll1_opy_ (u"ࠧࡶࡵࡨࡒࡪࡽࡗࡅࡃࠪᦑ"),
  bstack1l11ll1_opy_ (u"ࠨࡹࡧࡥࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫᦒ"), bstack1l11ll1_opy_ (u"ࠩࡺࡨࡦࡉ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࡖ࡬ࡱࡪࡵࡵࡵࠩᦓ"),
  bstack1l11ll1_opy_ (u"ࠪࡼࡨࡵࡤࡦࡑࡵ࡫ࡎࡪࠧᦔ"), bstack1l11ll1_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡖ࡭࡬ࡴࡩ࡯ࡩࡌࡨࠬᦕ"),
  bstack1l11ll1_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩ࡝ࡄࡂࡄࡸࡲࡩࡲࡥࡊࡦࠪᦖ"),
  bstack1l11ll1_opy_ (u"࠭ࡲࡦࡵࡨࡸࡔࡴࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡵࡸࡔࡴ࡬ࡺࠩᦗ"),
  bstack1l11ll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࡴࠩᦘ"),
  bstack1l11ll1_opy_ (u"ࠨࡹࡧࡥࡘࡺࡡࡳࡶࡸࡴࡗ࡫ࡴࡳ࡫ࡨࡷࠬᦙ"), bstack1l11ll1_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴࡼࡍࡳࡺࡥࡳࡸࡤࡰࠬᦚ"),
  bstack1l11ll1_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࡌࡦࡸࡤࡸࡣࡵࡩࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ᦛ"),
  bstack1l11ll1_opy_ (u"ࠫࡲࡧࡸࡕࡻࡳ࡭ࡳ࡭ࡆࡳࡧࡴࡹࡪࡴࡣࡺࠩᦜ"),
  bstack1l11ll1_opy_ (u"ࠬࡹࡩ࡮ࡲ࡯ࡩࡎࡹࡖࡪࡵ࡬ࡦࡱ࡫ࡃࡩࡧࡦ࡯ࠬᦝ"),
  bstack1l11ll1_opy_ (u"࠭ࡵࡴࡧࡆࡥࡷࡺࡨࡢࡩࡨࡗࡸࡲࠧᦞ"),
  bstack1l11ll1_opy_ (u"ࠧࡴࡪࡲࡹࡱࡪࡕࡴࡧࡖ࡭ࡳ࡭࡬ࡦࡶࡲࡲ࡙࡫ࡳࡵࡏࡤࡲࡦ࡭ࡥࡳࠩᦟ"),
  bstack1l11ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡉࡘࡆࡓࠫᦠ"),
  bstack1l11ll1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡱࡸࡧ࡭ࡏࡤࡆࡰࡵࡳࡱࡲࠧᦡ"),
  bstack1l11ll1_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡋ࡭ࡩࡪࡥ࡯ࡃࡳ࡭ࡕࡵ࡬ࡪࡥࡼࡉࡷࡸ࡯ࡳࠩᦢ"),
  bstack1l11ll1_opy_ (u"ࠫࡲࡵࡣ࡬ࡎࡲࡧࡦࡺࡩࡰࡰࡄࡴࡵ࠭ᦣ"),
  bstack1l11ll1_opy_ (u"ࠬࡲ࡯ࡨࡥࡤࡸࡋࡵࡲ࡮ࡣࡷࠫᦤ"), bstack1l11ll1_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌࡩ࡭ࡶࡨࡶࡘࡶࡥࡤࡵࠪᦥ"),
  bstack1l11ll1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡊࡥ࡭ࡣࡼࡅࡩࡨࠧᦦ"),
  bstack1l11ll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡋࡧࡐࡴࡩࡡࡵࡱࡵࡅࡺࡺ࡯ࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠫᦧ")
]
bstack1l1111ll11_opy_ = bstack1l11ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡷࡳࡰࡴࡧࡤࠨᦨ")
bstack11111l11_opy_ = [bstack1l11ll1_opy_ (u"ࠪ࠲ࡦࡶ࡫ࠨᦩ"), bstack1l11ll1_opy_ (u"ࠫ࠳ࡧࡡࡣࠩᦪ"), bstack1l11ll1_opy_ (u"ࠬ࠴ࡩࡱࡣࠪᦫ")]
bstack11lll11l11_opy_ = [bstack1l11ll1_opy_ (u"࠭ࡩࡥࠩ᦬"), bstack1l11ll1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ᦭"), bstack1l11ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ᦮"), bstack1l11ll1_opy_ (u"ࠩࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤࠨ᦯")]
bstack1ll1lll1ll_opy_ = {
  bstack1l11ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᦰ"): bstack1l11ll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᦱ"),
  bstack1l11ll1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦲ"): bstack1l11ll1_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᦳ"),
  bstack1l11ll1_opy_ (u"ࠧࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬᦴ"): bstack1l11ll1_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᦵ"),
  bstack1l11ll1_opy_ (u"ࠩ࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬᦶ"): bstack1l11ll1_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᦷ"),
  bstack1l11ll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵࡺࡩࡰࡰࡶࠫᦸ"): bstack1l11ll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᦹ")
}
bstack1ll1l11lll_opy_ = [
  bstack1l11ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᦺ"),
  bstack1l11ll1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬᦻ"),
  bstack1l11ll1_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᦼ"),
  bstack1l11ll1_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᦽ"),
  bstack1l11ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫᦾ"),
]
bstack1111lll11_opy_ = bstack1ll11lll1_opy_ + bstack11l1lll11l1_opy_ + bstack1l1lll1ll1_opy_
bstack11l11l1lll_opy_ = [
  bstack1l11ll1_opy_ (u"ࠫࡣࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴࠥࠩᦿ"),
  bstack1l11ll1_opy_ (u"ࠬࡤࡢࡴ࠯࡯ࡳࡨࡧ࡬࠯ࡥࡲࡱࠩ࠭ᧀ"),
  bstack1l11ll1_opy_ (u"࠭࡞࠲࠴࠺࠲ࠬᧁ"),
  bstack1l11ll1_opy_ (u"ࠧ࡟࠳࠳࠲ࠬᧂ"),
  bstack1l11ll1_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠱࡜࠸࠰࠽ࡢ࠴ࠧᧃ"),
  bstack1l11ll1_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠳࡝࠳࠱࠾ࡣ࠮ࠨᧄ"),
  bstack1l11ll1_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠵࡞࠴࠲࠷࡝࠯ࠩᧅ"),
  bstack1l11ll1_opy_ (u"ࠫࡣ࠷࠹࠳࠰࠴࠺࠽࠴ࠧᧆ")
]
bstack11ll11l11l1_opy_ = bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᧇ")
bstack11l1l11lll_opy_ = bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࠲ࡺ࠶࠵ࡥࡷࡧࡱࡸࠬᧈ")
bstack1lll1l1l_opy_ = [ bstack1l11ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᧉ") ]
bstack11ll111lll_opy_ = [ bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᧊") ]
bstack111l1ll1_opy_ = [bstack1l11ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭᧋")]
bstack1l1l11111_opy_ = [ bstack1l11ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᧌") ]
bstack11ll1111ll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡘࡊࡋࡔࡧࡷࡹࡵ࠭᧍")
bstack11ll1111l_opy_ = bstack1l11ll1_opy_ (u"࡙ࠬࡄࡌࡖࡨࡷࡹࡇࡴࡵࡧࡰࡴࡹ࡫ࡤࠨ᧎")
bstack1l1111l1l1_opy_ = bstack1l11ll1_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠪ᧏")
bstack1ll1l11l1_opy_ = bstack1l11ll1_opy_ (u"ࠧ࠵࠰࠳࠲࠵࠭᧐")
bstack1ll11ll1_opy_ = [
  bstack1l11ll1_opy_ (u"ࠨࡇࡕࡖࡤࡌࡁࡊࡎࡈࡈࠬ᧑"),
  bstack1l11ll1_opy_ (u"ࠩࡈࡖࡗࡥࡔࡊࡏࡈࡈࡤࡕࡕࡕࠩ᧒"),
  bstack1l11ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡃࡎࡒࡇࡐࡋࡄࡠࡄ࡜ࡣࡈࡒࡉࡆࡐࡗࠫ᧓"),
  bstack1l11ll1_opy_ (u"ࠫࡊࡘࡒࡠࡐࡈࡘ࡜ࡕࡒࡌࡡࡆࡌࡆࡔࡇࡆࡆࠪ᧔"),
  bstack1l11ll1_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡅࡕࡡࡑࡓ࡙ࡥࡃࡐࡐࡑࡉࡈ࡚ࡅࡅࠩ᧕"),
  bstack1l11ll1_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡄࡎࡒࡗࡊࡊࠧ᧖"),
  bstack1l11ll1_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡔࡈࡗࡊ࡚ࠧ᧗"),
  bstack1l11ll1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡋ࡛ࡓࡆࡆࠪ᧘"),
  bstack1l11ll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡅࡇࡕࡒࡕࡇࡇࠫ᧙"),
  bstack1l11ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫ᧚"),
  bstack1l11ll1_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡎࡐࡖࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࠬ᧛"),
  bstack1l11ll1_opy_ (u"ࠬࡋࡒࡓࡡࡄࡈࡉࡘࡅࡔࡕࡢࡍࡓ࡜ࡁࡍࡋࡇࠫ᧜"),
  bstack1l11ll1_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣ࡚ࡔࡒࡆࡃࡆࡌࡆࡈࡌࡆࠩ᧝"),
  bstack1l11ll1_opy_ (u"ࠧࡆࡔࡕࡣ࡙࡛ࡎࡏࡇࡏࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨ᧞"),
  bstack1l11ll1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡗࡍࡒࡋࡄࡠࡑࡘࡘࠬ᧟"),
  bstack1l11ll1_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡗࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ᧠"),
  bstack1l11ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡌࡔ࡙ࡔࡠࡗࡑࡖࡊࡇࡃࡉࡃࡅࡐࡊ࠭᧡"),
  bstack1l11ll1_opy_ (u"ࠫࡊࡘࡒࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫ᧢"),
  bstack1l11ll1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭᧣"),
  bstack1l11ll1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡔࡈࡗࡔࡒࡕࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ᧤"),
  bstack1l11ll1_opy_ (u"ࠧࡆࡔࡕࡣࡒࡇࡎࡅࡃࡗࡓࡗ࡟࡟ࡑࡔࡒ࡜࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭᧥"),
]
bstack11l1ll111l_opy_ = bstack1l11ll1_opy_ (u"ࠨ࠰࠲ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡤࡶࡹ࡯ࡦࡢࡥࡷࡷ࠴࠭᧦")
bstack1l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠩࢁࠫ᧧")), bstack1l11ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᧨"), bstack1l11ll1_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ᧩"))
bstack11ll1llll11_opy_ = bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴ࡮࠭᧪")
bstack11l1lllll1l_opy_ = [ bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᧫"), bstack1l11ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭᧬"), bstack1l11ll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ᧭"), bstack1l11ll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ᧮")]
bstack1llll11ll1_opy_ = [ bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᧯"), bstack1l11ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ᧰"), bstack1l11ll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ᧱"), bstack1l11ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭᧲") ]
bstack1lll1llll1_opy_ = [ bstack1l11ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭᧳") ]
bstack11l1l1ll11l_opy_ = [ bstack1l11ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᧴") ]
bstack1llll111l_opy_ = 360
bstack11ll111llll_opy_ = bstack1l11ll1_opy_ (u"ࠤࡤࡴࡵ࠳ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ᧵")
bstack11l1ll1l1l1_opy_ = bstack1l11ll1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴࡯ࡳࡴࡷࡨࡷࠧ᧶")
bstack11l1lll1l11_opy_ = bstack1l11ll1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠢ᧷")
bstack11ll1ll1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠧࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡴࡦࡵࡷࡷࠥࡧࡲࡦࠢࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡵ࡮ࠡࡑࡖࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࠫࡳࠡࡣࡱࡨࠥࡧࡢࡰࡸࡨࠤ࡫ࡵࡲࠡࡃࡱࡨࡷࡵࡩࡥࠢࡧࡩࡻ࡯ࡣࡦࡵ࠱ࠦ᧸")
bstack11lll11111l_opy_ = bstack1l11ll1_opy_ (u"ࠨ࠱࠲࠰࠳ࠦ᧹")
bstack111l11llll_opy_ = {
  bstack1l11ll1_opy_ (u"ࠧࡑࡃࡖࡗࠬ᧺"): bstack1l11ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᧻"),
  bstack1l11ll1_opy_ (u"ࠩࡉࡅࡎࡒࠧ᧼"): bstack1l11ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᧽"),
  bstack1l11ll1_opy_ (u"ࠫࡘࡑࡉࡑࠩ᧾"): bstack1l11ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᧿")
}
bstack111l1ll11_opy_ = [
  bstack1l11ll1_opy_ (u"ࠨࡧࡦࡶࠥᨀ"),
  bstack1l11ll1_opy_ (u"ࠢࡨࡱࡅࡥࡨࡱࠢᨁ"),
  bstack1l11ll1_opy_ (u"ࠣࡩࡲࡊࡴࡸࡷࡢࡴࡧࠦᨂ"),
  bstack1l11ll1_opy_ (u"ࠤࡵࡩ࡫ࡸࡥࡴࡪࠥᨃ"),
  bstack1l11ll1_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤᨄ"),
  bstack1l11ll1_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᨅ"),
  bstack1l11ll1_opy_ (u"ࠧࡹࡵࡣ࡯࡬ࡸࡊࡲࡥ࡮ࡧࡱࡸࠧᨆ"),
  bstack1l11ll1_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥᨇ"),
  bstack1l11ll1_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡅࡨࡺࡩࡷࡧࡈࡰࡪࡳࡥ࡯ࡶࠥᨈ"),
  bstack1l11ll1_opy_ (u"ࠣࡥ࡯ࡩࡦࡸࡅ࡭ࡧࡰࡩࡳࡺࠢᨉ"),
  bstack1l11ll1_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࡵࠥᨊ"),
  bstack1l11ll1_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠥᨋ"),
  bstack1l11ll1_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡆࡹࡹ࡯ࡥࡖࡧࡷ࡯ࡰࡵࠤᨌ"),
  bstack1l11ll1_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦᨍ"),
  bstack1l11ll1_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᨎ"),
  bstack1l11ll1_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡕࡱࡸࡧ࡭ࡇࡣࡵ࡫ࡲࡲࠧᨏ"),
  bstack1l11ll1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡏࡸࡰࡹ࡯ࡔࡰࡷࡦ࡬ࠧᨐ"),
  bstack1l11ll1_opy_ (u"ࠤࡶ࡬ࡦࡱࡥࠣᨑ"),
  bstack1l11ll1_opy_ (u"ࠥࡧࡱࡵࡳࡦࡃࡳࡴࠧᨒ")
]
bstack11l1llll111_opy_ = [
  bstack1l11ll1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥᨓ"),
  bstack1l11ll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᨔ"),
  bstack1l11ll1_opy_ (u"ࠨࡡࡶࡶࡲࠦᨕ"),
  bstack1l11ll1_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢᨖ"),
  bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᨗ")
]
bstack111ll11l1_opy_ = {
  bstack1l11ll1_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ᨘࠣ"): [bstack1l11ll1_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤᨙ")],
  bstack1l11ll1_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᨚ"): [bstack1l11ll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᨛ")],
  bstack1l11ll1_opy_ (u"ࠨࡡࡶࡶࡲࠦ᨜"): [bstack1l11ll1_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦ᨝"), bstack1l11ll1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦ᨞"), bstack1l11ll1_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ᨟"), bstack1l11ll1_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤᨠ")],
  bstack1l11ll1_opy_ (u"ࠦࡲࡧ࡮ࡶࡣ࡯ࠦᨡ"): [bstack1l11ll1_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧᨢ")],
  bstack1l11ll1_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᨣ"): [bstack1l11ll1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᨤ")],
}
bstack11l1lll111l_opy_ = {
  bstack1l11ll1_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢᨥ"): bstack1l11ll1_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࠣᨦ"),
  bstack1l11ll1_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᨧ"): bstack1l11ll1_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᨨ"),
  bstack1l11ll1_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡇ࡯ࡩࡲ࡫࡮ࡵࠤᨩ"): bstack1l11ll1_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࠣᨪ"),
  bstack1l11ll1_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡅࡨࡺࡩࡷࡧࡈࡰࡪࡳࡥ࡯ࡶࠥᨫ"): bstack1l11ll1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࠥᨬ"),
  bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᨭ"): bstack1l11ll1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᨮ")
}
bstack111l1l11l1_opy_ = {
  bstack1l11ll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᨯ"): bstack1l11ll1_opy_ (u"࡙ࠬࡵࡪࡶࡨࠤࡘ࡫ࡴࡶࡲࠪᨰ"),
  bstack1l11ll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᨱ"): bstack1l11ll1_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࠦࡔࡦࡣࡵࡨࡴࡽ࡮ࠨᨲ"),
  bstack1l11ll1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᨳ"): bstack1l11ll1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡔࡧࡷࡹࡵ࠭ᨴ"),
  bstack1l11ll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᨵ"): bstack1l11ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡗࡩࡦࡸࡤࡰࡹࡱࠫᨶ")
}
bstack11l1ll11ll1_opy_ = 65536
bstack11l1ll11lll_opy_ = bstack1l11ll1_opy_ (u"ࠬ࠴࠮࠯࡝ࡗࡖ࡚ࡔࡃࡂࡖࡈࡈࡢ࠭ᨷ")
bstack11l1lll1lll_opy_ = [
      bstack1l11ll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᨸ"), bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᨹ"), bstack1l11ll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᨺ"), bstack1l11ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᨻ"), bstack1l11ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬᨼ"),
      bstack1l11ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᨽ"), bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨᨾ"), bstack1l11ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᨿ"), bstack1l11ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨᩀ"),
      bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᩁ"), bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᩂ"), bstack1l11ll1_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ᩃ")
    ]
bstack11l1ll1l111_opy_= {
  bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᩄ"): bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᩅ"),
  bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪᩆ"): bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᩇ"),
  bstack1l11ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᩈ"): bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩉ"),
  bstack1l11ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᩊ"): bstack1l11ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᩋ"),
  bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᩌ"): bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᩍ"),
  bstack1l11ll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᩎ"): bstack1l11ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᩏ"),
  bstack1l11ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᩐ"): bstack1l11ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᩑ"),
  bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᩒ"): bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᩓ"),
  bstack1l11ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᩔ"): bstack1l11ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᩕ"),
  bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩖ"): bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧᩗ"),
  bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᩘ"): bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᩙ"),
  bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࠬᩚ"): bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭ᩛ"),
  bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᩜ"): bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᩝ"),
  bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩞ"): bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࡒࡴࡹ࡯࡯࡯ࡵࠪ᩟"),
  bstack1l11ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ᩠࠭"): bstack1l11ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧᩡ"),
  bstack1l11ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᩢ"): bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᩣ"),
  bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᩤ"): bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᩥ"),
  bstack1l11ll1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧᩦ"): bstack1l11ll1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᩧ"),
  bstack1l11ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᩨ"): bstack1l11ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᩩ"),
  bstack1l11ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩪ"): bstack1l11ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᩫ"),
  bstack1l11ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᩬ"): bstack1l11ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ᩭ"),
  bstack1l11ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᩮ"): bstack1l11ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᩯ"),
  bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᩰ"): bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᩱ"),
  bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᩲ"): bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩳ"),
  bstack1l11ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᩴ"): bstack1l11ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᩵"),
  bstack1l11ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᩶"): bstack1l11ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᩷"),
  bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ᩸"): bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ᩹"),
  bstack1l11ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩ᩺"): bstack1l11ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ᩻")
}
bstack11l1llll1ll_opy_ = [bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᩼"), bstack1l11ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ᩽")]
bstack11l11lllll_opy_ = (bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨ᩾"),)
bstack11l1lll11ll_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡶࡲࡧࡥࡹ࡫࡟ࡤ࡮࡬᩿ࠫ")
bstack1l1l1ll11_opy_ = bstack1l11ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳࡬ࡸࡩࡥࡵ࠲ࠦ᪀")
bstack1l1ll1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫ࡷ࡯ࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡧࡳࡩࡤࡲࡥࡷࡪ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࠣ᪁")
bstack1l1111l111_opy_ = bstack1l11ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠦ᪂")
class EVENTS(Enum):
  bstack11l1l1ll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡱ࠴࠵ࡾࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨ᪃")
  bstack1lll1ll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰࡪࡧ࡮ࡶࡲࠪ᪄") # final bstack11l1lll1ll1_opy_
  bstack11l1ll1ll11_opy_ = bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡴࡤ࡭ࡱࡪࡷࠬ᪅")
  bstack11ll1l1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪ᪆") #shift post bstack11l1lll1111_opy_
  bstack1ll1111111_opy_ = bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩ᪇") #shift post bstack11l1lll1111_opy_
  bstack11l1ll11111_opy_ = bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡀࡴࡦࡵࡷ࡬ࡺࡨࠧ᪈") #shift
  bstack11l1llll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨ᪉") #shift
  bstack1lll1l1111_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠿࡮ࡵࡣ࠯ࡰࡥࡳࡧࡧࡦ࡯ࡨࡲࡹ࠭᪊")
  bstack1ll111l1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡴࡣࡹࡩ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭᪋")
  bstack1l1l1l1ll_opy_ = bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡦࡵ࡭ࡻ࡫ࡲ࠮ࡲࡨࡶ࡫ࡵࡲ࡮ࡵࡦࡥࡳ࠭᪌")
  bstack1l11l111l1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀ࡬ࡰࡥࡤࡰࠬ᪍") #shift
  bstack1ll1l1llll_opy_ = bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡦࡶࡰ࠮ࡷࡳࡰࡴࡧࡤࠨ᪎") #shift
  bstack1l1l1l1l11_opy_ = bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡥ࡬࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹࠧ᪏")
  bstack111l1lll1_opy_ = bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠫ᪐") #shift
  bstack1ll11l1111_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡧࡦࡶ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠰ࡶࡪࡹࡵ࡭ࡶࡶࠫ᪑") #shift
  bstack11l1ll1l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹࠨ᪒") #shift
  bstack1l1l11lll11_opy_ = bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭᪓")
  bstack1llll1111_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭ࡴࡶࡤࡸࡺࡹࠧ᪔") #shift
  bstack11llll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨ᪕")
  bstack11l1ll1lll1_opy_ = bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡱࡻࡽ࠲ࡹࡥࡵࡷࡳࠫ᪖") #shift
  bstack1l111lll_opy_ = bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡷࡹࡵ࠭᪗")
  bstack11l1ll1ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡴࡰࡤࡴࡸ࡮࡯ࡵࠩ᪘") # not bstack11l1ll111l1_opy_ in python
  bstack1ll1llll1_opy_ = bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡴࡹ࡮ࡺࠧ᪙") # used in bstack11l1l1lllll_opy_
  bstack1l1111l1l_opy_ = bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽࡫ࡪࡺࠧ᪚") # used in bstack11l1l1lllll_opy_
  bstack1l111ll1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠾࡭ࡵ࡯࡬ࠩ᪛")
  bstack11l1l1l11l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪ࠭᪜")
  bstack11l111ll11_opy_ = bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳ࠭᪝") #
  bstack1ll11l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡰ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡺࡡ࡬ࡧࡖࡧࡷ࡫ࡥ࡯ࡕ࡫ࡳࡹ࠭᪞")
  bstack1lll1lll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡢࡷࡷࡳ࠲ࡩࡡࡱࡶࡸࡶࡪ࠭᪟")
  bstack11111l11l_opy_ = bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡴࡦࡵࡷࠫ᪠")
  bstack1ll111l1l1_opy_ = bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡶࡨࡷࡹ࠭᪡")
  bstack1111111l_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡸࡥ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ᪢") #shift
  bstack11l1l1ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫ᪣") #shift
  bstack11l1ll11l1l_opy_ = bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬ᪤")
  bstack11l1ll1111l_opy_ = bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡬ࡨࡱ࡫࠭ࡵ࡫ࡰࡩࡴࡻࡴࠨ᪥")
  bstack1lll11ll1ll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡹࡴࡢࡴࡷࠫ᪦")
  bstack11l1ll1l11l_opy_ = bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨᪧ")
  bstack11l1llll11l_opy_ = bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡤࡪࡨࡧࡰ࠳ࡵࡱࡦࡤࡸࡪ࠭᪨")
  bstack1lll11lll1l_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠧ᪩")
  bstack1lll11lll11_opy_ = bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡩ࡯࡯ࡰࡨࡧࡹ࠭᪪")
  bstack1lll11l11l1_opy_ = bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡳࡵࡱࡳࠫ᪫")
  bstack1lll1llll1l_opy_ = bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡶࡤࡶࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩ᪬")
  bstack1llll11ll11_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡥࡲࡲࡳ࡫ࡣࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲࠬ᪭")
  bstack11l1ll11l11_opy_ = bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹ࠭᪮")
  bstack11l1l1l1lll_opy_ = bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡪ࡮ࡴࡤࡏࡧࡤࡶࡪࡹࡴࡉࡷࡥࠫ᪯")
  bstack1l11ll11l11_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡌࡲ࡮ࡺࠧ᪰")
  bstack1l11l1ll1ll_opy_ = bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡲࡵࠩ᪱")
  bstack1ll11l1llll_opy_ = bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡉ࡯࡯ࡨ࡬࡫ࠬ᪲")
  bstack11l1l1ll111_opy_ = bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡃࡰࡰࡩ࡭࡬࠭᪳")
  bstack1ll111111ll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࡬ࡗࡪࡲࡦࡉࡧࡤࡰࡘࡺࡥࡱࠩ᪴")
  bstack1l1lllllll1_opy_ = bstack1l11ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࡭ࡘ࡫࡬ࡧࡊࡨࡥࡱࡍࡥࡵࡔࡨࡷࡺࡲࡴࠨ᪵")
  bstack1l1ll1111l1_opy_ = bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡈࡺࡪࡴࡴࠨ᪶")
  bstack1l1ll1l11l1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺ᪷ࠧ")
  bstack1l1l1l1ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼࡯ࡳ࡬ࡉࡲࡦࡣࡷࡩࡩࡋࡶࡦࡰࡷ᪸ࠫ")
  bstack11l1l1lll11_opy_ = bstack1l11ll1_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡩࡳࡷࡵࡦࡷࡨࡘࡪࡹࡴࡆࡸࡨࡲࡹ᪹࠭")
  bstack1l11ll1111l_opy_ = bstack1l11ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡰࡲ᪺ࠪ")
  bstack1ll1ll1l11l_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡱࡱࡗࡹࡵࡰࠨ᪻")
class STAGE(Enum):
  bstack1l1lll11ll_opy_ = bstack1l11ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫ᪼")
  END = bstack1l11ll1_opy_ (u"࠭ࡥ࡯ࡦ᪽ࠪ")
  bstack11lllll111_opy_ = bstack1l11ll1_opy_ (u"ࠧࡴ࡫ࡱ࡫ࡱ࡫ࠧ᪾")
bstack1111ll111_opy_ = {
  bstack1l11ll1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࠨᪿ"): bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵᫀࠩ"),
  bstack1l11ll1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ᫁"): bstack1l11ll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭᫂")
}
PLAYWRIGHT_HUB_URL = bstack1l11ll1_opy_ (u"ࠧࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃ᫃ࠢ")
bstack1ll11ll11ll_opy_ = 98
bstack1ll111l1ll1_opy_ = 100
bstack1111l1l11l_opy_ = {
  bstack1l11ll1_opy_ (u"࠭ࡲࡦࡴࡸࡲ᫄ࠬ"): bstack1l11ll1_opy_ (u"ࠧ࠮࠯ࡵࡩࡷࡻ࡮ࡴࠩ᫅"),
  bstack1l11ll1_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧ᫆"): bstack1l11ll1_opy_ (u"ࠩ࠰࠱ࡷ࡫ࡲࡶࡰࡶ࠱ࡩ࡫࡬ࡢࡻࠪ᫇"),
  bstack1l11ll1_opy_ (u"ࠪࡶࡪࡸࡵ࡯࠯ࡧࡩࡱࡧࡹࠨ᫈"): 0
}
bstack11l1l1ll1ll_opy_ = bstack1l11ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦ᫉")
bstack11l1ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡵࡱ࡮ࡲࡥࡩ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ᫊")
bstack1l111l111l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡔࡆࡕࡗࠤࡗࡋࡐࡐࡔࡗࡍࡓࡍࠠࡂࡐࡇࠤࡆࡔࡁࡍ࡛ࡗࡍࡈ࡙ࠢ᫋")