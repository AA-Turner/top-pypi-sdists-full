# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
import threading
from bstack_utils.helper import bstack11l1l1ll_opy_
from bstack_utils.constants import bstack11ll1l11111_opy_, EVENTS, STAGE
from bstack_utils.bstack1llllll1ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1ll1l111l1_opy_:
    bstack111l11ll11l_opy_ = None
    @classmethod
    def bstack111llll1_opy_(cls):
        if cls.on() and os.getenv(bstack1llllll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤὅ")):
            logger.info(
                bstack1llllll_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨ὆").format(os.getenv(bstack1llllll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ὇"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫὈ"), None) is None or os.environ[bstack1llllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬὉ")] == bstack1llllll_opy_ (u"ࠤࡱࡹࡱࡲࠢὊ"):
            return False
        return True
    @classmethod
    def bstack1111l1l1ll1_opy_(cls, bs_config, framework=bstack1llllll_opy_ (u"ࠥࠦὋ")):
        bstack11lll111l11_opy_ = False
        for fw in bstack11ll1l11111_opy_:
            if fw in framework:
                bstack11lll111l11_opy_ = True
        return bstack11l1l1ll_opy_(bs_config.get(bstack1llllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨὌ"), bstack11lll111l11_opy_))
    @classmethod
    def bstack1111l11l1ll_opy_(cls, framework):
        return framework in bstack11ll1l11111_opy_
    @classmethod
    def bstack1111ll1111l_opy_(cls, bs_config, framework):
        return cls.bstack1111l1l1ll1_opy_(bs_config, framework) is True and cls.bstack1111l11l1ll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1llllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩὍ"), None)
    @staticmethod
    def bstack111llll111_opy_():
        if getattr(threading.current_thread(), bstack1llllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ὎"), None):
            return {
                bstack1llllll_opy_ (u"ࠧࡵࡻࡳࡩࠬ὏"): bstack1llllll_opy_ (u"ࠨࡶࡨࡷࡹ࠭ὐ"),
                bstack1llllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩὑ"): getattr(threading.current_thread(), bstack1llllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧὒ"), None)
            }
        if getattr(threading.current_thread(), bstack1llllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨὓ"), None):
            return {
                bstack1llllll_opy_ (u"ࠬࡺࡹࡱࡧࠪὔ"): bstack1llllll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫὕ"),
                bstack1llllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧὖ"): getattr(threading.current_thread(), bstack1llllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬὗ"), None)
            }
        return None
    @staticmethod
    def bstack1111l11l1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1l111l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l11ll11_opy_(test, hook_name=None):
        bstack1111l11ll11_opy_ = test.parent
        if hook_name in [bstack1llllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ὘"), bstack1llllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫὙ"), bstack1llllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ὚"), bstack1llllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧὛ")]:
            bstack1111l11ll11_opy_ = test
        scope = []
        while bstack1111l11ll11_opy_ is not None:
            scope.append(bstack1111l11ll11_opy_.name)
            bstack1111l11ll11_opy_ = bstack1111l11ll11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l11ll1l_opy_(hook_type):
        if hook_type == bstack1llllll_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦ὜"):
            return bstack1llllll_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦὝ")
        elif hook_type == bstack1llllll_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧ὞"):
            return bstack1llllll_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤὟ")
    @staticmethod
    def bstack1111l11lll1_opy_(bstack1llll11ll1_opy_):
        try:
            if not bstack1ll1l111l1_opy_.on():
                return bstack1llll11ll1_opy_
            if os.environ.get(bstack1llllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣὠ"), None) == bstack1llllll_opy_ (u"ࠦࡹࡸࡵࡦࠤὡ"):
                tests = os.environ.get(bstack1llllll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤὢ"), None)
                if tests is None or tests == bstack1llllll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦὣ"):
                    return bstack1llll11ll1_opy_
                bstack1llll11ll1_opy_ = tests.split(bstack1llllll_opy_ (u"ࠧ࠭ࠩὤ"))
                return bstack1llll11ll1_opy_
        except Exception as exc:
            logger.debug(bstack1llllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤὥ") + str(str(exc)) + bstack1llllll_opy_ (u"ࠤࠥὦ"))
        return bstack1llll11ll1_opy_