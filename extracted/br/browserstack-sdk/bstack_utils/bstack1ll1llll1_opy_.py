# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11l111l1l1l_opy_ import bstack11l111ll111_opy_
from bstack_utils.constants import bstack11l11111lll_opy_, bstack1l11l111l1_opy_
from bstack_utils.bstack1lll1ll11l_opy_ import bstack1lllll111_opy_
from bstack_utils import bstack1l11l1l1l_opy_
bstack111lll111l1_opy_ = 10
class bstack1ll1l1ll11_opy_:
    def __init__(self, bstack1l11ll11ll_opy_, config, bstack11ll1ll1ll1_opy_=0):
        self.bstack111lll1l1l1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111lll1l111_opy_ = bstack11l1111_opy_ (u"ࠨࡻࡾ࠱ࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡦࡢ࡫࡯ࡩࡩ࠳ࡴࡦࡵࡷࡷࠧ᭳").format(bstack11l11111lll_opy_)
        self.bstack111lll1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣ᭴").format(os.environ.get(bstack11l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᭵"))))
        self.bstack111lll11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣ᭶").format(os.environ.get(bstack11l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᭷"))))
        self.bstack111lll11l1l_opy_ = 2
        self.bstack1l11ll11ll_opy_ = bstack1l11ll11ll_opy_
        self.config = config
        self.logger = bstack1l11l1l1l_opy_.get_logger(__name__, bstack1l11l111l1_opy_)
        self.bstack11ll1ll1ll1_opy_ = bstack11ll1ll1ll1_opy_
        self.bstack111lll11111_opy_ = False
        self.bstack111lll11ll1_opy_ = not (
                            os.environ.get(bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥ᭸")) and
                            os.environ.get(bstack11l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣ᭹")) and
                            os.environ.get(bstack11l1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣ᭺"))
                        )
        if bstack1lllll111_opy_.bstack11ll1ll111l_opy_(config):
            self.bstack111lll11l1l_opy_ = bstack1lllll111_opy_.bstack11ll11lll1l_opy_(config, self.bstack11ll1ll1ll1_opy_)
            self.bstack111ll1llll1_opy_()
    def bstack111ll1ll1ll_opy_(self):
        return bstack11l1111_opy_ (u"ࠢࡼࡿࡢࡿࢂࠨ᭻").format(self.config.get(bstack11l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ᭼")), os.environ.get(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ᭽")))
    def bstack111ll1lllll_opy_(self):
        try:
            if self.bstack111lll11ll1_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111lll11l11_opy_, bstack11l1111_opy_ (u"ࠥࡶࠧ᭾")) as f:
                        bstack111lll1111l_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111lll1111l_opy_ = set()
                bstack111ll1lll11_opy_ = bstack111lll1111l_opy_ - self.bstack111lll1l1l1_opy_
                if not bstack111ll1lll11_opy_:
                    return
                self.bstack111lll1l1l1_opy_.update(bstack111ll1lll11_opy_)
                data = {bstack11l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࠤ᭿"): list(self.bstack111lll1l1l1_opy_), bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣᮀ"): self.config.get(bstack11l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᮁ")), bstack11l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧᮂ"): os.environ.get(bstack11l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᮃ")), bstack11l1111_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢᮄ"): self.config.get(bstack11l1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᮅ"))}
            response = bstack11l111ll111_opy_.bstack111lll11lll_opy_(self.bstack111lll1l111_opy_, data)
            if response.get(bstack11l1111_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᮆ")) == 200:
                self.logger.debug(bstack11l1111_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡸ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧᮇ").format(data))
            else:
                self.logger.debug(bstack11l1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥᮈ").format(response))
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡷࡪࡴࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢᮉ").format(e))
    def bstack111ll1ll1l1_opy_(self):
        if self.bstack111lll11ll1_opy_:
            with self.lock:
                try:
                    with open(self.bstack111lll11l11_opy_, bstack11l1111_opy_ (u"ࠣࡴࠥᮊ")) as f:
                        bstack111ll1ll11l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111ll1ll11l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11l1111_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠧᮋ").format(failed_count))
                if failed_count >= self.bstack111lll11l1l_opy_:
                    self.logger.info(bstack11l1111_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦᮌ").format(failed_count, self.bstack111lll11l1l_opy_))
                    self.bstack111ll1ll111_opy_(failed_count)
                    self.bstack111lll11111_opy_ = True
            return
        try:
            response = bstack11l111ll111_opy_.bstack111ll1ll1l1_opy_(bstack11l1111_opy_ (u"ࠦࢀࢃ࠿ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࡀࡿࢂࠬࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࡁࢀࢃࠦࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࡂࢁࡽࠣᮍ").format(self.bstack111lll1l111_opy_, self.config.get(bstack11l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᮎ")), os.environ.get(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬᮏ")), self.config.get(bstack11l1111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᮐ"))))
            if response.get(bstack11l1111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᮑ")) == 200:
                failed_count = response.get(bstack11l1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࡃࡰࡷࡱࡸࠧᮒ"), 0)
                self.logger.debug(bstack11l1111_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧᮓ").format(failed_count))
                if failed_count >= self.bstack111lll11l1l_opy_:
                    self.logger.info(bstack11l1111_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦᮔ").format(failed_count, self.bstack111lll11l1l_opy_))
                    self.bstack111ll1ll111_opy_(failed_count)
                    self.bstack111lll11111_opy_ = True
            else:
                self.logger.error(bstack11l1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡰࡱࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤᮕ").format(response))
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡳࡱࡲࡩ࡯ࡩ࠽ࠤࢀࢃࠢᮖ").format(e))
    def bstack111ll1ll111_opy_(self, failed_count):
        with open(self.bstack111lll1l11l_opy_, bstack11l1111_opy_ (u"ࠢࡸࠤᮗ")) as f:
            f.write(bstack11l1111_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥࡧࡴࠡࡽࢀࡠࡳࠨᮘ").format(datetime.now()))
            f.write(bstack11l1111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࡠࡳࠨᮙ").format(failed_count))
        self.logger.debug(bstack11l1111_opy_ (u"ࠥࡅࡧࡵࡲࡵࠢࡅࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࢀࠦᮚ").format(self.bstack111lll1l11l_opy_))
    def bstack111ll1llll1_opy_(self):
        def bstack111ll1lll1l_opy_():
            while not self.bstack111lll11111_opy_:
                time.sleep(bstack111lll111l1_opy_)
                self.bstack111ll1lllll_opy_()
                self.bstack111ll1ll1l1_opy_()
        bstack111lll111ll_opy_ = threading.Thread(target=bstack111ll1lll1l_opy_, daemon=True)
        bstack111lll111ll_opy_.start()