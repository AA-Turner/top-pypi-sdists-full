# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
bstack1l111l_opy_ (u"ࠧࠨࠢࠋࡎࡲࡥࡩࠦࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡎࡱࡧࡹࡱ࡫ࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠊࡉࡣࡱࡨࡱ࡫ࡳࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡧࡿࠠࡥࡧ࡯ࡩ࡬ࡧࡴࡪࡰࡪࠤࡹࡵࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠋࠤࠥࠦጆ")
import sys
import os
import subprocess
import signal
from bstack_utils.helper import (
    bstack1ll1l11l1ll_opy_,
    get_cli_dir,
    bstack1ll1l111l1l_opy_
)
from bstack_utils.logger_utils import get_logger
logger = get_logger()
def bstack1ll1l11l1l1_opy_(config):
    bstack1l111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡷ࡬ࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧ࠱ࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥࡵࡲࠡࡥࡲࡲ࡫࡯ࡧ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡕࡪࡨࠤࡘࡊࡋࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡹࡴࡳ࠼ࠣࡔࡦࡺࡨࠡࡶࡲࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠣࠤࠥጇ")
    try:
        if bstack1l111l_opy_ (u"ࠧ࠮࠯ࡦࡳࡳ࡬ࡩࡨࠩገ") in sys.argv:
            bstack1ll1l11ll1l_opy_ = sys.argv.index(bstack1l111l_opy_ (u"ࠨ࠯࠰ࡧࡴࡴࡦࡪࡩࠪጉ"))
            if bstack1ll1l11ll1l_opy_ + 1 < len(sys.argv):
                bstack1lll1l11_opy_ = sys.argv[bstack1ll1l11ll1l_opy_ + 1]
                logger.debug(bstack1l111l_opy_ (u"ࠤࡉࡳࡺࡴࡤࠡ࠯࠰ࡧࡴࡴࡦࡪࡩࠣࡪࡱࡧࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡶ࡫࠾ࠥࢁࡽࠣጊ").format(bstack1lll1l11_opy_))
                return bstack1lll1l11_opy_
    except (ValueError, IndexError) as e:
        logger.debug(bstack1l111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣ࠱࠲ࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡬ࡢࡩ࠽ࠤࢀࢃࠢጋ").format(e))
        pass
    bstack1lll1l11_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨጌ"))
    if bstack1lll1l11_opy_:
        logger.debug(bstack1l111l_opy_ (u"ࠧࡌ࡯ࡶࡰࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡵࡧࡴࡩࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠽ࠤࢀࢃࠢግ").format(bstack1lll1l11_opy_))
        return bstack1lll1l11_opy_
    return None
def bstack1ll1l111lll_opy_(config):
    bstack1l111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡅࡹࡶࡵࡥࡨࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡹࡥࡷ࡯࡯ࡶࡵࠣࡷࡴࡻࡲࡤࡧࡶ࠲ࠏࠦࠠࠡࠢࡓࡶ࡮ࡵࡲࡪࡶࡼ࠾ࠥࡋ࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸࠦ࠾ࠡࡅࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡦࡪࡩ࠽ࠤ࡙࡮ࡥࠡࡕࡇࡏࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡆ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡽࡩࡵࡪࠣࡹࡸ࡫ࡲࡏࡣࡰࡩࠥࡧ࡮ࡥࠢࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠏࠦࠠࠡࠢࠥࠦࠧጎ")
    credentials = {
        bstack1l111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩጏ"): None,
        bstack1l111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫጐ"): None
    }
    credentials[bstack1l111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ጑")] = (
        os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫጒ")) or
        os.environ.get(bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࠨጓ"))
    )
    credentials[bstack1l111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨጔ")] = (
        os.environ.get(bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩጕ")) or
        os.environ.get(bstack1l111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡑࡅ࡚ࠩ጖"))
    )
    if not credentials[bstack1l111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ጗")] or not credentials[bstack1l111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬጘ")]:
        if config and isinstance(config, dict):
            credentials[bstack1l111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬጙ")] = config.get(bstack1l111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ጚ")) or config.get(bstack1l111l_opy_ (u"ࠬࡻࡳࡦࡴࠪጛ"))
            credentials[bstack1l111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩጜ")] = config.get(bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪጝ")) or config.get(bstack1l111l_opy_ (u"ࠨ࡭ࡨࡽࠬጞ"))
    return credentials
def bstack1l11ll11_opy_(config):
    bstack1l111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡈࡼࡪࡩࡵࡵࡧࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡥࡽࠥࡪࡥ࡭ࡧࡪࡥࡹ࡯࡮ࡨࠢࡷࡳࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰ࠽ࠎࠥࠦࠠࠡ࠳࠱ࠤࡊࡾࡴࡳࡣࡦࡸࡸࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠱ࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠊࠡࠢࠣࠤ࠷࠴ࠠࡅࡱࡺࡲࡱࡵࡡࡥࡵ࠲ࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯ࡦࠡࡰࡨࡩࡩ࡫ࡤࠋࠢࠣࠤࠥ࠹࠮ࠡࡕࡳࡥࡼࡴࡳࠡࡶ࡫ࡩࠥࡨࡩ࡯ࡣࡵࡽࠥࡧࡳࠡࡣࠣࡷࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡸ࡫ࡷ࡬ࠥ࡯࡮ࡩࡧࡵ࡭ࡹ࡫ࡤࠡࡵࡷࡨ࡮ࡵࠊࠡࠢࠣࠤ࠹࠴ࠠࡇࡱࡵࡻࡦࡸࡤࡴࠢࡶ࡭࡬ࡴࡡ࡭ࡵࠣࠬࡘࡏࡇࡊࡐࡗ࠰࡙ࠥࡉࡈࡖࡈࡖࡒ࠲ࠠࡦࡶࡦ࠲࠮ࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡩ࡫࡯ࡨࠥࡶࡲࡰࡥࡨࡷࡸࠐࠠࠡࠢࠣ࠹࠳ࠦࡅࡹ࡫ࡷࡷࠥࡽࡩࡵࡪࠣࡸ࡭࡫ࠠࡴࡣࡰࡩࠥࡩ࡯ࡥࡧࠣࡥࡸࠦࡴࡩࡧࠣࡧ࡭࡯࡬ࡥࠢࡳࡶࡴࡩࡥࡴࡵࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡖ࡫ࡩ࡙ࠥࡄࡌࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠐࠠࠡࠢࠣࠦࠧࠨጟ")
    try:
        bstack1ll1l111ll1_opy_ = sys.argv[2:] if len(sys.argv) > 2 else []
        logger.debug(bstack1l111l_opy_ (u"ࠪࡉࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠽ࠤࢀࢃࠧጠ").format(bstack1ll1l111ll1_opy_))
        credentials = bstack1ll1l111lll_opy_(config)
        if not credentials[bstack1l111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ጡ")] or not credentials[bstack1l111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨጢ")]:
            logger.error(bstack1l111l_opy_ (u"࠭ࡁࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡼࡳࡺࡸࠠࡶࡵࡨࡶࡓࡧ࡭ࡦࠢࡤࡲࡩࠦࡡࡤࡥࡨࡷࡸࡑࡥࡺࠢࡷࡳࠥ࡫ࡩࡵࡪࡨࡶࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧࠣࡳࡷࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠯ࠤࡹ࡮ࡥ࡯ࠢࡷࡶࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡧࡧࡢ࡫ࡱ࠲ࠬጣ"))
            sys.exit(1)
        try:
            bstack1ll1l11l11l_opy_ = get_cli_dir()
        except Exception as e:
            logger.error(bstack1l111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡃࡍࡋࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠪጤ").format(e))
            sys.exit(1)
        if not bstack1ll1l11l11l_opy_:
            logger.error(bstack1l111l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡄࡎࡌࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠧጥ"))
            sys.exit(1)
        binary_path = bstack1ll1l111l1l_opy_(bstack1ll1l11l11l_opy_)
        try:
            if not binary_path:
                logger.debug(bstack1l111l_opy_ (u"ࠩࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡ࡮ࡤࡸࡪࡹࡴࠡࡸࡨࡶࡸ࡯࡯࡯ࠩጦ"))
                binary_path = bstack1ll1l11l1ll_opy_(bstack1l111l_opy_ (u"ࠪࠫጧ"), bstack1ll1l11l11l_opy_, credentials)
            else:
                logger.debug(bstack1l111l_opy_ (u"ࠫࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠬࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡶࡲࡧࡥࡹ࡫ࡳࠨጨ"))
                binary_path = bstack1ll1l11l1ll_opy_(binary_path, bstack1ll1l11l11l_opy_, credentials)
        except Exception as e:
            logger.error(bstack1l111l_opy_ (u"ࠬࡇࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡻࡲࡹࡷࠦࡵࡴࡧࡵࡒࡦࡳࡥࠡࡣࡱࡨࠥࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠡࡶࡲࠤࡪ࡯ࡴࡩࡧࡵࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡲࡶࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠮ࠣࡸ࡭࡫࡮ࠡࡶࡵࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡦ࡭ࡡࡪࡰ࠱ࠫጩ"))
            logger.debug(bstack1l111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪጪ").format(e))
            sys.exit(1)
        if not binary_path:
            logger.error(bstack1l111l_opy_ (u"ࠧࡂࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡽࡴࡻࡲࠡࡷࡶࡩࡷࡔࡡ࡮ࡧࠣࡥࡳࡪࠠࡢࡥࡦࡩࡸࡹࡋࡦࡻࠣࡸࡴࠦࡥࡪࡶ࡫ࡩࡷࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡴࡸࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠰ࠥࡺࡨࡦࡰࠣࡸࡷࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡡࡨࡣ࡬ࡲ࠳࠭ጫ"))
            logger.debug(bstack1l111l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦ࡯ࡳࠢ࡯ࡳࡨࡧࡴࡦࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾ࠭ጬ"))
            sys.exit(1)
        logger.debug(bstack1l111l_opy_ (u"ࠩࡖࡴࡦࡽ࡮ࡪࡰࡪ࠾ࠥࢁࡽࠡ࡮ࡲࡥࡩࠦࡻࡾࠩጭ").format(binary_path, bstack1l111l_opy_ (u"ࠥࠤࠧጮ").join(bstack1ll1l111ll1_opy_)))
        bstack1ll1l11ll11_opy_ = [binary_path, bstack1l111l_opy_ (u"ࠫࡱࡵࡡࡥࠩጯ")] + bstack1ll1l111ll1_opy_
        bstack1ll1l11lll1_opy_ = subprocess.Popen(
            bstack1ll1l11ll11_opy_,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        is_exiting = [False]
        def bstack1ll1l11l111_opy_(signum, frame):
            bstack1l111l_opy_ (u"ࠧࠨࠢࡇࡱࡵࡻࡦࡸࡤࠡࡵ࡬࡫ࡳࡧ࡬ࡴࠢࡷࡳࠥࡺࡨࡦࠢࡦ࡬࡮ࡲࡤࠡࡲࡵࡳࡨ࡫ࡳࡴࠤࠥࠦጰ")
            if is_exiting[0]:
                return
            is_exiting[0] = True
            logger.debug(bstack1l111l_opy_ (u"࠭ࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡽࢀ࠰ࠥ࡬࡯ࡳࡹࡤࡶࡩ࡯࡮ࡨࠢࡷࡳࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳࠴࠮ࠨጱ").format(signum))
            if bstack1ll1l11lll1_opy_ and bstack1ll1l11lll1_opy_.poll() is None:
                try:
                    bstack1ll1l11lll1_opy_.send_signal(signum)
                    logger.debug(bstack1l111l_opy_ (u"ࠧࡘࡣ࡬ࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡩࡨࡪ࡮ࡧࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࡺ࡯ࠡࡧࡻ࡭ࡹ࠴࠮࠯ࠩጲ"))
                except ProcessLookupError:
                    pass
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, bstack1ll1l11l111_opy_)
        exit_code = bstack1ll1l11lll1_opy_.wait()
        logger.debug(bstack1l111l_opy_ (u"ࠨࡽࢀࠤࡪࡾࡩࡵࡧࡧࠤࡼ࡯ࡴࡩࠢࡦࡳࡩ࡫ࠠࡼࡿࠪጳ").format(binary_path, exit_code))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(bstack1l111l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢ࡬ࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࠼ࠣࡿࢂ࠭ጴ").format(e))
        logger.debug(bstack1l111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠧጵ").format(e))
        sys.exit(1)