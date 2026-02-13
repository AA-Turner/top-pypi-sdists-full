# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import json
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
logger = get_logger(__name__)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _1lll1l111ll_opy_ = {
        bstack11l11_opy_ (u"ࠩࡦࡰࡴࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳࠩᆉ"), bstack11l11_opy_ (u"ࠪࡧࡱࡵࡳࡦࠢࡦࡳࡳࡺࡥࡹࡶࠪᆊ"), bstack11l11_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠣࡴࡦ࡭ࡥࠨᆋ"),
        bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣ࡭ࡱࡶࡩࠥࡨࡲࡰࡹࡶࡩࡷ࠭ᆌ"), bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡣࡰࡰࡷࡩࡽࡺࠧᆍ"), bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡱࡣࡪࡩࠬᆎ"),
    }
    def __init__(self):
        self._1lll11llll1_opy_ = None
        self._1lll1l111l1_opy_ = False
        self._1lll11ll1l1_opy_ = False
        self._1lll1l1111l_opy_ = None
        self._1lll1l11l1l_opy_ = None
    def _1lll11ll1ll_opy_(self):
        if self._1lll11llll1_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1lll11llll1_opy_ = BuiltIn().get_library_instance(bstack11l11_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࠩᆏ"))
            except Exception as e:
                logger.warning(bstack11l11_opy_ (u"ࠤࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥ࡭ࡥࡵࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡀࠠࡼࡧࢀࠦᆐ").format(e=e))
        return self._1lll11llll1_opy_
    def _1lll11lll11_opy_(self):
        try:
            bstack1lll11lll1l_opy_ = self._1lll11ll1ll_opy_()
            if bstack1lll11lll1l_opy_ and hasattr(bstack1lll11lll1l_opy_, bstack11l11_opy_ (u"ࠪࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡠࡵࡷࡥࡹ࡫ࠧᆑ")):
                bstack1lll1l11111_opy_ = bstack1lll11lll1l_opy_._playwright_state._get_browser_catalog()
                for bstack1lll11l1l1l_opy_ in bstack1lll1l11111_opy_:
                    contexts = bstack1lll11l1l1l_opy_.get(bstack11l11_opy_ (u"ࠫࡨࡵ࡮ࡵࡧࡻࡸࡸ࠭ᆒ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack11l11_opy_ (u"ࠬࡶࡡࡨࡧࡶࠫᆓ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦ࠼ࠣࡿࡪࢃࠢᆔ").format(e=e))
            return False
    def _1lll11l11ll_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1lll11l11l1_opy_ = {
                bstack11l11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᆕ"): action,
                bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᆖ"): arguments
            }
            executor_cmd = bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠬᆗ") + json.dumps(bstack1lll11l11l1_opy_)
            arg_string = bstack11l11_opy_ (u"ࠥࡥࡷ࡭࠽ࡼࡧࡻࡩࡨࡻࡴࡰࡴࡢࡧࡲࡪࡽࠣᆘ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack11l11_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡋࡶࡢ࡮ࡸࡥࡹ࡫ࠠࡋࡣࡹࡥࡘࡩࡲࡪࡲࡷࠫᆙ"),
                None,
                bstack11l11_opy_ (u"ࠬࡥࠠ࠾ࡀࠣࡿࢂ࠭ᆚ"),
                arg_string
            )
            logger.debug(bstack11l11_opy_ (u"ࠨࡅࡹࡧࡦࡹࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡦࡩࡴࡪࡱࡱࢁ࠱ࠦࡲࡦࡵࡸࡰࡹࡀࠠࡼࡴࡨࡷࡺࡲࡴࡾࠤᆛ").format(action=action, result=result))
            return True
        except Exception as e:
            logger.warning(bstack11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡦࡿࠥᆜ").format(e=e))
    def _1lll11ll11l_opy_(self, status, reason=bstack11l11_opy_ (u"ࠣࠤᆝ")):
        bstack11l11_opy_ (u"ࠤࠥࠦࡒࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡳࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧࠨࠢᆞ")
        bstack1lll1l11l11_opy_ = bstack11l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᆟ") if status == bstack11l11_opy_ (u"ࠦࡕࡇࡓࡔࠤᆠ") else bstack11l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᆡ")
        if bstack1lll1l11l11_opy_ == bstack11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᆢ"):
            return self._1lll11l11ll_opy_(bstack11l11_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᆣ"), {
                bstack11l11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᆤ"): bstack1lll1l11l11_opy_,
                bstack11l11_opy_ (u"ࠤࡵࡩࡦࡹ࡯࡯ࠤᆥ"): reason
            })
        else:
            return self._1lll11l11ll_opy_(bstack11l11_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᆦ"), {
                bstack11l11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᆧ"): bstack1lll1l11l11_opy_
            })
    def _1lll11l1lll_opy_(self, name):
        bstack11l11_opy_ (u"ࠧࠨࠢࡔࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡳࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧࠨࠢᆨ")
        return self._1lll11l11ll_opy_(bstack11l11_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᆩ"), {
            bstack11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆪ"): name
        })
    def _1lll11ll111_opy_(self):
        bstack11l11_opy_ (u"ࠣࠤࠥࡑࡦࡸ࡫ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡡ࡯ࡦࠣࡷࡹࡧࡴࡶࡵࠣࡦࡪ࡬࡯ࡳࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡨࡲ࡯ࡴࡧࠣࡳࡷࠦࡴࡦࡣࡵࡨࡴࡽ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡹࡧࡴࡶࡵࠣ࡭ࡸࠦࡩ࡯ࡨࡨࡶࡷ࡫ࡤࠡࡨࡵࡳࡲࠦ࡟࡭ࡣࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩ࠿ࠦࡩࡧࠢࡤࡲࡾࠦࡆࡂࡋࡏ࠱ࡱ࡫ࡶࡦ࡮ࠣࡰࡴ࡭ࠠ࡮ࡧࡶࡷࡦ࡭ࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺࡥࡸࠦࡣࡢࡲࡷࡹࡷ࡫ࡤࠡࡦࡸࡶ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡺࡥࡴࡶ࠯ࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡩࡴࠢࡩࡥ࡮ࡲࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᆫ")
        if self._1lll11ll1l1_opy_:
            return
        try:
            bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
            if self._1lll1l1111l_opy_ and not bstack11l1l1111_opy_.bstack1lll11l1ll1_opy_():
                self._1lll11l1lll_opy_(self._1lll1l1111l_opy_)
            status = bstack11l11_opy_ (u"ࠩࡉࡅࡎࡒࠧᆬ") if self._1lll1l11l1l_opy_ else bstack11l11_opy_ (u"ࠪࡔࡆ࡙ࡓࠨᆭ")
            message = self._1lll1l11l1l_opy_ or bstack11l11_opy_ (u"ࠫࠬᆮ")
            if not bstack11l1l1111_opy_.bstack1llll11l11l_opy_():
                logger.debug(bstack11l11_opy_ (u"ࠧࡓࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡤ࡮ࡲࡷࡪࡀࠠࡴࡶࡤࡸࡺࡹ࠽ࡼࡵࡷࡥࡹࡻࡳࡾ࠮ࠣࡱࡪࡹࡳࡢࡩࡨࡁࢀࡳࡥࡴࡵࡤ࡫ࡪࢃࠢᆯ").format(status=status, message=message))
                self._1lll11ll11l_opy_(status, message)
            self._1lll11ll1l1_opy_ = True
            logger.debug(bstack11l11_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡳࡡࡳ࡭ࡨࡨࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᆰ"))
        except Exception as e:
            logger.error(bstack11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࡪࢃࠢᆱ").format(e=e))
    def start_test(self, name, attrs):
        logger.debug(bstack11l11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡵࡧࡶࡸࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡵࡧࡶࡸ࠿ࠦࡻ࡯ࡣࡰࡩࢂࠨᆲ").format(name=name))
        self._1lll1l111l1_opy_ = False
        self._1lll11ll1l1_opy_ = False
        self._1lll1l1111l_opy_ = name
        self._1lll1l11l1l_opy_ = None
    def end_test(self, name, attrs):
        status = attrs.get(bstack11l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᆳ"), bstack11l11_opy_ (u"࡙ࠪࡓࡑࡎࡐ࡙ࡑࠫᆴ"))
        message = attrs.get(bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᆵ"), bstack11l11_opy_ (u"ࠬ࠭ᆶ"))
        logger.debug(bstack11l11_opy_ (u"ࠨࡥ࡯ࡦࡢࡸࡪࡹࡴࠡࡅࡄࡐࡑࡋࡄࠡ࠯ࠣࡸࡪࡹࡴ࠻ࠢࡾࡲࡦࡳࡥࡾ࠮ࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࡹࡴࡢࡶࡸࡷࢂࠨᆷ").format(name=name, status=status))
        self._1lll1l111l1_opy_ = True
        if not self._1lll11ll1l1_opy_ and self._1lll11lll11_opy_():
            try:
                bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
                if not bstack11l1l1111_opy_.bstack1lll11l1ll1_opy_():
                    self._1lll11l1lll_opy_(name)
                if not bstack11l1l1111_opy_.bstack1llll11l11l_opy_():
                    logger.debug(bstack11l11_opy_ (u"ࠢࡎࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡲࠥ࡫࡮ࡥࡡࡷࡩࡸࡺ࠺ࠡࡵࡷࡥࡹࡻࡳ࠾ࡽࡶࡸࡦࡺࡵࡴࡿࠥᆸ").format(status=status))
                    self._1lll11ll11l_opy_(status, message)
                self._1lll11ll1l1_opy_ = True
                logger.debug(bstack11l11_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᆹ"))
            except Exception as e:
                logger.error(bstack11l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡴࠠࡦࡰࡧࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡪࢃࠢᆺ").format(e=e))
        elif self._1lll11ll1l1_opy_:
            logger.debug(bstack11l11_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤࡦࡲࡲࡦࡣࡧࡽࠥࡳࡡࡳ࡭ࡨࡨࠧᆻ"))
        else:
            logger.debug(bstack11l11_opy_ (u"ࠦࡓࡵࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠢᆼ"))
    def start_suite(self, name, attrs):
        bstack11l11_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡽࡨࡦࡰࠣࡥࠥࡹࡵࡪࡶࡨࠤࡸࡺࡡࡳࡶࡶࠦࠧࠨᆽ")
        logger.debug(bstack11l11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡵࡪࡶࡨࠤࡈࡇࡌࡍࡇࡇࠤ࠲ࠦࡳࡶ࡫ࡷࡩ࠿ࠦࡻ࡯ࡣࡰࡩࢂࠨᆾ").format(name=name))
    def end_suite(self, name, attrs):
        bstack11l11_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࡥࡥࠢࡥࡽࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡸࡪࡨࡲࠥࡧࠠࡴࡷ࡬ࡸࡪࠦࡥ࡯ࡦࡶࠦࠧࠨᆿ")
        logger.debug(bstack11l11_opy_ (u"ࠣࡧࡱࡨࡤࡹࡵࡪࡶࡨࠤࡈࡇࡌࡍࡇࡇࠤ࠲ࠦࡳࡶ࡫ࡷࡩ࠿ࠦࡻ࡯ࡣࡰࡩࢂࠨᇀ").format(name=name))
    def start_keyword(self, name, attrs):
        bstack11l11_opy_ (u"ࠤࠥࠦࡈࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡥࡩ࡫ࡵࡲࡦࠢࡤࠤࡰ࡫ࡹࡸࡱࡵࡨࠥ࡫ࡸࡦࡥࡸࡸࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡐࡥࡷࡱࡳࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡣࡱࡽࠥࡩ࡬ࡰࡵࡨࠤࡰ࡫ࡹࡸࡱࡵࡨࠥ࡫ࡸࡦࡥࡸࡸࡪࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠪࡺ࡬࡮ࡲࡥࠡࡲࡤ࡫ࡪࠦࡩࡴࠢࡶࡸ࡮ࡲ࡬ࠡࡣࡦࡸ࡮ࡼࡥࠪࠢࡲࡶࠥࡨࡥࡧࡱࡵࡩࠥࡺࡥࡢࡴࡧࡳࡼࡴࠠࡣࡧࡪ࡭ࡳࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᇁ")
        if self._1lll11ll1l1_opy_ or self._1lll1l111l1_opy_:
            return
        bstack1lll11l1l11_opy_ = False
        bstack1lll11lllll_opy_ = attrs.get(bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨᇂ"), bstack11l11_opy_ (u"ࠫࠬᇃ")).lower()
        if name.lower() in self._1lll1l111ll_opy_:
            bstack1lll11l1l11_opy_ = True
            logger.debug(bstack11l11_opy_ (u"ࠧࡉ࡬ࡰࡵࡨࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࡽࡱࡥࡲ࡫ࡽ࠭ࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡮ࡺࠠࡦࡺࡨࡧࡺࡺࡥࡴࠤᇄ").format(name=name))
        elif bstack1lll11lllll_opy_ == bstack11l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᇅ"):
            bstack1lll11l1l11_opy_ = True
            logger.debug(bstack11l11_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪ࠰ࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡵࡧࡤࡶࡩࡵࡷ࡯ࠢࡨࡼࡪࡩࡵࡵࡧࡶࠦᇆ"))
        if bstack1lll11l1l11_opy_ and self._1lll11lll11_opy_():
            self._1lll11ll111_opy_()
    def log_message(self, message):
        bstack11l11_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡴࡼࠤࡱࡵࡧࠡ࡯ࡨࡷࡸࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡧࡰࡵࡷࡵࡩࡸࠦࡆࡂࡋࡏࠤࡱ࡫ࡶࡦ࡮ࠣࡱࡪࡹࡳࡢࡩࡨࡷࠥࡺ࡯ࠡࡷࡶࡩࠥࡧࡳࠡࡧࡵࡶࡴࡸࠠࡳࡧࡤࡷࡴࡴࠬࠋࠢࠣࠤࠥࠦࠠࠡࠢࡶ࡭ࡳࡩࡥࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡤࡸࡹࡸࡳࠡࡦࡲࡩࡸࡴࠧࡵࠢ࡬ࡲࡨࡲࡵࡥࡧࠣࡸ࡭࡫ࠠࡦࡴࡵࡳࡷࠦ࡭ࡦࡵࡶࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᇇ")
        level = message.get(bstack11l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᇈ"), bstack11l11_opy_ (u"ࠪࠫᇉ"))
        if level == bstack11l11_opy_ (u"ࠫࡋࡇࡉࡍࠩᇊ"):
            self._1lll1l11l1l_opy_ = message.get(bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᇋ"), bstack11l11_opy_ (u"࠭ࠧᇌ"))
            logger.debug(bstack11l11_opy_ (u"ࠢࡄࡣࡳࡸࡺࡸࡥࡥࠢࡨࡶࡷࡵࡲࠡ࡯ࡨࡷࡸࡧࡧࡦ࠼ࠣࡿࡪࡸࡲࡰࡴࢀࠦᇍ").format(error=self._1lll1l11l1l_opy_))