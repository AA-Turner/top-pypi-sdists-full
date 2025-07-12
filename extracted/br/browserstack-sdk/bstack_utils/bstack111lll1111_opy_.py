# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import threading
from bstack_utils.helper import bstack11l1l1ll_opy_
from bstack_utils.constants import bstack11lll1111ll_opy_, EVENTS, STAGE
from bstack_utils.bstack1l11l1l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l1ll111ll_opy_:
    bstack111111ll1ll_opy_ = None
    @classmethod
    def bstack1l11llll1l_opy_(cls):
        if cls.on() and os.getenv(bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⅒")):
            logger.info(
                bstack11l1111_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨ⅓").format(os.getenv(bstack11l1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⅔"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⅕"), None) is None or os.environ[bstack11l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⅖")] == bstack11l1111_opy_ (u"ࠤࡱࡹࡱࡲࠢ⅗"):
            return False
        return True
    @classmethod
    def bstack1lllll111111_opy_(cls, bs_config, framework=bstack11l1111_opy_ (u"ࠥࠦ⅘")):
        bstack11ll1lllll1_opy_ = False
        for fw in bstack11lll1111ll_opy_:
            if fw in framework:
                bstack11ll1lllll1_opy_ = True
        return bstack11l1l1ll_opy_(bs_config.get(bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⅙"), bstack11ll1lllll1_opy_))
    @classmethod
    def bstack1llll1llll11_opy_(cls, framework):
        return framework in bstack11lll1111ll_opy_
    @classmethod
    def bstack1lllll1lll1l_opy_(cls, bs_config, framework):
        return cls.bstack1lllll111111_opy_(bs_config, framework) is True and cls.bstack1llll1llll11_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⅚"), None)
    @staticmethod
    def bstack111ll1l111_opy_():
        if getattr(threading.current_thread(), bstack11l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⅛"), None):
            return {
                bstack11l1111_opy_ (u"ࠧࡵࡻࡳࡩࠬ⅜"): bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹ࠭⅝"),
                bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⅞"): getattr(threading.current_thread(), bstack11l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⅟"), None)
            }
        if getattr(threading.current_thread(), bstack11l1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨⅠ"), None):
            return {
                bstack11l1111_opy_ (u"ࠬࡺࡹࡱࡧࠪⅡ"): bstack11l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࠫⅢ"),
                bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅣ"): getattr(threading.current_thread(), bstack11l1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬⅤ"), None)
            }
        return None
    @staticmethod
    def bstack1llll1lll1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1ll111ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1111lllll1_opy_(test, hook_name=None):
        bstack1llll1lll1l1_opy_ = test.parent
        if hook_name in [bstack11l1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧⅥ"), bstack11l1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫⅦ"), bstack11l1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪⅧ"), bstack11l1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧⅨ")]:
            bstack1llll1lll1l1_opy_ = test
        scope = []
        while bstack1llll1lll1l1_opy_ is not None:
            scope.append(bstack1llll1lll1l1_opy_.name)
            bstack1llll1lll1l1_opy_ = bstack1llll1lll1l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll1lll11l_opy_(hook_type):
        if hook_type == bstack11l1111_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦⅩ"):
            return bstack11l1111_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦⅪ")
        elif hook_type == bstack11l1111_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧⅫ"):
            return bstack11l1111_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤⅬ")
    @staticmethod
    def bstack1llll1lll111_opy_(bstack111l11l1_opy_):
        try:
            if not bstack1l1ll111ll_opy_.on():
                return bstack111l11l1_opy_
            if os.environ.get(bstack11l1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣⅭ"), None) == bstack11l1111_opy_ (u"ࠦࡹࡸࡵࡦࠤⅮ"):
                tests = os.environ.get(bstack11l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤⅯ"), None)
                if tests is None or tests == bstack11l1111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦⅰ"):
                    return bstack111l11l1_opy_
                bstack111l11l1_opy_ = tests.split(bstack11l1111_opy_ (u"ࠧ࠭ࠩⅱ"))
                return bstack111l11l1_opy_
        except Exception as exc:
            logger.debug(bstack11l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤⅲ") + str(str(exc)) + bstack11l1111_opy_ (u"ࠤࠥⅳ"))
        return bstack111l11l1_opy_