# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import re
from bstack_utils.bstack111l1l1l1l_opy_ import bstack1ll1l11l111l_opy_
from bstack_utils.bstack1ll111lll11_opy_ import bstack1ll11l1ll1l_opy_
def bstack1ll1l11lll11_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ☲")):
        return bstack1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ☳")
    elif fixture_name.startswith(bstack1ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ☴")):
        return bstack1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨ☵")
    elif fixture_name.startswith(bstack1ll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ☶")):
        return bstack1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ☷")
    elif fixture_name.startswith(bstack1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ☸")):
        return bstack1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨ☹")
def bstack1ll1l11l1ll1_opy_(fixture_name):
    return bool(re.match(bstack1ll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬ☺"), fixture_name))
def bstack1ll1l11l1lll_opy_(fixture_name):
    return bool(re.match(bstack1ll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ☻"), fixture_name))
def bstack1ll1l11l1111_opy_(fixture_name):
    return bool(re.match(bstack1ll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ☼"), fixture_name))
def bstack1ll1l11l1l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ☽")):
        return bstack1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ☾"), bstack1ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ☿")
    elif fixture_name.startswith(bstack1ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭♀")):
        return bstack1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭♁"), bstack1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ♂")
    elif fixture_name.startswith(bstack1ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ♃")):
        return bstack1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ♄"), bstack1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ♅")
    elif fixture_name.startswith(bstack1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ♆")):
        return bstack1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨ♇"), bstack1ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ♈")
    return None, None
def bstack1ll1l11ll1ll_opy_(hook_name):
    if hook_name in [bstack1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ♉"), bstack1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ♊")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1l111llll_opy_(hook_name):
    if hook_name in [bstack1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ♋"), bstack1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ♌")]:
        return bstack1ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ♍")
    elif hook_name in [bstack1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ♎"), bstack1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ♏")]:
        return bstack1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ♐")
    elif hook_name in [bstack1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭♑"), bstack1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ♒")]:
        return bstack1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ♓")
    elif hook_name in [bstack1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ♔"), bstack1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ♕")]:
        return bstack1ll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ♖")
    return hook_name
def bstack1ll1l11ll1l1_opy_(node, scenario):
    if hasattr(node, bstack1ll_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪ♗")):
        parts = node.nodeid.rsplit(bstack1ll_opy_ (u"ࠤ࡞ࠦ♘"))
        params = parts[-1]
        return bstack1ll_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥ♙").format(scenario.name, params)
    return scenario.name
def bstack1ll1l11l11ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭♚")):
            examples = list(node.callspec.params[bstack1ll_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫ♛")].values())
        return examples
    except:
        return []
def bstack1ll1l11l1l11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll1l11ll111_opy_(report):
    try:
        status = bstack1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭♜")
        if report.passed or (report.failed and hasattr(report, bstack1ll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ♝"))):
            status = bstack1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ♞")
        elif report.skipped:
            status = bstack1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ♟")
        bstack1ll1l11l111l_opy_(status)
    except:
        pass
def bstack11ll1lll_opy_(status):
    try:
        bstack1ll1l11ll11l_opy_ = bstack1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ♠")
        if status == bstack1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ♡"):
            bstack1ll1l11ll11l_opy_ = bstack1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ♢")
        elif status == bstack1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ♣"):
            bstack1ll1l11ll11l_opy_ = bstack1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ♤")
        bstack1ll1l11l111l_opy_(bstack1ll1l11ll11l_opy_)
    except:
        pass
def bstack1ll1l11l11l1_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1111l11ll1_opy_():
    bstack1ll_opy_ (u"ࠣࠤࠥࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡶࡹࡵࡧࡶࡸ࠲ࡶࡡࡳࡣ࡯ࡰࡪࡲࠠࡪࡵࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡡ࡯ࡦࠣࡶࡪࡺࡵࡳࡰࠣࡘࡷࡻࡥࠡ࡫ࡩࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧ࡬ࡴࡧࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪࠨࠢࠣ♥")
    return bstack1ll11l1ll1l_opy_(bstack1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠫ♦"))