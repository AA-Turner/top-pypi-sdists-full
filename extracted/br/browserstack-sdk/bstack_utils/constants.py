# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import re
from enum import Enum
bstack1l1ll1l1ll_opy_ = {
  bstack111ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨḅ"): bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࠫḆ"),
  bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫḇ"): bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡭ࡨࡽࠬḈ"),
  bstack111ll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ḉ"): bstack111ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨḊ"),
  bstack111ll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬḋ"): bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭Ḍ"),
  bstack111ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬḍ"): bstack111ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࠩḎ"),
  bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬḏ"): bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࠩḐ"),
  bstack111ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩḑ"): bstack111ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪḒ"),
  bstack111ll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬḓ"): bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫ࠬḔ"),
  bstack111ll_opy_ (u"ࠨࡥࡲࡲࡸࡵ࡬ࡦࡎࡲ࡫ࡸ࠭ḕ"): bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡲࡸࡵ࡬ࡦࠩḖ"),
  bstack111ll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨḗ"): bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨḘ"),
  bstack111ll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩḙ"): bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩḚ"),
  bstack111ll_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࠭ḛ"): bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡷ࡫ࡧࡩࡴ࠭Ḝ"),
  bstack111ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨḝ"): bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨḞ"),
  bstack111ll_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫḟ"): bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫḠ"),
  bstack111ll_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫḡ"): bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫḢ"),
  bstack111ll_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪḣ"): bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪḤ"),
  bstack111ll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬḥ"): bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭Ḧ"),
  bstack111ll_opy_ (u"ࠬࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫḧ"): bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫḨ"),
  bstack111ll_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬḩ"): bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬḪ"),
  bstack111ll_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩḫ"): bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩḬ"),
  bstack111ll_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ḭ"): bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭Ḯ"),
  bstack111ll_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨḯ"): bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨḰ"),
  bstack111ll_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧḱ"): bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡪࡲࡷࡹࡹࠧḲ"),
  bstack111ll_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫḳ"): bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦ࡫ࡩࡡࡤࡪࡨࠫḴ"),
  bstack111ll_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭ḵ"): bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭Ḷ"),
  bstack111ll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪḷ"): bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪḸ"),
  bstack111ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ḹ"): bstack111ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪḺ"),
  bstack111ll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨḻ"): bstack111ll_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪḼ"),
  bstack111ll_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ḽ"): bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧḾ"),
  bstack111ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨḿ"): bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨṀ"),
  bstack111ll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫṁ"): bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫṂ"),
  bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫṃ"): bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧṄ"),
  bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩṅ"): bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩṆ"),
  bstack111ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩṇ"): bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡳࡺࡸࡣࡦࠩṈ"),
  bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ṉ"): bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ṋ"),
  bstack111ll_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨṋ"): bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡒࡦࡳࡥࠨṌ"),
  bstack111ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫṍ"): bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫṎ"),
  bstack111ll_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧṏ"): bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧṐ"),
  bstack111ll_opy_ (u"ࠬࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪṑ"): bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪṒ"),
  bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪṓ"): bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪṔ"),
  bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫṕ"): bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫṖ")
}
bstack11111l1l11l_opy_ = [
  bstack111ll_opy_ (u"ࠫࡴࡹࠧṗ"),
  bstack111ll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨṘ"),
  bstack111ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨṙ"),
  bstack111ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬṚ"),
  bstack111ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬṛ"),
  bstack111ll_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭Ṝ"),
  bstack111ll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪṝ"),
]
bstack1lll11l111_opy_ = {
  bstack111ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ṟ"): [bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ṟ"), bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡢࡒࡆࡓࡅࠨṠ")],
  bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪṡ"): bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫṢ"),
  bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬṣ"): bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊ࠭Ṥ"),
  bstack111ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩṥ"): bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠪṦ"),
  bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨṧ"): bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩṨ"),
  bstack111ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨṩ"): bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡖࡣࡕࡋࡒࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪṪ"),
  bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧṫ"): bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࠩṬ"),
  bstack111ll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩṭ"): bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪṮ"),
  bstack111ll_opy_ (u"ࠧࡢࡲࡳࠫṯ"): [bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࡣࡎࡊࠧṰ"), bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡓࡔࠬṱ")],
  bstack111ll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬṲ"): bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡍࡑࡊࡐࡊ࡜ࡅࡍࠩṳ"),
  bstack111ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩṴ"): bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩṵ"),
  bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫṶ"): [bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠬṷ"), bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩṸ")],
  bstack111ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧṹ"): bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘ࡚ࡘࡂࡐࡕࡆࡅࡑࡋࠧṺ"),
  bstack111ll_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡅࡏࡘࠪṻ"): bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡒࡄࡊࡈࡗ࡙ࡘࡁࡕࡋࡒࡒࡤ࡙ࡍࡂࡔࡗࡣࡘࡋࡌࡆࡅࡗࡍࡔࡔ࡟ࡇࡇࡄࡘ࡚ࡘࡅࡠࡄࡕࡅࡓࡉࡈࡆࡕࠪṼ")
}
bstack1l1ll11ll1_opy_ = {
  bstack111ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩṽ"): [bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡤࡴࡡ࡮ࡧࠪṾ"), bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪṿ")],
  bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭Ẁ"): [bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡢ࡯ࡪࡿࠧẁ"), bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧẂ")],
  bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩẃ"): bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩẄ"),
  bstack111ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ẅ"): bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ẇ"),
  bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬẇ"): bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬẈ"),
  bstack111ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬẉ"): [bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡰࡱࠩẊ"), bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ẋ")],
  bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬẌ"): bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧẍ"),
  bstack111ll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧẎ"): bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧẏ"),
  bstack111ll_opy_ (u"ࠬࡧࡰࡱࠩẐ"): bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱࠩẑ"),
  bstack111ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩẒ"): bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩẓ"),
  bstack111ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ẕ"): bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ẕ"),
  bstack111ll_opy_ (u"ࠦࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡉࡌࡊࠤẖ"): bstack111ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࡵࡰࡥࡷࡺࡓࡦ࡮ࡨࡧࡹ࡯࡯࡯ࡈࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࡦࡵࠥẗ"),
}
bstack1111111l_opy_ = {
  bstack111ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩẘ"): bstack111ll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫẙ"),
  bstack111ll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪẚ"): [bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫẛ"), bstack111ll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ẜ")],
  bstack111ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩẝ"): bstack111ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪẞ"),
  bstack111ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪẟ"): bstack111ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧẠ"),
  bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ạ"): [bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪẢ"), bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩả")],
  bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬẤ"): bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧấ"),
  bstack111ll_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪẦ"): bstack111ll_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬầ"),
  bstack111ll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨẨ"): [bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩẩ"), bstack111ll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫẪ")],
  bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪẫ"): [bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭Ậ"), bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭ậ")]
}
bstack1l11l1l1_opy_ = [
  bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭Ắ"),
  bstack111ll_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫắ"),
  bstack111ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨẰ"),
  bstack111ll_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶࠪằ"),
  bstack111ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭Ẳ"),
  bstack111ll_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻࠪẳ"),
  bstack111ll_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩẴ"),
  bstack111ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬẵ"),
  bstack111ll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭Ặ"),
  bstack111ll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪặ"),
  bstack111ll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩẸ"),
  bstack111ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬẹ"),
]
bstack1lll11l1ll_opy_ = [
  bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩẺ"),
  bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪẻ"),
  bstack111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭Ẽ"),
  bstack111ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨẽ"),
  bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬẾ"),
  bstack111ll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬế"),
  bstack111ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧỀ"),
  bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩề"),
  bstack111ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩỂ"),
  bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬể"),
  bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬỄ"),
  bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࠩễ"),
  bstack111ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬỆ"),
  bstack111ll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡘࡦ࡭ࠧệ"),
  bstack111ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩỈ"),
  bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨỉ"),
  bstack111ll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫỊ"),
  bstack111ll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠷ࠧị"),
  bstack111ll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠲ࠨỌ"),
  bstack111ll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠴ࠩọ"),
  bstack111ll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠶ࠪỎ"),
  bstack111ll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠸ࠫỏ"),
  bstack111ll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠺ࠬỐ"),
  bstack111ll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠼࠭ố"),
  bstack111ll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠾ࠧỒ"),
  bstack111ll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠹ࠨồ"),
  bstack111ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩỔ"),
  bstack111ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪổ"),
  bstack111ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨỖ"),
  bstack111ll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨỗ"),
  bstack111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫỘ"),
  bstack111ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬộ"),
  bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭Ớ"),
  bstack111ll_opy_ (u"ࠪ࡬ࡺࡨࡒࡦࡩ࡬ࡳࡳ࠭ớ")
]
bstack1111111l11l_opy_ = [
  bstack111ll_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩỜ"),
  bstack111ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧờ"),
  bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩỞ"),
  bstack111ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬở"),
  bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡖࡲࡪࡱࡵ࡭ࡹࡿࠧỠ"),
  bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬỡ"),
  bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡤ࡫ࠬỢ"),
  bstack111ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩợ"),
  bstack111ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧỤ"),
  bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫụ"),
  bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨỦ"),
  bstack111ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧủ"),
  bstack111ll_opy_ (u"ࠩࡲࡷࠬỨ"),
  bstack111ll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ứ"),
  bstack111ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪỪ"),
  bstack111ll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧừ"),
  bstack111ll_opy_ (u"࠭ࡲࡦࡩ࡬ࡳࡳ࠭Ử"),
  bstack111ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩử"),
  bstack111ll_opy_ (u"ࠨ࡯ࡤࡧ࡭࡯࡮ࡦࠩỮ"),
  bstack111ll_opy_ (u"ࠩࡵࡩࡸࡵ࡬ࡶࡶ࡬ࡳࡳ࠭ữ"),
  bstack111ll_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨỰ"),
  bstack111ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨự"),
  bstack111ll_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫỲ"),
  bstack111ll_opy_ (u"࠭࡮ࡰࡒࡤ࡫ࡪࡒ࡯ࡢࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪỳ"),
  bstack111ll_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨỴ"),
  bstack111ll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧỵ"),
  bstack111ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭Ỷ"),
  bstack111ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡩࡳࡪࡋࡦࡻࡶࠫỷ"),
  bstack111ll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨỸ"),
  bstack111ll_opy_ (u"ࠬࡴ࡯ࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠩỹ"),
  bstack111ll_opy_ (u"࠭ࡣࡩࡧࡦ࡯࡚ࡘࡌࠨỺ"),
  bstack111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩỻ"),
  bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡄࡱࡲ࡯࡮࡫ࡳࠨỼ"),
  bstack111ll_opy_ (u"ࠩࡦࡥࡵࡺࡵࡳࡧࡆࡶࡦࡹࡨࠨỽ"),
  bstack111ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧỾ"),
  bstack111ll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫỿ"),
  bstack111ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡘࡨࡶࡸ࡯࡯࡯ࠩἀ"),
  bstack111ll_opy_ (u"࠭࡮ࡰࡄ࡯ࡥࡳࡱࡐࡰ࡮࡯࡭ࡳ࡭ࠧἁ"),
  bstack111ll_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭ἂ"),
  bstack111ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡍࡱࡪࡷࠬἃ"),
  bstack111ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡋࡧࠫἄ"),
  bstack111ll_opy_ (u"ࠪࡨࡪࡪࡩࡤࡣࡷࡩࡩࡊࡥࡷ࡫ࡦࡩࠬἅ"),
  bstack111ll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡔࡦࡸࡡ࡮ࡵࠪἆ"),
  bstack111ll_opy_ (u"ࠬࡶࡨࡰࡰࡨࡒࡺࡳࡢࡦࡴࠪἇ"),
  bstack111ll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫἈ"),
  bstack111ll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡔࡶࡴࡪࡱࡱࡷࠬἉ"),
  bstack111ll_opy_ (u"ࠨࡥࡲࡲࡸࡵ࡬ࡦࡎࡲ࡫ࡸ࠭Ἂ"),
  bstack111ll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩἋ"),
  bstack111ll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧἌ"),
  bstack111ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡆ࡮ࡵ࡭ࡦࡶࡵ࡭ࡨ࠭Ἅ"),
  bstack111ll_opy_ (u"ࠬࡼࡩࡥࡧࡲ࡚࠷࠭Ἆ"),
  bstack111ll_opy_ (u"࠭࡭ࡪࡦࡖࡩࡸࡹࡩࡰࡰࡌࡲࡸࡺࡡ࡭࡮ࡄࡴࡵࡹࠧἏ"),
  bstack111ll_opy_ (u"ࠧࡦࡵࡳࡶࡪࡹࡳࡰࡕࡨࡶࡻ࡫ࡲࠨἐ"),
  bstack111ll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧἑ"),
  bstack111ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡇࡩࡶࠧἒ"),
  bstack111ll_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪἓ"),
  bstack111ll_opy_ (u"ࠫࡸࡿ࡮ࡤࡖ࡬ࡱࡪ࡝ࡩࡵࡪࡑࡘࡕ࠭ἔ"),
  bstack111ll_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪἕ"),
  bstack111ll_opy_ (u"࠭ࡧࡱࡵࡏࡳࡨࡧࡴࡪࡱࡱࠫ἖"),
  bstack111ll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨ἗"),
  bstack111ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨἘ"),
  bstack111ll_opy_ (u"ࠩࡩࡳࡷࡩࡥࡄࡪࡤࡲ࡬࡫ࡊࡢࡴࠪἙ"),
  bstack111ll_opy_ (u"ࠪࡼࡲࡹࡊࡢࡴࠪἚ"),
  bstack111ll_opy_ (u"ࠫࡽࡳࡸࡋࡣࡵࠫἛ"),
  bstack111ll_opy_ (u"ࠬࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫἜ"),
  bstack111ll_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭Ἕ"),
  bstack111ll_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ἞"),
  bstack111ll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫ἟"),
  bstack111ll_opy_ (u"ࠩࡤࡴࡵ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ἠ"),
  bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩἡ"),
  bstack111ll_opy_ (u"ࠫࡷ࡫ࡳࡪࡩࡱࡅࡵࡶࠧἢ"),
  bstack111ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࡴࠩἣ"),
  bstack111ll_opy_ (u"࠭ࡣࡢࡰࡤࡶࡾ࠭ἤ"),
  bstack111ll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨἥ"),
  bstack111ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨἦ"),
  bstack111ll_opy_ (u"ࠩ࡬ࡩࠬἧ"),
  bstack111ll_opy_ (u"ࠪࡩࡩ࡭ࡥࠨἨ"),
  bstack111ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫἩ"),
  bstack111ll_opy_ (u"ࠬࡷࡵࡦࡷࡨࠫἪ"),
  bstack111ll_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨἫ"),
  bstack111ll_opy_ (u"ࠧࡢࡲࡳࡗࡹࡵࡲࡦࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠨἬ"),
  bstack111ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡄࡣࡰࡩࡷࡧࡉ࡮ࡣࡪࡩࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧἭ"),
  bstack111ll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡅࡹࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬἮ"),
  bstack111ll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡊࡰࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭Ἧ"),
  bstack111ll_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨἰ"),
  bstack111ll_opy_ (u"ࠬࡸࡥࡴࡧࡵࡺࡪࡊࡥࡷ࡫ࡦࡩࠬἱ"),
  bstack111ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ἲ"),
  bstack111ll_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩἳ"),
  bstack111ll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡣࡶࡷࡨࡵࡤࡦࠩἴ"),
  bstack111ll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡋࡲࡷࡉ࡫ࡶࡪࡥࡨࡗࡪࡺࡴࡪࡰࡪࡷࠬἵ"),
  bstack111ll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡹࡩ࡯࡯ࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪἶ"),
  bstack111ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡵࡶ࡬ࡦࡒࡤࡽࠬἷ"),
  bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭Ἰ"),
  bstack111ll_opy_ (u"࠭ࡷࡥ࡫ࡲࡗࡪࡸࡶࡪࡥࡨࠫἹ"),
  bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩἺ"),
  bstack111ll_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵࡅࡵࡳࡸࡹࡓࡪࡶࡨࡘࡷࡧࡣ࡬࡫ࡱ࡫ࠬἻ"),
  bstack111ll_opy_ (u"ࠩ࡫࡭࡬࡮ࡃࡰࡰࡷࡶࡦࡹࡴࠨἼ"),
  bstack111ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡓࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࡹࠧἽ"),
  bstack111ll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧἾ"),
  bstack111ll_opy_ (u"ࠬࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩἿ"),
  bstack111ll_opy_ (u"࠭ࡲࡦ࡯ࡲࡺࡪࡏࡏࡔࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࡒ࡯ࡤࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫὀ"),
  bstack111ll_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩὁ"),
  bstack111ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪὂ"),
  bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫὃ"),
  bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩὄ"),
  bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ὅ"),
  bstack111ll_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨ὆"),
  bstack111ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ὇"),
  bstack111ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡴࡻࡴࡴࠩὈ"),
  bstack111ll_opy_ (u"ࠨࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡔࡷࡵ࡭ࡱࡶࡅࡩ࡭ࡧࡶࡪࡱࡵࠫὉ")
]
bstack1ll11l11_opy_ = {
  bstack111ll_opy_ (u"ࠩࡹࠫὊ"): bstack111ll_opy_ (u"ࠪࡺࠬὋ"),
  bstack111ll_opy_ (u"ࠫ࡫࠭Ὄ"): bstack111ll_opy_ (u"ࠬ࡬ࠧὍ"),
  bstack111ll_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬ὎"): bstack111ll_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭὏"),
  bstack111ll_opy_ (u"ࠨࡱࡱࡰࡾࡧࡵࡵࡱࡰࡥࡹ࡫ࠧὐ"): bstack111ll_opy_ (u"ࠩࡲࡲࡱࡿࡁࡶࡶࡲࡱࡦࡺࡥࠨὑ"),
  bstack111ll_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧὒ"): bstack111ll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨὓ"),
  bstack111ll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨὔ"): bstack111ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩὕ"),
  bstack111ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪὖ"): bstack111ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫὗ"),
  bstack111ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬ὘"): bstack111ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭Ὑ"),
  bstack111ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧ὚"): bstack111ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨὛ"),
  bstack111ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧ὜"): bstack111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡌࡴࡹࡴࠨὝ"),
  bstack111ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩ὞"): bstack111ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖ࡯ࡳࡶࠪὟ"),
  bstack111ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫὠ"): bstack111ll_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ὡ"),
  bstack111ll_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧὢ"): bstack111ll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨὣ"),
  bstack111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨὤ"): bstack111ll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪὥ"),
  bstack111ll_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫὦ"): bstack111ll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬὧ"),
  bstack111ll_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨὨ"): bstack111ll_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩὩ"),
  bstack111ll_opy_ (u"࠭ࡰࡢࡥࡩ࡭ࡱ࡫ࠧὪ"): bstack111ll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪὫ"),
  bstack111ll_opy_ (u"ࠨࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪὬ"): bstack111ll_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬὭ"),
  bstack111ll_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭Ὦ"): bstack111ll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧὯ"),
  bstack111ll_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭ὰ"): bstack111ll_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧά"),
  bstack111ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩὲ"): bstack111ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪέ"),
  bstack111ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫὴ"): bstack111ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࠫή")
}
bstack111111l1ll1_opy_ = bstack111ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡩࡵࡪࡸࡦ࠳ࡩ࡯࡮࠱ࡳࡩࡷࡩࡹ࠰ࡥ࡯࡭࠴ࡸࡥ࡭ࡧࡤࡷࡪࡹ࠯࡭ࡣࡷࡩࡸࡺ࠯ࡥࡱࡺࡲࡱࡵࡡࡥࠤὶ")
bstack1111111ll1l_opy_ = bstack111ll_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠴࡮ࡥࡢ࡮ࡷ࡬ࡨ࡮ࡥࡤ࡭ࠥί")
bstack11l11111_opy_ = bstack111ll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡦࡦࡶ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡴࡧࡱࡨࡤࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤὸ")
bstack1ll111l1ll_opy_ = bstack111ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡹࡧ࠳࡭ࡻࡢࠨό")
bstack111111l1l_opy_ = bstack111ll_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠫὺ")
bstack11l1111l1l_opy_ = bstack111ll_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠺࠴࠵࠶࠲ࡻࡩ࠵ࡨࡶࡤࠪύ")
bstack11lll1lll_opy_ = bstack111ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡳ࡫ࡸࡵࡡ࡫ࡹࡧࡹࠧὼ")
bstack1l11ll1lll_opy_ = {
  bstack111ll_opy_ (u"ࠫࡩ࡫ࡦࡢࡷ࡯ࡸࠬώ"): bstack111ll_opy_ (u"ࠬ࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ὾"),
  bstack111ll_opy_ (u"࠭ࡵࡴ࠯ࡨࡥࡸࡺࠧ὿"): bstack111ll_opy_ (u"ࠧࡩࡷࡥ࠱ࡺࡹࡥ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᾀ"),
  bstack111ll_opy_ (u"ࠨࡷࡶࠫᾁ"): bstack111ll_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡵࡴ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᾂ"),
  bstack111ll_opy_ (u"ࠪࡩࡺ࠭ᾃ"): bstack111ll_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡧࡸ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᾄ"),
  bstack111ll_opy_ (u"ࠬ࡯࡮ࠨᾅ"): bstack111ll_opy_ (u"࠭ࡨࡶࡤ࠰ࡥࡵࡹ࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᾆ"),
  bstack111ll_opy_ (u"ࠧࡢࡷࠪᾇ"): bstack111ll_opy_ (u"ࠨࡪࡸࡦ࠲ࡧࡰࡴࡧ࠰ࡳࡳࡲࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᾈ")
}
bstack11111111lll_opy_ = {
  bstack111ll_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫᾉ"): 50,
  bstack111ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᾊ"): 40,
  bstack111ll_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬᾋ"): 30,
  bstack111ll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᾌ"): 20,
  bstack111ll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᾍ"): 10
}
bstack1l11l1lll1_opy_ = bstack11111111lll_opy_[bstack111ll_opy_ (u"ࠧࡪࡰࡩࡳࠬᾎ")]
bstack1l1111111_opy_ = bstack111ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤ࠱ࠪᾏ")
bstack111l111l11_opy_ = bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᾐ")
bstack1l1l11l11l_opy_ = bstack111ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᾑ")
bstack1111ll11ll_opy_ = bstack111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪᾒ")
bstack1111l111l1_opy_ = bstack111ll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪᾓ")
bstack11l1l11ll1_opy_ = {
  bstack111ll_opy_ (u"࠭ࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࠫᾔ"): bstack111ll_opy_ (u"ࠧࠫࠬ࠭ࠤࡠ࡙ࡄࡌ࠯ࡊࡉࡓ࠳࠰࠱࠷ࡠࠤࡥࡶࡹࡵࡧࡶࡸ࠲ࡶࡡࡳࡣ࡯ࡰࡪࡲࡠࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡪࡰࠣࡽࡴࡻࡲࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹ࠴ࠠࡕࡪ࡬ࡷࠥࡳࡡࡺࠢࡦࡥࡺࡹࡥࠡࡥࡲࡲ࡫ࡲࡩࡤࡶࡶࠤࡼ࡯ࡴࡩࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡵ࡯࡫ࡱࡷࡹࡧ࡬࡭ࠢ࡬ࡸࠥࡻࡳࡪࡰࡪ࠾ࠥࡶࡩࡱࠢࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡶࡡࡳࡣ࡯ࡰࡪࡲࠠࠫࠬ࠭ࠫᾕ")
}
bstack11111111ll1_opy_ = [bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩᾖ"), bstack111ll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩᾗ")]
bstack1111111lll1_opy_ = [bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᾘ"), bstack111ll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᾙ")]
bstack111ll11ll1_opy_ = re.compile(bstack111ll_opy_ (u"ࠬࡤ࡛࡝࡞ࡺ࠱ࡢ࠱࠺࠯ࠬࠧࠫᾚ"))
bstack111ll11l11_opy_ = [
  bstack111ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡑࡥࡲ࡫ࠧᾛ"),
  bstack111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᾜ"),
  bstack111ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᾝ"),
  bstack111ll_opy_ (u"ࠩࡱࡩࡼࡉ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᾞ"),
  bstack111ll_opy_ (u"ࠪࡥࡵࡶࠧᾟ"),
  bstack111ll_opy_ (u"ࠫࡺࡪࡩࡥࠩᾠ"),
  bstack111ll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᾡ"),
  bstack111ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࠭ᾢ"),
  bstack111ll_opy_ (u"ࠧࡰࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬᾣ"),
  bstack111ll_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࠭ᾤ"),
  bstack111ll_opy_ (u"ࠩࡱࡳࡗ࡫ࡳࡦࡶࠪᾥ"), bstack111ll_opy_ (u"ࠪࡪࡺࡲ࡬ࡓࡧࡶࡩࡹ࠭ᾦ"),
  bstack111ll_opy_ (u"ࠫࡨࡲࡥࡢࡴࡖࡽࡸࡺࡥ࡮ࡈ࡬ࡰࡪࡹࠧᾧ"),
  bstack111ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡘ࡮ࡳࡩ࡯ࡩࡶࠫᾨ"),
  bstack111ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࡏࡳ࡬࡭ࡩ࡯ࡩࠪᾩ"),
  bstack111ll_opy_ (u"ࠧࡰࡶ࡫ࡩࡷࡇࡰࡱࡵࠪᾪ"),
  bstack111ll_opy_ (u"ࠨࡲࡵ࡭ࡳࡺࡐࡢࡩࡨࡗࡴࡻࡲࡤࡧࡒࡲࡋ࡯࡮ࡥࡈࡤ࡭ࡱࡻࡲࡦࠩᾫ"),
  bstack111ll_opy_ (u"ࠩࡤࡴࡵࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧᾬ"), bstack111ll_opy_ (u"ࠪࡥࡵࡶࡐࡢࡥ࡮ࡥ࡬࡫ࠧᾭ"), bstack111ll_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡆࡩࡴࡪࡸ࡬ࡸࡾ࠭ᾮ"), bstack111ll_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡖࡡࡤ࡭ࡤ࡫ࡪ࠭ᾯ"), bstack111ll_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡄࡶࡴࡤࡸ࡮ࡵ࡮ࠨᾰ"),
  bstack111ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬᾱ"),
  bstack111ll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡔࡦࡵࡷࡔࡦࡩ࡫ࡢࡩࡨࡷࠬᾲ"),
  bstack111ll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡆࡳࡻ࡫ࡲࡢࡩࡨࠫᾳ"), bstack111ll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࡊࡴࡤࡊࡰࡷࡩࡳࡺࠧᾴ"),
  bstack111ll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩ᾵"),
  bstack111ll_opy_ (u"ࠬࡧࡤࡣࡒࡲࡶࡹ࠭ᾶ"),
  bstack111ll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪ࡙࡯ࡤ࡭ࡨࡸࠬᾷ"),
  bstack111ll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡊࡰࡶࡸࡦࡲ࡬ࡕ࡫ࡰࡩࡴࡻࡴࠨᾸ"),
  bstack111ll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡸ࡭࠭Ᾱ"),
  bstack111ll_opy_ (u"ࠩࡤࡺࡩ࠭Ὰ"), bstack111ll_opy_ (u"ࠪࡥࡻࡪࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭Ά"), bstack111ll_opy_ (u"ࠫࡦࡼࡤࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᾼ"), bstack111ll_opy_ (u"ࠬࡧࡶࡥࡃࡵ࡫ࡸ࠭᾽"),
  bstack111ll_opy_ (u"࠭ࡵࡴࡧࡎࡩࡾࡹࡴࡰࡴࡨࠫι"), bstack111ll_opy_ (u"ࠧ࡬ࡧࡼࡷࡹࡵࡲࡦࡒࡤࡸ࡭࠭᾿"), bstack111ll_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡸࡹࡷࡰࡴࡧࠫ῀"),
  bstack111ll_opy_ (u"ࠩ࡮ࡩࡾࡇ࡬ࡪࡣࡶࠫ῁"), bstack111ll_opy_ (u"ࠪ࡯ࡪࡿࡐࡢࡵࡶࡻࡴࡸࡤࠨῂ"),
  bstack111ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭ῃ"), bstack111ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡅࡷ࡭ࡳࠨῄ"), bstack111ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࡅ࡫ࡵࠫ῅"), bstack111ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡉࡨࡳࡱࡰࡩࡒࡧࡰࡱ࡫ࡱ࡫ࡋ࡯࡬ࡦࠩῆ"), bstack111ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡕࡴࡧࡖࡽࡸࡺࡥ࡮ࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࠬῇ"),
  bstack111ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡑࡱࡵࡸࠬῈ"), bstack111ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹࡹࠧΈ"),
  bstack111ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡇ࡭ࡸࡧࡢ࡭ࡧࡅࡹ࡮ࡲࡤࡄࡪࡨࡧࡰ࠭Ὴ"),
  bstack111ll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࡗ࡭ࡲ࡫࡯ࡶࡶࠪΉ"),
  bstack111ll_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡇࡣࡵ࡫ࡲࡲࠬῌ"), bstack111ll_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡃࡢࡶࡨ࡫ࡴࡸࡹࠨ῍"), bstack111ll_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡇ࡮ࡤ࡫ࡸ࠭῎"), bstack111ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡣ࡯ࡍࡳࡺࡥ࡯ࡶࡄࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ῏"),
  bstack111ll_opy_ (u"ࠪࡨࡴࡴࡴࡔࡶࡲࡴࡆࡶࡰࡐࡰࡕࡩࡸ࡫ࡴࠨῐ"),
  bstack111ll_opy_ (u"ࠫࡺࡴࡩࡤࡱࡧࡩࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ῑ"), bstack111ll_opy_ (u"ࠬࡸࡥࡴࡧࡷࡏࡪࡿࡢࡰࡣࡵࡨࠬῒ"),
  bstack111ll_opy_ (u"࠭࡮ࡰࡕ࡬࡫ࡳ࠭ΐ"),
  bstack111ll_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡕ࡯࡫ࡰࡴࡴࡸࡴࡢࡰࡷ࡚࡮࡫ࡷࡴࠩ῔"),
  bstack111ll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱࡨࡷࡵࡩࡥ࡙ࡤࡸࡨ࡮ࡥࡳࡵࠪ῕"),
  bstack111ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩῖ"),
  bstack111ll_opy_ (u"ࠪࡶࡪࡩࡲࡦࡣࡷࡩࡈ࡮ࡲࡰ࡯ࡨࡈࡷ࡯ࡶࡦࡴࡖࡩࡸࡹࡩࡰࡰࡶࠫῗ"),
  bstack111ll_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪῘ"),
  bstack111ll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡒࡤࡸ࡭࠭Ῑ"),
  bstack111ll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡓࡱࡧࡨࡨࠬῚ"),
  bstack111ll_opy_ (u"ࠧࡨࡲࡶࡉࡳࡧࡢ࡭ࡧࡧࠫΊ"),
  bstack111ll_opy_ (u"ࠨ࡫ࡶࡌࡪࡧࡤ࡭ࡧࡶࡷࠬ῜"),
  bstack111ll_opy_ (u"ࠩࡤࡨࡧࡋࡸࡦࡥࡗ࡭ࡲ࡫࡯ࡶࡶࠪ῝"),
  bstack111ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࡖࡧࡷ࡯ࡰࡵࠩ῞"),
  bstack111ll_opy_ (u"ࠫࡸࡱࡩࡱࡆࡨࡺ࡮ࡩࡥࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨ῟"),
  bstack111ll_opy_ (u"ࠬࡧࡵࡵࡱࡊࡶࡦࡴࡴࡑࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠬῠ"),
  bstack111ll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡎࡢࡶࡸࡶࡦࡲࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫῡ"),
  bstack111ll_opy_ (u"ࠧࡴࡻࡶࡸࡪࡳࡐࡰࡴࡷࠫῢ"),
  bstack111ll_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡦࡥࡌࡴࡹࡴࠨΰ"),
  bstack111ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡕ࡯࡮ࡲࡧࡰ࠭ῤ"), bstack111ll_opy_ (u"ࠪࡹࡳࡲ࡯ࡤ࡭ࡗࡽࡵ࡫ࠧῥ"), bstack111ll_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡏࡪࡿࠧῦ"),
  bstack111ll_opy_ (u"ࠬࡧࡵࡵࡱࡏࡥࡺࡴࡣࡩࠩῧ"),
  bstack111ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡣࡢࡶࡆࡥࡵࡺࡵࡳࡧࠪῨ"),
  bstack111ll_opy_ (u"ࠧࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࡒࡸ࡭࡫ࡲࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩῩ"),
  bstack111ll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦ࡙࡬ࡲࡩࡵࡷࡂࡰ࡬ࡱࡦࡺࡩࡰࡰࠪῪ"),
  bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡕࡱࡲࡰࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ύ"),
  bstack111ll_opy_ (u"ࠪࡩࡳ࡬࡯ࡳࡥࡨࡅࡵࡶࡉ࡯ࡵࡷࡥࡱࡲࠧῬ"),
  bstack111ll_opy_ (u"ࠫࡪࡴࡳࡶࡴࡨ࡛ࡪࡨࡶࡪࡧࡺࡷࡍࡧࡶࡦࡒࡤ࡫ࡪࡹࠧ῭"), bstack111ll_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡊࡥࡷࡶࡲࡳࡱࡹࡐࡰࡴࡷࠫ΅"), bstack111ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡊࡥࡵࡣ࡬ࡰࡸࡉ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠩ`"),
  bstack111ll_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫ࡁࡱࡲࡶࡇࡦࡩࡨࡦࡎ࡬ࡱ࡮ࡺࠧ῰"),
  bstack111ll_opy_ (u"ࠨࡥࡤࡰࡪࡴࡤࡢࡴࡉࡳࡷࡳࡡࡵࠩ῱"),
  bstack111ll_opy_ (u"ࠩࡥࡹࡳࡪ࡬ࡦࡋࡧࠫῲ"),
  bstack111ll_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪῳ"),
  bstack111ll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࡙ࡥࡳࡸ࡬ࡧࡪࡹࡅ࡯ࡣࡥࡰࡪࡪࠧῴ"), bstack111ll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡂࡷࡷ࡬ࡴࡸࡩࡻࡧࡧࠫ῵"),
  bstack111ll_opy_ (u"࠭ࡡࡶࡶࡲࡅࡨࡩࡥࡱࡶࡄࡰࡪࡸࡴࡴࠩῶ"), bstack111ll_opy_ (u"ࠧࡢࡷࡷࡳࡉ࡯ࡳ࡮࡫ࡶࡷࡆࡲࡥࡳࡶࡶࠫῷ"),
  bstack111ll_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡊࡰࡶࡸࡷࡻ࡭ࡦࡰࡷࡷࡑ࡯ࡢࠨῸ"),
  bstack111ll_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦ࡙ࡧࡰࠨΌ"),
  bstack111ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌࡲ࡮ࡺࡩࡢ࡮ࡘࡶࡱ࠭Ὼ"), bstack111ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡅࡱࡲ࡯ࡸࡒࡲࡴࡺࡶࡳࠨΏ"), bstack111ll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎ࡭࡮ࡰࡴࡨࡊࡷࡧࡵࡥ࡙ࡤࡶࡳ࡯࡮ࡨࠩῼ"), bstack111ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡦࡰࡏ࡭ࡳࡱࡳࡊࡰࡅࡥࡨࡱࡧࡳࡱࡸࡲࡩ࠭´"),
  bstack111ll_opy_ (u"ࠧ࡬ࡧࡨࡴࡐ࡫ࡹࡄࡪࡤ࡭ࡳࡹࠧ῾"),
  bstack111ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡻࡣࡥࡰࡪ࡙ࡴࡳ࡫ࡱ࡫ࡸࡊࡩࡳࠩ῿"),
  bstack111ll_opy_ (u"ࠩࡳࡶࡴࡩࡥࡴࡵࡄࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ "),
  bstack111ll_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡍࡨࡽࡉ࡫࡬ࡢࡻࠪ "),
  bstack111ll_opy_ (u"ࠫࡸ࡮࡯ࡸࡋࡒࡗࡑࡵࡧࠨ "),
  bstack111ll_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧ "),
  bstack111ll_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡘࡥࡴࡲࡲࡲࡸ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧ "), bstack111ll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷ࡛ࡦ࡯ࡴࡕ࡫ࡰࡩࡴࡻࡴࠨ "),
  bstack111ll_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࠫ "),
  bstack111ll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡶࡽࡳࡩࡅࡹࡧࡦࡹࡹ࡫ࡆࡳࡱࡰࡌࡹࡺࡰࡴࠩ "),
  bstack111ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡇࡦࡶࡴࡶࡴࡨࠫ "),
  bstack111ll_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫ "),
  bstack111ll_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡆࡳࡳࡺࡥࡹࡶࡏ࡭ࡸࡺࠧ "),
  bstack111ll_opy_ (u"࠭ࡷࡢ࡫ࡷࡊࡴࡸࡁࡱࡲࡖࡧࡷ࡯ࡰࡵࠩ​"),
  bstack111ll_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡄࡱࡱࡲࡪࡩࡴࡓࡧࡷࡶ࡮࡫ࡳࠨ‌"),
  bstack111ll_opy_ (u"ࠨࡣࡳࡴࡓࡧ࡭ࡦࠩ‍"),
  bstack111ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡖࡐࡈ࡫ࡲࡵࠩ‎"),
  bstack111ll_opy_ (u"ࠪࡸࡦࡶࡗࡪࡶ࡫ࡗ࡭ࡵࡲࡵࡒࡵࡩࡸࡹࡄࡶࡴࡤࡸ࡮ࡵ࡮ࠨ‏"),
  bstack111ll_opy_ (u"ࠫࡸࡩࡡ࡭ࡧࡉࡥࡨࡺ࡯ࡳࠩ‐"),
  bstack111ll_opy_ (u"ࠬࡽࡤࡢࡎࡲࡧࡦࡲࡐࡰࡴࡷࠫ‑"),
  bstack111ll_opy_ (u"࠭ࡳࡩࡱࡺ࡜ࡨࡵࡤࡦࡎࡲ࡫ࠬ‒"),
  bstack111ll_opy_ (u"ࠧࡪࡱࡶࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡻࡳࡦࠩ–"),
  bstack111ll_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡃࡰࡰࡩ࡭࡬ࡌࡩ࡭ࡧࠪ—"),
  bstack111ll_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡹࡳࡸࡱࡵࡨࠬ―"),
  bstack111ll_opy_ (u"ࠪࡹࡸ࡫ࡐࡳࡧࡥࡹ࡮ࡲࡴࡘࡆࡄࠫ‖"),
  bstack111ll_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸ࡜ࡊࡁࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠬ‗"),
  bstack111ll_opy_ (u"ࠬࡽࡥࡣࡆࡵ࡭ࡻ࡫ࡲࡂࡩࡨࡲࡹ࡛ࡲ࡭ࠩ‘"),
  bstack111ll_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡷ࡬ࠬ’"),
  bstack111ll_opy_ (u"ࠧࡶࡵࡨࡒࡪࡽࡗࡅࡃࠪ‚"),
  bstack111ll_opy_ (u"ࠨࡹࡧࡥࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫ‛"), bstack111ll_opy_ (u"ࠩࡺࡨࡦࡉ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࡖ࡬ࡱࡪࡵࡵࡵࠩ“"),
  bstack111ll_opy_ (u"ࠪࡼࡨࡵࡤࡦࡑࡵ࡫ࡎࡪࠧ”"), bstack111ll_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡖ࡭࡬ࡴࡩ࡯ࡩࡌࡨࠬ„"),
  bstack111ll_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩ࡝ࡄࡂࡄࡸࡲࡩࡲࡥࡊࡦࠪ‟"),
  bstack111ll_opy_ (u"࠭ࡲࡦࡵࡨࡸࡔࡴࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡵࡸࡔࡴ࡬ࡺࠩ†"),
  bstack111ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࡴࠩ‡"),
  bstack111ll_opy_ (u"ࠨࡹࡧࡥࡘࡺࡡࡳࡶࡸࡴࡗ࡫ࡴࡳ࡫ࡨࡷࠬ•"), bstack111ll_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴࡼࡍࡳࡺࡥࡳࡸࡤࡰࠬ‣"),
  bstack111ll_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࡌࡦࡸࡤࡸࡣࡵࡩࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭․"),
  bstack111ll_opy_ (u"ࠫࡲࡧࡸࡕࡻࡳ࡭ࡳ࡭ࡆࡳࡧࡴࡹࡪࡴࡣࡺࠩ‥"),
  bstack111ll_opy_ (u"ࠬࡹࡩ࡮ࡲ࡯ࡩࡎࡹࡖࡪࡵ࡬ࡦࡱ࡫ࡃࡩࡧࡦ࡯ࠬ…"),
  bstack111ll_opy_ (u"࠭ࡵࡴࡧࡆࡥࡷࡺࡨࡢࡩࡨࡗࡸࡲࠧ‧"),
  bstack111ll_opy_ (u"ࠧࡴࡪࡲࡹࡱࡪࡕࡴࡧࡖ࡭ࡳ࡭࡬ࡦࡶࡲࡲ࡙࡫ࡳࡵࡏࡤࡲࡦ࡭ࡥࡳࠩ "),
  bstack111ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡉࡘࡆࡓࠫ "),
  bstack111ll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡱࡸࡧ࡭ࡏࡤࡆࡰࡵࡳࡱࡲࠧ‪"),
  bstack111ll_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡋ࡭ࡩࡪࡥ࡯ࡃࡳ࡭ࡕࡵ࡬ࡪࡥࡼࡉࡷࡸ࡯ࡳࠩ‫"),
  bstack111ll_opy_ (u"ࠫࡲࡵࡣ࡬ࡎࡲࡧࡦࡺࡩࡰࡰࡄࡴࡵ࠭‬"),
  bstack111ll_opy_ (u"ࠬࡲ࡯ࡨࡥࡤࡸࡋࡵࡲ࡮ࡣࡷࠫ‭"), bstack111ll_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌࡩ࡭ࡶࡨࡶࡘࡶࡥࡤࡵࠪ‮"),
  bstack111ll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡊࡥ࡭ࡣࡼࡅࡩࡨࠧ "),
  bstack111ll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡋࡧࡐࡴࡩࡡࡵࡱࡵࡅࡺࡺ࡯ࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠫ‰")
]
bstack11l1l11lll_opy_ = bstack111ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡷࡳࡰࡴࡧࡤࠨ‱")
bstack1lll111l_opy_ = [bstack111ll_opy_ (u"ࠪ࠲ࡦࡶ࡫ࠨ′"), bstack111ll_opy_ (u"ࠫ࠳ࡧࡡࡣࠩ″"), bstack111ll_opy_ (u"ࠬ࠴ࡩࡱࡣࠪ‴")]
bstack11lllll1l1_opy_ = [bstack111ll_opy_ (u"࠭ࡩࡥࠩ‵"), bstack111ll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ‶"), bstack111ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ‷"), bstack111ll_opy_ (u"ࠩࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤࠨ‸")]
bstack11l11l11l_opy_ = {
  bstack111ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ‹"): bstack111ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ›"),
  bstack111ll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭※"): bstack111ll_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ‼"),
  bstack111ll_opy_ (u"ࠧࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ‽"): bstack111ll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ‾"),
  bstack111ll_opy_ (u"ࠩ࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ‿"): bstack111ll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⁀"),
  bstack111ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵࡺࡩࡰࡰࡶࠫ⁁"): bstack111ll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭⁂")
}
bstack1lll1111l1_opy_ = [
  bstack111ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ⁃"),
  bstack111ll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ⁄"),
  bstack111ll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⁅"),
  bstack111ll_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ⁆"),
  bstack111ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ⁇"),
]
bstack1l11ll111_opy_ = bstack1lll11l1ll_opy_ + bstack1111111l11l_opy_ + bstack111ll11l11_opy_
bstack11l111l11l_opy_ = [
  bstack111ll_opy_ (u"ࠫࡣࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴࠥࠩ⁈"),
  bstack111ll_opy_ (u"ࠬࡤࡢࡴ࠯࡯ࡳࡨࡧ࡬࠯ࡥࡲࡱࠩ࠭⁉"),
  bstack111ll_opy_ (u"࠭࡞࠲࠴࠺࠲ࠬ⁊"),
  bstack111ll_opy_ (u"ࠧ࡟࠳࠳࠲ࠬ⁋"),
  bstack111ll_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠱࡜࠸࠰࠽ࡢ࠴ࠧ⁌"),
  bstack111ll_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠳࡝࠳࠱࠾ࡣ࠮ࠨ⁍"),
  bstack111ll_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠵࡞࠴࠲࠷࡝࠯ࠩ⁎"),
  bstack111ll_opy_ (u"ࠫࡣ࠷࠹࠳࠰࠴࠺࠽࠴ࠧ⁏")
]
bstack1111l11111l_opy_ = bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭⁐")
bstack111l1l1l1_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠲ࡺ࠶࠵ࡥࡷࡧࡱࡸࠬ⁑")
bstack11llll1ll_opy_ = [ bstack111ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ⁒") ]
bstack11lllllll_opy_ = [ bstack111ll_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⁓") ]
bstack1ll1l111l_opy_ = [bstack111ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⁔")]
bstack111ll111l1_opy_ = [ bstack111ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⁕") ]
bstack1llll11l_opy_ = bstack111ll_opy_ (u"ࠫࡘࡊࡋࡔࡧࡷࡹࡵ࠭⁖")
bstack1lll11l11_opy_ = bstack111ll_opy_ (u"࡙ࠬࡄࡌࡖࡨࡷࡹࡇࡴࡵࡧࡰࡴࡹ࡫ࡤࠨ⁗")
bstack11l1ll1l1l_opy_ = bstack111ll_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠪ⁘")
bstack1l1l1l1l1l_opy_ = bstack111ll_opy_ (u"ࠧ࠵࠰࠳࠲࠵࠭⁙")
bstack11l1llll_opy_ = [
  bstack111ll_opy_ (u"ࠨࡇࡕࡖࡤࡌࡁࡊࡎࡈࡈࠬ⁚"),
  bstack111ll_opy_ (u"ࠩࡈࡖࡗࡥࡔࡊࡏࡈࡈࡤࡕࡕࡕࠩ⁛"),
  bstack111ll_opy_ (u"ࠪࡉࡗࡘ࡟ࡃࡎࡒࡇࡐࡋࡄࡠࡄ࡜ࡣࡈࡒࡉࡆࡐࡗࠫ⁜"),
  bstack111ll_opy_ (u"ࠫࡊࡘࡒࡠࡐࡈࡘ࡜ࡕࡒࡌࡡࡆࡌࡆࡔࡇࡆࡆࠪ⁝"),
  bstack111ll_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡅࡕࡡࡑࡓ࡙ࡥࡃࡐࡐࡑࡉࡈ࡚ࡅࡅࠩ⁞"),
  bstack111ll_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡄࡎࡒࡗࡊࡊࠧ "),
  bstack111ll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡔࡈࡗࡊ࡚ࠧ⁠"),
  bstack111ll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡋ࡛ࡓࡆࡆࠪ⁡"),
  bstack111ll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡅࡇࡕࡒࡕࡇࡇࠫ⁢"),
  bstack111ll_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫ⁣"),
  bstack111ll_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡎࡐࡖࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࠬ⁤"),
  bstack111ll_opy_ (u"ࠬࡋࡒࡓࡡࡄࡈࡉࡘࡅࡔࡕࡢࡍࡓ࡜ࡁࡍࡋࡇࠫ⁥"),
  bstack111ll_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣ࡚ࡔࡒࡆࡃࡆࡌࡆࡈࡌࡆࠩ⁦"),
  bstack111ll_opy_ (u"ࠧࡆࡔࡕࡣ࡙࡛ࡎࡏࡇࡏࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨ⁧"),
  bstack111ll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡗࡍࡒࡋࡄࡠࡑࡘࡘࠬ⁨"),
  bstack111ll_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡗࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ⁩"),
  bstack111ll_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡌࡔ࡙ࡔࡠࡗࡑࡖࡊࡇࡃࡉࡃࡅࡐࡊ࠭⁪"),
  bstack111ll_opy_ (u"ࠫࡊࡘࡒࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫ⁫"),
  bstack111ll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭⁬"),
  bstack111ll_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡔࡈࡗࡔࡒࡕࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ⁭"),
  bstack111ll_opy_ (u"ࠧࡆࡔࡕࡣࡒࡇࡎࡅࡃࡗࡓࡗ࡟࡟ࡑࡔࡒ࡜࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭⁮"),
]
bstack1l11lll11_opy_ = bstack111ll_opy_ (u"ࠨ࠰࠲ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡤࡶࡹ࡯ࡦࡢࡥࡷࡷ࠴࠭⁯")
bstack1l1lll11_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠩࢁࠫ⁰")), bstack111ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪⁱ"), bstack111ll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ⁲"))
bstack1111l1l1lll_opy_ = bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴ࡮࠭⁳")
bstack11111111l11_opy_ = [ bstack111ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⁴"), bstack111ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭⁵"), bstack111ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ⁶"), bstack111ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ⁷")]
bstack1111ll111_opy_ = [ bstack111ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⁸"), bstack111ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ⁹"), bstack111ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ⁺"), bstack111ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭⁻"), bstack111ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨ⁼") ]
bstack111111l1ll_opy_ = [ bstack111ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ⁽"), bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ⁾") ]
bstack1111111ll11_opy_ = [ bstack111ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪⁿ"), bstack111ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ₀") ]
bstack1l1l11lll_opy_ = 360
bstack11111lll1l1_opy_ = bstack111ll_opy_ (u"ࠧࡧࡰࡱ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧ₁")
bstack111111l11ll_opy_ = bstack111ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡫ࡶࡷࡺ࡫ࡳࠣ₂")
bstack111111ll1ll_opy_ = bstack111ll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠥ₃")
bstack1111l11l1l1_opy_ = bstack111ll_opy_ (u"ࠣࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡷࡩࡸࡺࡳࠡࡣࡵࡩࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡔ࡙ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠧࡶࠤࡦࡴࡤࠡࡣࡥࡳࡻ࡫ࠠࡧࡱࡵࠤࡆࡴࡤࡳࡱ࡬ࡨࠥࡪࡥࡷ࡫ࡦࡩࡸ࠴ࠢ₄")
bstack1111l11llll_opy_ = bstack111ll_opy_ (u"ࠤ࠴࠵࠳࠶ࠢ₅")
bstack1lll11l11l1_opy_ = {
  bstack111ll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ₆"): bstack111ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ₇"),
  bstack111ll_opy_ (u"ࠬࡌࡁࡊࡎࠪ₈"): bstack111ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭₉"),
  bstack111ll_opy_ (u"ࠧࡔࡍࡌࡔࠬ₊"): bstack111ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ₋")
}
bstack11lll1ll11_opy_ = [
  bstack111ll_opy_ (u"ࠤࡪࡩࡹࠨ₌"),
  bstack111ll_opy_ (u"ࠥ࡫ࡴࡈࡡࡤ࡭ࠥ₍"),
  bstack111ll_opy_ (u"ࠦ࡬ࡵࡆࡰࡴࡺࡥࡷࡪࠢ₎"),
  bstack111ll_opy_ (u"ࠧࡸࡥࡧࡴࡨࡷ࡭ࠨ₏"),
  bstack111ll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧₐ"),
  bstack111ll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦₑ"),
  bstack111ll_opy_ (u"ࠣࡵࡸࡦࡲ࡯ࡴࡆ࡮ࡨࡱࡪࡴࡴࠣₒ"),
  bstack111ll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨₓ"),
  bstack111ll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨₔ"),
  bstack111ll_opy_ (u"ࠦࡨࡲࡥࡢࡴࡈࡰࡪࡳࡥ࡯ࡶࠥₕ"),
  bstack111ll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࡸࠨₖ"),
  bstack111ll_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹࠨₗ"),
  bstack111ll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡂࡵࡼࡲࡨ࡙ࡣࡳ࡫ࡳࡸࠧₘ"),
  bstack111ll_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢₙ"),
  bstack111ll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢₚ"),
  bstack111ll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡘࡴࡻࡣࡩࡃࡦࡸ࡮ࡵ࡮ࠣₛ"),
  bstack111ll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡒࡻ࡬ࡵ࡫ࡗࡳࡺࡩࡨࠣₜ"),
  bstack111ll_opy_ (u"ࠧࡹࡨࡢ࡭ࡨࠦ₝"),
  bstack111ll_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࡆࡶࡰࠣ₞")
]
bstack111111l1l1l_opy_ = [
  bstack111ll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨ₟"),
  bstack111ll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ₠"),
  bstack111ll_opy_ (u"ࠤࡤࡹࡹࡵࠢ₡"),
  bstack111ll_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥ₢"),
  bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ₣")
]
bstack1lll1lll_opy_ = {
  bstack111ll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦ₤"): [bstack111ll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ₥")],
  bstack111ll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ₦"): [bstack111ll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ₧")],
  bstack111ll_opy_ (u"ࠤࡤࡹࡹࡵࠢ₨"): [bstack111ll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢ₩"), bstack111ll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢ₪"), bstack111ll_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ₫"), bstack111ll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ€")],
  bstack111ll_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢ₭"): [bstack111ll_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣ₮")],
  bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ₯"): [bstack111ll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ₰")],
}
bstack11111111l1l_opy_ = {
  bstack111ll_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ₱"): bstack111ll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦ₲"),
  bstack111ll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ₳"): bstack111ll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ₴"),
  bstack111ll_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ₵"): bstack111ll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦ₶"),
  bstack111ll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨ₷"): bstack111ll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨ₸"),
  bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ₹"): bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ₺")
}
bstack1lll1l1l1ll_opy_ = {
  bstack111ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ₻"): bstack111ll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡔࡧࡷࡹࡵ࠭₼"),
  bstack111ll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ₽"): bstack111ll_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡗࡩࡦࡸࡤࡰࡹࡱࠫ₾"),
  bstack111ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ₿"): bstack111ll_opy_ (u"࡚ࠬࡥࡴࡶࠣࡗࡪࡺࡵࡱࠩ⃀"),
  bstack111ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⃁"): bstack111ll_opy_ (u"ࠧࡕࡧࡶࡸ࡚ࠥࡥࡢࡴࡧࡳࡼࡴࠧ⃂")
}
bstack111111ll11l_opy_ = 65536
bstack111111ll111_opy_ = bstack111ll_opy_ (u"ࠨ࠰࠱࠲ࡠ࡚ࡒࡖࡐࡆࡅ࡙ࡋࡄ࡞ࠩ⃃")
bstack111111lll1l_opy_ = [
      bstack111ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ⃄"), bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭⃅"), bstack111ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⃆"), bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⃇"), bstack111ll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ⃈"),
      bstack111ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ⃉"), bstack111ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ⃊"), bstack111ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ⃋"), bstack111ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫ⃌"),
      bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ⃍"), bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ⃎"), bstack111ll_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩ⃏"), bstack111ll_opy_ (u"ࠧࡶࡵࡨࡶࡤࡪࡡࡵࡣࠪ⃐"), bstack111ll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ⃑"),
      bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷ⃒࠭"), bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡮ࡩࡾ⃓࠭"), bstack111ll_opy_ (u"ࠫ࡯ࡽࡴࠨ⃔")
    ]
bstack1111111l111_opy_= {
  bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⃕"): bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⃖"),
  bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ⃗"): bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷ⃘ࠬ"),
  bstack111ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ⃙"): bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹ⃚ࠧ"),
  bstack111ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ⃛"): bstack111ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⃜"),
  bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⃝"): bstack111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⃞"),
  bstack111ll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ⃟"): bstack111ll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ⃠"),
  bstack111ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⃡"): bstack111ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⃢"),
  bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⃣"): bstack111ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⃤"),
  bstack111ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭⃥ࠪ"): bstack111ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮⃦ࠫ"),
  bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ⃧"): bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ⃨"),
  bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⃩"): bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ⃪ࠩ"),
  bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬⃫࠭"): bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭⃬ࠧ"),
  bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ⃭ࠬ"): bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ⃮࠭"),
  bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࡒࡴࡹ࡯࡯࡯ࡵ⃯ࠪ"): bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫ⃰"),
  bstack111ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧ⃱"): bstack111ll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ⃲"),
  bstack111ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⃳"): bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⃴"),
  bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⃵"): bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⃶"),
  bstack111ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ⃷"): bstack111ll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩ⃸"),
  bstack111ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⃹"): bstack111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⃺"),
  bstack111ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⃻"): bstack111ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⃼"),
  bstack111ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭⃽"): bstack111ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ⃾"),
  bstack111ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ⃿"): bstack111ll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ℀"),
  bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ℁"): bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨℂ"),
  bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ℃"): bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ℄"),
  bstack111ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ℅"): bstack111ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ℆"),
  bstack111ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪℇ"): bstack111ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫ℈"),
  bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ℉"): bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ℊ"),
  bstack111ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪℋ"): bstack111ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫℌ")
}
bstack111111ll1l1_opy_ = [bstack111ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬℍ"), bstack111ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬℎ")]
bstack11l1l1l111_opy_ = (bstack111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢℏ"),)
bstack11111l11lll_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡷࡳࡨࡦࡺࡥࡠࡥ࡯࡭ࠬℐ")
bstack1111l11l11_opy_ = bstack111ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠲ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠱ࡹ࠵࠴࡭ࡲࡪࡦࡶ࠳ࠧℑ")
bstack1lll11111_opy_ = bstack111ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬ࡸࡩࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࠤℒ")
bstack1lll1l11_opy_ = bstack111ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠭ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠧℓ")
class EVENTS(Enum):
  bstack111111llll1_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩ℔")
  bstack1ll1llllll_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳࠫℕ")
  bstack1ll11l1ll_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡢ࡮࡬ࡾࡪ࠭№")
  bstack11111l1l111_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࡯ࡳ࡬ࡹࠧ℗")
  bstack11l11lll11_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬ℘") #shift post bstack11111l11111_opy_
  bstack1lll1l1ll_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮ࠫℙ") #shift post bstack11111l11111_opy_
  bstack11111l11l1l_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡮ࡵࡣࠩℚ") #shift
  bstack1111111l1l1_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪℛ") #shift
  bstack1111l111l_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨℜ")
  bstack1l1111lllll_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡶࡥࡻ࡫࠭ࡳࡧࡶࡹࡱࡺࡳࠨℝ")
  bstack1lll1ll1ll_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡴࡪࡸࡦࡰࡴࡰࡷࡨࡧ࡮ࠨ℞")
  bstack11l1lllll_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡮ࡲࡧࡦࡲࠧ℟") #shift
  bstack1llllll1l1_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡡࡱࡲ࠰ࡹࡵࡲ࡯ࡢࡦࠪ℠") #shift
  bstack111llll1l1_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡧ࡮࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠩ℡")
  bstack1llllll1ll_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭™") #shift
  bstack11l11ll1ll_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭℣") #shift
  bstack111111l1l11_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻࠪℤ") #shift
  bstack11l1llllll1_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ℥")
  bstack1l1lll1lll_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡶࡸࡦࡺࡵࡴࠩΩ") #shift
  bstack1111ll1l_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪ℧")
  bstack111111l1111_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡽࡿ࠭ࡴࡧࡷࡹࡵ࠭ℨ") #shift
  bstack11l1l1ll11_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡹࡻࡰࠨ℩")
  bstack11111l111ll_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡲࡦࡶࡳࡩࡱࡷࠫK") # not bstack111111l111l_opy_ in python
  bstack11lll1111_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡶࡻࡩࡵࠩÅ") # used in bstack111111lllll_opy_
  bstack111l1l1ll1l_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶࡲࡦ࠯ࡴࡹ࡮ࡺࠧℬ")
  bstack111l1l1l111_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱ࡶࡻࡩࡵࠩℭ")
  bstack111111111l_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡨࡧࡷࠫ℮") # used in bstack111111lllll_opy_
  bstack11l111111l_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡪࡲࡳࡰ࠭ℯ")
  bstack111l1llllll_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡨࡰࡱ࡮ࠫℰ")
  bstack111ll1111l1_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡪࡲࡳࡰ࠭ℱ")
  bstack1llllll11_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠬℲ")
  bstack111llllll1_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠬℳ") #
  bstack1lll1llll_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡹࡧ࡫ࡦࡕࡦࡶࡪ࡫࡮ࡔࡪࡲࡸࠬℴ")
  bstack11lll11l1l_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬℵ")
  bstack11l1lll11l_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡩ࠲ࡺࡥࡴࡶࠪℶ")
  bstack1lllll11ll_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡳࡸࡺ࠭ࡵࡧࡶࡸࠬℷ")
  bstack111lllll_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡷ࡫࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨℸ") #shift
  bstack1l11ll1ll1_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪℹ") #shift
  bstack111111l1lll_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫ℺")
  bstack11111l1111l_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡫ࡧࡰࡪ࠳ࡴࡪ࡯ࡨࡳࡺࡺࠧ℻")
  bstack111l1ll1l1_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡦࡺ࡬ࡸ࠲࡮ࡡ࡯ࡦ࡯ࡩࡷ࠭ℼ")
  bstack1l11ll1l111_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿࡫ࡸࡪࡶ࠰࡬ࡦࡴࡤ࡭ࡧࡵࠫℽ")
  bstack11111l11l11_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࠭࡮ࡧࡷࡶ࡮ࡩࡳࠨℾ")
  bstack11111l1ll11_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡩࡷࡥ࠾ࡸࡺ࡯ࡱࠩℿ")
  bstack1l1l111llll_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡵࡷࡥࡷࡺࠧ⅀")
  bstack11111l11ll1_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡧࡳࡼࡴ࡬ࡰࡣࡧࠫ⅁")
  bstack1111111llll_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡧ࡭࡫ࡣ࡬࠯ࡸࡴࡩࡧࡴࡦࠩ⅂")
  bstack1l11l111lll_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡣࡱࡲࡸࡸࡺࡲࡢࡲࠪ⅃")
  bstack1l11l1lll11_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡵࡷࡥࡷࡺࡢࡪࡰࡤࡶࡾ࠭⅄")
  bstack1l11l1l111l_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡦࡳࡳࡴࡥࡤࡶࠪⅅ")
  bstack1l11ll1l1l1_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡷࡹࡵࡰࠨⅆ")
  bstack1l11l1l1l11_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭ⅇ")
  bstack1l1l1l1l111_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩⅈ")
  bstack111111l11l1_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠪⅉ")
  bstack11111l111l1_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡨࡓ࡫ࡡࡳࡧࡶࡸࡍࡻࡢࠨ⅊")
  bstack11l1l111ll1_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡉ࡯࡫ࡷࠫ⅋")
  bstack11l11lllll1_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡶࡹ࠭⅌")
  bstack1l1111111l1_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡆࡳࡳ࡬ࡩࡨࠩ⅍")
  bstack111111lll11_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪⅎ")
  bstack11llll111ll_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡩࡔࡧ࡯ࡪࡍ࡫ࡡ࡭ࡕࡷࡩࡵ࠭⅏")
  bstack11llll1l11l_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡊࡩࡹࡘࡥࡴࡷ࡯ࡸࠬ⅐")
  bstack11ll1l11lll_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡅࡷࡧࡱࡸࠬ⅑")
  bstack11lll11ll11_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠫ⅒")
  bstack11ll1l11ll1_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡬ࡰࡩࡆࡶࡪࡧࡴࡦࡦࡈࡺࡪࡴࡴࠨ⅓")
  bstack11111l1l1ll_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡦࡰࡴࡹࡪࡻࡥࡕࡧࡶࡸࡊࡼࡥ࡯ࡶࠪ⅔")
  bstack11l11llllll_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡴࡶࠧ⅕")
  bstack1l11l11l1l1_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࡮ࡔࡶࡲࡴࠬ⅖")
  bstack111l1111l11_opy_ = bstack111ll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࡕࡱ࡮ࡲࡥࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪ⅗")
  bstack11l1l111_opy_ = bstack111ll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡱࡨࡋࡻ࡮࡯ࡧ࡯ࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪ⅘")
  bstack1l11llll11_opy_ = bstack111ll_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡌࡵ࡯ࡰࡨࡰ࡙࡫ࡳࡵࡅࡲࡱࡵࡲࡥࡵࡧࡧࠫ⅙")
  bstack1ll11ll1111_opy_ = bstack111ll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡴࡵࡲࡹࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡐࡺࡶࡨࡷࡹ࠭⅚")
  bstack1llll1ll111_opy_ = bstack111ll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡵࡶ࡬ࡺࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡃࡧ࡫ࡥࡻ࡫ࠧ⅛")
  bstack1ll111ll1l1_opy_ = bstack111ll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡴࡒࡼࡸࡪࡹࡴࠨ⅜")
  bstack1ll11l11l11_opy_ = bstack111ll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡹࡵࡧࡶࡸࡌ࡫ࡴࡕࡱࡷࡥࡱ࡚ࡥࡴࡶࡶࠫ⅝")
class STAGE(Enum):
  bstack11llll1l1_opy_ = bstack111ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ⅞")
  END = bstack111ll_opy_ (u"ࠪࡩࡳࡪࠧ⅟")
  bstack1l1l11l1l_opy_ = bstack111ll_opy_ (u"ࠫࡸ࡯࡮ࡨ࡮ࡨࠫⅠ")
bstack1ll11ll1l_opy_ = {
  bstack111ll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬⅡ"): bstack111ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭Ⅲ"),
  bstack111ll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫⅣ"): bstack111ll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪⅤ"),
  bstack111ll_opy_ (u"ࠩࡅࡉࡍࡇࡖࡆࠩⅥ"): bstack111ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪⅦ")
}
PLAYWRIGHT_HUB_URL = bstack111ll_opy_ (u"ࠦࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂࠨⅧ")
MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION = 98
MINIMUM_NON_BSTACK_INFRA_A11Y_SUPPORTED_CHROME_VERSION = 100
MINIMUM_CHROMEFORTESTING_SUPPORTED_VERSION = 141
ACCESSIBILITY_SUPPORTED_BROWSERS = {
    bstack111ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬⅨ"): {
        bstack111ll_opy_ (u"࠭ࡤࡪࡵࡳࡰࡦࡿ࡟࡯ࡣࡰࡩࠬⅩ"): bstack111ll_opy_ (u"ࠧࡄࡪࡵࡳࡲ࡫ࠧⅪ"),
        bstack111ll_opy_ (u"ࠨ࡯࡬ࡲࡤࡼࡥࡳࡵ࡬ࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬⅫ"): bstack111ll_opy_ (u"ࠩ࠼࠽ࠬⅬ"),
        bstack111ll_opy_ (u"ࠪࡱ࡮ࡴ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫⅭ"): bstack111ll_opy_ (u"ࠫ࠶࠶࠱ࠨⅮ"),
        bstack111ll_opy_ (u"ࠬࡳࡩ࡯ࡡࡹࡩࡷࡹࡩࡰࡰࡢࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧⅯ"): bstack111ll_opy_ (u"࠭࠱࠱࠳ࠪⅰ"),
        bstack111ll_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥࡴࡡࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡧ࡭࡫ࡣ࡬ࠩⅱ"): True
    },
    bstack111ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠪⅲ"): {
        bstack111ll_opy_ (u"ࠩࡧ࡭ࡸࡶ࡬ࡢࡻࡢࡲࡦࡳࡥࠨⅳ"): bstack111ll_opy_ (u"ࠪࡇ࡭ࡸ࡯࡮ࡧࠪⅴ"),
        bstack111ll_opy_ (u"ࠫࡲ࡯࡮ࡠࡸࡨࡶࡸ࡯࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨⅵ"): bstack111ll_opy_ (u"ࠬ࠿࠹ࠨⅶ"),
        bstack111ll_opy_ (u"࠭࡭ࡪࡰࡢࡺࡪࡸࡳࡪࡱࡱࡣࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧⅷ"): bstack111ll_opy_ (u"ࠧ࠲࠲࠴ࠫⅸ"),
        bstack111ll_opy_ (u"ࠨ࡯࡬ࡲࡤࡼࡥࡳࡵ࡬ࡳࡳࡥࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪⅹ"): bstack111ll_opy_ (u"ࠩ࠴࠴࠶࠭ⅺ"),
        bstack111ll_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡷࡤࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡣࡩࡧࡦ࡯ࠬⅻ"): True
    },
    bstack111ll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠮ࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠪⅼ"): {
        bstack111ll_opy_ (u"ࠬࡪࡩࡴࡲ࡯ࡥࡾࡥ࡮ࡢ࡯ࡨࠫⅽ"): bstack111ll_opy_ (u"࠭ࡃࡩࡴࡲࡱࡪ࠭ⅾ"),
        bstack111ll_opy_ (u"ࠧ࡮࡫ࡱࡣࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫⅿ"): bstack111ll_opy_ (u"ࠨ࠻࠼ࠫↀ"),
        bstack111ll_opy_ (u"ࠩࡰ࡭ࡳࡥࡶࡦࡴࡶ࡭ࡴࡴ࡟࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪↁ"): bstack111ll_opy_ (u"ࠪ࠵࠵࠷ࠧↂ"),
        bstack111ll_opy_ (u"ࠫࡲ࡯࡮ࡠࡸࡨࡶࡸ࡯࡯࡯ࡡࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭Ↄ"): bstack111ll_opy_ (u"ࠬ࠷࠰࠲ࠩↄ"),
        bstack111ll_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫ࡳࡠࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡦ࡬ࡪࡩ࡫ࠨↅ"): True
    },
    bstack111ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡦࡰࡴࡷࡩࡸࡺࡩ࡯ࡩࠪↆ"): {
        bstack111ll_opy_ (u"ࠨࡦ࡬ࡷࡵࡲࡡࡺࡡࡱࡥࡲ࡫ࠧↇ"): bstack111ll_opy_ (u"ࠩࡆ࡬ࡷࡵ࡭ࡦࡈࡲࡶ࡙࡫ࡳࡵ࡫ࡱ࡫ࠬↈ"),
        bstack111ll_opy_ (u"ࠪࡱ࡮ࡴ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ↉"): bstack111ll_opy_ (u"ࠫ࠶࠺࠱ࠨ↊"),
        bstack111ll_opy_ (u"ࠬࡳࡩ࡯ࡡࡹࡩࡷࡹࡩࡰࡰࡢࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭↋"): bstack111ll_opy_ (u"࠭࠱࠵࠳ࠪ↌"),
        bstack111ll_opy_ (u"ࠧ࡮࡫ࡱࡣࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ↍"): bstack111ll_opy_ (u"ࠨ࠳࠷࠵ࠬ↎"),
        bstack111ll_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡶࡣࡨ࡮ࡲࡰ࡯ࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤࡩࡨࡦࡥ࡮ࠫ↏"): True
    },
    bstack111ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ←"): {
        bstack111ll_opy_ (u"ࠫࡩ࡯ࡳࡱ࡮ࡤࡽࡤࡴࡡ࡮ࡧࠪ↑"): bstack111ll_opy_ (u"࡙ࠬࡡࡧࡣࡵ࡭ࠬ→"),
        bstack111ll_opy_ (u"࠭࡭ࡪࡰࡢࡺࡪࡸࡳࡪࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ↓"): bstack111ll_opy_ (u"ࠧ࠲࠺࠱࠸ࠬ↔"),
        bstack111ll_opy_ (u"ࠨ࡯࡬ࡲࡤࡼࡥࡳࡵ࡬ࡳࡳࡥ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ↕"): bstack111ll_opy_ (u"ࠩ࠴࠼࠳࠺ࠧ↖"),
        bstack111ll_opy_ (u"ࠪࡱ࡮ࡴ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ↗"): bstack111ll_opy_ (u"ࠫ࠶࠾࠮࠵ࠩ↘"),
        bstack111ll_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡹ࡟ࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡥ࡫ࡩࡨࡱࠧ↙"): False
    }
}
bstack1l1l111111_opy_ = (bstack111ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭↚"), bstack111ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩ↛"), bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩࡨࡳࡱࡰ࡭ࡺࡳࠧ↜"))
bstack1ll111ll11l_opy_ = {
  bstack111ll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࠨ↝"): bstack111ll_opy_ (u"ࠪ࠱࠲ࡸࡥࡳࡷࡱࡷࠬ↞"),
  bstack111ll_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪ↟"): bstack111ll_opy_ (u"ࠬ࠳࠭ࡳࡧࡵࡹࡳࡹ࠭ࡥࡧ࡯ࡥࡾ࠭↠"),
  bstack111ll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫ↡"): 0
}
bstack11111l1l1l1_opy_ = bstack111ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢ↢")
bstack1111111l1ll_opy_ = bstack111ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡸࡴࡱࡵࡡࡥ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧ↣")
bstack1ll1ll1l1l_opy_ = bstack111ll_opy_ (u"ࠤࡗࡉࡘ࡚ࠠࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠣࡅࡓࡊࠠࡂࡐࡄࡐ࡞࡚ࡉࡄࡕࠥ↤")