# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack11l11l1ll_opy_
logger = logging.getLogger(__name__)
def bstack11111l1l11_opy_(bstack1l1l1l111l_opy_):
  return True if bstack1l1l1l111l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll11lll1_opy_(context, *args):
    tags = getattr(args[0], bstack1ll1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᶐ"), [])
    bstack11ll111lll_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack11ll111lll_opy_
    try:
      bstack1ll1lll11_opy_ = threading.current_thread().bstackSessionDriver if bstack11111l1l11_opy_(bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᶑ")) else context.browser
      if bstack1ll1lll11_opy_ and bstack1ll1lll11_opy_.session_id and bstack11ll111lll_opy_ and bstack11l11l1ll_opy_(
              threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᶒ"), None):
          caps = bstack1ll1lll11_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1ll1l11_opy_ (u"ࠫࡕࡲࡡࡵࡨࡲࡶࡲࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࠨࡦ࠰ࡪ࠲࠱ࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠯ࠧᶓ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1ll1lll11_opy_, bstack11ll111lll_opy_)
    except Exception as e:
       logger.debug(bstack1ll1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬᶔ").format(str(e)))
def bstack1111ll1111_opy_(bstack1ll1lll11_opy_):
    if bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᶕ"), None) and bstack11l11l1ll_opy_(
      threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᶖ"), None) and not bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫᶗ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack11l1l11l11_opy_(bstack1ll1lll11_opy_, name=bstack1ll1l11_opy_ (u"ࠤࠥᶘ"), path=bstack1ll1l11_opy_ (u"ࠥࠦᶙ"))