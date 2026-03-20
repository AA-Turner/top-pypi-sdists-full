# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import re
from bstack_utils.session_utils import bstack1lll1111ll1l_opy_
from bstack_utils.bstack1lll11l1ll1_opy_ import bstack1lll11111l1_opy_
def bstack1lll111l1111_opy_(fixture_name):
    if fixture_name.startswith(bstack11lll1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ␠")):
        return bstack11lll1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ␡")
    elif fixture_name.startswith(bstack11lll1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ␢")):
        return bstack11lll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ␣")
    elif fixture_name.startswith(bstack11lll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ␤")):
        return bstack11lll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ␥")
    elif fixture_name.startswith(bstack11lll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ␦")):
        return bstack11lll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ␧")
def bstack1lll1111lll1_opy_(fixture_name):
    return bool(re.match(bstack11lll1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧ␨"), fixture_name))
def bstack1lll111l1ll1_opy_(fixture_name):
    return bool(re.match(bstack11lll1_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ␩"), fixture_name))
def bstack1lll1111l1ll_opy_(fixture_name):
    return bool(re.match(bstack11lll1_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ␪"), fixture_name))
def bstack1lll1111l1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11lll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ␫")):
        return bstack11lll1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ␬"), bstack11lll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ␭")
    elif fixture_name.startswith(bstack11lll1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ␮")):
        return bstack11lll1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨ␯"), bstack11lll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ␰")
    elif fixture_name.startswith(bstack11lll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ␱")):
        return bstack11lll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ␲"), bstack11lll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ␳")
    elif fixture_name.startswith(bstack11lll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ␴")):
        return bstack11lll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ␵"), bstack11lll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ␶")
    return None, None
def bstack1lll111l1l11_opy_(hook_name):
    if hook_name in [bstack11lll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ␷"), bstack11lll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭␸")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll111l1lll_opy_(hook_name):
    if hook_name in [bstack11lll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭␹"), bstack11lll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ␺")]:
        return bstack11lll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ␻")
    elif hook_name in [bstack11lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ␼"), bstack11lll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ␽")]:
        return bstack11lll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ␾")
    elif hook_name in [bstack11lll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ␿"), bstack11lll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⑀")]:
        return bstack11lll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⑁")
    elif hook_name in [bstack11lll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⑂"), bstack11lll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⑃")]:
        return bstack11lll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ⑄")
    return hook_name
def bstack1lll1111ll11_opy_(node, scenario):
    if hasattr(node, bstack11lll1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ⑅")):
        parts = node.nodeid.rsplit(bstack11lll1_opy_ (u"ࠦࡠࠨ⑆"))
        params = parts[-1]
        return bstack11lll1_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧ⑇").format(scenario.name, params)
    return scenario.name
def bstack1lll111l11l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11lll1_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ⑈")):
            examples = list(node.callspec.params[bstack11lll1_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭⑉")].values())
        return examples
    except:
        return []
def bstack1lll111l111l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll111l11ll_opy_(report):
    try:
        status = bstack11lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⑊")
        if report.passed or (report.failed and hasattr(report, bstack11lll1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ⑋"))):
            status = bstack11lll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⑌")
        elif report.skipped:
            status = bstack11lll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⑍")
        bstack1lll1111ll1l_opy_(status)
    except:
        pass
def bstack1111l1l1l_opy_(status):
    try:
        bstack1lll1111llll_opy_ = bstack11lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⑎")
        if status == bstack11lll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⑏"):
            bstack1lll1111llll_opy_ = bstack11lll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⑐")
        elif status == bstack11lll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⑑"):
            bstack1lll1111llll_opy_ = bstack11lll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⑒")
        bstack1lll1111ll1l_opy_(bstack1lll1111llll_opy_)
    except:
        pass
def bstack1lll111l1l1l_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1ll1ll1l11_opy_():
    bstack11lll1_opy_ (u"ࠥࠦࠧࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡱࡻࡷࡩࡸࡺ࠭ࡱࡣࡵࡥࡱࡲࡥ࡭ࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡣࡱࡨࠥࡸࡥࡵࡷࡵࡲ࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡮ࡶࡩࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥࠣࠤࠥ⑓")
    return bstack1lll11111l1_opy_(bstack11lll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭⑔"))