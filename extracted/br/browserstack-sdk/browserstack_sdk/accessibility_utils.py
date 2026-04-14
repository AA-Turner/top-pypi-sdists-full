# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
bstack1l111l_opy_ (u"ࠦࠧࠨࠊࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡕࡵ࡫࡯࡭ࡹ࡯ࡥࡴࠌࡗ࡬࡮ࡹࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࡴࠢࡸࡸ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠐࡷࡩࡧࡱࠤࡺࡹࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢࡺ࡭ࡹ࡮ࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠲ࠏࠨࠢࠣႁ")
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def _1lllll111ll_opy_():
    bstack1l111l_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡣࡦࡸ࡮ࡼࡥࠡࡲࡤ࡫ࡪࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࠢ࡯࡭ࡧࡸࡡࡳࡻࠪࡷࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡕࡷࡥࡹ࡫࠮ࠋࠢࠣࠤ࡛ࠥࡳࡦࡵࠣࡸ࡭࡫ࠠࡤࡱࡵࡶࡪࡩࡴࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡘࡺࡡࡵࡧࠣࡅࡕࡏࠠࡸ࡫ࡷ࡬ࠥࡥࡧࡦࡶࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡧࡴࡢ࡮ࡲ࡫࠭࠯ࠠࡢࡰࡧࠤࡤ࡭ࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡷࡶ࡮ࡶ࡬ࡦࡶࠫ࠭ࠏࠦࠠࠡࠢࡷࡳࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࡱࡿࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡧࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥࠡࡱࡥ࡮ࡪࡩࡴ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠐࠠࠡࠢࠣࠦࠧࠨႂ")
    try:
        from robot.libraries.BuiltIn import BuiltIn
        bstack1lllll11ll1_opy_ = BuiltIn().get_library_instance(bstack1l111l_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࠧႃ"))
        if bstack1lllll11ll1_opy_ and hasattr(bstack1lllll11ll1_opy_, bstack1l111l_opy_ (u"ࠧࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡤࡹࡴࡢࡶࡨࠫႄ")):
            bstack1lllll11l11_opy_ = bstack1lllll11ll1_opy_._playwright_state
            if hasattr(bstack1lllll11l11_opy_, bstack1l111l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤࡣࡷࡥࡱࡵࡧࠨႅ")) and hasattr(bstack1lllll11l11_opy_, bstack1l111l_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡵࡴ࡬ࡴࡱ࡫ࡴࠨႆ")):
                bstack1lllll11l1l_opy_ = bstack1lllll11l11_opy_._get_browser_catalog(False)
                _active_browser, _active_context, active_page = bstack1lllll11l11_opy_._get_active_triplet(bstack1lllll11l1l_opy_)
                return active_page
            else:
                logger.debug(bstack1l111l_opy_ (u"ࠥࡣ࡬࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡲࡤ࡫ࡪࡀࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡗࡹࡧࡴࡦࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡶࡪࡷࡵࡪࡴࡨࡨࠥࡳࡥࡵࡪࡲࡨࡸࠨႇ"))
                return None
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠦࡤ࡭ࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡳࡥ࡬࡫ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡧࢀࠦႈ").format(e=e))
    return None
class accessibility_utils:
    ROBOT_LIBRARY_SCOPE = bstack1l111l_opy_ (u"ࠬࡍࡌࡐࡄࡄࡐࠬႉ")
    def perform_scan(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1l111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ႊ"), None):
                logger.debug(bstack1l111l_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡄࡎࡌࠤࡳࡵࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠧႋ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1l111l_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠨႌ"))
                return None
            page = _1lllll111ll_opy_()
            if not page:
                logger.debug(bstack1l111l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡱࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧႍࠥ"))
                return None
            result = cli.accessibility.perform_scan(page, bstack1l111l_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠤႎ"), bstack1l111l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣႏ"))
            logger.info(bstack1l111l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࠥࡣࡢࡰ࠽ࠤࢀࡸࡥࡴࡷ࡯ࡸࢂࠨ႐").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack1l111l_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤ႑").format(e=e))
            return None
    def get_accessibility_results(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ႒"), None):
                logger.debug(bstack1l111l_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡀࠠࡄࡎࡌࠤࡳࡵࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠧ႓"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1l111l_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࠺ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠨ႔"))
                return None
            page = _1lllll111ll_opy_()
            if not page:
                logger.debug(bstack1l111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡱࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧࠥ႕"))
                return None
            result = cli.accessibility.get_accessibility_results(page, bstack1l111l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ႖"))
            logger.info(bstack1l111l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࡀࠠࡼࡴࡨࡷࡺࡲࡴࡾࠤ႗").format(result=__import__(bstack1l111l_opy_ (u"࠭ࡪࡴࡱࡱࠫ႘")).dumps(result, indent=2)))
            return result
        except Exception as e:
            logger.error(bstack1l111l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤ႙").format(e=e))
            return None
    def get_accessibility_results_summary(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1l111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨႚ"), None):
                logger.debug(bstack1l111l_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡆࡐࡎࠦ࡮ࡰࡶࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠢႛ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1l111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺ࠼ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠣႜ"))
                return None
            page = _1lllll111ll_opy_()
            if not page:
                logger.debug(bstack1l111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡳࡵࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩࠧႝ"))
                return None
            result = cli.accessibility.get_accessibility_results_summary(page, bstack1l111l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ႞"))
            logger.info(bstack1l111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡔࡷࡰࡱࡦࡸࡹ࠻ࠢࡾࡶࡪࡹࡵ࡭ࡶࢀࠦ႟").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack1l111l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡦࡿࠥႠ").format(e=e))
            return None