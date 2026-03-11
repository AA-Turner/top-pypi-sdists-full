# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1111l1l1l11_opy_ import bstack1111l1l1111_opy_
from bstack_utils.bstack111ll11l_opy_ import bstack1l1ll111l_opy_
from bstack_utils.helper import bstack1l11lll111_opy_
import json
class bstack11l11llll1_opy_:
    _1ll1111llll_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1111l1l111l_opy_ = bstack1111l1l1111_opy_(self.config, logger)
        self.bstack111ll11l_opy_ = bstack1l1ll111l_opy_.get_instance(config=self.config)
        self.bstack1111l111l1l_opy_ = {}
        self.bstack1lll1llll1l_opy_ = False
        self.bstack1111l11ll11_opy_ = (
            self.__1111l11ll1l_opy_()
            and self.bstack111ll11l_opy_ is not None
            and self.bstack111ll11l_opy_.bstack11l1ll11ll_opy_()
            and config.get(bstack1ll111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᳡"), None) is not None
            and config.get(bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ᳢ࠬ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def get_instance(cls, config, logger):
        if cls._1ll1111llll_opy_ is None and config is not None:
            cls._1ll1111llll_opy_ = bstack11l11llll1_opy_(config, logger)
        return cls._1ll1111llll_opy_
    def bstack11l1ll11ll_opy_(self):
        bstack1ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡱࠣࡲࡴࡺࠠࡢࡲࡳࡰࡾࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡷࡩࡧࡱ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓ࠶࠷ࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐࡴࡧࡩࡷ࡯࡮ࡨࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᳣")
        return self.bstack1111l11ll11_opy_ and self.bstack1111l11l1l1_opy_()
    def bstack1111l11l1l1_opy_(self):
        bstack1111l1l11ll_opy_ = os.getenv(bstack1ll111_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈ᳤ࠬ"), self.config.get(bstack1ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ᳥"), None))
        return bstack1111l1l11ll_opy_ in bstack1111l111l11_opy_
    def __1111l11ll1l_opy_(self):
        bstack1111l11lll1_opy_ = False
        for fw in bstack1111l1l11l1_opy_:
            if fw in self.config.get(bstack1ll111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬᳦ࠩ"), bstack1ll111_opy_ (u"ࠧࠨ᳧")):
                bstack1111l11lll1_opy_ = True
        return bstack1l11lll111_opy_(self.config.get(bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ᳨ࠬ"), bstack1111l11lll1_opy_))
    def bstack1111l111ll1_opy_(self):
        return (not self.bstack11l1ll11ll_opy_() and
                self.bstack111ll11l_opy_ is not None and self.bstack111ll11l_opy_.bstack11l1ll11ll_opy_())
    def bstack1111l111lll_opy_(self):
        if not self.bstack1111l111ll1_opy_():
            return
        if self.config.get(bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᳩ"), None) is None or self.config.get(bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᳪ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1ll111_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢࡲࡶࠥࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠣ࡭ࡸࠦ࡮ࡶ࡮࡯࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡹࡥࡵࠢࡤࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡶࡢ࡮ࡸࡩ࠳ࠨᳫ"))
        if not self.__1111l11ll1l_opy_():
            self.logger.info(bstack1ll111_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡥ࡯ࡣࡥࡰࡪࠦࡩࡵࠢࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠯ࠤᳬ"))
    def bstack1111l11l1ll_opy_(self):
        return self.bstack1lll1llll1l_opy_
    def bstack1lll1llll11_opy_(self, bstack1111l11llll_opy_):
        self.bstack1lll1llll1l_opy_ = bstack1111l11llll_opy_
        self.bstack1lll1ll1lll_opy_(bstack1ll111_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡪࡪ᳭ࠢ"), bstack1111l11llll_opy_)
    def bstack1lll11lllll_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1ll111_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡩࡳࡷࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧ࠯ࠤᳮ"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack111ll11l_opy_.bstack1111l11l11l_opy_()
            if self.bstack111ll11l_opy_ is not None:
                orchestration_strategy = self.bstack111ll11l_opy_.bstack1111lll1l1_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1ll111_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻࠣ࡭ࡸࠦࡎࡰࡰࡨ࠲ࠥࡉࡡ࡯ࡰࡲࡸࠥࡶࡲࡰࡥࡨࡩࡩࠦࡷࡪࡶ࡫ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠱ࠦᳯ"))
                return None
            self.logger.info(bstack1ll111_opy_ (u"ࠤࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻ࡮ࡺࡨࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡷࡶࡦࡺࡥࡨࡻ࠽ࠤࢀࢃࠢᳰ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1ll111_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡆࡐࡎࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨᳱ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1ll111_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡷࡩࡱࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢᳲ"))
                self.bstack1111l1l111l_opy_.bstack1111l11l111_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1111l1l111l_opy_.bstack1111l1111ll_opy_()
            if not ordered_test_files:
                return None
            self.bstack1lll1ll1lll_opy_(bstack1ll111_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴࡅࡲࡹࡳࡺࠢᳳ"), len(test_files))
            self.bstack1lll1ll1lll_opy_(bstack1ll111_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤ᳴"), int(os.environ.get(bstack1ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥᳵ")) or bstack1ll111_opy_ (u"ࠣ࠲ࠥᳶ")))
            self.bstack1lll1ll1lll_opy_(bstack1ll111_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨ᳷"), int(os.environ.get(bstack1ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ᳸")) or bstack1ll111_opy_ (u"ࠦ࠶ࠨ᳹")))
            self.bstack1lll1ll1lll_opy_(bstack1ll111_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡇࡴࡻ࡮ࡵࠤᳺ"), len(ordered_test_files))
            self.bstack1lll1ll1lll_opy_(bstack1ll111_opy_ (u"ࠨࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡄࡔࡎࡉࡡ࡭࡮ࡆࡳࡺࡴࡴࠣ᳻"), self.bstack1111l1l111l_opy_.bstack1111l1l1l1l_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢ࡜ࡴࡨࡳࡷࡪࡥࡳࡡࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࡣࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡰࡦࡹࡳࡦࡵ࠽ࠤࢀࢃࠢ᳼").format(e))
        return None
    def bstack1lll1ll1lll_opy_(self, key, value):
        self.bstack1111l111l1l_opy_[key] = value
    def bstack1lll1ll11l_opy_(self):
        return self.bstack1111l111l1l_opy_