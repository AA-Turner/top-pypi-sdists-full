# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
import threading
from bstack_utils.helper import bstack11l1l111ll_opy_
from bstack_utils.constants import bstack11l1lll1l11_opy_, EVENTS, STAGE
from bstack_utils.bstack11l1l1l111_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l1111l1_opy_:
    bstack111111llll1_opy_ = None
    @classmethod
    def bstack111l1ll1_opy_(cls):
        if cls.on() and os.getenv(bstack11ll1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨℐ")):
            logger.info(
                bstack11ll1l1_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬℑ").format(os.getenv(bstack11ll1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣℒ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨℓ"), None) is None or os.environ[bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ℔")] == bstack11ll1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦℕ"):
            return False
        return True
    @classmethod
    def bstack1lllll1111ll_opy_(cls, bs_config, framework=bstack11ll1l1_opy_ (u"ࠢࠣ№")):
        bstack11ll111l1ll_opy_ = False
        for fw in bstack11l1lll1l11_opy_:
            if fw in framework:
                bstack11ll111l1ll_opy_ = True
        return bstack11l1l111ll_opy_(bs_config.get(bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ℗"), bstack11ll111l1ll_opy_))
    @classmethod
    def bstack1llll1llll11_opy_(cls, framework):
        return framework in bstack11l1lll1l11_opy_
    @classmethod
    def bstack1lllll1l1111_opy_(cls, bs_config, framework):
        return cls.bstack1lllll1111ll_opy_(bs_config, framework) is True and cls.bstack1llll1llll11_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭℘"), None)
    @staticmethod
    def bstack111llll111_opy_():
        if getattr(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧℙ"), None):
            return {
                bstack11ll1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩℚ"): bstack11ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪℛ"),
                bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ℜ"): getattr(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫℝ"), None)
            }
        if getattr(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ℞"), None):
            return {
                bstack11ll1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ℟"): bstack11ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ℠"),
                bstack11ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ℡"): getattr(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ™"), None)
            }
        return None
    @staticmethod
    def bstack1llll1llllll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1111l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1111lllll1_opy_(test, hook_name=None):
        bstack1llll1lllll1_opy_ = test.parent
        if hook_name in [bstack11ll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ℣"), bstack11ll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨℤ"), bstack11ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ℥"), bstack11ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫΩ")]:
            bstack1llll1lllll1_opy_ = test
        scope = []
        while bstack1llll1lllll1_opy_ is not None:
            scope.append(bstack1llll1lllll1_opy_.name)
            bstack1llll1lllll1_opy_ = bstack1llll1lllll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll1lll1ll_opy_(hook_type):
        if hook_type == bstack11ll1l1_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣ℧"):
            return bstack11ll1l1_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣℨ")
        elif hook_type == bstack11ll1l1_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤ℩"):
            return bstack11ll1l1_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨK")
    @staticmethod
    def bstack1llll1llll1l_opy_(bstack1lllll1ll1_opy_):
        try:
            if not bstack1l1111l1_opy_.on():
                return bstack1lllll1ll1_opy_
            if os.environ.get(bstack11ll1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧÅ"), None) == bstack11ll1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨℬ"):
                tests = os.environ.get(bstack11ll1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨℭ"), None)
                if tests is None or tests == bstack11ll1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ℮"):
                    return bstack1lllll1ll1_opy_
                bstack1lllll1ll1_opy_ = tests.split(bstack11ll1l1_opy_ (u"ࠫ࠱࠭ℯ"))
                return bstack1lllll1ll1_opy_
        except Exception as exc:
            logger.debug(bstack11ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨℰ") + str(str(exc)) + bstack11ll1l1_opy_ (u"ࠨࠢℱ"))
        return bstack1lllll1ll1_opy_