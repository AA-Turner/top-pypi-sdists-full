# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import time
from bstack_utils.bstack1111l11l111_opy_ import bstack1111l111lll_opy_
from bstack_utils.constants import bstack11111ll1l1l_opy_
from bstack_utils.helper import get_host_info, bstack1llll11l1111_opy_
class bstack1lll1l11l1l1_opy_:
    bstack111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡥࡳࡪ࡬ࡦࡵࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡲࡷࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ✪")
    def __init__(self, config, logger):
        bstack111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡦ࡬ࡧࡹ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡥࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡶࡸࡷ࠲ࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢࡱࡥࡲ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ✫")
        self.config = config
        self.logger = logger
        self.bstack1ll11ll1l111_opy_ = bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡳࡰ࡮ࡺ࠭ࡵࡧࡶࡸࡸࠨ✬")
        self.bstack1ll11ll11ll1_opy_ = None
        self.default_timeout = 60
        self.bstack1ll11ll11lll_opy_ = 5
        self.bstack1ll11l1ll1ll_opy_ = 0
    def bstack1lll1l11l1ll_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡌࡲ࡮ࡺࡩࡢࡶࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡹࡴࡰࡴࡨࡷࠥࡺࡨࡦࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡰࡰ࡮࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ✭")
        self.logger.debug(bstack111l_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡏ࡮ࡪࡶ࡬ࡥࡹ࡯࡮ࡨࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡽࢀࠦ✮").format(orchestration_strategy))
        try:
            bstack1ll11ll11l1l_opy_ = []
            bstack111l_opy_ (u"ࠢࠣࠤ࡚ࡩࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡧࡧࡷࡧ࡭ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡯ࡳࠡࡵࡲࡹࡷࡩࡥࠡ࡫ࡶࠤࡹࡿࡰࡦࠢࡲࡪࠥࡧࡲࡳࡣࡼࠤࡦࡴࡤࠡ࡫ࡷࠫࡸࠦࡥ࡭ࡧࡰࡩࡳࡺࡳࠡࡣࡵࡩࠥࡵࡦࠡࡶࡼࡴࡪࠦࡤࡪࡥࡷࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡩࡨࡧࡵࡴࡧࠣ࡭ࡳࠦࡴࡩࡣࡷࠤࡨࡧࡳࡦ࠮ࠣࡹࡸ࡫ࡲࠡࡪࡤࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠ࡮ࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡸࡵࡵࡳࡥࡨࠤࡼ࡯ࡴࡩࠢࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠢ࡬ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦࠧࠨ✯")
            source = orchestration_metadata[bstack111l_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧ✰")].get(bstack111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ✱"), [])
            bstack1ll11l1llll1_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack111l_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩ✲")].get(bstack111l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬ✳"), False) and not bstack1ll11l1llll1_opy_:
                bstack1ll11ll11l1l_opy_ = bstack1llll11l1111_opy_(source) # bstack1ll11ll1l11l_opy_-repo is handled bstack1ll11ll11111_opy_
            payload = {
                bstack111l_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ✴"): [{bstack111l_opy_ (u"ࠨࡦࡪ࡮ࡨࡔࡦࡺࡨࠣ✵"): f} for f in test_files],
                bstack111l_opy_ (u"ࠢࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡓࡵࡴࡤࡸࡪ࡭ࡹࠣ✶"): orchestration_strategy,
                bstack111l_opy_ (u"ࠣࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡎࡧࡷࡥࡩࡧࡴࡢࠤ✷"): orchestration_metadata,
                bstack111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧ✸"): int(os.environ.get(bstack111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨ✹")) or bstack111l_opy_ (u"ࠦ࠵ࠨ✺")),
                bstack111l_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤ✻"): int(os.environ.get(bstack111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣ✼")) or bstack111l_opy_ (u"ࠢ࠲ࠤ✽")),
                bstack111l_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨ✾"): self.config.get(bstack111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ✿"), bstack111l_opy_ (u"ࠪࠫ❀")),
                bstack111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢ❁"): self.config.get(bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ❂"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ❃"): os.environ.get(bstack111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࠨ❄"), bstack111l_opy_ (u"ࠣࠤ❅")),
                bstack111l_opy_ (u"ࠤ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠦ❆"): get_host_info(),
                bstack111l_opy_ (u"ࠥࡴࡷࡊࡥࡵࡣ࡬ࡰࡸࠨ❇"): bstack1ll11ll11l1l_opy_
            }
            self.logger.debug(bstack111l_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳ࠻ࠢࡾࢁࠧ❈").format(payload))
            response = bstack1111l111lll_opy_.bstack1ll1l1111l1l_opy_(self.bstack1ll11ll1l111_opy_, payload)
            if response:
                self.bstack1ll11ll11ll1_opy_ = self._1ll11l1lllll_opy_(response)
                self.logger.debug(bstack111l_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡘࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ❉").format(self.bstack1ll11ll11ll1_opy_))
            else:
                self.logger.error(bstack111l_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠳ࠨ❊"))
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠢ࡜ࡵࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽࠾ࠥࢁࡽࠣ❋").format(e))
    def _1ll11l1lllll_opy_(self, response):
        bstack111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡤࡲࡩࠦࡥࡹࡶࡵࡥࡨࡺࡳࠡࡴࡨࡰࡪࡼࡡ࡯ࡶࠣࡪ࡮࡫࡬ࡥࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ❌")
        bstack11l1l1l1l1_opy_ = {}
        bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ❍")] = response.get(bstack111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ❎"), self.default_timeout)
        bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ❏")] = response.get(bstack111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ❐"), self.bstack1ll11ll11lll_opy_)
        bstack1ll11ll111ll_opy_ = response.get(bstack111l_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡛ࡲ࡭ࠤ❑"))
        bstack1ll11l1lll11_opy_ = response.get(bstack111l_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ❒"))
        if bstack1ll11ll111ll_opy_:
            bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ❓")] = bstack1ll11ll111ll_opy_.split(bstack11111ll1l1l_opy_ + bstack111l_opy_ (u"ࠤ࠲ࠦ❔"))[1] if bstack11111ll1l1l_opy_ + bstack111l_opy_ (u"ࠥ࠳ࠧ❕") in bstack1ll11ll111ll_opy_ else bstack1ll11ll111ll_opy_
        else:
            bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ❖")] = None
        if bstack1ll11l1lll11_opy_:
            bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ❗")] = bstack1ll11l1lll11_opy_.split(bstack11111ll1l1l_opy_ + bstack111l_opy_ (u"ࠨ࠯ࠣ❘"))[1] if bstack11111ll1l1l_opy_ + bstack111l_opy_ (u"ࠢ࠰ࠤ❙") in bstack1ll11l1lll11_opy_ else bstack1ll11l1lll11_opy_
        else:
            bstack11l1l1l1l1_opy_[bstack111l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ❚")] = None
        if (
            response.get(bstack111l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ❛")) is None or
            response.get(bstack111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ❜")) is None or
            response.get(bstack111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ❝")) is None or
            response.get(bstack111l_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ❞")) is None
        ):
            self.logger.debug(bstack111l_opy_ (u"ࠨ࡛ࡱࡴࡲࡧࡪࡹࡳࡠࡵࡳࡰ࡮ࡺ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡵࡳࡳࡳࡹࡥ࡞ࠢࡕࡩࡨ࡫ࡩࡷࡧࡧࠤࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥࠩࡵࠬࠤ࡫ࡵࡲࠡࡵࡲࡱࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦࡵࠣ࡭ࡳࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡆࡖࡉࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ❟"))
        return bstack11l1l1l1l1_opy_
    def bstack1lll1l111lll_opy_(self):
        if not self.bstack1ll11ll11ll1_opy_:
            self.logger.error(bstack111l_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸ࠴ࠢ❠"))
            return None
        bstack1ll11l1ll1l1_opy_ = None
        test_files = []
        bstack1ll11ll1111l_opy_ = int(time.time() * 1000) # bstack1ll11ll11l11_opy_ sec
        bstack1ll11ll111l1_opy_ = int(self.bstack1ll11ll11ll1_opy_.get(bstack111l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ❡"), self.bstack1ll11ll11lll_opy_))
        bstack1ll11l1lll1l_opy_ = int(self.bstack1ll11ll11ll1_opy_.get(bstack111l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ❢"), self.default_timeout)) * 1000
        bstack1ll11l1lll11_opy_ = self.bstack1ll11ll11ll1_opy_.get(bstack111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ❣"), None)
        bstack1ll11ll111ll_opy_ = self.bstack1ll11ll11ll1_opy_.get(bstack111l_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ❤"), None)
        if bstack1ll11ll111ll_opy_ is None and bstack1ll11l1lll11_opy_ is None:
            return None
        try:
            while bstack1ll11ll111ll_opy_ and (time.time() * 1000 - bstack1ll11ll1111l_opy_) < bstack1ll11l1lll1l_opy_:
                response = bstack1111l111lll_opy_.bstack1ll1l111l11l_opy_(bstack1ll11ll111ll_opy_, {})
                if response and response.get(bstack111l_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ❥")):
                    bstack1ll11l1ll1l1_opy_ = response.get(bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ❦"))
                self.bstack1ll11l1ll1ll_opy_ += 1
                if bstack1ll11l1ll1l1_opy_:
                    break
                time.sleep(bstack1ll11ll111l1_opy_)
                self.logger.debug(bstack111l_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡴࡨࡷࡺࡲࡴࠡࡗࡕࡐࠥࡧࡦࡵࡧࡵࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡾࢁࠥࡹࡥࡤࡱࡱࡨࡸ࠴ࠢ❧").format(bstack1ll11ll111l1_opy_))
            if bstack1ll11l1lll11_opy_ and not bstack1ll11l1ll1l1_opy_:
                self.logger.debug(bstack111l_opy_ (u"ࠣ࡝ࡪࡩࡹࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳ࡞ࠢࡉࡩࡹࡩࡨࡪࡰࡪࠤࡴࡸࡤࡦࡴࡨࡨࠥࡺࡥࡴࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡭ࡲ࡫࡯ࡶࡶ࡙ࠣࡗࡒࠢ❨"))
                response = bstack1111l111lll_opy_.bstack1ll1l111l11l_opy_(bstack1ll11l1lll11_opy_, {})
                if response and response.get(bstack111l_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ❩")):
                    bstack1ll11l1ll1l1_opy_ = response.get(bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ❪"))
            if bstack1ll11l1ll1l1_opy_ and len(bstack1ll11l1ll1l1_opy_) > 0:
                for bstack1llll1ll111_opy_ in bstack1ll11l1ll1l1_opy_:
                    file_path = bstack1llll1ll111_opy_.get(bstack111l_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ❫"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1ll11l1ll1l1_opy_:
                return None
            self.logger.debug(bstack111l_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡏࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡷ࡫ࡣࡦ࡫ࡹࡩࡩࡀࠠࡼࡿࠥ❬").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࡀࠠࡼࡿࠥ❭").format(e))
            return None
    def bstack1lll1l1l1111_opy_(self):
        bstack111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡣࡢ࡮࡯ࡷࠥࡳࡡࡥࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ❮")
        return self.bstack1ll11l1ll1ll_opy_