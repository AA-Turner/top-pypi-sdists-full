# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
bstack1ll1lll_opy_ (u"ࠤࠥࠦࠏࡎࡥ࡭ࡲࡨࡶࠥ࡬࡯ࡳࠢ࡬ࡲ࡯࡫ࡣࡵ࡫ࡱ࡫ࠥࡪࡥࡧࡣࡸࡰࡹࠦࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠦࡡࡳࡩࡶࠤࡼ࡮ࡥ࡯ࠢࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨ࠳ࠐࡓࡵࡴ࡬ࡧࡹࡲࡹࠡࡦࡨࡪࡪࡴࡳࡪࡸࡨ࠾ࠥࡴࡥࡷࡧࡵࠤࡴࡼࡥࡳࡹࡵ࡭ࡹ࡫ࡳࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡥࡷ࡭ࡳ࠯ࠌࡗ࡬࡮ࡹࠠࡪࡵࠣࡸ࡭࡫ࠠࡑࡻࡷ࡬ࡴࡴࠠࡦࡳࡸ࡭ࡻࡧ࡬ࡦࡰࡷࠤࡴ࡬ࠠࡋࡣࡹࡥࠬࡹࠠࡐࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬ࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࡍ࡫࡬ࡱࡧࡵ࠲ࠏࠨࠢࠣᯃ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack111l1l11lll_opy_ = [
    bstack1ll1lll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᯄ"),
    bstack1ll1lll_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡩ࡭ࡷࡹࡴ࠮ࡴࡸࡲࠬᯅ"),
    bstack1ll1lll_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡨࡪ࡬ࡡࡶ࡮ࡷ࠱ࡧࡸ࡯ࡸࡵࡨࡶ࠲ࡩࡨࡦࡥ࡮ࠫᯆ"),
    bstack1ll1lll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᯇ"),
    bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡨࡪ࡬ࡡࡶ࡮ࡷ࠱ࡦࡶࡰࡴࠩᯈ"),
    bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡬ࡶࡵࠨᯉ"),
    bstack1ll1lll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡪࡥࡷ࠯ࡶ࡬ࡲ࠳ࡵࡴࡣࡪࡩࠬᯊ"),
    bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡳࡰࡨࡷࡻࡦࡸࡥ࠮ࡴࡤࡷࡹ࡫ࡲࡪࡼࡨࡶࠬᯋ"),
    bstack1ll1lll_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡶࡥࡳࡪࡢࡰࡺࠪᯌ"),
    bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࠲ࡺࡩ࡮ࡧࡵ࠱ࡹ࡮ࡲࡰࡶࡷࡰ࡮ࡴࡧࠨᯍ"),
    bstack1ll1lll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࡯࡮ࡨ࠯ࡲࡧࡨࡲࡵࡥࡧࡧ࠱ࡼ࡯࡮ࡥࡱࡺࡷࠬᯎ"),
    bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡶࡪࡴࡤࡦࡴࡨࡶ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࡫ࡱ࡫ࠬᯏ"),
    bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡫࡫ࡡࡵࡷࡵࡩࡸࡃࡔࡳࡣࡱࡷࡱࡧࡴࡦࡗࡌࠫᯐ"),
    bstack1ll1lll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡯ࡰࡤ࠯ࡩࡰࡴࡵࡤࡪࡰࡪ࠱ࡵࡸ࡯ࡵࡧࡦࡸ࡮ࡵ࡮ࠨᯑ"),
    bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡷࡦࡤ࠰ࡷࡪࡩࡵࡳ࡫ࡷࡽࠬᯒ"),
    bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡧࡧࡤࡸࡺࡸࡥࡴ࠿࡙࡭ࡿࡊࡩࡴࡲ࡯ࡥࡾࡉ࡯࡮ࡲࡲࡷ࡮ࡺ࡯ࡳࠩᯓ"),
    bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮࡮ࡲ࡫࡬࡯࡮ࡨࠩᯔ"),
    bstack1ll1lll_opy_ (u"࠭࠭࠮ࡵ࡬ࡰࡪࡴࡴࠨᯕ")
]
def bstack11l1ll111_opy_(options, bstack11111ll1ll_opy_=bstack1ll1lll_opy_ (u"ࠢࠣᯖ")):
    bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡋࡱ࡮ࡪࡩࡴࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠌࠣࠤࠥࠦࡁࡥࡦࡶࠤ࠶࠾ࠠࡄࡪࡵࡳࡲ࡫ࠠࡢࡴࡪࡷࠥࡪࡥࡧࡧࡱࡷ࡮ࡼࡥ࡭ࡻࠣࠬࡴࡴ࡬ࡺࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷ࡫ࡳࡦࡰࡷ࠭࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠥࡵࡢ࡫ࡧࡦࡸࠥࡵࡲࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡺ࡭ࡹ࡮ࠠࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠮ࠩࠡ࡯ࡨࡸ࡭ࡵࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡺࡥࡹࡶࡢࡲࡦࡳࡥ࠻ࠢࡆࡳࡳࡺࡥࡹࡶࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠠࡧࡱࡵࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥ࠮ࡥ࠯ࡩ࠱࠰ࠥࠨࡰࡺࡶࡨࡷࡹࠨࠬࠡࠤࡳࡽࡹ࡮࡯࡯ࠤࠬࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡓࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣࡥࡩࡪࡥࡥࠌࠣࠤࠥࠦࠢࠣࠤᯗ")
    if not bstack11111ll1ll_opy_:
        bstack11111ll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠤ࡯ࡳࡦࡪ࠭ࡵࡧࡶࡸ࡮ࡴࡧࠣᯘ")
    if options is None or not hasattr(options, bstack1ll1lll_opy_ (u"ࠪࡥࡩࡪ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩᯙ")):
        logger.debug(bstack1ll1lll_opy_ (u"ࠦࡠࢁࡽ࡞ࠢࡒࡴࡹ࡯࡯࡯ࡵࠣ࡭ࡸࠦࡎࡰࡰࡨࠤࡴࡸࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡣࡧࡨࡤࡧࡲࡨࡷࡰࡩࡳࡺࠨࠪ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥ࡯࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠣᯚ").format(bstack11111ll1ll_opy_))
        return 0
    bstack111ll1ll111_opy_ = getattr(options, bstack1ll1lll_opy_ (u"ࠬࡥࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᯛ"), [])
    if not isinstance(bstack111ll1ll111_opy_, list):
        bstack111ll1ll111_opy_ = []
    bstack111l1l1l111_opy_ = set()
    for arg in bstack111ll1ll111_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1ll1lll_opy_ (u"࠭࠽ࠨᯜ"))[0] if bstack1ll1lll_opy_ (u"ࠧ࠾ࠩᯝ") in arg else arg
            bstack111l1l1l111_opy_.add(flag)
    bstack1ll1l11111_opy_ = 0
    for arg in bstack111l1l11lll_opy_:
        flag = arg.split(bstack1ll1lll_opy_ (u"ࠨ࠿ࠪᯞ"))[0] if bstack1ll1lll_opy_ (u"ࠩࡀࠫᯟ") in arg else arg
        if flag not in bstack111l1l1l111_opy_:
            options.add_argument(arg)
            bstack1ll1l11111_opy_ += 1
    if bstack1ll1l11111_opy_ > 0:
        logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟ࢀࢃ࡝ࠡࡋࡱ࡮ࡪࡩࡴࡦࡦࠣࡿࢂࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡶࠤ࡫ࡵࡲࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠢᯠ").format(bstack11111ll1ll_opy_, bstack1ll1l11111_opy_))
    return bstack1ll1l11111_opy_