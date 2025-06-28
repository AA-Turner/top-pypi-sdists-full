# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import re
from bstack_utils.bstack1llll1111l_opy_ import bstack11111l11lll_opy_
def bstack11111l1lll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1ll1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨẟ")):
        return bstack1l1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨẠ")
    elif fixture_name.startswith(bstack1l1ll1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨạ")):
        return bstack1l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨẢ")
    elif fixture_name.startswith(bstack1l1ll1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨả")):
        return bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨẤ")
    elif fixture_name.startswith(bstack1l1ll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪấ")):
        return bstack1l1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨẦ")
def bstack11111l1l1l1_opy_(fixture_name):
    return bool(re.match(bstack1l1ll1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬầ"), fixture_name))
def bstack11111ll1111_opy_(fixture_name):
    return bool(re.match(bstack1l1ll1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩẨ"), fixture_name))
def bstack11111l1l11l_opy_(fixture_name):
    return bool(re.match(bstack1l1ll1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩẩ"), fixture_name))
def bstack11111l1l111_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1ll1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬẪ")):
        return bstack1l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬẫ"), bstack1l1ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪẬ")
    elif fixture_name.startswith(bstack1l1ll1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ậ")):
        return bstack1l1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭Ắ"), bstack1l1ll1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬắ")
    elif fixture_name.startswith(bstack1l1ll1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧẰ")):
        return bstack1l1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧằ"), bstack1l1ll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨẲ")
    elif fixture_name.startswith(bstack1l1ll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨẳ")):
        return bstack1l1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨẴ"), bstack1l1ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪẵ")
    return None, None
def bstack11111l111ll_opy_(hook_name):
    if hook_name in [bstack1l1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧẶ"), bstack1l1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫặ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11111l11l1l_opy_(hook_name):
    if hook_name in [bstack1l1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫẸ"), bstack1l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪẹ")]:
        return bstack1l1ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪẺ")
    elif hook_name in [bstack1l1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬẻ"), bstack1l1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬẼ")]:
        return bstack1l1ll1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬẽ")
    elif hook_name in [bstack1l1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ế"), bstack1l1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬế")]:
        return bstack1l1ll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨỀ")
    elif hook_name in [bstack1l1ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧề"), bstack1l1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧỂ")]:
        return bstack1l1ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪể")
    return hook_name
def bstack11111l11ll1_opy_(node, scenario):
    if hasattr(node, bstack1l1ll1_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪỄ")):
        parts = node.nodeid.rsplit(bstack1l1ll1_opy_ (u"ࠤ࡞ࠦễ"))
        params = parts[-1]
        return bstack1l1ll1_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥỆ").format(scenario.name, params)
    return scenario.name
def bstack11111l1llll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1ll1_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ệ")):
            examples = list(node.callspec.params[bstack1l1ll1_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫỈ")].values())
        return examples
    except:
        return []
def bstack11111l1ll1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111l1l1ll_opy_(report):
    try:
        status = bstack1l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ỉ")
        if report.passed or (report.failed and hasattr(report, bstack1l1ll1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤỊ"))):
            status = bstack1l1ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨị")
        elif report.skipped:
            status = bstack1l1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪỌ")
        bstack11111l11lll_opy_(status)
    except:
        pass
def bstack1l111l1lll_opy_(status):
    try:
        bstack11111l11l11_opy_ = bstack1l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪọ")
        if status == bstack1l1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫỎ"):
            bstack11111l11l11_opy_ = bstack1l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬỏ")
        elif status == bstack1l1ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧỐ"):
            bstack11111l11l11_opy_ = bstack1l1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨố")
        bstack11111l11lll_opy_(bstack11111l11l11_opy_)
    except:
        pass
def bstack11111l1ll11_opy_(item=None, report=None, summary=None, extra=None):
    return