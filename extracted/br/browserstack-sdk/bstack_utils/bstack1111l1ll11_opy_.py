# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack11l11l11_opy_
logger = logging.getLogger(__name__)
def bstack1lll111lll_opy_(bstack1111ll11ll_opy_):
  return True if bstack1111ll11ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll111l11l_opy_(context, *args):
    tags = getattr(args[0], bstack1l1111l_opy_ (u"ࠫࡹࡧࡧࡴࠩᶯ"), [])
    bstack1l1lllll1l_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack1l1lllll1l_opy_
    try:
      bstack1llll1l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll111lll_opy_(bstack1l1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᶰ")) else context.browser
      if bstack1llll1l11_opy_ and bstack1llll1l11_opy_.session_id and bstack1l1lllll1l_opy_ and bstack11l11l11_opy_(
              threading.current_thread(), bstack1l1111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᶱ"), None):
          caps = bstack1llll1l11_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1l1111l_opy_ (u"ࠧࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡸࡻࡰࡱࡱࡵࡸࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࠫࡩ࠳࡭࠮࠭ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠫࠪᶲ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1llll1l11_opy_, bstack1l1lllll1l_opy_)
    except Exception as e:
       logger.debug(bstack1l1111l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨᶳ").format(str(e)))
def bstack1lll1lll1l_opy_(bstack1llll1l11_opy_):
    if bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᶴ"), None) and bstack11l11l11_opy_(
      threading.current_thread(), bstack1l1111l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᶵ"), None) and not bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧᶶ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack1l11llll11_opy_(bstack1llll1l11_opy_, name=bstack1l1111l_opy_ (u"ࠧࠨᶷ"), path=bstack1l1111l_opy_ (u"ࠨࠢᶸ"))