# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l11lllll_opy_ import bstack111l11l1l1l_opy_
from bstack_utils.bstack11llllll_opy_ import bstack111l1llll_opy_
from bstack_utils.helper import bstack1lll1l11l_opy_
class bstack11l11l111l_opy_:
    _1lll11l11l1_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l11l11l1_opy_ = bstack111l11l1l1l_opy_(self.config, logger)
        self.bstack11llllll_opy_ = bstack111l1llll_opy_.bstack1l11llll1_opy_(config=self.config)
        self.bstack111l11l1111_opy_ = {}
        self.bstack11111ll11l_opy_ = False
        self.bstack111l11ll11l_opy_ = (
            self.__111l11l11ll_opy_()
            and self.bstack11llllll_opy_ is not None
            and self.bstack11llllll_opy_.bstack1ll11llll1_opy_()
            and config.get(bstack1111l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨḳ"), None) is not None
            and config.get(bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧḴ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1l11llll1_opy_(cls, config, logger):
        if cls._1lll11l11l1_opy_ is None and config is not None:
            cls._1lll11l11l1_opy_ = bstack11l11l111l_opy_(config, logger)
        return cls._1lll11l11l1_opy_
    def bstack1ll11llll1_opy_(self):
        bstack1111l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡇࡳࠥࡴ࡯ࡵࠢࡤࡴࡵࡲࡹࠡࡶࡨࡷࡹࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡹ࡫ࡩࡳࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡕ࠱࠲ࡻࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡒࡶࡩ࡫ࡲࡪࡰࡪࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠣ࡭ࡸࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣḵ")
        return self.bstack111l11ll11l_opy_ and self.bstack111l11l1l11_opy_()
    def bstack111l11l1l11_opy_(self):
        return self.config.get(bstack1111l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩḶ"), None) in bstack11l1l1llll1_opy_
    def __111l11l11ll_opy_(self):
        bstack11ll1111111_opy_ = False
        for fw in bstack11l1l1ll111_opy_:
            if fw in self.config.get(bstack1111l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪḷ"), bstack1111l1l_opy_ (u"ࠨࠩḸ")):
                bstack11ll1111111_opy_ = True
        return bstack1lll1l11l_opy_(self.config.get(bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ḹ"), bstack11ll1111111_opy_))
    def bstack111l11ll111_opy_(self):
        return (not self.bstack1ll11llll1_opy_() and
                self.bstack11llllll_opy_ is not None and self.bstack11llllll_opy_.bstack1ll11llll1_opy_())
    def bstack111l11lll11_opy_(self):
        if not self.bstack111l11ll111_opy_():
            return
        if self.config.get(bstack1111l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨḺ"), None) is None or self.config.get(bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧḻ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1111l1l_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠣࡳࡷࠦࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠤ࡮ࡹࠠ࡯ࡷ࡯ࡰ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡳࡦࡶࠣࡥࠥࡴ࡯࡯࠯ࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠴ࠢḼ"))
        if not self.__111l11l11ll_opy_():
            self.logger.info(bstack1111l1l_opy_ (u"ࠨࡔࡦࡵࡷࠤࡗ࡫࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡥࡤࡲࠬࡺࠠࡸࡱࡵ࡯ࠥࡧࡳࠡࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡦࡰࡤࡦࡱ࡫ࠠࡪࡶࠣࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠰ࠥḽ"))
    def bstack111l11ll1ll_opy_(self):
        return self.bstack11111ll11l_opy_
    def bstack11111l1ll1_opy_(self, bstack111l11lll1l_opy_):
        self.bstack11111ll11l_opy_ = bstack111l11lll1l_opy_
        self.bstack11111lll11_opy_(bstack1111l1l_opy_ (u"ࠢࡢࡲࡳࡰ࡮࡫ࡤࠣḾ"), bstack111l11lll1l_opy_)
    def bstack111111lll1_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡰࡴࡧࡩࡷ࡯࡮ࡨ࠰ࠥḿ"))
                return None
            orchestration_strategy = None
            bstack111l11l1ll1_opy_ = self.bstack11llllll_opy_.bstack111l11l111l_opy_()
            if self.bstack11llllll_opy_ is not None:
                orchestration_strategy = self.bstack11llllll_opy_.bstack1lll111111_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1111l1l_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼࠤ࡮ࡹࠠࡏࡱࡱࡩ࠳ࠦࡃࡢࡰࡱࡳࡹࠦࡰࡳࡱࡦࡩࡪࡪࠠࡸ࡫ࡷ࡬ࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠲ࠧṀ"))
                return None
            self.logger.info(bstack1111l1l_opy_ (u"ࠥࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡯ࡴࡩࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣṁ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1111l1l_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡇࡑࡏࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢṂ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack1111l1l_opy_ (u"࡛ࠧࡳࡪࡰࡪࠤࡸࡪ࡫ࠡࡨ࡯ࡳࡼࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣṃ"))
                self.bstack111l11l11l1_opy_.bstack111l11llll1_opy_(test_files, orchestration_strategy, bstack111l11l1ll1_opy_)
                ordered_test_files = self.bstack111l11l11l1_opy_.bstack111l11l1lll_opy_()
            if not ordered_test_files:
                return None
            self.bstack11111lll11_opy_(bstack1111l1l_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣṄ"), len(test_files))
            self.bstack11111lll11_opy_(bstack1111l1l_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥṅ"), int(os.environ.get(bstack1111l1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦṆ")) or bstack1111l1l_opy_ (u"ࠤ࠳ࠦṇ")))
            self.bstack11111lll11_opy_(bstack1111l1l_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢṈ"), int(os.environ.get(bstack1111l1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢṉ")) or bstack1111l1l_opy_ (u"ࠧ࠷ࠢṊ")))
            self.bstack11111lll11_opy_(bstack1111l1l_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥṋ"), len(ordered_test_files))
            self.bstack11111lll11_opy_(bstack1111l1l_opy_ (u"ࠢࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡅࡕࡏࡃࡢ࡮࡯ࡇࡴࡻ࡮ࡵࠤṌ"), self.bstack111l11l11l1_opy_.bstack111l11ll1l1_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡱࡧࡳࡴࡧࡶ࠾ࠥࢁࡽࠣṍ").format(e))
        return None
    def bstack11111lll11_opy_(self, key, value):
        self.bstack111l11l1111_opy_[key] = value
    def bstack11ll11ll_opy_(self):
        return self.bstack111l11l1111_opy_