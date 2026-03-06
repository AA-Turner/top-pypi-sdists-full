# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
bstack1111_opy_ (u"ࠥࠦࠧࠐࡈࡦ࡮ࡳࡩࡷࠦࡦࡰࡴࠣ࡭ࡳࡰࡥࡤࡶ࡬ࡲ࡬ࠦࡤࡦࡨࡤࡹࡱࡺࠠࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠠࡢࡴࡪࡷࠥࡽࡨࡦࡰࠣࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩ࠴ࠊࡔࡶࡵ࡭ࡨࡺ࡬ࡺࠢࡧࡩ࡫࡫࡮ࡴ࡫ࡹࡩ࠿ࠦ࡮ࡦࡸࡨࡶࠥࡵࡶࡦࡴࡺࡶ࡮ࡺࡥࡴࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡦࡸࡧࡴ࠰ࠍࡘ࡭࡯ࡳࠡ࡫ࡶࠤࡹ࡮ࡥࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡧࡴࡹ࡮ࡼࡡ࡭ࡧࡱࡸࠥࡵࡦࠡࡌࡤࡺࡦ࠭ࡳࠡࡑࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࡎࡥ࡭ࡲࡨࡶ࠳ࠐࠢࠣࠤ᪥")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111111l1_opy_())
bstack111ll1lllll_opy_ = [
    bstack1111_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨ᪦"),
    bstack1111_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡪ࡮ࡸࡳࡵ࠯ࡵࡹࡳ࠭ᪧ"),
    bstack1111_opy_ (u"࠭࠭࠮ࡰࡲ࠱ࡩ࡫ࡦࡢࡷ࡯ࡸ࠲ࡨࡲࡰࡹࡶࡩࡷ࠳ࡣࡩࡧࡦ࡯ࠬ᪨"),
    bstack1111_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᪩"),
    bstack1111_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡩ࡫ࡦࡢࡷ࡯ࡸ࠲ࡧࡰࡱࡵࠪ᪪"),
    bstack1111_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡭ࡰࡶࠩ᪫"),
    bstack1111_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡤࡦࡸ࠰ࡷ࡭ࡳ࠭ࡶࡵࡤ࡫ࡪ࠭᪬"),
    bstack1111_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡴࡱࡩࡸࡼࡧࡲࡦ࠯ࡵࡥࡸࡺࡥࡳ࡫ࡽࡩࡷ࠭᪭"),
    bstack1111_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡷࡦࡴࡤࡣࡱࡻࠫ᪮"),
    bstack1111_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࠳ࡴࡪ࡯ࡨࡶ࠲ࡺࡨࡳࡱࡷࡸࡱ࡯࡮ࡨࠩ᪯"),
    bstack1111_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡦࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࡩ࡯ࡩ࠰ࡳࡨࡩ࡬ࡶࡦࡨࡨ࠲ࡽࡩ࡯ࡦࡲࡻࡸ࠭᪰"),
    bstack1111_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡷ࡫࡮ࡥࡧࡵࡩࡷ࠳ࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦ࡬ࡲ࡬࠭᪱"),
    bstack1111_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡬ࡥࡢࡶࡸࡶࡪࡹ࠽ࡕࡴࡤࡲࡸࡲࡡࡵࡧࡘࡍࠬ᪲"),
    bstack1111_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡩࡱࡥ࠰ࡪࡱࡵ࡯ࡥ࡫ࡱ࡫࠲ࡶࡲࡰࡶࡨࡧࡹ࡯࡯࡯ࠩ᪳"),
    bstack1111_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡸࡧࡥ࠱ࡸ࡫ࡣࡶࡴ࡬ࡸࡾ࠭᪴"),
    bstack1111_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡨࡨࡥࡹࡻࡲࡦࡵࡀ࡚࡮ࢀࡄࡪࡵࡳࡰࡦࡿࡃࡰ࡯ࡳࡳࡸ࡯ࡴࡰࡴ᪵ࠪ"),
    bstack1111_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯࡯ࡳ࡬࡭ࡩ࡯ࡩ᪶ࠪ"),
    bstack1111_opy_ (u"ࠧ࠮࠯ࡶ࡭ࡱ࡫࡮ࡵ᪷ࠩ")
]
def bstack1llllll1ll_opy_(options, bstack1l1l1111ll_opy_=bstack1111_opy_ (u"ࠣࠤ᪸")):
    bstack1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡌࡲ࡯࡫ࡣࡵࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡦࡰࡴࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠍࠤࠥࠦࠠࡂࡦࡧࡷࠥ࠷࠸ࠡࡅ࡫ࡶࡴࡳࡥࠡࡣࡵ࡫ࡸࠦࡤࡦࡨࡨࡲࡸ࡯ࡶࡦ࡮ࡼࠤ࠭ࡵ࡮࡭ࡻࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸࡥࡴࡧࡱࡸ࠮࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠦ࡯ࡣ࡬ࡨࡧࡹࠦ࡯ࡳࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡻ࡮ࡺࡨࠡࡣࡧࡨࡤࡧࡲࡨࡷࡰࡩࡳࡺࠨࠪࠢࡰࡩࡹ࡮࡯ࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡴࡦࡺࡷࡣࡳࡧ࡭ࡦ࠼ࠣࡇࡴࡴࡴࡦࡺࡷࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࡨࡲࡶࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࠨࡦ࠰ࡪ࠲࠱ࠦࠢࡱࡻࡷࡩࡸࡺࠢ࠭ࠢࠥࡴࡾࡺࡨࡰࡰࠥ࠭ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡔࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤࡦࡪࡤࡦࡦࠍࠤࠥࠦࠠࠣࠤ᪹ࠥ")
    if not bstack1l1l1111ll_opy_:
        bstack1l1l1111ll_opy_ = bstack1111_opy_ (u"ࠥࡰࡴࡧࡤ࠮ࡶࡨࡷࡹ࡯࡮ࡨࠤ᪺")
    if options is None or not hasattr(options, bstack1111_opy_ (u"ࠫࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ᪻")):
        logger.debug(bstack1111_opy_ (u"ࠧࡡࡻࡾ࡟ࠣࡓࡵࡺࡩࡰࡰࡶࠤ࡮ࡹࠠࡏࡱࡱࡩࠥࡵࡲࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡤࡨࡩࡥࡡࡳࡩࡸࡱࡪࡴࡴࠩࠫ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡩ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠤ᪼").format(bstack1l1l1111ll_opy_))
        return 0
    bstack11l11111lll_opy_ = getattr(options, bstack1111_opy_ (u"࠭࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ᪽ࠪ"), [])
    if not isinstance(bstack11l11111lll_opy_, list):
        bstack11l11111lll_opy_ = []
    bstack111lll11111_opy_ = set()
    for arg in bstack11l11111lll_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1111_opy_ (u"ࠧ࠾ࠩ᪾"))[0] if bstack1111_opy_ (u"ࠨ࠿ᪿࠪ") in arg else arg
            bstack111lll11111_opy_.add(flag)
    bstack11l11lll11_opy_ = 0
    for arg in bstack111ll1lllll_opy_:
        flag = arg.split(bstack1111_opy_ (u"ࠩࡀᫀࠫ"))[0] if bstack1111_opy_ (u"ࠪࡁࠬ᫁") in arg else arg
        if flag not in bstack111lll11111_opy_:
            options.add_argument(arg)
            bstack11l11lll11_opy_ += 1
    if bstack11l11lll11_opy_ > 0:
        logger.debug(bstack1111_opy_ (u"ࠦࡠࢁࡽ࡞ࠢࡌࡲ࡯࡫ࡣࡵࡧࡧࠤࢀࢃࠠࡄࡪࡵࡳࡲ࡫ࠠࡢࡴࡪࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠣ᫂").format(bstack1l1l1111ll_opy_, bstack11l11lll11_opy_))
    return bstack11l11lll11_opy_