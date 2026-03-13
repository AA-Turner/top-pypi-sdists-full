# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
bstack1111l_opy_ (u"ࠦࠧࠨࠊࡍࡱࡤࡨ࡚ࠥࡥࡴࡶ࡬ࡲ࡬ࠦࡍࡰࡦࡸࡰࡪࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠐࡈࡢࡰࡧࡰࡪࡹࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡦࡾࠦࡤࡦ࡮ࡨ࡫ࡦࡺࡩ࡯ࡩࠣࡸࡴࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾ࠴ࠊࠣࠤࠥᆄ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1llll1l111l_opy_,
    get_cli_dir,
    bstack1llll1l11ll_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1llll1l1lll_opy_(config):
    bstack1111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡋࡸࡵࡴࡤࡧࡹࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡶ࡫ࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡲࡳࡡ࡯ࡦ࠰ࡰ࡮ࡴࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤࡴࡸࠠࡤࡱࡱࡪ࡮࡭࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡔࡩࡧࠣࡗࡉࡑࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡸࡺࡲ࠻ࠢࡓࡥࡹ࡮ࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠡࡱࡵࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠢࠣࠤᆅ")
    try:
        if bstack1111l_opy_ (u"࠭࠭࠮ࡥࡲࡲ࡫࡯ࡧࠨᆆ") in sys.argv:
            bstack1llll1l11l1_opy_ = sys.argv.index(bstack1111l_opy_ (u"ࠧ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠩᆇ"))
            if bstack1llll1l11l1_opy_ + 1 < len(sys.argv):
                bstack1llll1l1ll1_opy_ = sys.argv[bstack1llll1l11l1_opy_ + 1]
                logger.debug(bstack1111l_opy_ (u"ࠣࡈࡲࡹࡳࡪࠠ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠢࡩࡰࡦ࡭ࠠࡸ࡫ࡷ࡬ࠥࡶࡡࡵࡪ࠽ࠤࢀࢃࠢᆈ").format(bstack1llll1l1ll1_opy_))
                return bstack1llll1l1ll1_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢ࠰࠱ࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡲࡡࡨ࠼ࠣࡿࢂࠨᆉ").format(e))
        pass
    bstack1llll1l1ll1_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧᆊ"))
    if bstack1llll1l1ll1_opy_:
        logger.debug(bstack1111l_opy_ (u"ࠦࡋࡵࡵ࡯ࡦࠣࡧࡴࡴࡦࡪࡩࠣࡴࡦࡺࡨࠡ࡫ࡱࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠼ࠣࡿࢂࠨᆋ").format(bstack1llll1l1ll1_opy_))
        return bstack1llll1l1ll1_opy_
    return None
def bstack1llll11llll_opy_(config):
    bstack1111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡋࡸࡵࡴࡤࡧࡹࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡩࡲࡦࡦࡨࡲࡹ࡯ࡡ࡭ࡵࠣࡪࡷࡵ࡭ࠡࡸࡤࡶ࡮ࡵࡵࡴࠢࡶࡳࡺࡸࡣࡦࡵ࠱ࠎࠥࠦࠠࠡࡒࡵ࡭ࡴࡸࡩࡵࡻ࠽ࠤࡊࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠥࡄࠠࡄࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡘ࡭࡫ࠠࡔࡆࡎࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡅ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡼ࡯ࡴࡩࠢࡸࡷࡪࡸࡎࡢ࡯ࡨࠤࡦࡴࡤࠡࡣࡦࡧࡪࡹࡳࡌࡧࡼࠎࠥࠦࠠࠡࠤࠥࠦᆌ")
    credentials = {
        bstack1111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᆍ"): None,
        bstack1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᆎ"): None
    }
    credentials[bstack1111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᆏ")] = (
        os.environ.get(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪᆐ")) or
        os.environ.get(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࠧᆑ"))
    )
    credentials[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᆒ")] = (
        os.environ.get(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᆓ")) or
        os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡐࡋ࡙ࠨᆔ"))
    )
    if not credentials[bstack1111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᆕ")] or not credentials[bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᆖ")]:
        if config and isinstance(config, dict):
            credentials[bstack1111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᆗ")] = config.get(bstack1111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᆘ")) or config.get(bstack1111l_opy_ (u"ࠫࡺࡹࡥࡳࠩᆙ"))
            credentials[bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᆚ")] = config.get(bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᆛ")) or config.get(bstack1111l_opy_ (u"ࠧ࡬ࡧࡼࠫᆜ"))
    return credentials
def bstack1lllll1111_opy_(config):
    bstack1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡇࡻࡩࡨࡻࡴࡦࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡤࡼࠤࡩ࡫࡬ࡦࡩࡤࡸ࡮ࡴࡧࠡࡶࡲࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯࠼ࠍࠤࠥࠦࠠ࠲࠰ࠣࡉࡽࡺࡲࡢࡥࡷࡷࠥࡩࡲࡦࡦࡨࡲࡹ࡯ࡡ࡭ࡵࠣࡪࡷࡵ࡭ࠡࡥࡲࡲ࡫࡯ࡧ࠰ࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠐࠠࠡࠢࠣ࠶࠳ࠦࡄࡰࡹࡱࡰࡴࡧࡤࡴ࠱ࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮࡬ࠠ࡯ࡧࡨࡨࡪࡪࠊࠡࠢࠣࠤ࠸࠴ࠠࡔࡲࡤࡻࡳࡹࠠࡵࡪࡨࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡹࠠࡢࠢࡶࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡷࡪࡶ࡫ࠤ࡮ࡴࡨࡦࡴ࡬ࡸࡪࡪࠠࡴࡶࡧ࡭ࡴࠐࠠࠡࠢࠣ࠸࠳ࠦࡆࡰࡴࡺࡥࡷࡪࡳࠡࡵ࡬࡫ࡳࡧ࡬ࡴࠢࠫࡗࡎࡍࡉࡏࡖ࠯ࠤࡘࡏࡇࡕࡇࡕࡑ࠱ࠦࡥࡵࡥ࠱࠭ࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠏࠦࠠࠡࠢ࠸࠲ࠥࡋࡸࡪࡶࡶࠤࡼ࡯ࡴࡩࠢࡷ࡬ࡪࠦࡳࡢ࡯ࡨࠤࡨࡵࡤࡦࠢࡤࡷࠥࡺࡨࡦࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡕࡪࡨࠤࡘࡊࡋࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠏࠦࠠࠡࠢࠥࠦࠧᆝ")
    try:
        bstack1llll11ll1l_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack1111l_opy_ (u"ࠩࡈࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴ࠼ࠣࡿࢂ࠭ᆞ").format(bstack1llll11ll1l_opy_))
        credentials = bstack1llll11llll_opy_(config)
        if not credentials[bstack1111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᆟ")] or not credentials[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᆠ")]:
            logger.error(bstack1111l_opy_ (u"ࠬࡇࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡻࡲࡹࡷࠦࡵࡴࡧࡵࡒࡦࡳࡥࠡࡣࡱࡨࠥࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠡࡶࡲࠤࡪ࡯ࡴࡩࡧࡵࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠮ࠣࡸ࡭࡫࡮ࠡࡶࡵࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡦ࡭ࡡࡪࡰ࠱ࠫᆡ"))
            sys.exit(1)
        try:
            bstack1llll1l1111_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack1111l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡉࡌࡊࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠩᆢ").format(e))
            sys.exit(1)
        if not bstack1llll1l1111_opy_:
            logger.error(bstack1111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡃࡍࡋࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠭ᆣ"))
            sys.exit(1)
        binary_path = bstack1llll1l11ll_opy_(bstack1llll1l1111_opy_)
        try:
            if not binary_path:
                logger.debug(bstack1111l_opy_ (u"ࠨࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡭ࡣࡷࡩࡸࡺࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠨᆤ"))
                binary_path = bstack1llll1l111l_opy_(bstack1111l_opy_ (u"ࠩࠪᆥ"), bstack1llll1l1111_opy_, credentials)
            else:
                logger.debug(bstack1111l_opy_ (u"ࠪࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩ࠲ࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡵࡱࡦࡤࡸࡪࡹࠧᆦ"))
                binary_path = bstack1llll1l111l_opy_(binary_path, bstack1llll1l1111_opy_, credentials)
        except Exception as e:
            logger.error(bstack1111l_opy_ (u"ࠫࡆࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥ࡯࡮ࡤࡱࡰࡴࡱ࡫ࡴࡦ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡥࡩࡪࠠࡺࡱࡸࡶࠥࡻࡳࡦࡴࡑࡥࡲ࡫ࠠࡢࡰࡧࠤࡦࡩࡣࡦࡵࡶࡏࡪࡿࠠࡵࡱࠣࡩ࡮ࡺࡨࡦࡴࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥࠡࡱࡵࠤࡦࡹࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳ࠭ࠢࡷ࡬ࡪࡴࠠࡵࡴࡼࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡺࡨࡦࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡥ࡬ࡧࡩ࡯࠰ࠪᆧ"))
            logger.debug(bstack1111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩᆨ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack1111l_opy_ (u"࠭ࡁࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡼࡳࡺࡸࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠢࡷࡳࠥ࡫ࡩࡵࡪࡨࡶࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠯ࠤࡹ࡮ࡥ࡯ࠢࡷࡶࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡧࡧࡢ࡫ࡱ࠲ࠬᆩ"))
            logger.debug(bstack1111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡵࡲࠡ࡮ࡲࡧࡦࡺࡥࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠬᆪ"))
            sys.exit(1)
        logger.debug(bstack1111l_opy_ (u"ࠨࡕࡳࡥࡼࡴࡩ࡯ࡩ࠽ࠤࢀࢃࠠ࡭ࡱࡤࡨࠥࢁࡽࠨᆫ").format(binary_path, bstack1111l_opy_ (u"ࠤࠣࠦᆬ").join(bstack1llll11ll1l_opy_)))
        bstack1llll11lll1_opy_ = [binary_path, bstack1111l_opy_ (u"ࠪࡰࡴࡧࡤࠨᆭ")] + bstack1llll11ll1l_opy_
        bstack1llll1l1l1l_opy_ = subprocess.Popen(
            bstack1llll11lll1_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1llll1l1l11_opy_(signum, frame):
            bstack1111l_opy_ (u"ࠦࠧࠨࡆࡰࡴࡺࡥࡷࡪࠠࡴ࡫ࡪࡲࡦࡲࡳࠡࡶࡲࠤࡹ࡮ࡥࠡࡥ࡫࡭ࡱࡪࠠࡱࡴࡲࡧࡪࡹࡳࠣࠤࠥᆮ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack1111l_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡴ࡫ࡪࡲࡦࡲࠠࡼࡿ࠯ࠤ࡫ࡵࡲࡸࡣࡵࡨ࡮ࡴࡧࠡࡶࡲࠤࡨ࡮ࡩ࡭ࡦࠣࡴࡷࡵࡣࡦࡵࡶ࠲࠳࠴ࠧᆯ").format(signum))
            if bstack1llll1l1l1l_opy_ and bstack1llll1l1l1l_opy_.poll() is None:
                try:
                    bstack1llll1l1l1l_opy_.send_signal(signum)
                    logger.debug(bstack1111l_opy_ (u"࠭ࡗࡢ࡫ࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡨ࡮ࡩ࡭ࡦࠣࡴࡷࡵࡣࡦࡵࡶࠤࡹࡵࠠࡦࡺ࡬ࡸ࠳࠴࠮ࠨᆰ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1llll1l1l11_opy_)
        exit_code = bstack1llll1l1l1l_opy_.wait()
        logger.debug(bstack1111l_opy_ (u"ࠧࡼࡿࠣࡩࡽ࡯ࡴࡦࡦࠣࡻ࡮ࡺࡨࠡࡥࡲࡨࡪࠦࡻࡾࠩᆱ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack1111l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡ࡫ࡱ࡭ࡹ࡯ࡡࡵ࡫ࡱ࡫ࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴ࠻ࠢࡾࢁࠬᆲ").format(e))
        logger.debug(bstack1111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡦࡨࡸࡦ࡯࡬ࡴ࠼ࠣࡿࢂ࠭ᆳ").format(e))
        sys.exit(1)