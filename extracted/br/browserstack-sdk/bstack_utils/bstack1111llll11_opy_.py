# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import threading
from bstack_utils.helper import bstack1ll1lll1l_opy_
from bstack_utils.constants import bstack11l111l1111_opy_, EVENTS, STAGE
from bstack_utils.bstack1l1111l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack1ll11l1l1l_opy_:
    bstack1lll1llll11l_opy_ = None
    @classmethod
    def bstack1ll11111_opy_(cls):
        if cls.on() and os.getenv(bstack11l1ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⎀")):
            logger.info(
                bstack11l1ll1_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠪ⎁").format(os.getenv(bstack11l1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⎂"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⎃"), None) is None or os.environ[bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⎄")] == bstack11l1ll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⎅"):
            return False
        return True
    @classmethod
    def bstack1lll111llll1_opy_(cls, bs_config, framework=bstack11l1ll1_opy_ (u"ࠣࠤ⎆")):
        bstack11l11l1l1l1_opy_ = False
        for fw in bstack11l111l1111_opy_:
            if fw in framework:
                bstack11l11l1l1l1_opy_ = True
        return bstack1ll1lll1l_opy_(bs_config.get(bstack11l1ll1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⎇"), bstack11l11l1l1l1_opy_))
    @classmethod
    def bstack1lll111ll111_opy_(cls, framework):
        return framework in bstack11l111l1111_opy_
    @classmethod
    def bstack1lll11l1l1ll_opy_(cls, bs_config, framework):
        return cls.bstack1lll111llll1_opy_(bs_config, framework) is True and cls.bstack1lll111ll111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⎈"), None)
    @staticmethod
    def bstack1111lll11l_opy_():
        if getattr(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⎉"), None):
            return {
                bstack11l1ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ⎊"): bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࠫ⎋"),
                bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⎌"): getattr(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⎍"), None)
            }
        if getattr(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⎎"), None):
            return {
                bstack11l1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨ⎏"): bstack11l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⎐"),
                bstack11l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⎑"): getattr(threading.current_thread(), bstack11l1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⎒"), None)
            }
        return None
    @staticmethod
    def bstack1lll111l1lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll11l1l1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11111l11l1_opy_(test, hook_name=None):
        bstack1lll111l1ll1_opy_ = test.parent
        if hook_name in [bstack11l1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⎓"), bstack11l1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⎔"), bstack11l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⎕"), bstack11l1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⎖")]:
            bstack1lll111l1ll1_opy_ = test
        scope = []
        while bstack1lll111l1ll1_opy_ is not None:
            scope.append(bstack1lll111l1ll1_opy_.name)
            bstack1lll111l1ll1_opy_ = bstack1lll111l1ll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll111ll1l1_opy_(hook_type):
        if hook_type == bstack11l1ll1_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤ⎗"):
            return bstack11l1ll1_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤ⎘")
        elif hook_type == bstack11l1ll1_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥ⎙"):
            return bstack11l1ll1_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢ⎚")
    @staticmethod
    def bstack1lll111ll11l_opy_(bstack11l1ll1l1_opy_):
        try:
            if not bstack1ll11l1l1l_opy_.on():
                return bstack11l1ll1l1_opy_
            if os.environ.get(bstack11l1ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨ⎛"), None) == bstack11l1ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ⎜"):
                tests = os.environ.get(bstack11l1ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢ⎝"), None)
                if tests is None or tests == bstack11l1ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⎞"):
                    return bstack11l1ll1l1_opy_
                bstack11l1ll1l1_opy_ = tests.split(bstack11l1ll1_opy_ (u"ࠬ࠲ࠧ⎟"))
                return bstack11l1ll1l1_opy_
        except Exception as exc:
            logger.debug(bstack11l1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢ⎠") + str(str(exc)) + bstack11l1ll1_opy_ (u"ࠢࠣ⎡"))
        return bstack11l1ll1l1_opy_