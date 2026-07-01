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
import glob
import time
from bstack_utils.bstack1llll1ll_opy_ import bstack1ll1l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
class bstack1lll11l1_opy_:
    def __init__(self, args, logger, bstack1ll1llll_opy_, bstack1ll1l11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1ll1llll_opy_ = bstack1ll1llll_opy_
        self.bstack1ll1l11l_opy_ = bstack1ll1l11l_opy_
        self.bstack1lll1lll_opy_ = []
    def _1lll111l_opy_(self, bstack1lll1lll_opy_):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡈࡼࡵࡧ࡮ࡥࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧ࡮ࡥࠢࡪࡰࡴࡨ࠭ࡱࡣࡷࡸࡪࡸ࡮ࠡࡧࡱࡸࡷ࡯ࡥࡴࠢ࡬ࡲࠥࡹࡰࡦࡥࡢࡪ࡮ࡲࡥࡴࠢࡷࡳࠥ࡯࡮ࡥ࡫ࡹ࡭ࡩࡻࡡ࡭ࠢ࠱ࡪࡪࡧࡴࡶࡴࡨࠤ࡫࡯࡬ࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡎࡡ࡯ࡦ࡯ࡩࡸࠦࡴࡩࡴࡨࡩࠥࡩࡡࡴࡧࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠱࠯ࠢࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࠮ࡥ࠯ࡩ࠱ࠤࠬ࡬ࡥࡢࡶࡸࡶࡪࡹࠧࠪࠢ⠗ࠤࡼࡧ࡬࡬ࡵࠣࡶࡪࡩࡵࡳࡵ࡬ࡺࡪࡲࡹࠡࡨࡲࡶࠥ࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠡࡨ࡬ࡰࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠵࠲ࠥࡍ࡬ࡰࡤࠣࡴࡦࡺࡴࡦࡴࡱࠤ࠭࡫࠮ࡨ࠰ࠣࠫ࡫࡫ࡡࡵࡷࡵࡩࡸ࠵ࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠩࠬࠤ⠙ࠦࡥࡹࡲࡤࡲࡩࡹࠠࡷ࡫ࡤࠤ࡬ࡲ࡯ࡣ࠰ࡪࡰࡴࡨࠨࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠸࠴ࠠࡑ࡮ࡤ࡭ࡳࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࠢ⠗ࠤࡰ࡫ࡰࡵࠢࡤࡷ࠲࡯ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡪࡰࡪࠤࡦࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡲࡶࠥࡻ࡮ࡦࡺࡳࡥࡳࡪࡥࡥࠢࡪࡰࡴࡨࠠࡵࡱࠣࡸ࡭࡫ࠠࡕࡑࠣࡷࡵࡲࡩࡵ࠯ࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡳࡥࡢࡰࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡶࡩࡷࡼࡥࡳࠢ࡫ࡥࡸࠦ࡮ࡰࠢࡹ࡭ࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡩ࡯ࡶࡲࠤ࡮ࡴࡤࡪࡸ࡬ࡨࡺࡧ࡬ࠡࡵࡳࡩࡨࡹࠠࡢࡰࡧࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫࡯ࡳࡦࡨࡶࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࡰࠤࡲ࡫ࡡ࡯࡫ࡱ࡫࡫ࡻ࡬࡭ࡻ࠱ࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥࠢࡨࡲࡸࡻࡲࡦࡵࠣ࡫ࡷࡧ࡮ࡶ࡮ࡤࡶࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࡴࠢࡤࡶࡪࠦࡳࡦࡰࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ࢖")
        expanded = []
        for entry in bstack1lll1lll_opy_:
            if os.path.isdir(entry):
                feature_files = sorted(
                    glob.glob(os.path.join(entry, bstack1l1llll_opy_ (u"ࠨࠬ࠭ࠫࢗ"), bstack1l1llll_opy_ (u"ࠩ࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬ࢘")), recursive=True)
                )
                if feature_files:
                    expanded.extend(feature_files)
                else:
                    expanded.append(entry)
            elif any(c in entry for c in (bstack1l1llll_opy_ (u"ࠪ࠮࢙ࠬ"), bstack1l1llll_opy_ (u"ࠫࡄ࢚࠭"), bstack1l1llll_opy_ (u"ࠬࡡ࢛ࠧ"))):
                feature_files = sorted(glob.glob(entry, recursive=True))
                if feature_files:
                    expanded.extend(feature_files)
                else:
                    expanded.append(entry)
            else:
                expanded.append(entry)
        return expanded
    @measure(event_name=EVENTS.bstack1ll1ll1l_opy_, stage=STAGE.SINGLE)
    def bstack1lll1111_opy_(self):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡃࡳࡴࡱࡿࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥ࡬࡯ࡳࠢࡥࡩ࡭ࡧࡶࡦࠢ࡬ࡪࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨࠢࠣ࢜")
        bstack1llll1ll_opy_ = bstack1ll1l1ll_opy_.bstack1lll1l11_opy_(self.bstack1ll1llll_opy_, self.logger)
        if bstack1llll1ll_opy_ is None:
            self.logger.warn(bstack1l1llll_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡩࡣࡱࡨࡱ࡫ࡲࠡ࡫ࡶࠤࡳࡵࡴࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩ࠴ࠠࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥ࢝"))
            return
        bstack1lll1l1l_opy_ = False
        bstack1llll1ll_opy_.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠣࡧࡱࡥࡧࡲࡥࡥࠤ࢞"), bstack1llll1ll_opy_.bstack1ll1lll1_opy_())
        start_time = time.time()
        if bstack1llll1ll_opy_.bstack1ll1lll1_opy_():
            test_files = self._1lll111l_opy_(self.bstack1lll1lll_opy_)
            bstack1lll1l1l_opy_ = True
            bstack1lll1ll1_opy_ = bstack1llll1ll_opy_.bstack1llll111_opy_(test_files)
            if bstack1lll1ll1_opy_:
                self.bstack1lll1lll_opy_ = [item.replace(bstack1l1llll_opy_ (u"ࠩ࡟ࡠࠬ࢟"), bstack1l1llll_opy_ (u"ࠪ࠳ࠬࢠ")) for item in bstack1lll1ll1_opy_]
                bstack1llll1ll_opy_.bstack1llll1l1_opy_(bstack1lll1l1l_opy_)
                self.logger.info(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡵࡴ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤࢡ").format(self.bstack1lll1lll_opy_))
            else:
                self.logger.info(bstack1l1llll_opy_ (u"ࠧࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡽࡥࡳࡧࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡢࡺࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥࢢ"))
        bstack1llll1ll_opy_.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠨࡴࡪ࡯ࡨࡘࡦࡱࡥ࡯ࡖࡲࡅࡵࡶ࡬ࡺࠤࢣ"), int((time.time() - start_time) * 1000))
    def bstack1ll1ll11_opy_(self, bstack1lll1lll_opy_):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡖࡩࡹࠦࡴࡩࡧࠣࡪࡪࡧࡴࡶࡴࡨࠤ࡫࡯࡬ࡦࡵࠣࡸࡴࠦࡢࡦࠢࡨࡼࡪࡩࡵࡵࡧࡧࠦࠧࠨࢤ")
        self.bstack1lll1lll_opy_ = bstack1lll1lll_opy_
    def bstack1llll11l_opy_(self):
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤ࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡩ࡭ࡧࡶࠦࠧࠨࢥ")
        return self.bstack1lll1lll_opy_