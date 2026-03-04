# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
bstack1lll1l_opy_ (u"ࠨࠢࠣࠌࡏࡳࡦࡪࠠࡕࡧࡶࡸ࡮ࡴࡧࠡࡏࡲࡨࡺࡲࡥࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠋࡊࡤࡲࡩࡲࡥࡴࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡨࡹࠡࡦࡨࡰࡪ࡭ࡡࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠌࠥࠦࠧქ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1lllll1l1ll_opy_,
    get_cli_dir,
    bstack1lllll1l1l1_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1lllll1llll_opy_(config):
    bstack1lll1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡆࡺࡷࡶࡦࡩࡴࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡸ࡭ࠦࡦࡳࡱࡰࠤࡨࡵ࡭࡮ࡣࡱࡨ࠲ࡲࡩ࡯ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦ࡯ࡳࠢࡦࡳࡳ࡬ࡩࡨ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡖ࡫ࡩ࡙ࠥࡄࡌࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡳࡵࡴ࠽ࠤࡕࡧࡴࡩࠢࡷࡳࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠤࠥࠦღ")
    try:
        if bstack1lll1l_opy_ (u"ࠨ࠯࠰ࡧࡴࡴࡦࡪࡩࠪყ") in sys.argv:
            bstack1llllll111l_opy_ = sys.argv.index(bstack1lll1l_opy_ (u"ࠩ࠰࠱ࡨࡵ࡮ࡧ࡫ࡪࠫშ"))
            if bstack1llllll111l_opy_ + 1 < len(sys.argv):
                bstack1lllll1lll1_opy_ = sys.argv[bstack1llllll111l_opy_ + 1]
                logger.debug(bstack1lll1l_opy_ (u"ࠥࡊࡴࡻ࡮ࡥࠢ࠰࠱ࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡲࡡࡨࠢࡺ࡭ࡹ࡮ࠠࡱࡣࡷ࡬࠿ࠦࡻࡾࠤჩ").format(bstack1lllll1lll1_opy_))
                return bstack1lllll1lll1_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤ࠲࠳ࡣࡰࡰࡩ࡭࡬ࠦࡦ࡭ࡣࡪ࠾ࠥࢁࡽࠣც").format(e))
        pass
    bstack1lllll1lll1_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩძ"))
    if bstack1lllll1lll1_opy_:
        logger.debug(bstack1lll1l_opy_ (u"ࠨࡆࡰࡷࡱࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥࡶࡡࡵࡪࠣ࡭ࡳࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࢁࡽࠣწ").format(bstack1lllll1lll1_opy_))
        return bstack1lllll1lll1_opy_
    return None
def bstack1lllll1ll1l_opy_(config):
    bstack1lll1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡆࡺࡷࡶࡦࡩࡴࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡤࡴࡨࡨࡪࡴࡴࡪࡣ࡯ࡷࠥ࡬ࡲࡰ࡯ࠣࡺࡦࡸࡩࡰࡷࡶࠤࡸࡵࡵࡳࡥࡨࡷ࠳ࠐࠠࠡࠢࠣࡔࡷ࡯࡯ࡳ࡫ࡷࡽ࠿ࠦࡅ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹࠠ࠿ࠢࡆࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪ࠾࡚ࠥࡨࡦࠢࡖࡈࡐࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡇ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡷࡪࡶ࡫ࠤࡺࡹࡥࡳࡐࡤࡱࡪࠦࡡ࡯ࡦࠣࡥࡨࡩࡥࡴࡵࡎࡩࡾࠐࠠࠡࠢࠣࠦࠧࠨჭ")
    credentials = {
        bstack1lll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪხ"): None,
        bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬჯ"): None
    }
    credentials[bstack1lll1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬჰ")] = (
        os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬჱ")) or
        os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࠩჲ"))
    )
    credentials[bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩჳ")] = (
        os.environ.get(bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪჴ")) or
        os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙ࡋࡆ࡛ࠪჵ"))
    )
    if not credentials[bstack1lll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫჶ")] or not credentials[bstack1lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ჷ")]:
        if config and isinstance(config, dict):
            credentials[bstack1lll1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ჸ")] = config.get(bstack1lll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧჹ")) or config.get(bstack1lll1l_opy_ (u"࠭ࡵࡴࡧࡵࠫჺ"))
            credentials[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ჻")] = config.get(bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫჼ")) or config.get(bstack1lll1l_opy_ (u"ࠩ࡮ࡩࡾ࠭ჽ"))
    return credentials
def bstack11lll1l1l_opy_(config):
    bstack1lll1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡉࡽ࡫ࡣࡶࡶࡨࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡦࡾࠦࡤࡦ࡮ࡨ࡫ࡦࡺࡩ࡯ࡩࠣࡸࡴࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱ࠾ࠏࠦࠠࠡࠢ࠴࠲ࠥࡋࡸࡵࡴࡤࡧࡹࡹࠠࡤࡴࡨࡨࡪࡴࡴࡪࡣ࡯ࡷࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡴࡦࡪࡩ࠲ࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠋࠢࠣࠤࠥ࠸࠮ࠡࡆࡲࡻࡳࡲ࡯ࡢࡦࡶ࠳ࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠦࡩࡧࠢࡱࡩࡪࡪࡥࡥࠌࠣࠤࠥࠦ࠳࠯ࠢࡖࡴࡦࡽ࡮ࡴࠢࡷ࡬ࡪࠦࡢࡪࡰࡤࡶࡾࠦࡡࡴࠢࡤࠤࡸࡻࡢࡱࡴࡲࡧࡪࡹࡳࠡࡹ࡬ࡸ࡭ࠦࡩ࡯ࡪࡨࡶ࡮ࡺࡥࡥࠢࡶࡸࡩ࡯࡯ࠋࠢࠣࠤࠥ࠺࠮ࠡࡈࡲࡶࡼࡧࡲࡥࡵࠣࡷ࡮࡭࡮ࡢ࡮ࡶࠤ࡙࠭ࡉࡈࡋࡑࡘ࠱ࠦࡓࡊࡉࡗࡉࡗࡓࠬࠡࡧࡷࡧ࠳࠯ࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡪ࡬ࡰࡩࠦࡰࡳࡱࡦࡩࡸࡹࠊࠡࠢࠣࠤ࠺࠴ࠠࡆࡺ࡬ࡸࡸࠦࡷࡪࡶ࡫ࠤࡹ࡮ࡥࠡࡵࡤࡱࡪࠦࡣࡰࡦࡨࠤࡦࡹࠠࡵࡪࡨࠤࡨ࡮ࡩ࡭ࡦࠣࡴࡷࡵࡣࡦࡵࡶࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡗ࡬ࡪࠦࡓࡅࡍࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠊࠡࠢࠣࠤࠧࠨࠢჾ")
    try:
        bstack1llllll1111_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack1lll1l_opy_ (u"ࠫࡊࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶࠣࡻ࡮ࡺࡨࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࠾ࠥࢁࡽࠨჿ").format(bstack1llllll1111_opy_))
        credentials = bstack1lllll1ll1l_opy_(config)
        if not credentials[bstack1lll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᄀ")] or not credentials[bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᄁ")]:
            logger.error(bstack1lll1l_opy_ (u"ࠧࡂࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡽࡴࡻࡲࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠣࡸࡴࠦࡥࡪࡶ࡫ࡩࡷࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠰ࠥࡺࡨࡦࡰࠣࡸࡷࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡡࡨࡣ࡬ࡲ࠳࠭ᄂ"))
            sys.exit(1)
        try:
            bstack1lllll11lll_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack1lll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡄࡎࡌࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠫᄃ").format(e))
            sys.exit(1)
        if not bstack1lllll11lll_opy_:
            logger.error(bstack1lll1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡅࡏࡍࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠨᄄ"))
            sys.exit(1)
        binary_path = bstack1lllll1l1l1_opy_(bstack1lllll11lll_opy_)
        try:
            if not binary_path:
                logger.debug(bstack1lll1l_opy_ (u"ࠪࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢ࡯ࡥࡹ࡫ࡳࡵࠢࡹࡩࡷࡹࡩࡰࡰࠪᄅ"))
                binary_path = bstack1lllll1l1ll_opy_(bstack1lll1l_opy_ (u"ࠫࠬᄆ"), bstack1lllll11lll_opy_, credentials)
            else:
                logger.debug(bstack1lll1l_opy_ (u"ࠬࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤ࠭ࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡷࡳࡨࡦࡺࡥࡴࠩᄇ"))
                binary_path = bstack1lllll1l1ll_opy_(binary_path, bstack1lllll11lll_opy_, credentials)
        except Exception as e:
            logger.error(bstack1lll1l_opy_ (u"࠭ࡁࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡼࡳࡺࡸࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠢࡷࡳࠥ࡫ࡩࡵࡪࡨࡶࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠯ࠤࡹ࡮ࡥ࡯ࠢࡷࡶࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡧࡧࡢ࡫ࡱ࠲ࠬᄈ"))
            logger.debug(bstack1lll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠫᄉ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack1lll1l_opy_ (u"ࠨࡃࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡲࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡾࡵࡵࡳࠢࡸࡷࡪࡸࡎࡢ࡯ࡨࠤࡦࡴࡤࠡࡣࡦࡧࡪࡹࡳࡌࡧࡼࠤࡹࡵࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡧ࡫࡯ࡩࠥࡵࡲࠡࡣࡶࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷ࠱ࠦࡴࡩࡧࡱࠤࡹࡸࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡣࡰ࡯ࡰࡥࡳࡪࠠࡢࡩࡤ࡭ࡳ࠴ࠧᄊ"))
            logger.debug(bstack1lll1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡰࡴࠣࡰࡴࡩࡡࡵࡧࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠧᄋ"))
            sys.exit(1)
        logger.debug(bstack1lll1l_opy_ (u"ࠪࡗࡵࡧࡷ࡯࡫ࡱ࡫࠿ࠦࡻࡾࠢ࡯ࡳࡦࡪࠠࡼࡿࠪᄌ").format(binary_path, bstack1lll1l_opy_ (u"ࠦࠥࠨᄍ").join(bstack1llllll1111_opy_)))
        bstack1lllll1l11l_opy_ = [binary_path, bstack1lll1l_opy_ (u"ࠬࡲ࡯ࡢࡦࠪᄎ")] + bstack1llllll1111_opy_
        bstack1lllll1l111_opy_ = subprocess.Popen(
            bstack1lllll1l11l_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1lllll1ll11_opy_(signum, frame):
            bstack1lll1l_opy_ (u"ࠨࠢࠣࡈࡲࡶࡼࡧࡲࡥࠢࡶ࡭࡬ࡴࡡ࡭ࡵࠣࡸࡴࠦࡴࡩࡧࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵࠥࠦࠧᄏ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack1lll1l_opy_ (u"ࠧࡓࡧࡦࡩ࡮ࡼࡥࡥࠢࡶ࡭࡬ࡴࡡ࡭ࠢࡾࢁ࠱ࠦࡦࡰࡴࡺࡥࡷࡪࡩ࡯ࡩࠣࡸࡴࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸ࠴࠮࠯ࠩᄐ").format(signum))
            if bstack1lllll1l111_opy_ and bstack1lllll1l111_opy_.poll() is None:
                try:
                    bstack1lllll1l111_opy_.send_signal(signum)
                    logger.debug(bstack1lll1l_opy_ (u"ࠨ࡙ࡤ࡭ࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸࠦࡴࡰࠢࡨࡼ࡮ࡺ࠮࠯࠰ࠪᄑ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1lllll1ll11_opy_)
        exit_code = bstack1lllll1l111_opy_.wait()
        logger.debug(bstack1lll1l_opy_ (u"ࠩࡾࢁࠥ࡫ࡸࡪࡶࡨࡨࠥࡽࡩࡵࡪࠣࡧࡴࡪࡥࠡࡽࢀࠫᄒ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack1lll1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣ࡭ࡳ࡯ࡴࡪࡣࡷ࡭ࡳ࡭ࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࠽ࠤࢀࢃࠧᄓ").format(e))
        logger.debug(bstack1lll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠨᄔ").format(e))
        sys.exit(1)