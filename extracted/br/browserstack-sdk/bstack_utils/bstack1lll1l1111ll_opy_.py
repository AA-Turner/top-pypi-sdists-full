# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
import time
from bstack_utils.bstack1111l11ll1l_opy_ import bstack1111l11l11l_opy_
from bstack_utils.constants import bstack111111lllll_opy_
from bstack_utils.helper import get_host_info, bstack1lllllll1l1l_opy_
class bstack1lll1l11l111_opy_:
    bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡢࡰࡧࡰࡪࡹࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡶࡻ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ✧")
    def __init__(self, config, logger):
        bstack1ll1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡪࡩࡤࡶ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡢࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡳࡵࡴ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦ࡮ࡢ࡯ࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ✨")
        self.config = config
        self.logger = logger
        self.bstack1ll11ll11l1l_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡰ࡭࡫ࡷ࠱ࡹ࡫ࡳࡵࡵࠥ✩")
        self.bstack1ll11l1lll1l_opy_ = None
        self.default_timeout = 60
        self.bstack1ll11ll11lll_opy_ = 5
        self.bstack1ll11ll1l1l1_opy_ = 0
    def bstack1lll1l111l11_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1ll1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡧ࡮ࡥࠢࡶࡸࡴࡸࡥࡴࠢࡷ࡬ࡪࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡴࡴࡲ࡬ࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ✪")
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡌࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣ✫").format(orchestration_strategy))
        try:
            bstack1ll11l1lllll_opy_ = []
            bstack1ll1l11_opy_ (u"ࠦࠧࠨࡗࡦࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤ࡫࡫ࡴࡤࡪࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢ࡬ࡷࠥࡹ࡯ࡶࡴࡦࡩࠥ࡯ࡳࠡࡶࡼࡴࡪࠦ࡯ࡧࠢࡤࡶࡷࡧࡹࠡࡣࡱࡨࠥ࡯ࡴࠨࡵࠣࡩࡱ࡫࡭ࡦࡰࡷࡷࠥࡧࡲࡦࠢࡲࡪࠥࡺࡹࡱࡧࠣࡨ࡮ࡩࡴࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡰࠣࡸ࡭ࡧࡴࠡࡥࡤࡷࡪ࠲ࠠࡶࡵࡨࡶࠥ࡮ࡡࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡲࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡵࡲࡹࡷࡩࡥࠡࡹ࡬ࡸ࡭ࠦࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭ࠦࡩ࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣࠤࠥ✬")
            source = orchestration_metadata[bstack1ll1l11_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫ✭")].get(bstack1ll1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭✮"), [])
            bstack1ll11ll11ll1_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1ll1l11_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭✯")].get(bstack1ll1l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩ✰"), False) and not bstack1ll11ll11ll1_opy_:
                bstack1ll11l1lllll_opy_ = bstack1lllllll1l1l_opy_(source) # bstack1ll11l1lll11_opy_-repo is handled bstack1ll11ll111l1_opy_
            payload = {
                bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ✱"): [{bstack1ll1l11_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧ✲"): f} for f in test_files],
                bstack1ll1l11_opy_ (u"ࠦࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡹࡸࡡࡵࡧࡪࡽࠧ✳"): orchestration_strategy,
                bstack1ll1l11_opy_ (u"ࠧࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡒ࡫ࡴࡢࡦࡤࡸࡦࠨ✴"): orchestration_metadata,
                bstack1ll1l11_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤ✵"): int(os.environ.get(bstack1ll1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥ✶")) or bstack1ll1l11_opy_ (u"ࠣ࠲ࠥ✷")),
                bstack1ll1l11_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨ✸"): int(os.environ.get(bstack1ll1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ✹")) or bstack1ll1l11_opy_ (u"ࠦ࠶ࠨ✺")),
                bstack1ll1l11_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥ✻"): self.config.get(bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ✼"), bstack1ll1l11_opy_ (u"ࠧࠨ✽")),
                bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦ✾"): self.config.get(bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ✿"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ❀"): os.environ.get(bstack1ll1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥ❁"), bstack1ll1l11_opy_ (u"ࠧࠨ❂")),
                bstack1ll1l11_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣ❃"): get_host_info(),
                bstack1ll1l11_opy_ (u"ࠢࡱࡴࡇࡩࡹࡧࡩ࡭ࡵࠥ❄"): bstack1ll11l1lllll_opy_
            }
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤ❅").format(payload))
            response = bstack1111l11l11l_opy_.bstack1ll1l111l1ll_opy_(self.bstack1ll11ll11l1l_opy_, payload)
            if response:
                self.bstack1ll11l1lll1l_opy_ = self._1ll11ll11111_opy_(response)
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡕࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ❆").format(self.bstack1ll11l1lll1l_opy_))
            else:
                self.logger.error(bstack1ll1l11_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠰ࠥ❇"))
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺࠻ࠢࡾࢁࠧ❈").format(e))
    def _1ll11ll11111_opy_(self, response):
        bstack1ll1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡡ࡯ࡦࠣࡩࡽࡺࡲࡢࡥࡷࡷࠥࡸࡥ࡭ࡧࡹࡥࡳࡺࠠࡧ࡫ࡨࡰࡩࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ❉")
        bstack1l1l1111l1_opy_ = {}
        bstack1l1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ❊")] = response.get(bstack1ll1l11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ❋"), self.default_timeout)
        bstack1l1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ❌")] = response.get(bstack1ll1l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ❍"), self.bstack1ll11ll11lll_opy_)
        bstack1ll11ll1l1ll_opy_ = response.get(bstack1ll1l11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ❎"))
        bstack1ll11ll1l11l_opy_ = response.get(bstack1ll1l11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ❏"))
        if bstack1ll11ll1l1ll_opy_:
            bstack1l1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ❐")] = bstack1ll11ll1l1ll_opy_.split(bstack111111lllll_opy_ + bstack1ll1l11_opy_ (u"ࠨ࠯ࠣ❑"))[1] if bstack111111lllll_opy_ + bstack1ll1l11_opy_ (u"ࠢ࠰ࠤ❒") in bstack1ll11ll1l1ll_opy_ else bstack1ll11ll1l1ll_opy_
        else:
            bstack1l1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ❓")] = None
        if bstack1ll11ll1l11l_opy_:
            bstack1l1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ❔")] = bstack1ll11ll1l11l_opy_.split(bstack111111lllll_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠳ࠧ❕"))[1] if bstack111111lllll_opy_ + bstack1ll1l11_opy_ (u"ࠦ࠴ࠨ❖") in bstack1ll11ll1l11l_opy_ else bstack1ll11ll1l11l_opy_
        else:
            bstack1l1l1111l1_opy_[bstack1ll1l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ❗")] = None
        if (
            response.get(bstack1ll1l11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ❘")) is None or
            response.get(bstack1ll1l11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ❙")) is None or
            response.get(bstack1ll1l11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ❚")) is None or
            response.get(bstack1ll1l11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ❛")) is None
        ):
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠥ࡟ࡵࡸ࡯ࡤࡧࡶࡷࡤࡹࡰ࡭࡫ࡷࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡹࡰࡰࡰࡶࡩࡢࠦࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡰࡸࡰࡱࠦࡶࡢ࡮ࡸࡩ࠭ࡹࠩࠡࡨࡲࡶࠥࡹ࡯࡮ࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡹࠠࡪࡰࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ❜"))
        return bstack1l1l1111l1_opy_
    def bstack1lll1l1111l1_opy_(self):
        if not self.bstack1ll11l1lll1l_opy_:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡔ࡯ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡧࡥࡹࡧࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠱ࠦ❝"))
            return None
        bstack1ll11ll1111l_opy_ = None
        test_files = []
        bstack1ll11l1llll1_opy_ = int(time.time() * 1000) # bstack1ll11ll111ll_opy_ sec
        bstack1ll11ll11l11_opy_ = int(self.bstack1ll11l1lll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ❞"), self.bstack1ll11ll11lll_opy_))
        bstack1ll11ll1l111_opy_ = int(self.bstack1ll11l1lll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ❟"), self.default_timeout)) * 1000
        bstack1ll11ll1l11l_opy_ = self.bstack1ll11l1lll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ❠"), None)
        bstack1ll11ll1l1ll_opy_ = self.bstack1ll11l1lll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ❡"), None)
        if bstack1ll11ll1l1ll_opy_ is None and bstack1ll11ll1l11l_opy_ is None:
            return None
        try:
            while bstack1ll11ll1l1ll_opy_ and (time.time() * 1000 - bstack1ll11l1llll1_opy_) < bstack1ll11ll1l111_opy_:
                response = bstack1111l11l11l_opy_.bstack1ll1l1111ll1_opy_(bstack1ll11ll1l1ll_opy_, {})
                if response and response.get(bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ❢")):
                    bstack1ll11ll1111l_opy_ = response.get(bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ❣"))
                self.bstack1ll11ll1l1l1_opy_ += 1
                if bstack1ll11ll1111l_opy_:
                    break
                time.sleep(bstack1ll11ll11l11_opy_)
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡌࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡧࡴࡲࡱࠥࡸࡥࡴࡷ࡯ࡸ࡛ࠥࡒࡍࠢࡤࡪࡹ࡫ࡲࠡࡹࡤ࡭ࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡻࡾࠢࡶࡩࡨࡵ࡮ࡥࡵ࠱ࠦ❤").format(bstack1ll11ll11l11_opy_))
            if bstack1ll11ll1l11l_opy_ and not bstack1ll11ll1111l_opy_:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡆࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡨࡵࡳࡲࠦࡴࡪ࡯ࡨࡳࡺࡺࠠࡖࡔࡏࠦ❥"))
                response = bstack1111l11l11l_opy_.bstack1ll1l1111ll1_opy_(bstack1ll11ll1l11l_opy_, {})
                if response and response.get(bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ❦")):
                    bstack1ll11ll1111l_opy_ = response.get(bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ❧"))
            if bstack1ll11ll1111l_opy_ and len(bstack1ll11ll1111l_opy_) > 0:
                for bstack1llll11llll_opy_ in bstack1ll11ll1111l_opy_:
                    file_path = bstack1llll11llll_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥ❨"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1ll11ll1111l_opy_:
                return None
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡓࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡴࡨࡧࡪ࡯ࡶࡦࡦ࠽ࠤࢀࢃࠢ❩").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽ࠤࢀࢃࠢ❪").format(e))
            return None
    def bstack1lll1l111ll1_opy_(self):
        bstack1ll1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡧࡦࡲ࡬ࡴࠢࡰࡥࡩ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ❫")
        return self.bstack1ll11ll1l1l1_opy_