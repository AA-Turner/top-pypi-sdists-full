# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import re
from enum import Enum
bstack11ll111l_opy_ = {
  bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᦣ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩᦤ"),
  bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᦥ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪᦦ"),
  bstack11l1l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᦧ"): bstack11l1l11_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᦨ"),
  bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᦩ"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫᦪ"),
  bstack11l1l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᦫ"): bstack11l1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧ᦬"),
  bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ᦭"): bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧ᦮"),
  bstack11l1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᦯"): bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᦰ"),
  bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᦱ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪᦲ"),
  bstack11l1l11_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫᦳ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧᦴ"),
  bstack11l1l11_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᦵ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᦶ"),
  bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᦷ"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᦸ"),
  bstack11l1l11_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫᦹ"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫᦺ"),
  bstack11l1l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᦻ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᦼ"),
  bstack11l1l11_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᦽ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩᦾ"),
  bstack11l1l11_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᦿ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩᧀ"),
  bstack11l1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨᧁ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨᧂ"),
  bstack11l1l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᧃ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᧄ"),
  bstack11l1l11_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩᧅ"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩᧆ"),
  bstack11l1l11_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᧇ"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᧈ"),
  bstack11l1l11_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧᧉ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧ᧊"),
  bstack11l1l11_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫ᧋"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫ᧌"),
  bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭᧍"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭᧎"),
  bstack11l1l11_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬ᧏"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬ᧐"),
  bstack11l1l11_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩ᧑"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩ᧒"),
  bstack11l1l11_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ᧓"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ᧔"),
  bstack11l1l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ᧕"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ᧖"),
  bstack11l1l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ᧗"): bstack11l1l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ᧘"),
  bstack11l1l11_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭᧙"): bstack11l1l11_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨ᧚"),
  bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ᧛"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᧜"),
  bstack11l1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭᧝"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭᧞"),
  bstack11l1l11_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ᧟"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ᧠"),
  bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩ᧡"): bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬ᧢"),
  bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᧣"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᧤"),
  bstack11l1l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ᧥"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧ᧦"),
  bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᧧"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᧨"),
  bstack11l1l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭᧩"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭᧪"),
  bstack11l1l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩ᧫"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩ᧬"),
  bstack11l1l11_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬ᧭"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬ᧮"),
  bstack11l1l11_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨ᧯"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨ᧰"),
  bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᧱"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᧲"),
  bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᧳"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᧴")
}
bstack111llllll11_opy_ = [
  bstack11l1l11_opy_ (u"ࠩࡲࡷࠬ᧵"),
  bstack11l1l11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᧶"),
  bstack11l1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᧷"),
  bstack11l1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᧸"),
  bstack11l1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ᧹"),
  bstack11l1l11_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ᧺"),
  bstack11l1l11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᧻"),
]
bstack11ll1l11l_opy_ = {
  bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ᧼"): [bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ᧽"), bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡐࡄࡑࡊ࠭᧾")],
  bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᧿"): bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᨀ"),
  bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᨁ"): bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠫᨂ"),
  bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᨃ"): bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠨᨄ"),
  bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᨅ"): bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᨆ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᨇ"): bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡔࡡࡓࡉࡗࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨᨈ"),
  bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᨉ"): bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧᨊ"),
  bstack11l1l11_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧᨋ"): bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨᨌ"),
  bstack11l1l11_opy_ (u"ࠬࡧࡰࡱࠩᨍ"): [bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࡡࡌࡈࠬᨎ"), bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࠪᨏ")],
  bstack11l1l11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᨐ"): bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡒࡏࡈࡎࡈ࡚ࡊࡒࠧᨑ"),
  bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᨒ"): bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᨓ"),
  bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᨔ"): [bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠪᨕ"), bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧᨖ")],
  bstack11l1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᨗ"): bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡘࡖࡇࡕࡓࡄࡃࡏࡉᨘࠬ"),
  bstack11l1l11_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡊࡔࡖࠨᨙ"): bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡓࡗࡉࡈࡆࡕࡗࡖࡆ࡚ࡉࡐࡐࡢࡗࡒࡇࡒࡕࡡࡖࡉࡑࡋࡃࡕࡋࡒࡒࡤࡌࡅࡂࡖࡘࡖࡊࡥࡂࡓࡃࡑࡇࡍࡋࡓࠨᨚ")
}
bstack11l111ll_opy_ = {
  bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᨛ"): [bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡢࡲࡦࡳࡥࠨ᨜"), bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡒࡦࡳࡥࠨ᨝")],
  bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᨞"): [bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡠ࡭ࡨࡽࠬ᨟"), bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᨠ")],
  bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᨡ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᨢ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᨣ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᨤ"),
  bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᨥ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᨦ"),
  bstack11l1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᨧ"): [bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡵࡶࠧᨨ"), bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᨩ")],
  bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᨪ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬᨫ"),
  bstack11l1l11_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᨬ"): bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᨭ"),
  bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࠧᨮ"): bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࠧᨯ"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᨰ"): bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᨱ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᨲ"): bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᨳ"),
  bstack11l1l11_opy_ (u"ࠤࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࡇࡑࡏࠢᨴ"): bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࠣᨵ"),
}
bstack1l1l11l1l_opy_ = {
  bstack11l1l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᨶ"): bstack11l1l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᨷ"),
  bstack11l1l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᨸ"): [bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᨹ"), bstack11l1l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᨺ")],
  bstack11l1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᨻ"): bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᨼ"),
  bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᨽ"): bstack11l1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᨾ"),
  bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᨿ"): [bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᩀ"), bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᩁ")],
  bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᩂ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᩃ"),
  bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᩄ"): bstack11l1l11_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪᩅ"),
  bstack11l1l11_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᩆ"): [bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᩇ"), bstack11l1l11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᩈ")],
  bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᩉ"): [bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫᩊ"), bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫᩋ")]
}
bstack1llll1ll_opy_ = [
  bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᩌ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᩍ"),
  bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ᩎ"),
  bstack11l1l11_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨᩏ"),
  bstack11l1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫᩐ"),
  bstack11l1l11_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨᩑ"),
  bstack11l1l11_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧᩒ"),
  bstack11l1l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᩓ"),
  bstack11l1l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᩔ"),
  bstack11l1l11_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᩕ"),
  bstack11l1l11_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩖ"),
  bstack11l1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᩗ"),
]
bstack11ll11l1ll_opy_ = [
  bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᩘ"),
  bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᩙ"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᩚ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᩛ"),
  bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᩜ"),
  bstack11l1l11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᩝ"),
  bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᩞ"),
  bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᩟"),
  bstack11l1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ᩠ࠧ"),
  bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᩡ"),
  bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᩢ"),
  bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧᩣ"),
  bstack11l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᩤ"),
  bstack11l1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡖࡤ࡫ࠬᩥ"),
  bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᩦ"),
  bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᩧ"),
  bstack11l1l11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᩨ"),
  bstack11l1l11_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠵ࠬᩩ"),
  bstack11l1l11_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠷࠭ᩪ"),
  bstack11l1l11_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠹ࠧᩫ"),
  bstack11l1l11_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠴ࠨᩬ"),
  bstack11l1l11_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠶ࠩᩭ"),
  bstack11l1l11_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠸ࠪᩮ"),
  bstack11l1l11_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠺ࠫᩯ"),
  bstack11l1l11_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠼ࠬᩰ"),
  bstack11l1l11_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠾࠭ᩱ"),
  bstack11l1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᩲ"),
  bstack11l1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᩳ"),
  bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ᩴ"),
  bstack11l1l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭᩵"),
  bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᩶"),
  bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᩷"),
  bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ᩸"),
  bstack11l1l11_opy_ (u"ࠨࡪࡸࡦࡗ࡫ࡧࡪࡱࡱࠫ᩹")
]
bstack111lll11l11_opy_ = [
  bstack11l1l11_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧ᩺"),
  bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᩻"),
  bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᩼"),
  bstack11l1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᩽"),
  bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡔࡷ࡯࡯ࡳ࡫ࡷࡽࠬ᩾"),
  bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ᩿ࠪ"),
  bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡔࡢࡩࠪ᪀"),
  bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ᪁"),
  bstack11l1l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᪂"),
  bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ᪃"),
  bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᪄"),
  bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ᪅"),
  bstack11l1l11_opy_ (u"ࠧࡰࡵࠪ᪆"),
  bstack11l1l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ᪇"),
  bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨ᪈"),
  bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬ᪉"),
  bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡧࡪࡱࡱࠫ᪊"),
  bstack11l1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧ᪋"),
  bstack11l1l11_opy_ (u"࠭࡭ࡢࡥ࡫࡭ࡳ࡫ࠧ᪌"),
  bstack11l1l11_opy_ (u"ࠧࡳࡧࡶࡳࡱࡻࡴࡪࡱࡱࠫ᪍"),
  bstack11l1l11_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᪎"),
  bstack11l1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭᪏"),
  bstack11l1l11_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩ᪐"),
  bstack11l1l11_opy_ (u"ࠫࡳࡵࡐࡢࡩࡨࡐࡴࡧࡤࡕ࡫ࡰࡩࡴࡻࡴࠨ᪑"),
  bstack11l1l11_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭᪒"),
  bstack11l1l11_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬ᪓"),
  bstack11l1l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ᪔"),
  bstack11l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩ᪕"),
  bstack11l1l11_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭᪖"),
  bstack11l1l11_opy_ (u"ࠪࡲࡴࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠧ᪗"),
  bstack11l1l11_opy_ (u"ࠫࡨ࡮ࡥࡤ࡭ࡘࡖࡑ࠭᪘"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᪙"),
  bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡉ࡯ࡰ࡭࡬ࡩࡸ࠭᪚"),
  bstack11l1l11_opy_ (u"ࠧࡤࡣࡳࡸࡺࡸࡥࡄࡴࡤࡷ࡭࠭᪛"),
  bstack11l1l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ᪜"),
  bstack11l1l11_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᪝"),
  bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡖࡦࡴࡶ࡭ࡴࡴࠧ᪞"),
  bstack11l1l11_opy_ (u"ࠫࡳࡵࡂ࡭ࡣࡱ࡯ࡕࡵ࡬࡭࡫ࡱ࡫ࠬ᪟"),
  bstack11l1l11_opy_ (u"ࠬࡳࡡࡴ࡭ࡖࡩࡳࡪࡋࡦࡻࡶࠫ᪠"),
  bstack11l1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡒ࡯ࡨࡵࠪ᪡"),
  bstack11l1l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡉࡥࠩ᪢"),
  bstack11l1l11_opy_ (u"ࠨࡦࡨࡨ࡮ࡩࡡࡵࡧࡧࡈࡪࡼࡩࡤࡧࠪ᪣"),
  bstack11l1l11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡒࡤࡶࡦࡳࡳࠨ᪤"),
  bstack11l1l11_opy_ (u"ࠪࡴ࡭ࡵ࡮ࡦࡐࡸࡱࡧ࡫ࡲࠨ᪥"),
  bstack11l1l11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩ᪦"),
  bstack11l1l11_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡒࡴࡹ࡯࡯࡯ࡵࠪᪧ"),
  bstack11l1l11_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫ᪨"),
  bstack11l1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ᪩"),
  bstack11l1l11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬ᪪"),
  bstack11l1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡄ࡬ࡳࡲ࡫ࡴࡳ࡫ࡦࠫ᪫"),
  bstack11l1l11_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࡘ࠵ࠫ᪬"),
  bstack11l1l11_opy_ (u"ࠫࡲ࡯ࡤࡔࡧࡶࡷ࡮ࡵ࡮ࡊࡰࡶࡸࡦࡲ࡬ࡂࡲࡳࡷࠬ᪭"),
  bstack11l1l11_opy_ (u"ࠬ࡫ࡳࡱࡴࡨࡷࡸࡵࡓࡦࡴࡹࡩࡷ࠭᪮"),
  bstack11l1l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬ᪯"),
  bstack11l1l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡅࡧࡴࠬ᪰"),
  bstack11l1l11_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨ᪱"),
  bstack11l1l11_opy_ (u"ࠩࡶࡽࡳࡩࡔࡪ࡯ࡨ࡛࡮ࡺࡨࡏࡖࡓࠫ᪲"),
  bstack11l1l11_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨ᪳"),
  bstack11l1l11_opy_ (u"ࠫ࡬ࡶࡳࡍࡱࡦࡥࡹ࡯࡯࡯ࠩ᪴"),
  bstack11l1l11_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ᪵࠭"),
  bstack11l1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ᪶࠭"),
  bstack11l1l11_opy_ (u"ࠧࡧࡱࡵࡧࡪࡉࡨࡢࡰࡪࡩࡏࡧࡲࠨ᪷"),
  bstack11l1l11_opy_ (u"ࠨࡺࡰࡷࡏࡧࡲࠨ᪸"),
  bstack11l1l11_opy_ (u"ࠩࡻࡱࡽࡐࡡࡳ᪹ࠩ"),
  bstack11l1l11_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴ᪺ࠩ"),
  bstack11l1l11_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫ᪻"),
  bstack11l1l11_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭᪼"),
  bstack11l1l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴ᪽ࠩ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡲࡳ࡚ࡪࡸࡳࡪࡱࡱࠫ᪾"),
  bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹᪿࠧ"),
  bstack11l1l11_opy_ (u"ࠩࡵࡩࡸ࡯ࡧ࡯ࡃࡳࡴᫀࠬ"),
  bstack11l1l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳࡹࠧ᫁"),
  bstack11l1l11_opy_ (u"ࠫࡨࡧ࡮ࡢࡴࡼࠫ᫂"),
  bstack11l1l11_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ᫃࠭"),
  bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ᫄࠭"),
  bstack11l1l11_opy_ (u"ࠧࡪࡧࠪ᫅"),
  bstack11l1l11_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭᫆"),
  bstack11l1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ᫇"),
  bstack11l1l11_opy_ (u"ࠪࡵࡺ࡫ࡵࡦࠩ᫈"),
  bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡱࡥࡱ࠭᫉"),
  bstack11l1l11_opy_ (u"ࠬࡧࡰࡱࡕࡷࡳࡷ࡫ࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳ᫊࠭"),
  bstack11l1l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡉࡡ࡮ࡧࡵࡥࡎࡳࡡࡨࡧࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬ᫋"),
  bstack11l1l11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡊࡾࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪᫌ"),
  bstack11l1l11_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡏ࡮ࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫᫍ"),
  bstack11l1l11_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᫎ"),
  bstack11l1l11_opy_ (u"ࠪࡶࡪࡹࡥࡳࡸࡨࡈࡪࡼࡩࡤࡧࠪ᫏"),
  bstack11l1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ᫐"),
  bstack11l1l11_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧ᫑"),
  bstack11l1l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡡࡴࡵࡦࡳࡩ࡫ࠧ᫒"),
  bstack11l1l11_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡉࡰࡵࡇࡩࡻ࡯ࡣࡦࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ᫓"),
  bstack11l1l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡷࡧ࡭ࡴࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨ᫔"),
  bstack11l1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡳࡴࡱ࡫ࡐࡢࡻࠪ᫕"),
  bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ᫖"),
  bstack11l1l11_opy_ (u"ࠫࡼࡪࡩࡰࡕࡨࡶࡻ࡯ࡣࡦࠩ᫗"),
  bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᫘"),
  bstack11l1l11_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡃࡳࡱࡶࡷࡘ࡯ࡴࡦࡖࡵࡥࡨࡱࡩ࡯ࡩࠪ᫙"),
  bstack11l1l11_opy_ (u"ࠧࡩ࡫ࡪ࡬ࡈࡵ࡮ࡵࡴࡤࡷࡹ࠭᫚"),
  bstack11l1l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡑࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࡷࠬ᫛"),
  bstack11l1l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬ᫜"),
  bstack11l1l11_opy_ (u"ࠪࡷ࡮ࡳࡏࡱࡶ࡬ࡳࡳࡹࠧ᫝"),
  bstack11l1l11_opy_ (u"ࠫࡷ࡫࡭ࡰࡸࡨࡍࡔ࡙ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࡐࡴࡩࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ᫞"),
  bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧ᫟"),
  bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᫠"),
  bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᫡"),
  bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧ᫢"),
  bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ᫣"),
  bstack11l1l11_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭᫤"),
  bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ᫥"),
  bstack11l1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧ᫦"),
  bstack11l1l11_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ᫧")
]
bstack11l1111l11_opy_ = {
  bstack11l1l11_opy_ (u"ࠧࡷࠩ᫨"): bstack11l1l11_opy_ (u"ࠨࡸࠪ᫩"),
  bstack11l1l11_opy_ (u"ࠩࡩࠫ᫪"): bstack11l1l11_opy_ (u"ࠪࡪࠬ᫫"),
  bstack11l1l11_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪ᫬"): bstack11l1l11_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫ᫭"),
  bstack11l1l11_opy_ (u"࠭࡯࡯࡮ࡼࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᫮"): bstack11l1l11_opy_ (u"ࠧࡰࡰ࡯ࡽࡆࡻࡴࡰ࡯ࡤࡸࡪ࠭᫯"),
  bstack11l1l11_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬ᫰"): bstack11l1l11_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭᫱"),
  bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭᫲"): bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧ᫳"),
  bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨ᫴"): bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩ᫵"),
  bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪ᫶"): bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ᫷"),
  bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬ᫸"): bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭᫹"),
  bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬ᫺"): bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡊࡲࡷࡹ࠭᫻"),
  bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧ᫼"): bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨ᫽"),
  bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩ᫾"): bstack11l1l11_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫ᫿"),
  bstack11l1l11_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᬀ"): bstack11l1l11_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᬁ"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᬂ"): bstack11l1l11_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨᬃ"),
  bstack11l1l11_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᬄ"): bstack11l1l11_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪᬅ"),
  bstack11l1l11_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ᬆ"): bstack11l1l11_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧᬇ"),
  bstack11l1l11_opy_ (u"ࠫࡵࡧࡣࡧ࡫࡯ࡩࠬᬈ"): bstack11l1l11_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᬉ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᬊ"): bstack11l1l11_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᬋ"),
  bstack11l1l11_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᬌ"): bstack11l1l11_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᬍ"),
  bstack11l1l11_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫᬎ"): bstack11l1l11_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬᬏ"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᬐ"): bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᬑ"),
  bstack11l1l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩᬒ"): bstack11l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡳࡩࡦࡺࡥࡳࠩᬓ")
}
bstack111lll111l1_opy_ = bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫࡮ࡺࡨࡶࡤ࠱ࡧࡴࡳ࠯ࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫࠲ࡶࡪࡲࡥࡢࡵࡨࡷ࠴ࡲࡡࡵࡧࡶࡸ࠴ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᬔ")
bstack111ll1ll1ll_opy_ = bstack11l1l11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠲࡬ࡪࡧ࡬ࡵࡪࡦ࡬ࡪࡩ࡫ࠣᬕ")
bstack111l11lll1_opy_ = bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡫ࡤࡴ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡹࡥ࡯ࡦࡢࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢᬖ")
HTTPS_HUB = bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ᬗ")
bstack11ll1l1l11_opy_ = bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩᬘ")
bstack1ll1ll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠸࠹࠺࠴࠰ࡹࡧ࠳࡭ࡻࡢࠨᬙ")
bstack11l1llll1l_opy_ = bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬᬚ")
bstack111ll111_opy_ = {
  bstack11l1l11_opy_ (u"ࠩࡧࡩ࡫ࡧࡵ࡭ࡶࠪᬛ"): bstack11l1l11_opy_ (u"ࠪ࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᬜ"),
  bstack11l1l11_opy_ (u"ࠫࡺࡹ࠭ࡦࡣࡶࡸࠬᬝ"): bstack11l1l11_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡸࡷࡪ࠳࡯࡯࡮ࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᬞ"),
  bstack11l1l11_opy_ (u"࠭ࡵࡴࠩᬟ"): bstack11l1l11_opy_ (u"ࠧࡩࡷࡥ࠱ࡺࡹ࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᬠ"),
  bstack11l1l11_opy_ (u"ࠨࡧࡸࠫᬡ"): bstack11l1l11_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡥࡶ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᬢ"),
  bstack11l1l11_opy_ (u"ࠪ࡭ࡳ࠭ᬣ"): bstack11l1l11_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡣࡳࡷ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᬤ"),
  bstack11l1l11_opy_ (u"ࠬࡧࡵࠨᬥ"): bstack11l1l11_opy_ (u"࠭ࡨࡶࡤ࠰ࡥࡵࡹࡥ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᬦ")
}
bstack111ll1llll1_opy_ = {
  bstack11l1l11_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩᬧ"): 50,
  bstack11l1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᬨ"): 40,
  bstack11l1l11_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᬩ"): 30,
  bstack11l1l11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᬪ"): 20,
  bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᬫ"): 10
}
bstack1llllll1l_opy_ = bstack111ll1llll1_opy_[bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᬬ")]
bstack1lll1111ll_opy_ = bstack11l1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩ࠯ࠨᬭ")
bstack1ll1l11l11_opy_ = bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᬮ")
bstack11lll1l1_opy_ = bstack11l1l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᬯ")
bstack1ll1l111l1_opy_ = bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᬰ")
bstack11l11ll1ll_opy_ = bstack11l1l11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡦࡴࡤࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡴࡦࡩ࡫ࡢࡩࡨࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡠࠨᬱ")
bstack11l111l1l_opy_ = {
  bstack11l1l11_opy_ (u"ࠫࡘࡊࡋ࠮ࡉࡈࡒ࠲࠶࠰࠶ࠩᬲ"): bstack11l1l11_opy_ (u"ࠬ࠰ࠪࠫࠢ࡞ࡗࡉࡑ࠭ࡈࡇࡑ࠱࠵࠶࠵࡞ࠢࡣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࡥࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥ࡯࡮ࠡࡻࡲࡹࡷࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠲࡚ࠥࡨࡪࡵࠣࡱࡦࡿࠠࡤࡣࡸࡷࡪࠦࡣࡰࡰࡩࡰ࡮ࡩࡴࡴࠢࡺ࡭ࡹ࡮ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࠠࡪࡶࠣࡹࡸ࡯࡮ࡨ࠼ࠣࡴ࡮ࡶࠠࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࠥ࠰ࠪࠫࠩᬳ")
}
bstack111llll1ll1_opy_ = [bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋ᬴ࠧ"), bstack11l1l11_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᬵ")]
bstack111llllll1l_opy_ = [bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᬶ"), bstack11l1l11_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᬷ")]
bstack11l111ll1l_opy_ = re.compile(bstack11l1l11_opy_ (u"ࠪࡢࡠࡢ࡜ࡸ࠯ࡠ࠯࠿࠴ࠪࠥࠩᬸ"))
bstack1lllllllll_opy_ = [
  bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡏࡣࡰࡩࠬᬹ"),
  bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᬺ"),
  bstack11l1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᬻ"),
  bstack11l1l11_opy_ (u"ࠧ࡯ࡧࡺࡇࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࠫᬼ"),
  bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࠬᬽ"),
  bstack11l1l11_opy_ (u"ࠩࡸࡨ࡮ࡪࠧᬾ"),
  bstack11l1l11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬᬿ"),
  bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࠫᭀ"),
  bstack11l1l11_opy_ (u"ࠬࡵࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪᭁ"),
  bstack11l1l11_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࠫᭂ"),
  bstack11l1l11_opy_ (u"ࠧ࡯ࡱࡕࡩࡸ࡫ࡴࠨᭃ"), bstack11l1l11_opy_ (u"ࠨࡨࡸࡰࡱࡘࡥࡴࡧࡷ᭄ࠫ"),
  bstack11l1l11_opy_ (u"ࠩࡦࡰࡪࡧࡲࡔࡻࡶࡸࡪࡳࡆࡪ࡮ࡨࡷࠬᭅ"),
  bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡖ࡬ࡱ࡮ࡴࡧࡴࠩᭆ"),
  bstack11l1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࡍࡱࡪ࡫࡮ࡴࡧࠨᭇ"),
  bstack11l1l11_opy_ (u"ࠬࡵࡴࡩࡧࡵࡅࡵࡶࡳࠨᭈ"),
  bstack11l1l11_opy_ (u"࠭ࡰࡳ࡫ࡱࡸࡕࡧࡧࡦࡕࡲࡹࡷࡩࡥࡐࡰࡉ࡭ࡳࡪࡆࡢ࡫࡯ࡹࡷ࡫ࠧᭉ"),
  bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡅࡨࡺࡩࡷ࡫ࡷࡽࠬᭊ"), bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡕࡧࡣ࡬ࡣࡪࡩࠬᭋ"), bstack11l1l11_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡄࡧࡹ࡯ࡶࡪࡶࡼࠫᭌ"), bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡔࡦࡩ࡫ࡢࡩࡨࠫ᭍"), bstack11l1l11_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭᭎"),
  bstack11l1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᭏"),
  bstack11l1l11_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙࡫ࡳࡵࡒࡤࡧࡰࡧࡧࡦࡵࠪ᭐"),
  bstack11l1l11_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࠩ᭑"), bstack11l1l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡅࡲࡺࡪࡸࡡࡨࡧࡈࡲࡩࡏ࡮ࡵࡧࡱࡸࠬ᭒"),
  bstack11l1l11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧ᭓"),
  bstack11l1l11_opy_ (u"ࠪࡥࡩࡨࡐࡰࡴࡷࠫ᭔"),
  bstack11l1l11_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡗࡴࡩ࡫ࡦࡶࠪ᭕"),
  bstack11l1l11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᭖"),
  bstack11l1l11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡶ࡫ࠫ᭗"),
  bstack11l1l11_opy_ (u"ࠧࡢࡸࡧࠫ᭘"), bstack11l1l11_opy_ (u"ࠨࡣࡹࡨࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫ᭙"), bstack11l1l11_opy_ (u"ࠩࡤࡺࡩࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫ᭚"), bstack11l1l11_opy_ (u"ࠪࡥࡻࡪࡁࡳࡩࡶࠫ᭛"),
  bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡌࡧࡼࡷࡹࡵࡲࡦࠩ᭜"), bstack11l1l11_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡶ࡫ࠫ᭝"), bstack11l1l11_opy_ (u"࠭࡫ࡦࡻࡶࡸࡴࡸࡥࡑࡣࡶࡷࡼࡵࡲࡥࠩ᭞"),
  bstack11l1l11_opy_ (u"ࠧ࡬ࡧࡼࡅࡱ࡯ࡡࡴࠩ᭟"), bstack11l1l11_opy_ (u"ࠨ࡭ࡨࡽࡕࡧࡳࡴࡹࡲࡶࡩ࠭᭠"),
  bstack11l1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࠫ᭡"), bstack11l1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡃࡵ࡫ࡸ࠭᭢"), bstack11l1l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪࡊࡩࡳࠩ᭣"), bstack11l1l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡇ࡭ࡸ࡯࡮ࡧࡐࡥࡵࡶࡩ࡯ࡩࡉ࡭ࡱ࡫ࠧ᭤"), bstack11l1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶ࡚ࡹࡥࡔࡻࡶࡸࡪࡳࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪ᭥"),
  bstack11l1l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࠪ᭦"), bstack11l1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡐࡰࡴࡷࡷࠬ᭧"),
  bstack11l1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡅ࡫ࡶࡥࡧࡲࡥࡃࡷ࡬ࡰࡩࡉࡨࡦࡥ࡮ࠫ᭨"),
  bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࡕ࡫ࡰࡩࡴࡻࡴࠨ᭩"),
  bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡅࡨࡺࡩࡰࡰࠪ᭪"), bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡈࡧࡴࡦࡩࡲࡶࡾ࠭᭫"), bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡌ࡬ࡢࡩࡶ᭬ࠫ"), bstack11l1l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡡ࡭ࡋࡱࡸࡪࡴࡴࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᭭"),
  bstack11l1l11_opy_ (u"ࠨࡦࡲࡲࡹ࡙ࡴࡰࡲࡄࡴࡵࡕ࡮ࡓࡧࡶࡩࡹ࠭᭮"),
  bstack11l1l11_opy_ (u"ࠩࡸࡲ࡮ࡩ࡯ࡥࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫ᭯"), bstack11l1l11_opy_ (u"ࠪࡶࡪࡹࡥࡵࡍࡨࡽࡧࡵࡡࡳࡦࠪ᭰"),
  bstack11l1l11_opy_ (u"ࠫࡳࡵࡓࡪࡩࡱࠫ᭱"),
  bstack11l1l11_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩ࡚ࡴࡩ࡮ࡲࡲࡶࡹࡧ࡮ࡵࡘ࡬ࡩࡼࡹࠧ᭲"),
  bstack11l1l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯ࡦࡵࡳ࡮ࡪࡗࡢࡶࡦ࡬ࡪࡸࡳࠨ᭳"),
  bstack11l1l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᭴"),
  bstack11l1l11_opy_ (u"ࠨࡴࡨࡧࡷ࡫ࡡࡵࡧࡆ࡬ࡷࡵ࡭ࡦࡆࡵ࡭ࡻ࡫ࡲࡔࡧࡶࡷ࡮ࡵ࡮ࡴࠩ᭵"),
  bstack11l1l11_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ᭶"),
  bstack11l1l11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡐࡢࡶ࡫ࠫ᭷"),
  bstack11l1l11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡘࡶࡥࡦࡦࠪ᭸"),
  bstack11l1l11_opy_ (u"ࠬ࡭ࡰࡴࡇࡱࡥࡧࡲࡥࡥࠩ᭹"),
  bstack11l1l11_opy_ (u"࠭ࡩࡴࡊࡨࡥࡩࡲࡥࡴࡵࠪ᭺"),
  bstack11l1l11_opy_ (u"ࠧࡢࡦࡥࡉࡽ࡫ࡣࡕ࡫ࡰࡩࡴࡻࡴࠨ᭻"),
  bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࡔࡥࡵ࡭ࡵࡺࠧ᭼"),
  bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡄࡦࡸ࡬ࡧࡪࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᭽"),
  bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯ࡈࡴࡤࡲࡹࡖࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠪ᭾"),
  bstack11l1l11_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡓࡧࡴࡶࡴࡤࡰࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩ᭿"),
  bstack11l1l11_opy_ (u"ࠬࡹࡹࡴࡶࡨࡱࡕࡵࡲࡵࠩᮀ"),
  bstack11l1l11_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡇࡤࡣࡊࡲࡷࡹ࠭ᮁ"),
  bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴ࡚ࡴ࡬ࡰࡥ࡮ࠫᮂ"), bstack11l1l11_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡕࡻࡳࡩࠬᮃ"), bstack11l1l11_opy_ (u"ࠩࡸࡲࡱࡵࡣ࡬ࡍࡨࡽࠬᮄ"),
  bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯ࡍࡣࡸࡲࡨ࡮ࠧᮅ"),
  bstack11l1l11_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡨࡧࡴࡄࡣࡳࡸࡺࡸࡥࠨᮆ"),
  bstack11l1l11_opy_ (u"ࠬࡻ࡮ࡪࡰࡶࡸࡦࡲ࡬ࡐࡶ࡫ࡩࡷࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧᮇ"),
  bstack11l1l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡗࡪࡰࡧࡳࡼࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࠨᮈ"),
  bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚࡯ࡰ࡮ࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᮉ"),
  bstack11l1l11_opy_ (u"ࠨࡧࡱࡪࡴࡸࡣࡦࡃࡳࡴࡎࡴࡳࡵࡣ࡯ࡰࠬᮊ"),
  bstack11l1l11_opy_ (u"ࠩࡨࡲࡸࡻࡲࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡵࡋࡥࡻ࡫ࡐࡢࡩࡨࡷࠬᮋ"), bstack11l1l11_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡈࡪࡼࡴࡰࡱ࡯ࡷࡕࡵࡲࡵࠩᮌ"), bstack11l1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨ࡛ࡪࡨࡶࡪࡧࡺࡈࡪࡺࡡࡪ࡮ࡶࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠧᮍ"),
  bstack11l1l11_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡶࡰࡴࡅࡤࡧ࡭࡫ࡌࡪ࡯࡬ࡸࠬᮎ"),
  bstack11l1l11_opy_ (u"࠭ࡣࡢ࡮ࡨࡲࡩࡧࡲࡇࡱࡵࡱࡦࡺࠧᮏ"),
  bstack11l1l11_opy_ (u"ࠧࡣࡷࡱࡨࡱ࡫ࡉࡥࠩᮐ"),
  bstack11l1l11_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᮑ"),
  bstack11l1l11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡊࡴࡡࡣ࡮ࡨࡨࠬᮒ"), bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࡘ࡫ࡲࡷ࡫ࡦࡩࡸࡇࡵࡵࡪࡲࡶ࡮ࢀࡥࡥࠩᮓ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰࡃࡦࡧࡪࡶࡴࡂ࡮ࡨࡶࡹࡹࠧᮔ"), bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡇ࡭ࡸࡳࡩࡴࡵࡄࡰࡪࡸࡴࡴࠩᮕ"),
  bstack11l1l11_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡵࡏ࡭ࡧ࠭ᮖ"),
  bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡗࡥࡵ࠭ᮗ"),
  bstack11l1l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡰ࡬ࡸ࡮ࡧ࡬ࡖࡴ࡯ࠫᮘ"), bstack11l1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡃ࡯ࡰࡴࡽࡐࡰࡲࡸࡴࡸ࠭ᮙ"), bstack11l1l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌ࡫ࡳࡵࡲࡦࡈࡵࡥࡺࡪࡗࡢࡴࡱ࡭ࡳ࡭ࠧᮚ"), bstack11l1l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵ࡫࡮ࡍ࡫ࡱ࡯ࡸࡏ࡮ࡃࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧࠫᮛ"),
  bstack11l1l11_opy_ (u"ࠬࡱࡥࡦࡲࡎࡩࡾࡉࡨࡢ࡫ࡱࡷࠬᮜ"),
  bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࢀࡡࡣ࡮ࡨࡗࡹࡸࡩ࡯ࡩࡶࡈ࡮ࡸࠧᮝ"),
  bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᮞ"),
  bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡸࡪࡸࡋࡦࡻࡇࡩࡱࡧࡹࠨᮟ"),
  bstack11l1l11_opy_ (u"ࠩࡶ࡬ࡴࡽࡉࡐࡕࡏࡳ࡬࠭ᮠ"),
  bstack11l1l11_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡗࡹࡸࡡࡵࡧࡪࡽࠬᮡ"),
  bstack11l1l11_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡖࡪࡹࡰࡰࡰࡶࡩ࡙࡯࡭ࡦࡱࡸࡸࠬᮢ"), bstack11l1l11_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࡙ࡤ࡭ࡹ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᮣ"),
  bstack11l1l11_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࠩᮤ"),
  bstack11l1l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡴࡻࡱࡧࡊࡾࡥࡤࡷࡷࡩࡋࡸ࡯࡮ࡊࡷࡸࡵࡹࠧᮥ"),
  bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡅࡤࡴࡹࡻࡲࡦࠩᮦ"),
  bstack11l1l11_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩᮧ"),
  bstack11l1l11_opy_ (u"ࠪࡪࡺࡲ࡬ࡄࡱࡱࡸࡪࡾࡴࡍ࡫ࡶࡸࠬᮨ"),
  bstack11l1l11_opy_ (u"ࠫࡼࡧࡩࡵࡈࡲࡶࡆࡶࡰࡔࡥࡵ࡭ࡵࡺࠧᮩ"),
  bstack11l1l11_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡉ࡯࡯ࡰࡨࡧࡹࡘࡥࡵࡴ࡬ࡩࡸ᮪࠭"),
  bstack11l1l11_opy_ (u"࠭ࡡࡱࡲࡑࡥࡲ࡫᮫ࠧ"),
  bstack11l1l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡔࡎࡆࡩࡷࡺࠧᮬ"),
  bstack11l1l11_opy_ (u"ࠨࡶࡤࡴ࡜࡯ࡴࡩࡕ࡫ࡳࡷࡺࡐࡳࡧࡶࡷࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭ᮭ"),
  bstack11l1l11_opy_ (u"ࠩࡶࡧࡦࡲࡥࡇࡣࡦࡸࡴࡸࠧᮮ"),
  bstack11l1l11_opy_ (u"ࠪࡻࡩࡧࡌࡰࡥࡤࡰࡕࡵࡲࡵࠩᮯ"),
  bstack11l1l11_opy_ (u"ࠫࡸ࡮࡯ࡸ࡚ࡦࡳࡩ࡫ࡌࡰࡩࠪ᮰"),
  bstack11l1l11_opy_ (u"ࠬ࡯࡯ࡴࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡹࡸ࡫ࠧ᮱"),
  bstack11l1l11_opy_ (u"࠭ࡸࡤࡱࡧࡩࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠨ᮲"),
  bstack11l1l11_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡷࡸࡽ࡯ࡳࡦࠪ᮳"),
  bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡕࡸࡥࡣࡷ࡬ࡰࡹ࡝ࡄࡂࠩ᮴"),
  bstack11l1l11_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶ࡚ࡈࡆࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪ᮵"),
  bstack11l1l11_opy_ (u"ࠪࡻࡪࡨࡄࡳ࡫ࡹࡩࡷࡇࡧࡦࡰࡷ࡙ࡷࡲࠧ᮶"),
  bstack11l1l11_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡵࡪࠪ᮷"),
  bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡐࡨࡻ࡜ࡊࡁࠨ᮸"),
  bstack11l1l11_opy_ (u"࠭ࡷࡥࡣࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩ᮹"), bstack11l1l11_opy_ (u"ࠧࡸࡦࡤࡇࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࡔࡪ࡯ࡨࡳࡺࡺࠧᮺ"),
  bstack11l1l11_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡏࡳࡩࡌࡨࠬᮻ"), bstack11l1l11_opy_ (u"ࠩࡻࡧࡴࡪࡥࡔ࡫ࡪࡲ࡮ࡴࡧࡊࡦࠪᮼ"),
  bstack11l1l11_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧ࡛ࡉࡇࡂࡶࡰࡧࡰࡪࡏࡤࠨᮽ"),
  bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡦࡶࡒࡲࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡳࡶࡒࡲࡱࡿࠧᮾ"),
  bstack11l1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹࡹࠧᮿ"),
  bstack11l1l11_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡩࡦࡵࠪᯀ"), bstack11l1l11_opy_ (u"ࠧࡸࡦࡤࡗࡹࡧࡲࡵࡷࡳࡖࡪࡺࡲࡺࡋࡱࡸࡪࡸࡶࡢ࡮ࠪᯁ"),
  bstack11l1l11_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࡊࡤࡶࡩࡽࡡࡳࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫᯂ"),
  bstack11l1l11_opy_ (u"ࠩࡰࡥࡽ࡚ࡹࡱ࡫ࡱ࡫ࡋࡸࡥࡲࡷࡨࡲࡨࡿࠧᯃ"),
  bstack11l1l11_opy_ (u"ࠪࡷ࡮ࡳࡰ࡭ࡧࡌࡷ࡛࡯ࡳࡪࡤ࡯ࡩࡈ࡮ࡥࡤ࡭ࠪᯄ"),
  bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡄࡣࡵࡸ࡭ࡧࡧࡦࡕࡶࡰࠬᯅ"),
  bstack11l1l11_opy_ (u"ࠬࡹࡨࡰࡷ࡯ࡨ࡚ࡹࡥࡔ࡫ࡱ࡫ࡱ࡫ࡴࡰࡰࡗࡩࡸࡺࡍࡢࡰࡤ࡫ࡪࡸࠧᯆ"),
  bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡎ࡝ࡄࡑࠩᯇ"),
  bstack11l1l11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼ࡚࡯ࡶࡥ࡫ࡍࡩࡋ࡮ࡳࡱ࡯ࡰࠬᯈ"),
  bstack11l1l11_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡉ࡫ࡧࡨࡪࡴࡁࡱ࡫ࡓࡳࡱ࡯ࡣࡺࡇࡵࡶࡴࡸࠧᯉ"),
  bstack11l1l11_opy_ (u"ࠩࡰࡳࡨࡱࡌࡰࡥࡤࡸ࡮ࡵ࡮ࡂࡲࡳࠫᯊ"),
  bstack11l1l11_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉࡳࡷࡳࡡࡵࠩᯋ"), bstack11l1l11_opy_ (u"ࠫࡱࡵࡧࡤࡣࡷࡊ࡮ࡲࡴࡦࡴࡖࡴࡪࡩࡳࠨᯌ"),
  bstack11l1l11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡈࡪࡲࡡࡺࡃࡧࡦࠬᯍ"),
  bstack11l1l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡉࡥࡎࡲࡧࡦࡺ࡯ࡳࡃࡸࡸࡴࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠩᯎ")
]
bstack1ll11l1l1_opy_ = bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡵࡱ࡮ࡲࡥࡩ࠭ᯏ")
bstack111llll1l_opy_ = [bstack11l1l11_opy_ (u"ࠨ࠰ࡤࡴࡰ࠭ᯐ"), bstack11l1l11_opy_ (u"ࠩ࠱ࡥࡦࡨࠧᯑ"), bstack11l1l11_opy_ (u"ࠪ࠲࡮ࡶࡡࠨᯒ")]
bstack111l11l1_opy_ = [bstack11l1l11_opy_ (u"ࠫ࡮ࡪࠧᯓ"), bstack11l1l11_opy_ (u"ࠬࡶࡡࡵࡪࠪᯔ"), bstack11l1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩᯕ"), bstack11l1l11_opy_ (u"ࠧࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩ࠭ᯖ")]
bstack1lll1l11ll_opy_ = {
  bstack11l1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᯗ"): bstack11l1l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᯘ"),
  bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᯙ"): bstack11l1l11_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩᯚ"),
  bstack11l1l11_opy_ (u"ࠬ࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᯛ"): bstack11l1l11_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᯜ"),
  bstack11l1l11_opy_ (u"ࠧࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᯝ"): bstack11l1l11_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᯞ"),
  bstack11l1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡸ࡮ࡵ࡮ࡴࠩᯟ"): bstack11l1l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫᯠ")
}
bstack1l1ll11l11_opy_ = [
  bstack11l1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᯡ"),
  bstack11l1l11_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪᯢ"),
  bstack11l1l11_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᯣ"),
  bstack11l1l11_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᯤ"),
  bstack11l1l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᯥ"),
]
bstack1l1l111l_opy_ = bstack11ll11l1ll_opy_ + bstack111lll11l11_opy_ + bstack1lllllllll_opy_
bstack1ll11lll1l_opy_ = [
  bstack11l1l11_opy_ (u"ࠩࡡࡰࡴࡩࡡ࡭ࡪࡲࡷࡹ᯦ࠪࠧ"),
  bstack11l1l11_opy_ (u"ࠪࡢࡧࡹ࠭࡭ࡱࡦࡥࡱ࠴ࡣࡰ࡯ࠧࠫᯧ"),
  bstack11l1l11_opy_ (u"ࠫࡣ࠷࠲࠸࠰ࠪᯨ"),
  bstack11l1l11_opy_ (u"ࠬࡤ࠱࠱࠰ࠪᯩ"),
  bstack11l1l11_opy_ (u"࠭࡞࠲࠹࠵࠲࠶ࡡ࠶࠮࠻ࡠ࠲ࠬᯪ"),
  bstack11l1l11_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠸࡛࠱࠯࠼ࡡ࠳࠭ᯫ"),
  bstack11l1l11_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠳࡜࠲࠰࠵ࡢ࠴ࠧᯬ"),
  bstack11l1l11_opy_ (u"ࠩࡡ࠵࠾࠸࠮࠲࠸࠻࠲ࠬᯭ")
]
bstack11l111l1l11_opy_ = bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᯮ")
bstack1l1111lll_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡪࡼࡥ࡯ࡶࠪᯯ")
bstack1l11ll11l_opy_ = [ bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᯰ") ]
bstack1l11llllll_opy_ = [ bstack11l1l11_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᯱ") ]
bstack1ll111111l_opy_ = [bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨ᯲ࠫ")]
bstack111l1l1l_opy_ = [ bstack11l1l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᯳") ]
bstack1l1l111l1l_opy_ = bstack11l1l11_opy_ (u"ࠩࡖࡈࡐ࡙ࡥࡵࡷࡳࠫ᯴")
bstack11l1l1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡅࡹࡺࡥ࡮ࡲࡷࡩࡩ࠭᯵")
bstack1l1lll1lll_opy_ = bstack11l1l11_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠨ᯶")
bstack1lll11ll1l_opy_ = bstack11l1l11_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࠫ᯷")
bstack11l11lll11_opy_ = [
  bstack11l1l11_opy_ (u"࠭ࡅࡓࡔࡢࡊࡆࡏࡌࡆࡆࠪ᯸"),
  bstack11l1l11_opy_ (u"ࠧࡆࡔࡕࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧ᯹"),
  bstack11l1l11_opy_ (u"ࠨࡇࡕࡖࡤࡈࡌࡐࡅࡎࡉࡉࡥࡂ࡚ࡡࡆࡐࡎࡋࡎࡕࠩ᯺"),
  bstack11l1l11_opy_ (u"ࠩࡈࡖࡗࡥࡎࡆࡖ࡚ࡓࡗࡑ࡟ࡄࡊࡄࡒࡌࡋࡄࠨ᯻"),
  bstack11l1l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡊ࡚࡟ࡏࡑࡗࡣࡈࡕࡎࡏࡇࡆࡘࡊࡊࠧ᯼"),
  bstack11l1l11_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡉࡌࡐࡕࡈࡈࠬ᯽"),
  bstack11l1l11_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡕࡈࡘࠬ᯾"),
  bstack11l1l11_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡓࡇࡉ࡙ࡘࡋࡄࠨ᯿"),
  bstack11l1l11_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡃࡅࡓࡗ࡚ࡅࡅࠩᰀ"),
  bstack11l1l11_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᰁ"),
  bstack11l1l11_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪᰂ"),
  bstack11l1l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡋࡑ࡚ࡆࡒࡉࡅࠩᰃ"),
  bstack11l1l11_opy_ (u"ࠫࡊࡘࡒࡠࡃࡇࡈࡗࡋࡓࡔࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧᰄ"),
  bstack11l1l11_opy_ (u"ࠬࡋࡒࡓࡡࡗ࡙ࡓࡔࡅࡍࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᰅ"),
  bstack11l1l11_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪᰆ"),
  bstack11l1l11_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᰇ"),
  bstack11l1l11_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡖࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡊࡒࡗ࡙ࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫᰈ"),
  bstack11l1l11_opy_ (u"ࠩࡈࡖࡗࡥࡐࡓࡑ࡛࡝ࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᰉ"),
  bstack11l1l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡔࡏࡕࡡࡕࡉࡘࡕࡌࡗࡇࡇࠫᰊ"),
  bstack11l1l11_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡒࡆࡕࡒࡐ࡚࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᰋ"),
  bstack11l1l11_opy_ (u"ࠬࡋࡒࡓࡡࡐࡅࡓࡊࡁࡕࡑࡕ࡝ࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫᰌ"),
]
bstack1ll1ll111l_opy_ = bstack11l1l11_opy_ (u"࠭࠮࠰ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡢࡴࡷ࡭࡫ࡧࡣࡵࡵ࠲ࠫᰍ")
bstack1l11ll1ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠧࡿࠩᰎ")), bstack11l1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᰏ"), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᰐ"))
bstack11l11l1l11l_opy_ = bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲ࡬ࠫᰑ")
bstack111llll1111_opy_ = [ bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᰒ"), bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᰓ"), bstack11l1l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬᰔ"), bstack11l1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᰕ")]
bstack11ll1l1lll_opy_ = [ bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᰖ"), bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᰗ"), bstack11l1l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩᰘ"), bstack11l1l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫᰙ") ]
bstack11l111111_opy_ = [ bstack11l1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᰚ") ]
bstack111ll1ll1l1_opy_ = [ bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᰛ") ]
bstack11l11l1l11_opy_ = 360
bstack11l1111lll1_opy_ = bstack11l1l11_opy_ (u"ࠢࡢࡲࡳ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᰜ")
bstack111ll1l1lll_opy_ = bstack11l1l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵࠥᰝ")
bstack111llll1l11_opy_ = bstack11l1l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠧᰞ")
bstack11l11l1l111_opy_ = bstack11l1l11_opy_ (u"ࠥࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡹ࡫ࡳࡵࡵࠣࡥࡷ࡫ࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡏࡔࠢࡹࡩࡷࡹࡩࡰࡰࠣࠩࡸࠦࡡ࡯ࡦࠣࡥࡧࡵࡶࡦࠢࡩࡳࡷࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠࡥࡧࡹ࡭ࡨ࡫ࡳ࠯ࠤᰟ")
bstack11l11ll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠦ࠶࠷࠮࠱ࠤᰠ")
bstack1lllllll11l_opy_ = {
  bstack11l1l11_opy_ (u"ࠬࡖࡁࡔࡕࠪᰡ"): bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᰢ"),
  bstack11l1l11_opy_ (u"ࠧࡇࡃࡌࡐࠬᰣ"): bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᰤ"),
  bstack11l1l11_opy_ (u"ࠩࡖࡏࡎࡖࠧᰥ"): bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᰦ")
}
bstack1ll1111111_opy_ = [
  bstack11l1l11_opy_ (u"ࠦ࡬࡫ࡴࠣᰧ"),
  bstack11l1l11_opy_ (u"ࠧ࡭࡯ࡃࡣࡦ࡯ࠧᰨ"),
  bstack11l1l11_opy_ (u"ࠨࡧࡰࡈࡲࡶࡼࡧࡲࡥࠤᰩ"),
  bstack11l1l11_opy_ (u"ࠢࡳࡧࡩࡶࡪࡹࡨࠣᰪ"),
  bstack11l1l11_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢᰫ"),
  bstack11l1l11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᰬ"),
  bstack11l1l11_opy_ (u"ࠥࡷࡺࡨ࡭ࡪࡶࡈࡰࡪࡳࡥ࡯ࡶࠥᰭ"),
  bstack11l1l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣᰮ"),
  bstack11l1l11_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣᰯ"),
  bstack11l1l11_opy_ (u"ࠨࡣ࡭ࡧࡤࡶࡊࡲࡥ࡮ࡧࡱࡸࠧᰰ"),
  bstack11l1l11_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࡳࠣᰱ"),
  bstack11l1l11_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴࠣᰲ"),
  bstack11l1l11_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࡄࡷࡾࡴࡣࡔࡥࡵ࡭ࡵࡺࠢᰳ"),
  bstack11l1l11_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤᰴ"),
  bstack11l1l11_opy_ (u"ࠦࡶࡻࡩࡵࠤᰵ"),
  bstack11l1l11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲ࡚࡯ࡶࡥ࡫ࡅࡨࡺࡩࡰࡰࠥᰶ"),
  bstack11l1l11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳࡍࡶ࡮ࡷ࡭࡙ࡵࡵࡤࡪ᰷ࠥ"),
  bstack11l1l11_opy_ (u"ࠢࡴࡪࡤ࡯ࡪࠨ᰸"),
  bstack11l1l11_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࡁࡱࡲࠥ᰹")
]
bstack111lll111ll_opy_ = [
  bstack11l1l11_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࠣ᰺"),
  bstack11l1l11_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢ᰻"),
  bstack11l1l11_opy_ (u"ࠦࡦࡻࡴࡰࠤ᰼"),
  bstack11l1l11_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧ᰽"),
  bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ᰾")
]
bstack1l1l1l11ll_opy_ = {
  bstack11l1l11_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨ᰿"): [bstack11l1l11_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢ᱀")],
  bstack11l1l11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ᱁"): [bstack11l1l11_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢ᱂")],
  bstack11l1l11_opy_ (u"ࠦࡦࡻࡴࡰࠤ᱃"): [bstack11l1l11_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡇ࡯ࡩࡲ࡫࡮ࡵࠤ᱄"), bstack11l1l11_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡄࡧࡹ࡯ࡶࡦࡇ࡯ࡩࡲ࡫࡮ࡵࠤ᱅"), bstack11l1l11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᱆"), bstack11l1l11_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢ᱇")],
  bstack11l1l11_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤ᱈"): [bstack11l1l11_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥ᱉")],
  bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᱊"): [bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ᱋")],
}
bstack111lll11lll_opy_ = {
  bstack11l1l11_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ᱌"): bstack11l1l11_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨᱍ"),
  bstack11l1l11_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᱎ"): bstack11l1l11_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᱏ"),
  bstack11l1l11_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢ᱐"): bstack11l1l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨ᱑"),
  bstack11l1l11_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣ᱒"): bstack11l1l11_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࠣ᱓"),
  bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ᱔"): bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ᱕")
}
bstack11111l1l11_opy_ = {
  bstack11l1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭᱖"): bstack11l1l11_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡖࡩࡹࡻࡰࠨ᱗"),
  bstack11l1l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ᱘"): bstack11l1l11_opy_ (u"࡙ࠬࡵࡪࡶࡨࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭᱙"),
  bstack11l1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᱚ"): bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸ࡙ࠥࡥࡵࡷࡳࠫᱛ"),
  bstack11l1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᱜ"): bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩᱝ")
}
bstack111ll1ll11l_opy_ = 65536
bstack111ll1lll1l_opy_ = bstack11l1l11_opy_ (u"ࠪ࠲࠳࠴࡛ࡕࡔࡘࡒࡈࡇࡔࡆࡆࡠࠫᱞ")
bstack111llll1l1l_opy_ = [
      bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᱟ"), bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᱠ"), bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᱡ"), bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᱢ"), bstack11l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᱣ"),
      bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᱤ"), bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᱥ"), bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᱦ"), bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᱧ"),
      bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᱨ"), bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᱩ"), bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫᱪ")
    ]
bstack111lll11l1l_opy_= {
  bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᱫ"): bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᱬ"),
  bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᱭ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᱮ"),
  bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᱯ"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᱰ"),
  bstack11l1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᱱ"): bstack11l1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᱲ"),
  bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᱳ"): bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᱴ"),
  bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᱵ"): bstack11l1l11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᱶ"),
  bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᱷ"): bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᱸ"),
  bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᱹ"): bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᱺ"),
  bstack11l1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᱻ"): bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᱼ"),
  bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᱽ"): bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ᱾"),
  bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᱿"): bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᲀ"),
  bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪᲁ"): bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫᲂ"),
  bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲃ"): bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᲄ"),
  bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࠧᲅ"): bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࡐࡲࡷ࡭ࡴࡴࡳࠨᲆ"),
  bstack11l1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᲇ"): bstack11l1l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬᲈ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᲉ"): bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᲊ"),
  bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᲋"): bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᲌"),
  bstack11l1l11_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ᲍"): bstack11l1l11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭᲎"),
  bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ᲏"): bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᲐ"),
  bstack11l1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᲑ"): bstack11l1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᲒ"),
  bstack11l1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᲓ"): bstack11l1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᲔ"),
  bstack11l1l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᲕ"): bstack11l1l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᲖ"),
  bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᲗ"): bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᲘ"),
  bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Კ"): bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᲚ"),
  bstack11l1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᲛ"): bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Ნ"),
  bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᲝ"): bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᲞ"),
  bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲟ"): bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᲠ"),
  bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᲡ"): bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᲢ")
}
bstack111lllll1ll_opy_ = [bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᲣ"), bstack11l1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᲤ")]
bstack111l1111_opy_ = (bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᲥ"),)
bstack111llll11l1_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠱ࡹ࠵࠴ࡻࡰࡥࡣࡷࡩࡤࡩ࡬ࡪࠩᲦ")
bstack1ll11lllll_opy_ = bstack11l1l11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠯ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠵ࡶ࠲࠱ࡪࡶ࡮ࡪࡳ࠰ࠤᲧ")
bstack1l11l11l1l_opy_ = bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩࡵ࡭ࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࠨᲨ")
bstack1ll1111l11_opy_ = bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠤᲩ")
class EVENTS(Enum):
  bstack111llll111l_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭Ც")
  bstack1ll1l1l111_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮ࡨࡥࡳࡻࡰࠨᲫ")
  bstack1111llllll_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡨ࡬ࡲࡦࡲࡩࡻࡧࠪᲬ")
  bstack111lll1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࡬ࡰࡩࡶࠫᲭ")
  bstack11lll1l11_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩᲮ") #shift post bstack111lll1l11l_opy_
  bstack111llll11_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨᲯ") #shift post bstack111lll1l11l_opy_
  bstack111lll1llll_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶ࡫ࡹࡧ࠭Ჰ") #shift
  bstack111lll1111l_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧᲱ") #shift
  bstack111ll1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠾࡭ࡻࡢ࠮࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠬᲲ")
  bstack1l1l1llllll_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡳࡢࡸࡨ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷࠬᲳ")
  bstack1l11llll_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡱࡧࡵࡪࡴࡸ࡭ࡴࡥࡤࡲࠬᲴ")
  bstack1l1llll1l1_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡲ࡯ࡤࡣ࡯ࠫᲵ") #shift
  bstack1ll11111l_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡥࡵࡶ࠭ࡶࡲ࡯ࡳࡦࡪࠧᲶ") #shift
  bstack1llll1l1l_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡤ࡫࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠭Ჷ")
  bstack11l11l11l1_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪᲸ") #shift
  bstack1l11ll11_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵࠪᲹ") #shift
  bstack111ll1ll111_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿࠧᲺ") #shift
  bstack1l111l1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ᲻")
  bstack1111l1l11_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡳࡵࡣࡷࡹࡸ࠭᲼") #shift
  bstack1ll1lllll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡨࡶࡤ࠰ࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠧᲽ")
  bstack111lll1l1l1_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡰࡺࡼ࠱ࡸ࡫ࡴࡶࡲࠪᲾ") #shift
  bstack1ll111l1l1_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡶࡸࡴࠬᲿ")
  bstack111lll1ll11_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡳ࡯ࡣࡳࡷ࡭ࡵࡴࠨ᳀") # not bstack111llll1lll_opy_ in python
  bstack1l1llllll_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡳࡸ࡭ࡹ࠭᳁") # used in bstack111ll1lll11_opy_
  bstack11l1ll1l111_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡶࡪ࠳ࡱࡶ࡫ࡷࠫ᳂")
  bstack11l1ll1l1l1_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮ࡳࡸ࡭ࡹ࠭᳃")
  bstack1l1ll1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾࡬࡫ࡴࠨ᳄") # used in bstack111ll1lll11_opy_
  bstack11l1l11l1l_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿࡮࡯ࡰ࡭ࠪ᳅")
  bstack11l1lll1lll_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡰࡳࡧ࠰࡬ࡴࡵ࡫ࠨ᳆")
  bstack11l1lll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡱࡶࡸ࠲࡮࡯ࡰ࡭ࠪ᳇")
  bstack1ll11l1lll_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠩ᳈")
  bstack1l1ll1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠩ᳉") #
  bstack1lll11llll_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡦࡵ࡭ࡻ࡫ࡲ࠮ࡶࡤ࡯ࡪ࡙ࡣࡳࡧࡨࡲࡘ࡮࡯ࡵࠩ᳊")
  bstack111lll1111_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡥࡺࡺ࡯࠮ࡥࡤࡴࡹࡻࡲࡦࠩ᳋")
  bstack11111lll1_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡦ࠯ࡷࡩࡸࡺࠧ᳌")
  bstack111lll11l_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡰࡰࡵࡷ࠱ࡹ࡫ࡳࡵࠩ᳍")
  bstack11llllllll_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡴࡨ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬ᳎") #shift
  bstack11llll1l1_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧ᳏") #shift
  bstack111lllll1l1_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࠭ࡤࡣࡳࡸࡺࡸࡥࠨ᳐")
  bstack111lll1l111_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿࡯ࡤ࡭ࡧ࠰ࡸ࡮ࡳࡥࡰࡷࡷࠫ᳑")
  bstack111l1lll1l_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡪࡾࡩࡵ࠯࡫ࡥࡳࡪ࡬ࡦࡴࠪ᳒")
  bstack1ll1l1ll11l_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡨࡼ࡮ࡺ࠭ࡩࡣࡱࡨࡱ࡫ࡲࠨ᳓")
  bstack111lllll111_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡰࡧ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ᳔ࠬ")
  bstack111lll1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸ࡭ࡻࡢ࠻ࡵࡷࡳࡵ᳕࠭")
  bstack1ll11lll1l1_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡹࡴࡢࡴࡷ᳖ࠫ")
  bstack111lll11111_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡰࡹࡱࡰࡴࡧࡤࠨ᳗")
  bstack111lll1lll1_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡤࡪࡨࡧࡰ࠳ࡵࡱࡦࡤࡸࡪ᳘࠭")
  bstack1ll1ll11ll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡧࡵ࡯ࡵࡵࡷࡶࡦࡶ᳙ࠧ")
  bstack1ll11111lll_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡹࡴࡢࡴࡷࡦ࡮ࡴࡡࡳࡻࠪ᳚")
  bstack1ll1l1l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡳࡳ࠳ࡣࡰࡰࡱࡩࡨࡺࠧ᳛")
  bstack1l1lll1llll_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡴࡶࡲࡴ᳜ࠬ")
  bstack1ll111llll1_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡷࡥࡷࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ᳝ࠪ")
  bstack1ll111ll1l1_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡳࡳࡴࡥࡤࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ᳞࠭")
  bstack111ll1l1ll1_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺ᳟ࠧ")
  bstack111lll11ll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡥࡐࡨࡥࡷ࡫ࡳࡵࡊࡸࡦࠬ᳠")
  bstack11lllll11l1_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡍࡳ࡯ࡴࠨ᳡")
  bstack11lllll1l1l_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡳࡶ᳢ࠪ")
  bstack1l1l1l1llll_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡃࡰࡰࡩ࡭࡬᳣࠭")
  bstack111lllll11l_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡄࡱࡱࡪ࡮࡭᳤ࠧ")
  bstack1l1l11l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࡭ࡘ࡫࡬ࡧࡊࡨࡥࡱ࡙ࡴࡦࡲ᳥ࠪ")
  bstack1l1l11l1111_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࡮࡙ࡥ࡭ࡨࡋࡩࡦࡲࡇࡦࡶࡕࡩࡸࡻ࡬ࡵ᳦ࠩ")
  bstack1l11ll1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡉࡻ࡫࡮ࡵ᳧ࠩ")
  bstack1l11ll111ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠨ᳨")
  bstack1l11l11l1ll_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡰࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࡅࡷࡧࡱࡸࠬᳩ")
  bstack111llll11ll_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡪࡴࡱࡶࡧࡸࡩ࡙࡫ࡳࡵࡇࡹࡩࡳࡺࠧᳪ")
  bstack11llll1111l_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡱࡳࠫᳫ")
  bstack1ll1l1lll1l_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡲࡲࡘࡺ࡯ࡱࠩᳬ")
  bstack11l1l11ll1l_opy_ = bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳ࡙ࡵࡲ࡯ࡢࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ᳭ࠧ")
  bstack1llll11l1_opy_ = bstack11l1l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫࡮ࡥࡈࡸࡲࡳ࡫࡬ࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠧᳮ")
  bstack111ll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦࡉࡹࡳࡴࡥ࡭ࡖࡨࡷࡹࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠨᳯ")
  bstack1llll1l11ll_opy_ = bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡱࡲ࡯ࡽࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡔࡾࡺࡥࡴࡶࠪᳰ")
  bstack1llll11111l_opy_ = bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡷࡕࡿࡴࡦࡵࡷࠫᳱ")
  bstack1lll1llllll_opy_ = bstack11l1l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡼࡸࡪࡹࡴࡈࡧࡷࡘࡴࡺࡡ࡭ࡖࡨࡷࡹࡹࠧᳲ")
class STAGE(Enum):
  bstack11111l11l_opy_ = bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫᳳ")
  END = bstack11l1l11_opy_ (u"࠭ࡥ࡯ࡦࠪ᳴")
  bstack1l11l1l11l_opy_ = bstack11l1l11_opy_ (u"ࠧࡴ࡫ࡱ࡫ࡱ࡫ࠧᳵ")
bstack1l1l1l1l_opy_ = {
  bstack11l1l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࠨᳶ"): bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᳷"),
  bstack11l1l11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ᳸"): bstack11l1l11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭᳹")
}
PLAYWRIGHT_HUB_URL = bstack11l1l11_opy_ (u"ࠧࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠢᳺ")
bstack1l1ll11l111_opy_ = 98
bstack1l1ll1l1l1l_opy_ = 100
bstack1llll1lll1l_opy_ = {
  bstack11l1l11_opy_ (u"࠭ࡲࡦࡴࡸࡲࠬ᳻"): bstack11l1l11_opy_ (u"ࠧ࠮࠯ࡵࡩࡷࡻ࡮ࡴࠩ᳼"),
  bstack11l1l11_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧ᳽"): bstack11l1l11_opy_ (u"ࠩ࠰࠱ࡷ࡫ࡲࡶࡰࡶ࠱ࡩ࡫࡬ࡢࡻࠪ᳾"),
  bstack11l1l11_opy_ (u"ࠪࡶࡪࡸࡵ࡯࠯ࡧࡩࡱࡧࡹࠨ᳿"): 0
}
bstack111ll1lllll_opy_ = bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦᴀ")
bstack111ll1l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡵࡱ࡮ࡲࡥࡩ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᴁ")
bstack1l1l1l11l1_opy_ = bstack11l1l11_opy_ (u"ࠨࡔࡆࡕࡗࠤࡗࡋࡐࡐࡔࡗࡍࡓࡍࠠࡂࡐࡇࠤࡆࡔࡁࡍ࡛ࡗࡍࡈ࡙ࠢᴂ")