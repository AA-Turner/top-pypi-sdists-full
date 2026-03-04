# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
bstack1lll1l_opy_ (u"ࠤࠥࠦࠏࡎࡥ࡭ࡲࡨࡶࠥ࡬࡯ࡳࠢ࡬ࡲ࡯࡫ࡣࡵ࡫ࡱ࡫ࠥࡪࡥࡧࡣࡸࡰࡹࠦࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠦࡡࡳࡩࡶࠤࡼ࡮ࡥ࡯ࠢࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨ࠳ࠐࡓࡵࡴ࡬ࡧࡹࡲࡹࠡࡦࡨࡪࡪࡴࡳࡪࡸࡨ࠾ࠥࡴࡥࡷࡧࡵࠤࡴࡼࡥࡳࡹࡵ࡭ࡹ࡫ࡳࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡥࡷ࡭ࡳ࠯ࠌࡗ࡬࡮ࡹࠠࡪࡵࠣࡸ࡭࡫ࠠࡑࡻࡷ࡬ࡴࡴࠠࡦࡳࡸ࡭ࡻࡧ࡬ࡦࡰࡷࠤࡴ࡬ࠠࡋࡣࡹࡥࠬࡹࠠࡐࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬ࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࡍ࡫࡬ࡱࡧࡵ࠲ࠏࠨࠢࠣ᪤")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.bstack1l1llllll11_opy_())
bstack111lll1111l_opy_ = [
    bstack1lll1l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ᪥"),
    bstack1lll1l_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡩ࡭ࡷࡹࡴ࠮ࡴࡸࡲࠬ᪦"),
    bstack1lll1l_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡨࡪ࡬ࡡࡶ࡮ࡷ࠱ࡧࡸ࡯ࡸࡵࡨࡶ࠲ࡩࡨࡦࡥ࡮ࠫᪧ"),
    bstack1lll1l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᪨"),
    bstack1lll1l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡨࡪ࡬ࡡࡶ࡮ࡷ࠱ࡦࡶࡰࡴࠩ᪩"),
    bstack1lll1l_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡬ࡶࡵࠨ᪪"),
    bstack1lll1l_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡪࡥࡷ࠯ࡶ࡬ࡲ࠳ࡵࡴࡣࡪࡩࠬ᪫"),
    bstack1lll1l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡳࡰࡨࡷࡻࡦࡸࡥ࠮ࡴࡤࡷࡹ࡫ࡲࡪࡼࡨࡶࠬ᪬"),
    bstack1lll1l_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡶࡥࡳࡪࡢࡰࡺࠪ᪭"),
    bstack1lll1l_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࠲ࡺࡩ࡮ࡧࡵ࠱ࡹ࡮ࡲࡰࡶࡷࡰ࡮ࡴࡧࠨ᪮"),
    bstack1lll1l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࡯࡮ࡨ࠯ࡲࡧࡨࡲࡵࡥࡧࡧ࠱ࡼ࡯࡮ࡥࡱࡺࡷࠬ᪯"),
    bstack1lll1l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡶࡪࡴࡤࡦࡴࡨࡶ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࡫ࡱ࡫ࠬ᪰"),
    bstack1lll1l_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡫࡫ࡡࡵࡷࡵࡩࡸࡃࡔࡳࡣࡱࡷࡱࡧࡴࡦࡗࡌࠫ᪱"),
    bstack1lll1l_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡯ࡰࡤ࠯ࡩࡰࡴࡵࡤࡪࡰࡪ࠱ࡵࡸ࡯ࡵࡧࡦࡸ࡮ࡵ࡮ࠨ᪲"),
    bstack1lll1l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡷࡦࡤ࠰ࡷࡪࡩࡵࡳ࡫ࡷࡽࠬ᪳"),
    bstack1lll1l_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡧࡧࡤࡸࡺࡸࡥࡴ࠿࡙࡭ࡿࡊࡩࡴࡲ࡯ࡥࡾࡉ࡯࡮ࡲࡲࡷ࡮ࡺ࡯ࡳࠩ᪴"),
    bstack1lll1l_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮࡮ࡲ࡫࡬࡯࡮ࡨ᪵ࠩ"),
    bstack1lll1l_opy_ (u"࠭࠭࠮ࡵ࡬ࡰࡪࡴࡴࠨ᪶")
]
def bstack11llll1ll1_opy_(options, bstack111l11l1ll_opy_=bstack1lll1l_opy_ (u"᪷ࠢࠣ")):
    bstack1lll1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡋࡱ࡮ࡪࡩࡴࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠌࠣࠤࠥࠦࡁࡥࡦࡶࠤ࠶࠾ࠠࡄࡪࡵࡳࡲ࡫ࠠࡢࡴࡪࡷࠥࡪࡥࡧࡧࡱࡷ࡮ࡼࡥ࡭ࡻࠣࠬࡴࡴ࡬ࡺࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷ࡫ࡳࡦࡰࡷ࠭࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠥࡵࡢ࡫ࡧࡦࡸࠥࡵࡲࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡺ࡭ࡹ࡮ࠠࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠮ࠩࠡ࡯ࡨࡸ࡭ࡵࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡺࡥࡹࡶࡢࡲࡦࡳࡥ࠻ࠢࡆࡳࡳࡺࡥࡹࡶࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࡧࡱࡵࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥ࠮ࡥ࠯ࡩ࠱࠰ࠥࠨࡰࡺࡶࡨࡷࡹࠨࠬࠡࠤࡳࡽࡹ࡮࡯࡯ࠤࠬࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡓࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣࡥࡩࡪࡥࡥࠌࠣࠤࠥࠦࠢࠣࠤ᪸")
    if not bstack111l11l1ll_opy_:
        bstack111l11l1ll_opy_ = bstack1lll1l_opy_ (u"ࠤ࡯ࡳࡦࡪ࠭ࡵࡧࡶࡸ࡮ࡴࡧ᪹ࠣ")
    if options is None or not hasattr(options, bstack1lll1l_opy_ (u"ࠪࡥࡩࡪ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵ᪺ࠩ")):
        logger.debug(bstack1lll1l_opy_ (u"ࠦࡠࢁࡽ࡞ࠢࡒࡴࡹ࡯࡯࡯ࡵࠣ࡭ࡸࠦࡎࡰࡰࡨࠤࡴࡸࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡣࡧࡨࡤࡧࡲࡨࡷࡰࡩࡳࡺࠨࠪ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥ࡯࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠣ᪻").format(bstack111l11l1ll_opy_))
        return 0
    bstack11l1111lll1_opy_ = getattr(options, bstack1lll1l_opy_ (u"ࠬࡥࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ᪼"), [])
    if not isinstance(bstack11l1111lll1_opy_, list):
        bstack11l1111lll1_opy_ = []
    bstack111lll111l1_opy_ = set()
    for arg in bstack11l1111lll1_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1lll1l_opy_ (u"࠭࠽ࠨ᪽"))[0] if bstack1lll1l_opy_ (u"ࠧ࠾ࠩ᪾") in arg else arg
            bstack111lll111l1_opy_.add(flag)
    bstack11lll1l11_opy_ = 0
    for arg in bstack111lll1111l_opy_:
        flag = arg.split(bstack1lll1l_opy_ (u"ࠨ࠿ᪿࠪ"))[0] if bstack1lll1l_opy_ (u"ࠩࡀᫀࠫ") in arg else arg
        if flag not in bstack111lll111l1_opy_:
            options.add_argument(arg)
            bstack11lll1l11_opy_ += 1
    if bstack11lll1l11_opy_ > 0:
        logger.debug(bstack1lll1l_opy_ (u"ࠥ࡟ࢀࢃ࡝ࠡࡋࡱ࡮ࡪࡩࡴࡦࡦࠣࡿࢂࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡶࠤ࡫ࡵࡲࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠢ᫁").format(bstack111l11l1ll_opy_, bstack11lll1l11_opy_))
    return bstack11lll1l11_opy_