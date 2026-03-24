# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࡍ࡫࡬ࡱࡧࡵࠤ࡫ࡵࡲࠡ࡫ࡱ࡮ࡪࡩࡴࡪࡰࡪࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠥࡧࡲࡨࡵࠣࡻ࡭࡫࡮ࠡࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡩࡳࡧࡢ࡭ࡧࡧ࠲ࠏ࡙ࡴࡳ࡫ࡦࡸࡱࡿࠠࡥࡧࡩࡩࡳࡹࡩࡷࡧ࠽ࠤࡳ࡫ࡶࡦࡴࠣࡳࡻ࡫ࡲࡸࡴ࡬ࡸࡪࡹࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡤࡶ࡬ࡹ࠮ࠋࡖ࡫࡭ࡸࠦࡩࡴࠢࡷ࡬ࡪࠦࡐࡺࡶ࡫ࡳࡳࠦࡥࡲࡷ࡬ࡺࡦࡲࡥ࡯ࡶࠣࡳ࡫ࠦࡊࡢࡸࡤࠫࡸࠦࡏࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࡌࡪࡲࡰࡦࡴ࠱ࠎࠧࠨࠢᮦ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack111l1ll1111_opy_ = [
    bstack1ll1lll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᮧ"),
    bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡴ࡯࠮ࡨ࡬ࡶࡸࡺ࠭ࡳࡷࡱࠫᮨ"),
    bstack1ll1lll_opy_ (u"ࠫ࠲࠳࡮ࡰ࠯ࡧࡩ࡫ࡧࡵ࡭ࡶ࠰ࡦࡷࡵࡷࡴࡧࡵ࠱ࡨ࡮ࡥࡤ࡭ࠪᮩ"),
    bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷ᮪ࠬ"),
    bstack1ll1lll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡧࡩ࡫ࡧࡵ࡭ࡶ࠰ࡥࡵࡶࡳࠨ᮫"),
    bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰࡫ࡵࡻࠧᮬ"),
    bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡩ࡫ࡶ࠮ࡵ࡫ࡱ࠲ࡻࡳࡢࡩࡨࠫᮭ"),
    bstack1ll1lll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡹ࡯ࡧࡶࡺࡥࡷ࡫࠭ࡳࡣࡶࡸࡪࡸࡩࡻࡧࡵࠫᮮ"),
    bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡴ࡯࠮ࡵࡤࡲࡩࡨ࡯ࡹࠩᮯ"),
    bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡣࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧ࠱ࡹ࡯࡭ࡦࡴ࠰ࡸ࡭ࡸ࡯ࡵࡶ࡯࡭ࡳ࡭ࠧ᮰"),
    bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࡮ࡴࡧ࠮ࡱࡦࡧࡱࡻࡤࡦࡦ࠰ࡻ࡮ࡴࡤࡰࡹࡶࠫ᮱"),
    bstack1ll1lll_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡵࡩࡳࡪࡥࡳࡧࡵ࠱ࡧࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࡪࡰࡪࠫ᮲"),
    bstack1ll1lll_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡪࡪࡧࡴࡶࡴࡨࡷࡂ࡚ࡲࡢࡰࡶࡰࡦࡺࡥࡖࡋࠪ᮳"),
    bstack1ll1lll_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱࡮ࡶࡣ࠮ࡨ࡯ࡳࡴࡪࡩ࡯ࡩ࠰ࡴࡷࡵࡴࡦࡥࡷ࡭ࡴࡴࠧ᮴"),
    bstack1ll1lll_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡽࡥࡣ࠯ࡶࡩࡨࡻࡲࡪࡶࡼࠫ᮵"),
    bstack1ll1lll_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡦࡦࡣࡷࡹࡷ࡫ࡳ࠾ࡘ࡬ࡾࡉ࡯ࡳࡱ࡮ࡤࡽࡈࡵ࡭ࡱࡱࡶ࡭ࡹࡵࡲࠨ᮶"),
    bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭࡭ࡱࡪ࡫࡮ࡴࡧࠨ᮷"),
    bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡴ࡫࡯ࡩࡳࡺࠧ᮸")
]
def bstack1l1ll1111l_opy_(options, bstack111ll1lll_opy_=bstack1ll1lll_opy_ (u"ࠨࠢ᮹")):
    bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡊࡰ࡭ࡩࡨࡺࠠࡥࡧࡩࡥࡺࡲࡴࠡࡅ࡫ࡶࡴࡳࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡫ࡵࡲࠡ࡮ࡲࡥࡩࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠋࠢࠣࠤࠥࡇࡤࡥࡵࠣ࠵࠽ࠦࡃࡩࡴࡲࡱࡪࠦࡡࡳࡩࡶࠤࡩ࡫ࡦࡦࡰࡶ࡭ࡻ࡫࡬ࡺࠢࠫࡳࡳࡲࡹࠡ࡫ࡩࠤࡳࡵࡴࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡪࡹࡥ࡯ࡶࠬ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠤࡴࡨࡪࡦࡥࡷࠤࡴࡸࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡹ࡬ࡸ࡭ࠦࡡࡥࡦࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠭࠯ࠠ࡮ࡧࡷ࡬ࡴࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡹ࡫ࡸࡵࡡࡱࡥࡲ࡫࠺ࠡࡅࡲࡲࡹ࡫ࡸࡵࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠦࡦࡰࡴࠣࡰࡴ࡭ࡧࡪࡰࡪࠤ࠭࡫࠮ࡨ࠰࠯ࠤࠧࡶࡹࡵࡧࡶࡸࠧ࠲ࠠࠣࡲࡼࡸ࡭ࡵ࡮ࠣࠫࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡒࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࡤࡨࡩ࡫ࡤࠋࠢࠣࠤࠥࠨࠢࠣᮺ")
    if not bstack111ll1lll_opy_:
        bstack111ll1lll_opy_ = bstack1ll1lll_opy_ (u"ࠣ࡮ࡲࡥࡩ࠳ࡴࡦࡵࡷ࡭ࡳ࡭ࠢᮻ")
    if options is None or not hasattr(options, bstack1ll1lll_opy_ (u"ࠩࡤࡨࡩࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨᮼ")):
        logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟ࢀࢃ࡝ࠡࡑࡳࡸ࡮ࡵ࡮ࡴࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠣࡳࡷࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡦࡧࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠮ࠩ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤ࡮ࡴࡪࡦࡥࡷ࡭ࡴࡴࠢᮽ").format(bstack111ll1lll_opy_))
        return 0
    bstack111lll1lll1_opy_ = getattr(options, bstack1ll1lll_opy_ (u"ࠫࡤࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᮾ"), [])
    if not isinstance(bstack111lll1lll1_opy_, list):
        bstack111lll1lll1_opy_ = []
    bstack111l1ll111l_opy_ = set()
    for arg in bstack111lll1lll1_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1ll1lll_opy_ (u"ࠬࡃࠧᮿ"))[0] if bstack1ll1lll_opy_ (u"࠭࠽ࠨᯀ") in arg else arg
            bstack111l1ll111l_opy_.add(flag)
    bstack1l11l1lll_opy_ = 0
    for arg in bstack111l1ll1111_opy_:
        flag = arg.split(bstack1ll1lll_opy_ (u"ࠧ࠾ࠩᯁ"))[0] if bstack1ll1lll_opy_ (u"ࠨ࠿ࠪᯂ") in arg else arg
        if flag not in bstack111l1ll111l_opy_:
            options.add_argument(arg)
            bstack1l11l1lll_opy_ += 1
    if bstack1l11l1lll_opy_ > 0:
        logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡞ࡿࢂࡣࠠࡊࡰ࡭ࡩࡨࡺࡥࡥࠢࡾࢁࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡵࠣࡪࡴࡸࠠ࡭ࡱࡤࡨࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠨᯃ").format(bstack111ll1lll_opy_, bstack1l11l1lll_opy_))
    return bstack1l11l1lll_opy_