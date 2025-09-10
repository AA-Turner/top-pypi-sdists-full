# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l11l111l_opy_ import bstack111l111llll_opy_
from bstack_utils.bstack11l1l11l11_opy_ import bstack1ll1l111_opy_
from bstack_utils.helper import bstack1l1l1llll1_opy_
class bstack1ll1l1ll1_opy_:
    _1lll111l11l_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l111l1l1_opy_ = bstack111l111llll_opy_(self.config, logger)
        self.bstack11l1l11l11_opy_ = bstack1ll1l111_opy_.bstack11l11lllll_opy_(config=self.config)
        self.bstack111l111ll1l_opy_ = {}
        self.bstack11111l1ll1_opy_ = False
        self.bstack111l1111l11_opy_ = (
            self.__111l11l11ll_opy_()
            and self.bstack11l1l11l11_opy_ is not None
            and self.bstack11l1l11l11_opy_.bstack11l11l11ll_opy_()
            and config.get(bstack1ll11ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬḷ"), None) is not None
            and config.get(bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫḸ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack11l11lllll_opy_(cls, config, logger):
        if cls._1lll111l11l_opy_ is None and config is not None:
            cls._1lll111l11l_opy_ = bstack1ll1l1ll1_opy_(config, logger)
        return cls._1lll111l11l_opy_
    def bstack11l11l11ll_opy_(self):
        bstack1ll11ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡄࡰࠢࡱࡳࡹࠦࡡࡱࡲ࡯ࡽࠥࡺࡥࡴࡶࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡽࡨࡦࡰ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡒ࠵࠶ࡿࠠࡪࡵࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡏࡳࡦࡨࡶ࡮ࡴࡧࠡ࡫ࡶࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧḹ")
        return self.bstack111l1111l11_opy_ and self.bstack111l111l1ll_opy_()
    def bstack111l111l1ll_opy_(self):
        return self.config.get(bstack1ll11ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭Ḻ"), None) in bstack11l1l1l11l1_opy_
    def __111l11l11ll_opy_(self):
        bstack11l1lll1ll1_opy_ = False
        for fw in bstack11l1ll1llll_opy_:
            if fw in self.config.get(bstack1ll11ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧḻ"), bstack1ll11ll_opy_ (u"ࠬ࠭Ḽ")):
                bstack11l1lll1ll1_opy_ = True
        return bstack1l1l1llll1_opy_(self.config.get(bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḽ"), bstack11l1lll1ll1_opy_))
    def bstack111l111ll11_opy_(self):
        return (not self.bstack11l11l11ll_opy_() and
                self.bstack11l1l11l11_opy_ is not None and self.bstack11l1l11l11_opy_.bstack11l11l11ll_opy_())
    def bstack111l1111ll1_opy_(self):
        if not self.bstack111l111ll11_opy_():
            return
        if self.config.get(bstack1ll11ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬḾ"), None) is None or self.config.get(bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫḿ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1ll11ll_opy_ (u"ࠤࡗࡩࡸࡺࠠࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡨࡧ࡮ࠨࡶࠣࡻࡴࡸ࡫ࠡࡣࡶࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠠࡰࡴࠣࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠡ࡫ࡶࠤࡳࡻ࡬࡭࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡷࡪࡺࠠࡢࠢࡱࡳࡳ࠳࡮ࡶ࡮࡯ࠤࡻࡧ࡬ࡶࡧ࠱ࠦṀ"))
        if not self.__111l11l11ll_opy_():
            self.logger.info(bstack1ll11ll_opy_ (u"ࠥࡘࡪࡹࡴࠡࡔࡨࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡩࡡ࡯ࠩࡷࠤࡼࡵࡲ࡬ࠢࡤࡷࠥࡺࡥࡴࡶࡕࡩࡵࡵࡲࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡪࡴࡡࡣ࡮ࡨࠤ࡮ࡺࠠࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡨ࡬ࡰࡪ࠴ࠢṁ"))
    def bstack111l111l111_opy_(self):
        return self.bstack11111l1ll1_opy_
    def bstack11111lll11_opy_(self, bstack111l11l1111_opy_):
        self.bstack11111l1ll1_opy_ = bstack111l11l1111_opy_
        self.bstack1111l11111_opy_(bstack1ll11ll_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠧṂ"), bstack111l11l1111_opy_)
    def bstack11111l1lll_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡡࡲࡦࡱࡵࡨࡪࡸ࡟ࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࡡࠥࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡧࡱࡵࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬࠴ࠢṃ"))
                return None
            orchestration_strategy = None
            bstack111l111l11l_opy_ = self.bstack11l1l11l11_opy_.bstack111l11l11l1_opy_()
            if self.bstack11l1l11l11_opy_ is not None:
                orchestration_strategy = self.bstack11l1l11l11_opy_.bstack1l1ll1l111_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡ࡫ࡶࠤࡓࡵ࡮ࡦ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡷࡵࡣࡦࡧࡧࠤࡼ࡯ࡴࡩࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠯ࠤṄ"))
                return None
            self.logger.info(bstack1ll11ll_opy_ (u"ࠢࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹ࡬ࡸ࡭ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡵࡴࡤࡸࡪ࡭ࡹ࠻ࠢࡾࢁࠧṅ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡗࡶ࡭ࡳ࡭ࠠࡄࡎࡌࠤ࡫ࡲ࡯ࡸࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦṆ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡘࡷ࡮ࡴࡧࠡࡵࡧ࡯ࠥ࡬࡬ࡰࡹࠣࡪࡴࡸࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧṇ"))
                self.bstack111l111l1l1_opy_.bstack111l1111lll_opy_(test_files, orchestration_strategy, bstack111l111l11l_opy_)
                ordered_test_files = self.bstack111l111l1l1_opy_.bstack111l111lll1_opy_()
            if not ordered_test_files:
                return None
            self.bstack1111l11111_opy_(bstack1ll11ll_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧṈ"), len(test_files))
            self.bstack1111l11111_opy_(bstack1ll11ll_opy_ (u"ࠦࡳࡵࡤࡦࡋࡱࡨࡪࡾࠢṉ"), int(os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣṊ")) or bstack1ll11ll_opy_ (u"ࠨ࠰ࠣṋ")))
            self.bstack1111l11111_opy_(bstack1ll11ll_opy_ (u"ࠢࡵࡱࡷࡥࡱࡔ࡯ࡥࡧࡶࠦṌ"), int(os.environ.get(bstack1ll11ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦṍ")) or bstack1ll11ll_opy_ (u"ࠤ࠴ࠦṎ")))
            self.bstack1111l11111_opy_(bstack1ll11ll_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴࡅࡲࡹࡳࡺࠢṏ"), len(ordered_test_files))
            self.bstack1111l11111_opy_(bstack1ll11ll_opy_ (u"ࠦࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳࡂࡒࡌࡇࡦࡲ࡬ࡄࡱࡸࡲࡹࠨṐ"), self.bstack111l111l1l1_opy_.bstack111l1111l1l_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡡࡲࡦࡱࡵࡨࡪࡸ࡟ࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࡡࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤ࡮ࡤࡷࡸ࡫ࡳ࠻ࠢࡾࢁࠧṑ").format(e))
        return None
    def bstack1111l11111_opy_(self, key, value):
        self.bstack111l111ll1l_opy_[key] = value
    def bstack11l11111l1_opy_(self):
        return self.bstack111l111ll1l_opy_