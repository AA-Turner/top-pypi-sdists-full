# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
bstack1ll11_opy_ (u"ࠧࠨࠢࠋࡊࡨࡰࡵ࡫ࡲࠡࡨࡲࡶࠥ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶ࡬ࡹࠠࡸࡪࡨࡲࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤ࠯ࠌࡖࡸࡷ࡯ࡣࡵ࡮ࡼࠤࡩ࡫ࡦࡦࡰࡶ࡭ࡻ࡫࠺ࠡࡰࡨࡺࡪࡸࠠࡰࡸࡨࡶࡼࡸࡩࡵࡧࡶࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡡࡳࡩࡶ࠲ࠏ࡚ࡨࡪࡵࠣ࡭ࡸࠦࡴࡩࡧࠣࡔࡾࡺࡨࡰࡰࠣࡩࡶࡻࡩࡷࡣ࡯ࡩࡳࡺࠠࡰࡨࠣࡎࡦࡼࡡࠨࡵࠣࡓࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࡉࡧ࡯ࡴࡪࡸ࠮ࠋࠤࠥࠦᯔ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack111l1l11l1l_opy_ = [
    bstack1ll11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᯕ"),
    bstack1ll11_opy_ (u"ࠧ࠮࠯ࡱࡳ࠲࡬ࡩࡳࡵࡷ࠱ࡷࡻ࡮ࠨᯖ"),
    bstack1ll11_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡤࡦࡨࡤࡹࡱࡺ࠭ࡣࡴࡲࡻࡸ࡫ࡲ࠮ࡥ࡫ࡩࡨࡱࠧᯗ"),
    bstack1ll11_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᯘ"),
    bstack1ll11_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡤࡦࡨࡤࡹࡱࡺ࠭ࡢࡲࡳࡷࠬᯙ"),
    bstack1ll11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡨࡲࡸࠫᯚ"),
    bstack1ll11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡦࡨࡺ࠲ࡹࡨ࡮࠯ࡸࡷࡦ࡭ࡥࠨᯛ"),
    bstack1ll11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡶࡳ࡫ࡺࡷࡢࡴࡨ࠱ࡷࡧࡳࡵࡧࡵ࡭ࡿ࡫ࡲࠨᯜ"),
    bstack1ll11_opy_ (u"ࠧ࠮࠯ࡱࡳ࠲ࡹࡡ࡯ࡦࡥࡳࡽ࠭ᯝ"),
    bstack1ll11_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡧࡧࡣ࡬ࡩࡵࡳࡺࡴࡤ࠮ࡶ࡬ࡱࡪࡸ࠭ࡵࡪࡵࡳࡹࡺ࡬ࡪࡰࡪࠫᯞ"),
    bstack1ll11_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࡫ࡱ࡫࠲ࡵࡣࡤ࡮ࡸࡨࡪࡪ࠭ࡸ࡫ࡱࡨࡴࡽࡳࠨᯟ"),
    bstack1ll11_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡲࡦࡰࡧࡩࡷ࡫ࡲ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࡮ࡴࡧࠨᯠ"),
    bstack1ll11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡧࡧࡤࡸࡺࡸࡥࡴ࠿ࡗࡶࡦࡴࡳ࡭ࡣࡷࡩ࡚ࡏࠧᯡ"),
    bstack1ll11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮࡫ࡳࡧ࠲࡬࡬ࡰࡱࡧ࡭ࡳ࡭࠭ࡱࡴࡲࡸࡪࡩࡴࡪࡱࡱࠫᯢ"),
    bstack1ll11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡺࡩࡧ࠳ࡳࡦࡥࡸࡶ࡮ࡺࡹࠨᯣ"),
    bstack1ll11_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡪࡪࡧࡴࡶࡴࡨࡷࡂ࡜ࡩࡻࡆ࡬ࡷࡵࡲࡡࡺࡅࡲࡱࡵࡵࡳࡪࡶࡲࡶࠬᯤ"),
    bstack1ll11_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡱࡵࡧࡨ࡫ࡱ࡫ࠬᯥ"),
    bstack1ll11_opy_ (u"ࠩ࠰࠱ࡸ࡯࡬ࡦࡰࡷ᯦ࠫ")
]
def bstack1lll11l11l_opy_(options, bstack1l1l11111l_opy_=bstack1ll11_opy_ (u"ࠥࠦᯧ")):
    bstack1ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡎࡴࡪࡦࡥࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡࡨࡲࡶࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠏࠦࠠࠡࠢࡄࡨࡩࡹࠠ࠲࠺ࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡳࠡࡦࡨࡪࡪࡴࡳࡪࡸࡨࡰࡾࠦࠨࡰࡰ࡯ࡽࠥ࡯ࡦࠡࡰࡲࡸࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡧࡶࡩࡳࡺࠩ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠡࡱࡥ࡮ࡪࡩࡴࠡࡱࡵࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡽࡩࡵࡪࠣࡥࡩࡪ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠪࠬࠤࡲ࡫ࡴࡩࡱࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡶࡨࡼࡹࡥ࡮ࡢ࡯ࡨ࠾ࠥࡉ࡯࡯ࡶࡨࡼࡹࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡࠪࡨ࠲࡬࠴ࠬࠡࠤࡳࡽࡹ࡫ࡳࡵࠤ࠯ࠤࠧࡶࡹࡵࡪࡲࡲࠧ࠯ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡏࡷࡰࡦࡪࡸࠠࡰࡨࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡡࡥࡦࡨࡨࠏࠦࠠࠡࠢࠥࠦࠧᯨ")
    if not bstack1l1l11111l_opy_:
        bstack1l1l11111l_opy_ = bstack1ll11_opy_ (u"ࠧࡲ࡯ࡢࡦ࠰ࡸࡪࡹࡴࡪࡰࡪࠦᯩ")
    if options is None or not hasattr(options, bstack1ll11_opy_ (u"࠭ࡡࡥࡦࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬᯪ")):
        logger.debug(bstack1ll11_opy_ (u"ࠢ࡜ࡽࢀࡡࠥࡕࡰࡵ࡫ࡲࡲࡸࠦࡩࡴࠢࡑࡳࡳ࡫ࠠࡰࡴࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠫ࠭࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡ࡫ࡱ࡮ࡪࡩࡴࡪࡱࡱࠦᯫ").format(bstack1l1l11111l_opy_))
        return 0
    bstack111ll11ll11_opy_ = getattr(options, bstack1ll11_opy_ (u"ࠨࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᯬ"), [])
    if not isinstance(bstack111ll11ll11_opy_, list):
        bstack111ll11ll11_opy_ = []
    bstack111l1l11ll1_opy_ = set()
    for arg in bstack111ll11ll11_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1ll11_opy_ (u"ࠩࡀࠫᯭ"))[0] if bstack1ll11_opy_ (u"ࠪࡁࠬᯮ") in arg else arg
            bstack111l1l11ll1_opy_.add(flag)
    bstack1llll11l_opy_ = 0
    for arg in bstack111l1l11l1l_opy_:
        flag = arg.split(bstack1ll11_opy_ (u"ࠫࡂ࠭ᯯ"))[0] if bstack1ll11_opy_ (u"ࠬࡃࠧᯰ") in arg else arg
        if flag not in bstack111l1l11ll1_opy_:
            options.add_argument(arg)
            bstack1llll11l_opy_ += 1
    if bstack1llll11l_opy_ > 0:
        logger.debug(bstack1ll11_opy_ (u"ࠨ࡛ࡼࡿࡠࠤࡎࡴࡪࡦࡥࡷࡩࡩࠦࡻࡾࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡤࡶ࡬ࡹࠠࡧࡱࡵࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠥᯱ").format(bstack1l1l11111l_opy_, bstack1llll11l_opy_))
    return bstack1llll11l_opy_