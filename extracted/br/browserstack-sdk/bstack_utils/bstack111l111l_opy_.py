# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import threading
from bstack_utils.helper import bstack1lll1111ll_opy_
from bstack_utils.constants import bstack111l1l1111l_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11l11l1lll_opy_:
    bstack1ll1lllll1ll_opy_ = None
    @classmethod
    def bstack11llll1111_opy_(cls):
        if cls.on() and os.getenv(bstack1ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ⛪")):
            logger.info(
                bstack1ll11_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩ⛫").format(os.getenv(bstack1ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⛬"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⛭"), None) is None or os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⛮")] == bstack1ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⛯"):
            return False
        return True
    @classmethod
    def bstack1ll1l1l111l1_opy_(cls, bs_config, framework=bstack1ll11_opy_ (u"ࠢࠣ⛰")):
        bstack111l1l111l1_opy_ = False
        for fw in bstack111l1l1111l_opy_:
            if fw in framework:
                bstack111l1l111l1_opy_ = True
        return bstack1lll1111ll_opy_(bs_config.get(bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⛱"), bstack111l1l111l1_opy_))
    @classmethod
    def bstack1ll1l11l1lll_opy_(cls, framework):
        return framework in bstack111l1l1111l_opy_
    @classmethod
    def bstack1ll1l1ll11ll_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l1l111l1_opy_(bs_config, framework) is True and cls.bstack1ll1l11l1lll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⛲"), None)
    @staticmethod
    def bstack1lllll11ll1_opy_():
        if getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⛳"), None):
            return {
                bstack1ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩ⛴"): bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࠪ⛵"),
                bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⛶"): getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⛷"), None)
            }
        if getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⛸"), None):
            return {
                bstack1ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⛹"): bstack1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⛺"),
                bstack1ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⛻"): getattr(threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⛼"), None)
            }
        return None
    @staticmethod
    def bstack1ll1l11l1l1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l11l1lll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lll1l1ll11_opy_(test, hook_name=None):
        bstack1ll1l11l1ll1_opy_ = test.parent
        if hook_name in [bstack1ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⛽"), bstack1ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⛾"), bstack1ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⛿"), bstack1ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ✀")]:
            bstack1ll1l11l1ll1_opy_ = test
        scope = []
        while bstack1ll1l11l1ll1_opy_ is not None:
            scope.append(bstack1ll1l11l1ll1_opy_.name)
            bstack1ll1l11l1ll1_opy_ = bstack1ll1l11l1ll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1l11ll11l_opy_(hook_type):
        if hook_type == bstack1ll11_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣ✁"):
            return bstack1ll11_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣ✂")
        elif hook_type == bstack1ll11_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤ✃"):
            return bstack1ll11_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨ✄")
    @staticmethod
    def bstack1ll1l11ll111_opy_(bstack1l1ll1l1_opy_):
        try:
            if not bstack11l11l1lll_opy_.on():
                return bstack1l1ll1l1_opy_
            if os.environ.get(bstack1ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧ✅"), None) == bstack1ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨ✆"):
                tests = os.environ.get(bstack1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨ✇"), None)
                if tests is None or tests == bstack1ll11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ✈"):
                    return bstack1l1ll1l1_opy_
                bstack1l1ll1l1_opy_ = tests.split(bstack1ll11_opy_ (u"ࠫ࠱࠭✉"))
                return bstack1l1ll1l1_opy_
        except Exception as exc:
            logger.debug(bstack1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨ✊") + str(str(exc)) + bstack1ll11_opy_ (u"ࠨࠢ✋"))
        return bstack1l1ll1l1_opy_