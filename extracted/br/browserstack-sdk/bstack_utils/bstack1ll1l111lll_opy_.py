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
bstack1l1llll_opy_ (u"ࠤࠥࠦࡑ࡚ࡓ࠮ࡱࡱࡰࡾࠦࡵ࡯࡫ࡷࡸࡪࡹࡴࠡ࡫ࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࡍࡵ࡯࡬ࡵࠣࡹࡳ࡯ࡴࡵࡧࡶࡸ࠳࡚ࡥࡴࡶࡆࡥࡸ࡫࠮ࡳࡷࡱࠬ࠮ࠦࡴࡰࠢࡨࡱ࡮ࡺࠠࡱࡧࡵ࠱ࡹ࡫ࡳࡵࠢࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠣ࠳࡚ࠥࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠊࡦࡸࡨࡲࡹࡹࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥࠤࡼ࡮ࡥ࡯ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡹࡳࡪࡥࡳࠢࡤࠤࡑࡵࡡࡥࠢࡗࡩࡸࡺࡩ࡯ࡩࠣࡗࡪࡹࡳࡪࡱࡱ࠲ࠏࡉ࡯ࡶࡰࡷࡩࡷࡶࡡࡳࡶࠣࡳ࡫ࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡࡣࡪࡩࡳࡺࠧࡴࠢࡳࡩࡷ࠳ࡴࡦࡵࡷࠤࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡌࡘࡲ࡮ࡺ࠮ࠡࡃࡦࡸ࡮ࡼࡡࡵࡧࡧࠤࡴࡴ࡬ࡺࠌࡺ࡬ࡪࡴࠠࡣࡵࡷࡥࡨࡱ࡟ࡶࡶ࡬ࡰࡸ࠴ࡨࡦ࡮ࡳࡩࡷ࠴ࡩࡴࡡ࡯ࡳࡦࡪ࡟ࡵࡧࡶࡸ࡮ࡴࡧࡠࡵࡨࡷࡸ࡯࡯࡯ࠪࠬࠤࡷ࡫ࡴࡶࡴࡱࡷ࡚ࠥࡲࡶࡧࠣࡷࡴࠦ࡮ࡰࡰ࠰ࡐ࡙࡙ࠊࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠢࡸࡷࡪࡸࡳࠡࡵࡨࡩࠥࡴ࡯ࠡࡥ࡫ࡥࡳ࡭ࡥࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸ࡬ࡳࡷ࠴ࠊࡕࡧࡶࡸࠥࡴࡡ࡮ࡧࡶࠤ࡫ࡵ࡬࡭ࡱࡺࠤࡹ࡮ࡥࠡࡖࡅ࠱ࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡦࡰࡴࡰࡥࡹࡀࠠ࠽࡯ࡲࡨࡺࡲࡥ࠿࠰࠿ࡇࡱࡧࡳࡴࡐࡤࡱࡪࡄ࠮࠽ࡶࡨࡷࡹࡥ࡭ࡦࡶ࡫ࡳࡩࡄࠊࠩࡧ࠱࡫࠳ࠦࡴࡦࡵࡷࡣࡱࡵࡧࡪࡰࡢࡴࡦ࡭ࡥ࠯ࡖࡨࡷࡹࡒ࡯ࡨ࡫ࡱ࠲ࡹ࡫ࡳࡵࡡࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡥ࡬ࡰࡩ࡬ࡲ࠮࠴ࠊࠣࠤࠥ⳶")
import datetime
import logging
import os
import traceback
import uuid
from bstack_utils.helper import bstack11ll11lll1_opy_
logger = logging.getLogger(__name__)
_1l1ll11llll1_opy_ = None
_1ll11111ll1l_opy_ = False
_1l1ll1ll1111_opy_ = False
def _1ll11111l11l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).strftime(bstack1l1llll_opy_ (u"ࠥࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨ࡝ࠦ⳷"))
def _1l1ll1l1ll1l_opy_(test_case):
    bstack1l1llll_opy_ (u"ࠦࠧࠨࡒࡦࡶࡸࡶࡳࠦ࡭ࡰࡦࡸࡰࡪ࠴ࡃ࡭ࡣࡶࡷ࠳ࡺࡥࡴࡶࡢࡱࡪࡺࡨࡰࡦࠣ⠘࡚ࠥࡂ࠮ࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡲࡦࡳࡩ࡯ࡩࠣࡪࡴࡸ࡭ࡢࡶ࠱ࠦࠧࠨ⳸")
    cls = test_case.__class__
    module = cls.__module__ or bstack1l1llll_opy_ (u"ࠧࠨ⳹")
    method = getattr(test_case, bstack1l1llll_opy_ (u"ࠨ࡟ࡵࡧࡶࡸࡒ࡫ࡴࡩࡱࡧࡒࡦࡳࡥࠣ⳺"), bstack1l1llll_opy_ (u"ࠢࠣ⳻")) or bstack1l1llll_opy_ (u"ࠣࠤ⳼")
    return bstack1l1llll_opy_ (u"ࠤࡾࢁ࠳ࢁࡽ࠯ࡽࢀࠦ⳽").format(module, cls.__name__, method) if module else bstack1l1llll_opy_ (u"ࠥࡿࢂ࠴ࡻࡾࠤ⳾").format(cls.__name__, method)
def _1l1ll1l1lll1_opy_(test_case):
    bstack1l1llll_opy_ (u"ࠦࠧࠨࡂࡦࡵࡷ࠱ࡪ࡬ࡦࡰࡴࡷࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣ࡭ࡣࡶࡷࠥ࠮ࡵࡴࡧࡧࠤࡧࡿࠠࡕࡧࡶࡸࡍࡻࡢࠡࡨࡲࡶࠥࡹ࡯ࡶࡴࡦࡩࠥࡲࡩ࡯࡭ࡶ࠭࠳ࠨࠢࠣ⳿")
    try:
        import inspect
        return inspect.getsourcefile(test_case.__class__) or bstack1l1llll_opy_ (u"ࠧࠨⴀ")
    except Exception:
        return bstack1l1llll_opy_ (u"ࠨࠢⴁ")
def _1l1ll1l1111l_opy_(test_case, test_uuid, started_at, bstack1ll1ll1ll_opy_=None, status=bstack1l1llll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣⴂ"), failure=None):
    cls = test_case.__class__
    payload = {
        bstack1l1llll_opy_ (u"ࠣࡶࡼࡴࡪࠨⴃ"): bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺࠢⴄ"),
        bstack1l1llll_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨⴅ"): bstack1l1llll_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨⴆ"),
        bstack1l1llll_opy_ (u"ࠧࡻࡵࡪࡦࠥⴇ"): test_uuid,
        bstack1l1llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦⴈ"): _1l1ll1l1ll1l_opy_(test_case),
        bstack1l1llll_opy_ (u"ࠢࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦⴉ"): _1l1ll1l1ll1l_opy_(test_case),
        bstack1l1llll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢⴊ"): cls.__name__,
        bstack1l1llll_opy_ (u"ࠤࡶࡧࡴࡶࡥࡴࠤⴋ"): [cls.__module__ or bstack1l1llll_opy_ (u"ࠥࠦⴌ"), cls.__name__],
        bstack1l1llll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠢⴍ"): _1l1ll1l1lll1_opy_(test_case),
        bstack1l1llll_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢⴎ"): _1l1ll1l1lll1_opy_(test_case),
        bstack1l1llll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨⴏ"): status,
        bstack1l1llll_opy_ (u"ࠢࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦⴐ"): started_at,
        bstack1l1llll_opy_ (u"ࠣࡶࡤ࡫ࡸࠨⴑ"): [],
        bstack1l1llll_opy_ (u"ࠤ࡫ࡳࡴࡱࡳࠣⴒ"): [],
        bstack1l1llll_opy_ (u"ࠥࡱࡪࡺࡡࠣⴓ"): {},
        bstack1l1llll_opy_ (u"ࠦࡧࡵࡤࡺࠤⴔ"): {bstack1l1llll_opy_ (u"ࠧࡲࡡ࡯ࡩࠥⴕ"): bstack1l1llll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨⴖ"), bstack1l1llll_opy_ (u"ࠢࡤࡱࡧࡩࠧⴗ"): bstack1l1llll_opy_ (u"ࠣࠤⴘ")},
        bstack1l1llll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦⴙ"): {},
    }
    if bstack1ll1ll1ll_opy_:
        payload[bstack1l1llll_opy_ (u"ࠥࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠣⴚ")] = bstack1ll1ll1ll_opy_
    if failure:
        payload[bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩࠧⴛ")] = failure
        payload[bstack1l1llll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡲࡦࡣࡶࡳࡳࠨⴜ")] = failure.get(bstack1l1llll_opy_ (u"ࠨࡲࡦࡣࡶࡳࡳࠨⴝ"), bstack1l1llll_opy_ (u"ࠢࠣⴞ"))
        payload[bstack1l1llll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠢⴟ")] = failure.get(bstack1l1llll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢⴠ"), bstack1l1llll_opy_ (u"ࠥࠦⴡ"))
    return payload
def _1l1ll1l1l1ll_opy_(test_case, bstack1l1ll1l11ll1_opy_, bstack1l1ll1l111l1_opy_):
    bstack1l1llll_opy_ (u"ࠦࠧࠨࡄࡪࡨࡩࠤࡹ࡮ࡥࠡࡷࡱ࡭ࡹࡺࡥࡴࡶࠣࡘࡪࡹࡴࡓࡧࡶࡹࡱࡺࠠࡣࡧࡩࡳࡷ࡫࠯ࡢࡨࡷࡩࡷࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡵࡵࡵࡥࡲࡱࡪ࠴ࠢࠣࠤⴢ")
    def _1l1ll1l11lll_opy_(attr):
        before = bstack1l1ll1l111l1_opy_.get(attr, 0)
        after = len(getattr(bstack1l1ll1l11ll1_opy_, attr, []) or [])
        return after - before
    if _1l1ll1l11lll_opy_(bstack1l1llll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࡷࠧⴣ")) > 0:
        return bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨⴤ"), bstack1l1llll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨⴥ")
    if _1l1ll1l11lll_opy_(bstack1l1llll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦࡵࠥ⴦")) > 0:
        return bstack1l1llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤⴧ"), bstack1l1llll_opy_ (u"ࠥࡥࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ⴨")
    if _1l1ll1l11lll_opy_(bstack1l1llll_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧ⴩")) > 0:
        return bstack1l1llll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨ⴪"), None
    return bstack1l1llll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ⴫"), None
def _1l1ll1l1l1l1_opy_(test_case, bstack1l1ll1l11ll1_opy_, bstack1l1ll1l111l1_opy_):
    bstack1l1llll_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸ࡭࡫ࠠ࡮ࡱࡶࡸࠥࡸࡥࡤࡧࡱࡸࠥ࡫ࡲࡳࡱࡵ࠳࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴ࠭ࠢ࡬ࡪࠥࡧ࡮ࡺ࠰ࠥࠦࠧ⴬")
    try:
        errors = (getattr(bstack1l1ll1l11ll1_opy_, bstack1l1llll_opy_ (u"ࠣࡧࡵࡶࡴࡸࡳࠣⴭ"), []) or [])[bstack1l1ll1l111l1_opy_.get(bstack1l1llll_opy_ (u"ࠤࡨࡶࡷࡵࡲࡴࠤ⴮"), 0):]
        failures = (getattr(bstack1l1ll1l11ll1_opy_, bstack1l1llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨࡷࠧ⴯"), []) or [])[bstack1l1ll1l111l1_opy_.get(bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠨⴰ"), 0):]
        bstack1l1ll1l11l11_opy_ = errors + failures
        if not bstack1l1ll1l11l11_opy_:
            return None
        _, bstack1l1ll1l11111_opy_ = bstack1l1ll1l11l11_opy_[-1]
        return {
            bstack1l1llll_opy_ (u"ࠧࡸࡥࡢࡵࡲࡲࠧⴱ"): bstack1l1ll1l11111_opy_.splitlines()[-1] if bstack1l1ll1l11111_opy_ else bstack1l1llll_opy_ (u"ࠨࠢⴲ"),
            bstack1l1llll_opy_ (u"ࠢࡵࡻࡳࡩࠧⴳ"): bstack1l1llll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤⴴ") if failures else bstack1l1llll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥⴵ"),
            bstack1l1llll_opy_ (u"ࠥࡦࡦࡩ࡫ࡵࡴࡤࡧࡪࠨⴶ"): [bstack1l1ll1l11111_opy_] if bstack1l1ll1l11111_opy_ else [],
        }
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࡥࡰࡢࡶࡦ࡬࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡥࡹ࡮ࡲࡤࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡳࡥࡾࡲ࡯ࡢࡦ࠽ࠤࢀࢃࠢⴷ").format(e))
        return None
def _1l1ll11lllll_opy_():
    bstack1l1llll_opy_ (u"ࠧࠨࠢࡓࡧࡶࡳࡱࡼࡥࠡࡶ࡫ࡩࠥࡧࡣࡵ࡫ࡹࡩࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡥࡴ࡬ࡺࡪࡸࠠࡵࡱࠣࡥࡹࡺࡡࡤࡪࠣ࡭ࡳࠦࡴࡦࡵࡷࡣࡷࡻ࡮࠯࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹ࠮ࠋࠢࠣࠤ࡚ࠥࡥࡴࡶࡋࡹࡧ࠭ࡳࠡࡲࡨࡶ࠲ࡸ࡯ࡸࠢࡣࡳࡷ࡯ࡧࡪࡰࡣ࠰ࠥࡦࡣࡣࡶࡢࡴࡱࡧࡴࡧࡱࡵࡱࡥ࠲ࠠࡡࡥࡥࡸࡤࡨࡲࡰࡹࡶࡩࡷࡦࠬࠡࡣࡱࡨࠏࠦࠠࠡࠢࡣࡷࡪࡹࡳࡪࡱࡱࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࡠࠡࡥࡲࡰࡺࡳ࡮ࡴࠢࡤࡶࡪࠦࡤࡦࡴ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡣ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࡢࠣࡪ࡮࡫࡬ࡥࠌࠣࠤࠥࠦ࡯࡯ࠢࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠣ࠳࡚ࠥࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠠࡱࡣࡼࡰࡴࡧࡤࡴࠢ⠗ࠤࡼ࡯ࡴࡩࡱࡸࡸࠥ࡯ࡴ࠭ࠢࡷ࡬ࡴࡹࡥࠡ࡮ࡤࡲࡩࠐࠠࠡࠢࠣࡒ࡚ࡒࡌࠡࠪࡤࡷࠥࡽࡥࠡࡱࡥࡷࡪࡸࡶࡦࡦࠣࡰࡴࡩࡡ࡭࡮ࡼ࠭ࠥ࡯࡮ࡴࡶࡨࡥࡩࠦ࡯ࡧࠢࡣࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࡡ࠮ࠣࡸ࡭࡫ࠠࡐࡕ࠮ࡦࡷࡵࡷࡴࡧࡵࠎࠥࠦࠠࠡࡵࡷࡶ࡮ࡴࡧ࠭ࠢࡤࡲࡩࠦࡴࡩࡧࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡥࠢࠫࡻ࡭࡯ࡣࡩࠢࡳࡶࡴࡪࡵࡤࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࡒࡌࠦࡌࡕࡕࠣࡶࡴࡽࡳࠋࠢࠣࠤࠥࡩࡡࡳࡴࡼ࠿ࠥࡹࡥࡦࠢࡥࡹ࡮ࡲࡤࠡ࠳࠵࠺࠽࠼࠲࠺࠷࠹ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡸࡥࡧࡧࡵࡩࡳࡩࡥࠡࡵ࡫ࡥࡵ࡫ࠩ࠯ࠌࠣࠤࠥࠦࡔࡩࡧࠣࡗࡉࡑࠠࡴࡶࡤࡱࡵࡹࠠࡵࡪࡨࠤ࡫ࡸࡥࡴࡪ࡯ࡽ࠲ࡩࡲࡦࡣࡷࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡡࡤࡶ࡬ࡺࡪࠦࡴࡩࡴࡨࡥࡩࠦࡩ࡯ࡵ࡬ࡨࡪࠐࠠࠡࠢࠣ࡭ࡹࡹࠠࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡖࡪࡳ࡯ࡵࡧ࠱ࡣࡤ࡯࡮ࡪࡶࡢࡣࠥࡽࡲࡢࡲࠣࠬࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱ࠯ࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠ࠰ࡳࡽࠥࡧࡲࡰࡷࡱࡨࠏࠦࠠࠡࠢࡣࡸ࡭ࡸࡥࡢࡦ࡬ࡲ࡬࠴ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡪࡵࡩࡦࡪࠨࠪ࠰ࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠡ࠿ࠣࡷࡪࡲࡦࡡࠫ࠱ࠤࡕࡿࡴࡦࡵࡷࠤࡵࡲࡵࡨ࡫ࡱࠎࠥࠦࠠࠡࡴࡨࡥࡩࡹࠠࡡ࡫ࡷࡩࡲ࠴࡟ࡥࡴ࡬ࡺࡪࡸࡠࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡱࡺࡲࠥ࡫࡭ࡪࡵࡶ࡭ࡴࡴࠠࡱࡣࡷ࡬ࡀࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠢ࡫ࡥࡸࠦ࡮ࡰࠌࠣࠤࠥࠦࡩࡵࡧࡰࠤࡪࡷࡵࡪࡸࡤࡰࡪࡴࡴ࠭ࠢࡶࡳࠥࡽࡥࠡࡷࡶࡩࠥࡺࡨࡦࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡪࡲࡳࡰࠦࡴࡩࡧࠣࡗࡉࡑࠠࡢ࡮ࡵࡩࡦࡪࡹࠋࠢࠣࠤࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡫ࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤⴸ")
    try:
        import threading
        return getattr(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬⴹ"), None)
    except Exception:
        return None
def _1l1ll1l11l1l_opy_(self, result=None):
    bstack1l1llll_opy_ (u"ࠢࠣࠤࡸࡲ࡮ࡺࡴࡦࡵࡷ࠲࡙࡫ࡳࡵࡅࡤࡷࡪ࠴ࡲࡶࡰࠣࡻࡷࡧࡰࡱࡧࡵࠤࡹ࡮ࡡࡵࠢࡨࡱ࡮ࡺࡳࠡࡲࡨࡶ࠲ࡺࡥࡴࡶࠣࡩࡻ࡫࡮ࡵࡵࠣࡹࡳࡪࡥࡳࠢࡏࡘࡘ࠴ࠢࠣࠤⴺ")
    if _1l1ll11llll1_opy_ is None:
        import unittest as _1l1ll1l1l11l_opy_
        return _1l1ll1l1l11l_opy_.TestCase.run(self, result)
    global _1l1ll1ll1111_opy_
    _1l1ll1ll1111_opy_ = True
    from bstack_utils.testhub_handler import TestHubHandler
    test_uuid = str(uuid.uuid4())
    started_at = _1ll11111l11l_opy_()
    test_name = _1l1ll1l1ll1l_opy_(self)
    bstack1l1ll1l1ll11_opy_ = result if result is not None else None
    bstack1l1ll1l111l1_opy_ = {
        bstack1l1llll_opy_ (u"ࠣࡧࡵࡶࡴࡸࡳࠣⴻ"): len(getattr(bstack1l1ll1l1ll11_opy_, bstack1l1llll_opy_ (u"ࠤࡨࡶࡷࡵࡲࡴࠤⴼ"), []) or []) if bstack1l1ll1l1ll11_opy_ else 0,
        bstack1l1llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨࡷࠧⴽ"): len(getattr(bstack1l1ll1l1ll11_opy_, bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩࡸࠨⴾ"), []) or []) if bstack1l1ll1l1ll11_opy_ else 0,
        bstack1l1llll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨⴿ"): len(getattr(bstack1l1ll1l1ll11_opy_, bstack1l1llll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢⵀ"), []) or []) if bstack1l1ll1l1ll11_opy_ else 0,
    }
    try:
        TestHubHandler.bstack1lll11ll1_opy_({
            bstack1l1llll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠦⵁ"): bstack1l1llll_opy_ (u"ࠣࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤⵂ"),
            bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࠦⵃ"): _1l1ll1l1111l_opy_(self, test_uuid, started_at),
        })
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࡤࡶࡡࡵࡥ࡫࠾࡚ࠥࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩࠦࡥ࡮࡫ࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣⵄ").format(e))
    bstack1l1ll1l1llll_opy_ = None
    try:
        bstack1l1ll1l1l111_opy_ = _1l1ll11llll1_opy_(self, result)
    except BaseException as e:
        bstack1l1ll1l1llll_opy_ = e
        bstack1l1ll1l1l111_opy_ = result
        raise
    finally:
        bstack1ll1ll1ll_opy_ = _1ll11111l11l_opy_()
        if bstack1l1ll1l1l111_opy_ is None:
            bstack1l1ll1l1l111_opy_ = result
        if bstack1l1ll1l1l111_opy_ is not None:
            status, _ = _1l1ll1l1l1ll_opy_(self, bstack1l1ll1l1l111_opy_, bstack1l1ll1l111l1_opy_)
            failure = _1l1ll1l1l1l1_opy_(self, bstack1l1ll1l1l111_opy_, bstack1l1ll1l111l1_opy_)
        elif bstack1l1ll1l1llll_opy_ is not None:
            status = bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦⵅ")
            failure = {
                bstack1l1llll_opy_ (u"ࠧࡸࡥࡢࡵࡲࡲࠧⵆ"): str(bstack1l1ll1l1llll_opy_),
                bstack1l1llll_opy_ (u"ࠨࡴࡺࡲࡨࠦⵇ"): type(bstack1l1ll1l1llll_opy_).__name__,
                bstack1l1llll_opy_ (u"ࠢࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠥⵈ"): [traceback.format_exc()],
            }
        else:
            status = bstack1l1llll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣⵉ")
            failure = None
        payload = _1l1ll1l1111l_opy_(
            self, test_uuid, started_at,
            bstack1ll1ll1ll_opy_=bstack1ll1ll1ll_opy_, status=status, failure=failure,
        )
        try:
            driver = _1l1ll11lllll_opy_()
            if driver is not None:
                payload[bstack1l1llll_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣⵊ")] = TestHubHandler.bstack1l11111l_opy_(driver)
        except Exception as _1l1ll1l111ll_opy_:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࡤࡶࡡࡵࡥ࡫࠾ࠥ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠤࡦࡺࡴࡢࡥ࡫ࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣⵋ").format(_1l1ll1l111ll_opy_))
        try:
            TestHubHandler.bstack1lll11ll1_opy_({
                bstack1l1llll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠣⵌ"): bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠢⵍ"),
                bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࠣⵎ"): payload,
            })
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࡡࡳࡥࡹࡩࡨ࠻ࠢࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠤࡪࡳࡩࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨⵏ").format(e))
    return bstack1l1ll1l1l111_opy_
def apply():
    bstack1l1llll_opy_ (u"ࠣࠤࠥࡍࡳࡹࡴࡢ࡮࡯ࠤࡹ࡮ࡥࠡࡷࡱ࡭ࡹࡺࡥࡴࡶࠣࡴࡦࡺࡣࡩࠢ࡬ࡪࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡵ࡯ࡦࡨࡶࠥࡒࡔࡔ࠰ࠣࡍࡩ࡫࡭ࡱࡱࡷࡩࡳࡺ࠮ࠣࠤࠥⵐ")
    global _1l1ll11llll1_opy_, _1ll11111ll1l_opy_
    if _1ll11111ll1l_opy_:
        return False
    if not bstack11ll11lll1_opy_():
        return False
    try:
        import unittest
        _1l1ll11llll1_opy_ = unittest.TestCase.run
        unittest.TestCase.run = _1l1ll1l11l1l_opy_
        _1ll11111ll1l_opy_ = True
        logger.info(bstack1l1llll_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࡣࡵࡧࡴࡤࡪ࠽ࠤࡦࡶࡰ࡭࡫ࡨࡨࠥࡻ࡮ࡪࡶࡷࡩࡸࡺ࠮ࡕࡧࡶࡸࡈࡧࡳࡦ࠰ࡵࡹࡳࠦࡰࡢࡶࡦ࡬ࠥ࡬࡯ࡳࠢࡏࡘࡘࠨⵑ"))
        return True
    except Exception as e:
        logger.error(bstack1l1llll_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࡤࡶࡡࡵࡥ࡫࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡳࡴࡱࡿࠠࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧⵒ").format(e))
        return False