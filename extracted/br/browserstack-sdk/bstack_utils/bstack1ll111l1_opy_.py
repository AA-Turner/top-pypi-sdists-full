# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l1l111l1_opy_ import bstack111l11lll11_opy_
from bstack_utils.bstack11l1l111l1_opy_ import bstack1l1l1llll1_opy_
from bstack_utils.helper import bstack11lll1ll11_opy_
class bstack1l11111l11_opy_:
    _1llll11ll11_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l1l1111l_opy_ = bstack111l11lll11_opy_(self.config, logger)
        self.bstack11l1l111l1_opy_ = bstack1l1l1llll1_opy_.bstack11l1lllll1_opy_(config=self.config)
        self.bstack111l1l11l1l_opy_ = {}
        self.bstack1111ll111l_opy_ = False
        self.bstack111l11ll1l1_opy_ = (
            self.__111l11llll1_opy_()
            and self.bstack11l1l111l1_opy_ is not None
            and self.bstack11l1l111l1_opy_.bstack111111lll_opy_()
            and config.get(bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ṇ"), None) is not None
            and config.get(bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬṇ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack11l1lllll1_opy_(cls, config, logger):
        if cls._1llll11ll11_opy_ is None and config is not None:
            cls._1llll11ll11_opy_ = bstack1l11111l11_opy_(config, logger)
        return cls._1llll11ll11_opy_
    def bstack111111lll_opy_(self):
        bstack1l1l1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡱࠣࡲࡴࡺࠠࡢࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡷࡩࡧࡱ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓ࠶࠷ࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐࡴࡧࡩࡷ࡯࡮ࡨࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨṈ")
        return self.bstack111l11ll1l1_opy_ and self.bstack111l1l11lll_opy_()
    def bstack111l1l11lll_opy_(self):
        return self.config.get(bstack1l1l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧṉ"), None) in bstack11l1ll1l1l1_opy_
    def __111l11llll1_opy_(self):
        bstack11ll1111ll1_opy_ = False
        for fw in bstack11l1lll1l1l_opy_:
            if fw in self.config.get(bstack1l1l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨṊ"), bstack1l1l1ll_opy_ (u"࠭ࠧṋ")):
                bstack11ll1111ll1_opy_ = True
        return bstack11lll1ll11_opy_(self.config.get(bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫṌ"), bstack11ll1111ll1_opy_))
    def bstack111l11ll11l_opy_(self):
        return (not self.bstack111111lll_opy_() and
                self.bstack11l1l111l1_opy_ is not None and self.bstack11l1l111l1_opy_.bstack111111lll_opy_())
    def bstack111l11lll1l_opy_(self):
        if not self.bstack111l11ll11l_opy_():
            return
        if self.config.get(bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ṍ"), None) is None or self.config.get(bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬṎ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l1l1ll_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡࡱࡵࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡴࡵ࡭࡮࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡸ࡫ࡴࠡࡣࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨ࠲ࠧṏ"))
        if not self.__111l11llll1_opy_():
            self.logger.info(bstack1l1l1ll_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡫࡮ࡢࡤ࡯ࡩࠥ࡯ࡴࠡࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫࠮ࠣṐ"))
    def bstack111l11ll1ll_opy_(self):
        return self.bstack1111ll111l_opy_
    def bstack1111l11l1l_opy_(self, bstack111l11ll111_opy_):
        self.bstack1111ll111l_opy_ = bstack111l11ll111_opy_
        self.bstack11111l1l11_opy_(bstack1l1l1ll_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠨṑ"), bstack111l11ll111_opy_)
    def bstack1111ll1111_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭࠮ࠣṒ"))
                return None
            orchestration_strategy = None
            bstack111l1l11ll1_opy_ = self.bstack11l1l111l1_opy_.bstack111l1l111ll_opy_()
            if self.bstack11l1l111l1_opy_ is not None:
                orchestration_strategy = self.bstack11l1l111l1_opy_.bstack11llll1l_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l1l1ll_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢ࡬ࡷࠥࡔ࡯࡯ࡧ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵࡸ࡯ࡤࡧࡨࡨࠥࡽࡩࡵࡪࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠰ࠥṓ"))
                return None
            self.logger.info(bstack1l1l1ll_opy_ (u"ࠣࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡿࢂࠨṔ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡅࡏࡍࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧṕ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack1l1l1ll_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡶࡨࡰࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨṖ"))
                self.bstack111l1l1111l_opy_.bstack111l11lllll_opy_(test_files, orchestration_strategy, bstack111l1l11ll1_opy_)
                ordered_test_files = self.bstack111l1l1111l_opy_.bstack111l1l11l11_opy_()
            if not ordered_test_files:
                return None
            self.bstack11111l1l11_opy_(bstack1l1l1ll_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨṗ"), len(test_files))
            self.bstack11111l1l11_opy_(bstack1l1l1ll_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣṘ"), int(os.environ.get(bstack1l1l1ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤṙ")) or bstack1l1l1ll_opy_ (u"ࠢ࠱ࠤṚ")))
            self.bstack11111l1l11_opy_(bstack1l1l1ll_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧṛ"), int(os.environ.get(bstack1l1l1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧṜ")) or bstack1l1l1ll_opy_ (u"ࠥ࠵ࠧṝ")))
            self.bstack11111l1l11_opy_(bstack1l1l1ll_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣṞ"), len(ordered_test_files))
            self.bstack11111l1l11_opy_(bstack1l1l1ll_opy_ (u"ࠧࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴࡃࡓࡍࡈࡧ࡬࡭ࡅࡲࡹࡳࡺࠢṟ"), self.bstack111l1l1111l_opy_.bstack111l1l11111_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥ࡯ࡥࡸࡹࡥࡴ࠼ࠣࡿࢂࠨṠ").format(e))
        return None
    def bstack11111l1l11_opy_(self, key, value):
        self.bstack111l1l11l1l_opy_[key] = value
    def bstack1l11l11lll_opy_(self):
        return self.bstack111l1l11l1l_opy_