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
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack1l1111l111_opy_
logger = logging.getLogger(__name__)
def bstack111l1l1l1l_opy_(bstack1l1l1l1lll_opy_):
  return True if bstack1l1l1l1lll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l111lll_opy_(context, *args):
    tags = getattr(args[0], bstack1ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬᯁ"), [])
    bstack1ll11l1ll_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack1ll11l1ll_opy_
    try:
      bstack1l1l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1l1l1l_opy_(bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᯂ")) else context.browser
      if bstack1l1l11111_opy_ and bstack1l1l11111_opy_.session_id and bstack1ll11l1ll_opy_ and bstack1l1111l111_opy_(
              threading.current_thread(), bstack1ll11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᯃ"), None):
          caps = bstack1l1l11111_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1ll11_opy_ (u"ࠪࡔࡱࡧࡴࡧࡱࡵࡱࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡴࡷࡳࡴࡴࡸࡴࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࠮ࡥ࠯ࡩ࠱࠰ࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠮࠭ᯄ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1l1l11111_opy_, bstack1ll11l1ll_opy_)
    except Exception as e:
       logger.debug(bstack1ll11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫᯅ").format(str(e)))
def bstack11l1l1l1ll_opy_(bstack1l1l11111_opy_):
    if bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᯆ"), None) and bstack1l1111l111_opy_(
      threading.current_thread(), bstack1ll11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᯇ"), None) and not bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪᯈ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack1l1l1ll1l_opy_(bstack1l1l11111_opy_, name=bstack1ll11_opy_ (u"ࠣࠤᯉ"), path=bstack1ll11_opy_ (u"ࠤࠥᯊ"))