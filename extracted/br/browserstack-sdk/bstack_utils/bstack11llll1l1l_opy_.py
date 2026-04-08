# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
bstack111l_opy_ (u"ࠨࠢࠣࠌࡋࡩࡱࡶࡥࡳࠢࡩࡳࡷࠦࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡭ࡳࠡࡹ࡫ࡩࡳࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥ࠰ࠍࡗࡹࡸࡩࡤࡶ࡯ࡽࠥࡪࡥࡧࡧࡱࡷ࡮ࡼࡥ࠻ࠢࡱࡩࡻ࡫ࡲࠡࡱࡹࡩࡷࡽࡲࡪࡶࡨࡷࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡢࡴࡪࡷ࠳ࠐࡔࡩ࡫ࡶࠤ࡮ࡹࠠࡵࡪࡨࠤࡕࡿࡴࡩࡱࡱࠤࡪࡷࡵࡪࡸࡤࡰࡪࡴࡴࠡࡱࡩࠤࡏࡧࡶࡢࠩࡶࠤࡔࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࡊࡨࡰࡵ࡫ࡲ࠯ࠌࠥࠦࠧᶣ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack11111llllll_opy_ = [
    bstack111l_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᶤ"),
    bstack111l_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡦࡪࡴࡶࡸ࠲ࡸࡵ࡯ࠩᶥ"),
    bstack111l_opy_ (u"ࠩ࠰࠱ࡳࡵ࠭ࡥࡧࡩࡥࡺࡲࡴ࠮ࡤࡵࡳࡼࡹࡥࡳ࠯ࡦ࡬ࡪࡩ࡫ࠨᶦ"),
    bstack111l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᶧ"),
    bstack111l_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡥࡧࡩࡥࡺࡲࡴ࠮ࡣࡳࡴࡸ࠭ᶨ"),
    bstack111l_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡩࡳࡹࠬᶩ"),
    bstack111l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡧࡩࡻ࠳ࡳࡩ࡯࠰ࡹࡸࡧࡧࡦࠩᶪ"),
    bstack111l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡷࡴ࡬ࡴࡸࡣࡵࡩ࠲ࡸࡡࡴࡶࡨࡶ࡮ࢀࡥࡳࠩᶫ"),
    bstack111l_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡳࡢࡰࡧࡦࡴࡾࠧᶬ"),
    bstack111l_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࠯ࡷ࡭ࡲ࡫ࡲ࠮ࡶ࡫ࡶࡴࡺࡴ࡭࡫ࡱ࡫ࠬᶭ"),
    bstack111l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦ࡬ࡲ࡬࠳࡯ࡤࡥ࡯ࡹࡩ࡫ࡤ࠮ࡹ࡬ࡲࡩࡵࡷࡴࠩᶮ"),
    bstack111l_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡳࡧࡱࡨࡪࡸࡥࡳ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࡯࡮ࡨࠩᶯ"),
    bstack111l_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡨࡨࡥࡹࡻࡲࡦࡵࡀࡘࡷࡧ࡮ࡴ࡮ࡤࡸࡪ࡛ࡉࠨᶰ"),
    bstack111l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯࡬ࡴࡨ࠳ࡦ࡭ࡱࡲࡨ࡮ࡴࡧ࠮ࡲࡵࡳࡹ࡫ࡣࡵ࡫ࡲࡲࠬᶱ"),
    bstack111l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡻࡪࡨ࠭ࡴࡧࡦࡹࡷ࡯ࡴࡺࠩᶲ"),
    bstack111l_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡫࡫ࡡࡵࡷࡵࡩࡸࡃࡖࡪࡼࡇ࡭ࡸࡶ࡬ࡢࡻࡆࡳࡲࡶ࡯ࡴ࡫ࡷࡳࡷ࠭ᶳ"),
    bstack111l_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡲ࡯ࡨࡩ࡬ࡲ࡬࠭ᶴ"),
    bstack111l_opy_ (u"ࠪ࠱࠲ࡹࡩ࡭ࡧࡱࡸࠬᶵ")
]
def bstack11111lll11_opy_(options, bstack11ll11l111_opy_=bstack111l_opy_ (u"ࠦࠧᶶ")):
    bstack111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡏ࡮࡫ࡧࡦࡸࠥࡪࡥࡧࡣࡸࡰࡹࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࡩࡳࡷࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠐࠠࠡࠢࠣࡅࡩࡪࡳࠡ࠳࠻ࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡴࠢࡧࡩ࡫࡫࡮ࡴ࡫ࡹࡩࡱࡿࠠࠩࡱࡱࡰࡾࠦࡩࡧࠢࡱࡳࡹࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡨࡷࡪࡴࡴࠪ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠢࡲࡦ࡯࡫ࡣࡵࠢࡲࡶࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡷࡪࡶ࡫ࠤࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠫ࠭ࠥࡳࡥࡵࡪࡲࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡷࡩࡽࡺ࡟࡯ࡣࡰࡩ࠿ࠦࡃࡰࡰࡷࡩࡽࡺࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤ࡫ࡵࡲࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢࠫࡩ࠳࡭࠮࠭ࠢࠥࡴࡾࡺࡥࡴࡶࠥ࠰ࠥࠨࡰࡺࡶ࡫ࡳࡳࠨࠩࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡐࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡢࡦࡧࡩࡩࠐࠠࠡࠢࠣࠦࠧࠨᶷ")
    if not bstack11ll11l111_opy_:
        bstack11ll11l111_opy_ = bstack111l_opy_ (u"ࠨ࡬ࡰࡣࡧ࠱ࡹ࡫ࡳࡵ࡫ࡱ࡫ࠧᶸ")
    if options is None or not hasattr(options, bstack111l_opy_ (u"ࠧࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭ᶹ")):
        logger.debug(bstack111l_opy_ (u"ࠣ࡝ࡾࢁࡢࠦࡏࡱࡶ࡬ࡳࡳࡹࠠࡪࡵࠣࡒࡴࡴࡥࠡࡱࡵࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡤࡥࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠬ࠮࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢ࡬ࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠧᶺ").format(bstack11ll11l111_opy_))
        return 0
    bstack1111ll1111l_opy_ = getattr(options, bstack111l_opy_ (u"ࠩࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶻ"), [])
    if not isinstance(bstack1111ll1111l_opy_, list):
        bstack1111ll1111l_opy_ = []
    bstack11111lllll1_opy_ = set()
    for arg in bstack1111ll1111l_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack111l_opy_ (u"ࠪࡁࠬᶼ"))[0] if bstack111l_opy_ (u"ࠫࡂ࠭ᶽ") in arg else arg
            bstack11111lllll1_opy_.add(flag)
    bstack1lllllllll1_opy_ = 0
    for arg in bstack11111llllll_opy_:
        flag = arg.split(bstack111l_opy_ (u"ࠬࡃࠧᶾ"))[0] if bstack111l_opy_ (u"࠭࠽ࠨᶿ") in arg else arg
        if flag not in bstack11111lllll1_opy_:
            options.add_argument(arg)
            bstack1lllllllll1_opy_ += 1
    if bstack1lllllllll1_opy_ > 0:
        logger.debug(bstack111l_opy_ (u"ࠢ࡜ࡽࢀࡡࠥࡏ࡮࡫ࡧࡦࡸࡪࡪࠠࡼࡿࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡳࠡࡨࡲࡶࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦ᷀").format(bstack11ll11l111_opy_, bstack1lllllllll1_opy_))
    return bstack1lllllllll1_opy_