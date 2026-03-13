# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import re
from bstack_utils.session_utils import bstack1lll11l1l111_opy_
from bstack_utils.bstack1lll1l1l1ll_opy_ import bstack1lll1ll11l1_opy_
def bstack1lll11l111ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1111l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⏕")):
        return bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⏖")
    elif fixture_name.startswith(bstack1111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⏗")):
        return bstack1111l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ⏘")
    elif fixture_name.startswith(bstack1111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⏙")):
        return bstack1111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⏚")
    elif fixture_name.startswith(bstack1111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⏛")):
        return bstack1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ⏜")
def bstack1lll11l1lll1_opy_(fixture_name):
    return bool(re.match(bstack1111l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ⏝"), fixture_name))
def bstack1lll11l1l11l_opy_(fixture_name):
    return bool(re.match(bstack1111l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭⏞"), fixture_name))
def bstack1lll11l11ll1_opy_(fixture_name):
    return bool(re.match(bstack1111l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭⏟"), fixture_name))
def bstack1lll11l1ll11_opy_(fixture_name):
    if fixture_name.startswith(bstack1111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⏠")):
        return bstack1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⏡"), bstack1111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⏢")
    elif fixture_name.startswith(bstack1111l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⏣")):
        return bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⏤"), bstack1111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ⏥")
    elif fixture_name.startswith(bstack1111l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⏦")):
        return bstack1111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ⏧"), bstack1111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ⏨")
    elif fixture_name.startswith(bstack1111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⏩")):
        return bstack1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ⏪"), bstack1111l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ⏫")
    return None, None
def bstack1lll11l1l1l1_opy_(hook_name):
    if hook_name in [bstack1111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⏬"), bstack1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⏭")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll11l11l1l_opy_(hook_name):
    if hook_name in [bstack1111l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⏮"), bstack1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⏯")]:
        return bstack1111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⏰")
    elif hook_name in [bstack1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⏱"), bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⏲")]:
        return bstack1111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ⏳")
    elif hook_name in [bstack1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⏴"), bstack1111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ⏵")]:
        return bstack1111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ⏶")
    elif hook_name in [bstack1111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⏷"), bstack1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⏸")]:
        return bstack1111l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ⏹")
    return hook_name
def bstack1lll11l11l11_opy_(node, scenario):
    if hasattr(node, bstack1111l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ⏺")):
        parts = node.nodeid.rsplit(bstack1111l_opy_ (u"ࠨ࡛ࠣ⏻"))
        params = parts[-1]
        return bstack1111l_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢ⏼").format(scenario.name, params)
    return scenario.name
def bstack1lll11l11lll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1111l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪ⏽")):
            examples = list(node.callspec.params[bstack1111l_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨ⏾")].values())
        return examples
    except:
        return []
def bstack1lll11l1llll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11ll1111_opy_(report):
    try:
        status = bstack1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⏿")
        if report.passed or (report.failed and hasattr(report, bstack1111l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ␀"))):
            status = bstack1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ␁")
        elif report.skipped:
            status = bstack1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ␂")
        bstack1lll11l1l111_opy_(status)
    except:
        pass
def bstack111lll111_opy_(status):
    try:
        bstack1lll11l1l1ll_opy_ = bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ␃")
        if status == bstack1111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ␄"):
            bstack1lll11l1l1ll_opy_ = bstack1111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ␅")
        elif status == bstack1111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ␆"):
            bstack1lll11l1l1ll_opy_ = bstack1111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ␇")
        bstack1lll11l1l111_opy_(bstack1lll11l1l1ll_opy_)
    except:
        pass
def bstack1lll11l1ll1l_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1ll1l1l1_opy_():
    bstack1111l_opy_ (u"ࠧࠨࠢࡄࡪࡨࡧࡰࠦࡩࡧࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠤ࡮ࡹࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡥࡳࡪࠠࡳࡧࡷࡹࡷࡴࠠࡕࡴࡸࡩࠥ࡯ࡦࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤࡰࡸ࡫ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠥࠦࠧ␈")
    return bstack1lll1ll11l1_opy_(bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡢࡴࡤࡰࡱ࡫࡬ࠨ␉"))