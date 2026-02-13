# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
bstack11l11_opy_ (u"ࠢࠣࠤࠍࡐࡴࡧࡤࠡࡖࡨࡷࡹ࡯࡮ࡨࠢࡐࡳࡩࡻ࡬ࡦࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠌࡋࡥࡳࡪ࡬ࡦࡵࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡢࡺࠢࡧࡩࡱ࡫ࡧࡢࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠍࠦࠧࠨი")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1lllll1l11l_opy_,
    get_cli_dir,
    bstack1lllll11lll_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1lllll11l1l_opy_(config):
    bstack11l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡇࡻࡸࡷࡧࡣࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡹ࡮ࠠࡧࡴࡲࡱࠥࡩ࡯࡮࡯ࡤࡲࡩ࠳࡬ࡪࡰࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡰࡴࠣࡧࡴࡴࡦࡪࡩ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡗ࡬ࡪࠦࡓࡅࡍࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡴࡶࡵ࠾ࠥࡖࡡࡵࡪࠣࡸࡴࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠥࠦࠧკ")
    try:
        if bstack11l11_opy_ (u"ࠩ࠰࠱ࡨࡵ࡮ࡧ࡫ࡪࠫლ") in sys.argv:
            bstack1lllll11111_opy_ = sys.argv.index(bstack11l11_opy_ (u"ࠪ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠬმ"))
            if bstack1lllll11111_opy_ + 1 < len(sys.argv):
                bstack1lllll1l111_opy_ = sys.argv[bstack1lllll11111_opy_ + 1]
                logger.debug(bstack11l11_opy_ (u"ࠦࡋࡵࡵ࡯ࡦࠣ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡬ࡢࡩࠣࡻ࡮ࡺࡨࠡࡲࡤࡸ࡭ࡀࠠࡼࡿࠥნ").format(bstack1lllll1l111_opy_))
                return bstack1lllll1l111_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥ࠳࠭ࡤࡱࡱࡪ࡮࡭ࠠࡧ࡮ࡤ࡫࠿ࠦࡻࡾࠤო").format(e))
        pass
    bstack1lllll1l111_opy_ = os.environ.get(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪპ"))
    if bstack1lllll1l111_opy_:
        logger.debug(bstack11l11_opy_ (u"ࠢࡇࡱࡸࡲࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡰࡢࡶ࡫ࠤ࡮ࡴࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸ࠿ࠦࡻࡾࠤჟ").format(bstack1lllll1l111_opy_))
        return bstack1lllll1l111_opy_
    return None
def bstack1lllll1111l_opy_(config):
    bstack11l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡇࡻࡸࡷࡧࡣࡵࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡥࡵࡩࡩ࡫࡮ࡵ࡫ࡤࡰࡸࠦࡦࡳࡱࡰࠤࡻࡧࡲࡪࡱࡸࡷࠥࡹ࡯ࡶࡴࡦࡩࡸ࠴ࠊࠡࠢࠣࠤࡕࡸࡩࡰࡴ࡬ࡸࡾࡀࠠࡆࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠡࡀࠣࡇࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡔࡩࡧࠣࡗࡉࡑࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡈ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡸ࡫ࡷ࡬ࠥࡻࡳࡦࡴࡑࡥࡲ࡫ࠠࡢࡰࡧࠤࡦࡩࡣࡦࡵࡶࡏࡪࡿࠊࠡࠢࠣࠤࠧࠨࠢრ")
    credentials = {
        bstack11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫს"): None,
        bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ტ"): None
    }
    credentials[bstack11l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭უ")] = (
        os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ფ")) or
        os.environ.get(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࠪქ"))
    )
    credentials[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪღ")] = (
        os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫყ")) or
        os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡌࡇ࡜ࠫშ"))
    )
    if not credentials[bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬჩ")] or not credentials[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧც")]:
        if config and isinstance(config, dict):
            credentials[bstack11l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧძ")] = config.get(bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨწ")) or config.get(bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࠬჭ"))
            credentials[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫხ")] = config.get(bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬჯ")) or config.get(bstack11l11_opy_ (u"ࠪ࡯ࡪࡿࠧჰ"))
    return credentials
def bstack1l111111ll_opy_(config):
    bstack11l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡊࡾࡥࡤࡷࡷࡩࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤࡧࡿࠠࡥࡧ࡯ࡩ࡬ࡧࡴࡪࡰࡪࠤࡹࡵࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲ࠿ࠐࠠࠡࠢࠣ࠵࠳ࠦࡅࡹࡶࡵࡥࡨࡺࡳࠡࡥࡵࡩࡩ࡫࡮ࡵ࡫ࡤࡰࡸࠦࡦࡳࡱࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠳ࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠌࠣࠤࠥࠦ࠲࠯ࠢࡇࡳࡼࡴ࡬ࡰࡣࡧࡷ࠴ࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡨࠣࡲࡪ࡫ࡤࡦࡦࠍࠤࠥࠦࠠ࠴࠰ࠣࡗࡵࡧࡷ࡯ࡵࠣࡸ࡭࡫ࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡵࠣࡥࠥࡹࡵࡣࡲࡵࡳࡨ࡫ࡳࡴࠢࡺ࡭ࡹ࡮ࠠࡪࡰ࡫ࡩࡷ࡯ࡴࡦࡦࠣࡷࡹࡪࡩࡰࠌࠣࠤࠥࠦ࠴࠯ࠢࡉࡳࡷࡽࡡࡳࡦࡶࠤࡸ࡯ࡧ࡯ࡣ࡯ࡷࠥ࠮ࡓࡊࡉࡌࡒ࡙࠲ࠠࡔࡋࡊࡘࡊࡘࡍ࠭ࠢࡨࡸࡨ࠴ࠩࠡࡶࡲࠤࡹ࡮ࡥࠡࡥ࡫࡭ࡱࡪࠠࡱࡴࡲࡧࡪࡹࡳࠋࠢࠣࠤࠥ࠻࠮ࠡࡇࡻ࡭ࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡶࡥࡲ࡫ࠠࡤࡱࡧࡩࠥࡧࡳࠡࡶ࡫ࡩࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡘ࡭࡫ࠠࡔࡆࡎࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠋࠢࠣࠤࠥࠨࠢࠣჱ")
    try:
        bstack1lllll11l11_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack11l11_opy_ (u"ࠬࡋࡸࡦࡥࡸࡸ࡮ࡴࡧࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷࠤࡼ࡯ࡴࡩࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷ࠿ࠦࡻࡾࠩჲ").format(bstack1lllll11l11_opy_))
        credentials = bstack1lllll1111l_opy_(config)
        if not credentials[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨჳ")] or not credentials[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪჴ")]:
            logger.error(bstack11l11_opy_ (u"ࠨࡃࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡲࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡾࡵࡵࡳࠢࡸࡷࡪࡸࡎࡢ࡯ࡨࠤࡦࡴࡤࠡࡣࡦࡧࡪࡹࡳࡌࡧࡼࠤࡹࡵࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡧ࡫࡯ࡩࠥࡵࡲࠡࡣࡶࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷ࠱ࠦࡴࡩࡧࡱࠤࡹࡸࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡣࡰ࡯ࡰࡥࡳࡪࠠࡢࡩࡤ࡭ࡳ࠴ࠧჵ"))
            sys.exit(1)
        try:
            bstack1llll1lllll_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack11l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡅࡏࡍࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠬჶ").format(e))
            sys.exit(1)
        if not bstack1llll1lllll_opy_:
            logger.error(bstack11l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡆࡐࡎࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠩჷ"))
            sys.exit(1)
        binary_path = bstack1lllll11lll_opy_(bstack1llll1lllll_opy_)
        try:
            if not binary_path:
                logger.debug(bstack11l11_opy_ (u"ࠫࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡰࡦࡺࡥࡴࡶࠣࡺࡪࡸࡳࡪࡱࡱࠫჸ"))
                binary_path = bstack1lllll1l11l_opy_(bstack11l11_opy_ (u"ࠬ࠭ჹ"), bstack1llll1lllll_opy_, credentials)
            else:
                logger.debug(bstack11l11_opy_ (u"࠭ࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡸࡴࡩࡧࡴࡦࡵࠪჺ"))
                binary_path = bstack1lllll1l11l_opy_(binary_path, bstack1llll1lllll_opy_, credentials)
        except Exception as e:
            logger.error(bstack11l11_opy_ (u"ࠧࡂࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡽࡴࡻࡲࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠣࡸࡴࠦࡥࡪࡶ࡫ࡩࡷࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠰ࠥࡺࡨࡦࡰࠣࡸࡷࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡡࡨࡣ࡬ࡲ࠳࠭჻"))
            logger.debug(bstack11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠬჼ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack11l11_opy_ (u"ࠩࡄࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡣࡧࡨࠥࡿ࡯ࡶࡴࠣࡹࡸ࡫ࡲࡏࡣࡰࡩࠥࡧ࡮ࡥࠢࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠥࡺ࡯ࠡࡧ࡬ࡸ࡭࡫ࡲࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡨ࡬ࡰࡪࠦ࡯ࡳࠢࡤࡷࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸ࠲ࠠࡵࡪࡨࡲࠥࡺࡲࡺࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡣࡪࡥ࡮ࡴ࠮ࠨჽ"))
            logger.debug(bstack11l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡱࡵࠤࡱࡵࡣࡢࡶࡨࠤࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠨჾ"))
            sys.exit(1)
        logger.debug(bstack11l11_opy_ (u"ࠫࡘࡶࡡࡸࡰ࡬ࡲ࡬ࡀࠠࡼࡿࠣࡰࡴࡧࡤࠡࡽࢀࠫჿ").format(binary_path, bstack11l11_opy_ (u"ࠧࠦࠢᄀ").join(bstack1lllll11l11_opy_)))
        bstack1lllll111l1_opy_ = [binary_path, bstack11l11_opy_ (u"࠭࡬ࡰࡣࡧࠫᄁ")] + bstack1lllll11l11_opy_
        bstack1lllll11ll1_opy_ = subprocess.Popen(
            bstack1lllll111l1_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1lllll111ll_opy_(signum, frame):
            bstack11l11_opy_ (u"ࠢࠣࠤࡉࡳࡷࡽࡡࡳࡦࠣࡷ࡮࡭࡮ࡢ࡮ࡶࠤࡹࡵࠠࡵࡪࡨࠤࡨ࡮ࡩ࡭ࡦࠣࡴࡷࡵࡣࡦࡵࡶࠦࠧࠨᄂ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack11l11_opy_ (u"ࠨࡔࡨࡧࡪ࡯ࡶࡦࡦࠣࡷ࡮࡭࡮ࡢ࡮ࠣࡿࢂ࠲ࠠࡧࡱࡵࡻࡦࡸࡤࡪࡰࡪࠤࡹࡵࠠࡤࡪ࡬ࡰࡩࠦࡰࡳࡱࡦࡩࡸࡹ࠮࠯࠰ࠪᄃ").format(signum))
            if bstack1lllll11ll1_opy_ and bstack1lllll11ll1_opy_.poll() is None:
                try:
                    bstack1lllll11ll1_opy_.send_signal(signum)
                    logger.debug(bstack11l11_opy_ (u"࡚ࠩࡥ࡮ࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡤࡪ࡬ࡰࡩࠦࡰࡳࡱࡦࡩࡸࡹࠠࡵࡱࠣࡩࡽ࡯ࡴ࠯࠰࠱ࠫᄄ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1lllll111ll_opy_)
        exit_code = bstack1lllll11ll1_opy_.wait()
        logger.debug(bstack11l11_opy_ (u"ࠪࡿࢂࠦࡥࡹ࡫ࡷࡩࡩࠦࡷࡪࡶ࡫ࠤࡨࡵࡤࡦࠢࡾࢁࠬᄅ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤ࡮ࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࠾ࠥࢁࡽࠨᄆ").format(e))
        logger.debug(bstack11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩᄇ").format(e))
        sys.exit(1)