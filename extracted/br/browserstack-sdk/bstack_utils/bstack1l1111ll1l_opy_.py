# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1llll1ll1l1l_opy_ import bstack1llll1lll11l_opy_
from bstack_utils.bstack1l11llll1l_opy_ import bstack1ll1lll1l_opy_
from bstack_utils.helper import bstack1l11llll_opy_
import json
class bstack11ll11l111_opy_:
    _1ll1l1l1111_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1llll1ll11l1_opy_ = bstack1llll1lll11l_opy_(self.config, logger)
        self.bstack1l11llll1l_opy_ = bstack1ll1lll1l_opy_.get_instance(config=self.config)
        self.bstack1llll1lll1l1_opy_ = {}
        self.bstack1lll1l11l11_opy_ = False
        self.bstack1llll1lll1ll_opy_ = (
            self.__1llll1llll11_opy_()
            and self.bstack1l11llll1l_opy_ is not None
            and self.bstack1l11llll1l_opy_.bstack1l1111ll11_opy_()
            and config.get(bstack1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ⋇"), None) is not None
            and config.get(bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ⋈"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def get_instance(cls, config, logger):
        if cls._1ll1l1l1111_opy_ is None and config is not None:
            cls._1ll1l1l1111_opy_ = bstack11ll11l111_opy_(config, logger)
        return cls._1ll1l1l1111_opy_
    def bstack1l1111ll11_opy_(self):
        bstack1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡊ࡯ࠡࡰࡲࡸࠥࡧࡰࡱ࡮ࡼࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡼ࡮ࡥ࡯࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡑ࠴࠵ࡾࠦࡩࡴࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡕࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡪࡵࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠦࡩࡴࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⋉")
        return self.bstack1llll1lll1ll_opy_ and self.bstack1llll1llllll_opy_()
    def bstack1llll1llllll_opy_(self):
        bstack1llll1lll111_opy_ = os.getenv(bstack1l1_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ⋊"), self.config.get(bstack1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⋋"), None))
        return bstack1llll1lll111_opy_ in bstack111l1l11l11_opy_
    def __1llll1llll11_opy_(self):
        bstack111l1l1ll11_opy_ = False
        for fw in bstack111l111l1ll_opy_:
            if fw in self.config.get(bstack1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⋌"), bstack1l1_opy_ (u"ࠬ࠭⋍")):
                bstack111l1l1ll11_opy_ = True
        return bstack1l11llll_opy_(self.config.get(bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⋎"), bstack111l1l1ll11_opy_))
    def bstack1lllll111111_opy_(self):
        return (not self.bstack1l1111ll11_opy_() and
                self.bstack1l11llll1l_opy_ is not None and self.bstack1l11llll1l_opy_.bstack1l1111ll11_opy_())
    def bstack1llll1lllll1_opy_(self):
        if not self.bstack1lllll111111_opy_():
            return
        if self.config.get(bstack1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ⋏"), None) is None or self.config.get(bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ⋐"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l1_opy_ (u"ࠤࡗࡩࡸࡺࠠࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡨࡧ࡮ࠨࡶࠣࡻࡴࡸ࡫ࠡࡣࡶࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠠࡰࡴࠣࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠡ࡫ࡶࠤࡳࡻ࡬࡭࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡷࡪࡺࠠࡢࠢࡱࡳࡳ࠳࡮ࡶ࡮࡯ࠤࡻࡧ࡬ࡶࡧ࠱ࠦ⋑"))
        if not self.__1llll1llll11_opy_():
            self.logger.info(bstack1l1_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡪࡴࡡࡣ࡮ࡨࠤ࡮ࡺࠠࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡨ࡬ࡰࡪ࠴ࠢ⋒"))
    def bstack1llll1ll1ll1_opy_(self):
        return self.bstack1lll1l11l11_opy_
    def bstack1lll11l1ll1_opy_(self, bstack1llll1ll1l11_opy_):
        self.bstack1lll1l11l11_opy_ = bstack1llll1ll1l11_opy_
        self.bstack1ll1lllllll_opy_(bstack1l1_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠧ⋓"), bstack1llll1ll1l11_opy_)
    def bstack1lll11lll1l_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l1_opy_ (u"ࠧࡡࡲࡦࡱࡵࡨࡪࡸ࡟ࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࡡࠥࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡧࡱࡵࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬࠴ࠢ⋔"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack1l11llll1l_opy_.bstack1llll1llll1l_opy_()
            if self.bstack1l11llll1l_opy_ is not None:
                orchestration_strategy = self.bstack1l11llll1l_opy_.bstack111l1lll_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l1_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡ࡫ࡶࠤࡓࡵ࡮ࡦ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡷࡵࡣࡦࡧࡧࠤࡼ࡯ࡴࡩࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠯ࠤ⋕"))
                return None
            self.logger.info(bstack1l1_opy_ (u"ࠢࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹ࡬ࡸ࡭ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡾࢁࠧ⋖").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l1_opy_ (u"ࠣࡗࡶ࡭ࡳ࡭ࠠࡄࡎࡌࠤ࡫ࡲ࡯ࡸࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦ⋗"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1l1_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡵࡧ࡯ࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧ⋘"))
                self.bstack1llll1ll11l1_opy_.bstack1llll1ll1lll_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1llll1ll11l1_opy_.bstack1lllll11111l_opy_()
            if not ordered_test_files:
                return None
            self.bstack1ll1lllllll_opy_(bstack1l1_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧ⋙"), len(test_files))
            self.bstack1ll1lllllll_opy_(bstack1l1_opy_ (u"ࠦࡳࡵࡤࡦࡋࡱࡨࡪࡾࠢ⋚"), int(os.environ.get(bstack1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣ⋛")) or bstack1l1_opy_ (u"ࠨ࠰ࠣ⋜")))
            self.bstack1ll1lllllll_opy_(bstack1l1_opy_ (u"ࠢࡵࡱࡷࡥࡱࡔ࡯ࡥࡧࡶࠦ⋝"), int(os.environ.get(bstack1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦ⋞")) or bstack1l1_opy_ (u"ࠤ࠴ࠦ⋟")))
            self.bstack1ll1lllllll_opy_(bstack1l1_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴࡅࡲࡹࡳࡺࠢ⋠"), len(ordered_test_files))
            self.bstack1ll1lllllll_opy_(bstack1l1_opy_ (u"ࠦࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳࡂࡒࡌࡇࡦࡲ࡬ࡄࡱࡸࡲࡹࠨ⋡"), self.bstack1llll1ll11l1_opy_.bstack1llll1ll11ll_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠧࡡࡲࡦࡱࡵࡨࡪࡸ࡟ࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࡡࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤ࡮ࡤࡷࡸ࡫ࡳ࠻ࠢࡾࢁࠧ⋢").format(e))
        return None
    def bstack1ll1lllllll_opy_(self, key, value):
        self.bstack1llll1lll1l1_opy_[key] = value
    def bstack11llll1l1_opy_(self):
        return self.bstack1llll1lll1l1_opy_