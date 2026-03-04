# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1llllll1llll_opy_ import bstack1llllll1ll1l_opy_
from bstack_utils.bstack1lll1ll111_opy_ import bstack11l1llll1_opy_
from bstack_utils.helper import bstack11ll1ll1l_opy_
import json
class bstack111lll1ll_opy_:
    _1l1llll111l_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1llllll1l1ll_opy_ = bstack1llllll1ll1l_opy_(self.config, logger)
        self.bstack1lll1ll111_opy_ = bstack11l1llll1_opy_.get_instance(config=self.config)
        self.bstack1llllll1l1l1_opy_ = {}
        self.bstack1llll11l111_opy_ = False
        self.bstack1lllllll11l1_opy_ = (
            self.__1lllllll111l_opy_()
            and self.bstack1lll1ll111_opy_ is not None
            and self.bstack1lll1ll111_opy_.bstack1l1l1l1l11_opy_()
            and config.get(bstack1lll1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭↱"), None) is not None
            and config.get(bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ↲"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def get_instance(cls, config, logger):
        if cls._1l1llll111l_opy_ is None and config is not None:
            cls._1l1llll111l_opy_ = bstack111lll1ll_opy_(config, logger)
        return cls._1l1llll111l_opy_
    def bstack1l1l1l1l11_opy_(self):
        bstack1lll1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡱࠣࡲࡴࡺࠠࡢࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡷࡩࡧࡱ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓ࠶࠷ࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐࡴࡧࡩࡷ࡯࡮ࡨࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ↳")
        return self.bstack1lllllll11l1_opy_ and self.bstack1llllll1l111_opy_()
    def bstack1llllll1l111_opy_(self):
        bstack1lllllll1l1l_opy_ = os.getenv(bstack1lll1l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ↴"), self.config.get(bstack1lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ↵"), None))
        return bstack1lllllll1l1l_opy_ in bstack111l1llll1l_opy_
    def __1lllllll111l_opy_(self):
        bstack111lll11111_opy_ = False
        for fw in bstack111l1lll111_opy_:
            if fw in self.config.get(bstack1lll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ↶"), bstack1lll1l_opy_ (u"ࠧࠨ↷")):
                bstack111lll11111_opy_ = True
        return bstack11ll1ll1l_opy_(self.config.get(bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ↸"), bstack111lll11111_opy_))
    def bstack1lllllll1111_opy_(self):
        return (not self.bstack1l1l1l1l11_opy_() and
                self.bstack1lll1ll111_opy_ is not None and self.bstack1lll1ll111_opy_.bstack1l1l1l1l11_opy_())
    def bstack1llllll1ll11_opy_(self):
        if not self.bstack1lllllll1111_opy_():
            return
        if self.config.get(bstack1lll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ↹"), None) is None or self.config.get(bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭↺"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1lll1l_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢࡲࡶࠥࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠣ࡭ࡸࠦ࡮ࡶ࡮࡯࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡹࡥࡵࠢࡤࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡶࡢ࡮ࡸࡩ࠳ࠨ↻"))
        if not self.__1lllllll111l_opy_():
            self.logger.info(bstack1lll1l_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡥ࡯ࡣࡥࡰࡪࠦࡩࡵࠢࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠯ࠤ↼"))
    def bstack1lllllll11ll_opy_(self):
        return self.bstack1llll11l111_opy_
    def bstack1lll1llllll_opy_(self, bstack1llllll1lll1_opy_):
        self.bstack1llll11l111_opy_ = bstack1llllll1lll1_opy_
        self.bstack1llll111ll1_opy_(bstack1lll1l_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡪࡪࠢ↽"), bstack1llllll1lll1_opy_)
    def bstack1llll1l1111_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡩࡳࡷࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧ࠯ࠤ↾"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack1lll1ll111_opy_.bstack1llllll11ll1_opy_()
            if self.bstack1lll1ll111_opy_ is not None:
                orchestration_strategy = self.bstack1lll1ll111_opy_.bstack1ll1l1ll1_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1lll1l_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻࠣ࡭ࡸࠦࡎࡰࡰࡨ࠲ࠥࡉࡡ࡯ࡰࡲࡸࠥࡶࡲࡰࡥࡨࡩࡩࠦࡷࡪࡶ࡫ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠱ࠦ↿"))
                return None
            self.logger.info(bstack1lll1l_opy_ (u"ࠤࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻ࡮ࡺࡨࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻ࠽ࠤࢀࢃࠢ⇀").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1lll1l_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡆࡐࡎࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨ⇁"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1lll1l_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡷࡩࡱࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢ⇂"))
                self.bstack1llllll1l1ll_opy_.bstack1lllllll1l11_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1llllll1l1ll_opy_.bstack1llllll11lll_opy_()
            if not ordered_test_files:
                return None
            self.bstack1llll111ll1_opy_(bstack1lll1l_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴࡅࡲࡹࡳࡺࠢ⇃"), len(test_files))
            self.bstack1llll111ll1_opy_(bstack1lll1l_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤ⇄"), int(os.environ.get(bstack1lll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥ⇅")) or bstack1lll1l_opy_ (u"ࠣ࠲ࠥ⇆")))
            self.bstack1llll111ll1_opy_(bstack1lll1l_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨ⇇"), int(os.environ.get(bstack1lll1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ⇈")) or bstack1lll1l_opy_ (u"ࠦ࠶ࠨ⇉")))
            self.bstack1llll111ll1_opy_(bstack1lll1l_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡇࡴࡻ࡮ࡵࠤ⇊"), len(ordered_test_files))
            self.bstack1llll111ll1_opy_(bstack1lll1l_opy_ (u"ࠨࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡄࡔࡎࡉࡡ࡭࡮ࡆࡳࡺࡴࡴࠣ⇋"), self.bstack1llllll1l1ll_opy_.bstack1llllll1l11l_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡰࡦࡹࡳࡦࡵ࠽ࠤࢀࢃࠢ⇌").format(e))
        return None
    def bstack1llll111ll1_opy_(self, key, value):
        self.bstack1llllll1l1l1_opy_[key] = value
    def bstack11l1ll11_opy_(self):
        return self.bstack1llllll1l1l1_opy_