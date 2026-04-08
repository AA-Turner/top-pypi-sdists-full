# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack1llll11111_opy_
logger = logging.getLogger(__name__)
def bstack1l11llll11_opy_(bstack11l1l1l11_opy_):
  return True if bstack11l1l1l11_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l11l1lll_opy_(context, *args):
    tags = getattr(args[0], bstack111l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᶐ"), [])
    bstack11llll11l_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack11llll11l_opy_
    try:
      bstack1llll11l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11llll11_opy_(bstack111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᶑ")) else context.browser
      if bstack1llll11l1l_opy_ and bstack1llll11l1l_opy_.session_id and bstack11llll11l_opy_ and bstack1llll11111_opy_(
              threading.current_thread(), bstack111l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᶒ"), None):
          caps = bstack1llll11l1l_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack111l_opy_ (u"ࠫࡕࡲࡡࡵࡨࡲࡶࡲࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࠨࡦ࠰ࡪ࠲࠱ࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠯ࠧᶓ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1llll11l1l_opy_, bstack11llll11l_opy_)
    except Exception as e:
       logger.debug(bstack111l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬᶔ").format(str(e)))
def bstack1llll1llll_opy_(bstack1llll11l1l_opy_):
    if bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᶕ"), None) and bstack1llll11111_opy_(
      threading.current_thread(), bstack111l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᶖ"), None) and not bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫᶗ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack111lll111l_opy_(bstack1llll11l1l_opy_, name=bstack111l_opy_ (u"ࠤࠥᶘ"), path=bstack111l_opy_ (u"ࠥࠦᶙ"))