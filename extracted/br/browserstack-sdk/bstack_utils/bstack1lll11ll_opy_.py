# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack111l1l1lll1_opy_ import bstack111l1l1l1ll_opy_
from bstack_utils.bstack1lll1111ll_opy_ import bstack11llllll_opy_
from bstack_utils.helper import bstack1ll111l11l_opy_
class bstack1l1l111l11_opy_:
    _1llll11l1ll_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack111l1l1ll11_opy_ = bstack111l1l1l1ll_opy_(self.config, logger)
        self.bstack1lll1111ll_opy_ = bstack11llllll_opy_.bstack1ll11ll1_opy_(config=self.config)
        self.bstack111l1ll1l11_opy_ = {}
        self.bstack1111l111ll_opy_ = False
        self.bstack111l1ll111l_opy_ = (
            self.__111l1l1l11l_opy_()
            and self.bstack1lll1111ll_opy_ is not None
            and self.bstack1lll1111ll_opy_.bstack1l111l1l1l_opy_()
            and config.get(bstack111l111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᷨ"), None) is not None
            and config.get(bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᷩ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1ll11ll1_opy_(cls, config, logger):
        if cls._1llll11l1ll_opy_ is None and config is not None:
            cls._1llll11l1ll_opy_ = bstack1l1l111l11_opy_(config, logger)
        return cls._1llll11l1ll_opy_
    def bstack1l111l1l1l_opy_(self):
        bstack111l111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡉࡵࠠ࡯ࡱࡷࠤࡦࡶࡰ࡭ࡻࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡻ࡭࡫࡮࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐ࠳࠴ࡽࠥ࡯ࡳࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡔࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡩࡴࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠣ࡭ࡸࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᷪ")
        return self.bstack111l1ll111l_opy_ and self.bstack111l1ll1111_opy_()
    def bstack111l1ll1111_opy_(self):
        return self.config.get(bstack111l111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᷫ"), None) in bstack11l1ll1lll1_opy_
    def __111l1l1l11l_opy_(self):
        bstack11lll111l1l_opy_ = False
        for fw in bstack11l1ll1l111_opy_:
            if fw in self.config.get(bstack111l111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᷬ"), bstack111l111_opy_ (u"ࠪࠫᷭ")):
                bstack11lll111l1l_opy_ = True
        return bstack1ll111l11l_opy_(self.config.get(bstack111l111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᷮ"), bstack11lll111l1l_opy_))
    def bstack111l1l1l1l1_opy_(self):
        return (not self.bstack1l111l1l1l_opy_() and
                self.bstack1lll1111ll_opy_ is not None and self.bstack1lll1111ll_opy_.bstack1l111l1l1l_opy_())
    def bstack111l1l1l111_opy_(self):
        if not self.bstack111l1l1l1l1_opy_():
            return
        if self.config.get(bstack111l111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᷯ"), None) is None or self.config.get(bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᷰ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack111l111_opy_ (u"ࠢࡕࡧࡶࡸࠥࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡦࡥࡳ࠭ࡴࠡࡹࡲࡶࡰࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥࡵࡲࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡱࡹࡱࡲ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡵࡨࡸࠥࡧࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥ࠯ࠤᷱ"))
        if not self.__111l1l1l11l_opy_():
            self.logger.info(bstack111l111_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡪࡵࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡥ࡯ࡣࡥࡰࡪࠦࡩࡵࠢࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠯ࠤᷲ"))
    def bstack111l1ll11l1_opy_(self):
        return self.bstack1111l111ll_opy_
    def bstack1111l11111_opy_(self, bstack111l1ll11ll_opy_):
        self.bstack1111l111ll_opy_ = bstack111l1ll11ll_opy_
        self.bstack11111l1l1l_opy_(bstack111l111_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠥᷳ"), bstack111l1ll11ll_opy_)
    def bstack1111l1llll_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack111l111_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡲࡶࡩ࡫ࡲࡪࡰࡪ࠲ࠧᷴ"))
                return None
            orchestration_strategy = None
            if self.bstack1lll1111ll_opy_ is not None:
                orchestration_strategy = self.bstack1lll1111ll_opy_.bstack11llll11_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack111l111_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦࡩࡴࠢࡑࡳࡳ࡫࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡵࡳࡨ࡫ࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠴ࠢ᷵"))
                return None
            self.logger.info(bstack111l111_opy_ (u"ࠧࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥ᷶").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack111l111_opy_ (u"ࠨࡕࡴ࡫ࡱ࡫ࠥࡉࡌࡊࠢࡩࡰࡴࡽࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤ᷷"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy)
            else:
                self.logger.debug(bstack111l111_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡳࡥ࡭ࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰᷸ࠥ"))
                self.bstack111l1l1ll11_opy_.bstack111l1l11lll_opy_(test_files, orchestration_strategy)
                ordered_test_files = self.bstack111l1l1ll11_opy_.bstack111l1l1ll1l_opy_()
            if not ordered_test_files:
                return None
            self.bstack11111l1l1l_opy_(bstack111l111_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶ᷹ࠥ"), len(test_files))
            self.bstack11111l1l1l_opy_(bstack111l111_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼ᷺ࠧ"), int(os.environ.get(bstack111l111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨ᷻")) or bstack111l111_opy_ (u"ࠦ࠵ࠨ᷼")))
            self.bstack11111l1l1l_opy_(bstack111l111_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤ᷽"), int(os.environ.get(bstack111l111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ᷾")) or bstack111l111_opy_ (u"ࠢ࠲ࠤ᷿")))
            self.bstack11111l1l1l_opy_(bstack111l111_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧḀ"), len(ordered_test_files))
            self.bstack11111l1l1l_opy_(bstack111l111_opy_ (u"ࠤࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡇࡐࡊࡅࡤࡰࡱࡉ࡯ࡶࡰࡷࠦḁ"), self.bstack111l1l1ll11_opy_.bstack111l1l1llll_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩ࡬ࡢࡵࡶࡩࡸࡀࠠࡼࡿࠥḂ").format(e))
        return None
    def bstack11111l1l1l_opy_(self, key, value):
        self.bstack111l1ll1l11_opy_[key] = value
    def bstack1l1lllll_opy_(self):
        return self.bstack111l1ll1l11_opy_