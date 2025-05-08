# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import re
from bstack_utils.bstack11ll1lll1l_opy_ import bstack111l1l1ll1l_opy_
def bstack111l1l11ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵉ")):
        return bstack1l1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵊ")
    elif fixture_name.startswith(bstack1l1lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵋ")):
        return bstack1l1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᵌ")
    elif fixture_name.startswith(bstack1l1lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵍ")):
        return bstack1l1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵎ")
    elif fixture_name.startswith(bstack1l1lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵏ")):
        return bstack1l1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩᵐ")
def bstack111l1l111ll_opy_(fixture_name):
    return bool(re.match(bstack1l1lll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᵑ"), fixture_name))
def bstack111l1l111l1_opy_(fixture_name):
    return bool(re.match(bstack1l1lll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᵒ"), fixture_name))
def bstack111l1l11111_opy_(fixture_name):
    return bool(re.match(bstack1l1lll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᵓ"), fixture_name))
def bstack111l1l11l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵔ")):
        return bstack1l1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᵕ"), bstack1l1lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᵖ")
    elif fixture_name.startswith(bstack1l1lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᵗ")):
        return bstack1l1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᵘ"), bstack1l1lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᵙ")
    elif fixture_name.startswith(bstack1l1lll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵚ")):
        return bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᵛ"), bstack1l1lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᵜ")
    elif fixture_name.startswith(bstack1l1lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵝ")):
        return bstack1l1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩᵞ"), bstack1l1lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᵟ")
    return None, None
def bstack111l1l1l1ll_opy_(hook_name):
    if hook_name in [bstack1l1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᵠ"), bstack1l1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᵡ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1l1l11l_opy_(hook_name):
    if hook_name in [bstack1l1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᵢ"), bstack1l1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᵣ")]:
        return bstack1l1lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᵤ")
    elif hook_name in [bstack1l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᵥ"), bstack1l1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᵦ")]:
        return bstack1l1lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᵧ")
    elif hook_name in [bstack1l1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᵨ"), bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᵩ")]:
        return bstack1l1lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᵪ")
    elif hook_name in [bstack1l1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᵫ"), bstack1l1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᵬ")]:
        return bstack1l1lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᵭ")
    return hook_name
def bstack111l1l11l11_opy_(node, scenario):
    if hasattr(node, bstack1l1lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᵮ")):
        parts = node.nodeid.rsplit(bstack1l1lll_opy_ (u"ࠥ࡟ࠧᵯ"))
        params = parts[-1]
        return bstack1l1lll_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᵰ").format(scenario.name, params)
    return scenario.name
def bstack111l1l1ll11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1lll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᵱ")):
            examples = list(node.callspec.params[bstack1l1lll_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬᵲ")].values())
        return examples
    except:
        return []
def bstack111l1l11lll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l1111l_opy_(report):
    try:
        status = bstack1l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᵳ")
        if report.passed or (report.failed and hasattr(report, bstack1l1lll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᵴ"))):
            status = bstack1l1lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᵵ")
        elif report.skipped:
            status = bstack1l1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᵶ")
        bstack111l1l1ll1l_opy_(status)
    except:
        pass
def bstack11l1111ll_opy_(status):
    try:
        bstack111l1l1l111_opy_ = bstack1l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᵷ")
        if status == bstack1l1lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᵸ"):
            bstack111l1l1l111_opy_ = bstack1l1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᵹ")
        elif status == bstack1l1lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᵺ"):
            bstack111l1l1l111_opy_ = bstack1l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᵻ")
        bstack111l1l1ll1l_opy_(bstack111l1l1l111_opy_)
    except:
        pass
def bstack111l1l1l1l1_opy_(item=None, report=None, summary=None, extra=None):
    return