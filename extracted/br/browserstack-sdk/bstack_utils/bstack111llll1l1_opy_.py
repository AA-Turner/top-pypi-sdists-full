# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
import threading
from bstack_utils.helper import bstack1ll111l11l_opy_
from bstack_utils.constants import bstack11l1ll1l111_opy_, EVENTS, STAGE
from bstack_utils.bstack1l1111ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11llll1l11_opy_:
    bstack111111l1l1l_opy_ = None
    @classmethod
    def bstack11l1lll1l1_opy_(cls):
        if cls.on() and os.getenv(bstack111l111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ⅖")):
            logger.info(
                bstack111l111_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬ⅗").format(os.getenv(bstack111l111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⅘"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⅙"), None) is None or os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⅚")] == bstack111l111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⅛"):
            return False
        return True
    @classmethod
    def bstack1lllll111ll1_opy_(cls, bs_config, framework=bstack111l111_opy_ (u"ࠢࠣ⅜")):
        bstack11lll111l1l_opy_ = False
        for fw in bstack11l1ll1l111_opy_:
            if fw in framework:
                bstack11lll111l1l_opy_ = True
        return bstack1ll111l11l_opy_(bs_config.get(bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⅝"), bstack11lll111l1l_opy_))
    @classmethod
    def bstack1llll1lll111_opy_(cls, framework):
        return framework in bstack11l1ll1l111_opy_
    @classmethod
    def bstack1lllll11l1ll_opy_(cls, bs_config, framework):
        return cls.bstack1lllll111ll1_opy_(bs_config, framework) is True and cls.bstack1llll1lll111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⅞"), None)
    @staticmethod
    def bstack111ll1llll_opy_():
        if getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⅟"), None):
            return {
                bstack111l111_opy_ (u"ࠫࡹࡿࡰࡦࠩⅠ"): bstack111l111_opy_ (u"ࠬࡺࡥࡴࡶࠪⅡ"),
                bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ⅲ"): getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫⅣ"), None)
            }
        if getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬⅤ"), None):
            return {
                bstack111l111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧⅥ"): bstack111l111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨⅦ"),
                bstack111l111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅧ"): getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩⅨ"), None)
            }
        return None
    @staticmethod
    def bstack1llll1lll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11llll1l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l1l111l_opy_(test, hook_name=None):
        bstack1llll1ll1lll_opy_ = test.parent
        if hook_name in [bstack111l111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫⅩ"), bstack111l111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨⅪ"), bstack111l111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧⅫ"), bstack111l111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫⅬ")]:
            bstack1llll1ll1lll_opy_ = test
        scope = []
        while bstack1llll1ll1lll_opy_ is not None:
            scope.append(bstack1llll1ll1lll_opy_.name)
            bstack1llll1ll1lll_opy_ = bstack1llll1ll1lll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll1lll1l1_opy_(hook_type):
        if hook_type == bstack111l111_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣⅭ"):
            return bstack111l111_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣⅮ")
        elif hook_type == bstack111l111_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤⅯ"):
            return bstack111l111_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨⅰ")
    @staticmethod
    def bstack1llll1ll1ll1_opy_(bstack1l111lll11_opy_):
        try:
            if not bstack11llll1l11_opy_.on():
                return bstack1l111lll11_opy_
            if os.environ.get(bstack111l111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧⅱ"), None) == bstack111l111_opy_ (u"ࠣࡶࡵࡹࡪࠨⅲ"):
                tests = os.environ.get(bstack111l111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨⅳ"), None)
                if tests is None or tests == bstack111l111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣⅴ"):
                    return bstack1l111lll11_opy_
                bstack1l111lll11_opy_ = tests.split(bstack111l111_opy_ (u"ࠫ࠱࠭ⅵ"))
                return bstack1l111lll11_opy_
        except Exception as exc:
            logger.debug(bstack111l111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨⅶ") + str(str(exc)) + bstack111l111_opy_ (u"ࠨࠢⅷ"))
        return bstack1l111lll11_opy_