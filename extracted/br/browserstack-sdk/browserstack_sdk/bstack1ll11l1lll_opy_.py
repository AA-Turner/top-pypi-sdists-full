# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
bstack1ll1l11_opy_ (u"ࠥࠦࠧࠐࡌࡰࡣࡧࠤ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥࡓ࡯ࡥࡷ࡯ࡩࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠏࡎࡡ࡯ࡦ࡯ࡩࡸࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡥࡽࠥࡪࡥ࡭ࡧࡪࡥࡹ࡯࡮ࡨࠢࡷࡳࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠐࠢࠣࠤዯ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1ll1l11lll1_opy_,
    get_cli_dir,
    bstack1ll1l111lll_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1ll1l11ll1l_opy_(config):
    bstack1ll1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡊࡾࡴࡳࡣࡦࡸࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡵࡪࠣࡪࡷࡵ࡭ࠡࡥࡲࡱࡲࡧ࡮ࡥ࠯࡯࡭ࡳ࡫ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣࡳࡷࠦࡣࡰࡰࡩ࡭࡬࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪ࠾࡚ࠥࡨࡦࠢࡖࡈࡐࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡷࡹࡸ࠺ࠡࡒࡤࡸ࡭ࠦࡴࡰࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠠࡰࡴࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠨࠢࠣደ")
    try:
        if bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡤࡱࡱࡪ࡮࡭ࠧዱ") in sys.argv:
            bstack1ll1l1l1111_opy_ = sys.argv.index(bstack1ll1l11_opy_ (u"࠭࠭࠮ࡥࡲࡲ࡫࡯ࡧࠨዲ"))
            if bstack1ll1l1l1111_opy_ + 1 < len(sys.argv):
                bstack1ll1l11ll11_opy_ = sys.argv[bstack1ll1l1l1111_opy_ + 1]
                logger.debug(bstack1ll1l11_opy_ (u"ࠢࡇࡱࡸࡲࡩࠦ࠭࠮ࡥࡲࡲ࡫࡯ࡧࠡࡨ࡯ࡥ࡬ࠦࡷࡪࡶ࡫ࠤࡵࡧࡴࡩ࠼ࠣࡿࢂࠨዳ").format(bstack1ll1l11ll11_opy_))
                return bstack1ll1l11ll11_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡ࠯࠰ࡧࡴࡴࡦࡪࡩࠣࡪࡱࡧࡧ࠻ࠢࡾࢁࠧዴ").format(e))
        pass
    bstack1ll1l11ll11_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ድ"))
    if bstack1ll1l11ll11_opy_:
        logger.debug(bstack1ll1l11_opy_ (u"ࠥࡊࡴࡻ࡮ࡥࠢࡦࡳࡳ࡬ࡩࡨࠢࡳࡥࡹ࡮ࠠࡪࡰࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠻ࠢࡾࢁࠧዶ").format(bstack1ll1l11ll11_opy_))
        return bstack1ll1l11ll11_opy_
    return None
def bstack1ll1l11l1l1_opy_(config):
    bstack1ll1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡊࡾࡴࡳࡣࡦࡸࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡨࡸࡥࡥࡧࡱࡸ࡮ࡧ࡬ࡴࠢࡩࡶࡴࡳࠠࡷࡣࡵ࡭ࡴࡻࡳࠡࡵࡲࡹࡷࡩࡥࡴ࠰ࠍࠤࠥࠦࠠࡑࡴ࡬ࡳࡷ࡯ࡴࡺ࠼ࠣࡉࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠤࡃࠦࡃࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡗ࡬ࡪࠦࡓࡅࡍࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡄࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡻ࡮ࡺࡨࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠍࠤࠥࠦࠠࠣࠤࠥዷ")
    credentials = {
        bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧዸ"): None,
        bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩዹ"): None
    }
    credentials[bstack1ll1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩዺ")] = (
        os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩዻ")) or
        os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗ࠭ዼ"))
    )
    credentials[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ዽ")] = (
        os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧዾ")) or
        os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡏࡊ࡟ࠧዿ"))
    )
    if not credentials[bstack1ll1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨጀ")] or not credentials[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪጁ")]:
        if config and isinstance(config, dict):
            credentials[bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪጂ")] = config.get(bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫጃ")) or config.get(bstack1ll1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࠨጄ"))
            credentials[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧጅ")] = config.get(bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨጆ")) or config.get(bstack1ll1l11_opy_ (u"࠭࡫ࡦࡻࠪጇ"))
    return credentials
def bstack1lll1111l1_opy_(config):
    bstack1ll1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡆࡺࡨࡧࡺࡺࡥࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡣࡻࠣࡨࡪࡲࡥࡨࡣࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࡖ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮࠻ࠌࠣࠤࠥࠦ࠱࠯ࠢࡈࡼࡹࡸࡡࡤࡶࡶࠤࡨࡸࡥࡥࡧࡱࡸ࡮ࡧ࡬ࡴࠢࡩࡶࡴࡳࠠࡤࡱࡱࡪ࡮࡭࠯ࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠏࠦࠠࠡࠢ࠵࠲ࠥࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡳ࠰ࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭࡫ࠦ࡮ࡦࡧࡧࡩࡩࠐࠠࠡࠢࠣ࠷࠳ࠦࡓࡱࡣࡺࡲࡸࠦࡴࡩࡧࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡸࠦࡡࠡࡵࡸࡦࡵࡸ࡯ࡤࡧࡶࡷࠥࡽࡩࡵࡪࠣ࡭ࡳ࡮ࡥࡳ࡫ࡷࡩࡩࠦࡳࡵࡦ࡬ࡳࠏࠦࠠࠡࠢ࠷࠲ࠥࡌ࡯ࡳࡹࡤࡶࡩࡹࠠࡴ࡫ࡪࡲࡦࡲࡳࠡࠪࡖࡍࡌࡏࡎࡕ࠮ࠣࡗࡎࡍࡔࡆࡔࡐ࠰ࠥ࡫ࡴࡤ࠰ࠬࠤࡹࡵࠠࡵࡪࡨࠤࡨ࡮ࡩ࡭ࡦࠣࡴࡷࡵࡣࡦࡵࡶࠎࠥࠦࠠࠡ࠷࠱ࠤࡊࡾࡩࡵࡵࠣࡻ࡮ࡺࡨࠡࡶ࡫ࡩࠥࡹࡡ࡮ࡧࠣࡧࡴࡪࡥࠡࡣࡶࠤࡹ࡮ࡥࠡࡥ࡫࡭ࡱࡪࠠࡱࡴࡲࡧࡪࡹࡳࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡔࡩࡧࠣࡗࡉࡑࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠎࠥࠦࠠࠡࠤࠥࠦገ")
    try:
        bstack1ll1l11llll_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡇࡻࡩࡨࡻࡴࡪࡰࡪࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳ࠻ࠢࡾࢁࠬጉ").format(bstack1ll1l11llll_opy_))
        credentials = bstack1ll1l11l1l1_opy_(config)
        if not credentials[bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫጊ")] or not credentials[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ጋ")]:
            logger.error(bstack1ll1l11_opy_ (u"ࠫࡆࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥ࡯࡮ࡤࡱࡰࡴࡱ࡫ࡴࡦ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡥࡩࡪࠠࡺࡱࡸࡶࠥࡻࡳࡦࡴࡑࡥࡲ࡫ࠠࡢࡰࡧࠤࡦࡩࡣࡦࡵࡶࡏࡪࡿࠠࡵࡱࠣࡩ࡮ࡺࡨࡦࡴࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥࠡࡱࡵࠤࡦࡹࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳ࠭ࠢࡷ࡬ࡪࡴࠠࡵࡴࡼࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡺࡨࡦࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡥ࡬ࡧࡩ࡯࠰ࠪጌ"))
            sys.exit(1)
        try:
            bstack1ll1l11l111_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡈࡒࡉࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠨግ").format(e))
            sys.exit(1)
        if not bstack1ll1l11l111_opy_:
            logger.error(bstack1ll1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡉࡌࡊࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠬጎ"))
            sys.exit(1)
        binary_path = bstack1ll1l111lll_opy_(bstack1ll1l11l111_opy_)
        try:
            if not binary_path:
                logger.debug(bstack1ll1l11_opy_ (u"ࠧࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦ࡬ࡢࡶࡨࡷࡹࠦࡶࡦࡴࡶ࡭ࡴࡴࠧጏ"))
                binary_path = bstack1ll1l11lll1_opy_(bstack1ll1l11_opy_ (u"ࠨࠩጐ"), bstack1ll1l11l111_opy_, credentials)
            else:
                logger.debug(bstack1ll1l11_opy_ (u"ࠩࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨ࠱ࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡻࡰࡥࡣࡷࡩࡸ࠭጑"))
                binary_path = bstack1ll1l11lll1_opy_(binary_path, bstack1ll1l11l111_opy_, credentials)
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠪࡅࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤ࡮ࡴࡣࡰ࡯ࡳࡰࡪࡺࡥ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡤࡨࡩࠦࡹࡰࡷࡵࠤࡺࡹࡥࡳࡐࡤࡱࡪࠦࡡ࡯ࡦࠣࡥࡨࡩࡥࡴࡵࡎࡩࡾࠦࡴࡰࠢࡨ࡭ࡹ࡮ࡥࡳࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫ࠠࡰࡴࠣࡥࡸࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹࠬࠡࡶ࡫ࡩࡳࠦࡴࡳࡻࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡹ࡮ࡥࠡࡥࡲࡱࡲࡧ࡮ࡥࠢࡤ࡫ࡦ࡯࡮࠯ࠩጒ"))
            logger.debug(bstack1ll1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠨጓ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack1ll1l11_opy_ (u"ࠬࡇࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡻࡲࡹࡷࠦࡵࡴࡧࡵࡒࡦࡳࡥࠡࡣࡱࡨࠥࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠡࡶࡲࠤࡪ࡯ࡴࡩࡧࡵࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠮ࠣࡸ࡭࡫࡮ࠡࡶࡵࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡦ࡭ࡡࡪࡰ࠱ࠫጔ"))
            logger.debug(bstack1ll1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡴࡸࠠ࡭ࡱࡦࡥࡹ࡫ࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠫጕ"))
            sys.exit(1)
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡔࡲࡤࡻࡳ࡯࡮ࡨ࠼ࠣࡿࢂࠦ࡬ࡰࡣࡧࠤࢀࢃࠧ጖").format(binary_path, bstack1ll1l11_opy_ (u"ࠣࠢࠥ጗").join(bstack1ll1l11llll_opy_)))
        bstack1ll1l1l111l_opy_ = [binary_path, bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡦࡪࠧጘ")] + bstack1ll1l11llll_opy_
        bstack1ll1l11l1ll_opy_ = subprocess.Popen(
            bstack1ll1l1l111l_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1ll1l11l11l_opy_(signum, frame):
            bstack1ll1l11_opy_ (u"ࠥࠦࠧࡌ࡯ࡳࡹࡤࡶࡩࠦࡳࡪࡩࡱࡥࡱࡹࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡪ࡬ࡰࡩࠦࡰࡳࡱࡦࡩࡸࡹࠢࠣࠤጙ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack1ll1l11_opy_ (u"ࠫࡗ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡳࡪࡩࡱࡥࡱࠦࡻࡾ࠮ࠣࡪࡴࡸࡷࡢࡴࡧ࡭ࡳ࡭ࠠࡵࡱࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵ࠱࠲࠳࠭ጚ").format(signum))
            if bstack1ll1l11l1ll_opy_ and bstack1ll1l11l1ll_opy_.poll() is None:
                try:
                    bstack1ll1l11l1ll_opy_.send_signal(signum)
                    logger.debug(bstack1ll1l11_opy_ (u"ࠬ࡝ࡡࡪࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵࠣࡸࡴࠦࡥࡹ࡫ࡷ࠲࠳࠴ࠧጛ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1ll1l11l11l_opy_)
        exit_code = bstack1ll1l11l1ll_opy_.wait()
        logger.debug(bstack1ll1l11_opy_ (u"࠭ࡻࡾࠢࡨࡼ࡮ࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡧࡩࠥࢁࡽࠨጜ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡪࡰ࡬ࡸ࡮ࡧࡴࡪࡰࡪࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺ࠺ࠡࡽࢀࠫጝ").format(e))
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠬጞ").format(e))
        sys.exit(1)