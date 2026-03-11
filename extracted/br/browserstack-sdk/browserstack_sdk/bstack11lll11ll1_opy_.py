# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
bstack1ll111_opy_ (u"ࠨࠢࠣࠌࡏࡳࡦࡪࠠࡕࡧࡶࡸ࡮ࡴࡧࠡࡏࡲࡨࡺࡲࡥࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠋࡊࡤࡲࡩࡲࡥࡴࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡨࡹࠡࡦࡨࡰࡪ࡭ࡡࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠌࠥࠦࠧᅎ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1llll1l1l1l_opy_,
    get_cli_dir,
    bstack1llll1l1l11_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1llll1l11l1_opy_(config):
    bstack1ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡆࡺࡷࡶࡦࡩࡴࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡸ࡭ࠦࡦࡳࡱࡰࠤࡨࡵ࡭࡮ࡣࡱࡨ࠲ࡲࡩ࡯ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦ࡯ࡳࠢࡦࡳࡳ࡬ࡩࡨ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡖ࡫ࡩ࡙ࠥࡄࡌࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡳࡵࡴ࠽ࠤࡕࡧࡴࡩࠢࡷࡳࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠤࠥࠦᅏ")
    try:
        if bstack1ll111_opy_ (u"ࠨ࠯࠰ࡧࡴࡴࡦࡪࡩࠪᅐ") in sys.argv:
            bstack1llll1l11ll_opy_ = sys.argv.index(bstack1ll111_opy_ (u"ࠩ࠰࠱ࡨࡵ࡮ࡧ࡫ࡪࠫᅑ"))
            if bstack1llll1l11ll_opy_ + 1 < len(sys.argv):
                bstack1llll1ll11l_opy_ = sys.argv[bstack1llll1l11ll_opy_ + 1]
                logger.debug(bstack1ll111_opy_ (u"ࠥࡊࡴࡻ࡮ࡥࠢ࠰࠱ࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡲࡡࡨࠢࡺ࡭ࡹ࡮ࠠࡱࡣࡷ࡬࠿ࠦࡻࡾࠤᅒ").format(bstack1llll1ll11l_opy_))
                return bstack1llll1ll11l_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack1ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤ࠲࠳ࡣࡰࡰࡩ࡭࡬ࠦࡦ࡭ࡣࡪ࠾ࠥࢁࡽࠣᅓ").format(e))
        pass
    bstack1llll1ll11l_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩᅔ"))
    if bstack1llll1ll11l_opy_:
        logger.debug(bstack1ll111_opy_ (u"ࠨࡆࡰࡷࡱࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥࡶࡡࡵࡪࠣ࡭ࡳࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࢁࡽࠣᅕ").format(bstack1llll1ll11l_opy_))
        return bstack1llll1ll11l_opy_
    return None
def bstack1llll1ll1ll_opy_(config):
    bstack1ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡆࡺࡷࡶࡦࡩࡴࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡤࡴࡨࡨࡪࡴࡴࡪࡣ࡯ࡷࠥ࡬ࡲࡰ࡯ࠣࡺࡦࡸࡩࡰࡷࡶࠤࡸࡵࡵࡳࡥࡨࡷ࠳ࠐࠠࠡࠢࠣࡔࡷ࡯࡯ࡳ࡫ࡷࡽ࠿ࠦࡅ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹࠠ࠿ࠢࡆࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪ࠾࡚ࠥࡨࡦࠢࡖࡈࡐࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡇ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡷࡪࡶ࡫ࠤࡺࡹࡥࡳࡐࡤࡱࡪࠦࡡ࡯ࡦࠣࡥࡨࡩࡥࡴࡵࡎࡩࡾࠐࠠࠡࠢࠣࠦࠧࠨᅖ")
    credentials = {
        bstack1ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᅗ"): None,
        bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᅘ"): None
    }
    credentials[bstack1ll111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᅙ")] = (
        os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᅚ")) or
        os.environ.get(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࠩᅛ"))
    )
    credentials[bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᅜ")] = (
        os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᅝ")) or
        os.environ.get(bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙ࡋࡆ࡛ࠪᅞ"))
    )
    if not credentials[bstack1ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᅟ")] or not credentials[bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᅠ")]:
        if config and isinstance(config, dict):
            credentials[bstack1ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᅡ")] = config.get(bstack1ll111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᅢ")) or config.get(bstack1ll111_opy_ (u"࠭ࡵࡴࡧࡵࠫᅣ"))
            credentials[bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᅤ")] = config.get(bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᅥ")) or config.get(bstack1ll111_opy_ (u"ࠩ࡮ࡩࡾ࠭ᅦ"))
    return credentials
def bstack1ll11llll1_opy_(config):
    bstack1ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡉࡽ࡫ࡣࡶࡶࡨࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡦࡾࠦࡤࡦ࡮ࡨ࡫ࡦࡺࡩ࡯ࡩࠣࡸࡴࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱ࠾ࠏࠦࠠࠡࠢ࠴࠲ࠥࡋࡸࡵࡴࡤࡧࡹࡹࠠࡤࡴࡨࡨࡪࡴࡴࡪࡣ࡯ࡷࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡴࡦࡪࡩ࠲ࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠋࠢࠣࠤࠥ࠸࠮ࠡࡆࡲࡻࡳࡲ࡯ࡢࡦࡶ࠳ࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠦࡩࡧࠢࡱࡩࡪࡪࡥࡥࠌࠣࠤࠥࠦ࠳࠯ࠢࡖࡴࡦࡽ࡮ࡴࠢࡷ࡬ࡪࠦࡢࡪࡰࡤࡶࡾࠦࡡࡴࠢࡤࠤࡸࡻࡢࡱࡴࡲࡧࡪࡹࡳࠡࡹ࡬ࡸ࡭ࠦࡩ࡯ࡪࡨࡶ࡮ࡺࡥࡥࠢࡶࡸࡩ࡯࡯ࠋࠢࠣࠤࠥ࠺࠮ࠡࡈࡲࡶࡼࡧࡲࡥࡵࠣࡷ࡮࡭࡮ࡢ࡮ࡶࠤ࡙࠭ࡉࡈࡋࡑࡘ࠱ࠦࡓࡊࡉࡗࡉࡗࡓࠬࠡࡧࡷࡧ࠳࠯ࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡪ࡬ࡰࡩࠦࡰࡳࡱࡦࡩࡸࡹࠊࠡࠢࠣࠤ࠺࠴ࠠࡆࡺ࡬ࡸࡸࠦࡷࡪࡶ࡫ࠤࡹ࡮ࡥࠡࡵࡤࡱࡪࠦࡣࡰࡦࡨࠤࡦࡹࠠࡵࡪࡨࠤࡨ࡮ࡩ࡭ࡦࠣࡴࡷࡵࡣࡦࡵࡶࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡗ࡬ࡪࠦࡓࡅࡍࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠊࠡࠢࠣࠤࠧࠨࠢᅧ")
    try:
        bstack1llll1ll1l1_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack1ll111_opy_ (u"ࠫࡊࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶࠣࡻ࡮ࡺࡨࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࠾ࠥࢁࡽࠨᅨ").format(bstack1llll1ll1l1_opy_))
        credentials = bstack1llll1ll1ll_opy_(config)
        if not credentials[bstack1ll111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᅩ")] or not credentials[bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᅪ")]:
            logger.error(bstack1ll111_opy_ (u"ࠧࡂࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡽࡴࡻࡲࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠣࡸࡴࠦࡥࡪࡶ࡫ࡩࡷࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠰ࠥࡺࡨࡦࡰࠣࡸࡷࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡡࡨࡣ࡬ࡲ࠳࠭ᅫ"))
            sys.exit(1)
        try:
            bstack1llll1ll111_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack1ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡄࡎࡌࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠫᅬ").format(e))
            sys.exit(1)
        if not bstack1llll1ll111_opy_:
            logger.error(bstack1ll111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡅࡏࡍࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠨᅭ"))
            sys.exit(1)
        binary_path = bstack1llll1l1l11_opy_(bstack1llll1ll111_opy_)
        try:
            if not binary_path:
                logger.debug(bstack1ll111_opy_ (u"ࠪࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢ࡯ࡥࡹ࡫ࡳࡵࠢࡹࡩࡷࡹࡩࡰࡰࠪᅮ"))
                binary_path = bstack1llll1l1l1l_opy_(bstack1ll111_opy_ (u"ࠫࠬᅯ"), bstack1llll1ll111_opy_, credentials)
            else:
                logger.debug(bstack1ll111_opy_ (u"ࠬࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤ࠭ࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡷࡳࡨࡦࡺࡥࡴࠩᅰ"))
                binary_path = bstack1llll1l1l1l_opy_(binary_path, bstack1llll1ll111_opy_, credentials)
        except Exception as e:
            logger.error(bstack1ll111_opy_ (u"࠭ࡁࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡼࡳࡺࡸࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠢࡷࡳࠥ࡫ࡩࡵࡪࡨࡶࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠯ࠤࡹ࡮ࡥ࡯ࠢࡷࡶࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡧࡧࡢ࡫ࡱ࠲ࠬᅱ"))
            logger.debug(bstack1ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠫᅲ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack1ll111_opy_ (u"ࠨࡃࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡲࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡾࡵࡵࡳࠢࡸࡷࡪࡸࡎࡢ࡯ࡨࠤࡦࡴࡤࠡࡣࡦࡧࡪࡹࡳࡌࡧࡼࠤࡹࡵࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡧ࡫࡯ࡩࠥࡵࡲࠡࡣࡶࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷ࠱ࠦࡴࡩࡧࡱࠤࡹࡸࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡣࡰ࡯ࡰࡥࡳࡪࠠࡢࡩࡤ࡭ࡳ࠴ࠧᅳ"))
            logger.debug(bstack1ll111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡰࡴࠣࡰࡴࡩࡡࡵࡧࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠧᅴ"))
            sys.exit(1)
        logger.debug(bstack1ll111_opy_ (u"ࠪࡗࡵࡧࡷ࡯࡫ࡱ࡫࠿ࠦࡻࡾࠢ࡯ࡳࡦࡪࠠࡼࡿࠪᅵ").format(binary_path, bstack1ll111_opy_ (u"ࠦࠥࠨᅶ").join(bstack1llll1ll1l1_opy_)))
        bstack1llll1l111l_opy_ = [binary_path, bstack1ll111_opy_ (u"ࠬࡲ࡯ࡢࡦࠪᅷ")] + bstack1llll1ll1l1_opy_
        bstack1llll1l1ll1_opy_ = subprocess.Popen(
            bstack1llll1l111l_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1llll1l1lll_opy_(signum, frame):
            bstack1ll111_opy_ (u"ࠨࠢࠣࡈࡲࡶࡼࡧࡲࡥࠢࡶ࡭࡬ࡴࡡ࡭ࡵࠣࡸࡴࠦࡴࡩࡧࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵࠥࠦࠧᅸ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack1ll111_opy_ (u"ࠧࡓࡧࡦࡩ࡮ࡼࡥࡥࠢࡶ࡭࡬ࡴࡡ࡭ࠢࡾࢁ࠱ࠦࡦࡰࡴࡺࡥࡷࡪࡩ࡯ࡩࠣࡸࡴࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸ࠴࠮࠯ࠩᅹ").format(signum))
            if bstack1llll1l1ll1_opy_ and bstack1llll1l1ll1_opy_.poll() is None:
                try:
                    bstack1llll1l1ll1_opy_.send_signal(signum)
                    logger.debug(bstack1ll111_opy_ (u"ࠨ࡙ࡤ࡭ࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸࠦࡴࡰࠢࡨࡼ࡮ࡺ࠮࠯࠰ࠪᅺ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1llll1l1lll_opy_)
        exit_code = bstack1llll1l1ll1_opy_.wait()
        logger.debug(bstack1ll111_opy_ (u"ࠩࡾࢁࠥ࡫ࡸࡪࡶࡨࡨࠥࡽࡩࡵࡪࠣࡧࡴࡪࡥࠡࡽࢀࠫᅻ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack1ll111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣ࡭ࡳ࡯ࡴࡪࡣࡷ࡭ࡳ࡭ࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࠽ࠤࢀࢃࠧᅼ").format(e))
        logger.debug(bstack1ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠨᅽ").format(e))
        sys.exit(1)