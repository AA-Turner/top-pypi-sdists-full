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
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1111l11l11_opy_ = {}
        bstack11111lll11_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫဳ"), bstack1111l_opy_ (u"ࠫࠬဴ"))
        if not bstack11111lll11_opy_:
            return bstack1111l11l11_opy_
        try:
            bstack11111lll1l_opy_ = json.loads(bstack11111lll11_opy_)
            if bstack1111l_opy_ (u"ࠧࡵࡳࠣဵ") in bstack11111lll1l_opy_:
                bstack1111l11l11_opy_[bstack1111l_opy_ (u"ࠨ࡯ࡴࠤံ")] = bstack11111lll1l_opy_[bstack1111l_opy_ (u"ࠢࡰࡵ့ࠥ")]
            if bstack1111l_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧး") in bstack11111lll1l_opy_ or bstack1111l_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲ္ࠧ") in bstack11111lll1l_opy_:
                bstack1111l11l11_opy_[bstack1111l_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ်")] = bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣျ"), bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣြ")))
            if bstack1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢွ") in bstack11111lll1l_opy_ or bstack1111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧှ") in bstack11111lll1l_opy_:
                bstack1111l11l11_opy_[bstack1111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨဿ")] = bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ၀"), bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ၁")))
            if bstack1111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ၂") in bstack11111lll1l_opy_ or bstack1111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ၃") in bstack11111lll1l_opy_:
                bstack1111l11l11_opy_[bstack1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ၄")] = bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ၅"), bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ၆")))
            if bstack1111l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤ၇") in bstack11111lll1l_opy_ or bstack1111l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ၈") in bstack11111lll1l_opy_:
                bstack1111l11l11_opy_[bstack1111l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ၉")] = bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧ၊"), bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ။")))
            if bstack1111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ၌") in bstack11111lll1l_opy_ or bstack1111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ၍") in bstack11111lll1l_opy_:
                bstack1111l11l11_opy_[bstack1111l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ၎")] = bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ၏"), bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥၐ")))
            if bstack1111l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣၑ") in bstack11111lll1l_opy_ or bstack1111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣၒ") in bstack11111lll1l_opy_:
                bstack1111l11l11_opy_[bstack1111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤၓ")] = bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦၔ"), bstack11111lll1l_opy_.get(bstack1111l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦၕ")))
            if bstack1111l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧၖ") in bstack11111lll1l_opy_:
                bstack1111l11l11_opy_[bstack1111l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨၗ")] = bstack11111lll1l_opy_[bstack1111l_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢၘ")]
        except Exception as error:
            logger.error(bstack1111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧၙ") +  str(error))
        return bstack1111l11l11_opy_