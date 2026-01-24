# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import time
from bstack_utils.bstack11l11lllll1_opy_ import bstack11l11lll11l_opy_
from bstack_utils.constants import bstack11l11111lll_opy_
from bstack_utils.helper import get_host_info, bstack111ll1l1l1l_opy_
class bstack11111ll1l1l_opy_:
    bstack1l1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡉࡣࡱࡨࡱ࡫ࡳࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡷࡼࡥࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ⇯")
    def __init__(self, config, logger):
        bstack1l1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡤࡪࡥࡷ࠰ࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡧࡴࡴࡦࡪࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡣࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡴࡶࡵ࠰ࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿࠠ࡯ࡣࡰࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⇰")
        self.config = config
        self.logger = logger
        self.bstack1lll1l1l1ll1_opy_ = bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡱ࡮࡬ࡸ࠲ࡺࡥࡴࡶࡶࠦ⇱")
        self.bstack1lll1l1l11ll_opy_ = None
        self.bstack1lll1l1l1lll_opy_ = 60
        self.bstack1lll1l1l1l1l_opy_ = 5
        self.bstack1lll1l11ll11_opy_ = 0
    def bstack11111llll11_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡊࡰ࡬ࡸ࡮ࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡸࡥࡲࡷࡨࡷࡹࠦࡡ࡯ࡦࠣࡷࡹࡵࡲࡦࡵࠣࡸ࡭࡫ࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡵࡵ࡬࡭࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⇲")
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡍࡳ࡯ࡴࡪࡣࡷ࡭ࡳ࡭ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡽࡩࡵࡪࠣࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡻࡾࠤ⇳").format(orchestration_strategy))
        try:
            bstack1lll1l11l1l1_opy_ = []
            bstack1l1111_opy_ (u"ࠧࠨࠢࡘࡧࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥ࡬ࡥࡵࡥ࡫ࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣ࡭ࡸࠦࡳࡰࡷࡵࡧࡪࠦࡩࡴࠢࡷࡽࡵ࡫ࠠࡰࡨࠣࡥࡷࡸࡡࡺࠢࡤࡲࡩࠦࡩࡵࠩࡶࠤࡪࡲࡥ࡮ࡧࡱࡸࡸࠦࡡࡳࡧࠣࡳ࡫ࠦࡴࡺࡲࡨࠤࡩ࡯ࡣࡵࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡧࡦࡥࡺࡹࡥࠡ࡫ࡱࠤࡹ࡮ࡡࡵࠢࡦࡥࡸ࡫ࠬࠡࡷࡶࡩࡷࠦࡨࡢࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡳࡵ࡭ࡶ࡬࠱ࡷ࡫ࡰࡰࠢࡶࡳࡺࡸࡣࡦࠢࡺ࡭ࡹ࡮ࠠࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠠࡪࡰࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤࠥࠦ⇴")
            source = orchestration_metadata[bstack1l1111_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ⇵")].get(bstack1l1111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ⇶"), [])
            bstack1lll1l1ll1l1_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1l1111_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ⇷")].get(bstack1l1111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ⇸"), False) and not bstack1lll1l1ll1l1_opy_:
                bstack1lll1l11l1l1_opy_ = bstack111ll1l1l1l_opy_(source) # bstack1lll1l1l1l11_opy_-repo is handled bstack1lll1l11ll1l_opy_
            payload = {
                bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ⇹"): [{bstack1l1111_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ⇺"): f} for f in test_files],
                bstack1l1111_opy_ (u"ࠧࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡘࡺࡲࡢࡶࡨ࡫ࡾࠨ⇻"): orchestration_strategy,
                bstack1l1111_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡓࡥࡵࡣࡧࡥࡹࡧࠢ⇼"): orchestration_metadata,
                bstack1l1111_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ⇽"): int(os.environ.get(bstack1l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ⇾")) or bstack1l1111_opy_ (u"ࠤ࠳ࠦ⇿")),
                bstack1l1111_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ∀"): int(os.environ.get(bstack1l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ∁")) or bstack1l1111_opy_ (u"ࠧ࠷ࠢ∂")),
                bstack1l1111_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ∃"): self.config.get(bstack1l1111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ∄"), bstack1l1111_opy_ (u"ࠨࠩ∅")),
                bstack1l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ∆"): self.config.get(bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭∇"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ∈"): os.environ.get(bstack1l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦ∉"), bstack1l1111_opy_ (u"ࠨࠢ∊")),
                bstack1l1111_opy_ (u"ࠢࡩࡱࡶࡸࡎࡴࡦࡰࠤ∋"): get_host_info(),
                bstack1l1111_opy_ (u"ࠣࡲࡵࡈࡪࡺࡡࡪ࡮ࡶࠦ∌"): bstack1lll1l11l1l1_opy_
            }
            self.logger.debug(bstack1l1111_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥ∍").format(payload))
            response = bstack11l11lll11l_opy_.bstack1lll1llll111_opy_(self.bstack1lll1l1l1ll1_opy_, payload)
            if response:
                self.bstack1lll1l1l11ll_opy_ = self._1lll1l1ll11l_opy_(response)
                self.logger.debug(bstack1l1111_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ∎").format(self.bstack1lll1l1l11ll_opy_))
            else:
                self.logger.error(bstack1l1111_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦ∏"))
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻࠼ࠣࡿࢂࠨ∐").format(e))
    def _1lll1l1ll11l_opy_(self, response):
        bstack1l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡢࡰࡧࠤࡪࡾࡴࡳࡣࡦࡸࡸࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡨ࡬ࡩࡱࡪࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ∑")
        bstack1ll11l1l1_opy_ = {}
        bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ−")] = response.get(bstack1l1111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ∓"), self.bstack1lll1l1l1lll_opy_)
        bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ∔")] = response.get(bstack1l1111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ∕"), self.bstack1lll1l1l1l1l_opy_)
        bstack1lll1l11llll_opy_ = response.get(bstack1l1111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ∖"))
        bstack1lll1l11lll1_opy_ = response.get(bstack1l1111_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ∗"))
        if bstack1lll1l11llll_opy_:
            bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ∘")] = bstack1lll1l11llll_opy_.split(bstack11l11111lll_opy_ + bstack1l1111_opy_ (u"ࠢ࠰ࠤ∙"))[1] if bstack11l11111lll_opy_ + bstack1l1111_opy_ (u"ࠣ࠱ࠥ√") in bstack1lll1l11llll_opy_ else bstack1lll1l11llll_opy_
        else:
            bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ∛")] = None
        if bstack1lll1l11lll1_opy_:
            bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ∜")] = bstack1lll1l11lll1_opy_.split(bstack11l11111lll_opy_ + bstack1l1111_opy_ (u"ࠦ࠴ࠨ∝"))[1] if bstack11l11111lll_opy_ + bstack1l1111_opy_ (u"ࠧ࠵ࠢ∞") in bstack1lll1l11lll1_opy_ else bstack1lll1l11lll1_opy_
        else:
            bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ∟")] = None
        if (
            response.get(bstack1l1111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ∠")) is None or
            response.get(bstack1l1111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ∡")) is None or
            response.get(bstack1l1111_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ∢")) is None or
            response.get(bstack1l1111_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ∣")) is None
        ):
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡠࡶࡲࡰࡥࡨࡷࡸࡥࡳࡱ࡮࡬ࡸࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡳࡱࡱࡱࡷࡪࡣࠠࡓࡧࡦࡩ࡮ࡼࡥࡥࠢࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠮ࡳࠪࠢࡩࡳࡷࠦࡳࡰ࡯ࡨࠤࡦࡺࡴࡳ࡫ࡥࡹࡹ࡫ࡳࠡ࡫ࡱࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣ∤"))
        return bstack1ll11l1l1_opy_
    def bstack1111l111111_opy_(self):
        if not self.bstack1lll1l1l11ll_opy_:
            self.logger.error(bstack1l1111_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠲ࠧ∥"))
            return None
        bstack1lll1l1l11l1_opy_ = None
        test_files = []
        bstack1lll1l1ll111_opy_ = int(time.time() * 1000) # bstack1lll1l1l111l_opy_ sec
        bstack1lll1l11l1ll_opy_ = int(self.bstack1lll1l1l11ll_opy_.get(bstack1l1111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ∦"), self.bstack1lll1l1l1l1l_opy_))
        bstack1lll1l1l1111_opy_ = int(self.bstack1lll1l1l11ll_opy_.get(bstack1l1111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ∧"), self.bstack1lll1l1l1lll_opy_)) * 1000
        bstack1lll1l11lll1_opy_ = self.bstack1lll1l1l11ll_opy_.get(bstack1l1111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ∨"), None)
        bstack1lll1l11llll_opy_ = self.bstack1lll1l1l11ll_opy_.get(bstack1l1111_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ∩"), None)
        if bstack1lll1l11llll_opy_ is None and bstack1lll1l11lll1_opy_ is None:
            return None
        try:
            while bstack1lll1l11llll_opy_ and (time.time() * 1000 - bstack1lll1l1ll111_opy_) < bstack1lll1l1l1111_opy_:
                response = bstack11l11lll11l_opy_.bstack1lll1lll1l11_opy_(bstack1lll1l11llll_opy_, {})
                if response and response.get(bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ∪")):
                    bstack1lll1l1l11l1_opy_ = response.get(bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ∫"))
                self.bstack1lll1l11ll11_opy_ += 1
                if bstack1lll1l1l11l1_opy_:
                    break
                time.sleep(bstack1lll1l11l1ll_opy_)
                self.logger.debug(bstack1l1111_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡆࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡨࡵࡳࡲࠦࡲࡦࡵࡸࡰࡹࠦࡕࡓࡎࠣࡥ࡫ࡺࡥࡳࠢࡺࡥ࡮ࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡼࡿࠣࡷࡪࡩ࡯࡯ࡦࡶ࠲ࠧ∬").format(bstack1lll1l11l1ll_opy_))
            if bstack1lll1l11lll1_opy_ and not bstack1lll1l1l11l1_opy_:
                self.logger.debug(bstack1l1111_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡵ࡫ࡰࡩࡴࡻࡴࠡࡗࡕࡐࠧ∭"))
                response = bstack11l11lll11l_opy_.bstack1lll1lll1l11_opy_(bstack1lll1l11lll1_opy_, {})
                if response and response.get(bstack1l1111_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ∮")):
                    bstack1lll1l1l11l1_opy_ = response.get(bstack1l1111_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ∯"))
            if bstack1lll1l1l11l1_opy_ and len(bstack1lll1l1l11l1_opy_) > 0:
                for bstack1111ll1lll_opy_ in bstack1lll1l1l11l1_opy_:
                    file_path = bstack1111ll1lll_opy_.get(bstack1l1111_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦ∰"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lll1l1l11l1_opy_:
                return None
            self.logger.debug(bstack1l1111_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡔࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡵࡩࡨ࡫ࡩࡷࡧࡧ࠾ࠥࢁࡽࠣ∱").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾ࠥࢁࡽࠣ∲").format(e))
            return None
    def bstack11111ll1ll1_opy_(self):
        bstack1l1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡨࡧ࡬࡭ࡵࠣࡱࡦࡪࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ∳")
        return self.bstack1lll1l11ll11_opy_