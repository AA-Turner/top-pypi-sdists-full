# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11l1llll11_opy_
from bstack_utils.helper import bstack1l1ll1ll1_opy_
logger = logging.getLogger(__name__)
def bstack1lllll11_opy_(bstack1l11ll111l_opy_):
  return True if bstack1l11ll111l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l1l111_opy_(context, *args):
    tags = getattr(args[0], bstack11lllll_opy_ (u"࠭ࡴࡢࡩࡶࠫᢷ"), [])
    bstack11ll1l1l_opy_ = bstack11l1llll11_opy_.bstack1l11lll111_opy_(tags)
    threading.current_thread().isA11yTest = bstack11ll1l1l_opy_
    try:
      bstack111lll11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllll11_opy_(bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ᢸ")) else context.browser
      if bstack111lll11ll_opy_ and bstack111lll11ll_opy_.session_id and bstack11ll1l1l_opy_ and bstack1l1ll1ll1_opy_(
              threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᢹ"), None):
          threading.current_thread().isA11yTest = bstack11l1llll11_opy_.bstack1ll11l1l11_opy_(bstack111lll11ll_opy_, bstack11ll1l1l_opy_)
    except Exception as e:
       logger.debug(bstack11lllll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩᢺ").format(str(e)))
def bstack1l1l11l1l_opy_(bstack111lll11ll_opy_):
    if bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᢻ"), None) and bstack1l1ll1ll1_opy_(
      threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᢼ"), None) and not bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨᢽ"), False):
      threading.current_thread().a11y_stop = True
      bstack11l1llll11_opy_.bstack1111ll1ll_opy_(bstack111lll11ll_opy_, name=bstack11lllll_opy_ (u"ࠨࠢᢾ"), path=bstack11lllll_opy_ (u"ࠢࠣᢿ"))