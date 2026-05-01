# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
bstack111ll_opy_ (u"ࠦࠧࠨࠊࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡕࡵ࡫࡯࡭ࡹ࡯ࡥࡴࠌࡗ࡬࡮ࡹࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࡴࠢࡸࡸ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠐࡷࡩࡧࡱࠤࡺࡹࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢࡺ࡭ࡹ࡮ࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠲ࠏࠨࠢࠣႏ")
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def _1lllll1111l_opy_():
    bstack111ll_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡣࡦࡸ࡮ࡼࡥࠡࡲࡤ࡫ࡪࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࠢ࡯࡭ࡧࡸࡡࡳࡻࠪࡷࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡕࡷࡥࡹ࡫࠮ࠋࠢࠣࠤ࡛ࠥࡳࡦࡵࠣࡸ࡭࡫ࠠࡤࡱࡵࡶࡪࡩࡴࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡘࡺࡡࡵࡧࠣࡅࡕࡏࠠࡸ࡫ࡷ࡬ࠥࡥࡧࡦࡶࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡧࡴࡢ࡮ࡲ࡫࠭࠯ࠠࡢࡰࡧࠤࡤ࡭ࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡷࡶ࡮ࡶ࡬ࡦࡶࠫ࠭ࠏࠦࠠࠡࠢࡷࡳࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࡱࡿࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡧࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥࠡࡱࡥ࡮ࡪࡩࡴ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠐࠠࠡࠢࠣࠦࠧࠨ႐")
    try:
        from robot.libraries.BuiltIn import BuiltIn
        bstack1lllll111l1_opy_ = BuiltIn().get_library_instance(bstack111ll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࠧ႑"))
        if bstack1lllll111l1_opy_ and hasattr(bstack1lllll111l1_opy_, bstack111ll_opy_ (u"ࠧࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡤࡹࡴࡢࡶࡨࠫ႒")):
            bstack1llll1lllll_opy_ = bstack1lllll111l1_opy_._playwright_state
            if hasattr(bstack1llll1lllll_opy_, bstack111ll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤࡣࡷࡥࡱࡵࡧࠨ႓")) and hasattr(bstack1llll1lllll_opy_, bstack111ll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡵࡴ࡬ࡴࡱ࡫ࡴࠨ႔")):
                bstack1lllll11111_opy_ = bstack1llll1lllll_opy_._get_browser_catalog(False)
                _active_browser, _active_context, active_page = bstack1llll1lllll_opy_._get_active_triplet(bstack1lllll11111_opy_)
                return active_page
            else:
                logger.debug(bstack111ll_opy_ (u"ࠥࡣ࡬࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡲࡤ࡫ࡪࡀࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡗࡹࡧࡴࡦࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡶࡪࡷࡵࡪࡴࡨࡨࠥࡳࡥࡵࡪࡲࡨࡸࠨ႕"))
                return None
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠦࡤ࡭ࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡳࡥ࡬࡫ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡧࢀࠦ႖").format(e=e))
    return None
class accessibility_utils:
    ROBOT_LIBRARY_SCOPE = bstack111ll_opy_ (u"ࠬࡍࡌࡐࡄࡄࡐࠬ႗")
    def perform_scan(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭႘"), None):
                logger.debug(bstack111ll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡄࡎࡌࠤࡳࡵࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠧ႙"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack111ll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠨႚ"))
                return None
            page = _1lllll1111l_opy_()
            if not page:
                logger.debug(bstack111ll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡱࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧࠥႛ"))
                return None
            result = cli.accessibility.perform_scan(page, bstack111ll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠤႜ"), bstack111ll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣႝ"))
            logger.info(bstack111ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࠥࡣࡢࡰ࠽ࠤࢀࡸࡥࡴࡷ࡯ࡸࢂࠨ႞").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤ႟").format(e=e))
            return None
    def get_accessibility_results(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧႠ"), None):
                logger.debug(bstack111ll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡀࠠࡄࡎࡌࠤࡳࡵࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠧႡ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack111ll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࠺ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠨႢ"))
                return None
            page = _1lllll1111l_opy_()
            if not page:
                logger.debug(bstack111ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡱࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧࠥႣ"))
                return None
            result = cli.accessibility.get_accessibility_results(page, bstack111ll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣႤ"))
            logger.info(bstack111ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࡀࠠࡼࡴࡨࡷࡺࡲࡴࡾࠤႥ").format(result=__import__(bstack111ll_opy_ (u"࠭ࡪࡴࡱࡱࠫႦ")).dumps(result, indent=2)))
            return result
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤႧ").format(e=e))
            return None
    def get_accessibility_results_summary(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨႨ"), None):
                logger.debug(bstack111ll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡆࡐࡎࠦ࡮ࡰࡶࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠢႩ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack111ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺ࠼ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠣႪ"))
                return None
            page = _1lllll1111l_opy_()
            if not page:
                logger.debug(bstack111ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡳࡵࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩࠧႫ"))
                return None
            result = cli.accessibility.get_accessibility_results_summary(page, bstack111ll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤႬ"))
            logger.info(bstack111ll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡔࡷࡰࡱࡦࡸࡹ࠻ࠢࡾࡶࡪࡹࡵ࡭ࡶࢀࠦႭ").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡦࡿࠥႮ").format(e=e))
            return None