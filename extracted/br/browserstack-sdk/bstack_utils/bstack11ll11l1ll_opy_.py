# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack111lll1ll1_opy_
logger = logging.getLogger(__name__)
def bstack11l1111l_opy_(bstack1111l1l11_opy_):
  return True if bstack1111l1l11_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l1lllll1_opy_(context, *args):
    tags = getattr(args[0], bstack111ll11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᶭ"), [])
    bstack111l11111_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack111l11111_opy_
    try:
      bstack11l1l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1111l_opy_(bstack111ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᶮ")) else context.browser
      if bstack11l1l1llll_opy_ and bstack11l1l1llll_opy_.session_id and bstack111l11111_opy_ and bstack111lll1ll1_opy_(
              threading.current_thread(), bstack111ll11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᶯ"), None):
          caps = bstack11l1l1llll_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack111ll11_opy_ (u"ࠬࡖ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࠩࡧ࠱࡫࠳࠲ࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠩࠨᶰ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack11l1l1llll_opy_, bstack111l11111_opy_)
    except Exception as e:
       logger.debug(bstack111ll11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᶱ").format(str(e)))
def bstack1l1111l1ll_opy_(bstack11l1l1llll_opy_):
    if bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᶲ"), None) and bstack111lll1ll1_opy_(
      threading.current_thread(), bstack111ll11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᶳ"), None) and not bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᶴ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack11111llll1_opy_(bstack11l1l1llll_opy_, name=bstack111ll11_opy_ (u"ࠥࠦᶵ"), path=bstack111ll11_opy_ (u"ࠦࠧᶶ"))