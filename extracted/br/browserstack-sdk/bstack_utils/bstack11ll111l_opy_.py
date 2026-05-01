# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack1ll11l1ll1_opy_
logger = logging.getLogger(__name__)
def bstack1l111l1ll1_opy_(bstack1111l1lll1_opy_):
  return True if bstack1111l1lll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l11l1l1_opy_(context, *args):
    tags = getattr(args[0], bstack111ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ᷊"), [])
    bstack111lll11_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack111lll11_opy_
    try:
      bstack1111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l1ll1_opy_(bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ᷋")) else context.browser
      if bstack1111111ll1_opy_ and bstack1111111ll1_opy_.session_id and bstack111lll11_opy_ and bstack1ll11l1ll1_opy_(
              threading.current_thread(), bstack111ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᷌"), None):
          caps = bstack1111111ll1_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack111ll_opy_ (u"࠭ࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡷࡺࡶࡰࡰࡴࡷࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࠪࡨ࠲࡬࠴ࠬࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠪࠩ᷍"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1111111ll1_opy_, bstack111lll11_opy_)
    except Exception as e:
       logger.debug(bstack111ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡤ࠵࠶ࡿࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃ᷎ࠧ").format(str(e)))
def bstack11111lll1l_opy_(bstack1111111ll1_opy_):
    if bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸ᷏ࠬ"), None) and bstack1ll11l1ll1_opy_(
      threading.current_thread(), bstack111ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᷐"), None) and not bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡠࡵࡷࡳࡵ࠭᷑"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack11l1ll11l_opy_(bstack1111111ll1_opy_, name=bstack111ll_opy_ (u"ࠦࠧ᷒"), path=bstack111ll_opy_ (u"ࠧࠨᷓ"))