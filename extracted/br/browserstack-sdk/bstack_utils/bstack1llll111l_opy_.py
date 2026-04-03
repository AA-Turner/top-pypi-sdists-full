# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1lll1l1111ll_opy_ import bstack1lll1l11l111_opy_
from bstack_utils.bstack111l1llll_opy_ import bstack11l1ll1ll_opy_
from bstack_utils.helper import bstack1l111l11l1_opy_
import json
class bstack111l1111ll_opy_:
    _1ll11111111_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1lll1l11l1ll_opy_ = bstack1lll1l11l111_opy_(self.config, logger)
        self.bstack111l1llll_opy_ = bstack11l1ll1ll_opy_.bstack1lllllll1_opy_(config=self.config)
        self.bstack1lll1l1l111l_opy_ = {}
        self.bstack1lllll111ll_opy_ = False
        self.bstack1lll1l111l1l_opy_ = (
            self.__1lll1l11ll11_opy_()
            and self.bstack111l1llll_opy_ is not None
            and self.bstack111l1llll_opy_.bstack1l11111ll1_opy_()
            and config.get(bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬⓇ"), None) is not None
            and config.get(bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫⓈ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1lllllll1_opy_(cls, config, logger):
        if cls._1ll11111111_opy_ is None and config is not None:
            cls._1ll11111111_opy_ = bstack111l1111ll_opy_(config, logger)
        return cls._1ll11111111_opy_
    def bstack1l11111ll1_opy_(self):
        bstack1ll1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡄࡰࠢࡱࡳࡹࠦࡡࡱࡲ࡯ࡽࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡽࡨࡦࡰ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡒ࠵࠶ࡿࠠࡪࡵࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡏࡳࡦࡨࡶ࡮ࡴࡧࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧⓉ")
        return self.bstack1lll1l111l1l_opy_ and self.bstack1lll1l11l11l_opy_()
    def bstack1lll1l11l11l_opy_(self):
        bstack1lll1l11lll1_opy_ = os.getenv(bstack1ll1l11_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫⓊ"), self.config.get(bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧⓋ"), None))
        return bstack1lll1l11lll1_opy_ in bstack11111ll11ll_opy_
    def __1lll1l11ll11_opy_(self):
        bstack11111llll1l_opy_ = False
        for fw in bstack111111ll1l1_opy_:
            if fw in self.config.get(bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨⓌ"), bstack1ll1l11_opy_ (u"࠭ࠧⓍ")):
                bstack11111llll1l_opy_ = True
        return bstack1l111l11l1_opy_(self.config.get(bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫⓎ"), bstack11111llll1l_opy_))
    def bstack1lll1l11llll_opy_(self):
        return (not self.bstack1l11111ll1_opy_() and
                self.bstack111l1llll_opy_ is not None and self.bstack111l1llll_opy_.bstack1l11111ll1_opy_())
    def bstack1lll1l111lll_opy_(self):
        if not self.bstack1lll1l11llll_opy_():
            return
        if self.config.get(bstack1ll1l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ⓩ"), None) is None or self.config.get(bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬⓐ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠡࡱࡵࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡴࡵ࡭࡮࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡸ࡫ࡴࠡࡣࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡼࡡ࡭ࡷࡨ࠲ࠧⓑ"))
        if not self.__1lll1l11ll11_opy_():
            self.logger.info(bstack1ll1l11_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡕࡩࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡣࡢࡰࠪࡸࠥࡽ࡯ࡳ࡭ࠣࡥࡸࠦࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡫࡮ࡢࡤ࡯ࡩࠥ࡯ࡴࠡࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫࠮ࠣⓒ"))
    def bstack1lll1l1l1111_opy_(self):
        return self.bstack1lllll111ll_opy_
    def bstack1llll1lllll_opy_(self, bstack1lll1l11l1l1_opy_):
        self.bstack1lllll111ll_opy_ = bstack1lll1l11l1l1_opy_
        self.bstack1lllll11111_opy_(bstack1ll1l11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠨⓓ"), bstack1lll1l11l1l1_opy_)
    def bstack1lllll11l11_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭࠮ࠣⓔ"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack111l1llll_opy_.bstack1lll1l11ll1l_opy_()
            if self.bstack111l1llll_opy_ is not None:
                orchestration_strategy = self.bstack111l1llll_opy_.bstack111l11111_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺࠢ࡬ࡷࠥࡔ࡯࡯ࡧ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵࡸ࡯ࡤࡧࡨࡨࠥࡽࡩࡵࡪࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠰ࠥⓕ"))
                return None
            self.logger.info(bstack1ll1l11_opy_ (u"ࠣࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡶࡵࡥࡹ࡫ࡧࡺ࠼ࠣࡿࢂࠨⓖ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡅࡏࡍࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧⓗ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1ll1l11_opy_ (u"࡙ࠥࡸ࡯࡮ࡨࠢࡶࡨࡰࠦࡦ࡭ࡱࡺࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨⓘ"))
                self.bstack1lll1l11l1ll_opy_.bstack1lll1l111l11_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1lll1l11l1ll_opy_.bstack1lll1l1111l1_opy_()
            if not ordered_test_files:
                return None
            self.bstack1lllll11111_opy_(bstack1ll1l11_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨⓙ"), len(test_files))
            self.bstack1lllll11111_opy_(bstack1ll1l11_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣⓚ"), int(os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤⓛ")) or bstack1ll1l11_opy_ (u"ࠢ࠱ࠤⓜ")))
            self.bstack1lllll11111_opy_(bstack1ll1l11_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧⓝ"), int(os.environ.get(bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧⓞ")) or bstack1ll1l11_opy_ (u"ࠥ࠵ࠧⓟ")))
            self.bstack1lllll11111_opy_(bstack1ll1l11_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣⓠ"), len(ordered_test_files))
            self.bstack1lllll11111_opy_(bstack1ll1l11_opy_ (u"ࠧࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴࡃࡓࡍࡈࡧ࡬࡭ࡅࡲࡹࡳࡺࠢⓡ"), self.bstack1lll1l11l1ll_opy_.bstack1lll1l111ll1_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨ࡛ࡳࡧࡲࡶࡩ࡫ࡲࡠࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࡢࠦࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥ࡯ࡥࡸࡹࡥࡴ࠼ࠣࡿࢂࠨⓢ").format(e))
        return None
    def bstack1lllll11111_opy_(self, key, value):
        self.bstack1lll1l1l111l_opy_[key] = value
    def bstack1111lll1l_opy_(self):
        return self.bstack1lll1l1l111l_opy_