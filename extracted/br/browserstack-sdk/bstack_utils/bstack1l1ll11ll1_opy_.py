# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.helper import bstack1lll11l1_opy_
logger = logging.getLogger(__name__)
def bstack111ll111l_opy_(bstack1ll1lll1_opy_):
  return True if bstack1ll1lll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l1l1l11_opy_(context, *args):
    tags = getattr(args[0], bstack1llllll_opy_ (u"ࠬࡺࡡࡨࡵࠪᙜ"), [])
    bstack11l11l11l_opy_ = bstack11111l11l_opy_.bstack11l1ll11l_opy_(tags)
    threading.current_thread().isA11yTest = bstack11l11l11l_opy_
    try:
      bstack111l1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll111l_opy_(bstack1llllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᙝ")) else context.browser
      if bstack111l1lll1_opy_ and bstack111l1lll1_opy_.session_id and bstack11l11l11l_opy_ and bstack1lll11l1_opy_(
              threading.current_thread(), bstack1llllll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᙞ"), None):
          threading.current_thread().isA11yTest = bstack11111l11l_opy_.bstack1l1ll1lll1_opy_(bstack111l1lll1_opy_, bstack11l11l11l_opy_)
    except Exception as e:
       logger.debug(bstack1llllll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨᙟ").format(str(e)))
def bstack1ll11l1ll1_opy_(bstack111l1lll1_opy_):
    if bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᙠ"), None) and bstack1lll11l1_opy_(
      threading.current_thread(), bstack1llllll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᙡ"), None) and not bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧᙢ"), False):
      threading.current_thread().a11y_stop = True
      bstack11111l11l_opy_.bstack1l1l1ll111_opy_(bstack111l1lll1_opy_, name=bstack1llllll_opy_ (u"ࠧࠨᙣ"), path=bstack1llllll_opy_ (u"ࠨࠢᙤ"))