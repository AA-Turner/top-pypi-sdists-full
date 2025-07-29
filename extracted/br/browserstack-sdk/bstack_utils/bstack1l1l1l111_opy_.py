# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import re
from bstack_utils.bstack1l1111l1l1_opy_ import bstack11111l1l111_opy_
def bstack11111l11lll_opy_(fixture_name):
    if fixture_name.startswith(bstackl_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩỦ")):
        return bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩủ")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩỨ")):
        return bstackl_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩứ")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩỪ")):
        return bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩừ")
    elif fixture_name.startswith(bstackl_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫỬ")):
        return bstackl_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩử")
def bstack111111ll1ll_opy_(fixture_name):
    return bool(re.match(bstackl_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭Ữ"), fixture_name))
def bstack11111l111l1_opy_(fixture_name):
    return bool(re.match(bstackl_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪữ"), fixture_name))
def bstack111111llll1_opy_(fixture_name):
    return bool(re.match(bstackl_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪỰ"), fixture_name))
def bstack111111lllll_opy_(fixture_name):
    if fixture_name.startswith(bstackl_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ự")):
        return bstackl_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ỳ"), bstackl_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫỳ")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧỴ")):
        return bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧỵ"), bstackl_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭Ỷ")
    elif fixture_name.startswith(bstackl_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨỷ")):
        return bstackl_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨỸ"), bstackl_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩỹ")
    elif fixture_name.startswith(bstackl_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩỺ")):
        return bstackl_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩỻ"), bstackl_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫỼ")
    return None, None
def bstack11111l1111l_opy_(hook_name):
    if hook_name in [bstackl_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨỽ"), bstackl_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬỾ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111111lll1l_opy_(hook_name):
    if hook_name in [bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬỿ"), bstackl_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫἀ")]:
        return bstackl_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫἁ")
    elif hook_name in [bstackl_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ἂ"), bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ἃ")]:
        return bstackl_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ἄ")
    elif hook_name in [bstackl_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧἅ"), bstackl_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ἆ")]:
        return bstackl_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩἇ")
    elif hook_name in [bstackl_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨἈ"), bstackl_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨἉ")]:
        return bstackl_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫἊ")
    return hook_name
def bstack11111l11l11_opy_(node, scenario):
    if hasattr(node, bstackl_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫἋ")):
        parts = node.nodeid.rsplit(bstackl_opy_ (u"ࠥ࡟ࠧἌ"))
        params = parts[-1]
        return bstackl_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦἍ").format(scenario.name, params)
    return scenario.name
def bstack11111l111ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstackl_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧἎ")):
            examples = list(node.callspec.params[bstackl_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬἏ")].values())
        return examples
    except:
        return []
def bstack11111l11l1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111l11ll1_opy_(report):
    try:
        status = bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧἐ")
        if report.passed or (report.failed and hasattr(report, bstackl_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥἑ"))):
            status = bstackl_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩἒ")
        elif report.skipped:
            status = bstackl_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫἓ")
        bstack11111l1l111_opy_(status)
    except:
        pass
def bstack1lll1111l_opy_(status):
    try:
        bstack111111lll11_opy_ = bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫἔ")
        if status == bstackl_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬἕ"):
            bstack111111lll11_opy_ = bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭἖")
        elif status == bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ἗"):
            bstack111111lll11_opy_ = bstackl_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩἘ")
        bstack11111l1l111_opy_(bstack111111lll11_opy_)
    except:
        pass
def bstack11111l11111_opy_(item=None, report=None, summary=None, extra=None):
    return