# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
bstack1111l_opy_ (u"ࠥࠦࠧࠐࡈࡦ࡮ࡳࡩࡷࠦࡦࡰࡴࠣ࡭ࡳࡰࡥࡤࡶ࡬ࡲ࡬ࠦࡤࡦࡨࡤࡹࡱࡺࠠࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠠࡢࡴࡪࡷࠥࡽࡨࡦࡰࠣࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩ࠴ࠊࡔࡶࡵ࡭ࡨࡺ࡬ࡺࠢࡧࡩ࡫࡫࡮ࡴ࡫ࡹࡩ࠿ࠦ࡮ࡦࡸࡨࡶࠥࡵࡶࡦࡴࡺࡶ࡮ࡺࡥࡴࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡦࡸࡧࡴ࠰ࠍࡘ࡭࡯ࡳࠡ࡫ࡶࠤࡹ࡮ࡥࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡧࡴࡹ࡮ࡼࡡ࡭ࡧࡱࡸࠥࡵࡦࠡࡌࡤࡺࡦ࠭ࡳࠡࡑࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࡎࡥ࡭ࡲࡨࡶ࠳ࠐࠢࠣࠤ᭛")
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
bstack111ll11ll1l_opy_ = [
    bstack1111l_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨ᭜"),
    bstack1111l_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡪ࡮ࡸࡳࡵ࠯ࡵࡹࡳ࠭᭝"),
    bstack1111l_opy_ (u"࠭࠭࠮ࡰࡲ࠱ࡩ࡫ࡦࡢࡷ࡯ࡸ࠲ࡨࡲࡰࡹࡶࡩࡷ࠳ࡣࡩࡧࡦ࡯ࠬ᭞"),
    bstack1111l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᭟"),
    bstack1111l_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡩ࡫ࡦࡢࡷ࡯ࡸ࠲ࡧࡰࡱࡵࠪ᭠"),
    bstack1111l_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡭ࡰࡶࠩ᭡"),
    bstack1111l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡤࡦࡸ࠰ࡷ࡭ࡳ࠭ࡶࡵࡤ࡫ࡪ࠭᭢"),
    bstack1111l_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡴࡱࡩࡸࡼࡧࡲࡦ࠯ࡵࡥࡸࡺࡥࡳ࡫ࡽࡩࡷ࠭᭣"),
    bstack1111l_opy_ (u"ࠬ࠳࠭࡯ࡱ࠰ࡷࡦࡴࡤࡣࡱࡻࠫ᭤"),
    bstack1111l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯ࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩ࠳ࡴࡪ࡯ࡨࡶ࠲ࡺࡨࡳࡱࡷࡸࡱ࡯࡮ࡨࠩ᭥"),
    bstack1111l_opy_ (u"ࠧ࠮࠯ࡧ࡭ࡸࡧࡢ࡭ࡧ࠰ࡦࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࡩ࡯ࡩ࠰ࡳࡨࡩ࡬ࡶࡦࡨࡨ࠲ࡽࡩ࡯ࡦࡲࡻࡸ࠭᭦"),
    bstack1111l_opy_ (u"ࠨ࠯࠰ࡨ࡮ࡹࡡࡣ࡮ࡨ࠱ࡷ࡫࡮ࡥࡧࡵࡩࡷ࠳ࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦ࡬ࡲ࡬࠭᭧"),
    bstack1111l_opy_ (u"ࠩ࠰࠱ࡩ࡯ࡳࡢࡤ࡯ࡩ࠲࡬ࡥࡢࡶࡸࡶࡪࡹ࠽ࡕࡴࡤࡲࡸࡲࡡࡵࡧࡘࡍࠬ᭨"),
    bstack1111l_opy_ (u"ࠪ࠱࠲ࡪࡩࡴࡣࡥࡰࡪ࠳ࡩࡱࡥ࠰ࡪࡱࡵ࡯ࡥ࡫ࡱ࡫࠲ࡶࡲࡰࡶࡨࡧࡹ࡯࡯࡯ࠩ᭩"),
    bstack1111l_opy_ (u"ࠫ࠲࠳ࡤࡪࡵࡤࡦࡱ࡫࠭ࡸࡧࡥ࠱ࡸ࡫ࡣࡶࡴ࡬ࡸࡾ࠭᭪"),
    bstack1111l_opy_ (u"ࠬ࠳࠭ࡥ࡫ࡶࡥࡧࡲࡥ࠮ࡨࡨࡥࡹࡻࡲࡦࡵࡀ࡚࡮ࢀࡄࡪࡵࡳࡰࡦࡿࡃࡰ࡯ࡳࡳࡸ࡯ࡴࡰࡴࠪ᭫"),
    bstack1111l_opy_ (u"࠭࠭࠮ࡦ࡬ࡷࡦࡨ࡬ࡦ࠯࡯ࡳ࡬࡭ࡩ࡯ࡩ᭬ࠪ"),
    bstack1111l_opy_ (u"ࠧ࠮࠯ࡶ࡭ࡱ࡫࡮ࡵࠩ᭭")
]
def bstack1l111l11l_opy_(options, bstack1l11ll111_opy_=bstack1111l_opy_ (u"ࠣࠤ᭮")):
    bstack1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡌࡲ࡯࡫ࡣࡵࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡦࡰࡴࠣࡰࡴࡧࡤࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠍࠤࠥࠦࠠࡂࡦࡧࡷࠥ࠷࠸ࠡࡅ࡫ࡶࡴࡳࡥࠡࡣࡵ࡫ࡸࠦࡤࡦࡨࡨࡲࡸ࡯ࡶࡦ࡮ࡼࠤ࠭ࡵ࡮࡭ࡻࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸࡥࡴࡧࡱࡸ࠮࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠦ࡯ࡣ࡬ࡨࡧࡹࠦ࡯ࡳࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡻ࡮ࡺࡨࠡࡣࡧࡨࡤࡧࡲࡨࡷࡰࡩࡳࡺࠨࠪࠢࡰࡩࡹ࡮࡯ࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡴࡦࡺࡷࡣࡳࡧ࡭ࡦ࠼ࠣࡇࡴࡴࡴࡦࡺࡷࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࡨࡲࡶࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࠨࡦ࠰ࡪ࠲࠱ࠦࠢࡱࡻࡷࡩࡸࡺࠢ࠭ࠢࠥࡴࡾࡺࡨࡰࡰࠥ࠭ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡔࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤࡦࡪࡤࡦࡦࠍࠤࠥࠦࠠࠣࠤࠥ᭯")
    if not bstack1l11ll111_opy_:
        bstack1l11ll111_opy_ = bstack1111l_opy_ (u"ࠥࡰࡴࡧࡤ࠮ࡶࡨࡷࡹ࡯࡮ࡨࠤ᭰")
    if options is None or not hasattr(options, bstack1111l_opy_ (u"ࠫࡦࡪࡤࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ᭱")):
        logger.debug(bstack1111l_opy_ (u"ࠧࡡࡻࡾ࡟ࠣࡓࡵࡺࡩࡰࡰࡶࠤ࡮ࡹࠠࡏࡱࡱࡩࠥࡵࡲࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡤࡨࡩࡥࡡࡳࡩࡸࡱࡪࡴࡴࠩࠫ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡩ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠤ᭲").format(bstack1l11ll111_opy_))
        return 0
    bstack111lll1l111_opy_ = getattr(options, bstack1111l_opy_ (u"࠭࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᭳"), [])
    if not isinstance(bstack111lll1l111_opy_, list):
        bstack111lll1l111_opy_ = []
    bstack111ll11ll11_opy_ = set()
    for arg in bstack111lll1l111_opy_:
        if isinstance(arg, str):
            flag = arg.split(bstack1111l_opy_ (u"ࠧ࠾ࠩ᭴"))[0] if bstack1111l_opy_ (u"ࠨ࠿ࠪ᭵") in arg else arg
            bstack111ll11ll11_opy_.add(flag)
    bstack1l1lllll11_opy_ = 0
    for arg in bstack111ll11ll1l_opy_:
        flag = arg.split(bstack1111l_opy_ (u"ࠩࡀࠫ᭶"))[0] if bstack1111l_opy_ (u"ࠪࡁࠬ᭷") in arg else arg
        if flag not in bstack111ll11ll11_opy_:
            options.add_argument(arg)
            bstack1l1lllll11_opy_ += 1
    if bstack1l1lllll11_opy_ > 0:
        logger.debug(bstack1111l_opy_ (u"ࠦࡠࢁࡽ࡞ࠢࡌࡲ࡯࡫ࡣࡵࡧࡧࠤࢀࢃࠠࡄࡪࡵࡳࡲ࡫ࠠࡢࡴࡪࡷࠥ࡬࡯ࡳࠢ࡯ࡳࡦࡪࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠣ᭸").format(bstack1l11ll111_opy_, bstack1l1lllll11_opy_))
    return bstack1l1lllll11_opy_