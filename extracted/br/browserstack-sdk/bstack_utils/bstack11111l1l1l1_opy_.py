# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import time
from bstack_utils.bstack11l11ll11l1_opy_ import bstack11l11ll1l11_opy_
from bstack_utils.constants import bstack11l111ll1ll_opy_
from bstack_utils.helper import get_host_info, bstack1111llll1l1_opy_
class bstack11111ll1l11_opy_:
    bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡸࡶࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ∓")
    def __init__(self, config, logger):
        bstack11lllll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡥ࡫ࡦࡸ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡤࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡵࡷࡶ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡࡰࡤࡱࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ∔")
        self.config = config
        self.logger = logger
        self.bstack1lll1l11ll1l_opy_ = bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡲ࡯࡭ࡹ࠳ࡴࡦࡵࡷࡷࠧ∕")
        self.bstack1lll1l1111l1_opy_ = None
        self.bstack1lll1l111lll_opy_ = 60
        self.bstack1lll1l11l1ll_opy_ = 5
        self.bstack1lll11llllll_opy_ = 0
    def bstack11111ll1ll1_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack11lllll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡱ࡭ࡹ࡯ࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡸࡺ࡯ࡳࡧࡶࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡶ࡯࡭࡮࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ∖")
        self.logger.debug(bstack11lllll_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡎࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥ∗").format(orchestration_strategy))
        try:
            bstack1lll1l11111l_opy_ = []
            bstack11lllll_opy_ (u"ࠨ࡙ࠢࠣࡨࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡦࡦࡶࡦ࡬ࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡮ࡹࠠࡴࡱࡸࡶࡨ࡫ࠠࡪࡵࠣࡸࡾࡶࡥࠡࡱࡩࠤࡦࡸࡲࡢࡻࠣࡥࡳࡪࠠࡪࡶࠪࡷࠥ࡫࡬ࡦ࡯ࡨࡲࡹࡹࠠࡢࡴࡨࠤࡴ࡬ࠠࡵࡻࡳࡩࠥࡪࡩࡤࡶࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡲࠥࡺࡨࡢࡶࠣࡧࡦࡹࡥ࠭ࠢࡸࡷࡪࡸࠠࡩࡣࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦ࡭ࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡷࡴࡻࡲࡤࡧࠣࡻ࡮ࡺࡨࠡࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠡ࡫ࡱࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥࠦࠧ∘")
            source = orchestration_metadata[bstack11lllll_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭∙")].get(bstack11lllll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ√"), [])
            bstack1lll11lllll1_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack11lllll_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨ∛")].get(bstack11lllll_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ∜"), False) and not bstack1lll11lllll1_opy_:
                bstack1lll1l11111l_opy_ = bstack1111llll1l1_opy_(source) # bstack1lll1l1111ll_opy_-repo is handled bstack1lll1l11l1l1_opy_
            payload = {
                bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ∝"): [{bstack11lllll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢ∞"): f} for f in test_files],
                bstack11lllll_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠢ∟"): orchestration_strategy,
                bstack11lllll_opy_ (u"ࠢࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡍࡦࡶࡤࡨࡦࡺࡡࠣ∠"): orchestration_metadata,
                bstack11lllll_opy_ (u"ࠣࡰࡲࡨࡪࡏ࡮ࡥࡧࡻࠦ∡"): int(os.environ.get(bstack11lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧ∢")) or bstack11lllll_opy_ (u"ࠥ࠴ࠧ∣")),
                bstack11lllll_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࡑࡳࡩ࡫ࡳࠣ∤"): int(os.environ.get(bstack11lllll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢ∥")) or bstack11lllll_opy_ (u"ࠨ࠱ࠣ∦")),
                bstack11lllll_opy_ (u"ࠢࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠧ∧"): self.config.get(bstack11lllll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭∨"), bstack11lllll_opy_ (u"ࠩࠪ∩")),
                bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠨ∪"): self.config.get(bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ∫"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ∬"): os.environ.get(bstack11lllll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠧ∭"), bstack11lllll_opy_ (u"ࠢࠣ∮")),
                bstack11lllll_opy_ (u"ࠣࡪࡲࡷࡹࡏ࡮ࡧࡱࠥ∯"): get_host_info(),
                bstack11lllll_opy_ (u"ࠤࡳࡶࡉ࡫ࡴࡢ࡫࡯ࡷࠧ∰"): bstack1lll1l11111l_opy_
            }
            self.logger.debug(bstack11lllll_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦ∱").format(payload))
            response = bstack11l11ll1l11_opy_.bstack1lll1ll1ll1l_opy_(self.bstack1lll1l11ll1l_opy_, payload)
            if response:
                self.bstack1lll1l1111l1_opy_ = self._1lll1l11l11l_opy_(response)
                self.logger.debug(bstack11lllll_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ∲").format(self.bstack1lll1l1111l1_opy_))
            else:
                self.logger.error(bstack11lllll_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࠧ∳"))
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼࠽ࠤࢀࢃࠢ∴").format(e))
    def _1lll1l11l11l_opy_(self, response):
        bstack11lllll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡣࡱࡨࠥ࡫ࡸࡵࡴࡤࡧࡹࡹࠠࡳࡧ࡯ࡩࡻࡧ࡮ࡵࠢࡩ࡭ࡪࡲࡤࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ∵")
        bstack1l1ll11l1_opy_ = {}
        bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ∶")] = response.get(bstack11lllll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ∷"), self.bstack1lll1l111lll_opy_)
        bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ∸")] = response.get(bstack11lllll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ∹"), self.bstack1lll1l11l1ll_opy_)
        bstack1lll1l111l11_opy_ = response.get(bstack11lllll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ∺"))
        bstack1lll1l111l1l_opy_ = response.get(bstack11lllll_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ∻"))
        if bstack1lll1l111l11_opy_:
            bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ∼")] = bstack1lll1l111l11_opy_.split(bstack11l111ll1ll_opy_ + bstack11lllll_opy_ (u"ࠣ࠱ࠥ∽"))[1] if bstack11l111ll1ll_opy_ + bstack11lllll_opy_ (u"ࠤ࠲ࠦ∾") in bstack1lll1l111l11_opy_ else bstack1lll1l111l11_opy_
        else:
            bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ∿")] = None
        if bstack1lll1l111l1l_opy_:
            bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ≀")] = bstack1lll1l111l1l_opy_.split(bstack11l111ll1ll_opy_ + bstack11lllll_opy_ (u"ࠧ࠵ࠢ≁"))[1] if bstack11l111ll1ll_opy_ + bstack11lllll_opy_ (u"ࠨ࠯ࠣ≂") in bstack1lll1l111l1l_opy_ else bstack1lll1l111l1l_opy_
        else:
            bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ≃")] = None
        if (
            response.get(bstack11lllll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ≄")) is None or
            response.get(bstack11lllll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ≅")) is None or
            response.get(bstack11lllll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ≆")) is None or
            response.get(bstack11lllll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ≇")) is None
        ):
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡡࡰࡳࡱࡦࡩࡸࡹ࡟ࡴࡲ࡯࡭ࡹࡥࡴࡦࡵࡷࡷࡤࡸࡥࡴࡲࡲࡲࡸ࡫࡝ࠡࡔࡨࡧࡪ࡯ࡶࡦࡦࠣࡲࡺࡲ࡬ࠡࡸࡤࡰࡺ࡫ࠨࡴࠫࠣࡪࡴࡸࠠࡴࡱࡰࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥࡴࠢ࡬ࡲࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤ≈"))
        return bstack1l1ll11l1_opy_
    def bstack11111ll1lll_opy_(self):
        if not self.bstack1lll1l1111l1_opy_:
            self.logger.error(bstack11lllll_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠳ࠨ≉"))
            return None
        bstack1lll1l111111_opy_ = None
        test_files = []
        bstack1lll11llll1l_opy_ = int(time.time() * 1000) # bstack1lll1l11ll11_opy_ sec
        bstack1lll1l11l111_opy_ = int(self.bstack1lll1l1111l1_opy_.get(bstack11lllll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ≊"), self.bstack1lll1l11l1ll_opy_))
        bstack1lll1l111ll1_opy_ = int(self.bstack1lll1l1111l1_opy_.get(bstack11lllll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ≋"), self.bstack1lll1l111lll_opy_)) * 1000
        bstack1lll1l111l1l_opy_ = self.bstack1lll1l1111l1_opy_.get(bstack11lllll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ≌"), None)
        bstack1lll1l111l11_opy_ = self.bstack1lll1l1111l1_opy_.get(bstack11lllll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ≍"), None)
        if bstack1lll1l111l11_opy_ is None and bstack1lll1l111l1l_opy_ is None:
            return None
        try:
            while bstack1lll1l111l11_opy_ and (time.time() * 1000 - bstack1lll11llll1l_opy_) < bstack1lll1l111ll1_opy_:
                response = bstack11l11ll1l11_opy_.bstack1lll1ll1ll11_opy_(bstack1lll1l111l11_opy_, {})
                if response and response.get(bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ≎")):
                    bstack1lll1l111111_opy_ = response.get(bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ≏"))
                self.bstack1lll11llllll_opy_ += 1
                if bstack1lll1l111111_opy_:
                    break
                time.sleep(bstack1lll1l11l111_opy_)
                self.logger.debug(bstack11lllll_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡳࡧࡶࡹࡱࡺࠠࡖࡔࡏࠤࡦ࡬ࡴࡦࡴࠣࡻࡦ࡯ࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡽࢀࠤࡸ࡫ࡣࡰࡰࡧࡷ࠳ࠨ≐").format(bstack1lll1l11l111_opy_))
            if bstack1lll1l111l1l_opy_ and not bstack1lll1l111111_opy_:
                self.logger.debug(bstack11lllll_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡬ࡱࡪࡵࡵࡵࠢࡘࡖࡑࠨ≑"))
                response = bstack11l11ll1l11_opy_.bstack1lll1ll1ll11_opy_(bstack1lll1l111l1l_opy_, {})
                if response and response.get(bstack11lllll_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ≒")):
                    bstack1lll1l111111_opy_ = response.get(bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ≓"))
            if bstack1lll1l111111_opy_ and len(bstack1lll1l111111_opy_) > 0:
                for bstack1111llllll_opy_ in bstack1lll1l111111_opy_:
                    file_path = bstack1111llllll_opy_.get(bstack11lllll_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧ≔"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lll1l111111_opy_:
                return None
            self.logger.debug(bstack11lllll_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡕࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡶࡪࡩࡥࡪࡸࡨࡨ࠿ࠦࡻࡾࠤ≕").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤ≖").format(e))
            return None
    def bstack11111ll111l_opy_(self):
        bstack11lllll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡩࡡ࡭࡮ࡶࠤࡲࡧࡤࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ≗")
        return self.bstack1lll11llllll_opy_