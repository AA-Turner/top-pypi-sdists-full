# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import threading
from bstack_utils.helper import bstack1ll111llll_opy_
from bstack_utils.constants import bstack111ll111lll_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11l11ll1l1_opy_:
    bstack1lll11l111l1_opy_ = None
    @classmethod
    def bstack11ll11l111_opy_(cls):
        if cls.on() and os.getenv(bstack1111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ♧")):
            logger.info(
                bstack1111l_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫ♨").format(os.getenv(bstack1111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ♩"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ♪"), None) is None or os.environ[bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ♫")] == bstack1111l_opy_ (u"ࠣࡰࡸࡰࡱࠨ♬"):
            return False
        return True
    @classmethod
    def bstack1ll1ll11l1ll_opy_(cls, bs_config, framework=bstack1111l_opy_ (u"ࠤࠥ♭")):
        bstack111ll11l1ll_opy_ = False
        for fw in bstack111ll111lll_opy_:
            if fw in framework:
                bstack111ll11l1ll_opy_ = True
        return bstack1ll111llll_opy_(bs_config.get(bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ♮"), bstack111ll11l1ll_opy_))
    @classmethod
    def bstack1ll1l1llll11_opy_(cls, framework):
        return framework in bstack111ll111lll_opy_
    @classmethod
    def bstack1ll1lll11ll1_opy_(cls, bs_config, framework):
        return cls.bstack1ll1ll11l1ll_opy_(bs_config, framework) is True and cls.bstack1ll1l1llll11_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ♯"), None)
    @staticmethod
    def bstack1111111lll_opy_():
        if getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ♰"), None):
            return {
                bstack1111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ♱"): bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࠬ♲"),
                bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ♳"): getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭♴"), None)
            }
        if getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ♵"), None):
            return {
                bstack1111l_opy_ (u"ࠫࡹࡿࡰࡦࠩ♶"): bstack1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ♷"),
                bstack1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭♸"): getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ♹"), None)
            }
        return None
    @staticmethod
    def bstack1ll1ll111111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l11ll1l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lllll11ll1_opy_(test, hook_name=None):
        bstack1ll1l1llllll_opy_ = test.parent
        if hook_name in [bstack1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭♺"), bstack1111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ♻"), bstack1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ♼"), bstack1111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭♽")]:
            bstack1ll1l1llllll_opy_ = test
        scope = []
        while bstack1ll1l1llllll_opy_ is not None:
            scope.append(bstack1ll1l1llllll_opy_.name)
            bstack1ll1l1llllll_opy_ = bstack1ll1l1llllll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1l1lllll1_opy_(hook_type):
        if hook_type == bstack1111l_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥ♾"):
            return bstack1111l_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥ♿")
        elif hook_type == bstack1111l_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦ⚀"):
            return bstack1111l_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣ⚁")
    @staticmethod
    def bstack1ll1l1llll1l_opy_(bstack1lll1l11_opy_):
        try:
            if not bstack11l11ll1l1_opy_.on():
                return bstack1lll1l11_opy_
            if os.environ.get(bstack1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢ⚂"), None) == bstack1111l_opy_ (u"ࠥࡸࡷࡻࡥࠣ⚃"):
                tests = os.environ.get(bstack1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣ⚄"), None)
                if tests is None or tests == bstack1111l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⚅"):
                    return bstack1lll1l11_opy_
                bstack1lll1l11_opy_ = tests.split(bstack1111l_opy_ (u"࠭ࠬࠨ⚆"))
                return bstack1lll1l11_opy_
        except Exception as exc:
            logger.debug(bstack1111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣ⚇") + str(str(exc)) + bstack1111l_opy_ (u"ࠣࠤ⚈"))
        return bstack1lll1l11_opy_