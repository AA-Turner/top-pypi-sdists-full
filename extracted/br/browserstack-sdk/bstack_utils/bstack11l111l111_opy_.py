# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
import threading
from bstack_utils.helper import bstack11l11llll1_opy_
from bstack_utils.constants import bstack11ll1lll111_opy_, EVENTS, STAGE
from bstack_utils.bstack1ll1l111l1_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l11ll11ll_opy_:
    bstack111l11l1ll1_opy_ = None
    @classmethod
    def bstack11l11l1ll_opy_(cls):
        if cls.on() and os.getenv(bstack1l1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢὊ")):
            logger.info(
                bstack1l1lll_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭Ὃ").format(os.getenv(bstack1l1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤὌ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩὍ"), None) is None or os.environ[bstack1l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ὎")] == bstack1l1lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ὏"):
            return False
        return True
    @classmethod
    def bstack1111l11llll_opy_(cls, bs_config, framework=bstack1l1lll_opy_ (u"ࠣࠤὐ")):
        bstack11lll111l1l_opy_ = False
        for fw in bstack11ll1lll111_opy_:
            if fw in framework:
                bstack11lll111l1l_opy_ = True
        return bstack11l11llll1_opy_(bs_config.get(bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ὑ"), bstack11lll111l1l_opy_))
    @classmethod
    def bstack1111l11ll1l_opy_(cls, framework):
        return framework in bstack11ll1lll111_opy_
    @classmethod
    def bstack1111lll11l1_opy_(cls, bs_config, framework):
        return cls.bstack1111l11llll_opy_(bs_config, framework) is True and cls.bstack1111l11ll1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧὒ"), None)
    @staticmethod
    def bstack111lllll11_opy_():
        if getattr(threading.current_thread(), bstack1l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨὓ"), None):
            return {
                bstack1l1lll_opy_ (u"ࠬࡺࡹࡱࡧࠪὔ"): bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࠫὕ"),
                bstack1l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧὖ"): getattr(threading.current_thread(), bstack1l1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬὗ"), None)
            }
        if getattr(threading.current_thread(), bstack1l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭὘"), None):
            return {
                bstack1l1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨὙ"): bstack1l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ὚"),
                bstack1l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬὛ"): getattr(threading.current_thread(), bstack1l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ὜"), None)
            }
        return None
    @staticmethod
    def bstack1111l11l1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11ll11ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111lll111l_opy_(test, hook_name=None):
        bstack1111l11lll1_opy_ = test.parent
        if hook_name in [bstack1l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬὝ"), bstack1l1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ὞"), bstack1l1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨὟ"), bstack1l1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬὠ")]:
            bstack1111l11lll1_opy_ = test
        scope = []
        while bstack1111l11lll1_opy_ is not None:
            scope.append(bstack1111l11lll1_opy_.name)
            bstack1111l11lll1_opy_ = bstack1111l11lll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l11ll11_opy_(hook_type):
        if hook_type == bstack1l1lll_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤὡ"):
            return bstack1l1lll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤὢ")
        elif hook_type == bstack1l1lll_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥὣ"):
            return bstack1l1lll_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢὤ")
    @staticmethod
    def bstack1111l11l1ll_opy_(bstack1l11l1ll1l_opy_):
        try:
            if not bstack1l11ll11ll_opy_.on():
                return bstack1l11l1ll1l_opy_
            if os.environ.get(bstack1l1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨὥ"), None) == bstack1l1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢὦ"):
                tests = os.environ.get(bstack1l1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢὧ"), None)
                if tests is None or tests == bstack1l1lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤὨ"):
                    return bstack1l11l1ll1l_opy_
                bstack1l11l1ll1l_opy_ = tests.split(bstack1l1lll_opy_ (u"ࠬ࠲ࠧὩ"))
                return bstack1l11l1ll1l_opy_
        except Exception as exc:
            logger.debug(bstack1l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢὪ") + str(str(exc)) + bstack1l1lll_opy_ (u"ࠢࠣὫ"))
        return bstack1l11l1ll1l_opy_