# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack11111ll1111_opy_ import bstack11111lll1l1_opy_
from bstack_utils.bstack1l1ll1l111_opy_ import bstack11111l1l_opy_
from bstack_utils.helper import bstack1ll1lll1l_opy_
import json
class bstack1l1lllll1l_opy_:
    _1ll1l1lll11_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack11111ll11l1_opy_ = bstack11111lll1l1_opy_(self.config, logger)
        self.bstack1l1ll1l111_opy_ = bstack11111l1l_opy_.bstack1l11l11l1_opy_(config=self.config)
        self.bstack11111lll11l_opy_ = {}
        self.bstack1llll11l111_opy_ = False
        self.bstack11111ll1lll_opy_ = (
            self.__11111llll11_opy_()
            and self.bstack1l1ll1l111_opy_ is not None
            and self.bstack1l1ll1l111_opy_.bstack1ll11l1lll_opy_()
            and config.get(bstack11l1ll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᾓ"), None) is not None
            and config.get(bstack11l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᾔ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack1l11l11l1_opy_(cls, config, logger):
        if cls._1ll1l1lll11_opy_ is None and config is not None:
            cls._1ll1l1lll11_opy_ = bstack1l1lllll1l_opy_(config, logger)
        return cls._1ll1l1lll11_opy_
    def bstack1ll11l1lll_opy_(self):
        bstack11l1ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡉࡵࠠ࡯ࡱࡷࠤࡦࡶࡰ࡭ࡻࠣࡸࡪࡹࡴࠡࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡻ࡭࡫࡮࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡐ࠳࠴ࡽࠥ࡯ࡳࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡔࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡩࡴࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠣ࡭ࡸࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠥ࡯ࡳࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᾕ")
        return self.bstack11111ll1lll_opy_ and self.bstack11111llll1l_opy_()
    def bstack11111llll1l_opy_(self):
        bstack11111llllll_opy_ = os.getenv(bstack11l1ll1_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩᾖ"), self.config.get(bstack11l1ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᾗ"), None))
        return bstack11111llllll_opy_ in bstack11l1111l1ll_opy_
    def __11111llll11_opy_(self):
        bstack11l11l1l1l1_opy_ = False
        for fw in bstack11l111l1111_opy_:
            if fw in self.config.get(bstack11l1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᾘ"), bstack11l1ll1_opy_ (u"ࠫࠬᾙ")):
                bstack11l11l1l1l1_opy_ = True
        return bstack1ll1lll1l_opy_(self.config.get(bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᾚ"), bstack11l11l1l1l1_opy_))
    def bstack11111lll1ll_opy_(self):
        return (not self.bstack1ll11l1lll_opy_() and
                self.bstack1l1ll1l111_opy_ is not None and self.bstack1l1ll1l111_opy_.bstack1ll11l1lll_opy_())
    def bstack11111ll1l1l_opy_(self):
        if not self.bstack11111lll1ll_opy_():
            return
        if self.config.get(bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᾛ"), None) is None or self.config.get(bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᾜ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack11l1ll1_opy_ (u"ࠣࡖࡨࡷࡹࠦࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡧࡦࡴࠧࡵࠢࡺࡳࡷࡱࠠࡢࡵࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠦ࡯ࡳࠢࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠠࡪࡵࠣࡲࡺࡲ࡬࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡶࡩࡹࠦࡡࠡࡰࡲࡲ࠲ࡴࡵ࡭࡮ࠣࡺࡦࡲࡵࡦ࠰ࠥᾝ"))
        if not self.__11111llll11_opy_():
            self.logger.info(bstack11l1ll1_opy_ (u"ࠤࡗࡩࡸࡺࠠࡓࡧࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡨࡧ࡮ࠨࡶࠣࡻࡴࡸ࡫ࠡࡣࡶࠤࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠤ࡮ࡹࠠࡥ࡫ࡶࡥࡧࡲࡥࡥ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣࡩࡳࡧࡢ࡭ࡧࠣ࡭ࡹࠦࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡧ࡫࡯ࡩ࠳ࠨᾞ"))
    def bstack11111ll111l_opy_(self):
        return self.bstack1llll11l111_opy_
    def bstack1lllll11lll_opy_(self, bstack11111lllll1_opy_):
        self.bstack1llll11l111_opy_ = bstack11111lllll1_opy_
        self.bstack1lllll1111l_opy_(bstack11l1ll1_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡧࡧࠦᾟ"), bstack11111lllll1_opy_)
    def bstack1llll1ll1ll_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡠࡸࡥࡰࡴࡧࡩࡷࡥࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࡠࠤࡓࡵࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡰࡴࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫࠳ࠨᾠ"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack1l1ll1l111_opy_.bstack11111ll1ll1_opy_()
            if self.bstack1l1ll1l111_opy_ is not None:
                orchestration_strategy = self.bstack1l1ll1l111_opy_.bstack11llll1ll_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack11l1ll1_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡴࡳࡣࡷࡩ࡬ࡿࠠࡪࡵࠣࡒࡴࡴࡥ࠯ࠢࡆࡥࡳࡴ࡯ࡵࠢࡳࡶࡴࡩࡥࡦࡦࠣࡻ࡮ࡺࡨࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴ࠮ࠣᾡ"))
                return None
            self.logger.info(bstack11l1ll1_opy_ (u"ࠨࡒࡦࡱࡵࡨࡪࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡸ࡫ࡷ࡬ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡽࢀࠦᾢ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡖࡵ࡬ࡲ࡬ࠦࡃࡍࡋࠣࡪࡱࡵࡷࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥᾣ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡗࡶ࡭ࡳ࡭ࠠࡴࡦ࡮ࠤ࡫ࡲ࡯ࡸࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦᾤ"))
                self.bstack11111ll11l1_opy_.bstack11111ll11ll_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack11111ll11l1_opy_.bstack11111ll1l11_opy_()
            if not ordered_test_files:
                return None
            self.bstack1lllll1111l_opy_(bstack11l1ll1_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡉ࡯ࡶࡰࡷࠦᾥ"), len(test_files))
            self.bstack1lllll1111l_opy_(bstack11l1ll1_opy_ (u"ࠥࡲࡴࡪࡥࡊࡰࡧࡩࡽࠨᾦ"), int(os.environ.get(bstack11l1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢᾧ")) or bstack11l1ll1_opy_ (u"ࠧ࠶ࠢᾨ")))
            self.bstack1lllll1111l_opy_(bstack11l1ll1_opy_ (u"ࠨࡴࡰࡶࡤࡰࡓࡵࡤࡦࡵࠥᾩ"), int(os.environ.get(bstack11l1ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥᾪ")) or bstack11l1ll1_opy_ (u"ࠣ࠳ࠥᾫ")))
            self.bstack1lllll1111l_opy_(bstack11l1ll1_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩ࡚ࡥࡴࡶࡉ࡭ࡱ࡫ࡳࡄࡱࡸࡲࡹࠨᾬ"), len(ordered_test_files))
            self.bstack1lllll1111l_opy_(bstack11l1ll1_opy_ (u"ࠥࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹࡁࡑࡋࡆࡥࡱࡲࡃࡰࡷࡱࡸࠧᾭ"), self.bstack11111ll11l1_opy_.bstack11111lll111_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡠࡸࡥࡰࡴࡧࡩࡷࡥࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࡠࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦ࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣ࡭ࡣࡶࡷࡪࡹ࠺ࠡࡽࢀࠦᾮ").format(e))
        return None
    def bstack1lllll1111l_opy_(self, key, value):
        self.bstack11111lll11l_opy_[key] = value
    def bstack1ll111l11l_opy_(self):
        return self.bstack11111lll11l_opy_