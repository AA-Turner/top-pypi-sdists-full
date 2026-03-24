# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack111l1lll11_opy_
logger = logging.getLogger(__name__)
def bstack11l11l1l_opy_(bstack111ll11ll_opy_):
  return True if bstack111ll11ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l1lll111_opy_(context, *args):
    tags = getattr(args[0], bstack1ll1lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᮓ"), [])
    bstack111ll1l111_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack111ll1l111_opy_
    try:
      bstack1l1l1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11l1l_opy_(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᮔ")) else context.browser
      if bstack1l1l1ll11l_opy_ and bstack1l1l1ll11l_opy_.session_id and bstack111ll1l111_opy_ and bstack111l1lll11_opy_(
              threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᮕ"), None):
          caps = bstack1l1l1ll11l_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1ll1lll_opy_ (u"࠭ࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡷࡺࡶࡰࡰࡴࡷࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࠪࡨ࠲࡬࠴ࠬࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠪࠩᮖ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1l1l1ll11l_opy_, bstack111ll1l111_opy_)
    except Exception as e:
       logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡤ࠵࠶ࡿࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧᮗ").format(str(e)))
def bstack1111l1111l_opy_(bstack1l1l1ll11l_opy_):
    if bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᮘ"), None) and bstack111l1lll11_opy_(
      threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᮙ"), None) and not bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡠࡵࡷࡳࡵ࠭ᮚ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack1ll1ll11ll_opy_(bstack1l1l1ll11l_opy_, name=bstack1ll1lll_opy_ (u"ࠦࠧᮛ"), path=bstack1ll1lll_opy_ (u"ࠧࠨᮜ"))