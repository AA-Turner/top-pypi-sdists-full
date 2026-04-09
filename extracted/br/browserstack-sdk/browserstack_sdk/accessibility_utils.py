# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
bstack11ll11_opy_ (u"ࠤࠥࠦࠏࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤ࡚ࡺࡩ࡭࡫ࡷ࡭ࡪࡹࠊࡕࡪ࡬ࡷࠥࡳ࡯ࡥࡷ࡯ࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡹࠠࡶࡶ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠎࡼ࡮ࡥ࡯ࠢࡸࡷ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷࠦ࡬ࡪࡤࡵࡥࡷࡿࠠࡸ࡫ࡷ࡬ࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠰ࠍࠦࠧࠨၪ")
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def _1lllll11lll_opy_():
    bstack11ll11_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨࠤࡴࡨࡪࡦࡥࡷࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࠠ࡭࡫ࡥࡶࡦࡸࡹࠨࡵࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡓࡵࡣࡷࡩ࠳ࠐ࡙ࠠࠡࠢࠣࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡩ࡯ࡳࡴࡨࡧࡹࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡖࡸࡦࡺࡥࠡࡃࡓࡍࠥࡽࡩࡵࡪࠣࡣ࡬࡫ࡴࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡥࡹࡧ࡬ࡰࡩࠫ࠭ࠥࡧ࡮ࡥࠢࡢ࡫ࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡵࡴ࡬ࡴࡱ࡫ࡴࠩࠫࠍࠤࠥࠦࠠࡵࡱࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶ࡯ࡽࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡥࠡࡣࡦࡸ࡮ࡼࡥࠡࡲࡤ࡫ࡪࠦ࡯ࡣ࡬ࡨࡧࡹ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠎࠥࠦࠠࠡࠤࠥࠦၫ")
    try:
        from robot.libraries.BuiltIn import BuiltIn
        bstack1lllll11ll1_opy_ = BuiltIn().get_library_instance(bstack11ll11_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࠬၬ"))
        if bstack1lllll11ll1_opy_ and hasattr(bstack1lllll11ll1_opy_, bstack11ll11_opy_ (u"ࠬࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡢࡷࡹࡧࡴࡦࠩၭ")):
            bstack1lllll1l111_opy_ = bstack1lllll11ll1_opy_._playwright_state
            if hasattr(bstack1lllll1l111_opy_, bstack11ll11_opy_ (u"࠭࡟ࡨࡧࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩࡡࡵࡣ࡯ࡳ࡬࠭ၮ")) and hasattr(bstack1lllll1l111_opy_, bstack11ll11_opy_ (u"ࠧࡠࡩࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡺࡲࡪࡲ࡯ࡩࡹ࠭ၯ")):
                bstack1lllll1l11l_opy_ = bstack1lllll1l111_opy_._get_browser_catalog(False)
                _active_browser, _active_context, active_page = bstack1lllll1l111_opy_._get_active_triplet(bstack1lllll1l11l_opy_)
                return active_page
            else:
                logger.debug(bstack11ll11_opy_ (u"ࠣࡡࡪࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡕࡷࡥࡹ࡫ࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡱࡪࡺࡨࡰࡦࡶࠦၰ"))
                return None
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠤࡢ࡫ࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤၱ").format(e=e))
    return None
class accessibility_utils:
    ROBOT_LIBRARY_SCOPE = bstack11ll11_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࠪၲ")
    def perform_scan(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫၳ"), None):
                logger.debug(bstack11ll11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡉࡌࡊࠢࡱࡳࡹࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠥၴ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack11ll11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠦၵ"))
                return None
            page = _1lllll11lll_opy_()
            if not page:
                logger.debug(bstack11ll11_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡯ࡱࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥࠣၶ"))
                return None
            result = cli.accessibility.perform_scan(page, bstack11ll11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴࠢၷ"), bstack11ll11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨၸ"))
            logger.info(bstack11ll11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡗࡨࡧ࡮࠻ࠢࡾࡶࡪࡹࡵ࡭ࡶࢀࠦၹ").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack11ll11_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࡪࢃࠢၺ").format(e=e))
            return None
    def get_accessibility_results(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬၻ"), None):
                logger.debug(bstack11ll11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶ࠾ࠥࡉࡌࡊࠢࡱࡳࡹࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠥၼ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack11ll11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷ࠿ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠦၽ"))
                return None
            page = _1lllll11lll_opy_()
            if not page:
                logger.debug(bstack11ll11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡀࠠ࡯ࡱࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥࠣၾ"))
                return None
            result = cli.accessibility.get_accessibility_results(page, bstack11ll11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨၿ"))
            logger.info(bstack11ll11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶ࠾ࠥࢁࡲࡦࡵࡸࡰࡹࢃࠢႀ").format(result=__import__(bstack11ll11_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩႁ")).dumps(result, indent=2)))
            return result
        except Exception as e:
            logger.error(bstack11ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࡪࢃࠢႂ").format(e=e))
            return None
    def get_accessibility_results_summary(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ႃ"), None):
                logger.debug(bstack11ll11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࡀࠠࡄࡎࡌࠤࡳࡵࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠧႄ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack11ll11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠨႅ"))
                return None
            page = _1lllll11lll_opy_()
            if not page:
                logger.debug(bstack11ll11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡱࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧࠥႆ"))
                return None
            result = cli.accessibility.get_accessibility_results_summary(page, bstack11ll11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢႇ"))
            logger.info(bstack11ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷ࡙ࠥࡵ࡮࡯ࡤࡶࡾࡀࠠࡼࡴࡨࡷࡺࡲࡴࡾࠤႈ").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack11ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣႉ").format(e=e))
            return None