# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡘࡸ࡮ࡲࡩࡵ࡫ࡨࡷࠏ࡚ࡨࡪࡵࠣࡱࡴࡪࡵ࡭ࡧࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥࡻࡴࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠌࡺ࡬ࡪࡴࠠࡶࡵ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࠤࡱ࡯ࡢࡳࡣࡵࡽࠥࡽࡩࡵࡪࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠮ࠋࠤࠥࠦှ")
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def _1111111l1l_opy_():
    bstack1ll1lll_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦࠢࡲࡦ࡯࡫ࡣࡵࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࠥࡲࡩࡣࡴࡤࡶࡾ࠭ࡳࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡘࡺࡡࡵࡧ࠱ࠎࠥࠦࠠࠡࡗࡶࡩࡸࠦࡴࡩࡧࠣࡧࡴࡸࡲࡦࡥࡷࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡔࡶࡤࡸࡪࠦࡁࡑࡋࠣࡻ࡮ࡺࡨࠡࡡࡪࡩࡹࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤࡣࡷࡥࡱࡵࡧࠩࠫࠣࡥࡳࡪࠠࡠࡩࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡺࡲࡪࡲ࡯ࡩࡹ࠮ࠩࠋࠢࠣࠤࠥࡺ࡯ࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴ࡭ࡻࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡪࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨࠤࡴࡨࡪࡦࡥࡷ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠌࠣࠤࠥࠦࠢࠣࠤဿ")
    try:
        from robot.libraries.BuiltIn import BuiltIn
        bstack11111111ll_opy_ = BuiltIn().get_library_instance(bstack1ll1lll_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࠪ၀"))
        if bstack11111111ll_opy_ and hasattr(bstack11111111ll_opy_, bstack1ll1lll_opy_ (u"ࠪࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡠࡵࡷࡥࡹ࡫ࠧ၁")):
            bstack1111111l11_opy_ = bstack11111111ll_opy_._playwright_state
            if hasattr(bstack1111111l11_opy_, bstack1ll1lll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡦࡺࡡ࡭ࡱࡪࠫ၂")) and hasattr(bstack1111111l11_opy_, bstack1ll1lll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡸࡷ࡯ࡰ࡭ࡧࡷࠫ၃")):
                bstack11111111l1_opy_ = bstack1111111l11_opy_._get_browser_catalog(False)
                _active_browser, _active_context, active_page = bstack1111111l11_opy_._get_active_triplet(bstack11111111l1_opy_)
                return active_page
            else:
                logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡟ࡨࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡵࡧࡧࡦ࠼ࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡓࡵࡣࡷࡩࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࡴࠤ၄"))
                return None
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡠࡩࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡶࡡࡨࡧࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࡪࢃࠢ၅").format(e=e))
    return None
class accessibility_utils:
    ROBOT_LIBRARY_SCOPE = bstack1ll1lll_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࠨ၆")
    def perform_scan(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ၇"), None):
                logger.debug(bstack1ll1lll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡇࡑࡏࠠ࡯ࡱࡷࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠣ၈"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1ll1lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠤ၉"))
                return None
            page = _1111111l1l_opy_()
            if not page:
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡴ࡯ࠡࡣࡦࡸ࡮ࡼࡥࠡࡲࡤ࡫ࡪࠨ၊"))
                return None
            result = cli.accessibility.perform_scan(page, bstack1ll1lll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲࠧ။"), bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ၌"))
            logger.info(bstack1ll1lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡕࡦࡥࡳࡀࠠࡼࡴࡨࡷࡺࡲࡴࡾࠤ၍").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࡨࢁࠧ၎").format(e=e))
            return None
    def get_accessibility_results(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ၏"), None):
                logger.debug(bstack1ll1lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴ࠼ࠣࡇࡑࡏࠠ࡯ࡱࡷࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠣၐ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵ࠽ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠤၑ"))
                return None
            page = _1111111l1l_opy_()
            if not page:
                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶ࠾ࠥࡴ࡯ࠡࡣࡦࡸ࡮ࡼࡥࠡࡲࡤ࡫ࡪࠨၒ"))
                return None
            result = cli.accessibility.get_accessibility_results(page, bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦၓ"))
            logger.info(bstack1ll1lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴ࠼ࠣࡿࡷ࡫ࡳࡶ࡮ࡷࢁࠧၔ").format(result=__import__(bstack1ll1lll_opy_ (u"ࠩ࡭ࡷࡴࡴࠧၕ")).dumps(result, indent=2)))
            return result
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࡨࢁࠧၖ").format(e=e))
            return None
    def get_accessibility_results_summary(self):
        try:
            from browserstack_sdk.sdk_cli.cli import cli
            if not cli.is_running() or not getattr(cli, bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫၗ"), None):
                logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼ࠾ࠥࡉࡌࡊࠢࡱࡳࡹࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠥၘ"))
                return None
            if not cli.accessibility.accessibility:
                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽ࠿ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠦၙ"))
                return None
            page = _1111111l1l_opy_()
            if not page:
                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࡀࠠ࡯ࡱࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥࠣၚ"))
                return None
            result = cli.accessibility.get_accessibility_results_summary(page, bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧၛ"))
            logger.info(bstack1ll1lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡗࡺࡳ࡭ࡢࡴࡼ࠾ࠥࢁࡲࡦࡵࡸࡰࡹࢃࠢၜ").format(result=result))
            return result
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࡩࢂࠨၝ").format(e=e))
            return None