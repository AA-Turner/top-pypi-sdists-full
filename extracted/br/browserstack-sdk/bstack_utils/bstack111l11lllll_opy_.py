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
import time
from bstack_utils.bstack11ll111lll1_opy_ import bstack11ll11l1111_opy_
from bstack_utils.constants import bstack11l1ll111l1_opy_
from bstack_utils.helper import get_host_info, bstack11l11l1ll11_opy_
class bstack111l11l1l1l_opy_:
    bstack1111l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡸࡶࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ⁚")
    def __init__(self, config, logger):
        bstack1111l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡥ࡫ࡦࡸ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡤࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡵࡷࡶ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡࡰࡤࡱࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⁛")
        self.config = config
        self.logger = logger
        self.bstack1lllll111l1l_opy_ = bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡲ࡯࡭ࡹ࠳ࡴࡦࡵࡷࡷࠧ⁜")
        self.bstack1llll1llllll_opy_ = None
        self.bstack1lllll1111l1_opy_ = 60
        self.bstack1llll1lll111_opy_ = 5
        self.bstack1lllll111111_opy_ = 0
    def bstack111l11llll1_opy_(self, test_files, orchestration_strategy, bstack111l11l1ll1_opy_={}):
        bstack1111l1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡱ࡭ࡹ࡯ࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡸࡺ࡯ࡳࡧࡶࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡶ࡯࡭࡮࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⁝")
        self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡎࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥ⁞").format(orchestration_strategy))
        try:
            bstack111l111ll11_opy_ = []
            if bstack111l11l1ll1_opy_[bstack1111l1l_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ ")].get(bstack1111l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨ⁠"), False): # check if bstack1llll1llll11_opy_ bstack1lllll1111ll_opy_ is enabled
                bstack1111lllll1l_opy_ = bstack111l11l1ll1_opy_[bstack1111l1l_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ⁡")].get(bstack1111l1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ⁢"), []) # for multi-repo
                bstack111l111ll11_opy_ = bstack11l11l1ll11_opy_(bstack1111lllll1l_opy_) # bstack111ll1l1ll1_opy_-repo is handled bstack111l111l1ll_opy_
            payload = {
                bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ⁣"): [{bstack1111l1l_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ⁤"): f} for f in test_files],
                bstack1111l1l_opy_ (u"ࠧࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡘࡺࡲࡢࡶࡨ࡫ࡾࠨ⁥"): orchestration_strategy,
                bstack1111l1l_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡓࡥࡵࡣࡧࡥࡹࡧࠢ⁦"): bstack111l11l1ll1_opy_,
                bstack1111l1l_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ⁧"): int(os.environ.get(bstack1111l1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ⁨")) or bstack1111l1l_opy_ (u"ࠤ࠳ࠦ⁩")),
                bstack1111l1l_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ⁪"): int(os.environ.get(bstack1111l1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ⁫")) or bstack1111l1l_opy_ (u"ࠧ࠷ࠢ⁬")),
                bstack1111l1l_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ⁭"): self.config.get(bstack1111l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ⁮"), bstack1111l1l_opy_ (u"ࠨࠩ⁯")),
                bstack1111l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ⁰"): self.config.get(bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ⁱ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1111l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ⁲"): self.config.get(bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⁳"), bstack1111l1l_opy_ (u"࠭ࠧ⁴")),
                bstack1111l1l_opy_ (u"ࠢࡩࡱࡶࡸࡎࡴࡦࡰࠤ⁵"): get_host_info(),
                bstack1111l1l_opy_ (u"ࠣࡲࡵࡈࡪࡺࡡࡪ࡮ࡶࠦ⁶"): bstack111l111ll11_opy_
            }
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥ⁷").format(payload))
            response = bstack11ll11l1111_opy_.bstack1llllll1111l_opy_(self.bstack1lllll111l1l_opy_, payload)
            if response:
                self.bstack1llll1llllll_opy_ = self._1lllll111l11_opy_(response)
                self.logger.debug(bstack1111l1l_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⁸").format(self.bstack1llll1llllll_opy_))
            else:
                self.logger.error(bstack1111l1l_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦ⁹"))
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻࠼ࠣࡿࢂࠨ⁺").format(e))
    def _1lllll111l11_opy_(self, response):
        bstack1111l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡢࡰࡧࠤࡪࡾࡴࡳࡣࡦࡸࡸࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡨ࡬ࡩࡱࡪࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⁻")
        bstack11ll11ll11_opy_ = {}
        bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ⁼")] = response.get(bstack1111l1l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ⁽"), self.bstack1lllll1111l1_opy_)
        bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ⁾")] = response.get(bstack1111l1l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧⁿ"), self.bstack1llll1lll111_opy_)
        bstack1llll1lll11l_opy_ = response.get(bstack1111l1l_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ₀"))
        bstack1lllll11111l_opy_ = response.get(bstack1111l1l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ₁"))
        if bstack1llll1lll11l_opy_:
            bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ₂")] = bstack1llll1lll11l_opy_.split(bstack11l1ll111l1_opy_ + bstack1111l1l_opy_ (u"ࠢ࠰ࠤ₃"))[1] if bstack11l1ll111l1_opy_ + bstack1111l1l_opy_ (u"ࠣ࠱ࠥ₄") in bstack1llll1lll11l_opy_ else bstack1llll1lll11l_opy_
        else:
            bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ₅")] = None
        if bstack1lllll11111l_opy_:
            bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ₆")] = bstack1lllll11111l_opy_.split(bstack11l1ll111l1_opy_ + bstack1111l1l_opy_ (u"ࠦ࠴ࠨ₇"))[1] if bstack11l1ll111l1_opy_ + bstack1111l1l_opy_ (u"ࠧ࠵ࠢ₈") in bstack1lllll11111l_opy_ else bstack1lllll11111l_opy_
        else:
            bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ₉")] = None
        if (
            response.get(bstack1111l1l_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ₊")) is None or
            response.get(bstack1111l1l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ₋")) is None or
            response.get(bstack1111l1l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ₌")) is None or
            response.get(bstack1111l1l_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ₍")) is None
        ):
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡠࡶࡲࡰࡥࡨࡷࡸࡥࡳࡱ࡮࡬ࡸࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡳࡱࡱࡱࡷࡪࡣࠠࡓࡧࡦࡩ࡮ࡼࡥࡥࠢࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠮ࡳࠪࠢࡩࡳࡷࠦࡳࡰ࡯ࡨࠤࡦࡺࡴࡳ࡫ࡥࡹࡹ࡫ࡳࠡ࡫ࡱࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣ₎"))
        return bstack11ll11ll11_opy_
    def bstack111l11l1lll_opy_(self):
        if not self.bstack1llll1llllll_opy_:
            self.logger.error(bstack1111l1l_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠲ࠧ₏"))
            return None
        bstack1llll1llll1l_opy_ = None
        test_files = []
        bstack1llll1lllll1_opy_ = int(time.time() * 1000) # bstack1llll1lll1ll_opy_ sec
        bstack1llll1lll1l1_opy_ = int(self.bstack1llll1llllll_opy_.get(bstack1111l1l_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣₐ"), self.bstack1llll1lll111_opy_))
        bstack1lllll111ll1_opy_ = int(self.bstack1llll1llllll_opy_.get(bstack1111l1l_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣₑ"), self.bstack1lllll1111l1_opy_)) * 1000
        bstack1lllll11111l_opy_ = self.bstack1llll1llllll_opy_.get(bstack1111l1l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧₒ"), None)
        bstack1llll1lll11l_opy_ = self.bstack1llll1llllll_opy_.get(bstack1111l1l_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧₓ"), None)
        if bstack1llll1lll11l_opy_ is None and bstack1lllll11111l_opy_ is None:
            return None
        try:
            while bstack1llll1lll11l_opy_ and (time.time() * 1000 - bstack1llll1lllll1_opy_) < bstack1lllll111ll1_opy_:
                response = bstack11ll11l1111_opy_.bstack1llllll11ll1_opy_(bstack1llll1lll11l_opy_, {})
                if response and response.get(bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤₔ")):
                    bstack1llll1llll1l_opy_ = response.get(bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥₕ"))
                self.bstack1lllll111111_opy_ += 1
                if bstack1llll1llll1l_opy_:
                    break
                time.sleep(bstack1llll1lll1l1_opy_)
                self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡆࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡨࡵࡳࡲࠦࡲࡦࡵࡸࡰࡹࠦࡕࡓࡎࠣࡥ࡫ࡺࡥࡳࠢࡺࡥ࡮ࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡼࡿࠣࡷࡪࡩ࡯࡯ࡦࡶ࠲ࠧₖ").format(bstack1llll1lll1l1_opy_))
            if bstack1lllll11111l_opy_ and not bstack1llll1llll1l_opy_:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡵ࡫ࡰࡩࡴࡻࡴࠡࡗࡕࡐࠧₗ"))
                response = bstack11ll11l1111_opy_.bstack1llllll11ll1_opy_(bstack1lllll11111l_opy_, {})
                if response and response.get(bstack1111l1l_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨₘ")):
                    bstack1llll1llll1l_opy_ = response.get(bstack1111l1l_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢₙ"))
            if bstack1llll1llll1l_opy_ and len(bstack1llll1llll1l_opy_) > 0:
                for bstack111ll1l1ll_opy_ in bstack1llll1llll1l_opy_:
                    file_path = bstack111ll1l1ll_opy_.get(bstack1111l1l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦₚ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1llll1llll1l_opy_:
                return None
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡔࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡵࡩࡨ࡫ࡩࡷࡧࡧ࠾ࠥࢁࡽࠣₛ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾ࠥࢁࡽࠣₜ").format(e))
            return None
    def bstack111l11ll1l1_opy_(self):
        bstack1111l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡨࡧ࡬࡭ࡵࠣࡱࡦࡪࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ₝")
        return self.bstack1lllll111111_opy_