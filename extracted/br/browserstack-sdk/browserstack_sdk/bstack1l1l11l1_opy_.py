# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l111ll11_opy_ = {}
        bstack111llll1l1_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ༇"), bstack11l1111_opy_ (u"ࠬ࠭༈"))
        if not bstack111llll1l1_opy_:
            return bstack1l111ll11_opy_
        try:
            bstack111llll1ll_opy_ = json.loads(bstack111llll1l1_opy_)
            if bstack11l1111_opy_ (u"ࠨ࡯ࡴࠤ༉") in bstack111llll1ll_opy_:
                bstack1l111ll11_opy_[bstack11l1111_opy_ (u"ࠢࡰࡵࠥ༊")] = bstack111llll1ll_opy_[bstack11l1111_opy_ (u"ࠣࡱࡶࠦ་")]
            if bstack11l1111_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ༌") in bstack111llll1ll_opy_ or bstack11l1111_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ།") in bstack111llll1ll_opy_:
                bstack1l111ll11_opy_[bstack11l1111_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ༎")] = bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ༏"), bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤ༐")))
            if bstack11l1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣ༑") in bstack111llll1ll_opy_ or bstack11l1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ༒") in bstack111llll1ll_opy_:
                bstack1l111ll11_opy_[bstack11l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ༓")] = bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦ༔"), bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ༕")))
            if bstack11l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ༖") in bstack111llll1ll_opy_ or bstack11l1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ༗") in bstack111llll1ll_opy_:
                bstack1l111ll11_opy_[bstack11l1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮༘ࠣ")] = bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰ༙ࠥ"), bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ༚")))
            if bstack11l1111_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥ༛") in bstack111llll1ll_opy_ or bstack11l1111_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ༜") in bstack111llll1ll_opy_:
                bstack1l111ll11_opy_[bstack11l1111_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ༝")] = bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨ༞"), bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦ༟")))
            if bstack11l1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ༠") in bstack111llll1ll_opy_ or bstack11l1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ༡") in bstack111llll1ll_opy_:
                bstack1l111ll11_opy_[bstack11l1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ༢")] = bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ༣"), bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦ༤")))
            if bstack11l1111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ༥") in bstack111llll1ll_opy_ or bstack11l1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ༦") in bstack111llll1ll_opy_:
                bstack1l111ll11_opy_[bstack11l1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ༧")] = bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ༨"), bstack111llll1ll_opy_.get(bstack11l1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ༩")))
            if bstack11l1111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ༪") in bstack111llll1ll_opy_:
                bstack1l111ll11_opy_[bstack11l1111_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ༫")] = bstack111llll1ll_opy_[bstack11l1111_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ༬")]
        except Exception as error:
            logger.error(bstack11l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨ༭") +  str(error))
        return bstack1l111ll11_opy_