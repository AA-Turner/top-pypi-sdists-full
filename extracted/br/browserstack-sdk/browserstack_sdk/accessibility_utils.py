# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
bstack1l1llll_opy_ (u"ࠥࠦࠧࠐࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡛ࠥࡴࡪ࡮࡬ࡸ࡮࡫ࡳࠋࡖ࡫࡭ࡸࠦ࡭ࡰࡦࡸࡰࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡳࠡࡷࡷ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠏࡽࡨࡦࡰࠣࡹࡸ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࠠ࡭࡫ࡥࡶࡦࡸࡹࠡࡹ࡬ࡸ࡭ࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠱ࠎࠧࠨࠢࡶ")
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def _1lllllll_opy_():
    bstack1l1llll_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩࠥࡵࡢ࡫ࡧࡦࡸࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠩࡶࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡔࡶࡤࡸࡪ࠴ࠊࠡࠢࠣࠤ࡚ࡹࡥࡴࠢࡷ࡬ࡪࠦࡣࡰࡴࡵࡩࡨࡺࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡗࡹࡧࡴࡦࠢࡄࡔࡎࠦࡷࡪࡶ࡫ࠤࡤ࡭ࡥࡵࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡦࡺࡡ࡭ࡱࡪࠬ࠮ࠦࡡ࡯ࡦࠣࡣ࡬࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡶࡵ࡭ࡵࡲࡥࡵࠪࠬࠎࠥࠦࠠࠡࡶࡲࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࡰࡾࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡦࠢࡤࡧࡹ࡯ࡶࡦࠢࡳࡥ࡬࡫ࠠࡰࡤ࡭ࡩࡨࡺࠬࠡࡱࡵࠤࡓࡵ࡮ࡦࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠏࠦࠠࠡࠢࠥࠦࠧࡷ")
    try:
        from robot.libraries.BuiltIn import BuiltIn
        bstack1llllll1_opy_ = BuiltIn().get_library_instance(bstack1l1llll_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࠭ࡸ"))
        if bstack1llllll1_opy_ and hasattr(bstack1llllll1_opy_, bstack1l1llll_opy_ (u"࠭࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡣࡸࡺࡡࡵࡧࠪࡹ")):
            bstack1lllll1l_opy_ = bstack1llllll1_opy_._playwright_state
            if hasattr(bstack1lllll1l_opy_, bstack1l1llll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣࡢࡶࡤࡰࡴ࡭ࠧࡺ")) and hasattr(bstack1lllll1l_opy_, bstack1l1llll_opy_ (u"ࠨࡡࡪࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡴࡳ࡫ࡳࡰࡪࡺࠧࡻ")):
                bstack1lllll11_opy_ = bstack1lllll1l_opy_._get_browser_catalog(False)
                _active_browser, _active_context, active_page = bstack1lllll1l_opy_._get_active_triplet(bstack1lllll11_opy_)
                return active_page
            else:
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡢ࡫ࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡖࡸࡦࡺࡥࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡵࡩࡶࡻࡩࡳࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࡷࠧࡼ"))
                return None
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡣ࡬࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡲࡤ࡫ࡪࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡦࡿࠥࡽ").format(e=e))
    return None
class accessibility_utils:
    ROBOT_LIBRARY_SCOPE = bstack1l1llll_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࠫࡾ")
    def perform_scan(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬࡿ"), None):
                logger.debug(bstack1l1llll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡃࡍࡋࠣࡲࡴࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠦࢀ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠧࢁ"))
                return None
            page = _1lllllll_opy_()
            if not page:
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡰࡲࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦࠤࢂ"))
                return None
            result = cli.accessibility.perform_scan(page, bstack1l1llll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣࢃ"), bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࢄ"))
            logger.info(bstack1l1llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡘࡩࡡ࡯࠼ࠣࡿࡷ࡫ࡳࡶ࡮ࡷࢁࠧࢅ").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣࢆ").format(e=e))
            return None
    def get_accessibility_results(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ࢇ"), None):
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷ࠿ࠦࡃࡍࡋࠣࡲࡴࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠦ࢈"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡀࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠧࢉ"))
                return None
            page = _1lllllll_opy_()
            if not page:
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࠺ࠡࡰࡲࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦࠤࢊ"))
                return None
            result = cli.accessibility.get_accessibility_results(page, bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࢋ"))
            logger.info(bstack1l1llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷ࠿ࠦࡻࡳࡧࡶࡹࡱࡺࡽࠣࢌ").format(result=__import__(bstack1l1llll_opy_ (u"ࠬࡰࡳࡰࡰࠪࢍ")).dumps(result, indent=2)))
            return result
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣࢎ").format(e=e))
            return None
    def get_accessibility_results_summary(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ࢏"), None):
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡅࡏࡍࠥࡴ࡯ࡵࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠨ࢐"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠢ࢑"))
                return None
            page = _1lllllll_opy_()
            if not page:
                logger.debug(bstack1l1llll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺ࠼ࠣࡲࡴࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨࠦ࢒"))
                return None
            result = cli.accessibility.get_accessibility_results_summary(page, bstack1l1llll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ࢓"))
            logger.info(bstack1l1llll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡓࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡽࡵࡩࡸࡻ࡬ࡵࡿࠥ࢔").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤ࢕").format(e=e))
            return None