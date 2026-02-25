# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
bstack11l1l11_opy_ (u"ࠣࠤࠥࠎࡍ࡫࡬ࡱࡧࡵࠤ࡫ࡵࡲࠡ࡫ࡱ࡮ࡪࡩࡴࡪࡰࡪࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠥࡧࡲࡨࡵࠣࡻ࡭࡫࡮ࠡࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡩࡳࡧࡢ࡭ࡧࡧ࠲ࠏ࡙ࡴࡳ࡫ࡦࡸࡱࡿࠠࡥࡧࡩࡩࡳࡹࡩࡷࡧ࠽ࠤࡳ࡫ࡶࡦࡴࠣࡳࡻ࡫ࡲࡸࡴ࡬ࡸࡪࡹࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡤࡶ࡬ࡹ࠮ࠋࡖ࡫࡭ࡸࠦࡩࡴࠢࡷ࡬ࡪࠦࡐࡺࡶ࡫ࡳࡳࠦࡥࡲࡷ࡬ࡺࡦࡲࡥ࡯ࡶࠣࡳ࡫ࠦࡊࡢࡸࡤࠫࡸࠦࡏࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࡌࡪࡲࡰࡦࡴ࠱ࠎࠧࠨࠢ᥽")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1111l11l_opy_())
bstack11l1111111l_opy_ = [
    bstack11l1l11_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭᥾"),
    bstack11l1l11_opy_ (u"ࠪ࠱࠲ࡴ࡯࠮ࡨ࡬ࡶࡸࡺ࠭ࡳࡷࡱࠫ᥿"),
    bstack11l1l11_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡧࡩ࡫ࡧࡵ࡭ࡶ࠰ࡦࡷࡵࡷࡴࡧࡵ࠱ࡨ࡮ࡥࡤ࡭ࠪᦀ"),
    bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᦁ"),
    bstack11l1l11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡧࡩ࡫ࡧࡵ࡭ࡶ࠰ࡥࡵࡶࡳࠨᦂ"),
    bstack11l1l11_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰࡫ࡵࡻࠧᦃ"),
    bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡩ࡫ࡶ࠮ࡵ࡫ࡱ࠲ࡻࡳࡢࡩࡨࠫᦄ"),
    bstack11l1l11_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡹ࡯ࡧࡶࡺࡥࡷ࡫࠭ࡳࡣࡶࡸࡪࡸࡩࡻࡧࡵࠫᦅ"),
    bstack11l1l11_opy_ (u"ࠪ࠱࠲ࡴ࡯࠮ࡵࡤࡲࡩࡨ࡯ࡹࠩᦆ"),
    bstack11l1l11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡣࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧ࠱ࡹ࡯࡭ࡦࡴ࠰ࡸ࡭ࡸ࡯ࡵࡶ࡯࡭ࡳ࡭ࠧᦇ"),
    bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࡮ࡴࡧ࠮ࡱࡦࡧࡱࡻࡤࡦࡦ࠰ࡻ࡮ࡴࡤࡰࡹࡶࠫᦈ"),
    bstack11l1l11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡵࡩࡳࡪࡥࡳࡧࡵ࠱ࡧࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࡪࡰࡪࠫᦉ"),
    bstack11l1l11_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡪࡪࡧࡴࡶࡴࡨࡷࡂ࡚ࡲࡢࡰࡶࡰࡦࡺࡥࡖࡋࠪᦊ"),
    bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡮ࡶࡣ࠮ࡨ࡯ࡳࡴࡪࡩ࡯ࡩ࠰ࡴࡷࡵࡴࡦࡥࡷ࡭ࡴࡴࠧᦋ"),
    bstack11l1l11_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡽࡥࡣ࠯ࡶࡩࡨࡻࡲࡪࡶࡼࠫᦌ"),
    bstack11l1l11_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡦࡦࡣࡷࡹࡷ࡫ࡳ࠾ࡘ࡬ࡾࡉ࡯ࡳࡱ࡮ࡤࡽࡈࡵ࡭ࡱࡱࡶ࡭ࡹࡵࡲࠨᦍ"),
    bstack11l1l11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭࡭ࡱࡪ࡫࡮ࡴࡧࠨᦎ"),
    bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡴ࡫࡯ࡩࡳࡺࠧᦏ")
]
def bstack1ll11111_opy_(options, bstack1lll1ll11_opy_=bstack11l1l11_opy_ (u"ࠨࠢᦐ")):
    bstack11l1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡊࡰ࡭ࡩࡨࡺࠠࡥࡧࡩࡥࡺࡲࡴࠡࡅ࡫ࡶࡴࡳࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡫ࡵࡲࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠋࠢࠣࠤࠥࡇࡤࡥࡵࠣ࠵࠽ࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡶࠤࡩ࡫ࡦࡦࡰࡶ࡭ࡻ࡫࡬ࡺࠢࠫࡳࡳࡲࡹࠡ࡫ࡩࠤࡳࡵࡴࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡪࡹࡥ࡯ࡶࠬ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠤࡴࡨࡪࡦࡥࡷࠤࡴࡸࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡹ࡬ࡸ࡭ࠦࡡࡥࡦࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠭࠯ࠠ࡮ࡧࡷ࡬ࡴࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡹ࡫ࡸࡵࡡࡱࡥࡲ࡫࠺ࠡࡅࡲࡲࡹ࡫ࡸࡵࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠦࡦࡰࡴࠣࡰࡴ࡭ࡧࡪࡰࡪࠤ࠭࡫࠮ࡨ࠰࠯ࠤࠧࡶࡹࡵࡧࡶࡸࠧ࠲ࠠࠣࡲࡼࡸ࡭ࡵ࡮ࠣࠫࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡒࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࡤࡨࡩ࡫ࡤࠋࠢࠣࠤࠥࠨࠢࠣᦑ")
    if not bstack1lll1ll11_opy_:
        bstack1lll1ll11_opy_ = bstack11l1l11_opy_ (u"ࠣ࡮ࡲࡥࡩ࠳ࡴࡦࡵࡷ࡭ࡳ࡭ࠢᦒ")
    if options is None or not hasattr(options, bstack11l1l11_opy_ (u"ࠩࡤࡨࡩࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨᦓ")):
        logger.debug(bstack11l1l11_opy_ (u"ࠥ࡟ࢀࢃ࡝ࠡࡑࡳࡸ࡮ࡵ࡮ࡴࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠣࡳࡷࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠮ࠩ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤ࡮ࡴࡪࡦࡥࡷ࡭ࡴࡴࠢᦔ").format(bstack1lll1ll11_opy_))
        return 0
    bstack11l11l1lll1_opy_ = getattr(options, bstack11l1l11_opy_ (u"ࠫࡤࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᦕ"), [])
    if not isinstance(bstack11l11l1lll1_opy_, list):
        bstack11l11l1lll1_opy_ = []
    bstack11l111111l1_opy_ = set()
    for arg in bstack11l11l1lll1_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack11l1l11_opy_ (u"ࠬࡃࠧᦖ"))[0] if bstack11l1l11_opy_ (u"࠭࠽ࠨᦗ") in arg else arg
            bstack11l111111l1_opy_.add(flag)
    bstack11l1l1lll_opy_ = 0
    for arg in bstack11l1111111l_opy_:
        flag = arg.split(bstack11l1l11_opy_ (u"ࠧ࠾ࠩᦘ"))[0] if bstack11l1l11_opy_ (u"ࠨ࠿ࠪᦙ") in arg else arg
        if flag not in bstack11l111111l1_opy_:
            options.add_argument(arg)
            bstack11l1l1lll_opy_ += 1
    if bstack11l1l1lll_opy_ > 0:
        logger.debug(bstack11l1l11_opy_ (u"ࠤ࡞ࡿࢂࡣࠠࡊࡰ࡭ࡩࡨࡺࡥࡥࠢࡾࢁࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡵࠣࡪࡴࡸࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠨᦚ").format(bstack1lll1ll11_opy_, bstack11l1l1lll_opy_))
    return bstack11l1l1lll_opy_