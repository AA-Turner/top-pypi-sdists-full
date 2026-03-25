# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
import threading
from bstack_utils.helper import bstack1l11llll_opy_
from bstack_utils.constants import bstack111l111l1ll_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1111l1lll1_opy_:
    bstack1lll11111l11_opy_ = None
    @classmethod
    def bstack11l1l1l11l_opy_(cls):
        if cls.on() and os.getenv(bstack1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⚽")):
            logger.info(
                bstack1l1_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭⚾").format(os.getenv(bstack1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⚿"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⛀"), None) is None or os.environ[bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⛁")] == bstack1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⛂"):
            return False
        return True
    @classmethod
    def bstack1ll1l1l1ll11_opy_(cls, bs_config, framework=bstack1l1_opy_ (u"ࠦࠧ⛃")):
        bstack111l1l1ll11_opy_ = False
        for fw in bstack111l111l1ll_opy_:
            if fw in framework:
                bstack111l1l1ll11_opy_ = True
        return bstack1l11llll_opy_(bs_config.get(bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⛄"), bstack111l1l1ll11_opy_))
    @classmethod
    def bstack1ll1l1l11111_opy_(cls, framework):
        return framework in bstack111l111l1ll_opy_
    @classmethod
    def bstack1ll1ll1111l1_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l1l1ll11_opy_(bs_config, framework) is True and cls.bstack1ll1l1l11111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⛅"), None)
    @staticmethod
    def bstack1lllll1lll1_opy_():
        if getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⛆"), None):
            return {
                bstack1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭⛇"): bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺࠧ⛈"),
                bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⛉"): getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⛊"), None)
            }
        if getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⛋"), None):
            return {
                bstack1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ⛌"): bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⛍"),
                bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⛎"): getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⛏"), None)
            }
        return None
    @staticmethod
    def bstack1ll1l1l1111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1111l1lll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lll1llllll_opy_(test, hook_name=None):
        bstack1ll1l1l111ll_opy_ = test.parent
        if hook_name in [bstack1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⛐"), bstack1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ⛑"), bstack1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⛒"), bstack1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⛓")]:
            bstack1ll1l1l111ll_opy_ = test
        scope = []
        while bstack1ll1l1l111ll_opy_ is not None:
            scope.append(bstack1ll1l1l111ll_opy_.name)
            bstack1ll1l1l111ll_opy_ = bstack1ll1l1l111ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1l1l111l1_opy_(hook_type):
        if hook_type == bstack1l1_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧ⛔"):
            return bstack1l1_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧ⛕")
        elif hook_type == bstack1l1_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨ⛖"):
            return bstack1l1_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥ⛗")
    @staticmethod
    def bstack1ll1l11lllll_opy_(bstack111l11lll1_opy_):
        try:
            if not bstack1111l1lll1_opy_.on():
                return bstack111l11lll1_opy_
            if os.environ.get(bstack1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤ⛘"), None) == bstack1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ⛙"):
                tests = os.environ.get(bstack1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥ⛚"), None)
                if tests is None or tests == bstack1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⛛"):
                    return bstack111l11lll1_opy_
                bstack111l11lll1_opy_ = tests.split(bstack1l1_opy_ (u"ࠨ࠮ࠪ⛜"))
                return bstack111l11lll1_opy_
        except Exception as exc:
            logger.debug(bstack1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥ⛝") + str(str(exc)) + bstack1l1_opy_ (u"ࠥࠦ⛞"))
        return bstack111l11lll1_opy_