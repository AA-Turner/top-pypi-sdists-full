# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import re
from bstack_utils.bstack11111l111_opy_ import bstack1ll1l11l1lll_opy_
from bstack_utils.bstack1ll11l1ll1l_opy_ import bstack1ll11l11ll1_opy_
def bstack1ll1l1l1111l_opy_(fixture_name):
    if fixture_name.startswith(bstack111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ☮")):
        return bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ☯")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ☰")):
        return bstack111l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫ☱")
    elif fixture_name.startswith(bstack111l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ☲")):
        return bstack111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ☳")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭☴")):
        return bstack111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫ☵")
def bstack1ll1l1l11111_opy_(fixture_name):
    return bool(re.match(bstack111l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨ☶"), fixture_name))
def bstack1ll1l11lll1l_opy_(fixture_name):
    return bool(re.match(bstack111l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬ☷"), fixture_name))
def bstack1ll1l11l1ll1_opy_(fixture_name):
    return bool(re.match(bstack111l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬ☸"), fixture_name))
def bstack1ll1l11ll111_opy_(fixture_name):
    if fixture_name.startswith(bstack111l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ☹")):
        return bstack111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ☺"), bstack111l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭☻")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ☼")):
        return bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩ☽"), bstack111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ☾")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ☿")):
        return bstack111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ♀"), bstack111l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ♁")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ♂")):
        return bstack111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫ♃"), bstack111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭♄")
    return None, None
def bstack1ll1l1l111l1_opy_(hook_name):
    if hook_name in [bstack111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ♅"), bstack111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ♆")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1l11ll1l1_opy_(hook_name):
    if hook_name in [bstack111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ♇"), bstack111l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭♈")]:
        return bstack111l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭♉")
    elif hook_name in [bstack111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ♊"), bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ♋")]:
        return bstack111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ♌")
    elif hook_name in [bstack111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ♍"), bstack111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨ♎")]:
        return bstack111l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ♏")
    elif hook_name in [bstack111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ♐"), bstack111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ♑")]:
        return bstack111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭♒")
    return hook_name
def bstack1ll1l11l1l1l_opy_(node, scenario):
    if hasattr(node, bstack111l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭♓")):
        parts = node.nodeid.rsplit(bstack111l_opy_ (u"ࠧࡡࠢ♔"))
        params = parts[-1]
        return bstack111l_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨ♕").format(scenario.name, params)
    return scenario.name
def bstack1ll1l11ll1ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩ♖")):
            examples = list(node.callspec.params[bstack111l_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧ♗")].values())
        return examples
    except:
        return []
def bstack1ll1l11ll11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll1l11llll1_opy_(report):
    try:
        status = bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ♘")
        if report.passed or (report.failed and hasattr(report, bstack111l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ♙"))):
            status = bstack111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ♚")
        elif report.skipped:
            status = bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭♛")
        bstack1ll1l11l1lll_opy_(status)
    except:
        pass
def bstack1ll1111l1l_opy_(status):
    try:
        bstack1ll1l11lllll_opy_ = bstack111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭♜")
        if status == bstack111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ♝"):
            bstack1ll1l11lllll_opy_ = bstack111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ♞")
        elif status == bstack111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ♟"):
            bstack1ll1l11lllll_opy_ = bstack111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ♠")
        bstack1ll1l11l1lll_opy_(bstack1ll1l11lllll_opy_)
    except:
        pass
def bstack1ll1l11lll11_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack11ll1111l1_opy_():
    bstack111l_opy_ (u"ࠦࠧࠨࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡲࡼࡸࡪࡹࡴ࠮ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࠣ࡭ࡸࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠢࡤࡲࡩࠦࡲࡦࡶࡸࡶࡳࠦࡔࡳࡷࡨࠤ࡮࡬ࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡯ࡷࡪࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦࠤࠥࠦ♡")
    return bstack1ll11l11ll1_opy_(bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡡࡳࡣ࡯ࡰࡪࡲࠧ♢"))