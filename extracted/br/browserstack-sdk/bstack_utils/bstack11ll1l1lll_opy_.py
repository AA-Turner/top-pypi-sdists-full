# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import re
from bstack_utils.bstack11lll11ll1_opy_ import bstack11111111l1l_opy_
def bstack1111111ll11_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὰ")):
        return bstack1l1l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧά")
    elif fixture_name.startswith(bstack1l1l1ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὲ")):
        return bstack1l1l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧέ")
    elif fixture_name.startswith(bstack1l1l1ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὴ")):
        return bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧή")
    elif fixture_name.startswith(bstack1l1l1ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩὶ")):
        return bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧί")
def bstack1111111l111_opy_(fixture_name):
    return bool(re.match(bstack1l1l1ll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫὸ"), fixture_name))
def bstack1111111llll_opy_(fixture_name):
    return bool(re.match(bstack1l1l1ll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨό"), fixture_name))
def bstack11111111l11_opy_(fixture_name):
    return bool(re.match(bstack1l1l1ll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨὺ"), fixture_name))
def bstack11111111ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l1ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫύ")):
        return bstack1l1l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫὼ"), bstack1l1l1ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩώ")
    elif fixture_name.startswith(bstack1l1l1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ὾")):
        return bstack1l1l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ὿"), bstack1l1l1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᾀ")
    elif fixture_name.startswith(bstack1l1l1ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᾁ")):
        return bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᾂ"), bstack1l1l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᾃ")
    elif fixture_name.startswith(bstack1l1l1ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᾄ")):
        return bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᾅ"), bstack1l1l1ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᾆ")
    return None, None
def bstack1111111ll1l_opy_(hook_name):
    if hook_name in [bstack1l1l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᾇ"), bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᾈ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111111l1ll_opy_(hook_name):
    if hook_name in [bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᾉ"), bstack1l1l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᾊ")]:
        return bstack1l1l1ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᾋ")
    elif hook_name in [bstack1l1l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᾌ"), bstack1l1l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᾍ")]:
        return bstack1l1l1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᾎ")
    elif hook_name in [bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᾏ"), bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᾐ")]:
        return bstack1l1l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᾑ")
    elif hook_name in [bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᾒ"), bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᾓ")]:
        return bstack1l1l1ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᾔ")
    return hook_name
def bstack1111111l1l1_opy_(node, scenario):
    if hasattr(node, bstack1l1l1ll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᾕ")):
        parts = node.nodeid.rsplit(bstack1l1l1ll_opy_ (u"ࠣ࡝ࠥᾖ"))
        params = parts[-1]
        return bstack1l1l1ll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᾗ").format(scenario.name, params)
    return scenario.name
def bstack1111111l11l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1l1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᾘ")):
            examples = list(node.callspec.params[bstack1l1l1ll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᾙ")].values())
        return examples
    except:
        return []
def bstack11111111lll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111111lll1_opy_(report):
    try:
        status = bstack1l1l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᾚ")
        if report.passed or (report.failed and hasattr(report, bstack1l1l1ll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᾛ"))):
            status = bstack1l1l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᾜ")
        elif report.skipped:
            status = bstack1l1l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᾝ")
        bstack11111111l1l_opy_(status)
    except:
        pass
def bstack1lll11ll1_opy_(status):
    try:
        bstack111111111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᾞ")
        if status == bstack1l1l1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᾟ"):
            bstack111111111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᾠ")
        elif status == bstack1l1l1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᾡ"):
            bstack111111111l1_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᾢ")
        bstack11111111l1l_opy_(bstack111111111l1_opy_)
    except:
        pass
def bstack111111111ll_opy_(item=None, report=None, summary=None, extra=None):
    return