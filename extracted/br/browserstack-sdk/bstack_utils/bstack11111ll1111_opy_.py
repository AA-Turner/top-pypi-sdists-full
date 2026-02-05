# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import time
from bstack_utils.bstack11l11ll1l1l_opy_ import bstack11l11lll1l1_opy_
from bstack_utils.constants import bstack11l1111ll1l_opy_
from bstack_utils.helper import get_host_info, bstack111ll1ll1l1_opy_
class bstack11111lll1l1_opy_:
    bstack11l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡍࡧ࡮ࡥ࡮ࡨࡷࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡴࡹࡩࡷ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ⇳")
    def __init__(self, config, logger):
        bstack11l1ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡨ࡮ࡩࡴ࠭ࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡤࡱࡱࡪ࡮࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡠࡵࡷࡶࡦࡺࡥࡨࡻ࠽ࠤࡸࡺࡲ࠭ࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡶࡸࡷࡧࡴࡦࡩࡼࠤࡳࡧ࡭ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⇴")
        self.config = config
        self.logger = logger
        self.bstack1lll1l11llll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡵࡲࡩࡵ࠯ࡷࡩࡸࡺࡳࠣ⇵")
        self.bstack1lll1l11l11l_opy_ = None
        self.bstack1lll1l11ll11_opy_ = 60
        self.bstack1lll1l11ll1l_opy_ = 5
        self.bstack1lll1l1l1111_opy_ = 0
    def bstack11111ll11ll_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack11l1ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡎࡴࡩࡵ࡫ࡤࡸࡪࡹࠠࡵࡪࡨࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡶࡻࡥࡴࡶࠣࡥࡳࡪࠠࡴࡶࡲࡶࡪࡹࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡲࡲࡰࡱ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⇶")
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡊࡰ࡬ࡸ࡮ࡧࡴࡪࡰࡪࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡺ࡭ࡹ࡮ࠠࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡿࢂࠨ⇷").format(orchestration_strategy))
        try:
            bstack1lll1l1l111l_opy_ = []
            bstack11l1ll1_opy_ (u"ࠤࠥࠦ࡜࡫ࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡩࡩࡹࡩࡨࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡪࡵࠣࡷࡴࡻࡲࡤࡧࠣ࡭ࡸࠦࡴࡺࡲࡨࠤࡴ࡬ࠠࡢࡴࡵࡥࡾࠦࡡ࡯ࡦࠣ࡭ࡹ࠭ࡳࠡࡧ࡯ࡩࡲ࡫࡮ࡵࡵࠣࡥࡷ࡫ࠠࡰࡨࠣࡸࡾࡶࡥࠡࡦ࡬ࡧࡹࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧ࡫ࡣࡢࡷࡶࡩࠥ࡯࡮ࠡࡶ࡫ࡥࡹࠦࡣࡢࡵࡨ࠰ࠥࡻࡳࡦࡴࠣ࡬ࡦࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡰࡹࡱࡺࡩ࠮ࡴࡨࡴࡴࠦࡳࡰࡷࡵࡧࡪࠦࡷࡪࡶ࡫ࠤ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠤ࡮ࡴࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨࠢࠣ⇸")
            source = orchestration_metadata[bstack11l1ll1_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ⇹")].get(bstack11l1ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ⇺"), [])
            bstack1lll1l11l111_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack11l1ll1_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫ⇻")].get(bstack11l1ll1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ⇼"), False) and not bstack1lll1l11l111_opy_:
                bstack1lll1l1l111l_opy_ = bstack111ll1ll1l1_opy_(source) # bstack1lll1l111lll_opy_-repo is handled bstack1lll1l1l11ll_opy_
            payload = {
                bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ⇽"): [{bstack11l1ll1_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥ⇾"): f} for f in test_files],
                bstack11l1ll1_opy_ (u"ࠤࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡕࡷࡶࡦࡺࡥࡨࡻࠥ⇿"): orchestration_strategy,
                bstack11l1ll1_opy_ (u"ࠥࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡐࡩࡹࡧࡤࡢࡶࡤࠦ∀"): orchestration_metadata,
                bstack11l1ll1_opy_ (u"ࠦࡳࡵࡤࡦࡋࡱࡨࡪࡾࠢ∁"): int(os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣ∂")) or bstack11l1ll1_opy_ (u"ࠨ࠰ࠣ∃")),
                bstack11l1ll1_opy_ (u"ࠢࡵࡱࡷࡥࡱࡔ࡯ࡥࡧࡶࠦ∄"): int(os.environ.get(bstack11l1ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡑࡗࡅࡑࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥ∅")) or bstack11l1ll1_opy_ (u"ࠤ࠴ࠦ∆")),
                bstack11l1ll1_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣ∇"): self.config.get(bstack11l1ll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ∈"), bstack11l1ll1_opy_ (u"ࠬ࠭∉")),
                bstack11l1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤ∊"): self.config.get(bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ∋"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11l1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨ∌"): os.environ.get(bstack11l1ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠣ∍"), bstack11l1ll1_opy_ (u"ࠥࠦ∎")),
                bstack11l1ll1_opy_ (u"ࠦ࡭ࡵࡳࡵࡋࡱࡪࡴࠨ∏"): get_host_info(),
                bstack11l1ll1_opy_ (u"ࠧࡶࡲࡅࡧࡷࡥ࡮ࡲࡳࠣ∐"): bstack1lll1l1l111l_opy_
            }
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡ࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽ࠤࢀࢃࠢ∑").format(payload))
            response = bstack11l11lll1l1_opy_.bstack1lll1lll111l_opy_(self.bstack1lll1l11llll_opy_, payload)
            if response:
                self.bstack1lll1l11l11l_opy_ = self._1lll1l11l1l1_opy_(response)
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡓࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ−").format(self.bstack1lll1l11l11l_opy_))
            else:
                self.logger.error(bstack11l1ll1_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠮ࠣ∓"))
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࡀࠠࡼࡿࠥ∔").format(e))
    def _1lll1l11l1l1_opy_(self, response):
        bstack11l1ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡇࡐࡊࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡦࡴࡤࠡࡧࡻࡸࡷࡧࡣࡵࡵࠣࡶࡪࡲࡥࡷࡣࡱࡸࠥ࡬ࡩࡦ࡮ࡧࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ∕")
        bstack111l1l11l1_opy_ = {}
        bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ∖")] = response.get(bstack11l1ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ∗"), self.bstack1lll1l11ll11_opy_)
        bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ∘")] = response.get(bstack11l1ll1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ∙"), self.bstack1lll1l11ll1l_opy_)
        bstack1lll1l11lll1_opy_ = response.get(bstack11l1ll1_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ√"))
        bstack1lll1l111l1l_opy_ = response.get(bstack11l1ll1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ∛"))
        if bstack1lll1l11lll1_opy_:
            bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ∜")] = bstack1lll1l11lll1_opy_.split(bstack11l1111ll1l_opy_ + bstack11l1ll1_opy_ (u"ࠦ࠴ࠨ∝"))[1] if bstack11l1111ll1l_opy_ + bstack11l1ll1_opy_ (u"ࠧ࠵ࠢ∞") in bstack1lll1l11lll1_opy_ else bstack1lll1l11lll1_opy_
        else:
            bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ∟")] = None
        if bstack1lll1l111l1l_opy_:
            bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ∠")] = bstack1lll1l111l1l_opy_.split(bstack11l1111ll1l_opy_ + bstack11l1ll1_opy_ (u"ࠣ࠱ࠥ∡"))[1] if bstack11l1111ll1l_opy_ + bstack11l1ll1_opy_ (u"ࠤ࠲ࠦ∢") in bstack1lll1l111l1l_opy_ else bstack1lll1l111l1l_opy_
        else:
            bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ∣")] = None
        if (
            response.get(bstack11l1ll1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ∤")) is None or
            response.get(bstack11l1ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ∥")) is None or
            response.get(bstack11l1ll1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ∦")) is None or
            response.get(bstack11l1ll1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ∧")) is None
        ):
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣ࡝ࡳࡶࡴࡩࡥࡴࡵࡢࡷࡵࡲࡩࡵࡡࡷࡩࡸࡺࡳࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࡠࠤࡗ࡫ࡣࡦ࡫ࡹࡩࡩࠦ࡮ࡶ࡮࡯ࠤࡻࡧ࡬ࡶࡧࠫࡷ࠮ࠦࡦࡰࡴࠣࡷࡴࡳࡥࠡࡣࡷࡸࡷ࡯ࡢࡶࡶࡨࡷࠥ࡯࡮ࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧ∨"))
        return bstack111l1l11l1_opy_
    def bstack11111ll1l11_opy_(self):
        if not self.bstack1lll1l11l11l_opy_:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡒࡴࠦࡲࡦࡳࡸࡩࡸࡺࠠࡥࡣࡷࡥࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠯ࠤ∩"))
            return None
        bstack1lll1l111ll1_opy_ = None
        test_files = []
        bstack1lll1l1111ll_opy_ = int(time.time() * 1000) # bstack1lll1l1l11l1_opy_ sec
        bstack1lll1l111l11_opy_ = int(self.bstack1lll1l11l11l_opy_.get(bstack11l1ll1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ∪"), self.bstack1lll1l11ll1l_opy_))
        bstack1lll1l11l1ll_opy_ = int(self.bstack1lll1l11l11l_opy_.get(bstack11l1ll1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ∫"), self.bstack1lll1l11ll11_opy_)) * 1000
        bstack1lll1l111l1l_opy_ = self.bstack1lll1l11l11l_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ∬"), None)
        bstack1lll1l11lll1_opy_ = self.bstack1lll1l11l11l_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ∭"), None)
        if bstack1lll1l11lll1_opy_ is None and bstack1lll1l111l1l_opy_ is None:
            return None
        try:
            while bstack1lll1l11lll1_opy_ and (time.time() * 1000 - bstack1lll1l1111ll_opy_) < bstack1lll1l11l1ll_opy_:
                response = bstack11l11lll1l1_opy_.bstack1lll1ll1llll_opy_(bstack1lll1l11lll1_opy_, {})
                if response and response.get(bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ∮")):
                    bstack1lll1l111ll1_opy_ = response.get(bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ∯"))
                self.bstack1lll1l1l1111_opy_ += 1
                if bstack1lll1l111ll1_opy_:
                    break
                time.sleep(bstack1lll1l111l11_opy_)
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡊࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡶࡪࡹࡵ࡭ࡶ࡙ࠣࡗࡒࠠࡢࡨࡷࡩࡷࠦࡷࡢ࡫ࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࢀࢃࠠࡴࡧࡦࡳࡳࡪࡳ࠯ࠤ∰").format(bstack1lll1l111l11_opy_))
            if bstack1lll1l111l1l_opy_ and not bstack1lll1l111ll1_opy_:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡋ࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡯࡭ࡦࡱࡸࡸ࡛ࠥࡒࡍࠤ∱"))
                response = bstack11l11lll1l1_opy_.bstack1lll1ll1llll_opy_(bstack1lll1l111l1l_opy_, {})
                if response and response.get(bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ∲")):
                    bstack1lll1l111ll1_opy_ = response.get(bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ∳"))
            if bstack1lll1l111ll1_opy_ and len(bstack1lll1l111ll1_opy_) > 0:
                for bstack1111ll11ll_opy_ in bstack1lll1l111ll1_opy_:
                    file_path = bstack1111ll11ll_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡦࡪ࡮ࡨࡔࡦࡺࡨࠣ∴"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lll1l111ll1_opy_:
                return None
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡑࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡲࡦࡥࡨ࡭ࡻ࡫ࡤ࠻ࠢࡾࢁࠧ∵").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻ࠢࡾࢁࠧ∶").format(e))
            return None
    def bstack11111lll111_opy_(self):
        bstack11l1ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡥࡤࡰࡱࡹࠠ࡮ࡣࡧࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ∷")
        return self.bstack1lll1l1l1111_opy_