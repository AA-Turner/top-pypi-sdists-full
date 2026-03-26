# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import glob
import time
from bstack_utils.bstack111l11l1_opy_ import bstack111lll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
class bstack111l11111l_opy_:
    def __init__(self, args, logger, bstack1lllllll11l_opy_, bstack1llllll1l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll11l_opy_ = bstack1lllllll11l_opy_
        self.bstack1llllll1l11_opy_ = bstack1llllll1l11_opy_
        self.bstack11llll1l11_opy_ = []
    def _1lllllll111_opy_(self, bstack11llll1l11_opy_):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࡆࡺࡳࡥࡳࡪࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡳࡪࠠࡨ࡮ࡲࡦ࠲ࡶࡡࡵࡶࡨࡶࡳࠦࡥ࡯ࡶࡵ࡭ࡪࡹࠠࡪࡰࠣࡷࡵ࡫ࡣࡠࡨ࡬ࡰࡪࡹࠠࡵࡱࠣ࡭ࡳࡪࡩࡷ࡫ࡧࡹࡦࡲࠠ࠯ࡨࡨࡥࡹࡻࡲࡦࠢࡩ࡭ࡱ࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡌࡦࡴࡤ࡭ࡧࡶࠤࡹ࡮ࡲࡦࡧࠣࡧࡦࡹࡥࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠶࠴ࠠࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࠬࡪ࠴ࡧ࠯ࠢࠪࡪࡪࡧࡴࡶࡴࡨࡷࠬ࠯ࠠ⠕ࠢࡺࡥࡱࡱࡳࠡࡴࡨࡧࡺࡸࡳࡪࡸࡨࡰࡾࠦࡦࡰࡴࠣ࠮࠳࡬ࡥࡢࡶࡸࡶࡪࠦࡦࡪ࡮ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠳࠰ࠣࡋࡱࡵࡢࠡࡲࡤࡸࡹ࡫ࡲ࡯ࠢࠫࡩ࠳࡭࠮ࠡࠩࡩࡩࡦࡺࡵࡳࡧࡶ࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧࠪࠢ⠗ࠤࡪࡾࡰࡢࡰࡧࡷࠥࡼࡩࡢࠢࡪࡰࡴࡨ࠮ࡨ࡮ࡲࡦ࠭࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠶࠲ࠥࡖ࡬ࡢ࡫ࡱࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࠠ⠕ࠢ࡮ࡩࡵࡺࠠࡢࡵ࠰࡭ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡤࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡰࡴࠣࡹࡳ࡫ࡸࡱࡣࡱࡨࡪࡪࠠࡨ࡮ࡲࡦࠥࡺ࡯ࠡࡶ࡫ࡩ࡚ࠥࡏࠡࡵࡳࡰ࡮ࡺ࠭ࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡱࡪࡧ࡮ࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡫ࠠࡴࡧࡵࡺࡪࡸࠠࡩࡣࡶࠤࡳࡵࠠࡷ࡫ࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤ࡮ࡴࡴࡰࠢ࡬ࡲࡩ࡯ࡶࡪࡦࡸࡥࡱࠦࡳࡱࡧࡦࡷࠥࡧ࡮ࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡴࡸࡤࡦࡴࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡥ࡮ࠢࡰࡩࡦࡴࡩ࡯ࡩࡩࡹࡱࡲࡹ࠯ࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡦࡰࡶࡹࡷ࡫ࡳࠡࡩࡵࡥࡳࡻ࡬ࡢࡴࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡢࡴࡨࠤࡸ࡫࡮ࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢၦ")
        expanded = []
        for entry in bstack11llll1l11_opy_:
            if os.path.isdir(entry):
                bstack1lllllll1_opy_ = sorted(
                    glob.glob(os.path.join(entry, bstack1ll1lll_opy_ (u"࠭ࠪࠫࠩၧ"), bstack1ll1lll_opy_ (u"ࠧࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪၨ")), recursive=True)
                )
                if bstack1lllllll1_opy_:
                    expanded.extend(bstack1lllllll1_opy_)
                else:
                    expanded.append(entry)
            elif any(c in entry for c in (bstack1ll1lll_opy_ (u"ࠨࠬࠪၩ"), bstack1ll1lll_opy_ (u"ࠩࡂࠫၪ"), bstack1ll1lll_opy_ (u"ࠪ࡟ࠬၫ"))):
                bstack1lllllll1_opy_ = sorted(glob.glob(entry, recursive=True))
                if bstack1lllllll1_opy_:
                    expanded.extend(bstack1lllllll1_opy_)
                else:
                    expanded.append(entry)
            else:
                expanded.append(entry)
        return expanded
    @measure(event_name=EVENTS.bstack1lllllll1l1_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack1ll1111lll_opy_(self):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡁࡱࡲ࡯ࡽࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡪࡨࠣࡩࡳࡧࡢ࡭ࡧࡧࠦࠧࠨၬ")
        bstack111l11l1_opy_ = bstack111lll11_opy_.get_instance(self.bstack1lllllll11l_opy_, self.logger)
        if bstack111l11l1_opy_ is None:
            self.logger.warn(bstack1ll1lll_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࡩࡴࠢࡱࡳࡹࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧ࠲࡙ࠥ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣၭ"))
            return
        bstack1lllllll1ll_opy_ = False
        bstack111l11l1_opy_.bstack1llllll1ll1_opy_(bstack1ll1lll_opy_ (u"ࠨࡥ࡯ࡣࡥࡰࡪࡪࠢၮ"), bstack111l11l1_opy_.bstack1l11llll_opy_())
        start_time = time.time()
        if bstack111l11l1_opy_.bstack1l11llll_opy_():
            test_files = self._1lllllll111_opy_(self.bstack11llll1l11_opy_)
            bstack1lllllll1ll_opy_ = True
            bstack1llllll1lll_opy_ = bstack111l11l1_opy_.bstack1llllll1l1l_opy_(test_files)
            if bstack1llllll1lll_opy_:
                self.bstack11llll1l11_opy_ = [item.replace(bstack1ll1lll_opy_ (u"ࠧ࡝࡞ࠪၯ"), bstack1ll1lll_opy_ (u"ࠨ࠱ࠪၰ")) for item in bstack1llllll1lll_opy_]
                bstack111l11l1_opy_.bstack1llllll11ll_opy_(bstack1lllllll1ll_opy_)
                self.logger.info(bstack1ll1lll_opy_ (u"ࠤࡗࡩࡸࡺࡳࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡺࡹࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢၱ").format(self.bstack11llll1l11_opy_))
            else:
                self.logger.info(bstack1ll1lll_opy_ (u"ࠥࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻࡪࡸࡥࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡧࡿࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣၲ"))
        bstack111l11l1_opy_.bstack1llllll1ll1_opy_(bstack1ll1lll_opy_ (u"ࠦࡹ࡯࡭ࡦࡖࡤ࡯ࡪࡴࡔࡰࡃࡳࡴࡱࡿࠢၳ"), int((time.time() - start_time) * 1000))
    def bstack111lllllll_opy_(self, bstack11llll1l11_opy_):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࡔࡧࡷࠤࡹ࡮ࡥࠡࡨࡨࡥࡹࡻࡲࡦࠢࡩ࡭ࡱ࡫ࡳࠡࡶࡲࠤࡧ࡫ࠠࡦࡺࡨࡧࡺࡺࡥࡥࠤࠥࠦၴ")
        self.bstack11llll1l11_opy_ = bstack11llll1l11_opy_
    def bstack1l1l11lll1_opy_(self):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡩࡩࡦࡺࡵࡳࡧࠣࡪ࡮ࡲࡥࡴࠤࠥࠦၵ")
        return self.bstack11llll1l11_opy_