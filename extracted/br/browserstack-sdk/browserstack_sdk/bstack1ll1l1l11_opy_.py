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
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1111llll1l_opy_ = {}
        bstack1111ll1l11_opy_ = os.environ.get(bstack11l11_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ྇"), bstack11l11_opy_ (u"ࠧࠨྈ"))
        if not bstack1111ll1l11_opy_:
            return bstack1111llll1l_opy_
        try:
            bstack1111ll1l1l_opy_ = json.loads(bstack1111ll1l11_opy_)
            if bstack11l11_opy_ (u"ࠣࡱࡶࠦྉ") in bstack1111ll1l1l_opy_:
                bstack1111llll1l_opy_[bstack11l11_opy_ (u"ࠤࡲࡷࠧྊ")] = bstack1111ll1l1l_opy_[bstack11l11_opy_ (u"ࠥࡳࡸࠨྋ")]
            if bstack11l11_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣྌ") in bstack1111ll1l1l_opy_ or bstack11l11_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣྍ") in bstack1111ll1l1l_opy_:
                bstack1111llll1l_opy_[bstack11l11_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤྎ")] = bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦྏ"), bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦྐ")))
            if bstack11l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥྑ") in bstack1111ll1l1l_opy_ or bstack11l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣྒ") in bstack1111ll1l1l_opy_:
                bstack1111llll1l_opy_[bstack11l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤྒྷ")] = bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨྔ"), bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦྕ")))
            if bstack11l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤྖ") in bstack1111ll1l1l_opy_ or bstack11l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤྗ") in bstack1111ll1l1l_opy_:
                bstack1111llll1l_opy_[bstack11l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ྘")] = bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧྙ"), bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧྚ")))
            if bstack11l11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧྛ") in bstack1111ll1l1l_opy_ or bstack11l11_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥྜ") in bstack1111ll1l1l_opy_:
                bstack1111llll1l_opy_[bstack11l11_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦྜྷ")] = bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣྞ"), bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨྟ")))
            if bstack11l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧྠ") in bstack1111ll1l1l_opy_ or bstack11l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥྡ") in bstack1111ll1l1l_opy_:
                bstack1111llll1l_opy_[bstack11l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦྡྷ")] = bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣྣ"), bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨྤ")))
            if bstack11l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦྥ") in bstack1111ll1l1l_opy_ or bstack11l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦྦ") in bstack1111ll1l1l_opy_:
                bstack1111llll1l_opy_[bstack11l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧྦྷ")] = bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢྨ"), bstack1111ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢྩ")))
            if bstack11l11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣྪ") in bstack1111ll1l1l_opy_:
                bstack1111llll1l_opy_[bstack11l11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤྫ")] = bstack1111ll1l1l_opy_[bstack11l11_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥྫྷ")]
        except Exception as error:
            logger.error(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣྭ") +  str(error))
        return bstack1111llll1l_opy_