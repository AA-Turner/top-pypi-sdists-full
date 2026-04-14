# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import re
from bstack_utils.bstack11ll11l1ll_opy_ import bstack1ll1l111ll1l_opy_
from bstack_utils.bstack1ll11l1ll11_opy_ import bstack1ll11ll1lll_opy_
def bstack1ll1l11l1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l111l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ♋")):
        return bstack1l111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ♌")
    elif fixture_name.startswith(bstack1l111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ♍")):
        return bstack1l111l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ♎")
    elif fixture_name.startswith(bstack1l111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ♏")):
        return bstack1l111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ♐")
    elif fixture_name.startswith(bstack1l111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ♑")):
        return bstack1l111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ♒")
def bstack1ll1l11l111l_opy_(fixture_name):
    return bool(re.match(bstack1l111l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ♓"), fixture_name))
def bstack1ll1l11ll1l1_opy_(fixture_name):
    return bool(re.match(bstack1l111l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭♔"), fixture_name))
def bstack1ll1l11l11l1_opy_(fixture_name):
    return bool(re.match(bstack1l111l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭♕"), fixture_name))
def bstack1ll1l11l1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ♖")):
        return bstack1l111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ♗"), bstack1l111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ♘")
    elif fixture_name.startswith(bstack1l111l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ♙")):
        return bstack1l111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ♚"), bstack1l111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ♛")
    elif fixture_name.startswith(bstack1l111l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ♜")):
        return bstack1l111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ♝"), bstack1l111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ♞")
    elif fixture_name.startswith(bstack1l111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ♟")):
        return bstack1l111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ♠"), bstack1l111l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ♡")
    return None, None
def bstack1ll1l111llll_opy_(hook_name):
    if hook_name in [bstack1l111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ♢"), bstack1l111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ♣")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1l11l11ll_opy_(hook_name):
    if hook_name in [bstack1l111l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ♤"), bstack1l111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ♥")]:
        return bstack1l111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ♦")
    elif hook_name in [bstack1l111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ♧"), bstack1l111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ♨")]:
        return bstack1l111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ♩")
    elif hook_name in [bstack1l111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ♪"), bstack1l111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ♫")]:
        return bstack1l111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ♬")
    elif hook_name in [bstack1l111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ♭"), bstack1l111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ♮")]:
        return bstack1l111l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ♯")
    return hook_name
def bstack1ll1l11l1111_opy_(node, scenario):
    if hasattr(node, bstack1l111l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ♰")):
        parts = node.nodeid.rsplit(bstack1l111l_opy_ (u"ࠨ࡛ࠣ♱"))
        params = parts[-1]
        return bstack1l111l_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢ♲").format(scenario.name, params)
    return scenario.name
def bstack1ll1l11l1l1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l111l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪ♳")):
            examples = list(node.callspec.params[bstack1l111l_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨ♴")].values())
        return examples
    except:
        return []
def bstack1ll1l111lll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll1l11ll11l_opy_(report):
    try:
        status = bstack1l111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ♵")
        if report.passed or (report.failed and hasattr(report, bstack1l111l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ♶"))):
            status = bstack1l111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ♷")
        elif report.skipped:
            status = bstack1l111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ♸")
        bstack1ll1l111ll1l_opy_(status)
    except:
        pass
def bstack11111l1l1_opy_(status):
    try:
        bstack1ll1l11l1l11_opy_ = bstack1l111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ♹")
        if status == bstack1l111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ♺"):
            bstack1ll1l11l1l11_opy_ = bstack1l111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ♻")
        elif status == bstack1l111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ♼"):
            bstack1ll1l11l1l11_opy_ = bstack1l111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ♽")
        bstack1ll1l111ll1l_opy_(bstack1ll1l11l1l11_opy_)
    except:
        pass
def bstack1ll1l11ll111_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack11ll11l1l_opy_():
    bstack1l111l_opy_ (u"ࠧࠨࠢࡄࡪࡨࡧࡰࠦࡩࡧࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠤ࡮ࡹࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡥࡳࡪࠠࡳࡧࡷࡹࡷࡴࠠࡕࡴࡸࡩࠥ࡯ࡦࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤࡰࡸ࡫ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠥࠦࠧ♾")
    return bstack1ll11ll1lll_opy_(bstack1l111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡢࡴࡤࡰࡱ࡫࡬ࠨ♿"))