# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import re
from enum import Enum
bstack1l111ll11l_opy_ = {
  bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭₱"): bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩ₲"),
  bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ₳"): bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪ₴"),
  bstack1l1llll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ₵"): bstack1l1llll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭₶"),
  bstack1l1llll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ₷"): bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫ₸"),
  bstack1l1llll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ₹"): bstack1l1llll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧ₺"),
  bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ₻"): bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧ₼"),
  bstack1l1llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ₽"): bstack1l1llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ₾"),
  bstack1l1llll_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪ₿"): bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪ⃀"),
  bstack1l1llll_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫ⃁"): bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧ⃂"),
  bstack1l1llll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭⃃"): bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭⃄"),
  bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧ⃅"): bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧ⃆"),
  bstack1l1llll_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫ⃇"): bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫ⃈"),
  bstack1l1llll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭⃉"): bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭⃊"),
  bstack1l1llll_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩ⃋"): bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩ⃌"),
  bstack1l1llll_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩ⃍"): bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩ⃎"),
  bstack1l1llll_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨ⃏"): bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨ⃐"),
  bstack1l1llll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ⃑"): bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱ⃒ࠫ"),
  bstack1l1llll_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴ⃓ࠩ"): bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩ⃔"),
  bstack1l1llll_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪ⃕"): bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪ⃖"),
  bstack1l1llll_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧ⃗"): bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮⃘ࠧ"),
  bstack1l1llll_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶ⃙ࠫ"): bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶ⃚ࠫ"),
  bstack1l1llll_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭⃛"): bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭⃜"),
  bstack1l1llll_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬ⃝"): bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬ⃞"),
  bstack1l1llll_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩ⃟"): bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩ⃠"),
  bstack1l1llll_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ⃡"): bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ⃢"),
  bstack1l1llll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ⃣"): bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ⃤"),
  bstack1l1llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨ⃥ࠫ"): bstack1l1llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ⃦"),
  bstack1l1llll_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭⃧"): bstack1l1llll_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨ⃨"),
  bstack1l1llll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ⃩"): bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲ⃪ࠬ"),
  bstack1l1llll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ⃫࠭"): bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ⃬࠭"),
  bstack1l1llll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦ⃭ࠩ"): bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦ⃮ࠩ"),
  bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴ⃯ࠩ"): bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬ⃰"),
  bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ⃱"): bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ⃲"),
  bstack1l1llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ⃳"): bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧ⃴"),
  bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⃵"): bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⃶"),
  bstack1l1llll_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭⃷"): bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭⃸"),
  bstack1l1llll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩ⃹"): bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩ⃺"),
  bstack1l1llll_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬ⃻"): bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬ⃼"),
  bstack1l1llll_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨ⃽"): bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨ⃾"),
  bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ⃿"): bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ℀"),
  bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ℁"): bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩℂ")
}
bstack1llllll1lll1_opy_ = [
  bstack1l1llll_opy_ (u"ࠩࡲࡷࠬ℃"),
  bstack1l1llll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭℄"),
  bstack1l1llll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭℅"),
  bstack1l1llll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ℆"),
  bstack1l1llll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪℇ"),
  bstack1l1llll_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ℈"),
  bstack1l1llll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ℉"),
]
bstack1l1ll1lllll_opy_ = {
  bstack1l1llll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫℊ"): [bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫℋ"), bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡐࡄࡑࡊ࠭ℌ")],
  bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨℍ"): bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩℎ"),
  bstack1l1llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪℏ"): bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠫℐ"),
  bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧℑ"): bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠨℒ"),
  bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ℓ"): bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ℔"),
  bstack1l1llll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ℕ"): bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡔࡡࡓࡉࡗࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨ№"),
  bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ℗"): bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧ℘"),
  bstack1l1llll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧℙ"): bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨℚ"),
  bstack1l1llll_opy_ (u"ࠬࡧࡰࡱࠩℛ"): [bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࡡࡌࡈࠬℜ"), bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࠪℝ")],
  bstack1l1llll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ℞"): bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡒࡏࡈࡎࡈ࡚ࡊࡒࠧ℟"),
  bstack1l1llll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ℠"): bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ℡"),
  bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ™"): [bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠪ℣"), bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧℤ")],
  bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ℥"): bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡘࡖࡇࡕࡓࡄࡃࡏࡉࠬΩ"),
  bstack1l1llll_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡊࡔࡖࠨ℧"): bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡓࡗࡉࡈࡆࡕࡗࡖࡆ࡚ࡉࡐࡐࡢࡗࡒࡇࡒࡕࡡࡖࡉࡑࡋࡃࡕࡋࡒࡒࡤࡌࡅࡂࡖࡘࡖࡊࡥࡂࡓࡃࡑࡇࡍࡋࡓࠨℨ")
}
bstack1111lllll_opy_ = {
  bstack1l1llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ℩"): [bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡢࡲࡦࡳࡥࠨK"), bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡒࡦࡳࡥࠨÅ")],
  bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫℬ"): [bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡠ࡭ࡨࡽࠬℭ"), bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ℮")],
  bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧℯ"): bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧℰ"),
  bstack1l1llll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫℱ"): bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫℲ"),
  bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪℳ"): bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪℴ"),
  bstack1l1llll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪℵ"): [bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡵࡶࠧℶ"), bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫℷ")],
  bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪℸ"): bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬℹ"),
  bstack1l1llll_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ℺"): bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ℻"),
  bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࠧℼ"): bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࠧℽ"),
  bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧℾ"): bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡨࡎࡨࡺࡪࡲࠧℿ"),
  bstack1l1llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⅀"): bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⅁"),
  bstack1l1llll_opy_ (u"ࠤࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡇࡑࡏࠢ⅂"): bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࠣ⅃"),
}
bstack1111lll11_opy_ = {
  bstack1l1llll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ⅄"): bstack1l1llll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩⅅ"),
  bstack1l1llll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨⅆ"): [bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩⅇ"), bstack1l1llll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫⅈ")],
  bstack1l1llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧⅉ"): bstack1l1llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ⅊"),
  bstack1l1llll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ⅋"): bstack1l1llll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ⅌"),
  bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ⅍"): [bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨⅎ"), bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ⅏")],
  bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⅐"): bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⅑"),
  bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨ⅒"): bstack1l1llll_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪ⅓"),
  bstack1l1llll_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⅔"): [bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⅕"), bstack1l1llll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⅖")],
  bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨ⅗"): [bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫ⅘"), bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫ⅙")]
}
bstack11lll1ll11_opy_ = [
  bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫ⅚"),
  bstack1l1llll_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩ⅛"),
  bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭⅜"),
  bstack1l1llll_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨ⅝"),
  bstack1l1llll_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫ⅞"),
  bstack1l1llll_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⅟"),
  bstack1l1llll_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧⅠ"),
  bstack1l1llll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪⅡ"),
  bstack1l1llll_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫⅢ"),
  bstack1l1llll_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨⅣ"),
  bstack1l1llll_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧⅤ"),
  bstack1l1llll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪⅥ"),
]
bstack1ll1ll1l11l_opy_ = [
  bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧⅦ"),
  bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨⅧ"),
  bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫⅨ"),
  bstack1l1llll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭Ⅹ"),
  bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅪ"),
  bstack1l1llll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪⅫ"),
  bstack1l1llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬⅬ"),
  bstack1l1llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧⅭ"),
  bstack1l1llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧⅮ"),
  bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪⅯ"),
  bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡑࡦࡴࡡࡨࡧࡰࡩࡳࡺࡏࡱࡶ࡬ࡳࡳࡹࠧⅰ"),
  bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫⅱ"),
  bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨⅲ"),
  bstack1l1llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫⅳ"),
  bstack1l1llll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡗࡥ࡬࠭ⅴ"),
  bstack1l1llll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨⅵ"),
  bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧⅶ"),
  bstack1l1llll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪⅷ"),
  bstack1l1llll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠶࠭ⅸ"),
  bstack1l1llll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠸ࠧⅹ"),
  bstack1l1llll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠳ࠨⅺ"),
  bstack1l1llll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠵ࠩⅻ"),
  bstack1l1llll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠷ࠪⅼ"),
  bstack1l1llll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠹ࠫⅽ"),
  bstack1l1llll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠻ࠬⅾ"),
  bstack1l1llll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠽࠭ⅿ"),
  bstack1l1llll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠿ࠧↀ"),
  bstack1l1llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨↁ"),
  bstack1l1llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩↂ"),
  bstack1l1llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧↃ"),
  bstack1l1llll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧↄ"),
  bstack1l1llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪↅ"),
  bstack1l1llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫↆ"),
  bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬↇ"),
  bstack1l1llll_opy_ (u"ࠩ࡫ࡹࡧࡘࡥࡨ࡫ࡲࡲࠬↈ"),
  bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡅࡤࡇࡪࡸࡴࡪࡨ࡬ࡧࡦࡺࡥࠨ↉")
]
bstack1lllllll1lll_opy_ = [
  bstack1l1llll_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩ↊"),
  bstack1l1llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ↋"),
  bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ↌"),
  bstack1l1llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ↍"),
  bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡖࡲࡪࡱࡵ࡭ࡹࡿࠧ↎"),
  bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ↏"),
  bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡤ࡫ࠬ←"),
  bstack1l1llll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ↑"),
  bstack1l1llll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ→"),
  bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ↓"),
  bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ↔"),
  bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ↕"),
  bstack1l1llll_opy_ (u"ࠩࡲࡷࠬ↖"),
  bstack1l1llll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭↗"),
  bstack1l1llll_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪ↘"),
  bstack1l1llll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧ↙"),
  bstack1l1llll_opy_ (u"࠭ࡲࡦࡩ࡬ࡳࡳ࠭↚"),
  bstack1l1llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩ↛"),
  bstack1l1llll_opy_ (u"ࠨ࡯ࡤࡧ࡭࡯࡮ࡦࠩ↜"),
  bstack1l1llll_opy_ (u"ࠩࡵࡩࡸࡵ࡬ࡶࡶ࡬ࡳࡳ࠭↝"),
  bstack1l1llll_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ↞"),
  bstack1l1llll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨ↟"),
  bstack1l1llll_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫ↠"),
  bstack1l1llll_opy_ (u"࠭࡮ࡰࡒࡤ࡫ࡪࡒ࡯ࡢࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪ↡"),
  bstack1l1llll_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨ↢"),
  bstack1l1llll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧ↣"),
  bstack1l1llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭↤"),
  bstack1l1llll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡩࡳࡪࡋࡦࡻࡶࠫ↥"),
  bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨ↦"),
  bstack1l1llll_opy_ (u"ࠬࡴ࡯ࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠩ↧"),
  bstack1l1llll_opy_ (u"࠭ࡣࡩࡧࡦ࡯࡚ࡘࡌࠨ↨"),
  bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ↩"),
  bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡄࡱࡲ࡯࡮࡫ࡳࠨ↪"),
  bstack1l1llll_opy_ (u"ࠩࡦࡥࡵࡺࡵࡳࡧࡆࡶࡦࡹࡨࠨ↫"),
  bstack1l1llll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ↬"),
  bstack1l1llll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ↭"),
  bstack1l1llll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡘࡨࡶࡸ࡯࡯࡯ࠩ↮"),
  bstack1l1llll_opy_ (u"࠭࡮ࡰࡄ࡯ࡥࡳࡱࡐࡰ࡮࡯࡭ࡳ࡭ࠧ↯"),
  bstack1l1llll_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭↰"),
  bstack1l1llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡍࡱࡪࡷࠬ↱"),
  bstack1l1llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡋࡧࠫ↲"),
  bstack1l1llll_opy_ (u"ࠪࡨࡪࡪࡩࡤࡣࡷࡩࡩࡊࡥࡷ࡫ࡦࡩࠬ↳"),
  bstack1l1llll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡔࡦࡸࡡ࡮ࡵࠪ↴"),
  bstack1l1llll_opy_ (u"ࠬࡶࡨࡰࡰࡨࡒࡺࡳࡢࡦࡴࠪ↵"),
  bstack1l1llll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫ↶"),
  bstack1l1llll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡔࡶࡴࡪࡱࡱࡷࠬ↷"),
  bstack1l1llll_opy_ (u"ࠨࡥࡲࡲࡸࡵ࡬ࡦࡎࡲ࡫ࡸ࠭↸"),
  bstack1l1llll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ↹"),
  bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧ↺"),
  bstack1l1llll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡆ࡮ࡵ࡭ࡦࡶࡵ࡭ࡨ࠭↻"),
  bstack1l1llll_opy_ (u"ࠬࡼࡩࡥࡧࡲ࡚࠷࠭↼"),
  bstack1l1llll_opy_ (u"࠭࡭ࡪࡦࡖࡩࡸࡹࡩࡰࡰࡌࡲࡸࡺࡡ࡭࡮ࡄࡴࡵࡹࠧ↽"),
  bstack1l1llll_opy_ (u"ࠧࡦࡵࡳࡶࡪࡹࡳࡰࡕࡨࡶࡻ࡫ࡲࠨ↾"),
  bstack1l1llll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ↿"),
  bstack1l1llll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡇࡩࡶࠧ⇀"),
  bstack1l1llll_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪ⇁"),
  bstack1l1llll_opy_ (u"ࠫࡸࡿ࡮ࡤࡖ࡬ࡱࡪ࡝ࡩࡵࡪࡑࡘࡕ࠭⇂"),
  bstack1l1llll_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪ⇃"),
  bstack1l1llll_opy_ (u"࠭ࡧࡱࡵࡏࡳࡨࡧࡴࡪࡱࡱࠫ⇄"),
  bstack1l1llll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨ⇅"),
  bstack1l1llll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨ⇆"),
  bstack1l1llll_opy_ (u"ࠩࡩࡳࡷࡩࡥࡄࡪࡤࡲ࡬࡫ࡊࡢࡴࠪ⇇"),
  bstack1l1llll_opy_ (u"ࠪࡼࡲࡹࡊࡢࡴࠪ⇈"),
  bstack1l1llll_opy_ (u"ࠫࡽࡳࡸࡋࡣࡵࠫ⇉"),
  bstack1l1llll_opy_ (u"ࠬࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫ⇊"),
  bstack1l1llll_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭⇋"),
  bstack1l1llll_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ⇌"),
  bstack1l1llll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫ⇍"),
  bstack1l1llll_opy_ (u"ࠩࡤࡴࡵ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⇎"),
  bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩ⇏"),
  bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡳࡪࡩࡱࡅࡵࡶࠧ⇐"),
  bstack1l1llll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࡴࠩ⇑"),
  bstack1l1llll_opy_ (u"࠭ࡣࡢࡰࡤࡶࡾ࠭⇒"),
  bstack1l1llll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨ⇓"),
  bstack1l1llll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ⇔"),
  bstack1l1llll_opy_ (u"ࠩ࡬ࡩࠬ⇕"),
  bstack1l1llll_opy_ (u"ࠪࡩࡩ࡭ࡥࠨ⇖"),
  bstack1l1llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫ⇗"),
  bstack1l1llll_opy_ (u"ࠬࡷࡵࡦࡷࡨࠫ⇘"),
  bstack1l1llll_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ⇙"),
  bstack1l1llll_opy_ (u"ࠧࡢࡲࡳࡗࡹࡵࡲࡦࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⇚"),
  bstack1l1llll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡄࡣࡰࡩࡷࡧࡉ࡮ࡣࡪࡩࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧ⇛"),
  bstack1l1llll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡅࡹࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬ⇜"),
  bstack1l1llll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡊࡰࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭⇝"),
  bstack1l1llll_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨ⇞"),
  bstack1l1llll_opy_ (u"ࠬࡸࡥࡴࡧࡵࡺࡪࡊࡥࡷ࡫ࡦࡩࠬ⇟"),
  bstack1l1llll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭⇠"),
  bstack1l1llll_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ⇡"),
  bstack1l1llll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡣࡶࡷࡨࡵࡤࡦࠩ⇢"),
  bstack1l1llll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡋࡲࡷࡉ࡫ࡶࡪࡥࡨࡗࡪࡺࡴࡪࡰࡪࡷࠬ⇣"),
  bstack1l1llll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡹࡩ࡯࡯ࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪ⇤"),
  bstack1l1llll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡵࡶ࡬ࡦࡒࡤࡽࠬ⇥"),
  bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭⇦"),
  bstack1l1llll_opy_ (u"࠭ࡷࡥ࡫ࡲࡗࡪࡸࡶࡪࡥࡨࠫ⇧"),
  bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⇨"),
  bstack1l1llll_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵࡅࡵࡳࡸࡹࡓࡪࡶࡨࡘࡷࡧࡣ࡬࡫ࡱ࡫ࠬ⇩"),
  bstack1l1llll_opy_ (u"ࠩ࡫࡭࡬࡮ࡃࡰࡰࡷࡶࡦࡹࡴࠨ⇪"),
  bstack1l1llll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡓࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࡹࠧ⇫"),
  bstack1l1llll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧ⇬"),
  bstack1l1llll_opy_ (u"ࠬࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⇭"),
  bstack1l1llll_opy_ (u"࠭ࡲࡦ࡯ࡲࡺࡪࡏࡏࡔࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࡒ࡯ࡤࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫ⇮"),
  bstack1l1llll_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩ⇯"),
  bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⇰"),
  bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫ⇱"),
  bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ⇲"),
  bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⇳"),
  bstack1l1llll_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨ⇴"),
  bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ⇵"),
  bstack1l1llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡴࡻࡴࡴࠩ⇶"),
  bstack1l1llll_opy_ (u"ࠨࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡔࡷࡵ࡭ࡱࡶࡅࡩ࡭ࡧࡶࡪࡱࡵࠫ⇷")
]
bstack1llll1l1ll_opy_ = {
  bstack1l1llll_opy_ (u"ࠩࡹࠫ⇸"): bstack1l1llll_opy_ (u"ࠪࡺࠬ⇹"),
  bstack1l1llll_opy_ (u"ࠫ࡫࠭⇺"): bstack1l1llll_opy_ (u"ࠬ࡬ࠧ⇻"),
  bstack1l1llll_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬ⇼"): bstack1l1llll_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭⇽"),
  bstack1l1llll_opy_ (u"ࠨࡱࡱࡰࡾࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⇾"): bstack1l1llll_opy_ (u"ࠩࡲࡲࡱࡿࡁࡶࡶࡲࡱࡦࡺࡥࠨ⇿"),
  bstack1l1llll_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧ∀"): bstack1l1llll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨ∁"),
  bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨ∂"): bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩ∃"),
  bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪ∄"): bstack1l1llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫ∅"),
  bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬ∆"): bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭∇"),
  bstack1l1llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧ∈"): bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨ∉"),
  bstack1l1llll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧ∊"): bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡌࡴࡹࡴࠨ∋"),
  bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩ∌"): bstack1l1llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖ࡯ࡳࡶࠪ∍"),
  bstack1l1llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫ∎"): bstack1l1llll_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭∏"),
  bstack1l1llll_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧ∐"): bstack1l1llll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ∑"),
  bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨ−"): bstack1l1llll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪ∓"),
  bstack1l1llll_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫ∔"): bstack1l1llll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬ∕"),
  bstack1l1llll_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨ∖"): bstack1l1llll_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩ∗"),
  bstack1l1llll_opy_ (u"࠭ࡰࡢࡥࡩ࡭ࡱ࡫ࠧ∘"): bstack1l1llll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ∙"),
  bstack1l1llll_opy_ (u"ࠨࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ√"): bstack1l1llll_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ∛"),
  bstack1l1llll_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭∜"): bstack1l1llll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧ∝"),
  bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭∞"): bstack1l1llll_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧ∟"),
  bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ∠"): bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ∡"),
  bstack1l1llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫ∢"): bstack1l1llll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࠫ∣")
}
bstack1llllll1l11l_opy_ = bstack1l1llll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡩࡵࡪࡸࡦ࠳ࡩ࡯࡮࠱ࡳࡩࡷࡩࡹ࠰ࡥ࡯࡭࠴ࡸࡥ࡭ࡧࡤࡷࡪࡹ࠯࡭ࡣࡷࡩࡸࡺ࠯ࡥࡱࡺࡲࡱࡵࡡࡥࠤ∤")
bstack1llllll1llll_opy_ = bstack1l1llll_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠴࡮ࡥࡢ࡮ࡷ࡬ࡨ࡮ࡥࡤ࡭ࠥ∥")
bstack1l1ll1l1ll_opy_ = bstack1l1llll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡦࡦࡶ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡴࡧࡱࡨࡤࡹࡤ࡬ࡡࡨࡺࡪࡴࡴࡴࠤ∦")
bstack1ll1111ll_opy_ = bstack1l1llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡹࡧ࠳࡭ࡻࡢࠨ∧")
bstack1lll1111ll1_opy_ = bstack1l1llll_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠫ∨")
bstack1111l11ll_opy_ = bstack1l1llll_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠺࠴࠵࠶࠲ࡻࡩ࠵ࡨࡶࡤࠪ∩")
bstack1ll1111ll11_opy_ = bstack1l1llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡳ࡫ࡸࡵࡡ࡫ࡹࡧࡹࠧ∪")
bstack1l1l111111_opy_ = {
  bstack1l1llll_opy_ (u"ࠫࡩ࡫ࡦࡢࡷ࡯ࡸࠬ∫"): bstack1l1llll_opy_ (u"ࠬ࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ∬"),
  bstack1l1llll_opy_ (u"࠭ࡵࡴ࠯ࡨࡥࡸࡺࠧ∭"): bstack1l1llll_opy_ (u"ࠧࡩࡷࡥ࠱ࡺࡹࡥ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ∮"),
  bstack1l1llll_opy_ (u"ࠨࡷࡶࠫ∯"): bstack1l1llll_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡵࡴ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ∰"),
  bstack1l1llll_opy_ (u"ࠪࡩࡺ࠭∱"): bstack1l1llll_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡧࡸ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ∲"),
  bstack1l1llll_opy_ (u"ࠬ࡯࡮ࠨ∳"): bstack1l1llll_opy_ (u"࠭ࡨࡶࡤ࠰ࡥࡵࡹ࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ∴"),
  bstack1l1llll_opy_ (u"ࠧࡢࡷࠪ∵"): bstack1l1llll_opy_ (u"ࠨࡪࡸࡦ࠲ࡧࡰࡴࡧ࠰ࡳࡳࡲࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ∶")
}
bstack1llllllllll1_opy_ = {
  bstack1l1llll_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫ∷"): 50,
  bstack1l1llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ∸"): 40,
  bstack1l1llll_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬ∹"): 30,
  bstack1l1llll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ∺"): 20,
  bstack1l1llll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬ∻"): 10
}
bstack111l11l111_opy_ = bstack1llllllllll1_opy_[bstack1l1llll_opy_ (u"ࠧࡪࡰࡩࡳࠬ∼")]
bstack1l11l11lll_opy_ = bstack1l1llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤ࠱ࠪ∽")
bstack1ll1ll1ll1l_opy_ = bstack1l1llll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧ∾")
bstack1ll111ll1ll_opy_ = bstack1l1llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩ∿")
bstack1l111lll1l_opy_ = bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪ≀")
bstack11llllll1_opy_ = bstack1l1llll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪ≁")
bstack1l1ll1111l1_opy_ = {
  bstack1l1llll_opy_ (u"࠭ࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࠫ≂"): bstack1l1llll_opy_ (u"ࠧࠫࠬ࠭ࠤࡠ࡙ࡄࡌ࠯ࡊࡉࡓ࠳࠰࠱࠷ࡠࠤࡥࡶࡹࡵࡧࡶࡸ࠲ࡶࡡࡳࡣ࡯ࡰࡪࡲࡠࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡪࡰࠣࡽࡴࡻࡲࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹ࠴ࠠࡕࡪ࡬ࡷࠥࡳࡡࡺࠢࡦࡥࡺࡹࡥࠡࡥࡲࡲ࡫ࡲࡩࡤࡶࡶࠤࡼ࡯ࡴࡩࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡵ࡯࡫ࡱࡷࡹࡧ࡬࡭ࠢ࡬ࡸࠥࡻࡳࡪࡰࡪ࠾ࠥࡶࡩࡱࠢࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡶࡡࡳࡣ࡯ࡰࡪࡲࠠࠫࠬ࠭ࠫ≃")
}
bstack1llllllll11l_opy_ = [bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ≄"), bstack1l1llll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ≅")]
bstack11111111l11_opy_ = [bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭≆"), bstack1l1llll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭≇")]
bstack1lll1l11111_opy_ = bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ≈")
bstack1l11111l11_opy_ = re.compile(bstack1l1llll_opy_ (u"࠭࡞࡜࡞࡟ࡻ࠲ࡣࠫ࠻࠰࠭ࠨࠬ≉"))
bstack1lll11lll11_opy_ = [
  bstack1l1llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨ≊"),
  bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ≋"),
  bstack1l1llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭≌"),
  bstack1l1llll_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧ≍"),
  bstack1l1llll_opy_ (u"ࠫࡦࡶࡰࠨ≎"),
  bstack1l1llll_opy_ (u"ࠬࡻࡤࡪࡦࠪ≏"),
  bstack1l1llll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ≐"),
  bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧ≑"),
  bstack1l1llll_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭≒"),
  bstack1l1llll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧ≓"),
  bstack1l1llll_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫ≔"), bstack1l1llll_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧ≕"),
  bstack1l1llll_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨ≖"),
  bstack1l1llll_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬ≗"),
  bstack1l1llll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫ≘"),
  bstack1l1llll_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫ≙"),
  bstack1l1llll_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪ≚"),
  bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨ≛"), bstack1l1llll_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨ≜"), bstack1l1llll_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧ≝"), bstack1l1llll_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧ≞"), bstack1l1llll_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ≟"),
  bstack1l1llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭≠"),
  bstack1l1llll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭≡"),
  bstack1l1llll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬ≢"), bstack1l1llll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨ≣"),
  bstack1l1llll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ≤"),
  bstack1l1llll_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧ≥"),
  bstack1l1llll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ࠭≦"),
  bstack1l1llll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩ≧"),
  bstack1l1llll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧ≨"),
  bstack1l1llll_opy_ (u"ࠪࡥࡻࡪࠧ≩"), bstack1l1llll_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ≪"), bstack1l1llll_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧ≫"), bstack1l1llll_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧ≬"),
  bstack1l1llll_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬ≭"), bstack1l1llll_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧ≮"), bstack1l1llll_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬ≯"),
  bstack1l1llll_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬ≰"), bstack1l1llll_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩ≱"),
  bstack1l1llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧ≲"), bstack1l1llll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩ≳"), bstack1l1llll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬ≴"), bstack1l1llll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪ≵"), bstack1l1llll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭≶"),
  bstack1l1llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭≷"), bstack1l1llll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨ≸"),
  bstack1l1llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧ≹"),
  bstack1l1llll_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫ≺"),
  bstack1l1llll_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭≻"), bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩ≼"), bstack1l1llll_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧ≽"), bstack1l1llll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭≾"),
  bstack1l1llll_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩ≿"),
  bstack1l1llll_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ⊀"), bstack1l1llll_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭⊁"),
  bstack1l1llll_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧ⊂"),
  bstack1l1llll_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪ⊃"),
  bstack1l1llll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫ⊄"),
  bstack1l1llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⊅"),
  bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬ⊆"),
  bstack1l1llll_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ⊇"),
  bstack1l1llll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮ࠧ⊈"),
  bstack1l1llll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭⊉"),
  bstack1l1llll_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬ⊊"),
  bstack1l1llll_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭⊋"),
  bstack1l1llll_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫ⊌"),
  bstack1l1llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪ⊍"),
  bstack1l1llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ⊎"),
  bstack1l1llll_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭⊏"),
  bstack1l1llll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬ⊐"),
  bstack1l1llll_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬ⊑"),
  bstack1l1llll_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩ⊒"),
  bstack1l1llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧ⊓"), bstack1l1llll_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨ⊔"), bstack1l1llll_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨ⊕"),
  bstack1l1llll_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪ⊖"),
  bstack1l1llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫ⊗"),
  bstack1l1llll_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪ⊘"),
  bstack1l1llll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫ⊙"),
  bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ⊚"),
  bstack1l1llll_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨ⊛"),
  bstack1l1llll_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨ⊜"), bstack1l1llll_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸࠬ⊝"), bstack1l1llll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠪ⊞"),
  bstack1l1llll_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨ⊟"),
  bstack1l1llll_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶࠪ⊠"),
  bstack1l1llll_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨࠬ⊡"),
  bstack1l1llll_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫ⊢"),
  bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨ⊣"), bstack1l1llll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨࠬ⊤"),
  bstack1l1llll_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪ⊥"), bstack1l1llll_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷࠬ⊦"),
  bstack1l1llll_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣࠩ⊧"),
  bstack1l1llll_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩ⊨"),
  bstack1l1llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧ⊩"), bstack1l1llll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴࠩ⊪"), bstack1l1llll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩࠪ⊫"), bstack1l1llll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧ⊬"),
  bstack1l1llll_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨ⊭"),
  bstack1l1llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪ⊮"),
  bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⊯"),
  bstack1l1llll_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫ⊰"),
  bstack1l1llll_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨࠩ⊱"),
  bstack1l1llll_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨ⊲"),
  bstack1l1llll_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ⊳"), bstack1l1llll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩ⊴"),
  bstack1l1llll_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬ⊵"),
  bstack1l1llll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪ⊶"),
  bstack1l1llll_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬ⊷"),
  bstack1l1llll_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬ⊸"),
  bstack1l1llll_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨ⊹"),
  bstack1l1llll_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪ⊺"),
  bstack1l1llll_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩ⊻"),
  bstack1l1llll_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧࠪ⊼"),
  bstack1l1llll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪ⊽"),
  bstack1l1llll_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ⊾"),
  bstack1l1llll_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪ⊿"),
  bstack1l1llll_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬ⋀"),
  bstack1l1llll_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭⋁"),
  bstack1l1llll_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪ⋂"),
  bstack1l1llll_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫ⋃"),
  bstack1l1llll_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ࠭⋄"),
  bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬ⋅"),
  bstack1l1llll_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭⋆"),
  bstack1l1llll_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮ࠪ⋇"),
  bstack1l1llll_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭⋈"),
  bstack1l1llll_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫ⋉"),
  bstack1l1llll_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ⋊"), bstack1l1llll_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪ⋋"),
  bstack1l1llll_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨ⋌"), bstack1l1llll_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭⋍"),
  bstack1l1llll_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫ⋎"),
  bstack1l1llll_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪ⋏"),
  bstack1l1llll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪ⋐"),
  bstack1l1llll_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭⋑"), bstack1l1llll_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭⋒"),
  bstack1l1llll_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ⋓"),
  bstack1l1llll_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪ⋔"),
  bstack1l1llll_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭⋕"),
  bstack1l1llll_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨ⋖"),
  bstack1l1llll_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪ⋗"),
  bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬ⋘"),
  bstack1l1llll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨ⋙"),
  bstack1l1llll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪ⋚"),
  bstack1l1llll_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧ⋛"),
  bstack1l1llll_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬ⋜"), bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫ⋝"),
  bstack1l1llll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨ⋞"),
  bstack1l1llll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡌࡨࡑࡵࡣࡢࡶࡲࡶࡆࡻࡴࡰࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠬ⋟")
]
bstack1ll111l11l1_opy_ = bstack1l1llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡸࡴࡱࡵࡡࡥࠩ⋠")
bstack1ll11lll111_opy_ = [bstack1l1llll_opy_ (u"ࠫ࠳ࡧࡰ࡬ࠩ⋡"), bstack1l1llll_opy_ (u"ࠬ࠴ࡡࡢࡤࠪ⋢"), bstack1l1llll_opy_ (u"࠭࠮ࡪࡲࡤࠫ⋣")]
bstack1l1l1l1ll11_opy_ = [bstack1l1llll_opy_ (u"ࠧࡪࡦࠪ⋤"), bstack1l1llll_opy_ (u"ࠨࡲࡤࡸ࡭࠭⋥"), bstack1l1llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ⋦"), bstack1l1llll_opy_ (u"ࠪࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥࠩ⋧")]
bstack1ll1l11l11_opy_ = {
  bstack1l1llll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ⋨"): bstack1l1llll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⋩"),
  bstack1l1llll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ⋪"): bstack1l1llll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ⋫"),
  bstack1l1llll_opy_ (u"ࠨࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭⋬"): bstack1l1llll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⋭"),
  bstack1l1llll_opy_ (u"ࠪ࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭⋮"): bstack1l1llll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⋯"),
  bstack1l1llll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡴࡪࡱࡱࡷࠬ⋰"): bstack1l1llll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ⋱")
}
bstack1ll1l11lll1_opy_ = [
  bstack1l1llll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ⋲"),
  bstack1l1llll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭⋳"),
  bstack1l1llll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⋴"),
  bstack1l1llll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⋵"),
  bstack1l1llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ⋶"),
]
bstack1l1l11lll1_opy_ = bstack1ll1ll1l11l_opy_ + bstack1lllllll1lll_opy_ + bstack1lll11lll11_opy_
bstack1l1l111lll1_opy_ = [
  bstack1l1llll_opy_ (u"ࠬࡤ࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵࠦࠪ⋷"),
  bstack1l1llll_opy_ (u"࠭࡞ࡣࡵ࠰ࡰࡴࡩࡡ࡭࠰ࡦࡳࡲࠪࠧ⋸"),
  bstack1l1llll_opy_ (u"ࠧ࡟࠳࠵࠻࠳࠭⋹"),
  bstack1l1llll_opy_ (u"ࠨࡠ࠴࠴࠳࠭⋺"),
  bstack1l1llll_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠲࡝࠹࠱࠾ࡣ࠮ࠨ⋻"),
  bstack1l1llll_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠴࡞࠴࠲࠿࡝࠯ࠩ⋼"),
  bstack1l1llll_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠶࡟࠵࠳࠱࡞࠰ࠪ⋽"),
  bstack1l1llll_opy_ (u"ࠬࡤ࠱࠺࠴࠱࠵࠻࠾࠮ࠨ⋾")
]
bstack11111l11ll1_opy_ = bstack1l1llll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ⋿")
bstack1111l11lll_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡦࡸࡨࡲࡹ࠭⌀")
bstack1l1l11111l1_opy_ = [ bstack1l1llll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⌁") ]
bstack11ll11llll_opy_ = [ bstack1l1llll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⌂") ]
bstack1llllllll1l_opy_ = [bstack1l1llll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⌃")]
bstack1l1l11l11ll_opy_ = [ bstack1l1llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⌄") ]
bstack11111l111l_opy_ = bstack1l1llll_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ⌅")
bstack11ll1llll1_opy_ = bstack1l1llll_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩ⌆")
bstack1lll11111ll_opy_ = bstack1l1llll_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫ⌇")
bstack1l1l1ll1l11_opy_ = bstack1l1llll_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ⌈")
bstack1111ll111l_opy_ = [
  bstack1l1llll_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭⌉"),
  bstack1l1llll_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪ⌊"),
  bstack1l1llll_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬ⌋"),
  bstack1l1llll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫ⌌"),
  bstack1l1llll_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪ⌍"),
  bstack1l1llll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨ⌎"),
  bstack1l1llll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨ⌏"),
  bstack1l1llll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫ⌐"),
  bstack1l1llll_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬ⌑"),
  bstack1l1llll_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ⌒"),
  bstack1l1llll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭⌓"),
  bstack1l1llll_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬ⌔"),
  bstack1l1llll_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪ⌕"),
  bstack1l1llll_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ⌖"),
  bstack1l1llll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭⌗"),
  bstack1l1llll_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ⌘"),
  bstack1l1llll_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧ⌙"),
  bstack1l1llll_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ⌚"),
  bstack1l1llll_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧ⌛"),
  bstack1l1llll_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭⌜"),
  bstack1l1llll_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ⌝"),
]
bstack1l111111l1_opy_ = bstack1l1llll_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧ⌞")
bstack11l11lllll_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠪࢂࠬ⌟")), bstack1l1llll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⌠"), bstack1l1llll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ⌡"))
bstack1111l1l1ll1_opy_ = bstack1l1llll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵ࡯ࠧ⌢")
bstack1111111l1l1_opy_ = [ bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⌣"), bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ⌤"), bstack1l1llll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ⌥"), bstack1l1llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ⌦")]
bstack1llllll1ll_opy_ = [ bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⌧"), bstack1l1llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ⌨"), bstack1l1llll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ〈"), bstack1l1llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ〉"), bstack1l1llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ⌫") ]
bstack1lll11ll1l1_opy_ = [ bstack1l1llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ⌬"), bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ⌭") ]
bstack1lllllllll1l_opy_ = [ bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⌮"), bstack1l1llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ⌯") ]
bstack1ll1llll1l1_opy_ = 360
bstack11111l111l1_opy_ = bstack1l1llll_opy_ (u"ࠨࡡࡱࡲ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨ⌰")
bstack1111111ll11_opy_ = bstack1l1llll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡬ࡷࡸࡻࡥࡴࠤ⌱")
bstack1111111lll1_opy_ = bstack1l1llll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠦ⌲")
bstack1111l1l11l1_opy_ = bstack1l1llll_opy_ (u"ࠤࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡸࡪࡹࡴࡴࠢࡤࡶࡪࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡲࡲࠥࡕࡓࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࠨࡷࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥࠡࡨࡲࡶࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦࡤࡦࡸ࡬ࡧࡪࡹ࠮ࠣ⌳")
bstack1111l11lll1_opy_ = bstack1l1llll_opy_ (u"ࠥ࠵࠶࠴࠰ࠣ⌴")
bstack111l111l_opy_ = {
  bstack1l1llll_opy_ (u"ࠫࡕࡇࡓࡔࠩ⌵"): bstack1l1llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⌶"),
  bstack1l1llll_opy_ (u"࠭ࡆࡂࡋࡏࠫ⌷"): bstack1l1llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⌸"),
  bstack1l1llll_opy_ (u"ࠨࡕࡎࡍࡕ࠭⌹"): bstack1l1llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⌺")
}
bstack1ll1l1l111_opy_ = [
  bstack1l1llll_opy_ (u"ࠥ࡫ࡪࡺࠢ⌻"),
  bstack1l1llll_opy_ (u"ࠦ࡬ࡵࡂࡢࡥ࡮ࠦ⌼"),
  bstack1l1llll_opy_ (u"ࠧ࡭࡯ࡇࡱࡵࡻࡦࡸࡤࠣ⌽"),
  bstack1l1llll_opy_ (u"ࠨࡲࡦࡨࡵࡩࡸ࡮ࠢ⌾"),
  bstack1l1llll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨ⌿"),
  bstack1l1llll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ⍀"),
  bstack1l1llll_opy_ (u"ࠤࡶࡹࡧࡳࡩࡵࡇ࡯ࡩࡲ࡫࡮ࡵࠤ⍁"),
  bstack1l1llll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢ⍂"),
  bstack1l1llll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢ⍃"),
  bstack1l1llll_opy_ (u"ࠧࡩ࡬ࡦࡣࡵࡉࡱ࡫࡭ࡦࡰࡷࠦ⍄"),
  bstack1l1llll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࡹࠢ⍅"),
  bstack1l1llll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡔࡥࡵ࡭ࡵࡺࠢ⍆"),
  bstack1l1llll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡃࡶࡽࡳࡩࡓࡤࡴ࡬ࡴࡹࠨ⍇"),
  bstack1l1llll_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣ⍈"),
  bstack1l1llll_opy_ (u"ࠥࡵࡺ࡯ࡴࠣ⍉"),
  bstack1l1llll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱ࡙ࡵࡵࡤࡪࡄࡧࡹ࡯࡯࡯ࠤ⍊"),
  bstack1l1llll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡓࡵ࡭ࡶ࡬ࡘࡴࡻࡣࡩࠤ⍋"),
  bstack1l1llll_opy_ (u"ࠨࡳࡩࡣ࡮ࡩࠧ⍌"),
  bstack1l1llll_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࡇࡰࡱࠤ⍍")
]
bstack1111111111l_opy_ = [
  bstack1l1llll_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࠢ⍎"),
  bstack1l1llll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ⍏"),
  bstack1l1llll_opy_ (u"ࠥࡥࡺࡺ࡯ࠣ⍐"),
  bstack1l1llll_opy_ (u"ࠦࡲࡧ࡮ࡶࡣ࡯ࠦ⍑"),
  bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ⍒")
]
bstack1l1l1llll1_opy_ = {
  bstack1l1llll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧ⍓"): [bstack1l1llll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨ⍔")],
  bstack1l1llll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ⍕"): [bstack1l1llll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ⍖")],
  bstack1l1llll_opy_ (u"ࠥࡥࡺࡺ࡯ࠣ⍗"): [bstack1l1llll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣ⍘"), bstack1l1llll_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣ⍙"), bstack1l1llll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ⍚"), bstack1l1llll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨ⍛")],
  bstack1l1llll_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣ⍜"): [bstack1l1llll_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤ⍝")],
  bstack1l1llll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ⍞"): [bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ⍟")],
}
bstack1lllllll11l1_opy_ = {
  bstack1l1llll_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦ⍠"): bstack1l1llll_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧ⍡"),
  bstack1l1llll_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ⍢"): bstack1l1llll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ⍣"),
  bstack1l1llll_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨ⍤"): bstack1l1llll_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧ⍥"),
  bstack1l1llll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢ⍦"): bstack1l1llll_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࠢ⍧"),
  bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ⍨"): bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ⍩")
}
bstack1llllll11_opy_ = {
  bstack1l1llll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ⍪"): bstack1l1llll_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡕࡨࡸࡺࡶࠧ⍫"),
  bstack1l1llll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭⍬"): bstack1l1llll_opy_ (u"ࠫࡘࡻࡩࡵࡧࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬ⍭"),
  bstack1l1llll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⍮"): bstack1l1llll_opy_ (u"࠭ࡔࡦࡵࡷࠤࡘ࡫ࡴࡶࡲࠪ⍯"),
  bstack1l1llll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ⍰"): bstack1l1llll_opy_ (u"ࠨࡖࡨࡷࡹࠦࡔࡦࡣࡵࡨࡴࡽ࡮ࠨ⍱")
}
bstack1llllll11lll_opy_ = 65536
bstack1111111llll_opy_ = bstack1l1llll_opy_ (u"ࠩ࠱࠲࠳ࡡࡔࡓࡗࡑࡇࡆ࡚ࡅࡅ࡟ࠪ⍲")
bstack11111111111_opy_ = [
      bstack1l1llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ⍳"), bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ⍴"), bstack1l1llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⍵"), bstack1l1llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⍶"), bstack1l1llll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩ⍷"),
      bstack1l1llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ⍸"), bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ⍹"), bstack1l1llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫ⍺"), bstack1l1llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬ⍻"),
      bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡐࡤࡱࡪ࠭⍼"), bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ⍽"), bstack1l1llll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ⍾"), bstack1l1llll_opy_ (u"ࠨࡷࡶࡩࡷࡥࡤࡢࡶࡤࠫ⍿"), bstack1l1llll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⎀"),
      bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࠧ⎁"), bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡯ࡪࡿࠧ⎂"), bstack1l1llll_opy_ (u"ࠬࡰࡷࡵࠩ⎃")
    ]
bstack11111111ll1_opy_= {
  bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⎄"): bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⎅"),
  bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ⎆"): bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭⎇"),
  bstack1l1llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⎈"): bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ⎉"),
  bstack1l1llll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⎊"): bstack1l1llll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⎋"),
  bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⎌"): bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⎍"),
  bstack1l1llll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ⎎"): bstack1l1llll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ⎏"),
  bstack1l1llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⎐"): bstack1l1llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⎑"),
  bstack1l1llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⎒"): bstack1l1llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⎓"),
  bstack1l1llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⎔"): bstack1l1llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⎕"),
  bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ⎖"): bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⎗"),
  bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⎘"): bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⎙"),
  bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧ⎚"): bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨ⎛"),
  bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⎜"): bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⎝"),
  bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫ⎞"): bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࡔࡶࡴࡪࡱࡱࡷࠬ⎟"),
  bstack1l1llll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ⎠"): bstack1l1llll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩ⎡"),
  bstack1l1llll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⎢"): bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⎣"),
  bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⎤"): bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⎥"),
  bstack1l1llll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩ⎦"): bstack1l1llll_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪ⎧"),
  bstack1l1llll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⎨"): bstack1l1llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⎩"),
  bstack1l1llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⎪"): bstack1l1llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⎫"),
  bstack1l1llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ⎬"): bstack1l1llll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨ⎭"),
  bstack1l1llll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ⎮"): bstack1l1llll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ⎯"),
  bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⎰"): bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⎱"),
  bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ⎲"): bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ⎳"),
  bstack1l1llll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⎴"): bstack1l1llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⎵"),
  bstack1l1llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫ⎶"): bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬ⎷"),
  bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭⎸"): bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ⎹"),
  bstack1l1llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ⎺"): bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬ⎻"),
  bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡈࡧࡃࡦࡴࡷ࡭࡫࡯ࡣࡢࡶࡨࠫ⎼"): bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡉࡡࡄࡧࡵࡸ࡮࡬ࡩࡤࡣࡷࡩࠬ⎽")
}
bstack111111l1111_opy_ = [bstack1l1llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⎾"), bstack1l1llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ⎿")]
bstack1l111lll11_opy_ = (bstack1l1llll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥ⏀"),)
bstack1111111l11l_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡺࡶࡤࡢࡶࡨࡣࡨࡲࡩࠨ⏁")
bstack11lll1l11l1_opy_ = 32
bstack1l11l1l1l11_opy_ = 3
bstack11lll1lll1l_opy_ = 1.0
bstack1ll1llll11l_opy_ = bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡩࡵ࡭ࡩࡹ࠯ࠣ⏂")
bstack1l11l1l111_opy_ = bstack1l1llll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨࡴ࡬ࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡤࡷ࡭ࡨ࡯ࡢࡴࡧ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࠧ⏃")
bstack1l11lll11l_opy_ = bstack1l1llll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠰ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠣ⏄")
class EVENTS(Enum):
  bstack1lllllll11ll_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࠱࠲ࡻ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬ⏅")
  bstack1llll11l11_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࠧ⏆")
  bstack11l11l11l1_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡥࡱ࡯ࡺࡦࠩ⏇")
  bstack1lllllll1ll1_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡲ࡯ࡨࡵࠪ⏈")
  bstack11l111l1ll_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨ⏉") #shift post bstack111111111l1_opy_
  bstack1ll111l1l1_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡶࡲࡪࡰࡷ࠱ࡧࡻࡩ࡭ࡦ࡯࡭ࡳࡱࠧ⏊") #shift post bstack111111111l1_opy_
  bstack1111111l111_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡪࡸࡦࠬ⏋") #shift
  bstack1llllllll1l1_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡩࡵࡷ࡯࡮ࡲࡥࡩ࠭⏌") #shift
  bstack1l11ll1111_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽࡬ࡺࡨ࠭࡮ࡣࡱࡥ࡬࡫࡭ࡦࡰࡷࠫ⏍")
  bstack11ll1ll1111_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿ࡹࡡࡷࡧ࠰ࡶࡪࡹࡵ࡭ࡶࡶࠫ⏎")
  bstack11l111llll_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡤࡳ࡫ࡹࡩࡷ࠳ࡰࡦࡴࡩࡳࡷࡳࡳࡤࡣࡱࠫ⏏")
  bstack1llll1ll111_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡱࡵࡣࡢ࡮ࠪ⏐") #shift
  bstack1lll1lllll1_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡤࡴࡵ࠳ࡵࡱ࡮ࡲࡥࡩ࠭⏑") #shift
  bstack11l1lll1ll_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡣࡪ࠯ࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠬ⏒")
  bstack11l111111l_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠭ࡳࡧࡶࡹࡱࡺࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠩ⏓") #shift
  bstack1l11l111l1_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴࠩ⏔") #shift
  bstack1llllllll1ll_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾ࠭⏕") #shift
  bstack11l1l1l1lll_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ⏖")
  bstack111llll111_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡹࡴࡢࡶࡸࡷࠬ⏗") #shift
  bstack1ll1lll1l1_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿࡮ࡵࡣ࠯ࡰࡥࡳࡧࡧࡦ࡯ࡨࡲࡹ࠭⏘")
  bstack1llllll1l111_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸ࡯ࡹࡻ࠰ࡷࡪࡺࡵࡱࠩ⏙") #shift
  bstack1111l1l1l_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥࡵࡷࡳࠫ⏚")
  bstack111111111ll_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡹ࡮ࡢࡲࡶ࡬ࡴࡺࠧ⏛") # not bstack1llllll1l1l1_opy_ in python
  bstack1llllll1ll1_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡲࡷ࡬ࡸࠬ⏜") # used in bstack1llllllll111_opy_
  bstack111l111ll1l_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡵࡩ࠲ࡷࡵࡪࡶࠪ⏝")
  bstack111l11l1111_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡳࡸࡺ࠭ࡲࡷ࡬ࡸࠬ⏞")
  bstack1l1llll1l1_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽࡫ࡪࡺࠧ⏟") # used in bstack1llllllll111_opy_
  bstack1ll11lll1l_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾࡭ࡵ࡯࡬ࠩ⏠")
  bstack111l1l11l11_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡦ࠯࡫ࡳࡴࡱࠧ⏡")
  bstack111l1l11l1l_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡰࡰࡵࡷ࠱࡭ࡵ࡯࡬ࠩ⏢")
  bstack1ll1111lll1_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠨ⏣")
  SDK_AUTOMATE_SESSION_ANNOTATION = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠨ⏤") #
  bstack11l1l111ll_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡵࡣ࡮ࡩࡘࡩࡲࡦࡧࡱࡗ࡭ࡵࡴࠨ⏥")
  bstack111l1111ll_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡤࡹࡹࡵ࠭ࡤࡣࡳࡸࡺࡸࡥࠨ⏦")
  bstack11ll1lll1l_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸࡥ࠮ࡶࡨࡷࡹ࠭⏧")
  bstack1l1l1l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡶ࡯ࡴࡶ࠰ࡸࡪࡹࡴࠨ⏨")
  bstack1ll1lllll1l_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡳࡧ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫ⏩") #shift
  bstack1ll1llll1ll_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭⏪") #shift
  bstack1lllllll1111_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴ࠳ࡣࡢࡲࡷࡹࡷ࡫ࠧ⏫")
  bstack111111l111l_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾࡮ࡪ࡬ࡦ࠯ࡷ࡭ࡲ࡫࡯ࡶࡶࠪ⏬")
  bstack1l1lll1l111_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡩࡽ࡯ࡴ࠮ࡪࡤࡲࡩࡲࡥࡳࠩ⏭")
  bstack1l11l1111l1_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡧࡻ࡭ࡹ࠳ࡨࡢࡰࡧࡰࡪࡸࠧ⏮")
  bstack1lllllll1l11_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࠰ࡱࡪࡺࡲࡪࡥࡶࠫ⏯")
  bstack11111111lll_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡴࡦࡵࡷ࡬ࡺࡨ࠺ࡴࡶࡲࡴࠬ⏰")
  bstack1l11111lll1_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡸࡺࡡࡳࡶࠪ⏱")
  bstack1llllll1ll11_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧ⏲")
  bstack11111111l1l_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡣࡩࡧࡦ࡯࠲ࡻࡰࡥࡣࡷࡩࠬ⏳")
  bstack11llllll1ll_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠭⏴")
  bstack1l11111l111_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡸࡺࡡࡳࡶࡥ࡭ࡳࡧࡲࡺࠩ⏵")
  bstack1l1111l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡩ࡯࡯ࡰࡨࡧࡹ࠭⏶")
  bstack1l111111l11_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡳࡵࡱࡳࠫ⏷")
  bstack1l111ll1ll1_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡶࡤࡶࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩ⏸")
  bstack11llll1llll_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡥࡲࡲࡳ࡫ࡣࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲࠬ⏹")
  bstack1llllll1l1ll_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹ࠭⏺")
  SDK_DRIVER_INIT_FAILURE = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽࡭ࡳ࡯ࡴ࠻ࡨࡤ࡭ࡱࡻࡲࡦࠩ⏻")
  bstack1lllllll111l_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡥࡐࡨࡥࡷ࡫ࡳࡵࡊࡸࡦࠬ⏼")
  bstack11l1111l1ll_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡍࡳ࡯ࡴࠨ⏽")
  bstack111llll11ll_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡳࡶࠪ⏾")
  bstack11ll11lll11_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡃࡰࡰࡩ࡭࡬࠭⏿")
  bstack1lllllll1l1l_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡄࡱࡱࡪ࡮࡭ࠧ␀")
  bstack11ll1111111_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࡭ࡘ࡫࡬ࡧࡊࡨࡥࡱ࡙ࡴࡦࡲࠪ␁")
  bstack11l1llllll1_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࡮࡙ࡥ࡭ࡨࡋࡩࡦࡲࡇࡦࡶࡕࡩࡸࡻ࡬ࡵࠩ␂")
  SDK_TEST_FRAMEWORK_EVENT = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡉࡻ࡫࡮ࡵࠩ␃")
  SDK_TEST_SESSION_EVENT = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠨ␄")
  SDK_CLI_LOG_CREATED_EVENT = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡰࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࡅࡷࡧࡱࡸࠬ␅")
  bstack1lllllllllll_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡪࡴࡱࡶࡧࡸࡩ࡙࡫ࡳࡵࡇࡹࡩࡳࡺࠧ␆")
  bstack111llll1ll1_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡱࡳࠫ␇")
  bstack1l111lll1l1_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡲࡲࡘࡺ࡯ࡱࠩ␈")
  bstack1111ll11l11_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳ࡙ࡵࡲ࡯ࡢࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧ␉")
  bstack1l111llll1_opy_ = bstack1l1llll_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫࡮ࡥࡈࡸࡲࡳ࡫࡬ࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠧ␊")
  bstack1111ll1lll_opy_ = bstack1l1llll_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦࡉࡹࡳࡴࡥ࡭ࡖࡨࡷࡹࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠨ␋")
  bstack11ll1ll1l_opy_ = bstack1l1llll_opy_ (u"ࠩࡶࡨࡰࡀࡡࡱࡲ࡯ࡽࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡔࡾࡺࡥࡴࡶࠪ␌")
  bstack1ll1ll1l_opy_ = bstack1l1llll_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳࡰࡾࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡇ࡫ࡨࡢࡸࡨࠫ␍")
  bstack11lll11l1_opy_ = bstack1l1llll_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡨ࡫ࡳࡴࡃࡵ࡫ࡸࡖࡹࡵࡧࡶࡸࠬ␎")
  bstack11llll111_opy_ = bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡽࡹ࡫ࡳࡵࡉࡨࡸ࡙ࡵࡴࡢ࡮ࡗࡩࡸࡺࡳࠨ␏")
class STAGE(Enum):
  bstack1l11ll1l1l_opy_ = bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬ␐")
  END = bstack1l1llll_opy_ (u"ࠧࡦࡰࡧࠫ␑")
  SINGLE = bstack1l1llll_opy_ (u"ࠨࡵ࡬ࡲ࡬ࡲࡥࠨ␒")
bstack1ll11lll1ll_opy_ = {
  bstack1l1llll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࠩ␓"): bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ␔"),
  bstack1l1llll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨ␕"): bstack1l1llll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ␖"),
  bstack1l1llll_opy_ (u"࠭ࡂࡆࡊࡄ࡚ࡊ࠭␗"): bstack1l1llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ␘")
}
PLAYWRIGHT_HUB_URL = bstack1l1llll_opy_ (u"ࠣࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠥ␙")
MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION = 98
MINIMUM_NON_BSTACK_INFRA_A11Y_SUPPORTED_CHROME_VERSION = 100
MINIMUM_CHROMEFORTESTING_SUPPORTED_VERSION = 141
ACCESSIBILITY_SUPPORTED_BROWSERS = {
    bstack1l1llll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ␚"): {
        bstack1l1llll_opy_ (u"ࠪࡨ࡮ࡹࡰ࡭ࡣࡼࡣࡳࡧ࡭ࡦࠩ␛"): bstack1l1llll_opy_ (u"ࠫࡈ࡮ࡲࡰ࡯ࡨࠫ␜"),
        bstack1l1llll_opy_ (u"ࠬࡳࡩ࡯ࡡࡹࡩࡷࡹࡩࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ␝"): bstack1l1llll_opy_ (u"࠭࠹࠺ࠩ␞"),
        bstack1l1llll_opy_ (u"ࠧ࡮࡫ࡱࡣࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ␟"): bstack1l1llll_opy_ (u"ࠨ࠳࠳࠵ࠬ␠"),
        bstack1l1llll_opy_ (u"ࠩࡰ࡭ࡳࡥࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ␡"): bstack1l1llll_opy_ (u"ࠪ࠵࠵࠷ࠧ␢"),
        bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡱࡶ࡫ࡵࡩࡸࡥࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡤࡪࡨࡧࡰ࠭␣"): True
    },
    bstack1l1llll_opy_ (u"ࠬࡩࡨࡳࡱࡰ࡭ࡺࡳࠧ␤"): {
        bstack1l1llll_opy_ (u"࠭ࡤࡪࡵࡳࡰࡦࡿ࡟࡯ࡣࡰࡩࠬ␥"): bstack1l1llll_opy_ (u"ࠧࡄࡪࡵࡳࡲ࡫ࠧ␦"),
        bstack1l1llll_opy_ (u"ࠨ࡯࡬ࡲࡤࡼࡥࡳࡵ࡬ࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ␧"): bstack1l1llll_opy_ (u"ࠩ࠼࠽ࠬ␨"),
        bstack1l1llll_opy_ (u"ࠪࡱ࡮ࡴ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ␩"): bstack1l1llll_opy_ (u"ࠫ࠶࠶࠱ࠨ␪"),
        bstack1l1llll_opy_ (u"ࠬࡳࡩ࡯ࡡࡹࡩࡷࡹࡩࡰࡰࡢࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ␫"): bstack1l1llll_opy_ (u"࠭࠱࠱࠳ࠪ␬"),
        bstack1l1llll_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥࡴࡡࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡧ࡭࡫ࡣ࡬ࠩ␭"): True
    },
    bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡩࡨࡳࡱࡰ࡭ࡺࡳࠧ␮"): {
        bstack1l1llll_opy_ (u"ࠩࡧ࡭ࡸࡶ࡬ࡢࡻࡢࡲࡦࡳࡥࠨ␯"): bstack1l1llll_opy_ (u"ࠪࡇ࡭ࡸ࡯࡮ࡧࠪ␰"),
        bstack1l1llll_opy_ (u"ࠫࡲ࡯࡮ࡠࡸࡨࡶࡸ࡯࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ␱"): bstack1l1llll_opy_ (u"ࠬ࠿࠹ࠨ␲"),
        bstack1l1llll_opy_ (u"࠭࡭ࡪࡰࡢࡺࡪࡸࡳࡪࡱࡱࡣࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ␳"): bstack1l1llll_opy_ (u"ࠧ࠲࠲࠴ࠫ␴"),
        bstack1l1llll_opy_ (u"ࠨ࡯࡬ࡲࡤࡼࡥࡳࡵ࡬ࡳࡳࡥࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ␵"): bstack1l1llll_opy_ (u"ࠩ࠴࠴࠶࠭␶"),
        bstack1l1llll_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡷࡤࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡣࡩࡧࡦ࡯ࠬ␷"): True
    },
    bstack1l1llll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡪࡴࡸࡴࡦࡵࡷ࡭ࡳ࡭ࠧ␸"): {
        bstack1l1llll_opy_ (u"ࠬࡪࡩࡴࡲ࡯ࡥࡾࡥ࡮ࡢ࡯ࡨࠫ␹"): bstack1l1llll_opy_ (u"࠭ࡃࡩࡴࡲࡱࡪࡌ࡯ࡳࡖࡨࡷࡹ࡯࡮ࡨࠩ␺"),
        bstack1l1llll_opy_ (u"ࠧ࡮࡫ࡱࡣࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ␻"): bstack1l1llll_opy_ (u"ࠨ࠳࠷࠵ࠬ␼"),
        bstack1l1llll_opy_ (u"ࠩࡰ࡭ࡳࡥࡶࡦࡴࡶ࡭ࡴࡴ࡟࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ␽"): bstack1l1llll_opy_ (u"ࠪ࠵࠹࠷ࠧ␾"),
        bstack1l1llll_opy_ (u"ࠫࡲ࡯࡮ࡠࡸࡨࡶࡸ࡯࡯࡯ࡡࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭␿"): bstack1l1llll_opy_ (u"ࠬ࠷࠴࠲ࠩ⑀"),
        bstack1l1llll_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫ࡳࡠࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡦ࡬ࡪࡩ࡫ࠨ⑁"): True
    },
    bstack1l1llll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ⑂"): {
        bstack1l1llll_opy_ (u"ࠨࡦ࡬ࡷࡵࡲࡡࡺࡡࡱࡥࡲ࡫ࠧ⑃"): bstack1l1llll_opy_ (u"ࠩࡖࡥ࡫ࡧࡲࡪࠩ⑄"),
        bstack1l1llll_opy_ (u"ࠪࡱ࡮ࡴ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⑅"): bstack1l1llll_opy_ (u"ࠫ࠶࠾࠮࠵ࠩ⑆"),
        bstack1l1llll_opy_ (u"ࠬࡳࡩ࡯ࡡࡹࡩࡷࡹࡩࡰࡰࡢࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⑇"): bstack1l1llll_opy_ (u"࠭࠱࠹࠰࠷ࠫ⑈"),
        bstack1l1llll_opy_ (u"ࠧ࡮࡫ࡱࡣࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⑉"): bstack1l1llll_opy_ (u"ࠨ࠳࠻࠲࠹࠭⑊"),
        bstack1l1llll_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡶࡣࡨ࡮ࡲࡰ࡯ࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤࡩࡨࡦࡥ࡮ࠫ⑋"): False
    }
}
bstack1llll1lll11_opy_ = (bstack1l1llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ⑌"), bstack1l1llll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠭⑍"), bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠯ࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫ⑎"))
bstack11l1l11ll_opy_ = {
  bstack1l1llll_opy_ (u"࠭ࡲࡦࡴࡸࡲࠬ⑏"): bstack1l1llll_opy_ (u"ࠧ࠮࠯ࡵࡩࡷࡻ࡮ࡴࠩ⑐"),
  bstack1l1llll_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧ⑑"): bstack1l1llll_opy_ (u"ࠩ࠰࠱ࡷ࡫ࡲࡶࡰࡶ࠱ࡩ࡫࡬ࡢࡻࠪ⑒"),
  bstack1l1llll_opy_ (u"ࠪࡶࡪࡸࡵ࡯࠯ࡧࡩࡱࡧࡹࠨ⑓"): 0
}
bstack1111111l1ll_opy_ = bstack1l1llll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦ⑔")
bstack1llllll1ll1l_opy_ = bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡵࡱ࡮ࡲࡥࡩ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ⑕")
bstack1lll11ll1l_opy_ = bstack1l1llll_opy_ (u"ࠨࡔࡆࡕࡗࠤࡗࡋࡐࡐࡔࡗࡍࡓࡍࠠࡂࡐࡇࠤࡆࡔࡁࡍ࡛ࡗࡍࡈ࡙ࠢ⑖")
MAX_DRIVER_INIT_ERROR_BYTES = 8000
BROWSERSTACK_SDK_RUN_ID_ENV = bstack1l1llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡖ࡚ࡔ࡟ࡊࡆࠥ⑗")
DRIVER_INIT_FAILURE_EDS_TIMEOUT_SECONDS = 5
bstack1111111ll1l_opy_ = bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࡐࡲࡷ࡭ࡴࡴࡳ࠯ࡶࡨࡷࡹࡖ࡬ࡢࡰࡌࡨࠬ⑘")
bstack1lllllllll11_opy_ = bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡐࡍࡃࡑࡣࡎࡊࠧ⑙")