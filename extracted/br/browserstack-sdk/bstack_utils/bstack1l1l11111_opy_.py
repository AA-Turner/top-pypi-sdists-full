# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import re
from bstack_utils.bstack1l1lllllll_opy_ import bstack11111l11lll_opy_
def bstack11111l11111_opy_(fixture_name):
    if fixture_name.startswith(bstack111l111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨụ")):
        return bstack111l111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨỦ")
    elif fixture_name.startswith(bstack111l111_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨủ")):
        return bstack111l111_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨỨ")
    elif fixture_name.startswith(bstack111l111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨứ")):
        return bstack111l111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨỪ")
    elif fixture_name.startswith(bstack111l111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪừ")):
        return bstack111l111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨỬ")
def bstack11111l111ll_opy_(fixture_name):
    return bool(re.match(bstack111l111_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬử"), fixture_name))
def bstack11111l1l111_opy_(fixture_name):
    return bool(re.match(bstack111l111_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩỮ"), fixture_name))
def bstack11111l1l11l_opy_(fixture_name):
    return bool(re.match(bstack111l111_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩữ"), fixture_name))
def bstack111111llll1_opy_(fixture_name):
    if fixture_name.startswith(bstack111l111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬỰ")):
        return bstack111l111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬự"), bstack111l111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪỲ")
    elif fixture_name.startswith(bstack111l111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ỳ")):
        return bstack111l111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭Ỵ"), bstack111l111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬỵ")
    elif fixture_name.startswith(bstack111l111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧỶ")):
        return bstack111l111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧỷ"), bstack111l111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨỸ")
    elif fixture_name.startswith(bstack111l111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨỹ")):
        return bstack111l111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨỺ"), bstack111l111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪỻ")
    return None, None
def bstack111111lll1l_opy_(hook_name):
    if hook_name in [bstack111l111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧỼ"), bstack111l111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫỽ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11111l111l1_opy_(hook_name):
    if hook_name in [bstack111l111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫỾ"), bstack111l111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪỿ")]:
        return bstack111l111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪἀ")
    elif hook_name in [bstack111l111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬἁ"), bstack111l111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬἂ")]:
        return bstack111l111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬἃ")
    elif hook_name in [bstack111l111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ἄ"), bstack111l111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬἅ")]:
        return bstack111l111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨἆ")
    elif hook_name in [bstack111l111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧἇ"), bstack111l111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧἈ")]:
        return bstack111l111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪἉ")
    return hook_name
def bstack11111l11l1l_opy_(node, scenario):
    if hasattr(node, bstack111l111_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪἊ")):
        parts = node.nodeid.rsplit(bstack111l111_opy_ (u"ࠤ࡞ࠦἋ"))
        params = parts[-1]
        return bstack111l111_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥἌ").format(scenario.name, params)
    return scenario.name
def bstack111111lll11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111l111_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭Ἅ")):
            examples = list(node.callspec.params[bstack111l111_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫἎ")].values())
        return examples
    except:
        return []
def bstack11111l11ll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11111l11l11_opy_(report):
    try:
        status = bstack111l111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ἇ")
        if report.passed or (report.failed and hasattr(report, bstack111l111_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤἐ"))):
            status = bstack111l111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨἑ")
        elif report.skipped:
            status = bstack111l111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪἒ")
        bstack11111l11lll_opy_(status)
    except:
        pass
def bstack11ll1llll1_opy_(status):
    try:
        bstack11111l1111l_opy_ = bstack111l111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪἓ")
        if status == bstack111l111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫἔ"):
            bstack11111l1111l_opy_ = bstack111l111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬἕ")
        elif status == bstack111l111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ἖"):
            bstack11111l1111l_opy_ = bstack111l111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ἗")
        bstack11111l11lll_opy_(bstack11111l1111l_opy_)
    except:
        pass
def bstack111111lllll_opy_(item=None, report=None, summary=None, extra=None):
    return