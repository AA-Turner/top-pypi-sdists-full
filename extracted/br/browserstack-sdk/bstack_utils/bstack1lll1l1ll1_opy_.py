# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import re
from bstack_utils.bstack1lll11111l_opy_ import bstack111l1l11lll_opy_
def bstack111l1l1l1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵍ")):
        return bstack11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᵎ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵏ")):
        return bstack11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ᵐ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵑ")):
        return bstack11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᵒ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵓ")):
        return bstack11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭ᵔ")
def bstack111l1l1l11l_opy_(fixture_name):
    return bool(re.match(bstack11lll_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࢁࡳ࡯ࡥࡷ࡯ࡩ࠮ࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᵕ"), fixture_name))
def bstack111l1l11l1l_opy_(fixture_name):
    return bool(re.match(bstack11lll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᵖ"), fixture_name))
def bstack111l11llll1_opy_(fixture_name):
    return bool(re.match(bstack11lll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᵗ"), fixture_name))
def bstack111l11lllll_opy_(fixture_name):
    if fixture_name.startswith(bstack11lll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵘ")):
        return bstack11lll_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᵙ"), bstack11lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᵚ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵛ")):
        return bstack11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᵜ"), bstack11lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᵝ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵞ")):
        return bstack11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᵟ"), bstack11lll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᵠ")
    elif fixture_name.startswith(bstack11lll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵡ")):
        return bstack11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭ᵢ"), bstack11lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨᵣ")
    return None, None
def bstack111l1l1111l_opy_(hook_name):
    if hook_name in [bstack11lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᵤ"), bstack11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᵥ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1l111l1_opy_(hook_name):
    if hook_name in [bstack11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵦ"), bstack11lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᵧ")]:
        return bstack11lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᵨ")
    elif hook_name in [bstack11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᵩ"), bstack11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᵪ")]:
        return bstack11lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᵫ")
    elif hook_name in [bstack11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᵬ"), bstack11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᵭ")]:
        return bstack11lll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᵮ")
    elif hook_name in [bstack11lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᵯ"), bstack11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᵰ")]:
        return bstack11lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨᵱ")
    return hook_name
def bstack111l1l11l11_opy_(node, scenario):
    if hasattr(node, bstack11lll_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᵲ")):
        parts = node.nodeid.rsplit(bstack11lll_opy_ (u"ࠢ࡜ࠤᵳ"))
        params = parts[-1]
        return bstack11lll_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᵴ").format(scenario.name, params)
    return scenario.name
def bstack111l1l1l1ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᵵ")):
            examples = list(node.callspec.params[bstack11lll_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᵶ")].values())
        return examples
    except:
        return []
def bstack111l1l111ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l11111_opy_(report):
    try:
        status = bstack11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᵷ")
        if report.passed or (report.failed and hasattr(report, bstack11lll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᵸ"))):
            status = bstack11lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᵹ")
        elif report.skipped:
            status = bstack11lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᵺ")
        bstack111l1l11lll_opy_(status)
    except:
        pass
def bstack11lll111_opy_(status):
    try:
        bstack111l1l1l111_opy_ = bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᵻ")
        if status == bstack11lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᵼ"):
            bstack111l1l1l111_opy_ = bstack11lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᵽ")
        elif status == bstack11lll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᵾ"):
            bstack111l1l1l111_opy_ = bstack11lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᵿ")
        bstack111l1l11lll_opy_(bstack111l1l1l111_opy_)
    except:
        pass
def bstack111l1l11ll1_opy_(item=None, report=None, summary=None, extra=None):
    return