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
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1ll1llll1111_opy_ import bstack1ll1lll1l1l1_opy_
from bstack_utils.bstack11ll1lll1_opy_ import bstack11ll1111l_opy_
from bstack_utils.helper import bstack11lll11l1l_opy_
import json
class bstack1ll1l1ll_opy_:
    _instance = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1ll1lll1ll11_opy_ = bstack1ll1lll1l1l1_opy_(self.config, logger)
        self.bstack11ll1lll1_opy_ = bstack11ll1111l_opy_.bstack1lll1l11_opy_(config=self.config)
        self.bstack1ll1lll11ll1_opy_ = {}
        self.bstack1lll1l1l_opy_ = False
        self.bstack1ll1lll11l1l_opy_ = (
            self.__1ll1lll1lll1_opy_()
            and self.bstack11ll1lll1_opy_ is not None
            and self.bstack11ll1lll1_opy_.bstack1ll1lll1_opy_()
            and config.get(bstack1l1llll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭⡲"), None) is not None
            and config.get(bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ⡳"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1lll1l11_opy_(cls, config, logger):
        if cls._instance is None and config is not None:
            cls._instance = bstack1ll1l1ll_opy_(config, logger)
        return cls._instance
    def bstack1ll1lll1_opy_(self):
        bstack1l1llll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡱࠣࡲࡴࡺࠠࡢࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡷࡩࡧࡱ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓ࠶࠷ࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐࡴࡧࡩࡷ࡯࡮ࡨࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⡴")
        return self.bstack1ll1lll11l1l_opy_ and self.bstack1ll1lll111ll_opy_()
    def bstack1ll1lll111ll_opy_(self):
        bstack1ll1llll111l_opy_ = os.getenv(bstack1l1llll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ⡵"), self.config.get(bstack1l1llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⡶"), None))
        return bstack1ll1llll111l_opy_ in bstack1lllllllll1l_opy_
    def __1ll1lll1lll1_opy_(self):
        bstack111111l11l1_opy_ = False
        for fw in bstack1111111l1l1_opy_:
            if fw in self.config.get(bstack1l1llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⡷"), bstack1l1llll_opy_ (u"ࠧࠨ⡸")):
                bstack111111l11l1_opy_ = True
        return bstack11lll11l1l_opy_(self.config.get(bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⡹"), bstack111111l11l1_opy_))
    def bstack1ll1lll1l1ll_opy_(self):
        return (not self.bstack1ll1lll1_opy_() and
                self.bstack11ll1lll1_opy_ is not None and self.bstack11ll1lll1_opy_.bstack1ll1lll1_opy_())
    def bstack1ll1lll1llll_opy_(self):
        if not self.bstack1ll1lll1l1ll_opy_():
            return
        if self.config.get(bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⡺"), None) is None or self.config.get(bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⡻"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢࡲࡶࠥࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠣ࡭ࡸࠦ࡮ࡶ࡮࡯࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡹࡥࡵࠢࡤࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡶࡢ࡮ࡸࡩ࠳ࠨ⡼"))
        if not self.__1ll1lll1lll1_opy_():
            self.logger.info(bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡥ࡯ࡣࡥࡰࡪࠦࡩࡵࠢࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠯ࠤ⡽"))
    def bstack1ll1lll1ll1l_opy_(self):
        return self.bstack1lll1l1l_opy_
    def bstack1llll1l1_opy_(self, bstack1ll1llll11l1_opy_):
        self.bstack1lll1l1l_opy_ = bstack1ll1llll11l1_opy_
        self.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡪࡪࠢ⡾"), bstack1ll1llll11l1_opy_)
    def bstack1llll111_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡩࡳࡷࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧ࠯ࠤ⡿"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack11ll1lll1_opy_.bstack1ll1lll1l11l_opy_()
            if self.bstack11ll1lll1_opy_ is not None:
                orchestration_strategy = self.bstack11ll1lll1_opy_.bstack1lll1111111_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l1llll_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻࠣ࡭ࡸࠦࡎࡰࡰࡨ࠲ࠥࡉࡡ࡯ࡰࡲࡸࠥࡶࡲࡰࡥࡨࡩࡩࠦࡷࡪࡶ࡫ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠱ࠦ⢀"))
                return None
            self.logger.info(bstack1l1llll_opy_ (u"ࠤࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻ࡮ࡺࡨࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻ࠽ࠤࢀࢃࠢ⢁").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l1llll_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡆࡐࡎࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨ⢂"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1l1llll_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡷࡩࡱࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢ⢃"))
                self.bstack1ll1lll1ll11_opy_.bstack1ll1lll1l111_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1ll1lll1ll11_opy_.bstack1ll1lll11lll_opy_()
            if not ordered_test_files:
                return None
            self.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴࡅࡲࡹࡳࡺࠢ⢄"), len(test_files))
            self.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤ⢅"), int(os.environ.get(bstack1l1llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥ⢆")) or bstack1l1llll_opy_ (u"ࠣ࠲ࠥ⢇")))
            self.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨ⢈"), int(os.environ.get(bstack1l1llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ⢉")) or bstack1l1llll_opy_ (u"ࠦ࠶ࠨ⢊")))
            self.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡇࡴࡻ࡮ࡵࠤ⢋"), len(ordered_test_files))
            self.bstack1ll1l1l1_opy_(bstack1l1llll_opy_ (u"ࠨࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡄࡔࡎࡉࡡ࡭࡮ࡆࡳࡺࡴࡴࠣ⢌"), self.bstack1ll1lll1ll11_opy_.bstack1ll1lll11l11_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡰࡦࡹࡳࡦࡵ࠽ࠤࢀࢃࠢ⢍").format(e))
        return None
    def bstack1ll1l1l1_opy_(self, key, value):
        self.bstack1ll1lll11ll1_opy_[key] = value
    def bstack1l11ll111l_opy_(self):
        return self.bstack1ll1lll11ll1_opy_