# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
import glob
import time
from bstack_utils.bstack111ll111_opy_ import bstack111ll1111l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
class bstack1ll111111l_opy_:
    def __init__(self, args, logger, bstack1lllll11111_opy_, bstack1lllll111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
        self.bstack1lllll111ll_opy_ = bstack1lllll111ll_opy_
        self.bstack111l11l111_opy_ = []
    def _1lllll11l1l_opy_(self, bstack111l11l111_opy_):
        bstack11ll11_opy_ (u"ࠨࠢࠣࡇࡻࡴࡦࡴࡤࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡴࡤࠡࡩ࡯ࡳࡧ࠳ࡰࡢࡶࡷࡩࡷࡴࠠࡦࡰࡷࡶ࡮࡫ࡳࠡ࡫ࡱࠤࡸࡶࡥࡤࡡࡩ࡭ࡱ࡫ࡳࠡࡶࡲࠤ࡮ࡴࡤࡪࡸ࡬ࡨࡺࡧ࡬ࠡ࠰ࡩࡩࡦࡺࡵࡳࡧࠣࡪ࡮ࡲࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡍࡧ࡮ࡥ࡮ࡨࡷࠥࡺࡨࡳࡧࡨࠤࡨࡧࡳࡦࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠷࠮ࠡࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࠭࡫࠮ࡨ࠰ࠣࠫ࡫࡫ࡡࡵࡷࡵࡩࡸ࠭ࠩࠡ⠖ࠣࡻࡦࡲ࡫ࡴࠢࡵࡩࡨࡻࡲࡴ࡫ࡹࡩࡱࡿࠠࡧࡱࡵࠤ࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠠࡧ࡫࡯ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠴࠱ࠤࡌࡲ࡯ࡣࠢࡳࡥࡹࡺࡥࡳࡰࠣࠬࡪ࠴ࡧ࠯ࠢࠪࡪࡪࡧࡴࡶࡴࡨࡷ࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨࠫࠣ⠘ࠥ࡫ࡸࡱࡣࡱࡨࡸࠦࡶࡪࡣࠣ࡫ࡱࡵࡢ࠯ࡩ࡯ࡳࡧ࠮ࠩ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠷࠳ࠦࡐ࡭ࡣ࡬ࡲࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡ⠖ࠣ࡯ࡪࡶࡴࠡࡣࡶ࠱࡮ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡥࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡱࡵࠤࡺࡴࡥࡹࡲࡤࡲࡩ࡫ࡤࠡࡩ࡯ࡳࡧࠦࡴࡰࠢࡷ࡬ࡪࠦࡔࡐࠢࡶࡴࡱ࡯ࡴ࠮ࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡲ࡫ࡡ࡯ࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡥࠡࡵࡨࡶࡻ࡫ࡲࠡࡪࡤࡷࠥࡴ࡯ࠡࡸ࡬ࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥ࡯࡮ࡵࡱࠣ࡭ࡳࡪࡩࡷ࡫ࡧࡹࡦࡲࠠࡴࡲࡨࡧࡸࠦࡡ࡯ࡦࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡵࡲࡥࡧࡵࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦ࡯ࠣࡱࡪࡧ࡮ࡪࡰࡪࡪࡺࡲ࡬ࡺ࠰ࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡧࡱࡷࡺࡸࡥࡴࠢࡪࡶࡦࡴࡵ࡭ࡣࡵࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳࠡࡣࡵࡩࠥࡹࡥ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣႊ")
        expanded = []
        for entry in bstack111l11l111_opy_:
            if os.path.isdir(entry):
                bstack1ll111ll1_opy_ = sorted(
                    glob.glob(os.path.join(entry, bstack11ll11_opy_ (u"ࠧࠫࠬࠪႋ"), bstack11ll11_opy_ (u"ࠨࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫႌ")), recursive=True)
                )
                if bstack1ll111ll1_opy_:
                    expanded.extend(bstack1ll111ll1_opy_)
                else:
                    expanded.append(entry)
            elif any(c in entry for c in (bstack11ll11_opy_ (u"ႍࠩ࠭ࠫ"), bstack11ll11_opy_ (u"ࠪࡃࠬႎ"), bstack11ll11_opy_ (u"ࠫࡠ࠭ႏ"))):
                bstack1ll111ll1_opy_ = sorted(glob.glob(entry, recursive=True))
                if bstack1ll111ll1_opy_:
                    expanded.extend(bstack1ll111ll1_opy_)
                else:
                    expanded.append(entry)
            else:
                expanded.append(entry)
        return expanded
    @measure(event_name=EVENTS.bstack1lllll11l11_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack1llllllll1l_opy_(self):
        bstack11ll11_opy_ (u"ࠧࠨࠢࡂࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡤࡨ࡬ࡦࡼࡥࠡ࡫ࡩࠤࡪࡴࡡࡣ࡮ࡨࡨࠧࠨࠢ႐")
        bstack111ll111_opy_ = bstack111ll1111l_opy_.bstack111llll11_opy_(self.bstack1lllll11111_opy_, self.logger)
        if bstack111ll111_opy_ is None:
            self.logger.warn(bstack11ll11_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡨࡢࡰࡧࡰࡪࡸࠠࡪࡵࠣࡲࡴࡺࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࡨ࠳ࠦࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤ႑"))
            return
        bstack1llll1llll1_opy_ = False
        bstack111ll111_opy_.bstack1llll1lll1l_opy_(bstack11ll11_opy_ (u"ࠢࡦࡰࡤࡦࡱ࡫ࡤࠣ႒"), bstack111ll111_opy_.bstack1ll11lll_opy_())
        start_time = time.time()
        if bstack111ll111_opy_.bstack1ll11lll_opy_():
            test_files = self._1lllll11l1l_opy_(self.bstack111l11l111_opy_)
            bstack1llll1llll1_opy_ = True
            bstack1lllll111l1_opy_ = bstack111ll111_opy_.bstack1llll1lllll_opy_(test_files)
            if bstack1lllll111l1_opy_:
                self.bstack111l11l111_opy_ = [item.replace(bstack11ll11_opy_ (u"ࠨ࡞࡟ࠫ႓"), bstack11ll11_opy_ (u"ࠩ࠲ࠫ႔")) for item in bstack1lllll111l1_opy_]
                bstack111ll111_opy_.bstack1lllll1111l_opy_(bstack1llll1llll1_opy_)
                self.logger.info(bstack11ll11_opy_ (u"ࠥࡘࡪࡹࡴࡴࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡻࡳࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ႕").format(self.bstack111l11l111_opy_))
            else:
                self.logger.info(bstack11ll11_opy_ (u"ࠦࡓࡵࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡫ࡲࡦࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡨࡹࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤ႖"))
        bstack111ll111_opy_.bstack1llll1lll1l_opy_(bstack11ll11_opy_ (u"ࠧࡺࡩ࡮ࡧࡗࡥࡰ࡫࡮ࡕࡱࡄࡴࡵࡲࡹࠣ႗"), int((time.time() - start_time) * 1000))
    def bstack11l1ll1l_opy_(self, bstack111l11l111_opy_):
        bstack11ll11_opy_ (u"ࠨࠢࠣࡕࡨࡸࠥࡺࡨࡦࠢࡩࡩࡦࡺࡵࡳࡧࠣࡪ࡮ࡲࡥࡴࠢࡷࡳࠥࡨࡥࠡࡧࡻࡩࡨࡻࡴࡦࡦࠥࠦࠧ႘")
        self.bstack111l11l111_opy_ = bstack111l11l111_opy_
    def bstack1ll1lll11_opy_(self):
        bstack11ll11_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡪࡪࡧࡴࡶࡴࡨࠤ࡫࡯࡬ࡦࡵࠥࠦࠧ႙")
        return self.bstack111l11l111_opy_