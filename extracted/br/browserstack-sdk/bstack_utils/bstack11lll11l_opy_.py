# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import re
from bstack_utils.bstack11ll1111l_opy_ import bstack111l1l11ll1_opy_
def bstack111l1l1111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵂ")):
        return bstack1l11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵃ")
    elif fixture_name.startswith(bstack1l11lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵄ")):
        return bstack1l11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᵅ")
    elif fixture_name.startswith(bstack1l11lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵆ")):
        return bstack1l11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵇ")
    elif fixture_name.startswith(bstack1l11lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵈ")):
        return bstack1l11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩᵉ")
def bstack111l1l1l111_opy_(fixture_name):
    return bool(re.match(bstack1l11lll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᵊ"), fixture_name))
def bstack111l1l11l1l_opy_(fixture_name):
    return bool(re.match(bstack1l11lll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᵋ"), fixture_name))
def bstack111l1l1l1l1_opy_(fixture_name):
    return bool(re.match(bstack1l11lll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᵌ"), fixture_name))
def bstack111l1l11111_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵍ")):
        return bstack1l11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᵎ"), bstack1l11lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᵏ")
    elif fixture_name.startswith(bstack1l11lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᵐ")):
        return bstack1l11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᵑ"), bstack1l11lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᵒ")
    elif fixture_name.startswith(bstack1l11lll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵓ")):
        return bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᵔ"), bstack1l11lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᵕ")
    elif fixture_name.startswith(bstack1l11lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵖ")):
        return bstack1l11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩᵗ"), bstack1l11lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᵘ")
    return None, None
def bstack111l1l1l1ll_opy_(hook_name):
    if hook_name in [bstack1l11lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᵙ"), bstack1l11lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᵚ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1l111l1_opy_(hook_name):
    if hook_name in [bstack1l11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᵛ"), bstack1l11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᵜ")]:
        return bstack1l11lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᵝ")
    elif hook_name in [bstack1l11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᵞ"), bstack1l11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᵟ")]:
        return bstack1l11lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᵠ")
    elif hook_name in [bstack1l11lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᵡ"), bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᵢ")]:
        return bstack1l11lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᵣ")
    elif hook_name in [bstack1l11lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᵤ"), bstack1l11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᵥ")]:
        return bstack1l11lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᵦ")
    return hook_name
def bstack111l1l11l11_opy_(node, scenario):
    if hasattr(node, bstack1l11lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᵧ")):
        parts = node.nodeid.rsplit(bstack1l11lll_opy_ (u"ࠥ࡟ࠧᵨ"))
        params = parts[-1]
        return bstack1l11lll_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᵩ").format(scenario.name, params)
    return scenario.name
def bstack111l1l1ll1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l11lll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᵪ")):
            examples = list(node.callspec.params[bstack1l11lll_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬᵫ")].values())
        return examples
    except:
        return []
def bstack111l1l111ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l1l11l_opy_(report):
    try:
        status = bstack1l11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᵬ")
        if report.passed or (report.failed and hasattr(report, bstack1l11lll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᵭ"))):
            status = bstack1l11lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᵮ")
        elif report.skipped:
            status = bstack1l11lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᵯ")
        bstack111l1l11ll1_opy_(status)
    except:
        pass
def bstack1ll1l111l1_opy_(status):
    try:
        bstack111l1l1ll11_opy_ = bstack1l11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᵰ")
        if status == bstack1l11lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᵱ"):
            bstack111l1l1ll11_opy_ = bstack1l11lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᵲ")
        elif status == bstack1l11lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᵳ"):
            bstack111l1l1ll11_opy_ = bstack1l11lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᵴ")
        bstack111l1l11ll1_opy_(bstack111l1l1ll11_opy_)
    except:
        pass
def bstack111l1l11lll_opy_(item=None, report=None, summary=None, extra=None):
    return