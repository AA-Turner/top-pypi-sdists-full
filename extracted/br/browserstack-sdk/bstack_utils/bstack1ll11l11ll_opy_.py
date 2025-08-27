# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import re
from bstack_utils.bstack11l1lll111_opy_ import bstack1llllllllll1_opy_
def bstack111111111l1_opy_(fixture_name):
    if fixture_name.startswith(bstack1111lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩὝ")):
        return bstack1111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ὞")
    elif fixture_name.startswith(bstack1111lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩὟ")):
        return bstack1111lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩὠ")
    elif fixture_name.startswith(bstack1111lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩὡ")):
        return bstack1111lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩὢ")
    elif fixture_name.startswith(bstack1111lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫὣ")):
        return bstack1111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩὤ")
def bstack1lllllllll1l_opy_(fixture_name):
    return bool(re.match(bstack1111lll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ὥ"), fixture_name))
def bstack11111111111_opy_(fixture_name):
    return bool(re.match(bstack1111lll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪὦ"), fixture_name))
def bstack1111111111l_opy_(fixture_name):
    return bool(re.match(bstack1111lll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪὧ"), fixture_name))
def bstack11111111l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1111lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ὠ")):
        return bstack1111lll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ὡ"), bstack1111lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫὪ")
    elif fixture_name.startswith(bstack1111lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὫ")):
        return bstack1111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧὬ"), bstack1111lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭Ὥ")
    elif fixture_name.startswith(bstack1111lll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨὮ")):
        return bstack1111lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨὯ"), bstack1111lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩὰ")
    elif fixture_name.startswith(bstack1111lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩά")):
        return bstack1111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩὲ"), bstack1111lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫέ")
    return None, None
def bstack1lllllllll11_opy_(hook_name):
    if hook_name in [bstack1111lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨὴ"), bstack1111lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬή")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llllllll1ll_opy_(hook_name):
    if hook_name in [bstack1111lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬὶ"), bstack1111lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫί")]:
        return bstack1111lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫὸ")
    elif hook_name in [bstack1111lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ό"), bstack1111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ὺ")]:
        return bstack1111lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ύ")
    elif hook_name in [bstack1111lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧὼ"), bstack1111lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ώ")]:
        return bstack1111lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ὾")
    elif hook_name in [bstack1111lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ὿"), bstack1111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᾀ")]:
        return bstack1111lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᾁ")
    return hook_name
def bstack1lllllllllll_opy_(node, scenario):
    if hasattr(node, bstack1111lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᾂ")):
        parts = node.nodeid.rsplit(bstack1111lll_opy_ (u"ࠥ࡟ࠧᾃ"))
        params = parts[-1]
        return bstack1111lll_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᾄ").format(scenario.name, params)
    return scenario.name
def bstack1llllllll11l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1111lll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᾅ")):
            examples = list(node.callspec.params[bstack1111lll_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬᾆ")].values())
        return examples
    except:
        return []
def bstack111111111ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111111l11_opy_(report):
    try:
        status = bstack1111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᾇ")
        if report.passed or (report.failed and hasattr(report, bstack1111lll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᾈ"))):
            status = bstack1111lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᾉ")
        elif report.skipped:
            status = bstack1111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᾊ")
        bstack1llllllllll1_opy_(status)
    except:
        pass
def bstack11l1111111_opy_(status):
    try:
        bstack1llllllll1l1_opy_ = bstack1111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᾋ")
        if status == bstack1111lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᾌ"):
            bstack1llllllll1l1_opy_ = bstack1111lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᾍ")
        elif status == bstack1111lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᾎ"):
            bstack1llllllll1l1_opy_ = bstack1111lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᾏ")
        bstack1llllllllll1_opy_(bstack1llllllll1l1_opy_)
    except:
        pass
def bstack11111111ll1_opy_(item=None, report=None, summary=None, extra=None):
    return