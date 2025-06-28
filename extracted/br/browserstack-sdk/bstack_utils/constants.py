# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import os
import re
from enum import Enum
bstack11ll11ll11_opy_ = {
  bstack1l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᝈ"): bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࠨᝉ"),
  bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᝊ"): bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡱࡥࡺࠩᝋ"),
  bstack1l1ll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᝌ"): bstack1l1ll1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᝍ"),
  bstack1l1ll1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᝎ"): bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪᝏ"),
  bstack1l1ll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᝐ"): bstack1l1ll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹ࠭ᝑ"),
  bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᝒ"): bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࠭ᝓ"),
  bstack1l1ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᝔"): bstack1l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᝕"),
  bstack1l1ll1_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩ᝖"): bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨࠩ᝗"),
  bstack1l1ll1_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪ᝘"): bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡯ࡵࡲࡰࡪ࠭᝙"),
  bstack1l1ll1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬ᝚"): bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬ᝛"),
  bstack1l1ll1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭᝜"): bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭᝝"),
  bstack1l1ll1_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪ᝞"): bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡻ࡯ࡤࡦࡱࠪ᝟"),
  bstack1l1ll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬᝠ"): bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬᝡ"),
  bstack1l1ll1_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨᝢ"): bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨᝣ"),
  bstack1l1ll1_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᝤ"): bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᝥ"),
  bstack1l1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧᝦ"): bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧᝧ"),
  bstack1l1ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᝨ"): bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᝩ"),
  bstack1l1ll1_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨᝪ"): bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨᝫ"),
  bstack1l1ll1_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩᝬ"): bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩ᝭"),
  bstack1l1ll1_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭ᝮ"): bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭ᝯ"),
  bstack1l1ll1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪᝰ"): bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡲࡩࡑࡥࡺࡵࠪ᝱"),
  bstack1l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᝲ"): bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬᝳ"),
  bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫ᝴"): bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡶࠫ᝵"),
  bstack1l1ll1_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨ᝶"): bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡨࡦࡥࡨ࡮ࡥࠨ᝷"),
  bstack1l1ll1_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪ᝸"): bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪ᝹"),
  bstack1l1ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧ᝺"): bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧ᝻"),
  bstack1l1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ᝼"): bstack1l1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ᝽"),
  bstack1l1ll1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬ᝾"): bstack1l1ll1_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧ᝿"),
  bstack1l1ll1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪក"): bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫខ"),
  bstack1l1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬគ"): bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬឃ"),
  bstack1l1ll1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨង"): bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨច"),
  bstack1l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨឆ"): bstack1l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫជ"),
  bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ឈ"): bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ញ"),
  bstack1l1ll1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ដ"): bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡰࡷࡵࡧࡪ࠭ឋ"),
  bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪឌ"): bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪឍ"),
  bstack1l1ll1_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬណ"): bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡏࡣࡰࡩࠬត"),
  bstack1l1ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨថ"): bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨទ"),
  bstack1l1ll1_opy_ (u"ࠧࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫធ"): bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫន"),
  bstack1l1ll1_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧប"): bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧផ"),
  bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧព"): bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧភ"),
  bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨម"): bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨយ")
}
bstack11l1llll1l1_opy_ = [
  bstack1l1ll1_opy_ (u"ࠨࡱࡶࠫរ"),
  bstack1l1ll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬល"),
  bstack1l1ll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬវ"),
  bstack1l1ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩឝ"),
  bstack1l1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩឞ"),
  bstack1l1ll1_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪស"),
  bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧហ"),
]
bstack1l1lllll_opy_ = {
  bstack1l1ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪឡ"): [bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪអ"), bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡏࡃࡐࡉࠬឣ")],
  bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧឤ"): bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨឥ"),
  bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩឦ"): bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠪឧ"),
  bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ឨ"): bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠧឩ"),
  bstack1l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬឪ"): bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ឫ"),
  bstack1l1ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬឬ"): bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡁࡓࡃࡏࡐࡊࡒࡓࡠࡒࡈࡖࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧឭ"),
  bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫឮ"): bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑ࠭ឯ"),
  bstack1l1ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ឰ"): bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧឱ"),
  bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰࠨឲ"): [bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࡠࡋࡇࠫឳ"), bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࠩ឴")],
  bstack1l1ll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ឵"): bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡑࡕࡇࡍࡇ࡙ࡉࡑ࠭ា"),
  bstack1l1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ិ"): bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ី"),
  bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨឹ"): bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡒࡆࡘࡋࡒࡗࡃࡅࡍࡑࡏࡔ࡚ࠩឺ"),
  bstack1l1ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪុ"): bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡖࡔࡅࡓࡘࡉࡁࡍࡇࠪូ")
}
bstack11llll1ll1_opy_ = {
  bstack1l1ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪួ"): [bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫើ"), bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫឿ")],
  bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧៀ"): [bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡣࡰ࡫ࡹࠨេ"), bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨែ")],
  bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪៃ"): bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪោ"),
  bstack1l1ll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧៅ"): bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧំ"),
  bstack1l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ះ"): bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ៈ"),
  bstack1l1ll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭៉"): [bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡱࡲࠪ៊"), bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ់")],
  bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭៌"): bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ៍"),
  bstack1l1ll1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ៎"): bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨ៏"),
  bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲࠪ័"): bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲࠪ៑"),
  bstack1l1ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮្ࠪ"): bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ៓"),
  bstack1l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ។"): bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ៕")
}
bstack11ll1l1ll1_opy_ = {
  bstack1l1ll1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ៖"): bstack1l1ll1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪៗ"),
  bstack1l1ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ៘"): [bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ៙"), bstack1l1ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ៚")],
  bstack1l1ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ៛"): bstack1l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩៜ"),
  bstack1l1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ៝"): bstack1l1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭៞"),
  bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ៟"): [bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ០"), bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨ១")],
  bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ២"): bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭៣"),
  bstack1l1ll1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ៤"): bstack1l1ll1_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫ៥"),
  bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ៦"): [bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ៧"), bstack1l1ll1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ៨")],
  bstack1l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩ៩"): [bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬ៪"), bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬ៫")]
}
bstack1llll1l11l_opy_ = [
  bstack1l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬ៬"),
  bstack1l1ll1_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪ៭"),
  bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ៮"),
  bstack1l1ll1_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩ៯"),
  bstack1l1ll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬ៰"),
  bstack1l1ll1_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩ៱"),
  bstack1l1ll1_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨ៲"),
  bstack1l1ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ៳"),
  bstack1l1ll1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ៴"),
  bstack1l1ll1_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៵"),
  bstack1l1ll1_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ៶"),
  bstack1l1ll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ៷"),
]
bstack111ll11l1_opy_ = [
  bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ៸"),
  bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៹"),
  bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ៺"),
  bstack1l1ll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ៻"),
  bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ៼"),
  bstack1l1ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ៽"),
  bstack1l1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭៾"),
  bstack1l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ៿"),
  bstack1l1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ᠀"),
  bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫ᠁"),
  bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ᠂"),
  bstack1l1ll1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪ᠃"),
  bstack1l1ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡖࡤ࡫ࠬ᠄"),
  bstack1l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᠅"),
  bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᠆"),
  bstack1l1ll1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩ᠇"),
  bstack1l1ll1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠵ࠬ᠈"),
  bstack1l1ll1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠷࠭᠉"),
  bstack1l1ll1_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠹ࠧ᠊"),
  bstack1l1ll1_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠴ࠨ᠋"),
  bstack1l1ll1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠶ࠩ᠌"),
  bstack1l1ll1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠸ࠪ᠍"),
  bstack1l1ll1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠺ࠫ᠎"),
  bstack1l1ll1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠼ࠬ᠏"),
  bstack1l1ll1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠾࠭᠐"),
  bstack1l1ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ᠑"),
  bstack1l1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᠒"),
  bstack1l1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭᠓"),
  bstack1l1ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭᠔"),
  bstack1l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᠕"),
  bstack1l1ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᠖"),
  bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ᠗")
]
bstack11l1ll111ll_opy_ = [
  bstack1l1ll1_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭᠘"),
  bstack1l1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ᠙"),
  bstack1l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭᠚"),
  bstack1l1ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ᠛"),
  bstack1l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫ᠜"),
  bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᠝"),
  bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩ᠞"),
  bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᠟"),
  bstack1l1ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᠠ"),
  bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᠡ"),
  bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᠢ"),
  bstack1l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᠣ"),
  bstack1l1ll1_opy_ (u"࠭࡯ࡴࠩᠤ"),
  bstack1l1ll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᠥ"),
  bstack1l1ll1_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧᠦ"),
  bstack1l1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫᠧ"),
  bstack1l1ll1_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪᠨ"),
  bstack1l1ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ᠩ"),
  bstack1l1ll1_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ᠪ"),
  bstack1l1ll1_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪᠫ"),
  bstack1l1ll1_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬᠬ"),
  bstack1l1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬᠭ"),
  bstack1l1ll1_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨᠮ"),
  bstack1l1ll1_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧᠯ"),
  bstack1l1ll1_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬᠰ"),
  bstack1l1ll1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᠱ"),
  bstack1l1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᠲ"),
  bstack1l1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨᠳ"),
  bstack1l1ll1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᠴ"),
  bstack1l1ll1_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ᠵ"),
  bstack1l1ll1_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬᠶ"),
  bstack1l1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᠷ"),
  bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬᠸ"),
  bstack1l1ll1_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬᠹ"),
  bstack1l1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᠺ"),
  bstack1l1ll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᠻ"),
  bstack1l1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᠼ"),
  bstack1l1ll1_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪࠫᠽ"),
  bstack1l1ll1_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵࠪᠾ"),
  bstack1l1ll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴࠩᠿ"),
  bstack1l1ll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨᡀ"),
  bstack1l1ll1_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩᡁ"),
  bstack1l1ll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧᡂ"),
  bstack1l1ll1_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧᡃ"),
  bstack1l1ll1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨᡄ"),
  bstack1l1ll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩᡅ"),
  bstack1l1ll1_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪᡆ"),
  bstack1l1ll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᡇ"),
  bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫᡈ"),
  bstack1l1ll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪᡉ"),
  bstack1l1ll1_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪᡊ"),
  bstack1l1ll1_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫᡋ"),
  bstack1l1ll1_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬᡌ"),
  bstack1l1ll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫᡍ"),
  bstack1l1ll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫᡎ"),
  bstack1l1ll1_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧᡏ"),
  bstack1l1ll1_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪᡐ"),
  bstack1l1ll1_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧᡑ"),
  bstack1l1ll1_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᡒ"),
  bstack1l1ll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬᡓ"),
  bstack1l1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬᡔ"),
  bstack1l1ll1_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࠧᡕ"),
  bstack1l1ll1_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧᡖ"),
  bstack1l1ll1_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨᡗ"),
  bstack1l1ll1_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨᡘ"),
  bstack1l1ll1_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪᡙ"),
  bstack1l1ll1_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᡚ"),
  bstack1l1ll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨᡛ"),
  bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࠪᡜ"),
  bstack1l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ᡝ"),
  bstack1l1ll1_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࠫᡞ"),
  bstack1l1ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ᡟ"),
  bstack1l1ll1_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪᡠ"),
  bstack1l1ll1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬᡡ"),
  bstack1l1ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᡢ"),
  bstack1l1ll1_opy_ (u"࠭ࡩࡦࠩᡣ"),
  bstack1l1ll1_opy_ (u"ࠧࡦࡦࡪࡩࠬᡤ"),
  bstack1l1ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᡥ"),
  bstack1l1ll1_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨᡦ"),
  bstack1l1ll1_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬᡧ"),
  bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬᡨ"),
  bstack1l1ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫᡩ"),
  bstack1l1ll1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩᡪ"),
  bstack1l1ll1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪᡫ"),
  bstack1l1ll1_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬᡬ"),
  bstack1l1ll1_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩᡭ"),
  bstack1l1ll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᡮ"),
  bstack1l1ll1_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ᡯ"),
  bstack1l1ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ᡰ"),
  bstack1l1ll1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᡱ"),
  bstack1l1ll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧᡲ"),
  bstack1l1ll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩᡳ"),
  bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᡴ"),
  bstack1l1ll1_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨᡵ"),
  bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᡶ"),
  bstack1l1ll1_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩᡷ"),
  bstack1l1ll1_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬᡸ"),
  bstack1l1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫ᡹"),
  bstack1l1ll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫ᡺"),
  bstack1l1ll1_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭᡻"),
  bstack1l1ll1_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨ᡼"),
  bstack1l1ll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭᡽"),
  bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᡾"),
  bstack1l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᡿"),
  bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᢀ"),
  bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᢁ"),
  bstack1l1ll1_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬᢂ"),
  bstack1l1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩᢃ"),
  bstack1l1ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭ᢄ"),
  bstack1l1ll1_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨᢅ")
]
bstack1l1ll1ll1_opy_ = {
  bstack1l1ll1_opy_ (u"࠭ࡶࠨᢆ"): bstack1l1ll1_opy_ (u"ࠧࡷࠩᢇ"),
  bstack1l1ll1_opy_ (u"ࠨࡨࠪᢈ"): bstack1l1ll1_opy_ (u"ࠩࡩࠫᢉ"),
  bstack1l1ll1_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩᢊ"): bstack1l1ll1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪᢋ"),
  bstack1l1ll1_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᢌ"): bstack1l1ll1_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬᢍ"),
  bstack1l1ll1_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫᢎ"): bstack1l1ll1_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬᢏ"),
  bstack1l1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬᢐ"): bstack1l1ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ᢑ"),
  bstack1l1ll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧᢒ"): bstack1l1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨᢓ"),
  bstack1l1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᢔ"): bstack1l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᢕ"),
  bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᢖ"): bstack1l1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᢗ"),
  bstack1l1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫᢘ"): bstack1l1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬᢙ"),
  bstack1l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ᢚ"): bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᢛ"),
  bstack1l1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᢜ"): bstack1l1ll1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᢝ"),
  bstack1l1ll1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᢞ"): bstack1l1ll1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᢟ"),
  bstack1l1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᢠ"): bstack1l1ll1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᢡ"),
  bstack1l1ll1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᢢ"): bstack1l1ll1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᢣ"),
  bstack1l1ll1_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬᢤ"): bstack1l1ll1_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ᢥ"),
  bstack1l1ll1_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫᢦ"): bstack1l1ll1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᢧ"),
  bstack1l1ll1_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᢨ"): bstack1l1ll1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦᢩࠩ"),
  bstack1l1ll1_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᢪ"): bstack1l1ll1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ᢫"),
  bstack1l1ll1_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪ᢬"): bstack1l1ll1_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫ᢭"),
  bstack1l1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭᢮"): bstack1l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᢯"),
  bstack1l1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨᢰ"): bstack1l1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࠨᢱ")
}
bstack11l1lll1111_opy_ = bstack1l1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡪ࡭ࡹ࡮ࡵࡣ࠰ࡦࡳࡲ࠵ࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪ࠱ࡵࡩࡱ࡫ࡡࡴࡧࡶ࠳ࡱࡧࡴࡦࡵࡷ࠳ࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᢲ")
bstack11l1ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠱࡫ࡩࡦࡲࡴࡩࡥ࡫ࡩࡨࡱࠢᢳ")
bstack11ll1111l_opy_ = bstack1l1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡪࡪࡳ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡸ࡫࡮ࡥࡡࡶࡨࡰࡥࡥࡷࡧࡱࡸࡸࠨᢴ")
bstack1111ll111_opy_ = bstack1l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡽࡤ࠰ࡪࡸࡦࠬᢵ")
bstack1ll11lll1_opy_ = bstack1l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠨᢶ")
bstack11llll1lll_opy_ = bstack1l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯࡯ࡧࡻࡸࡤ࡮ࡵࡣࡵࠪᢷ")
bstack11l1lll1l1l_opy_ = {
  bstack1l1ll1_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩᢸ"): 50,
  bstack1l1ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᢹ"): 40,
  bstack1l1ll1_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᢺ"): 30,
  bstack1l1ll1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᢻ"): 20,
  bstack1l1ll1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᢼ"): 10
}
bstack11lll111_opy_ = bstack11l1lll1l1l_opy_[bstack1l1ll1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᢽ")]
bstack11ll111l11_opy_ = bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᢾ")
bstack11l1lll11l_opy_ = bstack1l1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᢿ")
bstack1ll111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᣀ")
bstack11llll11ll_opy_ = bstack1l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᣁ")
bstack1l111l11ll_opy_ = bstack1l1ll1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡦࡴࡤࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡴࡦࡩ࡫ࡢࡩࡨࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡠࠨᣂ")
bstack11l1ll1l1ll_opy_ = [bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᣃ"), bstack1l1ll1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᣄ")]
bstack11l1ll1l1l1_opy_ = [bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᣅ"), bstack1l1ll1_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᣆ")]
bstack11l1l1ll1l_opy_ = re.compile(bstack1l1ll1_opy_ (u"ࠨࡠ࡞ࡠࡡࡽ࠭࡞࠭࠽࠲࠯ࠪࠧᣇ"))
bstack1ll1l111l_opy_ = [
  bstack1l1ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪᣈ"),
  bstack1l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᣉ"),
  bstack1l1ll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᣊ"),
  bstack1l1ll1_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩᣋ"),
  bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲࠪᣌ"),
  bstack1l1ll1_opy_ (u"ࠧࡶࡦ࡬ࡨࠬᣍ"),
  bstack1l1ll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᣎ"),
  bstack1l1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩᣏ"),
  bstack1l1ll1_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᣐ"),
  bstack1l1ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩᣑ"),
  bstack1l1ll1_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭ᣒ"), bstack1l1ll1_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩᣓ"),
  bstack1l1ll1_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪᣔ"),
  bstack1l1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧᣕ"),
  bstack1l1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ᣖ"),
  bstack1l1ll1_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭ᣗ"),
  bstack1l1ll1_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬᣘ"),
  bstack1l1ll1_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪᣙ"), bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪᣚ"), bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩᣛ"), bstack1l1ll1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩᣜ"), bstack1l1ll1_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫᣝ"),
  bstack1l1ll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨᣞ"),
  bstack1l1ll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨᣟ"),
  bstack1l1ll1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧᣠ"), bstack1l1ll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪᣡ"),
  bstack1l1ll1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬᣢ"),
  bstack1l1ll1_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩᣣ"),
  bstack1l1ll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨᣤ"),
  bstack1l1ll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫᣥ"),
  bstack1l1ll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩᣦ"),
  bstack1l1ll1_opy_ (u"ࠬࡧࡶࡥࠩᣧ"), bstack1l1ll1_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩᣨ"), bstack1l1ll1_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩᣩ"), bstack1l1ll1_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩᣪ"),
  bstack1l1ll1_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧᣫ"), bstack1l1ll1_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩᣬ"), bstack1l1ll1_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧᣭ"),
  bstack1l1ll1_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧᣮ"), bstack1l1ll1_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫᣯ"),
  bstack1l1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩᣰ"), bstack1l1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫᣱ"), bstack1l1ll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧᣲ"), bstack1l1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬᣳ"), bstack1l1ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨᣴ"),
  bstack1l1ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨᣵ"), bstack1l1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪ᣶"),
  bstack1l1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ᣷"),
  bstack1l1ll1_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᣸"),
  bstack1l1ll1_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨ᣹"), bstack1l1ll1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫ᣺"), bstack1l1ll1_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩ᣻"), bstack1l1ll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ᣼"),
  bstack1l1ll1_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫ᣽"),
  bstack1l1ll1_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ᣾"), bstack1l1ll1_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨ᣿"),
  bstack1l1ll1_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩᤀ"),
  bstack1l1ll1_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬᤁ"),
  bstack1l1ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭ᤂ"),
  bstack1l1ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᤃ"),
  bstack1l1ll1_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧᤄ"),
  bstack1l1ll1_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᤅ"),
  bstack1l1ll1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩᤆ"),
  bstack1l1ll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨᤇ"),
  bstack1l1ll1_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧᤈ"),
  bstack1l1ll1_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨᤉ"),
  bstack1l1ll1_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᤊ"),
  bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬᤋ"),
  bstack1l1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫᤌ"),
  bstack1l1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨᤍ"),
  bstack1l1ll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧᤎ"),
  bstack1l1ll1_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧᤏ"),
  bstack1l1ll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫᤐ"),
  bstack1l1ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩᤑ"), bstack1l1ll1_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪᤒ"), bstack1l1ll1_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪᤓ"),
  bstack1l1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬᤔ"),
  bstack1l1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ᤕ"),
  bstack1l1ll1_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬᤖ"),
  bstack1l1ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ᤗ"),
  bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᤘ"),
  bstack1l1ll1_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪᤙ"),
  bstack1l1ll1_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪᤚ"), bstack1l1ll1_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧᤛ"), bstack1l1ll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬᤜ"),
  bstack1l1ll1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪᤝ"),
  bstack1l1ll1_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬᤞ"),
  bstack1l1ll1_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧ᤟"),
  bstack1l1ll1_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᤠ"),
  bstack1l1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪᤡ"), bstack1l1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧᤢ"),
  bstack1l1ll1_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬᤣ"), bstack1l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧᤤ"),
  bstack1l1ll1_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫᤥ"),
  bstack1l1ll1_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫᤦ"),
  bstack1l1ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩᤧ"), bstack1l1ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫᤨ"), bstack1l1ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬᤩ"), bstack1l1ll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩᤪ"),
  bstack1l1ll1_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪᤫ"),
  bstack1l1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬ᤬"),
  bstack1l1ll1_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ᤭"),
  bstack1l1ll1_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭᤮"),
  bstack1l1ll1_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪࠫ᤯"),
  bstack1l1ll1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪᤰ"),
  bstack1l1ll1_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪᤱ"), bstack1l1ll1_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫᤲ"),
  bstack1l1ll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧᤳ"),
  bstack1l1ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬᤴ"),
  bstack1l1ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧᤵ"),
  bstack1l1ll1_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᤶ"),
  bstack1l1ll1_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪᤷ"),
  bstack1l1ll1_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬᤸ"),
  bstack1l1ll1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶ᤹ࠫ"),
  bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬ᤺"),
  bstack1l1ll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸ᤻ࠬ"),
  bstack1l1ll1_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ᤼"),
  bstack1l1ll1_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ᤽"),
  bstack1l1ll1_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧ᤾"),
  bstack1l1ll1_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨ᤿"),
  bstack1l1ll1_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩࠬ᥀"),
  bstack1l1ll1_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭᥁"),
  bstack1l1ll1_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ᥂"),
  bstack1l1ll1_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ᥃"),
  bstack1l1ll1_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ᥄"),
  bstack1l1ll1_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ᥅"),
  bstack1l1ll1_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ᥆"),
  bstack1l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭᥇"),
  bstack1l1ll1_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ᥈"), bstack1l1ll1_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ᥉"),
  bstack1l1ll1_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪ᥊"), bstack1l1ll1_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ᥋"),
  bstack1l1ll1_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭᥌"),
  bstack1l1ll1_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ᥍"),
  bstack1l1ll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ᥎"),
  bstack1l1ll1_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨ᥏"), bstack1l1ll1_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨᥐ"),
  bstack1l1ll1_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩᥑ"),
  bstack1l1ll1_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬᥒ"),
  bstack1l1ll1_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨᥓ"),
  bstack1l1ll1_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪᥔ"),
  bstack1l1ll1_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬᥕ"),
  bstack1l1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧᥖ"),
  bstack1l1ll1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪᥗ"),
  bstack1l1ll1_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬᥘ"),
  bstack1l1ll1_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩᥙ"),
  bstack1l1ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧᥚ"), bstack1l1ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭ᥛ"),
  bstack1l1ll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪᥜ"),
  bstack1l1ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡎࡪࡌࡰࡥࡤࡸࡴࡸࡁࡶࡶࡲࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠧᥝ")
]
bstack1l11l111ll_opy_ = bstack1l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡺࡶ࡬ࡰࡣࡧࠫᥞ")
bstack1l1ll1llll_opy_ = [bstack1l1ll1_opy_ (u"࠭࠮ࡢࡲ࡮ࠫᥟ"), bstack1l1ll1_opy_ (u"ࠧ࠯ࡣࡤࡦࠬᥠ"), bstack1l1ll1_opy_ (u"ࠨ࠰࡬ࡴࡦ࠭ᥡ")]
bstack11l11111l1_opy_ = [bstack1l1ll1_opy_ (u"ࠩ࡬ࡨࠬᥢ"), bstack1l1ll1_opy_ (u"ࠪࡴࡦࡺࡨࠨᥣ"), bstack1l1ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧᥤ"), bstack1l1ll1_opy_ (u"ࠬࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࠫᥥ")]
bstack1l111ll111_opy_ = {
  bstack1l1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᥦ"): bstack1l1ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᥧ"),
  bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩᥨ"): bstack1l1ll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧᥩ"),
  bstack1l1ll1_opy_ (u"ࠪࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᥪ"): bstack1l1ll1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬᥫ"),
  bstack1l1ll1_opy_ (u"ࠬ࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᥬ"): bstack1l1ll1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬᥭ"),
  bstack1l1ll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡶ࡬ࡳࡳࡹࠧ᥮"): bstack1l1ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᥯")
}
bstack1l11l1111l_opy_ = [
  bstack1l1ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᥰ"),
  bstack1l1ll1_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᥱ"),
  bstack1l1ll1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬᥲ"),
  bstack1l1ll1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫᥳ"),
  bstack1l1ll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧᥴ"),
]
bstack11ll11111_opy_ = bstack111ll11l1_opy_ + bstack11l1ll111ll_opy_ + bstack1ll1l111l_opy_
bstack11llll11l_opy_ = [
  bstack1l1ll1_opy_ (u"ࠧ࡟࡮ࡲࡧࡦࡲࡨࡰࡵࡷࠨࠬ᥵"),
  bstack1l1ll1_opy_ (u"ࠨࡠࡥࡷ࠲ࡲ࡯ࡤࡣ࡯࠲ࡨࡵ࡭ࠥࠩ᥶"),
  bstack1l1ll1_opy_ (u"ࠩࡡ࠵࠷࠽࠮ࠨ᥷"),
  bstack1l1ll1_opy_ (u"ࠪࡢ࠶࠶࠮ࠨ᥸"),
  bstack1l1ll1_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠴࡟࠻࠳࠹࡞࠰ࠪ᥹"),
  bstack1l1ll1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠶ࡠ࠶࠭࠺࡟࠱ࠫ᥺"),
  bstack1l1ll1_opy_ (u"࠭࡞࠲࠹࠵࠲࠸ࡡ࠰࠮࠳ࡠ࠲ࠬ᥻"),
  bstack1l1ll1_opy_ (u"ࠧ࡟࠳࠼࠶࠳࠷࠶࠹࠰ࠪ᥼")
]
bstack11ll11lll1l_opy_ = bstack1l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ᥽")
bstack1l1l1l1l1_opy_ = bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡨࡺࡪࡴࡴࠨ᥾")
bstack1l1ll1l1l1_opy_ = [ bstack1l1ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᥿") ]
bstack1lllll11l_opy_ = [ bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪᦀ") ]
bstack11l11llll1_opy_ = [bstack1l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᦁ")]
bstack1l111ll1l_opy_ = [ bstack1l1ll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᦂ") ]
bstack1l11lll1_opy_ = bstack1l1ll1_opy_ (u"ࠧࡔࡆࡎࡗࡪࡺࡵࡱࠩᦃ")
bstack1ll1l1l11l_opy_ = bstack1l1ll1_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠫᦄ")
bstack11ll1ll1ll_opy_ = bstack1l1ll1_opy_ (u"ࠩࡖࡈࡐ࡚ࡥࡴࡶࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱ࠭ᦅ")
bstack1ll1ll1111_opy_ = bstack1l1ll1_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࠩᦆ")
bstack1l1lllll1l_opy_ = [
  bstack1l1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡈࡄࡍࡑࡋࡄࠨᦇ"),
  bstack1l1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡗࡍࡒࡋࡄࡠࡑࡘࡘࠬᦈ"),
  bstack1l1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡆࡑࡕࡃࡌࡇࡇࡣࡇ࡟࡟ࡄࡎࡌࡉࡓ࡚ࠧᦉ"),
  bstack1l1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡋࡔࡘࡑࡕࡏࡤࡉࡈࡂࡐࡊࡉࡉ࠭ᦊ"),
  bstack1l1ll1_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡈࡘࡤࡔࡏࡕࡡࡆࡓࡓࡔࡅࡄࡖࡈࡈࠬᦋ"),
  bstack1l1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡇࡑࡕࡓࡆࡆࠪᦌ"),
  bstack1l1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡓࡆࡖࠪᦍ"),
  bstack1l1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡘࡅࡇࡗࡖࡉࡉ࠭ᦎ"),
  bstack1l1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡁࡃࡑࡕࡘࡊࡊࠧᦏ"),
  bstack1l1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᦐ"),
  bstack1l1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨᦑ"),
  bstack1l1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡉࡏࡘࡄࡐࡎࡊࠧᦒ"),
  bstack1l1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡁࡅࡆࡕࡉࡘ࡙࡟ࡖࡐࡕࡉࡆࡉࡈࡂࡄࡏࡉࠬᦓ"),
  bstack1l1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡗࡑࡒࡊࡒ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫᦔ"),
  bstack1l1ll1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤ࡚ࡉࡎࡇࡇࡣࡔ࡛ࡔࠨᦕ"),
  bstack1l1ll1_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬᦖ"),
  bstack1l1ll1_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡔࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡈࡐࡕࡗࡣ࡚ࡔࡒࡆࡃࡆࡌࡆࡈࡌࡆࠩᦗ"),
  bstack1l1ll1_opy_ (u"ࠧࡆࡔࡕࡣࡕࡘࡏ࡙࡛ࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧᦘ"),
  bstack1l1ll1_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡒࡔ࡚࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࠩᦙ"),
  bstack1l1ll1_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡗࡋࡓࡐࡎࡘࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨᦚ"),
  bstack1l1ll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡎࡃࡑࡈࡆ࡚ࡏࡓ࡛ࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩᦛ"),
]
bstack1l1llllll1_opy_ = bstack1l1ll1_opy_ (u"ࠫ࠳࠵ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡧࡲࡵ࡫ࡩࡥࡨࡺࡳ࠰ࠩᦜ")
bstack1ll11l1lll_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠬࢄࠧᦝ")), bstack1l1ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᦞ"), bstack1l1ll1_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᦟ"))
bstack11lll111l11_opy_ = bstack1l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡰࡪࠩᦠ")
bstack11ll11111l1_opy_ = [ bstack1l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᦡ"), bstack1l1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᦢ"), bstack1l1ll1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪᦣ"), bstack1l1ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᦤ")]
bstack11lll1ll1_opy_ = [ bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᦥ"), bstack1l1ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ᦦ"), bstack1l1ll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧᦧ"), bstack1l1ll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᦨ") ]
bstack11lllll111_opy_ = [ bstack1l1ll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᦩ") ]
bstack11l1lll11l1_opy_ = [ bstack1l1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᦪ") ]
bstack1ll1ll111l_opy_ = 360
bstack11ll11ll1ll_opy_ = bstack1l1ll1_opy_ (u"ࠧࡧࡰࡱ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧᦫ")
bstack11l1lll1ll1_opy_ = bstack1l1ll1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰࡫ࡶࡷࡺ࡫ࡳࠣ᦬")
bstack11ll1111l1l_opy_ = bstack1l1ll1_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠥ᦭")
bstack11ll1lll1l1_opy_ = bstack1l1ll1_opy_ (u"ࠣࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡷࡩࡸࡺࡳࠡࡣࡵࡩࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡔ࡙ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠧࡶࠤࡦࡴࡤࠡࡣࡥࡳࡻ࡫ࠠࡧࡱࡵࠤࡆࡴࡤࡳࡱ࡬ࡨࠥࡪࡥࡷ࡫ࡦࡩࡸ࠴ࠢ᦮")
bstack11ll1l11l1l_opy_ = bstack1l1ll1_opy_ (u"ࠤ࠴࠵࠳࠶ࠢ᦯")
bstack111l1l1l1l_opy_ = {
  bstack1l1ll1_opy_ (u"ࠪࡔࡆ࡙ࡓࠨᦰ"): bstack1l1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᦱ"),
  bstack1l1ll1_opy_ (u"ࠬࡌࡁࡊࡎࠪᦲ"): bstack1l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᦳ"),
  bstack1l1ll1_opy_ (u"ࠧࡔࡍࡌࡔࠬᦴ"): bstack1l1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᦵ")
}
bstack11111l1l_opy_ = [
  bstack1l1ll1_opy_ (u"ࠤࡪࡩࡹࠨᦶ"),
  bstack1l1ll1_opy_ (u"ࠥ࡫ࡴࡈࡡࡤ࡭ࠥᦷ"),
  bstack1l1ll1_opy_ (u"ࠦ࡬ࡵࡆࡰࡴࡺࡥࡷࡪࠢᦸ"),
  bstack1l1ll1_opy_ (u"ࠧࡸࡥࡧࡴࡨࡷ࡭ࠨᦹ"),
  bstack1l1ll1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧᦺ"),
  bstack1l1ll1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᦻ"),
  bstack1l1ll1_opy_ (u"ࠣࡵࡸࡦࡲ࡯ࡴࡆ࡮ࡨࡱࡪࡴࡴࠣᦼ"),
  bstack1l1ll1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨᦽ"),
  bstack1l1ll1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨᦾ"),
  bstack1l1ll1_opy_ (u"ࠦࡨࡲࡥࡢࡴࡈࡰࡪࡳࡥ࡯ࡶࠥᦿ"),
  bstack1l1ll1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࡸࠨᧀ"),
  bstack1l1ll1_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹࠨᧁ"),
  bstack1l1ll1_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡂࡵࡼࡲࡨ࡙ࡣࡳ࡫ࡳࡸࠧᧂ"),
  bstack1l1ll1_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢᧃ"),
  bstack1l1ll1_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᧄ"),
  bstack1l1ll1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡘࡴࡻࡣࡩࡃࡦࡸ࡮ࡵ࡮ࠣᧅ"),
  bstack1l1ll1_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡒࡻ࡬ࡵ࡫ࡗࡳࡺࡩࡨࠣᧆ"),
  bstack1l1ll1_opy_ (u"ࠧࡹࡨࡢ࡭ࡨࠦᧇ"),
  bstack1l1ll1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࡆࡶࡰࠣᧈ")
]
bstack11ll1111ll1_opy_ = [
  bstack1l1ll1_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨᧉ"),
  bstack1l1ll1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᧊"),
  bstack1l1ll1_opy_ (u"ࠤࡤࡹࡹࡵࠢ᧋"),
  bstack1l1ll1_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥ᧌"),
  bstack1l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᧍")
]
bstack1lll11l1l_opy_ = {
  bstack1l1ll1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦ᧎"): [bstack1l1ll1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ᧏")],
  bstack1l1ll1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᧐"): [bstack1l1ll1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᧑")],
  bstack1l1ll1_opy_ (u"ࠤࡤࡹࡹࡵࠢ᧒"): [bstack1l1ll1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢ᧓"), bstack1l1ll1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢ᧔"), bstack1l1ll1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ᧕"), bstack1l1ll1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ᧖")],
  bstack1l1ll1_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢ᧗"): [bstack1l1ll1_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣ᧘")],
  bstack1l1ll1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ᧙"): [bstack1l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ᧚")],
}
bstack11l1ll11l1l_opy_ = {
  bstack1l1ll1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ᧛"): bstack1l1ll1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦ᧜"),
  bstack1l1ll1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥ᧝"): bstack1l1ll1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᧞"),
  bstack1l1ll1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧ᧟"): bstack1l1ll1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦ᧠"),
  bstack1l1ll1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨ᧡"): bstack1l1ll1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨ᧢"),
  bstack1l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ᧣"): bstack1l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ᧤")
}
bstack1111lll1l1_opy_ = {
  bstack1l1ll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ᧥"): bstack1l1ll1_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡔࡧࡷࡹࡵ࠭᧦"),
  bstack1l1ll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ᧧"): bstack1l1ll1_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡗࡩࡦࡸࡤࡰࡹࡱࠫ᧨"),
  bstack1l1ll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ᧩"): bstack1l1ll1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡗࡪࡺࡵࡱࠩ᧪"),
  bstack1l1ll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ᧫"): bstack1l1ll1_opy_ (u"ࠧࡕࡧࡶࡸ࡚ࠥࡥࡢࡴࡧࡳࡼࡴࠧ᧬")
}
bstack11l1ll11l11_opy_ = 65536
bstack11l1llll111_opy_ = bstack1l1ll1_opy_ (u"ࠨ࠰࠱࠲ࡠ࡚ࡒࡖࡐࡆࡅ࡙ࡋࡄ࡞ࠩ᧭")
bstack11l1ll1ll1l_opy_ = [
      bstack1l1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ᧮"), bstack1l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭᧯"), bstack1l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ᧰"), bstack1l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ᧱"), bstack1l1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨ᧲"),
      bstack1l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ᧳"), bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ᧴"), bstack1l1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ᧵"), bstack1l1ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫ᧶"),
      bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᧷"), bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᧸"), bstack1l1ll1_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩ᧹")
    ]
bstack11l1lllll1l_opy_= {
  bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᧺"): bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᧻"),
  bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭᧼"): bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ᧽"),
  bstack1l1ll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ᧾"): bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᧿"),
  bstack1l1ll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᨀ"): bstack1l1ll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᨁ"),
  bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᨂ"): bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᨃ"),
  bstack1l1ll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᨄ"): bstack1l1ll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᨅ"),
  bstack1l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᨆ"): bstack1l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᨇ"),
  bstack1l1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᨈ"): bstack1l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᨉ"),
  bstack1l1ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᨊ"): bstack1l1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᨋ"),
  bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩᨌ"): bstack1l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪᨍ"),
  bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᨎ"): bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᨏ"),
  bstack1l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᨐ"): bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᨑ"),
  bstack1l1ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬᨒ"): bstack1l1ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ᨓ"),
  bstack1l1ll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᨔ"): bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᨕ"),
  bstack1l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᨖ"): bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᨗ"),
  bstack1l1ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸᨘ࠭"): bstack1l1ll1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧᨙ"),
  bstack1l1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᨚ"): bstack1l1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᨛ"),
  bstack1l1ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬ᨜"): bstack1l1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᨝"),
  bstack1l1ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫ᨞"): bstack1l1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ᨟"),
  bstack1l1ll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᨠ"): bstack1l1ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᨡ"),
  bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨢ"): bstack1l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᨣ"),
  bstack1l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᨤ"): bstack1l1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᨥ"),
  bstack1l1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᨦ"): bstack1l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᨧ"),
  bstack1l1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᨨ"): bstack1l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᨩ"),
  bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᨪ"): bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫᨫ"),
  bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᨬ"): bstack1l1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᨭ")
}
bstack11l1lll11ll_opy_ = [bstack1l1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᨮ"), bstack1l1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᨯ")]
bstack1ll11l111_opy_ = (bstack1l1ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᨰ"),)
bstack11l1llll1ll_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡥ࡭࠲ࡺ࠶࠵ࡵࡱࡦࡤࡸࡪࡥࡣ࡭࡫ࠪᨱ")
bstack11lll1111_opy_ = bstack1l1ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠰ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠯ࡷ࠳࠲࡫ࡷ࡯ࡤࡴ࠱ࠥᨲ")
bstack1111ll11_opy_ = bstack1l1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡪࡶ࡮ࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡨࡦࡹࡨࡣࡱࡤࡶࡩ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࠢᨳ")
bstack11lll1llll_opy_ = bstack1l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠲ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠥᨴ")
class EVENTS(Enum):
  bstack11ll1111l11_opy_ = bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡰ࠳࠴ࡽ࠿ࡶࡲࡪࡰࡷ࠱ࡧࡻࡩ࡭ࡦ࡯࡭ࡳࡱࠧᨵ")
  bstack1l11llll1l_opy_ = bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯ࡩࡦࡴࡵࡱࠩᨶ") # final bstack11l1ll11lll_opy_
  bstack11l1llllll1_opy_ = bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡳࡪ࡬ࡰࡩࡶࠫᨷ")
  bstack11llllllll_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩᨸ") #shift post bstack11ll111l1l1_opy_
  bstack11ll111l_opy_ = bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨᨹ") #shift post bstack11ll111l1l1_opy_
  bstack11l1lll1lll_opy_ = bstack1l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡥࡴࡶ࡫ࡹࡧ࠭ᨺ") #shift
  bstack11l1lllllll_opy_ = bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧᨻ") #shift
  bstack11llll1l_opy_ = bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠾࡭ࡻࡢ࠮࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠬᨼ")
  bstack1ll1l111l11_opy_ = bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡳࡢࡸࡨ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷࠬᨽ")
  bstack1lll1l1ll_opy_ = bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡱࡧࡵࡪࡴࡸ࡭ࡴࡥࡤࡲࠬᨾ")
  bstack11l1ll111l_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡲ࡯ࡤࡣ࡯ࠫᨿ") #shift
  bstack11l1l11111_opy_ = bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡥࡵࡶ࠭ࡶࡲ࡯ࡳࡦࡪࠧᩀ") #shift
  bstack11l1ll111_opy_ = bstack1l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡤ࡫࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠭ᩁ")
  bstack11l1lll1_opy_ = bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪᩂ") #shift
  bstack1ll1l11ll1_opy_ = bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿࡭ࡥࡵ࠯ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠯ࡵࡩࡸࡻ࡬ࡵࡵࠪᩃ") #shift
  bstack11ll1111111_opy_ = bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿࠧᩄ") #shift
  bstack1l1l1l1l1l1_opy_ = bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᩅ")
  bstack1ll1llllll_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡳࡵࡣࡷࡹࡸ࠭ᩆ") #shift
  bstack1ll11ll1l_opy_ = bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡨࡶࡤ࠰ࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠧᩇ")
  bstack11l1lllll11_opy_ = bstack1l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡲࡰࡺࡼ࠱ࡸ࡫ࡴࡶࡲࠪᩈ") #shift
  bstack1l1l11ll11_opy_ = bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡳࡦࡶࡸࡴࠬᩉ")
  bstack11ll111l111_opy_ = bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡳ࡯ࡣࡳࡷ࡭ࡵࡴࠨᩊ") # not bstack11l1ll1l11l_opy_ in python
  bstack11l11l1l11_opy_ = bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡳࡸ࡭ࡹ࠭ᩋ") # used in bstack11l1ll1ll11_opy_
  bstack1ll11111l1_opy_ = bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡪࡩࡹ࠭ᩌ") # used in bstack11l1ll1ll11_opy_
  bstack1l1lll11ll_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽࡬ࡴࡵ࡫ࠨᩍ")
  bstack1ll11ll1l1_opy_ = bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠬᩎ")
  bstack1lll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠬᩏ") #
  bstack1lll11llll_opy_ = bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡩࡸࡩࡷࡧࡵ࠱ࡹࡧ࡫ࡦࡕࡦࡶࡪ࡫࡮ࡔࡪࡲࡸࠬᩐ")
  bstack11l1l11l1_opy_ = bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾࡀࡡࡶࡶࡲ࠱ࡨࡧࡰࡵࡷࡵࡩࠬᩑ")
  bstack1l1ll1l1l_opy_ = bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡩ࠲ࡺࡥࡴࡶࠪᩒ")
  bstack1111ll1ll_opy_ = bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡳࡸࡺ࠭ࡵࡧࡶࡸࠬᩓ")
  bstack11l11l1111_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡷ࡫࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨᩔ") #shift
  bstack1l11lllll_opy_ = bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᩕ") #shift
  bstack11l1ll1llll_opy_ = bstack1l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫᩖ")
  bstack11ll11111ll_opy_ = bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡫ࡧࡰࡪ࠳ࡴࡪ࡯ࡨࡳࡺࡺࠧᩗ")
  bstack1lll111ll1l_opy_ = bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡸࡺࡡࡳࡶࠪᩘ")
  bstack11l1llll11l_opy_ = bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠧᩙ")
  bstack11ll111111l_opy_ = bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡣࡩࡧࡦ࡯࠲ࡻࡰࡥࡣࡷࡩࠬᩚ")
  bstack1lll1lllll1_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠭ᩛ")
  bstack1llll111111_opy_ = bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡨࡵ࡮࡯ࡧࡦࡸࠬᩜ")
  bstack1llll11l1ll_opy_ = bstack1l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡲࡲ࠲ࡹࡴࡰࡲࠪᩝ")
  bstack1lll1lll1l1_opy_ = bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡳࡵࡣࡵࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࠨᩞ")
  bstack1ll1lllllll_opy_ = bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡤࡱࡱࡲࡪࡩࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱࠫ᩟")
  bstack11l1lll1l11_opy_ = bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸ᩠ࠬ")
  bstack11ll111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡩ࡭ࡳࡪࡎࡦࡣࡵࡩࡸࡺࡈࡶࡤࠪᩡ")
  bstack1l11ll1l1ll_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡋࡱ࡭ࡹ࠭ᩢ")
  bstack1l11lll1ll1_opy_ = bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡸࡴࠨᩣ")
  bstack1ll1l111ll1_opy_ = bstack1l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡈࡵ࡮ࡧ࡫ࡪࠫᩤ")
  bstack11l1lll111l_opy_ = bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡀ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡉ࡯࡯ࡨ࡬࡫ࠬᩥ")
  bstack1ll1111l1l1_opy_ = bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࡫ࡖࡩࡱ࡬ࡈࡦࡣ࡯ࡗࡹ࡫ࡰࠨᩦ")
  bstack1ll1111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࡬ࡗࡪࡲࡦࡉࡧࡤࡰࡌ࡫ࡴࡓࡧࡶࡹࡱࡺࠧᩧ")
  bstack1l1llll11ll_opy_ = bstack1l1ll1_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡇࡹࡩࡳࡺࠧᩨ")
  bstack1l1ll11llll_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡪࡹࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡆࡸࡨࡲࡹ࠭ᩩ")
  bstack1l1ll1ll1ll_opy_ = bstack1l1ll1_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻࡮ࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࡊࡼࡥ࡯ࡶࠪᩪ")
  bstack11l1ll11ll1_opy_ = bstack1l1ll1_opy_ (u"ࠨࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡨࡲࡶࡻࡥࡶࡧࡗࡩࡸࡺࡅࡷࡧࡱࡸࠬᩫ")
  bstack1l11ll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺ࡯ࡱࠩᩬ")
  bstack1lll1l1l111_opy_ = bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱ࠺ࡰࡰࡖࡸࡴࡶࠧᩭ")
class STAGE(Enum):
  bstack111lll111_opy_ = bstack1l1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪᩮ")
  END = bstack1l1ll1_opy_ (u"ࠬ࡫࡮ࡥࠩᩯ")
  bstack1l1ll11ll1_opy_ = bstack1l1ll1_opy_ (u"࠭ࡳࡪࡰࡪࡰࡪ࠭ᩰ")
bstack1l111ll11_opy_ = {
  bstack1l1ll1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧᩱ"): bstack1l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᩲ"),
  bstack1l1ll1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ᩳ"): bstack1l1ll1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᩴ")
}
PLAYWRIGHT_HUB_URL = bstack1l1ll1_opy_ (u"ࠦࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂࠨ᩵")
bstack1ll11l111ll_opy_ = 98
bstack1ll1l111l1l_opy_ = 100
bstack11111l1lll_opy_ = {
  bstack1l1ll1_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫ᩶"): bstack1l1ll1_opy_ (u"࠭࠭࠮ࡴࡨࡶࡺࡴࡳࠨ᩷"),
  bstack1l1ll1_opy_ (u"ࠧࡥࡧ࡯ࡥࡾ࠭᩸"): bstack1l1ll1_opy_ (u"ࠨ࠯࠰ࡶࡪࡸࡵ࡯ࡵ࠰ࡨࡪࡲࡡࡺࠩ᩹"),
  bstack1l1ll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧ᩺"): 0
}
bstack11ll1111lll_opy_ = bstack1l1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥ᩻")
bstack11l1ll1lll1_opy_ = bstack1l1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣ᩼")