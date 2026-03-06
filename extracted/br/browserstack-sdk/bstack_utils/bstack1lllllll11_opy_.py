# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import re
from bstack_utils.session_utils import bstack1lll11lllll1_opy_
from bstack_utils.bstack1lll1ll11ll_opy_ import bstack1llll1111ll_opy_
def bstack1lll11llllll_opy_(fixture_name):
    if fixture_name.startswith(bstack1111_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⌖")):
        return bstack1111_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ⌗")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⌘")):
        return bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⌙")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⌚")):
        return bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ⌛")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⌜")):
        return bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⌝")
def bstack1lll1l1111l1_opy_(fixture_name):
    return bool(re.match(bstack1111_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧ⌞"), fixture_name))
def bstack1lll11lll11l_opy_(fixture_name):
    return bool(re.match(bstack1111_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ⌟"), fixture_name))
def bstack1lll1l11111l_opy_(fixture_name):
    return bool(re.match(bstack1111_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ⌠"), fixture_name))
def bstack1lll11lll1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack1111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⌡")):
        return bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⌢"), bstack1111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⌣")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⌤")):
        return bstack1111_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨ⌥"), bstack1111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ⌦")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⌧")):
        return bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⌨"), bstack1111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ〈")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ〉")):
        return bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⌫"), bstack1111_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ⌬")
    return None, None
def bstack1lll1l111111_opy_(hook_name):
    if hook_name in [bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⌭"), bstack1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⌮")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll11llll1l_opy_(hook_name):
    if hook_name in [bstack1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⌯"), bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ⌰")]:
        return bstack1111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⌱")
    elif hook_name in [bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⌲"), bstack1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⌳")]:
        return bstack1111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ⌴")
    elif hook_name in [bstack1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⌵"), bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⌶")]:
        return bstack1111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⌷")
    elif hook_name in [bstack1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⌸"), bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⌹")]:
        return bstack1111_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ⌺")
    return hook_name
def bstack1lll11lll111_opy_(node, scenario):
    if hasattr(node, bstack1111_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ⌻")):
        parts = node.nodeid.rsplit(bstack1111_opy_ (u"ࠦࡠࠨ⌼"))
        params = parts[-1]
        return bstack1111_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧ⌽").format(scenario.name, params)
    return scenario.name
def bstack1lll11llll11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1111_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ⌾")):
            examples = list(node.callspec.params[bstack1111_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭⌿")].values())
        return examples
    except:
        return []
def bstack1lll1l111l11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11lll1ll_opy_(report):
    try:
        status = bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⍀")
        if report.passed or (report.failed and hasattr(report, bstack1111_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ⍁"))):
            status = bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⍂")
        elif report.skipped:
            status = bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⍃")
        bstack1lll11lllll1_opy_(status)
    except:
        pass
def bstack11ll1l11_opy_(status):
    try:
        bstack1lll1l1111ll_opy_ = bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⍄")
        if status == bstack1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⍅"):
            bstack1lll1l1111ll_opy_ = bstack1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⍆")
        elif status == bstack1111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⍇"):
            bstack1lll1l1111ll_opy_ = bstack1111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⍈")
        bstack1lll11lllll1_opy_(bstack1lll1l1111ll_opy_)
    except:
        pass
def bstack1lll1l111l1l_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack11l1l111ll_opy_():
    bstack1111_opy_ (u"ࠥࠦࠧࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡱࡻࡷࡩࡸࡺ࠭ࡱࡣࡵࡥࡱࡲࡥ࡭ࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡣࡱࡨࠥࡸࡥࡵࡷࡵࡲ࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡮ࡶࡩࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥࠣࠤࠥ⍉")
    return bstack1llll1111ll_opy_(bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭⍊"))