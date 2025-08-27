# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l11ll1l1_opy_ import bstack111l1l11l11_opy_
from bstack_utils.bstack111l111ll_opy_ import bstack1l11llll1_opy_
from bstack_utils.helper import bstack11lll1111_opy_
class bstack11l111ll1l_opy_:
    _1ll1ll11l11_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l11l1ll1_opy_ = bstack111l1l11l11_opy_(self.config, logger)
        self.bstack111l111ll_opy_ = bstack1l11llll1_opy_.bstack1ll1lll1l1_opy_(config=self.config)
        self.bstack111l1l111ll_opy_ = {}
        self.bstack11111l1lll_opy_ = False
        self.bstack111l1l11111_opy_ = (
            self.__111l11ll111_opy_()
            and self.bstack111l111ll_opy_ is not None
            and self.bstack111l111ll_opy_.bstack1lll1111_opy_()
            and config.get(bstack1111lll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪḮ"), None) is not None
            and config.get(bstack1111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩḯ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1ll1lll1l1_opy_(cls, config, logger):
        if cls._1ll1ll11l11_opy_ is None and config is not None:
            cls._1ll1ll11l11_opy_ = bstack11l111ll1l_opy_(config, logger)
        return cls._1ll1ll11l11_opy_
    def bstack1lll1111_opy_(self):
        bstack1111lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡉࡵࠠ࡯ࡱࡷࠤࡦࡶࡰ࡭ࡻࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡻ࡭࡫࡮࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐ࠳࠴ࡽࠥ࡯ࡳࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡔࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡩࡴࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠣ࡭ࡸࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥḰ")
        return self.bstack111l1l11111_opy_ and self.bstack111l11lll11_opy_()
    def bstack111l11lll11_opy_(self):
        return self.config.get(bstack1111lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫḱ"), None) in bstack11l1ll1l1l1_opy_
    def __111l11ll111_opy_(self):
        bstack11ll1111l1l_opy_ = False
        for fw in bstack11l1lll111l_opy_:
            if fw in self.config.get(bstack1111lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬḲ"), bstack1111lll_opy_ (u"ࠪࠫḳ")):
                bstack11ll1111l1l_opy_ = True
        return bstack11lll1111_opy_(self.config.get(bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḴ"), bstack11ll1111l1l_opy_))
    def bstack111l1l1111l_opy_(self):
        return (not self.bstack1lll1111_opy_() and
                self.bstack111l111ll_opy_ is not None and self.bstack111l111ll_opy_.bstack1lll1111_opy_())
    def bstack111l11l1l1l_opy_(self):
        if not self.bstack111l1l1111l_opy_():
            return
        if self.config.get(bstack1111lll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪḵ"), None) is None or self.config.get(bstack1111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩḶ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1111lll_opy_ (u"ࠢࡕࡧࡶࡸࠥࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡦࡥࡳ࠭ࡴࠡࡹࡲࡶࡰࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥࡵࡲࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡱࡹࡱࡲ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡵࡨࡸࠥࡧࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥ࠯ࠤḷ"))
        if not self.__111l11ll111_opy_():
            self.logger.info(bstack1111lll_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡤࡪࡵࡤࡦࡱ࡫ࡤ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡨࡲࡦࡨ࡬ࡦࠢ࡬ࡸࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲ࠧḸ"))
    def bstack111l11lll1l_opy_(self):
        return self.bstack11111l1lll_opy_
    def bstack1111l1111l_opy_(self, bstack111l11l1lll_opy_):
        self.bstack11111l1lll_opy_ = bstack111l11l1lll_opy_
        self.bstack11111lll11_opy_(bstack1111lll_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠥḹ"), bstack111l11l1lll_opy_)
    def bstack11111l1l1l_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1111lll_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡲࡶࡩ࡫ࡲࡪࡰࡪ࠲ࠧḺ"))
                return None
            orchestration_strategy = None
            bstack111l11llll1_opy_ = self.bstack111l111ll_opy_.bstack111l1l111l1_opy_()
            if self.bstack111l111ll_opy_ is not None:
                orchestration_strategy = self.bstack111l111ll_opy_.bstack111ll1l1l_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1111lll_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦࡩࡴࠢࡑࡳࡳ࡫࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡵࡳࡨ࡫ࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠴ࠢḻ"))
                return None
            self.logger.info(bstack1111lll_opy_ (u"ࠧࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥḼ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1111lll_opy_ (u"ࠨࡕࡴ࡫ࡱ࡫ࠥࡉࡌࡊࠢࡩࡰࡴࡽࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤḽ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack1111lll_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡳࡥ࡭ࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥḾ"))
                self.bstack111l11l1ll1_opy_.bstack111l11ll1ll_opy_(test_files, orchestration_strategy, bstack111l11llll1_opy_)
                ordered_test_files = self.bstack111l11l1ll1_opy_.bstack111l11ll11l_opy_()
            if not ordered_test_files:
                return None
            self.bstack11111lll11_opy_(bstack1111lll_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥḿ"), len(test_files))
            self.bstack11111lll11_opy_(bstack1111lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧṀ"), int(os.environ.get(bstack1111lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨṁ")) or bstack1111lll_opy_ (u"ࠦ࠵ࠨṂ")))
            self.bstack11111lll11_opy_(bstack1111lll_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤṃ"), int(os.environ.get(bstack1111lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤṄ")) or bstack1111lll_opy_ (u"ࠢ࠲ࠤṅ")))
            self.bstack11111lll11_opy_(bstack1111lll_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧṆ"), len(ordered_test_files))
            self.bstack11111lll11_opy_(bstack1111lll_opy_ (u"ࠤࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡇࡐࡊࡅࡤࡰࡱࡉ࡯ࡶࡰࡷࠦṇ"), self.bstack111l11l1ll1_opy_.bstack111l11lllll_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1111lll_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩ࡬ࡢࡵࡶࡩࡸࡀࠠࡼࡿࠥṈ").format(e))
        return None
    def bstack11111lll11_opy_(self, key, value):
        self.bstack111l1l111ll_opy_[key] = value
    def bstack1ll1llllll_opy_(self):
        return self.bstack111l1l111ll_opy_