# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
bstack11ll11_opy_ (u"ࠢࠣࠤࠍࡌࡪࡲࡰࡦࡴࠣࡪࡴࡸࠠࡪࡰ࡭ࡩࡨࡺࡩ࡯ࡩࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠤࡦࡸࡧࡴࠢࡺ࡬ࡪࡴࠠࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡨࡲࡦࡨ࡬ࡦࡦ࠱ࠎࡘࡺࡲࡪࡥࡷࡰࡾࠦࡤࡦࡨࡨࡲࡸ࡯ࡶࡦ࠼ࠣࡲࡪࡼࡥࡳࠢࡲࡺࡪࡸࡷࡳ࡫ࡷࡩࡸࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡣࡵ࡫ࡸ࠴ࠊࡕࡪ࡬ࡷࠥ࡯ࡳࠡࡶ࡫ࡩࠥࡖࡹࡵࡪࡲࡲࠥ࡫ࡱࡶ࡫ࡹࡥࡱ࡫࡮ࡵࠢࡲࡪࠥࡐࡡࡷࡣࠪࡷࠥࡕࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࡋࡩࡱࡶࡥࡳ࠰ࠍࠦࠧࠨᶤ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack11111lllll1_opy_ = [
    bstack11ll11_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᶥ"),
    bstack11ll11_opy_ (u"ࠩ࠰࠱ࡳࡵ࠭ࡧ࡫ࡵࡷࡹ࠳ࡲࡶࡰࠪᶦ"),
    bstack11ll11_opy_ (u"ࠪ࠱࠲ࡴ࡯࠮ࡦࡨࡪࡦࡻ࡬ࡵ࠯ࡥࡶࡴࡽࡳࡦࡴ࠰ࡧ࡭࡫ࡣ࡬ࠩᶧ"),
    bstack11ll11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᶨ"),
    bstack11ll11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡦࡨࡪࡦࡻ࡬ࡵ࠯ࡤࡴࡵࡹࠧᶩ"),
    bstack11ll11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡪࡴࡺ࠭ᶪ"),
    bstack11ll11_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡨࡪࡼ࠭ࡴࡪࡰ࠱ࡺࡹࡡࡨࡧࠪᶫ"),
    bstack11ll11_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡸࡵࡦࡵࡹࡤࡶࡪ࠳ࡲࡢࡵࡷࡩࡷ࡯ࡺࡦࡴࠪᶬ"),
    bstack11ll11_opy_ (u"ࠩ࠰࠱ࡳࡵ࠭ࡴࡣࡱࡨࡧࡵࡸࠨᶭ"),
    bstack11ll11_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦ࠰ࡸ࡮ࡳࡥࡳ࠯ࡷ࡬ࡷࡵࡴࡵ࡮࡬ࡲ࡬࠭ᶮ"),
    bstack11ll11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡣࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧ࡭ࡳ࡭࠭ࡰࡥࡦࡰࡺࡪࡥࡥ࠯ࡺ࡭ࡳࡪ࡯ࡸࡵࠪᶯ"),
    bstack11ll11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡴࡨࡲࡩ࡫ࡲࡦࡴ࠰ࡦࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࡩ࡯ࡩࠪᶰ"),
    bstack11ll11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡩࡩࡦࡺࡵࡳࡧࡶࡁ࡙ࡸࡡ࡯ࡵ࡯ࡥࡹ࡫ࡕࡊࠩᶱ"),
    bstack11ll11_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰࡭ࡵࡩ࠭ࡧ࡮ࡲࡳࡩ࡯࡮ࡨ࠯ࡳࡶࡴࡺࡥࡤࡶ࡬ࡳࡳ࠭ᶲ"),
    bstack11ll11_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡼ࡫ࡢ࠮ࡵࡨࡧࡺࡸࡩࡵࡻࠪᶳ"),
    bstack11ll11_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡬ࡥࡢࡶࡸࡶࡪࡹ࠽ࡗ࡫ࡽࡈ࡮ࡹࡰ࡭ࡣࡼࡇࡴࡳࡰࡰࡵ࡬ࡸࡴࡸࠧᶴ"),
    bstack11ll11_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳࡬ࡰࡩࡪ࡭ࡳ࡭ࠧᶵ"),
    bstack11ll11_opy_ (u"ࠫ࠲࠳ࡳࡪ࡮ࡨࡲࡹ࠭ᶶ")
]
def bstack1111llll1_opy_(options, bstack111lll111_opy_=bstack11ll11_opy_ (u"ࠧࠨᶷ")):
    bstack11ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡉ࡯࡬ࡨࡧࡹࠦࡤࡦࡨࡤࡹࡱࡺࠠࡄࡪࡵࡳࡲ࡫ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣࡪࡴࡸࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠊࠡࠢࠣࠤࡆࡪࡤࡴࠢ࠴࠼ࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡵࠣࡨࡪ࡬ࡥ࡯ࡵ࡬ࡺࡪࡲࡹࠡࠪࡲࡲࡱࡿࠠࡪࡨࠣࡲࡴࡺࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡩࡸ࡫࡮ࡵࠫ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠣࡳࡧࡰࡥࡤࡶࠣࡳࡷࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡸ࡫ࡷ࡬ࠥࡧࡤࡥࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠬ࠮ࠦ࡭ࡦࡶ࡫ࡳࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡸࡪࡾࡴࡠࡰࡤࡱࡪࡀࠠࡄࡱࡱࡸࡪࡾࡴࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠥ࡬࡯ࡳࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠣࠬࡪ࠴ࡧ࠯࠮ࠣࠦࡵࡿࡴࡦࡵࡷࠦ࠱ࠦࠢࡱࡻࡷ࡬ࡴࡴࠢࠪࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡑࡹࡲࡨࡥࡳࠢࡲࡪࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡࡣࡧࡨࡪࡪࠊࠡࠢࠣࠤࠧࠨࠢᶸ")
    if not bstack111lll111_opy_:
        bstack111lll111_opy_ = bstack11ll11_opy_ (u"ࠢ࡭ࡱࡤࡨ࠲ࡺࡥࡴࡶ࡬ࡲ࡬ࠨᶹ")
    if options is None or not hasattr(options, bstack11ll11_opy_ (u"ࠨࡣࡧࡨࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧᶺ")):
        logger.debug(bstack11ll11_opy_ (u"ࠤ࡞ࡿࢂࡣࠠࡐࡲࡷ࡭ࡴࡴࡳࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠢࡲࡶࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡥࡦࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠭࠯ࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣ࡭ࡳࡰࡥࡤࡶ࡬ࡳࡳࠨᶻ").format(bstack111lll111_opy_))
        return 0
    bstack1111lll1l1l_opy_ = getattr(options, bstack11ll11_opy_ (u"ࠪࡣࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᶼ"), [])
    if not isinstance(bstack1111lll1l1l_opy_, list):
        bstack1111lll1l1l_opy_ = []
    bstack11111llll1l_opy_ = set()
    for arg in bstack1111lll1l1l_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack11ll11_opy_ (u"ࠫࡂ࠭ᶽ"))[0] if bstack11ll11_opy_ (u"ࠬࡃࠧᶾ") in arg else arg
            bstack11111llll1l_opy_.add(flag)
    bstack1ll1l11ll1_opy_ = 0
    for arg in bstack11111lllll1_opy_:
        flag = arg.split(bstack11ll11_opy_ (u"࠭࠽ࠨᶿ"))[0] if bstack11ll11_opy_ (u"ࠧ࠾ࠩ᷀") in arg else arg
        if flag not in bstack11111llll1l_opy_:
            options.add_argument(arg)
            bstack1ll1l11ll1_opy_ += 1
    if bstack1ll1l11ll1_opy_ > 0:
        logger.debug(bstack11ll11_opy_ (u"ࠣ࡝ࡾࢁࡢࠦࡉ࡯࡬ࡨࡧࡹ࡫ࡤࠡࡽࢀࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡴࠢࡩࡳࡷࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠧ᷁").format(bstack111lll111_opy_, bstack1ll1l11ll1_opy_))
    return bstack1ll1l11ll1_opy_