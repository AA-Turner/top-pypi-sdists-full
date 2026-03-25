# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
bstack1l1_opy_ (u"ࠨࠢࠣࠌࡋࡩࡱࡶࡥࡳࠢࡩࡳࡷࠦࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡭ࡳࠡࡹ࡫ࡩࡳࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥ࠰ࠍࡗࡹࡸࡩࡤࡶ࡯ࡽࠥࡪࡥࡧࡧࡱࡷ࡮ࡼࡥ࠻ࠢࡱࡩࡻ࡫ࡲࠡࡱࡹࡩࡷࡽࡲࡪࡶࡨࡷࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡢࡴࡪࡷ࠳ࠐࡔࡩ࡫ࡶࠤ࡮ࡹࠠࡵࡪࡨࠤࡕࡿࡴࡩࡱࡱࠤࡪࡷࡵࡪࡸࡤࡰࡪࡴࡴࠡࡱࡩࠤࡏࡧࡶࡢࠩࡶࠤࡔࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࡊࡨࡰࡵ࡫ࡲ࠯ࠌ᮫ࠥࠦࠧ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack111l1l1llll_opy_ = [
    bstack1l1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᮬ"),
    bstack1l1_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡦࡪࡴࡶࡸ࠲ࡸࡵ࡯ࠩᮭ"),
    bstack1l1_opy_ (u"ࠩ࠰࠱ࡳࡵ࠭ࡥࡧࡩࡥࡺࡲࡴ࠮ࡤࡵࡳࡼࡹࡥࡳ࠯ࡦ࡬ࡪࡩ࡫ࠨᮮ"),
    bstack1l1_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᮯ"),
    bstack1l1_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡥࡧࡩࡥࡺࡲࡴ࠮ࡣࡳࡴࡸ࠭᮰"),
    bstack1l1_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡩࡳࡹࠬ᮱"),
    bstack1l1_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡧࡩࡻ࠳ࡳࡩ࡯࠰ࡹࡸࡧࡧࡦࠩ᮲"),
    bstack1l1_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡷࡴ࡬ࡴࡸࡣࡵࡩ࠲ࡸࡡࡴࡶࡨࡶ࡮ࢀࡥࡳࠩ᮳"),
    bstack1l1_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡳࡢࡰࡧࡦࡴࡾࠧ᮴"),
    bstack1l1_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࠯ࡷ࡭ࡲ࡫ࡲ࠮ࡶ࡫ࡶࡴࡺࡴ࡭࡫ࡱ࡫ࠬ᮵"),
    bstack1l1_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦ࡬ࡲ࡬࠳࡯ࡤࡥ࡯ࡹࡩ࡫ࡤ࠮ࡹ࡬ࡲࡩࡵࡷࡴࠩ᮶"),
    bstack1l1_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡳࡧࡱࡨࡪࡸࡥࡳ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࡯࡮ࡨࠩ᮷"),
    bstack1l1_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡨࡨࡥࡹࡻࡲࡦࡵࡀࡘࡷࡧ࡮ࡴ࡮ࡤࡸࡪ࡛ࡉࠨ᮸"),
    bstack1l1_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯࡬ࡴࡨ࠳ࡦ࡭ࡱࡲࡨ࡮ࡴࡧ࠮ࡲࡵࡳࡹ࡫ࡣࡵ࡫ࡲࡲࠬ᮹"),
    bstack1l1_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡻࡪࡨ࠭ࡴࡧࡦࡹࡷ࡯ࡴࡺࠩᮺ"),
    bstack1l1_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡫࡫ࡡࡵࡷࡵࡩࡸࡃࡖࡪࡼࡇ࡭ࡸࡶ࡬ࡢࡻࡆࡳࡲࡶ࡯ࡴ࡫ࡷࡳࡷ࠭ᮻ"),
    bstack1l1_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡲ࡯ࡨࡩ࡬ࡲ࡬࠭ᮼ"),
    bstack1l1_opy_ (u"ࠪ࠱࠲ࡹࡩ࡭ࡧࡱࡸࠬᮽ")
]
def bstack111l11l11_opy_(options, bstack11111111l_opy_=bstack1l1_opy_ (u"ࠦࠧᮾ")):
    bstack1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡏ࡮࡫ࡧࡦࡸࠥࡪࡥࡧࡣࡸࡰࡹࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࡩࡳࡷࠦ࡬ࡰࡣࡧࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠐࠠࠡࠢࠣࡅࡩࡪࡳࠡ࠳࠻ࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡦࡸࡧࡴࠢࡧࡩ࡫࡫࡮ࡴ࡫ࡹࡩࡱࡿࠠࠩࡱࡱࡰࡾࠦࡩࡧࠢࡱࡳࡹࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡨࡷࡪࡴࡴࠪ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠢࡲࡦ࡯࡫ࡣࡵࠢࡲࡶࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡷࡪࡶ࡫ࠤࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠫ࠭ࠥࡳࡥࡵࡪࡲࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡷࡩࡽࡺ࡟࡯ࡣࡰࡩ࠿ࠦࡃࡰࡰࡷࡩࡽࡺࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠤ࡫ࡵࡲࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢࠫࡩ࠳࡭࠮࠭ࠢࠥࡴࡾࡺࡥࡴࡶࠥ࠰ࠥࠨࡰࡺࡶ࡫ࡳࡳࠨࠩࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡐࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡢࡦࡧࡩࡩࠐࠠࠡࠢࠣࠦࠧࠨᮿ")
    if not bstack11111111l_opy_:
        bstack11111111l_opy_ = bstack1l1_opy_ (u"ࠨ࡬ࡰࡣࡧ࠱ࡹ࡫ࡳࡵ࡫ࡱ࡫ࠧᯀ")
    if options is None or not hasattr(options, bstack1l1_opy_ (u"ࠧࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭ᯁ")):
        logger.debug(bstack1l1_opy_ (u"ࠣ࡝ࡾࢁࡢࠦࡏࡱࡶ࡬ࡳࡳࡹࠠࡪࡵࠣࡒࡴࡴࡥࠡࡱࡵࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡤࡥࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠬ࠮࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢ࡬ࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠧᯂ").format(bstack11111111l_opy_))
        return 0
    bstack111lll11ll1_opy_ = getattr(options, bstack1l1_opy_ (u"ࠩࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᯃ"), [])
    if not isinstance(bstack111lll11ll1_opy_, list):
        bstack111lll11ll1_opy_ = []
    bstack111l1ll1111_opy_ = set()
    for arg in bstack111lll11ll1_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1l1_opy_ (u"ࠪࡁࠬᯄ"))[0] if bstack1l1_opy_ (u"ࠫࡂ࠭ᯅ") in arg else arg
            bstack111l1ll1111_opy_.add(flag)
    bstack1111lll11l_opy_ = 0
    for arg in bstack111l1l1llll_opy_:
        flag = arg.split(bstack1l1_opy_ (u"ࠬࡃࠧᯆ"))[0] if bstack1l1_opy_ (u"࠭࠽ࠨᯇ") in arg else arg
        if flag not in bstack111l1ll1111_opy_:
            options.add_argument(arg)
            bstack1111lll11l_opy_ += 1
    if bstack1111lll11l_opy_ > 0:
        logger.debug(bstack1l1_opy_ (u"ࠢ࡜ࡽࢀࡡࠥࡏ࡮࡫ࡧࡦࡸࡪࡪࠠࡼࡿࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡳࠡࡨࡲࡶࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠦᯈ").format(bstack11111111l_opy_, bstack1111lll11l_opy_))
    return bstack1111lll11l_opy_