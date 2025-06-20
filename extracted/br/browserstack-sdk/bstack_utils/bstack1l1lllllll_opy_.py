# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import re
from bstack_utils.bstack1l1l11l11l_opy_ import bstack11111l1ll1l_opy_
def bstack11111l1l11l_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪṾ")):
        return bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪṿ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪẀ")):
        return bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪẁ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪẂ")):
        return bstack11ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪẃ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬẄ")):
        return bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪẅ")
def bstack11111l1lll1_opy_(fixture_name):
    return bool(re.match(bstack11ll11_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧẆ"), fixture_name))
def bstack11111ll11l1_opy_(fixture_name):
    return bool(re.match(bstack11ll11_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫẇ"), fixture_name))
def bstack11111ll111l_opy_(fixture_name):
    return bool(re.match(bstack11ll11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫẈ"), fixture_name))
def bstack11111l1l1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧẉ")):
        return bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧẊ"), bstack11ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬẋ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨẌ")):
        return bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨẍ"), bstack11ll11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧẎ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩẏ")):
        return bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩẐ"), bstack11ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪẑ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪẒ")):
        return bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪẓ"), bstack11ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬẔ")
    return None, None
def bstack11111l1ll11_opy_(hook_name):
    if hook_name in [bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩẕ"), bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ẖ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11111ll1111_opy_(hook_name):
    if hook_name in [bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ẗ"), bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬẘ")]:
        return bstack11ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬẙ")
    elif hook_name in [bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧẚ"), bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧẛ")]:
        return bstack11ll11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧẜ")
    elif hook_name in [bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨẝ"), bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧẞ")]:
        return bstack11ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪẟ")
    elif hook_name in [bstack11ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩẠ"), bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩạ")]:
        return bstack11ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬẢ")
    return hook_name
def bstack11111ll11ll_opy_(node, scenario):
    if hasattr(node, bstack11ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬả")):
        parts = node.nodeid.rsplit(bstack11ll11_opy_ (u"ࠦࡠࠨẤ"))
        params = parts[-1]
        return bstack11ll11_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧấ").format(scenario.name, params)
    return scenario.name
def bstack11111ll1l11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨẦ")):
            examples = list(node.callspec.params[bstack11ll11_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ầ")].values())
        return examples
    except:
        return []
def bstack11111l1l1ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111ll1ll1_opy_(report):
    try:
        status = bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨẨ")
        if report.passed or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦẩ"))):
            status = bstack11ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪẪ")
        elif report.skipped:
            status = bstack11ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬẫ")
        bstack11111l1ll1l_opy_(status)
    except:
        pass
def bstack1ll11lll11_opy_(status):
    try:
        bstack11111ll1l1l_opy_ = bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬẬ")
        if status == bstack11ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ậ"):
            bstack11111ll1l1l_opy_ = bstack11ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧẮ")
        elif status == bstack11ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩắ"):
            bstack11111ll1l1l_opy_ = bstack11ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪẰ")
        bstack11111l1ll1l_opy_(bstack11111ll1l1l_opy_)
    except:
        pass
def bstack11111l1llll_opy_(item=None, report=None, summary=None, extra=None):
    return