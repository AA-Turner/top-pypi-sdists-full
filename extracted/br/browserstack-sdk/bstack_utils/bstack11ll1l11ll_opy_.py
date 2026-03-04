# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import re
from bstack_utils.session_utils import bstack1lll1l111l1l_opy_
from bstack_utils.bstack1lll1ll1lll_opy_ import bstack1lll1lll1ll_opy_
def bstack1lll11lll1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⌕")):
        return bstack1lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⌖")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⌗")):
        return bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩ⌘")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⌙")):
        return bstack1lll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⌚")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⌛")):
        return bstack1lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩ⌜")
def bstack1lll11llll1l_opy_(fixture_name):
    return bool(re.match(bstack1lll1l_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭⌝"), fixture_name))
def bstack1lll1l111111_opy_(fixture_name):
    return bool(re.match(bstack1lll1l_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪ⌞"), fixture_name))
def bstack1lll11lll1ll_opy_(fixture_name):
    return bool(re.match(bstack1lll1l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪ⌟"), fixture_name))
def bstack1lll11llll11_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⌠")):
        return bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⌡"), bstack1lll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⌢")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⌣")):
        return bstack1lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧ⌤"), bstack1lll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭⌥")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⌦")):
        return bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⌧"), bstack1lll1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⌨")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ〈")):
        return bstack1lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩ〉"), bstack1lll1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ⌫")
    return None, None
def bstack1lll11lllll1_opy_(hook_name):
    if hook_name in [bstack1lll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⌬"), bstack1lll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⌭")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll1l111lll_opy_(hook_name):
    if hook_name in [bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⌮"), bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫ⌯")]:
        return bstack1lll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⌰")
    elif hook_name in [bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⌱"), bstack1lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⌲")]:
        return bstack1lll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭⌳")
    elif hook_name in [bstack1lll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⌴"), bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⌵")]:
        return bstack1lll1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⌶")
    elif hook_name in [bstack1lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⌷"), bstack1lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⌸")]:
        return bstack1lll1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ⌹")
    return hook_name
def bstack1lll1l111ll1_opy_(node, scenario):
    if hasattr(node, bstack1lll1l_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫ⌺")):
        parts = node.nodeid.rsplit(bstack1lll1l_opy_ (u"ࠥ࡟ࠧ⌻"))
        params = parts[-1]
        return bstack1lll1l_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦ⌼").format(scenario.name, params)
    return scenario.name
def bstack1lll1l1111l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1lll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ⌽")):
            examples = list(node.callspec.params[bstack1lll1l_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬ⌾")].values())
        return examples
    except:
        return []
def bstack1lll1l1111ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11llllll_opy_(report):
    try:
        status = bstack1lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⌿")
        if report.passed or (report.failed and hasattr(report, bstack1lll1l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⍀"))):
            status = bstack1lll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⍁")
        elif report.skipped:
            status = bstack1lll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⍂")
        bstack1lll1l111l1l_opy_(status)
    except:
        pass
def bstack1l111l1ll_opy_(status):
    try:
        bstack1lll1l11111l_opy_ = bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⍃")
        if status == bstack1lll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⍄"):
            bstack1lll1l11111l_opy_ = bstack1lll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⍅")
        elif status == bstack1lll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⍆"):
            bstack1lll1l11111l_opy_ = bstack1lll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⍇")
        bstack1lll1l111l1l_opy_(bstack1lll1l11111l_opy_)
    except:
        pass
def bstack1lll1l111l11_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack11l111lll_opy_():
    bstack1lll1l_opy_ (u"ࠤࠥࠦࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡢࡰࡧࠤࡷ࡫ࡴࡶࡴࡱࠤ࡙ࡸࡵࡦࠢ࡬ࡪࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡ࡭ࡵࡨࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠢࠣࠤ⍈")
    return bstack1lll1lll1ll_opy_(bstack1lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡦࡸࡡ࡭࡮ࡨࡰࠬ⍉"))