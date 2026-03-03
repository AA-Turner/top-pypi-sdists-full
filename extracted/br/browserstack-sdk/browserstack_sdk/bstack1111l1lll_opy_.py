# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
bstack11ll111_opy_ (u"ࠧࠨࠢࠋࡎࡲࡥࡩࠦࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡎࡱࡧࡹࡱ࡫ࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠊࡉࡣࡱࡨࡱ࡫ࡳࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡧࡿࠠࡥࡧ࡯ࡩ࡬ࡧࡴࡪࡰࡪࠤࡹࡵࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠋࠤࠥࠦო")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1lllll1ll1l_opy_,
    get_cli_dir,
    bstack1lllll1llll_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1llllll11ll_opy_(config):
    bstack11ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡷ࡬ࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧ࠱ࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥࡵࡲࠡࡥࡲࡲ࡫࡯ࡧ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡕࡪࡨࠤࡘࡊࡋࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡹࡴࡳ࠼ࠣࡔࡦࡺࡨࠡࡶࡲࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠣࠤࠥპ")
    try:
        if bstack11ll111_opy_ (u"ࠧ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠩჟ") in sys.argv:
            bstack1llllll11l1_opy_ = sys.argv.index(bstack11ll111_opy_ (u"ࠨ࠯࠰ࡧࡴࡴࡦࡪࡩࠪრ"))
            if bstack1llllll11l1_opy_ + 1 < len(sys.argv):
                bstack1lllll1lll1_opy_ = sys.argv[bstack1llllll11l1_opy_ + 1]
                logger.debug(bstack11ll111_opy_ (u"ࠤࡉࡳࡺࡴࡤࠡ࠯࠰ࡧࡴࡴࡦࡪࡩࠣࡪࡱࡧࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡶ࡫࠾ࠥࢁࡽࠣს").format(bstack1lllll1lll1_opy_))
                return bstack1lllll1lll1_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack11ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡬ࡢࡩ࠽ࠤࢀࢃࠢტ").format(e))
        pass
    bstack1lllll1lll1_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨუ"))
    if bstack1lllll1lll1_opy_:
        logger.debug(bstack11ll111_opy_ (u"ࠧࡌ࡯ࡶࡰࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡵࡧࡴࡩࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠽ࠤࢀࢃࠢფ").format(bstack1lllll1lll1_opy_))
        return bstack1lllll1lll1_opy_
    return None
def bstack1lllll1l1ll_opy_(config):
    bstack11ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡹࡥࡷ࡯࡯ࡶࡵࠣࡷࡴࡻࡲࡤࡧࡶ࠲ࠏࠦࠠࠡࠢࡓࡶ࡮ࡵࡲࡪࡶࡼ࠾ࠥࡋ࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸࠦ࠾ࠡࡅࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡦࡪࡩ࠽ࠤ࡙࡮ࡥࠡࡕࡇࡏࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡆ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡽࡩࡵࡪࠣࡹࡸ࡫ࡲࡏࡣࡰࡩࠥࡧ࡮ࡥࠢࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠏࠦࠠࠡࠢࠥࠦࠧქ")
    credentials = {
        bstack11ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩღ"): None,
        bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫყ"): None
    }
    credentials[bstack11ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫშ")] = (
        os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫჩ")) or
        os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࠨც"))
    )
    credentials[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨძ")] = (
        os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩწ")) or
        os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡑࡅ࡚ࠩჭ"))
    )
    if not credentials[bstack11ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪხ")] or not credentials[bstack11ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬჯ")]:
        if config and isinstance(config, dict):
            credentials[bstack11ll111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬჰ")] = config.get(bstack11ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ჱ")) or config.get(bstack11ll111_opy_ (u"ࠬࡻࡳࡦࡴࠪჲ"))
            credentials[bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩჳ")] = config.get(bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪჴ")) or config.get(bstack11ll111_opy_ (u"ࠨ࡭ࡨࡽࠬჵ"))
    return credentials
def bstack1ll11111ll_opy_(config):
    bstack11ll111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡈࡼࡪࡩࡵࡵࡧࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡥࡽࠥࡪࡥ࡭ࡧࡪࡥࡹ࡯࡮ࡨࠢࡷࡳࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰ࠽ࠎࠥࠦࠠࠡ࠳࠱ࠤࡊࡾࡴࡳࡣࡦࡸࡸࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠱ࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠊࠡࠢࠣࠤ࠷࠴ࠠࡅࡱࡺࡲࡱࡵࡡࡥࡵ࠲ࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯ࡦࠡࡰࡨࡩࡩ࡫ࡤࠋࠢࠣࠤࠥ࠹࠮ࠡࡕࡳࡥࡼࡴࡳࠡࡶ࡫ࡩࠥࡨࡩ࡯ࡣࡵࡽࠥࡧࡳࠡࡣࠣࡷࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡸ࡫ࡷ࡬ࠥ࡯࡮ࡩࡧࡵ࡭ࡹ࡫ࡤࠡࡵࡷࡨ࡮ࡵࠊࠡࠢࠣࠤ࠹࠴ࠠࡇࡱࡵࡻࡦࡸࡤࡴࠢࡶ࡭࡬ࡴࡡ࡭ࡵࠣࠬࡘࡏࡇࡊࡐࡗ࠰࡙ࠥࡉࡈࡖࡈࡖࡒ࠲ࠠࡦࡶࡦ࠲࠮ࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸࠐࠠࠡࠢࠣ࠹࠳ࠦࡅࡹ࡫ࡷࡷࠥࡽࡩࡵࡪࠣࡸ࡭࡫ࠠࡴࡣࡰࡩࠥࡩ࡯ࡥࡧࠣࡥࡸࠦࡴࡩࡧࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡖ࡫ࡩ࡙ࠥࡄࡌࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠐࠠࠡࠢࠣࠦࠧࠨჶ")
    try:
        bstack1llllll1l1l_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack11ll111_opy_ (u"ࠪࡉࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠽ࠤࢀࢃࠧჷ").format(bstack1llllll1l1l_opy_))
        credentials = bstack1lllll1l1ll_opy_(config)
        if not credentials[bstack11ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ჸ")] or not credentials[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨჹ")]:
            logger.error(bstack11ll111_opy_ (u"࠭ࡁࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡼࡳࡺࡸࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠢࡷࡳࠥ࡫ࡩࡵࡪࡨࡶࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠯ࠤࡹ࡮ࡥ࡯ࠢࡷࡶࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡧࡧࡢ࡫ࡱ࠲ࠬჺ"))
            sys.exit(1)
        try:
            bstack1llllll1l11_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack11ll111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡃࡍࡋࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠪ჻").format(e))
            sys.exit(1)
        if not bstack1llllll1l11_opy_:
            logger.error(bstack11ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡄࡎࡌࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠧჼ"))
            sys.exit(1)
        binary_path = bstack1lllll1llll_opy_(bstack1llllll1l11_opy_)
        try:
            if not binary_path:
                logger.debug(bstack11ll111_opy_ (u"ࠩࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡ࡮ࡤࡸࡪࡹࡴࠡࡸࡨࡶࡸ࡯࡯࡯ࠩჽ"))
                binary_path = bstack1lllll1ll1l_opy_(bstack11ll111_opy_ (u"ࠪࠫჾ"), bstack1llllll1l11_opy_, credentials)
            else:
                logger.debug(bstack11ll111_opy_ (u"ࠫࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠬࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡶࡲࡧࡥࡹ࡫ࡳࠨჿ"))
                binary_path = bstack1lllll1ll1l_opy_(binary_path, bstack1llllll1l11_opy_, credentials)
        except Exception as e:
            logger.error(bstack11ll111_opy_ (u"ࠬࡇࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡻࡲࡹࡷࠦࡵࡴࡧࡵࡒࡦࡳࡥࠡࡣࡱࡨࠥࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠡࡶࡲࠤࡪ࡯ࡴࡩࡧࡵࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠮ࠣࡸ࡭࡫࡮ࠡࡶࡵࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡦ࡭ࡡࡪࡰ࠱ࠫᄀ"))
            logger.debug(bstack11ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪᄁ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack11ll111_opy_ (u"ࠧࡂࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡽࡴࡻࡲࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠣࡸࡴࠦࡥࡪࡶ࡫ࡩࡷࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠰ࠥࡺࡨࡦࡰࠣࡸࡷࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡡࡨࡣ࡬ࡲ࠳࠭ᄂ"))
            logger.debug(bstack11ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦ࡯ࡳࠢ࡯ࡳࡨࡧࡴࡦࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾ࠭ᄃ"))
            sys.exit(1)
        logger.debug(bstack11ll111_opy_ (u"ࠩࡖࡴࡦࡽ࡮ࡪࡰࡪ࠾ࠥࢁࡽࠡ࡮ࡲࡥࡩࠦࡻࡾࠩᄄ").format(binary_path, bstack11ll111_opy_ (u"ࠥࠤࠧᄅ").join(bstack1llllll1l1l_opy_)))
        bstack1llllll111l_opy_ = [binary_path, bstack11ll111_opy_ (u"ࠫࡱࡵࡡࡥࠩᄆ")] + bstack1llllll1l1l_opy_
        bstack1llllll1111_opy_ = subprocess.Popen(
            bstack1llllll111l_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1lllll1ll11_opy_(signum, frame):
            bstack11ll111_opy_ (u"ࠧࠨࠢࡇࡱࡵࡻࡦࡸࡤࠡࡵ࡬࡫ࡳࡧ࡬ࡴࠢࡷࡳࠥࡺࡨࡦࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴࠤࠥࠦᄇ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack11ll111_opy_ (u"࠭ࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡽࢀ࠰ࠥ࡬࡯ࡳࡹࡤࡶࡩ࡯࡮ࡨࠢࡷࡳࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳࠴࠮ࠨᄈ").format(signum))
            if bstack1llllll1111_opy_ and bstack1llllll1111_opy_.poll() is None:
                try:
                    bstack1llllll1111_opy_.send_signal(signum)
                    logger.debug(bstack11ll111_opy_ (u"ࠧࡘࡣ࡬ࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࡺ࡯ࠡࡧࡻ࡭ࡹ࠴࠮࠯ࠩᄉ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1lllll1ll11_opy_)
        exit_code = bstack1llllll1111_opy_.wait()
        logger.debug(bstack11ll111_opy_ (u"ࠨࡽࢀࠤࡪࡾࡩࡵࡧࡧࠤࡼ࡯ࡴࡩࠢࡦࡳࡩ࡫ࠠࡼࡿࠪᄊ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack11ll111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢ࡬ࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࠼ࠣࡿࢂ࠭ᄋ").format(e))
        logger.debug(bstack11ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠧᄌ").format(e))
        sys.exit(1)