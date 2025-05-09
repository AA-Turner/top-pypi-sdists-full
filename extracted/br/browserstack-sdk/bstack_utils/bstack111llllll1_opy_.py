# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import os
import threading
from bstack_utils.helper import bstack1l11lll11l_opy_
from bstack_utils.constants import bstack11ll1l1ll11_opy_, EVENTS, STAGE
from bstack_utils.bstack1l11lll1_opy_ import get_logger
logger = get_logger(__name__)
class bstack1llll1ll1l_opy_:
    bstack111l11ll1l1_opy_ = None
    @classmethod
    def bstack111l1ll11_opy_(cls):
        if cls.on() and os.getenv(bstack11lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ὎")):
            logger.info(
                bstack11lll_opy_ (u"ࠧࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠪ὏").format(os.getenv(bstack11lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨὐ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ὑ"), None) is None or os.environ[bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧὒ")] == bstack11lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤὓ"):
            return False
        return True
    @classmethod
    def bstack1111l1l1l1l_opy_(cls, bs_config, framework=bstack11lll_opy_ (u"ࠧࠨὔ")):
        bstack11lll11111l_opy_ = False
        for fw in bstack11ll1l1ll11_opy_:
            if fw in framework:
                bstack11lll11111l_opy_ = True
        return bstack1l11lll11l_opy_(bs_config.get(bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪὕ"), bstack11lll11111l_opy_))
    @classmethod
    def bstack1111l11l1l1_opy_(cls, framework):
        return framework in bstack11ll1l1ll11_opy_
    @classmethod
    def bstack1111ll1111l_opy_(cls, bs_config, framework):
        return cls.bstack1111l1l1l1l_opy_(bs_config, framework) is True and cls.bstack1111l11l1l1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫὖ"), None)
    @staticmethod
    def bstack11l111l11l_opy_():
        if getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬὗ"), None):
            return {
                bstack11lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ὘"): bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࠨὙ"),
                bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ὚"): getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩὛ"), None)
            }
        if getattr(threading.current_thread(), bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ὜"), None):
            return {
                bstack11lll_opy_ (u"ࠧࡵࡻࡳࡩࠬὝ"): bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭὞"),
                bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩὟ"): getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧὠ"), None)
            }
        return None
    @staticmethod
    def bstack1111l11l11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1llll1ll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l1l11l1_opy_(test, hook_name=None):
        bstack1111l11l1ll_opy_ = test.parent
        if hook_name in [bstack11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩὡ"), bstack11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ὢ"), bstack11lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬὣ"), bstack11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩὤ")]:
            bstack1111l11l1ll_opy_ = test
        scope = []
        while bstack1111l11l1ll_opy_ is not None:
            scope.append(bstack1111l11l1ll_opy_.name)
            bstack1111l11l1ll_opy_ = bstack1111l11l1ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l11ll11_opy_(hook_type):
        if hook_type == bstack11lll_opy_ (u"ࠣࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍࠨὥ"):
            return bstack11lll_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡪࡲࡳࡰࠨὦ")
        elif hook_type == bstack11lll_opy_ (u"ࠥࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠢὧ"):
            return bstack11lll_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡨࡰࡱ࡮ࠦὨ")
    @staticmethod
    def bstack1111l11l111_opy_(bstack11llll1l1_opy_):
        try:
            if not bstack1llll1ll1l_opy_.on():
                return bstack11llll1l1_opy_
            if os.environ.get(bstack11lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠥὩ"), None) == bstack11lll_opy_ (u"ࠨࡴࡳࡷࡨࠦὪ"):
                tests = os.environ.get(bstack11lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠦὫ"), None)
                if tests is None or tests == bstack11lll_opy_ (u"ࠣࡰࡸࡰࡱࠨὬ"):
                    return bstack11llll1l1_opy_
                bstack11llll1l1_opy_ = tests.split(bstack11lll_opy_ (u"ࠩ࠯ࠫὭ"))
                return bstack11llll1l1_opy_
        except Exception as exc:
            logger.debug(bstack11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡩࡷࡻ࡮ࠡࡪࡤࡲࡩࡲࡥࡳ࠼ࠣࠦὮ") + str(str(exc)) + bstack11lll_opy_ (u"ࠦࠧὯ"))
        return bstack11llll1l1_opy_