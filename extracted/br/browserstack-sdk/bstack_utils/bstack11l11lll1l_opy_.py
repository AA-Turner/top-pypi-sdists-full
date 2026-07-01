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
import logging
import threading
import uuid as _uuid
from datetime import datetime, timezone
from bstack_utils.helper import bstack11ll11lll1_opy_
logger = logging.getLogger(__name__)
_1ll11111ll1l_opy_ = False
_1ll11111llll_opy_ = None
_1ll111111lll_opy_ = None
_1ll11111lll1_opy_ = bstack1l1llll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥ࡬ࡵࡵࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⩵")
_1ll111111ll1_opy_ = bstack1l1llll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟࡭ࡶࡶࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠪ⩶")
_1ll1111l11ll_opy_ = bstack1l1llll_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠ࡮ࡷࡷࡤ࡫࡭ࡪࡶࡷࡩࡩ࠭⩷")
def _1ll11111l11l_opy_():
    return datetime.now(timezone.utc).isoformat()
def _1ll1111l11l1_opy_(driver):
    bstack1l1llll_opy_ (u"ࠣࠤࠥࡆࡪࡹࡴ࠮ࡧࡩࡪࡴࡸࡴࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳࠢࡦࡥࡵࡹ࠮ࠡࡑࡵࡨࡪࡸ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴ࠰ࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠ࠮ࡀࠣࡸࡴࡶ࠭࡭ࡧࡹࡩࡱࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࠲ࡄࠠࡴࡪࡲࡶࡹࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭ࡪࡦ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ⩸")
    try:
        caps = getattr(driver, bstack1l1llll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ⩹"), None) or {}
        bstack1ll11111l1l1_opy_ = caps.get(bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⩺")) or {}
        if bstack1ll11111l1l1_opy_.get(bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⩻")):
            return str(bstack1ll11111l1l1_opy_[bstack1l1llll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⩼")])
        if caps.get(bstack1l1llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⩽")):
            return str(caps[bstack1l1llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⩾")])
        sid = getattr(driver, bstack1l1llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬ⩿"), bstack1l1llll_opy_ (u"ࠩࠪ⪀")) or bstack1l1llll_opy_ (u"ࠪࠫ⪁")
        if sid:
            return bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࢁࡽࠨ⪂").format(str(sid)[:8])
    except Exception:
        pass
    return bstack1l1llll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳ࠳ࡻࡾࠩ⪃").format(_uuid.uuid4().hex[:8])
def _1ll1111l1ll1_opy_():
    bstack1l1llll_opy_ (u"ࠨࠢࠣࡔࡨࡸࡺࡸ࡮ࡴࠢࡗࡶࡺ࡫ࠠࡪࡨࠣࡹࡳ࡯ࡴࡵࡧࡶࡸࡤࡶࡡࡵࡥ࡫ࠤ࡭ࡧࡳࠡࡨ࡬ࡶࡪࡪࠠࡐࡔࠣࡥࠥࡻ࡮ࡪࡶࡷࡩࡸࡺ࠮ࡕࡧࡶࡸࡈࡧࡳࡦࠢࡩࡶࡦࡳࡥࠋࠢࠣࠤࠥ࡯ࡳࠡࡱࡱࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡦࡥࡱࡲࠠࡴࡶࡤࡧࡰ࠴ࠠࡖࡵࡨࡨࠥࡺ࡯ࠡࡵ࡮࡭ࡵࠦࡡࡶࡶࡲ࠱ࡪࡳࡩࡵࠢࡩࡳࡷࠦࡵ࡯࡫ࡷࡸࡪࡹࡴ࠮ࡵࡷࡽࡱ࡫ࠊࠡࠢࠣࠤࡷࡻ࡮ࡴࠢࠫࡻ࡭࡫ࡲࡦࠢࡸࡲ࡮ࡺࡴࡦࡵࡷࡣࡵࡧࡴࡤࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡪࡳࡩࡵࡵࠣࡴࡪࡸ࠭ࡵࡧࡶࡸࠥ࡫ࡶࡦࡰࡷࡷ࠮࠴ࠢࠣࠤ⪄")
    try:
        from bstack_utils import bstack1ll1l111lll_opy_
        if getattr(bstack1ll1l111lll_opy_, bstack1l1llll_opy_ (u"ࠧࡠࡈࡌࡖࡊࡊ࡟ࡂࡖࡢࡐࡊࡇࡓࡕࡡࡒࡒࡈࡋࠧ⪅"), False):
            return True
    except Exception:
        pass
    try:
        import sys
        import unittest as _1ll1111l1111_opy_
        frame = sys._getframe(2)
        while frame is not None:
            bstack1ll11111l1ll_opy_ = frame.f_locals.get(bstack1l1llll_opy_ (u"ࠨࡵࡨࡰ࡫࠭⪆"))
            if bstack1ll11111l1ll_opy_ is not None and isinstance(bstack1ll11111l1ll_opy_, _1ll1111l1111_opy_.TestCase):
                return True
            frame = frame.f_back
    except Exception:
        pass
    return False
def _1ll11111ll11_opy_(self, *args, **kwargs):
    ret = _1ll111111lll_opy_(self, *args, **kwargs)
    if not bstack11ll11lll1_opy_():
        return ret
    try:
        setattr(self, _1ll11111lll1_opy_, _1ll11111l11l_opy_())
        setattr(self, _1ll111111ll1_opy_, _1ll1111l11l1_opy_(self))
        setattr(self, _1ll1111l11ll_opy_, False)
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢࡰ࡮࡬ࡥࡤࡻࡦࡰࡪࡥࡰࡢࡶࡦ࡬࠿ࠦࡩ࡯࡫ࡷࠤࡸࡺࡡ࡮ࡲࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠧ⪇").format(e))
    return ret
def _1ll1111l111l_opy_(self, *args, **kwargs):
    started_at = getattr(self, _1ll11111lll1_opy_, None)
    name = getattr(self, _1ll111111ll1_opy_, None) or _1ll1111l11l1_opy_(self)
    bstack1ll1111l1l11_opy_ = getattr(self, _1ll1111l11ll_opy_, False)
    try:
        return _1ll11111llll_opy_(self, *args, **kwargs)
    finally:
        if (
            not bstack1ll1111l1l11_opy_
            and bstack11ll11lll1_opy_()
            and not _1ll1111l1ll1_opy_()
        ):
            try:
                setattr(self, _1ll1111l11ll_opy_, True)
            except Exception:
                pass
            _1ll11111l111_opy_(self, started_at, name)
def _1ll11111l111_opy_(driver, started_at, name):
    bstack1l1llll_opy_ (u"ࠥࠦࠧࡋ࡭ࡪࡶࠣࡥ࡚ࠥࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩࠦࠫࠡࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠣࡴࡦ࡯ࡲࠡࡴࡨࡴࡷ࡫ࡳࡦࡰࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡩࡸࡩࡷࡧࡵࠎࠥࠦࠠࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡤࡷࠥࡧࠠࡴ࡫ࡱ࡫ࡱ࡫ࠠࡵࡧࡶࡸࠥࡸ࡯ࡸ࠰ࠥࠦࠧ⪈")
    try:
        from bstack_utils.testhub_handler import TestHubHandler
        test_uuid = str(_uuid.uuid4())
        if not started_at:
            started_at = _1ll11111l11l_opy_()
        bstack1ll1ll1ll_opy_ = _1ll11111l11l_opy_()
        common = {
            bstack1l1llll_opy_ (u"ࠫࡹࡿࡰࡦࠩ⪉"): bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࠪ⪊"),
            bstack1l1llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⪋"): bstack1l1llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨ⪌"),
            bstack1l1llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⪍"): test_uuid,
            bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⪎"): name,
            bstack1l1llll_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⪏"): name,
            bstack1l1llll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ⪐"): name,
            bstack1l1llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ⪑"): [name],
            bstack1l1llll_opy_ (u"࠭ࡴࡢࡩࡶࠫ⪒"): [],
            bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⪓"): [],
            bstack1l1llll_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭⪔"): {},
            bstack1l1llll_opy_ (u"ࠩࡥࡳࡩࡿࠧ⪕"): {bstack1l1llll_opy_ (u"ࠪࡰࡦࡴࡧࠨ⪖"): bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⪗"), bstack1l1llll_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⪘"): bstack1l1llll_opy_ (u"࠭ࠧ⪙")},
            bstack1l1llll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩ⪚"): {},
        }
        TestHubHandler.bstack1lll11ll1_opy_({
            bstack1l1llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⪛"): bstack1l1llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⪜"),
            bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⪝"): {**common, bstack1l1llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⪞"): started_at, bstack1l1llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⪟"): bstack1l1llll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⪠")},
        })
        finished = {
            **common,
            bstack1l1llll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⪡"): started_at,
            bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⪢"): bstack1ll1ll1ll_opy_,
            bstack1l1llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⪣"): bstack1l1llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⪤"),
        }
        try:
            finished[bstack1l1llll_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ⪥")] = TestHubHandler.bstack1l11111l_opy_(driver)
        except Exception as bstack1ll1111l1l1l_opy_:
            logger.debug(bstack1l1llll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥ࡬ࡪࡨࡨࡧࡾࡩ࡬ࡦࡡࡳࡥࡹࡩࡨ࠻ࠢ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠡࡣࡷࡸࡦࡩࡨࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠬ⪦").format(bstack1ll1111l1l1l_opy_))
        TestHubHandler.bstack1lll11ll1_opy_({
            bstack1l1llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⪧"): bstack1l1llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⪨"),
            bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⪩"): finished,
        })
        logger.info(bstack1l1llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢࡰ࡮࡬ࡥࡤࡻࡦࡰࡪࡥࡰࡢࡶࡦ࡬࠿ࠦࡥ࡮࡫ࡷࡸࡪࡪࠠࡵࡧࡶࡸࠥࡸ࡯ࡸࠢࡩࡳࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࡂࢁࡽࠨ⪪").format(name))
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣࡱ࡯ࡦࡦࡥࡼࡧࡱ࡫࡟ࡱࡣࡷࡧ࡭ࡀࠠࡦ࡯࡬ࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠩ⪫").format(e))
def apply():
    bstack1l1llll_opy_ (u"ࠦࠧࠨࡉ࡯ࡵࡷࡥࡱࡲࠠࡵࡪࡨࠤ࡜࡫ࡢࡅࡴ࡬ࡺࡪࡸࠠ࡭࡫ࡩࡩࡨࡿࡣ࡭ࡧࠣ࡬ࡴࡵ࡫ࡴ࠰ࠣࡍࡩ࡫࡭ࡱࡱࡷࡩࡳࡺ࠻ࠡࡰࡲ࠱ࡴࡶࠠࡸࡪࡨࡲࠥࡴ࡯ࡵࠌࠣࠤࠥࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡶࡰࡧࡩࡷࠦࡌࡕࡕ࠱ࠤࡈࡧ࡬࡭ࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯࠳ࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠠࡢ࡮ࡲࡲ࡬ࡹࡩࡥࡧࠍࠤࠥࠦࠠࡶࡰ࡬ࡸࡹ࡫ࡳࡵࡡࡳࡥࡹࡩࡨ࠯ࡣࡳࡴࡱࡿࠨࠪ࠰ࠥࠦࠧ⪬")
    global _1ll11111ll1l_opy_, _1ll11111llll_opy_, _1ll111111lll_opy_
    if _1ll11111ll1l_opy_:
        return False
    if not bstack11ll11lll1_opy_():
        return False
    try:
        from selenium.webdriver.remote.webdriver import WebDriver
        _1ll111111lll_opy_ = WebDriver.__init__
        _1ll11111llll_opy_ = WebDriver.quit
        WebDriver.__init__ = _1ll11111ll11_opy_
        WebDriver.quit = _1ll1111l111l_opy_
        _1ll11111ll1l_opy_ = True
        logger.info(bstack1l1llll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥ࡬ࡪࡨࡨࡧࡾࡩ࡬ࡦࡡࡳࡥࡹࡩࡨ࠻ࠢࡤࡴࡵࡲࡩࡦࡦ࡛ࠣࡪࡨࡄࡳ࡫ࡹࡩࡷࠦ࡬ࡪࡨࡨࡧࡾࡩ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡࡨࡲࡶࠥࡒࡔࡔࠢࡦࡹࡸࡺ࡯࡮࠯ࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹࡵࡲࠡࡵࡸࡴࡵࡵࡲࡵࠩ⪭"))
        return True
    except Exception as e:
        logger.error(bstack1l1llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟࡭࡫ࡩࡩࡨࡿࡣ࡭ࡧࡢࡴࡦࡺࡣࡩ࠼ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡࡱࡲ࡯ࡽ࠿ࠦࡻࡾࠩ⪮").format(e))
        return False