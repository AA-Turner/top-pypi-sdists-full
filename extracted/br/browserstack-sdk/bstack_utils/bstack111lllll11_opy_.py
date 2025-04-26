# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
import threading
from bstack_utils.helper import bstack11ll1l1l11_opy_
from bstack_utils.constants import bstack11ll1ll1l1l_opy_, EVENTS, STAGE
from bstack_utils.bstack11111llll_opy_ import get_logger
logger = get_logger(__name__)
class bstack111l1llll_opy_:
    bstack111l11lll11_opy_ = None
    @classmethod
    def bstack11ll1l11l_opy_(cls):
        if cls.on() and os.getenv(bstack1l11lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢὃ")):
            logger.info(
                bstack1l11lll_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭ὄ").format(os.getenv(bstack1l11lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤὅ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ὆"), None) is None or os.environ[bstack1l11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ὇")] == bstack1l11lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧὈ"):
            return False
        return True
    @classmethod
    def bstack1111l11llll_opy_(cls, bs_config, framework=bstack1l11lll_opy_ (u"ࠣࠤὉ")):
        bstack11lll111l11_opy_ = False
        for fw in bstack11ll1ll1l1l_opy_:
            if fw in framework:
                bstack11lll111l11_opy_ = True
        return bstack11ll1l1l11_opy_(bs_config.get(bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ὂ"), bstack11lll111l11_opy_))
    @classmethod
    def bstack1111l11lll1_opy_(cls, framework):
        return framework in bstack11ll1ll1l1l_opy_
    @classmethod
    def bstack1111lll11l1_opy_(cls, bs_config, framework):
        return cls.bstack1111l11llll_opy_(bs_config, framework) is True and cls.bstack1111l11lll1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧὋ"), None)
    @staticmethod
    def bstack111llllll1_opy_():
        if getattr(threading.current_thread(), bstack1l11lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨὌ"), None):
            return {
                bstack1l11lll_opy_ (u"ࠬࡺࡹࡱࡧࠪὍ"): bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࠫ὎"),
                bstack1l11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ὏"): getattr(threading.current_thread(), bstack1l11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬὐ"), None)
            }
        if getattr(threading.current_thread(), bstack1l11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ὑ"), None):
            return {
                bstack1l11lll_opy_ (u"ࠪࡸࡾࡶࡥࠨὒ"): bstack1l11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩὓ"),
                bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬὔ"): getattr(threading.current_thread(), bstack1l11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪὕ"), None)
            }
        return None
    @staticmethod
    def bstack1111l11l1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111l1llll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111ll1ll11_opy_(test, hook_name=None):
        bstack1111l11ll11_opy_ = test.parent
        if hook_name in [bstack1l11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬὖ"), bstack1l11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩὗ"), bstack1l11lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ὘"), bstack1l11lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬὙ")]:
            bstack1111l11ll11_opy_ = test
        scope = []
        while bstack1111l11ll11_opy_ is not None:
            scope.append(bstack1111l11ll11_opy_.name)
            bstack1111l11ll11_opy_ = bstack1111l11ll11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l11ll1l_opy_(hook_type):
        if hook_type == bstack1l11lll_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤ὚"):
            return bstack1l11lll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤὛ")
        elif hook_type == bstack1l11lll_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥ὜"):
            return bstack1l11lll_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢὝ")
    @staticmethod
    def bstack1111l11l1l1_opy_(bstack11l1lllll1_opy_):
        try:
            if not bstack111l1llll_opy_.on():
                return bstack11l1lllll1_opy_
            if os.environ.get(bstack1l11lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨ὞"), None) == bstack1l11lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢὟ"):
                tests = os.environ.get(bstack1l11lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢὠ"), None)
                if tests is None or tests == bstack1l11lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤὡ"):
                    return bstack11l1lllll1_opy_
                bstack11l1lllll1_opy_ = tests.split(bstack1l11lll_opy_ (u"ࠬ࠲ࠧὢ"))
                return bstack11l1lllll1_opy_
        except Exception as exc:
            logger.debug(bstack1l11lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢὣ") + str(str(exc)) + bstack1l11lll_opy_ (u"ࠢࠣὤ"))
        return bstack11l1lllll1_opy_