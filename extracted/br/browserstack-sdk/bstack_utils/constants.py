# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import re
from enum import Enum
bstack1l11111ll_opy_ = {
  bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᦘ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࠬᦙ"),
  bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᦚ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡮ࡩࡾ࠭ᦛ"),
  bstack11l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᦜ"): bstack11l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᦝ"),
  bstack11l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᦞ"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧᦟ"),
  bstack11l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᦠ"): bstack11l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࠪᦡ"),
  bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᦢ"): bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪᦣ"),
  bstack11l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᦤ"): bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᦥ"),
  bstack11l11_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᦦ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠭ᦧ"),
  bstack11l11_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧᦨ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡳࡹ࡯࡭ࡧࠪᦩ"),
  bstack11l11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩᦪ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩᦫ"),
  bstack11l11_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪ᦬"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪ᦭"),
  bstack11l11_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧ᦮"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡸ࡬ࡨࡪࡵࠧ᦯"),
  bstack11l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩᦰ"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩᦱ"),
  bstack11l11_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬᦲ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬᦳ"),
  bstack11l11_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬᦴ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬᦵ"),
  bstack11l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫᦶ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫᦷ"),
  bstack11l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᦸ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᦹ"),
  bstack11l11_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬᦺ"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬᦻ"),
  bstack11l11_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᦼ"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᦽ"),
  bstack11l11_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪᦾ"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪᦿ"),
  bstack11l11_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧᧀ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡯ࡦࡎࡩࡾࡹࠧᧁ"),
  bstack11l11_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩᧂ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳ࡜ࡧࡩࡵࠩᧃ"),
  bstack11l11_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨᧄ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡳࠨᧅ"),
  bstack11l11_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬᧆ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧ࡬ࡣࡢࡥ࡫ࡩࠬᧇ"),
  bstack11l11_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧᧈ"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧᧉ"),
  bstack11l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫ᧊"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫ᧋"),
  bstack11l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ᧌"): bstack11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ᧍"),
  bstack11l11_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ᧎"): bstack11l11_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫ᧏"),
  bstack11l11_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᧐"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᧑"),
  bstack11l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩ᧒"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩ᧓"),
  bstack11l11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬ᧔"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬ᧕"),
  bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬ᧖"): bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨ᧗"),
  bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᧘"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᧙"),
  bstack11l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ᧚"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡴࡻࡲࡤࡧࠪ᧛"),
  bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᧜"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᧝"),
  bstack11l11_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩ᧞"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡓࡧ࡭ࡦࠩ᧟"),
  bstack11l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬ᧠"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬ᧡"),
  bstack11l11_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨ᧢"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨ᧣"),
  bstack11l11_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫ᧤"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫ᧥"),
  bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᧦"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᧧"),
  bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ᧨"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ᧩")
}
bstack111ll1llll1_opy_ = [
  bstack11l11_opy_ (u"ࠬࡵࡳࠨ᧪"),
  bstack11l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ᧫"),
  bstack11l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᧬"),
  bstack11l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᧭"),
  bstack11l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭᧮"),
  bstack11l11_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ᧯"),
  bstack11l11_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ᧰"),
]
bstack1l11l11l1l_opy_ = {
  bstack11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ᧱"): [bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ᧲"), bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡓࡇࡍࡆࠩ᧳")],
  bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᧴"): bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ᧵"),
  bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᧶"): bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠧ᧷"),
  bstack11l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ᧸"): bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠫ᧹"),
  bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᧺"): bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ᧻"),
  bstack11l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᧼"): bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡗࡤࡖࡅࡓࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫ᧽"),
  bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ᧾"): bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࠪ᧿"),
  bstack11l11_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪᨀ"): bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫᨁ"),
  bstack11l11_opy_ (u"ࠨࡣࡳࡴࠬᨂ"): [bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡓࡔࡤࡏࡄࠨᨃ"), bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕ࠭ᨄ")],
  bstack11l11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᨅ"): bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡎࡒࡋࡑࡋࡖࡆࡎࠪᨆ"),
  bstack11l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᨇ"): bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᨈ"),
  bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᨉ"): [bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞࠭ᨊ"), bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪᨋ")],
  bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᨌ"): bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙࡛ࡒࡃࡑࡖࡇࡆࡒࡅࠨᨍ"),
  bstack11l11_opy_ (u"࠭ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࡆࡐ࡙ࠫᨎ"): bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡏࡓࡅࡋࡉࡘ࡚ࡒࡂࡖࡌࡓࡓࡥࡓࡎࡃࡕࡘࡤ࡙ࡅࡍࡇࡆࡘࡎࡕࡎࡠࡈࡈࡅ࡙࡛ࡒࡆࡡࡅࡖࡆࡔࡃࡉࡇࡖࠫᨏ")
}
bstack1ll11llll1_opy_ = {
  bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᨐ"): [bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᨑ"), bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᨒ")],
  bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᨓ"): [bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡣࡰ࡫ࡹࠨᨔ"), bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᨕ")],
  bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᨖ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᨗ"),
  bstack11l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ᨘࠧ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᨙ"),
  bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᨚ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᨛ"),
  bstack11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭᨜"): [bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡱࡲࠪ᨝"), bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᨞")],
  bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᨟"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᨠ"),
  bstack11l11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᨡ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᨢ"),
  bstack11l11_opy_ (u"࠭ࡡࡱࡲࠪᨣ"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲࠪᨤ"),
  bstack11l11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᨥ"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᨦ"),
  bstack11l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᨧ"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᨨ"),
  bstack11l11_opy_ (u"ࠧࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡃࡍࡋࠥᨩ"): bstack11l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࠦᨪ"),
}
bstack1lllll1ll1_opy_ = {
  bstack11l11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᨫ"): bstack11l11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᨬ"),
  bstack11l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᨭ"): [bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᨮ"), bstack11l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᨯ")],
  bstack11l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᨰ"): bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᨱ"),
  bstack11l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᨲ"): bstack11l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᨳ"),
  bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᨴ"): [bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᨵ"), bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᨶ")],
  bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᨷ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᨸ"),
  bstack11l11_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫᨹ"): bstack11l11_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭ᨺ"),
  bstack11l11_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᨻ"): [bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᨼ"), bstack11l11_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᨽ")],
  bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫᨾ"): [bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧᨿ"), bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࠧᩀ")]
}
bstack1llll1l1_opy_ = [
  bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧᩁ"),
  bstack11l11_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬᩂ"),
  bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩᩃ"),
  bstack11l11_opy_ (u"ࠫࡸ࡫ࡴࡘ࡫ࡱࡨࡴࡽࡒࡦࡥࡷࠫᩄ"),
  bstack11l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧᩅ"),
  bstack11l11_opy_ (u"࠭ࡳࡵࡴ࡬ࡧࡹࡌࡩ࡭ࡧࡌࡲࡹ࡫ࡲࡢࡥࡷࡥࡧ࡯࡬ࡪࡶࡼࠫᩆ"),
  bstack11l11_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪᩇ"),
  bstack11l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩈ"),
  bstack11l11_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧᩉ"),
  bstack11l11_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫᩊ"),
  bstack11l11_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᩋ"),
  bstack11l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᩌ"),
]
bstack1l1lllllll_opy_ = [
  bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᩍ"),
  bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᩎ"),
  bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᩏ"),
  bstack11l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᩐ"),
  bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᩑ"),
  bstack11l11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᩒ"),
  bstack11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᩓ"),
  bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᩔ"),
  bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᩕ"),
  bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩖ"),
  bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᩗ"),
  bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪᩘ"),
  bstack11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ᩙ"),
  bstack11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡙ࡧࡧࠨᩚ"),
  bstack11l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᩛ"),
  bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᩜ"),
  bstack11l11_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᩝ"),
  bstack11l11_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠱ࠨᩞ"),
  bstack11l11_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠳ࠩ᩟"),
  bstack11l11_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠵᩠ࠪ"),
  bstack11l11_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠷ࠫᩡ"),
  bstack11l11_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠹ࠬᩢ"),
  bstack11l11_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠻࠭ᩣ"),
  bstack11l11_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠽ࠧᩤ"),
  bstack11l11_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠸ࠨᩥ"),
  bstack11l11_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠺ࠩᩦ"),
  bstack11l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᩧ"),
  bstack11l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᩨ"),
  bstack11l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᩩ"),
  bstack11l11_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᩪ"),
  bstack11l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᩫ"),
  bstack11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩬ"),
  bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧᩭ"),
  bstack11l11_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧᩮ")
]
bstack111ll11ll1l_opy_ = [
  bstack11l11_opy_ (u"ࠬࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪᩯ"),
  bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᩰ"),
  bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᩱ"),
  bstack11l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᩲ"),
  bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡐࡳ࡫ࡲࡶ࡮ࡺࡹࠨᩳ"),
  bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᩴ"),
  bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡥ࡬࠭᩵"),
  bstack11l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ᩶"),
  bstack11l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᩷"),
  bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᩸"),
  bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᩹"),
  bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ᩺"),
  bstack11l11_opy_ (u"ࠪࡳࡸ࠭᩻"),
  bstack11l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ᩼"),
  bstack11l11_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫ᩽"),
  bstack11l11_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨ᩾"),
  bstack11l11_opy_ (u"ࠧࡳࡧࡪ࡭ࡴࡴ᩿ࠧ"),
  bstack11l11_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪ᪀"),
  bstack11l11_opy_ (u"ࠩࡰࡥࡨ࡮ࡩ࡯ࡧࠪ᪁"),
  bstack11l11_opy_ (u"ࠪࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠧ᪂"),
  bstack11l11_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩ᪃"),
  bstack11l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩ᪄"),
  bstack11l11_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬ᪅"),
  bstack11l11_opy_ (u"ࠧ࡯ࡱࡓࡥ࡬࡫ࡌࡰࡣࡧࡘ࡮ࡳࡥࡰࡷࡷࠫ᪆"),
  bstack11l11_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩ᪇"),
  bstack11l11_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ᪈"),
  bstack11l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ᪉"),
  bstack11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡪࡴࡤࡌࡧࡼࡷࠬ᪊"),
  bstack11l11_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ᪋"),
  bstack11l11_opy_ (u"࠭࡮ࡰࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠪ᪌"),
  bstack11l11_opy_ (u"ࠧࡤࡪࡨࡧࡰ࡛ࡒࡍࠩ᪍"),
  bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᪎"),
  bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡅࡲࡳࡰ࡯ࡥࡴࠩ᪏"),
  bstack11l11_opy_ (u"ࠪࡧࡦࡶࡴࡶࡴࡨࡇࡷࡧࡳࡩࠩ᪐"),
  bstack11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ᪑"),
  bstack11l11_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᪒"),
  bstack11l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࡙ࡩࡷࡹࡩࡰࡰࠪ᪓"),
  bstack11l11_opy_ (u"ࠧ࡯ࡱࡅࡰࡦࡴ࡫ࡑࡱ࡯ࡰ࡮ࡴࡧࠨ᪔"),
  bstack11l11_opy_ (u"ࠨ࡯ࡤࡷࡰ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧ᪕"),
  bstack11l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡎࡲ࡫ࡸ࠭᪖"),
  bstack11l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡌࡨࠬ᪗"),
  bstack11l11_opy_ (u"ࠫࡩ࡫ࡤࡪࡥࡤࡸࡪࡪࡄࡦࡸ࡬ࡧࡪ࠭᪘"),
  bstack11l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡕࡧࡲࡢ࡯ࡶࠫ᪙"),
  bstack11l11_opy_ (u"࠭ࡰࡩࡱࡱࡩࡓࡻ࡭ࡣࡧࡵࠫ᪚"),
  bstack11l11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬ᪛"),
  bstack11l11_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡕࡰࡵ࡫ࡲࡲࡸ࠭᪜"),
  bstack11l11_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧ᪝"),
  bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ᪞"),
  bstack11l11_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨ᪟"),
  bstack11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡇ࡯࡯࡮ࡧࡷࡶ࡮ࡩࠧ᪠"),
  bstack11l11_opy_ (u"࠭ࡶࡪࡦࡨࡳ࡛࠸ࠧ᪡"),
  bstack11l11_opy_ (u"ࠧ࡮࡫ࡧࡗࡪࡹࡳࡪࡱࡱࡍࡳࡹࡴࡢ࡮࡯ࡅࡵࡶࡳࠨ᪢"),
  bstack11l11_opy_ (u"ࠨࡧࡶࡴࡷ࡫ࡳࡴࡱࡖࡩࡷࡼࡥࡳࠩ᪣"),
  bstack11l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨ᪤"),
  bstack11l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡈࡪࡰࠨ᪥"),
  bstack11l11_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫ᪦"),
  bstack11l11_opy_ (u"ࠬࡹࡹ࡯ࡥࡗ࡭ࡲ࡫ࡗࡪࡶ࡫ࡒ࡙ࡖࠧᪧ"),
  bstack11l11_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫ᪨"),
  bstack11l11_opy_ (u"ࠧࡨࡲࡶࡐࡴࡩࡡࡵ࡫ࡲࡲࠬ᪩"),
  bstack11l11_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ᪪"),
  bstack11l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩ᪫"),
  bstack11l11_opy_ (u"ࠪࡪࡴࡸࡣࡦࡅ࡫ࡥࡳ࡭ࡥࡋࡣࡵࠫ᪬"),
  bstack11l11_opy_ (u"ࠫࡽࡳࡳࡋࡣࡵࠫ᪭"),
  bstack11l11_opy_ (u"ࠬࡾ࡭ࡹࡌࡤࡶࠬ᪮"),
  bstack11l11_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬ᪯"),
  bstack11l11_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧ᪰"),
  bstack11l11_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩ᪱"),
  bstack11l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬ᪲"),
  bstack11l11_opy_ (u"ࠪࡥࡵࡶࡖࡦࡴࡶ࡭ࡴࡴࠧ᪳"),
  bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ᪴"),
  bstack11l11_opy_ (u"ࠬࡸࡥࡴ࡫ࡪࡲࡆࡶࡰࠨ᪵"),
  bstack11l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯࡫ࡰࡥࡹ࡯࡯࡯ࡵ᪶ࠪ"),
  bstack11l11_opy_ (u"ࠧࡤࡣࡱࡥࡷࡿ᪷ࠧ"),
  bstack11l11_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹ᪸ࠩ"),
  bstack11l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦ᪹ࠩ"),
  bstack11l11_opy_ (u"ࠪ࡭ࡪ᪺࠭"),
  bstack11l11_opy_ (u"ࠫࡪࡪࡧࡦࠩ᪻"),
  bstack11l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ᪼"),
  bstack11l11_opy_ (u"࠭ࡱࡶࡧࡸࡩ᪽ࠬ"),
  bstack11l11_opy_ (u"ࠧࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ᪾"),
  bstack11l11_opy_ (u"ࠨࡣࡳࡴࡘࡺ࡯ࡳࡧࡆࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ᪿࠩ"),
  bstack11l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡅࡤࡱࡪࡸࡡࡊ࡯ࡤ࡫ࡪࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨᫀ"),
  bstack11l11_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡆࡺࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭᫁"),
  bstack11l11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡋࡱࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧ᫂"),
  bstack11l11_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴ᫃ࠩ"),
  bstack11l11_opy_ (u"࠭ࡲࡦࡵࡨࡶࡻ࡫ࡄࡦࡸ࡬ࡧࡪ᫄࠭"),
  bstack11l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ᫅"),
  bstack11l11_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪ᫆"),
  bstack11l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡤࡷࡸࡩ࡯ࡥࡧࠪ᫇"),
  bstack11l11_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡌࡳࡸࡊࡥࡷ࡫ࡦࡩࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭᫈"),
  bstack11l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡺࡪࡩࡰࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫ᫉"),
  bstack11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡶࡰ࡭ࡧࡓࡥࡾ᫊࠭"),
  bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᫋"),
  bstack11l11_opy_ (u"ࠧࡸࡦ࡬ࡳࡘ࡫ࡲࡷ࡫ࡦࡩࠬᫌ"),
  bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᫍ"),
  bstack11l11_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶࡆࡶࡴࡹࡳࡔ࡫ࡷࡩ࡙ࡸࡡࡤ࡭࡬ࡲ࡬࠭ᫎ"),
  bstack11l11_opy_ (u"ࠪ࡬࡮࡭ࡨࡄࡱࡱࡸࡷࡧࡳࡵࠩ᫏"),
  bstack11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡔࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࡳࠨ᫐"),
  bstack11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨ᫑"),
  bstack11l11_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪ᫒"),
  bstack11l11_opy_ (u"ࠧࡳࡧࡰࡳࡻ࡫ࡉࡐࡕࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࡌࡰࡥࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬ᫓"),
  bstack11l11_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪ᫔"),
  bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᫕"),
  bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬ᫖"),
  bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ᫗"),
  bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᫘"),
  bstack11l11_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩ᫙"),
  bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭᫚"),
  bstack11l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪ᫛"),
  bstack11l11_opy_ (u"ࠩࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡕࡸ࡯࡮ࡲࡷࡆࡪ࡮ࡡࡷ࡫ࡲࡶࠬ᫜")
]
bstack1111lll1ll_opy_ = {
  bstack11l11_opy_ (u"ࠪࡺࠬ᫝"): bstack11l11_opy_ (u"ࠫࡻ࠭᫞"),
  bstack11l11_opy_ (u"ࠬ࡬ࠧ᫟"): bstack11l11_opy_ (u"࠭ࡦࠨ᫠"),
  bstack11l11_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭᫡"): bstack11l11_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧ᫢"),
  bstack11l11_opy_ (u"ࠩࡲࡲࡱࡿࡡࡶࡶࡲࡱࡦࡺࡥࠨ᫣"): bstack11l11_opy_ (u"ࠪࡳࡳࡲࡹࡂࡷࡷࡳࡲࡧࡴࡦࠩ᫤"),
  bstack11l11_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨ᫥"): bstack11l11_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩ᫦"),
  bstack11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩ᫧"): bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ᫨"),
  bstack11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡰࡴࡷࠫ᫩"): bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬ᫪"),
  bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭᫫"): bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧ᫬"),
  bstack11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨ᫭"): bstack11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ᫮"),
  bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨ᫯"): bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡍࡵࡳࡵࠩ᫰"),
  bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪ᫱"): bstack11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫ᫲"),
  bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬ᫳"): bstack11l11_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧ᫴"),
  bstack11l11_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨ᫵"): bstack11l11_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ᫶"),
  bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩ᫷"): bstack11l11_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫ᫸"),
  bstack11l11_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬ᫹"): bstack11l11_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭᫺"),
  bstack11l11_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩ᫻"): bstack11l11_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪࠪ᫼"),
  bstack11l11_opy_ (u"ࠧࡱࡣࡦࡪ࡮ࡲࡥࠨ᫽"): bstack11l11_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ᫾"),
  bstack11l11_opy_ (u"ࠩࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ᫿"): bstack11l11_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᬀ"),
  bstack11l11_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᬁ"): bstack11l11_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᬂ"),
  bstack11l11_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧᬃ"): bstack11l11_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨᬄ"),
  bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᬅ"): bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᬆ"),
  bstack11l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬᬇ"): bstack11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡶࡥࡢࡶࡨࡶࠬᬈ")
}
bstack111lll11l1l_opy_ = bstack11l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡧࡪࡶ࡫ࡹࡧ࠴ࡣࡰ࡯࠲ࡴࡪࡸࡣࡺ࠱ࡦࡰ࡮࠵ࡲࡦ࡮ࡨࡥࡸ࡫ࡳ࠰࡮ࡤࡸࡪࡹࡴ࠰ࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᬉ")
bstack111lll11ll1_opy_ = bstack11l11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠵ࡨࡦࡣ࡯ࡸ࡭ࡩࡨࡦࡥ࡮ࠦᬊ")
bstack1l1l1l1l1_opy_ = bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡧࡧࡷ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡵࡨࡲࡩࡥࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥᬋ")
bstack11l111l1_opy_ = bstack11l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡺࡨ࠴࡮ࡵࡣࠩᬌ")
bstack1l1111ll1_opy_ = bstack11l11_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠬᬍ")
bstack1l11lll11_opy_ = bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠴࠵࠶࠷࠳ࡼࡪ࠯ࡩࡷࡥࠫᬎ")
bstack11l11111l1_opy_ = bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡴࡥࡹࡶࡢ࡬ࡺࡨࡳࠨᬏ")
bstack1ll1lllll1_opy_ = {
  bstack11l11_opy_ (u"ࠬࡪࡥࡧࡣࡸࡰࡹ࠭ᬐ"): bstack11l11_opy_ (u"࠭ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᬑ"),
  bstack11l11_opy_ (u"ࠧࡶࡵ࠰ࡩࡦࡹࡴࠨᬒ"): bstack11l11_opy_ (u"ࠨࡪࡸࡦ࠲ࡻࡳࡦ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᬓ"),
  bstack11l11_opy_ (u"ࠩࡸࡷࠬᬔ"): bstack11l11_opy_ (u"ࠪ࡬ࡺࡨ࠭ࡶࡵ࠰ࡳࡳࡲࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᬕ"),
  bstack11l11_opy_ (u"ࠫࡪࡻࠧᬖ"): bstack11l11_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡨࡹ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᬗ"),
  bstack11l11_opy_ (u"࠭ࡩ࡯ࠩᬘ"): bstack11l11_opy_ (u"ࠧࡩࡷࡥ࠱ࡦࡶࡳ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᬙ"),
  bstack11l11_opy_ (u"ࠨࡣࡸࠫᬚ"): bstack11l11_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡡࡱࡵࡨ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᬛ")
}
bstack111ll1l1l11_opy_ = {
  bstack11l11_opy_ (u"ࠪࡧࡷ࡯ࡴࡪࡥࡤࡰࠬᬜ"): 50,
  bstack11l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᬝ"): 40,
  bstack11l11_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ᬞ"): 30,
  bstack11l11_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᬟ"): 20,
  bstack11l11_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᬠ"): 10
}
bstack11ll111l_opy_ = bstack111ll1l1l11_opy_[bstack11l11_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᬡ")]
bstack11l1l1lll_opy_ = bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᬢ")
bstack11ll1111l_opy_ = bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᬣ")
bstack11l111ll11_opy_ = bstack11l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪᬤ")
bstack1lllllll1l_opy_ = bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᬥ")
bstack11lllll11_opy_ = bstack11l11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡢࡰࡧࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫᬦ")
bstack11l1ll1ll_opy_ = {
  bstack11l11_opy_ (u"ࠧࡔࡆࡎ࠱ࡌࡋࡎ࠮࠲࠳࠹ࠬᬧ"): bstack11l11_opy_ (u"ࠨࠬ࠭࠮ࠥࡡࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࡡࠥࡦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࡡࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡ࡫ࡱࠤࡾࡵࡵࡳࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠮ࠡࡖ࡫࡭ࡸࠦ࡭ࡢࡻࠣࡧࡦࡻࡳࡦࠢࡦࡳࡳ࡬࡬ࡪࡥࡷࡷࠥࡽࡩࡵࡪࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡭ࡹࠦࡵࡴ࡫ࡱ࡫࠿ࠦࡰࡪࡲࠣࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࠡࠬ࠭࠮ࠬᬨ")
}
bstack111ll111ll1_opy_ = [bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪᬩ"), bstack11l11_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪᬪ")]
bstack111ll1ll111_opy_ = [bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧᬫ"), bstack11l11_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧᬬ")]
bstack1llll11l_opy_ = re.compile(bstack11l11_opy_ (u"࠭࡞࡜࡞࡟ࡻ࠲ࡣࠫ࠻࠰࠭ࠨࠬᬭ"))
bstack1llll1l11_opy_ = [
  bstack11l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨᬮ"),
  bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᬯ"),
  bstack11l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᬰ"),
  bstack11l11_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧᬱ"),
  bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨᬲ"),
  bstack11l11_opy_ (u"ࠬࡻࡤࡪࡦࠪᬳ"),
  bstack11l11_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ᬴"),
  bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧᬵ"),
  bstack11l11_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ᬶ"),
  bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧᬷ"),
  bstack11l11_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫᬸ"), bstack11l11_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧᬹ"),
  bstack11l11_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨᬺ"),
  bstack11l11_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬᬻ"),
  bstack11l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫᬼ"),
  bstack11l11_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫᬽ"),
  bstack11l11_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪᬾ"),
  bstack11l11_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨᬿ"), bstack11l11_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨᭀ"), bstack11l11_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧᭁ"), bstack11l11_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧᭂ"), bstack11l11_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩᭃ"),
  bstack11l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ᭄࠭"),
  bstack11l11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ᭅ"),
  bstack11l11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬᭆ"), bstack11l11_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨᭇ"),
  bstack11l11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪᭈ"),
  bstack11l11_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧᭉ"),
  bstack11l11_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ࠭ᭊ"),
  bstack11l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩᭋ"),
  bstack11l11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧᭌ"),
  bstack11l11_opy_ (u"ࠪࡥࡻࡪࠧ᭍"), bstack11l11_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ᭎"), bstack11l11_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧ᭏"), bstack11l11_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧ᭐"),
  bstack11l11_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬ᭑"), bstack11l11_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧ᭒"), bstack11l11_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬ᭓"),
  bstack11l11_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬ᭔"), bstack11l11_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩ᭕"),
  bstack11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧ᭖"), bstack11l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩ᭗"), bstack11l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬ᭘"), bstack11l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪ᭙"), bstack11l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭᭚"),
  bstack11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭᭛"), bstack11l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨ᭜"),
  bstack11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧ᭝"),
  bstack11l11_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫ᭞"),
  bstack11l11_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭᭟"), bstack11l11_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩ᭠"), bstack11l11_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧ᭡"), bstack11l11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᭢"),
  bstack11l11_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩ᭣"),
  bstack11l11_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ᭤"), bstack11l11_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭᭥"),
  bstack11l11_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧ᭦"),
  bstack11l11_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪ᭧"),
  bstack11l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫ᭨"),
  bstack11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᭩"),
  bstack11l11_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬ᭪"),
  bstack11l11_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ᭫"),
  bstack11l11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮᭬ࠧ"),
  bstack11l11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭᭭"),
  bstack11l11_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬ᭮"),
  bstack11l11_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭᭯"),
  bstack11l11_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫ᭰"),
  bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪ᭱"),
  bstack11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ᭲"),
  bstack11l11_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭᭳"),
  bstack11l11_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬ᭴"),
  bstack11l11_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬ᭵"),
  bstack11l11_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩ᭶"),
  bstack11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧ᭷"), bstack11l11_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨ᭸"), bstack11l11_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨ᭹"),
  bstack11l11_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪ᭺"),
  bstack11l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫ᭻"),
  bstack11l11_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪ᭼"),
  bstack11l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫ᭽"),
  bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ᭾"),
  bstack11l11_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨ᭿"),
  bstack11l11_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨᮀ"), bstack11l11_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸࠬᮁ"), bstack11l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠪᮂ"),
  bstack11l11_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨᮃ"),
  bstack11l11_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶࠪᮄ"),
  bstack11l11_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨࠬᮅ"),
  bstack11l11_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫᮆ"),
  bstack11l11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨᮇ"), bstack11l11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨࠬᮈ"),
  bstack11l11_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪᮉ"), bstack11l11_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷࠬᮊ"),
  bstack11l11_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣࠩᮋ"),
  bstack11l11_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩᮌ"),
  bstack11l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧᮍ"), bstack11l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴࠩᮎ"), bstack11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩࠪᮏ"), bstack11l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧᮐ"),
  bstack11l11_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨᮑ"),
  bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪᮒ"),
  bstack11l11_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᮓ"),
  bstack11l11_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫᮔ"),
  bstack11l11_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨࠩᮕ"),
  bstack11l11_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨᮖ"),
  bstack11l11_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨᮗ"), bstack11l11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩᮘ"),
  bstack11l11_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬᮙ"),
  bstack11l11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪᮚ"),
  bstack11l11_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬᮛ"),
  bstack11l11_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬᮜ"),
  bstack11l11_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨᮝ"),
  bstack11l11_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪᮞ"),
  bstack11l11_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩᮟ"),
  bstack11l11_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧࠪᮠ"),
  bstack11l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪᮡ"),
  bstack11l11_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩᮢ"),
  bstack11l11_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪᮣ"),
  bstack11l11_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬᮤ"),
  bstack11l11_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭ᮥ"),
  bstack11l11_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪᮦ"),
  bstack11l11_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫᮧ"),
  bstack11l11_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ࠭ᮨ"),
  bstack11l11_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬᮩ"),
  bstack11l11_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ᮪࠭"),
  bstack11l11_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮᮫ࠪ"),
  bstack11l11_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭ᮬ"),
  bstack11l11_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫᮭ"),
  bstack11l11_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬᮮ"), bstack11l11_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪᮯ"),
  bstack11l11_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨ᮰"), bstack11l11_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭᮱"),
  bstack11l11_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫ᮲"),
  bstack11l11_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪ᮳"),
  bstack11l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪ᮴"),
  bstack11l11_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭᮵"), bstack11l11_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭᮶"),
  bstack11l11_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ᮷"),
  bstack11l11_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪ᮸"),
  bstack11l11_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭᮹"),
  bstack11l11_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨᮺ"),
  bstack11l11_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪᮻ"),
  bstack11l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬᮼ"),
  bstack11l11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨᮽ"),
  bstack11l11_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪᮾ"),
  bstack11l11_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧᮿ"),
  bstack11l11_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬᯀ"), bstack11l11_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫᯁ"),
  bstack11l11_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨᯂ"),
  bstack11l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡌࡨࡑࡵࡣࡢࡶࡲࡶࡆࡻࡴࡰࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠬᯃ")
]
bstack111l111ll_opy_ = bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡸࡴࡱࡵࡡࡥࠩᯄ")
bstack1l1ll11ll1_opy_ = [bstack11l11_opy_ (u"ࠫ࠳ࡧࡰ࡬ࠩᯅ"), bstack11l11_opy_ (u"ࠬ࠴ࡡࡢࡤࠪᯆ"), bstack11l11_opy_ (u"࠭࠮ࡪࡲࡤࠫᯇ")]
bstack11l1111ll_opy_ = [bstack11l11_opy_ (u"ࠧࡪࡦࠪᯈ"), bstack11l11_opy_ (u"ࠨࡲࡤࡸ࡭࠭ᯉ"), bstack11l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬᯊ"), bstack11l11_opy_ (u"ࠪࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥࠩᯋ")]
bstack11ll1l11l1_opy_ = {
  bstack11l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᯌ"): bstack11l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᯍ"),
  bstack11l11_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧᯎ"): bstack11l11_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬᯏ"),
  bstack11l11_opy_ (u"ࠨࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᯐ"): bstack11l11_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᯑ"),
  bstack11l11_opy_ (u"ࠪ࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᯒ"): bstack11l11_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᯓ"),
  bstack11l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡴࡪࡱࡱࡷࠬᯔ"): bstack11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧᯕ")
}
bstack1111llll11_opy_ = [
  bstack11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᯖ"),
  bstack11l11_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᯗ"),
  bstack11l11_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᯘ"),
  bstack11l11_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᯙ"),
  bstack11l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬᯚ"),
]
bstack1l11lll1_opy_ = bstack1l1lllllll_opy_ + bstack111ll11ll1l_opy_ + bstack1llll1l11_opy_
bstack1l11ll1lll_opy_ = [
  bstack11l11_opy_ (u"ࠬࡤ࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵࠦࠪᯛ"),
  bstack11l11_opy_ (u"࠭࡞ࡣࡵ࠰ࡰࡴࡩࡡ࡭࠰ࡦࡳࡲࠪࠧᯜ"),
  bstack11l11_opy_ (u"ࠧ࡟࠳࠵࠻࠳࠭ᯝ"),
  bstack11l11_opy_ (u"ࠨࡠ࠴࠴࠳࠭ᯞ"),
  bstack11l11_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠲࡝࠹࠱࠾ࡣ࠮ࠨᯟ"),
  bstack11l11_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠴࡞࠴࠲࠿࡝࠯ࠩᯠ"),
  bstack11l11_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠶࡟࠵࠳࠱࡞࠰ࠪᯡ"),
  bstack11l11_opy_ (u"ࠬࡤ࠱࠺࠴࠱࠵࠻࠾࠮ࠨᯢ")
]
bstack11l11111l11_opy_ = bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᯣ")
bstack1ll11l1ll_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡦࡸࡨࡲࡹ࠭ᯤ")
bstack1l111l1111_opy_ = [ bstack11l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᯥ") ]
bstack111l1l1l11_opy_ = [ bstack11l11_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᯦") ]
bstack1llll11l11_opy_ = [bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᯧ")]
bstack11l11l1l_opy_ = [ bstack11l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᯨ") ]
bstack11lll1l1l1_opy_ = bstack11l11_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧᯩ")
bstack1lll11lll1_opy_ = bstack11l11_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩᯪ")
bstack111l111111_opy_ = bstack11l11_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫᯫ")
bstack11ll111ll1_opy_ = bstack11l11_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧᯬ")
bstack11ll11l1l1_opy_ = [
  bstack11l11_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭ᯭ"),
  bstack11l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪᯮ"),
  bstack11l11_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬᯯ"),
  bstack11l11_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫᯰ"),
  bstack11l11_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪᯱ"),
  bstack11l11_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨ᯲"),
  bstack11l11_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨ᯳"),
  bstack11l11_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫ᯴"),
  bstack11l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬ᯵"),
  bstack11l11_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ᯶"),
  bstack11l11_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭᯷"),
  bstack11l11_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬ᯸"),
  bstack11l11_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪ᯹"),
  bstack11l11_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ᯺"),
  bstack11l11_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭᯻"),
  bstack11l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ᯼"),
  bstack11l11_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧ᯽"),
  bstack11l11_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ᯾"),
  bstack11l11_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧ᯿"),
  bstack11l11_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ᰀ"),
  bstack11l11_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᰁ"),
]
bstack1lll1ll1ll_opy_ = bstack11l11_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧᰂ")
bstack11l1111111_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠪࢂࠬᰃ")), bstack11l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᰄ"), bstack11l11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᰅ"))
bstack11l11ll1l11_opy_ = bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵ࡯ࠧᰆ")
bstack111ll1lllll_opy_ = [ bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᰇ"), bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᰈ"), bstack11l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨᰉ"), bstack11l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᰊ")]
bstack11l1111l_opy_ = [ bstack11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᰋ"), bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᰌ"), bstack11l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬᰍ"), bstack11l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᰎ") ]
bstack1l1l111l11_opy_ = [ bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᰏ") ]
bstack111ll111l1l_opy_ = [ bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᰐ") ]
bstack1l1l1l11l1_opy_ = 360
bstack11l11111111_opy_ = bstack11l11_opy_ (u"ࠥࡥࡵࡶ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥᰑ")
bstack111ll1lll1l_opy_ = bstack11l11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡩࡴࡵࡸࡩࡸࠨᰒ")
bstack111ll1l1l1l_opy_ = bstack11l11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠣᰓ")
bstack11l11l1ll1l_opy_ = bstack11l11_opy_ (u"ࠨࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡵࡧࡶࡸࡸࠦࡡࡳࡧࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦ࡯࡯ࠢࡒࡗࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࠥࡴࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩࠥ࡬࡯ࡳࠢࡄࡲࡩࡸ࡯ࡪࡦࠣࡨࡪࡼࡩࡤࡧࡶ࠲ࠧᰔ")
bstack11l111lll1l_opy_ = bstack11l11_opy_ (u"ࠢ࠲࠳࠱࠴ࠧᰕ")
bstack1111111ll1_opy_ = {
  bstack11l11_opy_ (u"ࠨࡒࡄࡗࡘ࠭ᰖ"): bstack11l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᰗ"),
  bstack11l11_opy_ (u"ࠪࡊࡆࡏࡌࠨᰘ"): bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᰙ"),
  bstack11l11_opy_ (u"࡙ࠬࡋࡊࡒࠪᰚ"): bstack11l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᰛ")
}
bstack111lll1lll_opy_ = [
  bstack11l11_opy_ (u"ࠢࡨࡧࡷࠦᰜ"),
  bstack11l11_opy_ (u"ࠣࡩࡲࡆࡦࡩ࡫ࠣᰝ"),
  bstack11l11_opy_ (u"ࠤࡪࡳࡋࡵࡲࡸࡣࡵࡨࠧᰞ"),
  bstack11l11_opy_ (u"ࠥࡶࡪ࡬ࡲࡦࡵ࡫ࠦᰟ"),
  bstack11l11_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥᰠ"),
  bstack11l11_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᰡ"),
  bstack11l11_opy_ (u"ࠨࡳࡶࡤࡰ࡭ࡹࡋ࡬ࡦ࡯ࡨࡲࡹࠨᰢ"),
  bstack11l11_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦᰣ"),
  bstack11l11_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦᰤ"),
  bstack11l11_opy_ (u"ࠤࡦࡰࡪࡧࡲࡆ࡮ࡨࡱࡪࡴࡴࠣᰥ"),
  bstack11l11_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࡶࠦᰦ"),
  bstack11l11_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠦᰧ"),
  bstack11l11_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࡇࡳࡺࡰࡦࡗࡨࡸࡩࡱࡶࠥᰨ"),
  bstack11l11_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧᰩ"),
  bstack11l11_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᰪ"),
  bstack11l11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡖࡲࡹࡨ࡮ࡁࡤࡶ࡬ࡳࡳࠨᰫ"),
  bstack11l11_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡐࡹࡱࡺࡩࡕࡱࡸࡧ࡭ࠨᰬ"),
  bstack11l11_opy_ (u"ࠥࡷ࡭ࡧ࡫ࡦࠤᰭ"),
  bstack11l11_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡄࡴࡵࠨᰮ")
]
bstack111lll11l11_opy_ = [
  bstack11l11_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦᰯ"),
  bstack11l11_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᰰ"),
  bstack11l11_opy_ (u"ࠢࡢࡷࡷࡳࠧᰱ"),
  bstack11l11_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣᰲ"),
  bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᰳ")
]
bstack1lll11ll1_opy_ = {
  bstack11l11_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤᰴ"): [bstack11l11_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥᰵ")],
  bstack11l11_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᰶ"): [bstack11l11_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶ᰷ࠥ")],
  bstack11l11_opy_ (u"ࠢࡢࡷࡷࡳࠧ᰸"): [bstack11l11_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ᰹"), bstack11l11_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧ᰺"), bstack11l11_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢ᰻"), bstack11l11_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ᰼")],
  bstack11l11_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧ᰽"): [bstack11l11_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨ᰾")],
  bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ᰿"): [bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ᱀")],
}
bstack111ll1l111l_opy_ = {
  bstack11l11_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣ᱁"): bstack11l11_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤ᱂"),
  bstack11l11_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣ᱃"): bstack11l11_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ᱄"),
  bstack11l11_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥ᱅"): bstack11l11_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࠤ᱆"),
  bstack11l11_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦ᱇"): bstack11l11_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦ᱈"),
  bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ᱉"): bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᱊")
}
bstack1lllll1llll_opy_ = {
  bstack11l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ᱋"): bstack11l11_opy_ (u"࠭ࡓࡶ࡫ࡷࡩ࡙ࠥࡥࡵࡷࡳࠫ᱌"),
  bstack11l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᱍ"): bstack11l11_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩᱎ"),
  bstack11l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᱏ"): bstack11l11_opy_ (u"ࠪࡘࡪࡹࡴࠡࡕࡨࡸࡺࡶࠧ᱐"),
  bstack11l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ᱑"): bstack11l11_opy_ (u"࡚ࠬࡥࡴࡶࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬ᱒")
}
bstack111ll11l1l1_opy_ = 65536
bstack111lll1ll11_opy_ = bstack11l11_opy_ (u"࠭࠮࠯࠰࡞ࡘࡗ࡛ࡎࡄࡃࡗࡉࡉࡣࠧ᱓")
bstack111ll1ll1l1_opy_ = [
      bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᱔"), bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᱕"), bstack11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᱖"), bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᱗"), bstack11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭᱘"),
      bstack11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ᱙"), bstack11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩᱚ"), bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᱛ"), bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᱜ"),
      bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᱝ"), bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᱞ"), bstack11l11_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᱟ")
    ]
bstack111lll1ll1l_opy_= {
  bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᱠ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᱡ"),
  bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᱢ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᱣ"),
  bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᱤ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᱥ"),
  bstack11l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᱦ"): bstack11l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᱧ"),
  bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᱨ"): bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᱩ"),
  bstack11l11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᱪ"): bstack11l11_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᱫ"),
  bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᱬ"): bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᱭ"),
  bstack11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᱮ"): bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᱯ"),
  bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᱰ"): bstack11l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᱱ"),
  bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧᱲ"): bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨᱳ"),
  bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᱴ"): bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᱵ"),
  bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭ᱶ"): bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧᱷ"),
  bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᱸ"): bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᱹ"),
  bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࡒࡴࡹ࡯࡯࡯ࡵࠪᱺ"): bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫᱻ"),
  bstack11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧᱼ"): bstack11l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨᱽ"),
  bstack11l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᱾"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᱿"),
  bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᲀ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᲁ"),
  bstack11l11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᲂ"): bstack11l11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᲃ"),
  bstack11l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᲄ"): bstack11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᲅ"),
  bstack11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᲆ"): bstack11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᲇ"),
  bstack11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ᲈ"): bstack11l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᲉ"),
  bstack11l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᲊ"): bstack11l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ᲋"),
  bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᲌"): bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᲍"),
  bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᲎"): bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᲏"),
  bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᲐ"): bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᲑ"),
  bstack11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᲒ"): bstack11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫᲓ"),
  bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᲔ"): bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭Ვ"),
  bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪᲖ"): bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᲗ")
}
bstack111lll1l11l_opy_ = [bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᲘ"), bstack11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᲙ")]
bstack1l1lll1l1_opy_ = (bstack11l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᲚ"),)
bstack111lll1l1ll_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡷࡳࡨࡦࡺࡥࡠࡥ࡯࡭ࠬᲛ")
bstack1l11111l1_opy_ = bstack11l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠲ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠱ࡹ࠵࠴࡭ࡲࡪࡦࡶ࠳ࠧᲜ")
bstack1l1ll1111_opy_ = bstack11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬ࡸࡩࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࠤᲝ")
bstack111l1l1111_opy_ = bstack11l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠭ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠧᲞ")
class EVENTS(Enum):
  bstack111ll1l11l1_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩᲟ")
  bstack111l11l11l_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳࠫᲠ")
  bstack1ll11l1lll_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡢ࡮࡬ࡾࡪ࠭Ს")
  bstack111ll11l11l_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࡯ࡳ࡬ࡹࠧᲢ")
  bstack1l1111lll1_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬᲣ") #shift post bstack111lll1l111_opy_
  bstack111l1ll11_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮ࠫᲤ") #shift post bstack111lll1l111_opy_
  bstack111ll11l1ll_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡮ࡵࡣࠩᲥ") #shift
  bstack111ll11ll11_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪᲦ") #shift
  bstack11l1l111_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨᲧ")
  bstack1l1l1l11lll_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡶࡥࡻ࡫࠭ࡳࡧࡶࡹࡱࡺࡳࠨᲨ")
  bstack11ll1l1lll_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡴࡪࡸࡦࡰࡴࡰࡷࡨࡧ࡮ࠨᲩ")
  bstack1l1111l11l_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡮ࡲࡧࡦࡲࠧᲪ") #shift
  bstack111l1ll1_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡡࡱࡲ࠰ࡹࡵࡲ࡯ࡢࡦࠪᲫ") #shift
  bstack1l1llll11l_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡧ࡮࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠩᲬ")
  bstack1llll1ll11_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭Ჭ") #shift
  bstack111ll1l11_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭Ხ") #shift
  bstack111ll1ll1ll_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻࠪᲯ") #shift
  bstack1l111l11l1l_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᲰ")
  bstack111lll1111_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡶࡸࡦࡺࡵࡴࠩᲱ") #shift
  bstack1lll1111l1_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪᲲ")
  bstack111ll1ll11l_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡽࡿ࠭ࡴࡧࡷࡹࡵ࠭Ჳ") #shift
  bstack11lllll1ll_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡹࡻࡰࠨᲴ")
  bstack111ll11l111_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡲࡦࡶࡳࡩࡱࡷࠫᲵ") # not bstack111lll111ll_opy_ in python
  bstack1lll11l1l1_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡶࡻࡩࡵࠩᲶ") # used in bstack111lll1111l_opy_
  bstack11l1l1l1l11_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶࡲࡦ࠯ࡴࡹ࡮ࡺࠧᲷ")
  bstack11l1l1ll1ll_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱ࡶࡻࡩࡵࠩᲸ")
  bstack1lll11111_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡨࡧࡷࠫᲹ") # used in bstack111lll1111l_opy_
  bstack11l1llllll_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡪࡲࡳࡰ࠭Ჺ")
  bstack11l1ll1111l_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡨࡰࡱ࡮ࠫ᲻")
  bstack11l1ll11ll1_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡪࡲࡳࡰ࠭᲼")
  bstack1lllllll11_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠬᲽ")
  bstack1111lll11l_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠬᲾ") #
  bstack1ll111lll_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡹࡧ࡫ࡦࡕࡦࡶࡪ࡫࡮ࡔࡪࡲࡸࠬᲿ")
  bstack11l11111_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬ᳀")
  bstack11lll1l11l_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡩ࠲ࡺࡥࡴࡶࠪ᳁")
  bstack111ll111l_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡳࡸࡺ࠭ࡵࡧࡶࡸࠬ᳂")
  bstack1l1l11ll1_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡷ࡫࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨ᳃") #shift
  bstack1l1l1ll11_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪ᳄") #shift
  bstack111ll11lll1_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫ᳅")
  bstack111lll11lll_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡫ࡧࡰࡪ࠳ࡴࡪ࡯ࡨࡳࡺࡺࠧ᳆")
  bstack1lll1lll1l_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡦࡺ࡬ࡸ࠲࡮ࡡ࡯ࡦ࡯ࡩࡷ࠭᳇")
  bstack1ll111ll11l_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿࡫ࡸࡪࡶ࠰࡬ࡦࡴࡤ࡭ࡧࡵࠫ᳈")
  bstack111ll11llll_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࠭࡮ࡧࡷࡶ࡮ࡩࡳࠨ᳉")
  bstack111lll11111_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡩࡷࡥ࠾ࡸࡺ࡯ࡱࠩ᳊")
  bstack1l1lll11ll1_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡵࡷࡥࡷࡺࠧ᳋")
  bstack111ll1l1111_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡧࡳࡼࡴ࡬ࡰࡣࡧࠫ᳌")
  bstack111lll111l1_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡧ࡭࡫ࡣ࡬࠯ࡸࡴࡩࡧࡴࡦࠩ᳍")
  bstack1ll11l1l11l_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡣࡱࡲࡸࡸࡺࡲࡢࡲࠪ᳎")
  bstack1l1ll1ll1ll_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡵࡷࡥࡷࡺࡢࡪࡰࡤࡶࡾ࠭᳏")
  bstack1l1lll1111l_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡦࡳࡳࡴࡥࡤࡶࠪ᳐")
  bstack1ll11l1llll_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡷࡹࡵࡰࠨ᳑")
  bstack1ll1l11111l_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡸࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭᳒")
  bstack1l1ll1lll1l_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩ᳓")
  bstack111ll1l1ll1_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶ᳔ࠪ")
  bstack111ll1lll11_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡨࡓ࡫ࡡࡳࡧࡶࡸࡍࡻࡢࠨ᳕")
  bstack11lllll1l1l_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡉ࡯࡫ࡷ᳖ࠫ")
  bstack11lll1ll11l_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡶࡹ᳗࠭")
  bstack1l1ll11l1l1_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡆࡳࡳ࡬ࡩࡨ᳘ࠩ")
  bstack111ll1l1lll_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩ᳙ࠪ")
  bstack1l11llllll1_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡩࡔࡧ࡯ࡪࡍ࡫ࡡ࡭ࡕࡷࡩࡵ࠭᳚")
  bstack1l1l1111ll1_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡊࡩࡹࡘࡥࡴࡷ࡯ࡸࠬ᳛")
  bstack1l11l1l111l_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡅࡷࡧࡱࡸ᳜ࠬ")
  bstack1l11ll11ll1_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷ᳝ࠫ")
  bstack1l11l1l1lll_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡬ࡰࡩࡆࡶࡪࡧࡴࡦࡦࡈࡺࡪࡴࡴࠨ᳞")
  bstack111ll1l11ll_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡦࡰࡴࡹࡪࡻࡥࡕࡧࡶࡸࡊࡼࡥ࡯ࡶ᳟ࠪ")
  bstack11lll1l11l1_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡴࡶࠧ᳠")
  bstack1ll1l11l111_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࡮ࡔࡶࡲࡴࠬ᳡")
  bstack11l1l1111ll_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࡕࡱ࡮ࡲࡥࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ᳢ࠪ")
  bstack111l11l1l_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡱࡨࡋࡻ࡮࡯ࡧ࡯ࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦ᳣ࠪ")
  bstack11lllllll_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡌࡵ࡯ࡰࡨࡰ࡙࡫ࡳࡵࡅࡲࡱࡵࡲࡥࡵࡧࡧ᳤ࠫ")
  bstack1lll1l1ll1l_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡴࡵࡲࡹࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡐࡺࡶࡨࡷࡹ᳥࠭")
  bstack1llll11l111_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡳࡑࡻࡷࡩࡸࡺ᳦ࠧ")
  bstack1llll1l111l_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡿࡴࡦࡵࡷࡋࡪࡺࡔࡰࡶࡤࡰ࡙࡫ࡳࡵࡵ᳧ࠪ")
class STAGE(Enum):
  bstack111l1ll11l_opy_ = bstack11l11_opy_ (u"ࠨࡵࡷࡥࡷࡺ᳨ࠧ")
  END = bstack11l11_opy_ (u"ࠩࡨࡲࡩ࠭ᳩ")
  bstack111ll11l1_opy_ = bstack11l11_opy_ (u"ࠪࡷ࡮ࡴࡧ࡭ࡧࠪᳪ")
bstack1l1ll11l1_opy_ = {
  bstack11l11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࠫᳫ"): bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᳬ"),
  bstack11l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆ᳭ࠪ"): bstack11l11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᳮ")
}
PLAYWRIGHT_HUB_URL = bstack11l11_opy_ (u"ࠣࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠥᳯ")
bstack1l1l1ll111l_opy_ = 98
bstack1l1ll111lll_opy_ = 100
bstack1lll1ll1l1l_opy_ = {
  bstack11l11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࠨᳰ"): bstack11l11_opy_ (u"ࠪ࠱࠲ࡸࡥࡳࡷࡱࡷࠬᳱ"),
  bstack11l11_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪᳲ"): bstack11l11_opy_ (u"ࠬ࠳࠭ࡳࡧࡵࡹࡳࡹ࠭ࡥࡧ࡯ࡥࡾ࠭ᳳ"),
  bstack11l11_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫ᳴"): 0
}
bstack111ll111lll_opy_ = bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᳵ")
bstack111lll1l1l1_opy_ = bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡸࡴࡱࡵࡡࡥ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧᳶ")
bstack1lllll1lll_opy_ = bstack11l11_opy_ (u"ࠤࡗࡉࡘ࡚ࠠࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠣࡅࡓࡊࠠࡂࡐࡄࡐ࡞࡚ࡉࡄࡕࠥ᳷")