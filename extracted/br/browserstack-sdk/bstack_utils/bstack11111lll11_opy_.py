# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack111ll1ll_opy_
logger = logging.getLogger(__name__)
def bstack1ll11l1l1_opy_(bstack111l11ll_opy_):
  return True if bstack111l11ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1111ll11l1_opy_(context, *args):
    tags = getattr(args[0], bstack11lll1_opy_ (u"ࠧࡵࡣࡪࡷࠬᮐ"), [])
    bstack1lll1l11l_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack1lll1l11l_opy_
    try:
      bstack111l111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11l1l1_opy_(bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᮑ")) else context.browser
      if bstack111l111l1_opy_ and bstack111l111l1_opy_.session_id and bstack1lll1l11l_opy_ and bstack111ll1ll_opy_(
              threading.current_thread(), bstack11lll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᮒ"), None):
          caps = bstack111l111l1_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack11lll1_opy_ (u"ࠪࡔࡱࡧࡴࡧࡱࡵࡱࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡴࡷࡳࡴࡴࡸࡴࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࠮ࡥ࠯ࡩ࠱࠰ࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠮࠭ᮓ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack111l111l1_opy_, bstack1lll1l11l_opy_)
    except Exception as e:
       logger.debug(bstack11lll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫᮔ").format(str(e)))
def bstack111lll11ll_opy_(bstack111l111l1_opy_):
    if bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᮕ"), None) and bstack111ll1ll_opy_(
      threading.current_thread(), bstack11lll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᮖ"), None) and not bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪᮗ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack111lll1l1_opy_(bstack111l111l1_opy_, name=bstack11lll1_opy_ (u"ࠣࠤᮘ"), path=bstack11lll1_opy_ (u"ࠤࠥᮙ"))