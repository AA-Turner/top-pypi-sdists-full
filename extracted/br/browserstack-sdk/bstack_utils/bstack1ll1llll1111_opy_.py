# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import time
from bstack_utils.bstack111111lllll_opy_ import bstack11111l111ll_opy_
from bstack_utils.constants import bstack1111111l1ll_opy_
from bstack_utils.helper import get_host_info, bstack1lll1lll1lll_opy_
class bstack1ll1lll1l1l1_opy_:
    bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡥࡳࡪ࡬ࡦࡵࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡲࡷࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⬨")
    def __init__(self, config, logger):
        bstack1l1llll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡦ࡬ࡧࡹ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡥࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡶࡸࡷ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢࡱࡥࡲ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⬩")
        self.config = config
        self.logger = logger
        self.bstack1l1llll11l11_opy_ = bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡳࡰ࡮ࡺ࠭ࡵࡧࡶࡸࡸࠨ⬪")
        self.bstack1l1llll1l11l_opy_ = None
        self.default_timeout = 60
        self.bstack1l1llll1ll11_opy_ = 5
        self.bstack1l1llll11ll1_opy_ = 0
    def bstack1ll1lll1l111_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡌࡲ࡮ࡺࡩࡢࡶࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡹࡴࡰࡴࡨࡷࠥࡺࡨࡦࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡰࡰ࡮࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⬫")
        self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡏ࡮ࡪࡶ࡬ࡥࡹ࡯࡮ࡨࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡽࢀࠦ⬬").format(orchestration_strategy))
        try:
            bstack1l1llll11l1l_opy_ = []
            bstack1l1llll_opy_ (u"ࠢࠣࠤ࡚ࡩࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡧࡧࡷࡧ࡭ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡯ࡳࠡࡵࡲࡹࡷࡩࡥࠡ࡫ࡶࠤࡹࡿࡰࡦࠢࡲࡪࠥࡧࡲࡳࡣࡼࠤࡦࡴࡤࠡ࡫ࡷࠫࡸࠦࡥ࡭ࡧࡰࡩࡳࡺࡳࠡࡣࡵࡩࠥࡵࡦࠡࡶࡼࡴࡪࠦࡤࡪࡥࡷࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡩࡨࡧࡵࡴࡧࠣ࡭ࡳࠦࡴࡩࡣࡷࠤࡨࡧࡳࡦ࠮ࠣࡹࡸ࡫ࡲࠡࡪࡤࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠ࡮ࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡸࡵࡵࡳࡥࡨࠤࡼ࡯ࡴࡩࠢࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠢ࡬ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦࠧࠨ⬭")
            source = orchestration_metadata[bstack1l1llll_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ⬮")].get(bstack1l1llll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ⬯"), [])
            bstack1l1llll11lll_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1l1llll_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ⬰")].get(bstack1l1llll_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ⬱"), False) and not bstack1l1llll11lll_opy_:
                bstack1l1llll11l1l_opy_ = bstack1lll1lll1lll_opy_(source) # bstack1l1llll1l1l1_opy_-repo is handled bstack1l1llll1l111_opy_
            payload = {
                bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ⬲"): [{bstack1l1llll_opy_ (u"ࠨࡦࡪ࡮ࡨࡔࡦࡺࡨࠣ⬳"): f} for f in test_files],
                bstack1l1llll_opy_ (u"ࠢࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡓࡵࡴࡤࡸࡪ࡭ࡹࠣ⬴"): orchestration_strategy,
                bstack1l1llll_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡎࡧࡷࡥࡩࡧࡴࡢࠤ⬵"): orchestration_metadata,
                bstack1l1llll_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧ⬶"): int(os.environ.get(bstack1l1llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨ⬷")) or bstack1l1llll_opy_ (u"ࠦ࠵ࠨ⬸")),
                bstack1l1llll_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤ⬹"): int(os.environ.get(bstack1l1llll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣ⬺")) or bstack1l1llll_opy_ (u"ࠢ࠲ࠤ⬻")),
                bstack1l1llll_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨ⬼"): self.config.get(bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⬽"), bstack1l1llll_opy_ (u"ࠪࠫ⬾")),
                bstack1l1llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢ⬿"): self.config.get(bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ⭀"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ⭁"): os.environ.get(bstack1l1llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࠨ⭂"), bstack1l1llll_opy_ (u"ࠣࠤ⭃")),
                bstack1l1llll_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦ⭄"): get_host_info(),
                bstack1l1llll_opy_ (u"ࠥࡴࡷࡊࡥࡵࡣ࡬ࡰࡸࠨ⭅"): bstack1l1llll11l1l_opy_
            }
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻ࠢࡾࢁࠧ⭆").format(payload))
            response = bstack11111l111ll_opy_.bstack1ll1111llll1_opy_(self.bstack1l1llll11l11_opy_, payload)
            if response:
                self.bstack1l1llll1l11l_opy_ = self._1l1llll1lll1_opy_(response)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⭇").format(self.bstack1l1llll1l11l_opy_))
            else:
                self.logger.error(bstack1l1llll_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠳ࠨ⭈"))
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽࠾ࠥࢁࡽࠣ⭉").format(e))
    def _1l1llll1lll1_opy_(self, response):
        bstack1l1llll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡤࡲࡩࠦࡥࡹࡶࡵࡥࡨࡺࡳࠡࡴࡨࡰࡪࡼࡡ࡯ࡶࠣࡪ࡮࡫࡬ࡥࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⭊")
        bstack1ll11l11l1_opy_ = {}
        bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ⭋")] = response.get(bstack1l1llll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ⭌"), self.default_timeout)
        bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ⭍")] = response.get(bstack1l1llll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ⭎"), self.bstack1l1llll1ll11_opy_)
        bstack1l1llll1ll1l_opy_ = response.get(bstack1l1llll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ⭏"))
        bstack1l1lllll1111_opy_ = response.get(bstack1l1llll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ⭐"))
        if bstack1l1llll1ll1l_opy_:
            bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ⭑")] = bstack1l1llll1ll1l_opy_.split(bstack1111111l1ll_opy_ + bstack1l1llll_opy_ (u"ࠤ࠲ࠦ⭒"))[1] if bstack1111111l1ll_opy_ + bstack1l1llll_opy_ (u"ࠥ࠳ࠧ⭓") in bstack1l1llll1ll1l_opy_ else bstack1l1llll1ll1l_opy_
        else:
            bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ⭔")] = None
        if bstack1l1lllll1111_opy_:
            bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ⭕")] = bstack1l1lllll1111_opy_.split(bstack1111111l1ll_opy_ + bstack1l1llll_opy_ (u"ࠨ࠯ࠣ⭖"))[1] if bstack1111111l1ll_opy_ + bstack1l1llll_opy_ (u"ࠢ࠰ࠤ⭗") in bstack1l1lllll1111_opy_ else bstack1l1lllll1111_opy_
        else:
            bstack1ll11l11l1_opy_[bstack1l1llll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ⭘")] = None
        if (
            response.get(bstack1l1llll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ⭙")) is None or
            response.get(bstack1l1llll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ⭚")) is None or
            response.get(bstack1l1llll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ⭛")) is None or
            response.get(bstack1l1llll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ⭜")) is None
        ):
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡛ࡱࡴࡲࡧࡪࡹࡳࡠࡵࡳࡰ࡮ࡺ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡵࡳࡳࡳࡹࡥ࡞ࠢࡕࡩࡨ࡫ࡩࡷࡧࡧࠤࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥࠩࡵࠬࠤ࡫ࡵࡲࠡࡵࡲࡱࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦࡵࠣ࡭ࡳࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ⭝"))
        return bstack1ll11l11l1_opy_
    def bstack1ll1lll11lll_opy_(self):
        if not self.bstack1l1llll1l11l_opy_:
            self.logger.error(bstack1l1llll_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸ࠴ࠢ⭞"))
            return None
        bstack1l1llll1l1ll_opy_ = None
        test_files = []
        bstack1l1lllll11l1_opy_ = int(time.time() * 1000) # bstack1l1lllll111l_opy_ sec
        bstack1l1llll111ll_opy_ = int(self.bstack1l1llll1l11l_opy_.get(bstack1l1llll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ⭟"), self.bstack1l1llll1ll11_opy_))
        bstack1l1llll1llll_opy_ = int(self.bstack1l1llll1l11l_opy_.get(bstack1l1llll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ⭠"), self.default_timeout)) * 1000
        bstack1l1lllll1111_opy_ = self.bstack1l1llll1l11l_opy_.get(bstack1l1llll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ⭡"), None)
        bstack1l1llll1ll1l_opy_ = self.bstack1l1llll1l11l_opy_.get(bstack1l1llll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ⭢"), None)
        if bstack1l1llll1ll1l_opy_ is None and bstack1l1lllll1111_opy_ is None:
            return None
        try:
            while bstack1l1llll1ll1l_opy_ and (time.time() * 1000 - bstack1l1lllll11l1_opy_) < bstack1l1llll1llll_opy_:
                response = bstack11111l111ll_opy_.bstack1ll111l111l1_opy_(bstack1l1llll1ll1l_opy_, {})
                if response and response.get(bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ⭣")):
                    bstack1l1llll1l1ll_opy_ = response.get(bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ⭤"))
                self.bstack1l1llll11ll1_opy_ += 1
                if bstack1l1llll1l1ll_opy_:
                    break
                time.sleep(bstack1l1llll111ll_opy_)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡴࡨࡷࡺࡲࡴࠡࡗࡕࡐࠥࡧࡦࡵࡧࡵࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡾࢁࠥࡹࡥࡤࡱࡱࡨࡸ࠴ࠢ⭥").format(bstack1l1llll111ll_opy_))
            if bstack1l1lllll1111_opy_ and not bstack1l1llll1l1ll_opy_:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡭ࡲ࡫࡯ࡶࡶ࡙ࠣࡗࡒࠢ⭦"))
                response = bstack11111l111ll_opy_.bstack1ll111l111l1_opy_(bstack1l1lllll1111_opy_, {})
                if response and response.get(bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ⭧")):
                    bstack1l1llll1l1ll_opy_ = response.get(bstack1l1llll_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ⭨"))
            if bstack1l1llll1l1ll_opy_ and len(bstack1l1llll1l1ll_opy_) > 0:
                for test_data in bstack1l1llll1l1ll_opy_:
                    file_path = test_data.get(bstack1l1llll_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ⭩"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1l1llll1l1ll_opy_:
                return None
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡏࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡷ࡫ࡣࡦ࡫ࡹࡩࡩࡀࠠࡼࡿࠥ⭪").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥ⭫").format(e))
            return None
    def bstack1ll1lll11l11_opy_(self):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡣࡢ࡮࡯ࡷࠥࡳࡡࡥࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⭬")
        return self.bstack1l1llll11ll1_opy_