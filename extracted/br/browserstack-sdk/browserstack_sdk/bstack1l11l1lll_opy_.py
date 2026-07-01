# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࡎࡲࡥࡩࠦࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡎࡱࡧࡹࡱ࡫ࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠊࡉࡣࡱࡨࡱ࡫ࡳࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡧࡿࠠࡥࡧ࡯ࡩ࡬ࡧࡴࡪࡰࡪࠤࡹࡵࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠋࠤࠥࠦ௣")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1l11l11ll_opy_,
    get_cli_dir,
    bstack1l11l1111_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1l11l11l1_opy_(config):
    bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡷ࡬ࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧ࠱ࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥࡵࡲࠡࡥࡲࡲ࡫࡯ࡧ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡕࡪࡨࠤࡘࡊࡋࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡹࡴࡳ࠼ࠣࡔࡦࡺࡨࠡࡶࡲࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠣࠤࠥ௤")
    try:
        if bstack1l1llll_opy_ (u"ࠧ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠩ௥") in sys.argv:
            bstack1l11ll1l1_opy_ = sys.argv.index(bstack1l1llll_opy_ (u"ࠨ࠯࠰ࡧࡴࡴࡦࡪࡩࠪ௦"))
            if bstack1l11ll1l1_opy_ + 1 < len(sys.argv):
                bstack1l11l1l1l_opy_ = sys.argv[bstack1l11ll1l1_opy_ + 1]
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡉࡳࡺࡴࡤࠡ࠯࠰ࡧࡴࡴࡦࡪࡩࠣࡪࡱࡧࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡶ࡫࠾ࠥࢁࡽࠣ௧").format(bstack1l11l1l1l_opy_))
                return bstack1l11l1l1l_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡬ࡢࡩ࠽ࠤࢀࢃࠢ௨").format(e))
        pass
    bstack1l11l1l1l_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ௩"))
    if bstack1l11l1l1l_opy_:
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡌ࡯ࡶࡰࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡵࡧࡴࡩࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠽ࠤࢀࢃࠢ௪").format(bstack1l11l1l1l_opy_))
        return bstack1l11l1l1l_opy_
    return None
def bstack1l11l1ll1_opy_(config):
    bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡹࡥࡷ࡯࡯ࡶࡵࠣࡷࡴࡻࡲࡤࡧࡶ࠲ࠏࠦࠠࠡࠢࡓࡶ࡮ࡵࡲࡪࡶࡼ࠾ࠥࡋ࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸࠦ࠾ࠡࡅࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡦࡪࡩ࠽ࠤ࡙࡮ࡥࠡࡕࡇࡏࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡆ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡽࡩࡵࡪࠣࡹࡸ࡫ࡲࡏࡣࡰࡩࠥࡧ࡮ࡥࠢࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠏࠦࠠࠡࠢࠥࠦࠧ௫")
    credentials = {
        bstack1l1llll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ௬"): None,
        bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ௭"): None
    }
    credentials[bstack1l1llll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ௮")] = (
        os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ௯")) or
        os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࠨ௰"))
    )
    credentials[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ௱")] = (
        os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ௲")) or
        os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡑࡅ࡚ࠩ௳"))
    )
    if not credentials[bstack1l1llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ௴")] or not credentials[bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ௵")]:
        if config and isinstance(config, dict):
            credentials[bstack1l1llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ௶")] = config.get(bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭௷")) or config.get(bstack1l1llll_opy_ (u"ࠬࡻࡳࡦࡴࠪ௸"))
            credentials[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ௹")] = config.get(bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ௺")) or config.get(bstack1l1llll_opy_ (u"ࠨ࡭ࡨࡽࠬ௻"))
    return credentials
def bstack1l11l1l11_opy_(config):
    bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡈࡼࡪࡩࡵࡵࡧࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡥࡽࠥࡪࡥ࡭ࡧࡪࡥࡹ࡯࡮ࡨࠢࡷࡳࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰ࠽ࠎࠥࠦࠠࠡ࠳࠱ࠤࡊࡾࡴࡳࡣࡦࡸࡸࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠱ࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠊࠡࠢࠣࠤ࠷࠴ࠠࡅࡱࡺࡲࡱࡵࡡࡥࡵ࠲ࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯ࡦࠡࡰࡨࡩࡩ࡫ࡤࠋࠢࠣࠤࠥ࠹࠮ࠡࡕࡳࡥࡼࡴࡳࠡࡶ࡫ࡩࠥࡨࡩ࡯ࡣࡵࡽࠥࡧࡳࠡࡣࠣࡷࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡸ࡫ࡷ࡬ࠥ࡯࡮ࡩࡧࡵ࡭ࡹ࡫ࡤࠡࡵࡷࡨ࡮ࡵࠊࠡࠢࠣࠤ࠹࠴ࠠࡇࡱࡵࡻࡦࡸࡤࡴࠢࡶ࡭࡬ࡴࡡ࡭ࡵࠣࠬࡘࡏࡇࡊࡐࡗ࠰࡙ࠥࡉࡈࡖࡈࡖࡒ࠲ࠠࡦࡶࡦ࠲࠮ࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸࠐࠠࠡࠢࠣ࠹࠳ࠦࡅࡹ࡫ࡷࡷࠥࡽࡩࡵࡪࠣࡸ࡭࡫ࠠࡴࡣࡰࡩࠥࡩ࡯ࡥࡧࠣࡥࡸࠦࡴࡩࡧࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡖ࡫ࡩ࡙ࠥࡄࡌࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠐࠠࠡࠢࠣࠦࠧࠨ௼")
    try:
        bstack1l11ll111_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack1l1llll_opy_ (u"ࠪࡉࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠽ࠤࢀࢃࠧ௽").format(bstack1l11ll111_opy_))
        credentials = bstack1l11l1ll1_opy_(config)
        if not credentials[bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭௾")] or not credentials[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ௿")]:
            logger.error(bstack1l1llll_opy_ (u"࠭ࡁࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡼࡳࡺࡸࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠢࡷࡳࠥ࡫ࡩࡵࡪࡨࡶࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠯ࠤࡹ࡮ࡥ࡯ࠢࡷࡶࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡧࡧࡢ࡫ࡱ࠲ࠬఀ"))
            sys.exit(1)
        try:
            bstack1l11ll11l_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡃࡍࡋࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠪఁ").format(e))
            sys.exit(1)
        if not bstack1l11ll11l_opy_:
            logger.error(bstack1l1llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡄࡎࡌࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠧం"))
            sys.exit(1)
        binary_path = bstack1l11l1111_opy_(bstack1l11ll11l_opy_)
        try:
            if not binary_path:
                logger.debug(bstack1l1llll_opy_ (u"ࠩࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡ࡮ࡤࡸࡪࡹࡴࠡࡸࡨࡶࡸ࡯࡯࡯ࠩః"))
                binary_path = bstack1l11l11ll_opy_(bstack1l1llll_opy_ (u"ࠪࠫఄ"), bstack1l11ll11l_opy_, credentials)
            else:
                logger.debug(bstack1l1llll_opy_ (u"ࠫࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠬࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡶࡲࡧࡥࡹ࡫ࡳࠨఅ"))
                binary_path = bstack1l11l11ll_opy_(binary_path, bstack1l11ll11l_opy_, credentials)
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠬࡇࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡻࡲࡹࡷࠦࡵࡴࡧࡵࡒࡦࡳࡥࠡࡣࡱࡨࠥࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠡࡶࡲࠤࡪ࡯ࡴࡩࡧࡵࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠮ࠣࡸ࡭࡫࡮ࠡࡶࡵࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡦ࡭ࡡࡪࡰ࠱ࠫఆ"))
            logger.debug(bstack1l1llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪఇ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack1l1llll_opy_ (u"ࠧࡂࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡽࡴࡻࡲࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠣࡸࡴࠦࡥࡪࡶ࡫ࡩࡷࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠰ࠥࡺࡨࡦࡰࠣࡸࡷࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡡࡨࡣ࡬ࡲ࠳࠭ఈ"))
            logger.debug(bstack1l1llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦ࡯ࡳࠢ࡯ࡳࡨࡧࡴࡦࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾ࠭ఉ"))
            sys.exit(1)
        logger.debug(bstack1l1llll_opy_ (u"ࠩࡖࡴࡦࡽ࡮ࡪࡰࡪ࠾ࠥࢁࡽࠡ࡮ࡲࡥࡩࠦࡻࡾࠩఊ").format(binary_path, bstack1l1llll_opy_ (u"ࠥࠤࠧఋ").join(bstack1l11ll111_opy_)))
        bstack1l11ll1ll_opy_ = [binary_path, bstack1l1llll_opy_ (u"ࠫࡱࡵࡡࡥࠩఌ")] + bstack1l11ll111_opy_
        bstack1l11l111l_opy_ = subprocess.Popen(
            bstack1l11ll1ll_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1l11lll11_opy_(signum, frame):
            bstack1l1llll_opy_ (u"ࠧࠨࠢࡇࡱࡵࡻࡦࡸࡤࠡࡵ࡬࡫ࡳࡧ࡬ࡴࠢࡷࡳࠥࡺࡨࡦࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴࠤࠥࠦ఍")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack1l1llll_opy_ (u"࠭ࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡽࢀ࠰ࠥ࡬࡯ࡳࡹࡤࡶࡩ࡯࡮ࡨࠢࡷࡳࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳࠴࠮ࠨఎ").format(signum))
            if bstack1l11l111l_opy_ and bstack1l11l111l_opy_.poll() is None:
                try:
                    bstack1l11l111l_opy_.send_signal(signum)
                    logger.debug(bstack1l1llll_opy_ (u"ࠧࡘࡣ࡬ࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࡺ࡯ࠡࡧࡻ࡭ࡹ࠴࠮࠯ࠩఏ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1l11lll11_opy_)
        exit_code = bstack1l11l111l_opy_.wait()
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡽࢀࠤࡪࡾࡩࡵࡧࡧࠤࡼ࡯ࡴࡩࠢࡦࡳࡩ࡫ࠠࡼࡿࠪఐ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack1l1llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢ࡬ࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࠼ࠣࡿࢂ࠭఑").format(e))
        logger.debug(bstack1l1llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠧఒ").format(e))
        sys.exit(1)