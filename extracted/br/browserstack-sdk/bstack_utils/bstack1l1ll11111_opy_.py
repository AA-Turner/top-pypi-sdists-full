# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack11ll1l11l_opy_
logger = logging.getLogger(__name__)
def bstack1llll11l1l_opy_(bstack1llll1l1l1_opy_):
  return True if bstack1llll1l1l1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l1111111_opy_(context, *args):
    tags = getattr(args[0], bstack11ll11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᶑ"), [])
    bstack111111111l_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack111111111l_opy_
    try:
      bstack111l111lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11l1l_opy_(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᶒ")) else context.browser
      if bstack111l111lll_opy_ and bstack111l111lll_opy_.session_id and bstack111111111l_opy_ and bstack11ll1l11l_opy_(
              threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᶓ"), None):
          caps = bstack111l111lll_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack11ll11_opy_ (u"ࠬࡖ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࠩࡧ࠱࡫࠳࠲ࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠩࠨᶔ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack111l111lll_opy_, bstack111111111l_opy_)
    except Exception as e:
       logger.debug(bstack11ll11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᶕ").format(str(e)))
def bstack1111l11l11_opy_(bstack111l111lll_opy_):
    if bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᶖ"), None) and bstack11ll1l11l_opy_(
      threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᶗ"), None) and not bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᶘ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack1111l1l111_opy_(bstack111l111lll_opy_, name=bstack11ll11_opy_ (u"ࠥࠦᶙ"), path=bstack11ll11_opy_ (u"ࠦࠧᶚ"))