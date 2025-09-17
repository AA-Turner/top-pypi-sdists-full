# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11lll1ll1l_opy_
from bstack_utils.helper import bstack1l11111ll_opy_
logger = logging.getLogger(__name__)
def bstack1ll1l1ll1_opy_(bstack1111l1ll_opy_):
  return True if bstack1111l1ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11111111l_opy_(context, *args):
    tags = getattr(args[0], bstack1l11ll1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ᝹"), [])
    bstack11llll11l_opy_ = bstack11lll1ll1l_opy_.bstack11l1lllll_opy_(tags)
    threading.current_thread().isA11yTest = bstack11llll11l_opy_
    try:
      bstack1l1l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1ll1_opy_(bstack1l11ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ᝺")) else context.browser
      if bstack1l1l11l11_opy_ and bstack1l1l11l11_opy_.session_id and bstack11llll11l_opy_ and bstack1l11111ll_opy_(
              threading.current_thread(), bstack1l11ll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᝻"), None):
          threading.current_thread().isA11yTest = bstack11lll1ll1l_opy_.bstack1lllll11_opy_(bstack1l1l11l11_opy_, bstack11llll11l_opy_)
    except Exception as e:
       logger.debug(bstack1l11ll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭᝼").format(str(e)))
def bstack1111111l1_opy_(bstack1l1l11l11_opy_):
    if bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ᝽"), None) and bstack1l11111ll_opy_(
      threading.current_thread(), bstack1l11ll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᝾"), None) and not bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬ᝿"), False):
      threading.current_thread().a11y_stop = True
      bstack11lll1ll1l_opy_.bstack1l1ll1111_opy_(bstack1l1l11l11_opy_, name=bstack1l11ll1_opy_ (u"ࠥࠦក"), path=bstack1l11ll1_opy_ (u"ࠦࠧខ"))