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
import json
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
logger = get_logger(__name__)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _1lll1ll11l1_opy_ = {
        bstack11l1l11_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵࠫᆒ"), bstack11l1l11_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠤࡨࡵ࡮ࡵࡧࡻࡸࠬᆓ"), bstack11l1l11_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠥࡶࡡࡨࡧࠪᆔ"),
        bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠨᆕ"), bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ࠰ࡦࡰࡴࡹࡥࠡࡥࡲࡲࡹ࡫ࡸࡵࠩᆖ"), bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࠱ࡧࡱࡵࡳࡦࠢࡳࡥ࡬࡫ࠧᆗ"),
    }
    def __init__(self):
        self._1lll1l111l1_opy_ = None
        self._1lll1l11lll_opy_ = False
        self._1lll1l1l1l1_opy_ = False
        self._1lll1l11l1l_opy_ = None
        self._1lll1l111ll_opy_ = None
    def _1lll1l1ll11_opy_(self):
        if self._1lll1l111l1_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1lll1l111l1_opy_ = BuiltIn().get_library_instance(bstack11l1l11_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࠫᆘ"))
            except Exception as e:
                logger.warning(bstack11l1l11_opy_ (u"ࠦࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡨࡧࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࠥࡲࡩࡣࡴࡤࡶࡾࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠻ࠢࡾࡩࢂࠨᆙ").format(e=e))
        return self._1lll1l111l1_opy_
    def _1lll1l11l11_opy_(self):
        try:
            bstack1lll1l1l11l_opy_ = self._1lll1l1ll11_opy_()
            if bstack1lll1l1l11l_opy_ and hasattr(bstack1lll1l1l11l_opy_, bstack11l1l11_opy_ (u"ࠬࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡢࡷࡹࡧࡴࡦࠩᆚ")):
                bstack1lll1l11ll1_opy_ = bstack1lll1l1l11l_opy_._playwright_state._get_browser_catalog()
                for bstack1lll1ll111l_opy_ in bstack1lll1l11ll1_opy_:
                    contexts = bstack1lll1ll111l_opy_.get(bstack11l1l11_opy_ (u"࠭ࡣࡰࡰࡷࡩࡽࡺࡳࠨᆛ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack11l1l11_opy_ (u"ࠧࡱࡣࡪࡩࡸ࠭ᆜ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨ࠾ࠥࢁࡥࡾࠤᆝ").format(e=e))
            return False
    def _1lll1l1l1ll_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1lll1ll1111_opy_ = {
                bstack11l1l11_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩᆞ"): action,
                bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᆟ"): arguments
            }
            executor_cmd = bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠧᆠ") + json.dumps(bstack1lll1ll1111_opy_)
            arg_string = bstack11l1l11_opy_ (u"ࠧࡧࡲࡨ࠿ࡾࡩࡽ࡫ࡣࡶࡶࡲࡶࡤࡩ࡭ࡥࡿࠥᆡ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack11l1l11_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸ࠮ࡆࡸࡤࡰࡺࡧࡴࡦࠢࡍࡥࡻࡧࡓࡤࡴ࡬ࡴࡹ࠭ᆢ"),
                None,
                bstack11l1l11_opy_ (u"ࠧࡠࠢࡀࡂࠥࢁࡽࠨᆣ"),
                arg_string
            )
            logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡻࡩࡨࡻࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡡࡤࡶ࡬ࡳࡳࢃࠬࠡࡴࡨࡷࡺࡲࡴ࠻ࠢࡾࡶࡪࡹࡵ࡭ࡶࢀࠦᆤ").format(action=action, result=result))
            return True
        except Exception as e:
            logger.warning(bstack11l1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡫ࡸࡦࡥࡸࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࡨࢁࠧᆥ").format(e=e))
    def _1lll1l1ll1l_opy_(self, status, reason=bstack11l1l11_opy_ (u"ࠥࠦᆦ")):
        bstack11l1l11_opy_ (u"ࠦࠧࠨࡍࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࡵ࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢࠣࠤᆧ")
        bstack1lll1l1llll_opy_ = bstack11l1l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᆨ") if status == bstack11l1l11_opy_ (u"ࠨࡐࡂࡕࡖࠦᆩ") else bstack11l1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᆪ")
        if bstack1lll1l1llll_opy_ == bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᆫ"):
            return self._1lll1l1l1ll_opy_(bstack11l1l11_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᆬ"), {
                bstack11l1l11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᆭ"): bstack1lll1l1llll_opy_,
                bstack11l1l11_opy_ (u"ࠦࡷ࡫ࡡࡴࡱࡱࠦᆮ"): reason
            })
        else:
            return self._1lll1l1l1ll_opy_(bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᆯ"), {
                bstack11l1l11_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᆰ"): bstack1lll1l1llll_opy_
            })
    def _1lll1l1l111_opy_(self, name):
        bstack11l1l11_opy_ (u"ࠢࠣࠤࡖࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࡵ࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢࠣࠤᆱ")
        return self._1lll1l1l1ll_opy_(bstack11l1l11_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᆲ"), {
            bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆳ"): name
        })
    def _1lll1l1lll1_opy_(self):
        bstack11l1l11_opy_ (u"ࠥࠦࠧࡓࡡࡳ࡭ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡨࡥࡧࡱࡵࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡣ࡭ࡱࡶࡩࠥࡵࡲࠡࡶࡨࡥࡷࡪ࡯ࡸࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡴࡢࡶࡸࡷࠥ࡯ࡳࠡ࡫ࡱࡪࡪࡸࡲࡦࡦࠣࡪࡷࡵ࡭ࠡࡡ࡯ࡥࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫࠺ࠡ࡫ࡩࠤࡦࡴࡹࠡࡈࡄࡍࡑ࠳࡬ࡦࡸࡨࡰࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼࡧࡳࠡࡥࡤࡴࡹࡻࡲࡦࡦࠣࡨࡺࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡵࡧࡶࡸ࠱ࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡ࡫ࡶࠤ࡫ࡧࡩ࡭࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᆴ")
        if self._1lll1l1l1l1_opy_:
            return
        try:
            global_config = Config.get_instance()
            if self._1lll1l11l1l_opy_ and not global_config.should_skip_session_name():
                self._1lll1l1l111_opy_(self._1lll1l11l1l_opy_)
            status = bstack11l1l11_opy_ (u"ࠫࡋࡇࡉࡍࠩᆵ") if self._1lll1l111ll_opy_ else bstack11l1l11_opy_ (u"ࠬࡖࡁࡔࡕࠪᆶ")
            message = self._1lll1l111ll_opy_ or bstack11l1l11_opy_ (u"࠭ࠧᆷ")
            if not global_config.should_skip_session_status():
                logger.debug(bstack11l1l11_opy_ (u"ࠢࡎࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡦࡰࡴࡹࡥ࠻ࠢࡶࡸࡦࡺࡵࡴ࠿ࡾࡷࡹࡧࡴࡶࡵࢀ࠰ࠥࡳࡥࡴࡵࡤ࡫ࡪࡃࡻ࡮ࡧࡶࡷࡦ࡭ࡥࡾࠤᆸ").format(status=status, message=message))
                self._1lll1l1ll1l_opy_(status, message)
            self._1lll1l1l1l1_opy_ = True
            logger.debug(bstack11l1l11_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᆹ"))
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡥࡾࠤᆺ").format(e=e))
    def start_test(self, name, attrs):
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡷࡩࡸࡺࠠࡄࡃࡏࡐࡊࡊࠠ࠮ࠢࡷࡩࡸࡺ࠺ࠡࡽࡱࡥࡲ࡫ࡽࠣᆻ").format(name=name))
        self._1lll1l11lll_opy_ = False
        self._1lll1l1l1l1_opy_ = False
        self._1lll1l11l1l_opy_ = name
        self._1lll1l111ll_opy_ = None
    def end_test(self, name, attrs):
        status = attrs.get(bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᆼ"), bstack11l1l11_opy_ (u"࡛ࠬࡎࡌࡐࡒ࡛ࡓ࠭ᆽ"))
        message = attrs.get(bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᆾ"), bstack11l1l11_opy_ (u"ࠧࠨᆿ"))
        logger.debug(bstack11l1l11_opy_ (u"ࠣࡧࡱࡨࡤࡺࡥࡴࡶࠣࡇࡆࡒࡌࡆࡆࠣ࠱ࠥࡺࡥࡴࡶ࠽ࠤࢀࡴࡡ࡮ࡧࢀ࠰ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡴࡶࡤࡸࡺࡹࡽࠣᇀ").format(name=name, status=status))
        self._1lll1l11lll_opy_ = True
        if not self._1lll1l1l1l1_opy_ and self._1lll1l11l11_opy_():
            try:
                global_config = Config.get_instance()
                if not global_config.should_skip_session_name():
                    self._1lll1l1l111_opy_(name)
                if not global_config.should_skip_session_status():
                    logger.debug(bstack11l1l11_opy_ (u"ࠤࡐࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡴࠠࡦࡰࡧࡣࡹ࡫ࡳࡵ࠼ࠣࡷࡹࡧࡴࡶࡵࡀࡿࡸࡺࡡࡵࡷࡶࢁࠧᇁ").format(status=status))
                    self._1lll1l1ll1l_opy_(status, message)
                self._1lll1l1l1l1_opy_ = True
                logger.debug(bstack11l1l11_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡰࡥࡷࡱࡥࡥࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᇂ"))
            except Exception as e:
                logger.error(bstack11l1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩ࡯ࠢࡨࡲࡩࡥࡴࡦࡵࡷ࠾ࠥࢁࡥࡾࠤᇃ").format(e=e))
        elif self._1lll1l1l1l1_opy_:
            logger.debug(bstack11l1l11_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡡ࡭ࡴࡨࡥࡩࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠢᇄ"))
        else:
            logger.debug(bstack11l1l11_opy_ (u"ࠨࡎࡰࠢࡤࡧࡹ࡯ࡶࡦࠢࡳࡥ࡬࡫ࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠤᇅ"))
    def start_suite(self, name, attrs):
        bstack11l1l11_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࡥࡥࠢࡥࡽࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡸࡪࡨࡲࠥࡧࠠࡴࡷ࡬ࡸࡪࠦࡳࡵࡣࡵࡸࡸࠨࠢࠣᇆ")
        logger.debug(bstack11l1l11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡷ࡬ࡸࡪࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡵࡸ࡭ࡹ࡫࠺ࠡࡽࡱࡥࡲ࡫ࡽࠣᇇ").format(name=name))
    def end_suite(self, name, attrs):
        bstack11l1l11_opy_ (u"ࠤࠥࠦࡈࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡺ࡬ࡪࡴࠠࡢࠢࡶࡹ࡮ࡺࡥࠡࡧࡱࡨࡸࠨࠢࠣᇈ")
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡩࡳࡪ࡟ࡴࡷ࡬ࡸࡪࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡵࡸ࡭ࡹ࡫࠺ࠡࡽࡱࡥࡲ࡫ࡽࠣᇉ").format(name=name))
    def start_keyword(self, name, attrs):
        bstack11l1l11_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡧ࡫ࡦࡰࡴࡨࠤࡦࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡦࡺࡨࡧࡺࡺࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡒࡧࡲ࡬ࡵࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡥࡳࡿࠠࡤ࡮ࡲࡷࡪࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡦࡺࡨࡧࡺࡺࡥࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠬࡼ࡮ࡩ࡭ࡧࠣࡴࡦ࡭ࡥࠡ࡫ࡶࠤࡸࡺࡩ࡭࡮ࠣࡥࡨࡺࡩࡷࡧࠬࠤࡴࡸࠠࡣࡧࡩࡳࡷ࡫ࠠࡵࡧࡤࡶࡩࡵࡷ࡯ࠢࡥࡩ࡬࡯࡮ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᇊ")
        if self._1lll1l1l1l1_opy_ or self._1lll1l11lll_opy_:
            return
        bstack1lll1l1111l_opy_ = False
        bstack1lll1ll11ll_opy_ = attrs.get(bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᇋ"), bstack11l1l11_opy_ (u"࠭ࠧᇌ")).lower()
        if name.lower() in self._1lll1ll11l1_opy_:
            bstack1lll1l1111l_opy_ = True
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡄ࡮ࡲࡷࡪࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࡿࡳࡧ࡭ࡦࡿ࠯ࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡢࡦࡨࡲࡶࡪࠦࡩࡵࠢࡨࡼࡪࡩࡵࡵࡧࡶࠦᇍ").format(name=name))
        elif bstack1lll1ll11ll_opy_ == bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᇎ"):
            bstack1lll1l1111l_opy_ = True
            logger.debug(bstack11l1l11_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬࠲ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡷࡩࡦࡸࡤࡰࡹࡱࠤࡪࡾࡥࡤࡷࡷࡩࡸࠨᇏ"))
        if bstack1lll1l1111l_opy_ and self._1lll1l11l11_opy_():
            self._1lll1l1lll1_opy_()
    def log_message(self, message):
        bstack11l1l11_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡶࡾࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡢࡲࡷࡹࡷ࡫ࡳࠡࡈࡄࡍࡑࠦ࡬ࡦࡸࡨࡰࠥࡳࡥࡴࡵࡤ࡫ࡪࡹࠠࡵࡱࠣࡹࡸ࡫ࠠࡢࡵࠣࡩࡷࡸ࡯ࡳࠢࡵࡩࡦࡹ࡯࡯࠮ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡸ࡯࡮ࡤࡧࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡦࡺࡴࡳࡵࠣࡨࡴ࡫ࡳ࡯ࠩࡷࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡺࡨࡦࠢࡨࡶࡷࡵࡲࠡ࡯ࡨࡷࡸࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᇐ")
        level = message.get(bstack11l1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᇑ"), bstack11l1l11_opy_ (u"ࠬ࠭ᇒ"))
        if level == bstack11l1l11_opy_ (u"࠭ࡆࡂࡋࡏࠫᇓ"):
            self._1lll1l111ll_opy_ = message.get(bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᇔ"), bstack11l1l11_opy_ (u"ࠨࠩᇕ"))
            logger.debug(bstack11l1l11_opy_ (u"ࠤࡆࡥࡵࡺࡵࡳࡧࡧࠤࡪࡸࡲࡰࡴࠣࡱࡪࡹࡳࡢࡩࡨ࠾ࠥࢁࡥࡳࡴࡲࡶࢂࠨᇖ").format(error=self._1lll1l111ll_opy_))