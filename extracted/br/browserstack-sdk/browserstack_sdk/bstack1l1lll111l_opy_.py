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
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack111l1ll1ll_opy_ = {}
        bstack1111lll1ll_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬྌ"), bstack11ll111_opy_ (u"ࠬ࠭ྍ"))
        if not bstack1111lll1ll_opy_:
            return bstack111l1ll1ll_opy_
        try:
            bstack1111llll11_opy_ = json.loads(bstack1111lll1ll_opy_)
            if bstack11ll111_opy_ (u"ࠨ࡯ࡴࠤྎ") in bstack1111llll11_opy_:
                bstack111l1ll1ll_opy_[bstack11ll111_opy_ (u"ࠢࡰࡵࠥྏ")] = bstack1111llll11_opy_[bstack11ll111_opy_ (u"ࠣࡱࡶࠦྐ")]
            if bstack11ll111_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨྑ") in bstack1111llll11_opy_ or bstack11ll111_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨྒ") in bstack1111llll11_opy_:
                bstack111l1ll1ll_opy_[bstack11ll111_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢྒྷ")] = bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤྔ"), bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤྕ")))
            if bstack11ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣྖ") in bstack1111llll11_opy_ or bstack11ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨྗ") in bstack1111llll11_opy_:
                bstack111l1ll1ll_opy_[bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ྘")] = bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦྙ"), bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤྚ")))
            if bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢྛ") in bstack1111llll11_opy_ or bstack11ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢྜ") in bstack1111llll11_opy_:
                bstack111l1ll1ll_opy_[bstack11ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣྜྷ")] = bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥྞ"), bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥྟ")))
            if bstack11ll111_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥྠ") in bstack1111llll11_opy_ or bstack11ll111_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣྡ") in bstack1111llll11_opy_:
                bstack111l1ll1ll_opy_[bstack11ll111_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤྡྷ")] = bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨྣ"), bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦྤ")))
            if bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥྥ") in bstack1111llll11_opy_ or bstack11ll111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣྦ") in bstack1111llll11_opy_:
                bstack111l1ll1ll_opy_[bstack11ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤྦྷ")] = bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨྨ"), bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦྩ")))
            if bstack11ll111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤྪ") in bstack1111llll11_opy_ or bstack11ll111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤྫ") in bstack1111llll11_opy_:
                bstack111l1ll1ll_opy_[bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥྫྷ")] = bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧྭ"), bstack1111llll11_opy_.get(bstack11ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧྮ")))
            if bstack11ll111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨྯ") in bstack1111llll11_opy_:
                bstack111l1ll1ll_opy_[bstack11ll111_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢྰ")] = bstack1111llll11_opy_[bstack11ll111_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣྱ")]
        except Exception as error:
            logger.error(bstack11ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨྲ") +  str(error))
        return bstack111l1ll1ll_opy_