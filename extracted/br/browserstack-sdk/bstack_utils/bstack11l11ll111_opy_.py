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
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack11llll11_opy_
logger = logging.getLogger(__name__)
def bstack1l1ll1l1l1l_opy_(bstack1lll1llllll_opy_):
  return True if bstack1lll1llllll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll11l1l1l1_opy_(context, *args):
    tags = getattr(args[0], bstack1l1llll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⁶"), [])
    bstack1ll111l111_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack1ll111l111_opy_
    try:
      bstack111ll1ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1l1l1l_opy_(bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ⁷")) else context.browser
      if bstack111ll1ll11_opy_ and bstack111ll1ll11_opy_.session_id and bstack1ll111l111_opy_ and bstack11llll11_opy_(
              threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⁸"), None):
          caps = bstack111ll1ll11_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1l1llll_opy_ (u"ࠫࡕࡲࡡࡵࡨࡲࡶࡲࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࠨࡦ࠰ࡪ࠲࠱ࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠯ࠧ⁹"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack111ll1ll11_opy_, bstack1ll111l111_opy_)
    except Exception as e:
       logger.debug(bstack1l1llll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬ⁺").format(str(e)))
def bstack1l1ll1l11ll_opy_(bstack111ll1ll11_opy_):
    if bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ⁻"), None) and bstack11llll11_opy_(
      threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⁼"), None) and not bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫ⁽"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack11ll11lll_opy_(bstack111ll1ll11_opy_, name=bstack1l1llll_opy_ (u"ࠤࠥ⁾"), path=bstack1l1llll_opy_ (u"ࠥࠦⁿ"))