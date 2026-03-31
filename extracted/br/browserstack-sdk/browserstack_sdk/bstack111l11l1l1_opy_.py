# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
bstack1ll11_opy_ (u"ࠦࠧࠨࠊࡍࡱࡤࡨ࡚ࠥࡥࡴࡶ࡬ࡲ࡬ࠦࡍࡰࡦࡸࡰࡪࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠐࡈࡢࡰࡧࡰࡪࡹࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡦࡾࠦࡤࡦ࡮ࡨ࡫ࡦࡺࡩ࡯ࡩࠣࡸࡴࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾ࠴ࠊࠣࠤࠥᇘ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1lll1l1l11l_opy_,
    get_cli_dir,
    bstack1lll1l1l111_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1lll1l11111_opy_(config):
    bstack1ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡋࡸࡵࡴࡤࡧࡹࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡶ࡫ࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡲࡳࡡ࡯ࡦ࠰ࡰ࡮ࡴࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤࡴࡸࠠࡤࡱࡱࡪ࡮࡭࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡔࡩࡧࠣࡗࡉࡑࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡸࡺࡲ࠻ࠢࡓࡥࡹ࡮ࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠡࡱࡵࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠢࠣࠤᇙ")
    try:
        if bstack1ll11_opy_ (u"࠭࠭࠮ࡥࡲࡲ࡫࡯ࡧࠨᇚ") in sys.argv:
            bstack1lll1l11l1l_opy_ = sys.argv.index(bstack1ll11_opy_ (u"ࠧ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠩᇛ"))
            if bstack1lll1l11l1l_opy_ + 1 < len(sys.argv):
                bstack1lll1l11l11_opy_ = sys.argv[bstack1lll1l11l1l_opy_ + 1]
                logger.debug(bstack1ll11_opy_ (u"ࠣࡈࡲࡹࡳࡪࠠ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠢࡩࡰࡦ࡭ࠠࡸ࡫ࡷ࡬ࠥࡶࡡࡵࡪ࠽ࠤࢀࢃࠢᇜ").format(bstack1lll1l11l11_opy_))
                return bstack1lll1l11l11_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack1ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢ࠰࠱ࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡲࡡࡨ࠼ࠣࡿࢂࠨᇝ").format(e))
        pass
    bstack1lll1l11l11_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧᇞ"))
    if bstack1lll1l11l11_opy_:
        logger.debug(bstack1ll11_opy_ (u"ࠦࡋࡵࡵ࡯ࡦࠣࡧࡴࡴࡦࡪࡩࠣࡴࡦࡺࡨࠡ࡫ࡱࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠼ࠣࡿࢂࠨᇟ").format(bstack1lll1l11l11_opy_))
        return bstack1lll1l11l11_opy_
    return None
def bstack1lll1l11lll_opy_(config):
    bstack1ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡋࡸࡵࡴࡤࡧࡹࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡩࡲࡦࡦࡨࡲࡹ࡯ࡡ࡭ࡵࠣࡪࡷࡵ࡭ࠡࡸࡤࡶ࡮ࡵࡵࡴࠢࡶࡳࡺࡸࡣࡦࡵ࠱ࠎࠥࠦࠠࠡࡒࡵ࡭ࡴࡸࡩࡵࡻ࠽ࠤࡊࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠥࡄࠠࡄࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡘ࡭࡫ࠠࡔࡆࡎࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡅ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡼ࡯ࡴࡩࠢࡸࡷࡪࡸࡎࡢ࡯ࡨࠤࡦࡴࡤࠡࡣࡦࡧࡪࡹࡳࡌࡧࡼࠎࠥࠦࠠࠡࠤࠥࠦᇠ")
    credentials = {
        bstack1ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᇡ"): None,
        bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᇢ"): None
    }
    credentials[bstack1ll11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᇣ")] = (
        os.environ.get(bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪᇤ")) or
        os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࠧᇥ"))
    )
    credentials[bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᇦ")] = (
        os.environ.get(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᇧ")) or
        os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡐࡋ࡙ࠨᇨ"))
    )
    if not credentials[bstack1ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᇩ")] or not credentials[bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᇪ")]:
        if config and isinstance(config, dict):
            credentials[bstack1ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᇫ")] = config.get(bstack1ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᇬ")) or config.get(bstack1ll11_opy_ (u"ࠫࡺࡹࡥࡳࠩᇭ"))
            credentials[bstack1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᇮ")] = config.get(bstack1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᇯ")) or config.get(bstack1ll11_opy_ (u"ࠧ࡬ࡧࡼࠫᇰ"))
    return credentials
def bstack11l1l11ll1_opy_(config):
    bstack1ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡇࡻࡩࡨࡻࡴࡦࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡤࡼࠤࡩ࡫࡬ࡦࡩࡤࡸ࡮ࡴࡧࠡࡶࡲࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯࠼ࠍࠤࠥࠦࠠ࠲࠰ࠣࡉࡽࡺࡲࡢࡥࡷࡷࠥࡩࡲࡦࡦࡨࡲࡹ࡯ࡡ࡭ࡵࠣࡪࡷࡵ࡭ࠡࡥࡲࡲ࡫࡯ࡧ࠰ࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠐࠠࠡࠢࠣ࠶࠳ࠦࡄࡰࡹࡱࡰࡴࡧࡤࡴ࠱ࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮࡬ࠠ࡯ࡧࡨࡨࡪࡪࠊࠡࠢࠣࠤ࠸࠴ࠠࡔࡲࡤࡻࡳࡹࠠࡵࡪࡨࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡹࠠࡢࠢࡶࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡷࡪࡶ࡫ࠤ࡮ࡴࡨࡦࡴ࡬ࡸࡪࡪࠠࡴࡶࡧ࡭ࡴࠐࠠࠡࠢࠣ࠸࠳ࠦࡆࡰࡴࡺࡥࡷࡪࡳࠡࡵ࡬࡫ࡳࡧ࡬ࡴࠢࠫࡗࡎࡍࡉࡏࡖ࠯ࠤࡘࡏࡇࡕࡇࡕࡑ࠱ࠦࡥࡵࡥ࠱࠭ࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠏࠦࠠࠡࠢ࠸࠲ࠥࡋࡸࡪࡶࡶࠤࡼ࡯ࡴࡩࠢࡷ࡬ࡪࠦࡳࡢ࡯ࡨࠤࡨࡵࡤࡦࠢࡤࡷࠥࡺࡨࡦࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡕࡪࡨࠤࡘࡊࡋࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠏࠦࠠࠡࠢࠥࠦࠧᇱ")
    try:
        bstack1lll1l11ll1_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack1ll11_opy_ (u"ࠩࡈࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴ࠼ࠣࡿࢂ࠭ᇲ").format(bstack1lll1l11ll1_opy_))
        credentials = bstack1lll1l11lll_opy_(config)
        if not credentials[bstack1ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᇳ")] or not credentials[bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᇴ")]:
            logger.error(bstack1ll11_opy_ (u"ࠬࡇࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡻࡲࡹࡷࠦࡵࡴࡧࡵࡒࡦࡳࡥࠡࡣࡱࡨࠥࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠡࡶࡲࠤࡪ࡯ࡴࡩࡧࡵࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠮ࠣࡸ࡭࡫࡮ࠡࡶࡵࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡦ࡭ࡡࡪࡰ࠱ࠫᇵ"))
            sys.exit(1)
        try:
            bstack1lll1l111ll_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack1ll11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡉࡌࡊࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠩᇶ").format(e))
            sys.exit(1)
        if not bstack1lll1l111ll_opy_:
            logger.error(bstack1ll11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡃࡍࡋࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠭ᇷ"))
            sys.exit(1)
        binary_path = bstack1lll1l1l111_opy_(bstack1lll1l111ll_opy_)
        try:
            if not binary_path:
                logger.debug(bstack1ll11_opy_ (u"ࠨࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡭ࡣࡷࡩࡸࡺࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠨᇸ"))
                binary_path = bstack1lll1l1l11l_opy_(bstack1ll11_opy_ (u"ࠩࠪᇹ"), bstack1lll1l111ll_opy_, credentials)
            else:
                logger.debug(bstack1ll11_opy_ (u"ࠪࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩ࠲ࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡵࡱࡦࡤࡸࡪࡹࠧᇺ"))
                binary_path = bstack1lll1l1l11l_opy_(binary_path, bstack1lll1l111ll_opy_, credentials)
        except Exception as e:
            logger.error(bstack1ll11_opy_ (u"ࠫࡆࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥ࡯࡮ࡤࡱࡰࡴࡱ࡫ࡴࡦ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡥࡩࡪࠠࡺࡱࡸࡶࠥࡻࡳࡦࡴࡑࡥࡲ࡫ࠠࡢࡰࡧࠤࡦࡩࡣࡦࡵࡶࡏࡪࡿࠠࡵࡱࠣࡩ࡮ࡺࡨࡦࡴࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥࠡࡱࡵࠤࡦࡹࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳ࠭ࠢࡷ࡬ࡪࡴࠠࡵࡴࡼࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡺࡨࡦࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡥ࡬ࡧࡩ࡯࠰ࠪᇻ"))
            logger.debug(bstack1ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩᇼ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack1ll11_opy_ (u"࠭ࡁࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡼࡳࡺࡸࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠢࡷࡳࠥ࡫ࡩࡵࡪࡨࡶࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠯ࠤࡹ࡮ࡥ࡯ࠢࡷࡶࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡧࡧࡢ࡫ࡱ࠲ࠬᇽ"))
            logger.debug(bstack1ll11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡵࡲࠡ࡮ࡲࡧࡦࡺࡥࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠬᇾ"))
            sys.exit(1)
        logger.debug(bstack1ll11_opy_ (u"ࠨࡕࡳࡥࡼࡴࡩ࡯ࡩ࠽ࠤࢀࢃࠠ࡭ࡱࡤࡨࠥࢁࡽࠨᇿ").format(binary_path, bstack1ll11_opy_ (u"ࠤࠣࠦሀ").join(bstack1lll1l11ll1_opy_)))
        bstack1lll1l111l1_opy_ = [binary_path, bstack1ll11_opy_ (u"ࠪࡰࡴࡧࡤࠨሁ")] + bstack1lll1l11ll1_opy_
        bstack1lll1l1l1l1_opy_ = subprocess.Popen(
            bstack1lll1l111l1_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1lll1l1111l_opy_(signum, frame):
            bstack1ll11_opy_ (u"ࠦࠧࠨࡆࡰࡴࡺࡥࡷࡪࠠࡴ࡫ࡪࡲࡦࡲࡳࠡࡶࡲࠤࡹ࡮ࡥࠡࡥ࡫࡭ࡱࡪࠠࡱࡴࡲࡧࡪࡹࡳࠣࠤࠥሂ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack1ll11_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡴ࡫ࡪࡲࡦࡲࠠࡼࡿ࠯ࠤ࡫ࡵࡲࡸࡣࡵࡨ࡮ࡴࡧࠡࡶࡲࠤࡨ࡮ࡩ࡭ࡦࠣࡴࡷࡵࡣࡦࡵࡶ࠲࠳࠴ࠧሃ").format(signum))
            if bstack1lll1l1l1l1_opy_ and bstack1lll1l1l1l1_opy_.poll() is None:
                try:
                    bstack1lll1l1l1l1_opy_.send_signal(signum)
                    logger.debug(bstack1ll11_opy_ (u"࠭ࡗࡢ࡫ࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡨ࡮ࡩ࡭ࡦࠣࡴࡷࡵࡣࡦࡵࡶࠤࡹࡵࠠࡦࡺ࡬ࡸ࠳࠴࠮ࠨሄ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1lll1l1111l_opy_)
        exit_code = bstack1lll1l1l1l1_opy_.wait()
        logger.debug(bstack1ll11_opy_ (u"ࠧࡼࡿࠣࡩࡽ࡯ࡴࡦࡦࠣࡻ࡮ࡺࡨࠡࡥࡲࡨࡪࠦࡻࡾࠩህ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack1ll11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡ࡫ࡱ࡭ࡹ࡯ࡡࡵ࡫ࡱ࡫ࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴ࠻ࠢࡾࢁࠬሆ").format(e))
        logger.debug(bstack1ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡦࡨࡸࡦ࡯࡬ࡴ࠼ࠣࡿࢂ࠭ሇ").format(e))
        sys.exit(1)