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
import glob
import time
from bstack_utils.bstack111l1l11l_opy_ import bstack11l1l11lll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
class bstack1111l1ll1l_opy_:
    def __init__(self, args, logger, bstack1lllll11111_opy_, bstack1lllll111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
        self.bstack1lllll111ll_opy_ = bstack1lllll111ll_opy_
        self.bstack1111lll11_opy_ = []
    def _1lllll11l11_opy_(self, bstack1111lll11_opy_):
        bstack111l_opy_ (u"ࠨࠢࠣࡇࡻࡴࡦࡴࡤࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡴࡤࠡࡩ࡯ࡳࡧ࠳ࡰࡢࡶࡷࡩࡷࡴࠠࡦࡰࡷࡶ࡮࡫ࡳࠡ࡫ࡱࠤࡸࡶࡥࡤࡡࡩ࡭ࡱ࡫ࡳࠡࡶࡲࠤ࡮ࡴࡤࡪࡸ࡬ࡨࡺࡧ࡬ࠡ࠰ࡩࡩࡦࡺࡵࡳࡧࠣࡪ࡮ࡲࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡍࡧ࡮ࡥ࡮ࡨࡷࠥࡺࡨࡳࡧࡨࠤࡨࡧࡳࡦࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠷࠮ࠡࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࠭࡫࠮ࡨ࠰ࠣࠫ࡫࡫ࡡࡵࡷࡵࡩࡸ࠭ࠩࠡ⠖ࠣࡻࡦࡲ࡫ࡴࠢࡵࡩࡨࡻࡲࡴ࡫ࡹࡩࡱࡿࠠࡧࡱࡵࠤ࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠠࡧ࡫࡯ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠴࠱ࠤࡌࡲ࡯ࡣࠢࡳࡥࡹࡺࡥࡳࡰࠣࠬࡪ࠴ࡧ࠯ࠢࠪࡪࡪࡧࡴࡶࡴࡨࡷ࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨࠫࠣ⠘ࠥ࡫ࡸࡱࡣࡱࡨࡸࠦࡶࡪࡣࠣ࡫ࡱࡵࡢ࠯ࡩ࡯ࡳࡧ࠮ࠩ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠷࠳ࠦࡐ࡭ࡣ࡬ࡲࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡ⠖ࠣ࡯ࡪࡶࡴࠡࡣࡶ࠱࡮ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡥࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡱࡵࠤࡺࡴࡥࡹࡲࡤࡲࡩ࡫ࡤࠡࡩ࡯ࡳࡧࠦࡴࡰࠢࡷ࡬ࡪࠦࡔࡐࠢࡶࡴࡱ࡯ࡴ࠮ࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡲ࡫ࡡ࡯ࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡥࠡࡵࡨࡶࡻ࡫ࡲࠡࡪࡤࡷࠥࡴ࡯ࠡࡸ࡬ࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥ࡯࡮ࡵࡱࠣ࡭ࡳࡪࡩࡷ࡫ࡧࡹࡦࡲࠠࡴࡲࡨࡧࡸࠦࡡ࡯ࡦࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡵࡲࡥࡧࡵࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦ࡯ࠣࡱࡪࡧ࡮ࡪࡰࡪࡪࡺࡲ࡬ࡺ࠰ࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡧࡱࡷࡺࡸࡥࡴࠢࡪࡶࡦࡴࡵ࡭ࡣࡵࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳࠡࡣࡵࡩࠥࡹࡥ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣႊ")
        expanded = []
        for entry in bstack1111lll11_opy_:
            if os.path.isdir(entry):
                bstack1l1l11111l_opy_ = sorted(
                    glob.glob(os.path.join(entry, bstack111l_opy_ (u"ࠧࠫࠬࠪႋ"), bstack111l_opy_ (u"ࠨࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫႌ")), recursive=True)
                )
                if bstack1l1l11111l_opy_:
                    expanded.extend(bstack1l1l11111l_opy_)
                else:
                    expanded.append(entry)
            elif any(c in entry for c in (bstack111l_opy_ (u"ႍࠩ࠭ࠫ"), bstack111l_opy_ (u"ࠪࡃࠬႎ"), bstack111l_opy_ (u"ࠫࡠ࠭ႏ"))):
                bstack1l1l11111l_opy_ = sorted(glob.glob(entry, recursive=True))
                if bstack1l1l11111l_opy_:
                    expanded.extend(bstack1l1l11111l_opy_)
                else:
                    expanded.append(entry)
            else:
                expanded.append(entry)
        return expanded
    @measure(event_name=EVENTS.bstack1llll1lll1l_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack1lll11l1l_opy_(self):
        bstack111l_opy_ (u"ࠧࠨࠢࡂࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡤࡨ࡬ࡦࡼࡥࠡ࡫ࡩࠤࡪࡴࡡࡣ࡮ࡨࡨࠧࠨࠢ႐")
        bstack111l1l11l_opy_ = bstack11l1l11lll_opy_.bstack1lll111ll_opy_(self.bstack1lllll11111_opy_, self.logger)
        if bstack111l1l11l_opy_ is None:
            self.logger.warn(bstack111l_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡨࡢࡰࡧࡰࡪࡸࠠࡪࡵࠣࡲࡴࡺࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࡨ࠳ࠦࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤ႑"))
            return
        bstack1lllll11l1l_opy_ = False
        bstack111l1l11l_opy_.bstack1llll1lllll_opy_(bstack111l_opy_ (u"ࠢࡦࡰࡤࡦࡱ࡫ࡤࠣ႒"), bstack111l1l11l_opy_.bstack1l1l1ll1l_opy_())
        start_time = time.time()
        if bstack111l1l11l_opy_.bstack1l1l1ll1l_opy_():
            test_files = self._1lllll11l11_opy_(self.bstack1111lll11_opy_)
            bstack1lllll11l1l_opy_ = True
            bstack1lllll1111l_opy_ = bstack111l1l11l_opy_.bstack1llll1llll1_opy_(test_files)
            if bstack1lllll1111l_opy_:
                self.bstack1111lll11_opy_ = [item.replace(bstack111l_opy_ (u"ࠨ࡞࡟ࠫ႓"), bstack111l_opy_ (u"ࠩ࠲ࠫ႔")) for item in bstack1lllll1111l_opy_]
                bstack111l1l11l_opy_.bstack1lllll111l1_opy_(bstack1lllll11l1l_opy_)
                self.logger.info(bstack111l_opy_ (u"ࠥࡘࡪࡹࡴࡴࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡻࡳࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ႕").format(self.bstack1111lll11_opy_))
            else:
                self.logger.info(bstack111l_opy_ (u"ࠦࡓࡵࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡫ࡲࡦࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡨࡹࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤ႖"))
        bstack111l1l11l_opy_.bstack1llll1lllll_opy_(bstack111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡗࡥࡰ࡫࡮ࡕࡱࡄࡴࡵࡲࡹࠣ႗"), int((time.time() - start_time) * 1000))
    def bstack11111lll1l_opy_(self, bstack1111lll11_opy_):
        bstack111l_opy_ (u"ࠨࠢࠣࡕࡨࡸࠥࡺࡨࡦࠢࡩࡩࡦࡺࡵࡳࡧࠣࡪ࡮ࡲࡥࡴࠢࡷࡳࠥࡨࡥࠡࡧࡻࡩࡨࡻࡴࡦࡦࠥࠦࠧ႘")
        self.bstack1111lll11_opy_ = bstack1111lll11_opy_
    def bstack1l1lll11_opy_(self):
        bstack111l_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡪࡪࡧࡴࡶࡴࡨࠤ࡫࡯࡬ࡦࡵࠥࠦࠧ႙")
        return self.bstack1111lll11_opy_