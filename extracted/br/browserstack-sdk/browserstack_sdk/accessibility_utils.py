# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࡙ࠣࡹ࡯࡬ࡪࡶ࡬ࡩࡸࠐࡔࡩ࡫ࡶࠤࡲࡵࡤࡶ࡮ࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡵࡵ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠍࡻ࡭࡫࡮ࠡࡷࡶ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࠥࡲࡩࡣࡴࡤࡶࡾࠦࡷࡪࡶ࡫ࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠯ࠌࠥࠦࠧ၆")
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def _1llllllllll_opy_():
    bstack1ll1lll_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧࠣࡳࡧࡰࡥࡤࡶࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷࠦ࡬ࡪࡤࡵࡥࡷࡿࠧࡴࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡙ࡴࡢࡶࡨ࠲ࠏࠦࠠࠡࠢࡘࡷࡪࡹࠠࡵࡪࡨࠤࡨࡵࡲࡳࡧࡦࡸࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡕࡷࡥࡹ࡫ࠠࡂࡒࡌࠤࡼ࡯ࡴࡩࠢࡢ࡫ࡪࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥࡤࡸࡦࡲ࡯ࡨࠪࠬࠤࡦࡴࡤࠡࡡࡪࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡴࡳ࡫ࡳࡰࡪࡺࠨࠪࠌࠣࠤࠥࠦࡴࡰࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵ࡮ࡼࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡫ࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩࠥࡵࡢ࡫ࡧࡦࡸ࠱ࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠠࡪࡨࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠍࠤࠥࠦࠠࠣࠤࠥ၇")
    try:
        from robot.libraries.BuiltIn import BuiltIn
        bstack1lllllllll1_opy_ = BuiltIn().get_library_instance(bstack1ll1lll_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࠫ၈"))
        if bstack1lllllllll1_opy_ and hasattr(bstack1lllllllll1_opy_, bstack1ll1lll_opy_ (u"ࠫࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡡࡶࡸࡦࡺࡥࠨ၉")):
            bstack1llllllll11_opy_ = bstack1lllllllll1_opy_._playwright_state
            if hasattr(bstack1llllllll11_opy_, bstack1ll1lll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡧࡴࡢ࡮ࡲ࡫ࠬ၊")) and hasattr(bstack1llllllll11_opy_, bstack1ll1lll_opy_ (u"࠭࡟ࡨࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡹࡸࡩࡱ࡮ࡨࡸࠬ။")):
                bstack1llllllll1l_opy_ = bstack1llllllll11_opy_._get_browser_catalog(False)
                _active_browser, _active_context, active_page = bstack1llllllll11_opy_._get_active_triplet(bstack1llllllll1l_opy_)
                return active_page
            else:
                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡠࡩࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡶࡡࡨࡧ࠽ࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡔࡶࡤࡸࡪࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࡵࠥ၌"))
                return None
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡡࡪࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣ၍").format(e=e))
    return None
class accessibility_utils:
    ROBOT_LIBRARY_SCOPE = bstack1ll1lll_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࠩ၎")
    def perform_scan(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ၏"), None):
                logger.debug(bstack1ll1lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡈࡒࡉࠡࡰࡲࡸࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦ࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠤၐ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠥၑ"))
                return None
            page = _1llllllllll_opy_()
            if not page:
                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡮ࡰࠢࡤࡧࡹ࡯ࡶࡦࠢࡳࡥ࡬࡫ࠢၒ"))
                return None
            result = cli.accessibility.perform_scan(page, bstack1ll1lll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࠨၓ"), bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧၔ"))
            logger.info(bstack1ll1lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡖࡧࡦࡴ࠺ࠡࡽࡵࡩࡸࡻ࡬ࡵࡿࠥၕ").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࡩࢂࠨၖ").format(e=e))
            return None
    def get_accessibility_results(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫၗ"), None):
                logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵ࠽ࠤࡈࡒࡉࠡࡰࡲࡸࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦ࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠤၘ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶ࠾ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠥၙ"))
                return None
            page = _1llllllllll_opy_()
            if not page:
                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷ࠿ࠦ࡮ࡰࠢࡤࡧࡹ࡯ࡶࡦࠢࡳࡥ࡬࡫ࠢၚ"))
                return None
            result = cli.accessibility.get_accessibility_results(page, bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧၛ"))
            logger.info(bstack1ll1lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵ࠽ࠤࢀࡸࡥࡴࡷ࡯ࡸࢂࠨၜ").format(result=__import__(bstack1ll1lll_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨၝ")).dumps(result, indent=2)))
            return result
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࡩࢂࠨၞ").format(e=e))
            return None
    def get_accessibility_results_summary(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬၟ"), None):
                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽ࠿ࠦࡃࡍࡋࠣࡲࡴࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠦၠ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࡀࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠧၡ"))
                return None
            page = _1llllllllll_opy_()
            if not page:
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡰࡲࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦࠤၢ"))
                return None
            result = cli.accessibility.get_accessibility_results_summary(page, bstack1ll1lll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨၣ"))
            logger.info(bstack1ll1lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡘࡻ࡭࡮ࡣࡵࡽ࠿ࠦࡻࡳࡧࡶࡹࡱࡺࡽࠣၤ").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࡪࢃࠢၥ").format(e=e))
            return None