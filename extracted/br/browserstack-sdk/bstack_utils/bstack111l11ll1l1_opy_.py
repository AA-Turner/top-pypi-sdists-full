# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import time
from bstack_utils.bstack11ll111ll1l_opy_ import bstack11ll111l1ll_opy_
from bstack_utils.constants import bstack11l1l1ll1ll_opy_
from bstack_utils.helper import get_host_info, bstack111llll1lll_opy_
class bstack111l11l111l_opy_:
    bstack1l11ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡢࡰࡧࡰࡪࡹࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡶࡻ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ⁘")
    def __init__(self, config, logger):
        bstack1l11ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡪࡩࡤࡶ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡢࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡳࡵࡴ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦ࡮ࡢ࡯ࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⁙")
        self.config = config
        self.logger = logger
        self.bstack1llll1llll11_opy_ = bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡰ࡭࡫ࡷ࠱ࡹ࡫ࡳࡵࡵࠥ⁚")
        self.bstack1llll1llll1l_opy_ = None
        self.bstack1llll1lll1ll_opy_ = 60
        self.bstack1llll1lll1l1_opy_ = 5
        self.bstack1lllll111l1l_opy_ = 0
    def bstack111l11l1ll1_opy_(self, test_files, orchestration_strategy, bstack111l11l1111_opy_={}):
        bstack1l11ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡧ࡮ࡥࠢࡶࡸࡴࡸࡥࡴࠢࡷ࡬ࡪࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡴࡴࡲ࡬ࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⁛")
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡌࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣ⁜").format(orchestration_strategy))
        try:
            bstack1111ll1l1ll_opy_ = []
            if bstack111l11l1111_opy_[bstack1l11ll1_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪ⁝")].get(bstack1l11ll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⁞"), False): # check if bstack1lllll11111l_opy_ bstack1llll1lll111_opy_ is enabled
                bstack1111ll11lll_opy_ = bstack111l11l1111_opy_[bstack1l11ll1_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ ")].get(bstack1l11ll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ⁠"), []) # for multi-repo
                bstack1111ll1l1ll_opy_ = bstack111llll1lll_opy_(bstack1111ll11lll_opy_) # bstack11l11111l11_opy_-repo is handled bstack111l111lll1_opy_
            payload = {
                bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ⁡"): [{bstack1l11ll1_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦ⁢"): f} for f in test_files],
                bstack1l11ll1_opy_ (u"ࠥࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡖࡸࡷࡧࡴࡦࡩࡼࠦ⁣"): orchestration_strategy,
                bstack1l11ll1_opy_ (u"ࠦࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡑࡪࡺࡡࡥࡣࡷࡥࠧ⁤"): bstack111l11l1111_opy_,
                bstack1l11ll1_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣ⁥"): int(os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤ⁦")) or bstack1l11ll1_opy_ (u"ࠢ࠱ࠤ⁧")),
                bstack1l11ll1_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧ⁨"): int(os.environ.get(bstack1l11ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦ⁩")) or bstack1l11ll1_opy_ (u"ࠥ࠵ࠧ⁪")),
                bstack1l11ll1_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤ⁫"): self.config.get(bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ⁬"), bstack1l11ll1_opy_ (u"࠭ࠧ⁭")),
                bstack1l11ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥ⁮"): self.config.get(bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ⁯"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l11ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢ⁰"): self.config.get(bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬⁱ"), bstack1l11ll1_opy_ (u"ࠫࠬ⁲")),
                bstack1l11ll1_opy_ (u"ࠧ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠢ⁳"): get_host_info(),
                bstack1l11ll1_opy_ (u"ࠨࡰࡳࡆࡨࡸࡦ࡯࡬ࡴࠤ⁴"): bstack1111ll1l1ll_opy_
            }
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾ࠥࢁࡽࠣ⁵").format(payload))
            response = bstack11ll111l1ll_opy_.bstack1llllll11ll1_opy_(self.bstack1llll1llll11_opy_, payload)
            if response:
                self.bstack1llll1llll1l_opy_ = self._1llll1lllll1_opy_(response)
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡔࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ⁶").format(self.bstack1llll1llll1l_opy_))
            else:
                self.logger.error(bstack1l11ll1_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠯ࠤ⁷"))
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀ࠺ࠡࡽࢀࠦ⁸").format(e))
    def _1llll1lllll1_opy_(self, response):
        bstack1l11ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡧ࡮ࡥࠢࡨࡼࡹࡸࡡࡤࡶࡶࠤࡷ࡫࡬ࡦࡸࡤࡲࡹࠦࡦࡪࡧ࡯ࡨࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⁹")
        bstack1lll111ll_opy_ = {}
        bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ⁺")] = response.get(bstack1l11ll1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ⁻"), self.bstack1llll1lll1ll_opy_)
        bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ⁼")] = response.get(bstack1l11ll1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ⁽"), self.bstack1llll1lll1l1_opy_)
        bstack1llll1ll1lll_opy_ = response.get(bstack1l11ll1_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ⁾"))
        bstack1lllll111l11_opy_ = response.get(bstack1l11ll1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢⁿ"))
        if bstack1llll1ll1lll_opy_:
            bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ₀")] = bstack1llll1ll1lll_opy_.split(bstack11l1l1ll1ll_opy_ + bstack1l11ll1_opy_ (u"ࠧ࠵ࠢ₁"))[1] if bstack11l1l1ll1ll_opy_ + bstack1l11ll1_opy_ (u"ࠨ࠯ࠣ₂") in bstack1llll1ll1lll_opy_ else bstack1llll1ll1lll_opy_
        else:
            bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ₃")] = None
        if bstack1lllll111l11_opy_:
            bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ₄")] = bstack1lllll111l11_opy_.split(bstack11l1l1ll1ll_opy_ + bstack1l11ll1_opy_ (u"ࠤ࠲ࠦ₅"))[1] if bstack11l1l1ll1ll_opy_ + bstack1l11ll1_opy_ (u"ࠥ࠳ࠧ₆") in bstack1lllll111l11_opy_ else bstack1lllll111l11_opy_
        else:
            bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ₇")] = None
        if (
            response.get(bstack1l11ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ₈")) is None or
            response.get(bstack1l11ll1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ₉")) is None or
            response.get(bstack1l11ll1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ₊")) is None or
            response.get(bstack1l11ll1_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ₋")) is None
        ):
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤ࡞ࡴࡷࡵࡣࡦࡵࡶࡣࡸࡶ࡬ࡪࡶࡢࡸࡪࡹࡴࡴࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࡡࠥࡘࡥࡤࡧ࡬ࡺࡪࡪࠠ࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨࠬࡸ࠯ࠠࡧࡱࡵࠤࡸࡵ࡭ࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩࡸࠦࡩ࡯ࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ₌"))
        return bstack1lll111ll_opy_
    def bstack111l11ll1ll_opy_(self):
        if not self.bstack1llll1llll1l_opy_:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡓࡵࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠰ࠥ₍"))
            return None
        bstack1lllll1111l1_opy_ = None
        test_files = []
        bstack1llll1lll11l_opy_ = int(time.time() * 1000) # bstack1lllll111111_opy_ sec
        bstack1llll1llllll_opy_ = int(self.bstack1llll1llll1l_opy_.get(bstack1l11ll1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ₎"), self.bstack1llll1lll1l1_opy_))
        bstack1lllll1111ll_opy_ = int(self.bstack1llll1llll1l_opy_.get(bstack1l11ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ₏"), self.bstack1llll1lll1ll_opy_)) * 1000
        bstack1lllll111l11_opy_ = self.bstack1llll1llll1l_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥₐ"), None)
        bstack1llll1ll1lll_opy_ = self.bstack1llll1llll1l_opy_.get(bstack1l11ll1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥₑ"), None)
        if bstack1llll1ll1lll_opy_ is None and bstack1lllll111l11_opy_ is None:
            return None
        try:
            while bstack1llll1ll1lll_opy_ and (time.time() * 1000 - bstack1llll1lll11l_opy_) < bstack1lllll1111ll_opy_:
                response = bstack11ll111l1ll_opy_.bstack1llllll1111l_opy_(bstack1llll1ll1lll_opy_, {})
                if response and response.get(bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢₒ")):
                    bstack1lllll1111l1_opy_ = response.get(bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣₓ"))
                self.bstack1lllll111l1l_opy_ += 1
                if bstack1lllll1111l1_opy_:
                    break
                time.sleep(bstack1llll1llllll_opy_)
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡋ࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࡸࠦࡦࡳࡱࡰࠤࡷ࡫ࡳࡶ࡮ࡷࠤ࡚ࡘࡌࠡࡣࡩࡸࡪࡸࠠࡸࡣ࡬ࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࢁࡽࠡࡵࡨࡧࡴࡴࡤࡴ࠰ࠥₔ").format(bstack1llll1llllll_opy_))
            if bstack1lllll111l11_opy_ and not bstack1lllll1111l1_opy_:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡌࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡧࡴࡲࡱࠥࡺࡩ࡮ࡧࡲࡹࡹࠦࡕࡓࡎࠥₕ"))
                response = bstack11ll111l1ll_opy_.bstack1llllll1111l_opy_(bstack1lllll111l11_opy_, {})
                if response and response.get(bstack1l11ll1_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦₖ")):
                    bstack1lllll1111l1_opy_ = response.get(bstack1l11ll1_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧₗ"))
            if bstack1lllll1111l1_opy_ and len(bstack1lllll1111l1_opy_) > 0:
                for bstack111lll111l_opy_ in bstack1lllll1111l1_opy_:
                    file_path = bstack111lll111l_opy_.get(bstack1l11ll1_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤₘ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lllll1111l1_opy_:
                return None
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡒࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡳࡧࡦࡩ࡮ࡼࡥࡥ࠼ࠣࡿࢂࠨₙ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼ࠣࡿࢂࠨₚ").format(e))
            return None
    def bstack111l11llll1_opy_(self):
        bstack1l11ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡇࡐࡊࠢࡦࡥࡱࡲࡳࠡ࡯ࡤࡨࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦₛ")
        return self.bstack1lllll111l1l_opy_