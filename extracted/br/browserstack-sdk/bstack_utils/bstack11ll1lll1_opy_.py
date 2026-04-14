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
bstack1l111l_opy_ (u"ࠢࠣࠤࠍࡌࡪࡲࡰࡦࡴࠣࡪࡴࡸࠠࡪࡰ࡭ࡩࡨࡺࡩ࡯ࡩࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠤࡦࡸࡧࡴࠢࡺ࡬ࡪࡴࠠࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡨࡲࡦࡨ࡬ࡦࡦ࠱ࠎࡘࡺࡲࡪࡥࡷࡰࡾࠦࡤࡦࡨࡨࡲࡸ࡯ࡶࡦ࠼ࠣࡲࡪࡼࡥࡳࠢࡲࡺࡪࡸࡷࡳ࡫ࡷࡩࡸࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡣࡵ࡫ࡸ࠴ࠊࡕࡪ࡬ࡷࠥ࡯ࡳࠡࡶ࡫ࡩࠥࡖࡹࡵࡪࡲࡲࠥ࡫ࡱࡶ࡫ࡹࡥࡱ࡫࡮ࡵࠢࡲࡪࠥࡐࡡࡷࡣࠪࡷࠥࡕࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࡋࡩࡱࡶࡥࡳ࠰ࠍࠦࠧࠨ᷀")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack11111ll1lll_opy_ = [
    bstack1l111l_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬ᷁"),
    bstack1l111l_opy_ (u"ࠩ࠰࠱ࡳࡵ࠭ࡧ࡫ࡵࡷࡹ࠳ࡲࡶࡰ᷂ࠪ"),
    bstack1l111l_opy_ (u"ࠪ࠱࠲ࡴ࡯࠮ࡦࡨࡪࡦࡻ࡬ࡵ࠯ࡥࡶࡴࡽࡳࡦࡴ࠰ࡧ࡭࡫ࡣ࡬ࠩ᷃"),
    bstack1l111l_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ᷄"),
    bstack1l111l_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡦࡨࡪࡦࡻ࡬ࡵ࠯ࡤࡴࡵࡹࠧ᷅"),
    bstack1l111l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡪࡴࡺ࠭᷆"),
    bstack1l111l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡨࡪࡼ࠭ࡴࡪࡰ࠱ࡺࡹࡡࡨࡧࠪ᷇"),
    bstack1l111l_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡸࡵࡦࡵࡹࡤࡶࡪ࠳ࡲࡢࡵࡷࡩࡷ࡯ࡺࡦࡴࠪ᷈"),
    bstack1l111l_opy_ (u"ࠩ࠰࠱ࡳࡵ࠭ࡴࡣࡱࡨࡧࡵࡸࠨ᷉"),
    bstack1l111l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦ࠰ࡸ࡮ࡳࡥࡳ࠯ࡷ࡬ࡷࡵࡴࡵ࡮࡬ࡲ࡬᷊࠭"),
    bstack1l111l_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡣࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧ࡭ࡳ࡭࠭ࡰࡥࡦࡰࡺࡪࡥࡥ࠯ࡺ࡭ࡳࡪ࡯ࡸࡵࠪ᷋"),
    bstack1l111l_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡴࡨࡲࡩ࡫ࡲࡦࡴ࠰ࡦࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࡩ࡯ࡩࠪ᷌"),
    bstack1l111l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡩࡩࡦࡺࡵࡳࡧࡶࡁ࡙ࡸࡡ࡯ࡵ࡯ࡥࡹ࡫ࡕࡊࠩ᷍"),
    bstack1l111l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰࡭ࡵࡩ࠭ࡧ࡮ࡲࡳࡩ࡯࡮ࡨ࠯ࡳࡶࡴࡺࡥࡤࡶ࡬ࡳࡳ᷎࠭"),
    bstack1l111l_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡼ࡫ࡢ࠮ࡵࡨࡧࡺࡸࡩࡵࡻ᷏ࠪ"),
    bstack1l111l_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡬ࡥࡢࡶࡸࡶࡪࡹ࠽ࡗ࡫ࡽࡈ࡮ࡹࡰ࡭ࡣࡼࡇࡴࡳࡰࡰࡵ࡬ࡸࡴࡸ᷐ࠧ"),
    bstack1l111l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳࡬ࡰࡩࡪ࡭ࡳ࡭ࠧ᷑"),
    bstack1l111l_opy_ (u"ࠫ࠲࠳ࡳࡪ࡮ࡨࡲࡹ࠭᷒")
]
def bstack11ll1111_opy_(options, bstack1l11lll1l1_opy_=bstack1l111l_opy_ (u"ࠧࠨᷓ")):
    bstack1l111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡉ࡯࡬ࡨࡧࡹࠦࡤࡦࡨࡤࡹࡱࡺࠠࡄࡪࡵࡳࡲ࡫ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣࡪࡴࡸࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠊࠡࠢࠣࠤࡆࡪࡤࡴࠢ࠴࠼ࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡵࠣࡨࡪ࡬ࡥ࡯ࡵ࡬ࡺࡪࡲࡹࠡࠪࡲࡲࡱࡿࠠࡪࡨࠣࡲࡴࡺࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡩࡸ࡫࡮ࡵࠫ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠣࡳࡧࡰࡥࡤࡶࠣࡳࡷࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡸ࡫ࡷ࡬ࠥࡧࡤࡥࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠬ࠮ࠦ࡭ࡦࡶ࡫ࡳࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡸࡪࡾࡴࡠࡰࡤࡱࡪࡀࠠࡄࡱࡱࡸࡪࡾࡴࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠥ࡬࡯ࡳࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠣࠬࡪ࠴ࡧ࠯࠮ࠣࠦࡵࡿࡴࡦࡵࡷࠦ࠱ࠦࠢࡱࡻࡷ࡬ࡴࡴࠢࠪࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡑࡹࡲࡨࡥࡳࠢࡲࡪࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡࡣࡧࡨࡪࡪࠊࠡࠢࠣࠤࠧࠨࠢᷔ")
    if not bstack1l11lll1l1_opy_:
        bstack1l11lll1l1_opy_ = bstack1l111l_opy_ (u"ࠢ࡭ࡱࡤࡨ࠲ࡺࡥࡴࡶ࡬ࡲ࡬ࠨᷕ")
    if options is None or not hasattr(options, bstack1l111l_opy_ (u"ࠨࡣࡧࡨࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧᷖ")):
        logger.debug(bstack1l111l_opy_ (u"ࠤ࡞ࡿࢂࡣࠠࡐࡲࡷ࡭ࡴࡴࡳࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠢࡲࡶࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡥࡦࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠭࠯ࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣ࡭ࡳࡰࡥࡤࡶ࡬ࡳࡳࠨᷗ").format(bstack1l11lll1l1_opy_))
        return 0
    bstack1111ll11lll_opy_ = getattr(options, bstack1l111l_opy_ (u"ࠪࡣࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᷘ"), [])
    if not isinstance(bstack1111ll11lll_opy_, list):
        bstack1111ll11lll_opy_ = []
    bstack11111ll1ll1_opy_ = set()
    for arg in bstack1111ll11lll_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1l111l_opy_ (u"ࠫࡂ࠭ᷙ"))[0] if bstack1l111l_opy_ (u"ࠬࡃࠧᷚ") in arg else arg
            bstack11111ll1ll1_opy_.add(flag)
    bstack111111ll1_opy_ = 0
    for arg in bstack11111ll1lll_opy_:
        flag = arg.split(bstack1l111l_opy_ (u"࠭࠽ࠨᷛ"))[0] if bstack1l111l_opy_ (u"ࠧ࠾ࠩᷜ") in arg else arg
        if flag not in bstack11111ll1ll1_opy_:
            options.add_argument(arg)
            bstack111111ll1_opy_ += 1
    if bstack111111ll1_opy_ > 0:
        logger.debug(bstack1l111l_opy_ (u"ࠣ࡝ࡾࢁࡢࠦࡉ࡯࡬ࡨࡧࡹ࡫ࡤࠡࡽࢀࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡴࠢࡩࡳࡷࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠧᷝ").format(bstack1l11lll1l1_opy_, bstack111111ll1_opy_))
    return bstack111111ll1_opy_