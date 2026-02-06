# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11l11ll11l1_opy_ import bstack11l11ll1l11_opy_
from bstack_utils.constants import bstack11l111ll1ll_opy_, bstack111l1l11ll_opy_
from bstack_utils.bstack1lll1111l1_opy_ import bstack11l1lll11_opy_
from bstack_utils import logger_utils
bstack111lll11lll_opy_ = 10
class bstack1111l1ll1_opy_:
    def __init__(self, bstack1l1111ll1l_opy_, config, bstack111lll1llll_opy_=0):
        self.bstack111lll1l11l_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111lll11ll1_opy_ = bstack11lllll_opy_ (u"ࠥࡿࢂ࠵ࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡪࡦ࡯࡬ࡦࡦ࠰ࡸࡪࡹࡴࡴࠤᰭ").format(bstack11l111ll1ll_opy_)
        self.bstack111llll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧᰮ").format(os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᰯ"))))
        self.bstack111lll11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧᰰ").format(os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᰱ"))))
        self.bstack111lll1ll1l_opy_ = 2
        self.bstack1l1111ll1l_opy_ = bstack1l1111ll1l_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack111l1l11ll_opy_)
        self.bstack111lll1llll_opy_ = bstack111lll1llll_opy_
        self.bstack111llll1111_opy_ = False
        self.bstack111lllll111_opy_ = not (
                            os.environ.get(bstack11lllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢᰲ")) and
                            os.environ.get(bstack11lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧᰳ")) and
                            os.environ.get(bstack11lllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧᰴ"))
                        )
        if bstack11l1lll11_opy_.bstack111lll1l1l1_opy_(config):
            self.bstack111lll1ll1l_opy_ = bstack11l1lll11_opy_.bstack111llll1l11_opy_(config, self.bstack111lll1llll_opy_)
            self.bstack111lll1l1ll_opy_()
    def bstack111lll1l111_opy_(self):
        return bstack11lllll_opy_ (u"ࠦࢀࢃ࡟ࡼࡿࠥᰵ").format(self.config.get(bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᰶ")), os.environ.get(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ᰷ࠬ")))
    def bstack111lll1ll11_opy_(self):
        try:
            if self.bstack111lllll111_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111lll11l11_opy_, bstack11lllll_opy_ (u"ࠢࡳࠤ᰸")) as f:
                        bstack111lll1lll1_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111lll1lll1_opy_ = set()
                bstack111llll111l_opy_ = bstack111lll1lll1_opy_ - self.bstack111lll1l11l_opy_
                if not bstack111llll111l_opy_:
                    return
                self.bstack111lll1l11l_opy_.update(bstack111llll111l_opy_)
                data = {bstack11lllll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࠨ᰹"): list(self.bstack111lll1l11l_opy_), bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ᰺"): self.config.get(bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᰻")), bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ᰼"): os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ᰽")), bstack11lllll_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ᰾"): self.config.get(bstack11lllll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᰿"))}
            response = bstack11l11ll1l11_opy_.bstack111lllll11l_opy_(self.bstack111lll11ll1_opy_, data)
            if response.get(bstack11lllll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᱀")) == 200:
                self.logger.debug(bstack11lllll_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡵࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ᱁").format(data))
            else:
                self.logger.debug(bstack11lllll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢ᱂").format(response))
        except Exception as e:
            self.logger.debug(bstack11lllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ᱃").format(e))
    def bstack111llll11ll_opy_(self):
        if self.bstack111lllll111_opy_:
            with self.lock:
                try:
                    with open(self.bstack111lll11l11_opy_, bstack11lllll_opy_ (u"ࠧࡸࠢ᱄")) as f:
                        bstack111llll1l1l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111llll1l1l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11lllll_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠤ᱅").format(failed_count))
                if failed_count >= self.bstack111lll1ll1l_opy_:
                    self.logger.info(bstack11lllll_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣ᱆").format(failed_count, self.bstack111lll1ll1l_opy_))
                    self.bstack111lll11l1l_opy_(failed_count)
                    self.bstack111llll1111_opy_ = True
            return
        try:
            response = bstack11l11ll1l11_opy_.bstack111llll11ll_opy_(bstack11lllll_opy_ (u"ࠣࡽࢀࡃࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫࠽ࡼࡿࠩࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲ࠾ࡽࢀࠪࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦ࠿ࡾࢁࠧ᱇").format(self.bstack111lll11ll1_opy_, self.config.get(bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ᱈")), os.environ.get(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ᱉")), self.config.get(bstack11lllll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ᱊"))))
            if response.get(bstack11lllll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ᱋")) == 200:
                failed_count = response.get(bstack11lllll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࡇࡴࡻ࡮ࡵࠤ᱌"), 0)
                self.logger.debug(bstack11lllll_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤᱍ").format(failed_count))
                if failed_count >= self.bstack111lll1ll1l_opy_:
                    self.logger.info(bstack11lllll_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨ࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣᱎ").format(failed_count, self.bstack111lll1ll1l_opy_))
                    self.bstack111lll11l1l_opy_(failed_count)
                    self.bstack111llll1111_opy_ = True
            else:
                self.logger.error(bstack11lllll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯࡭࡮ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨᱏ").format(response))
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡰ࡮࡯࡭ࡳ࡭࠺ࠡࡽࢀࠦ᱐").format(e))
    def bstack111lll11l1l_opy_(self, failed_count):
        with open(self.bstack111llll11l1_opy_, bstack11lllll_opy_ (u"ࠦࡼࠨ᱑")) as f:
            f.write(bstack11lllll_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࡤࡸࠥࢁࡽ࡝ࡰࠥ᱒").format(datetime.now()))
            f.write(bstack11lllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽ࡝ࡰࠥ᱓").format(failed_count))
        self.logger.debug(bstack11lllll_opy_ (u"ࠢࡂࡤࡲࡶࡹࠦࡂࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡽࠣ᱔").format(self.bstack111llll11l1_opy_))
    def bstack111lll1l1ll_opy_(self):
        def bstack111llll1lll_opy_():
            while not self.bstack111llll1111_opy_:
                time.sleep(bstack111lll11lll_opy_)
                self.bstack111lll1ll11_opy_()
                self.bstack111llll11ll_opy_()
        bstack111llll1ll1_opy_ = threading.Thread(target=bstack111llll1lll_opy_, daemon=True)
        bstack111llll1ll1_opy_.start()