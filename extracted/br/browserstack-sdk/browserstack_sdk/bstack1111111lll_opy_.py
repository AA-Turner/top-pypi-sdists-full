# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
bstack11lll1_opy_ (u"ࠧࠨࠢࠋࡎࡲࡥࡩࠦࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡎࡱࡧࡹࡱ࡫ࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠊࡉࡣࡱࡨࡱ࡫ࡳࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡧࡿࠠࡥࡧ࡯ࡩ࡬ࡧࡴࡪࡰࡪࠤࡹࡵࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠋࠤࠥࠦᆯ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1lll1ll11l1_opy_,
    get_cli_dir,
    bstack1lll1ll1l1l_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1lll1lll1ll_opy_(config):
    bstack11lll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡷ࡬ࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧ࠱ࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥࡵࡲࠡࡥࡲࡲ࡫࡯ࡧ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡕࡪࡨࠤࡘࡊࡋࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡹࡴࡳ࠼ࠣࡔࡦࡺࡨࠡࡶࡲࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠣࠤࠥᆰ")
    try:
        if bstack11lll1_opy_ (u"ࠧ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠩᆱ") in sys.argv:
            bstack1lll1ll1ll1_opy_ = sys.argv.index(bstack11lll1_opy_ (u"ࠨ࠯࠰ࡧࡴࡴࡦࡪࡩࠪᆲ"))
            if bstack1lll1ll1ll1_opy_ + 1 < len(sys.argv):
                bstack1lll1lll11l_opy_ = sys.argv[bstack1lll1ll1ll1_opy_ + 1]
                logger.debug(bstack11lll1_opy_ (u"ࠤࡉࡳࡺࡴࡤࠡ࠯࠰ࡧࡴࡴࡦࡪࡩࠣࡪࡱࡧࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡶ࡫࠾ࠥࢁࡽࠣᆳ").format(bstack1lll1lll11l_opy_))
                return bstack1lll1lll11l_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack11lll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡬ࡢࡩ࠽ࠤࢀࢃࠢᆴ").format(e))
        pass
    bstack1lll1lll11l_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨᆵ"))
    if bstack1lll1lll11l_opy_:
        logger.debug(bstack11lll1_opy_ (u"ࠧࡌ࡯ࡶࡰࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡵࡧࡴࡩࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠽ࠤࢀࢃࠢᆶ").format(bstack1lll1lll11l_opy_))
        return bstack1lll1lll11l_opy_
    return None
def bstack1lll1ll1l11_opy_(config):
    bstack11lll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡹࡥࡷ࡯࡯ࡶࡵࠣࡷࡴࡻࡲࡤࡧࡶ࠲ࠏࠦࠠࠡࠢࡓࡶ࡮ࡵࡲࡪࡶࡼ࠾ࠥࡋ࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸࠦ࠾ࠡࡅࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡦࡪࡩ࠽ࠤ࡙࡮ࡥࠡࡕࡇࡏࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡆ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡽࡩࡵࡪࠣࡹࡸ࡫ࡲࡏࡣࡰࡩࠥࡧ࡮ࡥࠢࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠏࠦࠠࠡࠢࠥࠦࠧᆷ")
    credentials = {
        bstack11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᆸ"): None,
        bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᆹ"): None
    }
    credentials[bstack11lll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᆺ")] = (
        os.environ.get(bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᆻ")) or
        os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࠨᆼ"))
    )
    credentials[bstack11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᆽ")] = (
        os.environ.get(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᆾ")) or
        os.environ.get(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡑࡅ࡚ࠩᆿ"))
    )
    if not credentials[bstack11lll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᇀ")] or not credentials[bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᇁ")]:
        if config and isinstance(config, dict):
            credentials[bstack11lll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᇂ")] = config.get(bstack11lll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᇃ")) or config.get(bstack11lll1_opy_ (u"ࠬࡻࡳࡦࡴࠪᇄ"))
            credentials[bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᇅ")] = config.get(bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᇆ")) or config.get(bstack11lll1_opy_ (u"ࠨ࡭ࡨࡽࠬᇇ"))
    return credentials
def bstack11ll1l1l1_opy_(config):
    bstack11lll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡈࡼࡪࡩࡵࡵࡧࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡥࡽࠥࡪࡥ࡭ࡧࡪࡥࡹ࡯࡮ࡨࠢࡷࡳࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰ࠽ࠎࠥࠦࠠࠡ࠳࠱ࠤࡊࡾࡴࡳࡣࡦࡸࡸࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠱ࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠊࠡࠢࠣࠤ࠷࠴ࠠࡅࡱࡺࡲࡱࡵࡡࡥࡵ࠲ࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯ࡦࠡࡰࡨࡩࡩ࡫ࡤࠋࠢࠣࠤࠥ࠹࠮ࠡࡕࡳࡥࡼࡴࡳࠡࡶ࡫ࡩࠥࡨࡩ࡯ࡣࡵࡽࠥࡧࡳࠡࡣࠣࡷࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡸ࡫ࡷ࡬ࠥ࡯࡮ࡩࡧࡵ࡭ࡹ࡫ࡤࠡࡵࡷࡨ࡮ࡵࠊࠡࠢࠣࠤ࠹࠴ࠠࡇࡱࡵࡻࡦࡸࡤࡴࠢࡶ࡭࡬ࡴࡡ࡭ࡵࠣࠬࡘࡏࡇࡊࡐࡗ࠰࡙ࠥࡉࡈࡖࡈࡖࡒ࠲ࠠࡦࡶࡦ࠲࠮ࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸࠐࠠࠡࠢࠣ࠹࠳ࠦࡅࡹ࡫ࡷࡷࠥࡽࡩࡵࡪࠣࡸ࡭࡫ࠠࡴࡣࡰࡩࠥࡩ࡯ࡥࡧࠣࡥࡸࠦࡴࡩࡧࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡖ࡫ࡩ࡙ࠥࡄࡌࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠐࠠࠡࠢࠣࠦࠧࠨᇈ")
    try:
        bstack1lll1lll111_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack11lll1_opy_ (u"ࠪࡉࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠽ࠤࢀࢃࠧᇉ").format(bstack1lll1lll111_opy_))
        credentials = bstack1lll1ll1l11_opy_(config)
        if not credentials[bstack11lll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᇊ")] or not credentials[bstack11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᇋ")]:
            logger.error(bstack11lll1_opy_ (u"࠭ࡁࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡼࡳࡺࡸࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠢࡷࡳࠥ࡫ࡩࡵࡪࡨࡶࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠯ࠤࡹ࡮ࡥ࡯ࠢࡷࡶࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡧࡧࡢ࡫ࡱ࠲ࠬᇌ"))
            sys.exit(1)
        try:
            bstack1lll1ll1lll_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack11lll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡃࡍࡋࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠪᇍ").format(e))
            sys.exit(1)
        if not bstack1lll1ll1lll_opy_:
            logger.error(bstack11lll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡄࡎࡌࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠧᇎ"))
            sys.exit(1)
        binary_path = bstack1lll1ll1l1l_opy_(bstack1lll1ll1lll_opy_)
        try:
            if not binary_path:
                logger.debug(bstack11lll1_opy_ (u"ࠩࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡ࡮ࡤࡸࡪࡹࡴࠡࡸࡨࡶࡸ࡯࡯࡯ࠩᇏ"))
                binary_path = bstack1lll1ll11l1_opy_(bstack11lll1_opy_ (u"ࠪࠫᇐ"), bstack1lll1ll1lll_opy_, credentials)
            else:
                logger.debug(bstack11lll1_opy_ (u"ࠫࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠬࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡶࡲࡧࡥࡹ࡫ࡳࠨᇑ"))
                binary_path = bstack1lll1ll11l1_opy_(binary_path, bstack1lll1ll1lll_opy_, credentials)
        except Exception as e:
            logger.error(bstack11lll1_opy_ (u"ࠬࡇࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡻࡲࡹࡷࠦࡵࡴࡧࡵࡒࡦࡳࡥࠡࡣࡱࡨࠥࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠡࡶࡲࠤࡪ࡯ࡴࡩࡧࡵࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠮ࠣࡸ࡭࡫࡮ࠡࡶࡵࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡦ࡭ࡡࡪࡰ࠱ࠫᇒ"))
            logger.debug(bstack11lll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪᇓ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack11lll1_opy_ (u"ࠧࡂࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡽࡴࡻࡲࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠣࡸࡴࠦࡥࡪࡶ࡫ࡩࡷࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠰ࠥࡺࡨࡦࡰࠣࡸࡷࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡡࡨࡣ࡬ࡲ࠳࠭ᇔ"))
            logger.debug(bstack11lll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦ࡯ࡳࠢ࡯ࡳࡨࡧࡴࡦࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾ࠭ᇕ"))
            sys.exit(1)
        logger.debug(bstack11lll1_opy_ (u"ࠩࡖࡴࡦࡽ࡮ࡪࡰࡪ࠾ࠥࢁࡽࠡ࡮ࡲࡥࡩࠦࡻࡾࠩᇖ").format(binary_path, bstack11lll1_opy_ (u"ࠥࠤࠧᇗ").join(bstack1lll1lll111_opy_)))
        bstack1lll1lll1l1_opy_ = [binary_path, bstack11lll1_opy_ (u"ࠫࡱࡵࡡࡥࠩᇘ")] + bstack1lll1lll111_opy_
        bstack1lll1ll11ll_opy_ = subprocess.Popen(
            bstack1lll1lll1l1_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1lll1ll111l_opy_(signum, frame):
            bstack11lll1_opy_ (u"ࠧࠨࠢࡇࡱࡵࡻࡦࡸࡤࠡࡵ࡬࡫ࡳࡧ࡬ࡴࠢࡷࡳࠥࡺࡨࡦࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴࠤࠥࠦᇙ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack11lll1_opy_ (u"࠭ࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡽࢀ࠰ࠥ࡬࡯ࡳࡹࡤࡶࡩ࡯࡮ࡨࠢࡷࡳࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳࠴࠮ࠨᇚ").format(signum))
            if bstack1lll1ll11ll_opy_ and bstack1lll1ll11ll_opy_.poll() is None:
                try:
                    bstack1lll1ll11ll_opy_.send_signal(signum)
                    logger.debug(bstack11lll1_opy_ (u"ࠧࡘࡣ࡬ࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࡺ࡯ࠡࡧࡻ࡭ࡹ࠴࠮࠯ࠩᇛ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1lll1ll111l_opy_)
        exit_code = bstack1lll1ll11ll_opy_.wait()
        logger.debug(bstack11lll1_opy_ (u"ࠨࡽࢀࠤࡪࡾࡩࡵࡧࡧࠤࡼ࡯ࡴࡩࠢࡦࡳࡩ࡫ࠠࡼࡿࠪᇜ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack11lll1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢ࡬ࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࠼ࠣࡿࢂ࠭ᇝ").format(e))
        logger.debug(bstack11lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠧᇞ").format(e))
        sys.exit(1)