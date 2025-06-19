# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import re
from bstack_utils.bstack111ll1ll_opy_ import bstack1111ll111ll_opy_
def bstack1111ll11ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack111lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṓ")):
        return bstack111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩṔ")
    elif fixture_name.startswith(bstack111lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṕ")):
        return bstack111lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩṖ")
    elif fixture_name.startswith(bstack111lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṗ")):
        return bstack111lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩṘ")
    elif fixture_name.startswith(bstack111lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫṙ")):
        return bstack111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩṚ")
def bstack1111l1ll1ll_opy_(fixture_name):
    return bool(re.match(bstack111lll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ṛ"), fixture_name))
def bstack1111l1ll11l_opy_(fixture_name):
    return bool(re.match(bstack111lll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪṜ"), fixture_name))
def bstack1111l1llll1_opy_(fixture_name):
    return bool(re.match(bstack111lll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪṝ"), fixture_name))
def bstack1111l1lll11_opy_(fixture_name):
    if fixture_name.startswith(bstack111lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ṟ")):
        return bstack111lll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ṟ"), bstack111lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫṠ")
    elif fixture_name.startswith(bstack111lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧṡ")):
        return bstack111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧṢ"), bstack111lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ṣ")
    elif fixture_name.startswith(bstack111lll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨṤ")):
        return bstack111lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨṥ"), bstack111lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩṦ")
    elif fixture_name.startswith(bstack111lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṧ")):
        return bstack111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩṨ"), bstack111lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫṩ")
    return None, None
def bstack1111ll11l11_opy_(hook_name):
    if hook_name in [bstack111lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨṪ"), bstack111lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬṫ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111l1ll1l1_opy_(hook_name):
    if hook_name in [bstack111lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬṬ"), bstack111lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫṭ")]:
        return bstack111lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫṮ")
    elif hook_name in [bstack111lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ṯ"), bstack111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭Ṱ")]:
        return bstack111lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ṱ")
    elif hook_name in [bstack111lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧṲ"), bstack111lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ṳ")]:
        return bstack111lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩṴ")
    elif hook_name in [bstack111lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨṵ"), bstack111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨṶ")]:
        return bstack111lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫṷ")
    return hook_name
def bstack1111ll1111l_opy_(node, scenario):
    if hasattr(node, bstack111lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫṸ")):
        parts = node.nodeid.rsplit(bstack111lll_opy_ (u"ࠥ࡟ࠧṹ"))
        params = parts[-1]
        return bstack111lll_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦṺ").format(scenario.name, params)
    return scenario.name
def bstack1111l1lllll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111lll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧṻ")):
            examples = list(node.callspec.params[bstack111lll_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬṼ")].values())
        return examples
    except:
        return []
def bstack1111ll111l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111ll11l1l_opy_(report):
    try:
        status = bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧṽ")
        if report.passed or (report.failed and hasattr(report, bstack111lll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥṾ"))):
            status = bstack111lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩṿ")
        elif report.skipped:
            status = bstack111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫẀ")
        bstack1111ll111ll_opy_(status)
    except:
        pass
def bstack1l1lll11l_opy_(status):
    try:
        bstack1111ll11111_opy_ = bstack111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫẁ")
        if status == bstack111lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬẂ"):
            bstack1111ll11111_opy_ = bstack111lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ẃ")
        elif status == bstack111lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨẄ"):
            bstack1111ll11111_opy_ = bstack111lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩẅ")
        bstack1111ll111ll_opy_(bstack1111ll11111_opy_)
    except:
        pass
def bstack1111l1lll1l_opy_(item=None, report=None, summary=None, extra=None):
    return