# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1lllll111l1l_opy_ import bstack1llll1ll1ll1_opy_
from bstack_utils.bstack1111ll1l_opy_ import bstack11lllllll_opy_
from bstack_utils.helper import bstack1lll11l1_opy_
import json
class bstack1l1l1ll1ll_opy_:
    _1ll1l1lll11_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1llll1lll11l_opy_ = bstack1llll1ll1ll1_opy_(self.config, logger)
        self.bstack1111ll1l_opy_ = bstack11lllllll_opy_.get_instance(config=self.config)
        self.bstack1lllll11111l_opy_ = {}
        self.bstack1lll11l1l1l_opy_ = False
        self.bstack1llll1lllll1_opy_ = (
            self.__1llll1lll111_opy_()
            and self.bstack1111ll1l_opy_ is not None
            and self.bstack1111ll1l_opy_.bstack1l1lllll_opy_()
            and config.get(bstack11lll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⊼"), None) is not None
            and config.get(bstack11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⊽"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def get_instance(cls, config, logger):
        if cls._1ll1l1lll11_opy_ is None and config is not None:
            cls._1ll1l1lll11_opy_ = bstack1l1l1ll1ll_opy_(config, logger)
        return cls._1ll1l1lll11_opy_
    def bstack1l1lllll_opy_(self):
        bstack11lll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡲࠤࡳࡵࡴࠡࡣࡳࡴࡱࡿࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡸࡪࡨࡲ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡔ࠷࠱ࡺࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡑࡵࡨࡪࡸࡩ࡯ࡩࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⊾")
        return self.bstack1llll1lllll1_opy_ and self.bstack1llll1llll1l_opy_()
    def bstack1llll1llll1l_opy_(self):
        bstack1lllll1111ll_opy_ = os.getenv(bstack11lll1_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭⊿"), self.config.get(bstack11lll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⋀"), None))
        return bstack1lllll1111ll_opy_ in bstack111l1l1l111_opy_
    def __1llll1lll111_opy_(self):
        bstack111l1ll11l1_opy_ = False
        for fw in bstack111l11ll11l_opy_:
            if fw in self.config.get(bstack11lll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⋁"), bstack11lll1_opy_ (u"ࠨࠩ⋂")):
                bstack111l1ll11l1_opy_ = True
        return bstack1lll11l1_opy_(self.config.get(bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⋃"), bstack111l1ll11l1_opy_))
    def bstack1llll1llll11_opy_(self):
        return (not self.bstack1l1lllll_opy_() and
                self.bstack1111ll1l_opy_ is not None and self.bstack1111ll1l_opy_.bstack1l1lllll_opy_())
    def bstack1llll1lll1ll_opy_(self):
        if not self.bstack1llll1llll11_opy_():
            return
        if self.config.get(bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ⋄"), None) is None or self.config.get(bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ⋅"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11lll1_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠣࡳࡷࠦࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠤ࡮ࡹࠠ࡯ࡷ࡯ࡰ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡳࡦࡶࠣࡥࠥࡴ࡯࡯࠯ࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠴ࠢ⋆"))
        if not self.__1llll1lll111_opy_():
            self.logger.info(bstack11lll1_opy_ (u"ࠨࡔࡦࡵࡷࠤࡗ࡫࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡥࡤࡲࠬࡺࠠࡸࡱࡵ࡯ࠥࡧࡳࠡࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡦࡰࡤࡦࡱ࡫ࠠࡪࡶࠣࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠰ࠥ⋇"))
    def bstack1lllll1111l1_opy_(self):
        return self.bstack1lll11l1l1l_opy_
    def bstack1lll111ll1l_opy_(self, bstack1llll1lll1l1_opy_):
        self.bstack1lll11l1l1l_opy_ = bstack1llll1lll1l1_opy_
        self.bstack1lll11llll1_opy_(bstack11lll1_opy_ (u"ࠢࡢࡲࡳࡰ࡮࡫ࡤࠣ⋈"), bstack1llll1lll1l1_opy_)
    def bstack1lll1l1111l_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11lll1_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡰࡴࡧࡩࡷ࡯࡮ࡨ࠰ࠥ⋉"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack1111ll1l_opy_.bstack1lllll111l11_opy_()
            if self.bstack1111ll1l_opy_ is not None:
                orchestration_strategy = self.bstack1111ll1l_opy_.bstack11l1l11ll1_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11lll1_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼࠤ࡮ࡹࠠࡏࡱࡱࡩ࠳ࠦࡃࡢࡰࡱࡳࡹࠦࡰࡳࡱࡦࡩࡪࡪࠠࡸ࡫ࡷ࡬ࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠲ࠧ⋊"))
                return None
            self.logger.info(bstack11lll1_opy_ (u"ࠥࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡯ࡴࡩࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣ⋋").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11lll1_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡇࡑࡏࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢ⋌"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack11lll1_opy_ (u"࡛ࠧࡳࡪࡰࡪࠤࡸࡪ࡫ࠡࡨ࡯ࡳࡼࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣ⋍"))
                self.bstack1llll1lll11l_opy_.bstack1llll1ll1lll_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1llll1lll11l_opy_.bstack1lllll111111_opy_()
            if not ordered_test_files:
                return None
            self.bstack1lll11llll1_opy_(bstack11lll1_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣ⋎"), len(test_files))
            self.bstack1lll11llll1_opy_(bstack11lll1_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥ⋏"), int(os.environ.get(bstack11lll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ⋐")) or bstack11lll1_opy_ (u"ࠤ࠳ࠦ⋑")))
            self.bstack1lll11llll1_opy_(bstack11lll1_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢ⋒"), int(os.environ.get(bstack11lll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢ⋓")) or bstack11lll1_opy_ (u"ࠧ࠷ࠢ⋔")))
            self.bstack1lll11llll1_opy_(bstack11lll1_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥ⋕"), len(ordered_test_files))
            self.bstack1lll11llll1_opy_(bstack11lll1_opy_ (u"ࠢࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡅࡕࡏࡃࡢ࡮࡯ࡇࡴࡻ࡮ࡵࠤ⋖"), self.bstack1llll1lll11l_opy_.bstack1llll1llllll_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡱࡧࡳࡴࡧࡶ࠾ࠥࢁࡽࠣ⋗").format(e))
        return None
    def bstack1lll11llll1_opy_(self, key, value):
        self.bstack1lllll11111l_opy_[key] = value
    def bstack1l111ll1ll_opy_(self):
        return self.bstack1lllll11111l_opy_