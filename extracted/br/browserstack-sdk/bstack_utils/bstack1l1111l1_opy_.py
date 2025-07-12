# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import re
from bstack_utils.bstack1l11l111ll_opy_ import bstack11111l111l1_opy_
def bstack11111l1l1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫỡ")):
        return bstack11l1111_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫỢ")
    elif fixture_name.startswith(bstack11l1111_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫợ")):
        return bstack11l1111_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫỤ")
    elif fixture_name.startswith(bstack11l1111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫụ")):
        return bstack11l1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫỦ")
    elif fixture_name.startswith(bstack11l1111_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ủ")):
        return bstack11l1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫỨ")
def bstack11111l1111l_opy_(fixture_name):
    return bool(re.match(bstack11l1111_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨứ"), fixture_name))
def bstack11111l11111_opy_(fixture_name):
    return bool(re.match(bstack11l1111_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬỪ"), fixture_name))
def bstack11111l11ll1_opy_(fixture_name):
    return bool(re.match(bstack11l1111_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬừ"), fixture_name))
def bstack11111l1l11l_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨỬ")):
        return bstack11l1111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨử"), bstack11l1111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭Ữ")
    elif fixture_name.startswith(bstack11l1111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩữ")):
        return bstack11l1111_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩỰ"), bstack11l1111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨự")
    elif fixture_name.startswith(bstack11l1111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪỲ")):
        return bstack11l1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪỳ"), bstack11l1111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫỴ")
    elif fixture_name.startswith(bstack11l1111_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫỵ")):
        return bstack11l1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫỶ"), bstack11l1111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ỷ")
    return None, None
def bstack11111l11l1l_opy_(hook_name):
    if hook_name in [bstack11l1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪỸ"), bstack11l1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧỹ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111111lllll_opy_(hook_name):
    if hook_name in [bstack11l1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧỺ"), bstack11l1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ỻ")]:
        return bstack11l1111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭Ỽ")
    elif hook_name in [bstack11l1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨỽ"), bstack11l1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨỾ")]:
        return bstack11l1111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨỿ")
    elif hook_name in [bstack11l1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩἀ"), bstack11l1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨἁ")]:
        return bstack11l1111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫἂ")
    elif hook_name in [bstack11l1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪἃ"), bstack11l1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪἄ")]:
        return bstack11l1111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ἅ")
    return hook_name
def bstack11111l1l111_opy_(node, scenario):
    if hasattr(node, bstack11l1111_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ἆ")):
        parts = node.nodeid.rsplit(bstack11l1111_opy_ (u"ࠧࡡࠢἇ"))
        params = parts[-1]
        return bstack11l1111_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨἈ").format(scenario.name, params)
    return scenario.name
def bstack11111l111ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1111_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩἉ")):
            examples = list(node.callspec.params[bstack11l1111_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧἊ")].values())
        return examples
    except:
        return []
def bstack11111l1l1ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111l11lll_opy_(report):
    try:
        status = bstack11l1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩἋ")
        if report.passed or (report.failed and hasattr(report, bstack11l1111_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧἌ"))):
            status = bstack11l1111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫἍ")
        elif report.skipped:
            status = bstack11l1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭Ἆ")
        bstack11111l111l1_opy_(status)
    except:
        pass
def bstack11ll1lllll_opy_(status):
    try:
        bstack111111llll1_opy_ = bstack11l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ἇ")
        if status == bstack11l1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧἐ"):
            bstack111111llll1_opy_ = bstack11l1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨἑ")
        elif status == bstack11l1111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪἒ"):
            bstack111111llll1_opy_ = bstack11l1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫἓ")
        bstack11111l111l1_opy_(bstack111111llll1_opy_)
    except:
        pass
def bstack11111l11l11_opy_(item=None, report=None, summary=None, extra=None):
    return