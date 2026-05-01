# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import re
from bstack_utils.bstack11111l1ll1_opy_ import bstack1ll11lllll1l_opy_
from bstack_utils.bstack1ll11ll1l11_opy_ import bstack1ll11l111l1_opy_
def bstack1ll1l111l11l_opy_(fixture_name):
    if fixture_name.startswith(bstack111ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⚱")):
        return bstack111ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⚲")
    elif fixture_name.startswith(bstack111ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⚳")):
        return bstack111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩ⚴")
    elif fixture_name.startswith(bstack111ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⚵")):
        return bstack111ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⚶")
    elif fixture_name.startswith(bstack111ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⚷")):
        return bstack111ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩ⚸")
def bstack1ll1l1111lll_opy_(fixture_name):
    return bool(re.match(bstack111ll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭⚹"), fixture_name))
def bstack1ll1l1111l1l_opy_(fixture_name):
    return bool(re.match(bstack111ll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪ⚺"), fixture_name))
def bstack1ll11lllllll_opy_(fixture_name):
    return bool(re.match(bstack111ll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪ⚻"), fixture_name))
def bstack1ll1l111l111_opy_(fixture_name):
    if fixture_name.startswith(bstack111ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⚼")):
        return bstack111ll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⚽"), bstack111ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⚾")
    elif fixture_name.startswith(bstack111ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⚿")):
        return bstack111ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧ⛀"), bstack111ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭⛁")
    elif fixture_name.startswith(bstack111ll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⛂")):
        return bstack111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⛃"), bstack111ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⛄")
    elif fixture_name.startswith(bstack111ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⛅")):
        return bstack111ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩ⛆"), bstack111ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ⛇")
    return None, None
def bstack1ll1l111l1l1_opy_(hook_name):
    if hook_name in [bstack111ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⛈"), bstack111ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⛉")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1l111111l_opy_(hook_name):
    if hook_name in [bstack111ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⛊"), bstack111ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫ⛋")]:
        return bstack111ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⛌")
    elif hook_name in [bstack111ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⛍"), bstack111ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⛎")]:
        return bstack111ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭⛏")
    elif hook_name in [bstack111ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⛐"), bstack111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⛑")]:
        return bstack111ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⛒")
    elif hook_name in [bstack111ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⛓"), bstack111ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⛔")]:
        return bstack111ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ⛕")
    return hook_name
def bstack1ll1l1111ll1_opy_(node, scenario):
    if hasattr(node, bstack111ll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫ⛖")):
        parts = node.nodeid.rsplit(bstack111ll_opy_ (u"ࠥ࡟ࠧ⛗"))
        params = parts[-1]
        return bstack111ll_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦ⛘").format(scenario.name, params)
    return scenario.name
def bstack1ll1l1111111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111ll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ⛙")):
            examples = list(node.callspec.params[bstack111ll_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬ⛚")].values())
        return examples
    except:
        return []
def bstack1ll1l11111l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll11llllll1_opy_(report):
    try:
        status = bstack111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⛛")
        if report.passed or (report.failed and hasattr(report, bstack111ll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⛜"))):
            status = bstack111ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⛝")
        elif report.skipped:
            status = bstack111ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⛞")
        bstack1ll11lllll1l_opy_(status)
    except:
        pass
def bstack11l11ll1l_opy_(status):
    try:
        bstack1ll1l1111l11_opy_ = bstack111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⛟")
        if status == bstack111ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⛠"):
            bstack1ll1l1111l11_opy_ = bstack111ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⛡")
        elif status == bstack111ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⛢"):
            bstack1ll1l1111l11_opy_ = bstack111ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⛣")
        bstack1ll11lllll1l_opy_(bstack1ll1l1111l11_opy_)
    except:
        pass
def bstack1ll1l11111ll_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1l1llll1l1_opy_():
    bstack111ll_opy_ (u"ࠤࠥࠦࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡢࡰࡧࠤࡷ࡫ࡴࡶࡴࡱࠤ࡙ࡸࡵࡦࠢ࡬ࡪࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡ࡭ࡵࡨࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠢࠣࠤ⛤")
    return bstack1ll11l111l1_opy_(bstack111ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡦࡸࡡ࡭࡮ࡨࡰࠬ⛥"))