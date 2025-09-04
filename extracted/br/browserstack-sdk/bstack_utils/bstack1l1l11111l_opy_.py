# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import re
from bstack_utils.bstack1ll1l11l11_opy_ import bstack1lllllll1l11_opy_
def bstack1llllllllll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1111l1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὢ")):
        return bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧὣ")
    elif fixture_name.startswith(bstack1111l1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὤ")):
        return bstack1111l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧὥ")
    elif fixture_name.startswith(bstack1111l1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὦ")):
        return bstack1111l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧὧ")
    elif fixture_name.startswith(bstack1111l1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩὨ")):
        return bstack1111l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧὩ")
def bstack1lllllllllll_opy_(fixture_name):
    return bool(re.match(bstack1111l1l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫὪ"), fixture_name))
def bstack1lllllllll11_opy_(fixture_name):
    return bool(re.match(bstack1111l1l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨὫ"), fixture_name))
def bstack1lllllll1l1l_opy_(fixture_name):
    return bool(re.match(bstack1111l1l_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨὬ"), fixture_name))
def bstack11111111111_opy_(fixture_name):
    if fixture_name.startswith(bstack1111l1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫὭ")):
        return bstack1111l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫὮ"), bstack1111l1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩὯ")
    elif fixture_name.startswith(bstack1111l1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬὰ")):
        return bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬά"), bstack1111l1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫὲ")
    elif fixture_name.startswith(bstack1111l1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭έ")):
        return bstack1111l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ὴ"), bstack1111l1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧή")
    elif fixture_name.startswith(bstack1111l1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὶ")):
        return bstack1111l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧί"), bstack1111l1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩὸ")
    return None, None
def bstack1lllllll1ll1_opy_(hook_name):
    if hook_name in [bstack1111l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ό"), bstack1111l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪὺ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lllllllll1l_opy_(hook_name):
    if hook_name in [bstack1111l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪύ"), bstack1111l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩὼ")]:
        return bstack1111l1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩώ")
    elif hook_name in [bstack1111l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ὾"), bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ὿")]:
        return bstack1111l1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᾀ")
    elif hook_name in [bstack1111l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᾁ"), bstack1111l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᾂ")]:
        return bstack1111l1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᾃ")
    elif hook_name in [bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᾄ"), bstack1111l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᾅ")]:
        return bstack1111l1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᾆ")
    return hook_name
def bstack1111111111l_opy_(node, scenario):
    if hasattr(node, bstack1111l1l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᾇ")):
        parts = node.nodeid.rsplit(bstack1111l1l_opy_ (u"ࠣ࡝ࠥᾈ"))
        params = parts[-1]
        return bstack1111l1l_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᾉ").format(scenario.name, params)
    return scenario.name
def bstack1lllllll1lll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1111l1l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᾊ")):
            examples = list(node.callspec.params[bstack1111l1l_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᾋ")].values())
        return examples
    except:
        return []
def bstack1llllllll11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llllllll111_opy_(report):
    try:
        status = bstack1111l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᾌ")
        if report.passed or (report.failed and hasattr(report, bstack1111l1l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᾍ"))):
            status = bstack1111l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᾎ")
        elif report.skipped:
            status = bstack1111l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᾏ")
        bstack1lllllll1l11_opy_(status)
    except:
        pass
def bstack11l1llllll_opy_(status):
    try:
        bstack1llllllll1ll_opy_ = bstack1111l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᾐ")
        if status == bstack1111l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᾑ"):
            bstack1llllllll1ll_opy_ = bstack1111l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᾒ")
        elif status == bstack1111l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᾓ"):
            bstack1llllllll1ll_opy_ = bstack1111l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᾔ")
        bstack1lllllll1l11_opy_(bstack1llllllll1ll_opy_)
    except:
        pass
def bstack1llllllll1l1_opy_(item=None, report=None, summary=None, extra=None):
    return