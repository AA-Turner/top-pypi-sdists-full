# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import threading
from bstack_utils.helper import bstack1ll111ll1_opy_
from bstack_utils.constants import bstack11ll11l11ll_opy_, EVENTS, STAGE
from bstack_utils.bstack1111ll111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1ll111_opy_:
    bstack1111l1l111l_opy_ = None
    @classmethod
    def bstack1111l1ll_opy_(cls):
        if cls.on() and os.getenv(bstack111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ₅")):
            logger.info(
                bstack111lll_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭₆").format(os.getenv(bstack111lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ₇"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ₈"), None) is None or os.environ[bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ₉")] == bstack111lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ₊"):
            return False
        return True
    @classmethod
    def bstack1111111ll1l_opy_(cls, bs_config, framework=bstack111lll_opy_ (u"ࠣࠤ₋")):
        bstack11ll1l11111_opy_ = False
        for fw in bstack11ll11l11ll_opy_:
            if fw in framework:
                bstack11ll1l11111_opy_ = True
        return bstack1ll111ll1_opy_(bs_config.get(bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭₌"), bstack11ll1l11111_opy_))
    @classmethod
    def bstack111111111ll_opy_(cls, framework):
        return framework in bstack11ll11l11ll_opy_
    @classmethod
    def bstack11111l11lll_opy_(cls, bs_config, framework):
        return cls.bstack1111111ll1l_opy_(bs_config, framework) is True and cls.bstack111111111ll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ₍"), None)
    @staticmethod
    def bstack111ll1ll1l_opy_():
        if getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ₎"), None):
            return {
                bstack111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪ₏"): bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࠫₐ"),
                bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧₑ"): getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬₒ"), None)
            }
        if getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ₓ"), None):
            return {
                bstack111lll_opy_ (u"ࠪࡸࡾࡶࡥࠨₔ"): bstack111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩₕ"),
                bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬₖ"): getattr(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪₗ"), None)
            }
        return None
    @staticmethod
    def bstack111111111l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1ll111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1111lllll1_opy_(test, hook_name=None):
        bstack1111111111l_opy_ = test.parent
        if hook_name in [bstack111lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬₘ"), bstack111lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩₙ"), bstack111lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨₚ"), bstack111lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬₛ")]:
            bstack1111111111l_opy_ = test
        scope = []
        while bstack1111111111l_opy_ is not None:
            scope.append(bstack1111111111l_opy_.name)
            bstack1111111111l_opy_ = bstack1111111111l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack11111111l11_opy_(hook_type):
        if hook_type == bstack111lll_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤₜ"):
            return bstack111lll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤ₝")
        elif hook_type == bstack111lll_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥ₞"):
            return bstack111lll_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢ₟")
    @staticmethod
    def bstack11111111111_opy_(bstack11l11l1l_opy_):
        try:
            if not bstack11l1ll111_opy_.on():
                return bstack11l11l1l_opy_
            if os.environ.get(bstack111lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨ₠"), None) == bstack111lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ₡"):
                tests = os.environ.get(bstack111lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢ₢"), None)
                if tests is None or tests == bstack111lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ₣"):
                    return bstack11l11l1l_opy_
                bstack11l11l1l_opy_ = tests.split(bstack111lll_opy_ (u"ࠬ࠲ࠧ₤"))
                return bstack11l11l1l_opy_
        except Exception as exc:
            logger.debug(bstack111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢ₥") + str(str(exc)) + bstack111lll_opy_ (u"ࠢࠣ₦"))
        return bstack11l11l1l_opy_