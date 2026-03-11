# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
bstack1ll111_opy_ (u"ࠤࠥࠦࠏࡎࡥ࡭ࡲࡨࡶࠥ࡬࡯ࡳࠢ࡬ࡲ࡯࡫ࡣࡵ࡫ࡱ࡫ࠥࡪࡥࡧࡣࡸࡰࡹࠦࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠦࡡࡳࡩࡶࠤࡼ࡮ࡥ࡯ࠢࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨ࠳ࠐࡓࡵࡴ࡬ࡧࡹࡲࡹࠡࡦࡨࡪࡪࡴࡳࡪࡸࡨ࠾ࠥࡴࡥࡷࡧࡵࠤࡴࡼࡥࡳࡹࡵ࡭ࡹ࡫ࡳࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡥࡷ࡭ࡳ࠯ࠌࡗ࡬࡮ࡹࠠࡪࡵࠣࡸ࡭࡫ࠠࡑࡻࡷ࡬ࡴࡴࠠࡦࡳࡸ࡭ࡻࡧ࡬ࡦࡰࡷࠤࡴ࡬ࠠࡋࡣࡹࡥࠬࡹࠠࡐࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬ࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࡍ࡫࡬ࡱࡧࡵ࠲ࠏࠨࠢࠣ≯")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111l111l_opy_())
bstack1ll1lll11lll_opy_ = [
    bstack1ll111_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ≰"),
    bstack1ll111_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡩ࡭ࡷࡹࡴ࠮ࡴࡸࡲࠬ≱"),
    bstack1ll111_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡨࡪ࡬ࡡࡶ࡮ࡷ࠱ࡧࡸ࡯ࡸࡵࡨࡶ࠲ࡩࡨࡦࡥ࡮ࠫ≲"),
    bstack1ll111_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭≳"),
    bstack1ll111_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡨࡪ࡬ࡡࡶ࡮ࡷ࠱ࡦࡶࡰࡴࠩ≴"),
    bstack1ll111_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡬ࡶࡵࠨ≵"),
    bstack1ll111_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡪࡥࡷ࠯ࡶ࡬ࡲ࠳ࡵࡴࡣࡪࡩࠬ≶"),
    bstack1ll111_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡳࡰࡨࡷࡻࡦࡸࡥ࠮ࡴࡤࡷࡹ࡫ࡲࡪࡼࡨࡶࠬ≷"),
    bstack1ll111_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡶࡥࡳࡪࡢࡰࡺࠪ≸"),
    bstack1ll111_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࠲ࡺࡩ࡮ࡧࡵ࠱ࡹ࡮ࡲࡰࡶࡷࡰ࡮ࡴࡧࠨ≹"),
    bstack1ll111_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࡯࡮ࡨ࠯ࡲࡧࡨࡲࡵࡥࡧࡧ࠱ࡼ࡯࡮ࡥࡱࡺࡷࠬ≺"),
    bstack1ll111_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡶࡪࡴࡤࡦࡴࡨࡶ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࡫ࡱ࡫ࠬ≻"),
    bstack1ll111_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡫࡫ࡡࡵࡷࡵࡩࡸࡃࡔࡳࡣࡱࡷࡱࡧࡴࡦࡗࡌࠫ≼"),
    bstack1ll111_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡯ࡰࡤ࠯ࡩࡰࡴࡵࡤࡪࡰࡪ࠱ࡵࡸ࡯ࡵࡧࡦࡸ࡮ࡵ࡮ࠨ≽"),
    bstack1ll111_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡷࡦࡤ࠰ࡷࡪࡩࡵࡳ࡫ࡷࡽࠬ≾"),
    bstack1ll111_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡧࡧࡤࡸࡺࡸࡥࡴ࠿࡙࡭ࡿࡊࡩࡴࡲ࡯ࡥࡾࡉ࡯࡮ࡲࡲࡷ࡮ࡺ࡯ࡳࠩ≿"),
    bstack1ll111_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮࡮ࡲ࡫࡬࡯࡮ࡨࠩ⊀"),
    bstack1ll111_opy_ (u"࠭࠭࠮ࡵ࡬ࡰࡪࡴࡴࠨ⊁")
]
def bstack11l1ll1l_opy_(options, bstack1l11l111l_opy_=bstack1ll111_opy_ (u"ࠢࠣ⊂")):
    bstack1ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡋࡱ࡮ࡪࡩࡴࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠌࠣࠤࠥࠦࡁࡥࡦࡶࠤ࠶࠾ࠠࡄࡪࡵࡳࡲ࡫ࠠࡢࡴࡪࡷࠥࡪࡥࡧࡧࡱࡷ࡮ࡼࡥ࡭ࡻࠣࠬࡴࡴ࡬ࡺࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷ࡫ࡳࡦࡰࡷ࠭࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠥࡵࡢ࡫ࡧࡦࡸࠥࡵࡲࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡺ࡭ࡹ࡮ࠠࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠮ࠩࠡ࡯ࡨࡸ࡭ࡵࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡺࡥࡹࡶࡢࡲࡦࡳࡥ࠻ࠢࡆࡳࡳࡺࡥࡹࡶࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࡧࡱࡵࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥ࠮ࡥ࠯ࡩ࠱࠰ࠥࠨࡰࡺࡶࡨࡷࡹࠨࠬࠡࠤࡳࡽࡹ࡮࡯࡯ࠤࠬࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡓࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣࡥࡩࡪࡥࡥࠌࠣࠤࠥࠦࠢࠣࠤ⊃")
    if not bstack1l11l111l_opy_:
        bstack1l11l111l_opy_ = bstack1ll111_opy_ (u"ࠤ࡯ࡳࡦࡪ࠭ࡵࡧࡶࡸ࡮ࡴࡧࠣ⊄")
    if options is None or not hasattr(options, bstack1ll111_opy_ (u"ࠪࡥࡩࡪ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩ⊅")):
        logger.debug(bstack1ll111_opy_ (u"ࠦࡠࢁࡽ࡞ࠢࡒࡴࡹ࡯࡯࡯ࡵࠣ࡭ࡸࠦࡎࡰࡰࡨࠤࡴࡸࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡣࡧࡨࡤࡧࡲࡨࡷࡰࡩࡳࡺࠨࠪ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥ࡯࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠣ⊆").format(bstack1l11l111l_opy_))
        return 0
    bstack1ll1llllll11_opy_ = getattr(options, bstack1ll111_opy_ (u"ࠬࡥࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⊇"), [])
    if not isinstance(bstack1ll1llllll11_opy_, list):
        bstack1ll1llllll11_opy_ = []
    bstack1ll1lll11ll1_opy_ = set()
    for arg in bstack1ll1llllll11_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1ll111_opy_ (u"࠭࠽ࠨ⊈"))[0] if bstack1ll111_opy_ (u"ࠧ࠾ࠩ⊉") in arg else arg
            bstack1ll1lll11ll1_opy_.add(flag)
    bstack111lll1l1_opy_ = 0
    for arg in bstack1ll1lll11lll_opy_:
        flag = arg.split(bstack1ll111_opy_ (u"ࠨ࠿ࠪ⊊"))[0] if bstack1ll111_opy_ (u"ࠩࡀࠫ⊋") in arg else arg
        if flag not in bstack1ll1lll11ll1_opy_:
            options.add_argument(arg)
            bstack111lll1l1_opy_ += 1
    if bstack111lll1l1_opy_ > 0:
        logger.debug(bstack1ll111_opy_ (u"ࠥ࡟ࢀࢃ࡝ࠡࡋࡱ࡮ࡪࡩࡴࡦࡦࠣࡿࢂࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡶࠤ࡫ࡵࡲࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠢ⊌").format(bstack1l11l111l_opy_, bstack111lll1l1_opy_))
    return bstack111lll1l1_opy_