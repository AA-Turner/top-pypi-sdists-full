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
bstack11l1l11_opy_ (u"ࠤࠥࠦࠏࡒ࡯ࡢࡦࠣࡘࡪࡹࡴࡪࡰࡪࠤࡒࡵࡤࡶ࡮ࡨࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠎࡍࡧ࡮ࡥ࡮ࡨࡷࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡤࡼࠤࡩ࡫࡬ࡦࡩࡤࡸ࡮ࡴࡧࠡࡶࡲࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠏࠨࠢࠣს")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1lllll1ll11_opy_,
    get_cli_dir,
    bstack1llllll11l1_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1llllll1l11_opy_(config):
    bstack11l1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡉࡽࡺࡲࡢࡥࡷࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡴࡩࠢࡩࡶࡴࡳࠠࡤࡱࡰࡱࡦࡴࡤ࠮࡮࡬ࡲࡪࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࡲࡶࠥࡩ࡯࡯ࡨ࡬࡫࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡦࡪࡩ࠽ࠤ࡙࡮ࡥࠡࡕࡇࡏࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡶࡸࡷࡀࠠࡑࡣࡷ࡬ࠥࡺ࡯ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠧࠨࠢტ")
    try:
        if bstack11l1l11_opy_ (u"ࠫ࠲࠳ࡣࡰࡰࡩ࡭࡬࠭უ") in sys.argv:
            bstack1lllll1lll1_opy_ = sys.argv.index(bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡤࡱࡱࡪ࡮࡭ࠧფ"))
            if bstack1lllll1lll1_opy_ + 1 < len(sys.argv):
                bstack1llllll111l_opy_ = sys.argv[bstack1lllll1lll1_opy_ + 1]
                logger.debug(bstack11l1l11_opy_ (u"ࠨࡆࡰࡷࡱࡨࠥ࠳࠭ࡤࡱࡱࡪ࡮࡭ࠠࡧ࡮ࡤ࡫ࠥࡽࡩࡵࡪࠣࡴࡦࡺࡨ࠻ࠢࡾࢁࠧქ").format(bstack1llllll111l_opy_))
                return bstack1llllll111l_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠢࡩࡰࡦ࡭࠺ࠡࡽࢀࠦღ").format(e))
        pass
    bstack1llllll111l_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬყ"))
    if bstack1llllll111l_opy_:
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡉࡳࡺࡴࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡲࡤࡸ࡭ࠦࡩ࡯ࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠺ࠡࡽࢀࠦშ").format(bstack1llllll111l_opy_))
        return bstack1llllll111l_opy_
    return None
def bstack1lllll1ll1l_opy_(config):
    bstack11l1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡉࡽࡺࡲࡢࡥࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡧࡷ࡫ࡤࡦࡰࡷ࡭ࡦࡲࡳࠡࡨࡵࡳࡲࠦࡶࡢࡴ࡬ࡳࡺࡹࠠࡴࡱࡸࡶࡨ࡫ࡳ࠯ࠌࠣࠤࠥࠦࡐࡳ࡫ࡲࡶ࡮ࡺࡹ࠻ࠢࡈࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠣࡂࠥࡉ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡖ࡫ࡩ࡙ࠥࡄࡌࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡊࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡺ࡭ࡹ࡮ࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠌࠣࠤࠥࠦࠢࠣࠤჩ")
    credentials = {
        bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ც"): None,
        bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨძ"): None
    }
    credentials[bstack11l1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨწ")] = (
        os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨჭ")) or
        os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࠬხ"))
    )
    credentials[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬჯ")] = (
        os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ჰ")) or
        os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡎࡉ࡞࠭ჱ"))
    )
    if not credentials[bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧჲ")] or not credentials[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩჳ")]:
        if config and isinstance(config, dict):
            credentials[bstack11l1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩჴ")] = config.get(bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪჵ")) or config.get(bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸࠧჶ"))
            credentials[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ჷ")] = config.get(bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧჸ")) or config.get(bstack11l1l11_opy_ (u"ࠬࡱࡥࡺࠩჹ"))
    return credentials
def bstack1ll11l11l1_opy_(config):
    bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡧࡦࡹࡹ࡫ࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡢࡺࠢࡧࡩࡱ࡫ࡧࡢࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࠺ࠋࠢࠣࠤࠥ࠷࠮ࠡࡇࡻࡸࡷࡧࡣࡵࡵࠣࡧࡷ࡫ࡤࡦࡰࡷ࡭ࡦࡲࡳࠡࡨࡵࡳࡲࠦࡣࡰࡰࡩ࡭࡬࠵ࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠎࠥࠦࠠࠡ࠴࠱ࠤࡉࡵࡷ࡯࡮ࡲࡥࡩࡹ࠯ࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡪࠥࡴࡥࡦࡦࡨࡨࠏࠦࠠࠡࠢ࠶࠲࡙ࠥࡰࡢࡹࡱࡷࠥࡺࡨࡦࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡷࠥࡧࠠࡴࡷࡥࡴࡷࡵࡣࡦࡵࡶࠤࡼ࡯ࡴࡩࠢ࡬ࡲ࡭࡫ࡲࡪࡶࡨࡨࠥࡹࡴࡥ࡫ࡲࠎࠥࠦࠠࠡ࠶࠱ࠤࡋࡵࡲࡸࡣࡵࡨࡸࠦࡳࡪࡩࡱࡥࡱࡹࠠࠩࡕࡌࡋࡎࡔࡔ࠭ࠢࡖࡍࡌ࡚ࡅࡓࡏ࠯ࠤࡪࡺࡣ࠯ࠫࠣࡸࡴࠦࡴࡩࡧࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵࠍࠤࠥࠦࠠ࠶࠰ࠣࡉࡽ࡯ࡴࡴࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡸࡧ࡭ࡦࠢࡦࡳࡩ࡫ࠠࡢࡵࠣࡸ࡭࡫ࠠࡤࡪ࡬ࡰࡩࠦࡰࡳࡱࡦࡩࡸࡹࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪ࠾࡚ࠥࡨࡦࠢࡖࡈࡐࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠍࠤࠥࠦࠠࠣࠤࠥჺ")
    try:
        bstack1llllll1l1l_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹࠦࡷࡪࡶ࡫ࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࠺ࠡࡽࢀࠫ჻").format(bstack1llllll1l1l_opy_))
        credentials = bstack1lllll1ll1l_opy_(config)
        if not credentials[bstack11l1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪჼ")] or not credentials[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬჽ")]:
            logger.error(bstack11l1l11_opy_ (u"ࠪࡅࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤ࡮ࡴࡣࡰ࡯ࡳࡰࡪࡺࡥ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡤࡨࡩࠦࡹࡰࡷࡵࠤࡺࡹࡥࡳࡐࡤࡱࡪࠦࡡ࡯ࡦࠣࡥࡨࡩࡥࡴࡵࡎࡩࡾࠦࡴࡰࠢࡨ࡭ࡹ࡮ࡥࡳࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫ࠠࡰࡴࠣࡥࡸࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹࠬࠡࡶ࡫ࡩࡳࠦࡴࡳࡻࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡹ࡮ࡥࠡࡥࡲࡱࡲࡧ࡮ࡥࠢࡤ࡫ࡦ࡯࡮࠯ࠩჾ"))
            sys.exit(1)
        try:
            bstack1llllll1111_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡇࡑࡏࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠧჿ").format(e))
            sys.exit(1)
        if not bstack1llllll1111_opy_:
            logger.error(bstack11l1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡈࡒࡉࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠫᄀ"))
            sys.exit(1)
        binary_path = bstack1llllll11l1_opy_(bstack1llllll1111_opy_)
        try:
            if not binary_path:
                logger.debug(bstack11l1l11_opy_ (u"࠭ࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡲࡡࡵࡧࡶࡸࠥࡼࡥࡳࡵ࡬ࡳࡳ࠭ᄁ"))
                binary_path = bstack1lllll1ll11_opy_(bstack11l1l11_opy_ (u"ࠧࠨᄂ"), bstack1llllll1111_opy_, credentials)
            else:
                logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡺࡶࡤࡢࡶࡨࡷࠬᄃ"))
                binary_path = bstack1lllll1ll11_opy_(binary_path, bstack1llllll1111_opy_, credentials)
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠩࡄࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡣࡧࡨࠥࡿ࡯ࡶࡴࠣࡹࡸ࡫ࡲࡏࡣࡰࡩࠥࡧ࡮ࡥࠢࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠥࡺ࡯ࠡࡧ࡬ࡸ࡭࡫ࡲࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡨ࡬ࡰࡪࠦ࡯ࡳࠢࡤࡷࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸ࠲ࠠࡵࡪࡨࡲࠥࡺࡲࡺࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡣࡪࡥ࡮ࡴ࠮ࠨᄄ"))
            logger.debug(bstack11l1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠧᄅ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack11l1l11_opy_ (u"ࠫࡆࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥ࡯࡮ࡤࡱࡰࡴࡱ࡫ࡴࡦ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡥࡩࡪࠠࡺࡱࡸࡶࠥࡻࡳࡦࡴࡑࡥࡲ࡫ࠠࡢࡰࡧࠤࡦࡩࡣࡦࡵࡶࡏࡪࡿࠠࡵࡱࠣࡩ࡮ࡺࡨࡦࡴࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥࠡࡱࡵࠤࡦࡹࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳ࠭ࠢࡷ࡬ࡪࡴࠠࡵࡴࡼࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡺࡨࡦࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡥ࡬ࡧࡩ࡯࠰ࠪᄆ"))
            logger.debug(bstack11l1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡳࡷࠦ࡬ࡰࡥࡤࡸࡪࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠪᄇ"))
            sys.exit(1)
        logger.debug(bstack11l1l11_opy_ (u"࠭ࡓࡱࡣࡺࡲ࡮ࡴࡧ࠻ࠢࡾࢁࠥࡲ࡯ࡢࡦࠣࡿࢂ࠭ᄈ").format(binary_path, bstack11l1l11_opy_ (u"ࠢࠡࠤᄉ").join(bstack1llllll1l1l_opy_)))
        bstack1llllll11ll_opy_ = [binary_path, bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡥࡩ࠭ᄊ")] + bstack1llllll1l1l_opy_
        bstack1llllll1ll1_opy_ = subprocess.Popen(
            bstack1llllll11ll_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1lllll1llll_opy_(signum, frame):
            bstack11l1l11_opy_ (u"ࠤࠥࠦࡋࡵࡲࡸࡣࡵࡨࠥࡹࡩࡨࡰࡤࡰࡸࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸࠨࠢࠣᄋ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack11l1l11_opy_ (u"ࠪࡖࡪࡩࡥࡪࡸࡨࡨࠥࡹࡩࡨࡰࡤࡰࠥࢁࡽ࠭ࠢࡩࡳࡷࡽࡡࡳࡦ࡬ࡲ࡬ࠦࡴࡰࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰࠱࠲ࠬᄌ").format(signum))
            if bstack1llllll1ll1_opy_ and bstack1llllll1ll1_opy_.poll() is None:
                try:
                    bstack1llllll1ll1_opy_.send_signal(signum)
                    logger.debug(bstack11l1l11_opy_ (u"ࠫ࡜ࡧࡩࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡷࡳࠥ࡫ࡸࡪࡶ࠱࠲࠳࠭ᄍ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1lllll1llll_opy_)
        exit_code = bstack1llllll1ll1_opy_.wait()
        logger.debug(bstack11l1l11_opy_ (u"ࠬࢁࡽࠡࡧࡻ࡭ࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡣࡰࡦࡨࠤࢀࢃࠧᄎ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡩ࡯࡫ࡷ࡭ࡦࡺࡩ࡯ࡩࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹࡀࠠࡼࡿࠪᄏ").format(e))
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠫᄐ").format(e))
        sys.exit(1)