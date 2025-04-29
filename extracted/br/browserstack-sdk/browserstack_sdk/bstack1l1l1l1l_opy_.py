# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll11l111l_opy_ = {}
        bstack11l11l1111_opy_ = os.environ.get(bstack1llllll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨຨ"), bstack1llllll_opy_ (u"ࠨࠩຩ"))
        if not bstack11l11l1111_opy_:
            return bstack1ll11l111l_opy_
        try:
            bstack11l11l111l_opy_ = json.loads(bstack11l11l1111_opy_)
            if bstack1llllll_opy_ (u"ࠤࡲࡷࠧສ") in bstack11l11l111l_opy_:
                bstack1ll11l111l_opy_[bstack1llllll_opy_ (u"ࠥࡳࡸࠨຫ")] = bstack11l11l111l_opy_[bstack1llllll_opy_ (u"ࠦࡴࡹࠢຬ")]
            if bstack1llllll_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤອ") in bstack11l11l111l_opy_ or bstack1llllll_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤຮ") in bstack11l11l111l_opy_:
                bstack1ll11l111l_opy_[bstack1llllll_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥຯ")] = bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧະ"), bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧັ")))
            if bstack1llllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦາ") in bstack11l11l111l_opy_ or bstack1llllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤຳ") in bstack11l11l111l_opy_:
                bstack1ll11l111l_opy_[bstack1llllll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥິ")] = bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢີ"), bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧຶ")))
            if bstack1llllll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥື") in bstack11l11l111l_opy_ or bstack1llllll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰຸࠥ") in bstack11l11l111l_opy_:
                bstack1ll11l111l_opy_[bstack1llllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱູࠦ")] = bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ຺"), bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨົ")))
            if bstack1llllll_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨຼ") in bstack11l11l111l_opy_ or bstack1llllll_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦຽ") in bstack11l11l111l_opy_:
                bstack1ll11l111l_opy_[bstack1llllll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧ຾")] = bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤ຿"), bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢເ")))
            if bstack1llllll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨແ") in bstack11l11l111l_opy_ or bstack1llllll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦໂ") in bstack11l11l111l_opy_:
                bstack1ll11l111l_opy_[bstack1llllll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧໃ")] = bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤໄ"), bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ໅")))
            if bstack1llllll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧໆ") in bstack11l11l111l_opy_ or bstack1llllll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ໇") in bstack11l11l111l_opy_:
                bstack1ll11l111l_opy_[bstack1llllll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ່")] = bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮້ࠣ"), bstack11l11l111l_opy_.get(bstack1llllll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮໊ࠣ")))
            if bstack1llllll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤ໋") in bstack11l11l111l_opy_:
                bstack1ll11l111l_opy_[bstack1llllll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ໌")] = bstack11l11l111l_opy_[bstack1llllll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦໍ")]
        except Exception as error:
            logger.error(bstack1llllll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡥࡹࡧ࠺ࠡࠤ໎") +  str(error))
        return bstack1ll11l111l_opy_