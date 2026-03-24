# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import re
from bstack_utils.session_utils import bstack1lll1111llll_opy_
from bstack_utils.bstack1lll111l1ll_opy_ import bstack1lll11l1lll_opy_
def bstack1lll1111ll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ␦")):
        return bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ␧")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ␨")):
        return bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩ␩")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ␪")):
        return bstack1ll1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ␫")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ␬")):
        return bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩ␭")
def bstack1lll11111lll_opy_(fixture_name):
    return bool(re.match(bstack1ll1lll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭␮"), fixture_name))
def bstack1lll1111ll11_opy_(fixture_name):
    return bool(re.match(bstack1ll1lll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪ␯"), fixture_name))
def bstack1lll111l1l11_opy_(fixture_name):
    return bool(re.match(bstack1ll1lll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪ␰"), fixture_name))
def bstack1lll111l11l1_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭␱")):
        return bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭␲"), bstack1ll1lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ␳")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ␴")):
        return bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧ␵"), bstack1ll1lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭␶")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ␷")):
        return bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ␸"), bstack1ll1lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ␹")
    elif fixture_name.startswith(bstack1ll1lll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ␺")):
        return bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩ␻"), bstack1ll1lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ␼")
    return None, None
def bstack1lll111l111l_opy_(hook_name):
    if hook_name in [bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ␽"), bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ␾")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll1111l111_opy_(hook_name):
    if hook_name in [bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ␿"), bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫ⑀")]:
        return bstack1ll1lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⑁")
    elif hook_name in [bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⑂"), bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⑃")]:
        return bstack1ll1lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭⑄")
    elif hook_name in [bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⑅"), bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⑆")]:
        return bstack1ll1lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⑇")
    elif hook_name in [bstack1ll1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⑈"), bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⑉")]:
        return bstack1ll1lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ⑊")
    return hook_name
def bstack1lll1111l11l_opy_(node, scenario):
    if hasattr(node, bstack1ll1lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫ⑋")):
        parts = node.nodeid.rsplit(bstack1ll1lll_opy_ (u"ࠥ࡟ࠧ⑌"))
        params = parts[-1]
        return bstack1ll1lll_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦ⑍").format(scenario.name, params)
    return scenario.name
def bstack1lll1111l1ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll1lll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ⑎")):
            examples = list(node.callspec.params[bstack1ll1lll_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬ⑏")].values())
        return examples
    except:
        return []
def bstack1lll1111lll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll1111l1l1_opy_(report):
    try:
        status = bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⑐")
        if report.passed or (report.failed and hasattr(report, bstack1ll1lll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⑑"))):
            status = bstack1ll1lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⑒")
        elif report.skipped:
            status = bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⑓")
        bstack1lll1111llll_opy_(status)
    except:
        pass
def bstack1lll11l1_opy_(status):
    try:
        bstack1lll111l1111_opy_ = bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⑔")
        if status == bstack1ll1lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⑕"):
            bstack1lll111l1111_opy_ = bstack1ll1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⑖")
        elif status == bstack1ll1lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⑗"):
            bstack1lll111l1111_opy_ = bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⑘")
        bstack1lll1111llll_opy_(bstack1lll111l1111_opy_)
    except:
        pass
def bstack1lll111l11ll_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack11lll11l1_opy_():
    bstack1ll1lll_opy_ (u"ࠤࠥࠦࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡰࡺࡶࡨࡷࡹ࠳ࡰࡢࡴࡤࡰࡱ࡫࡬ࠡ࡫ࡶࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡢࡰࡧࠤࡷ࡫ࡴࡶࡴࡱࠤ࡙ࡸࡵࡦࠢ࡬ࡪࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡ࡭ࡵࡨࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠢࠣࠤ⑙")
    return bstack1lll11l1lll_opy_(bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡦࡸࡡ࡭࡮ࡨࡰࠬ⑚"))