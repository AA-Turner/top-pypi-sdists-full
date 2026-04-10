# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1lll11lllll1_opy_ import bstack1lll1l111l11_opy_
from bstack_utils.bstack1ll1ll1ll_opy_ import bstack1l111111ll_opy_
from bstack_utils.helper import bstack11l1l1l11l_opy_
import json
class bstack1l11ll1ll_opy_:
    _1ll1111l111_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1lll1l11l11l_opy_ = bstack1lll1l111l11_opy_(self.config, logger)
        self.bstack1ll1ll1ll_opy_ = bstack1l111111ll_opy_.bstack1l111l1111_opy_(config=self.config)
        self.bstack1lll1l1111l1_opy_ = {}
        self.bstack1llll1lllll_opy_ = False
        self.bstack1lll1l11l1l1_opy_ = (
            self.__1lll1l11l1ll_opy_()
            and self.bstack1ll1ll1ll_opy_ is not None
            and self.bstack1ll1ll1ll_opy_.bstack1llll111ll_opy_()
            and config.get(bstack1ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩⓋ"), None) is not None
            and config.get(bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨⓌ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1l111l1111_opy_(cls, config, logger):
        if cls._1ll1111l111_opy_ is None and config is not None:
            cls._1ll1111l111_opy_ = bstack1l11ll1ll_opy_(config, logger)
        return cls._1ll1111l111_opy_
    def bstack1llll111ll_opy_(self):
        bstack1ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡈࡴࠦ࡮ࡰࡶࠣࡥࡵࡶ࡬ࡺࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡺ࡬ࡪࡴ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡏ࠲࠳ࡼࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓࡷࡪࡥࡳ࡫ࡱ࡫ࠥ࡯ࡳࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤⓍ")
        return self.bstack1lll1l11l1l1_opy_ and self.bstack1lll1l111lll_opy_()
    def bstack1lll1l111lll_opy_(self):
        bstack1lll11llll1l_opy_ = os.getenv(bstack1ll_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨⓎ"), self.config.get(bstack1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫⓏ"), None))
        return bstack1lll11llll1l_opy_ in bstack11111ll11ll_opy_
    def __1lll1l11l1ll_opy_(self):
        bstack11111ll1lll_opy_ = False
        for fw in bstack111111ll1l1_opy_:
            if fw in self.config.get(bstack1ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬⓐ"), bstack1ll_opy_ (u"ࠪࠫⓑ")):
                bstack11111ll1lll_opy_ = True
        return bstack11l1l1l11l_opy_(self.config.get(bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨⓒ"), bstack11111ll1lll_opy_))
    def bstack1lll1l1111ll_opy_(self):
        return (not self.bstack1llll111ll_opy_() and
                self.bstack1ll1ll1ll_opy_ is not None and self.bstack1ll1ll1ll_opy_.bstack1llll111ll_opy_())
    def bstack1lll1l111l1l_opy_(self):
        if not self.bstack1lll1l1111ll_opy_():
            return
        if self.config.get(bstack1ll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪⓓ"), None) is None or self.config.get(bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩⓔ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1ll_opy_ (u"ࠢࡕࡧࡶࡸࠥࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡦࡥࡳ࠭ࡴࠡࡹࡲࡶࡰࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥࡵࡲࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡱࡹࡱࡲ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡵࡨࡸࠥࡧࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥ࠯ࠤⓕ"))
        if not self.__1lll1l11l1ll_opy_():
            self.logger.info(bstack1ll_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡤࡪࡵࡤࡦࡱ࡫ࡤ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡨࡲࡦࡨ࡬ࡦࠢ࡬ࡸࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲ࠧⓖ"))
    def bstack1lll1l11111l_opy_(self):
        return self.bstack1llll1lllll_opy_
    def bstack1llll1llll1_opy_(self, bstack1lll1l11l111_opy_):
        self.bstack1llll1lllll_opy_ = bstack1lll1l11l111_opy_
        self.bstack1lllll111ll_opy_(bstack1ll_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠥⓗ"), bstack1lll1l11l111_opy_)
    def bstack1llll1lll1l_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1ll_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡲࡶࡩ࡫ࡲࡪࡰࡪ࠲ࠧⓘ"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack1ll1ll1ll_opy_.bstack1lll11llll11_opy_()
            if self.bstack1ll1ll1ll_opy_ is not None:
                orchestration_strategy = self.bstack1ll1ll1ll_opy_.bstack1l1l11ll1_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1ll_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦࡩࡴࠢࡑࡳࡳ࡫࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡵࡳࡨ࡫ࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠴ࠢⓙ"))
                return None
            self.logger.info(bstack1ll_opy_ (u"ࠧࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥⓚ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1ll_opy_ (u"ࠨࡕࡴ࡫ࡱ࡫ࠥࡉࡌࡊࠢࡩࡰࡴࡽࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤⓛ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1ll_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡳࡥ࡭ࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥⓜ"))
                self.bstack1lll1l11l11l_opy_.bstack1lll1l111111_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1lll1l11l11l_opy_.bstack1lll11llllll_opy_()
            if not ordered_test_files:
                return None
            self.bstack1lllll111ll_opy_(bstack1ll_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥⓝ"), len(test_files))
            self.bstack1lllll111ll_opy_(bstack1ll_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧⓞ"), int(os.environ.get(bstack1ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨⓟ")) or bstack1ll_opy_ (u"ࠦ࠵ࠨⓠ")))
            self.bstack1lllll111ll_opy_(bstack1ll_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤⓡ"), int(os.environ.get(bstack1ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤⓢ")) or bstack1ll_opy_ (u"ࠢ࠲ࠤⓣ")))
            self.bstack1lllll111ll_opy_(bstack1ll_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧⓤ"), len(ordered_test_files))
            self.bstack1lllll111ll_opy_(bstack1ll_opy_ (u"ࠤࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡇࡐࡊࡅࡤࡰࡱࡉ࡯ࡶࡰࡷࠦⓥ"), self.bstack1lll1l11l11l_opy_.bstack1lll1l111ll1_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1ll_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩ࡬ࡢࡵࡶࡩࡸࡀࠠࡼࡿࠥⓦ").format(e))
        return None
    def bstack1lllll111ll_opy_(self, key, value):
        self.bstack1lll1l1111l1_opy_[key] = value
    def bstack1llllllll1_opy_(self):
        return self.bstack1lll1l1111l1_opy_