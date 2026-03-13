# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import re
from enum import Enum
bstack1l1l11111l_opy_ = {
  bstack1111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᮃ"): bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷ࠭ᮄ"),
  bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᮅ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡯ࡪࡿࠧᮆ"),
  bstack1111l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᮇ"): bstack1111l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᮈ"),
  bstack1111l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᮉ"): bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᮊ"),
  bstack1111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᮋ"): bstack1111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࠫᮌ"),
  bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᮍ"): bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫᮎ"),
  bstack1111l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᮏ"): bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᮐ"),
  bstack1111l_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᮑ"): bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭ࠧᮒ"),
  bstack1111l_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨᮓ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡳࡰ࡮ࡨࠫᮔ"),
  bstack1111l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪᮕ"): bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪᮖ"),
  bstack1111l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫᮗ"): bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫᮘ"),
  bstack1111l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨᮙ"): bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡹ࡭ࡩ࡫࡯ࠨᮚ"),
  bstack1111l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪᮛ"): bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪᮜ"),
  bstack1111l_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ᮝ"): bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ᮞ"),
  bstack1111l_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᮟ"): bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᮠ"),
  bstack1111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬᮡ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸ࡮ࡳࡥࡻࡱࡱࡩࠬᮢ"),
  bstack1111l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᮣ"): bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᮤ"),
  bstack1111l_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭ᮥ"): bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭ᮦ"),
  bstack1111l_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧᮧ"): bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧᮨ"),
  bstack1111l_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫᮩ"): bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫᮪ࠫ"),
  bstack1111l_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨ᮫"): bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦࡰࡧࡏࡪࡿࡳࠨᮬ"),
  bstack1111l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪᮭ"): bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴ࡝ࡡࡪࡶࠪᮮ"),
  bstack1111l_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩᮯ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡴࠩ᮰"),
  bstack1111l_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭᮱"): bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡦࡤࡣࡦ࡬ࡪ࠭᮲"),
  bstack1111l_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ᮳"): bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ᮴"),
  bstack1111l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬ᮵"): bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬ᮶"),
  bstack1111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ᮷"): bstack1111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ᮸"),
  bstack1111l_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪ᮹"): bstack1111l_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬᮺ"),
  bstack1111l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᮻ"): bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᮼ"),
  bstack1111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪᮽ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪᮾ"),
  bstack1111l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ᮿ"): bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ᯀ"),
  bstack1111l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ᯁ"): bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࡴࠩᯂ"),
  bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᯃ"): bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᯄ"),
  bstack1111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᯅ"): bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸࡵࡵࡳࡥࡨࠫᯆ"),
  bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᯇ"): bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᯈ"),
  bstack1111l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪᯉ"): bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡪࡲࡷࡹࡔࡡ࡮ࡧࠪᯊ"),
  bstack1111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ᯋ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ᯌ"),
  bstack1111l_opy_ (u"ࠬࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᯍ"): bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᯎ"),
  bstack1111l_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬᯏ"): bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬᯐ"),
  bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᯑ"): bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᯒ"),
  bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᯓ"): bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᯔ")
}
bstack111l1lll111_opy_ = [
  bstack1111l_opy_ (u"࠭࡯ࡴࠩᯕ"),
  bstack1111l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᯖ"),
  bstack1111l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᯗ"),
  bstack1111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᯘ"),
  bstack1111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᯙ"),
  bstack1111l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᯚ"),
  bstack1111l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᯛ"),
]
bstack1l11l11lll_opy_ = {
  bstack1111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᯜ"): [bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨᯝ"), bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡔࡁࡎࡇࠪᯞ")],
  bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᯟ"): bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᯠ"),
  bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᯡ"): bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨᯢ"),
  bstack1111l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᯣ"): bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠬᯤ"),
  bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᯥ"): bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ᯦ࠫ"),
  bstack1111l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᯧ"): bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡘࡥࡐࡆࡔࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬᯨ"),
  bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᯩ"): bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫᯪ"),
  bstack1111l_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫᯫ"): bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬᯬ"),
  bstack1111l_opy_ (u"ࠩࡤࡴࡵ࠭ᯭ"): [bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕࡥࡉࡅࠩᯮ"), bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧᯯ")],
  bstack1111l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᯰ"): bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡙ࡄࡌࡡࡏࡓࡌࡒࡅࡗࡇࡏࠫᯱ"),
  bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ᯲ࠫ"): bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑ᯳ࠫ"),
  bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᯴"): [bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡐࡄࡖࡉࡗ࡜ࡁࡃࡋࡏࡍ࡙࡟ࠧ᯵"), bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫ᯶")],
  bstack1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᯷"): bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡕࡓࡄࡒࡗࡈࡇࡌࡆࠩ᯸"),
  bstack1111l_opy_ (u"ࠧࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࡇࡑ࡚ࠬ᯹"): bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡐࡔࡆࡌࡊ࡙ࡔࡓࡃࡗࡍࡔࡔ࡟ࡔࡏࡄࡖ࡙ࡥࡓࡆࡎࡈࡇ࡙ࡏࡏࡏࡡࡉࡉࡆ࡚ࡕࡓࡇࡢࡆࡗࡇࡎࡄࡊࡈࡗࠬ᯺")
}
bstack11l1l11111_opy_ = {
  bstack1111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ᯻"): [bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬ᯼"), bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᯽")],
  bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᯾"): [bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ᯿"), bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᰀ")],
  bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᰁ"): bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᰂ"),
  bstack1111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᰃ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᰄ"),
  bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᰅ"): bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᰆ"),
  bstack1111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᰇ"): [bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫᰈ"), bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᰉ")],
  bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᰊ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᰋ"),
  bstack1111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᰌ"): bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᰍ"),
  bstack1111l_opy_ (u"ࠧࡢࡲࡳࠫᰎ"): bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫᰏ"),
  bstack1111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᰐ"): bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᰑ"),
  bstack1111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᰒ"): bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᰓ"),
  bstack1111l_opy_ (u"ࠨࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࡄࡎࡌࠦᰔ"): bstack1111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࠧᰕ"),
}
bstack11lll1l1l_opy_ = {
  bstack1111l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᰖ"): bstack1111l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᰗ"),
  bstack1111l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᰘ"): [bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᰙ"), bstack1111l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᰚ")],
  bstack1111l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᰛ"): bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᰜ"),
  bstack1111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᰝ"): bstack1111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᰞ"),
  bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᰟ"): [bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᰠ"), bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᰡ")],
  bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᰢ"): bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᰣ"),
  bstack1111l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᰤ"): bstack1111l_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧᰥ"),
  bstack1111l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᰦ"): [bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᰧ"), bstack1111l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᰨ")],
  bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᰩ"): [bstack1111l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨᰪ"), bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࠨᰫ")]
}
bstack1111l1ll1l_opy_ = [
  bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨᰬ"),
  bstack1111l_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ᰭ"),
  bstack1111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪᰮ"),
  bstack1111l_opy_ (u"ࠬࡹࡥࡵ࡙࡬ࡲࡩࡵࡷࡓࡧࡦࡸࠬᰯ"),
  bstack1111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࡳࠨᰰ"),
  bstack1111l_opy_ (u"ࠧࡴࡶࡵ࡭ࡨࡺࡆࡪ࡮ࡨࡍࡳࡺࡥࡳࡣࡦࡸࡦࡨࡩ࡭࡫ࡷࡽࠬᰱ"),
  bstack1111l_opy_ (u"ࠨࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡔࡷࡵ࡭ࡱࡶࡅࡩ࡭ࡧࡶࡪࡱࡵࠫᰲ"),
  bstack1111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᰳ"),
  bstack1111l_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᰴ"),
  bstack1111l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬᰵ"),
  bstack1111l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫᰶ"),
  bstack1111l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹ᰷ࠧ"),
]
bstack11l11l1l11_opy_ = [
  bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᰸"),
  bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ᰹"),
  bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ᰺"),
  bstack1111l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᰻"),
  bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᰼"),
  bstack1111l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ᰽"),
  bstack1111l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᰾"),
  bstack1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᰿"),
  bstack1111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ᱀"),
  bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ᱁"),
  bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᱂"),
  bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫ᱃"),
  bstack1111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧ᱄"),
  bstack1111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡚ࡡࡨࠩ᱅"),
  bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᱆"),
  bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᱇"),
  bstack1111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭᱈"),
  bstack1111l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠲ࠩ᱉"),
  bstack1111l_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠴ࠪ᱊"),
  bstack1111l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠶ࠫ᱋"),
  bstack1111l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠸ࠬ᱌"),
  bstack1111l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠺࠭ᱍ"),
  bstack1111l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠼ࠧᱎ"),
  bstack1111l_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠷ࠨᱏ"),
  bstack1111l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠹ࠩ᱐"),
  bstack1111l_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠻ࠪ᱑"),
  bstack1111l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᱒"),
  bstack1111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬ᱓"),
  bstack1111l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪ᱔"),
  bstack1111l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ᱕"),
  bstack1111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭᱖"),
  bstack1111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᱗"),
  bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨ᱘"),
  bstack1111l_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨ᱙")
]
bstack111ll1111l1_opy_ = [
  bstack1111l_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫᱚ"),
  bstack1111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᱛ"),
  bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᱜ"),
  bstack1111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᱝ"),
  bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡑࡴ࡬ࡳࡷ࡯ࡴࡺࠩᱞ"),
  bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᱟ"),
  bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡦ࡭ࠧᱠ"),
  bstack1111l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᱡ"),
  bstack1111l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᱢ"),
  bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᱣ"),
  bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᱤ"),
  bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᱥ"),
  bstack1111l_opy_ (u"ࠫࡴࡹࠧᱦ"),
  bstack1111l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᱧ"),
  bstack1111l_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬᱨ"),
  bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩᱩ"),
  bstack1111l_opy_ (u"ࠨࡴࡨ࡫࡮ࡵ࡮ࠨᱪ"),
  bstack1111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫᱫ"),
  bstack1111l_opy_ (u"ࠪࡱࡦࡩࡨࡪࡰࡨࠫᱬ"),
  bstack1111l_opy_ (u"ࠫࡷ࡫ࡳࡰ࡮ࡸࡸ࡮ࡵ࡮ࠨᱭ"),
  bstack1111l_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᱮ"),
  bstack1111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡕࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪᱯ"),
  bstack1111l_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࠭ᱰ"),
  bstack1111l_opy_ (u"ࠨࡰࡲࡔࡦ࡭ࡥࡍࡱࡤࡨ࡙࡯࡭ࡦࡱࡸࡸࠬᱱ"),
  bstack1111l_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪᱲ"),
  bstack1111l_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᱳ"),
  bstack1111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᱴ"),
  bstack1111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭ᱵ"),
  bstack1111l_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪᱶ"),
  bstack1111l_opy_ (u"ࠧ࡯ࡱࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠫᱷ"),
  bstack1111l_opy_ (u"ࠨࡥ࡫ࡩࡨࡱࡕࡓࡎࠪᱸ"),
  bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᱹ"),
  bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡆࡳࡴࡱࡩࡦࡵࠪᱺ"),
  bstack1111l_opy_ (u"ࠫࡨࡧࡰࡵࡷࡵࡩࡈࡸࡡࡴࡪࠪᱻ"),
  bstack1111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᱼ"),
  bstack1111l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᱽ"),
  bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࡚ࡪࡸࡳࡪࡱࡱࠫ᱾"),
  bstack1111l_opy_ (u"ࠨࡰࡲࡆࡱࡧ࡮࡬ࡒࡲࡰࡱ࡯࡮ࡨࠩ᱿"),
  bstack1111l_opy_ (u"ࠩࡰࡥࡸࡱࡓࡦࡰࡧࡏࡪࡿࡳࠨᲀ"),
  bstack1111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡏࡳ࡬ࡹࠧᲁ"),
  bstack1111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡍࡩ࠭ᲂ"),
  bstack1111l_opy_ (u"ࠬࡪࡥࡥ࡫ࡦࡥࡹ࡫ࡤࡅࡧࡹ࡭ࡨ࡫ࠧᲃ"),
  bstack1111l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡖࡡࡳࡣࡰࡷࠬᲄ"),
  bstack1111l_opy_ (u"ࠧࡱࡪࡲࡲࡪࡔࡵ࡮ࡤࡨࡶࠬᲅ"),
  bstack1111l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ᲆ"),
  bstack1111l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡏࡱࡶ࡬ࡳࡳࡹࠧᲇ"),
  bstack1111l_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨᲈ"),
  bstack1111l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᲉ"),
  bstack1111l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩᲊ"),
  bstack1111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡈࡩࡰ࡯ࡨࡸࡷ࡯ࡣࠨ᲋"),
  bstack1111l_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࡜࠲ࠨ᲌"),
  bstack1111l_opy_ (u"ࠨ࡯࡬ࡨࡘ࡫ࡳࡴ࡫ࡲࡲࡎࡴࡳࡵࡣ࡯ࡰࡆࡶࡰࡴࠩ᲍"),
  bstack1111l_opy_ (u"ࠩࡨࡷࡵࡸࡥࡴࡵࡲࡗࡪࡸࡶࡦࡴࠪ᲎"),
  bstack1111l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩ᲏"),
  bstack1111l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡉࡤࡱࠩᲐ"),
  bstack1111l_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬᲑ"),
  bstack1111l_opy_ (u"࠭ࡳࡺࡰࡦࡘ࡮ࡳࡥࡘ࡫ࡷ࡬ࡓ࡚ࡐࠨᲒ"),
  bstack1111l_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬᲓ"),
  bstack1111l_opy_ (u"ࠨࡩࡳࡷࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭Ე"),
  bstack1111l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᲕ"),
  bstack1111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪᲖ"),
  bstack1111l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࡆ࡬ࡦࡴࡧࡦࡌࡤࡶࠬᲗ"),
  bstack1111l_opy_ (u"ࠬࡾ࡭ࡴࡌࡤࡶࠬᲘ"),
  bstack1111l_opy_ (u"࠭ࡸ࡮ࡺࡍࡥࡷ࠭Კ"),
  bstack1111l_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭Ლ"),
  bstack1111l_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᲛ"),
  bstack1111l_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪᲜ"),
  bstack1111l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭Ო"),
  bstack1111l_opy_ (u"ࠫࡦࡶࡰࡗࡧࡵࡷ࡮ࡵ࡮ࠨᲞ"),
  bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᲟ"),
  bstack1111l_opy_ (u"࠭ࡲࡦࡵ࡬࡫ࡳࡇࡰࡱࠩᲠ"),
  bstack1111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡰ࡬ࡱࡦࡺࡩࡰࡰࡶࠫᲡ"),
  bstack1111l_opy_ (u"ࠨࡥࡤࡲࡦࡸࡹࠨᲢ"),
  bstack1111l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᲣ"),
  bstack1111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᲤ"),
  bstack1111l_opy_ (u"ࠫ࡮࡫ࠧᲥ"),
  bstack1111l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪᲦ"),
  bstack1111l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭Ყ"),
  bstack1111l_opy_ (u"ࠧࡲࡷࡨࡹࡪ࠭Შ"),
  bstack1111l_opy_ (u"ࠨ࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪᲩ"),
  bstack1111l_opy_ (u"ࠩࡤࡴࡵ࡙ࡴࡰࡴࡨࡇࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠪᲪ"),
  bstack1111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡆࡥࡲ࡫ࡲࡢࡋࡰࡥ࡬࡫ࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩᲫ"),
  bstack1111l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡇࡻࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧᲬ"),
  bstack1111l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡌࡲࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨᲭ"),
  bstack1111l_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࠪᲮ"),
  bstack1111l_opy_ (u"ࠧࡳࡧࡶࡩࡷࡼࡥࡅࡧࡹ࡭ࡨ࡫ࠧᲯ"),
  bstack1111l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᲰ"),
  bstack1111l_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫᲱ"),
  bstack1111l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡥࡸࡹࡣࡰࡦࡨࠫᲲ"),
  bstack1111l_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡍࡴࡹࡄࡦࡸ࡬ࡧࡪ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᲳ"),
  bstack1111l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡻࡤࡪࡱࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬᲴ"),
  bstack1111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡰࡱ࡮ࡨࡔࡦࡿࠧᲵ"),
  bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᲶ"),
  bstack1111l_opy_ (u"ࠨࡹࡧ࡭ࡴ࡙ࡥࡳࡸ࡬ࡧࡪ࠭Ჷ"),
  bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᲸ"),
  bstack1111l_opy_ (u"ࠪࡴࡷ࡫ࡶࡦࡰࡷࡇࡷࡵࡳࡴࡕ࡬ࡸࡪ࡚ࡲࡢࡥ࡮࡭ࡳ࡭ࠧᲹ"),
  bstack1111l_opy_ (u"ࠫ࡭࡯ࡧࡩࡅࡲࡲࡹࡸࡡࡴࡶࠪᲺ"),
  bstack1111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡕࡸࡥࡧࡧࡵࡩࡳࡩࡥࡴࠩ᲻"),
  bstack1111l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩ᲼"),
  bstack1111l_opy_ (u"ࠧࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫᲽ"),
  bstack1111l_opy_ (u"ࠨࡴࡨࡱࡴࡼࡥࡊࡑࡖࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࡍࡱࡦࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭Ჾ"),
  bstack1111l_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫᲿ"),
  bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᳀"),
  bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭᳁"),
  bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ᳂"),
  bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᳃"),
  bstack1111l_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪ᳄"),
  bstack1111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ᳅"),
  bstack1111l_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫ᳆"),
  bstack1111l_opy_ (u"ࠪࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡖࡲࡰ࡯ࡳࡸࡇ࡫ࡨࡢࡸ࡬ࡳࡷ࠭᳇")
]
bstack1l1l11l1_opy_ = {
  bstack1111l_opy_ (u"ࠫࡻ࠭᳈"): bstack1111l_opy_ (u"ࠬࡼࠧ᳉"),
  bstack1111l_opy_ (u"࠭ࡦࠨ᳊"): bstack1111l_opy_ (u"ࠧࡧࠩ᳋"),
  bstack1111l_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧ᳌"): bstack1111l_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨ᳍"),
  bstack1111l_opy_ (u"ࠪࡳࡳࡲࡹࡢࡷࡷࡳࡲࡧࡴࡦࠩ᳎"): bstack1111l_opy_ (u"ࠫࡴࡴ࡬ࡺࡃࡸࡸࡴࡳࡡࡵࡧࠪ᳏"),
  bstack1111l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩ᳐"): bstack1111l_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪ᳑"),
  bstack1111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪ᳒"): bstack1111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫ᳓"),
  bstack1111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡱࡵࡸ᳔ࠬ"): bstack1111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ᳕࠭"),
  bstack1111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡸࡷࡪࡸ᳖ࠧ"): bstack1111l_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ᳗"),
  bstack1111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡧࡳࡴ᳘ࠩ"): bstack1111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵ᳙ࠪ"),
  bstack1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩ᳚"): bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ᳛"),
  bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡰࡴࡷ᳜ࠫ"): bstack1111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡱࡵࡸ᳝ࠬ"),
  bstack1111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ᳞࠭"): bstack1111l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ᳟"),
  bstack1111l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩ᳠"): bstack1111l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ᳡"),
  bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵ᳢ࠪ"): bstack1111l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷ᳣ࠬ"),
  bstack1111l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ᳤࠭"): bstack1111l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹ᳥ࠧ"),
  bstack1111l_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪ᳦ࠪ"): bstack1111l_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫᳧ࠫ"),
  bstack1111l_opy_ (u"ࠨࡲࡤࡧ࡫࡯࡬ࡦ᳨ࠩ"): bstack1111l_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᳩ"),
  bstack1111l_opy_ (u"ࠪࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᳪ"): bstack1111l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᳫ"),
  bstack1111l_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᳬ"): bstack1111l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦ᳭ࠩ"),
  bstack1111l_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨᳮ"): bstack1111l_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩᳯ"),
  bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᳰ"): bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᳱ"),
  bstack1111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷ࠭ᳲ"): bstack1111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡰࡦࡣࡷࡩࡷ࠭ᳳ")
}
bstack111l1l111l1_opy_ = bstack1111l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨ࡫ࡷ࡬ࡺࡨ࠮ࡤࡱࡰ࠳ࡵ࡫ࡲࡤࡻ࠲ࡧࡱ࡯࠯ࡳࡧ࡯ࡩࡦࡹࡥࡴ࠱࡯ࡥࡹ࡫ࡳࡵ࠱ࡧࡳࡼࡴ࡬ࡰࡣࡧࠦ᳴")
bstack111l1l1lll1_opy_ = bstack1111l_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠯ࡩࡧࡤࡰࡹ࡮ࡣࡩࡧࡦ࡯ࠧᳵ")
bstack11ll1111ll_opy_ = bstack1111l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡨࡨࡸ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡶࡩࡳࡪ࡟ࡴࡦ࡮ࡣࡪࡼࡥ࡯ࡶࡶࠦᳶ")
HTTPS_HUB = bstack1111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡻࡩ࠵ࡨࡶࡤࠪ᳷")
bstack11l1l111l1_opy_ = bstack1111l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧ࠭᳸")
bstack111ll1ll1_opy_ = bstack1111l_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠵࠶࠷࠸࠴ࡽࡤ࠰ࡪࡸࡦࠬ᳹")
bstack11l1lll1_opy_ = bstack1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠩᳺ")
bstack111l1l11l1_opy_ = {
  bstack1111l_opy_ (u"࠭ࡤࡦࡨࡤࡹࡱࡺࠧ᳻"): bstack1111l_opy_ (u"ࠧࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ᳼"),
  bstack1111l_opy_ (u"ࠨࡷࡶ࠱ࡪࡧࡳࡵࠩ᳽"): bstack1111l_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡵࡴࡧ࠰ࡳࡳࡲࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ᳾"),
  bstack1111l_opy_ (u"ࠪࡹࡸ࠭᳿"): bstack1111l_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡷࡶ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᴀ"),
  bstack1111l_opy_ (u"ࠬ࡫ࡵࠨᴁ"): bstack1111l_opy_ (u"࠭ࡨࡶࡤ࠰ࡩࡺ࠳࡯࡯࡮ࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᴂ"),
  bstack1111l_opy_ (u"ࠧࡪࡰࠪᴃ"): bstack1111l_opy_ (u"ࠨࡪࡸࡦ࠲ࡧࡰࡴ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᴄ"),
  bstack1111l_opy_ (u"ࠩࡤࡹࠬᴅ"): bstack1111l_opy_ (u"ࠪ࡬ࡺࡨ࠭ࡢࡲࡶࡩ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᴆ")
}
bstack111l1ll1111_opy_ = {
  bstack1111l_opy_ (u"ࠫࡨࡸࡩࡵ࡫ࡦࡥࡱ࠭ᴇ"): 50,
  bstack1111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᴈ"): 40,
  bstack1111l_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧᴉ"): 30,
  bstack1111l_opy_ (u"ࠧࡪࡰࡩࡳࠬᴊ"): 20,
  bstack1111l_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᴋ"): 10
}
bstack11l1111lll_opy_ = bstack111l1ll1111_opy_[bstack1111l_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᴌ")]
bstack1l11lll11l_opy_ = bstack1111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦ࠳ࠬᴍ")
bstack1ll1l111_opy_ = bstack1111l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᴎ")
bstack11l1l11lll_opy_ = bstack1111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᴏ")
bstack111ll1l11l_opy_ = bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᴐ")
bstack111ll11l11_opy_ = bstack1111l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬᴑ")
bstack1llll1l1_opy_ = {
  bstack1111l_opy_ (u"ࠨࡕࡇࡏ࠲ࡍࡅࡏ࠯࠳࠴࠺࠭ᴒ"): bstack1111l_opy_ (u"ࠩ࠭࠮࠯࡛ࠦࡔࡆࡎ࠱ࡌࡋࡎ࠮࠲࠳࠹ࡢࠦࡠࡱࡻࡷࡩࡸࡺ࠭ࡱࡣࡵࡥࡱࡲࡥ࡭ࡢࠣ࡭ࡸࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠢ࡬ࡲࠥࡿ࡯ࡶࡴࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠯ࠢࡗ࡬࡮ࡹࠠ࡮ࡣࡼࠤࡨࡧࡵࡴࡧࠣࡧࡴࡴࡦ࡭࡫ࡦࡸࡸࠦࡷࡪࡶ࡫ࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡗࡉࡑ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡮ࡺࠠࡶࡵ࡬ࡲ࡬ࡀࠠࡱ࡫ࡳࠤࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡱࡣࡵࡥࡱࡲࡥ࡭ࠢ࠭࠮࠯࠭ᴓ")
}
bstack111l1lll1ll_opy_ = [bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᴔ"), bstack1111l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᴕ")]
bstack111l1ll11ll_opy_ = [bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᴖ"), bstack1111l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᴗ")]
bstack1111ll1lll_opy_ = re.compile(bstack1111l_opy_ (u"ࠧ࡟࡝࡟ࡠࡼ࠳࡝ࠬ࠼࠱࠮ࠩ࠭ᴘ"))
bstack1ll1llllll_opy_ = [
  bstack1111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡓࡧ࡭ࡦࠩᴙ"),
  bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᴚ"),
  bstack1111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᴛ"),
  bstack1111l_opy_ (u"ࠫࡳ࡫ࡷࡄࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࠨᴜ"),
  bstack1111l_opy_ (u"ࠬࡧࡰࡱࠩᴝ"),
  bstack1111l_opy_ (u"࠭ࡵࡥ࡫ࡧࠫᴞ"),
  bstack1111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᴟ"),
  bstack1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࠨᴠ"),
  bstack1111l_opy_ (u"ࠩࡲࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧᴡ"),
  bstack1111l_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࠨᴢ"),
  bstack1111l_opy_ (u"ࠫࡳࡵࡒࡦࡵࡨࡸࠬᴣ"), bstack1111l_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡕࡩࡸ࡫ࡴࠨᴤ"),
  bstack1111l_opy_ (u"࠭ࡣ࡭ࡧࡤࡶࡘࡿࡳࡵࡧࡰࡊ࡮ࡲࡥࡴࠩᴥ"),
  bstack1111l_opy_ (u"ࠧࡦࡸࡨࡲࡹ࡚ࡩ࡮࡫ࡱ࡫ࡸ࠭ᴦ"),
  bstack1111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࡑࡵࡧࡨ࡫ࡱ࡫ࠬᴧ"),
  bstack1111l_opy_ (u"ࠩࡲࡸ࡭࡫ࡲࡂࡲࡳࡷࠬᴨ"),
  bstack1111l_opy_ (u"ࠪࡴࡷ࡯࡮ࡵࡒࡤ࡫ࡪ࡙࡯ࡶࡴࡦࡩࡔࡴࡆࡪࡰࡧࡊࡦ࡯࡬ࡶࡴࡨࠫᴩ"),
  bstack1111l_opy_ (u"ࠫࡦࡶࡰࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩᴪ"), bstack1111l_opy_ (u"ࠬࡧࡰࡱࡒࡤࡧࡰࡧࡧࡦࠩᴫ"), bstack1111l_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨᴬ"), bstack1111l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡑࡣࡦ࡯ࡦ࡭ࡥࠨᴭ"), bstack1111l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡆࡸࡶࡦࡺࡩࡰࡰࠪᴮ"),
  bstack1111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧᴯ"),
  bstack1111l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡨࡷࡹࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧᴰ"),
  bstack1111l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪ࠭ᴱ"), bstack1111l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࡅ࡯ࡦࡌࡲࡹ࡫࡮ࡵࠩᴲ"),
  bstack1111l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫᴳ"),
  bstack1111l_opy_ (u"ࠧࡢࡦࡥࡔࡴࡸࡴࠨᴴ"),
  bstack1111l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡔࡱࡦ࡯ࡪࡺࠧᴵ"),
  bstack1111l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡗ࡭ࡲ࡫࡯ࡶࡶࠪᴶ"),
  bstack1111l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡺࡨࠨᴷ"),
  bstack1111l_opy_ (u"ࠫࡦࡼࡤࠨᴸ"), bstack1111l_opy_ (u"ࠬࡧࡶࡥࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᴹ"), bstack1111l_opy_ (u"࠭ࡡࡷࡦࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨᴺ"), bstack1111l_opy_ (u"ࠧࡢࡸࡧࡅࡷ࡭ࡳࠨᴻ"),
  bstack1111l_opy_ (u"ࠨࡷࡶࡩࡐ࡫ࡹࡴࡶࡲࡶࡪ࠭ᴼ"), bstack1111l_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡺࡨࠨᴽ"), bstack1111l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡳࡴࡹࡲࡶࡩ࠭ᴾ"),
  bstack1111l_opy_ (u"ࠫࡰ࡫ࡹࡂ࡮࡬ࡥࡸ࠭ᴿ"), bstack1111l_opy_ (u"ࠬࡱࡥࡺࡒࡤࡷࡸࡽ࡯ࡳࡦࠪᵀ"),
  bstack1111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨᵁ"), bstack1111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡇࡲࡨࡵࠪᵂ"), bstack1111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࡇ࡭ࡷ࠭ᵃ"), bstack1111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡄࡪࡵࡳࡲ࡫ࡍࡢࡲࡳ࡭ࡳ࡭ࡆࡪ࡮ࡨࠫᵄ"), bstack1111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡗࡶࡩࡘࡿࡳࡵࡧࡰࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧᵅ"),
  bstack1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࠧᵆ"), bstack1111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࡴࠩᵇ"),
  bstack1111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡉ࡯ࡳࡢࡤ࡯ࡩࡇࡻࡩ࡭ࡦࡆ࡬ࡪࡩ࡫ࠨᵈ"),
  bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻ࡙࡯࡭ࡦࡱࡸࡸࠬᵉ"),
  bstack1111l_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡂࡥࡷ࡭ࡴࡴࠧᵊ"), bstack1111l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡅࡤࡸࡪ࡭࡯ࡳࡻࠪᵋ"), bstack1111l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡉࡰࡦ࡭ࡳࠨᵌ"), bstack1111l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡥࡱࡏ࡮ࡵࡧࡱࡸࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᵍ"),
  bstack1111l_opy_ (u"ࠬࡪ࡯࡯ࡶࡖࡸࡴࡶࡁࡱࡲࡒࡲࡗ࡫ࡳࡦࡶࠪᵎ"),
  bstack1111l_opy_ (u"࠭ࡵ࡯࡫ࡦࡳࡩ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨᵏ"), bstack1111l_opy_ (u"ࠧࡳࡧࡶࡩࡹࡑࡥࡺࡤࡲࡥࡷࡪࠧᵐ"),
  bstack1111l_opy_ (u"ࠨࡰࡲࡗ࡮࡭࡮ࠨᵑ"),
  bstack1111l_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡗࡱ࡭ࡲࡶ࡯ࡳࡶࡤࡲࡹ࡜ࡩࡦࡹࡶࠫᵒ"),
  bstack1111l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳࡪࡲࡰ࡫ࡧ࡛ࡦࡺࡣࡩࡧࡵࡷࠬᵓ"),
  bstack1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᵔ"),
  bstack1111l_opy_ (u"ࠬࡸࡥࡤࡴࡨࡥࡹ࡫ࡃࡩࡴࡲࡱࡪࡊࡲࡪࡸࡨࡶࡘ࡫ࡳࡴ࡫ࡲࡲࡸ࠭ᵕ"),
  bstack1111l_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᵖ"),
  bstack1111l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡔࡦࡺࡨࠨᵗ"),
  bstack1111l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡕࡳࡩࡪࡪࠧᵘ"),
  bstack1111l_opy_ (u"ࠩࡪࡴࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ᵙ"),
  bstack1111l_opy_ (u"ࠪ࡭ࡸࡎࡥࡢࡦ࡯ࡩࡸࡹࠧᵚ"),
  bstack1111l_opy_ (u"ࠫࡦࡪࡢࡆࡺࡨࡧ࡙࡯࡭ࡦࡱࡸࡸࠬᵛ"),
  bstack1111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࡘࡩࡲࡪࡲࡷࠫᵜ"),
  bstack1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡈࡪࡼࡩࡤࡧࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᵝ"),
  bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳࡌࡸࡡ࡯ࡶࡓࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠧᵞ"),
  bstack1111l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡐࡤࡸࡺࡸࡡ࡭ࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ᵟ"),
  bstack1111l_opy_ (u"ࠩࡶࡽࡸࡺࡥ࡮ࡒࡲࡶࡹ࠭ᵠ"),
  bstack1111l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡨࡧࡎ࡯ࡴࡶࠪᵡ"),
  bstack1111l_opy_ (u"ࠫࡸࡱࡩࡱࡗࡱࡰࡴࡩ࡫ࠨᵢ"), bstack1111l_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯࡙ࡿࡰࡦࠩᵣ"), bstack1111l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰࡑࡥࡺࠩᵤ"),
  bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳࡑࡧࡵ࡯ࡥ࡫ࠫᵥ"),
  bstack1111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡥࡤࡸࡈࡧࡰࡵࡷࡵࡩࠬᵦ"),
  bstack1111l_opy_ (u"ࠩࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࡔࡺࡨࡦࡴࡓࡥࡨࡱࡡࡨࡧࡶࠫᵧ"),
  bstack1111l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨ࡛࡮ࡴࡤࡰࡹࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࠬᵨ"),
  bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡳࡴࡲࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᵩ"),
  bstack1111l_opy_ (u"ࠬ࡫࡮ࡧࡱࡵࡧࡪࡇࡰࡱࡋࡱࡷࡹࡧ࡬࡭ࠩᵪ"),
  bstack1111l_opy_ (u"࠭ࡥ࡯ࡵࡸࡶࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡹࡈࡢࡸࡨࡔࡦ࡭ࡥࡴࠩᵫ"), bstack1111l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡅࡧࡹࡸࡴࡵ࡬ࡴࡒࡲࡶࡹ࠭ᵬ"), bstack1111l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡘࡧࡥࡺ࡮࡫ࡷࡅࡧࡷࡥ࡮ࡲࡳࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠫᵭ"),
  bstack1111l_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡳࡴࡸࡉࡡࡤࡪࡨࡐ࡮ࡳࡩࡵࠩᵮ"),
  bstack1111l_opy_ (u"ࠪࡧࡦࡲࡥ࡯ࡦࡤࡶࡋࡵࡲ࡮ࡣࡷࠫᵯ"),
  bstack1111l_opy_ (u"ࠫࡧࡻ࡮ࡥ࡮ࡨࡍࡩ࠭ᵰ"),
  bstack1111l_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬᵱ"),
  bstack1111l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡇࡱࡥࡧࡲࡥࡥࠩᵲ"), bstack1111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡩࡩ࠭ᵳ"),
  bstack1111l_opy_ (u"ࠨࡣࡸࡸࡴࡇࡣࡤࡧࡳࡸࡆࡲࡥࡳࡶࡶࠫᵴ"), bstack1111l_opy_ (u"ࠩࡤࡹࡹࡵࡄࡪࡵࡰ࡭ࡸࡹࡁ࡭ࡧࡵࡸࡸ࠭ᵵ"),
  bstack1111l_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡹࡌࡪࡤࠪᵶ"),
  bstack1111l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡔࡢࡲࠪᵷ"),
  bstack1111l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎࡴࡩࡵ࡫ࡤࡰ࡚ࡸ࡬ࠨᵸ"), bstack1111l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡇ࡬࡭ࡱࡺࡔࡴࡶࡵࡱࡵࠪᵹ"), bstack1111l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉࡨࡰࡲࡶࡪࡌࡲࡢࡷࡧ࡛ࡦࡸ࡮ࡪࡰࡪࠫᵺ"), bstack1111l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡨࡲࡑ࡯࡮࡬ࡵࡌࡲࡇࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠨᵻ"),
  bstack1111l_opy_ (u"ࠩ࡮ࡩࡪࡶࡋࡦࡻࡆ࡬ࡦ࡯࡮ࡴࠩᵼ"),
  bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡽࡥࡧࡲࡥࡔࡶࡵ࡭ࡳ࡭ࡳࡅ࡫ࡵࠫᵽ"),
  bstack1111l_opy_ (u"ࠫࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᵾ"),
  bstack1111l_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡏࡪࡿࡄࡦ࡮ࡤࡽࠬᵿ"),
  bstack1111l_opy_ (u"࠭ࡳࡩࡱࡺࡍࡔ࡙ࡌࡰࡩࠪᶀ"),
  bstack1111l_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᶁ"),
  bstack1111l_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡓࡧࡶࡴࡴࡴࡳࡦࡖ࡬ࡱࡪࡵࡵࡵࠩᶂ"), bstack1111l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࡝ࡡࡪࡶࡗ࡭ࡲ࡫࡯ࡶࡶࠪᶃ"),
  bstack1111l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾ࠭ᶄ"),
  bstack1111l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡸࡿ࡮ࡤࡇࡻࡩࡨࡻࡴࡦࡈࡵࡳࡲࡎࡴࡵࡲࡶࠫᶅ"),
  bstack1111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡉࡡࡱࡶࡸࡶࡪ࠭ᶆ"),
  bstack1111l_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᶇ"),
  bstack1111l_opy_ (u"ࠧࡧࡷ࡯ࡰࡈࡵ࡮ࡵࡧࡻࡸࡑ࡯ࡳࡵࠩᶈ"),
  bstack1111l_opy_ (u"ࠨࡹࡤ࡭ࡹࡌ࡯ࡳࡃࡳࡴࡘࡩࡲࡪࡲࡷࠫᶉ"),
  bstack1111l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡆࡳࡳࡴࡥࡤࡶࡕࡩࡹࡸࡩࡦࡵࠪᶊ"),
  bstack1111l_opy_ (u"ࠪࡥࡵࡶࡎࡢ࡯ࡨࠫᶋ"),
  bstack1111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡘࡒࡃࡦࡴࡷࠫᶌ"),
  bstack1111l_opy_ (u"ࠬࡺࡡࡱ࡙࡬ࡸ࡭࡙ࡨࡰࡴࡷࡔࡷ࡫ࡳࡴࡆࡸࡶࡦࡺࡩࡰࡰࠪᶍ"),
  bstack1111l_opy_ (u"࠭ࡳࡤࡣ࡯ࡩࡋࡧࡣࡵࡱࡵࠫᶎ"),
  bstack1111l_opy_ (u"ࠧࡸࡦࡤࡐࡴࡩࡡ࡭ࡒࡲࡶࡹ࠭ᶏ"),
  bstack1111l_opy_ (u"ࠨࡵ࡫ࡳࡼ࡞ࡣࡰࡦࡨࡐࡴ࡭ࠧᶐ"),
  bstack1111l_opy_ (u"ࠩ࡬ࡳࡸࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡶࡵࡨࠫᶑ"),
  bstack1111l_opy_ (u"ࠪࡼࡨࡵࡤࡦࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠬᶒ"),
  bstack1111l_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡴࡵࡺࡳࡷࡪࠧᶓ"),
  bstack1111l_opy_ (u"ࠬࡻࡳࡦࡒࡵࡩࡧࡻࡩ࡭ࡶ࡚ࡈࡆ࠭ᶔ"),
  bstack1111l_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡗࡅࡃࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧᶕ"),
  bstack1111l_opy_ (u"ࠧࡸࡧࡥࡈࡷ࡯ࡶࡦࡴࡄ࡫ࡪࡴࡴࡖࡴ࡯ࠫᶖ"),
  bstack1111l_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡹ࡮ࠧᶗ"),
  bstack1111l_opy_ (u"ࠩࡸࡷࡪࡔࡥࡸ࡙ࡇࡅࠬᶘ"),
  bstack1111l_opy_ (u"ࠪࡻࡩࡧࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᶙ"), bstack1111l_opy_ (u"ࠫࡼࡪࡡࡄࡱࡱࡲࡪࡩࡴࡪࡱࡱࡘ࡮ࡳࡥࡰࡷࡷࠫᶚ"),
  bstack1111l_opy_ (u"ࠬࡾࡣࡰࡦࡨࡓࡷ࡭ࡉࡥࠩᶛ"), bstack1111l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡘ࡯ࡧ࡯࡫ࡱ࡫ࡎࡪࠧᶜ"),
  bstack1111l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡘࡆࡄࡆࡺࡴࡤ࡭ࡧࡌࡨࠬᶝ"),
  bstack1111l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡏ࡯ࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡷࡺࡏ࡯࡮ࡼࠫᶞ"),
  bstack1111l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࡶࠫᶟ"),
  bstack1111l_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵ࡭ࡪࡹࠧᶠ"), bstack1111l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶࡾࡏ࡮ࡵࡧࡵࡺࡦࡲࠧᶡ"),
  bstack1111l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹࡎࡡࡳࡦࡺࡥࡷ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨᶢ"),
  bstack1111l_opy_ (u"࠭࡭ࡢࡺࡗࡽࡵ࡯࡮ࡨࡈࡵࡩࡶࡻࡥ࡯ࡥࡼࠫᶣ"),
  bstack1111l_opy_ (u"ࠧࡴ࡫ࡰࡴࡱ࡫ࡉࡴࡘ࡬ࡷ࡮ࡨ࡬ࡦࡅ࡫ࡩࡨࡱࠧᶤ"),
  bstack1111l_opy_ (u"ࠨࡷࡶࡩࡈࡧࡲࡵࡪࡤ࡫ࡪ࡙ࡳ࡭ࠩᶥ"),
  bstack1111l_opy_ (u"ࠩࡶ࡬ࡴࡻ࡬ࡥࡗࡶࡩࡘ࡯࡮ࡨ࡮ࡨࡸࡴࡴࡔࡦࡵࡷࡑࡦࡴࡡࡨࡧࡵࠫᶦ"),
  bstack1111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡋ࡚ࡈࡕ࠭ᶧ"),
  bstack1111l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡳࡺࡩࡨࡊࡦࡈࡲࡷࡵ࡬࡭ࠩᶨ"),
  bstack1111l_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࡍ࡯ࡤࡥࡧࡱࡅࡵ࡯ࡐࡰ࡮࡬ࡧࡾࡋࡲࡳࡱࡵࠫᶩ"),
  bstack1111l_opy_ (u"࠭࡭ࡰࡥ࡮ࡐࡴࡩࡡࡵ࡫ࡲࡲࡆࡶࡰࠨᶪ"),
  bstack1111l_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡰࡴࡰࡥࡹ࠭ᶫ"), bstack1111l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇ࡫࡯ࡸࡪࡸࡓࡱࡧࡦࡷࠬᶬ"),
  bstack1111l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡅࡧ࡯ࡥࡾࡇࡤࡣࠩᶭ"),
  bstack1111l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡍࡩࡒ࡯ࡤࡣࡷࡳࡷࡇࡵࡵࡱࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳ࠭ᶮ")
]
bstack11lllll1_opy_ = bstack1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪᶯ")
bstack1l1111l1_opy_ = [bstack1111l_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪᶰ"), bstack1111l_opy_ (u"࠭࠮ࡢࡣࡥࠫᶱ"), bstack1111l_opy_ (u"ࠧ࠯࡫ࡳࡥࠬᶲ")]
bstack1lll1111l_opy_ = [bstack1111l_opy_ (u"ࠨ࡫ࡧࠫᶳ"), bstack1111l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᶴ"), bstack1111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ᶵ"), bstack1111l_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪᶶ")]
bstack11l111lll1_opy_ = {
  bstack1111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᶷ"): bstack1111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᶸ"),
  bstack1111l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᶹ"): bstack1111l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᶺ"),
  bstack1111l_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᶻ"): bstack1111l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᶼ"),
  bstack1111l_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᶽ"): bstack1111l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫᶾ"),
  bstack1111l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭ᶿ"): bstack1111l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ᷀")
}
bstack11l1111l1l_opy_ = [
  bstack1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᷁"),
  bstack1111l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹ᷂ࠧ"),
  bstack1111l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ᷃"),
  bstack1111l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᷄"),
  bstack1111l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭᷅"),
]
bstack11l1l1111l_opy_ = bstack11l11l1l11_opy_ + bstack111ll1111l1_opy_ + bstack1ll1llllll_opy_
bstack1l111l111_opy_ = [
  bstack1111l_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫ᷆"),
  bstack1111l_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨ᷇"),
  bstack1111l_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧ᷈"),
  bstack1111l_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ᷉"),
  bstack1111l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯᷊ࠩ"),
  bstack1111l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪ᷋"),
  bstack1111l_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫ᷌"),
  bstack1111l_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩ᷍")
]
bstack111ll1llll1_opy_ = bstack1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ᷎")
bstack1l111l1111_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺ᷏ࠧ")
bstack1l11l11l_opy_ = [ bstack1111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨ᷐ࠫ") ]
bstack1l11l1111_opy_ = [ bstack1111l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ᷑") ]
bstack11ll1l11_opy_ = [bstack1111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᷒")]
bstack1l111lll_opy_ = [ bstack1111l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᷓ") ]
bstack1l1ll1l111_opy_ = bstack1111l_opy_ (u"࠭ࡓࡅࡍࡖࡩࡹࡻࡰࠨᷔ")
bstack1lll111l1_opy_ = bstack1111l_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪᷕ")
bstack1l111llll1_opy_ = bstack1111l_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠬᷖ")
bstack11l11ll1_opy_ = bstack1111l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࠨᷗ")
bstack11lll1l1l1_opy_ = [
  bstack1111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡇࡃࡌࡐࡊࡊࠧᷘ"),
  bstack1111l_opy_ (u"ࠫࡊࡘࡒࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫᷙ"),
  bstack1111l_opy_ (u"ࠬࡋࡒࡓࡡࡅࡐࡔࡉࡋࡆࡆࡢࡆ࡞ࡥࡃࡍࡋࡈࡒ࡙࠭ᷚ"),
  bstack1111l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡊ࡚ࡗࡐࡔࡎࡣࡈࡎࡁࡏࡉࡈࡈࠬᷛ"),
  bstack1111l_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡇࡗࡣࡓࡕࡔࡠࡅࡒࡒࡓࡋࡃࡕࡇࡇࠫᷜ"),
  bstack1111l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡆࡐࡔ࡙ࡅࡅࠩᷝ"),
  bstack1111l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊ࡙ࡅࡕࠩᷞ"),
  bstack1111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡆࡖࡕࡈࡈࠬᷟ"),
  bstack1111l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡇࡂࡐࡔࡗࡉࡉ࠭ᷠ"),
  bstack1111l_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᷡ"),
  bstack1111l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧᷢ"),
  bstack1111l_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤࡏࡎࡗࡃࡏࡍࡉ࠭ᷣ"),
  bstack1111l_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫᷤ"),
  bstack1111l_opy_ (u"ࠩࡈࡖࡗࡥࡔࡖࡐࡑࡉࡑࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪᷥ"),
  bstack1111l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧᷦ"),
  bstack1111l_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫᷧ"),
  bstack1111l_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡎࡏࡔࡖࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨᷨ"),
  bstack1111l_opy_ (u"࠭ࡅࡓࡔࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᷩ"),
  bstack1111l_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨᷪ"),
  bstack1111l_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡖࡊ࡙ࡏࡍࡗࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᷫ"),
  bstack1111l_opy_ (u"ࠩࡈࡖࡗࡥࡍࡂࡐࡇࡅ࡙ࡕࡒ࡚ࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᷬ"),
]
bstack1lll11ll_opy_ = bstack1111l_opy_ (u"ࠪ࠲࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠯ࠨᷭ")
bstack11l1llll1_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠫࢃ࠭ᷮ")), bstack1111l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᷯ"), bstack1111l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᷰ"))
bstack11l1111l111_opy_ = bstack1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡩࠨᷱ")
bstack111ll111lll_opy_ = [ bstack1111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᷲ"), bstack1111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᷳ"), bstack1111l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩᷴ"), bstack1111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᷵")]
bstack1ll1l1ll11_opy_ = [ bstack1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᷶"), bstack1111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ᷷ࠬ"), bstack1111l_opy_ (u"ࠧࡱࡣࡥࡳࡹ᷸࠭"), bstack1111l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ᷹") ]
bstack111l1ll111_opy_ = [ bstack1111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᷺") ]
bstack111l1l1llll_opy_ = [ bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᷻") ]
bstack1l1l1l11l1_opy_ = 360
bstack111ll1ll111_opy_ = bstack1111l_opy_ (u"ࠦࡦࡶࡰ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦ᷼")
bstack111l1l11ll1_opy_ = bstack1111l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡪࡵࡶࡹࡪࡹ᷽ࠢ")
bstack111ll11l111_opy_ = bstack1111l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡫ࡶࡷࡺ࡫ࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠤ᷾")
bstack111lll1l1l1_opy_ = bstack1111l_opy_ (u"ࠢࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡶࡨࡷࡹࡹࠠࡢࡴࡨࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡰࡰࠣࡓࡘࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠦࡵࠣࡥࡳࡪࠠࡢࡤࡲࡺࡪࠦࡦࡰࡴࠣࡅࡳࡪࡲࡰ࡫ࡧࠤࡩ࡫ࡶࡪࡥࡨࡷ࠳ࠨ᷿")
bstack111lll11ll1_opy_ = bstack1111l_opy_ (u"ࠣ࠳࠴࠲࠵ࠨḀ")
bstack1lllll1l1l1_opy_ = {
  bstack1111l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧḁ"): bstack1111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪḂ"),
  bstack1111l_opy_ (u"ࠫࡋࡇࡉࡍࠩḃ"): bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬḄ"),
  bstack1111l_opy_ (u"࠭ࡓࡌࡋࡓࠫḅ"): bstack1111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨḆ")
}
bstack11ll1l1lll_opy_ = [
  bstack1111l_opy_ (u"ࠣࡩࡨࡸࠧḇ"),
  bstack1111l_opy_ (u"ࠤࡪࡳࡇࡧࡣ࡬ࠤḈ"),
  bstack1111l_opy_ (u"ࠥ࡫ࡴࡌ࡯ࡳࡹࡤࡶࡩࠨḉ"),
  bstack1111l_opy_ (u"ࠦࡷ࡫ࡦࡳࡧࡶ࡬ࠧḊ"),
  bstack1111l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦḋ"),
  bstack1111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥḌ"),
  bstack1111l_opy_ (u"ࠢࡴࡷࡥࡱ࡮ࡺࡅ࡭ࡧࡰࡩࡳࡺࠢḍ"),
  bstack1111l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧḎ"),
  bstack1111l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧḏ"),
  bstack1111l_opy_ (u"ࠥࡧࡱ࡫ࡡࡳࡇ࡯ࡩࡲ࡫࡮ࡵࠤḐ"),
  bstack1111l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࡷࠧḑ"),
  bstack1111l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠧḒ"),
  bstack1111l_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡁࡴࡻࡱࡧࡘࡩࡲࡪࡲࡷࠦḓ"),
  bstack1111l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨḔ"),
  bstack1111l_opy_ (u"ࠣࡳࡸ࡭ࡹࠨḕ"),
  bstack1111l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡗࡳࡺࡩࡨࡂࡥࡷ࡭ࡴࡴࠢḖ"),
  bstack1111l_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡑࡺࡲࡴࡪࡖࡲࡹࡨ࡮ࠢḗ"),
  bstack1111l_opy_ (u"ࠦࡸ࡮ࡡ࡬ࡧࠥḘ"),
  bstack1111l_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࡅࡵࡶࠢḙ")
]
bstack111l1ll1l1l_opy_ = [
  bstack1111l_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧḚ"),
  bstack1111l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦḛ"),
  bstack1111l_opy_ (u"ࠣࡣࡸࡸࡴࠨḜ"),
  bstack1111l_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤḝ"),
  bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧḞ")
]
bstack1llll11l1l_opy_ = {
  bstack1111l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥḟ"): [bstack1111l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦḠ")],
  bstack1111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥḡ"): [bstack1111l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦḢ")],
  bstack1111l_opy_ (u"ࠣࡣࡸࡸࡴࠨḣ"): [bstack1111l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨḤ"), bstack1111l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨḥ"), bstack1111l_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣḦ"), bstack1111l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦḧ")],
  bstack1111l_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨḨ"): [bstack1111l_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢḩ")],
  bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥḪ"): [bstack1111l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦḫ")],
}
bstack111l1llll1l_opy_ = {
  bstack1111l_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤḬ"): bstack1111l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥḭ"),
  bstack1111l_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤḮ"): bstack1111l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥḯ"),
  bstack1111l_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦḰ"): bstack1111l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࠥḱ"),
  bstack1111l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧḲ"): bstack1111l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧḳ"),
  bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨḴ"): bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢḵ")
}
bstack1llll1ll11l_opy_ = {
  bstack1111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪḶ"): bstack1111l_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࠦࡓࡦࡶࡸࡴࠬḷ"),
  bstack1111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫḸ"): bstack1111l_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡖࡨࡥࡷࡪ࡯ࡸࡰࠪḹ"),
  bstack1111l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨḺ"): bstack1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡖࡩࡹࡻࡰࠨḻ"),
  bstack1111l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩḼ"): bstack1111l_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭ḽ")
}
bstack111l1l1111l_opy_ = 65536
bstack111l1ll11l1_opy_ = bstack1111l_opy_ (u"ࠧ࠯࠰࠱࡟࡙ࡘࡕࡏࡅࡄࡘࡊࡊ࡝ࠨḾ")
bstack111l1l1l11l_opy_ = [
      bstack1111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪḿ"), bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬṀ"), bstack1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ṁ"), bstack1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨṂ"), bstack1111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧṃ"),
      bstack1111l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩṄ"), bstack1111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪṅ"), bstack1111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩṆ"), bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪṇ"),
      bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫṈ"), bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ṉ"), bstack1111l_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨṊ")
    ]
bstack111l1l111ll_opy_= {
  bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪṋ"): bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫṌ"),
  bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬṍ"): bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭Ṏ"),
  bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩṏ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨṐ"),
  bstack1111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬṑ"): bstack1111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭Ṓ"),
  bstack1111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪṓ"): bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫṔ"),
  bstack1111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫṕ"): bstack1111l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬṖ"),
  bstack1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧṗ"): bstack1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨṘ"),
  bstack1111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪṙ"): bstack1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫṚ"),
  bstack1111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫṛ"): bstack1111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬṜ"),
  bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨṝ"): bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩṞ"),
  bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩṟ"): bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪṠ"),
  bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧṡ"): bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨṢ"),
  bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ṣ"): bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧṤ"),
  bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫṥ"): bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࡔࡶࡴࡪࡱࡱࡷࠬṦ"),
  bstack1111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨṧ"): bstack1111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩṨ"),
  bstack1111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬṩ"): bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫṪ"),
  bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬṫ"): bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ṭ"),
  bstack1111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩṭ"): bstack1111l_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪṮ"),
  bstack1111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ṯ"): bstack1111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧṰ"),
  bstack1111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨṱ"): bstack1111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩṲ"),
  bstack1111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧṳ"): bstack1111l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨṴ"),
  bstack1111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨṵ"): bstack1111l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩṶ"),
  bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṷ"): bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṸ"),
  bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪṹ"): bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫṺ"),
  bstack1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩṻ"): bstack1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪṼ"),
  bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫṽ"): bstack1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬṾ"),
  bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ṿ"): bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧẀ"),
  bstack1111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫẁ"): bstack1111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬẂ")
}
bstack111l1ll1ll1_opy_ = [bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ẃ"), bstack1111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭Ẅ")]
bstack11ll1111l_opy_ = (bstack1111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣẅ"),)
bstack111l1ll1l11_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡸࡴࡩࡧࡴࡦࡡࡦࡰ࡮࠭Ẇ")
bstack1l1lllllll_opy_ = bstack1111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡧࡳ࡫ࡧࡷ࠴ࠨẇ")
bstack1lllllll1l_opy_ = bstack1111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡲࡪࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡢࡵ࡫ࡦࡴࡧࡲࡥ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࠥẈ")
bstack1ll1ll1l1l_opy_ = bstack1111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳࠨẉ")
class EVENTS(Enum):
  bstack111l1lllll1_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪẊ")
  bstack1l1l1l111l_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡥࡢࡰࡸࡴࠬẋ")
  bstack1111l11111_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿࡬ࡩ࡯ࡣ࡯࡭ࡿ࡫ࠧẌ")
  bstack111l1l11l1l_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡰࡧࡰࡴ࡭ࡳࠨẍ")
  bstack1l11lll1ll_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭Ẏ") #shift post bstack111l1l1ll11_opy_
  bstack1111l1llll_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬẏ") #shift post bstack111l1l1ll11_opy_
  bstack111ll111ll1_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡨࡶࡤࠪẐ") #shift
  bstack111l1l1ll1l_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡧࡳࡼࡴ࡬ࡰࡣࡧࠫẑ") #shift
  bstack1ll111lll_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠻ࡪࡸࡦ࠲ࡳࡡ࡯ࡣࡪࡩࡲ࡫࡮ࡵࠩẒ")
  bstack1l1l111ll1l_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡷࡦࡼࡥ࠮ࡴࡨࡷࡺࡲࡴࡴࠩẓ")
  bstack1l11llll_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡵ࡫ࡲࡧࡱࡵࡱࡸࡩࡡ࡯ࠩẔ")
  bstack11l1l1ll1_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡯ࡳࡨࡧ࡬ࠨẕ") #shift
  bstack1lll111l1l_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡢࡲࡳ࠱ࡺࡶ࡬ࡰࡣࡧࠫẖ") #shift
  bstack11l111ll11_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡨ࡯࠭ࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠪẗ")
  bstack1lllll11l1_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧẘ") #shift
  bstack11ll1lll1l_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡪࡩࡹ࠳ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠳ࡲࡦࡵࡸࡰࡹࡹࠧẙ") #shift
  bstack111ll111l11_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼࠫẚ") #shift
  bstack1l111111l11_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩẛ")
  bstack111l11ll_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡶࡩࡸࡹࡩࡰࡰ࠰ࡷࡹࡧࡴࡶࡵࠪẜ") #shift
  bstack11lll111l1_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽࡬ࡺࡨ࠭࡮ࡣࡱࡥ࡬࡫࡭ࡦࡰࡷࠫẝ")
  bstack111l1l11111_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡴࡾࡹ࠮ࡵࡨࡸࡺࡶࠧẞ") #shift
  bstack111l11111l_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡺࡵࡱࠩẟ")
  bstack111ll11111l_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡷࡳࡧࡰࡴࡪࡲࡸࠬẠ") # not bstack111l1l1l1l1_opy_ in python
  bstack11111ll1l_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡷࡵࡪࡶࠪạ") # used in bstack111l1ll1lll_opy_
  bstack11l11ll1111_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡳࡧ࠰ࡵࡺ࡯ࡴࠨẢ")
  bstack11l11ll1ll1_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲ࡷࡵࡪࡶࠪả")
  bstack1111ll1ll1_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡩࡨࡸࠬẤ") # used in bstack111l1ll1lll_opy_
  bstack1l11ll1l1l_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼࡫ࡳࡴࡱࠧấ")
  bstack11l1l11ll1l_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷ࡫࠭ࡩࡱࡲ࡯ࠬẦ")
  bstack11l1l111ll1_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡵࡳࡵ࠯࡫ࡳࡴࡱࠧầ")
  bstack1lll1l1ll_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪ࠭Ẩ")
  bstack1llllll1l1_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳ࠭ẩ") #
  bstack111ll1111l_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡰ࠳࠴ࡽ࠿ࡪࡲࡪࡸࡨࡶ࠲ࡺࡡ࡬ࡧࡖࡧࡷ࡫ࡥ࡯ࡕ࡫ࡳࡹ࠭Ẫ")
  bstack1l1111llll_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡢࡷࡷࡳ࠲ࡩࡡࡱࡶࡸࡶࡪ࠭ẫ")
  bstack111l1l11l_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡴࡦࡵࡷࠫẬ")
  bstack111l11l11l_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡶࡨࡷࡹ࠭ậ")
  bstack1l1lll111_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡸࡥ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩẮ") #shift
  bstack1l1l11111_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫắ") #shift
  bstack111l1lll1l1_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬẰ")
  bstack111l1l11lll_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡬ࡨࡱ࡫࠭ࡵ࡫ࡰࡩࡴࡻࡴࠨằ")
  bstack11111l11_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡧࡻ࡭ࡹ࠳ࡨࡢࡰࡧࡰࡪࡸࠧẲ")
  bstack1ll1111ll1l_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡥࡹ࡫ࡷ࠱࡭ࡧ࡮ࡥ࡮ࡨࡶࠬẳ")
  bstack111l1l1l111_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡷࡪࡴࡤ࠮࡯ࡨࡸࡷ࡯ࡣࡴࠩẴ")
  bstack111l1l1l1ll_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡪࡸࡦ࠿ࡹࡴࡰࡲࠪẵ")
  bstack1l1ll111ll1_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡶࡸࡦࡸࡴࠨẶ")
  bstack111l1llllll_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡨࡴࡽ࡮࡭ࡱࡤࡨࠬặ")
  bstack111l1ll111l_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡨ࡮ࡥࡤ࡭࠰ࡹࡵࡪࡡࡵࡧࠪẸ")
  bstack1l1ll1lll11_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡤࡲࡳࡹࡹࡴࡳࡣࡳࠫẹ")
  bstack1ll111l1l11_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡶࡸࡦࡸࡴࡣ࡫ࡱࡥࡷࡿࠧẺ")
  bstack1l1ll11llll_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡧࡴࡴ࡮ࡦࡥࡷࠫẻ")
  bstack1l1lll111ll_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡸࡺ࡯ࡱࠩẼ")
  bstack1l1ll1l11ll_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠧẽ")
  bstack1l1l1lll1l1_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀࡣࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰࠪẾ")
  bstack111ll111111_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠫế")
  bstack111l1lll11l_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡨ࡬ࡲࡩࡔࡥࡢࡴࡨࡷࡹࡎࡵࡣࠩỀ")
  bstack11ll1ll1lll_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡊࡰ࡬ࡸࠬề")
  bstack11ll1ll1ll1_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡷࡺࠧỂ")
  bstack1l1l1l111l1_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪể")
  bstack111ll1111ll_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡈࡵ࡮ࡧ࡫ࡪࠫỄ")
  bstack1l11ll11l11_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡖࡸࡪࡶࠧễ")
  bstack1l11ll111ll_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࡫ࡖࡩࡱ࡬ࡈࡦࡣ࡯ࡋࡪࡺࡒࡦࡵࡸࡰࡹ࠭Ệ")
  bstack1l1111llll1_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡆࡸࡨࡲࡹ࠭ệ")
  bstack1l111l1l1l1_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠬỈ")
  bstack1l1111ll11l_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺࡭ࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࡉࡻ࡫࡮ࡵࠩỉ")
  bstack111l1llll11_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡧࡱࡵࡺ࡫ࡵࡦࡖࡨࡷࡹࡋࡶࡦࡰࡷࠫỊ")
  bstack11ll1lll111_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡵࡰࠨị")
  bstack1l1ll111111_opy_ = bstack1111l_opy_ (u"ࠩࡶࡨࡰࡀ࡯࡯ࡕࡷࡳࡵ࠭Ọ")
  bstack11l111l1l11_opy_ = bstack1111l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮ࡨࡥࡳࡻࡰࡖࡲ࡯ࡳࡦࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠫọ")
  bstack1l1ll1lll_opy_ = bstack1111l_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡌࡵ࡯ࡰࡨࡰ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠫỎ")
  bstack1l11111111_opy_ = bstack1111l_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪࡆࡶࡰࡱࡩࡱ࡚ࡥࡴࡶࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࠬỏ")
  bstack1lll1l111ll_opy_ = bstack1111l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡵࡶ࡬ࡺࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡑࡻࡷࡩࡸࡺࠧỐ")
  bstack1lll1ll1l1l_opy_ = bstack1111l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡴࡒࡼࡸࡪࡹࡴࠨố")
  bstack1lll1l1l111_opy_ = bstack1111l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡹࡵࡧࡶࡸࡌ࡫ࡴࡕࡱࡷࡥࡱ࡚ࡥࡴࡶࡶࠫỒ")
class STAGE(Enum):
  bstack1lll1l11ll_opy_ = bstack1111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨồ")
  END = bstack1111l_opy_ (u"ࠪࡩࡳࡪࠧỔ")
  bstack11lll111l_opy_ = bstack1111l_opy_ (u"ࠫࡸ࡯࡮ࡨ࡮ࡨࠫổ")
bstack11lll11ll1_opy_ = {
  bstack1111l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬỖ"): bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ỗ"),
  bstack1111l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫỘ"): bstack1111l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪộ")
}
PLAYWRIGHT_HUB_URL = bstack1111l_opy_ (u"ࠤࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠦỚ")
MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION = 98
bstack1l1l11l1l11_opy_ = 100
bstack1lll11lll1l_opy_ = {
  bstack1111l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࠩớ"): bstack1111l_opy_ (u"ࠫ࠲࠳ࡲࡦࡴࡸࡲࡸ࠭Ờ"),
  bstack1111l_opy_ (u"ࠬࡪࡥ࡭ࡣࡼࠫờ"): bstack1111l_opy_ (u"࠭࠭࠮ࡴࡨࡶࡺࡴࡳ࠮ࡦࡨࡰࡦࡿࠧỞ"),
  bstack1111l_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠳ࡤࡦ࡮ࡤࡽࠬở"): 0
}
bstack111ll111l1l_opy_ = bstack1111l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣỠ")
bstack111l1l11l11_opy_ = bstack1111l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡹࡵࡲ࡯ࡢࡦ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨỡ")
bstack1l1lllll1l_opy_ = bstack1111l_opy_ (u"ࠥࡘࡊ࡙ࡔࠡࡔࡈࡔࡔࡘࡔࡊࡐࡊࠤࡆࡔࡄࠡࡃࡑࡅࡑ࡟ࡔࡊࡅࡖࠦỢ")