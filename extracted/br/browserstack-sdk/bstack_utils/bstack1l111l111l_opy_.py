# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
bstack11lll1_opy_ (u"ࠧࠨࠢࠋࡊࡨࡰࡵ࡫ࡲࠡࡨࡲࡶࠥ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶ࡬ࡹࠠࡸࡪࡨࡲࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤ࠯ࠌࡖࡸࡷ࡯ࡣࡵ࡮ࡼࠤࡩ࡫ࡦࡦࡰࡶ࡭ࡻ࡫࠺ࠡࡰࡨࡺࡪࡸࠠࡰࡸࡨࡶࡼࡸࡩࡵࡧࡶࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡡࡳࡩࡶ࠲ࠏ࡚ࡨࡪࡵࠣ࡭ࡸࠦࡴࡩࡧࠣࡔࡾࡺࡨࡰࡰࠣࡩࡶࡻࡩࡷࡣ࡯ࡩࡳࡺࠠࡰࡨࠣࡎࡦࡼࡡࠨࡵࠣࡓࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࡉࡧ࡯ࡴࡪࡸ࠮ࠋࠤࠥࠦᮣ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack111l1ll11ll_opy_ = [
    bstack11lll1_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᮤ"),
    bstack11lll1_opy_ (u"ࠧ࠮࠯ࡱࡳ࠲࡬ࡩࡳࡵࡷ࠱ࡷࡻ࡮ࠨᮥ"),
    bstack11lll1_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡤࡦࡨࡤࡹࡱࡺ࠭ࡣࡴࡲࡻࡸ࡫ࡲ࠮ࡥ࡫ࡩࡨࡱࠧᮦ"),
    bstack11lll1_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᮧ"),
    bstack11lll1_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡤࡦࡨࡤࡹࡱࡺ࠭ࡢࡲࡳࡷࠬᮨ"),
    bstack11lll1_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡨࡲࡸࠫᮩ"),
    bstack11lll1_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡦࡨࡺ࠲ࡹࡨ࡮࠯ࡸࡷࡦ࡭ࡥࠨ᮪"),
    bstack11lll1_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡶࡳ࡫ࡺࡷࡢࡴࡨ࠱ࡷࡧࡳࡵࡧࡵ࡭ࡿ࡫ࡲࠨ᮫"),
    bstack11lll1_opy_ (u"ࠧ࠮࠯ࡱࡳ࠲ࡹࡡ࡯ࡦࡥࡳࡽ࠭ᮬ"),
    bstack11lll1_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡧࡧࡣ࡬ࡩࡵࡳࡺࡴࡤ࠮ࡶ࡬ࡱࡪࡸ࠭ࡵࡪࡵࡳࡹࡺ࡬ࡪࡰࡪࠫᮭ"),
    bstack11lll1_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࡫ࡱ࡫࠲ࡵࡣࡤ࡮ࡸࡨࡪࡪ࠭ࡸ࡫ࡱࡨࡴࡽࡳࠨᮮ"),
    bstack11lll1_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡲࡦࡰࡧࡩࡷ࡫ࡲ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࡮ࡴࡧࠨᮯ"),
    bstack11lll1_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡧࡧࡤࡸࡺࡸࡥࡴ࠿ࡗࡶࡦࡴࡳ࡭ࡣࡷࡩ࡚ࡏࠧ᮰"),
    bstack11lll1_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮࡫ࡳࡧ࠲࡬࡬ࡰࡱࡧ࡭ࡳ࡭࠭ࡱࡴࡲࡸࡪࡩࡴࡪࡱࡱࠫ᮱"),
    bstack11lll1_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡺࡩࡧ࠳ࡳࡦࡥࡸࡶ࡮ࡺࡹࠨ᮲"),
    bstack11lll1_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡪࡪࡧࡴࡶࡴࡨࡷࡂ࡜ࡩࡻࡆ࡬ࡷࡵࡲࡡࡺࡅࡲࡱࡵࡵࡳࡪࡶࡲࡶࠬ᮳"),
    bstack11lll1_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡱࡵࡧࡨ࡫ࡱ࡫ࠬ᮴"),
    bstack11lll1_opy_ (u"ࠩ࠰࠱ࡸ࡯࡬ࡦࡰࡷࠫ᮵")
]
def bstack1l1l1l1ll1_opy_(options, bstack1l1ll1l11l_opy_=bstack11lll1_opy_ (u"ࠥࠦ᮶")):
    bstack11lll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡎࡴࡪࡦࡥࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡࡨࡲࡶࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠏࠦࠠࠡࠢࡄࡨࡩࡹࠠ࠲࠺ࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡳࠡࡦࡨࡪࡪࡴࡳࡪࡸࡨࡰࡾࠦࠨࡰࡰ࡯ࡽࠥ࡯ࡦࠡࡰࡲࡸࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡧࡶࡩࡳࡺࠩ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠡࡱࡥ࡮ࡪࡩࡴࠡࡱࡵࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡽࡩࡵࡪࠣࡥࡩࡪ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠪࠬࠤࡲ࡫ࡴࡩࡱࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡶࡨࡼࡹࡥ࡮ࡢ࡯ࡨ࠾ࠥࡉ࡯࡯ࡶࡨࡼࡹࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡࠪࡨ࠲࡬࠴ࠬࠡࠤࡳࡽࡹ࡫ࡳࡵࠤ࠯ࠤࠧࡶࡹࡵࡪࡲࡲࠧ࠯ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡏࡷࡰࡦࡪࡸࠠࡰࡨࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡡࡥࡦࡨࡨࠏࠦࠠࠡࠢࠥࠦࠧ᮷")
    if not bstack1l1ll1l11l_opy_:
        bstack1l1ll1l11l_opy_ = bstack11lll1_opy_ (u"ࠧࡲ࡯ࡢࡦ࠰ࡸࡪࡹࡴࡪࡰࡪࠦ᮸")
    if options is None or not hasattr(options, bstack11lll1_opy_ (u"࠭ࡡࡥࡦࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ᮹")):
        logger.debug(bstack11lll1_opy_ (u"ࠢ࡜ࡽࢀࡡࠥࡕࡰࡵ࡫ࡲࡲࡸࠦࡩࡴࠢࡑࡳࡳ࡫ࠠࡰࡴࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠫ࠭࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡ࡫ࡱ࡮ࡪࡩࡴࡪࡱࡱࠦᮺ").format(bstack1l1ll1l11l_opy_))
        return 0
    bstack111lll11lll_opy_ = getattr(options, bstack11lll1_opy_ (u"ࠨࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᮻ"), [])
    if not isinstance(bstack111lll11lll_opy_, list):
        bstack111lll11lll_opy_ = []
    bstack111l1ll1l11_opy_ = set()
    for arg in bstack111lll11lll_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack11lll1_opy_ (u"ࠩࡀࠫᮼ"))[0] if bstack11lll1_opy_ (u"ࠪࡁࠬᮽ") in arg else arg
            bstack111l1ll1l11_opy_.add(flag)
    bstack11l1ll11l1_opy_ = 0
    for arg in bstack111l1ll11ll_opy_:
        flag = arg.split(bstack11lll1_opy_ (u"ࠫࡂ࠭ᮾ"))[0] if bstack11lll1_opy_ (u"ࠬࡃࠧᮿ") in arg else arg
        if flag not in bstack111l1ll1l11_opy_:
            options.add_argument(arg)
            bstack11l1ll11l1_opy_ += 1
    if bstack11l1ll11l1_opy_ > 0:
        logger.debug(bstack11lll1_opy_ (u"ࠨ࡛ࡼࡿࡠࠤࡎࡴࡪࡦࡥࡷࡩࡩࠦࡻࡾࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡤࡶ࡬ࡹࠠࡧࡱࡵࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠥᯀ").format(bstack1l1ll1l11l_opy_, bstack11l1ll11l1_opy_))
    return bstack11l1ll11l1_opy_