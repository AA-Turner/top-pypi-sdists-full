# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࡑࡵࡡࡥࠢࡗࡩࡸࡺࡩ࡯ࡩࠣࡑࡴࡪࡵ࡭ࡧࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠍࡌࡦࡴࡤ࡭ࡧࡶࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡣࡻࠣࡨࡪࡲࡥࡨࡣࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻ࠱ࠎࠧࠨࠢᇇ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1lll1l11l11_opy_,
    get_cli_dir,
    bstack1lll1l11lll_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1lll1l1ll11_opy_(config):
    bstack1ll1lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡈࡼࡹࡸࡡࡤࡶࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡺࡨࠡࡨࡵࡳࡲࠦࡣࡰ࡯ࡰࡥࡳࡪ࠭࡭࡫ࡱࡩࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡࡱࡵࠤࡨࡵ࡮ࡧ࡫ࡪ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡘ࡭࡫ࠠࡔࡆࡎࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡵࡷࡶ࠿ࠦࡐࡢࡶ࡫ࠤࡹࡵࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠥࡵࡲࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠦࠧࠨᇈ")
    try:
        if bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠬᇉ") in sys.argv:
            bstack1lll1l11l1l_opy_ = sys.argv.index(bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࡣࡰࡰࡩ࡭࡬࠭ᇊ"))
            if bstack1lll1l11l1l_opy_ + 1 < len(sys.argv):
                bstack1lll1l111l1_opy_ = sys.argv[bstack1lll1l11l1l_opy_ + 1]
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌ࡯ࡶࡰࡧࠤ࠲࠳ࡣࡰࡰࡩ࡭࡬ࠦࡦ࡭ࡣࡪࠤࡼ࡯ࡴࡩࠢࡳࡥࡹ࡮࠺ࠡࡽࢀࠦᇋ").format(bstack1lll1l111l1_opy_))
                return bstack1lll1l111l1_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦ࠭࠮ࡥࡲࡲ࡫࡯ࡧࠡࡨ࡯ࡥ࡬ࡀࠠࡼࡿࠥᇌ").format(e))
        pass
    bstack1lll1l111l1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫᇍ"))
    if bstack1lll1l111l1_opy_:
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡲࡹࡳࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡱࡣࡷ࡬ࠥ࡯࡮ࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࡀࠠࡼࡿࠥᇎ").format(bstack1lll1l111l1_opy_))
        return bstack1lll1l111l1_opy_
    return None
def bstack1lll1l1l11l_opy_(config):
    bstack1ll1lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡈࡼࡹࡸࡡࡤࡶࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡦࡶࡪࡪࡥ࡯ࡶ࡬ࡥࡱࡹࠠࡧࡴࡲࡱࠥࡼࡡࡳ࡫ࡲࡹࡸࠦࡳࡰࡷࡵࡧࡪࡹ࠮ࠋࠢࠣࠤࠥࡖࡲࡪࡱࡵ࡭ࡹࡿ࠺ࠡࡇࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴࠢࡁࠤࡈࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡕࡪࡨࠤࡘࡊࡋࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡉ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡹ࡬ࡸ࡭ࠦࡵࡴࡧࡵࡒࡦࡳࡥࠡࡣࡱࡨࠥࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠋࠢࠣࠤࠥࠨࠢࠣᇏ")
    credentials = {
        bstack1ll1lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᇐ"): None,
        bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᇑ"): None
    }
    credentials[bstack1ll1lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᇒ")] = (
        os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᇓ")) or
        os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࠫᇔ"))
    )
    credentials[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᇕ")] = (
        os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬᇖ")) or
        os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡍࡈ࡝ࠬᇗ"))
    )
    if not credentials[bstack1ll1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᇘ")] or not credentials[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᇙ")]:
        if config and isinstance(config, dict):
            credentials[bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᇚ")] = config.get(bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᇛ")) or config.get(bstack1ll1lll_opy_ (u"ࠨࡷࡶࡩࡷ࠭ᇜ"))
            credentials[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᇝ")] = config.get(bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᇞ")) or config.get(bstack1ll1lll_opy_ (u"ࠫࡰ࡫ࡹࠨᇟ"))
    return credentials
def bstack1l1l11l111_opy_(config):
    bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡋࡸࡦࡥࡸࡸࡪࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥࡨࡹࠡࡦࡨࡰࡪ࡭ࡡࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡀࠊࠡࠢࠣࠤ࠶࠴ࠠࡆࡺࡷࡶࡦࡩࡴࡴࠢࡦࡶࡪࡪࡥ࡯ࡶ࡬ࡥࡱࡹࠠࡧࡴࡲࡱࠥࡩ࡯࡯ࡨ࡬࡫࠴࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠍࠤࠥࠦࠠ࠳࠰ࠣࡈࡴࡽ࡮࡭ࡱࡤࡨࡸ࠵ࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡩࠤࡳ࡫ࡥࡥࡧࡧࠎࠥࠦࠠࠡ࠵࠱ࠤࡘࡶࡡࡸࡰࡶࠤࡹ࡮ࡥࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡶࠤࡦࠦࡳࡶࡤࡳࡶࡴࡩࡥࡴࡵࠣࡻ࡮ࡺࡨࠡ࡫ࡱ࡬ࡪࡸࡩࡵࡧࡧࠤࡸࡺࡤࡪࡱࠍࠤࠥࠦࠠ࠵࠰ࠣࡊࡴࡸࡷࡢࡴࡧࡷࠥࡹࡩࡨࡰࡤࡰࡸࠦࠨࡔࡋࡊࡍࡓ࡚ࠬࠡࡕࡌࡋ࡙ࡋࡒࡎ࠮ࠣࡩࡹࡩ࠮ࠪࠢࡷࡳࠥࡺࡨࡦࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴࠌࠣࠤࠥࠦ࠵࠯ࠢࡈࡼ࡮ࡺࡳࠡࡹ࡬ࡸ࡭ࠦࡴࡩࡧࠣࡷࡦࡳࡥࠡࡥࡲࡨࡪࠦࡡࡴࠢࡷ࡬ࡪࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡦࡪࡩ࠽ࠤ࡙࡮ࡥࠡࡕࡇࡏࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠌࠣࠤࠥࠦࠢࠣࠤᇠ")
    try:
        bstack1lll1l1l1ll_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack1ll1lll_opy_ (u"࠭ࡅࡹࡧࡦࡹࡹ࡯࡮ࡨࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸࠥࡽࡩࡵࡪࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࡀࠠࡼࡿࠪᇡ").format(bstack1lll1l1l1ll_opy_))
        credentials = bstack1lll1l1l11l_opy_(config)
        if not credentials[bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᇢ")] or not credentials[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᇣ")]:
            logger.error(bstack1ll1lll_opy_ (u"ࠩࡄࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡣࡧࡨࠥࡿ࡯ࡶࡴࠣࡹࡸ࡫ࡲࡏࡣࡰࡩࠥࡧ࡮ࡥࠢࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠥࡺ࡯ࠡࡧ࡬ࡸ࡭࡫ࡲࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡨ࡬ࡰࡪࠦ࡯ࡳࠢࡤࡷࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸ࠲ࠠࡵࡪࡨࡲࠥࡺࡲࡺࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡣࡪࡥ࡮ࡴ࠮ࠨᇤ"))
            sys.exit(1)
        try:
            bstack1lll1l1l1l1_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡆࡐࡎࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂ࠭ᇥ").format(e))
            sys.exit(1)
        if not bstack1lll1l1l1l1_opy_:
            logger.error(bstack1ll1lll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡇࡑࡏࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠪᇦ"))
            sys.exit(1)
        binary_path = bstack1lll1l11lll_opy_(bstack1lll1l1l1l1_opy_)
        try:
            if not binary_path:
                logger.debug(bstack1ll1lll_opy_ (u"ࠬࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡱࡧࡴࡦࡵࡷࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠬᇧ"))
                binary_path = bstack1lll1l11l11_opy_(bstack1ll1lll_opy_ (u"࠭ࠧᇨ"), bstack1lll1l1l1l1_opy_, credentials)
            else:
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡹࡵࡪࡡࡵࡧࡶࠫᇩ"))
                binary_path = bstack1lll1l11l11_opy_(binary_path, bstack1lll1l1l1l1_opy_, credentials)
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠨࡃࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡲࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡾࡵࡵࡳࠢࡸࡷࡪࡸࡎࡢ࡯ࡨࠤࡦࡴࡤࠡࡣࡦࡧࡪࡹࡳࡌࡧࡼࠤࡹࡵࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡧ࡫࡯ࡩࠥࡵࡲࠡࡣࡶࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷ࠱ࠦࡴࡩࡧࡱࠤࡹࡸࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡣࡰ࡯ࡰࡥࡳࡪࠠࡢࡩࡤ࡭ࡳ࠴ࠧᇪ"))
            logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡦࡨࡸࡦ࡯࡬ࡴ࠼ࠣࡿࢂ࠭ᇫ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack1ll1lll_opy_ (u"ࠪࡅࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤ࡮ࡴࡣࡰ࡯ࡳࡰࡪࡺࡥ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡤࡨࡩࠦࡹࡰࡷࡵࠤࡺࡹࡥࡳࡐࡤࡱࡪࠦࡡ࡯ࡦࠣࡥࡨࡩࡥࡴࡵࡎࡩࡾࠦࡴࡰࠢࡨ࡭ࡹ࡮ࡥࡳࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫ࠠࡰࡴࠣࡥࡸࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹࠬࠡࡶ࡫ࡩࡳࠦࡴࡳࡻࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡹ࡮ࡥࠡࡥࡲࡱࡲࡧ࡮ࡥࠢࡤ࡫ࡦ࡯࡮࠯ࠩᇬ"))
            logger.debug(bstack1ll1lll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡲࡶࠥࡲ࡯ࡤࡣࡷࡩࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠩᇭ"))
            sys.exit(1)
        logger.debug(bstack1ll1lll_opy_ (u"࡙ࠬࡰࡢࡹࡱ࡭ࡳ࡭࠺ࠡࡽࢀࠤࡱࡵࡡࡥࠢࡾࢁࠬᇮ").format(binary_path, bstack1ll1lll_opy_ (u"ࠨࠠࠣᇯ").join(bstack1lll1l1l1ll_opy_)))
        bstack1lll1l11ll1_opy_ = [binary_path, bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡤࡨࠬᇰ")] + bstack1lll1l1l1ll_opy_
        bstack1lll1l1l111_opy_ = subprocess.Popen(
            bstack1lll1l11ll1_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1lll1l111ll_opy_(signum, frame):
            bstack1ll1lll_opy_ (u"ࠣࠤࠥࡊࡴࡸࡷࡢࡴࡧࠤࡸ࡯ࡧ࡯ࡣ࡯ࡷࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠧࠨࠢᇱ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack1ll1lll_opy_ (u"ࠩࡕࡩࡨ࡫ࡩࡷࡧࡧࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤࢀࢃࠬࠡࡨࡲࡶࡼࡧࡲࡥ࡫ࡱ࡫ࠥࡺ࡯ࠡࡥ࡫࡭ࡱࡪࠠࡱࡴࡲࡧࡪࡹࡳ࠯࠰࠱ࠫᇲ").format(signum))
            if bstack1lll1l1l111_opy_ and bstack1lll1l1l111_opy_.poll() is None:
                try:
                    bstack1lll1l1l111_opy_.send_signal(signum)
                    logger.debug(bstack1ll1lll_opy_ (u"࡛ࠪࡦ࡯ࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡥ࡫࡭ࡱࡪࠠࡱࡴࡲࡧࡪࡹࡳࠡࡶࡲࠤࡪࡾࡩࡵ࠰࠱࠲ࠬᇳ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1lll1l111ll_opy_)
        exit_code = bstack1lll1l1l111_opy_.wait()
        logger.debug(bstack1ll1lll_opy_ (u"ࠫࢀࢃࠠࡦࡺ࡬ࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥࡩ࡯ࡥࡧࠣࡿࢂ࠭ᇴ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥ࡯࡮ࡪࡶ࡬ࡥࡹ࡯࡮ࡨࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࠿ࠦࡻࡾࠩᇵ").format(e))
        logger.debug(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪᇶ").format(e))
        sys.exit(1)