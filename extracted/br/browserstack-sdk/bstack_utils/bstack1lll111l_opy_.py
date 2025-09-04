# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1lll1111l1_opy_
from bstack_utils.helper import bstack1l11l1lll_opy_
logger = logging.getLogger(__name__)
def bstack111111l11_opy_(bstack11l11l1ll1_opy_):
  return True if bstack11l11l1ll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1111ll11_opy_(context, *args):
    tags = getattr(args[0], bstack1111l1l_opy_ (u"ࠬࡺࡡࡨࡵࠪ᝻"), [])
    bstack1ll1l111_opy_ = bstack1lll1111l1_opy_.bstack11l111ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll1l111_opy_
    try:
      bstack11l111111_opy_ = threading.current_thread().bstackSessionDriver if bstack111111l11_opy_(bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ᝼")) else context.browser
      if bstack11l111111_opy_ and bstack11l111111_opy_.session_id and bstack1ll1l111_opy_ and bstack1l11l1lll_opy_(
              threading.current_thread(), bstack1111l1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭᝽"), None):
          threading.current_thread().isA11yTest = bstack1lll1111l1_opy_.bstack11l1ll1l1l_opy_(bstack11l111111_opy_, bstack1ll1l111_opy_)
    except Exception as e:
       logger.debug(bstack1111l1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ᝾").format(str(e)))
def bstack1l11l11l11_opy_(bstack11l111111_opy_):
    if bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭᝿"), None) and bstack1l11l1lll_opy_(
      threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩក"), None) and not bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧខ"), False):
      threading.current_thread().a11y_stop = True
      bstack1lll1111l1_opy_.bstack11ll1l11_opy_(bstack11l111111_opy_, name=bstack1111l1l_opy_ (u"ࠧࠨគ"), path=bstack1111l1l_opy_ (u"ࠨࠢឃ"))