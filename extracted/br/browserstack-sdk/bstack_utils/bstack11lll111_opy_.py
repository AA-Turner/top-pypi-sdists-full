# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import threading
from bstack_utils.helper import bstack1111l11lll_opy_
from bstack_utils.constants import bstack111111ll111_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1lll1l11l_opy_:
    bstack1ll1l111111l_opy_ = None
    @classmethod
    def bstack1111l1111_opy_(cls):
        if cls.on() and os.getenv(bstack111ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⣺")):
            logger.info(
                bstack111ll11_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬ⣻").format(os.getenv(bstack111ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⣼"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⣽"), None) is None or os.environ[bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⣾")] == bstack111ll11_opy_ (u"ࠤࡱࡹࡱࡲࠢ⣿"):
            return False
        return True
    @classmethod
    def bstack1ll111l11111_opy_(cls, bs_config, framework=bstack111ll11_opy_ (u"ࠥࠦ⤀")):
        bstack11111ll1l11_opy_ = False
        for fw in bstack111111ll111_opy_:
            if fw in framework:
                bstack11111ll1l11_opy_ = True
        return bstack1111l11lll_opy_(bs_config.get(bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⤁"), bstack11111ll1l11_opy_))
    @classmethod
    def bstack1ll1111ll1ll_opy_(cls, framework):
        return framework in bstack111111ll111_opy_
    @classmethod
    def bstack1ll11l111l11_opy_(cls, bs_config, framework):
        return cls.bstack1ll111l11111_opy_(bs_config, framework) is True and cls.bstack1ll1111ll1ll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⤂"), None)
    @staticmethod
    def bstack1llll11l11l_opy_():
        if getattr(threading.current_thread(), bstack111ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⤃"), None):
            return {
                bstack111ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬ⤄"): bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹ࠭⤅"),
                bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⤆"): getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⤇"), None)
            }
        if getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⤈"), None):
            return {
                bstack111ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪ⤉"): bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⤊"),
                bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⤋"): getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⤌"), None)
            }
        return None
    @staticmethod
    def bstack1ll1111lll1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll1l11l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lll1l1l1l1_opy_(test, hook_name=None):
        bstack1ll1111lll11_opy_ = test.parent
        if hook_name in [bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⤍"), bstack111ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⤎"), bstack111ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⤏"), bstack111ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⤐")]:
            bstack1ll1111lll11_opy_ = test
        scope = []
        while bstack1ll1111lll11_opy_ is not None:
            scope.append(bstack1ll1111lll11_opy_.name)
            bstack1ll1111lll11_opy_ = bstack1ll1111lll11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1111llll1_opy_(hook_type):
        if hook_type == bstack111ll11_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦ⤑"):
            return bstack111ll11_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦ⤒")
        elif hook_type == bstack111ll11_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧ⤓"):
            return bstack111ll11_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤ⤔")
    @staticmethod
    def bstack1ll1111lllll_opy_(bstack111l1l1l1l_opy_):
        try:
            if not bstack1lll1l11l_opy_.on():
                return bstack111l1l1l1l_opy_
            if os.environ.get(bstack111ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣ⤕"), None) == bstack111ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤ⤖"):
                tests = os.environ.get(bstack111ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤ⤗"), None)
                if tests is None or tests == bstack111ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⤘"):
                    return bstack111l1l1l1l_opy_
                bstack111l1l1l1l_opy_ = tests.split(bstack111ll11_opy_ (u"ࠧ࠭ࠩ⤙"))
                return bstack111l1l1l1l_opy_
        except Exception as exc:
            logger.debug(bstack111ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤ⤚") + str(str(exc)) + bstack111ll11_opy_ (u"ࠤࠥ⤛"))
        return bstack111l1l1l1l_opy_