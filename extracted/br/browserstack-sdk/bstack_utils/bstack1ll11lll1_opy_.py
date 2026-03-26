# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack1l11lll1_opy_
logger = logging.getLogger(__name__)
def bstack1l11ll1111_opy_(bstack1ll1111ll_opy_):
  return True if bstack1ll1111ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l11l1l1l_opy_(context, *args):
    tags = getattr(args[0], bstack1ll1lll_opy_ (u"ࠫࡹࡧࡧࡴࠩ᮰"), [])
    bstack11111lll11_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack11111lll11_opy_
    try:
      bstack1111lll1ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11ll1111_opy_(bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ᮱")) else context.browser
      if bstack1111lll1ll_opy_ and bstack1111lll1ll_opy_.session_id and bstack11111lll11_opy_ and bstack1l11lll1_opy_(
              threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᮲"), None):
          caps = bstack1111lll1ll_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1ll1lll_opy_ (u"ࠧࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡸࡻࡰࡱࡱࡵࡸࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࠫࡩ࠳࡭࠮࠭ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠫࠪ᮳"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1111lll1ll_opy_, bstack11111lll11_opy_)
    except Exception as e:
       logger.debug(bstack1ll1lll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ᮴").format(str(e)))
def bstack11l1lll1l1_opy_(bstack1111lll1ll_opy_):
    if bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭᮵"), None) and bstack1l11lll1_opy_(
      threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᮶"), None) and not bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧ᮷"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack1111l1ll_opy_(bstack1111lll1ll_opy_, name=bstack1ll1lll_opy_ (u"ࠧࠨ᮸"), path=bstack1ll1lll_opy_ (u"ࠨࠢ᮹"))