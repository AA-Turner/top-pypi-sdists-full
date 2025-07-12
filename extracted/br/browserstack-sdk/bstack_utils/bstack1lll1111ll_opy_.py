# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11llll1l11_opy_
from bstack_utils.helper import bstack11ll1lll_opy_
logger = logging.getLogger(__name__)
def bstack1lll1lll1l_opy_(bstack1l1l11ll_opy_):
  return True if bstack1l1l11ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11111lll1_opy_(context, *args):
    tags = getattr(args[0], bstack11l1111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᠧ"), [])
    bstack11lll11lll_opy_ = bstack11llll1l11_opy_.bstack1lll111l1l_opy_(tags)
    threading.current_thread().isA11yTest = bstack11lll11lll_opy_
    try:
      bstack1ll1111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1lll1l_opy_(bstack11l1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᠨ")) else context.browser
      if bstack1ll1111l1_opy_ and bstack1ll1111l1_opy_.session_id and bstack11lll11lll_opy_ and bstack11ll1lll_opy_(
              threading.current_thread(), bstack11l1111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᠩ"), None):
          threading.current_thread().isA11yTest = bstack11llll1l11_opy_.bstack11l11llll_opy_(bstack1ll1111l1_opy_, bstack11lll11lll_opy_)
    except Exception as e:
       logger.debug(bstack11l1111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬᠪ").format(str(e)))
def bstack1l1l1111ll_opy_(bstack1ll1111l1_opy_):
    if bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᠫ"), None) and bstack11ll1lll_opy_(
      threading.current_thread(), bstack11l1111_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᠬ"), None) and not bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫᠭ"), False):
      threading.current_thread().a11y_stop = True
      bstack11llll1l11_opy_.bstack1lllll1lll_opy_(bstack1ll1111l1_opy_, name=bstack11l1111_opy_ (u"ࠤࠥᠮ"), path=bstack11l1111_opy_ (u"ࠥࠦᠯ"))