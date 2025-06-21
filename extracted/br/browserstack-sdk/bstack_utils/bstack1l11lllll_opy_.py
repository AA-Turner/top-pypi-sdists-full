# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import re
from bstack_utils.bstack1111ll1l_opy_ import bstack11111l1ll1l_opy_
def bstack11111ll1111_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫṿ")):
        return bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫẀ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫẁ")):
        return bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫẂ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫẃ")):
        return bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫẄ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ẅ")):
        return bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫẆ")
def bstack11111l1ll11_opy_(fixture_name):
    return bool(re.match(bstack1l1l1l1_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨẇ"), fixture_name))
def bstack11111ll1l1l_opy_(fixture_name):
    return bool(re.match(bstack1l1l1l1_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬẈ"), fixture_name))
def bstack11111ll1l11_opy_(fixture_name):
    return bool(re.match(bstack1l1l1l1_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬẉ"), fixture_name))
def bstack11111ll11l1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l1l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨẊ")):
        return bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨẋ"), bstack1l1l1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭Ẍ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩẍ")):
        return bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩẎ"), bstack1l1l1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨẏ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪẐ")):
        return bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪẑ"), bstack1l1l1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫẒ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫẓ")):
        return bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫẔ"), bstack1l1l1l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ẕ")
    return None, None
def bstack11111ll111l_opy_(hook_name):
    if hook_name in [bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪẖ"), bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧẗ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11111l1l1l1_opy_(hook_name):
    if hook_name in [bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧẘ"), bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ẙ")]:
        return bstack1l1l1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ẚ")
    elif hook_name in [bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨẛ"), bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨẜ")]:
        return bstack1l1l1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨẝ")
    elif hook_name in [bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩẞ"), bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨẟ")]:
        return bstack1l1l1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫẠ")
    elif hook_name in [bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪạ"), bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪẢ")]:
        return bstack1l1l1l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ả")
    return hook_name
def bstack11111l1lll1_opy_(node, scenario):
    if hasattr(node, bstack1l1l1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭Ấ")):
        parts = node.nodeid.rsplit(bstack1l1l1l1_opy_ (u"ࠧࡡࠢấ"))
        params = parts[-1]
        return bstack1l1l1l1_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨẦ").format(scenario.name, params)
    return scenario.name
def bstack11111l1llll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1l1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩầ")):
            examples = list(node.callspec.params[bstack1l1l1l1_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧẨ")].values())
        return examples
    except:
        return []
def bstack11111l1l11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111l1l1ll_opy_(report):
    try:
        status = bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩẩ")
        if report.passed or (report.failed and hasattr(report, bstack1l1l1l1_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧẪ"))):
            status = bstack1l1l1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫẫ")
        elif report.skipped:
            status = bstack1l1l1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭Ậ")
        bstack11111l1ll1l_opy_(status)
    except:
        pass
def bstack1l1l1lll11_opy_(status):
    try:
        bstack11111ll11ll_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ậ")
        if status == bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧẮ"):
            bstack11111ll11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨắ")
        elif status == bstack1l1l1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪẰ"):
            bstack11111ll11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫằ")
        bstack11111l1ll1l_opy_(bstack11111ll11ll_opy_)
    except:
        pass
def bstack11111ll1ll1_opy_(item=None, report=None, summary=None, extra=None):
    return