# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1l111ll111_opy_
from bstack_utils.helper import bstack11llll11l1_opy_
logger = logging.getLogger(__name__)
def bstack11l1l111l_opy_(bstack1l1ll1lll_opy_):
  return True if bstack1l1ll1lll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll1ll1ll_opy_(context, *args):
    tags = getattr(args[0], bstack11l1l11_opy_ (u"ࠫࡹࡧࡧࡴࠩᥫ"), [])
    bstack1l1lll11ll_opy_ = bstack1l111ll111_opy_.bstack11ll1lll1l_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1lll11ll_opy_
    try:
      bstack1l1ll1ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l111l_opy_(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᥬ")) else context.browser
      if bstack1l1ll1ll1_opy_ and bstack1l1ll1ll1_opy_.session_id and bstack1l1lll11ll_opy_ and bstack11llll11l1_opy_(
              threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᥭ"), None):
          threading.current_thread().isA11yTest = bstack1l111ll111_opy_.bstack111ll1ll11_opy_(bstack1l1ll1ll1_opy_, bstack1l1lll11ll_opy_)
    except Exception as e:
       logger.debug(bstack11l1l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡤ࠵࠶ࡿࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧ᥮").format(str(e)))
def bstack1l111l11ll_opy_(bstack1l1ll1ll1_opy_):
    if bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ᥯"), None) and bstack11llll11l1_opy_(
      threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᥰ"), None) and not bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡠࡵࡷࡳࡵ࠭ᥱ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l111ll111_opy_.bstack1l111ll1l1_opy_(bstack1l1ll1ll1_opy_, name=bstack11l1l11_opy_ (u"ࠦࠧᥲ"), path=bstack11l1l11_opy_ (u"ࠧࠨᥳ"))