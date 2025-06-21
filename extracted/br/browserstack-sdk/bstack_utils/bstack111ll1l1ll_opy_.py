# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
import threading
from bstack_utils.helper import bstack1lll1l1lll_opy_
from bstack_utils.constants import bstack11l1lll1l11_opy_, EVENTS, STAGE
from bstack_utils.bstack1llll1l111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1l1l1ll_opy_:
    bstack11111l11111_opy_ = None
    @classmethod
    def bstack1lll11l11_opy_(cls):
        if cls.on() and os.getenv(bstack1l1l1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⃰")):
            logger.info(
                bstack1l1l1l1_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨ⃱").format(os.getenv(bstack1l1l1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⃲"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⃳"), None) is None or os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⃴")] == bstack1l1l1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢ⃵"):
            return False
        return True
    @classmethod
    def bstack1lllll11l1l1_opy_(cls, bs_config, framework=bstack1l1l1l1_opy_ (u"ࠥࠦ⃶")):
        bstack11ll11l11ll_opy_ = False
        for fw in bstack11l1lll1l11_opy_:
            if fw in framework:
                bstack11ll11l11ll_opy_ = True
        return bstack1lll1l1lll_opy_(bs_config.get(bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⃷"), bstack11ll11l11ll_opy_))
    @classmethod
    def bstack1lllll111l11_opy_(cls, framework):
        return framework in bstack11l1lll1l11_opy_
    @classmethod
    def bstack1llllll1l1l1_opy_(cls, bs_config, framework):
        return cls.bstack1lllll11l1l1_opy_(bs_config, framework) is True and cls.bstack1lllll111l11_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⃸"), None)
    @staticmethod
    def bstack111ll1l11l_opy_():
        if getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⃹"), None):
            return {
                bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ⃺"): bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭⃻"),
                bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⃼"): getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⃽"), None)
            }
        if getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⃾"), None):
            return {
                bstack1l1l1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ⃿"): bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ℀"),
                bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ℁"): getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬℂ"), None)
            }
        return None
    @staticmethod
    def bstack1lllll1111ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1l1l1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1111llllll_opy_(test, hook_name=None):
        bstack1lllll1111l1_opy_ = test.parent
        if hook_name in [bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ℃"), bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ℄"), bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ℅"), bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ℆")]:
            bstack1lllll1111l1_opy_ = test
        scope = []
        while bstack1lllll1111l1_opy_ is not None:
            scope.append(bstack1lllll1111l1_opy_.name)
            bstack1lllll1111l1_opy_ = bstack1lllll1111l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lllll111l1l_opy_(hook_type):
        if hook_type == bstack1l1l1l1_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦℇ"):
            return bstack1l1l1l1_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦ℈")
        elif hook_type == bstack1l1l1l1_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧ℉"):
            return bstack1l1l1l1_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤℊ")
    @staticmethod
    def bstack1lllll11111l_opy_(bstack1l1ll1l1l1_opy_):
        try:
            if not bstack11l1l1l1ll_opy_.on():
                return bstack1l1ll1l1l1_opy_
            if os.environ.get(bstack1l1l1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣℋ"), None) == bstack1l1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤℌ"):
                tests = os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤℍ"), None)
                if tests is None or tests == bstack1l1l1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦℎ"):
                    return bstack1l1ll1l1l1_opy_
                bstack1l1ll1l1l1_opy_ = tests.split(bstack1l1l1l1_opy_ (u"ࠧ࠭ࠩℏ"))
                return bstack1l1ll1l1l1_opy_
        except Exception as exc:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤℐ") + str(str(exc)) + bstack1l1l1l1_opy_ (u"ࠤࠥℑ"))
        return bstack1l1ll1l1l1_opy_