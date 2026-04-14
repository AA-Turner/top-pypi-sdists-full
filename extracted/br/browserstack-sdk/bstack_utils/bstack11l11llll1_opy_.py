# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack1l111l11l_opy_
logger = logging.getLogger(__name__)
def bstack1ll1l1l11l_opy_(bstack11ll1ll111_opy_):
  return True if bstack11ll1ll111_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll11llll_opy_(context, *args):
    tags = getattr(args[0], bstack1l111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᶭ"), [])
    bstack1l1ll11111_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack1l1ll11111_opy_
    try:
      bstack11llll111_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1l11l_opy_(bstack1l111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᶮ")) else context.browser
      if bstack11llll111_opy_ and bstack11llll111_opy_.session_id and bstack1l1ll11111_opy_ and bstack1l111l11l_opy_(
              threading.current_thread(), bstack1l111l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᶯ"), None):
          caps = bstack11llll111_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1l111l_opy_ (u"ࠬࡖ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࠩࡧ࠱࡫࠳࠲ࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠩࠨᶰ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack11llll111_opy_, bstack1l1ll11111_opy_)
    except Exception as e:
       logger.debug(bstack1l111l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᶱ").format(str(e)))
def bstack1ll1111111_opy_(bstack11llll111_opy_):
    if bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᶲ"), None) and bstack1l111l11l_opy_(
      threading.current_thread(), bstack1l111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᶳ"), None) and not bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᶴ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack1ll111l1ll_opy_(bstack11llll111_opy_, name=bstack1l111l_opy_ (u"ࠥࠦᶵ"), path=bstack1l111l_opy_ (u"ࠦࠧᶶ"))