# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
bstack1ll_opy_ (u"ࠥࠦࠧࠐࡈࡦ࡮ࡳࡩࡷࠦࡦࡰࡴࠣ࡭ࡳࡰࡥࡤࡶ࡬ࡲ࡬ࠦࡤࡦࡨࡤࡹࡱࡺࠠࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠠࡢࡴࡪࡷࠥࡽࡨࡦࡰࠣࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩ࠴ࠊࡔࡶࡵ࡭ࡨࡺ࡬ࡺࠢࡧࡩ࡫࡫࡮ࡴ࡫ࡹࡩ࠿ࠦ࡮ࡦࡸࡨࡶࠥࡵࡶࡦࡴࡺࡶ࡮ࡺࡥࡴࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡦࡸࡧࡴ࠰ࠍࡘ࡭࡯ࡳࠡ࡫ࡶࠤࡹ࡮ࡥࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡧࡴࡹ࡮ࡼࡡ࡭ࡧࡱࡸࠥࡵࡦࠡࡌࡤࡺࡦ࠭ࡳࠡࡑࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࡎࡥ࡭ࡲࡨࡶ࠳ࠐࠢࠣࠤᶧ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack11111lll11l_opy_ = [
    bstack1ll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᶨ"),
    bstack1ll_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡪ࡮ࡸࡳࡵ࠯ࡵࡹࡳ࠭ᶩ"),
    bstack1ll_opy_ (u"࠭࠭࠮ࡰࡲ࠱ࡩ࡫ࡦࡢࡷ࡯ࡸ࠲ࡨࡲࡰࡹࡶࡩࡷ࠳ࡣࡩࡧࡦ࡯ࠬᶪ"),
    bstack1ll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᶫ"),
    bstack1ll_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡩ࡫ࡦࡢࡷ࡯ࡸ࠲ࡧࡰࡱࡵࠪᶬ"),
    bstack1ll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡭ࡰࡶࠩᶭ"),
    bstack1ll_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡤࡦࡸ࠰ࡷ࡭ࡳ࠭ࡶࡵࡤ࡫ࡪ࠭ᶮ"),
    bstack1ll_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡴࡱࡩࡸࡼࡧࡲࡦ࠯ࡵࡥࡸࡺࡥࡳ࡫ࡽࡩࡷ࠭ᶯ"),
    bstack1ll_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡷࡦࡴࡤࡣࡱࡻࠫᶰ"),
    bstack1ll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࠳ࡴࡪ࡯ࡨࡶ࠲ࡺࡨࡳࡱࡷࡸࡱ࡯࡮ࡨࠩᶱ"),
    bstack1ll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡦࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࡩ࡯ࡩ࠰ࡳࡨࡩ࡬ࡶࡦࡨࡨ࠲ࡽࡩ࡯ࡦࡲࡻࡸ࠭ᶲ"),
    bstack1ll_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡷ࡫࡮ࡥࡧࡵࡩࡷ࠳ࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦ࡬ࡲ࡬࠭ᶳ"),
    bstack1ll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡬ࡥࡢࡶࡸࡶࡪࡹ࠽ࡕࡴࡤࡲࡸࡲࡡࡵࡧࡘࡍࠬᶴ"),
    bstack1ll_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡩࡱࡥ࠰ࡪࡱࡵ࡯ࡥ࡫ࡱ࡫࠲ࡶࡲࡰࡶࡨࡧࡹ࡯࡯࡯ࠩᶵ"),
    bstack1ll_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡸࡧࡥ࠱ࡸ࡫ࡣࡶࡴ࡬ࡸࡾ࠭ᶶ"),
    bstack1ll_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡨࡨࡥࡹࡻࡲࡦࡵࡀ࡚࡮ࢀࡄࡪࡵࡳࡰࡦࡿࡃࡰ࡯ࡳࡳࡸ࡯ࡴࡰࡴࠪᶷ"),
    bstack1ll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯࡯ࡳ࡬࡭ࡩ࡯ࡩࠪᶸ"),
    bstack1ll_opy_ (u"ࠧ࠮࠯ࡶ࡭ࡱ࡫࡮ࡵࠩᶹ")
]
def bstack1l11l1l1l1_opy_(options, bstack1ll1l1l1_opy_=bstack1ll_opy_ (u"ࠣࠤᶺ")):
    bstack1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡌࡲ࡯࡫ࡣࡵࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡦࡰࡴࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠍࠤࠥࠦࠠࡂࡦࡧࡷࠥ࠷࠸ࠡࡅ࡫ࡶࡴࡳࡥࠡࡣࡵ࡫ࡸࠦࡤࡦࡨࡨࡲࡸ࡯ࡶࡦ࡮ࡼࠤ࠭ࡵ࡮࡭ࡻࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸࡥࡴࡧࡱࡸ࠮࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠦ࡯ࡣ࡬ࡨࡧࡹࠦ࡯ࡳࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡻ࡮ࡺࡨࠡࡣࡧࡨࡤࡧࡲࡨࡷࡰࡩࡳࡺࠨࠪࠢࡰࡩࡹ࡮࡯ࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡴࡦࡺࡷࡣࡳࡧ࡭ࡦ࠼ࠣࡇࡴࡴࡴࡦࡺࡷࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࡨࡲࡶࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࠨࡦ࠰ࡪ࠲࠱ࠦࠢࡱࡻࡷࡩࡸࡺࠢ࠭ࠢࠥࡴࡾࡺࡨࡰࡰࠥ࠭ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡔࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤࡦࡪࡤࡦࡦࠍࠤࠥࠦࠠࠣࠤࠥᶻ")
    if not bstack1ll1l1l1_opy_:
        bstack1ll1l1l1_opy_ = bstack1ll_opy_ (u"ࠥࡰࡴࡧࡤ࠮ࡶࡨࡷࡹ࡯࡮ࡨࠤᶼ")
    if options is None or not hasattr(options, bstack1ll_opy_ (u"ࠫࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪᶽ")):
        logger.debug(bstack1ll_opy_ (u"ࠧࡡࡻࡾ࡟ࠣࡓࡵࡺࡩࡰࡰࡶࠤ࡮ࡹࠠࡏࡱࡱࡩࠥࡵࡲࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡤࡨࡩࡥࡡࡳࡩࡸࡱࡪࡴࡴࠩࠫ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡩ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠤᶾ").format(bstack1ll1l1l1_opy_))
        return 0
    bstack1111lll1lll_opy_ = getattr(options, bstack1ll_opy_ (u"࠭࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᶿ"), [])
    if not isinstance(bstack1111lll1lll_opy_, list):
        bstack1111lll1lll_opy_ = []
    bstack11111lll111_opy_ = set()
    for arg in bstack1111lll1lll_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1ll_opy_ (u"ࠧ࠾ࠩ᷀"))[0] if bstack1ll_opy_ (u"ࠨ࠿ࠪ᷁") in arg else arg
            bstack11111lll111_opy_.add(flag)
    bstack1llll11ll1_opy_ = 0
    for arg in bstack11111lll11l_opy_:
        flag = arg.split(bstack1ll_opy_ (u"ࠩࡀ᷂ࠫ"))[0] if bstack1ll_opy_ (u"ࠪࡁࠬ᷃") in arg else arg
        if flag not in bstack11111lll111_opy_:
            options.add_argument(arg)
            bstack1llll11ll1_opy_ += 1
    if bstack1llll11ll1_opy_ > 0:
        logger.debug(bstack1ll_opy_ (u"ࠦࡠࢁࡽ࡞ࠢࡌࡲ࡯࡫ࡣࡵࡧࡧࠤࢀࢃࠠࡄࡪࡵࡳࡲ࡫ࠠࡢࡴࡪࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠣ᷄").format(bstack1ll1l1l1_opy_, bstack1llll11ll1_opy_))
    return bstack1llll11ll1_opy_