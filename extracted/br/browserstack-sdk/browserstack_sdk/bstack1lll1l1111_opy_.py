# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
bstack111ll_opy_ (u"ࠧࠨࠢࠋࡎࡲࡥࡩࠦࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡎࡱࡧࡹࡱ࡫ࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠊࡉࡣࡱࡨࡱ࡫ࡳࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡧࡿࠠࡥࡧ࡯ࡩ࡬ࡧࡴࡪࡰࡪࠤࡹࡵࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠋࠤࠥࠦጔ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1ll1l11111l_opy_,
    get_cli_dir,
    bstack1ll1l1111l1_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1ll1l11l1l1_opy_(config):
    bstack111ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡷ࡬ࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧ࠱ࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥࡵࡲࠡࡥࡲࡲ࡫࡯ࡧ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡕࡪࡨࠤࡘࡊࡋࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡹࡴࡳ࠼ࠣࡔࡦࡺࡨࠡࡶࡲࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠣࠤࠥጕ")
    try:
        if bstack111ll_opy_ (u"ࠧ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠩ጖") in sys.argv:
            bstack1ll1l111ll1_opy_ = sys.argv.index(bstack111ll_opy_ (u"ࠨ࠯࠰ࡧࡴࡴࡦࡪࡩࠪ጗"))
            if bstack1ll1l111ll1_opy_ + 1 < len(sys.argv):
                bstack1l1l1l1lll_opy_ = sys.argv[bstack1ll1l111ll1_opy_ + 1]
                logger.debug(bstack111ll_opy_ (u"ࠤࡉࡳࡺࡴࡤࠡ࠯࠰ࡧࡴࡴࡦࡪࡩࠣࡪࡱࡧࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡶ࡫࠾ࠥࢁࡽࠣጘ").format(bstack1l1l1l1lll_opy_))
                return bstack1l1l1l1lll_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack111ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡬ࡢࡩ࠽ࠤࢀࢃࠢጙ").format(e))
        pass
    bstack1l1l1l1lll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨጚ"))
    if bstack1l1l1l1lll_opy_:
        logger.debug(bstack111ll_opy_ (u"ࠧࡌ࡯ࡶࡰࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡵࡧࡴࡩࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠽ࠤࢀࢃࠢጛ").format(bstack1l1l1l1lll_opy_))
        return bstack1l1l1l1lll_opy_
    return None
def bstack1ll1l11l11l_opy_(config):
    bstack111ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡹࡥࡷ࡯࡯ࡶࡵࠣࡷࡴࡻࡲࡤࡧࡶ࠲ࠏࠦࠠࠡࠢࡓࡶ࡮ࡵࡲࡪࡶࡼ࠾ࠥࡋ࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸࠦ࠾ࠡࡅࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡦࡪࡩ࠽ࠤ࡙࡮ࡥࠡࡕࡇࡏࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡆ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡽࡩࡵࡪࠣࡹࡸ࡫ࡲࡏࡣࡰࡩࠥࡧ࡮ࡥࠢࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠏࠦࠠࠡࠢࠥࠦࠧጜ")
    credentials = {
        bstack111ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩጝ"): None,
        bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫጞ"): None
    }
    credentials[bstack111ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫጟ")] = (
        os.environ.get(bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫጠ")) or
        os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࠨጡ"))
    )
    credentials[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨጢ")] = (
        os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩጣ")) or
        os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡑࡅ࡚ࠩጤ"))
    )
    if not credentials[bstack111ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪጥ")] or not credentials[bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬጦ")]:
        if config and isinstance(config, dict):
            credentials[bstack111ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬጧ")] = config.get(bstack111ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ጨ")) or config.get(bstack111ll_opy_ (u"ࠬࡻࡳࡦࡴࠪጩ"))
            credentials[bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩጪ")] = config.get(bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪጫ")) or config.get(bstack111ll_opy_ (u"ࠨ࡭ࡨࡽࠬጬ"))
    return credentials
def bstack111l1lll11_opy_(config):
    bstack111ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡈࡼࡪࡩࡵࡵࡧࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡥࡽࠥࡪࡥ࡭ࡧࡪࡥࡹ࡯࡮ࡨࠢࡷࡳࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰ࠽ࠎࠥࠦࠠࠡ࠳࠱ࠤࡊࡾࡴࡳࡣࡦࡸࡸࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠱ࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠊࠡࠢࠣࠤ࠷࠴ࠠࡅࡱࡺࡲࡱࡵࡡࡥࡵ࠲ࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯ࡦࠡࡰࡨࡩࡩ࡫ࡤࠋࠢࠣࠤࠥ࠹࠮ࠡࡕࡳࡥࡼࡴࡳࠡࡶ࡫ࡩࠥࡨࡩ࡯ࡣࡵࡽࠥࡧࡳࠡࡣࠣࡷࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡸ࡫ࡷ࡬ࠥ࡯࡮ࡩࡧࡵ࡭ࡹ࡫ࡤࠡࡵࡷࡨ࡮ࡵࠊࠡࠢࠣࠤ࠹࠴ࠠࡇࡱࡵࡻࡦࡸࡤࡴࠢࡶ࡭࡬ࡴࡡ࡭ࡵࠣࠬࡘࡏࡇࡊࡐࡗ࠰࡙ࠥࡉࡈࡖࡈࡖࡒ࠲ࠠࡦࡶࡦ࠲࠮ࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸࠐࠠࠡࠢࠣ࠹࠳ࠦࡅࡹ࡫ࡷࡷࠥࡽࡩࡵࡪࠣࡸ࡭࡫ࠠࡴࡣࡰࡩࠥࡩ࡯ࡥࡧࠣࡥࡸࠦࡴࡩࡧࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡖ࡫ࡩ࡙ࠥࡄࡌࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠐࠠࠡࠢࠣࠦࠧࠨጭ")
    try:
        bstack1ll1l111lll_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack111ll_opy_ (u"ࠪࡉࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠽ࠤࢀࢃࠧጮ").format(bstack1ll1l111lll_opy_))
        credentials = bstack1ll1l11l11l_opy_(config)
        if not credentials[bstack111ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ጯ")] or not credentials[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨጰ")]:
            logger.error(bstack111ll_opy_ (u"࠭ࡁࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡼࡳࡺࡸࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠢࡷࡳࠥ࡫ࡩࡵࡪࡨࡶࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠯ࠤࡹ࡮ࡥ࡯ࠢࡷࡶࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡧࡧࡢ࡫ࡱ࠲ࠬጱ"))
            sys.exit(1)
        try:
            bstack1ll1l111l1l_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡃࡍࡋࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠪጲ").format(e))
            sys.exit(1)
        if not bstack1ll1l111l1l_opy_:
            logger.error(bstack111ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡄࡎࡌࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠧጳ"))
            sys.exit(1)
        binary_path = bstack1ll1l1111l1_opy_(bstack1ll1l111l1l_opy_)
        try:
            if not binary_path:
                logger.debug(bstack111ll_opy_ (u"ࠩࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡ࡮ࡤࡸࡪࡹࡴࠡࡸࡨࡶࡸ࡯࡯࡯ࠩጴ"))
                binary_path = bstack1ll1l11111l_opy_(bstack111ll_opy_ (u"ࠪࠫጵ"), bstack1ll1l111l1l_opy_, credentials)
            else:
                logger.debug(bstack111ll_opy_ (u"ࠫࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠬࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡶࡲࡧࡥࡹ࡫ࡳࠨጶ"))
                binary_path = bstack1ll1l11111l_opy_(binary_path, bstack1ll1l111l1l_opy_, credentials)
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠬࡇࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡻࡲࡹࡷࠦࡵࡴࡧࡵࡒࡦࡳࡥࠡࡣࡱࡨࠥࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠡࡶࡲࠤࡪ࡯ࡴࡩࡧࡵࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠮ࠣࡸ࡭࡫࡮ࠡࡶࡵࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡦ࡭ࡡࡪࡰ࠱ࠫጷ"))
            logger.debug(bstack111ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪጸ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack111ll_opy_ (u"ࠧࡂࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡽࡴࡻࡲࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠣࡸࡴࠦࡥࡪࡶ࡫ࡩࡷࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠰ࠥࡺࡨࡦࡰࠣࡸࡷࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡡࡨࡣ࡬ࡲ࠳࠭ጹ"))
            logger.debug(bstack111ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦ࡯ࡳࠢ࡯ࡳࡨࡧࡴࡦࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾ࠭ጺ"))
            sys.exit(1)
        logger.debug(bstack111ll_opy_ (u"ࠩࡖࡴࡦࡽ࡮ࡪࡰࡪ࠾ࠥࢁࡽࠡ࡮ࡲࡥࡩࠦࡻࡾࠩጻ").format(binary_path, bstack111ll_opy_ (u"ࠥࠤࠧጼ").join(bstack1ll1l111lll_opy_)))
        bstack1ll1l1111ll_opy_ = [binary_path, bstack111ll_opy_ (u"ࠫࡱࡵࡡࡥࠩጽ")] + bstack1ll1l111lll_opy_
        bstack1ll1l11l111_opy_ = subprocess.Popen(
            bstack1ll1l1111ll_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1ll1l111l11_opy_(signum, frame):
            bstack111ll_opy_ (u"ࠧࠨࠢࡇࡱࡵࡻࡦࡸࡤࠡࡵ࡬࡫ࡳࡧ࡬ࡴࠢࡷࡳࠥࡺࡨࡦࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴࠤࠥࠦጾ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack111ll_opy_ (u"࠭ࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡽࢀ࠰ࠥ࡬࡯ࡳࡹࡤࡶࡩ࡯࡮ࡨࠢࡷࡳࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳࠴࠮ࠨጿ").format(signum))
            if bstack1ll1l11l111_opy_ and bstack1ll1l11l111_opy_.poll() is None:
                try:
                    bstack1ll1l11l111_opy_.send_signal(signum)
                    logger.debug(bstack111ll_opy_ (u"ࠧࡘࡣ࡬ࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࡺ࡯ࠡࡧࡻ࡭ࡹ࠴࠮࠯ࠩፀ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1ll1l111l11_opy_)
        exit_code = bstack1ll1l11l111_opy_.wait()
        logger.debug(bstack111ll_opy_ (u"ࠨࡽࢀࠤࡪࡾࡩࡵࡧࡧࠤࡼ࡯ࡴࡩࠢࡦࡳࡩ࡫ࠠࡼࡿࠪፁ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack111ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢ࡬ࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࠼ࠣࡿࢂ࠭ፂ").format(e))
        logger.debug(bstack111ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠧፃ").format(e))
        sys.exit(1)