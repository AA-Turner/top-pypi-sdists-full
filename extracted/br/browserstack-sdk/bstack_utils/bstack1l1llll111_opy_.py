# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import re
from bstack_utils.bstack11l1111111_opy_ import bstack1lllllll1l11_opy_
def bstack1llllllll11l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11ll1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬὠ")):
        return bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬὡ")
    elif fixture_name.startswith(bstack1l11ll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬὢ")):
        return bstack1l11ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬὣ")
    elif fixture_name.startswith(bstack1l11ll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬὤ")):
        return bstack1l11ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬὥ")
    elif fixture_name.startswith(bstack1l11ll1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὦ")):
        return bstack1l11ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬὧ")
def bstack1lllllll1ll1_opy_(fixture_name):
    return bool(re.match(bstack1l11ll1_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩὨ"), fixture_name))
def bstack1lllllllllll_opy_(fixture_name):
    return bool(re.match(bstack1l11ll1_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭Ὡ"), fixture_name))
def bstack1llllllllll1_opy_(fixture_name):
    return bool(re.match(bstack1l11ll1_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭Ὢ"), fixture_name))
def bstack1lllllll1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11ll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩὫ")):
        return bstack1l11ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩὬ"), bstack1l11ll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧὭ")
    elif fixture_name.startswith(bstack1l11ll1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪὮ")):
        return bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪὯ"), bstack1l11ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩὰ")
    elif fixture_name.startswith(bstack1l11ll1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫά")):
        return bstack1l11ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫὲ"), bstack1l11ll1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬέ")
    elif fixture_name.startswith(bstack1l11ll1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬὴ")):
        return bstack1l11ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬή"), bstack1l11ll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧὶ")
    return None, None
def bstack1lllllll11ll_opy_(hook_name):
    if hook_name in [bstack1l11ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫί"), bstack1l11ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨὸ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lllllll1l1l_opy_(hook_name):
    if hook_name in [bstack1l11ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨό"), bstack1l11ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧὺ")]:
        return bstack1l11ll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧύ")
    elif hook_name in [bstack1l11ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩὼ"), bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩώ")]:
        return bstack1l11ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ὾")
    elif hook_name in [bstack1l11ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ὿"), bstack1l11ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᾀ")]:
        return bstack1l11ll1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᾁ")
    elif hook_name in [bstack1l11ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᾂ"), bstack1l11ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᾃ")]:
        return bstack1l11ll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᾄ")
    return hook_name
def bstack1llllllll1l1_opy_(node, scenario):
    if hasattr(node, bstack1l11ll1_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᾅ")):
        parts = node.nodeid.rsplit(bstack1l11ll1_opy_ (u"ࠨ࡛ࠣᾆ"))
        params = parts[-1]
        return bstack1l11ll1_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᾇ").format(scenario.name, params)
    return scenario.name
def bstack11111111111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l11ll1_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᾈ")):
            examples = list(node.callspec.params[bstack1l11ll1_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᾉ")].values())
        return examples
    except:
        return []
def bstack1llllllll111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lllllllll11_opy_(report):
    try:
        status = bstack1l11ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᾊ")
        if report.passed or (report.failed and hasattr(report, bstack1l11ll1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᾋ"))):
            status = bstack1l11ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᾌ")
        elif report.skipped:
            status = bstack1l11ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᾍ")
        bstack1lllllll1l11_opy_(status)
    except:
        pass
def bstack111ll1l1l_opy_(status):
    try:
        bstack1lllllllll1l_opy_ = bstack1l11ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᾎ")
        if status == bstack1l11ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᾏ"):
            bstack1lllllllll1l_opy_ = bstack1l11ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᾐ")
        elif status == bstack1l11ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᾑ"):
            bstack1lllllllll1l_opy_ = bstack1l11ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᾒ")
        bstack1lllllll1l11_opy_(bstack1lllllllll1l_opy_)
    except:
        pass
def bstack1llllllll1ll_opy_(item=None, report=None, summary=None, extra=None):
    return