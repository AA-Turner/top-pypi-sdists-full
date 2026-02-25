# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import time
from bstack_utils.bstack11l1111ll1l_opy_ import bstack11l1111l1ll_opy_
from bstack_utils.constants import bstack111ll1lllll_opy_
from bstack_utils.helper import get_host_info, bstack111l111111l_opy_
class bstack111111l11ll_opy_:
    bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡢࡰࡧࡰࡪࡹࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡶࡻ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ⋪")
    def __init__(self, config, logger):
        bstack11l1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡪࡩࡤࡶ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡢࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡳࡵࡴ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦ࡮ࡢ࡯ࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⋫")
        self.config = config
        self.logger = logger
        self.bstack1lll11l11lll_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡰ࡭࡫ࡷ࠱ࡹ࡫ࡳࡵࡵࠥ⋬")
        self.bstack1lll111lll11_opy_ = None
        self.bstack1lll11l111ll_opy_ = 60
        self.bstack1lll11l1l1l1_opy_ = 5
        self.bstack1lll111ll1ll_opy_ = 0
    def bstack11111111ll1_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack11l1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡧ࡮ࡥࠢࡶࡸࡴࡸࡥࡴࠢࡷ࡬ࡪࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡴࡴࡲ࡬ࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⋭")
        self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡌࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣ⋮").format(orchestration_strategy))
        try:
            bstack1lll111lll1l_opy_ = []
            bstack11l1l11_opy_ (u"ࠦࠧࠨࡗࡦࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤ࡫࡫ࡴࡤࡪࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢ࡬ࡷࠥࡹ࡯ࡶࡴࡦࡩࠥ࡯ࡳࠡࡶࡼࡴࡪࠦ࡯ࡧࠢࡤࡶࡷࡧࡹࠡࡣࡱࡨࠥ࡯ࡴࠨࡵࠣࡩࡱ࡫࡭ࡦࡰࡷࡷࠥࡧࡲࡦࠢࡲࡪࠥࡺࡹࡱࡧࠣࡨ࡮ࡩࡴࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡰࠣࡸ࡭ࡧࡴࠡࡥࡤࡷࡪ࠲ࠠࡶࡵࡨࡶࠥ࡮ࡡࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡲࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡵࡲࡹࡷࡩࡥࠡࡹ࡬ࡸ࡭ࠦࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭ࠦࡩ࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣࠤࠥ⋯")
            source = orchestration_metadata[bstack11l1l11_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫ⋰")].get(bstack11l1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭⋱"), [])
            bstack1lll11l1111l_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack11l1l11_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭⋲")].get(bstack11l1l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ⋳"), False) and not bstack1lll11l1111l_opy_:
                bstack1lll111lll1l_opy_ = bstack111l111111l_opy_(source) # bstack1lll11l11l11_opy_-repo is handled bstack1lll111llll1_opy_
            payload = {
                bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ⋴"): [{bstack11l1l11_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧ⋵"): f} for f in test_files],
                bstack11l1l11_opy_ (u"ࠦࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡹࡸࡡࡵࡧࡪࡽࠧ⋶"): orchestration_strategy,
                bstack11l1l11_opy_ (u"ࠧࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡒ࡫ࡴࡢࡦࡤࡸࡦࠨ⋷"): orchestration_metadata,
                bstack11l1l11_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤ⋸"): int(os.environ.get(bstack11l1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥ⋹")) or bstack11l1l11_opy_ (u"ࠣ࠲ࠥ⋺")),
                bstack11l1l11_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨ⋻"): int(os.environ.get(bstack11l1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ⋼")) or bstack11l1l11_opy_ (u"ࠦ࠶ࠨ⋽")),
                bstack11l1l11_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥ⋾"): self.config.get(bstack11l1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ⋿"), bstack11l1l11_opy_ (u"ࠧࠨ⌀")),
                bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦ⌁"): self.config.get(bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ⌂"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ⌃"): os.environ.get(bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥ⌄"), bstack11l1l11_opy_ (u"ࠧࠨ⌅")),
                bstack11l1l11_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣ⌆"): get_host_info(),
                bstack11l1l11_opy_ (u"ࠢࡱࡴࡇࡩࡹࡧࡩ࡭ࡵࠥ⌇"): bstack1lll111lll1l_opy_
            }
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤ⌈").format(payload))
            response = bstack11l1111l1ll_opy_.bstack1lll1l11lll1_opy_(self.bstack1lll11l11lll_opy_, payload)
            if response:
                self.bstack1lll111lll11_opy_ = self._1lll11l11111_opy_(response)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡕࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⌉").format(self.bstack1lll111lll11_opy_))
            else:
                self.logger.error(bstack11l1l11_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠰ࠥ⌊"))
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺࠻ࠢࡾࢁࠧ⌋").format(e))
    def _1lll11l11111_opy_(self, response):
        bstack11l1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡡ࡯ࡦࠣࡩࡽࡺࡲࡢࡥࡷࡷࠥࡸࡥ࡭ࡧࡹࡥࡳࡺࠠࡧ࡫ࡨࡰࡩࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⌌")
        bstack1lllllll1l_opy_ = {}
        bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ⌍")] = response.get(bstack11l1l11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ⌎"), self.bstack1lll11l111ll_opy_)
        bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ⌏")] = response.get(bstack11l1l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ⌐"), self.bstack1lll11l1l1l1_opy_)
        bstack1lll11l111l1_opy_ = response.get(bstack11l1l11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ⌑"))
        bstack1lll11l1l11l_opy_ = response.get(bstack11l1l11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ⌒"))
        if bstack1lll11l111l1_opy_:
            bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ⌓")] = bstack1lll11l111l1_opy_.split(bstack111ll1lllll_opy_ + bstack11l1l11_opy_ (u"ࠨ࠯ࠣ⌔"))[1] if bstack111ll1lllll_opy_ + bstack11l1l11_opy_ (u"ࠢ࠰ࠤ⌕") in bstack1lll11l111l1_opy_ else bstack1lll11l111l1_opy_
        else:
            bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ⌖")] = None
        if bstack1lll11l1l11l_opy_:
            bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ⌗")] = bstack1lll11l1l11l_opy_.split(bstack111ll1lllll_opy_ + bstack11l1l11_opy_ (u"ࠥ࠳ࠧ⌘"))[1] if bstack111ll1lllll_opy_ + bstack11l1l11_opy_ (u"ࠦ࠴ࠨ⌙") in bstack1lll11l1l11l_opy_ else bstack1lll11l1l11l_opy_
        else:
            bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ⌚")] = None
        if (
            response.get(bstack11l1l11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ⌛")) is None or
            response.get(bstack11l1l11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ⌜")) is None or
            response.get(bstack11l1l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ⌝")) is None or
            response.get(bstack11l1l11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ⌞")) is None
        ):
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡟ࡵࡸ࡯ࡤࡧࡶࡷࡤࡹࡰ࡭࡫ࡷࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡹࡰࡰࡰࡶࡩࡢࠦࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡰࡸࡰࡱࠦࡶࡢ࡮ࡸࡩ࠭ࡹࠩࠡࡨࡲࡶࠥࡹ࡯࡮ࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡹࠠࡪࡰࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ⌟"))
        return bstack1lllllll1l_opy_
    def bstack111111l1111_opy_(self):
        if not self.bstack1lll111lll11_opy_:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡔ࡯ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡧࡥࡹࡧࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠱ࠦ⌠"))
            return None
        bstack1lll11l1l111_opy_ = None
        test_files = []
        bstack1lll111lllll_opy_ = int(time.time() * 1000) # bstack1lll11l1l1ll_opy_ sec
        bstack1lll11l11ll1_opy_ = int(self.bstack1lll111lll11_opy_.get(bstack11l1l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ⌡"), self.bstack1lll11l1l1l1_opy_))
        bstack1lll11l11l1l_opy_ = int(self.bstack1lll111lll11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ⌢"), self.bstack1lll11l111ll_opy_)) * 1000
        bstack1lll11l1l11l_opy_ = self.bstack1lll111lll11_opy_.get(bstack11l1l11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ⌣"), None)
        bstack1lll11l111l1_opy_ = self.bstack1lll111lll11_opy_.get(bstack11l1l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ⌤"), None)
        if bstack1lll11l111l1_opy_ is None and bstack1lll11l1l11l_opy_ is None:
            return None
        try:
            while bstack1lll11l111l1_opy_ and (time.time() * 1000 - bstack1lll111lllll_opy_) < bstack1lll11l11l1l_opy_:
                response = bstack11l1111l1ll_opy_.bstack1lll1l111lll_opy_(bstack1lll11l111l1_opy_, {})
                if response and response.get(bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ⌥")):
                    bstack1lll11l1l111_opy_ = response.get(bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ⌦"))
                self.bstack1lll111ll1ll_opy_ += 1
                if bstack1lll11l1l111_opy_:
                    break
                time.sleep(bstack1lll11l11ll1_opy_)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡌࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡧࡴࡲࡱࠥࡸࡥࡴࡷ࡯ࡸ࡛ࠥࡒࡍࠢࡤࡪࡹ࡫ࡲࠡࡹࡤ࡭ࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡻࡾࠢࡶࡩࡨࡵ࡮ࡥࡵ࠱ࠦ⌧").format(bstack1lll11l11ll1_opy_))
            if bstack1lll11l1l11l_opy_ and not bstack1lll11l1l111_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡆࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡨࡵࡳࡲࠦࡴࡪ࡯ࡨࡳࡺࡺࠠࡖࡔࡏࠦ⌨"))
                response = bstack11l1111l1ll_opy_.bstack1lll1l111lll_opy_(bstack1lll11l1l11l_opy_, {})
                if response and response.get(bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ〈")):
                    bstack1lll11l1l111_opy_ = response.get(bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ〉"))
            if bstack1lll11l1l111_opy_ and len(bstack1lll11l1l111_opy_) > 0:
                for test_data in bstack1lll11l1l111_opy_:
                    file_path = test_data.get(bstack11l1l11_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥ⌫"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lll11l1l111_opy_:
                return None
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡓࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡴࡨࡧࡪ࡯ࡶࡦࡦ࠽ࠤࢀࢃࠢ⌬").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽ࠤࢀࢃࠢ⌭").format(e))
            return None
    def bstack1111111l1ll_opy_(self):
        bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡧࡦࡲ࡬ࡴࠢࡰࡥࡩ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⌮")
        return self.bstack1lll111ll1ll_opy_