# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import re
from bstack_utils.bstack1l1ll1ll1_opy_ import bstack1ll111ll111l_opy_
from bstack_utils.bstack11ll1l11l_opy_ import bstack11l1llll1_opy_
def bstack1ll111lll1ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1llll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⧩")):
        return bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⧪")
    elif fixture_name.startswith(bstack1l1llll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⧫")):
        return bstack1l1llll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧ⧬")
    elif fixture_name.startswith(bstack1l1llll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⧭")):
        return bstack1l1llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⧮")
    elif fixture_name.startswith(bstack1l1llll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⧯")):
        return bstack1l1llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧ⧰")
def bstack1ll111ll1l11_opy_(fixture_name):
    return bool(re.match(bstack1l1llll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ⧱"), fixture_name))
def bstack1ll111ll11l1_opy_(fixture_name):
    return bool(re.match(bstack1l1llll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨ⧲"), fixture_name))
def bstack1ll111llll11_opy_(fixture_name):
    return bool(re.match(bstack1l1llll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨ⧳"), fixture_name))
def bstack1ll111ll1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1llll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⧴")):
        return bstack1l1llll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫ⧵"), bstack1l1llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⧶")
    elif fixture_name.startswith(bstack1l1llll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⧷")):
        return bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬ⧸"), bstack1l1llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ⧹")
    elif fixture_name.startswith(bstack1l1llll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⧺")):
        return bstack1l1llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⧻"), bstack1l1llll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ⧼")
    elif fixture_name.startswith(bstack1l1llll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⧽")):
        return bstack1l1llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧ⧾"), bstack1l1llll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩ⧿")
    return None, None
def bstack1ll111ll1lll_opy_(hook_name):
    if hook_name in [bstack1l1llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⨀"), bstack1l1llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⨁")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll111lll1l1_opy_(hook_name):
    if hook_name in [bstack1l1llll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⨂"), bstack1l1llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ⨃")]:
        return bstack1l1llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⨄")
    elif hook_name in [bstack1l1llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⨅"), bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⨆")]:
        return bstack1l1llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ⨇")
    elif hook_name in [bstack1l1llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⨈"), bstack1l1llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ⨉")]:
        return bstack1l1llll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ⨊")
    elif hook_name in [bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⨋"), bstack1l1llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⨌")]:
        return bstack1l1llll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩ⨍")
    return hook_name
def bstack1ll111lllll1_opy_(node, scenario):
    if hasattr(node, bstack1l1llll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩ⨎")):
        parts = node.nodeid.rsplit(bstack1l1llll_opy_ (u"ࠣ࡝ࠥ⨏"))
        params = parts[-1]
        return bstack1l1llll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤ⨐").format(scenario.name, params)
    return scenario.name
def bstack1ll111lll11l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1llll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ⨑")):
            examples = list(node.callspec.params[bstack1l1llll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪ⨒")].values())
        return examples
    except Exception as e:
        from bstack_utils import logger_utils
        logger_utils.get_logger(__name__).debug(bstack1l1llll_opy_ (u"ࠧࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࡶࠤࡵࡧࡲࡴࡧࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃ࠺ࠡࡽࢀࠦ⨓").format(type(e).__name__, e), exc_info=True)
        return []
def bstack1ll111ll11ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll111lll111_opy_(report):
    try:
        status = bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⨔")
        if report.passed or (report.failed and hasattr(report, bstack1l1llll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⨕"))):
            status = bstack1l1llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⨖")
        elif report.skipped:
            status = bstack1l1llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⨗")
        bstack1ll111ll111l_opy_(status)
    except Exception as e:
        from bstack_utils import logger_utils
        logger_utils.get_logger(__name__).debug(bstack1l1llll_opy_ (u"ࠥࡷࡹࡵࡲࡦࡡࡳࡽࡹ࡫ࡳࡵࡡࡷࡩࡸࡺ࡟ࡴࡶࡤࡸࡺࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀ࠾ࠥࢁࡽࠣ⨘").format(type(e).__name__, e), exc_info=True)
def bstack1lll11l11l_opy_(status):
    try:
        bstack1ll111llll1l_opy_ = bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⨙")
        if status == bstack1l1llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⨚"):
            bstack1ll111llll1l_opy_ = bstack1l1llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⨛")
        elif status == bstack1l1llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⨜"):
            bstack1ll111llll1l_opy_ = bstack1l1llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⨝")
        bstack1ll111ll111l_opy_(bstack1ll111llll1l_opy_)
    except Exception as e:
        from bstack_utils import logger_utils
        logger_utils.get_logger(__name__).debug(bstack1l1llll_opy_ (u"ࠤࡶࡸࡴࡸࡥࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡺࡥࡴࡶࡢࡷࡹࡧࡴࡶࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃ࠺ࠡࡽࢀࠦ⨞").format(type(e).__name__, e), exc_info=True)
def bstack1ll111ll1l1l_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack111l1l1ll1_opy_():
    bstack1l1llll_opy_ (u"ࠥࠦࠧࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡱࡻࡷࡩࡸࡺ࠭ࡱࡣࡵࡥࡱࡲࡥ࡭ࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡣࡱࡨࠥࡸࡥࡵࡷࡵࡲ࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡮ࡶࡩࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥࠣࠤࠥ⨟")
    return bstack11l1llll1_opy_(bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭⨠"))