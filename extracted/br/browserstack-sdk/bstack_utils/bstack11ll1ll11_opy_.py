# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import re
from bstack_utils.bstack1l1l111l11_opy_ import bstack1llll11111ll_opy_
from bstack_utils.bstack1lllll1111l_opy_ import bstack1lllll1l11l_opy_
def bstack1llll11111l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11lllll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ℗")):
        return bstack11lllll_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ℘")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪℙ")):
        return bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪℚ")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪℛ")):
        return bstack11lllll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪℜ")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬℝ")):
        return bstack11lllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ℞")
def bstack1llll1111l11_opy_(fixture_name):
    return bool(re.match(bstack11lllll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧ℟"), fixture_name))
def bstack1llll111l11l_opy_(fixture_name):
    return bool(re.match(bstack11lllll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ℠"), fixture_name))
def bstack1lll1lllllll_opy_(fixture_name):
    return bool(re.match(bstack11lllll_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ℡"), fixture_name))
def bstack1llll1111ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11lllll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ™")):
        return bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ℣"), bstack11lllll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬℤ")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ℥")):
        return bstack11lllll_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨΩ"), bstack11lllll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ℧")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩℨ")):
        return bstack11lllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ℩"), bstack11lllll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪK")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪÅ")):
        return bstack11lllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪℬ"), bstack11lllll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬℭ")
    return None, None
def bstack1lll1lllll11_opy_(hook_name):
    if hook_name in [bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ℮"), bstack11lllll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ℯ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll1llllll1_opy_(hook_name):
    if hook_name in [bstack11lllll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ℰ"), bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬℱ")]:
        return bstack11lllll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬℲ")
    elif hook_name in [bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧℳ"), bstack11lllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧℴ")]:
        return bstack11lllll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧℵ")
    elif hook_name in [bstack11lllll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨℶ"), bstack11lllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧℷ")]:
        return bstack11lllll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪℸ")
    elif hook_name in [bstack11lllll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩℹ"), bstack11lllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ℺")]:
        return bstack11lllll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ℻")
    return hook_name
def bstack1lll1lllll1l_opy_(node, scenario):
    if hasattr(node, bstack11lllll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬℼ")):
        parts = node.nodeid.rsplit(bstack11lllll_opy_ (u"ࠦࡠࠨℽ"))
        params = parts[-1]
        return bstack11lllll_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧℾ").format(scenario.name, params)
    return scenario.name
def bstack1llll111l111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11lllll_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨℿ")):
            examples = list(node.callspec.params[bstack11lllll_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭⅀")].values())
        return examples
    except:
        return []
def bstack1llll1111111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llll111111l_opy_(report):
    try:
        status = bstack11lllll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⅁")
        if report.passed or (report.failed and hasattr(report, bstack11lllll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ⅂"))):
            status = bstack11lllll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⅃")
        elif report.skipped:
            status = bstack11lllll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⅄")
        bstack1llll11111ll_opy_(status)
    except:
        pass
def bstack1ll1lll11l_opy_(status):
    try:
        bstack1llll1111lll_opy_ = bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬⅅ")
        if status == bstack11lllll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ⅆ"):
            bstack1llll1111lll_opy_ = bstack11lllll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧⅇ")
        elif status == bstack11lllll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩⅈ"):
            bstack1llll1111lll_opy_ = bstack11lllll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪⅉ")
        bstack1llll11111ll_opy_(bstack1llll1111lll_opy_)
    except:
        pass
def bstack1llll1111l1l_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1l1l1l1111_opy_():
    bstack11lllll_opy_ (u"ࠥࠦࠧࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡱࡻࡷࡩࡸࡺ࠭ࡱࡣࡵࡥࡱࡲࡥ࡭ࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡣࡱࡨࠥࡸࡥࡵࡷࡵࡲ࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡮ࡶࡩࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥࠣࠤࠥ⅊")
    return bstack1lllll1l11l_opy_(bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭⅋"))