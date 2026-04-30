# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
bstack1l1111l_opy_ (u"ࠤࠥࠦࠏࡎࡥ࡭ࡲࡨࡶࠥ࡬࡯ࡳࠢ࡬ࡲ࡯࡫ࡣࡵ࡫ࡱ࡫ࠥࡪࡥࡧࡣࡸࡰࡹࠦࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠦࡡࡳࡩࡶࠤࡼ࡮ࡥ࡯ࠢࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨ࠳ࠐࡓࡵࡴ࡬ࡧࡹࡲࡹࠡࡦࡨࡪࡪࡴࡳࡪࡸࡨ࠾ࠥࡴࡥࡷࡧࡵࠤࡴࡼࡥࡳࡹࡵ࡭ࡹ࡫ࡳࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡥࡷ࡭ࡳ࠯ࠌࡗ࡬࡮ࡹࠠࡪࡵࠣࡸ࡭࡫ࠠࡑࡻࡷ࡬ࡴࡴࠠࡦࡳࡸ࡭ࡻࡧ࡬ࡦࡰࡷࠤࡴ࡬ࠠࡋࡣࡹࡥࠬࡹࠠࡐࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬ࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࡍ࡫࡬ࡱࡧࡵ࠲ࠏࠨ᷂ࠢࠣ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack11111ll1l1l_opy_ = [
    bstack1l1111l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ᷃"),
    bstack1l1111l_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡩ࡭ࡷࡹࡴ࠮ࡴࡸࡲࠬ᷄"),
    bstack1l1111l_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡨࡪ࡬ࡡࡶ࡮ࡷ࠱ࡧࡸ࡯ࡸࡵࡨࡶ࠲ࡩࡨࡦࡥ࡮ࠫ᷅"),
    bstack1l1111l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᷆"),
    bstack1l1111l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡨࡪ࡬ࡡࡶ࡮ࡷ࠱ࡦࡶࡰࡴࠩ᷇"),
    bstack1l1111l_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡬ࡶࡵࠨ᷈"),
    bstack1l1111l_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡪࡥࡷ࠯ࡶ࡬ࡲ࠳ࡵࡴࡣࡪࡩࠬ᷉"),
    bstack1l1111l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡳࡰࡨࡷࡻࡦࡸࡥ࠮ࡴࡤࡷࡹ࡫ࡲࡪࡼࡨࡶ᷊ࠬ"),
    bstack1l1111l_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡶࡥࡳࡪࡢࡰࡺࠪ᷋"),
    bstack1l1111l_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࠲ࡺࡩ࡮ࡧࡵ࠱ࡹ࡮ࡲࡰࡶࡷࡰ࡮ࡴࡧࠨ᷌"),
    bstack1l1111l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࡯࡮ࡨ࠯ࡲࡧࡨࡲࡵࡥࡧࡧ࠱ࡼ࡯࡮ࡥࡱࡺࡷࠬ᷍"),
    bstack1l1111l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡶࡪࡴࡤࡦࡴࡨࡶ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࡫ࡱ࡫᷎ࠬ"),
    bstack1l1111l_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡫࡫ࡡࡵࡷࡵࡩࡸࡃࡔࡳࡣࡱࡷࡱࡧࡴࡦࡗࡌ᷏ࠫ"),
    bstack1l1111l_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡯ࡰࡤ࠯ࡩࡰࡴࡵࡤࡪࡰࡪ࠱ࡵࡸ࡯ࡵࡧࡦࡸ࡮ࡵ࡮ࠨ᷐"),
    bstack1l1111l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡷࡦࡤ࠰ࡷࡪࡩࡵࡳ࡫ࡷࡽࠬ᷑"),
    bstack1l1111l_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡧࡧࡤࡸࡺࡸࡥࡴ࠿࡙࡭ࡿࡊࡩࡴࡲ࡯ࡥࡾࡉ࡯࡮ࡲࡲࡷ࡮ࡺ࡯ࡳࠩ᷒"),
    bstack1l1111l_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮࡮ࡲ࡫࡬࡯࡮ࡨࠩᷓ"),
    bstack1l1111l_opy_ (u"࠭࠭࠮ࡵ࡬ࡰࡪࡴࡴࠨᷔ")
]
def bstack11l1l11l1_opy_(options, bstack1llllllll1l_opy_=bstack1l1111l_opy_ (u"ࠢࠣᷕ")):
    bstack1l1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡋࡱ࡮ࡪࡩࡴࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠌࠣࠤࠥࠦࡁࡥࡦࡶࠤ࠶࠾ࠠࡄࡪࡵࡳࡲ࡫ࠠࡢࡴࡪࡷࠥࡪࡥࡧࡧࡱࡷ࡮ࡼࡥ࡭ࡻࠣࠬࡴࡴ࡬ࡺࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷ࡫ࡳࡦࡰࡷ࠭࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠥࡵࡢ࡫ࡧࡦࡸࠥࡵࡲࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡺ࡭ࡹ࡮ࠠࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠮ࠩࠡ࡯ࡨࡸ࡭ࡵࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡺࡥࡹࡶࡢࡲࡦࡳࡥ࠻ࠢࡆࡳࡳࡺࡥࡹࡶࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࡧࡱࡵࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥ࠮ࡥ࠯ࡩ࠱࠰ࠥࠨࡰࡺࡶࡨࡷࡹࠨࠬࠡࠤࡳࡽࡹ࡮࡯࡯ࠤࠬࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡓࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣࡥࡩࡪࡥࡥࠌࠣࠤࠥࠦࠢࠣࠤᷖ")
    if not bstack1llllllll1l_opy_:
        bstack1llllllll1l_opy_ = bstack1l1111l_opy_ (u"ࠤ࡯ࡳࡦࡪ࠭ࡵࡧࡶࡸ࡮ࡴࡧࠣᷗ")
    if options is None or not hasattr(options, bstack1l1111l_opy_ (u"ࠪࡥࡩࡪ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩᷘ")):
        logger.debug(bstack1l1111l_opy_ (u"ࠦࡠࢁࡽ࡞ࠢࡒࡴࡹ࡯࡯࡯ࡵࠣ࡭ࡸࠦࡎࡰࡰࡨࠤࡴࡸࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡣࡧࡨࡤࡧࡲࡨࡷࡰࡩࡳࡺࠨࠪ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥ࡯࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠣᷙ").format(bstack1llllllll1l_opy_))
        return 0
    bstack1111l1lll1l_opy_ = getattr(options, bstack1l1111l_opy_ (u"ࠬࡥࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᷚ"), [])
    if not isinstance(bstack1111l1lll1l_opy_, list):
        bstack1111l1lll1l_opy_ = []
    bstack11111ll1l11_opy_ = set()
    for arg in bstack1111l1lll1l_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1l1111l_opy_ (u"࠭࠽ࠨᷛ"))[0] if bstack1l1111l_opy_ (u"ࠧ࠾ࠩᷜ") in arg else arg
            bstack11111ll1l11_opy_.add(flag)
    bstack1ll1l11111_opy_ = 0
    for arg in bstack11111ll1l1l_opy_:
        flag = arg.split(bstack1l1111l_opy_ (u"ࠨ࠿ࠪᷝ"))[0] if bstack1l1111l_opy_ (u"ࠩࡀࠫᷞ") in arg else arg
        if flag not in bstack11111ll1l11_opy_:
            options.add_argument(arg)
            bstack1ll1l11111_opy_ += 1
    if bstack1ll1l11111_opy_ > 0:
        logger.debug(bstack1l1111l_opy_ (u"ࠥ࡟ࢀࢃ࡝ࠡࡋࡱ࡮ࡪࡩࡴࡦࡦࠣࡿࢂࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡶࠤ࡫ࡵࡲࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠢᷟ").format(bstack1llllllll1l_opy_, bstack1ll1l11111_opy_))
    return bstack1ll1l11111_opy_