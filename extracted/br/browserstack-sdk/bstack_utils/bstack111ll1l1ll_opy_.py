# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import re
from bstack_utils.bstack1lll1lll_opy_ import bstack1ll1l11111ll_opy_
from bstack_utils.bstack1ll11l11lll_opy_ import bstack1ll11l1l11l_opy_
def bstack1ll1l111l1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack111ll11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ♥")):
        return bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ♦")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ♧")):
        return bstack111ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ♨")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ♩")):
        return bstack111ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ♪")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ♫")):
        return bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ♬")
def bstack1ll1l1111ll1_opy_(fixture_name):
    return bool(re.match(bstack111ll11_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧ♭"), fixture_name))
def bstack1ll1l11111l1_opy_(fixture_name):
    return bool(re.match(bstack111ll11_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ♮"), fixture_name))
def bstack1ll1l111ll11_opy_(fixture_name):
    return bool(re.match(bstack111ll11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ♯"), fixture_name))
def bstack1ll1l1111lll_opy_(fixture_name):
    if fixture_name.startswith(bstack111ll11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ♰")):
        return bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ♱"), bstack111ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ♲")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ♳")):
        return bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨ♴"), bstack111ll11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ♵")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ♶")):
        return bstack111ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ♷"), bstack111ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ♸")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ♹")):
        return bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ♺"), bstack111ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ♻")
    return None, None
def bstack1ll1l1111l1l_opy_(hook_name):
    if hook_name in [bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ♼"), bstack111ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭♽")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1l111lll1_opy_(hook_name):
    if hook_name in [bstack111ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭♾"), bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ♿")]:
        return bstack111ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⚀")
    elif hook_name in [bstack111ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⚁"), bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⚂")]:
        return bstack111ll11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ⚃")
    elif hook_name in [bstack111ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⚄"), bstack111ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⚅")]:
        return bstack111ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⚆")
    elif hook_name in [bstack111ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⚇"), bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⚈")]:
        return bstack111ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ⚉")
    return hook_name
def bstack1ll1l111l11l_opy_(node, scenario):
    if hasattr(node, bstack111ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ⚊")):
        parts = node.nodeid.rsplit(bstack111ll11_opy_ (u"ࠦࡠࠨ⚋"))
        params = parts[-1]
        return bstack111ll11_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧ⚌").format(scenario.name, params)
    return scenario.name
def bstack1ll1l111llll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ⚍")):
            examples = list(node.callspec.params[bstack111ll11_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭⚎")].values())
        return examples
    except:
        return []
def bstack1ll1l111l1ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll1l1111l11_opy_(report):
    try:
        status = bstack111ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⚏")
        if report.passed or (report.failed and hasattr(report, bstack111ll11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ⚐"))):
            status = bstack111ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⚑")
        elif report.skipped:
            status = bstack111ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⚒")
        bstack1ll1l11111ll_opy_(status)
    except:
        pass
def bstack1l111l11_opy_(status):
    try:
        bstack1ll1l111l111_opy_ = bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⚓")
        if status == bstack111ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⚔"):
            bstack1ll1l111l111_opy_ = bstack111ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⚕")
        elif status == bstack111ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⚖"):
            bstack1ll1l111l111_opy_ = bstack111ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⚗")
        bstack1ll1l11111ll_opy_(bstack1ll1l111l111_opy_)
    except:
        pass
def bstack1ll1l111ll1l_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1ll11l1ll_opy_():
    bstack111ll11_opy_ (u"ࠥࠦࠧࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡱࡻࡷࡩࡸࡺ࠭ࡱࡣࡵࡥࡱࡲࡥ࡭ࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡣࡱࡨࠥࡸࡥࡵࡷࡵࡲ࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡮ࡶࡩࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥࠣࠤࠥ⚘")
    return bstack1ll11l1l11l_opy_(bstack111ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭⚙"))