# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
bstack11ll111_opy_ (u"ࠧࠨࠢࠋࡊࡨࡰࡵ࡫ࡲࠡࡨࡲࡶࠥ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶ࡬ࡹࠠࡸࡪࡨࡲࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤ࠯ࠌࡖࡸࡷ࡯ࡣࡵ࡮ࡼࠤࡩ࡫ࡦࡦࡰࡶ࡭ࡻ࡫࠺ࠡࡰࡨࡺࡪࡸࠠࡰࡸࡨࡶࡼࡸࡩࡵࡧࡶࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡡࡳࡩࡶ࠲ࠏ࡚ࡨࡪࡵࠣ࡭ࡸࠦࡴࡩࡧࠣࡔࡾࡺࡨࡰࡰࠣࡩࡶࡻࡩࡷࡣ࡯ࡩࡳࡺࠠࡰࡨࠣࡎࡦࡼࡡࠨࡵࠣࡓࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࡉࡧ࡯ࡴࡪࡸ࠮ࠋࠤࠥࠦ᥺")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1l11ll1l_opy_())
bstack11l11111111_opy_ = [
    bstack11ll111_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪ᥻"),
    bstack11ll111_opy_ (u"ࠧ࠮࠯ࡱࡳ࠲࡬ࡩࡳࡵࡷ࠱ࡷࡻ࡮ࠨ᥼"),
    bstack11ll111_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡤࡦࡨࡤࡹࡱࡺ࠭ࡣࡴࡲࡻࡸ࡫ࡲ࠮ࡥ࡫ࡩࡨࡱࠧ᥽"),
    bstack11ll111_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᥾"),
    bstack11ll111_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡤࡦࡨࡤࡹࡱࡺ࠭ࡢࡲࡳࡷࠬ᥿"),
    bstack11ll111_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡨࡲࡸࠫᦀ"),
    bstack11ll111_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡦࡨࡺ࠲ࡹࡨ࡮࠯ࡸࡷࡦ࡭ࡥࠨᦁ"),
    bstack11ll111_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡶࡳ࡫ࡺࡷࡢࡴࡨ࠱ࡷࡧࡳࡵࡧࡵ࡭ࡿ࡫ࡲࠨᦂ"),
    bstack11ll111_opy_ (u"ࠧ࠮࠯ࡱࡳ࠲ࡹࡡ࡯ࡦࡥࡳࡽ࠭ᦃ"),
    bstack11ll111_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡧࡧࡣ࡬ࡩࡵࡳࡺࡴࡤ࠮ࡶ࡬ࡱࡪࡸ࠭ࡵࡪࡵࡳࡹࡺ࡬ࡪࡰࡪࠫᦄ"),
    bstack11ll111_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࡫ࡱ࡫࠲ࡵࡣࡤ࡮ࡸࡨࡪࡪ࠭ࡸ࡫ࡱࡨࡴࡽࡳࠨᦅ"),
    bstack11ll111_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡲࡦࡰࡧࡩࡷ࡫ࡲ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࡮ࡴࡧࠨᦆ"),
    bstack11ll111_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡧࡧࡤࡸࡺࡸࡥࡴ࠿ࡗࡶࡦࡴࡳ࡭ࡣࡷࡩ࡚ࡏࠧᦇ"),
    bstack11ll111_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮࡫ࡳࡧ࠲࡬࡬ࡰࡱࡧ࡭ࡳ࡭࠭ࡱࡴࡲࡸࡪࡩࡴࡪࡱࡱࠫᦈ"),
    bstack11ll111_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡺࡩࡧ࠳ࡳࡦࡥࡸࡶ࡮ࡺࡹࠨᦉ"),
    bstack11ll111_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡪࡪࡧࡴࡶࡴࡨࡷࡂ࡜ࡩࡻࡆ࡬ࡷࡵࡲࡡࡺࡅࡲࡱࡵࡵࡳࡪࡶࡲࡶࠬᦊ"),
    bstack11ll111_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡱࡵࡧࡨ࡫ࡱ࡫ࠬᦋ"),
    bstack11ll111_opy_ (u"ࠩ࠰࠱ࡸ࡯࡬ࡦࡰࡷࠫᦌ")
]
def bstack111l1ll1l_opy_(options, bstack11l1ll1l1_opy_=bstack11ll111_opy_ (u"ࠥࠦᦍ")):
    bstack11ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡎࡴࡪࡦࡥࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡࡨࡲࡶࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠏࠦࠠࠡࠢࡄࡨࡩࡹࠠ࠲࠺ࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡳࠡࡦࡨࡪࡪࡴࡳࡪࡸࡨࡰࡾࠦࠨࡰࡰ࡯ࡽࠥ࡯ࡦࠡࡰࡲࡸࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡧࡶࡩࡳࡺࠩ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠡࡱࡥ࡮ࡪࡩࡴࠡࡱࡵࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡽࡩࡵࡪࠣࡥࡩࡪ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠪࠬࠤࡲ࡫ࡴࡩࡱࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡶࡨࡼࡹࡥ࡮ࡢ࡯ࡨ࠾ࠥࡉ࡯࡯ࡶࡨࡼࡹࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡࠪࡨ࠲࡬࠴ࠬࠡࠤࡳࡽࡹ࡫ࡳࡵࠤ࠯ࠤࠧࡶࡹࡵࡪࡲࡲࠧ࠯ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡏࡷࡰࡦࡪࡸࠠࡰࡨࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡡࡥࡦࡨࡨࠏࠦࠠࠡࠢࠥࠦࠧᦎ")
    if not bstack11l1ll1l1_opy_:
        bstack11l1ll1l1_opy_ = bstack11ll111_opy_ (u"ࠧࡲ࡯ࡢࡦ࠰ࡸࡪࡹࡴࡪࡰࡪࠦᦏ")
    if options is None or not hasattr(options, bstack11ll111_opy_ (u"࠭ࡡࡥࡦࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬᦐ")):
        logger.debug(bstack11ll111_opy_ (u"ࠢ࡜ࡽࢀࡡࠥࡕࡰࡵ࡫ࡲࡲࡸࠦࡩࡴࠢࡑࡳࡳ࡫ࠠࡰࡴࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠫ࠭࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡ࡫ࡱ࡮ࡪࡩࡴࡪࡱࡱࠦᦑ").format(bstack11l1ll1l1_opy_))
        return 0
    bstack11l111lll1l_opy_ = getattr(options, bstack11ll111_opy_ (u"ࠨࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᦒ"), [])
    if not isinstance(bstack11l111lll1l_opy_, list):
        bstack11l111lll1l_opy_ = []
    bstack11l1111111l_opy_ = set()
    for arg in bstack11l111lll1l_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack11ll111_opy_ (u"ࠩࡀࠫᦓ"))[0] if bstack11ll111_opy_ (u"ࠪࡁࠬᦔ") in arg else arg
            bstack11l1111111l_opy_.add(flag)
    bstack1l1ll1l1l1_opy_ = 0
    for arg in bstack11l11111111_opy_:
        flag = arg.split(bstack11ll111_opy_ (u"ࠫࡂ࠭ᦕ"))[0] if bstack11ll111_opy_ (u"ࠬࡃࠧᦖ") in arg else arg
        if flag not in bstack11l1111111l_opy_:
            options.add_argument(arg)
            bstack1l1ll1l1l1_opy_ += 1
    if bstack1l1ll1l1l1_opy_ > 0:
        logger.debug(bstack11ll111_opy_ (u"ࠨ࡛ࡼࡿࡠࠤࡎࡴࡪࡦࡥࡷࡩࡩࠦࡻࡾࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡤࡶ࡬ࡹࠠࡧࡱࡵࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠥᦗ").format(bstack11l1ll1l1_opy_, bstack1l1ll1l1l1_opy_))
    return bstack1l1ll1l1l1_opy_