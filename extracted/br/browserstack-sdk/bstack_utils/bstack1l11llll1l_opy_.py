# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import re
from bstack_utils.bstack1l1l11l111_opy_ import bstack111l1l1ll11_opy_
def bstack111l1l1l1ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1llllll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵄ")):
        return bstack1llllll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᵅ")
    elif fixture_name.startswith(bstack1llllll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵆ")):
        return bstack1llllll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᵇ")
    elif fixture_name.startswith(bstack1llllll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵈ")):
        return bstack1llllll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᵉ")
    elif fixture_name.startswith(bstack1llllll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵊ")):
        return bstack1llllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᵋ")
def bstack111l1l11l1l_opy_(fixture_name):
    return bool(re.match(bstack1llllll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᵌ"), fixture_name))
def bstack111l1l111ll_opy_(fixture_name):
    return bool(re.match(bstack1llllll_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᵍ"), fixture_name))
def bstack111l1l11111_opy_(fixture_name):
    return bool(re.match(bstack1llllll_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᵎ"), fixture_name))
def bstack111l1l1111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1llllll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵏ")):
        return bstack1llllll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᵐ"), bstack1llllll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᵑ")
    elif fixture_name.startswith(bstack1llllll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵒ")):
        return bstack1llllll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᵓ"), bstack1llllll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᵔ")
    elif fixture_name.startswith(bstack1llllll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵕ")):
        return bstack1llllll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᵖ"), bstack1llllll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᵗ")
    elif fixture_name.startswith(bstack1llllll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵘ")):
        return bstack1llllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᵙ"), bstack1llllll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᵚ")
    return None, None
def bstack111l1l1l111_opy_(hook_name):
    if hook_name in [bstack1llllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᵛ"), bstack1llllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᵜ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1l1l11l_opy_(hook_name):
    if hook_name in [bstack1llllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᵝ"), bstack1llllll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᵞ")]:
        return bstack1llllll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᵟ")
    elif hook_name in [bstack1llllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᵠ"), bstack1llllll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᵡ")]:
        return bstack1llllll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᵢ")
    elif hook_name in [bstack1llllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵣ"), bstack1llllll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᵤ")]:
        return bstack1llllll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᵥ")
    elif hook_name in [bstack1llllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᵦ"), bstack1llllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᵧ")]:
        return bstack1llllll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᵨ")
    return hook_name
def bstack111l1l11lll_opy_(node, scenario):
    if hasattr(node, bstack1llllll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᵩ")):
        parts = node.nodeid.rsplit(bstack1llllll_opy_ (u"ࠧࡡࠢᵪ"))
        params = parts[-1]
        return bstack1llllll_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᵫ").format(scenario.name, params)
    return scenario.name
def bstack111l1l1l1l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1llllll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᵬ")):
            examples = list(node.callspec.params[bstack1llllll_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᵭ")].values())
        return examples
    except:
        return []
def bstack111l1l11l11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l111l1_opy_(report):
    try:
        status = bstack1llllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᵮ")
        if report.passed or (report.failed and hasattr(report, bstack1llllll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᵯ"))):
            status = bstack1llllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᵰ")
        elif report.skipped:
            status = bstack1llllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᵱ")
        bstack111l1l1ll11_opy_(status)
    except:
        pass
def bstack1l1l1llll1_opy_(status):
    try:
        bstack111l1l11ll1_opy_ = bstack1llllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᵲ")
        if status == bstack1llllll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᵳ"):
            bstack111l1l11ll1_opy_ = bstack1llllll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᵴ")
        elif status == bstack1llllll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᵵ"):
            bstack111l1l11ll1_opy_ = bstack1llllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᵶ")
        bstack111l1l1ll11_opy_(bstack111l1l11ll1_opy_)
    except:
        pass
def bstack111l1l1ll1l_opy_(item=None, report=None, summary=None, extra=None):
    return