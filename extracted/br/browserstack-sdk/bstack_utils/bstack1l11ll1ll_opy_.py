# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࡋࡩࡱࡶࡥࡳࠢࡩࡳࡷࠦࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡭ࡳࠡࡹ࡫ࡩࡳࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥ࠰ࠍࡗࡹࡸࡩࡤࡶ࡯ࡽࠥࡪࡥࡧࡧࡱࡷ࡮ࡼࡥ࠻ࠢࡱࡩࡻ࡫ࡲࠡࡱࡹࡩࡷࡽࡲࡪࡶࡨࡷࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡢࡴࡪࡷ࠳ࠐࡔࡩ࡫ࡶࠤ࡮ࡹࠠࡵࡪࡨࠤࡕࡿࡴࡩࡱࡱࠤࡪࡷࡵࡪࡸࡤࡰࡪࡴࡴࠡࡱࡩࠤࡏࡧࡶࡢࠩࡶࠤࡔࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࡊࡨࡰࡵ࡫ࡲ࠯ࠌࠥࠦࠧᶣ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack11111lllll1_opy_ = [
    bstack1ll1l11_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᶤ"),
    bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡦࡪࡴࡶࡸ࠲ࡸࡵ࡯ࠩᶥ"),
    bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࡳࡵ࠭ࡥࡧࡩࡥࡺࡲࡴ࠮ࡤࡵࡳࡼࡹࡥࡳ࠯ࡦ࡬ࡪࡩ࡫ࠨᶦ"),
    bstack1ll1l11_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᶧ"),
    bstack1ll1l11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡥࡧࡩࡥࡺࡲࡴ࠮ࡣࡳࡴࡸ࠭ᶨ"),
    bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡩࡳࡹࠬᶩ"),
    bstack1ll1l11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡧࡩࡻ࠳ࡳࡩ࡯࠰ࡹࡸࡧࡧࡦࠩᶪ"),
    bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡷࡴ࡬ࡴࡸࡣࡵࡩ࠲ࡸࡡࡴࡶࡨࡶ࡮ࢀࡥࡳࠩᶫ"),
    bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡳࡢࡰࡧࡦࡴࡾࠧᶬ"),
    bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࠯ࡷ࡭ࡲ࡫ࡲ࠮ࡶ࡫ࡶࡴࡺࡴ࡭࡫ࡱ࡫ࠬᶭ"),
    bstack1ll1l11_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦ࡬ࡲ࡬࠳࡯ࡤࡥ࡯ࡹࡩ࡫ࡤ࠮ࡹ࡬ࡲࡩࡵࡷࡴࠩᶮ"),
    bstack1ll1l11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡳࡧࡱࡨࡪࡸࡥࡳ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࡯࡮ࡨࠩᶯ"),
    bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡨࡨࡥࡹࡻࡲࡦࡵࡀࡘࡷࡧ࡮ࡴ࡮ࡤࡸࡪ࡛ࡉࠨᶰ"),
    bstack1ll1l11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯࡬ࡴࡨ࠳ࡦ࡭ࡱࡲࡨ࡮ࡴࡧ࠮ࡲࡵࡳࡹ࡫ࡣࡵ࡫ࡲࡲࠬᶱ"),
    bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡻࡪࡨ࠭ࡴࡧࡦࡹࡷ࡯ࡴࡺࠩᶲ"),
    bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡫࡫ࡡࡵࡷࡵࡩࡸࡃࡖࡪࡼࡇ࡭ࡸࡶ࡬ࡢࡻࡆࡳࡲࡶ࡯ࡴ࡫ࡷࡳࡷ࠭ᶳ"),
    bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡲ࡯ࡨࡩ࡬ࡲ࡬࠭ᶴ"),
    bstack1ll1l11_opy_ (u"ࠪ࠱࠲ࡹࡩ࡭ࡧࡱࡸࠬᶵ")
]
def bstack11l11l1ll1_opy_(options, bstack11l1lll1l1_opy_=bstack1ll1l11_opy_ (u"ࠦࠧᶶ")):
    bstack1ll1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡏ࡮࡫ࡧࡦࡸࠥࡪࡥࡧࡣࡸࡰࡹࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࡩࡳࡷࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠐࠠࠡࠢࠣࡅࡩࡪࡳࠡ࠳࠻ࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡴࠢࡧࡩ࡫࡫࡮ࡴ࡫ࡹࡩࡱࡿࠠࠩࡱࡱࡰࡾࠦࡩࡧࠢࡱࡳࡹࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡨࡷࡪࡴࡴࠪ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠢࡲࡦ࡯࡫ࡣࡵࠢࡲࡶࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡷࡪࡶ࡫ࠤࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠫ࠭ࠥࡳࡥࡵࡪࡲࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡷࡩࡽࡺ࡟࡯ࡣࡰࡩ࠿ࠦࡃࡰࡰࡷࡩࡽࡺࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤ࡫ࡵࡲࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢࠫࡩ࠳࡭࠮࠭ࠢࠥࡴࡾࡺࡥࡴࡶࠥ࠰ࠥࠨࡰࡺࡶ࡫ࡳࡳࠨࠩࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡐࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡢࡦࡧࡩࡩࠐࠠࠡࠢࠣࠦࠧࠨᶷ")
    if not bstack11l1lll1l1_opy_:
        bstack11l1lll1l1_opy_ = bstack1ll1l11_opy_ (u"ࠨ࡬ࡰࡣࡧ࠱ࡹ࡫ࡳࡵ࡫ࡱ࡫ࠧᶸ")
    if options is None or not hasattr(options, bstack1ll1l11_opy_ (u"ࠧࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭ᶹ")):
        logger.debug(bstack1ll1l11_opy_ (u"ࠣ࡝ࡾࢁࡢࠦࡏࡱࡶ࡬ࡳࡳࡹࠠࡪࡵࠣࡒࡴࡴࡥࠡࡱࡵࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡤࡥࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠬ࠮࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢ࡬ࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠧᶺ").format(bstack11l1lll1l1_opy_))
        return 0
    bstack1111lll1l1l_opy_ = getattr(options, bstack1ll1l11_opy_ (u"ࠩࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶻ"), [])
    if not isinstance(bstack1111lll1l1l_opy_, list):
        bstack1111lll1l1l_opy_ = []
    bstack11111llllll_opy_ = set()
    for arg in bstack1111lll1l1l_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1ll1l11_opy_ (u"ࠪࡁࠬᶼ"))[0] if bstack1ll1l11_opy_ (u"ࠫࡂ࠭ᶽ") in arg else arg
            bstack11111llllll_opy_.add(flag)
    bstack111l11ll11_opy_ = 0
    for arg in bstack11111lllll1_opy_:
        flag = arg.split(bstack1ll1l11_opy_ (u"ࠬࡃࠧᶾ"))[0] if bstack1ll1l11_opy_ (u"࠭࠽ࠨᶿ") in arg else arg
        if flag not in bstack11111llllll_opy_:
            options.add_argument(arg)
            bstack111l11ll11_opy_ += 1
    if bstack111l11ll11_opy_ > 0:
        logger.debug(bstack1ll1l11_opy_ (u"ࠢ࡜ࡽࢀࡡࠥࡏ࡮࡫ࡧࡦࡸࡪࡪࠠࡼࡿࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡳࠡࡨࡲࡶࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦ᷀").format(bstack11l1lll1l1_opy_, bstack111l11ll11_opy_))
    return bstack111l11ll11_opy_