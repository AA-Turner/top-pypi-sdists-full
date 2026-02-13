# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import re
from bstack_utils.bstack1ll111l1l1_opy_ import bstack1lll1l1l1l11_opy_
from bstack_utils.bstack1llll1111l1_opy_ import bstack1llll11l1ll_opy_
def bstack1lll1l11llll_opy_(fixture_name):
    if fixture_name.startswith(bstack11l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⇣")):
        return bstack11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ⇤")
    elif fixture_name.startswith(bstack11l11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⇥")):
        return bstack11l11_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫ⇦")
    elif fixture_name.startswith(bstack11l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⇧")):
        return bstack11l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ⇨")
    elif fixture_name.startswith(bstack11l11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⇩")):
        return bstack11l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫ⇪")
def bstack1lll1l11lll1_opy_(fixture_name):
    return bool(re.match(bstack11l11_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨ⇫"), fixture_name))
def bstack1lll1l1l11ll_opy_(fixture_name):
    return bool(re.match(bstack11l11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬ⇬"), fixture_name))
def bstack1lll1l11ll11_opy_(fixture_name):
    return bool(re.match(bstack11l11_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬ⇭"), fixture_name))
def bstack1lll1l1l1111_opy_(fixture_name):
    if fixture_name.startswith(bstack11l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⇮")):
        return bstack11l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⇯"), bstack11l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⇰")
    elif fixture_name.startswith(bstack11l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⇱")):
        return bstack11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩ⇲"), bstack11l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ⇳")
    elif fixture_name.startswith(bstack11l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⇴")):
        return bstack11l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ⇵"), bstack11l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ⇶")
    elif fixture_name.startswith(bstack11l11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⇷")):
        return bstack11l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫ⇸"), bstack11l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭⇹")
    return None, None
def bstack1lll1l11l1l1_opy_(hook_name):
    if hook_name in [bstack11l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⇺"), bstack11l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⇻")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll1l1l1l1l_opy_(hook_name):
    if hook_name in [bstack11l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⇼"), bstack11l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⇽")]:
        return bstack11l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⇾")
    elif hook_name in [bstack11l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⇿"), bstack11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ∀")]:
        return bstack11l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ∁")
    elif hook_name in [bstack11l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ∂"), bstack11l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨ∃")]:
        return bstack11l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ∄")
    elif hook_name in [bstack11l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ∅"), bstack11l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ∆")]:
        return bstack11l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭∇")
    return hook_name
def bstack1lll1l1l111l_opy_(node, scenario):
    if hasattr(node, bstack11l11_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭∈")):
        parts = node.nodeid.rsplit(bstack11l11_opy_ (u"ࠧࡡࠢ∉"))
        params = parts[-1]
        return bstack11l11_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨ∊").format(scenario.name, params)
    return scenario.name
def bstack1lll1l11l111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l11_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩ∋")):
            examples = list(node.callspec.params[bstack11l11_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧ∌")].values())
        return examples
    except:
        return []
def bstack1lll1l11l11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll1l11l1ll_opy_(report):
    try:
        status = bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ∍")
        if report.passed or (report.failed and hasattr(report, bstack11l11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ∎"))):
            status = bstack11l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ∏")
        elif report.skipped:
            status = bstack11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭∐")
        bstack1lll1l1l1l11_opy_(status)
    except:
        pass
def bstack11ll1llll_opy_(status):
    try:
        bstack1lll1l1l11l1_opy_ = bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭∑")
        if status == bstack11l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ−"):
            bstack1lll1l1l11l1_opy_ = bstack11l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ∓")
        elif status == bstack11l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ∔"):
            bstack1lll1l1l11l1_opy_ = bstack11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ∕")
        bstack1lll1l1l1l11_opy_(bstack1lll1l1l11l1_opy_)
    except:
        pass
def bstack1lll1l11ll1l_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1l1111111l_opy_():
    bstack11l11_opy_ (u"ࠦࠧࠨࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡲࡼࡸࡪࡹࡴ࠮ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࠣ࡭ࡸࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠢࡤࡲࡩࠦࡲࡦࡶࡸࡶࡳࠦࡔࡳࡷࡨࠤ࡮࡬ࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡯ࡷࡪࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦࠤࠥࠦ∖")
    return bstack1llll11l1ll_opy_(bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡡࡳࡣ࡯ࡰࡪࡲࠧ∗"))