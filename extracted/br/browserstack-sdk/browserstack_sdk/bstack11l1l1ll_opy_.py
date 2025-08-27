# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l1ll1l1_opy_ = {}
        bstack111llll1l1_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ༎"), bstack1111lll_opy_ (u"ࠬ࠭༏"))
        if not bstack111llll1l1_opy_:
            return bstack1l1ll1l1_opy_
        try:
            bstack111llll1ll_opy_ = json.loads(bstack111llll1l1_opy_)
            if bstack1111lll_opy_ (u"ࠨ࡯ࡴࠤ༐") in bstack111llll1ll_opy_:
                bstack1l1ll1l1_opy_[bstack1111lll_opy_ (u"ࠢࡰࡵࠥ༑")] = bstack111llll1ll_opy_[bstack1111lll_opy_ (u"ࠣࡱࡶࠦ༒")]
            if bstack1111lll_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ༓") in bstack111llll1ll_opy_ or bstack1111lll_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ༔") in bstack111llll1ll_opy_:
                bstack1l1ll1l1_opy_[bstack1111lll_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ༕")] = bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ༖"), bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤ༗")))
            if bstack1111lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲ༘ࠣ") in bstack111llll1ll_opy_ or bstack1111lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ༙") in bstack111llll1ll_opy_:
                bstack1l1ll1l1_opy_[bstack1111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ༚")] = bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦ༛"), bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ༜")))
            if bstack1111lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ༝") in bstack111llll1ll_opy_ or bstack1111lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ༞") in bstack111llll1ll_opy_:
                bstack1l1ll1l1_opy_[bstack1111lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ༟")] = bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥ༠"), bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ༡")))
            if bstack1111lll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥ༢") in bstack111llll1ll_opy_ or bstack1111lll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ༣") in bstack111llll1ll_opy_:
                bstack1l1ll1l1_opy_[bstack1111lll_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ༤")] = bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨ༥"), bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦ༦")))
            if bstack1111lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ༧") in bstack111llll1ll_opy_ or bstack1111lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ༨") in bstack111llll1ll_opy_:
                bstack1l1ll1l1_opy_[bstack1111lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ༩")] = bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ༪"), bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦ༫")))
            if bstack1111lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ༬") in bstack111llll1ll_opy_ or bstack1111lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ༭") in bstack111llll1ll_opy_:
                bstack1l1ll1l1_opy_[bstack1111lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ༮")] = bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ༯"), bstack111llll1ll_opy_.get(bstack1111lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ༰")))
            if bstack1111lll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ༱") in bstack111llll1ll_opy_:
                bstack1l1ll1l1_opy_[bstack1111lll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ༲")] = bstack111llll1ll_opy_[bstack1111lll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ༳")]
        except Exception as error:
            logger.error(bstack1111lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨ༴") +  str(error))
        return bstack1l1ll1l1_opy_