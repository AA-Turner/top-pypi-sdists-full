# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import re
from bstack_utils.bstack1lll111l1_opy_ import bstack11111111l11_opy_
def bstack111111l111l_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨὣ")):
        return bstack11l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨὤ")
    elif fixture_name.startswith(bstack11l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨὥ")):
        return bstack11l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨὦ")
    elif fixture_name.startswith(bstack11l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨὧ")):
        return bstack11l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨὨ")
    elif fixture_name.startswith(bstack11l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪὩ")):
        return bstack11l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨὪ")
def bstack1111111lll1_opy_(fixture_name):
    return bool(re.match(bstack11l1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬὫ"), fixture_name))
def bstack111111l1111_opy_(fixture_name):
    return bool(re.match(bstack11l1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩὬ"), fixture_name))
def bstack1111111l11l_opy_(fixture_name):
    return bool(re.match(bstack11l1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩὭ"), fixture_name))
def bstack11111111ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬὮ")):
        return bstack11l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬὯ"), bstack11l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪὰ")
    elif fixture_name.startswith(bstack11l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ά")):
        return bstack11l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ὲ"), bstack11l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬέ")
    elif fixture_name.startswith(bstack11l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧὴ")):
        return bstack11l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧή"), bstack11l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨὶ")
    elif fixture_name.startswith(bstack11l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨί")):
        return bstack11l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨὸ"), bstack11l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪό")
    return None, None
def bstack1111111llll_opy_(hook_name):
    if hook_name in [bstack11l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧὺ"), bstack11l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫύ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111111l1ll_opy_(hook_name):
    if hook_name in [bstack11l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫὼ"), bstack11l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪώ")]:
        return bstack11l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ὾")
    elif hook_name in [bstack11l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ὿"), bstack11l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᾀ")]:
        return bstack11l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᾁ")
    elif hook_name in [bstack11l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᾂ"), bstack11l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᾃ")]:
        return bstack11l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᾄ")
    elif hook_name in [bstack11l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᾅ"), bstack11l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᾆ")]:
        return bstack11l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᾇ")
    return hook_name
def bstack1111111l1l1_opy_(node, scenario):
    if hasattr(node, bstack11l1_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᾈ")):
        parts = node.nodeid.rsplit(bstack11l1_opy_ (u"ࠤ࡞ࠦᾉ"))
        params = parts[-1]
        return bstack11l1_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᾊ").format(scenario.name, params)
    return scenario.name
def bstack1111111ll1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᾋ")):
            examples = list(node.callspec.params[bstack11l1_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᾌ")].values())
        return examples
    except:
        return []
def bstack11111111lll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111111l111_opy_(report):
    try:
        status = bstack11l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᾍ")
        if report.passed or (report.failed and hasattr(report, bstack11l1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᾎ"))):
            status = bstack11l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᾏ")
        elif report.skipped:
            status = bstack11l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᾐ")
        bstack11111111l11_opy_(status)
    except:
        pass
def bstack1l11l11l1l_opy_(status):
    try:
        bstack1111111ll11_opy_ = bstack11l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᾑ")
        if status == bstack11l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᾒ"):
            bstack1111111ll11_opy_ = bstack11l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᾓ")
        elif status == bstack11l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᾔ"):
            bstack1111111ll11_opy_ = bstack11l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᾕ")
        bstack11111111l11_opy_(bstack1111111ll11_opy_)
    except:
        pass
def bstack11111111l1l_opy_(item=None, report=None, summary=None, extra=None):
    return