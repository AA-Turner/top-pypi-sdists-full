# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11l1111111_opy_
from bstack_utils.helper import bstack1lll11lll1_opy_
logger = logging.getLogger(__name__)
def bstack1l111l111l_opy_(bstack111lllllll_opy_):
  return True if bstack111lllllll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11ll1lll_opy_(context, *args):
    tags = getattr(args[0], bstack1111_opy_ (u"࠭ࡴࡢࡩࡶࠫ᪓"), [])
    bstack11l1ll1l_opy_ = bstack11l1111111_opy_.bstack111l1lll1_opy_(tags)
    threading.current_thread().isA11yTest = bstack11l1ll1l_opy_
    try:
      bstack1lll1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l111l_opy_(bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭᪔")) else context.browser
      if bstack1lll1ll11l_opy_ and bstack1lll1ll11l_opy_.session_id and bstack11l1ll1l_opy_ and bstack1lll11lll1_opy_(
              threading.current_thread(), bstack1111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᪕"), None):
          threading.current_thread().isA11yTest = bstack11l1111111_opy_.bstack11ll1llll1_opy_(bstack1lll1ll11l_opy_, bstack11l1ll1l_opy_)
    except Exception as e:
       logger.debug(bstack1111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩ᪖").format(str(e)))
def bstack1l1lll1l_opy_(bstack1lll1ll11l_opy_):
    if bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ᪗"), None) and bstack1lll11lll1_opy_(
      threading.current_thread(), bstack1111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᪘"), None) and not bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨ᪙"), False):
      threading.current_thread().a11y_stop = True
      bstack11l1111111_opy_.bstack1ll1ll1l11_opy_(bstack1lll1ll11l_opy_, name=bstack1111_opy_ (u"ࠨࠢ᪚"), path=bstack1111_opy_ (u"ࠢࠣ᪛"))