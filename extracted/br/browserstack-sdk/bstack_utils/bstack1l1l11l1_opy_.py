# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import threading
from bstack_utils.helper import bstack11l1l1l11l_opy_
from bstack_utils.constants import bstack111111ll1l1_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111l111ll1_opy_:
    bstack1ll1l111ll11_opy_ = None
    @classmethod
    def bstack1l1lllll1l_opy_(cls):
        if cls.on() and os.getenv(bstack1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⣇")):
            logger.info(
                bstack1ll_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠪ⣈").format(os.getenv(bstack1ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⣉"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⣊"), None) is None or os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⣋")] == bstack1ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⣌"):
            return False
        return True
    @classmethod
    def bstack1ll111l1ll1l_opy_(cls, bs_config, framework=bstack1ll_opy_ (u"ࠣࠤ⣍")):
        bstack11111ll1lll_opy_ = False
        for fw in bstack111111ll1l1_opy_:
            if fw in framework:
                bstack11111ll1lll_opy_ = True
        return bstack11l1l1l11l_opy_(bs_config.get(bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⣎"), bstack11111ll1lll_opy_))
    @classmethod
    def bstack1ll111l1l1l1_opy_(cls, framework):
        return framework in bstack111111ll1l1_opy_
    @classmethod
    def bstack1ll111lllll1_opy_(cls, bs_config, framework):
        return cls.bstack1ll111l1ll1l_opy_(bs_config, framework) is True and cls.bstack1ll111l1l1l1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⣏"), None)
    @staticmethod
    def bstack1llll11ll11_opy_():
        if getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⣐"), None):
            return {
                bstack1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ⣑"): bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࠫ⣒"),
                bstack1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⣓"): getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⣔"), None)
            }
        if getattr(threading.current_thread(), bstack1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⣕"), None):
            return {
                bstack1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨ⣖"): bstack1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⣗"),
                bstack1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⣘"): getattr(threading.current_thread(), bstack1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⣙"), None)
            }
        return None
    @staticmethod
    def bstack1ll111l1l1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111l111ll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lll11ll111_opy_(test, hook_name=None):
        bstack1ll111l1l111_opy_ = test.parent
        if hook_name in [bstack1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⣚"), bstack1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⣛"), bstack1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⣜"), bstack1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⣝")]:
            bstack1ll111l1l111_opy_ = test
        scope = []
        while bstack1ll111l1l111_opy_ is not None:
            scope.append(bstack1ll111l1l111_opy_.name)
            bstack1ll111l1l111_opy_ = bstack1ll111l1l111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll111l1ll11_opy_(hook_type):
        if hook_type == bstack1ll_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤ⣞"):
            return bstack1ll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤ⣟")
        elif hook_type == bstack1ll_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥ⣠"):
            return bstack1ll_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢ⣡")
    @staticmethod
    def bstack1ll111l1l11l_opy_(bstack11ll111l1l_opy_):
        try:
            if not bstack111l111ll1_opy_.on():
                return bstack11ll111l1l_opy_
            if os.environ.get(bstack1ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨ⣢"), None) == bstack1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ⣣"):
                tests = os.environ.get(bstack1ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢ⣤"), None)
                if tests is None or tests == bstack1ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⣥"):
                    return bstack11ll111l1l_opy_
                bstack11ll111l1l_opy_ = tests.split(bstack1ll_opy_ (u"ࠬ࠲ࠧ⣦"))
                return bstack11ll111l1l_opy_
        except Exception as exc:
            logger.debug(bstack1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢ⣧") + str(str(exc)) + bstack1ll_opy_ (u"ࠢࠣ⣨"))
        return bstack11ll111l1l_opy_