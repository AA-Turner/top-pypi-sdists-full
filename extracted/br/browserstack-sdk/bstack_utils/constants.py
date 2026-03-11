# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import re
from enum import Enum
bstack1l11ll111l_opy_ = {
  bstack1ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ⊗"): bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࠬ⊘"),
  bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ⊙"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡮ࡩࡾ࠭⊚"),
  bstack1ll111_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ⊛"): bstack1ll111_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⊜"),
  bstack1ll111_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭⊝"): bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧ⊞"),
  bstack1ll111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭⊟"): bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࠪ⊠"),
  bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⊡"): bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪ⊢"),
  bstack1ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⊣"): bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⊤"),
  bstack1ll111_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭⊥"): bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠭⊦"),
  bstack1ll111_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧ⊧"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡳࡹ࡯࡭ࡧࠪ⊨"),
  bstack1ll111_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩ⊩"): bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࠩ⊪"),
  bstack1ll111_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪ⊫"): bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪ⊬"),
  bstack1ll111_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧ⊭"): bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡸ࡬ࡨࡪࡵࠧ⊮"),
  bstack1ll111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩ⊯"): bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩ⊰"),
  bstack1ll111_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬ⊱"): bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬ⊲"),
  bstack1ll111_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬ⊳"): bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬ⊴"),
  bstack1ll111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫ⊵"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫ⊶"),
  bstack1ll111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⊷"): bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⊸"),
  bstack1ll111_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬ⊹"): bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬ⊺"),
  bstack1ll111_opy_ (u"ࠨ࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭⊻"): bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡫ࡧࡰࡪ࡚ࡩ࡮ࡧࡲࡹࡹ࠭⊼"),
  bstack1ll111_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪ⊽"): bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪ⊾"),
  bstack1ll111_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾࡹࠧ⊿"): bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡯ࡦࡎࡩࡾࡹࠧ⋀"),
  bstack1ll111_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩ⋁"): bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡷࡷࡳ࡜ࡧࡩࡵࠩ⋂"),
  bstack1ll111_opy_ (u"ࠩ࡫ࡳࡸࡺࡳࠨ⋃"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡳࠨ⋄"),
  bstack1ll111_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬ⋅"): bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧ࡬ࡣࡢࡥ࡫ࡩࠬ⋆"),
  bstack1ll111_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧ⋇"): bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧ⋈"),
  bstack1ll111_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫ⋉"): bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫ⋊"),
  bstack1ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ⋋"): bstack1ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ⋌"),
  bstack1ll111_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ⋍"): bstack1ll111_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫ⋎"),
  bstack1ll111_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ⋏"): bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⋐"),
  bstack1ll111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩ⋑"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩ⋒"),
  bstack1ll111_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬ⋓"): bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬ⋔"),
  bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬ⋕"): bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨ⋖"),
  bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⋗"): bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⋘"),
  bstack1ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ⋙"): bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡴࡻࡲࡤࡧࠪ⋚"),
  bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⋛"): bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⋜"),
  bstack1ll111_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩ⋝"): bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡓࡧ࡭ࡦࠩ⋞"),
  bstack1ll111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬ⋟"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬ⋠"),
  bstack1ll111_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨ⋡"): bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨ⋢"),
  bstack1ll111_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫ⋣"): bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫ⋤"),
  bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ⋥"): bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ⋦"),
  bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⋧"): bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⋨")
}
bstack1ll1ll1l1l11_opy_ = [
  bstack1ll111_opy_ (u"ࠬࡵࡳࠨ⋩"),
  bstack1ll111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ⋪"),
  bstack1ll111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ⋫"),
  bstack1ll111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⋬"),
  bstack1ll111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭⋭"),
  bstack1ll111_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ⋮"),
  bstack1ll111_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ⋯"),
]
bstack111ll1ll1_opy_ = {
  bstack1ll111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ⋰"): [bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ⋱"), bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡓࡇࡍࡆࠩ⋲")],
  bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ⋳"): bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ⋴"),
  bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⋵"): bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠧ⋶"),
  bstack1ll111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ⋷"): bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠫ⋸"),
  bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⋹"): bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ⋺"),
  bstack1ll111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⋻"): bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡗࡤࡖࡅࡓࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫ⋼"),
  bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⋽"): bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࠪ⋾"),
  bstack1ll111_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪ⋿"): bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ⌀"),
  bstack1ll111_opy_ (u"ࠨࡣࡳࡴࠬ⌁"): [bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡓࡔࡤࡏࡄࠨ⌂"), bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕ࠭⌃")],
  bstack1ll111_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭⌄"): bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡎࡒࡋࡑࡋࡖࡆࡎࠪ⌅"),
  bstack1ll111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⌆"): bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ⌇"),
  bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⌈"): [bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞࠭⌉"), bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ⌊")],
  bstack1ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⌋"): bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙࡛ࡒࡃࡑࡖࡇࡆࡒࡅࠨ⌌"),
  bstack1ll111_opy_ (u"࠭ࡳ࡮ࡣࡵࡸࡘ࡫࡬ࡦࡥࡷ࡭ࡴࡴࡆࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࡫ࡳࡆࡐ࡙ࠫ⌍"): bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡏࡓࡅࡋࡉࡘ࡚ࡒࡂࡖࡌࡓࡓࡥࡓࡎࡃࡕࡘࡤ࡙ࡅࡍࡇࡆࡘࡎࡕࡎࡠࡈࡈࡅ࡙࡛ࡒࡆࡡࡅࡖࡆࡔࡃࡉࡇࡖࠫ⌎")
}
bstack1l11ll11ll_opy_ = {
  bstack1ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ⌏"): [bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫ⌐"), bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ⌑")],
  bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ⌒"): [bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡣࡰ࡫ࡹࠨ⌓"), bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ⌔")],
  bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ⌕"): bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ⌖"),
  bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⌗"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⌘"),
  bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⌙"): bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⌚"),
  bstack1ll111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⌛"): [bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡱࡲࠪ⌜"), bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⌝")],
  bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⌞"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ⌟"),
  bstack1ll111_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ⌠"): bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ⌡"),
  bstack1ll111_opy_ (u"࠭ࡡࡱࡲࠪ⌢"): bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲࠪ⌣"),
  bstack1ll111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ⌤"): bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ⌥"),
  bstack1ll111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ⌦"): bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ⌧"),
  bstack1ll111_opy_ (u"ࠧࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡃࡍࡋࠥ⌨"): bstack1ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࡶࡱࡦࡸࡴࡔࡧ࡯ࡩࡨࡺࡩࡰࡰࡉࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࡧࡶࠦ〈"),
}
bstack1111llll_opy_ = {
  bstack1ll111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ〉"): bstack1ll111_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⌫"),
  bstack1ll111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ⌬"): [bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⌭"), bstack1ll111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⌮")],
  bstack1ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⌯"): bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⌰"),
  bstack1ll111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ⌱"): bstack1ll111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ⌲"),
  bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ⌳"): [bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ⌴"), bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ⌵")],
  bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⌶"): bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⌷"),
  bstack1ll111_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ⌸"): bstack1ll111_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭⌹"),
  bstack1ll111_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ⌺"): [bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⌻"), bstack1ll111_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⌼")],
  bstack1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫ⌽"): [bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧ⌾"), bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࠧ⌿")]
}
bstack111l111lll_opy_ = [
  bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧ⍀"),
  bstack1ll111_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬ⍁"),
  bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ⍂"),
  bstack1ll111_opy_ (u"ࠫࡸ࡫ࡴࡘ࡫ࡱࡨࡴࡽࡒࡦࡥࡷࠫ⍃"),
  bstack1ll111_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧ⍄"),
  bstack1ll111_opy_ (u"࠭ࡳࡵࡴ࡬ࡧࡹࡌࡩ࡭ࡧࡌࡲࡹ࡫ࡲࡢࡥࡷࡥࡧ࡯࡬ࡪࡶࡼࠫ⍅"),
  bstack1ll111_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪ⍆"),
  bstack1ll111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭⍇"),
  bstack1ll111_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ⍈"),
  bstack1ll111_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ⍉"),
  bstack1ll111_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⍊"),
  bstack1ll111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭⍋"),
]
bstack1ll111lll_opy_ = [
  bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⍌"),
  bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ⍍"),
  bstack1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ⍎"),
  bstack1ll111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⍏"),
  bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⍐"),
  bstack1ll111_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭⍑"),
  bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⍒"),
  bstack1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⍓"),
  bstack1ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⍔"),
  bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭⍕"),
  bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⍖"),
  bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪ⍗"),
  bstack1ll111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭⍘"),
  bstack1ll111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡙ࡧࡧࠨ⍙"),
  bstack1ll111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⍚"),
  bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⍛"),
  bstack1ll111_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ⍜"),
  bstack1ll111_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠱ࠨ⍝"),
  bstack1ll111_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠳ࠩ⍞"),
  bstack1ll111_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠵ࠪ⍟"),
  bstack1ll111_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠷ࠫ⍠"),
  bstack1ll111_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠹ࠬ⍡"),
  bstack1ll111_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠻࠭⍢"),
  bstack1ll111_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠽ࠧ⍣"),
  bstack1ll111_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠸ࠨ⍤"),
  bstack1ll111_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠺ࠩ⍥"),
  bstack1ll111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⍦"),
  bstack1ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫ⍧"),
  bstack1ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ⍨"),
  bstack1ll111_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ⍩"),
  bstack1ll111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⍪"),
  bstack1ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭⍫"),
  bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ⍬"),
  bstack1ll111_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧ⍭")
]
bstack1ll1ll1l1ll1_opy_ = [
  bstack1ll111_opy_ (u"ࠬࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪ⍮"),
  bstack1ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ⍯"),
  bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ⍰"),
  bstack1ll111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⍱"),
  bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺࡐࡳ࡫ࡲࡶ࡮ࡺࡹࠨ⍲"),
  bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⍳"),
  bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡥ࡬࠭⍴"),
  bstack1ll111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ⍵"),
  bstack1ll111_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⍶"),
  bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ⍷"),
  bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⍸"),
  bstack1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ⍹"),
  bstack1ll111_opy_ (u"ࠪࡳࡸ࠭⍺"),
  bstack1ll111_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ⍻"),
  bstack1ll111_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫ⍼"),
  bstack1ll111_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨ⍽"),
  bstack1ll111_opy_ (u"ࠧࡳࡧࡪ࡭ࡴࡴࠧ⍾"),
  bstack1ll111_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪ⍿"),
  bstack1ll111_opy_ (u"ࠩࡰࡥࡨ࡮ࡩ࡯ࡧࠪ⎀"),
  bstack1ll111_opy_ (u"ࠪࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠧ⎁"),
  bstack1ll111_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩ⎂"),
  bstack1ll111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩ⎃"),
  bstack1ll111_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬ⎄"),
  bstack1ll111_opy_ (u"ࠧ࡯ࡱࡓࡥ࡬࡫ࡌࡰࡣࡧࡘ࡮ࡳࡥࡰࡷࡷࠫ⎅"),
  bstack1ll111_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩ⎆"),
  bstack1ll111_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ⎇"),
  bstack1ll111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⎈"),
  bstack1ll111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡪࡴࡤࡌࡧࡼࡷࠬ⎉"),
  bstack1ll111_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ⎊"),
  bstack1ll111_opy_ (u"࠭࡮ࡰࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠪ⎋"),
  bstack1ll111_opy_ (u"ࠧࡤࡪࡨࡧࡰ࡛ࡒࡍࠩ⎌"),
  bstack1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⎍"),
  bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡅࡲࡳࡰ࡯ࡥࡴࠩ⎎"),
  bstack1ll111_opy_ (u"ࠪࡧࡦࡶࡴࡶࡴࡨࡇࡷࡧࡳࡩࠩ⎏"),
  bstack1ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ⎐"),
  bstack1ll111_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ⎑"),
  bstack1ll111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࡙ࡩࡷࡹࡩࡰࡰࠪ⎒"),
  bstack1ll111_opy_ (u"ࠧ࡯ࡱࡅࡰࡦࡴ࡫ࡑࡱ࡯ࡰ࡮ࡴࡧࠨ⎓"),
  bstack1ll111_opy_ (u"ࠨ࡯ࡤࡷࡰ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧ⎔"),
  bstack1ll111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡎࡲ࡫ࡸ࠭⎕"),
  bstack1ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡌࡨࠬ⎖"),
  bstack1ll111_opy_ (u"ࠫࡩ࡫ࡤࡪࡥࡤࡸࡪࡪࡄࡦࡸ࡬ࡧࡪ࠭⎗"),
  bstack1ll111_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡕࡧࡲࡢ࡯ࡶࠫ⎘"),
  bstack1ll111_opy_ (u"࠭ࡰࡩࡱࡱࡩࡓࡻ࡭ࡣࡧࡵࠫ⎙"),
  bstack1ll111_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬ⎚"),
  bstack1ll111_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡕࡰࡵ࡫ࡲࡲࡸ࠭⎛"),
  bstack1ll111_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧ⎜"),
  bstack1ll111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ⎝"),
  bstack1ll111_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨ⎞"),
  bstack1ll111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡇ࡯࡯࡮ࡧࡷࡶ࡮ࡩࠧ⎟"),
  bstack1ll111_opy_ (u"࠭ࡶࡪࡦࡨࡳ࡛࠸ࠧ⎠"),
  bstack1ll111_opy_ (u"ࠧ࡮࡫ࡧࡗࡪࡹࡳࡪࡱࡱࡍࡳࡹࡴࡢ࡮࡯ࡅࡵࡶࡳࠨ⎡"),
  bstack1ll111_opy_ (u"ࠨࡧࡶࡴࡷ࡫ࡳࡴࡱࡖࡩࡷࡼࡥࡳࠩ⎢"),
  bstack1ll111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨ⎣"),
  bstack1ll111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡈࡪࡰࠨ⎤"),
  bstack1ll111_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫ⎥"),
  bstack1ll111_opy_ (u"ࠬࡹࡹ࡯ࡥࡗ࡭ࡲ࡫ࡗࡪࡶ࡫ࡒ࡙ࡖࠧ⎦"),
  bstack1ll111_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫ⎧"),
  bstack1ll111_opy_ (u"ࠧࡨࡲࡶࡐࡴࡩࡡࡵ࡫ࡲࡲࠬ⎨"),
  bstack1ll111_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ⎩"),
  bstack1ll111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩ⎪"),
  bstack1ll111_opy_ (u"ࠪࡪࡴࡸࡣࡦࡅ࡫ࡥࡳ࡭ࡥࡋࡣࡵࠫ⎫"),
  bstack1ll111_opy_ (u"ࠫࡽࡳࡳࡋࡣࡵࠫ⎬"),
  bstack1ll111_opy_ (u"ࠬࡾ࡭ࡹࡌࡤࡶࠬ⎭"),
  bstack1ll111_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬ⎮"),
  bstack1ll111_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧ⎯"),
  bstack1ll111_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩ⎰"),
  bstack1ll111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬ⎱"),
  bstack1ll111_opy_ (u"ࠪࡥࡵࡶࡖࡦࡴࡶ࡭ࡴࡴࠧ⎲"),
  bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ⎳"),
  bstack1ll111_opy_ (u"ࠬࡸࡥࡴ࡫ࡪࡲࡆࡶࡰࠨ⎴"),
  bstack1ll111_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯࡫ࡰࡥࡹ࡯࡯࡯ࡵࠪ⎵"),
  bstack1ll111_opy_ (u"ࠧࡤࡣࡱࡥࡷࡿࠧ⎶"),
  bstack1ll111_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ⎷"),
  bstack1ll111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ⎸"),
  bstack1ll111_opy_ (u"ࠪ࡭ࡪ࠭⎹"),
  bstack1ll111_opy_ (u"ࠫࡪࡪࡧࡦࠩ⎺"),
  bstack1ll111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ⎻"),
  bstack1ll111_opy_ (u"࠭ࡱࡶࡧࡸࡩࠬ⎼"),
  bstack1ll111_opy_ (u"ࠧࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ⎽"),
  bstack1ll111_opy_ (u"ࠨࡣࡳࡴࡘࡺ࡯ࡳࡧࡆࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠩ⎾"),
  bstack1ll111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡅࡤࡱࡪࡸࡡࡊ࡯ࡤ࡫ࡪࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨ⎿"),
  bstack1ll111_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡆࡺࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭⏀"),
  bstack1ll111_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡋࡱࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧ⏁"),
  bstack1ll111_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࠩ⏂"),
  bstack1ll111_opy_ (u"࠭ࡲࡦࡵࡨࡶࡻ࡫ࡄࡦࡸ࡬ࡧࡪ࠭⏃"),
  bstack1ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ⏄"),
  bstack1ll111_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪ⏅"),
  bstack1ll111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡤࡷࡸࡩ࡯ࡥࡧࠪ⏆"),
  bstack1ll111_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡌࡳࡸࡊࡥࡷ࡫ࡦࡩࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭⏇"),
  bstack1ll111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡺࡪࡩࡰࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫ⏈"),
  bstack1ll111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡶࡰ࡭ࡧࡓࡥࡾ࠭⏉"),
  bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ⏊"),
  bstack1ll111_opy_ (u"ࠧࡸࡦ࡬ࡳࡘ࡫ࡲࡷ࡫ࡦࡩࠬ⏋"),
  bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⏌"),
  bstack1ll111_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶࡆࡶࡴࡹࡳࡔ࡫ࡷࡩ࡙ࡸࡡࡤ࡭࡬ࡲ࡬࠭⏍"),
  bstack1ll111_opy_ (u"ࠪ࡬࡮࡭ࡨࡄࡱࡱࡸࡷࡧࡳࡵࠩ⏎"),
  bstack1ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡔࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࡳࠨ⏏"),
  bstack1ll111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨ⏐"),
  bstack1ll111_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪ⏑"),
  bstack1ll111_opy_ (u"ࠧࡳࡧࡰࡳࡻ࡫ࡉࡐࡕࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࡌࡰࡥࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⏒"),
  bstack1ll111_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪ⏓"),
  bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⏔"),
  bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬ⏕"),
  bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ⏖"),
  bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ⏗"),
  bstack1ll111_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩ⏘"),
  bstack1ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭⏙"),
  bstack1ll111_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪ⏚"),
  bstack1ll111_opy_ (u"ࠩࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡕࡸ࡯࡮ࡲࡷࡆࡪ࡮ࡡࡷ࡫ࡲࡶࠬ⏛")
]
bstack1l11lll11l_opy_ = {
  bstack1ll111_opy_ (u"ࠪࡺࠬ⏜"): bstack1ll111_opy_ (u"ࠫࡻ࠭⏝"),
  bstack1ll111_opy_ (u"ࠬ࡬ࠧ⏞"): bstack1ll111_opy_ (u"࠭ࡦࠨ⏟"),
  bstack1ll111_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭⏠"): bstack1ll111_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧ⏡"),
  bstack1ll111_opy_ (u"ࠩࡲࡲࡱࡿࡡࡶࡶࡲࡱࡦࡺࡥࠨ⏢"): bstack1ll111_opy_ (u"ࠪࡳࡳࡲࡹࡂࡷࡷࡳࡲࡧࡴࡦࠩ⏣"),
  bstack1ll111_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨ⏤"): bstack1ll111_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩ⏥"),
  bstack1ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩ⏦"): bstack1ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ⏧"),
  bstack1ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡰࡴࡷࠫ⏨"): bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬ⏩"),
  bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭⏪"): bstack1ll111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧ⏫"),
  bstack1ll111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨ⏬"): bstack1ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ⏭"),
  bstack1ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨ⏮"): bstack1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡍࡵࡳࡵࠩ⏯"),
  bstack1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪ⏰"): bstack1ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫ⏱"),
  bstack1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬ⏲"): bstack1ll111_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧ⏳"),
  bstack1ll111_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨ⏴"): bstack1ll111_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩ⏵"),
  bstack1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩ⏶"): bstack1ll111_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫ⏷"),
  bstack1ll111_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬ⏸"): bstack1ll111_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭⏹"),
  bstack1ll111_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩ⏺"): bstack1ll111_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪࠪ⏻"),
  bstack1ll111_opy_ (u"ࠧࡱࡣࡦࡪ࡮ࡲࡥࠨ⏼"): bstack1ll111_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ⏽"),
  bstack1ll111_opy_ (u"ࠩࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ⏾"): bstack1ll111_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭⏿"),
  bstack1ll111_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧ␀"): bstack1ll111_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨ␁"),
  bstack1ll111_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧ␂"): bstack1ll111_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨ␃"),
  bstack1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ␄"): bstack1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ␅"),
  bstack1ll111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬ␆"): bstack1ll111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡶࡥࡢࡶࡨࡶࠬ␇")
}
bstack1llllllll111_opy_ = bstack1ll111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡧࡪࡶ࡫ࡹࡧ࠴ࡣࡰ࡯࠲ࡴࡪࡸࡣࡺ࠱ࡦࡰ࡮࠵ࡲࡦ࡮ࡨࡥࡸ࡫ࡳ࠰࡮ࡤࡸࡪࡹࡴ࠰ࡦࡲࡻࡳࡲ࡯ࡢࡦࠥ␈")
bstack1lllllll111l_opy_ = bstack1ll111_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠵ࡨࡦࡣ࡯ࡸ࡭ࡩࡨࡦࡥ࡮ࠦ␉")
bstack1l1l111l_opy_ = bstack1ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡧࡧࡷ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡵࡨࡲࡩࡥࡳࡥ࡭ࡢࡩࡻ࡫࡮ࡵࡵࠥ␊")
HTTPS_HUB = bstack1ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡺࡨ࠴࡮ࡵࡣࠩ␋")
bstack11l11l11l1_opy_ = bstack1ll111_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠬ␌")
bstack111l1ll11l_opy_ = bstack1ll111_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠴࠵࠶࠷࠳ࡼࡪ࠯ࡩࡷࡥࠫ␍")
bstack1ll1lll1ll_opy_ = bstack1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡴࡥࡹࡶࡢ࡬ࡺࡨࡳࠨ␎")
bstack1llll1l1l_opy_ = {
  bstack1ll111_opy_ (u"ࠬࡪࡥࡧࡣࡸࡰࡹ࠭␏"): bstack1ll111_opy_ (u"࠭ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭␐"),
  bstack1ll111_opy_ (u"ࠧࡶࡵ࠰ࡩࡦࡹࡴࠨ␑"): bstack1ll111_opy_ (u"ࠨࡪࡸࡦ࠲ࡻࡳࡦ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ␒"),
  bstack1ll111_opy_ (u"ࠩࡸࡷࠬ␓"): bstack1ll111_opy_ (u"ࠪ࡬ࡺࡨ࠭ࡶࡵ࠰ࡳࡳࡲࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ␔"),
  bstack1ll111_opy_ (u"ࠫࡪࡻࠧ␕"): bstack1ll111_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡨࡹ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭␖"),
  bstack1ll111_opy_ (u"࠭ࡩ࡯ࠩ␗"): bstack1ll111_opy_ (u"ࠧࡩࡷࡥ࠱ࡦࡶࡳ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ␘"),
  bstack1ll111_opy_ (u"ࠨࡣࡸࠫ␙"): bstack1ll111_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡡࡱࡵࡨ࠱ࡴࡴ࡬ࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ␚")
}
bstack1111ll1ll1l_opy_ = {
  bstack1ll111_opy_ (u"ࠪࡧࡷ࡯ࡴࡪࡥࡤࡰࠬ␛"): 50,
  bstack1ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ␜"): 40,
  bstack1ll111_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭␝"): 30,
  bstack1ll111_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ␞"): 20,
  bstack1ll111_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭␟"): 10
}
bstack1l1lllll1_opy_ = bstack1111ll1ll1l_opy_[bstack1ll111_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭␠")]
bstack111111ll1_opy_ = bstack1ll111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥ࠲ࠫ␡")
bstack1ll1ll1ll1_opy_ = bstack1ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ␢")
bstack1l1ll1l111_opy_ = bstack1ll111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪ␣")
bstack1l111l1l1_opy_ = bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫ␤")
bstack1l1ll11l_opy_ = bstack1ll111_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡢࡰࡧࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫ␥")
bstack1l1ll11l11_opy_ = {
  bstack1ll111_opy_ (u"ࠧࡔࡆࡎ࠱ࡌࡋࡎ࠮࠲࠳࠹ࠬ␦"): bstack1ll111_opy_ (u"ࠨࠬ࠭࠮ࠥࡡࡓࡅࡍ࠰ࡋࡊࡔ࠭࠱࠲࠸ࡡࠥࡦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࡡࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡ࡫ࡱࠤࡾࡵࡵࡳࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠮ࠡࡖ࡫࡭ࡸࠦ࡭ࡢࡻࠣࡧࡦࡻࡳࡦࠢࡦࡳࡳ࡬࡬ࡪࡥࡷࡷࠥࡽࡩࡵࡪࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡭ࡹࠦࡵࡴ࡫ࡱ࡫࠿ࠦࡰࡪࡲࠣࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࠡࠬ࠭࠮ࠬ␧")
}
bstack1ll1ll1lll11_opy_ = [bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ␨"), bstack1ll111_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ␩")]
bstack1ll1lll1111l_opy_ = [bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ␪"), bstack1ll111_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ␫")]
bstack1111l1llll_opy_ = re.compile(bstack1ll111_opy_ (u"࠭࡞࡜࡞࡟ࡻ࠲ࡣࠫ࠻࠰࠭ࠨࠬ␬"))
bstack1lll1l1l1_opy_ = [
  bstack1ll111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨ␭"),
  bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ␮"),
  bstack1ll111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭␯"),
  bstack1ll111_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧ␰"),
  bstack1ll111_opy_ (u"ࠫࡦࡶࡰࠨ␱"),
  bstack1ll111_opy_ (u"ࠬࡻࡤࡪࡦࠪ␲"),
  bstack1ll111_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ␳"),
  bstack1ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧ␴"),
  bstack1ll111_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭␵"),
  bstack1ll111_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧ␶"),
  bstack1ll111_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫ␷"), bstack1ll111_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧ␸"),
  bstack1ll111_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨ␹"),
  bstack1ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬ␺"),
  bstack1ll111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫ␻"),
  bstack1ll111_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫ␼"),
  bstack1ll111_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪ␽"),
  bstack1ll111_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨ␾"), bstack1ll111_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨ␿"), bstack1ll111_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧ⑀"), bstack1ll111_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧ⑁"), bstack1ll111_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ⑂"),
  bstack1ll111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭⑃"),
  bstack1ll111_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭⑄"),
  bstack1ll111_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬ⑅"), bstack1ll111_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨ⑆"),
  bstack1ll111_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ⑇"),
  bstack1ll111_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧ⑈"),
  bstack1ll111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ࠭⑉"),
  bstack1ll111_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩ⑊"),
  bstack1ll111_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧ⑋"),
  bstack1ll111_opy_ (u"ࠪࡥࡻࡪࠧ⑌"), bstack1ll111_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ⑍"), bstack1ll111_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧ⑎"), bstack1ll111_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧ⑏"),
  bstack1ll111_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬ⑐"), bstack1ll111_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧ⑑"), bstack1ll111_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬ⑒"),
  bstack1ll111_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬ⑓"), bstack1ll111_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩ⑔"),
  bstack1ll111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧ⑕"), bstack1ll111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩ⑖"), bstack1ll111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬ⑗"), bstack1ll111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪ⑘"), bstack1ll111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭⑙"),
  bstack1ll111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭⑚"), bstack1ll111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨ⑛"),
  bstack1ll111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧ⑜"),
  bstack1ll111_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫ⑝"),
  bstack1ll111_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭⑞"), bstack1ll111_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩ⑟"), bstack1ll111_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧ①"), bstack1ll111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭②"),
  bstack1ll111_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩ③"),
  bstack1ll111_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ④"), bstack1ll111_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭⑤"),
  bstack1ll111_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧ⑥"),
  bstack1ll111_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪ⑦"),
  bstack1ll111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫ⑧"),
  bstack1ll111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⑨"),
  bstack1ll111_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬ⑩"),
  bstack1ll111_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ⑪"),
  bstack1ll111_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮ࠧ⑫"),
  bstack1ll111_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭⑬"),
  bstack1ll111_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬ⑭"),
  bstack1ll111_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭⑮"),
  bstack1ll111_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫ⑯"),
  bstack1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪ⑰"),
  bstack1ll111_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ⑱"),
  bstack1ll111_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭⑲"),
  bstack1ll111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬ⑳"),
  bstack1ll111_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬ⑴"),
  bstack1ll111_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩ⑵"),
  bstack1ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧ⑶"), bstack1ll111_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨ⑷"), bstack1ll111_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨ⑸"),
  bstack1ll111_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪ⑹"),
  bstack1ll111_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫ⑺"),
  bstack1ll111_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪ⑻"),
  bstack1ll111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫ⑼"),
  bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ⑽"),
  bstack1ll111_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨ⑾"),
  bstack1ll111_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨ⑿"), bstack1ll111_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸࠬ⒀"), bstack1ll111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠪ⒁"),
  bstack1ll111_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨ⒂"),
  bstack1ll111_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶࠪ⒃"),
  bstack1ll111_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨࠬ⒄"),
  bstack1ll111_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫ⒅"),
  bstack1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨ⒆"), bstack1ll111_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨࠬ⒇"),
  bstack1ll111_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪ⒈"), bstack1ll111_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷࠬ⒉"),
  bstack1ll111_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣࠩ⒊"),
  bstack1ll111_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩ⒋"),
  bstack1ll111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧ⒌"), bstack1ll111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴࠩ⒍"), bstack1ll111_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩࠪ⒎"), bstack1ll111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧ⒏"),
  bstack1ll111_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨ⒐"),
  bstack1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪ⒑"),
  bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⒒"),
  bstack1ll111_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫ⒓"),
  bstack1ll111_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨࠩ⒔"),
  bstack1ll111_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨ⒕"),
  bstack1ll111_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ⒖"), bstack1ll111_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩ⒗"),
  bstack1ll111_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬ⒘"),
  bstack1ll111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪ⒙"),
  bstack1ll111_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬ⒚"),
  bstack1ll111_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬ⒛"),
  bstack1ll111_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨ⒜"),
  bstack1ll111_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪ⒝"),
  bstack1ll111_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩ⒞"),
  bstack1ll111_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧࠪ⒟"),
  bstack1ll111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪ⒠"),
  bstack1ll111_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ⒡"),
  bstack1ll111_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪ⒢"),
  bstack1ll111_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬ⒣"),
  bstack1ll111_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭⒤"),
  bstack1ll111_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪ⒥"),
  bstack1ll111_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫ⒦"),
  bstack1ll111_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ࠭⒧"),
  bstack1ll111_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬ⒨"),
  bstack1ll111_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭⒩"),
  bstack1ll111_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮ࠪ⒪"),
  bstack1ll111_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭⒫"),
  bstack1ll111_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫ⒬"),
  bstack1ll111_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ⒭"), bstack1ll111_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪ⒮"),
  bstack1ll111_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨ⒯"), bstack1ll111_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭⒰"),
  bstack1ll111_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫ⒱"),
  bstack1ll111_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪ⒲"),
  bstack1ll111_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪ⒳"),
  bstack1ll111_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭⒴"), bstack1ll111_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭⒵"),
  bstack1ll111_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧⒶ"),
  bstack1ll111_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪⒷ"),
  bstack1ll111_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭Ⓒ"),
  bstack1ll111_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨⒹ"),
  bstack1ll111_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪⒺ"),
  bstack1ll111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬⒻ"),
  bstack1ll111_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨⒼ"),
  bstack1ll111_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪⒽ"),
  bstack1ll111_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧⒾ"),
  bstack1ll111_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬⒿ"), bstack1ll111_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫⓀ"),
  bstack1ll111_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨⓁ"),
  bstack1ll111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡌࡨࡑࡵࡣࡢࡶࡲࡶࡆࡻࡴࡰࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠬⓂ")
]
bstack1ll1l1ll_opy_ = bstack1ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡸࡴࡱࡵࡡࡥࠩⓃ")
bstack1lll111l_opy_ = [bstack1ll111_opy_ (u"ࠫ࠳ࡧࡰ࡬ࠩⓄ"), bstack1ll111_opy_ (u"ࠬ࠴ࡡࡢࡤࠪⓅ"), bstack1ll111_opy_ (u"࠭࠮ࡪࡲࡤࠫⓆ")]
bstack1l1l1lll11_opy_ = [bstack1ll111_opy_ (u"ࠧࡪࡦࠪⓇ"), bstack1ll111_opy_ (u"ࠨࡲࡤࡸ࡭࠭Ⓢ"), bstack1ll111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬⓉ"), bstack1ll111_opy_ (u"ࠪࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥࠩⓊ")]
bstack1ll1111ll_opy_ = {
  bstack1ll111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫⓋ"): bstack1ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪⓌ"),
  bstack1ll111_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧⓍ"): bstack1ll111_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬⓎ"),
  bstack1ll111_opy_ (u"ࠨࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭Ⓩ"): bstack1ll111_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪⓐ"),
  bstack1ll111_opy_ (u"ࠪ࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ⓑ"): bstack1ll111_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪⓒ"),
  bstack1ll111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡴࡪࡱࡱࡷࠬⓓ"): bstack1ll111_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧⓔ")
}
bstack1l1l11l11l_opy_ = [
  bstack1ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬⓕ"),
  bstack1ll111_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ⓖ"),
  bstack1ll111_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪⓗ"),
  bstack1ll111_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩⓘ"),
  bstack1ll111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬⓙ"),
]
bstack11111111_opy_ = bstack1ll111lll_opy_ + bstack1ll1ll1l1ll1_opy_ + bstack1lll1l1l1_opy_
bstack1l11llll11_opy_ = [
  bstack1ll111_opy_ (u"ࠬࡤ࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵࠦࠪⓚ"),
  bstack1ll111_opy_ (u"࠭࡞ࡣࡵ࠰ࡰࡴࡩࡡ࡭࠰ࡦࡳࡲࠪࠧⓛ"),
  bstack1ll111_opy_ (u"ࠧ࡟࠳࠵࠻࠳࠭ⓜ"),
  bstack1ll111_opy_ (u"ࠨࡠ࠴࠴࠳࠭ⓝ"),
  bstack1ll111_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠲࡝࠹࠱࠾ࡣ࠮ࠨⓞ"),
  bstack1ll111_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠴࡞࠴࠲࠿࡝࠯ࠩⓟ"),
  bstack1ll111_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠶࡟࠵࠳࠱࡞࠰ࠪⓠ"),
  bstack1ll111_opy_ (u"ࠬࡤ࠱࠺࠴࠱࠵࠻࠾࠮ࠨⓡ")
]
bstack1ll1llll1l11_opy_ = bstack1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧⓢ")
bstack1l1l11l11_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡦࡸࡨࡲࡹ࠭ⓣ")
bstack11ll1ll1l_opy_ = [ bstack1ll111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪⓤ") ]
bstack1ll1ll1l1_opy_ = [ bstack1ll111_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨⓥ") ]
bstack1l11l11ll_opy_ = [bstack1ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧⓦ")]
bstack111ll1llll_opy_ = [ bstack1ll111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫⓧ") ]
bstack11ll1lll11_opy_ = bstack1ll111_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧⓨ")
bstack11ll11ll11_opy_ = bstack1ll111_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩⓩ")
bstack1l1l1l1l11_opy_ = bstack1ll111_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫ⓪")
bstack1l11l11l1l_opy_ = bstack1ll111_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ⓫")
bstack1l11l1lll_opy_ = [
  bstack1ll111_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭⓬"),
  bstack1ll111_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪ⓭"),
  bstack1ll111_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬ⓮"),
  bstack1ll111_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫ⓯"),
  bstack1ll111_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪ⓰"),
  bstack1ll111_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨ⓱"),
  bstack1ll111_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨ⓲"),
  bstack1ll111_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫ⓳"),
  bstack1ll111_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬ⓴"),
  bstack1ll111_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ⓵"),
  bstack1ll111_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭⓶"),
  bstack1ll111_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬ⓷"),
  bstack1ll111_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪ⓸"),
  bstack1ll111_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ⓹"),
  bstack1ll111_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭⓺"),
  bstack1ll111_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ⓻"),
  bstack1ll111_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧ⓼"),
  bstack1ll111_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬ⓽"),
  bstack1ll111_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧ⓾"),
  bstack1ll111_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭⓿"),
  bstack1ll111_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ─"),
]
bstack1l1lll1ll_opy_ = bstack1ll111_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧ━")
bstack11l111lll_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠪࢂࠬ│")), bstack1ll111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ┃"), bstack1ll111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ┄"))
bstack1lll1111ll11_opy_ = bstack1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵ࡯ࠧ┅")
bstack1111l1l11l1_opy_ = [ bstack1ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ┆"), bstack1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ┇"), bstack1ll111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ┈"), bstack1ll111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ┉")]
bstack111l11llll_opy_ = [ bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ┊"), bstack1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ┋"), bstack1ll111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ┌"), bstack1ll111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ┍") ]
bstack111l1lll1l_opy_ = [ bstack1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ┎") ]
bstack1111l111l11_opy_ = [ bstack1ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ┏") ]
bstack111llllll_opy_ = 360
bstack1ll1llll1111_opy_ = bstack1ll111_opy_ (u"ࠥࡥࡵࡶ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥ┐")
bstack1ll1lll11111_opy_ = bstack1ll111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡩࡴࡵࡸࡩࡸࠨ┑")
bstack1ll1ll1l11ll_opy_ = bstack1ll111_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠣ┒")
bstack1lll11111111_opy_ = bstack1ll111_opy_ (u"ࠨࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡵࡧࡶࡸࡸࠦࡡࡳࡧࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦ࡯࡯ࠢࡒࡗࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࠥࡴࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩࠥ࡬࡯ࡳࠢࡄࡲࡩࡸ࡯ࡪࡦࠣࡨࡪࡼࡩࡤࡧࡶ࠲ࠧ┓")
bstack1lll111l111l_opy_ = bstack1ll111_opy_ (u"ࠢ࠲࠳࠱࠴ࠧ└")
bstack1lllll11111_opy_ = {
  bstack1ll111_opy_ (u"ࠨࡒࡄࡗࡘ࠭┕"): bstack1ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ┖"),
  bstack1ll111_opy_ (u"ࠪࡊࡆࡏࡌࠨ┗"): bstack1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ┘"),
  bstack1ll111_opy_ (u"࡙ࠬࡋࡊࡒࠪ┙"): bstack1ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ┚")
}
bstack1111lll1l_opy_ = [
  bstack1ll111_opy_ (u"ࠢࡨࡧࡷࠦ┛"),
  bstack1ll111_opy_ (u"ࠣࡩࡲࡆࡦࡩ࡫ࠣ├"),
  bstack1ll111_opy_ (u"ࠤࡪࡳࡋࡵࡲࡸࡣࡵࡨࠧ┝"),
  bstack1ll111_opy_ (u"ࠥࡶࡪ࡬ࡲࡦࡵ࡫ࠦ┞"),
  bstack1ll111_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ┟"),
  bstack1ll111_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ┠"),
  bstack1ll111_opy_ (u"ࠨࡳࡶࡤࡰ࡭ࡹࡋ࡬ࡦ࡯ࡨࡲࡹࠨ┡"),
  bstack1ll111_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦ┢"),
  bstack1ll111_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦ┣"),
  bstack1ll111_opy_ (u"ࠤࡦࡰࡪࡧࡲࡆ࡮ࡨࡱࡪࡴࡴࠣ┤"),
  bstack1ll111_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࡶࠦ┥"),
  bstack1ll111_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠦ┦"),
  bstack1ll111_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࡇࡳࡺࡰࡦࡗࡨࡸࡩࡱࡶࠥ┧"),
  bstack1ll111_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧ┨"),
  bstack1ll111_opy_ (u"ࠢࡲࡷ࡬ࡸࠧ┩"),
  bstack1ll111_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡖࡲࡹࡨ࡮ࡁࡤࡶ࡬ࡳࡳࠨ┪"),
  bstack1ll111_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡐࡹࡱࡺࡩࡕࡱࡸࡧ࡭ࠨ┫"),
  bstack1ll111_opy_ (u"ࠥࡷ࡭ࡧ࡫ࡦࠤ┬"),
  bstack1ll111_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡄࡴࡵࠨ┭")
]
bstack1ll1lll111ll_opy_ = [
  bstack1ll111_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦ┮"),
  bstack1ll111_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ┯"),
  bstack1ll111_opy_ (u"ࠢࡢࡷࡷࡳࠧ┰"),
  bstack1ll111_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣ┱"),
  bstack1ll111_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ┲")
]
bstack1l111l1lll_opy_ = {
  bstack1ll111_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤ┳"): [bstack1ll111_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ┴")],
  bstack1ll111_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ┵"): [bstack1ll111_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ┶")],
  bstack1ll111_opy_ (u"ࠢࡢࡷࡷࡳࠧ┷"): [bstack1ll111_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ┸"), bstack1ll111_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧ┹"), bstack1ll111_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢ┺"), bstack1ll111_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ┻")],
  bstack1ll111_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰࠧ┼"): [bstack1ll111_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨ┽")],
  bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ┾"): [bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ┿")],
}
bstack1llll1ll111l_opy_ = {
  bstack1ll111_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣ╀"): bstack1ll111_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤ╁"),
  bstack1ll111_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣ╂"): bstack1ll111_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ╃"),
  bstack1ll111_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥ╄"): bstack1ll111_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࠤ╅"),
  bstack1ll111_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡆࡩࡴࡪࡸࡨࡉࡱ࡫࡭ࡦࡰࡷࠦ╆"): bstack1ll111_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦ╇"),
  bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ╈"): bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ╉")
}
bstack1lllll11ll1_opy_ = {
  bstack1ll111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ╊"): bstack1ll111_opy_ (u"࠭ࡓࡶ࡫ࡷࡩ࡙ࠥࡥࡵࡷࡳࠫ╋"),
  bstack1ll111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ╌"): bstack1ll111_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩ╍"),
  bstack1ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ╎"): bstack1ll111_opy_ (u"ࠪࡘࡪࡹࡴࠡࡕࡨࡸࡺࡶࠧ╏"),
  bstack1ll111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ═"): bstack1ll111_opy_ (u"࡚ࠬࡥࡴࡶࠣࡘࡪࡧࡲࡥࡱࡺࡲࠬ║")
}
bstack111l1l111ll_opy_ = 65536
bstack111l1ll1lll_opy_ = bstack1ll111_opy_ (u"࠭࠮࠯࠰࡞ࡘࡗ࡛ࡎࡄࡃࡗࡉࡉࡣࠧ╒")
bstack111llll1111_opy_ = [
      bstack1ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ╓"), bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ╔"), bstack1ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ╕"), bstack1ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ╖"), bstack1ll111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭╗"),
      bstack1ll111_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ╘"), bstack1ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ╙"), bstack1ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ╚"), bstack1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩ╛"),
      bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ╜"), bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ╝"), bstack1ll111_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧ╞")
    ]
bstack111ll111111_opy_= {
  bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ╟"): bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ╠"),
  bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ╡"): bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ╢"),
  bstack1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ╣"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ╤"),
  bstack1ll111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ╥"): bstack1ll111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ╦"),
  bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ╧"): bstack1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ╨"),
  bstack1ll111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ╩"): bstack1ll111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ╪"),
  bstack1ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭╫"): bstack1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ╬"),
  bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ╭"): bstack1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ╮"),
  bstack1ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ╯"): bstack1ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ╰"),
  bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ╱"): bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ╲"),
  bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ╳"): bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ╴"),
  bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭╵"): bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠧ╶"),
  bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ╷"): bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭╸"),
  bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࡒࡴࡹ࡯࡯࡯ࡵࠪ╹"): bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࡓࡵࡺࡩࡰࡰࡶࠫ╺"),
  bstack1ll111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧ╻"): bstack1ll111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ╼"),
  bstack1ll111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ╽"): bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ╾"),
  bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ╿"): bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ▀"),
  bstack1ll111_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ▁"): bstack1ll111_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩ▂"),
  bstack1ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ▃"): bstack1ll111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭▄"),
  bstack1ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ▅"): bstack1ll111_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ▆"),
  bstack1ll111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭▇"): bstack1ll111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ█"),
  bstack1ll111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ▉"): bstack1ll111_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ▊"),
  bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ▋"): bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ▌"),
  bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ▍"): bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ▎"),
  bstack1ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ▏"): bstack1ll111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ▐"),
  bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ░"): bstack1ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫ▒"),
  bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ▓"): bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭▔"),
  bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ▕"): bstack1ll111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ▖")
}
bstack1lllllll1ll1_opy_ = [bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ▗"), bstack1ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ▘")]
bstack11ll1l11l_opy_ = (bstack1ll111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢ▙"),)
bstack111l1ll1l11_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡷࡳࡨࡦࡺࡥࡠࡥ࡯࡭ࠬ▚")
bstack1l11ll1l1_opy_ = bstack1ll111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠲ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠱ࡹ࠵࠴࡭ࡲࡪࡦࡶ࠳ࠧ▛")
bstack1lll11l11l_opy_ = bstack1ll111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬ࡸࡩࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࠤ▜")
bstack11l1111111_opy_ = bstack1ll111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠭ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠧ▝")
class EVENTS(Enum):
  bstack1ll1ll1ll111_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩ▞")
  bstack1l1111ll1l_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳࠫ▟")
  bstack1l111lll_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾࡫࡯࡮ࡢ࡮࡬ࡾࡪ࠭■")
  bstack1ll1ll1lll1l_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࡯ࡳ࡬ࡹࠧ□")
  bstack1l111l1l_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬ▢") #shift post bstack1ll1ll1ll1ll_opy_
  bstack11l111111_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮ࠫ▣") #shift post bstack1ll1ll1ll1ll_opy_
  bstack1lll1l111ll1_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡮ࡵࡣࠩ▤") #shift
  bstack1lllll11l11l_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪ▥") #shift
  bstack1lll1111l1_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨ▦")
  bstack1l1l11l1lll_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡶࡥࡻ࡫࠭ࡳࡧࡶࡹࡱࡺࡳࠨ▧")
  bstack1ll1l11ll1_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡴࡪࡸࡦࡰࡴࡰࡷࡨࡧ࡮ࠨ▨")
  bstack1lllll1l1l_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡮ࡲࡧࡦࡲࠧ▩") #shift
  bstack111l1l1l_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡡࡱࡲ࠰ࡹࡵࡲ࡯ࡢࡦࠪ▪") #shift
  bstack111l11l1l_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡧ࡮࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠩ▫")
  bstack1l1ll1ll11_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭▬") #shift
  bstack1ll1l11111_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭▭") #shift
  bstack1lllll1ll1ll_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻࠪ▮") #shift
  bstack1l111111lll_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ▯")
  bstack11ll1ll1ll_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡶࡸࡦࡺࡵࡴࠩ▰") #shift
  bstack1l1lllll1l_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪ▱")
  bstack1ll1ll1l1lll_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡽࡿ࠭ࡴࡧࡷࡹࡵ࠭▲") #shift
  bstack11l11l1l1_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡹࡻࡰࠨ△")
  bstack1ll1ll1ll1l1_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡲࡦࡶࡳࡩࡱࡷࠫ▴") # not bstack111lll1l1ll_opy_ in python
  bstack1l1l11llll_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡶࡻࡩࡵࠩ▵") # used in bstack1ll1lll111l1_opy_
  bstack11l11ll11ll_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶࡲࡦ࠯ࡴࡹ࡮ࡺࠧ▶")
  bstack11l11lll11l_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱ࡶࡻࡩࡵࠩ▷")
  bstack1l1lll1l1_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡨࡧࡷࠫ▸") # used in bstack1ll1lll111l1_opy_
  bstack1l111l1l1l_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡪࡲࡳࡰ࠭▹")
  bstack11l1l11l11l_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡶࡪ࠳ࡨࡰࡱ࡮ࠫ►")
  bstack11l1l11l1l1_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡴࡹࡴ࠮ࡪࡲࡳࡰ࠭▻")
  bstack1lllllllll_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠬ▼")
  bstack1lllll11l1_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠬ▽") #
  bstack1l11l111l1_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡹࡧ࡫ࡦࡕࡦࡶࡪ࡫࡮ࡔࡪࡲࡸࠬ▾")
  bstack111ll111ll_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬ▿")
  bstack1l1l111ll1_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡩ࠲ࡺࡥࡴࡶࠪ◀")
  bstack1l11l1111l_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡳࡸࡺ࠭ࡵࡧࡶࡸࠬ◁")
  bstack11ll11l111_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡷ࡫࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨ◂") #shift
  bstack1l1lll111_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪ◃") #shift
  bstack1111ll11ll1_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫ◄")
  bstack1ll1ll1l1l1l_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡫ࡧࡰࡪ࠳ࡴࡪ࡯ࡨࡳࡺࡺࠧ◅")
  bstack11ll1l111l_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡦࡺ࡬ࡸ࠲࡮ࡡ࡯ࡦ࡯ࡩࡷ࠭◆")
  bstack1l1l1lllll1_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿࡫ࡸࡪࡶ࠰࡬ࡦࡴࡤ࡭ࡧࡵࠫ◇")
  bstack1ll1ll1l111l_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࠭࡮ࡧࡷࡶ࡮ࡩࡳࠨ◈")
  bstack1lll11llll11_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡩࡷࡥ࠾ࡸࡺ࡯ࡱࠩ◉")
  bstack1ll11ll111l_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡵࡷࡥࡷࡺࠧ◊")
  bstack111ll1l1l1l_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡧࡳࡼࡴ࡬ࡰࡣࡧࠫ○")
  bstack111l11ll111_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡧ࡭࡫ࡣ࡬࠯ࡸࡴࡩࡧࡴࡦࠩ◌")
  bstack1ll11l11l11_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡴࡴ࠭ࡣࡱࡲࡸࡸࡺࡲࡢࡲࠪ◍")
  bstack1ll11l11ll1_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡵ࡮࠮ࡵࡷࡥࡷࡺࡢࡪࡰࡤࡶࡾ࠭◎")
  bstack1l1l1llllll_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡦࡳࡳࡴࡥࡤࡶࠪ●")
  bstack1ll11lll1l1_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡷࡹࡵࡰࠨ◐")
  bstack1ll1111111l_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡸࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠭◑")
  bstack1l1ll11l1l1_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯ࠩ◒")
  bstack1ll1ll1l11l1_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠪ◓")
  bstack1ll1ll1llll1_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡧ࡫ࡱࡨࡓ࡫ࡡࡳࡧࡶࡸࡍࡻࡢࠨ◔")
  bstack11lll11l111_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡉ࡯࡫ࡷࠫ◕")
  bstack11lll1ll111_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡶࡹ࠭◖")
  bstack1l1l11lll11_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡆࡳࡳ࡬ࡩࡨࠩ◗")
  bstack1ll1ll1lllll_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪ◘")
  bstack1l11ll1ll11_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡩࡔࡧ࡯ࡪࡍ࡫ࡡ࡭ࡕࡷࡩࡵ࠭◙")
  bstack1l11ll11l1l_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡊࡩࡹࡘࡥࡴࡷ࡯ࡸࠬ◚")
  bstack1l111l1ll1l_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡅࡷࡧࡱࡸࠬ◛")
  bstack1l1111l11ll_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠫ◜")
  bstack1l111lll11l_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡬ࡰࡩࡆࡶࡪࡧࡴࡦࡦࡈࡺࡪࡴࡴࠨ◝")
  bstack1ll1ll1ll11l_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡦࡰࡴࡹࡪࡻࡥࡕࡧࡶࡸࡊࡼࡥ࡯ࡶࠪ◞")
  bstack11ll1lll1l1_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡴࡶࠧ◟")
  bstack1l1llll1l11_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࡮ࡔࡶࡲࡴࠬ◠")
  bstack11l111l11l1_opy_ = bstack1ll111_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭ࡧࡤࡲࡺࡶࡕࡱ࡮ࡲࡥࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪ◡")
  bstack11l1l1111l_opy_ = bstack1ll111_opy_ (u"ࠪࡷࡩࡱ࠺ࡴࡧࡱࡨࡋࡻ࡮࡯ࡧ࡯ࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪ◢")
  bstack1ll1111l1_opy_ = bstack1ll111_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡌࡵ࡯ࡰࡨࡰ࡙࡫ࡳࡵࡅࡲࡱࡵࡲࡥࡵࡧࡧࠫ◣")
  bstack1lll1lll1l1_opy_ = bstack1ll111_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡴࡵࡲࡹࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡐࡺࡶࡨࡷࡹ࠭◤")
  bstack1lll1l111l1_opy_ = bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡳࡑࡻࡷࡩࡸࡺࠧ◥")
  bstack1lll1ll1ll1_opy_ = bstack1ll111_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡿࡴࡦࡵࡷࡋࡪࡺࡔࡰࡶࡤࡰ࡙࡫ࡳࡵࡵࠪ◦")
class STAGE(Enum):
  bstack11ll11ll1l_opy_ = bstack1ll111_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧ◧")
  END = bstack1ll111_opy_ (u"ࠩࡨࡲࡩ࠭◨")
  bstack11ll1111_opy_ = bstack1ll111_opy_ (u"ࠪࡷ࡮ࡴࡧ࡭ࡧࠪ◩")
bstack11lll111l_opy_ = {
  bstack1ll111_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࠫ◪"): bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ◫"),
  bstack1ll111_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪ◬"): bstack1ll111_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ◭")
}
PLAYWRIGHT_HUB_URL = bstack1ll111_opy_ (u"ࠣࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠥ◮")
bstack1l1l1l1l1l1_opy_ = 98
bstack1l1l1111ll1_opy_ = 100
bstack1lll1ll111l_opy_ = {
  bstack1ll111_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࠨ◯"): bstack1ll111_opy_ (u"ࠪ࠱࠲ࡸࡥࡳࡷࡱࡷࠬ◰"),
  bstack1ll111_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪ◱"): bstack1ll111_opy_ (u"ࠬ࠳࠭ࡳࡧࡵࡹࡳࡹ࠭ࡥࡧ࡯ࡥࡾ࠭◲"),
  bstack1ll111_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫ◳"): 0
}
bstack1lll1lll1l11_opy_ = bstack1ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢ◴")
bstack1111lll11l1_opy_ = bstack1ll111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡸࡴࡱࡵࡡࡥ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧ◵")
bstack11llll1l1_opy_ = bstack1ll111_opy_ (u"ࠤࡗࡉࡘ࡚ࠠࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠣࡅࡓࡊࠠࡂࡐࡄࡐ࡞࡚ࡉࡄࡕࠥ◶")