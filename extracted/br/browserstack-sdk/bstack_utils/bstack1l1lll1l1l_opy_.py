# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import re
from bstack_utils.bstack1l1l1l11_opy_ import bstack1111111l11l_opy_
def bstack1111111ll11_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὢ")):
        return bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧὣ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὤ")):
        return bstack1ll1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧὥ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὦ")):
        return bstack1ll1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧὧ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩὨ")):
        return bstack1ll1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧὩ")
def bstack1111111l1ll_opy_(fixture_name):
    return bool(re.match(bstack1ll1ll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫὪ"), fixture_name))
def bstack11111111ll1_opy_(fixture_name):
    return bool(re.match(bstack1ll1ll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨὫ"), fixture_name))
def bstack11111111l11_opy_(fixture_name):
    return bool(re.match(bstack1ll1ll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨὬ"), fixture_name))
def bstack1111111lll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫὭ")):
        return bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫὮ"), bstack1ll1ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩὯ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬὰ")):
        return bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬά"), bstack1ll1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫὲ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭έ")):
        return bstack1ll1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ὴ"), bstack1ll1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧή")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὶ")):
        return bstack1ll1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧί"), bstack1ll1ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩὸ")
    return None, None
def bstack111111l1111_opy_(hook_name):
    if hook_name in [bstack1ll1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ό"), bstack1ll1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪὺ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111111l1l1_opy_(hook_name):
    if hook_name in [bstack1ll1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪύ"), bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩὼ")]:
        return bstack1ll1ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩώ")
    elif hook_name in [bstack1ll1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ὾"), bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ὿")]:
        return bstack1ll1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᾀ")
    elif hook_name in [bstack1ll1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᾁ"), bstack1ll1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᾂ")]:
        return bstack1ll1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᾃ")
    elif hook_name in [bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᾄ"), bstack1ll1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᾅ")]:
        return bstack1ll1ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᾆ")
    return hook_name
def bstack11111111lll_opy_(node, scenario):
    if hasattr(node, bstack1ll1ll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᾇ")):
        parts = node.nodeid.rsplit(bstack1ll1ll_opy_ (u"ࠣ࡝ࠥᾈ"))
        params = parts[-1]
        return bstack1ll1ll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᾉ").format(scenario.name, params)
    return scenario.name
def bstack1111111l111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᾊ")):
            examples = list(node.callspec.params[bstack1ll1ll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᾋ")].values())
        return examples
    except:
        return []
def bstack1111111ll1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111111l111l_opy_(report):
    try:
        status = bstack1ll1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᾌ")
        if report.passed or (report.failed and hasattr(report, bstack1ll1ll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᾍ"))):
            status = bstack1ll1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᾎ")
        elif report.skipped:
            status = bstack1ll1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᾏ")
        bstack1111111l11l_opy_(status)
    except:
        pass
def bstack11l1ll1111_opy_(status):
    try:
        bstack11111111l1l_opy_ = bstack1ll1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᾐ")
        if status == bstack1ll1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᾑ"):
            bstack11111111l1l_opy_ = bstack1ll1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᾒ")
        elif status == bstack1ll1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᾓ"):
            bstack11111111l1l_opy_ = bstack1ll1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᾔ")
        bstack1111111l11l_opy_(bstack11111111l1l_opy_)
    except:
        pass
def bstack1111111llll_opy_(item=None, report=None, summary=None, extra=None):
    return