# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1lllll111l_opy_
from bstack_utils.helper import bstack11ll11l11_opy_
logger = logging.getLogger(__name__)
def bstack11l1l111ll_opy_(bstack1l111ll1l_opy_):
  return True if bstack1l111ll1l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack111l11ll1_opy_(context, *args):
    tags = getattr(args[0], bstack11l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᥡ"), [])
    bstack1l11l111l_opy_ = bstack1lllll111l_opy_.bstack11l11l1lll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l11l111l_opy_
    try:
      bstack111l11111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l111ll_opy_(bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᥢ")) else context.browser
      if bstack111l11111_opy_ and bstack111l11111_opy_.session_id and bstack1l11l111l_opy_ and bstack11ll11l11_opy_(
              threading.current_thread(), bstack11l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᥣ"), None):
          threading.current_thread().isA11yTest = bstack1lllll111l_opy_.bstack11l1l11ll1_opy_(bstack111l11111_opy_, bstack1l11l111l_opy_)
    except Exception as e:
       logger.debug(bstack11l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫᥤ").format(str(e)))
def bstack1111l1111_opy_(bstack111l11111_opy_):
    if bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᥥ"), None) and bstack11ll11l11_opy_(
      threading.current_thread(), bstack11l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᥦ"), None) and not bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪᥧ"), False):
      threading.current_thread().a11y_stop = True
      bstack1lllll111l_opy_.bstack1ll1l111l1_opy_(bstack111l11111_opy_, name=bstack11l11_opy_ (u"ࠣࠤᥨ"), path=bstack11l11_opy_ (u"ࠤࠥᥩ"))