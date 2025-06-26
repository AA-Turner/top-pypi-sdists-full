# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import re
from bstack_utils.bstack11l1l111_opy_ import bstack11111l1ll1l_opy_
def bstack11111l1lll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll1l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨẟ")):
        return bstack11ll1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨẠ")
    elif fixture_name.startswith(bstack11ll1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨạ")):
        return bstack11ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨẢ")
    elif fixture_name.startswith(bstack11ll1l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨả")):
        return bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨẤ")
    elif fixture_name.startswith(bstack11ll1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪấ")):
        return bstack11ll1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨẦ")
def bstack11111l11ll1_opy_(fixture_name):
    return bool(re.match(bstack11ll1l1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬầ"), fixture_name))
def bstack11111l1l11l_opy_(fixture_name):
    return bool(re.match(bstack11ll1l1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩẨ"), fixture_name))
def bstack11111l11l11_opy_(fixture_name):
    return bool(re.match(bstack11ll1l1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩẩ"), fixture_name))
def bstack11111l11lll_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll1l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬẪ")):
        return bstack11ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬẫ"), bstack11ll1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪẬ")
    elif fixture_name.startswith(bstack11ll1l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ậ")):
        return bstack11ll1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭Ắ"), bstack11ll1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬắ")
    elif fixture_name.startswith(bstack11ll1l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧẰ")):
        return bstack11ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧằ"), bstack11ll1l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨẲ")
    elif fixture_name.startswith(bstack11ll1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨẳ")):
        return bstack11ll1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨẴ"), bstack11ll1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪẵ")
    return None, None
def bstack11111l1l1ll_opy_(hook_name):
    if hook_name in [bstack11ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧẶ"), bstack11ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫặ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11111l11l1l_opy_(hook_name):
    if hook_name in [bstack11ll1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫẸ"), bstack11ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪẹ")]:
        return bstack11ll1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪẺ")
    elif hook_name in [bstack11ll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬẻ"), bstack11ll1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬẼ")]:
        return bstack11ll1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬẽ")
    elif hook_name in [bstack11ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ế"), bstack11ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬế")]:
        return bstack11ll1l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨỀ")
    elif hook_name in [bstack11ll1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧề"), bstack11ll1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧỂ")]:
        return bstack11ll1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪể")
    return hook_name
def bstack11111l111l1_opy_(node, scenario):
    if hasattr(node, bstack11ll1l1_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪỄ")):
        parts = node.nodeid.rsplit(bstack11ll1l1_opy_ (u"ࠤ࡞ࠦễ"))
        params = parts[-1]
        return bstack11ll1l1_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥỆ").format(scenario.name, params)
    return scenario.name
def bstack11111l1llll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11ll1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ệ")):
            examples = list(node.callspec.params[bstack11ll1l1_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫỈ")].values())
        return examples
    except:
        return []
def bstack11111l1ll11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111l111ll_opy_(report):
    try:
        status = bstack11ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ỉ")
        if report.passed or (report.failed and hasattr(report, bstack11ll1l1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤỊ"))):
            status = bstack11ll1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨị")
        elif report.skipped:
            status = bstack11ll1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪỌ")
        bstack11111l1ll1l_opy_(status)
    except:
        pass
def bstack1lll1l11_opy_(status):
    try:
        bstack11111l1l111_opy_ = bstack11ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪọ")
        if status == bstack11ll1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫỎ"):
            bstack11111l1l111_opy_ = bstack11ll1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬỏ")
        elif status == bstack11ll1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧỐ"):
            bstack11111l1l111_opy_ = bstack11ll1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨố")
        bstack11111l1ll1l_opy_(bstack11111l1l111_opy_)
    except:
        pass
def bstack11111l1l1l1_opy_(item=None, report=None, summary=None, extra=None):
    return