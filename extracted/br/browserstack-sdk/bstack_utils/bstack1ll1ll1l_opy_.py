# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack11111llllll_opy_ import bstack11111ll1l1l_opy_
from bstack_utils.bstack111l1111_opy_ import bstack1l1llll1l_opy_
from bstack_utils.helper import bstack1l1111lll1_opy_
import json
class bstack11111l1l1_opy_:
    _1ll1ll1l11l_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1111l1111ll_opy_ = bstack11111ll1l1l_opy_(self.config, logger)
        self.bstack111l1111_opy_ = bstack1l1llll1l_opy_.bstack111ll1lll1_opy_(config=self.config)
        self.bstack11111lll1ll_opy_ = {}
        self.bstack1lllll11111_opy_ = False
        self.bstack11111ll1lll_opy_ = (
            self.__1111l11111l_opy_()
            and self.bstack111l1111_opy_ is not None
            and self.bstack111l1111_opy_.bstack1l11111l_opy_()
            and config.get(bstack1l1111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᾋ"), None) is not None
            and config.get(bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᾌ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack111ll1lll1_opy_(cls, config, logger):
        if cls._1ll1ll1l11l_opy_ is None and config is not None:
            cls._1ll1ll1l11l_opy_ = bstack11111l1l1_opy_(config, logger)
        return cls._1ll1ll1l11l_opy_
    def bstack1l11111l_opy_(self):
        bstack1l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡈࡴࠦ࡮ࡰࡶࠣࡥࡵࡶ࡬ࡺࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡺ࡬ࡪࡴ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡏ࠲࠳ࡼࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡓࡷࡪࡥࡳ࡫ࡱ࡫ࠥ࡯ࡳࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᾍ")
        return self.bstack11111ll1lll_opy_ and self.bstack11111lllll1_opy_()
    def bstack11111lllll1_opy_(self):
        bstack11111lll1l1_opy_ = os.getenv(bstack1l1111_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨᾎ"), self.config.get(bstack1l1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᾏ"), None))
        return bstack11111lll1l1_opy_ in bstack11l1111llll_opy_
    def __1111l11111l_opy_(self):
        bstack11l11l1llll_opy_ = False
        for fw in bstack11l11l1ll11_opy_:
            if fw in self.config.get(bstack1l1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᾐ"), bstack1l1111_opy_ (u"ࠪࠫᾑ")):
                bstack11l11l1llll_opy_ = True
        return bstack1l1111lll1_opy_(self.config.get(bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᾒ"), bstack11l11l1llll_opy_))
    def bstack1111l1111l1_opy_(self):
        return (not self.bstack1l11111l_opy_() and
                self.bstack111l1111_opy_ is not None and self.bstack111l1111_opy_.bstack1l11111l_opy_())
    def bstack11111ll1l11_opy_(self):
        if not self.bstack1111l1111l1_opy_():
            return
        if self.config.get(bstack1l1111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᾓ"), None) is None or self.config.get(bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᾔ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l1111_opy_ (u"ࠢࡕࡧࡶࡸࠥࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡦࡥࡳ࠭ࡴࠡࡹࡲࡶࡰࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥࡵࡲࠡࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠦࡩࡴࠢࡱࡹࡱࡲ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡵࡨࡸࠥࡧࠠ࡯ࡱࡱ࠱ࡳࡻ࡬࡭ࠢࡹࡥࡱࡻࡥ࠯ࠤᾕ"))
        if not self.__1111l11111l_opy_():
            self.logger.info(bstack1l1111_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡤࡪࡵࡤࡦࡱ࡫ࡤ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡨࡲࡦࡨ࡬ࡦࠢ࡬ࡸࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲ࠧᾖ"))
    def bstack11111llll1l_opy_(self):
        return self.bstack1lllll11111_opy_
    def bstack1lllll11lll_opy_(self, bstack11111lll11l_opy_):
        self.bstack1lllll11111_opy_ = bstack11111lll11l_opy_
        self.bstack1llll1l11ll_opy_(bstack1l1111_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠥᾗ"), bstack11111lll11l_opy_)
    def bstack1lllll111l1_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l1111_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥ࡬࡯ࡳࠢࡲࡶࡩ࡫ࡲࡪࡰࡪ࠲ࠧᾘ"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack111l1111_opy_.bstack11111lll111_opy_()
            if self.bstack111l1111_opy_ is not None:
                orchestration_strategy = self.bstack111l1111_opy_.bstack1ll1l11111_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l1111_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦࡩࡴࠢࡑࡳࡳ࡫࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡵࡳࡨ࡫ࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠴ࠢᾙ"))
                return None
            self.logger.info(bstack1l1111_opy_ (u"ࠧࡘࡥࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥᾚ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l1111_opy_ (u"ࠨࡕࡴ࡫ࡱ࡫ࠥࡉࡌࡊࠢࡩࡰࡴࡽࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤᾛ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1l1111_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡳࡥ࡭ࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥᾜ"))
                self.bstack1111l1111ll_opy_.bstack11111llll11_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1111l1111ll_opy_.bstack1111l111111_opy_()
            if not ordered_test_files:
                return None
            self.bstack1llll1l11ll_opy_(bstack1l1111_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥᾝ"), len(test_files))
            self.bstack1llll1l11ll_opy_(bstack1l1111_opy_ (u"ࠤࡱࡳࡩ࡫ࡉ࡯ࡦࡨࡼࠧᾞ"), int(os.environ.get(bstack1l1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨᾟ")) or bstack1l1111_opy_ (u"ࠦ࠵ࠨᾠ")))
            self.bstack1llll1l11ll_opy_(bstack1l1111_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࡒࡴࡪࡥࡴࠤᾡ"), int(os.environ.get(bstack1l1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤᾢ")) or bstack1l1111_opy_ (u"ࠢ࠲ࠤᾣ")))
            self.bstack1llll1l11ll_opy_(bstack1l1111_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹࡃࡰࡷࡱࡸࠧᾤ"), len(ordered_test_files))
            self.bstack1llll1l11ll_opy_(bstack1l1111_opy_ (u"ࠤࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡇࡐࡊࡅࡤࡰࡱࡉ࡯ࡶࡰࡷࠦᾥ"), self.bstack1111l1111ll_opy_.bstack11111ll1ll1_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l1111_opy_ (u"ࠥ࡟ࡷ࡫࡯ࡳࡦࡨࡶࡤࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴ࡟ࠣࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩ࡬ࡢࡵࡶࡩࡸࡀࠠࡼࡿࠥᾦ").format(e))
        return None
    def bstack1llll1l11ll_opy_(self, key, value):
        self.bstack11111lll1ll_opy_[key] = value
    def bstack111l1111l_opy_(self):
        return self.bstack11111lll1ll_opy_