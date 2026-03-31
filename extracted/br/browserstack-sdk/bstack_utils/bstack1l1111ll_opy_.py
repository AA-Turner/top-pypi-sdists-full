# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import re
from bstack_utils.session_utils import bstack1lll11111lll_opy_
from bstack_utils.bstack1lll111l1l1_opy_ import bstack1lll111ll1l_opy_
def bstack1lll111111ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⑘")):
        return bstack1ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ⑙")
    elif fixture_name.startswith(bstack1ll11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⑚")):
        return bstack1ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⑛")
    elif fixture_name.startswith(bstack1ll11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⑜")):
        return bstack1ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ⑝")
    elif fixture_name.startswith(bstack1ll11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⑞")):
        return bstack1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⑟")
def bstack1lll11111l11_opy_(fixture_name):
    return bool(re.match(bstack1ll11_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧ①"), fixture_name))
def bstack1lll11111l1l_opy_(fixture_name):
    return bool(re.match(bstack1ll11_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ②"), fixture_name))
def bstack1lll11111ll1_opy_(fixture_name):
    return bool(re.match(bstack1ll11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ③"), fixture_name))
def bstack1lll11111111_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ④")):
        return bstack1ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⑤"), bstack1ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⑥")
    elif fixture_name.startswith(bstack1ll11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⑦")):
        return bstack1ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨ⑧"), bstack1ll11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ⑨")
    elif fixture_name.startswith(bstack1ll11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⑩")):
        return bstack1ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⑪"), bstack1ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⑫")
    elif fixture_name.startswith(bstack1ll11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⑬")):
        return bstack1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⑭"), bstack1ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ⑮")
    return None, None
def bstack1ll1llllll1l_opy_(hook_name):
    if hook_name in [bstack1ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⑯"), bstack1ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⑰")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1lllllll1_opy_(hook_name):
    if hook_name in [bstack1ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⑱"), bstack1ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ⑲")]:
        return bstack1ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⑳")
    elif hook_name in [bstack1ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⑴"), bstack1ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⑵")]:
        return bstack1ll11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ⑶")
    elif hook_name in [bstack1ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⑷"), bstack1ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⑸")]:
        return bstack1ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⑹")
    elif hook_name in [bstack1ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⑺"), bstack1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⑻")]:
        return bstack1ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ⑼")
    return hook_name
def bstack1ll1llllllll_opy_(node, scenario):
    if hasattr(node, bstack1ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ⑽")):
        parts = node.nodeid.rsplit(bstack1ll11_opy_ (u"ࠦࡠࠨ⑾"))
        params = parts[-1]
        return bstack1ll11_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧ⑿").format(scenario.name, params)
    return scenario.name
def bstack1lll1111111l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ⒀")):
            examples = list(node.callspec.params[bstack1ll11_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭⒁")].values())
        return examples
    except:
        return []
def bstack1ll1llllll11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll1111l11l_opy_(report):
    try:
        status = bstack1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⒂")
        if report.passed or (report.failed and hasattr(report, bstack1ll11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ⒃"))):
            status = bstack1ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⒄")
        elif report.skipped:
            status = bstack1ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⒅")
        bstack1lll11111lll_opy_(status)
    except:
        pass
def bstack1l1l11l1ll_opy_(status):
    try:
        bstack1lll111111l1_opy_ = bstack1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⒆")
        if status == bstack1ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⒇"):
            bstack1lll111111l1_opy_ = bstack1ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⒈")
        elif status == bstack1ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⒉"):
            bstack1lll111111l1_opy_ = bstack1ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⒊")
        bstack1lll11111lll_opy_(bstack1lll111111l1_opy_)
    except:
        pass
def bstack1lll1111l111_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1l1lll11_opy_():
    bstack1ll11_opy_ (u"ࠥࠦࠧࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡱࡻࡷࡩࡸࡺ࠭ࡱࡣࡵࡥࡱࡲࡥ࡭ࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡣࡱࡨࠥࡸࡥࡵࡷࡵࡲ࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡮ࡶࡩࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥࠣࠤࠥ⒋")
    return bstack1lll111ll1l_opy_(bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭⒌"))