# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack1l1lll111l_opy_
logger = logging.getLogger(__name__)
def bstack1111l1l1_opy_(bstack11ll1l1ll1_opy_):
  return True if bstack11ll1l1ll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack111ll1lll1_opy_(context, *args):
    tags = getattr(args[0], bstack1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᮘ"), [])
    bstack1l1ll11lll_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack1l1ll11lll_opy_
    try:
      bstack11111l1l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1111l1l1_opy_(bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᮙ")) else context.browser
      if bstack11111l1l11_opy_ and bstack11111l1l11_opy_.session_id and bstack1l1ll11lll_opy_ and bstack1l1lll111l_opy_(
              threading.current_thread(), bstack1l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᮚ"), None):
          caps = bstack11111l1l11_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1l1_opy_ (u"ࠫࡕࡲࡡࡵࡨࡲࡶࡲࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࠨࡦ࠰ࡪ࠲࠱ࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠯ࠧᮛ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack11111l1l11_opy_, bstack1l1ll11lll_opy_)
    except Exception as e:
       logger.debug(bstack1l1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬᮜ").format(str(e)))
def bstack11lll1lll1_opy_(bstack11111l1l11_opy_):
    if bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᮝ"), None) and bstack1l1lll111l_opy_(
      threading.current_thread(), bstack1l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᮞ"), None) and not bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫᮟ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack11l1lll1l_opy_(bstack11111l1l11_opy_, name=bstack1l1_opy_ (u"ࠤࠥᮠ"), path=bstack1l1_opy_ (u"ࠥࠦᮡ"))