# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import time
from bstack_utils.bstack11111l11l11_opy_ import bstack111111ll111_opy_
from bstack_utils.constants import bstack1lll1lll1l11_opy_
from bstack_utils.helper import get_host_info, bstack111l11l111l_opy_
class bstack1111l1l1111_opy_:
    bstack1ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡉࡣࡱࡨࡱ࡫ࡳࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡷࡼࡥࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥὁ")
    def __init__(self, config, logger):
        bstack1ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡤࡪࡥࡷ࠰ࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡧࡴࡴࡦࡪࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡣࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡴࡶࡵ࠰ࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿࠠ࡯ࡣࡰࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤὂ")
        self.config = config
        self.logger = logger
        self.bstack1lll1l11l1ll_opy_ = bstack1ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡱ࡮࡬ࡸ࠲ࡺࡥࡴࡶࡶࠦὃ")
        self.bstack1lll1l1l11l1_opy_ = None
        self.default_timeout = 60
        self.bstack1lll1l1l1lll_opy_ = 5
        self.bstack1lll1l11ll1l_opy_ = 0
    def bstack1111l11l111_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡊࡰ࡬ࡸ࡮ࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡸࡥࡲࡷࡨࡷࡹࠦࡡ࡯ࡦࠣࡷࡹࡵࡲࡦࡵࠣࡸ࡭࡫ࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡵࡵ࡬࡭࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥὄ")
        self.logger.debug(bstack1ll111_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡍࡳ࡯ࡴࡪࡣࡷ࡭ࡳ࡭ࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡽࡩࡵࡪࠣࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡻࡾࠤὅ").format(orchestration_strategy))
        try:
            bstack1lll1l1l1l11_opy_ = []
            bstack1ll111_opy_ (u"ࠧࠨࠢࡘࡧࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥ࡬ࡥࡵࡥ࡫ࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣ࡭ࡸࠦࡳࡰࡷࡵࡧࡪࠦࡩࡴࠢࡷࡽࡵ࡫ࠠࡰࡨࠣࡥࡷࡸࡡࡺࠢࡤࡲࡩࠦࡩࡵࠩࡶࠤࡪࡲࡥ࡮ࡧࡱࡸࡸࠦࡡࡳࡧࠣࡳ࡫ࠦࡴࡺࡲࡨࠤࡩ࡯ࡣࡵࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡧࡦࡥࡺࡹࡥࠡ࡫ࡱࠤࡹ࡮ࡡࡵࠢࡦࡥࡸ࡫ࠬࠡࡷࡶࡩࡷࠦࡨࡢࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡳࡵ࡭ࡶ࡬࠱ࡷ࡫ࡰࡰࠢࡶࡳࡺࡸࡣࡦࠢࡺ࡭ࡹ࡮ࠠࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠠࡪࡰࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤࠥࠦ὆")
            source = orchestration_metadata[bstack1ll111_opy_ (u"࠭ࡲࡶࡰࡢࡷࡲࡧࡲࡵࡡࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠬ὇")].get(bstack1ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧὈ"), [])
            bstack1lll1l1l1ll1_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1ll111_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧὉ")].get(bstack1ll111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪὊ"), False) and not bstack1lll1l1l1ll1_opy_:
                bstack1lll1l1l1l11_opy_ = bstack111l11l111l_opy_(source) # bstack1lll1l1l1l1l_opy_-repo is handled bstack1lll1l11llll_opy_
            payload = {
                bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤὋ"): [{bstack1ll111_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨὌ"): f} for f in test_files],
                bstack1ll111_opy_ (u"ࠧࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡘࡺࡲࡢࡶࡨ࡫ࡾࠨὍ"): orchestration_strategy,
                bstack1ll111_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡓࡥࡵࡣࡧࡥࡹࡧࠢ὎"): orchestration_metadata,
                bstack1ll111_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ὏"): int(os.environ.get(bstack1ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦὐ")) or bstack1ll111_opy_ (u"ࠤ࠳ࠦὑ")),
                bstack1ll111_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢὒ"): int(os.environ.get(bstack1ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨὓ")) or bstack1ll111_opy_ (u"ࠧ࠷ࠢὔ")),
                bstack1ll111_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦὕ"): self.config.get(bstack1ll111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬὖ"), bstack1ll111_opy_ (u"ࠨࠩὗ")),
                bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ὘"): self.config.get(bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭Ὑ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ὚"): os.environ.get(bstack1ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦὛ"), bstack1ll111_opy_ (u"ࠨࠢ὜")),
                bstack1ll111_opy_ (u"ࠢࡩࡱࡶࡸࡎࡴࡦࡰࠤὝ"): get_host_info(),
                bstack1ll111_opy_ (u"ࠣࡲࡵࡈࡪࡺࡡࡪ࡮ࡶࠦ὞"): bstack1lll1l1l1l11_opy_
            }
            self.logger.debug(bstack1ll111_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥὟ").format(payload))
            response = bstack111111ll111_opy_.bstack1lll1llll11l_opy_(self.bstack1lll1l11l1ll_opy_, payload)
            if response:
                self.bstack1lll1l1l11l1_opy_ = self._1lll1l1ll1l1_opy_(response)
                self.logger.debug(bstack1ll111_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨὠ").format(self.bstack1lll1l1l11l1_opy_))
            else:
                self.logger.error(bstack1ll111_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦὡ"))
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻࠼ࠣࡿࢂࠨὢ").format(e))
    def _1lll1l1ll1l1_opy_(self, response):
        bstack1ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡢࡰࡧࠤࡪࡾࡴࡳࡣࡦࡸࡸࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡨ࡬ࡩࡱࡪࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨὣ")
        bstack1ll11ll11l_opy_ = {}
        bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣὤ")] = response.get(bstack1ll111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤὥ"), self.default_timeout)
        bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦὦ")] = response.get(bstack1ll111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧὧ"), self.bstack1lll1l1l1lll_opy_)
        bstack1lll1l1l111l_opy_ = response.get(bstack1ll111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢὨ"))
        bstack1lll1l1l11ll_opy_ = response.get(bstack1ll111_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤὩ"))
        if bstack1lll1l1l111l_opy_:
            bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤὪ")] = bstack1lll1l1l111l_opy_.split(bstack1lll1lll1l11_opy_ + bstack1ll111_opy_ (u"ࠢ࠰ࠤὫ"))[1] if bstack1lll1lll1l11_opy_ + bstack1ll111_opy_ (u"ࠣ࠱ࠥὬ") in bstack1lll1l1l111l_opy_ else bstack1lll1l1l111l_opy_
        else:
            bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧὭ")] = None
        if bstack1lll1l1l11ll_opy_:
            bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢὮ")] = bstack1lll1l1l11ll_opy_.split(bstack1lll1lll1l11_opy_ + bstack1ll111_opy_ (u"ࠦ࠴ࠨὯ"))[1] if bstack1lll1lll1l11_opy_ + bstack1ll111_opy_ (u"ࠧ࠵ࠢὰ") in bstack1lll1l1l11ll_opy_ else bstack1lll1l1l11ll_opy_
        else:
            bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥά")] = None
        if (
            response.get(bstack1ll111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣὲ")) is None or
            response.get(bstack1ll111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥέ")) is None or
            response.get(bstack1ll111_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨὴ")) is None or
            response.get(bstack1ll111_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨή")) is None
        ):
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡠࡶࡲࡰࡥࡨࡷࡸࡥࡳࡱ࡮࡬ࡸࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡳࡱࡱࡱࡷࡪࡣࠠࡓࡧࡦࡩ࡮ࡼࡥࡥࠢࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠮ࡳࠪࠢࡩࡳࡷࠦࡳࡰ࡯ࡨࠤࡦࡺࡴࡳ࡫ࡥࡹࡹ࡫ࡳࠡ࡫ࡱࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣὶ"))
        return bstack1ll11ll11l_opy_
    def bstack1111l1111ll_opy_(self):
        if not self.bstack1lll1l1l11l1_opy_:
            self.logger.error(bstack1ll111_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠲ࠧί"))
            return None
        bstack1lll1l11ll11_opy_ = None
        test_files = []
        bstack1lll1l1l1111_opy_ = int(time.time() * 1000) # bstack1lll1l11lll1_opy_ sec
        bstack1lll1l1ll11l_opy_ = int(self.bstack1lll1l1l11l1_opy_.get(bstack1ll111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣὸ"), self.bstack1lll1l1l1lll_opy_))
        bstack1lll1l1ll111_opy_ = int(self.bstack1lll1l1l11l1_opy_.get(bstack1ll111_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣό"), self.default_timeout)) * 1000
        bstack1lll1l1l11ll_opy_ = self.bstack1lll1l1l11l1_opy_.get(bstack1ll111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧὺ"), None)
        bstack1lll1l1l111l_opy_ = self.bstack1lll1l1l11l1_opy_.get(bstack1ll111_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧύ"), None)
        if bstack1lll1l1l111l_opy_ is None and bstack1lll1l1l11ll_opy_ is None:
            return None
        try:
            while bstack1lll1l1l111l_opy_ and (time.time() * 1000 - bstack1lll1l1l1111_opy_) < bstack1lll1l1ll111_opy_:
                response = bstack111111ll111_opy_.bstack1lll1llll111_opy_(bstack1lll1l1l111l_opy_, {})
                if response and response.get(bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤὼ")):
                    bstack1lll1l11ll11_opy_ = response.get(bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥώ"))
                self.bstack1lll1l11ll1l_opy_ += 1
                if bstack1lll1l11ll11_opy_:
                    break
                time.sleep(bstack1lll1l1ll11l_opy_)
                self.logger.debug(bstack1ll111_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡆࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡨࡵࡳࡲࠦࡲࡦࡵࡸࡰࡹࠦࡕࡓࡎࠣࡥ࡫ࡺࡥࡳࠢࡺࡥ࡮ࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡼࡿࠣࡷࡪࡩ࡯࡯ࡦࡶ࠲ࠧ὾").format(bstack1lll1l1ll11l_opy_))
            if bstack1lll1l1l11ll_opy_ and not bstack1lll1l11ll11_opy_:
                self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡵ࡫ࡰࡩࡴࡻࡴࠡࡗࡕࡐࠧ὿"))
                response = bstack111111ll111_opy_.bstack1lll1llll111_opy_(bstack1lll1l1l11ll_opy_, {})
                if response and response.get(bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨᾀ")):
                    bstack1lll1l11ll11_opy_ = response.get(bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢᾁ"))
            if bstack1lll1l11ll11_opy_ and len(bstack1lll1l11ll11_opy_) > 0:
                for test_data in bstack1lll1l11ll11_opy_:
                    file_path = test_data.get(bstack1ll111_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦᾂ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lll1l11ll11_opy_:
                return None
            self.logger.debug(bstack1ll111_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡔࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡵࡩࡨ࡫ࡩࡷࡧࡧ࠾ࠥࢁࡽࠣᾃ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾ࠥࢁࡽࠣᾄ").format(e))
            return None
    def bstack1111l1l1l1l_opy_(self):
        bstack1ll111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡨࡧ࡬࡭ࡵࠣࡱࡦࡪࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᾅ")
        return self.bstack1lll1l11ll1l_opy_