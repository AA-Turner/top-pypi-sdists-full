# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import re
from bstack_utils.session_utils import bstack1lll111111l1_opy_
from bstack_utils.bstack1lll1111lll_opy_ import bstack1ll1llll1l1_opy_
def bstack1ll1llllllll_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⑇")):
        return bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⑈")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⑉")):
        return bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧ⑊")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⑋")):
        return bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⑌")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⑍")):
        return bstack1ll1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧ⑎")
def bstack1lll1111l1ll_opy_(fixture_name):
    return bool(re.match(bstack1ll1lll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ⑏"), fixture_name))
def bstack1lll111111ll_opy_(fixture_name):
    return bool(re.match(bstack1ll1lll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨ⑐"), fixture_name))
def bstack1lll1111l1l1_opy_(fixture_name):
    return bool(re.match(bstack1ll1lll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨ⑑"), fixture_name))
def bstack1lll11111ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⑒")):
        return bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ⑓"), bstack1ll1lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⑔")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⑕")):
        return bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ⑖"), bstack1ll1lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ⑗")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⑘")):
        return bstack1ll1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⑙"), bstack1ll1lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ⑚")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⑛")):
        return bstack1ll1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧ⑜"), bstack1ll1lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩ⑝")
    return None, None
def bstack1lll11111111_opy_(hook_name):
    if hook_name in [bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⑞"), bstack1ll1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⑟")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll11111l1l_opy_(hook_name):
    if hook_name in [bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ①"), bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ②")]:
        return bstack1ll1lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ③")
    elif hook_name in [bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ④"), bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⑤")]:
        return bstack1ll1lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ⑥")
    elif hook_name in [bstack1ll1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⑦"), bstack1ll1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ⑧")]:
        return bstack1ll1lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ⑨")
    elif hook_name in [bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⑩"), bstack1ll1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⑪")]:
        return bstack1ll1lll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩ⑫")
    return hook_name
def bstack1lll1111l111_opy_(node, scenario):
    if hasattr(node, bstack1ll1lll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩ⑬")):
        parts = node.nodeid.rsplit(bstack1ll1lll_opy_ (u"ࠣ࡝ࠥ⑭"))
        params = parts[-1]
        return bstack1ll1lll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤ⑮").format(scenario.name, params)
    return scenario.name
def bstack1ll1lllllll1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll1lll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ⑯")):
            examples = list(node.callspec.params[bstack1ll1lll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪ⑰")].values())
        return examples
    except:
        return []
def bstack1lll1111111l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11111lll_opy_(report):
    try:
        status = bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⑱")
        if report.passed or (report.failed and hasattr(report, bstack1ll1lll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⑲"))):
            status = bstack1ll1lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⑳")
        elif report.skipped:
            status = bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⑴")
        bstack1lll111111l1_opy_(status)
    except:
        pass
def bstack1ll1l11ll_opy_(status):
    try:
        bstack1lll11111l11_opy_ = bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⑵")
        if status == bstack1ll1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⑶"):
            bstack1lll11111l11_opy_ = bstack1ll1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⑷")
        elif status == bstack1ll1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⑸"):
            bstack1lll11111l11_opy_ = bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⑹")
        bstack1lll111111l1_opy_(bstack1lll11111l11_opy_)
    except:
        pass
def bstack1lll1111l11l_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1l1ll1l1ll_opy_():
    bstack1ll1lll_opy_ (u"ࠢࠣࠤࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡵࡿࡴࡦࡵࡷ࠱ࡵࡧࡲࡢ࡮࡯ࡩࡱࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥࡧ࡮ࡥࠢࡵࡩࡹࡻࡲ࡯ࠢࡗࡶࡺ࡫ࠠࡪࡨࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦࡲࡳࡦࠢࡲࡸ࡭࡫ࡲࡸ࡫ࡶࡩࠧࠨࠢ⑺")
    return bstack1ll1llll1l1_opy_(bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡤࡶࡦࡲ࡬ࡦ࡮ࠪ⑻"))