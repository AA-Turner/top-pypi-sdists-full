# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import re
from bstack_utils.bstack111lllll1_opy_ import bstack1llll111ll1l_opy_
from bstack_utils.bstack1llll1lllll_opy_ import bstack1lllll1l1l1_opy_
def bstack1llll111l111_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1ll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⃷")):
        return bstack11l1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⃸")
    elif fixture_name.startswith(bstack11l1ll1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⃹")):
        return bstack11l1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭⃺")
    elif fixture_name.startswith(bstack11l1ll1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⃻")):
        return bstack11l1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⃼")
    elif fixture_name.startswith(bstack11l1ll1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⃽")):
        return bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭⃾")
def bstack1llll1111ll1_opy_(fixture_name):
    return bool(re.match(bstack11l1ll1_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࢁࡳ࡯ࡥࡷ࡯ࡩ࠮ࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪ⃿"), fixture_name))
def bstack1llll11111l1_opy_(fixture_name):
    return bool(re.match(bstack11l1ll1_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧ℀"), fixture_name))
def bstack1llll111llll_opy_(fixture_name):
    return bool(re.match(bstack11l1ll1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧ℁"), fixture_name))
def bstack1llll111lll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1ll1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪℂ")):
        return bstack11l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ℃"), bstack11l1ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ℄")
    elif fixture_name.startswith(bstack11l1ll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ℅")):
        return bstack11l1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫ℆"), bstack11l1ll1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪℇ")
    elif fixture_name.startswith(bstack11l1ll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ℈")):
        return bstack11l1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ℉"), bstack11l1ll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ℊ")
    elif fixture_name.startswith(bstack11l1ll1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ℋ")):
        return bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭ℌ"), bstack11l1ll1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨℍ")
    return None, None
def bstack1llll111l1ll_opy_(hook_name):
    if hook_name in [bstack11l1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬℎ"), bstack11l1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩℏ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llll111l1l1_opy_(hook_name):
    if hook_name in [bstack11l1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩℐ"), bstack11l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨℑ")]:
        return bstack11l1ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨℒ")
    elif hook_name in [bstack11l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪℓ"), bstack11l1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ℔")]:
        return bstack11l1ll1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪℕ")
    elif hook_name in [bstack11l1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ№"), bstack11l1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ℗")]:
        return bstack11l1ll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭℘")
    elif hook_name in [bstack11l1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬℙ"), bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬℚ")]:
        return bstack11l1ll1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨℛ")
    return hook_name
def bstack1llll1111l1l_opy_(node, scenario):
    if hasattr(node, bstack11l1ll1_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨℜ")):
        parts = node.nodeid.rsplit(bstack11l1ll1_opy_ (u"ࠢ࡜ࠤℝ"))
        params = parts[-1]
        return bstack11l1ll1_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣ℞").format(scenario.name, params)
    return scenario.name
def bstack1llll1111lll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1ll1_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫ℟")):
            examples = list(node.callspec.params[bstack11l1ll1_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩ℠")].values())
        return examples
    except:
        return []
def bstack1llll111l11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llll1111l11_opy_(report):
    try:
        status = bstack11l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ℡")
        if report.passed or (report.failed and hasattr(report, bstack11l1ll1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ™"))):
            status = bstack11l1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭℣")
        elif report.skipped:
            status = bstack11l1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨℤ")
        bstack1llll111ll1l_opy_(status)
    except:
        pass
def bstack1l111ll1l_opy_(status):
    try:
        bstack1llll11111ll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ℥")
        if status == bstack11l1ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩΩ"):
            bstack1llll11111ll_opy_ = bstack11l1ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ℧")
        elif status == bstack11l1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬℨ"):
            bstack1llll11111ll_opy_ = bstack11l1ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭℩")
        bstack1llll111ll1l_opy_(bstack1llll11111ll_opy_)
    except:
        pass
def bstack1llll111ll11_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1l11111111_opy_():
    bstack11l1ll1_opy_ (u"ࠨࠢࠣࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࠥ࡯ࡳࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠤࡦࡴࡤࠡࡴࡨࡸࡺࡸ࡮ࠡࡖࡵࡹࡪࠦࡩࡧࠢࡩࡳࡺࡴࡤ࠭ࠢࡉࡥࡱࡹࡥࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨࠦࠧࠨK")
    return bstack1lllll1l1l1_opy_(bstack11l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡣࡵࡥࡱࡲࡥ࡭ࠩÅ"))