# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import json
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
logger = get_logger(__name__)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _1lll1l1llll_opy_ = {
        bstack11ll111_opy_ (u"ࠧࡤ࡮ࡲࡷࡪࠦࡢࡳࡱࡺࡷࡪࡸࠧᆎ"), bstack11ll111_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠠࡤࡱࡱࡸࡪࡾࡴࠨᆏ"), bstack11ll111_opy_ (u"ࠩࡦࡰࡴࡹࡥࠡࡲࡤ࡫ࡪ࠭ᆐ"),
        bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡲ࡯ࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵࠫᆑ"), bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡬ࡰࡵࡨࠤࡨࡵ࡮ࡵࡧࡻࡸࠬᆒ"), bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣ࡭ࡱࡶࡩࠥࡶࡡࡨࡧࠪᆓ"),
    }
    def __init__(self):
        self._1lll1l1l1l1_opy_ = None
        self._1lll1l111l1_opy_ = False
        self._1lll1l11l11_opy_ = False
        self._1lll1l11lll_opy_ = None
        self._1lll1l1l1ll_opy_ = None
    def _1lll1l1ll1l_opy_(self):
        if self._1lll1l1l1l1_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1lll1l1l1l1_opy_ = BuiltIn().get_library_instance(bstack11ll111_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࠧᆔ"))
            except Exception as e:
                logger.warning(bstack11ll111_opy_ (u"ࠢࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣ࡫ࡪࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠾ࠥࢁࡥࡾࠤᆕ").format(e=e))
        return self._1lll1l1l1l1_opy_
    def _1lll1l11111_opy_(self):
        try:
            bstack1lll1l11l1l_opy_ = self._1lll1l1ll1l_opy_()
            if bstack1lll1l11l1l_opy_ and hasattr(bstack1lll1l11l1l_opy_, bstack11ll111_opy_ (u"ࠨࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡥࡳࡵࡣࡷࡩࠬᆖ")):
                bstack1lll1ll1111_opy_ = bstack1lll1l11l1l_opy_._playwright_state._get_browser_catalog()
                for bstack1lll1l1ll11_opy_ in bstack1lll1ll1111_opy_:
                    contexts = bstack1lll1l1ll11_opy_.get(bstack11ll111_opy_ (u"ࠩࡦࡳࡳࡺࡥࡹࡶࡶࠫᆗ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack11ll111_opy_ (u"ࠪࡴࡦ࡭ࡥࡴࠩᆘ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡹ࡯ࡶࡦࠢࡳࡥ࡬࡫࠺ࠡࡽࡨࢁࠧᆙ").format(e=e))
            return False
    def _1lll1l1l11l_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1lll1ll11l1_opy_ = {
                bstack11ll111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᆚ"): action,
                bstack11ll111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᆛ"): arguments
            }
            executor_cmd = bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠪᆜ") + json.dumps(bstack1lll1ll11l1_opy_)
            arg_string = bstack11ll111_opy_ (u"ࠣࡣࡵ࡫ࡂࢁࡥࡹࡧࡦࡹࡹࡵࡲࡠࡥࡰࡨࢂࠨᆝ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack11ll111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴ࠱ࡉࡻࡧ࡬ࡶࡣࡷࡩࠥࡐࡡࡷࡣࡖࡧࡷ࡯ࡰࡵࠩᆞ"),
                None,
                bstack11ll111_opy_ (u"ࠪࡣࠥࡃ࠾ࠡࡽࢀࠫᆟ"),
                arg_string
            )
            logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡾࡥࡤࡷࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࡤࡧࡹ࡯࡯࡯ࡿ࠯ࠤࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥࢁࡲࡦࡵࡸࡰࡹࢃࠢᆠ").format(action=action, result=result))
            return True
        except Exception as e:
            logger.warning(bstack11ll111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡧࡻࡩࡨࡻࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀ࡫ࡽࠣᆡ").format(e=e))
    def _1lll1l1l111_opy_(self, status, reason=bstack11ll111_opy_ (u"ࠨࠢᆢ")):
        bstack11ll111_opy_ (u"ࠢࠣࠤࡐࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥࠦࠧᆣ")
        bstack1lll1l11ll1_opy_ = bstack11ll111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᆤ") if status == bstack11ll111_opy_ (u"ࠤࡓࡅࡘ࡙ࠢᆥ") else bstack11ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᆦ")
        if bstack1lll1l11ll1_opy_ == bstack11ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᆧ"):
            return self._1lll1l1l11l_opy_(bstack11ll111_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᆨ"), {
                bstack11ll111_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᆩ"): bstack1lll1l11ll1_opy_,
                bstack11ll111_opy_ (u"ࠢࡳࡧࡤࡷࡴࡴࠢᆪ"): reason
            })
        else:
            return self._1lll1l1l11l_opy_(bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᆫ"), {
                bstack11ll111_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᆬ"): bstack1lll1l11ll1_opy_
            })
    def _1lll1l1111l_opy_(self, name):
        bstack11ll111_opy_ (u"࡙ࠥࠦࠧࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥࠦࠧᆭ")
        return self._1lll1l1l11l_opy_(bstack11ll111_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᆮ"), {
            bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆯ"): name
        })
    def _1lll1l111ll_opy_(self):
        bstack11ll111_opy_ (u"ࠨࠢࠣࡏࡤࡶࡰࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡤࡨࡪࡴࡸࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡦࡰࡴࡹࡥࠡࡱࡵࠤࡹ࡫ࡡࡳࡦࡲࡻࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡷࡥࡹࡻࡳࠡ࡫ࡶࠤ࡮ࡴࡦࡦࡴࡵࡩࡩࠦࡦࡳࡱࡰࠤࡤࡲࡡࡴࡶࡢࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧ࠽ࠤ࡮࡬ࠠࡢࡰࡼࠤࡋࡇࡉࡍ࠯࡯ࡩࡻ࡫࡬ࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡣࡶࠤࡨࡧࡰࡵࡷࡵࡩࡩࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡸࡪࡹࡴ࠭ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡮ࡹࠠࡧࡣ࡬ࡰ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᆰ")
        if self._1lll1l11l11_opy_:
            return
        try:
            global_config = Config.get_instance()
            if self._1lll1l11lll_opy_ and not global_config.should_skip_session_name():
                self._1lll1l1111l_opy_(self._1lll1l11lll_opy_)
            status = bstack11ll111_opy_ (u"ࠧࡇࡃࡌࡐࠬᆱ") if self._1lll1l1l1ll_opy_ else bstack11ll111_opy_ (u"ࠨࡒࡄࡗࡘ࠭ᆲ")
            message = self._1lll1l1l1ll_opy_ or bstack11ll111_opy_ (u"ࠩࠪᆳ")
            if not global_config.should_skip_session_status():
                logger.debug(bstack11ll111_opy_ (u"ࠥࡑࡦࡸ࡫ࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡨࡥࡧࡱࡵࡩࠥࡩ࡬ࡰࡵࡨ࠾ࠥࡹࡴࡢࡶࡸࡷࡂࢁࡳࡵࡣࡷࡹࡸࢃࠬࠡ࡯ࡨࡷࡸࡧࡧࡦ࠿ࡾࡱࡪࡹࡳࡢࡩࡨࢁࠧᆴ").format(status=status, message=message))
                self._1lll1l1l111_opy_(status, message)
            self._1lll1l11l11_opy_ = True
            logger.debug(bstack11ll111_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡱࡦࡸ࡫ࡦࡦࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᆵ"))
        except Exception as e:
            logger.error(bstack11ll111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࡨࢁࠧᆶ").format(e=e))
    def start_test(self, name, attrs):
        logger.debug(bstack11ll111_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡺࡥࡴࡶࠣࡇࡆࡒࡌࡆࡆࠣ࠱ࠥࡺࡥࡴࡶ࠽ࠤࢀࡴࡡ࡮ࡧࢀࠦᆷ").format(name=name))
        self._1lll1l111l1_opy_ = False
        self._1lll1l11l11_opy_ = False
        self._1lll1l11lll_opy_ = name
        self._1lll1l1l1ll_opy_ = None
    def end_test(self, name, attrs):
        status = attrs.get(bstack11ll111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᆸ"), bstack11ll111_opy_ (u"ࠨࡗࡑࡏࡓࡕࡗࡏࠩᆹ"))
        message = attrs.get(bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᆺ"), bstack11ll111_opy_ (u"ࠪࠫᆻ"))
        logger.debug(bstack11ll111_opy_ (u"ࠦࡪࡴࡤࡠࡶࡨࡷࡹࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡶࡨࡷࡹࡀࠠࡼࡰࡤࡱࡪࢃࠬࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࡷࡹࡧࡴࡶࡵࢀࠦᆼ").format(name=name, status=status))
        self._1lll1l111l1_opy_ = True
        if not self._1lll1l11l11_opy_ and self._1lll1l11111_opy_():
            try:
                global_config = Config.get_instance()
                if not global_config.should_skip_session_name():
                    self._1lll1l1111l_opy_(name)
                if not global_config.should_skip_session_status():
                    logger.debug(bstack11ll111_opy_ (u"ࠧࡓࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡰࠣࡩࡳࡪ࡟ࡵࡧࡶࡸ࠿ࠦࡳࡵࡣࡷࡹࡸࡃࡻࡴࡶࡤࡸࡺࡹࡽࠣᆽ").format(status=status))
                    self._1lll1l1l111_opy_(status, message)
                self._1lll1l11l11_opy_ = True
                logger.debug(bstack11ll111_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡳࡡࡳ࡭ࡨࡨࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᆾ"))
            except Exception as e:
                logger.error(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡲࠥ࡫࡮ࡥࡡࡷࡩࡸࡺ࠺ࠡࡽࡨࢁࠧᆿ").format(e=e))
        elif self._1lll1l11l11_opy_:
            logger.debug(bstack11ll111_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡱࡦࡸ࡫ࡦࡦࠥᇀ"))
        else:
            logger.debug(bstack11ll111_opy_ (u"ࠤࡑࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡷࡪࡹࡳࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠧᇁ"))
    def start_suite(self, name, attrs):
        bstack11ll111_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡻ࡭࡫࡮ࠡࡣࠣࡷࡺ࡯ࡴࡦࠢࡶࡸࡦࡸࡴࡴࠤࠥࠦᇂ")
        logger.debug(bstack11ll111_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡺ࡯ࡴࡦࠢࡆࡅࡑࡒࡅࡅࠢ࠰ࠤࡸࡻࡩࡵࡧ࠽ࠤࢀࡴࡡ࡮ࡧࢀࠦᇃ").format(name=name))
    def end_suite(self, name, attrs):
        bstack11ll111_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡽࡨࡦࡰࠣࡥࠥࡹࡵࡪࡶࡨࠤࡪࡴࡤࡴࠤࠥࠦᇄ")
        logger.debug(bstack11ll111_opy_ (u"ࠨࡥ࡯ࡦࡢࡷࡺ࡯ࡴࡦࠢࡆࡅࡑࡒࡅࡅࠢ࠰ࠤࡸࡻࡩࡵࡧ࠽ࠤࢀࡴࡡ࡮ࡧࢀࠦᇅ").format(name=name))
    def start_keyword(self, name, attrs):
        bstack11ll111_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࡥࡥࠢࡥࡽࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡣࡧࡩࡳࡷ࡫ࠠࡢࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣࡩࡽ࡫ࡣࡶࡶࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡎࡣࡵ࡯ࡸࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡢࡦࡨࡲࡶࡪࠦࡡ࡯ࡻࠣࡧࡱࡵࡳࡦࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣࡩࡽ࡫ࡣࡶࡶࡨࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠨࡸࡪ࡬ࡰࡪࠦࡰࡢࡩࡨࠤ࡮ࡹࠠࡴࡶ࡬ࡰࡱࠦࡡࡤࡶ࡬ࡺࡪ࠯ࠠࡰࡴࠣࡦࡪ࡬࡯ࡳࡧࠣࡸࡪࡧࡲࡥࡱࡺࡲࠥࡨࡥࡨ࡫ࡱࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᇆ")
        if self._1lll1l11l11_opy_ or self._1lll1l111l1_opy_:
            return
        bstack1lll1ll111l_opy_ = False
        bstack1lll1l1lll1_opy_ = attrs.get(bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᇇ"), bstack11ll111_opy_ (u"ࠩࠪᇈ")).lower()
        if name.lower() in self._1lll1l1llll_opy_:
            bstack1lll1ll111l_opy_ = True
            logger.debug(bstack11ll111_opy_ (u"ࠥࡇࡱࡵࡳࡦࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣࡨࡪࡺࡥࡤࡶࡨࡨ࠿ࠦࡻ࡯ࡣࡰࡩࢂ࠲ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢ࡬ࡸࠥ࡫ࡸࡦࡥࡸࡸࡪࡹࠢᇉ").format(name=name))
        elif bstack1lll1l1lll1_opy_ == bstack11ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᇊ"):
            bstack1lll1ll111l_opy_ = True
            logger.debug(bstack11ll111_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨ࠮ࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡨࡥࡧࡱࡵࡩࠥࡺࡥࡢࡴࡧࡳࡼࡴࠠࡦࡺࡨࡧࡺࡺࡥࡴࠤᇋ"))
        if bstack1lll1ll111l_opy_ and self._1lll1l11111_opy_():
            self._1lll1l111ll_opy_()
    def log_message(self, message):
        bstack11ll111_opy_ (u"ࠨࠢࠣࡅࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡦࡰࡴࠣࡩࡻ࡫ࡲࡺࠢ࡯ࡳ࡬ࠦ࡭ࡦࡵࡶࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡥࡵࡺࡵࡳࡧࡶࠤࡋࡇࡉࡍࠢ࡯ࡩࡻ࡫࡬ࠡ࡯ࡨࡷࡸࡧࡧࡦࡵࠣࡸࡴࠦࡵࡴࡧࠣࡥࡸࠦࡥࡳࡴࡲࡶࠥࡸࡥࡢࡵࡲࡲ࠱ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡴ࡫ࡱࡧࡪࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡢࡶࡷࡶࡸࠦࡤࡰࡧࡶࡲࠬࡺࠠࡪࡰࡦࡰࡺࡪࡥࠡࡶ࡫ࡩࠥ࡫ࡲࡳࡱࡵࠤࡲ࡫ࡳࡴࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᇌ")
        level = message.get(bstack11ll111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᇍ"), bstack11ll111_opy_ (u"ࠨࠩᇎ"))
        if level == bstack11ll111_opy_ (u"ࠩࡉࡅࡎࡒࠧᇏ"):
            self._1lll1l1l1ll_opy_ = message.get(bstack11ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᇐ"), bstack11ll111_opy_ (u"ࠫࠬᇑ"))
            logger.debug(bstack11ll111_opy_ (u"ࠧࡉࡡࡱࡶࡸࡶࡪࡪࠠࡦࡴࡵࡳࡷࠦ࡭ࡦࡵࡶࡥ࡬࡫࠺ࠡࡽࡨࡶࡷࡵࡲࡾࠤᇒ").format(error=self._1lll1l1l1ll_opy_))