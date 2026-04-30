# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import re
from bstack_utils.bstack1l1111ll11_opy_ import bstack1ll1l111111l_opy_
from bstack_utils.bstack1ll111lllll_opy_ import bstack1ll11l1l1ll_opy_
def bstack1ll1l1111ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1111l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ♧")):
        return bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ♨")
    elif fixture_name.startswith(bstack1l1111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ♩")):
        return bstack1l1111l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ♪")
    elif fixture_name.startswith(bstack1l1111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ♫")):
        return bstack1l1111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ♬")
    elif fixture_name.startswith(bstack1l1111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ♭")):
        return bstack1l1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ♮")
def bstack1ll1l111l1ll_opy_(fixture_name):
    return bool(re.match(bstack1l1111l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ♯"), fixture_name))
def bstack1ll1l1111l1l_opy_(fixture_name):
    return bool(re.match(bstack1l1111l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭♰"), fixture_name))
def bstack1ll1l111l111_opy_(fixture_name):
    return bool(re.match(bstack1l1111l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭♱"), fixture_name))
def bstack1ll1l1111111_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ♲")):
        return bstack1l1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ♳"), bstack1l1111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ♴")
    elif fixture_name.startswith(bstack1l1111l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ♵")):
        return bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ♶"), bstack1l1111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ♷")
    elif fixture_name.startswith(bstack1l1111l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ♸")):
        return bstack1l1111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ♹"), bstack1l1111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ♺")
    elif fixture_name.startswith(bstack1l1111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ♻")):
        return bstack1l1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ♼"), bstack1l1111l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ♽")
    return None, None
def bstack1ll1l111ll11_opy_(hook_name):
    if hook_name in [bstack1l1111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ♾"), bstack1l1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ♿")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1l1111l11_opy_(hook_name):
    if hook_name in [bstack1l1111l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⚀"), bstack1l1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⚁")]:
        return bstack1l1111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⚂")
    elif hook_name in [bstack1l1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⚃"), bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⚄")]:
        return bstack1l1111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ⚅")
    elif hook_name in [bstack1l1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⚆"), bstack1l1111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ⚇")]:
        return bstack1l1111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ⚈")
    elif hook_name in [bstack1l1111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⚉"), bstack1l1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⚊")]:
        return bstack1l1111l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ⚋")
    return hook_name
def bstack1ll1l11111l1_opy_(node, scenario):
    if hasattr(node, bstack1l1111l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ⚌")):
        parts = node.nodeid.rsplit(bstack1l1111l_opy_ (u"ࠨ࡛ࠣ⚍"))
        params = parts[-1]
        return bstack1l1111l_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢ⚎").format(scenario.name, params)
    return scenario.name
def bstack1ll1l111l11l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1111l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪ⚏")):
            examples = list(node.callspec.params[bstack1l1111l_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨ⚐")].values())
        return examples
    except:
        return []
def bstack1ll1l111ll1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll1l11111ll_opy_(report):
    try:
        status = bstack1l1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⚑")
        if report.passed or (report.failed and hasattr(report, bstack1l1111l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⚒"))):
            status = bstack1l1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⚓")
        elif report.skipped:
            status = bstack1l1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⚔")
        bstack1ll1l111111l_opy_(status)
    except:
        pass
def bstack1l111llll_opy_(status):
    try:
        bstack1ll1l111l1l1_opy_ = bstack1l1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⚕")
        if status == bstack1l1111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⚖"):
            bstack1ll1l111l1l1_opy_ = bstack1l1111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⚗")
        elif status == bstack1l1111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⚘"):
            bstack1ll1l111l1l1_opy_ = bstack1l1111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⚙")
        bstack1ll1l111111l_opy_(bstack1ll1l111l1l1_opy_)
    except:
        pass
def bstack1ll1l1111lll_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1l111l1l1l_opy_():
    bstack1l1111l_opy_ (u"ࠧࠨࠢࡄࡪࡨࡧࡰࠦࡩࡧࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠤ࡮ࡹࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡥࡳࡪࠠࡳࡧࡷࡹࡷࡴࠠࡕࡴࡸࡩࠥ࡯ࡦࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤࡰࡸ࡫ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠥࠦࠧ⚚")
    return bstack1ll11l1l1ll_opy_(bstack1l1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡢࡴࡤࡰࡱ࡫࡬ࠨ⚛"))