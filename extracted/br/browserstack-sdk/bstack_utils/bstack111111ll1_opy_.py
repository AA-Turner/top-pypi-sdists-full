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
bstack111ll_opy_ (u"ࠣࠤࠥࠎࡍ࡫࡬ࡱࡧࡵࠤ࡫ࡵࡲࠡ࡫ࡱ࡮ࡪࡩࡴࡪࡰࡪࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠥࡧࡲࡨࡵࠣࡻ࡭࡫࡮ࠡࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡩࡳࡧࡢ࡭ࡧࡧ࠲ࠏ࡙ࡴࡳ࡫ࡦࡸࡱࡿࠠࡥࡧࡩࡩࡳࡹࡩࡷࡧ࠽ࠤࡳ࡫ࡶࡦࡴࠣࡳࡻ࡫ࡲࡸࡴ࡬ࡸࡪࡹࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡤࡶ࡬ࡹ࠮ࠋࡖ࡫࡭ࡸࠦࡩࡴࠢࡷ࡬ࡪࠦࡐࡺࡶ࡫ࡳࡳࠦࡥࡲࡷ࡬ࡺࡦࡲࡥ࡯ࡶࠣࡳ࡫ࠦࡊࡢࡸࡤࠫࡸࠦࡏࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࡌࡪࡲࡰࡦࡴ࠱ࠎࠧࠨࠢᷝ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack11111ll111l_opy_ = [
    bstack111ll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᷞ"),
    bstack111ll_opy_ (u"ࠪ࠱࠲ࡴ࡯࠮ࡨ࡬ࡶࡸࡺ࠭ࡳࡷࡱࠫᷟ"),
    bstack111ll_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡧࡩ࡫ࡧࡵ࡭ࡶ࠰ࡦࡷࡵࡷࡴࡧࡵ࠱ࡨ࡮ࡥࡤ࡭ࠪᷠ"),
    bstack111ll_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᷡ"),
    bstack111ll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡧࡩ࡫ࡧࡵ࡭ࡶ࠰ࡥࡵࡶࡳࠨᷢ"),
    bstack111ll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰࡫ࡵࡻࠧᷣ"),
    bstack111ll_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡩ࡫ࡶ࠮ࡵ࡫ࡱ࠲ࡻࡳࡢࡩࡨࠫᷤ"),
    bstack111ll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡹ࡯ࡧࡶࡺࡥࡷ࡫࠭ࡳࡣࡶࡸࡪࡸࡩࡻࡧࡵࠫᷥ"),
    bstack111ll_opy_ (u"ࠪ࠱࠲ࡴ࡯࠮ࡵࡤࡲࡩࡨ࡯ࡹࠩᷦ"),
    bstack111ll_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡣࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧ࠱ࡹ࡯࡭ࡦࡴ࠰ࡸ࡭ࡸ࡯ࡵࡶ࡯࡭ࡳ࡭ࠧᷧ"),
    bstack111ll_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࡮ࡴࡧ࠮ࡱࡦࡧࡱࡻࡤࡦࡦ࠰ࡻ࡮ࡴࡤࡰࡹࡶࠫᷨ"),
    bstack111ll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡵࡩࡳࡪࡥࡳࡧࡵ࠱ࡧࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࡪࡰࡪࠫᷩ"),
    bstack111ll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡪࡪࡧࡴࡶࡴࡨࡷࡂ࡚ࡲࡢࡰࡶࡰࡦࡺࡥࡖࡋࠪᷪ"),
    bstack111ll_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡮ࡶࡣ࠮ࡨ࡯ࡳࡴࡪࡩ࡯ࡩ࠰ࡴࡷࡵࡴࡦࡥࡷ࡭ࡴࡴࠧᷫ"),
    bstack111ll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡽࡥࡣ࠯ࡶࡩࡨࡻࡲࡪࡶࡼࠫᷬ"),
    bstack111ll_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡦࡦࡣࡷࡹࡷ࡫ࡳ࠾ࡘ࡬ࡾࡉ࡯ࡳࡱ࡮ࡤࡽࡈࡵ࡭ࡱࡱࡶ࡭ࡹࡵࡲࠨᷭ"),
    bstack111ll_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭࡭ࡱࡪ࡫࡮ࡴࡧࠨᷮ"),
    bstack111ll_opy_ (u"ࠬ࠳࠭ࡴ࡫࡯ࡩࡳࡺࠧᷯ")
]
def bstack1l1l1l1ll_opy_(options, bstack11l1ll1111_opy_=bstack111ll_opy_ (u"ࠨࠢᷰ")):
    bstack111ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡊࡰ࡭ࡩࡨࡺࠠࡥࡧࡩࡥࡺࡲࡴࠡࡅ࡫ࡶࡴࡳࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡫ࡵࡲࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠋࠢࠣࠤࠥࡇࡤࡥࡵࠣ࠵࠽ࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡶࠤࡩ࡫ࡦࡦࡰࡶ࡭ࡻ࡫࡬ࡺࠢࠫࡳࡳࡲࡹࠡ࡫ࡩࠤࡳࡵࡴࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡪࡹࡥ࡯ࡶࠬ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠤࡴࡨࡪࡦࡥࡷࠤࡴࡸࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡹ࡬ࡸ࡭ࠦࡡࡥࡦࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠭࠯ࠠ࡮ࡧࡷ࡬ࡴࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡹ࡫ࡸࡵࡡࡱࡥࡲ࡫࠺ࠡࡅࡲࡲࡹ࡫ࡸࡵࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠦࡦࡰࡴࠣࡰࡴ࡭ࡧࡪࡰࡪࠤ࠭࡫࠮ࡨ࠰࠯ࠤࠧࡶࡹࡵࡧࡶࡸࠧ࠲ࠠࠣࡲࡼࡸ࡭ࡵ࡮ࠣࠫࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡒࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࡤࡨࡩ࡫ࡤࠋࠢࠣࠤࠥࠨࠢࠣᷱ")
    if not bstack11l1ll1111_opy_:
        bstack11l1ll1111_opy_ = bstack111ll_opy_ (u"ࠣ࡮ࡲࡥࡩ࠳ࡴࡦࡵࡷ࡭ࡳ࡭ࠢᷲ")
    if options is None or not hasattr(options, bstack111ll_opy_ (u"ࠩࡤࡨࡩࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨᷳ")):
        logger.debug(bstack111ll_opy_ (u"ࠥ࡟ࢀࢃ࡝ࠡࡑࡳࡸ࡮ࡵ࡮ࡴࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠣࡳࡷࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠮ࠩ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤ࡮ࡴࡪࡦࡥࡷ࡭ࡴࡴࠢᷴ").format(bstack11l1ll1111_opy_))
        return 0
    bstack1111l1lll1l_opy_ = getattr(options, bstack111ll_opy_ (u"ࠫࡤࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ᷵"), [])
    if not isinstance(bstack1111l1lll1l_opy_, list):
        bstack1111l1lll1l_opy_ = []
    bstack11111ll1111_opy_ = set()
    for arg in bstack1111l1lll1l_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack111ll_opy_ (u"ࠬࡃࠧ᷶"))[0] if bstack111ll_opy_ (u"࠭࠽ࠨ᷷") in arg else arg
            bstack11111ll1111_opy_.add(flag)
    bstack11l11l11ll_opy_ = 0
    for arg in bstack11111ll111l_opy_:
        flag = arg.split(bstack111ll_opy_ (u"ࠧ࠾᷸ࠩ"))[0] if bstack111ll_opy_ (u"ࠨ࠿᷹ࠪ") in arg else arg
        if flag not in bstack11111ll1111_opy_:
            options.add_argument(arg)
            bstack11l11l11ll_opy_ += 1
    if bstack11l11l11ll_opy_ > 0:
        logger.debug(bstack111ll_opy_ (u"ࠤ࡞ࡿࢂࡣࠠࡊࡰ࡭ࡩࡨࡺࡥࡥࠢࡾࢁࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡵࠣࡪࡴࡸࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠨ᷺").format(bstack11l1ll1111_opy_, bstack11l11l11ll_opy_))
    return bstack11l11l11ll_opy_