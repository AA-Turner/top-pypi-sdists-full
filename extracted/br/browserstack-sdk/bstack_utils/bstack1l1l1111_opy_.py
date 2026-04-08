# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import threading
from bstack_utils.helper import bstack1l1ll11l1_opy_
from bstack_utils.constants import bstack11111l1l1l1_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111l1l1l11_opy_:
    bstack1ll1l111llll_opy_ = None
    @classmethod
    def bstack11l1l1ll1l_opy_(cls):
        if cls.on() and os.getenv(bstack111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⣃")):
            logger.info(
                bstack111l_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭⣄").format(os.getenv(bstack111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⣅"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⣆"), None) is None or os.environ[bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⣇")] == bstack111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⣈"):
            return False
        return True
    @classmethod
    def bstack1ll111ll1l11_opy_(cls, bs_config, framework=bstack111l_opy_ (u"ࠦࠧ⣉")):
        bstack11111llll11_opy_ = False
        for fw in bstack11111l1l1l1_opy_:
            if fw in framework:
                bstack11111llll11_opy_ = True
        return bstack1l1ll11l1_opy_(bs_config.get(bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⣊"), bstack11111llll11_opy_))
    @classmethod
    def bstack1ll111l1llll_opy_(cls, framework):
        return framework in bstack11111l1l1l1_opy_
    @classmethod
    def bstack1ll11l1ll111_opy_(cls, bs_config, framework):
        return cls.bstack1ll111ll1l11_opy_(bs_config, framework) is True and cls.bstack1ll111l1llll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⣋"), None)
    @staticmethod
    def bstack1llll1l1111_opy_():
        if getattr(threading.current_thread(), bstack111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⣌"), None):
            return {
                bstack111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⣍"): bstack111l_opy_ (u"ࠩࡷࡩࡸࡺࠧ⣎"),
                bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⣏"): getattr(threading.current_thread(), bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⣐"), None)
            }
        if getattr(threading.current_thread(), bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⣑"), None):
            return {
                bstack111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⣒"): bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⣓"),
                bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⣔"): getattr(threading.current_thread(), bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⣕"), None)
            }
        return None
    @staticmethod
    def bstack1ll111ll11l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111l1l1l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lll1ll1l11_opy_(test, hook_name=None):
        bstack1ll111ll1111_opy_ = test.parent
        if hook_name in [bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⣖"), bstack111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ⣗"), bstack111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⣘"), bstack111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⣙")]:
            bstack1ll111ll1111_opy_ = test
        scope = []
        while bstack1ll111ll1111_opy_ is not None:
            scope.append(bstack1ll111ll1111_opy_.name)
            bstack1ll111ll1111_opy_ = bstack1ll111ll1111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll111l1lll1_opy_(hook_type):
        if hook_type == bstack111l_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧ⣚"):
            return bstack111l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧ⣛")
        elif hook_type == bstack111l_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨ⣜"):
            return bstack111l_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥ⣝")
    @staticmethod
    def bstack1ll111ll111l_opy_(bstack1111lll11_opy_):
        try:
            if not bstack111l1l1l11_opy_.on():
                return bstack1111lll11_opy_
            if os.environ.get(bstack111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤ⣞"), None) == bstack111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ⣟"):
                tests = os.environ.get(bstack111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥ⣠"), None)
                if tests is None or tests == bstack111l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⣡"):
                    return bstack1111lll11_opy_
                bstack1111lll11_opy_ = tests.split(bstack111l_opy_ (u"ࠨ࠮ࠪ⣢"))
                return bstack1111lll11_opy_
        except Exception as exc:
            logger.debug(bstack111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥ⣣") + str(str(exc)) + bstack111l_opy_ (u"ࠥࠦ⣤"))
        return bstack1111lll11_opy_