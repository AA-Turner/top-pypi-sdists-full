# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111l1ll11l1_opy_ import bstack111l1ll1111_opy_
from bstack_utils.constants import bstack111l11ll1ll_opy_, bstack11l11llll1_opy_
from bstack_utils.bstack1l1l1llll1_opy_ import bstack1l1ll11ll1_opy_
from bstack_utils import logger_utils
bstack1111ll1ll1l_opy_ = 10
class bstack1ll1l1ll1l_opy_:
    def __init__(self, bstack11lll11ll1_opy_, config, bstack1111ll1llll_opy_=0):
        self.bstack1111ll11ll1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1111ll11l11_opy_ = bstack1ll11_opy_ (u"ࠤࡾࢁ࠴ࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡩࡥ࡮ࡲࡥࡥ࠯ࡷࡩࡸࡺࡳࠣὦ").format(bstack111l11ll1ll_opy_)
        self.bstack1111lll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦὧ").format(os.environ.get(bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩὨ"))))
        self.bstack1111ll1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࢀࢃ࠮ࡵࡺࡷࠦὩ").format(os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫὪ"))))
        self.bstack1111ll1l111_opy_ = 2
        self.bstack11lll11ll1_opy_ = bstack11lll11ll1_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack11l11llll1_opy_)
        self.bstack1111ll1llll_opy_ = bstack1111ll1llll_opy_
        self.bstack1111lll1111_opy_ = False
        self.bstack1111lll111l_opy_ = not (
                            os.environ.get(bstack1ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࠨὫ")) and
                            os.environ.get(bstack1ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦὬ")) and
                            os.environ.get(bstack1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦὭ"))
                        )
        if bstack1l1ll11ll1_opy_.bstack1111ll1lll1_opy_(config):
            self.bstack1111ll1l111_opy_ = bstack1l1ll11ll1_opy_.bstack1111ll1l11l_opy_(config, self.bstack1111ll1llll_opy_)
            self.bstack1111lll1lll_opy_()
    def bstack1111lll1ll1_opy_(self):
        return bstack1ll11_opy_ (u"ࠥࡿࢂࡥࡻࡾࠤὮ").format(self.config.get(bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧὯ")), os.environ.get(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫὰ")))
    def bstack1111ll11lll_opy_(self):
        try:
            if self.bstack1111lll111l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1111ll1l1l1_opy_, bstack1ll11_opy_ (u"ࠨࡲࠣά")) as f:
                        bstack1111lll1l11_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1111lll1l11_opy_ = set()
                bstack1111ll111ll_opy_ = bstack1111lll1l11_opy_ - self.bstack1111ll11ll1_opy_
                if not bstack1111ll111ll_opy_:
                    return
                self.bstack1111ll11ll1_opy_.update(bstack1111ll111ll_opy_)
                data = {bstack1ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࡔࡦࡵࡷࡷࠧὲ"): list(self.bstack1111ll11ll1_opy_), bstack1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦέ"): self.config.get(bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬὴ")), bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣή"): os.environ.get(bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪὶ")), bstack1ll11_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥί"): self.config.get(bstack1ll11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫὸ"))}
            response = bstack111l1ll1111_opy_.bstack1111ll1ll11_opy_(self.bstack1111ll11l11_opy_, data)
            if response.get(bstack1ll11_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢό")) == 200:
                self.logger.debug(bstack1ll11_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡴࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣὺ").format(data))
            else:
                self.logger.debug(bstack1ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨύ").format(response))
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥὼ").format(e))
    def bstack1111lll11ll_opy_(self):
        if self.bstack1111lll111l_opy_:
            with self.lock:
                try:
                    with open(self.bstack1111ll1l1l1_opy_, bstack1ll11_opy_ (u"ࠦࡷࠨώ")) as f:
                        bstack1111ll1l1ll_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1111ll1l1ll_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1ll11_opy_ (u"ࠧࡖ࡯࡭࡮ࡨࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠣ὾").format(failed_count))
                if failed_count >= self.bstack1111ll1l111_opy_:
                    self.logger.info(bstack1ll11_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢ὿").format(failed_count, self.bstack1111ll1l111_opy_))
                    self.bstack1111ll11l1l_opy_(failed_count)
                    self.bstack1111lll1111_opy_ = True
            return
        try:
            response = bstack111l1ll1111_opy_.bstack1111lll11ll_opy_(bstack1ll11_opy_ (u"ࠢࡼࡿࡂࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࡃࡻࡾࠨࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࠽ࡼࡿࠩࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥ࠾ࡽࢀࠦᾀ").format(self.bstack1111ll11l11_opy_, self.config.get(bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᾁ")), os.environ.get(bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᾂ")), self.config.get(bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᾃ"))))
            if response.get(bstack1ll11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᾄ")) == 200:
                failed_count = response.get(bstack1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࡆࡳࡺࡴࡴࠣᾅ"), 0)
                self.logger.debug(bstack1ll11_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽࠣᾆ").format(failed_count))
                if failed_count >= self.bstack1111ll1l111_opy_:
                    self.logger.info(bstack1ll11_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢᾇ").format(failed_count, self.bstack1111ll1l111_opy_))
                    self.bstack1111ll11l1l_opy_(failed_count)
                    self.bstack1111lll1111_opy_ = True
            else:
                self.logger.error(bstack1ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡵ࡬࡭ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧᾈ").format(response))
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡶ࡯࡭࡮࡬ࡲ࡬ࡀࠠࡼࡿࠥᾉ").format(e))
    def bstack1111ll11l1l_opy_(self, failed_count):
        with open(self.bstack1111lll1l1l_opy_, bstack1ll11_opy_ (u"ࠥࡻࠧᾊ")) as f:
            f.write(bstack1ll11_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࡣࡷࠤࢀࢃ࡜࡯ࠤᾋ").format(datetime.now()))
            f.write(bstack1ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃ࡜࡯ࠤᾌ").format(failed_count))
        self.logger.debug(bstack1ll11_opy_ (u"ࠨࡁࡣࡱࡵࡸࠥࡈࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡦࡦ࠽ࠤࢀࢃࠢᾍ").format(self.bstack1111lll1l1l_opy_))
    def bstack1111lll1lll_opy_(self):
        def bstack1111llll111_opy_():
            while not self.bstack1111lll1111_opy_:
                time.sleep(bstack1111ll1ll1l_opy_)
                self.bstack1111ll11lll_opy_()
                self.bstack1111lll11ll_opy_()
        bstack1111lll11l1_opy_ = threading.Thread(target=bstack1111llll111_opy_, daemon=True)
        bstack1111lll11l1_opy_.start()