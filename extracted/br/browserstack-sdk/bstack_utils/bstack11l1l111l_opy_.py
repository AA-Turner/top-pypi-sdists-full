# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1l1l11l1l1_opy_
from bstack_utils.helper import bstack1111l1l11_opy_
logger = logging.getLogger(__name__)
def bstack11llllll1l_opy_(bstack111ll1lll_opy_):
  return True if bstack111ll1lll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1lll111l_opy_(context, *args):
    tags = getattr(args[0], bstack1ll11ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ᝿"), [])
    bstack1111llll1_opy_ = bstack1l1l11l1l1_opy_.bstack1l1l1l11ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1111llll1_opy_
    try:
      bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack11llllll1l_opy_(bstack1ll11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩក")) else context.browser
      if bstack1l1111l11_opy_ and bstack1l1111l11_opy_.session_id and bstack1111llll1_opy_ and bstack1111l1l11_opy_(
              threading.current_thread(), bstack1ll11ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪខ"), None):
          threading.current_thread().isA11yTest = bstack1l1l11l1l1_opy_.bstack111ll1111_opy_(bstack1l1111l11_opy_, bstack1111llll1_opy_)
    except Exception as e:
       logger.debug(bstack1ll11ll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬគ").format(str(e)))
def bstack1l1111111_opy_(bstack1l1111l11_opy_):
    if bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪឃ"), None) and bstack1111l1l11_opy_(
      threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ង"), None) and not bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫច"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1l11l1l1_opy_.bstack1l11ll1l11_opy_(bstack1l1111l11_opy_, name=bstack1ll11ll_opy_ (u"ࠤࠥឆ"), path=bstack1ll11ll_opy_ (u"ࠥࠦជ"))