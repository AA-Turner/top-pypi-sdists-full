# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
bstack11l11_opy_ (u"ࠧࠨࠢࠋࡊࡨࡰࡵ࡫ࡲࠡࡨࡲࡶࠥ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶ࡬ࡹࠠࡸࡪࡨࡲࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤ࠯ࠌࡖࡸࡷ࡯ࡣࡵ࡮ࡼࠤࡩ࡫ࡦࡦࡰࡶ࡭ࡻ࡫࠺ࠡࡰࡨࡺࡪࡸࠠࡰࡸࡨࡶࡼࡸࡩࡵࡧࡶࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡡࡳࡩࡶ࠲ࠏ࡚ࡨࡪࡵࠣ࡭ࡸࠦࡴࡩࡧࠣࡔࡾࡺࡨࡰࡰࠣࡩࡶࡻࡩࡷࡣ࡯ࡩࡳࡺࠠࡰࡨࠣࡎࡦࡼࡡࠨࡵࠣࡓࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࡉࡧ࡯ࡴࡪࡸ࠮ࠋࠤࠥࠦᥳ")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111l11l1_opy_())
bstack111llll11l1_opy_ = [
    bstack11l11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᥴ"),
    bstack11l11_opy_ (u"ࠧ࠮࠯ࡱࡳ࠲࡬ࡩࡳࡵࡷ࠱ࡷࡻ࡮ࠨ᥵"),
    bstack11l11_opy_ (u"ࠨ࠯࠰ࡲࡴ࠳ࡤࡦࡨࡤࡹࡱࡺ࠭ࡣࡴࡲࡻࡸ࡫ࡲ࠮ࡥ࡫ࡩࡨࡱࠧ᥶"),
    bstack11l11_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᥷"),
    bstack11l11_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡤࡦࡨࡤࡹࡱࡺ࠭ࡢࡲࡳࡷࠬ᥸"),
    bstack11l11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡨࡲࡸࠫ᥹"),
    bstack11l11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡦࡨࡺ࠲ࡹࡨ࡮࠯ࡸࡷࡦ࡭ࡥࠨ᥺"),
    bstack11l11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡶࡳ࡫ࡺࡷࡢࡴࡨ࠱ࡷࡧࡳࡵࡧࡵ࡭ࡿ࡫ࡲࠨ᥻"),
    bstack11l11_opy_ (u"ࠧ࠮࠯ࡱࡳ࠲ࡹࡡ࡯ࡦࡥࡳࡽ࠭᥼"),
    bstack11l11_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡧࡧࡣ࡬ࡩࡵࡳࡺࡴࡤ࠮ࡶ࡬ࡱࡪࡸ࠭ࡵࡪࡵࡳࡹࡺ࡬ࡪࡰࡪࠫ᥽"),
    bstack11l11_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲ࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ࡫ࡱ࡫࠲ࡵࡣࡤ࡮ࡸࡨࡪࡪ࠭ࡸ࡫ࡱࡨࡴࡽࡳࠨ᥾"),
    bstack11l11_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡲࡦࡰࡧࡩࡷ࡫ࡲ࠮ࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࡮ࡴࡧࠨ᥿"),
    bstack11l11_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡧࡧࡤࡸࡺࡸࡥࡴ࠿ࡗࡶࡦࡴࡳ࡭ࡣࡷࡩ࡚ࡏࠧᦀ"),
    bstack11l11_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮࡫ࡳࡧ࠲࡬࡬ࡰࡱࡧ࡭ࡳ࡭࠭ࡱࡴࡲࡸࡪࡩࡴࡪࡱࡱࠫᦁ"),
    bstack11l11_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡺࡩࡧ࠳ࡳࡦࡥࡸࡶ࡮ࡺࡹࠨᦂ"),
    bstack11l11_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡪࡪࡧࡴࡶࡴࡨࡷࡂ࡜ࡩࡻࡆ࡬ࡷࡵࡲࡡࡺࡅࡲࡱࡵࡵࡳࡪࡶࡲࡶࠬᦃ"),
    bstack11l11_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡱࡵࡧࡨ࡫ࡱ࡫ࠬᦄ"),
    bstack11l11_opy_ (u"ࠩ࠰࠱ࡸ࡯࡬ࡦࡰࡷࠫᦅ")
]
def bstack111ll11ll1_opy_(options, bstack111111lll_opy_=bstack11l11_opy_ (u"ࠥࠦᦆ")):
    bstack11l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡎࡴࡪࡦࡥࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡉࡨࡳࡱࡰࡩࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡࡨࡲࡶࠥࡲ࡯ࡢࡦࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠏࠦࠠࠡࠢࡄࡨࡩࡹࠠ࠲࠺ࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡳࠡࡦࡨࡪࡪࡴࡳࡪࡸࡨࡰࡾࠦࠨࡰࡰ࡯ࡽࠥ࡯ࡦࠡࡰࡲࡸࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡧࡶࡩࡳࡺࠩ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠡࡱࡥ࡮ࡪࡩࡴࠡࡱࡵࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡽࡩࡵࡪࠣࡥࡩࡪ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠪࠬࠤࡲ࡫ࡴࡩࡱࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡶࡨࡼࡹࡥ࡮ࡢ࡯ࡨ࠾ࠥࡉ࡯࡯ࡶࡨࡼࡹࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡࠪࡨ࠲࡬࠴ࠬࠡࠤࡳࡽࡹ࡫ࡳࡵࠤ࠯ࠤࠧࡶࡹࡵࡪࡲࡲࠧ࠯ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡏࡷࡰࡦࡪࡸࠠࡰࡨࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡡࡥࡦࡨࡨࠏࠦࠠࠡࠢࠥࠦࠧᦇ")
    if not bstack111111lll_opy_:
        bstack111111lll_opy_ = bstack11l11_opy_ (u"ࠧࡲ࡯ࡢࡦ࠰ࡸࡪࡹࡴࡪࡰࡪࠦᦈ")
    if options is None or not hasattr(options, bstack11l11_opy_ (u"࠭ࡡࡥࡦࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬᦉ")):
        logger.debug(bstack11l11_opy_ (u"ࠢ࡜ࡽࢀࡡࠥࡕࡰࡵ࡫ࡲࡲࡸࠦࡩࡴࠢࡑࡳࡳ࡫ࠠࡰࡴࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠫ࠭࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡ࡫ࡱ࡮ࡪࡩࡴࡪࡱࡱࠦᦊ").format(bstack111111lll_opy_))
        return 0
    bstack11l1111l1l1_opy_ = getattr(options, bstack11l11_opy_ (u"ࠨࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᦋ"), [])
    if not isinstance(bstack11l1111l1l1_opy_, list):
        bstack11l1111l1l1_opy_ = []
    bstack111llll111l_opy_ = set()
    for arg in bstack11l1111l1l1_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack11l11_opy_ (u"ࠩࡀࠫᦌ"))[0] if bstack11l11_opy_ (u"ࠪࡁࠬᦍ") in arg else arg
            bstack111llll111l_opy_.add(flag)
    bstack1ll1l1ll11_opy_ = 0
    for arg in bstack111llll11l1_opy_:
        flag = arg.split(bstack11l11_opy_ (u"ࠫࡂ࠭ᦎ"))[0] if bstack11l11_opy_ (u"ࠬࡃࠧᦏ") in arg else arg
        if flag not in bstack111llll111l_opy_:
            options.add_argument(arg)
            bstack1ll1l1ll11_opy_ += 1
    if bstack1ll1l1ll11_opy_ > 0:
        logger.debug(bstack11l11_opy_ (u"ࠨ࡛ࡼࡿࡠࠤࡎࡴࡪࡦࡥࡷࡩࡩࠦࡻࡾࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡤࡶ࡬ࡹࠠࡧࡱࡵࠤࡱࡵࡡࡥࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠥᦐ").format(bstack111111lll_opy_, bstack1ll1l1ll11_opy_))
    return bstack1ll1l1ll11_opy_