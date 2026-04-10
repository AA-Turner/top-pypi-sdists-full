# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack1llll1lll_opy_
logger = logging.getLogger(__name__)
def bstack11ll11111_opy_(bstack111l1111l_opy_):
  return True if bstack111l1111l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll1llll11_opy_(context, *args):
    tags = getattr(args[0], bstack1ll_opy_ (u"ࠬࡺࡡࡨࡵࠪᶔ"), [])
    bstack11l1111ll1_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack11l1111ll1_opy_
    try:
      bstack11lll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11111_opy_(bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᶕ")) else context.browser
      if bstack11lll111_opy_ and bstack11lll111_opy_.session_id and bstack11l1111ll1_opy_ and bstack1llll1lll_opy_(
              threading.current_thread(), bstack1ll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᶖ"), None):
          caps = bstack11lll111_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1ll_opy_ (u"ࠨࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࠬࡪ࠴ࡧ࠯࠮ࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠬࠫᶗ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack11lll111_opy_, bstack11l1111ll1_opy_)
    except Exception as e:
       logger.debug(bstack1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩᶘ").format(str(e)))
def bstack11111lllll_opy_(bstack11lll111_opy_):
    if bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᶙ"), None) and bstack1llll1lll_opy_(
      threading.current_thread(), bstack1ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᶚ"), None) and not bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨᶛ"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack1111l111_opy_(bstack11lll111_opy_, name=bstack1ll_opy_ (u"ࠨࠢᶜ"), path=bstack1ll_opy_ (u"ࠢࠣᶝ"))