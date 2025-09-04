# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import re
from enum import Enum
bstack1lll11ll11_opy_ = {
  bstack1111l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩធ"): bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࠬន"),
  bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬប"): bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡮ࡩࡾ࠭ផ"),
  bstack1111l1l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧព"): bstack1111l1l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩភ"),
  bstack1111l1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ម"): bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧយ"),
  bstack1111l1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭រ"): bstack1111l1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࠪល"),
  bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭វ"): bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪឝ"),
  bstack1111l1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪឞ"): bstack1111l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫស"),
  bstack1111l1l_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ហ"): bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠭ឡ"),
  bstack1111l1l_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧអ"): bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡳࡹ࡯࡭ࡧࠪឣ"),
  bstack1111l1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩឤ"): bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩឥ"),
  bstack1111l1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪឦ"): bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪឧ"),
  bstack1111l1l_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧឨ"): bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡸ࡬ࡨࡪࡵࠧឩ"),
  bstack1111l1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩឪ"): bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩឫ"),
  bstack1111l1l_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬឬ"): bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬឭ"),
  bstack1111l1l_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬឮ"): bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬឯ"),
  bstack1111l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫឰ"): bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫឱ"),
  bstack1111l1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ឲ"): bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧឳ"),
  bstack1111l1l_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬ឴"): bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬ឵"),
  bstack1111l1l_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ា"): bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ិ"),
  bstack1111l1l_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪី"): bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪឹ"),
  bstack1111l1l_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧឺ"): bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡯ࡦࡎࡩࡾࡹࠧុ"),
  bstack1111l1l_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩូ"): bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳ࡜ࡧࡩࡵࠩួ"),
  bstack1111l1l_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨើ"): bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡳࠨឿ"),
  bstack1111l1l_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬៀ"): bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧ࡬ࡣࡢࡥ࡫ࡩࠬេ"),
  bstack1111l1l_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧែ"): bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧៃ"),
  bstack1111l1l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫោ"): bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫៅ"),
  bstack1111l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧំ"): bstack1111l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫះ"),
  bstack1111l1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩៈ"): bstack1111l1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫ៉"),
  bstack1111l1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ៊"): bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ់"),
  bstack1111l1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩ៌"): bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩ៍"),
  bstack1111l1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬ៎"): bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬ៏"),
  bstack1111l1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬ័"): bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨ៑"),
  bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍ្ࠪ"): bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ៓"),
  bstack1111l1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ។"): bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡴࡻࡲࡤࡧࠪ៕"),
  bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ៖"): bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧៗ"),
  bstack1111l1l_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩ៘"): bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡓࡧ࡭ࡦࠩ៙"),
  bstack1111l1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬ៚"): bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬ៛"),
  bstack1111l1l_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨៜ"): bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨ៝"),
  bstack1111l1l_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫ៞"): bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫ៟"),
  bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ០"): bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ១"),
  bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ២"): bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ៣")
}
bstack11l1lll11ll_opy_ = [
  bstack1111l1l_opy_ (u"ࠬࡵࡳࠨ៤"),
  bstack1111l1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ៥"),
  bstack1111l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ៦"),
  bstack1111l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭៧"),
  bstack1111l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭៨"),
  bstack1111l1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ៩"),
  bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ៪"),
]
bstack11lll1l1_opy_ = {
  bstack1111l1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ៫"): [bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ៬"), bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡓࡇࡍࡆࠩ៭")],
  bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ៮"): bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ៯"),
  bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭៰"): bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠧ៱"),
  bstack1111l1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ៲"): bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠫ៳"),
  bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ៴"): bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ៵"),
  bstack1111l1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ៶"): bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡗࡤࡖࡅࡓࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫ៷"),
  bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ៸"): bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࠪ៹"),
  bstack1111l1l_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪ៺"): bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ៻"),
  bstack1111l1l_opy_ (u"ࠨࡣࡳࡴࠬ៼"): [bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡓࡔࡤࡏࡄࠨ៽"), bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕ࠭៾")],
  bstack1111l1l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭៿"): bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡎࡒࡋࡑࡋࡖࡆࡎࠪ᠀"),
  bstack1111l1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᠁"): bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ᠂"),
  bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᠃"): [bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞࠭᠄"), bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ᠅")],
  bstack1111l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᠆"): bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙࡛ࡒࡃࡑࡖࡇࡆࡒࡅࠨ᠇")
}
bstack1lll11l1l_opy_ = {
  bstack1111l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ᠈"): [bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡣࡳࡧ࡭ࡦࠩ᠉"), bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᠊")],
  bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᠋"): [bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡡ࡮ࡩࡾ࠭᠌"), bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭᠍")],
  bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᠎"): bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᠏"),
  bstack1111l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᠐"): bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᠑"),
  bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᠒"): bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᠓"),
  bstack1111l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ᠔"): [bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡶࡰࠨ᠕"), bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ᠖")],
  bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᠗"): bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭᠘"),
  bstack1111l1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭᠙"): bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭᠚"),
  bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࠨ᠛"): bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࠨ᠜"),
  bstack1111l1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ᠝"): bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ᠞"),
  bstack1111l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᠟"): bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᠠ")
}
bstack1ll1ll11_opy_ = {
  bstack1111l1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᠡ"): bstack1111l1l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᠢ"),
  bstack1111l1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᠣ"): [bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᠤ"), bstack1111l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᠥ")],
  bstack1111l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᠦ"): bstack1111l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᠧ"),
  bstack1111l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᠨ"): bstack1111l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᠩ"),
  bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᠪ"): [bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᠫ"), bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ᠬ")],
  bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᠭ"): bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᠮ"),
  bstack1111l1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᠯ"): bstack1111l1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩᠰ"),
  bstack1111l1l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᠱ"): [bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᠲ"), bstack1111l1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᠳ")],
  bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧᠴ"): [bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪᠵ"), bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࠪᠶ")]
}
bstack1ll1l11111_opy_ = [
  bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪᠷ"),
  bstack1111l1l_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨᠸ"),
  bstack1111l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬᠹ"),
  bstack1111l1l_opy_ (u"ࠧࡴࡧࡷ࡛࡮ࡴࡤࡰࡹࡕࡩࡨࡺࠧᠺ"),
  bstack1111l1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪᠻ"),
  bstack1111l1l_opy_ (u"ࠩࡶࡸࡷ࡯ࡣࡵࡈ࡬ࡰࡪࡏ࡮ࡵࡧࡵࡥࡨࡺࡡࡣ࡫࡯࡭ࡹࡿࠧᠼ"),
  bstack1111l1l_opy_ (u"ࠪࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡖࡲࡰ࡯ࡳࡸࡇ࡫ࡨࡢࡸ࡬ࡳࡷ࠭ᠽ"),
  bstack1111l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᠾ"),
  bstack1111l1l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪᠿ"),
  bstack1111l1l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᡀ"),
  bstack1111l1l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᡁ"),
  bstack1111l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᡂ"),
]
bstack11111llll_opy_ = [
  bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᡃ"),
  bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᡄ"),
  bstack1111l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪᡅ"),
  bstack1111l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᡆ"),
  bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᡇ"),
  bstack1111l1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᡈ"),
  bstack1111l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᡉ"),
  bstack1111l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᡊ"),
  bstack1111l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᡋ"),
  bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩᡌ"),
  bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᡍ"),
  bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭ᡎ"),
  bstack1111l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩᡏ"),
  bstack1111l1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡕࡣࡪࠫᡐ"),
  bstack1111l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᡑ"),
  bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᡒ"),
  bstack1111l1l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᡓ"),
  bstack1111l1l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠴ࠫᡔ"),
  bstack1111l1l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠶ࠬᡕ"),
  bstack1111l1l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠸࠭ᡖ"),
  bstack1111l1l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠺ࠧᡗ"),
  bstack1111l1l_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠵ࠨᡘ"),
  bstack1111l1l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠷ࠩᡙ"),
  bstack1111l1l_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠹ࠪᡚ"),
  bstack1111l1l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠻ࠫᡛ"),
  bstack1111l1l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠽ࠬᡜ"),
  bstack1111l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᡝ"),
  bstack1111l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᡞ"),
  bstack1111l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᡟ"),
  bstack1111l1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᡠ"),
  bstack1111l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᡡ"),
  bstack1111l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᡢ"),
  bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᡣ")
]
bstack11l1ll1ll1l_opy_ = [
  bstack1111l1l_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬᡤ"),
  bstack1111l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᡥ"),
  bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᡦ"),
  bstack1111l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᡧ"),
  bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡒࡵ࡭ࡴࡸࡩࡵࡻࠪᡨ"),
  bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᡩ"),
  bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡧࡧࠨᡪ"),
  bstack1111l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᡫ"),
  bstack1111l1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᡬ"),
  bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᡭ"),
  bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᡮ"),
  bstack1111l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪᡯ"),
  bstack1111l1l_opy_ (u"ࠬࡵࡳࠨᡰ"),
  bstack1111l1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᡱ"),
  bstack1111l1l_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ᡲ"),
  bstack1111l1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪᡳ"),
  bstack1111l1l_opy_ (u"ࠩࡵࡩ࡬࡯࡯࡯ࠩᡴ"),
  bstack1111l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬᡵ"),
  bstack1111l1l_opy_ (u"ࠫࡲࡧࡣࡩ࡫ࡱࡩࠬᡶ"),
  bstack1111l1l_opy_ (u"ࠬࡸࡥࡴࡱ࡯ࡹࡹ࡯࡯࡯ࠩᡷ"),
  bstack1111l1l_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᡸ"),
  bstack1111l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫ᡹"),
  bstack1111l1l_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧ᡺"),
  bstack1111l1l_opy_ (u"ࠩࡱࡳࡕࡧࡧࡦࡎࡲࡥࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᡻"),
  bstack1111l1l_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫ᡼"),
  bstack1111l1l_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪ᡽"),
  bstack1111l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ᡾"),
  bstack1111l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧ᡿"),
  bstack1111l1l_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫᢀ"),
  bstack1111l1l_opy_ (u"ࠨࡰࡲࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠬᢁ"),
  bstack1111l1l_opy_ (u"ࠩࡦ࡬ࡪࡩ࡫ࡖࡔࡏࠫᢂ"),
  bstack1111l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᢃ"),
  bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡇࡴࡵ࡫ࡪࡧࡶࠫᢄ"),
  bstack1111l1l_opy_ (u"ࠬࡩࡡࡱࡶࡸࡶࡪࡉࡲࡢࡵ࡫ࠫᢅ"),
  bstack1111l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᢆ"),
  bstack1111l1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᢇ"),
  bstack1111l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡛࡫ࡲࡴ࡫ࡲࡲࠬᢈ"),
  bstack1111l1l_opy_ (u"ࠩࡱࡳࡇࡲࡡ࡯࡭ࡓࡳࡱࡲࡩ࡯ࡩࠪᢉ"),
  bstack1111l1l_opy_ (u"ࠪࡱࡦࡹ࡫ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩᢊ"),
  bstack1111l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡐࡴ࡭ࡳࠨᢋ"),
  bstack1111l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡎࡪࠧᢌ"),
  bstack1111l1l_opy_ (u"࠭ࡤࡦࡦ࡬ࡧࡦࡺࡥࡥࡆࡨࡺ࡮ࡩࡥࠨᢍ"),
  bstack1111l1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡐࡢࡴࡤࡱࡸ࠭ᢎ"),
  bstack1111l1l_opy_ (u"ࠨࡲ࡫ࡳࡳ࡫ࡎࡶ࡯ࡥࡩࡷ࠭ᢏ"),
  bstack1111l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᢐ"),
  bstack1111l1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡐࡲࡷ࡭ࡴࡴࡳࠨᢑ"),
  bstack1111l1l_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩᢒ"),
  bstack1111l1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᢓ"),
  bstack1111l1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪᢔ"),
  bstack1111l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡂࡪࡱࡰࡩࡹࡸࡩࡤࠩᢕ"),
  bstack1111l1l_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࡖ࠳ࠩᢖ"),
  bstack1111l1l_opy_ (u"ࠩࡰ࡭ࡩ࡙ࡥࡴࡵ࡬ࡳࡳࡏ࡮ࡴࡶࡤࡰࡱࡇࡰࡱࡵࠪᢗ"),
  bstack1111l1l_opy_ (u"ࠪࡩࡸࡶࡲࡦࡵࡶࡳࡘ࡫ࡲࡷࡧࡵࠫᢘ"),
  bstack1111l1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪᢙ"),
  bstack1111l1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡃࡥࡲࠪᢚ"),
  bstack1111l1l_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ᢛ"),
  bstack1111l1l_opy_ (u"ࠧࡴࡻࡱࡧ࡙࡯࡭ࡦ࡙࡬ࡸ࡭ࡔࡔࡑࠩᢜ"),
  bstack1111l1l_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᢝ"),
  bstack1111l1l_opy_ (u"ࠩࡪࡴࡸࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧᢞ"),
  bstack1111l1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫᢟ"),
  bstack1111l1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫᢠ"),
  bstack1111l1l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡇ࡭ࡧ࡮ࡨࡧࡍࡥࡷ࠭ᢡ"),
  bstack1111l1l_opy_ (u"࠭ࡸ࡮ࡵࡍࡥࡷ࠭ᢢ"),
  bstack1111l1l_opy_ (u"ࠧࡹ࡯ࡻࡎࡦࡸࠧᢣ"),
  bstack1111l1l_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧᢤ"),
  bstack1111l1l_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩᢥ"),
  bstack1111l1l_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫᢦ"),
  bstack1111l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧᢧ"),
  bstack1111l1l_opy_ (u"ࠬࡧࡰࡱࡘࡨࡶࡸ࡯࡯࡯ࠩᢨ"),
  bstack1111l1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷᢩࠬ"),
  bstack1111l1l_opy_ (u"ࠧࡳࡧࡶ࡭࡬ࡴࡁࡱࡲࠪᢪ"),
  bstack1111l1l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࡷࠬ᢫"),
  bstack1111l1l_opy_ (u"ࠩࡦࡥࡳࡧࡲࡺࠩ᢬"),
  bstack1111l1l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ᢭"),
  bstack1111l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ᢮"),
  bstack1111l1l_opy_ (u"ࠬ࡯ࡥࠨ᢯"),
  bstack1111l1l_opy_ (u"࠭ࡥࡥࡩࡨࠫᢰ"),
  bstack1111l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᢱ"),
  bstack1111l1l_opy_ (u"ࠨࡳࡸࡩࡺ࡫ࠧᢲ"),
  bstack1111l1l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫᢳ"),
  bstack1111l1l_opy_ (u"ࠪࡥࡵࡶࡓࡵࡱࡵࡩࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠫᢴ"),
  bstack1111l1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡇࡦࡳࡥࡳࡣࡌࡱࡦ࡭ࡥࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪᢵ"),
  bstack1111l1l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡈࡼࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨᢶ"),
  bstack1111l1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡍࡳࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩᢷ"),
  bstack1111l1l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᢸ"),
  bstack1111l1l_opy_ (u"ࠨࡴࡨࡷࡪࡸࡶࡦࡆࡨࡺ࡮ࡩࡥࠨᢹ"),
  bstack1111l1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᢺ"),
  bstack1111l1l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬᢻ"),
  bstack1111l1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡦࡹࡳࡤࡱࡧࡩࠬᢼ"),
  bstack1111l1l_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡎࡵࡳࡅࡧࡹ࡭ࡨ࡫ࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᢽ"),
  bstack1111l1l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡵࡥ࡫ࡲࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭ᢾ"),
  bstack1111l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡱࡲ࡯ࡩࡕࡧࡹࠨᢿ"),
  bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᣀ"),
  bstack1111l1l_opy_ (u"ࠩࡺࡨ࡮ࡵࡓࡦࡴࡹ࡭ࡨ࡫ࠧᣁ"),
  bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᣂ"),
  bstack1111l1l_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸࡈࡸ࡯ࡴࡵࡖ࡭ࡹ࡫ࡔࡳࡣࡦ࡯࡮ࡴࡧࠨᣃ"),
  bstack1111l1l_opy_ (u"ࠬ࡮ࡩࡨࡪࡆࡳࡳࡺࡲࡢࡵࡷࠫᣄ"),
  bstack1111l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡖࡲࡦࡨࡨࡶࡪࡴࡣࡦࡵࠪᣅ"),
  bstack1111l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᣆ"),
  bstack1111l1l_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬᣇ"),
  bstack1111l1l_opy_ (u"ࠩࡵࡩࡲࡵࡶࡦࡋࡒࡗࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࡎࡲࡧࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧᣈ"),
  bstack1111l1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬᣉ"),
  bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᣊ"),
  bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧᣋ"),
  bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᣌ"),
  bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᣍ"),
  bstack1111l1l_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫᣎ"),
  bstack1111l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨᣏ"),
  bstack1111l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬᣐ"),
  bstack1111l1l_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧᣑ")
]
bstack111ll1l1l_opy_ = {
  bstack1111l1l_opy_ (u"ࠬࡼࠧᣒ"): bstack1111l1l_opy_ (u"࠭ࡶࠨᣓ"),
  bstack1111l1l_opy_ (u"ࠧࡧࠩᣔ"): bstack1111l1l_opy_ (u"ࠨࡨࠪᣕ"),
  bstack1111l1l_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨᣖ"): bstack1111l1l_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩᣗ"),
  bstack1111l1l_opy_ (u"ࠫࡴࡴ࡬ࡺࡣࡸࡸࡴࡳࡡࡵࡧࠪᣘ"): bstack1111l1l_opy_ (u"ࠬࡵ࡮࡭ࡻࡄࡹࡹࡵ࡭ࡢࡶࡨࠫᣙ"),
  bstack1111l1l_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪᣚ"): bstack1111l1l_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫᣛ"),
  bstack1111l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫᣜ"): bstack1111l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬᣝ"),
  bstack1111l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ᣞ"): bstack1111l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᣟ"),
  bstack1111l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᣠ"): bstack1111l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᣡ"),
  bstack1111l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᣢ"): bstack1111l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫᣣ"),
  bstack1111l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪᣤ"): bstack1111l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡈࡰࡵࡷࠫᣥ"),
  bstack1111l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬᣦ"): bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᣧ"),
  bstack1111l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧᣨ"): bstack1111l1l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᣩ"),
  bstack1111l1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᣪ"): bstack1111l1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫᣫ"),
  bstack1111l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᣬ"): bstack1111l1l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᣭ"),
  bstack1111l1l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᣮ"): bstack1111l1l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨᣯ"),
  bstack1111l1l_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫᣰ"): bstack1111l1l_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬᣱ"),
  bstack1111l1l_opy_ (u"ࠩࡳࡥࡨ࡬ࡩ࡭ࡧࠪᣲ"): bstack1111l1l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᣳ"),
  bstack1111l1l_opy_ (u"ࠫࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᣴ"): bstack1111l1l_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᣵ"),
  bstack1111l1l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ᣶"): bstack1111l1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ᣷"),
  bstack1111l1l_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩ᣸"): bstack1111l1l_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪ᣹"),
  bstack1111l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᣺"): bstack1111l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭᣻"),
  bstack1111l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࠲ࡸࡥࡱࡧࡤࡸࡪࡸࠧ᣼"): bstack1111l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡱࡧࡤࡸࡪࡸࠧ᣽")
}
bstack11l1ll1l11l_opy_ = bstack1111l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩ࡬ࡸ࡭ࡻࡢ࠯ࡥࡲࡱ࠴ࡶࡥࡳࡥࡼ࠳ࡨࡲࡩ࠰ࡴࡨࡰࡪࡧࡳࡦࡵ࠲ࡰࡦࡺࡥࡴࡶ࠲ࡨࡴࡽ࡮࡭ࡱࡤࡨࠧ᣾")
bstack11l1lll1lll_opy_ = bstack1111l1l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠰ࡪࡨࡥࡱࡺࡨࡤࡪࡨࡧࡰࠨ᣿")
bstack1ll1ll1ll_opy_ = bstack1111l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡩࡩࡹ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡷࡪࡴࡤࡠࡵࡧ࡯ࡤ࡫ࡶࡦࡰࡷࡷࠧᤀ")
bstack1l1ll1111l_opy_ = bstack1111l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡼࡪ࠯ࡩࡷࡥࠫᤁ")
bstack1ll1ll11l_opy_ = bstack1111l1l_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠧᤂ")
bstack1ll11lll1l_opy_ = bstack1111l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠩᤃ")
bstack11l1lll1l11_opy_ = {
  bstack1111l1l_opy_ (u"࠭ࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠨᤄ"): 50,
  bstack1111l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᤅ"): 40,
  bstack1111l1l_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩᤆ"): 30,
  bstack1111l1l_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᤇ"): 20,
  bstack1111l1l_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᤈ"): 10
}
bstack1ll111ll11_opy_ = bstack11l1lll1l11_opy_[bstack1111l1l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᤉ")]
bstack1ll1lll1l_opy_ = bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᤊ")
bstack11l1l1l111_opy_ = bstack1111l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᤋ")
bstack1l1lllll1_opy_ = bstack1111l1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᤌ")
bstack11l11111_opy_ = bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᤍ")
bstack11ll1l1l_opy_ = bstack1111l1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡥࡳࡪࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡳࡥࡨࡱࡡࡨࡧࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧᤎ")
bstack11l1l1lll1l_opy_ = [bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᤏ"), bstack1111l1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᤐ")]
bstack11l1lllll1l_opy_ = [bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᤑ"), bstack1111l1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᤒ")]
bstack1111l1l1_opy_ = re.compile(bstack1111l1l_opy_ (u"ࠧ࡟࡝࡟ࡠࡼ࠳࡝ࠬ࠼࠱࠮ࠩ࠭ᤓ"))
bstack1lll1l1ll_opy_ = [
  bstack1111l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡓࡧ࡭ࡦࠩᤔ"),
  bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᤕ"),
  bstack1111l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᤖ"),
  bstack1111l1l_opy_ (u"ࠫࡳ࡫ࡷࡄࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࠨᤗ"),
  bstack1111l1l_opy_ (u"ࠬࡧࡰࡱࠩᤘ"),
  bstack1111l1l_opy_ (u"࠭ࡵࡥ࡫ࡧࠫᤙ"),
  bstack1111l1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᤚ"),
  bstack1111l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࠨᤛ"),
  bstack1111l1l_opy_ (u"ࠩࡲࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧᤜ"),
  bstack1111l1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࠨᤝ"),
  bstack1111l1l_opy_ (u"ࠫࡳࡵࡒࡦࡵࡨࡸࠬᤞ"), bstack1111l1l_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡕࡩࡸ࡫ࡴࠨ᤟"),
  bstack1111l1l_opy_ (u"࠭ࡣ࡭ࡧࡤࡶࡘࡿࡳࡵࡧࡰࡊ࡮ࡲࡥࡴࠩᤠ"),
  bstack1111l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹ࡚ࡩ࡮࡫ࡱ࡫ࡸ࠭ᤡ"),
  bstack1111l1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࡑࡵࡧࡨ࡫ࡱ࡫ࠬᤢ"),
  bstack1111l1l_opy_ (u"ࠩࡲࡸ࡭࡫ࡲࡂࡲࡳࡷࠬᤣ"),
  bstack1111l1l_opy_ (u"ࠪࡴࡷ࡯࡮ࡵࡒࡤ࡫ࡪ࡙࡯ࡶࡴࡦࡩࡔࡴࡆࡪࡰࡧࡊࡦ࡯࡬ࡶࡴࡨࠫᤤ"),
  bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩᤥ"), bstack1111l1l_opy_ (u"ࠬࡧࡰࡱࡒࡤࡧࡰࡧࡧࡦࠩᤦ"), bstack1111l1l_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨᤧ"), bstack1111l1l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡑࡣࡦ࡯ࡦ࡭ࡥࠨᤨ"), bstack1111l1l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡆࡸࡶࡦࡺࡩࡰࡰࠪᤩ"),
  bstack1111l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧᤪ"),
  bstack1111l1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡨࡷࡹࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧᤫ"),
  bstack1111l1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪ࠭᤬"), bstack1111l1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࡅ࡯ࡦࡌࡲࡹ࡫࡮ࡵࠩ᤭"),
  bstack1111l1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫ᤮"),
  bstack1111l1l_opy_ (u"ࠧࡢࡦࡥࡔࡴࡸࡴࠨ᤯"),
  bstack1111l1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡔࡱࡦ࡯ࡪࡺࠧᤰ"),
  bstack1111l1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡗ࡭ࡲ࡫࡯ࡶࡶࠪᤱ"),
  bstack1111l1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡺࡨࠨᤲ"),
  bstack1111l1l_opy_ (u"ࠫࡦࡼࡤࠨᤳ"), bstack1111l1l_opy_ (u"ࠬࡧࡶࡥࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᤴ"), bstack1111l1l_opy_ (u"࠭ࡡࡷࡦࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨᤵ"), bstack1111l1l_opy_ (u"ࠧࡢࡸࡧࡅࡷ࡭ࡳࠨᤶ"),
  bstack1111l1l_opy_ (u"ࠨࡷࡶࡩࡐ࡫ࡹࡴࡶࡲࡶࡪ࠭ᤷ"), bstack1111l1l_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡺࡨࠨᤸ"), bstack1111l1l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡳࡴࡹࡲࡶࡩ᤹࠭"),
  bstack1111l1l_opy_ (u"ࠫࡰ࡫ࡹࡂ࡮࡬ࡥࡸ࠭᤺"), bstack1111l1l_opy_ (u"ࠬࡱࡥࡺࡒࡤࡷࡸࡽ࡯ࡳࡦ᤻ࠪ"),
  bstack1111l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨ᤼"), bstack1111l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡇࡲࡨࡵࠪ᤽"), bstack1111l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࡇ࡭ࡷ࠭᤾"), bstack1111l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡄࡪࡵࡳࡲ࡫ࡍࡢࡲࡳ࡭ࡳ࡭ࡆࡪ࡮ࡨࠫ᤿"), bstack1111l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡗࡶࡩࡘࡿࡳࡵࡧࡰࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧ᥀"),
  bstack1111l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࠧ᥁"), bstack1111l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࡴࠩ᥂"),
  bstack1111l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡉ࡯ࡳࡢࡤ࡯ࡩࡇࡻࡩ࡭ࡦࡆ࡬ࡪࡩ࡫ࠨ᥃"),
  bstack1111l1l_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻ࡙࡯࡭ࡦࡱࡸࡸࠬ᥄"),
  bstack1111l1l_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡂࡥࡷ࡭ࡴࡴࠧ᥅"), bstack1111l1l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡅࡤࡸࡪ࡭࡯ࡳࡻࠪ᥆"), bstack1111l1l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡉࡰࡦ࡭ࡳࠨ᥇"), bstack1111l1l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡥࡱࡏ࡮ࡵࡧࡱࡸࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ᥈"),
  bstack1111l1l_opy_ (u"ࠬࡪ࡯࡯ࡶࡖࡸࡴࡶࡁࡱࡲࡒࡲࡗ࡫ࡳࡦࡶࠪ᥉"),
  bstack1111l1l_opy_ (u"࠭ࡵ࡯࡫ࡦࡳࡩ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨ᥊"), bstack1111l1l_opy_ (u"ࠧࡳࡧࡶࡩࡹࡑࡥࡺࡤࡲࡥࡷࡪࠧ᥋"),
  bstack1111l1l_opy_ (u"ࠨࡰࡲࡗ࡮࡭࡮ࠨ᥌"),
  bstack1111l1l_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡗࡱ࡭ࡲࡶ࡯ࡳࡶࡤࡲࡹ࡜ࡩࡦࡹࡶࠫ᥍"),
  bstack1111l1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳࡪࡲࡰ࡫ࡧ࡛ࡦࡺࡣࡩࡧࡵࡷࠬ᥎"),
  bstack1111l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᥏"),
  bstack1111l1l_opy_ (u"ࠬࡸࡥࡤࡴࡨࡥࡹ࡫ࡃࡩࡴࡲࡱࡪࡊࡲࡪࡸࡨࡶࡘ࡫ࡳࡴ࡫ࡲࡲࡸ࠭ᥐ"),
  bstack1111l1l_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᥑ"),
  bstack1111l1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡔࡦࡺࡨࠨᥒ"),
  bstack1111l1l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡕࡳࡩࡪࡪࠧᥓ"),
  bstack1111l1l_opy_ (u"ࠩࡪࡴࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ᥔ"),
  bstack1111l1l_opy_ (u"ࠪ࡭ࡸࡎࡥࡢࡦ࡯ࡩࡸࡹࠧᥕ"),
  bstack1111l1l_opy_ (u"ࠫࡦࡪࡢࡆࡺࡨࡧ࡙࡯࡭ࡦࡱࡸࡸࠬᥖ"),
  bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࡘࡩࡲࡪࡲࡷࠫᥗ"),
  bstack1111l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡈࡪࡼࡩࡤࡧࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᥘ"),
  bstack1111l1l_opy_ (u"ࠧࡢࡷࡷࡳࡌࡸࡡ࡯ࡶࡓࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠧᥙ"),
  bstack1111l1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡐࡤࡸࡺࡸࡡ࡭ࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ᥚ"),
  bstack1111l1l_opy_ (u"ࠩࡶࡽࡸࡺࡥ࡮ࡒࡲࡶࡹ࠭ᥛ"),
  bstack1111l1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡨࡧࡎ࡯ࡴࡶࠪᥜ"),
  bstack1111l1l_opy_ (u"ࠫࡸࡱࡩࡱࡗࡱࡰࡴࡩ࡫ࠨᥝ"), bstack1111l1l_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯࡙ࡿࡰࡦࠩᥞ"), bstack1111l1l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰࡑࡥࡺࠩᥟ"),
  bstack1111l1l_opy_ (u"ࠧࡢࡷࡷࡳࡑࡧࡵ࡯ࡥ࡫ࠫᥠ"),
  bstack1111l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡥࡤࡸࡈࡧࡰࡵࡷࡵࡩࠬᥡ"),
  bstack1111l1l_opy_ (u"ࠩࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࡔࡺࡨࡦࡴࡓࡥࡨࡱࡡࡨࡧࡶࠫᥢ"),
  bstack1111l1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨ࡛࡮ࡴࡤࡰࡹࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࠬᥣ"),
  bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡳࡴࡲࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᥤ"),
  bstack1111l1l_opy_ (u"ࠬ࡫࡮ࡧࡱࡵࡧࡪࡇࡰࡱࡋࡱࡷࡹࡧ࡬࡭ࠩᥥ"),
  bstack1111l1l_opy_ (u"࠭ࡥ࡯ࡵࡸࡶࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡹࡈࡢࡸࡨࡔࡦ࡭ࡥࡴࠩᥦ"), bstack1111l1l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡅࡧࡹࡸࡴࡵ࡬ࡴࡒࡲࡶࡹ࠭ᥧ"), bstack1111l1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡘࡧࡥࡺ࡮࡫ࡷࡅࡧࡷࡥ࡮ࡲࡳࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠫᥨ"),
  bstack1111l1l_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡳࡴࡸࡉࡡࡤࡪࡨࡐ࡮ࡳࡩࡵࠩᥩ"),
  bstack1111l1l_opy_ (u"ࠪࡧࡦࡲࡥ࡯ࡦࡤࡶࡋࡵࡲ࡮ࡣࡷࠫᥪ"),
  bstack1111l1l_opy_ (u"ࠫࡧࡻ࡮ࡥ࡮ࡨࡍࡩ࠭ᥫ"),
  bstack1111l1l_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬᥬ"),
  bstack1111l1l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡇࡱࡥࡧࡲࡥࡥࠩᥭ"), bstack1111l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡩࡩ࠭᥮"),
  bstack1111l1l_opy_ (u"ࠨࡣࡸࡸࡴࡇࡣࡤࡧࡳࡸࡆࡲࡥࡳࡶࡶࠫ᥯"), bstack1111l1l_opy_ (u"ࠩࡤࡹࡹࡵࡄࡪࡵࡰ࡭ࡸࡹࡁ࡭ࡧࡵࡸࡸ࠭ᥰ"),
  bstack1111l1l_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡹࡌࡪࡤࠪᥱ"),
  bstack1111l1l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡔࡢࡲࠪᥲ"),
  bstack1111l1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎࡴࡩࡵ࡫ࡤࡰ࡚ࡸ࡬ࠨᥳ"), bstack1111l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡇ࡬࡭ࡱࡺࡔࡴࡶࡵࡱࡵࠪᥴ"), bstack1111l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉࡨࡰࡲࡶࡪࡌࡲࡢࡷࡧ࡛ࡦࡸ࡮ࡪࡰࡪࠫ᥵"), bstack1111l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡨࡲࡑ࡯࡮࡬ࡵࡌࡲࡇࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠨ᥶"),
  bstack1111l1l_opy_ (u"ࠩ࡮ࡩࡪࡶࡋࡦࡻࡆ࡬ࡦ࡯࡮ࡴࠩ᥷"),
  bstack1111l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡽࡥࡧࡲࡥࡔࡶࡵ࡭ࡳ࡭ࡳࡅ࡫ࡵࠫ᥸"),
  bstack1111l1l_opy_ (u"ࠫࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ᥹"),
  bstack1111l1l_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡏࡪࡿࡄࡦ࡮ࡤࡽࠬ᥺"),
  bstack1111l1l_opy_ (u"࠭ࡳࡩࡱࡺࡍࡔ࡙ࡌࡰࡩࠪ᥻"),
  bstack1111l1l_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡔࡶࡵࡥࡹ࡫ࡧࡺࠩ᥼"),
  bstack1111l1l_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡓࡧࡶࡴࡴࡴࡳࡦࡖ࡬ࡱࡪࡵࡵࡵࠩ᥽"), bstack1111l1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࡝ࡡࡪࡶࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᥾"),
  bstack1111l1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾ࠭᥿"),
  bstack1111l1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡸࡿ࡮ࡤࡇࡻࡩࡨࡻࡴࡦࡈࡵࡳࡲࡎࡴࡵࡲࡶࠫᦀ"),
  bstack1111l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡉࡡࡱࡶࡸࡶࡪ࠭ᦁ"),
  bstack1111l1l_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᦂ"),
  bstack1111l1l_opy_ (u"ࠧࡧࡷ࡯ࡰࡈࡵ࡮ࡵࡧࡻࡸࡑ࡯ࡳࡵࠩᦃ"),
  bstack1111l1l_opy_ (u"ࠨࡹࡤ࡭ࡹࡌ࡯ࡳࡃࡳࡴࡘࡩࡲࡪࡲࡷࠫᦄ"),
  bstack1111l1l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡆࡳࡳࡴࡥࡤࡶࡕࡩࡹࡸࡩࡦࡵࠪᦅ"),
  bstack1111l1l_opy_ (u"ࠪࡥࡵࡶࡎࡢ࡯ࡨࠫᦆ"),
  bstack1111l1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡘࡒࡃࡦࡴࡷࠫᦇ"),
  bstack1111l1l_opy_ (u"ࠬࡺࡡࡱ࡙࡬ࡸ࡭࡙ࡨࡰࡴࡷࡔࡷ࡫ࡳࡴࡆࡸࡶࡦࡺࡩࡰࡰࠪᦈ"),
  bstack1111l1l_opy_ (u"࠭ࡳࡤࡣ࡯ࡩࡋࡧࡣࡵࡱࡵࠫᦉ"),
  bstack1111l1l_opy_ (u"ࠧࡸࡦࡤࡐࡴࡩࡡ࡭ࡒࡲࡶࡹ࠭ᦊ"),
  bstack1111l1l_opy_ (u"ࠨࡵ࡫ࡳࡼ࡞ࡣࡰࡦࡨࡐࡴ࡭ࠧᦋ"),
  bstack1111l1l_opy_ (u"ࠩ࡬ࡳࡸࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡶࡵࡨࠫᦌ"),
  bstack1111l1l_opy_ (u"ࠪࡼࡨࡵࡤࡦࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠬᦍ"),
  bstack1111l1l_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡴࡵࡺࡳࡷࡪࠧᦎ"),
  bstack1111l1l_opy_ (u"ࠬࡻࡳࡦࡒࡵࡩࡧࡻࡩ࡭ࡶ࡚ࡈࡆ࠭ᦏ"),
  bstack1111l1l_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡗࡅࡃࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧᦐ"),
  bstack1111l1l_opy_ (u"ࠧࡸࡧࡥࡈࡷ࡯ࡶࡦࡴࡄ࡫ࡪࡴࡴࡖࡴ࡯ࠫᦑ"),
  bstack1111l1l_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡹ࡮ࠧᦒ"),
  bstack1111l1l_opy_ (u"ࠩࡸࡷࡪࡔࡥࡸ࡙ࡇࡅࠬᦓ"),
  bstack1111l1l_opy_ (u"ࠪࡻࡩࡧࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᦔ"), bstack1111l1l_opy_ (u"ࠫࡼࡪࡡࡄࡱࡱࡲࡪࡩࡴࡪࡱࡱࡘ࡮ࡳࡥࡰࡷࡷࠫᦕ"),
  bstack1111l1l_opy_ (u"ࠬࡾࡣࡰࡦࡨࡓࡷ࡭ࡉࡥࠩᦖ"), bstack1111l1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡘ࡯ࡧ࡯࡫ࡱ࡫ࡎࡪࠧᦗ"),
  bstack1111l1l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡘࡆࡄࡆࡺࡴࡤ࡭ࡧࡌࡨࠬᦘ"),
  bstack1111l1l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡏ࡯ࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡷࡺࡏ࡯࡮ࡼࠫᦙ"),
  bstack1111l1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࡶࠫᦚ"),
  bstack1111l1l_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵ࡭ࡪࡹࠧᦛ"), bstack1111l1l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶࡾࡏ࡮ࡵࡧࡵࡺࡦࡲࠧᦜ"),
  bstack1111l1l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹࡎࡡࡳࡦࡺࡥࡷ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨᦝ"),
  bstack1111l1l_opy_ (u"࠭࡭ࡢࡺࡗࡽࡵ࡯࡮ࡨࡈࡵࡩࡶࡻࡥ࡯ࡥࡼࠫᦞ"),
  bstack1111l1l_opy_ (u"ࠧࡴ࡫ࡰࡴࡱ࡫ࡉࡴࡘ࡬ࡷ࡮ࡨ࡬ࡦࡅ࡫ࡩࡨࡱࠧᦟ"),
  bstack1111l1l_opy_ (u"ࠨࡷࡶࡩࡈࡧࡲࡵࡪࡤ࡫ࡪ࡙ࡳ࡭ࠩᦠ"),
  bstack1111l1l_opy_ (u"ࠩࡶ࡬ࡴࡻ࡬ࡥࡗࡶࡩࡘ࡯࡮ࡨ࡮ࡨࡸࡴࡴࡔࡦࡵࡷࡑࡦࡴࡡࡨࡧࡵࠫᦡ"),
  bstack1111l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡋ࡚ࡈࡕ࠭ᦢ"),
  bstack1111l1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡳࡺࡩࡨࡊࡦࡈࡲࡷࡵ࡬࡭ࠩᦣ"),
  bstack1111l1l_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࡍ࡯ࡤࡥࡧࡱࡅࡵ࡯ࡐࡰ࡮࡬ࡧࡾࡋࡲࡳࡱࡵࠫᦤ"),
  bstack1111l1l_opy_ (u"࠭࡭ࡰࡥ࡮ࡐࡴࡩࡡࡵ࡫ࡲࡲࡆࡶࡰࠨᦥ"),
  bstack1111l1l_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡰࡴࡰࡥࡹ࠭ᦦ"), bstack1111l1l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇ࡫࡯ࡸࡪࡸࡓࡱࡧࡦࡷࠬᦧ"),
  bstack1111l1l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡅࡧ࡯ࡥࡾࡇࡤࡣࠩᦨ"),
  bstack1111l1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡍࡩࡒ࡯ࡤࡣࡷࡳࡷࡇࡵࡵࡱࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳ࠭ᦩ")
]
bstack1ll11l1111_opy_ = bstack1111l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪᦪ")
bstack1l1l111l11_opy_ = [bstack1111l1l_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪᦫ"), bstack1111l1l_opy_ (u"࠭࠮ࡢࡣࡥࠫ᦬"), bstack1111l1l_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ᦭")]
bstack11llll1l1_opy_ = [bstack1111l1l_opy_ (u"ࠨ࡫ࡧࠫ᦮"), bstack1111l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ᦯"), bstack1111l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ᦰ"), bstack1111l1l_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪᦱ")]
bstack1l1ll11ll_opy_ = {
  bstack1111l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᦲ"): bstack1111l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᦳ"),
  bstack1111l1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᦴ"): bstack1111l1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦵ"),
  bstack1111l1l_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᦶ"): bstack1111l1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᦷ"),
  bstack1111l1l_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᦸ"): bstack1111l1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫᦹ"),
  bstack1111l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦺ"): bstack1111l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨᦻ")
}
bstack1lllll11ll_opy_ = [
  bstack1111l1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦼ"),
  bstack1111l1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧᦽ"),
  bstack1111l1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᦾ"),
  bstack1111l1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᦿ"),
  bstack1111l1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᧀ"),
]
bstack1l11lllll1_opy_ = bstack11111llll_opy_ + bstack11l1ll1ll1l_opy_ + bstack1lll1l1ll_opy_
bstack11ll11ll1l_opy_ = [
  bstack1111l1l_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫᧁ"),
  bstack1111l1l_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨᧂ"),
  bstack1111l1l_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧᧃ"),
  bstack1111l1l_opy_ (u"ࠩࡡ࠵࠵࠴ࠧᧄ"),
  bstack1111l1l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩᧅ"),
  bstack1111l1l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪᧆ"),
  bstack1111l1l_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫᧇ"),
  bstack1111l1l_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩᧈ")
]
bstack11ll11l11ll_opy_ = bstack1111l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᧉ")
bstack1ll11lllll_opy_ = bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧ᧊")
bstack11lll11l1l_opy_ = [ bstack1111l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᧋") ]
bstack1ll1l11lll_opy_ = [ bstack1111l1l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ᧌") ]
bstack1ll1ll1l_opy_ = [bstack1111l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᧍")]
bstack11111l1l_opy_ = [ bstack1111l1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᧎") ]
bstack111l111ll_opy_ = bstack1111l1l_opy_ (u"࠭ࡓࡅࡍࡖࡩࡹࡻࡰࠨ᧏")
bstack1111l1l1l_opy_ = bstack1111l1l_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪ᧐")
bstack11ll11l1l1_opy_ = bstack1111l1l_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠬ᧑")
bstack1lllll11l_opy_ = bstack1111l1l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࠨ᧒")
bstack11ll11111_opy_ = [
  bstack1111l1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡇࡃࡌࡐࡊࡊࠧ᧓"),
  bstack1111l1l_opy_ (u"ࠫࡊࡘࡒࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫ᧔"),
  bstack1111l1l_opy_ (u"ࠬࡋࡒࡓࡡࡅࡐࡔࡉࡋࡆࡆࡢࡆ࡞ࡥࡃࡍࡋࡈࡒ࡙࠭᧕"),
  bstack1111l1l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡊ࡚ࡗࡐࡔࡎࡣࡈࡎࡁࡏࡉࡈࡈࠬ᧖"),
  bstack1111l1l_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡇࡗࡣࡓࡕࡔࡠࡅࡒࡒࡓࡋࡃࡕࡇࡇࠫ᧗"),
  bstack1111l1l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡆࡐࡔ࡙ࡅࡅࠩ᧘"),
  bstack1111l1l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊ࡙ࡅࡕࠩ᧙"),
  bstack1111l1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡆࡖࡕࡈࡈࠬ᧚"),
  bstack1111l1l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡇࡂࡐࡔࡗࡉࡉ࠭᧛"),
  bstack1111l1l_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭᧜"),
  bstack1111l1l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧ᧝"),
  bstack1111l1l_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤࡏࡎࡗࡃࡏࡍࡉ࠭᧞"),
  bstack1111l1l_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫ᧟"),
  bstack1111l1l_opy_ (u"ࠩࡈࡖࡗࡥࡔࡖࡐࡑࡉࡑࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ᧠"),
  bstack1111l1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧ᧡"),
  bstack1111l1l_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫ᧢"),
  bstack1111l1l_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡎࡏࡔࡖࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨ᧣"),
  bstack1111l1l_opy_ (u"࠭ࡅࡓࡔࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭᧤"),
  bstack1111l1l_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨ᧥"),
  bstack1111l1l_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡖࡊ࡙ࡏࡍࡗࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ᧦"),
  bstack1111l1l_opy_ (u"ࠩࡈࡖࡗࡥࡍࡂࡐࡇࡅ࡙ࡕࡒ࡚ࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨ᧧"),
]
bstack1ll11l1ll1_opy_ = bstack1111l1l_opy_ (u"ࠪ࠲࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠯ࠨ᧨")
bstack11llll111_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠫࢃ࠭᧩")), bstack1111l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ᧪"), bstack1111l1l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ᧫"))
bstack11ll11ll1l1_opy_ = bstack1111l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡩࠨ᧬")
bstack11l1l1ll111_opy_ = [ bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᧭"), bstack1111l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᧮"), bstack1111l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ᧯"), bstack1111l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᧰")]
bstack11ll111l11_opy_ = [ bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᧱"), bstack1111l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ᧲"), bstack1111l1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭᧳"), bstack1111l1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ᧴") ]
bstack1l11ll1ll_opy_ = [ bstack1111l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᧵") ]
bstack11l1l1llll1_opy_ = [ bstack1111l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᧶") ]
bstack1l1lllll11_opy_ = 360
bstack11ll111l11l_opy_ = bstack1111l1l_opy_ (u"ࠦࡦࡶࡰ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦ᧷")
bstack11l1l1lll11_opy_ = bstack1111l1l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡪࡵࡶࡹࡪࡹࠢ᧸")
bstack11l1lll111l_opy_ = bstack1111l1l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡫ࡶࡷࡺ࡫ࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠤ᧹")
bstack11ll11ll1ll_opy_ = bstack1111l1l_opy_ (u"ࠢࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡶࡨࡷࡹࡹࠠࡢࡴࡨࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡰࡰࠣࡓࡘࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠦࡵࠣࡥࡳࡪࠠࡢࡤࡲࡺࡪࠦࡦࡰࡴࠣࡅࡳࡪࡲࡰ࡫ࡧࠤࡩ࡫ࡶࡪࡥࡨࡷ࠳ࠨ᧺")
bstack11ll1l1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠣ࠳࠴࠲࠵ࠨ᧻")
bstack1111ll111l_opy_ = {
  bstack1111l1l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ᧼"): bstack1111l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᧽"),
  bstack1111l1l_opy_ (u"ࠫࡋࡇࡉࡍࠩ᧾"): bstack1111l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᧿"),
  bstack1111l1l_opy_ (u"࠭ࡓࡌࡋࡓࠫᨀ"): bstack1111l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᨁ")
}
bstack1111lllll_opy_ = [
  bstack1111l1l_opy_ (u"ࠣࡩࡨࡸࠧᨂ"),
  bstack1111l1l_opy_ (u"ࠤࡪࡳࡇࡧࡣ࡬ࠤᨃ"),
  bstack1111l1l_opy_ (u"ࠥ࡫ࡴࡌ࡯ࡳࡹࡤࡶࡩࠨᨄ"),
  bstack1111l1l_opy_ (u"ࠦࡷ࡫ࡦࡳࡧࡶ࡬ࠧᨅ"),
  bstack1111l1l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦᨆ"),
  bstack1111l1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᨇ"),
  bstack1111l1l_opy_ (u"ࠢࡴࡷࡥࡱ࡮ࡺࡅ࡭ࡧࡰࡩࡳࡺࠢᨈ"),
  bstack1111l1l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧᨉ"),
  bstack1111l1l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧᨊ"),
  bstack1111l1l_opy_ (u"ࠥࡧࡱ࡫ࡡࡳࡇ࡯ࡩࡲ࡫࡮ࡵࠤᨋ"),
  bstack1111l1l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࡷࠧᨌ"),
  bstack1111l1l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠧᨍ"),
  bstack1111l1l_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡁࡴࡻࡱࡧࡘࡩࡲࡪࡲࡷࠦᨎ"),
  bstack1111l1l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨᨏ"),
  bstack1111l1l_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᨐ"),
  bstack1111l1l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡗࡳࡺࡩࡨࡂࡥࡷ࡭ࡴࡴࠢᨑ"),
  bstack1111l1l_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡑࡺࡲࡴࡪࡖࡲࡹࡨ࡮ࠢᨒ"),
  bstack1111l1l_opy_ (u"ࠦࡸ࡮ࡡ࡬ࡧࠥᨓ"),
  bstack1111l1l_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࡅࡵࡶࠢᨔ")
]
bstack11l1llll1l1_opy_ = [
  bstack1111l1l_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧᨕ"),
  bstack1111l1l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᨖ"),
  bstack1111l1l_opy_ (u"ࠣࡣࡸࡸࡴࠨᨗ"),
  bstack1111l1l_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤᨘ"),
  bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᨙ")
]
bstack1l1l11lll1_opy_ = {
  bstack1111l1l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥᨚ"): [bstack1111l1l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦᨛ")],
  bstack1111l1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ᨜"): [bstack1111l1l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᨝")],
  bstack1111l1l_opy_ (u"ࠣࡣࡸࡸࡴࠨ᨞"): [bstack1111l1l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨ᨟"), bstack1111l1l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨᨠ"), bstack1111l1l_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᨡ"), bstack1111l1l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦᨢ")],
  bstack1111l1l_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨᨣ"): [bstack1111l1l_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢᨤ")],
  bstack1111l1l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᨥ"): [bstack1111l1l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᨦ")],
}
bstack11l1ll111ll_opy_ = {
  bstack1111l1l_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤᨧ"): bstack1111l1l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥᨨ"),
  bstack1111l1l_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᨩ"): bstack1111l1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᨪ"),
  bstack1111l1l_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦᨫ"): bstack1111l1l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࠥᨬ"),
  bstack1111l1l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧᨭ"): bstack1111l1l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧᨮ"),
  bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᨯ"): bstack1111l1l_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᨰ")
}
bstack111l1ll1ll_opy_ = {
  bstack1111l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᨱ"): bstack1111l1l_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࠦࡓࡦࡶࡸࡴࠬᨲ"),
  bstack1111l1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᨳ"): bstack1111l1l_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡖࡨࡥࡷࡪ࡯ࡸࡰࠪᨴ"),
  bstack1111l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᨵ"): bstack1111l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡖࡩࡹࡻࡰࠨᨶ"),
  bstack1111l1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᨷ"): bstack1111l1l_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭ᨸ")
}
bstack11l1lll1111_opy_ = 65536
bstack11l1ll11111_opy_ = bstack1111l1l_opy_ (u"ࠧ࠯࠰࠱࡟࡙ࡘࡕࡏࡅࡄࡘࡊࡊ࡝ࠨᨹ")
bstack11l1ll1ll11_opy_ = [
      bstack1111l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᨺ"), bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᨻ"), bstack1111l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᨼ"), bstack1111l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᨽ"), bstack1111l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧᨾ"),
      bstack1111l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᨿ"), bstack1111l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᩀ"), bstack1111l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᩁ"), bstack1111l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪᩂ"),
      bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᩃ"), bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᩄ"), bstack1111l1l_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨᩅ")
    ]
bstack11l1ll11lll_opy_= {
  bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᩆ"): bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᩇ"),
  bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᩈ"): bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩉ"),
  bstack1111l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩊ"): bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᩋ"),
  bstack1111l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᩌ"): bstack1111l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᩍ"),
  bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᩎ"): bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᩏ"),
  bstack1111l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᩐ"): bstack1111l1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᩑ"),
  bstack1111l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᩒ"): bstack1111l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᩓ"),
  bstack1111l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᩔ"): bstack1111l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᩕ"),
  bstack1111l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᩖ"): bstack1111l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᩗ"),
  bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨᩘ"): bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩙ"),
  bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᩚ"): bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᩛ"),
  bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧᩜ"): bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨᩝ"),
  bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩞ"): bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᩟"),
  bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶ᩠ࠫ"): bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࡔࡶࡴࡪࡱࡱࡷࠬᩡ"),
  bstack1111l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨᩢ"): bstack1111l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩᩣ"),
  bstack1111l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᩤ"): bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᩥ"),
  bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᩦ"): bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᩧ"),
  bstack1111l1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᩨ"): bstack1111l1l_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪᩩ"),
  bstack1111l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᩪ"): bstack1111l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᩫ"),
  bstack1111l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᩬ"): bstack1111l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩭ"),
  bstack1111l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᩮ"): bstack1111l1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᩯ"),
  bstack1111l1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᩰ"): bstack1111l1l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᩱ"),
  bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᩲ"): bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᩳ"),
  bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᩴ"): bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᩵"),
  bstack1111l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᩶"): bstack1111l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᩷"),
  bstack1111l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᩸"): bstack1111l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬ᩹"),
  bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭᩺"): bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ᩻"),
  bstack1111l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ᩼"): bstack1111l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬ᩽")
}
bstack11l1ll1111l_opy_ = [bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᩾"), bstack1111l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ᩿࠭")]
bstack1ll1111l_opy_ = (bstack1111l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣ᪀"),)
bstack11l1lll1l1l_opy_ = bstack1111l1l_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡸࡴࡩࡧࡴࡦࡡࡦࡰ࡮࠭᪁")
bstack1ll1ll1lll_opy_ = bstack1111l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡧࡳ࡫ࡧࡷ࠴ࠨ᪂")
bstack11ll1ll11l_opy_ = bstack1111l1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡲࡪࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡢࡵ࡫ࡦࡴࡧࡲࡥ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࠥ᪃")
bstack11ll1llll1_opy_ = bstack1111l1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳࠨ᪄")
class EVENTS(Enum):
  bstack11l1l1ll11l_opy_ = bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪ᪅")
  bstack111lllll1_opy_ = bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡥࡢࡰࡸࡴࠬ᪆") # final bstack11l1ll1llll_opy_
  bstack11l1ll11l11_opy_ = bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࡯ࡳ࡬ࡹࠧ᪇")
  bstack1l11ll11_opy_ = bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬ᪈") #shift post bstack11l1llll111_opy_
  bstack1ll1l1ll11_opy_ = bstack1111l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮ࠫ᪉") #shift post bstack11l1llll111_opy_
  bstack11l1ll1lll1_opy_ = bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡮ࡵࡣࠩ᪊") #shift
  bstack11l1llll11l_opy_ = bstack1111l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪ᪋") #shift
  bstack1l111lll1l_opy_ = bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨ᪌")
  bstack1ll1l1111l1_opy_ = bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡶࡥࡻ࡫࠭ࡳࡧࡶࡹࡱࡺࡳࠨ᪍")
  bstack1ll11ll1l1_opy_ = bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡴࡪࡸࡦࡰࡴࡰࡷࡨࡧ࡮ࠨ᪎")
  bstack1l1llll1l1_opy_ = bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡮ࡲࡧࡦࡲࠧ᪏") #shift
  bstack1l111l11ll_opy_ = bstack1111l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡡࡱࡲ࠰ࡹࡵࡲ࡯ࡢࡦࠪ᪐") #shift
  bstack1llll1llll_opy_ = bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡧ࡮࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠩ᪑")
  bstack1l11l111ll_opy_ = bstack1111l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭᪒") #shift
  bstack1l1l11ll1l_opy_ = bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭᪓") #shift
  bstack11l1l1ll1ll_opy_ = bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻࠪ᪔") #shift
  bstack1l1l1l111l1_opy_ = bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ᪕")
  bstack1ll1l1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡶࡸࡦࡺࡵࡴࠩ᪖") #shift
  bstack1l111lll11_opy_ = bstack1111l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪ᪗")
  bstack11l1l1ll1l1_opy_ = bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡽࡿ࠭ࡴࡧࡷࡹࡵ࠭᪘") #shift
  bstack1l111l111_opy_ = bstack1111l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡹࡻࡰࠨ᪙")
  bstack11l1llll1ll_opy_ = bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡲࡦࡶࡳࡩࡱࡷࠫ᪚") # not bstack11l1l1lllll_opy_ in python
  bstack11ll1lll1l_opy_ = bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡶࡻࡩࡵࠩ᪛") # used in bstack11l1ll1l1l1_opy_
  bstack11l11111l_opy_ = bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿࡭ࡥࡵࠩ᪜") # used in bstack11l1ll1l1l1_opy_
  bstack11l1l1l1_opy_ = bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡀࡨࡰࡱ࡮ࠫ᪝")
  bstack1111lll1_opy_ = bstack1111l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠨ᪞")
  bstack11l1lll11l_opy_ = bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠨ᪟") #
  bstack1llll1l11_opy_ = bstack1111l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡵࡣ࡮ࡩࡘࡩࡲࡦࡧࡱࡗ࡭ࡵࡴࠨ᪠")
  bstack1ll1l11l1_opy_ = bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡤࡹࡹࡵ࠭ࡤࡣࡳࡸࡺࡸࡥࠨ᪡")
  bstack1ll1111l1l_opy_ = bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸࡥ࠮ࡶࡨࡷࡹ࠭᪢")
  bstack11ll1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶ࡯ࡴࡶ࠰ࡸࡪࡹࡴࠨ᪣")
  bstack1l1l11ll_opy_ = bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡳࡧ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫ᪤") #shift
  bstack11111lll1_opy_ = bstack1111l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᪥") #shift
  bstack11l1ll1l1ll_opy_ = bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴ࠳ࡣࡢࡲࡷࡹࡷ࡫ࠧ᪦")
  bstack11l1lll11l1_opy_ = bstack1111l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾࡮ࡪ࡬ࡦ࠯ࡷ࡭ࡲ࡫࡯ࡶࡶࠪᪧ")
  bstack1lll1111l11_opy_ = bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡴࡶࡤࡶࡹ࠭᪨")
  bstack11l1ll11l1l_opy_ = bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪ᪩")
  bstack11l1ll1l111_opy_ = bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡦ࡬ࡪࡩ࡫࠮ࡷࡳࡨࡦࡺࡥࠨ᪪")
  bstack1ll1ll1l11l_opy_ = bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡢࡰࡱࡷࡷࡹࡸࡡࡱࠩ᪫")
  bstack1llll11l1ll_opy_ = bstack1111l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡤࡱࡱࡲࡪࡩࡴࠨ᪬")
  bstack1llll1l1111_opy_ = bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡵࡷࡳࡵ࠭᪭")
  bstack1lll11ll1ll_opy_ = bstack1111l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡸࡦࡸࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱࠫ᪮")
  bstack1lll1l11ll1_opy_ = bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡴࡴ࡮ࡦࡥࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠧ᪯")
  bstack11l1lll1ll1_opy_ = bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠨ᪰")
  bstack11l1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࠿࡬ࡩ࡯ࡦࡑࡩࡦࡸࡥࡴࡶࡋࡹࡧ࠭᪱")
  bstack1l11ll1111l_opy_ = bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡎࡴࡩࡵࠩ᪲")
  bstack1l11l1llll1_opy_ = bstack1111l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡴࡷࠫ᪳")
  bstack1ll11lllll1_opy_ = bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡄࡱࡱࡪ࡮࡭ࠧ᪴")
  bstack11l1ll11ll1_opy_ = bstack1111l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡅࡲࡲ࡫࡯ࡧࠨ᪵")
  bstack1ll11111ll1_opy_ = bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࡮࡙ࡥ࡭ࡨࡋࡩࡦࡲࡓࡵࡧࡳ᪶ࠫ")
  bstack1l1llllllll_opy_ = bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࡯ࡓࡦ࡮ࡩࡌࡪࡧ࡬ࡈࡧࡷࡖࡪࡹࡵ࡭ࡶ᪷ࠪ")
  bstack1l1lll1111l_opy_ = bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡊࡼࡥ࡯ࡶ᪸ࠪ")
  bstack1l1lll1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠩࡶࡨࡰࡀࡴࡦࡵࡷࡗࡪࡹࡳࡪࡱࡱࡉࡻ࡫࡮ࡵ᪹ࠩ")
  bstack1l1lll1l11l_opy_ = bstack1111l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡱࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࡆࡸࡨࡲࡹ᪺࠭")
  bstack11l1lllll11_opy_ = bstack1111l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿࡫࡮ࡲࡷࡨࡹࡪ࡚ࡥࡴࡶࡈࡺࡪࡴࡴࠨ᪻")
  bstack1l11ll1ll11_opy_ = bstack1111l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡲࡴࠬ᪼")
  bstack1lll111l1l1_opy_ = bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡳࡳ࡙ࡴࡰࡲ᪽ࠪ")
class STAGE(Enum):
  bstack1111l11ll_opy_ = bstack1111l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭᪾")
  END = bstack1111l1l_opy_ (u"ࠨࡧࡱࡨᪿࠬ")
  bstack1l1111l1ll_opy_ = bstack1111l1l_opy_ (u"ࠩࡶ࡭ࡳ࡭࡬ࡦᫀࠩ")
bstack11l111l11_opy_ = {
  bstack1111l1l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࠪ᫁"): bstack1111l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᫂"),
  bstack1111l1l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅ᫃ࠩ"): bstack1111l1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ᫄")
}
PLAYWRIGHT_HUB_URL = bstack1111l1l_opy_ (u"ࠢࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠤ᫅")
bstack1ll1l111l11_opy_ = 98
bstack1ll11l11lll_opy_ = 100
bstack1111l1ll11_opy_ = {
  bstack1111l1l_opy_ (u"ࠨࡴࡨࡶࡺࡴࠧ᫆"): bstack1111l1l_opy_ (u"ࠩ࠰࠱ࡷ࡫ࡲࡶࡰࡶࠫ᫇"),
  bstack1111l1l_opy_ (u"ࠪࡨࡪࡲࡡࡺࠩ᫈"): bstack1111l1l_opy_ (u"ࠫ࠲࠳ࡲࡦࡴࡸࡲࡸ࠳ࡤࡦ࡮ࡤࡽࠬ᫉"),
  bstack1111l1l_opy_ (u"ࠬࡸࡥࡳࡷࡱ࠱ࡩ࡫࡬ࡢࡻ᫊ࠪ"): 0
}
bstack11l1ll111l1_opy_ = bstack1111l1l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨ᫋")
bstack11l1llllll1_opy_ = bstack1111l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡷࡳࡰࡴࡧࡤ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦᫌ")
bstack11l1l1111l_opy_ = bstack1111l1l_opy_ (u"ࠣࡖࡈࡗ࡙ࠦࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠢࡄࡒࡉࠦࡁࡏࡃࡏ࡝࡙ࡏࡃࡔࠤᫍ")