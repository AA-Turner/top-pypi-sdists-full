# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import re
from bstack_utils.session_utils import bstack1llll11l1lll_opy_
from bstack_utils.bstack1lll1ll1111_opy_ import bstack1lll1lll11l_opy_
def bstack1llll11l1l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṅ")):
        return bstack1ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩṆ")
    elif fixture_name.startswith(bstack1ll111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṇ")):
        return bstack1ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩṈ")
    elif fixture_name.startswith(bstack1ll111_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṉ")):
        return bstack1ll111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩṊ")
    elif fixture_name.startswith(bstack1ll111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫṋ")):
        return bstack1ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩṌ")
def bstack1llll11l1ll1_opy_(fixture_name):
    return bool(re.match(bstack1ll111_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ṍ"), fixture_name))
def bstack1llll11l111l_opy_(fixture_name):
    return bool(re.match(bstack1ll111_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪṎ"), fixture_name))
def bstack1llll11ll111_opy_(fixture_name):
    return bool(re.match(bstack1ll111_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪṏ"), fixture_name))
def bstack1llll11l1111_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll111_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ṑ")):
        return bstack1ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ṑ"), bstack1ll111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫṒ")
    elif fixture_name.startswith(bstack1ll111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧṓ")):
        return bstack1ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧṔ"), bstack1ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ṕ")
    elif fixture_name.startswith(bstack1ll111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨṖ")):
        return bstack1ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨṗ"), bstack1ll111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩṘ")
    elif fixture_name.startswith(bstack1ll111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṙ")):
        return bstack1ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩṚ"), bstack1ll111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫṛ")
    return None, None
def bstack1llll111lll1_opy_(hook_name):
    if hook_name in [bstack1ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨṜ"), bstack1ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬṝ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llll11l11ll_opy_(hook_name):
    if hook_name in [bstack1ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬṞ"), bstack1ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫṟ")]:
        return bstack1ll111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫṠ")
    elif hook_name in [bstack1ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ṡ"), bstack1ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭Ṣ")]:
        return bstack1ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ṣ")
    elif hook_name in [bstack1ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧṤ"), bstack1ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ṥ")]:
        return bstack1ll111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩṦ")
    elif hook_name in [bstack1ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨṧ"), bstack1ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨṨ")]:
        return bstack1ll111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫṩ")
    return hook_name
def bstack1llll111ll11_opy_(node, scenario):
    if hasattr(node, bstack1ll111_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫṪ")):
        parts = node.nodeid.rsplit(bstack1ll111_opy_ (u"ࠥ࡟ࠧṫ"))
        params = parts[-1]
        return bstack1ll111_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦṬ").format(scenario.name, params)
    return scenario.name
def bstack1llll11l11l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll111_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧṭ")):
            examples = list(node.callspec.params[bstack1ll111_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬṮ")].values())
        return examples
    except:
        return []
def bstack1llll111llll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llll11l1l11_opy_(report):
    try:
        status = bstack1ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧṯ")
        if report.passed or (report.failed and hasattr(report, bstack1ll111_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥṰ"))):
            status = bstack1ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩṱ")
        elif report.skipped:
            status = bstack1ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫṲ")
        bstack1llll11l1lll_opy_(status)
    except:
        pass
def bstack1l1111l1l1_opy_(status):
    try:
        bstack1llll111ll1l_opy_ = bstack1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫṳ")
        if status == bstack1ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬṴ"):
            bstack1llll111ll1l_opy_ = bstack1ll111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ṵ")
        elif status == bstack1ll111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨṶ"):
            bstack1llll111ll1l_opy_ = bstack1ll111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩṷ")
        bstack1llll11l1lll_opy_(bstack1llll111ll1l_opy_)
    except:
        pass
def bstack1llll111l1ll_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1ll111l11_opy_():
    bstack1ll111_opy_ (u"ࠤࠥࠦࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡢࡰࡧࠤࡷ࡫ࡴࡶࡴࡱࠤ࡙ࡸࡵࡦࠢ࡬ࡪࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡ࡭ࡵࡨࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠢࠣࠤṸ")
    return bstack1lll1lll11l_opy_(bstack1ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡦࡸࡡ࡭࡮ࡨࡰࠬṹ"))