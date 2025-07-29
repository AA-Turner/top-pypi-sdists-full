# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
import threading
from bstack_utils.helper import bstack11l1111ll_opy_
from bstack_utils.constants import bstack11l1ll1l11l_opy_, EVENTS, STAGE
from bstack_utils.bstack1ll11l1ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l11l1l1l1_opy_:
    bstack111111l1111_opy_ = None
    @classmethod
    def bstack1l1l1l1l1_opy_(cls):
        if cls.on() and os.getenv(bstackl_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⅗")):
            logger.info(
                bstackl_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭⅘").format(os.getenv(bstackl_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⅙"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⅚"), None) is None or os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⅛")] == bstackl_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⅜"):
            return False
        return True
    @classmethod
    def bstack1lllll111l1l_opy_(cls, bs_config, framework=bstackl_opy_ (u"ࠣࠤ⅝")):
        bstack11ll1111l1l_opy_ = False
        for fw in bstack11l1ll1l11l_opy_:
            if fw in framework:
                bstack11ll1111l1l_opy_ = True
        return bstack11l1111ll_opy_(bs_config.get(bstackl_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⅞"), bstack11ll1111l1l_opy_))
    @classmethod
    def bstack1llll1lll111_opy_(cls, framework):
        return framework in bstack11l1ll1l11l_opy_
    @classmethod
    def bstack1lllll11llll_opy_(cls, bs_config, framework):
        return cls.bstack1lllll111l1l_opy_(bs_config, framework) is True and cls.bstack1llll1lll111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⅟"), None)
    @staticmethod
    def bstack111ll11lll_opy_():
        if getattr(threading.current_thread(), bstackl_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨⅠ"), None):
            return {
                bstackl_opy_ (u"ࠬࡺࡹࡱࡧࠪⅡ"): bstackl_opy_ (u"࠭ࡴࡦࡵࡷࠫⅢ"),
                bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅣ"): getattr(threading.current_thread(), bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬⅤ"), None)
            }
        if getattr(threading.current_thread(), bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭Ⅵ"), None):
            return {
                bstackl_opy_ (u"ࠪࡸࡾࡶࡥࠨⅦ"): bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩⅧ"),
                bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅨ"): getattr(threading.current_thread(), bstackl_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪⅩ"), None)
            }
        return None
    @staticmethod
    def bstack1llll1lll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11l1l1l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l11llll_opy_(test, hook_name=None):
        bstack1llll1ll1l1l_opy_ = test.parent
        if hook_name in [bstackl_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬⅪ"), bstackl_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩⅫ"), bstackl_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨⅬ"), bstackl_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬⅭ")]:
            bstack1llll1ll1l1l_opy_ = test
        scope = []
        while bstack1llll1ll1l1l_opy_ is not None:
            scope.append(bstack1llll1ll1l1l_opy_.name)
            bstack1llll1ll1l1l_opy_ = bstack1llll1ll1l1l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll1ll1lll_opy_(hook_type):
        if hook_type == bstackl_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤⅮ"):
            return bstackl_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤⅯ")
        elif hook_type == bstackl_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥⅰ"):
            return bstackl_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢⅱ")
    @staticmethod
    def bstack1llll1ll1ll1_opy_(bstack11ll11l11l_opy_):
        try:
            if not bstack1l11l1l1l1_opy_.on():
                return bstack11ll11l11l_opy_
            if os.environ.get(bstackl_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨⅲ"), None) == bstackl_opy_ (u"ࠤࡷࡶࡺ࡫ࠢⅳ"):
                tests = os.environ.get(bstackl_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢⅴ"), None)
                if tests is None or tests == bstackl_opy_ (u"ࠦࡳࡻ࡬࡭ࠤⅵ"):
                    return bstack11ll11l11l_opy_
                bstack11ll11l11l_opy_ = tests.split(bstackl_opy_ (u"ࠬ࠲ࠧⅶ"))
                return bstack11ll11l11l_opy_
        except Exception as exc:
            logger.debug(bstackl_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢⅷ") + str(str(exc)) + bstackl_opy_ (u"ࠢࠣⅸ"))
        return bstack11ll11l11l_opy_