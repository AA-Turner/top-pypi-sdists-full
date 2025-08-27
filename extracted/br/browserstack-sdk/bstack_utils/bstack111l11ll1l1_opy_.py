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
import time
from bstack_utils.bstack11ll111llll_opy_ import bstack11ll11l1ll1_opy_
from bstack_utils.constants import bstack11l1ll11111_opy_
from bstack_utils.helper import get_host_info, bstack11l11ll1lll_opy_
class bstack111l1l11l11_opy_:
    bstack1111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡌࡦࡴࡤ࡭ࡧࡶࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡹࡥࡳࡸࡨࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ⁕")
    def __init__(self, config, logger):
        bstack1111lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡧ࡭ࡨࡺࠬࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡣࡰࡰࡩ࡭࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࡟ࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡷࡹࡸࠬࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡵࡷࡶࡦࡺࡥࡨࡻࠣࡲࡦࡳࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⁖")
        self.config = config
        self.logger = logger
        self.bstack1lllll111l1l_opy_ = bstack1111lll_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡴࡱ࡯ࡴ࠮ࡶࡨࡷࡹࡹࠢ⁗")
        self.bstack1lllll111ll1_opy_ = None
        self.bstack1lllll111l11_opy_ = 60
        self.bstack1lllll111111_opy_ = 5
        self.bstack1lllll11l1ll_opy_ = 0
    def bstack111l11ll1ll_opy_(self, test_files, orchestration_strategy, bstack111l11llll1_opy_={}):
        bstack1111lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡍࡳ࡯ࡴࡪࡣࡷࡩࡸࠦࡴࡩࡧࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡤࡲࡩࠦࡳࡵࡱࡵࡩࡸࠦࡴࡩࡧࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡱࡱ࡯ࡰ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⁘")
        self.logger.debug(bstack1111lll_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡩ࡯ࡩࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡹ࡬ࡸ࡭ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡾࢁࠧ⁙").format(orchestration_strategy))
        try:
            bstack111l111llll_opy_ = []
            if bstack111l11llll1_opy_[bstack1111lll_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ⁚")].get(bstack1111lll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ⁛"), False): # check if bstack1lllll11l11l_opy_ bstack1lllll111lll_opy_ is enabled
                bstack111l11111l1_opy_ = bstack111l11llll1_opy_[bstack1111lll_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ⁜")].get(bstack1111lll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ⁝"), []) # for multi-repo
                bstack111l111llll_opy_ = bstack11l11ll1lll_opy_(bstack111l11111l1_opy_) # bstack11l111111l1_opy_-repo is handled bstack111l11111ll_opy_
            payload = {
                bstack1111lll_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ⁞"): [{bstack1111lll_opy_ (u"ࠨࡦࡪ࡮ࡨࡔࡦࡺࡨࠣ "): f} for f in test_files],
                bstack1111lll_opy_ (u"ࠢࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡓࡵࡴࡤࡸࡪ࡭ࡹࠣ⁠"): orchestration_strategy,
                bstack1111lll_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡎࡧࡷࡥࡩࡧࡴࡢࠤ⁡"): bstack111l11llll1_opy_,
                bstack1111lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧ⁢"): int(os.environ.get(bstack1111lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨ⁣")) or bstack1111lll_opy_ (u"ࠦ࠵ࠨ⁤")),
                bstack1111lll_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤ⁥"): int(os.environ.get(bstack1111lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣ⁦")) or bstack1111lll_opy_ (u"ࠢ࠲ࠤ⁧")),
                bstack1111lll_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨ⁨"): self.config.get(bstack1111lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⁩"), bstack1111lll_opy_ (u"ࠪࠫ⁪")),
                bstack1111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢ⁫"): self.config.get(bstack1111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ⁬"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ⁭"): self.config.get(bstack1111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⁮"), bstack1111lll_opy_ (u"ࠨࠩ⁯")),
                bstack1111lll_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦ⁰"): get_host_info(),
                bstack1111lll_opy_ (u"ࠥࡴࡷࡊࡥࡵࡣ࡬ࡰࡸࠨⁱ"): bstack111l111llll_opy_
            }
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻ࠢࡾࢁࠧ⁲").format(payload))
            response = bstack11ll11l1ll1_opy_.bstack1llllll11l1l_opy_(self.bstack1lllll111l1l_opy_, payload)
            if response:
                self.bstack1lllll111ll1_opy_ = self._1lllll11l111_opy_(response)
                self.logger.debug(bstack1111lll_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⁳").format(self.bstack1lllll111ll1_opy_))
            else:
                self.logger.error(bstack1111lll_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠳ࠨ⁴"))
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽࠾ࠥࢁࡽࠣ⁵").format(e))
    def _1lllll11l111_opy_(self, response):
        bstack1111lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡤࡲࡩࠦࡥࡹࡶࡵࡥࡨࡺࡳࠡࡴࡨࡰࡪࡼࡡ࡯ࡶࠣࡪ࡮࡫࡬ࡥࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⁶")
        bstack1l1111llll_opy_ = {}
        bstack1l1111llll_opy_[bstack1111lll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ⁷")] = response.get(bstack1111lll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ⁸"), self.bstack1lllll111l11_opy_)
        bstack1l1111llll_opy_[bstack1111lll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ⁹")] = response.get(bstack1111lll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ⁺"), self.bstack1lllll111111_opy_)
        bstack1lllll1111l1_opy_ = response.get(bstack1111lll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ⁻"))
        bstack1llll1lllll1_opy_ = response.get(bstack1111lll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ⁼"))
        if bstack1lllll1111l1_opy_:
            bstack1l1111llll_opy_[bstack1111lll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ⁽")] = bstack1lllll1111l1_opy_.split(bstack11l1ll11111_opy_ + bstack1111lll_opy_ (u"ࠤ࠲ࠦ⁾"))[1] if bstack11l1ll11111_opy_ + bstack1111lll_opy_ (u"ࠥ࠳ࠧⁿ") in bstack1lllll1111l1_opy_ else bstack1lllll1111l1_opy_
        else:
            bstack1l1111llll_opy_[bstack1111lll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ₀")] = None
        if bstack1llll1lllll1_opy_:
            bstack1l1111llll_opy_[bstack1111lll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ₁")] = bstack1llll1lllll1_opy_.split(bstack11l1ll11111_opy_ + bstack1111lll_opy_ (u"ࠨ࠯ࠣ₂"))[1] if bstack11l1ll11111_opy_ + bstack1111lll_opy_ (u"ࠢ࠰ࠤ₃") in bstack1llll1lllll1_opy_ else bstack1llll1lllll1_opy_
        else:
            bstack1l1111llll_opy_[bstack1111lll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ₄")] = None
        if (
            response.get(bstack1111lll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ₅")) is None or
            response.get(bstack1111lll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ₆")) is None or
            response.get(bstack1111lll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ₇")) is None or
            response.get(bstack1111lll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ₈")) is None
        ):
            self.logger.debug(bstack1111lll_opy_ (u"ࠨ࡛ࡱࡴࡲࡧࡪࡹࡳࡠࡵࡳࡰ࡮ࡺ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡵࡳࡳࡳࡹࡥ࡞ࠢࡕࡩࡨ࡫ࡩࡷࡧࡧࠤࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥࠩࡵࠬࠤ࡫ࡵࡲࠡࡵࡲࡱࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦࡵࠣ࡭ࡳࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ₉"))
        return bstack1l1111llll_opy_
    def bstack111l11ll11l_opy_(self):
        if not self.bstack1lllll111ll1_opy_:
            self.logger.error(bstack1111lll_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸ࠴ࠢ₊"))
            return None
        bstack1llll1llllll_opy_ = None
        test_files = []
        bstack1lllll11l1l1_opy_ = int(time.time() * 1000) # bstack1lllll11111l_opy_ sec
        bstack1llll1llll1l_opy_ = int(self.bstack1lllll111ll1_opy_.get(bstack1111lll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ₋"), self.bstack1lllll111111_opy_))
        bstack1lllll1111ll_opy_ = int(self.bstack1lllll111ll1_opy_.get(bstack1111lll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ₌"), self.bstack1lllll111l11_opy_)) * 1000
        bstack1llll1lllll1_opy_ = self.bstack1lllll111ll1_opy_.get(bstack1111lll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ₍"), None)
        bstack1lllll1111l1_opy_ = self.bstack1lllll111ll1_opy_.get(bstack1111lll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ₎"), None)
        if bstack1lllll1111l1_opy_ is None and bstack1llll1lllll1_opy_ is None:
            return None
        try:
            while bstack1lllll1111l1_opy_ and (time.time() * 1000 - bstack1lllll11l1l1_opy_) < bstack1lllll1111ll_opy_:
                response = bstack11ll11l1ll1_opy_.bstack1llllll1l1l1_opy_(bstack1lllll1111l1_opy_, {})
                if response and response.get(bstack1111lll_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ₏")):
                    bstack1llll1llllll_opy_ = response.get(bstack1111lll_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧₐ"))
                self.bstack1lllll11l1ll_opy_ += 1
                if bstack1llll1llllll_opy_:
                    break
                time.sleep(bstack1llll1llll1l_opy_)
                self.logger.debug(bstack1111lll_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡴࡨࡷࡺࡲࡴࠡࡗࡕࡐࠥࡧࡦࡵࡧࡵࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡾࢁࠥࡹࡥࡤࡱࡱࡨࡸ࠴ࠢₑ").format(bstack1llll1llll1l_opy_))
            if bstack1llll1lllll1_opy_ and not bstack1llll1llllll_opy_:
                self.logger.debug(bstack1111lll_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡭ࡲ࡫࡯ࡶࡶ࡙ࠣࡗࡒࠢₒ"))
                response = bstack11ll11l1ll1_opy_.bstack1llllll1l1l1_opy_(bstack1llll1lllll1_opy_, {})
                if response and response.get(bstack1111lll_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣₓ")):
                    bstack1llll1llllll_opy_ = response.get(bstack1111lll_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤₔ"))
            if bstack1llll1llllll_opy_ and len(bstack1llll1llllll_opy_) > 0:
                for bstack111ll1lll1_opy_ in bstack1llll1llllll_opy_:
                    file_path = bstack111ll1lll1_opy_.get(bstack1111lll_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨₕ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1llll1llllll_opy_:
                return None
            self.logger.debug(bstack1111lll_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡏࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡷ࡫ࡣࡦ࡫ࡹࡩࡩࡀࠠࡼࡿࠥₖ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥₗ").format(e))
            return None
    def bstack111l11lllll_opy_(self):
        bstack1111lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡣࡢ࡮࡯ࡷࠥࡳࡡࡥࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣₘ")
        return self.bstack1lllll11l1ll_opy_