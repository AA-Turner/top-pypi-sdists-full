# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import re
from bstack_utils.bstack11l1l11l1_opy_ import bstack1llll111llll_opy_
from bstack_utils.bstack1llll11l11l_opy_ import bstack1lllll1ll11_opy_
def bstack1llll11l111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⃳")):
        return bstack1l1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⃴")
    elif fixture_name.startswith(bstack1l1111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⃵")):
        return bstack1l1111_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩ⃶")
    elif fixture_name.startswith(bstack1l1111_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⃷")):
        return bstack1l1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⃸")
    elif fixture_name.startswith(bstack1l1111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⃹")):
        return bstack1l1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩ⃺")
def bstack1llll11l1111_opy_(fixture_name):
    return bool(re.match(bstack1l1111_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭⃻"), fixture_name))
def bstack1llll111lll1_opy_(fixture_name):
    return bool(re.match(bstack1l1111_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪ⃼"), fixture_name))
def bstack1llll11l11ll_opy_(fixture_name):
    return bool(re.match(bstack1l1111_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪ⃽"), fixture_name))
def bstack1llll111ll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1111_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⃾")):
        return bstack1l1111_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⃿"), bstack1l1111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ℀")
    elif fixture_name.startswith(bstack1l1111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ℁")):
        return bstack1l1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧℂ"), bstack1l1111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭℃")
    elif fixture_name.startswith(bstack1l1111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ℄")):
        return bstack1l1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ℅"), bstack1l1111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ℆")
    elif fixture_name.startswith(bstack1l1111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩℇ")):
        return bstack1l1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩ℈"), bstack1l1111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ℉")
    return None, None
def bstack1llll11l11l1_opy_(hook_name):
    if hook_name in [bstack1l1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨℊ"), bstack1l1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬℋ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llll111l1l1_opy_(hook_name):
    if hook_name in [bstack1l1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬℌ"), bstack1l1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫℍ")]:
        return bstack1l1111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫℎ")
    elif hook_name in [bstack1l1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ℏ"), bstack1l1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ℐ")]:
        return bstack1l1111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ℑ")
    elif hook_name in [bstack1l1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧℒ"), bstack1l1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ℓ")]:
        return bstack1l1111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ℔")
    elif hook_name in [bstack1l1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨℕ"), bstack1l1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ№")]:
        return bstack1l1111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ℗")
    return hook_name
def bstack1llll11l1l1l_opy_(node, scenario):
    if hasattr(node, bstack1l1111_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫ℘")):
        parts = node.nodeid.rsplit(bstack1l1111_opy_ (u"ࠥ࡟ࠧℙ"))
        params = parts[-1]
        return bstack1l1111_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦℚ").format(scenario.name, params)
    return scenario.name
def bstack1llll11l1l11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1111_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧℛ")):
            examples = list(node.callspec.params[bstack1l1111_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬℜ")].values())
        return examples
    except:
        return []
def bstack1llll111ll11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llll111l1ll_opy_(report):
    try:
        status = bstack1l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧℝ")
        if report.passed or (report.failed and hasattr(report, bstack1l1111_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ℞"))):
            status = bstack1l1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ℟")
        elif report.skipped:
            status = bstack1l1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ℠")
        bstack1llll111llll_opy_(status)
    except:
        pass
def bstack1l1lll111_opy_(status):
    try:
        bstack1llll11l1ll1_opy_ = bstack1l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ℡")
        if status == bstack1l1111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ™"):
            bstack1llll11l1ll1_opy_ = bstack1l1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭℣")
        elif status == bstack1l1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨℤ"):
            bstack1llll11l1ll1_opy_ = bstack1l1111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ℥")
        bstack1llll111llll_opy_(bstack1llll11l1ll1_opy_)
    except:
        pass
def bstack1llll111l11l_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack111ll111ll_opy_():
    bstack1l1111_opy_ (u"ࠤࠥࠦࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡢࡰࡧࠤࡷ࡫ࡴࡶࡴࡱࠤ࡙ࡸࡵࡦࠢ࡬ࡪࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡ࡭ࡵࡨࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠢࠣࠤΩ")
    return bstack1lllll1ll11_opy_(bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡦࡸࡡ࡭࡮ࡨࡰࠬ℧"))