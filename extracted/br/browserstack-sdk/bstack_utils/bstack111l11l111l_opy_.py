# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import time
from bstack_utils.bstack11ll1111l11_opy_ import bstack11ll11111l1_opy_
from bstack_utils.constants import bstack11l1l1ll11l_opy_
from bstack_utils.helper import get_host_info, bstack111ll111l11_opy_
class bstack111l111llll_opy_:
    bstack1ll11ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡉࡣࡱࡨࡱ࡫ࡳࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡷࡼࡥࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ⁙")
    def __init__(self, config, logger):
        bstack1ll11ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡤࡪࡥࡷ࠰ࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡧࡴࡴࡦࡪࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡣࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡴࡶࡵ࠰ࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿࠠ࡯ࡣࡰࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⁚")
        self.config = config
        self.logger = logger
        self.bstack1lllll11111l_opy_ = bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡱ࡮࡬ࡸ࠲ࡺࡥࡴࡶࡶࠦ⁛")
        self.bstack1llll1lllll1_opy_ = None
        self.bstack1lllll111l1l_opy_ = 60
        self.bstack1lllll111l11_opy_ = 5
        self.bstack1lllll111111_opy_ = 0
    def bstack111l1111lll_opy_(self, test_files, orchestration_strategy, bstack111l111l11l_opy_={}):
        bstack1ll11ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡊࡰ࡬ࡸ࡮ࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡸࡥࡲࡷࡨࡷࡹࠦࡡ࡯ࡦࠣࡷࡹࡵࡲࡦࡵࠣࡸ࡭࡫ࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡵࡵ࡬࡭࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⁜")
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡍࡳ࡯ࡴࡪࡣࡷ࡭ࡳ࡭ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡽࡩࡵࡪࠣࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡻࡾࠤ⁝").format(orchestration_strategy))
        try:
            bstack1111ll11ll1_opy_ = []
            if bstack111l111l11l_opy_[bstack1ll11ll_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫ⁞")].get(bstack1ll11ll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ "), False): # check if bstack1llll1lll1l1_opy_ bstack1llll1lll1ll_opy_ is enabled
                bstack1111l1lll11_opy_ = bstack111l111l11l_opy_[bstack1ll11ll_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭⁠")].get(bstack1ll11ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ⁡"), []) # for multi-repo
                bstack1111ll11ll1_opy_ = bstack111ll111l11_opy_(bstack1111l1lll11_opy_) # bstack111ll11ll1l_opy_-repo is handled bstack1111l1llll1_opy_
            payload = {
                bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ⁢"): [{bstack1ll11ll_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧ⁣"): f} for f in test_files],
                bstack1ll11ll_opy_ (u"ࠦࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡹࡸࡡࡵࡧࡪࡽࠧ⁤"): orchestration_strategy,
                bstack1ll11ll_opy_ (u"ࠧࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡒ࡫ࡴࡢࡦࡤࡸࡦࠨ⁥"): bstack111l111l11l_opy_,
                bstack1ll11ll_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤ⁦"): int(os.environ.get(bstack1ll11ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥ⁧")) or bstack1ll11ll_opy_ (u"ࠣ࠲ࠥ⁨")),
                bstack1ll11ll_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨ⁩"): int(os.environ.get(bstack1ll11ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ⁪")) or bstack1ll11ll_opy_ (u"ࠦ࠶ࠨ⁫")),
                bstack1ll11ll_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥ⁬"): self.config.get(bstack1ll11ll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ⁭"), bstack1ll11ll_opy_ (u"ࠧࠨ⁮")),
                bstack1ll11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦ⁯"): self.config.get(bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ⁰"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣⁱ"): self.config.get(bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⁲"), bstack1ll11ll_opy_ (u"ࠬ࠭⁳")),
                bstack1ll11ll_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣ⁴"): get_host_info(),
                bstack1ll11ll_opy_ (u"ࠢࡱࡴࡇࡩࡹࡧࡩ࡭ࡵࠥ⁵"): bstack1111ll11ll1_opy_
            }
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤ⁶").format(payload))
            response = bstack11ll11111l1_opy_.bstack1llllll11lll_opy_(self.bstack1lllll11111l_opy_, payload)
            if response:
                self.bstack1llll1lllll1_opy_ = self._1lllll1111ll_opy_(response)
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡕࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⁷").format(self.bstack1llll1lllll1_opy_))
            else:
                self.logger.error(bstack1ll11ll_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠰ࠥ⁸"))
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺࠻ࠢࡾࢁࠧ⁹").format(e))
    def _1lllll1111ll_opy_(self, response):
        bstack1ll11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡡ࡯ࡦࠣࡩࡽࡺࡲࡢࡥࡷࡷࠥࡸࡥ࡭ࡧࡹࡥࡳࡺࠠࡧ࡫ࡨࡰࡩࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⁺")
        bstack1llll111ll_opy_ = {}
        bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ⁻")] = response.get(bstack1ll11ll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ⁼"), self.bstack1lllll111l1l_opy_)
        bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ⁽")] = response.get(bstack1ll11ll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ⁾"), self.bstack1lllll111l11_opy_)
        bstack1llll1llll1l_opy_ = response.get(bstack1ll11ll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨⁿ"))
        bstack1lllll1111l1_opy_ = response.get(bstack1ll11ll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ₀"))
        if bstack1llll1llll1l_opy_:
            bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ₁")] = bstack1llll1llll1l_opy_.split(bstack11l1l1ll11l_opy_ + bstack1ll11ll_opy_ (u"ࠨ࠯ࠣ₂"))[1] if bstack11l1l1ll11l_opy_ + bstack1ll11ll_opy_ (u"ࠢ࠰ࠤ₃") in bstack1llll1llll1l_opy_ else bstack1llll1llll1l_opy_
        else:
            bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ₄")] = None
        if bstack1lllll1111l1_opy_:
            bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ₅")] = bstack1lllll1111l1_opy_.split(bstack11l1l1ll11l_opy_ + bstack1ll11ll_opy_ (u"ࠥ࠳ࠧ₆"))[1] if bstack11l1l1ll11l_opy_ + bstack1ll11ll_opy_ (u"ࠦ࠴ࠨ₇") in bstack1lllll1111l1_opy_ else bstack1lllll1111l1_opy_
        else:
            bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ₈")] = None
        if (
            response.get(bstack1ll11ll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ₉")) is None or
            response.get(bstack1ll11ll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ₊")) is None or
            response.get(bstack1ll11ll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ₋")) is None or
            response.get(bstack1ll11ll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ₌")) is None
        ):
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥ࡟ࡵࡸ࡯ࡤࡧࡶࡷࡤࡹࡰ࡭࡫ࡷࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡹࡰࡰࡰࡶࡩࡢࠦࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡰࡸࡰࡱࠦࡶࡢ࡮ࡸࡩ࠭ࡹࠩࠡࡨࡲࡶࠥࡹ࡯࡮ࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡹࠠࡪࡰࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ₍"))
        return bstack1llll111ll_opy_
    def bstack111l111lll1_opy_(self):
        if not self.bstack1llll1lllll1_opy_:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡔ࡯ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡧࡥࡹࡧࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠱ࠦ₎"))
            return None
        bstack1llll1lll11l_opy_ = None
        test_files = []
        bstack1llll1lll111_opy_ = int(time.time() * 1000) # bstack1llll1llll11_opy_ sec
        bstack1llll1ll1lll_opy_ = int(self.bstack1llll1lllll1_opy_.get(bstack1ll11ll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ₏"), self.bstack1lllll111l11_opy_))
        bstack1llll1llllll_opy_ = int(self.bstack1llll1lllll1_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢₐ"), self.bstack1lllll111l1l_opy_)) * 1000
        bstack1lllll1111l1_opy_ = self.bstack1llll1lllll1_opy_.get(bstack1ll11ll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦₑ"), None)
        bstack1llll1llll1l_opy_ = self.bstack1llll1lllll1_opy_.get(bstack1ll11ll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦₒ"), None)
        if bstack1llll1llll1l_opy_ is None and bstack1lllll1111l1_opy_ is None:
            return None
        try:
            while bstack1llll1llll1l_opy_ and (time.time() * 1000 - bstack1llll1lll111_opy_) < bstack1llll1llllll_opy_:
                response = bstack11ll11111l1_opy_.bstack1llllll1111l_opy_(bstack1llll1llll1l_opy_, {})
                if response and response.get(bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣₓ")):
                    bstack1llll1lll11l_opy_ = response.get(bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤₔ"))
                self.bstack1lllll111111_opy_ += 1
                if bstack1llll1lll11l_opy_:
                    break
                time.sleep(bstack1llll1ll1lll_opy_)
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡌࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡧࡴࡲࡱࠥࡸࡥࡴࡷ࡯ࡸ࡛ࠥࡒࡍࠢࡤࡪࡹ࡫ࡲࠡࡹࡤ࡭ࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡻࡾࠢࡶࡩࡨࡵ࡮ࡥࡵ࠱ࠦₕ").format(bstack1llll1ll1lll_opy_))
            if bstack1lllll1111l1_opy_ and not bstack1llll1lll11l_opy_:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡆࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡨࡵࡳࡲࠦࡴࡪ࡯ࡨࡳࡺࡺࠠࡖࡔࡏࠦₖ"))
                response = bstack11ll11111l1_opy_.bstack1llllll1111l_opy_(bstack1lllll1111l1_opy_, {})
                if response and response.get(bstack1ll11ll_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧₗ")):
                    bstack1llll1lll11l_opy_ = response.get(bstack1ll11ll_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨₘ"))
            if bstack1llll1lll11l_opy_ and len(bstack1llll1lll11l_opy_) > 0:
                for bstack111lll1111_opy_ in bstack1llll1lll11l_opy_:
                    file_path = bstack111lll1111_opy_.get(bstack1ll11ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥₙ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1llll1lll11l_opy_:
                return None
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡓࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡴࡨࡧࡪ࡯ࡶࡦࡦ࠽ࠤࢀࢃࠢₚ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽ࠤࢀࢃࠢₛ").format(e))
            return None
    def bstack111l1111l1l_opy_(self):
        bstack1ll11ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡧࡦࡲ࡬ࡴࠢࡰࡥࡩ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧₜ")
        return self.bstack1lllll111111_opy_