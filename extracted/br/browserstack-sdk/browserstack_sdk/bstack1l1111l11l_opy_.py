# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
bstack1111_opy_ (u"ࠢࠣࠤࠍࡐࡴࡧࡤࠡࡖࡨࡷࡹ࡯࡮ࡨࠢࡐࡳࡩࡻ࡬ࡦࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠌࡋࡥࡳࡪ࡬ࡦࡵࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡢࡺࠢࡧࡩࡱ࡫ࡧࡢࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠍࠦࠧࠨღ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1lllll1l11l_opy_,
    get_cli_dir,
    bstack1lllll1l1l1_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1lllll1l111_opy_(config):
    bstack1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡇࡻࡸࡷࡧࡣࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡹ࡮ࠠࡧࡴࡲࡱࠥࡩ࡯࡮࡯ࡤࡲࡩ࠳࡬ࡪࡰࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡰࡴࠣࡧࡴࡴࡦࡪࡩ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡗ࡬ࡪࠦࡓࡅࡍࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡴࡶࡵ࠾ࠥࡖࡡࡵࡪࠣࡸࡴࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠥࠦࠧყ")
    try:
        if bstack1111_opy_ (u"ࠩ࠰࠱ࡨࡵ࡮ࡧ࡫ࡪࠫშ") in sys.argv:
            bstack1lllll11ll1_opy_ = sys.argv.index(bstack1111_opy_ (u"ࠪ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠬჩ"))
            if bstack1lllll11ll1_opy_ + 1 < len(sys.argv):
                bstack1lllll1l1ll_opy_ = sys.argv[bstack1lllll11ll1_opy_ + 1]
                logger.debug(bstack1111_opy_ (u"ࠦࡋࡵࡵ࡯ࡦࠣ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡬ࡢࡩࠣࡻ࡮ࡺࡨࠡࡲࡤࡸ࡭ࡀࠠࡼࡿࠥც").format(bstack1lllll1l1ll_opy_))
                return bstack1lllll1l1ll_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥ࠳࠭ࡤࡱࡱࡪ࡮࡭ࠠࡧ࡮ࡤ࡫࠿ࠦࡻࡾࠤძ").format(e))
        pass
    bstack1lllll1l1ll_opy_ = os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪწ"))
    if bstack1lllll1l1ll_opy_:
        logger.debug(bstack1111_opy_ (u"ࠢࡇࡱࡸࡲࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡰࡢࡶ࡫ࠤ࡮ࡴࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸ࠿ࠦࡻࡾࠤჭ").format(bstack1lllll1l1ll_opy_))
        return bstack1lllll1l1ll_opy_
    return None
def bstack1lllll1llll_opy_(config):
    bstack1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡇࡻࡸࡷࡧࡣࡵࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡥࡵࡩࡩ࡫࡮ࡵ࡫ࡤࡰࡸࠦࡦࡳࡱࡰࠤࡻࡧࡲࡪࡱࡸࡷࠥࡹ࡯ࡶࡴࡦࡩࡸ࠴ࠊࠡࠢࠣࠤࡕࡸࡩࡰࡴ࡬ࡸࡾࡀࠠࡆࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠡࡀࠣࡇࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡔࡩࡧࠣࡗࡉࡑࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡈ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡸ࡫ࡷ࡬ࠥࡻࡳࡦࡴࡑࡥࡲ࡫ࠠࡢࡰࡧࠤࡦࡩࡣࡦࡵࡶࡏࡪࡿࠊࠡࠢࠣࠤࠧࠨࠢხ")
    credentials = {
        bstack1111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫჯ"): None,
        bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ჰ"): None
    }
    credentials[bstack1111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ჱ")] = (
        os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ჲ")) or
        os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࠪჳ"))
    )
    credentials[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪჴ")] = (
        os.environ.get(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫჵ")) or
        os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡌࡇ࡜ࠫჶ"))
    )
    if not credentials[bstack1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬჷ")] or not credentials[bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧჸ")]:
        if config and isinstance(config, dict):
            credentials[bstack1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧჹ")] = config.get(bstack1111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨჺ")) or config.get(bstack1111_opy_ (u"ࠧࡶࡵࡨࡶࠬ჻"))
            credentials[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫჼ")] = config.get(bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬჽ")) or config.get(bstack1111_opy_ (u"ࠪ࡯ࡪࡿࠧჾ"))
    return credentials
def bstack111ll1lll_opy_(config):
    bstack1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡊࡾࡥࡤࡷࡷࡩࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡧࡿࠠࡥࡧ࡯ࡩ࡬ࡧࡴࡪࡰࡪࠤࡹࡵࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲ࠿ࠐࠠࠡࠢࠣ࠵࠳ࠦࡅࡹࡶࡵࡥࡨࡺࡳࠡࡥࡵࡩࡩ࡫࡮ࡵ࡫ࡤࡰࡸࠦࡦࡳࡱࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠳ࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠌࠣࠤࠥࠦ࠲࠯ࠢࡇࡳࡼࡴ࡬ࡰࡣࡧࡷ࠴ࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡨࠣࡲࡪ࡫ࡤࡦࡦࠍࠤࠥࠦࠠ࠴࠰ࠣࡗࡵࡧࡷ࡯ࡵࠣࡸ࡭࡫ࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡵࠣࡥࠥࡹࡵࡣࡲࡵࡳࡨ࡫ࡳࡴࠢࡺ࡭ࡹ࡮ࠠࡪࡰ࡫ࡩࡷ࡯ࡴࡦࡦࠣࡷࡹࡪࡩࡰࠌࠣࠤࠥࠦ࠴࠯ࠢࡉࡳࡷࡽࡡࡳࡦࡶࠤࡸ࡯ࡧ࡯ࡣ࡯ࡷࠥ࠮ࡓࡊࡉࡌࡒ࡙࠲ࠠࡔࡋࡊࡘࡊࡘࡍ࠭ࠢࡨࡸࡨ࠴ࠩࠡࡶࡲࠤࡹ࡮ࡥࠡࡥ࡫࡭ࡱࡪࠠࡱࡴࡲࡧࡪࡹࡳࠋࠢࠣࠤࠥ࠻࠮ࠡࡇࡻ࡭ࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡶࡥࡲ࡫ࠠࡤࡱࡧࡩࠥࡧࡳࠡࡶ࡫ࡩࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡘ࡭࡫ࠠࡔࡆࡎࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠋࠢࠣࠤࠥࠨࠢࠣჿ")
    try:
        bstack1lllll1ll1l_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack1111_opy_ (u"ࠬࡋࡸࡦࡥࡸࡸ࡮ࡴࡧࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷࠤࡼ࡯ࡴࡩࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷ࠿ࠦࡻࡾࠩᄀ").format(bstack1lllll1ll1l_opy_))
        credentials = bstack1lllll1llll_opy_(config)
        if not credentials[bstack1111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᄁ")] or not credentials[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᄂ")]:
            logger.error(bstack1111_opy_ (u"ࠨࡃࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡲࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡾࡵࡵࡳࠢࡸࡷࡪࡸࡎࡢ࡯ࡨࠤࡦࡴࡤࠡࡣࡦࡧࡪࡹࡳࡌࡧࡼࠤࡹࡵࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡧ࡫࡯ࡩࠥࡵࡲࠡࡣࡶࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷ࠱ࠦࡴࡩࡧࡱࠤࡹࡸࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡣࡰ࡯ࡰࡥࡳࡪࠠࡢࡩࡤ࡭ࡳ࠴ࠧᄃ"))
            sys.exit(1)
        try:
            bstack1lllll1lll1_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack1111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡅࡏࡍࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠬᄄ").format(e))
            sys.exit(1)
        if not bstack1lllll1lll1_opy_:
            logger.error(bstack1111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡆࡐࡎࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠩᄅ"))
            sys.exit(1)
        binary_path = bstack1lllll1l1l1_opy_(bstack1lllll1lll1_opy_)
        try:
            if not binary_path:
                logger.debug(bstack1111_opy_ (u"ࠫࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡰࡦࡺࡥࡴࡶࠣࡺࡪࡸࡳࡪࡱࡱࠫᄆ"))
                binary_path = bstack1lllll1l11l_opy_(bstack1111_opy_ (u"ࠬ࠭ᄇ"), bstack1lllll1lll1_opy_, credentials)
            else:
                logger.debug(bstack1111_opy_ (u"࠭ࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡸࡴࡩࡧࡴࡦࡵࠪᄈ"))
                binary_path = bstack1lllll1l11l_opy_(binary_path, bstack1lllll1lll1_opy_, credentials)
        except Exception as e:
            logger.error(bstack1111_opy_ (u"ࠧࡂࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡽࡴࡻࡲࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠣࡸࡴࠦࡥࡪࡶ࡫ࡩࡷࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠰ࠥࡺࡨࡦࡰࠣࡸࡷࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡡࡨࡣ࡬ࡲ࠳࠭ᄉ"))
            logger.debug(bstack1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠬᄊ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack1111_opy_ (u"ࠩࡄࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡣࡧࡨࠥࡿ࡯ࡶࡴࠣࡹࡸ࡫ࡲࡏࡣࡰࡩࠥࡧ࡮ࡥࠢࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠥࡺ࡯ࠡࡧ࡬ࡸ࡭࡫ࡲࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡨ࡬ࡰࡪࠦ࡯ࡳࠢࡤࡷࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸ࠲ࠠࡵࡪࡨࡲࠥࡺࡲࡺࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡣࡪࡥ࡮ࡴ࠮ࠨᄋ"))
            logger.debug(bstack1111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡱࡵࠤࡱࡵࡣࡢࡶࡨࠤࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠨᄌ"))
            sys.exit(1)
        logger.debug(bstack1111_opy_ (u"ࠫࡘࡶࡡࡸࡰ࡬ࡲ࡬ࡀࠠࡼࡿࠣࡰࡴࡧࡤࠡࡽࢀࠫᄍ").format(binary_path, bstack1111_opy_ (u"ࠧࠦࠢᄎ").join(bstack1lllll1ll1l_opy_)))
        bstack1lllll11lll_opy_ = [binary_path, bstack1111_opy_ (u"࠭࡬ࡰࡣࡧࠫᄏ")] + bstack1lllll1ll1l_opy_
        bstack1lllll11l1l_opy_ = subprocess.Popen(
            bstack1lllll11lll_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1lllll1ll11_opy_(signum, frame):
            bstack1111_opy_ (u"ࠢࠣࠤࡉࡳࡷࡽࡡࡳࡦࠣࡷ࡮࡭࡮ࡢ࡮ࡶࠤࡹࡵࠠࡵࡪࡨࠤࡨ࡮ࡩ࡭ࡦࠣࡴࡷࡵࡣࡦࡵࡶࠦࠧࠨᄐ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack1111_opy_ (u"ࠨࡔࡨࡧࡪ࡯ࡶࡦࡦࠣࡷ࡮࡭࡮ࡢ࡮ࠣࡿࢂ࠲ࠠࡧࡱࡵࡻࡦࡸࡤࡪࡰࡪࠤࡹࡵࠠࡤࡪ࡬ࡰࡩࠦࡰࡳࡱࡦࡩࡸࡹ࠮࠯࠰ࠪᄑ").format(signum))
            if bstack1lllll11l1l_opy_ and bstack1lllll11l1l_opy_.poll() is None:
                try:
                    bstack1lllll11l1l_opy_.send_signal(signum)
                    logger.debug(bstack1111_opy_ (u"࡚ࠩࡥ࡮ࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡤࡪ࡬ࡰࡩࠦࡰࡳࡱࡦࡩࡸࡹࠠࡵࡱࠣࡩࡽ࡯ࡴ࠯࠰࠱ࠫᄒ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1lllll1ll11_opy_)
        exit_code = bstack1lllll11l1l_opy_.wait()
        logger.debug(bstack1111_opy_ (u"ࠪࡿࢂࠦࡥࡹ࡫ࡷࡩࡩࠦࡷࡪࡶ࡫ࠤࡨࡵࡤࡦࠢࡾࢁࠬᄓ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack1111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤ࡮ࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࠾ࠥࢁࡽࠨᄔ").format(e))
        logger.debug(bstack1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩᄕ").format(e))
        sys.exit(1)