# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import re
from bstack_utils.session_utils import bstack1lll1ll11l1l_opy_
from bstack_utils.bstack1llll1111ll_opy_ import bstack1llll11ll11_opy_
def bstack1lll1l1llll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⇫")):
        return bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⇬")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⇭")):
        return bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ⇮")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⇯")):
        return bstack11ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⇰")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⇱")):
        return bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ⇲")
def bstack1lll1l1lll1l_opy_(fixture_name):
    return bool(re.match(bstack11ll111_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ⇳"), fixture_name))
def bstack1lll1l1lllll_opy_(fixture_name):
    return bool(re.match(bstack11ll111_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭⇴"), fixture_name))
def bstack1lll1l1ll1l1_opy_(fixture_name):
    return bool(re.match(bstack11ll111_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭⇵"), fixture_name))
def bstack1lll1ll11l11_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⇶")):
        return bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⇷"), bstack11ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⇸")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⇹")):
        return bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⇺"), bstack11ll111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ⇻")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⇼")):
        return bstack11ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ⇽"), bstack11ll111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ⇾")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⇿")):
        return bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ∀"), bstack11ll111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ∁")
    return None, None
def bstack1lll1l1ll11l_opy_(hook_name):
    if hook_name in [bstack11ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ∂"), bstack11ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ∃")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll1l1ll111_opy_(hook_name):
    if hook_name in [bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ∄"), bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ∅")]:
        return bstack11ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ∆")
    elif hook_name in [bstack11ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ∇"), bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ∈")]:
        return bstack11ll111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ∉")
    elif hook_name in [bstack11ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ∊"), bstack11ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ∋")]:
        return bstack11ll111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ∌")
    elif hook_name in [bstack11ll111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ∍"), bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ∎")]:
        return bstack11ll111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ∏")
    return hook_name
def bstack1lll1ll111ll_opy_(node, scenario):
    if hasattr(node, bstack11ll111_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ∐")):
        parts = node.nodeid.rsplit(bstack11ll111_opy_ (u"ࠨ࡛ࠣ∑"))
        params = parts[-1]
        return bstack11ll111_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢ−").format(scenario.name, params)
    return scenario.name
def bstack1lll1ll11111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11ll111_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪ∓")):
            examples = list(node.callspec.params[bstack11ll111_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨ∔")].values())
        return examples
    except:
        return []
def bstack1lll1ll111l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll1l1ll1ll_opy_(report):
    try:
        status = bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ∕")
        if report.passed or (report.failed and hasattr(report, bstack11ll111_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ∖"))):
            status = bstack11ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ∗")
        elif report.skipped:
            status = bstack11ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ∘")
        bstack1lll1ll11l1l_opy_(status)
    except:
        pass
def bstack1l1ll1ll1l_opy_(status):
    try:
        bstack1lll1ll1111l_opy_ = bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ∙")
        if status == bstack11ll111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ√"):
            bstack1lll1ll1111l_opy_ = bstack11ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ∛")
        elif status == bstack11ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ∜"):
            bstack1lll1ll1111l_opy_ = bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ∝")
        bstack1lll1ll11l1l_opy_(bstack1lll1ll1111l_opy_)
    except:
        pass
def bstack1lll1l1lll11_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack11l11l111_opy_():
    bstack11ll111_opy_ (u"ࠧࠨࠢࡄࡪࡨࡧࡰࠦࡩࡧࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠤ࡮ࡹࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡥࡳࡪࠠࡳࡧࡷࡹࡷࡴࠠࡕࡴࡸࡩࠥ࡯ࡦࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤࡰࡸ࡫ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠥࠦࠧ∞")
    return bstack1llll11ll11_opy_(bstack11ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡢࡴࡤࡰࡱ࡫࡬ࠨ∟"))