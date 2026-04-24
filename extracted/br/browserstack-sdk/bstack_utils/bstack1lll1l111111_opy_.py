# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import time
from bstack_utils.bstack1111l111l1l_opy_ import bstack1111l1111ll_opy_
from bstack_utils.constants import bstack1111111ll11_opy_
from bstack_utils.helper import get_host_info, bstack1llll11ll111_opy_
class bstack1lll11llllll_opy_:
    bstack111ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡸࡶࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ❡")
    def __init__(self, config, logger):
        bstack111ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡥ࡫ࡦࡸ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡤࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡵࡷࡶ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡࡰࡤࡱࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ❢")
        self.config = config
        self.logger = logger
        self.bstack1ll11l1l11ll_opy_ = bstack111ll11_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡲ࡯࡭ࡹ࠳ࡴࡦࡵࡷࡷࠧ❣")
        self.bstack1ll11l1l111l_opy_ = None
        self.default_timeout = 60
        self.bstack1ll11l11l1l1_opy_ = 5
        self.bstack1ll11l11l111_opy_ = 0
    def bstack1lll11ll1lll_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack111ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡱ࡭ࡹ࡯ࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡸࡺ࡯ࡳࡧࡶࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡶ࡯࡭࡮࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ❤")
        self.logger.debug(bstack111ll11_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡎࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥ❥").format(orchestration_strategy))
        try:
            bstack1ll11l1l1ll1_opy_ = []
            bstack111ll11_opy_ (u"ࠨ࡙ࠢࠣࡨࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡦࡦࡶࡦ࡬ࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡮ࡹࠠࡴࡱࡸࡶࡨ࡫ࠠࡪࡵࠣࡸࡾࡶࡥࠡࡱࡩࠤࡦࡸࡲࡢࡻࠣࡥࡳࡪࠠࡪࡶࠪࡷࠥ࡫࡬ࡦ࡯ࡨࡲࡹࡹࠠࡢࡴࡨࠤࡴ࡬ࠠࡵࡻࡳࡩࠥࡪࡩࡤࡶࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡲࠥࡺࡨࡢࡶࠣࡧࡦࡹࡥ࠭ࠢࡸࡷࡪࡸࠠࡩࡣࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦ࡭ࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡷࡴࡻࡲࡤࡧࠣࡻ࡮ࡺࡨࠡࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠡ࡫ࡱࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥࠦࠧ❦")
            source = orchestration_metadata[bstack111ll11_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭❧")].get(bstack111ll11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ❨"), [])
            bstack1ll11l11l1ll_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack111ll11_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨ❩")].get(bstack111ll11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ❪"), False) and not bstack1ll11l11l1ll_opy_:
                bstack1ll11l1l1ll1_opy_ = bstack1llll11ll111_opy_(source) # bstack1ll11l1l11l1_opy_-repo is handled bstack1ll11l11ll11_opy_
            payload = {
                bstack111ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ❫"): [{bstack111ll11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢ❬"): f} for f in test_files],
                bstack111ll11_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠢ❭"): orchestration_strategy,
                bstack111ll11_opy_ (u"ࠢࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡍࡦࡶࡤࡨࡦࡺࡡࠣ❮"): orchestration_metadata,
                bstack111ll11_opy_ (u"ࠣࡰࡲࡨࡪࡏ࡮ࡥࡧࡻࠦ❯"): int(os.environ.get(bstack111ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧ❰")) or bstack111ll11_opy_ (u"ࠥ࠴ࠧ❱")),
                bstack111ll11_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࡑࡳࡩ࡫ࡳࠣ❲"): int(os.environ.get(bstack111ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢ❳")) or bstack111ll11_opy_ (u"ࠨ࠱ࠣ❴")),
                bstack111ll11_opy_ (u"ࠢࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠧ❵"): self.config.get(bstack111ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭❶"), bstack111ll11_opy_ (u"ࠩࠪ❷")),
                bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠨ❸"): self.config.get(bstack111ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ❹"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ❺"): os.environ.get(bstack111ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠧ❻"), bstack111ll11_opy_ (u"ࠢࠣ❼")),
                bstack111ll11_opy_ (u"ࠣࡪࡲࡷࡹࡏ࡮ࡧࡱࠥ❽"): get_host_info(),
                bstack111ll11_opy_ (u"ࠤࡳࡶࡉ࡫ࡴࡢ࡫࡯ࡷࠧ❾"): bstack1ll11l1l1ll1_opy_
            }
            self.logger.debug(bstack111ll11_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦ❿").format(payload))
            response = bstack1111l1111ll_opy_.bstack1ll11lll11l1_opy_(self.bstack1ll11l1l11ll_opy_, payload)
            if response:
                self.bstack1ll11l1l111l_opy_ = self._1ll11l11l11l_opy_(response)
                self.logger.debug(bstack111ll11_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ➀").format(self.bstack1ll11l1l111l_opy_))
            else:
                self.logger.error(bstack111ll11_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࠧ➁"))
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼࠽ࠤࢀࢃࠢ➂").format(e))
    def _1ll11l11l11l_opy_(self, response):
        bstack111ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡣࡱࡨࠥ࡫ࡸࡵࡴࡤࡧࡹࡹࠠࡳࡧ࡯ࡩࡻࡧ࡮ࡵࠢࡩ࡭ࡪࡲࡤࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ➃")
        bstack1l111l1l1_opy_ = {}
        bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ➄")] = response.get(bstack111ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ➅"), self.default_timeout)
        bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ➆")] = response.get(bstack111ll11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ➇"), self.bstack1ll11l11l1l1_opy_)
        bstack1ll11l11llll_opy_ = response.get(bstack111ll11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ➈"))
        bstack1ll11l1l1111_opy_ = response.get(bstack111ll11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ➉"))
        if bstack1ll11l11llll_opy_:
            bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥ➊")] = bstack1ll11l11llll_opy_.split(bstack1111111ll11_opy_ + bstack111ll11_opy_ (u"ࠣ࠱ࠥ➋"))[1] if bstack1111111ll11_opy_ + bstack111ll11_opy_ (u"ࠤ࠲ࠦ➌") in bstack1ll11l11llll_opy_ else bstack1ll11l11llll_opy_
        else:
            bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ➍")] = None
        if bstack1ll11l1l1111_opy_:
            bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ➎")] = bstack1ll11l1l1111_opy_.split(bstack1111111ll11_opy_ + bstack111ll11_opy_ (u"ࠧ࠵ࠢ➏"))[1] if bstack1111111ll11_opy_ + bstack111ll11_opy_ (u"ࠨ࠯ࠣ➐") in bstack1ll11l1l1111_opy_ else bstack1ll11l1l1111_opy_
        else:
            bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ➑")] = None
        if (
            response.get(bstack111ll11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ➒")) is None or
            response.get(bstack111ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ➓")) is None or
            response.get(bstack111ll11_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ➔")) is None or
            response.get(bstack111ll11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢ➕")) is None
        ):
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡡࡰࡳࡱࡦࡩࡸࡹ࡟ࡴࡲ࡯࡭ࡹࡥࡴࡦࡵࡷࡷࡤࡸࡥࡴࡲࡲࡲࡸ࡫࡝ࠡࡔࡨࡧࡪ࡯ࡶࡦࡦࠣࡲࡺࡲ࡬ࠡࡸࡤࡰࡺ࡫ࠨࡴࠫࠣࡪࡴࡸࠠࡴࡱࡰࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥࡴࠢ࡬ࡲࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤ➖"))
        return bstack1l111l1l1_opy_
    def bstack1lll11llll11_opy_(self):
        if not self.bstack1ll11l1l111l_opy_:
            self.logger.error(bstack111ll11_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠳ࠨ➗"))
            return None
        bstack1ll11l1l1l1l_opy_ = None
        test_files = []
        bstack1ll11l11ll1l_opy_ = int(time.time() * 1000) # bstack1ll11l11lll1_opy_ sec
        bstack1ll11l111lll_opy_ = int(self.bstack1ll11l1l111l_opy_.get(bstack111ll11_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ➘"), self.bstack1ll11l11l1l1_opy_))
        bstack1ll11l1l1l11_opy_ = int(self.bstack1ll11l1l111l_opy_.get(bstack111ll11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ➙"), self.default_timeout)) * 1000
        bstack1ll11l1l1111_opy_ = self.bstack1ll11l1l111l_opy_.get(bstack111ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ➚"), None)
        bstack1ll11l11llll_opy_ = self.bstack1ll11l1l111l_opy_.get(bstack111ll11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ➛"), None)
        if bstack1ll11l11llll_opy_ is None and bstack1ll11l1l1111_opy_ is None:
            return None
        try:
            while bstack1ll11l11llll_opy_ and (time.time() * 1000 - bstack1ll11l11ll1l_opy_) < bstack1ll11l1l1l11_opy_:
                response = bstack1111l1111ll_opy_.bstack1ll11lll1ll1_opy_(bstack1ll11l11llll_opy_, {})
                if response and response.get(bstack111ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ➜")):
                    bstack1ll11l1l1l1l_opy_ = response.get(bstack111ll11_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦ➝"))
                self.bstack1ll11l11l111_opy_ += 1
                if bstack1ll11l1l1l1l_opy_:
                    break
                time.sleep(bstack1ll11l111lll_opy_)
                self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡳࡧࡶࡹࡱࡺࠠࡖࡔࡏࠤࡦ࡬ࡴࡦࡴࠣࡻࡦ࡯ࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡽࢀࠤࡸ࡫ࡣࡰࡰࡧࡷ࠳ࠨ➞").format(bstack1ll11l111lll_opy_))
            if bstack1ll11l1l1111_opy_ and not bstack1ll11l1l1l1l_opy_:
                self.logger.debug(bstack111ll11_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡬ࡱࡪࡵࡵࡵࠢࡘࡖࡑࠨ➟"))
                response = bstack1111l1111ll_opy_.bstack1ll11lll1ll1_opy_(bstack1ll11l1l1111_opy_, {})
                if response and response.get(bstack111ll11_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ➠")):
                    bstack1ll11l1l1l1l_opy_ = response.get(bstack111ll11_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ➡"))
            if bstack1ll11l1l1l1l_opy_ and len(bstack1ll11l1l1l1l_opy_) > 0:
                for bstack1llll1l11ll_opy_ in bstack1ll11l1l1l1l_opy_:
                    file_path = bstack1llll1l11ll_opy_.get(bstack111ll11_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧ➢"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1ll11l1l1l1l_opy_:
                return None
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡕࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡶࡪࡩࡥࡪࡸࡨࡨ࠿ࠦࡻࡾࠤ➣").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤ➤").format(e))
            return None
    def bstack1lll11lll1ll_opy_(self):
        bstack111ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡩࡡ࡭࡮ࡶࠤࡲࡧࡤࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ➥")
        return self.bstack1ll11l11l111_opy_