# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import time
from bstack_utils.bstack11l111l1111_opy_ import bstack11l1111lll1_opy_
from bstack_utils.constants import bstack111lllll1l1_opy_
from bstack_utils.helper import get_host_info, bstack1111lll1111_opy_
class bstack1111111l1ll_opy_:
    bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡌࡦࡴࡤ࡭ࡧࡶࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡹࡥࡳࡸࡨࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ⋧")
    def __init__(self, config, logger):
        bstack11ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡧ࡭ࡨࡺࠬࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡣࡰࡰࡩ࡭࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࡟ࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡷࡹࡸࠬࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡵࡷࡶࡦࡺࡥࡨࡻࠣࡲࡦࡳࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⋨")
        self.config = config
        self.logger = logger
        self.bstack1lll111lllll_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡴࡱ࡯ࡴ࠮ࡶࡨࡷࡹࡹࠢ⋩")
        self.bstack1lll11l11lll_opy_ = None
        self.bstack1lll11l1l1l1_opy_ = 60
        self.bstack1lll11l11l1l_opy_ = 5
        self.bstack1lll111ll1ll_opy_ = 0
    def bstack111111l1l11_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack11ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡍࡳ࡯ࡴࡪࡣࡷࡩࡸࠦࡴࡩࡧࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡤࡲࡩࠦࡳࡵࡱࡵࡩࡸࠦࡴࡩࡧࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡱࡱ࡯ࡰ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⋪")
        self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡩ࡯ࡩࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡹ࡬ࡸ࡭ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡾࢁࠧ⋫").format(orchestration_strategy))
        try:
            bstack1lll111lll11_opy_ = []
            bstack11ll111_opy_ (u"ࠣࠤ࡛ࠥࡪࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡨࡨࡸࡨ࡮ࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡩࡴࠢࡶࡳࡺࡸࡣࡦࠢ࡬ࡷࠥࡺࡹࡱࡧࠣࡳ࡫ࠦࡡࡳࡴࡤࡽࠥࡧ࡮ࡥࠢ࡬ࡸࠬࡹࠠࡦ࡮ࡨࡱࡪࡴࡴࡴࠢࡤࡶࡪࠦ࡯ࡧࠢࡷࡽࡵ࡫ࠠࡥ࡫ࡦࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡴࠠࡵࡪࡤࡸࠥࡩࡡࡴࡧ࠯ࠤࡺࡹࡥࡳࠢ࡫ࡥࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡ࡯ࡸࡰࡹ࡯࠭ࡳࡧࡳࡳࠥࡹ࡯ࡶࡴࡦࡩࠥࡽࡩࡵࡪࠣࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠣ࡭ࡳࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠧࠨࠢ⋬")
            source = orchestration_metadata[bstack11ll111_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨ⋭")].get(bstack11ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ⋮"), [])
            bstack1lll11l1111l_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack11ll111_opy_ (u"ࠫࡷࡻ࡮ࡠࡵࡰࡥࡷࡺ࡟ࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠪ⋯")].get(bstack11ll111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡩ࠭⋰"), False) and not bstack1lll11l1111l_opy_:
                bstack1lll111lll11_opy_ = bstack1111lll1111_opy_(source) # bstack1lll111lll1l_opy_-repo is handled bstack1lll11l11111_opy_
            payload = {
                bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ⋱"): [{bstack11ll111_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤ⋲"): f} for f in test_files],
                bstack11ll111_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡶࡵࡥࡹ࡫ࡧࡺࠤ⋳"): orchestration_strategy,
                bstack11ll111_opy_ (u"ࠤࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡏࡨࡸࡦࡪࡡࡵࡣࠥ⋴"): orchestration_metadata,
                bstack11ll111_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨ⋵"): int(os.environ.get(bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ⋶")) or bstack11ll111_opy_ (u"ࠧ࠶ࠢ⋷")),
                bstack11ll111_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥ⋸"): int(os.environ.get(bstack11ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ⋹")) or bstack11ll111_opy_ (u"ࠣ࠳ࠥ⋺")),
                bstack11ll111_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢ⋻"): self.config.get(bstack11ll111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ⋼"), bstack11ll111_opy_ (u"ࠫࠬ⋽")),
                bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ⋾"): self.config.get(bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ⋿"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ⌀"): os.environ.get(bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ⌁"), bstack11ll111_opy_ (u"ࠤࠥ⌂")),
                bstack11ll111_opy_ (u"ࠥ࡬ࡴࡹࡴࡊࡰࡩࡳࠧ⌃"): get_host_info(),
                bstack11ll111_opy_ (u"ࠦࡵࡸࡄࡦࡶࡤ࡭ࡱࡹࠢ⌄"): bstack1lll111lll11_opy_
            }
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼ࠣࡿࢂࠨ⌅").format(payload))
            response = bstack11l1111lll1_opy_.bstack1lll1l11l1ll_opy_(self.bstack1lll111lllll_opy_, payload)
            if response:
                self.bstack1lll11l11lll_opy_ = self._1lll11l11l11_opy_(response)
                self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡ࡙ࠥࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ⌆").format(self.bstack1lll11l11lll_opy_))
            else:
                self.logger.error(bstack11ll111_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢ⌇"))
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶ࠾࠿ࠦࡻࡾࠤ⌈").format(e))
    def _1lll11l11l11_opy_(self, response):
        bstack11ll111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡥࡳࡪࠠࡦࡺࡷࡶࡦࡩࡴࡴࠢࡵࡩࡱ࡫ࡶࡢࡰࡷࠤ࡫࡯ࡥ࡭ࡦࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⌉")
        bstack11l11l1ll1_opy_ = {}
        bstack11l11l1ll1_opy_[bstack11ll111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ⌊")] = response.get(bstack11ll111_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ⌋"), self.bstack1lll11l1l1l1_opy_)
        bstack11l11l1ll1_opy_[bstack11ll111_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ⌌")] = response.get(bstack11ll111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠣ⌍"), self.bstack1lll11l11l1l_opy_)
        bstack1lll11l1l11l_opy_ = response.get(bstack11ll111_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ⌎"))
        bstack1lll11l1l111_opy_ = response.get(bstack11ll111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ⌏"))
        if bstack1lll11l1l11l_opy_:
            bstack11l11l1ll1_opy_[bstack11ll111_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ⌐")] = bstack1lll11l1l11l_opy_.split(bstack111lllll1l1_opy_ + bstack11ll111_opy_ (u"ࠥ࠳ࠧ⌑"))[1] if bstack111lllll1l1_opy_ + bstack11ll111_opy_ (u"ࠦ࠴ࠨ⌒") in bstack1lll11l1l11l_opy_ else bstack1lll11l1l11l_opy_
        else:
            bstack11l11l1ll1_opy_[bstack11ll111_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ⌓")] = None
        if bstack1lll11l1l111_opy_:
            bstack11l11l1ll1_opy_[bstack11ll111_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ⌔")] = bstack1lll11l1l111_opy_.split(bstack111lllll1l1_opy_ + bstack11ll111_opy_ (u"ࠢ࠰ࠤ⌕"))[1] if bstack111lllll1l1_opy_ + bstack11ll111_opy_ (u"ࠣ࠱ࠥ⌖") in bstack1lll11l1l111_opy_ else bstack1lll11l1l111_opy_
        else:
            bstack11l11l1ll1_opy_[bstack11ll111_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ⌗")] = None
        if (
            response.get(bstack11ll111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ⌘")) is None or
            response.get(bstack11ll111_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ⌙")) is None or
            response.get(bstack11ll111_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ⌚")) is None or
            response.get(bstack11ll111_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ⌛")) is None
        ):
            self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡜ࡲࡵࡳࡨ࡫ࡳࡴࡡࡶࡴࡱ࡯ࡴࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡶࡴࡴࡴࡳࡦ࡟ࠣࡖࡪࡩࡥࡪࡸࡨࡨࠥࡴࡵ࡭࡮ࠣࡺࡦࡲࡵࡦࠪࡶ࠭ࠥ࡬࡯ࡳࠢࡶࡳࡲ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧࡶࠤ࡮ࡴࠠࡴࡲ࡯࡭ࡹࠦࡴࡦࡵࡷࡷࠥࡇࡐࡊࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ⌜"))
        return bstack11l11l1ll1_opy_
    def bstack1111111llll_opy_(self):
        if not self.bstack1lll11l11lll_opy_:
            self.logger.error(bstack11ll111_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡑࡳࠥࡸࡥࡲࡷࡨࡷࡹࠦࡤࡢࡶࡤࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠮ࠣ⌝"))
            return None
        bstack1lll111llll1_opy_ = None
        test_files = []
        bstack1lll111ll1l1_opy_ = int(time.time() * 1000) # bstack1lll11l111ll_opy_ sec
        bstack1lll11l11ll1_opy_ = int(self.bstack1lll11l11lll_opy_.get(bstack11ll111_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ⌞"), self.bstack1lll11l11l1l_opy_))
        bstack1lll11l111l1_opy_ = int(self.bstack1lll11l11lll_opy_.get(bstack11ll111_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ⌟"), self.bstack1lll11l1l1l1_opy_)) * 1000
        bstack1lll11l1l111_opy_ = self.bstack1lll11l11lll_opy_.get(bstack11ll111_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ⌠"), None)
        bstack1lll11l1l11l_opy_ = self.bstack1lll11l11lll_opy_.get(bstack11ll111_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ⌡"), None)
        if bstack1lll11l1l11l_opy_ is None and bstack1lll11l1l111_opy_ is None:
            return None
        try:
            while bstack1lll11l1l11l_opy_ and (time.time() * 1000 - bstack1lll111ll1l1_opy_) < bstack1lll11l111l1_opy_:
                response = bstack11l1111lll1_opy_.bstack1lll1l11l111_opy_(bstack1lll11l1l11l_opy_, {})
                if response and response.get(bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ⌢")):
                    bstack1lll111llll1_opy_ = response.get(bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ⌣"))
                self.bstack1lll111ll1ll_opy_ += 1
                if bstack1lll111llll1_opy_:
                    break
                time.sleep(bstack1lll11l11ll1_opy_)
                self.logger.debug(bstack11ll111_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡵࡩࡸࡻ࡬ࡵࠢࡘࡖࡑࠦࡡࡧࡶࡨࡶࠥࡽࡡࡪࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡿࢂࠦࡳࡦࡥࡲࡲࡩࡹ࠮ࠣ⌤").format(bstack1lll11l11ll1_opy_))
            if bstack1lll11l1l111_opy_ and not bstack1lll111llll1_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡊࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡮ࡳࡥࡰࡷࡷࠤ࡚ࡘࡌࠣ⌥"))
                response = bstack11l1111lll1_opy_.bstack1lll1l11l111_opy_(bstack1lll11l1l111_opy_, {})
                if response and response.get(bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ⌦")):
                    bstack1lll111llll1_opy_ = response.get(bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ⌧"))
            if bstack1lll111llll1_opy_ and len(bstack1lll111llll1_opy_) > 0:
                for test_data in bstack1lll111llll1_opy_:
                    file_path = test_data.get(bstack11ll111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢ⌨"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lll111llll1_opy_:
                return None
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡐࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡸࡥࡤࡧ࡬ࡺࡪࡪ࠺ࠡࡽࢀࠦ〈").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦ〉").format(e))
            return None
    def bstack1111111l1l1_opy_(self):
        bstack11ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡤࡣ࡯ࡰࡸࠦ࡭ࡢࡦࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⌫")
        return self.bstack1lll111ll1ll_opy_