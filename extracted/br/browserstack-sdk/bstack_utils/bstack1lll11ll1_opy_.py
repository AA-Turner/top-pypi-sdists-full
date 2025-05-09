# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11l1lll11_opy_
from bstack_utils.helper import bstack1llll11ll1_opy_
logger = logging.getLogger(__name__)
def bstack11lll1ll_opy_(bstack11ll111ll1_opy_):
  return True if bstack11ll111ll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l1l1ll_opy_(context, *args):
    tags = getattr(args[0], bstack11lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᙡ"), [])
    bstack11lllllll_opy_ = bstack11l1lll11_opy_.bstack1l11l111l_opy_(tags)
    threading.current_thread().isA11yTest = bstack11lllllll_opy_
    try:
      bstack1l1l11ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll1ll_opy_(bstack11lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᙢ")) else context.browser
      if bstack1l1l11ll1_opy_ and bstack1l1l11ll1_opy_.session_id and bstack11lllllll_opy_ and bstack1llll11ll1_opy_(
              threading.current_thread(), bstack11lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᙣ"), None):
          threading.current_thread().isA11yTest = bstack11l1lll11_opy_.bstack1ll1lll11l_opy_(bstack1l1l11ll1_opy_, bstack11lllllll_opy_)
    except Exception as e:
       logger.debug(bstack11lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᙤ").format(str(e)))
def bstack1111l11l_opy_(bstack1l1l11ll1_opy_):
    if bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᙥ"), None) and bstack1llll11ll1_opy_(
      threading.current_thread(), bstack11lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᙦ"), None) and not bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᙧ"), False):
      threading.current_thread().a11y_stop = True
      bstack11l1lll11_opy_.bstack1lll1l1l1_opy_(bstack1l1l11ll1_opy_, name=bstack11lll_opy_ (u"ࠥࠦᙨ"), path=bstack11lll_opy_ (u"ࠦࠧᙩ"))