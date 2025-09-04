# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1lllll1l1l_opy_ = {}
        bstack111lll1l1l_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ༓"), bstack1111l1l_opy_ (u"ࠪࠫ༔"))
        if not bstack111lll1l1l_opy_:
            return bstack1lllll1l1l_opy_
        try:
            bstack111lll1ll1_opy_ = json.loads(bstack111lll1l1l_opy_)
            if bstack1111l1l_opy_ (u"ࠦࡴࡹࠢ༕") in bstack111lll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111l1l_opy_ (u"ࠧࡵࡳࠣ༖")] = bstack111lll1ll1_opy_[bstack1111l1l_opy_ (u"ࠨ࡯ࡴࠤ༗")]
            if bstack1111l1l_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱ༘ࠦ") in bstack111lll1ll1_opy_ or bstack1111l1l_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱ༙ࠦ") in bstack111lll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111l1l_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ༚")] = bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ༛"), bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ༜")))
            if bstack1111l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨ༝") in bstack111lll1ll1_opy_ or bstack1111l1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ༞") in bstack111lll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ༟")] = bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ༠"), bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ༡")))
            if bstack1111l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ༢") in bstack111lll1ll1_opy_ or bstack1111l1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧ༣") in bstack111lll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ༤")] = bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ༥"), bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ༦")))
            if bstack1111l1l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣ༧") in bstack111lll1ll1_opy_ or bstack1111l1l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ༨") in bstack111lll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111l1l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ༩")] = bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦ༪"), bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ༫")))
            if bstack1111l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ༬") in bstack111lll1ll1_opy_ or bstack1111l1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ༭") in bstack111lll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111l1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ༮")] = bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ༯"), bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ༰")))
            if bstack1111l1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ༱") in bstack111lll1ll1_opy_ or bstack1111l1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ༲") in bstack111lll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ༳")] = bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥ༴"), bstack111lll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰ༵ࠥ")))
            if bstack1111l1l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ༶") in bstack111lll1ll1_opy_:
                bstack1lllll1l1l_opy_[bstack1111l1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷ༷ࠧ")] = bstack111lll1ll1_opy_[bstack1111l1l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ༸")]
        except Exception as error:
            logger.error(bstack1111l1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼༹ࠣࠦ") +  str(error))
        return bstack1lllll1l1l_opy_