# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1l11l1l1l_opy_
from bstack_utils.helper import bstack111ll1l1_opy_
logger = logging.getLogger(__name__)
def bstack1llll1l1l_opy_(bstack11l11ll1_opy_):
  return True if bstack11l11ll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1llllll1l_opy_(context, *args):
    tags = getattr(args[0], bstack11l1ll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᢗ"), [])
    bstack1l11l1ll_opy_ = bstack1l11l1l1l_opy_.bstack1lll1l1lll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l11l1ll_opy_
    try:
      bstack1ll111ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll1l1l_opy_(bstack11l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᢘ")) else context.browser
      if bstack1ll111ll11_opy_ and bstack1ll111ll11_opy_.session_id and bstack1l11l1ll_opy_ and bstack111ll1l1_opy_(
              threading.current_thread(), bstack11l1ll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᢙ"), None):
          threading.current_thread().isA11yTest = bstack1l11l1l1l_opy_.bstack1ll1l1ll1l_opy_(bstack1ll111ll11_opy_, bstack1l11l1ll_opy_)
    except Exception as e:
       logger.debug(bstack11l1ll1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬᢚ").format(str(e)))
def bstack11l11l11l1_opy_(bstack1ll111ll11_opy_):
    if bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᢛ"), None) and bstack111ll1l1_opy_(
      threading.current_thread(), bstack11l1ll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᢜ"), None) and not bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫᢝ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l11l1l1l_opy_.bstack11ll1l111_opy_(bstack1ll111ll11_opy_, name=bstack11l1ll1_opy_ (u"ࠤࠥᢞ"), path=bstack11l1ll1_opy_ (u"ࠥࠦᢟ"))