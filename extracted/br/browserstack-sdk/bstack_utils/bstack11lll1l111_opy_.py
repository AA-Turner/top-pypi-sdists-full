# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import re
from bstack_utils.bstack11l1111111_opy_ import bstack1llllll1l111_opy_
def bstack1lllllll11l1_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll11ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫὦ")):
        return bstack1ll11ll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫὧ")
    elif fixture_name.startswith(bstack1ll11ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫὨ")):
        return bstack1ll11ll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫὩ")
    elif fixture_name.startswith(bstack1ll11ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫὪ")):
        return bstack1ll11ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫὫ")
    elif fixture_name.startswith(bstack1ll11ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ὤ")):
        return bstack1ll11ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫὭ")
def bstack1llllll1llll_opy_(fixture_name):
    return bool(re.match(bstack1ll11ll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨὮ"), fixture_name))
def bstack1llllll1ll11_opy_(fixture_name):
    return bool(re.match(bstack1ll11ll_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬὯ"), fixture_name))
def bstack1lllllll11ll_opy_(fixture_name):
    return bool(re.match(bstack1ll11ll_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬὰ"), fixture_name))
def bstack1llllll1l11l_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll11ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨά")):
        return bstack1ll11ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨὲ"), bstack1ll11ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭έ")
    elif fixture_name.startswith(bstack1ll11ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩὴ")):
        return bstack1ll11ll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩή"), bstack1ll11ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨὶ")
    elif fixture_name.startswith(bstack1ll11ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪί")):
        return bstack1ll11ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪὸ"), bstack1ll11ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫό")
    elif fixture_name.startswith(bstack1ll11ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫὺ")):
        return bstack1ll11ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫύ"), bstack1ll11ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ὼ")
    return None, None
def bstack1llllll1ll1l_opy_(hook_name):
    if hook_name in [bstack1ll11ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪώ"), bstack1ll11ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ὾")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llllll1l1ll_opy_(hook_name):
    if hook_name in [bstack1ll11ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ὿"), bstack1ll11ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᾀ")]:
        return bstack1ll11ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᾁ")
    elif hook_name in [bstack1ll11ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᾂ"), bstack1ll11ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᾃ")]:
        return bstack1ll11ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᾄ")
    elif hook_name in [bstack1ll11ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᾅ"), bstack1ll11ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᾆ")]:
        return bstack1ll11ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᾇ")
    elif hook_name in [bstack1ll11ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᾈ"), bstack1ll11ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᾉ")]:
        return bstack1ll11ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᾊ")
    return hook_name
def bstack1llllll1l1l1_opy_(node, scenario):
    if hasattr(node, bstack1ll11ll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᾋ")):
        parts = node.nodeid.rsplit(bstack1ll11ll_opy_ (u"ࠧࡡࠢᾌ"))
        params = parts[-1]
        return bstack1ll11ll_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᾍ").format(scenario.name, params)
    return scenario.name
def bstack1lllllll1111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll11ll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᾎ")):
            examples = list(node.callspec.params[bstack1ll11ll_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᾏ")].values())
        return examples
    except:
        return []
def bstack1lllllll1l11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lllllll1l1l_opy_(report):
    try:
        status = bstack1ll11ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᾐ")
        if report.passed or (report.failed and hasattr(report, bstack1ll11ll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᾑ"))):
            status = bstack1ll11ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᾒ")
        elif report.skipped:
            status = bstack1ll11ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᾓ")
        bstack1llllll1l111_opy_(status)
    except:
        pass
def bstack111llll11_opy_(status):
    try:
        bstack1lllllll111l_opy_ = bstack1ll11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᾔ")
        if status == bstack1ll11ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᾕ"):
            bstack1lllllll111l_opy_ = bstack1ll11ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᾖ")
        elif status == bstack1ll11ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᾗ"):
            bstack1lllllll111l_opy_ = bstack1ll11ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᾘ")
        bstack1llllll1l111_opy_(bstack1lllllll111l_opy_)
    except:
        pass
def bstack1llllll1lll1_opy_(item=None, report=None, summary=None, extra=None):
    return