# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11ll1l1ll1_opy_
from bstack_utils.helper import bstack11l11l1ll1_opy_
logger = logging.getLogger(__name__)
def bstack1l1ll1ll_opy_(bstack1l1ll111l_opy_):
  return True if bstack1l1ll111l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1lll111l1_opy_(context, *args):
    tags = getattr(args[0], bstack1l11lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᙚ"), [])
    bstack1l11l11lll_opy_ = bstack11ll1l1ll1_opy_.bstack111ll1l1l_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l11l11lll_opy_
    try:
      bstack1ll1l11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1ll_opy_(bstack1l11lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᙛ")) else context.browser
      if bstack1ll1l11lll_opy_ and bstack1ll1l11lll_opy_.session_id and bstack1l11l11lll_opy_ and bstack11l11l1ll1_opy_(
              threading.current_thread(), bstack1l11lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᙜ"), None):
          threading.current_thread().isA11yTest = bstack11ll1l1ll1_opy_.bstack1lll1l11l1_opy_(bstack1ll1l11lll_opy_, bstack1l11l11lll_opy_)
    except Exception as e:
       logger.debug(bstack1l11lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᙝ").format(str(e)))
def bstack11l1ll11l1_opy_(bstack1ll1l11lll_opy_):
    if bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᙞ"), None) and bstack11l11l1ll1_opy_(
      threading.current_thread(), bstack1l11lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᙟ"), None) and not bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᙠ"), False):
      threading.current_thread().a11y_stop = True
      bstack11ll1l1ll1_opy_.bstack1l111l11l1_opy_(bstack1ll1l11lll_opy_, name=bstack1l11lll_opy_ (u"ࠥࠦᙡ"), path=bstack1l11lll_opy_ (u"ࠦࠧᙢ"))