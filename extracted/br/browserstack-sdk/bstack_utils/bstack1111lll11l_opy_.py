# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import threading
from bstack_utils.helper import bstack1lll1l111_opy_
from bstack_utils.constants import bstack111llll1111_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l111111_opy_:
    bstack1lll1l1l1l1l_opy_ = None
    @classmethod
    def bstack1l1l1ll1ll_opy_(cls):
        if cls.on() and os.getenv(bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⑷")):
            logger.info(
                bstack11l1l11_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬ⑸").format(os.getenv(bstack11l1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⑹"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⑺"), None) is None or os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⑻")] == bstack11l1l11_opy_ (u"ࠤࡱࡹࡱࡲࠢ⑼"):
            return False
        return True
    @classmethod
    def bstack1ll1lllll1l1_opy_(cls, bs_config, framework=bstack11l1l11_opy_ (u"ࠥࠦ⑽")):
        bstack11l11111111_opy_ = False
        for fw in bstack111llll1111_opy_:
            if fw in framework:
                bstack11l11111111_opy_ = True
        return bstack1lll1l111_opy_(bs_config.get(bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⑾"), bstack11l11111111_opy_))
    @classmethod
    def bstack1ll1llll1111_opy_(cls, framework):
        return framework in bstack111llll1111_opy_
    @classmethod
    def bstack1lll1111ll1l_opy_(cls, bs_config, framework):
        return cls.bstack1ll1lllll1l1_opy_(bs_config, framework) is True and cls.bstack1ll1llll1111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⑿"), None)
    @staticmethod
    def bstack1111l1l1l1_opy_():
        if getattr(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⒀"), None):
            return {
                bstack11l1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ⒁"): bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭⒂"),
                bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⒃"): getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⒄"), None)
            }
        if getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⒅"), None):
            return {
                bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ⒆"): bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⒇"),
                bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⒈"): getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⒉"), None)
            }
        return None
    @staticmethod
    def bstack1ll1lll1llll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l111111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111111lll1_opy_(test, hook_name=None):
        bstack1ll1llll111l_opy_ = test.parent
        if hook_name in [bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⒊"), bstack11l1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⒋"), bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⒌"), bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⒍")]:
            bstack1ll1llll111l_opy_ = test
        scope = []
        while bstack1ll1llll111l_opy_ is not None:
            scope.append(bstack1ll1llll111l_opy_.name)
            bstack1ll1llll111l_opy_ = bstack1ll1llll111l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1lll1lll1_opy_(hook_type):
        if hook_type == bstack11l1l11_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦ⒎"):
            return bstack11l1l11_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦ⒏")
        elif hook_type == bstack11l1l11_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧ⒐"):
            return bstack11l1l11_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤ⒑")
    @staticmethod
    def bstack1ll1llll11l1_opy_(bstack111ll11111_opy_):
        try:
            if not bstack1l111111_opy_.on():
                return bstack111ll11111_opy_
            if os.environ.get(bstack11l1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣ⒒"), None) == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ⒓"):
                tests = os.environ.get(bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤ⒔"), None)
                if tests is None or tests == bstack11l1l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⒕"):
                    return bstack111ll11111_opy_
                bstack111ll11111_opy_ = tests.split(bstack11l1l11_opy_ (u"ࠧ࠭ࠩ⒖"))
                return bstack111ll11111_opy_
        except Exception as exc:
            logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤ⒗") + str(str(exc)) + bstack11l1l11_opy_ (u"ࠤࠥ⒘"))
        return bstack111ll11111_opy_