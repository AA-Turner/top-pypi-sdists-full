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
bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࡋࡩࡱࡶࡥࡳࠢࡩࡳࡷࠦࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡭ࡳࠡࡹ࡫ࡩࡳࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥ࠰ࠍࡗࡹࡸࡩࡤࡶ࡯ࡽࠥࡪࡥࡧࡧࡱࡷ࡮ࡼࡥ࠻ࠢࡱࡩࡻ࡫ࡲࠡࡱࡹࡩࡷࡽࡲࡪࡶࡨࡷࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡢࡴࡪࡷ࠳ࠐࡔࡩ࡫ࡶࠤ࡮ࡹࠠࡵࡪࡨࠤࡕࡿࡴࡩࡱࡱࠤࡪࡷࡵࡪࡸࡤࡰࡪࡴࡴࠡࡱࡩࠤࡏࡧࡶࡢࠩࡶࠤࡔࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࡊࡨࡰࡵ࡫ࡲ࠯ࠌࠥࠦࠧ₉")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack111111l1l1l_opy_ = [
    bstack1l1llll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫ₊"),
    bstack1l1llll_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡦࡪࡴࡶࡸ࠲ࡸࡵ࡯ࠩ₋"),
    bstack1l1llll_opy_ (u"ࠩ࠰࠱ࡳࡵ࠭ࡥࡧࡩࡥࡺࡲࡴ࠮ࡤࡵࡳࡼࡹࡥࡳ࠯ࡦ࡬ࡪࡩ࡫ࠨ₌"),
    bstack1l1llll_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ₍"),
    bstack1l1llll_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡥࡧࡩࡥࡺࡲࡴ࠮ࡣࡳࡴࡸ࠭₎"),
    bstack1l1llll_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡩࡳࡹࠬ₏"),
    bstack1l1llll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡧࡩࡻ࠳ࡳࡩ࡯࠰ࡹࡸࡧࡧࡦࠩₐ"),
    bstack1l1llll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡷࡴ࡬ࡴࡸࡣࡵࡩ࠲ࡸࡡࡴࡶࡨࡶ࡮ࢀࡥࡳࠩₑ"),
    bstack1l1llll_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡳࡢࡰࡧࡦࡴࡾࠧₒ"),
    bstack1l1llll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࠯ࡷ࡭ࡲ࡫ࡲ࠮ࡶ࡫ࡶࡴࡺࡴ࡭࡫ࡱ࡫ࠬₓ"),
    bstack1l1llll_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦ࡬ࡲ࡬࠳࡯ࡤࡥ࡯ࡹࡩ࡫ࡤ࠮ࡹ࡬ࡲࡩࡵࡷࡴࠩₔ"),
    bstack1l1llll_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡳࡧࡱࡨࡪࡸࡥࡳ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࡯࡮ࡨࠩₕ"),
    bstack1l1llll_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡨࡨࡥࡹࡻࡲࡦࡵࡀࡘࡷࡧ࡮ࡴ࡮ࡤࡸࡪ࡛ࡉࠨₖ"),
    bstack1l1llll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯࡬ࡴࡨ࠳ࡦ࡭ࡱࡲࡨ࡮ࡴࡧ࠮ࡲࡵࡳࡹ࡫ࡣࡵ࡫ࡲࡲࠬₗ"),
    bstack1l1llll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡻࡪࡨ࠭ࡴࡧࡦࡹࡷ࡯ࡴࡺࠩₘ"),
    bstack1l1llll_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡫࡫ࡡࡵࡷࡵࡩࡸࡃࡖࡪࡼࡇ࡭ࡸࡶ࡬ࡢࡻࡆࡳࡲࡶ࡯ࡴ࡫ࡷࡳࡷ࠭ₙ"),
    bstack1l1llll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡲ࡯ࡨࡩ࡬ࡲ࡬࠭ₚ"),
    bstack1l1llll_opy_ (u"ࠪ࠱࠲ࡹࡩ࡭ࡧࡱࡸࠬₛ")
]
def bstack1l1l1lll11l_opy_(options, bstack1ll1111l1l_opy_=bstack1l1llll_opy_ (u"ࠦࠧₜ")):
    bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡏ࡮࡫ࡧࡦࡸࠥࡪࡥࡧࡣࡸࡰࡹࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࡩࡳࡷࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠐࠠࠡࠢࠣࡅࡩࡪࡳࠡ࠳࠻ࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡴࠢࡧࡩ࡫࡫࡮ࡴ࡫ࡹࡩࡱࡿࠠࠩࡱࡱࡰࡾࠦࡩࡧࠢࡱࡳࡹࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡨࡷࡪࡴࡴࠪ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠢࡲࡦ࡯࡫ࡣࡵࠢࡲࡶࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡷࡪࡶ࡫ࠤࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠫ࠭ࠥࡳࡥࡵࡪࡲࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡷࡩࡽࡺ࡟࡯ࡣࡰࡩ࠿ࠦࡃࡰࡰࡷࡩࡽࡺࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤ࡫ࡵࡲࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢࠫࡩ࠳࡭࠮࠭ࠢࠥࡴࡾࡺࡥࡴࡶࠥ࠰ࠥࠨࡰࡺࡶ࡫ࡳࡳࠨࠩࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡐࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡢࡦࡧࡩࡩࠐࠠࠡࠢࠣࠦࠧࠨ₝")
    if not bstack1ll1111l1l_opy_:
        bstack1ll1111l1l_opy_ = bstack1l1llll_opy_ (u"ࠨ࡬ࡰࡣࡧ࠱ࡹ࡫ࡳࡵ࡫ࡱ࡫ࠧ₞")
    if options is None or not hasattr(options, bstack1l1llll_opy_ (u"ࠧࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭₟")):
        logger.debug(bstack1l1llll_opy_ (u"ࠣ࡝ࡾࢁࡢࠦࡏࡱࡶ࡬ࡳࡳࡹࠠࡪࡵࠣࡒࡴࡴࡥࠡࡱࡵࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡤࡥࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠬ࠮࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢ࡬ࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠧ₠").format(bstack1ll1111l1l_opy_))
        return 0
    bstack11111llllll_opy_ = getattr(options, bstack1l1llll_opy_ (u"ࠩࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭₡"), [])
    if not isinstance(bstack11111llllll_opy_, list):
        bstack11111llllll_opy_ = []
    bstack111111l1ll1_opy_ = set()
    for arg in bstack11111llllll_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1l1llll_opy_ (u"ࠪࡁࠬ₢"))[0] if bstack1l1llll_opy_ (u"ࠫࡂ࠭₣") in arg else arg
            bstack111111l1ll1_opy_.add(flag)
    bstack111111l1l1_opy_ = 0
    for arg in bstack111111l1l1l_opy_:
        flag = arg.split(bstack1l1llll_opy_ (u"ࠬࡃࠧ₤"))[0] if bstack1l1llll_opy_ (u"࠭࠽ࠨ₥") in arg else arg
        if flag not in bstack111111l1ll1_opy_:
            options.add_argument(arg)
            bstack111111l1l1_opy_ += 1
    if bstack111111l1l1_opy_ > 0:
        logger.debug(bstack1l1llll_opy_ (u"ࠢ࡜ࡽࢀࡡࠥࡏ࡮࡫ࡧࡦࡸࡪࡪࠠࡼࡿࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡳࠡࡨࡲࡶࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦ₦").format(bstack1ll1111l1l_opy_, bstack111111l1l1_opy_))
    return bstack111111l1l1_opy_